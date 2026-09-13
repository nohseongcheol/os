package pci

import . "port"
import . "ማቋረጫ"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Oማብሪያgetdriver(ዲቫይስ TPeripheralcomponentinterconnectዲቫይስdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type Tነባርpcicontrollerhandler struct {
}

func (self Tነባርpcicontrollerhandler) Oማብሪያgetdriver(ዲቫይስ TPeripheralcomponentinterconnectዲቫይስdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectዲቫይስdescriptor struct {
	Portbase	uint32
	Iማቋረጫ		uint32

	bus		uint16
	ዲቫይስ_2		uint16
	function	uint16

	Vሻጭመለያ		uint16
	Dዲቫይስመለያ	uint16

	መደብመለያ		uint8
	subclassመለያ	uint8
	ገጽታመለያ		uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectዲቫይስdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	ትእዛዝport		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataport = 0xCFC
	self.ትእዛዝport = 0xCF8

	self.ipcicontrollerhandler = Tነባርpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Rማንበቢያ(bus uint16, ዲቫይስ_2 uint16, function uint16, registeroffset uint32) uint32 {
	var መለያ_2 uint32 = 0
	መለያ_2 = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(ዲቫይስ_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	Portመጻፊያdword(self.ትእዛዝport, መለያ_2)

	result1 := Portማንበቢያdword(self.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Wመጻፊያ(bus uint16, ዲቫይስ_2 uint16, function uint16, registeroffset uint32, ዋጋ uint32) {
	var መለያ_2 uint32
	መለያ_2 = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((ዲቫይስ_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	Portመጻፊያdword(self.ትእዛዝport, መለያ_2)
	Portመጻፊያdword(self.dataport, ዋጋ)
}
func (self *TPeripheralcomponentinterconnectcontroller) Dዲቫይስhasfunctions(bus uint16, ዲቫይስ_2 uint16) bool {
	result := self.Rማንበቢያ(bus, ዲቫይስ_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Sይምረጡdriver(drivermanager *TDrivermanager, interrupts *Tማቋረጫmanager) {
	for bus := 0; bus < 8; bus++ {
		for ዲቫይስ_2 := 0; ዲቫይስ_2 < 32; ዲቫይስ_2++ {

			var ቁጥርfunctions int = 1
			if self.Dዲቫይስhasfunctions(uint16(bus), uint16(ዲቫይስ_2)) == true {
				ቁጥርfunctions = 8
			} else {
				ቁጥርfunctions = 1
			}

			for function := 0; function < ቁጥርfunctions; function++ {
				var ዲቫይስ TPeripheralcomponentinterconnectዲቫይስdescriptor
				ዲቫይስ = self.Getዲቫይስdescriptor(uint16(bus), uint16(ዲቫይስ_2), uint16(function))
				if ዲቫይስ.Vሻጭመለያ == 0x0000 || ዲቫይስ.Vሻጭመለያ == 0xFFFF {
					continue
				}

				for መደርደሪያቁጥር := 0; መደርደሪያቁጥር < 6; መደርደሪያቁጥር++ {
					var መደርደሪያ TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(ዲቫይስ_2), uint16(function), uint16(መደርደሪያቁጥር))
					if መደርደሪያ.address_2 != 0 && (መደርደሪያ.regtype == 1) {
						ዲቫይስ.Portbase = መደርደሪያ.address_2
					}

					self.Getdriver(ዲቫይስ, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) Getዲቫይስdescriptor(bus uint16, ዲቫይስ_2 uint16, function uint16) TPeripheralcomponentinterconnectዲቫይስdescriptor {
	var result TPeripheralcomponentinterconnectዲቫይስdescriptor
	result = TPeripheralcomponentinterconnectዲቫይስdescriptor{}
	result.bus = bus
	result.ዲቫይስ_2 = ዲቫይስ_2
	result.function = function

	result.Vሻጭመለያ = uint16(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x00))
	result.Dዲቫይስመለያ = uint16(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x02))

	result.መደብመለያ = uint8(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x0b))
	result.subclassመለያ = uint8(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x0a))
	result.ገጽታመለያ = uint8(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x09))

	result.revision = uint8(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x08))
	result.Iማቋረጫ = uint32(self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, ዲቫይስ_2 uint16, function uint16, መደርደሪያ uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Rማንበቢያ(bus, ዲቫይስ_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if መደርደሪያ >= uint16(maxbars) {
		return result
	}

	መደርደሪያዋጋ := self.Rማንበቢያ(bus, ዲቫይስ_2, function, uint32(0x10+4*መደርደሪያ))

	if (መደርደሪያዋጋ & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = መደርደሪያዋጋ & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(ዲቫይስ TPeripheralcomponentinterconnectዲቫይስdescriptor, interrupts *Tማቋረጫmanager) {

	self.ipcicontrollerhandler.Oማብሪያgetdriver(ዲቫይስ)

}
