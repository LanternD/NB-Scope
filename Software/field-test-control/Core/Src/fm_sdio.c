/**
   @file fm_sdio.c
   @brief Function implementation for SD card access, from basic erase, r/w,
   checking, to FATFS file organization.
 */

#include "fm_sdio.h"

uint8_t sdio_write_buf[SD_BLOCK_SIZE * SD_NUM_BLOCKS];
uint8_t sdio_read_buf[SD_BLOCK_SIZE * SD_NUM_BLOCKS];

FATFS sd_fs;   // FATFS file system object
FIL fm_file;   // file object
FRESULT f_res; // the return code of file operation

uint32_t f_r_cnt; // count of succeeded file IO
uint32_t f_w_cnt; // count of succeeded file IO
uint8_t file_str_test[] =
    "qwertyuiopasdfghjklzxcvbnm!\n";            // string to be written to file
uint8_t r_text_buf[100];                        // file read buf
char fm_file_path[] = "STM32Cube Test_DMA.txt"; // file path

// Used to keep track of the SDIO module for current sensing or dbg log
// recording pipeline.
sdio_monitor_t sdm_st = {FR_TIMEOUT, SD_NEED_NOTHING, 0, 0, 0, "", 0};

sd_test_state_t check_erased_buffer(uint32_t *p_buf, uint32_t buf_len) {
  while (buf_len--) {
    if (*p_buf != 0xFFFFFFFF && *p_buf != 0) {
      return FAILED;
    }
    p_buf++;
  }
  return PASSED;
}

void sd_erase_test(void) {
  sd_status =
      HAL_SD_Erase(&SD_HANDLER, SD_RW_TEST_ADDRESS,
                   SD_RW_TEST_ADDRESS + SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS);

  HAL_Delay(100);
  char status_char[2] = {sd_status + '0', '\n'};
  usb_cdc_send_string("[INFO] Erase operation status: ");
  usb_cdc_send_string(status_char);

  if (HAL_OK == sd_status) {
    // write succeeded, read them out
    sd_status = HAL_SD_ReadBlocks(&SD_HANDLER, (uint8_t *)sdio_read_buf,
                                  SD_RW_TEST_ADDRESS, SD_RW_TEST_NUM_BLOCKS,
                                  SD_OPERATION_TIMEOUT);
    HAL_Delay(100);
    status_char[0] = sd_status + '0';
    usb_cdc_send_string("[INFO] Read erased block status: ");
    usb_cdc_send_string(status_char);

    test_status = check_erased_buffer(sdio_read_buf, SD_RW_TEST_NUM_BLOCKS *
                                                         SD_RW_TEST_NUM_BLOCKS);

    if (PASSED == test_status) {
      usb_cdc_send_string("[INFO] Erase test passed!\n");
    } else {
      usb_cdc_send_string("[ERR] Erase test failed. Data mismatched.\n");
    }
  } else {
    usb_cdc_send_string("[ERR] Erase test failed. Part of the SD card does not "
                        "support erase. Please continue to the R/W test.\n");
  }
}

void fill_buffer(uint32_t *p_buf, uint32_t buf_len, uint32_t offset) {
  uint32_t index = 0;
  for (index = 0; index < buf_len; ++index) {
    p_buf[index] = index + offset;
  }
}

void fill_buffer_with_random_char(uint32_t *p_buf, uint32_t buf_len) {
  uint32_t index = 0;
  uint8_t count = 0;
  uint8_t rand;
  for (index = 0; index < buf_len; ++index) {
    rand = dy_rand(26); // 26 letters
    if (rand + count >= 26) {
      p_buf[index] = (rand + count) % 26 + 'a';
    } else {
      p_buf[index] = (rand + count) + 'a';
    }
    count += 1;
  }
}

sd_test_state_t compare_buffer(uint32_t *p_buf1, uint32_t *p_buf2,
                               uint32_t buf_len) {
  uint32_t i;
  usb_cdc_send_string("Sample (buf1/buf2): \n");
  for (i = 0; i < buf_len; ++i) {
    if (p_buf1[i] != p_buf2[i]) {
      return FAILED;
    }
    if (i % 100 == 0) {
      usb_cdc_send_string((char *)&p_buf1[i]);
      usb_cdc_send_string((char *)&p_buf2[i]);
      usb_cdc_send_string("\n");
    }
  }
  return PASSED;
}

void sd_write_read_test(void) {

  usb_cdc_send_string("[INFO] SD card RW test start.\n");
  char status_char[2] = {sd_status + '0', '\n'};

  // Add data to buffer
  /* fill_buffer(sdio_write_buf, SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS, 0x3456);
   */
  fill_buffer_with_random_char(sdio_write_buf,
                               SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS);

  // Write data to SD card
  sd_status = HAL_SD_WriteBlocks(
      &SD_HANDLER, (uint8_t *)sdio_write_buf, SD_RW_TEST_ADDRESS,
      USE_HAL_WWDG_REGISTER_CALLBACKS, SD_OPERATION_TIMEOUT);
  status_char[0] = sd_status + '0';
  usb_cdc_send_string("[INFO] Write blocks status: ");
  usb_cdc_send_string(status_char);

  HAL_Delay(100);

  // Read data from SD card
  sd_status = HAL_SD_ReadBlocks(&SD_HANDLER, (uint8_t *)sdio_read_buf,
                                SD_RW_TEST_ADDRESS, SD_RW_TEST_NUM_BLOCKS,
                                SD_OPERATION_TIMEOUT);
  status_char[0] = sd_status + '0';
  usb_cdc_send_string("[INFO] Read blocks status: ");
  usb_cdc_send_string(status_char);

  // Compare the R/W data
  test_status = compare_buffer(sdio_write_buf, sdio_write_buf,
                               SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS);

  HAL_Delay(10);
  if (PASSED == test_status) {
    usb_cdc_send_string("[INFO] SD card RW test PASSED!\n");
  } else {
    usb_cdc_send_string("[INFO] SD card RW test FAILED!\n");
  }
  usb_cdc_send_string("[INFO] SD card RW test finished.\n");
}

void show_micro_sd_meta_info(void) {
  uint8_t cid[4], cap[4], blk_size[4];
  char cid_char[9], cap_char[9], blk_size_char[13] = {'\0'};
  cid_char[8] = '\n';
  cap_char[8] = '\n';
  blk_size_char[12] = '\n';

  dy_int32_to_byte_array(SD_HANDLER.CID, cid);
  dy_htoa(cid, 4, (uint8_t *)cid_char);
  export_one_field("Card ManufacturerID: ", cid_char);

  dy_int32_to_byte_array(SD_HANDLER.SdCard.RelCardAdd, cap);
  dy_htoa(cap, 4, (uint8_t *)cap_char);
  export_one_field("Card Relative Address: ", cap_char);

  dy_itoa(SD_HANDLER.SdCard.BlockSize, blk_size_char);
  dy_shift_leading_null_chars(blk_size_char);
  export_one_field("Card Blocksize: ", blk_size_char);
}

void sd_write_read_test_dma(void) {

  usb_cdc_send_string("[INFO] SD card RW test start.\n");
  char status_char[2] = {sd_status + '0', '\n'};

  // Add data to buffer
  /* fill_buffer(sdio_write_buf, SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS, 0x3456);
   */
  fill_buffer_with_random_char(sdio_write_buf,
                               SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS);

  // Write data to SD card
  sd_status = HAL_SD_WriteBlocks_DMA(&SD_HANDLER, (uint8_t *)sdio_write_buf,
                                     SD_RW_TEST_ADDRESS,
                                     USE_HAL_WWDG_REGISTER_CALLBACKS);
  status_char[0] = sd_status + '0';
  usb_cdc_send_string("[INFO] DMA Write blocks status: ");
  usb_cdc_send_string(status_char);

  HAL_Delay(100);

  // Read data from SD card
  sd_status = HAL_SD_ReadBlocks_DMA(&SD_HANDLER, (uint8_t *)sdio_read_buf,
                                    SD_RW_TEST_ADDRESS, SD_RW_TEST_NUM_BLOCKS);
  status_char[0] = sd_status + '0';
  usb_cdc_send_string("[INFO] DMA Read blocks status: ");
  usb_cdc_send_string(status_char);

  // Compare the R/W data
  test_status = compare_buffer(sdio_write_buf, sdio_write_buf,
                               SD_BLOCK_SIZE * SD_RW_TEST_NUM_BLOCKS);

  HAL_Delay(10);
  if (PASSED == test_status) {
    usb_cdc_send_string("[INFO] SD card DMA RW test PASSED!\n");
  } else {
    usb_cdc_send_string("[INFO] SD card DMA RW test FAILED!\n");
  }
  usb_cdc_send_string("[INFO] SD card DMA RW test finished.\n");
}

void fatfs_rw_demo(void) {

  // Step 1: register the fs object.
  f_res = f_mount(&sd_fs, "", 1); // return 0 = OK, else has error.
  if (f_res) {
    usb_cdc_send_string("Mount error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
    Error_Handler();
  } else {
    usb_cdc_send_string("Mount succeeded!\n");
  }

  // Step 2: create and open a new file to write.
  f_res = f_open(&fm_file, fm_file_path, FA_CREATE_ALWAYS | FA_WRITE);
  if (f_res) {
    usb_cdc_send_string("Open file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Open file succeeded!\n");
  }

  // Step 3: Write data to the file.
  // TODO: change the string to random char buf.
  /* fill_buffer_with_random_char(file_str_test, 100); */
  // size-1 to prevent from writing the \0 to file.
  f_res = f_write(&fm_file, file_str_test, sizeof(file_str_test) - 1,
                  (void *)&f_w_cnt);
  if (f_res) {
    usb_cdc_send_string("Write file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Write file succeeded!\n");
  }

  // Step 4: Close file handler.
  f_res = f_close(&fm_file);
  if (f_res) {
    usb_cdc_send_string("Close file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Close file succeeded!\n");
  }

  // Step 5: Open the file again and read data.
  f_res = f_open(&fm_file, fm_file_path, FA_READ);
  if (f_res) {
    usb_cdc_send_string("Re-open file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Re-open file succeeded!\n");
  }

  // Step 6: Read data from SD card to buffer.
  f_res =
      f_read(&fm_file, r_text_buf, sizeof(r_text_buf) - 1, (UINT *)&f_r_cnt);
  if (f_res) {
    usb_cdc_send_string("Read file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Read file succeeded!\n");
  }

  // Step 7: Close the file handler
  f_res = f_close(&fm_file);
  if (f_res) {
    usb_cdc_send_string("Close2 file with error: ");
    CDC_Transmit_FS((uint8_t *)&f_res, 1);
  } else {
    usb_cdc_send_string("Close2 file succeeded!\n");
  }

  if (f_w_cnt == f_r_cnt) {
    usb_cdc_send_string("FATFS test PASSED!\n");
  }
}

HAL_StatusTypeDef configure_dma_for_sd(SD_HandleTypeDef *hsd) {
  HAL_StatusTypeDef status = HAL_ERROR;
  // TODO: add dma configuration here.
  return status;
}

FRESULT f_open_append(FIL *fp, const char *file_path) {
  FRESULT fr;

  /* Opens an existing file. If not exist, creates a new file. */
  fr = f_open(fp, file_path, FA_WRITE | FA_OPEN_ALWAYS);
  if (fr == FR_OK) {
    /* Seek to end of the file to append data */
    fr = f_lseek(fp, f_size(fp));
    if (fr != FR_OK)
      f_close(fp);
  }
  return fr;
}

FRESULT f_set_timestamp(char *file_path, int year, uint8_t month, uint8_t m_day,
                        uint8_t hour, uint8_t min, uint8_t sec) {
  FILINFO fno;
  fno.fdate = (WORD)(((year - 1980) * 512U) | month * 32U | m_day);
  fno.ftime = (WORD)(hour * 2048U | min * 32U | sec / 2U);

  return f_utime(file_path, &fno);
}

uint8_t f_mount_with_retry(void) {

  FRESULT sd_res = FR_TIMEOUT;
  uint8_t mount_attempt = 0;
  while ((FR_OK != sd_res) and (mount_attempt < 4)) {
    // Keep trying until succeed.
    sd_res = f_mount(&sd_fs, "", 1);
    mount_attempt += 1;
    HAL_Delay(10);
  }
  // Note: the assigned variable is is_sd_mounted, not sd_res.
  if (FR_OK == sd_res) {
    usb_cdc_send_string("[INFO] Mnt OK\n");
    return True;
  } else {
    usb_cdc_send_string("[ERR] Mnt NOK\n");
    return False;
  }
}

uint8_t f_open_append_with_retry(FIL *fp, const char *file_path) {
  FRESULT sd_res = FR_TIMEOUT; // reset
  uint8_t sd_failed_attempt = 0;
  while ((FR_OK != sd_res) and (sd_failed_attempt <= 4)) {
    /* sd_res = f_open(&fm_file, file_path, FA_CREATE_ALWAYS | FA_WRITE); */
    sd_res = f_open_append(fp, file_path);
    sd_failed_attempt += 1;
    HAL_Delay(1);
  }
  // Note: the assigned variable is is_file_opened, not sd_res.
  if (FR_OK == sd_res) {
    usb_cdc_send_string("[INFO] FO OK\n");
    return True;
  } else {
    usb_cdc_send_string("[ERR] FO NOK\n");
    return False;
  }
}

uint8_t f_open_to_fix_error_with_retry(FIL *fp, const char *file_path,
                                       DWORD *pos_ptr) {
  FRESULT sd_res = FR_TIMEOUT; // reset
  uint8_t f_op_attempt = 0;
  while ((FR_OK != sd_res) and (f_op_attempt <= 4)) {
    /* Opens an existing file. If not exist, creates a new file. */
    sd_res = f_open(fp, file_path, FA_WRITE | FA_OPEN_ALWAYS);
    if (sd_res == FR_OK) {
      /* Seek to end of the file to append data */
      sd_res = f_lseek(fp, *pos_ptr);
      if (sd_res != FR_OK)
        f_close(fp);
    }
    f_op_attempt += 1;
    HAL_Delay(1);
  }
  // FE=Fix Error
  // Note: the assigned variable is is_file_opened, not sd_res.
  if (FR_OK == sd_res) {
    usb_cdc_send_string("[INFO] FO-FE OK\n");
    return True;
  } else {
    usb_cdc_send_string("[ERR] FO-FE NOK\n");
    return False;
  }
}

uint8_t f_close_with_retry(FIL *fp) {
  FRESULT sd_res = FR_TIMEOUT; // reset
  uint8_t f_op_attempt = 0;
  while ((FR_OK != sd_res) and (f_op_attempt < 5)) {
    sd_res = f_close(fp);
    f_op_attempt += 1;
    HAL_Delay(1);
  }
  // Note: the assigned variable is is_file_closed, not sd_res.
  if (FR_OK == sd_res) {
    usb_cdc_send_string("[INFO] FX OK\n");
    return True;
  } else {
    usb_cdc_send_string("[ERR] FX NOK\n");
    return False;
  }
}

void sd_card_fixing_routine() {

  uint8_t sd_op_attempt = 0;
  FRESULT sd_res = FR_TIMEOUT; // local variable

  switch (sdm_st.fix_sd_code) {
  case SD_NEED_REOPEN_APPEND:
    if (sdm_st.is_file_opened) {
      f_close_with_retry(&fm_file);
      sdm_st.is_file_opened = False;
    }
    sdm_st.is_file_opened =
        f_open_append_with_retry(&fm_file, sdm_st.file_path);
    break;
  case SD_NEED_REMOUNT_REOPEN:
    // TODO: check whether this is enough to solve the problem
    usb_cdc_send_string("[INFO] Re-init FATFS and remount SD.\n");
    if (sdm_st.is_file_opened) {
      f_close_with_retry(&fm_file);
      sdm_st.is_file_opened = False;
    }
    f_mount(0, "", 0); // Unmount
    sdm_st.is_sd_mounted = False;

    MX_FATFS_Init();

    while ((FR_OK != sd_res) and (sd_op_attempt < 4)) {
      // Keep trying until succeeded.
      sd_res = f_mount(&sd_fs, "", 1);
      sd_op_attempt += 1;
      HAL_Delay(10);
    }
    if (FR_OK == sd_res) {
      sdm_st.is_sd_mounted = True;
    } else {
      usb_cdc_send_string("[ERR] SD mount failed! Plug it in and reset MCU.\n");
      sdm_st.is_sd_mounted = False;
      sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
    }

    // Re-open the file.
    if (sdm_st.is_sd_mounted) {
      sdm_st.is_file_opened = f_open_to_fix_error_with_retry(
          &fm_file, sdm_st.file_path, &sdm_st.file_end_ptr);
    }
    sdm_st.cumulative_fatfs_io_error = 0;
    // TODO: reset MCU if error still exists after reboot.
    break;
  case SD_NEED_REOPEN_FIX_BLOCK:
    usb_cdc_send_string("[INFO] Fix abnormal block.\n");
    // Deal with special cases first, other errors may occur.
    if (sdm_st.is_file_opened) {
      f_sync(&fm_file);
      f_close_with_retry(&fm_file);
      sdm_st.is_file_opened = False;
    }
    sdm_st.is_file_opened = f_open_to_fix_error_with_retry(
        &fm_file, sdm_st.file_path, &sdm_st.file_end_ptr);
    break;
  case SD_NEED_NOTHING:
  default:
    break;
  }
}

void sdio_show_success_count_and_io_error(void) {
#if HAS_USB_CDC_VCP
  if (0 != sdm_st.sd_res) {
    char zero_str[ITOA_BUF_LEN] = {'\0'};
    char zero_disp[15] = {'\0'};
    zero_disp[0] = '(';
    dy_itoa(sdm_st.consecutive_zero_cnt, zero_str);
    dy_shift_leading_null_chars(zero_str);
    strcat(zero_disp, zero_str);
    strcat(zero_disp, ")");

    memset(zero_disp, 0, ITOA_BUF_LEN);
    dy_itoa(sdm_st.sd_res, zero_str);
    dy_shift_leading_null_chars(zero_str);
    strcat(zero_disp, zero_str);
    dy_append_newline(zero_disp);
    usb_cdc_send_string(zero_disp);

    sdm_st.consecutive_zero_cnt = 0; // reset counter
  }
#endif
}

void sdio_reset_sdio_monitor() {
  sdm_st.sd_res = FR_TIMEOUT; // initialization
  sdm_st.is_sd_mounted = False;
  sdm_st.is_file_opened = False;
  sdm_st.need_block_rewrite = False;
  sdm_st.consecutive_zero_cnt = 0;
  sdm_st.cumulative_fatfs_io_error = 0;
  sdm_st.fix_sd_code = SD_NEED_NOTHING;
}

void sdio_determine_fixing_request() {
  // Error handler - zero-block occurs, open file and overwrite the block.
  if (1 == sdm_st.sd_res or 2 == sdm_st.sd_res or 9 == sdm_st.sd_res) {
    sdm_st.fix_sd_code = SD_NEED_REOPEN_FIX_BLOCK;
    sdm_st.need_block_rewrite = True;
  }

  // Error handler - continuous 2 occurs
  if (sdm_st.cumulative_fatfs_io_error >= MAX_FATFS_ALLOWED_ERROR) {
    sdm_st.fix_sd_code = SD_NEED_REMOUNT_REOPEN;
  }
}
