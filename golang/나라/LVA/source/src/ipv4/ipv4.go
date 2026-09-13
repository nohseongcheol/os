package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ethernetIetvars"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetsprotocolv4Ziņojumsbuffer struct {
	lenver		byte
	tos		byte
	kopāGarums	[2]byte

	ident		[2]byte
	karogiandoffset	[2]byte

	laikstolive	byte
	protocol	byte
	checksum	[2]byte

	avotsipaddress	[4]byte
	mērķisipaddress	[4]byte
}

var ipIzmērs uint8 = (4 + 4 + 4 + 8)

type TInternetsprotocolv4Ziņojums struct {
	headerGarums	uint8
	versija		uint8
	tos		uint8
	kopāGarums	uint16

	ident		uint16
	karogiandoffset	uint16

	laikstolive	uint8
	protocol	uint8
	checksum	uint16

	avotsipaddress	uint32
	mērķisipaddress	uint32
}

func (pats *TInternetsprotocolv4Ziņojums) Init(buffer_2 TInternetsprotocolv4Ziņojumsbuffer) {

	pats.versija = ((buffer_2.lenver & 0xF0) >> 4)
	pats.headerGarums = buffer_2.lenver & 0x0F
	pats.tos = buffer_2.tos
	pats.kopāGarums = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.kopāGarums))

	pats.ident = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.ident))
	pats.karogiandoffset = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.karogiandoffset))

	pats.laikstolive = buffer_2.laikstolive
	pats.protocol = buffer_2.protocol
	pats.checksum = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.checksum))

	pats.avotsipaddress = Unsignedinteger32r(Masīvstounsignedinteger32(buffer_2.avotsipaddress))
	pats.mērķisipaddress = Unsignedinteger32r(Masīvstounsignedinteger32(buffer_2.mērķisipaddress))

}
func (pats *TInternetsprotocolv4Ziņojums) Kopabuffer(buffer_2 *TInternetsprotocolv4Ziņojumsbuffer) {

	buffer_2.lenver = byte(((pats.versija & 0x0F) << 4) | (pats.headerGarums & 0x0F))
	buffer_2.tos = pats.tos
	buffer_2.kopāGarums = Unsignedinteger16toMasīvs(pats.kopāGarums)

	buffer_2.ident = Unsignedinteger16toMasīvs(pats.ident)
	buffer_2.karogiandoffset = Unsignedinteger16toMasīvs(pats.karogiandoffset)

	buffer_2.laikstolive = pats.laikstolive
	buffer_2.protocol = pats.protocol
	buffer_2.checksum = Unsignedinteger16toMasīvs(pats.checksum)

	buffer_2.avotsipaddress = Unsignedinteger32toMasīvs(pats.avotsipaddress)
	buffer_2.mērķisipaddress = Unsignedinteger32toMasīvs(pats.mērķisipaddress)

}

type IInternetsprotocolhandler interface {
	Init(backend TInternetsprotocolprovider, pihandler IInternetsprotocolhandler, pprotocol uint8)
	Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder uint32, mērķisipaddressTīklsbyteorder uint32, dataKursors uintptr, izmērs uint32) bool
	Sūtīt(mērķisipaddressTīklsbyteorder uint32, pprotocol uint8, dataKursors uintptr, izmērs uint32)
	Providerget() *TInternetsprotocolprovider
}

type TInternetsprotocolhandler struct {
}

var ipethernetIetvarshandler IpethernetIetvarshandler = IpethernetIetvarshandler{}
var protocol uint8

func (pats *TInternetsprotocolhandler) Init(backend TInternetsprotocolprovider, pihandler IInternetsprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (pats *TInternetsprotocolhandler) Internetsprotocolreceivewhen(avotsipaddressTīklsbyteorder uint32, mērķisipaddressTīklsbyteorder uint32, dataKursors uintptr, izmērs uint32) bool {
	ipconsole.MDrukāt(([]byte)("ipHandler:OnInternet"))
	return false
}
func (pats *TInternetsprotocolhandler) Sūtīt(mērķisipaddressTīklsbyteorder uint32, pprotocol uint8, dataKursors uintptr, izmērs uint32) {

	ipprovider.Sūtīt(mērķisipaddressTīklsbyteorder, pprotocol, dataKursors, izmērs)
}
func (pats *TInternetsprotocolhandler) Providerget() *TInternetsprotocolprovider {
	return &ipprovider
}

type IpethernetIetvarshandler struct {
	TEthernetIetvarshandler
}

var ipprovider TInternetsprotocolprovider

func (pats *IpethernetIetvarshandler) EthernetIetvarsreceivewhen(dataKursors uintptr, izmērs int) bool {
	ipconsole.MDrukāt(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.EthernetIetvarsreceivewhen(dataKursors, uint32(izmērs))

}

func (pats *IpethernetIetvarshandler) Sūtīt(mērķisipaddressTīklsbyteorder uint64, dataKursors uintptr, izmērs uint32) {
	ipconsole.MDrukāt(([]byte)("ipefhandler:send\n"))
	var ethernetTipsbe = Unsignedinteger16r(0x0800)
	pats.TEthernetIetvarshandler.IetvarsSūtīt(mērķisipaddressTīklsbyteorder, ethernetTipsbe, dataKursors, izmērs)

}

var handler_2 [255]IInternetsprotocolhandler

type TInternetsprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetIetvarshandler

func (pats *TInternetsprotocolprovider) Init(pefprovider TEthernetIetvarsprovider, pefhandler IEthernetIetvarshandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Kopahandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	pats.arpprovider = arp
	pats.Gatewayip = gatewayip
	pats.SubnetMaska = subnetMaska
	ipprovider = *pats
}
func (pats *TInternetsprotocolprovider) EthernetIetvarsreceivewhen(ethernetIetvarspayload uintptr, izmērs uint32) bool {
	if izmērs < uint32(ipIzmērs) {
		return false
	}

	var buffer_2 *TInternetsprotocolv4Ziņojumsbuffer = (*TInternetsprotocolv4Ziņojumsbuffer)(Pointer(ethernetIetvarspayload))
	var internetsprotocolZiņojums TInternetsprotocolv4Ziņojums
	internetsprotocolZiņojums.Init(*buffer_2)

	var reply bool = false

	if internetsprotocolZiņojums.mērķisipaddress == uint32(efhandler.Getipaddress()) {

		var garums uint32 = uint32(internetsprotocolZiņojums.kopāGarums)
		if garums > izmērs {
			garums = izmērs
		}
		if handler_2[internetsprotocolZiņojums.protocol] != nil {
			reply = handler_2[internetsprotocolZiņojums.protocol].Internetsprotocolreceivewhen(internetsprotocolZiņojums.avotsipaddress, internetsprotocolZiņojums.mērķisipaddress, ethernetIetvarspayload+uintptr(4*internetsprotocolZiņojums.headerGarums), uint32(garums-uint32(4*internetsprotocolZiņojums.headerGarums)))

		}
	}

	if reply {

		var temporary = internetsprotocolZiņojums.mērķisipaddress
		internetsprotocolZiņojums.mērķisipaddress = internetsprotocolZiņojums.avotsipaddress
		internetsprotocolZiņojums.avotsipaddress = temporary

		internetsprotocolZiņojums.laikstolive = 0x40
		internetsprotocolZiņojums.checksum = 0

		internetsprotocolZiņojums.Kopabuffer(buffer_2)
		internetsprotocolZiņojums.checksum = pats.Checksum((*([4096]uint16))(Pointer(ethernetIetvarspayload)), uint32(4*internetsprotocolZiņojums.headerGarums))

		internetsprotocolZiņojums.Kopabuffer(buffer_2)

	}

	ipconsole.MDrukāt(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Drukāt(internetsprotocolZiņojums.avotsipaddress)
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MUnsignedinteger32Drukāt(internetsprotocolZiņojums.mērķisipaddress)
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MUnsignedinteger16Drukāt(uint16(internetsprotocolZiņojums.headerGarums))
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MUnsignedinteger16Drukāt(uint16(internetsprotocolZiņojums.versija))
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MUnsignedinteger16Drukāt(internetsprotocolZiņojums.kopāGarums)
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MUnsignedinteger32Drukāt(uint32(efhandler.Getipaddress()))
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MDrukāt(([]byte)("\n"))

	return reply

}
func (pats *TInternetsprotocolprovider) Sūtīt(mērķisipaddressTīklsbyteorder uint32, protocol uint8, dataKursors uintptr, izmērs uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetsprotocolv4Ziņojumsbuffer = (*TInternetsprotocolv4Ziņojumsbuffer)(Pointer(&buffer1_2))
	var ziņojums TInternetsprotocolv4Ziņojums = TInternetsprotocolv4Ziņojums{}
	ziņojums.versija = 4
	ziņojums.headerGarums = ipIzmērs / 4
	ziņojums.tos = 0
	ziņojums.kopāGarums = Unsignedinteger16r(uint16(izmērs + uint32(ipIzmērs)))

	ziņojums.ident = 0x0100
	ziņojums.karogiandoffset = 0x0040
	ziņojums.laikstolive = 0x40
	ziņojums.protocol = protocol

	ziņojums.mērķisipaddress = mērķisipaddressTīklsbyteorder

	ziņojums.avotsipaddress = uint32(efhandler.Getipaddress())

	ziņojums.checksum = 0

	ziņojums.Kopabuffer(buffer_2)
	ziņojums.checksum = pats.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipIzmērs))
	ziņojums.Kopabuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursors))

	for i := 0; i < int(izmērs); i++ {

		buffer1_2[i+int(ipIzmērs)] = databuffer_2[i]
	}

	ipconsole.MDrukātxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(izmērs)+int(ipIzmērs); i++ {
		ipconsole.MHexadecimalDrukāt(buffer1_2[i])
	}
	ipconsole.MDrukāt(([]byte)(":"))
	ipconsole.MDrukāt(([]byte)("]\n"))

	var nākamaishopipaddressTīklsbyteorder uint32 = mērķisipaddressTīklsbyteorder
	if (mērķisipaddressTīklsbyteorder & pats.SubnetMaska) != (ziņojums.avotsipaddress & pats.SubnetMaska) {
		nākamaishopipaddressTīklsbyteorder = pats.Gatewayip
	}

	var sūtītdataKursors = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Drukāt(nākamaishopipaddressTīklsbyteorder)

	var ethernetTipsbe = Unsignedinteger16r(0x0800)
	efhandler.IetvarsSūtīt(pats.arpprovider.Resolve(nākamaishopipaddressTīklsbyteorder), ethernetTipsbe, sūtītdataKursors, uint32(ipIzmērs)+uint32(izmērs))

}
func (pats *TInternetsprotocolprovider) Checksum(pdata *[4096]uint16, garumsIenākošāBaiti uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBaiti [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (garumsIenākošāBaiti % 2) != 0 {
		temporary += uint32(uint16(dataBaiti[garumsIenākošāBaiti-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (pats *TInternetsprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
