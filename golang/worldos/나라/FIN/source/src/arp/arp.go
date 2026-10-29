/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konsoli"
import . "jaetun_siirtotien_verkkokehys"
import . "util"

var arpKonsoli TKonsoli = TKonsoli{}

type ArpViestibuffer struct {
	laitteistoTyyppi	[2]byte
	protocol		[2]byte
	laitteistoaddressKoko	byte
	protocoladdressKoko	byte
	komento			[2]byte

	lähdemacaddress	[6]byte
	lähdeipaddress	[4]byte
	kohdemacaddress	[6]byte
	kohdeipaddress	[4]byte
}

var arpmesgKoko uint32 = (64+92+64)/8 + 2

type ArpViesti struct {
	laitteistoTyyppi	uint16
	protocol		uint16
	laitteistoaddressKoko	uint8
	protocoladdressKoko	uint8
	komento			uint16

	lähdemacaddress	uint64
	lähdeipaddress	uint32
	kohdemacaddress	uint64
	kohdeipaddress	uint32
}

func (itse *ArpViesti) Init(buffer_2 *ArpViestibuffer) {

	itse.laitteistoTyyppi = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.laitteistoTyyppi))
	itse.protocol = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.protocol))
	itse.laitteistoaddressKoko = byte(buffer_2.laitteistoaddressKoko)
	itse.protocoladdressKoko = byte(buffer_2.protocoladdressKoko)
	itse.komento = Unsignedinteger16r(Taulukkotounsignedinteger16(buffer_2.komento))

	itse.lähdemacaddress = Unsignedinteger48r(Taulukkotounsignedinteger48(buffer_2.lähdemacaddress))
	itse.lähdeipaddress = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer_2.lähdeipaddress))
	itse.kohdemacaddress = Unsignedinteger48r(Taulukkotounsignedinteger48(buffer_2.kohdemacaddress))
	itse.kohdeipaddress = Unsignedinteger32r(Taulukkotounsignedinteger32(buffer_2.kohdeipaddress))
}
func (itse *ArpViesti) Asetabuffer(buffer_2 *ArpViestibuffer) {
	buffer_2.laitteistoTyyppi = Unsignedinteger16toTaulukko(itse.laitteistoTyyppi)
	buffer_2.protocol = Unsignedinteger16toTaulukko(itse.protocol)
	buffer_2.laitteistoaddressKoko = uint8(itse.laitteistoaddressKoko)
	buffer_2.protocoladdressKoko = uint8(itse.protocoladdressKoko)

	buffer_2.komento = Unsignedinteger16toTaulukko(itse.komento)
	buffer_2.lähdemacaddress = Unsignedinteger48toTaulukko(itse.lähdemacaddress)
	buffer_2.lähdeipaddress = Unsignedinteger32toTaulukko(itse.lähdeipaddress)
	buffer_2.kohdemacaddress = Unsignedinteger48toTaulukko(itse.kohdemacaddress)
	buffer_2.kohdeipaddress = Unsignedinteger32toTaulukko(itse.kohdeipaddress)
}

type ArpethernetKehyshandler struct {
	TEthernetKehyshandler
}

var arpprovider Arpprovider
var jaetun_siirtotien_verkkokehysten_tarjoaja TJaetun_siirtotien_verkkokehysten_tarjoaja

func (itse *ArpethernetKehyshandler) EthernetKehysreceivewhen(dataOsoitin uintptr, koko int) bool {
	arpKonsoli.MTulostaxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetKehysreceivewhen(dataOsoitin, uint32(koko))

}
func (itse *ArpethernetKehyshandler) Lähetä(kohdemacbe uint64, dataOsoitin uintptr, koko uint32) {
	arpKonsoli.MTulostaxy([]byte("arp send:"), 0, 24)
	var ethernetTyyppibe = Unsignedinteger16r(0x0806)
	itse.TEthernetKehyshandler.KehysLähetä(kohdemacbe, ethernetTyyppibe, dataOsoitin, koko)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numerocachehakusana	int

	handler	IEthernetKehyshandler
}

var handler IEthernetKehyshandler

func (itse *Arpprovider) Init(backend TJaetun_siirtotien_verkkokehysten_tarjoaja, userhandler IEthernetKehyshandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Asetahandler(userhandler, 0x0806)
	itse.numerocachehakusana = 0
	arpprovider = *itse

}

func (itse *Arpprovider) EthernetKehysreceivewhen(dataOsoitin uintptr, koko uint32) bool {

	if koko < arpmesgKoko {
		return false
	}
	var arpbuffer *ArpViestibuffer = (*ArpViestibuffer)(Pointer(dataOsoitin))
	var arp ArpViesti = ArpViesti{}
	arp.Init(arpbuffer)

	if arp.laitteistoTyyppi == 0x0100 {

		if arp.protocol == 0x0008 && arp.laitteistoaddressKoko == 6 && arp.protocoladdressKoko == 4 && uint64(arp.kohdeipaddress) == handler.Getipaddress() {

			arpKonsoli.MTulosta([]byte("arp onetherframe"))
			arpKonsoli.MUnsignedinteger16Tulosta(arp.protocol)
			arpKonsoli.MTulosta([]byte(":"))
			arpKonsoli.MUnsignedinteger64Tulosta(uint64(arp.kohdemacaddress))
			arpKonsoli.MTulosta([]byte(":"))
			arpKonsoli.MUnsignedinteger16Tulosta(arp.komento)
			arpKonsoli.MTulosta([]byte(":"))
			arpKonsoli.MUnsignedinteger64Tulosta(handler.Getmacaddress())

			switch arp.komento {
			case 0x0100:

				if itse.Getmaclähteestäcache(arp.lähdeipaddress) == 0xFFFFFFFFFFFF {
					if itse.numerocachehakusana < 128 {
						itse.Ipcache[itse.numerocachehakusana] = arp.lähdeipaddress
						itse.Maccache[itse.numerocachehakusana] = arp.lähdemacaddress
						itse.numerocachehakusana++
					}
				}
				arp.komento = 0x0200
				arp.kohdeipaddress = arp.lähdeipaddress
				arp.kohdemacaddress = arp.lähdemacaddress
				arp.lähdeipaddress = uint32(handler.Getipaddress())
				arp.lähdemacaddress = handler.Getmacaddress()
				arp.Asetabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsoli.MTulosta(([]byte)("self.numCacheEntries"))

				if itse.numerocachehakusana < 128 {
					itse.Ipcache[itse.numerocachehakusana] = arp.lähdeipaddress
					itse.Maccache[itse.numerocachehakusana] = arp.lähdemacaddress
					itse.numerocachehakusana++
				}
				break
			}

		}
	}
	return false

}

func (itse *Arpprovider) Broadcastmacaddress(IpVerkkobyteorder uint32) {

	var arp ArpViesti = ArpViesti{}
	arp.laitteistoTyyppi = 0x0100
	arp.protocol = 0x0008
	arp.laitteistoaddressKoko = 6
	arp.protocoladdressKoko = 4
	arp.komento = 0x0200

	arp.lähdeipaddress = uint32(handler.Getipaddress())

	arp.kohdemacaddress = itse.Resolve(IpVerkkobyteorder)
	arp.kohdeipaddress = IpVerkkobyteorder
	arpKonsoli.MTulostaxy([]byte("broad mac"), 0, 15)

	arp.lähdemacaddress = handler.Getmacaddress()

	var arpbuffer ArpViestibuffer = ArpViestibuffer{}
	arp.Asetabuffer(&arpbuffer)

	var osoiteviite uintptr = uintptr(Pointer(&arpbuffer))
	handler.Lähetä(arp.kohdemacaddress, osoiteviite, arpmesgKoko)
}
func (itse *Arpprovider) Requestmacaddress(IpVerkkobyteorder uint32) {

	var arp ArpViesti = ArpViesti{}
	arp.laitteistoTyyppi = 0x0100

	arp.protocol = 0x0008
	arp.laitteistoaddressKoko = 6
	arp.protocoladdressKoko = 4
	arp.komento = 0x0100

	arp.lähdemacaddress = handler.Getmacaddress()
	arp.lähdeipaddress = uint32(handler.Getipaddress())

	arp.kohdemacaddress = 0xFFFFFFFFFFFF
	arp.kohdeipaddress = IpVerkkobyteorder

	var arpbuffer ArpViestibuffer = ArpViestibuffer{}
	arp.Asetabuffer(&arpbuffer)

	var osoiteviite uintptr = uintptr(Pointer(&arpbuffer))
	handler.Lähetä(arp.kohdemacaddress, osoiteviite, arpmesgKoko)
}
func (itse *Arpprovider) KokeileTulosta(data *[]byte, koko uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsoli.MTulostaxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsoli.MHexadecimalTulosta(buffer_2[i])
		arpKonsoli.MTulosta([]byte(":"))
	}
	arpKonsoli.MTulosta([]byte("]"))
}

func (itse *Arpprovider) Getmaclähteestäcache(IpVerkkobyteorder uint32) uint64 {
	for i := 0; i < itse.numerocachehakusana; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsoli.MTulosta(([]byte)("["))
		arpKonsoli.MUnsignedinteger32Tulosta(itse.Ipcache[i])
		arpKonsoli.MTulosta(([]byte)(":"))
		arpKonsoli.MUnsignedinteger32Tulosta(IpVerkkobyteorder)
		arpKonsoli.MTulosta(([]byte)(":"))
		arpKonsoli.MTulosta(([]byte)(":"))
		arpKonsoli.MUnsignedinteger64Tulosta(itse.Maccache[i])
		arpKonsoli.MTulosta(([]byte)("]\n"))

		if itse.Ipcache[i] == IpVerkkobyteorder {
			arpKonsoli.MTulosta([]byte("getmacfromcache"))
			return itse.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (itse *Arpprovider) Resolve(IpVerkkobyteorder uint32) uint64 {
	var tULOS uint64 = itse.Getmaclähteestäcache(IpVerkkobyteorder)
	if tULOS == 0xFFFFFFFFFFFF {
		itse.Requestmacaddress(IpVerkkobyteorder)
	}
	for i := 0; i < 128 && tULOS == 0xFFFFFFFFFFFF; i++ {
		tULOS = itse.Getmaclähteestäcache(IpVerkkobyteorder)

	}

	return tULOS
}
