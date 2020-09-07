# Introduction

Node mainboard is responsible for hosting the module shieldboard, sensing the environment, collecting debug log and current traces, and so on.

Major components on the board: 

- STM32F103 as the main processor
- LM3671-3.3 as input but converter
- CM1624 as micro SD card protector
- CAT24C128 as non-volatile memory
- TXB0108 as logic level converter (3.3v <-> 1.8v)
- Si7021 as temperature and relative humidity sensor
- INA219 as current sensor

It is powered by one or two 18650 batteries. It also supports USB 5V as the input voltage, using jumper cap to switch.

# Known Issues

If you use the generic ST-Link V2 dongle as programmer, do not use it to power the board alone, otherwise the LM3671 buck converter chip will burn. 

**Correct way**: Power on the board using 18650 battery or 5V USB, then plug on the ST-Link debugger. After you finish programming/debugging, unplug ST-Link V2 FIRST, and then shutdown the board power.

# Suggestions in Mainboard Hardware Design

The latest version of mainboard generally works well, but I have several important suggestions for future design. 

1. Upgrade the power chip. LM3671 supports a maximum current of 600 mA, which sometimes has little margin for some NB-IoT modules. So I suggest using other power IC, such as LM3281 or TPS62160.
2. 

# Change log

## Ver 3.2


# Gallery

## Ver 3.2
