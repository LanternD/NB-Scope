# Important Note

- The majority of the modules here can be soldered by hand, except Quectel BG96 and uBlox SARA-R410M-02B.
  - If you solder the SARA-R410M-02B **by yourself** (customizing the stencil and applying the solder paste), instead of using the SMT service, you need to shrink the size of all the pads of the SARA-R410M-02B footprint! Otherwise they are likely to get short-circuited.
  - Before
  ![SARA footprint before](../assets/sara_pad_size_before.png)
  - After
  ![SARA footprint after](../assets/sara_pad_size_after.png)
  
- All the shieldboards have a RESET button for the module.
- This a design compatibility issue in those modules with a "PWR_KEY" pin, including SARA-R410M-02B, BG96, BC26, and BC66. The pin requires an open collector transistor to enable, which I use different hardware designs to take care of it across different version of the board. Here is the summary:
  - Node mainboard v3.2 + BC26/BC66/SARA shieldboard: no modification needed.
  - Node mainboard v3.2 + SARA shieldboard: use GPIO_L4 as the `PWRKEY` control pin.
  - Node mainboard v3.1 + BC26/BC66/BG96 shieldboard: need to fixed by the `pwr_key_addon` in "Auxilliary Boards" folder. (**Highly unrecommended**)
  - Node mainboard v3.1 + SARA shieldboard: use GPIO_L4 as the `PWRKEY` control pin. (**Highly unrecommended**)

# Photos

## Quectel BC26 (BC66) Shieldboard

![BC26 Shiledboard](../assets/bc26_bc66_module_board.png)
![BC26 Shiledboard](../assets/bc26_bc66_module_board_B.png)

Note: BC66 is almost identical to BC26 board, except for the swap between UART Tx and Rx pin.

## Quectel BC28 Shieldboard

![BC28 Shiledboard](../assets/bc28_module_board.png)
![BC28 Shiledboard](../assets/bc28_module_board_B.png)

## Quectel BC95/BC35 Shieldboard

![BC95 Shiledboard](../assets/bc95_bc35_module_board.png)
![BC95 Shiledboard](../assets/bc95_bc35_module_board_B.png)

## Gosuncn ME3616 Shieldboard

![ME3616 Shiledboard](../assets/me3616_module_board.png)
![ME3616 Shiledboard](../assets/me3616_module_board_B.png)

## Quectel BG96/BG36 Shieldboard

![BG96 Shiledboard](../assets/bg96_module_board.png)
![BG96 Shiledboard](../assets/bg96_module_board_B.png)

## uBlox SARA-R410M-02B Shieldboard

![SARA Shiledboard](../assets/sara_r410m_02b_module_board_v2.0.png)
![SARA Shiledboard](../assets/sara_r410m_02b_module_board_v2.0_B.png)
