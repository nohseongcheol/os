package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetOkvir"
import . "arp"

var ipconsole TConsole = TConsole{}

type TSpletprotocolv4Sporočilobuffer struct {
	lenver		byte
	tos		byte
	skupnoDolžina	[2]byte

	ident			[2]byte
	zastaviceandoffset	[2]byte

	častolive	byte
	protocol	byte
	checksum	[2]byte

	viripaddress	[4]byte
	ciljipaddress	[4]byte
}

var ipVelikost uint8 = (4 + 4 + 4 + 8)

type TSpletprotocolv4Sporočilo struct {
	headerDolžina	uint8
	različica	uint8
	tos		uint8
	skupnoDolžina	uint16

	ident			uint16
	zastaviceandoffset	uint16

	častolive	uint8
	protocol	uint8
	checksum	uint16

	viripaddress	uint32
	ciljipaddress	uint32
}

func (sam *TSpletprotocolv4Sporočilo) Init(buffer_2 TSpletprotocolv4Sporočilobuffer) {

	sam.različica = ((buffer_2.lenver & 0xF0) >> 4)
	sam.headerDolžina = buffer_2.lenver & 0x0F
	sam.tos = buffer_2.tos
	sam.skupnoDolžina = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.skupnoDolžina))

	sam.ident = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.ident))
	sam.zastaviceandoffset = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.zastaviceandoffset))

	sam.častolive = buffer_2.častolive
	sam.protocol = buffer_2.protocol
	sam.checksum = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.checksum))

	sam.viripaddress = Unsignedinteger32r(Poljetounsignedinteger32(buffer_2.viripaddress))
	sam.ciljipaddress = Unsignedinteger32r(Poljetounsignedinteger32(buffer_2.ciljipaddress))

}
func (sam *TSpletprotocolv4Sporočilo) Množicabuffer(buffer_2 *TSpletprotocolv4Sporočilobuffer) {

	buffer_2.lenver = byte(((sam.različica & 0x0F) << 4) | (sam.headerDolžina & 0x0F))
	buffer_2.tos = sam.tos
	buffer_2.skupnoDolžina = Unsignedinteger16toPolje(sam.skupnoDolžina)

	buffer_2.ident = Unsignedinteger16toPolje(sam.ident)
	buffer_2.zastaviceandoffset = Unsignedinteger16toPolje(sam.zastaviceandoffset)

	buffer_2.častolive = sam.častolive
	buffer_2.protocol = sam.protocol
	buffer_2.checksum = Unsignedinteger16toPolje(sam.checksum)

	buffer_2.viripaddress = Unsignedinteger32toPolje(sam.viripaddress)
	buffer_2.ciljipaddress = Unsignedinteger32toPolje(sam.ciljipaddress)

}

type ISpletprotocolhandler interface {
	Init(backend TSpletprotocolprovider, pihandler ISpletprotocolhandler, pprotocol uint8)
	Spletprotocolreceivewhen(viripaddressOmrežjebyteorder uint32, ciljipaddressOmrežjebyteorder uint32, dataKazalnik uintptr, velikost uint32) bool
	Pošlji(ciljipaddressOmrežjebyteorder uint32, pprotocol uint8, dataKazalnik uintptr, velikost uint32)
	Providerget() *TSpletprotocolprovider
}

type TSpletprotocolhandler struct {
}

var ipethernetOkvirhandler IpethernetOkvirhandler = IpethernetOkvirhandler{}
var protocol uint8

func (sam *TSpletprotocolhandler) Init(backend TSpletprotocolprovider, pihandler ISpletprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (sam *TSpletprotocolhandler) Spletprotocolreceivewhen(viripaddressOmrežjebyteorder uint32, ciljipaddressOmrežjebyteorder uint32, dataKazalnik uintptr, velikost uint32) bool {
	ipconsole.MNatisni(([]byte)("ipHandler:OnInternet"))
	return false
}
func (sam *TSpletprotocolhandler) Pošlji(ciljipaddressOmrežjebyteorder uint32, pprotocol uint8, dataKazalnik uintptr, velikost uint32) {

	ipprovider.Pošlji(ciljipaddressOmrežjebyteorder, pprotocol, dataKazalnik, velikost)
}
func (sam *TSpletprotocolhandler) Providerget() *TSpletprotocolprovider {
	return &ipprovider
}

type IpethernetOkvirhandler struct {
	TEthernetOkvirhandler
}

var ipprovider TSpletprotocolprovider

func (sam *IpethernetOkvirhandler) EthernetOkvirreceivewhen(dataKazalnik uintptr, velikost int) bool {
	ipconsole.MNatisni(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetOkvirreceivewhen(dataKazalnik, uint32(velikost))

}

func (sam *IpethernetOkvirhandler) Pošlji(ciljipaddressOmrežjebyteorder uint64, dataKazalnik uintptr, velikost uint32) {
	ipconsole.MNatisni(([]byte)("ipefhandler:send\n"))
	var ethernetVrstabe = Unsignedinteger16r(0x0800)
	sam.TEthernetOkvirhandler.OkvirPošlji(ciljipaddressOmrežjebyteorder, ethernetVrstabe, dataKazalnik, velikost)

}

var handler_2 [255]ISpletprotocolhandler

type TSpletprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetOkvirhandler

func (sam *TSpletprotocolprovider) Init(pefprovider TEthernetOkvirprovider, pefhandler IEthernetOkvirhandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Množicahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	sam.arpprovider = arp
	sam.Gatewayip = gatewayip
	sam.SubnetMaska = subnetMaska
	ipprovider = *sam
}
func (sam *TSpletprotocolprovider) EthernetOkvirreceivewhen(ethernetOkvirpayload uintptr, velikost uint32) bool {
	if velikost < uint32(ipVelikost) {
		return false
	}

	var buffer_2 *TSpletprotocolv4Sporočilobuffer = (*TSpletprotocolv4Sporočilobuffer)(Pointer(ethernetOkvirpayload))
	var spletprotocolSporočilo TSpletprotocolv4Sporočilo
	spletprotocolSporočilo.Init(*buffer_2)

	var reply bool = false

	if spletprotocolSporočilo.ciljipaddress == uint32(efhandler.Getipaddress()) {

		var dolžina uint32 = uint32(spletprotocolSporočilo.skupnoDolžina)
		if dolžina > velikost {
			dolžina = velikost
		}
		if handler_2[spletprotocolSporočilo.protocol] != nil {
			reply = handler_2[spletprotocolSporočilo.protocol].Spletprotocolreceivewhen(spletprotocolSporočilo.viripaddress, spletprotocolSporočilo.ciljipaddress, ethernetOkvirpayload+uintptr(4*spletprotocolSporočilo.headerDolžina), uint32(dolžina-uint32(4*spletprotocolSporočilo.headerDolžina)))

		}
	}

	if reply {

		var temporary = spletprotocolSporočilo.ciljipaddress
		spletprotocolSporočilo.ciljipaddress = spletprotocolSporočilo.viripaddress
		spletprotocolSporočilo.viripaddress = temporary

		spletprotocolSporočilo.častolive = 0x40
		spletprotocolSporočilo.checksum = 0

		spletprotocolSporočilo.Množicabuffer(buffer_2)
		spletprotocolSporočilo.checksum = sam.Checksum((*([4096]uint16))(Pointer(ethernetOkvirpayload)), uint32(4*spletprotocolSporočilo.headerDolžina))

		spletprotocolSporočilo.Množicabuffer(buffer_2)

	}

	ipconsole.MNatisni(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Natisni(spletprotocolSporočilo.viripaddress)
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MUnsignedinteger32Natisni(spletprotocolSporočilo.ciljipaddress)
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MUnsignedinteger16Natisni(uint16(spletprotocolSporočilo.headerDolžina))
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MUnsignedinteger16Natisni(uint16(spletprotocolSporočilo.različica))
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MUnsignedinteger16Natisni(spletprotocolSporočilo.skupnoDolžina)
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MUnsignedinteger32Natisni(uint32(efhandler.Getipaddress()))
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MNatisni(([]byte)("\n"))

	return reply

}
func (sam *TSpletprotocolprovider) Pošlji(ciljipaddressOmrežjebyteorder uint32, protocol uint8, dataKazalnik uintptr, velikost uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TSpletprotocolv4Sporočilobuffer = (*TSpletprotocolv4Sporočilobuffer)(Pointer(&buffer1_2))
	var sporočilo TSpletprotocolv4Sporočilo = TSpletprotocolv4Sporočilo{}
	sporočilo.različica = 4
	sporočilo.headerDolžina = ipVelikost / 4
	sporočilo.tos = 0
	sporočilo.skupnoDolžina = Unsignedinteger16r(uint16(velikost + uint32(ipVelikost)))

	sporočilo.ident = 0x0100
	sporočilo.zastaviceandoffset = 0x0040
	sporočilo.častolive = 0x40
	sporočilo.protocol = protocol

	sporočilo.ciljipaddress = ciljipaddressOmrežjebyteorder

	sporočilo.viripaddress = uint32(efhandler.Getipaddress())

	sporočilo.checksum = 0

	sporočilo.Množicabuffer(buffer_2)
	sporočilo.checksum = sam.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipVelikost))
	sporočilo.Množicabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKazalnik))

	for i := 0; i < int(velikost); i++ {

		buffer1_2[i+int(ipVelikost)] = databuffer_2[i]
	}

	ipconsole.MNatisnixy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(velikost)+int(ipVelikost); i++ {
		ipconsole.MHexadecimalNatisni(buffer1_2[i])
	}
	ipconsole.MNatisni(([]byte)(":"))
	ipconsole.MNatisni(([]byte)("]\n"))

	var naslednjehopipaddressOmrežjebyteorder uint32 = ciljipaddressOmrežjebyteorder
	if (ciljipaddressOmrežjebyteorder & sam.SubnetMaska) != (sporočilo.viripaddress & sam.SubnetMaska) {
		naslednjehopipaddressOmrežjebyteorder = sam.Gatewayip
	}

	var pošljidataKazalnik = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Natisni(naslednjehopipaddressOmrežjebyteorder)

	var ethernetVrstabe = Unsignedinteger16r(0x0800)
	efhandler.OkvirPošlji(sam.arpprovider.Resolve(naslednjehopipaddressOmrežjebyteorder), ethernetVrstabe, pošljidataKazalnik, uint32(ipVelikost)+uint32(velikost))

}
func (sam *TSpletprotocolprovider) Checksum(pdata *[4096]uint16, dolžinaVhodnoBajtov uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajtov [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (dolžinaVhodnoBajtov % 2) != 0 {
		temporary += uint32(uint16(dataBajtov[dolžinaVhodnoBajtov-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (sam *TSpletprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
