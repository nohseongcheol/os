/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pci

import . "port"
import . "interrupció"
import . "consola"
import . "driver/driver"

type IpciControladorhandler interface {
	Engegatgetdriver(dispositiu TPeripheralcomponentinterconnectDispositiudescriptor)
}

var ipciControladorhandler IpciControladorhandler

type TPerdefectepciControladorhandler struct {
}

func (unmateix TPerdefectepciControladorhandler) Engegatgetdriver(dispositiu TPeripheralcomponentinterconnectDispositiudescriptor) {
}

type TBaseAdreçaregister struct {
	prefetchcapable	bool
	adreça_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispositiudescriptor struct {
	Portbase	uint32
	Interrupció	uint32

	bus		uint16
	dispositiu_2	uint16
	funció		uint16

	FabricantIdentificador	uint16
	DispositiuIdentificador	uint16

	classeIdentificador	uint8
	subclassIdentificador	uint8
	interfícieIdentificador	uint8

	revision	uint8
}

func (unmateix *TPeripheralcomponentinterconnectDispositiudescriptor) Init() {
}

type TPeripheralcomponentinterconnectControlador struct {
	ipciControladorhandler	IpciControladorhandler
	dataport		uint16
	ordreport		uint16
}

func (unmateix *TPeripheralcomponentinterconnectControlador) Init(ipciControladorhandler IpciControladorhandler) {
	unmateix.dataport = 0xCFC
	unmateix.ordreport = 0xCF8

	unmateix.ipciControladorhandler = TPerdefectepciControladorhandler{}
	if ipciControladorhandler != nil {
		unmateix.ipciControladorhandler = ipciControladorhandler
	}
}

var iRecompte int = 0

func (unmateix *TPeripheralcomponentinterconnectControlador) Lectura(bus uint16, dispositiu_2 uint16, funció uint16, registeroffset uint32) uint32 {
	var identificador uint32 = 0
	identificador = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispositiu_2&0x1f) << 11) | (uint32(funció&0x07) << 8) | uint32(registeroffset&0xFC)

	PortEscripturadword(unmateix.ordreport, identificador)

	rESULTAT1 := PortLecturadword(unmateix.dataport)
	rESULTAT2 := (rESULTAT1 >> (8 * (registeroffset % 4)))

	return rESULTAT2
}

func (unmateix *TPeripheralcomponentinterconnectControlador) Escriptura(bus uint16, dispositiu_2 uint16, funció uint16, registeroffset uint32, valor uint32) {
	var identificador uint32
	identificador = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispositiu_2&0x1f)<<11) | uint32((funció&0x07)<<8) | uint32(registeroffset&0xFC)
	PortEscripturadword(unmateix.ordreport, identificador)
	PortEscripturadword(unmateix.dataport, valor)
}
func (unmateix *TPeripheralcomponentinterconnectControlador) DispositiuhasFuncions(bus uint16, dispositiu_2 uint16) bool {
	rESULTAT := unmateix.Lectura(bus, dispositiu_2, 0, 0x0E)
	if (rESULTAT & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var consola TConsola = TConsola{}

func (unmateix *TPeripheralcomponentinterconnectControlador) Seleccionadriver(drivermanager *TDrivermanager, interrupts *TInterrupciómanager) {
	for bus := 0; bus < 8; bus++ {
		for dispositiu_2 := 0; dispositiu_2 < 32; dispositiu_2++ {

			var nombreFuncions int = 1
			if unmateix.DispositiuhasFuncions(uint16(bus), uint16(dispositiu_2)) == true {
				nombreFuncions = 8
			} else {
				nombreFuncions = 1
			}

			for funció := 0; funció < nombreFuncions; funció++ {
				var dispositiu TPeripheralcomponentinterconnectDispositiudescriptor
				dispositiu = unmateix.GetDispositiudescriptor(uint16(bus), uint16(dispositiu_2), uint16(funció))
				if dispositiu.FabricantIdentificador == 0x0000 || dispositiu.FabricantIdentificador == 0xFFFF {
					continue
				}

				for barraNombre := 0; barraNombre < 6; barraNombre++ {
					var barra TBaseAdreçaregister = unmateix.GetbaseAdreçaregister(uint16(bus), uint16(dispositiu_2), uint16(funció), uint16(barraNombre))
					if barra.adreça_2 != 0 && (barra.regtype == 1) {
						dispositiu.Portbase = barra.adreça_2
					}

					unmateix.Getdriver(dispositiu, interrupts)

				}

			}

		}
	}
}
func (unmateix *TPeripheralcomponentinterconnectControlador) GetDispositiudescriptor(bus uint16, dispositiu_2 uint16, funció uint16) TPeripheralcomponentinterconnectDispositiudescriptor {
	var rESULTAT TPeripheralcomponentinterconnectDispositiudescriptor
	rESULTAT = TPeripheralcomponentinterconnectDispositiudescriptor{}
	rESULTAT.bus = bus
	rESULTAT.dispositiu_2 = dispositiu_2
	rESULTAT.funció = funció

	rESULTAT.FabricantIdentificador = uint16(unmateix.Lectura(bus, dispositiu_2, funció, 0x00))
	rESULTAT.DispositiuIdentificador = uint16(unmateix.Lectura(bus, dispositiu_2, funció, 0x02))

	rESULTAT.classeIdentificador = uint8(unmateix.Lectura(bus, dispositiu_2, funció, 0x0b))
	rESULTAT.subclassIdentificador = uint8(unmateix.Lectura(bus, dispositiu_2, funció, 0x0a))
	rESULTAT.interfícieIdentificador = uint8(unmateix.Lectura(bus, dispositiu_2, funció, 0x09))

	rESULTAT.revision = uint8(unmateix.Lectura(bus, dispositiu_2, funció, 0x08))
	rESULTAT.Interrupció = uint32(unmateix.Lectura(bus, dispositiu_2, funció, 0x3C))

	return rESULTAT
}
func (unmateix *TPeripheralcomponentinterconnectControlador) GetbaseAdreçaregister(bus uint16, dispositiu_2 uint16, funció uint16, barra uint16) TBaseAdreçaregister {
	var rESULTAT TBaseAdreçaregister

	headertype := unmateix.Lectura(bus, dispositiu_2, funció, 0x0E) & 0x7F
	var màxbars int = int(6 - (4 * headertype))
	if barra >= uint16(màxbars) {
		return rESULTAT
	}

	barraValor := unmateix.Lectura(bus, dispositiu_2, funció, uint32(0x10+4*barra))

	if (barraValor & 0x1) != 0 {
		rESULTAT.regtype = 1
	} else {
		rESULTAT.regtype = 0
	}

	if rESULTAT.regtype == 0 {
	} else {
		rESULTAT.adreça_2 = barraValor & ^uint32(0x3)
		rESULTAT.prefetchcapable = false
	}

	return rESULTAT
}
func (unmateix *TPeripheralcomponentinterconnectControlador) Getdriver(dispositiu TPeripheralcomponentinterconnectDispositiudescriptor, interrupts *TInterrupciómanager) {

	unmateix.ipciControladorhandler.Engegatgetdriver(dispositiu)

}
