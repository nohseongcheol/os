package laidinisKadras

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var laidinisconsole TConsole = TConsole{}

type TLaidinisKadrasheaderbuffer struct {
	tikslasmacbe	[6]byte
	šaltinismacbe	[6]byte
	laidinisTipasbe	[2]byte
}

var kadrasheaderDydis int = 14

type TLaidinisKadrasheader struct {
	tikslasmacbe	uint64
	šaltinismacbe	uint64
	laidinisTipasbe	uint16
}

func (self *TLaidinisKadrasheader) Init(buffer_2 TLaidinisKadrasheaderbuffer) {
	self.tikslasmacbe = (Masyvastounsignedinteger48(buffer_2.tikslasmacbe))
	self.šaltinismacbe = (Masyvastounsignedinteger48(buffer_2.šaltinismacbe))
	self.laidinisTipasbe = (Masyvastounsignedinteger16(buffer_2.laidinisTipasbe))

}
func (self *TLaidinisKadrasheader) Nustatytabuffer(buffer_2 *TLaidinisKadrasheaderbuffer) {
	buffer_2.tikslasmacbe = Unsignedinteger48toMasyvas(Unsignedinteger48r(self.tikslasmacbe))
	buffer_2.šaltinismacbe = Unsignedinteger48toMasyvas(Unsignedinteger48r(self.šaltinismacbe))
	buffer_2.laidinisTipasbe = Unsignedinteger16toMasyvas(Unsignedinteger16r(self.laidinisTipasbe))
}

type ILaidinisKadrashandler interface {
	Init(backend TLaidinisKadrasprovider)
	Nustatytahandler(handler ILaidinisKadrashandler, laidinisTipas uint16)
	LaidinisKadrasreceivewhen(dataRodyklė uintptr, dydis int) bool
	Siųsti(tikslasmacbe uint64, dataRodyklė uintptr, dydis uint32)
	KadrasSiųsti(tikslasmacbe uint64, laidinisTipasbe uint16, dataRodyklė uintptr, dydis uint32)
	Providerget() TLaidinisKadrasprovider
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TLaidinisKadrashandler struct {
}

var kadras TLaidinisKadrasheader
var Backend TLaidinisKadrasprovider
var handler_2 [65535]ILaidinisKadrashandler
var efhandler *TLaidinisKadrashandler = nil

func (self *TLaidinisKadrashandler) Init(backend TLaidinisKadrasprovider) {
	Backend = backend
}

func (self *TLaidinisKadrashandler) Nustatytahandler(handler ILaidinisKadrashandler, pLaidinisTipas uint16) {
	handler_2[pLaidinisTipas] = handler
}
func (self *TLaidinisKadrashandler) Nustatytabackend(backend TLaidinisKadrasprovider) {
	Backend = backend
}
func (self *TLaidinisKadrashandler) Getbackend() TLaidinisKadrasprovider {
	return Backend
}
func (self *TLaidinisKadrashandler) LaidinisKadrasreceivewhen(dataRodyklė uintptr, dydis int) bool {
	laidinisconsole.MSpausdinti(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TLaidinisKadrashandler) Siųsti(tikslasmacbe uint64, dataRodyklė uintptr, dydis uint32) {
	Backend.KadrasSiųsti(tikslasmacbe, kadras.laidinisTipasbe, dataRodyklė, dydis)
}
func (self *TLaidinisKadrashandler) KadrasSiųsti(tikslasmacbe uint64, laidinisTipasbe uint16, dataRodyklė uintptr, dydis uint32) {
	Backend.KadrasSiųsti(tikslasmacbe, laidinisTipasbe, dataRodyklė, dydis)
}
func (self *TLaidinisKadrashandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TLaidinisKadrashandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TLaidinisKadrashandler) Providerget() TLaidinisKadrasprovider {
	return Backend
}

type TLaidinisKadrasrawdatahandler struct {
	TRawdatahandler
}

var provider TLaidinisKadrasprovider

func (self *TLaidinisKadrasrawdatahandler) Init(pprovider TLaidinisKadrasprovider, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TLaidinisKadrasrawdatahandler) Įjungtarawdatareceive(dataRodyklė uintptr, dydis int) bool {
	return provider.Įjungtarawdatareceive(dataRodyklė, dydis)
}
func (self *TLaidinisKadrasrawdatahandler) Siųsti(dataRodyklė uintptr, dydis uint32) {
	provider.Siųsti(dataRodyklė, dydis)
}
func (self *TLaidinisKadrasrawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TLaidinisKadrasrawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TLaidinisKadrasrawdatahandler) Providerget() TLaidinisKadrasprovider {
	return provider
}

type TLaidinisKadrasprovider struct {
	tinklasKortų	Tamdam79c973
	handler_2	[65565]ILaidinisKadrashandler
}

func (self *TLaidinisKadrasprovider) Init(backend Tamdam79c973) {

	self.tinklasKortų = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TLaidinisKadrasprovider) Įjungtarawdatareceive(dataRodyklė uintptr, dydis int) bool {

	var buffer_2 *TLaidinisKadrasheaderbuffer = (*TLaidinisKadrasheaderbuffer)(Pointer(dataRodyklė))
	var kadras TLaidinisKadrasheader = TLaidinisKadrasheader{}
	kadras.Init(*buffer_2)
	var reply bool = false

	if kadras.tikslasmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(kadras.tikslasmacbe) == self.Getmacaddress() {
		if handler_2[kadras.laidinisTipasbe] != nil {
			laidinisconsole.MSpausdinti(([]byte)("provider\n"))

			var rodyklė_2 uintptr = uintptr(Pointer(dataRodyklė)) + uintptr(kadrasheaderDydis)
			reply = handler_2[kadras.laidinisTipasbe].LaidinisKadrasreceivewhen(rodyklė_2, dydis-kadrasheaderDydis)

		}
	}

	if reply {
		kadras.tikslasmacbe = kadras.šaltinismacbe
		kadras.šaltinismacbe = Unsignedinteger48r(self.Getmacaddress())
		kadras.Nustatytabuffer(buffer_2)

	}

	laidinisconsole.MSpausdintixy(([]byte)("spro["), 0, 1)
	laidinisconsole.MUnsignedinteger64Spausdinti(kadras.šaltinismacbe)
	laidinisconsole.MSpausdinti(([]byte)(":"))
	laidinisconsole.MUnsignedinteger64Spausdinti(kadras.tikslasmacbe)
	laidinisconsole.MSpausdinti(([]byte)(":]["))
	laidinisconsole.MUnsignedinteger64Spausdinti(self.Getmacaddress())
	laidinisconsole.MSpausdinti(([]byte)(":"))
	laidinisconsole.MUnsignedinteger16Spausdinti(kadras.laidinisTipasbe)
	laidinisconsole.MSpausdinti(([]byte)("]"))

	return reply

}
func (self *TLaidinisKadrasprovider) Siųsti(dataRodyklė uintptr, dydis uint32) {
	self.tinklasKortų.Siųsti(dataRodyklė, dydis)
}
func (self *TLaidinisKadrasprovider) KadrasSiųsti(tikslasmacbe uint64, laidinisTipasbe uint16, dataRodyklė uintptr, dydis uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TLaidinisKadrasheaderbuffer = (*TLaidinisKadrasheaderbuffer)(Pointer(&buffer2_2))

	var kadras TLaidinisKadrasheader = TLaidinisKadrasheader{}
	kadras.Init(*buffer_2)

	kadras.tikslasmacbe = Unsignedinteger48r(tikslasmacbe)
	kadras.šaltinismacbe = Unsignedinteger48r(self.tinklasKortų.Getmacaddress())
	kadras.laidinisTipasbe = Unsignedinteger16r(laidinisTipasbe)

	kadras.Nustatytabuffer(buffer_2)
	var šaltinis_2 [4096]byte = *(*([4096]byte))(Pointer(dataRodyklė))

	var i uint32 = 0
	for i = 0; i < dydis; i++ {
		buffer2_2[uint32(kadrasheaderDydis)+i] = šaltinis_2[i]

	}

	var rodyklė_2 uintptr = uintptr(Pointer(&buffer2_2))

	self.tinklasKortų.Siųsti(rodyklė_2, dydis+uint32(kadrasheaderDydis))

}
func (self *TLaidinisKadrasprovider) Getmacaddress() uint64 {
	return self.tinklasKortų.Getmacaddress()
}
func (self *TLaidinisKadrasprovider) Getipaddress() uint64 {
	return self.tinklasKortų.Getipaddress()
}
