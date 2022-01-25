/**
 ******************************************************************************
 * @file           : si7021.h
   @author: Deliang Yang
 * @brief          : header for controlling Silicon Lab SI7021, reading
 *  temperature and relative humidity (RH), via the I2C interface.
 * @date_created: 2019.11.12
 ******************************************************************************
 * @attention: (1) I assume there is only one SI7021 on the board. If there are
 *multiple, please add I2C handler and device address to method argument. (2)
 SI7021 measures the temperature automatically when it measures the RH. So just
 measure RH and "read temperature from previous RH measurement" to save the
 time.
 */
#ifndef __SI7021_H__
#define __SI7021_H__

#include "main.h" // add the hi2c2 declaration
#include "stm32f1xx_hal.h"

/* Module macros  ************************************************************/
// Define SI7021 port and address
#define SI7021_I2C_PORT hi2c2
#define SI7021_I2C_ADDRESS (0x40 << 1)

// Command available for SI7021
#define CMD_SI7021_MEASURE_RH_HOLD 0xE5
#define CMD_SI7021_MEASURE_RH_NO_HOLD 0xF5
#define CMD_SI7021_MEASURE_TEMPERATURE_HOLD 0xE3
#define CMD_SI7021_MEASURE_TEMPERATURE_NO_HOLD 0xF3
#define CMD_SI7021_READ_TEMPERATURE 0xE0
#define CMD_SI7021_RESET 0xFE
#define CMD_SI7021_WRITE_USER_REG1 0xE6
#define CMD_SI7021_READ_USER_REG1 0xE7
#define CMD_SI7021_WRITE_HEATER_CONTROL_REG 0x51
#define CMD_SI7021_READ_HEATER_CONTROL_REG 0x11
#define CMD_SI7021_READ_EID_0 0xFA
#define CMD_SI7021_READ_EID_1 0x0F
#define CMD_SI7021_READ_EID_2 0xFC
#define CMD_SI7021_READ_EID_3 0xC9
#define CMD_SI7021_READ_FIRMWARE_REVISION 0x84B8

// Other macros
#define SI7021_I2C_TIMEOUT 10000

/* Locally defined typedefs and variables declaration with the typedef *******/
enum temp_rh_indicator { TEMPERATURE, RH };

/* Module function declaration ***********************************************/
// TODO: add description for the following functions.
void si7021_reset(void);
void si7021_init(void);
uint8_t si7021_send_command(uint8_t cmd);
uint8_t si7021_send_long_command(uint16_t cmd); // probably don't need this.

uint16_t si7021_start_measure(uint8_t cmd);
float si7021_convert_code_to_float(enum temp_rh_indicator th_ind,
                                   uint16_t var_code);
float si7021_read_previous_temp(void); // different from get_temp
float si7021_get_rh(void);
float si7021_get_temperature(void);
void si7021_write_user_register(uint8_t reg_value);
uint8_t si7021_read_user_register(void);
// TODO: implement checksum checking, heater on/off, change resolution
uint8_t si7021_get_firmware_version(void);
// TODO: implement this function.
uint8_t si7021_check_device_id1(void);

#endif
