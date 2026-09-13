package giao_thức_mạng_liên_kết_4

import . "unsafe"
import . "util"
import . "console"
import . "khung_mạng_dùng_chung_môi_trường_truyền"
import . "arp"

var ipconsole TConsole = TConsole{}

type TMạngprotocolv4thôngbáobuffer struct {
	lenver		byte
	tos		byte
	tổngĐộdài	[2]byte

	ident		[2]byte
	cờvàoffset	[2]byte

	giờtolive	byte
	protocol	byte
	checksum	[2]byte

	mãnguồnipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipCỡ uint8 = (4 + 4 + 4 + 8)

type TMạngprotocolv4thôngbáo struct {
	headerĐộdài	uint8
	phiênbản	uint8
	tos		uint8
	tổngĐộdài	uint16

	ident		uint16
	cờvàoffset	uint16

	giờtolive	uint8
	protocol	uint8
	checksum	uint16

	mãnguồnipaddress	uint32
	destinationipaddress	uint32
}

func (mình *TMạngprotocolv4thôngbáo) Init(buffer_2 TMạngprotocolv4thôngbáobuffer) {

	mình.phiênbản = ((buffer_2.lenver & 0xF0) >> 4)
	mình.headerĐộdài = buffer_2.lenver & 0x0F
	mình.tos = buffer_2.tos
	mình.tổngĐộdài = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.tổngĐộdài))

	mình.ident = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.ident))
	mình.cờvàoffset = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.cờvàoffset))

	mình.giờtolive = buffer_2.giờtolive
	mình.protocol = buffer_2.protocol
	mình.checksum = Unsignedinteger16r(Mảngtounsignedinteger16(buffer_2.checksum))

	mình.mãnguồnipaddress = Unsignedinteger32r(Mảngtounsignedinteger32(buffer_2.mãnguồnipaddress))
	mình.destinationipaddress = Unsignedinteger32r(Mảngtounsignedinteger32(buffer_2.destinationipaddress))

}
func (mình *TMạngprotocolv4thôngbáo) Đặtbuffer(buffer_2 *TMạngprotocolv4thôngbáobuffer) {

	buffer_2.lenver = byte(((mình.phiênbản & 0x0F) << 4) | (mình.headerĐộdài & 0x0F))
	buffer_2.tos = mình.tos
	buffer_2.tổngĐộdài = Unsignedinteger16toMảng(mình.tổngĐộdài)

	buffer_2.ident = Unsignedinteger16toMảng(mình.ident)
	buffer_2.cờvàoffset = Unsignedinteger16toMảng(mình.cờvàoffset)

	buffer_2.giờtolive = mình.giờtolive
	buffer_2.protocol = mình.protocol
	buffer_2.checksum = Unsignedinteger16toMảng(mình.checksum)

	buffer_2.mãnguồnipaddress = Unsignedinteger32toMảng(mình.mãnguồnipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toMảng(mình.destinationipaddress)

}

type IMạngprotocolhandler interface {
	Init(backend TBộ_cung_cấp_giao_thức_mạng_liên_kết, pihandler IMạngprotocolhandler, pprotocol uint8)
	Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder uint32, destinationipaddressMạngbyteorder uint32, dataContrỏ uintptr, cỡ uint32) bool
	Gởi(destinationipaddressMạngbyteorder uint32, pprotocol uint8, dataContrỏ uintptr, cỡ uint32)
	Providerget() *TBộ_cung_cấp_giao_thức_mạng_liên_kết
}

type TMạngprotocolhandler struct {
}

var ipethernetframehandler Ipethernetframehandler = Ipethernetframehandler{}
var protocol uint8

func (mình *TMạngprotocolhandler) Init(backend TBộ_cung_cấp_giao_thức_mạng_liên_kết, pihandler IMạngprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (mình *TMạngprotocolhandler) Mạngprotocolreceivewhen(mãnguồnipaddressMạngbyteorder uint32, destinationipaddressMạngbyteorder uint32, dataContrỏ uintptr, cỡ uint32) bool {
	ipconsole.MIn(([]byte)("ipHandler:OnInternet"))
	return false
}
func (mình *TMạngprotocolhandler) Gởi(destinationipaddressMạngbyteorder uint32, pprotocol uint8, dataContrỏ uintptr, cỡ uint32) {

	bộ_cung_cấp_giao_thức_mạng_liên_kết.Gởi(destinationipaddressMạngbyteorder, pprotocol, dataContrỏ, cỡ)
}
func (mình *TMạngprotocolhandler) Providerget() *TBộ_cung_cấp_giao_thức_mạng_liên_kết {
	return &bộ_cung_cấp_giao_thức_mạng_liên_kết
}

type Ipethernetframehandler struct {
	TEthernetframehandler
}

var bộ_cung_cấp_giao_thức_mạng_liên_kết TBộ_cung_cấp_giao_thức_mạng_liên_kết

func (mình *Ipethernetframehandler) Ethernetframereceivewhen(dataContrỏ uintptr, cỡ int) bool {
	ipconsole.MIn(([]byte)("iphandler:onEtherfameRecv\n"))
	return bộ_cung_cấp_giao_thức_mạng_liên_kết.Ethernetframereceivewhen(dataContrỏ, uint32(cỡ))

}

func (mình *Ipethernetframehandler) Gởi(destinationipaddressMạngbyteorder uint64, dataContrỏ uintptr, cỡ uint32) {
	ipconsole.MIn(([]byte)("ipefhandler:send\n"))
	var ethernetKiểube = Unsignedinteger16r(0x0800)
	mình.TEthernetframehandler.FrameGởi(destinationipaddressMạngbyteorder, ethernetKiểube, dataContrỏ, cỡ)

}

var handler_2 [255]IMạngprotocolhandler

type TBộ_cung_cấp_giao_thức_mạng_liên_kết struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetLọc	uint32
}

var efhandler IEthernetframehandler

func (mình *TBộ_cung_cấp_giao_thức_mạng_liên_kết) Init(pefprovider TBộ_cung_cấp_khung_mạng_dùng_chung_môi_trường_truyền, pefhandler IEthernetframehandler, arp Arpprovider, gatewayip uint32, subnetLọc uint32) {

	efhandler = pefhandler
	efhandler.Đặthandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	mình.arpprovider = arp
	mình.Gatewayip = gatewayip
	mình.SubnetLọc = subnetLọc
	bộ_cung_cấp_giao_thức_mạng_liên_kết = *mình
}
func (mình *TBộ_cung_cấp_giao_thức_mạng_liên_kết) Ethernetframereceivewhen(ethernetframepayload uintptr, cỡ uint32) bool {
	if cỡ < uint32(ipCỡ) {
		return false
	}

	var buffer_2 *TMạngprotocolv4thôngbáobuffer = (*TMạngprotocolv4thôngbáobuffer)(Pointer(ethernetframepayload))
	var mạngprotocolthôngbáo TMạngprotocolv4thôngbáo
	mạngprotocolthôngbáo.Init(*buffer_2)

	var reply bool = false

	if mạngprotocolthôngbáo.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var độdài uint32 = uint32(mạngprotocolthôngbáo.tổngĐộdài)
		if độdài > cỡ {
			độdài = cỡ
		}
		if handler_2[mạngprotocolthôngbáo.protocol] != nil {
			reply = handler_2[mạngprotocolthôngbáo.protocol].Mạngprotocolreceivewhen(mạngprotocolthôngbáo.mãnguồnipaddress, mạngprotocolthôngbáo.destinationipaddress, ethernetframepayload+uintptr(4*mạngprotocolthôngbáo.headerĐộdài), uint32(độdài-uint32(4*mạngprotocolthôngbáo.headerĐộdài)))

		}
	}

	if reply {

		var temporary = mạngprotocolthôngbáo.destinationipaddress
		mạngprotocolthôngbáo.destinationipaddress = mạngprotocolthôngbáo.mãnguồnipaddress
		mạngprotocolthôngbáo.mãnguồnipaddress = temporary

		mạngprotocolthôngbáo.giờtolive = 0x40
		mạngprotocolthôngbáo.checksum = 0

		mạngprotocolthôngbáo.Đặtbuffer(buffer_2)
		mạngprotocolthôngbáo.checksum = mình.Checksum((*([4096]uint16))(Pointer(ethernetframepayload)), uint32(4*mạngprotocolthôngbáo.headerĐộdài))

		mạngprotocolthôngbáo.Đặtbuffer(buffer_2)

	}

	ipconsole.MIn(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32In(mạngprotocolthôngbáo.mãnguồnipaddress)
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MUnsignedinteger32In(mạngprotocolthôngbáo.destinationipaddress)
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MUnsignedinteger16In(uint16(mạngprotocolthôngbáo.headerĐộdài))
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MUnsignedinteger16In(uint16(mạngprotocolthôngbáo.phiênbản))
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MUnsignedinteger16In(mạngprotocolthôngbáo.tổngĐộdài)
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MUnsignedinteger32In(uint32(efhandler.Getipaddress()))
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MIn(([]byte)("\n"))

	return reply

}
func (mình *TBộ_cung_cấp_giao_thức_mạng_liên_kết) Gởi(destinationipaddressMạngbyteorder uint32, protocol uint8, dataContrỏ uintptr, cỡ uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TMạngprotocolv4thôngbáobuffer = (*TMạngprotocolv4thôngbáobuffer)(Pointer(&buffer1_2))
	var thôngbáo TMạngprotocolv4thôngbáo = TMạngprotocolv4thôngbáo{}
	thôngbáo.phiênbản = 4
	thôngbáo.headerĐộdài = ipCỡ / 4
	thôngbáo.tos = 0
	thôngbáo.tổngĐộdài = Unsignedinteger16r(uint16(cỡ + uint32(ipCỡ)))

	thôngbáo.ident = 0x0100
	thôngbáo.cờvàoffset = 0x0040
	thôngbáo.giờtolive = 0x40
	thôngbáo.protocol = protocol

	thôngbáo.destinationipaddress = destinationipaddressMạngbyteorder

	thôngbáo.mãnguồnipaddress = uint32(efhandler.Getipaddress())

	thôngbáo.checksum = 0

	thôngbáo.Đặtbuffer(buffer_2)
	thôngbáo.checksum = mình.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipCỡ))
	thôngbáo.Đặtbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataContrỏ))

	for i := 0; i < int(cỡ); i++ {

		buffer1_2[i+int(ipCỡ)] = databuffer_2[i]
	}

	ipconsole.MInxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(cỡ)+int(ipCỡ); i++ {
		ipconsole.MHexadecimalIn(buffer1_2[i])
	}
	ipconsole.MIn(([]byte)(":"))
	ipconsole.MIn(([]byte)("]\n"))

	var kếhopipaddressMạngbyteorder uint32 = destinationipaddressMạngbyteorder
	if (destinationipaddressMạngbyteorder & mình.SubnetLọc) != (thôngbáo.mãnguồnipaddress & mình.SubnetLọc) {
		kếhopipaddressMạngbyteorder = mình.Gatewayip
	}

	var gởidataContrỏ = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32In(kếhopipaddressMạngbyteorder)

	var ethernetKiểube = Unsignedinteger16r(0x0800)
	efhandler.FrameGởi(mình.arpprovider.Resolve(kếhopipaddressMạngbyteorder), ethernetKiểube, gởidataContrỏ, uint32(ipCỡ)+uint32(cỡ))

}
func (mình *TBộ_cung_cấp_giao_thức_mạng_liên_kết) Checksum(pdata *[4096]uint16, độdàiVàoByte uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataByte [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (độdàiVàoByte % 2) != 0 {
		temporary += uint32(uint16(dataByte[độdàiVàoByte-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (mình *TBộ_cung_cấp_giao_thức_mạng_liên_kết) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
