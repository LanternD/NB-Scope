# Introduction

Auxilliary boards are used to extend the capability of the mainboard and shieldboard, as well as to calibrate the current sensors.

# Current Calibration Board

Since the 0.1 Ohm current sensing resistors are different, the current sensing should be calibrated as per mainboard. 

You need a series of resistors for this board. The actual resistance does not matter. We just compare the sensor reading with the digital multimeter or power monitor reading.

## How to calibrate

![calibration guide](../../../assets/current_sensing_calibration_guide.png)

Solder the 1.27 mm pitch headers according to the image above. Then follow the instruction to test the output.

Before calibration, make sure the embedded code runs the "current sensing demo" (`void run_demo8_i_bus_sensing()` in `Software/field-test-control/Src/fm_demo.c`). Check the `main.c` as well.

Steps:

1. See the figure above.
2. See the figure above.
3. Read and record the external current measurement device output (mA).
4. Read and record the INA226 output via the USB UART. The board will output the current register reading once per second.
5. Repeat the above steps for resistors from 13.3 Ohm to 165 Ohm. The 11 Ohm is not recommended. Do not try the 5.6 Ohm.
6. Calculation as follows:
  
  1. Multiply the register value by 0.018311 to get the current reading of INA226. (Note: if the output is already the current value, you don't need to do this conversion, depending on the output of the embedded program.)
  2. Divide the INA226 current by the meter reading current to get a ratio.
  3. Multiply the ratio with 2778 (the preset INA226 calibration register value) to get the new calibration register value. 
  4. Average all the calibration values to get the final calibration value.
  
Here is a table showing the measurement and calculation example for one of our board.

| Expected current (mA) | Meter reading (mA) | INA226 register reading | Calculated INA226 current (mA) | New calibration value |
|-----------------------|--------------------|-------------------------|--------------------------------|-----------------------|
|                    20 |               20.0 |                    1089 |                      19.940679 |              2786.264 |
|                  48.5 |               49.0 |                    2659 |                      48.688949 |              2795.747 |
|                   100 |               99.5 |                    5484 |                     100.417524 |              2752.517 |
|                   150 |              149.0 |                    8235 |                     150.791085 |              2745.003 |
|                   200 |              198.0 |                   10974 |                     200.944914 |              2737.287 |
|                   248 |                244 |                   13487 |                     246.960457 |              2744.699 |

The final calibration value is the average of the last column, resulting in 2760.

The value you get should not be too far from these value above. The final calibration value is around 2700 - 2900. For the same batch of boards, the standard deviation is less than 50. If you use a different batch of current sensing resistor, the value can deviate up to 150. 

**The new current calibration value should be written into the onboard EEPROM before node deployment.**

Note: you need to calibrate EVERY mainboard.

# Firmware Upgrade Extension Board

This is the predecessor of "Module Benchmark Extension Board". Generally you can ignore this one.

# Module Benchmark Extension Board

An upgraded version of "Firmware Upgrade Extension Board". It docks the shieldboard for the "real-time benchmark mode" of NB-Scope. It can be used to upgrade the NB-IoT module firmware as well. Basically it pinouts all the necessary connectivity of the UE module, such that we can connect them to other peripherals, such as power monitor and UART. 

The two pin headers are compatible with the mainboard.

The "EXT3V3" is used to connect to the power monitor. For example, the RED terminal of the monitor is connected to the EXT3V3, and the BLACK terminal is connected to the 3V3, repectively. "EXTGND" is likewise.

# PWRKEY Addon

A tiny board that simply has a BJT on it. It is used to fixed the PWRKEY pin on the UE modules before ver 3.2 mainboard. If you use the latest version of the mainboard, you can ignore this.
