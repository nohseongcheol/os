package صفحهکلید

import . "unsafe"

import . "درگاه"
import . "interrupt"

import . "console"
import . "سیستمcall"

type Iصفحهکلیدeventhandler interface {
	Oروشنkeyپایین(key byte)
	Oروشنkeyبالا(key byte)
}

var iصفحهکلیدeventhandler Iصفحهکلیدeventhandler
var defaultصفحهکلیدeventhandler TDefaultصفحهکلیدeventhandler

type TDefaultصفحهکلیدeventhandler struct {
}

func (خود *TDefaultصفحهکلیدeventhandler) Oروشنkeyپایین(key byte) {
	hex := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = hex[((key >> 4) & 0xF)]
	buffer[18] = hex[key&0xF]

	console_2 := TConsole{}
	console_2.Mچاپ(buffer)

}
func (خود *TDefaultصفحهکلیدeventhandler) Oروشنkeyبالا(key byte) {
}

type Tصفحهکلیدdriver struct {
	TInterrupthandler
}

var فعالصفحهکلیدdriver *Tصفحهکلیدdriver
var interrupthandler func(uint32) uint32

var dataدرگاه_2 uint16 = 0x60
var فرماندرگاه_2 uint16 = 0x64

const ps2انتظارlimit = 100000

func انتظارps2ورودیempty() bool {
	for i := 0; i < ps2انتظارlimit; i++ {
		if (Pدرگاهخواندنbyte(فرماندرگاه_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func انتظارps2خروجیfull() bool {
	for i := 0; i < ps2انتظارlimit; i++ {
		if (Pدرگاهخواندنbyte(فرماندرگاه_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func نوشتنps2فرمان(مقدار uint8) bool {
	if !انتظارps2ورودیempty() {
		return false
	}
	Pدرگاهنوشتنbyte(فرماندرگاه_2, مقدار)
	return true
}

func نوشتنps2data(مقدار uint8) bool {
	if !انتظارps2ورودیempty() {
		return false
	}
	Pدرگاهنوشتنbyte(dataدرگاه_2, مقدار)
	return true
}

func خواندنps2data() (uint8, bool) {
	if !انتظارps2خروجیfull() {
		return 0, false
	}
	return Pدرگاهخواندنbyte(dataدرگاه_2), true
}

func (خود *Tصفحهکلیدdriver) Initdriver(manager *TInterruptmanager, صفحهکلیدeventhandler Iصفحهکلیدeventhandler) {

	iصفحهکلیدeventhandler = &defaultصفحهکلیدeventhandler
	if صفحهکلیدeventhandler != nil {
		iصفحهکلیدeventhandler = صفحهکلیدeventhandler
	}

	فعالصفحهکلیدdriver = خود
	interrupthandler = handleصفحهکلیدinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	خود.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (Pدرگاهخواندنbyte(فرماندرگاه_2)&0x01) != 0; i++ {
		Pدرگاهخواندنbyte(dataدرگاه_2)
	}

	if !نوشتنps2فرمان(0xAE) || !نوشتنps2فرمان(0x20) {
		return
	}
	وضعیت, تأیید := خواندنps2data()
	if !تأیید {
		return
	}
	وضعیت |= 0x01
	وضعیت &^= 0x10
	if !نوشتنps2فرمان(0x60) || !نوشتنps2data(وضعیت) {
		return
	}

	if !نوشتنps2data(0xF4) {
		return
	}
	ack, تأیید := خواندنps2data()
	if !تأیید || ack != 0xFA {
		return
	}

}

func handleصفحهکلیدinterrupt(esp uint32) uint32 {
	if فعالصفحهکلیدdriver == nil {
		Pدرگاهخواندنbyte(dataدرگاه_2)
		return esp
	}
	return فعالصفحهکلیدdriver.Handleinterrupt(esp)
}

const صفحهکلیدqueueاندازه = 64

var صفحهکلیدqueue [صفحهکلیدqueueاندازه]byte
var صفحهکلیدqueueخواندن uint8
var صفحهکلیدqueueنوشتن uint8
var چپتبدیل bool
var راستتبدیل bool
var extendedپویشcode bool

func queueصفحهکلیدbyte(key byte) {
	بعدی := (صفحهکلیدqueueنوشتن + 1) % صفحهکلیدqueueاندازه
	if بعدی == صفحهکلیدqueueخواندن {
		return
	}
	صفحهکلیدqueue[صفحهکلیدqueueنوشتن] = key
	صفحهکلیدqueueنوشتن = بعدی
}

func Processpendingصفحهکلیدevents() {
	for صفحهکلیدqueueخواندن != صفحهکلیدqueueنوشتن {
		key := صفحهکلیدqueue[صفحهکلیدqueueخواندن]
		صفحهکلیدqueueخواندن = (صفحهکلیدqueueخواندن + 1) % صفحهکلیدqueueاندازه
		Stdinputbyte(key)
		if iصفحهکلیدeventhandler != nil {
			iصفحهکلیدeventhandler.Oروشنkeyپایین(key)
		}
	}
}

func پویشcodetobyte(پویشcode uint8) (byte, bool) {
	تبدیل := چپتبدیل || راستتبدیل

	if پویشcode >= 0x02 && پویشcode <= 0x0B {
		if تبدیل {
			return "!@#$%^&*()"[پویشcode-0x02], true
		}
		return "1234567890"[پویشcode-0x02], true
	}
	if پویشcode >= 0x10 && پویشcode <= 0x19 {
		key := "qwertyuiop"[پویشcode-0x10]
		if تبدیل {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if پویشcode >= 0x1E && پویشcode <= 0x26 {
		key := "asdfghjkl"[پویشcode-0x1E]
		if تبدیل {
			key -= 'a' - 'A'
		}
		return key, true
	}
	if پویشcode >= 0x2C && پویشcode <= 0x32 {
		key := "zxcvbnm"[پویشcode-0x2C]
		if تبدیل {
			key -= 'a' - 'A'
		}
		return key, true
	}

	switch پویشcode {
	case 0x0C:
		if تبدیل {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if تبدیل {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if تبدیل {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if تبدیل {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if تبدیل {
			return ':', true
		}
		return ';', true
	case 0x28:
		if تبدیل {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if تبدیل {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if تبدیل {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if تبدیل {
			return '<', true
		}
		return ',', true
	case 0x34:
		if تبدیل {
			return '>', true
		}
		return '.', true
	case 0x35:
		if تبدیل {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (خود *Tصفحهکلیدdriver) Handleinterrupt(esp uint32) uint32 {
	وضعیت := Pدرگاهخواندنbyte(فرماندرگاه_2)
	if (وضعیت&0x01) == 0 || (وضعیت&0x20) != 0 {
		return esp
	}

	پویشcode := Pدرگاهخواندنbyte(dataدرگاه_2)
	if پویشcode == 0xE0 {
		extendedپویشcode = true
		return esp
	}
	if extendedپویشcode {
		extendedپویشcode = false
		return esp
	}

	released := (پویشcode & 0x80) != 0
	basecode := پویشcode & 0x7F
	if basecode == 0x2A {
		چپتبدیل = !released
		return esp
	}
	if basecode == 0x36 {
		راستتبدیل = !released
		return esp
	}
	if released {
		return esp
	}

	if key, تأیید := پویشcodetobyte(basecode); تأیید {
		queueصفحهکلیدbyte(key)
	}

	return esp
}
