/**
   @file fm_sdio.h
   @author Deliang Yang
   @date_created 2019-11-20
   @last_update 2019-11-20
   @version 0.1
   @brief Function declaration for SD card access, from basic erase,
   r/w, checking, to FATFS file organization.
   @details Work flow: (1) erase (2) check erase (3) write (4) check
   write.
*/

#ifndef __FM_SDIO_H__
#define __FM_SDIO_H__

#include "dy_utils.h" // use the dy_rand() function.
#include "fatfs.h"
#include "main.h" // get the hsd handler
#include "nb_iot_mod.h"
#include "stm32f1xx_hal.h"

/* Macros for the module *****************************************************/
#define SD_HANDLER hsd
#define SDIO_DMA_HANDLER hdma_sdio

#define SD_BLOCK_SIZE 512
#define SD_NUM_BLOCKS 8 /*!< number of blocks per buffer */
#define SD_RW_TEST_ADDRESS 0x00008000
#define SD_RW_TEST_NUM_BLOCKS 4
#define SD_OPERATION_TIMEOUT 0x0FFF

#define MAX_FATFS_ALLOWED_ERROR 25 // Chosen empirically.

/* Exported defined variables ************************************************/
extern uint8_t sdio_write_buf[];
extern uint8_t sdio_read_buf[];

extern FATFS sd_fs;   // FATFS file system object
extern FIL fm_file;   // file object
extern FRESULT f_res; // the return code of file operation

extern uint32_t f_r_cnt;        // count of succeeded file IO
extern uint32_t f_w_cnt;        // count of succeeded file IO
extern uint8_t file_str_test[]; // string to be written
extern uint8_t r_text_buf[];
extern char fm_file_path[]; // file path

/* Externally declared functions *********************************************/
extern void usb_cdc_send_string(char *str_buf);
extern uint8_t CDC_Transmit_FS(uint8_t *Buf, uint16_t Len);

/* Locally defined typedefs and variables declaration with the typedef *******/
typedef enum { FAILED, PASSED } sd_test_state_t;

typedef enum {
  SD_NEED_NOTHING,
  SD_NEED_REOPEN_APPEND,
  SD_NEED_REMOUNT_REOPEN,
  SD_NEED_REOPEN_FIX_BLOCK
} fix_sd_et;

typedef struct {
  FRESULT sd_res; /*!< Last sd operation return value */
  fix_sd_et fix_sd_code;
  uint8_t is_file_opened;     /*!< =1 if file in OPEN status */
  uint8_t is_sd_mounted;      /*!< =1 if SD card is mounted */
  uint8_t need_block_rewrite; /*!< need rewrite abnormal block */
  char file_path[30];         /*!< file_path string */
  DWORD file_end_ptr;         /*!< Mark the file end before writing a block */
  uint16_t consecutive_zero_cnt; /*!< Count the continuous write success */
  uint16_t
      cumulative_fatfs_io_error; /*!< Count the total error to decide remount */
} sdio_monitor_t;

extern sdio_monitor_t sdm_st;

HAL_StatusTypeDef sd_status;
sd_test_state_t test_status;

/* Module function declaration ***********************************************/
/**
   @brief Check whether the erase buffer is correct. The erased buffer region
   contains either 0xFF or 0x00.
   @param *p_buf: pointer of the buffer
   @param buf_len: length of the buffer.
   @return PASSED if all the bytes are either 0xFF or 0x00; FAILED otherwise.
 */
sd_test_state_t check_erased_buffer(uint32_t *p_buf, uint32_t buf_len);

/**
   @brief Erase the SD card at the macro-defined address. No DMA support
   @param *p_buf: pointer of the buffer.
   @param buf_len: length of the buffer.
   @return PASSED if all the bytes are either 0xFF or 0x00; FAILED otherwise.
   @attention This operation ruins the file system of the SD card. It needs to
   be formatted again before accessing. So process this with caution.
 */
void sd_erase_test(void);

/**
   @brief Add data to a buffer for writing.
   @param *p_buf pointer to buffer.
   @return pointer to the filled buffer.
*/
void fill_buffer(uint32_t *p_buf, uint32_t buf_len, uint32_t offset);

/**
   @brief Add random characters to a buffer for writing.
   @param *p_buf pointer to buffer.
   @return pointer to the filled buffer.
*/
void fill_buffer_with_random_char(uint32_t *p_buf, uint32_t buf_len);

/**
   @brief SD card write and read test. The read data are compared to the written
   ones to check the integrity. No DMA support.
   @attention This operation ruins the file system of the SD card. It needs to
   be formatted again before accessing. So process this with caution.
*/
void sd_write_read_test(void);

/**
   @brief SD card write and read test. The read data are compared to the written
   ones to check the integrity. With DMA support.
   @attention This operation ruins the file system of the SD card. It needs to
   be formatted again before accessing. So process this with caution.
*/
void sd_write_read_test_dma(void);

/**
   @brief Compare the data between to two buffers.
   @param *p_buf1: pointer to the 1st buffer.
   @return PASSED if two buffers equal; FAILED otherwise.
*/
sd_test_state_t compare_buffer(uint32_t *p_buf1, uint32_t *p_buf2,
                               uint32_t buf_len);

/**
   @brief Show the meta info of the micro SD card through USB VCP.
   @param None
   @return None
   @note ManufacturerID, Capacity, Blocksize.
*/
void show_micro_sd_meta_info(void);

/**
   @brief Read/write demo with FATFS file system.
   @param None
   @return None.
   @note Use this first instead of the sd_write_read_test() to preserve the file
   structure within the SD card.
*/
void fatfs_rw_demo(void);

/**
   @brief Test how many data can be written into the SD card with current
   setting.
   @param None
   @return None
   @note The process is run for 30 seconds. Check the speed_test.txt file size
   to calculate the speed.
*/
void write_speed_test(void);

/**
   @brief Configure DMA channel for the SD card R/W access.
   @param hsd: SD card handler
   @return status of the initialization function.
   @note Put it to bsd_driver_sd.c, see
   https://blog.csdn.net/zl199203/article/details/83514105
*/
HAL_StatusTypeDef configure_dma_for_sd(SD_HandleTypeDef *hsd);

/**
   @brief Append new data to a file.
   @param fp: file object to create.
   @param file_path: file_location.
   @return FRESULT: operation result flag.
   @note Open a file and move the cursor to the end of the file.
    Check this link: http://elm-chan.org/fsw/ff/res/app1.c
*/
FRESULT f_open_append(FIL *fp, const char *file_path);

/**
   @brief Set file timestamp in FATFS
   @param file_path, year 2019, month 11, m_day 23, hour 22, min 11, sec 21
   @return FRESULT, operation return code
   @note A question: should this function called after file close, or while file
   opens?
*/
FRESULT f_set_timestamp(char *file_path, int year, uint8_t month, uint8_t m_day,
                        uint8_t hour, uint8_t min, uint8_t sec);

/**
   @brief Mount SD card, try 4 times by default.
   @return FRESULT. 0 if succeeded.
   @note No parameter here but we use global variable in the f_mount inside.
*/
uint8_t f_mount_with_retry(void);

/**
   @brief Try to open several times until it succeeds.
   @param fp: file object.
   @param file_path: path to the file.
   @return 1 if succeeds, 0 otherwise.
   @note It attempts 4 times by default.
*/
uint8_t f_open_append_with_retry(FIL *fp, const char *file_path);

/**
   @brief Open the file with error to write again. Such that the abnormal
   blocks will be filled.
   @param fp: file handler.
   @param file_path: string file path.
   @prarm pos_ptr: Position pointer.
   @return 1 if OK, 0 otherwise.
   @note It attampts 4 times by default.
*/
uint8_t f_open_to_fix_error_with_retry(FIL *fp, const char *file_path,
                                       DWORD *pos_ptr);

/**
   @brief Try to close several times until it succeeds.
   @param fp: file object.
   @return 1 if succeeds, 0 otherwise.
   @note It attempts 10 times by default.
*/
uint8_t f_close_with_retry(FIL *fp);

void sd_card_fixing_routine(void);

void sdio_show_success_count_and_io_error(void);

/**
   @brief Rest the sdio monitor sdm_st. For pipeline changing.
   @param None. (global variable inside)
   @return None.
*/
void sdio_reset_sdio_monitor(void);

/**
   @brief Determine whether to set the fix_sd_code or not since lasst SD card operation.
   @param None. (global variable inside)
   @return None.
   @note Call it right after f_write or other code that use sdm_st.res to get return value.
*/
void sdio_determine_fixing_request(void);
#endif // END ifndef
