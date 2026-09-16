/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konzole"
import . "rámec_sítě_se_sdíleným_médiem"
import . "util"

var arpKonzole TKonzole = TKonzole{}

type ArpZprávabuffer struct {
	hardwareTyp		[2]byte
	protocol		[2]byte
	hardwareAdresaVelikost	byte
	protocolAdresaVelikost	byte
	příkaz			[2]byte

	zdrojmacAdresa	[6]byte
	zdrojipAdresa	[4]byte
	cílmacAdresa	[6]byte
	cílipAdresa	[4]byte
}

var arpmesgVelikost uint32 = (64+92+64)/8 + 2

type ArpZpráva struct {
	hardwareTyp		uint16
	protocol		uint16
	hardwareAdresaVelikost	uint8
	protocolAdresaVelikost	uint8
	příkaz			uint16

	zdrojmacAdresa	uint64
	zdrojipAdresa	uint32
	cílmacAdresa	uint64
	cílipAdresa	uint32
}

func (self *ArpZpráva) Init(buffer_2 *ArpZprávabuffer) {

	self.hardwareTyp = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.hardwareTyp))
	self.protocol = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.protocol))
	self.hardwareAdresaVelikost = byte(buffer_2.hardwareAdresaVelikost)
	self.protocolAdresaVelikost = byte(buffer_2.protocolAdresaVelikost)
	self.příkaz = Unsignedinteger16r(Poledounsignedinteger16(buffer_2.příkaz))

	self.zdrojmacAdresa = Unsignedinteger48r(Poledounsignedinteger48(buffer_2.zdrojmacAdresa))
	self.zdrojipAdresa = Unsignedinteger32r(Poledounsignedinteger32(buffer_2.zdrojipAdresa))
	self.cílmacAdresa = Unsignedinteger48r(Poledounsignedinteger48(buffer_2.cílmacAdresa))
	self.cílipAdresa = Unsignedinteger32r(Poledounsignedinteger32(buffer_2.cílipAdresa))
}
func (self *ArpZpráva) Nastavitbuffer(buffer_2 *ArpZprávabuffer) {
	buffer_2.hardwareTyp = Unsignedinteger16doPole(self.hardwareTyp)
	buffer_2.protocol = Unsignedinteger16doPole(self.protocol)
	buffer_2.hardwareAdresaVelikost = uint8(self.hardwareAdresaVelikost)
	buffer_2.protocolAdresaVelikost = uint8(self.protocolAdresaVelikost)

	buffer_2.příkaz = Unsignedinteger16doPole(self.příkaz)
	buffer_2.zdrojmacAdresa = Unsignedinteger48doPole(self.zdrojmacAdresa)
	buffer_2.zdrojipAdresa = Unsignedinteger32doPole(self.zdrojipAdresa)
	buffer_2.cílmacAdresa = Unsignedinteger48doPole(self.cílmacAdresa)
	buffer_2.cílipAdresa = Unsignedinteger32doPole(self.cílipAdresa)
}

type ArpethernetRámhandler struct {
	TEthernetRámhandler
}

var arpprovider Arpprovider
var poskytovatel_rámců_sítě_se_sdíleným_médiem TPoskytovatel_rámců_sítě_se_sdíleným_médiem

func (self *ArpethernetRámhandler) EthernetRámreceivewhen(dataKurzor uintptr, velikost int) bool {
	arpKonzole.MTisknoutxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRámreceivewhen(dataKurzor, uint32(velikost))

}
func (self *ArpethernetRámhandler) Poslat(cílmacbe uint64, dataKurzor uintptr, velikost uint32) {
	arpKonzole.MTisknoutxy([]byte("arp send:"), 0, 24)
	var ethernetTypbe = Unsignedinteger16r(0x0806)
	self.TEthernetRámhandler.RámPoslat(cílmacbe, ethernetTypbe, dataKurzor, velikost)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	číslocacheZáznam	int

	handler	IEthernetRámhandler
}

var handler IEthernetRámhandler

func (self *Arpprovider) Init(backend TPoskytovatel_rámců_sítě_se_sdíleným_médiem, userhandler IEthernetRámhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Nastavithandler(userhandler, 0x0806)
	self.číslocacheZáznam = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetRámreceivewhen(dataKurzor uintptr, velikost uint32) bool {

	if velikost < arpmesgVelikost {
		return false
	}
	var arpbuffer *ArpZprávabuffer = (*ArpZprávabuffer)(Pointer(dataKurzor))
	var arp ArpZpráva = ArpZpráva{}
	arp.Init(arpbuffer)

	if arp.hardwareTyp == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareAdresaVelikost == 6 && arp.protocolAdresaVelikost == 4 && uint64(arp.cílipAdresa) == handler.GetipAdresa() {

			arpKonzole.MTisknout([]byte("arp onetherframe"))
			arpKonzole.MUnsignedinteger16Tisknout(arp.protocol)
			arpKonzole.MTisknout([]byte(":"))
			arpKonzole.MUnsignedinteger64Tisknout(uint64(arp.cílmacAdresa))
			arpKonzole.MTisknout([]byte(":"))
			arpKonzole.MUnsignedinteger16Tisknout(arp.příkaz)
			arpKonzole.MTisknout([]byte(":"))
			arpKonzole.MUnsignedinteger64Tisknout(handler.GetmacAdresa())

			switch arp.příkaz {
			case 0x0100:

				if self.Getmaczcache(arp.zdrojipAdresa) == 0xFFFFFFFFFFFF {
					if self.číslocacheZáznam < 128 {
						self.Ipcache[self.číslocacheZáznam] = arp.zdrojipAdresa
						self.Maccache[self.číslocacheZáznam] = arp.zdrojmacAdresa
						self.číslocacheZáznam++
					}
				}
				arp.příkaz = 0x0200
				arp.cílipAdresa = arp.zdrojipAdresa
				arp.cílmacAdresa = arp.zdrojmacAdresa
				arp.zdrojipAdresa = uint32(handler.GetipAdresa())
				arp.zdrojmacAdresa = handler.GetmacAdresa()
				arp.Nastavitbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonzole.MTisknout(([]byte)("self.numCacheEntries"))

				if self.číslocacheZáznam < 128 {
					self.Ipcache[self.číslocacheZáznam] = arp.zdrojipAdresa
					self.Maccache[self.číslocacheZáznam] = arp.zdrojmacAdresa
					self.číslocacheZáznam++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) BroadcastmacAdresa(IpSíťbyteorder uint32) {

	var arp ArpZpráva = ArpZpráva{}
	arp.hardwareTyp = 0x0100
	arp.protocol = 0x0008
	arp.hardwareAdresaVelikost = 6
	arp.protocolAdresaVelikost = 4
	arp.příkaz = 0x0200

	arp.zdrojipAdresa = uint32(handler.GetipAdresa())

	arp.cílmacAdresa = self.Resolve(IpSíťbyteorder)
	arp.cílipAdresa = IpSíťbyteorder
	arpKonzole.MTisknoutxy([]byte("broad mac"), 0, 15)

	arp.zdrojmacAdresa = handler.GetmacAdresa()

	var arpbuffer ArpZprávabuffer = ArpZprávabuffer{}
	arp.Nastavitbuffer(&arpbuffer)

	var odkaz_na_adresu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Poslat(arp.cílmacAdresa, odkaz_na_adresu, arpmesgVelikost)
}
func (self *Arpprovider) RequestmacAdresa(IpSíťbyteorder uint32) {

	var arp ArpZpráva = ArpZpráva{}
	arp.hardwareTyp = 0x0100

	arp.protocol = 0x0008
	arp.hardwareAdresaVelikost = 6
	arp.protocolAdresaVelikost = 4
	arp.příkaz = 0x0100

	arp.zdrojmacAdresa = handler.GetmacAdresa()
	arp.zdrojipAdresa = uint32(handler.GetipAdresa())

	arp.cílmacAdresa = 0xFFFFFFFFFFFF
	arp.cílipAdresa = IpSíťbyteorder

	var arpbuffer ArpZprávabuffer = ArpZprávabuffer{}
	arp.Nastavitbuffer(&arpbuffer)

	var odkaz_na_adresu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Poslat(arp.cílmacAdresa, odkaz_na_adresu, arpmesgVelikost)
}
func (self *Arpprovider) OtestovatTisknout(data *[]byte, velikost uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonzole.MTisknoutxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonzole.MHexadecimalTisknout(buffer_2[i])
		arpKonzole.MTisknout([]byte(":"))
	}
	arpKonzole.MTisknout([]byte("]"))
}

func (self *Arpprovider) Getmaczcache(IpSíťbyteorder uint32) uint64 {
	for i := 0; i < self.číslocacheZáznam; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonzole.MTisknout(([]byte)("["))
		arpKonzole.MUnsignedinteger32Tisknout(self.Ipcache[i])
		arpKonzole.MTisknout(([]byte)(":"))
		arpKonzole.MUnsignedinteger32Tisknout(IpSíťbyteorder)
		arpKonzole.MTisknout(([]byte)(":"))
		arpKonzole.MTisknout(([]byte)(":"))
		arpKonzole.MUnsignedinteger64Tisknout(self.Maccache[i])
		arpKonzole.MTisknout(([]byte)("]\n"))

		if self.Ipcache[i] == IpSíťbyteorder {
			arpKonzole.MTisknout([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpSíťbyteorder uint32) uint64 {
	var vÝSLEDEK uint64 = self.Getmaczcache(IpSíťbyteorder)
	if vÝSLEDEK == 0xFFFFFFFFFFFF {
		self.RequestmacAdresa(IpSíťbyteorder)
	}
	for i := 0; i < 128 && vÝSLEDEK == 0xFFFFFFFFFFFF; i++ {
		vÝSLEDEK = self.Getmaczcache(IpSíťbyteorder)

	}

	return vÝSLEDEK
}
