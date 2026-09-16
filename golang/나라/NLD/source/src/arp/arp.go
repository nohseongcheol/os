/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "frame_van_het_gedeelde_medium_netwerk"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpBerichtbuffer struct {
	apparatuurSoort			[2]byte
	protocol			[2]byte
	apparatuuraddressGrootte	byte
	protocoladdressGrootte		byte
	opdracht			[2]byte

	bronmacaddress		[6]byte
	bronipaddress		[4]byte
	bestemmingmacaddress	[6]byte
	bestemmingipaddress	[4]byte
}

var arpmesgGrootte uint32 = (64+92+64)/8 + 2

type ArpBericht struct {
	apparatuurSoort			uint16
	protocol			uint16
	apparatuuraddressGrootte	uint8
	protocoladdressGrootte		uint8
	opdracht			uint16

	bronmacaddress		uint64
	bronipaddress		uint32
	bestemmingmacaddress	uint64
	bestemmingipaddress	uint32
}

func (zelf *ArpBericht) Init(buffer_2 *ArpBerichtbuffer) {

	zelf.apparatuurSoort = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.apparatuurSoort))
	zelf.protocol = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.protocol))
	zelf.apparatuuraddressGrootte = byte(buffer_2.apparatuuraddressGrootte)
	zelf.protocoladdressGrootte = byte(buffer_2.protocoladdressGrootte)
	zelf.opdracht = Unsignedinteger16r(Reeksnaarunsignedinteger16(buffer_2.opdracht))

	zelf.bronmacaddress = Unsignedinteger48r(Reeksnaarunsignedinteger48(buffer_2.bronmacaddress))
	zelf.bronipaddress = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer_2.bronipaddress))
	zelf.bestemmingmacaddress = Unsignedinteger48r(Reeksnaarunsignedinteger48(buffer_2.bestemmingmacaddress))
	zelf.bestemmingipaddress = Unsignedinteger32r(Reeksnaarunsignedinteger32(buffer_2.bestemmingipaddress))
}
func (zelf *ArpBericht) Instellenbuffer(buffer_2 *ArpBerichtbuffer) {
	buffer_2.apparatuurSoort = Unsignedinteger16naarReeks(zelf.apparatuurSoort)
	buffer_2.protocol = Unsignedinteger16naarReeks(zelf.protocol)
	buffer_2.apparatuuraddressGrootte = uint8(zelf.apparatuuraddressGrootte)
	buffer_2.protocoladdressGrootte = uint8(zelf.protocoladdressGrootte)

	buffer_2.opdracht = Unsignedinteger16naarReeks(zelf.opdracht)
	buffer_2.bronmacaddress = Unsignedinteger48naarReeks(zelf.bronmacaddress)
	buffer_2.bronipaddress = Unsignedinteger32naarReeks(zelf.bronipaddress)
	buffer_2.bestemmingmacaddress = Unsignedinteger48naarReeks(zelf.bestemmingmacaddress)
	buffer_2.bestemmingipaddress = Unsignedinteger32naarReeks(zelf.bestemmingipaddress)
}

type Arpethernetframehandler struct {
	TEthernetframehandler
}

var arpprovider Arpprovider
var frameleverancier_van_het_gedeelde_medium_netwerk TFrameleverancier_van_het_gedeelde_medium_netwerk

func (zelf *Arpethernetframehandler) Ethernetframereceivewhen(dataMuisaanwijzer uintptr, grootte int) bool {
	arpconsole.MAfdrukkenxy([]byte("arp recv:"), 0, 23)
	return arpprovider.Ethernetframereceivewhen(dataMuisaanwijzer, uint32(grootte))

}
func (zelf *Arpethernetframehandler) Verzenden(bestemmingmacbe uint64, dataMuisaanwijzer uintptr, grootte uint32) {
	arpconsole.MAfdrukkenxy([]byte("arp send:"), 0, 24)
	var ethernetSoortbe = Unsignedinteger16r(0x0806)
	zelf.TEthernetframehandler.FrameVerzenden(bestemmingmacbe, ethernetSoortbe, dataMuisaanwijzer, grootte)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	getalcacheItem	int

	handler	IEthernetframehandler
}

var handler IEthernetframehandler

func (zelf *Arpprovider) Init(backend TFrameleverancier_van_het_gedeelde_medium_netwerk, userhandler IEthernetframehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Instellenhandler(userhandler, 0x0806)
	zelf.getalcacheItem = 0
	arpprovider = *zelf

}

func (zelf *Arpprovider) Ethernetframereceivewhen(dataMuisaanwijzer uintptr, grootte uint32) bool {

	if grootte < arpmesgGrootte {
		return false
	}
	var arpbuffer *ArpBerichtbuffer = (*ArpBerichtbuffer)(Pointer(dataMuisaanwijzer))
	var arp ArpBericht = ArpBericht{}
	arp.Init(arpbuffer)

	if arp.apparatuurSoort == 0x0100 {

		if arp.protocol == 0x0008 && arp.apparatuuraddressGrootte == 6 && arp.protocoladdressGrootte == 4 && uint64(arp.bestemmingipaddress) == handler.Getipaddress() {

			arpconsole.MAfdrukken([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Afdrukken(arp.protocol)
			arpconsole.MAfdrukken([]byte(":"))
			arpconsole.MUnsignedinteger64Afdrukken(uint64(arp.bestemmingmacaddress))
			arpconsole.MAfdrukken([]byte(":"))
			arpconsole.MUnsignedinteger16Afdrukken(arp.opdracht)
			arpconsole.MAfdrukken([]byte(":"))
			arpconsole.MUnsignedinteger64Afdrukken(handler.Getmacaddress())

			switch arp.opdracht {
			case 0x0100:

				if zelf.Getmacvancache(arp.bronipaddress) == 0xFFFFFFFFFFFF {
					if zelf.getalcacheItem < 128 {
						zelf.Ipcache[zelf.getalcacheItem] = arp.bronipaddress
						zelf.Maccache[zelf.getalcacheItem] = arp.bronmacaddress
						zelf.getalcacheItem++
					}
				}
				arp.opdracht = 0x0200
				arp.bestemmingipaddress = arp.bronipaddress
				arp.bestemmingmacaddress = arp.bronmacaddress
				arp.bronipaddress = uint32(handler.Getipaddress())
				arp.bronmacaddress = handler.Getmacaddress()
				arp.Instellenbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MAfdrukken(([]byte)("self.numCacheEntries"))

				if zelf.getalcacheItem < 128 {
					zelf.Ipcache[zelf.getalcacheItem] = arp.bronipaddress
					zelf.Maccache[zelf.getalcacheItem] = arp.bronmacaddress
					zelf.getalcacheItem++
				}
				break
			}

		}
	}
	return false

}

func (zelf *Arpprovider) Broadcastmacaddress(IpNetwerkbyteorder uint32) {

	var arp ArpBericht = ArpBericht{}
	arp.apparatuurSoort = 0x0100
	arp.protocol = 0x0008
	arp.apparatuuraddressGrootte = 6
	arp.protocoladdressGrootte = 4
	arp.opdracht = 0x0200

	arp.bronipaddress = uint32(handler.Getipaddress())

	arp.bestemmingmacaddress = zelf.Resolve(IpNetwerkbyteorder)
	arp.bestemmingipaddress = IpNetwerkbyteorder
	arpconsole.MAfdrukkenxy([]byte("broad mac"), 0, 15)

	arp.bronmacaddress = handler.Getmacaddress()

	var arpbuffer ArpBerichtbuffer = ArpBerichtbuffer{}
	arp.Instellenbuffer(&arpbuffer)

	var adresverwijzing uintptr = uintptr(Pointer(&arpbuffer))
	handler.Verzenden(arp.bestemmingmacaddress, adresverwijzing, arpmesgGrootte)
}
func (zelf *Arpprovider) Requestmacaddress(IpNetwerkbyteorder uint32) {

	var arp ArpBericht = ArpBericht{}
	arp.apparatuurSoort = 0x0100

	arp.protocol = 0x0008
	arp.apparatuuraddressGrootte = 6
	arp.protocoladdressGrootte = 4
	arp.opdracht = 0x0100

	arp.bronmacaddress = handler.Getmacaddress()
	arp.bronipaddress = uint32(handler.Getipaddress())

	arp.bestemmingmacaddress = 0xFFFFFFFFFFFF
	arp.bestemmingipaddress = IpNetwerkbyteorder

	var arpbuffer ArpBerichtbuffer = ArpBerichtbuffer{}
	arp.Instellenbuffer(&arpbuffer)

	var adresverwijzing uintptr = uintptr(Pointer(&arpbuffer))
	handler.Verzenden(arp.bestemmingmacaddress, adresverwijzing, arpmesgGrootte)
}
func (zelf *Arpprovider) ProefAfdrukken(data *[]byte, grootte uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MAfdrukkenxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalAfdrukken(buffer_2[i])
		arpconsole.MAfdrukken([]byte(":"))
	}
	arpconsole.MAfdrukken([]byte("]"))
}

func (zelf *Arpprovider) Getmacvancache(IpNetwerkbyteorder uint32) uint64 {
	for i := 0; i < zelf.getalcacheItem; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MAfdrukken(([]byte)("["))
		arpconsole.MUnsignedinteger32Afdrukken(zelf.Ipcache[i])
		arpconsole.MAfdrukken(([]byte)(":"))
		arpconsole.MUnsignedinteger32Afdrukken(IpNetwerkbyteorder)
		arpconsole.MAfdrukken(([]byte)(":"))
		arpconsole.MAfdrukken(([]byte)(":"))
		arpconsole.MUnsignedinteger64Afdrukken(zelf.Maccache[i])
		arpconsole.MAfdrukken(([]byte)("]\n"))

		if zelf.Ipcache[i] == IpNetwerkbyteorder {
			arpconsole.MAfdrukken([]byte("getmacfromcache"))
			return zelf.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (zelf *Arpprovider) Resolve(IpNetwerkbyteorder uint32) uint64 {
	var rESULTAAT uint64 = zelf.Getmacvancache(IpNetwerkbyteorder)
	if rESULTAAT == 0xFFFFFFFFFFFF {
		zelf.Requestmacaddress(IpNetwerkbyteorder)
	}
	for i := 0; i < 128 && rESULTAAT == 0xFFFFFFFFFFFF; i++ {
		rESULTAAT = zelf.Getmacvancache(IpNetwerkbyteorder)

	}

	return rESULTAAT
}
