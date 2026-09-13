package pci

import . "порт"
import . "interrupt"
import . "консол"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(төхөөрөмж TPeripheralcomponentinterconnectТөхөөрөмжdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TСтандартpcicontrollerhandler struct {
}

func (self TСтандартpcicontrollerhandler) Ongetdriver(төхөөрөмж TPeripheralcomponentinterconnectТөхөөрөмжdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectТөхөөрөмжdescriptor struct {
	Портbase	uint32
	Interrupt	uint32

	bus		uint16
	төхөөрөмж_2	uint16
	function	uint16

	VendorДугаар	uint16
	ТөхөөрөмжДугаар	uint16

	ангиДугаар	uint8
	subclassДугаар	uint8
	интерфейсДугаар	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectТөхөөрөмжdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataПорт		uint16
	тушаалПорт		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataПорт = 0xCFC
	self.тушаалПорт = 0xCF8

	self.ipcicontrollerhandler = TСтандартpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Унших(bus uint16, төхөөрөмж_2 uint16, function uint16, registeroffset uint32) uint32 {
	var дугаар uint32 = 0
	дугаар = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(төхөөрөмж_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	ПортБичихdword(self.тушаалПорт, дугаар)

	result1 := ПортУншихdword(self.dataПорт)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Бичих(bus uint16, төхөөрөмж_2 uint16, function uint16, registeroffset uint32, утга uint32) {
	var дугаар uint32
	дугаар = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((төхөөрөмж_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	ПортБичихdword(self.тушаалПорт, дугаар)
	ПортБичихdword(self.dataПорт, утга)
}
func (self *TPeripheralcomponentinterconnectcontroller) Төхөөрөмжhasfunctions(bus uint16, төхөөрөмж_2 uint16) bool {
	result := self.Унших(bus, төхөөрөмж_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var консол TКонсол = TКонсол{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(driverЗохицуулагч *TDriverЗохицуулагч, interrupts *TInterruptЗохицуулагч) {
	for bus := 0; bus < 8; bus++ {
		for төхөөрөмж_2 := 0; төхөөрөмж_2 < 32; төхөөрөмж_2++ {

			var numberfunctions int = 1
			if self.Төхөөрөмжhasfunctions(uint16(bus), uint16(төхөөрөмж_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var төхөөрөмж TPeripheralcomponentinterconnectТөхөөрөмжdescriptor
				төхөөрөмж = self.GetТөхөөрөмжdescriptor(uint16(bus), uint16(төхөөрөмж_2), uint16(function))
				if төхөөрөмж.VendorДугаар == 0x0000 || төхөөрөмж.VendorДугаар == 0xFFFF {
					continue
				}

				for багцnumber := 0; багцnumber < 6; багцnumber++ {
					var багц TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(төхөөрөмж_2), uint16(function), uint16(багцnumber))
					if багц.address_2 != 0 && (багц.regtype == 1) {
						төхөөрөмж.Портbase = багц.address_2
					}

					self.Getdriver(төхөөрөмж, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetТөхөөрөмжdescriptor(bus uint16, төхөөрөмж_2 uint16, function uint16) TPeripheralcomponentinterconnectТөхөөрөмжdescriptor {
	var result TPeripheralcomponentinterconnectТөхөөрөмжdescriptor
	result = TPeripheralcomponentinterconnectТөхөөрөмжdescriptor{}
	result.bus = bus
	result.төхөөрөмж_2 = төхөөрөмж_2
	result.function = function

	result.VendorДугаар = uint16(self.Унших(bus, төхөөрөмж_2, function, 0x00))
	result.ТөхөөрөмжДугаар = uint16(self.Унших(bus, төхөөрөмж_2, function, 0x02))

	result.ангиДугаар = uint8(self.Унших(bus, төхөөрөмж_2, function, 0x0b))
	result.subclassДугаар = uint8(self.Унших(bus, төхөөрөмж_2, function, 0x0a))
	result.интерфейсДугаар = uint8(self.Унших(bus, төхөөрөмж_2, function, 0x09))

	result.revision = uint8(self.Унших(bus, төхөөрөмж_2, function, 0x08))
	result.Interrupt = uint32(self.Унших(bus, төхөөрөмж_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, төхөөрөмж_2 uint16, function uint16, багц uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Унших(bus, төхөөрөмж_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if багц >= uint16(maxbars) {
		return result
	}

	багцУтга := self.Унших(bus, төхөөрөмж_2, function, uint32(0x10+4*багц))

	if (багцУтга & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = багцУтга & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(төхөөрөмж TPeripheralcomponentinterconnectТөхөөрөмжdescriptor, interrupts *TInterruptЗохицуулагч) {

	self.ipcicontrollerhandler.Ongetdriver(төхөөрөмж)

}
