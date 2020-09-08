# Introduction

Node mainboard is responsible for hosting the module shieldboard, sensing the environment, collecting debug log and current traces, and so on.

Major components on the board: 

- STM32F103 as the main processor
- LM3671-3.3 as DC-DC converter
- CM1624 as micro SD card protector
- CAT24C128 as non-volatile memory
- TXB0108 as logic level converter (3.3v <-> 1.8v)
- Si7021 as temperature and relative humidity sensor
- INA226 as current sensor

It is powered by one or two 18650 batteries. It also supports USB 5V as the input voltage, using jumper cap to switch.

# Important Notes

## Components

- Pin headers. For the two rows hosting the NB-IoT UE shieldboard and the power jumpper, please use 1.27 mm pitch connectors. For all the other 1.27 mm throughhole connectors with 3-6 pins, use 1.25 mm pitch connectors. Please take a look at the photo of Ver 3.1 below. Please find the datasheet in "[Hardware/Materials](../Materials/A1251.pdf)" folder. Male connector: A1251H-XP; Female connector: A1251WV-XP. Note: this is just an example. You don't need to use the exact component.
- The 1.25mm pitch connectors could be converted to 2.54 mm pitch pins to connect to other components, such as ST-Link programmer.
- USB connector. There are many similar USB connectors available, please take a look at their size and shape and ensure they match. "Molex-105017-0001" would work but it is expensive. 
- Battery holder. One thing that is not shown in the picture is the battery holder, whose model is "BK-18650-PC4". You need to solder this **after everything else**, because the battery holder will block the access to whole bottom layer.

## NB-IoT UE Pin Assignment

The pin assignment should be taken care for future module shieldboard design.

![Module Pin Assignment](../../../assets/module_board_pin_assignment.png)

Note: the labels starting with `M_` means the pins are treated as part of the module. For example, `M_MAIN_UART_TX` means the UART Tx of the module, which should be connected to the MCU UART Rx pin accordingly.

`Left_Conn` means the upper row in the picture below, `Right_conn` is the bottom row accordingly.

The module ground GNDs are aggregated to 4 pins on the `Right_conn`, which passes through a current sampling resistor on the mainboard.

# Known Issues

- If you use the generic ST-Link V2 dongle as programmer, do not use it to power the board alone, otherwise the LM3671 buck converter chip will burn. 

  **Correct way**: Power on the board using 18650 battery or 5V USB, then plug on the ST-Link debugger. After you finish programming/debugging, unplug ST-Link V2 FIRST, and then shutdown the board power.

- I didn't add the ESD protection to the board, so please ensure the ESD on the hand is largely removed before touching the board.

**Note**: Ver 3.1 and 3.0 have other minor issues, which were largely fixed in Ver 3.2. Please see the "Change Log" below. To save your time, do not use Ver 3.0 and 3.1.

- The "Module USB" can use as the 5V input of the board, while the "MCU USB" cannot do it. If you want to use the latter one to power the board, connect the "+5V" near it to the "+5V" near the "PWR SELECT" pin header.

# Suggestions in Mainboard Hardware Design

The latest version (ver 3.2) of mainboard generally works well, but I have several important suggestions for future design. 

1. Upgrade the power chip. LM3671 supports a maximum current of 600 mA, which sometimes has little margin for some NB-IoT modules. So I suggest using other power IC, such as LM3281 or TPS62160.
2. The STM32F103 does not have DMA channel for SD card writing, which means you cannot do anything else when writing the SD card. My suggestion is to use another STM32 chip. You need to double check in STM32 CubeMX whether the chip supports DMA channel in SDIO interface.
3. Add the ESD protection circuit.
4. Add a fuse to the power module.

# Gallery

## Ver 3.2

![Node Mainboard v3.2](../../../assets/node_base_v3.2.png)
![Node Mainboard v3.2](../../../assets/node_base_v3.2_B.png)

Note: the two shieldboard rows should be pin socket, instead of pin header. They are interchangeable though.

## Ver 3.1

![Node Mainboard v3.1](../../../assets/node_base_v3.1_actual.jpg)
![Node Mainboard v3.1](../../../assets/node_base_v3.1.png)
![Node Mainboard v3.1](../../../assets/node_base_v3.1_B.png)

## Ver 3.0

![Node Mainboard v3.0](../../../assets/node_base_v3.0.png)
![Node Mainboard v3.0](../../../assets/node_base_v3.0_B.png)

# Change Log

## Ver 3.2

- Added a DTC143Z to control the PWRKEY pin for uBlox SARA-R410M-02B and Quectel BG96, BC26, and BC66, such that we don't need the `pwr_key_add_on` modification board for these modules.
- Replaced the labels in schematic by another type (with an enclosure), which shows the direction of the signal.
- Added a power jumper to isolate the DC-DC module with other components on the board, for easier debugging.
- Used a smaller form factor transistor (DTC143Z) for LED control.
- Added a 1.5k pull-up resistor for USB connector.
- Removed the BOOT0 control header. Connected BOOT0 to GND by default. Added a pad for connecting to 3.3V by jumper wire temporarily. 
- Used a better matching footprint for all the buttons.
- Reduced the SWD connector from 6 pins to 4 pins.

## Ver 3.1

- Updated the power module. Replaced the large inductor to a smaller one. The power module layout was also improved.
- Replaced the resistor array in micro SD card protetion circuit with CM1624.
- Updated the layout of the user buttons.

## Ver 3.0

Actually the first version of NB-Scope mainboard. 
