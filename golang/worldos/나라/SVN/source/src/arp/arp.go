/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetOkvir"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpSporočilobuffer struct {
	strojnaopremaVrsta		[2]byte
	protocol			[2]byte
	strojnaopremaaddressVelikost	byte
	protocoladdressVelikost		byte
	ukaz				[2]byte

	virmacaddress	[6]byte
	viripaddress	[4]byte
	ciljmacaddress	[6]byte
	ciljipaddress	[4]byte
}

var arpmesgVelikost uint32 = (64+92+64)/8 + 2

type ArpSporočilo struct {
	strojnaopremaVrsta		uint16
	protocol			uint16
	strojnaopremaaddressVelikost	uint8
	protocoladdressVelikost		uint8
	ukaz				uint16

	virmacaddress	uint64
	viripaddress	uint32
	ciljmacaddress	uint64
	ciljipaddress	uint32
}

func (sam *ArpSporočilo) Init(buffer_2 *ArpSporočilobuffer) {

	sam.strojnaopremaVrsta = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.strojnaopremaVrsta))
	sam.protocol = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.protocol))
	sam.strojnaopremaaddressVelikost = byte(buffer_2.strojnaopremaaddressVelikost)
	sam.protocoladdressVelikost = byte(buffer_2.protocoladdressVelikost)
	sam.ukaz = Unsignedinteger16r(Poljetounsignedinteger16(buffer_2.ukaz))

	sam.virmacaddress = Unsignedinteger48r(Poljetounsignedinteger48(buffer_2.virmacaddress))
	sam.viripaddress = Unsignedinteger32r(Poljetounsignedinteger32(buffer_2.viripaddress))
	sam.ciljmacaddress = Unsignedinteger48r(Poljetounsignedinteger48(buffer_2.ciljmacaddress))
	sam.ciljipaddress = Unsignedinteger32r(Poljetounsignedinteger32(buffer_2.ciljipaddress))
}
func (sam *ArpSporočilo) Množicabuffer(buffer_2 *ArpSporočilobuffer) {
	buffer_2.strojnaopremaVrsta = Unsignedinteger16toPolje(sam.strojnaopremaVrsta)
	buffer_2.protocol = Unsignedinteger16toPolje(sam.protocol)
	buffer_2.strojnaopremaaddressVelikost = uint8(sam.strojnaopremaaddressVelikost)
	buffer_2.protocoladdressVelikost = uint8(sam.protocoladdressVelikost)

	buffer_2.ukaz = Unsignedinteger16toPolje(sam.ukaz)
	buffer_2.virmacaddress = Unsignedinteger48toPolje(sam.virmacaddress)
	buffer_2.viripaddress = Unsignedinteger32toPolje(sam.viripaddress)
	buffer_2.ciljmacaddress = Unsignedinteger48toPolje(sam.ciljmacaddress)
	buffer_2.ciljipaddress = Unsignedinteger32toPolje(sam.ciljipaddress)
}

type ArpethernetOkvirhandler struct {
	TEthernetOkvirhandler
}

var arpprovider Arpprovider
var ethernetOkvirprovider TEthernetOkvirprovider

func (sam *ArpethernetOkvirhandler) EthernetOkvirreceivewhen(dataKazalnik uintptr, velikost int) bool {
	arpconsole.MNatisnixy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetOkvirreceivewhen(dataKazalnik, uint32(velikost))

}
func (sam *ArpethernetOkvirhandler) Pošlji(ciljmacbe uint64, dataKazalnik uintptr, velikost uint32) {
	arpconsole.MNatisnixy([]byte("arp send:"), 0, 24)
	var ethernetVrstabe = Unsignedinteger16r(0x0806)
	sam.TEthernetOkvirhandler.OkvirPošlji(ciljmacbe, ethernetVrstabe, dataKazalnik, velikost)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	številkacachevnos	int

	handler	IEthernetOkvirhandler
}

var handler IEthernetOkvirhandler

func (sam *Arpprovider) Init(backend TEthernetOkvirprovider, userhandler IEthernetOkvirhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Množicahandler(userhandler, 0x0806)
	sam.številkacachevnos = 0
	arpprovider = *sam

}

func (sam *Arpprovider) EthernetOkvirreceivewhen(dataKazalnik uintptr, velikost uint32) bool {

	if velikost < arpmesgVelikost {
		return false
	}
	var arpbuffer *ArpSporočilobuffer = (*ArpSporočilobuffer)(Pointer(dataKazalnik))
	var arp ArpSporočilo = ArpSporočilo{}
	arp.Init(arpbuffer)

	if arp.strojnaopremaVrsta == 0x0100 {

		if arp.protocol == 0x0008 && arp.strojnaopremaaddressVelikost == 6 && arp.protocoladdressVelikost == 4 && uint64(arp.ciljipaddress) == handler.Getipaddress() {

			arpconsole.MNatisni([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Natisni(arp.protocol)
			arpconsole.MNatisni([]byte(":"))
			arpconsole.MUnsignedinteger64Natisni(uint64(arp.ciljmacaddress))
			arpconsole.MNatisni([]byte(":"))
			arpconsole.MUnsignedinteger16Natisni(arp.ukaz)
			arpconsole.MNatisni([]byte(":"))
			arpconsole.MUnsignedinteger64Natisni(handler.Getmacaddress())

			switch arp.ukaz {
			case 0x0100:

				if sam.Getmacfromcache(arp.viripaddress) == 0xFFFFFFFFFFFF {
					if sam.številkacachevnos < 128 {
						sam.Ipcache[sam.številkacachevnos] = arp.viripaddress
						sam.Maccache[sam.številkacachevnos] = arp.virmacaddress
						sam.številkacachevnos++
					}
				}
				arp.ukaz = 0x0200
				arp.ciljipaddress = arp.viripaddress
				arp.ciljmacaddress = arp.virmacaddress
				arp.viripaddress = uint32(handler.Getipaddress())
				arp.virmacaddress = handler.Getmacaddress()
				arp.Množicabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MNatisni(([]byte)("self.numCacheEntries"))

				if sam.številkacachevnos < 128 {
					sam.Ipcache[sam.številkacachevnos] = arp.viripaddress
					sam.Maccache[sam.številkacachevnos] = arp.virmacaddress
					sam.številkacachevnos++
				}
				break
			}

		}
	}
	return false

}

func (sam *Arpprovider) Broadcastmacaddress(IpOmrežjebyteorder uint32) {

	var arp ArpSporočilo = ArpSporočilo{}
	arp.strojnaopremaVrsta = 0x0100
	arp.protocol = 0x0008
	arp.strojnaopremaaddressVelikost = 6
	arp.protocoladdressVelikost = 4
	arp.ukaz = 0x0200

	arp.viripaddress = uint32(handler.Getipaddress())

	arp.ciljmacaddress = sam.Resolve(IpOmrežjebyteorder)
	arp.ciljipaddress = IpOmrežjebyteorder
	arpconsole.MNatisnixy([]byte("broad mac"), 0, 15)

	arp.virmacaddress = handler.Getmacaddress()

	var arpbuffer ArpSporočilobuffer = ArpSporočilobuffer{}
	arp.Množicabuffer(&arpbuffer)

	var kazalnik uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošlji(arp.ciljmacaddress, kazalnik, arpmesgVelikost)
}
func (sam *Arpprovider) Requestmacaddress(IpOmrežjebyteorder uint32) {

	var arp ArpSporočilo = ArpSporočilo{}
	arp.strojnaopremaVrsta = 0x0100

	arp.protocol = 0x0008
	arp.strojnaopremaaddressVelikost = 6
	arp.protocoladdressVelikost = 4
	arp.ukaz = 0x0100

	arp.virmacaddress = handler.Getmacaddress()
	arp.viripaddress = uint32(handler.Getipaddress())

	arp.ciljmacaddress = 0xFFFFFFFFFFFF
	arp.ciljipaddress = IpOmrežjebyteorder

	var arpbuffer ArpSporočilobuffer = ArpSporočilobuffer{}
	arp.Množicabuffer(&arpbuffer)

	var kazalnik uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošlji(arp.ciljmacaddress, kazalnik, arpmesgVelikost)
}
func (sam *Arpprovider) PreizkusNatisni(data *[]byte, velikost uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MNatisnixy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalNatisni(buffer_2[i])
		arpconsole.MNatisni([]byte(":"))
	}
	arpconsole.MNatisni([]byte("]"))
}

func (sam *Arpprovider) Getmacfromcache(IpOmrežjebyteorder uint32) uint64 {
	for i := 0; i < sam.številkacachevnos; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MNatisni(([]byte)("["))
		arpconsole.MUnsignedinteger32Natisni(sam.Ipcache[i])
		arpconsole.MNatisni(([]byte)(":"))
		arpconsole.MUnsignedinteger32Natisni(IpOmrežjebyteorder)
		arpconsole.MNatisni(([]byte)(":"))
		arpconsole.MNatisni(([]byte)(":"))
		arpconsole.MUnsignedinteger64Natisni(sam.Maccache[i])
		arpconsole.MNatisni(([]byte)("]\n"))

		if sam.Ipcache[i] == IpOmrežjebyteorder {
			arpconsole.MNatisni([]byte("getmacfromcache"))
			return sam.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (sam *Arpprovider) Resolve(IpOmrežjebyteorder uint32) uint64 {
	var rEZULTAT uint64 = sam.Getmacfromcache(IpOmrežjebyteorder)
	if rEZULTAT == 0xFFFFFFFFFFFF {
		sam.Requestmacaddress(IpOmrežjebyteorder)
	}
	for i := 0; i < 128 && rEZULTAT == 0xFFFFFFFFFFFF; i++ {
		rEZULTAT = sam.Getmacfromcache(IpOmrežjebyteorder)

	}

	return rEZULTAT
}
