package klaviatura

import . "unsafe"

import . "qapı"
import . "interrupt"

import . "console"
import . "systemcall"

type IKlaviaturaeventhandler interface {
	OnAçardown(açar byte)
	OnAçarYuxarı(açar byte)
}

var iKlaviaturaeventhandler IKlaviaturaeventhandler
var önQurğuluKlaviaturaeventhandler TÖnQurğuluKlaviaturaeventhandler

type TÖnQurğuluKlaviaturaeventhandler struct {
}

func (self *TÖnQurğuluKlaviaturaeventhandler) OnAçardown(açar byte) {
	onaltılıq := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = onaltılıq[((açar >> 4) & 0xF)]
	buffer[18] = onaltılıq[açar&0xF]

	console_2 := TConsole{}
	console_2.MÇapEt(buffer)

}
func (self *TÖnQurğuluKlaviaturaeventhandler) OnAçarYuxarı(açar byte) {
}

type TKlaviaturadriver struct {
	TInterrupthandler
}

var fəalKlaviaturadriver *TKlaviaturadriver
var interrupthandler func(uint32) uint32

var dataQapı_2 uint16 = 0x60
var əmrQapı_2 uint16 = 0x64

const ps2waitlimit = 100000

func waitps2inputempty() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (QapıOxumabyte(əmrQapı_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func waitps2outputTam() bool {
	for i := 0; i < ps2waitlimit; i++ {
		if (QapıOxumabyte(əmrQapı_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func yazmaps2Əmr(qiymət uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	QapıYazmabyte(əmrQapı_2, qiymət)
	return true
}

func yazmaps2data(qiymət uint8) bool {
	if !waitps2inputempty() {
		return false
	}
	QapıYazmabyte(dataQapı_2, qiymət)
	return true
}

func oxumaps2data() (uint8, bool) {
	if !waitps2outputTam() {
		return 0, false
	}
	return QapıOxumabyte(dataQapı_2), true
}

func (self *TKlaviaturadriver) Initdriver(manager *TInterruptmanager, klaviaturaeventhandler IKlaviaturaeventhandler) {

	iKlaviaturaeventhandler = &önQurğuluKlaviaturaeventhandler
	if klaviaturaeventhandler != nil {
		iKlaviaturaeventhandler = klaviaturaeventhandler
	}

	fəalKlaviaturadriver = self
	interrupthandler = handleKlaviaturainterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (QapıOxumabyte(əmrQapı_2)&0x01) != 0; i++ {
		QapıOxumabyte(dataQapı_2)
	}

	if !yazmaps2Əmr(0xAE) || !yazmaps2Əmr(0x20) {
		return
	}
	vəziyyət, oldu := oxumaps2data()
	if !oldu {
		return
	}
	vəziyyət |= 0x01
	vəziyyət &^= 0x10
	if !yazmaps2Əmr(0x60) || !yazmaps2data(vəziyyət) {
		return
	}

	if !yazmaps2data(0xF4) {
		return
	}
	ack, oldu := oxumaps2data()
	if !oldu || ack != 0xFA {
		return
	}

}

func handleKlaviaturainterrupt(esp uint32) uint32 {
	if fəalKlaviaturadriver == nil {
		QapıOxumabyte(dataQapı_2)
		return esp
	}
	return fəalKlaviaturadriver.Handleinterrupt(esp)
}

const klaviaturaqueueBöyüklük = 64

var klaviaturaqueue [klaviaturaqueueBöyüklük]byte
var klaviaturaqueueOxuma uint8
var klaviaturaqueueYazma uint8
var solshift bool
var sağshift bool
var extendedscancode bool

func queueKlaviaturabyte(açar byte) {
	sonrakı := (klaviaturaqueueYazma + 1) % klaviaturaqueueBöyüklük
	if sonrakı == klaviaturaqueueOxuma {
		return
	}
	klaviaturaqueue[klaviaturaqueueYazma] = açar
	klaviaturaqueueYazma = sonrakı
}

func ProcesspendingKlaviaturaevents() {
	for klaviaturaqueueOxuma != klaviaturaqueueYazma {
		açar := klaviaturaqueue[klaviaturaqueueOxuma]
		klaviaturaqueueOxuma = (klaviaturaqueueOxuma + 1) % klaviaturaqueueBöyüklük
		Stdinputbyte(açar)
		if iKlaviaturaeventhandler != nil {
			iKlaviaturaeventhandler.OnAçardown(açar)
		}
	}
}

func scancodetobyte(scancode uint8) (byte, bool) {
	shift := solshift || sağshift

	if scancode >= 0x02 && scancode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[scancode-0x02], true
		}
		return "1234567890"[scancode-0x02], true
	}
	if scancode >= 0x10 && scancode <= 0x19 {
		açar := "qwertyuiop"[scancode-0x10]
		if shift {
			açar -= 'a' - 'A'
		}
		return açar, true
	}
	if scancode >= 0x1E && scancode <= 0x26 {
		açar := "asdfghjkl"[scancode-0x1E]
		if shift {
			açar -= 'a' - 'A'
		}
		return açar, true
	}
	if scancode >= 0x2C && scancode <= 0x32 {
		açar := "zxcvbnm"[scancode-0x2C]
		if shift {
			açar -= 'a' - 'A'
		}
		return açar, true
	}

	switch scancode {
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

func (self *TKlaviaturadriver) Handleinterrupt(esp uint32) uint32 {
	vəziyyət := QapıOxumabyte(əmrQapı_2)
	if (vəziyyət&0x01) == 0 || (vəziyyət&0x20) != 0 {
		return esp
	}

	scancode := QapıOxumabyte(dataQapı_2)
	if scancode == 0xE0 {
		extendedscancode = true
		return esp
	}
	if extendedscancode {
		extendedscancode = false
		return esp
	}

	released := (scancode & 0x80) != 0
	basecode := scancode & 0x7F
	if basecode == 0x2A {
		solshift = !released
		return esp
	}
	if basecode == 0x36 {
		sağshift = !released
		return esp
	}
	if released {
		return esp
	}

	if açar, oldu := scancodetobyte(basecode); oldu {
		queueKlaviaturabyte(açar)
	}

	return esp
}
