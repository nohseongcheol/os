package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "локалнамрежаEthernetРамка"
import . "arp"

var ipconsole TConsole = TConsole{}

type TИнтернетprotocolv4СЪОБЩЕНИЕbuffer struct {
	lenver		byte
	tos		byte
	общодължина	[2]byte

	ident			[2]byte
	флаговеandoffset	[2]byte

	времеtolive	byte
	protocol	byte
	checksum	[2]byte

	източникipaddress	[4]byte
	назначениеipaddress	[4]byte
}

var ipРазмер uint8 = (4 + 4 + 4 + 8)

type TИнтернетprotocolv4СЪОБЩЕНИЕ struct {
	headerдължина	uint8
	версия		uint8
	tos		uint8
	общодължина	uint16

	ident			uint16
	флаговеandoffset	uint16

	времеtolive	uint8
	protocol	uint8
	checksum	uint16

	източникipaddress	uint32
	назначениеipaddress	uint32
}

func (себеси *TИнтернетprotocolv4СЪОБЩЕНИЕ) Init(buffer_2 TИнтернетprotocolv4СЪОБЩЕНИЕbuffer) {

	себеси.версия = ((buffer_2.lenver & 0xF0) >> 4)
	себеси.headerдължина = buffer_2.lenver & 0x0F
	себеси.tos = buffer_2.tos
	себеси.общодължина = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.общодължина))

	себеси.ident = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.ident))
	себеси.флаговеandoffset = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.флаговеandoffset))

	себеси.времеtolive = buffer_2.времеtolive
	себеси.protocol = buffer_2.protocol
	себеси.checksum = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.checksum))

	себеси.източникipaddress = Unsignedinteger32r(Масивtounsignedinteger32(buffer_2.източникipaddress))
	себеси.назначениеipaddress = Unsignedinteger32r(Масивtounsignedinteger32(buffer_2.назначениеipaddress))

}
func (себеси *TИнтернетprotocolv4СЪОБЩЕНИЕ) Задайbuffer(buffer_2 *TИнтернетprotocolv4СЪОБЩЕНИЕbuffer) {

	buffer_2.lenver = byte(((себеси.версия & 0x0F) << 4) | (себеси.headerдължина & 0x0F))
	buffer_2.tos = себеси.tos
	buffer_2.общодължина = Unsignedinteger16toМасив(себеси.общодължина)

	buffer_2.ident = Unsignedinteger16toМасив(себеси.ident)
	buffer_2.флаговеandoffset = Unsignedinteger16toМасив(себеси.флаговеandoffset)

	buffer_2.времеtolive = себеси.времеtolive
	buffer_2.protocol = себеси.protocol
	buffer_2.checksum = Unsignedinteger16toМасив(себеси.checksum)

	buffer_2.източникipaddress = Unsignedinteger32toМасив(себеси.източникipaddress)
	buffer_2.назначениеipaddress = Unsignedinteger32toМасив(себеси.назначениеipaddress)

}

type IИнтернетprotocolhandler interface {
	Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8)
	Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder uint32, назначениеipaddressМрежаbyteorder uint32, dataПоказалци uintptr, размер uint32) bool
	Изпращане(назначениеipaddressМрежаbyteorder uint32, pprotocol uint8, dataПоказалци uintptr, размер uint32)
	Providerget() *TИнтернетprotocolprovider
}

type TИнтернетprotocolhandler struct {
}

var ipЛокалнамрежаEthernetРамкаhandler IpЛокалнамрежаEthernetРамкаhandler = IpЛокалнамрежаEthernetРамкаhandler{}
var protocol uint8

func (себеси *TИнтернетprotocolhandler) Init(backend TИнтернетprotocolprovider, pihandler IИнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (себеси *TИнтернетprotocolhandler) Интернетprotocolreceivewhen(източникipaddressМрежаbyteorder uint32, назначениеipaddressМрежаbyteorder uint32, dataПоказалци uintptr, размер uint32) bool {
	ipconsole.MПечат(([]byte)("ipHandler:OnInternet"))
	return false
}
func (себеси *TИнтернетprotocolhandler) Изпращане(назначениеipaddressМрежаbyteorder uint32, pprotocol uint8, dataПоказалци uintptr, размер uint32) {

	ipprovider.Изпращане(назначениеipaddressМрежаbyteorder, pprotocol, dataПоказалци, размер)
}
func (себеси *TИнтернетprotocolhandler) Providerget() *TИнтернетprotocolprovider {
	return &ipprovider
}

type IpЛокалнамрежаEthernetРамкаhandler struct {
	TЛокалнамрежаEthernetРамкаhandler
}

var ipprovider TИнтернетprotocolprovider

func (себеси *IpЛокалнамрежаEthernetРамкаhandler) ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци uintptr, размер int) bool {
	ipconsole.MПечат(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци, uint32(размер))

}

func (себеси *IpЛокалнамрежаEthernetРамкаhandler) Изпращане(назначениеipaddressМрежаbyteorder uint64, dataПоказалци uintptr, размер uint32) {
	ipconsole.MПечат(([]byte)("ipefhandler:send\n"))
	var локалнамрежаEthernetТипbe = Unsignedinteger16r(0x0800)
	себеси.TЛокалнамрежаEthernetРамкаhandler.РамкаИзпращане(назначениеipaddressМрежаbyteorder, локалнамрежаEthernetТипbe, dataПоказалци, размер)

}

var handler_2 [255]IИнтернетprotocolhandler

type TИнтернетprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IЛокалнамрежаEthernetРамкаhandler

func (себеси *TИнтернетprotocolprovider) Init(pefprovider TЛокалнамрежаEthernetРамкаprovider, pefhandler IЛокалнамрежаEthernetРамкаhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Задайhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	себеси.arpprovider = arp
	себеси.Gatewayip = gatewayip
	себеси.SubnetМаска = subnetМаска
	ipprovider = *себеси
}
func (себеси *TИнтернетprotocolprovider) ЛокалнамрежаEthernetРамкаreceivewhen(локалнамрежаEthernetРамкаpayload uintptr, размер uint32) bool {
	if размер < uint32(ipРазмер) {
		return false
	}

	var buffer_2 *TИнтернетprotocolv4СЪОБЩЕНИЕbuffer = (*TИнтернетprotocolv4СЪОБЩЕНИЕbuffer)(Pointer(локалнамрежаEthernetРамкаpayload))
	var интернетprotocolСЪОБЩЕНИЕ TИнтернетprotocolv4СЪОБЩЕНИЕ
	интернетprotocolСЪОБЩЕНИЕ.Init(*buffer_2)

	var reply bool = false

	if интернетprotocolСЪОБЩЕНИЕ.назначениеipaddress == uint32(efhandler.Getipaddress()) {

		var дължина uint32 = uint32(интернетprotocolСЪОБЩЕНИЕ.общодължина)
		if дължина > размер {
			дължина = размер
		}
		if handler_2[интернетprotocolСЪОБЩЕНИЕ.protocol] != nil {
			reply = handler_2[интернетprotocolСЪОБЩЕНИЕ.protocol].Интернетprotocolreceivewhen(интернетprotocolСЪОБЩЕНИЕ.източникipaddress, интернетprotocolСЪОБЩЕНИЕ.назначениеipaddress, локалнамрежаEthernetРамкаpayload+uintptr(4*интернетprotocolСЪОБЩЕНИЕ.headerдължина), uint32(дължина-uint32(4*интернетprotocolСЪОБЩЕНИЕ.headerдължина)))

		}
	}

	if reply {

		var temporary = интернетprotocolСЪОБЩЕНИЕ.назначениеipaddress
		интернетprotocolСЪОБЩЕНИЕ.назначениеipaddress = интернетprotocolСЪОБЩЕНИЕ.източникipaddress
		интернетprotocolСЪОБЩЕНИЕ.източникipaddress = temporary

		интернетprotocolСЪОБЩЕНИЕ.времеtolive = 0x40
		интернетprotocolСЪОБЩЕНИЕ.checksum = 0

		интернетprotocolСЪОБЩЕНИЕ.Задайbuffer(buffer_2)
		интернетprotocolСЪОБЩЕНИЕ.checksum = себеси.Checksum((*([4096]uint16))(Pointer(локалнамрежаEthernetРамкаpayload)), uint32(4*интернетprotocolСЪОБЩЕНИЕ.headerдължина))

		интернетprotocolСЪОБЩЕНИЕ.Задайbuffer(buffer_2)

	}

	ipconsole.MПечат(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Печат(интернетprotocolСЪОБЩЕНИЕ.източникipaddress)
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MUnsignedinteger32Печат(интернетprotocolСЪОБЩЕНИЕ.назначениеipaddress)
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печат(uint16(интернетprotocolСЪОБЩЕНИЕ.headerдължина))
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печат(uint16(интернетprotocolСЪОБЩЕНИЕ.версия))
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MUnsignedinteger16Печат(интернетprotocolСЪОБЩЕНИЕ.общодължина)
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MUnsignedinteger32Печат(uint32(efhandler.Getipaddress()))
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MПечат(([]byte)("\n"))

	return reply

}
func (себеси *TИнтернетprotocolprovider) Изпращане(назначениеipaddressМрежаbyteorder uint32, protocol uint8, dataПоказалци uintptr, размер uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TИнтернетprotocolv4СЪОБЩЕНИЕbuffer = (*TИнтернетprotocolv4СЪОБЩЕНИЕbuffer)(Pointer(&buffer1_2))
	var сЪОБЩЕНИЕ TИнтернетprotocolv4СЪОБЩЕНИЕ = TИнтернетprotocolv4СЪОБЩЕНИЕ{}
	сЪОБЩЕНИЕ.версия = 4
	сЪОБЩЕНИЕ.headerдължина = ipРазмер / 4
	сЪОБЩЕНИЕ.tos = 0
	сЪОБЩЕНИЕ.общодължина = Unsignedinteger16r(uint16(размер + uint32(ipРазмер)))

	сЪОБЩЕНИЕ.ident = 0x0100
	сЪОБЩЕНИЕ.флаговеandoffset = 0x0040
	сЪОБЩЕНИЕ.времеtolive = 0x40
	сЪОБЩЕНИЕ.protocol = protocol

	сЪОБЩЕНИЕ.назначениеipaddress = назначениеipaddressМрежаbyteorder

	сЪОБЩЕНИЕ.източникipaddress = uint32(efhandler.Getipaddress())

	сЪОБЩЕНИЕ.checksum = 0

	сЪОБЩЕНИЕ.Задайbuffer(buffer_2)
	сЪОБЩЕНИЕ.checksum = себеси.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipРазмер))
	сЪОБЩЕНИЕ.Задайbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataПоказалци))

	for i := 0; i < int(размер); i++ {

		buffer1_2[i+int(ipРазмер)] = databuffer_2[i]
	}

	ipconsole.MПечатxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(размер)+int(ipРазмер); i++ {
		ipconsole.MHexadecimalПечат(buffer1_2[i])
	}
	ipconsole.MПечат(([]byte)(":"))
	ipconsole.MПечат(([]byte)("]\n"))

	var следващоhopipaddressМрежаbyteorder uint32 = назначениеipaddressМрежаbyteorder
	if (назначениеipaddressМрежаbyteorder & себеси.SubnetМаска) != (сЪОБЩЕНИЕ.източникipaddress & себеси.SubnetМаска) {
		следващоhopipaddressМрежаbyteorder = себеси.Gatewayip
	}

	var изпращанеdataПоказалци = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Печат(следващоhopipaddressМрежаbyteorder)

	var локалнамрежаEthernetТипbe = Unsignedinteger16r(0x0800)
	efhandler.РамкаИзпращане(себеси.arpprovider.Resolve(следващоhopipaddressМрежаbyteorder), локалнамрежаEthernetТипbe, изпращанеdataПоказалци, uint32(ipРазмер)+uint32(размер))

}
func (себеси *TИнтернетprotocolprovider) Checksum(pdata *[4096]uint16, дължинаВходящБайтове uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБайтове [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (дължинаВходящБайтове % 2) != 0 {
		temporary += uint32(uint16(dataБайтове[дължинаВходящБайтове-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (себеси *TИнтернетprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
