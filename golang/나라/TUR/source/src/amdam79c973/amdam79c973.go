/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package amdam79c973

import . "unsafe"
import . "kesme"
import . "konsol"
import . "bağlantıNoktası"
import . "pci"

var ağKartKonsol TKonsol = TKonsol{}

type TInitializationBlok struct {
	kİP			uint16
	sayıGönderbuffer	uint8
	sayırecvbuffer		uint8

	physicaladdress	uint64

	mantıksaladdress		uint64
	recvbufferAçıklamaaddress	uintptr
	gönderbufferAçıklamaaddress	uintptr
}
type TBufferdescriptor struct {
	address_2	uint32
	imler		uint32
	imler2		uint32
	ulaşılabilir	uint32
}

type IRawdatahandler interface {
	Açıkrawdatareceive(dataBelirteç uintptr, boyut int) bool
	Gönder(dataBelirteç uintptr, boyut uint32)
}

var rawdatabackend Tamdam79c973

type TRawdatahandler struct {
}

func (self *TRawdatahandler) Ayarlabackend(backend Tamdam79c973) {

	rawdatabackend = backend
}
func (self *TRawdatahandler) Getbackend() Tamdam79c973 {
	return rawdatabackend
}
func (self *TRawdatahandler) Açıkrawdatareceive(dataBelirteç uintptr, boyut int) bool {
	ağKartKonsol.MYazdırxy(([]byte)("TRawDataRecv"), 1, 20)
	return true
}

func (self *TRawdatahandler) Gönder(dataBelirteç uintptr, boyut uint32) {
	ağKartKonsol.MYazdırxy(([]byte)("TRawDataSend"), 10, 10)
	rawdatabackend.Gönder(dataBelirteç, boyut)
}

var Macaddress0BağlantıNoktası uint16
var Macaddress2BağlantıNoktası uint16
var Macaddress4BağlantıNoktası uint16
var registerdataBağlantıNoktası uint16
var registeraddressBağlantıNoktası uint16
var sıfırlaBağlantıNoktası uint16
var busCtrlregisterdataBağlantıNoktası uint16

var initBlok TInitializationBlok

var gönderbufferAçıklama [8]TBufferdescriptor
var gönderbufferAçıklamaBellek [2048 + 15]byte
var gönderbuffer [2*1024 + 15][8]uint8
var şuanGönderbuffer uint8

var recvbufferAçıklama [8]TBufferdescriptor
var recvbufferAçıklamaBellek [2048 + 15]uint8
var recvbuffer [2*1024 + 15][8]uint8
var şuanrecvbuffer uint8
var funcDeğer func(*Tamdam79c973, uint32) uint32

type Tamdam79c973 struct {
	TKesmehandler
	aygıtdescriptor	TPeripheralcomponentinterconnectAygıtdescriptor
	kesme		*TKesmemanager
	handler		*TRawdatahandler
}

var konsol_2 TKonsol = TKonsol{}
var irawdatahandler IRawdatahandler

func (self *Tamdam79c973) Initdriver(kesme *TKesmemanager, aygıtdescriptor TPeripheralcomponentinterconnectAygıtdescriptor, handler IRawdatahandler) {

	self.aygıtdescriptor = aygıtdescriptor

	funcDeğer = (*Tamdam79c973).HandleKesme
	var address uintptr
	address = uintptr(Pointer(&funcDeğer))

	self.Init(uint8(0x20+aygıtdescriptor.Kesme), uintptr(Pointer(kesme)), address)

	Macaddress0BağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase)
	Macaddress2BağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x02
	Macaddress4BağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x04
	registerdataBağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x10
	registeraddressBağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x12
	sıfırlaBağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x14
	busCtrlregisterdataBağlantıNoktası = uint16(aygıtdescriptor.BağlantıNoktasıbase) + 0x16

	irawdatahandler = &TRawdatahandler{}
	if handler != nil {
		irawdatahandler = handler
	}

	şuanGönderbuffer = 0
	şuanrecvbuffer = 0

	var Mac0 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress0BağlantıNoktası) % 256)
	var Mac1 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress0BağlantıNoktası) / 256)
	var Mac2 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress2BağlantıNoktası) % 256)
	var Mac3 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress2BağlantıNoktası) / 256)
	var Mac4 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress4BağlantıNoktası) % 256)
	var Mac5 uint64 = uint64(BağlantıNoktasıOkumakelime(Macaddress4BağlantıNoktası) / 256)

	var Mac uint64 = (Mac5 << 40) | (Mac4 << 32) | (Mac3 << 24) | (Mac2 << 16) | (Mac1 << 8) | Mac0

	var macaddress uint64 = (Mac0 << 40) | (Mac1 << 32) | (Mac2 << 24) | (Mac3 << 16) | (Mac4 << 8) | Mac5

	konsol_2.MYazdırxy(([]byte)("[interrupt num : "), 0, 13)
	konsol_2.MHexadecimalYazdır(uint8(aygıtdescriptor.Kesme))
	konsol_2.MYazdır(([]byte)("]"))
	konsol_2.MYazdır(([]byte)("[mac address : "))
	konsol_2.MUnsignedinteger16Yazdır(uint16(macaddress >> 32))
	konsol_2.MUnsignedinteger32Yazdır(uint32(macaddress & 0x00000000FFFFFFFF))
	konsol_2.MYazdır(([]byte)("]"))

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 20)
	BağlantıNoktasıYazmakelime(busCtrlregisterdataBağlantıNoktası, 0x102)

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, 0x04)

	initBlok.kİP = 0x0000
	initBlok.sayıGönderbuffer = 3
	initBlok.sayırecvbuffer = 3

	initBlok.physicaladdress = Mac

	initBlok.mantıksaladdress = 0

	gönderbufferAçıklama = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&gönderbufferAçıklamaBellek)) + 15) & ^(uintptr)(0xF)))
	initBlok.gönderbufferAçıklamaaddress = uintptr(Pointer(&gönderbufferAçıklama))
	recvbufferAçıklama = *(*([8]TBufferdescriptor))(Pointer((uintptr((Pointer)(&recvbufferAçıklamaBellek)) + 15) & ^(uintptr)(0xF)))
	initBlok.recvbufferAçıklamaaddress = uintptr(Pointer(&recvbufferAçıklama))

	for i := 0; i < 8; i++ {
		gönderbufferAçıklama[i].address_2 = uint32((uintptr(Pointer(&gönderbuffer[i])) + 15) & ^(uintptr(0xF)))
		gönderbufferAçıklama[i].imler = 0x7FF | 0xF000
		gönderbufferAçıklama[i].imler2 = 0
		gönderbufferAçıklama[i].ulaşılabilir = 0

		recvbufferAçıklama[i].address_2 = uint32((uintptr(Pointer(&recvbuffer[i])) + 15) & ^(uintptr(0xF)))
		recvbufferAçıklama[i].imler = 0xF7FF | 0x80000000

	}

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 1)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, uint16(uintptr(Pointer(&initBlok))&0xFFFF))

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 2)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, uint16((uintptr(Pointer(&initBlok))>>16)&0xFFFF))

}
func (self *Tamdam79c973) Etkinleştir() {
	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, 0x41)

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 4)
	temporary := BağlantıNoktasıOkumakelime(registerdataBağlantıNoktası)
	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 4)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, temporary|0xC00)

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, 0x42)

}
func (self *Tamdam79c973) Sıfırla() int {
	BağlantıNoktasıOkumakelime(sıfırlaBağlantıNoktası)
	BağlantıNoktasıYazmakelime(sıfırlaBağlantıNoktası, 0)
	return 10
}

var count uint16 = 0

func (self *Tamdam79c973) HandleKesme(esp uint32) uint32 {

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	temporary := uint32(BağlantıNoktasıOkumakelime(registerdataBağlantıNoktası))
	konsol_2.MYazdır(([]byte)("interrupt("))
	konsol_2.MUnsignedinteger32Yazdır(esp)
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger32Yazdır(temporary)
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger16Yazdır(count)
	count++
	konsol_2.MYazdır(([]byte)(")"))

	if (temporary & 0x8000) == 0x8000 {
		konsol_2.MYazdır(([]byte)("am79c973 error"))
	}
	if (temporary & 0x2000) == 0x2000 {
		konsol_2.MYazdır(([]byte)("am79c973 collision error"))
	}
	if (temporary & 0x1000) == 0x1000 {
		konsol_2.MYazdır(([]byte)("am79c973 missed frame"))
	}
	if (temporary & 0x0800) == 0x0800 {
		konsol_2.MYazdır(([]byte)("am79c973 memory error"))
	}
	if (temporary & 0x0400) == 0x0400 {
		konsol_2.MYazdır(([]byte)("am79c973 data received"))
		self.Receive()
	}
	if (temporary & 0x0200) == 0x0200 {
		konsol_2.MYazdır(([]byte)("am79c973 data sent"))
	}

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, uint16(temporary))

	if (temporary & 0x0100) == 0x0100 {
		konsol_2.MYazdır(([]byte)("[netcard(am79c973) init done]"))
	}
	return esp
}

func (self *Tamdam79c973) Gönder(dataBelirteç uintptr, boyut uint32) {
	var gönderdescriptor uint16 = uint16(şuanGönderbuffer)
	şuanGönderbuffer = 0

	if boyut > 1518 {
		boyut = 1518
	}

	var kaynak_2 [4096]byte = *(*([4096]byte))(Pointer(dataBelirteç))
	var hedef_2 uint32 = gönderbufferAçıklama[gönderdescriptor].address_2 + boyut - 1

	for i := 0; i < int(boyut); i++ {

		*(*byte)(Pointer(uintptr(hedef_2))) = kaynak_2[int(boyut)-i-1]

		hedef_2--
	}

	var data [4096]byte = *(*([4096]byte))(Pointer(dataBelirteç))
	konsol_2.MYazdırxy(([]byte)("send packet"), 0, 2)
	for i := 0; i < 64; i++ {
		konsol_2.MHexadecimalYazdır(data[i])
		konsol_2.MYazdır(([]byte)(":"))
	}
	konsol_2.MYazdır(([]byte)("\n"))

	gönderbufferAçıklama[gönderdescriptor].ulaşılabilir = 0
	gönderbufferAçıklama[gönderdescriptor].imler2 = 0
	gönderbufferAçıklama[gönderdescriptor].imler = 0x8300F000 | uint32((-boyut)&0xFFF)

	BağlantıNoktasıYazmakelime(registeraddressBağlantıNoktası, 0)
	BağlantıNoktasıYazmakelime(registerdataBağlantıNoktası, 0x48)

}
func (self *Tamdam79c973) Receive() {
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(&gönderbuffer))))
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MHexadecimalYazdır(gönderbuffer[0][0])
	konsol_2.MHexadecimalYazdır(gönderbuffer[0][1])
	konsol_2.MYazdır(([]byte)(":"))
	şuanrecvbuffer = 0

	for ; (recvbufferAçıklama[şuanrecvbuffer].imler & 0x80000000) == 0; şuanrecvbuffer = (şuanrecvbuffer + 1) % 8 {

		if !(recvbufferAçıklama[şuanrecvbuffer].imler&0x40000000 != 0) && ((recvbufferAçıklama[şuanrecvbuffer].imler & 0x03000000) == 0x03000000) {
			var boyut uint32 = recvbufferAçıklama[şuanrecvbuffer].imler & 0xFFF
			if boyut > 64 {
				boyut -= 4
			}

			konsol_2.MYazdır([]byte(" size : ["))
			konsol_2.MUnsignedinteger32Yazdır(boyut)
			konsol_2.MYazdır([]byte("]"))

			var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(uintptr(recvbufferAçıklama[şuanrecvbuffer].address_2)))
			var adres_başvurusu uintptr = uintptr(Pointer(&buffer_2))
			if irawdatahandler != nil {
				if irawdatahandler.Açıkrawdatareceive(adres_başvurusu, int(boyut)) {

					konsol_2.MYazdırxy(([]byte)("self.Send"), 0, 22)

					self.Gönder(adres_başvurusu, boyut)
				}
			}

			var i uint32
			for i = 0; i < 64; i++ {
				konsol_2.MHexadecimalYazdır(buffer_2[i])
				konsol_2.MYazdır([]byte(":"))
			}

		}
		recvbufferAçıklama[şuanrecvbuffer].imler2 = 0
		recvbufferAçıklama[şuanrecvbuffer].imler = 0x8000F7FF
	}
}
func (self *Tamdam79c973) Ayarlahandler(handler *TRawdatahandler) {
	self.handler = handler
}
func (self *Tamdam79c973) Getmacaddress() uint64 {

	return initBlok.physicaladdress
}
func (self *Tamdam79c973) Ayarlaipaddress(ip uint64) {
	initBlok.mantıksaladdress = ip
}
func (self *Tamdam79c973) Getipaddress() uint64 {
	return initBlok.mantıksaladdress
}
