#!/usr/bin/env python3
"""Generate the Night Fleet scene (v2): a dark, red space-opera battle.

A hooded dark warlord with a red energy blade stands on a deck, silhouetted
against a dying red world, while a black capital ship drifts overhead and
fighter squadrons trade red laser fire. All original art: no franchise ships,
characters or logos.

Usage: gen_fleet.py <out_dir> [scene.ts path]
"""
import random
import sys

random.seed(11)
W, H = 1600, 1000


def f(x):
    return f"{x:.1f}".rstrip('0').rstrip('.')


# ---------- stars, each layer tiled twice so it scrolls forever ----------
def star_layer(n, rmin, rmax, omin, omax, twinkle=False):
    stars = []
    for _ in range(n):
        x, y = random.uniform(0, W), random.uniform(0, H * 0.92)
        stars.append((x, y, random.uniform(rmin, rmax), random.uniform(omin, omax),
                      random.choice(['#ffffff', '#ffffff', '#ffe0dc', '#ffd0c8'])))
    out = []
    for dx in (0, W):
        for i, (x, y, r, o, tint) in enumerate(stars):
            extra = ''
            if twinkle and i % 3 == 0:
                extra = f' class="tw" style="animation-delay:-{f(random.uniform(0, 6))}s"'
            out.append(f'<circle cx="{f(x + dx)}" cy="{f(y)}" r="{f(r)}" fill="{tint}" opacity="{f(o)}"{extra}/>')
    return ''.join(out)


far = star_layer(140, 0.5, 0.9, 0.3, 0.65)
mid = star_layer(55, 0.9, 1.4, 0.5, 0.85, twinkle=True)
near = star_layer(14, 1.5, 2.0, 0.75, 1.0, twinkle=True)

# ---------- fleet fighter: black hull, red trim, nose toward +x ----------
FIGHTER = (
    '<g>'
    '<polygon points="5,-4 -12,-29 -23,-29 -11,-4" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8"/>'
    '<polygon points="5,4 -12,29 -23,29 -11,4" fill="url(#hullG)" stroke="#3a3f49" stroke-width=".8"/>'
    '<line x1="-12" y1="-27" x2="-22" y2="-27" stroke="#ff2d3d" stroke-width="2.2"/>'
    '<line x1="-12" y1="27" x2="-22" y2="27" stroke="#ff2d3d" stroke-width="2.2"/>'
    '<polygon points="34,0 15,-6.5 -16,-5.5 -22,0 -16,5.5 15,6.5" fill="#1d2028" stroke="#4b515d" stroke-width=".8"/>'
    '<ellipse cx="12" cy="0" rx="7" ry="3" fill="#ff2d3d" opacity=".85"/>'
    '<ellipse cx="13" cy="-.6" rx="3" ry="1" fill="#ffd6d6" opacity=".8"/>'
    '<circle class="eng" cx="-24" cy="0" r="7" fill="url(#engR)"/>'
    '</g>'
)


def bolts(delay, color='#ff2d3d'):
    """Twin wing cannons: two streaks fly ahead of the nose and fade."""
    one = (f'<line x1="22" y1="{{y}}" x2="56" y2="{{y}}" stroke="{color}" stroke-width="6" stroke-opacity=".28" stroke-linecap="round"/>'
           f'<line x1="22" y1="{{y}}" x2="56" y2="{{y}}" stroke="#ffe8e8" stroke-width="1.8" stroke-linecap="round"/>')
    return f'<g class="bolt" style="animation-delay:{delay}s">{one.format(y=-10)}{one.format(y=10)}</g>'


# ---------- the opposing interceptor: pale hull, cyan engine ----------
INTERCEPTOR = (
    '<g>'
    '<polygon points="30,0 6,-5 -18,-14 -22,-14 -14,-4 -20,0 -14,4 -22,14 -18,14 6,5" fill="#a9a395" stroke="#d8d2c4" stroke-width=".8"/>'
    '<polygon points="-4,-5 -16,-22 -20,-22 -12,-5" fill="#7f7a70"/>'
    '<polygon points="-4,5 -16,22 -20,22 -12,5" fill="#7f7a70"/>'
    '<ellipse cx="10" cy="0" rx="5" ry="2.2" fill="#0d2230" stroke="#7fd6ff" stroke-width=".6"/>'
    '<circle class="eng" cx="-22" cy="0" r="5.5" fill="url(#engB)"/>'
    '</g>'
)


# ---------- the black capital ship, nose toward -x, about 680 long ----------
def capital(with_guns=True):
    lights = []
    for y, x0, x1 in [(-13, 160, 610), (-3, 110, 640), (7, 130, 630), (17, 180, 600)]:
        x = x0
        while x < x1:
            if random.random() < 0.5:
                red = random.random() < 0.18
                cls = f' class="blink" style="animation-delay:-{f(random.uniform(0, 9))}s"' if random.random() < 0.12 else ''
                lights.append(f'<rect x="{f(x)}" y="{y}" width="2.4" height="1.3" fill="{"#ff3b3b" if red else "#ffcfb0"}" opacity=".8"{cls}/>')
            x += random.uniform(5, 11)
    guns = ''
    if with_guns:
        shots = []
        for i, (gx, d) in enumerate([(260, 0), (380, -1.3), (500, -2.4), (330, -3.1)]):
            shots.append(
                f'<g transform="translate({gx},34) rotate(152)"><g class="tbolt" style="animation-delay:{d}s">'
                '<line x1="0" y1="0" x2="46" y2="0" stroke="#ff2233" stroke-width="7" stroke-opacity=".3" stroke-linecap="round"/>'
                '<line x1="0" y1="0" x2="46" y2="0" stroke="#ffe0e0" stroke-width="2.2" stroke-linecap="round"/>'
                '</g></g>')
        guns = ''.join(shots)
    return (
        '<g>'
        + guns +
        '<polygon points="0,0 130,-19 430,-32 570,-37 680,-33 680,33 570,37 430,32 130,19" fill="url(#capG)" stroke="#2c313b" stroke-width="1"/>'
        '<polygon points="0,0 130,-19 430,-32 430,-26 130,-14" fill="#3a404b"/>'
        '<polygon points="150,-11 440,-32 440,-13 150,-3" fill="#161920"/>'
        '<polygon points="450,-36 530,-62 625,-64 642,-36" fill="#1b1f27" stroke="#2c313b" stroke-width="1"/>'
        '<polygon points="555,-64 562,-100 618,-100 624,-64" fill="#20242c" stroke="#353a45" stroke-width="1"/>'
        '<rect x="566" y="-90" width="48" height="3" fill="#ff3b3b" opacity=".85"/>'
        '<line x1="580" y1="-100" x2="576" y2="-138" stroke="#3d434e" stroke-width="2"/>'
        '<line x1="602" y1="-100" x2="610" y2="-126" stroke="#3d434e" stroke-width="2"/>'
        '<circle cx="576" cy="-139" r="2.6" fill="#ff2d3d" class="blink"/>'
        '<polygon points="190,19 570,37 570,56 240,31" fill="#0b0d11"/>'
        '<line x1="130" y1="0" x2="680" y2="0" stroke="#ff2d3d" stroke-width="1" stroke-opacity=".55"/>'
        '<line x1="310" y1="-26" x2="310" y2="26" stroke="#0e1015" stroke-width="2"/>'
        '<line x1="480" y1="-34" x2="480" y2="34" stroke="#0e1015" stroke-width="2"/>'
        + ''.join(lights) +
        '<g class="cengs">'
        '<circle cx="686" cy="-18" r="18" fill="url(#engR)"/>'
        '<circle cx="686" cy="0" r="22" fill="url(#engR)"/>'
        '<circle cx="686" cy="18" r="18" fill="url(#engR)"/>'
        '</g>'
        '</g>'
    )


CAP = capital()
CAP_FAR = capital(with_guns=False)


def flash(x, y, delay, size=1.0):
    return (f'<g transform="translate({x},{y}) scale({size})"><g class="boom" style="animation-delay:{delay}s">'
            '<circle r="15" fill="url(#boomG)"/><circle r="9" fill="none" stroke="#ff9a6b" stroke-width="1.4"/>'
            '</g></g>')


def jump(x, y, delay):
    lines = ''.join(
        f'<line x1="0" y1="{dy}" x2="{-ln}" y2="{dy}" stroke="#ffe6e6" stroke-width="1.4" stroke-opacity="{o}" stroke-linecap="round"/>'
        for dy, ln, o in [(-6, 240, .9), (-2, 330, 1), (2, 280, .9), (6, 200, .7), (-10, 150, .5), (10, 170, .5)])
    return (f'<g transform="translate({x},{y}) rotate(-8)"><g class="jump" style="animation-delay:{delay}s">'
            f'{lines}<circle r="5" fill="#ffffff"/></g></g>')


# ---------- the dying red world ----------
def planet():
    bands = ''.join(
        f'<rect x="-300" y="{y}" width="600" height="{h}" fill="{c}" opacity="{o}"/>'
        for y, h, c, o in [(-190, 30, '#ff5a3a', .12), (-120, 22, '#000000', .35), (-60, 40, '#ff4a2a', .1),
                           (10, 26, '#000000', .4), (70, 34, '#ff3a2a', .1), (140, 24, '#000000', .4)])
    cracks = ('<path d="M-150,-40 L-90,-10 L-60,-35 L10,5 L60,-15 M-40,60 L20,40 L70,70 L130,45" '
              'fill="none" stroke="#ff4a2a" stroke-width="2" stroke-opacity=".55" class="lava"/>')
    ring = ('<ellipse rx="430" ry="70" fill="none" stroke="url(#ringG)" stroke-width="20"/>'
            '<ellipse rx="392" ry="62" fill="none" stroke="#ff6a4a" stroke-opacity=".14" stroke-width="5"/>')
    return (
        '<g class="planetPos"><g transform="translate(1250,930) rotate(-14)">'
        '<circle r="330" fill="url(#atmoGlow)" class="glowpulse"/>'
        + ring +
        '<circle r="280" fill="url(#planetG)"/>'
        f'<g clip-path="url(#planetClip)">{bands}{cracks}</g>'
        '<circle r="280" fill="url(#shadeG)"/>'
        f'<g clip-path="url(#ringFront)">{ring}</g>'
        '</g></g>'
    )


# ---------- the dark warlord: hooded, cloaked, red blade lowered ----------
# Local frame: feet at (0,0), head near y=-470, facing left toward the battle.
WARLORD = (
    '<g class="lordPos"><g transform="translate(1180,1000) scale(.9)">'
    # red aura behind him so the silhouette reads against the planet
    '<ellipse cx="0" cy="-250" rx="220" ry="300" fill="url(#auraG)" class="glowpulse"/>'
    # cape, swaying a little from the shoulders
    '<g class="cape">'
    '<path d="M-62,-372 C-96,-290 -128,-150 -168,0 L160,0 C134,-150 104,-292 72,-372 Z" fill="#040406"/>'
    '<path d="M72,-372 C104,-292 134,-150 160,0" fill="none" stroke="#ff3a2a" stroke-width="2.5" stroke-opacity=".55"/>'
    '<path d="M10,-330 C2,-220 -6,-110 -18,0 M44,-340 C58,-230 70,-110 84,0" fill="none" stroke="#14151a" stroke-width="3"/>'
    '</g>'
    # body and shoulders
    '<path d="M-74,-372 C-58,-398 62,-400 84,-372 L70,-250 L48,-60 L-42,-60 L-64,-250 Z" fill="#07070a"/>'
    # hood
    '<path d="M-46,-392 C-60,-452 -22,-492 8,-494 C44,-494 70,-454 60,-392 C40,-404 -26,-404 -46,-392 Z" fill="#050507"/>'
    '<path d="M60,-392 C70,-454 44,-494 8,-494" fill="none" stroke="#ff3a2a" stroke-width="2" stroke-opacity=".6"/>'
    # the void under the hood, with two faint ember eyes
    '<path d="M-28,-404 C-30,-440 -8,-462 6,-462 C26,-462 40,-440 34,-404 Z" fill="#000000"/>'
    '<g class="eyes"><ellipse cx="-6" cy="-430" rx="4" ry="1.6" fill="#ff2d2d"/><ellipse cx="14" cy="-430" rx="4" ry="1.6" fill="#ff2d2d"/></g>'
    # arm reaching forward to the hilt
    '<path d="M-60,-360 C-92,-320 -118,-280 -132,-246 L-116,-236 C-98,-268 -74,-304 -46,-336 Z" fill="#08080b"/>'
    # the blade, lowered toward the battle, humming
    '<g transform="translate(-126,-240) rotate(-152)">'
    '<g class="blade">'
    '<line x1="12" y1="0" x2="300" y2="0" stroke="#ff1a2a" stroke-width="30" stroke-opacity=".12" stroke-linecap="round"/>'
    '<line x1="12" y1="0" x2="300" y2="0" stroke="#ff1a2a" stroke-width="14" stroke-opacity=".35" stroke-linecap="round"/>'
    '<line x1="12" y1="0" x2="300" y2="0" stroke="#ff3a44" stroke-width="6" stroke-linecap="round"/>'
    '<line x1="12" y1="0" x2="300" y2="0" stroke="#fff0f0" stroke-width="2.4" stroke-linecap="round"/>'
    '</g>'
    '<rect x="-24" y="-4.5" width="38" height="9" rx="2" fill="#2a2d33" stroke="#6a707a" stroke-width="1"/>'
    '<rect x="-6" y="-4.5" width="4" height="9" fill="#0b0c0f"/>'
    '</g>'
    '</g></g>'
)

# a dark observation deck he stands on, lit red along its edge
DECK = (
    '<g class="lordPos">'
    '<polygon points="860,1000 940,968 1600,968 1600,1000" fill="#050507"/>'
    '<line x1="940" y1="968" x2="1600" y2="968" stroke="#ff2d3d" stroke-width="2" stroke-opacity=".7"/>'
    '<g fill="#ff2d3d">' + ''.join(f'<rect x="{x}" y="978" width="14" height="3" opacity=".55" class="blink" style="animation-delay:-{f(i*0.4)}s"/>' for i, x in enumerate(range(980, 1600, 70))) + '</g>'
    '</g>'
)

STYLE = """
.drift-far{animation:scroll 260s linear infinite}
.drift-mid{animation:scroll 150s linear infinite}
.drift-near{animation:scroll 90s linear infinite}
@keyframes scroll{to{transform:translateX(-1600px)}}
.tw{animation:tw 4.5s ease-in-out infinite}
@keyframes tw{50%{opacity:.25}}
.neb{animation:breathe 22s ease-in-out infinite}
.neb2{animation:breathe 30s ease-in-out infinite reverse}
@keyframes breathe{50%{opacity:.6}}
.glowpulse{animation:glow 5s ease-in-out infinite}
@keyframes glow{50%{opacity:.7}}
.eng{animation:flick .18s steps(2) infinite}
@keyframes flick{50%{opacity:.7}}
.cengs{animation:pulse 3.2s ease-in-out infinite}
@keyframes pulse{50%{opacity:.7}}
.blink{animation:blink 2.6s steps(1) infinite}
@keyframes blink{50%{opacity:.15}}
.lava{animation:glow 3.4s ease-in-out infinite}
.capmove{animation:capmove 170s linear infinite;animation-delay:-62s}
@keyframes capmove{from{transform:translateX(1750px)}to{transform:translateX(-860px)}}
.capfar{animation:capmove 300s linear infinite;animation-delay:-130s}
.sqA{animation:sqA 22s linear infinite;animation-delay:-5.5s}
@keyframes sqA{0%{transform:translate(-320px,260px)}40%{transform:translate(1920px,500px)}100%{transform:translate(1920px,500px)}}
.sqD{animation:sqD 27s linear infinite;animation-delay:-19s}
@keyframes sqD{0%{transform:translate(-320px,120px)}36%{transform:translate(1920px,230px)}100%{transform:translate(1920px,230px)}}
.sqB{animation:sqB 29s linear infinite;animation-delay:-6.5s}
.sqC{animation:sqB 29s linear infinite;animation-delay:-5.3s}
@keyframes sqB{0%{transform:translate(1920px,640px)}40%{transform:translate(-320px,520px)}100%{transform:translate(-320px,520px)}}
.bolt{animation:bolt 1.4s linear infinite;opacity:0}
@keyframes bolt{0%{transform:translateX(0);opacity:1}40%{transform:translateX(430px);opacity:0}100%{transform:translateX(430px);opacity:0}}
.tbolt{animation:tbolt 4.2s linear infinite;opacity:0}
@keyframes tbolt{0%{transform:translateX(0);opacity:1}30%{transform:translateX(620px);opacity:0}100%{transform:translateX(620px);opacity:0}}
.boom{animation:boom 11s ease-out infinite;opacity:0;transform-box:fill-box;transform-origin:center}
@keyframes boom{0%{opacity:0;transform:scale(.2)}2%{opacity:1;transform:scale(.6)}9%{opacity:0;transform:scale(1.7)}100%{opacity:0;transform:scale(1.7)}}
.jump{animation:jump 17s ease-in infinite;opacity:0;transform-box:fill-box;transform-origin:right center}
@keyframes jump{0%{opacity:0;transform:scaleX(.02)}1%{opacity:1;transform:scaleX(.02)}4%{opacity:1;transform:scaleX(1)}7%{opacity:0;transform:scaleX(1.4) translateX(-120px)}100%{opacity:0}}
.blade{animation:hum .11s steps(2) infinite}
@keyframes hum{50%{opacity:.86}}
.cape{animation:cape 7s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 0}
@keyframes cape{50%{transform:skewX(-2.2deg)}}
.eyes{animation:eyes 9s ease-in-out infinite}
@keyframes eyes{0%,100%{opacity:.25}45%,55%{opacity:.9}}
@media (max-aspect-ratio:3/4){
  .planetPos{transform:translate(-420px,0)}
  .lordPos{transform:translate(0px,250px) scale(.75)}
  .capPos{transform:translate(0,40px) scale(.7)}
}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.bolt,.tbolt,.boom,.jump{opacity:0}}
"""

DEFS = """
<radialGradient id="space" cx="70%" cy="60%" r="90%"><stop offset="0" stop-color="#2a0508"/><stop offset=".45" stop-color="#0c0406"/><stop offset="1" stop-color="#030304"/></radialGradient>
<radialGradient id="nebR"><stop offset="0" stop-color="#b0101e" stop-opacity=".55"/><stop offset=".5" stop-color="#5a0812" stop-opacity=".25"/><stop offset="1" stop-color="#2a0408" stop-opacity="0"/></radialGradient>
<radialGradient id="nebD"><stop offset="0" stop-color="#3a0610" stop-opacity=".6"/><stop offset="1" stop-color="#120206" stop-opacity="0"/></radialGradient>
<linearGradient id="hullG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c3038"/><stop offset="1" stop-color="#0e1014"/></linearGradient>
<linearGradient id="capG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e333c"/><stop offset=".5" stop-color="#16191f"/><stop offset="1" stop-color="#08090c"/></linearGradient>
<radialGradient id="engR"><stop offset="0" stop-color="#fff0ea"/><stop offset=".35" stop-color="#ff4a3a"/><stop offset="1" stop-color="#ff1a2e" stop-opacity="0"/></radialGradient>
<radialGradient id="engB"><stop offset="0" stop-color="#f0fbff"/><stop offset=".35" stop-color="#5cc8ff"/><stop offset="1" stop-color="#1a8cff" stop-opacity="0"/></radialGradient>
<radialGradient id="boomG"><stop offset="0" stop-color="#fff2d8"/><stop offset=".35" stop-color="#ff9a4a"/><stop offset=".7" stop-color="#e2302a" stop-opacity=".6"/><stop offset="1" stop-color="#7a1010" stop-opacity="0"/></radialGradient>
<radialGradient id="planetG" cx="30%" cy="25%" r="80%"><stop offset="0" stop-color="#8a1e1a"/><stop offset=".45" stop-color="#4a0c10"/><stop offset=".8" stop-color="#1c0408"/><stop offset="1" stop-color="#0a0204"/></radialGradient>
<radialGradient id="shadeG" cx="80%" cy="85%" r="85%"><stop offset="0" stop-color="#020203" stop-opacity=".95"/><stop offset=".55" stop-color="#020203" stop-opacity=".55"/><stop offset="1" stop-color="#020203" stop-opacity="0"/></radialGradient>
<radialGradient id="atmoGlow"><stop offset=".78" stop-color="#ff2a1a" stop-opacity="0"/><stop offset=".86" stop-color="#ff2a1a" stop-opacity=".45"/><stop offset="1" stop-color="#ff2a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="auraG"><stop offset="0" stop-color="#ff2030" stop-opacity=".35"/><stop offset=".6" stop-color="#a00a18" stop-opacity=".12"/><stop offset="1" stop-color="#500008" stop-opacity="0"/></radialGradient>
<linearGradient id="ringG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7a2018" stop-opacity=".1"/><stop offset=".5" stop-color="#ff6a4a" stop-opacity=".45"/><stop offset="1" stop-color="#7a2018" stop-opacity=".1"/></linearGradient>
<clipPath id="planetClip"><circle r="280"/></clipPath>
<clipPath id="ringFront"><rect x="-600" y="0" width="1200" height="200"/></clipPath>
"""

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">'
    f'<style>{STYLE}</style><defs>{DEFS}</defs>'
    f'<rect width="{W}" height="{H}" fill="url(#space)"/>'
    '<ellipse class="neb" cx="1150" cy="220" rx="760" ry="340" fill="url(#nebR)"/>'
    '<ellipse class="neb2" cx="380" cy="760" rx="680" ry="320" fill="url(#nebD)"/>'
    '<ellipse class="neb2" cx="700" cy="430" rx="520" ry="150" fill="url(#nebR)" opacity=".4"/>'
    f'<g class="drift-far">{far}</g>'
    f'<g class="drift-mid">{mid}</g>'
    f'<g transform="translate(0,330) scale(.3)" opacity=".5"><g class="capfar">{CAP_FAR}</g></g>'
    + flash(1240, 420, -0.2, 1.2) + flash(420, 250, -4.5) + flash(960, 95, -8.5, .8) + flash(620, 640, -2.5, .9)
    + jump(1320, 330, -0.3) + jump(470, 560, -9.3)
    + planet()
    + f'<g class="capPos"><g transform="translate(0,150)"><g class="capmove">{CAP}</g></g></g>'
    # squadron A: three fleet fighters crossing left to right, firing
    '<g class="sqA"><g transform="rotate(6.1)">'
    f'<g>{FIGHTER}{bolts(0)}</g>'
    f'<g transform="translate(-58,-40)">{FIGHTER}{bolts(-.5)}</g>'
    f'<g transform="translate(-58,40)">{FIGHTER}{bolts(-1)}</g>'
    '</g></g>'
    # squadron D: a pair high up
    '<g class="sqD"><g transform="rotate(2.8) scale(.7)">'
    f'<g>{FIGHTER}{bolts(-.3)}</g><g transform="translate(-54,30)">{FIGHTER}{bolts(-.8)}</g>'
    '</g></g>'
    # squadron B: two interceptors fleeing right to left; C: fleet fighters chasing them
    f'<g class="sqB"><g transform="rotate(183.1)"><g>{INTERCEPTOR}</g><g transform="translate(-46,34)">{INTERCEPTOR}</g></g></g>'
    f'<g class="sqC"><g transform="rotate(183.1)"><g>{FIGHTER}{bolts(-.2)}</g><g transform="translate(-50,-36)">{FIGHTER}{bolts(-.9)}</g></g></g>'
    + DECK + WARLORD +
    f'<g class="drift-near">{near}</g>'
    '</svg>'
)

base = sys.argv[1] if len(sys.argv) > 1 else '.'
open(f'{base}/fleet.svg', 'w').write(svg)
assert '`' not in svg and '${' not in svg
if len(sys.argv) > 2:
    open(sys.argv[2], 'w').write(
        '// Night Fleet: an original dark space-opera battle. Generated by gen_fleet.py.\n'
        f'export const SCENE = `{svg}`\n')
print('chars', len(svg))
