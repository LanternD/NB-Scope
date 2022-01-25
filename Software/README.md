# Introduction

This folder stores the software codes of the NB-Scope project. There are 3 major parts:

- Embedded system (mainboard)
- Server logging
- Data processing

Note that the codebase is developed by different members of our group, so the code style may vary across different components.

**Most of the code is uploaded. Generally, the content in this `Software` folder will not be updated in the future, unless there is major components missing.**

# Embedded Code

In the "field-test-control" folder.

There are many components in this code. I could not explain all the details in it, so I just have a basic summary here.

- Current sensing
- SD card R/W
- EEPROM R/W
- Si7021 control (temperature and relative humidity sensing)
- SSD1306 I2C OLED screen control
- NB-IoT module control
- Field measurement pipeline. You can customize your own.

# Server-side Logging

In "udp-server-for-nb-iot" folder.

# Data Processing

In the "deplotment-data-analyzer" folder.



