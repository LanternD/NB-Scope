/**
   @file demo.h
   @author Deliang Yang
   @date_created 2020-01-09
   @last_update N/A
   @version 0.1
   @brief The functions are originally in fm_project_main.c. I moved them here to keep the file well-organized.
   @details The functions here will not be called in fm_project_main but this demo header may need the functions in fm_project_main*/

#ifndef __FM_DEMO_H__
#define __FM_DEMO_H__

#include "fm_project_main.h"

#define MAX_DEMO_HEADER_REPETITION 15 // how many times the header is sent.

/* Demo functions **********************************************************/
/**
   @brief Execute the demos based on the given choice.
   @param demo_choice: 0 to 255. 255 means running all the demos sequentially.
   @return None.
   @note Options:
   0. LED blinking;
   1. SSD1306 display test;
   2. Button controlled LED without EXTI;
   3. Button controlled LED with EXTI;
   4. Temperature and humidity sensor demo;
   5. Sleep and wakeup, RTC control, EEPROM demo;
   6. TF card insertion detection, erase and r/w test;
   7. Battery voltage sensing;
   8. Current sensing;
   9. USB VCP AT command forward.
   10. Debug log to file.
*/
void run_demos(uint8_t demo_choice);

void run_demo0_led_blinking();
void run_demo1_ssd1306_test();
void run_demo2_btn_led_no_exti();
void run_demo3_btn_led_exti();
void run_demo4_temp_humd_sensing();
void run_demo5_eeprom_sleep_wakeup();
void run_demo6_tf_card_rw();
void run_demo7_v_batt_sensing();

/**
   @brief Samples the i_bus to the max of the capability of INA226. Output the
   i_bus and v_bus value every 10000 point.
   @param None.
   @return None.
   @note Currently the speed is around 10000 points per 1.362 seconds,
   equivalent to about 7300 per second.
*/
void run_demo8_i_bus_sensing();
void run_demo9_main_uart_dma();
void run_demo10_read_debug_log();

#endif /* __FM_DEMO_H__ */
