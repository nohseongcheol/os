/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package timer

import . "unsafe"

import . "keskeytys"
import . "konsoli"

type ITimerTapahtumahandler interface {
	Päällätick()
}

var itimerTapahtumahandler ITimerTapahtumahandler

type TOletustimerTapahtumahandler struct {
}

func (itse *TOletustimerTapahtumahandler) Päällätick() {
}

type TTimerdriver struct {
	TKeskeytyshandler
}

var keskeytyshandler func(*TTimerdriver, uint32) uint32

func (itse *TTimerdriver) Init(manager *TKeskeytysmanager, näppäimistöTapahtumahandler ITimerTapahtumahandler) {
	itimerTapahtumahandler = &TOletustimerTapahtumahandler{}
	if näppäimistöTapahtumahandler != nil {
		itimerTapahtumahandler = näppäimistöTapahtumahandler
	}

	keskeytyshandler = (*TTimerdriver).KahvaKeskeytys
	var address uintptr
	address = uintptr(Pointer(&keskeytyshandler))

	itse.TKeskeytyshandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (itse *TTimerdriver) KahvaKeskeytys(esp uint32) uint32 {
	konsoli_2 := TKonsoli{}
	konsoli_2.MUnsignedinteger32Tulostaxy(tickcount, 3, 1)
	tickcount++

	return esp
}
