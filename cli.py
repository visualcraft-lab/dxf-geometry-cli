#!/usr/bin/env python3
"""Minimal zero-dependency CLI for 2D CAD and DXF geometry calculations."""
from __future__ import annotations

import argparse
import json
import math
import sys
from typing import List, Sequence, Tuple

Point = Tuple[float, float]


def distance(a: Point, b: Point) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def polyline_length(pts: Sequence[Point], closed: bool = False) -> float:
    if len(pts) < 2:
        return 0.0
    total = sum(distance(pts[i - 1], pts[i]) for i in range(1, len(pts)))
    if closed and len(pts) > 2:
        total += distance(pts[-1], pts[0])
    return total


def polygon_area(pts: Sequence[Point]) -> float:
    n = len(pts)
    if n < 3:
        return 0.0
    acc = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    return abs(acc) * 0.5


def pixels_to_mm(pixels: float, dpi: float) -> float:
    return 0.0 if dpi <= 0 else (pixels / dpi) * 25.4


def paper_to_model_scale(paper_length: float, scale_denominator: float) -> float:
    return 0.0 if scale_denominator <= 0 else paper_length * scale_denominator


def _perp_distance(p: Point, a: Point, b: Point) -> float:
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0.0 and dy == 0.0:
        return distance(p, a)
    num = abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0])
    return num / math.hypot(dx, dy)


def simplify_rdp(pts: Sequence[Point], epsilon: float) -> List[Point]:
    if len(pts) <= 2 or epsilon <= 0:
        return list(pts)
    max_dist = -1.0
    index = 0
    for i in range(1, len(pts) - 1):
        d = _perp_distance(pts[i], pts[0], pts[-1])
        if d > max_dist:
            max_dist = d
            index = i
    if max_dist > epsilon:
        left = simplify_rdp(pts[: index + 1], epsilon)
        right = simplify_rdp(pts[index:], epsilon)
        return left[:-1] + right
    return [pts[0], pts[-1]]


def format_dxf_polyline(pts: Sequence[Point], layer: str = "0", closed: bool = False) -> str:
    layer_name = layer or "0"
    flag = 1 if closed else 0
    lines = [
        "0", "SECTION", "2", "ENTITIES",
        "0", "LWPOLYLINE",
        "8", layer_name,
        "90", str(len(pts)),
        "70", str(flag),
    ]
    for x, y in pts:
        lines.extend(["10", f"{x:.4f}", "20", f"{y:.4f}"])
    lines.extend(["0", "ENDSEC", "0", "EOF"])
    return "\n".join(lines) + "\n"


def parse_points(raw: Sequence[str]) -> List[Point]:
    pts: List[Point] = []
    for item in raw:
        x_s, y_s = item.split(",", 1)
        pts.append((float(x_s), float(y_s)))
    return pts


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dxf-geometry-cli", description="2D CAD/DXF geometry utilities")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_dpi = sub.add_parser("dpi", help="Convert pixels at DPI to millimeters")
    p_dpi.add_argument("pixels", type=float)
    p_dpi.add_argument("dpi", type=float)

    p_scale = sub.add_parser("scale", help="Convert paper length using 1:N architectural scale")
    p_scale.add_argument("paper_mm", type=float)
    p_scale.add_argument("denominator", type=float)

    p_poly = sub.add_parser("poly", help="Compute polyline length and polygon area from x,y points")
    p_poly.add_argument("--closed", action="store_true")
    p_poly.add_argument("points", nargs="+", help="Coordinates formatted as x,y")

    p_rdp = sub.add_parser("simplify", help="Simplify polyline using Ramer-Douglas-Peucker")
    p_rdp.add_argument("--epsilon", type=float, required=True)
    p_rdp.add_argument("points", nargs="+", help="Coordinates formatted as x,y")

    p_dxf = sub.add_parser("dxf", help="Emit minimal ASCII DXF LWPOLYLINE block")
    p_dxf.add_argument("--layer", default="0")
    p_dxf.add_argument("--closed", action="store_true")
    p_dxf.add_argument("points", nargs="+", help="Coordinates formatted as x,y")

    args = parser.parse_args(argv)
    if args.cmd == "dpi":
        print(json.dumps({"pixels": args.pixels, "dpi": args.dpi, "mm": round(pixels_to_mm(args.pixels, args.dpi), 6)}))
    elif args.cmd == "scale":
        print(json.dumps({"paper_mm": args.paper_mm, "scale": f"1:{args.denominator:g}", "model_mm": round(paper_to_model_scale(args.paper_mm, args.denominator), 6)}))
    elif args.cmd == "poly":
        pts = parse_points(args.points)
        print(json.dumps({"length": round(polyline_length(pts, args.closed), 6), "area": round(polygon_area(pts), 6)}))
    elif args.cmd == "simplify":
        pts = parse_points(args.points)
        out = simplify_rdp(pts, args.epsilon)
        print(json.dumps({"input_count": len(pts), "output_count": len(out), "points": out}))
    elif args.cmd == "dxf":
        pts = parse_points(args.points)
        sys.stdout.write(format_dxf_polyline(pts, args.layer, args.closed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
