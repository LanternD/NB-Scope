# Hardware Guideline

## Overview

This folder contains the NB-Scope nodes hardware designs. Specifically, we have a folder for the mainboard, a folder for all the shieldboard for NB-Scope, and a folder for the auxilliary boards.

### Mainboard

The mainboard has 3 versions. **Please use ver 3.2**. The outdated versions are for reference only. They may work but not very stable. Ver 1.0 and 2.0 are not for NB-Scope projects, thus are omitted.

### Shieldboards

We have 7 types of shieldboard designs, supporting up to 9 types of different NB-IoT modules, including:

- Quectel BC28
- Quectel BC35
- Quectel BC26
- Quectel BC66
- Quectel BC95 (Not tested)
- Quectel BG36 (Not tested)
- Quectel BG96
- Gosuncn ME3616
- uBlox SARA-R410M-02B

(Quectel BG36/BG96 and Quectel BC35/BC95, have the same pin assignment, respectively.)

The module PCB project names should be straight-forward in the "Shieldboards" folder.

### Auxilliary boards

- Current sensing calibration board
- Firmware upgrade extension board
- Moulde benchmark extension board
- PWR_KEY addon

### Libraries

If you encounter missing symbol/footprint problem when opening the schematic or PCB files, please import them in the `Libraries` folder. The missing libraries should be a subset of the available footprints.

## General Guideline

### EDA environment

The software to open the projects is [KiCad](https://kicad-pcb.org/) (Pronounced as "key-cad").

PLEASE use the **Nightly-build** version of KiCad because the projects are created by that. The projects are not backward compatible.

To open the 3D viewer, click "View->3D Viewer" (<kbd>⌥+3</kbd> on Mac or <kbd>Alt+3</kbd> on other operating systems) in the `Pcbnew` software menu.

### Project structure

- `<project_name>.pro`: project main file.
- `<project_name>.sch` or `<project_name>.kicad_sch`: project schematic design. If `.sch` and `.kicad_sch` co-exist, use the `.kicad_sch` one.
- `<project_name>.kicad_pcb`: project PCB design.
- `Exported Files` folder: exported/generated files from the projects, including Gerber files, bill of materials (BOM), positioning files (for SMT process), and other board 3D photos or documents. I suggest you double check the project schematic and pcb designs, then generate these fabrication files again by yourself, instead of sending the Gerber files to manufacturers directly.

There are some KiCad generated backup or middle files. I forget to remove them before committing. You may ignore or edit them. They have the following patterns:

- `fp-info-cache`
- `<project name>-cache.lib`
- `<project name>-rescue.dcm`
- `<project name>-rescue.lib`
- `<project name>.kicad_pcb-bak`
- `<project name>.sch-bak`
- `sys-lib-table`

## Click into their corresponding folders for more details

If you have any questions, please send me an email to "yangdeli at msu.edu".
