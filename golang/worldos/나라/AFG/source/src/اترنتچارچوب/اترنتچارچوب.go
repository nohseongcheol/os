/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package اترنتچارچوب

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var اترنتconsole TConsole = TConsole{}

type Tاترنتچارچوبheaderbuffer struct {
	مقصدmacbe	[6]byte
	مبدأmacbe	[6]byte
	اترنتنوعbe	[2]byte
}

var چارچوبheaderاندازه int = 14

type Tاترنتچارچوبheader struct {
	مقصدmacbe	uint64
	مبدأmacbe	uint64
	اترنتنوعbe	uint16
}

func (خود *Tاترنتچارچوبheader) Init(buffer_2 Tاترنتچارچوبheaderbuffer) {
	خود.مقصدmacbe = (Aآرایهtounsignedinteger48(buffer_2.مقصدmacbe))
	خود.مبدأmacbe = (Aآرایهtounsignedinteger48(buffer_2.مبدأmacbe))
	خود.اترنتنوعbe = (Aآرایهtounsignedinteger16(buffer_2.اترنتنوعbe))

}
func (خود *Tاترنتچارچوبheader) Setbuffer(buffer_2 *Tاترنتچارچوبheaderbuffer) {
	buffer_2.مقصدmacbe = Unsignedinteger48toآرایه(Unsignedinteger48r(خود.مقصدmacbe))
	buffer_2.مبدأmacbe = Unsignedinteger48toآرایه(Unsignedinteger48r(خود.مبدأmacbe))
	buffer_2.اترنتنوعbe = Unsignedinteger16toآرایه(Unsignedinteger16r(خود.اترنتنوعbe))
}

type Iاترنتچارچوبhandler interface {
	Init(backend Tاترنتچارچوبprovider)
	Sethandler(handler Iاترنتچارچوبhandler, اترنتنوع uint16)
	Oاترنتچارچوبreceivewhen(datapointer uintptr, اندازه int) bool
	Send(مقصدmacbe uint64, datapointer uintptr, اندازه uint32)
	Sچارچوبsend(مقصدmacbe uint64, اترنتنوعbe uint16, datapointer uintptr, اندازه uint32)
	Providerget() Tاترنتچارچوبprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type Tاترنتچارچوبhandler struct {
}

var چارچوب Tاترنتچارچوبheader
var Backend Tاترنتچارچوبprovider
var handler_2 [65535]Iاترنتچارچوبhandler
var efhandler *Tاترنتچارچوبhandler = nil

func (خود *Tاترنتچارچوبhandler) Init(backend Tاترنتچارچوبprovider) {
	Backend = backend
}

func (خود *Tاترنتچارچوبhandler) Sethandler(handler Iاترنتچارچوبhandler, pاترنتنوع uint16) {
	handler_2[pاترنتنوع] = handler
}
func (خود *Tاترنتچارچوبhandler) Setbackend(backend Tاترنتچارچوبprovider) {
	Backend = backend
}
func (خود *Tاترنتچارچوبhandler) Getbackend() Tاترنتچارچوبprovider {
	return Backend
}
func (خود *Tاترنتچارچوبhandler) Oاترنتچارچوبreceivewhen(datapointer uintptr, اندازه int) bool {
	اترنتconsole.Mچاپ(([]byte)("OnEtherFrameReceived"))
	return false
}
func (خود *Tاترنتچارچوبhandler) Send(مقصدmacbe uint64, datapointer uintptr, اندازه uint32) {
	Backend.Sچارچوبsend(مقصدmacbe, چارچوب.اترنتنوعbe, datapointer, اندازه)
}
func (خود *Tاترنتچارچوبhandler) Sچارچوبsend(مقصدmacbe uint64, اترنتنوعbe uint16, datapointer uintptr, اندازه uint32) {
	Backend.Sچارچوبsend(مقصدmacbe, اترنتنوعbe, datapointer, اندازه)
}
func (خود *Tاترنتچارچوبhandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (خود *Tاترنتچارچوبhandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (خود *Tاترنتچارچوبhandler) Providerget() Tاترنتچارچوبprovider {
	return Backend
}

type Tاترنتچارچوبrawdatahandler struct {
	TRawdatahandler
}

var provider Tاترنتچارچوبprovider

func (خود *Tاترنتچارچوبrawdatahandler) Init(pprovider Tاترنتچارچوبprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (خود *Tاترنتچارچوبrawdatahandler) Oروشنrawdatareceive(datapointer uintptr, اندازه int) bool {
	return provider.Oروشنrawdatareceive(datapointer, اندازه)
}
func (خود *Tاترنتچارچوبrawdatahandler) Send(datapointer uintptr, اندازه uint32) {
	provider.Send(datapointer, اندازه)
}
func (خود *Tاترنتچارچوبrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (خود *Tاترنتچارچوبrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (خود *Tاترنتچارچوبrawdatahandler) Providerget() Tاترنتچارچوبprovider {
	return provider
}

type Tاترنتچارچوبprovider struct {
	شبکهcard	Tamdam79c973
	handler_2	[65565]Iاترنتچارچوبhandler
}

func (خود *Tاترنتچارچوبprovider) Init(backend Tamdam79c973) {

	خود.شبکهcard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		خود.handler_2[i] = nil
	}
}

var count uint16 = 0

func (خود *Tاترنتچارچوبprovider) Oروشنrawdatareceive(datapointer uintptr, اندازه int) bool {

	var buffer_2 *Tاترنتچارچوبheaderbuffer = (*Tاترنتچارچوبheaderbuffer)(Pointer(datapointer))
	var چارچوب Tاترنتچارچوبheader = Tاترنتچارچوبheader{}
	چارچوب.Init(*buffer_2)
	var reply bool = false

	if چارچوب.مقصدmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(چارچوب.مقصدmacbe) == خود.Getmacaddress() {
		if handler_2[چارچوب.اترنتنوعbe] != nil {
			اترنتconsole.Mچاپ(([]byte)("provider\n"))

			var pointer uintptr = uintptr(Pointer(datapointer)) + uintptr(چارچوبheaderاندازه)
			reply = handler_2[چارچوب.اترنتنوعbe].Oاترنتچارچوبreceivewhen(pointer, اندازه-چارچوبheaderاندازه)

		}
	}

	if reply {
		چارچوب.مقصدmacbe = چارچوب.مبدأmacbe
		چارچوب.مبدأmacbe = Unsignedinteger48r(خود.Getmacaddress())
		چارچوب.Setbuffer(buffer_2)

	}

	اترنتconsole.Mچاپxy(([]byte)("spro["), 0, 1)
	اترنتconsole.MUnsignedinteger64چاپ(چارچوب.مبدأmacbe)
	اترنتconsole.Mچاپ(([]byte)(":"))
	اترنتconsole.MUnsignedinteger64چاپ(چارچوب.مقصدmacbe)
	اترنتconsole.Mچاپ(([]byte)(":]["))
	اترنتconsole.MUnsignedinteger64چاپ(خود.Getmacaddress())
	اترنتconsole.Mچاپ(([]byte)(":"))
	اترنتconsole.MUnsignedinteger16چاپ(چارچوب.اترنتنوعbe)
	اترنتconsole.Mچاپ(([]byte)("]"))

	return reply

}
func (خود *Tاترنتچارچوبprovider) Send(datapointer uintptr, اندازه uint32) {
	خود.شبکهcard.Send(datapointer, اندازه)
}
func (خود *Tاترنتچارچوبprovider) Sچارچوبsend(مقصدmacbe uint64, اترنتنوعbe uint16, datapointer uintptr, اندازه uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *Tاترنتچارچوبheaderbuffer = (*Tاترنتچارچوبheaderbuffer)(Pointer(&buffer2_2))

	var چارچوب Tاترنتچارچوبheader = Tاترنتچارچوبheader{}
	چارچوب.Init(*buffer_2)

	چارچوب.مقصدmacbe = Unsignedinteger48r(مقصدmacbe)
	چارچوب.مبدأmacbe = Unsignedinteger48r(خود.شبکهcard.Getmacaddress())
	چارچوب.اترنتنوعbe = Unsignedinteger16r(اترنتنوعbe)

	چارچوب.Setbuffer(buffer_2)
	var مبدأ_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	var i uint32 = 0
	for i = 0; i < اندازه; i++ {
		buffer2_2[uint32(چارچوبheaderاندازه)+i] = مبدأ_2[i]

	}

	var pointer uintptr = uintptr(Pointer(&buffer2_2))

	خود.شبکهcard.Send(pointer, اندازه+uint32(چارچوبheaderاندازه))

}
func (خود *Tاترنتچارچوبprovider) Getmacaddress() uint64 {
	return خود.شبکهcard.Getmacaddress()
}
func (خود *Tاترنتچارچوبprovider) Getipaddress() uint64 {
	return خود.شبکهcard.Getipaddress()
}
