package pci

import . "anschluss"
import . "unterbrechung"
import . "konsole"
import . "treiber/treiber"

type IpciSteuerunghandler interface {
	BeigetTreiber(gerät TPeripheralcomponentinterconnectGerätdescriptor)
}

var ipciSteuerunghandler IpciSteuerunghandler

type TStandardpciSteuerunghandler struct {
}

func (selbst TStandardpciSteuerunghandler) BeigetTreiber(gerät TPeripheralcomponentinterconnectGerätdescriptor) {
}

type TBaseaddressRegister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectGerätdescriptor struct {
	Anschlussbase	uint32
	Unterbrechung	uint32

	bus		uint16
	gerät_2		uint16
	funktion	uint16

	HerstellerKennung	uint16
	GerätKennung		uint16

	klasseKennung		uint8
	subclassKennung		uint8
	schnittstelleKennung	uint8

	revision	uint8
}

func (selbst *TPeripheralcomponentinterconnectGerätdescriptor) Init() {
}

type TPeripheralcomponentinterconnectSteuerung struct {
	ipciSteuerunghandler	IpciSteuerunghandler
	datenAnschluss		uint16
	befehlAnschluss		uint16
}

func (selbst *TPeripheralcomponentinterconnectSteuerung) Init(ipciSteuerunghandler IpciSteuerunghandler) {
	selbst.datenAnschluss = 0xCFC
	selbst.befehlAnschluss = 0xCF8

	selbst.ipciSteuerunghandler = TStandardpciSteuerunghandler{}
	if ipciSteuerunghandler != nil {
		selbst.ipciSteuerunghandler = ipciSteuerunghandler
	}
}

var iAnzahl int = 0

func (selbst *TPeripheralcomponentinterconnectSteuerung) Lesen(bus uint16, gerät_2 uint16, funktion uint16, registeroffset uint32) uint32 {
	var kennung uint32 = 0
	kennung = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(gerät_2&0x1f) << 11) | (uint32(funktion&0x07) << 8) | uint32(registeroffset&0xFC)

	AnschlussSchreibendword(selbst.befehlAnschluss, kennung)

	ergebnis1 := AnschlussLesendword(selbst.datenAnschluss)
	ergebnis2 := (ergebnis1 >> (8 * (registeroffset % 4)))

	return ergebnis2
}

func (selbst *TPeripheralcomponentinterconnectSteuerung) Schreiben(bus uint16, gerät_2 uint16, funktion uint16, registeroffset uint32, wert uint32) {
	var kennung uint32
	kennung = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((gerät_2&0x1f)<<11) | uint32((funktion&0x07)<<8) | uint32(registeroffset&0xFC)
	AnschlussSchreibendword(selbst.befehlAnschluss, kennung)
	AnschlussSchreibendword(selbst.datenAnschluss, wert)
}
func (selbst *TPeripheralcomponentinterconnectSteuerung) GeräthasFunktionen(bus uint16, gerät_2 uint16) bool {
	ergebnis := selbst.Lesen(bus, gerät_2, 0, 0x0E)
	if (ergebnis & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsole TKonsole = TKonsole{}

func (selbst *TPeripheralcomponentinterconnectSteuerung) AuswählenTreiber(treiberVerwalter *TTreiberVerwalter, interrupts *TUnterbrechungVerwalter) {
	for bus := 0; bus < 8; bus++ {
		for gerät_2 := 0; gerät_2 < 32; gerät_2++ {

			var nummerFunktionen int = 1
			if selbst.GeräthasFunktionen(uint16(bus), uint16(gerät_2)) == true {
				nummerFunktionen = 8
			} else {
				nummerFunktionen = 1
			}

			for funktion := 0; funktion < nummerFunktionen; funktion++ {
				var gerät TPeripheralcomponentinterconnectGerätdescriptor
				gerät = selbst.GetGerätdescriptor(uint16(bus), uint16(gerät_2), uint16(funktion))
				if gerät.HerstellerKennung == 0x0000 || gerät.HerstellerKennung == 0xFFFF {
					continue
				}

				for balkenNummer := 0; balkenNummer < 6; balkenNummer++ {
					var balken TBaseaddressRegister = selbst.GetbaseaddressRegister(uint16(bus), uint16(gerät_2), uint16(funktion), uint16(balkenNummer))
					if balken.address_2 != 0 && (balken.regtype == 1) {
						gerät.Anschlussbase = balken.address_2
					}

					selbst.GetTreiber(gerät, interrupts)

				}

			}

		}
	}
}
func (selbst *TPeripheralcomponentinterconnectSteuerung) GetGerätdescriptor(bus uint16, gerät_2 uint16, funktion uint16) TPeripheralcomponentinterconnectGerätdescriptor {
	var ergebnis TPeripheralcomponentinterconnectGerätdescriptor
	ergebnis = TPeripheralcomponentinterconnectGerätdescriptor{}
	ergebnis.bus = bus
	ergebnis.gerät_2 = gerät_2
	ergebnis.funktion = funktion

	ergebnis.HerstellerKennung = uint16(selbst.Lesen(bus, gerät_2, funktion, 0x00))
	ergebnis.GerätKennung = uint16(selbst.Lesen(bus, gerät_2, funktion, 0x02))

	ergebnis.klasseKennung = uint8(selbst.Lesen(bus, gerät_2, funktion, 0x0b))
	ergebnis.subclassKennung = uint8(selbst.Lesen(bus, gerät_2, funktion, 0x0a))
	ergebnis.schnittstelleKennung = uint8(selbst.Lesen(bus, gerät_2, funktion, 0x09))

	ergebnis.revision = uint8(selbst.Lesen(bus, gerät_2, funktion, 0x08))
	ergebnis.Unterbrechung = uint32(selbst.Lesen(bus, gerät_2, funktion, 0x3C))

	return ergebnis
}
func (selbst *TPeripheralcomponentinterconnectSteuerung) GetbaseaddressRegister(bus uint16, gerät_2 uint16, funktion uint16, balken uint16) TBaseaddressRegister {
	var ergebnis TBaseaddressRegister

	headertype := selbst.Lesen(bus, gerät_2, funktion, 0x0E) & 0x7F
	var maximumbars int = int(6 - (4 * headertype))
	if balken >= uint16(maximumbars) {
		return ergebnis
	}

	balkenWert := selbst.Lesen(bus, gerät_2, funktion, uint32(0x10+4*balken))

	if (balkenWert & 0x1) != 0 {
		ergebnis.regtype = 1
	} else {
		ergebnis.regtype = 0
	}

	if ergebnis.regtype == 0 {
	} else {
		ergebnis.address_2 = balkenWert & ^uint32(0x3)
		ergebnis.prefetchcapable = false
	}

	return ergebnis
}
func (selbst *TPeripheralcomponentinterconnectSteuerung) GetTreiber(gerät TPeripheralcomponentinterconnectGerätdescriptor, interrupts *TUnterbrechungVerwalter) {

	selbst.ipciSteuerunghandler.BeigetTreiber(gerät)

}
