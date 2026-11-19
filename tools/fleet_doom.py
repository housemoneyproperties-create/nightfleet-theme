# Night Fleet, part 2: a smooth cracked-sphere battle station that charges,
# fires and blows the moon apart (then a new moon drifts back in), and the lord
# now swings his blade every so often. Runs after fleet_ships.py.
import sys, math, random
import xml.etree.ElementTree as ET
SVGNS = 'http://www.w3.org/2000/svg'; NS = '{%s}' % SVGNS
ET.register_namespace('', SVGNS)
random.seed(9)
FK = []

def fk(dx, dy, rot):
    n = 'fr%d' % len(FK)
    FK.append('@keyframes %s{0%%,58.6%%{opacity:0;transform:translate(0,0) rotate(0)}59.3%%{opacity:1;transform:translate(%.0fpx,%.0fpx) rotate(%.0fdeg)}82%%{opacity:.85}90%%,100%%{opacity:0;transform:translate(%.0fpx,%.0fpx) rotate(%.0fdeg)}}' % (n, dx*.12, dy*.12, rot*.1, dx, dy, rot))
    return n


src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
head, svg, tail = s[:s.index('`') + 1], s[s.index('`') + 1:s.rindex('`')], s[s.rindex('`'):]
root = ET.fromstring(svg)
parent = {c: p for p in root.iter() for c in p}


def frag(xml):
    return list(ET.fromstring('<g xmlns="%s">%s</g>' % (SVGNS, xml)))


CYCLE = 60  # seconds for charge -> fire -> blast -> new moon
style = root.find(NS + 'style')
t = style.text
a, b = t.index('.charge{'), t.index('@media (max-aspect-ratio:3/4)')
t = t[:a] + (
    '.charge{animation:charge %(c)ss ease-in infinite}\n'
    '@keyframes charge{0%%{opacity:.25}54%%{opacity:1}57%%{opacity:1}59%%{opacity:.15}100%%{opacity:.25}}\n'
    '.beam{animation:beam %(c)ss linear infinite;opacity:0}\n'
    '@keyframes beam{0%%,54.5%%{opacity:0}55%%{opacity:1}58%%{opacity:1}59%%,100%%{opacity:0}}\n'
    '.mcrack{animation:mcrack %(c)ss ease-in infinite;opacity:0}\n'
    '@keyframes mcrack{0%%,55%%{opacity:0}57.8%%{opacity:1}58.3%%,100%%{opacity:0}}\n'
    '.moonA{animation:moonA %(c)ss linear infinite}\n'
    '@keyframes moonA{0%%,58%%{opacity:1}58.4%%,88%%{opacity:0}100%%{opacity:1}}\n'
    '.blast{animation:blast %(c)ss ease-out infinite;opacity:0;transform-box:fill-box;transform-origin:center}\n'
    '@keyframes blast{0%%,58%%{opacity:0;transform:scale(.2)}59%%{opacity:1;transform:scale(1)}66%%{opacity:0;transform:scale(1.7)}100%%{opacity:0}}\n'
    '.shock{animation:shock %(c)ss ease-out infinite;opacity:0;transform-box:fill-box;transform-origin:center}\n'
    '@keyframes shock{0%%,58.2%%{opacity:0;transform:scale(.2)}59%%{opacity:1;transform:scale(1)}72%%{opacity:0;transform:scale(7)}100%%{opacity:0}}\n'
    '.ash{animation:ash %(c)ss ease-out infinite;opacity:0}\n'
    '@keyframes ash{0%%,58.5%%{opacity:0}62%%{opacity:.8}86%%{opacity:0}100%%{opacity:0}}\n'
    '.frag{animation-duration:%(c)ss;animation-timing-function:cubic-bezier(.15,.7,.3,1);animation-iteration-count:infinite;opacity:0;transform-box:fill-box;transform-origin:center}\n'
    '.flash{animation:flash %(c)ss ease-out infinite;opacity:0}\n'
    '@keyframes flash{0%%,58.3%%{opacity:0}59%%{opacity:.5}64%%{opacity:.18}75%%,100%%{opacity:0}}\n'
    '.shake{animation:shake %(c)ss linear infinite}\n'
    '@keyframes shake{0%%,60.4%%{transform:translate(0,0)}60.8%%{transform:translate(5px,-3px)}61.2%%{transform:translate(-4px,3px)}61.6%%{transform:translate(3px,2px)}62%%{transform:translate(-2px,-1px)}62.6%%,100%%{transform:translate(0,0)}}\n'
) % {'c': CYCLE} + t[b:]
style.text = t

# ---- remove the spiked station, its beam, the impact and the old moon ----
left = [e for e in root.iter(NS + 'g') if e.get('class') == 'leftFill'][0]
for g in list(left):
    tr = g.get('transform') or ''
    if tr.startswith('translate(255,235)') or tr.startswith('translate(160,700)') or tr.startswith('translate(95,820)') or g.get('class') == 'beam':
        left.remove(g)

defs = root.find(NS + 'defs')
for x in frag('<radialGradient id="sphG" cx="68%" cy="30%" r="80%"><stop offset="0" stop-color="#8a9099"/><stop offset=".35" stop-color="#4a4f58"/>'
              '<stop offset=".75" stop-color="#1c1e23"/><stop offset="1" stop-color="#08090b"/></radialGradient>'
              '<radialGradient id="rockG" cx="30%" cy="30%" r="90%"><stop offset="0" stop-color="#6a2a22"/><stop offset=".5" stop-color="#2a0e10"/><stop offset="1" stop-color="#0c0405"/></radialGradient>'
              '<radialGradient id="flashG"><stop offset="0" stop-color="#fff0d8" stop-opacity="1"/><stop offset=".12" stop-color="#ffb070" stop-opacity=".7"/><stop offset=".45" stop-color="#ff5a3a" stop-opacity=".25"/><stop offset="1" stop-color="#ff3b2a" stop-opacity="0"/></radialGradient>'
              '<radialGradient id="rimG" cx="50%" cy="50%" r="50%"><stop offset=".82" stop-color="#ff2d3d" stop-opacity="0"/>'
              '<stop offset=".97" stop-color="#ff2d3d" stop-opacity=".45"/><stop offset="1" stop-color="#ff2d3d" stop-opacity="0"/></radialGradient>'):
    defs.append(x)

# ---- the moon: intact, cracking, then shattering ----
MX, MY, MR = 95, 820, 180
P = ['<circle cx="%d" cy="%d" r="1500" fill="url(#flashG)" class="flash"/>' % (MX, MY), '<g transform="translate(%d,%d)">' % (MX, MY),
     '<g class="moonA"><g transform="scale(.62)"><circle r="345" fill="url(#atmoGlow)" class="glowpulse"/>'
     '<circle r="290" fill="url(#planetG)"/><circle r="290" fill="url(#shadeG)"/></g></g>']
# glowing cracks that open just before it goes
cr = []
for i in range(7):
    a = math.radians(-60 + i * 22 + random.uniform(-6, 6)); r = 0
    pts = [(38 * math.cos(a), -38 * math.sin(a) * -1)]
    x, y = 40, -40
    path = 'M40,-40'
    for k in range(4):
        r += random.uniform(30, 48)
        aa = a + random.uniform(-.35, .35)
        path += ' L%.1f,%.1f' % (40 + r * math.cos(aa) * -1, -40 + r * math.sin(aa))
    cr.append('<path d="%s" stroke="#ffb36b" stroke-width="%.1f" fill="none" stroke-linecap="round"/>' % (path, random.uniform(2, 4.5)))
P.append('<g class="mcrack"><circle cx="40" cy="-40" r="30" fill="url(#coreG)"/>' + ''.join(cr) + '</g>')
# shattered pieces: wedges of the disc flung outward
N = 18
JIT = [0] + [random.uniform(-.35, .35) for _ in range(N - 1)]
for i in range(N):
    a1 = 2 * math.pi * (i + JIT[i]) / N; a2 = 2 * math.pi * (i + 1 + JIT[(i + 1) % N] + (N if i == N - 1 else 0) * 0) / N
    r_in = random.uniform(0, 50); pts = []
    for k in range(4):
        aa = a1 + (a2 - a1) * k / 3
        rr = MR * random.uniform(.82, 1.0)
        pts.append((rr * math.cos(aa), rr * math.sin(aa)))
    pts.append((r_in * math.cos((a1 + a2) / 2), r_in * math.sin((a1 + a2) / 2)))
    am = (a1 + a2) / 2; dist = random.uniform(260, 520)
    dx, dy, rot = dist * math.cos(am), dist * math.sin(am), random.uniform(-260, 260)
    fill = random.choice(['url(#rockG)', 'url(#rockG)', '#1d0b0d'])
    P.append('<polygon class="frag %s" points="%s" fill="%s" stroke="#ff7a4a" stroke-width="1.6" stroke-opacity=".55"/>'
             % (fk(dx, dy, rot), ' '.join('%.1f,%.1f' % q for q in pts), fill))
for i in range(26):  # small burning rubble
    am = random.uniform(0, 2 * math.pi); dist = random.uniform(200, 640); k = random.uniform(3, 9)
    P.append('<circle class="frag %s" cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>'
             % (fk(dist * math.cos(am), dist * math.sin(am), 0), random.uniform(-60, 60), random.uniform(-60, 60), k, random.choice(['#ff7a3a', '#ffb36b', '#d0283a'])))
P.append('<circle r="230" fill="url(#coreG)" class="ash"/>')
P.append('<circle r="190" fill="url(#boomG)" class="blast"/>')
P.append('<circle r="70" fill="none" stroke="#ffc58a" stroke-width="5" class="shock"/>')
P.append('<circle r="70" fill="none" stroke="#ff3b3b" stroke-width="12" stroke-opacity=".35" class="shock"/>')
P.append('</g>')

# ---- the station: a smooth gunmetal sphere split by glowing seams ----
SX, SY, SR = 255, 235, 92
tx, ty = MX + 40, MY - 40          # where the beam lands
d = math.hypot(tx - SX, ty - SY); ux, uy = (tx - SX) / d, (ty - SY) / d
ex, ey = SR * ux, SR * uy           # emitter on the surface, facing the moon
S = ['<g transform="translate(%d,%d)">' % (SX, SY),
     '<circle r="150" fill="url(#coreG)" class="charge" opacity=".7"/>',
     '<circle r="%d" fill="url(#sphG)"/>' % SR,
     '<circle r="%d" fill="url(#rimG)"/>' % (SR + 6)]
seams = ['M-70,-58 C-40,-30 -36,6 -60,38 C-48,60 -30,70 -12,88',
         'M22,-90 C10,-60 18,-30 46,-12 C66,0 78,24 84,40',
         'M-88,10 C-50,18 -10,10 22,30 C40,44 44,70 34,86']
S.append('<g class="charge">' + ''.join('<path d="%s" stroke="#ff3b2a" stroke-width="2.6" fill="none" stroke-linecap="round"/>' % p for p in seams) + '</g>')
S.append('<g opacity=".55">' + ''.join('<path d="%s" stroke="#ffd0a0" stroke-width=".9" fill="none" stroke-linecap="round"/>' % p for p in seams) + '</g>')
S.append('<circle cx="%.1f" cy="%.1f" r="26" fill="url(#coreG)" class="charge"/>' % (ex, ey))
S.append('<circle cx="%.1f" cy="%.1f" r="7" fill="#fff0e0" class="charge"/>' % (ex, ey))
for k, (lx, ly) in enumerate(((-30, -70), (60, -50), (-75, 20), (40, 60))):
    S.append('<circle cx="%d" cy="%d" r="1.8" fill="#ff6a5a" class="blink" style="animation-delay:-%.1fs"/>' % (lx, ly, k * 1.1))
S.append('</g>')
bx, by = SX + ex, SY + ey
S.append('<g class="beam"><line x1="%.1f" y1="%.1f" x2="%d" y2="%d" stroke="#ff2d3d" stroke-width="26" stroke-opacity=".22" stroke-linecap="round"/>'
         '<line x1="%.1f" y1="%.1f" x2="%d" y2="%d" stroke="#ff4a3a" stroke-width="8" stroke-linecap="round"/>'
         '<line x1="%.1f" y1="%.1f" x2="%d" y2="%d" stroke="#fff0e0" stroke-width="2.6" stroke-linecap="round"/></g>' % ((bx, by, tx, ty) * 3))
for x in frag(''.join(P) + ''.join(S)):
    left.append(x)




FKN = [k.split('{')[0][11:] for k in FK]
style.text += '\n' + '\n'.join(FK) + '\n' + ''.join('.%s{animation-name:%s}' % (n, n) for n in FKN) + '\n'
def wrap_shake(g, delay=0):
    w = ET.Element(NS + 'g', {'class': 'shake'})
    if delay: w.set('style', 'animation-delay:%.2fs' % delay)
    for k in list(g): g.remove(k); w.append(k)
    g.append(w)
for g in list(root.iter(NS + 'g')):
    c = (g.get('class') or '').split()
    if 'lordPos' in c: wrap_shake(g, -0.25)
    elif 'capmove' in c: wrap_shake(g)
st = style.text
def weave(name, x0, y0, x1, y1, end, amp):
    pts = []
    for i in range(7):
        f = i / 6; y = y0 + (y1 - y0) * f + (amp * math.sin(f * math.pi * 2.3) if 0 < i < 6 else 0)
        pts.append('%.1f%%{transform:translate(%dpx,%dpx)}' % (end * f, x0 + (x1 - x0) * f, y))
    return '@keyframes %s{%s100%%{transform:translate(%dpx,%dpx)}}' % (name, ''.join(pts), x1, y1)
import re
st = re.sub(r'@keyframes sqA\{[^}]*\}[^}]*\}[^}]*\}\}', weave('sqA', -320, 270, 1920, 505, 40, 55), st)
st = re.sub(r'@keyframes sqD\{[^}]*\}[^}]*\}[^}]*\}\}', weave('sqD', -320, 120, 1920, 230, 36, -45), st)
st = re.sub(r'@keyframes sqB\{[^}]*\}[^}]*\}[^}]*\}\}', weave('sqB', 1920, 640, -320, 520, 40, 40), st)
import re as _re
def _remap(m):
    t = float(m.group(1)) * 30 / 100
    n = t * 46.2 / 16.2 if t <= 16.2 else t + 30
    return ('%.2f' % (n / 60 * 100)).rstrip('0').rstrip('.') + '%'
def _fix(m):
    return _re.sub(r'([0-9.]+)%', _remap, m.group(0))
st = _re.sub(r'@keyframes (?:charge|beam|mcrack|moonA|blast|shock|ash|flash|shake|fr\d+)\{.*?\}\}', _fix, st)
style.text = st

out = ET.tostring(root, encoding='unicode').replace(' />', '/>')
open(out_path, 'w', encoding='utf-8').write(head + out + tail)
print('chars', len(out))
