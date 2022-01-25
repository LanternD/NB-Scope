/**
  @file nb_iot_mod.h
  @author Deliang Yang
  @date_created 2019-11-24
  @last_update N/A
  @version 0.1
  @brief Library for controlling a series of NB-IoT modules.
  @details AT commands, module initialization, server interaction, test
  control. The interrupt handlers are put in "stm32f1xx_it.c".
  - Many of the enum values depends on the readout results from EEPROM. Before
  the MCU goes to sleep, the MCU writes all the updated values to EEPROM.
*/
#ifndef __NB_IOT_MOD_H__
#define __NB_IOT_MOD_H__

/* #include "dy_utils.h" */
/* #include "eeprom_mgr.h" */
#include "fm_project_main.h"
/* #include "main.h" */
/* #include "string.h" */
#include "usbd_cdc_if.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Macros for module control ***********************************************/
#define MAIN_UART_BUF_SIZE 512
#define DBG_UART_BUF_SIZE 512 // one SD block size.

#define BC28_DBG_PORT_BAUD 921600 /*!< Not used. Configured in CubeMX */
#define HAS_DBG_LOG 0
#define MAIN_UART huart2
#define MAIN_UART_DMA_RX hdma_usart2_rx
#define MAIN_UART_DMA_TX hdma_usart2_tx
#define DBG_UART huart1
#define DBG_UART_DMA_RX hdma_usart1_rx
#define DBG_BUF_COPY_DMA hdma_memtomem_dma1_channel1
#define COLLECT_DATA_TIMEOUT                                                   \
  30 /*!< max duration for running the I/dbglog collection pipeline */
#define MAX_NETWORK_ATTACH_QUERY_COUNT                                         \
  150 /*!< max allowed query, interval=200ms, 30s in total */
#if HAS_DBG_LOG
#define DBG_LOG_PORT huart1
#endif

// Xianghui
/*AT Response Indentifiers*/
/* #define ME_ATE0 ATE */
/* #define GET_FIRMWARE firmware */
/* #define REBOOT reboot */
/* #define GET_CSQ csq */
/* #define GET_MODULE_INFO module_info */
/* #define GET_RADIO_INFO radio_info */
/* #define CLOSE_SOCKET close_socket */
/* #define CREATE_SOCKET create_socket */
/* #define SEND_UDP send_udp */
/* #define PING ping */
/* #define BC28 bc28 */

/* #define ME_ATE0 0 */
/* #define GET_FIRMWARE 1 */
/* #define REBOOT 2 */
/* #define GET_CSQ 3 */
/* #define GET_MODULE_INFO 4 */
/* #define GET_RADIO_INFO 5 */
/* #define CLOSE_SOCKET 6 */
/* #define CREATE_SOCKET 7 */
/* #define SEND_PACK 8 */
/* #define PING 9 */
/* #define BAND 10 */
/* #define GET_DOWN_CDP 11 */
/* #define GET_DOWN_UDP 12 */
/* #define CLOSE_ECHO 13 */
/* #define SET_APN 14 */
/* #define BIND_SOCKET 15 */
/* #define STOP_NNMI 16 */
/* #define NET_ATTACH 17 */
/* #define RSRP_28_35_95 18 */
/*AT Variables*/

// Xianghui

/* ENUM for the uplink control ***********************************************/
typedef enum {
  ME_ATE0,
  GET_FIRMWARE,
  REBOOT,
  GET_CSQ,
  GET_MODULE_INFO,
  GET_RADIO_INFO,
  CLOSE_SOCKET,
  CREATE_SOCKET,
  SEND_PACK,
  PING,
  BAND,
  GET_DOWN_CDP,
  GET_DOWN_UDP,
  CLOSE_ECHO,
  SET_APN,
  BIND_SOCKET,
  STOP_NNMI,
  NET_ATTACH,
  RSRP_28_35_95,
  AT_BG96_ECL,
  AT_BG96_QENG,
  AT_ATTACH_RES
} at_cmd_id_et;

/**
 This is assigned by function identify_module_on_board();
 */
typedef enum {
  MODULE_UNDEFINED,
  BC28,
  BC35,
  BC95,
  BC26,
  BC66,
  BG36,
  BG96,
  SARAR410M02B,
  ME3616
} module_on_board_et;

typedef enum {
  OPERATOR_UNDEFINED,
  OPERATOR_CM,
  OPERATOR_CT,
  OPERATOR_VZ
} network_operator_et;

typedef enum {
  PREAMBLE,
  SEQ_NUM,
  TIME_TICK,
  LENGTH,
  MSG_ID,
  DATA,
  FINISHED,
  TO_SDIO
} debug_log_fsm_et; /*!< Finite state machine for debug log decoding. */

typedef enum { PROTO_UDP, PROTO_CDP } protocol_choice_et;

typedef enum {
  MODE_UNDEFINED,
  MODE_PACKET_NUM_LIMIT,
  MODE_TIME_LIMIT,
  MODE_FREERUN
} test_mode_et;

typedef enum {
  TASK_NOT_ASSIGNED,
  TASK_IN_EXECUTION,
  TASK_FINISHED_SUCCESSFULLY,
  TASK_TERMINATED_BY_USER,
  TASK_HAS_ERROR_IN_EXECUTION
} task_status_et;

typedef struct {
  uint8_t test_version;
  uint8_t date[3];      //  year (2digits), month, date
  uint8_t timestamp[3]; // hour, minute, second
} parsed_dl_packet_info_t;

typedef struct {
  uint8_t is_task_assigned_flag;
  test_mode_et e_test_mode;
  uint16_t test_id;
  uint8_t application_type;
  uint8_t
      collect_dbg_log_flag; /*!<  0: collect current; 1: collect debug log. */
  uint16_t ul_total_time;
  uint16_t ul_total_packet;
  uint16_t packet_index;
  uint16_t ul_packet_size;
  uint16_t mcu_sleep_timer;
  task_status_et e_task_status; // may overlap with work_mode
  uint8_t error_code_this_run;  // see eeprom_mgr.h for detail
  // The above will go in to the EEPROM.
  // Below will be temporarily used during MCU awakes.
  uint8_t is_task_finished_flag;
  uint8_t is_module_init_ready_flag; // Module need some time to attach to the
                                     // network.
  uint8_t did_module_enter_psm;
  uint32_t packet_sending_time_stamp; // decide when to standby.

} task_monitor_t; // eeprom_task_monitor_t is for eeprom IO, this one is for
                  // actual task control and monitoring. If some fields doesn't
                  // affect the task control. Update them in the ULP directly,
                  // don't move it here.

typedef enum {
  TASK_ERR_NO_ERR,
  TASK_ERR_SDIO_TOO_MANY_ERRORS,
  TASK_ERR_PACKET_NOT_TRANSMITTED_FAIL_TO_ATTACH,
  TASK_ERR_PACKET_NOT_TRANSMITTED_BAD_SIGNAL,
  TASK_ERR_LAST_TASK_TERMINATED_BY_USER,
  TASK_ERR_EEPROM_IO
} error_code_et;

typedef struct {
  char node_id[6];
  char i_d_indicator[4];
  char test_id[8];
  char packet_index[8];
} file_path_field_t;

typedef struct {
  char rsrp[10];
  char rsrq[10];
  char snr[10];
  char ecl[10];
  char pci[10];
  char earfcn[10];
  char cell_id[20];
  char csq[10];
} radio_info_t;

typedef struct {
  char node_id[10];          // UE_ID 3-{001}
  char packet_index[10];     // Pack_Index 3-{001}
  char module_type[20];      // module_type, see module_on_baord_et
  char network_operator[10]; // Operator 3-{001}
  char app_type[10];         // APP_Type 3-{001}
  char sleep_timer[10];      //
  radio_info_t radio_info;
  char temperature[8]; //
  char humidity[8];    //
  char v_bat[15];
  char ubhv[10];            // UE base board hardware version  (UBHV) 3-{001}
  char umhv[10];            // UE module board hardware version (UMHV) 3{001}
  char msv[10];             // mcu software version (MSV) 2{v1}
  char err_code[10];        // error code, 2 digits
  char test_id[10];         //
  char ul_packet_size[10];  // ul pack size
  char ul_total_packet[10]; // total packet number
} ul_packet_t;

/* Exported global variables ***********************************************/

extern uint8_t main_uart_rx_buf[];
extern uint8_t main_uart_tx_buf[];
extern uint8_t main_rx_complete_flag; // 1 if the RX IDLE, ready to be read.
extern uint16_t main_rx_byte_cnt;
extern uint8_t main_uart_ready_to_cdc_flag;

extern uint8_t dbg_log_buf1[];
extern uint8_t dbg_log_buf2[];
extern uint8_t dbg_log_buf_choice;
extern uint8_t dbg_log_buf_ready;
extern uint32_t dbg_log_byte_cnt;
extern uint8_t dbg_log_block_ready_flag;

extern uint8_t imei[];     // buffer for IMEI
extern char socket_num[];  // UDP socket number
extern uint8_t csq[];      // CSQ
extern uint8_t firmware[]; // firmware
extern radio_info_t radio_info_st;
extern uint8_t close_socket_flag;
extern uint8_t create_socket_flag;
extern uint8_t stop_echo_flag;
extern uint8_t net_attached_flag;
extern uint8_t ul_success_flag;
extern uint8_t init_cdp_flag;

extern module_on_board_et e_module_type;
extern network_operator_et e_network_operator;

extern ul_packet_t ul_packet_st;
extern task_monitor_t g_tm_st;
extern file_path_field_t file_path_field_st;

/* Functions ***************************************************************/

/* ## EEPROM IO post-processing ********************************************/

void assign_module_on_board_str(char *dest_module_name_str);
void assign_network_operator_str(char *dest_network_operator_str);

/**
   @brief Process the information in BCM, update the UL packet field. Prepare to
   export, etc.
   @param bcm_st: this is a global variable, but just put it here anyway.
   @return None.
   @note Make sure you read BCM from EEPROM before calling this function. The
   ul_packet_st will be updated. But it is not an input here.
*/
void process_board_constant_meta(eeprom_board_constant_meta_t *bcm_st);

/**
   @brief Process the information in BVM, update the ULP fields accordingly.
   @param bvm_st: variable meta.
   @param ulp: ulink packet stuct.
   @return None.
   @note Called this function after BVM is actually read.
*/
void process_board_variable_meta(eeprom_board_variable_meta_t *bvm_st);

void process_eeprom_task_monitor(eeprom_task_monitor_t *tm_st);

void assign_task_monitor_temp_variables();

void export_one_field(char *key_str, char *value_str);

/**
   @brief Export the BCM to USB VCP.
   @param bcm_st: board constat meta for EEPROM IO.
   @return None.
   @note Call this after eeprom_read_board_constant_meta() and
   process_board_constant_meta().
*/
void export_bcm_to_usb_vcp(eeprom_board_constant_meta_t *bcm_st);
void export_bvm_to_usb_vcp(eeprom_board_variable_meta_t *bvm_st);
void export_tm_to_usb_vcp(eeprom_task_monitor_t *tm_st);

void determine_work_mode_after_loading_eeprom();
void update_task_monitor_end_of_run();

void update_board_variable_meta();
void update_eeprom_task_monitor();

/**
   @brief Generate the file name according to the settings in the task.
   @param None.
   @return None.
   @note Make sure you call this function when task monitor is properly
   procesed.
*/
void generate_log_file_name(char *dest_file_path_buf);

/* ## UE UL task control ***************************************************/

/**
    @brief Send AT command to NB-IoT Module
    @param cmd_buf: char array storing the command
    @return None.
    @note The return information from the UART will be forwarded to USB CDC.
   Watch that on the host PC.
*/
void mod_send_cmd(char *cmd_buf);
void module_reset(uint8_t is_pull_up_needed);
void reset_ue(void);
void main_uart_rx_idle_irq_handler();
void dbg_uart_rx_irq_handler();
void HAL_UART_RxHalfCpltCallback(UART_HandleTypeDef *huart); // overloading
void notify_sdio_data_ready();

/* Migrated from XH below **************************************************/

void fill_udp_packet();
char *Int2String(int num, char *str);
int String2Int(char *str);
/**
   @brief Check whether "OK" is in the return value
   @param None.
   @return 1 if OK presents, 0 otherwise.
*/
uint8_t at_has_ok_in_return(void);
void print_at_return_msg(void);
void string_2_hexstr(char *str, char *hex_str);
void hexstr_2_str(char *hex_str, char *str);
void print_erro(char *erro_reason);

void fliter_28_35_95_rsrq(char *Radio_Res);
void fliter_28_35_95_snr(char *Radio_Res);
void fliter_28_35_95_ecl(char *Radio_Res);
void fliter_28_35_95_pci(char *Radio_Res);
void fliter_28_35_95_earfcn(char *Radio_Res);
void fliter_28_35_95_cell_id(char *Radio_Res);

char *fliter_26_earfcn(char *F_begin);
char *fliter_26_pci(char *F_begin);
char *fliter_26_cell_id(char *F_begin);
char *fliter_26_rsrp(char *F_begin);
char *fliter_26_rsrq(char *F_begin);
char *fliter_26_snr(char *F_begin);
char *fliter_26_ecl(char *F_begin);

char *fliter_me3616_ecl(char *Radio_Res);
char *fliter_me3616_band(char *Radio_Res);
char *fliter_me3616_snr(char *Radio_Res);
char *fliter_me3616_rsrq(char *Radio_Res);
char *fliter_me3616_rsrp(char *Radio_Res);
char *fliter_me3616_cell_id(char *Radio_Res);
char *fliter_me3616_pci(char *Radio_Res);
char *fliter_me3616_earfcn(char *Radio_Res);

void fliter_28_35_95_radio_info(void);
void fliter_26_radio_info(void);
void fliter_me3616_radio_info(void);

// BG96 related functions
uint8_t is_bg96_dl_packet_delivered(void);
void parse_bg96_ecl(void);
void parse_bg96_qeng(void);
void bg96_generate_ul_packet_payload(char *dest_buf, char *dest_msg_len_str);

// SARAR410M02B realted functions
void sara_make_ul_packet(char *dest_buf);
void sara_get_radio_info(void);

// BC66 related functions

void parse_bc66_qeng(void);
void post_run_module_control();
/************************************************************************/

void parse_close_echo(void);
void parse_get_csq(void);
void parse_get_firmware(void);
void parse_radio_info(void);
void parse_down_pack_cdp(void);
void parse_down_pack_udp(void);
void parse_at_ping(void);
void parse_close_socket(void);
void parse_create_socket(void);
void parse_bind_sock(void);
void parse_send_pack_result(void);
void parse_set_apn(void);
void parse_stop_nnmi(void);
void parse_at_result(int at_command_type);

void at_qualcomm_create_pdp_context(void);
void at_close_echo(void);
void at_close_nnmi(void);
void at_get_module_info();
void at_create_socket();
void at_close_socket();
void at_send_udp(char *payload[1000]);
void at_get_csq();
void at_get_firmware_version();
void at_get_current_band();
void at_get_network_status();
void at_ping(void);
void at_read_downlink_packet(char *return_buf);
void at_get_current_time();
void at_init_cdp_server(void);
void at_set_apn(void);
void at_get_down_pack_cdp(void);
void at_get_down_pack_udp(void);

void update_peripheral_var(void);
void update_predefined_var(void);
void update_radio_info_var(void);

void pack_item_2_str(char *tmp);

/**
   @brief Generate the uplink AT command for CDP protocol
   @param at_pack: store the output results
*/
void make_at_pack_cdp(char *at_pack);
void make_at_pack_udp_bc28(char *at_pack, char *sock_num);
void make_at_pack_udp_bc26(char *at_pack);
void make_at_pack_udp_me3616(char *at_pack, char *sock_num);
/**
   @brief Interface for making the packets. Switch the module type inside.
   @param at_pack: store the outptu results
*/
void make_at_pack_udp(char *at_pack, char *sock_num);

/**
   @brief The follow two are deprecated: use make_at_pack() instead.
*/
void fill_up_pack_cdp(char *at_pack);
void fill_up_pack_udp(char *at_pack, char *sock_num);

void get_down_init_info(char *down_pack);
void get_init_pack(void);

/* void update_eeprom_items(char *sleep_timer, char *app_type, char *test_id,
 */
/*                          char *total_packet, char *ul_packet_size); */

/**
   @brief This function is DEPRECATED. It is separated into two parts:
   (1) Generate the packet
   (2) Sending in it the sensing pipeline.
*/
void send_test_pack(void);


/**
   @brief The actual packet is sent during the sensing pipeline. Such that the whole period will be captured.
   @param CMD: the command to be send, AT command with payload.
   @return None
   @note If the module is BG96, the AT command is generated specifically.
*/
void send_test_packet_in_pipeline(char *command);

/**
   @brief Generate the AT command for UL field test packet. 
   @param output_cmd: the output array storing the return command.
   @note If the module is BG96, the packet only has payload. The AT command header should be implemented at where the packet is sent. The message length should be calculated in send_test_packet_in_pipeline().
*/
void wrap_up_test_packet(char *output_cmd);

void mod_analyze_downlink_packet(); /*!< FIXME: impl in get_down_init_info() */
void mod_analyze_network_status();
void mod_main_uart_dma_config(); /*!< FIXME: Do not need this. */

#ifdef __cplusplus
}
#endif
#endif
