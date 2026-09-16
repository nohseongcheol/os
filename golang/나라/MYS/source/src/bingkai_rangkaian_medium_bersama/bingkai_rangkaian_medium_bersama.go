/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package bingkai_rangkaian_medium_bersama

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var eternetconsole TConsole = TConsole{}

type TEternetBingkaiheaderbuffer struct {
	destinationmacbe	[6]byte
	sumbermacbe		[6]byte
	eternetJenisbe		[2]byte
}

var bingkaiheaderSaiz int = 14

type TPengepala_bingkai_rangkaian_medium_bersama struct {
	destinationmacbe	uint64
	sumbermacbe		uint64
	eternetJenisbe		uint16
}

func (diri *TPengepala_bingkai_rangkaian_medium_bersama) Init(buffer_2 TEternetBingkaiheaderbuffer) {
	diri.destinationmacbe = (Tatasusunantounsignedinteger48(buffer_2.destinationmacbe))
	diri.sumbermacbe = (Tatasusunantounsignedinteger48(buffer_2.sumbermacbe))
	diri.eternetJenisbe = (Tatasusunantounsignedinteger16(buffer_2.eternetJenisbe))

}
func (diri *TPengepala_bingkai_rangkaian_medium_bersama) Tetapkanbuffer(buffer_2 *TEternetBingkaiheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toTatasusunan(Unsignedinteger48r(diri.destinationmacbe))
	buffer_2.sumbermacbe = Unsignedinteger48toTatasusunan(Unsignedinteger48r(diri.sumbermacbe))
	buffer_2.eternetJenisbe = Unsignedinteger16toTatasusunan(Unsignedinteger16r(diri.eternetJenisbe))
}

type IEternetBingkaihandler interface {
	Init(backend TPembekal_bingkai_rangkaian_medium_bersama)
	Tetapkanhandler(handler IEternetBingkaihandler, eternetJenis uint16)
	EternetBingkaireceivewhen(dataPenuding uintptr, saiz int) bool
	Hantar(destinationmacbe uint64, dataPenuding uintptr, saiz uint32)
	BingkaiHantar(destinationmacbe uint64, eternetJenisbe uint16, dataPenuding uintptr, saiz uint32)
	Providerget() TPembekal_bingkai_rangkaian_medium_bersama
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEternetBingkaihandler struct {
}

var bingkai TPengepala_bingkai_rangkaian_medium_bersama
var Backend TPembekal_bingkai_rangkaian_medium_bersama
var handler_2 [65535]IEternetBingkaihandler
var efhandler *TEternetBingkaihandler = nil

func (diri *TEternetBingkaihandler) Init(backend TPembekal_bingkai_rangkaian_medium_bersama) {
	Backend = backend
}

func (diri *TEternetBingkaihandler) Tetapkanhandler(handler IEternetBingkaihandler, pEternetJenis uint16) {
	handler_2[pEternetJenis] = handler
}
func (diri *TEternetBingkaihandler) Tetapkanbackend(backend TPembekal_bingkai_rangkaian_medium_bersama) {
	Backend = backend
}
func (diri *TEternetBingkaihandler) Getbackend() TPembekal_bingkai_rangkaian_medium_bersama {
	return Backend
}
func (diri *TEternetBingkaihandler) EternetBingkaireceivewhen(dataPenuding uintptr, saiz int) bool {
	eternetconsole.MCetak(([]byte)("OnEtherFrameReceived"))
	return false
}
func (diri *TEternetBingkaihandler) Hantar(destinationmacbe uint64, dataPenuding uintptr, saiz uint32) {
	Backend.BingkaiHantar(destinationmacbe, bingkai.eternetJenisbe, dataPenuding, saiz)
}
func (diri *TEternetBingkaihandler) BingkaiHantar(destinationmacbe uint64, eternetJenisbe uint16, dataPenuding uintptr, saiz uint32) {
	Backend.BingkaiHantar(destinationmacbe, eternetJenisbe, dataPenuding, saiz)
}
func (diri *TEternetBingkaihandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (diri *TEternetBingkaihandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (diri *TEternetBingkaihandler) Providerget() TPembekal_bingkai_rangkaian_medium_bersama {
	return Backend
}

type TEternetBingkairawdatahandler struct {
	TRawdatahandler
}

var provider TPembekal_bingkai_rangkaian_medium_bersama

func (diri *TEternetBingkairawdatahandler) Init(pprovider TPembekal_bingkai_rangkaian_medium_bersama, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (diri *TEternetBingkairawdatahandler) Bukarawdatareceive(dataPenuding uintptr, saiz int) bool {
	return provider.Bukarawdatareceive(dataPenuding, saiz)
}
func (diri *TEternetBingkairawdatahandler) Hantar(dataPenuding uintptr, saiz uint32) {
	provider.Hantar(dataPenuding, saiz)
}
func (diri *TEternetBingkairawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (diri *TEternetBingkairawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (diri *TEternetBingkairawdatahandler) Providerget() TPembekal_bingkai_rangkaian_medium_bersama {
	return provider
}

type TPembekal_bingkai_rangkaian_medium_bersama struct {
	rangkaiancard	Tamdam79c973
	handler_2	[65565]IEternetBingkaihandler
}

func (diri *TPembekal_bingkai_rangkaian_medium_bersama) Init(backend Tamdam79c973) {

	diri.rangkaiancard = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		diri.handler_2[i] = nil
	}
}

var count uint16 = 0

func (diri *TPembekal_bingkai_rangkaian_medium_bersama) Bukarawdatareceive(dataPenuding uintptr, saiz int) bool {

	var buffer_2 *TEternetBingkaiheaderbuffer = (*TEternetBingkaiheaderbuffer)(Pointer(dataPenuding))
	var bingkai TPengepala_bingkai_rangkaian_medium_bersama = TPengepala_bingkai_rangkaian_medium_bersama{}
	bingkai.Init(*buffer_2)
	var reply bool = false

	if bingkai.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(bingkai.destinationmacbe) == diri.Getmacaddress() {
		if handler_2[bingkai.eternetJenisbe] != nil {
			eternetconsole.MCetak(([]byte)("provider\n"))

			var rujukan_alamat uintptr = uintptr(Pointer(dataPenuding)) + uintptr(bingkaiheaderSaiz)
			reply = handler_2[bingkai.eternetJenisbe].EternetBingkaireceivewhen(rujukan_alamat, saiz-bingkaiheaderSaiz)

		}
	}

	if reply {
		bingkai.destinationmacbe = bingkai.sumbermacbe
		bingkai.sumbermacbe = Unsignedinteger48r(diri.Getmacaddress())
		bingkai.Tetapkanbuffer(buffer_2)

	}

	eternetconsole.MCetakxy(([]byte)("spro["), 0, 1)
	eternetconsole.MUnsignedinteger64Cetak(bingkai.sumbermacbe)
	eternetconsole.MCetak(([]byte)(":"))
	eternetconsole.MUnsignedinteger64Cetak(bingkai.destinationmacbe)
	eternetconsole.MCetak(([]byte)(":]["))
	eternetconsole.MUnsignedinteger64Cetak(diri.Getmacaddress())
	eternetconsole.MCetak(([]byte)(":"))
	eternetconsole.MUnsignedinteger16Cetak(bingkai.eternetJenisbe)
	eternetconsole.MCetak(([]byte)("]"))

	return reply

}
func (diri *TPembekal_bingkai_rangkaian_medium_bersama) Hantar(dataPenuding uintptr, saiz uint32) {
	diri.rangkaiancard.Hantar(dataPenuding, saiz)
}
func (diri *TPembekal_bingkai_rangkaian_medium_bersama) BingkaiHantar(destinationmacbe uint64, eternetJenisbe uint16, dataPenuding uintptr, saiz uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEternetBingkaiheaderbuffer = (*TEternetBingkaiheaderbuffer)(Pointer(&buffer2_2))

	var bingkai TPengepala_bingkai_rangkaian_medium_bersama = TPengepala_bingkai_rangkaian_medium_bersama{}
	bingkai.Init(*buffer_2)

	bingkai.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	bingkai.sumbermacbe = Unsignedinteger48r(diri.rangkaiancard.Getmacaddress())
	bingkai.eternetJenisbe = Unsignedinteger16r(eternetJenisbe)

	bingkai.Tetapkanbuffer(buffer_2)
	var sumber_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenuding))

	var i uint32 = 0
	for i = 0; i < saiz; i++ {
		buffer2_2[uint32(bingkaiheaderSaiz)+i] = sumber_2[i]

	}

	var rujukan_alamat uintptr = uintptr(Pointer(&buffer2_2))

	diri.rangkaiancard.Hantar(rujukan_alamat, saiz+uint32(bingkaiheaderSaiz))

}
func (diri *TPembekal_bingkai_rangkaian_medium_bersama) Getmacaddress() uint64 {
	return diri.rangkaiancard.Getmacaddress()
}
func (diri *TPembekal_bingkai_rangkaian_medium_bersama) Getipaddress() uint64 {
	return diri.rangkaiancard.Getipaddress()
}
