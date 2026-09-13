package klaviatuur

import . "unsafe"

import . "port"
import . "katkestus"

import . "console"
import . "süsteemcall"

type IKlaviatuurSündmushandler interface {
	SeesVõtiNoolalla(võti byte)
	SeesVõtiÜles(võti byte)
}

var iKlaviatuurSündmushandler IKlaviatuurSündmushandler
var vaikimisiKlaviatuurSündmushandler TVaikimisiKlaviatuurSündmushandler

type TVaikimisiKlaviatuurSündmushandler struct {
}

func (ise *TVaikimisiKlaviatuurSündmushandler) SeesVõtiNoolalla(võti byte) {
	väärtus16ndsüsteem := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = väärtus16ndsüsteem[((võti >> 4) & 0xF)]
	buffer[18] = väärtus16ndsüsteem[võti&0xF]

	console_2 := TConsole{}
	console_2.MPrindi(buffer)

}
func (ise *TVaikimisiKlaviatuurSündmushandler) SeesVõtiÜles(võti byte) {
}

type TKlaviatuurdriver struct {
	TKatkestushandler
}

var aktiivneKlaviatuurdriver *TKlaviatuurdriver
var katkestushandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var käskport_2 uint16 = 0x64

const ps2OotaPiir = 100000

func ootaps2SisendTühi() bool {
	for i := 0; i < ps2OotaPiir; i++ {
		if (PortLugeminebyte(käskport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ootaps2VäljundTäielik() bool {
	for i := 0; i < ps2OotaPiir; i++ {
		if (PortLugeminebyte(käskport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func kirjutamineps2Käsk(väärtus uint8) bool {
	if !ootaps2SisendTühi() {
		return false
	}
	PortKirjutaminebyte(käskport_2, väärtus)
	return true
}

func kirjutamineps2data(väärtus uint8) bool {
	if !ootaps2SisendTühi() {
		return false
	}
	PortKirjutaminebyte(dataport_2, väärtus)
	return true
}

func lugemineps2data() (uint8, bool) {
	if !ootaps2VäljundTäielik() {
		return 0, false
	}
	return PortLugeminebyte(dataport_2), true
}

func (ise *TKlaviatuurdriver) Initdriver(manager *TKatkestusmanager, klaviatuurSündmushandler IKlaviatuurSündmushandler) {

	iKlaviatuurSündmushandler = &vaikimisiKlaviatuurSündmushandler
	if klaviatuurSündmushandler != nil {
		iKlaviatuurSündmushandler = klaviatuurSündmushandler
	}

	aktiivneKlaviatuurdriver = ise
	katkestushandler = handleKlaviatuurKatkestus
	var address uintptr
	address = uintptr(Pointer(&katkestushandler))

	ise.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (PortLugeminebyte(käskport_2)&0x01) != 0; i++ {
		PortLugeminebyte(dataport_2)
	}

	if !kirjutamineps2Käsk(0xAE) || !kirjutamineps2Käsk(0x20) {
		return
	}
	olek, olgu := lugemineps2data()
	if !olgu {
		return
	}
	olek |= 0x01
	olek &^= 0x10
	if !kirjutamineps2Käsk(0x60) || !kirjutamineps2data(olek) {
		return
	}

	if !kirjutamineps2data(0xF4) {
		return
	}
	ack, olgu := lugemineps2data()
	if !olgu || ack != 0xFA {
		return
	}

}

func handleKlaviatuurKatkestus(esp uint32) uint32 {
	if aktiivneKlaviatuurdriver == nil {
		PortLugeminebyte(dataport_2)
		return esp
	}
	return aktiivneKlaviatuurdriver.HandleKatkestus(esp)
}

const klaviatuurqueueSuurus = 64

var klaviatuurqueue [klaviatuurqueueSuurus]byte
var klaviatuurqueueLugemine uint8
var klaviatuurqueueKirjutamine uint8
var vasakulshift bool
var paremalshift bool
var extendedVaataläbicode bool

func queueKlaviatuurbyte(võti byte) {
	järgmine := (klaviatuurqueueKirjutamine + 1) % klaviatuurqueueSuurus
	if järgmine == klaviatuurqueueLugemine {
		return
	}
	klaviatuurqueue[klaviatuurqueueKirjutamine] = võti
	klaviatuurqueueKirjutamine = järgmine
}

func ProtsesspendingKlaviatuurSündmused() {
	for klaviatuurqueueLugemine != klaviatuurqueueKirjutamine {
		võti := klaviatuurqueue[klaviatuurqueueLugemine]
		klaviatuurqueueLugemine = (klaviatuurqueueLugemine + 1) % klaviatuurqueueSuurus
		Stdinputbyte(võti)
		if iKlaviatuurSündmushandler != nil {
			iKlaviatuurSündmushandler.SeesVõtiNoolalla(võti)
		}
	}
}

func vaataläbicodetobyte(vaataläbicode uint8) (byte, bool) {
	shift := vasakulshift || paremalshift

	if vaataläbicode >= 0x02 && vaataläbicode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[vaataläbicode-0x02], true
		}
		return "1234567890"[vaataläbicode-0x02], true
	}
	if vaataläbicode >= 0x10 && vaataläbicode <= 0x19 {
		võti := "qwertyuiop"[vaataläbicode-0x10]
		if shift {
			võti -= 'a' - 'A'
		}
		return võti, true
	}
	if vaataläbicode >= 0x1E && vaataläbicode <= 0x26 {
		võti := "asdfghjkl"[vaataläbicode-0x1E]
		if shift {
			võti -= 'a' - 'A'
		}
		return võti, true
	}
	if vaataläbicode >= 0x2C && vaataläbicode <= 0x32 {
		võti := "zxcvbnm"[vaataläbicode-0x2C]
		if shift {
			võti -= 'a' - 'A'
		}
		return võti, true
	}

	switch vaataläbicode {
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

func (ise *TKlaviatuurdriver) HandleKatkestus(esp uint32) uint32 {
	olek := PortLugeminebyte(käskport_2)
	if (olek&0x01) == 0 || (olek&0x20) != 0 {
		return esp
	}

	vaataläbicode := PortLugeminebyte(dataport_2)
	if vaataläbicode == 0xE0 {
		extendedVaataläbicode = true
		return esp
	}
	if extendedVaataläbicode {
		extendedVaataläbicode = false
		return esp
	}

	released := (vaataläbicode & 0x80) != 0
	basecode := vaataläbicode & 0x7F
	if basecode == 0x2A {
		vasakulshift = !released
		return esp
	}
	if basecode == 0x36 {
		paremalshift = !released
		return esp
	}
	if released {
		return esp
	}

	if võti, olgu := vaataläbicodetobyte(basecode); olgu {
		queueKlaviatuurbyte(võti)
	}

	return esp
}
