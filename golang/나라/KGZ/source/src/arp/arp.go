package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpmessagebuffer struct {
	жабдууларТүрү		[2]byte
	protocol		[2]byte
	жабдууларaddressӨлчөм	byte
	protocoladdressӨлчөм	byte
	команда			[2]byte

	баштапкытекстmacaddress	[6]byte
	баштапкытекстipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgӨлчөм uint32 = (64+92+64)/8 + 2

type Arpmessage struct {
	жабдууларТүрү		uint16
	protocol		uint16
	жабдууларaddressӨлчөм	uint8
	protocoladdressӨлчөм	uint8
	команда			uint16

	баштапкытекстmacaddress	uint64
	баштапкытекстipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpmessage) Init(buffer_2 *Arpmessagebuffer) {

	self.жабдууларТүрү = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.жабдууларТүрү))
	self.protocol = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.protocol))
	self.жабдууларaddressӨлчөм = byte(buffer_2.жабдууларaddressӨлчөм)
	self.protocoladdressӨлчөм = byte(buffer_2.protocoladdressӨлчөм)
	self.команда = Unsignedinteger16r(Массивtounsignedinteger16(buffer_2.команда))

	self.баштапкытекстmacaddress = Unsignedinteger48r(Массивtounsignedinteger48(buffer_2.баштапкытекстmacaddress))
	self.баштапкытекстipaddress = Unsignedinteger32r(Массивtounsignedinteger32(buffer_2.баштапкытекстipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Массивtounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Массивtounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpmessage) Setbuffer(buffer_2 *Arpmessagebuffer) {
	buffer_2.жабдууларТүрү = Unsignedinteger16toМассив(self.жабдууларТүрү)
	buffer_2.protocol = Unsignedinteger16toМассив(self.protocol)
	buffer_2.жабдууларaddressӨлчөм = uint8(self.жабдууларaddressӨлчөм)
	buffer_2.protocoladdressӨлчөм = uint8(self.protocoladdressӨлчөм)

	buffer_2.команда = Unsignedinteger16toМассив(self.команда)
	buffer_2.баштапкытекстmacaddress = Unsignedinteger48toМассив(self.баштапкытекстmacaddress)
	buffer_2.баштапкытекстipaddress = Unsignedinteger32toМассив(self.баштапкытекстipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toМассив(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toМассив(self.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (self *Arpethernetframehandler) Ethernetframereceivewhen(dataКөрсөткүч uintptr, өлчөм int) bool {
	arpconsole.MБасмаxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(dataКөрсөткүч, uint32(өлчөм))

}
func (self *Arpethernetframehandler) Send(destinationmacbe uint64, dataКөрсөткүч uintptr, өлчөм uint32) {
	arpconsole.MБасмаxy([]byte("arp send:"), 0, 24)
	var ethernetТүрүbe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.Framesend(destinationmacbe, ethernetТүрүbe, dataКөрсөткүч, өлчөм)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	нОМЕРcacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (self *Arpprovider) Init(backend TEthernetframeprovider, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.нОМЕРcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernetframereceivewhen(dataКөрсөткүч uintptr, өлчөм uint32) bool {

	if өлчөм < arpmesgӨлчөм {
		return false
	}
	var arpbuffer *Arpmessagebuffer = (*Arpmessagebuffer)(Pointer(dataКөрсөткүч))
	var arp Arpmessage = Arpmessage{}
	arp.Init(arpbuffer)

	if arp.жабдууларТүрү == 0x0100 {

		if arp.protocol == 0x0008 && arp.жабдууларaddressӨлчөм == 6 && arp.protocoladdressӨлчөм == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MБасма([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Басма(arp.protocol)
			arpconsole.MБасма([]byte(":"))
			arpconsole.MUnsignedinteger64Басма(uint64(arp.destinationmacaddress))
			arpconsole.MБасма([]byte(":"))
			arpconsole.MUnsignedinteger16Басма(arp.команда)
			arpconsole.MБасма([]byte(":"))
			arpconsole.MUnsignedinteger64Басма(handler.Getmacaddress())

			switch arp.команда {
			case 0x0100:

				if self.Getmacfromcache(arp.баштапкытекстipaddress) == 0xFFFFFFFFFFFF {
					if self.нОМЕРcacheentry < 128 {
						self.Ipcache[self.нОМЕРcacheentry] = arp.баштапкытекстipaddress
						self.Maccache[self.нОМЕРcacheentry] = arp.баштапкытекстmacaddress
						self.нОМЕРcacheentry++
					}
				}
				arp.команда = 0x0200
				arp.destinationipaddress = arp.баштапкытекстipaddress
				arp.destinationmacaddress = arp.баштапкытекстmacaddress
				arp.баштапкытекстipaddress = uint32(handler.Getipaddress())
				arp.баштапкытекстmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MБасма(([]byte)("self.numCacheEntries"))

				if self.нОМЕРcacheentry < 128 {
					self.Ipcache[self.нОМЕРcacheentry] = arp.баштапкытекстipaddress
					self.Maccache[self.нОМЕРcacheentry] = arp.баштапкытекстmacaddress
					self.нОМЕРcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpТармакbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.жабдууларТүрү = 0x0100
	arp.protocol = 0x0008
	arp.жабдууларaddressӨлчөм = 6
	arp.protocoladdressӨлчөм = 4
	arp.команда = 0x0200

	arp.баштапкытекстipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpТармакbyteorder)
	arp.destinationipaddress = IpТармакbyteorder
	arpconsole.MБасмаxy([]byte("broad mac"), 0, 15)

	arp.баштапкытекстmacaddress = handler.Getmacaddress()

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var көрсөткүч uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, көрсөткүч, arpmesgӨлчөм)
}
func (self *Arpprovider) Requestmacaddress(IpТармакbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.жабдууларТүрү = 0x0100

	arp.protocol = 0x0008
	arp.жабдууларaddressӨлчөм = 6
	arp.protocoladdressӨлчөм = 4
	arp.команда = 0x0100

	arp.баштапкытекстmacaddress = handler.Getmacaddress()
	arp.баштапкытекстipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpТармакbyteorder

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var көрсөткүч uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, көрсөткүч, arpmesgӨлчөм)
}
func (self *Arpprovider) ТекшерүүБасма(data *[]byte, өлчөм uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MБасмаxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalБасма(buffer_2[i])
		arpconsole.MБасма([]byte(":"))
	}
	arpconsole.MБасма([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpТармакbyteorder uint32) uint64 {
	for i := 0; i < self.нОМЕРcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MБасма(([]byte)("["))
		arpconsole.MUnsignedinteger32Басма(self.Ipcache[i])
		arpconsole.MБасма(([]byte)(":"))
		arpconsole.MUnsignedinteger32Басма(IpТармакbyteorder)
		arpconsole.MБасма(([]byte)(":"))
		arpconsole.MБасма(([]byte)(":"))
		arpconsole.MUnsignedinteger64Басма(self.Maccache[i])
		arpconsole.MБасма(([]byte)("]\n"))

		if self.Ipcache[i] == IpТармакbyteorder {
			arpconsole.MБасма([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpТармакbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpТармакbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpТармакbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpТармакbyteorder)

	}

	return result
}
