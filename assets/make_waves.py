"""Generate animated wave banners (SVG, SMIL) used in the GitHub README and Notion portfolio."""
import math, os

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "'Pretendard','Apple SD Gothic Neo','Noto Sans KR','Segoe UI',sans-serif"


def wave(w, base, amp, periods=2, phase=0.0, top=True, h=0):
    """Closed path of a sine wave spanning 2*w (so it can slide by w and loop)."""
    pts = []
    steps = 120
    for i in range(steps + 1):
        x = 2 * w * i / steps
        y = base + amp * math.sin(2 * math.pi * periods * x / w + phase)
        pts.append(f"{x:.1f},{y:.1f}")
    if top:  # fill from top edge down to the wave
        return f"M0,0 L{' L'.join(pts)} L{2*w},0 Z"
    return f"M0,{h} L{' L'.join(pts)} L{2*w},{h} Z"  # fill from wave down to bottom


def layer(d, fill, opacity, dur, w, reverse=False):
    frm, to = ("0", f"-{w}") if not reverse else (f"-{w}", "0")
    return (f'<g opacity="{opacity}"><path d="{d}" fill="{fill}">'
            f'<animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" '
            f'dur="{dur}s" repeatCount="indefinite"/></path></g>')


def header(name, title, sub, out, w=1200, h=240):
    grad = (f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{2*w}" y2="0">'
            '<stop offset="0" stop-color="#1E293B"/><stop offset="0.5" stop-color="#2563EB"/><stop offset="1" stop-color="#1E293B"/></linearGradient>')
    layers = [
        layer(wave(w, h - 46, 14, 1, 0.0, True), "url(#g)", 0.35, 14, w, True),
        layer(wave(w, h - 56, 18, 1, 1.4, True), "url(#g)", 0.55, 10, w),
        layer(wave(w, h - 70, 12, 2, 0.6, True), "url(#g)", 1.0, 8, w, True),
    ]
    text = (
        f'<text x="{w/2}" y="{h*0.36}" text-anchor="middle" font-family="{FONT}" font-size="46" '
        f'font-weight="800" fill="#FFFFFF" opacity="0">{title}'
        '<animate attributeName="opacity" from="0" to="1" begin="0.2s" dur="1.2s" fill="freeze"/></text>'
        f'<text x="{w/2}" y="{h*0.36 + 40}" text-anchor="middle" font-family="{FONT}" font-size="19" '
        f'font-weight="500" fill="#DBEAFE" letter-spacing="1" opacity="0">{sub}'
        '<animate attributeName="opacity" from="0" to="1" begin="0.8s" dur="1.2s" fill="freeze"/></text>'
    )
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'role="img" aria-label="{name}"><defs>{grad}</defs>'
           f'<svg width="{w}" height="{h}" overflow="hidden">{"".join(layers)}</svg>{text}</svg>')
    open(os.path.join(HERE, out), "w", encoding="utf-8").write(svg)


def footer(out, w=1200, h=110):
    grad = (f'<linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{2*w}" y2="0">'
            '<stop offset="0" stop-color="#2563EB"/><stop offset="0.5" stop-color="#1E293B"/><stop offset="1" stop-color="#2563EB"/></linearGradient>')
    layers = [
        layer(wave(w, 40, 12, 1, 0.0, False, h), "url(#g)", 0.35, 14, w),
        layer(wave(w, 52, 14, 1, 1.4, False, h), "url(#g)", 0.55, 10, w, True),
        layer(wave(w, 66, 10, 2, 0.6, False, h), "url(#g)", 1.0, 8, w),
    ]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{grad}</defs><svg width="{w}" height="{h}" overflow="hidden">{"".join(layers)}</svg></svg>')
    open(os.path.join(HERE, out), "w", encoding="utf-8").write(svg)


header("Hwang Yeongho", "Hwang Yeongho", "Java · Spring Boot Backend Developer", "wave-header.svg")
header("RIDEFIT", "RIDEFIT", "오토바이 부품 호환 확인 + 2D 장착 미리보기", "wave-ridefit.svg")
header("EASYS", "EASYS", "스터디 · 멘토링 · 스트리밍 학습 플랫폼", "wave-easys.svg")
footer("wave-footer.svg")
print("ok")
