# TECHNOLOGY FOR THE WELDER'S WORLD

|DE|EN|FR|ES|ZH|JA|
|---|---|---|---|---|---|
|1 Hauptplatine|Main PCB|Carte mère|Circuito integrado principal|主板|マザーボード|
|2 LED 3 Stk.|3 x LED|3 DEL|3 LED|LED 灯（3 个）|LED 3 pc|
|3 SD-Slot|SD slot|Port SD|Ranura SD|SD 卡槽|SD-Slot|
|4 Hauptschalter Q1|Main switch Q1|Interrupteur principal Q1|Interruptor principal Q1|总开关 Q1|メインスイッチ Q1|
---
# 1 Command overview

An SD card can be used to import firmware updates, program updates and bus mappings. The error memory and system information can also be read. A conventional SDHC card in FAT32 format is required. Write protection must not be activated.

# 2 Procedure

All the necessary files must be on the card. The process is managed using the script file ‘Script.txt’.

# NOTICE

- Do not switch off the eBOX or remove the SD card during a firmware update as the eBOX will otherwise no longer boot up and will need to be returned to the manufacturer.

# DANGER

Risk of injury due to unexpected start-up. The following instructions must be adhered to for the entire duration of maintenance, servicing, disassembly and repair work:

- Switch off the power source.
- Close the compressed air supply.
- Disconnect the mains plug.

1. Switch off the eBOX at the main switch (4) then use a key to open the housing cover.
2. Insert the SD card into the SD slot (3) until it clicks into place.
3. Switch on the eBOX at the main switch (4). All processes activated in the file ‘Script.txt’ are run through. A firmware update can take up to 5 minutes. During the update, the middle LED lights up yellow. Once the update is complete, the yellow LED goes out and the lower green LED flashes. If a transmission error occurs, the top status LED also lights up red.
4. Once the update is complete, remove the SD card again.
5. Switch the eBOX off and back on at the main switch (4). The eBOX restarts.

# 3 Setting the network parameters (IP address, subnet mask, DHCP)

From firmware version V4.1, the network IP address, subnet mask and DHCP enable/disable can be set using the SD card script.

|IP address|SETIPADR=192.168.0.199|
|---|---|
|Subnet mask|SETSUBNM=255.255.255.0|
|DHCP enable/disable|SETDHCP=0 0=disable, 1=enable|

Tab. 1 Creating the network parameters

EN - 2
---
# 4 Firmware updates

Once the axis controller firmware has been downloaded, the file MIOACHSCO_BOOT_SCRIPT.txt is written to the SD card. Once the multi I/O board firmware has been downloaded, the file MULTIIO_BOOT_SCRIPT.txt is written to the SD card. This prevents the firmware from being downloaded again after the hardware has been reset. Both the MIOACHSCO and the Multi I/O then conduct a hardware reset. To update the firmware again, you must delete the files ‘MIOACHSCO_BOOT_SCRIPT.txt’ and ‘MULTIIO_BOOT_SCRIPT.txt’ from the SD card. All the necessary data is provided by ABICOR BINZEL.

# 5 Explanation of the script commands

When the eBOX is turned on, a check is conducted to see if an SD card has been inserted. If this is the case the system searches for the file ‘Script.txt’. If this is found, the file is read line by line and the commands are sequentially processed. The file can be created and edited using Windows Notepad, for example. Each line must be completed with ENTER. All lines that start with a semi-colon are identified as comment lines and ignored when the script is processed.

EN - 3
---
# Explanation of the script commands

|Process|Command|Explanation|Example|
|---|---|---|---|
|Loading|SALOAD|The stand-alone program is loaded to the multi I/O memory from the SD card.|SALOAD=eBOX_BUS_v100_PP_SF10_500_MF30_300_5W.PSQ|
|ABMAPPING|The bus mapping is loaded from the SD card. The file in which the mapping is stored is specified after the equals sign.|ABMAPPING=testmapping.map| |
|Firmware update for|MIOACHSCOFWUPDATE|The firmware for a MioAchsCo axis controller is updated. The command is followed by a blank space and then the file name of the Intel-Hex file, a further blank space and then the build number. The Intel-Hex file and boot loader file ‘MIOACHSCO_BOOT.hex’ must both be on the SD card. The firmware version can be seen from the build number.|MIOACHSCOFWUPDATE MIOACHSCO_V02_15_13032014.hex 1907622421|
|MULTIIOFWUPDATE|The firmware for a multi I/O card is updated. The command is followed by a blank space and then the file name of the Intel-Hex file, a further blank space and then the build number. The Intel-Hex file and boot loader file ‘MULTIIO_BOOT.hex’ must both be on the SD card. The firmware version can be seen from the build number.|MULTIIOFWUPDATE MultiIO_V37_17032014.hex 1907622421| |
|Saving the error memory|CPYERRFILE|The entire error memory is written to a file on the SD card. The file ‘ErrList.txt’ is created on the SD card. All error entries from the error memory are written in this file line by line.|CPYERRFILE|
|Deleting the error|ERRCLEAR|The entire error memory is erased.|ERRCLEAR|
|Writing system info to a file|SYSINFO|All system information is written in a file on the SD card. The file is called ‘SysInfo.txt’. Information about all firmware versions in the system (multi I/O, ADDA, MioAchsCo) is written to this file together with the stand-alone program version info, the current date and time, the operating hours counter, the Anybus module ID and the IP address.|SYSINFO|