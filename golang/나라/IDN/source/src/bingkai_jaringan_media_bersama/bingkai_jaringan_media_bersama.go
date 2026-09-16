/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package bingkai_jaringan_media_bersama

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetBingkaiheaderbuffer struct {
	tujuanmacbe	[6]byte
	sumbermacbe	[6]byte
	ethernetTipebe	[2]byte
}

var bingkaiheaderUkuran int = 14

type TKepala_bingkai_jaringan_media_bersama struct {
	tujuanmacbe	uint64
	sumbermacbe	uint64
	ethernetTipebe	uint16
}

func (dirisendiri *TKepala_bingkai_jaringan_media_bersama) Init(buffer_2 TEthernetBingkaiheaderbuffer) {
	dirisendiri.tujuanmacbe = (Jajarantounsignedinteger48(buffer_2.tujuanmacbe))
	dirisendiri.sumbermacbe = (Jajarantounsignedinteger48(buffer_2.sumbermacbe))
	dirisendiri.ethernetTipebe = (Jajarantounsignedinteger16(buffer_2.ethernetTipebe))

}
func (dirisendiri *TKepala_bingkai_jaringan_media_bersama) Aturbuffer(buffer_2 *TEthernetBingkaiheaderbuffer) {
	buffer_2.tujuanmacbe = Unsignedinteger48toJajaran(Unsignedinteger48r(dirisendiri.tujuanmacbe))
	buffer_2.sumbermacbe = Unsignedinteger48toJajaran(Unsignedinteger48r(dirisendiri.sumbermacbe))
	buffer_2.ethernetTipebe = Unsignedinteger16toJajaran(Unsignedinteger16r(dirisendiri.ethernetTipebe))
}

type IEthernetBingkaihandler interface {
	Init(backend TPenyedia_bingkai_jaringan_media_bersama)
	Aturhandler(handler IEthernetBingkaihandler, ethernetTipe uint16)
	EthernetBingkaireceivewhen(dataPenunjuk uintptr, ukuran int) bool
	Kirim(tujuanmacbe uint64, dataPenunjuk uintptr, ukuran uint32)
	BingkaiKirim(tujuanmacbe uint64, ethernetTipebe uint16, dataPenunjuk uintptr, ukuran uint32)
	Providerget() TPenyedia_bingkai_jaringan_media_bersama
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetBingkaihandler struct {
}

var bingkai TKepala_bingkai_jaringan_media_bersama
var Backend TPenyedia_bingkai_jaringan_media_bersama
var handler_2 [65535]IEthernetBingkaihandler
var efhandler *TEthernetBingkaihandler = nil

func (dirisendiri *TEthernetBingkaihandler) Init(backend TPenyedia_bingkai_jaringan_media_bersama) {
	Backend = backend
}

func (dirisendiri *TEthernetBingkaihandler) Aturhandler(handler IEthernetBingkaihandler, pethernetTipe uint16) {
	handler_2[pethernetTipe] = handler
}
func (dirisendiri *TEthernetBingkaihandler) Aturbackend(backend TPenyedia_bingkai_jaringan_media_bersama) {
	Backend = backend
}
func (dirisendiri *TEthernetBingkaihandler) Getbackend() TPenyedia_bingkai_jaringan_media_bersama {
	return Backend
}
func (dirisendiri *TEthernetBingkaihandler) EthernetBingkaireceivewhen(dataPenunjuk uintptr, ukuran int) bool {
	ethernetconsole.MCetak(([]byte)("OnEtherFrameReceived"))
	return false
}
func (dirisendiri *TEthernetBingkaihandler) Kirim(tujuanmacbe uint64, dataPenunjuk uintptr, ukuran uint32) {
	Backend.BingkaiKirim(tujuanmacbe, bingkai.ethernetTipebe, dataPenunjuk, ukuran)
}
func (dirisendiri *TEthernetBingkaihandler) BingkaiKirim(tujuanmacbe uint64, ethernetTipebe uint16, dataPenunjuk uintptr, ukuran uint32) {
	Backend.BingkaiKirim(tujuanmacbe, ethernetTipebe, dataPenunjuk, ukuran)
}
func (dirisendiri *TEthernetBingkaihandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (dirisendiri *TEthernetBingkaihandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (dirisendiri *TEthernetBingkaihandler) Providerget() TPenyedia_bingkai_jaringan_media_bersama {
	return Backend
}

type TEthernetBingkairawdatahandler struct {
	TRawdatahandler
}

var provider TPenyedia_bingkai_jaringan_media_bersama

func (dirisendiri *TEthernetBingkairawdatahandler) Init(pprovider TPenyedia_bingkai_jaringan_media_bersama, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (dirisendiri *TEthernetBingkairawdatahandler) Hiduprawdatareceive(dataPenunjuk uintptr, ukuran int) bool {
	return provider.Hiduprawdatareceive(dataPenunjuk, ukuran)
}
func (dirisendiri *TEthernetBingkairawdatahandler) Kirim(dataPenunjuk uintptr, ukuran uint32) {
	provider.Kirim(dataPenunjuk, ukuran)
}
func (dirisendiri *TEthernetBingkairawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (dirisendiri *TEthernetBingkairawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (dirisendiri *TEthernetBingkairawdatahandler) Providerget() TPenyedia_bingkai_jaringan_media_bersama {
	return provider
}

type TPenyedia_bingkai_jaringan_media_bersama struct {
	jaringanKartu	Tamdam79c973
	handler_2	[65565]IEthernetBingkaihandler
}

func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) Init(backend Tamdam79c973) {

	dirisendiri.jaringanKartu = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		dirisendiri.handler_2[i] = nil
	}
}

var count uint16 = 0

func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) Hiduprawdatareceive(dataPenunjuk uintptr, ukuran int) bool {

	var buffer_2 *TEthernetBingkaiheaderbuffer = (*TEthernetBingkaiheaderbuffer)(Pointer(dataPenunjuk))
	var bingkai TKepala_bingkai_jaringan_media_bersama = TKepala_bingkai_jaringan_media_bersama{}
	bingkai.Init(*buffer_2)
	var reply bool = false

	if bingkai.tujuanmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(bingkai.tujuanmacbe) == dirisendiri.Getmacaddress() {
		if handler_2[bingkai.ethernetTipebe] != nil {
			ethernetconsole.MCetak(([]byte)("provider\n"))

			var acuan_alamat uintptr = uintptr(Pointer(dataPenunjuk)) + uintptr(bingkaiheaderUkuran)
			reply = handler_2[bingkai.ethernetTipebe].EthernetBingkaireceivewhen(acuan_alamat, ukuran-bingkaiheaderUkuran)

		}
	}

	if reply {
		bingkai.tujuanmacbe = bingkai.sumbermacbe
		bingkai.sumbermacbe = Unsignedinteger48r(dirisendiri.Getmacaddress())
		bingkai.Aturbuffer(buffer_2)

	}

	ethernetconsole.MCetakxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64Cetak(bingkai.sumbermacbe)
	ethernetconsole.MCetak(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64Cetak(bingkai.tujuanmacbe)
	ethernetconsole.MCetak(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64Cetak(dirisendiri.Getmacaddress())
	ethernetconsole.MCetak(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16Cetak(bingkai.ethernetTipebe)
	ethernetconsole.MCetak(([]byte)("]"))

	return reply

}
func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) Kirim(dataPenunjuk uintptr, ukuran uint32) {
	dirisendiri.jaringanKartu.Kirim(dataPenunjuk, ukuran)
}
func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) BingkaiKirim(tujuanmacbe uint64, ethernetTipebe uint16, dataPenunjuk uintptr, ukuran uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetBingkaiheaderbuffer = (*TEthernetBingkaiheaderbuffer)(Pointer(&buffer2_2))

	var bingkai TKepala_bingkai_jaringan_media_bersama = TKepala_bingkai_jaringan_media_bersama{}
	bingkai.Init(*buffer_2)

	bingkai.tujuanmacbe = Unsignedinteger48r(tujuanmacbe)
	bingkai.sumbermacbe = Unsignedinteger48r(dirisendiri.jaringanKartu.Getmacaddress())
	bingkai.ethernetTipebe = Unsignedinteger16r(ethernetTipebe)

	bingkai.Aturbuffer(buffer_2)
	var sumber_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenunjuk))

	var i uint32 = 0
	for i = 0; i < ukuran; i++ {
		buffer2_2[uint32(bingkaiheaderUkuran)+i] = sumber_2[i]

	}

	var acuan_alamat uintptr = uintptr(Pointer(&buffer2_2))

	dirisendiri.jaringanKartu.Kirim(acuan_alamat, ukuran+uint32(bingkaiheaderUkuran))

}
func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) Getmacaddress() uint64 {
	return dirisendiri.jaringanKartu.Getmacaddress()
}
func (dirisendiri *TPenyedia_bingkai_jaringan_media_bersama) Getipaddress() uint64 {
	return dirisendiri.jaringanKartu.Getipaddress()
}
