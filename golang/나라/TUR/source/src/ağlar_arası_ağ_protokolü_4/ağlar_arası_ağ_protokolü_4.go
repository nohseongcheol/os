package ağlar_arası_ağ_protokolü_4

import . "unsafe"
import . "util"
import . "konsol"
import . "ortak_ortam_ağ_çerçevesi"
import . "arp"

var ipKonsol TKonsol = TKonsol{}

type Tİnternetprotocolv4İletibuffer struct {
	lenver		byte
	tos		byte
	toplamSüre	[2]byte

	ident		[2]byte
	imlerVEoffset	[2]byte

	saattolive	byte
	protocol	byte
	checksum	[2]byte

	kaynakipaddress	[4]byte
	hedefipaddress	[4]byte
}

var ipBoyut uint8 = (4 + 4 + 4 + 8)

type Tİnternetprotocolv4İleti struct {
	headerSüre	uint8
	sürüm		uint8
	tos		uint8
	toplamSüre	uint16

	ident		uint16
	imlerVEoffset	uint16

	saattolive	uint8
	protocol	uint8
	checksum	uint16

	kaynakipaddress	uint32
	hedefipaddress	uint32
}

func (self *Tİnternetprotocolv4İleti) Init(buffer_2 Tİnternetprotocolv4İletibuffer) {

	self.sürüm = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerSüre = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.toplamSüre = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.toplamSüre))

	self.ident = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.ident))
	self.imlerVEoffset = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.imlerVEoffset))

	self.saattolive = buffer_2.saattolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.checksum))

	self.kaynakipaddress = Unsignedinteger32r(Dizitounsignedinteger32(buffer_2.kaynakipaddress))
	self.hedefipaddress = Unsignedinteger32r(Dizitounsignedinteger32(buffer_2.hedefipaddress))

}
func (self *Tİnternetprotocolv4İleti) Ayarlabuffer(buffer_2 *Tİnternetprotocolv4İletibuffer) {

	buffer_2.lenver = byte(((self.sürüm & 0x0F) << 4) | (self.headerSüre & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.toplamSüre = Unsignedinteger16toDizi(self.toplamSüre)

	buffer_2.ident = Unsignedinteger16toDizi(self.ident)
	buffer_2.imlerVEoffset = Unsignedinteger16toDizi(self.imlerVEoffset)

	buffer_2.saattolive = self.saattolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toDizi(self.checksum)

	buffer_2.kaynakipaddress = Unsignedinteger32toDizi(self.kaynakipaddress)
	buffer_2.hedefipaddress = Unsignedinteger32toDizi(self.hedefipaddress)

}

type Iİnternetprotocolhandler interface {
	Init(backend TAğlar_arası_ağ_protokolü_sağlayıcısı, pihandler Iİnternetprotocolhandler, pprotocol uint8)
	İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder uint32, hedefipaddressAğbyteorder uint32, dataBelirteç uintptr, boyut uint32) bool
	Gönder(hedefipaddressAğbyteorder uint32, pprotocol uint8, dataBelirteç uintptr, boyut uint32)
	Providerget() *TAğlar_arası_ağ_protokolü_sağlayıcısı
}

type Tİnternetprotocolhandler struct {
}

var ipEternetÇerçevehandler IpEternetÇerçevehandler = IpEternetÇerçevehandler{}
var protocol uint8

func (self *Tİnternetprotocolhandler) Init(backend TAğlar_arası_ağ_protokolü_sağlayıcısı, pihandler Iİnternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tİnternetprotocolhandler) İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder uint32, hedefipaddressAğbyteorder uint32, dataBelirteç uintptr, boyut uint32) bool {
	ipKonsol.MYazdır(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tİnternetprotocolhandler) Gönder(hedefipaddressAğbyteorder uint32, pprotocol uint8, dataBelirteç uintptr, boyut uint32) {

	ağlar_arası_ağ_protokolü_sağlayıcısı.Gönder(hedefipaddressAğbyteorder, pprotocol, dataBelirteç, boyut)
}
func (self *Tİnternetprotocolhandler) Providerget() *TAğlar_arası_ağ_protokolü_sağlayıcısı {
	return &ağlar_arası_ağ_protokolü_sağlayıcısı
}

type IpEternetÇerçevehandler struct {
	TEternetÇerçevehandler
}

var ağlar_arası_ağ_protokolü_sağlayıcısı TAğlar_arası_ağ_protokolü_sağlayıcısı

func (self *IpEternetÇerçevehandler) EternetÇerçevereceivewhen(dataBelirteç uintptr, boyut int) bool {
	ipKonsol.MYazdır(([]byte)("iphandler:onEtherfameRecv\n"))
	return ağlar_arası_ağ_protokolü_sağlayıcısı.EternetÇerçevereceivewhen(dataBelirteç, uint32(boyut))

}

func (self *IpEternetÇerçevehandler) Gönder(hedefipaddressAğbyteorder uint64, dataBelirteç uintptr, boyut uint32) {
	ipKonsol.MYazdır(([]byte)("ipefhandler:send\n"))
	var eternetTürbe = Unsignedinteger16r(0x0800)
	self.TEternetÇerçevehandler.ÇerçeveGönder(hedefipaddressAğbyteorder, eternetTürbe, dataBelirteç, boyut)

}

var handler_2 [255]Iİnternetprotocolhandler

type TAğlar_arası_ağ_protokolü_sağlayıcısı struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaske	uint32
}

var efhandler IEternetÇerçevehandler

func (self *TAğlar_arası_ağ_protokolü_sağlayıcısı) Init(pefprovider TOrtak_ortam_ağ_çerçevesi_sağlayıcısı, pefhandler IEternetÇerçevehandler, arp Arpprovider, gatewayip uint32, subnetMaske uint32) {

	efhandler = pefhandler
	efhandler.Ayarlahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetMaske = subnetMaske
	ağlar_arası_ağ_protokolü_sağlayıcısı = *self
}
func (self *TAğlar_arası_ağ_protokolü_sağlayıcısı) EternetÇerçevereceivewhen(eternetÇerçevepayload uintptr, boyut uint32) bool {
	if boyut < uint32(ipBoyut) {
		return false
	}

	var buffer_2 *Tİnternetprotocolv4İletibuffer = (*Tİnternetprotocolv4İletibuffer)(Pointer(eternetÇerçevepayload))
	var internetprotocolİleti Tİnternetprotocolv4İleti
	internetprotocolİleti.Init(*buffer_2)

	var reply bool = false

	if internetprotocolİleti.hedefipaddress == uint32(efhandler.Getipaddress()) {

		var süre uint32 = uint32(internetprotocolİleti.toplamSüre)
		if süre > boyut {
			süre = boyut
		}
		if handler_2[internetprotocolİleti.protocol] != nil {
			reply = handler_2[internetprotocolİleti.protocol].İnternetprotocolreceivewhen(internetprotocolİleti.kaynakipaddress, internetprotocolİleti.hedefipaddress, eternetÇerçevepayload+uintptr(4*internetprotocolİleti.headerSüre), uint32(süre-uint32(4*internetprotocolİleti.headerSüre)))

		}
	}

	if reply {

		var temporary = internetprotocolİleti.hedefipaddress
		internetprotocolİleti.hedefipaddress = internetprotocolİleti.kaynakipaddress
		internetprotocolİleti.kaynakipaddress = temporary

		internetprotocolİleti.saattolive = 0x40
		internetprotocolİleti.checksum = 0

		internetprotocolİleti.Ayarlabuffer(buffer_2)
		internetprotocolİleti.checksum = self.Checksum((*([4096]uint16))(Pointer(eternetÇerçevepayload)), uint32(4*internetprotocolİleti.headerSüre))

		internetprotocolİleti.Ayarlabuffer(buffer_2)

	}

	ipKonsol.MYazdır(([]byte)("ipmessage"))
	ipKonsol.MUnsignedinteger32Yazdır(internetprotocolİleti.kaynakipaddress)
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MUnsignedinteger32Yazdır(internetprotocolİleti.hedefipaddress)
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Yazdır(uint16(internetprotocolİleti.headerSüre))
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Yazdır(uint16(internetprotocolİleti.sürüm))
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MUnsignedinteger16Yazdır(internetprotocolİleti.toplamSüre)
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MUnsignedinteger32Yazdır(uint32(efhandler.Getipaddress()))
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MYazdır(([]byte)("\n"))

	return reply

}
func (self *TAğlar_arası_ağ_protokolü_sağlayıcısı) Gönder(hedefipaddressAğbyteorder uint32, protocol uint8, dataBelirteç uintptr, boyut uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tİnternetprotocolv4İletibuffer = (*Tİnternetprotocolv4İletibuffer)(Pointer(&buffer1_2))
	var ileti Tİnternetprotocolv4İleti = Tİnternetprotocolv4İleti{}
	ileti.sürüm = 4
	ileti.headerSüre = ipBoyut / 4
	ileti.tos = 0
	ileti.toplamSüre = Unsignedinteger16r(uint16(boyut + uint32(ipBoyut)))

	ileti.ident = 0x0100
	ileti.imlerVEoffset = 0x0040
	ileti.saattolive = 0x40
	ileti.protocol = protocol

	ileti.hedefipaddress = hedefipaddressAğbyteorder

	ileti.kaynakipaddress = uint32(efhandler.Getipaddress())

	ileti.checksum = 0

	ileti.Ayarlabuffer(buffer_2)
	ileti.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipBoyut))
	ileti.Ayarlabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataBelirteç))

	for i := 0; i < int(boyut); i++ {

		buffer1_2[i+int(ipBoyut)] = databuffer_2[i]
	}

	ipKonsol.MYazdırxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(boyut)+int(ipBoyut); i++ {
		ipKonsol.MHexadecimalYazdır(buffer1_2[i])
	}
	ipKonsol.MYazdır(([]byte)(":"))
	ipKonsol.MYazdır(([]byte)("]\n"))

	var sonrakihopipaddressAğbyteorder uint32 = hedefipaddressAğbyteorder
	if (hedefipaddressAğbyteorder & self.SubnetMaske) != (ileti.kaynakipaddress & self.SubnetMaske) {
		sonrakihopipaddressAğbyteorder = self.Gatewayip
	}

	var gönderdataBelirteç = uintptr(Pointer(&buffer1_2))
	ipKonsol.MUnsignedinteger32Yazdır(sonrakihopipaddressAğbyteorder)

	var eternetTürbe = Unsignedinteger16r(0x0800)
	efhandler.ÇerçeveGönder(self.arpprovider.Resolve(sonrakihopipaddressAğbyteorder), eternetTürbe, gönderdataBelirteç, uint32(ipBoyut)+uint32(boyut))

}
func (self *TAğlar_arası_ağ_protokolü_sağlayıcısı) Checksum(pdata *[4096]uint16, süreGelenBayt uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBayt [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (süreGelenBayt % 2) != 0 {
		temporary += uint32(uint16(dataBayt[süreGelenBayt-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TAğlar_arası_ağ_protokolü_sağlayıcısı) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
