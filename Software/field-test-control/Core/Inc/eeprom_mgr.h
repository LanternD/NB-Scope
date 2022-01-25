/**
  @file eeprom_mgr.h
  @brief   ON Semiconductor EEPROM CAT24C128 IO
  @date    Nov 2019
  @version 0.1
  @author  Deliang Yang
  @details This library contains the necessary functions to
  initialize, read and write data to the EEPROM CAT24C128 using the I2C
  protocol.
  @note The CAT24C128 has 128 Kbits capacity, whose address ranges from 0x0000
  to 0x3FFF.
  @attention This module only takes care of the EEPROM IO. How the
  information is processed should be implemented in other module, such as
  nb_iot_mod.h
*/

#ifndef EEPROM_MGR_H
#define EEPROM_MGR_H

#include "dy_utils.h"
#include "main.h"
#include "string.h"

/* Module macros  ************************************************************/
#ifndef EEPROM_I2C_PORT
#define EEPROM_I2C_PORT hi2c2
#endif

#define EEPROM_ADDR 0xA2 // device address.
#define EEPROM_MEMADDSIZE 2
//!< Memory address size. 1 means 8-bit address, 2 means 16-bit address. 2
//!< for CAT24C128.

#define EEPROM_I2C_TIMEOUT 200

#define EEPROM_DEMO_ADDRESS_START 0x3FC0
#define EEPROM_BCM_ADDR_START 0x0100
#define EEPROM_BVM_ADDR_START 0x0250
#define EEPROM_TM_ADDR_START 0x400

/**
   @brief A smallest meaningful element of the eeprom storage.
 */
typedef struct {
  uint16_t addr;     /**< address in EEPROM */
  int value;         /**< could be 8 / 16 / 32 bit */
  uint8_t byte_size; /**< 1, 2, or 4 bit */
} eeprom_element_t;

/**
   @brief The meta below should be only written to EEPROM for only once, unless
   there is hardware update.
   @note If there are new elements to add, append at the end only.
   If you add one field, update the following functions accordingly:
   - eeprom_read_board_constant_meta_struct()
   - eeprom_write_baord_constant_meta_struct()
   - process_board_constant_meta()
   - exprot_bcm_to_usb_vcp()
*/
typedef struct {
  eeprom_element_t node_region; /*!< char, node number region, A=USA, C=China */
  eeprom_element_t node_num;    /*!< int8, node number without the 'A' or 'C' */
  eeprom_element_t module_on_board; /*!< int8, module indicator */
  /*!< List of module supported: (consistent with nb_iot_mod.h)
     - 0: UNKNOWN
     - 1: Quectel BC28
     - 2: Quectel BC35
     - 3: Quectel BC95
     - 4: Quectel BC26
     - 5: Quectel BC66
     - 6: Quectel BG36
     - 7: Quectel BG96
     - 8: uBlox SARAR410M02B
     - 9: ZTE ME3616
   */
  eeprom_element_t network_operator; /*!< int8 */
  /*!< List of operators, determine the packet protocol to UL
    - 0: China Telecom (CT)
    - 1: China Mobile (CM)
    - 2: Verizon (VR)
  */
  eeprom_element_t is_debug_log_supported; /*!< int8, Only BC28, BC35, BC95
                                              supports debug log */
  eeprom_element_t
      base_board_hardware_version; /*!< int8, 0=blue base board (V3.0), 1=red
                                      base board (V3.1) */
  eeprom_element_t
      module_board_hardware_version; /*!< int8, if nothing changed, the version
                                        is 1. Change this in the future
                                        (rarely). */
  eeprom_element_t
      current_calibration_value; /*!< int16, calibration register value */
  eeprom_element_t
      v_batt_calibration_value; /*!< int16, battery ADC value sensing
                                calibration coefficient. The original value
                                is 1.xxx, here we multiply it by 1000 as int. */
} eeprom_board_constant_meta_t;

/**
   @brief The meta that is going to update every now and then. Use another
   function to handle this.
   @note If there are new elements to add, append at the end only.
   If you add one field, update the following functions accordingly:
   - eeprom_read_board_variable_meta_struct()
   - eeprom_write_baord_variable_meta_struct()
   - process_board_variable_meta()
   - exprot_bcm_to_usb_vcp()
 */
typedef struct {
  eeprom_element_t mcu_software_version; /*!< int16, incremental*/
  eeprom_element_t year_month_date; /*!< int32, the time that the firmware is
                                       compiled. 2B year, 1B month, 1B date */
  eeprom_element_t
      mcu_wakeup_count; /*!< int32, count the time that MCU awakes */
} eeprom_board_variable_meta_t;

/**
   @brief The task monitor board. Defines the MCU uplink Tx behavior, monitor
   the execution of the task.
   @note If there are new elements to add, append at the end only.
   If you add one field, update the following functions accordingly:
   - eeprom_read_task_monitor_struct()
   - eeprom_write_task_monitor_struct()
   - process_eeprom_task_monitor()
   - exprot_tm_to_usb_vcp()
 */
typedef struct {
  eeprom_element_t is_task_assigned; /*!< int8, task assigned by the server*/
  eeprom_element_t test_mode; /*!< int8, indicator: 0=fixed UL time; 1=fixed
                               packet number assigned by server */
  eeprom_element_t test_id;   /*!< int16 an id assigned to this test round. */
  eeprom_element_t application_type; /*!< int8, see document. not affect the
                                        task execution. */
  eeprom_element_t
      collect_debug_log_or_current; /*!< int8, 0=current, 1=debug log*/
  eeprom_element_t ul_total_time;   /*!< int16, minutes, for test_mode=0 case,
                                       assigned by server */
  eeprom_element_t
      ul_total_pkt; /*!< int16, for test_mode=1 case, assigned by server */
  eeprom_element_t
      ul_pkt_count; /*!< int16, The number of packets that are transmitted. Used
                       to determine the end of the task. */
  eeprom_element_t ul_pkt_size; /*!< int16, number of bytes that a packet
                                   contains. The useful info takes some bytes.
                                   The rest is filled by random chars. */
  eeprom_element_t
      mcu_sleep_timer; /*!< int16, seconds, the time that MCU sleep before next
                          awake. Note that if you want a 3 minutes packet
                          interval, this value should be set as
                          (180-uplink_packet_tx_time) */
  eeprom_element_t task_status; /*!< int8,
                     0=the task is not assigned, node is in IDLE state, press
                      SW1 3 times to start;
                     1=the task is assigned and executing, but not finished yet;
                     2=the task finished succesfully;
                     3=last the task is terminated by the user;
                     4=there is error in the task execution. */
  eeprom_element_t
      err_code_last_run; /*!< int8, need to specify.
                           0: no error;
                           1: SD card IO to many errors;
                           2: packet not transmitted (failed to attch)
                           3: packet not transmitted (bad signal);
                           4: task terminated in last task;
                           5: eeprom IO error;*/
} eeprom_task_monitor_t;

/* Module function declaration
 ***********************************************/
/**
   Write one byte, for char or uint8_t variables.
 */
uint8_t eeprom_write_1_byte(uint16_t address, uint8_t *p_byte);

/**
   @brief Write two bytes, for uint16_t variables.
   @note Little endian, lower byte should be in buf[0], higher byte in buf[1]
 */
uint8_t eeprom_write_2_bytes(uint16_t address, uint8_t *p_bytes);

/**
   @brief Write four bytes, for uint32_t variables.
   @note Little endian.
 */
uint8_t eeprom_write_4_bytes(uint16_t address, uint8_t *p_bytes);

/**
  Write data to an address. Highly suggest that the buffer does not occupy 2
  pages at the same time. This function is different from eeprom_write_page().
  @param uint16_t start_address: the start address of the page.
  @param p_data: the buffer that contains the data. Any length <= 64 should be
  ok.
*/
uint8_t eeprom_write_buffer(uint16_t start_address, uint8_t *p_data,
                            uint8_t size_of_data);

/**
   Write a page's data. The input buffer should be exactly 64-byte length. The
  lowest 6 bits should be 0. \n
  Could use this function to write a string (<64 chars).
 */
uint8_t eeprom_write_page(uint16_t address, uint8_t *p_data);

/**
   Read one byte, for uint8_t and char variables.
 */
uint8_t eeprom_read_1_byte(uint16_t address, uint8_t *dest_buf);

/**
   Read two bytes, for uint16_t variables.
 */
uint8_t eeprom_read_2_bytes(uint16_t address, uint8_t *dest_buf);

/**
   Read four bytes, for uint32_t variables.
 */
uint8_t eeprom_read_4_bytes(uint16_t address, uint8_t *dest_buf);

/**
  Read data from an address.
  @param uint16_t start_address: the start address of the page.
  @param p_data: the buffer that contains the data. Any length <= 64 should be
  ok.
*/

uint8_t eeprom_read_buffer(uint16_t start_address, uint8_t *dest_buf,
                           uint8_t size_of_data);
/**
   Read 1 page from an address.
   @param address: The final 6 bits of the address should be all 0.
   @param dest_buf: The buffer to store the results.
 */
uint8_t eeprom_read_page(uint16_t address, uint8_t *dest_buf);

/**
   @brief Write a single element in a struct to EEPROM.
   @param eeprom_element_t ele: one element that has address in it.
   @return 0 if succeed, -1 if fail.
*/
uint8_t eeprom_write_one_element(eeprom_element_t *ele);

/**
   @brief Write the constant meta struct to the EEPROM. The address is stored in
   the element struct.
   @param st: a struct consists of elements.
   @return 0 if all the elements are written succesfully, N if N elements failed
   in writing.
   @note The address of the final element is not known. Resolve the possible
   address overlapping by separating the start address far enough.
*/
uint8_t
eeprom_write_board_constant_meta_struct(eeprom_board_constant_meta_t *bcm_st);
uint8_t
eeprom_write_board_variable_meta_struct(eeprom_board_variable_meta_t *bvm_st);
uint8_t eeprom_write_task_monitor_struct(eeprom_task_monitor_t *tm_st);

/**
   @brief Read a single element in a struct to EEPROM.
   @param eeprom_element_t ele: one element that has address in it. Assume the
   address is assigned.
   @return The field value of the element, -1 if fail.
*/
uint8_t eeprom_read_one_element(eeprom_element_t *ele);
/**
   @brief Read the board constant meta out. It is used to determine many of the
   board configuration.
   @param A struct that store the read values.
   @return 0 if succeed, N if there is N failed readings.
   @note The elements should be read according to the written sequence. These
   function could not be duplexed because the struct is not iterable.
*/
uint8_t eeprom_read_board_constant_meta_struct(
    eeprom_board_constant_meta_t *dest_bcm_st);
uint8_t eeprom_read_board_variable_meta_struct(
    eeprom_board_variable_meta_t *dest_bvm_st);
uint8_t eeprom_read_task_monitor_struct(eeprom_task_monitor_t *dest_tm_st);

/**
   @brief Format the struct and send them to host PC via USB VCP.
   @param g_bcm_st, g_bvm_st, g_tm_st.
   @return None.
   @note Wrap these functions in #if HAS_USB_CDC_VCP #endif
*/

#endif
