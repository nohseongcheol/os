/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package χρονόμετρο

import . "unsafe"

import . "διακοπή"
import . "console"

type IΧρονόμετροΣυμβάνhandler interface {
	Ενεργήtick()
}

var iΧρονόμετροΣυμβάνhandler IΧρονόμετροΣυμβάνhandler

type TΠροεπιλογήΧρονόμετροΣυμβάνhandler struct {
}

func (self *TΠροεπιλογήΧρονόμετροΣυμβάνhandler) Ενεργήtick() {
}

type TΧρονόμετροdriver struct {
	TΔιακοπήhandler
}

var διακοπήhandler func(*TΧρονόμετροdriver, uint32) uint32

func (self *TΧρονόμετροdriver) Init(manager *TΔιακοπήmanager, πληκτρολόγιοΣυμβάνhandler IΧρονόμετροΣυμβάνhandler) {
	iΧρονόμετροΣυμβάνhandler = &TΠροεπιλογήΧρονόμετροΣυμβάνhandler{}
	if πληκτρολόγιοΣυμβάνhandler != nil {
		iΧρονόμετροΣυμβάνhandler = πληκτρολόγιοΣυμβάνhandler
	}

	διακοπήhandler = (*TΧρονόμετροdriver).ΧειρολαβήΔιακοπή
	var address uintptr
	address = uintptr(Pointer(&διακοπήhandler))

	self.TΔιακοπήhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (self *TΧρονόμετροdriver) ΧειρολαβήΔιακοπή(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Εκτύπωσηxy(tickcount, 3, 1)
	tickcount++

	return esp
}
