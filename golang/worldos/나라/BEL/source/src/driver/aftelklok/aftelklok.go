/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package aftelklok

import . "unsafe"

import . "interrupt"
import . "console"

type IAftelklokGebeurtenishandler interface {
	Aantick()
}

var iAftelklokGebeurtenishandler IAftelklokGebeurtenishandler

type TStandaardAftelklokGebeurtenishandler struct {
}

func (zelf *TStandaardAftelklokGebeurtenishandler) Aantick() {
}

type TAftelklokdriver struct {
	TInterrupthandler
}

var interrupthandler func(*TAftelklokdriver, uint32) uint32

func (zelf *TAftelklokdriver) Init(manager *TInterruptmanager, toetsenbordGebeurtenishandler IAftelklokGebeurtenishandler) {
	iAftelklokGebeurtenishandler = &TStandaardAftelklokGebeurtenishandler{}
	if toetsenbordGebeurtenishandler != nil {
		iAftelklokGebeurtenishandler = toetsenbordGebeurtenishandler
	}

	interrupthandler = (*TAftelklokdriver).Handgreepinterrupt
	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	zelf.TInterrupthandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickAantal uint32 = 0

func (zelf *TAftelklokdriver) Handgreepinterrupt(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Afdrukkenxy(tickAantal, 3, 1)
	tickAantal++

	return esp
}
