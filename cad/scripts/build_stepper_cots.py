#!/usr/bin/env python3
"""
Generate verified COTS STEP models for NEMA 17 Stepper Motors, Planetary Gearboxes,
and ESP32-CAM module to complete the hardware catalog for the 70 cm Stepper-Servo hybrid arm.
"""

import os
import sys
import math
from build123d import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT = os.path.dirname(SCRIPT_DIR)
COMPONENTS_DIR = os.path.join(CAD_ROOT, "components")
os.makedirs(COMPONENTS_DIR, exist_ok=True)

# 1. NEMA 17 Stepper Motor 48mm (17HS19-2004S1 / 42x42x48mm)
def build_nema17_48mm():
    with BuildPart() as p:
        # Main square stator body with corner chamfers
        Box(42.3, 42.3, 48.0)
        # Corner chamfers
        for cx in [-21.15, 21.15]:
            for cy in [-21.15, 21.15]:
                with Locations((cx, cy, 0)):
                    Cylinder(radius=4.5, height=50.0, mode=Mode.SUBTRACT)
        # Front pilot boss: Dia 22.0mm, H = 2.0mm
        with Locations((0, 0, 24.0 + 1.0)):
            Cylinder(radius=11.0, height=2.0)
            # Output shaft: Dia 5.0mm, H = 24.0mm
            with Locations((0, 0, 1.0 + 12.0)):
                Cylinder(radius=2.5, height=24.0)
                # D-flat (0.5mm flat cut over 15mm length)
                with Locations((2.25, 0, 4.5)):
                    Box(1.0, 5.0, 15.0, mode=Mode.SUBTRACT)
        # 4x M3 mounting threaded holes on front face (31.0 x 31.0 mm pitch, 4.5mm depth)
        for hx in [-15.5, 15.5]:
            for hy in [-15.5, 15.5]:
                with Locations((hx, hy, 24.0 - 2.25)):
                    Cylinder(radius=1.5, height=5.0, mode=Mode.SUBTRACT)
        # Rear connector terminal boss
        with Locations((0, -21.15, -16.0)):
            Box(15.0, 4.0, 8.0, mode=Mode.ADD)
    return p.part

# 2. NEMA 17 Stepper Motor 40mm (17HS15-1504S / 42x42x40mm)
def build_nema17_40mm():
    with BuildPart() as p:
        Box(42.3, 42.3, 40.0)
        for cx in [-21.15, 21.15]:
            for cy in [-21.15, 21.15]:
                with Locations((cx, cy, 0)):
                    Cylinder(radius=4.5, height=42.0, mode=Mode.SUBTRACT)
        with Locations((0, 0, 20.0 + 1.0)):
            Cylinder(radius=11.0, height=2.0)
            with Locations((0, 0, 1.0 + 12.0)):
                Cylinder(radius=2.5, height=24.0)
                with Locations((2.25, 0, 4.5)):
                    Box(1.0, 5.0, 15.0, mode=Mode.SUBTRACT)
        for hx in [-15.5, 15.5]:
            for hy in [-15.5, 15.5]:
                with Locations((hx, hy, 20.0 - 2.25)):
                    Cylinder(radius=1.5, height=5.0, mode=Mode.SUBTRACT)
        with Locations((0, -21.15, -12.0)):
            Box(15.0, 4.0, 8.0, mode=Mode.ADD)
    return p.part

# 3. 10:1 Planetary Gearbox (NEMA 17 mount face, 42x42x38mm cylindrical reduction stage, 8mm D-shaft)
def build_planetary_gearbox_10to1():
    with BuildPart() as p:
        # Gearbox body: Dia 36mm reduction barrel with 42x42x5mm front flange
        Cylinder(radius=18.0, height=36.0)
        # Front mounting flange
        with Locations((0, 0, 18.0 - 2.5)):
            Box(42.3, 42.3, 5.0, mode=Mode.ADD)
            for cx in [-21.15, 21.15]:
                for cy in [-21.15, 21.15]:
                    with Locations((cx, cy, 0)):
                        Cylinder(radius=4.5, height=6.0, mode=Mode.SUBTRACT)
        # Front pilot boss: Dia 22.0mm, H = 2.5mm
        with Locations((0, 0, 18.0 + 1.25)):
            Cylinder(radius=11.0, height=2.5)
            # Output shaft: Dia 8.0mm, H = 20.0mm with 7.0mm D-flat
            with Locations((0, 0, 1.25 + 10.0)):
                Cylinder(radius=4.0, height=20.0)
                # D-flat
                with Locations((3.5, 0, 2.5)):
                    Box(1.5, 8.0, 15.0, mode=Mode.SUBTRACT)
        # 4x M3 mounting holes on 31.0 x 31.0 mm pitch through front flange
        for hx in [-15.5, 15.5]:
            for hy in [-15.5, 15.5]:
                with Locations((hx, hy, 18.0 - 5.0)):
                    Cylinder(radius=1.5, height=12.0, mode=Mode.SUBTRACT)
    return p.part

# 4. 5:1 Planetary Gearbox (NEMA 17 mount face, 42x42x28mm cylindrical reduction stage, 8mm D-shaft)
def build_planetary_gearbox_5to1():
    with BuildPart() as p:
        Cylinder(radius=18.0, height=28.0)
        with Locations((0, 0, 14.0 - 2.5)):
            Box(42.3, 42.3, 5.0, mode=Mode.ADD)
            for cx in [-21.15, 21.15]:
                for cy in [-21.15, 21.15]:
                    with Locations((cx, cy, 0)):
                        Cylinder(radius=4.5, height=6.0, mode=Mode.SUBTRACT)
        with Locations((0, 0, 14.0 + 1.25)):
            Cylinder(radius=11.0, height=2.5)
            with Locations((0, 0, 1.25 + 10.0)):
                Cylinder(radius=4.0, height=20.0)
                with Locations((3.5, 0, 2.5)):
                    Box(1.5, 8.0, 15.0, mode=Mode.SUBTRACT)
        for hx in [-15.5, 15.5]:
            for hy in [-15.5, 15.5]:
                with Locations((hx, hy, 14.0 - 5.0)):
                    Cylinder(radius=1.5, height=12.0, mode=Mode.SUBTRACT)
    return p.part

# 5. ESP32-CAM Module (27.0 x 40.5 x 12.0 mm with OV2640 lens)
def build_esp32_cam():
    with BuildPart() as p:
        # PCB substrate: 27.0 x 40.5 x 1.6 mm
        Box(27.0, 40.5, 1.6)
        # 4x corner mounting pads
        # Metal shield can (ESP32-S): 18.0 x 16.0 x 3.0 mm
        with Locations((0, -8.0, 0.8 + 1.5)):
            Box(18.0, 16.0, 3.0)
        # MicroSD card socket on back
        with Locations((0, -10.0, -0.8 - 1.0)):
            Box(14.0, 15.0, 2.0)
        # OV2640 camera sensor turret: 8.5 x 8.5 x 5.0 mm base + Dia 7.0mm lens
        with Locations((0, 12.0, 0.8 + 2.5)):
            Box(8.5, 8.5, 5.0)
            with Locations((0, 0, 2.5 + 2.0)):
                Cylinder(radius=3.5, height=4.0)
                Cylinder(radius=2.0, height=2.0, mode=Mode.SUBTRACT) # lens aperture
    return p.part

if __name__ == "__main__":
    models = {
        "motor_nema17_48mm.step": build_nema17_48mm(),
        "motor_nema17_40mm.step": build_nema17_40mm(),
        "gearbox_planetary_10to1.step": build_planetary_gearbox_10to1(),
        "gearbox_planetary_5to1.step": build_planetary_gearbox_5to1(),
        "camera_esp32_cam.step": build_esp32_cam(),
    }
    for fname, part in models.items():
        out_path = os.path.join(COMPONENTS_DIR, fname)
        export_step(part, out_path)
        print(f"Exported: {fname} (Volume: {part.volume:,.1f} mm^3)")
