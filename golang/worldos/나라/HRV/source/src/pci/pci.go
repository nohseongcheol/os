/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "prekid"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Uključenogetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TZadanopcicontrollerhandler struct {
}

func (sam TZadanopcicontrollerhandler) Uključenogetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUređajdescriptor struct {
	Portbase	uint32
	Prekid		uint32

	bus		uint16
	uređaj_2	uint16
	funkcija	uint16

	ProdavačIdentifikacija	uint16
	UređajIdentifikacija	uint16

	razredIdentifikacija	uint8
	subclassIdentifikacija	uint8
	sUČELJEIdentifikacija	uint8

	revision	uint8
}

func (sam *TPeripheralcomponentinterconnectUređajdescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	naredbaport		uint16
}

func (sam *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	sam.dataport = 0xCFC
	sam.naredbaport = 0xCF8

	sam.ipcicontrollerhandler = TZadanopcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		sam.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (sam *TPeripheralcomponentinterconnectcontroller) Čitaj(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32) uint32 {
	var identifikacija uint32 = 0
	identifikacija = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(uređaj_2&0x1f) << 11) | (uint32(funkcija&0x07) << 8) | uint32(registeroffset&0xFC)

	PortZapišidword(sam.naredbaport, identifikacija)

	rEZULTAT1 := PortČitajdword(sam.dataport)
	rEZULTAT2 := (rEZULTAT1 >> (8 * (registeroffset % 4)))

	return rEZULTAT2
}

func (sam *TPeripheralcomponentinterconnectcontroller) Zapiši(bus uint16, uređaj_2 uint16, funkcija uint16, registeroffset uint32, vrijednost uint32) {
	var identifikacija uint32
	identifikacija = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((uređaj_2&0x1f)<<11) | uint32((funkcija&0x07)<<8) | uint32(registeroffset&0xFC)
	PortZapišidword(sam.naredbaport, identifikacija)
	PortZapišidword(sam.dataport, vrijednost)
}
func (sam *TPeripheralcomponentinterconnectcontroller) UređajhasFunkcije(bus uint16, uređaj_2 uint16) bool {
	rEZULTAT := sam.Čitaj(bus, uređaj_2, 0, 0x0E)
	if (rEZULTAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (sam *TPeripheralcomponentinterconnectcontroller) Odaberidriver(drivermanager *TDrivermanager, interrupts *TPrekidmanager) {
	for bus := 0; bus < 8; bus++ {
		for uređaj_2 := 0; uređaj_2 < 32; uređaj_2++ {

			var bROJFunkcije int = 1
			if sam.UređajhasFunkcije(uint16(bus), uint16(uređaj_2)) == true {
				bROJFunkcije = 8
			} else {
				bROJFunkcije = 1
			}

			for funkcija := 0; funkcija < bROJFunkcije; funkcija++ {
				var uređaj TPeripheralcomponentinterconnectUređajdescriptor
				uređaj = sam.GetUređajdescriptor(uint16(bus), uint16(uređaj_2), uint16(funkcija))
				if uređaj.ProdavačIdentifikacija == 0x0000 || uređaj.ProdavačIdentifikacija == 0xFFFF {
					continue
				}

				for barBROJ := 0; barBROJ < 6; barBROJ++ {
					var bar TBaseaddressregister = sam.Getbaseaddressregister(uint16(bus), uint16(uređaj_2), uint16(funkcija), uint16(barBROJ))
					if bar.address_2 != 0 && (bar.regtype == 1) {
						uređaj.Portbase = bar.address_2
					}

					sam.Getdriver(uređaj, interrupts)

				}

			}

		}
	}
}
func (sam *TPeripheralcomponentinterconnectcontroller) GetUređajdescriptor(bus uint16, uređaj_2 uint16, funkcija uint16) TPeripheralcomponentinterconnectUređajdescriptor {
	var rEZULTAT TPeripheralcomponentinterconnectUređajdescriptor
	rEZULTAT = TPeripheralcomponentinterconnectUređajdescriptor{}
	rEZULTAT.bus = bus
	rEZULTAT.uređaj_2 = uređaj_2
	rEZULTAT.funkcija = funkcija

	rEZULTAT.ProdavačIdentifikacija = uint16(sam.Čitaj(bus, uređaj_2, funkcija, 0x00))
	rEZULTAT.UređajIdentifikacija = uint16(sam.Čitaj(bus, uređaj_2, funkcija, 0x02))

	rEZULTAT.razredIdentifikacija = uint8(sam.Čitaj(bus, uređaj_2, funkcija, 0x0b))
	rEZULTAT.subclassIdentifikacija = uint8(sam.Čitaj(bus, uređaj_2, funkcija, 0x0a))
	rEZULTAT.sUČELJEIdentifikacija = uint8(sam.Čitaj(bus, uređaj_2, funkcija, 0x09))

	rEZULTAT.revision = uint8(sam.Čitaj(bus, uređaj_2, funkcija, 0x08))
	rEZULTAT.Prekid = uint32(sam.Čitaj(bus, uređaj_2, funkcija, 0x3C))

	return rEZULTAT
}
func (sam *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, uređaj_2 uint16, funkcija uint16, bar uint16) TBaseaddressregister {
	var rEZULTAT TBaseaddressregister

	headertype := sam.Čitaj(bus, uređaj_2, funkcija, 0x0E) & 0x7F
	var maksbars int = int(6 - (4 * headertype))
	if bar >= uint16(maksbars) {
		return rEZULTAT
	}

	barVrijednost := sam.Čitaj(bus, uređaj_2, funkcija, uint32(0x10+4*bar))

	if (barVrijednost & 0x1) != 0 {
		rEZULTAT.regtype = 1
	} else {
		rEZULTAT.regtype = 0
	}

	if rEZULTAT.regtype == 0 {
	} else {
		rEZULTAT.address_2 = barVrijednost & ^uint32(0x3)
		rEZULTAT.prefetchcapable = false
	}

	return rEZULTAT
}
func (sam *TPeripheralcomponentinterconnectcontroller) Getdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor, interrupts *TPrekidmanager) {

	sam.ipcicontrollerhandler.Uključenogetdriver(uređaj)

}
