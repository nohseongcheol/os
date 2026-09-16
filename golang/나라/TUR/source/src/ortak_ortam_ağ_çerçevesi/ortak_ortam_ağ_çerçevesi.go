/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ortak_ortam_ağ_çerçevesi

import . "konsol"

import . "amdam79c973"
import . "unsafe"
import . "util"

var eternetKonsol TKonsol = TKonsol{}

type TEternetÇerçeveheaderbuffer struct {
	hedefmacbe	[6]byte
	kaynakmacbe	[6]byte
	eternetTürbe	[2]byte
}

var çerçeveheaderBoyut int = 14

type TOrtak_ortam_ağ_çerçevesi_başlığı struct {
	hedefmacbe	uint64
	kaynakmacbe	uint64
	eternetTürbe	uint16
}

func (self *TOrtak_ortam_ağ_çerçevesi_başlığı) Init(buffer_2 TEternetÇerçeveheaderbuffer) {
	self.hedefmacbe = (Dizitounsignedinteger48(buffer_2.hedefmacbe))
	self.kaynakmacbe = (Dizitounsignedinteger48(buffer_2.kaynakmacbe))
	self.eternetTürbe = (Dizitounsignedinteger16(buffer_2.eternetTürbe))

}
func (self *TOrtak_ortam_ağ_çerçevesi_başlığı) Ayarlabuffer(buffer_2 *TEternetÇerçeveheaderbuffer) {
	buffer_2.hedefmacbe = Unsignedinteger48toDizi(Unsignedinteger48r(self.hedefmacbe))
	buffer_2.kaynakmacbe = Unsignedinteger48toDizi(Unsignedinteger48r(self.kaynakmacbe))
	buffer_2.eternetTürbe = Unsignedinteger16toDizi(Unsignedinteger16r(self.eternetTürbe))
}

type IEternetÇerçevehandler interface {
	Init(backend TOrtak_ortam_ağ_çerçevesi_sağlayıcısı)
	Ayarlahandler(handler IEternetÇerçevehandler, eternetTür uint16)
	EternetÇerçevereceivewhen(dataBelirteç uintptr, boyut int) bool
	Gönder(hedefmacbe uint64, dataBelirteç uintptr, boyut uint32)
	ÇerçeveGönder(hedefmacbe uint64, eternetTürbe uint16, dataBelirteç uintptr, boyut uint32)
	Providerget() TOrtak_ortam_ağ_çerçevesi_sağlayıcısı
	Getmacaddress() uint64
	Getipaddress() uint64
}

type TEternetÇerçevehandler struct {
}

var çerçeve TOrtak_ortam_ağ_çerçevesi_başlığı
var Backend TOrtak_ortam_ağ_çerçevesi_sağlayıcısı
var handler_2 [65535]IEternetÇerçevehandler
var efhandler *TEternetÇerçevehandler = nil

func (self *TEternetÇerçevehandler) Init(backend TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) {
	Backend = backend
}

func (self *TEternetÇerçevehandler) Ayarlahandler(handler IEternetÇerçevehandler, pEternetTür uint16) {
	handler_2[pEternetTür] = handler
}
func (self *TEternetÇerçevehandler) Ayarlabackend(backend TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) {
	Backend = backend
}
func (self *TEternetÇerçevehandler) Getbackend() TOrtak_ortam_ağ_çerçevesi_sağlayıcısı {
	return Backend
}
func (self *TEternetÇerçevehandler) EternetÇerçevereceivewhen(dataBelirteç uintptr, boyut int) bool {
	eternetKonsol.MYazdır(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *TEternetÇerçevehandler) Gönder(hedefmacbe uint64, dataBelirteç uintptr, boyut uint32) {
	Backend.ÇerçeveGönder(hedefmacbe, çerçeve.eternetTürbe, dataBelirteç, boyut)
}
func (self *TEternetÇerçevehandler) ÇerçeveGönder(hedefmacbe uint64, eternetTürbe uint16, dataBelirteç uintptr, boyut uint32) {
	Backend.ÇerçeveGönder(hedefmacbe, eternetTürbe, dataBelirteç, boyut)
}
func (self *TEternetÇerçevehandler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *TEternetÇerçevehandler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *TEternetÇerçevehandler) Providerget() TOrtak_ortam_ağ_çerçevesi_sağlayıcısı {
	return Backend
}

type TEternetÇerçeverawdatahandler struct {
	TRawdatahandler
}

var provider TOrtak_ortam_ağ_çerçevesi_sağlayıcısı

func (self *TEternetÇerçeverawdatahandler) Init(pprovider TOrtak_ortam_ağ_çerçevesi_sağlayıcısı, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *TEternetÇerçeverawdatahandler) Açıkrawdatareceive(dataBelirteç uintptr, boyut int) bool {
	return provider.Açıkrawdatareceive(dataBelirteç, boyut)
}
func (self *TEternetÇerçeverawdatahandler) Gönder(dataBelirteç uintptr, boyut uint32) {
	provider.Gönder(dataBelirteç, boyut)
}
func (self *TEternetÇerçeverawdatahandler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *TEternetÇerçeverawdatahandler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *TEternetÇerçeverawdatahandler) Providerget() TOrtak_ortam_ağ_çerçevesi_sağlayıcısı {
	return provider
}

type TOrtak_ortam_ağ_çerçevesi_sağlayıcısı struct {
	ağKart		Tamdam79c973
	handler_2	[65565]IEternetÇerçevehandler
}

func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) Init(backend Tamdam79c973) {

	self.ağKart = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var count uint16 = 0

func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) Açıkrawdatareceive(dataBelirteç uintptr, boyut int) bool {

	var buffer_2 *TEternetÇerçeveheaderbuffer = (*TEternetÇerçeveheaderbuffer)(Pointer(dataBelirteç))
	var çerçeve TOrtak_ortam_ağ_çerçevesi_başlığı = TOrtak_ortam_ağ_çerçevesi_başlığı{}
	çerçeve.Init(*buffer_2)
	var reply bool = false

	if çerçeve.hedefmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(çerçeve.hedefmacbe) == self.Getmacaddress() {
		if handler_2[çerçeve.eternetTürbe] != nil {
			eternetKonsol.MYazdır(([]byte)("provider\n"))

			var adres_başvurusu uintptr = uintptr(Pointer(dataBelirteç)) + uintptr(çerçeveheaderBoyut)
			reply = handler_2[çerçeve.eternetTürbe].EternetÇerçevereceivewhen(adres_başvurusu, boyut-çerçeveheaderBoyut)

		}
	}

	if reply {
		çerçeve.hedefmacbe = çerçeve.kaynakmacbe
		çerçeve.kaynakmacbe = Unsignedinteger48r(self.Getmacaddress())
		çerçeve.Ayarlabuffer(buffer_2)

	}

	eternetKonsol.MYazdırxy(([]byte)("spro["), 0, 1)
	eternetKonsol.MUnsignedinteger64Yazdır(çerçeve.kaynakmacbe)
	eternetKonsol.MYazdır(([]byte)(":"))
	eternetKonsol.MUnsignedinteger64Yazdır(çerçeve.hedefmacbe)
	eternetKonsol.MYazdır(([]byte)(":]["))
	eternetKonsol.MUnsignedinteger64Yazdır(self.Getmacaddress())
	eternetKonsol.MYazdır(([]byte)(":"))
	eternetKonsol.MUnsignedinteger16Yazdır(çerçeve.eternetTürbe)
	eternetKonsol.MYazdır(([]byte)("]"))

	return reply

}
func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) Gönder(dataBelirteç uintptr, boyut uint32) {
	self.ağKart.Gönder(dataBelirteç, boyut)
}
func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) ÇerçeveGönder(hedefmacbe uint64, eternetTürbe uint16, dataBelirteç uintptr, boyut uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEternetÇerçeveheaderbuffer = (*TEternetÇerçeveheaderbuffer)(Pointer(&buffer2_2))

	var çerçeve TOrtak_ortam_ağ_çerçevesi_başlığı = TOrtak_ortam_ağ_çerçevesi_başlığı{}
	çerçeve.Init(*buffer_2)

	çerçeve.hedefmacbe = Unsignedinteger48r(hedefmacbe)
	çerçeve.kaynakmacbe = Unsignedinteger48r(self.ağKart.Getmacaddress())
	çerçeve.eternetTürbe = Unsignedinteger16r(eternetTürbe)

	çerçeve.Ayarlabuffer(buffer_2)
	var kaynak_2 [4096]byte = *(*([4096]byte))(Pointer(dataBelirteç))

	var i uint32 = 0
	for i = 0; i < boyut; i++ {
		buffer2_2[uint32(çerçeveheaderBoyut)+i] = kaynak_2[i]

	}

	var adres_başvurusu uintptr = uintptr(Pointer(&buffer2_2))

	self.ağKart.Gönder(adres_başvurusu, boyut+uint32(çerçeveheaderBoyut))

}
func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) Getmacaddress() uint64 {
	return self.ağKart.Getmacaddress()
}
func (self *TOrtak_ortam_ağ_çerçevesi_sağlayıcısı) Getipaddress() uint64 {
	return self.ağKart.Getipaddress()
}
