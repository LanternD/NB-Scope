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
- moulde benchmark extension board
- PWR_KEY addon

## EDA Environment

The software to open the projects is [KiCad](https://kicad-pcb.org/). 

PLEASE use the **Nightly-build** version of KiCad because the projects are created by that. The projects are not backward compatible.

## To be added later
