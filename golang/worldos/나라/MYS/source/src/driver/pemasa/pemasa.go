/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package pemasa

import . "unsafe"

import . "sampuk"
import . "console"

type IPemasaPeristiwahandler interface {
	Bukatick()
}

var iPemasaPeristiwahandler IPemasaPeristiwahandler

type TLalaiPemasaPeristiwahandler struct {
}

func (diri *TLalaiPemasaPeristiwahandler) Bukatick() {
}

type TPemasadriver struct {
	TSampukhandler
}

var sampukhandler func(*TPemasadriver, uint32) uint32

func (diri *TPemasadriver) Init(manager *TSampukmanager, papankekunciPeristiwahandler IPemasaPeristiwahandler) {
	iPemasaPeristiwahandler = &TLalaiPemasaPeristiwahandler{}
	if papankekunciPeristiwahandler != nil {
		iPemasaPeristiwahandler = papankekunciPeristiwahandler
	}

	sampukhandler = (*TPemasadriver).KendaliSampuk
	var address uintptr
	address = uintptr(Pointer(&sampukhandler))

	diri.TSampukhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (diri *TPemasadriver) KendaliSampuk(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Cetakxy(tickcount, 3, 1)
	tickcount++

	return esp
}
