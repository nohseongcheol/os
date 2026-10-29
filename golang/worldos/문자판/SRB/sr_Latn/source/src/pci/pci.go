/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "ometanje"
import . "konzola"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Nagetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TPodrazumevanopcicontrollerhandler struct {
}

func (isti TPodrazumevanopcicontrollerhandler) Nagetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUređajdescriptor struct {
	Portbase	uint32
	Ometanje		uint32

	bus		uint16
	uređaj_2	uint16
	funkcija	uint16

	ProizvođačIB	uint16
	UređajIB	uint16

	klasaIB		uint8
	subclassIB	uint8
	uREĐAJIB	uint8

	revision	uint8
}

func (isti *TPeripheralcomponentinterconnectUređajdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPort		uint16
	naredbaPort		uint16
}

func (isti *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	isti.dataPort = 0xCFC
	isti.naredbaPort = 0xCF8

	isti.ipcicontrollerhandler = TPodrazumevanopcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		isti.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (isti *TPeripheralcomponentinterconnectcontroller) Čitanje(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var iB uint32 = 0
	iB = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(uređaj_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	PortPišedword(isti.naredbaPort, iB)

	iSHOD1 := Portčitanjedword(isti.dataPort)
	iSHOD2 := (iSHOD1 >> (8 * (registeroffset % 4)))

	return iSHOD2
}

func (isti *TPeripheralcomponentinterconnectcontroller) Piše(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32, vrednost uint32) {
	var iB uint32
	iB = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((uređaj_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	PortPišedword(isti.naredbaPort, iB)
	PortPišedword(isti.dataPort, vrednost)
}
func (isti *TPeripheralcomponentinterconnectcontroller) UređajHasFunkcije(bus uint16, uređaj_2 uint16) bool {
	iSHOD := isti.Čitanje(bus, uređaj_2, 0, 0x0E)
	if (iSHOD & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konzola TKonzola = TKonzola{}

func (isti *TPeripheralcomponentinterconnectcontroller) Izaberidriver(drivermanager *TDrivermanager, interrupts *TOmetanjemanager) {
	for bus := 0; bus < 8; bus++ {
		for uređaj_2 := 0; uređaj_2 < 32; uređaj_2++ {

			var brojFunkcije int = 1
			if isti.UređajHasFunkcije(uint16(bus), uint16(uređaj_2)) == true {
				brojFunkcije = 8
			} else {
				brojFunkcije = 1
			}

			for funkcija := 0; funkcija < brojFunkcije; funkcija++ {
				var uređaj TPeripheralcomponentinterconnectUređajdescriptor
				uređaj = isti.GetUređajdescriptor(uint16(bus), uint16(uređaj_2), uint16(funkcija))
				if uređaj.ProizvođačIB == 0x0000 || uređaj.ProizvođačIB == 0xFFFF {
					continue
				}

				for barbroj := 0; barbroj < 6; barbroj++ {
					var bar TBaseaddressregister = isti.Getbaseaddressregister(uint16(bus), uint16(uređaj_2), uint16(funkcija), uint16(barbroj))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						uređaj.Portbase = bar.address_2
					}

					isti.Getdriver(uređaj, interrupts)

				}

			}

		}
	}
}
func (isti *TPeripheralcomponentinterconnectcontroller) GetUređajdescriptor(bus uint16, uređaj_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectUređajdescriptor {
	var iSHOD TPeripheralcomponentinterconnectUređajdescriptor
	iSHOD = TPeripheralcomponentinterconnectUređajdescriptor{}
	iSHOD.bus = bus
	iSHOD.uređaj_2 = uređaj_2
	iSHOD.funkcija = funkcija

	iSHOD.ProizvođačIB = uint16(isti.Čitanje(bus, uređaj_2, funkcija, 0x00))
	iSHOD.UređajIB = uint16(isti.Čitanje(bus, uređaj_2, funkcija, 0x02))

	iSHOD.klasaIB = uint8(isti.Čitanje(bus, uređaj_2, funkcija, 0x0b))
	iSHOD.subclassIB = uint8(isti.Čitanje(bus, uređaj_2, funkcija, 0x0a))
	iSHOD.uREĐAJIB = uint8(isti.Čitanje(bus, uređaj_2, funkcija, 0x09))

	iSHOD.revision = uint8(isti.Čitanje(bus, uređaj_2, funkcija, 0x08))
	iSHOD.Ometanje = uint32(isti.Čitanje(bus, uređaj_2, funkcija, 0x3C))

	return iSHOD
}
func (isti *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, uređaj_2 uint16, funkcija uint16, bar uint16) TBaseaddressregister {
	var iSHOD TBaseaddressregister

	headertype := isti.Čitanje(bus, uređaj_2, funkcija, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if bar >= uint16(maksbars) {
		return iSHOD
	}

	barVrednost := isti.Čitanje(bus, uređaj_2, funkcija, uint32(0x10+4*bar))

	if (barVrednost & 0x1) != 0 {
		iSHOD.regtype = 1
	} else {
		iSHOD.regtype = 0
	}

	if iSHOD.regtype == 0 {
	} else {
		iSHOD.address_2 = barVrednost & ^uint32(0x3)
		iSHOD.prefetchcapable = false
	}

	return iSHOD
}
func (isti *TPeripheralcomponentinterconnectcontroller) Getdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor, interrupts *TOmetanjemanager) {

	isti.ipcicontrollerhandler.Nagetdriver(uređaj)

}
