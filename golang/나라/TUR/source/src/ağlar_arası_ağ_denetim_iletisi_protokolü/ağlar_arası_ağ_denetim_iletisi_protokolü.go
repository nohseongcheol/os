package ağlar_arası_ağ_denetim_iletisi_protokolü

import . "unsafe"
import . "konsol"
import . "bellekmanager"
import . "ortak_ortam_ağ_çerçevesi"
import . "ağlar_arası_ağ_protokolü_4"
import . "util"

var icmpKonsol = TKonsol{}

type TİnternetCtrlİletiprotocolİletibuffer struct {
	Tür	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpBoyut int = 64

type TİnternetCtrlİletiprotocolİleti struct {
	Tür	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (self *TİnternetCtrlİletiprotocolİleti) Init(buffer_2 TİnternetCtrlİletiprotocolİletibuffer) {
	self.Tür = buffer_2.Tür
	self.code = buffer_2.code

	self.checksum = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.checksum))
	self.data = Unsignedinteger32r(Dizitounsignedinteger32(buffer_2.data))
}

func (self *TİnternetCtrlİletiprotocolİleti) Ayarlabuffer(buffer_2 *TİnternetCtrlİletiprotocolİletibuffer) {
	buffer_2.Tür = self.Tür
	buffer_2.code = self.code

	buffer_2.checksum = Unsignedinteger16toDizi(self.checksum)
	buffer_2.data = Unsignedinteger32toDizi(self.data)
}

type Icmphandler struct {
	Tİnternetprotocolhandler
}

var ağlar_arası_ağ_denetim_iletisi_protokolü *TAğlar_arası_ağ_denetim_iletisi_protokolü

func (self *Icmphandler) İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder uint32, hedefipaddressAğbyteorder uint32, dataBelirteç uintptr, boyut uint32) bool {
	return ağlar_arası_ağ_denetim_iletisi_protokolü.İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder, hedefipaddressAğbyteorder, dataBelirteç, boyut)
}

var iphandler Iİnternetprotocolhandler

type TAğlar_arası_ağ_denetim_iletisi_protokolü struct {
}

func (self *TAğlar_arası_ağ_denetim_iletisi_protokolü) Init(backend TAğlar_arası_ağ_protokolü_sağlayıcısı, handler Iİnternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	ağlar_arası_ağ_denetim_iletisi_protokolü = self
}
func (self *TAğlar_arası_ağ_denetim_iletisi_protokolü) İnternetprotocolreceivewhen(kaynakipaddressAğbyteorder uint32, hedefipaddressAğbyteorder uint32, dataBelirteç uintptr, boyut uint32) bool {
	if boyut < uint32(icmpBoyut) {
		return false
	}

	var buffer_2 *TİnternetCtrlİletiprotocolİletibuffer = (*TİnternetCtrlİletiprotocolİletibuffer)(Pointer(dataBelirteç))
	var msg TİnternetCtrlİletiprotocolİleti = TİnternetCtrlİletiprotocolİleti{}
	msg.Init(*buffer_2)

	icmpKonsol.MYazdır(([]byte)("icmp:OnInternet"))
	icmpKonsol.MUnsignedinteger16Yazdır(uint16(msg.Tür))
	icmpKonsol.MYazdır(([]byte)(":"))

	switch msg.Tür {
	case 0:
		icmpKonsol.MYazdır(([]byte)("ping response from "))
		break

	case 8:
		icmpKonsol.MYazdır(([]byte)("ping send "))
		msg.Tür = 0

		msg.checksum = 0
		msg.Ayarlabuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataBelirteç)), uint32(icmpBoyut))

		msg.Ayarlabuffer(buffer_2)

		return true
		break
	}
	return false
}

func (self *TAğlar_arası_ağ_denetim_iletisi_protokolü) EchorequestGönder(ipAğbyteorder uint32) bool {
	var ağlar_arası_ağ_denetim_iletisi_protokolü TİnternetCtrlİletiprotocolİleti = TİnternetCtrlİletiprotocolİleti{}

	var bellekmanager = &TBellekmanager{}
	var buffer_2 = (*TİnternetCtrlİletiprotocolİletibuffer)(bellekmanager.Bellek_ayır(1024))

	ağlar_arası_ağ_denetim_iletisi_protokolü.Tür = 8
	ağlar_arası_ağ_denetim_iletisi_protokolü.code = 0
	ağlar_arası_ağ_denetim_iletisi_protokolü.data = 0x3713
	ağlar_arası_ağ_denetim_iletisi_protokolü.checksum = 0
	ağlar_arası_ağ_denetim_iletisi_protokolü.Ayarlabuffer(buffer_2)
	ağlar_arası_ağ_denetim_iletisi_protokolü.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpBoyut))
	ağlar_arası_ağ_denetim_iletisi_protokolü.Ayarlabuffer(buffer_2)

	var dataBelirteç uintptr = uintptr(Pointer(buffer_2))
	iphandler.Gönder(ipAğbyteorder, 0x01, dataBelirteç, uint32(icmpBoyut))

	return false

}
