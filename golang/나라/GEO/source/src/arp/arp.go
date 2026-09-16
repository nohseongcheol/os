/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpშეტყობინებაbuffer struct {
	აპარატურატიპი		[2]byte
	protocol		[2]byte
	აპარატურაaddressზომა	byte
	protocoladdressზომა	byte
	ბრძანება		[2]byte

	წყაროmacaddress		[6]byte
	წყაროipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgზომა uint32 = (64+92+64)/8 + 2

type Arpშეტყობინება struct {
	აპარატურატიპი		uint16
	protocol		uint16
	აპარატურაaddressზომა	uint8
	protocoladdressზომა	uint8
	ბრძანება		uint16

	წყაროmacaddress		uint64
	წყაროipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpშეტყობინება) Init(buffer_2 *Arpშეტყობინებაbuffer) {

	self.აპარატურატიპი = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.აპარატურატიპი))
	self.protocol = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.protocol))
	self.აპარატურაaddressზომა = byte(buffer_2.აპარატურაaddressზომა)
	self.protocoladdressზომა = byte(buffer_2.protocoladdressზომა)
	self.ბრძანება = Unsignedinteger16r(Aმასივიtounsignedinteger16(buffer_2.ბრძანება))

	self.წყაროmacaddress = Unsignedinteger48r(Aმასივიtounsignedinteger48(buffer_2.წყაროmacaddress))
	self.წყაროipaddress = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer_2.წყაროipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Aმასივიtounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpშეტყობინება) Setbuffer(buffer_2 *Arpშეტყობინებაbuffer) {
	buffer_2.აპარატურატიპი = Unsignedinteger16toმასივი(self.აპარატურატიპი)
	buffer_2.protocol = Unsignedinteger16toმასივი(self.protocol)
	buffer_2.აპარატურაaddressზომა = uint8(self.აპარატურაaddressზომა)
	buffer_2.protocoladdressზომა = uint8(self.protocoladdressზომა)

	buffer_2.ბრძანება = Unsignedinteger16toმასივი(self.ბრძანება)
	buffer_2.წყაროmacaddress = Unsignedinteger48toმასივი(self.წყაროmacaddress)
	buffer_2.წყაროipaddress = Unsignedinteger32toმასივი(self.წყაროipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toმასივი(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toმასივი(self.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (self *Arpethernetframehandler) Ethernetframereceivewhen(dataკურსორი uintptr, ზომა int) bool {
	arpconsole.Mბეჭდვაxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(dataკურსორი, uint32(ზომა))

}
func (self *Arpethernetframehandler) Sგაგზავნა(destinationmacbe uint64, dataკურსორი uintptr, ზომა uint32) {
	arpconsole.Mბეჭდვაxy([]byte("arp send:"), 0, 24)
	var ethernetტიპიbe = Unsignedinteger16r(0x0806)
	self.TEthernetframehandler.Frameგაგზავნა(destinationmacbe, ethernetტიპიbe, dataკურსორი, ზომა)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	რიცხვიcacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (self *Arpprovider) Init(backend TEthernetframeprovider, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.რიცხვიcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernetframereceivewhen(dataკურსორი uintptr, ზომა uint32) bool {

	if ზომა < arpmesgზომა {
		return false
	}
	var arpbuffer *Arpშეტყობინებაbuffer = (*Arpშეტყობინებაbuffer)(Pointer(dataკურსორი))
	var arp Arpშეტყობინება = Arpშეტყობინება{}
	arp.Init(arpbuffer)

	if arp.აპარატურატიპი == 0x0100 {

		if arp.protocol == 0x0008 && arp.აპარატურაaddressზომა == 6 && arp.protocoladdressზომა == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.Mბეჭდვა([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16ბეჭდვა(arp.protocol)
			arpconsole.Mბეჭდვა([]byte(":"))
			arpconsole.MUnsignedinteger64ბეჭდვა(uint64(arp.destinationmacaddress))
			arpconsole.Mბეჭდვა([]byte(":"))
			arpconsole.MUnsignedinteger16ბეჭდვა(arp.ბრძანება)
			arpconsole.Mბეჭდვა([]byte(":"))
			arpconsole.MUnsignedinteger64ბეჭდვა(handler.Getmacaddress())

			switch arp.ბრძანება {
			case 0x0100:

				if self.Getmacfromcache(arp.წყაროipaddress) == 0xFFFFFFFFFFFF {
					if self.რიცხვიcacheentry < 128 {
						self.Ipcache[self.რიცხვიcacheentry] = arp.წყაროipaddress
						self.Maccache[self.რიცხვიcacheentry] = arp.წყაროmacaddress
						self.რიცხვიcacheentry++
					}
				}
				arp.ბრძანება = 0x0200
				arp.destinationipaddress = arp.წყაროipaddress
				arp.destinationmacaddress = arp.წყაროmacaddress
				arp.წყაროipaddress = uint32(handler.Getipaddress())
				arp.წყაროmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.Mბეჭდვა(([]byte)("self.numCacheEntries"))

				if self.რიცხვიcacheentry < 128 {
					self.Ipcache[self.რიცხვიcacheentry] = arp.წყაროipaddress
					self.Maccache[self.რიცხვიcacheentry] = arp.წყაროmacaddress
					self.რიცხვიcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipქსელიbyteorder uint32) {

	var arp Arpშეტყობინება = Arpშეტყობინება{}
	arp.აპარატურატიპი = 0x0100
	arp.protocol = 0x0008
	arp.აპარატურაaddressზომა = 6
	arp.protocoladdressზომა = 4
	arp.ბრძანება = 0x0200

	arp.წყაროipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipქსელიbyteorder)
	arp.destinationipaddress = Ipქსელიbyteorder
	arpconsole.Mბეჭდვაxy([]byte("broad mac"), 0, 15)

	arp.წყაროmacaddress = handler.Getmacaddress()

	var arpbuffer Arpშეტყობინებაbuffer = Arpშეტყობინებაbuffer{}
	arp.Setbuffer(&arpbuffer)

	var კურსორი uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sგაგზავნა(arp.destinationmacaddress, კურსორი, arpmesgზომა)
}
func (self *Arpprovider) Requestmacaddress(Ipქსელიbyteorder uint32) {

	var arp Arpშეტყობინება = Arpშეტყობინება{}
	arp.აპარატურატიპი = 0x0100

	arp.protocol = 0x0008
	arp.აპარატურაaddressზომა = 6
	arp.protocoladdressზომა = 4
	arp.ბრძანება = 0x0100

	arp.წყაროmacaddress = handler.Getmacaddress()
	arp.წყაროipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipქსელიbyteorder

	var arpbuffer Arpშეტყობინებაbuffer = Arpშეტყობინებაbuffer{}
	arp.Setbuffer(&arpbuffer)

	var კურსორი uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sგაგზავნა(arp.destinationmacaddress, კურსორი, arpmesgზომა)
}
func (self *Arpprovider) Testბეჭდვა(data *[]byte, ზომა uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.Mბეჭდვაxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalბეჭდვა(buffer_2[i])
		arpconsole.Mბეჭდვა([]byte(":"))
	}
	arpconsole.Mბეჭდვა([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipქსელიbyteorder uint32) uint64 {
	for i := 0; i < self.რიცხვიcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.Mბეჭდვა(([]byte)("["))
		arpconsole.MUnsignedinteger32ბეჭდვა(self.Ipcache[i])
		arpconsole.Mბეჭდვა(([]byte)(":"))
		arpconsole.MUnsignedinteger32ბეჭდვა(Ipქსელიbyteorder)
		arpconsole.Mბეჭდვა(([]byte)(":"))
		arpconsole.Mბეჭდვა(([]byte)(":"))
		arpconsole.MUnsignedinteger64ბეჭდვა(self.Maccache[i])
		arpconsole.Mბეჭდვა(([]byte)("]\n"))

		if self.Ipcache[i] == Ipქსელიbyteorder {
			arpconsole.Mბეჭდვა([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipქსელიbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipქსელიbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipქსელიbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipქსელიbyteorder)

	}

	return result
}
