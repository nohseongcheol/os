package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "אתרנטframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type Tאינטרנטprotocolv4הודעהbuffer struct {
	lenver		byte
	tos		byte
	totalאורך	[2]byte

	ident		[2]byte
	דגליםandoffset	[2]byte

	זמןtolive	byte
	protocol	byte
	checksum	[2]byte

	מקורipaddress	[4]byte
	יעדipaddress	[4]byte
}

var ipגודל uint8 = (4 + 4 + 4 + 8)

type Tאינטרנטprotocolv4הודעה struct {
	headerאורך	uint8
	גרסה		uint8
	tos		uint8
	totalאורך	uint16

	ident		uint16
	דגליםandoffset	uint16

	זמןtolive	uint8
	protocol	uint8
	checksum	uint16

	מקורipaddress	uint32
	יעדipaddress	uint32
}

func (self *Tאינטרנטprotocolv4הודעה) Init(buffer_2 Tאינטרנטprotocolv4הודעהbuffer) {

	self.גרסה = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerאורך = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.totalאורך = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.totalאורך))

	self.ident = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.ident))
	self.דגליםandoffset = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.דגליםandoffset))

	self.זמןtolive = buffer_2.זמןtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.checksum))

	self.מקורipaddress = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer_2.מקורipaddress))
	self.יעדipaddress = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer_2.יעדipaddress))

}
func (self *Tאינטרנטprotocolv4הודעה) Sקבעbuffer(buffer_2 *Tאינטרנטprotocolv4הודעהbuffer) {

	buffer_2.lenver = byte(((self.גרסה & 0x0F) << 4) | (self.headerאורך & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.totalאורך = Unsignedinteger16toמערך(self.totalאורך)

	buffer_2.ident = Unsignedinteger16toמערך(self.ident)
	buffer_2.דגליםandoffset = Unsignedinteger16toמערך(self.דגליםandoffset)

	buffer_2.זמןtolive = self.זמןtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toמערך(self.checksum)

	buffer_2.מקורipaddress = Unsignedinteger32toמערך(self.מקורipaddress)
	buffer_2.יעדipaddress = Unsignedinteger32toמערך(self.יעדipaddress)

}

type Iאינטרנטprotocolhandler interface {
	Init(backend Tאינטרנטprotocolprovider, pihandler Iאינטרנטprotocolhandler, pprotocol uint8)
	Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder uint32, יעדipaddressרשתbyteorder uint32, dataסמן uintptr, גודל uint32) bool
	Sשלח(יעדipaddressרשתbyteorder uint32, pprotocol uint8, dataסמן uintptr, גודל uint32)
	Providerget() *Tאינטרנטprotocolprovider
}

type Tאינטרנטprotocolhandler struct {
}

var ipאתרנטframehandler Ipאתרנטframehandler = Ipאתרנטframehandler{}
var protocol uint8

func (self *Tאינטרנטprotocolhandler) Init(backend Tאינטרנטprotocolprovider, pihandler Iאינטרנטprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tאינטרנטprotocolhandler) Oאינטרנטprotocolreceivewhen(מקורipaddressרשתbyteorder uint32, יעדipaddressרשתbyteorder uint32, dataסמן uintptr, גודל uint32) bool {
	ipconsole.Mהדפסה(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tאינטרנטprotocolhandler) Sשלח(יעדipaddressרשתbyteorder uint32, pprotocol uint8, dataסמן uintptr, גודל uint32) {

	ipprovider.Sשלח(יעדipaddressרשתbyteorder, pprotocol, dataסמן, גודל)
}
func (self *Tאינטרנטprotocolhandler) Providerget() *Tאינטרנטprotocolprovider {
	return &ipprovider
}

type Ipאתרנטframehandler struct {
	Tאתרנטframehandler
}

var ipprovider Tאינטרנטprotocolprovider

func (self *Ipאתרנטframehandler) Oאתרנטframereceivewhen(dataסמן uintptr, גודל int) bool {
	ipconsole.Mהדפסה(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Oאתרנטframereceivewhen(dataסמן, uint32(גודל))

}

func (self *Ipאתרנטframehandler) Sשלח(יעדipaddressרשתbyteorder uint64, dataסמן uintptr, גודל uint32) {
	ipconsole.Mהדפסה(([]byte)("ipefhandler:send\n"))
	var אתרנטסוגbe = Unsignedinteger16r(0x0800)
	self.Tאתרנטframehandler.Frameשלח(יעדipaddressרשתbyteorder, אתרנטסוגbe, dataסמן, גודל)

}

var handler_2 [255]Iאינטרנטprotocolhandler

type Tאינטרנטprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetסינון	uint32
}

var efhandler Iאתרנטframehandler

func (self *Tאינטרנטprotocolprovider) Init(pefprovider Tאתרנטframeprovider, pefhandler Iאתרנטframehandler, arp Arpprovider, gatewayip uint32, subnetסינון uint32) {

	efhandler = pefhandler
	efhandler.Sקבעhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetסינון = subnetסינון
	ipprovider = *self
}
func (self *Tאינטרנטprotocolprovider) Oאתרנטframereceivewhen(אתרנטframepayload uintptr, גודל uint32) bool {
	if גודל < uint32(ipגודל) {
		return false
	}

	var buffer_2 *Tאינטרנטprotocolv4הודעהbuffer = (*Tאינטרנטprotocolv4הודעהbuffer)(Pointer(אתרנטframepayload))
	var אינטרנטprotocolהודעה Tאינטרנטprotocolv4הודעה
	אינטרנטprotocolהודעה.Init(*buffer_2)

	var reply bool = false

	if אינטרנטprotocolהודעה.יעדipaddress == uint32(efhandler.Getipaddress()) {

		var אורך uint32 = uint32(אינטרנטprotocolהודעה.totalאורך)
		if אורך > גודל {
			אורך = גודל
		}
		if handler_2[אינטרנטprotocolהודעה.protocol] != nil {
			reply = handler_2[אינטרנטprotocolהודעה.protocol].Oאינטרנטprotocolreceivewhen(אינטרנטprotocolהודעה.מקורipaddress, אינטרנטprotocolהודעה.יעדipaddress, אתרנטframepayload+uintptr(4*אינטרנטprotocolהודעה.headerאורך), uint32(אורך-uint32(4*אינטרנטprotocolהודעה.headerאורך)))

		}
	}

	if reply {

		var temporary = אינטרנטprotocolהודעה.יעדipaddress
		אינטרנטprotocolהודעה.יעדipaddress = אינטרנטprotocolהודעה.מקורipaddress
		אינטרנטprotocolהודעה.מקורipaddress = temporary

		אינטרנטprotocolהודעה.זמןtolive = 0x40
		אינטרנטprotocolהודעה.checksum = 0

		אינטרנטprotocolהודעה.Sקבעbuffer(buffer_2)
		אינטרנטprotocolהודעה.checksum = self.Checksum((*([4096]uint16))(Pointer(אתרנטframepayload)), uint32(4*אינטרנטprotocolהודעה.headerאורך))

		אינטרנטprotocolהודעה.Sקבעbuffer(buffer_2)

	}

	ipconsole.Mהדפסה(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32הדפסה(אינטרנטprotocolהודעה.מקורipaddress)
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.MUnsignedinteger32הדפסה(אינטרנטprotocolהודעה.יעדipaddress)
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.MUnsignedinteger16הדפסה(uint16(אינטרנטprotocolהודעה.headerאורך))
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.MUnsignedinteger16הדפסה(uint16(אינטרנטprotocolהודעה.גרסה))
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.MUnsignedinteger16הדפסה(אינטרנטprotocolהודעה.totalאורך)
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.MUnsignedinteger32הדפסה(uint32(efhandler.Getipaddress()))
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.Mהדפסה(([]byte)("\n"))

	return reply

}
func (self *Tאינטרנטprotocolprovider) Sשלח(יעדipaddressרשתbyteorder uint32, protocol uint8, dataסמן uintptr, גודל uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tאינטרנטprotocolv4הודעהbuffer = (*Tאינטרנטprotocolv4הודעהbuffer)(Pointer(&buffer1_2))
	var הודעה Tאינטרנטprotocolv4הודעה = Tאינטרנטprotocolv4הודעה{}
	הודעה.גרסה = 4
	הודעה.headerאורך = ipגודל / 4
	הודעה.tos = 0
	הודעה.totalאורך = Unsignedinteger16r(uint16(גודל + uint32(ipגודל)))

	הודעה.ident = 0x0100
	הודעה.דגליםandoffset = 0x0040
	הודעה.זמןtolive = 0x40
	הודעה.protocol = protocol

	הודעה.יעדipaddress = יעדipaddressרשתbyteorder

	הודעה.מקורipaddress = uint32(efhandler.Getipaddress())

	הודעה.checksum = 0

	הודעה.Sקבעbuffer(buffer_2)
	הודעה.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipגודל))
	הודעה.Sקבעbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataסמן))

	for i := 0; i < int(גודל); i++ {

		buffer1_2[i+int(ipגודל)] = databuffer_2[i]
	}

	ipconsole.Mהדפסהxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(גודל)+int(ipגודל); i++ {
		ipconsole.MHexadecimalהדפסה(buffer1_2[i])
	}
	ipconsole.Mהדפסה(([]byte)(":"))
	ipconsole.Mהדפסה(([]byte)("]\n"))

	var הבאhopipaddressרשתbyteorder uint32 = יעדipaddressרשתbyteorder
	if (יעדipaddressרשתbyteorder & self.Subnetסינון) != (הודעה.מקורipaddress & self.Subnetסינון) {
		הבאhopipaddressרשתbyteorder = self.Gatewayip
	}

	var שלחdataסמן = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32הדפסה(הבאhopipaddressרשתbyteorder)

	var אתרנטסוגbe = Unsignedinteger16r(0x0800)
	efhandler.Frameשלח(self.arpprovider.Resolve(הבאhopipaddressרשתbyteorder), אתרנטסוגbe, שלחdataסמן, uint32(ipגודל)+uint32(גודל))

}
func (self *Tאינטרנטprotocolprovider) Checksum(pdata *[4096]uint16, אורךנכנסבתים uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataבתים [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (אורךנכנסבתים % 2) != 0 {
		temporary += uint32(uint16(dataבתים[אורךנכנסבתים-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tאינטרנטprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
