#include "nb_iot_mod.h"
#include "string.h"

// Declare the module on the board. Initialize as 'undefined' first.
module_on_board_et e_module_type = MODULE_UNDEFINED;
network_operator_et e_network_operator = OPERATOR_UNDEFINED;

/**
   @brief The g_tm_st here are only for initialization. It should be overwritten
   asap after the EEPROM is loaded.
 */
task_monitor_t g_tm_st = {
    0,                     // is_task_assigned_flag
    MODE_PACKET_NUM_LIMIT, // e_test_mode
    0,                     // test_id
    1,                     // application_type
    0,                     // collect_dbg_log_flag
    100,                   // ul_total_time
    100,                   // ul_total_packet
    0,                     // packet_index
    256,                   // ul_packet_size
    25,                    // mcu_sleep_timer
    TASK_NOT_ASSIGNED,     // e_task_status
    0,                     // error_code_this_run
    /* The above will be written to EEPROM ***********************************/
    0, // is_task_finished_flag
    0, // is_module_init_ready_flag
    0  // did_module_enter_psm
};
ul_packet_t ul_packet_st;
file_path_field_t file_path_field_st = {"", "", "",
                                        ""}; // make sure they are clean.

// Main uart variables
uint8_t main_uart_rx_buf[MAIN_UART_BUF_SIZE] = {'\0'};
uint8_t main_uart_tx_buf[MAIN_UART_BUF_SIZE] = {'\0'};
uint8_t main_rx_complete_flag = 0; // 1 if the RX IDLE, ready to be read.
uint16_t main_rx_byte_cnt = 0;
uint8_t main_uart_ready_to_cdc_flag = 0;

// Dbg uart variables
uint8_t dbg_log_buf1[DBG_UART_BUF_SIZE] = {0};
uint8_t dbg_log_buf2[DBG_UART_BUF_SIZE] = {0};
// Switch between the two buffers, init as the next one
uint8_t dbg_log_buf_choice = 2;
// Tell the main function to deal with the data. slightly diff from buf_choice.
uint8_t dbg_log_buf_ready = 0;
uint8_t dbg_log_block_ready_flag = 0;
uint32_t dbg_log_byte_cnt = 0; // count the bytes received
// Private variables
uint8_t dbg_log_block_id = 0; /*!< block# for DMA transfer, 0-7 */

/* Variables from XH *******************************************************/
/*AT cmd related variables*/
radio_info_t radio_info_st = {"", "", "", "", "", "", ""};
char down_pack[600] = "";                 // buffer for down link msg
uint8_t imei[20] = "";                    // buffer for IMEI
char socket_num[2] = "";                  // UDP socket number
uint8_t csq[3] = "";                      // CSQ
uint8_t firmware[20] = "";                // firmware
char server_ip[20] = {"129.211.125.101"}; // server ip addr
char server_ip_linode[20] = "96.126.124.91";
char server_udp_port[10] = {"9678"}; // server udp port
char server_udp_port_linode[10] = "9678";

uint8_t close_socket_flag = 0;  // flag for successfully closing socket or not
uint8_t create_socket_flag = 0; // flag for successfully creating socket or not
uint8_t stop_echo_flag = 0; // a flag for closing me3616 auto at response echo
uint8_t init_cdp_flag = 0;  // regist cdp server need some steps,only once need
uint8_t parse_down_pack_ok_flag =
    0;                         //  flag for successfully parse down pack or not
uint8_t ping_success_flag = 0; // flag for successfully ping a server or not
uint8_t ul_success_flag = 0;   // flag for successfully send ul pack or not
uint8_t set_apn_flag = 0;      // flag for successfully set apn or not
uint8_t net_attached_flag = 0; // flag for ue successfully attaching network
protocol_choice_et e_tran_type =
    PROTO_UDP; // flag for protocol: 0 for udp; 1 for cdp

const uint8_t char_2d[4] = {"2d"};
const uint8_t char_dot[3] = {"2e"};
const uint8_t char_bar[3] = {"7c"};
// Xianghui

/* Functions *****************************************************************/

void assign_module_on_board_str(char *dest_module_name) {
  switch (e_module_type) {
  case MODULE_UNDEFINED:
    strcpy(dest_module_name, "Undefined");
    break;
  case BC28:
    strcpy(dest_module_name, "BC28");
    break;
  case BC35:
    strcpy(dest_module_name, "BC35");
    break;
  case BC95:
    strcpy(dest_module_name, "BC95");
    break;
  case BC26:
    strcpy(dest_module_name, "BC26");
    break;
  case BC66:
    strcpy(dest_module_name, "BC66");
    break;
  case BG36:
    strcpy(dest_module_name, "BG36");
    break;
  case BG96:
    strcpy(dest_module_name, "BG96");
    break;
  case SARAR410M02B:
    strcpy(dest_module_name, "SARAR410M02B");
    break;
  case ME3616:
    strcpy(dest_module_name, "ME3616");
    break;
  default:
    strcpy(dest_module_name, "Unknown");
    break;
  }
}

void assign_network_operator_str(char *dest_network_operator_str) {
  switch (e_network_operator) {
  case OPERATOR_UNDEFINED:
    strcpy(dest_network_operator_str, "Undefined");
    break;
  case OPERATOR_CM:
    strcpy(dest_network_operator_str, "China Mobile");
    break;
  case OPERATOR_CT:
    strcpy(dest_network_operator_str, "China Telecom");
    break;
  case OPERATOR_VZ:
    strcpy(dest_network_operator_str, "Verizon");
    break;
  default:
    break;
  }
}

void process_board_constant_meta(eeprom_board_constant_meta_t *bcm_st) {
  // Assign ulp node_id
  char node_id_ul[3] = {'\0'};
  dy_itoa_with_leading_0(g_bcm_st.node_num.value, 3, node_id_ul);
  node_id_ul[0] = g_bcm_st.node_region.value; // 'A' or 'C'
  strcpy(ul_packet_st.node_id, node_id_ul);
  // For output file naming.
  strcpy(file_path_field_st.node_id, node_id_ul);

  // Assign ulp module_on board
  e_module_type = (module_on_board_et)bcm_st->module_on_board.value;
  char mod_type_ul[4] = {'\0'};
  dy_itoa_with_leading_0((int)e_module_type, 3, mod_type_ul);
  strcpy(ul_packet_st.module_type, mod_type_ul);

  // Assign ulp.network_operator
  e_network_operator = (network_operator_et)bcm_st->network_operator.value;
  char net_op_ul[3] = "";
  dy_itoa_with_leading_0((int)e_network_operator, 3, net_op_ul);
  strcpy(ul_packet_st.network_operator, net_op_ul);

  // Assign base board hardware version
  char bbhv_ul[3] = "";
  dy_itoa_with_leading_0(bcm_st->base_board_hardware_version.value, 3, bbhv_ul);
  strcpy(ul_packet_st.ubhv, bbhv_ul);

  // Assign module board hardware version
  char mbhv_ul[3] = "";
  dy_itoa_with_leading_0(bcm_st->module_board_hardware_version.value, 3,
                         mbhv_ul);
  strcpy(ul_packet_st.umhv, mbhv_ul);
}

void process_board_variable_meta(eeprom_board_variable_meta_t *bvm_st) {
  char mcu_soft_ver_exp[5] = "";
  dy_itoa_with_leading_0(bvm_st->mcu_software_version.value, 5,
                         mcu_soft_ver_exp);
  strcpy(ul_packet_st.msv, mcu_soft_ver_exp);

  // FIXME: move all the update work to the end of the packet.
  bvm_st->mcu_wakeup_count.value += 1;                 // increment for record.
  eeprom_write_one_element(&bvm_st->mcu_wakeup_count); // update directly
}

void process_eeprom_task_monitor(eeprom_task_monitor_t *epr_tm_st) {
  // copy the eeprom data to task monitor struct.
  // Convertion: the loaded fields are the config for last run. So please modify
  // them before starting this run of field test.
  g_tm_st.is_task_assigned_flag = epr_tm_st->is_task_assigned.value;
  g_tm_st.e_test_mode = (test_mode_et)epr_tm_st->test_mode.value;
  g_tm_st.e_task_status = (task_status_et)epr_tm_st->task_status.value;
  g_tm_st.ul_packet_size = epr_tm_st->ul_pkt_size.value;
  g_tm_st.ul_total_time = epr_tm_st->ul_total_time.value;
  g_tm_st.ul_total_packet = epr_tm_st->ul_total_pkt.value;
  g_tm_st.mcu_sleep_timer = epr_tm_st->mcu_sleep_timer.value;
  g_tm_st.packet_index = epr_tm_st->ul_pkt_count.value + 1;

  // Make sure module on board is set correctly until here.
  // Determine we collect current or debug log in this run.
  if (1 == g_bcm_st.is_debug_log_supported.value) {
    if (1 == epr_tm_st->collect_debug_log_or_current.value) {
      // Alternate the choice
      g_tm_st.collect_dbg_log_flag = 0; /*!< This run */
    } else {
      g_tm_st.collect_dbg_log_flag = 1; /*!< This run */
    }
  } else {
    g_tm_st.collect_dbg_log_flag = 0;
  }

  // Update file_path_fields
  if (0 == g_tm_st.collect_dbg_log_flag) {
    file_path_field_st.i_d_indicator[0] = 'I';
  } else {
    file_path_field_st.i_d_indicator[0] = 'D';
  }

  // Load them to the ul_packet_st.
  char test_id_ul[5] = "";
  dy_itoa_with_leading_0(epr_tm_st->test_id.value, 5, test_id_ul);
  strcpy(ul_packet_st.test_id, test_id_ul);
  strcpy(file_path_field_st.test_id, test_id_ul);

  char packet_index_ul[4] = "";
  // Note that this is the incremented value
  dy_itoa_with_leading_0(g_tm_st.packet_index, 4, packet_index_ul);
  strcpy(ul_packet_st.packet_index, packet_index_ul);
  strcpy(file_path_field_st.packet_index, packet_index_ul);

  char app_tpye_ul[3] = "";
  dy_itoa_with_leading_0(epr_tm_st->application_type.value, 3, app_tpye_ul);
  strcpy(ul_packet_st.app_type, app_tpye_ul);

  char sleep_tmr_ul[6] = "";
  dy_itoa_with_leading_0(epr_tm_st->mcu_sleep_timer.value, 6, sleep_tmr_ul);
  strcpy(ul_packet_st.sleep_timer, sleep_tmr_ul);

  char ec[2] = "";
  dy_itoa_with_leading_0(epr_tm_st->err_code_last_run.value, 2, ec);
  strcpy(ul_packet_st.err_code, ec);

  char u_pack_size[10] = {""};
  dy_itoa_with_leading_0(epr_tm_st->ul_pkt_size.value, 4, u_pack_size);
  strcpy(ul_packet_st.ul_packet_size, u_pack_size);

  char u_total_pack[10] = {""};
  dy_itoa_with_leading_0(epr_tm_st->ul_total_pkt.value, 4, u_total_pack);
  strcpy(ul_packet_st.ul_total_packet, u_total_pack);

  g_tm_st.error_code_this_run = 0; // Reset first, update if error occurs.
}

void assign_task_monitor_temp_variables() {
  g_tm_st.is_task_finished_flag = 0;
  g_tm_st.did_module_enter_psm = 0;
}

void export_one_field(char *key_str, char *value_str) {
#if HAS_USB_CDC_VCP
  char disp_buf[30] = ""; // long enough
  strcpy(disp_buf, key_str);
  strcat(disp_buf, value_str);
  dy_append_newline(disp_buf);
  usb_cdc_send_string(disp_buf);
  HAL_Delay(1);
#endif
}

void export_bcm_to_usb_vcp(eeprom_board_constant_meta_t *bcm_st) {

  export_one_field("=>Board Meta (CONST)", "\n");
  export_one_field("Node ID: ", ul_packet_st.node_id);

  char module_name_str[15] = {'\0'}; // for export only actually
  assign_module_on_board_str(module_name_str);
  export_one_field("Module: ", module_name_str);

  char network_operator_str[15] = {'\0'}; // for export only, move to local
  assign_network_operator_str(network_operator_str);
  export_one_field("Operator: ", network_operator_str);

  char dl[2] = "";
  dl[0] = bcm_st->is_debug_log_supported.value + '0';
  export_one_field("DBG log support: ", dl);

  char bbhw_str[3] = "";
  dy_itoa_with_leading_0(bcm_st->base_board_hardware_version.value, 3,
                         bbhw_str);
  export_one_field("Base board HW Ver: ", bbhw_str);

  char mbhw_str[3] = "";
  dy_itoa_with_leading_0(bcm_st->module_board_hardware_version.value, 3,
                         mbhw_str);
  export_one_field("Module board HW Ver: ", mbhw_str);

  char ical_str[4] = "";
  dy_itoa_with_leading_0(bcm_st->current_calibration_value.value, 4, ical_str);
  export_one_field("I_mod calibration: ", ical_str);

  char vbc_str[4] = "";
  dy_itoa_with_leading_0(bcm_st->v_batt_calibration_value.value, 4, vbc_str);
  export_one_field("V_batt calibration: ", vbc_str);
}

void export_bvm_to_usb_vcp(eeprom_board_variable_meta_t *bvm_st) {
  export_one_field("=>Board Meta (VARIABLE)", "\n");

  export_one_field("MCU software version: ", ul_packet_st.msv);

  char ymd_exp[9] = "";
  char y[5] = "";
  char m[3] = "";
  char d[3] = "";
  uint16_t yn = (bvm_st->year_month_date.value >> 16) & 0xFFFF;
  uint8_t mn = (bvm_st->year_month_date.value >> 8) & 0xFF;
  uint8_t dn = bvm_st->year_month_date.value & 0xFF;
  dy_itoa_with_leading_0(yn, 4, y);
  dy_itoa_with_leading_0(mn, 2, m);
  dy_itoa_with_leading_0(dn, 2, d);
  strcat(ymd_exp, y);
  strcat(ymd_exp, m);
  strcat(ymd_exp, d);
  export_one_field("Date: ", ymd_exp);

  char wkupcnt_exp[10] = "";
  dy_itoa_with_leading_0(bvm_st->mcu_wakeup_count.value, 6, wkupcnt_exp);
  export_one_field("Wake up count: ", wkupcnt_exp);
}

void export_tm_to_usb_vcp(eeprom_task_monitor_t *tm_st) {
  export_one_field("=>Task Monitor", "\n");

  char ita[2] = "";
  ita[0] = g_tm_st.is_task_assigned_flag + '0';
  export_one_field("Is task assigned: ", ita);

  char tm[2] = "";
  tm[0] = (char)g_tm_st.e_test_mode + '0';
  export_one_field("Test mode: ", tm);

  export_one_field("Test ID: ", ul_packet_st.test_id);
  export_one_field("Application: ", ul_packet_st.app_type);

  char dbgi[2] = "";
  dbgi[0] = g_tm_st.collect_dbg_log_flag + '0';
  export_one_field("DBG log or I: ", dbgi);

  char ultt[5] = "";
  dy_itoa_with_leading_0(g_tm_st.ul_total_time, 5, ultt);
  export_one_field("UL total time: ", ultt);

  char ultp[5] = "";
  dy_itoa_with_leading_0(g_tm_st.ul_total_packet, 5, ultp);
  export_one_field("UL total packet: ", ultp);

  export_one_field("UL packet index: ", ul_packet_st.packet_index);

  char pktsize[4] = "";
  dy_itoa_with_leading_0(g_tm_st.ul_packet_size, 4, pktsize);
  export_one_field("UL packet size: ", pktsize);

  char slptmr[5] = "";
  dy_itoa_with_leading_0(g_tm_st.mcu_sleep_timer, 5, slptmr);
  export_one_field("Sleep timer: ", slptmr);

  char tstatus[2] = "";
  tstatus[0] = (char)g_tm_st.e_task_status + '0';
  export_one_field("Task status: ", tstatus);

  export_one_field("Error code last run: ", ul_packet_st.err_code);
}

void determine_work_mode_after_loading_eeprom() {
  if (0 == g_tm_st.is_task_assigned_flag) {
    // Not assigned
    work_mode = STATE_INIT_PACKET;
  } else {
    // Task assigned by the server
    if (0 == g_tm_st.is_task_finished_flag) {
      // Task not finished;
      work_mode = STATE_FIELD_TEST;
    } else {
      // Ready for the next round
      work_mode = STATE_INIT_PACKET;
      /*Xianghui*/
      config_rtc_standby_auto_wakeup_after(1);
      HAL_PWR_EnterSTANDBYMode();
      // fixed-TODO: Go to sleep
    }
  }
}

void update_task_monitor_end_of_run() {
  if (g_tm_st.packet_index == g_tm_st.ul_total_packet) {
    // we already transmit enough packet for this run.
    g_tm_st.is_task_finished_flag = 1;
    g_tm_st.e_task_status = TASK_FINISHED_SUCCESSFULLY;
  }
}

void mod_main_uart_dma_config() {
  /* HAL_UART_Receive_DMA(&MAIN_UART, main_uart_rx_buf, MAIN_UART_BUF_SIZE); */
}

void main_uart_rx_idle_irq_handler() {
  volatile uint32_t cnt_temp;
  uint8_t local_buf[512] = {'\0'};

  if (RESET != (__HAL_UART_GET_FLAG(&MAIN_UART, UART_FLAG_IDLE))) {
    __HAL_UART_CLEAR_IDLEFLAG(&MAIN_UART);
    HAL_UART_DMAStop(&MAIN_UART);

    cnt_temp = MAIN_UART.hdmarx->Instance->CNDTR;
    main_rx_byte_cnt = MAIN_UART_BUF_SIZE - cnt_temp;
    main_rx_complete_flag = 1;
    for (int i = 0; i < main_rx_byte_cnt; i++) {
      UserTxBufferFS[i] = main_uart_rx_buf[i];
      local_buf[i] = main_uart_rx_buf[i];
    }
    if (STATE_DEMOS == work_mode) {
      // Forward the results to USB HOST.
      CDC_Transmit_FS(UserTxBufferFS, main_rx_byte_cnt);
      HAL_UART_Receive_DMA(&MAIN_UART, main_uart_rx_buf, MAIN_UART_BUF_SIZE);
    }
    /* main_uart_ready_to_cdc_flag = 1; */
  }
}

void module_reset(uint8_t is_pull_up_needed) {
  uint8_t effect_state = 0; // by default, drive the pin low to reset.
  if (is_pull_up_needed) {
    effect_state = 1;
  }

  uint16_t reset_timer = 0;
  switch (e_module_type) {
  case BG96:
    reset_timer = 250;
    break;
  case ME3616:
    reset_timer = 420;
    break;
  default:
    reset_timer = 100;
    break;
  }
  HAL_GPIO_WritePin(M_RESET_GPIO_Port, M_RESET_Pin, effect_state);
  HAL_Delay(reset_timer);
  HAL_GPIO_WritePin(M_RESET_GPIO_Port, M_RESET_Pin, !effect_state);

  // Apply PWR_ON to part of the modules.
  if (BC26 == e_module_type or BG96 == e_module_type or
      SARAR410M02B == e_module_type or BC66 == e_module_type or
      ME3616 == e_module_type) {

    uint16_t pwr_on_delay;
    switch (e_module_type) {
    case BC26:
      pwr_on_delay = 80;
      break;
    case BC66:
      pwr_on_delay = 600;
      break;
    case BG96:
      pwr_on_delay = 700;
      break;
    case SARAR410M02B:
      pwr_on_delay = 150;
      break;
    case ME3616:
      pwr_on_delay = 2500;
      break;
    default:
      pwr_on_delay = 400;
      break;
    }
    // Pull down the PWR_KEY pin (Open Drain)
    HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_SET);
    HAL_Delay(pwr_on_delay);
    HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_RESET);
  }

  if (SARAR410M02B == e_module_type) {
    // TODO: add a comment to this line.
    HAL_GPIO_WritePin(M_GPIO_R1_GPIO_Port, M_GPIO_R1_Pin, GPIO_PIN_SET);
  }
}

void reset_ue(void) {
  // TODO: Merge this function with module_rest(0)
  switch (e_module_type) {
  case BC28:
  case BC95:
  case BC35:
    HAL_GPIO_WritePin(GPIOA, M_RESET_Pin, GPIO_PIN_SET);
    break;
  case BC26:
    HAL_GPIO_WritePin(GPIOA, M_RESET_Pin, GPIO_PIN_RESET);
    module_reset(0);
    HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_SET);
    break;
  case ME3616:
    HAL_GPIO_WritePin(GPIOA, M_RESET_Pin, GPIO_PIN_RESET);
    module_reset(1);
    HAL_GPIO_WritePin(M_GPIO_L4_GPIO_Port, M_GPIO_L4_Pin, GPIO_PIN_SET);
    break;
    // The above module are used in China.
  case BG96:
  case BC66:
  case SARAR410M02B:
    module_reset(0);
    break;
  default:
    HAL_GPIO_WritePin(GPIOA, M_RESET_Pin, GPIO_PIN_RESET);
    break;
  }
  /*waiting for reset NB module*/
  if ('A' != g_bcm_st.node_region.value) {
    HAL_Delay(5000);
  } else {
    HAL_Delay(2000);
  }
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
  if (huart == &DBG_UART) {
    HAL_UART_DMAStop(&DBG_UART);
    dbg_log_byte_cnt += DBG_UART_BUF_SIZE;
    if (dbg_log_buf_choice == 1) {
      HAL_UART_Receive_DMA(&DBG_UART, dbg_log_buf1, DBG_UART_BUF_SIZE);
      dbg_log_buf_choice = 2; // swap, for next round
      dbg_log_buf_ready = 2;
    } else if (dbg_log_buf_choice == 2) {
      HAL_UART_Receive_DMA(&DBG_UART, dbg_log_buf2, DBG_UART_BUF_SIZE);
      dbg_log_buf_choice = 1; // swap, for next round
      dbg_log_buf_ready = 1;
    } else {
      usb_cdc_send_string("[ERR] Unknown dbg log buf choice. [a]\n");
    }
    LED1_TOGGLE;
  }
}

void update_board_variable_meta() {
  // TODO: write the new time to BVM here, for setting the SD card file
  // timestamp.
}

void update_eeprom_task_monitor() {
  // Convertion: The fields here are the end results and configuration of this
  // run. The next run of field test should decide its config by updating these
  // fields.
  g_eeprom_tm_st.is_task_assigned.value = g_tm_st.is_task_assigned_flag;
  g_eeprom_tm_st.test_mode.value = g_tm_st.e_test_mode;
  /* g_eeprom_tm_st.test_id.value = g_tm_st.test_id; */
  /* g_eeprom_tm_st.application_type.value = g_tm_st.application_type; */
  g_eeprom_tm_st.collect_debug_log_or_current.value =
      g_tm_st.collect_dbg_log_flag;
  /* g_eeprom_tm_st.ul_total_time.value = g_tm_st.ul_total_time; */
  /* g_eeprom_tm_st.ul_total_pkt.value = g_tm_st.ul_total_packet; */
  g_eeprom_tm_st.ul_pkt_count.value = g_tm_st.packet_index;
  /* g_eeprom_tm_st.ul_pkt_size.value = g_tm_st.ul_packet_size; */
  /* g_eeprom_tm_st.mcu_sleep_timer.value = g_tm_st.mcu_sleep_timer; */
  g_eeprom_tm_st.task_status.value = g_tm_st.e_task_status;
  g_eeprom_tm_st.err_code_last_run.value = g_tm_st.error_code_this_run;
}

void generate_log_file_name(char *dest_file_path_buf) {
  char file_path[30] = "";
  const char connector[2] = "_";
  strcpy(file_path, file_path_field_st.node_id);
  strcat(file_path, connector);
  strcat(file_path, file_path_field_st.i_d_indicator);
  strcat(file_path, connector);
  strcat(file_path, file_path_field_st.test_id);
  strcat(file_path, connector);
  strcat(file_path, file_path_field_st.packet_index);
  strcat(file_path, ".log");
  strcpy(dest_file_path_buf, file_path);
}

void print_at_return_msg(void) {
#if HAS_USB_CDC_VCP
  CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
#endif
}

/* BG96 control code **********************************************/
uint8_t at_has_ok_in_return(void) {
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    return 1;
  } else {
    return 0;
  }
}

void at_qualcomm_create_pdp_context(void) {
  char CMD[70] = "";
  uint8_t success_count = 0;

  strcpy(CMD, "AT+QICSGP=1\r\n");
  mod_send_cmd(CMD);
  print_at_return_msg();

  strcpy(CMD, "AT+QIACT=1\r\n");
  mod_send_cmd(CMD);
  print_at_return_msg();

  success_count += at_has_ok_in_return();
  strcpy(CMD, "AT+QIOPEN=1,2,\"UDP Service\",\"");
  // "1" is the contextID; "2" is the connectID
  // contextID is used in IP related services, such as Ping.
  // ConnectID is used in socket, most cases.

  strcat(CMD, server_ip_linode);
  strcat(CMD, "\",0,");
  strcat(CMD, server_udp_port_linode);
  strcat(CMD, ",0\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  print_at_return_msg();
  success_count += at_has_ok_in_return();

  mod_send_cmd("AT+QISTATE=0,1\r\n");
  print_at_return_msg();

  if (2 == success_count) {
    create_socket_flag = 1;
  } else {
    create_socket_flag = 0;
  }
}

void parse_bg96_ecl(void) {
  if (BG96 != e_module_type) {
    return;
  }
  // If not attached, reply: ERROR
  // Typical reply: +QCFG: "celevel",1

  if (NULL != strstr(main_uart_rx_buf, "ERROR")) {
    usb_cdc_send_string("[WRN] BG96 ECL not avaiable\n");
  } else if (NULL != strstr(main_uart_rx_buf, "celevel")) {
    if (NULL != strstr(main_uart_rx_buf, "0")) {
      strcpy(radio_info_st.ecl, "0");
    } else if (NULL != strstr(main_uart_rx_buf, "1")) {
      strcpy(radio_info_st.ecl, "1");
    } else if (NULL != strstr(main_uart_rx_buf, "2")) {
      strcpy(radio_info_st.ecl, "2");
    } else {
      usb_cdc_send_string("[ERR] Unknown ECL for BG96\n");
    }
  }
  export_one_field("BG96 ECL: ", radio_info_st.ecl);
}

void parse_bg96_qeng(void) {
  // Example reply: +QENG:
  /* "servingcell","NOCONN","CAT-NB","FDD",460,11,DDA1451,280,2506,5,0,0,69C9,-84,-17,-67,
   * 8, 44 */
  /*  Order(split by comma): +QENG: */
  /*  "servingcell",<state>,"rat",<is_tdd>,<mcc>,<mnc>, <cellid>, <pcid>,
   * <earfcn>, <freq_band_ind>, <ul_bandw idth>, <dl_bandwidth>, <tac>, <rsrp>,
   * <rsrq>, <rssi>, <sinr>, <srxlev> */
  char delim[] = ",";
  uint8_t item_idx = 0;

  /* print_at_return_msg(); */

  char *ptr = strtok(main_uart_rx_buf, delim);

  while (NULL != ptr and item_idx < 19) {
    // Note: the index starts from 0;
    switch (item_idx) {
      // TODO: add a condition to skip abnormal values. or maybe it's too long
    case 6:
      strcpy(radio_info_st.cell_id, ptr);
      break;
    case 7:
      strcpy(radio_info_st.pci, ptr);
      break;
    case 8:
      strcpy(radio_info_st.earfcn, ptr);
      break;
    case 13:
      strcpy(radio_info_st.rsrp, ptr);
      break;
    case 14:
      strcpy(radio_info_st.rsrq, ptr);
      break;
    case 16:
      strcpy(radio_info_st.snr, ptr);
      break;
    default:
      break;
    }
    ptr = strtok(NULL, delim);
    item_idx++;
  }
}

void bg96_generate_ul_packet_payload(char *dest_buf, char *dest_msg_len_str) {

  char packet_buf[600] = {""};
  char msg_len_str[ITOA_BUF_LEN] = {""};

  // Run this for the new BG96 (may or may not help)
  //  strcpy(ul_packet_st.test_id, "00101");
  //  strcpy(ul_packet_st.ul_total_packet, "030");

  pack_item_2_str(packet_buf);

  dy_itoa(strlen(packet_buf), msg_len_str);
  dy_shift_leading_null_chars(msg_len_str);

  strcpy(dest_msg_len_str, msg_len_str);
  strcat(packet_buf, "\r\n");
  strcpy(dest_buf, packet_buf);
}

/* SARAR410M02B control code *************************************************/
void sara_make_ul_packet(char *dest_buf) {
  char packet_buf[600] = {""};
  char msg_len_str[ITOA_BUF_LEN] = {""};

  pack_item_2_str(packet_buf);

  dy_itoa(strlen(packet_buf), msg_len_str);
  dy_shift_leading_null_chars(msg_len_str);

  strcpy(dest_buf, "AT+USOST=0,\"96.126.124.91\",9678,"); // AT command header
  strcat(dest_buf, msg_len_str);                          // Message length
  strcat(dest_buf, ",\"");
  strcat(dest_buf, packet_buf);
  strcat(dest_buf, "\"\r\n");
}

void sara_get_radio_info(void) {
  mod_send_cmd("AT+CEREG?\r\n");
  if (NULL != strstr(main_uart_rx_buf, "3,1")) {
    // Attached.
    char *s_ptr = strstr(main_uart_rx_buf, "\",\""); // start pattern
    s_ptr += 3;
    char *end_ptr = strstr(s_ptr, "\","); // end pattern
    strncpy(radio_info_st.cell_id, s_ptr, end_ptr - s_ptr);
  }
  mod_send_cmd("AT+UCGED?\r\n");
  if (NULL != strstr(main_uart_rx_buf, "+RSRP")) {
    char *ptr = strstr(main_uart_rx_buf, ": ");
    ptr += 2;
    ptr = strtok(ptr, ",");
    strcpy(radio_info_st.pci, ptr);

    ptr = strtok(NULL, ",\"");
    strcpy(radio_info_st.earfcn, ptr);

    ptr = strtok(NULL, "\",");
    strcpy(radio_info_st.rsrp, ptr);

    ptr = strtok(NULL, "+RSRQ: ");
    ptr = strtok(NULL, ",");
    ptr = strtok(NULL, ",\"");
    ptr = strtok(NULL, "\",");
    strcpy(radio_info_st.rsrq, ptr);
  }
  strcpy(radio_info_st.snr, "99"); // Not avaiable for SRARR410M02B
  strcpy(radio_info_st.ecl, "9");  // Not avaiable for SRARR410M02B
}

/* BC66 control code *********************************************************/
void parse_bc66_qeng(void) {
  // Example: +QENG: 0,5184,3,143,"37D2C1E",-94,-7,0,-127,13,"E486",0,
  // Order: ConnectID, EARFCN, X, PCI, CellID, RSRP, RSRQ, RSSI, SNR, Band, TAC,
  // ECL
  uint8_t item_idx = 0;

  print_at_return_msg();

  char *ptr = strtok(main_uart_rx_buf, ",");

  while (NULL != ptr and item_idx < 13) {
    // Note: the index starts from 0;
    switch (item_idx) {
      // TODO: add a condition to skip abnormal values. or maybe it's too long
    case 1:
      strcpy(radio_info_st.earfcn, ptr);
      break;
    case 3:
      strcpy(radio_info_st.pci, ptr);
      break;
    case 4:
      strcpy(radio_info_st.cell_id, ptr);
      break;
    case 5:
      strcpy(radio_info_st.rsrp, ptr);
      break;
    case 6:
      strcpy(radio_info_st.rsrq, ptr);
      break;
    case 8:
      strcpy(radio_info_st.snr, ptr);
      break;
    case 11:
      strcpy(radio_info_st.ecl, ptr);
      break;
    default:
      break;
    }
    ptr = strtok(NULL, ",");
    item_idx++;
  }
}

// TODO: improve the following code if time allows.
/* Migrated from XH's code
 ***************************************************/

void notify_sdio_data_ready(DMA_HandleTypeDef *hdma_m2m) {
  usb_cdc_send_string("RunHERE");
  if (dbg_log_block_id == 0) {
    // The 8th block transfer completed.
    dbg_log_block_ready_flag = 1;
  }
}

void mod_send_cmd(char *cmd_buf) {
  memset(main_uart_rx_buf, 0, sizeof(main_uart_rx_buf));
  main_rx_byte_cnt = 0;
  main_rx_complete_flag = 0;
  HAL_UART_Receive_DMA(&MAIN_UART, (uint8_t *)main_uart_rx_buf,
                       MAIN_UART_BUF_SIZE); // Start UART receiver
//  HAL_UART_Transmit(&MAIN_UART, (uint8_t *)cmd_buf, strlen(cmd_buf),
//                    2000); //	Send AT CMD to UE
  HAL_UART_Transmit_DMA(&MAIN_UART, (uint8_t *)cmd_buf, strlen(cmd_buf)); //	Send AT CMD to UE
  switch (e_module_type) { // waiting for MCU gets responds
  case BG96:
    HAL_Delay(300);
    break;
  case BC66:
    HAL_Delay(300);
    break;
  case SARAR410M02B:
    HAL_Delay(200);
    break;
  case BC28:
    HAL_Delay(1000);
    break;
  case ME3616:
    HAL_Delay(1500);
    break;
  default:
    HAL_Delay(1200);
    break;
  }
}

void mod_send_field_test_pack(char *cmd_buf) {
  memset(main_uart_rx_buf, 0, sizeof(main_uart_rx_buf));
  main_rx_byte_cnt = 0;
  main_rx_complete_flag = 0;
  HAL_UART_Receive_DMA(&MAIN_UART, (uint8_t *)main_uart_rx_buf,
                       MAIN_UART_BUF_SIZE); // Start UART receiver
//  HAL_UART_Transmit(&MAIN_UART, (uint8_t *)cmd_buf, strlen(cmd_buf),
//                    2000); // Send AT CMD to UE
  HAL_UART_Transmit_DMA(&MAIN_UART, (uint8_t *)cmd_buf, strlen(cmd_buf)); // Send AT CMD to UE
  // no waiting here
}

char *Int2String(int num, char *str) {
  int i = 0;
  if (num < 0) {
    num = -num;
    str[i++] = '-';
  }
  do {
    str[i++] = num % 10 + 48;
    num /= 10;
  } while (num);

  str[i] = '\0';

  int j = 0;
  if (str[0] == '-') {
    j = 1;
    ++i;
  }
  for (; j < i / 2; j++) {

    str[j] = str[j] + str[i - 1 - j];
    str[i - 1 - j] = str[j] - str[i - 1 - j];
    str[j] = str[j] - str[i - 1 - j];
  }
  return str;
}

int String2Int(char *str) {
  char flag = '+';
  long res = 0;

  if (*str == '-') {
    ++str;
    flag = '-';
  }
  while (*str >= 48 && *str < 57) {
    res = 10 * res + *str++ - 48;
  }

  if (flag == '-') {
    res = -res;
  }
  return (int)res;
}

void string_2_hexstr(char *str, char *hex_str) {
  char tmp[3] = {""};
  strcpy(hex_str, "");
  int i = 0;
  for (i = 0; i < strlen(str); i++) {
    strcpy(tmp, "");
    sprintf(tmp, "%x", *(str + i));
    strcat(hex_str, tmp);
  }
}

uint16_t String2Int_id(char *str) {
  char flag = '+';
  uint16_t res = 0;

  if (*str == '-') {
    ++str;
    flag = '-';
  }
  while (*str >= 48 && *str < 57) {
    res = 10 * res + *str++ - 48;
  }

  if (flag == '-') {
    res = -res;
  }
  return (uint16_t)res;
}

void hexstr_2_str(char *hex_str, char *str) {
  strcpy(str, "");
  if ((strlen(hex_str) % 2) == 0) {
    char tmp[5] = {""};
    int i = 0;
    for (i = 0; i < strlen(hex_str); i = i + 2) {
      strncpy(tmp, hex_str + i, 2);
      if (strcmp(tmp, char_2d) == 0) {
        strcat(str, "-");
      } else if (strcmp(tmp, char_dot) == 0) {
        strcat(str, ".");
      } else if (strcmp(tmp, char_bar) == 0 || strcmp(tmp, "7C") == 0) {
        strcat(str, "|");
      } else if (strcmp(tmp, "39") == 0) {
        strcat(str, "9");
      } else {
        sprintf(tmp, "%c", String2Int(tmp) + 18);
        strcat(str, tmp);
      }
    }
  }
}

void print_erro(char *erro_reason) { usb_cdc_send_string(erro_reason); }

void at_init_cdp_server(void) {
  // ue just needs once below operations in it`s all life
  char CMD[512] = {""};
  init_cdp_flag = 0; // if successfully init cdp server, init_cdp_flag=9
  strcpy(CMD, "AT+CFUN=0\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+NBAND\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+CGSN=1\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+NCDP=180.101.147.115,5683\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+NRB\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(4000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+CFUN=1\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+CSCON=1\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+CEREG=4\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
  strcpy(CMD, "AT+CGATT=1\r\n");
  CDC_Transmit_FS(CMD, strlen(CMD));
  mod_send_cmd(CMD);
  CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(1000);
  if (strstr(main_uart_rx_buf, "OK") != NULL) {
    init_cdp_flag++;
  }
}

void fliter_28_35_95_rsrq(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "RSRQ");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 5;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.rsrq[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse RSRQ\n");
  }
  // usb_cdc_send_string(radio_info.rsrq);
}

void fliter_28_35_95_snr(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "SNR");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 4;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.snr[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse SNR\n");
  }
  // usb_cdc_send_string(radio_info.snr);
}

void fliter_28_35_95_ecl(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "ECL");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 4;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.ecl[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse ECL\n");
  }
  // usb_cdc_send_string(radio_info.ecl);
}

void fliter_28_35_95_pci(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "PCI");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 4;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.pci[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse PCI\n");
  }
  // usb_cdc_send_string(radio_info.pci);
}

void fliter_28_35_95_earfcn(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "EARFCN");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 7;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.earfcn[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse EARFCN\n");
  }
  // usb_cdc_send_string(radio_info.earfcn);
}

void fliter_28_35_95_cell_id(char *Radio_Res) {
  int j = 0;
  char *F_band = strstr(Radio_Res, "Cell");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 8;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.cell_id[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse CELL_ID\n");
  }
  // usb_cdc_send_string(radio_info.cell_id);
}

char *fliter_26_earfcn(char *F_begin) {
  /*
             earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
    +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
    +QENG: 1,3734,2,89,-119
    +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = strstr(F_begin, "QENG");
  if (F_band >= 0) {
    j = 0;
    F_band = F_band + 8;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.earfcn[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse earfcn\n");
  }
  usb_cdc_send_string(radio_info_st.earfcn);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return F_band + 3;
}

char *fliter_26_pci(char *F_begin) {
  /*
             earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
    +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
    +QENG: 1,3734,2,89,-119
    +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.pci[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse pci\n");
  }
  usb_cdc_send_string(radio_info_st.pci);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return F_band + 2;
}

char *fliter_26_cell_id(char *F_begin) {
  /*
             earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
    +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
    +QENG: 1,3734,2,89,-119
    +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (*(F_band) != 34) {
      radio_info_st.cell_id[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse cell_id\n");
  }
  usb_cdc_send_string(radio_info_st.cell_id);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return F_band + 2;
}

char *fliter_26_rsrp(char *F_begin) {
  /*
             earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
    +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
    +QENG: 1,3734,2,89,-119
    +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.rsrp[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse rsrp\n");
  }
  usb_cdc_send_string(radio_info_st.rsrp);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return F_band + 1;
}

char *fliter_26_rsrq(char *F_begin) {
  /*
           earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
  +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
  +QENG: 1,3734,2,89,-119
  +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.rsrq[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse rsrq\n");
  }
  usb_cdc_send_string(radio_info_st.rsrq);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  F_band++;
  while (*(F_band) != 44) {
    F_band++;
  }
  return F_band + 1;
}

char *fliter_26_snr(char *F_begin) {
  /*
         earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
  +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
  +QENG: 1,3734,2,89,-119
  +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.snr[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse snr\n");
  }
  usb_cdc_send_string(radio_info_st.snr);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");

  F_band++;
  while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
    F_band++;
  }
  F_band = F_band + 2;
  while (*(F_band) != 44) {
    F_band++;
  }
  return F_band + 1;
}

char *fliter_26_ecl(char *F_begin) {
  /*
          earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
   +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
   +QENG: 1,3734,2,89,-119
   +QENG: 1,3736,2,411,-105*/
  //','=44
  int j = 0;
  char *F_band = F_begin;
  if (F_band >= 0) {
    j = 0;
    while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '-') {
      radio_info_st.ecl[j++] = *(F_band++);
    }
  } else {
    print_erro("Erro Occured when parse snr\n");
  }
  usb_cdc_send_string(radio_info_st.ecl);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");

  return F_band;
}

char *fliter_me3616_ecl(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    radio_info_st.ecl[j++] = *(F++);
  } else {
    print_erro("Erro Occured when parse ecl\n");
  }
  usb_cdc_send_string(radio_info_st.ecl);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  Radio_Res = F;
  return Radio_Res;
}

char *fliter_me3616_band(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      F++;
    }
    ++F;
    while (*(F) != 44) {
      F++;
    }
    Radio_Res = F + 1;
  } else {
    print_erro("Erro Occured when parse Band\n");
  }
  // usb_cdc_send_string(radio_info.);
  // HAL_Delay(200);
  // usb_cdc_send_string("=*=\n");

  return Radio_Res;
}

char *fliter_me3616_snr(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      radio_info_st.snr[j++] = *(F++);
    }
    Radio_Res = ++F;
  } else {
    print_erro("Erro Occured when parse SNR\n");
  }
  usb_cdc_send_string(radio_info_st.snr);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");

  return Radio_Res;
}

char *fliter_me3616_rsrq(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      radio_info_st.rsrq[j++] = *(F++);
    }
    F++;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      F++;
    }
    Radio_Res = ++F;
  } else {
    print_erro("Erro Occured when parse RSRQ\n");
  }
  usb_cdc_send_string(radio_info_st.rsrq);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return Radio_Res;
}

char *fliter_me3616_rsrp(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      radio_info_st.rsrp[j++] = *(F++);
    }
  } else {
    print_erro("Erro Occured when parse RSRP\n");
  }
  usb_cdc_send_string(radio_info_st.rsrp);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  Radio_Res = ++F;
  return Radio_Res;
}

char *fliter_me3616_cell_id(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (*(F) != 34) {
      radio_info_st.cell_id[j++] = *(F++);
    }
  } else {
    print_erro("Erro Occured when parse Cell ID\n");
  }
  usb_cdc_send_string(radio_info_st.cell_id);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  Radio_Res = F + 2;
  return Radio_Res;
}

char *fliter_me3616_pci(char *Radio_Res) {
  int j = 0;
  char *F = Radio_Res;
  if (F >= 0) {
    j = 0;
    while (('0' <= *(F) && *(F) <= '9') || *(F) == '-') {
      radio_info_st.pci[j++] = *(F++);
    }
    Radio_Res = F + 2;
  } else {
    print_erro("Erro Occured when parse PCI\n");
  }
  usb_cdc_send_string(radio_info_st.pci);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  return Radio_Res;
}

char *fliter_me3616_earfcn(char *Radio_Res) {
  int j = 0;
  char *F = strstr(Radio_Res, "*MENGINFOSC:");
  if (F >= 0) {
    j = 0;
    F = F + 13;
    while ('0' <= *(F) && *(F) <= '9' || *(F) == '-') {
      radio_info_st.earfcn[j++] = *(F++);
    }
  } else {
    print_erro("Erro Occured when parse EARFCN\n");
  }
  usb_cdc_send_string(radio_info_st.earfcn);
  HAL_Delay(200);
  usb_cdc_send_string("=*=\n");
  Radio_Res = F + 3;
  return Radio_Res;
}

void fliter_28_35_95_radio_info(void) {
  // FIXME: no RSRP here?
  fliter_28_35_95_rsrq(main_uart_rx_buf);
  fliter_28_35_95_snr(main_uart_rx_buf);
  fliter_28_35_95_ecl(main_uart_rx_buf);
  fliter_28_35_95_pci(main_uart_rx_buf);
  fliter_28_35_95_earfcn(main_uart_rx_buf);
  fliter_28_35_95_cell_id(main_uart_rx_buf);
}

void fliter_26_radio_info(void) {
  /*
             earf,-,pci,cell_id,rsrp,rsrq,rssi,snr,band,tac,ecl
    +QENG: 0,3738,2,412,"5012620",-87,-5,-82,9,8,"3A27",0,
    +QENG: 1,3734,2,89,-119
    +QENG: 1,3736,2,411,-105*/
  //','=44
  char *parse_tag = main_uart_rx_buf;
  parse_tag = fliter_26_earfcn(parse_tag);
  parse_tag = fliter_26_pci(parse_tag);
  parse_tag = fliter_26_cell_id(parse_tag);
  parse_tag = fliter_26_rsrp(parse_tag);
  parse_tag = fliter_26_rsrq(parse_tag);
  parse_tag = fliter_26_snr(parse_tag);
  parse_tag = fliter_26_ecl(parse_tag);
  usb_cdc_send_string("=====\n");
}

void fliter_me3616_radio_info(void) {
  // usb_cdc_send_string(main_uart_rx_buf);
  // HAL_Delay(1000);
  // CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
  // HAL_Delay(1000);

  char *parse_tag = main_uart_rx_buf;
  /*the order of calling bellow function can not changed*/
  parse_tag = fliter_me3616_earfcn(parse_tag);  // 1
  parse_tag = fliter_me3616_pci(parse_tag);     // 2
  parse_tag = fliter_me3616_cell_id(parse_tag); // 3
  parse_tag = fliter_me3616_rsrp(parse_tag);    // 3
  parse_tag = fliter_me3616_rsrq(parse_tag);    // 4
  parse_tag = fliter_me3616_snr(parse_tag);     // 5
  parse_tag = fliter_me3616_band(parse_tag);    // 6
  parse_tag = fliter_me3616_ecl(parse_tag);     // 7
}

void parse_close_echo(void) {
  switch (e_module_type) {
  case BC28:
    stop_echo_flag = 1;
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      stop_echo_flag = 1;
    } else {
      print_erro("Erro Occured when parse_close_echo for bc26\n");
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      stop_echo_flag = 1;
    } else {
      print_erro("Erro Occured when parse_close_echo for ME3616\n");
    }
    break;
  case BG96:
    stop_echo_flag = at_has_ok_in_return();
    break;
  default:
    break;
  }
}

void parse_get_csq(void) {
  int j = 0;
  switch (e_module_type) {
  case BC28:
    j = 0;
    if (strstr(main_uart_rx_buf, "CSQ") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CSQ");
      if (F >= 0) {
        j = 0;
        F = F + 4;
        while ('0' <= *(F) && *(F) <= '9' || *(F) == '-') {
          csq[j++] = *(F++);
        }
      }
    } else {
      print_erro("Erro Occured when parse csq\n");
    }
    break;
  case BC26:
    j = 0;
    if (strstr(main_uart_rx_buf, "CSQ") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CSQ");
      if (F >= 0) {
        j = 0;
        F = F + 5;
        while ('0' <= *(F) && *(F) <= '9') {
          csq[j++] = *(F++);
        }
      }
    } else {
      print_erro("Erro Occured when parse csq for bc26\n");
    }
    break;
  case ME3616:
    j = 0;
    if (strstr(main_uart_rx_buf, "CSQ") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CSQ");
      if (F >= 0) {
        j = 0;
        F = F + 5;
        while ('0' <= *(F) && *(F) <= '9') {
          csq[j++] = *(F++);
        }
      }
    } else {
      print_erro("Erro Occured when parse csq for bc26\n");
    }
    break;
  case SARAR410M02B: // same as BG96
  case BG96:
  case BC66:
    print_at_return_msg();
    if (NULL != strstr(main_uart_rx_buf, "CSQ:")) {
      char *ptr = main_uart_rx_buf; // locate the start of the num
      ptr += 8;
      strncpy(csq, ptr, strstr(main_uart_rx_buf, ",") - ptr);
    } else {
      usb_cdc_send_string("[ERR] CSQ return msg has error\n");
    }
    break;
  default:
    break;
  }
  export_one_field("CSQ: ", csq);
  strcpy(radio_info_st.csq, csq);
}

void parse_get_firmware(void) {
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "SECURITY") != NULL) {
      strncpy(firmware, main_uart_rx_buf + 6, 18);
    } else {
      print_erro("Erro Occured when parse at_result for "
                 "at_get_firmware_version()\n");
      return;
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "BC26") != NULL) {
      char *F = strstr(main_uart_rx_buf, "BC26");
      strncpy(firmware, F, 12);
    } else {
      print_erro("Erro Occured when parse at_result for "
                 "at_get_firmware_version()\n");
      return;
    }
    break;
  case ME3616:
    usb_cdc_send_string(main_uart_rx_buf);
    HAL_Delay(1000);
    CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
    HAL_Delay(1000);
    break;
  default:
    break;
  }
  usb_cdc_send_string(firmware);
}

void parse_rsrp(void) {
  int j = 0;
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "NUESTATS:CELL") != NULL) {
      char *F = strstr(main_uart_rx_buf, "NUESTATS:CELL");
      F += 14;
      while (*(F) != ',') {
        F++;
      }
      F++;
      while (*(F) != ',') {
        F++;
      }
      F++;
      while (*(F) != ',') {
        F++;
      }
      F++;
      while (*(F) != ',') {
        radio_info_st.rsrp[j++] = *(F++);
      }
    } else {
      usb_cdc_send_string("error occured at parse_rsrp for BC28/35/29");
    }
    break;
  default:
    break;
  }
}

void parse_radio_info(void) {
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "NUESTATS") != NULL) {
      fliter_28_35_95_radio_info();
    } else {
      print_erro("Erro Occured when parse at_result for get_radio_info()\n");
      return;
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "QENG") != NULL) {
      fliter_26_radio_info();
    } else {
      print_erro("Erro Occured when parse at_result for get_radio_info()\n");
      return;
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "MENGINFOSC") != NULL) {
      fliter_me3616_radio_info();
    } else {
      print_erro("Erro Occured when parse at_result for get_radio_info()\n");
      return;
    }
    break;
  default:
    break;
  }
}

void parse_at_ping(void) {
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ping_success_flag = 1;
    } else {
      ping_success_flag = 0;
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ping_success_flag = 1;
    } else {
      ping_success_flag = 0;
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ping_success_flag = 1;
    } else if (strstr(main_uart_rx_buf, "BUSY") != NULL) {
      usb_cdc_send_string("ping is busy\n");
    } else {
      ping_success_flag = 0;
    }
    break;
  case BG96:
    ping_success_flag = at_has_ok_in_return();
    // TODO: error may return later, check it later.
    break;
  default:
    break;
  }
  if (ping_success_flag == 1) {
    usb_cdc_send_string("ping ok\n");
  } else {
    usb_cdc_send_string("ping not ok\n");
  }
}

void parse_attach_status(void) {
  print_at_return_msg();
  HAL_Delay(300);
  // TODO: remove this delay, if works as well, do not add it back.
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "CEREG:") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CEREG");
      if (*(F + 8) == '1') {
        net_attached_flag = 1;
      }
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "CEREG:") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CEREG");
      if (*(F + 9) == '1') {
        net_attached_flag = 1;
      }
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "CEREG:") != NULL) {
      char *F = strstr(main_uart_rx_buf, "CEREG");
      if (*(F + 9) == '1') {
        net_attached_flag = 1;
      }
    }
    break;
  case BG96:
    if (NULL != strstr(main_uart_rx_buf, "CEREG:")) {
      if (NULL != strstr(main_uart_rx_buf, "0,1") or
          NULL != strstr(main_uart_rx_buf, "0,3")) {
        net_attached_flag = 1;
      }
    }
    break;
  case SARAR410M02B:
    if (NULL != strstr(main_uart_rx_buf, "CEREG:")) {
      if (NULL != strstr(main_uart_rx_buf, "3,1")) {
        net_attached_flag = 1;
      }
    }
    break;

  default:
    break;
  }
  if (net_attached_flag == 1) {
    usb_cdc_send_string("net attached ok\n");
  } else {
    usb_cdc_send_string("net attached not ok\n");
  }
}

void parse_close_socket(void) {
  // usb_cdc_send_string(main_uart_rx_buf);
  // HAL_Delay(1000);
  // CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
  // HAL_Delay(1000);
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "OK") != NULL ||
        strstr(main_uart_rx_buf, "ERROR") != NULL) {
      close_socket_flag = 1;
    } else {
      print_erro("Erro Occured when parse at_result for close_socket()\n");
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      close_socket_flag = 1;
    } else {
      print_erro("Erro Occured when parse at_result for close_socket()\n");
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "socket_id") != NULL ||
        strstr(main_uart_rx_buf, "OK") != NULL) {
      close_socket_flag = 1;
    } else {
      print_erro("Erro Occured when parse at_result for close_socket()\n");
    }
    break;
  default:
    break;
  }

  if (close_socket_flag) {
    usb_cdc_send_string("close socket ok\n");
  } else {
    usb_cdc_send_string("close socket not ok\n");
  }
}

void parse_create_socket(void) {
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "1") != NULL ||
        strstr(main_uart_rx_buf, "0") != NULL ||
        strstr(main_uart_rx_buf, "2") != NULL ||
        strstr(main_uart_rx_buf, "3") != NULL) {
      create_socket_flag = 1;
      socket_num[0] = main_uart_rx_buf[2];
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_create_socket()\n");
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      create_socket_flag = 1;
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_create_socket()\n");
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "+ESOC") != NULL) {
      socket_num[0] = *(strstr(main_uart_rx_buf, "+ESOC") + 6);
      create_socket_flag = 1;
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_create_socket()\n");
    }
    break;
  default:
    break;
  }

  if (create_socket_flag) {
    usb_cdc_send_string("creat socket ok\n");
  } else {
    usb_cdc_send_string("creat socket not ok\n");
  }
}

void parse_bind_sock(void) {
  switch (e_module_type) {
  case BC28:
    break;
  case BC26:
  case BC66:
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      create_socket_flag = 1;
    } else {
      print_erro("Erro Occured when parse at_result for parse_bind_sock()\n");
    }
    break;
  default:
    break;
  }

  if (create_socket_flag) {
    usb_cdc_send_string("bind socket ok\n");
  } else {
    usb_cdc_send_string("bind socket not ok\n");
  }
}

void parse_send_pack_result(void) {
  // usb_cdc_send_string(main_uart_rx_buf);
  // HAL_Delay(1000);
  // CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
  // HAL_Delay(1000);
  // TODO: merge the code below (they are the same)
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ul_success_flag = 1;
    } else if (strstr(main_uart_rx_buf, "ERROR") != NULL) {
      ul_success_flag = 0;
    } else {
      print_erro("Erro Occured when parse parse_send_pack_result()\n");
    }
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ul_success_flag = 1;
    } else if (strstr(main_uart_rx_buf, "ERROR") != NULL) {
      ul_success_flag = 0;
    } else {
      print_erro("Erro Occured when parse parse_send_pack_result()\n");
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      ul_success_flag = 1;
    } else if (strstr(main_uart_rx_buf, "ERROR") != NULL) {
      ul_success_flag = 0;
    } else {
      print_erro("Erro Occured when parse parse_send_pack_result()\n");
    }
    break;
  case BG96:
  case SARAR410M02B:
    ul_success_flag = at_has_ok_in_return();
    break;
  default:
    break;
  }
}

void parse_set_apn(void) {
  // CDC_Transmit_FS(main_uart_rx_buf, main_rx_byte_cnt);
  HAL_Delay(200);
  switch (e_module_type) {
  case BC28:
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      set_apn_flag = 1;
    } else {
      print_erro("Erro Occured when parse at_result for parse_set_apn()\n");
      return;
    }
    break;
  default:
    break;
  }
  if (set_apn_flag) {
    usb_cdc_send_string("set apn ok\n");
  } else {
    usb_cdc_send_string("set apn not ok\n");
  }
}

void parse_stop_nnmi(void) {
  switch (e_module_type) {
  case BC28:
    break;
  case BC26:
  case BC66:
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "OK") != NULL) {
      print_erro("stop auto nnmi ok\n");
    } else {
      print_erro("stop auto nnmi not ok\n");
    }
    break;
  default:
    break;
  }
}

void parse_down_pack_cdp(void) {
  //"646F776E666C6167"="downflag" as an indicator for parsing down_pack
  parse_down_pack_ok_flag = 0;
  char tmp[128] = {""};
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "646F776E666C6167") != NULL) {
      int j = 0;
      char *F_band = strstr(main_uart_rx_buf, "646F776E666C6167");
      if (F_band >= 0) {
        parse_down_pack_ok_flag = 1;
        j = 0;
        F_band = F_band + 16;
        while (('0' <= *(F_band) && *(F_band) <= 'z') || *(F_band) == '-') {
          tmp[j++] = *(F_band++);
        }
      }
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_down_pack_cdp()\n");
      return;
    }
    hexstr_2_str(tmp, down_pack); //"3130" stransfer to "10"
    break;
  default:
    break;
  }
}

void parse_down_pack_udp(void) {
  // usb_cdc_send_string(main_uart_rx_buf);
  // HAL_Delay(1000);
  // CDC_Transmit_FS(main_uart_rx_buf, strlen(main_uart_rx_buf));
  // HAL_Delay(1000);

  //"646F776E666C6167"="downflag" as an indicator for parsing down_pack
  parse_down_pack_ok_flag = 0;
  char tmp[128] = {""};
  int j = 0;
  switch (e_module_type) {
  case BC28:
    if (strstr(main_uart_rx_buf, "646F776E666C6167") != NULL) {
      char *F_band =
          strstr(main_uart_rx_buf, "646F776E666C6167"); // down msg flag
      if (F_band >= 0) {
        parse_down_pack_ok_flag = 1;
        j = 0;
        F_band = F_band + 16;
        while (('0' <= *(F_band) && *(F_band) < 'z') || *(F_band) == '-') {
          tmp[j++] = *(F_band++);
        }
      }
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_down_pack_udp()\n");
      return;
    }
    hexstr_2_str(tmp, down_pack);
    break;
  case BC26:
  case BC66:
    if (strstr(main_uart_rx_buf, "downflag") != NULL) {
      char *F_band = strstr(main_uart_rx_buf, "downflag"); // down msg flag
      if (F_band >= 0) {
        parse_down_pack_ok_flag = 1;
        j = 0;
        F_band = F_band + 8;
        while (('0' <= *(F_band) && *(F_band) <= '9') || *(F_band) == '|') {
          tmp[j++] = *(F_band++);
        }
      }
      strcpy(down_pack, tmp);
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_down_pack_udp()\n");
      return;
    }
    break;
  case ME3616:
    if (strstr(main_uart_rx_buf, "646f776e666c6167") != NULL) {
      char *F_band =
          strstr(main_uart_rx_buf, "646f776e666c6167"); // down msg flag
      if (F_band >= 0) {
        parse_down_pack_ok_flag = 1;
        j = 0;
        F_band = F_band + 16;
        while ('0' <= *(F_band) && *(F_band) <= 'z' ||
               *(F_band) == '-' && *(F_band) != ',') {
          tmp[j++] = *(F_band++);
        }
      }
    } else {
      print_erro(
          "Erro Occured when parse at_result for parse_down_pack_udp()\n");
      return;
    }
    hexstr_2_str(tmp, down_pack);
    break;
  case BG96:
  case SARAR410M02B:
    if (NULL != strstr(main_uart_rx_buf, "downflag")) {
      parse_down_pack_ok_flag = 1;
      char *start_ptr = strstr(main_uart_rx_buf, "downflag");
      start_ptr += 8;
      char *end_ptr = strstr(start_ptr, "\r\n");
      if (SARAR410M02B == e_module_type) {
        end_ptr -= 1;
      } // exclude the end double quote.
      strncpy(down_pack, start_ptr, end_ptr - start_ptr);
    }
    break;
  default:
    break;
  }
}

void parse_at_result(int at_command_type) {
  switch (at_command_type) {
  case GET_FIRMWARE:
    parse_get_firmware();
    break;
  case GET_RADIO_INFO:
    parse_radio_info();
    break;
  case GET_DOWN_CDP:
    parse_down_pack_cdp();
    break;
  /* case GET_DOWN_UDP: */
  /*   parse_down_pack_udp(); */
  /*   break; */
  case PING:
    parse_at_ping();
    break;
  case CREATE_SOCKET:
    parse_create_socket();
    break;
  case CLOSE_SOCKET:
    parse_close_socket();
    break;
  case SEND_PACK:
    parse_send_pack_result();
    break;
  case GET_CSQ:
    parse_get_csq();
    break;
  case CLOSE_ECHO:
    parse_close_echo();
    break;
  case SET_APN:
    parse_set_apn();
    break;
  case BIND_SOCKET:
    parse_bind_sock();
    break;
  case STOP_NNMI:
    parse_stop_nnmi();
    break;
  /* case NET_ATTACH: */
  /*   parse_attach_status(); */
  /*   break; */
  case RSRP_28_35_95:
    parse_rsrp();
    break;
  default:
    break;
  }
}

void at_close_echo(void) {
  stop_echo_flag = 0;
  char CMD[30] = {""};
  switch (e_module_type) {
  case BC28:
    stop_echo_flag = 1; // No need to close echo
    break;
  case BC35:
    stop_echo_flag = 1;
    break;
  case BC95:
    stop_echo_flag = 1;
    break;
    // TODO: merge the code below
  case BC26:
  case BC66:
  case BG96:
  case SARAR410M02B:
    strcpy(CMD, "ATE0\r\n");
    mod_send_cmd(CMD);
    parse_at_result(CLOSE_ECHO);
    break;
  case ME3616:
    strcpy(CMD, "ATE0\r\n");
    mod_send_cmd(CMD);
    parse_at_result(CLOSE_ECHO);
    break;
  default:
    break;
  }
  if (stop_echo_flag) {
    usb_cdc_send_string("close auto echo ok\n");
  } else {
    usb_cdc_send_string("close auto echo not ok\n");
  }
}

void at_get_csq(void) {
  strcpy(csq, "");
  char CMD[30] = {""};
  switch (e_module_type) {
  case BC28:
  case BC35:
  case BC95:
  case BC26:
  case BC66:
  case ME3616:
  case BG96:
  case SARAR410M02B:
    strcpy(CMD, "AT+CSQ\r\n");
    break;
  default:
    break;
  }
  mod_send_cmd(CMD);
  parse_at_result(GET_CSQ);
}

void at_close_nnmi(void) {
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+NNMI=0\r\n");
    mod_send_cmd(CMD);
    parse_at_result(STOP_NNMI);
    break;
  case BC26:
  case BC66:
    break;
  case ME3616:
    strcpy(CMD, "AT+ESOREADEN=1\r\n");
    mod_send_cmd(CMD);
    parse_at_result(STOP_NNMI);
    break;
  default:
    break;
  }
}

void at_ping(void) {
  ping_success_flag = 0;
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+NPING=129.211.125.101\r\n");
    break;
  case BC26:
    strcpy(CMD, "AT+QPING=1,\"129.211.125.101\"\r\n");
    break;
  case ME3616:
    strcpy(CMD, "AT+PING=129.211.125.101\r\n");
    break;
  case BC66:
    strcpy(CMD, "AT+QPING=1,\"96.126.124.91\"\r\n");
    break;
  case BG96:
    // TODO: test this
    strcpy(CMD, "AT+QPING=1,\"96.126.124.91\"\r\n");
    break;
  default:
    break;
  }
  mod_send_cmd(CMD);
  parse_at_result(PING);
}

void at_get_firmware_version() {
  memset(firmware, 0, sizeof(firmware));
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+CGMR\r\n");
    break;
  case BC26:
  case BC66:
    /*Xianghui*/
    strcpy(CMD, "AT+CGMR\r\n");
    // fixed-TODO: not implemented.
    break;
  case ME3616:
    strcpy(CMD, "AT+GAPPVERSION?\r\n");
    break;
  default:
    break;
  }
  mod_send_cmd(CMD);
  parse_at_result(GET_FIRMWARE);
}

void at_get_network_status(void) {
  /*Get CSQ*/
  at_get_csq();

  /* Empty the buf. */
  strcpy(radio_info_st.rsrp, "");
  strcpy(radio_info_st.rsrq, "");
  strcpy(radio_info_st.snr, "");
  strcpy(radio_info_st.ecl, "");
  strcpy(radio_info_st.pci, "");
  strcpy(radio_info_st.earfcn, "");
  strcpy(radio_info_st.cell_id, "");
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC95:
  case BC35:
  case BC28:
    strcpy(CMD, "AT+NUESTATS=RADIO\r\n");
    mod_send_cmd(CMD);
    parse_at_result(GET_RADIO_INFO);
    strcpy(CMD, "AT+NUESTATS=CELL\r\n");
    mod_send_cmd(CMD);
    parse_at_result(RSRP_28_35_95);
    break;
  case BC26:
    strcpy(CMD, "AT+QENG=0\r\n");
    mod_send_cmd(CMD);
    parse_at_result(GET_RADIO_INFO);
    break;
  case BC66:
    mod_send_cmd("AT+QENG=0\r\n");
    parse_bc66_qeng();
    break;
  case ME3616:
    strcpy(CMD, "AT*MENGINFO=0\r\n");
    mod_send_cmd(CMD);
    parse_at_result(GET_RADIO_INFO);
    break;
  case BG96:
    mod_send_cmd("AT+QCFG=\"celevel\"\r\n");
    parse_bg96_ecl();

    mod_send_cmd("AT+QENG=\"servingcell\"\r\n");
    parse_bg96_qeng();
    break;
  case SARAR410M02B:
    sara_get_radio_info();
    break;
  default:
    break;
  }
}

void at_query_net_attach(void) {
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC28:
  case BC26:
  case BC66:
  case ME3616:
  case BG96:
  case SARAR410M02B:
    strcpy(CMD, "AT+CEREG?\r\n");
    break;
  default:
    break;
  }
  // TODO: check CMD is not empty before sending.
  mod_send_cmd(CMD);
  parse_attach_status();
  /* parse_at_result(NET_ATTACH); */
}

void at_set_apn(void) {
  set_apn_flag = 0;
  switch (e_module_type) {
  case BC28:
    set_apn_flag = 1;
    break;
  case BC26:
    mod_send_cmd("AT+QCGDEFCONT=\"IP\",\"spe.inetd.vodafone.nbiot\"\r\n");
    parse_at_result(SET_APN);
    break;
  case BC66:
    mod_send_cmd("AT+QCGDEFCONT=\"IP\",\"mw01.vzwstatic\"\r\n");
    break;
  default:
    break;
  }
}

void at_get_down_pack_cdp(void) {
  parse_down_pack_ok_flag = 0;
  strcpy(down_pack, "");
  char CMD[20] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+NMGR\r\n");
    break;
  case BC26:
  case BC66:
    break;
  default:
    break;
  }
  mod_send_cmd(CMD);
  parse_at_result(GET_DOWN_CDP);
  if (parse_down_pack_ok_flag) {
    usb_cdc_send_string("parse cdp down pack ok\n");
  } else {
    usb_cdc_send_string("parse cdp down pack not ok\n");
  }
}

void at_get_down_pack_udp(void) {

  if (SARAR410M02B == e_module_type) {
    return;
  }

  parse_down_pack_ok_flag = 0;
  strcpy(down_pack, "");
  char CMD[20] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+NSORF=1,1000\r\n");
    break;
  case BC26:
  case BC66:
    strcpy(CMD, "AT+QIRD=0,512\r\n");
    break;
  case ME3616:
    strcpy(CMD, "AT+ESOREAD=");
    strcat(CMD, socket_num);
    strcat(CMD, ",512\r\n");
    break;
  case BG96:
    strcpy(CMD, "AT+QIRD=2\r\n");
    break;
  default:
    break;
  }

  mod_send_cmd(CMD);
  /* parse_at_result(GET_DOWN_UDP); */
  parse_down_pack_udp();
  if (parse_down_pack_ok_flag) {
    usb_cdc_send_string("[INFO] Parse udp down pack OK\n");
  } else {
    usb_cdc_send_string("[ERR] Parse udp down pack not OK\n");
  }
}

void update_peripheral_var(void) {
  // update temperature/humidity/v_bat
  float rh = si7021_get_rh();
  float temp = si7021_get_temperature();

  float v_batt_reg = 0;
  float v_batt = 0;

  char temp_string[ITOA_BUF_LEN] = "";
  char rh_string[ITOA_BUF_LEN] = "";
  char v_batt_string[ITOA_BUF_LEN] = "";

  dy_ftoa(temp, temp_string);
  dy_ftoa(rh, rh_string);

  dy_shift_leading_null_chars(temp_string);
  dy_shift_leading_null_chars(rh_string);

  HAL_ADC_Start(&V_BATT_ADC);
  HAL_ADC_PollForConversion(&V_BATT_ADC, HAL_MAX_DELAY);
  HAL_Delay(15);
  v_batt_reg = HAL_ADC_GetValue(&V_BATT_ADC);
  HAL_ADC_Stop(&V_BATT_ADC);

  v_batt = v_batt_reg * V_BATT_CONSTANT *
           g_bcm_st.v_batt_calibration_value.value / 1000;
  dy_ftoa(v_batt, v_batt_string);
  dy_shift_leading_null_chars(v_batt_string);

  // TODO: This part is not debugged.
  strcpy(ul_packet_st.humidity, rh_string);
  strcpy(ul_packet_st.temperature, temp_string);
  strcpy(ul_packet_st.v_bat, v_batt_string);
}

void update_radio_info_var(void) {
  at_get_network_status(); // update radio_info variables
  memcpy(&ul_packet_st.radio_info, &radio_info_st, sizeof(radio_info_st));
}

void at_close_socket(void) {
  close_socket_flag = 0;
  char CMD[50] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(CMD, "AT+NSOCL=1\r\n");
    mod_send_cmd(CMD);
    parse_at_result(CLOSE_SOCKET);
    break;
  case BC26:
    strcpy(CMD, "AT+QICLOSE=0\r\n"); // close No.0 socket
    mod_send_cmd(CMD);
    parse_at_result(CLOSE_SOCKET);
    break;
  case ME3616:
    strcpy(CMD, "AT+ESOCL="); // close No.0 socket
    strcat(CMD, socket_num);
    strcat(CMD, "\r\n");
    mod_send_cmd(CMD);
    parse_at_result(CLOSE_SOCKET);
    break;
  case BC66:
  case BG96:
    close_socket_flag = 1; // no need to close at all.
    break;
  case SARAR410M02B:
    mod_send_cmd("AT+USOCL=0\r\n");
    close_socket_flag =
        1; // Don't care the result. If it is open, then it is closed.
    break;
  default:
    break;
  }
}

void at_create_socket(void) {
  create_socket_flag = 0;
  // Close socket
  at_close_socket();
  char CMD[70] = {""};

  if (close_socket_flag) {
    switch (e_module_type) {
    case BC28:
      strcpy(CMD, "AT+NSOCR=DGRAM,17,9123,1\r\n");
      mod_send_cmd(CMD);
      parse_at_result(CREATE_SOCKET);
      break;
    case BC26:
      // create No.0 socket
      strcpy(CMD,
             "AT+QIOPEN=1,0,\"UDP\",\"129.211.125.101\",9678,9123,0,0\r\n");
      mod_send_cmd(CMD);
      parse_at_result(CREATE_SOCKET);
      break;
    case BC66:
      // create No.0 socket
      strcpy(CMD, "AT+QIOPEN=1,0,\"UDP\",\"96.126.124.91\",9678,9123,0,0\r\n");
      mod_send_cmd(CMD);
      parse_at_result(CREATE_SOCKET);
      break;
    case ME3616:
      strcpy(CMD, "AT+ESOC=1,2,1\r\n");
      mod_send_cmd(CMD);
      parse_at_result(CREATE_SOCKET);
      if (create_socket_flag) {
        create_socket_flag = 0;
        strcpy(CMD, "AT+ESOCON=");
        strcat(CMD, socket_num);
        strcat(CMD, ",9678,\"129.211.125.101\"\r\n");
        mod_send_cmd(CMD);
        parse_at_result(BIND_SOCKET);
      }
      break;
    case BG96:
      at_qualcomm_create_pdp_context();
      break;
    case SARAR410M02B:
      mod_send_cmd("AT+CGDCONT?\r\n");
      if (NULL != strstr(main_uart_rx_buf, "1,\"IP\"")) {
        // The PDP context is ready
        mod_send_cmd("AT+USOCR=17,6666\r\n");
        if (NULL != strstr(main_uart_rx_buf, "SOCR: 0")) {
          create_socket_flag = 1;
        }
      } else {
        usb_cdc_send_string("[ERR] SARAR410M02B PDP context not ready\n");
      }
      break;
    default:
      break;
    }
  } else {
    print_erro("Have not closed socket\n");
    return;
  }
}

void pack_item_2_str(char *tmp) {
  strcat(tmp, ul_packet_st.node_id);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.packet_index);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.module_type);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.network_operator);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.app_type);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.sleep_timer);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.csq);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.earfcn);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.pci);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.cell_id);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.ecl);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.rsrq);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.rsrp);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.radio_info.snr);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.temperature);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.humidity);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.v_bat);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.ubhv);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.umhv);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.msv);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.err_code);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.test_id);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.ul_total_packet);
  strcat(tmp, "|");
  strcat(tmp, ul_packet_st.ul_packet_size);

  int len_sup = strlen(tmp);
  int len_all = String2Int(ul_packet_st.ul_packet_size);
  if (len_all > len_sup && len_all < 512) {
    strcat(tmp, "|");
    for (int i = len_sup; i < len_all; i++) {
      strcat(tmp, "d");
    }
  }
}

void make_at_pack_cdp(char *at_pack) {
  char tmp[512] = {""};
  char at_head[512] = {""};
  char msg_lenght[5] = {""};
  char at_length[5] = {""};
  switch (e_module_type) {
  case BC28:
    strcpy(at_head, "AT+NMGS=");
    pack_item_2_str(tmp);
    string_2_hexstr(tmp, at_pack);
    sprintf(msg_lenght, "%04x", strlen(at_pack) / 2);
    sprintf(at_length, "%d", (strlen(at_pack) + 6) / 2);
    strcat(at_head, at_length);
    strcat(at_head, ",");
    strcat(at_head, "41");
    strcat(at_head, msg_lenght);
    strcat(at_head, at_pack);
    strcpy(at_pack, at_head);
    strcat(at_pack, "\r\n");
    break;
  default:
    break;
  }
}

void make_at_pack_udp_bc28(char *at_pack, char *sock_num) {
  char at_head[600] = {""};
  char tmp_pack[600] = {""};
  char msg_lenght[10] = {""};

  strcpy(at_head, "AT+NSOST=");
  strcat(at_head, sock_num);
  strcat(at_head, ",");
  strcat(at_head, server_ip);
  strcat(at_head, ",");
  strcat(at_head, server_udp_port);
  strcat(at_head, ",");
  pack_item_2_str(tmp_pack);
  string_2_hexstr(tmp_pack, at_pack);
  sprintf(msg_lenght, "%d", strlen(tmp_pack));
  strcat(at_head, msg_lenght);
  strcat(at_head, ",");
  strcat(at_head, at_pack);
  strcpy(at_pack, at_head);
  strcat(at_pack, "\r\n");
}

void make_at_pack_udp_bc26(char *at_pack) {
  char at_head[512] = {""};
  char tmp_pack[512] = {""};
  char msg_lenght[4] = {""};

  // AT+QISEND=<connectID>,<send_length>,<data>
  strcpy(at_head, "AT+QISEND=0,"); // defualt socket num is "0" for bc26
  pack_item_2_str(tmp_pack);
  sprintf(msg_lenght, "%d", strlen(tmp_pack));
  strcat(at_head, msg_lenght);
  strcat(at_head, ",");
  strcat(at_head, tmp_pack);
  strcpy(at_pack, at_head);
  strcat(at_pack, "\r\n");
}

void make_at_pack_udp_me3616(char *at_pack, char *sock_num) {
  char at_head[600] = {""};
  char tmp_pack[600] = {""};
  char msg_lenght[10] = {""};

  strcpy(at_head, "AT+ESOSEND=");
  strcat(at_head, sock_num);
  strcat(at_head, ",");
  pack_item_2_str(tmp_pack);
  string_2_hexstr(tmp_pack, at_pack);
  sprintf(msg_lenght, "%d", strlen(tmp_pack));
  strcat(at_head, msg_lenght);
  strcat(at_head, ",");
  strcat(at_head, at_pack);
  strcpy(at_pack, at_head);
  strcat(at_pack, "\r\n");
  // usb_cdc_send_string(at_pack);
}

void make_at_pack_udp(char *at_pack, char *sock_num) {
  switch (e_module_type) {
  case BC28:
    make_at_pack_udp_bc28(at_pack, sock_num);
    break;
  case BC26:
  case BC66:
    make_at_pack_udp_bc26(at_pack);
    break;
  case ME3616:
    make_at_pack_udp_me3616(at_pack, sock_num);
    break;
  default:
    break;
  }
}

void fill_up_pack_cdp(char *at_pack) {
  update_peripheral_var();
  update_radio_info_var();
  make_at_pack_cdp(at_pack);
}

void fill_up_pack_udp(char *at_pack, char *sock_num) {
  /* update_peripheral_var(); */ // moved to get_init_pack()
  /* update_radio_info_var(); */
  /* make_at_pack_udp(at_pack, sock_num); */
}

void get_down_init_info(char *down_pack) {
  // down msg like this "downflag001|00010|001|100|26"
  int j = 0;
  char sleep_timer[10] = {""};
  char app_type[10] = {""};
  char total_ul[10] = {""};
  char ul_size[10] = {""};
  char test_id[10] = {""};
  if (strstr(down_pack, "|") != NULL) {
    char *F_bar = strstr(down_pack, "|");
    for (j = 0; j < 3; j++) {
      app_type[j] = *(F_bar + j - 3);
    }
    F_bar++;
    j = 0;
    while (*(F_bar) != '|') {
      sleep_timer[j++] = *(F_bar++);
    }
    F_bar++;
    j = 0;
    while (*(F_bar) != '|') {
      test_id[j++] = *(F_bar++);
    }
    F_bar++;
    j = 0;
    while (*(F_bar) != '|') {
      total_ul[j++] = *(F_bar++);
    }
    F_bar++;
    j = 0;
    while (*(F_bar) != '\0') {
      ul_size[j++] = *(F_bar++);
    }
  } else {
    usb_cdc_send_string("error occured when get_down_init_info\n");
    /*get into standby mode*/
    config_rtc_standby_auto_wakeup_after(1);
    HAL_PWR_EnterSTANDBYMode();
  }

  g_eeprom_tm_st.ul_pkt_count.value = 0;
  g_eeprom_tm_st.is_task_assigned.value = 1;
  g_eeprom_tm_st.mcu_sleep_timer.value = atoi(sleep_timer);
  g_eeprom_tm_st.application_type.value = atoi(app_type);
  g_eeprom_tm_st.test_id.value = atoi(test_id);
  g_eeprom_tm_st.ul_total_pkt.value = atoi(total_ul);
  g_eeprom_tm_st.ul_pkt_size.value = atoi(ul_size);
}

void init_ue_before_packing(void) {
  /*close auto echo & check the network attach status*/
  uint16_t delay_time = 0;
  uint8_t close_echo_failed_attempt = 0;
  while (!stop_echo_flag and (close_echo_failed_attempt <= 5)) {
    at_close_echo();
    HAL_Delay(700);
    close_echo_failed_attempt += 1;
  }

  // Module-specified initialization via AT commands.
  switch (e_module_type) {
  case BG96:
    mod_send_cmd("AT+QCFG=\"band\",0,1,1008,1\r\n");    // search B13 (verizon)
    mod_send_cmd("AT+QCFG=\"nwscanseq\",030201,1\r\n"); // NB-IoT has higher
                                                        // scan priority
    mod_send_cmd(
        "AT+QCFG=\" nwscanmode\",3,1\r\n"); // LTE has higher scan priority
    mod_send_cmd("AT+QCFG=\"iotopmode\",1,1\r\n");    // NB mode
    mod_send_cmd("AT+QCFG=\"nb1/bandprior\",0D\r\n"); // Search B13 first.
    break;
  case SARAR410M02B:
    mod_send_cmd("AT+CEREG=3\r\n"); // detailed network registration status
    mod_send_cmd("AT+UCGED=5\r\n"); // search band mask
    break;
  case BC66:
    mod_send_cmd("AT+QBAND=3,2,12,13\r\n"); // lock the three bands to search
    break;
  default:
    break;
  }

  uint8_t net_attached_num = 0;
  net_attached_flag = 0;

  while (!net_attached_flag &&
         (net_attached_num <= MAX_NETWORK_ATTACH_QUERY_COUNT)) {
    net_attached_num++;
    at_query_net_attach(); // net_attached_flag will be set in here.
    HAL_Delay(200);
    LED0_TOGGLE;
  }

  // Attach failure handler
  if (net_attached_num > MAX_NETWORK_ATTACH_QUERY_COUNT) {
    g_tm_st.test_id = atoi(ul_packet_st.test_id); // Remain unchanged.
    g_tm_st.error_code_this_run =
        (uint8_t)TASK_ERR_PACKET_NOT_TRANSMITTED_FAIL_TO_ATTACH;

    usb_cdc_send_string("FT: Attach network failed \n");
    usb_cdc_send_string("FT: write config to EEPROM\n");
    update_eeprom_task_monitor();
    eeprom_write_task_monitor_struct(&g_eeprom_tm_st);

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
    /*get into standby mode*/
    config_rtc_standby_auto_wakeup_after(1);
    HAL_PWR_EnterSTANDBYMode();
  }
  LED0_ON;
  LED1_OFF;
}

void get_init_pack(void) {
  // Init UE to get network attached.
  init_ue_before_packing();
  ul_success_flag = 0;
  char CMD[600] = {""};
  char bg96_qisend_cmd[50] = "";
  char bg96_payload_len_str[5] = "";

  // Important!
  strcpy(ul_packet_st.packet_index, "000"); // must set pack_index as "000"

  // Generate the packet
  switch (e_tran_type) {
  case PROTO_UDP:
    // Create socket
    at_create_socket();

    if (create_socket_flag) {
      update_peripheral_var();
      update_radio_info_var();
      switch (e_module_type) {
      case BG96:
        bg96_generate_ul_packet_payload(CMD, bg96_payload_len_str);
        break;
      case SARAR410M02B:
        sara_make_ul_packet(CMD);
        break;
      case BC26:
      case BC66:
      case BC28:
      case ME3616:
        at_close_nnmi(); // close auto get down msg
        make_at_pack_udp(CMD, socket_num);
        break;
      default:
        break;
      }
    } else {
      usb_cdc_send_string("[ERR] Socket not created\n");
    }
    break;
  case PROTO_CDP:
    at_close_nnmi(); // close auto get down msg
    fill_up_pack_cdp(CMD);
    break;
  default:
    break;
  }

  // Send the UL packet
  volatile uint8_t resent_init_packet_count = 0;
  volatile uint8_t dl_query_attempt = 0;
  const uint8_t MAX_RESNT_ATTEMPT = 5;
  while (resent_init_packet_count < MAX_RESNT_ATTEMPT and
         !parse_down_pack_ok_flag) {

    char resent_atmpt[2] = "1";
    resent_atmpt[0] = resent_init_packet_count + 1 + '0';
    export_one_field("[INFO] Fetch init pack attempt ", resent_atmpt);

    if (BG96 == e_module_type) {
      strcpy(bg96_qisend_cmd, "AT+QISEND=2,");
      strcat(bg96_qisend_cmd, bg96_payload_len_str);
      strcat(bg96_qisend_cmd, ",\"96.126.124.91\",9678\r\n");
      mod_send_cmd(bg96_qisend_cmd);
      usb_cdc_send_string(bg96_qisend_cmd);
      if (NULL != strstr(main_uart_rx_buf, ">")) {
        // Ready to send.
        mod_send_cmd(CMD); // send ul pack
        usb_cdc_send_string("[INFO] Init packet: ");
        /* CDC_Transmit_FS(CMD, 128); // TODO: delete this later. */
        HAL_UART_Receive_DMA(&MAIN_UART, (uint8_t *)main_uart_rx_buf,
                             MAIN_UART_BUF_SIZE); // Start UART receiver
        // used to get the downlink packet notice.
      } else {
        usb_cdc_send_string("[ERR] BG96 is not ready for packet tx");
      }
    } else {
      // Other modules
      mod_send_cmd(CMD);
    }
    parse_at_result(SEND_PACK); // parse result
    print_at_return_msg();

    if (ul_success_flag == 1) {
      usb_cdc_send_string("[INFO] Send init packet OK\n");
    } else {
      usb_cdc_send_string("[ERR] Send init packet not OK\n");
      return;
    }

    // Wait for down init pack
    char wait_cnt[2] = "";
    switch (e_module_type) {
    case BG96:
      dl_query_attempt = 0;
      while (dl_query_attempt < 5) {
        if (is_bg96_dl_packet_delivered()) {
          break;
        }
        dl_query_attempt += 1;
        wait_cnt[0] = dl_query_attempt + '0';
        export_one_field("BG96 Wait for DL msg ", wait_cnt);
        HAL_Delay(1000);
      }
      break;
    case SARAR410M02B:
      dl_query_attempt = 0;
      while (dl_query_attempt < 5) {
        mod_send_cmd("AT+USORF=0,512\r\n");
        print_at_return_msg();
        if (NULL != strstr(main_uart_rx_buf, "9678")) { // has valid init pack
          break;
        }
        dl_query_attempt += 1;
        wait_cnt[0] = dl_query_attempt + '0';
        export_one_field("SARA Wait for DL msg ", wait_cnt);
        HAL_Delay(1000);
      }
      if (dl_query_attempt < 5) {
        parse_down_pack_udp();
      }
      break;
    case BC66:
      HAL_Delay(5000);
      break;
    default:
      HAL_Delay(5000);
      break;
    }

    switch (e_tran_type) { // wait for down pack and parse it
    case PROTO_UDP:
      at_get_down_pack_udp(); // will set parse_down_pack_ok_flag inside.
      break;
    case PROTO_CDP:
      at_get_down_pack_cdp();
      break;
    default:
      break;
    }

    if (SARAR410M02B == e_module_type and dl_query_attempt < 5) {
      parse_down_pack_ok_flag = 1;
    }
    resent_init_packet_count += 1;
  }

  if (parse_down_pack_ok_flag) // get down msg from ue
  {
    get_down_init_info(down_pack);
    // parse down init_info from pack, goto STANDBY in the end.
  } else {
    usb_cdc_send_string(
        "[ERR] at_get_down_pack() failed, get into standby mode to retry\n");
    config_rtc_standby_auto_wakeup_after(1);
    HAL_PWR_EnterSTANDBYMode();
  }
}

void send_test_pack(void) {
  init_ue_before_packing();

  ul_success_flag = 0;
  char CMD[600] = {""};
  char bg96_qisend_cmd[50] = "";
  char bg96_payload_len_str[5] = "";

  // Generate the packet
  switch (e_tran_type) {
  case PROTO_UDP:
    at_create_socket();
    if (create_socket_flag) {

      update_peripheral_var();
      update_radio_info_var();

      // Embedded switch
      switch (e_module_type) {
      case BG96:
        bg96_generate_ul_packet_payload(CMD, bg96_payload_len_str);
        break;
      case SARAR410M02B:
        sara_make_ul_packet(CMD);
        break;
      default:
        at_close_nnmi(); // close auto get down msg
        make_at_pack_udp(CMD, socket_num);
        break;
      }
    } else {
      usb_cdc_send_string("Have not created socket\n");
    }
    break;
  case PROTO_CDP:
    at_close_nnmi(); // close auto get down msg
    fill_up_pack_cdp(CMD);
    break;
  default:
    break;
  }

  // Send AT command
  if (BG96 == e_module_type) {
    strcpy(bg96_qisend_cmd, "AT+QISEND=2,");
    strcat(bg96_qisend_cmd, bg96_payload_len_str);
    strcat(bg96_qisend_cmd, ",\"96.126.124.91\",9678\r\n");
    mod_send_cmd(bg96_qisend_cmd);
    usb_cdc_send_string(bg96_qisend_cmd);
    if (NULL != strstr(main_uart_rx_buf, ">")) { // Ready to send.
      usb_cdc_send_string("[INFO] Field test packet: ");
      CDC_Transmit_FS(CMD, 16);      // TODO: delete this later.
      mod_send_field_test_pack(CMD); // send ul pack
      // used to get the downlink packet notice.
    } else {
      usb_cdc_send_string("[ERR] BG96 is not ready for packet tx");
    }
  } else {
    mod_send_field_test_pack(CMD);
  }

  g_tm_st.test_id = atoi(ul_packet_st.test_id); // XXX DY: what's the purpose?
  // GOTO debug log collecting or current sensing.
}

void wrap_up_test_packet(char *CMD) {

  init_ue_before_packing();

  ul_success_flag = 0;
  strcpy(CMD, ""); // clear the cmd
  char bg96_payload_len_str[5] = "";

  // Generate the packet
  switch (e_tran_type) {
  case PROTO_UDP:
    at_create_socket();
    if (create_socket_flag) {

      update_peripheral_var();
      update_radio_info_var();

      // Embedded switch
      switch (e_module_type) {
      case BG96:
        bg96_generate_ul_packet_payload(CMD, bg96_payload_len_str);
        // Note: in this function, bg96_payload_len_str is not returned.
        break;
      case SARAR410M02B:
        sara_make_ul_packet(CMD);
        break;
      default:
        at_close_nnmi(); // close auto get down msg
        make_at_pack_udp(CMD, socket_num);
        break;
      }
    } else {
      usb_cdc_send_string("Have not created socket\n");
    }
    break;
  case PROTO_CDP:
    at_close_nnmi(); // close auto get down msg
    fill_up_pack_cdp(CMD);
    break;
  default:
    break;
  }
}

void send_test_packet_in_pipeline(char* CMD){

  // Enter from the sensing pipeline
  // Send AT command
  if (BG96 == e_module_type) {

    char bg96_payload_len_str[ITOA_BUF_LEN] = {""};

    dy_itoa(strlen(CMD), bg96_payload_len_str);
    dy_shift_leading_null_chars(bg96_payload_len_str);

    char bg96_qisend_cmd[50] = "";
    strcpy(bg96_qisend_cmd, "AT+QISEND=2,");
    strcat(bg96_qisend_cmd, bg96_payload_len_str);
    strcat(bg96_qisend_cmd, ",\"96.126.124.91\",9678\r\n");
    mod_send_cmd(bg96_qisend_cmd);
    usb_cdc_send_string(bg96_qisend_cmd);
    if (NULL != strstr(main_uart_rx_buf, ">")) { // Ready to send.
      usb_cdc_send_string("[INFO] Field test packet: ");
      /* CDC_Transmit_FS(CMD, 16);      // TODO: delete this later. */
      mod_send_field_test_pack(CMD); // send ul pack
      // used to get the downlink packet notice.
    } else {
      usb_cdc_send_string("[ERR] BG96 is not ready for packet tx");
    }
  } else {
    // Other modules
    mod_send_field_test_pack(CMD);
  }

  g_tm_st.test_id = atoi(ul_packet_st.test_id); // XXX DY: what's the purpose?
  // GOTO debug log collecting or current sensing.
}

/* Added by DY, organize them leter **********************************/
uint8_t is_bg96_dl_packet_delivered() {
  if (NULL != strstr(main_uart_rx_buf, "+QIURC:")) {
    return True;
  } else {
    return False;
  }
}

void post_run_module_control() {
  switch (e_module_type) {
  case SARAR410M02B:
    mod_send_cmd(
        "AT+CFUN=15\r\n"); // it will not enter PSM itself. Manually shutdown.
    break;
  default:
    break;
  }
}
