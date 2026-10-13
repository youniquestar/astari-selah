# 3D Mechanical CAD & Modeling Subsystem

This directory contains all physical CAD assemblies, structural components, fasteners, COTS electronics STEP files, and CadQuery / FreeCAD generation scripts for the 5-DOF robotic manipulator.

## Folder Overview
```
cad/
├── assembly/
│   ├── astari_selah_master.FCStd           # Native FreeCAD modular parametric master assembly
│   ├── five_dof_arm_complete_assembly.step # Full master assembly with 50+ components
│   └── freecad_5dof.FCStd                  # FreeCAD legacy assembly project
├── parts/
│   ├── *.step                              # Solid models of all 8 3D printed parts
│   └── *.stl                               # Slice-ready 3D printing meshes
├── components/
│   └── *.step                              # COTS hardware (ESP32, PCA9685, RDS5160, MG996R, bearings, LiPo)
├── fasteners/
│   └── *.step                              # Standard ISO/DIN fasteners (M3, M4, M8 screws, bolts, nuts)
├── scripts/
│   ├── generate_final_3d_model.py          # Master CadQuery generator script
│   └── ...                                 # Individual link generators
└── manufacturing/
    └── MANUFACTURING_GUIDE.md              # Slicing parameters, materials, and tolerances
```
