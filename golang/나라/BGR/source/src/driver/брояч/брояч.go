/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package брояч

import . "unsafe"

import . "прекъсване"
import . "console"

type IБроячСъбитиеhandler interface {
	Вклtick()
}

var iБроячСъбитиеhandler IБроячСъбитиеhandler

type TПоподразбиранеБроячСъбитиеhandler struct {
}

func (себеси *TПоподразбиранеБроячСъбитиеhandler) Вклtick() {
}

type TБроячdriver struct {
	TПрекъсванеhandler
}

var прекъсванеhandler func(*TБроячdriver, uint32) uint32

func (себеси *TБроячdriver) Init(manager *TПрекъсванеmanager, клавиатураСъбитиеhandler IБроячСъбитиеhandler) {
	iБроячСъбитиеhandler = &TПоподразбиранеБроячСъбитиеhandler{}
	if клавиатураСъбитиеhandler != nil {
		iБроячСъбитиеhandler = клавиатураСъбитиеhandler
	}

	прекъсванеhandler = (*TБроячdriver).РъкохваткаПрекъсване
	var address uintptr
	address = uintptr(Pointer(&прекъсванеhandler))

	себеси.TПрекъсванеhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (себеси *TБроячdriver) РъкохваткаПрекъсване(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Печатxy(tickcount, 3, 1)
	tickcount++

	return esp
}
