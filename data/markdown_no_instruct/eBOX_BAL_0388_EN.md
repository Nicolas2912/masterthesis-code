# TECHNOLOGY FOR THE WELDER'S WORLD.

# DE Betriebsanleitung / EN Operating instructions

# FR Mode d’emploi / ES Instructivo de servicio

# eBOX

# MFS-V3

# DE eBOX

# EN eBOX

# FR eBOX

# ES eBOX

EN 60 974-1

ZERIZI

TFIERTES

DIN EN

ISO 9001

QM-SYSTEM

www.binzel-abicor.com
---
# eBOX

EN      English Translation of the original operating instructions

© The manufacturer reserves the right, at any time and without prior notice, to make such changes and amendments to these operation Instructions which may become necessary due to misprints, inaccuracies or improvements to the product. Such changes will however be incorporated into subsequent editions of the Instructions. All trademarks mentioned in the operating instructions are the property of their respective owners. All brand names and trademarks that appear in this manual are the property of their respective owners/manufacturers. Our latest product documents as well as all contact details for the ABICOR BINZEL national subsidiaries and partners worldwide can be found on our website at www.binzel-abicor.com

# 1 Identification

EN-3

# 2 Safety

EN-4

# 2.1 Designated use

EN-4

# 2.2 Responsibilities of the user

EN-4

# 2.3 Personal protective equipment (PPE)

EN-4

# 2.4 Classification of the warnings

EN-5

# 2.5 Emergency information

EN-5

# 3 Product description

EN-6

# 3.1 Technical data

EN-6

# 3.2 Abbreviations

EN-6

# 3.3 Nameplate

EN-7

# 3.4 Signs and symbols used

EN-7

# 4 Scope of delivery

EN-7

# 4.1 Transport

EN-8

# 4.1.1 Removing the transport protection

EN-8

# 4.2 Storage

EN-8

# 5 Functional description

EN-9

# 6 Putting into operation

EN-9

# 6.1 Installation

EN-10

# 6.2 eBOX US1 power supply for the bus module and logic circuit

EN-10

# 6.2.1 Internal power supply

EN-10

# 6.2.2 External power supply

EN-11

# 6.3 Establishing connections

EN-12

# 6.4 eBOX & M-Drive standard / Masterliner

EN-12

# 6.5 eBOX & MF1

EN-13

# 6.6 eBOX, MF1 & MF1 rear drive

EN-14

# 6.7 Power supply

EN-15

# 6.8 Pin assignment

EN-16
---
# 1 Identification

The eBOX is part of the MFS-V3 wire feeder system and is used in industry and the trade for the delivery of the welding filler materials. All of the electronic control elements are integrated into the BOX. The modular design of the wire feeder system enables individual mechanical and electronic adjustment via I/O or digital BUS systems. These operating instructions solely describe the eBOX.

The following eBOX versions are available:

- Analog
- Digital for various field bus systems/interfaces

The eBOX must only be operated using original ABICOR BINZEL spare parts.

# 1.1 CE marking

This device fulfils the requirements of the relevant EU directives.

Conformity is confirmed by the CE marking on the device.

EN - 3
---
# 2 Safety

The attached safety instructions must be observed.

# 2.1 Designated use

- The device described in these instructions may be used only for the purpose described in these instructions in the manner described. In doing so, observe the operating, maintenance and servicing conditions.
- Any other use is considered contrary to the designated use.
- Unauthorized conversions or power increase modifications are not allowed.

# 2.2 Responsibilities of the user

- Keep the operating instructions within easy reach at the device for reference and enclose the operating instructions when handing over the product.
- Putting into operation, operating and maintenance work may only be carried out by qualified personnel. Qualified personnel are persons who, based on their special training, knowledge, experience and due to their knowledge of the relevant standards, are able to assess the tasks assigned to them and identify possible dangers (in Germany see TRBS 1203).
- Keep other persons out of the work area.
- Please observe the accident prevention regulations of the country in question.
- Ensure good lighting of the work area and keep the work area clean.
- Occupational health and safety regulations of the country in question. For example, Germany: Protection Law and the Company Safety Ordinance.
- Regulations on occupational safety and accident prevention.

# 2.3 Personal protective equipment (PPE)

To avoid dangers for the user, wearing personal protective equipment (PPE) is recommended in these instructions.

- It consists of protective clothing, safety goggles, class P3 respiratory mask, safety gloves and safety shoes.
---
# 2 Safety

# 2.4 Classification of the warnings

The warnings used in the operating instructions are divided into four different levels and are shown prior to potentially dangerous work steps. Arranged in descending order of importance, they have the following meaning:

- DANGER

Describes an imminent threatening danger. If this danger is not avoided, it will result in fatal or extremely critical injuries.
- WARNING

Describes a potentially dangerous situation. If not avoided, it can result in serious injury.
- CAUTION

Describes a potentially harmful situation. If not avoided, it may result in slight or minor injuries.
- NOTICE

Describes the risk of impairing work results or the risk that the work may result in material damage to the equipment.

# 2.5 Emergency information

In case of emergency, immediately interrupt the following supplies:

- Power

Further measures can be found in the "Power source" oper peripheral devices.

EN - 5
---
# 3 Product description

# 3.1 Technical data

|eBOX|eBOX|eBOX|
|---|
|685|214|600|
|385|Bi2|Bi2|

Ambient temperature: - 10 °C to + 40 °C

Relative humidity: up to 90 % at 20 °C

# Tab. 1 Ambient conditions during operation

Storage in a closed environment, ambient temperature: - 10 °C to + 40 °C

Ambient temperature for transport

Relative humidity: - 25 °C to + 55 °C

up to 90 % at 20 °C

# Tab. 2 Ambient conditions for shipment and storage

Weight: 21.5 kg

Connection voltage: 100-240 V AC/ 50 or 60 Hz

Internal operating voltage: 24 VDC / 38 VDC

Power consumption: 1.0 kW

Protection type: IP21

# Tab. 3 eBOX

# 3.2 Abbreviations

|MFS-V3|Complete wire feeder system comprising an eBOX with one or two wire drives plus all necessary media and control leads|
|---|---|
|MF1|Process-side wire drive|
|MF1 front drive|Process-side wire drive on PushPush systems|
|MF1 rear drive|Rear wire drive on PushPush systems|
|M-Drive|Alternative rear drive (only on PushPush systems)|
|eBOX|Wire drive control unit|

# Tab. 4 Abbreviations
---
# 3.3 Nameplate

The eBOX is labelled with a nameplate as follows:

Biai= 0+7014 VUlTILO eBOX nruani Bizz IBICOR

Fig. 2 eBOX nameplate

Please note the nameplate details and the device information when making any enquiries:

- Device type, device number, service number, year of construction, firmware, field bus system.

# 3.4 Signs and symbols used

In the operating instructions, the following signs and symbols are used:

|Symbol|Description|
|---|---|
|•|List of symbols for action commands and enumerations|
|Cross reference symbol|refers to detailed, supplementary or further information|
|1|Action(s) described in the text to be carried out in succession|

# 4 Scope of delivery

- eBOX - ready for operation, either analog/digital or with field bus interface (customer specific)
- Mains cable (customer specific)
- SD card with eBOX backup files (customer specific)
- Operating instructions

Tab. 5 Scope of delivery

Manual terminal for the MF control

Tab. 6 Options

Order the equipment parts and wear parts separately. The order data and ID numbers for the equipment parts and wear parts can be found in the current catalogue. Contact details for advice and orders can be found online at www.binzel-abicor.com.

EN - 7
---
# 4 Scope of delivery

# 4.1 Transport

Although the items delivered are carefully checked and packaged, it is not possible to exclude the risk of transport damage.

Goods inspection Use the delivery note to check that everything has been delivered. Check the delivery for damage (visual inspection).

In case of complaints If the delivery has been damaged during transportation, contact the last carrier immediately. Retain the packaging for potential inspection by the carrier.

Packaging for returns Where possible, use the original packaging and the original packaging material. If you have any questions about the packaging and/or how to secure an item during shipment, please consult your supplier.

# 4.1.1 Removing the transport protection

WARNING
Risk of fire
The transport protection has the potential to cause a fire.
• Remove the transport protection before putting the system into operation for the first time.

|1|eBOX|
|---|---|
|2|Transport protection|

Fig. 3 Removing the transport protection

1 Open the cover of the eBOX (1) and remove the transport protection (2).

# 4.2 Storage

Physical storage conditions in a closed environment:

Tab. 2 Ambient conditions for shipment and storage on page EN-6

EN - 8
---
# Functional description

The eBOX control unit acts as the communication interface between the higher-level system control unit and the MFS's wire drives (optional for a hot wire power source). All the default target values required for the wire feed process (analog/digital or via field bus) are forwarded to the drives via microprocessor-based motor control units. All electronic components are installed in the metal housing. The power supply is provided via a separate connecting cable. For the connection voltage and power consumption, see: 3.1 Technical data on page EN-6

# Putting into operation

DANGER

Risk of injury due to unexpected start-up. The following instructions must be adhered to throughout all maintenance, servicing, assembly, disassembly and repair work:

- Switch off the power source.
- Close the compressed air supply.
- Close the gas supply.
- Disconnect the mains plug.

DANGER

Risk of injury. Safety switches on covers and protective devices are ineffective in manual mode (only in connection with M-Drive).

- Greater concentration.

NOTICE

Please take note of the following instructions:

- 2 Safety on page EN-4

The system may only be installed and put into operation by authorized personnel (in Germany see TRBS 1203).

Remove the transport protection before putting the system into operation for the first time. 4.1.1 Removing the transport protection on page EN-8

Install the service software before putting the system into operation for the first time. To do this, please refer to the information in the service software operating instructions BAL.0420.

EN - 9
---
# 6 Putting into operation

# 6.1 Installation

Select an installation site with sufficient ventilation and clearance for the housing fan.

# 6.2 eBOX US1 power supply for the bus module and logic circuit

The eBOX's logic circuit is powered by an internal power supply unit by default.

# 6.2.1 Internal power supply

When using an internal power supply, configure the following jumper settings on the main PCB (4):

1. Set jumper (1) to on (bottom position), jumper (2) to on (left position) and jumper (3) to on (bottom position).

Switch on the eBOX at the main switch Q1 (6).

|1|J1, J2|3|J5, J6|5|Port US1/US2 X3|
|---|---|---|---|---|---|
|2|J3, J4|4|Main PCB|6|Main switch Q1|

Fig. 4 Internal power supply

EN - 10
---
# 6 Putting into operation

# 6.2.2 External power supply

|1|J1, J2|3|J5, J6|5|US1/US2 port X3|
|---|---|---|---|---|---|
|2|J3, J4|4|Main PCB|6|Main switch Q1|

Fig. 5 Power supply

On an AIDA-compliant eBOX, the logic circuit is externally powered via the X3 port (5) in order to avoid any bus communication failure if the internal power supply fails.

When using an external power supply, configure the following jumper settings on the main PCB (4), always retaining the order shown:

1. Set jumper (1) to off (top position), jumper (2) to on (left position) and jumper (3) to on (top position).
2. Switch on the eBOX at the main switch Q1 (6).
3. Connect the AIDA power connector to the X3 port (5).

EN - 11
---
# 6 Putting into operation

# 6.3 Establishing connections

# 6.4 eBOX & M-Drive standard / Masterliner

Establish the connections as shown in the following diagram:

1
M-Drive
2
Port for control lead X11
3
eBOX
4
Control lead
5
Port for control lead X46

Fig. 6 eBOX & M-Drive standard / Masterliner

EN - 12
---
# 6 Putting into operation

# 6.5 eBOX & MF1

Establish the connections as shown in the following diagram:

|1| |2| |3| |4| |5| |6| |7| |8|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Wire end sensor| |Barrel| |eBOX| |Control lead eBOX - masterfeeder| |Masterfeeder MF1| |Flex supply| |Masterliner| |Wire end sensor control lead|

Fig. 7 eBOX & MF1

EN - 13
---
# 6 Putting into operation

# 6.6 eBOX, MF1 & MF1 rear drive

Establish the connections as shown in the following diagram:

|1|2|3|4|5|6|7|8|9|10|
|---|---|---|---|---|---|---|---|---|---|
|Wire end sensor|Barrel|eBOX|Wire end sensor control lead|Control lead eBOX - MF1/ MF1DIG. /sensor|Flex supply|MF1 front drive|Masterliner|MF1 rear drive|Masterliner|

Fig. 8 eBOX, MF1 & MF1 rear drive

EN - 14
---
# 6 Putting into operation

# 6.7 Power supply

DANGER

Electric shock

Dangerous voltage due to defective cables.

• Check that all live cables and connections are properly installed.

• Replace any damaged, deformed or worn parts.

1 Mains port X1

For details of the power supply and the fuse protection, please see:

- 3.1 Technical data on page EN-6
- 3.3 Nameplate on page EN-7

1 Insert the mains plug into the mains port X1 (1).

EN - 15
---
# 6 Putting into operation

# 6.8 Pin assignment

1 eBOX - robot X2

2 Manual terminal (optional) X10

3 M-Drive - eBOX X11

|X1 pin|Description|Signals|
|---|---|---|
|1| |L1|
|2| | |
|3| | |
|4| |N|
|5| | |
|PE| |PE|

Tab. 8 Mains cable port

|X2 pin|Description|Signals|
|---|---|---|
|1| |24 VDC|
|2| |GND|
|3| |CAN-high|
|4| |CAN-low|
|5| |CAN-GND|
|6| | |
|7| | |
|8| |PE|

Tab. 9 Manual terminal port

EN - 16
---
# 6 Putting into operation

|X11 pin|Description|
|---|---|
|A1|Encoder front drive|
|A2|Encoder front drive|
|A3|Encoder front drive|
|A4|Encoder front drive|
|A5|Encoder front drive|
|A6|Rear drive encoder|
|A7|Rear drive encoder|
|A8|Rear drive encoder|
|A9|Rear drive encoder|
|A10|Rear drive encoder|
|B1|Actual value encoder|
|B2|Actual value encoder|
|B3|Actual value encoder|
|B4|Actual value encoder|
|B5|Front drive|
|B6|Front drive|
|B7|Rear drive|
|B8|Rear drive|
|B9|Terminal strip|
|B10|Reset|
|C1|Inching|
|C2| |
|C3|Gas test|
|C4|Gas valve|
|C5|Gas valve|
|C6|Air blast valve|
|C7|Air blast valve|
|C8| |
|C9|CAT|
|C10|CAT|
|D1|Sensor|
|D2|Gas pressure controller|
|D3|Gas pressure controller|
|D4|Hood safety switch|
|D5|Hood safety switch|
|D6| |
|D7| |
|D8| |
|D9| |
|D10|End of wire|

# Tab. 10 M-Drive - eBOX control lead

|Signals| |
|---|---|
|Gnd| |
|5 V| |
|5 V Stby| |
|Ch A| |
|Ch B| |
|Gnd| |
|5 V| |
|5 V Stby| |
|Ch A| |
|Ch B| |
|5 V| |
|Gnd| |
|Ch A| |
|Ch B| |
|+| |
|-| |
|+| |
|-| |
|24 V for inching/init/reverse| |
|Switched back| |
|Switched back| |
|Switched| |
|24 V| |
|24 V switched Out22| |
|GND| |
|24 V switched Out24| |
|GND| |
|COM| |
|Normally closed switch| |
|Sensor| |
|24 V| |
|Switched back| |
|24 V| |
|Switched back| |
|GND| |
|24 V| |
|Switched back| |

EN - 17
---
# 6 Putting into operation

# eBOX

|X10 pin|Description|Signals|
|---|---|---|
|1| |24 VDC|
|2| |GND|
|3| |CAN - A|
|4| |CAN - B|
|5| |GND|
|6| | |
|7| | |
|8|Screen (PE)| |

Tab. 11 Manual terminal port (optional)

|X3 pin|Description|Signals|
|---|---|---|
|1|US1|24 VDC|
|2|US1|GND|
|3|US2|24 VDC|
|4|US2|GND|
|5| |PE|

Tab. 12 US1/US2 port (on AIDA version only)

|X13 pin|Description|Signals|
|---|---|---|
|A| |GND|
|B| |Arc|
|C| |Start (zero potential contact)|
|D| |Start (zero potential contact)|
|E| |Target hot wire output 0-10 V|
|F| |Power source ready|
|G| |24 VDC|
|H| |Detection 0-5 V or 0-10 V setpoint voltage|
|I| | |
|J| | |

Tab. 13 Port for the hot wire power source

Explanation:

The output setpoint voltage for the hot wire output is 0 - 10 VDC. If contacts I and J are bypassed, the output setpoint voltage for the hot wire output is 0 - 5 VDC.

EN - 18
---
# 7 Operation

# NOTICE

The eBOX may only be operated by qualified personnel (in Germany see TRBS 1203).

# 7.1 Control elements

| |1|2|3|4|5|6| | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|
|17|16|eBOX|15|14|13|12|11|10|9|8|7|
|1 eBOX status LED P1|6 Outlet air grille|10 Option|13 I/O interface port X2| | | | | | | | |
|2 Key-operated switch S1|7 Manual terminal port X10|11 Control lead port|14 Inlet air grille| | | | | | | | |
|3 Reset button S2|8 Hot wire power source port M-Drive or MF1 X11|12 US1/US2 port X3|16 Main switch Q1| | | | | | | | |
|4 Front drive status LED P2|9 Option (on AIDA version only)|15 Mains cable port X1|17 Ethernet/USB interface| | | | | | | | |

Fig. 11 eBOX control elements

# Symbol

Main switch Q1 (16) Fig. (11)

Switching state ON (LEDs illuminated in green, device fans running)

Switching state OFF (no power to the system)

Key-operated switch S1 (2) Fig. (11)*

Switch position: automatic: the wire feeder is fully functional when the cover (M-Drive) is closed

Switch position: manual: the protective device is bridged. The inching (wire feed) function is enabled when the cover (M-Drive) is open. The key can be removed in any position.

* Solely for systems with M-Drive; obsolete for other versions.

Reset button S2 (3) Fig. (11)

Press the button after eliminating a fault. The internal control system is reset to the starting position.

LED P3, rear drive (5) Fig. (11)

Status green = ready, status red, flashing = fault

LED P2, front drive (4) Fig. (11)

Status green = ready, status red, flashing = fault

EN - 19
---
# 8 Putting out of operation

NOTICE

- Please make sure that the shutdown procedures for all components mounted in the welding system are strictly observed before putting out of operation begins.

Fig. 11 eBOX control elements on page EN-19

1. Use the main switch (16) to cut the power to the eBOX.

# 9 Maintenance and cleaning

Scheduled maintenance and cleaning are prerequisites for a long service life and trouble-free operation.

DANGER

- Risk of injury due to unexpected start-up
- The following instructions must be adhered to throughout all maintenance, servicing, assembly, disassembly and repair work:

DANGER

- Electric shock
- Dangerous voltage due to defective cables.
- Check all live cables and connections for proper installation and damage.
- Replace any damaged, deformed or worn parts.

NOTICE

- Maintenance and cleaning work may only be carried out by qualified personnel (in Germany see TRBS 1203).
- Always wear your personal protective equipment when performing maintenance and cleaning work.
---
# 9 Maintenance and cleaning

# 9.1 Maintenance intervals

NOTICE

- The maintenance intervals given are standard values and refer to single-shift operation.

Overview of the pin assignment

Observe the instructions of the guideline EN 60974-4 Inspection and test during the operation of arc welding equipment as well as the laws and guidelines valid in the respective country. Check the following:

|Weekly|Monthly|Quarterly|
|---|---|---|
|-|Check, clean and, depending on the level of dirt, replace the air filters.|-|
|1. Open the air grilles (1) and (2) (snap-on closures), remove the air filters and air blast with dry compressed air. Replace the filters if necessary. 2. Insert the air filters into the air grilles (1) and (2) and re-attach the air grilles (1) and (2) to the housing.|1. Open the air grilles (1) and (2) (snap-on closures), remove the air filters and air blast with dry compressed air. Replace the filters if necessary. 2. Insert the air filters into the air grilles (1) and (2) and re-attach the air grilles (1) and (2) to the housing.|1. Open the air grilles (1) and (2) (snap-on closures), remove the air filters and air blast with dry compressed air. Replace the filters if necessary. 2. Insert the air filters into the air grilles (1) and (2) and re-attach the air grilles (1) and (2) to the housing.|

Tab. 14 Maintenance and cleaning

EN - 21
---
# 10 Troubleshooting

# DANGER

Risk of injury and machine damage when handled by unauthorized persons. Incorrect repair work and changes of the product may lead to significant injuries and machine damage. The product warranty will be rendered invalid if the unit is handled by unauthorized persons.

- Operating, maintenance, cleaning and repair work may only be carried out by qualified personnel (in Germany see TRBS 1203).

Please observe the attached document "Warranty". In the event of any doubts and/or problems, please contact your retailer or the manufacturer.

# NOTICE

- Please also consult the operating instructions for the welding components, such as the power source, welding torch system, re-circulating cooling unit etc.

|Fault|Cause|
|---|---|
|Unit is not ready for operation|- Control system or component defective
- Gas flow controller defective or set incorrectly
- M-Drive safety switch not actuated
|
|Wire is not fed|- Motor defective
- Defective control lead. No feed or only 100% feed possible
|
|LED does not illuminate|Fuse switched off|

# Tab. 15 Troubleshooting

Troubleshooting

- Ask a Binzel specialist to replace the defective control system or component
- Ask a Binzel specialist to check and set the gas flow controller
- Ask a Binzel specialist to check the switch
- Switch off the power to the system
- Ask a Binzel specialist to replace the motor
- Press the reset button
- Replace the feed system
- Check the control lead and the connectors. Replace the control lead if necessary
- Check that a power supply is available and/or if the light on the power supply unit illuminates. If not, replace the fuse

# 10.1 Reading the error memory

Please see the information on the SD card instruction leaflet BEI.0144.0 Tab. 2.

EN - 22
---
# 11 Disassembly

# DANGER

Risk of injury due to unexpected start-up. The following instructions must be adhered to throughout all maintenance, servicing, assembly, disassembly and repair work:

- Switch off the power source.
- Close the compressed air supply.
- Close the gas supply.
- Switch off the entire welding system.
- Disconnect the mains plug.

# NOTICE

- Disassembly may only be carried out by qualified personnel (in Germany see TRBS 1203).
- Observe also the operating instructions of the welding components, such as the MFS-V3 and welding torch system, re-circulating cooling unit etc.
- Observe the information provided in the following section: 8 Putting out of operation on page EN-20.

1. Disconnect the cable assembly from the wire feeder.
2. Disconnect the connection leads from the eBOX.

# 12 Disposal

When disposing of the system, local regulations, laws, provisions, standards and guidelines must be observed. To correctly dispose of the product, it must first be disassembled. Please take note of the following information: 11 Disassembly on page EN-23.

# 12.1 Materials

This product is mainly made of metallic materials, which can be melted in steel and iron works and are thus almost infinitely recyclable. The plastic materials used are labelled in preparation for their sorting and separation for later recycling.

# 12.2 Consumables

Oil, greases and cleaning agents must not contaminate the ground or enter the sewage system. These substances must be stored, transported and disposed of in suitable containers. Please observe the relevant local regulations and disposal instructions in the safety data sheets specified by the manufacturer of the consumables. Contaminated cleaning tools (brushes, rags, etc.) must also be disposed of in accordance with the information provided by the consumables’ manufacturer.

# 12.3 Packaging

ABICOR BINZEL has reduced the transport packaging to the necessary minimum. The ability to recycle packaging materials is always considered during their selection.
---
# 13 Options

# 13.1 Manual terminal for the MF control

Please see the information in operating instructions BAL.0389.0.

EN - 24