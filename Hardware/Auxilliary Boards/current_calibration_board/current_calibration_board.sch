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
$Comp
L Connector_Generic:Conn_01x03 J1
U 1 1 5DB2157D
P 3125 1475
F 0 "J1" H 3205 1517 50  0000 L CNN
F 1 "Vcc_Conn" H 3205 1426 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x03_P1.27mm_Vertical" H 3125 1475 50  0001 C CNN
F 3 "~" H 3125 1475 50  0001 C CNN
	1    3125 1475
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5DB21A6D
P 3125 2025
F 0 "J2" H 3205 2067 50  0000 L CNN
F 1 "Vcc_Conn" H 3205 1976 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x03_P1.27mm_Vertical" H 3125 2025 50  0001 C CNN
F 3 "~" H 3125 2025 50  0001 C CNN
	1    3125 2025
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x04 J3
U 1 1 5DB21D2A
P 3125 2625
F 0 "J3" H 3205 2617 50  0000 L CNN
F 1 "GND_Conn" H 3205 2526 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x04_P1.27mm_Vertical" H 3125 2625 50  0001 C CNN
F 3 "~" H 3125 2625 50  0001 C CNN
	1    3125 2625
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5DB2358B
P 2775 2975
F 0 "#PWR0101" H 2775 2725 50  0001 C CNN
F 1 "GND" H 2780 2802 50  0000 C CNN
F 2 "" H 2775 2975 50  0001 C CNN
F 3 "" H 2775 2975 50  0001 C CNN
	1    2775 2975
	1    0    0    -1  
$EndComp
Wire Wire Line
	2775 2975 2775 2825
Wire Wire Line
	2775 2525 2925 2525
Wire Wire Line
	2925 2625 2775 2625
Connection ~ 2775 2625
Wire Wire Line
	2775 2625 2775 2525
Wire Wire Line
	2925 2725 2775 2725
Connection ~ 2775 2725
Wire Wire Line
	2775 2725 2775 2625
Wire Wire Line
	2925 2825 2775 2825
Connection ~ 2775 2825
Wire Wire Line
	2775 2825 2775 2725
$Comp
L power:+3.3V #PWR0102
U 1 1 5DB239DD
P 2750 1275
F 0 "#PWR0102" H 2750 1125 50  0001 C CNN
F 1 "+3.3V" H 2765 1448 50  0000 C CNN
F 2 "" H 2750 1275 50  0001 C CNN
F 3 "" H 2750 1275 50  0001 C CNN
	1    2750 1275
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0103
U 1 1 5DB244EB
P 2750 1850
F 0 "#PWR0103" H 2750 1700 50  0001 C CNN
F 1 "+3.3V" H 2765 2023 50  0000 C CNN
F 2 "" H 2750 1850 50  0001 C CNN
F 3 "" H 2750 1850 50  0001 C CNN
	1    2750 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	2750 1850 2750 1925
Wire Wire Line
	2925 2025 2750 2025
Wire Wire Line
	2925 1925 2750 1925
Connection ~ 2750 1925
Wire Wire Line
	2750 1925 2750 2025
Wire Wire Line
	2925 1375 2750 1375
Connection ~ 2750 1375
Wire Wire Line
	2750 1375 2750 1275
Wire Wire Line
	2925 1475 2750 1475
Wire Wire Line
	2750 1475 2750 1375
NoConn ~ 2925 1575
NoConn ~ 2925 2125
$Comp
L Device:R R1
U 1 1 5DB26DC7
P 5675 2175
F 0 "R1" V 5725 2025 50  0000 C CNN
F 1 "165" V 5675 2175 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric_Pad1.15x1.40mm_HandSolder" V 5605 2175 50  0001 C CNN
F 3 "~" H 5675 2175 50  0001 C CNN
	1    5675 2175
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_01x08 J5
U 1 1 5DB27785
P 4975 2575
F 0 "J5" H 4893 1950 50  0000 C CNN
F 1 "Conn_01x08" H 4893 2041 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical" H 4975 2575 50  0001 C CNN
F 3 "~" H 4975 2575 50  0001 C CNN
	1    4975 2575
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 5DB2B825
P 6050 3000
F 0 "#PWR0104" H 6050 2750 50  0001 C CNN
F 1 "GND" H 6055 2827 50  0000 C CNN
F 2 "" H 6050 3000 50  0001 C CNN
F 3 "" H 6050 3000 50  0001 C CNN
	1    6050 3000
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0105
U 1 1 5DB2E4AA
P 3950 2100
F 0 "#PWR0105" H 3950 1950 50  0001 C CNN
F 1 "+3.3V" H 3965 2273 50  0000 C CNN
F 2 "" H 3950 2100 50  0001 C CNN
F 3 "" H 3950 2100 50  0001 C CNN
	1    3950 2100
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 2100 3950 2150
Wire Wire Line
	3950 2150 4125 2150
$Comp
L Connector_Generic:Conn_01x03 J4
U 1 1 5DB2D465
P 4325 2250
F 0 "J4" H 4405 2292 50  0000 L CNN
F 1 "Vcc_Conn" H 4405 2201 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 4325 2250 50  0001 C CNN
F 3 "~" H 4325 2250 50  0001 C CNN
	1    4325 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4125 2250 3950 2250
Wire Wire Line
	3950 2250 3950 2150
Connection ~ 3950 2150
Wire Wire Line
	4125 2350 3950 2350
Wire Wire Line
	3950 2350 3950 2250
Connection ~ 3950 2250
$Comp
L Device:R R2
U 1 1 5DB3133A
P 5675 2275
F 0 "R2" V 5725 2100 50  0000 C CNN
F 1 "68" V 5675 2275 50  0000 C CNN
F 2 "Resistor_SMD:R_1206_3216Metric_Pad1.42x1.75mm_HandSolder" V 5605 2275 50  0001 C CNN
F 3 "~" H 5675 2275 50  0001 C CNN
	1    5675 2275
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 5DB38CC0
P 5675 2375
F 0 "R3" V 5725 2200 50  0000 C CNN
F 1 "33" V 5675 2375 50  0000 C CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 5605 2375 50  0001 C CNN
F 3 "~" H 5675 2375 50  0001 C CNN
	1    5675 2375
	0    1    1    0   
$EndComp
Wire Wire Line
	6050 3000 6050 2875
Wire Wire Line
	6050 2175 5825 2175
Wire Wire Line
	5825 2275 6050 2275
Connection ~ 6050 2275
Wire Wire Line
	6050 2275 6050 2175
Wire Wire Line
	5825 2375 6050 2375
Connection ~ 6050 2375
Wire Wire Line
	6050 2375 6050 2275
Wire Wire Line
	5525 2175 5175 2175
Wire Wire Line
	5525 2275 5175 2275
Wire Wire Line
	5175 2375 5525 2375
$Comp
L Device:R R4
U 1 1 5DB3C5C7
P 5675 2475
F 0 "R4" V 5725 2300 50  0000 C CNN
F 1 "22" V 5675 2475 50  0000 C CNN
F 2 "Resistor_SMD:R_1210_3225Metric_Pad1.42x2.65mm_HandSolder" V 5605 2475 50  0001 C CNN
F 3 "~" H 5675 2475 50  0001 C CNN
	1    5675 2475
	0    1    1    0   
$EndComp
$Comp
L Device:R R5
U 1 1 5DB3E8FD
P 5675 2575
F 0 "R5" V 5725 2400 50  0000 C CNN
F 1 "16.5" V 5675 2575 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" V 5605 2575 50  0001 C CNN
F 3 "~" H 5675 2575 50  0001 C CNN
	1    5675 2575
	0    1    1    0   
$EndComp
$Comp
L Device:R R6
U 1 1 5DB3FC49
P 5675 2675
F 0 "R6" V 5725 2500 50  0000 C CNN
F 1 "13.3" V 5675 2675 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" V 5605 2675 50  0001 C CNN
F 3 "~" H 5675 2675 50  0001 C CNN
	1    5675 2675
	0    1    1    0   
$EndComp
$Comp
L Device:R R7
U 1 1 5DB41849
P 5675 2775
F 0 "R7" V 5725 2600 50  0000 C CNN
F 1 "11" V 5675 2775 50  0000 C CNN
F 2 "Resistor_SMD:R_2512_6332Metric_Pad1.52x3.35mm_HandSolder" V 5605 2775 50  0001 C CNN
F 3 "~" H 5675 2775 50  0001 C CNN
	1    5675 2775
	0    1    1    0   
$EndComp
$Comp
L Device:R R8
U 1 1 5DB42DCD
P 5675 2875
F 0 "R8" V 5725 2700 50  0000 C CNN
F 1 "5.6" V 5675 2875 50  0000 C CNN
F 2 "LTD_Customized:Resistor_SMD_1225_2W" V 5605 2875 50  0001 C CNN
F 3 "~" H 5675 2875 50  0001 C CNN
	1    5675 2875
	0    1    1    0   
$EndComp
Wire Wire Line
	5525 2475 5175 2475
Wire Wire Line
	5175 2575 5525 2575
Wire Wire Line
	5525 2675 5175 2675
Wire Wire Line
	5175 2775 5525 2775
Wire Wire Line
	5525 2875 5175 2875
Wire Wire Line
	5825 2875 6050 2875
Connection ~ 6050 2875
Wire Wire Line
	6050 2875 6050 2775
Wire Wire Line
	6050 2775 5825 2775
Connection ~ 6050 2775
Wire Wire Line
	6050 2775 6050 2675
Wire Wire Line
	5825 2675 6050 2675
Connection ~ 6050 2675
Wire Wire Line
	6050 2675 6050 2575
Wire Wire Line
	6050 2575 5825 2575
Connection ~ 6050 2575
Wire Wire Line
	6050 2575 6050 2475
Wire Wire Line
	5825 2475 6050 2475
Connection ~ 6050 2475
Wire Wire Line
	6050 2475 6050 2375
Text Notes 3150 3850 0    50   ~ 0
Note: do not solder the 1x8 pin header, just use the probe of the \ncurrent meter to short circuit the 2.54 mm connector. The reading\nof the current meter is the ground truth.
$Comp
L Connector_Generic:Conn_01x03 J6
U 1 1 5DB56E5C
P 4325 2825
F 0 "J6" H 4405 2867 50  0000 L CNN
F 1 "GND_Conn" H 4405 2776 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 4325 2825 50  0001 C CNN
F 3 "~" H 4325 2825 50  0001 C CNN
	1    4325 2825
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0106
U 1 1 5DB591BC
P 4000 3075
F 0 "#PWR0106" H 4000 2825 50  0001 C CNN
F 1 "GND" H 4005 2902 50  0000 C CNN
F 2 "" H 4000 3075 50  0001 C CNN
F 3 "" H 4000 3075 50  0001 C CNN
	1    4000 3075
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 3075 4000 2925
Wire Wire Line
	4000 2725 4125 2725
Wire Wire Line
	4125 2825 4000 2825
Connection ~ 4000 2825
Wire Wire Line
	4000 2825 4000 2725
Wire Wire Line
	4125 2925 4000 2925
Connection ~ 4000 2925
Wire Wire Line
	4000 2925 4000 2825
$EndSCHEMATC
