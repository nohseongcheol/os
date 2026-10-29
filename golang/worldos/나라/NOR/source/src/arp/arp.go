/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetRamme"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpMeldingbuffer struct {
	maskinvareFiltype		[2]byte
	protocol			[2]byte
	maskinvareaddressStørrelse	byte
	protocoladdressStørrelse	byte
	kommando			[2]byte

	kildemacaddress	[6]byte
	kildeipaddress	[4]byte
	målmacaddress	[6]byte
	målipaddress	[4]byte
}

var arpmesgStørrelse uint32 = (64+92+64)/8 + 2

type ArpMelding struct {
	maskinvareFiltype		uint16
	protocol			uint16
	maskinvareaddressStørrelse	uint8
	protocoladdressStørrelse	uint8
	kommando			uint16

	kildemacaddress	uint64
	kildeipaddress	uint32
	målmacaddress	uint64
	målipaddress	uint32
}

func (selv *ArpMelding) Init(buffer_2 *ArpMeldingbuffer) {

	selv.maskinvareFiltype = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.maskinvareFiltype))
	selv.protocol = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.protocol))
	selv.maskinvareaddressStørrelse = byte(buffer_2.maskinvareaddressStørrelse)
	selv.protocoladdressStørrelse = byte(buffer_2.protocoladdressStørrelse)
	selv.kommando = Unsignedinteger16r(Tabelltounsignedinteger16(buffer_2.kommando))

	selv.kildemacaddress = Unsignedinteger48r(Tabelltounsignedinteger48(buffer_2.kildemacaddress))
	selv.kildeipaddress = Unsignedinteger32r(Tabelltounsignedinteger32(buffer_2.kildeipaddress))
	selv.målmacaddress = Unsignedinteger48r(Tabelltounsignedinteger48(buffer_2.målmacaddress))
	selv.målipaddress = Unsignedinteger32r(Tabelltounsignedinteger32(buffer_2.målipaddress))
}
func (selv *ArpMelding) Settbuffer(buffer_2 *ArpMeldingbuffer) {
	buffer_2.maskinvareFiltype = Unsignedinteger16toTabell(selv.maskinvareFiltype)
	buffer_2.protocol = Unsignedinteger16toTabell(selv.protocol)
	buffer_2.maskinvareaddressStørrelse = uint8(selv.maskinvareaddressStørrelse)
	buffer_2.protocoladdressStørrelse = uint8(selv.protocoladdressStørrelse)

	buffer_2.kommando = Unsignedinteger16toTabell(selv.kommando)
	buffer_2.kildemacaddress = Unsignedinteger48toTabell(selv.kildemacaddress)
	buffer_2.kildeipaddress = Unsignedinteger32toTabell(selv.kildeipaddress)
	buffer_2.målmacaddress = Unsignedinteger48toTabell(selv.målmacaddress)
	buffer_2.målipaddress = Unsignedinteger32toTabell(selv.målipaddress)
}

type ArpethernetRammehandler struct {
	TEthernetRammehandler
}

var arpprovider Arpprovider
var ethernetRammeprovider TEthernetRammeprovider

func (selv *ArpethernetRammehandler) EthernetRammereceivewhen(dataPeker uintptr, størrelse int) bool {
	arpconsole.MSkrivutxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRammereceivewhen(dataPeker, uint32(størrelse))

}
func (selv *ArpethernetRammehandler) Send(målmacbe uint64, dataPeker uintptr, størrelse uint32) {
	arpconsole.MSkrivutxy([]byte("arp send:"), 0, 24)
	var ethernetFiltypebe = Unsignedinteger16r(0x0806)
	selv.TEthernetRammehandler.Rammesend(målmacbe, ethernetFiltypebe, dataPeker, størrelse)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	tallcacheentry	int

	handler	IEthernetRammehandler
}

var handler IEthernetRammehandler

func (selv *Arpprovider) Init(backend TEthernetRammeprovider, userhandler IEthernetRammehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Setthandler(userhandler, 0x0806)
	selv.tallcacheentry = 0
	arpprovider = *selv

}

func (selv *Arpprovider) EthernetRammereceivewhen(dataPeker uintptr, størrelse uint32) bool {

	if størrelse < arpmesgStørrelse {
		return false
	}
	var arpbuffer *ArpMeldingbuffer = (*ArpMeldingbuffer)(Pointer(dataPeker))
	var arp ArpMelding = ArpMelding{}
	arp.Init(arpbuffer)

	if arp.maskinvareFiltype == 0x0100 {

		if arp.protocol == 0x0008 && arp.maskinvareaddressStørrelse == 6 && arp.protocoladdressStørrelse == 4 && uint64(arp.målipaddress) == handler.Getipaddress() {

			arpconsole.MSkrivut([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Skrivut(arp.protocol)
			arpconsole.MSkrivut([]byte(":"))
			arpconsole.MUnsignedinteger64Skrivut(uint64(arp.målmacaddress))
			arpconsole.MSkrivut([]byte(":"))
			arpconsole.MUnsignedinteger16Skrivut(arp.kommando)
			arpconsole.MSkrivut([]byte(":"))
			arpconsole.MUnsignedinteger64Skrivut(handler.Getmacaddress())

			switch arp.kommando {
			case 0x0100:

				if selv.Getmacfromcache(arp.kildeipaddress) == 0xFFFFFFFFFFFF {
					if selv.tallcacheentry < 128 {
						selv.Ipcache[selv.tallcacheentry] = arp.kildeipaddress
						selv.Maccache[selv.tallcacheentry] = arp.kildemacaddress
						selv.tallcacheentry++
					}
				}
				arp.kommando = 0x0200
				arp.målipaddress = arp.kildeipaddress
				arp.målmacaddress = arp.kildemacaddress
				arp.kildeipaddress = uint32(handler.Getipaddress())
				arp.kildemacaddress = handler.Getmacaddress()
				arp.Settbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MSkrivut(([]byte)("self.numCacheEntries"))

				if selv.tallcacheentry < 128 {
					selv.Ipcache[selv.tallcacheentry] = arp.kildeipaddress
					selv.Maccache[selv.tallcacheentry] = arp.kildemacaddress
					selv.tallcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (selv *Arpprovider) Broadcastmacaddress(IpNettverkbyteorder uint32) {

	var arp ArpMelding = ArpMelding{}
	arp.maskinvareFiltype = 0x0100
	arp.protocol = 0x0008
	arp.maskinvareaddressStørrelse = 6
	arp.protocoladdressStørrelse = 4
	arp.kommando = 0x0200

	arp.kildeipaddress = uint32(handler.Getipaddress())

	arp.målmacaddress = selv.Resolve(IpNettverkbyteorder)
	arp.målipaddress = IpNettverkbyteorder
	arpconsole.MSkrivutxy([]byte("broad mac"), 0, 15)

	arp.kildemacaddress = handler.Getmacaddress()

	var arpbuffer ArpMeldingbuffer = ArpMeldingbuffer{}
	arp.Settbuffer(&arpbuffer)

	var peker uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.målmacaddress, peker, arpmesgStørrelse)
}
func (selv *Arpprovider) Requestmacaddress(IpNettverkbyteorder uint32) {

	var arp ArpMelding = ArpMelding{}
	arp.maskinvareFiltype = 0x0100

	arp.protocol = 0x0008
	arp.maskinvareaddressStørrelse = 6
	arp.protocoladdressStørrelse = 4
	arp.kommando = 0x0100

	arp.kildemacaddress = handler.Getmacaddress()
	arp.kildeipaddress = uint32(handler.Getipaddress())

	arp.målmacaddress = 0xFFFFFFFFFFFF
	arp.målipaddress = IpNettverkbyteorder

	var arpbuffer ArpMeldingbuffer = ArpMeldingbuffer{}
	arp.Settbuffer(&arpbuffer)

	var peker uintptr = uintptr(Pointer(&arpbuffer))
	handler.Send(arp.målmacaddress, peker, arpmesgStørrelse)
}
func (selv *Arpprovider) TestSkrivut(data *[]byte, størrelse uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MSkrivutxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalSkrivut(buffer_2[i])
		arpconsole.MSkrivut([]byte(":"))
	}
	arpconsole.MSkrivut([]byte("]"))
}

func (selv *Arpprovider) Getmacfromcache(IpNettverkbyteorder uint32) uint64 {
	for i := 0; i < selv.tallcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MSkrivut(([]byte)("["))
		arpconsole.MUnsignedinteger32Skrivut(selv.Ipcache[i])
		arpconsole.MSkrivut(([]byte)(":"))
		arpconsole.MUnsignedinteger32Skrivut(IpNettverkbyteorder)
		arpconsole.MSkrivut(([]byte)(":"))
		arpconsole.MSkrivut(([]byte)(":"))
		arpconsole.MUnsignedinteger64Skrivut(selv.Maccache[i])
		arpconsole.MSkrivut(([]byte)("]\n"))

		if selv.Ipcache[i] == IpNettverkbyteorder {
			arpconsole.MSkrivut([]byte("getmacfromcache"))
			return selv.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (selv *Arpprovider) Resolve(IpNettverkbyteorder uint32) uint64 {
	var result uint64 = selv.Getmacfromcache(IpNettverkbyteorder)
	if result == 0xFFFFFFFFFFFF {
		selv.Requestmacaddress(IpNettverkbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = selv.Getmacfromcache(IpNettverkbyteorder)

	}

	return result
}
