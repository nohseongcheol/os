/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konsolë"
import . "ethernetKornizë"
import . "util"

var arpKonsolë TKonsolë = TKonsolë{}

type ArpMesazhibuffer struct {
	hardwareLloji		[2]byte
	protocol		[2]byte
	hardwareaddressMadhësia	byte
	protocoladdressMadhësia	byte
	urdhër			[2]byte

	burimimacaddress	[6]byte
	burimiipaddress		[4]byte
	destinacionimacaddress	[6]byte
	destinacioniipaddress	[4]byte
}

var arpmesgMadhësia uint32 = (64+92+64)/8 + 2

type ArpMesazhi struct {
	hardwareLloji		uint16
	protocol		uint16
	hardwareaddressMadhësia	uint8
	protocoladdressMadhësia	uint8
	urdhër			uint16

	burimimacaddress	uint64
	burimiipaddress		uint32
	destinacionimacaddress	uint64
	destinacioniipaddress	uint32
}

func (vetvetja *ArpMesazhi) Init(buffer_2 *ArpMesazhibuffer) {

	vetvetja.hardwareLloji = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.hardwareLloji))
	vetvetja.protocol = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.protocol))
	vetvetja.hardwareaddressMadhësia = byte(buffer_2.hardwareaddressMadhësia)
	vetvetja.protocoladdressMadhësia = byte(buffer_2.protocoladdressMadhësia)
	vetvetja.urdhër = Unsignedinteger16r(Rreshtimitounsignedinteger16(buffer_2.urdhër))

	vetvetja.burimimacaddress = Unsignedinteger48r(Rreshtimitounsignedinteger48(buffer_2.burimimacaddress))
	vetvetja.burimiipaddress = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer_2.burimiipaddress))
	vetvetja.destinacionimacaddress = Unsignedinteger48r(Rreshtimitounsignedinteger48(buffer_2.destinacionimacaddress))
	vetvetja.destinacioniipaddress = Unsignedinteger32r(Rreshtimitounsignedinteger32(buffer_2.destinacioniipaddress))
}
func (vetvetja *ArpMesazhi) Caktonibuffer(buffer_2 *ArpMesazhibuffer) {
	buffer_2.hardwareLloji = Unsignedinteger16toRreshtimi(vetvetja.hardwareLloji)
	buffer_2.protocol = Unsignedinteger16toRreshtimi(vetvetja.protocol)
	buffer_2.hardwareaddressMadhësia = uint8(vetvetja.hardwareaddressMadhësia)
	buffer_2.protocoladdressMadhësia = uint8(vetvetja.protocoladdressMadhësia)

	buffer_2.urdhër = Unsignedinteger16toRreshtimi(vetvetja.urdhër)
	buffer_2.burimimacaddress = Unsignedinteger48toRreshtimi(vetvetja.burimimacaddress)
	buffer_2.burimiipaddress = Unsignedinteger32toRreshtimi(vetvetja.burimiipaddress)
	buffer_2.destinacionimacaddress = Unsignedinteger48toRreshtimi(vetvetja.destinacionimacaddress)
	buffer_2.destinacioniipaddress = Unsignedinteger32toRreshtimi(vetvetja.destinacioniipaddress)
}

type ArpethernetKornizëhandler struct {
	TEthernetKornizëhandler
}

var arpprovider Arpprovider
var ethernetKornizëprovider TEthernetKornizëprovider

func (vetvetja *ArpethernetKornizëhandler) EthernetKornizëreceivewhen(dataKursori uintptr, madhësia int) bool {
	arpKonsolë.MPrintoxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetKornizëreceivewhen(dataKursori, uint32(madhësia))

}
func (vetvetja *ArpethernetKornizëhandler) Dërgo(destinacionimacbe uint64, dataKursori uintptr, madhësia uint32) {
	arpKonsolë.MPrintoxy([]byte("arp send:"), 0, 24)
	var ethernetLlojibe = Unsignedinteger16r(0x0806)
	vetvetja.TEthernetKornizëhandler.KornizëDërgo(destinacionimacbe, ethernetLlojibe, dataKursori, madhësia)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IEthernetKornizëhandler
}

var handler IEthernetKornizëhandler

func (vetvetja *Arpprovider) Init(backend TEthernetKornizëprovider, userhandler IEthernetKornizëhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Caktonihandler(userhandler, 0x0806)
	vetvetja.numbercacheentry = 0
	arpprovider = *vetvetja

}

func (vetvetja *Arpprovider) EthernetKornizëreceivewhen(dataKursori uintptr, madhësia uint32) bool {

	if madhësia < arpmesgMadhësia {
		return false
	}
	var arpbuffer *ArpMesazhibuffer = (*ArpMesazhibuffer)(Pointer(dataKursori))
	var arp ArpMesazhi = ArpMesazhi{}
	arp.Init(arpbuffer)

	if arp.hardwareLloji == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressMadhësia == 6 && arp.protocoladdressMadhësia == 4 && uint64(arp.destinacioniipaddress) == handler.Getipaddress() {

			arpKonsolë.MPrinto([]byte("arp onetherframe"))
			arpKonsolë.MUnsignedinteger16Printo(arp.protocol)
			arpKonsolë.MPrinto([]byte(":"))
			arpKonsolë.MUnsignedinteger64Printo(uint64(arp.destinacionimacaddress))
			arpKonsolë.MPrinto([]byte(":"))
			arpKonsolë.MUnsignedinteger16Printo(arp.urdhër)
			arpKonsolë.MPrinto([]byte(":"))
			arpKonsolë.MUnsignedinteger64Printo(handler.Getmacaddress())

			switch arp.urdhër {
			case 0x0100:

				if vetvetja.Getmacfromcache(arp.burimiipaddress) == 0xFFFFFFFFFFFF {
					if vetvetja.numbercacheentry < 128 {
						vetvetja.Ipcache[vetvetja.numbercacheentry] = arp.burimiipaddress
						vetvetja.Maccache[vetvetja.numbercacheentry] = arp.burimimacaddress
						vetvetja.numbercacheentry++
					}
				}
				arp.urdhër = 0x0200
				arp.destinacioniipaddress = arp.burimiipaddress
				arp.destinacionimacaddress = arp.burimimacaddress
				arp.burimiipaddress = uint32(handler.Getipaddress())
				arp.burimimacaddress = handler.Getmacaddress()
				arp.Caktonibuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsolë.MPrinto(([]byte)("self.numCacheEntries"))

				if vetvetja.numbercacheentry < 128 {
					vetvetja.Ipcache[vetvetja.numbercacheentry] = arp.burimiipaddress
					vetvetja.Maccache[vetvetja.numbercacheentry] = arp.burimimacaddress
					vetvetja.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (vetvetja *Arpprovider) Broadcastmacaddress(IpRrjetibyteorder uint32) {

	var arp ArpMesazhi = ArpMesazhi{}
	arp.hardwareLloji = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressMadhësia = 6
	arp.protocoladdressMadhësia = 4
	arp.urdhër = 0x0200

	arp.burimiipaddress = uint32(handler.Getipaddress())

	arp.destinacionimacaddress = vetvetja.Resolve(IpRrjetibyteorder)
	arp.destinacioniipaddress = IpRrjetibyteorder
	arpKonsolë.MPrintoxy([]byte("broad mac"), 0, 15)

	arp.burimimacaddress = handler.Getmacaddress()

	var arpbuffer ArpMesazhibuffer = ArpMesazhibuffer{}
	arp.Caktonibuffer(&arpbuffer)

	var kursori uintptr = uintptr(Pointer(&arpbuffer))
	handler.Dërgo(arp.destinacionimacaddress, kursori, arpmesgMadhësia)
}
func (vetvetja *Arpprovider) Requestmacaddress(IpRrjetibyteorder uint32) {

	var arp ArpMesazhi = ArpMesazhi{}
	arp.hardwareLloji = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressMadhësia = 6
	arp.protocoladdressMadhësia = 4
	arp.urdhër = 0x0100

	arp.burimimacaddress = handler.Getmacaddress()
	arp.burimiipaddress = uint32(handler.Getipaddress())

	arp.destinacionimacaddress = 0xFFFFFFFFFFFF
	arp.destinacioniipaddress = IpRrjetibyteorder

	var arpbuffer ArpMesazhibuffer = ArpMesazhibuffer{}
	arp.Caktonibuffer(&arpbuffer)

	var kursori uintptr = uintptr(Pointer(&arpbuffer))
	handler.Dërgo(arp.destinacionimacaddress, kursori, arpmesgMadhësia)
}
func (vetvetja *Arpprovider) ProvoPrinto(data *[]byte, madhësia uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsolë.MPrintoxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsolë.MHexadecimalPrinto(buffer_2[i])
		arpKonsolë.MPrinto([]byte(":"))
	}
	arpKonsolë.MPrinto([]byte("]"))
}

func (vetvetja *Arpprovider) Getmacfromcache(IpRrjetibyteorder uint32) uint64 {
	for i := 0; i < vetvetja.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsolë.MPrinto(([]byte)("["))
		arpKonsolë.MUnsignedinteger32Printo(vetvetja.Ipcache[i])
		arpKonsolë.MPrinto(([]byte)(":"))
		arpKonsolë.MUnsignedinteger32Printo(IpRrjetibyteorder)
		arpKonsolë.MPrinto(([]byte)(":"))
		arpKonsolë.MPrinto(([]byte)(":"))
		arpKonsolë.MUnsignedinteger64Printo(vetvetja.Maccache[i])
		arpKonsolë.MPrinto(([]byte)("]\n"))

		if vetvetja.Ipcache[i] == IpRrjetibyteorder {
			arpKonsolë.MPrinto([]byte("getmacfromcache"))
			return vetvetja.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (vetvetja *Arpprovider) Resolve(IpRrjetibyteorder uint32) uint64 {
	var result uint64 = vetvetja.Getmacfromcache(IpRrjetibyteorder)
	if result == 0xFFFFFFFFFFFF {
		vetvetja.Requestmacaddress(IpRrjetibyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = vetvetja.Getmacfromcache(IpRrjetibyteorder)

	}

	return result
}
