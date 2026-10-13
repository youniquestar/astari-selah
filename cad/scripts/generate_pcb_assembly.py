import cadquery as cq
import os

# ==============================================================================
# 1. PARAMETRIC DIMENSIONS & CLEARANCES (Units: mm)
# ==============================================================================
# PCB Base
PCB_LENGTH = 100.0
PCB_WIDTH = 80.0
PCB_THICKNESS = 1.6
M3_HOLE_DIA = 3.2
HOLE_OFFSET = 4.0

# Components (Mockups for spatial verification)
ESP32_L = 52.0
ESP32_W = 28.0
ESP32_H = 6.0

XL4016_L = 61.0
XL4016_W = 50.0
XL4016_H = 25.0 # Max height with heatsinks

LM2596_L = 43.0
LM2596_W = 21.0
LM2596_H = 14.0

TERMINAL_BLOCK_L = 10.0
TERMINAL_BLOCK_W = 8.0
TERMINAL_BLOCK_H = 10.0

# ==============================================================================
# 2. GENERATE PCB SUBSTRATE
# ==============================================================================
# Create the FR4 Board
pcb_board = (
    cq.Workplane("XY")
    .box(PCB_LENGTH, PCB_WIDTH, PCB_THICKNESS)
)

# Add 4x M3 mounting holes at corners
mount_pts = [
    ( PCB_LENGTH/2 - HOLE_OFFSET,  PCB_WIDTH/2 - HOLE_OFFSET),
    (-PCB_LENGTH/2 + HOLE_OFFSET,  PCB_WIDTH/2 - HOLE_OFFSET),
    ( PCB_LENGTH/2 - HOLE_OFFSET, -PCB_WIDTH/2 + HOLE_OFFSET),
    (-PCB_LENGTH/2 + HOLE_OFFSET, -PCB_WIDTH/2 + HOLE_OFFSET),
]

pcb_board = (
    pcb_board.faces(">Z")
    .workplane()
    .pushPoints(mount_pts)
    .hole(M3_HOLE_DIA)
)

# Apply 2.0mm fillets to corners for handling
pcb_board = pcb_board.edges("|Z").fillet(2.0)

# ==============================================================================
# 3. GENERATE COMPONENT MOCKUPS
# ==============================================================================
# A. ESP32 NodeMCU
esp32_mock = cq.Workplane("XY").box(ESP32_W, ESP32_L, ESP32_H)
# Add gold antenna trace block for visual reference
antenna = cq.Workplane("XY").box(ESP32_W, 7.0, 1.0).translate((0, ESP32_L/2 - 3.5, ESP32_H/2 + 0.5))
esp32_mock = esp32_mock.union(antenna)

# B. XL4016 Buck Converter Zone
xl4016_mock = cq.Workplane("XY").box(XL4016_W, XL4016_L, XL4016_H)

# C. LM2596 Buck Converter Zone
lm2596_mock = cq.Workplane("XY").box(LM2596_W, LM2596_L, LM2596_H)

# D. Power Terminal Block (3-Pin)
terminal_mock = cq.Workplane("XY").box(TERMINAL_BLOCK_W * 1.5, TERMINAL_BLOCK_L, TERMINAL_BLOCK_H)

# ==============================================================================
# 4. ASSEMBLE THE PCB
# ==============================================================================
# Initialize Assembly
pcb_assembly = cq.Assembly(name="Main_Carrier_PCB")

# Base Board (Green FR4)
pcb_assembly.add(
    pcb_board, 
    name="FR4_Board", 
    color=cq.Color(0.1, 0.5, 0.2) # Dark Green
)

# Place ESP32 (Center Right)
pcb_assembly.add(
    esp32_mock, 
    name="ESP32_NodeMCU", 
    loc=cq.Location(cq.Vector(PCB_LENGTH/4, 0, PCB_THICKNESS/2 + ESP32_H/2)),
    color=cq.Color(0.2, 0.2, 0.2) # Charcoal
)

# Place XL4016 Carrier (Left Side)
pcb_assembly.add(
    xl4016_mock, 
    name="XL4016_High_Power", 
    loc=cq.Location(cq.Vector(-PCB_LENGTH/4 - 5, 0, PCB_THICKNESS/2 + XL4016_H/2)),
    color=cq.Color(0.7, 0.2, 0.2) # Dark Red Board
)

# Place LM2596 Carrier (Top Right)
pcb_assembly.add(
    lm2596_mock, 
    name="LM2596_Logic_Power", 
    loc=cq.Location(cq.Vector(PCB_LENGTH/4 + 5, PCB_WIDTH/2 - 15, PCB_THICKNESS/2 + LM2596_H/2)),
    color=cq.Color(0.2, 0.4, 0.8) # Blue Board
)

# Place Battery / Main Power Terminals (Bottom Center)
pcb_assembly.add(
    terminal_mock, 
    name="LiPo_Terminals", 
    loc=cq.Location(cq.Vector(0, -PCB_WIDTH/2 + 10, PCB_THICKNESS/2 + TERMINAL_BLOCK_H/2)),
    color=cq.Color(0.1, 0.8, 0.1) # Bright Green Plastic
)

# ==============================================================================
# 5. EXPORT OUTPUTS
# ==============================================================================
if __name__ == "__main__":
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    os.makedirs(export_dir, exist_ok=True)

    # Export full multi-body assembly with colors to STEP
    step_path = os.path.join(export_dir, "custom_carrier_pcb.step")
    pcb_assembly.save(step_path)
    
    # Export just the bare PCB board to STL (if 3D printing a test fit dummy)
    stl_path = os.path.join(export_dir, "custom_carrier_pcb_bare.stl")
    cq.exporters.export(pcb_board, stl_path)
    
    # Export individual components to STEP
    cq.exporters.export(esp32_mock, os.path.join(export_dir, "esp32.step"))
    cq.exporters.export(xl4016_mock, os.path.join(export_dir, "xl4016_pwm_driver.step"))
    cq.exporters.export(lm2596_mock, os.path.join(export_dir, "lm2596.step"))
    cq.exporters.export(terminal_mock, os.path.join(export_dir, "terminals.step"))

    print(f"[CAD Export] Successfully generated:")
    print(f" - Assembly STEP: {step_path}")
    print(f" - Bare Board STL: {stl_path}")
    print(" - Individual component STEP files generated.")