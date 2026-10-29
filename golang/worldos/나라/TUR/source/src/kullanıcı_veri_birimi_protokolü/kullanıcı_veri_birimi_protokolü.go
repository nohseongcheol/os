/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package kullanıcı_veri_birimi_protokolü

import . "unsafe"
import . "konsol"
import . "util"
import . "bellekmanager"
import . "ağlar_arası_ağ_protokolü_4"

var udpKonsol = TKonsol{}

type TKullanıcıdatagramprotocolheaderbuffer struct {
	kaynak_kapı_numarası	[2]byte
	hedef_kapı_numarası	[2]byte

	süre		[2]byte
	checksum	[2]byte
}

var udpheaderBoyut uint32 = 8

type TKullanıcı_veri_birimi_başlığı struct {
	kaynak_kapı_numarası	uint16
	hedef_kapı_numarası	uint16

	süre		uint16
	checksum	uint16
}

func (self *TKullanıcı_veri_birimi_başlığı) Init(buffer_2 *TKullanıcıdatagramprotocolheaderbuffer) {
	self.kaynak_kapı_numarası = Dizitounsignedinteger16(buffer_2.kaynak_kapı_numarası)
	self.hedef_kapı_numarası = Dizitounsignedinteger16(buffer_2.hedef_kapı_numarası)

	self.süre = Dizitounsignedinteger16(buffer_2.süre)
	self.checksum = Dizitounsignedinteger16(buffer_2.checksum)
}
func (self *TKullanıcı_veri_birimi_başlığı) Ayarlabuffer(buffer_2 *TKullanıcıdatagramprotocolheaderbuffer) {

	buffer_2.kaynak_kapı_numarası = Unsignedinteger16toDizi(self.kaynak_kapı_numarası)
	buffer_2.hedef_kapı_numarası = Unsignedinteger16toDizi(self.hedef_kapı_numarası)

	buffer_2.süre = Unsignedinteger16toDizi(self.süre)
	buffer_2.checksum = Unsignedinteger16toDizi(self.checksum)

}

type IKullanıcıdatagramprotocolhandler interface {
	HandleKullanıcıdatagramprotocolİleti(yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası, data uintptr, boyut uint16)
}

type TKullanıcıdatagramprotocolhandler struct {
}

func (self *TKullanıcıdatagramprotocolhandler) Init(backend TAğlar_arası_ağ_protokolü_sağlayıcısı) {
}
func (self *TKullanıcıdatagramprotocolhandler) HandleKullanıcıdatagramprotocolİleti(yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası, data uintptr, boyut uint16) {
}

type IKullanıcıdatagramprotocolYuva interface {
	HandleKullanıcıdatagramprotocolİleti(data uintptr, boyut uint16)
}
type TKullanıcı_veri_birimi_iletişim_uç_noktası struct {
	uzakBağlantıNoktasıSayı		uint16
	uzakip				uint32
	yerelBağlantıNoktasıSayı	uint16
	yerelip				uint32

	listening	bool
}

var udpprovider TKullanıcıdatagramprotocolprovider
var udphandler IKullanıcıdatagramprotocolhandler

func (self *TKullanıcı_veri_birimi_iletişim_uç_noktası) Dene() {
}
func (self *TKullanıcı_veri_birimi_iletişim_uç_noktası) Init(pudpprovider TKullanıcıdatagramprotocolprovider, pudphandler IKullanıcıdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *TKullanıcı_veri_birimi_iletişim_uç_noktası) HandleKullanıcıdatagramprotocolİleti(data uintptr, boyut uint16) {
	if udphandler != nil {
		udphandler.HandleKullanıcıdatagramprotocolİleti(self, data, boyut)
	}
}
func (self *TKullanıcı_veri_birimi_iletişim_uç_noktası) Gönder(pdata []byte, boyut uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(boyut); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Gönder(self, data, boyut)
}
func (self *TKullanıcı_veri_birimi_iletişim_uç_noktası) BağlantıyıKes() {
	udpprovider.BağlantıyıKes(self)
}

type TKullanıcıdatagramprotocolprovider struct {
}

var iphandler Iİnternetprotocolhandler
var sockets [65535]TKullanıcı_veri_birimi_iletişim_uç_noktası
var sayısockets int
var boşBağlantıNoktası uint16

func (self *TKullanıcıdatagramprotocolprovider) Init(pipprovider TAğlar_arası_ağ_protokolü_sağlayıcısı, piphandler Iİnternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	sayısockets = 0
	boşBağlantıNoktası = 1024
}
func (self *TKullanıcıdatagramprotocolprovider) İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder uint32, hedefipaddressAğbyteorder uint32, internetprotocolpayload uintptr, boyut uint32) bool {
	if boyut < udpheaderBoyut {
		return false
	}

	var buffer_2 *TKullanıcıdatagramprotocolheaderbuffer = (*TKullanıcıdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKullanıcı_veri_birimi_başlığı
	msg.Init(buffer_2)

	var yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası = nil

	for i := 0; i < sayısockets && yuva == nil; i++ {
		if sockets[i].yerelBağlantıNoktasıSayı == msg.hedef_kapı_numarası && sockets[i].yerelip == hedefipaddressAğbyteorder && sockets[i].listening == true {
			yuva = &sockets[i]
			yuva.listening = false
			yuva.uzakBağlantıNoktasıSayı = msg.kaynak_kapı_numarası
			yuva.uzakip = kaynakipaddressAğbyteorder
		} else if sockets[i].yerelBağlantıNoktasıSayı == msg.hedef_kapı_numarası && sockets[i].yerelip == hedefipaddressAğbyteorder && sockets[i].uzakBağlantıNoktasıSayı == msg.kaynak_kapı_numarası && sockets[i].uzakip == kaynakipaddressAğbyteorder {
			yuva = &sockets[i]

		}
	}

	msg.Ayarlabuffer(buffer_2)
	if yuva != nil {
		yuva.HandleKullanıcıdatagramprotocolİleti(internetprotocolpayload+uintptr(udpheaderBoyut), uint16(boyut-udpheaderBoyut))
	}

	return false
}

func (self *TKullanıcıdatagramprotocolprovider) Bağlan(ip uint32, bağlantıNoktası uint16) *TKullanıcı_veri_birimi_iletişim_uç_noktası {
	var bellekmanager = &TBellekmanager{}
	var yuva = (*TKullanıcı_veri_birimi_iletişim_uç_noktası)(bellekmanager.Bellek_ayır(50))

	if yuva != nil {

		yuva.Init(*self, nil)
		yuva.uzakBağlantıNoktasıSayı = bağlantıNoktası
		yuva.uzakip = ip
		yuva.yerelBağlantıNoktasıSayı = boşBağlantıNoktası
		boşBağlantıNoktası++
		yuva.yerelip = uint32((*iphandler.Providerget()).Getipaddress())

		yuva.uzakBağlantıNoktasıSayı = Unsignedinteger16r(yuva.uzakBağlantıNoktasıSayı)
		yuva.yerelBağlantıNoktasıSayı = Unsignedinteger16r(yuva.yerelBağlantıNoktasıSayı)

		sockets[sayısockets] = *yuva
		sayısockets++

	}
	return yuva

}
func (self *TKullanıcıdatagramprotocolprovider) Listen(bağlantıNoktası uint16) *TKullanıcı_veri_birimi_iletişim_uç_noktası {
	var yuva = &TKullanıcı_veri_birimi_iletişim_uç_noktası{}
	yuva = nil
	if yuva != nil {
		yuva.Init(*self, nil)
		yuva.listening = true
		yuva.yerelBağlantıNoktasıSayı = bağlantıNoktası
		yuva.yerelip = uint32((*iphandler.Providerget()).Getipaddress())

		yuva.yerelBağlantıNoktasıSayı = Unsignedinteger16r(yuva.yerelBağlantıNoktasıSayı)
	}
	return yuva
}
func (self *TKullanıcıdatagramprotocolprovider) BağlantıyıKes(yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası) {
	for i := 0; i < sayısockets && yuva == nil; i++ {
		if sockets[i] == *yuva {
			sayısockets--
			sockets[i] = sockets[sayısockets]
			break
		}
	}
}
func (self *TKullanıcıdatagramprotocolprovider) Gönder(yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası, pdata uintptr, boyut uint16) {
	var toplamSüre = uint32(boyut) + udpheaderBoyut

	var buffer_2 [4096]byte

	var msgbuffer = (*TKullanıcıdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKullanıcı_veri_birimi_başlığı{}

	msg.kaynak_kapı_numarası = yuva.yerelBağlantıNoktasıSayı
	msg.hedef_kapı_numarası = yuva.uzakBağlantıNoktasıSayı
	msg.süre = Unsignedinteger16r(uint16(toplamSüre))

	msg.checksum = 0x0
	msg.Ayarlabuffer(msgbuffer)

	var dataBayt [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(boyut); i++ {
		buffer_2[int(udpheaderBoyut)+i] = dataBayt[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Gönder(yuva.uzakip, 0x11, data, toplamSüre)

}
func (self *TKullanıcıdatagramprotocolprovider) Bind(yuva *TKullanıcı_veri_birimi_iletişim_uç_noktası, handler *TKullanıcıdatagramprotocolhandler,) {
}
