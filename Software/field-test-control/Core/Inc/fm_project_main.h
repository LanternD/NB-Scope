/**
  @file fm_project_main.h
  @author Deliang Yang
  @date_created 2019-11-10
  @last_update N/A
  @version 0.1
  @brief The de facto main header file for the project, getting rid of the
  possible regenerating main.h by the cubeMX.
  @details Prevent from defining and exporting typedef, variables, enum in this
  header.
*/
#ifndef __FM_PROJECT_MAIN_H__
#define __FM_PROJECT_MAIN_H__

#include "dwt_delay.h"
#include "dy_syntax.h"
#include "dy_utils.h"
#include "eeprom_mgr.h"
#include "fm_sdio.h"
#include "main.h" // Pin re-labels and peripheral handlers
#include "nb_iot_mod.h"
#include "si7021.h"
#include "ssd1306.h"
#include "stm32f1xx_hal.h"
#include "ti_ina226.h"
#include "usb_device.h"
#include <string.h> // actually included in other place.

#ifdef __cplusplus
extern "C" {
#endif

/* Project macros  ***********************************************************/

#define ULTX_CURRENT_POINT_1K 10

#define V_BATT_ADC hadc1
#define V_BATT_CALIBRATION_VALUE 1.2753F
// inverse of 470k/(470k+220k) need to calibrate.
#define V_BATT_DIVIDING_RATIO_INV_DEFAULT 1.4859F
#define V_BATT_CONSTANT V_BATT_CALIBRATION_VALUE * 3300 / 4096
/* Note about ADC conversion (V_batt sensing):
 GetValue returns the ADC reg value. reg_val*3.3/4096 = real voltage
 This is the 470k/(220k+470k) divided value. Need to convert again.
 So, V_batt = (470+220)/470*3.3v/4096 * V_adc_reg
 Need to measure the real value of 690k/470k (=1.4681 by default), which can be
 different for different board.
 */

#define USB_DP_GPIO_Port GPIOA
#define USB_DP_Pin GPIO_PIN_12
#define USB_DM_GPIO_Port GPIOA
#define USB_DM_Pin GPIO_PIN_11

/* Frequently used functions*/
#define LED0_ON HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_SET)
#define LED0_OFF HAL_GPIO_WritePin(LED0_GPIO_Port, LED0_Pin, GPIO_PIN_RESET)
#define LED1_ON HAL_GPIO_WritePin(LED1_GPIO_Port, LED1_Pin, GPIO_PIN_SET)
#define LED1_OFF HAL_GPIO_WritePin(LED1_GPIO_Port, LED1_Pin, GPIO_PIN_RESET)
#define LED0_TOGGLE HAL_GPIO_TogglePin(LED0_GPIO_Port, LED0_Pin)
#define LED1_TOGGLE HAL_GPIO_TogglePin(LED1_GPIO_Port, LED1_Pin)
#define IS_BUTTON1_PRESSED                                                     \
  GPIO_PIN_RESET == HAL_GPIO_ReadPin(BUTTON1_GPIO_Port, BUTTON1_Pin)
#define IS_BUTTON2_PRESSED                                                     \
  GPIO_PIN_RESET == HAL_GPIO_ReadPin(BUTTON2_GPIO_Port, BUTTON2_Pin)

/* Variables/functions from other modules ************************************/
// Note: usuall the vairables from other modules are exported in their header
// files, so including their header grants the access to those variables. Here
// we only need the functions from the CubeMX generated modules.
extern uint8_t CDC_Transmit_FS(uint8_t *Buf, uint16_t Len);
extern uint8_t CDC_is_busy();

/* TypeDefs
 ****************************************************************/
// State machine enum
typedef enum {
  STATE_DEMOS, /*!< Set the MCU to run demo only. */
  STATE_INIT,  /*!< The MCU just wakes up, loading everything from EEPROM. It
                  should exit this state and enter IDLE or FIELD_TEST soon.
                */
  STATE_IDLE,  /*!< The task is not assigned, waiting for the user to press
                  SW1. */
  STATE_INIT_PACKET, /*!< Get the init packet from server. */
  STATE_FIELD_TEST,  /*!< The actual mode that the MCU is executing the UL
                        field  measurement task. */
  STATE_WRITE_META_TO_EEPROM,      /*!< Write the board constant meta to EEPROM,
                                      run this before the node can be actually
                                      deployed.
                                    */
  STATE_PPL_CURRENT_SENSING_TO_SD, /*!< The pipeline where the node senses
                                      the current and writes them to SD card
                                      if inserted. */
  STATE_PPL_DBG_LOG_TO_SD,         /*!< The pipeline that the node collects the
                                      debug log and writes them into the SD card if
                                      inserted.
                                    */
  STATE_DEVELOP_1, /*!< Put things here if it is under development, move
                      somewhere else later */
  STATE_DEVELOP_2, /*!< Put things here if it is under development, move
                      somewhere else later */
} work_mode_fsm_et;

/* Exported variables ******************************************************/
extern eeprom_board_constant_meta_t g_bcm_st;
extern eeprom_board_variable_meta_t g_bvm_st;
extern eeprom_task_monitor_t g_eeprom_tm_st;
extern uint8_t terminate_task_flag;
extern uint8_t proceed_to_init_packet_flag;
extern work_mode_fsm_et work_mode;
extern uint8_t pseudo_assigned_flag; /*!< delete this later */

/* Module function declaration ***********************************************/

/**
   @brief Get the global RTC timestamp, in second format
   @param None.
   @return u32t RTC time in second.
   @note Used in STANDBY mode determination.
*/
uint32_t get_rtc_timestamp();
void project_additional_init(void);

void switch_work_mode(work_mode_fsm_et new_mode);

/* Supportive functions ****************************************************/

/**
   @brief Enter MCU PSM mode.
   @return None.
   @note Please do so after the NB-IoT module enters PSM.
 */
void power_enter_sleep_mode();

/**
   @brief Set the alarm timer to wakeup the MCU.
   @param alarm_sec: how many seconds you want the MCU to sleep.
   @return None.
   @note Put the MCU into STANDBY as soon as this function is executed.
*/
void config_rtc_standby_auto_wakeup_after(uint16_t alarm_sec);

/**
    @brief Send string to Host PC, which is able to count the string length.
    @param A pointer to the buf that is going to be sent.
    @return None.
    @note The function will stop parsing until '\0' or '\n' is found. Be sure
    to include that at the end of your char array.
  */
void usb_cdc_send_string(char *str_buf);

/**
   @brief Send line break to UART.
   @param None.
   @return None.
*/
void usb_cdc_new_line();

/**
   @brief Load previous state from the eeprom. The addresses are predefined.
   @param None.
   @return HAL_STATUS, 0=OK, 1-3 for other reasons.
   @note The fields are defined in a struct. If the loaded info is null, write
   a predefined set into it.
*/
HAL_StatusTypeDef load_previous_state_from_eeprom();

/**
   @brief Write board variable meta and task monitor to the EEPROM.
   @param g_bvm: (global) board variable meta
   @param g_tm_st (global) task monitor
   @return HAL_STATUS, 0=OK, 1-3 for other reasons.
   @note
*/
HAL_StatusTypeDef write_current_state_to_eeprom();

/**
   @brief Send the start signal via LED blinking
   @param None.
   @return None.
*/
void emit_field_test_start_signal();

/**
   @brief Send the field test termination signal via LED blinking
   @param None.
   @return None.
*/
void emit_field_test_terminate_signal();

/* Pipelines (End-to-end routine) ******************************************/
/**
   @brief Debug current sensing. End to end, from reading to writing to the SD
   card.
   @param None.
   @return None.
   @note Two buffers involve, one storing the time ticks, the other one
   storing the current sensing int16 (reg_val). This function should be able
   to run independently. After that the function will be integrated into the
   main pipeline.
*/
void current_sensing_to_sd_pipeline(char *command);

/**
   @brief Continuously read in the debug log and write it out to SD card.
   @param None.
   @return None.
   @note Two buffers switching to store the read-in debug log.
*/
void dbg_log_to_sd_pipeline(char *command);

/**
   @brief XXX DEPRECARTED. Read the i_bus transmission part reg_val to sd.
   @param None.
   @return None.
   @note Loaded the very first current to RAM, and write to SD one by one. The
   ULTX current is crucial for analysis. So it is important to get a detail of
   it.
*/
void ul_transmission_current_sensing_to_sd_pipeline();

/**
   @brief Pipeline to write board meta to the board.
   @param None.
   @return None.
*/
void board_meta_io_pipeline();

/**
    @brief Load board constant meta, variable meta, and task monitor from
   EEPROM.
    @param None.
    @return None.
    @note All the vairables are global variables defined in eeprom_mgr.h
*/
void load_meta_and_task_from_eeprom();

/**
   @brief Communicate with the server to have the task assigned.
   @param None.
   @return None.
   @note Start the pipeline.
*/
void task_assignment_pipeline();

/**
   @brief Control the module to perform a normal uplink transmission
   @param None.
   @return None.
   @note Make sure all the environment variables are set before calling this
   function.
*/
void field_test_control_pipeline();

void develop_override_loaded_results_from_eeprom();

#ifdef __cplusplus
}
#endif

#endif
