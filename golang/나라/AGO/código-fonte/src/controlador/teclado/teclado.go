package teclado

import . "unsafe"

import . "porto"
import . "interrupção"

import . "console"
import . "sistemachamada"

type ITecladoeventohandler interface {
	AoChaveAbaixo(chave byte)
	AoChaveParacima(chave byte)
}

var itecladoeventohandler ITecladoeventohandler
var predefiniçãotecladoeventohandler TPredefiniçãotecladoeventohandler

type TPredefiniçãotecladoeventohandler struct {
}

func (próprio *TPredefiniçãotecladoeventohandler) AoChaveAbaixo(chave byte) {
	hexadecimal := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hexadecimal[((chave >> 4) & 0xF)]
	buffer[18] = hexadecimal[chave&0xF]

	console_2 := TConsole{}
	console_2.MImprimir(buffer)

}
func (próprio *TPredefiniçãotecladoeventohandler) AoChaveParacima(chave byte) {
}

type TTecladocontrolador struct {
	TInterrupçãohandler
}

var ativotecladocontrolador *TTecladocontrolador
var interrupçãohandler func(uint32) uint32

var dadosporto_2 uint16 = 0x60
var comandoporto_2 uint16 = 0x64

const ps2EsperarLimite = 100000

func esperarps2EntradaVazio() bool {
	for i := 0; i < ps2EsperarLimite; i++ {
		if (Portolerocteto(comandoporto_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func esperarps2ResultadoTotal() bool {
	for i := 0; i < ps2EsperarLimite; i++ {
		if (Portolerocteto(comandoporto_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func escreverps2Comando(valor uint8) bool {
	if !esperarps2EntradaVazio() {
		return false
	}
	Portoescreverocteto(comandoporto_2, valor)
	return true
}

func escreverps2dados(valor uint8) bool {
	if !esperarps2EntradaVazio() {
		return false
	}
	Portoescreverocteto(dadosporto_2, valor)
	return true
}

func lerps2dados() (uint8, bool) {
	if !esperarps2ResultadoTotal() {
		return 0, false
	}
	return Portolerocteto(dadosporto_2), true
}

func (próprio *TTecladocontrolador) Initcontrolador(gestor *TInterrupçãogestor, tecladoeventohandler ITecladoeventohandler) {

	itecladoeventohandler = &predefiniçãotecladoeventohandler
	if tecladoeventohandler != nil {
		itecladoeventohandler = tecladoeventohandler
	}

	ativotecladocontrolador = próprio
	interrupçãohandler = manípulotecladointerrupção
	var endereço uintptr
	endereço = uintptr(Pointer(&interrupçãohandler))

	próprio.Init(0x21, uintptr(Pointer(gestor)), endereço)

	for i := 0; i < 32 && (Portolerocteto(comandoporto_2)&0x01) != 0; i++ {
		Portolerocteto(dadosporto_2)
	}

	if !escreverps2Comando(0xAE) || !escreverps2Comando(0x20) {
		return
	}
	estado, aceitar := lerps2dados()
	if !aceitar {
		return
	}
	estado |= 0x01
	estado &^= 0x10
	if !escreverps2Comando(0x60) || !escreverps2dados(estado) {
		return
	}

	if !escreverps2dados(0xF4) {
		return
	}
	ack, aceitar := lerps2dados()
	if !aceitar || ack != 0xFA {
		return
	}

}

func manípulotecladointerrupção(esp uint32) uint32 {
	if ativotecladocontrolador == nil {
		Portolerocteto(dadosporto_2)
		return esp
	}
	return ativotecladocontrolador.Manípulointerrupção(esp)
}

const tecladofilaTamanho = 64

var tecladofila [tecladofilaTamanho]byte
var tecladofilaler uint8
var tecladofilaescrever uint8
var esquerdashift bool
var direitashift bool
var extendedAnalisarcode bool

func filatecladoocteto(chave byte) {
	seguinte := (tecladofilaescrever + 1) % tecladofilaTamanho
	if seguinte == tecladofilaler {
		return
	}
	tecladofila[tecladofilaescrever] = chave
	tecladofilaescrever = seguinte
}

func Processopendentetecladoeventos() {
	for tecladofilaler != tecladofilaescrever {
		chave := tecladofila[tecladofilaler]
		tecladofilaler = (tecladofilaler + 1) % tecladofilaTamanho
		Stdinputocteto(chave)
		if itecladoeventohandler != nil {
			itecladoeventohandler.AoChaveAbaixo(chave)
		}
	}
}

func analisarcodeparaocteto(analisarcode uint8) (byte, bool) {
	shift := esquerdashift || direitashift

	if analisarcode >= 0x02 && analisarcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[analisarcode-0x02], true
		}
		return "1234567890"[analisarcode-0x02], true
	}
	if analisarcode >= 0x10 && analisarcode <= 0x19 {
		chave := "qwertyuiop"[analisarcode-0x10]
		if shift {
			chave -= 'a' - 'A'
		}
		return chave, true
	}
	if analisarcode >= 0x1E && analisarcode <= 0x26 {
		chave := "asdfghjkl"[analisarcode-0x1E]
		if shift {
			chave -= 'a' - 'A'
		}
		return chave, true
	}
	if analisarcode >= 0x2C && analisarcode <= 0x32 {
		chave := "zxcvbnm"[analisarcode-0x2C]
		if shift {
			chave -= 'a' - 'A'
		}
		return chave, true
	}

	switch analisarcode {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (próprio *TTecladocontrolador) Manípulointerrupção(esp uint32) uint32 {
	estado := Portolerocteto(comandoporto_2)
	if (estado&0x01) == 0 || (estado&0x20) != 0 {
		return esp
	}

	analisarcode := Portolerocteto(dadosporto_2)
	if analisarcode == 0xE0 {
		extendedAnalisarcode = true
		return esp
	}
	if extendedAnalisarcode {
		extendedAnalisarcode = false
		return esp
	}

	released := (analisarcode & 0x80) != 0
	basecode := analisarcode & 0x7F
	if basecode == 0x2A {
		esquerdashift = !released
		return esp
	}
	if basecode == 0x36 {
		direitashift = !released
		return esp
	}
	if released {
		return esp
	}

	if chave, aceitar := analisarcodeparaocteto(basecode); aceitar {
		filatecladoocteto(chave)
	}

	return esp
}
