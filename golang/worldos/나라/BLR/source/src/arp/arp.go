/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "лякальнаясеткаФрэйм"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpпаведамленнеbuffer struct {
	апаратураТып		[2]byte
	protocol		[2]byte
	апаратураaddressПамер	byte
	protocoladdressПамер	byte
	загад			[2]byte

	крыніцаmacaddress	[6]byte
	крыніцаipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgПамер uint32 = (64+92+64)/8 + 2

type Arpпаведамленне struct {
	апаратураТып		uint16
	protocol		uint16
	апаратураaddressПамер	uint8
	protocoladdressПамер	uint8
	загад			uint16

	крыніцаmacaddress	uint64
	крыніцаipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpпаведамленне) Init(buffer_2 *Arpпаведамленнеbuffer) {

	self.апаратураТып = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.апаратураТып))
	self.protocol = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.protocol))
	self.апаратураaddressПамер = byte(buffer_2.апаратураaddressПамер)
	self.protocoladdressПамер = byte(buffer_2.protocoladdressПамер)
	self.загад = Unsignedinteger16r(Масіўtounsignedinteger16(buffer_2.загад))

	self.крыніцаmacaddress = Unsignedinteger48r(Масіўtounsignedinteger48(buffer_2.крыніцаmacaddress))
	self.крыніцаipaddress = Unsignedinteger32r(Масіўtounsignedinteger32(buffer_2.крыніцаipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Масіўtounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Масіўtounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpпаведамленне) Вызначанаbuffer(buffer_2 *Arpпаведамленнеbuffer) {
	buffer_2.апаратураТып = Unsignedinteger16toМасіў(self.апаратураТып)
	buffer_2.protocol = Unsignedinteger16toМасіў(self.protocol)
	buffer_2.апаратураaddressПамер = uint8(self.апаратураaddressПамер)
	buffer_2.protocoladdressПамер = uint8(self.protocoladdressПамер)

	buffer_2.загад = Unsignedinteger16toМасіў(self.загад)
	buffer_2.крыніцаmacaddress = Unsignedinteger48toМасіў(self.крыніцаmacaddress)
	buffer_2.крыніцаipaddress = Unsignedinteger32toМасіў(self.крыніцаipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toМасіў(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toМасіў(self.destinationipaddress)
}

type ArpЛякальнаясеткаФрэймhandler struct {
	TЛякальнаясеткаФрэймhandler
}

var arpprovider Arpprovider
var лякальнаясеткаФрэймprovider TЛякальнаясеткаФрэймprovider

func (self *ArpЛякальнаясеткаФрэймhandler) ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік uintptr, памер int) bool {
	arpconsole.MДрукавацьxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік, uint32(памер))

}
func (self *ArpЛякальнаясеткаФрэймhandler) Даслаць(destinationmacbe uint64, dataПаказальнік uintptr, памер uint32) {
	arpconsole.MДрукавацьxy([]byte("arp send:"), 0, 24)
	var лякальнаясеткаТыпbe = Unsignedinteger16r(0x0806)
	self.TЛякальнаясеткаФрэймhandler.ФрэймДаслаць(destinationmacbe, лякальнаясеткаТыпbe, dataПаказальнік, памер)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	нУМАРcacheentry	int

	handler	IЛякальнаясеткаФрэймhandler
}

var handler IЛякальнаясеткаФрэймhandler

func (self *Arpprovider) Init(backend TЛякальнаясеткаФрэймprovider, userhandler IЛякальнаясеткаФрэймhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Вызначанаhandler(userhandler, 0x0806)
	self.нУМАРcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) ЛякальнаясеткаФрэймreceivewhen(dataПаказальнік uintptr, памер uint32) bool {

	if памер < arpmesgПамер {
		return false
	}
	var arpbuffer *Arpпаведамленнеbuffer = (*Arpпаведамленнеbuffer)(Pointer(dataПаказальнік))
	var arp Arpпаведамленне = Arpпаведамленне{}
	arp.Init(arpbuffer)

	if arp.апаратураТып == 0x0100 {

		if arp.protocol == 0x0008 && arp.апаратураaddressПамер == 6 && arp.protocoladdressПамер == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MДрукаваць([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Друкаваць(arp.protocol)
			arpconsole.MДрукаваць([]byte(":"))
			arpconsole.MUnsignedinteger64Друкаваць(uint64(arp.destinationmacaddress))
			arpconsole.MДрукаваць([]byte(":"))
			arpconsole.MUnsignedinteger16Друкаваць(arp.загад)
			arpconsole.MДрукаваць([]byte(":"))
			arpconsole.MUnsignedinteger64Друкаваць(handler.Getmacaddress())

			switch arp.загад {
			case 0x0100:

				if self.Getmacfromcache(arp.крыніцаipaddress) == 0xFFFFFFFFFFFF {
					if self.нУМАРcacheentry < 128 {
						self.Ipcache[self.нУМАРcacheentry] = arp.крыніцаipaddress
						self.Maccache[self.нУМАРcacheentry] = arp.крыніцаmacaddress
						self.нУМАРcacheentry++
					}
				}
				arp.загад = 0x0200
				arp.destinationipaddress = arp.крыніцаipaddress
				arp.destinationmacaddress = arp.крыніцаmacaddress
				arp.крыніцаipaddress = uint32(handler.Getipaddress())
				arp.крыніцаmacaddress = handler.Getmacaddress()
				arp.Вызначанаbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MДрукаваць(([]byte)("self.numCacheEntries"))

				if self.нУМАРcacheentry < 128 {
					self.Ipcache[self.нУМАРcacheentry] = arp.крыніцаipaddress
					self.Maccache[self.нУМАРcacheentry] = arp.крыніцаmacaddress
					self.нУМАРcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpСеткаbyteorder uint32) {

	var arp Arpпаведамленне = Arpпаведамленне{}
	arp.апаратураТып = 0x0100
	arp.protocol = 0x0008
	arp.апаратураaddressПамер = 6
	arp.protocoladdressПамер = 4
	arp.загад = 0x0200

	arp.крыніцаipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpСеткаbyteorder)
	arp.destinationipaddress = IpСеткаbyteorder
	arpconsole.MДрукавацьxy([]byte("broad mac"), 0, 15)

	arp.крыніцаmacaddress = handler.Getmacaddress()

	var arpbuffer Arpпаведамленнеbuffer = Arpпаведамленнеbuffer{}
	arp.Вызначанаbuffer(&arpbuffer)

	var паказальнік uintptr = uintptr(Pointer(&arpbuffer))
	handler.Даслаць(arp.destinationmacaddress, паказальнік, arpmesgПамер)
}
func (self *Arpprovider) Requestmacaddress(IpСеткаbyteorder uint32) {

	var arp Arpпаведамленне = Arpпаведамленне{}
	arp.апаратураТып = 0x0100

	arp.protocol = 0x0008
	arp.апаратураaddressПамер = 6
	arp.protocoladdressПамер = 4
	arp.загад = 0x0100

	arp.крыніцаmacaddress = handler.Getmacaddress()
	arp.крыніцаipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpСеткаbyteorder

	var arpbuffer Arpпаведамленнеbuffer = Arpпаведамленнеbuffer{}
	arp.Вызначанаbuffer(&arpbuffer)

	var паказальнік uintptr = uintptr(Pointer(&arpbuffer))
	handler.Даслаць(arp.destinationmacaddress, паказальнік, arpmesgПамер)
}
func (self *Arpprovider) ПраверкаДрукаваць(data *[]byte, памер uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MДрукавацьxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalДрукаваць(buffer_2[i])
		arpconsole.MДрукаваць([]byte(":"))
	}
	arpconsole.MДрукаваць([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpСеткаbyteorder uint32) uint64 {
	for i := 0; i < self.нУМАРcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MДрукаваць(([]byte)("["))
		arpconsole.MUnsignedinteger32Друкаваць(self.Ipcache[i])
		arpconsole.MДрукаваць(([]byte)(":"))
		arpconsole.MUnsignedinteger32Друкаваць(IpСеткаbyteorder)
		arpconsole.MДрукаваць(([]byte)(":"))
		arpconsole.MДрукаваць(([]byte)(":"))
		arpconsole.MUnsignedinteger64Друкаваць(self.Maccache[i])
		arpconsole.MДрукаваць(([]byte)("]\n"))

		if self.Ipcache[i] == IpСеткаbyteorder {
			arpconsole.MДрукаваць([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpСеткаbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpСеткаbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpСеткаbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpСеткаbyteorder)

	}

	return result
}
