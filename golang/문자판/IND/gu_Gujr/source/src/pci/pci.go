package pci

import . "port"
import . "interrupt"
import . "console"
import . "drivers/driver"

type IPCIControllerHandler interface {
	OnGetDriver(dev TPeripheralComponentInterconnectDeviceDescriptor)
}

var iPCIControllerHandler IPCIControllerHandler

type TDefaultPCIControllerHandler struct {
}

func (self TDefaultPCIControllerHandler) OnGetDriver(dev TPeripheralComponentInterconnectDeviceDescriptor) {
}

type TBaseAddressRegister struct {
	prefetchable	bool
	address	uint32
	regtype		uint8
}
type TPeripheralComponentInterconnectDeviceDescriptor struct {
	PortBase	uint32
	Interrupt	uint32

	bus		uint16
	device		uint16
	function	uint16

	Vendor_id	uint16
	Device_id	uint16

	class_id		uint8
	subclass_id	uint8
	interface_id	uint8

	revision	uint8
}

func (self *TPeripheralComponentInterconnectDeviceDescriptor) Vઆરંભ_કરવો() {
}

type TPeripheralComponentInterconnectController struct {
	iPCIControllerHandler	IPCIControllerHandler
	dataPort		uint16
	commandPort		uint16
}

func (self *TPeripheralComponentInterconnectController) Vઆરંભ_કરવો(iPCIControllerHandler IPCIControllerHandler) {
	self.dataPort = 0xCFC
	self.commandPort = 0xCF8

	self.iPCIControllerHandler = TDefaultPCIControllerHandler{}
	if iPCIControllerHandler != nil {
		self.iPCIControllerHandler = iPCIControllerHandler
	}
}

var iCount int = 0

func (self *TPeripheralComponentInterconnectController) Vવાંચવું(bus uint16, device uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(device&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	PortWriteDword(self.commandPort, id)

	result1 := PortReadDword(self.dataPort)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralComponentInterconnectController) Vલખવું(bus uint16, device uint16, function uint16, registeroffset uint32, value uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((device&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	PortWriteDword(self.commandPort, id)
	PortWriteDword(self.dataPort, value)
}
func (self *TPeripheralComponentInterconnectController) DeviceHasFunctions(bus uint16, device uint16) bool {
	result := self.Vવાંચવું(bus, device, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console T콘솔 = T콘솔{}

func (self *TPeripheralComponentInterconnectController) SelectDrivers(driverManager *TDriverManager, interrupts *TInterruptManager) {
	for bus := 0; bus < 8; bus++ {
		for device := 0; device < 32; device++ {

			var numFunctions int = 1
			if self.DeviceHasFunctions(uint16(bus), uint16(device)) == true {
				numFunctions = 8
			} else {
				numFunctions = 1
			}

			for function := 0; function < numFunctions; function++ {
				var dev TPeripheralComponentInterconnectDeviceDescriptor
				dev = self.GetDeviceDescriptor(uint16(bus), uint16(device), uint16(function))
				if dev.Vendor_id == 0x0000 || dev.Vendor_id == 0xFFFF {
					continue
				}

				for barNum := 0; barNum < 6; barNum++ {
					var bar TBaseAddressRegister = self.GetBaseAddressRegister(uint16(bus), uint16(device), uint16(function), uint16(barNum))
					if bar.address != 0 && (bar.regtype == 1) {
						dev.PortBase = bar.address
					}

					self.GetDriver(dev, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralComponentInterconnectController) GetDeviceDescriptor(bus uint16, device uint16, function uint16) TPeripheralComponentInterconnectDeviceDescriptor {
	var result TPeripheralComponentInterconnectDeviceDescriptor
	result = TPeripheralComponentInterconnectDeviceDescriptor{}
	result.bus = bus
	result.device = device
	result.function = function

	result.Vendor_id = uint16(self.Vવાંચવું(bus, device, function, 0x00))
	result.Device_id = uint16(self.Vવાંચવું(bus, device, function, 0x02))

	result.class_id = uint8(self.Vવાંચવું(bus, device, function, 0x0b))
	result.subclass_id = uint8(self.Vવાંચવું(bus, device, function, 0x0a))
	result.interface_id = uint8(self.Vવાંચવું(bus, device, function, 0x09))

	result.revision = uint8(self.Vવાંચવું(bus, device, function, 0x08))
	result.Interrupt = uint32(self.Vવાંચવું(bus, device, function, 0x3C))

	return result
}
func (self *TPeripheralComponentInterconnectController) GetBaseAddressRegister(bus uint16, device uint16, function uint16, bar uint16) TBaseAddressRegister {
	var result TBaseAddressRegister

	headertype := self.Vવાંચવું(bus, device, function, 0x0E) & 0x7F
	var maxBARs int = int(6 - (4 * headertype))
	if bar >= uint16(maxBARs) {
		return result
	}

	bar_value := self.Vવાંચવું(bus, device, function, uint32(0x10+4*bar))

	if (bar_value & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address = bar_value & ^uint32(0x3)
		result.prefetchable = false
	}

	return result
}
func (self *TPeripheralComponentInterconnectController) GetDriver(dev TPeripheralComponentInterconnectDeviceDescriptor, interrupts *TInterruptManager) {

	self.iPCIControllerHandler.OnGetDriver(dev)

}
