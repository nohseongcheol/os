/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package khung_mạng_dùng_chung_môi_trường_truyền

import . "console"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetconsole TConsole = TConsole{}

type TEthernetframeheaderbuffer struct {
	destinationmacbe	[6]byte
	mãnguồnmacbe		[6]byte
	ethernetKiểube		[2]byte
}

var frameheaderCỡ int = 14

type TĐầu_khung_mạng_dùng_chung_môi_trường_truyền struct {
	destinationmacbe	uint64
	mãnguồnmacbe		uint64
	ethernetKiểube		uint16
}

func (mình *TĐầu_khung_mạng_dùng_chung_môi_trường_truyền) Init(buffer_2 TEthernetframeheaderbuffer) {
	mình.destinationmacbe = (Mảngtounsignedinteger48(buffer_2.destinationmacbe))
	mình.mãnguồnmacbe = (Mảngtounsignedinteger48(buffer_2.mãnguồnmacbe))
	mình.ethernetKiểube = (Mảngtounsignedinteger16(buffer_2.ethernetKiểube))

}
func (mình *TĐầu_khung_mạng_dùng_chung_môi_trường_truyền) Đặtbuffer(buffer_2 *TEthernetframeheaderbuffer) {
	buffer_2.destinationmacbe = Unsignedinteger48toMảng(Unsignedinteger48r(mình.destinationmacbe))
	buffer_2.mãnguồnmacbe = Unsignedinteger48toMảng(Unsignedinteger48r(mình.mãnguồnmacbe))
	buffer_2.ethernetKiểube = Unsignedinteger16toMảng(Unsignedinteger16r(mình.ethernetKiểube))
}

type IEthernetframehandler interface {
	Init(backend TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền)
	Đặthandler(handler IEthernetframehandler, ethernetKiểu uint16)
	Ethernetframereceivewhen(dataContrỏ uintptr, cỡ int) bool
	Gởi(destinationmacbe uint64, dataContrỏ uintptr, cỡ uint32)
	FrameGởi(destinationmacbe uint64, ethernetKiểube uint16, dataContrỏ uintptr, cỡ uint32)
	Providerget() TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEthernetframehandler struct {
}

var frame TĐầu_khung_mạng_dùng_chung_môi_trường_truyền
var Backend TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền
var handler_2 [65535]IEthernetframehandler
var efhandler *TEthernetframehandler = nil

func (mình *TEthernetframehandler) Init(backend TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) {
	Backend = backend
}

func (mình *TEthernetframehandler) Đặthandler(handler IEthernetframehandler, pethernetKiểu uint16) {
	handler_2[pethernetKiểu] = handler
}
func (mình *TEthernetframehandler) Đặtbackend(backend TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) {
	Backend = backend
}
func (mình *TEthernetframehandler) Getbackend() TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền {
	return Backend
}
func (mình *TEthernetframehandler) Ethernetframereceivewhen(dataContrỏ uintptr, cỡ int) bool {
	ethernetconsole.MIn(([]byte)("OnEtherFrameReceived"))
	return false
}
func (mình *TEthernetframehandler) Gởi(destinationmacbe uint64, dataContrỏ uintptr, cỡ uint32) {
	Backend.FrameGởi(destinationmacbe, frame.ethernetKiểube, dataContrỏ, cỡ)
}
func (mình *TEthernetframehandler) FrameGởi(destinationmacbe uint64, ethernetKiểube uint16, dataContrỏ uintptr, cỡ uint32) {
	Backend.FrameGởi(destinationmacbe, ethernetKiểube, dataContrỏ, cỡ)
}
func (mình *TEthernetframehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (mình *TEthernetframehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (mình *TEthernetframehandler) Providerget() TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền {
	return Backend
}

type TEthernetframerawdatahandler struct {
	TRawdatahandler
}

var provider TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền

func (mình *TEthernetframerawdatahandler) Init(pprovider TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (mình *TEthernetframerawdatahandler) Bậtrawdatareceive(dataContrỏ uintptr, cỡ int) bool {
	return provider.Bậtrawdatareceive(dataContrỏ, cỡ)
}
func (mình *TEthernetframerawdatahandler) Gởi(dataContrỏ uintptr, cỡ uint32) {
	provider.Gởi(dataContrỏ, cỡ)
}
func (mình *TEthernetframerawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (mình *TEthernetframerawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (mình *TEthernetframerawdatahandler) Providerget() TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền {
	return provider
}

type TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền struct {
	mạngĐánhbài	Tamdam79c973
	handler_2	[65565]IEthernetframehandler
}

func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) Init(backend Tamdam79c973) {

	mình.mạngĐánhbài = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		mình.handler_2[i] = nil
	}
}

var sốlượng uint16 = 0

func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) Bậtrawdatareceive(dataContrỏ uintptr, cỡ int) bool {

	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(dataContrỏ))
	var frame TĐầu_khung_mạng_dùng_chung_môi_trường_truyền = TĐầu_khung_mạng_dùng_chung_môi_trường_truyền{}
	frame.Init(*buffer_2)
	var reply bool = false

	if frame.destinationmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(frame.destinationmacbe) == mình.Getmacaddress() {
		if handler_2[frame.ethernetKiểube] != nil {
			ethernetconsole.MIn(([]byte)("provider\n"))

			var tham_chiếu_địa_chỉ uintptr = uintptr(Pointer(dataContrỏ)) + uintptr(frameheaderCỡ)
			reply = handler_2[frame.ethernetKiểube].Ethernetframereceivewhen(tham_chiếu_địa_chỉ, cỡ-frameheaderCỡ)

		}
	}

	if reply {
		frame.destinationmacbe = frame.mãnguồnmacbe
		frame.mãnguồnmacbe = Unsignedinteger48r(mình.Getmacaddress())
		frame.Đặtbuffer(buffer_2)

	}

	ethernetconsole.MInxy(([]byte)("spro["), 0, 1)
	ethernetconsole.MUnsignedinteger64In(frame.mãnguồnmacbe)
	ethernetconsole.MIn(([]byte)(":"))
	ethernetconsole.MUnsignedinteger64In(frame.destinationmacbe)
	ethernetconsole.MIn(([]byte)(":]["))
	ethernetconsole.MUnsignedinteger64In(mình.Getmacaddress())
	ethernetconsole.MIn(([]byte)(":"))
	ethernetconsole.MUnsignedinteger16In(frame.ethernetKiểube)
	ethernetconsole.MIn(([]byte)("]"))

	return reply

}
func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) Gởi(dataContrỏ uintptr, cỡ uint32) {
	mình.mạngĐánhbài.Gởi(dataContrỏ, cỡ)
}
func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) FrameGởi(destinationmacbe uint64, ethernetKiểube uint16, dataContrỏ uintptr, cỡ uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetframeheaderbuffer = (*TEthernetframeheaderbuffer)(Pointer(&buffer2_2))

	var frame TĐầu_khung_mạng_dùng_chung_môi_trường_truyền = TĐầu_khung_mạng_dùng_chung_môi_trường_truyền{}
	frame.Init(*buffer_2)

	frame.destinationmacbe = Unsignedinteger48r(destinationmacbe)
	frame.mãnguồnmacbe = Unsignedinteger48r(mình.mạngĐánhbài.Getmacaddress())
	frame.ethernetKiểube = Unsignedinteger16r(ethernetKiểube)

	frame.Đặtbuffer(buffer_2)
	var mãnguồn_2 [4096]byte = *(*([4096]byte))(Pointer(dataContrỏ))

	var i uint32 = 0
	for i = 0; i < cỡ; i++ {
		buffer2_2[uint32(frameheaderCỡ)+i] = mãnguồn_2[i]

	}

	var tham_chiếu_địa_chỉ uintptr = uintptr(Pointer(&buffer2_2))

	mình.mạngĐánhbài.Gởi(tham_chiếu_địa_chỉ, cỡ+uint32(frameheaderCỡ))

}
func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) Getmacaddress() uint64 {
	return mình.mạngĐánhbài.Getmacaddress()
}
func (mình *TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền) Getipaddress() uint64 {
	return mình.mạngĐánhbài.Getipaddress()
}
