/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetIkadiri"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpUbutumwabuffer struct {
	hardwareUbwoko		[2]byte
	protocol		[2]byte
	hardwareaddressIngano	byte
	protocoladdressIngano	byte
	icyowifuza		[2]byte

	inkomokomacaddress	[6]byte
	inkomokoipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgIngano uint32 = (64+92+64)/8 + 2

type ArpUbutumwa struct {
	hardwareUbwoko		uint16
	protocol		uint16
	hardwareaddressIngano	uint8
	protocoladdressIngano	uint8
	icyowifuza		uint16

	inkomokomacaddress	uint64
	inkomokoipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *ArpUbutumwa) Init(buffer_2 *ArpUbutumwabuffer) {

	self.hardwareUbwoko = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.hardwareUbwoko))
	self.protocol = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.protocol))
	self.hardwareaddressIngano = byte(buffer_2.hardwareaddressIngano)
	self.protocoladdressIngano = byte(buffer_2.protocoladdressIngano)
	self.icyowifuza = Unsignedinteger16r(Imbonerahamwetounsignedinteger16(buffer_2.icyowifuza))

	self.inkomokomacaddress = Unsignedinteger48r(Imbonerahamwetounsignedinteger48(buffer_2.inkomokomacaddress))
	self.inkomokoipaddress = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer_2.inkomokoipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Imbonerahamwetounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Imbonerahamwetounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *ArpUbutumwa) Setbuffer(buffer_2 *ArpUbutumwabuffer) {
	buffer_2.hardwareUbwoko = Unsignedinteger16toImbonerahamwe(self.hardwareUbwoko)
	buffer_2.protocol = Unsignedinteger16toImbonerahamwe(self.protocol)
	buffer_2.hardwareaddressIngano = uint8(self.hardwareaddressIngano)
	buffer_2.protocoladdressIngano = uint8(self.protocoladdressIngano)

	buffer_2.icyowifuza = Unsignedinteger16toImbonerahamwe(self.icyowifuza)
	buffer_2.inkomokomacaddress = Unsignedinteger48toImbonerahamwe(self.inkomokomacaddress)
	buffer_2.inkomokoipaddress = Unsignedinteger32toImbonerahamwe(self.inkomokoipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toImbonerahamwe(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toImbonerahamwe(self.destinationipaddress)
}

type ArpethernetIkadirihandler struct {
	TEthernetIkadirihandler
}

var arpprovider Arpprovider
var ethernetIkadiriprovider TEthernetIkadiriprovider

func (self *ArpethernetIkadirihandler) EthernetIkadirireceivewhen(datapointer uintptr, ingano int) bool {
	arpconsole.MGucapaxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetIkadirireceivewhen(datapointer, uint32(ingano))

}
func (self *ArpethernetIkadirihandler) Send(destinationmacbe uint64, datapointer uintptr, ingano uint32) {
	arpconsole.MGucapaxy([]byte("arp send:"), 0, 24)
	var ethernetUbwokobe = Unsignedinteger16r(0x0806)
	self.TEthernetIkadirihandler.Ikadirisend(destinationmacbe, ethernetUbwokobe, datapointer, ingano)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetIkadirihandler
}

var handler IEthernetIkadirihandler

func (self *Arpprovider) Init(backend TEthernetIkadiriprovider, userhandler IEthernetIkadirihandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetIkadirireceivewhen(datapointer uintptr, ingano uint32) bool {

	if ingano < arpmesgIngano {
		return false
	}
	var arpbuffer *ArpUbutumwabuffer = (*ArpUbutumwabuffer)(Pointer(datapointer))
	var arp ArpUbutumwa = ArpUbutumwa{}
	arp.Init(arpbuffer)

	if arp.hardwareUbwoko == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressIngano == 6 && arp.protocoladdressIngano == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MGucapa([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Gucapa(arp.protocol)
			arpconsole.MGucapa([]byte(":"))
			arpconsole.MUnsignedinteger64Gucapa(uint64(arp.destinationmacaddress))
			arpconsole.MGucapa([]byte(":"))
			arpconsole.MUnsignedinteger16Gucapa(arp.icyowifuza)
			arpconsole.MGucapa([]byte(":"))
			arpconsole.MUnsignedinteger64Gucapa(handler.Getmacaddress())

			switch arp.icyowifuza {
			case 0x0100:

				if self.Getmacfromcache(arp.inkomokoipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.inkomokoipaddress
						self.Maccache[self.numbercacheentry] = arp.inkomokomacaddress
						self.numbercacheentry++
					}
				}
				arp.icyowifuza = 0x0200
				arp.destinationipaddress = arp.inkomokoipaddress
				arp.destinationmacaddress = arp.inkomokomacaddress
				arp.inkomokoipaddress = uint32(handler.Getipaddress())
				arp.inkomokomacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MGucapa(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.inkomokoipaddress
					self.Maccache[self.numbercacheentry] = arp.inkomokomacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipurusobebyteorder uint32) {

	var arp ArpUbutumwa = ArpUbutumwa{}
	arp.hardwareUbwoko = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressIngano = 6
	arp.protocoladdressIngano = 4
	arp.icyowifuza = 0x0200

	arp.inkomokoipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipurusobebyteorder)
	arp.destinationipaddress = Ipurusobebyteorder
	arpconsole.MGucapaxy([]byte("broad mac"), 0, 15)

	arp.inkomokomacaddress = handler.Getmacaddress()

	var arpbuffer ArpUbutumwabuffer = ArpUbutumwabuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgIngano)
}
func (self *Arpprovider) Requestmacaddress(Ipurusobebyteorder uint32) {

	var arp ArpUbutumwa = ArpUbutumwa{}
	arp.hardwareUbwoko = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressIngano = 6
	arp.protocoladdressIngano = 4
	arp.icyowifuza = 0x0100

	arp.inkomokomacaddress = handler.Getmacaddress()
	arp.inkomokoipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipurusobebyteorder

	var arpbuffer ArpUbutumwabuffer = ArpUbutumwabuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgIngano)
}
func (self *Arpprovider) TestGucapa(data *[]byte, ingano uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MGucapaxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalGucapa(buffer_2[i])
		arpconsole.MGucapa([]byte(":"))
	}
	arpconsole.MGucapa([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipurusobebyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MGucapa(([]byte)("["))
		arpconsole.MUnsignedinteger32Gucapa(self.Ipcache[i])
		arpconsole.MGucapa(([]byte)(":"))
		arpconsole.MUnsignedinteger32Gucapa(Ipurusobebyteorder)
		arpconsole.MGucapa(([]byte)(":"))
		arpconsole.MGucapa(([]byte)(":"))
		arpconsole.MUnsignedinteger64Gucapa(self.Maccache[i])
		arpconsole.MGucapa(([]byte)("]\n"))

		if self.Ipcache[i] == Ipurusobebyteorder {
			arpconsole.MGucapa([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipurusobebyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipurusobebyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipurusobebyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipurusobebyteorder)

	}

	return result
}
