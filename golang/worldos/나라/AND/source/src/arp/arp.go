/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "consola"
import . "cableMarc"
import . "util"

var arpConsola TConsola = TConsola{}

type ArpMissatgebuffer struct {
	maquinariTipus		[2]byte
	protocol		[2]byte
	maquinariAdreçaMida	byte
	protocolAdreçaMida	byte
	ordre			[2]byte

	origenmacAdreça		[6]byte
	origenipAdreça		[4]byte
	destinaciómacAdreça	[6]byte
	destinacióipAdreça	[4]byte
}

var arpmesgMida uint32 = (64+92+64)/8 + 2

type ArpMissatge struct {
	maquinariTipus		uint16
	protocol		uint16
	maquinariAdreçaMida	uint8
	protocolAdreçaMida	uint8
	ordre			uint16

	origenmacAdreça		uint64
	origenipAdreça		uint32
	destinaciómacAdreça	uint64
	destinacióipAdreça	uint32
}

func (unmateix *ArpMissatge) Init(buffer_2 *ArpMissatgebuffer) {

	unmateix.maquinariTipus = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.maquinariTipus))
	unmateix.protocol = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.protocol))
	unmateix.maquinariAdreçaMida = byte(buffer_2.maquinariAdreçaMida)
	unmateix.protocolAdreçaMida = byte(buffer_2.protocolAdreçaMida)
	unmateix.ordre = Unsignedinteger16r(Matriutounsignedinteger16(buffer_2.ordre))

	unmateix.origenmacAdreça = Unsignedinteger48r(Matriutounsignedinteger48(buffer_2.origenmacAdreça))
	unmateix.origenipAdreça = Unsignedinteger32r(Matriutounsignedinteger32(buffer_2.origenipAdreça))
	unmateix.destinaciómacAdreça = Unsignedinteger48r(Matriutounsignedinteger48(buffer_2.destinaciómacAdreça))
	unmateix.destinacióipAdreça = Unsignedinteger32r(Matriutounsignedinteger32(buffer_2.destinacióipAdreça))
}
func (unmateix *ArpMissatge) Estableixbuffer(buffer_2 *ArpMissatgebuffer) {
	buffer_2.maquinariTipus = Unsignedinteger16toMatriu(unmateix.maquinariTipus)
	buffer_2.protocol = Unsignedinteger16toMatriu(unmateix.protocol)
	buffer_2.maquinariAdreçaMida = uint8(unmateix.maquinariAdreçaMida)
	buffer_2.protocolAdreçaMida = uint8(unmateix.protocolAdreçaMida)

	buffer_2.ordre = Unsignedinteger16toMatriu(unmateix.ordre)
	buffer_2.origenmacAdreça = Unsignedinteger48toMatriu(unmateix.origenmacAdreça)
	buffer_2.origenipAdreça = Unsignedinteger32toMatriu(unmateix.origenipAdreça)
	buffer_2.destinaciómacAdreça = Unsignedinteger48toMatriu(unmateix.destinaciómacAdreça)
	buffer_2.destinacióipAdreça = Unsignedinteger32toMatriu(unmateix.destinacióipAdreça)
}

type ArpCableMarchandler struct {
	TCableMarchandler
}

var arpprovider Arpprovider
var cableMarcprovider TCableMarcprovider

func (unmateix *ArpCableMarchandler) CableMarcreceivewhen(dataPunter uintptr, mida int) bool {
	arpConsola.MImprimeixxy([]byte("arp recv:"), 0, 23)
	return arpprovider.CableMarcreceivewhen(dataPunter, uint32(mida))

}
func (unmateix *ArpCableMarchandler) Envia(destinaciómacbe uint64, dataPunter uintptr, mida uint32) {
	arpConsola.MImprimeixxy([]byte("arp send:"), 0, 24)
	var cableTipusbe = Unsignedinteger16r(0x0806)
	unmateix.TCableMarchandler.MarcEnvia(destinaciómacbe, cableTipusbe, dataPunter, mida)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	nombrecacheentrada	int

	handler	ICableMarchandler
}

var handler ICableMarchandler

func (unmateix *Arpprovider) Init(backend TCableMarcprovider, userhandler ICableMarchandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Estableixhandler(userhandler, 0x0806)
	unmateix.nombrecacheentrada = 0
	arpprovider = *unmateix

}

func (unmateix *Arpprovider) CableMarcreceivewhen(dataPunter uintptr, mida uint32) bool {

	if mida < arpmesgMida {
		return false
	}
	var arpbuffer *ArpMissatgebuffer = (*ArpMissatgebuffer)(Pointer(dataPunter))
	var arp ArpMissatge = ArpMissatge{}
	arp.Init(arpbuffer)

	if arp.maquinariTipus == 0x0100 {

		if arp.protocol == 0x0008 && arp.maquinariAdreçaMida == 6 && arp.protocolAdreçaMida == 4 && uint64(arp.destinacióipAdreça) == handler.GetipAdreça() {

			arpConsola.MImprimeix([]byte("arp onetherframe"))
			arpConsola.MUnsignedinteger16Imprimeix(arp.protocol)
			arpConsola.MImprimeix([]byte(":"))
			arpConsola.MUnsignedinteger64Imprimeix(uint64(arp.destinaciómacAdreça))
			arpConsola.MImprimeix([]byte(":"))
			arpConsola.MUnsignedinteger16Imprimeix(arp.ordre)
			arpConsola.MImprimeix([]byte(":"))
			arpConsola.MUnsignedinteger64Imprimeix(handler.GetmacAdreça())

			switch arp.ordre {
			case 0x0100:

				if unmateix.Getmacdesdecache(arp.origenipAdreça) == 0xFFFFFFFFFFFF {
					if unmateix.nombrecacheentrada < 128 {
						unmateix.Ipcache[unmateix.nombrecacheentrada] = arp.origenipAdreça
						unmateix.Maccache[unmateix.nombrecacheentrada] = arp.origenmacAdreça
						unmateix.nombrecacheentrada++
					}
				}
				arp.ordre = 0x0200
				arp.destinacióipAdreça = arp.origenipAdreça
				arp.destinaciómacAdreça = arp.origenmacAdreça
				arp.origenipAdreça = uint32(handler.GetipAdreça())
				arp.origenmacAdreça = handler.GetmacAdreça()
				arp.Estableixbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpConsola.MImprimeix(([]byte)("self.numCacheEntries"))

				if unmateix.nombrecacheentrada < 128 {
					unmateix.Ipcache[unmateix.nombrecacheentrada] = arp.origenipAdreça
					unmateix.Maccache[unmateix.nombrecacheentrada] = arp.origenmacAdreça
					unmateix.nombrecacheentrada++
				}
				break
			}

		}
	}
	return false

}

func (unmateix *Arpprovider) BroadcastmacAdreça(IpXarxabyteorder uint32) {

	var arp ArpMissatge = ArpMissatge{}
	arp.maquinariTipus = 0x0100
	arp.protocol = 0x0008
	arp.maquinariAdreçaMida = 6
	arp.protocolAdreçaMida = 4
	arp.ordre = 0x0200

	arp.origenipAdreça = uint32(handler.GetipAdreça())

	arp.destinaciómacAdreça = unmateix.Resolve(IpXarxabyteorder)
	arp.destinacióipAdreça = IpXarxabyteorder
	arpConsola.MImprimeixxy([]byte("broad mac"), 0, 15)

	arp.origenmacAdreça = handler.GetmacAdreça()

	var arpbuffer ArpMissatgebuffer = ArpMissatgebuffer{}
	arp.Estableixbuffer(&arpbuffer)

	var punter uintptr = uintptr(Pointer(&arpbuffer))
	handler.Envia(arp.destinaciómacAdreça, punter, arpmesgMida)
}
func (unmateix *Arpprovider) RequestmacAdreça(IpXarxabyteorder uint32) {

	var arp ArpMissatge = ArpMissatge{}
	arp.maquinariTipus = 0x0100

	arp.protocol = 0x0008
	arp.maquinariAdreçaMida = 6
	arp.protocolAdreçaMida = 4
	arp.ordre = 0x0100

	arp.origenmacAdreça = handler.GetmacAdreça()
	arp.origenipAdreça = uint32(handler.GetipAdreça())

	arp.destinaciómacAdreça = 0xFFFFFFFFFFFF
	arp.destinacióipAdreça = IpXarxabyteorder

	var arpbuffer ArpMissatgebuffer = ArpMissatgebuffer{}
	arp.Estableixbuffer(&arpbuffer)

	var punter uintptr = uintptr(Pointer(&arpbuffer))
	handler.Envia(arp.destinaciómacAdreça, punter, arpmesgMida)
}
func (unmateix *Arpprovider) ProvaImprimeix(data *[]byte, mida uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpConsola.MImprimeixxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpConsola.MHexadecimalImprimeix(buffer_2[i])
		arpConsola.MImprimeix([]byte(":"))
	}
	arpConsola.MImprimeix([]byte("]"))
}

func (unmateix *Arpprovider) Getmacdesdecache(IpXarxabyteorder uint32) uint64 {
	for i := 0; i < unmateix.nombrecacheentrada; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpConsola.MImprimeix(([]byte)("["))
		arpConsola.MUnsignedinteger32Imprimeix(unmateix.Ipcache[i])
		arpConsola.MImprimeix(([]byte)(":"))
		arpConsola.MUnsignedinteger32Imprimeix(IpXarxabyteorder)
		arpConsola.MImprimeix(([]byte)(":"))
		arpConsola.MImprimeix(([]byte)(":"))
		arpConsola.MUnsignedinteger64Imprimeix(unmateix.Maccache[i])
		arpConsola.MImprimeix(([]byte)("]\n"))

		if unmateix.Ipcache[i] == IpXarxabyteorder {
			arpConsola.MImprimeix([]byte("getmacfromcache"))
			return unmateix.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (unmateix *Arpprovider) Resolve(IpXarxabyteorder uint32) uint64 {
	var rESULTAT uint64 = unmateix.Getmacdesdecache(IpXarxabyteorder)
	if rESULTAT == 0xFFFFFFFFFFFF {
		unmateix.RequestmacAdreça(IpXarxabyteorder)
	}
	for i := 0; i < 128 && rESULTAT == 0xFFFFFFFFFFFF; i++ {
		rESULTAT = unmateix.Getmacdesdecache(IpXarxabyteorder)

	}

	return rESULTAT
}
