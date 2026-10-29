/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetRamme"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpMeddelelsebuffer struct {
	udstyrtype			[2]byte
	protocol			[2]byte
	udstyraddressStørrelse		byte
	protocoladdressStørrelse	byte
	kommando			[2]byte

	kildemacaddress		[6]byte
	kildeipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgStørrelse uint32 = (64+92+64)/8 + 2

type ArpMeddelelse struct {
	udstyrtype			uint16
	protocol			uint16
	udstyraddressStørrelse		uint8
	protocoladdressStørrelse	uint8
	kommando			uint16

	kildemacaddress		uint64
	kildeipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (selv *ArpMeddelelse) Init(buffer_2 *ArpMeddelelsebuffer) {

	selv.udstyrtype = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.udstyrtype))
	selv.protocol = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.protocol))
	selv.udstyraddressStørrelse = byte(buffer_2.udstyraddressStørrelse)
	selv.protocoladdressStørrelse = byte(buffer_2.protocoladdressStørrelse)
	selv.kommando = Unsignedinteger16r(Tabeltounsignedinteger16(buffer_2.kommando))

	selv.kildemacaddress = Unsignedinteger48r(Tabeltounsignedinteger48(buffer_2.kildemacaddress))
	selv.kildeipaddress = Unsignedinteger32r(Tabeltounsignedinteger32(buffer_2.kildeipaddress))
	selv.destinationmacaddress = Unsignedinteger48r(Tabeltounsignedinteger48(buffer_2.destinationmacaddress))
	selv.destinationipaddress = Unsignedinteger32r(Tabeltounsignedinteger32(buffer_2.destinationipaddress))
}
func (selv *ArpMeddelelse) Satbuffer(buffer_2 *ArpMeddelelsebuffer) {
	buffer_2.udstyrtype = Unsignedinteger16toTabel(selv.udstyrtype)
	buffer_2.protocol = Unsignedinteger16toTabel(selv.protocol)
	buffer_2.udstyraddressStørrelse = uint8(selv.udstyraddressStørrelse)
	buffer_2.protocoladdressStørrelse = uint8(selv.protocoladdressStørrelse)

	buffer_2.kommando = Unsignedinteger16toTabel(selv.kommando)
	buffer_2.kildemacaddress = Unsignedinteger48toTabel(selv.kildemacaddress)
	buffer_2.kildeipaddress = Unsignedinteger32toTabel(selv.kildeipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toTabel(selv.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toTabel(selv.destinationipaddress)
}

type ArpethernetRammehandler struct {
	TEthernetRammehandler
}

var arpprovider Arpprovider
var ethernetRammeprovider TEthernetRammeprovider

func (selv *ArpethernetRammehandler) EthernetRammereceivewhen(dataMarkør uintptr, størrelse int) bool {
	arpconsole.MUdskrivxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRammereceivewhen(dataMarkør, uint32(størrelse))

}
func (selv *ArpethernetRammehandler) Send(destinationmacbe uint64, dataMarkør uintptr, størrelse uint32) {
	arpconsole.MUdskrivxy([]byte("arp send:"), 0, 24)
	var ethernettypebe = Unsignedinteger16r(0x0806)
	selv.TEthernetRammehandler.Rammesend(destinationmacbe, ethernettypebe, dataMarkør, størrelse)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	talcacheemne	int

	handler	IEthernetRammehandler
}

var handler IEthernetRammehandler

func (selv *Arpprovider) Init(backend TEthernetRammeprovider, userhandler IEthernetRammehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sathandler(userhandler, 0x0806)
	selv.talcacheemne = 0
	arpprovider = *selv

}

func (selv *Arpprovider) EthernetRammereceivewhen(dataMarkør uintptr, størrelse uint32) bool {

	if størrelse < arpmesgStørrelse {
		return false
	}
	var arpbuffer *ArpMeddelelsebuffer = (*ArpMeddelelsebuffer)(Pointer(dataMarkør))
	var arp ArpMeddelelse = ArpMeddelelse{}
	arp.Init(arpbuffer)

	if arp.udstyrtype == 0x0100 {

		if arp.protocol == 0x0008 && arp.udstyraddressStørrelse == 6 && arp.protocoladdressStørrelse == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MUdskriv([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Udskriv(arp.protocol)
			arpconsole.MUdskriv([]byte(":"))
			arpconsole.MUnsignedinteger64Udskriv(uint64(arp.destinationmacaddress))
			arpconsole.MUdskriv([]byte(":"))
			arpconsole.MUnsignedinteger16Udskriv(arp.kommando)
			arpconsole.MUdskriv([]byte(":"))
			arpconsole.MUnsignedinteger64Udskriv(handler.Getmacaddress())

			switch arp.kommando {
			case 0x0100:

				if selv.Getmacfracache(arp.kildeipaddress) == 0xFFFFFFFFFFFF {
					if selv.talcacheemne < 128 {
						selv.Ipcache[selv.talcacheemne] = arp.kildeipaddress
						selv.Maccache[selv.talcacheemne] = arp.kildemacaddress
						selv.talcacheemne++
					}
				}
				arp.kommando = 0x0200
				arp.destinationipaddress = arp.kildeipaddress
				arp.destinationmacaddress = arp.kildemacaddress
				arp.kildeipaddress = uint32(handler.Getipaddress())
				arp.kildemacaddress = handler.Getmacaddress()
				arp.Satbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MUdskriv(([]byte)("self.numCacheEntries"))

				if selv.talcacheemne < 128 {
					selv.Ipcache[selv.talcacheemne] = arp.kildeipaddress
					selv.Maccache[selv.talcacheemne] = arp.kildemacaddress
					selv.talcacheemne++
				}
				break
			}

		}
	}
	return false

}

func (selv *Arpprovider) Broadcastmacaddress(IpNetværkbyteorder uint32) {

	var arp ArpMeddelelse = ArpMeddelelse{}
	arp.udstyrtype = 0x0100
	arp.protocol = 0x0008
	arp.udstyraddressStørrelse = 6
	arp.protocoladdressStørrelse = 4
	arp.kommando = 0x0200

	arp.kildeipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = selv.Resolve(IpNetværkbyteorder)
	arp.destinationipaddress = IpNetværkbyteorder
	arpconsole.MUdskrivxy([]byte("broad mac"), 0, 15)

	arp.kildemacaddress = handler.Getmacaddress()

	var arpbuffer ArpMeddelelsebuffer = ArpMeddelelsebuffer{}
	arp.Satbuffer(&arpbuffer)

	var markør uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, markør, arpmesgStørrelse)
}
func (selv *Arpprovider) Requestmacaddress(IpNetværkbyteorder uint32) {

	var arp ArpMeddelelse = ArpMeddelelse{}
	arp.udstyrtype = 0x0100

	arp.protocol = 0x0008
	arp.udstyraddressStørrelse = 6
	arp.protocoladdressStørrelse = 4
	arp.kommando = 0x0100

	arp.kildemacaddress = handler.Getmacaddress()
	arp.kildeipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpNetværkbyteorder

	var arpbuffer ArpMeddelelsebuffer = ArpMeddelelsebuffer{}
	arp.Satbuffer(&arpbuffer)

	var markør uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.destinationmacaddress, markør, arpmesgStørrelse)
}
func (selv *Arpprovider) PrøvUdskriv(data *[]byte, størrelse uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MUdskrivxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalUdskriv(buffer_2[i])
		arpconsole.MUdskriv([]byte(":"))
	}
	arpconsole.MUdskriv([]byte("]"))
}

func (selv *Arpprovider) Getmacfracache(IpNetværkbyteorder uint32) uint64 {
	for i := 0; i < selv.talcacheemne; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MUdskriv(([]byte)("["))
		arpconsole.MUnsignedinteger32Udskriv(selv.Ipcache[i])
		arpconsole.MUdskriv(([]byte)(":"))
		arpconsole.MUnsignedinteger32Udskriv(IpNetværkbyteorder)
		arpconsole.MUdskriv(([]byte)(":"))
		arpconsole.MUdskriv(([]byte)(":"))
		arpconsole.MUnsignedinteger64Udskriv(selv.Maccache[i])
		arpconsole.MUdskriv(([]byte)("]\n"))

		if selv.Ipcache[i] == IpNetværkbyteorder {
			arpconsole.MUdskriv([]byte("getmacfromcache"))
			return selv.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (selv *Arpprovider) Resolve(IpNetværkbyteorder uint32) uint64 {
	var result uint64 = selv.Getmacfracache(IpNetværkbyteorder)
	if result == 0xFFFFFFFFFFFF {
		selv.Requestmacaddress(IpNetværkbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = selv.Getmacfracache(IpNetværkbyteorder)

	}

	return result
}
