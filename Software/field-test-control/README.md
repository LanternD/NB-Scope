# Field Test Control

Embedded code that runs on STM32F103RET6, hosting a bunch of peripherals. It performs the NB-IoT field measurement task.

Note: the "`fm_`" in the code means "field measurement".

# MCU Software version log

- 00001: 20200111. Code is ready for BC28/BC26/ME3616. Migrating to BG96.
- 00002:

# Design 

## MCU

- STM32F103RETx. 72MHz 512kB Flash, 64kB RAM.
- High speed external (HSE) crystal oscillator: 8MHz, cap: 10 pF.
- LSE crystal oscillator: 32.768kHz, cap: 10 pF, high quality ceramic cap.
- No pull-up resistor needed for **RESET**.
- I2C pull-up resistor = 4.7 kOhm.
- SDIO freq max: 48 MHz.

### Pin Connection

- TF (SDIO)

	39 PC8 <-> TF 7 SDIO_D0
	40 PC9 <-> TF 8 SDIO_D1
	51 PC10 <-> TF 1 SDIO_D2
	52 PC11 <-> TF 2 SDIO_D3
	53 PC12 <-> TF 5 SDIO_CLK
	54 PD2 <-> TF 3 SDIO_CMD

- SWD (MCU debug port)

	46 PA13 SWD_IO <-> SWD_IO
	49 PA14 SWD_CLK<-> SWD_CLK
	55 PB3 SWO <-> SWO

- Temperature & humidity sensor, EEPROM (share the same I2C)

  29 PB10 I2C2_SCL <-> Si7021 Sensor_SCL, EEPROM_SCL
  30 PB11 I2C2_SDA <-> Si7021 Sensor_SDA, EEPROM_SDA

- INA226 current sensor

  58 PB6 I2C1_SCL <-> INA226_SCL
  59 PB7 I2C1_SDA <-> INA226_SDA

- MCU USB

  44 PA11 USBDM <-> Connector USB DM
  45 PA12 USBDP <-> Connector USB DP

- Misc.

16 PA2 USART2_Tx <-> Module Main UART Rx
17 PA3 USART2_Rx <-> Module Main UART Tx
42 PA9 USART1_Tx <-> Module Debug UART Rx
43 PA10 USART1_Rx <-> Module Debug UART Tx

8 PC0 ADC123_IN10 <-> V_batt ADC

33 PB12 SPI2_NSS <-> Module SPI_CS
34 PB13 SPI2_SCK <-> Module SPI_CLK / I2S_CK
35 PB14 SPI2_MISO <-> Module SPI2_MISO
36 PB15 SPI2_MOSI <-> Module SPI2_MOSI

9 PC1 <-> GPIO_L1
10 PC2 <-> PSM_IND
11 PC3 <-> GPIO_L2
14 PA0 <-> GPIO_L3
15 PA1 <-> GPIO_L4
20 PA4 <-> Module PWRKEY
21 PA5 <-> Module RESET
22 PA6 <-> Module PSM external wakeup interruption
23 PA7 <-> AP_READY
50 PA15 <-> GPIO_R1
41 PA8 <-> GPIO_R2
38 PC7 <-> GPIO_R3
37 PC6 <-> Module RI

- Not used by module:

26 PB0 <-> SWITCH_1
27 PB1 <-> SWITCH_2
56 PB4 <-> TF_DETECT (Ext GPIO_1)
57 PB5 <-> Ext GPIO_2
61 PB8 <-> Ext GPIO_3
62 PB9 <-> Ext GPIO_4
24 PC4 <-> LED 0 on board
25 PC5 <-> LED 1 on board
2 PC13 <-> Not Connected

### Logic Convertion on Base Board

- Main UART Tx/Rx
- AUX UART Tx/Rx
- Debug UART Tx/Rx
- RI

### I2C Address

- INA226: 7 byte address is 0x80. with I2C1
- SI7021: 7 byte address is 0x40. with I2C2. After adding the r/w bit, should be 0x81 and 0x80;
- CAT24C128: 7 byte address is 0x54. with I2C2.
- SSD1306 display: 7 byte address is 0x78. with I2C2.

### EEPROM Storage Design

There are 256 pages available, 64 Bytes each. So the total capacity is 256\*64 = 16382 Bytes = 128 Kbits.

- Global Variables:
	- Last running mode

- Demo page
	- 0x2000 - 0x2003: uint32_t wakeup times from sleeping.
	- 0x2004 - 0x2004: uint8_t seconds to sleep (for RTT configuration).

## TF Card

Need pull-up 25 kOhm, serial 40 Ohm: CLK, CMD, Data0, Data1, Data2, Data3

Convex resistor array CAY16-223J8LF

# Current Sensing INA226

- Use Kelven connection!
- LSB for shunt voltage: fixed 2.5 uV.
- Calculation example:
	- Current LSB value = 0.8/2^15 = 0.000024414 = 24.414 uA
	- Calibration registor = 0.00512/(CurrentLSB\*ShuntResistor) = 0.00512 / (0.000024414\*0.05) = 4194
	- Example: Assume current_truth = 0.2A, R_shunt=0.05 Ohm, then shunt voltage = 10mV. ShuntVReg = 10mV/2.5uV=4000. current_calc = ShuntV\*CalibrationReg/2048 = 4000\*4194/2048 \* Current LSB = 8191 \* Current LSB=8191\*0.000024414=0.199984 A.
- Choose 100 mOhm resistor.

## Current sensing calibration

As the shunt resistor has resistant variation, we need to calibrate it. Here's how to get the calibration register value:

- The shunt resistor on board is 100 mOhm.
- Determine the max possible current: I_max = 0.6A
- Calculate the current LSB: current_lsb = I_max / 2^15 = 0.6/2^15 = **0.018311** mA/bit <= **Fix this number!**
- According to the 7.5.1 Eq(3) in the datasheet: CurrentRegister = ShuntVoltage * CalibrationReg / 2048
- I_acutal = CurrentRegister * current_lsb
- Accoarding to Eq(1), calbirationReg_theoretical = 0.00512 / (current_lsb*R_shunt) = 0.00512 / (0.018311/1000*0.1) = 2796.1
- **Assume** the calibrationReg = 2778 (according to the calibration measurement on an actual circuit board)
- CalibrationReg_New / CalibrationReg_Old (which is 2778) = multimeter_current_reading / current_reading_from_INA226 = multimeter_current_reading / (CurrentReg_Old * current_lsb)
- **Example**: CurrentReg (use USB VCP to check) is 13543, Multiply this by 0.018311, you get an INA226 current reading = 248 mA. Next, the multimeter reading is 246.0 mA. So 248/246 = CalibrationReg_New/2778 => we have CalibrationReg_New = 2778*248/246 = 2800.
- Update INA226_CALIB_VAL in ti_ina226.h Line32 with the new caibration register 2800
- Check that the new current reading is more accurate.

# Modules

- Need to convert 3.3v to 1.8v (bidirectional): BC26, BC66, BG96, SARA R410M 02B
- Need to convert 3.3v to 3.0v (bidirectional): BC28, BC35, BC95
- Left side: 16 pins
- Right side: 10 pins

# Programming Task Lists

- RTT clock signal configuration
- [x] Battery voltage sensing
- Sleep and wake-up
- Watch-dog
- Temperature and humidity sensor reading
- [x] EEPROM writing and reading (share the same I2C with the sensor)
- Current sensing
- TF card read/write through SDIO
- AT Command control API
- Server configuration
- Debug log reading
- Debug log FSM
- (\*) DMA: current I2C to SDIO

------

# Links

- current sensor resistors

	[10 mOhm](https://www.mouser.com/ProductDetail/ROHM-Semiconductor/PMR100HZPFU10L0?qs=sGAEpiMZZMtlleCFQhR%2FzZdCyObyGWxusWWJKncYy0Q%3D)
	[100 mOhm](https://www.mouser.com/ProductDetail/Bourns/CRM1206AFX-R100ELF?qs=sGAEpiMZZMtlleCFQhR%2FzXAGiOCRCr1IaXP90uykHS56ie6t3FxO7w%3D%3D)

- tf card socket

	http://www.klsele.com/products/connectors/641/4975.html

- Resistor array 8X

	- [8X 22kOhm](https://www.mouser.com/ProductDetail/Bourns/CAY16-223J8LF?qs=sGAEpiMZZMvrmc6UYKmaNe77kisCPsGdUuiwPEa9T%2FU%3D)
	- [4X 2.2kOhm](https://www.mouser.com/ProductDetail/Bourns/CAY16-222J4LF?qs=sGAEpiMZZMvrmc6UYKmaNUApqJ%252B%2FEZrJ%2FpdW56SM27Q%3D)
	- [8X 43 Ohm](https://www.mouser.com/ProductDetail/Bourns/CAY16-430J4LF?qs=sGAEpiMZZMukHu%252BjC5l7YZZvIpUe0TuoDMVA%252BgU2smk%3D)

- 8MHz Crystal Oscillator

	https://detail.tmall.com/item.htm?spm=a230r.1.14.11.6bc4917d8fGEWE&id=36990674059&cm_id=140105335569ed55e27b&abbucket=13

# Future

- [x] Replace the pull-up resistors and protection circuits for SD card with On Semiconductor **CM1624**.
- [x] Redesign the 3.3 V converter circuit.
- [ ] Isolate the 3.3 V power output with the circuit power (with a jumper cap).
- [ ] Add a 1.5k pull-up resistor at MCU USB D+. (Must Have)
- [ ] The PWR_KEY pin should not go though the TXB0108. Move this part to the base board with a transistor.

# Module Board

[Impedance Calculator](https://chemandy.com/calculators/coplanar-waveguide-with-ground-calculator.htm)

Fr4 material. Relative permittivity=4.4. The board thickness is chosen as 1 mm. The trace thickness is 1.35 mil for 1oz copper. 

Microstrip: the trace width should be **1.83~1.87** mm.
Coplanar: the gap width should be **0.3 mm**, the track width is **1.29 mm**.


# Module specific AT commands

## BG96

- Set once
    + Scan sequence
        * AT+QCFG="nwscanmode",3,1
        * AT+QCFG="iotopmode",1,1
        * AT+QCFG="band",1,1,180A,11

- AT+QPSMS?
    + +QPSMS: 1,,,"46800","2880"  // network side parameters.



## SARA R410M-02B 

GPIO assignment: 

- Pin16, M_NET_LED
- Pin19, SARA_GPIO1
- Pin23, SARA_GPIO2
- Pin24, SARA_GPIO3
- Pin25, SARA_STATUS_LED
- Pin42, SIM_DET

AT Command

These command is needed for only **ONCE**.

- Set pin function (Page 168)
  - AT+UGPIOC=16,2
  - AT+UGPIOC=25,10
  - AT+UGPIOC=42,7
  
- Set searchable bands (reboot to take effect)
  - AT+UBANDMASK=0,0,0
  - AT+UBANDMASK=1,6154,0 (only search Band 2, 4, 12, 13)
  
- Select RAT
  - AT+URAT=8 // NB-IoT only

- PDP context definition

  - 

- PSM setting
    + AT+CPSMS=1,,,"00101100","00000001"  // For all the USA modules. (except BC66)
    + 12 hours PSM, 2 seconds idle.
    + Default: +CPSMS:0,,,"00011000","00001010"
    
The belows need to be set every round.

- Cell Info (Not supported)

  - AT+UCGED=5
  - AT+UCGED?

# BC66

- Set the CGDEFCONT (PDP context)
  - AT+QCGDEFCONT="IP","mw01.vzwstatic"  // for new models

Default CPSMS: +CPSMS: 1,,,"00100011","00100010"
  - AT+CPSMS=1,,,"00100011","00100010"  // This is the default
  - AT+CPSMS=1,,,"00100011","00000101"  // new: idle 10 seconds.

- Set baudrate
    + AT+IPR=115200  // fixed rate
    + AT&W  // write to NVM
