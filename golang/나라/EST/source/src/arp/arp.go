package arp

import . "unsafe"
import . "console"
import . "ethernetRaam"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpTeadebuffer struct {
	riistvaraLiik		[2]byte
	protocol		[2]byte
	riistvaraaddressSuurus	byte
	protocoladdressSuurus	byte
	käsk			[2]byte

	aLLIKASmacaddress	[6]byte
	aLLIKASipaddress	[4]byte
	sihtfailmacaddress	[6]byte
	sihtfailipaddress	[4]byte
}

var arpmesgSuurus uint32 = (64+92+64)/8 + 2

type ArpTeade struct {
	riistvaraLiik		uint16
	protocol		uint16
	riistvaraaddressSuurus	uint8
	protocoladdressSuurus	uint8
	käsk			uint16

	aLLIKASmacaddress	uint64
	aLLIKASipaddress	uint32
	sihtfailmacaddress	uint64
	sihtfailipaddress	uint32
}

func (ise *ArpTeade) Init(buffer_2 *ArpTeadebuffer) {

	ise.riistvaraLiik = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.riistvaraLiik))
	ise.protocol = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.protocol))
	ise.riistvaraaddressSuurus = byte(buffer_2.riistvaraaddressSuurus)
	ise.protocoladdressSuurus = byte(buffer_2.protocoladdressSuurus)
	ise.käsk = Unsignedinteger16r(Massiivtounsignedinteger16(buffer_2.käsk))

	ise.aLLIKASmacaddress = Unsignedinteger48r(Massiivtounsignedinteger48(buffer_2.aLLIKASmacaddress))
	ise.aLLIKASipaddress = Unsignedinteger32r(Massiivtounsignedinteger32(buffer_2.aLLIKASipaddress))
	ise.sihtfailmacaddress = Unsignedinteger48r(Massiivtounsignedinteger48(buffer_2.sihtfailmacaddress))
	ise.sihtfailipaddress = Unsignedinteger32r(Massiivtounsignedinteger32(buffer_2.sihtfailipaddress))
}
func (ise *ArpTeade) Määrabuffer(buffer_2 *ArpTeadebuffer) {
	buffer_2.riistvaraLiik = Unsignedinteger16toMassiiv(ise.riistvaraLiik)
	buffer_2.protocol = Unsignedinteger16toMassiiv(ise.protocol)
	buffer_2.riistvaraaddressSuurus = uint8(ise.riistvaraaddressSuurus)
	buffer_2.protocoladdressSuurus = uint8(ise.protocoladdressSuurus)

	buffer_2.käsk = Unsignedinteger16toMassiiv(ise.käsk)
	buffer_2.aLLIKASmacaddress = Unsignedinteger48toMassiiv(ise.aLLIKASmacaddress)
	buffer_2.aLLIKASipaddress = Unsignedinteger32toMassiiv(ise.aLLIKASipaddress)
	buffer_2.sihtfailmacaddress = Unsignedinteger48toMassiiv(ise.sihtfailmacaddress)
	buffer_2.sihtfailipaddress = Unsignedinteger32toMassiiv(ise.sihtfailipaddress)
}

type ArpethernetRaamhandler struct {
	TEthernetRaamhandler
}

var arpprovider Arpprovider
var ethernetRaamprovider TEthernetRaamprovider

func (ise *ArpethernetRaamhandler) EthernetRaamreceivewhen(dataKursor uintptr, suurus int) bool {
	arpconsole.MPrindixy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRaamreceivewhen(dataKursor, uint32(suurus))

}
func (ise *ArpethernetRaamhandler) Saada(sihtfailmacbe uint64, dataKursor uintptr, suurus uint32) {
	arpconsole.MPrindixy([]byte("arp send:"), 0, 24)
	var ethernetLiikbe = Unsignedinteger16r(0x0806)
	ise.TEthernetRaamhandler.RaamSaada(sihtfailmacbe, ethernetLiikbe, dataKursor, suurus)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	arvcachekirje	int

	handler	IEthernetRaamhandler
}

var handler IEthernetRaamhandler

func (ise *Arpprovider) Init(backend TEthernetRaamprovider, userhandler IEthernetRaamhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Määrahandler(userhandler, 0x0806)
	ise.arvcachekirje = 0
	arpprovider = *ise

}

func (ise *Arpprovider) EthernetRaamreceivewhen(dataKursor uintptr, suurus uint32) bool {

	if suurus < arpmesgSuurus {
		return false
	}
	var arpbuffer *ArpTeadebuffer = (*ArpTeadebuffer)(Pointer(dataKursor))
	var arp ArpTeade = ArpTeade{}
	arp.Init(arpbuffer)

	if arp.riistvaraLiik == 0x0100 {

		if arp.protocol == 0x0008 && arp.riistvaraaddressSuurus == 6 && arp.protocoladdressSuurus == 4 && uint64(arp.sihtfailipaddress) == handler.Getipaddress() {

			arpconsole.MPrindi([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Prindi(arp.protocol)
			arpconsole.MPrindi([]byte(":"))
			arpconsole.MUnsignedinteger64Prindi(uint64(arp.sihtfailmacaddress))
			arpconsole.MPrindi([]byte(":"))
			arpconsole.MUnsignedinteger16Prindi(arp.käsk)
			arpconsole.MPrindi([]byte(":"))
			arpconsole.MUnsignedinteger64Prindi(handler.Getmacaddress())

			switch arp.käsk {
			case 0x0100:

				if ise.Getmacfromcache(arp.aLLIKASipaddress) == 0xFFFFFFFFFFFF {
					if ise.arvcachekirje < 128 {
						ise.Ipcache[ise.arvcachekirje] = arp.aLLIKASipaddress
						ise.Maccache[ise.arvcachekirje] = arp.aLLIKASmacaddress
						ise.arvcachekirje++
					}
				}
				arp.käsk = 0x0200
				arp.sihtfailipaddress = arp.aLLIKASipaddress
				arp.sihtfailmacaddress = arp.aLLIKASmacaddress
				arp.aLLIKASipaddress = uint32(handler.Getipaddress())
				arp.aLLIKASmacaddress = handler.Getmacaddress()
				arp.Määrabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MPrindi(([]byte)("self.numCacheEntries"))

				if ise.arvcachekirje < 128 {
					ise.Ipcache[ise.arvcachekirje] = arp.aLLIKASipaddress
					ise.Maccache[ise.arvcachekirje] = arp.aLLIKASmacaddress
					ise.arvcachekirje++
				}
				break
			}

		}
	}
	return false

}

func (ise *Arpprovider) Broadcastmacaddress(IpVõrkbyteorder uint32) {

	var arp ArpTeade = ArpTeade{}
	arp.riistvaraLiik = 0x0100
	arp.protocol = 0x0008
	arp.riistvaraaddressSuurus = 6
	arp.protocoladdressSuurus = 4
	arp.käsk = 0x0200

	arp.aLLIKASipaddress = uint32(handler.Getipaddress())

	arp.sihtfailmacaddress = ise.Resolve(IpVõrkbyteorder)
	arp.sihtfailipaddress = IpVõrkbyteorder
	arpconsole.MPrindixy([]byte("broad mac"), 0, 15)

	arp.aLLIKASmacaddress = handler.Getmacaddress()

	var arpbuffer ArpTeadebuffer = ArpTeadebuffer{}
	arp.Määrabuffer(&arpbuffer)

	var kursor uintptr = uintptr(Pointer(&arpbuffer))
	handler.Saada(arp.sihtfailmacaddress, kursor, arpmesgSuurus)
}
func (ise *Arpprovider) Requestmacaddress(IpVõrkbyteorder uint32) {

	var arp ArpTeade = ArpTeade{}
	arp.riistvaraLiik = 0x0100

	arp.protocol = 0x0008
	arp.riistvaraaddressSuurus = 6
	arp.protocoladdressSuurus = 4
	arp.käsk = 0x0100

	arp.aLLIKASmacaddress = handler.Getmacaddress()
	arp.aLLIKASipaddress = uint32(handler.Getipaddress())

	arp.sihtfailmacaddress = 0xFFFFFFFFFFFF
	arp.sihtfailipaddress = IpVõrkbyteorder

	var arpbuffer ArpTeadebuffer = ArpTeadebuffer{}
	arp.Määrabuffer(&arpbuffer)

	var kursor uintptr = uintptr(Pointer(&arpbuffer))
	handler.Saada(arp.sihtfailmacaddress, kursor, arpmesgSuurus)
}
func (ise *Arpprovider) TestiPrindi(data *[]byte, suurus uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MPrindixy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalPrindi(buffer_2[i])
		arpconsole.MPrindi([]byte(":"))
	}
	arpconsole.MPrindi([]byte("]"))
}

func (ise *Arpprovider) Getmacfromcache(IpVõrkbyteorder uint32) uint64 {
	for i := 0; i < ise.arvcachekirje; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MPrindi(([]byte)("["))
		arpconsole.MUnsignedinteger32Prindi(ise.Ipcache[i])
		arpconsole.MPrindi(([]byte)(":"))
		arpconsole.MUnsignedinteger32Prindi(IpVõrkbyteorder)
		arpconsole.MPrindi(([]byte)(":"))
		arpconsole.MPrindi(([]byte)(":"))
		arpconsole.MUnsignedinteger64Prindi(ise.Maccache[i])
		arpconsole.MPrindi(([]byte)("]\n"))

		if ise.Ipcache[i] == IpVõrkbyteorder {
			arpconsole.MPrindi([]byte("getmacfromcache"))
			return ise.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (ise *Arpprovider) Resolve(IpVõrkbyteorder uint32) uint64 {
	var tULEMUS uint64 = ise.Getmacfromcache(IpVõrkbyteorder)
	if tULEMUS == 0xFFFFFFFFFFFF {
		ise.Requestmacaddress(IpVõrkbyteorder)
	}
	for i := 0; i < 128 && tULEMUS == 0xFFFFFFFFFFFF; i++ {
		tULEMUS = ise.Getmacfromcache(IpVõrkbyteorder)

	}

	return tULEMUS
}
