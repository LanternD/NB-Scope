/**
  ********************************************************************************
  * @brief   STM32 HAL Library for INA226 Current/Power Monitor
  * @date    Feb 2016
  * @version 1.0
  * @author  George Christidis
  * @modified Deliang Yang
  ********************************************************************************
  * @details
			This library contains the necessary functions to initialize, read and
			write data to the TI INA226 Current/Power Monitor using the I2C
			protocol.
      Voltage range: -40.96 to 40.96 V
	******************************************************************************
	*/

#ifndef __TI_INA226_H__
#define __TI_INA226_H__

#include "stm32f1xx_hal.h"
#include "stm32f1xx_hal_i2c.h"
#include "main.h"
//#include "arm_math.h"

/* Module macros  ************************************************************/
#define INA226_I2C_PORT hi2c1

#ifndef INA226_ADDRESS
#define INA226_ADDRESS	0x80
#endif

#define INA226_CALIB_VAL		2778 // This needs measurement to find!
#define INA226_CURRENTLSB		0.018311 // mA/bit. calculate this according to the manual.
#define INA226_CURRENTLSB_INV	1/INA226_CURRENTLSB // bit/mA
#define INA226_VBUS_LSB 1.25F  // according to datasheet Page 16
#define INA226_POWERLSB_INV		1/(INA226_CURRENTLSB*25) // bit/mW
#define INA226_I2CTIMEOUT		10

#define INA226_CONFIG		0x00 // Configuration Register (R/W)
#define INA226_SHUNTV		0x01 // Shunt Voltage (R)
#define INA226_BUSV			0x02 // Bus Voltage (R)
#define INA226_POWER		0x03 // Power (R)
#define INA226_CURRENT		0x04 // Current (R)
#define INA226_CALIB		0x05 // Calibration (R/W)
#define INA226_MASK			0x06 // Mask/Enable (R/W)
#define INA226_ALERTL		0x07 // Alert Limit (R/W)
#define INA226_MANUF_ID		0xFE // Manufacturer ID (R)
#define INA226_DIE_ID		0xFF // Die ID (R)

#define INA226_MODE_POWER_DOWN			(0<<0) // Power-Down
#define INA226_MODE_TRIG_SHUNT_VOLTAGE	(1<<0) // Shunt Voltage, Triggered
#define INA226_MODE_TRIG_BUS_VOLTAGE	(2<<0) // Bus Voltage, Triggered
#define INA226_MODE_TRIG_SHUNT_AND_BUS	(3<<0) // Shunt and Bus, Triggered
#define INA226_MODE_POWER_DOWN2			(4<<0) // Power-Down
#define INA226_MODE_CONT_SHUNT_VOLTAGE	(5<<0) // Shunt Voltage, Continuous
#define INA226_MODE_CONT_BUS_VOLTAGE	(6<<0) // Bus Voltage, Continuous
#define INA226_MODE_CONT_SHUNT_AND_BUS	(7<<0) // Shunt and Bus, Continuous

// Shunt Voltage Conversion Time
#define INA226_VSH_140uS			(0<<3)
#define INA226_VSH_204uS			(1<<3)
#define INA226_VSH_332uS			(2<<3)
#define INA226_VSH_588uS			(3<<3)
#define INA226_VSH_1100uS			(4<<3)
#define INA226_VSH_2116uS			(5<<3)
#define INA226_VSH_4156uS			(6<<3)
#define INA226_VSH_8244uS			(7<<3)

// Bus Voltage Conversion Time (VBUS CT Bit Settings[6-8])
#define INA226_VBUS_140uS			(0<<6)
#define INA226_VBUS_204uS			(1<<6)
#define INA226_VBUS_332uS			(2<<6)
#define INA226_VBUS_588uS			(3<<6)
#define INA226_VBUS_1100uS			(4<<6)
#define INA226_VBUS_2116uS			(5<<6)
#define INA226_VBUS_4156uS			(6<<6)
#define INA226_VBUS_8244uS			(7<<6)

// Averaging Mode (AVG Bit Settings[9-11])
#define INA226_AVG_1				(0<<9)
#define INA226_AVG_4				(1<<9)
#define INA226_AVG_16				(2<<9)
#define INA226_AVG_64				(3<<9)
#define INA226_AVG_128				(4<<9)
#define INA226_AVG_256				(5<<9)
#define INA226_AVG_512				(6<<9)
#define INA226_AVG_1024				(7<<9)

// Reset Bit (RST bit [15])
#define INA226_RESET_ACTIVE			(1<<15)
#define INA226_RESET_INACTIVE		(0<<15)

// Mask/Enable Register
#define INA226_MER_SOL				(1<<15) // Shunt Voltage Over-Voltage
#define INA226_MER_SUL				(1<<14) // Shunt Voltage Under-Voltage
#define INA226_MER_BOL				(1<<13) // Bus Voltagee Over-Voltage
#define INA226_MER_BUL				(1<<12) // Bus Voltage Under-Voltage
#define INA226_MER_POL				(1<<11) // Power Over-Limit
#define INA226_MER_CNVR				(1<<10) // Conversion Ready
#define INA226_MER_AFF				(1<<4)  // Alert Function Flag
#define INA226_MER_CVRF				(1<<3)  // Conversion Ready Flag
#define INA226_MER_OVF				(1<<2)  // Math Overflow Flag
#define INA226_MER_APOL				(1<<1)  // Alert Polarity Bit
#define INA226_MER_LEN				(1<<0)  // Alert Latch Enable

#define INA226_MANUF_ID_DEFAULT	0x5449
#define INA226_DIE_ID_DEFAULT		0x2260

extern uint16_t i_bus_reg_buf[];
extern uint16_t i_bus_ticks_16_buf[];
extern uint32_t i_bus_ticks_32_buf[];
extern uint16_t i_idx;

/* Module function declaration ***********************************************/
float INA226_getBusV(void);
float INA226_getCurrent(void);
float INA226_getPower(void);

// Basic functions
/**
   @brief Send one byte to INA226.
   @param cmd_byte: 8-bit command, see above macros.
   @return 0 if no error, -1 otherwise.
   @note For general command sending.
*/
uint8_t ina226_send_one_byte(uint8_t cmd_byte);

/**
   @brief Set a 16-bit value to a register in INA226.
   @param cmd_byte: the register to be set.
   @param data_byte: 16-bit value for the register.
   @return 0 if succeed, -1 otherwise.
   @note All the value in ina226 are 16-bit format.
*/
uint8_t ina226_set_reg(uint8_t cmd_byte, uint16_t data_byte);

/**
   @brief Read register value of INA226.
   @param cmd_byte: 8-bit register indicator.
   @param rx_buf: a two-byte array for the results.
   @return register value if succeed, -1 otherwise.
   @note All the register value in INA226 are 16-bit format;
*/
uint16_t ina226_read_reg(uint8_t cmd_byte);

// Getter functions
uint16_t INA226_getConfig(void);
uint16_t INA226_getShuntV(void);
uint16_t INA226_getBusVReg(void);
uint16_t INA226_getPowerReg(void);
uint16_t INA226_getCalibrationReg(void);

/**
   @brief Get the Current Register (04H) value
   @param None
   @return 16-bit register value
   @note Current_reg value = ShuntV*Calibration_Reg/2048
*/
uint16_t INA226_getCurrentReg(void);
uint16_t INA226_getManufID(void);
uint16_t INA226_getDieID(void);
uint16_t INA226_getMaskEnable(void);
uint16_t INA226_getAlertLimit(void);

// Setter functions
uint8_t INA226_setConfig(uint16_t ConfigWord);
uint8_t INA226_setCalibrationReg(uint16_t ConfigWord);
uint8_t INA226_setAlertLimit(uint16_t ConfigWord);
uint8_t INA226_setMaskEnable(uint16_t ConfigWord);

#endif
