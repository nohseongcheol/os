/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokol_jaringan_saling_terhubung_4

import . "unsafe"
import . "util"
import . "console"
import . "bingkai_jaringan_media_bersama"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4Pesanbuffer struct {
	lenver		byte
	tos		byte
	totalPanjang	[2]byte

	ident		[2]byte
	tandadanoffset	[2]byte

	waktutolive	byte
	protocol	byte
	checksum	[2]byte

	sumberipaddress	[4]byte
	tujuanipaddress	[4]byte
}

var ipUkuran uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Pesan struct {
	headerPanjang	uint8
	versi		uint8
	tos		uint8
	totalPanjang	uint16

	ident		uint16
	tandadanoffset	uint16

	waktutolive	uint8
	protocol	uint8
	checksum	uint16

	sumberipaddress	uint32
	tujuanipaddress	uint32
}

func (dirisendiri *TInternetprotocolv4Pesan) Init(buffer_2 TInternetprotocolv4Pesanbuffer) {

	dirisendiri.versi = ((buffer_2.lenver & 0xF0) >> 4)
	dirisendiri.headerPanjang = buffer_2.lenver & 0x0F
	dirisendiri.tos = buffer_2.tos
	dirisendiri.totalPanjang = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.totalPanjang))

	dirisendiri.ident = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.ident))
	dirisendiri.tandadanoffset = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.tandadanoffset))

	dirisendiri.waktutolive = buffer_2.waktutolive
	dirisendiri.protocol = buffer_2.protocol
	dirisendiri.checksum = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.checksum))

	dirisendiri.sumberipaddress = Unsignedinteger32r(Jajarantounsignedinteger32(buffer_2.sumberipaddress))
	dirisendiri.tujuanipaddress = Unsignedinteger32r(Jajarantounsignedinteger32(buffer_2.tujuanipaddress))

}
func (dirisendiri *TInternetprotocolv4Pesan) Aturbuffer(buffer_2 *TInternetprotocolv4Pesanbuffer) {

	buffer_2.lenver = byte(((dirisendiri.versi & 0x0F) << 4) | (dirisendiri.headerPanjang & 0x0F))
	buffer_2.tos = dirisendiri.tos
	buffer_2.totalPanjang = Unsignedinteger16toJajaran(dirisendiri.totalPanjang)

	buffer_2.ident = Unsignedinteger16toJajaran(dirisendiri.ident)
	buffer_2.tandadanoffset = Unsignedinteger16toJajaran(dirisendiri.tandadanoffset)

	buffer_2.waktutolive = dirisendiri.waktutolive
	buffer_2.protocol = dirisendiri.protocol
	buffer_2.checksum = Unsignedinteger16toJajaran(dirisendiri.checksum)

	buffer_2.sumberipaddress = Unsignedinteger32toJajaran(dirisendiri.sumberipaddress)
	buffer_2.tujuanipaddress = Unsignedinteger32toJajaran(dirisendiri.tujuanipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TPenyedia_protokol_jaringan_saling_terhubung, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder uint32, tujuanipaddressJaringanbyteorder uint32, dataPenunjuk uintptr, ukuran uint32) bool
	Kirim(tujuanipaddressJaringanbyteorder uint32, pprotocol uint8, dataPenunjuk uintptr, ukuran uint32)
	Providerget() *TPenyedia_protokol_jaringan_saling_terhubung
}

type TInternetprotocolhandler struct {
}

var ipethernetBingkaihandler IpethernetBingkaihandler = IpethernetBingkaihandler{}
var protocol uint8

func (dirisendiri *TInternetprotocolhandler) Init(backend TPenyedia_protokol_jaringan_saling_terhubung, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (dirisendiri *TInternetprotocolhandler) Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder uint32, tujuanipaddressJaringanbyteorder uint32, dataPenunjuk uintptr, ukuran uint32) bool {
	ipconsole.MCetak(([]byte)("ipHandler:OnInternet"))
	return false
}
func (dirisendiri *TInternetprotocolhandler) Kirim(tujuanipaddressJaringanbyteorder uint32, pprotocol uint8, dataPenunjuk uintptr, ukuran uint32) {

	penyedia_protokol_jaringan_saling_terhubung.Kirim(tujuanipaddressJaringanbyteorder, pprotocol, dataPenunjuk, ukuran)
}
func (dirisendiri *TInternetprotocolhandler) Providerget() *TPenyedia_protokol_jaringan_saling_terhubung {
	return &penyedia_protokol_jaringan_saling_terhubung
}

type IpethernetBingkaihandler struct {
	TEthernetBingkaihandler
}

var penyedia_protokol_jaringan_saling_terhubung TPenyedia_protokol_jaringan_saling_terhubung

func (dirisendiri *IpethernetBingkaihandler) EthernetBingkaireceivewhen(dataPenunjuk uintptr, ukuran int) bool {
	ipconsole.MCetak(([]byte)("iphandler:onEtherfameRecv\n"))
	return penyedia_protokol_jaringan_saling_terhubung.EthernetBingkaireceivewhen(dataPenunjuk, uint32(ukuran))

}

func (dirisendiri *IpethernetBingkaihandler) Kirim(tujuanipaddressJaringanbyteorder uint64, dataPenunjuk uintptr, ukuran uint32) {
	ipconsole.MCetak(([]byte)("ipefhandler:send\n"))
	var ethernetTipebe = Unsignedinteger16r(0x0800)
	dirisendiri.TEthernetBingkaihandler.BingkaiKirim(tujuanipaddressJaringanbyteorder, ethernetTipebe, dataPenunjuk, ukuran)

}

var handler_2 [255]IInternetprotocolhandler

type TPenyedia_protokol_jaringan_saling_terhubung struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetTopeng	uint32
}

var efhandler IEthernetBingkaihandler

func (dirisendiri *TPenyedia_protokol_jaringan_saling_terhubung) Init(pefprovider TPenyedia_bingkai_jaringan_media_bersama, pefhandler IEthernetBingkaihandler, arp Arpprovider, gatewayip uint32, subnetTopeng uint32) {

	efhandler = pefhandler
	efhandler.Aturhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	dirisendiri.arpprovider = arp
	dirisendiri.Gatewayip = gatewayip
	dirisendiri.SubnetTopeng = subnetTopeng
	penyedia_protokol_jaringan_saling_terhubung = *dirisendiri
}
func (dirisendiri *TPenyedia_protokol_jaringan_saling_terhubung) EthernetBingkaireceivewhen(ethernetBingkaipayload uintptr, ukuran uint32) bool {
	if ukuran < uint32(ipUkuran) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Pesanbuffer = (*TInternetprotocolv4Pesanbuffer)(Pointer(ethernetBingkaipayload))
	var internetprotocolPesan TInternetprotocolv4Pesan
	internetprotocolPesan.Init(*buffer_2)

	var reply bool = false

	if internetprotocolPesan.tujuanipaddress == uint32(efhandler.Getipaddress()) {

		var panjang uint32 = uint32(internetprotocolPesan.totalPanjang)
		if panjang > ukuran {
			panjang = ukuran
		}
		if handler_2[internetprotocolPesan.protocol] != nil {
			reply = handler_2[internetprotocolPesan.protocol].Internetprotocolreceivewhen(internetprotocolPesan.sumberipaddress, internetprotocolPesan.tujuanipaddress, ethernetBingkaipayload+uintptr(4*internetprotocolPesan.headerPanjang), uint32(panjang-uint32(4*internetprotocolPesan.headerPanjang)))

		}
	}

	if reply {

		var temporary = internetprotocolPesan.tujuanipaddress
		internetprotocolPesan.tujuanipaddress = internetprotocolPesan.sumberipaddress
		internetprotocolPesan.sumberipaddress = temporary

		internetprotocolPesan.waktutolive = 0x40
		internetprotocolPesan.checksum = 0

		internetprotocolPesan.Aturbuffer(buffer_2)
		internetprotocolPesan.checksum = dirisendiri.Checksum((*([4096]uint16))(Pointer(ethernetBingkaipayload)), uint32(4*internetprotocolPesan.headerPanjang))

		internetprotocolPesan.Aturbuffer(buffer_2)

	}

	ipconsole.MCetak(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Cetak(internetprotocolPesan.sumberipaddress)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger32Cetak(internetprotocolPesan.tujuanipaddress)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(uint16(internetprotocolPesan.headerPanjang))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(uint16(internetprotocolPesan.versi))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(internetprotocolPesan.totalPanjang)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger32Cetak(uint32(efhandler.Getipaddress()))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MCetak(([]byte)("\n"))

	return reply

}
func (dirisendiri *TPenyedia_protokol_jaringan_saling_terhubung) Kirim(tujuanipaddressJaringanbyteorder uint32, protocol uint8, dataPenunjuk uintptr, ukuran uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Pesanbuffer = (*TInternetprotocolv4Pesanbuffer)(Pointer(&buffer1_2))
	var pesan TInternetprotocolv4Pesan = TInternetprotocolv4Pesan{}
	pesan.versi = 4
	pesan.headerPanjang = ipUkuran / 4
	pesan.tos = 0
	pesan.totalPanjang = Unsignedinteger16r(uint16(ukuran + uint32(ipUkuran)))

	pesan.ident = 0x0100
	pesan.tandadanoffset = 0x0040
	pesan.waktutolive = 0x40
	pesan.protocol = protocol

	pesan.tujuanipaddress = tujuanipaddressJaringanbyteorder

	pesan.sumberipaddress = uint32(efhandler.Getipaddress())

	pesan.checksum = 0

	pesan.Aturbuffer(buffer_2)
	pesan.checksum = dirisendiri.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipUkuran))
	pesan.Aturbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenunjuk))

	for i := 0; i < int(ukuran); i++ {

		buffer1_2[i+int(ipUkuran)] = databuffer_2[i]
	}

	ipconsole.MCetakxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(ukuran)+int(ipUkuran); i++ {
		ipconsole.MHexadecimalCetak(buffer1_2[i])
	}
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MCetak(([]byte)("]\n"))

	var berikutnyahopipaddressJaringanbyteorder uint32 = tujuanipaddressJaringanbyteorder
	if (tujuanipaddressJaringanbyteorder & dirisendiri.SubnetTopeng) != (pesan.sumberipaddress & dirisendiri.SubnetTopeng) {
		berikutnyahopipaddressJaringanbyteorder = dirisendiri.Gatewayip
	}

	var kirimdataPenunjuk = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Cetak(berikutnyahopipaddressJaringanbyteorder)

	var ethernetTipebe = Unsignedinteger16r(0x0800)
	efhandler.BingkaiKirim(dirisendiri.arpprovider.Resolve(berikutnyahopipaddressJaringanbyteorder), ethernetTipebe, kirimdataPenunjuk, uint32(ipUkuran)+uint32(ukuran))

}
func (dirisendiri *TPenyedia_protokol_jaringan_saling_terhubung) Checksum(pdata *[4096]uint16, panjangMasukByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (panjangMasukByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[panjangMasukByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (dirisendiri *TPenyedia_protokol_jaringan_saling_terhubung) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
