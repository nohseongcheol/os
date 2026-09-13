package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpSargytbuffer struct {
	hardwareHil		[2]byte
	protocol		[2]byte
	hardwareaddressUlulyk	byte
	protocoladdressUlulyk	byte
	command			[2]byte

	çeşmemacaddress		[6]byte
	çeşmeipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgUlulyk uint32 = (64+92+64)/8 + 2

type ArpSargyt struct {
	hardwareHil		uint16
	protocol		uint16
	hardwareaddressUlulyk	uint8
	protocoladdressUlulyk	uint8
	command			uint16

	çeşmemacaddress		uint64
	çeşmeipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *ArpSargyt) Init(buffer_2 *ArpSargytbuffer) {

	self.hardwareHil = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwareHil))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddressUlulyk = byte(buffer_2.hardwareaddressUlulyk)
	self.protocoladdressUlulyk = byte(buffer_2.protocoladdressUlulyk)
	self.command = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.command))

	self.çeşmemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.çeşmemacaddress))
	self.çeşmeipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.çeşmeipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *ArpSargyt) Setbuffer(buffer_2 *ArpSargytbuffer) {
	buffer_2.hardwareHil = Unsignedinteger16toarray(self.hardwareHil)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddressUlulyk = uint8(self.hardwareaddressUlulyk)
	buffer_2.protocoladdressUlulyk = uint8(self.protocoladdressUlulyk)

	buffer_2.command = Unsignedinteger16toarray(self.command)
	buffer_2.çeşmemacaddress = Unsignedinteger48toarray(self.çeşmemacaddress)
	buffer_2.çeşmeipaddress = Unsignedinteger32toarray(self.çeşmeipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (self *Arpethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, ululyk int) bool {
	arpconsole.MÇapxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(datapointer, uint32(ululyk))

}
func (self *Arpethernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, ululyk uint32) {
	arpconsole.MÇapxy([]byte("arp send:"), 0, 24)
	var ethernetHilbe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.Framesend(destinationmacbe, ethernetHilbe, datapointer, ululyk)
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

func (self *Arpprovider) Ethernetframereceivewhen(datapointer uintptr, ululyk uint32) bool {

	if ululyk < arpmesgUlulyk {
		return false
	}
	var arpbuffer *ArpSargytbuffer = (*ArpSargytbuffer)(Pointer(datapointer))
	var arp ArpSargyt = ArpSargyt{}
	arp.Init(arpbuffer)

	if arp.hardwareHil == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressUlulyk == 6 && arp.protocoladdressUlulyk == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MÇap([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Çap(arp.protocol)
			arpconsole.MÇap([]byte(":"))
			arpconsole.MUnsignedinteger64Çap(uint64(arp.destinationmacaddress))
			arpconsole.MÇap([]byte(":"))
			arpconsole.MUnsignedinteger16Çap(arp.command)
			arpconsole.MÇap([]byte(":"))
			arpconsole.MUnsignedinteger64Çap(handler.Getmacaddress())

			switch arp.command {
			case 0x0100:

				if self.Getmacfromcache(arp.çeşmeipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.çeşmeipaddress
						self.Maccache[self.numbercacheentry] = arp.çeşmemacaddress
						self.numbercacheentry++
					}
				}
				arp.command = 0x0200
				arp.destinationipaddress = arp.çeşmeipaddress
				arp.destinationmacaddress = arp.çeşmemacaddress
				arp.çeşmeipaddress = uint32(handler.Getipaddress())
				arp.çeşmemacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MÇap(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.çeşmeipaddress
					self.Maccache[self.numbercacheentry] = arp.çeşmemacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpŞebekebyteorder uint32) {

	var arp ArpSargyt = ArpSargyt{}
	arp.hardwareHil = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressUlulyk = 6
	arp.protocoladdressUlulyk = 4
	arp.command = 0x0200

	arp.çeşmeipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpŞebekebyteorder)
	arp.destinationipaddress = IpŞebekebyteorder
	arpconsole.MÇapxy([]byte("broad mac"), 0, 15)

	arp.çeşmemacaddress = handler.Getmacaddress()

	var arpbuffer ArpSargytbuffer = ArpSargytbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgUlulyk)
}
func (self *Arpprovider) Requestmacaddress(IpŞebekebyteorder uint32) {

	var arp ArpSargyt = ArpSargyt{}
	arp.hardwareHil = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressUlulyk = 6
	arp.protocoladdressUlulyk = 4
	arp.command = 0x0100

	arp.çeşmemacaddress = handler.Getmacaddress()
	arp.çeşmeipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpŞebekebyteorder

	var arpbuffer ArpSargytbuffer = ArpSargytbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgUlulyk)
}
func (self *Arpprovider) TestÇap(data *[]byte, ululyk uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MÇapxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalÇap(buffer_2[i])
		arpconsole.MÇap([]byte(":"))
	}
	arpconsole.MÇap([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpŞebekebyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MÇap(([]byte)("["))
		arpconsole.MUnsignedinteger32Çap(self.Ipcache[i])
		arpconsole.MÇap(([]byte)(":"))
		arpconsole.MUnsignedinteger32Çap(IpŞebekebyteorder)
		arpconsole.MÇap(([]byte)(":"))
		arpconsole.MÇap(([]byte)(":"))
		arpconsole.MUnsignedinteger64Çap(self.Maccache[i])
		arpconsole.MÇap(([]byte)("]\n"))

		if self.Ipcache[i] == IpŞebekebyteorder {
			arpconsole.MÇap([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpŞebekebyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpŞebekebyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpŞebekebyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpŞebekebyteorder)

	}

	return result
}
