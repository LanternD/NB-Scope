/* USER CODE BEGIN Header */
/**
 ******************************************************************************
 * @file           : main.h
 * @brief          : Header for main.c file.
 *                   This file contains the common defines of the application.
 ******************************************************************************
 * @attention Include this file whenever you need the macros here.
 *
 * <h2><center>&copy; Copyright (c) 2019 STMicroelectronics.
 * All rights reserved.</center></h2>
 *
 * This software component is licensed by ST under Ultimate Liberty license
 * SLA0044, the "License"; You may not use this file except in compliance with
 * the License. You may obtain a copy of the License at:
 *                             www.st.com/SLA0044
 *
 ******************************************************************************
 */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f1xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */
extern ADC_HandleTypeDef hadc1;
extern I2C_HandleTypeDef hi2c1;
extern I2C_HandleTypeDef hi2c2;
extern RTC_HandleTypeDef hrtc;
extern SD_HandleTypeDef hsd;
extern SPI_HandleTypeDef hspi2;
extern UART_HandleTypeDef huart1; // debug log port
extern UART_HandleTypeDef huart2; // main uart port
extern DMA_HandleTypeDef hdma_sdio;
extern DMA_HandleTypeDef hdma_usart2_rx;
extern DMA_HandleTypeDef hdma_usart2_tx;
extern DMA_HandleTypeDef hdma_usart1_rx;
extern DMA_HandleTypeDef hdma_memtomem_dma1_channel1;
/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */
// Configuration
#define IN_DEVELOPMENT 1 // Enable button-driven control, not missing any data.
#define HAS_DISPLAY 0     // SSD1306 is installed
#define FORWARD_MAIN_UART_TO_USB 1
#define HAS_USB_CDC_VCP 1 // enable virtual comm port
#define HAS_SD_CARD_IO 1  // Set 0 to make it compile faster for development.
#define BSP_W_USE_DMA 0     // enable the DMA W in bsp_driver_sd.c
#define BSP_R_USE_DMA 0     // enable the DMA R in bsp_driver_sd.c

/* USER CODE END EM */

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define V_BATT_ADC_Pin GPIO_PIN_0
#define V_BATT_ADC_GPIO_Port GPIOC
#define M_GPIO_L1_Pin GPIO_PIN_1
#define M_GPIO_L1_GPIO_Port GPIOC
#define M_PSM_IND_Pin GPIO_PIN_2
#define M_PSM_IND_GPIO_Port GPIOC
#define M_GPIO_L2_Pin GPIO_PIN_3
#define M_GPIO_L2_GPIO_Port GPIOC
#define M_GPIO_L3_Pin GPIO_PIN_0
#define M_GPIO_L3_GPIO_Port GPIOA
#define M_GPIO_L4_Pin GPIO_PIN_1
#define M_GPIO_L4_GPIO_Port GPIOA
#define M_PWRKEY_Pin GPIO_PIN_4
#define M_PWRKEY_GPIO_Port GPIOA
#define M_RESET_Pin GPIO_PIN_5
#define M_RESET_GPIO_Port GPIOA
#define M_WAKEUP_FROM_PSM_Pin GPIO_PIN_6
#define M_WAKEUP_FROM_PSM_GPIO_Port GPIOA
#define M_AP_READY_Pin GPIO_PIN_7
#define M_AP_READY_GPIO_Port GPIOA
#define LED0_Pin GPIO_PIN_4
#define LED0_GPIO_Port GPIOC
#define LED1_Pin GPIO_PIN_5
#define LED1_GPIO_Port GPIOC
#define BUTTON1_Pin GPIO_PIN_0
#define BUTTON1_GPIO_Port GPIOB
#define BUTTON1_EXTI_IRQn EXTI0_IRQn
#define BUTTON2_Pin GPIO_PIN_1
#define BUTTON2_GPIO_Port GPIOB
#define BUTTON2_EXTI_IRQn EXTI1_IRQn
#define BUS_SCL_Pin GPIO_PIN_10
#define BUS_SCL_GPIO_Port GPIOB
#define BUS_SDA_Pin GPIO_PIN_11
#define BUS_SDA_GPIO_Port GPIOB
#define M_SPI_CS_Pin GPIO_PIN_12
#define M_SPI_CS_GPIO_Port GPIOB
#define M_RI_Pin GPIO_PIN_6
#define M_RI_GPIO_Port GPIOC
#define M_GPIO_R3_Pin GPIO_PIN_7
#define M_GPIO_R3_GPIO_Port GPIOC
#define M_GPIO_R2_Pin GPIO_PIN_8
#define M_GPIO_R2_GPIO_Port GPIOA
#define M_GPIO_R1_Pin GPIO_PIN_15
#define M_GPIO_R1_GPIO_Port GPIOA
#define TF_DET_Pin GPIO_PIN_4
#define TF_DET_GPIO_Port GPIOB
#define GPIO_2_Pin GPIO_PIN_5
#define GPIO_2_GPIO_Port GPIOB
#define INA226_SCL_Pin GPIO_PIN_6
#define INA226_SCL_GPIO_Port GPIOB
#define INA226_SDA_Pin GPIO_PIN_7
#define INA226_SDA_GPIO_Port GPIOB
#define GPIO_3_Pin GPIO_PIN_8
#define GPIO_3_GPIO_Port GPIOB
#define GPIO_4_Pin GPIO_PIN_9
#define GPIO_4_GPIO_Port GPIOB
/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
