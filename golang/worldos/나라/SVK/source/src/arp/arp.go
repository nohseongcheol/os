/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konzola"
import . "ethernetRámec"
import . "util"

var arpKonzola TKonzola = TKonzola{}

type ArpSprávabuffer struct {
	hardvérTyp		[2]byte
	protocol		[2]byte
	hardvéraddressVeľkosť	byte
	protocoladdressVeľkosť	byte
	príkaz			[2]byte

	zdrojmacaddress	[6]byte
	zdrojipaddress	[4]byte
	cieľmacaddress	[6]byte
	cieľipaddress	[4]byte
}

var arpmesgVeľkosť uint32 = (64+92+64)/8 + 2

type ArpSpráva struct {
	hardvérTyp		uint16
	protocol		uint16
	hardvéraddressVeľkosť	uint8
	protocoladdressVeľkosť	uint8
	príkaz			uint16

	zdrojmacaddress	uint64
	zdrojipaddress	uint32
	cieľmacaddress	uint64
	cieľipaddress	uint32
}

func (vlastný *ArpSpráva) Init(buffer_2 *ArpSprávabuffer) {

	vlastný.hardvérTyp = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.hardvérTyp))
	vlastný.protocol = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.protocol))
	vlastný.hardvéraddressVeľkosť = byte(buffer_2.hardvéraddressVeľkosť)
	vlastný.protocoladdressVeľkosť = byte(buffer_2.protocoladdressVeľkosť)
	vlastný.príkaz = Unsignedinteger16r(Poletounsignedinteger16(buffer_2.príkaz))

	vlastný.zdrojmacaddress = Unsignedinteger48r(Poletounsignedinteger48(buffer_2.zdrojmacaddress))
	vlastný.zdrojipaddress = Unsignedinteger32r(Poletounsignedinteger32(buffer_2.zdrojipaddress))
	vlastný.cieľmacaddress = Unsignedinteger48r(Poletounsignedinteger48(buffer_2.cieľmacaddress))
	vlastný.cieľipaddress = Unsignedinteger32r(Poletounsignedinteger32(buffer_2.cieľipaddress))
}
func (vlastný *ArpSpráva) Sadabuffer(buffer_2 *ArpSprávabuffer) {
	buffer_2.hardvérTyp = Unsignedinteger16toPole(vlastný.hardvérTyp)
	buffer_2.protocol = Unsignedinteger16toPole(vlastný.protocol)
	buffer_2.hardvéraddressVeľkosť = uint8(vlastný.hardvéraddressVeľkosť)
	buffer_2.protocoladdressVeľkosť = uint8(vlastný.protocoladdressVeľkosť)

	buffer_2.príkaz = Unsignedinteger16toPole(vlastný.príkaz)
	buffer_2.zdrojmacaddress = Unsignedinteger48toPole(vlastný.zdrojmacaddress)
	buffer_2.zdrojipaddress = Unsignedinteger32toPole(vlastný.zdrojipaddress)
	buffer_2.cieľmacaddress = Unsignedinteger48toPole(vlastný.cieľmacaddress)
	buffer_2.cieľipaddress = Unsignedinteger32toPole(vlastný.cieľipaddress)
}

type ArpethernetRámechandler struct {
	TEthernetRámechandler
}

var arpprovider Arpprovider
var ethernetRámecprovider TEthernetRámecprovider

func (vlastný *ArpethernetRámechandler) EthernetRámecreceivewhen(dataKurzor uintptr, veľkosť int) bool {
	arpKonzola.MTlačiťxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRámecreceivewhen(dataKurzor, uint32(veľkosť))

}
func (vlastný *ArpethernetRámechandler) Poslať(cieľmacbe uint64, dataKurzor uintptr, veľkosť uint32) {
	arpKonzola.MTlačiťxy([]byte("arp send:"), 0, 24)
	var ethernetTypbe = Unsignedinteger16r(0x0806)
	vlastný.TEthernetRámechandler.RámecPoslať(cieľmacbe, ethernetTypbe, dataKurzor, veľkosť)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	číslocachepoložka	int

	handler	IEthernetRámechandler
}

var handler IEthernetRámechandler

func (vlastný *Arpprovider) Init(backend TEthernetRámecprovider, userhandler IEthernetRámechandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Sadahandler(userhandler, 0x0806)
	vlastný.číslocachepoložka = 0
	arpprovider = *vlastný

}

func (vlastný *Arpprovider) EthernetRámecreceivewhen(dataKurzor uintptr, veľkosť uint32) bool {

	if veľkosť < arpmesgVeľkosť {
		return false
	}
	var arpbuffer *ArpSprávabuffer = (*ArpSprávabuffer)(Pointer(dataKurzor))
	var arp ArpSpráva = ArpSpráva{}
	arp.Init(arpbuffer)

	if arp.hardvérTyp == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardvéraddressVeľkosť == 6 && arp.protocoladdressVeľkosť == 4 && uint64(arp.cieľipaddress) == handler.Getipaddress() {

			arpKonzola.MTlačiť([]byte("arp onetherframe"))
			arpKonzola.MUnsignedinteger16Tlačiť(arp.protocol)
			arpKonzola.MTlačiť([]byte(":"))
			arpKonzola.MUnsignedinteger64Tlačiť(uint64(arp.cieľmacaddress))
			arpKonzola.MTlačiť([]byte(":"))
			arpKonzola.MUnsignedinteger16Tlačiť(arp.príkaz)
			arpKonzola.MTlačiť([]byte(":"))
			arpKonzola.MUnsignedinteger64Tlačiť(handler.Getmacaddress())

			switch arp.príkaz {
			case 0x0100:

				if vlastný.Getmaczcache(arp.zdrojipaddress) == 0xFFFFFFFFFFFF {
					if vlastný.číslocachepoložka < 128 {
						vlastný.Ipcache[vlastný.číslocachepoložka] = arp.zdrojipaddress
						vlastný.Maccache[vlastný.číslocachepoložka] = arp.zdrojmacaddress
						vlastný.číslocachepoložka++
					}
				}
				arp.príkaz = 0x0200
				arp.cieľipaddress = arp.zdrojipaddress
				arp.cieľmacaddress = arp.zdrojmacaddress
				arp.zdrojipaddress = uint32(handler.Getipaddress())
				arp.zdrojmacaddress = handler.Getmacaddress()
				arp.Sadabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonzola.MTlačiť(([]byte)("self.numCacheEntries"))

				if vlastný.číslocachepoložka < 128 {
					vlastný.Ipcache[vlastný.číslocachepoložka] = arp.zdrojipaddress
					vlastný.Maccache[vlastný.číslocachepoložka] = arp.zdrojmacaddress
					vlastný.číslocachepoložka++
				}
				break
			}

		}
	}
	return false

}

func (vlastný *Arpprovider) Broadcastmacaddress(IpSieťbyteorder uint32) {

	var arp ArpSpráva = ArpSpráva{}
	arp.hardvérTyp = 0x0100
	arp.protocol = 0x0008
	arp.hardvéraddressVeľkosť = 6
	arp.protocoladdressVeľkosť = 4
	arp.príkaz = 0x0200

	arp.zdrojipaddress = uint32(handler.Getipaddress())

	arp.cieľmacaddress = vlastný.Resolve(IpSieťbyteorder)
	arp.cieľipaddress = IpSieťbyteorder
	arpKonzola.MTlačiťxy([]byte("broad mac"), 0, 15)

	arp.zdrojmacaddress = handler.Getmacaddress()

	var arpbuffer ArpSprávabuffer = ArpSprávabuffer{}
	arp.Sadabuffer(&arpbuffer)

	var kurzor uintptr = uintptr(Pointer(&arpbuffer))
	handler.Poslať(arp.cieľmacaddress, kurzor, arpmesgVeľkosť)
}
func (vlastný *Arpprovider) Requestmacaddress(IpSieťbyteorder uint32) {

	var arp ArpSpráva = ArpSpráva{}
	arp.hardvérTyp = 0x0100

	arp.protocol = 0x0008
	arp.hardvéraddressVeľkosť = 6
	arp.protocoladdressVeľkosť = 4
	arp.príkaz = 0x0100

	arp.zdrojmacaddress = handler.Getmacaddress()
	arp.zdrojipaddress = uint32(handler.Getipaddress())

	arp.cieľmacaddress = 0xFFFFFFFFFFFF
	arp.cieľipaddress = IpSieťbyteorder

	var arpbuffer ArpSprávabuffer = ArpSprávabuffer{}
	arp.Sadabuffer(&arpbuffer)

	var kurzor uintptr = uintptr(Pointer(&arpbuffer))
	handler.Poslať(arp.cieľmacaddress, kurzor, arpmesgVeľkosť)
}
func (vlastný *Arpprovider) OtestovaťTlačiť(data *[]byte, veľkosť uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonzola.MTlačiťxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonzola.MHexadecimalTlačiť(buffer_2[i])
		arpKonzola.MTlačiť([]byte(":"))
	}
	arpKonzola.MTlačiť([]byte("]"))
}

func (vlastný *Arpprovider) Getmaczcache(IpSieťbyteorder uint32) uint64 {
	for i := 0; i < vlastný.číslocachepoložka; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonzola.MTlačiť(([]byte)("["))
		arpKonzola.MUnsignedinteger32Tlačiť(vlastný.Ipcache[i])
		arpKonzola.MTlačiť(([]byte)(":"))
		arpKonzola.MUnsignedinteger32Tlačiť(IpSieťbyteorder)
		arpKonzola.MTlačiť(([]byte)(":"))
		arpKonzola.MTlačiť(([]byte)(":"))
		arpKonzola.MUnsignedinteger64Tlačiť(vlastný.Maccache[i])
		arpKonzola.MTlačiť(([]byte)("]\n"))

		if vlastný.Ipcache[i] == IpSieťbyteorder {
			arpKonzola.MTlačiť([]byte("getmacfromcache"))
			return vlastný.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (vlastný *Arpprovider) Resolve(IpSieťbyteorder uint32) uint64 {
	var result uint64 = vlastný.Getmaczcache(IpSieťbyteorder)
	if result == 0xFFFFFFFFFFFF {
		vlastný.Requestmacaddress(IpSieťbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = vlastný.Getmaczcache(IpSieťbyteorder)

	}

	return result
}
