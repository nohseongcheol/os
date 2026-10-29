/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetเฟรม"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpmessagebuffer struct {
	hardwareประเภท		[2]byte
	protocol		[2]byte
	hardwareaddressขนาด	byte
	protocoladdressขนาด	byte
	command			[2]byte

	sourcemacaddress	[6]byte
	sourceipaddress		[4]byte
	ปลายทางmacaddress	[6]byte
	ปลายทางipaddress	[4]byte
}

var arpmesgขนาด uint32 = (64+92+64)/8 + 2

type Arpmessage struct {
	hardwareประเภท		uint16
	protocol		uint16
	hardwareaddressขนาด	uint8
	protocoladdressขนาด	uint8
	command			uint16

	sourcemacaddress	uint64
	sourceipaddress		uint32
	ปลายทางmacaddress	uint64
	ปลายทางipaddress	uint32
}

func (self *Arpmessage) Init(buffer_2 *Arpmessagebuffer) {

	self.hardwareประเภท = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwareประเภท))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddressขนาด = byte(buffer_2.hardwareaddressขนาด)
	self.protocoladdressขนาด = byte(buffer_2.protocoladdressขนาด)
	self.command = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.command))

	self.sourcemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.sourcemacaddress))
	self.sourceipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.sourceipaddress))
	self.ปลายทางmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.ปลายทางmacaddress))
	self.ปลายทางipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.ปลายทางipaddress))
}
func (self *Arpmessage) Sกำหนดbuffer(buffer_2 *Arpmessagebuffer) {
	buffer_2.hardwareประเภท = Unsignedinteger16toarray(self.hardwareประเภท)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddressขนาด = uint8(self.hardwareaddressขนาด)
	buffer_2.protocoladdressขนาด = uint8(self.protocoladdressขนาด)

	buffer_2.command = Unsignedinteger16toarray(self.command)
	buffer_2.sourcemacaddress = Unsignedinteger48toarray(self.sourcemacaddress)
	buffer_2.sourceipaddress = Unsignedinteger32toarray(self.sourceipaddress)
	buffer_2.ปลายทางmacaddress = Unsignedinteger48toarray(self.ปลายทางmacaddress)
	buffer_2.ปลายทางipaddress = Unsignedinteger32toarray(self.ปลายทางipaddress)
}

type Arpethernetเฟรมhandler struct {
	TEthernetเฟรมhandler
}

var arpprovider Arpprovider
var ethernetเฟรมprovider TEthernetเฟรมprovider

func (self *Arpethernetเฟรมhandler) Ethernetเฟรมreceivewhen(datapointer uintptr, ขนาด int) bool {
	arpconsole.MPrintxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetเฟรมreceivewhen(datapointer, uint32(ขนาด))

}
func (self *Arpethernetเฟรมhandler) Send(ปลายทางmacbe uint64, datapointer uintptr, ขนาด uint32) {
	arpconsole.MPrintxy([]byte("arp send:"), 0, 24)
	var ethernetประเภทbe = Unsignedinteger16r(0x0806)
	self.TEthernetเฟรมhandler.Sเฟรมsend(ปลายทางmacbe, ethernetประเภทbe, datapointer, ขนาด)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetเฟรมhandler
}

var handler IEthernetเฟรมhandler

func (self *Arpprovider) Init(backend TEthernetเฟรมprovider, userhandler IEthernetเฟรมhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sกำหนดhandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernetเฟรมreceivewhen(datapointer uintptr, ขนาด uint32) bool {

	if ขนาด < arpmesgขนาด {
		return false
	}
	var arpbuffer *Arpmessagebuffer = (*Arpmessagebuffer)(Pointer(datapointer))
	var arp Arpmessage = Arpmessage{}
	arp.Init(arpbuffer)

	if arp.hardwareประเภท == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressขนาด == 6 && arp.protocoladdressขนาด == 4 && uint64(arp.ปลายทางipaddress) == handler.Getipaddress() {

			arpconsole.MPrint([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16print(arp.protocol)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(uint64(arp.ปลายทางmacaddress))
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger16print(arp.command)
			arpconsole.MPrint([]byte(":"))
			arpconsole.MUnsignedinteger64print(handler.Getmacaddress())

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
				arp.ปลายทางipaddress = arp.sourceipaddress
				arp.ปลายทางmacaddress = arp.sourcemacaddress
				arp.sourceipaddress = uint32(handler.Getipaddress())
				arp.sourcemacaddress = handler.Getmacaddress()
				arp.Sกำหนดbuffer(arpbuffer)

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

func (self *Arpprovider) Broadcastmacaddress(Ipnetworkbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.hardwareประเภท = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressขนาด = 6
	arp.protocoladdressขนาด = 4
	arp.command = 0x0200

	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.ปลายทางmacaddress = self.Resolve(Ipnetworkbyteorder)
	arp.ปลายทางipaddress = Ipnetworkbyteorder
	arpconsole.MPrintxy([]byte("broad mac"), 0, 15)

	arp.sourcemacaddress = handler.Getmacaddress()

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Sกำหนดbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.ปลายทางmacaddress, pointer, arpmesgขนาด)
}
func (self *Arpprovider) Requestmacaddress(Ipnetworkbyteorder uint32) {

	var arp Arpmessage = Arpmessage{}
	arp.hardwareประเภท = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressขนาด = 6
	arp.protocoladdressขนาด = 4
	arp.command = 0x0100

	arp.sourcemacaddress = handler.Getmacaddress()
	arp.sourceipaddress = uint32(handler.Getipaddress())

	arp.ปลายทางmacaddress = 0xFFFFFFFFFFFF
	arp.ปลายทางipaddress = Ipnetworkbyteorder

	var arpbuffer Arpmessagebuffer = Arpmessagebuffer{}
	arp.Sกำหนดbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.ปลายทางmacaddress, pointer, arpmesgขนาด)
}
func (self *Arpprovider) Tทดสอบprint(data *[]byte, ขนาด uint32) {
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
