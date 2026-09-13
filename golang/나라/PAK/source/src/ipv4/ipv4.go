package ipv4

import . "unsafe"
import . "util"
import . "console"
import . "ایتھرنیٹframe"
import . "arp"

var ipconsole TConsole = TConsole{}

type Tانٹرنیٹprotocolv4پیغامbuffer struct {
	lenver		byte
	tos		byte
	میزانطول	[2]byte

	ident			[2]byte
	جھنڈیاںandoffset	[2]byte

	وقتtolive	byte
	protocol	byte
	checksum	[2]byte

	مصدرipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipحجم uint8 = (4 + 4 + 4 + 8)

type Tانٹرنیٹprotocolv4پیغام struct {
	headerطول	uint8
	ورژن		uint8
	tos		uint8
	میزانطول	uint16

	ident			uint16
	جھنڈیاںandoffset	uint16

	وقتtolive	uint8
	protocol	uint8
	checksum	uint16

	مصدرipaddress		uint32
	destinationipaddress	uint32
}

func (self *Tانٹرنیٹprotocolv4پیغام) Init(buffer_2 Tانٹرنیٹprotocolv4پیغامbuffer) {

	self.ورژن = ((buffer_2.lenver & 0xF0) >> 4)
	self.headerطول = buffer_2.lenver & 0x0F
	self.tos = buffer_2.tos
	self.میزانطول = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.میزانطول))

	self.ident = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.ident))
	self.جھنڈیاںandoffset = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.جھنڈیاںandoffset))

	self.وقتtolive = buffer_2.وقتtolive
	self.protocol = buffer_2.protocol
	self.checksum = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.checksum))

	self.مصدرipaddress = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer_2.مصدرipaddress))
	self.destinationipaddress = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer_2.destinationipaddress))

}
func (self *Tانٹرنیٹprotocolv4پیغام) Sسیٹbuffer(buffer_2 *Tانٹرنیٹprotocolv4پیغامbuffer) {

	buffer_2.lenver = byte(((self.ورژن & 0x0F) << 4) | (self.headerطول & 0x0F))
	buffer_2.tos = self.tos
	buffer_2.میزانطول = Unsignedinteger16toلڑی(self.میزانطول)

	buffer_2.ident = Unsignedinteger16toلڑی(self.ident)
	buffer_2.جھنڈیاںandoffset = Unsignedinteger16toلڑی(self.جھنڈیاںandoffset)

	buffer_2.وقتtolive = self.وقتtolive
	buffer_2.protocol = self.protocol
	buffer_2.checksum = Unsignedinteger16toلڑی(self.checksum)

	buffer_2.مصدرipaddress = Unsignedinteger32toلڑی(self.مصدرipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toلڑی(self.destinationipaddress)

}

type Iانٹرنیٹprotocolhandler interface {
	Init(backend Tانٹرنیٹprotocolprovider, pihandler Iانٹرنیٹprotocolhandler, pprotocol uint8)
	Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder uint32, destinationipaddressنیٹورکbyteorder uint32, dataپؤائنٹر uintptr, حجم uint32) bool
	Send(destinationipaddressنیٹورکbyteorder uint32, pprotocol uint8, dataپؤائنٹر uintptr, حجم uint32)
	Providerget() *Tانٹرنیٹprotocolprovider
}

type Tانٹرنیٹprotocolhandler struct {
}

var ipایتھرنیٹframehandler Ipایتھرنیٹframehandler = Ipایتھرنیٹframehandler{}
var protocol uint8

func (self *Tانٹرنیٹprotocolhandler) Init(backend Tانٹرنیٹprotocolprovider, pihandler Iانٹرنیٹprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (self *Tانٹرنیٹprotocolhandler) Oانٹرنیٹprotocolreceivewhen(مصدرipaddressنیٹورکbyteorder uint32, destinationipaddressنیٹورکbyteorder uint32, dataپؤائنٹر uintptr, حجم uint32) bool {
	ipconsole.Mچھاپیں(([]byte)("ipHandler:OnInternet"))
	return false
}
func (self *Tانٹرنیٹprotocolhandler) Send(destinationipaddressنیٹورکbyteorder uint32, pprotocol uint8, dataپؤائنٹر uintptr, حجم uint32) {

	ipprovider.Send(destinationipaddressنیٹورکbyteorder, pprotocol, dataپؤائنٹر, حجم)
}
func (self *Tانٹرنیٹprotocolhandler) Providerget() *Tانٹرنیٹprotocolprovider {
	return &ipprovider
}

type Ipایتھرنیٹframehandler struct {
	Tایتھرنیٹframehandler
}

var ipprovider Tانٹرنیٹprotocolprovider

func (self *Ipایتھرنیٹframehandler) Oایتھرنیٹframereceivewhen(dataپؤائنٹر uintptr, حجم int) bool {
	ipconsole.Mچھاپیں(([]byte)("iphandler:onEtherfameRecv\n"))
	return ipprovider.Oایتھرنیٹframereceivewhen(dataپؤائنٹر, uint32(حجم))

}

func (self *Ipایتھرنیٹframehandler) Send(destinationipaddressنیٹورکbyteorder uint64, dataپؤائنٹر uintptr, حجم uint32) {
	ipconsole.Mچھاپیں(([]byte)("ipefhandler:send\n"))
	var ایتھرنیٹنوعیتbe = Unsignedinteger16r(0x0800)
	self.Tایتھرنیٹframehandler.Framesend(destinationipaddressنیٹورکbyteorder, ایتھرنیٹنوعیتbe, dataپؤائنٹر, حجم)

}

var handler_2 [255]Iانٹرنیٹprotocolhandler

type Tانٹرنیٹprotocolprovider struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler Iایتھرنیٹframehandler

func (self *Tانٹرنیٹprotocolprovider) Init(pefprovider Tایتھرنیٹframeprovider, pefhandler Iایتھرنیٹframehandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Sسیٹhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	self.arpprovider = arp
	self.Gatewayip = gatewayip
	self.Subnetmask = subnetmask
	ipprovider = *self
}
func (self *Tانٹرنیٹprotocolprovider) Oایتھرنیٹframereceivewhen(ایتھرنیٹframepayload uintptr, حجم uint32) bool {
	if حجم < uint32(ipحجم) {
		return false
	}

	var buffer_2 *Tانٹرنیٹprotocolv4پیغامbuffer = (*Tانٹرنیٹprotocolv4پیغامbuffer)(Pointer(ایتھرنیٹframepayload))
	var انٹرنیٹprotocolپیغام Tانٹرنیٹprotocolv4پیغام
	انٹرنیٹprotocolپیغام.Init(*buffer_2)

	var reply bool = false

	if انٹرنیٹprotocolپیغام.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var طول uint32 = uint32(انٹرنیٹprotocolپیغام.میزانطول)
		if طول > حجم {
			طول = حجم
		}
		if handler_2[انٹرنیٹprotocolپیغام.protocol] != nil {
			reply = handler_2[انٹرنیٹprotocolپیغام.protocol].Oانٹرنیٹprotocolreceivewhen(انٹرنیٹprotocolپیغام.مصدرipaddress, انٹرنیٹprotocolپیغام.destinationipaddress, ایتھرنیٹframepayload+uintptr(4*انٹرنیٹprotocolپیغام.headerطول), uint32(طول-uint32(4*انٹرنیٹprotocolپیغام.headerطول)))

		}
	}

	if reply {

		var temporary = انٹرنیٹprotocolپیغام.destinationipaddress
		انٹرنیٹprotocolپیغام.destinationipaddress = انٹرنیٹprotocolپیغام.مصدرipaddress
		انٹرنیٹprotocolپیغام.مصدرipaddress = temporary

		انٹرنیٹprotocolپیغام.وقتtolive = 0x40
		انٹرنیٹprotocolپیغام.checksum = 0

		انٹرنیٹprotocolپیغام.Sسیٹbuffer(buffer_2)
		انٹرنیٹprotocolپیغام.checksum = self.Checksum((*([4096]uint16))(Pointer(ایتھرنیٹframepayload)), uint32(4*انٹرنیٹprotocolپیغام.headerطول))

		انٹرنیٹprotocolپیغام.Sسیٹbuffer(buffer_2)

	}

	ipconsole.Mچھاپیں(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32چھاپیں(انٹرنیٹprotocolپیغام.مصدرipaddress)
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.MUnsignedinteger32چھاپیں(انٹرنیٹprotocolپیغام.destinationipaddress)
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.MUnsignedinteger16چھاپیں(uint16(انٹرنیٹprotocolپیغام.headerطول))
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.MUnsignedinteger16چھاپیں(uint16(انٹرنیٹprotocolپیغام.ورژن))
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.MUnsignedinteger16چھاپیں(انٹرنیٹprotocolپیغام.میزانطول)
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.MUnsignedinteger32چھاپیں(uint32(efhandler.Getipaddress()))
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.Mچھاپیں(([]byte)("\n"))

	return reply

}
func (self *Tانٹرنیٹprotocolprovider) Send(destinationipaddressنیٹورکbyteorder uint32, protocol uint8, dataپؤائنٹر uintptr, حجم uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *Tانٹرنیٹprotocolv4پیغامbuffer = (*Tانٹرنیٹprotocolv4پیغامbuffer)(Pointer(&buffer1_2))
	var پیغام Tانٹرنیٹprotocolv4پیغام = Tانٹرنیٹprotocolv4پیغام{}
	پیغام.ورژن = 4
	پیغام.headerطول = ipحجم / 4
	پیغام.tos = 0
	پیغام.میزانطول = Unsignedinteger16r(uint16(حجم + uint32(ipحجم)))

	پیغام.ident = 0x0100
	پیغام.جھنڈیاںandoffset = 0x0040
	پیغام.وقتtolive = 0x40
	پیغام.protocol = protocol

	پیغام.destinationipaddress = destinationipaddressنیٹورکbyteorder

	پیغام.مصدرipaddress = uint32(efhandler.Getipaddress())

	پیغام.checksum = 0

	پیغام.Sسیٹbuffer(buffer_2)
	پیغام.checksum = self.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipحجم))
	پیغام.Sسیٹbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataپؤائنٹر))

	for i := 0; i < int(حجم); i++ {

		buffer1_2[i+int(ipحجم)] = databuffer_2[i]
	}

	ipconsole.Mچھاپیںxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(حجم)+int(ipحجم); i++ {
		ipconsole.MHexadecimalچھاپیں(buffer1_2[i])
	}
	ipconsole.Mچھاپیں(([]byte)(":"))
	ipconsole.Mچھاپیں(([]byte)("]\n"))

	var اگلاhopipaddressنیٹورکbyteorder uint32 = destinationipaddressنیٹورکbyteorder
	if (destinationipaddressنیٹورکbyteorder & self.Subnetmask) != (پیغام.مصدرipaddress & self.Subnetmask) {
		اگلاhopipaddressنیٹورکbyteorder = self.Gatewayip
	}

	var senddataپؤائنٹر = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32چھاپیں(اگلاhopipaddressنیٹورکbyteorder)

	var ایتھرنیٹنوعیتbe = Unsignedinteger16r(0x0800)
	efhandler.Framesend(self.arpprovider.Resolve(اگلاhopipaddressنیٹورکbyteorder), ایتھرنیٹنوعیتbe, senddataپؤائنٹر, uint32(ipحجم)+uint32(حجم))

}
func (self *Tانٹرنیٹprotocolprovider) Checksum(pdata *[4096]uint16, طولاندربائٹس uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataبائٹس [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (طولاندربائٹس % 2) != 0 {
		temporary += uint32(uint16(dataبائٹس[طولاندربائٹس-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (self *Tانٹرنیٹprotocolprovider) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
