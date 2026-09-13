package arp

import . "unsafe"
import . "консол"
import . "итернэтframe"
import . "util"

var arpКонсол TКонсол = TКонсол{}

type ArpМэдээbuffer struct {
	техникхангамжТөрөл		[2]byte
	protocol			[2]byte
	техникхангамжaddressХэмжээ	byte
	protocoladdressХэмжээ		byte
	тушаал				[2]byte

	эхmacaddress		[6]byte
	эхipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgХэмжээ uint32 = (64+92+64)/8 + 2

type ArpМэдээ struct {
	техникхангамжТөрөл		uint16
	protocol			uint16
	техникхангамжaddressХэмжээ	uint8
	protocoladdressХэмжээ		uint8
	тушаал				uint16

	эхmacaddress		uint64
	эхipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *ArpМэдээ) Init(buffer_2 *ArpМэдээbuffer) {

	self.техникхангамжТөрөл = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.техникхангамжТөрөл))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.техникхангамжaddressХэмжээ = byte(buffer_2.техникхангамжaddressХэмжээ)
	self.protocoladdressХэмжээ = byte(buffer_2.protocoladdressХэмжээ)
	self.тушаал = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.тушаал))

	self.эхmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.эхmacaddress))
	self.эхipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.эхipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *ArpМэдээ) Setbuffer(buffer_2 *ArpМэдээbuffer) {
	buffer_2.техникхангамжТөрөл = Unsignedinteger16toarray(self.техникхангамжТөрөл)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.техникхангамжaddressХэмжээ = uint8(self.техникхангамжaddressХэмжээ)
	buffer_2.protocoladdressХэмжээ = uint8(self.protocoladdressХэмжээ)

	buffer_2.тушаал = Unsignedinteger16toarray(self.тушаал)
	buffer_2.эхmacaddress = Unsignedinteger48toarray(self.эхmacaddress)
	buffer_2.эхipaddress = Unsignedinteger32toarray(self.эхipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(self.destinationipaddress)
}

type ArpИтернэтframehandler struct {
	TИтернэтframehandler
}

var arpprovider Arpprovider
var итернэтframeprovider TИтернэтframeprovider

func (self *ArpИтернэтframehandler) Итернэтframereceivewhen(datapointer uintptr, хэмжээ int) bool {
	arpКонсол.MХэвлэхxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Итернэтframereceivewhen(datapointer, uint32(хэмжээ))

}
func (self *ArpИтернэтframehandler) Send(destinationmacbe uint64, datapointer uintptr, хэмжээ uint32) {
	arpКонсол.MХэвлэхxy([]byte("arp send:"), 0, 24)
	var итернэтТөрөлbe = Unsignedinteger16r(0x0806)
	self.TИтернэтframehandler.Framesend(destinationmacbe, итернэтТөрөлbe, datapointer, хэмжээ)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IИтернэтframehandler
}

var handler IИтернэтframehandler

func (self *Arpprovider) Init(backend TИтернэтframeprovider, userhandler IИтернэтframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.numbercacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Итернэтframereceivewhen(datapointer uintptr, хэмжээ uint32) bool {

	if хэмжээ < arpmesgХэмжээ {
		return false
	}
	var arpbuffer *ArpМэдээbuffer = (*ArpМэдээbuffer)(Pointer(datapointer))
	var arp ArpМэдээ = ArpМэдээ{}
	arp.Init(arpbuffer)

	if arp.техникхангамжТөрөл == 0x0100 {

		if arp.protocol == 0x0008 && arp.техникхангамжaddressХэмжээ == 6 && arp.protocoladdressХэмжээ == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpКонсол.MХэвлэх([]byte("arp onetherframe"))
			arpКонсол.MUnsignedinteger16Хэвлэх(arp.protocol)
			arpКонсол.MХэвлэх([]byte(":"))
			arpКонсол.MUnsignedinteger64Хэвлэх(uint64(arp.destinationmacaddress))
			arpКонсол.MХэвлэх([]byte(":"))
			arpКонсол.MUnsignedinteger16Хэвлэх(arp.тушаал)
			arpКонсол.MХэвлэх([]byte(":"))
			arpКонсол.MUnsignedinteger64Хэвлэх(handler.Getmacaddress())

			switch arp.тушаал {
			case 0x0100:

				if self.Getmacfromcache(arp.эхipaddress) == 0xFFFFFFFFFFFF {
					if self.numbercacheentry < 128 {
						self.Ipcache[self.numbercacheentry] = arp.эхipaddress
						self.Maccache[self.numbercacheentry] = arp.эхmacaddress
						self.numbercacheentry++
					}
				}
				arp.тушаал = 0x0200
				arp.destinationipaddress = arp.эхipaddress
				arp.destinationmacaddress = arp.эхmacaddress
				arp.эхipaddress = uint32(handler.Getipaddress())
				arp.эхmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpКонсол.MХэвлэх(([]byte)("self.numCacheEntries"))

				if self.numbercacheentry < 128 {
					self.Ipcache[self.numbercacheentry] = arp.эхipaddress
					self.Maccache[self.numbercacheentry] = arp.эхmacaddress
					self.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpСүлжээbyteorder uint32) {

	var arp ArpМэдээ = ArpМэдээ{}
	arp.техникхангамжТөрөл = 0x0100
	arp.protocol = 0x0008
	arp.техникхангамжaddressХэмжээ = 6
	arp.protocoladdressХэмжээ = 4
	arp.тушаал = 0x0200

	arp.эхipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(IpСүлжээbyteorder)
	arp.destinationipaddress = IpСүлжээbyteorder
	arpКонсол.MХэвлэхxy([]byte("broad mac"), 0, 15)

	arp.эхmacaddress = handler.Getmacaddress()

	var arpbuffer ArpМэдээbuffer = ArpМэдээbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgХэмжээ)
}
func (self *Arpprovider) Requestmacaddress(IpСүлжээbyteorder uint32) {

	var arp ArpМэдээ = ArpМэдээ{}
	arp.техникхангамжТөрөл = 0x0100

	arp.protocol = 0x0008
	arp.техникхангамжaddressХэмжээ = 6
	arp.protocoladdressХэмжээ = 4
	arp.тушаал = 0x0100

	arp.эхmacaddress = handler.Getmacaddress()
	arp.эхipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpСүлжээbyteorder

	var arpbuffer ArpМэдээbuffer = ArpМэдээbuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgХэмжээ)
}
func (self *Arpprovider) TestХэвлэх(data *[]byte, хэмжээ uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpКонсол.MХэвлэхxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpКонсол.MHexadecimalХэвлэх(buffer_2[i])
		arpКонсол.MХэвлэх([]byte(":"))
	}
	arpКонсол.MХэвлэх([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpСүлжээbyteorder uint32) uint64 {
	for i := 0; i < self.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpКонсол.MХэвлэх(([]byte)("["))
		arpКонсол.MUnsignedinteger32Хэвлэх(self.Ipcache[i])
		arpКонсол.MХэвлэх(([]byte)(":"))
		arpКонсол.MUnsignedinteger32Хэвлэх(IpСүлжээbyteorder)
		arpКонсол.MХэвлэх(([]byte)(":"))
		arpКонсол.MХэвлэх(([]byte)(":"))
		arpКонсол.MUnsignedinteger64Хэвлэх(self.Maccache[i])
		arpКонсол.MХэвлэх(([]byte)("]\n"))

		if self.Ipcache[i] == IpСүлжээbyteorder {
			arpКонсол.MХэвлэх([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpСүлжээbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpСүлжээbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpСүлжээbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpСүлжээbyteorder)

	}

	return result
}
