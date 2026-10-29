/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetRammi"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpSKILABOÐbuffer struct {
	vélbúnaðurTegund	[2]byte
	protocol		[2]byte
	vélbúnaðuraddressStærð	byte
	protocoladdressStærð	byte
	skipun			[2]byte

	upprunimacaddress	[6]byte
	uppruniipaddress	[4]byte
	áfangastaðurmacaddress	[6]byte
	áfangastaðuripaddress	[4]byte
}

var arpmesgStærð uint32 = (64+92+64)/8 + 2

type ArpSKILABOÐ struct {
	vélbúnaðurTegund	uint16
	protocol		uint16
	vélbúnaðuraddressStærð	uint8
	protocoladdressStærð	uint8
	skipun			uint16

	upprunimacaddress	uint64
	uppruniipaddress	uint32
	áfangastaðurmacaddress	uint64
	áfangastaðuripaddress	uint32
}

func (sjálft *ArpSKILABOÐ) Init(buffer_2 *ArpSKILABOÐbuffer) {

	sjálft.vélbúnaðurTegund = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.vélbúnaðurTegund))
	sjálft.protocol = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.protocol))
	sjálft.vélbúnaðuraddressStærð = byte(buffer_2.vélbúnaðuraddressStærð)
	sjálft.protocoladdressStærð = byte(buffer_2.protocoladdressStærð)
	sjálft.skipun = Unsignedinteger16r(Fylkitounsignedinteger16(buffer_2.skipun))

	sjálft.upprunimacaddress = Unsignedinteger48r(Fylkitounsignedinteger48(buffer_2.upprunimacaddress))
	sjálft.uppruniipaddress = Unsignedinteger32r(Fylkitounsignedinteger32(buffer_2.uppruniipaddress))
	sjálft.áfangastaðurmacaddress = Unsignedinteger48r(Fylkitounsignedinteger48(buffer_2.áfangastaðurmacaddress))
	sjálft.áfangastaðuripaddress = Unsignedinteger32r(Fylkitounsignedinteger32(buffer_2.áfangastaðuripaddress))
}
func (sjálft *ArpSKILABOÐ) Setjabuffer(buffer_2 *ArpSKILABOÐbuffer) {
	buffer_2.vélbúnaðurTegund = Unsignedinteger16toFylki(sjálft.vélbúnaðurTegund)
	buffer_2.protocol = Unsignedinteger16toFylki(sjálft.protocol)
	buffer_2.vélbúnaðuraddressStærð = uint8(sjálft.vélbúnaðuraddressStærð)
	buffer_2.protocoladdressStærð = uint8(sjálft.protocoladdressStærð)

	buffer_2.skipun = Unsignedinteger16toFylki(sjálft.skipun)
	buffer_2.upprunimacaddress = Unsignedinteger48toFylki(sjálft.upprunimacaddress)
	buffer_2.uppruniipaddress = Unsignedinteger32toFylki(sjálft.uppruniipaddress)
	buffer_2.áfangastaðurmacaddress = Unsignedinteger48toFylki(sjálft.áfangastaðurmacaddress)
	buffer_2.áfangastaðuripaddress = Unsignedinteger32toFylki(sjálft.áfangastaðuripaddress)
}

type ArpethernetRammihandler struct {
	TEthernetRammihandler
}

var arpprovider Arpprovider
var ethernetRammiprovider TEthernetRammiprovider

func (sjálft *ArpethernetRammihandler) EthernetRammireceivewhen(dataBendill uintptr, stærð int) bool {
	arpconsole.MPrentaxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRammireceivewhen(dataBendill, uint32(stærð))

}
func (sjálft *ArpethernetRammihandler) Senda(áfangastaðurmacbe uint64, dataBendill uintptr, stærð uint32) {
	arpconsole.MPrentaxy([]byte("arp send:"), 0, 24)
	var ethernetTegundbe = Unsignedinteger16r(0x0806)
	sjálft.TEthernetRammihandler.RammiSenda(áfangastaðurmacbe, ethernetTegundbe, dataBendill, stærð)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetRammihandler
}

var handler IEthernetRammihandler

func (sjálft *Arpprovider) Init(backend TEthernetRammiprovider, userhandler IEthernetRammihandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Setjahandler(userhandler, 0x0806)
	sjálft.numbercacheentry = 0
	arpprovider = *sjálft

}

func (sjálft *Arpprovider) EthernetRammireceivewhen(dataBendill uintptr, stærð uint32) bool {

	if stærð < arpmesgStærð {
		return false
	}
	var arpbuffer *ArpSKILABOÐbuffer = (*ArpSKILABOÐbuffer)(Pointer(dataBendill))
	var arp ArpSKILABOÐ = ArpSKILABOÐ{}
	arp.Init(arpbuffer)

	if arp.vélbúnaðurTegund == 0x0100 {

		if arp.protocol == 0x0008 && arp.vélbúnaðuraddressStærð == 6 && arp.protocoladdressStærð == 4 && uint64(arp.áfangastaðuripaddress) == handler.Getipaddress() {

			arpconsole.MPrenta([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Prenta(arp.protocol)
			arpconsole.MPrenta([]byte(":"))
			arpconsole.MUnsignedinteger64Prenta(uint64(arp.áfangastaðurmacaddress))
			arpconsole.MPrenta([]byte(":"))
			arpconsole.MUnsignedinteger16Prenta(arp.skipun)
			arpconsole.MPrenta([]byte(":"))
			arpconsole.MUnsignedinteger64Prenta(handler.Getmacaddress())

			switch arp.skipun {
			case 0x0100:

				if sjálft.Getmacfromcache(arp.uppruniipaddress) == 0xFFFFFFFFFFFF {
					if sjálft.numbercacheentry < 128 {
						sjálft.Ipcache[sjálft.numbercacheentry] = arp.uppruniipaddress
						sjálft.Maccache[sjálft.numbercacheentry] = arp.upprunimacaddress
						sjálft.numbercacheentry++
					}
				}
				arp.skipun = 0x0200
				arp.áfangastaðuripaddress = arp.uppruniipaddress
				arp.áfangastaðurmacaddress = arp.upprunimacaddress
				arp.uppruniipaddress = uint32(handler.Getipaddress())
				arp.upprunimacaddress = handler.Getmacaddress()
				arp.Setjabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MPrenta(([]byte)("self.numCacheEntries"))

				if sjálft.numbercacheentry < 128 {
					sjálft.Ipcache[sjálft.numbercacheentry] = arp.uppruniipaddress
					sjálft.Maccache[sjálft.numbercacheentry] = arp.upprunimacaddress
					sjálft.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (sjálft *Arpprovider) Broadcastmacaddress(IpNetkerfibyteorder uint32) {

	var arp ArpSKILABOÐ = ArpSKILABOÐ{}
	arp.vélbúnaðurTegund = 0x0100
	arp.protocol = 0x0008
	arp.vélbúnaðuraddressStærð = 6
	arp.protocoladdressStærð = 4
	arp.skipun = 0x0200

	arp.uppruniipaddress = uint32(handler.Getipaddress())

	arp.áfangastaðurmacaddress = sjálft.Resolve(IpNetkerfibyteorder)
	arp.áfangastaðuripaddress = IpNetkerfibyteorder
	arpconsole.MPrentaxy([]byte("broad mac"), 0, 15)

	arp.upprunimacaddress = handler.Getmacaddress()

	var arpbuffer ArpSKILABOÐbuffer = ArpSKILABOÐbuffer{}
	arp.Setjabuffer(&arpbuffer)

	var bendill uintptr = uintptr(Pointer(&arpbuffer))
	handler.Senda(arp.áfangastaðurmacaddress, bendill, arpmesgStærð)
}
func (sjálft *Arpprovider) Requestmacaddress(IpNetkerfibyteorder uint32) {

	var arp ArpSKILABOÐ = ArpSKILABOÐ{}
	arp.vélbúnaðurTegund = 0x0100

	arp.protocol = 0x0008
	arp.vélbúnaðuraddressStærð = 6
	arp.protocoladdressStærð = 4
	arp.skipun = 0x0100

	arp.upprunimacaddress = handler.Getmacaddress()
	arp.uppruniipaddress = uint32(handler.Getipaddress())

	arp.áfangastaðurmacaddress = 0xFFFFFFFFFFFF
	arp.áfangastaðuripaddress = IpNetkerfibyteorder

	var arpbuffer ArpSKILABOÐbuffer = ArpSKILABOÐbuffer{}
	arp.Setjabuffer(&arpbuffer)

	var bendill uintptr = uintptr(Pointer(&arpbuffer))
	handler.Senda(arp.áfangastaðurmacaddress, bendill, arpmesgStærð)
}
func (sjálft *Arpprovider) PrófunPrenta(data *[]byte, stærð uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MPrentaxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalPrenta(buffer_2[i])
		arpconsole.MPrenta([]byte(":"))
	}
	arpconsole.MPrenta([]byte("]"))
}

func (sjálft *Arpprovider) Getmacfromcache(IpNetkerfibyteorder uint32) uint64 {
	for i := 0; i < sjálft.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MPrenta(([]byte)("["))
		arpconsole.MUnsignedinteger32Prenta(sjálft.Ipcache[i])
		arpconsole.MPrenta(([]byte)(":"))
		arpconsole.MUnsignedinteger32Prenta(IpNetkerfibyteorder)
		arpconsole.MPrenta(([]byte)(":"))
		arpconsole.MPrenta(([]byte)(":"))
		arpconsole.MUnsignedinteger64Prenta(sjálft.Maccache[i])
		arpconsole.MPrenta(([]byte)("]\n"))

		if sjálft.Ipcache[i] == IpNetkerfibyteorder {
			arpconsole.MPrenta([]byte("getmacfromcache"))
			return sjálft.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (sjálft *Arpprovider) Resolve(IpNetkerfibyteorder uint32) uint64 {
	var nIÐURSTAÐA uint64 = sjálft.Getmacfromcache(IpNetkerfibyteorder)
	if nIÐURSTAÐA == 0xFFFFFFFFFFFF {
		sjálft.Requestmacaddress(IpNetkerfibyteorder)
	}
	for i := 0; i < 128 && nIÐURSTAÐA == 0xFFFFFFFFFFFF; i++ {
		nIÐURSTAÐA = sjálft.Getmacfromcache(IpNetkerfibyteorder)

	}

	return nIÐURSTAÐA
}
