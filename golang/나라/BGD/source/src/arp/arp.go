package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpmessagebuffer struct {
	hardwareধরণ		[2]byte
	protocol		[2]byte
	hardwareaddresssize	byte
	protocoladdresssize	byte
	command			[2]byte

	উৎসmacaddress		[6]byte
	উৎসipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgsize uint32 = (64+92+64)/8 + 2

type Arpmessage struct {
	hardwareধরণ		uint16
	protocol		uint16
	hardwareaddresssize	uint8
	protocoladdresssize	uint8
	command			uint16

	উৎসmacaddress		uint64
	উৎসipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpmessage) Init(buffer_2 *Arpmessagebuffer) {

	self.hardwareধরণ = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwareধরণ))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddresssize = byte(buffer_2.hardwareaddresssize)
	self.protocoladdresssize = byte(buffer_2.protocoladdresssize)
	self.command = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.command))

	self.উৎসmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.উৎসmacaddress))
	self.উৎসipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.উৎসipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpmessage) Setbuffer(buffer_2 *Arpmessagebuffer) {
	buffer_2.hardwareধরণ = Unsignedinteger16toarray(self.hardwareধরণ)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddresssize = uint8(self.hardwareaddresssize)
	buffer_2.protocoladdresssize = uint8(self.protocoladdresssize)

	buffer_2.command = Unsignedinteger16toarray(self.command)
	buffer_2.উৎসmacaddress = Unsignedinteger48toarray(self.উৎসmacaddress)
	buffer_2.উৎসipaddress = Unsignedinteger32toarray(self.উৎসipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (self *Arpethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, size int) bool {
	arpconsole.MPrintxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(datapointer, uint32(size))

}
func (self *Arpethernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, size uint32) {
	arpconsole.MPrintxy([]byte("arp send:"), 0, 24)
	var ethernetধরণbe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.Framesend(destinationmacbe, ethernetধরণbe, datapointer, size)
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

	if arp.hardwareধরণ == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddresssize == 6 && arp.protocoladdresssize == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MPrint([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16print(arp.protocol)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(uint64(arp.destinationmacaddress))
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger16print(arp.command)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(handler.Getmacaddress())

			switch arp.command {
			case 0x0100:

				if self.Getmacfromcache(arp.উৎসipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.উৎসipaddress
						self.Maccache[self.numbercacheentry] = arp.উৎসmacaddress
						self.numbercacheentry++
					}
				}
				arp.command = 0x0200
				arp.destinationipaddress = arp.উৎসipaddress
				arp.destinationmacaddress = arp.উৎসmacaddress
				arp.উৎসipaddress = uint32(handler.Getipaddress())
				arp.উৎসmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MPrint(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.উৎসipaddress
					self.Maccache[self.numbercacheentry] = arp.উৎসmacaddress
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
	arp.hardwareধরণ = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddresssize = 6
	arp.protocoladdresssize = 4
	arp.command = 0x0200

	arp.উৎসipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipnetworkbyteorder)
	arp.destinationipaddress = Ipnetworkbyteorder
	arpconsole.MPrintxy([]byte("broad mac"), 0, 15)

	arp.উৎসmacaddress = handler.Getmacaddress()

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgsize)
}
func (self *Arpprovider) Requestmacaddress(Ipnetworkbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.hardwareধরণ = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddresssize = 6
	arp.protocoladdresssize = 4
	arp.command = 0x0100

	arp.উৎসmacaddress = handler.Getmacaddress()
	arp.উৎসipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipnetworkbyteorder

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgsize)
}
func (self *Arpprovider) Testprint(data *[]byte, size uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MPrintxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalprint(buffer_2[i])
		arpconsole.MPrint([]byte(":"))
	}
	arpconsole.MPrint([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipnetworkbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MPrint(([]byte)("["))
		arpconsole.MUnsignedinteger32print(self.Ipcache[i])
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MUnsignedinteger32print(Ipnetworkbyteorder)
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MUnsignedinteger64print(self.Maccache[i])
		arpconsole.MPrint(([]byte)("]\n"))

		if self.Ipcache[i] == Ipnetworkbyteorder {
			arpconsole.MPrint([]byte("getmacfromcache"))
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
