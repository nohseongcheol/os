package teclado

import . "unsafe"

import . "puerto"
import . "interrupción"
import . "consola"

type IRatóneventohandler interface {
	AlratónAbajo(botón int8)
	AlratónSubir(botón int8)
	AlratónMover(x int8, y int8)
}

var iratóneventohandler IRatóneventohandler

type TPredeterminadoratóneventohandler struct {
}

var consola_2 TConsola = TConsola{}
var previousx int16 = 0
var previousy int16 = 0
var xPosición int16 = 0
var yPosición int16 = 0

func (propio TPredeterminadoratóneventohandler) AlratónAbajo(botón int8) {
	buffer := []byte("+")
	consola_2.MImprimirxy(buffer, uint16(previousx), uint16(previousy))
}
func (propio TPredeterminadoratóneventohandler) AlratónSubir(botón int8)	{}
func (propio TPredeterminadoratóneventohandler) AlratónMover(x int8, y int8) {

	xPosición += int16(x)
	if xPosición < 0 {
		xPosición = 0
	}
	if xPosición >= 80 {
		xPosición = 79
	}

	yPosición -= int16(y)

	if yPosición < 0 {
		yPosición = 0
	}
	if yPosición >= 25 {
		yPosición = 24
	}

	buffer := []byte(" ")
	consola_2.MImprimirxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	consola_2.MImprimirxy(buffer, uint16(xPosición), uint16(yPosición))

	previousx = xPosición
	previousy = yPosición
}

type TRatóncontrolador struct {
	TInterrupciónhandler
}

var activoratóncontrolador *TRatóncontrolador
var interrupciónhandler func(uint32) uint32

var datospuerto_2 uint16 = 0x60
var ordenpuerto_2 uint16 = 0x64

const ps2EsperarLimitar = 100000

func esperarps2EntradaVacío() bool {
	for i := 0; i < ps2EsperarLimitar; i++ {
		if (Puertoleerocteto(ordenpuerto_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func esperarps2SalidaCompleto() bool {
	for i := 0; i < ps2EsperarLimitar; i++ {
		if (Puertoleerocteto(ordenpuerto_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func escribirps2Orden(valor uint8) bool {
	if !esperarps2EntradaVacío() {
		return false
	}
	Puertoescribirocteto(ordenpuerto_2, valor)
	return true
}

func escribirps2datos(valor uint8) bool {
	if !esperarps2EntradaVacío() {
		return false
	}
	Puertoescribirocteto(datospuerto_2, valor)
	return true
}

func leerps2datos() (uint8, bool) {
	if !esperarps2SalidaCompleto() {
		return 0, false
	}
	return Puertoleerocteto(datospuerto_2), true
}

func enviarratónOrden(valor uint8) bool {
	if !escribirps2Orden(0xD4) || !escribirps2datos(valor) {
		return false
	}
	ack, aceptar := leerps2datos()
	return aceptar && ack == 0xFA
}

func (propio *TRatóncontrolador) Initcontrolador(gestor *TInterrupcióngestor, ratóneventohandler IRatóneventohandler) {

	iratóneventohandler = TPredeterminadoratóneventohandler{}

	if ratóneventohandler != nil {
		iratóneventohandler = ratóneventohandler
	}

	activoratóncontrolador = propio
	interrupciónhandler = manijaratóninterrupción
	var dirección uintptr
	dirección = uintptr(Pointer(&interrupciónhandler))
	propio.Init(0x2C, uintptr(Pointer(gestor)), dirección)

	for i := 0; i < 32 && (Puertoleerocteto(ordenpuerto_2)&0x01) != 0; i++ {
		Puertoleerocteto(datospuerto_2)
	}

	if !escribirps2Orden(0xA8) || !escribirps2Orden(0x20) {
		return
	}
	estado, aceptar := leerps2datos()
	if !aceptar {
		return
	}
	estado |= 0x02
	estado &^= 0x20
	if !escribirps2Orden(0x60) || !escribirps2datos(estado) {
		return
	}

	if !enviarratónOrden(0xF6) || !enviarratónOrden(0xF4) {
		return
	}
	desplazamiento = 0

}

func manijaratóninterrupción(esp uint32) uint32 {
	if activoratóncontrolador == nil {
		Puertoleerocteto(datospuerto_2)
		return esp
	}
	return activoratóncontrolador.Manijainterrupción(esp)
}

var recuento uint8 = 0
var buffer_2 [3]int8
var desplazamiento uint8 = 0

var botón_2 int8
var pendientex int16
var pendientey int16
var pendienteBotón int8
var pendienteratónevento bool

func (propio *TRatóncontrolador) Manijainterrupción(esp uint32) uint32 {
	estado := Puertoleerocteto(ordenpuerto_2)
	if (estado&0x01) == 0 || (estado&0x20) == 0 {
		return esp
	}

	datos := Puertoleerocteto(datospuerto_2)

	if desplazamiento == 0 && (datos&0x08) == 0 {
		return esp
	}
	buffer_2[desplazamiento] = int8(datos)
	desplazamiento = (desplazamiento + 1) % 3
	if desplazamiento == 0 {
		pAQUETEEstado := uint8(buffer_2[0])

		if (pAQUETEEstado & 0xC0) == 0 {
			pendientex += int16(buffer_2[1])
			pendientey += int16(buffer_2[2])
			if pendientex > 127 {
				pendientex = 127
			} else if pendientex < -127 {
				pendientex = -127
			}
			if pendientey > 127 {
				pendientey = 127
			} else if pendientey < -127 {
				pendientey = -127
			}
		}
		pendienteBotón = int8(pAQUETEEstado & 0x07)
		pendienteratónevento = true
	}

	return esp

}

func Procesopendienteratóneventos() {
	if iratóneventohandler == nil {
		return
	}

	Interrupcióndeactive()
	if !pendienteratónevento {
		InterrupciónActivo()
		return
	}
	x := int8(pendientex)
	y := int8(pendientey)
	nuevoBotón := pendienteBotón
	oldBotón := botón_2

	pendientex = 0
	pendientey = 0
	pendienteratónevento = false
	InterrupciónActivo()

	if x != 0 || y != 0 {
		iratóneventohandler.AlratónMover(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		máscara := int8(0x1 << i)
		if (nuevoBotón & máscara) != (oldBotón & máscara) {
			if (nuevoBotón & máscara) != 0 {
				iratóneventohandler.AlratónAbajo(int8(i + 1))
			} else {
				iratóneventohandler.AlratónSubir(int8(i + 1))
			}
		}
	}
	botón_2 = nuevoBotón
}
