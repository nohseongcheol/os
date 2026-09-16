/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ethernetRamme

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetRammeheaderbuffer struct {
	destinationmacbe	[6]byte
	kildemacbe		[6]byte
	ethernettypebe		[2]byte
}

var rammeheaderStørrelse int = 14

type TEthernetRammeheader struct {
	destinationmacbe	uint64
	kildemacbe		uint64
	ethernettypebe		uint16
}

func (selv *TEthernetRammeheader) Init(buffer_2 TEthernetRammeheaderbuffer) {
	selv.destinationmacbe = (Tabeltounsignedinteger48(buffer_2.destinationmacbe))
	selv.kildemacbe = (Tabeltounsignedinteger48(buffer_2.kildemacbe))
	selv.ethernettypebe = (Tabeltounsignedinteger16(buffer_2.ethernettypebe))

}
func (selv *TEthernetRammeheader) Satbuffer(buffer_2 *TEthernetRammeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toTabel(Unsignedinteger48r(selv.destinationmacbe))
	buffer_2.kildemacbe = Unsignedinteger48toTabel(Unsignedinteger48r(selv.kildemacbe))
	buffer_2.ethernettypebe = Unsignedinteger16toTabel(Unsignedinteger16r(selv.ethernettypebe))
}

type IEthernetRammehandler interface {
	Init(backend TEthernetRammeprovider)
	Sathandler(handler IEthernetRammehandler, ethernettype uint16)
	EthernetRammereceivewhen(dataMarkør uintptr, størrelse int) bool
	Send(destinationmacbe uint64, dataMarkør uintptr, størrelse uint32)
	Rammesend(destinationmacbe uint64, ethernettypebe uint16, dataMarkør uintptr, størrelse uint32)
	Providerget() TEthernetRammeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetRammehandler struct {
}

var ramme TEthernetRammeheader
var Backend TEthernetRammeprovider
var handler_2 [65535]IEthernetRammehandler
var efhandler *TEthernetRammehandler = nil

func (selv *TEthernetRammehandler) Init(backend TEthernetRammeprovider) {
	Backend = backend
}

func (selv *TEthernetRammehandler) Sathandler(handler IEthernetRammehandler, pethernettype uint16) {
	handler_2[pethernettype] = handler
}
func (selv *TEthernetRammehandler) Satbackend(backend TEthernetRammeprovider) {
	Backend = backend
}
func (selv *TEthernetRammehandler) Getbackend() TEthernetRammeprovider {
	return Backend
}
func (selv *TEthernetRammehandler) EthernetRammereceivewhen(dataMarkør uintptr, størrelse int) bool {
	ethernetconsole.MUdskriv(([]byte)("OnEtherFrameReceived"))
	return false
}
func (selv *TEthernetRammehandler) Send(destinationmacbe uint64, dataMarkør uintptr, størrelse uint32) {
	Backend.Rammesend(destinationmacbe, ramme.ethernettypebe, dataMarkør, størrelse)
}
func (selv *TEthernetRammehandler) Rammesend(destinationmacbe uint64, ethernettypebe uint16, dataMarkør uintptr, størrelse uint32) {
	Backend.Rammesend(destinationmacbe, ethernettypebe, dataMarkør, størrelse)
}
func (selv *TEthernetRammehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (selv *TEthernetRammehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (selv *TEthernetRammehandler) Providerget() TEthernetRammeprovider {
	return Backend
}

type TEthernetRammerawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetRammeprovider

func (selv *TEthernetRammerawdatahandler) Init(pprovider TEthernetRammeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (selv *TEthernetRammerawdatahandler) Tændtrawdatareceive(dataMarkør uintptr, størrelse int) bool {
	return provider.Tændtrawdatareceive(dataMarkør, størrelse)
}
func (selv *TEthernetRammerawdatahandler) Send(dataMarkør uintptr, størrelse uint32) {
	provider.Send(dataMarkør, størrelse)
}
func (selv *TEthernetRammerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (selv *TEthernetRammerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (selv *TEthernetRammerawdatahandler) Providerget() TEthernetRammeprovider {
	return provider
}

type TEthernetRammeprovider struct {
	netværkKortspil	Tamdam79c973
	handler_2	[65565]IEthernetRammehandler
}

func (selv *TEthernetRammeprovider) Init(backend Tamdam79c973) {

	selv.netværkKortspil = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		selv.handler_2[i] = nil
	}
}

var antal uint16 = 0

func (selv *TEthernetRammeprovider) Tændtrawdatareceive(dataMarkør uintptr, størrelse int) bool {

	var buffer_2 *TEthernetRammeheaderbuffer = (*TEthernetRammeheaderbuffer)(Pointer(dataMarkør))
	var ramme TEthernetRammeheader = TEthernetRammeheader{}
	ramme.Init(*buffer_2)
	var reply bool = false

	if ramme.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(ramme.destinationmacbe) == selv.Getmacaddress() {
		if handler_2[ramme.ethernettypebe] != nil {
			ethernetconsole.MUdskriv(([]byte)("provider\n"))

			var markør uintptr = uintptr(Pointer(dataMarkør)) + uintptr(rammeheaderStørrelse)
			reply = handler_2[ramme.ethernettypebe].EthernetRammereceivewhen(markør, størrelse-rammeheaderStørrelse)

		}
	}

	if reply {
		ramme.destinationmacbe = ramme.kildemacbe
		ramme.kildemacbe = Unsignedinteger48r(selv.Getmacaddress())
		ramme.Satbuffer(buffer_2)

	}

	ethernetconsole.MUdskrivxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Udskriv(ramme.kildemacbe)
	ethernetconsole.MUdskriv(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Udskriv(ramme.destinationmacbe)
	ethernetconsole.MUdskriv(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Udskriv(selv.Getmacaddress())
	ethernetconsole.MUdskriv(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Udskriv(ramme.ethernettypebe)
	ethernetconsole.MUdskriv(([]byte)("]"))

	return reply

}
func (selv *TEthernetRammeprovider) Send(dataMarkør uintptr, størrelse uint32) {
	selv.netværkKortspil.Send(dataMarkør, størrelse)
}
func (selv *TEthernetRammeprovider) Rammesend(destinationmacbe uint64, ethernettypebe uint16, dataMarkør uintptr, størrelse uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetRammeheaderbuffer = (*TEthernetRammeheaderbuffer)(Pointer(&buffer2_2))

	var ramme TEthernetRammeheader = TEthernetRammeheader{}
	ramme.Init(*buffer_2)

	ramme.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	ramme.kildemacbe = Unsignedinteger48r(selv.netværkKortspil.Getmacaddress())
	ramme.ethernettypebe = Unsignedinteger16r(ethernettypebe)

	ramme.Satbuffer(buffer_2)
	var kilde_2 [4096]byte = *(*([4096]byte))(Pointer(dataMarkør))

	var i uint32 = 0
	for i = 0; i < størrelse; i++ {
		buffer2_2[uint32(rammeheaderStørrelse)+i] = kilde_2[i]

	}

	var markør uintptr = uintptr(Pointer(&buffer2_2))

	selv.netværkKortspil.Send(markør, størrelse+uint32(rammeheaderStørrelse))

}
func (selv *TEthernetRammeprovider) Getmacaddress() uint64 {
	return selv.netværkKortspil.Getmacaddress()
}
func (selv *TEthernetRammeprovider) Getipaddress() uint64 {
	return selv.netværkKortspil.Getipaddress()
}
