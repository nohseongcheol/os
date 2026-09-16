/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package πληκτρολόγιο

import . "unsafe"

import . "θύρα"
import . "διακοπή"

import . "console"
import . "σύστημαcall"

type IΠληκτρολόγιοΣυμβάνhandler interface {
	ΕνεργήΚλειδίΚάτω(κλειδί byte)
	ΕνεργήΚλειδίΠάνω(κλειδί byte)
}

var iΠληκτρολόγιοΣυμβάνhandler IΠληκτρολόγιοΣυμβάνhandler
var προεπιλογήΠληκτρολόγιοΣυμβάνhandler TΠροεπιλογήΠληκτρολόγιοΣυμβάνhandler

type TΠροεπιλογήΠληκτρολόγιοΣυμβάνhandler struct {
}

func (self *TΠροεπιλογήΠληκτρολόγιοΣυμβάνhandler) ΕνεργήΚλειδίΚάτω(κλειδί byte) {
	δεκαεξαδικό := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = δεκαεξαδικό[((κλειδί >> 4) & 0xF)]
	buffer[18] = δεκαεξαδικό[κλειδί&0xF]

	console_2 := TConsole{}
	console_2.MΕκτύπωση(buffer)

}
func (self *TΠροεπιλογήΠληκτρολόγιοΣυμβάνhandler) ΕνεργήΚλειδίΠάνω(κλειδί byte) {
}

type TΠληκτρολόγιοdriver struct {
	TΔιακοπήhandler
}

var ενεργόΠληκτρολόγιοdriver *TΠληκτρολόγιοdriver
var διακοπήhandler func(uint32) uint32

var dataΘύρα_2 uint16 = 0x60
var εντολήΘύρα_2 uint16 = 0x64

const ps2ΑναμονήΌριο = 100000

func αναμονήps2ΕίσοδοςΚενή() bool {
	for i := 0; i < ps2ΑναμονήΌριο; i++ {
		if (ΘύραΑνάγνωσηbyte(εντολήΘύρα_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func αναμονήps2ΈξοδοςΠλήρες() bool {
	for i := 0; i < ps2ΑναμονήΌριο; i++ {
		if (ΘύραΑνάγνωσηbyte(εντολήΘύρα_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func εγγραφήps2Εντολή(τιμή uint8) bool {
	if !αναμονήps2ΕίσοδοςΚενή() {
		return false
	}
	ΘύραΕγγραφήbyte(εντολήΘύρα_2, τιμή)
	return true
}

func εγγραφήps2data(τιμή uint8) bool {
	if !αναμονήps2ΕίσοδοςΚενή() {
		return false
	}
	ΘύραΕγγραφήbyte(dataΘύρα_2, τιμή)
	return true
}

func ανάγνωσηps2data() (uint8, bool) {
	if !αναμονήps2ΈξοδοςΠλήρες() {
		return 0, false
	}
	return ΘύραΑνάγνωσηbyte(dataΘύρα_2), true
}

func (self *TΠληκτρολόγιοdriver) Initdriver(manager *TΔιακοπήmanager, πληκτρολόγιοΣυμβάνhandler IΠληκτρολόγιοΣυμβάνhandler) {

	iΠληκτρολόγιοΣυμβάνhandler = &προεπιλογήΠληκτρολόγιοΣυμβάνhandler
	if πληκτρολόγιοΣυμβάνhandler != nil {
		iΠληκτρολόγιοΣυμβάνhandler = πληκτρολόγιοΣυμβάνhandler
	}

	ενεργόΠληκτρολόγιοdriver = self
	διακοπήhandler = χειρολαβήΠληκτρολόγιοΔιακοπή
	var address uintptr
	address = uintptr(Pointer(&διακοπήhandler))

	self.Init(0x21, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ΘύραΑνάγνωσηbyte(εντολήΘύρα_2)&0x01) != 0; i++ {
		ΘύραΑνάγνωσηbyte(dataΘύρα_2)
	}

	if !εγγραφήps2Εντολή(0xAE) || !εγγραφήps2Εντολή(0x20) {
		return
	}
	κατάσταση, εντάξει := ανάγνωσηps2data()
	if !εντάξει {
		return
	}
	κατάσταση |= 0x01
	κατάσταση &^= 0x10
	if !εγγραφήps2Εντολή(0x60) || !εγγραφήps2data(κατάσταση) {
		return
	}

	if !εγγραφήps2data(0xF4) {
		return
	}
	ack, εντάξει := ανάγνωσηps2data()
	if !εντάξει || ack != 0xFA {
		return
	}

}

func χειρολαβήΠληκτρολόγιοΔιακοπή(esp uint32) uint32 {
	if ενεργόΠληκτρολόγιοdriver == nil {
		ΘύραΑνάγνωσηbyte(dataΘύρα_2)
		return esp
	}
	return ενεργόΠληκτρολόγιοdriver.ΧειρολαβήΔιακοπή(esp)
}

const πληκτρολόγιοqueueΜέγεθος = 64

var πληκτρολόγιοqueue [πληκτρολόγιοqueueΜέγεθος]byte
var πληκτρολόγιοqueueΑνάγνωση uint8
var πληκτρολόγιοqueueΕγγραφή uint8
var αριστεράshift bool
var δεξιάshift bool
var extendedΣάρωσηcode bool

func queueΠληκτρολόγιοbyte(κλειδί byte) {
	επόμενο := (πληκτρολόγιοqueueΕγγραφή + 1) % πληκτρολόγιοqueueΜέγεθος
	if επόμενο == πληκτρολόγιοqueueΑνάγνωση {
		return
	}
	πληκτρολόγιοqueue[πληκτρολόγιοqueueΕγγραφή] = κλειδί
	πληκτρολόγιοqueueΕγγραφή = επόμενο
}

func ΔιεργασίαpendingΠληκτρολόγιοΓεγονότα() {
	for πληκτρολόγιοqueueΑνάγνωση != πληκτρολόγιοqueueΕγγραφή {
		κλειδί := πληκτρολόγιοqueue[πληκτρολόγιοqueueΑνάγνωση]
		πληκτρολόγιοqueueΑνάγνωση = (πληκτρολόγιοqueueΑνάγνωση + 1) % πληκτρολόγιοqueueΜέγεθος
		Stdinputbyte(κλειδί)
		if iΠληκτρολόγιοΣυμβάνhandler != nil {
			iΠληκτρολόγιοΣυμβάνhandler.ΕνεργήΚλειδίΚάτω(κλειδί)
		}
	}
}

func σάρωσηcodetobyte(σάρωσηcode uint8) (byte, bool) {
	shift := αριστεράshift || δεξιάshift

	if σάρωσηcode >= 0x02 && σάρωσηcode <= 0x0B {
		if shift {
			return "!@#$%^&*()"[σάρωσηcode-0x02], true
		}
		return "1234567890"[σάρωσηcode-0x02], true
	}
	if σάρωσηcode >= 0x10 && σάρωσηcode <= 0x19 {
		κλειδί := "qwertyuiop"[σάρωσηcode-0x10]
		if shift {
			κλειδί -= 'a' - 'A'
		}
		return κλειδί, true
	}
	if σάρωσηcode >= 0x1E && σάρωσηcode <= 0x26 {
		κλειδί := "asdfghjkl"[σάρωσηcode-0x1E]
		if shift {
			κλειδί -= 'a' - 'A'
		}
		return κλειδί, true
	}
	if σάρωσηcode >= 0x2C && σάρωσηcode <= 0x32 {
		κλειδί := "zxcvbnm"[σάρωσηcode-0x2C]
		if shift {
			κλειδί -= 'a' - 'A'
		}
		return κλειδί, true
	}

	switch σάρωσηcode {
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

func (self *TΠληκτρολόγιοdriver) ΧειρολαβήΔιακοπή(esp uint32) uint32 {
	κατάσταση := ΘύραΑνάγνωσηbyte(εντολήΘύρα_2)
	if (κατάσταση&0x01) == 0 || (κατάσταση&0x20) != 0 {
		return esp
	}

	σάρωσηcode := ΘύραΑνάγνωσηbyte(dataΘύρα_2)
	if σάρωσηcode == 0xE0 {
		extendedΣάρωσηcode = true
		return esp
	}
	if extendedΣάρωσηcode {
		extendedΣάρωσηcode = false
		return esp
	}

	released := (σάρωσηcode & 0x80) != 0
	basecode := σάρωσηcode & 0x7F
	if basecode == 0x2A {
		αριστεράshift = !released
		return esp
	}
	if basecode == 0x36 {
		δεξιάshift = !released
		return esp
	}
	if released {
		return esp
	}

	if κλειδί, εντάξει := σάρωσηcodetobyte(basecode); εντάξει {
		queueΠληκτρολόγιοbyte(κλειδί)
	}

	return esp
}
