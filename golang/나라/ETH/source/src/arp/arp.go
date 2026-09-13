package arp

import . "unsafe"
import . "console"
import . "ethernetክፈፍ"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpመልእክትbuffer struct {
	ጠንካራአካልአይነት		[2]byte
	protocol		[2]byte
	ጠንካራአካልaddressመጠን	byte
	protocoladdressመጠን	byte
	ትእዛዝ			[2]byte

	ምንጩmacaddress		[6]byte
	ምንጩipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgመጠን uint32 = (64+92+64)/8 + 2

type Arpመልእክት struct {
	ጠንካራአካልአይነት		uint16
	protocol		uint16
	ጠንካራአካልaddressመጠን	uint8
	protocoladdressመጠን	uint8
	ትእዛዝ			uint16

	ምንጩmacaddress		uint64
	ምንጩipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (self *Arpመልእክት) Init(buffer_2 *Arpመልእክትbuffer) {

	self.ጠንካራአካልአይነት = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.ጠንካራአካልአይነት))
	self.protocol = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.protocol))
	self.ጠንካራአካልaddressመጠን = byte(buffer_2.ጠንካራአካልaddressመጠን)
	self.protocoladdressመጠን = byte(buffer_2.protocoladdressመጠን)
	self.ትእዛዝ = Unsignedinteger16r(Aማዘጋጃtounsignedinteger16(buffer_2.ትእዛዝ))

	self.ምንጩmacaddress = Unsignedinteger48r(Aማዘጋጃtounsignedinteger48(buffer_2.ምንጩmacaddress))
	self.ምንጩipaddress = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer_2.ምንጩipaddress))
	self.destinationmacaddress = Unsignedinteger48r(Aማዘጋጃtounsignedinteger48(buffer_2.destinationmacaddress))
	self.destinationipaddress = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer_2.destinationipaddress))
}
func (self *Arpመልእክት) Setbuffer(buffer_2 *Arpመልእክትbuffer) {
	buffer_2.ጠንካራአካልአይነት = Unsignedinteger16toማዘጋጃ(self.ጠንካራአካልአይነት)
	buffer_2.protocol = Unsignedinteger16toማዘጋጃ(self.protocol)
	buffer_2.ጠንካራአካልaddressመጠን = uint8(self.ጠንካራአካልaddressመጠን)
	buffer_2.protocoladdressመጠን = uint8(self.protocoladdressመጠን)

	buffer_2.ትእዛዝ = Unsignedinteger16toማዘጋጃ(self.ትእዛዝ)
	buffer_2.ምንጩmacaddress = Unsignedinteger48toማዘጋጃ(self.ምንጩmacaddress)
	buffer_2.ምንጩipaddress = Unsignedinteger32toማዘጋጃ(self.ምንጩipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toማዘጋጃ(self.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toማዘጋጃ(self.destinationipaddress)
}

type Arpethernetክፈፍhandler struct {
	TEthernetክፈፍhandler
}

var arpprovider Arpprovider
var ethernetክፈፍprovider TEthernetክፈፍprovider

func (self *Arpethernetክፈፍhandler) Ethernetክፈፍreceivewhen(dataጠቋሚ uintptr, መጠን int) bool {
	arpconsole.Mማተሚያxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetክፈፍreceivewhen(dataጠቋሚ, uint32(መጠን))

}
func (self *Arpethernetክፈፍhandler) Send(destinationmacbe uint64, dataጠቋሚ uintptr, መጠን uint32) {
	arpconsole.Mማተሚያxy([]byte("arp send:"), 0, 24)
	var ethernetአይነትbe = Unsignedinteger16r(0x0806)
	self.TEthernetክፈፍhandler.Sክፈፍsend(destinationmacbe, ethernetአይነትbe, dataጠቋሚ, መጠን)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	ቁጥርcacheentry	int

	handler	IEthernetክፈፍhandler
}

var handler IEthernetክፈፍhandler

func (self *Arpprovider) Init(backend TEthernetክፈፍprovider, userhandler IEthernetክፈፍhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	self.ቁጥርcacheentry = 0
	arpprovider = *self

}

func (self *Arpprovider) Ethernetክፈፍreceivewhen(dataጠቋሚ uintptr, መጠን uint32) bool {

	if መጠን < arpmesgመጠን {
		return false
	}
	var arpbuffer *Arpመልእክትbuffer = (*Arpመልእክትbuffer)(Pointer(dataጠቋሚ))
	var arp Arpመልእክት = Arpመልእክት{}
	arp.Init(arpbuffer)

	if arp.ጠንካራአካልአይነት == 0x0100 {

		if arp.protocol == 0x0008 && arp.ጠንካራአካልaddressመጠን == 6 && arp.protocoladdressመጠን == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.Mማተሚያ([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16ማተሚያ(arp.protocol)
			arpconsole.Mማተሚያ([]byte(":"))
			arpconsole.MUnsignedinteger64ማተሚያ(uint64(arp.destinationmacaddress))
			arpconsole.Mማተሚያ([]byte(":"))
			arpconsole.MUnsignedinteger16ማተሚያ(arp.ትእዛዝ)
			arpconsole.Mማተሚያ([]byte(":"))
			arpconsole.MUnsignedinteger64ማተሚያ(handler.Getmacaddress())

			switch arp.ትእዛዝ {
			case 0x0100:

				if self.Getmacfromcache(arp.ምንጩipaddress) == 0xFFFFFFFFFFFF {
					if self.ቁጥርcacheentry < 128 {
						self.Ipcache[self.ቁጥርcacheentry] = arp.ምንጩipaddress
						self.Maccache[self.ቁጥርcacheentry] = arp.ምንጩmacaddress
						self.ቁጥርcacheentry++
					}
				}
				arp.ትእዛዝ = 0x0200
				arp.destinationipaddress = arp.ምንጩipaddress
				arp.destinationmacaddress = arp.ምንጩmacaddress
				arp.ምንጩipaddress = uint32(handler.Getipaddress())
				arp.ምንጩmacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.Mማተሚያ(([]byte)("self.numCacheEntries"))

				if self.ቁጥርcacheentry < 128 {
					self.Ipcache[self.ቁጥርcacheentry] = arp.ምንጩipaddress
					self.Maccache[self.ቁጥርcacheentry] = arp.ምንጩmacaddress
					self.ቁጥርcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(Ipኔትዎርክbyteorder uint32) {

	var arp Arpመልእክት = Arpመልእክት{}
	arp.ጠንካራአካልአይነት = 0x0100
	arp.protocol = 0x0008
	arp.ጠንካራአካልaddressመጠን = 6
	arp.protocoladdressመጠን = 4
	arp.ትእዛዝ = 0x0200

	arp.ምንጩipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = self.Resolve(Ipኔትዎርክbyteorder)
	arp.destinationipaddress = Ipኔትዎርክbyteorder
	arpconsole.Mማተሚያxy([]byte("broad mac"), 0, 15)

	arp.ምንጩmacaddress = handler.Getmacaddress()

	var arpbuffer Arpመልእክትbuffer = Arpመልእክትbuffer{}
	arp.Setbuffer(&arpbuffer)

	var ጠቋሚ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, ጠቋሚ, arpmesgመጠን)
}
func (self *Arpprovider) Requestmacaddress(Ipኔትዎርክbyteorder uint32) {

	var arp Arpመልእክት = Arpመልእክት{}
	arp.ጠንካራአካልአይነት = 0x0100

	arp.protocol = 0x0008
	arp.ጠንካራአካልaddressመጠን = 6
	arp.protocoladdressመጠን = 4
	arp.ትእዛዝ = 0x0100

	arp.ምንጩmacaddress = handler.Getmacaddress()
	arp.ምንጩipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = Ipኔትዎርክbyteorder

	var arpbuffer Arpመልእክትbuffer = Arpመልእክትbuffer{}
	arp.Setbuffer(&arpbuffer)

	var ጠቋሚ uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, ጠቋሚ, arpmesgመጠን)
}
func (self *Arpprovider) Tመሞከሪያማተሚያ(data *[]byte, መጠን uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.Mማተሚያxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalማተሚያ(buffer_2[i])
		arpconsole.Mማተሚያ([]byte(":"))
	}
	arpconsole.Mማተሚያ([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(Ipኔትዎርክbyteorder uint32) uint64 {
	for i := 0; i < self.ቁጥርcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.Mማተሚያ(([]byte)("["))
		arpconsole.MUnsignedinteger32ማተሚያ(self.Ipcache[i])
		arpconsole.Mማተሚያ(([]byte)(":"))
		arpconsole.MUnsignedinteger32ማተሚያ(Ipኔትዎርክbyteorder)
		arpconsole.Mማተሚያ(([]byte)(":"))
		arpconsole.Mማተሚያ(([]byte)(":"))
		arpconsole.MUnsignedinteger64ማተሚያ(self.Maccache[i])
		arpconsole.Mማተሚያ(([]byte)("]\n"))

		if self.Ipcache[i] == Ipኔትዎርክbyteorder {
			arpconsole.Mማተሚያ([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(Ipኔትዎርክbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(Ipኔትዎርክbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(Ipኔትዎርክbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(Ipኔትዎርክbyteorder)

	}

	return result
}
