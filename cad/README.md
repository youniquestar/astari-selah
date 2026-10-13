# 3D Mechanical CAD & Modeling Subsystem

This directory contains all physical CAD assemblies, structural components, fasteners, COTS electronics STEP files, and CadQuery / FreeCAD generation scripts for the 5-DOF robotic manipulator.

## Folder Overview
```
cad/
├── Selah/                              # Modular FreeCAD CAD subsystem with 'Selah' folder hierarchy
│   ├── assembly/Selah_Master.FCStd     # Master FreeCAD project with root 'Selah' group
│   ├── assembly/Selah_Assembly.step    # Master full assembly STEP solid
│   ├── parts/*.FCStd                   # Dedicated FreeCAD project for each individual part
│   ├── parts/*.step, *.stl             # Modular solid STEPs and slice-ready STLs
│   ├── components/*.step               # COTS actuators, bearings, and sensors
│   └── scripts/build_selah_cad.py      # Automated headless FreeCAD rebuild script
├── assembly/
│   ├── astari_selah_master.FCStd       # Native FreeCAD assembly
│   ├── five_dof_arm_complete_assembly.step # Full master assembly
│   └── freecad_5dof.FCStd              # Legacy assembly project
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
