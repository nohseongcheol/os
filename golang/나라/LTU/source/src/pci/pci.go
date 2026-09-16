/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "prievadas"
import . "pertraukimas"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Įjungtagetdriver(įrenginys TPeripheralcomponentinterconnectĮrenginysdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TNumatytasispcicontrollerhandler struct {
}

func (self TNumatytasispcicontrollerhandler) Įjungtagetdriver(įrenginys TPeripheralcomponentinterconnectĮrenginysdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectĮrenginysdescriptor struct {
	Prievadasbase	uint32
	Pertraukimas	uint32

	bus		uint16
	įrenginys_2	uint16
	funkcija	uint16

	Gamintojasid	uint16
	Įrenginysid	uint16

	klasėid		uint8
	subclassid	uint8
	sĄSAJAid	uint8

	revision	uint8
}

func (self *TPeripheralcomponentinterconnectĮrenginysdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPrievadas		uint16
	komandaPrievadas	uint16
}

func (self *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	self.dataPrievadas = 0xCFC
	self.komandaPrievadas = 0xCF8

	self.ipcicontrollerhandler = TNumatytasispcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		self.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (self *TPeripheralcomponentinterconnectcontroller) Skaitymas(bus uint16, įrenginys_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(įrenginys_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	PrievadasRašymasdword(self.komandaPrievadas, id)

	rEZULTATAS1 := PrievadasSkaitymasdword(self.dataPrievadas)
	rEZULTATAS2 := (rEZULTATAS1 >> (8 * (registeroffset % 4)))

	return rEZULTATAS2
}

func (self *TPeripheralcomponentinterconnectcontroller) Rašymas(bus uint16, įrenginys_2 uint16, funkcija uint16, registeroffset uint32, reikšmė uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((įrenginys_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	PrievadasRašymasdword(self.komandaPrievadas, id)
	PrievadasRašymasdword(self.dataPrievadas, reikšmė)
}
func (self *TPeripheralcomponentinterconnectcontroller) ĮrenginyshasFunkcijos(bus uint16, įrenginys_2 uint16) bool {
	rEZULTATAS := self.Skaitymas(bus, įrenginys_2, 0, 0x0E)
	if (rEZULTATAS & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (self *TPeripheralcomponentinterconnectcontroller) Žymėtidriver(drivermanager *TDrivermanager, interrupts *TPertraukimasmanager) {
	for bus := 0; bus < 8; bus++ {
		for įrenginys_2 := 0; įrenginys_2 < 32; įrenginys_2++ {

			var skaičiusFunkcijos int = 1
			if self.ĮrenginyshasFunkcijos(uint16(bus), uint16(įrenginys_2)) == true {
				skaičiusFunkcijos = 8
			} else {
				skaičiusFunkcijos = 1
			}

			for funkcija := 0; funkcija < skaičiusFunkcijos; funkcija++ {
				var įrenginys TPeripheralcomponentinterconnectĮrenginysdescriptor
				įrenginys = self.GetĮrenginysdescriptor(uint16(bus), uint16(įrenginys_2), uint16(funkcija))
				if įrenginys.Gamintojasid == 0x0000 || įrenginys.Gamintojasid == 0xFFFF {
					continue
				}

				for juostaSkaičius := 0; juostaSkaičius < 6; juostaSkaičius++ {
					var juosta TBaseaddressregister = self.Getbaseaddressregister(uint16(bus), uint16(įrenginys_2), uint16(funkcija), uint16(juostaSkaičius))
					if juosta.address_2 != 0 && (juosta.regtype == 1) {
						įrenginys.Prievadasbase = juosta.address_2
					}

					self.Getdriver(įrenginys, interrupts)

				}

			}

		}
	}
}
func (self *TPeripheralcomponentinterconnectcontroller) GetĮrenginysdescriptor(bus uint16, įrenginys_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectĮrenginysdescriptor {
	var rEZULTATAS TPeripheralcomponentinterconnectĮrenginysdescriptor
	rEZULTATAS = TPeripheralcomponentinterconnectĮrenginysdescriptor{}
	rEZULTATAS.bus = bus
	rEZULTATAS.įrenginys_2 = įrenginys_2
	rEZULTATAS.funkcija = funkcija

	rEZULTATAS.Gamintojasid = uint16(self.Skaitymas(bus, įrenginys_2, funkcija, 0x00))
	rEZULTATAS.Įrenginysid = uint16(self.Skaitymas(bus, įrenginys_2, funkcija, 0x02))

	rEZULTATAS.klasėid = uint8(self.Skaitymas(bus, įrenginys_2, funkcija, 0x0b))
	rEZULTATAS.subclassid = uint8(self.Skaitymas(bus, įrenginys_2, funkcija, 0x0a))
	rEZULTATAS.sĄSAJAid = uint8(self.Skaitymas(bus, įrenginys_2, funkcija, 0x09))

	rEZULTATAS.revision = uint8(self.Skaitymas(bus, įrenginys_2, funkcija, 0x08))
	rEZULTATAS.Pertraukimas = uint32(self.Skaitymas(bus, įrenginys_2, funkcija, 0x3C))

	return rEZULTATAS
}
func (self *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, įrenginys_2 uint16, funkcija uint16, juosta uint16) TBaseaddressregister {
	var rEZULTATAS TBaseaddressregister

	headertype := self.Skaitymas(bus, įrenginys_2, funkcija, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if juosta >= uint16(maksbars) {
		return rEZULTATAS
	}

	juostaReikšmė := self.Skaitymas(bus, įrenginys_2, funkcija, uint32(0x10+4*juosta))

	if (juostaReikšmė & 0x1) != 0 {
		rEZULTATAS.regtype = 1
	} else {
		rEZULTATAS.regtype = 0
	}

	if rEZULTATAS.regtype == 0 {
	} else {
		rEZULTATAS.address_2 = juostaReikšmė & ^uint32(0x3)
		rEZULTATAS.prefetchcapable = false
	}

	return rEZULTATAS
}
func (self *TPeripheralcomponentinterconnectcontroller) Getdriver(įrenginys TPeripheralcomponentinterconnectĮrenginysdescriptor, interrupts *TPertraukimasmanager) {

	self.ipcicontrollerhandler.Įjungtagetdriver(įrenginys)

}
