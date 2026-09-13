package pci

import . "qapı"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(avadanlıq TPeripheralcomponentinterconnectAvadanlıqdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TÖnQurğulupcicontrollerhandler struct {
}

func (self TÖnQurğulupcicontrollerhandler) Ongetdriver(avadanlıq TPeripheralcomponentinterconnectAvadanlıqdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectAvadanlıqdescriptor struct {
	Qapıbase	uint32
	Interrupt	uint32

	bus		uint16
	avadanlıq_2	uint16
	function	uint16

	Vendorid	uint16
	Avadanlıqid	uint16

	sinifid		uint8
	subclassid	uint8
	interfaceid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectAvadanlıqdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataQapı		uint16
	əmrQapı			uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataQapı = 0xCFC
	self.əmrQapı = 0xCF8

	self.ipcicontrollerhandler = TÖnQurğulupcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Oxuma(bus uint16, avadanlıq_2 uint16, function uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(avadanlıq_2&0x1f) << 11) | (uint32(function&0x07) << 8) | uint32(registeroffset&0xFC)

	QapıYazmadword(self.əmrQapı, id)

	result1 := QapıOxumadword(self.dataQapı)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Yazma(bus uint16, avadanlıq_2 uint16, function uint16, registeroffset uint32, qiymət uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((avadanlıq_2&0x1f)<<11) | uint32((function&0x07)<<8) | uint32(registeroffset&0xFC)
	QapıYazmadword(self.əmrQapı, id)
	QapıYazmadword(self.dataQapı, qiymət)
}
func (self *TPeripheralcomponentinterconnectcontroller) Avadanlıqhasfunctions(bus uint16, avadanlıq_2 uint16) bool {
	result := self.Oxuma(bus, avadanlıq_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for avadanlıq_2 := 0; avadanlıq_2 < 32; avadanlıq_2++ {

			var numberfunctions int = 1
			if self.Avadanlıqhasfunctions(uint16(bus), uint16(avadanlıq_2)) == true {
				numberfunctions = 8
			} else {
				numberfunctions = 1
			}

			for function := 0; function < numberfunctions; function++ {
				var avadanlıq TPeripheralcomponentinterconnectAvadanlıqdescriptor
				avadanlıq = self.GetAvadanlıqdescriptor(uint16(bus), uint16(avadanlıq_2), uint16(function))
				if avadanlıq.Vendorid == 0x0000 || avadanlıq.Vendorid == 0xFFFF {
					continue
				}

				for çubuqnumber := 0; çubuqnumber < 6; çubuqnumber++ {
					var çubuq TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(avadanlıq_2), uint16(function), uint16(çubuqnumber))
					if çubuq.address_2 != 0 && (çubuq.regtype == 1) {
						avadanlıq.Qapıbase = çubuq.address_2
					}

					self.Getdriver(avadanlıq, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetAvadanlıqdescriptor(bus uint16, avadanlıq_2 uint16, function uint16) TPeripheralcomponentinterconnectAvadanlıqdescriptor {
	var result TPeripheralcomponentinterconnectAvadanlıqdescriptor
	result = TPeripheralcomponentinterconnectAvadanlıqdescriptor{}
	result.bus = bus
	result.avadanlıq_2 = avadanlıq_2
	result.function = function

	result.Vendorid = uint16(self.Oxuma(bus, avadanlıq_2, function, 0x00))
	result.Avadanlıqid = uint16(self.Oxuma(bus, avadanlıq_2, function, 0x02))

	result.sinifid = uint8(self.Oxuma(bus, avadanlıq_2, function, 0x0b))
	result.subclassid = uint8(self.Oxuma(bus, avadanlıq_2, function, 0x0a))
	result.interfaceid = uint8(self.Oxuma(bus, avadanlıq_2, function, 0x09))

	result.revision = uint8(self.Oxuma(bus, avadanlıq_2, function, 0x08))
	result.Interrupt = uint32(self.Oxuma(bus, avadanlıq_2, function, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, avadanlıq_2 uint16, function uint16, çubuq uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Oxuma(bus, avadanlıq_2, function, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if çubuq >= uint16(maxbars) {
		return result
	}

	çubuqQiymət := self.Oxuma(bus, avadanlıq_2, function, uint32(0x10+4*çubuq))

	if (çubuqQiymət & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = çubuqQiymət & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(avadanlıq TPeripheralcomponentinterconnectAvadanlıqdescriptor, interrupts *TInterruptmanager) {

	self.ipcicontrollerhandler.Ongetdriver(avadanlıq)

}
