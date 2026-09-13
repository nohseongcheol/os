package arp

import . "unsafe"
import . "конзола"
import . "žičanavezaOkvir"
import . "util"

var arpКонзола TКонзола = TКонзола{}

type Arpпорукаbuffer struct {
	хардверВрста		[2]byte
	protocol		[2]byte
	хардверaddressВеличина	byte
	protocoladdressВеличина	byte
	наредба			[2]byte

	izvormacaddress		[6]byte
	izvoripaddress		[4]byte
	odredištemacaddress	[6]byte
	odredišteipaddress	[4]byte
}

var arpmesgВеличина uint32 = (64+92+64)/8 + 2

type Arpпорука struct {
	хардверВрста		uint16
	protocol		uint16
	хардверaddressВеличина	uint8
	protocoladdressВеличина	uint8
	наредба			uint16

	izvormacaddress		uint64
	izvoripaddress		uint32
	odredištemacaddress	uint64
	odredišteipaddress	uint32
}

func (isti *Arpпорука) Init(buffer_2 *Arpпорукаbuffer) {

	isti.хардверВрста = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.хардверВрста))
	isti.protocol = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.protocol))
	isti.хардверaddressВеличина = byte(buffer_2.хардверaddressВеличина)
	isti.protocoladdressВеличина = byte(buffer_2.protocoladdressВеличина)
	isti.наредба = Unsignedinteger16r(Низtounsignedinteger16(buffer_2.наредба))

	isti.izvormacaddress = Unsignedinteger48r(Низtounsignedinteger48(buffer_2.izvormacaddress))
	isti.izvoripaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.izvoripaddress))
	isti.odredištemacaddress = Unsignedinteger48r(Низtounsignedinteger48(buffer_2.odredištemacaddress))
	isti.odredišteipaddress = Unsignedinteger32r(Низtounsignedinteger32(buffer_2.odredišteipaddress))
}
func (isti *Arpпорука) Скупbuffer(buffer_2 *Arpпорукаbuffer) {
	buffer_2.хардверВрста = Unsignedinteger16toНиз(isti.хардверВрста)
	buffer_2.protocol = Unsignedinteger16toНиз(isti.protocol)
	buffer_2.хардверaddressВеличина = uint8(isti.хардверaddressВеличина)
	buffer_2.protocoladdressВеличина = uint8(isti.protocoladdressВеличина)

	buffer_2.наредба = Unsignedinteger16toНиз(isti.наредба)
	buffer_2.izvormacaddress = Unsignedinteger48toНиз(isti.izvormacaddress)
	buffer_2.izvoripaddress = Unsignedinteger32toНиз(isti.izvoripaddress)
	buffer_2.odredištemacaddress = Unsignedinteger48toНиз(isti.odredištemacaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toНиз(isti.odredišteipaddress)
}

type ArpŽičanavezaOkvirhandler struct {
	TŽičanavezaOkvirhandler
}

var arpprovider Arpprovider
var žičanavezaOkvirprovider TŽičanavezaOkvirprovider

func (isti *ArpŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, величина int) bool {
	arpКонзола.MŠtampajxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ŽičanavezaOkvirreceivewhen(dataPokazivač, uint32(величина))

}
func (isti *ArpŽičanavezaOkvirhandler) Пошаљи(odredištemacbe uint64, dataPokazivač uintptr, величина uint32) {
	arpКонзола.MŠtampajxy([]byte("arp send:"), 0, 24)
	var žičanavezaВрстаbe = Unsignedinteger16r(0x0806)
	isti.TŽičanavezaOkvirhandler.OkvirПошаљи(odredištemacbe, žičanavezaВрстаbe, dataPokazivač, величина)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	бројcacheунос	int

	handler	IŽičanavezaOkvirhandler
}

var handler IŽičanavezaOkvirhandler

func (isti *Arpprovider) Init(backend TŽičanavezaOkvirprovider, userhandler IŽičanavezaOkvirhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Скупhandler(userhandler, 0x0806)
	isti.бројcacheунос = 0
	arpprovider = *isti

}

func (isti *Arpprovider) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, величина uint32) bool {

	if величина < arpmesgВеличина {
		return false
	}
	var arpbuffer *Arpпорукаbuffer = (*Arpпорукаbuffer)(Pointer(dataPokazivač))
	var arp Arpпорука = Arpпорука{}
	arp.Init(arpbuffer)

	if arp.хардверВрста == 0x0100 {

		if arp.protocol == 0x0008 && arp.хардверaddressВеличина == 6 && arp.protocoladdressВеличина == 4 && uint64(arp.odredišteipaddress) == handler.Getipaddress() {

			arpКонзола.MŠtampaj([]byte("arp onetherframe"))
			arpКонзола.MUnsignedinteger16Štampaj(arp.protocol)
			arpКонзола.MŠtampaj([]byte(":"))
			arpКонзола.MUnsignedinteger64Štampaj(uint64(arp.odredištemacaddress))
			arpКонзола.MŠtampaj([]byte(":"))
			arpКонзола.MUnsignedinteger16Štampaj(arp.наредба)
			arpКонзола.MŠtampaj([]byte(":"))
			arpКонзола.MUnsignedinteger64Štampaj(handler.Getmacaddress())

			switch arp.наредба {
			case 0x0100:

				if isti.Getmacsacache(arp.izvoripaddress) == 0xFFFFFFFFFFFF {
					if isti.бројcacheунос < 128 {
						isti.Ipcache[isti.бројcacheунос] = arp.izvoripaddress
						isti.Maccache[isti.бројcacheунос] = arp.izvormacaddress
						isti.бројcacheунос++
					}
				}
				arp.наредба = 0x0200
				arp.odredišteipaddress = arp.izvoripaddress
				arp.odredištemacaddress = arp.izvormacaddress
				arp.izvoripaddress = uint32(handler.Getipaddress())
				arp.izvormacaddress = handler.Getmacaddress()
				arp.Скупbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpКонзола.MŠtampaj(([]byte)("self.numCacheEntries"))

				if isti.бројcacheунос < 128 {
					isti.Ipcache[isti.бројcacheунос] = arp.izvoripaddress
					isti.Maccache[isti.бројcacheунос] = arp.izvormacaddress
					isti.бројcacheунос++
				}
				break
			}

		}
	}
	return false

}

func (isti *Arpprovider) Broadcastmacaddress(IpМрежаbyteorder uint32) {

	var arp Arpпорука = Arpпорука{}
	arp.хардверВрста = 0x0100
	arp.protocol = 0x0008
	arp.хардверaddressВеличина = 6
	arp.protocoladdressВеличина = 4
	arp.наредба = 0x0200

	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = isti.Resolve(IpМрежаbyteorder)
	arp.odredišteipaddress = IpМрежаbyteorder
	arpКонзола.MŠtampajxy([]byte("broad mac"), 0, 15)

	arp.izvormacaddress = handler.Getmacaddress()

	var arpbuffer Arpпорукаbuffer = Arpпорукаbuffer{}
	arp.Скупbuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Пошаљи(arp.odredištemacaddress, pokazivač, arpmesgВеличина)
}
func (isti *Arpprovider) Requestmacaddress(IpМрежаbyteorder uint32) {

	var arp Arpпорука = Arpпорука{}
	arp.хардверВрста = 0x0100

	arp.protocol = 0x0008
	arp.хардверaddressВеличина = 6
	arp.protocoladdressВеличина = 4
	arp.наредба = 0x0100

	arp.izvormacaddress = handler.Getmacaddress()
	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = 0xFFFFFFFFFFFF
	arp.odredišteipaddress = IpМрежаbyteorder

	var arpbuffer Arpпорукаbuffer = Arpпорукаbuffer{}
	arp.Скупbuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Пошаљи(arp.odredištemacaddress, pokazivač, arpmesgВеличина)
}
func (isti *Arpprovider) ТестŠtampaj(data *[]byte, величина uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpКонзола.MŠtampajxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpКонзола.MHexadecimalŠtampaj(buffer_2[i])
		arpКонзола.MŠtampaj([]byte(":"))
	}
	arpКонзола.MŠtampaj([]byte("]"))
}

func (isti *Arpprovider) Getmacsacache(IpМрежаbyteorder uint32) uint64 {
	for i := 0; i < isti.бројcacheунос; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpКонзола.MŠtampaj(([]byte)("["))
		arpКонзола.MUnsignedinteger32Štampaj(isti.Ipcache[i])
		arpКонзола.MŠtampaj(([]byte)(":"))
		arpКонзола.MUnsignedinteger32Štampaj(IpМрежаbyteorder)
		arpКонзола.MŠtampaj(([]byte)(":"))
		arpКонзола.MŠtampaj(([]byte)(":"))
		arpКонзола.MUnsignedinteger64Štampaj(isti.Maccache[i])
		arpКонзола.MŠtampaj(([]byte)("]\n"))

		if isti.Ipcache[i] == IpМрежаbyteorder {
			arpКонзола.MŠtampaj([]byte("getmacfromcache"))
			return isti.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (isti *Arpprovider) Resolve(IpМрежаbyteorder uint32) uint64 {
	var иСХОД uint64 = isti.Getmacsacache(IpМрежаbyteorder)
	if иСХОД == 0xFFFFFFFFFFFF {
		isti.Requestmacaddress(IpМрежаbyteorder)
	}
	for i := 0; i < 128 && иСХОД == 0xFFFFFFFFFFFF; i++ {
		иСХОД = isti.Getmacsacache(IpМрежаbyteorder)

	}

	return иСХОД
}
