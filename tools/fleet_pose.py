# Night Fleet, part 3: every 20s the lord raises his whole arm from the shoulder,
# holds the blade high in a pose, leans back, then slashes down with a light
# streak, his body pitching forward and his cape swinging after. Runs after fleet_doom.py.
import sys, math
import xml.etree.ElementTree as ET
SVGNS = 'http://www.w3.org/2000/svg'; NS = '{%s}' % SVGNS
ET.register_namespace('', SVGNS)
src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
head, svg, tail = s[:s.index('`') + 1], s[s.index('`') + 1:s.rindex('`')], s[s.rindex('`'):]
root = ET.fromstring(svg)

C = 45  # seconds per pose cycle
SH = (-136, -494)    # shoulder pivot (lord units)
HI = (-223.8, -271.2)  # hilt / wrist pivot
# arm angle over the cycle: idle, raise, hold high, slash past rest, settle
ARM = [(0, 0), (77.8, 0), (83.6, 58), (85, 55), (89.8, 57, 'cubic-bezier(.55,0,.85,.4)'), (91.1, -12), (92.4, 3), (96, 0), (100, 0)]
WRIST = [(0, 0), (77.8, 0), (83.6, 100), (85, 97), (89.6, 102, 'cubic-bezier(.55,0,.85,.4)'), (90.9, -18), (92.4, 4), (96, 0), (100, 0)]
LEAN = [(0, 0), (77.8, 0), (83.6, -1.2), (89.8, -1.4), (91.1, 1.6), (94, 0), (100, 0)]
CAPE = [(0, 0), (77.8, 0), (83.6, 1), (89.8, 1), (91.3, -1), (92.6, -4.5), (94.6, 2), (96.8, -.6), (98.5, 0), (100, 0)]

def kf(name, pts, fmt):
    return '@keyframes %s{%s}' % (name, ''.join('%s%%{transform:%s%s}' % (('%.1f' % q[0]).rstrip('0').rstrip('.'), fmt % q[1], (';animation-timing-function:' + q[2]) if len(q) > 2 else '') for q in pts))

css = ('.pArm{animation:pArm %(c)ss cubic-bezier(.45,0,.4,1) infinite}\n'
       '.pWr{animation:pWr %(c)ss ease-in-out infinite}\n'
       '.pLean{animation:pLean %(c)ss ease-in-out infinite}\n'
       '.pCape{animation:pCape %(c)ss ease-in-out infinite;transform-box:fill-box;transform-origin:50%% 0}\n'
       '.pStreak{animation:pStreak %(c)ss linear infinite;opacity:0}\n'
       '@keyframes pStreak{0%%,90.95%%{opacity:0}91.25%%{opacity:.8}92.2%%{opacity:.3}93%%,100%%{opacity:0}}\n'
       '.pFlare{animation:pFlare %(c)ss ease-in-out infinite;opacity:0}\n'
       '@keyframes pFlare{0%%,78%%{opacity:0}83.6%%,89.8%%{opacity:1}91.5%%,100%%{opacity:0}}\n') % {'c': C}
css += kf('pArm', ARM, 'rotate(%gdeg)') + '\n' + kf('pWr', WRIST, 'rotate(%gdeg)') + '\n' \
    + kf('pLean', LEAN, 'rotate(%gdeg)') + '\n' + kf('pCape', CAPE, 'skewX(%gdeg)') + '\n'
style = root.find(NS + 'style')
# keep reduced-motion last so it still wins
t = style.text
i = t.index('@media (prefers-reduced-motion')
style.text = t[:i] + css + t[i:]

lord = [e for e in root.iter(NS + 'g') if e.get('transform') == 'translate(1175,1000) scale(.93)'][0]
kids = list(lord)

def pivot(pt, cls, children):
    o = ET.Element(NS + 'g', {'transform': 'translate(%g,%g)' % pt})
    a = ET.SubElement(o, NS + 'g', {'class': cls})
    inner = ET.SubElement(a, NS + 'g', {'transform': 'translate(%g,%g)' % (-pt[0], -pt[1])})
    for c in children:
        inner.append(c)
    return o, inner

def idx(pred):
    return [i for i, k in enumerate(kids) if pred(k)][0]

i_fore = idx(lambda k: k.get('d', '').startswith('M-208.2,-320.8'))
i_breath = idx(lambda k: k.get('class') == 'hood-breath')
i_halo = idx(lambda k: k.get('fill') == 'url(#hood-halo)')
i_core = idx(lambda k: k.get('stroke') == '#ffe6de')
i_cape = idx(lambda k: k.get('class') == 'hood-cape')
arm = kids[i_fore:i_breath]            # forearm, hand, sleeve
blade = kids[i_halo:i_core + 1]        # glow, blade, core
for k in arm + blade:
    lord.remove(k)

# arm: rotates about the shoulder
armG, _ = pivot(SH, 'pArm', arm)
# blade: rotates about the shoulder with the arm, plus the wrist on top
wr, _ = pivot(HI, 'pWr', blade)
bladeG, _ = pivot(SH, 'pArm', [wr])
# a hot flare on the blade while it is held high
fl = ET.SubElement(wr[0][0], NS + 'path', {'class': 'pFlare', 'd': 'M-224.4,-269.3L-287.4,-68.9', 'stroke': '#ff6a5a',
                                            'stroke-width': '14', 'stroke-opacity': '.35', 'stroke-linecap': 'round'})
kids = list(lord)
pos_breath = kids.index([k for k in kids if k.get('class') == 'hood-breath'][0])
lord.insert(pos_breath, armG)
lord.insert(pos_breath + 2, bladeG)

# streak: the arc the blade tip sweeps through during the slash
tip = (-289.0, -60.0)
vx, vy = tip[0] - SH[0], tip[1] - SH[1]
def rot(a):
    r = math.radians(a)
    return SH[0] + vx * math.cos(r) - vy * math.sin(r), SH[1] + vx * math.sin(r) + vy * math.cos(r)
def arc(a0, a1, n=24):
    return 'M' + ' L'.join('%.1f,%.1f' % rot(a0 + (a1 - a0) * k / n) for k in range(n + 1))
hil = lambda a: (SH[0] + (HI[0] - SH[0]) * math.cos(math.radians(a)) - (HI[1] - SH[1]) * math.sin(math.radians(a)),
                 SH[1] + (HI[0] - SH[0]) * math.sin(math.radians(a)) + (HI[1] - SH[1]) * math.cos(math.radians(a)))
st = ET.Element(NS + 'g', {'class': 'pStreak'})
# a filled fan between hilt path and tip path for a soft swoosh
a0, a1 = 78, -22
outer = [rot(a0 + (a1 - a0) * k / 24) for k in range(25)]
inner = [hil(a0 + (a1 - a0) * k / 24) for k in range(25)][::-1]
def R(p, c, a):
    r = math.radians(a); x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(r) - y * math.sin(r), c[1] + x * math.sin(r) + y * math.cos(r)
def tipat(f):  # f 0..1 through the slash
    arm = 57 + (-12 - 57) * f; wr = 102 + (-18 - 102) * f
    return R(R(tip, HI, wr), SH, arm)
def path(f0, f1, n=24):
    return 'M' + ' L'.join('%.1f,%.1f' % tipat(f0 + (f1 - f0) * k / n) for k in range(n + 1))
ET.SubElement(st, NS + 'path', {'d': path(.05, 1), 'stroke': '#ff3a40', 'stroke-width': '12', 'stroke-opacity': '.3',
                                'fill': 'none', 'stroke-linecap': 'round'})
ET.SubElement(st, NS + 'path', {'d': path(.45, 1), 'stroke': '#ffd6cc', 'stroke-width': '3', 'stroke-opacity': '.75',
                                'fill': 'none', 'stroke-linecap': 'round'})
kids = list(lord)
lord.insert(kids.index(bladeG), st)

# cape swings after the slash (wrap the existing animated cape so both run)
kids = list(lord)
cape = [k for k in kids if k.get('class') == 'hood-cape'][0]
ci = kids.index(cape); lord.remove(cape)
cw = ET.Element(NS + 'g', {'class': 'pCape'}); cw.append(cape); lord.insert(ci, cw)

# whole body leans back, then pitches into the slash (pivot at the feet)
body = list(lord)
keep = [k for k in body if (k.get('class') or '') == 'fog' or (k.get('class') or '') == 'ember']
moving = [k for k in body if k not in keep]
for k in moving:
    lord.remove(k)
leanG, _ = pivot((-40, 0), 'pLean', moving)
lord.insert(2, leanG)

out = ET.tostring(root, encoding='unicode').replace(' />', '/>')
open(out_path, 'w', encoding='utf-8').write(head + out + tail)
print('chars', len(out), 'arm parts', len(arm), 'blade parts', len(blade))
