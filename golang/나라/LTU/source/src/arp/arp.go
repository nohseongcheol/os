package arp

import . "unsafe"
import . "console"
import . "laidinisKadras"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpPranešimasbuffer struct {
	aparatinėįrangaTipas		[2]byte
	protocol			[2]byte
	aparatinėįrangaaddressDydis	byte
	protocoladdressDydis		byte
	komanda				[2]byte

	šaltinismacaddress	[6]byte
	šaltinisipaddress	[4]byte
	tikslasmacaddress	[6]byte
	tikslasipaddress	[4]byte
}

var arpmesgDydis uint32 = (64+92+64)/8 + 2

type ArpPranešimas struct {
	aparatinėįrangaTipas		uint16
	protocol			uint16
	aparatinėįrangaaddressDydis	uint8
	protocoladdressDydis		uint8
	komanda				uint16

	šaltinismacaddress	uint64
	šaltinisipaddress	uint32
	tikslasmacaddress	uint64
	tikslasipaddress	uint32
}

func (self *ArpPranešimas) Init(buffer_2 *ArpPranešimasbuffer) {

	self.aparatinėįrangaTipas = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.aparatinėįrangaTipas))
	self.protocol = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.protocol))
	self.aparatinėįrangaaddressDydis = byte(buffer_2.aparatinėįrangaaddressDydis)
	self.protocoladdressDydis = byte(buffer_2.protocoladdressDydis)
	self.komanda = Unsignedinteger16r(Masyvastounsignedinteger16(buffer_2.komanda))

	self.šaltinismacaddress = Unsignedinteger48r(Masyvastounsignedinteger48(buffer_2.šaltinismacaddress))
	self.šaltinisipaddress = Unsignedinteger32r(Masyvastounsignedinteger32(buffer_2.šaltinisipaddress))
	self.tikslasmacaddress = Unsignedinteger48r(Masyvastounsignedinteger48(buffer_2.tikslasmacaddress))
	self.tikslasipaddress = Unsignedinteger32r(Masyvastounsignedinteger32(buffer_2.tikslasipaddress))
}
func (self *ArpPranešimas) Nustatytabuffer(buffer_2 *ArpPranešimasbuffer) {
	buffer_2.aparatinėįrangaTipas = Unsignedinteger16toMasyvas(self.aparatinėįrangaTipas)
	buffer_2.protocol = Unsignedinteger16toMasyvas(self.protocol)
	buffer_2.aparatinėįrangaaddressDydis = uint8(self.aparatinėįrangaaddressDydis)
	buffer_2.protocoladdressDydis = uint8(self.protocoladdressDydis)

	buffer_2.komanda = Unsignedinteger16toMasyvas(self.komanda)
	buffer_2.šaltinismacaddress = Unsignedinteger48toMasyvas(self.šaltinismacaddress)
	buffer_2.šaltinisipaddress = Unsignedinteger32toMasyvas(self.šaltinisipaddress)
	buffer_2.tikslasmacaddress = Unsignedinteger48toMasyvas(self.tikslasmacaddress)
	buffer_2.tikslasipaddress = Unsignedinteger32toMasyvas(self.tikslasipaddress)
}

type ArpLaidinisKadrashandler struct {
	TLaidinisKadrashandler
}

var arpprovider Arpprovider
var laidinisKadrasprovider TLaidinisKadrasprovider

func (self *ArpLaidinisKadrashandler) LaidinisKadrasreceivewhen(dataRodyklė uintptr, dydis int) bool {
	arpconsole.MSpausdintixy([]byte("arp recv:"), 0, 23)
	return arpprovider.LaidinisKadrasreceivewhen(dataRodyklė, uint32(dydis))

}
func (self *ArpLaidinisKadrashandler) Siųsti(tikslasmacbe uint64, dataRodyklė uintptr, dydis uint32) {
	arpconsole.MSpausdintixy([]byte("arp send:"), 0, 24)
	var laidinisTipasbe = Unsignedinteger16r(0x0806)
	self.TLaidinisKadrashandler.KadrasSiųsti(tikslasmacbe, laidinisTipasbe, dataRodyklė, dydis)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	skaičiuscacheįrašas	int

	handler	ILaidinisKadrashandler
}

var handler ILaidinisKadrashandler

func (self *Arpprovider) Init(backend TLaidinisKadrasprovider, userhandler ILaidinisKadrashandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Nustatytahandler(userhandler, 0x0806)
	self.skaičiuscacheįrašas = 0
	arpprovider = *self

}

func (self *Arpprovider) LaidinisKadrasreceivewhen(dataRodyklė uintptr, dydis uint32) bool {

	if dydis < arpmesgDydis {
		return false
	}
	var arpbuffer *ArpPranešimasbuffer = (*ArpPranešimasbuffer)(Pointer(dataRodyklė))
	var arp ArpPranešimas = ArpPranešimas{}
	arp.Init(arpbuffer)

	if arp.aparatinėįrangaTipas == 0x0100 {

		if arp.protocol == 0x0008 && arp.aparatinėįrangaaddressDydis == 6 && arp.protocoladdressDydis == 4 && uint64(arp.tikslasipaddress) == handler.Getipaddress() {

			arpconsole.MSpausdinti([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Spausdinti(arp.protocol)
			arpconsole.MSpausdinti([]byte(":"))
			arpconsole.MUnsignedinteger64Spausdinti(uint64(arp.tikslasmacaddress))
			arpconsole.MSpausdinti([]byte(":"))
			arpconsole.MUnsignedinteger16Spausdinti(arp.komanda)
			arpconsole.MSpausdinti([]byte(":"))
			arpconsole.MUnsignedinteger64Spausdinti(handler.Getmacaddress())

			switch arp.komanda {
			case 0x0100:

				if self.Getmacfromcache(arp.šaltinisipaddress) == 0xFFFFFFFFFFFF {
					if self.skaičiuscacheįrašas < 128 {
						self.Ipcache[self.skaičiuscacheįrašas] = arp.šaltinisipaddress
						self.Maccache[self.skaičiuscacheįrašas] = arp.šaltinismacaddress
						self.skaičiuscacheįrašas++
					}
				}
				arp.komanda = 0x0200
				arp.tikslasipaddress = arp.šaltinisipaddress
				arp.tikslasmacaddress = arp.šaltinismacaddress
				arp.šaltinisipaddress = uint32(handler.Getipaddress())
				arp.šaltinismacaddress = handler.Getmacaddress()
				arp.Nustatytabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MSpausdinti(([]byte)("self.numCacheEntries"))

				if self.skaičiuscacheįrašas < 128 {
					self.Ipcache[self.skaičiuscacheįrašas] = arp.šaltinisipaddress
					self.Maccache[self.skaičiuscacheįrašas] = arp.šaltinismacaddress
					self.skaičiuscacheįrašas++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpTinklasbyteorder uint32) {

	var arp ArpPranešimas = ArpPranešimas{}
	arp.aparatinėįrangaTipas = 0x0100
	arp.protocol = 0x0008
	arp.aparatinėįrangaaddressDydis = 6
	arp.protocoladdressDydis = 4
	arp.komanda = 0x0200

	arp.šaltinisipaddress = uint32(handler.Getipaddress())

	arp.tikslasmacaddress = self.Resolve(IpTinklasbyteorder)
	arp.tikslasipaddress = IpTinklasbyteorder
	arpconsole.MSpausdintixy([]byte("broad mac"), 0, 15)

	arp.šaltinismacaddress = handler.Getmacaddress()

	var arpbuffer ArpPranešimasbuffer = ArpPranešimasbuffer{}
	arp.Nustatytabuffer(&arpbuffer)

	var rodyklė_2 uintptr = uintptr(Pointer(&arpbuffer))
	handler.Siųsti(arp.tikslasmacaddress, rodyklė_2, arpmesgDydis)
}
func (self *Arpprovider) Requestmacaddress(IpTinklasbyteorder uint32) {

	var arp ArpPranešimas = ArpPranešimas{}
	arp.aparatinėįrangaTipas = 0x0100

	arp.protocol = 0x0008
	arp.aparatinėįrangaaddressDydis = 6
	arp.protocoladdressDydis = 4
	arp.komanda = 0x0100

	arp.šaltinismacaddress = handler.Getmacaddress()
	arp.šaltinisipaddress = uint32(handler.Getipaddress())

	arp.tikslasmacaddress = 0xFFFFFFFFFFFF
	arp.tikslasipaddress = IpTinklasbyteorder

	var arpbuffer ArpPranešimasbuffer = ArpPranešimasbuffer{}
	arp.Nustatytabuffer(&arpbuffer)

	var rodyklė_2 uintptr = uintptr(Pointer(&arpbuffer))
	handler.Siųsti(arp.tikslasmacaddress, rodyklė_2, arpmesgDydis)
}
func (self *Arpprovider) TestasSpausdinti(data *[]byte, dydis uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MSpausdintixy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalSpausdinti(buffer_2[i])
		arpconsole.MSpausdinti([]byte(":"))
	}
	arpconsole.MSpausdinti([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpTinklasbyteorder uint32) uint64 {
	for i := 0; i < self.skaičiuscacheįrašas; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MSpausdinti(([]byte)("["))
		arpconsole.MUnsignedinteger32Spausdinti(self.Ipcache[i])
		arpconsole.MSpausdinti(([]byte)(":"))
		arpconsole.MUnsignedinteger32Spausdinti(IpTinklasbyteorder)
		arpconsole.MSpausdinti(([]byte)(":"))
		arpconsole.MSpausdinti(([]byte)(":"))
		arpconsole.MUnsignedinteger64Spausdinti(self.Maccache[i])
		arpconsole.MSpausdinti(([]byte)("]\n"))

		if self.Ipcache[i] == IpTinklasbyteorder {
			arpconsole.MSpausdinti([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpTinklasbyteorder uint32) uint64 {
	var rEZULTATAS uint64 = self.Getmacfromcache(IpTinklasbyteorder)
	if rEZULTATAS == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpTinklasbyteorder)
	}
	for i := 0; i < 128 && rEZULTATAS == 0xFFFFFFFFFFFF; i++ {
		rEZULTATAS = self.Getmacfromcache(IpTinklasbyteorder)

	}

	return rEZULTATAS
}
