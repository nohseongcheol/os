/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package πληκτρολόγιο

import . "unsafe"

import . "θύρα"
import . "διακοπή"
import . "console"

type IΠοντίκιΣυμβάνhandler interface {
	ΕνεργήΠοντίκιΚάτω(κουμπί int8)
	ΕνεργήΠοντίκιΠάνω(κουμπί int8)
	ΕνεργήΠοντίκιΜετακίνηση(x int8, y int8)
}

var iΠοντίκιΣυμβάνhandler IΠοντίκιΣυμβάνhandler

type TΠροεπιλογήΠοντίκιΣυμβάνhandler struct {
}

var console_2 TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xΘέση int16 = 0
var yΘέση int16 = 0

func (self TΠροεπιλογήΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΚάτω(κουμπί int8) {
	buffer := []byte("+")
	console_2.MΕκτύπωσηxy(buffer, uint16(previousx), uint16(previousy))
}
func (self TΠροεπιλογήΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΠάνω(κουμπί int8)	{}
func (self TΠροεπιλογήΠοντίκιΣυμβάνhandler) ΕνεργήΠοντίκιΜετακίνηση(x int8, y int8) {

	xΘέση += int16(x)
	if xΘέση < 0 {
		xΘέση = 0
	}
	if xΘέση >= 80 {
		xΘέση = 79
	}

	yΘέση -= int16(y)

	if yΘέση < 0 {
		yΘέση = 0
	}
	if yΘέση >= 25 {
		yΘέση = 24
	}

	buffer := []byte(" ")
	console_2.MΕκτύπωσηxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	console_2.MΕκτύπωσηxy(buffer, uint16(xΘέση), uint16(yΘέση))

	previousx = xΘέση
	previousy = yΘέση
}

type TΠοντίκιdriver struct {
	TΔιακοπήhandler
}

var ενεργόΠοντίκιdriver *TΠοντίκιdriver
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

func αποστολήΠοντίκιΕντολή(τιμή uint8) bool {
	if !εγγραφήps2Εντολή(0xD4) || !εγγραφήps2data(τιμή) {
		return false
	}
	ack, εντάξει := ανάγνωσηps2data()
	return εντάξει && ack == 0xFA
}

func (self *TΠοντίκιdriver) Initdriver(manager *TΔιακοπήmanager, ποντίκιΣυμβάνhandler IΠοντίκιΣυμβάνhandler) {

	iΠοντίκιΣυμβάνhandler = TΠροεπιλογήΠοντίκιΣυμβάνhandler{}

	if ποντίκιΣυμβάνhandler != nil {
		iΠοντίκιΣυμβάνhandler = ποντίκιΣυμβάνhandler
	}

	ενεργόΠοντίκιdriver = self
	διακοπήhandler = χειρολαβήΠοντίκιΔιακοπή
	var address uintptr
	address = uintptr(Pointer(&διακοπήhandler))
	self.Init(0x2C, uintptr(Pointer(manager)), address)

	for i := 0; i < 32 && (ΘύραΑνάγνωσηbyte(εντολήΘύρα_2)&0x01) != 0; i++ {
		ΘύραΑνάγνωσηbyte(dataΘύρα_2)
	}

	if !εγγραφήps2Εντολή(0xA8) || !εγγραφήps2Εντολή(0x20) {
		return
	}
	κατάσταση, εντάξει := ανάγνωσηps2data()
	if !εντάξει {
		return
	}
	κατάσταση |= 0x02
	κατάσταση &^= 0x20
	if !εγγραφήps2Εντολή(0x60) || !εγγραφήps2data(κατάσταση) {
		return
	}

	if !αποστολήΠοντίκιΕντολή(0xF6) || !αποστολήΠοντίκιΕντολή(0xF4) {
		return
	}
	offset = 0

}

func χειρολαβήΠοντίκιΔιακοπή(esp uint32) uint32 {
	if ενεργόΠοντίκιdriver == nil {
		ΘύραΑνάγνωσηbyte(dataΘύρα_2)
		return esp
	}
	return ενεργόΠοντίκιdriver.ΧειρολαβήΔιακοπή(esp)
}

var count uint8 = 0
var buffer_2 [3]int8
var offset uint8 = 0

var κουμπί_2 int8
var pendingx int16
var pendingy int16
var pendingΚουμπί int8
var pendingΠοντίκιΣυμβάν bool

func (self *TΠοντίκιdriver) ΧειρολαβήΔιακοπή(esp uint32) uint32 {
	κατάσταση := ΘύραΑνάγνωσηbyte(εντολήΘύρα_2)
	if (κατάσταση&0x01) == 0 || (κατάσταση&0x20) == 0 {
		return esp
	}

	data := ΘύραΑνάγνωσηbyte(dataΘύρα_2)

	if offset == 0 && (data&0x08) == 0 {
		return esp
	}
	buffer_2[offset] = int8(data)
	offset = (offset + 1) % 3
	if offset == 0 {
		packetΚατάσταση := uint8(buffer_2[0])

		if (packetΚατάσταση & 0xC0) == 0 {
			pendingx += int16(buffer_2[1])
			pendingy += int16(buffer_2[2])
			if pendingx > 127 {
				pendingx = 127
			} else if pendingx < -127 {
				pendingx = -127
			}
			if pendingy > 127 {
				pendingy = 127
			} else if pendingy < -127 {
				pendingy = -127
			}
		}
		pendingΚουμπί = int8(packetΚατάσταση & 0x07)
		pendingΠοντίκιΣυμβάν = true
	}

	return esp

}

func ΔιεργασίαpendingΠοντίκιΓεγονότα() {
	if iΠοντίκιΣυμβάνhandler == nil {
		return
	}

	Διακοπήdeactive()
	if !pendingΠοντίκιΣυμβάν {
		ΔιακοπήΕνεργό()
		return
	}
	x := int8(pendingx)
	y := int8(pendingy)
	νέοΚουμπί := pendingΚουμπί
	oldΚουμπί := κουμπί_2

	pendingx = 0
	pendingy = 0
	pendingΠοντίκιΣυμβάν = false
	ΔιακοπήΕνεργό()

	if x != 0 || y != 0 {
		iΠοντίκιΣυμβάνhandler.ΕνεργήΠοντίκιΜετακίνηση(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		μάσκα := int8(0x1 << i)
		if (νέοΚουμπί & μάσκα) != (oldΚουμπί & μάσκα) {
			if (νέοΚουμπί & μάσκα) != 0 {
				iΠοντίκιΣυμβάνhandler.ΕνεργήΠοντίκιΚάτω(int8(i + 1))
			} else {
				iΠοντίκιΣυμβάνhandler.ΕνεργήΠοντίκιΠάνω(int8(i + 1))
			}
		}
	}
	κουμπί_2 = νέοΚουμπί
}
