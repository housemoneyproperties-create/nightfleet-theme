"""Night Fleet dark lord, v7: the hooded lord, an original design.

A towering faceless figure in a deep cowl and a massive layered cloak stands on
the deck, three-quarter turned toward the battle. The hood holds a black void
with two faint ember eyes. One dark gauntlet shows where the cloak parts and
holds a red energy blade low, point toward the deck; the blade throws red bounce
light up the cloak folds and into the cowl, and the burning planet limb behind
rims the hood crown and shoulders.

Local frame: feet at (0,0), up is negative y, about 620 tall, x -291..300 (blade tip; its glow spills a little further).
Exports LORD_DEFS (gradients, ids prefixed hood-), LORD_CSS, LORD.
"""

RIM = '#ff4a30'    # back light from the burning limb
HOT = '#ff2632'    # bounce light from the blade


def n(v):
    return f'{v:.1f}'.rstrip('0').rstrip('.')


def p(d, fill, extra=''):
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def cres(x0, y0, cx, cy, x1, y1, dx, dy, fill, op):
    """A tapered highlight: two quadratic arcs between the same end points."""
    return (f'<path d="M{x0},{y0}Q{cx},{cy} {x1},{y1}Q{cx + dx},{cy + dy} {x0},{y0}Z" '
            f'fill="{fill}" opacity="{op}"/>')


def taper(x0, y0, ax, ay, bx, by, x1, y1, w, fill, op):
    """A tapered fold: a cubic and the same cubic pushed sideways by w."""
    return (f'<path d="M{x0},{y0}C{ax},{ay} {bx},{by} {x1},{y1}C{bx + w},{by} {ax + w},{ay} {x0},{y0}Z" '
            f'fill="{fill}" opacity="{op}"/>')


def fold(x0, y0, ax, ay, bx, by, x1, y1, w=30, dark=.5, lit=None, lop=0.0):
    """Soft shadow trough (two nested tapers) with a lit ridge on its blade side."""
    s = (taper(x0, y0, ax, ay, bx, by, x1, y1, w, '#000', dark)
         + taper(x0, y0, ax + w * .3, ay, bx + w * .3, by, x1, y1, w * .4, '#000', dark))
    if lit:
        s += taper(x0, y0, ax, ay, bx, by, x1, y1, -w * .3, lit, lop)
    return s


def line(x0, y0, x1, y1, stroke, w, op=1):
    return (f'<path d="M{n(x0)},{n(y0)}L{n(x1)},{n(y1)}" stroke="{stroke}" stroke-width="{w}" '
            f'stroke-linecap="round" opacity="{op}"/>')


def lg(i, x1, y1, x2, y2, stops, user=False):
    u = ' gradientUnits="userSpaceOnUse"' if user else ''
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else '') + '/>'
                for o, c, a in stops)
    return f'<linearGradient id="hood-{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>{s}</linearGradient>'


def rg(i, stops, attrs=''):
    s = ''.join(f'<stop offset="{o}" stop-color="{c}"' + (f' stop-opacity="{a}"' if a != 1 else '') + '/>'
                for o, c, a in stops)
    return f'<radialGradient id="hood-{i}"{attrs}>{s}</radialGradient>'


USER = ' gradientUnits="userSpaceOnUse"'
LORD_DEFS = ''.join([
    lg('cape', 0, 0, .3, 1, [(0, '#121319', 1), (.4, '#07070a', 1), (.85, '#050405', 1), (1, '#16070a', 1)]),
    lg('body', .7, 0, .3, 1, [(0, '#15161d', 1), (.25, '#0b0b0f', 1), (.7, '#060608', 1), (1, '#0b0406', 1)]),
    lg('mantle', .8, 0, .4, 1, [(0, '#23242e', 1), (.25, '#101116', 1), (1, '#050506', 1)]),
    lg('cowl', .85, .05, .25, .9, [(0, '#30323f', 1), (.3, '#14151b', 1), (.75, '#060608', 1), (1, '#120507', 1)]),
    lg('plate', 0, 0, 1, 0, [(0, '#6a1218', 1), (.3, '#141419', 1), (.6, '#2b2e3a', 1), (1, '#08080b', 1)]),
    rg('bounce', [(0, HOT, .5), (.4, '#c8141e', .22), (1, '#7a0a10', 0)], USER + ' cx="-262" cy="-160" r="340"'),
    rg('under', [(0, HOT, .42), (.5, '#c8141e', .14), (1, '#7a0a10', 0)], USER + ' cx="-150" cy="-410" r="150"'),
    rg('glow', [(0, '#ff3a26', .3), (.5, '#c81a14', .12), (1, '#c81a14', 0)]),
    rg('halo', [(0, '#ff2a36', .5), (.4, '#ff1a2a', .16), (1, '#ff1a2a', 0)]),
    rg('eye', [(0, '#ff5a3a', .9), (.4, '#ff2a1a', .3), (1, '#ff1010', 0)]),
    rg('spill', [(0, '#ff3a30', .6), (.4, '#ff2a2a', .2), (1, '#ff2a2a', 0)]),
])

LORD_CSS = (
    '.hood-cape{animation:hood-cape 11s ease-in-out infinite;transform-box:fill-box;transform-origin:20% 0}'
    '@keyframes hood-cape{50%{transform:skewX(1.5deg) scaleX(1.02)}}'
    '.hood-hem{animation:hood-hem 11s ease-in-out -2s infinite;transform-box:fill-box;transform-origin:50% 0}'
    '@keyframes hood-hem{50%{transform:translateX(4px) scaleX(1.025)}}'
    '.hood-breath{animation:hood-breath 6s ease-in-out infinite}'
    '@keyframes hood-breath{0%,100%{transform:translateY(0)}45%{transform:translateY(-3px)}}'
    '.hood-eye{animation:hood-eye 7s ease-in-out -2.5s infinite}'
    '@keyframes hood-eye{0%,100%{opacity:.3}40%,60%{opacity:1}}'
    '.hood-hum{animation:hood-hum 2.7s ease-in-out infinite}'
    '@keyframes hood-hum{0%,100%{opacity:.8}50%{opacity:1}}'
)

# ------------------------------------------------------------------ back light
GLOW = '<ellipse cx="-24" cy="-520" rx="230" ry="190" fill="url(#hood-glow)"/>'

# ------------------------------------------------------------------ trailing cape (behind, sways)
CAPE_D = ('M60,-512C100,-508 118,-492 126,-466C146,-400 150,-300 170,-210C186,-140 220,-70 296,-18'
          'C302,-6 290,0 266,0L0,0L0,-420Z')
CAPE = (
    '<g class="hood-cape">'
    + p(CAPE_D, 'url(#hood-cape)')
    + fold(140, -380, 150, -260, 176, -130, 236, -8, 30, .55, '#3a3d4c', .22)
    # pooled train on the deck
    + p('M186,-150C204,-90 240,-50 296,-18C302,-6 290,0 266,0L170,0C206,-6 226,-18 228,-40C210,-70 194,-110 186,-150Z',
        '#0d0d12')
    + cres(228, -40, 258, -24, 296, -18, 0, 5, '#4a1012', .9)
    + cres(136, -410, 146, -330, 158, -262, -4, 0, RIM, .55)
    + cres(200, -118, 232, -58, 296, -18, -3, 3, RIM, .45)
    + '</g>'
)

# ------------------------------------------------------------------ main cloak
BODY_D = ('M-60,-518C-96,-520 -132,-514 -150,-498C-164,-484 -166,-460 -168,-430C-172,-380 -176,-330 -178,-280'
          'C-180,-220 -182,-150 -183,-100C-184,-60 -182,-30 -190,0L210,0C196,-50 172,-130 156,-230'
          'C142,-320 140,-420 122,-470C114,-494 96,-508 60,-512Z')
OPEN_D = 'M-100,-410C-116,-300 -150,-150 -170,0L-92,0C-100,-140 -100,-290 -100,-410Z'
BODY = (
    p(BODY_D, 'url(#hood-body)')
    + p(BODY_D, 'url(#hood-bounce)')
    # shadow cast by the shoulder mantle
    + p('M-176,-440C-140,-426 -96,-408 -60,-386C-10,-410 70,-430 130,-458L140,-420C80,-388 -10,-366 -60,-340'
        'C-100,-368 -150,-392 -184,-400Z', '#000', ' opacity=".5"')
    # folds, lit on the blade side, fading away from it
    + fold(-40, -380, -56, -260, -64, -120, -44, -4, 34, .6, HOT, .34)
    + fold(10, -396, 6, -270, 24, -130, 20, -4, 26, .5, HOT, .2)
    + fold(60, -416, 72, -280, 94, -140, 104, -4, 30, .55, HOT, .1)
    + fold(108, -438, 122, -300, 140, -150, 168, -4, 24, .5, '#3a3d4c', .14)
    + fold(136, -330, 142, -250, 152, -160, 176, -60, 18, .45)
    # the parting: inner dark and a boot
    + p(OPEN_D, '#020203')
    + p('M-198,0C-186,-12 -160,-22 -132,-22L-104,-20L-94,0Z', '#111116')
    + cres(-198, 0, -170, -22, -132, -22, 2, 5, HOT, .7)
    # lit edge of the far flap, facing the blade
    + taper(-100, -410, -100, -290, -100, -140, -92, 0, 9, HOT, .6)
    + taper(-100, -410, -100, -290, -100, -140, -92, 0, 28, HOT, .14)
    + cres(-178, -280, -182, -140, -189, -4, 4, 0, HOT, .7)
)

# ------------------------------------------------------------------ hem on the deck
HEM = (
    '<ellipse cx="30" cy="2" rx="270" ry="9" fill="#000" opacity=".7"/>'
    '<g class="hood-hem">'
    + p('M-94,0C-78,-9 -56,-10 -38,-4C-12,-12 24,-12 48,-4C74,-11 108,-11 128,-4C154,-11 192,-9 214,0Z',
        '#08080b')
    + cres(-94, 0, -66, -14, -38, -4, 0, 3, HOT, .3)
    + cres(-38, -4, 4, -17, 48, -4, 0, 2.5, '#34111a', .7)
    + cres(48, -4, 88, -15, 128, -4, 0, 2, '#22242e', .6)
    + '</g>'
)

# ------------------------------------------------------------------ sword arm and blade
AX, AY = -.3, .954            # blade axis (down and forward)
PX, PY = .954, .3             # across the blade
HX, HY = -216, -296           # the fist


def at(t, s=0.0):
    return HX + AX * t + PX * s, HY + AY * t + PY * s


SLEEVE_D = ('M-128,-506C-164,-490 -178,-430 -194,-382C-204,-354 -222,-340 -234,-326C-226,-312 -204,-304 -188,-308'
            'C-180,-286 -176,-260 -182,-234C-160,-280 -144,-340 -126,-400Z')
E0, TIP = at(26), at(250)
ARM = (
    # plain smooth grip
    line(*at(-26), *at(26), '#191a21', 8)
    + line(*at(-24, 2), *at(-12, 2), '#6a7184', 1.4, .6)
    + line(*at(-28, -4), *at(-28, 4), '#2a2c36', 5)
    + line(*at(26, -8), *at(26, 8), '#30323e', 4.5)
    + line(*at(26, -8), *at(26, -2), HOT, 4.5, .8)
    + f'<g transform="translate({HX},{HY}) rotate(20)">'
    # wrist plate and fist
    + p('M-11,-8L-13,-30L13,-30L12,-8Z', 'url(#hood-plate)')
    + p('M-14,-10C-18,2 -16,16 -1,19C13,18 17,4 13,-10C4,-6 -6,-6 -14,-10Z', '#0e0e12')
    + cres(-16, 0, -15, 17, -1, 19, 4, -3, HOT, .9)
    + cres(-12, -10, -15, -18, -13, -28, 3, 0, HOT, .8)
    + p('M-15,-2C-6,2 6,2 14,-3M-15,6C-6,10 6,10 14,5', 'none', ' stroke="#000" stroke-width="1.4" opacity=".8"')
    + cres(13, -10, 17, 2, 12, 12, -2, 0, '#8a93a8', .35)
    + '</g>'
    # the wide hanging sleeve
    + p(SLEEVE_D, 'url(#hood-body)')
    + p(SLEEVE_D, 'url(#hood-bounce)')
    + fold(-150, -470, -170, -420, -184, -370, -206, -326, 16, .5)
    + fold(-136, -430, -150, -380, -164, -320, -180, -250, 14, .45, HOT, .3)
    + p('M-234,-326C-226,-312 -204,-304 -188,-308C-198,-322 -218,-330 -234,-326Z', '#000')
    + cres(-234, -326, -216, -304, -188, -308, 0, -3.5, HOT, .6)
    + cres(-188, -308, -178, -272, -182, -234, 5, 0, HOT, .6)
)


def blade():
    (ax, ay), (bx, by) = at(26, -4.8), at(26, 4.8)
    (cx, cy), (dx, dy) = at(234, 3), at(234, -3)
    e, t = E0, TIP
    s = '<g class="hood-hum">'
    for w, o in ((64, .05), (40, .08), (26, .14), (16, .3)):
        s += line(e[0], e[1], t[0], t[1], '#ff1e2c', w, o)
    s += '</g>'
    s += (f'<path d="M{n(ax)},{n(ay)}L{n(bx)},{n(by)}L{n(cx)},{n(cy)}L{n(t[0])},{n(t[1])}L{n(dx)},{n(dy)}Z" '
          f'fill="#ff2a38"/>')
    c0, c1 = at(28), at(238)
    s += line(c0[0], c0[1], c1[0], c1[1], '#ffe6de', 3, .95)
    return s


BLADE = (
    f'<ellipse class="hood-hum" cx="{n(TIP[0] + 6)}" cy="-2" rx="150" ry="15" fill="url(#hood-spill)"/>'
    f'<ellipse class="hood-hum" cx="{n(at(140)[0])}" cy="{n(at(140)[1])}" rx="120" ry="170" '
    f'fill="url(#hood-halo)"/>'
    + blade()
)

# ------------------------------------------------------------------ mantle and hood (breathe)
MANTLE_D = ('M-60,-520C-96,-523 -134,-517 -153,-500C-167,-486 -170,-464 -174,-436C-140,-424 -96,-408 -60,-384'
            'C-10,-408 70,-430 130,-456C120,-494 98,-512 50,-520Z')
HOOD_D = ('M-86,-498C-94,-540 -90,-590 -58,-612C-38,-625 -10,-621 4,-600C20,-576 20,-540 32,-496'
          'C6,-478 -60,-478 -86,-498Z')
VOID_D = ('M-75,-508C-83,-544 -77,-584 -53,-596C-31,-602 -13,-584 -11,-556C-9,-530 -17,-508 -31,-494'
          'C-47,-490 -63,-496 -75,-508Z')
TOP = (
    '<g class="hood-breath">'
    + p(MANTLE_D, 'url(#hood-mantle)')
    + p(MANTLE_D, 'url(#hood-under)')
    + fold(56, -506, 80, -490, 96, -470, 104, -448, 20, .45)
    + fold(14, -500, 30, -476, 40, -450, 40, -426, 16, .35)
    + fold(-70, -500, -78, -470, -82, -440, -84, -400, 16, .4, HOT, .22)
    + fold(-112, -508, -130, -480, -128, -450, -112, -416, 20, .45, HOT, .3)
    + fold(-30, -480, -36, -450, -44, -420, -58, -390, 18, .4, HOT, .2)
    # lower edge of the mantle catching the blade
    + cres(-174, -436, -110, -418, -60, -384, 2, -6, HOT, .55)
    + cres(-60, -384, 30, -422, 130, -456, 0, -4, HOT, .16)
    # rim from the limb on the shoulders
    + cres(66, -518, 118, -514, 130, -456, -13, 10, RIM, .9)
    + cres(-84, -521, -136, -522, -158, -494, 2, 3, RIM, .4)
    # cowl
    + '<g transform="translate(-27,-496) scale(1.14) translate(27,496)">'
    + p(HOOD_D, 'url(#hood-cowl)')
    + fold(0, -592, 8, -560, 10, -530, 18, -492, 16, .5)
    + p(VOID_D, '#000')
    # cloth of the opening lit from below, and the far inner wall
    + cres(-75, -508, -56, -488, -31, -494, 0, -6, HOT, .5)
    + cres(-80, -544, -85, -522, -75, -508, 3.5, 0, HOT, .45)
    + p('M-53,-596C-31,-602 -13,-584 -11,-556C-9,-530 -17,-508 -31,-494C-23,-512 -20,-532 -22,-552'
        'C-24,-574 -36,-590 -53,-596Z', '#3a070b', ' opacity=".5"')
    # ember eyes deep inside
    + '<g class="hood-eye">'
      '<circle cx="-58" cy="-553" r="7" fill="url(#hood-eye)" opacity=".7"/>'
      '<circle cx="-38" cy="-552" r="7" fill="url(#hood-eye)" opacity=".7"/>'
      '<path d="M-62,-553.5L-54,-552.4L-58,-551.4Z M-42,-551.6L-34,-552.8L-38,-550.6Z" fill="#ff7a4a" opacity=".85"/>'
      '</g>'
    # rim on the crown and the back of the hood
    + cres(-58, -612, -16, -636, 4, -600, 0, 6, RIM, .8)
    + cres(4, -600, 20, -572, 24, -536, -5, 0, RIM, .9)
    + '</g></g>'
)

LORD = GLOW + CAPE + BODY + HEM + ARM + TOP + BLADE
