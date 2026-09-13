package arp

import . "unsafe"
import . "konsol"
import . "ram_i_nät_med_delat_medium"
import . "util"

var arpKonsol TKonsol = TKonsol{}

type ArpMeddelandebuffer struct {
	hårdvaraTyp		[2]byte
	protocol		[2]byte
	hårdvaraAdressStorlek	byte
	protocolAdressStorlek	byte
	kommando		[2]byte

	källamacAdress	[6]byte
	källaipAdress	[4]byte
	målmacAdress	[6]byte
	målipAdress	[4]byte
}

var arpmesgStorlek uint32 = (64+92+64)/8 + 2

type ArpMeddelande struct {
	hårdvaraTyp		uint16
	protocol		uint16
	hårdvaraAdressStorlek	uint8
	protocolAdressStorlek	uint8
	kommando		uint16

	källamacAdress	uint64
	källaipAdress	uint32
	målmacAdress	uint64
	målipAdress	uint32
}

func (själv *ArpMeddelande) Init(buffer_2 *ArpMeddelandebuffer) {

	själv.hårdvaraTyp = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.hårdvaraTyp))
	själv.protocol = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.protocol))
	själv.hårdvaraAdressStorlek = byte(buffer_2.hårdvaraAdressStorlek)
	själv.protocolAdressStorlek = byte(buffer_2.protocolAdressStorlek)
	själv.kommando = Unsignedinteger16r(Vektortounsignedinteger16(buffer_2.kommando))

	själv.källamacAdress = Unsignedinteger48r(Vektortounsignedinteger48(buffer_2.källamacAdress))
	själv.källaipAdress = Unsignedinteger32r(Vektortounsignedinteger32(buffer_2.källaipAdress))
	själv.målmacAdress = Unsignedinteger48r(Vektortounsignedinteger48(buffer_2.målmacAdress))
	själv.målipAdress = Unsignedinteger32r(Vektortounsignedinteger32(buffer_2.målipAdress))
}
func (själv *ArpMeddelande) Mängdbuffer(buffer_2 *ArpMeddelandebuffer) {
	buffer_2.hårdvaraTyp = Unsignedinteger16toVektor(själv.hårdvaraTyp)
	buffer_2.protocol = Unsignedinteger16toVektor(själv.protocol)
	buffer_2.hårdvaraAdressStorlek = uint8(själv.hårdvaraAdressStorlek)
	buffer_2.protocolAdressStorlek = uint8(själv.protocolAdressStorlek)

	buffer_2.kommando = Unsignedinteger16toVektor(själv.kommando)
	buffer_2.källamacAdress = Unsignedinteger48toVektor(själv.källamacAdress)
	buffer_2.källaipAdress = Unsignedinteger32toVektor(själv.källaipAdress)
	buffer_2.målmacAdress = Unsignedinteger48toVektor(själv.målmacAdress)
	buffer_2.målipAdress = Unsignedinteger32toVektor(själv.målipAdress)
}

type ArpethernetRamhandler struct {
	TEthernetRamhandler
}

var arpprovider Arpprovider
var ramleverantör_för_nät_med_delat_medium TRamleverantör_för_nät_med_delat_medium

func (själv *ArpethernetRamhandler) EthernetRamreceivewhen(dataMuspekare uintptr, storlek int) bool {
	arpKonsol.MSkrivutxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRamreceivewhen(dataMuspekare, uint32(storlek))

}
func (själv *ArpethernetRamhandler) Skicka(målmacbe uint64, dataMuspekare uintptr, storlek uint32) {
	arpKonsol.MSkrivutxy([]byte("arp send:"), 0, 24)
	var ethernetTypbe = Unsignedinteger16r(0x0806)
	själv.TEthernetRamhandler.RamSkicka(målmacbe, ethernetTypbe, dataMuspekare, storlek)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	nummercachepost	int

	handler	IEthernetRamhandler
}

var handler IEthernetRamhandler

func (själv *Arpprovider) Init(backend TRamleverantör_för_nät_med_delat_medium, userhandler IEthernetRamhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Mängdhandler(userhandler, 0x0806)
	själv.nummercachepost = 0
	arpprovider = *själv

}

func (själv *Arpprovider) EthernetRamreceivewhen(dataMuspekare uintptr, storlek uint32) bool {

	if storlek < arpmesgStorlek {
		return false
	}
	var arpbuffer *ArpMeddelandebuffer = (*ArpMeddelandebuffer)(Pointer(dataMuspekare))
	var arp ArpMeddelande = ArpMeddelande{}
	arp.Init(arpbuffer)

	if arp.hårdvaraTyp == 0x0100 {

		if arp.protocol == 0x0008 && arp.hårdvaraAdressStorlek == 6 && arp.protocolAdressStorlek == 4 && uint64(arp.målipAdress) == handler.GetipAdress() {

			arpKonsol.MSkrivut([]byte("arp onetherframe"))
			arpKonsol.MUnsignedinteger16Skrivut(arp.protocol)
			arpKonsol.MSkrivut([]byte(":"))
			arpKonsol.MUnsignedinteger64Skrivut(uint64(arp.målmacAdress))
			arpKonsol.MSkrivut([]byte(":"))
			arpKonsol.MUnsignedinteger16Skrivut(arp.kommando)
			arpKonsol.MSkrivut([]byte(":"))
			arpKonsol.MUnsignedinteger64Skrivut(handler.GetmacAdress())

			switch arp.kommando {
			case 0x0100:

				if själv.Getmacfromcache(arp.källaipAdress) == 0xFFFFFFFFFFFF {
					if själv.nummercachepost < 128 {
						själv.Ipcache[själv.nummercachepost] = arp.källaipAdress
						själv.Maccache[själv.nummercachepost] = arp.källamacAdress
						själv.nummercachepost++
					}
				}
				arp.kommando = 0x0200
				arp.målipAdress = arp.källaipAdress
				arp.målmacAdress = arp.källamacAdress
				arp.källaipAdress = uint32(handler.GetipAdress())
				arp.källamacAdress = handler.GetmacAdress()
				arp.Mängdbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsol.MSkrivut(([]byte)("self.numCacheEntries"))

				if själv.nummercachepost < 128 {
					själv.Ipcache[själv.nummercachepost] = arp.källaipAdress
					själv.Maccache[själv.nummercachepost] = arp.källamacAdress
					själv.nummercachepost++
				}
				break
			}

		}
	}
	return false

}

func (själv *Arpprovider) BroadcastmacAdress(IpNätverkbyteorder uint32) {

	var arp ArpMeddelande = ArpMeddelande{}
	arp.hårdvaraTyp = 0x0100
	arp.protocol = 0x0008
	arp.hårdvaraAdressStorlek = 6
	arp.protocolAdressStorlek = 4
	arp.kommando = 0x0200

	arp.källaipAdress = uint32(handler.GetipAdress())

	arp.målmacAdress = själv.Resolve(IpNätverkbyteorder)
	arp.målipAdress = IpNätverkbyteorder
	arpKonsol.MSkrivutxy([]byte("broad mac"), 0, 15)

	arp.källamacAdress = handler.GetmacAdress()

	var arpbuffer ArpMeddelandebuffer = ArpMeddelandebuffer{}
	arp.Mängdbuffer(&arpbuffer)

	var adressreferens uintptr = uintptr(Pointer(&arpbuffer))
	handler.Skicka(arp.målmacAdress, adressreferens, arpmesgStorlek)
}
func (själv *Arpprovider) RequestmacAdress(IpNätverkbyteorder uint32) {

	var arp ArpMeddelande = ArpMeddelande{}
	arp.hårdvaraTyp = 0x0100

	arp.protocol = 0x0008
	arp.hårdvaraAdressStorlek = 6
	arp.protocolAdressStorlek = 4
	arp.kommando = 0x0100

	arp.källamacAdress = handler.GetmacAdress()
	arp.källaipAdress = uint32(handler.GetipAdress())

	arp.målmacAdress = 0xFFFFFFFFFFFF
	arp.målipAdress = IpNätverkbyteorder

	var arpbuffer ArpMeddelandebuffer = ArpMeddelandebuffer{}
	arp.Mängdbuffer(&arpbuffer)

	var adressreferens uintptr = uintptr(Pointer(&arpbuffer))
	handler.Skicka(arp.målmacAdress, adressreferens, arpmesgStorlek)
}
func (själv *Arpprovider) TestaSkrivut(data *[]byte, storlek uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsol.MSkrivutxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsol.MHexadecimalSkrivut(buffer_2[i])
		arpKonsol.MSkrivut([]byte(":"))
	}
	arpKonsol.MSkrivut([]byte("]"))
}

func (själv *Arpprovider) Getmacfromcache(IpNätverkbyteorder uint32) uint64 {
	for i := 0; i < själv.nummercachepost; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsol.MSkrivut(([]byte)("["))
		arpKonsol.MUnsignedinteger32Skrivut(själv.Ipcache[i])
		arpKonsol.MSkrivut(([]byte)(":"))
		arpKonsol.MUnsignedinteger32Skrivut(IpNätverkbyteorder)
		arpKonsol.MSkrivut(([]byte)(":"))
		arpKonsol.MSkrivut(([]byte)(":"))
		arpKonsol.MUnsignedinteger64Skrivut(själv.Maccache[i])
		arpKonsol.MSkrivut(([]byte)("]\n"))

		if själv.Ipcache[i] == IpNätverkbyteorder {
			arpKonsol.MSkrivut([]byte("getmacfromcache"))
			return själv.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (själv *Arpprovider) Resolve(IpNätverkbyteorder uint32) uint64 {
	var rESULTAT uint64 = själv.Getmacfromcache(IpNätverkbyteorder)
	if rESULTAT == 0xFFFFFFFFFFFF {
		själv.RequestmacAdress(IpNätverkbyteorder)
	}
	for i := 0; i < 128 && rESULTAT == 0xFFFFFFFFFFFF; i++ {
		rESULTAT = själv.Getmacfromcache(IpNätverkbyteorder)

	}

	return rESULTAT
}
