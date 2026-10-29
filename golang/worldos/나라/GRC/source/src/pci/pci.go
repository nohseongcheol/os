/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "θύρα"
import . "διακοπή"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ενεργήgetdriver(συσκευή TPeripheralcomponentinterconnectΣυσκευήdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TΠροεπιλογήpcicontrollerhandler struct {
}

func (self TΠροεπιλογήpcicontrollerhandler) Ενεργήgetdriver(συσκευή TPeripheralcomponentinterconnectΣυσκευήdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectΣυσκευήdescriptor struct {
	Θύραbase	uint32
	Διακοπή		uint32

	bus		uint16
	συσκευή_2	uint16
	συνάρτηση	uint16

	ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ	uint16
	ΣυσκευήΤΑΥΤΌΤΗΤΑ	uint16

	κλάσηΤΑΥΤΌΤΗΤΑ		uint8
	subclassΤΑΥΤΌΤΗΤΑ	uint8
	δΙΕΠΑΦΗΤΑΥΤΌΤΗΤΑ	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectΣυσκευήdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataΘύρα		uint16
	εντολήΘύρα		uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataΘύρα = 0xCFC
	self.εντολήΘύρα = 0xCF8

	self.ipcicontrollerhandler = TΠροεπιλογήpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Ανάγνωση(bus uint16, συσκευή_2 uint16, συνάρτηση uint16, registeroffset uint32) uint32 {
	var τΑΥΤΌΤΗΤΑ uint32 = 0
	τΑΥΤΌΤΗΤΑ = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(συσκευή_2&0x1f) << 11) | (uint32(συνάρτηση&0x07) << 8) | uint32(registeroffset&0xFC)

	ΘύραΕγγραφήdword(self.εντολήΘύρα, τΑΥΤΌΤΗΤΑ)

	result1 := ΘύραΑνάγνωσηdword(self.dataΘύρα)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (self *TPeripheralcomponentinterconnectcontroller) Εγγραφή(bus uint16, συσκευή_2 uint16, συνάρτηση uint16, registeroffset uint32, τιμή uint32) {
	var τΑΥΤΌΤΗΤΑ uint32
	τΑΥΤΌΤΗΤΑ = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((συσκευή_2&0x1f)<<11) | uint32((συνάρτηση&0x07)<<8) | uint32(registeroffset&0xFC)
	ΘύραΕγγραφήdword(self.εντολήΘύρα, τΑΥΤΌΤΗΤΑ)
	ΘύραΕγγραφήdword(self.dataΘύρα, τιμή)
}
func (self *TPeripheralcomponentinterconnectcontroller) ΣυσκευήhasΣυναρτήσεις(bus uint16, συσκευή_2 uint16) bool {
	result := self.Ανάγνωση(bus, συσκευή_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Επιλογήdriver(drivermanager *TDrivermanager, interrupts *TΔιακοπήmanager) {
	for bus := 0; bus < 8; bus++ {
		for συσκευή_2 := 0; συσκευή_2 < 32; συσκευή_2++ {

			var αριθμόςΣυναρτήσεις int = 1
			if self.ΣυσκευήhasΣυναρτήσεις(uint16(bus), uint16(συσκευή_2)) == true {
				αριθμόςΣυναρτήσεις = 8
			} else {
				αριθμόςΣυναρτήσεις = 1
			}

			for συνάρτηση := 0; συνάρτηση < αριθμόςΣυναρτήσεις; συνάρτηση++ {
				var συσκευή TPeripheralcomponentinterconnectΣυσκευήdescriptor
				συσκευή = self.GetΣυσκευήdescriptor(uint16(bus), uint16(συσκευή_2), uint16(συνάρτηση))
				if συσκευή.ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ == 0x0000 || συσκευή.ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ == 0xFFFF {
					continue
				}

				for μπάραΑριθμός := 0; μπάραΑριθμός < 6; μπάραΑριθμός++ {
					var μπάρα TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(συσκευή_2), uint16(συνάρτηση), uint16(μπάραΑριθμός))
					if μπάρα.address_2 != 0 && (μπάρα.regtype == 1) {
						συσκευή.Θύραbase = μπάρα.address_2
					}

					self.Getdriver(συσκευή, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetΣυσκευήdescriptor(bus uint16, συσκευή_2 uint16, συνάρτηση uint16) TPeripheralcomponentinterconnectΣυσκευήdescriptor {
	var result TPeripheralcomponentinterconnectΣυσκευήdescriptor
	result = TPeripheralcomponentinterconnectΣυσκευήdescriptor{}
	result.bus = bus
	result.συσκευή_2 = συσκευή_2
	result.συνάρτηση = συνάρτηση

	result.ΚατασκευαστήςΤΑΥΤΌΤΗΤΑ = uint16(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x00))
	result.ΣυσκευήΤΑΥΤΌΤΗΤΑ = uint16(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x02))

	result.κλάσηΤΑΥΤΌΤΗΤΑ = uint8(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x0b))
	result.subclassΤΑΥΤΌΤΗΤΑ = uint8(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x0a))
	result.δΙΕΠΑΦΗΤΑΥΤΌΤΗΤΑ = uint8(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x09))

	result.revision = uint8(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x08))
	result.Διακοπή = uint32(self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x3C))

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, συσκευή_2 uint16, συνάρτηση uint16, μπάρα uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, 0x0E) & 0x7F
	var μεγbars int = int(6 - (4 * headertype))
	if μπάρα >= uint16(μεγbars) {
		return result
	}

	μπάραΤιμή := self.Ανάγνωση(bus, συσκευή_2, συνάρτηση, uint32(0x10+4*μπάρα))

	if (μπάραΤιμή & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = μπάραΤιμή & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(συσκευή TPeripheralcomponentinterconnectΣυσκευήdescriptor, interrupts *TΔιακοπήmanager) {

	self.ipcicontrollerhandler.Ενεργήgetdriver(συσκευή)

}
