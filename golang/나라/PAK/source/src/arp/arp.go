package arp

import . "unsafe"
import . "console"
import . "ایتھرنیٹframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpپیغامbuffer struct {
	ہارڈویئرنوعیت		[2]byte
	protocol		[2]byte
	ہارڈویئرaddressحجم	byte
	protocoladdressحجم	byte
	کمانڈ			[2]byte

	مصدرmacaddress		[6]byte
	مصدرipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgحجم uint32 = (64+92+64)/8 + 2

type Arpپیغام struct {
	ہارڈویئرنوعیت		uint16
	protocol		uint16
	ہارڈویئرaddressحجم	uint8
	protocoladdressحجم	uint8
	کمانڈ			uint16

	مصدرmacaddress		uint64
	مصدرipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpپیغام) Init(buffer_2 *Arpپیغامbuffer) {

	self.ہارڈویئرنوعیت = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.ہارڈویئرنوعیت))
	self.protocol = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.protocol))
	self.ہارڈویئرaddressحجم = byte(buffer_2.ہارڈویئرaddressحجم)
	self.protocoladdressحجم = byte(buffer_2.protocoladdressحجم)
	self.کمانڈ = Unsignedinteger16r(Aلڑیtounsignedinteger16(buffer_2.کمانڈ))

	self.مصدرmacaddress = Unsignedinteger48r(Aلڑیtounsignedinteger48(buffer_2.مصدرmacaddress))
	self.مصدرipaddress = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer_2.مصدرipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Aلڑیtounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpپیغام) Sسیٹbuffer(buffer_2 *Arpپیغامbuffer) {
	buffer_2.ہارڈویئرنوعیت = Unsignedinteger16toلڑی(self.ہارڈویئرنوعیت)
	buffer_2.protocol = Unsignedinteger16toلڑی(self.protocol)
	buffer_2.ہارڈویئرaddressحجم = uint8(self.ہارڈویئرaddressحجم)
	buffer_2.protocoladdressحجم = uint8(self.protocoladdressحجم)

	buffer_2.کمانڈ = Unsignedinteger16toلڑی(self.کمانڈ)
	buffer_2.مصدرmacaddress = Unsignedinteger48toلڑی(self.مصدرmacaddress)
	buffer_2.مصدرipaddress = Unsignedinteger32toلڑی(self.مصدرipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toلڑی(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toلڑی(self.destinationipaddress)
}

type Arpایتھرنیٹframehandler struct {
	Tایتھرنیٹframehandler
}

var arpprovider Arpprovider
var ایتھرنیٹframeprovider Tایتھرنیٹframeprovider

func (self *Arpایتھرنیٹframehandler) Oایتھرنیٹframereceivewhen(dataپؤائنٹر uintptr, حجم int) bool {
	arpconsole.Mچھاپیںxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oایتھرنیٹframereceivewhen(dataپؤائنٹر, uint32(حجم))

}
func (self *Arpایتھرنیٹframehandler) Send(destinationmacbe uint64, dataپؤائنٹر uintptr, حجم uint32) {
	arpconsole.Mچھاپیںxy([]byte("arp send:"), 0, 24)
	var ایتھرنیٹنوعیتbe = Unsignedinteger16r(0x0806)
	self.Tایتھرنیٹframehandler.Framesend(destinationmacbe, ایتھرنیٹنوعیتbe, dataپؤائنٹر, حجم)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	Iایتھرنیٹframehandler
}

var handler Iایتھرنیٹframehandler

func (self *Arpprovider) Init(backend Tایتھرنیٹframeprovider, userhandler Iایتھرنیٹframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sسیٹhandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Oایتھرنیٹframereceivewhen(dataپؤائنٹر uintptr, حجم uint32) bool {

	if حجم < arpmesgحجم {
		return false
	}
	var arpbuffer *Arpپیغامbuffer = (*Arpپیغامbuffer)(Pointer(dataپؤائنٹر))
	var arp Arpپیغام = Arpپیغام{}
	arp.Init(arpbuffer)

	if arp.ہارڈویئرنوعیت == 0x0100 {

		if arp.protocol == 0x0008 && arp.ہارڈویئرaddressحجم == 6 && arp.protocoladdressحجم == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.Mچھاپیں([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16چھاپیں(arp.protocol)
			arpconsole.Mچھاپیں([]byte(":"))
			arpconsole.MUnsignedinteger64چھاپیں(uint64(arp.destinationmacaddress))
			arpconsole.Mچھاپیں([]byte(":"))
			arpconsole.MUnsignedinteger16چھاپیں(arp.کمانڈ)
			arpconsole.Mچھاپیں([]byte(":"))
			arpconsole.MUnsignedinteger64چھاپیں(handler.Getmacaddress())

			switch arp.کمانڈ {
			case 0x0100:

				if self.Getmacfromcache(arp.مصدرipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.مصدرipaddress
						self.Maccache[self.numbercacheentry] = arp.مصدرmacaddress
						self.numbercacheentry++
					}
				}
				arp.کمانڈ = 0x0200
				arp.destinationipaddress = arp.مصدرipaddress
				arp.destinationmacaddress = arp.مصدرmacaddress
				arp.مصدرipaddress = uint32(handler.Getipaddress())
				arp.مصدرmacaddress = handler.Getmacaddress()
				arp.Sسیٹbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.Mچھاپیں(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.مصدرipaddress
					self.Maccache[self.numbercacheentry] = arp.مصدرmacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipنیٹورکbyteorder uint32) {

	var arp Arpپیغام = Arpپیغام{}
	arp.ہارڈویئرنوعیت = 0x0100
	arp.protocol = 0x0008
	arp.ہارڈویئرaddressحجم = 6
	arp.protocoladdressحجم = 4
	arp.کمانڈ = 0x0200

	arp.مصدرipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipنیٹورکbyteorder)
	arp.destinationipaddress = Ipنیٹورکbyteorder
	arpconsole.Mچھاپیںxy([]byte("broad mac"), 0, 15)

	arp.مصدرmacaddress = handler.Getmacaddress()

	var arpbuffer Arpپیغامbuffer = Arpپیغامbuffer{}
	arp.Sسیٹbuffer(&arpbuffer)

	var پؤائنٹر uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, پؤائنٹر, arpmesgحجم)
}
func (self *Arpprovider) Requestmacaddress(Ipنیٹورکbyteorder uint32) {

	var arp Arpپیغام = Arpپیغام{}
	arp.ہارڈویئرنوعیت = 0x0100

	arp.protocol = 0x0008
	arp.ہارڈویئرaddressحجم = 6
	arp.protocoladdressحجم = 4
	arp.کمانڈ = 0x0100

	arp.مصدرmacaddress = handler.Getmacaddress()
	arp.مصدرipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipنیٹورکbyteorder

	var arpbuffer Arpپیغامbuffer = Arpپیغامbuffer{}
	arp.Sسیٹbuffer(&arpbuffer)

	var پؤائنٹر uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, پؤائنٹر, arpmesgحجم)
}
func (self *Arpprovider) Tٹیسٹچھاپیں(data *[]byte, حجم uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.Mچھاپیںxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalچھاپیں(buffer_2[i])
		arpconsole.Mچھاپیں([]byte(":"))
	}
	arpconsole.Mچھاپیں([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipنیٹورکbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.Mچھاپیں(([]byte)("["))
		arpconsole.MUnsignedinteger32چھاپیں(self.Ipcache[i])
		arpconsole.Mچھاپیں(([]byte)(":"))
		arpconsole.MUnsignedinteger32چھاپیں(Ipنیٹورکbyteorder)
		arpconsole.Mچھاپیں(([]byte)(":"))
		arpconsole.Mچھاپیں(([]byte)(":"))
		arpconsole.MUnsignedinteger64چھاپیں(self.Maccache[i])
		arpconsole.Mچھاپیں(([]byte)("]\n"))

		if self.Ipcache[i] == Ipنیٹورکbyteorder {
			arpconsole.Mچھاپیں([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipنیٹورکbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipنیٹورکbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipنیٹورکbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipنیٹورکbyteorder)

	}

	return result
}
