/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "consola"
import . "cableMarc"
import . "arp"

var ipConsola TConsola = TConsola{}

type TInternetprotocolv4Missatgebuffer struct {
	lenver		byte
	tos		byte
	totalDurada	[2]byte

	ident			[2]byte
	senyaladorsioffset	[2]byte

	horatolive	byte
	protocol	byte
	checksum	[2]byte

	origenipAdreça		[4]byte
	destinacióipAdreça	[4]byte
}

var ipMida uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Missatge struct {
	headerDurada	uint8
	versió		uint8
	tos		uint8
	totalDurada	uint16

	ident			uint16
	senyaladorsioffset	uint16

	horatolive	uint8
	protocol	uint8
	checksum	uint16

	origenipAdreça		uint32
	destinacióipAdreça	uint32
}

func (unmateix *TInternetprotocolv4Missatge) Init(buffer_2 TInternetprotocolv4Missatgebuffer) {

	unmateix.versió = ((buffer_2.lenver & 0xF0) >> 4)
	unmateix.headerDurada = buffer_2.lenver & 0x0F
	unmateix.tos = buffer_2.tos
	unmateix.totalDurada = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.totalDurada))

	unmateix.ident = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.ident))
	unmateix.senyaladorsioffset = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.senyaladorsioffset))

	unmateix.horatolive = buffer_2.horatolive
	unmateix.protocol = buffer_2.protocol
	unmateix.checksum = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.checksum))

	unmateix.origenipAdreça = Unsignedinteger32r(Matriutounsignedinteger32(buffer_2.origenipAdreça))
	unmateix.destinacióipAdreça = Unsignedinteger32r(Matriutounsignedinteger32(buffer_2.destinacióipAdreça))

}
func (unmateix *TInternetprotocolv4Missatge) Estableixbuffer(buffer_2 *TInternetprotocolv4Missatgebuffer) {

	buffer_2.lenver = byte(((unmateix.versió & 0x0F) << 4) | (unmateix.headerDurada & 0x0F))
	buffer_2.tos = unmateix.tos
	buffer_2.totalDurada = Unsignedinteger16toMatriu(unmateix.totalDurada)

	buffer_2.ident = Unsignedinteger16toMatriu(unmateix.ident)
	buffer_2.senyaladorsioffset = Unsignedinteger16toMatriu(unmateix.senyaladorsioffset)

	buffer_2.horatolive = unmateix.horatolive
	buffer_2.protocol = unmateix.protocol
	buffer_2.checksum = Unsignedinteger16toMatriu(unmateix.checksum)

	buffer_2.origenipAdreça = Unsignedinteger32toMatriu(unmateix.origenipAdreça)
	buffer_2.destinacióipAdreça = Unsignedinteger32toMatriu(unmateix.destinacióipAdreça)

}

type IInternetprotocolhandler interface {
	Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder uint32, destinacióipAdreçaXarxabyteorder uint32, dataPunter uintptr, mida uint32) bool
	Envia(destinacióipAdreçaXarxabyteorder uint32, pprotocol uint8, dataPunter uintptr, mida uint32)
	Providerget() *TInternetprotocolprovider
}

type TInternetprotocolhandler struct {
}

var ipCableMarchandler IpCableMarchandler = IpCableMarchandler{}
var protocol uint8

func (unmateix *TInternetprotocolhandler) Init(backend TInternetprotocolprovider, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (unmateix *TInternetprotocolhandler) Internetprotocolreceivewhen(origenipAdreçaXarxabyteorder uint32, destinacióipAdreçaXarxabyteorder uint32, dataPunter uintptr, mida uint32) bool {
	ipConsola.MImprimeix(([]byte)("ipHandler:OnInternet"))
	return false
}
func (unmateix *TInternetprotocolhandler) Envia(destinacióipAdreçaXarxabyteorder uint32, pprotocol uint8, dataPunter uintptr, mida uint32) {

	ipprovider.Envia(destinacióipAdreçaXarxabyteorder, pprotocol, dataPunter, mida)
}
func (unmateix *TInternetprotocolhandler) Providerget() *TInternetprotocolprovider {
	return &ipprovider
}

type IpCableMarchandler struct {
	TCableMarchandler
}

var ipprovider TInternetprotocolprovider

func (unmateix *IpCableMarchandler) CableMarcreceivewhen(dataPunter uintptr, mida int) bool {
	ipConsola.MImprimeix(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.CableMarcreceivewhen(dataPunter, uint32(mida))

}

func (unmateix *IpCableMarchandler) Envia(destinacióipAdreçaXarxabyteorder uint64, dataPunter uintptr, mida uint32) {
	ipConsola.MImprimeix(([]byte)("ipefhandler:send\n"))
	var cableTipusbe = Unsignedinteger16r(0x0800)
	unmateix.TCableMarchandler.MarcEnvia(destinacióipAdreçaXarxabyteorder, cableTipusbe, dataPunter, mida)

}

var handler_2 [255]IInternetprotocolhandler

type TInternetprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMàscara	uint32
}

var efhandler ICableMarchandler

func (unmateix *TInternetprotocolprovider) Init(pefprovider TCableMarcprovider, pefhandler ICableMarchandler, arp Arpprovider, gatewayip uint32, subnetMàscara uint32) {

	efhandler = pefhandler
	efhandler.Estableixhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	unmateix.arpprovider = arp
	unmateix.Gatewayip = gatewayip
	unmateix.SubnetMàscara = subnetMàscara
	ipprovider = *unmateix
}
func (unmateix *TInternetprotocolprovider) CableMarcreceivewhen(cableMarcpayload uintptr, mida uint32) bool {
	if mida < uint32(ipMida) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Missatgebuffer = (*TInternetprotocolv4Missatgebuffer)(Pointer(cableMarcpayload))
	var internetprotocolMissatge TInternetprotocolv4Missatge
	internetprotocolMissatge.Init(*buffer_2)

	var reply bool = false

	if internetprotocolMissatge.destinacióipAdreça == uint32(efhandler.GetipAdreça()) {

		var durada uint32 = uint32(internetprotocolMissatge.totalDurada)
		if durada > mida {
			durada = mida
		}
		if handler_2[internetprotocolMissatge.protocol] != nil {
			reply = handler_2[internetprotocolMissatge.protocol].Internetprotocolreceivewhen(internetprotocolMissatge.origenipAdreça, internetprotocolMissatge.destinacióipAdreça, cableMarcpayload+uintptr(4*internetprotocolMissatge.headerDurada), uint32(durada-uint32(4*internetprotocolMissatge.headerDurada)))

		}
	}

	if reply {

		var temporary = internetprotocolMissatge.destinacióipAdreça
		internetprotocolMissatge.destinacióipAdreça = internetprotocolMissatge.origenipAdreça
		internetprotocolMissatge.origenipAdreça = temporary

		internetprotocolMissatge.horatolive = 0x40
		internetprotocolMissatge.checksum = 0

		internetprotocolMissatge.Estableixbuffer(buffer_2)
		internetprotocolMissatge.checksum = unmateix.Checksum((*([4096]uint16))(Pointer(cableMarcpayload)), uint32(4*internetprotocolMissatge.headerDurada))

		internetprotocolMissatge.Estableixbuffer(buffer_2)

	}

	ipConsola.MImprimeix(([]byte)("ipmessage"))
	ipConsola.MUnsignedinteger32Imprimeix(internetprotocolMissatge.origenipAdreça)
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MUnsignedinteger32Imprimeix(internetprotocolMissatge.destinacióipAdreça)
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MUnsignedinteger16Imprimeix(uint16(internetprotocolMissatge.headerDurada))
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MUnsignedinteger16Imprimeix(uint16(internetprotocolMissatge.versió))
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MUnsignedinteger16Imprimeix(internetprotocolMissatge.totalDurada)
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MUnsignedinteger32Imprimeix(uint32(efhandler.GetipAdreça()))
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MImprimeix(([]byte)("\n"))

	return reply

}
func (unmateix *TInternetprotocolprovider) Envia(destinacióipAdreçaXarxabyteorder uint32, protocol uint8, dataPunter uintptr, mida uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Missatgebuffer = (*TInternetprotocolv4Missatgebuffer)(Pointer(&buffer1_2))
	var missatge TInternetprotocolv4Missatge = TInternetprotocolv4Missatge{}
	missatge.versió = 4
	missatge.headerDurada = ipMida / 4
	missatge.tos = 0
	missatge.totalDurada = Unsignedinteger16r(uint16(mida + uint32(ipMida)))

	missatge.ident = 0x0100
	missatge.senyaladorsioffset = 0x0040
	missatge.horatolive = 0x40
	missatge.protocol = protocol

	missatge.destinacióipAdreça = destinacióipAdreçaXarxabyteorder

	missatge.origenipAdreça = uint32(efhandler.GetipAdreça())

	missatge.checksum = 0

	missatge.Estableixbuffer(buffer_2)
	missatge.checksum = unmateix.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipMida))
	missatge.Estableixbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPunter))

	for i := 0; i < int(mida); i++ {

		buffer1_2[i+int(ipMida)] = databuffer_2[i]
	}

	ipConsola.MImprimeixxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(mida)+int(ipMida); i++ {
		ipConsola.MHexadecimalImprimeix(buffer1_2[i])
	}
	ipConsola.MImprimeix(([]byte)(":"))
	ipConsola.MImprimeix(([]byte)("]\n"))

	var següenthopipAdreçaXarxabyteorder uint32 = destinacióipAdreçaXarxabyteorder
	if (destinacióipAdreçaXarxabyteorder & unmateix.SubnetMàscara) != (missatge.origenipAdreça & unmateix.SubnetMàscara) {
		següenthopipAdreçaXarxabyteorder = unmateix.Gatewayip
	}

	var enviadataPunter = uintptr(Pointer(&buffer1_2))
	ipConsola.MUnsignedinteger32Imprimeix(següenthopipAdreçaXarxabyteorder)

	var cableTipusbe = Unsignedinteger16r(0x0800)
	efhandler.MarcEnvia(unmateix.arpprovider.Resolve(següenthopipAdreçaXarxabyteorder), cableTipusbe, enviadataPunter, uint32(ipMida)+uint32(mida))

}
func (unmateix *TInternetprotocolprovider) Checksum(pdata *[4096]uint16, duradaabytes uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var databytes [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (duradaabytes % 2) != 0 {
		temporary += uint32(uint16(databytes[duradaabytes-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (unmateix *TInternetprotocolprovider) GetipAdreça() uint64 {
	return efhandler.GetipAdreça()
}
