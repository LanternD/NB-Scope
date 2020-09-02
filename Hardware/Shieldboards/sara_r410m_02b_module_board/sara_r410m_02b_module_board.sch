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
Text Label 9950 2500 0    50   ~ 0
M_DBG_UART_TX
Text Label 9950 3600 0    50   ~ 0
M_GND
Text Label 8225 1600 0    50   ~ 0
M_VCC
Text Notes 8275 1050 0    50   ~ 0
Connectors to the module board
Text Label 9950 2000 0    50   ~ 0
SIM_CLK
$Comp
L power:GND #PWR0102
U 1 1 5DABC251
P 9200 5950
F 0 "#PWR0102" H 9200 5700 50  0001 C CNN
F 1 "GND" V 9205 5822 50  0000 R CNN
F 2 "" H 9200 5950 50  0001 C CNN
F 3 "" H 9200 5950 50  0001 C CNN
	1    9200 5950
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0103
U 1 1 5DABC261
P 8625 1375
F 0 "#PWR0103" H 8625 1225 50  0001 C CNN
F 1 "+3.3V" H 8640 1548 50  0000 C CNN
F 2 "" H 8625 1375 50  0001 C CNN
F 3 "" H 8625 1375 50  0001 C CNN
	1    8625 1375
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x22 J2
U 1 1 5DABC1FA
P 9325 2500
F 0 "J2" H 9155 3742 50  0000 L CNN
F 1 "Left_Conn" H 9155 3651 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x22_P1.27mm_Vertical" H 9325 2500 50  0001 C CNN
F 3 "~" H 9325 2500 50  0001 C CNN
	1    9325 2500
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C1
U 1 1 5DABC162
P 9550 5850
F 0 "C1" V 9450 6000 50  0000 C CNN
F 1 "100nF" V 9650 5950 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 9550 5850 50  0001 C CNN
F 3 "~" H 9550 5850 50  0001 C CNN
	1    9550 5850
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x22 J3
U 1 1 5DABC1A3
P 10850 2500
F 0 "J3" H 10768 3717 50  0000 C CNN
F 1 "Right_Conn" H 10768 3626 50  0000 C CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x22_P1.27mm_Vertical" H 10850 2500 50  0001 C CNN
F 3 "~" H 10850 2500 50  0001 C CNN
	1    10850 2500
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW1
U 1 1 5DABC173
P 9550 5550
F 0 "SW1" H 9700 5650 50  0000 C CNN
F 1 "SW_Push" H 9600 5450 50  0000 C CNN
F 2 "LTD_Customized:SMD_Switch" H 9550 5750 50  0001 C CNN
F 3 "~" H 9550 5750 50  0001 C CNN
	1    9550 5550
	1    0    0    -1  
$EndComp
Text Label 9950 1900 0    50   ~ 0
SIM_IO
Wire Wire Line
	8225 1700 9125 1700
Wire Wire Line
	9125 1800 8225 1800
Wire Wire Line
	8225 1900 9125 1900
Connection ~ 9900 5550
Wire Wire Line
	9125 3000 8225 3000
Wire Wire Line
	9350 5550 9200 5550
Wire Notes Line
	9000 4850 9000 6350
Wire Notes Line
	9000 6350 11050 6350
Wire Wire Line
	9850 3500 9850 3600
Wire Wire Line
	9125 2000 8225 2000
Wire Wire Line
	8225 2100 9125 2100
Wire Wire Line
	9125 2200 8225 2200
Wire Wire Line
	8225 2300 9125 2300
Wire Wire Line
	9125 2400 8225 2400
Wire Wire Line
	8225 2500 9125 2500
Wire Wire Line
	9125 2600 8225 2600
Wire Wire Line
	9125 2800 8225 2800
Wire Wire Line
	8225 2900 9125 2900
Text Label 9950 3000 0    50   ~ 0
M_RI
Text Label 9950 3100 0    50   ~ 0
GPIO_R2
Text Label 9950 3200 0    50   ~ 0
GPIO_R3
Text Label 9950 3400 0    50   ~ 0
M_GND
Text Label 9950 2100 0    50   ~ 0
SIM_GND
Text Label 9950 2200 0    50   ~ 0
GPIO_R1
Wire Wire Line
	8625 1500 9125 1500
Text Label 9950 1600 0    50   ~ 0
M_VCC
Text Label 8225 3300 0    50   ~ 0
M_VDD_OUT
Text Label 9950 3300 0    50   ~ 0
M_GND
Text Label 9950 2700 0    50   ~ 0
M_AUX_UART_Tx
Text Label 9950 1800 0    50   ~ 0
SIM_RST
Text Label 9950 1700 0    50   ~ 0
V_SIM
Wire Wire Line
	8225 2700 9125 2700
Wire Wire Line
	8225 1500 8625 1500
Wire Wire Line
	9125 1600 8225 1600
Connection ~ 8625 1500
Connection ~ 9850 3600
Text Label 9950 2600 0    50   ~ 0
M_DBG_UART_Rx
Text Label 9950 2800 0    50   ~ 0
M_AUX_UART_Rx
Text Label 9950 2900 0    50   ~ 0
M_NET_LED
Wire Wire Line
	9850 3500 10650 3500
Wire Wire Line
	9950 3200 10650 3200
Wire Wire Line
	8625 1375 8625 1500
Text Label 9950 2300 0    50   ~ 0
M_SDA
Wire Wire Line
	9950 2400 10650 2400
Wire Wire Line
	10650 2300 9950 2300
Wire Wire Line
	9850 3600 9850 3750
Wire Wire Line
	9850 3600 10650 3600
Wire Wire Line
	9850 3300 9850 3400
Wire Wire Line
	9850 3300 10650 3300
Wire Wire Line
	9850 3400 10650 3400
Wire Wire Line
	9850 3400 9850 3500
Wire Wire Line
	9900 5850 9900 5550
Connection ~ 9850 3500
Wire Wire Line
	9200 5850 9200 5950
Wire Notes Line
	9000 4850 11050 4850
Wire Wire Line
	9950 1500 10650 1500
Wire Wire Line
	10650 1600 9950 1600
Wire Wire Line
	9950 1700 10650 1700
Wire Wire Line
	10650 1800 9950 1800
Wire Wire Line
	9950 1900 10650 1900
Wire Wire Line
	10650 2000 9950 2000
Wire Wire Line
	9950 2100 10650 2100
Wire Wire Line
	10650 2200 9950 2200
Wire Wire Line
	9950 2500 10650 2500
Wire Wire Line
	10650 2600 9950 2600
Wire Wire Line
	10650 2700 9950 2700
Wire Wire Line
	9950 2800 10650 2800
Wire Wire Line
	10650 2900 9950 2900
Wire Wire Line
	9950 3000 10650 3000
Wire Wire Line
	10650 3100 9950 3100
Connection ~ 9850 3400
Wire Wire Line
	9650 5850 9900 5850
Wire Wire Line
	9200 5550 9200 5850
Text Label 8225 3600 0    50   ~ 0
GPIO_L4
Text Label 9950 1500 0    50   ~ 0
M_VCC
Text Label 9950 2400 0    50   ~ 0
M_SCL
Wire Notes Line
	11050 6350 11050 4850
Text Notes 9150 3750 0    50   ~ 0
From Node Base
Text Label 8225 1800 0    50   ~ 0
PSM_IND
Text Label 8225 1900 0    50   ~ 0
B_SPI_MISO-I2S_RXD
Text Label 9950 3500 0    50   ~ 0
M_GND
Wire Wire Line
	9125 3200 8225 3200
Wire Wire Line
	9900 5550 9750 5550
Text Label 8225 1700 0    50   ~ 0
GPIO_L1
Text Label 8225 1500 0    50   ~ 0
M_VCC
Text Label 8225 2500 0    50   ~ 0
M_USB_DP
Text Label 8225 2600 0    50   ~ 0
M_USB_DM
Text Label 8225 2700 0    50   ~ 0
M_ADC
Text Label 8225 2800 0    50   ~ 0
M_MAIN_UART_Tx
Text Label 8225 2900 0    50   ~ 0
M_MAIN_UART_Rx
Wire Wire Line
	8225 3100 9125 3100
Wire Wire Line
	8225 3300 9125 3300
Wire Wire Line
	9125 3400 8225 3400
Wire Wire Line
	8225 3500 9125 3500
Connection ~ 9200 5850
$Comp
L power:GND #PWR0104
U 1 1 5DABC286
P 9850 3750
F 0 "#PWR0104" H 9850 3500 50  0001 C CNN
F 1 "GND" H 9855 3577 50  0000 C CNN
F 2 "" H 9850 3750 50  0001 C CNN
F 3 "" H 9850 3750 50  0001 C CNN
	1    9850 3750
	1    0    0    -1  
$EndComp
Text Notes 10150 6200 0    50   ~ 0
Reset Buttom Circuit
Wire Wire Line
	9900 5550 10500 5550
Text Label 8225 2000 0    50   ~ 0
B_SPI_MOSI-I2S_WA
Text Label 8225 2100 0    50   ~ 0
B_SPI_CLK-I2S_CLK
Text Label 8225 2200 0    50   ~ 0
B_SPI_CS-I2S_CS
Wire Wire Line
	9450 5850 9200 5850
Text Label 8225 2300 0    50   ~ 0
GPIO_L2
Text Label 8225 2400 0    50   ~ 0
M_USB_VBUS
Wire Wire Line
	9125 3600 8225 3600
Text Label 8225 3000 0    50   ~ 0
M_PWRKEY
Text Label 8225 3100 0    50   ~ 0
M_RESET
Text Label 8225 3200 0    50   ~ 0
PSM_EINT
Text Label 8225 3400 0    50   ~ 0
M_AP_READY
Text Label 8225 3500 0    50   ~ 0
GPIO_L3
$Comp
L dly_customized:uBlox_SARA-R410M-02B U1
U 1 1 5DA66C5C
P 1750 5900
F 0 "U1" H 1800 9575 50  0000 C CNN
F 1 "uBlox_SARA-R410M-02B" H 2850 9000 50  0000 C CNN
F 2 "LTD_Customized:Ublox_SARA-R410M-02B" H 1750 5900 50  0001 C CNN
F 3 "" H 1750 5900 50  0001 C CNN
	1    1750 5900
	1    0    0    -1  
$EndComp
NoConn ~ 4550 2850
NoConn ~ 4550 2950
NoConn ~ 4550 3050
NoConn ~ 4550 3150
NoConn ~ 4550 3250
NoConn ~ 4550 3950
NoConn ~ 4550 4050
NoConn ~ 4550 4150
NoConn ~ 4550 4250
NoConn ~ 1550 3350
NoConn ~ 1550 3550
NoConn ~ 1550 3650
NoConn ~ 1550 3750
NoConn ~ 1550 3850
NoConn ~ 3800 2100
NoConn ~ 2500 2100
Connection ~ 3750 1000
Wire Wire Line
	4075 700  4075 550 
$Comp
L Device:R R1
U 1 1 5DA77154
P 3500 1000
F 0 "R1" V 3293 1000 50  0000 C CNN
F 1 "0" V 3384 1000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3430 1000 50  0001 C CNN
F 3 "~" H 3500 1000 50  0001 C CNN
	1    3500 1000
	0    1    1    0   
$EndComp
Connection ~ 3900 1375
Wire Wire Line
	4075 1375 3900 1375
$Comp
L Device:C_Small C2
U 1 1 5DA7C173
P 3250 1200
F 0 "C2" H 3342 1246 50  0000 L CNN
F 1 "100nF" H 3342 1155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3250 1200 50  0001 C CNN
F 3 "~" H 3250 1200 50  0001 C CNN
	1    3250 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	4275 1375 4075 1375
Wire Wire Line
	3250 1300 3250 1375
Wire Wire Line
	3750 1375 3900 1375
Wire Wire Line
	3875 1000 3750 1000
Wire Wire Line
	3750 1100 3750 1000
$Comp
L Device:C_Small C3
U 1 1 5DA7D9D5
P 3750 1200
F 0 "C3" H 3842 1246 50  0000 L CNN
F 1 "100nF" H 3842 1155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3750 1200 50  0001 C CNN
F 3 "~" H 3750 1200 50  0001 C CNN
	1    3750 1200
	1    0    0    -1  
$EndComp
Wire Wire Line
	3250 1100 3250 1000
$Comp
L DLY_Customized:1865 J1
U 1 1 5DA16505
P 4175 1000
F 0 "J1" H 4405 1000 50  0000 L CNN
F 1 "1865" H 4375 700 50  0001 L BNN
F 2 "LTD_Customized:SMA_Antenna" H 3975 1350 50  0001 L BNN
F 3 "Bad" H 4425 800 50  0001 L BNN
F 4 "SMA Connector" H 4425 1250 50  0001 L BNN "Field4"
	1    4175 1000
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5DA9C78F
P 3900 1425
F 0 "#PWR0105" H 3900 1175 50  0001 C CNN
F 1 "GND" H 4000 1300 50  0000 C CNN
F 2 "" H 3900 1425 50  0001 C CNN
F 3 "" H 3900 1425 50  0001 C CNN
	1    3900 1425
	1    0    0    -1  
$EndComp
Wire Wire Line
	3750 1000 3650 1000
Wire Wire Line
	4275 700  4275 550 
Wire Wire Line
	3250 1375 3750 1375
Connection ~ 3750 1375
Wire Wire Line
	3900 1375 3900 1425
Wire Wire Line
	4275 1300 4275 1375
Wire Wire Line
	3250 1000 3350 1000
Wire Wire Line
	3750 1300 3750 1375
Connection ~ 4075 1375
Wire Wire Line
	4075 1300 4075 1375
$Comp
L power:+3.3V #PWR0101
U 1 1 5DAA0278
P 3400 1750
F 0 "#PWR0101" H 3400 1600 50  0001 C CNN
F 1 "+3.3V" H 3415 1923 50  0000 C CNN
F 2 "" H 3400 1750 50  0001 C CNN
F 3 "" H 3400 1750 50  0001 C CNN
	1    3400 1750
	1    0    0    -1  
$EndComp
Connection ~ 4175 550 
$Comp
L power:GND #PWR0106
U 1 1 5DA9E95E
P 4175 550
F 0 "#PWR0106" H 4175 300 50  0001 C CNN
F 1 "GND" H 4175 375 50  0000 C CNN
F 2 "" H 4175 550 50  0001 C CNN
F 3 "" H 4175 550 50  0001 C CNN
	1    4175 550 
	1    0    0    -1  
$EndComp
Wire Wire Line
	4075 550  4175 550 
Wire Wire Line
	4275 550  4175 550 
$Comp
L Device:C_Small C6
U 1 1 5DB78BA6
P 3700 1900
F 0 "C6" H 3792 1946 50  0000 L CNN
F 1 "100nF" H 3792 1855 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 3700 1900 50  0001 C CNN
F 3 "~" H 3700 1900 50  0001 C CNN
	1    3700 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 1750 3400 1800
$Comp
L power:GND #PWR0107
U 1 1 5DAA3D39
P 3700 2000
F 0 "#PWR0107" H 3700 1750 50  0001 C CNN
F 1 "GND" H 3800 1875 50  0000 C CNN
F 2 "" H 3700 2000 50  0001 C CNN
F 3 "" H 3700 2000 50  0001 C CNN
	1    3700 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3700 1800 3400 1800
Connection ~ 3400 1800
Wire Wire Line
	3400 1800 3400 1975
Wire Wire Line
	3500 2100 3500 1975
Wire Wire Line
	3500 1975 3400 1975
Connection ~ 3400 1975
Wire Wire Line
	3400 1975 3400 2100
Wire Wire Line
	3600 2100 3600 1975
Wire Wire Line
	3600 1975 3500 1975
Connection ~ 3500 1975
Wire Wire Line
	3100 2100 3100 1000
Wire Wire Line
	3100 1000 3250 1000
Connection ~ 3250 1000
$Comp
L power:GND #PWR0108
U 1 1 5DAAC410
P 4150 5225
F 0 "#PWR0108" H 4150 4975 50  0001 C CNN
F 1 "GND" H 4155 5052 50  0000 C CNN
F 2 "" H 4150 5225 50  0001 C CNN
F 3 "" H 4150 5225 50  0001 C CNN
	1    4150 5225
	1    0    0    -1  
$EndComp
Wire Wire Line
	4150 5225 4150 5100
Text Label 4825 3850 0    50   ~ 0
SIM_CLK
Text Label 4825 3750 0    50   ~ 0
SIM_IO
Text Label 4825 3650 0    50   ~ 0
SIM_RST
Text Label 4825 3550 0    50   ~ 0
V_SIM
Wire Wire Line
	4825 3550 4550 3550
Wire Wire Line
	4550 3650 4825 3650
Wire Wire Line
	4825 3750 4550 3750
Wire Wire Line
	4825 3850 4550 3850
Text Label 4825 3950 0    50   ~ 0
SIM_GND
$Comp
L power:GND #PWR0109
U 1 1 5DAC085E
P 4825 4000
F 0 "#PWR0109" H 4825 3750 50  0001 C CNN
F 1 "GND" H 4830 3827 50  0000 C CNN
F 2 "" H 4825 4000 50  0001 C CNN
F 3 "" H 4825 4000 50  0001 C CNN
	1    4825 4000
	1    0    0    -1  
$EndComp
Wire Wire Line
	4825 4000 4825 3950
Text Label 900  3450 0    50   ~ 0
M_RI
Wire Wire Line
	1550 3450 900  3450
Text Label 875  4050 0    50   ~ 0
M_MAIN_UART_Tx
Text Label 875  3950 0    50   ~ 0
M_MAIN_UART_Rx
Wire Wire Line
	1550 3950 875  3950
Wire Wire Line
	875  4050 1550 4050
Text Label 3500 5325 0    50   ~ 0
M_USB_DP
Text Label 3400 5425 0    50   ~ 0
M_USB_DM
Text Label 1025 5400 0    50   ~ 0
M_USB_VBUS
Wire Wire Line
	3400 5425 3400 5100
Wire Wire Line
	3500 5100 3500 5325
Text Label 900  3150 0    50   ~ 0
M_VDD_OUT
Wire Wire Line
	900  3150 1550 3150
Text Label 875  4250 0    50   ~ 0
M_PWR_KEY_NEW
Wire Wire Line
	875  4250 1550 4250
Wire Wire Line
	4825 3450 4550 3450
Text Label 3200 5625 0    50   ~ 0
SARA_SDA
Text Label 3300 5525 0    50   ~ 0
SARA_SCL
Wire Wire Line
	3300 5525 3300 5100
Wire Wire Line
	3200 5100 3200 5625
$Comp
L Logic_LevelTranslator:TXB0304RUT U2
U 1 1 5DB624F8
P 6750 2350
F 0 "U2" H 6750 1561 50  0000 C CNN
F 1 "TXB0304RUT" H 7050 1675 50  0000 C CNN
F 2 "Package_DFN_QFN:Texas_R_PUQFN-N12" H 6750 1600 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/txb0304.pdf" H 6860 2445 50  0001 C CNN
	1    6750 2350
	1    0    0    -1  
$EndComp
$Comp
L Logic_LevelTranslator:TXB0304RUT U3
U 1 1 5DB65707
P 5600 6825
F 0 "U3" H 5600 6036 50  0000 C CNN
F 1 "TXB0304RUT" H 5250 6150 50  0000 C CNN
F 2 "Package_DFN_QFN:Texas_R_PUQFN-N12" H 5600 6075 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/txb0304.pdf" H 5710 6920 50  0001 C CNN
	1    5600 6825
	1    0    0    -1  
$EndComp
Text Notes 6050 7625 0    50   ~ 0
For right hand part
Text Notes 5925 3100 0    50   ~ 0
For left hand part
Text Label 6175 6725 0    50   ~ 0
M_SDA
Text Label 6175 6925 0    50   ~ 0
M_SCL
Text Label 4725 6725 0    50   ~ 0
SARA_SDA
Text Label 4725 6925 0    50   ~ 0
SARA_SCL
Text Label 6175 1450 0    50   ~ 0
M_VDD_OUT
Text Label 4875 5900 0    50   ~ 0
M_VDD_OUT
Wire Wire Line
	4875 5900 4975 5900
Wire Wire Line
	5500 5900 5500 6125
Wire Wire Line
	6175 1450 6275 1450
Wire Wire Line
	6650 1450 6650 1650
Wire Wire Line
	6350 1850 6275 1850
Wire Wire Line
	6275 1850 6275 1575
Connection ~ 6275 1450
Wire Wire Line
	6275 1450 6650 1450
Wire Wire Line
	5200 6325 5150 6325
Wire Wire Line
	5150 6325 5150 5900
Connection ~ 5150 5900
Wire Wire Line
	5150 5900 5500 5900
$Comp
L power:+3.3V #PWR0110
U 1 1 5DBA2AB8
P 5700 5900
F 0 "#PWR0110" H 5700 5750 50  0001 C CNN
F 1 "+3.3V" H 5715 6073 50  0000 C CNN
F 2 "" H 5700 5900 50  0001 C CNN
F 3 "" H 5700 5900 50  0001 C CNN
	1    5700 5900
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0111
U 1 1 5DBA5F33
P 6850 1625
F 0 "#PWR0111" H 6850 1475 50  0001 C CNN
F 1 "+3.3V" H 7000 1675 50  0000 C CNN
F 2 "" H 6850 1625 50  0001 C CNN
F 3 "" H 6850 1625 50  0001 C CNN
	1    6850 1625
	1    0    0    -1  
$EndComp
Text Label 6175 6525 0    50   ~ 0
GPIO_R1
Text Label 4725 6525 0    50   ~ 0
SARA_GPIO5
Wire Wire Line
	6175 6525 6000 6525
Wire Wire Line
	6000 6725 6175 6725
Wire Wire Line
	6175 6925 6000 6925
Wire Wire Line
	6175 7125 6000 7125
Wire Wire Line
	5200 6925 4725 6925
Wire Wire Line
	4725 6725 5200 6725
Wire Wire Line
	5200 6525 4725 6525
$Comp
L power:GND #PWR0112
U 1 1 5DBCBEF6
P 5600 7525
F 0 "#PWR0112" H 5600 7275 50  0001 C CNN
F 1 "GND" H 5605 7352 50  0000 C CNN
F 2 "" H 5600 7525 50  0001 C CNN
F 3 "" H 5600 7525 50  0001 C CNN
	1    5600 7525
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0114
U 1 1 5DBCE443
P 6750 3050
F 0 "#PWR0114" H 6750 2800 50  0001 C CNN
F 1 "GND" H 6755 2877 50  0000 C CNN
F 2 "" H 6750 3050 50  0001 C CNN
F 3 "" H 6750 3050 50  0001 C CNN
	1    6750 3050
	1    0    0    -1  
$EndComp
Text Label 7225 2050 0    50   ~ 0
M_RESET
Text Label 7225 2450 0    50   ~ 0
GPIO_L2
Wire Wire Line
	6850 1625 6850 1650
Wire Wire Line
	5700 5900 5700 5975
Wire Wire Line
	4725 7125 5200 7125
Wire Wire Line
	7225 2050 7150 2050
Wire Wire Line
	7225 2250 7150 2250
Wire Wire Line
	7225 2450 7150 2450
Text Label 5775 2650 0    50   ~ 0
SARA_GPIO6
Text Label 5775 2050 0    50   ~ 0
SARA_RESET
Text Label 5775 2450 0    50   ~ 0
SARA_GPIO2
Wire Wire Line
	5775 2050 6350 2050
Wire Wire Line
	6350 2250 5775 2250
Wire Wire Line
	5775 2450 6350 2450
Wire Wire Line
	5775 2650 6350 2650
Wire Wire Line
	875  4350 1550 4350
Text Label 10500 5550 0    50   ~ 0
SARA_RESET
Text Notes 9650 5100 0    50   ~ 0
Note: no pull-up resistor needed \n(has internal one)
Text Label 7225 2250 0    50   ~ 0
GPIO_L3
Wire Wire Line
	7225 2650 7150 2650
Text Label 1725 5500 0    50   ~ 0
SARA_RESET
Text Label 1725 5600 0    50   ~ 0
SARA_GPIO6
Text Label 2900 5575 1    50   ~ 0
SARA_GPIO2
Wire Wire Line
	2900 5575 2900 5100
Text Label 4825 3450 0    50   ~ 0
SARA_GPIO5
Wire Wire Line
	1725 5600 2500 5600
Wire Wire Line
	2500 5600 2500 5100
Wire Wire Line
	2400 5100 2400 5500
Wire Wire Line
	2400 5500 1725 5500
Wire Wire Line
	2300 5400 2300 5100
Text Label 875  4350 0    50   ~ 0
M_NET_LED
Text Label 7225 2650 0    50   ~ 0
GPIO_L1
Text Label 3000 5575 1    50   ~ 0
SARA_GPIO3
Wire Wire Line
	3000 5575 3000 5100
Text Label 3100 5725 0    50   ~ 0
SARA_STATUS_LED
Wire Wire Line
	3100 5725 3100 5100
$Comp
L Transistor_BJT:MMBT3904 Q1
U 1 1 5D76365F
P 8425 5650
F 0 "Q1" H 8616 5696 50  0000 L CNN
F 1 "MMBT3904" H 8025 5500 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 8625 5575 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 8425 5650 50  0001 L CNN
	1    8425 5650
	1    0    0    -1  
$EndComp
$Comp
L Device:R R22
U 1 1 5D7709F6
P 7950 5650
F 0 "R22" V 7850 5650 50  0000 C CNN
F 1 "2.2k" V 7950 5650 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7880 5650 50  0001 C CNN
F 3 "~" H 7950 5650 50  0001 C CNN
	1    7950 5650
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0150
U 1 1 5D771A78
P 8525 5925
F 0 "#PWR0150" H 8525 5675 50  0001 C CNN
F 1 "GND" H 8530 5752 50  0000 C CNN
F 2 "" H 8525 5925 50  0001 C CNN
F 3 "" H 8525 5925 50  0001 C CNN
	1    8525 5925
	1    0    0    -1  
$EndComp
Wire Wire Line
	8100 5650 8225 5650
Wire Wire Line
	8525 5850 8525 5925
Wire Wire Line
	8525 5300 8525 5450
$Comp
L Device:LED D1
U 1 1 5D7613BF
P 8375 5300
F 0 "D1" V 8350 5450 50  0000 R CNN
F 1 "LED" V 8475 5475 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 8400 5475 50  0001 C CNN
F 3 "~" H 8400 5475 50  0001 C CNN
	1    8375 5300
	-1   0    0    1   
$EndComp
Wire Wire Line
	7750 5275 7750 5300
$Comp
L Device:R R5
U 1 1 5DBCE477
P 8075 5300
F 0 "R5" V 7975 5300 50  0000 C CNN
F 1 "2.2k" V 8075 5300 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8005 5300 50  0001 C CNN
F 3 "~" H 8075 5300 50  0001 C CNN
	1    8075 5300
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7750 5300 7925 5300
$Comp
L power:+3.3V #PWR0113
U 1 1 5DBE5185
P 7750 5275
F 0 "#PWR0113" H 7750 5125 50  0001 C CNN
F 1 "+3.3V" H 7765 5448 50  0000 C CNN
F 2 "" H 7750 5275 50  0001 C CNN
F 3 "" H 7750 5275 50  0001 C CNN
	1    7750 5275
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C8
U 1 1 5DB4DD7D
P 6150 6075
F 0 "C8" H 6050 6000 50  0000 C CNN
F 1 "100nF" H 5900 6050 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6150 6075 50  0001 C CNN
F 3 "~" H 6150 6075 50  0001 C CNN
	1    6150 6075
	-1   0    0    1   
$EndComp
$Comp
L Device:C_Small C7
U 1 1 5DBED931
P 4975 6050
F 0 "C7" H 4875 6200 50  0000 C CNN
F 1 "100nF" H 5075 6150 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4975 6050 50  0001 C CNN
F 3 "~" H 4975 6050 50  0001 C CNN
	1    4975 6050
	-1   0    0    1   
$EndComp
$Comp
L Device:C_Small C5
U 1 1 5DB736A5
P 7300 1725
F 0 "C5" H 7175 1725 50  0000 C CNN
F 1 "100nF" H 7150 1650 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7300 1725 50  0001 C CNN
F 3 "~" H 7300 1725 50  0001 C CNN
	1    7300 1725
	-1   0    0    1   
$EndComp
$Comp
L Device:C_Small C4
U 1 1 5DB75DB1
P 6125 1675
F 0 "C4" H 6025 1825 50  0000 C CNN
F 1 "100nF" H 6225 1775 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6125 1675 50  0001 C CNN
F 3 "~" H 6125 1675 50  0001 C CNN
	1    6125 1675
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0115
U 1 1 5DB8433B
P 4975 6225
F 0 "#PWR0115" H 4975 5975 50  0001 C CNN
F 1 "GND" H 4980 6052 50  0000 C CNN
F 2 "" H 4975 6225 50  0001 C CNN
F 3 "" H 4975 6225 50  0001 C CNN
	1    4975 6225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0116
U 1 1 5DB8965C
P 7300 1825
F 0 "#PWR0116" H 7300 1575 50  0001 C CNN
F 1 "GND" H 7150 1775 50  0000 C CNN
F 2 "" H 7300 1825 50  0001 C CNN
F 3 "" H 7300 1825 50  0001 C CNN
	1    7300 1825
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 5DB8E531
P 6125 1775
F 0 "#PWR0117" H 6125 1525 50  0001 C CNN
F 1 "GND" H 5975 1700 50  0000 C CNN
F 2 "" H 6125 1775 50  0001 C CNN
F 3 "" H 6125 1775 50  0001 C CNN
	1    6125 1775
	1    0    0    -1  
$EndComp
Wire Wire Line
	6125 1575 6275 1575
Connection ~ 6275 1575
Wire Wire Line
	6275 1575 6275 1450
Wire Wire Line
	7300 1625 6850 1625
Connection ~ 6850 1625
$Comp
L power:GND #PWR0118
U 1 1 5DBAEE73
P 6150 6175
F 0 "#PWR0118" H 6150 5925 50  0001 C CNN
F 1 "GND" H 6000 6125 50  0000 C CNN
F 2 "" H 6150 6175 50  0001 C CNN
F 3 "" H 6150 6175 50  0001 C CNN
	1    6150 6175
	1    0    0    -1  
$EndComp
Wire Wire Line
	6150 5975 5700 5975
Connection ~ 5700 5975
Wire Wire Line
	5700 5975 5700 6125
Wire Wire Line
	4975 5950 4975 5900
Connection ~ 4975 5900
Wire Wire Line
	4975 5900 5150 5900
Wire Wire Line
	4975 6150 4975 6225
Text Label 5775 2250 0    50   ~ 0
SARA_GPIO3
Text Label 7025 5650 0    50   ~ 0
SARA_STATUS_LED
Wire Wire Line
	7025 5650 7800 5650
NoConn ~ 6175 7125
NoConn ~ 4725 7125
Text Label 6030 4320 0    50   ~ 0
GPIO_L4
Text Notes 725  6125 0    50   ~ 0
Note: \nThe SARA uses the STUPID ITU-T V.24 recommendation. \nSo the "RXD" on the module means the RXD of the MCU. \nIt actually outputs data.
$Comp
L Device:R R3
U 1 1 5DFB232F
P 7230 4690
F 0 "R3" V 7140 4690 50  0000 C CNN
F 1 "47k" V 7230 4700 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7160 4690 50  0001 C CNN
F 3 "~" H 7230 4690 50  0001 C CNN
	1    7230 4690
	0    1    1    0   
$EndComp
$Comp
L Transistor_BJT:MMBT3904 Q2
U 1 1 5DFB2330
P 7400 4320
F 0 "Q2" H 7591 4366 50  0000 L CNN
F 1 "MMBT3904" H 7591 4275 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 7600 4245 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 7400 4320 50  0001 L CNN
	1    7400 4320
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5DFB2331
P 6770 4320
F 0 "R2" V 6680 4320 50  0000 C CNN
F 1 "4.7k" V 6770 4330 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 6700 4320 50  0001 C CNN
F 3 "~" H 6770 4320 50  0001 C CNN
	1    6770 4320
	0    1    1    0   
$EndComp
Wire Wire Line
	7500 4520 7500 4690
Wire Wire Line
	7080 4320 7200 4320
Wire Wire Line
	6920 4320 7080 4320
Wire Wire Line
	7500 4690 7380 4690
Wire Wire Line
	7080 4690 7080 4320
Text Label 7500 4690 0    50   ~ 0
M_GND
Text Label 7500 3790 0    50   ~ 0
M_PWR_KEY_NEW
Connection ~ 7080 4320
Wire Wire Line
	6030 4320 6620 4320
Wire Wire Line
	7500 3790 7500 3935
$Comp
L dly_customized:Test_Pin T1
U 1 1 5DFB6FE0
P 7500 3935
F 0 "T1" V 7449 4213 50  0000 L CNN
F 1 "M_PWR_KEY" V 7540 4213 50  0000 L CNN
F 2 "LTD_Customized:test_pad" H 7500 3935 50  0001 C CNN
F 3 "" H 7500 3935 50  0001 C CNN
	1    7500 3935
	0    1    1    0   
$EndComp
Connection ~ 7500 3935
Wire Wire Line
	7500 3935 7500 4120
Wire Wire Line
	1025 5400 1585 5400
Wire Wire Line
	1685 5400 2300 5400
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5DFB3220
P 1585 5200
F 0 "J4" V 1549 5012 50  0000 R CNN
F 1 "USB_DET_Conn" V 1700 5285 50  0000 R CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 1585 5200 50  0001 C CNN
F 3 "~" H 1585 5200 50  0001 C CNN
	1    1585 5200
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
