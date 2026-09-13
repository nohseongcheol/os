package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "лякальнаясеткаФрэйм"
import . "arp"

var ipconsole TConsole = TConsole{}

type TІнтэрнэтprotocolv4паведамленнеbuffer struct {
	lenver		byte
	tos		byte
	агуламДаўжыня	[2]byte

	ident		[2]byte
	сцяжкіandoffset	[2]byte

	часtolive	byte
	protocol	byte
	checksum	[2]byte

	крыніцаipaddress	[4]byte
	destinationipaddress	[4]byte
}

var ipПамер uint8 = (4 + 4 + 4 + 8)

type TІнтэрнэтprotocolv4паведамленне struct {
	headerДаўжыня	uint8
	version		uint8
	tos		uint8
	агуламДаўжыня	uint16

	ident		uint16
	сцяжкіandoffset	uint16

	часtolive	uint8
	protocol	uint8
	checksum	uint16

	крыніцаipaddress	uint32
	destinationipaddress	uint32
}

func (self *TІнтэрнэтprotocolv4паведамленне) Init(buffer_2 TІнтэрнэтprotocolv4паведамленнеbuffer) {

	self.version = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerДаўжыня = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.агуламДаўжыня = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.агуламДаўжыня))

	self.ident = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.ident))
	self.сцяжкіandoffset = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.сцяжкіandoffset))

	self.часtolive = buffer_2.часtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.checksum))

	self.крыніцаipaddress = Unsignedinteger32r(Масіўtounsignedinteger32(buffer_2.крыніцаipaddress))
	self.destinationipaddress = Unsignedinteger32r(Масіўtounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *TІнтэрнэтprotocolv4паведамленне) Вызначанаbuffer(buffer_2 *TІнтэрнэтprotocolv4паведамленнеbuffer) {

	buffer_2.lenver = byte(((self.version & 0x0F) << 4) | (self.headerДаўжыня & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.агуламДаўжыня = Unsignedinteger16toМасіў(self.агуламДаўжыня)

	buffer_2.ident = Unsignedinteger16toМасіў(self.ident)
	buffer_2.сцяжкіandoffset = Unsignedinteger16toМасіў(self.сцяжкіandoffset)

	buffer_2.часtolive = self.часtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toМасіў(self.checksum)

	buffer_2.крыніцаipaddress = Unsignedinteger32toМасіў(self.крыніцаipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toМасіў(self.destinationipaddress)

}

type IІнтэрнэтprotocolhandler interface {
	Init(backend TІнтэрнэтprotocolprovider, pihandler IІнтэрнэтprotocolhandler, pprotocol uint8)
	Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder uint32, destinationipaddressСеткаbyteorder uint32, dataПаказальнік uintptr, памер uint32) bool
	Даслаць(destinationipaddressСеткаbyteorder uint32, pprotocol uint8, dataПаказальнік uintptr, памер uint32)
	Providerget() *TІнтэрнэтprotocolprovider
}

type TІнтэрнэтprotocolhandler struct {
}

var ipЛякальнаясеткаФрэймhandler IpЛякальнаясеткаФрэймhandler = IpЛякальнаясеткаФрэймhandler{}
var protocol uint8

func (self *TІнтэрнэтprotocolhandler) Init(backend TІнтэрнэтprotocolprovider, pihandler IІнтэрнэтprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *TІнтэрнэтprotocolhandler) Інтэрнэтprotocolreceivewhen(крыніцаipaddressСеткаbyteorder uint32, destinationipaddressСеткаbyteorder uint32, dataПаказальнік uintptr, памер uint32) bool {
	ipconsole.MДрукаваць(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *TІнтэрнэтprotocolhandler) Даслаць(destinationipaddressСеткаbyteorder uint32, pprotocol uint8, dataПаказальнік uintptr, памер uint32) {

	ipprovider.Даслаць(destinationipaddressСеткаbyteorder, pprotocol, dataПаказальнік, памер)
}
func (self *TІнтэрнэтprotocolhandler) Providerget() *TІнтэрнэтprotocolprovider {
	return &ipprovider
}

type IpЛякальнаясеткаФрэймhandler struct {
	TЛякальнаясеткаФрэймhandler
}

var ipprovider TІнтэрнэтprotocolprovider

func (self *IpЛякальнаясеткаФрэймhandler) ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік uintptr, памер int) bool {
	ipconsole.MДрукаваць(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік, uint32(памер))

}

func (self *IpЛякальнаясеткаФрэймhandler) Даслаць(destinationipaddressСеткаbyteorder uint64, dataПаказальнік uintptr, памер uint32) {
	ipconsole.MДрукаваць(([]byte)("ipefhandler:send\n"))
	var лякальнаясеткаТыпbe = Unsignedinteger16r(0x0800)
	self.TЛякальнаясеткаФрэймhandler.ФрэймДаслаць(destinationipaddressСеткаbyteorder, лякальнаясеткаТыпbe, dataПаказальнік, памер)

}

var handler_2 [255]IІнтэрнэтprotocolhandler

type TІнтэрнэтprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IЛякальнаясеткаФрэймhandler

func (self *TІнтэрнэтprotocolprovider) Init(pefprovider TЛякальнаясеткаФрэймprovider, pefhandler IЛякальнаясеткаФрэймhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Вызначанаhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.SubnetМаска = subnetМаска
	ipprovider = *self
}
func (self *TІнтэрнэтprotocolprovider) ЛякальнаясеткаФрэймreceivewhen(лякальнаясеткаФрэймpayload uintptr, памер uint32) bool {
	if памер < uint32(ipПамер) {
		return false
	}

	var buffer_2 *TІнтэрнэтprotocolv4паведамленнеbuffer = (*TІнтэрнэтprotocolv4паведамленнеbuffer)(Pointer(лякальнаясеткаФрэймpayload))
	var інтэрнэтprotocolпаведамленне TІнтэрнэтprotocolv4паведамленне
	інтэрнэтprotocolпаведамленне.Init(*buffer_2)

	var reply bool = false

	if інтэрнэтprotocolпаведамленне.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var даўжыня uint32 = uint32(інтэрнэтprotocolпаведамленне.агуламДаўжыня)
		if даўжыня > памер {
			даўжыня = памер
		}
		if handler_2[інтэрнэтprotocolпаведамленне.protocol] != nil {
			reply = handler_2[інтэрнэтprotocolпаведамленне.protocol].Інтэрнэтprotocolreceivewhen(інтэрнэтprotocolпаведамленне.крыніцаipaddress, інтэрнэтprotocolпаведамленне.destinationipaddress, лякальнаясеткаФрэймpayload+uintptr(4*інтэрнэтprotocolпаведамленне.headerДаўжыня), uint32(даўжыня-uint32(4*інтэрнэтprotocolпаведамленне.headerДаўжыня)))

		}
	}

	if reply {

		var temporary = інтэрнэтprotocolпаведамленне.destinationipaddress
		інтэрнэтprotocolпаведамленне.destinationipaddress = інтэрнэтprotocolпаведамленне.крыніцаipaddress
		інтэрнэтprotocolпаведамленне.крыніцаipaddress = temporary

		інтэрнэтprotocolпаведамленне.часtolive = 0x40
		інтэрнэтprotocolпаведамленне.checksum = 0

		інтэрнэтprotocolпаведамленне.Вызначанаbuffer(buffer_2)
		інтэрнэтprotocolпаведамленне.checksum = self.Checksum((*([4096]uint16))(Pointer(лякальнаясеткаФрэймpayload)), uint32(4*інтэрнэтprotocolпаведамленне.headerДаўжыня))

		інтэрнэтprotocolпаведамленне.Вызначанаbuffer(buffer_2)

	}

	ipconsole.MДрукаваць(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Друкаваць(інтэрнэтprotocolпаведамленне.крыніцаipaddress)
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MUnsignedinteger32Друкаваць(інтэрнэтprotocolпаведамленне.destinationipaddress)
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MUnsignedinteger16Друкаваць(uint16(інтэрнэтprotocolпаведамленне.headerДаўжыня))
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MUnsignedinteger16Друкаваць(uint16(інтэрнэтprotocolпаведамленне.version))
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MUnsignedinteger16Друкаваць(інтэрнэтprotocolпаведамленне.агуламДаўжыня)
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MUnsignedinteger32Друкаваць(uint32(efhandler.Getipaddress()))
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MДрукаваць(([]byte)("\n"))

	return reply

}
func (self *TІнтэрнэтprotocolprovider) Даслаць(destinationipaddressСеткаbyteorder uint32, protocol uint8, dataПаказальнік uintptr, памер uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TІнтэрнэтprotocolv4паведамленнеbuffer = (*TІнтэрнэтprotocolv4паведамленнеbuffer)(Pointer(&buffer1_2))
	var паведамленне TІнтэрнэтprotocolv4паведамленне = TІнтэрнэтprotocolv4паведамленне{}
	паведамленне.version = 4
	паведамленне.headerДаўжыня = ipПамер / 4
	паведамленне.tos = 0
	паведамленне.агуламДаўжыня = Unsignedinteger16r(uint16(памер + uint32(ipПамер)))

	паведамленне.ident = 0x0100
	паведамленне.сцяжкіandoffset = 0x0040
	паведамленне.часtolive = 0x40
	паведамленне.protocol = protocol

	паведамленне.destinationipaddress = destinationipaddressСеткаbyteorder

	паведамленне.крыніцаipaddress = uint32(efhandler.Getipaddress())

	паведамленне.checksum = 0

	паведамленне.Вызначанаbuffer(buffer_2)
	паведамленне.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipПамер))
	паведамленне.Вызначанаbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataПаказальнік))

	for i := 0; i < int(памер); i++ {

		buffer1_2[i+int(ipПамер)] = databuffer_2[i]
	}

	ipconsole.MДрукавацьxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(памер)+int(ipПамер); i++ {
		ipconsole.MHexadecimalДрукаваць(buffer1_2[i])
	}
	ipconsole.MДрукаваць(([]byte)(":"))
	ipconsole.MДрукаваць(([]byte)("]\n"))

	var наступныhopipaddressСеткаbyteorder uint32 = destinationipaddressСеткаbyteorder
	if (destinationipaddressСеткаbyteorder & self.SubnetМаска) != (паведамленне.крыніцаipaddress & self.SubnetМаска) {
		наступныhopipaddressСеткаbyteorder = self.Gatewayip
	}

	var даслацьdataПаказальнік = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Друкаваць(наступныhopipaddressСеткаbyteorder)

	var лякальнаясеткаТыпbe = Unsignedinteger16r(0x0800)
	efhandler.ФрэймДаслаць(self.arpprovider.Resolve(наступныhopipaddressСеткаbyteorder), лякальнаясеткаТыпbe, даслацьdataПаказальнік, uint32(ipПамер)+uint32(памер))

}
func (self *TІнтэрнэтprotocolprovider) Checksum(pdata *[4096]uint16, даўжыняуБайтаў uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБайтаў [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (даўжыняуБайтаў % 2) != 0 {
		temporary += uint32(uint16(dataБайтаў[даўжыняуБайтаў-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *TІнтэрнэтprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
