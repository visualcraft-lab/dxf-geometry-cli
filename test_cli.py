import unittest
import cli


class TestDxfGeometryCLI(unittest.TestCase):
    def test_polyline_and_area(self):
        sq = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        self.assertAlmostEqual(cli.polyline_length(sq, False), 30.0)
        self.assertAlmostEqual(cli.polyline_length(sq, True), 40.0)
        self.assertAlmostEqual(cli.polygon_area(sq), 100.0)

    def test_dpi_and_scale(self):
        self.assertAlmostEqual(cli.pixels_to_mm(300.0, 300.0), 25.4)
        self.assertAlmostEqual(cli.paper_to_model_scale(20.0, 50.0), 1000.0)

    def test_simplify_and_dxf(self):
        pts = [(0.0, 0.0), (5.0, 0.05), (10.0, 0.0), (10.0, 10.0)]
        simplified = cli.simplify_rdp(pts, 0.2)
        self.assertEqual(len(simplified), 3)
        dxf = cli.format_dxf_polyline(simplified, "WALLS", True)
        self.assertIn("LWPOLYLINE", dxf)
        self.assertIn("WALLS", dxf)
        self.assertIn("EOF", dxf)


if __name__ == "__main__":
    unittest.main()
