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
L Device:R R1
U 1 1 5DE95E56
P 5160 3150
F 0 "R1" V 5070 3150 50  0000 C CNN
F 1 "4.7k" V 5160 3160 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5090 3150 50  0001 C CNN
F 3 "~" H 5160 3150 50  0001 C CNN
	1    5160 3150
	0    1    1    0   
$EndComp
$Comp
L Device:R R2
U 1 1 5DE96132
P 5620 3520
F 0 "R2" V 5530 3520 50  0000 C CNN
F 1 "47k" V 5620 3530 50  0000 C CNN
F 2 "Resistor_SMD:R_0805_2012Metric" V 5550 3520 50  0001 C CNN
F 3 "~" H 5620 3520 50  0001 C CNN
	1    5620 3520
	0    1    1    0   
$EndComp
Wire Wire Line
	5010 3150 4470 3150
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5DE992B3
P 4220 3250
F 0 "J1" H 4300 3242 50  0000 L CNN
F 1 "MCU_PWR_KEY" H 4300 3151 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 4220 3250 50  0001 C CNN
F 3 "~" H 4220 3250 50  0001 C CNN
	1    4220 3250
	-1   0    0    1   
$EndComp
Wire Wire Line
	4420 3250 4470 3250
Connection ~ 4470 3150
Wire Wire Line
	4470 3150 4420 3150
Wire Wire Line
	4470 3150 4470 3250
Wire Wire Line
	5890 3350 5890 3520
Wire Wire Line
	5890 2950 5890 2800
Wire Wire Line
	5890 2800 5890 2700
Wire Wire Line
	5890 3520 5770 3520
Connection ~ 5890 2800
$Comp
L Connector_Generic:Conn_01x02 J2
U 1 1 5DE9446F
P 6090 2700
F 0 "J2" H 6170 2692 50  0000 L CNN
F 1 "M_PWR_KEY" H 6170 2601 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 6090 2700 50  0001 C CNN
F 3 "~" H 6090 2700 50  0001 C CNN
	1    6090 2700
	1    0    0    -1  
$EndComp
$Comp
L Transistor_BJT:MMBT3904 Q1
U 1 1 5DE93157
P 5790 3150
F 0 "Q1" H 5981 3196 50  0000 L CNN
F 1 "MMBT3904" H 5981 3105 50  0000 L CNN
F 2 "Package_TO_SOT_SMD:SOT-23" H 5990 3075 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N3904.pdf" H 5790 3150 50  0001 L CNN
	1    5790 3150
	1    0    0    -1  
$EndComp
Wire Wire Line
	5310 3150 5470 3150
Wire Wire Line
	5470 3520 5470 3150
Connection ~ 5470 3150
Wire Wire Line
	5470 3150 5590 3150
$Comp
L Connector_Generic:Conn_01x02 J3
U 1 1 5DEA0D85
P 6150 3690
F 0 "J3" H 6230 3682 50  0000 L CNN
F 1 "M_GND" H 6230 3591 50  0000 L CNN
F 2 "Connector_PinHeader_1.27mm:PinHeader_1x02_P1.27mm_Vertical" H 6150 3690 50  0001 C CNN
F 3 "~" H 6150 3690 50  0001 C CNN
	1    6150 3690
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 3790 5890 3790
Wire Wire Line
	5890 3790 5890 3690
Connection ~ 5890 3520
Wire Wire Line
	5950 3690 5890 3690
Connection ~ 5890 3690
Wire Wire Line
	5890 3690 5890 3520
Text Label 4470 3150 0    50   ~ 0
MCU_PWR_KEY
Text Label 5890 2620 0    50   ~ 0
M_PWR_KEY
Wire Wire Line
	5890 2620 5890 2700
Connection ~ 5890 2700
Text Label 5890 3520 0    50   ~ 0
M_GND
$EndSCHEMATC
