import os
import sys
import FreeCAD
import Part

def analyze_file(filepath):
    print("=" * 70)
    print("FILE:", os.path.basename(filepath))
    print("Path:", filepath)
    print(f"Size: {os.path.getsize(filepath):,} bytes")
    try:
        shape = Part.Shape()
        shape.read(filepath)
        bb = shape.BoundBox
        solids = shape.Solids
        faces = len(shape.Faces)
        edges = len(shape.Edges)
        vol = shape.Volume
        cog = shape.CenterOfGravity
        print(f"Topology: {len(solids)} Solids, {faces} Faces, {edges} Edges")
        print(f"Bounding Box: X=[{bb.XMin:.2f}, {bb.XMax:.2f}] (len={bb.XLength:.2f}mm), Y=[{bb.YMin:.2f}, {bb.YMax:.2f}] (len={bb.YLength:.2f}mm), Z=[{bb.ZMin:.2f}, {bb.ZMax:.2f}] (len={bb.ZLength:.2f}mm)")
        print(f"Volume: {vol:,.2f} mm^3")
        print(f"Center of Gravity: ({cog.x:.2f}, {cog.y:.2f}, {cog.z:.2f})")
        if len(solids) > 1:
            print(f"Sub-solids count: {len(solids)}")
            for idx, s in enumerate(solids[:10]):
                s_bb = s.BoundBox
                print(f"  Solid #{idx+1}: Vol={s.Volume:,.1f} mm^3, BoundingBox: [{s_bb.XLength:.1f} x {s_bb.YLength:.1f} x {s_bb.ZLength:.1f}]")
    except Exception as e:
        print("Error reading shape:", e)

print(">>> CHIMERA A1 5-DOF ROBOT ARM ANALYSIS <<<")
chimera_dir = "/home/jeremiah/ros2_ws/CHIMERA A1 5-DOF ROBOT ARM"
for fname in sorted(os.listdir(chimera_dir)):
    if fname.lower().endswith((".step", ".stp")):
        analyze_file(os.path.join(chimera_dir, fname))

print("\n>>> E.R.A 5-DOF ROBOT ARM ANALYSIS <<<")
era_dir = "/home/jeremiah/ros2_ws/E.R.A 5-DOF ROBOT ARM/ERA Robotic Arm - 5965119/files"
for fname in sorted(os.listdir(era_dir)):
    if fname.lower().endswith((".step", ".stp")):
        analyze_file(os.path.join(era_dir, fname))

sys.exit(0)
