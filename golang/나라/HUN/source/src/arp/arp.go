package arp

import . "unsafe"
import . "konzol"
import . "ethernetKeret"
import . "util"

var arpKonzol TKonzol = TKonzol{}

type ArpÜzenetbuffer struct {
	hardverTípus		[2]byte
	protocol		[2]byte
	hardveraddressMéret	byte
	protocoladdressMéret	byte
	parancs			[2]byte

	forrásmacaddress	[6]byte
	forrásipaddress		[4]byte
	célmacaddress		[6]byte
	célipaddress		[4]byte
}

var arpmesgMéret uint32 = (64+92+64)/8 + 2

type ArpÜzenet struct {
	hardverTípus		uint16
	protocol		uint16
	hardveraddressMéret	uint8
	protocoladdressMéret	uint8
	parancs			uint16

	forrásmacaddress	uint64
	forrásipaddress		uint32
	célmacaddress		uint64
	célipaddress		uint32
}

func (self *ArpÜzenet) Init(buffer_2 *ArpÜzenetbuffer) {

	self.hardverTípus = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.hardverTípus))
	self.protocol = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.protocol))
	self.hardveraddressMéret = byte(buffer_2.hardveraddressMéret)
	self.protocoladdressMéret = byte(buffer_2.protocoladdressMéret)
	self.parancs = Unsignedinteger16r(Tömbtounsignedinteger16(buffer_2.parancs))

	self.forrásmacaddress = Unsignedinteger48r(Tömbtounsignedinteger48(buffer_2.forrásmacaddress))
	self.forrásipaddress = Unsignedinteger32r(Tömbtounsignedinteger32(buffer_2.forrásipaddress))
	self.célmacaddress = Unsignedinteger48r(Tömbtounsignedinteger48(buffer_2.célmacaddress))
	self.célipaddress = Unsignedinteger32r(Tömbtounsignedinteger32(buffer_2.célipaddress))
}
func (self *ArpÜzenet) Halmazbuffer(buffer_2 *ArpÜzenetbuffer) {
	buffer_2.hardverTípus = Unsignedinteger16toTömb(self.hardverTípus)
	buffer_2.protocol = Unsignedinteger16toTömb(self.protocol)
	buffer_2.hardveraddressMéret = uint8(self.hardveraddressMéret)
	buffer_2.protocoladdressMéret = uint8(self.protocoladdressMéret)

	buffer_2.parancs = Unsignedinteger16toTömb(self.parancs)
	buffer_2.forrásmacaddress = Unsignedinteger48toTömb(self.forrásmacaddress)
	buffer_2.forrásipaddress = Unsignedinteger32toTömb(self.forrásipaddress)
	buffer_2.célmacaddress = Unsignedinteger48toTömb(self.célmacaddress)
	buffer_2.célipaddress = Unsignedinteger32toTömb(self.célipaddress)
}

type ArpethernetKerethandler struct {
	TEthernetKerethandler
}

var arpprovider Arpprovider
var ethernetKeretprovider TEthernetKeretprovider

func (self *ArpethernetKerethandler) EthernetKeretreceivewhen(dataMutató uintptr, méret int) bool {
	arpKonzol.MNyomtatásxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetKeretreceivewhen(dataMutató, uint32(méret))

}
func (self *ArpethernetKerethandler) Küldés(célmacbe uint64, dataMutató uintptr, méret uint32) {
	arpKonzol.MNyomtatásxy([]byte("arp send:"), 0, 24)
	var ethernetTípusbe = Unsignedinteger16r(0x0806)
	self.TEthernetKerethandler.KeretKüldés(célmacbe, ethernetTípusbe, dataMutató, méret)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	számcachebejegyzés	int

	handler	IEthernetKerethandler
}

var handler IEthernetKerethandler

func (self *Arpprovider) Init(backend TEthernetKeretprovider, userhandler IEthernetKerethandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Halmazhandler(userhandler, 0x0806)
	self.számcachebejegyzés = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetKeretreceivewhen(dataMutató uintptr, méret uint32) bool {

	if méret < arpmesgMéret {
		return false
	}
	var arpbuffer *ArpÜzenetbuffer = (*ArpÜzenetbuffer)(Pointer(dataMutató))
	var arp ArpÜzenet = ArpÜzenet{}
	arp.Init(arpbuffer)

	if arp.hardverTípus == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardveraddressMéret == 6 && arp.protocoladdressMéret == 4 && uint64(arp.célipaddress) == handler.Getipaddress() {

			arpKonzol.MNyomtatás([]byte("arp onetherframe"))
			arpKonzol.MUnsignedinteger16Nyomtatás(arp.protocol)
			arpKonzol.MNyomtatás([]byte(":"))
			arpKonzol.MUnsignedinteger64Nyomtatás(uint64(arp.célmacaddress))
			arpKonzol.MNyomtatás([]byte(":"))
			arpKonzol.MUnsignedinteger16Nyomtatás(arp.parancs)
			arpKonzol.MNyomtatás([]byte(":"))
			arpKonzol.MUnsignedinteger64Nyomtatás(handler.Getmacaddress())

			switch arp.parancs {
			case 0x0100:

				if self.Getmacfromcache(arp.forrásipaddress) == 0xFFFFFFFFFFFF {
					if self.számcachebejegyzés < 128 {
						self.Ipcache[self.számcachebejegyzés] = arp.forrásipaddress
						self.Maccache[self.számcachebejegyzés] = arp.forrásmacaddress
						self.számcachebejegyzés++
					}
				}
				arp.parancs = 0x0200
				arp.célipaddress = arp.forrásipaddress
				arp.célmacaddress = arp.forrásmacaddress
				arp.forrásipaddress = uint32(handler.Getipaddress())
				arp.forrásmacaddress = handler.Getmacaddress()
				arp.Halmazbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonzol.MNyomtatás(([]byte)("self.numCacheEntries"))

				if self.számcachebejegyzés < 128 {
					self.Ipcache[self.számcachebejegyzés] = arp.forrásipaddress
					self.Maccache[self.számcachebejegyzés] = arp.forrásmacaddress
					self.számcachebejegyzés++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpHálózatbyteorder uint32) {

	var arp ArpÜzenet = ArpÜzenet{}
	arp.hardverTípus = 0x0100
	arp.protocol = 0x0008
	arp.hardveraddressMéret = 6
	arp.protocoladdressMéret = 4
	arp.parancs = 0x0200

	arp.forrásipaddress = uint32(handler.Getipaddress())

	arp.célmacaddress = self.Resolve(IpHálózatbyteorder)
	arp.célipaddress = IpHálózatbyteorder
	arpKonzol.MNyomtatásxy([]byte("broad mac"), 0, 15)

	arp.forrásmacaddress = handler.Getmacaddress()

	var arpbuffer ArpÜzenetbuffer = ArpÜzenetbuffer{}
	arp.Halmazbuffer(&arpbuffer)

	var mutató uintptr = uintptr(Pointer(&arpbuffer))
	handler.Küldés(arp.célmacaddress, mutató, arpmesgMéret)
}
func (self *Arpprovider) Requestmacaddress(IpHálózatbyteorder uint32) {

	var arp ArpÜzenet = ArpÜzenet{}
	arp.hardverTípus = 0x0100

	arp.protocol = 0x0008
	arp.hardveraddressMéret = 6
	arp.protocoladdressMéret = 4
	arp.parancs = 0x0100

	arp.forrásmacaddress = handler.Getmacaddress()
	arp.forrásipaddress = uint32(handler.Getipaddress())

	arp.célmacaddress = 0xFFFFFFFFFFFF
	arp.célipaddress = IpHálózatbyteorder

	var arpbuffer ArpÜzenetbuffer = ArpÜzenetbuffer{}
	arp.Halmazbuffer(&arpbuffer)

	var mutató uintptr = uintptr(Pointer(&arpbuffer))
	handler.Küldés(arp.célmacaddress, mutató, arpmesgMéret)
}
func (self *Arpprovider) TesztNyomtatás(data *[]byte, méret uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonzol.MNyomtatásxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonzol.MHexadecimalNyomtatás(buffer_2[i])
		arpKonzol.MNyomtatás([]byte(":"))
	}
	arpKonzol.MNyomtatás([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpHálózatbyteorder uint32) uint64 {
	for i := 0; i < self.számcachebejegyzés; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonzol.MNyomtatás(([]byte)("["))
		arpKonzol.MUnsignedinteger32Nyomtatás(self.Ipcache[i])
		arpKonzol.MNyomtatás(([]byte)(":"))
		arpKonzol.MUnsignedinteger32Nyomtatás(IpHálózatbyteorder)
		arpKonzol.MNyomtatás(([]byte)(":"))
		arpKonzol.MNyomtatás(([]byte)(":"))
		arpKonzol.MUnsignedinteger64Nyomtatás(self.Maccache[i])
		arpKonzol.MNyomtatás(([]byte)("]\n"))

		if self.Ipcache[i] == IpHálózatbyteorder {
			arpKonzol.MNyomtatás([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpHálózatbyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpHálózatbyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpHálózatbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpHálózatbyteorder)

	}

	return result
}
