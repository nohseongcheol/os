/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "конзола"
import . "жичанавезаОквир"
import . "util"

var arpКонзола TКонзола = TКонзола{}

type Arpпорукаbuffer struct {
	хардверВрста		[2]byte
	protocol		[2]byte
	хардверaddressВеличина	byte
	protocoladdressВеличина	byte
	наредба			[2]byte

	изворmacaddress		[6]byte
	изворipaddress		[4]byte
	одредиштеmacaddress	[6]byte
	одредиштеipaddress	[4]byte
}

var arpmesgВеличина uint32 = (64+92+64)/8 + 2

type Arpпорука struct {
	хардверВрста		uint16
	protocol		uint16
	хардверaddressВеличина	uint8
	protocoladdressВеличина	uint8
	наредба			uint16

	изворmacaddress		uint64
	изворipaddress		uint32
	одредиштеmacaddress	uint64
	одредиштеipaddress	uint32
}

func (исти *Arpпорука) Init(buffer_2 *Arpпорукаbuffer) {

	исти.хардверВрста = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.хардверВрста))
	исти.protocol = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.protocol))
	исти.хардверaddressВеличина = byte(buffer_2.хардверaddressВеличина)
	исти.protocoladdressВеличина = byte(buffer_2.protocoladdressВеличина)
	исти.наредба = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.наредба))

	исти.изворmacaddress = Unsignedinteger48r(Низtounsignedinteger48(buffer_2.изворmacaddress))
	исти.изворipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.изворipaddress))
	исти.одредиштеmacaddress = Unsignedinteger48r(Низtounsignedinteger48(buffer_2.одредиштеmacaddress))
	исти.одредиштеipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.одредиштеipaddress))
}
func (исти *Arpпорука) Скупbuffer(buffer_2 *Arpпорукаbuffer) {
	buffer_2.хардверВрста = Unsignedinteger16toНиз(исти.хардверВрста)
	buffer_2.protocol = Unsignedinteger16toНиз(исти.protocol)
	buffer_2.хардверaddressВеличина = uint8(исти.хардверaddressВеличина)
	buffer_2.protocoladdressВеличина = uint8(исти.protocoladdressВеличина)

	buffer_2.наредба = Unsignedinteger16toНиз(исти.наредба)
	buffer_2.изворmacaddress = Unsignedinteger48toНиз(исти.изворmacaddress)
	buffer_2.изворipaddress = Unsignedinteger32toНиз(исти.изворipaddress)
	buffer_2.одредиштеmacaddress = Unsignedinteger48toНиз(исти.одредиштеmacaddress)
	buffer_2.одредиштеipaddress = Unsignedinteger32toНиз(исти.одредиштеipaddress)
}

type ArpЖичанавезаОквирhandler struct {
	TЖичанавезаОквирhandler
}

var arpprovider Arpprovider
var жичанавезаОквирprovider TЖичанавезаОквирprovider

func (исти *ArpЖичанавезаОквирhandler) ЖичанавезаОквирreceivewhen(dataПоказивач uintptr, величина int) bool {
	arpКонзола.MШтампајxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ЖичанавезаОквирreceivewhen(dataПоказивач, uint32(величина))

}
func (исти *ArpЖичанавезаОквирhandler) Пошаљи(одредиштеmacbe uint64, dataПоказивач uintptr, величина uint32) {
	arpКонзола.MШтампајxy([]byte("arp send:"), 0, 24)
	var жичанавезаВрстаbe = Unsignedinteger16r(0x0806)
	исти.TЖичанавезаОквирhandler.ОквирПошаљи(одредиштеmacbe, жичанавезаВрстаbe, dataПоказивач, величина)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	бројcacheунос	int

	handler	IЖичанавезаОквирhandler
}

var handler IЖичанавезаОквирhandler

func (исти *Arpprovider) Init(backend TЖичанавезаОквирprovider, userhandler IЖичанавезаОквирhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Скупhandler(userhandler, 0x0806)
	исти.бројcacheунос = 0
	arpprovider = *исти

}

func (исти *Arpprovider) ЖичанавезаОквирreceivewhen(dataПоказивач uintptr, величина uint32) bool {

	if величина < arpmesgВеличина {
		return false
	}
	var arpbuffer *Arpпорукаbuffer = (*Arpпорукаbuffer)(Pointer(dataПоказивач))
	var arp Arpпорука = Arpпорука{}
	arp.Init(arpbuffer)

	if arp.хардверВрста == 0x0100 {

		if arp.protocol == 0x0008 && arp.хардверaddressВеличина == 6 && arp.protocoladdressВеличина == 4 && uint64(arp.одредиштеipaddress) == handler.Getipaddress() {

			arpКонзола.MШтампај([]byte("arp onetherframe"))
			arpКонзола.MUnsignedinteger16Штампај(arp.protocol)
			arpКонзола.MШтампај([]byte(":"))
			arpКонзола.MUnsignedinteger64Штампај(uint64(arp.одредиштеmacaddress))
			arpКонзола.MШтампај([]byte(":"))
			arpКонзола.MUnsignedinteger16Штампај(arp.наредба)
			arpКонзола.MШтампај([]byte(":"))
			arpКонзола.MUnsignedinteger64Штампај(handler.Getmacaddress())

			switch arp.наредба {
			case 0x0100:

				if исти.Getmacсаcache(arp.изворipaddress) == 0xFFFFFFFFFFFF {
					if исти.бројcacheунос < 128 {
						исти.Ipcache[исти.бројcacheунос] = arp.изворipaddress
						исти.Maccache[исти.бројcacheунос] = arp.изворmacaddress
						исти.бројcacheунос++
					}
				}
				arp.наредба = 0x0200
				arp.одредиштеipaddress = arp.изворipaddress
				arp.одредиштеmacaddress = arp.изворmacaddress
				arp.изворipaddress = uint32(handler.Getipaddress())
				arp.изворmacaddress = handler.Getmacaddress()
				arp.Скупbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpКонзола.MШтампај(([]byte)("self.numCacheEntries"))

				if исти.бројcacheунос < 128 {
					исти.Ipcache[исти.бројcacheунос] = arp.изворipaddress
					исти.Maccache[исти.бројcacheунос] = arp.изворmacaddress
					исти.бројcacheунос++
				}
				break
			}

		}
	}
	return false

}

func (исти *Arpprovider) Broadcastmacaddress(IpМрежаbyteorder uint32) {

	var arp Arpпорука = Arpпорука{}
	arp.хардверВрста = 0x0100
	arp.protocol = 0x0008
	arp.хардверaddressВеличина = 6
	arp.protocoladdressВеличина = 4
	arp.наредба = 0x0200

	arp.изворipaddress = uint32(handler.Getipaddress())

	arp.одредиштеmacaddress = исти.Resolve(IpМрежаbyteorder)
	arp.одредиштеipaddress = IpМрежаbyteorder
	arpКонзола.MШтампајxy([]byte("broad mac"), 0, 15)

	arp.изворmacaddress = handler.Getmacaddress()

	var arpbuffer Arpпорукаbuffer = Arpпорукаbuffer{}
	arp.Скупbuffer(&arpbuffer)

	var показивач uintptr = uintptr(Pointer(&arpbuffer))
	handler.Пошаљи(arp.одредиштеmacaddress, показивач, arpmesgВеличина)
}
func (исти *Arpprovider) Requestmacaddress(IpМрежаbyteorder uint32) {

	var arp Arpпорука = Arpпорука{}
	arp.хардверВрста = 0x0100

	arp.protocol = 0x0008
	arp.хардверaddressВеличина = 6
	arp.protocoladdressВеличина = 4
	arp.наредба = 0x0100

	arp.изворmacaddress = handler.Getmacaddress()
	arp.изворipaddress = uint32(handler.Getipaddress())

	arp.одредиштеmacaddress = 0xFFFFFFFFFFFF
	arp.одредиштеipaddress = IpМрежаbyteorder

	var arpbuffer Arpпорукаbuffer = Arpпорукаbuffer{}
	arp.Скупbuffer(&arpbuffer)

	var показивач uintptr = uintptr(Pointer(&arpbuffer))
	handler.Пошаљи(arp.одредиштеmacaddress, показивач, arpmesgВеличина)
}
func (исти *Arpprovider) ТестШтампај(data *[]byte, величина uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpКонзола.MШтампајxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpКонзола.MHexadecimalШтампај(buffer_2[i])
		arpКонзола.MШтампај([]byte(":"))
	}
	arpКонзола.MШтампај([]byte("]"))
}

func (исти *Arpprovider) Getmacсаcache(IpМрежаbyteorder uint32) uint64 {
	for i := 0; i < исти.бројcacheунос; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpКонзола.MШтампај(([]byte)("["))
		arpКонзола.MUnsignedinteger32Штампај(исти.Ipcache[i])
		arpКонзола.MШтампај(([]byte)(":"))
		arpКонзола.MUnsignedinteger32Штампај(IpМрежаbyteorder)
		arpКонзола.MШтампај(([]byte)(":"))
		arpКонзола.MШтампај(([]byte)(":"))
		arpКонзола.MUnsignedinteger64Штампај(исти.Maccache[i])
		arpКонзола.MШтампај(([]byte)("]\n"))

		if исти.Ipcache[i] == IpМрежаbyteorder {
			arpКонзола.MШтампај([]byte("getmacfromcache"))
			return исти.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (исти *Arpprovider) Resolve(IpМрежаbyteorder uint32) uint64 {
	var иСХОД uint64 = исти.Getmacсаcache(IpМрежаbyteorder)
	if иСХОД == 0xFFFFFFFFFFFF {
		исти.Requestmacaddress(IpМрежаbyteorder)
	}
	for i := 0; i < 128 && иСХОД == 0xFFFFFFFFFFFF; i++ {
		иСХОД = исти.Getmacсаcache(IpМрежаbyteorder)

	}

	return иСХОД
}
