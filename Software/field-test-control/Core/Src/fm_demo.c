/**
   @file fm_demo.c
   @author Deliang Yang
   @date_created 2020.01.09
   @last_update N/A
   @version 0.1
   @brief Implementation of the demo functions
*/

#include "fm_demo.h"

uint8_t demo_header_sent_cnt = 0; // private local variable.

void run_demos(uint8_t demo_choice) {

  usb_cdc_send_string("[INFO] Demo BEGIN\n");

  if (0 == demo_choice or 255 == demo_choice) {
    run_demo0_led_blinking();
  }

  if (1 == demo_choice or 255 == demo_choice) {
    run_demo1_ssd1306_test();
  }

  if (2 == demo_choice) {
    run_demo2_btn_led_no_exti();
  }

  if (3 == demo_choice or 255 == demo_choice) {
    run_demo3_btn_led_exti();
  }

  if (4 == demo_choice or 255 == demo_choice) {
    run_demo4_temp_humd_sensing();
  }

  if (5 == demo_choice or 255 == demo_choice) {
    run_demo5_eeprom_sleep_wakeup();
  }

  if (6 == demo_choice or 255 == demo_choice) {
#if HAS_SD_CARD_IO
    run_demo6_tf_card_rw();
#else
    usb_cdc_send_string("[WRN] SD IO disabled.");
#endif
  }

  if (7 == demo_choice or 255 == demo_choice) {
    run_demo7_v_batt_sensing();
  }

  if (8 == demo_choice or 255 == demo_choice) {
    run_demo8_i_bus_sensing();
  }

  if (9 == demo_choice or 255 == demo_choice) {
    run_demo9_main_uart_dma();
  }

  if (10 == demo_choice or 255 == demo_choice) {
    run_demo10_read_debug_log();
  }

  if (128 == demo_choice or 254 == demo_choice) {
  }

  HAL_Delay(300);
  usb_cdc_send_string("[INFO] Demo END\n");
}

void run_demo0_led_blinking() {

  // Demo 0: LED blinking

  SSD1306_screen_text_t demo0_page;
  strcpy(demo0_page.line1, "Demo 0\n");
  strcpy(demo0_page.line2, "LED Blinking\n");
  strcpy(demo0_page.line3, "Blink 10 times\n");
  strcpy(demo0_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo0_page);
#endif
  if (demo_header_sent_cnt < MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo0_page.line1);
    usb_cdc_send_string(demo0_page.line2);
    usb_cdc_send_string(demo0_page.line3);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
  LED0_OFF;
  LED1_OFF;
  for (int8_t i = 0; i < 20; i++) {
    // repeat 20 times = flash 10 times
    LED0_TOGGLE;
    LED1_TOGGLE;
    HAL_Delay(350);
  }
  LED0_OFF;
  LED1_OFF;
}

void run_demo1_ssd1306_test() {

  // Demo 1: OLED (or LCD) display testing

  SSD1306_screen_text_t demo1_page;

  strcpy(demo1_page.line1, "Demo 1\n");
  strcpy(demo1_page.line2, "OLED screen test\n");
  strcpy(demo1_page.line3, "FPS+boarder+font\n");
  strcpy(demo1_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo1_page);
  HAL_Delay(2500);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo1_page.line1);
    usb_cdc_send_string(demo1_page.line2);
    usb_cdc_send_string(demo1_page.line3);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
#if HAS_DISPLAY
  ssd1306_TestAll();
  HAL_Delay(2000);
#endif
}

void run_demo2_btn_led_no_exti() {

  // Demo 2: LED controlled by buttons, need to set demo_choice=2 exactly to
  // run.
  SSD1306_screen_text_t demo2_page;

  strcpy(demo2_page.line1, "Demo 2\n");
  strcpy(demo2_page.line2, "Btns control LED\n");
  strcpy(demo2_page.line3, "Press SW1 or SW2\n");
  strcpy(demo2_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo2_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo2_page.line1);
    usb_cdc_send_string(demo2_page.line2);
    usb_cdc_send_string(demo2_page.line3);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
  HAL_NVIC_DisableIRQ(EXTI0_IRQn);
  HAL_NVIC_DisableIRQ(EXTI1_IRQn);

  HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin,
                    HAL_GPIO_ReadPin(BUTTON1_GPIO_Port, BUTTON1_Pin));
  HAL_GPIO_WritePin(LED1_GPIO_Port, LED1_Pin,
                    HAL_GPIO_ReadPin(BUTTON2_GPIO_Port, BUTTON2_Pin));
}

void run_demo3_btn_led_exti() {

  // Demo 3: Use button to control LED, with external interruption.
  // Print out demo info.
  SSD1306_screen_text_t demo3_page;

  strcpy(demo3_page.line1, "Demo 3\n");
  strcpy(demo3_page.line2, "Btn -> LED, EXTI\n");
  strcpy(demo3_page.line3, "Press SW1 or SW2\n");
  strcpy(demo3_page.line4, "(10 seconds)\n");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo3_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo3_page.line1);
    usb_cdc_send_string(demo3_page.line2);
    usb_cdc_send_string(demo3_page.line3);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
  HAL_NVIC_EnableIRQ(EXTI0_IRQn);
  HAL_NVIC_EnableIRQ(EXTI1_IRQn);
  HAL_Delay(10000);
  HAL_NVIC_DisableIRQ(EXTI0_IRQn);
  HAL_NVIC_DisableIRQ(EXTI1_IRQn);
  /* no code here. write it in the GPIO_EXTI_IRQHandler() in
  stm32f1xx_it.c or re-implement HAL_GPIO_EXTI_Callback() */
}

void run_demo4_temp_humd_sensing() {

  // Demo 4: Temperature and relative humidity sensing.
  // Print out demo info.
  SSD1306_screen_text_t demo4_page;

  strcpy(demo4_page.line1, "Demo 4\n");
  strcpy(demo4_page.line2, "Temp/Humd Sensing\n");
  strcpy(demo4_page.line3, "SW2 to start\n");
  strcpy(demo4_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo4_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo4_page.line1);
    usb_cdc_send_string(demo4_page.line2);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  // Demo START
  si7021_init();
  volatile float rh;
  volatile float temperature;
  volatile float temperature1;

  HAL_Delay(5); // make sure the init function works well.

  while (!(IS_BUTTON2_PRESSED)) {
    // press SW2 to run.
  }
  /* volatile uint8_t si7021_fm_version; */
  /* si7021_fm_version = si7021_get_firmware_version(); */
  while (!(IS_BUTTON1_PRESSED)) {
    rh = si7021_get_rh();
    temperature = si7021_read_previous_temp();
    temperature1 = si7021_get_temperature();

    char temp_string[ITOA_BUF_LEN] = {'\0'};
    char rh_string[ITOA_BUF_LEN] = {'\0'};
    char temp1_string[ITOA_BUF_LEN] = {'\0'};

    dy_ftoa(temperature, temp_string);
    dy_ftoa(rh, rh_string);
    dy_ftoa(temperature1, temp1_string);

    char temp_disp[18] = "Temp: ";
    // 18 is the longest string that 128 px can hold.
    char rh_disp[18] = "Humd: ";

    dy_cancat_sensor_string(temp_disp, 6, temp1_string);
    dy_cancat_sensor_string(rh_disp, 6, rh_string);

    dy_append_newline(temp_disp);
    dy_append_newline(rh_disp);

    strcpy(demo4_page.line3, temp_disp);
    strcpy(demo4_page.line4, rh_disp);

#if HAS_DISPLAY
    ssd1306_display_whole_screen(demo4_page);
#endif

    usb_cdc_send_string(demo4_page.line3); // sensor reading.
    usb_cdc_send_string(demo4_page.line4);
    HAL_Delay(1000);
  }
}

void run_demo5_eeprom_sleep_wakeup() {

  // Demo 5: Sleep and wakeup, Store the parameters in the EEPROM.
  // Print out demo info.
  SSD1306_screen_text_t demo5_page;

  strcpy(demo5_page.line1, "Demo 5\n");
  strcpy(demo5_page.line2, "Sleep and Wake up\n");
  strcpy(demo5_page.line3, "RTT + EEPROM\n");
  strcpy(demo5_page.line4, "SW1 to skip\n");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo5_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo5_page.line1);
    usb_cdc_send_string(demo5_page.line2);
    usb_cdc_send_string(demo5_page.line3);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  // Demo START
#if IN_DEVELOPMENT
  /* while (!(IS_BUTTON2_PRESSED)) { */
  /*   // press SW2 to run. */
  /* } */
#endif

  static uint32_t demo_wake_up_count = 0;
  uint8_t demo_wake_up_count_arr[4] = {0, 0, 0, 0}; // byte, not ascii
  char sent_str[27] = "Wkup cnt: ";
  char count_str[ITOA_BUF_LEN] = {'\0'};
  uint16_t rw_addr = 0x0400;

  const uint8_t sub_program_choice = 0; /*!< Select code snippet */

  switch (sub_program_choice) {
  case 0:
    while (True) {
      eeprom_read_4_bytes(EEPROM_DEMO_ADDRESS_START, demo_wake_up_count_arr);
      demo_wake_up_count = dy_int8_arr_to_int32(demo_wake_up_count_arr);
      if (-1 == demo_wake_up_count) {
        // initialization
        demo_wake_up_count = 1;
      } else {
        demo_wake_up_count += 1;
      }
      // Write back to the EEPROM again.
      dy_int32_to_byte_array(demo_wake_up_count, demo_wake_up_count_arr);
      eeprom_write_4_bytes(EEPROM_DEMO_ADDRESS_START, demo_wake_up_count_arr);

      dy_itoa(demo_wake_up_count, count_str);
      dy_cancat_sensor_string(sent_str, 10, count_str);
      dy_append_newline(sent_str);

      strcpy(demo5_page.line4, sent_str);
      ssd1306_display_whole_screen(demo5_page);
      usb_cdc_send_string(sent_str);

      // Put the MCU into STANDBY mode.
      usb_cdc_send_string("[PWR] Enter STANDBY after 3 seconds\n");
      usb_cdc_send_string("Press SW1 to skip this loop\n");

      emit_field_test_start_signal();
      uint16_t delay_round_cnt = 0;
      while (delay_round_cnt < 100) {
        HAL_Delay(30);
        delay_round_cnt += 1;
        if (IS_BUTTON1_PRESSED) {
          delay_round_cnt = 999;
        }
      }
      if (999 == delay_round_cnt) {
        break;
      }
      emit_field_test_start_signal();
      /* HAL_Delay(3000); */
      config_rtc_standby_auto_wakeup_after(8);
      // Enter STANTBY Mode (lowest power, = shutdown)
      HAL_PWR_EnterSTANDBYMode();
      /* This is the end of this routine. **********************************/
      break; // exit while 1 loop (actually not possible because it slept.)
    }
    emit_field_test_terminate_signal();
    LED0_ON;
    LED1_ON;
    HAL_Delay(50);
    break;
  case 1:
    // Read the value in the address one by one.
    usb_cdc_send_string("START\n");
    for (int i = 0; i < 6; ++i) {
      eeprom_read_4_bytes(rw_addr, demo_wake_up_count_arr);
      for (uint8_t j = 0; j < 4; ++j) {
        uint8_t ch = demo_wake_up_count_arr[j] + '0';
        CDC_Transmit_FS(&ch, 1);
        HAL_Delay(10);
      }
      rw_addr += 4;
      HAL_Delay(200);
    }
    break;
  case 2:
    // Read, write, read
    rw_addr = EEPROM_BCM_ADDR_START;
    usb_cdc_send_string("Read 1 page\n");
    for (int i = 0; i < 16; ++i) {
      eeprom_read_4_bytes(rw_addr, demo_wake_up_count_arr);
      for (uint8_t j = 0; j < 4; ++j) {
        uint8_t ch = demo_wake_up_count_arr[j] + '0';
        CDC_Transmit_FS(&ch, 1);
        HAL_Delay(10);
      }
      rw_addr += 4;
    }

    rw_addr = EEPROM_BCM_ADDR_START;
    usb_cdc_send_string("Update 1 page\n");
    for (int i = 0; i < 16; ++i) {
      memset(demo_wake_up_count_arr, 0x36, 4);
      eeprom_write_4_bytes(rw_addr, demo_wake_up_count_arr);
      rw_addr += 4;
      HAL_Delay(10);
    }

    rw_addr = EEPROM_BCM_ADDR_START;
    usb_cdc_send_string("Page update done. Read 1 page\n");
    for (int i = 0; i < 16; ++i) {
      eeprom_read_4_bytes(rw_addr, demo_wake_up_count_arr);
      for (uint8_t j = 0; j < 4; ++j) {
        uint8_t ch = demo_wake_up_count_arr[j] + '0';
        CDC_Transmit_FS(&ch, 1);
        HAL_Delay(10);
      }
      rw_addr += 4;
    }
    HAL_Delay(50);
    break;
  default:
    break;
  }

  /*
  // utils function test. Passed, commented here.
  uint16_t test1 = 65234;
  uint32_t test2 = 0x12abcdef;
  uint8_t test1_buf[2] = {0, 0};
  uint8_t test2_buf[4] = {0, 0, 0, 0};
  dy_int16_to_byte_array(test1, test1_buf);
  dy_int32_to_byte_array(test2, test2_buf);
  volatile uint16_t reverse_test1 = 0;
  reverse_test1 = dy_int8_arr_to_int16(test1_buf);
  volatile uint32_t reverse_test2 = 0;
  reverse_test2 = dy_int8_arr_to_int32(test2_buf);
  */

  // FIXME: change to read 1 byte temporarily
  HAL_Delay(1000);
}

void run_demo6_tf_card_rw() {
  // Demo 6: TF card insertion detection. Use button to test file appending.

  static char tf_inserted_disp[17] = "TF inserted: N";
  static Bool last_det_state = True;
  Bool this_det_state = HAL_GPIO_ReadPin(TF_DET_GPIO_Port, TF_DET_Pin);
  Bool is_det_state_changed = False;
  if (this_det_state != last_det_state) {
    is_det_state_changed = True;
  }
  if (GPIO_PIN_RESET == this_det_state) {
    // Pin = 0, inserted; Pin = 1: no card detected.
    tf_inserted_disp[13] = 'Y';
  } else {
    tf_inserted_disp[13] = 'N';
  }
  tf_inserted_disp[14] = '\n';

  last_det_state = this_det_state;

  // Print out demo info.
  SSD1306_screen_text_t demo6_page;

  strcpy(demo6_page.line1, "Demo 6\n");
  strcpy(demo6_page.line2, "TF card I/O\n");
  strcpy(demo6_page.line3, tf_inserted_disp);
  strcpy(demo6_page.line4, "SW1: append txt\n");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo6_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo6_page.line1);
    usb_cdc_send_string(demo6_page.line2);
    usb_cdc_send_string(demo6_page.line3);
    usb_cdc_send_string(demo6_page.line4);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  if (is_det_state_changed) {
    usb_cdc_send_string(demo6_page.line3);
  }

  // Demo START
  while (!(IS_BUTTON2_PRESSED)) {
    // press SW2 to run.
  }

  while (!(IS_BUTTON1_PRESSED)) {
    // exit when BTN1 is pressed; append file when BTN2 is pressed.
    if (GPIO_PIN_RESET == HAL_GPIO_ReadPin(BUTTON2_GPIO_Port, BUTTON2_Pin)) {

      show_micro_sd_meta_info();

      // Test SD card erase.
      /* sd_erase_test(); */

      // R/W a block of texts.
      /* sd_write_read_test(); */
      /* sd_write_read_test_dma(); */

      // comment this out to reduce compilation time and hex size.
      fatfs_rw_demo();
      HAL_Delay(150);
    }
    HAL_Delay(500);
  }
}

void run_demo7_v_batt_sensing() {

  // Demo 7: Battery voltage sensing.
  SSD1306_screen_text_t demo7_page;

  strcpy(demo7_page.line1, "Demo 7\n");
  strcpy(demo7_page.line2, "Battery Voltage\n");
  strcpy(demo7_page.line3, "SW2 to start\n");
  strcpy(demo7_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo7_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo7_page.line1);
    usb_cdc_send_string(demo7_page.line2);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  // Demo START
  while (!(IS_BUTTON2_PRESSED)) {
    // press SW2 to run.
  }

  volatile float v_batt_reg = 0;
  volatile float v_batt = 0;
  HAL_ADCEx_Calibration_Start(&V_BATT_ADC);
  HAL_Delay(3);

  while (!(IS_BUTTON1_PRESSED)) {
    HAL_ADC_Start(&V_BATT_ADC);
    HAL_ADC_PollForConversion(&V_BATT_ADC, HAL_MAX_DELAY);
    HAL_Delay(15);
    v_batt_reg = HAL_ADC_GetValue(&V_BATT_ADC);
    HAL_ADC_Stop(&V_BATT_ADC);

    char v_batt_string[9] = {'\0'};         // for ftoa
    char v_batt_reg_string[9] = {'\0'};     // for ftoa
    char v_batt_disp[17] = "V_batt: ";      // for display
    char v_batt_reg_disp[17] = "V_b reg: "; // for reg_value display

    dy_itoa(v_batt_reg, v_batt_reg_string);

    v_batt = v_batt_reg * V_BATT_CONSTANT * V_BATT_DIVIDING_RATIO_INV_DEFAULT;
    dy_ftoa(v_batt, v_batt_string);

    // 18 is the longest string that 128 px can hold.
    dy_cancat_sensor_string(v_batt_reg_disp, 9, v_batt_reg_string);
    dy_append_newline(v_batt_reg_disp);

    dy_cancat_sensor_string(v_batt_disp, 8, v_batt_string);
    dy_append_newline(v_batt_disp);

    strcpy(demo7_page.line3, v_batt_disp);
#if HAS_DISPLAY
    ssd1306_display_whole_screen(demo7_page);
#endif
    usb_cdc_send_string(demo7_page.line3);
    usb_cdc_send_string(v_batt_reg_disp);
    HAL_Delay(1000);
  }
}

void run_demo8_i_bus_sensing() {

  // Demo 8: Current sensing test.
  SSD1306_screen_text_t demo8_page;

  strcpy(demo8_page.line1, "Demo 8\n");
  strcpy(demo8_page.line2, "Current sensing\n");
  strcpy(demo8_page.line3, "SW2 to start\n");
  strcpy(demo8_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo8_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo8_page.line1);
    usb_cdc_send_string(demo8_page.line2);
    usb_cdc_send_string(demo8_page.line3);
    usb_cdc_send_string(demo8_page.line4);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
  INA226_setConfig(INA226_MODE_CONT_SHUNT_AND_BUS | INA226_VBUS_204uS |
                   INA226_VSH_204uS | INA226_AVG_512);
  INA226_setCalibrationReg(INA226_CALIB_VAL); // important!
  // Note: INA226_CALIB_VAL(2778) is the reference for calibration.

  /* volatile uint16_t calib_reg = INA226_getCalibrationReg(); */

  volatile uint32_t c_data_point_cnt = 0;
  volatile float v_bus = 0;
  volatile float i_bus = 0;
  volatile uint16_t i_bus_reg = 0;

  while (!(IS_BUTTON2_PRESSED)) {
    // press SW2 to run.
  }
  strcpy(demo8_page.line3, "Point count:\n");

  while (!(IS_BUTTON1_PRESSED)) {
    // infinite loop until Button1 is pressed.

    i_bus_reg = INA226_getCurrentReg(); // get the current register reading
    i_bus = INA226_getCurrent();        // get the real current reading
    c_data_point_cnt++;

    if (c_data_point_cnt % 5000 == 0) {

      v_bus = INA226_getBusV(); // per 10k current measurement.
      char i_bus_disp[17] = {'\0'};
      char i_bus_reg_disp[17] = "";
      char v_bus_disp[17] = {'\0'};
      char dp_cnt_disp[17] = {'\0'};

      dy_ftoa(i_bus, i_bus_disp);
      dy_itoa(i_bus_reg, i_bus_reg_disp);
      dy_itoa(c_data_point_cnt, dp_cnt_disp);
      dy_ftoa(v_bus, v_bus_disp);

      dy_shift_leading_null_chars(v_bus_disp);
      dy_shift_leading_null_chars(i_bus_disp);
      dy_shift_leading_null_chars(i_bus_reg_disp);
      dy_shift_leading_null_chars(dp_cnt_disp);
#if HAS_DISPLAY
      strcpy(demo8_page.line4, dp_cnt_disp);
      ssd1306_display_whole_screen(demo8_page);
#endif
      export_one_field("#point cnt: ", dp_cnt_disp);
      export_one_field("I REG: ", i_bus_reg_disp);
      export_one_field("I actual: ", i_bus_disp);
      export_one_field("V BUS: ", v_bus_disp);
      usb_cdc_new_line();
    }
  }
  HAL_Delay(1000);
}

void run_demo9_main_uart_dma() {

  // Demo : IO between host PC and MCU.

  SSD1306_screen_text_t demo9_page;

  strcpy(demo9_page.line1, "Demo 9\n");
  strcpy(demo9_page.line2, "PC to Module\n");
  strcpy(demo9_page.line3, "Tx/Rx via VCP\n");
  strcpy(demo9_page.line4, "SW1=end SW2=P_K\n");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo9_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo9_page.line1);
    usb_cdc_send_string(demo9_page.line2);
    usb_cdc_send_string(demo9_page.line3);
    usb_cdc_send_string(demo9_page.line4);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }

  // Demo START
  __HAL_UART_ENABLE_IT(&MAIN_UART, UART_IT_IDLE); // idle interrupt

  // Reset the module
  module_reset(0);
  /* uint8_t at_test[] = "AT+CSQ\r\n"; */
  /* static uint32_t periodic_ati_timer = 0; */


  HAL_UART_Receive_DMA(&MAIN_UART, main_uart_rx_buf, MAIN_UART_BUF_SIZE);
  while (!(IS_BUTTON1_PRESSED)) {
    // Vanilla version

    /* if (periodic_ati_timer % 200 == 0) { */
    /*   HAL_UART_Transmit(&MAIN_UART, "ATI\r\n", sizeof("ATI\r\n"), 0xFF); */
    /* } */
    /* HAL_Delay(10); */
    /* periodic_ati_timer += 1; */

    /* HAL_UART_Receive(&MAIN_UART, main_uart_rx_buf, 10, 0xFF); */
    /* CDC_Transmit_FS(main_uart_rx_buf, 10); */
    /* HAL_Delay(100); */

    /* HAL_Delay(2000); */
    /* if (IS_BUTTON2_PRESSED) { */
    /*   // Manually power on the BC26/BC66 module. */
    /*   HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_SET);
     */
    /*   HAL_Delay(500); */
    /*   HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin,
     * GPIO_PIN_RESET);
     */
    /* } */

    if (IS_BUTTON2_PRESSED) {
      // Manually power on the BC26/BC66 module.
      HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_SET);
    } else {
      HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_RESET);
      HAL_Delay(5);
    }

    if (main_rx_complete_flag) {
      /* usb_cdc_send_string((char *)&main_uart_rx_buf); // or Transmit_FS */
      /* CDC_Transmit_FS((char *)&main_uart_rx_buf, main_rx_byte_cnt); */
      /* HAL_UART_Receive_DMA(&MAIN_UART, main_uart_rx_buf,
       * MAIN_UART_BUF_SIZE); */
      main_rx_complete_flag = 0;
    }
  }
  HAL_Delay(1000);
}

void run_demo10_read_debug_log() {
  // Demo 10: Read debug log from the UART (BC28). Send to host via USB CDC.
  SSD1306_screen_text_t demo10_page;

  strcpy(demo10_page.line1, "Demo 10\n");
  strcpy(demo10_page.line2, "Read in DGB log\n");
  strcpy(demo10_page.line3, "kB count:\n");
  strcpy(demo10_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demo10_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demo10_page.line1);
    usb_cdc_send_string(demo10_page.line2);
    usb_cdc_send_string(demo10_page.line3);
    usb_cdc_send_string(demo10_page.line4);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  load_meta_and_task_from_eeprom();
  while (!(IS_BUTTON2_PRESSED)) {
    // Press to start
  }

  HAL_UART_Receive_DMA(&DBG_UART, dbg_log_buf1, DBG_UART_BUF_SIZE);

  static uint32_t last_byte_count = 0;
  // TODO: enable DMA half transfer interrupt.
  while (!(IS_BUTTON1_PRESSED)) {
    // infinite loop until Button1 is pressed.

    if (dbg_log_buf_ready) { // ==1 or ==2
      if (1 == dbg_log_buf_ready) {
        CDC_Transmit_FS(dbg_log_buf1, DBG_UART_BUF_SIZE);
      } else if (2 == dbg_log_buf_ready) {
        CDC_Transmit_FS(dbg_log_buf2, DBG_UART_BUF_SIZE);
      } else {
        usb_cdc_send_string("[ERR] Unknown DBG BUF #.\n");
      }
      dbg_log_buf_ready = 0; // reset the flag
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
      strcpy(demo10_page.line4, dbg_log_kb_cnt_disp);
      ssd1306_display_whole_screen(demo10_page);
#endif
      usb_cdc_send_string("kByte cnt: ");
      usb_cdc_send_string(dbg_log_kb_cnt_disp);
      HAL_Delay(1);
      /* if (dbg_log_buf_choice == 1){ */
      /*   CDC_Transmit_FS(dbg_log_buf2, 1024); */
      /* } else if (dbg_log_buf_choice == 2){ */
      /*   CDC_Transmit_FS(dbg_log_buf1, 1024); */
      /* } */
      if (dbg_log_block_ready_flag) {
        CDC_Transmit_FS(sdio_write_buf, SD_BLOCK_SIZE * SD_NUM_BLOCKS);
        dbg_log_block_ready_flag = 0;
      }
      last_byte_count = dbg_log_byte_cnt;
    }
  }
  HAL_Delay(1000);
}

void demox_template() {

  // Demo : template.

  SSD1306_screen_text_t demox_page;
  strcpy(demox_page.line1, "Demo X\n");
  strcpy(demox_page.line2, " ");
  strcpy(demox_page.line3, " ");
  strcpy(demox_page.line4, " ");

#if HAS_DISPLAY
  ssd1306_display_whole_screen(demox_page);
#endif
  if (demo_header_sent_cnt <= MAX_DEMO_HEADER_REPETITION) {
    usb_cdc_send_string(demox_page.line1);
    usb_cdc_send_string(demox_page.line2);
    usb_cdc_send_string(demox_page.line3);
    usb_cdc_send_string(demox_page.line4);
    demo_header_sent_cnt += 1;
    if (demo_header_sent_cnt == MAX_DEMO_HEADER_REPETITION) {
      // Max repetition reached.
      usb_cdc_send_string("(Max number of header repetition reached.)\n");
    }
  }
  // Demo START

  // Demo END
  HAL_Delay(1000);
}
