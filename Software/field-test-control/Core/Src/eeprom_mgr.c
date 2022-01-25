#include "eeprom_mgr.h"

/* Basic functions ***********************************************************/
uint8_t eeprom_write_1_byte(uint16_t address, uint8_t *p_byte) {
  return HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                           EEPROM_MEMADDSIZE, p_byte, 1, EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_write_2_bytes(uint16_t address, uint8_t *p_bytes) {
  return HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                           EEPROM_MEMADDSIZE, p_bytes, 2, EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_write_4_bytes(uint16_t address, uint8_t *p_bytes) {
  uint8_t res = 0;
  res = HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                          EEPROM_MEMADDSIZE, p_bytes, 4, EEPROM_I2C_TIMEOUT);
  return res;
}

uint8_t eeprom_write_buffer(uint16_t start_address, uint8_t *p_data,
                            uint8_t size_of_data) {
  return HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, start_address,
                           EEPROM_MEMADDSIZE, p_data, size_of_data,
                           EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_write_page(uint16_t address, uint8_t *p_data) {
  return HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                           EEPROM_MEMADDSIZE, p_data, 64, EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_read_1_byte(uint16_t address, uint8_t *dest_buf) {
  return HAL_I2C_Mem_Read(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                          EEPROM_MEMADDSIZE, dest_buf, 1, EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_read_2_bytes(uint16_t address, uint8_t *dest_buf) {
  return HAL_I2C_Mem_Read(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                          EEPROM_MEMADDSIZE, dest_buf, 2, EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_read_4_bytes(uint16_t address, uint8_t *dest_buf) {
  uint8_t res = 0;
  res = HAL_I2C_Mem_Read(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                         EEPROM_MEMADDSIZE, dest_buf, 4, EEPROM_I2C_TIMEOUT);
  return res;
}

uint8_t eeprom_read_buffer(uint16_t start_address, uint8_t *dest_buf,
                           uint8_t size_of_data) {
  return HAL_I2C_Mem_Read(&EEPROM_I2C_PORT, EEPROM_ADDR, start_address,
                          EEPROM_MEMADDSIZE, dest_buf, size_of_data,
                          EEPROM_I2C_TIMEOUT);
}

uint8_t eeprom_read_page(uint16_t address, uint8_t *dest_buf) {
  return HAL_I2C_Mem_Read(&EEPROM_I2C_PORT, EEPROM_ADDR, address,
                          EEPROM_MEMADDSIZE, dest_buf, 64, EEPROM_I2C_TIMEOUT);
}

/* Meaningful blocks IO ******************************************************/
uint8_t eeprom_write_one_element(eeprom_element_t *ele) {
  uint8_t w_buf[4] = {0};
  uint8_t res = 0;
  if (1 == ele->byte_size) {
    w_buf[0] = ele->value & 0xFF;
    res = eeprom_write_1_byte(ele->addr, w_buf);
    /* res = HAL_I2C_Mem_Write(&EEPROM_I2C_PORT, EEPROM_ADDR, ele->addr, */
    /*                          EEPROM_MEMADDSIZE, w_buf, 1,
     * EEPROM_I2C_TIMEOUT); */
    HAL_Delay(2);
  } else if (2 == ele->byte_size) {
    w_buf[0] = ele->value & 0xFF;
    w_buf[1] = (ele->value >> 8) & 0xFF;
    res = eeprom_write_2_bytes(ele->addr, w_buf);
    HAL_Delay(4);
  } else if (4 == ele->byte_size) {
    w_buf[0] = ele->value & 0xFF;
    w_buf[1] = (ele->value >> 8) & 0xFF;
    w_buf[2] = (ele->value >> 16) & 0xFF;
    w_buf[3] = (ele->value >> 24) & 0xFF;
    res = eeprom_write_4_bytes(ele->addr, w_buf);
    HAL_Delay(8);
  } else {
    res = -1;
  }
  return res;
}

uint8_t
eeprom_write_board_constant_meta_struct(eeprom_board_constant_meta_t *bcm_st) {
  uint8_t failure_cnt = 0;
  failure_cnt += eeprom_write_one_element(&bcm_st->node_region);
  failure_cnt += eeprom_write_one_element(&bcm_st->node_num);
  failure_cnt += eeprom_write_one_element(&bcm_st->module_on_board);
  failure_cnt += eeprom_write_one_element(&bcm_st->network_operator);
  failure_cnt += eeprom_write_one_element(&bcm_st->is_debug_log_supported);
  failure_cnt += eeprom_write_one_element(&bcm_st->base_board_hardware_version);
  failure_cnt +=
      eeprom_write_one_element(&bcm_st->module_board_hardware_version);
  failure_cnt += eeprom_write_one_element(&bcm_st->current_calibration_value);
  failure_cnt += eeprom_write_one_element(&bcm_st->v_batt_calibration_value);
  return failure_cnt;
}

uint8_t
eeprom_write_board_variable_meta_struct(eeprom_board_variable_meta_t *bvm_st) {
  uint8_t failure_cnt = 0;
  failure_cnt += eeprom_write_one_element(&bvm_st->mcu_software_version);
  failure_cnt += eeprom_write_one_element(&bvm_st->year_month_date);
  return failure_cnt;
}

uint8_t eeprom_write_task_monitor_struct(eeprom_task_monitor_t *tm_st) {
  uint8_t failure_cnt = 0;
  failure_cnt += eeprom_write_one_element(&tm_st->is_task_assigned);
  failure_cnt += eeprom_write_one_element(&tm_st->test_mode);
  failure_cnt += eeprom_write_one_element(&tm_st->test_id);
  failure_cnt += eeprom_write_one_element(&tm_st->application_type);
  failure_cnt += eeprom_write_one_element(&tm_st->collect_debug_log_or_current);
  failure_cnt += eeprom_write_one_element(&tm_st->ul_total_time);
  failure_cnt += eeprom_write_one_element(&tm_st->ul_total_pkt);
  failure_cnt += eeprom_write_one_element(&tm_st->ul_pkt_count);
  failure_cnt += eeprom_write_one_element(&tm_st->ul_pkt_size);
  failure_cnt += eeprom_write_one_element(&tm_st->mcu_sleep_timer);
  failure_cnt += eeprom_write_one_element(&tm_st->task_status);
  failure_cnt += eeprom_write_one_element(&tm_st->err_code_last_run);
  return failure_cnt;
}

uint8_t eeprom_read_one_element(eeprom_element_t *ele) {
  uint8_t res;
  if (1 == ele->byte_size) {
    uint8_t rcv_byte;
    res = eeprom_read_1_byte(ele->addr, &rcv_byte);
    ele->value = rcv_byte;
    return res;
  } else if (2 == ele->byte_size) {
    uint8_t rcv_buf[2];
    res = eeprom_read_2_bytes(ele->addr, rcv_buf);
    ele->value = (int)(rcv_buf[1] << 8) | rcv_buf[0];
    return res;
  } else if (4 == ele->byte_size) {
    uint8_t rcv_buf[4] = {0};
    res = eeprom_read_4_bytes(ele->addr, rcv_buf);
    ele->value = (int)(rcv_buf[3] << 24) | (rcv_buf[2] << 16) |
                 (rcv_buf[1] << 8) | rcv_buf[0];
    return res;
  } else {
    return -1;
  }
}

uint8_t eeprom_read_board_constant_meta_struct(
    eeprom_board_constant_meta_t *dest_bcm_st) {
  uint8_t failure_cnt = 0;

  failure_cnt += eeprom_read_one_element(&dest_bcm_st->node_region);
  failure_cnt += eeprom_read_one_element(&dest_bcm_st->node_num);
  failure_cnt += eeprom_read_one_element(&dest_bcm_st->module_on_board);
  failure_cnt += eeprom_read_one_element(&dest_bcm_st->network_operator);
  failure_cnt += eeprom_read_one_element(&dest_bcm_st->is_debug_log_supported);
  failure_cnt +=
      eeprom_read_one_element(&dest_bcm_st->base_board_hardware_version);
  failure_cnt +=
      eeprom_read_one_element(&dest_bcm_st->module_board_hardware_version);
  failure_cnt +=
      eeprom_read_one_element(&dest_bcm_st->current_calibration_value);
  failure_cnt +=
      eeprom_read_one_element(&dest_bcm_st->v_batt_calibration_value);

  return failure_cnt;
}

uint8_t eeprom_read_board_variable_meta_struct(
    eeprom_board_variable_meta_t *dest_bvm_st) {

  uint8_t failure_cnt = 0;

  failure_cnt += eeprom_read_one_element(&dest_bvm_st->mcu_software_version);
  failure_cnt += eeprom_read_one_element(&dest_bvm_st->year_month_date);
  failure_cnt += eeprom_read_one_element(&dest_bvm_st->mcu_wakeup_count);

  return failure_cnt;
}
uint8_t eeprom_read_task_monitor_struct(eeprom_task_monitor_t *dest_tm_st) {
  uint8_t failure_cnt = 0;

  failure_cnt += eeprom_read_one_element(&dest_tm_st->is_task_assigned);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->test_mode);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->test_id);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->application_type);
  failure_cnt +=
      eeprom_read_one_element(&dest_tm_st->collect_debug_log_or_current);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->ul_total_time);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->ul_total_pkt);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->ul_pkt_count);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->ul_pkt_size);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->mcu_sleep_timer);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->task_status);
  failure_cnt += eeprom_read_one_element(&dest_tm_st->err_code_last_run);

  return failure_cnt;
}
