# Regenerates assets/header.svg and assets/footer.svg. Run: python3 build.py
import math, html, pathlib
e = html.escape
W = 800
ALT = 'Josh Kim. SWE intern at Palantir. Engineer learning to design. Currently reading Creative Selection by Ken Kocienda. Project spotlight: biped physics engine.'
FAM = 'Futura,"Century Gothic","Trebuchet MS",sans-serif'
bg, fg, dim = '#000000', '#f1f1ee', '#a2a29e'
def stripes(H, lenses, p=9, sw=3.4, wave=1.0, pad=10):
    """Wavy lines pushed apart by each lens (cx, cy, half-gap, half-width). Only whole lines are drawn, so none is cut by an edge."""
    d = ''
    for j in range(-12, H//p + 13):
        y0 = j*p + p/2
        pts, lo, hi = [], 1e9, -1e9
        for x in range(-10, W + 11, 8):
            y = y0 + wave*(7*math.sin(x/110 + j*0.13) + 3*math.sin(x/41 - j*0.2))
            for cx, cy, g, sx in lenses:
                u = y0 - cy
                G = math.exp(-((x - cx)/sx)**4)
                y += math.copysign(math.sqrt(u*u + (g*G)**2) - abs(u), u)
            lo, hi = min(lo, y), max(hi, y)
            pts.append('%d %.1f' % (x, y))
        if lo >= pad and hi <= H - pad: d += 'M' + 'L'.join(pts)
    return f'<path d="{d}" fill="none" stroke="{fg}" stroke-width="{sw}"/>'
def svg(h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{e(label)}">'
            f'<style>text{{font-family:{FAM}}}</style><rect width="{W}" height="{h}" fill="{bg}"/>{body}</svg>')
def T(x, y, s, size, fill, bold=False, anchor='start', ls=0):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{500 if bold else 400}" text-anchor="{anchor}" letter-spacing="{ls}">{e(s)}</text>'
H, cy, sy = 560, 196, 452
b = stripes(H, [(400, cy, 84, 318), (262, sy, 50, 250)])
b += T(400, cy - 26, 'Josh Kim', 25, fg, True, 'middle', .3)
b += T(400, cy + 12, 'SWE intern @ Palantir  ·  engineer learning to design', 14, fg, False, 'middle')
b += T(400, cy + 44, 'currently reading Creative Selection by Ken Kocienda', 12.5, dim, False, 'middle', .3)
b += T(132, sy + 6, 'Project spotlight', 20, fg, True) + T(132, sy + 32, 'biped physics engine', 13, dim, False, ls=.3)
pathlib.Path('assets/header.svg').write_text(svg(H, b, ALT))
# The footer is one stripe field cut into three images, one per link, so each image can carry its own link.
LINKS = [('site', 'joshkim.me ↗', 'Visit joshkim.me'), ('x', 'X ↗', 'Follow on X'), ('linkedin', 'LinkedIn ↗', 'Connect on LinkedIn')]
FH, cuts = 120, [0, 267, 534, W]
centres = [(cuts[i] + cuts[i + 1]) / 2 for i in range(3)]
field = stripes(FH, [(c, 60, 22, 92) for c in centres], wave=.4)
for i, (name, label, alt) in enumerate(LINKS):
    x0, w = cuts[i], cuts[i + 1] - cuts[i]
    body = field + T(centres[i], 65, label, 14, fg, True, 'middle')
    pathlib.Path(f'assets/footer-{name}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{FH}" viewBox="{x0} 0 {w} {FH}" role="img" aria-label="{e(alt)}">'
        f'<style>text{{font-family:{FAM}}}</style><rect x="{x0}" width="{w}" height="{FH}" fill="{bg}"/>{body}</svg>')
