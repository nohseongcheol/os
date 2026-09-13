package pci

import . "vrata"
import . "prekinitev"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Vključenogetdriver(naprava TPeripheralcomponentinterconnectNapravadescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TPrivzetopcicontrollerhandler struct {
}

func (sam TPrivzetopcicontrollerhandler) Vključenogetdriver(naprava TPeripheralcomponentinterconnectNapravadescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectNapravadescriptor struct {
	Vratabase	uint32
	Prekinitev	uint32

	bus		uint16
	naprava_2	uint16
	funkcija	uint16

	Prodajalecid	uint16
	Napravaid	uint16

	razredid	uint8
	subclassid	uint8
	vMESNIKid	uint8

	revision	uint8
}

func (sam *TPeripheralcomponentinterconnectNapravadescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataVrata		uint16
	ukazVrata		uint16
}

func (sam *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	sam.dataVrata = 0xCFC
	sam.ukazVrata = 0xCF8

	sam.ipcicontrollerhandler = TPrivzetopcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		sam.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (sam *TPeripheralcomponentinterconnectcontroller) Branje(bus uint16, naprava_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(naprava_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	VrataPisanjedword(sam.ukazVrata, id)

	rEZULTAT1 := VrataBranjedword(sam.dataVrata)
	rEZULTAT2 := (rEZULTAT1 >> (8 * (registeroffset % 4)))

	return rEZULTAT2
}

func (sam *TPeripheralcomponentinterconnectcontroller) Pisanje(bus uint16, naprava_2 uint16, funkcija uint16, registeroffset uint32, vrednost uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((naprava_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	VrataPisanjedword(sam.ukazVrata, id)
	VrataPisanjedword(sam.dataVrata, vrednost)
}
func (sam *TPeripheralcomponentinterconnectcontroller) NapravahasFunkcije(bus uint16, naprava_2 uint16) bool {
	rEZULTAT := sam.Branje(bus, naprava_2, 0, 0x0E)
	if (rEZULTAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (sam *TPeripheralcomponentinterconnectcontroller) Selectdriver(drivermanager *TDrivermanager, interrupts *TPrekinitevmanager) {
	for bus := 0; bus < 8; bus++ {
		for naprava_2 := 0; naprava_2 < 32; naprava_2++ {

			var številkaFunkcije int = 1
			if sam.NapravahasFunkcije(uint16(bus), uint16(naprava_2)) == true {
				številkaFunkcije = 8
			} else {
				številkaFunkcije = 1
			}

			for funkcija := 0; funkcija < številkaFunkcije; funkcija++ {
				var naprava TPeripheralcomponentinterconnectNapravadescriptor
				naprava = sam.GetNapravadescriptor(uint16(bus), uint16(naprava_2), uint16(funkcija))
				if naprava.Prodajalecid == 0x0000 || naprava.Prodajalecid == 0xFFFF {
					continue
				}

				for vrsticaŠtevilka := 0; vrsticaŠtevilka < 6; vrsticaŠtevilka++ {
					var vrstica TBaseaddressregister = sam.Getbaseaddressregister(uint16(bus), uint16(naprava_2), uint16(funkcija), uint16(vrsticaŠtevilka))
					if vrstica.address_2 != 0 && (vrstica.regtype == 1) {
						naprava.Vratabase = vrstica.address_2
					}

					sam.Getdriver(naprava, interrupts)

				}

			}

		}
	}
}
func (sam *TPeripheralcomponentinterconnectcontroller) GetNapravadescriptor(bus uint16, naprava_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectNapravadescriptor {
	var rEZULTAT TPeripheralcomponentinterconnectNapravadescriptor
	rEZULTAT = TPeripheralcomponentinterconnectNapravadescriptor{}
	rEZULTAT.bus = bus
	rEZULTAT.naprava_2 = naprava_2
	rEZULTAT.funkcija = funkcija

	rEZULTAT.Prodajalecid = uint16(sam.Branje(bus, naprava_2, funkcija, 0x00))
	rEZULTAT.Napravaid = uint16(sam.Branje(bus, naprava_2, funkcija, 0x02))

	rEZULTAT.razredid = uint8(sam.Branje(bus, naprava_2, funkcija, 0x0b))
	rEZULTAT.subclassid = uint8(sam.Branje(bus, naprava_2, funkcija, 0x0a))
	rEZULTAT.vMESNIKid = uint8(sam.Branje(bus, naprava_2, funkcija, 0x09))

	rEZULTAT.revision = uint8(sam.Branje(bus, naprava_2, funkcija, 0x08))
	rEZULTAT.Prekinitev = uint32(sam.Branje(bus, naprava_2, funkcija, 0x3C))

	return rEZULTAT
}
func (sam *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, naprava_2 uint16, funkcija uint16, vrstica uint16) TBaseaddressregister {
	var rEZULTAT TBaseaddressregister

	headertype := sam.Branje(bus, naprava_2, funkcija, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if vrstica >= uint16(maxbars) {
		return rEZULTAT
	}

	vrsticaVrednost := sam.Branje(bus, naprava_2, funkcija, uint32(0x10+4*vrstica))

	if (vrsticaVrednost & 0x1) != 0 {
		rEZULTAT.regtype = 1
	} else {
		rEZULTAT.regtype = 0
	}

	if rEZULTAT.regtype == 0 {
	} else {
		rEZULTAT.address_2 = vrsticaVrednost & ^uint32(0x3)
		rEZULTAT.prefetchcapable = false
	}

	return rEZULTAT
}
func (sam *TPeripheralcomponentinterconnectcontroller) Getdriver(naprava TPeripheralcomponentinterconnectNapravadescriptor, interrupts *TPrekinitevmanager) {

	sam.ipcicontrollerhandler.Vključenogetdriver(naprava)

}
