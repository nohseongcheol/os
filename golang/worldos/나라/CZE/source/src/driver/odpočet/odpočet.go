/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package odpočet

import . "unsafe"

import . "přerušení"
import . "konzole"

type IOdpočetUdálostihandler interface {
	Zapnutotick()
}

var iOdpočetUdálostihandler IOdpočetUdálostihandler

type TVýchozíOdpočetUdálostihandler struct {
}

func (self *TVýchozíOdpočetUdálostihandler) Zapnutotick() {
}

type TOdpočetdriver struct {
	TPřerušeníhandler
}

var přerušeníhandler func(*TOdpočetdriver, uint32) uint32

func (self *TOdpočetdriver) Init(manager *TPřerušenímanager, klávesniceUdálostihandler IOdpočetUdálostihandler) {
	iOdpočetUdálostihandler = &TVýchozíOdpočetUdálostihandler{}
	if klávesniceUdálostihandler != nil {
		iOdpočetUdálostihandler = klávesniceUdálostihandler
	}

	přerušeníhandler = (*TOdpočetdriver).ÚchytkaPřerušení
	var adresa uintptr
	adresa = uintptr(Pointer(&přerušeníhandler))

	self.TPřerušeníhandler.Init(0x20, uintptr(Pointer(manager)), adresa)

}

var tickPočet uint32 = 0

func (self *TOdpočetdriver) ÚchytkaPřerušení(esp uint32) uint32 {
	konzole_2 := TKonzole{}
	konzole_2.MUnsignedinteger32Tisknoutxy(tickPočet, 3, 1)
	tickPočet++

	return esp
}
