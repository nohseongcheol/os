/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "laidinisKadras"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetasprotocolv4Pranešimasbuffer struct {
	lenver		byte
	tos		byte
	išvisoTrukmė	[2]byte

	ident			[2]byte
	parametraiiroffset	[2]byte

	laikastolive	byte
	protocol	byte
	kontrolinėsuma	[2]byte

	šaltinisipaddress	[4]byte
	tikslasipaddress	[4]byte
}

var ipDydis uint8 = (4 + 4 + 4 + 8)

type TInternetasprotocolv4Pranešimas struct {
	headerTrukmė	uint8
	versija		uint8
	tos		uint8
	išvisoTrukmė	uint16

	ident			uint16
	parametraiiroffset	uint16

	laikastolive	uint8
	protocol	uint8
	kontrolinėsuma	uint16

	šaltinisipaddress	uint32
	tikslasipaddress	uint32
}

func (self *TInternetasprotocolv4Pranešimas) Init(buffer_2 TInternetasprotocolv4Pranešimasbuffer) {

	self.versija = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerTrukmė = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.išvisoTrukmė = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.išvisoTrukmė))

	self.ident = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.ident))
	self.parametraiiroffset = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.parametraiiroffset))

	self.laikastolive = buffer_2.laikastolive
	self.protocol = buffer_2.protocol
	self.kontrolinėsuma = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.kontrolinėsuma))

	self.šaltinisipaddress = Unsignedinteger32r(Masyvastounsignedinteger32(buffer_2.šaltinisipaddress))
	self.tikslasipaddress = Unsignedinteger32r(Masyvastounsignedinteger32(buffer_2.tikslasipaddress))

}
func (self *TInternetasprotocolv4Pranešimas) Nustatytabuffer(buffer_2 *TInternetasprotocolv4Pranešimasbuffer) {

	buffer_2.lenver = byte(((self.versija & 0x0F) << 4) | (self.headerTrukmė & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.išvisoTrukmė = Unsignedinteger16toMasyvas(self.išvisoTrukmė)

	buffer_2.ident = Unsignedinteger16toMasyvas(self.ident)
	buffer_2.parametraiiroffset = Unsignedinteger16toMasyvas(self.parametraiiroffset)

	buffer_2.laikastolive = self.laikastolive
	buffer_2.protocol = self.protocol
	buffer_2.kontrolinėsuma = Unsignedinteger16toMasyvas(self.kontrolinėsuma)

	buffer_2.šaltinisipaddress = Unsignedinteger32toMasyvas(self.šaltinisipaddress)
	buffer_2.tikslasipaddress = Unsignedinteger32toMasyvas(self.tikslasipaddress)

}

type IInternetasprotocolhandler interface {
	Init(backend TInternetasprotocolprovider, pihandler IInternetasprotocolhandler, pprotocol uint8)
	Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder uint32, tikslasipaddressTinklasbyteorder uint32, dataRodyklė uintptr, dydis uint32) bool
	Siųsti(tikslasipaddressTinklasbyteorder uint32, pprotocol uint8, dataRodyklė uintptr, dydis uint32)
	Providerget() *TInternetasprotocolprovider
}

type TInternetasprotocolhandler struct {
}

var ipLaidinisKadrashandler IpLaidinisKadrashandler = IpLaidinisKadrashandler{}
var protocol uint8

func (self *TInternetasprotocolhandler) Init(backend TInternetasprotocolprovider, pihandler IInternetasprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetasprotocolhandler) Internetasprotocolreceivewhen(šaltinisipaddressTinklasbyteorder uint32, tikslasipaddressTinklasbyteorder uint32, dataRodyklė uintptr, dydis uint32) bool {
	ipconsole.MSpausdinti(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetasprotocolhandler) Siųsti(tikslasipaddressTinklasbyteorder uint32, pprotocol uint8, dataRodyklė uintptr, dydis uint32) {

	ipprovider.Siųsti(tikslasipaddressTinklasbyteorder, pprotocol, dataRodyklė, dydis)
}
func (self *TInternetasprotocolhandler) Providerget() *TInternetasprotocolprovider {
	return &ipprovider
}

type IpLaidinisKadrashandler struct {
	TLaidinisKadrashandler
}

var ipprovider TInternetasprotocolprovider

func (self *IpLaidinisKadrashandler) LaidinisKadrasreceivewhen(dataRodyklė uintptr, dydis int) bool {
	ipconsole.MSpausdinti(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.LaidinisKadrasreceivewhen(dataRodyklė, uint32(dydis))

}

func (self *IpLaidinisKadrashandler) Siųsti(tikslasipaddressTinklasbyteorder uint64, dataRodyklė uintptr, dydis uint32) {
	ipconsole.MSpausdinti(([]byte)("ipefhandler:send\n"))
	var laidinisTipasbe = Unsignedinteger16r(0x0800)
	self.TLaidinisKadrashandler.KadrasSiųsti(tikslasipaddressTinklasbyteorder, laidinisTipasbe, dataRodyklė, dydis)

}

var handler_2 [255]IInternetasprotocolhandler

type TInternetasprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetKaukė	uint32
}

var efhandler ILaidinisKadrashandler

func (self *TInternetasprotocolprovider) Init(pefprovider TLaidinisKadrasprovider, pefhandler ILaidinisKadrashandler, arp Arpprovider, gatewayip uint32, subnetKaukė uint32) {

	efhandler = pefhandler
	efhandler.Nustatytahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetKaukė = subnetKaukė
	ipprovider = *self
}
func (self *TInternetasprotocolprovider) LaidinisKadrasreceivewhen(laidinisKadraspayload uintptr, dydis uint32) bool {
	if dydis < uint32(ipDydis) {
		return false
	}

	var buffer_2 *TInternetasprotocolv4Pranešimasbuffer = (*TInternetasprotocolv4Pranešimasbuffer)(Pointer(laidinisKadraspayload))
	var internetasprotocolPranešimas TInternetasprotocolv4Pranešimas
	internetasprotocolPranešimas.Init(*buffer_2)

	var reply bool = false

	if internetasprotocolPranešimas.tikslasipaddress == uint32(efhandler.Getipaddress()) {

		var trukmė uint32 = uint32(internetasprotocolPranešimas.išvisoTrukmė)
		if trukmė > dydis {
			trukmė = dydis
		}
		if handler_2[internetasprotocolPranešimas.protocol] != nil {
			reply = handler_2[internetasprotocolPranešimas.protocol].Internetasprotocolreceivewhen(internetasprotocolPranešimas.šaltinisipaddress, internetasprotocolPranešimas.tikslasipaddress, laidinisKadraspayload+uintptr(4*internetasprotocolPranešimas.headerTrukmė), uint32(trukmė-uint32(4*internetasprotocolPranešimas.headerTrukmė)))

		}
	}

	if reply {

		var temporary = internetasprotocolPranešimas.tikslasipaddress
		internetasprotocolPranešimas.tikslasipaddress = internetasprotocolPranešimas.šaltinisipaddress
		internetasprotocolPranešimas.šaltinisipaddress = temporary

		internetasprotocolPranešimas.laikastolive = 0x40
		internetasprotocolPranešimas.kontrolinėsuma = 0

		internetasprotocolPranešimas.Nustatytabuffer(buffer_2)
		internetasprotocolPranešimas.kontrolinėsuma = self.Kontrolinėsuma((*([4096]uint16))(Pointer(laidinisKadraspayload)), uint32(4*internetasprotocolPranešimas.headerTrukmė))

		internetasprotocolPranešimas.Nustatytabuffer(buffer_2)

	}

	ipconsole.MSpausdinti(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Spausdinti(internetasprotocolPranešimas.šaltinisipaddress)
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MUnsignedinteger32Spausdinti(internetasprotocolPranešimas.tikslasipaddress)
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MUnsignedinteger16Spausdinti(uint16(internetasprotocolPranešimas.headerTrukmė))
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MUnsignedinteger16Spausdinti(uint16(internetasprotocolPranešimas.versija))
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MUnsignedinteger16Spausdinti(internetasprotocolPranešimas.išvisoTrukmė)
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MUnsignedinteger32Spausdinti(uint32(efhandler.Getipaddress()))
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MSpausdinti(([]byte)("\n"))

	return reply

}
func (self *TInternetasprotocolprovider) Siųsti(tikslasipaddressTinklasbyteorder uint32, protocol uint8, dataRodyklė uintptr, dydis uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetasprotocolv4Pranešimasbuffer = (*TInternetasprotocolv4Pranešimasbuffer)(Pointer(&buffer1_2))
	var pranešimas TInternetasprotocolv4Pranešimas = TInternetasprotocolv4Pranešimas{}
	pranešimas.versija = 4
	pranešimas.headerTrukmė = ipDydis / 4
	pranešimas.tos = 0
	pranešimas.išvisoTrukmė = Unsignedinteger16r(uint16(dydis + uint32(ipDydis)))

	pranešimas.ident = 0x0100
	pranešimas.parametraiiroffset = 0x0040
	pranešimas.laikastolive = 0x40
	pranešimas.protocol = protocol

	pranešimas.tikslasipaddress = tikslasipaddressTinklasbyteorder

	pranešimas.šaltinisipaddress = uint32(efhandler.Getipaddress())

	pranešimas.kontrolinėsuma = 0

	pranešimas.Nustatytabuffer(buffer_2)
	pranešimas.kontrolinėsuma = self.Kontrolinėsuma((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipDydis))
	pranešimas.Nustatytabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataRodyklė))

	for i := 0; i < int(dydis); i++ {

		buffer1_2[i+int(ipDydis)] = databuffer_2[i]
	}

	ipconsole.MSpausdintixy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(dydis)+int(ipDydis); i++ {
		ipconsole.MHexadecimalSpausdinti(buffer1_2[i])
	}
	ipconsole.MSpausdinti(([]byte)(":"))
	ipconsole.MSpausdinti(([]byte)("]\n"))

	var kitashopipaddressTinklasbyteorder uint32 = tikslasipaddressTinklasbyteorder
	if (tikslasipaddressTinklasbyteorder & self.SubnetKaukė) != (pranešimas.šaltinisipaddress & self.SubnetKaukė) {
		kitashopipaddressTinklasbyteorder = self.Gatewayip
	}

	var siųstidataRodyklė = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Spausdinti(kitashopipaddressTinklasbyteorder)

	var laidinisTipasbe = Unsignedinteger16r(0x0800)
	efhandler.KadrasSiųsti(self.arpprovider.Resolve(kitashopipaddressTinklasbyteorder), laidinisTipasbe, siųstidataRodyklė, uint32(ipDydis)+uint32(dydis))

}
func (self *TInternetasprotocolprovider) Kontrolinėsuma(pdata *[4096]uint16, trukmėĮBaitų uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBaitų [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (trukmėĮBaitų % 2) != 0 {
		temporary += uint32(uint16(dataBaitų[trukmėĮBaitų-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TInternetasprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
