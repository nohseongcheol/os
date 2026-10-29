/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokol_propojených_sítí_4

import . "unsafe"
import . "util"
import . "konzole"
import . "rámec_sítě_se_sdíleným_médiem"
import . "arp"

var ipKonzole TKonzole = TKonzole{}

type TInternetprotocolv4Zprávabuffer struct {
	lenver		byte
	tos		byte
	celkemDélka	[2]byte

	ident		[2]byte
	příznakyaoffset	[2]byte

	časdolive	byte
	protocol	byte
	kontrolnísoučet	[2]byte

	zdrojipAdresa	[4]byte
	cílipAdresa	[4]byte
}

var ipVelikost uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Zpráva struct {
	headerDélka	uint8
	verze		uint8
	tos		uint8
	celkemDélka	uint16

	ident		uint16
	příznakyaoffset	uint16

	časdolive	uint8
	protocol	uint8
	kontrolnísoučet	uint16

	zdrojipAdresa	uint32
	cílipAdresa	uint32
}

func (self *TInternetprotocolv4Zpráva) Init(buffer_2 TInternetprotocolv4Zprávabuffer) {

	self.verze = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerDélka = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.celkemDélka = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.celkemDélka))

	self.ident = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.ident))
	self.příznakyaoffset = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.příznakyaoffset))

	self.časdolive = buffer_2.časdolive
	self.protocol = buffer_2.protocol
	self.kontrolnísoučet = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.kontrolnísoučet))

	self.zdrojipAdresa = Unsignedinteger32r(Poledounsignedinteger32(buffer_2.zdrojipAdresa))
	self.cílipAdresa = Unsignedinteger32r(Poledounsignedinteger32(buffer_2.cílipAdresa))

}
func (self *TInternetprotocolv4Zpráva) Nastavitbuffer(buffer_2 *TInternetprotocolv4Zprávabuffer) {

	buffer_2.lenver = byte(((self.verze & 0x0F) << 4) | (self.headerDélka & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.celkemDélka = Unsignedinteger16doPole(self.celkemDélka)

	buffer_2.ident = Unsignedinteger16doPole(self.ident)
	buffer_2.příznakyaoffset = Unsignedinteger16doPole(self.příznakyaoffset)

	buffer_2.časdolive = self.časdolive
	buffer_2.protocol = self.protocol
	buffer_2.kontrolnísoučet = Unsignedinteger16doPole(self.kontrolnísoučet)

	buffer_2.zdrojipAdresa = Unsignedinteger32doPole(self.zdrojipAdresa)
	buffer_2.cílipAdresa = Unsignedinteger32doPole(self.cílipAdresa)

}

type IInternetprotocolhandler interface {
	Init(backend TPoskytovatel_protokolu_propojených_sítí, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder uint32, cílipAdresaSíťbyteorder uint32, dataKurzor uintptr, velikost uint32) bool
	Poslat(cílipAdresaSíťbyteorder uint32, pprotocol uint8, dataKurzor uintptr, velikost uint32)
	Providerget() *TPoskytovatel_protokolu_propojených_sítí
}

type TInternetprotocolhandler struct {
}

var ipethernetRámhandler IpethernetRámhandler = IpethernetRámhandler{}
var protocol uint8

func (self *TInternetprotocolhandler) Init(backend TPoskytovatel_protokolu_propojených_sítí, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TInternetprotocolhandler) Internetprotocolreceivewhen(zdrojipAdresaSíťbyteorder uint32, cílipAdresaSíťbyteorder uint32, dataKurzor uintptr, velikost uint32) bool {
	ipKonzole.MTisknout(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TInternetprotocolhandler) Poslat(cílipAdresaSíťbyteorder uint32, pprotocol uint8, dataKurzor uintptr, velikost uint32) {

	poskytovatel_protokolu_propojených_sítí.Poslat(cílipAdresaSíťbyteorder, pprotocol, dataKurzor, velikost)
}
func (self *TInternetprotocolhandler) Providerget() *TPoskytovatel_protokolu_propojených_sítí {
	return &poskytovatel_protokolu_propojených_sítí
}

type IpethernetRámhandler struct {
	TEthernetRámhandler
}

var poskytovatel_protokolu_propojených_sítí TPoskytovatel_protokolu_propojených_sítí

func (self *IpethernetRámhandler) EthernetRámreceivewhen(dataKurzor uintptr, velikost int) bool {
	ipKonzole.MTisknout(([]byte)("iphandler:onEtherfameRecv\n"))
	return poskytovatel_protokolu_propojených_sítí.EthernetRámreceivewhen(dataKurzor, uint32(velikost))

}

func (self *IpethernetRámhandler) Poslat(cílipAdresaSíťbyteorder uint64, dataKurzor uintptr, velikost uint32) {
	ipKonzole.MTisknout(([]byte)("ipefhandler:send\n"))
	var ethernetTypbe = Unsignedinteger16r(0x0800)
	self.TEthernetRámhandler.RámPoslat(cílipAdresaSíťbyteorder, ethernetTypbe, dataKurzor, velikost)

}

var handler_2 [255]IInternetprotocolhandler

type TPoskytovatel_protokolu_propojených_sítí struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetRámhandler

func (self *TPoskytovatel_protokolu_propojených_sítí) Init(pefprovider TPoskytovatel_rámců_sítě_se_sdíleným_médiem, pefhandler IEthernetRámhandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Nastavithandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetMaska = subnetMaska
	poskytovatel_protokolu_propojených_sítí = *self
}
func (self *TPoskytovatel_protokolu_propojených_sítí) EthernetRámreceivewhen(ethernetRámpayload uintptr, velikost uint32) bool {
	if velikost < uint32(ipVelikost) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Zprávabuffer = (*TInternetprotocolv4Zprávabuffer)(Pointer(ethernetRámpayload))
	var internetprotocolZpráva TInternetprotocolv4Zpráva
	internetprotocolZpráva.Init(*buffer_2)

	var reply bool = false

	if internetprotocolZpráva.cílipAdresa == uint32(efhandler.GetipAdresa()) {

		var délka uint32 = uint32(internetprotocolZpráva.celkemDélka)
		if délka > velikost {
			délka = velikost
		}
		if handler_2[internetprotocolZpráva.protocol] != nil {
			reply = handler_2[internetprotocolZpráva.protocol].Internetprotocolreceivewhen(internetprotocolZpráva.zdrojipAdresa, internetprotocolZpráva.cílipAdresa, ethernetRámpayload+uintptr(4*internetprotocolZpráva.headerDélka), uint32(délka-uint32(4*internetprotocolZpráva.headerDélka)))

		}
	}

	if reply {

		var temporary = internetprotocolZpráva.cílipAdresa
		internetprotocolZpráva.cílipAdresa = internetprotocolZpráva.zdrojipAdresa
		internetprotocolZpráva.zdrojipAdresa = temporary

		internetprotocolZpráva.časdolive = 0x40
		internetprotocolZpráva.kontrolnísoučet = 0

		internetprotocolZpráva.Nastavitbuffer(buffer_2)
		internetprotocolZpráva.kontrolnísoučet = self.Kontrolnísoučet((*([4096]uint16))(Pointer(ethernetRámpayload)), uint32(4*internetprotocolZpráva.headerDélka))

		internetprotocolZpráva.Nastavitbuffer(buffer_2)

	}

	ipKonzole.MTisknout(([]byte)("ipmessage"))
	ipKonzole.MUnsignedinteger32Tisknout(internetprotocolZpráva.zdrojipAdresa)
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MUnsignedinteger32Tisknout(internetprotocolZpráva.cílipAdresa)
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MUnsignedinteger16Tisknout(uint16(internetprotocolZpráva.headerDélka))
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MUnsignedinteger16Tisknout(uint16(internetprotocolZpráva.verze))
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MUnsignedinteger16Tisknout(internetprotocolZpráva.celkemDélka)
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MUnsignedinteger32Tisknout(uint32(efhandler.GetipAdresa()))
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MTisknout(([]byte)("\n"))

	return reply

}
func (self *TPoskytovatel_protokolu_propojených_sítí) Poslat(cílipAdresaSíťbyteorder uint32, protocol uint8, dataKurzor uintptr, velikost uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Zprávabuffer = (*TInternetprotocolv4Zprávabuffer)(Pointer(&buffer1_2))
	var zpráva TInternetprotocolv4Zpráva = TInternetprotocolv4Zpráva{}
	zpráva.verze = 4
	zpráva.headerDélka = ipVelikost / 4
	zpráva.tos = 0
	zpráva.celkemDélka = Unsignedinteger16r(uint16(velikost + uint32(ipVelikost)))

	zpráva.ident = 0x0100
	zpráva.příznakyaoffset = 0x0040
	zpráva.časdolive = 0x40
	zpráva.protocol = protocol

	zpráva.cílipAdresa = cílipAdresaSíťbyteorder

	zpráva.zdrojipAdresa = uint32(efhandler.GetipAdresa())

	zpráva.kontrolnísoučet = 0

	zpráva.Nastavitbuffer(buffer_2)
	zpráva.kontrolnísoučet = self.Kontrolnísoučet((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVelikost))
	zpráva.Nastavitbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))

	for i := 0; i < int(velikost); i++ {

		buffer1_2[i+int(ipVelikost)] = databuffer_2[i]
	}

	ipKonzole.MTisknoutxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(velikost)+int(ipVelikost); i++ {
		ipKonzole.MHexadecimalTisknout(buffer1_2[i])
	}
	ipKonzole.MTisknout(([]byte)(":"))
	ipKonzole.MTisknout(([]byte)("]\n"))

	var následujícíhopipAdresaSíťbyteorder uint32 = cílipAdresaSíťbyteorder
	if (cílipAdresaSíťbyteorder & self.SubnetMaska) != (zpráva.zdrojipAdresa & self.SubnetMaska) {
		následujícíhopipAdresaSíťbyteorder = self.Gatewayip
	}

	var poslatdataKurzor = uintptr(Pointer(&buffer1_2))
	ipKonzole.MUnsignedinteger32Tisknout(následujícíhopipAdresaSíťbyteorder)

	var ethernetTypbe = Unsignedinteger16r(0x0800)
	efhandler.RámPoslat(self.arpprovider.Resolve(následujícíhopipAdresaSíťbyteorder), ethernetTypbe, poslatdataKurzor, uint32(ipVelikost)+uint32(velikost))

}
func (self *TPoskytovatel_protokolu_propojených_sítí) Kontrolnísoučet(pdata *[4096]uint16, délkaVstupBytů uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBytů [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (délkaVstupBytů % 2) != 0 {
		temporary += uint32(uint16(dataBytů[délkaVstupBytů-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TPoskytovatel_protokolu_propojených_sítí) GetipAdresa() uint64 {
	return efhandler.GetipAdresa()
}
