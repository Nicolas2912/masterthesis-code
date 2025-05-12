# TECHNOLOGY FOR THE WELDER'S WORLD.

# DE Betriebsanleitung / EN Operating instructions

# MFS-V3

# DE Service Software

# EN Service software

# ZERIZI

# TFIERTES

# DIN EN

# ISO 9001M

# QM-SYSET

www.binzel-abicor.com
---
# MFS service software

EN        English Translation of the original operating instructions

© The manufacturer reserves the right, at any time and without prior notice, to make such changes and amendments to these operation Instructions which may become necessary due to misprints, inaccuracies or improvements to the product. Such changes will however be incorporated into subsequent editions of the Instructions. All trademarks mentioned in the operating instructions are the property of their respective owners. All brand names and trademarks that appear in this manual are the property of their respective owners/manufacturers. To obtain contact data for the ABICOR BINZEL representative or partner in a specific country, please visit our homepage www.binzel-abicor.com.

# 1 Identification

EN-3

# 2 Areas of application

EN-3

# 3 System requirements

EN-3

# 4 Connecting the eBOX to a PC

EN-4

# 5 Installing the software

EN-5

# 5.1 Software installation settings for Windows 7

EN-8

# 5.2 Software installation settings for Windows XP

EN-10

# 6 Configuring the driver

EN-12

# 7 Starting the software

EN-14

# 8 User levels/user rights

EN-15

# 9 Setting up the software

EN-16

# 9.1 Device type settings

EN-16

# 9.2 Connection type settings

EN-16

# 9.3 Ethernet IP address (only in connection with Profinet-controlled MFS-V2 systems)

EN-17

# 9.4 Ethernet option with the device type MFS-V3

EN-17

# 9.5 CAN bus (only in conjunction with MF control)

EN-18

# 9.6 Testing the connection

EN-18

# 9.7 Channel visualisation monitoring settings, user level 1

EN-19

# 9.8 Channel visualisation monitoring settings, user level 2

EN-20

# 9.9 Drive, gear reduction, encoder and measuring wheel monitoring settings, user level 2

EN-24

# 9.10 Start/stop trigger monitoring settings, user level 2

EN-25

# 9.11 Log file path monitoring settings, user level 2

EN-26

# 9.12 Process data display settings, user level 2

EN-27

# 9.13 Signal description IO settings, user level 2

EN-28

# 9.14 Signal description Dig IO settings, user level 2

EN-30

# 9.15 Device type settings

EN-31

# 9.15.1 eBOX (MFS-V3 only)

EN-31

# 9.16 Service interval settings (MFS-V3 only)

EN-32

EN - 2
---
# MFS service software

# 1 Identification

These printed instructions provide support with the installation, configuration and setup of the service software for master feeder systems.

The latest version can be downloaded from our FTP server:

|FTP server|94.137.159.242|
|---|---|
|User|binzel_mfs|
|Password|download|

- Please use a suitable FTP client.
- Enter these details and click ‘Connect’.

# 2 Areas of application

The visualisation and monitoring of processes and equipment in the welding and brazing industry is becoming increasingly important. This software acts as a visualisation and analysis system for all process parameters and data relevant to the master feeder systems MFS-V2 and MFS-V3.

Data is requested and graphically displayed via the Ethernet and USB interfaces. The software offers the following functions:

- Visualisation of actual values
- Visualisation of eBOX inputs and outputs
- Component and seam-specific archiving of the actual values for the process
- Visualisation of target values
- Threshold value monitoring and display
- Nonconformity and event logs
- Data export to Microsoft Excel
- Diagnosis
- Presentation of maintenance intervals or messages
- Job functionality for up to 64 jobs (MFS-V3 only)

This software is a useful tool for documenting process parameters in areas where process results must be precisely reproduced. During operation, the software detects when threshold values have been exceeded and displays this on the screen.

Recording and displaying data during process optimisation helps to set up a system during maintenance and servicing. For example, the values displayed can indicate whether the system needs to be cleaned or whether resistors are impeding wire feeding from the wire feed roll.

# 3 System requirements

|PC (laptop) with processor|At least Pentium III (500 MHz)|
|---|---|
|Main memory|At least 64 MB RAM|
|Memory requirement|100 MB min.|
|Operating system|Microsoft Windows|
| |- Windows 7|
| |- XP|

NOTICE

- The software can be used on all of the listed operating systems.
- Administrator rights are required.
---
# 4 Connecting the eBOX to a PC

# MFS service software

|Software|Microsoft Excel (for importing CSV files)|
|---|---|
|Connection|At least one free USB interface or Ethernet port|
|eBOX MFS-V2|Firmware version 6.5 or above|
|eBOX MFS-V3|Firmware version 5.0 or above|

# NOTICE

- The following steps must only be completed by qualified personnel (in Germany, see TRBS 1203).
- Observe the safety regulations in the operating instructions for the individual components.
- Note that, with older MFS V2 eBOXes, there is a risk of identifying the service interface incorrectly on the hand-held unit.
- eBOXes with a serial number &lt; E0051 are not suitable for this software and may damage the hardware (USB converter).

There are three ways of establishing a connection between the eBOX and a PC:

1. USB/RS converter (881.3220.1) required (eBOX MFS-V2 only)
- Switch off the eBOX and disconnect it from the mains.
- Connect the RS interface converter to the SERVICE connection bush on the eBOX.
- Connect the converter to the PC via a USB port.
- Connect the eBOX to the mains power supply.
- Switch on the eBOX.
2. Connection via Ethernet (eBOX MFS-V3 and eBOX MFS-V2 with Profinet only)
- Switch on the eBOX.
- Establish a connection between the eBOX and PC using an Ethernet patch cable.
- Connect to the mains.
3. Connection via CAN (eBOX MFS-V3 with hand terminal MF control only)
- Connect the MF control to the eBOX (X10 hand terminal).
- Switch on the eBOX.

The MF control comes with Windows 7 Embedded and boots as soon as the eBOX is switched on.

# NOTICE

- To prevent data losses, always properly shut down the MF control operating system before disconnecting the X10 plug or switching off the eBOX.
---
# MFS service software

# 5 Installing the software

# Description

|• Start the file using ‘Abicor_Binzel_Service_Software_Setup.exe’.| | | |
|---|---|---|---|
|• Select a language.|Sprachenauswahl| | |
| |Bitte wahlen Sie eine Sprache aus, die fur den Installationsvorgang benutzt werden soll.| | |
| |Abbrechen| | |
|• Click ‘Next’.|MFS Service Software Setup| | |
| |Software Setup Wizard| | |
| |Welcome to the MFS Service| | |
| |This instal MFS Service Software 6.3 on your computer It is recommended that You close other applications before continuing: Click Next to continue.| | |
| |Next|Cancel| |
|• Accept the terms of the license agreement and click ‘Next’.| | | |
| |MFS Service Software Setup| | |
| |License Agreement| | |
| |Read the following important information before continuing:| | |
| |Please read the following License Agreement. YOU must accept the terms of this agreement before continuing with the installation.| | |
| |License of Alexander Binzel Schweibtechnik GmbH & Co, KG| | |
| |Copyright -| | |
| |Copyright (c) ABICOR Binzel Alexander Binzel Schweibtechnik GmbH & Co. KG| | |
| |All rights reserved.| | |
| |Redistribution and use permitted provided that the following conditions are met:| | |
| |Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.| | |
| |do not accept the agreement| | |
| |Back|Next|Cancel|

# NOTICE

• The software settings and user data are stored in the user directory as they do not require administrator rights.
---
# 5 Installing the software

# MFS service software

|Description|Screenshot| | | |
|---|---|---|---|---|
|The target directory is displayed. Click ‘Next’.| | | | |
|On Windows XP systems, the data is stored at the following path:| | | | |
|C:\Documents and Settings\All Users\| | | | |
|Application Data\MFS_SERVICE_SOFTWARE_DATA| | | | |
|On Windows 7 systems, the data is stored at the following path:| | | | |
|C:\ProgramData\MFS_SERVICE_SOFTWARE_| | | | |
|DATA| | | | |
|Setup will install MFS Service Software the folder shown below.| | | | |
|To continue, click Next. If you would like to select a different folder, click Browse.| | | | |
| |Destination Folder|Abicor Binzel MFS Service Software| | |
| |Required free space:|35.1 MB| | |
| |Available free space:|80.9 GB| | |
| | |Back|Next|Cancel|

# MFS Service Software Setup

You are asked whether a desktop icon should be created and the program should be added to the Start menu. Click ‘Next’.

# Select Additional Tasks

Which additional tasks should be performed?

Select the additional tasks you would like setup to perform while installing MFS Service Software, then click Next.

- Create desktop icon
- Create start menu folder

# MFS Service Software Setup

The software is installed.

# Installing

Please wait while Setup installs MFS Service Software on your computer.

Installing:

C: Abicor Binzel MFS Service Software HELP_MFSV3ISERR_16_DEjpg

Back

Next

Cancel
---
# MFS service software

# 5 Installing the software

Description

ScreenshotYou can choose if the software should be started after completion. Click ‘Finish’.MFS Service Software SetupCompleting the MFS Service Software Setup WizardSetup has finished installing MFS Service Software on your computer. Click Finish - next Setup.Launch MFS Service SoftwareThe software installation is now complete. The shortcut to the start file appears on the desktop.MFS_Service_SoftwareOnce installation is complete, a text file with notes on the USB driver installation appears. This driver is only required if an eBOX V2 is connected via a USB converter. This file can also be opened via the entry in the Start menu.
---
# 5 Installing the software

# MFS service software

# 5.1 Software installation settings for Windows 7

|Description|Screenshot| | | |
|---|---|---|---|---|
|• Right-click the software icon on your desktop.|Eigenschaften von MFS Service Software Erweiterte Eigenschaften| | | |
|• Click: Settings/Properties/Advanced.| | | | |
|• Select the ‘Run as administrator’ checkbox.| | | | |
|• Click ‘OK’.| | | | |
|• Connect the USB converter and cable (eBOX MFS-V2 only).| | | | |
|• Connect the D-sub cable from the converter to the X49 serial interface in the direction of the eBOX as well as the USB cable to the PC.| | | | |
|• Connect to the Ethernet (eBOX MFS-V3 or MFS-V2 with Profinet only).| | | | |
|• Insert the D-sub cable from the converter into the USB interface. The device manager indicates whether hardware has been detected.| | | | |

# Gerate-Manager

|Datei|Aktion|Ansicht|
|---|---|---|
|NB-Weber|Akkus|Io Andere Gerate|
|FT23ZR USB UART|Anschluzse (COM & LPT)|Communications Port (COM1)|
|Printer Port (LPT1)|Audio-, Video- und Gamecontroller|Bildverarbeitungsgerate|
|Computer|DVDICD-ROM-Laufwerke|Grafikkarte|
|IDE ATNATAP]-Controller|Laufwerke|Mauze und andere Zeigegerate|
|Monitore|Netzwerkadapter|Prozessoren|
|Smartcard-Leser|Systemgerate|astaturen|
|USB-Controller| | |
---
# MFS service software

# 5 Installing the software

Description

• If the hardware has not been detected, re-install the driver manually. The driver file is located in the installation directory that was either adopted from the default settings or defined manually.

Example

Successful installation of the driver software and automatic detection of COM3.

|Gerate-Manager|Datei|Aktion|Ansicht|
|---|---|---|---|
|NB-!|Treiberzofnware aktualisieren FT232R USB UART|Auf dem Computer nach Treibersoftware such Ordner suchen|wahlen Sie den Ordner, Cer d e Treiber fur die|
|An diezem Ort nach Treibersoftware suchen:|C: Userslweber Downloadsl OKWBEO4L1OG_tcm3-1570301|C: Userslweber Downloadsl OKWBEO4L1OG_tcm3-1570301|C: Userslweber Downloadsl OKWBEO4L1OG_tcm3-1570301|
|Programme|Unterordner einbeziehen|Programme 626)|Abicor Binzel Service Software|
|Documents|Driver MFS USB Adapter|amds-|aus einer Liste von Geratetreibern auf de|
|Dieze Liste enthalt installierte Treibersoftware; die mit|Driver MFS USB Adzpter|aus derselben Kategorie stamnen;|Ordner:|
|Abbrechen|Weiter|Abbrechen| |
---
# 5 Installing the software

# MFS service software

# 5.2 Software installation settings for Windows XP

Description

|• Connect the USB converter. The wizard for finding new hardware appears.|Assistent für das Suchen neuer Hardware|
|---|---|
| |Willkommen|
| |Computer, auf der Hardwareinstallations-CD oder auf der|
| |Ec wird nach aklue #und aktualisierter Software auf dem|
| |Windows Update (mit Ihrer Erlaubnis) gesucht|
| |Soll eine Verbindung mit Windows Update hergestellt werden;|
| |um nach Scitwaje Zusuchen?|
| |Ja mu deseene Mal|
| |Ja undjeces Mal wenn ein Gerät angeschlossen wird|
| |Nein desmalncht|
| |Klicken Sie auf "Weiter", um den Vorgang fortzusetzen:|
| |~Zujuck Weiter > Abbrechen|

• Select: ‘No, not this time’ and click ‘Next’.

• Select ‘Install software from a list or a given source’ and click ‘Next’.

|Assistent für das Suchen neuer Hardware|Hardwarekomponenten installieren:|
|---|---|
| |Mit diesem Assistenten können Sie Software für die folgende|
| |FTz3ZR USB UaRT|
| |Falls die Hardwarekomponente mit einer CD oder Diskette geliefert wurde, legen Sie diese jetzt ein:|
| |Wie möchten Sie vorgehen?|
| |Software automatisch installieren (empfohlen)|
| |Software von einer Liste oder bestimmten Quelle installieren (für fortgeschrittene Benutzer)|
| |Klicken Sie auf "Weiter", um den Vorgang fortzusetzen:|
| |Zuiick Weiter > Abbrechen|

• Select the path shown.

|Ordner suchen|wählen Sie den Ordner, der die Treiber für die Hardwarekomponente enthält,|
|---|---|
|7-Zip|Abicor Binzel Service Software/Driver|
|Documents|USB Adapter|
|Driver|Speedo|
|Adobe|AS_PZW|
| |Klicken Sie auf ein Pluszeichen, um Unterordner anzuzeigen,|
| |Abbrechen|

• Confirm by clicking ‘OK’.
---
# MFS service software

# 5 Installing the software

# Description

- Click ‘Next’ and confirm all of the following windows with ‘Next’ or ‘Finish’.

# Screenshot

Assistent für das Suchen neuer Hardware

Wählen Sie die Such- und Installationsoptionen

Diese Quellen nach dem zutreffendsten Treiber durchsuchen

Verwenden Sie die Kontrollkästchen um die Standardsuche zu erweitern oder einzuschränken. Lokale Treiber sind in der Standardsuche mit einbegriffen. Der zutreffendste Treiber wird installiert.

- Wechselmedien durchsuchen (Diskette, CD)
- Folgende Quelle ebenfalls durchsuchen: C:\Programme\Abicor Binzel\service Software Driver
- Durchsuchen
- Nicht suchen, sondern den zu installierenden Treiber selbst wählen

Verwenden Sie diese Option, um einen Gerätetreiber aus einer Liste zu wählen. Es wird nicht garantiert, dass der von Ihnen gewählte Treiber der Hardware am besten entspricht;

Zurück          Weiter >          Abbrechen

EN - 11
---
# 6 Configuring the driver

Description

Screenshot• Open the device manager via the control panel.

4 Gerate-Manager

Datei Aktion Ansicht

CPU491

Anschlusse (COM und LPT)

Druckeranschluss (LPT1)

Kommunikationsanschluss (COM1)

USB Serial Port (COM6)

Kudio- video- und Gamecontroller

Batterien

Computer

DVDICD-ROM-Laufwerke

Eingabegerate (Human Interface Devices)

Grafikkarte

IDE ATAYATAPI-Controller

IEEE 1394 Bus-Hostcontroller

Infrarotgerate

Laufwerke

Mause und andere Zeigegerate

Modems

Monitore

Netzwerkadapter

PCMCIA- und Flash-Speichergerate

PCMCIA-Adapter

• Double-click the relevant USB port to configure the connection settings.

Eigenschaften von USB Serial Port (COM6)

Allgemein | Anschlusseinstellungen Treiber Details

Bits pro Sekunde: 38400

Datenbits:

Paritat: Keine

Stoppbits:

Flusssteuerung: Keine

Erweitert_ wiederherstellen Abbrechen

• Select the path shown.• Leave the other settings unchanged and click ‘Advanced’.
---
# MFS service software

# 6 Configuring the driver

|Description|Screenshot|
|---|---|
|• Use the ‘COM port number’ field to select the appropriate COM port (between 1 and 8).|Erweiterte Einstellungen für COM6|
|• Enter 1 in the ‘Latency (ms)’ field and confirm all windows by clicking ‘OK’.|COM-Anschlussnummer: COM6|
| |USB Packetgrößen|
|Reduzieren $2?d ? Werte Um Pertormance Probleme bei geringen Baudraten zu beheben;|Standard|
|Erhöhen Sie & 2 Werte für eine höhere Geschwindigkeit.| |
|Empfangen (Bytes):|4096|
|Senden (Bytes):|4096|
|BM Einstellungen|Allgemeine Optionen|
|Reduzieren S020 ? Werte, Um Kommunikationsprobleme Zu verringern;|PlugPlay Für serielle Schnittstelle|
|Wartezeit (ms):|Serielle Drucker|
|Abbrechen der Kommunikation; Wenn das Gerät ausgeschaltet wird| |
|Event bei unvorhergesehener Entfernung des Geräts| |
|Timeouts| |
|Minimale Anzahl der Lese-Timeouts (ms):| |
|Minimale Anzahl der Schreib-Timeouts (ms):| |

EN - 13
---
# 7 Starting the software

# MFS service software

# NOTICE

- You require administrator rights to start the software.

# Description

# Screenshot

• After starting the software, this window appears.

|Abicor Binze MFS Service Software|V6.4 16.09.2015|
|---|---|
|MFS Service-Software|MFS Service-Software|
|21.09.2015|07:38:37|

|Settings|Monitoring|Job Window|
|---|---|---|
|System Info|Load Log File|User Login|
|Minimize|Diagnosis|Signal Status In/Out|
|Connect|Disconnect|Quit|

BINZE

User Level

Not connected

EN - 14
---
# 8 User levels/user rights

NOTICE

• The software has three user levels.

# Description

User level 0 is freely accessible to all users.

User level 1 is password protected.

User level 2 is password protected and is used for configuration purposes by qualified personnel.

# User level 0

# User level 1

# User level 2

Screenshot

Abicor Binze MFS Service Software  User Login

V6.4 16.09.2015XEZ

User Login

21.09.2015 07:38:50

Home

User

User

User

Minimize

Change User Password

Back

# User Level 0

The software always starts in level 0 mode. At this level, it is only possible to start existing visualisation configurations or open existing log files. The Settings menu is hidden and it is not possible to create, load, change or save setups.

A password is required to access level 1. The initial password is ‘BiVisu’ and can be changed at any time.

The default password for level 1 can be reset by entering ‘RESETPW’ in the level 2 field. In level 1 mode, setup files can be loaded but not modified or saved.

In level 2 mode, all settings and parameters can be configured without any restrictions. This level is only intended for use by qualified personnel.

The password for this level is ‘MASTER’ and should only be given to qualified or trained specialists.

Further information about the options offered by the individual user levels plus more detailed explanations of these can be found in the ‘User levels and rights’ section of this manual.

15 Releasing the user levels and rights on page EN-58

EN - 15
---
# 9 Setting up the software

The following basic settings are required to properly operate the software. Please note the user levels required to configure these.

# 9.1 Device type settings

|Description|Screenshot|
|---|---|
|• Select the applicable system: MFS-V2 or MFS-V3.|User 2 Settings System Device Type|

# 9.2 Connection type settings

|Description|Screenshot|
|---|---|
|• Select the applicable connection type. Only possible if the device type is set to MFS-V2.|User Settings System Connection Type|
|COM port/USB • Configure the COM port as per the settings in the device manager.|Abicon Binzel MFS Service Software Settings System Connection Type V6.5 22.09.2015 XEZ Settings System Connection Type 20.10.2015 1409,05|

COM Port USB

COM-Port

CoM3

User Level 2

Not connected
---
# MFS service software

# 9 Setting up the software

# 9.3 Ethernet IP address (only in connection with Profinet-controlled MFS-V2 systems)

Description

- Ensure that the IP addresses of the PC and the eBOX are set correctly.
- Disable DHCP (automatically obtain IP address) and enter a fixed IP address (e.g. 192.168.0.3). The first three digits of the IP address have to be the same.

Screenshot

|Abicor Binze MFS Service Software|Settings|System Connection Type|
|---|---|---|
|V6.4 16.09.2015|XEZ|Settings System Connection Type|
|21.09.2015|07:50:54| |

MFSV2

|COM Port USB|Ethernet|
|---|---|
|IP-Adress|192.168.0.3|
| |Minimize|
| |Back|
| |IP List|
|User Level 2|Not connected|

# 9.4 Ethernet option with the device type MFS-V3

Description

- Ensure that the IP addresses of the PC and the eBOX are set correctly.
- Disable DHCP (see above – automatically obtain IP address) and enter a fixed IP address (e.g. 192.168.0.3). The first three digits of the IP address have to be the same.

The default IP address on delivery is: 192.168.0.3

Screenshot

|Abicor Binze MFS Service Software|Settings|System Connection Type|
|---|---|---|
|V6.4 16.09.2015|XEZ|Settings System Connection Type|
|21.09.2015|07:51:13| |

MFSV2

|COM Port USB|Ethernet|
|---|---|
|IP-Adress|192.168.0.3|
| |Minimize|
| |Back|
| |IP List|
|User Level 2|Not connected|

EN - 17
---
# 9 Setting up the software

# 9.5 CAN bus (only in conjunction with MF control)

Description

• Only select the CAN bus interface if using the MF control.

Screenshot
Abicor Binze MFS Service Software Settingsi SystemlConnection Type

V6.4 16.09.2015XEZ

Settings System Connection Type

21.09.2015 07:52:20

MFSV3

Home

Ethernet

CAN Bus

Minimize

Back

User Level 2

Not connected

# 9.6 Testing the connection

Description

• Click the button.

Screenshot
Connect Disconnect

Following a successful connection, this screen is displayed.

Text Anzeige

Actual Settings

Actual Slave Setup

Number Type Azis

ave MULTI-IO 9600

COH Ort COM1

Modul Address

TCP-Connection Setup

Actual Display

Enabled IP-Adress 192 168 0 . 3

Actual IQ Display Setup

Actual Trigger Setup

Actual Drive and Measuring Wheel Setup

Actual Description File

Schliessen Datei speichern

The connection status information is displayed at the bottom right of every screen.

If no connection is established, re-check all connection settings as necessary and ensure that the connection cables are properly inserted.

Possible error messages

FehlerMFS-Visu MessageFehler beim Sendenl6Connecting:Abbrechen
---
# MFS service software

# 9 Setting up the software

# 9.7 Channel visualisation monitoring settings, user level 1

Description

In user level 1 mode, only pre-configured setup files can be read by selecting ‘Load Setup File’. It is not possible to modify existing configurations or create new setup files.

|Screenshot|User|Settings|Monitoring|
|---|---|---|---|
|Abicor Binze MFS Service Software|Settings Monitoring|V6.4 16.09.2015|Settings Monitoring|
|21.09.2015|08.04.22| | |

Channel Visualisation

Specifies the number of channels displayed in the Monitoring window as well as their settings.

Drive, Gear Reduction, Encoder, Meas. Wheel

Used to set the parameters for the master drive.

Start/Stop Trigger

Stipulates the signal used to start/stop recording log files. Abicor Binzel provides ready-made records.

EN - 19
---
# 9 Setting up the software

# MFS service software

# 9.8 Channel visualisation monitoring settings, user level 2

NOTICE

- Setup files for monitoring purposes should only be created by qualified or trained specialists.
- Save all entries/changes made. Otherwise, these will be lost.

# Description

In user level 2 mode, pre-configured setup files can be read by selecting ‘Load Setup File’. It is possible to modify existing configurations or create new setup files. Eight user-defined channels are available. The motor current, amount of wire, actual wire speed, analog and digital inputs, frequency inputs and all register values can be selected. The configured settings are only applied once they have been saved using the parameter ‘Save Setup File’.

It is also necessary to adjust the value in the ‘Recording Time’ field to the length of the welding or brazing process. For example, if a wire feed duration of 26 seconds is required for a task, it is useful to set the value to 30 seconds so that the graphs are not displayed for an unnecessarily lengthy amount of time. The ‘Min. Cycle Time’ field stipulates the number of seconds after which a record should be saved as a log file. This is useful, for example, if the wire cutters are briefly started between the main cycles but this should not be logged. The ‘Y-Axis Division’ field specifies the number of vertical graphical divisions.

# Screenshot

| |User| |Settings|Monitoring| | | |
|---|---|---|---|---|---|---|---|
|Channel Visualisation|Abicor Binzel MFS Service Software|Settings Monitoring Channels| | | | | |
| | | | | |16.09.2015|Settings Monitoring Channels|21.09.2015 08:09:49|
|Channel1| | |Channel2|Channel3|Channel4| | |
| |Channel5| |Channel6|Channelz|Channel3| | |
| |Recording Time| | | |Minimize|sec| |
|Min. Cycle Time|sec|Y-Axis Division| | | | | |
| |User Level 2| | | | | | |
|Load Setup File|Save Setup File|Setup loaded from: S: WMFS V3eBOX Programmierung eBOX Systemspezifische Daten eBOX_V3_AD_VIftblunbet-Drive| | | | | |
---
# MFS service software

# 9 Setting up the software

|Description|Screenshot|
|---|---|
|Set the signal type and value ranges.|Channel Visualisation|

|Abicor Binze MFS Service Software|Settings Monitoring Channel|16.09.2015|XEZ|
|---|---|---|---|
|Settings Monitoring Channel 1|21.09.2015|08:12:12| |

|Signal Type|Number|Bit 0..7|
|---|---|---|
|Off| | |
|Signal Range|Minimum|Maximum|
|Status Indicator|Range from|To|
|User Level 2| |Not connected|

|Abicor Binze MFS Service Software|Settings Monitoring Channel|V6.4|16.09.2015|XEZ|
|---|---|---|---|---|
| |Settings Monitoring Channel 1|21.09.2015|08:12:31| |

|Signal Type|Number|Bit 0..7|
|---|---|---|
|Off| | |
|Motor Current [A]|Maximum| |
|add. Encoder Way [m]| | |
|add. Encoder Speed [ml/min]| | |
|Analog Input|To|Minimize|
|Frequency Input [0.1Hz]| | |
|Digital Input| | |
|Memory 8-Bit| | |
|Memory 16-Bit| | |
|Memory 24-Bit| | |
|Memory 8-Bit Single Bit| |Back|
|Memory 16-Bit Byte-Swap| | |
|User Level 2| |Not connected|

• Save the setup file.

|Touch File Dialog|Select Path and File|
|---|---|
|c: [|cI|
|Intel| |
|Master Pull| |
|Outlook-Archiv| |
|PerfLoas| |
|Save File|Monitoring.asp|
| |Zuruck|

EN - 21
---
# 9 Setting up the software

# MFS service software

|Description|Screenshot|
|---|---|
|• Enter the file name – the file extension is automatically added.||
|• Select a directory.| |

Once a setup file has been loaded, the enabled channels are indicated by a green check mark and the disabled ones by a red cross. The currently loaded setup file is displayed below the channels.

# Settings Monitoring Channels

16.09.2015 XEZ

Settings Monitoring Channels 21.09.2015 08:25.41

|Channel1|Channel2|Channel3|Channel4|
|---|---|---|---|
|Channel5|Channel6|Channelz|Channel3|

Recording Time sec

Min. Cycle Time sec

Y-Axis Division

User Level 2 Load

Setup File Save Setup File

Setup loaded from: S: WMFS V3eBOX Programmierung eBOX Systemspezifische Daten eBOX_V3_AD_VIftblunbet-Drive
---
# MFS service software

# 9 Setting up the software

Description

Set the signal type and value ranges.

• Save the setup file.

# Screenshot

|Abicor Binze MFS Service Software Einstellungen| Monitoring Kanal|ViOt 30,04,2015XEZ|Einstellungen Monitoring Kanal 1|04,05.2015 06.52:17|
|---|---|---|---|
|Signaltyp|Nummer|Bit 0..7|loff|
|Signalbereich|Minimum|Maximum|Status Anzeige|
|Bereich von|bis zu|Minimize|zuruck|
|Benutzerlevel 2|Nicht verbunden|Nicht verbunden|Nicht verbunden|

|Abicor Binze MFS Service Software Einstellungen| Monitoring Kanal|ViOt 30,04,2015XEZ|Einstellungen Monitoring Kanal 1|04,05.2015 06.52:35|
|---|---|---|---|
|Signaltyp|Nummer|Bit 0..7|Off|
|Motor Current [A]|Maximum|add. Encoder Way [m]|add. Encoder Speed [mlmin]|
|Analog Input|bis zu|Minimize|zuruck|
|Frequency Input [0.1Hz]|Digital Input|Memory 8-Bit|Memory 16-Bit|
|Memory 24-Bit|Memory 8-Bit Single Bit|Memory 16-Bit Byte-Swap| |
|Benutzerlevel 2|Nicht verbunden|Nicht verbunden|Nicht verbunden|

# Touch File Dialog

Pfad und Datei auswahlen

|c: [|CI|Bilder|
|---|---|---|
|Intel|Master Pull|Outlook-Archiv|
|c:l PerfLoas| |Datei speichern|
|asp| |Zuruck|

EN - 23
---
# 9 Setting up the software

# MFS service software

# 9.9 Drive, gear reduction, encoder and measuring wheel monitoring settings, user level 2

|Description|Screenshot|
|---|---|
|This area is used to set the parameters for the front drive.|User|
|Abicor Binzel|MFS Service Softwarel Settings Monitoring Drive; Gear Reduction; Encoder; Meas Wheel|
|16.09.2015XEZ|Settings Monitoring Drive, Gear Reduction; Encoder; Meas. Wheel|
|21.09.2015|08:27:03|

# Drive Parameters

|Diameter|20 mm|
|---|---|
|Encoder Line Count|Bo0|
|Gearbox Ratio|30 to|

# User Level 2

# Measuring Wheel Parameters

|Diameter|14 mm|
|---|---|
|Encoder Line Count|1024|

Home

Minimize

Back

Load

Setup File

Save Setup File

Setup File loaded S:WFS V3leBOX Programmierung eBOX Systemspezifische Daten eBOX_V3_AD_v1ubot epnrt2f-Drive_

EN - 24
---
# MFS service software

# 9 Setting up the software

# 9.10 Start/stop trigger monitoring settings, user level 2

|Description|Screenshot|
|---|---|
|Start/Stop Trigger|Abicor Binze MFS Service Software Settings Monitoring Start/Stop Trigger|
|16.09.2015|Settings Monitoring Start/Stop Trigger|
|21.09.2015|08:28:50|
|Visualisation Start|Visualisation Stop Trigger|
|Signal Type|Fieldbus Input|
|Number|Bit 0..7|
|Trigger Comparison Trigger Value|(rising Edge|
|Trigger Delay [ms]|1150|
|User Level 2|Load Setup File|
| |Save Setup File|
|Setup loaded from:|WFS V3leBOX Programmierung eBOX Systemspezifische Daten eBOX_V3_AD_v1ubot epnrt2f-Drive_|

# Example: Start Trigger

|Signal Type|Field bus Input|
|---|---|
|Number|0|
|Bit 0...7|Only relevant for single bit queries|
|Trigger Comparison|Increasing flank|
|Trigger Value|1|
|Trigger Delay [ms]|0 (Recording starts from the trigger once the specified delay period has passed)|

# Stop Trigger

|Signal Type|Field bus Input|
|---|---|
|Number|0|
|Bit 0...7|Only relevant for single bit queries|
|Trigger Comparison|Declining flank|
|Trigger Value|0|
|Trigger Delay [ms]|150 (Recording stops from the trigger once the specified delay period has passed)|

EN - 25
---
# 9 Setting up the software

# MFS service software

# 9.11 Log file path monitoring settings, user level 2

Description

Screenshot

|Log File Path|Abicor Binzel MFS Service Software Settings Monitoring|
|---|---|
|Version|V6.4 16.09.2015|
|Date|21.09.2015|
|Time|08.31:52|
|Path for Log Files|C:\Logfiles|
|IP Address|192.168.0.3|
|Minimize| |
|Select this path for log files| |
|Data Format|Ring Memory|
|Data Separator|Enable|
|Days until files will be deleted| |
|Back| |
|Apply| |

User Level 2

This window is used to set the path for saving log files. Select a folder path previously created in Windows and click ‘Select this path for log files’. If Ethernet communication takes place, a subfolder is automatically generated with the corresponding IP address in the path defined above.

Data Format stipulates the separator used for the CSV file to be created.

Ring buffer: If the ring buffer is enabled, all log data older than the specified number of days is deleted.

Click ‘Apply’ to save all the settings.

EN - 26
---
# MFS service software

# 9 Setting up the software

# 9.12 Process data display settings, user level 2

Beschreibung

The process data display is used to visualise the bus data for systems controlled using the field bus. A total of 64 channels are available for input and output data. This makes it possible to display the full bus mapping of the I/O data. Click the ‘Load Setup File’ button to read the preconfigured setup files.

# Example of the process data display

|User|Settings|Signal description|
|---|---|---|
|Abicor Binze MFS Service Software|Settings Proc Data Dispplay|connected with 192,168,200.225|
|V6.5 22.09.2015 XEZ|Settings Proc Data Dispplay|20.10.2015 14.23.42|

|Channel Proc Data|Data Type|Description|
|---|---|---|
|Process Data tput|Process Data Output| |
|eBOXNBAD process release|eBOX OUTB0syslem ready| |
|eBOXNBI ialze (error reset)|eBOX OUTBt1 n enor| |
|eBOXNB42 start vorward|eBOX OUTB72 process acive| |
|eBOXNB3 nching|eBOX OUTBI3 -| |
|eBOXNB44 start backward|eBOX OUTB4 wie speedis n window| |
|eBOXNBtS hot wire activete|eBOX OUTBts wie speedis window 2| |
|eBOXNB36 _|eBOX OUT B36| |
|eBOXNBAZ -|eBOX OUTBIZ wie avalabl| |
|eBOXNB78 _|eBOX OUTB78 conbrol cable connecied| |
|eBOXNBt9 -|eBOX OUTBt9 n motor controter eror| |
|eBOXNBXO _|eBOX OUTBXIO selectedjb i3 avatabl| |
|eBOXNBIIT|eBOX OUTBtTT wire movement acirve| |
|eBOXNBX12|eBOX OUTBX12| |
|eBOXNBt13 _|eBOX OUTBt13 &cis 0n| |
|eBOXNBX14-|eBOX OUTB414 hot wie power gource re| |
|eBOXNBt1S ~|eBOX OUTBt15 ~| |
|eBOXNBX16-|eBOX OUTBX16 _| |
|eBOXNBt1Z _|eBOX OUTBt1Z| |
|eBOXNBX18|eBOX OUTBX18| |
|eBOXNBt19|eBOX OUTBt19| |
|eBOX NBCo _|eBOX OUTB720 key swachis n &Ui0 mo| |
|eBOXNBZI operaing mode WI|eBOX OUTB721 ek operatng mode WT| |
|eBOXNB722 operaing mode W2|eBOX OUTB722 ack operatng mode W2| |
|eBOXNB23 operaing mode W4|eBOX OUTB723 eck operatng mode W4| |
|eBOXNByte3 selectedjb nunber|eBOX OUT Bytej chargedpb number| |
|eBOXNWord2 setvelue curenthot wi|eBOX OUT Word2| |
|eBOX N Word3|eBOX OUT Word3| |
|eBOX N Word4 setvelue wire speed|eBOX OUT Word4|velue wie speed|

EN - 27
---
# 9 Setting up the software

# MFS service software

# 9.13 Signal description IO settings, user level 2

|Description|Screenshot| | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
|Abicor Binzel MFS Service Software Settings Signal description V6.4 16.09.2015 XEZ| | | | | | | | | | | |
|Settings Signal description 21.09.2015 08:37:22| | | | | | | | | | | |
| | | | | | | | |Channel 1|Channel 2|Channel 3|Channel 4|
|Channel 5|Channel 6|Channel 7|Channel 8| | | | | | | | |
|Channel 9|Channel 10|Channel 11|Channel 12| | | | | | | | |
|Channel 13|Channel 14|Channel 15|Channel 16| | | | | | | | |

User Level 2

Setup loaded from File not found

Not connected

16 user-defined channels are available. These can be displayed from the Monitoring window as a bar chart or status indicator (green/grey – true/false) by clicking the I/O Window button.

• Click the ‘Load Setup File’ button to load a preconfigured file.

A unique signal name should be entered in the ‘Descriptive Text’ field.

# Signal description

|Channel|Signal Type|Number|Bit 0..7|
|---|---|---|---|
|Channel 1|@ff|Descriptive Text| |

User Level 2

Not connected
---
# MFS service software

# 9 Setting up the software

# Description

All entries/changes to the settings must subsequently be saved as the configured settings are otherwise lost.

|Abicor Binzel MFS Service Software|Settings|Signal description|Channel|
|---|---|---|---|
|16.09.2015|XEZ|Settings|Signal description|
|Channel 1|21.09.2015|08:38:06| |

|Signal Type|Number|Bit 0..7|
|---|---|---|
|Off| | |
|Motor Current [A]|add: Encoder Way [m]|none|
|Analog Input| | |
|Digital Input| | |
|Frequency Input [0.1Hz]| | |
|Memory 8-Bit| | |
|Memory 6-Bit| | |
|Memory 24-Bit| | |
|Memory 8-Bit Single Bit| | |
|Memory 16-Bit Byte-Swap| | |
|User Level 2| |Not connected|

Once a setup file has been loaded, the enabled channels are indicated by a green check mark and the disabled ones by a red cross.

The currently loaded setup file is displayed below the channels.

|Channel 1|Channel 2|Channel 3|Channel 4|Channel 5|Channel 6|Channel 7|Channel 8|Channel 9|Channel 10|Channel 11|Channel 12|Channel 13|Channel 14|Channel 15|Channel 16|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|User Level 2|Setup saved to D: signals ios| | | | | | | | | | | | | |Not connected|

# Example of the IO Display

IO DisplaySystem readySlave Drive OKMaster Drive OKKey switch in Auto positionControl Cable connectedwire speed is in WindowSet value wire speedMotor current MasterMotor current SlaveSet value hotwire powerset value speed deviation windowvalue speed deviation windowExit
EN - 29
---
# 9 Setting up the software

# MFS service software

# 9.14 Signal description Dig IO settings, user level 2

The hardware’s digital I/Os are displayed in this window.

# Digital Inputs and Outputs

|Description|Screenshot|
|---|---|
|You can click to assign a user-defined name to each I/O.|Digital Inputs and Outputs|
|This window can later be displayed from the Monitoring window as a green/grey (true/false) status indicator by clicking the Digital I/Os button.| |

Field bus activities can also be detected in OUT and IN.

|Digital Inputs|Digital Outputs|
|---|---|
|Inp.17|Out.1|
|Inp.18|Out.2|
|Inp.20|Out.3|
|Inp.21|Out.4|
|Inp.22|Out.5|
|Inp.23|Out.6|
|Inp.24|Out.7|
|Inp.25|Out.8|
|Inp.26|Out.9|
|Inp.27|Out.10|
|Inp.12|Out.11|
|Inp.28|Out.12|
|Inp.29|Out.13|
|Inp.30|Out.14|
|Inp.15|Out.15|
|Inp.16|Out.16|
|Inp.31|Out.17|
|Inp.32|Out.18|

Fieldbus

Load Setup File

Save Setup File

EN - 30
---
# MFS service software

# 9 Setting up the software

# 9.15 Device type settings

# 9.15.1 eBOX (MFS-V3 only)

NOTICE
- An active connection to the eBOX is required for these settings.
- Testing the connection on page EN-18

|Description|Screenshot|
|---|---|
|The ‘Max. hot wire current’ field is used to set the maximum hot wire current for the power source used with a current of 10 VDC at the power source’s analog input.||
|If a connected wire end sensor is used, a check box can be selected to visually represent the wire end sensor in the Job Window.| |
|If the wire buffer function is enabled, after stopping the process the wire is pressed through the rear drive into the cable assembly to ensure that there is always sufficient wire buffer in the wire guide when starting a process.| |
|The wire is pressed into the cable assembly at a constant speed until the power set for the rear motor is reached.| |
|When the ‘Monitoring welding voltage’ checkbox is enabled, the system switches off if the specified value is exceeded.| |
|The wire feed-in rate can be set to between 0.1 and 10 m/min.| |
|The acceleration time of the wire feed-in rate can be set to between 0.5 and 5 seconds.| |
|Click ‘Apply’ to save all the settings.| |

User Level 2

Device type can only be changed when disconnected

Connected

| |Max: hot wire current|200| | |
|---|---|---|---|---|
| |Wire end sensor available| | | |
| |Wire buffer function|999| | |
| |Monitoring welding Voltage|5,977| | |
| |Inching Speed and Acc.|ml/min|sec| |
| | | |MFS-V2|Minimize|
| | | |MFS-V3|Back|
| | |Apply| | |

EN - 31
---
# 9 Setting up the software

# MFS service software

# 9.16 Service interval settings (MFS-V3 only)

NOTICE
- An active connection to the eBOX is required for these settings.
- Testing the connection on page EN-18

# Description

# Screenshot

| |User|Settings|Job File Editor|
|---|---|---|---|
|Up to 4 interval messages can be generated and displayed in the software as visual message windows. This is useful for scheduled system maintenance intervals. The following statuses can be queried:| | | |
|Operating Hours [h]|Duration for which the eBOX has been switched on since the last reset| | |
|Delivery Time [h]|Duration of the actual eBOX wire feed process since the last reset| | |
|Cycles|Number of eBOX start/stop cycles completed since the last reset| | |
|Delivery amount [m]|Amount of eBOX wire used since the last reset| | |
|Default|A value of 0 – 1000 can be entered| | |
|Current|Shows the currently set values| | |
|Reset|Currently set values can be reset to zero| | |
|On/Off|Messages can be enabled or disabled| | |
|Edit|The text in messages can be freely entered. Maximum 80 characters| | |

Abicor Binze MFS Service Software Settings Service Intervals connected with 192.168.200.225

V6.4 16.09.2015 XEZ Service Intervals

|Settings|Default|Current|Reset|On/Off|
|---|---|---|---|---|
|Operating Hours [h]| | | | |
|Delivery Time [h]| | | | |
|Cycles| | | | |
|Delivery amount [m]|0| | | |

User Level 2

EN - 32

WLAN Modul

21.09.2015 08:58:52

Message

Edit

Home

Edit

Edit

Edit

Minimize

Back

Connected
---
# MFS service software

# 10 Job mode (MFS-V3 only)

The MFS-V3 system can be used in 2 operating modes (field bus systems only).

- Normal control
- Job selection

# 10.1 Normal control

In normal control mode, all values and signals are specified via the bus interface. The wire is fed forwards or backwards in speed mode. The wire feed speed is determined by a target setting (bus data word). It is not possible to use a positioning mode in this mode. In the case of hot wire applications, the hot wire current is also specified via a target setting (bus data word).

# 10.2 Job selection

The job selection mode makes it possible to save preconfigured jobs in the eBOX MFS-V3 for appropriate welding and brazing tasks. During the process, these jobs are then loaded via a bit pattern (bus interface). The jobs must be created with the service software, v6.0 or above. A maximum of 64 jobs is possible.

The following parameters can be specified and saved in the job:

- Max. hot wire current [A] (power source)
- Target value for the hot wire current variable via bus or fixed in job
- Target value for the wire speed variable via bus or fixed in job
- Tolerance of two wire windows in percent
- Backwards positioning
- Forwards positioning
- Delay between backwards and forwards positioning
- Motor current limits for pre-warning and errors in relation to both drives
- Job number
- Job description

EN - 33
---
# 10 Job mode (MFS-V3 only)

# 10.3 Job file editor settings (MFS-V3 only)

Description

Screenshot

Max. hot wire current [A] power source

The power source receives an analog target value (0…10 VDC) for the hot wire current from the eBOX.

This screen is used to set the maximum hot wire current for the power source used.

That is, 0…10 VDC on the power source’s analog input then equates to a hot wire current of 0... max. A.

Target value for the hot wire current variable via bus or fixed in job

If the hot wire current should be saved in the job, the value [A] for the hot wire current is entered.

If the hot wire current in this job is variably specified via a bus, the ‘Hot Wire from Bus’ field is selected.

If the wire speed should be saved in the job, the value [m/min] for the wire speed is entered.

If the wire speed in this job is variably specified via a bus, the ‘Wire Speed from Bus’ field is selected.

EN - 34

|Abicor Binze MFS Service Software Job List eBOX ob Data Editor|Abicor Binze MFS Service Software Job List eBOX ob Data Editor|connected with : 192.168.200.,225|WLAN Modul|WLAN Modul|
|---|---|---|
|V6.4 16.09.2015XEZ|V6.4 16.09.2015XEZ|Job Data Editor 21.,09.2015 08:59.50|Job Data Editor 21.,09.2015 08:59.50|Job Data Editor 21.,09.2015 08:59.50|
|Max hot wire current|Import Job|Export Job|Delay|Home|
|100| | |ms| |
|Job. No.|mmin|mlmin| | |
|Hotwire from BUS|Motor Prew|Wirespeed from BUS|mimin|Motor Error|
|Tolerance|Motor 2 Prew|Tolerance 2|Motor 2 Error| |
|Ignore time|ms|Average| | |
|Job Description|User Level| |Connected| |
---
# MFS service software

# 10 Job mode (MFS-V3 only)

# Description

Tolerance of two wire windows in percent

Two tolerance values can be specified for the deviation of the wire actual value from the target value. If the upper or lower tolerance limits are exceeded, a warning is emitted. To suppress a warning message during the acceleration phase, an Ignore time [ms] should be specified that is greater than the system’s acceleration time constant.

# Backwards positioning

Automatic wire retraction can be configured. This positioning occurs as soon as the wire feed start signal drops on the end of the seam. The wire speed can be set to between 0 and 10 m/min and the positioning route to between 0 and 20 mm.

# Forwards and backwards positioning plus delay between backwards and forwards positioning

An automatic wire feed can be configured to follow the wire retraction process. This positioning occurs as soon as the wire retraction positioning is complete and the specified delay [ms] has passed. The wire speed can be set to between 0 and 10 m/min and the positioning route to between 0 and 20 mm.

EN - 35
---
# 10 Job mode (MFS-V3 only)

# MFS service software

Description

Motor current limits for pre-warning and errors in relation to both drives. Limits for triggering motor current pre-warning and error messages can be specified for each drive. If these limits are exceeded, a warning message is emitted in the case of the pre-warning and an error message in the event of an error. In the event of an error, the system switches off and both drives stop. The system is released again through the acknowledgement or initialisation of the eBOX once the error has been eliminated.

The value range for the motor current is based on the maximum for the end level in the axis controller. The values entered here should correspond to the motor used.

|Motor 1 Prew.|Rear drive value range for pre-warning|0 - 7 [A]|
|---|---|---|
|Motor 1 Error|Rear drive value range for error|0 - 7 [A]|
|Motor 2 Prew.|Front drive value range for pre-warning|0 - 7 [A]|
|Motor 2 Error|Front drive value range for error|0 - 7 [A]|
|Average|Average formation for hiding current spikes|2 – 16|

Gliding average formation: To suppress warning and error messages caused by current spikes, e.g. during the acceleration phase, a value should be specified for the gliding average formation. This parameter specifies the number of values used to determine the average. The smaller the value, the less weight readings near to the average carry. The higher the value, the slower the average follows spikes in the readings.

# NOTICE

- Ensure that the value for the pre-warning is lower than that for the error.
- All values for motor current monitoring must be calculated and adjusted on the basis of the entire system as each system has different coefficients of friction and therefore different resultant motor currents.

EN - 36
---
# MFS service software

# 10 Job mode (MFS-V3 only)

# Description

Job number and job descriptionA job number between 1 and 64 is specified in the ‘Job No.’ field.A job description can be entered in the ‘Job Description’ field with a maximum of 16 characters.

# Example

The job can be saved by clicking the ‘Export Job’ button.

# Screenshot

The specified file name already contains the job number and description.Touch File DialogSelect Path and FileIntelLogdatenLogfilesMaster PullOutlook-Archivc:l PerfLoasLwelding_lefJOBSave File1-welding_left JOBZuruckEN - 37
---
# 10 Job mode (MFS-V3 only)

# 10.4 Job list eBOX settings (MFS-V3 only)

NOTICE
- An active connection to the eBOX is required for these settings.
- Testing the connection on page EN-18

# Description

Click the ‘Job List eBOX’ button to display all of the memory locations for jobs on the eBOX in a list from 1 – 64.

|Job No|eBox|Name|
|---|---|---|
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |

Use the ‘Import Job’ button to transfer jobs previously created in the job file editor to the eBOX and save them. It is sensible to save the job to the memory location with the same job number as the file name.

Use the ‘Export Job’ button to read and externally save a selected job that has been saved on the eBOX.

Use the ‘Exp. All Jobs’ button to read and externally save all jobs that have been saved on the eBOX.

Use the ‘Delete Job’ button to delete a selected job that has been saved on the eBOX.

Use the ‘Delete All Jobs’ button to delete all the jobs that have been saved on the eBOX.

Use the ‘Edit Job’ button to edit and re-save a selected job that has been saved on the eBOX.
---
# MFS service software

# 10 Job mode (MFS-V3 only)

# Description

# Screenshot

# Example: Import Job

- Click the ‘Import Job’ button.
- Select the desired job (multiple selection possible).
- Click the ‘Open File’ button.

# Touch File Dialog

Select Path and File

- Intel
- Logdaten
- Logfiles
- Master Pull
- Outlook-Archiv
- c:l PerfLoas
- Lwelding_lefJOB

# Open File

Zuruck

A query appears to ask if the job should be saved to the currently selected memory location 0 (Job List eBOX).

Yes: the job ‘1-roof_seam_left.JOB’ is saved to memory location 0 on the eBOX (not recommended).

No: the job ‘1-roof_seam_left.JOB’ is saved to memory location 1 on the eBOX, as per the job number.

In this case, select No.

EN - 39
---
# 10 Job mode (MFS-V3 only)

# MFS service software

Description

Memory location 1 is then labelled as ‘used’.

EN - 40

# Screenshot

Abicor Binze MFS Service Software Settings Job List eBOX connected with: 192.168.200.225 WLAN Mcdul 16.09.2015 XEZ Job List 21.09.2015 09:13.27

|Job No|eBox|Name|
|---|---|---|
|used|welding_leit| |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |
|free| | |

Home

Minimize

Back

Import Job

Export Job

Exp _ All Jobs

Delete Job

Delete Jobs

Edit Job

Save Job

User Level 2

Connected
---
# MFS service software

# 10 Job mode (MFS-V3 only)

# 10.5 Job window (MFS-V3 only)

NOTICE
- An active connection to the eBOX is required for these settings.

Testing the connection on page EN-18

|Description|Screenshot| | | | | | |
|---|---|---|---|---|---|---|---|
| |User|User| |Job File Editor| | | |
| |Abicor Binze MFS Service Software|Job Window| |connected with 192.168.200.225| | | |
| | | | | |WLAN Modul|Job Window|21.,09.2015 09.39.51|
| |Motor current|0,647A| | | | | |
| |Motor 2|0,589A| | | | | |
| | | |Edit| |Save| | |
| | |Set point|Act Valu;|Job: No: 500| | | |
| | | |welding_left|5,02 ml/min| | | |
| | |Set poin|5 ml/min|Act Valul5,067 m/min| | | |
| | | | | | |Minimize| |
| | |Hotwire from BUS| | | | | |
| | |Wirespeed from BUS|5,02 m/min| | | | |
| |Tolerance|10| | | | | |
| |Tolerance 2|20| | | | | |
| |Ignore time|300 ms| | | | | |
| |Status|OK| | | | | |
| |User Level| | | | |Connected| |

All parameters for the currently loaded job are displayed in the job window. The present motor currents and wire actual value are also displayed.

The present hot wire values, motor currents and wire actual value are also displayed.

The status ‘red’ indicates that no process is currently active.

The status ‘green’ indicates that a process is currently active.

The red hand indicates that the eBOX’s key switch is set to Service.

The green hand indicates that the eBOX’s key switch is set to Auto.

EN - 41
---
# 10 Job mode (MFS-V3 only)

# MFS service software

Description

If the wire end sensor has been previously enabled in the device settings, the following icon additionally appears:

- Green indicates that wire is available.
- Red indicates that no wire is available.

The status field indicates whether the system is ready for operation, is emitting a warning or has an error.

All warnings and error messages are described in a later section.

Status: OK

EN - 42
---
# MFS service software

# 10 Job mode (MFS-V3 only)

# 10.6 Job window edit mode (MFS-V3 only)

NOTICE
- An active connection to the eBOX is required for these settings.

9.6 Testing the connection on page EN-18

|Description|Screenshot|
|---|---|
|User|Job File Editor|
|In user level 2 mode, the ‘Edit/View’ button can be used to switch between the view only and edit modes in order to change parameters. This can also be done while a process is running. The change can only be saved while there is no process running. To do this, click ‘Save’.|In user level 2 mode, the ‘Edit/View’ button can be used to switch between the view only and edit modes in order to change parameters. This can also be done while a process is running. The change can only be saved while there is no process running. To do this, click ‘Save’.|

EN - 43
---
# 11 Monitoring mode

# NOTICE

• An active connection to the eBOX is required for these settings.

9.6 Testing the connection on page EN-18

# Description

|Screenshot|or|or|M|
|---|---|---|---|
|User|User|User|Monitoring|

# Example

Channel 1Channel 2Channel 3Channel 4Channel 5

The Monitoring window is divided into several sections.

Top left

Centre left

Bottom left

Middle

# Wire actual value

- Motor current rear drive
- Motor current front drive
- Used data volume
- Start signal

# History list of the log files

These are stored here successively and can be loaded for viewing by double-clicking them. All log files are stored as CSV files at the path specified in the settings.

# History list of the warnings and errors

These are stored here successively and can be viewed more closely or removed from the list by right-clicking them. All messages are permanently stored in an ‘ErrorLog.txt’ file at the specified log path. If the list is cleared in the Monitoring window, this is entered in the ‘ErrorLog.txt’ file using the entry ‘ACK’ plus a time stamp.

# Status indicator

for the start/stop trigger, start/stop visualisation, recording/cycle time and warning and error statuses.

# Time diagram

for displaying the channels. Up to 8 channels can be included.
---
# MFS service software

# 11 Monitoring mode

# 11.1 Closing the Monitoring window

Description

The Monitoring window can be minimised at the top right or closed completely by clicking the Monitoring window itself.

Screenshot

Do you want to really want to exit this software?

Yes
No
# Example for log data

All entries are given a date and a time stamp.

| | |ErrorLog txt|Editor| | |
|---|---|---|---|---|---|
| |Datei| |Bearbeiten|Format|Ansicht|
| |FERR| | |MULTI-IO| |
| |SERR| | |MULTI-| |
| |SERR| |2015|MULTI| |
| |SERR| | |10:28|MULTI-IO|

EN - 45
---
# 12 System Information

# NOTICE

• An active connection to the eBOX is required for these settings.

9.6 Testing the connection on page EN-18

# Description

Click the ‘System Info’ button to view the eBOX’s current configuration.

The ‘Error Memory’ button is only visible in user level 2 mode and is for servicing work by Abicor Binzel.

Click the ‘Error Log’ button to view the content of the ‘ErrorLog.txt’ file located in the log path.

# Example

|SERR|2015 10:54:50|MULTI-IO Status|warning prewarning|current Master drive|
|---|---|---|---|---|
|SERR|2015 10:19:39|MULTI-IO Status|Master drive Error| |
|SERR|2015 10:54:50|MULTI-IO Status|warning prewarning motor current|Master drive|
|SERR|2015 10:50:05|MULTI-IO Status|Wire outside window| |
|SERR|2015 10:07:23|MULTI-IO Status|valid job loaded| |

# Correction

Exit

Save File
---
# MFS service software

# 12 System Information

|Description|Screenshot|
|---|---|
|System information| |
|Slave Type|Main printed circuit board multi-IO (here MFS-V3), address, IP address|
|TCP Connected|TCP connection enabled|
|Firmware MultiIO|Firmware status of the main printed circuit board|
|Firmware MultiIO-ADDA|Firmware status of the internal ADDA controller|
|Firmware MIOACHSCO|Firmware status of the axis controller printed circuit board|
|Stand-Alone Software|Currently loaded user program|
|Mapping File|Currently loaded bus mapping|
|System RTC|Current system time|
|Working counter|Current number of operating hours|
|Anybus-Module|Currently installed field bus module|

The system information can be exported as a text file by clicking ‘Save File’.

# Example of an error log

The error log displays all previous warning, nonconformity and error messages. The error log can be exported as a text file by clicking ‘Save File’.

Correction information can be displayed. To view this, select the applicable error entry and then click the ‘Correction’ button.

# Show Text

|SERR|Date|Status|Message|
|---|---|---|---|
|SERR|2015 10:54:50|MULTI-IO Status|warning prewarning current Master drive|
|SERR|2015 10:19:39|MULTI-IO Status|Master drive Error|
|SERR|2015 10:54:50|MULTI-IO Status|warning prewarning tor current Master drive|
|SERR|2015 10:50:05|MULTI-IO Status|Wire outside window|
|SERR|2015 10:07:23|MULTI-IO Status|No valid TOD loaded|

Correction Exit Save File

EN - 47
---
# 12 System Information

# MFS service software

|Description|Screenshot|
|---|---|
|A window opens with descriptions of how to correct the error and an appropriate photo.|Help information|
|Click to zoom in on the photo or to close it again.| |
|valid job loaded|Correction|
|job number has been selected|saved|
|Please check appropriate job and SaVF position|the eBOK job list|
|Select that has already been saved|job number|
|This message must be acknowledged!| |
|Exit| |

EN - 48
---
# MFS service software

# 13 Diagnosis

NOTICE
- An active connection to the eBOX is required for these settings.

9.6 Testing the connection on page EN-18

# Description

The diagnosis mode can be used to check if the drives, wire actual value encoder, inching button, reset button and key switch are functioning correctly. The functional checks can only be selected in diagnosis mode if there is no active process. Furthermore, it is not possible to conduct a process start while diagnosis mode is enabled; the system reports ‘System not ready’.

# Testing drives

|User|User|User|Diagnosis|
|---|---|---|---|
|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225|WLAN Modul|
|16.09.2015XEZ|Diagnosis|21.,09.2015 09.54,07|Test Drives|
|Master Drive|Slave Drive|Inching Button|Reset Button|
|Key Switch|Check Measuring Wheel|Timeout|30 sec|
|Minimize|Minimize|Minimize|Back|
|User Level 2|Connected|Connected|Connected|

# Additional Instructions

With the wire inserted, open the rocker arms on the pressure rolls on the drive!

Abicor Binze Service Software

Please open the pressure rolls for the drives

OK
Cancel
EN - 49
---
# 13 Diagnosis

# MFS service software

Description

The test run starts. The drive moves forwards at a predefined speed for approx. 6 seconds. During this time, a check is conducted to see if the drives’ control encoder increments are correct. (Target/actual comparison)

At the end of a successful test run, the message ‘Test OK’ appears. When running a test on the rear slave drive, it is also possible to choose whether this is an MF1 drive or an M-Drive. This setting should be accurate as different drive parameters are used for the different drives.

# EN - 50

# Screenshot

|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225|WLAN Modul| | |
|---|---|---|---|---|---|
|V6.4|16.09.2015|XEZ|Diagnosis|21.09.2015|09.54.47|

# Test Drives

# Test Inputs/Outputs

|Inching Button|Test is running|Reset Button| |Home| | |
|---|---|---|---|---|---|---|
|Master Drive|MF-1|Slave Drive|M-Drive| | | |
|User Level 2| | | |Connected|Check Measuring Wheel|Timeout|
|Meas Wheel Tes|30 sec| | |Minimize| | |
| | | | |Back| | |

# Screenshot

|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225|WLAN Modul| |
|---|---|---|---|---|
|16.09.2015|XEZ|Diagnosis|21.09.2015|09.55.06|

# Test Drives

# Test Inputs/Outputs

|Inching Button|Test OK|Reset Button| |Home| | |
|---|---|---|---|---|---|---|
|Master Drive|MF-1|Slave Drive|M-Drive| | | |
|User Level 2| | | |Connected|Check Measuring Wheel|Timeout|
|Meas Wheel Tes|30 sec| | |Minimize| | |
| | | | |Back| | |
---
# MFS service software

# Diagnosis

Description

Testing drives in the event of nonconformities

This message is displayed if a test is unsuccessful.

Possible causes

- Control lead not connected
- Drive’s encoder defective
- Motor current too high (&gt; 7 A)
- Control lead defective
- Drive mechanically blocked
- Drive motor defective
- eBOX axis controller printed circuit board faulty

At the end of an unsuccessful test run, the message ‘Test Error’ appears.

Abicor Binzel MFS Service Software Diagnosis

Connected with 192.168.200.225

WLAN Modul

16.09.2015 XEZ

Diagnosis 21.09.2015 10:00;20

# Test Drives

|Test Error| | | | | | | | |
|---|---|---|---|---|---|---|---|---|
|Inching Button| | | |Reset Button| |Home| | |
| |Master Drive| | | | | | | |
| |Slave Drive|M-Drive| | | | | | |
| |User Level 2| | | | | | | |
| | | | |Check Measuring Wheel| | | | |
| | | | | |Timeout|MF-1|30 sec| |
| | | | | | |Minimize|Meas Wheel Test|Back|
| | | | | | |Connected|EN - 51| |
---
# 13 Diagnosis

# MFS service software

# 13.1 Checking the measuring wheel

NOTICE
- Use two people to conduct this test.

# Description

The measuring wheel test checks if the wire actual value encoder is functioning correctly. This is the additional encoder on the front MF1 drive. This additional encoder has no influence on regulating the system speed. The wire actual value encoder transmits the wire speed actually measured on the wire.

As the wire actual value encoder is generally mounted on the front drive in a position near the process, in the case of a system installed in the welding cell, it is useful to set a timeout period that gives the user enough time to manually move the measuring roll on the front drive after starting the test. If the measuring roll is not moved as intended in the specified period, the diagnosis software reports a nonconformity.

EN - 52
---
# MFS service software

# 13 Diagnosis

# 13.2 Workflow

Description

- Set a timeout period.
- Start the test.
- Manually turn the measuring wheel clockwise.
- The expired timeout period is displayed.
- Turn the measuring wheel anticlockwise.

The test has been successfully completed within the timeout period.

# Screenshot

|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225 WLAN Modul|V6.4 16.09.2015 XEZ|
|---|---|---|---|
|Diagnosis|21.09.2015 10:01:43|Test Drives|Test Inputs/Outputs|
|Inching Button|Reset Button|Home|Master Drive|
|Key Switch|Check Measuring Wheel|Timeout|MF-1|
|30|sec|Minimize|Slave Drive|
|Meas_ Wheel Tes|27 sec|M-Drive|Turn measuring wheel clockwise|
|Back|User Level 2|Connected| |

|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225 WLAN Modul|V6.4 16.09.2015 XEZ|
|---|---|---|---|
|Diagnosis|21.09.2015 10:06:21|Test Drives|Test Inputs/Outputs|
|Inching Button|Reset Button|Home|Master Drive|
|Key Switch|Check Measuring Wheel|Timeout|MF-1|
|30|sec|Minimize|Slave Drive|
|Meas_ Wheel Tes|24 sec|M-Drive|Turn measuring wheel anticlockwise|
|Back|User Level 2|Connected| |

|Abicor Binze MFS Service Software|Diagnosis|connected with 192.168.200.225 WLAN Modul|16.09.2015 XEZ|
|---|---|---|---|
|Diagnosis|21.09.2015 10:07:52|Test Drives|Test Inputs/Outputs|
|Inching Button|Reset Button|Home|Master Drive|
|Key Switch|Check Measuring Wheel|Timeout|MF-1|
|30|sec|Minimize|Slave Drive|
|Meas Wheel Tes|1 sec|M-Drive|Test OK|
|Back|User Level 2|Connected| |

EN - 53
---
# 13 Diagnosis

# MFS service software

# Description

Screenshot

# Possible causes

- Control lead not connected
- Signals lost along the entire signal flow
- Connector in the eBOX not correctly inserted

# Control lead defective

- Switch/button faulty
- eBOX multibus IO printed circuit board faulty

# Description

Screenshot

# Check the measuring wheel in the event of a nonconformity

This message is displayed if a test is unsuccessful.

Abicor Binze Service Software

OK

# Possible causes

- Measuring wheel not moved within the timeout period
- Control lead not connected
- Control lead defective
- Actual value encoder signals lost along the entire signal flow
- Actual value encoder defective
- Connector in the eBOX not correctly inserted
- eBOX multibus IO printed circuit board faulty

# Testing the inputs/outputs

By pressing or switching the applicable elements, the correct function is displayed through incremental values and signalling.

If the test is not successful, no green status indicator appears.

# Possible causes

- Control lead not connected
- Control lead defective
- Signals lost along the entire signal flow
- Connector in the eBOX not correctly inserted
- eBOX multibus IO printed circuit board faulty

# Error: measuring wheel is not counting correctly

EN - 54
---
# MFS service software

# 14 Warnings and error messages (status)

Description

Presentation of the messages

All warnings and error messages are only logged and displayed in the case of active communication and an active ‘Job Window’ or ‘Monitoring Window’. The visual indication is provided by means of a banner located above the ‘Job Window’ or ‘Monitoring Window’. Warnings are indicated in yellow. Error messages are indicated in red.

# Example of a job warning window

|Abicor Binze MFS Service Software|connected with 192.168.200.225|WLAN Modul|
|---|---|---|
|16.09.2015|Job Window|21.09.2015 10:18:01|
|Motor current|0,015A|Motor|
|Motor 2|0,024A|Edit|
|Set point|184,915|Delay|
|Act Value| |Job: No_ 45|
| |0,196 ml/min| |
|Set point|3,728 ml/min|Act Value|
| |2,039|Minimize|
|Hotwire from BUS| |Motor Prew 001|
|Wirespeed from BUS|902 m/min|Motor Error|
|Tolerance|55|Motor 2 Prew|
|Tolerance 2|254|896|
|Ignore time|505 ms| |
|Status|Warning|User Level|
| | |Connected|

# Example of an error in the Monitoring window

EN - 55
---
# 14 Warnings and error messages (status)

# MFS service software

# Description

Presentation of the messages

All warnings and error messages are only logged and displayed in the case of active communication and an active ‘Job Window’ or ‘Monitoring Window’. The visual indication is provided by means of a banner located above the ‘Job Window’ or ‘Monitoring Window’.

- Warnings are indicated in yellow.
- Error messages are indicated in red.

# Message list

Depending on the system configuration, the following warnings and error messages can occur.

|There is no nonconformity and the system is|Status|OK|
|---|---|---|
|The eBOX reports that the selected job does|Status|No valid job loaded|
|not exist. A job is classed as valid as soon| | |
|as it has been stored on the eBOX| | |
|regardless of the parameter values. As soon| | |
|as a job memory location is deleted on the| | |
|eBOX, the memory location is classed as| | |
|invalid.| | |
|The key switch on the eBOX was switched|Status|Active process interrupted by service mode|
|from ‘Auto’ to ‘Service’ during the active| | |
|process.| | |
|The process was started despite the key|Status|Process activated externally during service mode|
|switch on the eBOX being set to ‘Service’.| | |
|The M-Drive’s protection cover is not closed|Status|Protection cover not closed|
|on systems with an M-Drive.| | |
|The motor output stage for the master drive|Status|Master drive error|
|is reporting an error due to an excess| | |
|current or the overheating of the motor| | |
|output stage.| | |
|The motor output stage for the slave drive is|Status|Slave drive error|
|reporting an error due to an excess current| | |
|or the overheating of the motor output| | |
|stage.| | |
|The fact that the control lead for the drive is|Status|Control cable not connected|
|not properly connected to the eBOX is| | |
|reported on systems without an M-Drive.| | |
|The process was started without a defined|Status|Process start without defined system mode|
|system mode (see bit pattern for the| | |
|operating mode).| | |
|The wire actual value is outside the|Status|Wire outside window 1|
|specified permissible deviation in| | |
|window 1.| | |
|The wire actual value is outside the|Status|Wire outside window 2|
|specified permissible deviation in| | |
|window 2.| | |
|The rear drive’s motor current exceeds the|Status|Slave drive motor current prewarning|
|value specified for the pre-warning in the| | |
|job.| | |
|The rear drive’s motor current exceeds the|Status|Slave drive motor current fault|
|value specified for the error in the job.| | |
|The system switches off with an error message.| | |
|The front drive’s motor current exceeds the|Status|Master drive motor current prewarning|
|value specified for the pre-warning in the job.| | |

EN - 56
---
# MFS service software

# 14 Warnings and error messages (status)

|Description|Screenshot|
|---|---|
|The front drive’s motor current exceeds the value specified for the error in the job. The system switches off with an error message.|Status: Master drive motor current fault|
|The system reports a drop in the external US2 voltage (protective door open). Only for AIDA-compliant systems.|Status: Voltage drop US2 personnel protection|
|The system reports that no wire is available while the wire end sensor is enabled.|Status: Wire end sensor reports that no wire is available|

EN - 57
---
# 15 Releasing the user levels and rights

All entries with the following sign require active communication with the eBOX.

|Description|Screenshot|
|---|---|
|All entries with this sign require active communication with the eBOX.| |
|User level 0|User|
|Options at this level| |
|Load Log File| |
|User Login| |
|Connect/Disconnect Communication| |
|System Information| |
|Error Log| |
|Monitoring| |
|Signal Status In/Out| |
|IO Display| |
|Digital Display| |
|Job Window without edit function (MFS-V3 only)| |

EN - 58
---
# MFS service software

# 15 Releasing the user levels and rights

|Description|Screenshot|
|---|---|
|User level 1|Uce|

# Options at this level

- Load Log File
- User Login
- Connect/Disconnect Communication
- Settings
- System
- Language
- System Language Settings
- Monitoring
- Channel Visualisation (setup files can only be loaded)
- Start/Stop Trigger (setup files can only be loaded)
- Drive, Gear Reduction, Encoder, Meas. Wheel (setup files can only be loaded)
- Job List eBOX without edit function (MFS-V3 only)
- Service Intervals without edit function (MFS-V3 only)
- Job File Editor (jobs can be created with the import and export function)
- Signal description IO and Dig. IO (setup files can only be loaded)
- System Information
- System Information
- Error Log
- Diagnosis
- Monitoring
- Signal Status In/Out
- IO Display
- Dig. IO Display
- Job Window without edit function (MFS-V3 only)

EN - 59
---
# 15 Releasing the user levels and rights

# MFS service software

# Description

# Screenshot

# User level 2

# Options at this level

- Load Log File
- User Login
- Connect/Disconnect Communication
- Settings
- System
- Language
- System Language Settings
- Date Time
- IP address
- Device Type
- Device Setup
- Connection Type
- Job List eBOX with import, export and edit functions (MFS-V3 only)
- Service Intervals with edit function (MFS-V3 only)
- Monitoring
- Channel Visualisation (setup files can be created, loaded and saved)
- Start/Stop Trigger (setup files can be created, loaded and saved)
- Drive, Gear Reduction, Encoder, Meas. Wheel (setup files can be created, loaded and saved)
- Log File Path (select memory location for log data)
- Job File Editor (jobs can be created with the import and export function)
- Signal description IO and Dig. IO (setup files can be created, loaded and saved)
- System Information
- System Information
- Error Log
- Diagnosis
- Monitoring
- Signal Status In/Out
- IO Display
- Dig. IO Display
- Job Window with edit function (MFS-V3 only)
---
MFS service software  Notes

Notes





                      EN - 61
---
# TECHNOLOGY FOR THE WELDER'S WORLD.

BAL.0420.0 • 2016-07-05

Alexander Binzel Schweisstechnik GmbH & Co.KG

Postfach 10 01 53 • D–35331 Giessen

Tel.: ++49 (0) 64 08 / 59–0

Fax: ++49 (0) 64 08 / 59–191

Email: info@binzel-abicor.com

www.binzel-abicor.com