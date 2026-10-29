/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package teclado

import . "unsafe"

import . "puerto"
import . "interrupción"

import . "consola"
import . "sistemallamada"

type ITecladoeventohandler interface {
	AlClaveAbajo(clave byte)
	AlClaveSubir(clave byte)
}

var itecladoeventohandler ITecladoeventohandler
var predeterminadotecladoeventohandler TPredeterminadotecladoeventohandler

type TPredeterminadotecladoeventohandler struct {
}

func (propio *TPredeterminadotecladoeventohandler) AlClaveAbajo(clave byte) {
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hexadecimal[((clave >> 4) & 0xF)]
	buffer[18] = hexadecimal[clave&0xF]

	consola_2 := TConsola{}
	consola_2.MImprimir(buffer)

}
func (propio *TPredeterminadotecladoeventohandler) AlClaveSubir(clave byte) {
}

type TTecladocontrolador struct {
	TInterrupciónhandler
}

var activotecladocontrolador *TTecladocontrolador
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

func (propio *TTecladocontrolador) Initcontrolador(gestor *TInterrupcióngestor, tecladoeventohandler ITecladoeventohandler) {

	itecladoeventohandler = &predeterminadotecladoeventohandler
	if tecladoeventohandler != nil {
		itecladoeventohandler = tecladoeventohandler
	}

	activotecladocontrolador = propio
	interrupciónhandler = manijatecladointerrupción
	var dirección uintptr
	dirección = uintptr(Pointer(&interrupciónhandler))

	propio.Init(0x21, uintptr(Pointer(gestor)), dirección)

	for i := 0; i < 32 && (Puertoleerocteto(ordenpuerto_2)&0x01) != 0; i++ {
		Puertoleerocteto(datospuerto_2)
	}

	if !escribirps2Orden(0xAE) || !escribirps2Orden(0x20) {
		return
	}
	estado, aceptar := leerps2datos()
	if !aceptar {
		return
	}
	estado |= 0x01
	estado &^= 0x10
	if !escribirps2Orden(0x60) || !escribirps2datos(estado) {
		return
	}

	if !escribirps2datos(0xF4) {
		return
	}
	ack, aceptar := leerps2datos()
	if !aceptar || ack != 0xFA {
		return
	}

}

func manijatecladointerrupción(esp uint32) uint32 {
	if activotecladocontrolador == nil {
		Puertoleerocteto(datospuerto_2)
		return esp
	}
	return activotecladocontrolador.Manijainterrupción(esp)
}

const tecladocolaTamaño = 64

var tecladocola [tecladocolaTamaño]byte
var tecladocolaleer uint8
var tecladocolaescribir uint8
var izquierdaMayús bool
var derechaMayús bool
var extendedInspeccionarcode bool

func colatecladoocteto(clave byte) {
	siguiente := (tecladocolaescribir + 1) % tecladocolaTamaño
	if siguiente == tecladocolaleer {
		return
	}
	tecladocola[tecladocolaescribir] = clave
	tecladocolaescribir = siguiente
}

func Procesopendientetecladoeventos() {
	for tecladocolaleer != tecladocolaescribir {
		clave := tecladocola[tecladocolaleer]
		tecladocolaleer = (tecladocolaleer + 1) % tecladocolaTamaño
		Stdinputocteto(clave)
		if itecladoeventohandler != nil {
			itecladoeventohandler.AlClaveAbajo(clave)
		}
	}
}

func inspeccionarcodetoocteto(inspeccionarcode uint8) (byte, bool) {
	mayús := izquierdaMayús || derechaMayús

	if inspeccionarcode >= 0x02 && inspeccionarcode <= 0x0B {
		if mayús {
			return "!@#$%^&*()"[inspeccionarcode-0x02], true
		}
		return "1234567890"[inspeccionarcode-0x02], true
	}
	if inspeccionarcode >= 0x10 && inspeccionarcode <= 0x19 {
		clave := "qwertyuiop"[inspeccionarcode-0x10]
		if mayús {
			clave -= 'a' - 'A'
		}
		return clave, true
	}
	if inspeccionarcode >= 0x1E && inspeccionarcode <= 0x26 {
		clave := "asdfghjkl"[inspeccionarcode-0x1E]
		if mayús {
			clave -= 'a' - 'A'
		}
		return clave, true
	}
	if inspeccionarcode >= 0x2C && inspeccionarcode <= 0x32 {
		clave := "zxcvbnm"[inspeccionarcode-0x2C]
		if mayús {
			clave -= 'a' - 'A'
		}
		return clave, true
	}

	switch inspeccionarcode {
	case 0x0C:
		if mayús {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if mayús {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if mayús {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if mayús {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if mayús {
			return ':', true
		}
		return ';', true
	case 0x28:
		if mayús {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if mayús {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if mayús {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if mayús {
			return '<', true
		}
		return ',', true
	case 0x34:
		if mayús {
			return '>', true
		}
		return '.', true
	case 0x35:
		if mayús {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (propio *TTecladocontrolador) Manijainterrupción(esp uint32) uint32 {
	estado := Puertoleerocteto(ordenpuerto_2)
	if (estado&0x01) == 0 || (estado&0x20) != 0 {
		return esp
	}

	inspeccionarcode := Puertoleerocteto(datospuerto_2)
	if inspeccionarcode == 0xE0 {
		extendedInspeccionarcode = true
		return esp
	}
	if extendedInspeccionarcode {
		extendedInspeccionarcode = false
		return esp
	}

	released := (inspeccionarcode & 0x80) != 0
	basecode := inspeccionarcode & 0x7F
	if basecode == 0x2A {
		izquierdaMayús = !released
		return esp
	}
	if basecode == 0x36 {
		derechaMayús = !released
		return esp
	}
	if released {
		return esp
	}

	if clave, aceptar := inspeccionarcodetoocteto(basecode); aceptar {
		colatecladoocteto(clave)
	}

	return esp
}
