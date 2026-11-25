# dxf-geometry-cli (Docker)

Lightweight CLI container for 2D CAD and DXF geometry calculations: raster DPI-to-millimeter calibration, architectural drawing scale conversion, polyline perimeter and polygon area, Ramer-Douglas-Peucker simplification, and ASCII DXF `LWPOLYLINE` export.

## Usage

```bash
# Convert 300 pixels at 300 DPI to millimeters
docker run --rm visualcraftlab/dxf-geometry-cli dpi 300 300

# Convert 20 mm paper length at 1:50 architectural scale
docker run --rm visualcraftlab/dxf-geometry-cli scale 20 50

# Compute perimeter and area of a closed rectangle
docker run --rm visualcraftlab/dxf-geometry-cli poly --closed 0,0 10,0 10,10 0,10

# Simplify noisy vectorized vertices with Ramer-Douglas-Peucker
docker run --rm visualcraftlab/dxf-geometry-cli simplify --epsilon 0.2 0,0 5,0.05 10,0 10,10
```

## Online Reference

- Interactive image-to-CAD converter: [ImgToCAD](https://imgtocad.com/)
- Sketch vectorization reference: [Sketch to CAD](https://imgtocad.com/sketch-to-cad)
- Source code: [visualcraft-lab/dxf-geometry-cli](https://github.com/visualcraft-lab/dxf-geometry-cli)

## License

MIT License — see [LICENSE](LICENSE).
