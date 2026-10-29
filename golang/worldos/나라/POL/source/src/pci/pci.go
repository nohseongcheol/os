/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "przerwanie"
import . "konsola"
import . "driver/driver"

type IpciKontrolerhandler interface {
	Włączgetdriver(urządzenie TPeripheralcomponentinterconnectUrządzeniedescriptor)
}

var ipciKontrolerhandler IpciKontrolerhandler

type TDomyślnepciKontrolerhandler struct {
}

func (bieżący TDomyślnepciKontrolerhandler) Włączgetdriver(urządzenie TPeripheralcomponentinterconnectUrządzeniedescriptor) {
}

type TBaseAdresregister struct {
	prefetchcapable	bool
	adres_2		uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectUrządzeniedescriptor struct {
	Portbase	uint32
	Przerwanie	uint32

	bus		uint16
	urządzenie_2	uint16
	funkcja		uint16

	DostawcaIdentyfikator	uint16
	UrządzenieIdentyfikator	uint16

	klasaIdentyfikator	uint8
	subclassIdentyfikator	uint8
	interfejsIdentyfikator	uint8

	revision	uint8
}

func (bieżący *TPeripheralcomponentinterconnectUrządzeniedescriptor) Init() {
}

type TPeripheralcomponentinterconnectKontroler struct {
	ipciKontrolerhandler	IpciKontrolerhandler
	dataport		uint16
	polecenieport		uint16
}

func (bieżący *TPeripheralcomponentinterconnectKontroler) Init(ipciKontrolerhandler IpciKontrolerhandler) {
	bieżący.dataport = 0xCFC
	bieżący.polecenieport = 0xCF8

	bieżący.ipciKontrolerhandler = TDomyślnepciKontrolerhandler{}
	if ipciKontrolerhandler != nil {
		bieżący.ipciKontrolerhandler = ipciKontrolerhandler
	}
}

var iLiczba int = 0

func (bieżący *TPeripheralcomponentinterconnectKontroler) Odczyt(bus uint16, urządzenie_2 uint16, funkcja uint16, registeroffset uint32) uint32 {
	var identyfikator uint32 = 0
	identyfikator = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(urządzenie_2&0x1f) << 11) | (uint32(funkcja&0x07) << 8) | uint32(registeroffset&0xFC)

	PortZapisdword(bieżący.polecenieport, identyfikator)

	wYNIK1 := PortOdczytdword(bieżący.dataport)
	wYNIK2 := (wYNIK1 >> (8 * (registeroffset % 4)))

	return wYNIK2
}

func (bieżący *TPeripheralcomponentinterconnectKontroler) Zapis(bus uint16, urządzenie_2 uint16, funkcja uint16, registeroffset uint32, wartość uint32) {
	var identyfikator uint32
	identyfikator = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((urządzenie_2&0x1f)<<11) | uint32((funkcja&0x07)<<8) | uint32(registeroffset&0xFC)
	PortZapisdword(bieżący.polecenieport, identyfikator)
	PortZapisdword(bieżący.dataport, wartość)
}
func (bieżący *TPeripheralcomponentinterconnectKontroler) UrządzeniehasFunkcje(bus uint16, urządzenie_2 uint16) bool {
	wYNIK := bieżący.Odczyt(bus, urządzenie_2, 0, 0x0E)
	if (wYNIK & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsola TKonsola = TKonsola{}

func (bieżący *TPeripheralcomponentinterconnectKontroler) Zaznaczdriver(drivermanager *TDrivermanager, interrupts *TPrzerwaniemanager) {
	for bus := 0; bus < 8; bus++ {
		for urządzenie_2 := 0; urządzenie_2 < 32; urządzenie_2++ {

			var liczbaFunkcje int = 1
			if bieżący.UrządzeniehasFunkcje(uint16(bus), uint16(urządzenie_2)) == true {
				liczbaFunkcje = 8
			} else {
				liczbaFunkcje = 1
			}

			for funkcja := 0; funkcja < liczbaFunkcje; funkcja++ {
				var urządzenie TPeripheralcomponentinterconnectUrządzeniedescriptor
				urządzenie = bieżący.GetUrządzeniedescriptor(uint16(bus), uint16(urządzenie_2), uint16(funkcja))
				if urządzenie.DostawcaIdentyfikator == 0x0000 || urządzenie.DostawcaIdentyfikator == 0xFFFF {
					continue
				}

				for pasekLiczba := 0; pasekLiczba < 6; pasekLiczba++ {
					var pasek TBaseAdresregister = bieżący.GetbaseAdresregister(uint16(bus), uint16(urządzenie_2), uint16(funkcja), uint16(pasekLiczba))
					if pasek.adres_2 != 0 && (pasek.regtype == 1) {
						urządzenie.Portbase = pasek.adres_2
					}

					bieżący.Getdriver(urządzenie, interrupts)

				}

			}

		}
	}
}
func (bieżący *TPeripheralcomponentinterconnectKontroler) GetUrządzeniedescriptor(bus uint16, urządzenie_2 uint16, funkcja uint16) TPeripheralcomponentinterconnectUrządzeniedescriptor {
	var wYNIK TPeripheralcomponentinterconnectUrządzeniedescriptor
	wYNIK = TPeripheralcomponentinterconnectUrządzeniedescriptor{}
	wYNIK.bus = bus
	wYNIK.urządzenie_2 = urządzenie_2
	wYNIK.funkcja = funkcja

	wYNIK.DostawcaIdentyfikator = uint16(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x00))
	wYNIK.UrządzenieIdentyfikator = uint16(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x02))

	wYNIK.klasaIdentyfikator = uint8(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x0b))
	wYNIK.subclassIdentyfikator = uint8(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x0a))
	wYNIK.interfejsIdentyfikator = uint8(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x09))

	wYNIK.revision = uint8(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x08))
	wYNIK.Przerwanie = uint32(bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x3C))

	return wYNIK
}
func (bieżący *TPeripheralcomponentinterconnectKontroler) GetbaseAdresregister(bus uint16, urządzenie_2 uint16, funkcja uint16, pasek uint16) TBaseAdresregister {
	var wYNIK TBaseAdresregister

	headertype := bieżący.Odczyt(bus, urządzenie_2, funkcja, 0x0E) & 0x7F
	var maksymalnabars int = int(6 - (4 * headertype))
	if pasek >= uint16(maksymalnabars) {
		return wYNIK
	}

	pasekWartość := bieżący.Odczyt(bus, urządzenie_2, funkcja, uint32(0x10+4*pasek))

	if (pasekWartość & 0x1) != 0 {
		wYNIK.regtype = 1
	} else {
		wYNIK.regtype = 0
	}

	if wYNIK.regtype == 0 {
	} else {
		wYNIK.adres_2 = pasekWartość & ^uint32(0x3)
		wYNIK.prefetchcapable = false
	}

	return wYNIK
}
func (bieżący *TPeripheralcomponentinterconnectKontroler) Getdriver(urządzenie TPeripheralcomponentinterconnectUrządzeniedescriptor, interrupts *TPrzerwaniemanager) {

	bieżący.ipciKontrolerhandler.Włączgetdriver(urządzenie)

}
