package pci

import . "porto"
import . "interrupção"
import . "console"
import . "controlador/controlador"

type Ipcicontroladorhandler interface {
	Aogetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor)
}

var ipcicontroladorhandler Ipcicontroladorhandler

type TPredefiniçãopcicontroladorhandler struct {
}

func (próprio TPredefiniçãopcicontroladorhandler) Aogetcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor) {
}

type TBaseEndereçoregisto struct {
	prefetchcapable	bool
	endereço_2	uint32
	regtype		uint8
}
type TPeripheralcomponentinterconnectDispositivodescriptor struct {
	Portobase	uint32
	Interrupção	uint32

	bus		uint16
	dispositivo_2	uint16
	função		uint16

	Fabricanteid	uint16
	Dispositivoid	uint16

	classeid	uint8
	subclassid	uint8
	interfaceid	uint8

	revision	uint8
}

func (próprio *TPeripheralcomponentinterconnectDispositivodescriptor) Init() {
}

type TPeripheralcomponentinterconnectcontrolador struct {
	ipcicontroladorhandler	Ipcicontroladorhandler
	dadosporto		uint16
	comandoporto		uint16
}

func (próprio *TPeripheralcomponentinterconnectcontrolador) Init(ipcicontroladorhandler Ipcicontroladorhandler) {
	próprio.dadosporto = 0xCFC
	próprio.comandoporto = 0xCF8

	próprio.ipcicontroladorhandler = TPredefiniçãopcicontroladorhandler{}
	if ipcicontroladorhandler != nil {
		próprio.ipcicontroladorhandler = ipcicontroladorhandler
	}
}

var iContar int = 0

func (próprio *TPeripheralcomponentinterconnectcontrolador) Ler(bus uint16, dispositivo_2 uint16, função uint16, registeroffset uint32) uint32 {
	var id uint32 = 0
	id = 0x1<<31 | (uint32(bus&0xFF) << 16) | (uint32(dispositivo_2&0x1f) << 11) | (uint32(função&0x07) << 8) | uint32(registeroffset&0xFC)

	Portoescreverdword(próprio.comandoporto, id)

	destino1 := Portolerdword(próprio.dadosporto)
	destino2 := (destino1 >> (8 * (registeroffset % 4)))

	return destino2
}

func (próprio *TPeripheralcomponentinterconnectcontrolador) Escrever(bus uint16, dispositivo_2 uint16, função uint16, registeroffset uint32, valor uint32) {
	var id uint32
	id = 0x1<<31 | uint32((bus&0xFF)<<16) | uint32((dispositivo_2&0x1f)<<11) | uint32((função&0x07)<<8) | uint32(registeroffset&0xFC)
	Portoescreverdword(próprio.comandoporto, id)
	Portoescreverdword(próprio.dadosporto, valor)
}
func (próprio *TPeripheralcomponentinterconnectcontrolador) DispositivohasFunções(bus uint16, dispositivo_2 uint16) bool {
	destino_3 := próprio.Ler(bus, dispositivo_2, 0, 0x0E)
	if (destino_3 & (1 << 7)) != 0 {
		return true
	} else {
		return false
	}
}

var console TConsole = TConsole{}

func (próprio *TPeripheralcomponentinterconnectcontrolador) Selecionarcontrolador(controladorgestor *TControladorgestor, interrupts *TInterrupçãogestor) {
	for bus := 0; bus < 8; bus++ {
		for dispositivo_2 := 0; dispositivo_2 < 32; dispositivo_2++ {

			var númeroFunções int = 1
			if próprio.DispositivohasFunções(uint16(bus), uint16(dispositivo_2)) == true {
				númeroFunções = 8
			} else {
				númeroFunções = 1
			}

			for função := 0; função < númeroFunções; função++ {
				var dispositivo TPeripheralcomponentinterconnectDispositivodescriptor
				dispositivo = próprio.GetDispositivodescriptor(uint16(bus), uint16(dispositivo_2), uint16(função))
				if dispositivo.Fabricanteid == 0x0000 || dispositivo.Fabricanteid == 0xFFFF {
					continue
				}

				for barraNúmero := 0; barraNúmero < 6; barraNúmero++ {
					var barra TBaseEndereçoregisto = próprio.GetbaseEndereçoregisto(uint16(bus), uint16(dispositivo_2), uint16(função), uint16(barraNúmero))
					if barra.endereço_2 != 0 && (barra.regtype == 1) {
						dispositivo.Portobase = barra.endereço_2
					}

					próprio.Getcontrolador(dispositivo, interrupts)

				}

			}

		}
	}
}
func (próprio *TPeripheralcomponentinterconnectcontrolador) GetDispositivodescriptor(bus uint16, dispositivo_2 uint16, função uint16) TPeripheralcomponentinterconnectDispositivodescriptor {
	var destino_3 TPeripheralcomponentinterconnectDispositivodescriptor
	destino_3 = TPeripheralcomponentinterconnectDispositivodescriptor{}
	destino_3.bus = bus
	destino_3.dispositivo_2 = dispositivo_2
	destino_3.função = função

	destino_3.Fabricanteid = uint16(próprio.Ler(bus, dispositivo_2, função, 0x00))
	destino_3.Dispositivoid = uint16(próprio.Ler(bus, dispositivo_2, função, 0x02))

	destino_3.classeid = uint8(próprio.Ler(bus, dispositivo_2, função, 0x0b))
	destino_3.subclassid = uint8(próprio.Ler(bus, dispositivo_2, função, 0x0a))
	destino_3.interfaceid = uint8(próprio.Ler(bus, dispositivo_2, função, 0x09))

	destino_3.revision = uint8(próprio.Ler(bus, dispositivo_2, função, 0x08))
	destino_3.Interrupção = uint32(próprio.Ler(bus, dispositivo_2, função, 0x3C))

	return destino_3
}
func (próprio *TPeripheralcomponentinterconnectcontrolador) GetbaseEndereçoregisto(bus uint16, dispositivo_2 uint16, função uint16, barra uint16) TBaseEndereçoregisto {
	var destino_3 TBaseEndereçoregisto

	headertype := próprio.Ler(bus, dispositivo_2, função, 0x0E) & 0x7F
	var maxbars int = int(6 - (4 * headertype))
	if barra >= uint16(maxbars) {
		return destino_3
	}

	barraValor := próprio.Ler(bus, dispositivo_2, função, uint32(0x10+4*barra))

	if (barraValor & 0x1) != 0 {
		destino_3.regtype = 1
	} else {
		destino_3.regtype = 0
	}

	if destino_3.regtype == 0 {
	} else {
		destino_3.endereço_2 = barraValor & ^uint32(0x3)
		destino_3.prefetchcapable = false
	}

	return destino_3
}
func (próprio *TPeripheralcomponentinterconnectcontrolador) Getcontrolador(dispositivo TPeripheralcomponentinterconnectDispositivodescriptor, interrupts *TInterrupçãogestor) {

	próprio.ipcicontroladorhandler.Aogetcontrolador(dispositivo)

}
