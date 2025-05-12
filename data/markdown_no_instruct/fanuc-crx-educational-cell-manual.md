# Robot CRX-10+A, CRX-10+A/L

# MECHANICAL UNIT

# OPERATOR'S MANUAL

B-84194EN/01

© FANUC CORPORATION, 2020
---
# Original Instructions

Thank you very much for purchasing FANUC Collaborative Robot. Before using the Robot, be sure to read the "SAFETY PRECAUTIONS" in this manual and understand the content.

- No part of this manual may be reproduced in any form.
- The appearance and specifications of this product are subject to change without notice.

The products in this manual are controlled based on Japan's “Foreign Exchange and Foreign Trade Law". The export from Japan may be subject to an export license by the government of Japan. Further, re-export to another country may be subject to the license of the government of the country from where the product is re-exported. Furthermore, the product may also be controlled by re-export regulations of the United States government. Should you wish to export or re-export these products, please contact FANUC for advice.

In this manual, we endeavor to include all pertinent matters. There are, however, a very large number of operations that must not or cannot be performed, and if the manual contained them all, it would be enormous in volume. It is, therefore, requested to assume that any operations that are not explicitly described as being possible are "not possible".
---
# SAFETY PRECAUTIONS

This chapter explains cautions for safety usage of FANUC collaborative robot. Robot cannot work without the end effector or peripheral equipment. By combined with the end effector and peripheral equipment and assembling the system, robot can demonstrate works. In other words the robot is one part of the system.

FANUC is not and does not represent itself as an expert in safety systems, safety equipment, or the specific safety aspects of your company and/or its workplace. It is the responsibility of the owner, employer, or user to take all necessary steps to guarantee the safety of all personnel in the workplace. The appropriate level of safety for your application and installation can best be determined by safety system professionals.

FANUC therefore, recommends that each customer consult with such professionals in order to provide a safe application. Additionally, robot system owner, it is your responsibility to arrange for the training of the operator of a robot system to recognize and respond to known hazards associated with robot to be aware of the recommended operating procedures. Because FANUC prepare for the professional training course of the robot, please use it.

It is recognized that the operational characteristics of robots can be significantly different from those of other machines and equipment. Robots are capable of high energy movements through a large volume beyond the base of robots. Although, robot is substitution for work at dangerous zone or harmful zone, but it may cause work-related accident by mistake. So perfect safety precautions for usage is required when installing it.

In order to prevent work-related accident by robot, as indicators of the steps that an employer should take each safe standard (JIS, ISO, IEC) are provided, these shows the contents for during installation and usage. This chapter provides some hints and guidelines for the robot system safety design.

Before using the FANUC collaborative robot, be sure to read this manual to become familiar with those contents.
---
# SAFETY PRECAUTIONS

# 1. DEFINITION OF WARNING AND CAUTION

To ensure the safety of users and prevent damage to the machine, this manual indicates each precaution on safety with "WARNING" or "CAUTION" according to its severity. Supplementary information is indicated by "NOTE". Please read each "WARNING", "CAUTION" and "NOTE" before using the robots.

|Symbol|Definitions|
|---|---|
|WARNING|Used if hazard resulting in the death or serious injury of the user will be expected to occur if he or she fails to follow the approved procedure.|
|CAUTION|Used if a hazard resulting in the minor or moderate injury of the user, or equipment damage may be expected to occur if he or she fails to follow the approved procedure.|
|NOTE|Used if a supplementary explanation not related to any of WARNING and CAUTION is to be indicated.|

• Check this manual thoroughly, and keep it handy for the future reference.

# 2. FANUC COLLABORATIVE ROBOT SYSTEM

# 2.1 OVERVIEW

The collaborative robot means the robot that work with workers. The robot system that is designed with following this manual, can admit the safety work of person near the moving robot.

System example: If the robot contacts to person, the robot stops.

This chapter explains cautions for safety usage of collaborative robot. So unless otherwise specified, in this manual, “robot” means “collaborative robot”.
---
# SAFETY PRECAUTIONS

# 2.2 PURPOSE OF ROBOT

FANUC Robot series can be used for the following applications.

- Arc welding
- Handling
- Assembling

Required functionality for these applications is implemented by selecting an appropriate TOOL software. Please consult your FANUC sales representative if you want to use the robot for any application other than listed above.

Even when you use the robot for the purpose of any of the applications listed above, the robot must not be under any of the conditions listed below. Inappropriate usage of robots may cause not only damage to the robot system, but also serious injury or even death of the user in the premises.

- Flammable atmosphere
- Explosive atmosphere
- Radioactive environment
- In water or any kind of liquid
- Use of robot for the purpose of transferring human or animals
- Use of robot as a step (climbing upon the robot)
- Outdoor
- Use of robot under conditions not in accordance with FANUC recommended installation or usage

FANUC is not responsible for any damage caused by misuse of the robots. Before using the robot, check the specifications of the robot, and then take adequate safety measures to prevent hazardous conditions.

# 2.3 CONFIGURATION OF ROBOT SYSTEM

The following elements has been verified their safety.

- Robot
- Robot controller
- Robot teach pendant
- End effector
- Other peripheral devices (machine)
- Workpiece

Users conduct risk assessment of robot system, and the following elements must be prepared by the user according to system configuration as the need arises.

- Safeguard
- Interlocked gate
- Interlocking device

Except the robot, the robot controller and the robot teach pendant depend on the system, so please them by users. FANUC Robot has an interface to connect interlocking devices. So confirm the specifications and design the interlock system.

Security is already confirmed against following components.

- Robot
- Robot controller and teach pendant

FANUC can not guarantee safety for end effector, other peripheral equipment and workpiece. System designer must design the system in consideration of security according to safety standard. Robot system designer must design the robot system to secure the security according to EN ISO 10218 (ANSI RIA ISO 10218) and Annex I of Machinery Directive.
---
# SAFETY PRECAUTIONS

# 2.4 DEFNITION OF THE USER

The user can be classified as follows.

# Collaborative worker

- Enter collaborative workspace, work with the robot
- Change the robot attitude by forcing robot directly, example push to escape function
- Restart the program with operator button set for collaborative worker.

# Operator:

- Turns robot controller power ON/OFF
- Starts robot program from operator’s panel

# Programmer:

- Operates the robot and performs the teaching using a teach pendant.
- Operates the robot and performs the teaching using the direct teach.

# Maintenance engineer:

- Operates the robot
- Teaches robot inside the safety fence
- Maintenance (repair, adjustment, replacement)

Programmer and maintenance engineer must be trained specialized training for the robot. Collaborative worker that may contact to robot must be informed regularly about the risks, emergencies and necessary safety measures.

**Table 2.4 (a) List of workings to the collaborative robot**
|Collaborative worker|Operator|Programmer or Teaching operator|Maintenance technician|
|---|---|---|---|
|Power ON/OFF for Robot controller|{|{|{|
|Select operating mode (AUTO, T1, T2)| |{| |
|Select Remote/Local mode| |{| |
|Select robot program with teach pendant| |{| |
|Select robot program with external device| |{| |
|Start robot program with operator’s panel|{|{| |
|Start robot program with teach pendant| |{| |
|Reset alarm with operator’s panel|{| | |
|Reset alarm with teach pendant|{| | |
|Set data on the teach pendant|{| | |
|Teaching with teach pendant|{| | |
|Teaching with direct teach|{| | |
|Emergency stop with operator’s panel|{|{|{|
|Emergency stop with teach pendant|{|{|{|
|Maintenance for operator’s panel| | | |
|Maintenance for teach pendant| | | |
|Enter collaborative workspace, work with the robot|{|{|{|
|Restart the program with operator button which is set for collaborative worker|{|{|{|
---
# SAFETY PRECAUTIONS

The collaborative worker, programmer and maintenance engineer take care of their safety using the following safety protectors as the need arises, for example.

- Adequate clothes, uniform, overall for operation
- Safety shoes
- Helmet
- Protective glasses

In addition, a user in this manual means collaborative worker, programmer, teaching operator and maintenance engineer.

# 2.4.1 Robot Training

When people access the robot, the collaborative robot may move and not stop. All people that may enter the area where the collaborative robots are placed must be trained following training:

- The worker must be trained for the characteristics of the collaborative robot. The characteristics of the collaborative robot are described in this manual. Especially, refer to Section 3.6 in SAFETY PRECAUTIONS in particular.
- Collaborative workers and operators working with collaborative robots may contact with the collaborative robot. The workers must be periodically trained for its dangers and methods to secure safety in emergencies.

The programmer, teaching operator and maintenance engineer must be trained for the robot operating and maintenance. The required items are:

- Robot basic knowledge
- Robot safety (laws, ordinances, labor security hygiene rule, safety precautions)
- Practice of jog feed
- Practice of robot manual operation and teaching
- Programming practice, teaching and playback practice
- Practice of automatic operation
- Explanation of configuration and function of robot
- Explanation and practice of setting up frame
- Explanation of interface between robot and peripheral device
- Explanation and practice of initial setting
- Explanation and practice of troubleshooting
- Explanation and practice of periodic checks and periodic replacement
- Explanation and practice of file input/output
- Explanation and practice of mastering
- Explanation and practice of disassemble and assemble of robots

Some training courses for these items for the maintenance engineer or system engineer are provided in the robot school and each technical service center. Contact your local FANUC representative.

# WARNING

Robot operating personnel such as programmers, teaching operators or maintenance engineers must be properly trained. Without appropriate training, any operation inside the safety fence may cause very severe injury or even death of personnel due to the multiple and various hazards caused by the robot arm.
---
# SAFETY PRECAUTIONS

# 2.4.2 Safety of the working person

Working person safety is the primary safety consideration. As it is very dangerous to enter the operating area of the robot during its automatic operation, adequate safety precautions must be observed. The following lists the general safety precautions. Careful consideration must be made to ensure working person safety.

1. We obligate the Working person to take a FANUC training courses. FANUC provides various training courses. Contact your local FANUC representative for details.
2. Even when the robot is stationary during operation, it is possible that the robot is still in a ready to move state, and is waiting for a signal. In this state, the robot is regarded as still in motion. To ensure working person safety, provide the system with an alarm to indicate visually or aurally that the robot is in motion.
3. Implement the Risk assessment, if necessary, install a safety fence with a gate so that no working person can enter the work area without passing through the gate. Install an interlocking device, a safety plug, and so forth in the safety gate so that the robot is stopped as the safety gate is opened. The controller is designed to receive this interlocking signal of the door switch. When the gate is opened and this signal is received, the controller stops the robot (Please refer to "STOP TYPE OF ROBOT" in SAFETY PRECAUTIONS for detail of stop type). For connection, refer to below Fig. 2.4.2 (b).
4. Provide the peripheral devices with appropriate grounding (Class A, Class B, Class C, and Class D).
5. Recommend to install the peripheral device outside of the work area.
6. Draw an outline on the floor, clearly indicating the range of the robot motion, including the tools such as a hand.
7. Implement the Risk assessment, if necessary, install a mat switch or photoelectric switch on the floor with an interlock to a visual or aural alarm that issues alarm with light, buzzer, or stops the robot when a working person enters the work area.
8. If necessary, install a safety lock so that no one except the working person in charge can turn the power on the robot controller. The circuit breaker installed in the controller is designed to disable anyone from turning it on when it is locked with a padlock.
9. When adjusting each peripheral device independently, make sure to turn the power off the robot controller.
10. Operators must take the gloves off while manipulating the operator’s panel or teach pendant. Operation with gloved fingers may cause an operation error.
11. Programs, system variables, and other information can be saved on memory card or USB memories. Be sure to save the data periodically in case the data is lost in an accident. (Refer to Controller maintenance manual.)
12. The robot must be transported and installed by accurate procedure recommended by FANUC. Wrong transportation or installation may cause the robot to fall, resulting in severe injury to workers.
13. In the first operation of the robot after installation, the operation should be restricted to low speeds. Then, the speed should be gradually increased to check the operation of the robot.
14. Before the robot is started, it should be checked that no one is in the area of the safety fence. At the same time, a check must be made to ensure that there is no risk of hazardous situations. If detected, such a situation should be eliminated before the operation.
---
# SAFETY PRECAUTIONS

(15) When connecting the peripheral devices related to stop (safety fence etc.) and each signal (external emergency, fence etc.) of robot, be sure to confirm the stop movement and do not take the wrong connection.

(16) In preparing the trestle, please secure the maintenance worker safety at high place in reference to Fig. 2.4.2 (c). Design with the Scaffolding and Safety-belt with circumspection.

# Fig. 2.4.2 (a) Safety fence and safety gate

RP1 Pulsecoder RI/RO, XHBK, XROT

RM1 Motor power/brake

EARTH

Safety fence

Interlocking device and safety plug that are activated if the gate is opened.

# WARNING

1. When you close a fence, make sure that no one is around the robot in closing the safety fence.
2. After the door interlock switch is actuated, robot slows down and stops within 2 seconds, and then servo power is cut off. Before cutting off the servo power, never enter the safeguarded area (inside of safety fence, etc.).

# Fig. 2.4.2 (b) Connection diagram for the signal of the safety fence

Main board For the R-30iB Mini Plus

EAS1, 24V-2, EAS2, 0V are on the main board.

Refer to the 3. ELECTRICAL CONNECTIONS of II. CONNECTION in R-30iB Mini Plus CONTROLLER MAINTENANCE MANUAL (B-84175EN) for details.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

# Hook for safety belt

# Fence

# Steps

# Trestle

# Footstep for maintenance

Fig. 2.4.2 (c) Footstep for maintenance

# 2.4.3 Safety of the Collaborative Worker

A collaborative worker indicates the personnel who work with collaborative robots, and if necessary, perform the start operation of the program with the operator button for collaborative workers. Because they may contact with the collaborative robot, they must periodically be trained about its danger and securing safety method at emergency.

# 2.4.4 Safety of the Operator

An “Operator” indicates a person who turns on and off the power to the robot system, and starts a robot program with the operator’s panel (in daily operation). Prohibit operators from working inside the safety fence.

1. If you don’t need to operate the robot, turn off the power to the robot controller, or press the “EMERGENCY STOP” button, and then proceed with your work.
2. Install a safety fence with a safety gate to prevent any worker other than the operator from entering the work area unexpectedly and the worker from entering a hazardous area.
3. Install one or more necessary quantities of EMERGENCY STOP button(s) within the operator’s reach in appropriate location(s) based on the system layout.

The robot controller is designed to be connected to an external EMERGENCY STOP button. With this connection, the controller stops the robot operation (Please refer to "STOP TYPE OF ROBOT" in SAFETY PRECAUTIONS for detail of stop type), when the external EMERGENCY STOP button is pressed. See the diagram below for connection.

# Emergency stop button

外部非常停止ボタン (Note)

|Main board|Connect EES1 and 24V-2, EES2 and 0V.|
|---|---|
|For the R-30iB Mini Plus|EES1, 24V-2, EES2, 0V are on the main board.|
|EES1|Refer to the 3. ELECTRICAL CONNECTIONS of II. CONNECTION in R-30iB Mini Plus CONTROLLER MAINTENANCE MANUAL (B-84175EN) for details.|
|24V-2| |
|EES2| |
|0V| |

Fig. 2.4.4 (a) Connection diagram for external emergency stop button
---
# SAFETY PRECAUTIONS

# 2.4.5 Safety of the Programmer

While teaching the robot, the operator must enter the work area of the robot. Especially the teach pendant operator must secure own safety.

1. Unless it is specifically necessary to enter the robot work area, carry out all tasks outside the area.
2. Before teaching the robot, check that the robot and its peripheral devices are all in the normal condition.
3. If it is inevitable to enter the robot work area to teach the robot, check the locations, settings, and other conditions of the safety devices (such as the EMERGENCY STOP button, the Enabling device (DEADMAN switch) on the teach pendant) before entering the area.
4. The programmer must be extremely careful not to let anyone else enter the robot work area.
5. Programming must be done outside of the safety fence as far as possible. If programming needs to be done in the area of the safety fence, the programmer must take the following precautions:
- Before entering the safety fence area, ensure that there is no risk of hazardous situation in the area.
- Be ready to press the emergency stop button whenever it is necessary.
- Operate the Robot at low speed.
- Before starting programming, check the entire system status to ensure that no remote instruction to the peripheral equipment or motion would harm working person.
6. Operator must work under the condition of Contact Stop function activates.
7. Required to deactivate the Contact Stop temporally, take measure to disseminate Contact Stop function deactivates.

Our operator panel is provided with an emergency stop button and a key switch (mode switch) for selecting the automatic operation mode (AUTO) and the teach modes (T1 and T2). Before entering the inside of the safety fence for the purpose of teaching, set the switch to a teach mode, remove the key from the mode switch to prevent other people from changing the operation mode carelessly, then open the safety gate. If the safety gate is opened with the automatic operation mode set, the robot stops (Please refer to "STOP TYPE OF ROBOT" in SAFETY PRECAUTIONS for detail of stop type). After the switch is set to a teach mode, the safety gate is disabled. The programmer should understand that the safety gate is disabled and is responsible for keeping other people from entering the inside of the safety fence.

Our teach pendant is provided with an enabling device (DEADMAN switch) as well as an emergency stop button. These button and switch function as follows:

1. Emergency stop button: Causes the stop of the robot (Please refer to "STOP TYPE OF ROBOT" in SAFETY PRECAUTIONS for detail of stop type) when pressed.
2. Enabling device (DEADMAN switch): Functions differently depending on the teach pendant enable/disable switch setting status.
- Enable: Servo power is turned off when the operator releases the enabling device (DEADMAN switch) or when the operator presses the switch strongly.
- Disable: The enabling device (DEADMAN switch) is disabled.

Note: The DEADMAN switch is provided to stop the robot when the operator releases the teach pendant or presses the pendant strongly in case of emergency. The R-30iB employs a 3-position enabling device (DEADMAN switch), which allows the robot to operate when the 3-position enabling device (DEADMAN switch) is pressed to its intermediate point. When the operator releases the enabling device (DEADMAN switch) or presses the switch strongly, the robot stops immediately.

The programmer intention of starting teaching is determined by the controller through the dual operation of setting the teach pendant enable/disable switch to the enable position and pressing the enabling device (DEADMAN switch). The programmer should make sure that the robot could operate in such conditions and be responsible in carrying out tasks safely.

Based on the risk assessment by FANUC, number of operation of enabling device (DEADMAN switch) should not exceed about 10000 times per year.
---
# SAFETY PRECAUTIONS

B-84194EN/01

The teach pendant, operator panel, and peripheral device interface send each robot start signal. However the validity of each signal changes as follows depending on the mode switch and the DEADMAN switch of the operator panel, the teach pendant enable switch and the remote condition on the software.

In case of operating the robot as a collaborative robot without safety fence, there may be a possibility that robot will not stop even personnel approach. In that case, the robot will suspend when personnel contact.

|Mode|Teach pendant enable switch|Software remote condition|
|---|---|---|
|AUTO|On|Local|
| |Off|Local|
| | |Remote|
|T1, T2|On|Local|
| |Off|Local|
| | |Remote|

T1,T2 mode: Enabling device (DEADMAN switch) is effective.

|Teach pendant|Operator panel|Peripheral device|
|---|---|---|
|Not allowed|Not allowed|Not allowed|
|Not allowed|Not allowed|Not allowed|
|Not allowed|Allowed to start|Not allowed|
|Not allowed|Not allowed|Allowed to start|
|Allowed to start|Not allowed|Not allowed|
|Allowed to start|Not allowed|Not allowed|
|Not allowed|Not allowed|Not allowed|
|Not allowed|Not allowed|Not allowed|

(6) To start the system using the operator’s panel, make certain that nobody is in the robot work area and that there are no abnormal conditions in the robot work area.

(7) When a program is completed, be sure to carry out the test operation according to the following procedure.

1. Run the program for at least one operation cycle in the single step mode at low speed.
2. Run the program for at least one operation cycle in the continuous operation mode at low speed.
3. Run the program for one operation cycle in the continuous operation mode at the intermediate speed and check that no abnormalities occur due to a delay in timing.
4. Run the program for one operation cycle in the continuous operation mode at the normal operating speed, and check that the system operates automatically without trouble.
5. After checking the completeness of the program through the test operation above, execute it in the automatic operation mode.

(8) While operating the system in the automatic operation mode, the teach pendant operator must leave the robot work area.

# 2.4.6 Safety of the Maintenance Engineer

For the safety of maintenance engineer personnel, pay utmost attention to the following.

1. Must never be in the area during its operation.
2. A hazardous situation may occur when the robot or the system are kept with their power-on during maintenance operations. Therefore, for any maintenance operation, the robot and the system must be put into the power-off state. If necessary, a lock should be in place in order to prevent any other person from turning on the robot and/or the system. In case maintenance needs to be executed in the power-on state, the emergency stop button must be pressed.
3. If it becomes necessary to enter the robot operation area while the power is on, press the emergency stop button on the operator panel, or the teach pendant before entering the area. The maintenance personnel must indicate that maintenance work is in progress and be careful not to allow other people to operate the robot carelessly. (See Section 4.5.)
4. When entering the area enclosed by the safety fence, the maintenance worker must check the entire system in order to make sure that there is no dangerous situation around. In case the worker needs to enter the safety area whilst a dangerous situation exists, extreme care must be taken, and entire system status must be carefully monitored.
5. Before the maintenance of the pneumatic system is started, the supply pressure should be shut off and the pressure in the piping should be reduced to zero.
---
# SAFETY PRECAUTIONS

1. Before teaching, check the robot and its peripheral devices are all in the normal condition.
2. Do not operate the robot in the automatic mode while anybody is in the robot work area.
3. Make certain that their escape path is not obstructed inside the safety fence, or the robot operation area. Provided, however, that the robot secure the operation as a collaborative robot.
4. When a tool is mounted on the robot, or any moving device other than the robot is installed, such as belt conveyor, careful attention required for those motion.
5. Assign an expert near the operator panel who can press the EMERGENCY STOP button whenever he sees the potential danger.
6. In case of replacing a part, please contact your local FANUC representative. Wrong procedure may cause the serious damage to the robot and the worker.
7. Make sure that no impurity into the system in while (in) replacing or reinstalling components.
8. Turn off the circuit breaker to protect against electric shock in handling each unit or printed circuit board in the controller during inspection. If there are two cabinets, turn off both circuit breakers.
9. A part should be replaced with a part recommended by FANUC. If other parts are used, malfunction or damage would occur. Especially, a fuse that is not recommended by FANUC should not be used. Such a fuse may cause a fire.
10. When restarting the robot system after completing maintenance work, make sure in advance that there is no person in the work area and that the robot and the peripheral devices are not abnormal.
11. In case of remove the motor or brake, suspend the arm by crane or other equipment beforehand to avoid falling.
12. Whenever grease is spilled on the floor, remove them as soon as possible to prevent from falling.
13. The following parts are heated. If a maintenance worker needs to touch such a part in the heated state, the worker should wear heat-resistant gloves or use other protective tools.
- Servo motor
- Inside of the controller
- Reducer
- Gearbox
- Wrist unit
14. Maintenance must be done with appropriate lighting. Be careful that those lighting will not cause any further danger.
15. When a motor, reducer, or other heavy load is handled, a crane or other equipment should be used to protect maintenance workers from excessive load. Otherwise, the maintenance workers would be severely injured.
16. Must never climb or step on the robot even in the maintenance. If it is attempted, the robot would be adversely affected. In addition, a misstep can cause injury to the worker.
17. Secure footstep and wear the safety belt in performing the maintenance work in high place.
18. Remove all the spilled oil or water and metal chips around the robot in the safety fence after completing the maintenance.
19. All the related bolts and components must return to the original place in replacing the parts. If some parts are missing or left (remained), repeat the replacement work until complete the installation.
20. In case robot motion is required during maintenance, the following precautions should be taken:
- Secure an escape route. And during the maintenance motion itself, monitor continuously the whole system so that your escape route will not become blocked by the robot, or by peripheral equipment.
- Keep vigilant attention for the potential danger and to press the emergency stop button whenever it is necessary.
21. Periodic inspection required. (Refer to the robot mechanical manual and controller maintenance manual.) A failure to do the periodical inspection can adversely affect the performance or service life of the robot and may cause an accident.
22. After replacing some parts, a test run required by the predetermined method. (See TESTING section of “Controller operator’s manual”. During the test run, the maintenance staff must work outside the safety fence as the need arises.
23. Make certain that their escape path is not obstructed inside the safety fence, or the robot operation area. Provided, however, that the robot secure the operation as a collaborative robot.
---
# SAFETY PRECAUTIONS

# 2.5 RELEVANT STANDARDS

FANUC robot series meets following standards.

[For CE marking : Machinery/Low voltage Directives]

- EN ISO 10218‑1
- EN 60204‑1
- EN/ISO 13849‑1

[For NRTL]

- UL 1740
- CAN/CSA Z434
- CSA C22.2 No.73

NOTE

For ISO 13849-1 the following safety categories have been applied.

|Emergency Controller model|stop| | | | |
|---|---|---|---|---|---|
|R-30iB Mini Plus [7DA5 or later]|Cat.4|PL e|SIL 3| | |
| |Dual Check Safety (optional functions)|Applied|Position/ Speed check|Safe I/O|Safety Network|
|[7DA5 or later]|Cat.3|Cat.4|EN ISO 13849-1:2015| | |
|PL d|PL e|SIL 2|SIL 3| | |

|Controller model|Collaborative robot function|Applied|(Collaborative robot safety function)|standard|
|---|---|---|---|---|
|R-30iB Mini Plus|Cat.3|EN ISO 13849-1:2015|PL d| |

[CE marking : For EMC Directive]

- EN 55011 (Group 1, Class A)
- EN 61000‑6‑2

For the above standards, FANUC robot systems have been certified by the following third parties.

- CE marking : TÜV Rheinland Japan, TÜV SÜD Japan
- NRTL : TÜV SÜD America
---
# SAFETY PRECAUTIONS

# 3 ROBOT SYSTEM DESIGN

In this chapter, requirements for robot system design are described.

- Placement of Equipment
- Power Supply and Protective Earth Connection
- Other Precautions

In addition, the basic requirements for end effector, workpiece, and peripheral equipment are outlined in 3.5 in SAFETY PRECAUTIONS. The characteristic of collaborative robot are outlined in 3.6 in SAFETY PRECAUTIONS.

About the safety fence, safety gate and other protection devices, refer to Section 4.5 to 4.7 in SAFETY PRECAUTIONS.

Collaborative robot applications are different from traditional robot systems because of the capability of the robot to operate in close proximity to a person in the robot’s operating space without an enabling device. Guidance in ISO 10218-2 (ANSI/RIA R15.06-2012) should be followed in the construction of the robot system using collaborative robots.

In ISO10218-2, carrying out risk assessment (a dangerous evaluation) for the whole robot system is demanded. Depending on a result of the risk assessment (a dangerous evaluation), please carry out appropriate safe protection plan to reduce the risk that a person injures.

# 3.1 GENERAL

The robot system must be designed, constructed, and implemented so that in case of a foreseeable failure of any single component, whether electrical, electronic, mechanical, pneumatic, or hydraulic, safety functions are not affected or when they are, the robot system is left in a safe condition (“Failure to safety”).

Under the intended conditions of use, the discomfort, fatigue and psychological stress faced by the operator must be reduced to the minimum possible, taking into account ergonomic principles such as:

- allowing for the variability of the collaborative worker and operator’s physical dimensions, strength and stamina,
- providing enough space for movements of the parts of the collaborative worker and operator’s body,
- avoiding a machine-determined work rate,
- avoiding monitoring that requires lengthy concentration,
- adapting the man/machinery interface to the foreseeable characteristics of the collaborative worker and operators.

ISO10218-2 requires performing risk assessment for the whole robot system. The application of the electrical equipment of the robot system must be accordance with IEC/EN60204-1 or NFPA70/NFPA79.
---
# SAFETY PRECAUTIONS

# 3.2 PLACEMENT OF EQUIPMENT

Please make sure the following requirements are all satisfied for each component of a robot system.

- Be sure to perform the risk assessment and be sure to design the appropriate safeguarding measures.
- An appropriate safety fence/guard must be placed according to the safety standards. Please refer to section 3.5 and 3.6 in SAFETY PRECAUTIONS for the basic requirement of the safety fence/guard and protection devices.
- As the need arises, the additional space are required beyond the restricted space to define the safeguarded space.
- The operator panel must be located at a safe place:
- outside the safety fence, and cannot be reached from inside the safety fence, if the robot system has safety fence.
- where it can be easily seen, and easily operated by the operator,
- where the operator can operate it without hesitation or loss of time and without ambiguity,
- where collaborative worker or operator can confirm the emergency stop button easily and can operate it easily, and
- where no dangerous situation is created by operating it.
- If the robot controller is placed inside or near the robot operating space, the distance between the maintenance space of robot controller and robot operating space should be sufficient (over 1.22m from the opening section of robot controller, or opening section of robot controller is placed to opposite direction of robot operating space).
- The operating position must be designed and constructed in such a way as to avoid any risk due to exhaust gases and/or lack of oxygen.
- If the robot system is intended to be used in a hazardous environment presenting risks to the health and safety of the collaborative worker and operator or if the robot system itself gives rise to a hazardous environment, adequate means must be provided to ensure that the operator has good working conditions and is protected against any foreseeable hazards.
- Where appropriate, the operating position must be fitted with an adequate cabin designed, constructed and/or equipped to fulfill the above requirements. The exit must allow rapid evacuation. Moreover, when applicable, an emergency exit must be provided in a direction which is different from the usual exit.
- A large space must be secured around each component enough for the maintenance and inspection of the robot system.
- The robot system must be designed and constructed in such a way as to allow access in safety to all areas where intervention is necessary during operation, adjustment and maintenance.
- The space inside or near the robot operating space for maintenance and inspection must be designed to protect the user from falling off or slipping off the step, and where appropriate, handholds that are fixed relative to the operator and that enable them to maintain their stability should be prepared.
- The robot system must be secured on a stable floor. Especially the robot mechanical unit must be attached to the stable place according to the instructions in the maintenance manual or operator’s manual.
---
# SAFETY PRECAUTIONS

- The robot system must be designed to avoid trapping and collision between the moving parts of the robot and other fixed or moving objects.
- The layouts must be designed in such a way that between moving parts of the robot and objects in the environment (e.g. pillars of the structure, ceiling joists, fences, supply leads) sufficient clearance is available.
- When T2 mode is used, the following clearance is required for robot system installation.
- 0.5m or more from readily accessible areas of buildings, structures, utilities, other machines and equipment not specifically supporting the robot function that may create trapping or a pinch point. Where this minimum clearance is not provided, additional safeguarding devices are required.
- Stop robot motion while personnel are within 0.5m of the trapping or pinch hazard. If these actions are not applied, it may cause injury to the users.
- When a limitation of the restricted space, by limiting the range of motion of the primary axes (J1, J2, J3-axes), is required by the plan, limiting devices must be provided. They should not cause injury to a person and must comply with one of the following:
- Mechanical stoppers which are capable of stopping the robot at any adjusted position when it is carrying its rated load at maximum velocity.
- Alternative methods of limiting the range of motion may be provided only if they are designed, constructed, and installed to achieve the same level of safety as the mechanical stoppers. This may include using the robot controller and limit switches according to IEC/EN 60204-1 or NFPA70/NFPA79. Note that the limiting devices must be correctly adjusted and secured.
- When it is intended that collaborative workers or operators will perform manual operations associated with the robot, such as loading and unloading of parts, this must be taken into account in the arrangement of the robot system, either by providing part loading devices so that the operator cannot access the hazardous area, or by providing appropriate safeguards for the manual activity.
- Where appropriate and where the working conditions so permit, work stations constituting an integral part of the robot system must be designed for the installation of seats.
- The operator’s seat must enable him or her to maintain a stable position. Furthermore, the seat and its distance from the operator's panel must be capable of being adapted to the operator.
- If the robot system is subject to vibrations, the seat must be designed and constructed in such a way as to reduce the vibrations transmitted to the operator to the lowest level that is reasonably possible. The seat mountings must withstand all stresses to which they can be subjected; where there is no floor beneath the feet of the operator, footrests covered with a slip-resistant material must be provided.
- On transportation of robot mechanical unit or controller, proper transportation procedure described in the operator’s or maintenance manual for each model has to be followed.

# WARNING

Follow the procedure specified by FANUC when transporting the robot mechanical unit or controller. Otherwise, it may fall over due to the loss of the mechanical stability (balance), resulting in serious injury or death of personnel.
---
# SAFETY PRECAUTIONS

# 3.3 POWER SUPPLY AND PROTECTIVE EARTH CONNECTION

- The power supply and the grounding must be connected according to the maintenance manual.
- Unsafe conditions must be avoided in the event of a power down, power recovery after a power down or supply voltage fluctuations. Unsafe conditions to be avoided are:
- Dropping workpiece or any material,
- Safety equipment not functioning, etc.
- WARNING

Dropping workpiece or any material may result in personal injury.

The robot system must have means to isolate its power sources. These means must be located in such a way that no person will be exposed to any hazard, as well as must have a lockout/tagout capability.

# 3.4 OTHER PRECAUTIONS

- Shutdown (removal of power) to the robot system or any peripheral equipment must not result in a hazardous condition.
- All environmental conditions must be evaluated to ensure compatibility of the robot and the robot system with the anticipated operational conditions. These conditions include, but are not limited to, explosive mixtures, corrosive conditions, humidity, dust, temperature, electromagnetic interference (EMI), radio frequency interference (RFI), and vibration.
- The control position where the operator stands must be predetermined. The control position must satisfy the following conditions:
- The operator can easily operate the operator panel or the teach pendant.
- The operator can easily make sure that nobody is inside or near the robot operating space or inside the safety fence (if safety fence is placed).
- The operator can easily verify the operation of the system.
- The operator can immediately stop the entire or partial system in the event of a malfunction of the system or any dangerous condition.
- The following safety measures must be used if the operator cannot easily verify nobody is inside the safety fence, or as required by the risk-assessment result:
- A visible/audible warning (complying EN/ISO/IEC standards or OSHA) is used before the robot starts moving.
- A measure for the collaborative worker inside or near the robot operating space to stop the robot system or a measure for the person to evacuate outside the robot operating space.
- The control system is designed and constructed in such a way that starting is prevented while someone is in the danger zone.
- If necessary, means must be provided to ensure that the robot system can be controlled only from control positions located in one or more predetermined zones or locations.
---
# SAFETY PRECAUTIONS

- Where there is more than one control position, the control system must be designed in such a way that the use of one of them precludes the use of the others, except for stop controls and emergency stops.
- When the robot system has two or more operating positions, each position must be provided with all the required control devices without the operators hindering or putting each other into a hazardous situation.
- The manual intervention and reset procedure to restart the robot system after an emergency stop must take place outside the restricted space.
- A warning device must be such that the operator and people in the dangerous area can easily recognize it.
- For UL standard compliance, “a yellow or amber visual indicator” specified by CL 36.1 of UL 1740 was to be installed by the end-user or system manufacturer. SYSRDY or PROGRUN output signals are available for installing such a visual indicator.
- The area must be appropriately lighted, especially for maintenance and inspection. The lighting must not create a new dangerous situation (e.g. dazzled).
- CAUTION

Operation inside of the safety fence (teaching, maintenance, etc.) without suitable ambient lighting can cause hazards of collision (with some obstacles inside of the safety fence) or slipping/falling down of personnel.
- It is recommended that adjustment, greasing or oiling, and other maintenance work can be performed from outside the dangerous area while the system is stopping. If it is not feasible, a method to perform these operations safely must be established.
- If the robot and the peripheral equipment synchronously move in the robot system, an appropriate measure must be provided to avoid unsafe conditions by stopping the entire system in the event any of the equipment stops due to malfunction.
- Any robot that can be controlled from a remote location must be provided with an effective means that must prevent hazardous conditions of the robot being initiated from any other location.
- It is recognized that for certain phases of the robot system life (e.g. commissioning, process changeover, cleaning, and maintenance) it may not be possible to design completely adequate safeguards to protect against every hazard or that contain safeguards may be suspended. Under these conditions, appropriate safe working procedures must be used.
- A robot system manufacturer must provide an operation manual according to EN ISO 10218 etc.
- Requirements of each safety standard (EN ISO, IEC, JIS etc.) and labor security hygiene rule must be considered when a robot application system is designed.
- Keep the component cells of the robot system clean, operate the robot where insulated from the influence of grease, water, and dust.
- Don’t use unconfirmed liquid for cutting fluid and cleaning fluid.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

- Adopt limit switches or mechanical stoppers to limit the robot motion, and avoid the robot from collisions against peripheral devices or tools.
- Observe the following precautions about the mechanical unit cables. Failure to follow precautions may cause mechanical troubles.
- Use mechanical unit cable that have required user interface.
- Do not add user cable or hose to inside of mechanical unit.
- Please do not obstruct the movement of the mechanical unit cable when cables are added to outside of mechanical unit.
- In the case of the model that a cable is exposed, please do not perform remodeling (Adding a protective cover and fix an outside cable more) obstructing the behavior of the outcrop of the cable.
- When installing user peripheral equipment on the robot mechanical unit, please pay attention that equipment does not interfere with the robot itself.
- The frequent power-off stop for the robot during operation causes the trouble of the robot. Please avoid the system construction that power-off stop would be operated routinely. (Refer to bad case example.) Please execute power-off stop after reducing the speed of the robot and stopping it by hold stop or cycle stop when it is not urgent. (Please refer to "STOP TYPE OF ROBOT" in SAFETY PRECAUTIONS for detail of stop type.)
- (Bad case example)
- Whenever poor product is generated, a line stops by emergency stop and power-off of the robot is executed.
- When alteration was necessary, safety switch is operated by opening safety fence and power-off stop is executed for the robot during operation.
- An operator pushes the emergency stop button frequently, and a line stops.
- An area sensor or a mat switch connected to safety signal operates routinely and power-off stop is executed for the robot.
- Power-off stop is regularly incurred due to an inappropriate setting for Dual Check Safety (DCS).
- Power-off stop of Robot is executed when collision detection alarm (SRVO-050) etc. occurs. Please try to avoid unnecessary power-off stops. It may cause the trouble of the robot, too. So remove the causes of the alarm.
- Operating the robot in the jog mode, set it at an appropriate speed so that the operator can manage the robot in any eventuality.
- Before pressing the jog key, be sure to comprehend the robot movement by the key in advance.
---
# SAFETY PRECAUTIONS

# 3.5 END EFFECTOR, WORKPIECE AND PERIPHERAL EQUIPMENT

It is the responsibility of the robot system manufacturer to perform the risk assessment of the end effector, workpiece and peripheral equipment. This section outlines the basic requirement for the risk assessment of these components.

# End Effector

- End effectors must be designed and constructed, or safeguarded, so that
- power failure does not cause release of the load (workpiece) or result in a hazardous condition.
- The static and dynamic forces created by the load (workpiece) and the end effector together are within the load capacity and dynamic response of the robot.
- Shape or motion of the end effector does not harm the personnel.
- We recommend to protect the hard part with sponges, and relax the force when the personnel contact it.
- If it is equipped with a tool that can function with several different conditions (speed, etc.), the selection of the condition must be safely and securely done.

# Workpiece

- The material and its shape must not be dangerous and if unsafe, safety measures must be provided.
- If the workpiece is in extreme high or low temperature, safety measures must be provided to avoid personnel from touching or getting too close to it.

# WARNING

Dropping workpiece or any material may result in personal injury.

# Peripheral Equipment (including end effector)

- The material and shape must not be dangerous.
- If any component could break down during operation, it must be placed so that it will not scatter if it breaks down.
- Pipes (for liquid/gas) must have enough strength for its internal / external pressure.
- Pipes must be secured and protected from the external pressure or tension.
- Be sure to provide measures to avoid a dangerous situation if a pipe is broken causing sudden movement of the pipe or the high speed flow of material.
- If a pneumatic device is used, be sure to install an air valve which shuts off the air supply to the robot.
- If a power source other than the electricity (e.g. pneumatic, water, heat) is used in the system, be sure to perform appropriate risk-assessment, and be sure to provide appropriate safety measures.
---
# SAFETY PRECAUTIONS

B-84194EN/01

- Be sure to provide safety measures to avoid swapping of components that cause unsafe conditions, by
- design to avoid mount mistakes,
- indication of necessary information on the parts.
- Be sure to provide safety measures to avoid inferior contacts, by
- design,
- displaying the information on the connectors, pipes and cables.
- Be sure to provide safety measures to avoid an unsafe condition by touching an extremely high/low temperature parts (if any).
- Be sure to provide safety measures to avoid fire or explosion through sufficient amount of investigation.
- Vibration and sound noise must be kept to a minimum.
- For place where personnel may contact, get rid of sharp points and rough surfaces, because those may harm personnel by contact.
- If a laser equipment is used, the following must be considered.
- avoid unexpected emission of laser light
- direct/indirect emission of light must give no harm to the health
- laser light must give no harm to health during maintenance / adjustment.

# 3.6 THE CHARACTERISTIC OF COLLABORATIVE ROBOT AND LIMITATIONS AND USAGE NOTES

This section describes that the characteristic of collaborative robot and limitations and usage notes. Refer to Collaborative Robot Function OPERATOR’S MANUAL (B‑83744EN) about the detail of each function.

# CONTACT STOP FUNCTION

- When the external force exceeds the external force limit, the robot stops. Example, when a person contacts to robot and big external force add to robot, the robot stops. This function does not guarantee safety in the all situation. The notice must be followed and additional appropriate safeguarding measures must be placed as the need arises.

※External force：Force to act on the robot at the time of contact by the robot motion.
- The external force is calculated by the torque acting on each axis. Therefore, when the robot contacts at the point near the each axis, the robot may not stop even if the external force is more than the external force limit. On the other hand, when the robot contacts at the point far from the each axis, the robot may stop even if the external force is smaller than the external force limit.
- A default value of external force limit is 150N. The sensitivity of contact stop can be increased by decreasing the external force limit. But in case of increasing sensitivity, the robot may stop by misdetecting the contact depending on the motion of the robot. The external force limit can’t increase more than 150N.
- There is a function which resume the program automatically after contact stop. If this function is effective, Even if the robot stops, program is restarted automatically when required condition is met.
---
# SAFETY PRECAUTIONS

# WARNING

Motion groups other than Collaborative robot are outside of the scope of the contact stop function. If a person comes into contact with the motion group other than Collaborative robot, a serious personal injury could result. If the robot system is designed to include the motion group other than Collaborative robot, adequate risk assessment for the whole robot system is necessary to verify that the motion group other than Collaborative robot are outside of the scope of the contact stop function.

# ACCEPTABLE MOTION SPEED FOR BODY REGIONS

Be sure to set motion speed in order to prevent injury caused by the force of contact to a sensitive area as determined by the risk assessment. Please note that a default value of collaborative motion speed is 250mm/s, and the maximum setting value is 1000mm/s. For reference, acceptable motion speed for body regions are shown below.

|Body region|Acceptable motion speed (mm/s)|
|---|---|
|Face, Neck|Not applicable|
|Arm, Hand, Fingers|1000|
|Thigh, knee|250|
|Lower legs|Not applicable|
|Body region excluding the above region|300|

# RESTART AFTER CONTACT STOP

Restart by the switch installed near the robot is possible. In that case, be sure to install the emergency stop button near the restart switch.

# PUSH TO ESCAPE

When a person pushes the robot, the robot escapes. Only J1 axis, J2 axis and J3 axis can respectively escape by pushing. The robot stops after certain distance escape. In this case, release your hand for a moment and push again. When the robot escapes, the attitude of TCP changes.

# RETREAT AFTER CONTACT STOP

When the robot was stopped by the contact stop and if strong force to robot remains, the robot will retreat slightly.

# NOTE TO DESIGN THE COLLABORATIVE WORKSPACE

When the designer of a robot application system designs the workspace where person work near robot, the designer must follow the following notes.

# WARNING

When person is pinched between the robot and the other object (wall, floor, etc.), and the robot arm, it may result in personal injury.

The space where a person escapes at contacting to robot must be placed between collaborative workspace and wall, floor, etc. If the space can’t be placed, the robot system must be designed to use additional appropriate safeguarding measures. Example, when a person access to dangerous space, the robot stops.

The following countermeasure is effective as a measure to reduce the generation force when pinching between the robot and the other object.

- Reduce the robot's motion speed near the place where pinching is occurred.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

- Cover the object or the table with a soft material because the lower the rigidity of the contact point, the smaller the generated force.
- Untrained (according to Subsection 2.4.1) people must not enter collaborative workspace.
- The ambient working space in which people may collide with the collaborative robot shall be arranged so they can move safely.

# WARNING

Inappropriate collaborative workspace may result in personal injury.

# WORKING NOTE INSIDE THE COLLABORATIVE WORKSPACE

- Please don't put any objects on the robot. Foreign objects may cause an improper detection of the external contact seen by the robot.
- When people enter the collaborative workspace, please take care of their safety using the personal protective equipment (helmet, safety shoes, protective glasses etc.), as the need arises.

# INDICATION OF COLLABORATION MODE

The visual indication, for example lamp, indicating that the robot is in collaborative operation is necessary. The LED installed on the robot is set for this purpose. The LED color differs depending on the robot status according to the following table.

|LED color|Robot status|
|---|---|
|Green|Collaborative mode|
|Flash green|Direct teaching|
|Yellow|High speed mode|
|Red|Alarm occurrence|

Fig. 3.6 (b) LED on the robot
---
# SAFETY PRECAUTIONS

# PROTECT OF HEAD, NECK

# WARNING

An impact force to the head or neck from contact with the robot may cause death or heavy injury of the users.

- The robot system must be designed not to contact robot to head or neck of person with frequency.

# WARNING

If a part of body is pinched, it might cause heavy injury.

- When wrist unit or J3 arm approaches J1 base or J2 base, a part of your body may be pinched.

# EXTERNAL FORCE AGAINST THE ROBOT

- If force generated from the end effector, force of pushing direction or pulling direction generated from the cables and hoses connected to the end effector exceeds the restriction value of the external force, design a system during considering to avoid force mentioned above is applied to the robot.
- For information of the external force and load monitoring method, refer to Subsection 4.2.2 “Payload Monitor” of the OPERATOR’S MANUAL (Collaborative Robot Function) (B‑83744EN).

# HIGH SPEED MODE

- By default, the speed of the collaborative robot is limited by 1000mm/s. but robot can move with over this speed. If operating robot with 1000m/s or more, risk assessment for traditional robot (no‑collaborative) is required and additional appropriate safeguarding measures is required as the need arises. The basic safeguarding measures is safeguarding fence, but other safeguarding measures that is result of risk assessment may be admitted.
- Contact stop function is not available with this mode.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

# 4 SAFETY DEVICES

# 4.1 STOP TYPE OF ROBOT

There are following three types of Stop Category.

# Stop Category 0 following IEC 60204-1 (Power-off Stop)

Servo power is turned off, and the robot stops immediately. Servo power is turned off when the robot is moving, and the motion path of the deceleration is uncontrolled.

“Stop Category 0” performs following processing.

- An alarm is generated, and then the servo power turns off. Instantly the robot stops.
- Execution of the program is paused.

Frequent Category 0 Stop of the robot during operation can cause mechanical problems of the robot. Avoid system designs that require routine or frequent Category 0 Stop conditions.

# Stop Category 1 following IEC 60204-1 (Controlled Stop, Smooth Stop)

The robot is decelerated until it stops, and servo power is turned off.

“Stop Category 1” performs following processing.

- The alarm "SRVO-199 Controlled stop" or "SRVO-289 Smooth Stop" occurs along with a decelerated stop. The program execution is paused.
- An alarm is generated, and then the servo power turns off.

In Smooth stop, the robot decelerates until it stops with the deceleration time shorter than Controlled stop. The stop type of Stop Category 1 is different according to the robot model or option configuration. Please refer to the operator's manual of a particular robot model.

# Stop Category 2 following IEC 60204-1 (Hold)

The robot is decelerated until it stops, and servo power remains on.

“Stop Category 2” performs following processing.

- The robot operation is decelerated until it stops. Execution of the program is paused.
---
# SAFETY PRECAUTIONS

# WARNING

1. The stopping distance and time of Stop Category 1 are longer than those of Stop Category 0. A risk assessment for the whole robot system which takes into consideration the increased stopping distance and stopping time is necessary when Stop Category 1 is used. Please refer to the operator's manual of a particular robot model for the data of stopping distance and time.
2. In multi arm system, the longest stopping distance and time of Stop Category 1 among each robot are adopted as those for the system. A risk assessment for the whole robot system which takes into consideration a possibility that the stopping distance and time increase, is necessary on the multi arm system.
3. In the system which has extended axis, the longer stopping distance and time of Stop Category 1 among robot and extended axis are adopted as those for the system. A risk assessment for the whole robot system which takes into consideration a possibility that the stopping distance and time increase, is necessary on the system which has extended axis. Please refer to the extended axis setup procedure of the controller operator’s manual for considering the stopping distance and time of the extended axis.
4. When Stop Category 1 occurs during deceleration by Stop Category 2, the stop type of robot is changed to Stop Category 0.
5. In case of Stop Category 1, motor power shutdown is delayed for a maximum of 2 seconds. In this case, a risk assessment for the whole robot system is necessary, including the 2 seconds delay.

When the emergency stop button is pressed or the FENCE is open, the stop type of robot is Stop Category 0 or Stop Category 1. The configuration of stop type for each situation is called stop pattern. The stop pattern is different according to the option configuration.

# Stop Pattern

|Stop pattern|Emergency stop button|External Emergency stop|FENCE open|SVOFF input|Enabling device (Deadman switch) (*)|
|---|---|---|---|---|---|
|AUTO|Category 1|Category 1|Category 1|Category 1|-|
|D|T1|Category 1|Category 1|-|Category 1|
| |T2|Category 1|Category 1|-|Category 1|

Category 0: Stop Category 0

Category 1: Stop Category 1

-: Disable

(*) The stop pattern of NTED input is same as enabling device (Deadman switch).

The following table indicates the Stop pattern according to the controller type or option configuration.

|Option|R-30iB Mini Plus|
|---|---|
|Standard|D(**)|

(**) R‑30i B Mini Plus does not have SVOFF input.

The stop pattern of the controller is displayed in "Stop pattern" line in software version screen. Please refer to "Software version" in operator's manual of controller for the detail of software version screen.
---
# SAFETY PRECAUTIONS

# 4.2 EMERGENCY STOP

This robot has following emergency stop devices.

- emergency stop button (They are on the operator panel and teach pendant.)
- external emergency stop (input signal)

When emergency stop button is pushed, the robot stops immediately (refer to Section 3.1). The external emergency stop input signal is input from peripheral devices. The signal terminal is inside of the robot controller.

# 4.3 MODE SELECT SWITCH

The MODE SELECT SWITCH is installed on the robot controller. (This is an option for some controllers.) You can select one of the operation modes using this switch. The selected operation mode can be locked by removing its key. When the mode is changed by this switch, the robot system stops and a message is shown in teach pendant LCD.

T1
AUTO
T2
Fig. 4.3 (a) Example of mode select switch

# 4.3.1 Operating Modes

There are two or three operating modes.

CAUTION

When high speed mode (contact stop function is disabled) is applied, contact stop function, push to escape function, retreat function after contact stop are set to disabled.

# AUTO: Automatic Mode

- The operator panel/box becomes enable.
- The robot program can be started by the operator panel/box start button or peripheral device I/O.
- If the robot system has safety fence, safety fence is enabled.
- The robot can be operated at the specified maximum speed.
- The contact stop function is enabled.
- The push to escape function is enabled.
- The retreat function after contact stop is enabled.
---
# SAFETY PRECAUTIONS

# Test Mode 1

- Program can be activated from the teach pendant only.
- The robot cannot be operated at speeds higher than 250mm/s at both of tool center point (tool coordinate origin) or wrist flange center.
- If the robot system has safety fence, safety fence is disabled. (Robot does not stop when fence is opened.)
- The contact stop function is enabled.
- The push to escape function is disabled.
- The retreat function after contact stop is disabled at jogging.

# Test Mode 2 (Optional)

- Program can be activated from the teach pendant only.
- The robot can be operated at the specified maximum speed.
- If the robot system has safety fence, safety fence is disabled. (Robot does not stop when fence is opened.)
- The contact stop function is enabled.
- The push to escape function is disabled.
- The retreat function after contact stop is disabled at jogging.

Please refer to the operator’s manual of robot controller for detail.

# 4.4 ENABLING DEVICE (DEADMAN SWITCH)

The enabling device (deadman switch) is used as an “enabling device”. When the teach pendant is enabled, robot motion is allowed only while at least one of enabling devices (deadman switches) is gripped. If you release or hard grip switches, the robot stops immediately. In case of the tablet TP, if you release or hard push the enabling device (deadman switch), the robot stops immediately.

# Enabling device (Deadman switch)

デットマンスイッチ

Fig. 4.4 (a) Enabling device (Deadman switch) (Tablet TP)
---
# SAFETY PRECAUTIONS

# DEADMAN SWITCH

Enabling device (Deadman switch)

Fig. 4.4 (b) Enabling device (Deadman switch) (iPendant)

Based on the risk assessment by FANUC, number of operation of enabling device (DEADMAN switch) must not exceed about 10000 times per year.

# 4.5 SAFEGUARDS

The safeguards consists of:

- Safety fence (fixed guard)
- Safety gate (with interlocking devices)
- Safety plug and socket
- Other protection devices

These safety devices must be complied with EN ISO, IEC and so on. In addition, system designers must install these devices according to the risk assessment. This section describes the basic requirements for these devices. Please refer to EN ISO 10218 and so on for detail. Note that these safety devices must be fitted to the robot system by the system house, etc.

# WARNING

Suitable safety guards are installed around robot system as the need arises. Robot operation without safety guards required from the result of risk assessment can cause serious injury or death of personnel.

# 4.5.1 Safety Fence

The basic requirements for Safety Fence are as follows:

- The fence is constructed to withstand foreseeable operational and environmental forces.
- The fence is free of sharp edges and projection and is not themselves a hazard.
- The fence prevents access to the safeguarded space except through openings associated with interlocking devices.
- The fence is permanently fixed in position and is removable only with the aid of tools.
- Fixing system of the safety fence must remain attached to the safety fence or to the robot system when they are removed.
- Where possible, safety fence must be incapable of remaining in place without their fixings.
- The fence cause minimum obstruction to the view of the production process. (wire mesh, lattice, panel etc.)
- The fence is located at an adequate distance from the maximum space.
---
# SAFETY PRECAUTIONS

- The fence should be connected to PE (protective Earth) to prevent the electric shock with accident.
- Please refer to the following and their related standards for detail of safety fence aperture size, minimum size of grids and so on.
- EN ISO 13855
- EN ISO 13857
- ANSI B11.19

# 4.5.2 Safety Gate and Plugs

The basic requirements for Safety Gate are as follows.

- The gate prevents the robot system from automatic operation until the gate is closed.
- The closure of the gate is not the control to restart automatic operation. This must be a deliberate action at a control station.
- The gate has plug and socket for interlock. The plug and socket must be selected appropriate things for safety.

This gate must be the one either it remains locked closed until the risk of injury from the hazard has passed (interlocking guard with guard locking) or opening the guard while the robot system is working gives a stop or emergency stop instruction (interlocking guard).

Please refer to EN ISO 14119 or ANSI B11.19 for detail of interlocking system.

If a personnel whole body can enter the safeguard space via the interlocking door, installing a device that the door does not close without intending.

Care should be taken to ensure that actuation of an interlock installed to protect against on hazard (e.g. stopping hazardous motion of the robot system) does not create a different hazard (e.g. the release of hazardous substances into the work zone).

# 4.5.3 Other Protection Devices

Protection devices must be designed and incorporated into the control system so that:

- they can be adjusted only by means of an intentional action, such as the use of a tool, key, etc.,
- the absence or failure of one of their components prevents starting or stops the moving parts.

As the need arises, the robot system must be designed so that:

- moving parts cannot start up while they are within the operator’s reach,
- the exposed person cannot reach moving parts once they have started up.

If some presence sensing devices are used for safety purposes, they must comply with the following:

- A presence sensing device must be installed and arranged so that persons cannot enter and reach into a hazardous area without activating the device.
- A presence sensing device must be installed and arranged so that persons cannot reach the restricted space before the hazardous conditions have ceased.
- Barriers used in conjunction with the presence-sensing device may be required to prevent persons from bypassing the device.
- Their operation must not be adversely affected by any of the environmental conditions for which the system was intended.
- When a presence-sensing device has been activated, it may be possible to restart the robot system from the stopped position provided that this does not create other hazards.
- As the need arises, resumption of robot motion must require the removal of the sensing field interruption. The result of risk assessment may require that this must not be the control to restart automatic operation.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

# 4.6 OPERATION INSIDE OF THE SAFETY FENCE

When some workers (programmer, maintenance engineer) have to enter the safety fence, the following care has to be taken into account.

- Make sure that the robot system has been completely stopped before entering the safety fence. Never enter the safety fence during the robot moving. If the robot is moving, stop the robot by hold button (or input signal), and after "controlled stop" it (servo power off), then you can enter the safety fence. (In case a safety fence is installed.)
- Make sure that an indicator lamp for stop condition (to be suitably installed by the end user) shows the stopped status of the robot, and enter the safety fence from the safety gate.
- To inform you are working in the safety fence, display “working”. During robot teaching or test operation, robot may move to an unexpected direction. So exercise special care, and perform teaching in the position where you can escape from the robot in case of dangerous situation.
- Set "Safe speed" signal enabled.
- When more than one worker collaborates for their operation, a user in charge should be equipped with teach pendant, and other users have to follow his order. Any operations from the external interface and robot controller operation panel without his order have to be prohibited.
- All users inside of the safety fence always have to secure the escape zone to avoid hazards from unintended movement of the robot.
- Care should be taken by all workers not to close off the escape routes for each other.
- Do not operate the robot resting against the wall, apparatus installed inside of the safety fence, etc. those take away escape zone from the operator.
- Keep watching the robot during operation in jogging, program verification, etc.
- Stop the robot immediately by E‑stop SW when somebody recognizes dangerous situation. Whenever possible, other user who is readily accessible to the E‑stop SW keeps watch from the outside of the safety fence.
- Make sure that deadman switches on teach pendant are operated only by hand.
- Make sure that nobody still exists inside of the safety fence when the safety gate is going to be closed.
- Do not leave tools etc. inside of the operating space of robot or peripheral devices, when operation inside of the safety fence has been finished.

# WARNING

1. Safety procedures of entering the safety fence have to be established and observed. Improper procedure of entering the safety fence can cause serious injury or death of personnel who enter the safety fence.
2. During teaching or maintenance of robot system with safety fence opened, special care shall be taken not to enter any other personnel who is not work for these operations. Unauthorized entry to inside of safety fence can cause serious injury or death of personnel who enter the safety fence.
---
# 4.7 THE SAFETY SEQUENCE FOR FENCE ENTRY

This section describes the safety procedure of entering the safety fence. Note that only a programmer or a maintenance person can enter the safety fence. A general person CANNOT enter the safety fence.

# Entering into the SAFETY FENCE

1. The robot is moving automatically (in AUTO mode).
2. Stop the robot by pressing HOLD buttons or HOLD input signal.
3. Change the operating mode to T1 or T2 from AUTO.
4. Remove the operating mode key switch for mode lock to prevent other persons change the operating mode.
5. Remove the plug2 from socket 2.
6. Open the gate of the safety fence, and put the plug2 to socket4.
7. Remove the plug1 from socket1.
8. Enter inside of the safety fence, and put the plug 1 to socket 3.

Please refer to Fig. 4.7 (a) for details of safety fence and safety plug configurations.

The key of operating mode key switch and the safety plug1 must be carried into the safety fence. The safety plug1 must be put to the socket3 inside fence.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

# Safety Fence

|Maximum space|Controller (operator panel)|Operator’s box|Restriction space|
|---|---|---|---|
|Mode switch key|Teach pendant|Safety gate|Safeguard distance|

# Safety Fence

|Safety gate| |Safety Fence| |
|---|---|---|---|
| |Plug 1|Socket 3 (inside of safety fence)| |
|Socket 1|Socket 2| |Socket 4|
| |Plug 2| | |

|Socket 1|Safety fence|«Inside of safety fence »|Plug 1|
|---|---|---|---|
|Socket 2|Safety gate|Socket 3|Safety fence|
|Socket 1|Safety gate|Socket 4|(OPENED)|
| | |Plug 2| |

# FENCE1

# FENCE2

# EMGIN1

# EMGIN2

| |Socket 1|Socket 3| | | |
|---|---|---|---|---|---|
| | | |Plug 1| | |
| | | | |Socket 4|Plug 2|
| | |Socket 2| | | |

# When the safety gate is CLOSED

# When the safety gate is OPENED

# Fig. 4.7 (a) SAFETY FENCE and SAFETY GATE example

s‑32
---
# SAFETY PRECAUTIONS

# GENERAL CAUTIONS

In this chapter, the requirements for safety during the following situations are described:

- Installation (5.1)
- Commissioning and functional testing (5.2)
- Programming (5.3)
- Program verification (5.4)
- Troubleshooting (5.5)
- Saving programmed data (5.6)
- Automatic operation (5.7)
- Maintenance (5.8)
- Dismantling / scrapping (5.9)
- Procedure to move arm without drive power in emergency or abnormal situations (5.10)
- Warning & Caution label (5.11)

The user must ensure that the safeguarding methods are provided, utilized, and maintained for each operation associated with the robot system and in particular for personnel other than those utilizing the teach pendant or enabling device.

The user must ensure that a teach pendant not connected to the robot controller must be inaccessible.

# WARNING

1. Safety procedures of entering the safety fence have to be established and observed. Improper procedure of entering the safety fence can cause serious injury or death of personnel who enter the safety fence.
2. During teaching or maintenance of robot system, special care shall be taken not to access any other personnel who is not working for these operations. Unauthorized entry to inside of safety fence can cause serious injury or death of personnel who enter the safety fence.
3. The servo motors, the regenerative resistor units and the isolated transformers on the AC power supply may be hot even after robot operation. Touching the surface of these components should be therefore avoided as much as possible. When touching any of these components is nonetheless required (ex.: for maintenance purposes), special care must be applied in order to avoid burn injury.

# 5.1 INSTALLATION

Be sure to install the robot system in accordance with FANUC’s requirements. The safeguarding methods must be identified by the hazard analysis and the risk assessment. The user must review the safety requirements to ensure that the appropriate safeguards are applied and operational prior to use in production.
---
# SAFETY PRECAUTIONS

# B-84194EN/01

# 5.2 COMMISSIONING AND FUNCTIONAL TESTING

During the testing of robots or robot systems after installation or relocation, be sure to follow the following procedures. These procedures are also applied to robots or robot systems after modifications (e.g. changes in hardware or software, replacement of parts, adjustments) and after maintenance or repairs that can adversely affect their operation.

# 5.2.1 Designation of the Restricted Space and Restriction of User

During the commissioning and functional testing, if the contact stop function is enabled, it is admitted that people they are trained about collaborative robot access the robot. During the commissioning and functional testing, if the contact stop function is disabled or untrained people may access the robot, and the safeguarding methods are not in place, interim means of designating the restricted space must be in place before proceeding. And users must not be allowed in the safeguarded space until the safeguards are functional.

# 5.2.2 Safety and Operational Verification

For commissioning and testing of the robot or the robot system, follow the instruction by the manufacturer (FANUC). At the initial start‑up, be sure to include the following procedure (but not limited to).

Before applying power, verify that:

- the robot has been properly mechanically mounted and is stable,
- the electrical connections are correct and the power (i.e. voltage, frequency, interference levels) is within specified limits,
- the other utilities (e.g. water, air, gas) are properly connected and within specified limits,
- the peripheral equipment is properly connected,
- the limiting devices that establish the restricted space (when utilized) are installed,
- the safeguarding means are applied, and
- the physical environment is as specified (e.g. lighting and noise levels, temperature, humidity, atmospheric contaminants).

After applying power, verify that:

- the start, stop, and mode selection (including key lock switches) control devices function as intended,
- each axis moves and is restricted as intended,
- emergency stop circuits and devices are functional,
- the safeguards and interlocks function as intended (when installing the controller),
- Contact stop function correctly,
- it is possible to shut out the outer power source,
- Teaching and restarting function correctly,
- other safeguarding is in place (e.g. barriers, warning devices),
- in reduced speed, the robot operates properly and has the capability to handle the product or workpiece, and
- in automatic (normal) operation, the robot operates properly and has the capability to perform the intended task at the rated speed and load.

# 5.2.3 Robot System Restart Procedures

A procedure for the restart of the robot system after hardware, software or task program modification, repair, or maintenance must include but not necessarily be limited to the following:

- check any changes or additions to the hardware prior to applying power;
- functionally test the robot system for proper operation.
---
# SAFETY PRECAUTIONS

# 5.3 PROGRAMMING

Whenever possible, programming must be performed with all persons outside the safeguarded space or the robot operating space and neighborhood. When it is necessary to perform programming with personnel inside the safeguarded space, the following safety procedures are necessary.

# WARNING

No other personnel than programmer or teaching operator enter inside of safety fence during teaching. Unauthorized entry to inside of safety fence can cause serious injury or death of personnel who enter the safety fence.

# 5.3.1 Prior to Programming

The following conditions must be met before making taught program.

- The programmer must be trained on the type of robot used in the actual robot system and must be familiar with the recommended programming procedures including all of the safeguarding methods.
- The programmer must visually check the robot system and safeguarded space to ensure that extraneous conditions which can cause hazardous do not exist.
- When using the teach pendant to make taught program, the teach pendant must be tested to ensure proper operation.
- Any faults or failures of the robot system must be corrected prior to teaching the robot.
- Before entering the safeguarded space or robot operating space and neighborhood, the programmer must ensure that all necessary safeguards are in place and functioning.
- The programmer must set the operating mode to taught mode prior to entering the safeguarded space or robot operating space and neighborhood. Take measure to prevent the third person starting auto operation.
- The results of risk assessment may admit that people they are not programmer but trained about collaborative robot access to the robot operating space and neighborhood easily, during programming. In this case, confirm that the contact stop function is enabled.

# 5.3.2 During Programming

During programming, only the programmer must be allowed in the safeguarded space and the following conditions must be met.

- The robot system must be under the sole control of the programmer within the safeguarded space or robot operating space or neighborhood.
- The controls of the teach pendant must be used as intended.
- The robot system must not respond to any remote commands or conditions that would cause hazardous conditions.
- All robot system emergency stop devices must remain functional. If it is impossible, take measures to secure security of users in safeguard space or robot operating space or neighborhood.
- The results of risk assessment may admit that people they are not programmer but trained about collaborative robot access to the robot operating space and neighborhood easily, during programming. In this case, confirm that the contact stop function is enabled. If the programmer changes the contact stop function to disable temporary, indicate to the surrounding people.

# 5.3.3 Returning to Automatic Operation

The programmer must return the suspended safeguards to their original effectiveness prior to initiating automatic operation of the robot system.
---
# SAFETY PRECAUTIONS

# 5.3.4 Other Cautions for Programming

- Adopt a limit switch or other sensor to detect a dangerous state and, if necessary, design the program to stop the robot when the sensor signal is received.
- Design the program to stop the robot when an abnormal condition occurs in any other robots or peripheral devices, even though the robot itself is normal.
- For a system in which the robot and its peripheral devices are in synchronous motion, particular care must be taken in programming in order not to interfere with each other.
- Provide a suitable interface between the robot and its peripheral devices so that the robot can detect the states of all devices in the system, and can be stopped according to the states.
- Design to arrange avoiding mutual interference when various robot’s operation space crossover significantly.
- Be sure to specify the predetermined work origin in a motion program so that the robot starts from the origin and terminates at the origin. Make it possible for the operator to distinguish easily that the robot motion has terminated at a glance.
- Circumspect program with sufficient delay required for the program after executing some control command in adopting actuators (pneumatic, hydraulic, and electric).
- Adopt limit switches for the end effector, and control the robot system by monitoring the state.

# 5.4 PROGRAM VERIFICATION

When visual examination of the robot system response to the task program is necessary as part of the verification procedure, it should be made with all persons outside the safeguarded space and its neighborhood. When it is necessary to perform program verification with personnel inside the safeguarded space or the robot operating space and neighborhood, apply the following contents.

- Program verification must initially be performed at reduced speed. Special care is required when override is specified in the program.
- When it is necessary to examine the movement of the robot at full (operational) speed, apply the following contents:
- Only the programmer can change safety operation mode to normal operation mode by means which requires careful operation;
- Workers in safeguard space or robot operating space and its neighborhood always can use enable device or other devices with an equivalent safety level if necessary;
- Safe working procedures are established to minimize the exposure of personnel to hazards within the safeguarded space or robot operating space and its neighborhood.

# 5.5 TROUBLESHOOTING

When troubleshooting is performed from within the safeguarded space or the robot operating space and neighborhood, be sure to follow the following contents.

- Personnel responsible for troubleshooting are specifically authorized and trained for these activities;
- Personnel entering the safeguarded space or robot operating space must operate the robot with the enable machine;
- Safe working procedures are established to minimize the exposure of personnel to hazards within the safeguarded space or robot operating space and its neighborhood.

# 5.6 SAVING PROGRAMMED DATA

A record of the task programs together with any modifications must be maintained. The programmed data which is saved in portable media must be stored in a suitably protected environment when not in use.
---
# 5.7 AUTOMATIC OPERATION

Automatic operation must only be permissible when

- the intended safeguards are in place and functioning,
- proper safe working procedures are followed.

The results of risk assessment may require to check following items before automatic operation

- no personnel are present within the safeguarded space,

# WARNING

Please make sure that nobody remained inside of the safety fence before starting up automatic operation of robot systems. If somebody remained inside of the safety fence exists, trapped personnel inside of the safety fence might meet serious situation, which can lead them to serious injury or death.

# 5.8 MAINTENANCE

The robot and robot system must have an inspection and maintenance program to ensure continued safe operation of the robot system.

The inspection and maintenance program must take into account the robot and robot system manufacturer’s recommendations.

Personnel who perform maintenance or repair on robots or a robot system must be trained in the procedures necessary to perform safely the required tasks.

Personnel who maintain and repair robot systems must be safeguarded from hazards.

Where possible, maintenance must be performed from outside the safeguarded space or robot operating space or neighborhood by placing the robot arm in a predetermined position.

The results of risk assessment may admit that people they don’t maintain or repair but trained about collaborative robot access to the robot operating space and neighborhood easily, during maintenance. In this case, confirm that the contact stop function is enabled.

The following is the safety procedure of entering safeguarded space for maintenance.

# WARNING

Make sure the Main breaker must be shut down in the robot maintenance with the exception of following.

- Replacing batteries of the Robot
- Demand of operating the peripheral equipment in maintenance operation
- Safety maintenance disturbance

Maintenance without disconnecting the electric power supply may cause serious electric shock.
---
# SAFETY PRECAUTIONS

# Entering safeguarded space for maintenance

1. Stop the robot system.
2. Shut off the power of the robot system, and lock the main breaker to prevent powering on during maintenance, by mistake. If you have to enter the safeguarded space while power is available to the robot system, you must do the following things prior to entering the safeguarded space:
- check the robot system to determine if any conditions exist that are likely to cause malfunctions,
- check if the teach pendant works correctly, and
- if any damage or malfunction is found, complete the required corrections and perform retest before personnel enter the safeguarded space.
3. Enter the safeguarded space (see Section 4.7 “The Safety Sequence for Fence Entry”).
4. After the maintenance working, check if the safeguarded system is effective. If it has been suspended to perform the maintenance working, return their original effectiveness.

# DISMANTLING / SCRAPPING

Do not start dismantling the robot before contacting such as FANUC Europe Corporation, FANUC America Corporation, SHANGHAI‑FANUC Robotics CO., LTD. or FANUC Corporation in Japan. Please contact us when you have to dismantle/scrap FANUC robot systems.

# WARNING

When dismantling and/or scrapping robot mechanical units equipped with spring balancers, the robot arm may move unexpectedly due to the stored elastic energy of the springs inside the balancer(s), and subsequently lose its balance. Dismantling and scrapping of such robot system must be done only after releasing the stored energy and according to the instructions provided by FANUC. Very severe injury or death of personnel may occur in case any of these instructions is not followed.

# CAUTION

Robot batteries used for memory and/or encoder backup must be disposed of appropriately. Failure to do so may cause short circuit during dismantling/scrapping, which potentially can cause ignition or explosion.

# WARNING & CAUTION LABEL

(1) Operation space and payload label

|REACH|CRX-10iA|1249|
|---|---|---|
| |CRX-10iA/L|1418|
|MAX. PAYLOAD :|10kg|10kg|
|LED LIGHT :|STATUS INDICATOR|STATUS INDICATOR|

Fig. 5.10 (a) Operating space and payload label
---
# SAFETY PRECAUTIONS

# DAILY MAINTENANCE

# 6.1 MECHANICAL UNIT

To keep the robot system safe, please perform periodic maintenance those are specified in operator’s manual or maintenance manual. In addition, please clean each part of the system and visually check them for any damage or cracks. Daily check items are as follows (but not limited to):

- Input power voltage
- Pneumatic pressure
- Damage of connection cables
- Looseness of connectors
- Lubrication
- Emergency stop functions
- Effectiveness of deadman switch on teach pendant
- Safety gate interlocks (in case the robot system has safety gate interlocks)
- Vibration, noise by the robot movement
- Functions of peripheral devices
- Fixtures of robot and peripheral devices

# 6.2 CONTROL UNIT

Before operating the system each day, clean each part of the system and check the system parts for any damage or cracks. Also, check the following:

1. Before service operation
- Check the cable connected to the teach pendant for excessive twisting.
- Check the controller and peripheral devices for abnormalities.
- Check the safety function.
2. After service operation
At the end of service operation, return the robot to the proper position, then turned off the controller. Clean each part, and check for any damage or cracks. If the ventilation port and the fan motor of the controller are dusty, wipe off the dust.
---
NO_CONTENT_HERE
---
# PREFACE

This manual explains operation procedures for the following mechanical units:

|Model name|Mechanical unit specification No.|Maximum load|
|---|---|---|
|FANUC Robot CRX-10iA|A05B-1702-B201|10kg|
|FANUC Robot CRX-10iA/L|A05B-1702-B202|10kg|

The label stating the mechanical unit and force sensor specification number is affixed in the following position. Before reading this manual, verify the specification number of the mechanical unit.

(1) TYPE (2) NO. (3) DATE (4) W E I G H T (5) Kg

Position of label indicating mechanical unit and force sensor specification number

# TABLE 1 (a) Mechanical unit

|(1) Model name|(2) TYPE|(3) No.|
|---|---|---|
|FANUC Robot|A05B-1702-B201|SERIAL NO. IS PRINTED|
|FANUC Robot|A05B-1702-B202| |

(4) DATE (5) WEIGHT kg

(Without controller)

PRODUCTION

YEAR AND MONTH ARE PRINTED

40

40

p‑1
---
# PREFACE

# B-84194EN/01

# RELATED MANUALS

For the FANUC Robot series, the following manuals are available:

|R-30iB Mini Plus|OPERATOR’S MANUAL|(Basic Operation)|
|---|---|---|
|Intended readers:|Intended readers:|Intended readers:|
|Operator, programmer, Teaching operator, Maintenance technician, System designer|Operator, programmer, Teaching operator, Maintenance technician, System designer|Operator, programmer, Teaching operator, Maintenance technician, System designer|
|Topics:|Topics:|Topics:|
|Robot functions, Operations, Programming, Setup, Interfaces, Alarms|Robot functions, Operations, Programming, Setup, Interfaces, Alarms|Robot functions, Operations, Programming, Setup, Interfaces, Alarms|
|Use:|Use:|Use:|
|Robot operation, Teaching, System design|Robot operation, Teaching, System design|Robot operation, Teaching, System design|
|ARC Welding Function|OPERATOR’S MANUAL|B-83284EN-2|
|Dispense Function|OPERATOR’S MANUAL|B-83284EN-4|
|Collaborative Robot Function|OPERATOR’S MANUAL|B-83744EN|
|MAINTENANCE MANUAL|B-84175EN|B-84175EN|
|Intended readers:|Intended readers:|Intended readers:|
|Maintenance technician, System designer|Maintenance technician, System designer|Maintenance technician, System designer|
|Topics:|Topics:|Topics:|
|Installation, Start-up, Connection, Maintenance|Installation, Start-up, Connection, Maintenance|Installation, Start-up, Connection, Maintenance|
|Use:|Use:|Use:|
|Installation, Start-up, Connection, Maintenance|Installation, Start-up, Connection, Maintenance|Installation, Start-up, Connection, Maintenance|

This manual uses following terms.

|Name|Terms in this manual|
|---|---|
|Connection cable between robot and controller|Robot connection cable|
|Robot mechanical unit|Mechanical unit|
---
# TABLE OF CONTENTS

# SAFETY PRECAUTIONS

............................................................................s-1

# 1 DEFINITION OF WARNING AND CAUTION

.................................................................s-2

# 2 FANUC COLLABORATIVE ROBOT SYSTEM

............................................................s-2

# 2.1 OVERVIEW

................................................................................................ s-2

# 2.2 PURPOSE OF ROBOT

.............................................................................. s-3

# 2.3 CONFIGURATION OF ROBOT SYSTEM

.................................................. s-3

# 2.4 DEFNITION OF THE USER

....................................................................... s-4

# 2.4.1 Robot Training

......................................................................................................s‑5

# 2.4.2 Safety of the working person

.................................................................................s‑6

# 2.4.3 Safety of the Collaborative Worker

.......................................................................s‑8

# 2.4.4 Safety of the Operator

...........................................................................................s‑8

# 2.4.5 Safety of the Programmer

......................................................................................s‑9

# 2.4.6 Safety of the Maintenance Engineer

....................................................................s‑10

# 2.5 RELEVANT STANDARDS

.............................................................................. s-12

# 3 ROBOT SYSTEM DESIGN

........................................................................s-13

# 3.1 GENERAL

................................................................................................ s-13

# 3.2 PLACEMENT OF EQUIPMENT

................................................................ s-14

# 3.3 POWER SUPPLY AND PROTECTIVE EARTH CONNECTION

............... s-16

# 3.4 OTHER PRECAUTIONS

.......................................................................... s-16

# 3.5 END EFFECTOR, WORKPIECE AND PERIPHERAL EQUIPMENT

........ s-19

# 3.6 THE CHARACTERISTIC OF COLLABORATIVE ROBOT AND LIMITATIONS AND USAGE NOTES

............................................................ s-20

# 4 SAFETY DEVICES

.............................................................................s-24

# 4.1 STOP TYPE OF ROBOT

.......................................................................... s-24

# 4.2 EMERGENCY STOP

................................................................................ s-26

# 4.3 MODE SELECT SWITCH

......................................................................... s-26

# 4.3.1 Operating Modes

.................................................................................................s‑26

# 4.4 ENABLING DEVICE (DEADMAN SWITCH)

............................................. s-27

# 4.5 SAFEGUARDS

......................................................................................... s-28

# 4.5.1 Safety Fence

........................................................................................................s‑28

# 4.5.2 Safety Gate and Plugs

..........................................................................................s‑29

# 4.5.3 Other Protection Devices

.....................................................................................s‑29

# 4.6 OPERATION INSIDE OF THE SAFETY FENCE

...................................... s-30

# 4.7 THE SAFETY SEQUENCE FOR FENCE ENTRY

.................................................... s-31

# 5 GENERAL CAUTIONS

.......................................................................s-33

# 5.1 INSTALLATION

........................................................................................ s-33

# 5.2 COMMISSIONING AND FUNCTIONAL TESTING

................................... s-34

# 5.2.1 Designation of the Restricted Space and Restriction of User

..........................s‑34

# 5.2.2 Safety and Operational Verification

....................................................................s‑34

# 5.2.3 Robot System Restart Procedures

.......................................................................s‑34

# 5.3 PROGRAMMING

...................................................................................... s-35

# 5.3.1 Prior to Programming

..........................................................................................s‑35

# 5.3.2 During Programming

...........................................................................................s‑35
---
# TABLE OF CONTENTS

# 5.3

# Returning to Automatic Operation

s-35

# Other Cautions for Programming

s-36

# 5.4

# PROGRAM VERIFICATION

s-36

# 5.5

# TROUBLESHOOTING

s-36

# 5.6

# SAVING PROGRAMMED DATA

s-36

# 5.7

# AUTOMATIC OPERATION

s-37

# 5.8

# MAINTENANCE

s-37

# 5.9

# DISMANTLING / SCRAPPING

s-38

# 5.10

# WARNING & CAUTION LABEL

s-38

# 6

# DAILY MAINTENANCE

s-39

# 6.1

# MECHANICAL UNIT

s-39

# 6.2

# CONTROL UNIT

s-39

# PREFACE

p-1

# 1

# TRANSPORTATION AND INSTALLATION

1

# 1.1

# TRANSPORTATION

1

# 1.2

# INSTALLATION

2

# 1.2.1

# Angle of Mounting Surface Setting

6

# 1.3

# MAINTENANCE AREA

8

# 1.4

# INSTALLATION CONDITIONS

8

# 2

# CONNECTION WITH THE CONTROLLER

9

# 2.1

# CONNECTION WITH THE CONTROLLER

9

# 3

# BASIC SPECIFICATIONS

11

# 3.1

# ROBOT CONFIGURATION

11

# 3.2

# MECHANICAL UNIT EXTERNAL DIMENSIONS AND OPERATING SPACE

14

# 3.3

# ZERO POINT POSITION AND MOTION LIMIT

16

# 3.4

# WRIST LOAD CONDITIONS

21

# 4

# EQUIPMENT INSTALLATION TO THE ROBOT

22

# 4.1

# END EFFECTOR INSTALLATION TO WRIST

22

# 4.2

# LOAD SETTING

23

# 5

# PIPING AND WIRING TO THE END EFFECTOR

25

# 5.1

# INTERFACE FOR OPTION CABLE

26

# 6

# AXIS LIMIT SETUP

29

# 6.1

# CHANGE AXIS LIMIT BY DCS

29

# 6.2

# RISK ASSESSMENT FOR J5-AXIS MOTION RANGE

32

# 7

# CHECKS AND MAINTENANCE

33

# 7.1

# PERIODIC MAINTENANCE

33

# 7.1.1

# Daily Checks

33

# 7.1.2

# Periodic Check and Maintenance

34

c-2
---
# TABLE OF CONTENTS

# 7.2 CHECK POINTS

.......................................................................................... 36

# 7.2.1 Confirmation of Oil Seepage

......................................................................................... 36

# 7.2.2 Check the Mechanical Unit Connectors

.......................................................................................... 37

# 7.3 MAINTENANCE

.......................................................................................... 38

# 7.3.1 Replacing the Batteries

.......................................................................................... 38

# 7.4 STORAGE

.......................................................................................... 38

# 8 MASTERING

.......................................................................................... 39

# 8.1 OVERVIEW

.......................................................................................... 39

# 8.2 RESETTING ALARMS AND PREPARING FOR MASTERING

.......................................................................................... 40

# 8.3 ZERO POSITION MASTERING

.......................................................................................... 41

# 8.4 QUICK MASTERING

.......................................................................................... 44

# 8.5 QUICK MASTERING FOR SINGLE AXIS

.......................................................................................... 46

# 8.6 SINGLE AXIS MASTERING

.......................................................................................... 48

# 8.7 MASTERING DATA ENTRY

.......................................................................................... 51

# 8.8 VERIFYING MASTERING

.......................................................................................... 53

# 9 TROUBLESHOOTING

.......................................................................................... 54

# 9.1 TROUBLESHOOTING

.......................................................................................... 54

# APPENDIX

# A PERIODIC MAINTENANCE TABLE

.......................................................................................... 63

# B MOUNTING BOLT TORQUE LIST

.......................................................................................... 66

# C EU DECLARATION OF CONFORMITY

.......................................................................................... 67

# D CONTACTS

.......................................................................................... 68

c‑3
---
NO_CONTENT_HERE
---
# 1. TRANSPORTATION AND INSTALLATION

# 1.1 TRANSPORTATION

When transporting the robot, sure to change the posture of the robot to that shown below and pack it in the transport box. Please perform packing the robot in two people. Refer to specification of Section 1.2 about unpacking and installation.

The transport kit and the carrying support can be purchased from FANUC. Refer to Table 1.1 (a) about specification.

WARNING
The robot becomes unstable when it is transported with the end effector applied to wrist. Please be sure to remove the end effector when the robot is transported.

# Carrying support

|M1|CRX-10iA|A97L-0318-0710#10IA-1|
|---|---|---|
|4|CRX-10iA/L|A97L-0318-0710#10IAL-1|
|0|One worker supports the arm, and the other worker takes off the bolts fixing the robot to the base.|One worker supports the arm, and the other worker takes off the bolts fixing the robot to the base.|

Please tighten the box with PP bands.

# Transport kit

|CRX-10iA|A97L-0318-0710#10IA|
|---|---|
|CRX-10iA/L|A97L-0318-0710#10IAL|

Fig. 1.1 (a) Transportation using transport box（CRX-10iA, CRX-10iA/L）
---
# 1. TRANSPORTATION AND INSTALLATION

# B-84194EN/01

|Model|Name|Specification|
|---|---|---|
|CRX-10iA|Transport kit|A97L-0318-0710#10IA|
| |Carrying support|A97L-0318-0710#10IA-1|
|CRX-10iA/L|Transport kit|A97L-0318-0710#10IAL|
| |Carrying support|A97L-0318-0710#10IAL-1|

Note) The transport kit includes the carrying support.

# 1.2 INSTALLATION

Please perform unpacking and the installation of the robot in two people. Fig 1.2(a) shows how to unpack and to install.

One worker supports the arm, and the other worker fixes the robot arm to the base using bolts.

# Fig. 1.2 (a) Unpacking and the installation of the robot (CRX-10iA, CRX-10iA/L)
---
# 1. TRANSPORTATION AND INSTALLATION

Fig. 1.2 (b), (c) show the robot base dimensions.

CAUTION

Flatness of robot installation surface must be less than or equal to 0.5mm.

Inclination of robot installation surface must be less than or equal to 0.5°.

If robot base is placed on uneven ground, it may result in the base breakage or low performance of the robot.

|45°|45°|
|---|
|4-φ9 through|4-O 9貫貫|
|O 170| |
|61|61|
|J1-axis|J1軸回転中心|
|95|99|
|rotation center|rotation center|
|SECTION A-A|SECTION A-A|
|A|C|
|25| |
|O 8|13|
|SECTION C-C|SECTION C-C|
|B| |
|198|154|
|98.3| |
|φ8 FG8 Depth10|O8 FG8 深さ10|
|13| |
|13| |
|+0.024|+0.006|
|7.6|50.2|
|O8 FG8 Depth10|φ8 FG8 深さ10|
|13| |
|8 +0.024|+0.006|
|10|120|
|8.1|50.7|
|Locating surface|Locating surface|
|突き当て面|突き当て面|
|10|120|
|OBLONG HOLE Depth10|OBLONG HOLE Depth10|
|長穴 深さ10|長穴 深さ10|
|VIEW B|VIEW B|
|矢視 B|矢視 B|
|OBLONG HOLE Depth10|OBLONG HOLE Depth10|
|長穴 深さ10|長穴 深さ10|

Fig. 1.2 (b) Dimensions of the robot base (back side connector)
---
# 1. TRANSPORTATION AND INSTALLATION

B-84194EN/01

|45°|4-φ9 through|4-O 9貫貫|O 170|61|
|---|---|---|---|---|
| |61|95|99|J1-axis|
| |J1軸回転中心|rotation center| | |

# A SECTION A-A

断面 A-A

# C

|O 8|13|
|---|---|
|25|正面|
|Front|0.85|

# SECTION C-C

断面 C-C

# B

|98.3|13|
|---|---|
|φ8 FG8 Depth10|O8 FG8 深さ10|
|13|+0.024|
|+0.006|7.6|
|50.2|8|
|10|120|

# Locating surface

突き当て面

|50.7|8 +0.024|
|---|---|
|10|OBLONG HOLE Depth10|
|長穴 深さ10| |

# VIEW B

矢視 B

Fig. 1.2 (c) Dimensions of the robot base (bottom connector)

Fig. 1.2 (d), Table 1.2 (a) indicate the force and moment applied to the robot base.

Table 1.2 (b) indicate the stopping distance and time of the J1 through J3 axes until the robot stopped by Power‑Off stop or Smooth stop after input the stop signal.

Refer to the data below in considering the strength of the installation plane.

# NOTE

Stopping times and distances in Table 1.2 (b) are reference values measured in accordance with ISO 10218-1. Please measure and check the actual values, since it varies depending on robot individual, load condition and operation program.
---
# 1. TRANSPORTATION AND INSTALLATION

Fig. 1.2 (d) Force and moment that acts on the robot base

|Vertical moment|Force in vertical direction| |Horizontal moment|Force in horizontal direction|
|---|---|---|---|---|
| |MV [Nm]|FV N|MH Nm|FH N (kgf)|
|During stillness|310|490|0|0|
|During acceleration or deceleration|380|550|120|180|
|During Smooth stop|610|800|250|220|

|Model|Speed|Stopping time [ms]|Stopping angle [deg] (rad)| | |
|---|---|---|---|---|---|
|CRX-10iA|250mm/s| |456|9.4(0.16)| |
| |300mm/s| |460|11.2(0.20)| |
| |1000mm/s| |468|29.3(0.51)| |
|MAX speed (HIGH SPEED MODE)|484| |29.3(0.51)| | |
|CRX-10iA/L|250mm/s| |340|6.5(0.11)| |
| |300mm/s| |340|7.8(0.14)| |
| |1000mm/s| |352|21.8(0.38)| |
|MAX speed (HIGH SPEED MODE)| | |520|32.4(0.57)| |

Stopping time and distance until the robot stopping by contact stop after input of stop signal. When contact stop is performed, robot stops in stopping time/ stopping distance which is shorter than the controlled stop. For the examination of the system, please use a value at the time of the controlled stop mentioned above.
---
# TRANSPORTATION AND INSTALLATION

# 1.2.1 Angle of Mounting Surface Setting

For all robot mounts except floor mount, be sure to set the mounting angle referring to the procedure below. Refer to Section 3.1 for installation specifications.

# WARNING

Depends on the robot position, risk assessment has to be done.

1. Turn on the controller with [PREV] and [NEXT] key pressed. Then select [3 Controlled start].
2. Press the [MENU] key and select [9 MAINTENANCE].
3. Select the robot for which you want to set the mount angle, and press the [ENTER] key.

| |ROBOT MAINTENANCE|CTRL START MANU|
|---|---|---|
| |Setup Robot System Variables| |
| |Group|Robot Library/Option Ext Axes|
|1|CRX-10iA|0|
|[TYPE]ORD NO|AUTO|MANUAL|

Press [F4] key.
Press the [ENTER] key until screen below is displayed.

*******Group 1 Initialization************

**************CRX-10iA********************

--- MOUNT ANGLE SETTING ---

0 [deg] : floor mount type

90 [deg] : wall mount type

180 [deg] : upside-down mount type

Set mount_angle (0-180[deg])->

Default value = 0
---
# 1. TRANSPORTATION AND INSTALLATION

6 Input the mount angle referring to Fig.1.2.1 (a).

＋

Angle of 設置角度 mounting surface

# Fig. 1.2.1 (a) Mounting angle

7 Press the [ENTER] key until screen below is displayed again.

|ROBOT MAINTENANCE|CTRL|START|MANU|
|---|---|---|---|
|Setup Robot System Variables|Setup Robot System Variables|Setup Robot System Variables|Setup Robot System Variables|
|Group CRX-10iA|1|Robot Library/Option Ext Axes|0|
|[TYPE]ORD NO|AUTO|MANUAL| |

8 Press [FCTN] key and select [1 START (COLD)].
---
# TRANSPORTATION AND INSTALLATION

# 1.3 MAINTENANCE AREA

Fig. 1.3 (a) shows the maintenance area of the mechanical unit. Make sure to secure enough room for mastering. Refer to Chapter 8 for the mastering.

|500| |400| |500| |500|810|500|
|---|---|---|---|---|---|---|---|---|
|(In case of bottom|(In case of bottom|(In case of bottom|(底面分線盤の場合)|(底面分線盤の場合)|(底面分線盤の場合)|(底面分線盤の場合)|(底面分線盤の場合)|(底面分線盤の場合)|
|500| | | | | | | | |

Fig. 1.3 (a) Maintenance area

# 1.4 INSTALLATION CONDITIONS

Refer to specification of Section 3.1 about installation conditions.

‑ 8 ‑
---
# 2 CONNECTION WITH THE CONTROLLER

# 2.1 CONNECTION WITH THE CONTROLLER

The robot is connected with the controller via the power and signal cable, the earth line, the camera cable or the force sensor cable. Connect these cables to the connectors on the option cables, see refer to Chapter 5.

WARNING

Before turning on controller power, be sure to connect the robot and controller with the earth line (ground). Otherwise, there is the risk of electrical shock.

# 2. CONNECTION WITH THE CONTROLLER

CAUTION
1. Before connecting the cables, be sure to turn off the controller power.
2. Don’t use 10m or longer coiled cable without first untying it. The long coiled cable could heat up and become damaged.

|Robot mechanical unit|Controller|
|---|---|
|power, signal cable|earth line|
|Earth terminal (M4 bolt)|Connector for camera cable or force sensor cable|
|Clamp for power and signal| |

Fig. 2.1 (a) Cable connection (back side connector)
---
# 2. CONNECTION WITH THE CONTROLLER

# B-84194EN/01

|Robot|ロボット機構部|
|---|---|
|Controller|制御装置|
|power, signal cable|動力、信号ケーブル|
|earth line|アース線|
|Connector for camera cable or force sensor cable|Connector for camera cable or force sensor cable|
|Clamp for power and signal|動力、信号線クランプ|
|Earth terminal is at the same place with the backside connector panel|アース端子は背面分線盤と同じ箇所|

Fig. 2.1 (b) Cable connection (bottom side connector)

‑ 10 ‑
---
# BASIC SPECIFICATIONS

# 3.1 ROBOT CONFIGURATION

|J5軸用ACサーボモータ|AC servo motor for J5-axis|
|---|---|
|J6軸用ACサーボモータ|AC servo motor for J6-axis|
|J4軸用ACサーボモータ|AC servo motor for J4-axis|
|J3軸用ACサーボモータ|AC servo motor for J3-axis|
|エンドエフェクタ|End effector|
|取り付け面|mounting face|
|J3アーム|J3 arm|
|手首ユニット|Wrist unit|
|J2アーム|J2 arm|
|J2軸用ACサーボモータ|AC servo motor for J2-axis|
|J2ベース|J2 base|
|J1軸用ACサーボモータ|AC servo motor for J1-axis|
|J1ベース|J1 base|

Fig. 3.1 (a) Mechanical unit configuration

| | | | | | | |J3|-|+|
|---|---|---|---|---|---|---|---|---|---|
|J4| |X|J5|+|-| | | | |
|Y|-J6|+|-| | | | | | |
|Z|+|-| | | | | | | |
| | | | | |J1| |+| | |

Fig. 3.1 (b) Each axes coordinates and mechanical interface coordinates

NOTE: The end effector mounting face center is 0, 0, 0 of the mechanical interface coordinates.
---
# 3. BASIC SPECIFICATIONS

# B-84194EN/01

|Item| |Specification|Specification| |
|---|---|---|---|---|
|Model| |CRX-10iA|CRX-10iA/L| |
|Type| | |Articulated type| |
|Controlled axes| | |6-axis(J1, J2, J3, J4, J5, J6)| |
|Reach| |1249 mm|1418 mm| |
|Installation| | |Floor, Upside-down, Wall & Angle mount (Note 2)| |
| |J1-axis|380° (6.63 rad)|360° (6.28 rad)| |
| |J2-axis| |360° (6.28 rad)| |
|Motion range|J3-axis|570° (9.95 rad)|540° (9.95 rad)| |
| |J4-axis| |380° (6.63 rad)| |
| |J5-axis| |360° (6.28 rad)| |
| |J6-axis| |380° (6.63 rad)| |
|Maximum speed| | |1000mm/s (NOTE 4) (maximum speed 2000mm/s (NOTE 5))| |
|Maximum load at wrist| | |10kg| |
|Allowable load moment at wrist|J4-axis| |34.8Nm| |
| |J5-axis| |26.0Nm| |
| |J6-axis| |11.0Nm| |
|Allowable load inertia at wrist|J4-axis| |1.28kg.m2| |
| |J5-axis| |0.90kg.m2| |
| |J6-axis| |0.30kg.m2| |
|Repeatability (NOTE 6)| | |±0.05mm| |
|Robot mass| |40kg|40kg| |
|Dust proof and drip proof mechanism|Conform to IP67 (NOTE 7)| | | |
|Acoustic noise level| | |Less than 70dB (NOTE 8)| |
| | |Ambient temperature:|Operating 0 to 45℃|(NOTE 9)|
| | | |Storage,Transport -10 to 60℃| |
| | |Ambient humidity:|Normally 75%RH or less (No dew or frost allowed)| |
|Installation environment| | |Short time 95%RH or less (Within 1 month)| |
| | |Permissible altitude:|Above the sea 1000m or less| |
| | |Free of corrosive gases|(NOTE 10)| |
| | |Vibration acceleration :|4.9m/s2 (0.5G) or less|(NOTE 11)|
| | |Environment without fire| | |

# NOTE

1. Even if the robot is used according to the defined specifications, motion programs might shorten reducer life or cause the robot to overheat. Use ROBOGUIDE for further evaluation before running production.
2. There is no limit of operating space for all the installation types.
3. During short distance motions, the axis speed may not reach the maximum value stated.
4. It is necessary to set a motion speed according to risk assessment of system considering pinching with the surroundings.
5. If the area is monitored by a safety sensor (located separately).
6. Compliant with ISO9283.
7. Definition of IP code
8. Definition of IP 67
9. - 6 = Dust-tight: Complete protection against contact
- 7 = Protection from water immersion: Ingress of water in harmful quantity shall not be possible when the enclosure is immersed in water under defined conditions of pressure and time.

This value is equivalent continuous A-weighted sound pressure level, which applied with ISO11201 (EN31201). This value is measured with the following conditions.
10. - Maximum load and speed
- Operating mode is AUTO

When robot is used in low temperature environment that is near to 0ºC, or not operated for a long time in the environment that is less than 0ºC in a holiday or the night, collision detection alarm (SRVO-050) etc. may occur since the resistance of the drive mechanism could be high immediately after starting the operation.
11. Contact the service representative, if the robot is to be used in an environment or a place subjected to hot/cold temperatures, severe vibrations, heavy dust, cutting oil splash and or other foreign substances.
12. Depending on the vibration of the floor or the hand, robot may stop due to the vibration in less than this value.
---
# 3. BASIC SPECIFICATIONS

# Performance of resistant chemicals and resistant solvents

1. The robot (including severe dust/liquid protection model) cannot be used with the following liquids.
Potentially these liquids will cause irreversible damage to the rubber parts (such as: gaskets, oil seals,
O‑rings etc.). (As exception to this only liquids tested and approved by FANUC can be used with the
robot.)
- (a) Organic solvents
- (b) Cutting fluid including chlorine / gasoline
- (c) Amine type detergent
- (d) Acid, alkali and liquid causing rust
- (e) Other liquids or solutions, that will harm NBR or CR rubber
2. When the robots work in the environment, using water or liquid, complete draining of J1 base must
be done. Incomplete draining of J1 base will make the robot break down.
3. Do not use unconfirmed cutting fluid and cleaning fluid.
4. Do not use the robot immersed in water, neither temporary nor permanent. Robot must not be wet
permanently.
---
# 3. BASIC SPECIFICATIONS

# 3.2 MECHANICAL UNIT EXTERNAL DIMENSIONS AND OPERATING SPACE

Fig. 3.2 (a), (b) show the robot operating space. When installing peripheral devices, be careful not to interfere with the robot and its operating space.

|+190 DEG|+190 DEG|0 DEG|-190 DEG|-190 DEG|
|---|---|---|
|R 1240|R 1080|MOTION RANGE OF J5-AXIS ROTATION CENTER|Operating space of J5-axis rotation center|Operating space of J5-axis rotation center|
|Operating space of end of flange|Operating space of end of flange|J5-AXIS ROTATION CENTER|End of flange|END OF FLANGE|
|378|150|160|540|MOTION RANGE OF END OF FLANGE|
|J5-axis rotation center|J5-axis rotation center|387|540|433|
|245|160|O190|449|O2480O 2160|
|Operating space of J5-axis rotation center|Operating space of J5-axis rotation center|MOTION RANGE OF J5-AXIS ROTATION CENTER|MOTION RANGE OF J5-AXIS ROTATION CENTER|MOTION RANGE OF J5-AXIS ROTATION CENTER|

Fig. 3.2 (a) Operating space (CRX-10iA)
---
# 3. BASIC SPECIFICATIONS

|0 DEG|±180 DEG|
|---|---|
|R 1410|R 1250|

Operating space of

MOTION RANGE OF

J5-axis rotation center

# J5-AXIS ROTATION CENTER

Operating space of

MOTION RANGE OF

end of flange

# END OF FLANGE

# J5-axis rotation center

# J5-AXIS ROTATION CENTER

|378|End of flange|END OF FLANGE|
|---|---|---|
|150|160|540|
|710|340| |
|415|245|113|
|O 190| |448|

O2820

O2500

Operating space of

MOTION RANGE OF

J5-axis rotation center

# J5-AXIS ROTATION CENTER

Fig. 3.2 (b) Operating space (CRX-10iA/L)

‑ 15 ‑
---
# 3. BASIC SPECIFICATIONS

# 3.3 ZERO POINT POSITION AND MOTION LIMIT

Zero point and motion range are provided for each controlled axis. Exceeding the software motion limit of a controlled axis is called overtravel (OT). Overtravel is detected at both ends of the motion limit for each axis. The robot cannot exceed the motion range unless there is a loss of zero point position due to abnormalities in the servo system or system error.

Fig.3.3 (a) to (h) show the zero point, and motion limit of each axis.

* The motion range can be changed. For information on how to change the motion range, see Chapter 6, “AXIS LIMIT SETUP”.

|Software restriction|Software restriction|
|---|
|- 190°|+190º Stroke end (Upper limit)|
|-190º|-190°ストロークエンド（下限） Stroke end (Lower limit)|
|+ 190°| |

Fig. 3.3 (a) J1-axis motion limit (CRX-10iA)
---
# 3. BASIC SPECIFICATIONS

# Software restriction

|＋ 180°|Stroke end (Upper limit)|+180°ストロークエンド（上限）|
|---|---|---|
|-180°|Stroke end (Lower limit)|-180°ストロークエンド（下限）|

# Fig. 3.3 (b) J1-axis motion limit (CRX-10iA/L)

# Software restriction

|-180°|180°|+|
|---|---|---|
|-180º|-180°ストロークエンド（下限）|Stroke end (Lower limit)|
|+180º|+180°ストロークエンド（上限）|Stroke end (Upper limit)|

(Note) Motion limit is restricted by the position of the J3-axis.

注)J3の位置によって動作範囲に制限を受けます。

# Fig. 3.3 (c) J2-axis motion limit (CRX-10iA,CRX-10iA/L)

‑ 17 ‑
---
# 3. BASIC SPECIFICATIONS

# B-84194EN/01

# ソフトウェアによる制限

# Software restriction

|+375°|+375º|+375°ストロークエンド（上限）|
|---|---|---|
|-195º|-195°ストロークエンド（下限）|Stroke end (Lower limit)|
|-195°| | |

(Note) Motion limit is restricted by the position of the J2-axis.

注) J2軸の位置によって動作範囲に制限を受けます。

# Fig. 3.3 (d) J3-axis motion limit (CRX-10iA)

# ソフトウェアによる制限

# Software restriction

|-270º|-270°ストロークエンド（下限）|Stroke end (Lower limit)|
|---|---|---|
|+270°|+270º|+270°ストロークエンド（上限）|
|-270°| | |

(Note) Motion limit is restricted by the position of the J2-axis.

# Fig. 3.3 (e) J3-axis motion limit (CRX-10iA/L)

‑ 18 ‑
---
# 3. BASIC SPECIFICATIONS

# Software restriction

|-190°| |+190°|
|---|---|---|
|-190º|Stroke end|+190º (Upper limit)|
|-190°ストロークエンド（下限）| |Stroke end|
| |(Lower limit)|+190°ストロークエンド（上限）|

Fig. 3.3 (f) J4-axis motion limit (CRX-10iA,CRX-10iA/L)

# Software restriction

|+180°| |+180º (Upper limit)|
|---|---|---|
|-180º|Stroke end| |
|-180°ストロークエンド（下限）| |(Lower limit)|

Fig. 3.3 (g) J5-axis motion limit (CRX-10iA,CRX-10iA/L)
---
# 3. BASIC SPECIFICATIONS

# B-84194EN/01

# Software restriction

|+190º (Upper limit)|+190°ストロークエンド（上限）|Stroke end|
|---|---|---|
|-190º|-190°ストロークエンド（下限）|(Lower limit)|

Fig. 3.3 (h) J6-axis motion limit (CRX-10iA,CRX-10iA/L)

‑ 20 ‑
---
# 3. BASIC SPECIFICATIONS

# 3.4 WRIST LOAD CONDITIONS

Fig. 3.4 (a) is diagrams showing the allowable load that can be applied to the wrist section.

- Apply a load within the region indicated in the graph.
- Please use it to meet the requirement of the allowable load moment and inertia at wrist. See the 3.1 about allowable load moment and inertia at wrist.
- See Section 4.1 about mounting of end effector.

| |Z (cm)| | | | |
|---|---|---|---|---|---|
| | | |30|5kg| |
| | | |25| | |
| | | |20|7kg| |
| | | |15|10kg| |
| | | |10| | |
| | | |5| | |
| |5|10|15|20|25|

Fig. 3.4 (a) Wrist load diagram (CRX-10iA, CRX-10iA/L)

‑ 21 ‑
---
# 4. EQUIPMENT INSTALLATION TO THE ROBOT

# 4.1 END EFFECTOR INSTALLATION TO WRIST

Fig. 4.1 (a) shows the figures for installing end effectors on the wrist. Select screws and positioning pins of a length that matches the depth of the tapped holes and pin holes. See Appendix B “Bolt tightening torque” for tightening torque specifications.

CAUTION

Notice the tooling coupling depth to wrist flange should be shorter than the flange coupling length.

WARNING

When the robot mounted the end effector operates, the end effector may collide with the robot, and if a part of body is pinched between the end effector and the robot, it might cause heavy injury.

|EE interface|Camera cable interface or force sensor cable interface|
|---|---|
|6.5|6.5|
|O31.5 H7|O63 h7|
|25 ±0.05|O6H7 Depth 6.5|
| |7-M6 Depth10|
|O50| |
|45°|45°|
|Wrist interface|Wrist interface|

Fig. 4.1 (a) End effector interface（CRX-10iA, CRX-10iA/L）
---
# 4. EQUIPMENT INSTALLATION TO THE ROBOT

# 4.2 LOAD SETTING

WARNING

If the load setting is wrong, safety function may lost, and it may cause injury of the personnel. If the load setting is changed, confirm the value and perform the test again.

CAUTION

1. Perform load setting (payload, payload center and inertia) correctly. If load setting is not correct, the sensitivity of the contact stop may getting worse. In addition, collaborative robot always check the load is correct or not during operations. If the robot detect the actual load does not match the load setting, robot stops for safety. So if load setting is incorrect, you cannot operate the robot.
2. Set the correct load condition parameter before the robot runs. Do not operate the robot in over when its payload is exceeded or incorrect. Do not exceed the allowable payload including connection cables and its swing. Operation in with the robot over payload may result in troubles such as reducer life reduction.

The operation motion performance screens include the MOTION PERFORMANCE screen, MOTION PAYLOAD SET screen, and payload information and equipment information on the robot.

1. Press the [MENU] key to display the screen menu.
2. Select [6 SYSTEM] on the next page.
3. Press the F1 ([TYPE]) key to display the screen switch menu.
4. Select “MOTION.” The MOTION PERFORMANCE screen will be displayed.

|MOTION PERFORMANCE| |JOINT 10%|
|---|---|---|
|Group1| | |
|No.|PAYLOAD[kg]|[ Comment]|
|1|10.00| |
|2|0.00|[[ ]]|
|3|0.00| |
|4|0.00|[[ ]]|
|5|0.00| |
|6|0.00|[[ ]]|
|7|0.00|[[ ]]|
|8|0.00|[[ ]]|
|9|0.00| |
|10|0.00|[ ]|

Active PAYLOAD number = 0

[ TYPE]   GROUP

IDENT     DETAIL     ARMLOAD      SETIND  &gt;&gt;

‑ 23 ‑
---
# 4. EQUIPMENT INSTALLATION TO THE ROBOT

# B-84194EN/01

Ten different pieces of payload information can be set using condition No.1 to No.10 on this screen. Place the cursor on one of the numbers, and press F3 (DETAIL). The MOTION PAYLOAD SET screen appears.

# MOTION PAYLOAD SET

| | |JOINT|100%| |
|---|---|---|---|---|
|Group 1|Schedule No[1]:[Comment]| | | |
|1 PAYLOAD|[kg]|10.00| | |
|2 PAYLOAD CENTER|X [cm]|-11.27| | |
|3 PAYLOAD CENTER|Y [cm]|0.00| | |
|4 PAYLOAD CENTER|Z [cm]|8.04| | |
|5 PAYLOAD INERTIA X [kgfcms2]| |0.25| | |
|6 PAYLOAD INERTIA Y [kgfcms2]| |0.29| | |
|7 PAYLOAD INERTIA Z [kgfcms2]| |0.24| | |
|[TYPE]|GROUP|NUMBER|DEFAULT|HELP|

Center of robot
ロボットの
end effector mounting face
エンドエフェクタ取付面
中心

Mass m (kg)
質量m(kg)

x (cm)
g
Iy (kgf・cm・s2)
Center of gravity
重心

Iz (kgf・cm・s2)
y (cm)
g

z (cm)
g
Ix (kgf・cm・s2)

Fig. 4.2 (a) Standard tool coordinate

# 6

Set the payload, gravity center position, and inertia around the gravity center on the MOTION PAYLOAD SET screen. The X, Y, and Z directions displayed on this screen correspond to the respective standard tool coordinates (with no tool coordinate system set up). When values are entered, the following message appears: “Path and Cycle time will change. Set it?” Respond to the message with F4 ([YES]) or F5 ([NO]).

# 7

Pressing F3 ([NUMBER]) will bring you to the MOTION PAYLOAD SET screen for another condition number. For a multigroup system, pressing F2 ([GROUP]) will bring you to the MOTION PAYLOAD SET screen for another group.

# 8

Press the PREV key to return to the MOTION PERFORMANCE screen. Press F5 ([SETIND]), and enter the desired payload setting condition number.

# 9

On the list screen, pressing F4 ARMLOAD brings you to the device-setting screen.

# MOTION ARMLOAD SET

| | | |JOINT|100%| | |
|---|---|---|---|---|---|---|
|Group 1|1 ARM LOAD AXIS #1 [kg]| | |0.00| | |
| |2 ARM LOAD AXIS #3 [kg]| | |0.00| | |
| |[TYPE]|GROUP|DEFAULT|HELP| | |

# 10

Specify the mass of the loads on the J2 base and J3 casing. When you enter the following parameter, ARMLOAD AXIS #1[kg]: Mass of the load on the J2 base (Contact FANUC if you install equipment on J2 base.)
ARMLOAD AXIS #3[kg]: Mass of the load on the J3 casing (Contact FANUC if you install equipment on J3 casing.) the confirmation message “Path and Cycle time will change. Set it?” appears. Select F4 YES or F5 NO. Once the mass of a device is entered, it is put in effect by turning the power off and on again.

‑ 24 ‑
---
# PIPING AND WIRING TO THE END EFFECTOR

# WARNING

- Only use appropriately-specified mechanical unit cables.
- Do not add user cables or hoses inside of the mechanical unit.
- Please do not obstruct the movement of the mechanical unit cable when cables are added to outside of mechanical unit.
- Please do not perform remodeling (adding a protective cover, or secure an additional outside cable) that obstructs the behavior of the outcrop of the cable.
- When external equipment is installed in the robot, make sure that it does not interfere with other parts of the robot.
- Cut and discard any unnecessary length of wire strand of the end effector (hand) cable. Insulate the cable with seal tape. (See Fig. 5 (a))
- If you have end effector wiring and a process that develops static electricity, keep the end effector wiring as far away from the process as possible. If the end effector and process must remain close, be sure to insulate the cable.
- Be sure to seal the connectors of the user cable and terminal parts of all cables to prevent water from entering the mechanical unit. Also, attach the cover to the unused connector.
- Frequently check that connectors are tight and cable jackets are not damaged.
- When precautions are not followed, damage to cables might occur. Cable failure may result in incorrect function of end effector, robot faults, or damage to robot electrical hardware. In addition, electric shock could occur when touching the power cables.

# End effector (hand) cable

Insulation processing

Cut unnecessary length of unused wire strand

Fig. 5 (a) Treatment method of end effector (hand) cable

‑ 25 ‑
---
# 5. PIPING AND WIRING TO THE END EFFECTOR

# 5.1 INTERFACE FOR OPTION CABLE

Fig. 5.1 (a), (b) show the position of the option cable interface. EE interface is prepared as options.

NOTE

Each option cable is written as shown below on the connector panel.

EE interface : EE

|Position of output|出口側|
|---|---|
|side connector|コネクタ位置|
|Position of input|入力側|
|side connector|コネクタ位置|
|Backside connector panel|背面分線盤の場合|
|Bottom connector panel|底面分線盤の場合|

Fig. 5.1 (a) Interface for option cable
---
# 5. PIPING AND WIRING TO THE END EFFECTOR

|カメラケーブル|Camera cable| |
|---|---|---|
|インターフェース|interface or|もしくは|
|力センサケーブル|cable interface|インターフェース|

|Backside connector panel|背面分線盤|Bottom connector panel|底面分線盤|
|---|---|---|---|
|J1 connector panel|J1分線盤| | |

|Camera cable interface or|force sensor cable interface|カメラケーブル|
|---|---|---|
|EE interface|インターフェース|もしくは|
|EEインターフェース|力センサケーブル|インターフェース|

# Wrist flange

手首フランジ

Fig. 5.1 (b) Interface for option cable

‑ 27 ‑
---
# 5. PIPING AND WIRING TO THE END EFFECTOR

# EE interface

Fig. 5.1 (c) shows the pin layout for the EE interface.

EEインタフェース(出力側)

EE interface (Output)

1424230 (PHOENIX CONTACT K.K)

1424230( フェニックスコンタクト((株)))

|white|Analog Input - RS485+|
|---|---|
|brown|Analog Input 2_ RS485-|
|green|Digital Input 2|
|yellow|Digital Input|
|pink| |
|grey|POWER(24V/12V POWER OFF)|
|blue|Digital Output|
|red|Ground|

Outside FANUC delivery scope

お客様にてご用意ください

# Controller

制御装置

Fig. 5.1 (c) Pin layout for EE interface

# CAUTION

For wiring of the peripheral device to the end effector interface, refer to the CONTROLLER MAINTENANCE MANUAL.

# Connector specifications

**Table 5.1 (a) Connector specifications (User side)**
|Cable name|Input side (J1 base)|Output side (Wrist flange)|Maker/dealer|
|---|---|---|---|
|EE|────|1404190|Straight plug (Attached)|
| | |1404194|Angle plug|

**Table 5.1 (b) Connector specifications (Mechanical unit side・reference)**
|Cable name|Input side (J1 base)|Output side (Wrist flange)|Maker/dealer|
|---|---|---|---|
|EE|────|1424230|PHOENIX CONTACT K.K|

# NOTE

For details, such as the dimensions, of the parts listed above, refer to the related catalogs offered by the respective manufactures, or contact your local FANUC representative.
---
# 6. AXIS LIMIT SETUP

By setting the motion range of each axes, you can change the robot’s motion range from the standard values. Changing the motion range of the robot is effective under following circumstances:

- Used motion range of the robot is limited.
- There’s an area where tool and peripheral devices interfere with robot.
- The length of cables and hoses attached for application is limited.

# WARNING

1. Changing the motion range of any axis affects the operating range of the robot. To avoid trouble, carefully consider the possible effect of the change to the movable range of each axis in advance. Otherwise, it is likely that an unexpected condition will occur; for example, an alarm may occur when the robot tries to reach a previously taught position.
2. Use the DCS function so that damage to peripheral equipment and injuries to human bodies can be avoided.

# 6.1 CHANGE AXIS LIMIT BY DCS

The robot motion can be restricted with DCS (Dual check safety) function. The robot motion can be restricted at any angle and position if it is in robot motion area. DCS functions are certified to meet the requirements of International Standard ISO13849‑1 and IEC61508 approved by notified body. If only the operating space is set using Joint Position Check, the robot stops after it goes beyond the workspace. When the motor power is shut down, the robot’s momentum causes it to move some distance before it completely stops. The actual "Robot Stop Position" will be beyond the workspace. To stop the robot within the robot workspace, use the DCS Stop Position Prediction function. The stop position prediction is disabled by default.

As an example, we shows the procedure to set ±30º for J2‑axis in here. Refer to Dual check safety function Operator’s Manual (B‑83184EN) for details of other setting, function and DCS stop position prediction.

# Setting procedure

1. Press the [MENU] key to display the screen menu.
2. Press [0 NEXT] and press [6 SYSTEM].
3. Press the F1 (]TYPE]).
4. Select [DCS]. The following screen will be displayed.

|AUTO|DCS|JOINT 1%| | |
|---|---|---|---|---|
| |1|Joint position check|OK| |
| |2|Joint speed check:| | |
| |3|Cart. position check| | |
| |4|Cart. speed check| | |
| |5|T1 mode speed check| | |
| |6|User model| | |
| |7|Tool frame| | |
| |8|User frame| | |
| |9|Stop position prediction| | |
| |[TYPE]|APPLY|DETAIL|UNDO|
---
# 6. AXIS LIMIT SETUP

B-84194EN/01

1. Move the cursor to [1 Joint position check], then press the [DETAIL].

|AUTO|DCS|JOINT 1%|
|---|---|---|
|Join Position check|Join Position check|Join Position check|
|No.|G|Status Comment|
|1|DISABLE|1 1 ‑‑‑‑ [ ]|
|2|DISABLE|1 1 ‑‑‑‑ [ ]|
|3|DISABLE|1 1 ‑‑‑‑ [ ]|
|4|DISABLE|1 1 ‑‑‑‑ [ ]|
|5|DISABLE|1 1 ‑‑‑‑ [ ]|
|6|DISABLE|1 1 ‑‑‑‑ [ ]|
|7|DISABLE|1 1 ‑‑‑‑ [ ]|
|8|DISABLE|1 1 ‑‑‑‑ [ ]|
|9|DISABLE|1 1 ‑‑‑‑ [ ]|
|10|DISABLE|1 1 ‑‑‑‑ [ ]|

Move the cursor to [1], then press the [DETAIL].

|AUTO|DCS|JOINT 1%|
|---|---|---|
|No. 1|Status:|Status:|
|1 Comment|[*********************]|[*********************]|
|2 Enable/Disable|DISABLE|DISABLE|
|3 Group|1|1|
|4 Axis|1|1|
|5 Safe side:| | |
|Position (deg):|Current:|0.000|
|6 Upper limit:|0.000| |
|7 Lower limit:|0.000| |
|8 Stop type:|Power‑off stop| |

Move the cursor to [DISABLE], then press [CHOICE], set the status to [ENABLE].
Move the cursor to [Group], then input the robot group number, then press the [ENTER] key.
Move the cursor to [Axis], then input “2”, then press the [ENTER] key.
Move the cursor to [Upper limit] right side, then input “30”, then press the [ENTER] key.
Move the cursor to [Lower limit] right side, then input “‑30”, then press the [ENTER] key.

WARNING

If only the operating space is set using Joint Position Check, the robot stops after it goes beyond the workspace. When the motor power is shut down, the robot’s momentum causes it to move some distance before it completely stops. The actual "Robot Stop Position" will be beyond the workspace. To stop the robot within the robot workspace, use the DCS Stop Position Prediction function. The stop position prediction is disabled by default.

|AUTO|DCS|JOINT 1%|
|---|---|---|
|No. 1|Status:|Status:|
|1 Comment|[*********************]|[*********************]|
|2 Enable/Disable|DISABLE|DISABLE|
|3 Group|1|1|
|4 Axis|1|1|
|5 Safe side:| | |
|Position (deg):|Current:|0.000|
|6 Upper limit:|+30.000| |
|7 Lower limit:|‑30.000| |
|8 Stop type:|Power‑off stop| |

‑ 30 ‑
---
# 6. AXIS LIMIT SETUP

12 Press the [PREV] key two times, back to the first screen.

|AUTO|DCS| | |JOINT 1%| |
|---|---|---|---|---|---|
| |1|Joint position check| |UNSF|CHGD|
| |2|Joint speed check:| | | |
| |3|Cart. position check|OK| | |
| |4|Cart. speed check| | | |
| |5|T1 mode speed check| | | |
| |6|User model| | | |
| |7|Tool frame| | | |
| |8|User frame| | | |
| |9|Stop position prediction| | | |

[TYPE] APPLY DETAIL UNDO

13 Press the [APPLY].

14 Input 4‑digit password, then press the [ENTER] key. (Password default setting is “1111”.)

15 The following screen will be displayed, then press the [OK].

|AUTO|DCS| |JOINT 1%|
|---|---|---|---|
| |Verify (diff)| | |
| |F Number :|F0000| |
|VERSION :| |HandlingTool| |
| |$VERSION :|V7.7097| |
| |DATE:|17-7-28|19;44|
| |DCS Version:|V2. 0. 11| |

---Joint Position Check-----------------

| |No.| |G|A|Status Comment|
|---|---|---|---|---|---|
|1|EBABLE|1|2|CHGD [| |
|2|ENABLE|1|2|---- [| |
|3|DISABLE|1|2|---- [| |

ALL OK QUIT

[CHGD] on the right side of [1 Joint position check] will change to [PEND].

AUTO

DCS

JOINT 1%

| |1|Joint position check| | |UNSF|PEND|
|---|---|---|---|---|---|---|
| |2|Joint speed check:| | | | |
| |3|Cart. position check|OK| | | |
| |4|Cart. speed check| | | | |
| |5|T1 mode speed check| | | | |
| |6|User model| | | | |
| |7|Tool frame| | | | |
| |8|User frame| | | | |
| |9|Stop position prediction| | | | |

[TYPE] APPLY DETAIL UNDO

16 Cycle the power of the controller in the cold start mode so the new settings are enabled.

WARNING

You must cycle the power of the controller to enable the new setting. If you fail to do so, the robot does not work normally and it may injure personnel or damage the equipment.

‑ 31 ‑
---
# 6. AXIS LIMIT SETUP

# 6.2 RISK ASSESSMENT FOR J5-AXIS MOTION RANGE

Perform the setting of the J5‑axis motion range after performing the risk assessment for the robot system including an end effector.

WARNING

When the motion range is performed without a risk assessment, it might cause danger such as pinching fingers.

# Setting procedure

1. Change the J5‑axis motion range referring to Section 6.1.
2. Change the upper limit and the lower limit of the J5‑axis DCS axis position check. Refer to Chapter 3 of the DUAL CHECK SAFETY FUNCTION OPERATOR’S MANUAL (B‑83184EN). Set a 1° margin against the motion range (example: motion range ±120°, DCS each axis position check upper limit = 121°, lower limit = -121°).
3. Turn off the controller and then turn it back on again in the cold start mode so the new information can be used.

‑ 32 ‑
---
# 7. CHECKS AND MAINTENANCE

Optimum performance of the robot can be maintained by performing the periodic maintenance procedures presented in this chapter. (See APPENDIX A PERIODIC MAINTENANCE TABLE.)

NOTE

The periodic maintenance procedures described in this chapter assume that the FANUC robot is used for up to 3840 hours a year. In cases where robot use exceeds 3840 hours/year, adjust the given maintenance frequencies accordingly. The ratio of actual operation time/year vs. the 3840 hours/year should be used to calculate the new (higher) frequencies. For example, when using the robot 7680 hours a year with a recommended maintenance interval of 3 years or 11520 hours, use the following calculation to determine the maintenance frequency: 3 years / 2 = perform maintenance every 1.5 years.

# 7.1 PERIODIC MAINTENANCE

# 7.1.1 Daily Checks

Check the following items when necessary before daily system operation.

|Check items|Check points and management|
|---|---|
|Oil seepage|Check to see if there is oil on the sealed part of each joint. If there is an oil seepage, clean it. ⇒”7.2.1 Confirmation of Oil Seepage”|
|Vibration, abnormal noises|Check whether vibration or abnormal noises occur. When vibration or abnormal noises occur, perform measures referring to the following section: ⇒”9.1 TROUBLESHOOTING” (symptom：Vibration, Noise)|
|Positioning accuracy|Check that the taught positions of the robot have not deviated from the previously taught positions. If displacement occurs, perform the measures as described in the following section: ⇒”9.1 TROUBLESHOOTING” (symptom：Displacement)|
|Peripheral devices for proper operation|Check whether the peripheral devices operate properly according to commands from the robot and the peripheral devices.|
|Brakes for each axis|Check that the droppage of the end effector is within 5 mm when the servo power turned off. If the end effector (hand) drops, perform the measures as described in the following section: ⇒”9.1 TROUBLESHOOTING” (symptom：Dropping axis)|
|Warnings|Check whether unexpected warnings occur in the alarm screen on the teach pendant. If unexpected warnings occur, perform the measures as described in the following manual: ⇒”CONTROLLER OPERATOR’S MANUAL (Alarm Code List)(B-83284EN-1)”|
---
# 7. CHECKS AND MAINTENANCE

# 7.1.2 Periodic Check and Maintenance

Check the following items at the intervals recommended below based on the total operating time or the accumulated operating time, whichever comes first. (○ : Item needs to be performed.)

|Check and maintenance intervals|Periodic Check and maintenance item|Check points, management and maintenance method|table No.| | | |
|---|---|---|---|---|---|---|
|1 month|3 months|1 year|2 years|3 years|4 years|8 years|
|320h|960h|3840h|7680h|11520h|15360h|30720h|
| |○|○|Cleaning the controller ventilation system|Confirm the controller ventilation system is not dusty. If dust has accumulated, remove it.|9| |
|Only|1st check|Check for external damage|Check whether the robot has external damage due to the interference with the peripheral devices. If an interference occurs, eliminate the cause. Also, if the external damage is serious and causes a problem in which the robot cannot be used, replace the damaged parts. (Perform diary checks for green covers.)|1| | |
|○|○|Check for water|Check whether the robot is subjected to water or cutting oils. If water is found, remove the cause and wipe off the liquid.|2| | |
| |○|○|Check for damages to the teach pendant cable, the operation box connection cable or the robot connection cable|Check whether the cable connected to the teach pendant, operation box and robot are unevenly twisted or damaged. If damage is found, replace the damaged cables.|8| |
| |○|○|Check for damage to the end effector connection cable (hand)|Check whether the end effector connection cables are unevenly twisted or damaged. If damage is found, replace the damaged cables.|3| |
| |○|○|Check the exposed connectors|Check the connection of exposed connectors.|4| |
| |○|○|Retightening the end effector mounting bolts|Retighten the end effector mounting bolts. Refer to the following section for tightening torque information: ⇒”4.1 END EFFECTOR INSTALLATION TO WRIST”|5| |
---
# 7. CHECKS AND MAINTENANCE

# Check and maintenance intervals

| | | | | |Periodic|(Operating time, Accumulated operating time)|Check and maintenance item|Check points, management and maintenance method|maintenance table No.|
|---|---|---|---|---|---|---|---|---|---|
|1 month|3 months|1 year|2 years|3 years|4 years|8 years| | | |
|320h|960h|3840h|7680h|11520h|15360h|30720h| | | |
|○| | | | | | | | | |
|Retightening the external main bolts| | | | | | | | | |
|Retighten the robot installation bolts (according to procedure in Section 1.2), bolts to be removed for inspection, and bolts exposed to the outside. Refer to the recommended bolt tightening torque guidelines at the end of the manual. An adhesive to prevent bolts from loosening is applied to some bolts. If the bolts are tightened with greater than the recommended torque, the adhesive might be removed. Therefore, follow the recommended bolt tightening torque guidelines when retightening the bolts.| | | | | | | | | |
|Only 1st check| | | | | | | | | |
|○| | | | | | | | | |
|Clean spatters, sawdust and dust| | | | | | | | | |
|Check that spatters, sawdust, or dust does not exist on the robot main body. If dust has accumulated, remove it. Especially, clean the robot movable parts well (each joint, surroundings of the wrist flange, conduit part, wrist axis hollow part).| | | | | | | | | |
|Only 1st check| | | | | | | | | |
---
# 7. CHECKS AND MAINTENANCE

# 7.2 CHECK POINTS

# 7.2.1 Confirmation of Oil Seepage

Check items

Check there is oil on sealed part of each joint parts. If there is oil seepage, clean them.

Management

x Oil might accumulate on the outside of the seal lip depending on the movement condition or environment of the axis. If the oil changes to a state of liquid, the oil might fall depending on the axis movement. To prevent oil spots, be sure to wipe away any accumulated oil under the axis components as shown in Fig. 7.2.1 (a) before you operate the robot. If you must wipe oil frequently, and opening the grease outlet does not stop the seepage, perform the measures below.

⇒”9.1 TROUBLESHOOTING”(symptom：Grease leakage)

‑ 36 ‑
---
# 7. CHECKS AND MAINTENANCE

# 7.2.2 Check the Mechanical Unit Connectors

# Inspection points of the connectors

- Robot connection cables, earth terminal and user cables

# Check items

- Circular connector: Check the connector for tightness by turning it manually.
- Earth terminal: Check the connector for tightness.

Fig. 7.2.2 (a) Connector Inspection points

‑ 37 ‑
---
# 7. CHECKS AND MAINTENANCE

# 7.3 MAINTENANCE

# 7.3.1 Replacing the Batteries

The position data of each axis is preserved by the backup batteries. Please use the following procedure to replace when the backup battery voltage drop alarm occurs.

Procedure of replacing the battery (Under consideration)

1. Keep the power on. Press the EMERGENCY STOP button to prohibit the robot motion.

CAUTION

Be sure to keep the power on. Replacing the batteries with the power supply turned off causes all current position data to be lost. Therefore, mastering will be required again.

Remove the bolts and the J2 arm root side cover.
Remove the cable connector of the batteries.
Remove bolts and cover plate of the battery.
Take out the old batteries (2 pcs) from the battery case. Then replace the batteries (2 pcs).
Assemble them by reversing the sequence. The gasket is reusable.

|Gasket|ガスケット|
|---|---|
|Cover|カバー|
|Bolt|ボルト|
|M4 x 12 (6 pcs)|M4X12 (6個)|
|Tightening torque: 4.5Nm|締結トルク：4.5Ｎｍ|

Battery clip

リチウムバッテリ (2本）

FANUC spec. :A98L-0031-0011#D

バッテリケーブル

When replacing the batteries, replace two batteries together.

ファナック仕様:A98L-0031-0011#D

Cable connector of the batteries

バッテリケーブルコネクタ

Cover plate of battery

バッテリカバー板金

|Bolt|ボルト|
|---|---|
|M3 x 8 (4 pcs)|M3X8 (4個)|

Fig. 7.3.1 (a) Replacing the battery

# 7.4 STORAGE

When storing the robot, place it on a level surface with the same posture for transportation. (See Section 1.1.)
---
# 8. MASTERING

Mastering associates the angle of each robot axis with the pulse count value supplied from the absolute Pulsecoder connected to the corresponding axis motor. To be specific, mastering is an operation for obtaining the pulse count value corresponding to the zero position.

# 8.1 OVERVIEW

The current position of the robot is determined according to the pulse count value supplied from the Pulsecoder on each axis. Mastering is factory‑performed. It is unnecessary to perform mastering in daily operations. However, mastering is required under the following conditions:

- Motor replacement.
- Pulsecoder replacement.
- Reducer replacement.
- Cable replacement.
- Batteries for pulse count backup in the mechanical unit have gone dead.

# CAUTION

Robot data (including mastering data) and Pulsecoder data are backed up by their respective backup batteries. Data will be lost if the batteries die. Replace the batteries in the controller and mechanical units periodically. An alarm will alert you when battery voltage is low.

# Types of Mastering

There are following mastering methods:

|Fixture position mastering|Mastering performed with the mastering fixture.|
|---|---|
|Zero-position mastering|Mastering which performed with all axes set at the 0-degree position. A zero-position mark (witness mark) is attached to each robot axis. This mastering is performed with all axes aligned to their respective witness marks.|
|Quick mastering|This is performed at a user-specified position. The corresponding count value is obtained from the rotation count of the Pulsecoder connected to the relevant motor and the rotation angle within one rotation. Quick mastering uses the fact that the absolute value of a rotation angle within one rotation will not be lost. (All axes at the same time)|
|Quick mastering for single axis|This is performed at a user-specified position for one axis. The corresponding count value is obtained from the rotation count of the Pulsecoder connected to the relevant motor and the rotation angle within one rotation. Quick mastering uses the fact that the absolute value of a rotation angle within one rotation will not be lost.|
|Single axis mastering|Mastering which performed for one axis at a time. The mastering position for each axis can be specified by the user. Useful in performing mastering on a specific axis.|
|Mastering data entry|Enter the Mastering data directly.|

This section describes zero‑position mastering, quick mastering, quick mastering for single axis, single‑axis mastering, and mastering data entry. For more detailed mastering (fixture position mastering), contact your local FANUC representative.

This section describes zero‑position mastering, quick mastering, single‑axis mastering, and mastering data entry. For more detailed mastering (fixture position mastering), contact your local FANUC representative.

‑ 39 ‑

# Table 8.1 (a) Type of mastering
---
# 8. MASTERING

# CAUTION

1. If mastering is performed incorrectly, the robot may behave unexpectedly. This is very dangerous. For this reason, the Master/Cal screen is designed to appear only when the $MASTER_ENB system variable is 1 or 2. After performing positioning, press F5, ([DONE]) on the Master/Cal screen. The $MASTER_ENB system variable is then reset to 0 automatically, and the Master/Cal screen will disappear.
2. Before performing mastering, it is recommended that you back up the current mastering data.

# 8.2 RESETTING ALARMS AND PREPARING FOR MASTERING

Before performing mastering because a motor is replaced, you must release the relevant alarm and display the positioning menu.

Alarm displayed: “SRVO‑062 BZAL” or “SRVO‑075 Pulse not established”

# Procedure

1. Display the positioning menu by following steps 1 to 6.
1. Press the [MENU] key to display the screen menu.
2. Press [0 NEXT] and select [6 SYSTEM].
3. Press F1 [TYPE], and select [SYSTEM Variable] from the menu.
4. Place the cursor on $MASTER_ENB, then key in [1] and press [ENTER] key.
5. Press F1 [TYPE], and select [Master/Cal] from the menu.
6. Select the desired mastering type from the [Master/Cal] menu.
2. To reset the "SRVO‑062 BZAL" alarm, follow steps 1 to 5.
1. Press the [MENU] key to display the screen menu.
2. Press [0 NEXT] and select [6 SYSTEM].
3. Press F1 [TYPE], and select [Master/Cal] from the menu.
4. Press the F3 [RES_PCA], then press F4 [YES].
5. Turn off the controller power and on again.
3. To reset the "SRVO‑075 Pulse not established" alarm, follow steps 1 to 2.
1. When the controller power is turned on again, the message "SRVO‑075 Pulse not established" appears again.
2. Move the axis for which the message mentioned above has appeared in either direction till the alarm disappears when you press [FAULT RESET].
---
# 8. MASTERING

# 8.3 ZERO POSITION MASTERING

Zero‑position mastering (witness mark mastering) is performed with all axes set at the 0‑degree position. A zero‑position mark (witness mark) is attached to each robot axis (Fig. 8.3 (a)). This mastering is performed with all axes set at the 0‑degree position using their respective witness marks. Zero‑position mastering involves a visual check. It cannot be so accurate. It should be used only as a quick‑fix method.

# Procedure of Zero-position Mastering

1. Press the [MENU] key to display the screen menu.
2. Select [0 NEXT] and press [6 SYSTEM].
3. Press F1 [TYPE].
4. Select [Master/Cal].

|SYSTEM Master/Cal|AUTO|JOINT 10 %|TORQUE = [ON]|
|---|---|---|---|
|1|FIXTURE POSITION MASTER| | |
|2|ZERO POSITION MASTER| | |
|3|QUICK MASTER| | |
|4|QUICK MASTER FOR SINGLE AXIS| | |
|5|SINGLE AXIS MASTER| | |
|6|SET QUICK MASTER REF| | |
|7|CALIBRATE| | |

Press 'ENTER' or number key to select.

[ TYPE ] LOAD RES_PCA DONE

Release brake control, and jog the robot into a posture for mastering.

NOTE

Brake control can be released by setting the system variables as follows:

$PARAM_GROUP.SV_OFF_ALL : FALSE

$PARAM_GROUP.SV_OFF_ENB[*] : FALSE (for all axes)

After changing the system variables, turn off the controller power and on again.

Select [2 ZERO POSITION MASTER]. Press F4 [YES].

|SYSTEM Master/Cal|AUTO|JOINT 10 %|TORQUE = [ON]|
|---|---|---|---|
|1|FIXTURE POSITION MASTER| | |
|2|ZERO POSITION MASTER| | |
|3|QUICK MASTER| | |
|4|QUICK MASTER FOR SINGLE AXIS| | |
|5|SINGLE AXIS MASTER| | |
|6|SET QUICK MASTER REF| | |
|7|CALIBRATE| | |

Robot Mastered! Mastering Data:

&lt;0&gt; &lt;11808249&gt; &lt;38767856&gt;

&lt;9873638&gt; &lt;12200039&gt; &lt;2000319&gt;

[ TYPE ] LOAD RES_PCA DONE
---
# 8. MASTERING

Select [7 CALIBRATE] and press F4 [YES]. Mastering will be performed automatically. Alternatively, turn off the controller power and on again. Turning on the power always causes positioning to be performed.

SYSTEM Master/Cal AUTO JOINT 10 %

TORQUE = [ON]

1. FIXTURE POSITION MASTER
2. ZERO POSITION MASTER
3. QUICK MASTER
4. QUICK MASTER FOR SINGLE AXIS
5. SINGLE AXIS MASTER
6. SET QUICK MASTER REF
7. CALIBRATE

Robot Calibrated! Cur Jnt Ang(deg):

&lt; 0.0000&gt; &lt; 0.0000&gt; &lt; 0.0000&gt;

&lt; 0.0000&gt; &lt; 0.0000&gt; &lt; 0.0000&gt;

After positioning is completed, press F5 [DONE].

DONE

F5

Return brake control to original setting, and cycle power of the controller.

# Table 8.3 (a) Posture with position marks (witness mark) aligned

|Axis|Position|
|---|---|
|J1-axis|0 deg|
|J2-axis|0 deg|
|J3-axis|0 deg (When J2-axis is 0 deg.)|
|J4-axis|0 deg|
|J5-axis|0 deg|
|J6-axis|0 deg|
---
# 8. MASTERING

|Zero-position mark (J2)| | |合いマーク|J2| | | | | |
|---|---|---|---|---|---|---|---|---|---|
|45°|Zero-position mark (J4)|合いマーク|J4|Zero-position mark (J6)|J6|合いマーク| | | |
| |Zero-position mark (J1)| | | |合いマーク|J1|Zero-position mark (J5)|合いマーク|J5|
|Detail of|合いマーク|合いマーク|Zero-position mark (J3)|J3| | | | | |

Section A-A

断面 A-A

矢視 B

Fig. 8.3 (a) Zero-position mark (witness mark) for each axis

‑ 43 ‑
---
# 8. MASTERING

# 8.4 QUICK MASTERING

Quick mastering is performed at a user‑specified position. The pulse count value is obtained from the rotation speed of the Pulsecoder connected to the relevant motor and the rotation angle within one rotation. Quick mastering uses the fact that the absolute value of a rotation angle within one rotation will not be lost.

Quick mastering is factory‑performed at the position indicated in Table 8.3 (a). Do not change the setting unless there is any problem.

If setting the robot at the position mentioned above is impossible, you must re‑set the quick mastering reference position using the following method. (It would be convenient to set up a marker that can work in place of the witness mark.)

# CAUTION

1. Quick mastering can be used, if the pulse count value is lost, for example, because a low voltage has been detected on the backup battery for the pulse counter.
2. Quick mastering cannot be used, after the Pulsecoder is replaced or after the mastering data is lost from the robot controller.

# Procedure Recording the Quick Mastering Reference Position

1. Select [6 SYSTEM].
2. Select [Master/Cal]. The positioning screen will be displayed.

|SYSTEM Master/Cal|AUTO|JOINT 10 %|TORQUE = [ON]|
|---|---|---|---|
|1 FIXTURE POSITION MASTER|2 ZERO POSITION MASTER|3 QUICK MASTER|4 QUICK MASTER FOR SINGLE AXIS|
|5 SINGLE AXIS MASTER|6 SET QUICK MASTER REF|7 CALIBRATE|Press 'ENTER' or number key to select.|
|[ TYPE ]|LOAD|RES_PCA|DONE|

Release brake control, and jog the robot to the quick mastering reference position.
Select [6 SET QUICK MASTER REF] and press F4 [YES]. Quick mastering reference position will be set.

# CAUTION

If the robot has lost mastering data due to mechanical disassembly or repair, you cannot perform this procedure. In this case, perform Fixture position mastering or zero–position mastering is required to restore mastering data.

‑ 44 ‑
---
# 8. MASTERING

# Procedure of Quick Mastering

1. Display the Master/Cal screen.
|SYSTEM Master/Cal|AUTO|JOINT 10 %|TORQUE = [ON]|
|---|---|---|---|
|1 FIXTURE POSITION MASTER|2 ZERO POSITION MASTER|3 QUICK MASTER|4 QUICK MASTER FOR SINGLE AXIS|
|5 SINGLE AXIS MASTER|6 SET QUICK MASTER REF|7 CALIBRATE|Robot Not Mastered!|
|Quick master? [NO]| | | |
2. Release brake control, and jog the robot to the quick mastering reference position.
3. Select [3 QUICK MASTER] and press F4 [YES]. Quick mastering reference position will be set.
2 ZERO POSITION MASTER
3 QUICK MASTER
4 QUICK MASTER FOR SINGLE AXIS
4. Select [7 CALIBRATE] and press the [ENTER] key. Calibration is executed. Calibration is executed by cycling power.
5. After completing the calibration, press F5 [Done].
DONE
F5
6. Return brake control to original setting, and cycle power of the controller.
---
# 8. MASTERING

# 8.5 QUICK MASTERING FOR SINGLE AXIS

Quick mastering is performed at a user‑specified position for one axis. The pulse count value is obtained from the rotation times of the Pulsecoder connected to the relevant motor and the rotation angle within one rotation. Quick mastering uses the character that the absolute value of a rotation angle within one rotation will not be lost.

Quick mastering is factory‑performed at the position indicated in Table 8.3 (a). Do not change the setting unless there is any problem.

If setting the robot at the position mentioned above is impossible, you must re‑set the quick mastering reference position using the following method. (It would be convenient to set up a marker that can work in place of the witness mark.)

# CAUTION

1. Quick mastering can be used, if the pulse count value is lost, for example, because a low voltage has been detected on the backup battery for the pulse counter.
2. Quick mastering cannot be used, after the Pulsecoder is replaced or after the mastering data is lost from the robot controller.

# Procedure Recording the Quick Mastering Reference Position

1. Select [6 SYSTEM].
2. Select [Master/Cal]. The positioning screen will be displayed.

|SYSTEM Master/Cal|AUTO|JOINT 10 %|
|---|---|---|
|TORQUE = [ON]|1 FIXTURE POSITION MASTER|2 ZERO POSITION MASTER|
|3 QUICK MASTER|4 QUICK MASTER FOR SINGLE AXIS|5 SINGLE AXIS MASTER|
|6 SET QUICK MASTER REF|7 CALIBRATE|Press 'ENTER' or number key to select.|
|[ TYPE ]|LOAD|RES_PCA|
|DONE|DONE|DONE|

Release brake control, and jog the robot to the quick mastering reference position.
Select [6 SET QUICK MASTER REF] and press F4 [YES]. Quick mastering reference position will be set.

# CAUTION

If the robot has lost mastering data due to mechanical disassembly or repair, you cannot perform this procedure. In this case, perform Fixture position mastering or zero –position mastering is required to restore mastering data.
---
# 8. MASTERING

# Procedure of Quick Mastering

1. Display the Master/Cal screen.

SYSTEM Master/Cal               AUTO      JOINT 10 %
TORQUE = [ON ]
1 FIXTURE POSITION MASTER
2 ZERO POSITION MASTER
3 QUICK MASTER
4 QUICK MASTER FOR SINGLE AXIS
5 SINGLE AXIS MASTER
6 SET QUICK MASTER REF
7 CALIBRATE
Press 'ENTER' or number key to select.
[ TYPE ]    LOAD      RES_PCA                    DONE

2. Select [4 QUICK MASTER FOR SINGLE AXIS]. The quick master for single axis screen will be displayed.

SINGLE AXIS MASTER                  AUTO      JOINT 10%
1/9
ACTUAL     POS      (MSTR POS)        (SEL)    [ST]
J1          0.000       (       0.000)    (0)      [2]
J2          0.000       (       0.000)    (0)      [2]
J3          0.000       (       0.000)    (0)      [2]
J4          0.000       (       0.000)    (0)      [2]
J5          0.000       (       0.000)    (0)      [2]
J6          0.000       (       0.000)    (0)      [0]
E1          0.000       (       0.000)    (0)      [0]
E2          0.000       (       0.000)    (0)      [0]
E3          0.000       (       0.000)    (0)      [0]

3. Move the cursor to the [SEL] column for the unmastered axis and press the numeric key [1].
Setting of [SEL] is available for one or more axes.

SINGLE AXIS MASTER                  AUTO      JOINT 10%
1/9
ACTUAL      POS     (MSTR POS)        (SEL)    [ST]
J5          0.000       (      0.000)     (0)      [2]
J6          0.000       (      0.000)     (0)      [0]

4. Turn off brake control, then jog the robot to the quick mastering reference position.
5. Press F5 [EXEC]. Mastering is performed. So, [SEL] is reset to 0, and [ST] is re-set to 2.
6. Select [7 CALIBRATE] and press [ENTER] key. Calibration is executed. Calibration is executed by cycling power.
7. After completing the calibration, press F5 Done.

DONE
F5

8. Return brake control to original setting, and cycle power of the controller.
---
# 8. MASTERING

# 8.6 SINGLE AXIS MASTERING

Single axis mastering is performed for one axis at a time. The mastering position for each axis can be specified by the user.

Single axis mastering can be used, if mastering data for a specific axis is lost, for example, because a low voltage has been detected on the pulse counter backup battery or because the Pulsecoder has been replaced.

|SINGLE AXIS MASTER| | | |AUTO|JOINT|10%|
|---|---|---|---|---|---|---|
|ACTUAL POS (MSTR POS)| | | | |(SEL)|[ST]|
| |J1|0.000|(0.000)| |(0)|[2]|
| |J2|0.000|(0.000)| |(0)|[2]|
| |J3|0.000|(0.000)| |(0)|[2]|
| |J4|0.000|(0.000)| |(0)|[2]|
| |J5|0.000|(0.000)| |(0)|[2]|
| |J6|0.000|(0.000)| |(0)|[0]|
| |E1|0.000|(0.000)| |(0)|[0]|
| |E2|0.000|(0.000)| |(0)|[0]|
| |E3|0.000|(0.000)| |(0)|[0]|

# Table 8.6 (a) Items set in single axis mastering

|Item|Description|
|---|---|
|Current position (ACTUAL AXIS)|The current position of the robot is displayed for each axis in degree units.|
|Mastering position (MSTR POS)|A mastering position is specified for an axis to be subjected to single axis mastering. It would be convenient if it is set to the 0 degree position.|
|SEL|This item is set to 1 for an axis to be subjected to single axis mastering. Usually, it is 0.|
|ST|This item indicates whether single axis mastering has been completed for the corresponding axis. It cannot be changed directly by the user. The value of the item is reflected in $EACHMST_DON (1 to 9).|
| |0 : Mastering data has been lost. Single axis mastering is necessary.|
| |1 : Mastering data has been lost. (Mastering has been performed only for the other interactive axes.) Single axis mastering is necessary.|
| |2 : Mastering has been completed.|
---
# 8. MASTERING

# Procedure of Single axis mastering

1. Select [6 SYSTEM].
2. Select [Master/Cal].

SYSTEM Master/Cal AUTO JOINT 10 %

TORQUE = [ON]

- 1 FIXTURE POSITION MASTER
- 2 ZERO POSITION MASTER
- 3 QUICK MASTER
- 4 QUICK MASTER FOR SINGLE AXIS
- 5 SINGLE AXIS MASTER
- 6 SET QUICK MASTER REF
- 7 CALIBRATE

Press 'ENTER' or number key to select.

[ TYPE ] LOAD RES_PCA DONE
3. Select [5 SINGLE AXIS MASTER]. The following screen will be displayed.

SINGLE AXIS MASTER AUTO JOINT 10% 1/9

|ACTUAL POS| | |(MSTR POS)| |(SEL)|[ST]|
|---|---|---|---|---|---|---|
| |J1|0.000|(0.000)| |(0)|[2]|
| |J2|0.000|(0.000)| |(0)|[2]|
| |J3|0.000|(0.000)| |(0)|[2]|
| |J4|0.000|(0.000)| |(0)|[2]|
| |J5|0.000|(0.000)| |(0)|[2]|
| |J6|0.000|(0.000)| |(0)|[0]|
| |E1|0.000|(0.000)| |(0)|[0]|
| |E2|0.000|(0.000)| |(0)|[0]|
| |E3|0.000|(0.000)| |(0)|[0]|
4. For the axis to which to perform single axis mastering, set (SEL) to “1.” Setting of [SEL] is available for one or more axes.
5. Turn off brake control, then jog the robot to the mastering position.
6. Enter axis data for the mastering position.
7. Press F5 [EXEC]. Mastering is performed. So, [SEL] is reset to 0, and [ST] is reset to 2 or 1.

EXEC SINGLE AXIS MASTER AUTO JOINT 10% 6/9

|ACTUAL POS| | |(MSTR POS)|(SEL)|[ST]| | |
|---|---|---|---|---|---|---|---|
| | |F5|J1|0.000|(0.000)|(0)|[2]|
| | |J2|0.000|(0.000)|(0)|[2]| |
| | |J3|0.000|(0.000)|(0)|[2]| |
| | |J4|0.000|(0.000)|(0)|[2]| |
| | |J5|0.000|(0.000)|(0)|[2]| |
| | | |J6|90.000|(0.000)|(1)|[0]|
| | |E1|0.000|(0.000)|(0)|[0]| |
| | |E2|0.000|(0.000)|(0)|[0]| |
| | |E3|0.000|(0.000)|(0)|[0]| |

EXEC

‑ 49 ‑
---
# 8. MASTERING

When single axis mastering is completed, press the previous page key to resume the previous screen.

|SYSTEM Master/Cal|AUTO|JOINT 10 %|TORQUE = [ON]|
|---|---|---|---|
|1 FIXTURE POSITION MASTER|2 ZERO POSITION MASTER|3 QUICK MASTER|4 QUICK MASTER FOR SINGLE AXIS|
|5 SINGLE AXIS MASTER|6 SET QUICK MASTER REF|7 CALIBRATE|Press 'ENTER' or number key to select.|

[ TYPE ] LOAD RES_PCA DONE

# 9

Select [7 CALIBRATE], then press F4 [YES]. Positioning is performed. Alternatively, turn off the controller power and on again. Positioning is performed.

# 10

After positioning is completed, press F5 [DONE].

DONE

F5

# 11

Return brake control to original setting, and cycle power of the controller.

‑ 50 ‑
---
# 8. MASTERING

# 8.7 MASTERING DATA ENTRY

This function enables mastering data values to be assigned directly to a system variable. It can be used if mastering data has been lost but the pulse count is preserved.

# Mastering data entry method

1. Press the [MENU] key, then press [0 NEXT] and select [6 SYSTEM].
2. Press F1 [TYPE]. Select [Variables]. The system variable screen appears.

| |SYSTEM Variables|AUTO|JOINT 10%|1/669|
|---|---|---|---|---|
|1|$AAVM_GRP|AAVM_GRP_T| | |
|2|$AAVM_WRK|AAVM_WRK_T| | |
|3|$ABSPOS_GRP|ABSPOS_GRP_T| | |
|4|$ACC_MAXLMT|0| | |
|5|$ACC_MINLMT|0| | |
|6|$ACC_PRE_EXE|0| | |

3 Change the mastering data. The mastering data is saved to the $DMR_GRP.$MASTER_COUN system variable.

| |SYSTEM Variables|AUTO|JOINT 10%|1/669|
|---|---|---|---|---|
|135|$DMR_GRP|DMR_GRP_T| | |
|136|$DMSW_CFG|DMSW_CFG_T| | |

4 Select $DMR_GRP.

|SYSTEM Variables|AUTO|JOINT 10%|1/1|
|---|---|---|---|
|$DMR_GRP|1/29| | |
|1|$MASTER_DONE|FALSE| |
|2|$OT_MINUS|[9] of BOO LEAN| |
|3|$OT_PLUS|[9] of BO OLEAN| |
|4|$NASTER_COUN|[9] of INTEGER| |
|5|$REF_DONE|FALSE| |
|6|$REF_POS|[9] of REAL| |

[ TYPE ] TRUE FALSE

‑ 51 ‑
---
# 8. MASTERING

Select $MASTER_COUN, and enter the mastering data you have recorded.

|SYSTEM Variables|AUTO|JOINT 10%|
|---|---|---|
|$DMR_GRP[1].$MASTER_COUN|1/9| |
|[1]|95678329| |
|[2]|10223045| |
|[3]|3020442| |
|[4]|30405503| |
|[5]|20497709| |
|[6]|2039490| |
|[7]|0| |
|[8]|0| |
|[9]|0| |

[ TYPE ]

Press [PREV] key.

Set $MASTER_DONE to TRUE.

|SYSTEM Variables|AUTO|JOINT 10%|
|---|---|---|
|$DMR_GRP|1/29| |
|$MASTER_DONE|TRUE| |
|$OT_MINUS|[9] of BOO LEAN| |

[ TYPE ]

TRUE
FALSE
Display the positioning screen, and select [7 CALIBRATE], then press F4 [YES].

After completing positioning, press F5 [DONE].

DONE

F5

‑ 52 ‑
---
# 8. MASTERING

# 8.8 VERIFYING MASTERING

1. How to verify that the robot is mastered properly:
Usually, positioning is performed automatically when the power is turned on. To check whether mastering has been performed correctly, examine if the current displayed position meets the actual robot position by using the procedure described below:

1. Reproduce a particular point in a program. Check whether the point agrees with the specified position.
2. Set all axes of the robot to their 0-degree (0 rad) positions. Check that the zero-degree position marks indicated in Section 8.3 of OPERATOR’S MANUAL are aligned. There is no need to use a visual aid.

If the displayed and actual positions do not match, the counter value for a Pulsecoder may have been invalidated as a result of an alarm described in 2. Alternatively, the mastering data in system variable $DMR_GRP.$MASTER_COUN may have been overwritten as a result of an operation error or some other reason. Compare the data with the values indicated on the supplied data sheet. This system variable is overwritten whenever mastering is performed. Whenever mastering is performed, record the value of the system variable on the data sheet.
2. Alarm type displayed during mastering and their solution method:
1. BZAL alarm
This alarm is displayed if the Pulsecoder's backup battery voltage decreases to 0 V while the power to the controller is disconnected. Furthermore, if the Pulsecoder connector is removed for cable replacement, etc. this alarm is displayed as the voltage decreases to 0. Confirm if the alarm will disappear by performing a pulse reset (See Section 8.2.). Then, cycle power of the controller to check if the alarm disappears or not. The battery may be drained if the alarm is still displayed. Perform a pulse reset, and turn off and on the controller power after replacing the battery. Note that, if this alarm is displayed, all the original data held by the Pulsecoder will be lost. Mastering is required.
2. BLAL alarm
This alarm is displayed if the voltage of the Pulsecoder's backup battery has fallen to a level where backup is no longer possible. If this alarm is displayed, replace the battery with a new one immediately while keeping the power turned on. Check whether the current position data is valid, using the procedure described in 1.
3. Alarm notification like CKAL, RCAL, PHAL, CSAL, DTERR, CRCERR, STBERR, and SPHAL may have trouble with Pulsecoder, contact your local FANUC representative.
---
# 9. TROUBLESHOOTING

The source of mechanical unit problems may be difficult to locate because of overlapping causes. Problems may become further complicated, if they are not corrected properly. Therefore, you must keep an accurate record of problems and take proper corrective actions.

# 9.1 TROUBLESHOOTING

Table 9.1 (a) shows the major troubleshooting that may occur in the mechanical unit and their probable causes. If you cannot pinpoint a failure cause or which measures to take, contact your local FANUC representative.

|Symptom|Description|Cause|Measure|
|---|---|---|---|
|Vibration|- The J1 base lifts off the base plate as the robot operates. - There is a gap between the J1 base and base plate. - A J1 base retaining bolt is loose.|[J1 base fastening]|- If a bolt is loose, apply LOCTITE and tighten it with the appropriate torque. - Adjust the base plate surface flatness to within the specified tolerance. - If there is any foreign material between the J1 base and base plate, eliminate them. - If the robot is not securely fastened to the floor plate, the J1 base lift from the ground. Thus may cause the collision, and lead to vibration.|
| |- The rack or floor plate vibrates during operation of the robot.|[Rack or floor]|- Reinforce the rack or floor to make it more rigid. - If reinforcing the rack or floor is impossible, modify the robot control program; doing so will reduce the vibration.|
| |- Vibration becomes more serious when the robot is in a specific posture. - If the operating speed of the robot is reduced, vibration stops. - Vibration is most noticeable when the robot is accelerating. - Vibration occurs when two or more axes operate at the same time.|[Overload]|- Check the maximum load that the robot can handle or not. If the robot is overloaded, reduce the load, or modify the robot control program. - Vibration can be reduced by re-modifying the robot control program; reducing speed or acceleration with minimizing the influence on the entire cycle time.|
---
# 9. TROUBLESHOOTING

|Symptom|Description|Cause|Measure|
|---|---|---|---|
|Vibration|- Vibration was first noticed after the robot collided with an object or the robot was overloaded for a long period. - Periodic vibration and noise occur.|[Gear, bearing, or reducer] - It is likely that collision or overload applied an excessive force on the drive mechanism, thus damaging the tooth surface or rolling contact surface of a bearing, or reducer. - It is likely that prolonged use of the robot while overloaded caused fretting of the tooth surface or rolling contact surface of a bearing, or reducer due to resulting metal fatigue. - It is likely that foreign matter caught in a gear, bearing, or within a reducer caused damage on the tooth surface or rolling contact surface of the bearing, or reducer. - It is likely that foreign matter caught in a gear, bearing, or within a reducer caused vibration.|- Operate one axis at a time to determine which axis is vibrating. - Remove the motor, and replace the gear, the bearing, and the reducer. For the spec. of parts and the method of replacement, contact FANUC. - Using the robot within its maximum rating prevents problems with the drive mechanism.|
|Noise (Continued)|- There is some relationship between the vibration of the robot and the operation of a machine near the robot.|[Noise from a nearby machine] - If the robot is not grounded properly, electrical noise is induced on the grounding wire, preventing commands from being transferred accurately, thus leading to vibration. - If the robot is grounded at an unsuitable point, its grounding potential becomes unstable, and noise is likely to be induced on the grounding line, thus leading to vibration.|- Connect the grounding wire firmly to ensure a reliable ground potential and prevent extraneous electrical noise.|
---
# 9. TROUBLESHOOTING

|Symptom|Description|Cause|Measure|
|---|---|---|---|
|Vibration|- The cause of problem cannot be identified from examination of the floor, rack, or mechanical unit.|[Controller, cable, and motor]|- Refer to the Controller Maintenance Manual for troubleshooting related to the controller and amplifier. - Replace the motor of the axis that is vibrating, and check whether vibration still occurs. To replace the motor, Contact your local FANUC representative. - If vibration occurs only when the robot assumes a specific posture, it is likely that a cable in the mechanical unit is broken. - Check whether the jacket of the cable connecting the mechanical unit and controller is damaged. If so, replace the connection cable, and check whether vibration still occurs. - Check whether the jacket of the power cable is damaged. If so, replace the power cable, and check whether vibration still occurs. - Check that the robot is supplied with the rated voltage. - Check that the robot control parameter is set to a valid value. If it is set to an invalid value, correct them. Contact your local FANUC representative for further information if necessary.|
|Noise (Continued)|- Pulsecoder defect may be the cause of the vibration as the motor cannot propagate the accurate position to the controller. - If the motor becomes defective, vibration might occur because the motor cannot deliver its rated performance. - If a power line in a movable cable of the mechanical unit has an intermittent break, vibration might occur because the motor cannot accurately respond to commands. - If a Pulsecoder wire in a movable part of the mechanical unit has an intermittent break, vibration might occur because commands cannot be sent to the motor accurately. - If a connection cable between the mechanical unit and the controller has an intermittent break, vibration might occur. - If the power supply cable is about to be snapped, vibration might occur. - If the power source voltage drops below the rating, vibration might occur. - It may vibrate when the invalid value parameter was set.| | |
|Rattling|- While the robot is not supplied with power, pushing it with the hand causes tottering part of the mechanical unit. - There is a gap on the mounting face of the mechanical unit.|[Mechanical unit coupling bolt]|- Check the following retaining bolts tightness for each axis. If any of these bolts is loose, apply LOCTITE and bolt down with appropriate torque. - Motor - Reducer - Reducer shaft - Base - Arm - Casting - End effector|
---
# 9. TROUBLESHOOTING

|Symptom|Description|Cause|Measure|
|---|---|---|---|
|Motor overheating|- The ambient temperature of the installation location increases, causing the motor to overheat. - After the robot control program or the load was changed, the motor overheated.|[Ambient temperature] - It is likely that a rise in the ambient temperature prevented the motor from releasing heat efficiently, thus leading to overheating. [Operating condition] - It is likely that the robot was operated with the maximum average current exceeded.|- The teach pendant can be used to monitor the average current. Check the average current when the robot control program is running. The allowable average current is specified for the robot according to its ambient temperature. Contact FANUC for further information. - Relaxing the robot control program and conditions can reduce the average current, thus preventing overheating. - Reducing the ambient temperature is the most effective means of preventing overheating. - Having the surroundings of the motor well ventilated enables the motor to release heat efficiently, thus preventing overheating. Using a fan to direct air at the motor is also effective. - If there is a source of heat near the motor, it is advisable to install shielding to protect the motor from heat radiation.|
| |- After a robot control parameter (load setting etc.) was changed, the motor overheated.|[Parameter] - If data input for a workpiece is invalid, the robot cannot accelerate or decelerate normally, so the average current increases, leading to the motor overheating.|- As for load setting, input an appropriate parameter referring to Section 4.2 of the operator’s manual.|
| |- Symptom other than stated above|[Mechanical unit problems] - It is likely that problems occurred in the mechanical unit drive mechanism, thus placing an excessive load on the motor. [Motor problems] - It is likely that motor brake failure locked on the brake, and caused the motor overloaded.|- Repair the mechanical unit referring to the above descriptions of vibration, noise, and rattling. - Check that, when the servo system is energized, the brake is released. If the brake remains applied to the motor all the time, replace the motor. - Judgment is possible if the average current decreased after replacing the motor, the former motor had been defected.|
---
# 9. TROUBLESHOOTING

|Symptom|Description|
|---|---|
|Grease leakage|- Grease or oil is leaking from the mechanical unit.|
|Oil leakage| |
|Dropping axis|- An axis falls because the brake went out. - An axis falls in standstill.|

|Cause|Measure|
|---|---|
|[Poor sealing]|- If a crack develops in the casting, sealant can be used as a quick-fix to prevent further grease or oil leakage. However, the component should be replaced as soon as possible, because the crack might extend. - Probable causes are a crack in the casting, a broken O-ring, a damaged oil seal, or a loose seal bolt. - A crack in a casting can occur due to excessive force that might be caused in collision. - An O-ring can be damaged if it is trapped or cut during disassembling or re-assembling. - An oil seal might be damaged if extraneous dust scratches the lip of the oil seal.|
| |- O-rings are used in the locations listed below. - Motor coupling section - Reducer (case and shaft) coupling section - Wrist connection section - J3 arm coupling section - Inside the wrist|
| |- Oil seals are used in the locations stated below. - Inside the reducer - Inside the wrist|
|[Brake drive relay and motor]|- Check whether the brake drive relay contacts stuck to each other or not. If they are found to be stuck, replace the relay. - Replace the motor confirmed following symptoms. - Brake shoe is worn out - Brake main body is damaged - Oil soak through the motor|
| |- It is likely that oil or grease soak through the motor, causing the brake to slip.|
---
# B-84194EN/01

# Symptom

# Displacement

- The robot operates at a point other than the taught position.
- The repeatability is not within the tolerance.
- Displacement occurs only in specific peripheral equipment.
- Displacement occurred after a parameter was changed.

# BZAL alarm Displayed.

- BZAL is displayed on the teach pendant screen.

# Though a person does not touch the robot, a contact stop or payload error occurs and stops the robot

- Though a person does not touch the robot, robot stops due to contact stop.
- Robot stops due to payload error.

# Cross check alarm displayed.

- Cross check alarm is displayed on the teach pendant screen.

# 9. TROUBLESHOOTING

|Cause|Measure|
|---|---|
|[Mechanical unit problems]|- If the repeatability is unstable, probable causes are a failure in the drive mechanism or a loose bolt, and so on.
- If the repeatability is stable, correct the taught program. The problem will not occur unless another collision occurs.
- If the Pulsecoder is faulty, replace the motor or the Pulsecoder.
|
|[Peripheral equipment displacement]|- Correct the setting of the peripheral equipment position.
- Correct the taught program.
|
|[Parameter]|- Re-enter the previous optimal mastering data.
- If optimal mastering data is unavailable, perform mastering again.
- Replace the battery.
- Replace the cable.
- It is likely that the Pulsecoder cable is defective.
|
|Unintended contact occurred.|Get rid of the matter which contact with the robot.|
|Incorrect robot installation is performed.|Install the robot according to Section 1.2.|
|The end effector or the workpiece does not match the load setting.|Match the end effector and the workpiece to the load setting.|
|Vibration of the floor or the hand is applied to the robot.|Make sure that vibration of the floor or the hand is not applied to the robot.|
|Refer to “Though a person does not touch the robot, a contact stop or payload error occurs and stops the robot” contents.|Refer to “Though a person does not touch the robot, a contact stop or payload error occurs and stops the robot” contents.|
|It is likely that the sensor is broken.|Replace the unit.|
---
NO_CONTENT_HERE
---
APPENDIX
---
NO_CONTENT_HERE
---
# APPENDIX A. PERIODIC MAINTENANCE TABLE

PERIODIC MAINTENANCE TABLE
---
# A. PERIODIC MAINTENANCE TABLE

# APPENDIX

# B-84194EN/01

# FANUC Robot CRX-10iA, CRX-10iA/L

# Periodic Maintenance Table

|Items|Accumulated operating time (H)|Oil Check time|Grease check| | | | | | | | | | | | | | | | | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | |First|3 months|6 months|9 months|1 year|2 years|3 years|4 years|5 years|6 years| | | | | | | | | |
| | | |1|Check for external damage or peeling paint|0.1H|-|○|○|○|○|○|○|○|○| | | | | | | | | |
| |2|Check for water|0.1H|-| | |○|○|○|○|○|○|○|○| | | | | | | | | |
| | | |3|Check the end effector (hand) cable| | | | | | | | | |0.1H|-|○|○|○| | | | | |
| |4|Check the exposed connector (Loosening)|0.1H|-| | |○| |○| | | | | | | | | | | | | | |
| |5|Tighten the end effector bolt|0.1H|-| | |○| |○| | | | | | | | | | | | | | |
| |6|Tighten the cover and main bolt|1.0H|-| | |○| |○| | | | | | | | | | | | | | |
| |7|Remove spatter and dust etc.|1.0H| | | |○| |○| | | | | | | | | | | | | | |
| |8|Check the robot cable, teach pendant cable and robot connecting cable|0.2H|-| | |○| |○| | | | | | | | | | | | | | |
| |9|Cleaning the controller ventilation system|0.2H|-|○|○|○|○|○|○|○|○| | | | | | | | | | | |

*1

●: requires order of parts

○: does not require order of parts
---
# APPENDIX A. PERIODIC MAINTENANCE TABLE

| | | | | | | | | | | | | | | | | | | | |Item|years| | | | | |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|3| | | |4| | | |5| | | |6| | | |7| | | |8| | | | | | |
| | | | | | | | | | | | | | | | | | | | |1|○|○|○|○|○|○|
| | | | | | | | | | | | | | | | | | | | |2|○|○|○|○|○|○|
| | | | | | | | | | | | | | | | | | | | |3|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |4|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |5|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |6|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |7|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |8|○| |○| |○| |
| | | | | | | | | | | | | | | | | | | | |9|○|○|○|○|○|○|

‑ 65 ‑
---
# MOUNTING BOLT TORQUE LIST

NOTE

When applying LOCTITE to a part, spread the LOCTITE on the entire length of the engaging part of the female thread. If applied to the male threads, poor adhesion can occur potentially loosening the bolt. Clean the bolts and the threaded holes and wipe off the oil on the engaging section. Make sure that there is no solvent left in the threaded holes. In this case, remove all the excess LOCTITE when you are finished screwing the bolts into the threaded holes.

Use the following strength bolts. Comply with any bolt specification instructions as specified.

Hexagon socket head bolt made of steel:

- Size M22 or less: Tensile strength 1200N/mm2 or more
- Size M24 or more: Tensile strength 1000N/mm2 or more
- All size plating bolt: Tensile strength 1000N/mm2 or more

Hexagon bolt, stainless bolt, special shape bolt (button bolt, low‑head bolt, flush bolt, etc.) Tensile strength 400N/mm2 or more

Refer to the following tables if the bolts tightening torque are not specified.

# Recommended bolt tightening torques

Unit: Nm

|Nominal diameter|Hexagon socket head bolt (steel)|Hexagon socket head bolt (stainless)|Hexagon socket head button bolt (steel)|Hexagon bolt (steel)| | | | |
|---|---|---|---|---|---|---|---|---|
|Tightening torque Upper limit|Tightening torque Lower limit|Tightening torque Upper limit|Tightening torque Lower limit|Tightening torque Upper limit|Tightening torque Lower limit|Tightening torque Upper limit|Tightening torque Lower limit| |
|M3|1.8|1.3|0.76|0.53|――――|――――|――――|――――|
|M4|4.0|2.8|1.8|1.3|1.8|1.3|1.7|1.2|
|M5|7.9|5.6|3.4|2.5|4.0|2.8|3.2|2.3|
|M6|14|9.6|5.8|4.1|7.9|5.6|5.5|3.8|
|M8|32|23|14|9.8|14|9.6|13|9.3|
|M10|66|46|27|19|32|23|26|19|
|M12|110|78|48|33|――――|――――|45|31|
|(M14)|180|130|76|53|――――|――――|73|51|
|M16|270|190|120|82|――――|――――|98|69|
|(M18)|380|260|160|110|――――|――――|140|96|
|M20|530|370|230|160|――――|――――|190|130|
|(M22)|730|510|――――|――――|――――|――――|――――|――――|
|M24|930|650|――――|――――|――――|――――|――――|――――|
|(M27)|1400|960|――――|――――|――――|――――|――――|――――|
|M30|1800|1300|――――|――――|――――|――――|――――|――――|
|M36|3200|2300|――――|――――|――――|――――|――――|――――|
---
# EU DECLARATION OF CONFORMITY

For FANUC robot series (for CE marking: both of the following labels are attached), EU declarations of conformity with the following contents are applied.

# Label for CE marking (on the robot mechanical unit)

INDUSTRIAL ROBOT

工业机器人

AUTHORIZED REPRESENTATIVE IN EU 欧盟授权代表:

FANUC Europe Corporation, S.A.

ZONE INDUSTRIELLE L-6468 ECHTERNACH, GRAND-DUCHE DE LUXEMBOURG

# Label for CE marking (on the robot controller)

ROBOT

WEIGHT CONTROLLER 200 KG

Note: Value of "WEIGHT" and "INPUT VOLTAGE" depend on the robot controller specification.

INPUT VOLTAGE 380 - 500 VAC

# Contents of EU declarations of conformity for Machinery Directive (2006/42/EC)

|Item|Contents|
|---|---|
|Name of the manufacturer|FANUC CORPORATION|
|Address of the manufacturer|3580 Komanba, Shibokusa, Oshino-mura, Minamitsuru-gun, Yamanashi Prefecture, 401-0597 Japan|
|Model|Please refer to "operator's manual" for each robot models. At the beginning of "PREFACE", following information is listed.|
|Designation|Model: "Model name" Designation: "Mechanical unit specification No."|
|Applied standards|EN ISO 10218-1, EN 60204-1|
|Importer/Distributor in EU|FANUC EUROPE CORPORATION, 7, rue Benedikt Zender L-6468 Echternach|
|Date|Date of manufacture (to be written in EC declaration of conformity attached for each robot system)|
---
# CONTACTS

|ADDRESS|PHONE|
|---|---|
|FANUC Corporation Oshino-mura, Yamanashi Prefecture 401-0597, Japan|TEL:81-555-84-5555 FAX:81-555-84-5512|
|FANUC America Corporation. 3900 W. Hamlin Road Rochester Hills, Michigan 48309-3253|TEL:01-248-377-7000 TOLLFREE:01-800-47-ROBOT (76268) FAX: 01-248-276-4133|
|FANUC America Southeast Robotics Southeast Office 13245 Reese Blvd.#140 Campbell Building Huntersville, NC 28078|TEL: 01-704-596-5121|
|FANUC America Midwest Robotics Midwest Office 1800 Lakewood Blvd. Hoffman Estates, IL 60192|TEL:01-847-898-6000 FAX: 01-847- 898-6010|
|Northeast FANUC America Corporation 7700 Innovation Way Mason, OH 45040|TEL:609-737-1445 FAX: 866-741-4550|
|FANUC America West Robotics 25951 Commercentre Drive Lake Forest, CA 92630|TEL:01-949-59 5-2700 FAX:01-949-595-2750|
|FANUC Robotics do Brazil, LTDA Rua Matteo Forte, 22- Áqua Branca São Paulo, SP Brasil CEP 05038-160|TEL: 55-11-3619-0599|
|FANUC Robotics Canada, Ltd. 6774 Financial Drive Mississauga, Ontario L5N 7J6|TEL: 01-905-812-2300 TOLLFREE:01-800-47-ROBOT|
|FANUC Robotique du Canada, Ltee. Succursale du Quebec 1096 Rue Levis, Suite #6 Lachenaie, Quebec J6W 4L1|TEL: (450) 492-9001 TOLLFREE:01-800-47-ROBOT|
|FANUC Robotics Mexico, S.A. de C.V. Circuito Aguascalientes Norte 136 Parque Industrial del Valle de Aguascalientes 20355 Aguascalientes, Ags. Mexico|TEL:52-449-922-8000 TOLLFREE:01-800-47-ROBOT|
|FANUC Europe Corporation 7, rue Benedikt Zender L-6468 Echternach|TEL:352-7277771 FAX:352-727777403|
|FANUC Deutschland GmbH Bernhauser Straße 36, D-73765 Neuhausen, a.d.F., Germany|TEL: 49 7158 9873 0 FAX:49 7158 98 73–100|
|FANUC France s.à.r.l. 15 rue Léonard de Vinci Lisses F-91027 Evry Cedex, France|TEL:+33 1 6989 7000 FAX:+33 1 6989 7001|
|FANUC UK Limited. Seven Stars Industrial Estate Quinn Close Whitley, Coventry CV3 4LB United Kingdom|TEL:+44 2476 63 9669 FAX:+44 2476 30 4333|
|FANUC ITALIA S.R.L. Viale delle Industrie 1/A I-20020 ARESE (MI), Italy|TEL:+39 02 457 95 1 FAX:+39 02 457 95 250|
|FANUC Iberia S.L. Ronda Can Rabadá, n° 23 PoI.Ind "El Camí Ral", Nave n°1 E-08860 Castelldefels (Barcelona) Spain|TEL:+34 93 664 13 35 FAX:+34 93 665 76 41|
|FANUC Czech s.r.o. U Pekarky 1A/484 CZ-180 00 Praha 8 – Liben, Czech Republic|TEL:+420 234 072 900 FAX:+420 234 072 910|
|FANUC SWITZERLAND GmbH Grenchenstrasse 7 P.O. Box CH-2500 Biel/Bienne 8 Switzerland|TEL: +41 323 666 363 FAX: +41 323 666 364|
|FANUC Benelux BVBA Generaal De Wittelaan 15 B-2800 Mechelen|TEL: +32 15 78 88 10 FAX: +32 15 78 80 01|
|FANUC Hungary Kft. Torbágy utca 20, HU-2045 Törökbálint Hungary|TEL: +36 23 332 007 FAX: +36 23 332 009|
|FANUC Polska Sp.z.o.o.. ul. Tyniecka 12, PL-52-407 Wroclaw Poland|TEL: +48 7177 66 170 FAX: +48 71 77 66 179|
|FANUC Austria GmbH Sonnenstr. 4 A-4653 Eberstalzell|Phone: + (43) 732 77 4900 Fax: + (43) 732 77 4961|
|FANUC Robotics LLC Hayчный проезд, д.19 117246г Москва Росспя|TEL: +7 495 665 0058 FAX: +7 495 22834 04|
---
# APPENDIX

# D. CONTACTS

|ADDRESS|PHONE|
|---|---|
|FANUC Turkey Endustriyel Otomasyon Şerifali Mevkii Barbaros Cd. Tic. Ltd. Şti. Söyleşi Sok. No:23 B Blok TR-34760 Ümraniye Istanbul Turkey|TEL: +90 216 651 1408 FAX: +90 216 489 8988|
|FANUC Nordic AB Hammarbacken 4B, S-19149 Sollentuna Sweden|TEL: +46 8 505 80 700 FAX: +46 8 505 80 700|
|FANUC ADRIA d.o.o. Kidričeva 24B, SI - 3000 Celje, Slovenia|TEL: +386 8 205 64 97 FAX: +386 8 205 64 98|
|SHANGHAI-FANUC Robotics Co., Ltd. No.1500 Fulian Road, Baoshan Area, Shanghai P.R. China. Post Code: 201906|TEL: +86 21 5032 7700 FAX: +86 21 5032 7711|
|KOREA FANUC CORPORATION 101 Wanam-ro, Seongsan-gu, Changwon-si, Gyeongsangnam-do, Korea|TEL: +82 55 278 1200 FAX: +82 55 284 9826|
|FANUC OCEANIA PTY LTD 10 Healey Circuit, Huntingwood, NSW 2148, Australia|TEL: +61 2 8822 4600 FAX: +61 2 8822 4666|
---
NO_CONTENT_HERE
---
# INDEX

|**A**| |
|---|---|
|Angle of Mounting Surface Setting|6|
|AUTOMATIC OPERATION|s‑37|
|AXIS LIMIT SETUP|29|
| | |
|**B**| |
|BASIC SPECIFICATIONS|11|
|CHANGE AXIS LIMIT BY DCS|29|
|CHECK POINTS|36|
|Check the Mechanical Unit Connectors|37|
|CHECKS AND MAINTENANCE|33|
|COMMISSIONING AND FUNCTIONAL TESTING|s‑34|
|CONFIGURATION OF ROBOT SYSTEM|s‑3|
|Confirmation of Oil Seepage|36|
|CONNECTION WITH THE CONTROLLER|9|
|CONTACTS|68|
|CONTROL UNIT|s‑39|
| | |
|**C**| |
|MECHANICAL UNIT|s‑39|
|MECHANICAL UNIT EXTERNAL DIMENSIONS AND OPERATING SPACE|14|
|MODE SELECT SWITCH|s‑26|
|MOUNTING BOLT TORQUE LIST|66|
| | |
|**D**| |
|Daily Checks|33|
|DAILY MAINTENANCE|s‑39|
|DEFINITION OF WARNING AND CAUTION|s‑2|
|DEFNITION OF THE USER|s‑4|
|Designation of the Restricted Space and Restriction of User|s‑34|
|DISMANTLING / SCRAPPING|s‑38|
|During Programming|s‑35|
|PROGRAM VERIFICATION|s‑36|
| | |
|**E**| |
|EMERGENCY STOP|s‑26|
|ENABLING DEVICE (DEADMAN SWITCH)|s‑27|
|END EFFECTOR INSTALLATION TO WRIST|22|
|END EFFECTOR, WORKPIECE AND PERIPHERAL EQUIPMENT|s‑19|
|EQUIPMENT INSTALLATION TO THE ROBOT|22|
|EU DECLARATION OF CONFORMITY|67|
| | |
|**F**| |
|FANUC COLLABORATIVE ROBOT SYSTEM|s‑2|
| | |
|**G**| |
|GENERAL|s‑13|
|GENERAL CAUTIONS|s‑33|
| | |
|**I**| |
|INSTALLATION|s‑33,2|
|INSTALLATION CONDITIONS|8|
|INTERFACE FOR OPTION CABLE|26|
| | |
|**L**| |
|LOAD SETTING|23|
| | |
|**P**| |
|Periodic Check and Maintenance|34|
|PERIODIC MAINTENANCE|33|
|PERIODIC MAINTENANCE TABLE|63|
|PIPING AND WIRING TO THE END EFFECTOR|25|
|PLACEMENT OF EQUIPMENT|s‑14|
|POWER SUPPLY AND PROTECTIVE EARTH CONNECTION|s‑16|
| | |
|**Q**| |
|QUICK MASTERING|44|
|QUICK MASTERING FOR SINGLE AXIS|46|
| | |
|**R**| |
|RELEVANT STANDARDS|s‑12|
|Replacing the Batteries|38|
|RESETTING ALARMS AND PREPARING FOR MASTERING|40|
|Returning to Automatic Operation|s‑35|
|RISK ASSESSMENT FOR J5‑AXIS MOTION RANGE|32|
|ROBOT CONFIGURATION|11|
|ROBOT SYSTEM DESIGN|s‑13|
|Robot System Restart Procedures|s‑34|
|Robot Training|s‑5|
| | |
|**S**| |
|SAFEGUARDS|s‑28|
|Safety and Operational Verification|s‑34|
|SAFETY DEVICES|s‑24|
|Safety Fence|s‑28|
---
# INDEX

- Safety Gate and Plugs .................................................s‑29
- Safety of the Collaborative Worker...............................s‑8
- Safety of the Maintenance Engineer ...........................s‑10
- Safety of the Operator ...................................................s‑8
- Safety of the Programmer .............................................s‑9
- Safety of the working person ........................................s‑6
- SAFETY PRECAUTIONS ...........................................s‑1
- SAVING PROGRAMMED DATA ............................s‑36
- SINGLE AXIS MASTERING .......................................48
- STOP TYPE OF ROBOT............................................s‑24
- STORAGE .....................................................................38
- # THE CHARACTERISTIC OF COLLABORATIVE ROBOT AND LIMITATIONS AND USAGE

- NOTES ....................................................................s‑20
- THE SAFETY SEQUENCE FOR FENCE ENTRY...s‑31
- TRANSPORTATION ......................................................1
- TRANSPORTATION AND INSTALLATION...............1
- TROUBLESHOOTING .........................................s‑36,54
- VERIFYING MASTERING ..........................................53
- WARNING & CAUTION LABEL.............................s‑38
- WRIST LOAD CONDITIONS ......................................21
- ZERO POINT POSITION AND MOTION LIMIT .......16
- ZERO POSITION MASTERING ..................................41
---
# REVISION RECORD

|Edition|Date|Contents|
|---|---|---|
|01|June, 2020|r‑1|
---
    B-84194EN/01
*  B  -   8  4  1  9  4  E  N  /  0  1  *