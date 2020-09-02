EESchema Schematic File Version 5
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
Comment5 ""
Comment6 ""
Comment7 ""
Comment8 ""
Comment9 ""
$EndDescr
Wire Wire Line
	9150 4275 9950 4275
Wire Wire Line
	9150 3975 9950 3975
Wire Wire Line
	9150 4075 9950 4075
Wire Wire Line
	9150 4175 9950 4175
Wire Wire Line
	9250 3875 9950 3875
Text Label 9250 3975 0    50   ~ 0
M_GND
Text Label 9250 3875 0    50   ~ 0
GPIO_R3
Connection ~ 9150 4075
Text Label 9250 4275 0    50   ~ 0
M_GND
Wire Wire Line
	9150 3975 9150 4075
Wire Wire Line
	9150 4075 9150 4175
Text Label 9250 4175 0    50   ~ 0
M_GND
Text Label 9250 4075 0    50   ~ 0
M_GND
Wire Wire Line
	9150 4175 9150 4275
Wire Wire Line
	9150 4275 9150 4425
Connection ~ 9150 4175
$Comp
L power:GND #PWR0104
U 1 1 5DABC286
P 9150 4425
F 0 "#PWR0104" H 9150 4175 50  0001 C CNN
F 1 "GND" H 9155 4252 50  0000 C CNN
F 2 "" H 9150 4425 50  0001 C CNN
F 3 "" H 9150 4425 50  0001 C CNN
	1    9150 4425
	1    0    0    -1  
$EndComp
Connection ~ 9150 4275
Text Label 8175 4950 0    50   ~ 0
Ext_GND_Terminal
Wire Wire Line
	9950 3575 9250 3575
Wire Wire Line
	9250 3675 9950 3675
Wire Wire Line
	9950 3775 9250 3775
Text Label 9250 3675 0    50   ~ 0
M_RI
Text Label 9250 3775 0    50   ~ 0
GPIO_R2
Text Label 9250 3475 0    50   ~ 0
M_AUX_UART_Rx
Text Label 9250 3575 0    50   ~ 0
M_NET_LED
Text Label 9250 3375 0    50   ~ 0
M_AUX_UART_Tx
Wire Wire Line
	8100 3375 9950 3375
Wire Wire Line
	8000 3475 9950 3475
$Comp
L Connector_Generic:Conn_01x03 J6
U 1 1 5E16D4EB
P 7950 4575
F 0 "J6" V 7914 4388 50  0000 R CNN
F 1 "GND_CONN" V 7823 4388 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 7950 4575 50  0001 C CNN
F 3 "~" H 7950 4575 50  0001 C CNN
	1    7950 4575
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5E15B73A
P 7950 4950
F 0 "#PWR0106" H 7950 4700 50  0001 C CNN
F 1 "GND" H 7955 4777 50  0000 C CNN
F 2 "" H 7950 4950 50  0001 C CNN
F 3 "" H 7950 4950 50  0001 C CNN
	1    7950 4950
	1    0    0    -1  
$EndComp
Wire Wire Line
	7850 4950 7850 4775
Wire Wire Line
	7950 4775 7950 4950
Wire Wire Line
	8050 4775 8050 4950
Wire Wire Line
	7950 4950 7850 4950
Connection ~ 7950 4950
Text Label 8150 4950 0    50   ~ 0
Ext_GND_Terminal
Wire Wire Line
	8050 4950 8175 4950
Wire Wire Line
	5700 2400 6600 2400
Text Label 5700 2600 0    50   ~ 0
B_SPI_MISO-I2S_RXD
Text Label 5700 2400 0    50   ~ 0
GPIO_L1
Wire Wire Line
	6600 2300 5700 2300
Text Label 5700 2900 0    50   ~ 0
B_SPI_CS-I2S_CS
Wire Wire Line
	6600 2700 5700 2700
Wire Wire Line
	5700 2800 6600 2800
Text Label 5700 2500 0    50   ~ 0
PSM_IND
Wire Wire Line
	6600 2900 5700 2900
Wire Wire Line
	6600 2500 5700 2500
Wire Wire Line
	5700 2600 6600 2600
Text Label 5700 2700 0    50   ~ 0
B_SPI_MOSI-I2S_WA
Text Label 5700 2800 0    50   ~ 0
B_SPI_CLK-I2S_CLK
Text Label 5700 2300 0    50   ~ 0
M_VCC
Connection ~ 6100 2200
$Comp
L power:+3.3V #PWR0103
U 1 1 5DABC261
P 6100 2075
F 0 "#PWR0103" H 6100 1925 50  0001 C CNN
F 1 "+3.3V" H 6115 2248 50  0000 C CNN
F 2 "" H 6100 2075 50  0001 C CNN
F 3 "" H 6100 2075 50  0001 C CNN
	1    6100 2075
	1    0    0    -1  
$EndComp
Text Label 5700 2200 0    50   ~ 0
M_VCC
Wire Wire Line
	5700 2200 6100 2200
$Comp
L Connector_Generic:Conn_01x22 J2
U 1 1 5DABC1FA
P 6800 3200
F 0 "J2" H 6630 4442 50  0000 L CNN
F 1 "Left_Conn" H 6630 4351 50  0000 L CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x22_P1.27mm_Vertical" H 6800 3200 50  0001 C CNN
F 3 "~" H 6800 3200 50  0001 C CNN
	1    6800 3200
	1    0    0    -1  
$EndComp
Text Label 5700 3000 0    50   ~ 0
GPIO_L2
Wire Wire Line
	6100 2200 6600 2200
$Comp
L power:GND #PWR0107
U 1 1 5E15D4D4
P 7900 2875
F 0 "#PWR0107" H 7900 2625 50  0001 C CNN
F 1 "GND" H 7905 2702 50  0000 C CNN
F 2 "" H 7900 2875 50  0001 C CNN
F 3 "" H 7900 2875 50  0001 C CNN
	1    7900 2875
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 2075 6100 2200
$Comp
L Connector_Generic:Conn_01x03 J5
U 1 1 5E144EC4
P 7925 1375
F 0 "J5" V 7889 1188 50  0000 R CNN
F 1 "VCC_CONN" V 7798 1188 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 7925 1375 50  0001 C CNN
F 3 "~" H 7925 1375 50  0001 C CNN
	1    7925 1375
	0    -1   -1   0   
$EndComp
Connection ~ 8025 1575
Wire Wire Line
	7925 1575 8025 1575
Wire Wire Line
	8025 1575 8025 2175
Text Label 7575 1575 2    50   ~ 0
3V3_Terminal
Wire Wire Line
	7575 1575 7825 1575
Wire Wire Line
	5700 3000 6600 3000
Text Label 5700 3300 0    50   ~ 0
M_USB_DM
Text Label 5700 3500 0    50   ~ 0
M_MAIN_UART_Tx
Text Label 5700 3100 0    50   ~ 0
M_USB_VBUS
Wire Wire Line
	5700 3400 6600 3400
$Comp
L Connector_Generic:Conn_01x03 J1
U 1 1 5E14ACAE
P 4075 2725
F 0 "J1" V 4039 2538 50  0000 R CNN
F 1 "MAIN_UART_CONN" V 4275 3025 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 4075 2725 50  0001 C CNN
F 3 "~" H 4075 2725 50  0001 C CNN
	1    4075 2725
	0    -1   -1   0   
$EndComp
Wire Wire Line
	3975 2925 3975 3600
Wire Wire Line
	4075 2925 4075 3500
$Comp
L power:GND #PWR0101
U 1 1 5E155425
P 4175 2925
F 0 "#PWR0101" H 4175 2675 50  0001 C CNN
F 1 "GND" H 4180 2752 50  0000 C CNN
F 2 "" H 4175 2925 50  0001 C CNN
F 3 "" H 4175 2925 50  0001 C CNN
	1    4175 2925
	1    0    0    -1  
$EndComp
Text Label 5700 3200 0    50   ~ 0
M_USB_DP
Text Label 5700 3400 0    50   ~ 0
M_ADC
Wire Wire Line
	5275 3700 5275 4050
Wire Wire Line
	5275 4050 4250 4050
Connection ~ 5275 4050
Wire Wire Line
	6600 3900 5700 3900
Wire Wire Line
	5700 3800 6600 3800
Wire Wire Line
	3975 3600 6600 3600
Wire Wire Line
	4075 3500 6600 3500
Wire Wire Line
	5275 3700 6600 3700
Wire Wire Line
	4950 3100 6600 3100
Wire Wire Line
	4850 3200 6600 3200
Wire Wire Line
	4750 3300 6600 3300
$Comp
L Connector_Generic:Conn_01x04 J8
U 1 1 5E1766E6
P 4750 2400
F 0 "J8" V 4714 2113 50  0000 R CNN
F 1 "USB_CONN" V 4623 2113 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical" H 4750 2400 50  0001 C CNN
F 3 "~" H 4750 2400 50  0001 C CNN
	1    4750 2400
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4950 2600 4950 3100
Wire Wire Line
	4850 2600 4850 3200
Wire Wire Line
	4750 3300 4750 2600
Wire Wire Line
	4650 2600 4650 2900
Wire Wire Line
	9950 2475 9250 2475
Wire Wire Line
	8025 2175 9950 2175
Wire Wire Line
	8300 3175 9950 3175
Wire Wire Line
	8200 3275 9950 3275
Wire Wire Line
	9950 2275 9250 2275
Wire Wire Line
	9250 2375 9950 2375
Text Label 9250 2675 0    50   ~ 0
SIM_CLK
Text Label 9250 3075 0    50   ~ 0
M_SCL
Wire Wire Line
	9950 2675 9250 2675
Text Label 9250 2975 0    50   ~ 0
M_SDA
Text Label 9250 2775 0    50   ~ 0
SIM_GND
Wire Wire Line
	9950 2875 9250 2875
Text Label 9250 3175 0    50   ~ 0
M_DBG_UART_TX
Wire Wire Line
	9250 2775 9950 2775
Wire Wire Line
	9250 3075 9950 3075
Wire Wire Line
	9950 2975 9250 2975
Text Label 9250 2875 0    50   ~ 0
GPIO_R1
Text Label 9250 2575 0    50   ~ 0
SIM_IO
$Comp
L Connector_Generic:Conn_01x22 J3
U 1 1 5DABC1A3
P 10150 3175
F 0 "J3" H 10068 4392 50  0000 C CNN
F 1 "Right_Conn" H 10068 4301 50  0000 C CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x22_P1.27mm_Vertical" H 10150 3175 50  0001 C CNN
F 3 "~" H 10150 3175 50  0001 C CNN
	1    10150 3175
	1    0    0    -1  
$EndComp
Wire Wire Line
	9250 2575 9950 2575
Text Label 9250 3275 0    50   ~ 0
M_DBG_UART_Rx
Text Label 9250 2475 0    50   ~ 0
SIM_RST
Text Label 9250 2175 0    50   ~ 0
M_VCC
Text Label 9250 2375 0    50   ~ 0
V_SIM
Text Label 9250 2275 0    50   ~ 0
M_VCC
$Comp
L Connector_Generic:Conn_01x05 J7
U 1 1 5E16450C
P 8100 2675
F 0 "J7" V 8064 2388 50  0000 R CNN
F 1 "DBG_UART_CONN" V 7973 2388 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 8100 2675 50  0001 C CNN
F 3 "~" H 8100 2675 50  0001 C CNN
	1    8100 2675
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8300 2875 8300 3175
Wire Wire Line
	8200 2875 8200 3275
Wire Wire Line
	8100 2875 8100 3375
Wire Wire Line
	8000 2875 8000 3475
Text Label 5700 4300 0    50   ~ 0
GPIO_L4
Wire Wire Line
	5700 4000 6600 4000
Wire Wire Line
	6600 4100 5700 4100
Wire Wire Line
	5700 4200 6600 4200
Wire Wire Line
	6600 4300 5700 4300
Text Label 5700 4100 0    50   ~ 0
M_AP_READY
Text Label 5700 4200 0    50   ~ 0
GPIO_L3
Text Label 5700 4000 0    50   ~ 0
M_VDD_OUT
Text Label 5700 3600 0    50   ~ 0
M_MAIN_UART_Rx
Text Label 5700 3700 0    50   ~ 0
M_PWRKEY
Text Label 5700 3800 0    50   ~ 0
M_RESET
Text Label 5700 3900 0    50   ~ 0
PSM_EINT
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5E14E9AF
P 4150 3850
F 0 "J4" V 4114 3663 50  0000 R CNN
F 1 "PWR_KEY_TO_GND_CONN" V 4023 3663 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 4150 3850 50  0001 C CNN
F 3 "~" H 4150 3850 50  0001 C CNN
	1    4150 3850
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E155B67
P 4150 4050
F 0 "#PWR0102" H 4150 3800 50  0001 C CNN
F 1 "GND" H 4155 3877 50  0000 C CNN
F 2 "" H 4150 4050 50  0001 C CNN
F 3 "" H 4150 4050 50  0001 C CNN
	1    4150 4050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5E158BDD
P 3975 4700
F 0 "#PWR0105" H 3975 4450 50  0001 C CNN
F 1 "GND" H 3980 4527 50  0000 C CNN
F 2 "" H 3975 4700 50  0001 C CNN
F 3 "" H 3975 4700 50  0001 C CNN
	1    3975 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5275 4700 5275 4050
$Comp
L power:GND #PWR0108
U 1 1 5E17921B
P 4650 2900
F 0 "#PWR0108" H 4650 2650 50  0001 C CNN
F 1 "GND" H 4655 2727 50  0000 C CNN
F 2 "" H 4650 2900 50  0001 C CNN
F 3 "" H 4650 2900 50  0001 C CNN
	1    4650 2900
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW1
U 1 1 5E14FD6E
P 4175 4700
F 0 "SW1" H 4175 4984 50  0000 C CNN
F 1 "PWR_KEY_TO_GND_BTN" H 4175 4893 50  0000 C CNN
F 2 "LTD_Customized:SMD_Switch" H 4175 4900 50  0001 C CNN
F 3 "~" H 4175 4900 50  0001 C CNN
	1    4175 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	4375 4700 5275 4700
NoConn ~ 4025 5850
Text Label 3450 5450 0    50   ~ 0
V_SIM
Text Label 3450 5950 0    50   ~ 0
SIM_IO
Wire Wire Line
	3450 5950 4025 5950
$Comp
L Connector:SIM_Card J9
U 1 1 5E2685B4
P 4525 5750
F 0 "J9" H 5155 5849 50  0000 L CNN
F 1 "SIM_Card" H 5155 5758 50  0000 L CNN
F 2 "LTD_Customized:XUNPU_SMN-304" H 4525 6100 50  0001 C CNN
F 3 " ~" H 4475 5750 50  0001 C CNN
	1    4525 5750
	1    0    0    -1  
$EndComp
Wire Wire Line
	3450 5450 4025 5450
Wire Wire Line
	3450 5550 4025 5550
Text Label 3450 5750 0    50   ~ 0
SIM_GND
Wire Wire Line
	3450 5750 4025 5750
Wire Wire Line
	3450 5650 4025 5650
Text Label 3450 5650 0    50   ~ 0
SIM_CLK
Text Label 3450 5550 0    50   ~ 0
SIM_RST
$Comp
L Device:R R2
U 1 1 5E291765
P 1475 5625
F 0 "R2" H 1405 5580 50  0000 R CNN
F 1 "2.2k" H 1405 5670 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1405 5625 50  0001 C CNN
F 3 "~" H 1475 5625 50  0001 C CNN
	1    1475 5625
	-1   0    0    1   
$EndComp
Text Label 725  6275 0    50   ~ 0
M_NET_LED
Wire Wire Line
	725  6275 1125 6275
$Comp
L Device:LED D2
U 1 1 5E29173F
P 1475 5925
F 0 "D2" V 1513 5807 50  0000 R CNN
F 1 "LED" V 1422 5807 50  0000 R CNN
F 2 "LED_SMD:LED_0603_1608Metric" H 1475 5925 50  0001 C CNN
F 3 "~" H 1475 5925 50  0001 C CNN
	1    1475 5925
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 5E291728
P 1475 6475
F 0 "#PWR0109" H 1475 6225 50  0001 C CNN
F 1 "GND" H 1480 6302 50  0000 C CNN
F 2 "" H 1475 6475 50  0001 C CNN
F 3 "" H 1475 6475 50  0001 C CNN
	1    1475 6475
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J11
U 1 1 5E29DEDA
P 1275 5475
F 0 "J11" H 1450 5400 50  0000 C CNN
F 1 "NET_LED_SW" H 1450 5575 50  0000 C CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 1275 5475 50  0001 C CNN
F 3 "~" H 1275 5475 50  0001 C CNN
	1    1275 5475
	-1   0    0    1   
$EndComp
$Comp
L Transistor_BJT:DTC143Z Q1
U 1 1 5E2944A6
P 1375 6275
F 0 "Q1" H 1562 6320 50  0000 L CNN
F 1 "DTC143Z" H 1562 6230 50  0000 L CNN
F 2 "LTD_Customized:SOT-723" H 1375 6275 50  0001 L CNN
F 3 "" H 1375 6275 50  0001 L CNN
	1    1375 6275
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0110
U 1 1 5E286A47
P 1425 3775
F 0 "#PWR0110" H 1425 3625 50  0001 C CNN
F 1 "+3.3V" H 1440 3948 50  0000 C CNN
F 2 "" H 1425 3775 50  0001 C CNN
F 3 "" H 1425 3775 50  0001 C CNN
	1    1425 3775
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0111
U 1 1 5E28953D
P 1425 4475
F 0 "#PWR0111" H 1425 4225 50  0001 C CNN
F 1 "GND" H 1430 4302 50  0000 C CNN
F 2 "" H 1425 4475 50  0001 C CNN
F 3 "" H 1425 4475 50  0001 C CNN
	1    1425 4475
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J10
U 1 1 5E28BC8E
P 1225 3875
F 0 "J10" H 1400 3800 50  0000 C CNN
F 1 "PWR_LED_SW" H 1400 3975 50  0000 C CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 1225 3875 50  0001 C CNN
F 3 "~" H 1225 3875 50  0001 C CNN
	1    1225 3875
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D1
U 1 1 5E288384
P 1425 4325
F 0 "D1" V 1463 4207 50  0000 R CNN
F 1 "LED" V 1372 4207 50  0000 R CNN
F 2 "LED_SMD:LED_0603_1608Metric" H 1425 4325 50  0001 C CNN
F 3 "~" H 1425 4325 50  0001 C CNN
	1    1425 4325
	0    -1   -1   0   
$EndComp
$Comp
L Device:R R1
U 1 1 5E287B32
P 1425 4025
F 0 "R1" H 1355 3980 50  0000 R CNN
F 1 "2.2k" H 1355 4070 50  0000 R CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1355 4025 50  0001 C CNN
F 3 "~" H 1425 4025 50  0001 C CNN
	1    1425 4025
	-1   0    0    1   
$EndComp
$Comp
L power:+3.3V #PWR0112
U 1 1 5E29B688
P 1475 5375
F 0 "#PWR0112" H 1475 5225 50  0001 C CNN
F 1 "+3.3V" H 1490 5548 50  0000 C CNN
F 2 "" H 1475 5375 50  0001 C CNN
F 3 "" H 1475 5375 50  0001 C CNN
	1    1475 5375
	1    0    0    -1  
$EndComp
$EndSCHEMATC
