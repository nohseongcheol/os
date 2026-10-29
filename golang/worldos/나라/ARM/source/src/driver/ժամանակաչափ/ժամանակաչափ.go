/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ժամանակաչափ

import . "unsafe"

import . "ընդհատել"
import . "console"

type IԺամանակաչափeventhandler interface {
	Միացնելtick()
}

var iԺամանակաչափeventhandler IԺամանակաչափeventhandler

type TՀիմնականԺամանակաչափeventhandler struct {
}

func (ինքնուրույն *TՀիմնականԺամանակաչափeventhandler) Միացնելtick() {
}

type TԺամանակաչափdriver struct {
	TԸնդհատելhandler
}

var ընդհատելhandler func(*TԺամանակաչափdriver, uint32) uint32

func (ինքնուրույն *TԺամանակաչափdriver) Init(manager *TԸնդհատելmanager, ստեղնաշարeventhandler IԺամանակաչափeventhandler) {
	iԺամանակաչափeventhandler = &TՀիմնականԺամանակաչափeventhandler{}
	if ստեղնաշարeventhandler != nil {
		iԺամանակաչափeventhandler = ստեղնաշարeventhandler
	}

	ընդհատելhandler = (*TԺամանակաչափdriver).HandleԸնդհատել
	var address uintptr
	address = uintptr(Pointer(&ընդհատելhandler))

	ինքնուրույն.TԸնդհատելhandler.Init(0x20, uintptr(Pointer(manager)), address)

}

var tickcount uint32 = 0

func (ինքնուրույն *TԺամանակաչափdriver) HandleԸնդհատել(esp uint32) uint32 {
	console_2 := TConsole{}
	console_2.MUnsignedinteger32Տպելxy(tickcount, 3, 1)
	tickcount++

	return esp
}
