package pci

import . "puerto"
import . "interrupción"
import . "consola"
import . "controlador/controlador"

type Ipcicontroladorhandler interface {
	Algetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor)
}

var ipcicontroladorhandler Ipcicontroladorhandler

type TPredeterminadopcicontroladorhandler struct {
}

func (propio TPredeterminadopcicontroladorhandler) Algetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
}

type TBaseDirecciónregistro struct {
	prefetchcapable	bool
	dirección_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispositivodescriptor struct {
	Puertobase	uint32
	Interrupción	uint32

	bus		uint16
	dispositivo_2	uint16
	función		uint16

	Fabricanteid	uint16
	Dispositivoid	uint16

	claseid		uint8
	subclassid	uint8
	interfazid	uint8

	revision	uint8
}

func (propio *TPeripheralcomponentinterconnectDispositivodescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontrolador struct {
	ipcicontroladorhandler	Ipcicontroladorhandler
	datospuerto		uint16
	ordenpuerto		uint16
}

func (propio *TPeripheralcomponentinterconnectcontrolador) Init(ipcicontroladorhandler Ipcicontroladorhandler) {
	propio.datospuerto = 0xCFC
	propio.ordenpuerto = 0xCF8

	propio.ipcicontroladorhandler = TPredeterminadopcicontroladorhandler{}
	if ipcicontroladorhandler != nil {
		propio.ipcicontroladorhandler = ipcicontroladorhandler
	}
}

var iRecuento int = 0

func (propio *TPeripheralcomponentinterconnectcontrolador) Leer(bus uint16, dispositivo_2 uint16, función uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispositivo_2&0x1f) << 11) | (uint32(función&0x07) << 8) | uint32(registeroffset&0xFC)

	Puertoescribirdword(propio.ordenpuerto, id)

	rESULTADO1 := Puertoleerdword(propio.datospuerto)
	rESULTADO2 := (rESULTADO1 >> (8 * (registeroffset % 4)))

	return rESULTADO2
}

func (propio *TPeripheralcomponentinterconnectcontrolador) Escribir(bus uint16, dispositivo_2 uint16, función uint16, registeroffset uint32, valor uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispositivo_2&0x1f)<<11) | uint32((función&0x07)<<8) | uint32(registeroffset&0xFC)
	Puertoescribirdword(propio.ordenpuerto, id)
	Puertoescribirdword(propio.datospuerto, valor)
}
func (propio *TPeripheralcomponentinterconnectcontrolador) DispositivohasFunciones(bus uint16, dispositivo_2 uint16) bool {
	rESULTADO := propio.Leer(bus, dispositivo_2, 0, 0x0E)
	if (rESULTADO & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var consola TConsola = TConsola{}

func (propio *TPeripheralcomponentinterconnectcontrolador) Seleccionarcontrolador(controladorgestor *TControladorgestor, interrupts *TInterrupcióngestor) {
	for bus := 0; bus < 8; bus++ {
		for dispositivo_2 := 0; dispositivo_2 < 32; dispositivo_2++ {

			var númeroFunciones int = 1
			if propio.DispositivohasFunciones(uint16(bus), uint16(dispositivo_2)) == true {
				númeroFunciones = 8
			} else {
				númeroFunciones = 1
			}

			for función := 0; función < númeroFunciones; función++ {
				var dispositivo TPeripheralcomponentinterconnectDispositivodescriptor
				dispositivo = propio.GetDispositivodescriptor(uint16(bus), uint16(dispositivo_2), uint16(función))
				if dispositivo.Fabricanteid == 0x0000 || dispositivo.Fabricanteid == 0xFFFF {
					continue
				}

				for barraNúmero := 0; barraNúmero < 6; barraNúmero++ {
					var barra TBaseDirecciónregistro = propio.GetbaseDirecciónregistro(uint16(bus), uint16(dispositivo_2), uint16(función), uint16(barraNúmero))
					if barra.dirección_2 != 0 && (barra.regtype == 1) {
						dispositivo.Puertobase = barra.dirección_2
					}

					propio.Getcontrolador(dispositivo, interrupts)

				}

			}

		}
	}
}
func (propio *TPeripheralcomponentinterconnectcontrolador) GetDispositivodescriptor(bus uint16, dispositivo_2 uint16, función uint16) TPeripheralcomponentinterconnectDispositivodescriptor {
	var rESULTADO TPeripheralcomponentinterconnectDispositivodescriptor
	rESULTADO = TPeripheralcomponentinterconnectDispositivodescriptor{}
	rESULTADO.bus = bus
	rESULTADO.dispositivo_2 = dispositivo_2
	rESULTADO.función = función

	rESULTADO.Fabricanteid = uint16(propio.Leer(bus, dispositivo_2, función, 0x00))
	rESULTADO.Dispositivoid = uint16(propio.Leer(bus, dispositivo_2, función, 0x02))

	rESULTADO.claseid = uint8(propio.Leer(bus, dispositivo_2, función, 0x0b))
	rESULTADO.subclassid = uint8(propio.Leer(bus, dispositivo_2, función, 0x0a))
	rESULTADO.interfazid = uint8(propio.Leer(bus, dispositivo_2, función, 0x09))

	rESULTADO.revision = uint8(propio.Leer(bus, dispositivo_2, función, 0x08))
	rESULTADO.Interrupción = uint32(propio.Leer(bus, dispositivo_2, función, 0x3C))

	return rESULTADO
}
func (propio *TPeripheralcomponentinterconnectcontrolador) GetbaseDirecciónregistro(bus uint16, dispositivo_2 uint16, función uint16, barra uint16) TBaseDirecciónregistro {
	var rESULTADO TBaseDirecciónregistro

	headertype := propio.Leer(bus, dispositivo_2, función, 0x0E) & 0x7F
	var máxbars int = int(6 - (4 * headertype))
	if barra >= uint16(máxbars) {
		return rESULTADO
	}

	barraValor := propio.Leer(bus, dispositivo_2, función, uint32(0x10+4*barra))

	if (barraValor & 0x1) != 0 {
		rESULTADO.regtype = 1
	} else {
		rESULTADO.regtype = 0
	}

	if rESULTADO.regtype == 0 {
	} else {
		rESULTADO.dirección_2 = barraValor & ^uint32(0x3)
		rESULTADO.prefetchcapable = false
	}

	return rESULTADO
}
func (propio *TPeripheralcomponentinterconnectcontrolador) Getcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor, interrupts *TInterrupcióngestor) {

	propio.ipcicontroladorhandler.Algetcontrolador(dispositivo)

}
