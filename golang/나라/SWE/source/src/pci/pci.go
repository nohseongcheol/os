package pci

import . "port"
import . "avbrott"
import . "konsol"
import . "driver/driver"

type IpciStyrenhethandler interface {
	Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor)
}

var ipciStyrenhethandler IpciStyrenhethandler

type TStandardpciStyrenhethandler struct {
}

func (själv TStandardpciStyrenhethandler) Pågetdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor) {
}

type TBaseAdressregister struct {
	prefetchcapable	bool
	adress_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectEnhetdescriptor struct {
	Portbase	uint32
	Avbrott		uint32

	bus		uint16
	enhet_2		uint16
	funktion	uint16

	Tillverkareid	uint16
	Enhetid		uint16

	klassid		uint8
	subclassid	uint8
	gränssnittid	uint8

	revision	uint8
}

func (själv *TPeripheralcomponentinterconnectEnhetdescriptor) Init() {
}

type TPeripheralcomponentinterconnectStyrenhet struct {
	ipciStyrenhethandler	IpciStyrenhethandler
	dataport		uint16
	kommandoport		uint16
}

func (själv *TPeripheralcomponentinterconnectStyrenhet) Init(ipciStyrenhethandler IpciStyrenhethandler) {
	själv.dataport = 0xCFC
	själv.kommandoport = 0xCF8

	själv.ipciStyrenhethandler = TStandardpciStyrenhethandler{}
	if ipciStyrenhethandler != nil {
		själv.ipciStyrenhethandler = ipciStyrenhethandler
	}
}

var iAntal int = 0

func (själv *TPeripheralcomponentinterconnectStyrenhet) Läs(bus uint16, enhet_2 uint16, funktion uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(enhet_2&0x1f) << 11) | (uint32(funktion&0x07) << 8) | uint32(registeroffset&0xFC)

	PortSkrivdword(själv.kommandoport, id)

	rESULTAT1 := PortLäsdword(själv.dataport)
	rESULTAT2 := (rESULTAT1 >> (8 * (registeroffset % 4)))

	return rESULTAT2
}

func (själv *TPeripheralcomponentinterconnectStyrenhet) Skriv(bus uint16, enhet_2 uint16, funktion uint16, registeroffset uint32, värde uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((enhet_2&0x1f)<<11) | uint32((funktion&0x07)<<8) | uint32(registeroffset&0xFC)
	PortSkrivdword(själv.kommandoport, id)
	PortSkrivdword(själv.dataport, värde)
}
func (själv *TPeripheralcomponentinterconnectStyrenhet) EnhethasFunktioner(bus uint16, enhet_2 uint16) bool {
	rESULTAT := själv.Läs(bus, enhet_2, 0, 0x0E)
	if (rESULTAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsol TKonsol = TKonsol{}

func (själv *TPeripheralcomponentinterconnectStyrenhet) Väljdriver(drivermanager *TDrivermanager, interrupts *TAvbrottmanager) {
	for bus := 0; bus < 8; bus++ {
		for enhet_2 := 0; enhet_2 < 32; enhet_2++ {

			var nummerFunktioner int = 1
			if själv.EnhethasFunktioner(uint16(bus), uint16(enhet_2)) == true {
				nummerFunktioner = 8
			} else {
				nummerFunktioner = 1
			}

			for funktion := 0; funktion < nummerFunktioner; funktion++ {
				var enhet TPeripheralcomponentinterconnectEnhetdescriptor
				enhet = själv.GetEnhetdescriptor(uint16(bus), uint16(enhet_2), uint16(funktion))
				if enhet.Tillverkareid == 0x0000 || enhet.Tillverkareid == 0xFFFF {
					continue
				}

				for radNummer := 0; radNummer < 6; radNummer++ {
					var rad TBaseAdressregister = själv.GetbaseAdressregister(uint16(bus), uint16(enhet_2), uint16(funktion), uint16(radNummer))
					if rad.adress_2 != 0 && (rad.regtype == 1) {
						enhet.Portbase = rad.adress_2
					}

					själv.Getdriver(enhet, interrupts)

				}

			}

		}
	}
}
func (själv *TPeripheralcomponentinterconnectStyrenhet) GetEnhetdescriptor(bus uint16, enhet_2 uint16, funktion uint16) TPeripheralcomponentinterconnectEnhetdescriptor {
	var rESULTAT TPeripheralcomponentinterconnectEnhetdescriptor
	rESULTAT = TPeripheralcomponentinterconnectEnhetdescriptor{}
	rESULTAT.bus = bus
	rESULTAT.enhet_2 = enhet_2
	rESULTAT.funktion = funktion

	rESULTAT.Tillverkareid = uint16(själv.Läs(bus, enhet_2, funktion, 0x00))
	rESULTAT.Enhetid = uint16(själv.Läs(bus, enhet_2, funktion, 0x02))

	rESULTAT.klassid = uint8(själv.Läs(bus, enhet_2, funktion, 0x0b))
	rESULTAT.subclassid = uint8(själv.Läs(bus, enhet_2, funktion, 0x0a))
	rESULTAT.gränssnittid = uint8(själv.Läs(bus, enhet_2, funktion, 0x09))

	rESULTAT.revision = uint8(själv.Läs(bus, enhet_2, funktion, 0x08))
	rESULTAT.Avbrott = uint32(själv.Läs(bus, enhet_2, funktion, 0x3C))

	return rESULTAT
}
func (själv *TPeripheralcomponentinterconnectStyrenhet) GetbaseAdressregister(bus uint16, enhet_2 uint16, funktion uint16, rad uint16) TBaseAdressregister {
	var rESULTAT TBaseAdressregister

	headertype := själv.Läs(bus, enhet_2, funktion, 0x0E) & 0x7F
	var maximalbars int = int(6 - (4 * headertype))
	if rad >= uint16(maximalbars) {
		return rESULTAT
	}

	radVärde := själv.Läs(bus, enhet_2, funktion, uint32(0x10+4*rad))

	if (radVärde & 0x1) != 0 {
		rESULTAT.regtype = 1
	} else {
		rESULTAT.regtype = 0
	}

	if rESULTAT.regtype == 0 {
	} else {
		rESULTAT.adress_2 = radVärde & ^uint32(0x3)
		rESULTAT.prefetchcapable = false
	}

	return rESULTAT
}
func (själv *TPeripheralcomponentinterconnectStyrenhet) Getdriver(enhet TPeripheralcomponentinterconnectEnhetdescriptor, interrupts *TAvbrottmanager) {

	själv.ipciStyrenhethandler.Pågetdriver(enhet)

}
