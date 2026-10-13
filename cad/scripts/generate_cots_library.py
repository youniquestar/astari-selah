#!/usr/bin/env python3
"""
================================================================================
ASTARI SELAH — HIGH-PRECISION COTS HARDWARE LIBRARY GENERATOR
================================================================================
Constructs accurate, production-grade 3D STEP models of all COTS actuators,
bearings, sensors, and ISO/DIN fasteners using build123d.
================================================================================
"""

import os
import math
from build123d import *

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT = os.path.dirname(SCRIPT_DIR)
COMPONENTS_DIR = os.path.join(CAD_ROOT, "components")
FASTENERS_DIR = os.path.join(CAD_ROOT, "fasteners")

os.makedirs(COMPONENTS_DIR, exist_ok=True)
os.makedirs(FASTENERS_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. DSSERVO RDS5160 (60 kg·cm High-Torque Digital Servo)
# ------------------------------------------------------------------------------
def generate_rds5160():
    print("Generating DSSERVO RDS5160...")
    with BuildPart() as p:
        # Main body housing
        Box(60.0, 30.0, 48.0)
        # Mounting flanges
        with Locations((0, 0, 10.0)):
            Box(75.0, 30.0, 4.0)
        # Mounting screw slots on flanges (4x M3)
        with Locations((0, 0, 10.0)):
            with GridLocations(68.0, 10.0, 2, 2):
                Cylinder(radius=1.8, height=10.0, mode=Mode.SUBTRACT)
        # Aluminum heatsink cooling fins around center
        for z in [-2.0, 0.0, 2.0]:
            with Locations((0, 0, z)):
                Box(60.6, 30.6, 1.2, mode=Mode.ADD)
        # Output spline turret & 25T gear shaft
        with Locations((-14.0, 0.0, 24.0)):
            Cylinder(radius=10.0, height=5.0)
            with Locations((0, 0, 5.0)):
                Cylinder(radius=3.0, height=5.0)
                # Tapped center screw hole
                Cylinder(radius=1.2, height=6.0, mode=Mode.SUBTRACT)
        # Wire strain relief exit block
        with Locations((26.0, 0.0, -20.0)):
            Box(6.0, 8.0, 6.0)
            
    export_step(p.part, os.path.join(COMPONENTS_DIR, "servo_rds5160_60kg.step"))
    print("  ✓ Saved servo_rds5160_60kg.step")

# ------------------------------------------------------------------------------
# 2. TowerPro MG996R (11 kg·cm Metal Gear Standard Servo)
# ------------------------------------------------------------------------------
def generate_mg996r():
    print("Generating TowerPro MG996R...")
    with BuildPart() as p:
        # Main body
        Box(40.7, 19.7, 42.9)
        # Mounting tabs
        with Locations((0, 0, 6.0)):
            Box(54.0, 19.0, 2.8)
        # Eyelet holes (4x M2.5)
        with Locations((0, 0, 6.0)):
            with GridLocations(48.0, 10.0, 2, 2):
                Cylinder(radius=1.3, height=8.0, mode=Mode.SUBTRACT)
        # Output turret & 25T spline
        with Locations((-10.0, 0.0, 21.45)):
            Cylinder(radius=6.0, height=4.5)
            with Locations((0, 0, 4.5)):
                Cylinder(radius=2.9, height=4.5)
                Cylinder(radius=1.2, height=5.0, mode=Mode.SUBTRACT)
                
    export_step(p.part, os.path.join(COMPONENTS_DIR, "servo_mg996r.step"))
    print("  ✓ Saved servo_mg996r.step")

# ------------------------------------------------------------------------------
# 3. 6812ZZ Thin Section Deep Groove Ball Bearing (60x78x10mm)
# ------------------------------------------------------------------------------
def generate_bearing_6812zz():
    print("Generating 6812ZZ Bearing...")
    with BuildPart() as p:
        # Outer ring
        Cylinder(radius=78.0 / 2, height=10.0)
        # Inner bore
        Cylinder(radius=60.0 / 2, height=12.0, mode=Mode.SUBTRACT)
        # Shield recesses on top and bottom
        for z in [4.5, -4.5]:
            with Locations((0, 0, z)):
                Cylinder(radius=75.0 / 2, height=1.5, mode=Mode.SUBTRACT)
                Cylinder(radius=63.0 / 2, height=2.0, mode=Mode.ADD)
                Cylinder(radius=60.0 / 2, height=3.0, mode=Mode.SUBTRACT)
                
    export_step(p.part, os.path.join(COMPONENTS_DIR, "bearing_6812zz_turntable.step"))
    print("  ✓ Saved bearing_6812zz_turntable.step")

# ------------------------------------------------------------------------------
# 4. 608ZZ Miniature Radial Ball Bearing (8x22x7mm)
# ------------------------------------------------------------------------------
def generate_bearing_608zz():
    print("Generating 608ZZ Bearing...")
    with BuildPart() as p:
        # Outer ring
        Cylinder(radius=22.0 / 2, height=7.0)
        # Inner bore
        Cylinder(radius=8.0 / 2, height=9.0, mode=Mode.SUBTRACT)
        # Dust shield grooves
        for z in [3.0, -3.0]:
            with Locations((0, 0, z)):
                Cylinder(radius=20.5 / 2, height=1.2, mode=Mode.SUBTRACT)
                Cylinder(radius=9.5 / 2, height=1.5, mode=Mode.ADD)
                Cylinder(radius=8.0 / 2, height=2.0, mode=Mode.SUBTRACT)
                
    export_step(p.part, os.path.join(COMPONENTS_DIR, "bearing_608zz_counter_pivot.step"))
    print("  ✓ Saved bearing_608zz_counter_pivot.step")

# ------------------------------------------------------------------------------
# 5. Interlink Electronics FSR 402 Force Sensor
# ------------------------------------------------------------------------------
def generate_fsr402():
    print("Generating FSR 402 Sensor...")
    with BuildPart() as p:
        # Active circular sensing area
        Cylinder(radius=18.3 / 2, height=0.45)
        # Flexible tail
        with Locations((0, -25.0, 0.0)):
            Box(5.0, 36.0, 0.25)
        # Solder pin tabs
        with Locations((0, -44.0, 0.0)):
            with GridLocations(2.54, 1.0, 2, 1):
                Box(1.0, 3.0, 0.3)
                
    export_step(p.part, os.path.join(COMPONENTS_DIR, "sensor_fsr402_tactile.step"))
    print("  ✓ Saved sensor_fsr402_tactile.step")

# ------------------------------------------------------------------------------
# 6. ISO 4762 / DIN 912 Fasteners (M8, M4, M3)
# ------------------------------------------------------------------------------
def generate_fasteners():
    print("Generating ISO Fasteners...")
    # M8 x 30mm Hex Bolt + M8 Nyloc Nut
    with BuildPart() as m8_bolt:
        Cylinder(radius=8.0 / 2, height=30.0)
        with Locations((0, 0, 15.0)):
            with BuildSketch() as s:
                RegularPolygon(radius=13.0 / math.sqrt(3), side_count=6)
            extrude(amount=5.5)
    export_step(m8_bolt.part, os.path.join(FASTENERS_DIR, "bolt_m8x30_hex.step"))
    
    with BuildPart() as m8_nut:
        with BuildSketch() as s:
            RegularPolygon(radius=13.0 / math.sqrt(3), side_count=6)
        extrude(amount=6.8)
        Cylinder(radius=8.0 / 2, height=10.0, mode=Mode.SUBTRACT)
    export_step(m8_nut.part, os.path.join(FASTENERS_DIR, "nut_m8_nyloc.step"))

    # M4 x 16mm SHCS
    with BuildPart() as m4_shcs:
        Cylinder(radius=4.0 / 2, height=16.0)
        with Locations((0, 0, 8.0)):
            Cylinder(radius=7.0 / 2, height=4.0)
            with Locations((0, 0, 2.0)):
                with BuildSketch() as s:
                    RegularPolygon(radius=3.0 / math.sqrt(3), side_count=6)
                extrude(amount=2.5, mode=Mode.SUBTRACT)
    export_step(m4_shcs.part, os.path.join(FASTENERS_DIR, "screw_m4x16_shcs.step"))

    # M3 x 16mm SHCS
    with BuildPart() as m3_shcs:
        Cylinder(radius=3.0 / 2, height=16.0)
        with Locations((0, 0, 8.0)):
            Cylinder(radius=5.5 / 2, height=3.0)
            with Locations((0, 0, 1.5)):
                with BuildSketch() as s:
                    RegularPolygon(radius=2.5 / math.sqrt(3), side_count=6)
                extrude(amount=2.0, mode=Mode.SUBTRACT)
    export_step(m3_shcs.part, os.path.join(FASTENERS_DIR, "screw_m3x16_shcs.step"))

    print("  ✓ All standard ISO fasteners generated.")

if __name__ == "__main__":
    generate_rds5160()
    generate_mg996r()
    generate_bearing_6812zz()
    generate_bearing_608zz()
    generate_fsr402()
    generate_fasteners()
    print("Hardware COTS library successfully generated in STEP format!")
