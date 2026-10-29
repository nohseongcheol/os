/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "اترنتچارچوب"
import . "arp"

var ipconsole TConsole = TConsole{}

type Tاینترنتprotocolv4پیغامbuffer struct {
	lenver		byte
	tos		byte
	totalطول	[2]byte

	ident		[2]byte
	flagsandoffset	[2]byte

	زمانtolive	byte
	protocol	byte
	checksum	[2]byte

	مبدأipaddress	[4]byte
	مقصدipaddress	[4]byte
}

var ipاندازه uint8 = (4 + 4 + 4 + 8)

type Tاینترنتprotocolv4پیغام struct {
	headerطول	uint8
	version		uint8
	tos		uint8
	totalطول	uint16

	ident		uint16
	flagsandoffset	uint16

	زمانtolive	uint8
	protocol	uint8
	checksum	uint16

	مبدأipaddress	uint32
	مقصدipaddress	uint32
}

func (خود *Tاینترنتprotocolv4پیغام) Init(buffer_2 Tاینترنتprotocolv4پیغامbuffer) {

	خود.version = ((buffer_2.lenver & 0xF0) >> 4)
	خود.headerطول = buffer_2.lenver & 0x0F
	خود.tos = buffer_2.tos
	خود.totalطول = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.totalطول))

	خود.ident = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.ident))
	خود.flagsandoffset = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.flagsandoffset))

	خود.زمانtolive = buffer_2.زمانtolive
	خود.protocol = buffer_2.protocol
	خود.checksum = Unsignedinteger16r(Aآرایهtounsignedinteger16(buffer_2.checksum))

	خود.مبدأipaddress = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer_2.مبدأipaddress))
	خود.مقصدipaddress = Unsignedinteger32r(Aآرایهtounsignedinteger32(buffer_2.مقصدipaddress))

}
func (خود *Tاینترنتprotocolv4پیغام) Setbuffer(buffer_2 *Tاینترنتprotocolv4پیغامbuffer) {

	buffer_2.lenver = byte(((خود.version & 0x0F) << 4) | (خود.headerطول & 0x0F))
	buffer_2.tos = خود.tos
	buffer_2.totalطول = Unsignedinteger16toآرایه(خود.totalطول)

	buffer_2.ident = Unsignedinteger16toآرایه(خود.ident)
	buffer_2.flagsandoffset = Unsignedinteger16toآرایه(خود.flagsandoffset)

	buffer_2.زمانtolive = خود.زمانtolive
	buffer_2.protocol = خود.protocol
	buffer_2.checksum = Unsignedinteger16toآرایه(خود.checksum)

	buffer_2.مبدأipaddress = Unsignedinteger32toآرایه(خود.مبدأipaddress)
	buffer_2.مقصدipaddress = Unsignedinteger32toآرایه(خود.مقصدipaddress)

}

type Iاینترنتprotocolhandler interface {
	Init(backend Tاینترنتprotocolprovider, pihandler Iاینترنتprotocolhandler, pprotocol uint8)
	Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder uint32, مقصدipaddressشبکهbyteorder uint32, datapointer uintptr, اندازه uint32) bool
	Send(مقصدipaddressشبکهbyteorder uint32, pprotocol uint8, datapointer uintptr, اندازه uint32)
	Providerget() *Tاینترنتprotocolprovider
}

type Tاینترنتprotocolhandler struct {
}

var ipاترنتچارچوبhandler Ipاترنتچارچوبhandler = Ipاترنتچارچوبhandler{}
var protocol uint8

func (خود *Tاینترنتprotocolhandler) Init(backend Tاینترنتprotocolprovider, pihandler Iاینترنتprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (خود *Tاینترنتprotocolhandler) Oاینترنتprotocolreceivewhen(مبدأipaddressشبکهbyteorder uint32, مقصدipaddressشبکهbyteorder uint32, datapointer uintptr, اندازه uint32) bool {
	ipconsole.Mچاپ(([]byte)("ipHandler:OnInternet"))
	return false
}
func (خود *Tاینترنتprotocolhandler) Send(مقصدipaddressشبکهbyteorder uint32, pprotocol uint8, datapointer uintptr, اندازه uint32) {

	ipprovider.Send(مقصدipaddressشبکهbyteorder, pprotocol, datapointer, اندازه)
}
func (خود *Tاینترنتprotocolhandler) Providerget() *Tاینترنتprotocolprovider {
	return &ipprovider
}

type Ipاترنتچارچوبhandler struct {
	Tاترنتچارچوبhandler
}

var ipprovider Tاینترنتprotocolprovider

func (خود *Ipاترنتچارچوبhandler) Oاترنتچارچوبreceivewhen(datapointer uintptr, اندازه int) bool {
	ipconsole.Mچاپ(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Oاترنتچارچوبreceivewhen(datapointer, uint32(اندازه))

}

func (خود *Ipاترنتچارچوبhandler) Send(مقصدipaddressشبکهbyteorder uint64, datapointer uintptr, اندازه uint32) {
	ipconsole.Mچاپ(([]byte)("ipefhandler:send\n"))
	var اترنتنوعbe = Unsignedinteger16r(0x0800)
	خود.Tاترنتچارچوبhandler.Sچارچوبsend(مقصدipaddressشبکهbyteorder, اترنتنوعbe, datapointer, اندازه)

}

var handler_2 [255]Iاینترنتprotocolhandler

type Tاینترنتprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetنقاب	uint32
}

var efhandler Iاترنتچارچوبhandler

func (خود *Tاینترنتprotocolprovider) Init(pefprovider Tاترنتچارچوبprovider, pefhandler Iاترنتچارچوبhandler, arp Arpprovider, gatewayip uint32, subnetنقاب uint32) {

	efhandler = pefhandler
	efhandler.Sethandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	خود.arpprovider = arp
	خود.Gatewayip = gatewayip
	خود.Subnetنقاب = subnetنقاب
	ipprovider = *خود
}
func (خود *Tاینترنتprotocolprovider) Oاترنتچارچوبreceivewhen(اترنتچارچوبpayload uintptr, اندازه uint32) bool {
	if اندازه < uint32(ipاندازه) {
		return false
	}

	var buffer_2 *Tاینترنتprotocolv4پیغامbuffer = (*Tاینترنتprotocolv4پیغامbuffer)(Pointer(اترنتچارچوبpayload))
	var اینترنتprotocolپیغام Tاینترنتprotocolv4پیغام
	اینترنتprotocolپیغام.Init(*buffer_2)

	var reply bool = false

	if اینترنتprotocolپیغام.مقصدipaddress == uint32(efhandler.Getipaddress()) {

		var طول uint32 = uint32(اینترنتprotocolپیغام.totalطول)
		if طول > اندازه {
			طول = اندازه
		}
		if handler_2[اینترنتprotocolپیغام.protocol] != nil {
			reply = handler_2[اینترنتprotocolپیغام.protocol].Oاینترنتprotocolreceivewhen(اینترنتprotocolپیغام.مبدأipaddress, اینترنتprotocolپیغام.مقصدipaddress, اترنتچارچوبpayload+uintptr(4*اینترنتprotocolپیغام.headerطول), uint32(طول-uint32(4*اینترنتprotocolپیغام.headerطول)))

		}
	}

	if reply {

		var temporary = اینترنتprotocolپیغام.مقصدipaddress
		اینترنتprotocolپیغام.مقصدipaddress = اینترنتprotocolپیغام.مبدأipaddress
		اینترنتprotocolپیغام.مبدأipaddress = temporary

		اینترنتprotocolپیغام.زمانtolive = 0x40
		اینترنتprotocolپیغام.checksum = 0

		اینترنتprotocolپیغام.Setbuffer(buffer_2)
		اینترنتprotocolپیغام.checksum = خود.Checksum((*([4096]uint16))(Pointer(اترنتچارچوبpayload)), uint32(4*اینترنتprotocolپیغام.headerطول))

		اینترنتprotocolپیغام.Setbuffer(buffer_2)

	}

	ipconsole.Mچاپ(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32چاپ(اینترنتprotocolپیغام.مبدأipaddress)
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.MUnsignedinteger32چاپ(اینترنتprotocolپیغام.مقصدipaddress)
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.MUnsignedinteger16چاپ(uint16(اینترنتprotocolپیغام.headerطول))
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.MUnsignedinteger16چاپ(uint16(اینترنتprotocolپیغام.version))
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.MUnsignedinteger16چاپ(اینترنتprotocolپیغام.totalطول)
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.MUnsignedinteger32چاپ(uint32(efhandler.Getipaddress()))
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.Mچاپ(([]byte)("\n"))

	return reply

}
func (خود *Tاینترنتprotocolprovider) Send(مقصدipaddressشبکهbyteorder uint32, protocol uint8, datapointer uintptr, اندازه uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tاینترنتprotocolv4پیغامbuffer = (*Tاینترنتprotocolv4پیغامbuffer)(Pointer(&buffer1_2))
	var پیغام Tاینترنتprotocolv4پیغام = Tاینترنتprotocolv4پیغام{}
	پیغام.version = 4
	پیغام.headerطول = ipاندازه / 4
	پیغام.tos = 0
	پیغام.totalطول = Unsignedinteger16r(uint16(اندازه + uint32(ipاندازه)))

	پیغام.ident = 0x0100
	پیغام.flagsandoffset = 0x0040
	پیغام.زمانtolive = 0x40
	پیغام.protocol = protocol

	پیغام.مقصدipaddress = مقصدipaddressشبکهbyteorder

	پیغام.مبدأipaddress = uint32(efhandler.Getipaddress())

	پیغام.checksum = 0

	پیغام.Setbuffer(buffer_2)
	پیغام.checksum = خود.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipاندازه))
	پیغام.Setbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(datapointer))

	for i := 0; i < int(اندازه); i++ {

		buffer1_2[i+int(ipاندازه)] = databuffer_2[i]
	}

	ipconsole.Mچاپxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(اندازه)+int(ipاندازه); i++ {
		ipconsole.MHexadecimalچاپ(buffer1_2[i])
	}
	ipconsole.Mچاپ(([]byte)(":"))
	ipconsole.Mچاپ(([]byte)("]\n"))

	var بعدیhopipaddressشبکهbyteorder uint32 = مقصدipaddressشبکهbyteorder
	if (مقصدipaddressشبکهbyteorder & خود.Subnetنقاب) != (پیغام.مبدأipaddress & خود.Subnetنقاب) {
		بعدیhopipaddressشبکهbyteorder = خود.Gatewayip
	}

	var senddatapointer = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32چاپ(بعدیhopipaddressشبکهbyteorder)

	var اترنتنوعbe = Unsignedinteger16r(0x0800)
	efhandler.Sچارچوبsend(خود.arpprovider.Resolve(بعدیhopipaddressشبکهbyteorder), اترنتنوعbe, senddatapointer, uint32(ipاندازه)+uint32(اندازه))

}
func (خود *Tاینترنتprotocolprovider) Checksum(pdata *[4096]uint16, طولداخلبایت uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataبایت [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (طولداخلبایت % 2) != 0 {
		temporary += uint32(uint16(dataبایت[طولداخلبایت-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (خود *Tاینترنتprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
