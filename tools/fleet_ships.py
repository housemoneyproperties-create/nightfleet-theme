# Rebuilds Night Fleet's ships with original designs: a planet-killer station,
# a lance-hulled flagship, talon interceptors and twin-boom rebel fighters.
import sys, math, random
import xml.etree.ElementTree as ET
SVGNS = 'http://www.w3.org/2000/svg'; NS = '{%s}' % SVGNS
ET.register_namespace('', SVGNS)
random.seed(42)

src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
head, svg, tail = s[:s.index('`') + 1], s[s.index('`') + 1:s.rindex('`')], s[s.rindex('`'):]
root = ET.fromstring(svg)
parent = {c: p for p in root.iter() for c in p}


def frag(xml):
    return list(ET.fromstring('<g xmlns="%s">%s</g>' % (SVGNS, xml)))


# ---- 0. stars parked off-canvas (the drift layers no longer scroll) ----
for e in list(root.iter(NS + 'circle')):
    if e.get('cx') and float(e.get('cx')) > 1620:
        parent[e].remove(e)

# ---- 1. new gradients and animation rules ----
defs = root.find(NS + 'defs')
for x in frag(
    '<radialGradient id="coreG"><stop offset="0" stop-color="#fff3e6"/><stop offset=".25" stop-color="#ff6a3a"/>'
    '<stop offset=".6" stop-color="#d0182a" stop-opacity=".55"/><stop offset="1" stop-color="#6a0610" stop-opacity="0"/></radialGradient>'
    '<linearGradient id="lanceG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f49"/><stop offset=".45" stop-color="#1a1d24"/><stop offset="1" stop-color="#07080b"/></linearGradient>'
    '<linearGradient id="rebG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9c1c7"/><stop offset="1" stop-color="#6c767e"/></linearGradient>'):
    defs.append(x)
style = root.find(NS + 'style')
assert '@media (max-aspect-ratio:3/4)' in style.text
style.text = style.text.replace('@media (max-aspect-ratio:3/4)',
    '.charge{animation:charge 14s ease-in infinite}\n'
    '@keyframes charge{0%{opacity:.3}80%{opacity:.75}88%{opacity:1}92%{opacity:.25}100%{opacity:.3}}\n'
    '.beam{animation:beam 14s linear infinite;opacity:0}\n'
    '@keyframes beam{0%,87%{opacity:0}88.5%{opacity:1}92%{opacity:.9}94%,100%{opacity:0}}\n'
    '.impact{animation:impact 14s ease-out infinite;opacity:0;transform-box:fill-box;transform-origin:center}\n'
    '@keyframes impact{0%,88%{opacity:0;transform:scale(.3)}90%{opacity:1;transform:scale(1)}96%{opacity:0;transform:scale(1.8)}100%{opacity:0}}\n'
    '@media (max-aspect-ratio:3/4)', 1)

# ---- 2. planet-killer station (replaces the small ring station) ----
left = [e for e in root.iter(NS + 'g') if e.get('class') == 'leftFill'][0]
for g in list(left):
    if g.get('transform') == 'translate(205,185)':
        left.remove(g)
sx, sy = 255, 235
dash = '150 30 90 46 160 38 120 57'
parts = ['<g transform="translate(%d,%d)">' % (sx, sy),
         '<circle r="150" fill="url(#coreG)" class="charge"/>',
         '<circle r="104" fill="#0a0b0f"/>',
         '<circle r="104" fill="none" stroke="#1f2229" stroke-width="20" stroke-dasharray="%s"/>' % dash,
         '<circle r="104" fill="none" stroke="#3a3f48" stroke-width="2" stroke-dasharray="%s"/>' % dash,
         '<circle r="82" fill="none" stroke="#14161b" stroke-width="7" stroke-dasharray="60 18 110 26 70 30 130 71" transform="rotate(40)"/>',
         '<circle r="104" fill="none" stroke="#ff2d3d" stroke-width="1.3" stroke-opacity=".55" stroke-dasharray="6 40 3 70 6 55" transform="rotate(12)"/>']
for i, a in enumerate(range(0, 360, 45)):
    L = 34 + (i % 3) * 14
    r0 = 110
    a1, a2, am = math.radians(a - 5), math.radians(a + 5), math.radians(a)
    p = [(r0 * math.cos(a1), r0 * math.sin(a1)), ((r0 + L) * math.cos(am), (r0 + L) * math.sin(am)), (r0 * math.cos(a2), r0 * math.sin(a2))]
    parts.append('<polygon points="%s" fill="#181b21" stroke="#2c3038" stroke-width="1"/>' % ' '.join('%.1f,%.1f' % q for q in p))
    if i % 2 == 0:
        parts.append('<circle cx="%.1f" cy="%.1f" r="2.4" fill="#ff5a4a" class="blink" style="animation-delay:-%.1fs"/>' % (p[1][0], p[1][1], i * .7))
parts += ['<circle r="40" fill="#1a0507"/>',
          '<circle r="34" fill="url(#coreG)" class="charge"/>',
          '<circle r="12" fill="#fff0e0" class="charge" opacity=".9"/>']
for _ in range(9):  # chunks drifting from the breaks
    a = random.uniform(0, 2 * math.pi); r = random.uniform(125, 170); k = random.uniform(3, 8)
    cx, cy = r * math.cos(a), r * math.sin(a)
    parts.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#16181d"/>' % (cx - k, cy, cx, cy - k * .7, cx + k, cy + k * .2, cx - k * .2, cy + k * .8))
parts.append('</g>')
mx, my = 160, 700  # the beam lands on the moon
parts.append('<g class="beam"><line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ff2d3d" stroke-width="22" stroke-opacity=".25" stroke-linecap="round"/>'
             '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ff4a3a" stroke-width="7" stroke-linecap="round"/>'
             '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#fff0e0" stroke-width="2.2" stroke-linecap="round"/></g>' % ((sx, sy, mx, my) * 3))
parts.append('<g transform="translate(%d,%d)"><g class="impact"><circle r="60" fill="url(#boomG)"/><circle r="34" fill="none" stroke="#ffb36b" stroke-width="2"/></g></g>' % (mx, my))
for x in frag(''.join(parts)):
    left.append(x)

# ---- 3. the flagship: a long lance hull with stacked command towers ----
cap = [e for e in root.iter(NS + 'g') if e.get('class') == 'capmove'][0]
hull = [c for c in cap if c.get('transform') is None][0]
keep = [c for c in hull if c.tag == NS + 'g' and 'rotate(150)' in (c.get('transform') or '')]
for c in list(hull):
    hull.remove(c)
F = ['<ellipse cx="800" cy="0" rx="150" ry="34" fill="url(#plume)" class="cengs"/>',
     '<polygon points="0,0 140,-12 400,-27 620,-35 760,-38 780,-32 780,32 760,38 620,30 400,20 140,8" fill="url(#lanceG)"/>',
     '<polygon points="0,0 140,-12 400,-27 620,-35 760,-38 760,-33 620,-30 400,-22 140,-8 8,-1" fill="#4a505b"/>',
     '<polygon points="8,1 140,8 400,20 620,30 760,38 780,32 780,6 400,5 140,3" fill="#06070a" opacity=".85"/>',
     '<line x1="150" y1="0" x2="770" y2="0" stroke="#ff2d3d" stroke-width="1.1" stroke-opacity=".5"/>']
for pts in ('330,-25 362,-42 480,-42 492,-31', '440,-32 466,-55 590,-55 606,-35', '552,-36 574,-66 700,-66 718,-37'):
    F.append('<polygon points="%s" fill="#1b1f26" stroke="#30353e" stroke-width="1"/>' % pts)
F.append('<line x1="362" y1="-42" x2="480" y2="-42" stroke="#4a505b" stroke-width="1.4"/><line x1="466" y1="-55" x2="590" y2="-55" stroke="#4a505b" stroke-width="1.4"/><line x1="574" y1="-66" x2="700" y2="-66" stroke="#4a505b" stroke-width="1.4"/>')
F.append('<polygon points="618,-66 630,-128 656,-128 668,-66" fill="#20242c"/><polygon points="600,-142 686,-142 680,-126 606,-126" fill="#2b3039"/>'
         '<rect x="608" y="-137" width="70" height="2.6" fill="#ff3b3b"/><line x1="643" y1="-142" x2="643" y2="-176" stroke="#2b3039" stroke-width="2"/><circle cx="643" cy="-178" r="2.6" fill="#ff2d3d" class="blink"/>')
F.append('<polygon points="520,-55 530,-92 550,-92 558,-55" fill="#1d2128"/><polygon points="508,-102 572,-102 566,-90 514,-90" fill="#272c34"/>'
         '<rect x="516" y="-98" width="48" height="2.2" fill="#ff3b3b" opacity=".85"/><line x1="540" y1="-102" x2="540" y2="-122" stroke="#272c34" stroke-width="1.6"/><circle cx="540" cy="-124" r="2" fill="#ff2d3d" class="blink" style="animation-delay:-1.3s"/>')
for x in range(170, 330, 26):
    yt = -12 - (x - 140) * 15 / 260
    F.append('<rect x="%d" y="%.1f" width="11" height="4" fill="#2a2e37"/><line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#3a3f48" stroke-width="1.4"/>' % (x, yt - 4, x + 2, yt - 3, x - 9, yt - 6))
F.append('<polygon points="250,18 296,58 580,58 626,30" fill="#0a0c10"/><polygon points="250,18 296,58 300,58 256,18" fill="#2c313b"/>'
         '<rect x="320" y="50" width="220" height="3" fill="#ff2d3d" opacity=".55"/>')
for y, x1, x2, dsh, op in ((-14, 160, 600, '2.4 6 2.4 11 2.4 4', .8), (-4, 120, 740, '2.4 9 2.4 5 2.4 15', .7), (8, 180, 700, '2.4 7 2.4 13', .6), (18, 300, 720, '2.4 5 2.4 9 2.4 18', .55)):
    F.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ffcfb0" stroke-width="1.3" stroke-dasharray="%s" opacity="%s"/>' % (x1, y, x2, y, dsh, op))
for x, y in ((236, -4), (412, 8), (588, -14), (655, 18), (702, -4)):
    F.append('<rect x="%d" y="%.1f" width="2.4" height="1.3" fill="#ff3b3b" class="blink" style="animation-delay:-%.1fs"/>' % (x, y - 0.6, (x % 9) * .9))
F.append('<g class="cengs"><circle cx="786" cy="-24" r="17" fill="url(#engR)"/><circle cx="786" cy="-6" r="22" fill="url(#engR)"/><circle cx="786" cy="14" r="22" fill="url(#engR)"/><circle cx="786" cy="30" r="14" fill="url(#engR)"/></g>')
for x in frag(''.join(F)):
    hull.append(x)
for c in keep:  # the flagship's guns keep firing over the new hull
    hull.append(c)

# ---- 4. fighters ----
TALON = ('<polygon points="26,0 6,-5 -14,-4 -19,0 -14,4 6,5" fill="#15171c" stroke="#3a3f49" stroke-width=".8"/>'
         '<path d="M-4,-4 C0,-20 14,-30 34,-33 C18,-24 10,-15 8,-5 Z" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8"/>'
         '<path d="M-4,4 C0,20 14,30 34,33 C18,24 10,15 8,5 Z" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8"/>'
         '<path d="M30,-32 L36,-34 L32,-29 Z M30,32 L36,34 L32,29 Z" fill="#d0283a"/>'
         '<ellipse cx="10" cy="0" rx="6" ry="2.6" fill="#d42a3a" opacity=".85"/>'
         '<circle class="eng" cx="-20" cy="0" r="7" fill="url(#engR)"/>')
REBEL = ('<rect x="-26" y="-18" width="22" height="6" rx="3" fill="url(#rebG)"/><rect x="-26" y="12" width="22" height="6" rx="3" fill="url(#rebG)"/>'
         '<polygon points="4,-3 -6,-13 -14,-13 -8,-3" fill="#8a949b"/><polygon points="4,3 -6,13 -14,13 -8,3" fill="#8a949b"/>'
         '<polygon points="36,0 12,-4 -16,-4.5 -20,0 -16,4.5 12,4" fill="url(#rebG)"/>'
         '<line x1="-10" y1="0" x2="20" y2="0" stroke="#e0782a" stroke-width="1.6"/>'
         '<ellipse cx="14" cy="-1" rx="5" ry="2" fill="#0d2230"/>'
         '<circle class="eng" cx="-27" cy="-15" r="5" fill="url(#engB)"/><circle class="eng" cx="-27" cy="15" r="5" fill="url(#engB)"/>')
swapped = {'R': 0, 'B': 0}
for g in list(root.iter(NS + 'g')):
    kids = list(g)
    trail = [k for k in kids if k.tag == NS + 'rect' and k.get('fill') in ('url(#trailR)', 'url(#trailB)')]
    if not trail:
        continue
    side = 'R' if trail[0].get('fill') == 'url(#trailR)' else 'B'
    for k in kids:
        if k is not trail[0]:
            g.remove(k)
    for x in frag(TALON if side == 'R' else REBEL):
        g.append(x)
    swapped[side] += 1

# ---- 5. more crossfire and explosions ----
X = []
for x, y, rot, col, d in ((520, 470, -6, '#ff3b3b', .3), (700, 520, 174, '#5cc8ff', .9), (380, 610, -10, '#ff3b3b', .6),
                          (900, 430, 186, '#5cc8ff', 1.1), (640, 700, -4, '#ff3b3b', 0.0), (1000, 620, 178, '#5cc8ff', .5)):
    X.append('<g transform="translate(%d,%d) rotate(%d)"><g class="bolt" style="animation-delay:-%.1fs"><line x1="0" y1="0" x2="34" y2="0" stroke="%s" stroke-width="2.6" stroke-linecap="round"/></g></g>' % (x, y, rot, d, col))
for x, y, sc, d in ((560, 540, 1.0, 3.1), (840, 480, .8, 6.4), (430, 420, .9, 8.8)):
    X.append('<g transform="translate(%d,%d) scale(%s)"><g class="boom" style="animation-delay:-%.1fs"><circle r="16" fill="url(#boomG)"/><circle r="10" fill="none" stroke="#ff9a6b" stroke-width="1.4"/></g></g>' % (x, y, sc, d))
lord = [e for e in root if e.get('class') == 'lordPos'][0]
idx = list(root).index(lord)
for i, x in enumerate(frag(''.join(X))):
    root.insert(idx + i, x)

out = ET.tostring(root, encoding='unicode').replace(' />', '/>')
open(out_path, 'w', encoding='utf-8').write(head + out + tail)
print('fighters swapped', swapped, 'chars', len(out))
