package pci

import . "porta"
import . "interrupt"
import . "console"
import . "driver/driver"

type Ipcicontrollerhandler interface {
	Accesogetdriver(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor)
}

var ipcicontrollerhandler Ipcicontrollerhandler

type TPredefinitopcicontrollerhandler struct {
}

func (séstesso TPredefinitopcicontrollerhandler) Accesogetdriver(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
}

type TBaseaddressregister struct {
	prefetchcapable	bool
	address_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispositivodescriptor struct {
	Portabase	uint32
	Interrupt	uint32

	bus		uint16
	dispositivo_2	uint16
	funzione	uint16

	Fornitoreid	uint16
	Dispositivoid	uint16

	classeid	uint8
	subclassid	uint8
	interfacciaid	uint8

	revision	uint8
}

func (séstesso *TPeripheralcomponentinterconnectDispositivodescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontroller struct {
	ipcicontrollerhandler	Ipcicontrollerhandler
	dataPorta		uint16
	comandoPorta		uint16
}

func (séstesso *TPeripheralcomponentinterconnectcontroller) Init(ipcicontrollerhandler Ipcicontrollerhandler) {
	séstesso.dataPorta = 0xCFC
	séstesso.comandoPorta = 0xCF8

	séstesso.ipcicontrollerhandler = TPredefinitopcicontrollerhandler{}
	if ipcicontrollerhandler != nil {
		séstesso.ipcicontrollerhandler = ipcicontrollerhandler
	}
}

var iConteggio int = 0

func (séstesso *TPeripheralcomponentinterconnectcontroller) Lettura(bus uint16, dispositivo_2 uint16, funzione uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispositivo_2&0x1f) << 11) | (uint32(funzione&0x07) << 8) | uint32(registeroffset&0xFC)

	PortaScritturadword(séstesso.comandoPorta, id)

	rISULTATO1 := PortaLetturadword(séstesso.dataPorta)
	rISULTATO2 := (rISULTATO1 >> (8 * (registeroffset % 4)))

	return rISULTATO2
}

func (séstesso *TPeripheralcomponentinterconnectcontroller) Scrittura(bus uint16, dispositivo_2 uint16, funzione uint16, registeroffset uint32, valore uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispositivo_2&0x1f)<<11) | uint32((funzione&0x07)<<8) | uint32(registeroffset&0xFC)
	PortaScritturadword(séstesso.comandoPorta, id)
	PortaScritturadword(séstesso.dataPorta, valore)
}
func (séstesso *TPeripheralcomponentinterconnectcontroller) DispositivohasFunzioni(bus uint16, dispositivo_2 uint16) bool {
	rISULTATO := séstesso.Lettura(bus, dispositivo_2, 0, 0x0E)
	if (rISULTATO & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (séstesso *TPeripheralcomponentinterconnectcontroller) Selezionadriver(drivermanager *TDrivermanager, interrupts *TInterruptmanager) {
	for bus := 0; bus < 8; bus++ {
		for dispositivo_2 := 0; dispositivo_2 < 32; dispositivo_2++ {

			var numeroFunzioni int = 1
			if séstesso.DispositivohasFunzioni(uint16(bus), uint16(dispositivo_2)) == true {
				numeroFunzioni = 8
			} else {
				numeroFunzioni = 1
			}

			for funzione := 0; funzione < numeroFunzioni; funzione++ {
				var dispositivo TPeripheralcomponentinterconnectDispositivodescriptor
				dispositivo = séstesso.GetDispositivodescriptor(uint16(bus), uint16(dispositivo_2), uint16(funzione))
				if dispositivo.Fornitoreid == 0x0000 || dispositivo.Fornitoreid == 0xFFFF {
					continue
				}

				for barraNumero := 0; barraNumero < 6; barraNumero++ {
					var barra TBaseaddressregister = séstesso.Getbaseaddressregister(uint16(bus), uint16(dispositivo_2), uint16(funzione), uint16(barraNumero))
					if barra.address_2 != 0 && (barra.regtype == 1) {
						dispositivo.Portabase = barra.address_2
					}

					séstesso.Getdriver(dispositivo, interrupts)

				}

			}

		}
	}
}
func (séstesso *TPeripheralcomponentinterconnectcontroller) GetDispositivodescriptor(bus uint16, dispositivo_2 uint16, funzione uint16) TPeripheralcomponentinterconnectDispositivodescriptor {
	var rISULTATO TPeripheralcomponentinterconnectDispositivodescriptor
	rISULTATO = TPeripheralcomponentinterconnectDispositivodescriptor{}
	rISULTATO.bus = bus
	rISULTATO.dispositivo_2 = dispositivo_2
	rISULTATO.funzione = funzione

	rISULTATO.Fornitoreid = uint16(séstesso.Lettura(bus, dispositivo_2, funzione, 0x00))
	rISULTATO.Dispositivoid = uint16(séstesso.Lettura(bus, dispositivo_2, funzione, 0x02))

	rISULTATO.classeid = uint8(séstesso.Lettura(bus, dispositivo_2, funzione, 0x0b))
	rISULTATO.subclassid = uint8(séstesso.Lettura(bus, dispositivo_2, funzione, 0x0a))
	rISULTATO.interfacciaid = uint8(séstesso.Lettura(bus, dispositivo_2, funzione, 0x09))

	rISULTATO.revision = uint8(séstesso.Lettura(bus, dispositivo_2, funzione, 0x08))
	rISULTATO.Interrupt = uint32(séstesso.Lettura(bus, dispositivo_2, funzione, 0x3C))

	return rISULTATO
}
func (séstesso *TPeripheralcomponentinterconnectcontroller) Getbaseaddressregister(bus uint16, dispositivo_2 uint16, funzione uint16, barra uint16) TBaseaddressregister {
	var rISULTATO TBaseaddressregister

	headertype := séstesso.Lettura(bus, dispositivo_2, funzione, 0x0E) & 0x7F
	var massimabars int = int(6 - (4 * headertype))
	if barra >= uint16(massimabars) {
		return rISULTATO
	}

	barraValore := séstesso.Lettura(bus, dispositivo_2, funzione, uint32(0x10+4*barra))

	if (barraValore & 0x1) != 0 {
		rISULTATO.regtype = 1
	} else {
		rISULTATO.regtype = 0
	}

	if rISULTATO.regtype == 0 {
	} else {
		rISULTATO.address_2 = barraValore & ^uint32(0x3)
		rISULTATO.prefetchcapable = false
	}

	return rISULTATO
}
func (séstesso *TPeripheralcomponentinterconnectcontroller) Getdriver(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor, interrupts *TInterruptmanager) {

	séstesso.ipcicontrollerhandler.Accesogetdriver(dispositivo)

}
