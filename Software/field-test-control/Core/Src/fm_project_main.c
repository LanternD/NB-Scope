/**
   @file fm_project_main.c
   @brief Actual main program body
   @author Deliang Yang
   @date_created 2019.11.13
   @note The main.c is always subject to modification by the CubeMX code
   generator. I would like to move the user added functions here to keep all my
   code consistent.
   @attention Try not to define global variables here. Define them in their own
   module instead.
 */

#include "fm_project_main.h"
#include "main.h"

/* Variables for other modules ***********************************************/

work_mode_fsm_et work_mode = STATE_INIT; // applied globally
uint8_t pseudo_assigned_flag = 0;
const char nl = '\n'; // for usb_cdc_vcp new line

uint8_t sw1_cnt_to_start_field_test = 0;
uint8_t sw2_cnt_to_terminate_field_test = 0;
uint8_t proceed_to_init_packet_flag = 0;
uint8_t terminate_task_flag = 0;

// These eeprom struct are default value, should be override after loading.
eeprom_board_constant_meta_t g_bcm_st = {
    {EEPROM_BCM_ADDR_START, 'A', 1},               // node_region
    {EEPROM_BCM_ADDR_START + 1, 7, 1},             // node_num
    {EEPROM_BCM_ADDR_START + 2, (uint8_t)BC28, 1}, // module_on_board
    {EEPROM_BCM_ADDR_START + 3, (uint8_t)OPERATOR_UNDEFINED,
     1},                                  // network_operator
    {EEPROM_BCM_ADDR_START + 4, 0, 1},    // is_debug_log_supported
    {EEPROM_BCM_ADDR_START + 5, 3, 1},    // base_board_hardware_version
    {EEPROM_BCM_ADDR_START + 6, 1, 1},    // module_board_hardware_version
    {EEPROM_BCM_ADDR_START + 7, 2743, 2}, // current_calibration_value
    {EEPROM_BCM_ADDR_START + 9, 1485, 2}, // v_batt_calibration_value
};

eeprom_board_variable_meta_t g_bvm_st = {
    {EEPROM_BVM_ADDR_START, 2, 2}, // mcu_software_version
    {EEPROM_BVM_ADDR_START + 2, (2020 << 16) | (1 << 8) | (17),
     4},                               // year_month_date
    {EEPROM_BVM_ADDR_START + 6, 0, 4}, // mcu_wakeup_count
};

eeprom_task_monitor_t g_eeprom_tm_st = {
    {EEPROM_TM_ADDR_START, 0, 1},        // is_task_assigned
    {EEPROM_TM_ADDR_START + 1, 1, 1},    // test_mode
    {EEPROM_TM_ADDR_START + 2, 0, 2},    // test_id
    {EEPROM_TM_ADDR_START + 4, 0, 1},    // application_type
    {EEPROM_TM_ADDR_START + 5, 1, 1},    // collect_debug_log_or_current
    {EEPROM_TM_ADDR_START + 6, 0, 2},    // ul_total_time
    {EEPROM_TM_ADDR_START + 8, 30, 2},   // ul_total_pkt
    {EEPROM_TM_ADDR_START + 10, 10, 2},  // ul_pkt_count
    {EEPROM_TM_ADDR_START + 12, 256, 2}, // ul_pkt_size
    {EEPROM_TM_ADDR_START + 14, 25, 2},  // mcu_sleep_timer
    {EEPROM_TM_ADDR_START + 16, 0, 1},   // task_status
    {EEPROM_TM_ADDR_START + 17, 0, 1},   // error_code_last_run
};

/* Functions ***************************************************************/

// No need to add this function to fm_project_main.h. It has already been
// declared.
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {

  switch (work_mode) {
  case STATE_DEMOS:
    if (GPIO_Pin == GPIO_PIN_0) {
      HAL_GPIO_TogglePin(LED0_GPIO_Port, LED0_Pin);
    }
    elif (GPIO_Pin == GPIO_PIN_1) {
      HAL_GPIO_TogglePin(LED1_GPIO_Port, LED1_Pin);
    }
    break;

  case STATE_INIT_PACKET: // Press SW1 3 times, and the MCU starts field test
                          // routine.
    if (GPIO_Pin == GPIO_PIN_0) {
      sw1_cnt_to_start_field_test += 1;
      if (3 <= sw1_cnt_to_start_field_test) {
        // TODO: update display and USB VCP
        // TODO: update the task_status_code in task monitor
        proceed_to_init_packet_flag = 1; // Let it pass.
        sw1_cnt_to_start_field_test = 0;
      }
    } else if (GPIO_Pin == GPIO_PIN_1) {
      sw1_cnt_to_start_field_test = 0; // clear the count
    }
    break;

  case STATE_FIELD_TEST:
    if (GPIO_Pin == GPIO_PIN_0) {
      sw2_cnt_to_terminate_field_test = 0; // clear the count
    } else if (GPIO_Pin == GPIO_PIN_1) {
      sw2_cnt_to_terminate_field_test += 1;
      if (3 <= sw2_cnt_to_terminate_field_test) {
        // TODO: update display and USB VCP
        // TODO: update the task_status_code in task monitor and reboot.
        terminate_task_flag = 1;
        sw2_cnt_to_terminate_field_test = 0;
        /* work_mode = STATE_IDLE; // terminate the field test. */
      }
      break;

    default:
      // Do nothing
      HAL_Delay(1);
      break;
    }
  }
}

void emit_field_test_start_signal(void) {
  LED0_ON;
  LED1_ON;
  for (uint8_t i = 0; i < 10; i++) {
    LED0_TOGGLE;
    LED1_TOGGLE;
    HAL_Delay(250);
  }
  LED0_OFF;
  LED1_OFF;
}

void emit_field_test_terminate_signal(void) {
  LED0_ON;
  LED1_OFF;
  for (uint8_t i = 0; i < 10; i++) {
    LED0_TOGGLE;
    LED1_TOGGLE;
    HAL_Delay(250);
  }
  LED0_OFF;
  LED1_OFF;
}

uint32_t get_rtc_timestamp(void) {
  RTC_TimeTypeDef rtc_time_st;
  HAL_RTC_GetTime(&hrtc, &rtc_time_st, RTC_FORMAT_BIN);
  return rtc_time_st.Hours * 3600 + rtc_time_st.Minutes * 60 +
         rtc_time_st.Seconds;
}

void project_additional_init(void) {
  DWT_Init();

  // Reset NB-IoT Module. Note: the e_module_type may be undefined.
  module_reset(0);
  // Listen to the main UART.
  __HAL_UART_ENABLE_IT(&MAIN_UART, UART_IT_IDLE);
  HAL_UART_Receive_DMA(&MAIN_UART, main_uart_rx_buf, MAIN_UART_BUF_SIZE);

  // Humidity temperature sensor init
  si7021_init();

  // ADC calibration
  HAL_ADCEx_Calibration_Start(&V_BATT_ADC);
  HAL_Delay(3);
}

void power_enter_sleep_mode(void) {
  /* HAL_DBGMCU_DisableDBGSleepMode();  // Optional */
  /* SysTick->CTRL = 0x00;  // shutdown the timer */
  /* SysTick->VAL = 0x00; */
  config_rtc_standby_auto_wakeup_after(15);
  HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
}

void config_rtc_standby_auto_wakeup_after(uint16_t alarm_sec) {
  HAL_RTC_Init(&hrtc);

  // Clear previous PWR flags.
  __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);
  __HAL_RTC_ALARM_CLEAR_FLAG(&hrtc, RTC_FLAG_ALRAF);

  RTC_AlarmTypeDef rtc_alarm_st;
  uint32_t time_second_format;
  uint32_t time_alarm_second_format;

  // Get current time
  time_second_format = get_rtc_timestamp();

  // Set alarm timer
  time_alarm_second_format = time_second_format + alarm_sec;

  rtc_alarm_st.Alarm = 0; // only one alarm_id for STM32F1, default=0
  rtc_alarm_st.AlarmTime.Hours = time_alarm_second_format / 3600;
  rtc_alarm_st.AlarmTime.Minutes = (time_alarm_second_format % 3600) / 60;
  rtc_alarm_st.AlarmTime.Seconds = time_alarm_second_format % 60;

  HAL_RTC_SetAlarm_IT(&hrtc, &rtc_alarm_st, RTC_FORMAT_BIN);
}

void usb_cdc_send_string(char *str_buf) {
#if HAS_USB_CDC_VCP
  uint16_t len_str = 0;
  char *p = str_buf;
  // auto count the string length. Send until \0 or \n
  while (len_str < 1024 and (*p != '\0') and (*p != '\n')) {
    len_str++;
    p++;
  }
  if (*p == '\n') {
    len_str += 1; // count the '\n'
  }
  CDC_Transmit_FS((uint8_t *)str_buf, len_str);
  /* DWT_Delay(90*len_str);  // 86.81 us per byte under 115200 */
  HAL_Delay(1 + len_str / 10); // choose the delay empirically
  // wait for the transmission completes.
#endif
}

void usb_cdc_new_line(void) {
  CDC_Transmit_FS((uint8_t *)&nl, 1);
  HAL_Delay(1);
}

/***************************************************************************/

void current_sensing_to_sd_pipeline(char *CMD) {
  // Pipeline: current sensing.
  LED1_ON;

  INA226_setConfig(INA226_MODE_CONT_SHUNT_VOLTAGE | INA226_VSH_140uS |
                   INA226_AVG_1);
  INA226_setCalibrationReg(
      g_bcm_st.current_calibration_value.value); // important!

  uint32_t c_data_point_cnt = 0;
  float v_bus = 0;
  float i_bus = 0;

  sdm_st.sd_res = FR_TIMEOUT;   // initialization
  sdm_st.is_sd_mounted = False; // maybe run in ULTX.
  sdm_st.is_file_opened = False;
  sdm_st.need_block_rewrite = False;
  sdm_st.consecutive_zero_cnt = 0;
  sdm_st.cumulative_fatfs_io_error = 0;

  if (STATE_PPL_CURRENT_SENSING_TO_SD == work_mode) {
    eeprom_element_t dev_file_cnt = {0x3FF0, 0, 2};
    eeprom_read_one_element(&dev_file_cnt);
    char dev_file_id[4] = "";
    dy_itoa_with_leading_0(dev_file_cnt.value++, 4, dev_file_id);
    // Override the file name in develop mode.
    strcpy(file_path_field_st.node_id, "Dev");
    strcpy(file_path_field_st.i_d_indicator, "I");
    strcpy(file_path_field_st.test_id, "7775");
    strcpy(file_path_field_st.packet_index, dev_file_id);
    export_one_field("[INFO] Log file id: ", dev_file_id);

    usb_cdc_send_string("[INFO] Develop mode. Press SW2 to begin\n");
    while (!(IS_BUTTON2_PRESSED)) {
    } // only in debug mode.
    eeprom_write_one_element(&dev_file_cnt);
  }
  // This field may be overriden by ULTX pipeline, set it again.
  strcpy(file_path_field_st.i_d_indicator, "I");
  generate_log_file_name(sdm_st.file_path);

  enum current_output_format {
    ALL_CURRENT,
    TIMETICK_16_CURRENT,
    TIMETICK_32_CURRENT
  };
  const enum current_output_format cofm = TIMETICK_16_CURRENT;
  uint16_t i_write_buffer_len = 0;

  uint16_t format_1_write_buf[20 * SD_BLOCK_SIZE];   // block size=512
  uint16_t format_1_current_buf[10 * SD_BLOCK_SIZE]; // effective num of points
  uint16_t format_1_timestamp16_buf[10 * SD_BLOCK_SIZE];
  // Note: block number test passed: 1, 4, 8, 20. Failed: 40 (too much memory)

  // Control error handler in the pipeline.
  sdm_st.fix_sd_code = SD_NEED_NOTHING;

  // Mount SD card
  if (!sdm_st.is_sd_mounted) {
    sdm_st.is_sd_mounted = f_mount_with_retry();
  }
  if (!sdm_st.is_sd_mounted) {
    usb_cdc_send_string("[ERR] No Micro SD found! Plug it in and reset MCU.");
  }

  // Open file.
  if (sdm_st.is_sd_mounted) {
    sdm_st.is_file_opened =
        f_open_append_with_retry(&fm_file, sdm_st.file_path);
  }

  uint32_t rtc_now = get_rtc_timestamp();
  uint32_t tmp_rtc = rtc_now; // FIXME: this is for debug only.
  static uint8_t is_ul_packet_sent = False;  // Mark whether the ul packet is sent.

  // Pipeline loop
  while (!(IS_BUTTON1_PRESSED) and
         (rtc_now <= tmp_rtc + COLLECT_DATA_TIMEOUT) and !terminate_task_flag) {
    // TODO: add low current sensing break rule

    sdm_st.need_block_rewrite = False;
    sdm_st.sd_res = 0;
    sdm_st.fix_sd_code = SD_NEED_NOTHING;

    // Collect points
    HAL_GPIO_WritePin(GPIO_3_GPIO_Port, GPIO_3_Pin, GPIO_PIN_SET);
    sdm_st.fix_sd_code = SD_NEED_NOTHING;
    if (ALL_CURRENT == cofm) {
      // 16-bit current, continuous
      for (i_idx = 0; i_idx < 256; i_idx++) {
        i_bus_reg_buf[i_idx] = INA226_getCurrentReg();
        c_data_point_cnt++;
      }
      i_write_buffer_len = 512;
    } else if (TIMETICK_16_CURRENT == cofm) {
      // 16-bit ticks + 16-bit current, interleaved
      for (i_idx = 0; i_idx < 10 * SD_BLOCK_SIZE; i_idx++) {
        format_1_current_buf[i_idx] = INA226_getCurrentReg();
        format_1_timestamp16_buf[i_idx] = HAL_GetTick() & 0xFFFF;
        c_data_point_cnt++;
      }
      // Interleave the data points.
      for (int k = 0; k < 10 * SD_BLOCK_SIZE; ++k) {
        format_1_write_buf[2 * k] = format_1_timestamp16_buf[k];
        format_1_write_buf[2 * k + 1] = format_1_current_buf[k];
      }
      i_write_buffer_len = 40 * SD_BLOCK_SIZE;
    }
    // Benchmark sampling rate.
    HAL_GPIO_WritePin(GPIO_3_GPIO_Port, GPIO_3_Pin, GPIO_PIN_RESET);

    // Write to file.
    if (sdm_st.is_sd_mounted and sdm_st.is_file_opened) {
      HAL_GPIO_WritePin(GPIO_2_GPIO_Port, GPIO_2_Pin, GPIO_PIN_SET);
      sdm_st.file_end_ptr = f_tell(&fm_file); // record before writing block
      // Write to file
      if (ALL_CURRENT == cofm) {
        sdm_st.sd_res = f_write(&fm_file, i_bus_reg_buf, i_write_buffer_len,
                                (void *)&f_w_cnt);
        // f_sync(&fm_file);
      } else if (TIMETICK_16_CURRENT == cofm) {
        sdm_st.sd_res = f_write(&fm_file, format_1_write_buf,
                                i_write_buffer_len, (void *)&f_w_cnt);
        // f_sync(&fm_file);
      }
      // Benchmark the write time.
      HAL_GPIO_WritePin(GPIO_2_GPIO_Port, GPIO_2_Pin, GPIO_PIN_RESET);

      (0 == sdm_st.sd_res) ? sdm_st.consecutive_zero_cnt++
                           : sdm_st.cumulative_fatfs_io_error++;

      // Reset zero counter, show continuous write success count in ().
      sdio_show_success_count_and_io_error();

      // Set flag if necessary.
      sdio_determine_fixing_request();

    } else {
      g_tm_st.error_code_this_run = (uint8_t)TASK_ERR_SDIO_TOO_MANY_ERRORS;
      if (!sdm_st.is_file_opened) {
        usb_cdc_send_string("[ERR] File not opened, go to REOPEN option\n");
        sdm_st.fix_sd_code = SD_NEED_REOPEN_APPEND;
      }
      if (!sdm_st.is_sd_mounted) {
        // higher priority, override the above one.
        usb_cdc_send_string("[ERR] SD not mounted, go to REMOUNT option\n");
        sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
      }
    }

    // Fix error if there is any above.
    sd_card_fixing_routine();

    if (sdm_st.need_block_rewrite) { // assume mounted+opened
      // Write again
      if (ALL_CURRENT == cofm) {
        sdm_st.sd_res = f_write(&fm_file, i_bus_reg_buf, i_write_buffer_len,
                                (void *)&f_w_cnt);
        /* f_sync(&fm_file); */
      } else if (TIMETICK_16_CURRENT == cofm) {
        sdm_st.sd_res = f_write(&fm_file, format_1_write_buf,
                                i_write_buffer_len, (void *)&f_w_cnt);
        // f_sync(&fm_file);
      }
      (0 == sdm_st.sd_res) ? sdm_st.consecutive_zero_cnt++
                           : sdm_st.cumulative_fatfs_io_error++;
      sdm_st.need_block_rewrite = False;
    }

#if HAS_USB_CDC_VCP
    // Note: this display consumes lots of time and will affect current sensing
    if (c_data_point_cnt % (200 * 512) == 0) {

      f_sync(&fm_file); // sync every 200 blocks just in case.

      char dp_cnt_disp[17] = {'\0'};
      dy_itoa(c_data_point_cnt / 512, dp_cnt_disp);
      dy_shift_leading_null_chars(dp_cnt_disp);
      dy_append_newline(dp_cnt_disp);
      export_one_field("i_mod block count: ", dp_cnt_disp);
    }
#if HAS_DISPLAY && 0
    char dp_cnt_disp[17] = {'\0'};
    dy_itoa(c_data_point_cnt, dp_cnt_disp);
    dy_shift_leading_null_chars(dp_cnt_disp);
    dy_append_newline(dp_cnt_disp);
    strcpy(i_bus_sensing_ppl_page.line4, dp_cnt_disp);
    ssd1306_display_whole_screen(i_bus_sensing_ppl_page);
#endif

#endif
    // equals to "if False" at this point.
    if (c_data_point_cnt % 10240 == 1) {

      char i_bus_disp[17] = {'\0'};
      char v_bus_disp[17] = {'\0'};

      dy_ftoa(i_bus, i_bus_disp);
      dy_shift_leading_null_chars(i_bus_disp);
      dy_append_newline(i_bus_disp);

      v_bus = INA226_getBusV(); // per 10k current measurement.
      dy_ftoa(v_bus, v_bus_disp);
      dy_shift_leading_null_chars(v_bus_disp);
      dy_append_newline(v_bus_disp);

#if HAS_DISPLAY && HAS_USB_CDC_VCP
      char dp_cnt_disp[17] = {'\0'};
      dy_itoa(c_data_point_cnt, dp_cnt_disp);
      dy_shift_leading_null_chars(dp_cnt_disp);
      dy_append_newline(dp_cnt_disp);

      strcpy(i_bus_sensing_ppl_page.line4, dp_cnt_disp);
      ssd1306_display_whole_screen(i_bus_sensing_ppl_page);
      usb_cdc_send_string("#point: ");
      usb_cdc_send_string(dp_cnt_disp);
      usb_cdc_send_string("I: ");
      usb_cdc_send_string(i_bus_disp);
      usb_cdc_send_string("V: ");
      usb_cdc_send_string(v_bus_disp);
#endif
    }
    rtc_now = get_rtc_timestamp();
  }

  // Send the UL packet after one cycle of the current sensing.
  if (!is_ul_packet_sent) {
    // IMPORTANT: make sure this is executed for only once.
    mod_send_field_test_pack(CMD);
    is_ul_packet_sent = True;
  }

  // Close file
  uint8_t is_file_closed = f_close_with_retry(&fm_file);
  if (True == is_file_closed) {
    sdm_st.is_file_opened = False;
  }
  // TODO: get the timestamp from the network and update this.
  f_set_timestamp(sdm_st.file_path, 2020, 1, 8, 17, 28, 12);
  usb_cdc_send_string("[INFO] Current pipeline ended.\n");
}

/***************************************************************************/

void dbg_log_to_sd_pipeline(char *CMD) {
  // Pipeline: Read debug log from the UART (BC28/35/95). Save to SD card.
  SSD1306_screen_text_t dbg_log_reading_ppl_page;

  strcpy(dbg_log_reading_ppl_page.line1, "Pipeline\n");
  strcpy(dbg_log_reading_ppl_page.line2, "DGB log => SD\n");
  strcpy(dbg_log_reading_ppl_page.line3, " ");
  strcpy(dbg_log_reading_ppl_page.line4, " ");

  ssd1306_display_whole_screen(dbg_log_reading_ppl_page);

  usb_cdc_new_line();
  usb_cdc_send_string(dbg_log_reading_ppl_page.line1);
  usb_cdc_send_string(dbg_log_reading_ppl_page.line2);

  /* FRESULT sd_res = FR_TIMEOUT; // initialization */
  /* uint8_t sd_failed_attempt = 0; */
  /* uint8_t is_sd_mounted = False; */
  /* uint8_t is_file_opened = False; */
  sdm_st.need_block_rewrite = False;
  sdm_st.sd_res = FR_TIMEOUT; // initialization
  sdm_st.is_sd_mounted = False;
  sdm_st.is_file_opened = False;
  sdm_st.need_block_rewrite = False;
  sdm_st.consecutive_zero_cnt = 0;
  sdm_st.cumulative_fatfs_io_error = 0;
  sdm_st.fix_sd_code = SD_NEED_NOTHING;

  /* char file_path[30] = ""; //"dbg_log_dev_0001.log"; */
  if (STATE_PPL_DBG_LOG_TO_SD == work_mode) {
    eeprom_element_t dev_file_cnt = {0x3FF2, 0, 2};
    eeprom_read_one_element(&dev_file_cnt);
    char dev_file_id[4] = "";
    dy_itoa_with_leading_0(dev_file_cnt.value++, 4, dev_file_id);
    strcpy(file_path_field_st.node_id, "Dev");
    strcpy(file_path_field_st.i_d_indicator, "D");
    strcpy(file_path_field_st.test_id, "8888");
    strcpy(file_path_field_st.packet_index, dev_file_id);
    export_one_field("[INFO] Log file id: ", dev_file_id);

    usb_cdc_send_string("[INFO] Develop mode. Press SW2 to begin\n");
    while (!(IS_BUTTON2_PRESSED)) {
    } // only in debug mode.
    eeprom_write_one_element(&dev_file_cnt);
  }
  generate_log_file_name(sdm_st.file_path);

  /* uint16_t consecutive_zero_cnt = 0; */
  /* uint16_t cumulative_fatfs_io_error = 0; */

  strcpy(dbg_log_reading_ppl_page.line3, "SW1=Stop/kB cnt:\n");

  ssd1306_display_whole_screen(dbg_log_reading_ppl_page);

  // Mount SD card
  if (FR_OK == f_mount_with_retry()) {
    sdm_st.is_sd_mounted = True;
  } else {
    usb_cdc_send_string("[ERR] No Micro SD found! Plug it in and reset MCU.");
  }

  // Open file.
  if (sdm_st.is_sd_mounted) {
    sdm_st.is_file_opened =
        f_open_append_with_retry(&fm_file, sdm_st.file_path);
  }

  HAL_UART_Receive_DMA(&DBG_UART, dbg_log_buf1, DBG_UART_BUF_SIZE);

  static uint32_t last_byte_count = 0;

  sdm_st.file_end_ptr = f_tell(&fm_file);
  uint32_t rtc_now = get_rtc_timestamp();
  uint32_t tmp_rtc = rtc_now; // FIXME: debug purpose only
  static uint8_t is_ul_packet_sent = False;

  while (
      !(IS_BUTTON1_PRESSED) &&
      (rtc_now <=
       tmp_rtc + COLLECT_DATA_TIMEOUT)) { // TODO: update this to UE PSM flag.

    sdm_st.sd_res = 0;
    sdm_st.need_block_rewrite = False;    // reset
    sdm_st.fix_sd_code = SD_NEED_NOTHING; // reset every round

    // Write DBG log to file
    if (sdm_st.is_sd_mounted and sdm_st.is_file_opened) {
      if (dbg_log_buf_ready) { // ==1 or ==2
        // Benchmark write time BEGIN
        HAL_GPIO_WritePin(GPIO_2_GPIO_Port, GPIO_2_Pin, GPIO_PIN_SET);
        sdm_st.file_end_ptr = f_tell(&fm_file); // record before writing block
        if (1 == dbg_log_buf_ready) {
          sdm_st.sd_res = f_write(&fm_file, dbg_log_buf1, DBG_UART_BUF_SIZE,
                                  (void *)&f_w_cnt);
          // f_sync(&fm_file);
        } else if (2 == dbg_log_buf_ready) {
          sdm_st.sd_res = f_write(&fm_file, dbg_log_buf2, DBG_UART_BUF_SIZE,
                                  (void *)&f_w_cnt);
          // f_sync(&fm_file);
        } else {
          usb_cdc_send_string("[ERR] Unknown DBG BUF #.\n");
        }
        dbg_log_buf_ready = 0; // reset the flag
        // Benchmark write time END
        HAL_GPIO_WritePin(GPIO_2_GPIO_Port, GPIO_2_Pin, GPIO_PIN_RESET);

        // Deal with return code
        (0 == sdm_st.sd_res) ? sdm_st.consecutive_zero_cnt++
                             : sdm_st.cumulative_fatfs_io_error++;

        // Reset zero counter, show how many continuous write success in ().
        sdio_show_success_count_and_io_error();

        // Error handler - zero-block occurs, open file and overwrite the
        // block.
        if (1 == sdm_st.sd_res or 2 == sdm_st.sd_res or 9 == sdm_st.sd_res) {
          sdm_st.fix_sd_code = SD_NEED_REOPEN_FIX_BLOCK;
          sdm_st.need_block_rewrite = True;
        }

        // Error handler - continuous 2 occurs
        if (sdm_st.cumulative_fatfs_io_error >= MAX_FATFS_ALLOWED_ERROR) {
          sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
        }
      }
    } else {
      g_tm_st.error_code_this_run = (uint8_t)TASK_ERR_SDIO_TOO_MANY_ERRORS;
      if (!sdm_st.is_file_opened) {
        usb_cdc_send_string("[ERR] File not opened, go to REOPEN option\n");
        sdm_st.fix_sd_code = SD_NEED_REOPEN_APPEND;
      }
      if (!sdm_st.is_sd_mounted) {
        // higher priority, override the above one.
        usb_cdc_send_string("[ERR] SD not mounted, go to REMOUNT option\n");
        sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
      }
    }

    // Fix error if there is any above.
    sd_card_fixing_routine();

    if (sdm_st.need_block_rewrite) {
      // Write again after reopen file and lseek size(file)-512
      if (1 == dbg_log_buf_ready) {
        sdm_st.sd_res = f_write(&fm_file, dbg_log_buf1, DBG_UART_BUF_SIZE,
                                (void *)&f_w_cnt);
        // f_sync(&fm_file);
      } else if (2 == dbg_log_buf_ready) {
        sdm_st.sd_res = f_write(&fm_file, dbg_log_buf2, DBG_UART_BUF_SIZE,
                                (void *)&f_w_cnt);
        // f_sync(&fm_file);
      } else {
        usb_cdc_send_string("[ERR] Unknown DBG BUF #.\n");
      }
      (0 == sdm_st.sd_res) ? sdm_st.consecutive_zero_cnt++
                           : sdm_st.cumulative_fatfs_io_error++;
    }

    // Display received bytes:
    if ((dbg_log_byte_cnt % 10240 == 1) and
        (last_byte_count != dbg_log_byte_cnt)) {
      char dbg_log_kb_cnt_disp[15] = {'\0'};

      float dbg_log_kb_cnt = (float)dbg_log_byte_cnt / 1024;

      dy_ftoa(dbg_log_kb_cnt, dbg_log_kb_cnt_disp);
      dy_shift_leading_null_chars(dbg_log_kb_cnt_disp);
      dy_append_newline(dbg_log_kb_cnt_disp);
#if HAS_DISPLAY
      strcpy(dbg_log_reading_ppl_page.line4, dbg_log_kb_cnt_disp);
      ssd1306_display_whole_screen(dbg_log_reading_ppl_page);
#endif
#if HAS_USB_CDC_VCP
      export_one_field("kByte cnt: ", dbg_log_kb_cnt_disp);
      if (dbg_log_block_ready_flag) {
        CDC_Transmit_FS(sdio_write_buf, SD_BLOCK_SIZE * SD_NUM_BLOCKS);
        dbg_log_block_ready_flag = 0;
      }
#endif
      last_byte_count = dbg_log_byte_cnt;
    }
    rtc_now = get_rtc_timestamp();

    // Send the UL packet after one cycle of the current sensing.
    if (!is_ul_packet_sent) {
      // IMPORTANT: make sure this is executed for only once.
      mod_send_field_test_pack(CMD);
      is_ul_packet_sent = True;
    }
  }

  // While loop broke, close file
  sdm_st.sd_res = f_close_with_retry(&fm_file);
  // TODO: get the timestamp from the network and update this.
  f_set_timestamp(sdm_st.file_path, 2020, 1, 9, 17, 28, 12);
  usb_cdc_send_string("[INFO] Debug log collecting pipeline ended.\n");
}

/***************************************************************************/

void ul_transmission_current_sensing_to_sd_pipeline(void) {
  usb_cdc_send_string("[INFO] Begin of i_ultx pipeline\n");

  INA226_setConfig(INA226_MODE_CONT_SHUNT_VOLTAGE | INA226_VSH_140uS |
                   INA226_AVG_1);
  INA226_setCalibrationReg(
      g_bcm_st.current_calibration_value.value); // important!

  if (STATE_PPL_CURRENT_SENSING_TO_SD == work_mode) {
    eeprom_element_t dev_file_cnt = {0x3FF0, 0, 2};
    eeprom_read_one_element(&dev_file_cnt);
    char dev_file_id[4] = "";
    dy_itoa_with_leading_0(dev_file_cnt.value, 4, dev_file_id);
    // Compared to current ppl, the dev_file_cnt.value is not ++ here.
    // Override the file name in develop mode.
    strcpy(file_path_field_st.node_id, "Dev");
    strcpy(file_path_field_st.test_id, "7775");
    strcpy(file_path_field_st.packet_index, dev_file_id);
    export_one_field("[INFO] Log file id: ", dev_file_id);

    usb_cdc_send_string("[INFO] Develop mode. Press SW2 to begin\n");
    while (!(IS_BUTTON2_PRESSED)) {
    } // only in debug mode.
  }
  strcpy(file_path_field_st.i_d_indicator, "ITX");
  generate_log_file_name(sdm_st.file_path);

  // Mount SD card if it is not mounted.
  if (!sdm_st.is_sd_mounted) {
    sdm_st.is_sd_mounted = f_mount_with_retry();
  }
  if (!sdm_st.is_sd_mounted) {
    usb_cdc_send_string("[ERR] No Micro SD found! Plug it in and reset MCU.");
  }

  // Open file.
  if (sdm_st.is_sd_mounted and !sdm_st.is_file_opened) {
    sdm_st.is_file_opened =
        f_open_append_with_retry(&fm_file, sdm_st.file_path);
  }

  // Note: take 20kB RAM == 10k data samples => 1.280 seconds.
  uint16_t i_ultx_buf[ULTX_CURRENT_POINT_1K * 1024] = {0};

  uint16_t file_header[8] = {0};
  file_header[0] = 0xa937; // Let sublime text open as hexdecimal

  file_header[1] = HAL_GetTick() & 0xFFFF; // start time.

  HAL_GPIO_WritePin(GPIO_3_GPIO_Port, GPIO_3_Pin, GPIO_PIN_SET);
  // Collect samples as fast as possible.
  for (uint16_t i = 0; i < 10 * 1024; ++i) {
    i_ultx_buf[i] = INA226_getCurrentReg();
  }
  HAL_GPIO_WritePin(GPIO_3_GPIO_Port, GPIO_3_Pin, GPIO_PIN_RESET);
  file_header[2] = HAL_GetTick() & 0xFFFF; // end time.

  // Write header.
  f_write(&fm_file, file_header, 16, (void *)&f_w_cnt);

  // From RAM to SD card.
  usb_cdc_send_string("ULTX current to SD: ");

  uint8_t *i_buf_ptr = &i_ultx_buf;
  for (uint16_t j = 0; j < ULTX_CURRENT_POINT_1K * 2 * 1024 / 512;
       j++) { // j=0...19

    // Reset the flags every round
    sdm_st.fix_sd_code = SD_NEED_NOTHING;
    sdm_st.sd_res = 0;
    sdm_st.need_block_rewrite = False;

    if (sdm_st.is_sd_mounted and sdm_st.is_file_opened) {
      sdm_st.file_end_ptr = f_tell(&fm_file);

      HAL_GPIO_WritePin(GPIO_2_GPIO_Port, GPIO_2_Pin, GPIO_PIN_SET);

      sdm_st.sd_res = f_write(&fm_file, i_buf_ptr, 512, (void *)&f_w_cnt);

      // Export result.
      char res[2] = "";
      res[0] = sdm_st.sd_res + '0';
      usb_cdc_send_string(res);
    } else {
      // Not mounted or not open
      g_tm_st.error_code_this_run = (uint8_t)TASK_ERR_SDIO_TOO_MANY_ERRORS;
      if (!sdm_st.is_file_opened) {
        usb_cdc_send_string("[ERR] File not opened, go to REOPEN option\n");
        sdm_st.fix_sd_code = SD_NEED_REOPEN_APPEND;
      }
      if (!sdm_st.is_sd_mounted) {
        // higher priority, override the above one.
        usb_cdc_send_string("[ERR] SD not mounted, go to REMOUNT option\n");
        sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
      }
    }

    // Fix error if there is any above.
    sd_card_fixing_routine();

    if (sdm_st.need_block_rewrite) { // assume mounted+opened
      // Write again
      sdm_st.sd_res =
          f_write(&fm_file, i_ultx_buf + 512 * j, 512, (void *)&f_w_cnt);

      (0 == sdm_st.sd_res) ? sdm_st.consecutive_zero_cnt++
                           : sdm_st.cumulative_fatfs_io_error++;
      sdm_st.need_block_rewrite = False;
    }
    i_buf_ptr += 512;
  }

  // Close file
  sdm_st.sd_res = f_close_with_retry(&fm_file);
  // TODO: get the timestamp from the network and update this.
  f_set_timestamp(sdm_st.file_path, 2020, 1, 8, 17, 28, 12);
  usb_cdc_send_string("[INFO] End of i_ultx pipeline\n");
}

/***************************************************************************/

void board_meta_io_pipeline(void) {

  SSD1306_screen_text_t board_meta_io_ppl_page;

  strcpy(board_meta_io_ppl_page.line1, "META IO\n");
  strcpy(board_meta_io_ppl_page.line2, "W first, then R\n");
  strcpy(board_meta_io_ppl_page.line3, "SW1 to W\n");
  strcpy(board_meta_io_ppl_page.line4, "SW2 to R\n");
#if HAS_DISPLAY
  ssd1306_display_whole_screen(board_meta_io_ppl_page);
#endif
  // Pipeline starts
  uint8_t w_return_code = 0;
  uint8_t r_return_code = 0;

  while (!(IS_BUTTON1_PRESSED)) {
  };
  w_return_code = eeprom_write_board_constant_meta_struct(
      &g_bcm_st); // this function should be
                  // called for only ONCE.
  w_return_code += eeprom_write_board_variable_meta_struct(&g_bvm_st);

#if HAS_USB_CDC_VCP
  char ret_disp[2] = "";
  ret_disp[0] = w_return_code + '0';
  export_one_field("BCM EEPROM write result: ", ret_disp);
#endif

  while (!(IS_BUTTON2_PRESSED)) {
  };

  r_return_code = eeprom_read_board_constant_meta_struct(&g_bcm_st);
  r_return_code = eeprom_read_board_variable_meta_struct(&g_bvm_st);
#if HAS_USB_CDC_VCP
  ret_disp[0] = r_return_code + '0';
  export_one_field("BCM EEPROM read result: ", ret_disp);
#endif

  process_board_constant_meta(&g_bcm_st);
  process_board_variable_meta(&g_bvm_st);

  export_bcm_to_usb_vcp(&g_bcm_st);
  export_bvm_to_usb_vcp(&g_bvm_st);

  while (1) {
    HAL_Delay(100);
  }; // Do nothing.
}

/***************************************************************************/

void load_meta_and_task_from_eeprom(void) {
  // The write part is for debug purpose, don't enable it in actual running.
  const uint8_t need_writing_flag = 0;
  char ret_code[4] = {0};
  if (need_writing_flag) {
    while (!(IS_BUTTON2_PRESSED)) {
    }

    ret_code[0] = eeprom_write_board_constant_meta_struct(&g_bcm_st);
    ret_code[1] = eeprom_write_board_variable_meta_struct(&g_bvm_st);
    ret_code[2] = eeprom_write_task_monitor_struct(&g_eeprom_tm_st);
    for (uint8_t ii = 0; ii < 3; ++ii) {
      ret_code[ii] += '0';
    }
    export_one_field("EEPROM task writing results: ", ret_code);
  }

  /* while(!(IS_BUTTON1_PRESSED)){} */
  ret_code[0] = eeprom_read_board_constant_meta_struct(&g_bcm_st);
  ret_code[1] = eeprom_read_board_variable_meta_struct(&g_bvm_st);
  ret_code[2] = eeprom_read_task_monitor_struct(&g_eeprom_tm_st);
  for (uint8_t ii = 0; ii < 3; ++ii) {
    ret_code[ii] += '0';
  }

  export_one_field("EEPROM task loading results: ", ret_code);

  process_board_constant_meta(&g_bcm_st);
  process_board_variable_meta(&g_bvm_st);
  process_eeprom_task_monitor(&g_eeprom_tm_st);

#if HAS_USB_CDC_VCP
  export_bcm_to_usb_vcp(&g_bcm_st);
  export_bvm_to_usb_vcp(&g_bvm_st);
  export_tm_to_usb_vcp(&g_eeprom_tm_st); // no input is needed.
#endif
}

/***************************************************************************/

void task_assignment_pipeline(void) {

  usb_cdc_send_string("Step: Task not assigned, press SW1 3 times to start\n");
  LED0_ON;
  LED1_OFF;

  uint8_t wait_count = 0;
  const uint8_t ENABLE_AUTO_SLEEP = True;
  while (!proceed_to_init_packet_flag) {
    // Press SW1 3 times to start.
    LED0_TOGGLE;
    LED1_TOGGLE;
    HAL_Delay(500);
    wait_count += 1;
    if (wait_count > 120 and ENABLE_AUTO_SLEEP) { // 60 seconds
      usb_cdc_send_string("[INFO] No action, Go to STANBY to save power\n");

      switch (e_module_type) {
      case BG96:
        mod_send_cmd("AT+QPOWD=0\r\n");
        HAL_Delay(1500);
        break;
      case BC66:
        mod_send_cmd("AT+QPOWD=0\r\n");
        break;
      case SARAR410M02B:
        mod_send_cmd("AT+CPWROFF\r\n");
        break;
      }
      config_rtc_standby_auto_wakeup_after(3600); // sleep 600 s, long time.
      // Note: reset the module to start another test.
      HAL_PWR_EnterSTANDBYMode();
    }
  }

  proceed_to_init_packet_flag = 0;
  emit_field_test_start_signal();

  // Xianghui
  usb_cdc_send_string("[INFO] Send init packet\n");
  get_init_pack();

  usb_cdc_send_string("[INFO] Write config to EEPROM\n");
  /* update_eeprom_task_monitor(); */
  // DY: already updated at the end of get_init_pack();
  eeprom_write_task_monitor_struct(&g_eeprom_tm_st);
  // 2020-01-02

  // Enter STANTBY Mode (lowest power, =shutdown)
  usb_cdc_send_string("[INFO] Goto STANDBY\n");
  config_rtc_standby_auto_wakeup_after(2);
  HAL_PWR_EnterSTANDBYMode();
}

/***************************************************************************/

void field_test_control_pipeline(void) {

  LED0_ON;
  LED1_OFF;
  char CMD[600] = {""};
  g_tm_st.error_code_this_run =
      (uint8_t)TASK_ERR_NO_ERR; // update this if error occurs.

  usb_cdc_send_string("Step: Run field test control pipeline\n");
  /* HAL_Delay(1000); */

  // static uint8_t pseudo_packet_index = 0;
  if (g_tm_st.packet_index <= g_tm_st.ul_total_packet) {
    // Send 6 packets as example.
    char pid_exp[3] = "";
    dy_itoa_with_leading_0(g_tm_st.packet_index, 3, pid_exp);
    export_one_field("FT: PacketID ", pid_exp);

    g_tm_st.packet_sending_time_stamp = get_rtc_timestamp();

    /* The core here */
    usb_cdc_send_string("FT: send packet\n");
    send_test_pack(); // send field test pack

    LED0_OFF;
    LED1_ON;

    /* HAL_Delay(5000); */
#if HAS_SD_CARD_IO
    if (g_tm_st.collect_dbg_log_flag) {
      dbg_log_to_sd_pipeline(CMD);
    } else {
      current_sensing_to_sd_pipeline(CMD);
    }
#endif
    usb_cdc_send_string("FT: I/D pipeline ends, go to STANDBY\n");

    /*parse ul pack result for field test*/
    parse_at_result(SEND_PACK);
    if (ul_success_flag) {
      usb_cdc_send_string("FT: Sent UL Packet ok\n");
    } else {
      g_tm_st.error_code_this_run =
          (uint8_t)TASK_ERR_PACKET_NOT_TRANSMITTED_BAD_SIGNAL;
      usb_cdc_send_string("FT: Sent UL Packet failed \n");
    }
  } else {
    // End of test
    usb_cdc_send_string(
        "Step: field test finished\n, set flag to unassigned, go to sleep\n");
    /* update_task_monitor_end_of_run(); */
    g_tm_st.is_task_assigned_flag = 0;
    g_tm_st.packet_index = 0; // reset the packet idx
  }

  // TODO: check module enter PSM

  // Check whether user terminated the task.
  if (1 == terminate_task_flag) {
    usb_cdc_send_string("XXX: The task is terminated by the user. Set task "
                        "assigned to 0. Go to STANDBY\n");
    emit_field_test_terminate_signal();
    terminate_task_flag = 0;
    // g_eeprom_tm_st.is_task_assigned.value = 0;
    g_tm_st.is_task_assigned_flag = 0;
    g_tm_st.packet_index = 0; // reset the packet idx
    g_tm_st.e_task_status = TASK_TERMINATED_BY_USER;
    g_tm_st.error_code_this_run = (uint8_t)TASK_TERMINATED_BY_USER;
  }

  usb_cdc_send_string("FT: write config to EEPROM\n");
  update_eeprom_task_monitor();
  eeprom_write_task_monitor_struct(&g_eeprom_tm_st);
  eeprom_write_board_variable_meta_struct(&g_bvm_st);

  LED0_OFF;
  LED1_OFF;

  // Execute some commands for some modules before sleep.
  post_run_module_control();

  usb_cdc_send_string("FT: Goto STANDBY \n");
  // TODO: update bvm_st timestamp with AT+CCLK.
  config_rtc_standby_auto_wakeup_after(g_eeprom_tm_st.mcu_sleep_timer.value);
  HAL_PWR_EnterSTANDBYMode();
}

/***************************************************************************/

void develop_override_loaded_results_from_eeprom(void) {
  usb_cdc_send_string("Task monitor override at DY's side\n");
  usb_cdc_send_string("Press SW1 to override\n");
  while (!(IS_BUTTON1_PRESSED)) {
  }

  load_meta_and_task_from_eeprom();
  e_module_type = BC28;
  g_tm_st.is_task_assigned_flag = True;
  g_tm_st.packet_index = 001;
  g_tm_st.ul_total_packet = 300;
  g_tm_st.test_id = 777;
  g_tm_st.application_type = 4;
  g_tm_st.collect_dbg_log_flag = 1;
  g_tm_st.ul_packet_size = 256;
  g_tm_st.mcu_sleep_timer = 5;
  g_tm_st.e_test_mode = MODE_PACKET_NUM_LIMIT;
  update_eeprom_task_monitor();
  g_eeprom_tm_st.test_id.value = 777;
  eeprom_write_task_monitor_struct(&g_eeprom_tm_st);
  usb_cdc_send_string("Task Monitor updated in EEPROM\n");
  load_meta_and_task_from_eeprom();
  while (1) {
  }
}
