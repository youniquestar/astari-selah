import cadquery as cq
import os
import shutil

def assemble_arm():
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    asm_dir = os.path.join(export_dir, "base_enclosure_fused_assembly")
    grp_dir = os.path.join(export_dir, "gripper_assembly")
    final_dir = os.path.join(export_dir, "final_3D_model")

    os.makedirs(final_dir, exist_ok=True)

    print("Importing STEP files...")
    # Load STEP files
    base = cq.importers.importStep(os.path.join(asm_dir, "base_enclosure_fused.step"))
    yoke = cq.importers.importStep(os.path.join(asm_dir, "complete_shoulder_yoke_axis.step"))
    upper_arm = cq.importers.importStep(os.path.join(asm_dir, "link_1_upper_arm.step"))
    forearm = cq.importers.importStep(os.path.join(asm_dir, "link_2_forearm.step"))
    wrist = cq.importers.importStep(os.path.join(asm_dir, "link_3_wrist_assembly.step"))
    gripper_base = cq.importers.importStep(os.path.join(grp_dir, "gripper_base.step"))
    left_finger = cq.importers.importStep(os.path.join(grp_dir, "gripper_left_finger.step"))
    right_finger = cq.importers.importStep(os.path.join(grp_dir, "gripper_right_finger.step"))
    pcb = cq.importers.importStep(os.path.join(export_dir, "custom_carrier_pcb.step"))

    # Define global positions
    Z_BASE = 0.0
    Z_YOKE = Z_BASE + 85.0
    Z_SHOULDER = Z_YOKE + (8.0 + 55.0) 
    Z_ELBOW = Z_SHOULDER + 220.0
    Z_WRIST = Z_ELBOW + 180.0

    print("Building Assembly Hierarchy with Colors...")
    # Create Assembly
    arm_asm = cq.Assembly(name="FinalFiveDOFArm")

    # Blue and Black Theme
    blue_color = cq.Color(0.0, 0.2, 0.8) # Deep Blue
    black_color = cq.Color(0.1, 0.1, 0.1) # Black/Dark Gray

    # Add Base
    arm_asm.add(base, name="Base", color=black_color)

    # Add Yoke
    arm_asm.add(yoke, name="Yoke", loc=cq.Location(cq.Vector(0, 0, Z_YOKE)), color=blue_color)

    # Add Upper Arm
    arm_asm.add(upper_arm, name="UpperArm", loc=cq.Location(cq.Vector(0, 0, Z_SHOULDER)), color=black_color)

    # Add Forearm
    arm_asm.add(forearm, name="Forearm", loc=cq.Location(cq.Vector(0, 0, Z_ELBOW)), color=blue_color)

    # Add Wrist
    arm_asm.add(wrist, name="Wrist", loc=cq.Location(cq.Vector(0, 0, Z_WRIST)), color=black_color)

    # Add Gripper Base
    arm_asm.add(gripper_base, name="GripperBase", loc=cq.Location(cq.Vector(0, 0, Z_WRIST)), color=blue_color)

    # Add Fingers
    left_finger_loc = cq.Location(cq.Vector(-12.5, 21.7, Z_WRIST + 105.5))
    right_finger_loc = cq.Location(cq.Vector(12.5, 21.7, Z_WRIST + 105.5))

    left_loc_open = left_finger_loc * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 25.0)
    right_loc_open = right_finger_loc * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -25.0)

    arm_asm.add(left_finger, name="LeftFinger", loc=left_loc_open, color=black_color)
    arm_asm.add(right_finger, name="RightFinger", loc=right_loc_open, color=black_color)

    # Add PCB to Base (Mocking placement on the side or top of base)
    pcb_loc = cq.Location(cq.Vector(60, 0, 40)) * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90)
    arm_asm.add(pcb, name="Main_Carrier_PCB", loc=pcb_loc) # PCB has its own colors from the step file

    # Generating basic fasteners (Mocking some screws at joints)
    screw = cq.Workplane("XY").cylinder(height=10, radius=2).union(cq.Workplane("XY").workplane(offset=5).cylinder(height=3, radius=3.5))
    
    # Adding mock screws to shoulder and elbow joints
    arm_asm.add(screw, name="Screw_Shoulder_Left", loc=cq.Location(cq.Vector(-35, 0, Z_SHOULDER)) * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90), color=cq.Color(0.8, 0.8, 0.8))
    arm_asm.add(screw, name="Screw_Shoulder_Right", loc=cq.Location(cq.Vector(35, 0, Z_SHOULDER)) * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -90), color=cq.Color(0.8, 0.8, 0.8))
    arm_asm.add(screw, name="Screw_Elbow_Left", loc=cq.Location(cq.Vector(-30, 0, Z_ELBOW)) * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 90), color=cq.Color(0.8, 0.8, 0.8))
    arm_asm.add(screw, name="Screw_Elbow_Right", loc=cq.Location(cq.Vector(30, 0, Z_ELBOW)) * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -90), color=cq.Color(0.8, 0.8, 0.8))

    # Export Full Assembly
    out_step = os.path.join(final_dir, "final_complete_arm_assembly.step")
    print("Exporting to STEP (this may take a few seconds)...")
    arm_asm.save(out_step)
    
    # Copy all individual step files to final folder as well, as requested: "Each part ... should be generated seperately and each component ... should also be generated seperately"
    # Actually, they are already generated, we just need to move/copy them to the final folder for easy access
    shutil.copy2(os.path.join(asm_dir, "base_enclosure_fused.step"), final_dir)
    shutil.copy2(os.path.join(asm_dir, "complete_shoulder_yoke_axis.step"), final_dir)
    shutil.copy2(os.path.join(asm_dir, "link_1_upper_arm.step"), final_dir)
    shutil.copy2(os.path.join(asm_dir, "link_2_forearm.step"), final_dir)
    shutil.copy2(os.path.join(asm_dir, "link_3_wrist_assembly.step"), final_dir)
    shutil.copy2(os.path.join(grp_dir, "gripper_base.step"), final_dir)
    shutil.copy2(os.path.join(grp_dir, "gripper_left_finger.step"), final_dir)
    shutil.copy2(os.path.join(grp_dir, "gripper_right_finger.step"), final_dir)
    shutil.copy2(os.path.join(export_dir, "custom_carrier_pcb.step"), final_dir)
    shutil.copy2(os.path.join(export_dir, "esp32.step"), final_dir)
    shutil.copy2(os.path.join(export_dir, "xl4016_pwm_driver.step"), final_dir)
    shutil.copy2(os.path.join(export_dir, "lm2596.step"), final_dir)
    shutil.copy2(os.path.join(export_dir, "terminals.step"), final_dir)

    print(f"Exported Final Assembly and copied individual components to {final_dir}")

if __name__ == "__main__":
    assemble_arm()
