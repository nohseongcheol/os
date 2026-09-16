/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetframe"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpPORUKAbuffer struct {
	sklopovljeVrsta			[2]byte
	protocol			[2]byte
	sklopovljeaddressVeličina	byte
	protocoladdressVeličina		byte
	naredba				[2]byte

	izvormacaddress		[6]byte
	izvoripaddress		[4]byte
	odredištemacaddress	[6]byte
	odredišteipaddress	[4]byte
}

var arpmesgVeličina uint32 = (64+92+64)/8 + 2

type ArpPORUKA struct {
	sklopovljeVrsta			uint16
	protocol			uint16
	sklopovljeaddressVeličina	uint8
	protocoladdressVeličina		uint8
	naredba				uint16

	izvormacaddress		uint64
	izvoripaddress		uint32
	odredištemacaddress	uint64
	odredišteipaddress	uint32
}

func (sam *ArpPORUKA) Init(buffer_2 *ArpPORUKAbuffer) {

	sam.sklopovljeVrsta = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.sklopovljeVrsta))
	sam.protocol = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.protocol))
	sam.sklopovljeaddressVeličina = byte(buffer_2.sklopovljeaddressVeličina)
	sam.protocoladdressVeličina = byte(buffer_2.protocoladdressVeličina)
	sam.naredba = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.naredba))

	sam.izvormacaddress = Unsignedinteger48r(Niztounsignedinteger48(buffer_2.izvormacaddress))
	sam.izvoripaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.izvoripaddress))
	sam.odredištemacaddress = Unsignedinteger48r(Niztounsignedinteger48(buffer_2.odredištemacaddress))
	sam.odredišteipaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.odredišteipaddress))
}
func (sam *ArpPORUKA) Postavibuffer(buffer_2 *ArpPORUKAbuffer) {
	buffer_2.sklopovljeVrsta = Unsignedinteger16toNiz(sam.sklopovljeVrsta)
	buffer_2.protocol = Unsignedinteger16toNiz(sam.protocol)
	buffer_2.sklopovljeaddressVeličina = uint8(sam.sklopovljeaddressVeličina)
	buffer_2.protocoladdressVeličina = uint8(sam.protocoladdressVeličina)

	buffer_2.naredba = Unsignedinteger16toNiz(sam.naredba)
	buffer_2.izvormacaddress = Unsignedinteger48toNiz(sam.izvormacaddress)
	buffer_2.izvoripaddress = Unsignedinteger32toNiz(sam.izvoripaddress)
	buffer_2.odredištemacaddress = Unsignedinteger48toNiz(sam.odredištemacaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toNiz(sam.odredišteipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var ethernetframeprovider TEthernetframeprovider

func (sam *Arpethernetframehandler) Ethernetframereceivewhen(dataPokazivač uintptr, veličina int) bool {
	arpconsole.MIspisxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(dataPokazivač, uint32(veličina))

}
func (sam *Arpethernetframehandler) Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32) {
	arpconsole.MIspisxy([]byte("arp send:"), 0, 24)
	var ethernetVrstabe = Unsignedinteger16r(0x0806)
	sam.TEthernetframehandler.FramePošalji(odredištemacbe, ethernetVrstabe, dataPokazivač, veličina)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	bROJcacheentry	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (sam *Arpprovider) Init(backend TEthernetframeprovider, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Postavihandler(userhandler, 0x0806)
	sam.bROJcacheentry = 0
	arpprovider = *sam

}

func (sam *Arpprovider) Ethernetframereceivewhen(dataPokazivač uintptr, veličina uint32) bool {

	if veličina < arpmesgVeličina {
		return false
	}
	var arpbuffer *ArpPORUKAbuffer = (*ArpPORUKAbuffer)(Pointer(dataPokazivač))
	var arp ArpPORUKA = ArpPORUKA{}
	arp.Init(arpbuffer)

	if arp.sklopovljeVrsta == 0x0100 {

		if arp.protocol == 0x0008 && arp.sklopovljeaddressVeličina == 6 && arp.protocoladdressVeličina == 4 && uint64(arp.odredišteipaddress) == handler.Getipaddress() {

			arpconsole.MIspis([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Ispis(arp.protocol)
			arpconsole.MIspis([]byte(":"))
			arpconsole.MUnsignedinteger64Ispis(uint64(arp.odredištemacaddress))
			arpconsole.MIspis([]byte(":"))
			arpconsole.MUnsignedinteger16Ispis(arp.naredba)
			arpconsole.MIspis([]byte(":"))
			arpconsole.MUnsignedinteger64Ispis(handler.Getmacaddress())

			switch arp.naredba {
			case 0x0100:

				if sam.Getmacfromcache(arp.izvoripaddress) == 0xFFFFFFFFFFFF {
					if sam.bROJcacheentry < 128 {
						sam.Ipcache[sam.bROJcacheentry] = arp.izvoripaddress
						sam.Maccache[sam.bROJcacheentry] = arp.izvormacaddress
						sam.bROJcacheentry++
					}
				}
				arp.naredba = 0x0200
				arp.odredišteipaddress = arp.izvoripaddress
				arp.odredištemacaddress = arp.izvormacaddress
				arp.izvoripaddress = uint32(handler.Getipaddress())
				arp.izvormacaddress = handler.Getmacaddress()
				arp.Postavibuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MIspis(([]byte)("self.numCacheEntries"))

				if sam.bROJcacheentry < 128 {
					sam.Ipcache[sam.bROJcacheentry] = arp.izvoripaddress
					sam.Maccache[sam.bROJcacheentry] = arp.izvormacaddress
					sam.bROJcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (sam *Arpprovider) Broadcastmacaddress(IpMrežabyteorder uint32) {

	var arp ArpPORUKA = ArpPORUKA{}
	arp.sklopovljeVrsta = 0x0100
	arp.protocol = 0x0008
	arp.sklopovljeaddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0200

	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = sam.Resolve(IpMrežabyteorder)
	arp.odredišteipaddress = IpMrežabyteorder
	arpconsole.MIspisxy([]byte("broad mac"), 0, 15)

	arp.izvormacaddress = handler.Getmacaddress()

	var arpbuffer ArpPORUKAbuffer = ArpPORUKAbuffer{}
	arp.Postavibuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pokazivač, arpmesgVeličina)
}
func (sam *Arpprovider) Requestmacaddress(IpMrežabyteorder uint32) {

	var arp ArpPORUKA = ArpPORUKA{}
	arp.sklopovljeVrsta = 0x0100

	arp.protocol = 0x0008
	arp.sklopovljeaddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0100

	arp.izvormacaddress = handler.Getmacaddress()
	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = 0xFFFFFFFFFFFF
	arp.odredišteipaddress = IpMrežabyteorder

	var arpbuffer ArpPORUKAbuffer = ArpPORUKAbuffer{}
	arp.Postavibuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pokazivač, arpmesgVeličina)
}
func (sam *Arpprovider) ProvjeriIspis(data *[]byte, veličina uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MIspisxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalIspis(buffer_2[i])
		arpconsole.MIspis([]byte(":"))
	}
	arpconsole.MIspis([]byte("]"))
}

func (sam *Arpprovider) Getmacfromcache(IpMrežabyteorder uint32) uint64 {
	for i := 0; i < sam.bROJcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MIspis(([]byte)("["))
		arpconsole.MUnsignedinteger32Ispis(sam.Ipcache[i])
		arpconsole.MIspis(([]byte)(":"))
		arpconsole.MUnsignedinteger32Ispis(IpMrežabyteorder)
		arpconsole.MIspis(([]byte)(":"))
		arpconsole.MIspis(([]byte)(":"))
		arpconsole.MUnsignedinteger64Ispis(sam.Maccache[i])
		arpconsole.MIspis(([]byte)("]\n"))

		if sam.Ipcache[i] == IpMrežabyteorder {
			arpconsole.MIspis([]byte("getmacfromcache"))
			return sam.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (sam *Arpprovider) Resolve(IpMrežabyteorder uint32) uint64 {
	var rEZULTAT uint64 = sam.Getmacfromcache(IpMrežabyteorder)
	if rEZULTAT == 0xFFFFFFFFFFFF {
		sam.Requestmacaddress(IpMrežabyteorder)
	}
	for i := 0; i < 128 && rEZULTAT == 0xFFFFFFFFFFFF; i++ {
		rEZULTAT = sam.Getmacfromcache(IpMrežabyteorder)

	}

	return rEZULTAT
}
