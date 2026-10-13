"""
=================================================================================
FINAL COMPLETE 3D MODEL — 5-DOF Robotic Arm
=================================================================================
Generates every structural part, electronic component, servo motor, bearing,
fastener, and screw as INDIVIDUAL STEP files, then assembles everything into
a single master STEP assembly with realistic color assignments.

Color Scheme:
  - Structural 3D-printed parts: Alternating BLUE (#0044BB) and BLACK (#1A1A1A)
  - Servos:        Matte black / dark grey aluminium
  - Bearings:      Chrome silver
  - Fasteners:     Stainless steel / zinc-plated
  - ESP32:         Charcoal PCB with gold antenna
  - PCB boards:    Dark green FR4
  - Buck converters: Blue/Red PCB with aluminium heatsinks
  - LiPo battery:  Yellow warning label on black pack
  - PCA9685:       Purple breakout board
  - Wiring:        Red/black silicone

Export Structure (all in cad_export/final_3d_model/):
  parts/           — Structural arm components (base, yoke, upper arm, etc.)
  components/      — Electronic modules (ESP32, PCA9685, servos, etc.)
  fasteners/       — Screws, bolts, nuts, washers
  assembly/        — Full unified assembly STEP
=================================================================================
"""

import cadquery as cq
import os
import math
import shutil

# ==============================================================================
# OUTPUT PATHS
# ==============================================================================
EXPORT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTS_DIR      = os.path.join(EXPORT_ROOT, "parts")
COMPONENTS_DIR = os.path.join(EXPORT_ROOT, "components")
FASTENERS_DIR  = os.path.join(EXPORT_ROOT, "fasteners")
ASSEMBLY_DIR   = os.path.join(EXPORT_ROOT, "assembly")

for d in [PARTS_DIR, COMPONENTS_DIR, FASTENERS_DIR, ASSEMBLY_DIR]:
    os.makedirs(d, exist_ok=True)

# ==============================================================================
# COLOR PALETTE
# ==============================================================================
# Structural arm body colors — alternating blue and black
BLUE         = cq.Color(0.0, 0.27, 0.73, 1.0)      # Deep rich blue
BLACK        = cq.Color(0.10, 0.10, 0.10, 1.0)      # Near-black PETG/PLA+
DARK_BLUE    = cq.Color(0.05, 0.15, 0.55, 1.0)      # Accent dark blue

# Component-accurate colors
CHROME       = cq.Color(0.78, 0.80, 0.82, 1.0)      # Bearing / stainless steel
STEEL        = cq.Color(0.55, 0.57, 0.58, 1.0)      # Zinc-plated fasteners
SERVO_BLACK  = cq.Color(0.12, 0.12, 0.14, 1.0)      # Matte servo body
SERVO_ALU    = cq.Color(0.70, 0.72, 0.74, 1.0)      # Brushed aluminum horn
FR4_GREEN    = cq.Color(0.08, 0.45, 0.15, 1.0)      # Solder-mask green
ESP_CHARCOAL = cq.Color(0.15, 0.15, 0.18, 1.0)      # ESP32 PCB
GOLD_TRACE   = cq.Color(0.85, 0.72, 0.20, 1.0)      # Antenna / traces
RED_PCB      = cq.Color(0.65, 0.12, 0.12, 1.0)      # XL4016 board
BLUE_PCB     = cq.Color(0.12, 0.30, 0.75, 1.0)      # LM2596 board
PURPLE_PCB   = cq.Color(0.40, 0.10, 0.60, 1.0)      # PCA9685 breakout
LIPO_BLACK   = cq.Color(0.08, 0.08, 0.08, 1.0)      # Battery pack
LIPO_YELLOW  = cq.Color(0.95, 0.85, 0.05, 1.0)      # Battery warning label
COPPER       = cq.Color(0.80, 0.50, 0.20, 1.0)      # Wire / copper
RUBBER_BLACK = cq.Color(0.06, 0.06, 0.06, 1.0)      # Rubber feet / grommets
GREEN_TERM   = cq.Color(0.10, 0.70, 0.20, 1.0)      # Screw terminal blocks
HEATSINK_ALU = cq.Color(0.75, 0.75, 0.78, 1.0)      # Aluminum heatsink
CAP_BLACK    = cq.Color(0.05, 0.05, 0.05, 1.0)      # Electrolytic capacitor

# ==============================================================================
# HELPER: PARAMETRIC FASTENER GENERATORS
# ==============================================================================

def m3_socket_head_cap_screw(length=10.0):
    """ISO 4762 M3 Socket Head Cap Screw"""
    head = cq.Workplane("XY").circle(2.75).extrude(3.0)      # Ø5.5 head, 3mm tall
    # Hex socket recess — cut from the head solid
    hex_cut = cq.Workplane("XY").workplane(offset=1.0).polygon(6, 2.5).extrude(2.1)
    head = head.cut(hex_cut)
    shaft = cq.Workplane("XY").circle(1.5).extrude(-length)   # M3 shaft
    screw = head.union(shaft)
    return screw

def m3_hex_nut():
    """ISO 4032 M3 Hex Nut"""
    nut = (
        cq.Workplane("XY")
        .polygon(6, 6.01)    # 5.5mm across flats → 6.01mm circumradius
        .extrude(2.4)
        .faces(">Z").workplane()
        .circle(1.5)
        .cutThruAll()
    )
    return nut

def m3_washer():
    """DIN 125 M3 Flat Washer"""
    washer = (
        cq.Workplane("XY")
        .circle(3.5)
        .circle(1.6)
        .extrude(0.5)
    )
    return washer

def m8_hex_bolt(length=30.0):
    """ISO 4014 M8 Hex Bolt"""
    head = cq.Workplane("XY").polygon(6, 14.38).extrude(5.3)   # 13mm AF
    shaft = cq.Workplane("XY").circle(4.0).extrude(-length)
    bolt = head.union(shaft)
    return bolt

def m8_hex_nut():
    """ISO 4032 M8 Hex Nut"""
    nut = (
        cq.Workplane("XY")
        .polygon(6, 14.38)
        .extrude(6.5)
        .faces(">Z").workplane()
        .circle(4.0)
        .cutThruAll()
    )
    return nut

def m4_socket_head_cap_screw(length=16.0):
    """ISO 4762 M4 Socket Head Cap Screw"""
    head = cq.Workplane("XY").circle(3.5).extrude(4.0)
    shaft = cq.Workplane("XY").circle(2.0).extrude(-length)
    return head.union(shaft)

# ==============================================================================
# COMPONENT GENERATORS
# ==============================================================================

def create_rds5160_servo():
    """DSSERVO RDS5160 — 60.0×30.0×55.0mm with spline at top"""
    body = cq.Workplane("XY").box(60.0, 30.0, 55.0)
    # Mounting flanges (74mm pitch along X, 10mm wide, 2.5mm thick tabs)
    left_tab = cq.Workplane("XY").box(7.0, 30.0, 2.5).translate((-33.5, 0, 0))
    right_tab = cq.Workplane("XY").box(7.0, 30.0, 2.5).translate((33.5, 0, 0))
    servo = body.union(left_tab).union(right_tab)
    # Output spline cylinder on top
    spline = cq.Workplane("XY").workplane(offset=27.5).circle(10.0).extrude(5.0)
    servo = servo.union(spline)
    # Spline gear teeth impression (visual only)
    spline_teeth = cq.Workplane("XY").workplane(offset=32.0).polygon(25, 9.0).extrude(0.5)
    servo = servo.union(spline_teeth)
    return servo

def create_mg996r_servo():
    """TowerPro MG996R — 40.7×19.7×42.0mm"""
    body = cq.Workplane("XY").box(40.7, 19.7, 42.0)
    # Mounting flanges
    left_tab = cq.Workplane("XY").box(3.65, 19.7, 2.5).translate((-22.175, 0, 0))
    right_tab = cq.Workplane("XY").box(3.65, 19.7, 2.5).translate((22.175, 0, 0))
    servo = body.union(left_tab).union(right_tab)
    # Output spline
    spline = cq.Workplane("XY").workplane(offset=21.0).circle(7.0).extrude(4.0)
    servo = servo.union(spline)
    return servo

def create_6812zz_bearing():
    """6812ZZ Deep Groove Ball Bearing: 60mm ID × 78mm OD × 10mm W"""
    outer = cq.Workplane("XY").circle(78.0 / 2.0).circle(60.0 / 2.0).extrude(10.0)
    return outer

def create_608zz_bearing():
    """608ZZ Bearing: 8mm ID × 22mm OD × 7mm W"""
    bearing = cq.Workplane("XY").circle(22.0 / 2.0).circle(8.0 / 2.0).extrude(7.0)
    return bearing

def create_esp32_nodemcu():
    """ESP32 NodeMCU DevKit — 52×28×6mm with antenna block"""
    pcb = cq.Workplane("XY").box(28.0, 52.0, 1.6)
    # USB-C port
    usb = cq.Workplane("XY").box(9.0, 7.0, 3.2).translate((0, -26.0 + 3.5, 1.6))
    # Chip module
    chip = cq.Workplane("XY").box(18.0, 18.0, 3.0).translate((0, 5.0, 1.6))
    # Antenna trace block
    antenna = cq.Workplane("XY").box(18.0, 7.0, 0.5).translate((0, 26.0 - 3.5, 2.5))
    # Pin headers (left and right)
    left_pins = cq.Workplane("XY").box(2.54, 44.0, 8.5).translate((-12.0, 0, -4.25))
    right_pins = cq.Workplane("XY").box(2.54, 44.0, 8.5).translate((12.0, 0, -4.25))
    esp = pcb.union(usb).union(chip).union(antenna).union(left_pins).union(right_pins)
    return esp, antenna, pcb

def create_pca9685_board():
    """PCA9685 16-Channel I2C PWM/Servo Driver — 62×25×12mm"""
    pcb = cq.Workplane("XY").box(62.0, 25.0, 1.6)
    # Servo pin headers (16 × 3-pin rows along the top edge)
    pin_block = cq.Workplane("XY").box(58.0, 8.0, 8.5).translate((0, -8.0, 5.0))
    # IC chip
    chip = cq.Workplane("XY").box(8.0, 8.0, 2.0).translate((0, 5.0, 1.6))
    # Capacitor
    cap = cq.Workplane("XY").circle(3.0).extrude(8.0).translate((20.0, 5.0, 1.6))
    board = pcb.union(pin_block).union(chip).union(cap)
    return board

def create_xl4016_module():
    """XL4016 Step-Down Buck — 61×50×25mm with dual heatsinks"""
    pcb = cq.Workplane("XY").box(61.0, 50.0, 1.6)
    # Dual heatsinks
    hs1 = cq.Workplane("XY").box(12.0, 34.0, 18.0).translate((-18.0, 0, 10.0))
    hs2 = cq.Workplane("XY").box(12.0, 34.0, 18.0).translate((18.0, 0, 10.0))
    # Heatsink fin cuts (for realism)
    for i in range(5):
        for hs_x in [-18.0, 18.0]:
            fin = cq.Workplane("XY").box(1.0, 30.0, 16.0).translate((hs_x, 0, 10.0 + (i - 2) * 0.5))
    # Potentiometer
    pot = cq.Workplane("XY").box(6.0, 6.0, 4.0).translate((0, 20.0, 3.0))
    # Screw terminals
    term_in = cq.Workplane("XY").box(10.0, 8.0, 9.0).translate((-22.0, 0, 5.5))
    term_out = cq.Workplane("XY").box(10.0, 8.0, 9.0).translate((22.0, 0, 5.5))
    module = pcb.union(hs1).union(hs2).union(pot).union(term_in).union(term_out)
    return module, hs1, hs2

def create_lm2596_module():
    """LM2596 Step-Down Buck — 43×21×14mm"""
    pcb = cq.Workplane("XY").box(43.0, 21.0, 1.6)
    inductor = cq.Workplane("XY").workplane(offset=0.8).circle(6.0).extrude(7.0).translate((2.0, 0, 0))
    pot = cq.Workplane("XY").box(9.5, 4.5, 10.0).translate((-12.0, 3.0, 6.0))
    cap = cq.Workplane("XY").circle(4.0).extrude(8.0).translate((15.0, 0, 0.8))
    module = pcb.union(inductor).union(pot).union(cap)
    return module

def create_lipo_3s():
    """3S 11.1V LiPo Battery Pack — 75×35×26mm"""
    body = cq.Workplane("XY").box(75.0, 35.0, 26.0)
    # Warning label (raised)
    label = cq.Workplane("XY").box(40.0, 25.0, 0.3).translate((0, 0, 13.15))
    # Balance connector
    balance = cq.Workplane("XY").box(12.0, 8.0, 5.0).translate((-37.5 + 6.0, 0, -13.0 + 2.5))
    # XT60 connector
    xt60 = cq.Workplane("XY").box(16.0, 8.0, 7.0).translate((37.5 - 8.0, 0, -13.0 + 3.5))
    return body, label, balance, xt60

def create_screw_terminal_2pin():
    """5.08mm pitch 2-pin screw terminal block"""
    body = cq.Workplane("XY").box(10.16, 8.0, 10.0)
    # Screw holes
    body = body.faces(">Z").workplane().pushPoints([(-2.54, 0), (2.54, 0)]).circle(1.6).cutBlind(-3.0)
    return body

def create_electrolytic_cap(dia=10.0, height=16.0):
    """Radial electrolytic capacitor"""
    body = cq.Workplane("XY").circle(dia / 2.0).extrude(height)
    # Top vent cross
    vent_h = cq.Workplane("XY").workplane(offset=height - 0.5).center(0, 0).rect(dia * 0.6, 1.0).extrude(0.6)
    vent_v = cq.Workplane("XY").workplane(offset=height - 0.5).center(0, 0).rect(1.0, dia * 0.6).extrude(0.6)
    body = body.cut(vent_h).cut(vent_v)
    return body

def create_servo_horn_round():
    """25T Round Aluminum Servo Horn Ø25.4mm"""
    horn = cq.Workplane("XY").circle(25.4 / 2.0).extrude(2.0)
    # Center spline hole
    horn = horn.faces(">Z").workplane().circle(3.0).cutThruAll()
    # 4× M3 mounting holes at 14mm PCD
    bolt_pts = [(7.0 * math.cos(math.radians(a)), 7.0 * math.sin(math.radians(a))) for a in [45, 135, 225, 315]]
    horn = horn.faces(">Z").workplane().pushPoints(bolt_pts).hole(3.2)
    return horn

def create_rubber_foot():
    """Ø15mm adhesive rubber bumper foot"""
    foot = cq.Workplane("XY").circle(7.5).extrude(3.0)
    foot = foot.edges(">Z").fillet(1.0)
    return foot

# ==============================================================================
# GENERATE AND EXPORT ALL INDIVIDUAL PARTS
# ==============================================================================
print("=" * 70)
print("  FINAL 3D MODEL — 5-DOF Robotic Arm")
print("  Generating all individual parts and components...")
print("=" * 70)

# --- Import existing structural parts from prior generation ---
SRC_ASM = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export/base_enclosure_fused_assembly")
SRC_GRP = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export/gripper_assembly")

structural_parts = {
    "base_enclosure":        os.path.join(SRC_ASM, "base_enclosure_fused.step"),
    "shoulder_yoke":         os.path.join(SRC_ASM, "complete_shoulder_yoke_axis.step"),
    "upper_arm":             os.path.join(SRC_ASM, "link_1_upper_arm.step"),
    "forearm":               os.path.join(SRC_ASM, "link_2_forearm.step"),
    "wrist":                 os.path.join(SRC_ASM, "link_3_wrist_assembly.step"),
    "gripper_base":          os.path.join(SRC_GRP, "gripper_base.step"),
    "gripper_left_finger":   os.path.join(SRC_GRP, "gripper_left_finger.step"),
    "gripper_right_finger":  os.path.join(SRC_GRP, "gripper_right_finger.step"),
}

# Copy structural parts to final_3d_model/parts/
print("\n[1/6] Copying structural parts...")
for name, src in structural_parts.items():
    dst = os.path.join(PARTS_DIR, f"{name}.step")
    if os.path.exists(dst):
        print(f"  ✓ {name} (already present in parts/)")
    elif os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"  ✓ {name}")
    else:
        print(f"  ✗ MISSING: {src}")

# --- Generate electronic components ---
print("\n[2/6] Generating electronic components...")

# Servos
rds5160 = create_rds5160_servo()
cq.exporters.export(rds5160, os.path.join(COMPONENTS_DIR, "servo_rds5160_yaw.step"))
print("  ✓ DSSERVO RDS5160 (Yaw)")

rds5160_shoulder = create_rds5160_servo()
cq.exporters.export(rds5160_shoulder, os.path.join(COMPONENTS_DIR, "servo_rds5160_shoulder.step"))
print("  ✓ DSSERVO RDS5160 (Shoulder)")

mg996r_elbow = create_mg996r_servo()
cq.exporters.export(mg996r_elbow, os.path.join(COMPONENTS_DIR, "servo_mg996r_elbow.step"))
print("  ✓ TowerPro MG996R (Elbow)")

mg996r_wrist = create_mg996r_servo()
cq.exporters.export(mg996r_wrist, os.path.join(COMPONENTS_DIR, "servo_mg996r_wrist.step"))
print("  ✓ TowerPro MG996R (Wrist)")

mg996r_gripper = create_mg996r_servo()
cq.exporters.export(mg996r_gripper, os.path.join(COMPONENTS_DIR, "servo_mg996r_gripper.step"))
print("  ✓ TowerPro MG996R (Gripper)")

# Bearings
bearing_6812 = create_6812zz_bearing()
cq.exporters.export(bearing_6812, os.path.join(COMPONENTS_DIR, "bearing_6812zz.step"))
print("  ✓ 6812ZZ Bearing (Yaw)")

bearing_608_shoulder = create_608zz_bearing()
cq.exporters.export(bearing_608_shoulder, os.path.join(COMPONENTS_DIR, "bearing_608zz_shoulder.step"))
print("  ✓ 608ZZ Bearing (Shoulder)")

bearing_608_elbow = create_608zz_bearing()
cq.exporters.export(bearing_608_elbow, os.path.join(COMPONENTS_DIR, "bearing_608zz_elbow.step"))
print("  ✓ 608ZZ Bearing (Elbow)")

bearing_608_wrist = create_608zz_bearing()
cq.exporters.export(bearing_608_wrist, os.path.join(COMPONENTS_DIR, "bearing_608zz_wrist.step"))
print("  ✓ 608ZZ Bearing (Wrist)")

# Electronics
esp32_full, esp32_ant, esp32_pcb = create_esp32_nodemcu()
cq.exporters.export(esp32_full, os.path.join(COMPONENTS_DIR, "esp32_nodemcu.step"))
print("  ✓ ESP32 NodeMCU")

pca9685 = create_pca9685_board()
cq.exporters.export(pca9685, os.path.join(COMPONENTS_DIR, "pca9685_pwm_driver.step"))
print("  ✓ PCA9685 PWM Driver")

xl4016_mod, xl_hs1, xl_hs2 = create_xl4016_module()
cq.exporters.export(xl4016_mod, os.path.join(COMPONENTS_DIR, "xl4016_buck_converter.step"))
print("  ✓ XL4016 Buck Converter")

lm2596_mod = create_lm2596_module()
cq.exporters.export(lm2596_mod, os.path.join(COMPONENTS_DIR, "lm2596_buck_converter.step"))
print("  ✓ LM2596 Buck Converter")

lipo_body, lipo_label, lipo_bal, lipo_xt60 = create_lipo_3s()
lipo_full = lipo_body.union(lipo_label).union(lipo_bal).union(lipo_xt60)
cq.exporters.export(lipo_full, os.path.join(COMPONENTS_DIR, "lipo_3s_battery.step"))
print("  ✓ 3S LiPo Battery")

servo_horn = create_servo_horn_round()
cq.exporters.export(servo_horn, os.path.join(COMPONENTS_DIR, "servo_horn_round_25t.step"))
print("  ✓ Round 25T Servo Horn")

term_block = create_screw_terminal_2pin()
cq.exporters.export(term_block, os.path.join(COMPONENTS_DIR, "screw_terminal_2pin.step"))
print("  ✓ 2-Pin Screw Terminal")

cap_1000uf = create_electrolytic_cap(10.0, 16.0)
cq.exporters.export(cap_1000uf, os.path.join(COMPONENTS_DIR, "capacitor_1000uf.step"))
print("  ✓ 1000µF Capacitor")

cap_470uf = create_electrolytic_cap(8.0, 12.0)
cq.exporters.export(cap_470uf, os.path.join(COMPONENTS_DIR, "capacitor_470uf.step"))
print("  ✓ 470µF Capacitor")

rubber = create_rubber_foot()
cq.exporters.export(rubber, os.path.join(COMPONENTS_DIR, "rubber_foot.step"))
print("  ✓ Rubber Foot")

# --- Generate fasteners ---
print("\n[3/6] Generating fasteners...")

m3x10 = m3_socket_head_cap_screw(10.0)
cq.exporters.export(m3x10, os.path.join(FASTENERS_DIR, "m3x10_shcs.step"))
print("  ✓ M3×10 SHCS")

m3x16 = m3_socket_head_cap_screw(16.0)
cq.exporters.export(m3x16, os.path.join(FASTENERS_DIR, "m3x16_shcs.step"))
print("  ✓ M3×16 SHCS")

m3x20 = m3_socket_head_cap_screw(20.0)
cq.exporters.export(m3x20, os.path.join(FASTENERS_DIR, "m3x20_shcs.step"))
print("  ✓ M3×20 SHCS")

m3_nut = m3_hex_nut()
cq.exporters.export(m3_nut, os.path.join(FASTENERS_DIR, "m3_hex_nut.step"))
print("  ✓ M3 Hex Nut")

m3_wash = m3_washer()
cq.exporters.export(m3_wash, os.path.join(FASTENERS_DIR, "m3_washer.step"))
print("  ✓ M3 Washer")

m8x30 = m8_hex_bolt(30.0)
cq.exporters.export(m8x30, os.path.join(FASTENERS_DIR, "m8x30_hex_bolt.step"))
print("  ✓ M8×30 Hex Bolt")

m8_nut_part = m8_hex_nut()
cq.exporters.export(m8_nut_part, os.path.join(FASTENERS_DIR, "m8_hex_nut.step"))
print("  ✓ M8 Hex Nut")

m4x16 = m4_socket_head_cap_screw(16.0)
cq.exporters.export(m4x16, os.path.join(FASTENERS_DIR, "m4x16_shcs.step"))
print("  ✓ M4×16 SHCS")

# ==============================================================================
# LOAD STRUCTURAL PARTS FROM STEP FILES
# ==============================================================================
print("\n[4/6] Loading structural STEP files for assembly...")

base_solid       = cq.importers.importStep(structural_parts["base_enclosure"])
yoke_solid       = cq.importers.importStep(structural_parts["shoulder_yoke"])
upper_arm_solid  = cq.importers.importStep(structural_parts["upper_arm"])
forearm_solid    = cq.importers.importStep(structural_parts["forearm"])
wrist_solid      = cq.importers.importStep(structural_parts["wrist"])
grip_base_solid  = cq.importers.importStep(structural_parts["gripper_base"])
grip_left_solid  = cq.importers.importStep(structural_parts["gripper_left_finger"])
grip_right_solid = cq.importers.importStep(structural_parts["gripper_right_finger"])

print("  All structural STEP files loaded.")

# ==============================================================================
# ASSEMBLE COMPLETE ARM
# ==============================================================================
print("\n[5/6] Building master assembly with 50+ components...")

# --- Z-axis kinematic positions (arm standing straight up) ---
Z_BASE       = 0.0
Z_ROOF       = 85.0                         # Top of base enclosure
Z_TURNTABLE  = Z_ROOF                       # Turntable plate sits on roof
Z_YOKE_BASE  = Z_TURNTABLE + 8.0            # Yoke base plate on top of turntable
Z_PIVOT      = Z_YOKE_BASE + 55.0           # Shoulder pitch axis
Z_ELBOW      = Z_PIVOT + 220.0              # Upper arm is 220mm long
Z_WRIST      = Z_ELBOW + 180.0              # Forearm is 180mm long

# Gripper extends from wrist
Z_GRIP_SERVO = Z_WRIST + 95.0 - 60.0        # Gripper servo center
Z_GRIP_PIVOT = Z_WRIST + 105.5              # Finger pivot line

# Base internal electronics Z
Z_FLOOR       = 5.0                          # Top of floor plate
Z_STANDOFF    = Z_FLOOR + 5.0               # Top of standoffs
Z_PCB_TOP     = Z_STANDOFF + 1.6            # Top of mounted PCBs
Z_SERVO_PILLAR= Z_FLOOR + 70.0              # Top of servo pillar

# Build the master assembly
asm = cq.Assembly(name="Five_DOF_Robotic_Arm_Complete")

# ─────────────────────────────────────────────────────────────
# STRUCTURAL PARTS — Blue/Black alternating scheme
# ─────────────────────────────────────────────────────────────

# 1. Base Enclosure (BLACK)
asm.add(base_solid, name="Base_Enclosure", color=BLACK)

# 2. Shoulder Yoke + Turntable (BLUE)
asm.add(yoke_solid, name="Shoulder_Yoke_Turntable",
        loc=cq.Location(cq.Vector(0, 0, Z_ROOF)),
        color=BLUE)

# 3. Upper Arm / Link 1 (BLACK)
asm.add(upper_arm_solid, name="Upper_Arm_Link1",
        loc=cq.Location(cq.Vector(0, 0, Z_PIVOT)),
        color=BLACK)

# 4. Forearm / Link 2 (BLUE)
asm.add(forearm_solid, name="Forearm_Link2",
        loc=cq.Location(cq.Vector(0, 0, Z_ELBOW)),
        color=BLUE)

# 5. Wrist / Link 3 (BLACK)
asm.add(wrist_solid, name="Wrist_Link3",
        loc=cq.Location(cq.Vector(0, 0, Z_WRIST)),
        color=BLACK)

# 6. Gripper Base (BLUE)
asm.add(grip_base_solid, name="Gripper_Base",
        loc=cq.Location(cq.Vector(0, 0, Z_WRIST)),
        color=BLUE)

# 7. Left Finger (BLACK)
left_loc = (cq.Location(cq.Vector(-12.5, 21.7, Z_GRIP_PIVOT))
            * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 25.0))
asm.add(grip_left_solid, name="Left_Finger", loc=left_loc, color=BLACK)

# 8. Right Finger (BLACK)
right_loc = (cq.Location(cq.Vector(12.5, 21.7, Z_GRIP_PIVOT))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -25.0))
asm.add(grip_right_solid, name="Right_Finger", loc=right_loc, color=BLACK)

# ─────────────────────────────────────────────────────────────
# SERVOS
# ─────────────────────────────────────────────────────────────

# Yaw Servo (RDS5160) — inside base pillar, spline points up
asm.add(rds5160, name="Servo_Yaw_RDS5160",
        loc=cq.Location(cq.Vector(0, 0, Z_FLOOR + 35.0)),
        color=SERVO_BLACK)

# Shoulder Servo (RDS5160) — in left upright of yoke, oriented along X
shoulder_servo_loc = (cq.Location(cq.Vector(-42.5, 0, Z_PIVOT + Z_ROOF))
                      * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0))
asm.add(rds5160_shoulder, name="Servo_Shoulder_RDS5160",
        loc=shoulder_servo_loc, color=SERVO_BLACK)

# Elbow Servo (MG996R) — in distal end of upper arm
elbow_servo_loc = (cq.Location(cq.Vector(0, 0, Z_ELBOW))
                   * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0))
asm.add(mg996r_elbow, name="Servo_Elbow_MG996R",
        loc=elbow_servo_loc, color=SERVO_BLACK)

# Wrist Servo (MG996R) — in distal end of forearm
wrist_servo_loc = (cq.Location(cq.Vector(0, 0, Z_WRIST))
                   * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0))
asm.add(mg996r_wrist, name="Servo_Wrist_MG996R",
        loc=wrist_servo_loc, color=SERVO_BLACK)

# Gripper Servo (MG996R) — horizontal inside gripper base
grip_servo_loc = cq.Location(cq.Vector(-12.5, 0, Z_WRIST + 95.0))
asm.add(mg996r_gripper, name="Servo_Gripper_MG996R",
        loc=grip_servo_loc, color=SERVO_BLACK)

# ─────────────────────────────────────────────────────────────
# BEARINGS
# ─────────────────────────────────────────────────────────────

# 6812ZZ in base roof bearing pocket
asm.add(bearing_6812, name="Bearing_6812ZZ_Yaw",
        loc=cq.Location(cq.Vector(0, 0, Z_ROOF - 9.5)),
        color=CHROME)

# 608ZZ in shoulder passive pivot (right upright of yoke)
asm.add(bearing_608_shoulder, name="Bearing_608ZZ_Shoulder",
        loc=cq.Location(cq.Vector(32.5, 0, Z_PIVOT + Z_ROOF - 3.5)),
        color=CHROME)

# 608ZZ at elbow (right side of forearm clevis)
asm.add(bearing_608_elbow, name="Bearing_608ZZ_Elbow",
        loc=cq.Location(cq.Vector(28.5, 0, Z_ELBOW - 3.5)),
        color=CHROME)

# 608ZZ at wrist
asm.add(bearing_608_wrist, name="Bearing_608ZZ_Wrist",
        loc=cq.Location(cq.Vector(22.0, 0, Z_WRIST - 3.5)),
        color=CHROME)

# ─────────────────────────────────────────────────────────────
# SERVO HORNS (at each driven joint)
# ─────────────────────────────────────────────────────────────
horn_color = SERVO_ALU

# Shoulder horn (on upper arm proximal face)
asm.add(servo_horn, name="Horn_Shoulder",
        loc=(cq.Location(cq.Vector(-27.5, 0, Z_PIVOT + Z_ROOF))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=horn_color)

# Elbow horn (on forearm clevis)
horn_elbow = create_servo_horn_round()
asm.add(horn_elbow, name="Horn_Elbow",
        loc=(cq.Location(cq.Vector(-28.5, 0, Z_ELBOW))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=horn_color)

# Wrist horn
horn_wrist = create_servo_horn_round()
asm.add(horn_wrist, name="Horn_Wrist",
        loc=(cq.Location(cq.Vector(-22.0, 0, Z_WRIST))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=horn_color)

# ─────────────────────────────────────────────────────────────
# ELECTRONICS — Inside base enclosure
# ─────────────────────────────────────────────────────────────

# ESP32 NodeMCU (Right side of base, at standoff positions)
asm.add(esp32_full, name="ESP32_NodeMCU",
        loc=cq.Location(cq.Vector(64.0, 0, Z_STANDOFF + 0.8)),
        color=ESP_CHARCOAL)

# PCA9685 PWM Driver (Rear of base)
asm.add(pca9685, name="PCA9685_PWM_Driver",
        loc=cq.Location(cq.Vector(0, -55.0, Z_STANDOFF + 0.8)),
        color=PURPLE_PCB)

# XL4016 Buck Converter (Left side of base)
asm.add(xl4016_mod, name="XL4016_Buck_Converter",
        loc=cq.Location(cq.Vector(-55.0, 0, Z_STANDOFF + 0.8)),
        color=RED_PCB)

# LM2596 Buck Converter (Front of base)
asm.add(lm2596_mod, name="LM2596_Buck_Converter",
        loc=cq.Location(cq.Vector(0, 52.0, Z_STANDOFF + 0.8)),
        color=BLUE_PCB)

# 3S LiPo Battery (Rear bay)
lipo_center_y = -130.0 + 4.0 + 20.5
asm.add(lipo_full, name="LiPo_3S_Battery",
        loc=cq.Location(cq.Vector(0, lipo_center_y, Z_FLOOR + 13.0)),
        color=LIPO_BLACK)

# Screw Terminals (on XL4016 and near battery)
for i, (x, y) in enumerate([(-55.0, 30.0), (-55.0, -30.0), (30.0, -55.0)]):
    t = create_screw_terminal_2pin()
    asm.add(t, name=f"Screw_Terminal_{i+1}",
            loc=cq.Location(cq.Vector(x, y, Z_PCB_TOP + 5.0)),
            color=GREEN_TERM)

# Capacitors
asm.add(cap_1000uf, name="Cap_1000uF",
        loc=cq.Location(cq.Vector(-30.0, 30.0, Z_PCB_TOP)),
        color=CAP_BLACK)

asm.add(cap_470uf, name="Cap_470uF",
        loc=cq.Location(cq.Vector(30.0, 40.0, Z_PCB_TOP)),
        color=CAP_BLACK)

# ─────────────────────────────────────────────────────────────
# FASTENERS — Placed at every joint and mounting point
# ─────────────────────────────────────────────────────────────

# --- M8 Shoulder Pivot Bolt (through right upright → 608ZZ → upper arm) ---
asm.add(m8x30, name="M8_Bolt_Shoulder_Pivot",
        loc=(cq.Location(cq.Vector(42.5, 0, Z_PIVOT + Z_ROOF))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -90.0)),
        color=STEEL)

asm.add(m8_nut_part, name="M8_Nut_Shoulder_Pivot",
        loc=(cq.Location(cq.Vector(-30.0, 0, Z_PIVOT + Z_ROOF))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=STEEL)

# --- M8 Elbow Pivot Bolt ---
m8_elbow = m8_hex_bolt(30.0)
asm.add(m8_elbow, name="M8_Bolt_Elbow_Pivot",
        loc=(cq.Location(cq.Vector(36.5, 0, Z_ELBOW))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -90.0)),
        color=STEEL)

m8_elbow_nut = m8_hex_nut()
asm.add(m8_elbow_nut, name="M8_Nut_Elbow_Pivot",
        loc=(cq.Location(cq.Vector(-30.0, 0, Z_ELBOW))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=STEEL)

# --- M8 Wrist Pivot Bolt ---
m8_wrist = m8_hex_bolt(25.0)
asm.add(m8_wrist, name="M8_Bolt_Wrist_Pivot",
        loc=(cq.Location(cq.Vector(27.0, 0, Z_WRIST))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -90.0)),
        color=STEEL)

m8_wrist_nut = m8_hex_nut()
asm.add(m8_wrist_nut, name="M8_Nut_Wrist_Pivot",
        loc=(cq.Location(cq.Vector(-25.0, 0, Z_WRIST))
             * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
        color=STEEL)

# --- M3 Turntable-to-Yoke mounting screws (4×) ---
yoke_mount_pts = [(35.0, 25.0), (-35.0, 25.0), (35.0, -25.0), (-35.0, -25.0)]
for i, (x, y) in enumerate(yoke_mount_pts):
    screw = m3_socket_head_cap_screw(16.0)
    asm.add(screw, name=f"M3_Screw_TurntableYoke_{i+1}",
            loc=cq.Location(cq.Vector(x, y, Z_ROOF + 8.0 + 3.0)),
            color=STEEL)
    nut = m3_hex_nut()
    asm.add(nut, name=f"M3_Nut_TurntableYoke_{i+1}",
            loc=cq.Location(cq.Vector(x, y, Z_ROOF - 2.0)),
            color=STEEL)

# --- M3 Servo Horn mounting screws (4× per horn at shoulder, elbow, wrist) ---
horn_bolt_positions = [
    (7.0 * 0.707, 7.0 * 0.707),
    (-7.0 * 0.707, 7.0 * 0.707),
    (7.0 * 0.707, -7.0 * 0.707),
    (-7.0 * 0.707, -7.0 * 0.707),
]

joint_data = [
    ("Shoulder", -27.5, Z_PIVOT + Z_ROOF),
    ("Elbow", -28.5, Z_ELBOW),
    ("Wrist", -22.0, Z_WRIST),
]
for joint_name, x_off, z_off in joint_data:
    for j, (dy, dz) in enumerate(horn_bolt_positions):
        s = m3_socket_head_cap_screw(10.0)
        asm.add(s, name=f"M3_Horn_{joint_name}_{j+1}",
                loc=(cq.Location(cq.Vector(x_off - 3.0, dy, z_off + dz))
                     * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
                color=STEEL)

# --- M3 Servo Flange screws (4× per servo body for shoulder, elbow, wrist) ---
servo_flange_data = [
    ("Shoulder_Flange", -42.5, Z_PIVOT + Z_ROOF, [(37.0, 5.0), (-37.0, 5.0), (37.0, -5.0), (-37.0, -5.0)]),
    ("Elbow_Flange", 0, Z_ELBOW, [(24.0, 5.0), (-24.0, 5.0), (24.0, -5.0), (-24.0, -5.0)]),
]
for name, base_x, base_z, pts in servo_flange_data:
    for j, (dy, dz) in enumerate(pts):
        s = m3_socket_head_cap_screw(10.0)
        asm.add(s, name=f"M3_{name}_{j+1}",
                loc=(cq.Location(cq.Vector(base_x, dy, base_z + dz))
                     * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90.0)),
                color=STEEL)

# --- M4 Gripper pivot bolt ---
asm.add(m4x16, name="M4_Bolt_Gripper_Pivot",
        loc=cq.Location(cq.Vector(12.5, 21.7 + 5.0, Z_GRIP_PIVOT)),
        color=STEEL)

# --- Rubber feet (4× on base bottom) ---
foot_positions = [(60.0, 60.0), (-60.0, 60.0), (60.0, -90.0), (-60.0, -90.0)]
for i, (x, y) in enumerate(foot_positions):
    foot = create_rubber_foot()
    asm.add(foot, name=f"Rubber_Foot_{i+1}",
            loc=cq.Location(cq.Vector(x, y, -3.0)),
            color=RUBBER_BLACK)

# ==============================================================================
# EXPORT FINAL ASSEMBLY
# ==============================================================================
print("\n[6/6] Exporting final master assembly STEP...")
assembly_path = os.path.join(ASSEMBLY_DIR, "five_dof_arm_complete_assembly.step")
asm.save(assembly_path)

# ==============================================================================
# SUMMARY
# ==============================================================================
# Count files
n_parts = len([f for f in os.listdir(PARTS_DIR) if f.endswith('.step')])
n_components = len([f for f in os.listdir(COMPONENTS_DIR) if f.endswith('.step')])
n_fasteners = len([f for f in os.listdir(FASTENERS_DIR) if f.endswith('.step')])

print("\n" + "=" * 70)
print("  EXPORT COMPLETE")
print("=" * 70)
print(f"  Output: {EXPORT_ROOT}")
print(f"  ├── parts/       ({n_parts} structural STEP files)")
print(f"  ├── components/  ({n_components} electronic/mechanical STEP files)")
print(f"  ├── fasteners/   ({n_fasteners} fastener STEP files)")
print(f"  └── assembly/    (1 master assembly STEP)")
print(f"\n  Master Assembly: {assembly_path}")
print(f"  Total individual exports: {n_parts + n_components + n_fasteners + 1}")
print("=" * 70)
