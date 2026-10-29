/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konsola"
import . "ramka_sieci_o_wspólnym_medium"
import . "util"

var arpKonsola TKonsola = TKonsola{}

type ArpWiadomośćbuffer struct {
	sprzętTyp		[2]byte
	protocol		[2]byte
	sprzętAdresRozmiar	byte
	protocolAdresRozmiar	byte
	polecenie		[2]byte

	źródłomacAdres	[6]byte
	źródłoipAdres	[4]byte
	celmacAdres	[6]byte
	celipAdres	[4]byte
}

var arpmesgRozmiar uint32 = (64+92+64)/8 + 2

type ArpWiadomość struct {
	sprzętTyp		uint16
	protocol		uint16
	sprzętAdresRozmiar	uint8
	protocolAdresRozmiar	uint8
	polecenie		uint16

	źródłomacAdres	uint64
	źródłoipAdres	uint32
	celmacAdres	uint64
	celipAdres	uint32
}

func (bieżący *ArpWiadomość) Init(buffer_2 *ArpWiadomośćbuffer) {

	bieżący.sprzętTyp = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.sprzętTyp))
	bieżący.protocol = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.protocol))
	bieżący.sprzętAdresRozmiar = byte(buffer_2.sprzętAdresRozmiar)
	bieżący.protocolAdresRozmiar = byte(buffer_2.protocolAdresRozmiar)
	bieżący.polecenie = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.polecenie))

	bieżący.źródłomacAdres = Unsignedinteger48r(Tablicatounsignedinteger48(buffer_2.źródłomacAdres))
	bieżący.źródłoipAdres = Unsignedinteger32r(Tablicatounsignedinteger32(buffer_2.źródłoipAdres))
	bieżący.celmacAdres = Unsignedinteger48r(Tablicatounsignedinteger48(buffer_2.celmacAdres))
	bieżący.celipAdres = Unsignedinteger32r(Tablicatounsignedinteger32(buffer_2.celipAdres))
}
func (bieżący *ArpWiadomość) Zbiórbuffer(buffer_2 *ArpWiadomośćbuffer) {
	buffer_2.sprzętTyp = Unsignedinteger16toTablica(bieżący.sprzętTyp)
	buffer_2.protocol = Unsignedinteger16toTablica(bieżący.protocol)
	buffer_2.sprzętAdresRozmiar = uint8(bieżący.sprzętAdresRozmiar)
	buffer_2.protocolAdresRozmiar = uint8(bieżący.protocolAdresRozmiar)

	buffer_2.polecenie = Unsignedinteger16toTablica(bieżący.polecenie)
	buffer_2.źródłomacAdres = Unsignedinteger48toTablica(bieżący.źródłomacAdres)
	buffer_2.źródłoipAdres = Unsignedinteger32toTablica(bieżący.źródłoipAdres)
	buffer_2.celmacAdres = Unsignedinteger48toTablica(bieżący.celmacAdres)
	buffer_2.celipAdres = Unsignedinteger32toTablica(bieżący.celipAdres)
}

type ArpethernetRamkahandler struct {
	TEthernetRamkahandler
}

var arpprovider Arpprovider
var dostawca_ramek_sieci_o_wspólnym_medium TDostawca_ramek_sieci_o_wspólnym_medium

func (bieżący *ArpethernetRamkahandler) EthernetRamkareceivewhen(dataKursor uintptr, rozmiar int) bool {
	arpKonsola.MWydrukujxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRamkareceivewhen(dataKursor, uint32(rozmiar))

}
func (bieżący *ArpethernetRamkahandler) Wyślij(celmacbe uint64, dataKursor uintptr, rozmiar uint32) {
	arpKonsola.MWydrukujxy([]byte("arp send:"), 0, 24)
	var ethernetTypbe = Unsignedinteger16r(0x0806)
	bieżący.TEthernetRamkahandler.RamkaWyślij(celmacbe, ethernetTypbe, dataKursor, rozmiar)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	liczbacachewpis	int

	handler	IEthernetRamkahandler
}

var handler IEthernetRamkahandler

func (bieżący *Arpprovider) Init(backend TDostawca_ramek_sieci_o_wspólnym_medium, userhandler IEthernetRamkahandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Zbiórhandler(userhandler, 0x0806)
	bieżący.liczbacachewpis = 0
	arpprovider = *bieżący

}

func (bieżący *Arpprovider) EthernetRamkareceivewhen(dataKursor uintptr, rozmiar uint32) bool {

	if rozmiar < arpmesgRozmiar {
		return false
	}
	var arpbuffer *ArpWiadomośćbuffer = (*ArpWiadomośćbuffer)(Pointer(dataKursor))
	var arp ArpWiadomość = ArpWiadomość{}
	arp.Init(arpbuffer)

	if arp.sprzętTyp == 0x0100 {

		if arp.protocol == 0x0008 && arp.sprzętAdresRozmiar == 6 && arp.protocolAdresRozmiar == 4 && uint64(arp.celipAdres) == handler.GetipAdres() {

			arpKonsola.MWydrukuj([]byte("arp onetherframe"))
			arpKonsola.MUnsignedinteger16Wydrukuj(arp.protocol)
			arpKonsola.MWydrukuj([]byte(":"))
			arpKonsola.MUnsignedinteger64Wydrukuj(uint64(arp.celmacAdres))
			arpKonsola.MWydrukuj([]byte(":"))
			arpKonsola.MUnsignedinteger16Wydrukuj(arp.polecenie)
			arpKonsola.MWydrukuj([]byte(":"))
			arpKonsola.MUnsignedinteger64Wydrukuj(handler.GetmacAdres())

			switch arp.polecenie {
			case 0x0100:

				if bieżący.Getmaczcache(arp.źródłoipAdres) == 0xFFFFFFFFFFFF {
					if bieżący.liczbacachewpis < 128 {
						bieżący.Ipcache[bieżący.liczbacachewpis] = arp.źródłoipAdres
						bieżący.Maccache[bieżący.liczbacachewpis] = arp.źródłomacAdres
						bieżący.liczbacachewpis++
					}
				}
				arp.polecenie = 0x0200
				arp.celipAdres = arp.źródłoipAdres
				arp.celmacAdres = arp.źródłomacAdres
				arp.źródłoipAdres = uint32(handler.GetipAdres())
				arp.źródłomacAdres = handler.GetmacAdres()
				arp.Zbiórbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsola.MWydrukuj(([]byte)("self.numCacheEntries"))

				if bieżący.liczbacachewpis < 128 {
					bieżący.Ipcache[bieżący.liczbacachewpis] = arp.źródłoipAdres
					bieżący.Maccache[bieżący.liczbacachewpis] = arp.źródłomacAdres
					bieżący.liczbacachewpis++
				}
				break
			}

		}
	}
	return false

}

func (bieżący *Arpprovider) BroadcastmacAdres(IpSiećbyteorder uint32) {

	var arp ArpWiadomość = ArpWiadomość{}
	arp.sprzętTyp = 0x0100
	arp.protocol = 0x0008
	arp.sprzętAdresRozmiar = 6
	arp.protocolAdresRozmiar = 4
	arp.polecenie = 0x0200

	arp.źródłoipAdres = uint32(handler.GetipAdres())

	arp.celmacAdres = bieżący.Resolve(IpSiećbyteorder)
	arp.celipAdres = IpSiećbyteorder
	arpKonsola.MWydrukujxy([]byte("broad mac"), 0, 15)

	arp.źródłomacAdres = handler.GetmacAdres()

	var arpbuffer ArpWiadomośćbuffer = ArpWiadomośćbuffer{}
	arp.Zbiórbuffer(&arpbuffer)

	var odwołanie_do_adresu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Wyślij(arp.celmacAdres, odwołanie_do_adresu, arpmesgRozmiar)
}
func (bieżący *Arpprovider) RequestmacAdres(IpSiećbyteorder uint32) {

	var arp ArpWiadomość = ArpWiadomość{}
	arp.sprzętTyp = 0x0100

	arp.protocol = 0x0008
	arp.sprzętAdresRozmiar = 6
	arp.protocolAdresRozmiar = 4
	arp.polecenie = 0x0100

	arp.źródłomacAdres = handler.GetmacAdres()
	arp.źródłoipAdres = uint32(handler.GetipAdres())

	arp.celmacAdres = 0xFFFFFFFFFFFF
	arp.celipAdres = IpSiećbyteorder

	var arpbuffer ArpWiadomośćbuffer = ArpWiadomośćbuffer{}
	arp.Zbiórbuffer(&arpbuffer)

	var odwołanie_do_adresu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Wyślij(arp.celmacAdres, odwołanie_do_adresu, arpmesgRozmiar)
}
func (bieżący *Arpprovider) PrzetestujWydrukuj(data *[]byte, rozmiar uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsola.MWydrukujxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsola.MHexadecimalWydrukuj(buffer_2[i])
		arpKonsola.MWydrukuj([]byte(":"))
	}
	arpKonsola.MWydrukuj([]byte("]"))
}

func (bieżący *Arpprovider) Getmaczcache(IpSiećbyteorder uint32) uint64 {
	for i := 0; i < bieżący.liczbacachewpis; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsola.MWydrukuj(([]byte)("["))
		arpKonsola.MUnsignedinteger32Wydrukuj(bieżący.Ipcache[i])
		arpKonsola.MWydrukuj(([]byte)(":"))
		arpKonsola.MUnsignedinteger32Wydrukuj(IpSiećbyteorder)
		arpKonsola.MWydrukuj(([]byte)(":"))
		arpKonsola.MWydrukuj(([]byte)(":"))
		arpKonsola.MUnsignedinteger64Wydrukuj(bieżący.Maccache[i])
		arpKonsola.MWydrukuj(([]byte)("]\n"))

		if bieżący.Ipcache[i] == IpSiećbyteorder {
			arpKonsola.MWydrukuj([]byte("getmacfromcache"))
			return bieżący.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (bieżący *Arpprovider) Resolve(IpSiećbyteorder uint32) uint64 {
	var wYNIK uint64 = bieżący.Getmaczcache(IpSiećbyteorder)
	if wYNIK == 0xFFFFFFFFFFFF {
		bieżący.RequestmacAdres(IpSiećbyteorder)
	}
	for i := 0; i < 128 && wYNIK == 0xFFFFFFFFFFFF; i++ {
		wYNIK = bieżący.Getmaczcache(IpSiećbyteorder)

	}

	return wYNIK
}
