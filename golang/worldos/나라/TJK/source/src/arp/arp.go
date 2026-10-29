/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpmessagebuffer struct {
	hardwaretype		[2]byte
	protocol		[2]byte
	hardwareaddresssize	byte
	protocoladdresssize	byte
	command			[2]byte

	sourcemacaddress	[6]byte
	sourceipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgsize uint32 = (64+92+64)/8 + 2

type Arpmessage struct {
	hardwaretype		uint16
	protocol		uint16
	hardwareaddresssize	uint8
	protocoladdresssize	uint8
	command			uint16

	sourcemacaddress	uint64
	sourceipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpmessage) Init(buffer_2 *Arpmessagebuffer) {

	self.hardwaretype = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwaretype))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddresssize = byte(buffer_2.hardwareaddresssize)
	self.protocoladdresssize = byte(buffer_2.protocoladdresssize)
	self.command = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.command))

	self.sourcemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.sourcemacaddress))
	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpmessage) Setbuffer(buffer_2 *Arpmessagebuffer) {
	buffer_2.hardwaretype = Unsignedinteger16toarray(self.hardwaretype)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddresssize = uint8(self.hardwareaddresssize)
	buffer_2.protocoladdresssize = uint8(self.protocoladdresssize)

	buffer_2.command = Unsignedinteger16toarray(self.command)
	buffer_2.sourcemacaddress = Unsignedinteger48toarray(self.sourcemacaddress)
	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (self *Arpethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, size int) bool {
	arpconsole.MЧопкарданxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(datapointer, uint32(size))

}
func (self *Arpethernetframehandler) Ирсолкунед(destinationmacbe uint64, datapointer uintptr, size uint32) {
	arpconsole.MЧопкарданxy([]byte("arp send:"), 0, 24)
	var ethernettypebe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.FrameИрсолкунед(destinationmacbe, ethernettypebe, datapointer, size)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (self *Arpprovider) Init(backend TEthernetframeprovider, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernetframereceivewhen(datapointer uintptr, size uint32) bool {

	if size < arpmesgsize {
		return false
	}
	var arpbuffer *Arpmessagebuffer = (*Arpmessagebuffer)(Pointer(datapointer))
	var arp Arpmessage = Arpmessage{}
	arp.Init(arpbuffer)

	if arp.hardwaretype == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddresssize == 6 && arp.protocoladdresssize == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MЧопкардан([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Чопкардан(arp.protocol)
			arpconsole.MЧопкардан([]byte(":"))
			arpconsole.MUnsignedinteger64Чопкардан(uint64(arp.destinationmacaddress))
			arpconsole.MЧопкардан([]byte(":"))
			arpconsole.MUnsignedinteger16Чопкардан(arp.command)
			arpconsole.MЧопкардан([]byte(":"))
			arpconsole.MUnsignedinteger64Чопкардан(handler.Getmacaddress())

			switch arp.command {
			case 0x0100:

				if self.Getmacfromcache(arp.sourceipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.sourceipaddress
						self.Maccache[self.numbercacheentry] = arp.sourcemacaddress
						self.numbercacheentry++
					}
				}
				arp.command = 0x0200
				arp.destinationipaddress = arp.sourceipaddress
				arp.destinationmacaddress = arp.sourcemacaddress
				arp.sourceipaddress = uint32(handler.Getipaddress())
				arp.sourcemacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MЧопкардан(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.sourceipaddress
					self.Maccache[self.numbercacheentry] = arp.sourcemacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipnetworkbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.hardwaretype = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddresssize = 6
	arp.protocoladdresssize = 4
	arp.command = 0x0200

	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipnetworkbyteorder)
	arp.destinationipaddress = Ipnetworkbyteorder
	arpconsole.MЧопкарданxy([]byte("broad mac"), 0, 15)

	arp.sourcemacaddress = handler.Getmacaddress()

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Ирсолкунед(arp.destinationmacaddress, pointer, arpmesgsize)
}
func (self *Arpprovider) Requestmacaddress(Ipnetworkbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.hardwaretype = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddresssize = 6
	arp.protocoladdresssize = 4
	arp.command = 0x0100

	arp.sourcemacaddress = handler.Getmacaddress()
	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipnetworkbyteorder

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Ирсолкунед(arp.destinationmacaddress, pointer, arpmesgsize)
}
func (self *Arpprovider) TestЧопкардан(data *[]byte, size uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MЧопкарданxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalЧопкардан(buffer_2[i])
		arpconsole.MЧопкардан([]byte(":"))
	}
	arpconsole.MЧопкардан([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipnetworkbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MЧопкардан(([]byte)("["))
		arpconsole.MUnsignedinteger32Чопкардан(self.Ipcache[i])
		arpconsole.MЧопкардан(([]byte)(":"))
		arpconsole.MUnsignedinteger32Чопкардан(Ipnetworkbyteorder)
		arpconsole.MЧопкардан(([]byte)(":"))
		arpconsole.MЧопкардан(([]byte)(":"))
		arpconsole.MUnsignedinteger64Чопкардан(self.Maccache[i])
		arpconsole.MЧопкардан(([]byte)("]\n"))

		if self.Ipcache[i] == Ipnetworkbyteorder {
			arpconsole.MЧопкардан([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipnetworkbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipnetworkbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipnetworkbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipnetworkbyteorder)

	}

	return result
}
