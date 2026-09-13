package pci

import . "port"
import . "prerušenie"
import . "konzola"
import . "driver/driver"

type IpciRadičhandler interface {
	Zapnutégetdriver(zariadenie TPeripheralcomponentinterconnectZariadeniedescriptor)
}

var ipciRadičhandler IpciRadičhandler

type TPredvolenépciRadičhandler struct {
}

func (vlastný TPredvolenépciRadičhandler) Zapnutégetdriver(zariadenie TPeripheralcomponentinterconnectZariadeniedescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectZariadeniedescriptor struct {
	Portbase	uint32
	Prerušenie	uint32

	bus		uint16
	zariadenie_2	uint16
	funkcia		uint16

	VýrobcaIdentifikátor	uint16
	ZariadenieIdentifikátor	uint16

	triedaIdentifikátor	uint8
	subclassIdentifikátor	uint8
	rozhranieIdentifikátor	uint8

	revision	uint8
}

func (vlastný *TPeripheralcomponentinterconnectZariadeniedescriptor) Init() {
}

type TPeripheralcomponentinterconnectRadič struct {
	ipciRadičhandler	IpciRadičhandler
	dataport		uint16
	príkazport		uint16
}

func (vlastný *TPeripheralcomponentinterconnectRadič) Init(ipciRadičhandler IpciRadičhandler) {
	vlastný.dataport = 0xCFC
	vlastný.príkazport = 0xCF8

	vlastný.ipciRadičhandler = TPredvolenépciRadičhandler{}
	if ipciRadičhandler != nil {
		vlastný.ipciRadičhandler = ipciRadičhandler
	}
}

var icount int = 0

func (vlastný *TPeripheralcomponentinterconnectRadič) Čítanie(bus uint16, zariadenie_2 uint16, funkcia uint16, registeroffset uint32) uint32 {
	var identifikátor uint32 = 0
	identifikátor = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(zariadenie_2&0x1f) << 11) | (uint32(funkcia&0x07) << 8) | uint32(registeroffset&0xFC)

	PortZápisdword(vlastný.príkazport, identifikátor)

	result1 := PortČítaniedword(vlastný.dataport)
	result2 := (result1 >> (8 * (registeroffset % 4)))

	return result2
}

func (vlastný *TPeripheralcomponentinterconnectRadič) Zápis(bus uint16, zariadenie_2 uint16, funkcia uint16, registeroffset uint32, hodnota uint32) {
	var identifikátor uint32
	identifikátor = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((zariadenie_2&0x1f)<<11) | uint32((funkcia&0x07)<<8) | uint32(registeroffset&0xFC)
	PortZápisdword(vlastný.príkazport, identifikátor)
	PortZápisdword(vlastný.dataport, hodnota)
}
func (vlastný *TPeripheralcomponentinterconnectRadič) ZariadeniehasFunkcie(bus uint16, zariadenie_2 uint16) bool {
	result := vlastný.Čítanie(bus, zariadenie_2, 0, 0x0E)
	if (result & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var konzola TKonzola = TKonzola{}

func (vlastný *TPeripheralcomponentinterconnectRadič) Vybraťdriver(drivermanager *TDrivermanager, interrupts *TPrerušeniemanager) {
	for bus := 0; bus < 8; bus++ {
		for zariadenie_2 := 0; zariadenie_2 < 32; zariadenie_2++ {

			var čísloFunkcie int = 1
			if vlastný.ZariadeniehasFunkcie(uint16(bus), uint16(zariadenie_2)) == true {
				čísloFunkcie = 8
			} else {
				čísloFunkcie = 1
			}

			for funkcia := 0; funkcia < čísloFunkcie; funkcia++ {
				var zariadenie TPeripheralcomponentinterconnectZariadeniedescriptor
				zariadenie = vlastný.GetZariadeniedescriptor(uint16(bus), uint16(zariadenie_2), uint16(funkcia))
				if zariadenie.VýrobcaIdentifikátor == 0x0000 || zariadenie.VýrobcaIdentifikátor == 0xFFFF {
					continue
				}

				for lištaČíslo := 0; lištaČíslo < 6; lištaČíslo++ {
					var lišta TBaseaddressregister = vlastný.Getbaseaddressregister(uint16(bus), uint16(zariadenie_2), uint16(funkcia), uint16(lištaČíslo))
					if lišta.address_2 != 0 && (lišta.regtype == 1) {
						zariadenie.Portbase = lišta.address_2
					}

					vlastný.Getdriver(zariadenie, interrupts)

				}

			}

		}
	}
}
func (vlastný *TPeripheralcomponentinterconnectRadič) GetZariadeniedescriptor(bus uint16, zariadenie_2 uint16, funkcia uint16) TPeripheralcomponentinterconnectZariadeniedescriptor {
	var result TPeripheralcomponentinterconnectZariadeniedescriptor
	result = TPeripheralcomponentinterconnectZariadeniedescriptor{}
	result.bus = bus
	result.zariadenie_2 = zariadenie_2
	result.funkcia = funkcia

	result.VýrobcaIdentifikátor = uint16(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x00))
	result.ZariadenieIdentifikátor = uint16(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x02))

	result.triedaIdentifikátor = uint8(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x0b))
	result.subclassIdentifikátor = uint8(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x0a))
	result.rozhranieIdentifikátor = uint8(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x09))

	result.revision = uint8(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x08))
	result.Prerušenie = uint32(vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x3C))

	return result
}
func (vlastný *TPeripheralcomponentinterconnectRadič) Getbaseaddressregister(bus uint16, zariadenie_2 uint16, funkcia uint16, lišta uint16) TBaseaddressregister {
	var result TBaseaddressregister

	headertype := vlastný.Čítanie(bus, zariadenie_2, funkcia, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if lišta >= uint16(maxbars) {
		return result
	}

	lištaHodnota := vlastný.Čítanie(bus, zariadenie_2, funkcia, uint32(0x10+4*lišta))

	if (lištaHodnota & 0x1) != 0 {
		result.regtype = 1
	} else {
		result.regtype = 0
	}

	if result.regtype == 0 {
	} else {
		result.address_2 = lištaHodnota & ^uint32(0x3)
		result.prefetchcapable = false
	}

	return result
}
func (vlastný *TPeripheralcomponentinterconnectRadič) Getdriver(zariadenie TPeripheralcomponentinterconnectZariadeniedescriptor, interrupts *TPrerušeniemanager) {

	vlastný.ipciRadičhandler.Zapnutégetdriver(zariadenie)

}
