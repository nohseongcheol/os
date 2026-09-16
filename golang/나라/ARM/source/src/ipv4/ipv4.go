/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetՇրջանակ"
import . "arp"

var ipconsole TConsole = TConsole{}

type TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer struct {
	lenver			byte
	tos			byte
	ընդհանուրԵրկարություն	[2]byte

	ident			[2]byte
	դրոշներandoffset	[2]byte

	ժամանակtolive	byte
	protocol	byte
	checksum	[2]byte

	աղբյուրipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipՉափս uint8 = (4 + 4 + 4 + 8)

type TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ struct {
	headerԵրկարություն	uint8
	version			uint8
	tos			uint8
	ընդհանուրԵրկարություն	uint16

	ident			uint16
	դրոշներandoffset	uint16

	ժամանակtolive	uint8
	protocol	uint8
	checksum	uint16

	աղբյուրipaddress	uint32
	destinationipaddress	uint32
}

func (ինքնուրույն *TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Init(buffer_2 TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {

	ինքնուրույն.version = ((buffer_2.lenver & 0xF0) >> 4)
	ինքնուրույն.headerԵրկարություն = buffer_2.lenver & 0x0F
	ինքնուրույն.tos = buffer_2.tos
	ինքնուրույն.ընդհանուրԵրկարություն = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.ընդհանուրԵրկարություն))

	ինքնուրույն.ident = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.ident))
	ինքնուրույն.դրոշներandoffset = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.դրոշներandoffset))

	ինքնուրույն.ժամանակtolive = buffer_2.ժամանակtolive
	ինքնուրույն.protocol = buffer_2.protocol
	ինքնուրույն.checksum = Unsignedinteger16r(Զանգվածtounsignedinteger16(buffer_2.checksum))

	ինքնուրույն.աղբյուրipaddress = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer_2.աղբյուրipaddress))
	ինքնուրույն.destinationipaddress = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer_2.destinationipaddress))

}
func (ինքնուրույն *TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ) Setbuffer(buffer_2 *TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer) {

	buffer_2.lenver = byte(((ինքնուրույն.version & 0x0F) << 4) | (ինքնուրույն.headerԵրկարություն & 0x0F))
	buffer_2.tos = ինքնուրույն.tos
	buffer_2.ընդհանուրԵրկարություն = Unsignedinteger16toԶանգված(ինքնուրույն.ընդհանուրԵրկարություն)

	buffer_2.ident = Unsignedinteger16toԶանգված(ինքնուրույն.ident)
	buffer_2.դրոշներandoffset = Unsignedinteger16toԶանգված(ինքնուրույն.դրոշներandoffset)

	buffer_2.ժամանակtolive = ինքնուրույն.ժամանակtolive
	buffer_2.protocol = ինքնուրույն.protocol
	buffer_2.checksum = Unsignedinteger16toԶանգված(ինքնուրույն.checksum)

	buffer_2.աղբյուրipaddress = Unsignedinteger32toԶանգված(ինքնուրույն.աղբյուրipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toԶանգված(ինքնուրույն.destinationipaddress)

}

type IՀամացանցprotocolhandler interface {
	Init(backend TՀամացանցprotocolprovider, pihandler IՀամացանցprotocolhandler, pprotocol uint8)
	Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder uint32, destinationipaddressՑանցbyteorder uint32, dataՑուցիչ uintptr, չափս uint32) bool
	ՈՒղարկել(destinationipaddressՑանցbyteorder uint32, pprotocol uint8, dataՑուցիչ uintptr, չափս uint32)
	Providerget() *TՀամացանցprotocolprovider
}

type TՀամացանցprotocolhandler struct {
}

var ipethernetՇրջանակhandler IpethernetՇրջանակhandler = IpethernetՇրջանակhandler{}
var protocol uint8

func (ինքնուրույն *TՀամացանցprotocolhandler) Init(backend TՀամացանցprotocolprovider, pihandler IՀամացանցprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (ինքնուրույն *TՀամացանցprotocolhandler) Համացանցprotocolreceivewhen(աղբյուրipaddressՑանցbyteorder uint32, destinationipaddressՑանցbyteorder uint32, dataՑուցիչ uintptr, չափս uint32) bool {
	ipconsole.MՏպել(([]byte)("ipHandler:OnInternet"))
	return false
}
func (ինքնուրույն *TՀամացանցprotocolhandler) ՈՒղարկել(destinationipaddressՑանցbyteorder uint32, pprotocol uint8, dataՑուցիչ uintptr, չափս uint32) {

	ipprovider.ՈՒղարկել(destinationipaddressՑանցbyteorder, pprotocol, dataՑուցիչ, չափս)
}
func (ինքնուրույն *TՀամացանցprotocolhandler) Providerget() *TՀամացանցprotocolprovider {
	return &ipprovider
}

type IpethernetՇրջանակhandler struct {
	TEthernetՇրջանակhandler
}

var ipprovider TՀամացանցprotocolprovider

func (ինքնուրույն *IpethernetՇրջանակhandler) EthernetՇրջանակreceivewhen(dataՑուցիչ uintptr, չափս int) bool {
	ipconsole.MՏպել(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetՇրջանակreceivewhen(dataՑուցիչ, uint32(չափս))

}

func (ինքնուրույն *IpethernetՇրջանակhandler) ՈՒղարկել(destinationipaddressՑանցbyteorder uint64, dataՑուցիչ uintptr, չափս uint32) {
	ipconsole.MՏպել(([]byte)("ipefhandler:send\n"))
	var ethernetՏիպbe = Unsignedinteger16r(0x0800)
	ինքնուրույն.TEthernetՇրջանակhandler.ՇրջանակՈՒղարկել(destinationipaddressՑանցbyteorder, ethernetՏիպbe, dataՑուցիչ, չափս)

}

var handler_2 [255]IՀամացանցprotocolhandler

type TՀամացանցprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEthernetՇրջանակhandler

func (ինքնուրույն *TՀամացանցprotocolprovider) Init(pefprovider TEthernetՇրջանակprovider, pefhandler IEthernetՇրջանակhandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sethandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	ինքնուրույն.arpprovider = arp
	ինքնուրույն.Gatewayip = gatewayip
	ինքնուրույն.Subnetmask = subnetmask
	ipprovider = *ինքնուրույն
}
func (ինքնուրույն *TՀամացանցprotocolprovider) EthernetՇրջանակreceivewhen(ethernetՇրջանակpayload uintptr, չափս uint32) bool {
	if չափս < uint32(ipՉափս) {
		return false
	}

	var buffer_2 *TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = (*TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer)(Pointer(ethernetՇրջանակpayload))
	var համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ
	համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.Init(*buffer_2)

	var reply bool = false

	if համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var երկարություն uint32 = uint32(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ընդհանուրԵրկարություն)
		if երկարություն > չափս {
			երկարություն = չափս
		}
		if handler_2[համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.protocol] != nil {
			reply = handler_2[համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.protocol].Համացանցprotocolreceivewhen(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress, համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress, ethernetՇրջանակpayload+uintptr(4*համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.headerԵրկարություն), uint32(երկարություն-uint32(4*համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.headerԵրկարություն)))

		}
	}

	if reply {

		var temporary = համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress
		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress = համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress
		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress = temporary

		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ժամանակtolive = 0x40
		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.checksum = 0

		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.Setbuffer(buffer_2)
		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.checksum = ինքնուրույն.Checksum((*([4096]uint16))(Pointer(ethernetՇրջանակpayload)), uint32(4*համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.headerԵրկարություն))

		համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.Setbuffer(buffer_2)

	}

	ipconsole.MՏպել(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Տպել(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress)
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MUnsignedinteger32Տպել(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress)
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MUnsignedinteger16Տպել(uint16(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.headerԵրկարություն))
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MUnsignedinteger16Տպել(uint16(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.version))
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MUnsignedinteger16Տպել(համացանցprotocolՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ընդհանուրԵրկարություն)
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MUnsignedinteger32Տպել(uint32(efhandler.Getipaddress()))
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MՏպել(([]byte)("\n"))

	return reply

}
func (ինքնուրույն *TՀամացանցprotocolprovider) ՈՒղարկել(destinationipaddressՑանցbyteorder uint32, protocol uint8, dataՑուցիչ uintptr, չափս uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer = (*TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆbuffer)(Pointer(&buffer1_2))
	var հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ = TՀամացանցprotocolv4ՀԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ{}
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.version = 4
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.headerԵրկարություն = ipՉափս / 4
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.tos = 0
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ընդհանուրԵրկարություն = Unsignedinteger16r(uint16(չափս + uint32(ipՉափս)))

	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ident = 0x0100
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.դրոշներandoffset = 0x0040
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.ժամանակtolive = 0x40
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.protocol = protocol

	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.destinationipaddress = destinationipaddressՑանցbyteorder

	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress = uint32(efhandler.Getipaddress())

	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.checksum = 0

	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.Setbuffer(buffer_2)
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.checksum = ինքնուրույն.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipՉափս))
	հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataՑուցիչ))

	for i := 0; i < int(չափս); i++ {

		buffer1_2[i+int(ipՉափս)] = databuffer_2[i]
	}

	ipconsole.MՏպելxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(չափս)+int(ipՉափս); i++ {
		ipconsole.MHexadecimalՏպել(buffer1_2[i])
	}
	ipconsole.MՏպել(([]byte)(":"))
	ipconsole.MՏպել(([]byte)("]\n"))

	var հաջորդhopipaddressՑանցbyteorder uint32 = destinationipaddressՑանցbyteorder
	if (destinationipaddressՑանցbyteorder & ինքնուրույն.Subnetmask) != (հԱՂՈՐԴԱԳՐՈՒԹՅՈՒՆ.աղբյուրipaddress & ինքնուրույն.Subnetmask) {
		հաջորդhopipaddressՑանցbyteorder = ինքնուրույն.Gatewayip
	}

	var ոՒղարկելdataՑուցիչ = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Տպել(հաջորդhopipaddressՑանցbyteorder)

	var ethernetՏիպbe = Unsignedinteger16r(0x0800)
	efhandler.ՇրջանակՈՒղարկել(ինքնուրույն.arpprovider.Resolve(հաջորդhopipaddressՑանցbyteorder), ethernetՏիպbe, ոՒղարկելdataՑուցիչ, uint32(ipՉափս)+uint32(չափս))

}
func (ինքնուրույն *TՀամացանցprotocolprovider) Checksum(pdata *[4096]uint16, երկարությունՄեջԲայթեր uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataԲայթեր [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (երկարությունՄեջԲայթեր % 2) != 0 {
		temporary += uint32(uint16(dataԲայթեր[երկարությունՄեջԲայթեր-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (ինքնուրույն *TՀամացանցprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
