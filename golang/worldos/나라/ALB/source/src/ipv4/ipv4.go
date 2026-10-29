/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "konsolë"
import . "ethernetKornizë"
import . "arp"

var ipKonsolë TKonsolë = TKonsolë{}

type TInternetprotocolv4Mesazhibuffer struct {
	lenver		byte
	tos		byte
	gjithsejGjatësi	[2]byte

	ident			[2]byte
	flamurkaandoffset	[2]byte

	oratolive	byte
	protocol	byte
	checksum	[2]byte

	burimiipaddress		[4]byte
	destinacioniipaddress	[4]byte
}

var ipMadhësia uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Mesazhi struct {
	headerGjatësi	uint8
	version		uint8
	tos		uint8
	gjithsejGjatësi	uint16

	ident			uint16
	flamurkaandoffset	uint16

	oratolive	uint8
	protocol	uint8
	checksum	uint16

	burimiipaddress		uint32
	destinacioniipaddress	uint32
}

func (vetvetja *TInternetprotocolv4Mesazhi) Init(buffer_2 TInternetprotocolv4Mesazhibuffer) {

	vetvetja.version = ((buffer_2.lenver & 0xF0) >> 4)
	vetvetja.headerGjatësi = buffer_2.lenver & 0x0F
	vetvetja.tos = buffer_2.tos
	vetvetja.gjithsejGjatësi = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.gjithsejGjatësi))

	vetvetja.ident = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.ident))
	vetvetja.flamurkaandoffset = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.flamurkaandoffset))

	vetvetja.oratolive = buffer_2.oratolive
	vetvetja.protocol = buffer_2.protocol
	vetvetja.checksum = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.checksum))

	vetvetja.burimiipaddress = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer_2.burimiipaddress))
	vetvetja.destinacioniipaddress = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer_2.destinacioniipaddress))

}
func (vetvetja *TInternetprotocolv4Mesazhi) Caktonibuffer(buffer_2 *TInternetprotocolv4Mesazhibuffer) {

	buffer_2.lenver = byte(((vetvetja.version & 0x0F) << 4) | (vetvetja.headerGjatësi & 0x0F))
	buffer_2.tos = vetvetja.tos
	buffer_2.gjithsejGjatësi = Unsignedinteger16toRreshtimi(vetvetja.gjithsejGjatësi)

	buffer_2.ident = Unsignedinteger16toRreshtimi(vetvetja.ident)
	buffer_2.flamurkaandoffset = Unsignedinteger16toRreshtimi(vetvetja.flamurkaandoffset)

	buffer_2.oratolive = vetvetja.oratolive
	buffer_2.protocol = vetvetja.protocol
	buffer_2.checksum = Unsignedinteger16toRreshtimi(vetvetja.checksum)

	buffer_2.burimiipaddress = Unsignedinteger32toRreshtimi(vetvetja.burimiipaddress)
	buffer_2.destinacioniipaddress = Unsignedinteger32toRreshtimi(vetvetja.destinacioniipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder uint32, destinacioniipaddressRrjetibyteorder uint32, dataKursori uintptr, madhësia uint32) bool
	Dërgo(destinacioniipaddressRrjetibyteorder uint32, pprotocol uint8, dataKursori uintptr, madhësia uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetKornizëhandler IpethernetKornizëhandler = IpethernetKornizëhandler{}
var protocol uint8

func (vetvetja *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (vetvetja *TInternetprotocolhandler) Internetprotocolreceivewhen(burimiipaddressRrjetibyteorder uint32, destinacioniipaddressRrjetibyteorder uint32, dataKursori uintptr, madhësia uint32) bool {
	ipKonsolë.MPrinto(([]byte)("ipHandler:OnInternet"))
	return false
}
func (vetvetja *TInternetprotocolhandler) Dërgo(destinacioniipaddressRrjetibyteorder uint32, pprotocol uint8, dataKursori uintptr, madhësia uint32) {

	ipprovider.Dërgo(destinacioniipaddressRrjetibyteorder, pprotocol, dataKursori, madhësia)
}
func (vetvetja *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetKornizëhandler struct {
	TEthernetKornizëhandler
}

var ipprovider TInternetprotocolprovider

func (vetvetja *IpethernetKornizëhandler) EthernetKornizëreceivewhen(dataKursori uintptr, madhësia int) bool {
	ipKonsolë.MPrinto(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetKornizëreceivewhen(dataKursori, uint32(madhësia))

}

func (vetvetja *IpethernetKornizëhandler) Dërgo(destinacioniipaddressRrjetibyteorder uint64, dataKursori uintptr, madhësia uint32) {
	ipKonsolë.MPrinto(([]byte)("ipefhandler:send\n"))
	var ethernetLlojibe = Unsignedinteger16r(0x0800)
	vetvetja.TEthernetKornizëhandler.KornizëDërgo(destinacioniipaddressRrjetibyteorder, ethernetLlojibe, dataKursori, madhësia)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetKornizëhandler

func (vetvetja *TInternetprotocolprovider) Init(pefprovider TEthernetKornizëprovider, pefhandler IEthernetKornizëhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Caktonihandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	vetvetja.arpprovider = arp
	vetvetja.Gatewayip = gatewayip
	vetvetja.Subnetmask = subnetmask
	ipprovider = *vetvetja
}
func (vetvetja *TInternetprotocolprovider) EthernetKornizëreceivewhen(ethernetKornizëpayload uintptr, madhësia uint32) bool {
	if madhësia < uint32(ipMadhësia) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Mesazhibuffer = (*TInternetprotocolv4Mesazhibuffer)(Pointer(ethernetKornizëpayload))
	var internetprotocolMesazhi TInternetprotocolv4Mesazhi
	internetprotocolMesazhi.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMesazhi.destinacioniipaddress == uint32(efhandler.Getipaddress()) {

		var gjatësi uint32 = uint32(internetprotocolMesazhi.gjithsejGjatësi)
		if gjatësi > madhësia {
			gjatësi = madhësia
		}
		if handler_2[internetprotocolMesazhi.protocol] != nil {
			reply = handler_2[internetprotocolMesazhi.protocol].Internetprotocolreceivewhen(internetprotocolMesazhi.burimiipaddress, internetprotocolMesazhi.destinacioniipaddress, ethernetKornizëpayload+uintptr(4*internetprotocolMesazhi.headerGjatësi), uint32(gjatësi-uint32(4*internetprotocolMesazhi.headerGjatësi)))

		}
	}

	if reply {

		var temporary = internetprotocolMesazhi.destinacioniipaddress
		internetprotocolMesazhi.destinacioniipaddress = internetprotocolMesazhi.burimiipaddress
		internetprotocolMesazhi.burimiipaddress = temporary

		internetprotocolMesazhi.oratolive = 0x40
		internetprotocolMesazhi.checksum = 0

		internetprotocolMesazhi.Caktonibuffer(buffer_2)
		internetprotocolMesazhi.checksum = vetvetja.Checksum((*([4096]uint16))(Pointer(ethernetKornizëpayload)), uint32(4*internetprotocolMesazhi.headerGjatësi))

		internetprotocolMesazhi.Caktonibuffer(buffer_2)

	}

	ipKonsolë.MPrinto(([]byte)("ipmessage"))
	ipKonsolë.MUnsignedinteger32Printo(internetprotocolMesazhi.burimiipaddress)
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MUnsignedinteger32Printo(internetprotocolMesazhi.destinacioniipaddress)
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MUnsignedinteger16Printo(uint16(internetprotocolMesazhi.headerGjatësi))
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MUnsignedinteger16Printo(uint16(internetprotocolMesazhi.version))
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MUnsignedinteger16Printo(internetprotocolMesazhi.gjithsejGjatësi)
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MUnsignedinteger32Printo(uint32(efhandler.Getipaddress()))
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MPrinto(([]byte)("\n"))

	return reply

}
func (vetvetja *TInternetprotocolprovider) Dërgo(destinacioniipaddressRrjetibyteorder uint32, protocol uint8, dataKursori uintptr, madhësia uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Mesazhibuffer = (*TInternetprotocolv4Mesazhibuffer)(Pointer(&buffer1_2))
	var mesazhi TInternetprotocolv4Mesazhi = TInternetprotocolv4Mesazhi{}
	mesazhi.version = 4
	mesazhi.headerGjatësi = ipMadhësia / 4
	mesazhi.tos = 0
	mesazhi.gjithsejGjatësi = Unsignedinteger16r(uint16(madhësia + uint32(ipMadhësia)))

	mesazhi.ident = 0x0100
	mesazhi.flamurkaandoffset = 0x0040
	mesazhi.oratolive = 0x40
	mesazhi.protocol = protocol

	mesazhi.destinacioniipaddress = destinacioniipaddressRrjetibyteorder

	mesazhi.burimiipaddress = uint32(efhandler.Getipaddress())

	mesazhi.checksum = 0

	mesazhi.Caktonibuffer(buffer_2)
	mesazhi.checksum = vetvetja.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipMadhësia))
	mesazhi.Caktonibuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursori))

	for i := 0; i < int(madhësia); i++ {

		buffer1_2[i+int(ipMadhësia)] = databuffer_2[i]
	}

	ipKonsolë.MPrintoxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(madhësia)+int(ipMadhësia); i++ {
		ipKonsolë.MHexadecimalPrinto(buffer1_2[i])
	}
	ipKonsolë.MPrinto(([]byte)(":"))
	ipKonsolë.MPrinto(([]byte)("]\n"))

	var pasuesenhopipaddressRrjetibyteorder uint32 = destinacioniipaddressRrjetibyteorder
	if (destinacioniipaddressRrjetibyteorder & vetvetja.Subnetmask) != (mesazhi.burimiipaddress & vetvetja.Subnetmask) {
		pasuesenhopipaddressRrjetibyteorder = vetvetja.Gatewayip
	}

	var dërgodataKursori = uintptr(Pointer(&buffer1_2))
	ipKonsolë.MUnsignedinteger32Printo(pasuesenhopipaddressRrjetibyteorder)

	var ethernetLlojibe = Unsignedinteger16r(0x0800)
	efhandler.KornizëDërgo(vetvetja.arpprovider.Resolve(pasuesenhopipaddressRrjetibyteorder), ethernetLlojibe, dërgodataKursori, uint32(ipMadhësia)+uint32(madhësia))

}
func (vetvetja *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, gjatësiZmadhobytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (gjatësiZmadhobytes % 2) != 0 {
		temporary += uint32(uint16(databytes[gjatësiZmadhobytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (vetvetja *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
