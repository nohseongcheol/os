package pci

import . "porta"
import . "interrupt"
import . "konsolë"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Ongetdriver(dispozitivi TPeripheralcomponentinterconnectDispozitividescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TEprezgjedhurpcicontrollerhandler struct {
}

func (vetvetja TEprezgjedhurpcicontrollerhandler) Ongetdriver(dispozitivi TPeripheralcomponentinterconnectDispozitividescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispozitividescriptor struct {
	Portabase	uint32
	Interrupt	uint32

	bus		uint16
	dispozitivi_2	uint16
	funksion	uint16

	Vendorid	uint16
	Dispozitiviid	uint16

	klasaid		uint8
	subclassid	uint8
	iNTERFAQJAid	uint8

	revision	uint8
}

func (vetvetja *TPeripheralcomponentinterconnectDispozitividescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPorta		uint16
	urdhërPorta		uint16
}

func (vetvetja *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	vetvetja.dataPorta = 0xCFC
	vetvetja.urdhërPorta = 0xCF8

	vetvetja.ipcicontrollerhandler = TEprezgjedhurpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		vetvetja.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (vetvetja *TPeripheralcomponentinterconnectcontroller) Leximi(bus uint16, dispozitivi_2 uint16, funksion uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispozitivi_2&0x1f) << 11) | (uint32(funksion&0x07) << 8) | uint32(registeroffset&0xFC)

	PortaShkrimidword(vetvetja.urdhërPorta, id)

	result1 := PortaLeximidword(vetvetja.dataPorta)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (vetvetja *TPeripheralcomponentinterconnectcontroller) Shkrimi(bus uint16, dispozitivi_2 uint16, funksion uint16, registeroffset uint32, vlera uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispozitivi_2&0x1f)<<11) | uint32((funksion&0x07)<<8) | uint32(registeroffset&0xFC)
	PortaShkrimidword(vetvetja.urdhërPorta, id)
	PortaShkrimidword(vetvetja.dataPorta, vlera)
}
func (vetvetja *TPeripheralcomponentinterconnectcontroller) DispozitivihasFunksionet(bus uint16, dispozitivi_2 uint16) bool {
	result := vetvetja.Leximi(bus, dispozitivi_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsolë TKonsolë = TKonsolë{}

func (vetvetja *TPeripheralcomponentinterconnectcontroller) Përzgjidhnidriver(driverManazhuesi *TDriverManazhuesi, interrupts *TInterruptManazhuesi) {
	for bus := 0; bus < 8; bus++ {
		for dispozitivi_2 := 0; dispozitivi_2 < 32; dispozitivi_2++ {

			var numberFunksionet int = 1
			if vetvetja.DispozitivihasFunksionet(uint16(bus), uint16(dispozitivi_2)) == true {
				numberFunksionet = 8
			} else {
				numberFunksionet = 1
			}

			for funksion := 0; funksion < numberFunksionet; funksion++ {
				var dispozitivi TPeripheralcomponentinterconnectDispozitividescriptor
				dispozitivi = vetvetja.GetDispozitividescriptor(uint16(bus), uint16(dispozitivi_2), uint16(funksion))
				if dispozitivi.Vendorid == 0x0000 || dispozitivi.Vendorid == 0xFFFF {
					continue
				}

				for shtyllënumber := 0; shtyllënumber < 6; shtyllënumber++ {
					var shtyllë TBaseaddressregister = vetvetja.Getbaseaddressregister(uint16(bus), uint16(dispozitivi_2), uint16(funksion), uint16(shtyllënumber))
					if shtyllë.address_2 != 0 && (shtyllë.regtype == 1) {
						dispozitivi.Portabase = shtyllë.address_2
					}

					vetvetja.Getdriver(dispozitivi, interrupts)

				}

			}

		}
	}
}
func (vetvetja *TPeripheralcomponentinterconnectcontroller) GetDispozitividescriptor(bus uint16, dispozitivi_2 uint16, funksion uint16) TPeripheralcomponentinterconnectDispozitividescriptor {
	var result TPeripheralcomponentinterconnectDispozitividescriptor
	result = TPeripheralcomponentinterconnectDispozitividescriptor{}
	result.bus = bus
	result.dispozitivi_2 = dispozitivi_2
	result.funksion = funksion

	result.Vendorid = uint16(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x00))
	result.Dispozitiviid = uint16(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x02))

	result.klasaid = uint8(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x0b))
	result.subclassid = uint8(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x0a))
	result.iNTERFAQJAid = uint8(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x09))

	result.revision = uint8(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x08))
	result.Interrupt = uint32(vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x3C))

	return result
}
func (vetvetja *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, dispozitivi_2 uint16, funksion uint16, shtyllë uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := vetvetja.Leximi(bus, dispozitivi_2, funksion, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if shtyllë >= uint16(maxbars) {
		return result
	}

	shtyllëVlera := vetvetja.Leximi(bus, dispozitivi_2, funksion, uint32(0x10+4*shtyllë))

	if (shtyllëVlera & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = shtyllëVlera & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (vetvetja *TPeripheralcomponentinterconnectcontroller) Getdriver(dispozitivi TPeripheralcomponentinterconnectDispozitividescriptor, interrupts *TInterruptManazhuesi) {

	vetvetja.ipcicontrollerhandler.Ongetdriver(dispozitivi)

}
