package tastiera

import . "unsafe"

import . "porta"
import . "interrupt"

import . "console"
import . "sistemacall"

type ITastieraEventohandler interface {
	AccesoChiaveGiù(chiave byte)
	AccesoChiaveSu(chiave byte)
}

var iTastieraEventohandler ITastieraEventohandler
var predefinitoTastieraEventohandler TPredefinitoTastieraEventohandler

type TPredefinitoTastieraEventohandler struct {
}

func (séstesso *TPredefinitoTastieraEventohandler) AccesoChiaveGiù(chiave byte) {
	esadecimale := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = esadecimale[((chiave >> 4) & 0xF)]
	buffer[18] = esadecimale[chiave&0xF]

	console_2 := TConsole{}
	console_2.MStampa(buffer)

}
func (séstesso *TPredefinitoTastieraEventohandler) AccesoChiaveSu(chiave byte) {
}

type TTastieradriver struct {
	TInterrupthandler
}

var attivoTastieradriver *TTastieradriver
var interrupthandler func(uint32) uint32

var dataPorta_2 uint16 = 0x60
var comandoPorta_2 uint16 = 0x64

const ps2AttendiLimite = 100000

func attendips2IngressoVuoto() bool {
	for i := 0; i < ps2AttendiLimite; i++ {
		if (PortaLetturabyte(comandoPorta_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func attendips2UscitaCompleto() bool {
	for i := 0; i < ps2AttendiLimite; i++ {
		if (PortaLetturabyte(comandoPorta_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func scritturaps2Comando(valore uint8) bool {
	if !attendips2IngressoVuoto() {
		return false
	}
	PortaScritturabyte(comandoPorta_2, valore)
	return true
}

func scritturaps2data(valore uint8) bool {
	if !attendips2IngressoVuoto() {
		return false
	}
	PortaScritturabyte(dataPorta_2, valore)
	return true
}

func letturaps2data() (uint8, bool) {
	if !attendips2UscitaCompleto() {
		return 0, false
	}
	return PortaLetturabyte(dataPorta_2), true
}

func (séstesso *TTastieradriver) Initdriver(manager *TInterruptmanager, tastieraEventohandler ITastieraEventohandler) {

	iTastieraEventohandler = &predefinitoTastieraEventohandler
	if tastieraEventohandler != nil {
		iTastieraEventohandler = tastieraEventohandler
	}

	attivoTastieradriver = séstesso
	interrupthandler = manigliaTastierainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	séstesso.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortaLetturabyte(comandoPorta_2)&0x01) != 0; i++ {
		PortaLetturabyte(dataPorta_2)
	}

	if !scritturaps2Comando(0xAE) || !scritturaps2Comando(0x20) {
		return
	}
	stato, fatto := letturaps2data()
	if !fatto {
		return
	}
	stato |= 0x01
	stato &^= 0x10
	if !scritturaps2Comando(0x60) || !scritturaps2data(stato) {
		return
	}

	if !scritturaps2data(0xF4) {
		return
	}
	ack, fatto := letturaps2data()
	if !fatto || ack != 0xFA {
		return
	}

}

func manigliaTastierainterrupt(esp uint32) uint32 {
	if attivoTastieradriver == nil {
		PortaLetturabyte(dataPorta_2)
		return esp
	}
	return attivoTastieradriver.Manigliainterrupt(esp)
}

const tastieraqueueDimensione = 64

var tastieraqueue [tastieraqueueDimensione]byte
var tastieraqueueLettura uint8
var tastieraqueueScrittura uint8
var sinistraMaiusc bool
var destraMaiusc bool
var extendedScansionecode bool

func queueTastierabyte(chiave byte) {
	successivo := (tastieraqueueScrittura + 1) % tastieraqueueDimensione
	if successivo == tastieraqueueLettura {
		return
	}
	tastieraqueue[tastieraqueueScrittura] = chiave
	tastieraqueueScrittura = successivo
}

func ProcessipendingTastieraEventi() {
	for tastieraqueueLettura != tastieraqueueScrittura {
		chiave := tastieraqueue[tastieraqueueLettura]
		tastieraqueueLettura = (tastieraqueueLettura + 1) % tastieraqueueDimensione
		Stdinputbyte(chiave)
		if iTastieraEventohandler != nil {
			iTastieraEventohandler.AccesoChiaveGiù(chiave)
		}
	}
}

func scansionecodetobyte(scansionecode uint8) (byte, bool) {
	maiusc := sinistraMaiusc || destraMaiusc

	if scansionecode >= 0x02 && scansionecode <= 0x0B {
		if maiusc {
			return "!@#$%^&*()"[scansionecode-0x02], true
		}
		return "1234567890"[scansionecode-0x02], true
	}
	if scansionecode >= 0x10 && scansionecode <= 0x19 {
		chiave := "qwertyuiop"[scansionecode-0x10]
		if maiusc {
			chiave -= 'a' - 'A'
		}
		return chiave, true
	}
	if scansionecode >= 0x1E && scansionecode <= 0x26 {
		chiave := "asdfghjkl"[scansionecode-0x1E]
		if maiusc {
			chiave -= 'a' - 'A'
		}
		return chiave, true
	}
	if scansionecode >= 0x2C && scansionecode <= 0x32 {
		chiave := "zxcvbnm"[scansionecode-0x2C]
		if maiusc {
			chiave -= 'a' - 'A'
		}
		return chiave, true
	}

	switch scansionecode {
	case 0x0C:
		if maiusc {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if maiusc {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if maiusc {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if maiusc {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if maiusc {
			return ':', true
		}
		return ';', true
	case 0x28:
		if maiusc {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if maiusc {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if maiusc {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if maiusc {
			return '<', true
		}
		return ',', true
	case 0x34:
		if maiusc {
			return '>', true
		}
		return '.', true
	case 0x35:
		if maiusc {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (séstesso *TTastieradriver) Manigliainterrupt(esp uint32) uint32 {
	stato := PortaLetturabyte(comandoPorta_2)
	if (stato&0x01) == 0 || (stato&0x20) != 0 {
		return esp
	}

	scansionecode := PortaLetturabyte(dataPorta_2)
	if scansionecode == 0xE0 {
		extendedScansionecode = true
		return esp
	}
	if extendedScansionecode {
		extendedScansionecode = false
		return esp
	}

	released := (scansionecode & 0x80) != 0
	basecode := scansionecode & 0x7F
	if basecode == 0x2A {
		sinistraMaiusc = !released
		return esp
	}
	if basecode == 0x36 {
		destraMaiusc = !released
		return esp
	}
	if released {
		return esp
	}

	if chiave, fatto := scansionecodetobyte(basecode); fatto {
		queueTastierabyte(chiave)
	}

	return esp
}
