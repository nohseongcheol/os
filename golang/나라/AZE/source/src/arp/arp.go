/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "eternetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpİsmarıcbuffer struct {
	hardwareNöv		[2]byte
	protocol		[2]byte
	hardwareaddressBöyüklük	byte
	protocoladdressBöyüklük	byte
	əmr			[2]byte

	mənbəmacaddress		[6]byte
	mənbəipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgBöyüklük uint32 = (64+92+64)/8 + 2

type Arpİsmarıc struct {
	hardwareNöv		uint16
	protocol		uint16
	hardwareaddressBöyüklük	uint8
	protocoladdressBöyüklük	uint8
	əmr			uint16

	mənbəmacaddress		uint64
	mənbəipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpİsmarıc) Init(buffer_2 *Arpİsmarıcbuffer) {

	self.hardwareNöv = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwareNöv))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardwareaddressBöyüklük = byte(buffer_2.hardwareaddressBöyüklük)
	self.protocoladdressBöyüklük = byte(buffer_2.protocoladdressBöyüklük)
	self.əmr = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.əmr))

	self.mənbəmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.mənbəmacaddress))
	self.mənbəipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.mənbəipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpİsmarıc) Setbuffer(buffer_2 *Arpİsmarıcbuffer) {
	buffer_2.hardwareNöv = Unsignedinteger16toarray(self.hardwareNöv)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardwareaddressBöyüklük = uint8(self.hardwareaddressBöyüklük)
	buffer_2.protocoladdressBöyüklük = uint8(self.protocoladdressBöyüklük)

	buffer_2.əmr = Unsignedinteger16toarray(self.əmr)
	buffer_2.mənbəmacaddress = Unsignedinteger48toarray(self.mənbəmacaddress)
	buffer_2.mənbəipaddress = Unsignedinteger32toarray(self.mənbəipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type ArpEternetframehandler struct {
	TEternetframehandler
}

var arpprovider Arpprovider
var eternetframeprovider TEternetframeprovider

func (self *ArpEternetframehandler) Eternetframereceivewhen(datapointer uintptr, böyüklük int) bool {
	arpconsole.MÇapEtxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Eternetframereceivewhen(datapointer, uint32(böyüklük))

}
func (self *ArpEternetframehandler) Send(destinationmacbe uint64, datapointer uintptr, böyüklük uint32) {
	arpconsole.MÇapEtxy([]byte("arp send:"), 0, 24)
	var eternetNövbe = Unsignedinteger16r(0x0806)
	self.TEternetframehandler.Framesend(destinationmacbe, eternetNövbe, datapointer, böyüklük)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEternetframehandler
}

var handler IEternetframehandler

func (self *Arpprovider) Init(backend TEternetframeprovider, userhandler IEternetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Eternetframereceivewhen(datapointer uintptr, böyüklük uint32) bool {

	if böyüklük < arpmesgBöyüklük {
		return false
	}
	var arpbuffer *Arpİsmarıcbuffer = (*Arpİsmarıcbuffer)(Pointer(datapointer))
	var arp Arpİsmarıc = Arpİsmarıc{}
	arp.Init(arpbuffer)

	if arp.hardwareNöv == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressBöyüklük == 6 && arp.protocoladdressBöyüklük == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MÇapEt([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16ÇapEt(arp.protocol)
			arpconsole.MÇapEt([]byte(":"))
			arpconsole.MUnsignedinteger64ÇapEt(uint64(arp.destinationmacaddress))
			arpconsole.MÇapEt([]byte(":"))
			arpconsole.MUnsignedinteger16ÇapEt(arp.əmr)
			arpconsole.MÇapEt([]byte(":"))
			arpconsole.MUnsignedinteger64ÇapEt(handler.Getmacaddress())

			switch arp.əmr {
			case 0x0100:

				if self.Getmacfromcache(arp.mənbəipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.mənbəipaddress
						self.Maccache[self.numbercacheentry] = arp.mənbəmacaddress
						self.numbercacheentry++
					}
				}
				arp.əmr = 0x0200
				arp.destinationipaddress = arp.mənbəipaddress
				arp.destinationmacaddress = arp.mənbəmacaddress
				arp.mənbəipaddress = uint32(handler.Getipaddress())
				arp.mənbəmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MÇapEt(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.mənbəipaddress
					self.Maccache[self.numbercacheentry] = arp.mənbəmacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpŞəbəkəbyteorder uint32) {

	var arp Arpİsmarıc = Arpİsmarıc{}
	arp.hardwareNöv = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressBöyüklük = 6
	arp.protocoladdressBöyüklük = 4
	arp.əmr = 0x0200

	arp.mənbəipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpŞəbəkəbyteorder)
	arp.destinationipaddress = IpŞəbəkəbyteorder
	arpconsole.MÇapEtxy([]byte("broad mac"), 0, 15)

	arp.mənbəmacaddress = handler.Getmacaddress()

	var arpbuffer Arpİsmarıcbuffer = Arpİsmarıcbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgBöyüklük)
}
func (self *Arpprovider) Requestmacaddress(IpŞəbəkəbyteorder uint32) {

	var arp Arpİsmarıc = Arpİsmarıc{}
	arp.hardwareNöv = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressBöyüklük = 6
	arp.protocoladdressBöyüklük = 4
	arp.əmr = 0x0100

	arp.mənbəmacaddress = handler.Getmacaddress()
	arp.mənbəipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpŞəbəkəbyteorder

	var arpbuffer Arpİsmarıcbuffer = Arpİsmarıcbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgBöyüklük)
}
func (self *Arpprovider) TestÇapEt(data *[]byte, böyüklük uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MÇapEtxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalÇapEt(buffer_2[i])
		arpconsole.MÇapEt([]byte(":"))
	}
	arpconsole.MÇapEt([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpŞəbəkəbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MÇapEt(([]byte)("["))
		arpconsole.MUnsignedinteger32ÇapEt(self.Ipcache[i])
		arpconsole.MÇapEt(([]byte)(":"))
		arpconsole.MUnsignedinteger32ÇapEt(IpŞəbəkəbyteorder)
		arpconsole.MÇapEt(([]byte)(":"))
		arpconsole.MÇapEt(([]byte)(":"))
		arpconsole.MUnsignedinteger64ÇapEt(self.Maccache[i])
		arpconsole.MÇapEt(([]byte)("]\n"))

		if self.Ipcache[i] == IpŞəbəkəbyteorder {
			arpconsole.MÇapEt([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpŞəbəkəbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpŞəbəkəbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpŞəbəkəbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpŞəbəkəbyteorder)

	}

	return result
}
