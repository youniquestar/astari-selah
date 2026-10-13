import cadquery as cq
import os

def assemble_arm():
    export_dir = os.path.expanduser("~/ros2_ws/src/five_dof_arm_description/cad_export")
    asm_dir = os.path.join(export_dir, "base_enclosure_fused_assembly")
    grp_dir = os.path.join(export_dir, "gripper_assembly")

    print("Importing STEP files...")
    # 1. Load STEP files
    base = cq.importers.importStep(os.path.join(asm_dir, "base_enclosure_fused.step"))
    yoke = cq.importers.importStep(os.path.join(asm_dir, "complete_shoulder_yoke_axis.step"))
    upper_arm = cq.importers.importStep(os.path.join(asm_dir, "link_1_upper_arm.step"))
    forearm = cq.importers.importStep(os.path.join(asm_dir, "link_2_forearm.step"))
    wrist = cq.importers.importStep(os.path.join(asm_dir, "link_3_wrist_assembly.step"))
    gripper_base = cq.importers.importStep(os.path.join(grp_dir, "gripper_base.step"))
    left_finger = cq.importers.importStep(os.path.join(grp_dir, "gripper_left_finger.step"))
    right_finger = cq.importers.importStep(os.path.join(grp_dir, "gripper_right_finger.step"))

    # 2. Define global positions
    # Arm stands completely straight up along Z axis.
    Z_BASE = 0.0
    Z_YOKE = Z_BASE + 85.0
    Z_SHOULDER = Z_YOKE + (8.0 + 55.0) # 63.0 local (8mm turntable plate + 55mm pivot height)
    Z_ELBOW = Z_SHOULDER + 220.0
    Z_WRIST = Z_ELBOW + 180.0

    print("Building Assembly Hierarchy...")
    # 3. Create Assembly
    arm_asm = cq.Assembly(name="FiveDOFArm")

    # Add Base
    arm_asm.add(base, name="Base")

    # Add Yoke
    arm_asm.add(yoke, name="Yoke", loc=cq.Location(cq.Vector(0, 0, Z_YOKE)))

    # Add Upper Arm
    arm_asm.add(upper_arm, name="UpperArm", loc=cq.Location(cq.Vector(0, 0, Z_SHOULDER)))

    # Add Forearm
    arm_asm.add(forearm, name="Forearm", loc=cq.Location(cq.Vector(0, 0, Z_ELBOW)))

    # Add Wrist
    arm_asm.add(wrist, name="Wrist", loc=cq.Location(cq.Vector(0, 0, Z_WRIST)))

    # Add Gripper Base
    arm_asm.add(gripper_base, name="GripperBase", loc=cq.Location(cq.Vector(0, 0, Z_WRIST)))

    # Add Fingers
    # Fingers are placed relative to Gripper Base. Gripper Base is at Z_WRIST.
    left_finger_loc = cq.Location(cq.Vector(-12.5, 21.7, Z_WRIST + 105.5))
    right_finger_loc = cq.Location(cq.Vector(12.5, 21.7, Z_WRIST + 105.5))

    # Open the fingers slightly to 25 degrees for a nice visual pose
    left_loc_open = left_finger_loc * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), 25.0)
    right_loc_open = right_finger_loc * cq.Location(cq.Vector(0,0,0), cq.Vector(0,1,0), -25.0)

    arm_asm.add(left_finger, name="LeftFinger", loc=left_loc_open)
    arm_asm.add(right_finger, name="RightFinger", loc=right_loc_open)

    # Export Full Assembly
    out_step = os.path.join(export_dir, "full_arm_assembly.step")
    print("Exporting to STEP (this may take a few seconds)...")
    arm_asm.save(out_step)
    print(f"Exported {out_step}")

if __name__ == "__main__":
    assemble_arm()
