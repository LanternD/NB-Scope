#include "si7021.h"

void si7021_init() { si7021_reset(); }
void si7021_reset() { si7021_send_command(CMD_SI7021_RESET); }

uint8_t si7021_send_command(uint8_t cmd) {
  uint8_t *cmd_local = &cmd;
  return HAL_I2C_Master_Transmit(&SI7021_I2C_PORT, SI7021_I2C_ADDRESS,
                                 cmd_local, 1, SI7021_I2C_TIMEOUT);
}

uint8_t si7021_send_long_command(uint16_t cmd) {
  uint8_t cmd_buf[2] = {(uint8_t)(cmd >> 8), (uint8_t)cmd & 0xFF};
  return HAL_I2C_Master_Transmit(&SI7021_I2C_PORT, SI7021_I2C_ADDRESS,
                                 (uint8_t *)&cmd_buf, 2, SI7021_I2C_TIMEOUT);
}

uint16_t si7021_received_2_bytes() {
  uint8_t received_data_table[2];
  if (HAL_OK != HAL_I2C_Master_Receive(&SI7021_I2C_PORT, SI7021_I2C_ADDRESS,
                                       received_data_table, 2,
                                       SI7021_I2C_TIMEOUT)) {
    return 0xFFFF;
  } else {
    return ((uint16_t)received_data_table[0] << 8 |
            received_data_table[1]); // most significant byte first.
  }
}

float si7021_read_previous_temp() {
  // Different from get_temperature.
  // Read temperature from last RH measurement.
  si7021_send_command(CMD_SI7021_READ_TEMPERATURE);
  uint16_t temp_code = si7021_received_2_bytes();
  if (0xFFFF != temp_code) {
    // formula from the datasheet
    enum temp_rh_indicator ind = TEMPERATURE;
    return si7021_convert_code_to_float(ind, temp_code);
  } else {
    return -1.0;
  }
}

float si7021_convert_code_to_float(enum temp_rh_indicator th_ind,
                                   uint16_t var_code) {
  if (TEMPERATURE == th_ind) {
    float temp = (175.72 * var_code / 65536) - 46.85;
    // TODO: trim value <-10 or >85 according to the datasheet
    return temp;
  } else if (RH == th_ind) {
    float rh = (125.0 * var_code / 65536) - 6;
    // TODO: trim value <0 or >100 according to the datasheet
    return rh;
  } else {
    return -1;
  }
}

uint16_t si7021_start_measure(uint8_t cmd) {
  // duplex for both temperature and RH. Use different cmd accordingly.
  // Do not pass CMD_SI7021_READ_TEMPERATURE cmd here.
  uint8_t received_data_table[3]; // msb, lsb, checksum

  if (HAL_OK != si7021_send_command(cmd)) {
    return -1;
  }
  HAL_Delay(10);
  if (HAL_OK != HAL_I2C_Master_Receive(&SI7021_I2C_PORT, SI7021_I2C_ADDRESS,
                                       received_data_table, 3,
                                       SI7021_I2C_TIMEOUT)) {
    return -1;
  } else {
    // most significant byte first. Ignore the checksum byte at this version.
    return ((uint16_t)received_data_table[0] << 8 | received_data_table[1]);
  }
}

float si7021_get_rh() {
  volatile uint16_t rh_code = si7021_start_measure(CMD_SI7021_MEASURE_RH_HOLD);
  enum temp_rh_indicator ind = RH;
  // merge with return after debugging.
  float rh_float = si7021_convert_code_to_float(ind, rh_code);
  return rh_float;
}

float si7021_get_temperature() {
  volatile uint16_t temp_code =
      si7021_start_measure(CMD_SI7021_MEASURE_TEMPERATURE_HOLD);
  enum temp_rh_indicator ind = TEMPERATURE;
  // merge with return after debugging.
  float temp_float = si7021_convert_code_to_float(ind, temp_code);
  return temp_float;
}

uint8_t si7021_get_firmware_version(void) {
  uint8_t fm_version;

  if (HAL_OK != si7021_send_long_command(CMD_SI7021_READ_FIRMWARE_REVISION)) {
    return -1;
  }
  HAL_Delay(10);
  if (HAL_OK != HAL_I2C_Master_Receive(&SI7021_I2C_PORT, SI7021_I2C_ADDRESS,
                                       &fm_version, 1, SI7021_I2C_TIMEOUT)) {
    return -1;
  }
  if (0xFF == fm_version) {
    fm_version = 1;
  } else if (0x20 == fm_version) {
    fm_version = 2;
  }
  return fm_version;
}
