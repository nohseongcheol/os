/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "portti"
import . "keskeytys"
import . "konsoli"
import . "driver/driver"

type IpciOhjainhandler interface {
	Päällägetdriver(laite TPeripheralcomponentinterconnectLaitedescriptor)
}

var ipciOhjainhandler IpciOhjainhandler

type TOletuspciOhjainhandler struct {
}

func (itse TOletuspciOhjainhandler) Päällägetdriver(laite TPeripheralcomponentinterconnectLaitedescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectLaitedescriptor struct {
	Porttibase	uint32
	Keskeytys	uint32

	bus	uint16
	laite_2	uint16
	funktio	uint16

	ValmistajaTUNNISTE	uint16
	LaiteTUNNISTE		uint16

	luokkaTUNNISTE		uint8
	subclassTUNNISTE	uint8
	liitäntäTUNNISTE	uint8

	revision	uint8
}

func (itse *TPeripheralcomponentinterconnectLaitedescriptor) Init() {
}

type TPeripheralcomponentinterconnectOhjain struct {
	ipciOhjainhandler	IpciOhjainhandler
	dataPortti		uint16
	komentoPortti		uint16
}

func (itse *TPeripheralcomponentinterconnectOhjain) Init(ipciOhjainhandler IpciOhjainhandler) {
	itse.dataPortti = 0xCFC
	itse.komentoPortti = 0xCF8

	itse.ipciOhjainhandler = TOletuspciOhjainhandler{}
	if ipciOhjainhandler != nil {
		itse.ipciOhjainhandler = ipciOhjainhandler
	}
}

var icount int = 0

func (itse *TPeripheralcomponentinterconnectOhjain) Luku(bus uint16, laite_2 uint16, funktio uint16, registeroffset uint32) uint32 {
	var tUNNISTE uint32 = 0
	tUNNISTE = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(laite_2&0x1f) << 11) | (uint32(funktio&0x07) << 8) | uint32(registeroffset&0xFC)

	PorttiKirjoitusdword(itse.komentoPortti, tUNNISTE)

	tULOS1 := PorttiLukudword(itse.dataPortti)
	tULOS2 := (tULOS1 >> (8 * (registeroffset % 4)))

	return tULOS2
}

func (itse *TPeripheralcomponentinterconnectOhjain) Kirjoitus(bus uint16, laite_2 uint16, funktio uint16, registeroffset uint32, arvo uint32) {
	var tUNNISTE uint32
	tUNNISTE = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((laite_2&0x1f)<<11) | uint32((funktio&0x07)<<8) | uint32(registeroffset&0xFC)
	PorttiKirjoitusdword(itse.komentoPortti, tUNNISTE)
	PorttiKirjoitusdword(itse.dataPortti, arvo)
}
func (itse *TPeripheralcomponentinterconnectOhjain) LaitehasFunktiot(bus uint16, laite_2 uint16) bool {
	tULOS := itse.Luku(bus, laite_2, 0, 0x0E)
	if (tULOS & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konsoli TKonsoli = TKonsoli{}

func (itse *TPeripheralcomponentinterconnectOhjain) Valitsedriver(drivermanager *TDrivermanager, interrupts *TKeskeytysmanager) {
	for bus := 0; bus < 8; bus++ {
		for laite_2 := 0; laite_2 < 32; laite_2++ {

			var numeroFunktiot int = 1
			if itse.LaitehasFunktiot(uint16(bus), uint16(laite_2)) == true {
				numeroFunktiot = 8
			} else {
				numeroFunktiot = 1
			}

			for funktio := 0; funktio < numeroFunktiot; funktio++ {
				var laite TPeripheralcomponentinterconnectLaitedescriptor
				laite = itse.GetLaitedescriptor(uint16(bus), uint16(laite_2), uint16(funktio))
				if laite.ValmistajaTUNNISTE == 0x0000 || laite.ValmistajaTUNNISTE == 0xFFFF {
					continue
				}

				for palkkiNumero := 0; palkkiNumero < 6; palkkiNumero++ {
					var palkki TBaseaddressregister = itse.Getbaseaddressregister(uint16(bus), uint16(laite_2), uint16(funktio), uint16(palkkiNumero))
					if palkki.address_2 != 0 && (palkki.regtype == 1) {
						laite.Porttibase = palkki.address_2
					}

					itse.Getdriver(laite, interrupts)

				}

			}

		}
	}
}
func (itse *TPeripheralcomponentinterconnectOhjain) GetLaitedescriptor(bus uint16, laite_2 uint16, funktio uint16) TPeripheralcomponentinterconnectLaitedescriptor {
	var tULOS TPeripheralcomponentinterconnectLaitedescriptor
	tULOS = TPeripheralcomponentinterconnectLaitedescriptor{}
	tULOS.bus = bus
	tULOS.laite_2 = laite_2
	tULOS.funktio = funktio

	tULOS.ValmistajaTUNNISTE = uint16(itse.Luku(bus, laite_2, funktio, 0x00))
	tULOS.LaiteTUNNISTE = uint16(itse.Luku(bus, laite_2, funktio, 0x02))

	tULOS.luokkaTUNNISTE = uint8(itse.Luku(bus, laite_2, funktio, 0x0b))
	tULOS.subclassTUNNISTE = uint8(itse.Luku(bus, laite_2, funktio, 0x0a))
	tULOS.liitäntäTUNNISTE = uint8(itse.Luku(bus, laite_2, funktio, 0x09))

	tULOS.revision = uint8(itse.Luku(bus, laite_2, funktio, 0x08))
	tULOS.Keskeytys = uint32(itse.Luku(bus, laite_2, funktio, 0x3C))

	return tULOS
}
func (itse *TPeripheralcomponentinterconnectOhjain) Getbaseaddressregister(bus uint16, laite_2 uint16, funktio uint16, palkki uint16) TBaseaddressregister {
	var tULOS TBaseaddressregister

	headertype := itse.Luku(bus, laite_2, funktio, 0x0E) & 0x7F
	var maksimibars int = int(6 - (4 * headertype))
	if palkki >= uint16(maksimibars) {
		return tULOS
	}

	palkkiArvo := itse.Luku(bus, laite_2, funktio, uint32(0x10+4*palkki))

	if (palkkiArvo & 0x1) != 0 {
		tULOS.regtype = 1
	} else {
		tULOS.regtype = 0
	}

	if tULOS.regtype == 0 {
	} else {
		tULOS.address_2 = palkkiArvo & ^uint32(0x3)
		tULOS.prefetchcapable = false
	}

	return tULOS
}
func (itse *TPeripheralcomponentinterconnectOhjain) Getdriver(laite TPeripheralcomponentinterconnectLaitedescriptor, interrupts *TKeskeytysmanager) {

	itse.ipciOhjainhandler.Päällägetdriver(laite)

}
