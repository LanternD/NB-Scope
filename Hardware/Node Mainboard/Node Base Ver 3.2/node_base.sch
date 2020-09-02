EESchema Schematic File Version 5
EELAYER 30 0
EELAYER END
$Descr A3 16535 11693
encoding utf-8
Sheet 1 1
Title "NB-IoT Node Base V3.0"
Date "2019-10-03"
Rev "3.0"
Comp "MSU"
Comment1 "Author: Deliang Yang"
Comment2 ""
Comment3 ""
Comment4 ""
Comment5 ""
Comment6 ""
Comment7 ""
Comment8 ""
Comment9 ""
$EndDescr
$Comp
L Device:C_Small C5
U 1 1 5D90B68B
P 1775 4825
F 0 "C5" V 1546 4825 50  0000 C CNN
F 1 "10pF" V 1637 4825 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1775 4825 50  0001 C CNN
F 3 "~" H 1775 4825 50  0001 C CNN
	1    1775 4825
	0    1    1    0   
$EndComp
$Comp
L Device:Crystal Y1
U 1 1 5D90B68C
P 2175 2775
F 0 "Y1" V 2221 2644 50  0000 R CNN
F 1 "8MHz" V 2130 2644 50  0000 R CNN
F 2 "Crystal:Crystal_SMD_5032-2Pin_5.0x3.2mm" H 2175 2775 50  0001 C CNN
F 3 "~" H 2175 2775 50  0001 C CNN
	1    2175 2775
	0    -1   -1   0   
$EndComp
$Comp
L power:VSSA #PWR0101
U 1 1 5D90B68D
P 4025 5975
F 0 "#PWR0101" H 4025 5825 50  0001 C CNN
F 1 "VSSA" H 4043 6148 50  0000 C CNN
F 2 "" H 4025 5975 50  0001 C CNN
F 3 "" H 4025 5975 50  0001 C CNN
	1    4025 5975
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5D90B68E
P 1275 4675
F 0 "#PWR0102" H 1275 4425 50  0001 C CNN
F 1 "GND" V 1280 4547 50  0000 R CNN
F 2 "" H 1275 4675 50  0001 C CNN
F 3 "" H 1275 4675 50  0001 C CNN
	1    1275 4675
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5D90B690
P 3725 5275
F 0 "#PWR0103" H 3725 5025 50  0001 C CNN
F 1 "GND" V 3730 5147 50  0000 R CNN
F 2 "" H 3725 5275 50  0001 C CNN
F 3 "" H 3725 5275 50  0001 C CNN
	1    3725 5275
	1    0    0    -1  
$EndComp
$Comp
L power:VSSA #PWR0104
U 1 1 5D90B692
P 4025 5375
F 0 "#PWR0104" H 4025 5225 50  0001 C CNN
F 1 "VSSA" H 4043 5548 50  0000 C CNN
F 2 "" H 4025 5375 50  0001 C CNN
F 3 "" H 4025 5375 50  0001 C CNN
	1    4025 5375
	-1   0    0    1   
$EndComp
$Comp
L Device:Crystal Y2
U 1 1 5D90B693
P 2175 4675
F 0 "Y2" V 2221 4544 50  0000 R CNN
F 1 "32.768kHz" V 2130 4544 50  0000 R CNN
F 2 "Crystal:Crystal_SMD_3215-2Pin_3.2x1.5mm" H 2175 4675 50  0001 C CNN
F 3 "~" H 2175 4675 50  0001 C CNN
	1    2175 4675
	0    -1   -1   0   
$EndComp
Connection ~ 3925 1075
Connection ~ 4025 1075
Connection ~ 2175 4525
Connection ~ 3625 1075
Connection ~ 3725 1075
Connection ~ 2175 4825
Connection ~ 1275 2775
Connection ~ 3825 5175
Connection ~ 1275 4675
Connection ~ 3725 5175
Connection ~ 3825 1075
Wire Wire Line
	1275 4825 1275 4675
Wire Wire Line
	1875 4825 2175 4825
Wire Wire Line
	2725 4525 2175 4525
Wire Wire Line
	3575 5925 3425 5925
Wire Wire Line
	3725 5175 3825 5175
Wire Wire Line
	1675 2625 1275 2625
Wire Wire Line
	3125 4625 2725 4625
Wire Wire Line
	4525 2825 4775 2825
Wire Wire Line
	3625 4925 3625 5175
Wire Wire Line
	2725 4825 2725 4725
Wire Wire Line
	1275 2625 1275 2775
Wire Wire Line
	1675 2925 1275 2925
Wire Wire Line
	3725 4925 3725 5175
Wire Wire Line
	1275 2925 1275 2775
Wire Wire Line
	2725 4725 3125 4725
Wire Wire Line
	1875 4525 2175 4525
Wire Wire Line
	2725 4625 2725 4525
Wire Wire Line
	4775 3525 4525 3525
Wire Wire Line
	2175 4825 2725 4825
Wire Wire Line
	3125 2825 2725 2825
Wire Wire Line
	3825 4925 3825 5175
Wire Wire Line
	3825 5175 3925 5175
Wire Wire Line
	4775 2925 4525 2925
Wire Wire Line
	3925 5175 3925 4925
Wire Wire Line
	3725 5275 3725 5175
Wire Wire Line
	3625 5175 3725 5175
Wire Wire Line
	4025 4925 4025 5375
Wire Wire Line
	3425 5925 3425 5975
Wire Wire Line
	1675 4525 1275 4525
Wire Wire Line
	1275 4525 1275 4675
Wire Wire Line
	1675 4825 1275 4825
Text Label 4775 3525 0    50   ~ 0
SWO
Text Label 4775 2825 0    50   ~ 0
SWD_IO
Text Label 4775 2925 0    50   ~ 0
SWD_CLK
Text Label 2825 1525 0    50   ~ 0
nRESET
$Comp
L power:+3.3V #PWR0105
U 1 1 5D90B694
P 3625 925
F 0 "#PWR0105" H 3625 775 50  0001 C CNN
F 1 "+3.3V" H 3640 1098 50  0000 C CNN
F 2 "" H 3625 925 50  0001 C CNN
F 3 "" H 3625 925 50  0001 C CNN
	1    3625 925 
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5D90B695
P 3425 5975
F 0 "#PWR0106" H 3425 5725 50  0001 C CNN
F 1 "GND" V 3430 5847 50  0000 R CNN
F 2 "" H 3425 5975 50  0001 C CNN
F 3 "" H 3425 5975 50  0001 C CNN
	1    3425 5975
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C2
U 1 1 5D90B696
P 1775 2625
F 0 "C2" V 1546 2625 50  0000 C CNN
F 1 "10pF" V 1637 2625 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1775 2625 50  0001 C CNN
F 3 "~" H 1775 2625 50  0001 C CNN
	1    1775 2625
	0    1    1    0   
$EndComp
$Comp
L Device:C_Small C3
U 1 1 5D90B697
P 1775 2925
F 0 "C3" V 1546 2925 50  0000 C CNN
F 1 "10pF" V 1637 2925 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1775 2925 50  0001 C CNN
F 3 "~" H 1775 2925 50  0001 C CNN
	1    1775 2925
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0107
U 1 1 5D90B698
P 1275 2775
F 0 "#PWR0107" H 1275 2525 50  0001 C CNN
F 1 "GND" V 1280 2647 50  0000 R CNN
F 2 "" H 1275 2775 50  0001 C CNN
F 3 "" H 1275 2775 50  0001 C CNN
	1    1275 2775
	0    1    1    0   
$EndComp
Wire Wire Line
	3625 925  3625 1075
Wire Wire Line
	2575 4225 3125 4225
Wire Wire Line
	4775 2625 4525 2625
Wire Wire Line
	3725 1075 3625 1075
Wire Wire Line
	3925 1325 3925 1075
Wire Wire Line
	3825 1075 3725 1075
Wire Wire Line
	4125 1325 4125 1075
Wire Wire Line
	4525 2225 4775 2225
Wire Wire Line
	3725 1325 3725 1075
Wire Wire Line
	3625 1075 3625 1325
Wire Wire Line
	4025 1325 4025 1075
Wire Wire Line
	4125 1075 4025 1075
Wire Wire Line
	4025 1075 3925 1075
Wire Wire Line
	2575 3625 3125 3625
Wire Wire Line
	4775 1925 4525 1925
Wire Wire Line
	4525 2025 4775 2025
Wire Wire Line
	3825 1325 3825 1075
Wire Wire Line
	3125 4325 2575 4325
Wire Wire Line
	4525 3025 4775 3025
Wire Wire Line
	2575 3025 3125 3025
Wire Wire Line
	3125 3225 2575 3225
Wire Wire Line
	4525 2725 4775 2725
Wire Wire Line
	4525 3325 4775 3325
Wire Wire Line
	4775 3225 4525 3225
Wire Wire Line
	2725 2825 2725 2625
Wire Wire Line
	2575 4425 3125 4425
Wire Wire Line
	4775 2125 4525 2125
Wire Wire Line
	3125 3725 2575 3725
Wire Wire Line
	2575 3325 3125 3325
Wire Wire Line
	3925 1075 3825 1075
Text Label 4775 1825 0    50   ~ 0
USART2_Rx
$Comp
L Device:R R2
U 1 1 5D90B699
P 1975 5975
F 0 "R2" H 2045 6021 50  0000 L CNN
F 1 "470k" H 2045 5930 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1905 5975 50  0001 C CNN
F 3 "~" H 1975 5975 50  0001 C CNN
	1    1975 5975
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 5D90B69A
P 1975 5575
F 0 "R1" H 2045 5621 50  0000 L CNN
F 1 "220k" H 2045 5530 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 1905 5575 50  0001 C CNN
F 3 "~" H 1975 5575 50  0001 C CNN
	1    1975 5575
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0109
U 1 1 5D90B69D
P 5075 3425
F 0 "#PWR0109" H 5075 3175 50  0001 C CNN
F 1 "GND" V 5080 3297 50  0000 R CNN
F 2 "" H 5075 3425 50  0001 C CNN
F 3 "" H 5075 3425 50  0001 C CNN
	1    5075 3425
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0110
U 1 1 5D90B6A0
P 1975 6225
F 0 "#PWR0110" H 1975 5975 50  0001 C CNN
F 1 "GND" H 2175 6175 50  0000 R CNN
F 2 "" H 1975 6225 50  0001 C CNN
F 3 "" H 1975 6225 50  0001 C CNN
	1    1975 6225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0111
U 1 1 5D90B6A2
P 1375 1825
F 0 "#PWR0111" H 1375 1575 50  0001 C CNN
F 1 "GND" V 1380 1697 50  0000 R CNN
F 2 "" H 1375 1825 50  0001 C CNN
F 3 "" H 1375 1825 50  0001 C CNN
	1    1375 1825
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0112
U 1 1 5D90B6A3
P 2225 2025
F 0 "#PWR0112" H 2225 1775 50  0001 C CNN
F 1 "GND" V 2230 1897 50  0000 R CNN
F 2 "" H 2225 2025 50  0001 C CNN
F 3 "" H 2225 2025 50  0001 C CNN
	1    2225 2025
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C1
U 1 1 5D90B6A5
P 1775 1775
F 0 "C1" V 1875 1875 50  0000 C CNN
F 1 "10nF" V 1637 1775 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1775 1775 50  0001 C CNN
F 3 "~" H 1775 1775 50  0001 C CNN
	1    1775 1775
	0    1    1    0   
$EndComp
Connection ~ 2175 1525
Connection ~ 1375 1775
Connection ~ 1975 5775
Wire Notes Line
	6150 675  875  675 
Wire Notes Line
	6150 6425 6150 675 
Wire Wire Line
	1975 5775 1975 5825
Wire Wire Line
	1375 1525 1375 1775
Wire Wire Line
	1975 1525 2175 1525
Wire Wire Line
	1675 1775 1375 1775
Wire Wire Line
	4775 1625 4525 1625
Wire Wire Line
	1375 1775 1375 1825
Wire Notes Line
	875  675  875  6425
Wire Wire Line
	1975 5425 1975 5325
Wire Wire Line
	1575 1525 1375 1525
Wire Wire Line
	2575 3425 3125 3425
Wire Wire Line
	4525 1525 4775 1525
Wire Notes Line
	875  6425 6150 6425
Wire Wire Line
	2175 1775 2175 1525
Wire Wire Line
	1975 6225 1975 6125
Wire Wire Line
	1875 1775 2175 1775
Wire Wire Line
	4525 3425 5075 3425
Wire Wire Line
	1975 5725 1975 5775
Wire Wire Line
	1975 5775 2225 5775
Text Label 2225 5775 0    50   ~ 0
VBAT_ADC
Text Notes 1975 2500 0    50   ~ 0
Note: Default pull the pin to 0.\nConnect the test point to 3.3V\n if you want to change it.
Text Label 4775 3425 0    50   ~ 0
BOOT1
Text Notes 975  875  0    50   ~ 0
MCU Module (STM32F103RETx)
Wire Wire Line
	2575 4125 3125 4125
Wire Wire Line
	4775 3625 4525 3625
Wire Wire Line
	2575 3825 3125 3825
Wire Wire Line
	4525 4025 4775 4025
Wire Wire Line
	4525 2325 4775 2325
Wire Wire Line
	2575 3925 3125 3925
Wire Wire Line
	2575 4025 3125 4025
Wire Wire Line
	4525 4425 4775 4425
Wire Wire Line
	3125 3525 2575 3525
Wire Wire Line
	4775 4125 4525 4125
Wire Wire Line
	2775 4525 3125 4525
Text Label 1975 5325 0    50   ~ 0
V_BATT
Wire Wire Line
	1875 2625 2175 2625
NoConn ~ 2375 6900
$Comp
L Connector:SIM_Card J1
U 1 1 5D91F075
P 1875 7000
F 0 "J1" H 2505 7100 50  0000 L CNN
F 1 "SIM_Card" H 2505 7009 50  0000 L CNN
F 2 "LTD_Customized:Nano Sim Socket 1.1H, 6P" H 1875 7350 50  0001 C CNN
F 3 " ~" H 1825 7000 50  0001 C CNN
	1    1875 7000
	-1   0    0    1   
$EndComp
Wire Wire Line
	2375 7200 2725 7200
Wire Wire Line
	2725 7350 2725 7200
$Comp
L Device:C_Small C11
U 1 1 5D920C1C
P 14625 2425
F 0 "C11" H 14717 2471 50  0000 L CNN
F 1 "100nF" H 14717 2380 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 14625 2425 50  0001 C CNN
F 3 "~" H 14625 2425 50  0001 C CNN
	1    14625 2425
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C10
U 1 1 5D920C20
P 14275 2425
F 0 "C10" H 14367 2471 50  0000 L CNN
F 1 "100nF" H 14367 2380 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 14275 2425 50  0001 C CNN
F 3 "~" H 14275 2425 50  0001 C CNN
	1    14275 2425
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0115
U 1 1 5D920C21
P 14775 2175
F 0 "#PWR0115" H 14775 2025 50  0001 C CNN
F 1 "+3.3V" H 14790 2348 50  0000 C CNN
F 2 "" H 14775 2175 50  0001 C CNN
F 3 "" H 14775 2175 50  0001 C CNN
	1    14775 2175
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C12
U 1 1 5D920C22
P 14975 2425
F 0 "C12" H 15067 2471 50  0000 L CNN
F 1 "100nF" H 15067 2380 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 14975 2425 50  0001 C CNN
F 3 "~" H 14975 2425 50  0001 C CNN
	1    14975 2425
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C13
U 1 1 5D920C23
P 15325 2425
F 0 "C13" H 15417 2471 50  0000 L CNN
F 1 "100nF" H 15417 2380 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 15325 2425 50  0001 C CNN
F 3 "~" H 15325 2425 50  0001 C CNN
	1    15325 2425
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0117
U 1 1 5D920C25
P 14775 2675
F 0 "#PWR0117" H 14775 2425 50  0001 C CNN
F 1 "GND" H 14780 2547 50  0000 R CNN
F 2 "" H 14775 2675 50  0001 C CNN
F 3 "" H 14775 2675 50  0001 C CNN
	1    14775 2675
	1    0    0    -1  
$EndComp
Wire Wire Line
	14275 2225 14625 2225
Wire Wire Line
	14975 2225 15325 2225
Wire Wire Line
	14775 2175 14775 2225
Wire Wire Line
	14775 2225 14975 2225
Wire Wire Line
	14975 2325 14975 2225
Wire Wire Line
	14275 2325 14275 2225
Wire Wire Line
	14625 2325 14625 2225
Wire Wire Line
	14275 2575 14625 2575
Wire Wire Line
	14625 2225 14775 2225
Wire Wire Line
	14275 2525 14275 2575
Wire Wire Line
	15325 2575 15325 2525
Wire Wire Line
	15325 2225 15325 2325
Connection ~ 14775 2575
Connection ~ 14975 2575
Connection ~ 14975 2225
Connection ~ 14775 2225
Connection ~ 14625 2575
Connection ~ 14625 2225
Wire Wire Line
	14775 2675 14775 2575
Wire Wire Line
	14775 2575 14975 2575
Wire Wire Line
	14975 2575 15325 2575
Wire Wire Line
	14975 2525 14975 2575
Wire Wire Line
	14625 2525 14625 2575
Wire Wire Line
	14625 2575 14775 2575
$Comp
L Device:L L1
U 1 1 5D920C26
P 13325 1550
F 0 "L1" V 13515 1550 50  0000 C CNN
F 1 "2.2uH" V 13424 1550 50  0000 C CNN
F 2 "LTD_Customized:L_Sumida_CDRH2D14_3.2x3.2x1.55mm" H 13325 1550 50  0001 C CNN
F 3 "~" H 13325 1550 50  0001 C CNN
	1    13325 1550
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0118
U 1 1 5D920C27
P 12875 1950
F 0 "#PWR0118" H 12875 1700 50  0001 C CNN
F 1 "GND" H 12880 1822 50  0000 R CNN
F 2 "" H 12875 1950 50  0001 C CNN
F 3 "" H 12875 1950 50  0001 C CNN
	1    12875 1950
	1    0    0    -1  
$EndComp
$Comp
L Regulator_Switching:LM3670MF U4
U 1 1 5D920C28
P 12875 1650
F 0 "U4" H 12875 1975 50  0000 C CNN
F 1 "LM3671MF-3.3" H 12875 1884 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:TSOT-23-5" H 12925 1400 50  0001 L CNN
F 3 "http://www.ti.com/lit/ds/symlink/lm3670.pdf" H 12625 1300 50  0001 C CNN
	1    12875 1650
	1    0    0    -1  
$EndComp
Connection ~ 12475 1550
Connection ~ 12875 1950
Connection ~ 12325 1550
Connection ~ 13750 1550
Wire Notes Line
	10200 2975 15800 2975
Wire Wire Line
	12225 1500 12225 1550
Wire Wire Line
	12575 1650 12475 1650
Wire Notes Line
	15800 675  10200 675 
Wire Notes Line
	15800 2975 15800 675 
Wire Wire Line
	12225 1550 12325 1550
Text Notes 10250 825  0    50   ~ 0
Power Connector for the circuit board
Wire Wire Line
	12475 1650 12475 1550
Wire Wire Line
	12325 1900 12325 1950
Wire Wire Line
	13750 1600 13750 1550
Wire Wire Line
	12325 1950 12875 1950
Wire Wire Line
	12325 1550 12475 1550
Wire Notes Line
	10200 675  10200 2975
Wire Wire Line
	13750 1850 13750 1800
Wire Wire Line
	12325 1700 12325 1550
Wire Wire Line
	12475 1550 12575 1550
Wire Wire Line
	13475 1550 13600 1550
$Comp
L power:GND #PWR0120
U 1 1 5D920C2F
P 13750 1850
F 0 "#PWR0120" H 13750 1600 50  0001 C CNN
F 1 "GND" H 13700 1700 50  0000 R CNN
F 2 "" H 13750 1850 50  0001 C CNN
F 3 "" H 13750 1850 50  0001 C CNN
	1    13750 1850
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C8
U 1 1 5D920C30
P 12325 1800
F 0 "C8" H 12417 1846 50  0000 L CNN
F 1 "4.7uF" H 12417 1755 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 12325 1800 50  0001 C CNN
F 3 "~" H 12325 1800 50  0001 C CNN
	1    12325 1800
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C9
U 1 1 5D920C31
P 13750 1700
F 0 "C9" H 13842 1746 50  0000 L CNN
F 1 "10uF" H 13850 1650 50  0000 L CNN
F 2 "Capacitor_SMD:C_0805_2012Metric" H 13750 1700 50  0001 C CNN
F 3 "~" H 13750 1700 50  0001 C CNN
	1    13750 1700
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0121
U 1 1 5D920C34
P 15525 1300
F 0 "#PWR0121" H 15525 1150 50  0001 C CNN
F 1 "+5V" H 15540 1473 50  0000 C CNN
F 2 "" H 15525 1300 50  0001 C CNN
F 3 "" H 15525 1300 50  0001 C CNN
	1    15525 1300
	1    0    0    -1  
$EndComp
Text Label 15175 1500 0    50   ~ 0
V_BATT
Text Label 12225 1500 0    50   ~ 0
V_IN
Text Label 15275 1400 0    50   ~ 0
V_IN
Wire Wire Line
	15275 1200 15275 1400
Wire Wire Line
	15525 1300 15375 1300
Wire Wire Line
	15375 1300 15375 1200
Text Notes 10450 2875 0    50   ~ 0
Note:\n1. V_in should be manually chosen between Li-on Battery and +5V USB\n2. The BC28 is powered by 3.3V\n3. The External_Power connector should be carefully secured to prevent short circuit
$Comp
L power:GND #PWR0122
U 1 1 5D92F8DF
P 7700 2175
F 0 "#PWR0122" H 7700 1925 50  0001 C CNN
F 1 "GND" V 7705 2047 50  0000 R CNN
F 2 "" H 7700 2175 50  0001 C CNN
F 3 "" H 7700 2175 50  0001 C CNN
	1    7700 2175
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J6
U 1 1 5D92F8E0
P 8650 1625
F 0 "J6" H 8730 1617 50  0000 L CNN
F 1 "SWD_Conn" H 8475 1300 50  0000 L CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x04_P1.27mm_Vertical" H 8650 1625 50  0001 C CNN
F 3 "~" H 8650 1625 50  0001 C CNN
	1    8650 1625
	1    0    0    -1  
$EndComp
Text Label 7850 1525 0    50   ~ 0
VCC_TARGET
Text Label 7850 1625 0    50   ~ 0
SWD_CLK
Connection ~ 7700 1725
Connection ~ 7250 1075
Wire Wire Line
	7700 1725 8450 1725
Text Notes 7350 1475 0    50   ~ 0
Pull-down
Text Notes 6650 1175 0    50   ~ 0
Pull-up
Text Label 7850 1825 0    50   ~ 0
SWD_IO
Text Label 7850 2025 0    50   ~ 0
SWO
$Comp
L power:+3.3V #PWR0123
U 1 1 5D92F8E1
P 7250 1025
F 0 "#PWR0123" H 7250 875 50  0001 C CNN
F 1 "+3.3V" H 7265 1198 50  0000 C CNN
F 2 "" H 7250 1025 50  0001 C CNN
F 3 "" H 7250 1025 50  0001 C CNN
	1    7250 1025
	1    0    0    -1  
$EndComp
$Comp
L Device:R R7
U 1 1 5D92F8E2
P 7250 1325
F 0 "R7" V 7150 1325 50  0000 C CNN
F 1 "10k" V 7250 1325 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7180 1325 50  0001 C CNN
F 3 "~" H 7250 1325 50  0001 C CNN
	1    7250 1325
	1    0    0    -1  
$EndComp
$Comp
L Device:R R8
U 1 1 5D92F8E4
P 7550 1625
F 0 "R8" V 7450 1625 50  0000 C CNN
F 1 "10k" V 7550 1625 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 7480 1625 50  0001 C CNN
F 3 "~" H 7550 1625 50  0001 C CNN
	1    7550 1625
	0    1    1    0   
$EndComp
Wire Wire Line
	7700 1725 7700 2175
Wire Wire Line
	7250 1825 8450 1825
Wire Wire Line
	7250 1175 7250 1075
Wire Wire Line
	7250 1075 7650 1075
Wire Wire Line
	7700 1625 8450 1625
Wire Wire Line
	7650 1525 8450 1525
Wire Wire Line
	7400 1725 7700 1725
Wire Wire Line
	7650 1525 7650 1075
Wire Wire Line
	7400 1625 7400 1725
Wire Wire Line
	7250 1825 7250 1475
Wire Wire Line
	7250 1025 7250 1075
Wire Notes Line
	6550 775  9000 775 
Wire Notes Line
	6550 775  6550 2525
Wire Notes Line
	6550 2525 9000 2525
Wire Notes Line
	9000 775  9000 2525
Text Notes 8100 925  0    50   ~ 0
MCU SWD Connector
Wire Wire Line
	7825 4550 7975 4550
Wire Notes Line
	6475 5400 8525 5400
Wire Wire Line
	7425 5050 7425 4975
Wire Notes Line
	8525 4100 6475 4100
Wire Notes Line
	6475 4100 6475 5400
Wire Wire Line
	7975 4750 7825 4750
Wire Wire Line
	7975 4650 7825 4650
Wire Notes Line
	8525 5400 8525 4100
$Comp
L power:GND #PWR0124
U 1 1 5D934DA9
P 7425 5050
F 0 "#PWR0124" H 7425 4800 50  0001 C CNN
F 1 "GND" H 7675 5050 50  0000 R CNN
F 2 "" H 7425 5050 50  0001 C CNN
F 3 "" H 7425 5050 50  0001 C CNN
	1    7425 5050
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0125
U 1 1 5D934DAA
P 7425 4275
F 0 "#PWR0125" H 7425 4125 50  0001 C CNN
F 1 "+3.3V" H 7250 4350 50  0000 C CNN
F 2 "" H 7425 4275 50  0001 C CNN
F 3 "" H 7425 4275 50  0001 C CNN
	1    7425 4275
	1    0    0    -1  
$EndComp
$Comp
L Memory_EEPROM:CAT24C256 U3
U 1 1 5D934DAB
P 7425 4650
F 0 "U3" H 7075 5000 50  0000 C CNN
F 1 "CAT24C128" H 7125 4900 50  0000 C CNN
F 2 "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" H 7425 4650 50  0001 C CNN
F 3 "https://www.onsemi.com/pub/Collateral/CAT24C128-D.PDF" H 7425 4650 50  0001 C CNN
	1    7425 4650
	1    0    0    -1  
$EndComp
Text Label 7975 4550 0    50   ~ 0
I2C2_SDA
Text Label 7975 4650 0    50   ~ 0
I2C2_SCL
Text Notes 7925 4250 0    50   ~ 0
EEPROM 128kb
Wire Notes Line
	13125 4050 13125 6050
Wire Notes Line
	13125 6050 8800 6050
Wire Notes Line
	8800 6050 8800 4050
$Comp
L power:GND #PWR0131
U 1 1 5D93D267
P 11150 4875
F 0 "#PWR0131" H 11150 4625 50  0001 C CNN
F 1 "GND" H 11155 4747 50  0000 R CNN
F 2 "" H 11150 4875 50  0001 C CNN
F 3 "" H 11150 4875 50  0001 C CNN
	1    11150 4875
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0132
U 1 1 5D93D268
P 11150 4650
F 0 "#PWR0132" H 11150 4400 50  0001 C CNN
F 1 "GND" H 11155 4522 50  0000 R CNN
F 2 "" H 11150 4650 50  0001 C CNN
F 3 "" H 11150 4650 50  0001 C CNN
	1    11150 4650
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED D4
U 1 1 5D93D26C
P 11000 4875
F 0 "D4" V 11039 4758 50  0000 R CNN
F 1 "LED" V 10948 4758 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 11000 4875 50  0001 C CNN
F 3 "~" H 11000 4875 50  0001 C CNN
	1    11000 4875
	-1   0    0    1   
$EndComp
$Comp
L Device:LED D2
U 1 1 5D93D270
P 11000 4425
F 0 "D2" V 11039 4308 50  0000 R CNN
F 1 "LED" V 10948 4308 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 11000 4425 50  0001 C CNN
F 3 "~" H 11000 4425 50  0001 C CNN
	1    11000 4425
	-1   0    0    1   
$EndComp
Text Notes 8850 5925 0    50   ~ 0
Note: the LEDs should be in different colors
Text Notes 9425 4200 0    50   ~ 0
LED Indicator
Text Notes 10125 4250 0    50   ~ 0
Note: if you don’t want the power indicator, \ndon’t solder it the LED and the resistor.
$Comp
L Device:R R5
U 1 1 5D953B7C
P 3725 5925
F 0 "R5" V 3625 5825 50  0000 C CNN
F 1 "0" V 3725 5925 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 3655 5925 50  0001 C CNN
F 3 "~" H 3725 5925 50  0001 C CNN
	1    3725 5925
	0    1    1    0   
$EndComp
Wire Wire Line
	3875 5925 4025 5925
Wire Wire Line
	4025 5925 4025 5975
Wire Wire Line
	2375 7000 3100 7000
Wire Wire Line
	2725 7200 3100 7200
Connection ~ 2725 7200
Wire Wire Line
	2375 7300 2925 7300
Connection ~ 2925 7300
Wire Wire Line
	2925 7300 3025 7300
Text Label 3100 6800 0    50   ~ 0
SIM_IO
Text Label 3100 7000 0    50   ~ 0
SIM_GND
Text Label 3100 7100 0    50   ~ 0
SIM_CLK
Text Label 3100 7200 0    50   ~ 0
SIM_RST
Text Label 3100 7300 0    50   ~ 0
SIM_VCC
Wire Wire Line
	1875 2925 2175 2925
$Comp
L Analog_ADC:INA226 U5
U 1 1 5D9CB0E7
P 2525 9675
F 0 "U5" H 2525 10356 50  0000 C CNN
F 1 "INA226" H 2525 10265 50  0000 C CNN
F 2 "Package_SO:VSSOP-10_3x3mm_P0.5mm" H 3325 9225 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/ina226.pdf" H 2875 9575 50  0001 C CNN
	1    2525 9675
	1    0    0    -1  
$EndComp
Text Label 12900 6800 0    50   ~ 0
M_VCC
Text Label 12900 6900 0    50   ~ 0
M_VCC
Text Label 12900 7000 0    50   ~ 0
GPIO_L1
Text Label 12900 7100 0    50   ~ 0
PSM_IND
Text Label 12900 7200 0    50   ~ 0
M_SPI_MISO-I2S_RXD
Text Label 12900 7300 0    50   ~ 0
M_SPI_MOSI-I2S_WA
Text Label 12900 7400 0    50   ~ 0
M_SPI_CLK-I2S_CLK
Text Label 12900 7500 0    50   ~ 0
M_SPI_CS-I2S_CS
Text Label 12900 7600 0    50   ~ 0
GPIO_L2
Text Label 12900 7700 0    50   ~ 0
M_USB_VBUS
Text Label 12900 7800 0    50   ~ 0
M_USB_DP
Text Label 12900 7900 0    50   ~ 0
M_USB_DM
Text Label 12900 8000 0    50   ~ 0
M_ADC
Text Label 12900 8100 0    50   ~ 0
M_MAIN_UART_Tx
Text Label 12900 8200 0    50   ~ 0
M_MAIN_UART_Rx
Text Label 12900 8300 0    50   ~ 0
M_PWRKEY
Text Label 12900 8400 0    50   ~ 0
M_RESET
Text Label 12900 8500 0    50   ~ 0
PSM_EINT
Text Label 12900 8700 0    50   ~ 0
M_AP_READY
$Comp
L Connector_Generic:Conn_01x22 J12
U 1 1 5D9CD5C5
P 14000 7800
F 0 "J12" H 13830 9042 50  0000 L CNN
F 1 "Left_Conn" H 13830 8951 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x22_P1.27mm_Vertical" H 14000 7800 50  0001 C CNN
F 3 "~" H 14000 7800 50  0001 C CNN
	1    14000 7800
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x22 J13
U 1 1 5D9CE193
P 15525 7800
F 0 "J13" H 15443 9017 50  0000 C CNN
F 1 "Right_Conn" H 15443 8926 50  0000 C CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x22_P1.27mm_Vertical" H 15525 7800 50  0001 C CNN
F 3 "~" H 15525 7800 50  0001 C CNN
	1    15525 7800
	1    0    0    -1  
$EndComp
Text Label 12900 8800 0    50   ~ 0
GPIO_L3
Text Label 12900 8900 0    50   ~ 0
GPIO_L4
Text Label 14625 6800 0    50   ~ 0
M_VCC
Text Label 14625 7600 0    50   ~ 0
M_SDA
Text Label 14625 7700 0    50   ~ 0
M_SCL
Text Label 14625 7800 0    50   ~ 0
M_DBG_UART_TX
Text Label 14625 7900 0    50   ~ 0
M_DBG_UART_Rx
Text Label 14625 8100 0    50   ~ 0
M_AUX_UART_Rx
Text Label 14625 8200 0    50   ~ 0
M_NET_LED
Text Label 14625 8300 0    50   ~ 0
M_RI
Text Label 14625 8400 0    50   ~ 0
GPIO_R2
Text Label 14625 8500 0    50   ~ 0
GPIO_R3
Text Label 14625 8700 0    50   ~ 0
M_GND
Text Label 14625 8800 0    50   ~ 0
M_GND
Text Label 14625 8900 0    50   ~ 0
M_GND
Wire Wire Line
	12900 6800 13300 6800
Wire Wire Line
	13800 6900 12900 6900
Wire Wire Line
	12900 7000 13800 7000
Wire Wire Line
	13800 7100 12900 7100
Wire Wire Line
	12900 7200 13800 7200
Wire Wire Line
	13800 7300 12900 7300
Wire Wire Line
	12900 7400 13800 7400
Wire Wire Line
	13800 7500 12900 7500
Wire Wire Line
	12900 7600 13800 7600
Wire Wire Line
	13800 7700 12900 7700
Wire Wire Line
	12900 7800 13800 7800
Wire Wire Line
	13800 7900 12900 7900
Wire Wire Line
	13800 8100 12900 8100
Wire Wire Line
	12900 8200 13800 8200
Wire Wire Line
	13800 8300 12900 8300
Wire Wire Line
	12900 8400 13800 8400
Wire Wire Line
	13800 8500 12900 8500
Wire Wire Line
	12900 8600 13800 8600
Wire Wire Line
	13800 8700 12900 8700
Wire Wire Line
	12900 8800 13800 8800
Wire Wire Line
	13800 8900 12900 8900
Wire Wire Line
	14625 6800 15325 6800
Wire Wire Line
	15325 6900 14625 6900
Wire Wire Line
	14625 7000 15325 7000
Wire Wire Line
	15325 7100 14625 7100
Wire Wire Line
	14625 7200 15325 7200
Wire Wire Line
	15325 7300 14625 7300
Wire Wire Line
	14625 7400 15325 7400
Wire Wire Line
	15325 7500 14625 7500
Wire Wire Line
	14625 7800 15325 7800
Wire Wire Line
	15325 7900 14625 7900
Wire Wire Line
	15325 8000 14625 8000
Wire Wire Line
	14625 8100 15325 8100
Wire Wire Line
	15325 8200 14625 8200
Wire Wire Line
	14625 8300 15325 8300
Wire Wire Line
	15325 8400 14625 8400
Wire Wire Line
	14625 8500 15325 8500
Wire Wire Line
	15325 8600 14625 8600
Wire Wire Line
	14625 8700 15325 8700
Wire Wire Line
	15325 8800 14625 8800
Wire Wire Line
	14625 8900 15325 8900
$Comp
L power:GND #PWR0138
U 1 1 5DB4DD25
P 1525 10075
F 0 "#PWR0138" H 1525 9825 50  0001 C CNN
F 1 "GND" V 1530 9947 50  0000 R CNN
F 2 "" H 1525 10075 50  0001 C CNN
F 3 "" H 1525 10075 50  0001 C CNN
	1    1525 10075
	1    0    0    -1  
$EndComp
Text Label 1525 9475 0    50   ~ 0
M_GND
Wire Wire Line
	1525 9625 1525 9575
Wire Wire Line
	1525 9925 1525 9975
Wire Wire Line
	2125 9875 1975 9875
Wire Wire Line
	1975 9875 1975 9975
Wire Wire Line
	1975 9975 1525 9975
Connection ~ 1525 9975
Wire Wire Line
	1525 9975 1525 10075
Wire Wire Line
	2125 9775 1975 9775
Wire Wire Line
	1975 9775 1975 9575
Wire Wire Line
	1975 9575 1525 9575
Connection ~ 1525 9575
Wire Wire Line
	1525 9575 1525 9475
$Comp
L power:GND #PWR0139
U 1 1 5DB6CDFD
P 3525 9525
F 0 "#PWR0139" H 3525 9275 50  0001 C CNN
F 1 "GND" H 3725 9525 50  0000 R CNN
F 2 "" H 3525 9525 50  0001 C CNN
F 3 "" H 3525 9525 50  0001 C CNN
	1    3525 9525
	1    0    0    -1  
$EndComp
Wire Wire Line
	3525 9525 3525 9475
Connection ~ 3525 9475
Wire Wire Line
	3525 9475 3525 9375
$Comp
L power:GND #PWR0140
U 1 1 5DB6E9A1
P 2525 10325
F 0 "#PWR0140" H 2525 10075 50  0001 C CNN
F 1 "GND" V 2530 10197 50  0000 R CNN
F 2 "" H 2525 10325 50  0001 C CNN
F 3 "" H 2525 10325 50  0001 C CNN
	1    2525 10325
	1    0    0    -1  
$EndComp
Wire Wire Line
	2525 10325 2525 10175
$Comp
L power:+3.3V #PWR0141
U 1 1 5DB76D73
P 2125 9075
F 0 "#PWR0141" H 2125 8925 50  0001 C CNN
F 1 "+3.3V" H 2140 9248 50  0000 C CNN
F 2 "" H 2125 9075 50  0001 C CNN
F 3 "" H 2125 9075 50  0001 C CNN
	1    2125 9075
	1    0    0    -1  
$EndComp
Wire Wire Line
	2125 9075 2125 9125
Wire Wire Line
	2125 9125 2525 9125
Wire Wire Line
	2525 9125 2525 9175
Wire Wire Line
	2125 9375 2125 9125
Connection ~ 2125 9125
Text Label 3025 9675 0    50   ~ 0
Current_SDA
Text Label 3025 9775 0    50   ~ 0
Current_SCL
Wire Wire Line
	3025 9775 2925 9775
Wire Wire Line
	2925 9675 3025 9675
NoConn ~ 2925 9975
$Comp
L power:+3.3V #PWR0142
U 1 1 5DB93D9A
P 14775 4450
F 0 "#PWR0142" H 14775 4300 50  0001 C CNN
F 1 "+3.3V" H 14790 4623 50  0000 C CNN
F 2 "" H 14775 4450 50  0001 C CNN
F 3 "" H 14775 4450 50  0001 C CNN
	1    14775 4450
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0143
U 1 1 5DB98635
P 14675 5375
F 0 "#PWR0143" H 14675 5125 50  0001 C CNN
F 1 "GND" H 14680 5247 50  0000 R CNN
F 2 "" H 14675 5375 50  0001 C CNN
F 3 "" H 14675 5375 50  0001 C CNN
	1    14675 5375
	1    0    0    -1  
$EndComp
Wire Wire Line
	14675 5125 14675 5275
Wire Wire Line
	14775 4525 14775 4450
Text Label 13675 4725 0    50   ~ 0
Sensor_SDA
Text Label 13675 4925 0    50   ~ 0
Sensor_SCL
Wire Wire Line
	13675 4925 14275 4925
Wire Wire Line
	14275 4725 13675 4725
$Comp
L Sensor_Humidity:Si7021-A20 U6
U 1 1 5DBA6CE9
P 14775 4825
F 0 "U6" H 15219 4871 50  0000 L CNN
F 1 "Si7021-A20" H 15219 4780 50  0000 L CNN
F 2 "Package_DFN_QFN:DFN-6-1EP_3x3mm_P1mm_EP1.5x2.4mm" H 14775 4425 50  0001 C CNN
F 3 "https://www.silabs.com/documents/public/data-sheets/Si7021-A20.pdf" H 14575 5125 50  0001 C CNN
	1    14775 4825
	1    0    0    -1  
$EndComp
Text Notes 13675 5775 0    50   ~ 0
Note: the T&H sensor shares the I2C bus with EEPROM
Text Notes 12575 6350 0    50   ~ 0
Connectors to the module board
Text Notes 1275 9025 0    50   ~ 0
Current Sensor
Text Label 13775 5175 0    50   ~ 0
Sensor_SDA
Text Label 13775 5275 0    50   ~ 0
I2C2_SDA
Text Label 13775 5525 0    50   ~ 0
I2C2_SCL
Text Label 13775 5425 0    50   ~ 0
Sensor_SCL
Wire Wire Line
	13775 5175 13675 5175
Wire Wire Line
	13675 5175 13675 5275
Wire Wire Line
	13675 5275 13775 5275
Wire Wire Line
	13775 5425 13675 5425
Wire Wire Line
	13675 5425 13675 5525
Wire Wire Line
	13675 5525 13775 5525
Text Label 11450 1375 0    50   ~ 0
V_BATT
$Comp
L power:GND #PWR0114
U 1 1 5D94D379
P 11475 1925
F 0 "#PWR0114" H 11475 1675 50  0001 C CNN
F 1 "GND" H 11650 1775 50  0000 R CNN
F 2 "" H 11475 1925 50  0001 C CNN
F 3 "" H 11475 1925 50  0001 C CNN
	1    11475 1925
	1    0    0    -1  
$EndComp
Wire Wire Line
	11475 1925 11350 1925
Wire Wire Line
	11450 1375 11350 1375
$Comp
L MCU_ST_STM32F1:STM32F103RETx U2
U 1 1 5D99D8E2
P 3825 3125
F 0 "U2" H 3825 1236 50  0000 C CNN
F 1 "STM32F103RETx" H 3825 1145 50  0000 C CNN
F 2 "Package_QFP:LQFP-64_10x10mm_P0.5mm" H 3225 1425 50  0001 R CNN
F 3 "http://www.st.com/st-web-ui/static/active/en/resource/technical/document/datasheet/CD00191185.pdf" H 3825 3125 50  0001 C CNN
	1    3825 3125
	1    0    0    -1  
$EndComp
Wire Wire Line
	2175 1525 3125 1525
$Comp
L power:VSSA #PWR0116
U 1 1 5D9E621A
P 4750 5950
F 0 "#PWR0116" H 4750 5800 50  0001 C CNN
F 1 "VSSA" H 4768 6123 50  0000 C CNN
F 2 "" H 4750 5950 50  0001 C CNN
F 3 "" H 4750 5950 50  0001 C CNN
	1    4750 5950
	-1   0    0    1   
$EndComp
$Comp
L power:+3.3V #PWR0130
U 1 1 5D9F1721
P 4750 5525
F 0 "#PWR0130" H 4750 5375 50  0001 C CNN
F 1 "+3.3V" H 4765 5698 50  0000 C CNN
F 2 "" H 4750 5525 50  0001 C CNN
F 3 "" H 4750 5525 50  0001 C CNN
	1    4750 5525
	1    0    0    -1  
$EndComp
Wire Wire Line
	4750 5525 4750 5575
Wire Wire Line
	4750 5875 4750 5950
Text Label 2575 4225 0    50   ~ 0
SDIO_DATA2
Text Label 2575 3025 0    50   ~ 0
SDIO_CMD
Text Label 2575 4025 0    50   ~ 0
SDIO_DATA0
Text Label 2575 4425 0    50   ~ 0
SDIO_CLK
Text Label 2575 4125 0    50   ~ 0
SDIO_DATA1
Text Label 2575 4325 0    50   ~ 0
SDIO_DATA3
Wire Wire Line
	2625 8200 2625 8150
Wire Wire Line
	2725 8175 2725 8150
NoConn ~ 2525 8150
Wire Wire Line
	2725 8175 2925 8175
Wire Wire Line
	2925 8175 2925 7300
$Comp
L power:GND #PWR0113
U 1 1 5D91F077
P 2625 8200
F 0 "#PWR0113" H 2625 7950 50  0001 C CNN
F 1 "GND" H 2675 8050 50  0000 R CNN
F 2 "" H 2625 8200 50  0001 C CNN
F 3 "" H 2625 8200 50  0001 C CNN
	1    2625 8200
	1    0    0    -1  
$EndComp
Wire Notes Line
	800  6600 3600 6600
Text Notes 975  8275 0    50   ~ 0
SIM Card Module
Wire Notes Line
	1075 8800 1075 10875
Wire Notes Line
	1075 10875 3850 10875
Wire Notes Line
	3850 10875 3850 8800
Wire Notes Line
	3850 8800 1075 8800
Wire Notes Line
	9750 6175 9750 9100
Wire Notes Line
	9750 9100 15750 9100
Wire Notes Line
	15750 9100 15750 6175
Wire Notes Line
	15750 6175 9750 6175
Wire Notes Line
	13475 4050 13475 5900
Wire Notes Line
	13475 5900 15900 5900
Wire Notes Line
	15900 5900 15900 4050
Wire Notes Line
	15900 4050 13475 4050
Text Notes 13575 4200 0    50   ~ 0
Temperature and Humidity Sensor
$Comp
L Device:C_Small C14
U 1 1 5DABCEC8
P 5050 7750
F 0 "C14" V 5150 7850 50  0000 C CNN
F 1 "10nF" V 4912 7750 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 5050 7750 50  0001 C CNN
F 3 "~" H 5050 7750 50  0001 C CNN
	1    5050 7750
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0145
U 1 1 5DABCED9
P 4650 7825
F 0 "#PWR0145" H 4650 7575 50  0001 C CNN
F 1 "GND" V 4655 7697 50  0000 R CNN
F 2 "" H 4650 7825 50  0001 C CNN
F 3 "" H 4650 7825 50  0001 C CNN
	1    4650 7825
	1    0    0    -1  
$EndComp
Wire Wire Line
	4850 7500 4650 7500
Wire Wire Line
	4950 7750 4650 7750
Wire Wire Line
	4650 7500 4650 7750
Connection ~ 4650 7750
Wire Wire Line
	4650 7750 4650 7825
Wire Wire Line
	5250 7500 5400 7500
Wire Wire Line
	5150 7750 5400 7750
Wire Wire Line
	5400 7750 5400 7500
Connection ~ 5400 7500
Wire Wire Line
	5400 7500 5475 7500
Text Label 5475 7500 0    50   ~ 0
SWITCH_1
Wire Notes Line
	4350 7050 4350 8125
Wire Notes Line
	4350 8125 7100 8125
Wire Notes Line
	7100 8125 7100 7050
Wire Notes Line
	7100 7050 4350 7050
Text Notes 4400 7150 0    50   ~ 0
Switch (event controller)
Wire Notes Line
	4325 8700 4325 11075
Wire Wire Line
	6975 10225 6975 10575
Wire Wire Line
	7075 10225 6975 10225
Text Label 4475 10325 0    50   ~ 0
SDIO_DATA0
Text Label 4475 10425 0    50   ~ 0
SDIO_DATA1
$Comp
L power:+3.3V #PWR0135
U 1 1 5DA39854
P 5100 9525
F 0 "#PWR0135" H 5100 9375 50  0001 C CNN
F 1 "+3.3V" H 5115 9698 50  0000 C CNN
F 2 "" H 5100 9525 50  0001 C CNN
F 3 "" H 5100 9525 50  0001 C CNN
	1    5100 9525
	1    0    0    -1  
$EndComp
Text Label 8600 10825 0    50   ~ 0
TF_Card_Detection
Text Notes 6375 10975 0    50   ~ 0
Note: Pin 9 should be the shield (GND), but the footprint \nhas the card detection (CD) as Pin 9.
Text Label 4475 10225 0    50   ~ 0
SDIO_CLK
Text Label 4475 9825 0    50   ~ 0
SDIO_DATA3
Text Label 4475 9725 0    50   ~ 0
SDIO_DATA2
Text Label 4475 9925 0    50   ~ 0
SDIO_CMD
Wire Wire Line
	6975 10025 7075 10025
$Comp
L power:GND #PWR0137
U 1 1 5DA53AB6
P 6975 10575
F 0 "#PWR0137" H 6975 10325 50  0001 C CNN
F 1 "GND" H 7025 10425 50  0000 R CNN
F 2 "" H 6975 10575 50  0001 C CNN
F 3 "" H 6975 10575 50  0001 C CNN
	1    6975 10575
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0136
U 1 1 5DA51E3E
P 6975 9200
F 0 "#PWR0136" H 6975 9050 50  0001 C CNN
F 1 "+3.3V" H 6990 9373 50  0000 C CNN
F 2 "" H 6975 9200 50  0001 C CNN
F 3 "" H 6975 9200 50  0001 C CNN
	1    6975 9200
	1    0    0    -1  
$EndComp
Text Notes 8425 8925 0    50   ~ 0
TF Card Module
Wire Notes Line
	4325 11075 9325 11075
Wire Notes Line
	9325 11075 9325 8700
Wire Notes Line
	3600 8500 800  8500
Wire Notes Line
	9325 8700 4325 8700
Wire Notes Line
	3600 6600 3600 8500
Wire Notes Line
	800  8500 800  6600
Text Label 4775 3925 0    50   ~ 0
I2C1_SDA
Text Label 2900 10375 0    50   ~ 0
Current_SDA
Text Label 2900 10650 0    50   ~ 0
Current_SCL
Text Label 2900 10750 0    50   ~ 0
I2C1_SCL
Text Label 2900 10475 0    50   ~ 0
I2C1_SDA
Wire Wire Line
	2900 10375 2825 10375
Wire Wire Line
	2825 10375 2825 10475
Wire Wire Line
	2825 10475 2900 10475
Wire Wire Line
	2900 10650 2825 10650
Wire Wire Line
	2825 10650 2825 10750
Wire Wire Line
	2825 10750 2900 10750
Text Label 4775 4325 0    50   ~ 0
I2C2_SDA
Text Label 4775 4225 0    50   ~ 0
I2C2_SCL
$Comp
L power:+3.3V #PWR0146
U 1 1 5DC92C4B
P 5875 3300
F 0 "#PWR0146" H 5875 3150 50  0001 C CNN
F 1 "+3.3V" H 5890 3473 50  0000 C CNN
F 2 "" H 5875 3300 50  0001 C CNN
F 3 "" H 5875 3300 50  0001 C CNN
	1    5875 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	4525 3725 4775 3725
Text Label 4775 3825 0    50   ~ 0
I2C1_SCL
Wire Wire Line
	7425 4275 7425 4350
Wire Wire Line
	7425 4350 6875 4350
Wire Wire Line
	6875 4350 6875 4550
Wire Wire Line
	6875 4550 7025 4550
Connection ~ 7425 4350
Wire Wire Line
	7025 4650 6875 4650
Wire Wire Line
	6875 4650 6875 4750
Wire Wire Line
	6875 4750 7025 4750
Wire Wire Line
	6875 4750 6875 4975
Wire Wire Line
	6875 4975 7425 4975
Connection ~ 6875 4750
Connection ~ 7425 4975
Wire Wire Line
	7425 4975 7425 4950
Text Notes 6600 5325 0    50   ~ 0
Note: EEPROM address 0b1010100x. \nWhen x=0, write, x=1, read
Wire Wire Line
	7975 4750 7975 4975
Wire Wire Line
	7975 4975 7425 4975
$Comp
L Connector_Generic:Conn_01x04 J4
U 1 1 5DD97F8F
P 7850 3250
F 0 "J4" H 7930 3242 50  0000 L CNN
F 1 "Display_Connector" H 7350 2950 50  0000 L CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x04_P1.27mm_Vertical" H 7850 3250 50  0001 C CNN
F 3 "~" H 7850 3250 50  0001 C CNN
	1    7850 3250
	1    0    0    -1  
$EndComp
Text Label 7200 3450 0    50   ~ 0
I2C2_SDA
Text Label 7200 3350 0    50   ~ 0
I2C2_SCL
$Comp
L power:+3.3V #PWR0147
U 1 1 5DDA1795
P 7450 3125
F 0 "#PWR0147" H 7450 2975 50  0001 C CNN
F 1 "+3.3V" H 7465 3298 50  0000 C CNN
F 2 "" H 7450 3125 50  0001 C CNN
F 3 "" H 7450 3125 50  0001 C CNN
	1    7450 3125
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0148
U 1 1 5DDA17A3
P 7050 3250
F 0 "#PWR0148" H 7050 3000 50  0001 C CNN
F 1 "GND" H 7055 3122 50  0000 R CNN
F 2 "" H 7050 3250 50  0001 C CNN
F 3 "" H 7050 3250 50  0001 C CNN
	1    7050 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 3125 7450 3150
Wire Wire Line
	7450 3150 7650 3150
Wire Wire Line
	7650 3250 7050 3250
Wire Wire Line
	7200 3350 7650 3350
Wire Wire Line
	7650 3450 7200 3450
Wire Notes Line
	6775 2750 6775 3775
Wire Notes Line
	6775 3775 8250 3775
Wire Notes Line
	8250 3775 8250 2750
Wire Notes Line
	8250 2750 6775 2750
Text Notes 6825 2850 0    50   ~ 0
Display Connector
Text Notes 6850 3725 0    50   ~ 0
Note: the address is 0x78
Text Notes 1150 10800 0    50   ~ 0
Note: the address is 0x80
Text Label 4775 1725 0    50   ~ 0
USART2_Tx
Text Label 5250 1825 0    50   ~ 0
M_MAIN_UART_Tx_H
Text Label 5250 1725 0    50   ~ 0
M_MAIN_UART_Rx_H
Wire Wire Line
	4525 1725 5250 1725
Wire Wire Line
	4525 1825 5250 1825
Text Label 4775 2525 0    50   ~ 0
USART1_Rx
Text Label 4775 2425 0    50   ~ 0
USART1_Tx
Text Label 5250 2525 0    50   ~ 0
M_DBG_UART_TX_H
Text Label 5250 2425 0    50   ~ 0
M_DBG_UART_Rx_H
Wire Wire Line
	4525 2425 5250 2425
Wire Wire Line
	4525 2525 5250 2525
$Comp
L power:+3.3V #PWR0149
U 1 1 5DFB9A49
P 13300 6675
F 0 "#PWR0149" H 13300 6525 50  0001 C CNN
F 1 "+3.3V" H 13315 6848 50  0000 C CNN
F 2 "" H 13300 6675 50  0001 C CNN
F 3 "" H 13300 6675 50  0001 C CNN
	1    13300 6675
	1    0    0    -1  
$EndComp
Wire Wire Line
	13300 6675 13300 6800
Connection ~ 13300 6800
Wire Wire Line
	13300 6800 13800 6800
Text Label 14225 7600 0    50   ~ 0
I2C2_SDA
Text Label 14225 7700 0    50   ~ 0
I2C2_SCL
Wire Wire Line
	14225 7600 15325 7600
Wire Wire Line
	14225 7700 15325 7700
Text Label 2575 3225 0    50   ~ 0
VBAT_ADC
Text Label 5200 4625 0    50   ~ 0
M_SPI_MISO-I2S_RXD
Text Label 5200 4525 0    50   ~ 0
M_SPI_CLK-I2S_CLK
Text Label 5200 4725 0    50   ~ 0
M_SPI_MOSI-I2S_WA
Text Label 4775 4525 0    50   ~ 0
SPI2_CK
Wire Wire Line
	4525 4525 5200 4525
Text Label 4775 4625 0    50   ~ 0
SPI2_MISO
Wire Wire Line
	4525 4625 5200 4625
Text Label 4775 4725 0    50   ~ 0
SPI2_MOSI
Wire Wire Line
	4525 4725 5200 4725
Text Label 14625 7400 0    50   ~ 0
SIM_GND
Text Label 14625 7500 0    50   ~ 0
GPIO_R1
Text Label 14625 7300 0    50   ~ 0
SIM_CLK
Text Label 14625 7200 0    50   ~ 0
SIM_IO
Text Label 14625 7100 0    50   ~ 0
SIM_RST
Text Label 14625 7000 0    50   ~ 0
V_SIM
Text Label 14625 6900 0    50   ~ 0
M_VCC
$Comp
L power:GND #PWR0150
U 1 1 5D771A78
P 11600 5775
F 0 "#PWR0150" H 11600 5525 50  0001 C CNN
F 1 "GND" H 11605 5602 50  0000 C CNN
F 2 "" H 11600 5775 50  0001 C CNN
F 3 "" H 11600 5775 50  0001 C CNN
	1    11600 5775
	1    0    0    -1  
$EndComp
Wire Notes Line
	8800 4050 13125 4050
Text Label 10825 5475 0    50   ~ 0
M_NET_LED
Text Label 4775 4425 0    50   ~ 0
M_SPI_CS-I2S_CS
Wire Wire Line
	10825 5500 10825 5475
$Comp
L Connector_Generic:Conn_01x03 J9
U 1 1 5E186F3E
P 9600 3250
F 0 "J9" H 9680 3292 50  0000 L CNN
F 1 "AUX_UART" H 9425 3025 50  0000 L CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x03_P1.27mm_Vertical" H 9600 3250 50  0001 C CNN
F 3 "~" H 9600 3250 50  0001 C CNN
	1    9600 3250
	1    0    0    -1  
$EndComp
Text Label 8750 3250 0    50   ~ 0
M_AUX_UART_Rx_H
Text Label 8750 3150 0    50   ~ 0
M_AUX_UART_Tx_H
Wire Wire Line
	9400 3250 8750 3250
$Comp
L power:GND #PWR0153
U 1 1 5E198EE7
P 9225 3400
F 0 "#PWR0153" H 9225 3150 50  0001 C CNN
F 1 "GND" H 9230 3272 50  0000 R CNN
F 2 "" H 9225 3400 50  0001 C CNN
F 3 "" H 9225 3400 50  0001 C CNN
	1    9225 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	9400 3350 9225 3350
Wire Wire Line
	9225 3350 9225 3400
Wire Wire Line
	9400 3150 8750 3150
Wire Notes Line
	8625 2850 8625 3625
Wire Notes Line
	8625 3625 9825 3625
Wire Notes Line
	9825 3625 9825 2850
Wire Notes Line
	9825 2850 8625 2850
Text Notes 8650 2975 0    50   ~ 0
Aux UART Connector
Text Label 2575 3525 0    50   ~ 0
GPIO_L2
Text Label 2575 3425 0    50   ~ 0
PSM_IND
Text Label 2575 3325 0    50   ~ 0
GPIO_L1
Text Label 4775 1625 0    50   ~ 0
GPIO_L4
Text Label 4775 1525 0    50   ~ 0
GPIO_L3
Text Label 4775 2225 0    50   ~ 0
M_AP_READY
Text Label 4775 2125 0    50   ~ 0
PSM_EINT
Text Label 4775 1925 0    50   ~ 0
M_PWRKEY_H
Text Label 4775 2025 0    50   ~ 0
M_RESET
$Comp
L node_base-rescue:Test_Pin-dly_customized T1
U 1 1 5E21EF91
P 12850 8000
F 0 "T1" V 13065 8117 50  0000 C CNN
F 1 "M_ADC" V 12974 8117 50  0000 C CNN
F 2 "LTD_Customized:test_pad" H 12850 8000 50  0001 C CNN
F 3 "" H 12850 8000 50  0001 C CNN
	1    12850 8000
	0    -1   -1   0   
$EndComp
Wire Wire Line
	12850 8000 13800 8000
Wire Wire Line
	8525 7250 8525 7300
$Comp
L Device:R R20
U 1 1 5E232737
P 8675 7500
F 0 "R20" V 8575 7500 50  0000 C CNN
F 1 "22" V 8675 7500 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8605 7500 50  0001 C CNN
F 3 "~" H 8675 7500 50  0001 C CNN
	1    8675 7500
	0    1    1    0   
$EndComp
Wire Wire Line
	7925 7900 7925 8000
$Comp
L Connector:USB_B_Micro J10
U 1 1 5E232749
P 8025 7500
F 0 "J10" H 8082 7967 50  0000 C CNN
F 1 "USB_B_Micro" H 8082 7876 50  0000 C CNN
F 2 "Connector_USB:USB_Micro-B_Molex-105017-0001" H 8175 7450 50  0001 C CNN
F 3 "~" H 8175 7450 50  0001 C CNN
	1    8025 7500
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR0154
U 1 1 5E232768
P 8525 7250
F 0 "#PWR0154" H 8525 7100 50  0001 C CNN
F 1 "+5V" H 8540 7423 50  0000 C CNN
F 2 "" H 8525 7250 50  0001 C CNN
F 3 "" H 8525 7250 50  0001 C CNN
	1    8525 7250
	1    0    0    -1  
$EndComp
Text Notes 8575 7000 0    50   ~ 0
USB Connector for MCU
Wire Wire Line
	8825 8150 9175 8150
Wire Notes Line
	9575 8500 9575 6850
NoConn ~ 8325 7700
Wire Wire Line
	8525 7500 8325 7500
$Comp
L power:GNDA #PWR0155
U 1 1 5E23277E
P 8025 8050
F 0 "#PWR0155" H 8025 7800 50  0001 C CNN
F 1 "GNDA" H 8030 7877 50  0000 C CNN
F 2 "" H 8025 8050 50  0001 C CNN
F 3 "" H 8025 8050 50  0001 C CNN
	1    8025 8050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0156
U 1 1 5E23278C
P 9175 8150
F 0 "#PWR0156" H 9175 7900 50  0001 C CNN
F 1 "GND" H 9425 8100 50  0000 R CNN
F 2 "" H 9175 8150 50  0001 C CNN
F 3 "" H 9175 8150 50  0001 C CNN
	1    9175 8150
	1    0    0    -1  
$EndComp
$Comp
L power:GNDA #PWR0157
U 1 1 5E23279A
P 8825 8150
F 0 "#PWR0157" H 8825 7900 50  0001 C CNN
F 1 "GNDA" H 8625 8100 50  0000 C CNN
F 2 "" H 8825 8150 50  0001 C CNN
F 3 "" H 8825 8150 50  0001 C CNN
	1    8825 8150
	1    0    0    -1  
$EndComp
Wire Wire Line
	8975 7600 8825 7600
Wire Wire Line
	7925 8000 8025 8000
Wire Wire Line
	8025 8000 8025 8050
Wire Notes Line
	7625 8500 9575 8500
Connection ~ 8025 8000
Wire Notes Line
	7625 6850 7625 8500
Wire Notes Line
	9575 6850 7625 6850
$Comp
L Device:R R21
U 1 1 5E2327B4
P 8675 7600
F 0 "R21" V 8775 7600 50  0000 C CNN
F 1 "22" V 8675 7600 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8605 7600 50  0001 C CNN
F 3 "~" H 8675 7600 50  0001 C CNN
	1    8675 7600
	0    1    1    0   
$EndComp
Wire Wire Line
	8525 7300 8325 7300
Wire Wire Line
	8825 7500 8850 7500
Wire Wire Line
	8025 7900 8025 8000
Wire Wire Line
	8325 7600 8525 7600
Text Label 8975 7500 0    50   ~ 0
MCU_USB_DP
Text Label 8975 7600 0    50   ~ 0
MCU_USB_DM
Text Label 4775 2625 0    50   ~ 0
MCU_USB_DM
Text Label 4775 2725 0    50   ~ 0
MCU_USB_DP
Text Label 4775 3025 0    50   ~ 0
GPIO_R1
Text Label 4775 2325 0    50   ~ 0
GPIO_R2
Text Label 2575 3925 0    50   ~ 0
GPIO_R3
Text Label 2575 3825 0    50   ~ 0
M_RI_H
Text Label 2575 3625 0    50   ~ 0
LED0
Text Label 2575 3725 0    50   ~ 0
LED1
Wire Wire Line
	5900 7725 5900 7800
$Comp
L Device:C_Small C15
U 1 1 5E32B4F0
P 6300 7725
F 0 "C15" V 6400 7825 50  0000 C CNN
F 1 "10nF" V 6162 7725 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6300 7725 50  0001 C CNN
F 3 "~" H 6300 7725 50  0001 C CNN
	1    6300 7725
	0    1    1    0   
$EndComp
Text Label 6725 7475 0    50   ~ 0
SWITCH_2
Wire Wire Line
	6650 7725 6650 7475
Wire Wire Line
	6100 7475 5900 7475
Wire Wire Line
	6650 7475 6725 7475
$Comp
L power:GND #PWR0158
U 1 1 5E32B505
P 5900 7800
F 0 "#PWR0158" H 5900 7550 50  0001 C CNN
F 1 "GND" V 5905 7672 50  0000 R CNN
F 2 "" H 5900 7800 50  0001 C CNN
F 3 "" H 5900 7800 50  0001 C CNN
	1    5900 7800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 7475 6650 7475
Connection ~ 5900 7725
Wire Wire Line
	6200 7725 5900 7725
Wire Wire Line
	6400 7725 6650 7725
Connection ~ 6650 7475
Wire Wire Line
	5900 7475 5900 7725
Connection ~ 10000 10550
Wire Wire Line
	10300 10150 10500 10150
Wire Wire Line
	10000 10450 10000 10550
Wire Wire Line
	10800 10050 11050 10050
Wire Wire Line
	10500 9850 10300 9850
$Comp
L Device:R R10
U 1 1 5D93722C
P 10650 10150
F 0 "R10" V 10750 10150 50  0000 C CNN
F 1 "22" V 10650 10150 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 10580 10150 50  0001 C CNN
F 3 "~" H 10650 10150 50  0001 C CNN
	1    10650 10150
	0    1    1    0   
$EndComp
Wire Notes Line
	11550 9400 9600 9400
Wire Notes Line
	9600 9400 9600 11050
Wire Notes Line
	9600 11050 11550 11050
Wire Wire Line
	10000 10550 10000 10600
Wire Wire Line
	9900 10550 10000 10550
Wire Wire Line
	11050 10150 10800 10150
$Comp
L power:GNDA #PWR0129
U 1 1 5D937232
P 10800 10700
F 0 "#PWR0129" H 10800 10450 50  0001 C CNN
F 1 "GNDA" H 10600 10650 50  0000 C CNN
F 2 "" H 10800 10700 50  0001 C CNN
F 3 "" H 10800 10700 50  0001 C CNN
	1    10800 10700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0128
U 1 1 5D937231
P 11150 10700
F 0 "#PWR0128" H 11150 10450 50  0001 C CNN
F 1 "GND" H 11400 10650 50  0000 R CNN
F 2 "" H 11150 10700 50  0001 C CNN
F 3 "" H 11150 10700 50  0001 C CNN
	1    11150 10700
	1    0    0    -1  
$EndComp
$Comp
L power:GNDA #PWR0127
U 1 1 5D937230
P 10000 10600
F 0 "#PWR0127" H 10000 10350 50  0001 C CNN
F 1 "GNDA" H 10005 10427 50  0000 C CNN
F 2 "" H 10000 10600 50  0001 C CNN
F 3 "" H 10000 10600 50  0001 C CNN
	1    10000 10600
	1    0    0    -1  
$EndComp
Wire Wire Line
	10500 10050 10300 10050
NoConn ~ 10300 10250
Wire Notes Line
	11550 11050 11550 9400
Wire Wire Line
	10800 10700 11150 10700
Text Label 11050 10150 0    50   ~ 0
M_USB_DM
Text Notes 10475 9525 0    50   ~ 0
USB Connector for Module
$Comp
L power:+5V #PWR0159
U 1 1 5D93722D
P 10500 9800
F 0 "#PWR0159" H 10500 9650 50  0001 C CNN
F 1 "+5V" H 10515 9973 50  0000 C CNN
F 2 "" H 10500 9800 50  0001 C CNN
F 3 "" H 10500 9800 50  0001 C CNN
	1    10500 9800
	1    0    0    -1  
$EndComp
$Comp
L Connector:USB_B_Micro J5
U 1 1 5D93722E
P 10000 10050
F 0 "J5" H 10057 10517 50  0000 C CNN
F 1 "USB_B_Micro" H 10057 10426 50  0000 C CNN
F 2 "Connector_USB:USB_Micro-B_Molex-105017-0001" H 10150 10000 50  0001 C CNN
F 3 "~" H 10150 10000 50  0001 C CNN
	1    10000 10050
	1    0    0    -1  
$EndComp
Wire Wire Line
	9900 10450 9900 10550
$Comp
L Device:R R9
U 1 1 5D93722F
P 10650 10050
F 0 "R9" V 10550 10050 50  0000 C CNN
F 1 "22" V 10650 10050 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 10580 10050 50  0001 C CNN
F 3 "~" H 10650 10050 50  0001 C CNN
	1    10650 10050
	0    1    1    0   
$EndComp
Wire Wire Line
	10500 9800 10500 9850
Wire Notes Line
	8300 5600 6825 5600
Text Notes 6875 5700 0    50   ~ 0
GPIO Out
Wire Notes Line
	6825 5600 6825 6625
Wire Wire Line
	7575 5875 7575 5900
Wire Notes Line
	6825 6625 8300 6625
Wire Notes Line
	8300 6625 8300 5600
$Comp
L power:+3.3V #PWR0160
U 1 1 5E3C4325
P 7575 5875
F 0 "#PWR0160" H 7575 5725 50  0001 C CNN
F 1 "+3.3V" H 7590 6048 50  0000 C CNN
F 2 "" H 7575 5875 50  0001 C CNN
F 3 "" H 7575 5875 50  0001 C CNN
	1    7575 5875
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0161
U 1 1 5E3C4334
P 7600 6450
F 0 "#PWR0161" H 7600 6200 50  0001 C CNN
F 1 "GND" H 7605 6322 50  0000 R CNN
F 2 "" H 7600 6450 50  0001 C CNN
F 3 "" H 7600 6450 50  0001 C CNN
	1    7600 6450
	1    0    0    -1  
$EndComp
Wire Wire Line
	7575 5900 7775 5900
$Comp
L Connector_Generic:Conn_01x06 J7
U 1 1 5E3D4BBA
P 7975 6100
F 0 "J7" H 8055 6092 50  0000 L CNN
F 1 "GPIO_Out" H 7825 5675 50  0000 L CNN
F 2 "Connector_PinSocket_1.27mm:PinSocket_1x06_P1.27mm_Vertical" H 7975 6100 50  0001 C CNN
F 3 "~" H 7975 6100 50  0001 C CNN
	1    7975 6100
	1    0    0    -1  
$EndComp
NoConn ~ 2775 4525
Text Label 4775 3225 0    50   ~ 0
SWITCH_1
Text Label 4775 3325 0    50   ~ 0
SWITCH_2
Wire Wire Line
	7775 6400 7600 6400
Wire Wire Line
	7600 6400 7600 6450
Text Label 4775 3625 0    50   ~ 0
GPIO_1
Text Label 4775 3725 0    50   ~ 0
GPIO_2
Text Label 4775 4025 0    50   ~ 0
GPIO_3
Text Label 4775 4125 0    50   ~ 0
GPIO_4
Text Label 7400 6000 0    50   ~ 0
GPIO_1
Text Label 7400 6100 0    50   ~ 0
GPIO_2
Text Label 7400 6200 0    50   ~ 0
GPIO_3
Text Label 7400 6300 0    50   ~ 0
GPIO_4
Wire Wire Line
	7400 6000 7775 6000
Wire Wire Line
	7775 6100 7400 6100
Wire Wire Line
	7400 6200 7775 6200
Wire Wire Line
	7775 6300 7400 6300
Text Label 11050 10050 0    50   ~ 0
M_USB_DP
$Comp
L Device:C_Small C17
U 1 1 5E483798
P 7675 4350
F 0 "C17" V 7446 4350 50  0000 C CNN
F 1 "10nF" V 7537 4350 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 7675 4350 50  0001 C CNN
F 3 "~" H 7675 4350 50  0001 C CNN
	1    7675 4350
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0151
U 1 1 5E48422C
P 7925 4350
F 0 "#PWR0151" H 7925 4100 50  0001 C CNN
F 1 "GND" H 8175 4350 50  0000 R CNN
F 2 "" H 7925 4350 50  0001 C CNN
F 3 "" H 7925 4350 50  0001 C CNN
	1    7925 4350
	1    0    0    -1  
$EndComp
Wire Wire Line
	7775 4350 7925 4350
Wire Wire Line
	7575 4350 7425 4350
$Comp
L Device:C_Small C16
U 1 1 5E496378
P 1925 9225
F 0 "C16" H 1775 9325 50  0000 C CNN
F 1 "100nF" H 1775 9150 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1925 9225 50  0001 C CNN
F 3 "~" H 1925 9225 50  0001 C CNN
	1    1925 9225
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0152
U 1 1 5E4A4F3C
P 1925 9325
F 0 "#PWR0152" H 1925 9075 50  0001 C CNN
F 1 "GND" H 2000 9175 50  0000 R CNN
F 2 "" H 1925 9325 50  0001 C CNN
F 3 "" H 1925 9325 50  0001 C CNN
	1    1925 9325
	1    0    0    -1  
$EndComp
Wire Wire Line
	2125 9125 1925 9125
Wire Wire Line
	5875 3300 5875 3375
Wire Wire Line
	5575 3825 4525 3825
Wire Wire Line
	4525 3925 5675 3925
Wire Wire Line
	4525 4225 5775 4225
Wire Wire Line
	4525 4325 5875 4325
Text Label 10750 9850 0    50   ~ 0
M_USB_VBUS
Wire Wire Line
	10750 9850 10500 9850
Connection ~ 10500 9850
Text Label 12900 8600 0    50   ~ 0
M_VDD_OUT
Text Label 14625 8600 0    50   ~ 0
M_GND
$Comp
L Logic_LevelTranslator:TXB0108DQSR U7
U 1 1 5E5D2053
P 11050 7500
F 0 "U7" H 10800 8175 50  0000 C CNN
F 1 "TXB0108DQSR" H 11475 6825 50  0000 C CNN
F 2 "Package_SON:USON-20_2x4mm_P0.4mm" H 11050 6750 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/txb0108.pdf" H 11050 7400 50  0001 C CNN
	1    11050 7500
	1    0    0    -1  
$EndComp
Text Notes 9950 6400 0    50   ~ 0
Note: in logic converter, VCC_A < VCC_B\nB side: 3.3 V (MCU), A side: 1.8/3.0 V (Module)
$Comp
L power:+3.3V #PWR0162
U 1 1 5E663E72
P 11150 6625
F 0 "#PWR0162" H 11150 6475 50  0001 C CNN
F 1 "+3.3V" H 11165 6798 50  0000 C CNN
F 2 "" H 11150 6625 50  0001 C CNN
F 3 "" H 11150 6625 50  0001 C CNN
	1    11150 6625
	1    0    0    -1  
$EndComp
Wire Wire Line
	11150 6625 11150 6650
Text Label 10150 6650 0    50   ~ 0
M_VDD_OUT
Wire Wire Line
	10950 6650 10950 6800
$Comp
L Device:C_Small C18
U 1 1 5E67DB9A
P 10250 6750
F 0 "C18" H 10075 6750 50  0000 C CNN
F 1 "100nF" H 10100 6675 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 10250 6750 50  0001 C CNN
F 3 "~" H 10250 6750 50  0001 C CNN
	1    10250 6750
	1    0    0    -1  
$EndComp
$Comp
L Device:C_Small C19
U 1 1 5E67E697
P 11475 6750
F 0 "C19" H 11350 6675 50  0000 C CNN
F 1 "100nF" H 11350 6850 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 11475 6750 50  0001 C CNN
F 3 "~" H 11475 6750 50  0001 C CNN
	1    11475 6750
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0163
U 1 1 5E681E63
P 11475 6850
F 0 "#PWR0163" H 11475 6600 50  0001 C CNN
F 1 "GND" H 11480 6677 50  0000 C CNN
F 2 "" H 11475 6850 50  0001 C CNN
F 3 "" H 11475 6850 50  0001 C CNN
	1    11475 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	11475 6650 11150 6650
Connection ~ 11150 6650
$Comp
L power:GND #PWR0164
U 1 1 5E687179
P 10250 6900
F 0 "#PWR0164" H 10250 6650 50  0001 C CNN
F 1 "GND" H 10255 6727 50  0000 C CNN
F 2 "" H 10250 6900 50  0001 C CNN
F 3 "" H 10250 6900 50  0001 C CNN
	1    10250 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	10150 6650 10250 6650
Connection ~ 10250 6650
Wire Wire Line
	10250 6850 10250 6900
Wire Wire Line
	10650 7100 10575 7100
$Comp
L power:GND #PWR0165
U 1 1 5E692A55
P 11050 8250
F 0 "#PWR0165" H 11050 8000 50  0001 C CNN
F 1 "GND" H 11055 8077 50  0000 C CNN
F 2 "" H 11050 8250 50  0001 C CNN
F 3 "" H 11050 8250 50  0001 C CNN
	1    11050 8250
	1    0    0    -1  
$EndComp
Wire Wire Line
	11050 8250 11050 8200
Wire Wire Line
	10250 6650 10575 6650
Wire Wire Line
	9950 7900 10650 7900
Wire Wire Line
	10650 7800 9950 7800
Wire Wire Line
	10650 7600 9950 7600
Wire Wire Line
	9950 7500 10650 7500
Wire Wire Line
	10650 7400 9950 7400
Wire Wire Line
	9950 7300 10650 7300
Wire Wire Line
	10650 7200 9950 7200
Text Label 9950 7900 0    50   ~ 0
M_MAIN_UART_Tx
Text Label 9950 7800 0    50   ~ 0
M_MAIN_UART_Rx
Text Label 9950 7500 0    50   ~ 0
M_DBG_UART_Rx
Text Label 9950 7600 0    50   ~ 0
M_DBG_UART_TX
Text Label 9950 7300 0    50   ~ 0
M_AUX_UART_Rx
Text Label 12100 8400 0    50   ~ 0
M_PWRKEY
Text Label 9950 7200 0    50   ~ 0
M_RI
Text Label 9950 7400 0    50   ~ 0
M_AUX_UART_Tx
Text Label 14625 8000 0    50   ~ 0
M_AUX_UART_Tx
Text Label 11200 8600 0    50   ~ 0
M_PWRKEY_H
Text Label 11600 7200 0    50   ~ 0
M_RI_H
Text Label 11600 7800 0    50   ~ 0
M_MAIN_UART_Rx_H
Text Label 11600 7500 0    50   ~ 0
M_DBG_UART_Rx_H
Text Label 11600 7900 0    50   ~ 0
M_MAIN_UART_Tx_H
Text Label 11600 7600 0    50   ~ 0
M_DBG_UART_TX_H
Text Label 11600 7300 0    50   ~ 0
M_AUX_UART_Rx_H
Text Label 11600 7400 0    50   ~ 0
M_AUX_UART_Tx_H
Wire Wire Line
	11600 7200 11450 7200
Wire Wire Line
	11450 7300 11600 7300
Wire Wire Line
	11600 7400 11450 7400
Wire Wire Line
	11450 7500 11600 7500
Wire Wire Line
	11600 7600 11450 7600
Wire Wire Line
	11450 7700 11600 7700
Wire Wire Line
	11600 7800 11450 7800
Wire Wire Line
	11450 7900 11600 7900
$Comp
L Device:R R12
U 1 1 5DB4F615
P 1525 9775
F 0 "R12" H 1595 9821 50  0000 L CNN
F 1 "R100" H 1595 9730 50  0000 L CNN
F 2 "Resistor_SMD:R_1206_3216Metric" V 1455 9775 50  0001 C CNN
F 3 "~" H 1525 9775 50  0001 C CNN
	1    1525 9775
	1    0    0    -1  
$EndComp
Wire Wire Line
	14875 5125 14875 5275
Wire Wire Line
	14875 5275 14675 5275
Connection ~ 14675 5275
Wire Wire Line
	14675 5275 14675 5375
Wire Wire Line
	11600 5700 11600 5775
$Comp
L Device:R_Pack04 RN4
U 1 1 5E834F52
P 10175 4900
F 0 "RN4" H 10363 4946 50  0000 L CNN
F 1 "2.2k" H 10363 4855 50  0000 L CNN
F 2 "Resistor_SMD:R_Array_Convex_4x0603" V 10450 4900 50  0001 C CNN
F 3 "~" H 10175 4900 50  0001 C CNN
	1    10175 4900
	0    1    1    0   
$EndComp
$Comp
L Device:LED D3
U 1 1 5D93D26B
P 11000 4650
F 0 "D3" V 11039 4533 50  0000 R CNN
F 1 "LED" V 10948 4533 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 11000 4650 50  0001 C CNN
F 3 "~" H 11000 4650 50  0001 C CNN
	1    11000 4650
	-1   0    0    1   
$EndComp
Wire Wire Line
	11600 5150 11600 5300
Connection ~ 2175 2625
Wire Wire Line
	2175 2625 2725 2625
Connection ~ 2175 2925
Wire Wire Line
	2175 2925 3125 2925
Wire Wire Line
	5575 3375 5675 3375
$Comp
L Device:R R3
U 1 1 5D9BFA7E
P 5575 3575
F 0 "R3" H 5525 3275 50  0000 L CNN
F 1 "4.7k" V 5575 3500 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5505 3575 50  0001 C CNN
F 3 "~" H 5575 3575 50  0001 C CNN
	1    5575 3575
	1    0    0    -1  
$EndComp
$Comp
L Device:R R11
U 1 1 5D9CD1BC
P 5675 3575
F 0 "R11" H 5625 3275 50  0000 L CNN
F 1 "4.7k" V 5675 3500 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5605 3575 50  0001 C CNN
F 3 "~" H 5675 3575 50  0001 C CNN
	1    5675 3575
	1    0    0    -1  
$EndComp
$Comp
L Device:R R13
U 1 1 5D9CDA17
P 5775 3575
F 0 "R13" H 5725 3275 50  0000 L CNN
F 1 "4.7k" V 5775 3500 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5705 3575 50  0001 C CNN
F 3 "~" H 5775 3575 50  0001 C CNN
	1    5775 3575
	1    0    0    -1  
$EndComp
$Comp
L Device:R R16
U 1 1 5D9CE487
P 5875 3575
F 0 "R16" H 5825 3275 50  0000 L CNN
F 1 "4.7k" V 5875 3500 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5805 3575 50  0001 C CNN
F 3 "~" H 5875 3575 50  0001 C CNN
	1    5875 3575
	1    0    0    -1  
$EndComp
Wire Wire Line
	5875 3425 5875 3375
Connection ~ 5875 3375
Wire Wire Line
	5775 3425 5775 3375
Connection ~ 5775 3375
Wire Wire Line
	5775 3375 5875 3375
Wire Wire Line
	5675 3425 5675 3375
Connection ~ 5675 3375
Wire Wire Line
	5675 3375 5775 3375
Wire Wire Line
	5575 3375 5575 3425
Wire Wire Line
	5575 3725 5575 3825
Wire Wire Line
	5675 3725 5675 3925
Wire Wire Line
	5775 3725 5775 4225
Wire Wire Line
	5875 3725 5875 4325
$Comp
L Switch:SW_Push SW1
U 1 1 5D90B6A1
P 1775 1525
F 0 "SW1" H 1775 1810 50  0000 C CNN
F 1 "SW_RST" H 1775 1719 50  0000 C CNN
F 2 "LTD_Customized:SMD_Switch" H 1775 1725 50  0001 C CNN
F 3 "~" H 1775 1725 50  0001 C CNN
	1    1775 1525
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW2
U 1 1 5DABCEB7
P 5050 7500
F 0 "SW2" H 5050 7785 50  0000 C CNN
F 1 "SW_1" H 5050 7694 50  0000 C CNN
F 2 "LTD_Customized:SMD_Switch" H 5050 7700 50  0001 C CNN
F 3 "~" H 5050 7700 50  0001 C CNN
	1    5050 7500
	1    0    0    -1  
$EndComp
$Comp
L Switch:SW_Push SW3
U 1 1 5E32B518
P 6300 7475
F 0 "SW3" H 6300 7760 50  0000 C CNN
F 1 "SW_2" H 6300 7669 50  0000 C CNN
F 2 "LTD_Customized:SMD_Switch" H 6300 7675 50  0001 C CNN
F 3 "~" H 6300 7675 50  0001 C CNN
	1    6300 7475
	1    0    0    -1  
$EndComp
$Comp
L node_base-rescue:Battery_Holder_2x-dly_customized H1
U 1 1 5D947AB4
P 10750 1325
F 0 "H1" H 10800 1400 50  0000 L CNN
F 1 "Battery_Holder_2x" H 10700 600 50  0000 L CNN
F 2 "LTD_Customized:18650_Battery_Holder_2x" H 10750 1325 50  0001 C CNN
F 3 "" H 10750 1325 50  0001 C CNN
	1    10750 1325
	1    0    0    -1  
$EndComp
Wire Wire Line
	15175 1200 15175 1500
$Comp
L Connector_Generic:Conn_01x03 J8
U 1 1 5D9EC1DE
P 15275 1000
F 0 "J8" V 15239 812 50  0000 R CNN
F 1 "PWR_SELECT" V 15375 1200 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 15275 1000 50  0001 C CNN
F 3 "~" H 15275 1000 50  0001 C CNN
	1    15275 1000
	0    -1   -1   0   
$EndComp
$Comp
L power:+3.3V #PWR0126
U 1 1 5D7BC6FD
P 9600 4600
F 0 "#PWR0126" H 9600 4450 50  0001 C CNN
F 1 "+3.3V" H 9615 4773 50  0000 C CNN
F 2 "" H 9600 4600 50  0001 C CNN
F 3 "" H 9600 4600 50  0001 C CNN
	1    9600 4600
	1    0    0    -1  
$EndComp
Text Label 9725 4700 0    50   ~ 0
LED0
Text Label 9725 4800 0    50   ~ 0
LED1
$Comp
L power:GND #PWR0133
U 1 1 5D93D26A
P 11150 4425
F 0 "#PWR0133" H 11150 4175 50  0001 C CNN
F 1 "GND" H 11150 4325 50  0000 R CNN
F 2 "" H 11150 4425 50  0001 C CNN
F 3 "" H 11150 4425 50  0001 C CNN
	1    11150 4425
	0    -1   -1   0   
$EndComp
$Comp
L Device:LED D1
U 1 1 5D7613BF
P 11450 5150
F 0 "D1" V 11425 5300 50  0000 R CNN
F 1 "LED" V 11550 5325 50  0000 R CNN
F 2 "LED_SMD:LED_0805_2012Metric" H 11475 5325 50  0001 C CNN
F 3 "~" H 11475 5325 50  0001 C CNN
	1    11450 5150
	-1   0    0    1   
$EndComp
Wire Wire Line
	10375 4700 10575 4700
Wire Wire Line
	10575 4700 10575 4425
Wire Wire Line
	10575 4425 10850 4425
Wire Wire Line
	10375 4800 10650 4800
Wire Wire Line
	10650 4800 10650 4650
Wire Wire Line
	10650 4650 10850 4650
Wire Wire Line
	10750 4875 10850 4875
Wire Wire Line
	10825 5150 11300 5150
Wire Wire Line
	9975 4700 9725 4700
Wire Wire Line
	9725 4800 9975 4800
Wire Wire Line
	9600 4600 9600 4900
Wire Wire Line
	9600 4900 9975 4900
Wire Wire Line
	9600 5000 9600 4900
Wire Wire Line
	9600 5000 9975 5000
Connection ~ 9600 4900
Wire Wire Line
	10750 5000 10375 5000
Wire Wire Line
	10750 4875 10750 5000
Wire Wire Line
	10375 4900 10825 4900
Wire Wire Line
	10825 4900 10825 5150
$Comp
L Device:C_Small C4
U 1 1 5D90B68A
P 1775 4525
F 0 "C4" V 1546 4525 50  0000 C CNN
F 1 "10pF" V 1637 4525 50  0000 C CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 1775 4525 50  0001 C CNN
F 3 "~" H 1775 4525 50  0001 C CNN
	1    1775 4525
	0    1    1    0   
$EndComp
$Comp
L Device:C C7
U 1 1 5D9F40B2
P 4750 5725
F 0 "C7" H 4865 5771 50  0000 L CNN
F 1 "10nF" H 4865 5680 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4788 5575 50  0001 C CNN
F 3 "~" H 4750 5725 50  0001 C CNN
	1    4750 5725
	1    0    0    -1  
$EndComp
Wire Wire Line
	2925 9375 3525 9375
Wire Wire Line
	2925 9475 3525 9475
Wire Wire Line
	2375 6800 2525 6800
Wire Wire Line
	2375 7100 2625 7100
$Comp
L dly_customized:SMF05C U1
U 1 1 5D91F076
P 2825 7950
F 0 "U1" V 3075 8600 60  0000 R CNN
F 1 "SMF05C" V 2925 8775 60  0000 R CNN
F 2 "Package_TO_SOT_SMD:SOT-363_SC-70-6" H 2825 7900 60  0001 C CNN
F 3 "" H 2825 7900 60  0001 C CNN
	1    2825 7950
	0    -1   -1   0   
$EndComp
Wire Wire Line
	2525 7350 2525 6800
Connection ~ 2525 6800
Wire Wire Line
	2525 6800 3100 6800
Wire Wire Line
	2625 7100 2625 7350
Connection ~ 2625 7100
Wire Wire Line
	2625 7100 3100 7100
Text Label 3150 7450 0    50   ~ 0
V_SIM
Wire Wire Line
	3150 7450 3025 7450
Wire Wire Line
	3025 7450 3025 7300
Connection ~ 3025 7300
Wire Wire Line
	3025 7300 3100 7300
$Comp
L Device:C_Small C20
U 1 1 5DA09042
P 6800 9425
F 0 "C20" H 6892 9471 50  0000 L CNN
F 1 "100nF" H 6892 9380 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 6800 9425 50  0001 C CNN
F 3 "~" H 6800 9425 50  0001 C CNN
	1    6800 9425
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 9325 6975 9325
Wire Wire Line
	6975 9200 6975 9325
Connection ~ 6975 9325
Wire Wire Line
	6975 9325 6975 10025
Wire Wire Line
	6800 9525 6925 9525
Wire Wire Line
	6925 9525 6925 10225
Wire Wire Line
	6925 10225 6975 10225
Connection ~ 6975 10225
$Comp
L Device:R R14
U 1 1 5DB9F8C3
P 13375 1750
F 0 "R14" V 13475 1675 50  0000 C CNN
F 1 "0" V 13375 1750 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 13305 1750 50  0001 C CNN
F 3 "~" H 13375 1750 50  0001 C CNN
	1    13375 1750
	0    1    1    0   
$EndComp
Wire Wire Line
	13225 1750 13175 1750
Wire Wire Line
	13525 1750 13600 1750
Wire Wire Line
	13600 1750 13600 1550
Connection ~ 13600 1550
Wire Wire Line
	13600 1550 13750 1550
Wire Wire Line
	11150 6650 11150 6800
Wire Wire Line
	10575 6650 10575 7100
Connection ~ 10575 6650
Wire Wire Line
	10575 6650 10950 6650
$Comp
L node_base-rescue:CM1624-dly_customized U8
U 1 1 5DBE37A5
P 6225 10525
F 0 "U8" H 6650 10598 50  0000 C CNN
F 1 "CM1624" H 6650 10689 50  0000 C CNN
F 2 "LTD_Customized:UDFN-16_3.3x1.35mm_0.4Pitch" H 6225 10525 50  0001 C CNN
F 3 "" H 6225 10525 50  0001 C CNN
	1    6225 10525
	-1   0    0    1   
$EndComp
$Comp
L Connector:Micro_SD_Card J3
U 1 1 5DA14FFE
P 7975 10025
F 0 "J3" H 7925 10742 50  0000 C CNN
F 1 "Micro_SD_Card" H 7925 10651 50  0000 C CNN
F 2 "LTD_Customized:TF_Card_Socket" H 9125 10325 50  0001 C CNN
F 3 "http://katalog.we-online.de/em/datasheet/693072010801.pdf" H 7975 10025 50  0001 C CNN
	1    7975 10025
	1    0    0    -1  
$EndComp
Wire Wire Line
	8775 10625 8775 10700
Wire Wire Line
	8775 10700 8550 10700
Wire Wire Line
	8550 10700 8550 10825
Wire Wire Line
	8550 10825 8600 10825
Wire Wire Line
	6325 9725 7075 9725
Wire Wire Line
	6325 9825 7075 9825
Wire Wire Line
	6325 9925 7075 9925
Wire Wire Line
	6325 10225 6750 10225
Wire Wire Line
	6750 10225 6750 10125
Wire Wire Line
	6750 10125 7075 10125
Wire Wire Line
	6325 10325 7075 10325
Wire Wire Line
	6325 10425 7075 10425
$Comp
L power:GND #PWR0134
U 1 1 5DBF8DBC
P 6000 9250
F 0 "#PWR0134" H 6000 9000 50  0001 C CNN
F 1 "GND" H 6050 9100 50  0000 R CNN
F 2 "" H 6000 9250 50  0001 C CNN
F 3 "" H 6000 9250 50  0001 C CNN
	1    6000 9250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6000 9250 5775 9250
Wire Wire Line
	5775 9250 5775 9425
Wire Wire Line
	5275 10425 4475 10425
Wire Wire Line
	4475 10325 5275 10325
Wire Wire Line
	5275 10225 4475 10225
Wire Wire Line
	4475 9925 5275 9925
Wire Wire Line
	5275 9825 4475 9825
Wire Wire Line
	5275 9725 4475 9725
Wire Wire Line
	5275 10025 5100 10025
Wire Wire Line
	5100 9525 5100 10025
NoConn ~ 5275 10125
NoConn ~ 6325 10025
NoConn ~ 6325 10125
Text Label 8775 10625 0    50   ~ 0
GPIO_1
Text Label 6450 9725 0    50   ~ 0
SD_DATA2
Text Label 6450 9825 0    50   ~ 0
SD_DATA3
Text Label 6450 9925 0    50   ~ 0
SD_CMD
Text Label 6450 10225 0    50   ~ 0
SD_CLK
Text Label 6450 10325 0    50   ~ 0
SD_DATA0
Text Label 6450 10425 0    50   ~ 0
SD_DATA1
$Comp
L Transistor_BJT:DTC143Z Q1
U 1 1 5E0C1A01
P 11500 5500
F 0 "Q1" H 11688 5546 50  0000 L CNN
F 1 "DTC143Z" H 11688 5455 50  0000 L CNN
F 2 "LTD_Customized:SOT-723" H 11500 5500 50  0001 L CNN
F 3 "" H 11500 5500 50  0001 L CNN
	1    11500 5500
	1    0    0    -1  
$EndComp
Wire Wire Line
	10825 5500 11250 5500
$Comp
L Transistor_BJT:DTC143Z Q2
U 1 1 5E0C8F01
P 12000 8600
F 0 "Q2" H 12188 8646 50  0000 L CNN
F 1 "DTC143Z" H 12188 8555 50  0000 L CNN
F 2 "LTD_Customized:SOT-723" H 12000 8600 50  0001 L CNN
F 3 "" H 12000 8600 50  0001 L CNN
	1    12000 8600
	1    0    0    -1  
$EndComp
Wire Wire Line
	11200 8600 11750 8600
$Comp
L power:GND #PWR0108
U 1 1 5E0CBC74
P 12100 8800
F 0 "#PWR0108" H 12100 8550 50  0001 C CNN
F 1 "GND" H 12105 8627 50  0000 C CNN
F 2 "" H 12100 8800 50  0001 C CNN
F 3 "" H 12100 8800 50  0001 C CNN
	1    12100 8800
	1    0    0    -1  
$EndComp
$Comp
L Device:R R15
U 1 1 5E0D04A9
P 8850 7350
F 0 "R15" H 8920 7396 50  0000 L CNN
F 1 "1.5k" H 8920 7305 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 8780 7350 50  0001 C CNN
F 3 "~" H 8850 7350 50  0001 C CNN
	1    8850 7350
	1    0    0    -1  
$EndComp
Connection ~ 8850 7500
Wire Wire Line
	8850 7500 8975 7500
$Comp
L power:+3.3V #PWR0144
U 1 1 5E0D096F
P 8850 7200
F 0 "#PWR0144" H 8850 7050 50  0001 C CNN
F 1 "+3.3V" H 8865 7373 50  0000 C CNN
F 2 "" H 8850 7200 50  0001 C CNN
F 3 "" H 8850 7200 50  0001 C CNN
	1    8850 7200
	1    0    0    -1  
$EndComp
Wire Wire Line
	2225 1725 2225 2025
$Comp
L Device:R R4
U 1 1 5E0C1C7B
P 2525 1725
F 0 "R4" V 2425 1725 50  0000 C CNN
F 1 "10k" V 2525 1725 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 2455 1725 50  0001 C CNN
F 3 "~" H 2525 1725 50  0001 C CNN
	1    2525 1725
	0    1    1    0   
$EndComp
Wire Wire Line
	2675 1725 2800 1725
Wire Wire Line
	2225 1725 2375 1725
$Comp
L Connector:TestPoint TP1
U 1 1 5E0C54F3
P 2800 1725
F 0 "TP1" H 2742 1751 50  0000 R CNN
F 1 "3.3VPU" H 2742 1842 50  0000 R CNN
F 2 "LTD_Customized:test_pad" H 3000 1725 50  0001 C CNN
F 3 "~" H 3000 1725 50  0001 C CNN
	1    2800 1725
	-1   0    0    1   
$EndComp
Connection ~ 2800 1725
Wire Wire Line
	2800 1725 3125 1725
NoConn ~ 11600 7700
NoConn ~ 10650 7700
$Comp
L Connector_Generic:Conn_02x02_Counter_Clockwise J2
U 1 1 5E0CAEC9
P 14425 1450
F 0 "J2" H 14475 1667 50  0000 C CNN
F 1 "3.3V ISO" H 14475 1576 50  0000 C CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_2x02_P1.27mm_Vertical" H 14425 1450 50  0001 C CNN
F 3 "~" H 14425 1450 50  0001 C CNN
	1    14425 1450
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0166
U 1 1 5E0CCE15
P 14825 1425
F 0 "#PWR0166" H 14825 1275 50  0001 C CNN
F 1 "+3.3V" H 14840 1598 50  0000 C CNN
F 2 "" H 14825 1425 50  0001 C CNN
F 3 "" H 14825 1425 50  0001 C CNN
	1    14825 1425
	1    0    0    -1  
$EndComp
Wire Wire Line
	14725 1450 14825 1450
Wire Wire Line
	14825 1450 14825 1425
Wire Wire Line
	14725 1550 14825 1550
Wire Wire Line
	14825 1550 14825 1450
Connection ~ 14825 1450
Wire Wire Line
	14225 1450 14225 1550
Connection ~ 14225 1550
Text Notes 14175 1800 0    50   ~ 0
Note: Open this circuit to test \nthe power module individually.
$Comp
L power:+3.3VA #PWR0119
U 1 1 5E0D5C81
P 13750 1550
F 0 "#PWR0119" H 13750 1400 50  0001 C CNN
F 1 "+3.3VA" H 13765 1723 50  0000 C CNN
F 2 "" H 13750 1550 50  0001 C CNN
F 3 "" H 13750 1550 50  0001 C CNN
	1    13750 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	13750 1550 14075 1550
$Comp
L Connector:TestPoint TP2
U 1 1 5E0D8EC8
P 14075 1550
F 0 "TP2" H 14017 1576 50  0000 R CNN
F 1 "3.3V_OUT" H 14017 1667 50  0000 R CNN
F 2 "LTD_Customized:test_pad" H 14275 1550 50  0001 C CNN
F 3 "~" H 14275 1550 50  0001 C CNN
	1    14075 1550
	1    0    0    -1  
$EndComp
Connection ~ 14075 1550
Wire Wire Line
	14075 1550 14225 1550
$EndSCHEMATC
