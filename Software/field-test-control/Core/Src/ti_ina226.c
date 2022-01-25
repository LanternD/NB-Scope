/**
  ********************************************************************************
  * @brief   STM32 HAL Library for INA226 Current/Power Monitor
  * @date    Feb 2016
  * @version 1.0
  * @author  George Christidis
  * @updated_by Deliang Yang
  ********************************************************************************
  * @details
                        This library contains the necessary functions to
  initialize, read and write data to the TI INA226 Current/Power Monitor using
  the I2C protocol.
        ******************************************************************************
        */

#include "ti_ina226.h"

/* Added by Deliang Yang *****************************************************/
uint16_t i_bus_reg_buf[512];      // moved to local. No need to be global
uint16_t i_bus_ticks_16_buf[512]; // moved to local. No need to be global
uint32_t i_bus_ticks_32_buf[256]; // moved to local. No need to be global
uint16_t i_idx = 0;               // moved to local. No need to be global

uint8_t ina226_send_one_byte(uint8_t cmd_byte) {
  uint8_t cmd = cmd_byte;
  return HAL_I2C_Master_Transmit(&INA226_I2C_PORT, INA226_ADDRESS, &cmd, 1,
                                 INA226_I2CTIMEOUT);
}

uint8_t ina226_set_reg(uint8_t cmd_byte, uint16_t data_byte) {
  uint8_t tx_buf[3];
  tx_buf[0] = cmd_byte;
  tx_buf[1] = (data_byte & 0xFF00) >> 8;
  tx_buf[2] = (data_byte & 0x00FF);

  return HAL_I2C_Master_Transmit(&INA226_I2C_PORT, INA226_ADDRESS, tx_buf, 3,
                                 INA226_I2CTIMEOUT);
}

uint16_t ina226_read_reg(uint8_t cmd_byte) {
  uint8_t cmd = cmd_byte;
  uint8_t rx_buf[2];
  HAL_I2C_Master_Transmit(&INA226_I2C_PORT, INA226_ADDRESS, &cmd, 1,
                          INA226_I2CTIMEOUT);
  if (HAL_I2C_Master_Receive(&INA226_I2C_PORT, INA226_ADDRESS, rx_buf, 2,
                             INA226_I2CTIMEOUT) != HAL_OK) {
    return 0xFF;
  } else {
    return ((uint16_t)rx_buf[0] << 8 | rx_buf[1]);
  }
}

float INA226_getBusV(void) { return (INA226_getBusVReg() * INA226_VBUS_LSB); }

float INA226_getCurrent(void) {
  int current_reg = (short)INA226_getCurrentReg();
  return (current_reg * INA226_CURRENTLSB);
}

float INA226_getPower(void) {
  return (INA226_getPowerReg() * INA226_POWERLSB_INV);
}

uint16_t INA226_getConfig(void) { return ina226_read_reg(INA226_CONFIG); }

uint16_t INA226_getShuntV(void) { return ina226_read_reg(INA226_SHUNTV); }

uint16_t INA226_getBusVReg(void) { return ina226_read_reg(INA226_BUSV); }

uint16_t INA226_getCalibrationReg(void) {
  return ina226_read_reg(INA226_CALIB);
}

uint16_t INA226_getPowerReg(void) { return ina226_read_reg(INA226_POWER); }

uint16_t INA226_getCurrentReg(void) { return ina226_read_reg(INA226_CURRENT); }

uint16_t INA226_getManufID(void) { return ina226_read_reg(INA226_MANUF_ID); }

uint16_t INA226_getDieID(void) { return ina226_read_reg(INA226_DIE_ID); }

uint16_t INA226_getMaskEnable(void) { return ina226_read_reg(INA226_MASK); }

uint16_t INA226_getAlertLimit(void) { return ina226_read_reg(INA226_ALERTL); }

uint8_t INA226_setConfig(uint16_t config_word) {
  return ina226_set_reg(INA226_CONFIG, config_word);
}

uint8_t INA226_setAlertLimit(uint16_t config_word) {
  return ina226_set_reg(INA226_ALERTL, config_word);
}

uint8_t INA226_setMaskEnable(uint16_t config_word) {
  return ina226_set_reg(INA226_MASK, config_word);
}

uint8_t INA226_setCalibrationReg(uint16_t config_word) {
  return ina226_set_reg(INA226_CALIB, config_word);
}
