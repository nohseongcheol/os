/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ethernetframe

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	odredištemacbe	[6]byte
	izvormacbe	[6]byte
	ethernetVrstabe	[2]byte
}

var frameheaderVeličina int = 14

type TEthernetframeheader struct {
	odredištemacbe	uint64
	izvormacbe	uint64
	ethernetVrstabe	uint16
}

func (sam *TEthernetframeheader) Init(buffer_2 TEthernetframeheaderbuffer) {
	sam.odredištemacbe = (Niztounsignedinteger48(buffer_2.odredištemacbe))
	sam.izvormacbe = (Niztounsignedinteger48(buffer_2.izvormacbe))
	sam.ethernetVrstabe = (Niztounsignedinteger16(buffer_2.ethernetVrstabe))

}
func (sam *TEthernetframeheader) Postavibuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.odredištemacbe = Unsignedinteger48toNiz(Unsignedinteger48r(sam.odredištemacbe))
	buffer_2.izvormacbe = Unsignedinteger48toNiz(Unsignedinteger48r(sam.izvormacbe))
	buffer_2.ethernetVrstabe = Unsignedinteger16toNiz(Unsignedinteger16r(sam.ethernetVrstabe))
}

type IEthernetframehandler interface {
	Init(backend TEthernetframeprovider)
	Postavihandler(handler IEthernetframehandler, ethernetVrsta uint16)
	Ethernetframereceivewhen(dataPokazivač uintptr, veličina int) bool
	Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32)
	FramePošalji(odredištemacbe uint64, ethernetVrstabe uint16, dataPokazivač uintptr, veličina uint32)
	Providerget() TEthernetframeprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetframehandler struct {
}

var frame TEthernetframeheader
var Backend TEthernetframeprovider
var handler_2 [65535]IEthernetframehandler
var efhandler *TEthernetframehandler = nil

func (sam *TEthernetframehandler) Init(backend TEthernetframeprovider) {
	Backend = backend
}

func (sam *TEthernetframehandler) Postavihandler(handler IEthernetframehandler, pethernetVrsta uint16) {
	handler_2[pethernetVrsta] = handler
}
func (sam *TEthernetframehandler) Postavibackend(backend TEthernetframeprovider) {
	Backend = backend
}
func (sam *TEthernetframehandler) Getbackend() TEthernetframeprovider {
	return Backend
}
func (sam *TEthernetframehandler) Ethernetframereceivewhen(dataPokazivač uintptr, veličina int) bool {
	ethernetconsole.MIspis(([]byte)("OnEtherFrameReceived"))
	return false
}
func (sam *TEthernetframehandler) Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32) {
	Backend.FramePošalji(odredištemacbe, frame.ethernetVrstabe, dataPokazivač, veličina)
}
func (sam *TEthernetframehandler) FramePošalji(odredištemacbe uint64, ethernetVrstabe uint16, dataPokazivač uintptr, veličina uint32) {
	Backend.FramePošalji(odredištemacbe, ethernetVrstabe, dataPokazivač, veličina)
}
func (sam *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (sam *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (sam *TEthernetframehandler) Providerget() TEthernetframeprovider {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TEthernetframeprovider

func (sam *TEthernetframerawdatahandler) Init(pprovider TEthernetframeprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (sam *TEthernetframerawdatahandler) Uključenorawdatareceive(dataPokazivač uintptr, veličina int) bool {
	return provider.Uključenorawdatareceive(dataPokazivač, veličina)
}
func (sam *TEthernetframerawdatahandler) Pošalji(dataPokazivač uintptr, veličina uint32) {
	provider.Pošalji(dataPokazivač, veličina)
}
func (sam *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (sam *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (sam *TEthernetframerawdatahandler) Providerget() TEthernetframeprovider {
	return provider
}

type TEthernetframeprovider struct {
	mrežaKarte	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (sam *TEthernetframeprovider) Init(backend Tamdam79c973) {

	sam.mrežaKarte = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		sam.handler_2[i] = nil
	}
}

var count uint16 = 0

func (sam *TEthernetframeprovider) Uključenorawdatareceive(dataPokazivač uintptr, veličina int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(dataPokazivač))
	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.odredištemacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.odredištemacbe) == sam.Getmacaddress() {
		if handler_2[frame.ethernetVrstabe] != nil {
			ethernetconsole.MIspis(([]byte)("provider\n"))

			var pokazivač uintptr = uintptr(Pointer(dataPokazivač)) + uintptr(frameheaderVeličina)
			reply = handler_2[frame.ethernetVrstabe].Ethernetframereceivewhen(pokazivač, veličina-frameheaderVeličina)

		}
	}

	if reply {
		frame.odredištemacbe = frame.izvormacbe
		frame.izvormacbe = Unsignedinteger48r(sam.Getmacaddress())
		frame.Postavibuffer(buffer_2)

	}

	ethernetconsole.MIspisxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Ispis(frame.izvormacbe)
	ethernetconsole.MIspis(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Ispis(frame.odredištemacbe)
	ethernetconsole.MIspis(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Ispis(sam.Getmacaddress())
	ethernetconsole.MIspis(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Ispis(frame.ethernetVrstabe)
	ethernetconsole.MIspis(([]byte)("]"))

	return reply

}
func (sam *TEthernetframeprovider) Pošalji(dataPokazivač uintptr, veličina uint32) {
	sam.mrežaKarte.Pošalji(dataPokazivač, veličina)
}
func (sam *TEthernetframeprovider) FramePošalji(odredištemacbe uint64, ethernetVrstabe uint16, dataPokazivač uintptr, veličina uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TEthernetframeheader = TEthernetframeheader{}
	frame.Init(*buffer_2)

	frame.odredištemacbe = Unsignedinteger48r(odredištemacbe)
	frame.izvormacbe = Unsignedinteger48r(sam.mrežaKarte.Getmacaddress())
	frame.ethernetVrstabe = Unsignedinteger16r(ethernetVrstabe)

	frame.Postavibuffer(buffer_2)
	var izvor_2 [4096]byte = *(*([4096]byte))(Pointer(dataPokazivač))

	var i uint32 = 0
	for i = 0; i < veličina; i++ {
		buffer2_2[uint32(frameheaderVeličina)+i] = izvor_2[i]

	}

	var pokazivač uintptr = uintptr(Pointer(&buffer2_2))

	sam.mrežaKarte.Pošalji(pokazivač, veličina+uint32(frameheaderVeličina))

}
func (sam *TEthernetframeprovider) Getmacaddress() uint64 {
	return sam.mrežaKarte.Getmacaddress()
}
func (sam *TEthernetframeprovider) Getipaddress() uint64 {
	return sam.mrežaKarte.Getipaddress()
}
