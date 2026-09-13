package amdam79c973

import . "unsafe"
import . "giánđoạn"
import . "console"
import . "cổng"
import . "pci"

var mạngĐánhbàiconsole TConsole = TConsole{}

type TInitializationTắcnghẽn struct {
	chếđộ		uint16
	sỐGởibuffer	uint8
	sỐrecvbuffer	uint8

	physicaladdress	uint64

	logicaladdress		uint64
	recvbufferMôtảaddress	uintptr
	gởibufferMôtảaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	cờ		uint32
	cờ2		uint32
	sẵnsàng		uint32
}

type IRawdatahandler interface {
	Bậtrawdatareceive(dataContrỏ uintptr, cỡ int) bool
	Gởi(dataContrỏ uintptr, cỡ uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (mình *TRawdatahandler) Đặtbackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (mình *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (mình *TRawdatahandler) Bậtrawdatareceive(dataContrỏ uintptr, cỡ int) bool {
	mạngĐánhbàiconsole.MInxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (mình *TRawdatahandler) Gởi(dataContrỏ uintptr, cỡ uint32) {
	mạngĐánhbàiconsole.MInxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Gởi(dataContrỏ, cỡ)
}

var Macaddress0Cổng uint16
var Macaddress2Cổng uint16
var Macaddress4Cổng uint16
var registerdataCổng uint16
var registeraddressCổng uint16
var đặtlạiCổng uint16
var busĐiềukhiểnregisterdataCổng uint16

var initTắcnghẽn TInitializationTắcnghẽn

var gởibufferMôtả [8]TBufferdescriptor
var gởibufferMôtảBộnhớ [2048 + 15]byte
var gởibuffer [2*1024 + 15][8]uint8
var hiệnhànhGởibuffer uint8

var recvbufferMôtả [8]TBufferdescriptor
var recvbufferMôtảBộnhớ [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var hiệnhànhrecvbuffer uint8
var funcGiátrị func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TGiánđoạnhandler
	thiếtbịdescriptor	TPeripheralcomponentinterconnectThiếtbịdescriptor
	giánđoạn		*TGiánđoạnmanager
	handler			*TRawdatahandler
}

var console_2 TConsole = TConsole{}
var irawdatahandler IRawdatahandler

func (mình *Tamdam79c973) Initdriver(giánđoạn *TGiánđoạnmanager, thiếtbịdescriptor TPeripheralcomponentinterconnectThiếtbịdescriptor, handler IRawdatahandler) {

	mình.thiếtbịdescriptor = thiếtbịdescriptor

	funcGiátrị = (*Tamdam79c973).HandleGiánđoạn
	var address uintptr
	address = uintptr(Pointer(&funcGiátrị))

	mình.Init(uint8(0x20+thiếtbịdescriptor.Giánđoạn), uintptr(Pointer(giánđoạn)), address)

	Macaddress0Cổng = uint16(thiếtbịdescriptor.Cổngbase)
	Macaddress2Cổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x02
	Macaddress4Cổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x04
	registerdataCổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x10
	registeraddressCổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x12
	đặtlạiCổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x14
	busĐiềukhiểnregisterdataCổng = uint16(thiếtbịdescriptor.Cổngbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	hiệnhànhGởibuffer = 0
	hiệnhànhrecvbuffer = 0

	var Mac0 uint64 = uint64(CổngĐọctừ(Macaddress0Cổng) % 256)
	var Mac1 uint64 = uint64(CổngĐọctừ(Macaddress0Cổng) / 256)
	var Mac2 uint64 = uint64(CổngĐọctừ(Macaddress2Cổng) % 256)
	var Mac3 uint64 = uint64(CổngĐọctừ(Macaddress2Cổng) / 256)
	var Mac4 uint64 = uint64(CổngĐọctừ(Macaddress4Cổng) % 256)
	var Mac5 uint64 = uint64(CổngĐọctừ(Macaddress4Cổng) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	console_2.MInxy(([]byte)("[interrupt num : "), 0, 13)
	console_2.MHexadecimalIn(uint8(thiếtbịdescriptor.Giánđoạn))
	console_2.MIn(([]byte)("]"))
	console_2.MIn(([]byte)("[mac address : "))
	console_2.MUnsignedinteger16In(uint16(macaddress >> 32))
	console_2.MUnsignedinteger32In(uint32(macaddress & 0x00000000FFFFFFFF))
	console_2.MIn(([]byte)("]"))

	CổngGhitừ(registeraddressCổng, 20)
	CổngGhitừ(busĐiềukhiểnregisterdataCổng, 0x102)

	CổngGhitừ(registeraddressCổng, 0)
	CổngGhitừ(registerdataCổng, 0x04)

	initTắcnghẽn.chếđộ = 0x0000
	initTắcnghẽn.sỐGởibuffer = 3
	initTắcnghẽn.sỐrecvbuffer = 3

	initTắcnghẽn.physicaladdress = Mac

	initTắcnghẽn.logicaladdress = 0

	gởibufferMôtả = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&gởibufferMôtảBộnhớ)) + 15) & ^(uintptr)(0xF)))
	initTắcnghẽn.gởibufferMôtảaddress = uintptr(Pointer(&gởibufferMôtả))
	recvbufferMôtả = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferMôtảBộnhớ)) + 15) & ^(uintptr)(0xF)))
	initTắcnghẽn.recvbufferMôtảaddress = uintptr(Pointer(&recvbufferMôtả))

	for i := 0; i < 8; i++ {
		gởibufferMôtả[i].address_2 = uint32((uintptr(Pointer(&gởibuffer[i])) + 15) & ^(uintptr(0xF)))
		gởibufferMôtả[i].cờ = 0x7FF | 0xF000
		gởibufferMôtả[i].cờ2 = 0
		gởibufferMôtả[i].sẵnsàng = 0

		recvbufferMôtả[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferMôtả[i].cờ = 0xF7FF | 0x80000000

	}

	CổngGhitừ(registeraddressCổng, 1)
	CổngGhitừ(registerdataCổng, uint16(uintptr(Pointer(&initTắcnghẽn))&0xFFFF))

	CổngGhitừ(registeraddressCổng, 2)
	CổngGhitừ(registerdataCổng, uint16((uintptr(Pointer(&initTắcnghẽn))>>16)&0xFFFF))

}
func (mình *Tamdam79c973) Bật() {
	CổngGhitừ(registeraddressCổng, 0)
	CổngGhitừ(registerdataCổng, 0x41)

	CổngGhitừ(registeraddressCổng, 4)
	temporary := CổngĐọctừ(registerdataCổng)
	CổngGhitừ(registeraddressCổng, 4)
	CổngGhitừ(registerdataCổng, temporary|0xC00)

	CổngGhitừ(registeraddressCổng, 0)
	CổngGhitừ(registerdataCổng, 0x42)

}
func (mình *Tamdam79c973) Đặtlại() int {
	CổngĐọctừ(đặtlạiCổng)
	CổngGhitừ(đặtlạiCổng, 0)
	return 10
}

var sốlượng uint16 = 0

func (mình *Tamdam79c973) HandleGiánđoạn(esp uint32) uint32 {

	CổngGhitừ(registeraddressCổng, 0)
	temporary := uint32(CổngĐọctừ(registerdataCổng))
	console_2.MIn(([]byte)("interrupt("))
	console_2.MUnsignedinteger32In(esp)
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger32In(temporary)
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger16In(sốlượng)
	sốlượng++
	console_2.MIn(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		console_2.MIn(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		console_2.MIn(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		console_2.MIn(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		console_2.MIn(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		console_2.MIn(([]byte)("am79c973 data received"))
		mình.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		console_2.MIn(([]byte)("am79c973 data sent"))
	}

	CổngGhitừ(registeraddressCổng, 0)
	CổngGhitừ(registerdataCổng, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		console_2.MIn(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (mình *Tamdam79c973) Gởi(dataContrỏ uintptr, cỡ uint32) {
	var gởidescriptor uint16 = uint16(hiệnhànhGởibuffer)
	hiệnhànhGởibuffer = 0

	if cỡ > 1518 {
		cỡ = 1518
	}

	var mãnguồn_2 [4096]byte = *(*([4096]byte))(Pointer(dataContrỏ))
	var destination_2 uint32 = gởibufferMôtả[gởidescriptor].address_2 + cỡ - 1

	for i := 0; i < int(cỡ); i++ {

		*(*byte)(Pointer(uintptr(destination_2))) = mãnguồn_2[int(cỡ)-i-1]

		destination_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataContrỏ))
	console_2.MInxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		console_2.MHexadecimalIn(data[i])
		console_2.MIn(([]byte)(":"))
	}
	console_2.MIn(([]byte)("\n"))

	gởibufferMôtả[gởidescriptor].sẵnsàng = 0
	gởibufferMôtả[gởidescriptor].cờ2 = 0
	gởibufferMôtả[gởidescriptor].cờ = 0x8300F000 | uint32((-cỡ)&0xFFF)

	CổngGhitừ(registeraddressCổng, 0)
	CổngGhitừ(registerdataCổng, 0x48)

}
func (mình *Tamdam79c973) Receive() {
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger32In(uint32(uintptr(Pointer(&gởibuffer))))
	console_2.MIn(([]byte)(":"))
	console_2.MHexadecimalIn(gởibuffer[0][0])
	console_2.MHexadecimalIn(gởibuffer[0][1])
	console_2.MIn(([]byte)(":"))
	hiệnhànhrecvbuffer = 0

	for ; (recvbufferMôtả[hiệnhànhrecvbuffer].cờ & 0x80000000) == 0; hiệnhànhrecvbuffer = (hiệnhànhrecvbuffer + 1) % 8 {

		if !(recvbufferMôtả[hiệnhànhrecvbuffer].cờ&0x40000000 != 0) && ((recvbufferMôtả[hiệnhànhrecvbuffer].cờ & 0x03000000) == 0x03000000) {
			var cỡ uint32 = recvbufferMôtả[hiệnhànhrecvbuffer].cờ & 0xFFF
			if cỡ > 64 {
				cỡ -= 4
			}

			console_2.MIn([]byte(" size : ["))
			console_2.MUnsignedinteger32In(cỡ)
			console_2.MIn([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferMôtả[hiệnhànhrecvbuffer].address_2)))
			var tham_chiếu_địa_chỉ uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Bậtrawdatareceive(tham_chiếu_địa_chỉ, int(cỡ)) {

					console_2.MInxy(([]byte)("self.Send"), 0, 22)

					mình.Gởi(tham_chiếu_địa_chỉ, cỡ)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				console_2.MHexadecimalIn(buffer_2[i])
				console_2.MIn([]byte(":"))
			}

		}
		recvbufferMôtả[hiệnhànhrecvbuffer].cờ2 = 0
		recvbufferMôtả[hiệnhànhrecvbuffer].cờ = 0x8000F7FF
	}
}
func (mình *Tamdam79c973) Đặthandler(handler *TRawdatahandler) {
	mình.handler = handler
}
func (mình *Tamdam79c973) Getmacaddress() uint64 {

	return initTắcnghẽn.physicaladdress
}
func (mình *Tamdam79c973) Đặtipaddress(ip uint64) {
	initTắcnghẽn.logicaladdress = ip
}
func (mình *Tamdam79c973) Getipaddress() uint64 {
	return initTắcnghẽn.logicaladdress
}
