package pci

import . "port"
import . "katkestus"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Seesgetdriver(seade TPeripheralcomponentinterconnectSeadedescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TVaikimisipcicontrollerhandler struct {
}

func (ise TVaikimisipcicontrollerhandler) Seesgetdriver(seade TPeripheralcomponentinterconnectSeadedescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectSeadedescriptor struct {
	Portbase	uint32
	Katkestus	uint32

	bus		uint16
	seade_2		uint16
	funktsioon	uint16

	Tootjaid	uint16
	Seadeid		uint16

	klassid		uint8
	subclassid	uint8
	lIIDESid	uint8

	revision	uint8
}

func (ise *TPeripheralcomponentinterconnectSeadedescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	käskport		uint16
}

func (ise *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	ise.dataport = 0xCFC
	ise.käskport = 0xCF8

	ise.ipcicontrollerhandler = TVaikimisipcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		ise.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (ise *TPeripheralcomponentinterconnectcontroller) Lugemine(bus uint16, seade_2 uint16, funktsioon uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(seade_2&0x1f) << 11) | (uint32(funktsioon&0x07) << 8) | uint32(registeroffset&0xFC)

	PortKirjutaminedword(ise.käskport, id)

	tULEMUS1 := PortLugeminedword(ise.dataport)
	tULEMUS2 := (tULEMUS1 >> (8 * (registeroffset % 4)))

	return tULEMUS2
}

func (ise *TPeripheralcomponentinterconnectcontroller) Kirjutamine(bus uint16, seade_2 uint16, funktsioon uint16, registeroffset uint32, väärtus uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((seade_2&0x1f)<<11) | uint32((funktsioon&0x07)<<8) | uint32(registeroffset&0xFC)
	PortKirjutaminedword(ise.käskport, id)
	PortKirjutaminedword(ise.dataport, väärtus)
}
func (ise *TPeripheralcomponentinterconnectcontroller) SeadehasFunktsioonid(bus uint16, seade_2 uint16) bool {
	tULEMUS := ise.Lugemine(bus, seade_2, 0, 0x0E)
	if (tULEMUS & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (ise *TPeripheralcomponentinterconnectcontroller) Validriver(drivermanager *TDrivermanager, interrupts *TKatkestusmanager) {
	for bus := 0; bus < 8; bus++ {
		for seade_2 := 0; seade_2 < 32; seade_2++ {

			var arvFunktsioonid int = 1
			if ise.SeadehasFunktsioonid(uint16(bus), uint16(seade_2)) == true {
				arvFunktsioonid = 8
			} else {
				arvFunktsioonid = 1
			}

			for funktsioon := 0; funktsioon < arvFunktsioonid; funktsioon++ {
				var seade TPeripheralcomponentinterconnectSeadedescriptor
				seade = ise.GetSeadedescriptor(uint16(bus), uint16(seade_2), uint16(funktsioon))
				if seade.Tootjaid == 0x0000 || seade.Tootjaid == 0xFFFF {
					continue
				}

				for ribaArv := 0; ribaArv < 6; ribaArv++ {
					var riba TBaseaddressregister = ise.Getbaseaddressregister(uint16(bus), uint16(seade_2), uint16(funktsioon), uint16(ribaArv))
					if riba.address_2 != 0 && (riba.regtype == 1) {
						seade.Portbase = riba.address_2
					}

					ise.Getdriver(seade, interrupts)

				}

			}

		}
	}
}
func (ise *TPeripheralcomponentinterconnectcontroller) GetSeadedescriptor(bus uint16, seade_2 uint16, funktsioon uint16) TPeripheralcomponentinterconnectSeadedescriptor {
	var tULEMUS TPeripheralcomponentinterconnectSeadedescriptor
	tULEMUS = TPeripheralcomponentinterconnectSeadedescriptor{}
	tULEMUS.bus = bus
	tULEMUS.seade_2 = seade_2
	tULEMUS.funktsioon = funktsioon

	tULEMUS.Tootjaid = uint16(ise.Lugemine(bus, seade_2, funktsioon, 0x00))
	tULEMUS.Seadeid = uint16(ise.Lugemine(bus, seade_2, funktsioon, 0x02))

	tULEMUS.klassid = uint8(ise.Lugemine(bus, seade_2, funktsioon, 0x0b))
	tULEMUS.subclassid = uint8(ise.Lugemine(bus, seade_2, funktsioon, 0x0a))
	tULEMUS.lIIDESid = uint8(ise.Lugemine(bus, seade_2, funktsioon, 0x09))

	tULEMUS.revision = uint8(ise.Lugemine(bus, seade_2, funktsioon, 0x08))
	tULEMUS.Katkestus = uint32(ise.Lugemine(bus, seade_2, funktsioon, 0x3C))

	return tULEMUS
}
func (ise *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, seade_2 uint16, funktsioon uint16, riba uint16) TBaseaddressregister {
	var tULEMUS TBaseaddressregister

	headertype := ise.Lugemine(bus, seade_2, funktsioon, 0x0E) & 0x7F
	var suurimbars int = int(6 - (4 * headertype))
	if riba >= uint16(suurimbars) {
		return tULEMUS
	}

	ribaVäärtus := ise.Lugemine(bus, seade_2, funktsioon, uint32(0x10+4*riba))

	if (ribaVäärtus & 0x1) != 0 {
		tULEMUS.regtype = 1
	} else {
		tULEMUS.regtype = 0
	}

	if tULEMUS.regtype == 0 {
	} else {
		tULEMUS.address_2 = ribaVäärtus & ^uint32(0x3)
		tULEMUS.prefetchcapable = false
	}

	return tULEMUS
}
func (ise *TPeripheralcomponentinterconnectcontroller) Getdriver(seade TPeripheralcomponentinterconnectSeadedescriptor, interrupts *TKatkestusmanager) {

	ise.ipcicontrollerhandler.Seesgetdriver(seade)

}
