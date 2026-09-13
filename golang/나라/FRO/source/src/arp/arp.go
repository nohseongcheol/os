package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpboðanbuffer struct {
	hardwaretype		[2]byte
	protocol		[2]byte
	hardwareaddressStødd	byte
	protocoladdressStødd	byte
	stýriboð		[2]byte

	sourcemacaddress	[6]byte
	sourceipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgStødd uint32 = (64+92+64)/8 + 2

type Arpboðan struct {
	hardwaretype		uint16
	protocol		uint16
	hardwareaddressStødd	uint8
	protocoladdressStødd	uint8
	stýriboð		uint16

	sourcemacaddress	uint64
	sourceipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpboðan) Init(buffer_2 *Arpboðanbuffer) {

	self.hardwaretype = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwaretype))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddressStødd = byte(buffer_2.hardwareaddressStødd)
	self.protocoladdressStødd = byte(buffer_2.protocoladdressStødd)
	self.stýriboð = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.stýriboð))

	self.sourcemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.sourcemacaddress))
	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpboðan) Setbuffer(buffer_2 *Arpboðanbuffer) {
	buffer_2.hardwaretype = Unsignedinteger16toarray(self.hardwaretype)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddressStødd = uint8(self.hardwareaddressStødd)
	buffer_2.protocoladdressStødd = uint8(self.protocoladdressStødd)

	buffer_2.stýriboð = Unsignedinteger16toarray(self.stýriboð)
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

func (self *Arpethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, stødd int) bool {
	arpconsole.MPrintxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(datapointer, uint32(stødd))

}
func (self *Arpethernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, stødd uint32) {
	arpconsole.MPrintxy([]byte("arp send:"), 0, 24)
	var ethernettypebe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.Framesend(destinationmacbe, ethernettypebe, datapointer, stødd)
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

func (self *Arpprovider) Ethernetframereceivewhen(datapointer uintptr, stødd uint32) bool {

	if stødd < arpmesgStødd {
		return false
	}
	var arpbuffer *Arpboðanbuffer = (*Arpboðanbuffer)(Pointer(datapointer))
	var arp Arpboðan = Arpboðan{}
	arp.Init(arpbuffer)

	if arp.hardwaretype == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressStødd == 6 && arp.protocoladdressStødd == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MPrint([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16print(arp.protocol)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(uint64(arp.destinationmacaddress))
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger16print(arp.stýriboð)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(handler.Getmacaddress())

			switch arp.stýriboð {
			case 0x0100:

				if self.Getmacfromcache(arp.sourceipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.sourceipaddress
						self.Maccache[self.numbercacheentry] = arp.sourcemacaddress
						self.numbercacheentry++
					}
				}
				arp.stýriboð = 0x0200
				arp.destinationipaddress = arp.sourceipaddress
				arp.destinationmacaddress = arp.sourcemacaddress
				arp.sourceipaddress = uint32(handler.Getipaddress())
				arp.sourcemacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MPrint(([]byte)("self.numCacheEntries"))

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

func (self *Arpprovider) Broadcastmacaddress(IpNetbyteorder uint32) {

	var arp Arpboðan = Arpboðan{}
	arp.hardwaretype = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressStødd = 6
	arp.protocoladdressStødd = 4
	arp.stýriboð = 0x0200

	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpNetbyteorder)
	arp.destinationipaddress = IpNetbyteorder
	arpconsole.MPrintxy([]byte("broad mac"), 0, 15)

	arp.sourcemacaddress = handler.Getmacaddress()

	var arpbuffer Arpboðanbuffer = Arpboðanbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgStødd)
}
func (self *Arpprovider) Requestmacaddress(IpNetbyteorder uint32) {

	var arp Arpboðan = Arpboðan{}
	arp.hardwaretype = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressStødd = 6
	arp.protocoladdressStødd = 4
	arp.stýriboð = 0x0100

	arp.sourcemacaddress = handler.Getmacaddress()
	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpNetbyteorder

	var arpbuffer Arpboðanbuffer = Arpboðanbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgStødd)
}
func (self *Arpprovider) Testprint(data *[]byte, stødd uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MPrintxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalprint(buffer_2[i])
		arpconsole.MPrint([]byte(":"))
	}
	arpconsole.MPrint([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpNetbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MPrint(([]byte)("["))
		arpconsole.MUnsignedinteger32print(self.Ipcache[i])
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MUnsignedinteger32print(IpNetbyteorder)
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MPrint(([]byte)(":"))
		arpconsole.MUnsignedinteger64print(self.Maccache[i])
		arpconsole.MPrint(([]byte)("]\n"))

		if self.Ipcache[i] == IpNetbyteorder {
			arpconsole.MPrint([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpNetbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpNetbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpNetbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpNetbyteorder)

	}

	return result
}
