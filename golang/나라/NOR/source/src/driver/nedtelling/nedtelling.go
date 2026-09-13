package nedtelling

import . "unsafe"

import . "avbrudd"
import . "console"

type INedtellingHendelsehandler interface {
	Påtick()
}

var iNedtellingHendelsehandler INedtellingHendelsehandler

type TStandardNedtellingHendelsehandler struct {
}

func (selv *TStandardNedtellingHendelsehandler) Påtick() {
}

type TNedtellingdriver struct {
	TAvbruddhandler
}

var avbruddhandler func(*TNedtellingdriver, uint32) uint32

func (selv *TNedtellingdriver) Init(manager *TAvbruddmanager, tastaturHendelsehandler INedtellingHendelsehandler) {
	iNedtellingHendelsehandler = &TStandardNedtellingHendelsehandler{}
	if tastaturHendelsehandler != nil {
		iNedtellingHendelsehandler = tastaturHendelsehandler
	}

	avbruddhandler = (*TNedtellingdriver).HåndtakAvbrudd
	var address uintptr
	address = uintptr(Pointer(&avbruddhandler))

	selv.TAvbruddhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickAntall uint32 = 0

func (selv *TNedtellingdriver) HåndtakAvbrudd(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Skrivutxy(tickAntall, 3, 1)
	tickAntall++

	return esp
}
