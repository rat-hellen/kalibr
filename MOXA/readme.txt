SecureBoot enabled !!! выключить !!!
драйвер установить (./ для установки из текущего каталога):
sudo ./mxinstall
посмотреть:
dmesg | grep usb
перезагрузить компьютер
найти устройства:
find /sys -name bComPreser
sudo su переход в root (переименовать можно только от root)
переименовать, справа от > должны быть найденные выше пресерверы:
echo 1 > ...
echo 2 > ...
echo 3 > ...
echo 4 > ...
перезагрузить компьютер
проверить:
ll /dev/tty*
================================================================================

        MOXA UPort Series Driver Installation Guide for Linux Kernel 6.x

                          Copyright(C)2012 Moxa Inc.

================================================================================
Date: 02/24/2023

CONTENTS

1. Introduction
2. System Requirements
3. Installation
   3.1 Driver files   
   3.2 Device naming convention
   3.3 Module driver configuration
   3.4 Static driver configuration
   3.5 Verify driver installation
4. COM Preserver function
5. Setserial
6. Troubleshooting

-----------------------------------------------------------------------------
1. Introduction

   The MOXA UPort series driver supports following devices. 

   [2 Port]
    - UPort 1250 : 2 Port RS-232/422/485 USB to Serial Hub
    - UPort 1250I : 2 Port RS-232/422/485 USB to Serial Hub with Isolation

   [4 Port]    
    - UPort 1410 : 4 Port RS-232 USB to Serial Hub
    - UPort 1450 : 4 Port RS-232/422/485 USB to Serial Hub
    - UPort 1450I : 4 Port RS-232/422/485 USB to Serial Hub with Isolation
    
   [8 Port]    
    - UPort 1610-8 : 8 Port RS-232 USB to Serial Hub
    - UPort 1650-8 : 8 Port RS-232/422/485 USB to Serial Hub
    
   [16 Port]    
    - UPort 1610-16 : 16 Port RS-232 USB to Serial Hub
    - UPort 1650-16 : 16 Port RS-232/422/485 USB to Serial Hub

   This driver supports x86 and x64(AMD64/EM64T) hardware platform. In 
   order to maintain compatibility, this version has also been properly 
   tested with several Linux distribution (see version.txt). However, 
   if compatibility problem occurs, please contact Moxa Inc. technical
   support. (support@moxa.com)

   All the drivers are published in form of source code under GNU General 
   Public License in this version. Please refer to GNU General Public 
   License announcement in each source code file for more detail.

   This version of driver can be only installed as Loadable Module (Module 
   driver). Before you install the driver, please refer to installation 
   procedure in the User's Manual.

-----------------------------------------------------------------------------
2. System Requirements

   - Hardware Platform: x86, x64 
   - Kernel Version: 4.x
   - GCC version 3.x 
   - Kernel source

   Additional requirements for Raspbian
   - gcc-4.8.3 or above
   - ncurses-devel-5.9 or above
   - rpi-source (https://github.com/notro/rpi-source/wiki)

-----------------------------------------------------------------------------
3. Installation

   3.1 Driver files   
   3.2 Device naming convention
   3.3 Module driver configuration   
   3.4 Verify driver installation
       
   3.1 Driver files

       The driver file may be obtained from website, under the product page.
       The first step is to copy driver file
       "driv_linux_uport_[VERSION]_[BUILD].tgz" into a user directory.
       e.g. /moxa. Please execute following commands as below.

       # cd /moxa
       # tar xvfz driv_linux_uport_[VERSION]_[BUILD].tgz
       
       You may find all driver files in /moxa/mxuport.   

   3.2 Device naming convention
        
       Dialin and callout port
       -----------------------
       This driver remains traditional serial device properties and only
       dial-in ports will be created. The device name for each serial port is
       /dev/ttyUSBxx which xx is a sequence number maintained by USB subsystem.
       
       For the past UPort drivers, it created device name /dev/ttyMXUSBxx
       due to some limitation of previous kernel. We also preserve these
       traditional names as linkages in /dev. Please read "3.5 Verify driver
       installation" to check these created device names.       

   3.3 Module driver configuration

       3.3.1 Build the MOXA driver
         
          Before using the MOXA driver, you need compile all the source 
          code. This step is only need to be executed once. But you need to 
          re-compile the source code when you modify the source code. 

       	  Find "Makefile" in /moxa/mxuport, then run	
             
             # make install   
           
          The driver files "mxuport.ko" and "mxusbserial.ko" will be properly
          compiled and copied to system directories respectively. 

          Or you can use "mxinstall" in /moxa/mxuport to install Moxa
          software. "mxinstall" is a script that make it easy to install
          driver and then load the driver in one single step.
             
       3.3.2 Load the MOXA driver  
         
          Insert the MOXA driver as following:

	      # modprobe mxuport 

          It will activate the MOXA UPort driver.
	  
       3.3.3 Unload the MOXA driver
        
          Unload the MOXA driver as following:
            
              #rmmod mxuport
              
              #rmmod mxusbserial	  
	
       3.3.4 Uninstall the MOXA driver  
         
          Find "Makefile" in /moxa/mxuport, then run

	      # make remove 

	  It will uninstall the MOXA UPort driver.  
	      
   3.4 Static driver configuration
       
       Note: To use static driver, you must install the linux kernel
             source package.
   
       3.4.1 Copy  file
	  # cd /usr/src/<kernel-source directory>/drivers/usb/serial/
	  # cp /moxa/mxuport/driver/mxuport/mx-uport.* .
	  # cp /moxa/mxuport/driver/mxuport/UPort*.* .
	  # cp /moxa/mxuport/driver/mxusbserial/mxbus.c .
	  # cp /moxa/mxuport/driver/mxusbserial/mxusb-serial.* .
	  
       3.4.2 Modify kernel configuration file.
          Add the following line into configuration file.
          
            /usr/src/<kernel-source directory>/drivers/usb/serial/Kconfig
            ...
            config USB_SERIAL_CONSOLE
            ...
            config USB_SERIAL_GENERIC
            ...
            config MOXA_UPORT_SERIAL        <-- Add these lines.
            tristate "Moxa USB Serial "     <-- 
            config MOXA_UPORT               <-- 
            tristate "Moxa UPort "          <-- 
            depends on MOXA_UPORT_SERIAL    <--
            ...

       3.4.3 Modify the kernel Makefile 
          Add the following line to the last line of Makefile.
            /usr/src/<kernel-source directory>/drviers/usb/serial/Makefile
            ...
            ...
            ...
            obj-$(CONFIG_MOXA_UPORT_SERIAL) += mxusbserial.o <-- Add these lines.
            obj-$(CONFIG_MOXA_UPORT) += mxuport.o            <--         
            mxusbserial-objs :=mxusb-serial.o mxbus.o        <-- 
            mxuport-objs :=mx-uport.o                        <-- 

       3.4.4 Setup kernel configuration
          
          Configure the kernel:

            # cd /usr/src/<kernel-source directory>
            # make menuconfig
            
          You will go into a menu-driven system. Please select [Device Drivers]
          [USB Support], [USB Serial Converter support], enable the 
          [USB Serial Converter support],the [ MOXA USB SERIAL ] and
          [ MOXA UPORT ]drivers with "[*]" by pressing space bar for
          built-in (not "[M]"),then select [Exit] to exit this program and 
          save kernel configurations. 
          
       3.4.5 Rebuild kernel
      	  The following are for Linux kernel rebuilding, for your 
          reference only.
          For appropriate details, please refer to the Linux document.

          a. cd /usr/src/<kernel-source directory>
          b. make 	     
          c. make modules	
          d. make modules_install
          e. make install

   3.5 Verify driver installation
   
       You may refer to /var/log/messages to check the latest status
       log reported by this driver whenever it's activated or type command
       "dmesg" to get driver information include model name and tty name of
       installed UPort.
       dmesg | grep usb > ~/usb.txt

       Following demonstrates the messages when installing UPort 1410.
       
         mxuport 1-4.1:1.0: MOXA UPort 1400 series converter detected
         usb 1-4.1: MOXA UPort 1410 detected
         usb 1-4.1: Device firmware version v1.4.9
         usb 1-4.1: MOXA UPort 1400 series converter now attached to ttyUSB0
         usb 1-4.1: MOXA UPort 1400 series converter now attached to ttyUSB1
         usb 1-4.1: MOXA UPort 1400 series converter now attached to ttyUSB2
         usb 1-4.1: MOXA UPort 1400 series converter now attached to ttyUSB3
         
       Above message indicates /dev/ttyUSB[0~3] are installed successfully.
       UPort driver includes udev rules which will also create symbolic name
       ttyMXUSB[0~3] for legacy application.

-----------------------------------------------------------------------------
4. COM Preserver function

   Linux assigns the tty port number by the sequence of discovery order
   starting from ttyUSB0. However user may be confused what the actual tty
   names are after reordering the UPorts or system reboot.
   
   With Moxa's COM Preserver function, the COM names remain on the UPort device.
   UPort Linux driver uses udev device manager with COM Preserver to restore
   tty symbolic name automatically.

   Following is a demonstration explaining the usage of this function.

   (1) Durint installation, user may choose to enable the COM Preserver function.

      # Do you want to enable COM Preserver function? [y/N]. y

   (2) Assign the preferred prefix tty name, e.g., ttyMyPort.

      # Enter the prefix name of symbolic tty name: [ttyMXUSB] ttyMyPort

   (3) Plug-in UPort devices, e.g., UPort 1250 and UPort 1410. There are 2
       possible order to discovery the UPorts. So the ttyUSB names are all
       listed below.

         1st:                                2nd:
         UPort 1250 +--- ttyUSB0             UPort 1410 +--- ttyUSB0
                    +--- ttyUSB1                        +--- ttyUSB1
                                                        +--- ttyUSB2
         UPort 1410 +--- ttyUSB2                        +--- ttyUSB3
                    +--- ttyUSB3
                    +--- ttyUSB4             UPort 1250 +--- ttyUSB4
                    +--- ttyUSB5                        +--- ttyUSB5

   (4) Manage the COM names to serial ports. UPort driver uses sysfs to manager
       this property. Type following commnad to list all sysfs nodes in system.

         # find /sys -name bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-2/1-2:1.0/ttyUSB0/bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-2/1-2:1.0/ttyUSB1/bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-4/1-4:1.0/ttyUSB2/bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-4/1-4:1.0/ttyUSB3/bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-4/1-4:1.0/ttyUSB4/bComPreserver_com
           /sys/devices/pci0000:00/0000:00:02.1/usb1/1-4/1-4:1.0/ttyUSB5/bComPreserver_com

      #port = '/dev/ttyMXUSB1'
      #port = '/dev/ttyMXUSB2'
      #port = '/dev/ttyMXUSB3'
      #port = '/dev/ttyMXUSB4'

       Store the symbolic name to serial ports that user want to manage with
       COM Preserver. The tty number is unique value from 1 to 255.
       The following command shows the example to assign ttyMyPort11 to ttyUSB0.

         # echo 11 > /sys/devices/pci0000:00/0000:00:02.1/usb1/1-2/1-2:1.0/ttyUSB0/bComPreserver_com

       Check the saved tty number by following command.

         # cat < /sys/devices/pci0000:00/0000:00:02.1/usb1/1-2/1-2:1.0/ttyUSB0/bComPreserver_com | xargs
         11

   (5) The next time user plug-in UPorts, UPort driver will create static
       symbolic name for serial ports.

         1st:                                2nd:
         UPort 1250 +--- ttyMyPort11         UPort 1410 +--- ttyMyPort13
                    +--- ttyMyPort12                    +--- ttyMyPort14
                                                        +--- ttyMyPort15
         UPort 1410 +--- ttyMyPort13                    +--- ttyMyPort16
                    +--- ttyMyPort14
                    +--- ttyMyPort15         UPort 1250 +--- ttyMyPort11
                    +--- ttyMyPort16                    +--- ttyMyPort12

   Note: The tty(COM) names are stored in UPort device. These changes of
         tty numbers will also affect the COM names when user manually
         restore the COM Preserver function in Windows.

-----------------------------------------------------------------------------
5. Setserial

   UPort driver takes advantage of the setserial tool to configure the UPort.
   Most of the setserial features are not supported because they are depended
   on the UART hardware. The supported Setserial parameters are listed as below.
   
   uart        set UART type(16450-->disable FIFO, 16550A-->enable FIFO)   

   port        use for change port interface
               0x3 RS-485 4W
               0x2 RS-422
               0x1 RS-485 2W
               0x0 RS-232               
		
   spd_hi      Use 57.6kb  when the application requests 38.4kb.
   spd_vhi     Use 115.2kb when the application requests 38.4kb.
   spd_shi     Use 230kb   when the application requests 38.4kb.
   spd_warp    Use 460kb   when the application requests 38.4kb.
   spd_normal  Use 38.4kb  when the application requests 38.4kb.

   [Example]	

    i) The following command sets interface of "/dev/ttyMXUSB0" to RS-422.	

       # setserial /dev/ttyMXUSB0 port 0x2
       
    ii) Lookup the serial settings of current port.
    
       # setserial -g /dev/ttyMXUSB0
       
    iii) The following command sets FIFO of "/dev/ttyMXUSB0".
       Disable FIFO:
       # setserial /dev/ttyMXUSB0 uart 16450
       
       Enable FIFO:
       # setserial /dev/ttyMXUSB0 uart 16550A
         	   
-----------------------------------------------------------------------------
6. Troubleshooting 

   1. Compile error
      To build Moxa driver, it needs kernel header files. If you got
      some compile error, please run "rpm -qa | grep kernel" to check 
      whether the kernel-source package is installed properly. If not,
      please get the kernel-source irpm package and run "rpm -ivh <pacakge>"
      to install. You also need to make sure the build tool is ready,
      including make/gcc/lib. Please see Linux relative document to 
      get more information.
   
   2. No such file or directory
      This problem is that device node not make automatically during
      loading driver. It usually happens under previous kernel version such
      as "2.6.0" - "2.6.5". Therefore, just execute the make node script 
      "upmknod" to generate device node.
      
-----------------------------------------------------------------------------

