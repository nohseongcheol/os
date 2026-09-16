/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "konzola"
import . "ethernetRámec"
import . "arp"

var ipKonzola TKonzola = TKonzola{}

type TInternetprotocolv4Správabuffer struct {
	lenver		byte
	tos		byte
	celkomDĺžka	[2]byte

	ident			[2]byte
	príznakyaPosunutie	[2]byte

	častolive	byte
	protocol	byte
	checksum	[2]byte

	zdrojipaddress	[4]byte
	cieľipaddress	[4]byte
}

var ipVeľkosť uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Správa struct {
	headerDĺžka	uint8
	verzia		uint8
	tos		uint8
	celkomDĺžka	uint16

	ident			uint16
	príznakyaPosunutie	uint16

	častolive	uint8
	protocol	uint8
	checksum	uint16

	zdrojipaddress	uint32
	cieľipaddress	uint32
}

func (vlastný *TInternetprotocolv4Správa) Init(buffer_2 TInternetprotocolv4Správabuffer) {

	vlastný.verzia = ((buffer_2.lenver & 0xF0) >> 4)
	vlastný.headerDĺžka = buffer_2.lenver & 0x0F
	vlastný.tos = buffer_2.tos
	vlastný.celkomDĺžka = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.celkomDĺžka))

	vlastný.ident = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.ident))
	vlastný.príznakyaPosunutie = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.príznakyaPosunutie))

	vlastný.častolive = buffer_2.častolive
	vlastný.protocol = buffer_2.protocol
	vlastný.checksum = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.checksum))

	vlastný.zdrojipaddress = Unsignedinteger32r(Poletounsignedinteger32(buffer_2.zdrojipaddress))
	vlastný.cieľipaddress = Unsignedinteger32r(Poletounsignedinteger32(buffer_2.cieľipaddress))

}
func (vlastný *TInternetprotocolv4Správa) Sadabuffer(buffer_2 *TInternetprotocolv4Správabuffer) {

	buffer_2.lenver = byte(((vlastný.verzia & 0x0F) << 4) | (vlastný.headerDĺžka & 0x0F))
	buffer_2.tos = vlastný.tos
	buffer_2.celkomDĺžka = Unsignedinteger16toPole(vlastný.celkomDĺžka)

	buffer_2.ident = Unsignedinteger16toPole(vlastný.ident)
	buffer_2.príznakyaPosunutie = Unsignedinteger16toPole(vlastný.príznakyaPosunutie)

	buffer_2.častolive = vlastný.častolive
	buffer_2.protocol = vlastný.protocol
	buffer_2.checksum = Unsignedinteger16toPole(vlastný.checksum)

	buffer_2.zdrojipaddress = Unsignedinteger32toPole(vlastný.zdrojipaddress)
	buffer_2.cieľipaddress = Unsignedinteger32toPole(vlastný.cieľipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder uint32, cieľipaddressSieťbyteorder uint32, dataKurzor uintptr, veľkosť uint32) bool
	Poslať(cieľipaddressSieťbyteorder uint32, pprotocol uint8, dataKurzor uintptr, veľkosť uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipethernetRámechandler IpethernetRámechandler = IpethernetRámechandler{}
var protocol uint8

func (vlastný *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (vlastný *TInternetprotocolhandler) Internetprotocolreceivewhen(zdrojipaddressSieťbyteorder uint32, cieľipaddressSieťbyteorder uint32, dataKurzor uintptr, veľkosť uint32) bool {
	ipKonzola.MTlačiť(([]byte)("ipHandler:OnInternet"))
	return false
}
func (vlastný *TInternetprotocolhandler) Poslať(cieľipaddressSieťbyteorder uint32, pprotocol uint8, dataKurzor uintptr, veľkosť uint32) {

	ipprovider.Poslať(cieľipaddressSieťbyteorder, pprotocol, dataKurzor, veľkosť)
}
func (vlastný *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpethernetRámechandler struct {
	TEthernetRámechandler
}

var ipprovider TInternetprotocolprovider

func (vlastný *IpethernetRámechandler) EthernetRámecreceivewhen(dataKurzor uintptr, veľkosť int) bool {
	ipKonzola.MTlačiť(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetRámecreceivewhen(dataKurzor, uint32(veľkosť))

}

func (vlastný *IpethernetRámechandler) Poslať(cieľipaddressSieťbyteorder uint64, dataKurzor uintptr, veľkosť uint32) {
	ipKonzola.MTlačiť(([]byte)("ipefhandler:send\n"))
	var ethernetTypbe = Unsignedinteger16r(0x0800)
	vlastný.TEthernetRámechandler.RámecPoslať(cieľipaddressSieťbyteorder, ethernetTypbe, dataKurzor, veľkosť)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Bránaip		uint32
	SubnetMaska	uint32
}

var efhandler IEthernetRámechandler

func (vlastný *TInternetprotocolprovider) Init(pefprovider TEthernetRámecprovider, pefhandler IEthernetRámechandler, arp Arpprovider, bránaip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Sadahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	vlastný.arpprovider = arp
	vlastný.Bránaip = bránaip
	vlastný.SubnetMaska = subnetMaska
	ipprovider = *vlastný
}
func (vlastný *TInternetprotocolprovider) EthernetRámecreceivewhen(ethernetRámecpayload uintptr, veľkosť uint32) bool {
	if veľkosť < uint32(ipVeľkosť) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Správabuffer = (*TInternetprotocolv4Správabuffer)(Pointer(ethernetRámecpayload))
	var internetprotocolSpráva TInternetprotocolv4Správa
	internetprotocolSpráva.Init(*buffer_2)

	var reply bool = false

	if internetprotocolSpráva.cieľipaddress == uint32(efhandler.Getipaddress()) {

		var dĺžka uint32 = uint32(internetprotocolSpráva.celkomDĺžka)
		if dĺžka > veľkosť {
			dĺžka = veľkosť
		}
		if handler_2[internetprotocolSpráva.protocol] != nil {
			reply = handler_2[internetprotocolSpráva.protocol].Internetprotocolreceivewhen(internetprotocolSpráva.zdrojipaddress, internetprotocolSpráva.cieľipaddress, ethernetRámecpayload+uintptr(4*internetprotocolSpráva.headerDĺžka), uint32(dĺžka-uint32(4*internetprotocolSpráva.headerDĺžka)))

		}
	}

	if reply {

		var temporary = internetprotocolSpráva.cieľipaddress
		internetprotocolSpráva.cieľipaddress = internetprotocolSpráva.zdrojipaddress
		internetprotocolSpráva.zdrojipaddress = temporary

		internetprotocolSpráva.častolive = 0x40
		internetprotocolSpráva.checksum = 0

		internetprotocolSpráva.Sadabuffer(buffer_2)
		internetprotocolSpráva.checksum = vlastný.Checksum((*([4096]uint16))(Pointer(ethernetRámecpayload)), uint32(4*internetprotocolSpráva.headerDĺžka))

		internetprotocolSpráva.Sadabuffer(buffer_2)

	}

	ipKonzola.MTlačiť(([]byte)("ipmessage"))
	ipKonzola.MUnsignedinteger32Tlačiť(internetprotocolSpráva.zdrojipaddress)
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MUnsignedinteger32Tlačiť(internetprotocolSpráva.cieľipaddress)
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Tlačiť(uint16(internetprotocolSpráva.headerDĺžka))
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Tlačiť(uint16(internetprotocolSpráva.verzia))
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MUnsignedinteger16Tlačiť(internetprotocolSpráva.celkomDĺžka)
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MUnsignedinteger32Tlačiť(uint32(efhandler.Getipaddress()))
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MTlačiť(([]byte)("\n"))

	return reply

}
func (vlastný *TInternetprotocolprovider) Poslať(cieľipaddressSieťbyteorder uint32, protocol uint8, dataKurzor uintptr, veľkosť uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Správabuffer = (*TInternetprotocolv4Správabuffer)(Pointer(&buffer1_2))
	var správa TInternetprotocolv4Správa = TInternetprotocolv4Správa{}
	správa.verzia = 4
	správa.headerDĺžka = ipVeľkosť / 4
	správa.tos = 0
	správa.celkomDĺžka = Unsignedinteger16r(uint16(veľkosť + uint32(ipVeľkosť)))

	správa.ident = 0x0100
	správa.príznakyaPosunutie = 0x0040
	správa.častolive = 0x40
	správa.protocol = protocol

	správa.cieľipaddress = cieľipaddressSieťbyteorder

	správa.zdrojipaddress = uint32(efhandler.Getipaddress())

	správa.checksum = 0

	správa.Sadabuffer(buffer_2)
	správa.checksum = vlastný.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVeľkosť))
	správa.Sadabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKurzor))

	for i := 0; i < int(veľkosť); i++ {

		buffer1_2[i+int(ipVeľkosť)] = databuffer_2[i]
	}

	ipKonzola.MTlačiťxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(veľkosť)+int(ipVeľkosť); i++ {
		ipKonzola.MHexadecimalTlačiť(buffer1_2[i])
	}
	ipKonzola.MTlačiť(([]byte)(":"))
	ipKonzola.MTlačiť(([]byte)("]\n"))

	var nasledujúcihopipaddressSieťbyteorder uint32 = cieľipaddressSieťbyteorder
	if (cieľipaddressSieťbyteorder & vlastný.SubnetMaska) != (správa.zdrojipaddress & vlastný.SubnetMaska) {
		nasledujúcihopipaddressSieťbyteorder = vlastný.Bránaip
	}

	var poslaťdataKurzor = uintptr(Pointer(&buffer1_2))
	ipKonzola.MUnsignedinteger32Tlačiť(nasledujúcihopipaddressSieťbyteorder)

	var ethernetTypbe = Unsignedinteger16r(0x0800)
	efhandler.RámecPoslať(vlastný.arpprovider.Resolve(nasledujúcihopipaddressSieťbyteorder), ethernetTypbe, poslaťdataKurzor, uint32(ipVeľkosť)+uint32(veľkosť))

}
func (vlastný *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, dĺžkanaBajty uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajty [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (dĺžkanaBajty % 2) != 0 {
		temporary += uint32(uint16(dataBajty[dĺžkanaBajty-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (vlastný *TInternetprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
