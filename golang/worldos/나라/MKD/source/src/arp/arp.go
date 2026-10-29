/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "етернетРамка"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpПоракаbuffer struct {
	хардверТип		[2]byte
	protocol		[2]byte
	хардверaddressГолемина	byte
	protocoladdressГолемина	byte
	команда			[2]byte

	изворmacaddress		[6]byte
	изворipaddress		[4]byte
	одредиштеmacaddress	[6]byte
	одредиштеipaddress	[4]byte
}

var arpmesgГолемина uint32 = (64+92+64)/8 + 2

type ArpПорака struct {
	хардверТип		uint16
	protocol		uint16
	хардверaddressГолемина	uint8
	protocoladdressГолемина	uint8
	команда			uint16

	изворmacaddress		uint64
	изворipaddress		uint32
	одредиштеmacaddress	uint64
	одредиштеipaddress	uint32
}

func (само *ArpПорака) Init(buffer_2 *ArpПоракаbuffer) {

	само.хардверТип = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.хардверТип))
	само.protocol = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.protocol))
	само.хардверaddressГолемина = byte(buffer_2.хардверaddressГолемина)
	само.protocoladdressГолемина = byte(buffer_2.protocoladdressГолемина)
	само.команда = Unsignedinteger16r(Построиtounsignedinteger16(buffer_2.команда))

	само.изворmacaddress = Unsignedinteger48r(Построиtounsignedinteger48(buffer_2.изворmacaddress))
	само.изворipaddress = Unsignedinteger32r(Построиtounsignedinteger32(buffer_2.изворipaddress))
	само.одредиштеmacaddress = Unsignedinteger48r(Построиtounsignedinteger48(buffer_2.одредиштеmacaddress))
	само.одредиштеipaddress = Unsignedinteger32r(Построиtounsignedinteger32(buffer_2.одредиштеipaddress))
}
func (само *ArpПорака) Поставиbuffer(buffer_2 *ArpПоракаbuffer) {
	buffer_2.хардверТип = Unsignedinteger16toПострои(само.хардверТип)
	buffer_2.protocol = Unsignedinteger16toПострои(само.protocol)
	buffer_2.хардверaddressГолемина = uint8(само.хардверaddressГолемина)
	buffer_2.protocoladdressГолемина = uint8(само.protocoladdressГолемина)

	buffer_2.команда = Unsignedinteger16toПострои(само.команда)
	buffer_2.изворmacaddress = Unsignedinteger48toПострои(само.изворmacaddress)
	buffer_2.изворipaddress = Unsignedinteger32toПострои(само.изворipaddress)
	buffer_2.одредиштеmacaddress = Unsignedinteger48toПострои(само.одредиштеmacaddress)
	buffer_2.одредиштеipaddress = Unsignedinteger32toПострои(само.одредиштеipaddress)
}

type ArpЕтернетРамкаhandler struct {
	TЕтернетРамкаhandler
}

var arpprovider Arpprovider
var етернетРамкаprovider TЕтернетРамкаprovider

func (само *ArpЕтернетРамкаhandler) ЕтернетРамкаreceivewhen(dataСтрелка uintptr, големина int) bool {
	arpconsole.MПечатиxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ЕтернетРамкаreceivewhen(dataСтрелка, uint32(големина))

}
func (само *ArpЕтернетРамкаhandler) Испрати(одредиштеmacbe uint64, dataСтрелка uintptr, големина uint32) {
	arpconsole.MПечатиxy([]byte("arp send:"), 0, 24)
	var етернетТипbe = Unsignedinteger16r(0x0806)
	само.TЕтернетРамкаhandler.РамкаИспрати(одредиштеmacbe, етернетТипbe, dataСтрелка, големина)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numbercacheentry	int

	handler	IЕтернетРамкаhandler
}

var handler IЕтернетРамкаhandler

func (само *Arpprovider) Init(backend TЕтернетРамкаprovider, userhandler IЕтернетРамкаhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Поставиhandler(userhandler, 0x0806)
	само.numbercacheentry = 0
	arpprovider = *само

}

func (само *Arpprovider) ЕтернетРамкаreceivewhen(dataСтрелка uintptr, големина uint32) bool {

	if големина < arpmesgГолемина {
		return false
	}
	var arpbuffer *ArpПоракаbuffer = (*ArpПоракаbuffer)(Pointer(dataСтрелка))
	var arp ArpПорака = ArpПорака{}
	arp.Init(arpbuffer)

	if arp.хардверТип == 0x0100 {

		if arp.protocol == 0x0008 && arp.хардверaddressГолемина == 6 && arp.protocoladdressГолемина == 4 && uint64(arp.одредиштеipaddress) == handler.Getipaddress() {

			arpconsole.MПечати([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Печати(arp.protocol)
			arpconsole.MПечати([]byte(":"))
			arpconsole.MUnsignedinteger64Печати(uint64(arp.одредиштеmacaddress))
			arpconsole.MПечати([]byte(":"))
			arpconsole.MUnsignedinteger16Печати(arp.команда)
			arpconsole.MПечати([]byte(":"))
			arpconsole.MUnsignedinteger64Печати(handler.Getmacaddress())

			switch arp.команда {
			case 0x0100:

				if само.Getmacfromcache(arp.изворipaddress) == 0xFFFFFFFFFFFF {
					if само.numbercacheentry < 128 {
						само.Ipcache[само.numbercacheentry] = arp.изворipaddress
						само.Maccache[само.numbercacheentry] = arp.изворmacaddress
						само.numbercacheentry++
					}
				}
				arp.команда = 0x0200
				arp.одредиштеipaddress = arp.изворipaddress
				arp.одредиштеmacaddress = arp.изворmacaddress
				arp.изворipaddress = uint32(handler.Getipaddress())
				arp.изворmacaddress = handler.Getmacaddress()
				arp.Поставиbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MПечати(([]byte)("self.numCacheEntries"))

				if само.numbercacheentry < 128 {
					само.Ipcache[само.numbercacheentry] = arp.изворipaddress
					само.Maccache[само.numbercacheentry] = arp.изворmacaddress
					само.numbercacheentry++
				}
				break
			}

		}
	}
	return false

}

func (само *Arpprovider) Broadcastmacaddress(IpМрежаbyteorder uint32) {

	var arp ArpПорака = ArpПорака{}
	arp.хардверТип = 0x0100
	arp.protocol = 0x0008
	arp.хардверaddressГолемина = 6
	arp.protocoladdressГолемина = 4
	arp.команда = 0x0200

	arp.изворipaddress = uint32(handler.Getipaddress())

	arp.одредиштеmacaddress = само.Resolve(IpМрежаbyteorder)
	arp.одредиштеipaddress = IpМрежаbyteorder
	arpconsole.MПечатиxy([]byte("broad mac"), 0, 15)

	arp.изворmacaddress = handler.Getmacaddress()

	var arpbuffer ArpПоракаbuffer = ArpПоракаbuffer{}
	arp.Поставиbuffer(&arpbuffer)

	var стрелка uintptr = uintptr(Pointer(&arpbuffer))
	handler.Испрати(arp.одредиштеmacaddress, стрелка, arpmesgГолемина)
}
func (само *Arpprovider) Requestmacaddress(IpМрежаbyteorder uint32) {

	var arp ArpПорака = ArpПорака{}
	arp.хардверТип = 0x0100

	arp.protocol = 0x0008
	arp.хардверaddressГолемина = 6
	arp.protocoladdressГолемина = 4
	arp.команда = 0x0100

	arp.изворmacaddress = handler.Getmacaddress()
	arp.изворipaddress = uint32(handler.Getipaddress())

	arp.одредиштеmacaddress = 0xFFFFFFFFFFFF
	arp.одредиштеipaddress = IpМрежаbyteorder

	var arpbuffer ArpПоракаbuffer = ArpПоракаbuffer{}
	arp.Поставиbuffer(&arpbuffer)

	var стрелка uintptr = uintptr(Pointer(&arpbuffer))
	handler.Испрати(arp.одредиштеmacaddress, стрелка, arpmesgГолемина)
}
func (само *Arpprovider) TestПечати(data *[]byte, големина uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MПечатиxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalПечати(buffer_2[i])
		arpconsole.MПечати([]byte(":"))
	}
	arpconsole.MПечати([]byte("]"))
}

func (само *Arpprovider) Getmacfromcache(IpМрежаbyteorder uint32) uint64 {
	for i := 0; i < само.numbercacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MПечати(([]byte)("["))
		arpconsole.MUnsignedinteger32Печати(само.Ipcache[i])
		arpconsole.MПечати(([]byte)(":"))
		arpconsole.MUnsignedinteger32Печати(IpМрежаbyteorder)
		arpconsole.MПечати(([]byte)(":"))
		arpconsole.MПечати(([]byte)(":"))
		arpconsole.MUnsignedinteger64Печати(само.Maccache[i])
		arpconsole.MПечати(([]byte)("]\n"))

		if само.Ipcache[i] == IpМрежаbyteorder {
			arpconsole.MПечати([]byte("getmacfromcache"))
			return само.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (само *Arpprovider) Resolve(IpМрежаbyteorder uint32) uint64 {
	var result uint64 = само.Getmacfromcache(IpМрежаbyteorder)
	if result == 0xFFFFFFFFFFFF {
		само.Requestmacaddress(IpМрежаbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = само.Getmacfromcache(IpМрежаbyteorder)

	}

	return result
}
