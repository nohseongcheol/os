package arp

import . "unsafe"
import . "console"
import . "אתרנטframe"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpהודעהbuffer struct {
	חומרהסוג		[2]byte
	protocol		[2]byte
	חומרהaddressגודל	byte
	protocoladdressגודל	byte
	פקודה			[2]byte

	מקורmacaddress	[6]byte
	מקורipaddress	[4]byte
	יעדmacaddress	[6]byte
	יעדipaddress	[4]byte
}

var arpmesgגודל uint32 = (64+92+64)/8 + 2

type Arpהודעה struct {
	חומרהסוג		uint16
	protocol		uint16
	חומרהaddressגודל	uint8
	protocoladdressגודל	uint8
	פקודה			uint16

	מקורmacaddress	uint64
	מקורipaddress	uint32
	יעדmacaddress	uint64
	יעדipaddress	uint32
}

func (self *Arpהודעה) Init(buffer_2 *Arpהודעהbuffer) {

	self.חומרהסוג = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.חומרהסוג))
	self.protocol = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.protocol))
	self.חומרהaddressגודל = byte(buffer_2.חומרהaddressגודל)
	self.protocoladdressגודל = byte(buffer_2.protocoladdressגודל)
	self.פקודה = Unsignedinteger16r(Aמערךtounsignedinteger16(buffer_2.פקודה))

	self.מקורmacaddress = Unsignedinteger48r(Aמערךtounsignedinteger48(buffer_2.מקורmacaddress))
	self.מקורipaddress = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer_2.מקורipaddress))
	self.יעדmacaddress = Unsignedinteger48r(Aמערךtounsignedinteger48(buffer_2.יעדmacaddress))
	self.יעדipaddress = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer_2.יעדipaddress))
}
func (self *Arpהודעה) Sקבעbuffer(buffer_2 *Arpהודעהbuffer) {
	buffer_2.חומרהסוג = Unsignedinteger16toמערך(self.חומרהסוג)
	buffer_2.protocol = Unsignedinteger16toמערך(self.protocol)
	buffer_2.חומרהaddressגודל = uint8(self.חומרהaddressגודל)
	buffer_2.protocoladdressגודל = uint8(self.protocoladdressגודל)

	buffer_2.פקודה = Unsignedinteger16toמערך(self.פקודה)
	buffer_2.מקורmacaddress = Unsignedinteger48toמערך(self.מקורmacaddress)
	buffer_2.מקורipaddress = Unsignedinteger32toמערך(self.מקורipaddress)
	buffer_2.יעדmacaddress = Unsignedinteger48toמערך(self.יעדmacaddress)
	buffer_2.יעדipaddress = Unsignedinteger32toמערך(self.יעדipaddress)
}

type Arpאתרנטframehandler struct {
	Tאתרנטframehandler
}

var arpprovider Arpprovider
var אתרנטframeprovider Tאתרנטframeprovider

func (self *Arpאתרנטframehandler) Oאתרנטframereceivewhen(dataסמן uintptr, גודל int) bool {
	arpconsole.Mהדפסהxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Oאתרנטframereceivewhen(dataסמן, uint32(גודל))

}
func (self *Arpאתרנטframehandler) Sשלח(יעדmacbe uint64, dataסמן uintptr, גודל uint32) {
	arpconsole.Mהדפסהxy([]byte("arp send:"), 0, 24)
	var אתרנטסוגbe = Unsignedinteger16r(0x0806)
	self.Tאתרנטframehandler.Frameשלח(יעדmacbe, אתרנטסוגbe, dataסמן, גודל)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	מספרcacheentry	int

	handler	Iאתרנטframehandler
}

var handler Iאתרנטframehandler

func (self *Arpprovider) Init(backend Tאתרנטframeprovider, userhandler Iאתרנטframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sקבעhandler(userhandler, 0x0806)
	self.מספרcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Oאתרנטframereceivewhen(dataסמן uintptr, גודל uint32) bool {

	if גודל < arpmesgגודל {
		return false
	}
	var arpbuffer *Arpהודעהbuffer = (*Arpהודעהbuffer)(Pointer(dataסמן))
	var arp Arpהודעה = Arpהודעה{}
	arp.Init(arpbuffer)

	if arp.חומרהסוג == 0x0100 {

		if arp.protocol == 0x0008 && arp.חומרהaddressגודל == 6 && arp.protocoladdressגודל == 4 && uint64(arp.יעדipaddress) == handler.Getipaddress() {

			arpconsole.Mהדפסה([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16הדפסה(arp.protocol)
			arpconsole.Mהדפסה([]byte(":"))
			arpconsole.MUnsignedinteger64הדפסה(uint64(arp.יעדmacaddress))
			arpconsole.Mהדפסה([]byte(":"))
			arpconsole.MUnsignedinteger16הדפסה(arp.פקודה)
			arpconsole.Mהדפסה([]byte(":"))
			arpconsole.MUnsignedinteger64הדפסה(handler.Getmacaddress())

			switch arp.פקודה {
			case 0x0100:

				if self.Getmacfromcache(arp.מקורipaddress) == 0xFFFFFFFFFFFF {
					if self.מספרcacheentry < 128 {
						self.Ipcache[self.מספרcacheentry] = arp.מקורipaddress
						self.Maccache[self.מספרcacheentry] = arp.מקורmacaddress
						self.מספרcacheentry++
					}
				}
				arp.פקודה = 0x0200
				arp.יעדipaddress = arp.מקורipaddress
				arp.יעדmacaddress = arp.מקורmacaddress
				arp.מקורipaddress = uint32(handler.Getipaddress())
				arp.מקורmacaddress = handler.Getmacaddress()
				arp.Sקבעbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.Mהדפסה(([]byte)("self.numCacheEntries"))

				if self.מספרcacheentry < 128 {
					self.Ipcache[self.מספרcacheentry] = arp.מקורipaddress
					self.Maccache[self.מספרcacheentry] = arp.מקורmacaddress
					self.מספרcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipרשתbyteorder uint32) {

	var arp Arpהודעה = Arpהודעה{}
	arp.חומרהסוג = 0x0100
	arp.protocol = 0x0008
	arp.חומרהaddressגודל = 6
	arp.protocoladdressגודל = 4
	arp.פקודה = 0x0200

	arp.מקורipaddress = uint32(handler.Getipaddress())

	arp.יעדmacaddress = self.Resolve(Ipרשתbyteorder)
	arp.יעדipaddress = Ipרשתbyteorder
	arpconsole.Mהדפסהxy([]byte("broad mac"), 0, 15)

	arp.מקורmacaddress = handler.Getmacaddress()

	var arpbuffer Arpהודעהbuffer = Arpהודעהbuffer{}
	arp.Sקבעbuffer(&arpbuffer)

	var סמן uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sשלח(arp.יעדmacaddress, סמן, arpmesgגודל)
}
func (self *Arpprovider) Requestmacaddress(Ipרשתbyteorder uint32) {

	var arp Arpהודעה = Arpהודעה{}
	arp.חומרהסוג = 0x0100

	arp.protocol = 0x0008
	arp.חומרהaddressגודל = 6
	arp.protocoladdressגודל = 4
	arp.פקודה = 0x0100

	arp.מקורmacaddress = handler.Getmacaddress()
	arp.מקורipaddress = uint32(handler.Getipaddress())

	arp.יעדmacaddress = 0xFFFFFFFFFFFF
	arp.יעדipaddress = Ipרשתbyteorder

	var arpbuffer Arpהודעהbuffer = Arpהודעהbuffer{}
	arp.Sקבעbuffer(&arpbuffer)

	var סמן uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sשלח(arp.יעדmacaddress, סמן, arpmesgגודל)
}
func (self *Arpprovider) Tבדיקההדפסה(data *[]byte, גודל uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.Mהדפסהxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalהדפסה(buffer_2[i])
		arpconsole.Mהדפסה([]byte(":"))
	}
	arpconsole.Mהדפסה([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipרשתbyteorder uint32) uint64 {
	for i := 0; i < self.מספרcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.Mהדפסה(([]byte)("["))
		arpconsole.MUnsignedinteger32הדפסה(self.Ipcache[i])
		arpconsole.Mהדפסה(([]byte)(":"))
		arpconsole.MUnsignedinteger32הדפסה(Ipרשתbyteorder)
		arpconsole.Mהדפסה(([]byte)(":"))
		arpconsole.Mהדפסה(([]byte)(":"))
		arpconsole.MUnsignedinteger64הדפסה(self.Maccache[i])
		arpconsole.Mהדפסה(([]byte)("]\n"))

		if self.Ipcache[i] == Ipרשתbyteorder {
			arpconsole.Mהדפסה([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipרשתbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipרשתbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipרשתbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipרשתbyteorder)

	}

	return result
}
