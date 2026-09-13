package የፊደልሠሌዳ

import . "unsafe"

import . "port"
import . "ማቋረጫ"

import . "console"
import . "ስርአትcall"

type Iየፊደልሠሌዳeventhandler interface {
	Oማብሪያቁልፍወደታች(ቁልፍ byte)
	Oማብሪያቁልፍወደላይ(ቁልፍ byte)
}

var iየፊደልሠሌዳeventhandler Iየፊደልሠሌዳeventhandler
var ነባርየፊደልሠሌዳeventhandler Tነባርየፊደልሠሌዳeventhandler

type Tነባርየፊደልሠሌዳeventhandler struct {
}

func (self *Tነባርየፊደልሠሌዳeventhandler) Oማብሪያቁልፍወደታች(ቁልፍ byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((ቁልፍ >> 4) & 0xF)]
	buffer[18] = hex[ቁልፍ&0xF]

	console_2 := TConsole{}
	console_2.Mማተሚያ(buffer)

}
func (self *Tነባርየፊደልሠሌዳeventhandler) Oማብሪያቁልፍወደላይ(ቁልፍ byte) {
}

type Tየፊደልሠሌዳdriver struct {
	Tማቋረጫhandler
}

var አሰራየፊደልሠሌዳdriver *Tየፊደልሠሌዳdriver
var ማቋረጫhandler func(uint32) uint32

var dataport_2 uint16 = 0x60
var ትእዛዝport_2 uint16 = 0x64

const ps2ይጠብቁገደብ = 100000

func ይጠብቁps2ማስገቢያባዶ() bool {
	for i := 0; i < ps2ይጠብቁገደብ; i++ {
		if (Portማንበቢያbyte(ትእዛዝport_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func ይጠብቁps2ውጤትሙሉ() bool {
	for i := 0; i < ps2ይጠብቁገደብ; i++ {
		if (Portማንበቢያbyte(ትእዛዝport_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func መጻፊያps2ትእዛዝ(ዋጋ uint8) bool {
	if !ይጠብቁps2ማስገቢያባዶ() {
		return false
	}
	Portመጻፊያbyte(ትእዛዝport_2, ዋጋ)
	return true
}

func መጻፊያps2data(ዋጋ uint8) bool {
	if !ይጠብቁps2ማስገቢያባዶ() {
		return false
	}
	Portመጻፊያbyte(dataport_2, ዋጋ)
	return true
}

func ማንበቢያps2data() (uint8, bool) {
	if !ይጠብቁps2ውጤትሙሉ() {
		return 0, false
	}
	return Portማንበቢያbyte(dataport_2), true
}

func (self *Tየፊደልሠሌዳdriver) Initdriver(manager *Tማቋረጫmanager, የፊደልሠሌዳeventhandler Iየፊደልሠሌዳeventhandler) {

	iየፊደልሠሌዳeventhandler = &ነባርየፊደልሠሌዳeventhandler
	if የፊደልሠሌዳeventhandler != nil {
		iየፊደልሠሌዳeventhandler = የፊደልሠሌዳeventhandler
	}

	አሰራየፊደልሠሌዳdriver = self
	ማቋረጫhandler = handleየፊደልሠሌዳማቋረጫ
	var address uintptr
	address = uintptr(Pointer(&ማቋረጫhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Portማንበቢያbyte(ትእዛዝport_2)&0x01) != 0; i++ {
		Portማንበቢያbyte(dataport_2)
	}

	if !መጻፊያps2ትእዛዝ(0xAE) || !መጻፊያps2ትእዛዝ(0x20) {
		return
	}
	ሁኔታ, እሺ := ማንበቢያps2data()
	if !እሺ {
		return
	}
	ሁኔታ |= 0x01
	ሁኔታ &^= 0x10
	if !መጻፊያps2ትእዛዝ(0x60) || !መጻፊያps2data(ሁኔታ) {
		return
	}

	if !መጻፊያps2data(0xF4) {
		return
	}
	ack, እሺ := ማንበቢያps2data()
	if !እሺ || ack != 0xFA {
		return
	}

}

func handleየፊደልሠሌዳማቋረጫ(esp uint32) uint32 {
	if አሰራየፊደልሠሌዳdriver == nil {
		Portማንበቢያbyte(dataport_2)
		return esp
	}
	return አሰራየፊደልሠሌዳdriver.Handleማቋረጫ(esp)
}

const የፊደልሠሌዳqueueመጠን = 64

var የፊደልሠሌዳqueue [የፊደልሠሌዳqueueመጠን]byte
var የፊደልሠሌዳqueueማንበቢያ uint8
var የፊደልሠሌዳqueueመጻፊያ uint8
var ግራshift bool
var ቀኝshift bool
var extendedማሰሻcode bool

func queueየፊደልሠሌዳbyte(ቁልፍ byte) {
	የሚቀጥለው := (የፊደልሠሌዳqueueመጻፊያ + 1) % የፊደልሠሌዳqueueመጠን
	if የሚቀጥለው == የፊደልሠሌዳqueueማንበቢያ {
		return
	}
	የፊደልሠሌዳqueue[የፊደልሠሌዳqueueመጻፊያ] = ቁልፍ
	የፊደልሠሌዳqueueመጻፊያ = የሚቀጥለው
}

func Pሂደቶችpendingየፊደልሠሌዳevents() {
	for የፊደልሠሌዳqueueማንበቢያ != የፊደልሠሌዳqueueመጻፊያ {
		ቁልፍ := የፊደልሠሌዳqueue[የፊደልሠሌዳqueueማንበቢያ]
		የፊደልሠሌዳqueueማንበቢያ = (የፊደልሠሌዳqueueማንበቢያ + 1) % የፊደልሠሌዳqueueመጠን
		Stdinputbyte(ቁልፍ)
		if iየፊደልሠሌዳeventhandler != nil {
			iየፊደልሠሌዳeventhandler.Oማብሪያቁልፍወደታች(ቁልፍ)
		}
	}
}

func ማሰሻcodetobyte(ማሰሻcode uint8) (byte, bool) {
	shift := ግራshift || ቀኝshift

	if ማሰሻcode >= 0x02 && ማሰሻcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[ማሰሻcode-0x02], true
		}
		return "1234567890"[ማሰሻcode-0x02], true
	}
	if ማሰሻcode >= 0x10 && ማሰሻcode <= 0x19 {
		ቁልፍ := "qwertyuiop"[ማሰሻcode-0x10]
		if shift {
			ቁልፍ -= 'a' - 'A'
		}
		return ቁልፍ, true
	}
	if ማሰሻcode >= 0x1E && ማሰሻcode <= 0x26 {
		ቁልፍ := "asdfghjkl"[ማሰሻcode-0x1E]
		if shift {
			ቁልፍ -= 'a' - 'A'
		}
		return ቁልፍ, true
	}
	if ማሰሻcode >= 0x2C && ማሰሻcode <= 0x32 {
		ቁልፍ := "zxcvbnm"[ማሰሻcode-0x2C]
		if shift {
			ቁልፍ -= 'a' - 'A'
		}
		return ቁልፍ, true
	}

	switch ማሰሻcode {
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

func (self *Tየፊደልሠሌዳdriver) Handleማቋረጫ(esp uint32) uint32 {
	ሁኔታ := Portማንበቢያbyte(ትእዛዝport_2)
	if (ሁኔታ&0x01) == 0 || (ሁኔታ&0x20) != 0 {
		return esp
	}

	ማሰሻcode := Portማንበቢያbyte(dataport_2)
	if ማሰሻcode == 0xE0 {
		extendedማሰሻcode = true
		return esp
	}
	if extendedማሰሻcode {
		extendedማሰሻcode = false
		return esp
	}

	released := (ማሰሻcode & 0x80) != 0
	basecode := ማሰሻcode & 0x7F
	if basecode == 0x2A {
		ግራshift = !released
		return esp
	}
	if basecode == 0x36 {
		ቀኝshift = !released
		return esp
	}
	if released {
		return esp
	}

	if ቁልፍ, እሺ := ማሰሻcodetobyte(basecode); እሺ {
		queueየፊደልሠሌዳbyte(ቁልፍ)
	}

	return esp
}
