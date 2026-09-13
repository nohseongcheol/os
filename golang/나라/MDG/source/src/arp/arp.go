package arp

import . "unsafe"
import . "konsoly"
import . "ethernetframe"
import . "util"

var arpKonsoly TKonsoly = TKonsoly{}

type ArpHafatrabuffer struct {
	hardwareKarazana	[2]byte
	protocol		[2]byte
	hardwareaddressHabe	byte
	protocoladdressHabe	byte
	baiko			[2]byte

	loharanomacaddress	[6]byte
	loharanoipaddress	[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgHabe uint32 = (64+92+64)/8 + 2

type ArpHafatra struct {
	hardwareKarazana	uint16
	protocol		uint16
	hardwareaddressHabe	uint8
	protocoladdressHabe	uint8
	baiko			uint16

	loharanomacaddress	uint64
	loharanoipaddress	uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (nytena *ArpHafatra) Init(buffer_2 *ArpHafatrabuffer) {

	nytena.hardwareKarazana = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardwareKarazana))
	nytena.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	nytena.hardwareaddressHabe = byte(buffer_2.hardwareaddressHabe)
	nytena.protocoladdressHabe = byte(buffer_2.protocoladdressHabe)
	nytena.baiko = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.baiko))

	nytena.loharanomacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.loharanomacaddress))
	nytena.loharanoipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.loharanoipaddress))
	nytena.destinationmacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.destinationmacaddress))
	nytena.destinationipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.destinationipaddress))
}
func (nytena *ArpHafatra) Setbuffer(buffer_2 *ArpHafatrabuffer) {
	buffer_2.hardwareKarazana = Unsignedinteger16toarray(nytena.hardwareKarazana)
	buffer_2.protocol = Unsignedinteger16toarray(nytena.protocol)
	buffer_2.hardwareaddressHabe = uint8(nytena.hardwareaddressHabe)
	buffer_2.protocoladdressHabe = uint8(nytena.protocoladdressHabe)

	buffer_2.baiko = Unsignedinteger16toarray(nytena.baiko)
	buffer_2.loharanomacaddress = Unsignedinteger48toarray(nytena.loharanomacaddress)
	buffer_2.loharanoipaddress = Unsignedinteger32toarray(nytena.loharanoipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toarray(nytena.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toarray(nytena.destinationipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (nytena *Arpethernetframehandler) Ethernetframereceivewhen(datapointer uintptr, habe int) bool {
	arpKonsoly.MAtontayxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(datapointer, uint32(habe))

}
func (nytena *Arpethernetframehandler) Send(destinationmacbe uint64, datapointer uintptr, habe uint32) {
	arpKonsoly.MAtontayxy([]byte("arp send:"), 0, 24)
	var ethernetKarazanabe = Unsignedinteger16r(0x0806)
	nytena.TEthernetframehandler.Framesend(destinationmacbe, ethernetKarazanabe, datapointer, habe)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (nytena *Arpprovider) Init(backend TEthernetframeprovider, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sethandler(userhandler, 0x0806)
	nytena.numbercacheentry = 0
	arpprovider = *nytena

}

func (nytena *Arpprovider) Ethernetframereceivewhen(datapointer uintptr, habe uint32) bool {

	if habe < arpmesgHabe {
		return false
	}
	var arpbuffer *ArpHafatrabuffer = (*ArpHafatrabuffer)(Pointer(datapointer))
	var arp ArpHafatra = ArpHafatra{}
	arp.Init(arpbuffer)

	if arp.hardwareKarazana == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressHabe == 6 && arp.protocoladdressHabe == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpKonsoly.MAtontay([]byte("arp onetherframe"))
			arpKonsoly.MUnsignedinteger16Atontay(arp.protocol)
			arpKonsoly.MAtontay([]byte(":"))
			arpKonsoly.MUnsignedinteger64Atontay(uint64(arp.destinationmacaddress))
			arpKonsoly.MAtontay([]byte(":"))
			arpKonsoly.MUnsignedinteger16Atontay(arp.baiko)
			arpKonsoly.MAtontay([]byte(":"))
			arpKonsoly.MUnsignedinteger64Atontay(handler.Getmacaddress())

			switch arp.baiko {
			case 0x0100:

				if nytena.Getmacfromcache(arp.loharanoipaddress) == 0xFFFFFFFFFFFF {
					if nytena.numbercacheentry < 128 {
						nytena.Ipcache[nytena.numbercacheentry] = arp.loharanoipaddress
						nytena.Maccache[nytena.numbercacheentry] = arp.loharanomacaddress
						nytena.numbercacheentry++
					}
				}
				arp.baiko = 0x0200
				arp.destinationipaddress = arp.loharanoipaddress
				arp.destinationmacaddress = arp.loharanomacaddress
				arp.loharanoipaddress = uint32(handler.Getipaddress())
				arp.loharanomacaddress = handler.Getmacaddress()
				arp.Setbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsoly.MAtontay(([]byte)("self.numCacheEntries"))

				if nytena.numbercacheentry < 128 {
					nytena.Ipcache[nytena.numbercacheentry] = arp.loharanoipaddress
					nytena.Maccache[nytena.numbercacheentry] = arp.loharanomacaddress
					nytena.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (nytena *Arpprovider) Broadcastmacaddress(IpRezobyteorder uint32) {

	var arp ArpHafatra = ArpHafatra{}
	arp.hardwareKarazana = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressHabe = 6
	arp.protocoladdressHabe = 4
	arp.baiko = 0x0200

	arp.loharanoipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = nytena.Resolve(IpRezobyteorder)
	arp.destinationipaddress = IpRezobyteorder
	arpKonsoly.MAtontayxy([]byte("broad mac"), 0, 15)

	arp.loharanomacaddress = handler.Getmacaddress()

	var arpbuffer ArpHafatrabuffer = ArpHafatrabuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgHabe)
}
func (nytena *Arpprovider) Requestmacaddress(IpRezobyteorder uint32) {

	var arp ArpHafatra = ArpHafatra{}
	arp.hardwareKarazana = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressHabe = 6
	arp.protocoladdressHabe = 4
	arp.baiko = 0x0100

	arp.loharanomacaddress = handler.Getmacaddress()
	arp.loharanoipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpRezobyteorder

	var arpbuffer ArpHafatrabuffer = ArpHafatrabuffer{}
	arp.Setbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, pointer, arpmesgHabe)
}
func (nytena *Arpprovider) TestAtontay(data *[]byte, habe uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsoly.MAtontayxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsoly.MHexadecimalAtontay(buffer_2[i])
		arpKonsoly.MAtontay([]byte(":"))
	}
	arpKonsoly.MAtontay([]byte("]"))
}

func (nytena *Arpprovider) Getmacfromcache(IpRezobyteorder uint32) uint64 {
	for i := 0; i < nytena.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsoly.MAtontay(([]byte)("["))
		arpKonsoly.MUnsignedinteger32Atontay(nytena.Ipcache[i])
		arpKonsoly.MAtontay(([]byte)(":"))
		arpKonsoly.MUnsignedinteger32Atontay(IpRezobyteorder)
		arpKonsoly.MAtontay(([]byte)(":"))
		arpKonsoly.MAtontay(([]byte)(":"))
		arpKonsoly.MUnsignedinteger64Atontay(nytena.Maccache[i])
		arpKonsoly.MAtontay(([]byte)("]\n"))

		if nytena.Ipcache[i] == IpRezobyteorder {
			arpKonsoly.MAtontay([]byte("getmacfromcache"))
			return nytena.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (nytena *Arpprovider) Resolve(IpRezobyteorder uint32) uint64 {
	var result uint64 = nytena.Getmacfromcache(IpRezobyteorder)
	if result == 0xFFFFFFFFFFFF {
		nytena.Requestmacaddress(IpRezobyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = nytena.Getmacfromcache(IpRezobyteorder)

	}

	return result
}
