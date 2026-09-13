package arp

import . "unsafe"
import . "console"
import . "ethernetRamka"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpXABARbuffer struct {
	qurilmalarTuri		[2]byte
	protocol		[2]byte
	qurilmalaraddressHajmi	byte
	protocoladdressHajmi	byte
	buyruq			[2]byte

	sourcemacaddress	[6]byte
	sourceipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgHajmi uint32 = (64+92+64)/8 + 2

type ArpXABAR struct {
	qurilmalarTuri		uint16
	protocol		uint16
	qurilmalaraddressHajmi	uint8
	protocoladdressHajmi	uint8
	buyruq			uint16

	sourcemacaddress	uint64
	sourceipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *ArpXABAR) Init(buffer_2 *ArpXABARbuffer) {

	self.qurilmalarTuri = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.qurilmalarTuri))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.qurilmalaraddressHajmi = byte(buffer_2.qurilmalaraddressHajmi)
	self.protocoladdressHajmi = byte(buffer_2.protocoladdressHajmi)
	self.buyruq = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.buyruq))

	self.sourcemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.sourcemacaddress))
	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *ArpXABAR) Setbuffer(buffer_2 *ArpXABARbuffer) {
	buffer_2.qurilmalarTuri = Unsignedinteger16toarray(self.qurilmalarTuri)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.qurilmalaraddressHajmi = uint8(self.qurilmalaraddressHajmi)
	buffer_2.protocoladdressHajmi = uint8(self.protocoladdressHajmi)

	buffer_2.buyruq = Unsignedinteger16toarray(self.buyruq)
	buffer_2.sourcemacaddress = Unsignedinteger48toarray(self.sourcemacaddress)
	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type ArpethernetRamkahandler struct {
	TEthernetRamkahandler
}

var arpprovider Arpprovider
var ethernetRamkaprovider TEthernetRamkaprovider

func (self *ArpethernetRamkahandler) EthernetRamkareceivewhen(dataKorsatgich uintptr, hajmi int) bool {
	arpconsole.MChopetishxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRamkareceivewhen(dataKorsatgich, uint32(hajmi))

}
func (self *ArpethernetRamkahandler) Joʻnatish(destinationmacbe uint64, dataKorsatgich uintptr, hajmi uint32) {
	arpconsole.MChopetishxy([]byte("arp send:"), 0, 24)
	var ethernetTuribe = Unsignedinteger16r(0x0806)
	self.TEthernetRamkahandler.RamkaJoʻnatish(destinationmacbe, ethernetTuribe, dataKorsatgich, hajmi)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	rAQAMcacheentry	int

	handler	IEthernetRamkahandler
}

var handler IEthernetRamkahandler

func (self *Arpprovider) Init(backend TEthernetRamkaprovider, userhandler IEthernetRamkahandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.rAQAMcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetRamkareceivewhen(dataKorsatgich uintptr, hajmi uint32) bool {

	if hajmi < arpmesgHajmi {
		return false
	}
	var arpbuffer *ArpXABARbuffer = (*ArpXABARbuffer)(Pointer(dataKorsatgich))
	var arp ArpXABAR = ArpXABAR{}
	arp.Init(arpbuffer)

	if arp.qurilmalarTuri == 0x0100 {

		if arp.protocol == 0x0008 && arp.qurilmalaraddressHajmi == 6 && arp.protocoladdressHajmi == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MChopetish([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Chopetish(arp.protocol)
			arpconsole.MChopetish([]byte(":"))
			arpconsole.MUnsignedinteger64Chopetish(uint64(arp.destinationmacaddress))
			arpconsole.MChopetish([]byte(":"))
			arpconsole.MUnsignedinteger16Chopetish(arp.buyruq)
			arpconsole.MChopetish([]byte(":"))
			arpconsole.MUnsignedinteger64Chopetish(handler.Getmacaddress())

			switch arp.buyruq {
			case 0x0100:

				if self.Getmacfromcache(arp.sourceipaddress) == 0xFFFFFFFFFFFF {
					if self.rAQAMcacheentry < 128 {
						self.Ipcache[self.rAQAMcacheentry] = arp.sourceipaddress
						self.Maccache[self.rAQAMcacheentry] = arp.sourcemacaddress
						self.rAQAMcacheentry++
					}
				}
				arp.buyruq = 0x0200
				arp.destinationipaddress = arp.sourceipaddress
				arp.destinationmacaddress = arp.sourcemacaddress
				arp.sourceipaddress = uint32(handler.Getipaddress())
				arp.sourcemacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MChopetish(([]byte)("self.numCacheEntries"))

				if self.rAQAMcacheentry < 128 {
					self.Ipcache[self.rAQAMcacheentry] = arp.sourceipaddress
					self.Maccache[self.rAQAMcacheentry] = arp.sourcemacaddress
					self.rAQAMcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpTarmoqbyteorder uint32) {

	var arp ArpXABAR = ArpXABAR{}
	arp.qurilmalarTuri = 0x0100
	arp.protocol = 0x0008
	arp.qurilmalaraddressHajmi = 6
	arp.protocoladdressHajmi = 4
	arp.buyruq = 0x0200

	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpTarmoqbyteorder)
	arp.destinationipaddress = IpTarmoqbyteorder
	arpconsole.MChopetishxy([]byte("broad mac"), 0, 15)

	arp.sourcemacaddress = handler.Getmacaddress()

	var arpbuffer ArpXABARbuffer = ArpXABARbuffer{}
	arp.Setbuffer(&arpbuffer)

	var korsatgich uintptr = uintptr(Pointer(&arpbuffer))
	handler.Joʻnatish(arp.destinationmacaddress, korsatgich, arpmesgHajmi)
}
func (self *Arpprovider) Requestmacaddress(IpTarmoqbyteorder uint32) {

	var arp ArpXABAR = ArpXABAR{}
	arp.qurilmalarTuri = 0x0100

	arp.protocol = 0x0008
	arp.qurilmalaraddressHajmi = 6
	arp.protocoladdressHajmi = 4
	arp.buyruq = 0x0100

	arp.sourcemacaddress = handler.Getmacaddress()
	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpTarmoqbyteorder

	var arpbuffer ArpXABARbuffer = ArpXABARbuffer{}
	arp.Setbuffer(&arpbuffer)

	var korsatgich uintptr = uintptr(Pointer(&arpbuffer))
	handler.Joʻnatish(arp.destinationmacaddress, korsatgich, arpmesgHajmi)
}
func (self *Arpprovider) SinashChopetish(data *[]byte, hajmi uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MChopetishxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalChopetish(buffer_2[i])
		arpconsole.MChopetish([]byte(":"))
	}
	arpconsole.MChopetish([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpTarmoqbyteorder uint32) uint64 {
	for i := 0; i < self.rAQAMcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MChopetish(([]byte)("["))
		arpconsole.MUnsignedinteger32Chopetish(self.Ipcache[i])
		arpconsole.MChopetish(([]byte)(":"))
		arpconsole.MUnsignedinteger32Chopetish(IpTarmoqbyteorder)
		arpconsole.MChopetish(([]byte)(":"))
		arpconsole.MChopetish(([]byte)(":"))
		arpconsole.MUnsignedinteger64Chopetish(self.Maccache[i])
		arpconsole.MChopetish(([]byte)("]\n"))

		if self.Ipcache[i] == IpTarmoqbyteorder {
			arpconsole.MChopetish([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpTarmoqbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpTarmoqbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpTarmoqbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpTarmoqbyteorder)

	}

	return result
}
