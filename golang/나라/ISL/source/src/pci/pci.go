package pci

import . "port"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Notagetdriver(tæki TPeripheralcomponentinterconnectTækidescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TSjálfgefiðpcicontrollerhandler struct {
}

func (sjálft TSjálfgefiðpcicontrollerhandler) Notagetdriver(tæki TPeripheralcomponentinterconnectTækidescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectTækidescriptor struct {
	Portbase	uint32
	Interrupt	uint32

	bus	uint16
	tæki_2	uint16
	aðgerð	uint16

	FramleiðandiAuðkenni	uint16
	TækiAuðkenni		uint16

	flokkurAuðkenni		uint8
	subclassAuðkenni	uint8
	sKILAuðkenni		uint8

	revision	uint8
}

func (sjálft *TPeripheralcomponentinterconnectTækidescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataport		uint16
	skipunport		uint16
}

func (sjálft *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	sjálft.dataport = 0xCFC
	sjálft.skipunport = 0xCF8

	sjálft.ipcicontrollerhandler = TSjálfgefiðpcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		sjálft.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var icount int = 0

func (sjálft *TPeripheralcomponentinterconnectcontroller) Lestur(bus uint16, tæki_2 uint16, aðgerð uint16, registeroffset uint32) uint32 {
	var auðkenni uint32 = 0
	auðkenni = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(tæki_2&0x1f) << 11) | (uint32(aðgerð&0x07) << 8) | uint32(registeroffset&0xFC)

	PortSkriftdword(sjálft.skipunport, auðkenni)

	nIÐURSTAÐA1 := PortLesturdword(sjálft.dataport)
	nIÐURSTAÐA2 := (nIÐURSTAÐA1 >> (8 * (registeroffset % 4)))

	return nIÐURSTAÐA2
}

func (sjálft *TPeripheralcomponentinterconnectcontroller) Skrift(bus uint16, tæki_2 uint16, aðgerð uint16, registeroffset uint32, gildi uint32) {
	var auðkenni uint32
	auðkenni = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((tæki_2&0x1f)<<11) | uint32((aðgerð&0x07)<<8) | uint32(registeroffset&0xFC)
	PortSkriftdword(sjálft.skipunport, auðkenni)
	PortSkriftdword(sjálft.dataport, gildi)
}
func (sjálft *TPeripheralcomponentinterconnectcontroller) TækihasAðgerðir(bus uint16, tæki_2 uint16) bool {
	nIÐURSTAÐA := sjálft.Lestur(bus, tæki_2, 0, 0x0E)
	if (nIÐURSTAÐA & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (sjálft *TPeripheralcomponentinterconnectcontroller) Veljadriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for tæki_2 := 0; tæki_2 < 32; tæki_2++ {

			var numberAðgerðir int = 1
			if sjálft.TækihasAðgerðir(uint16(bus), uint16(tæki_2)) == true {
				numberAðgerðir = 8
			} else {
				numberAðgerðir = 1
			}

			for aðgerð := 0; aðgerð < numberAðgerðir; aðgerð++ {
				var tæki TPeripheralcomponentinterconnectTækidescriptor
				tæki = sjálft.GetTækidescriptor(uint16(bus), uint16(tæki_2), uint16(aðgerð))
				if tæki.FramleiðandiAuðkenni == 0x0000 || tæki.FramleiðandiAuðkenni == 0xFFFF {
					continue
				}

				for stikanumber := 0; stikanumber < 6; stikanumber++ {
					var stika TBaseaddressregister = sjálft.Getbaseaddressregister(uint16(bus), uint16(tæki_2), uint16(aðgerð), uint16(stikanumber))
					if stika.address_2 != 0 && (stika.regtype == 1) {
						tæki.Portbase = stika.address_2
					}

					sjálft.Getdriver(tæki, interrupts)

				}

			}

		}
	}
}
func (sjálft *TPeripheralcomponentinterconnectcontroller) GetTækidescriptor(bus uint16, tæki_2 uint16, aðgerð uint16) TPeripheralcomponentinterconnectTækidescriptor {
	var nIÐURSTAÐA TPeripheralcomponentinterconnectTækidescriptor
	nIÐURSTAÐA = TPeripheralcomponentinterconnectTækidescriptor{}
	nIÐURSTAÐA.bus = bus
	nIÐURSTAÐA.tæki_2 = tæki_2
	nIÐURSTAÐA.aðgerð = aðgerð

	nIÐURSTAÐA.FramleiðandiAuðkenni = uint16(sjálft.Lestur(bus, tæki_2, aðgerð, 0x00))
	nIÐURSTAÐA.TækiAuðkenni = uint16(sjálft.Lestur(bus, tæki_2, aðgerð, 0x02))

	nIÐURSTAÐA.flokkurAuðkenni = uint8(sjálft.Lestur(bus, tæki_2, aðgerð, 0x0b))
	nIÐURSTAÐA.subclassAuðkenni = uint8(sjálft.Lestur(bus, tæki_2, aðgerð, 0x0a))
	nIÐURSTAÐA.sKILAuðkenni = uint8(sjálft.Lestur(bus, tæki_2, aðgerð, 0x09))

	nIÐURSTAÐA.revision = uint8(sjálft.Lestur(bus, tæki_2, aðgerð, 0x08))
	nIÐURSTAÐA.Interrupt = uint32(sjálft.Lestur(bus, tæki_2, aðgerð, 0x3C))

	return nIÐURSTAÐA
}
func (sjálft *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, tæki_2 uint16, aðgerð uint16, stika uint16) TBaseaddressregister {
	var nIÐURSTAÐA TBaseaddressregister

	headertype := sjálft.Lestur(bus, tæki_2, aðgerð, 0x0E) & 0x7F
	var hámarkbars int = int(6 - (4 * headertype))
	if stika >= uint16(hámarkbars) {
		return nIÐURSTAÐA
	}

	stikaGildi := sjálft.Lestur(bus, tæki_2, aðgerð, uint32(0x10+4*stika))

	if (stikaGildi & 0x1) != 0 {
		nIÐURSTAÐA.regtype = 1
	} else {
		nIÐURSTAÐA.regtype = 0
	}

	if nIÐURSTAÐA.regtype == 0 {
	} else {
		nIÐURSTAÐA.address_2 = stikaGildi & ^uint32(0x3)
		nIÐURSTAÐA.prefetchcapable = false
	}

	return nIÐURSTAÐA
}
func (sjálft *TPeripheralcomponentinterconnectcontroller) Getdriver(tæki TPeripheralcomponentinterconnectTækidescriptor, interrupts *TInterruptmanager) {

	sjálft.ipcicontrollerhandler.Notagetdriver(tæki)

}
