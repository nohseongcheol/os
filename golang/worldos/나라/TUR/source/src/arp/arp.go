/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konsol"
import . "ortak_ortam_ağ_çerçevesi"
import . "util"

var arpKonsol TKonsol = TKonsol{}

type Arpİletibuffer struct {
	donanımTür		[2]byte
	protocol		[2]byte
	donanımaddressBoyut	byte
	protocoladdressBoyut	byte
	komut			[2]byte

	kaynakmacaddress	[6]byte
	kaynakipaddress		[4]byte
	hedefmacaddress		[6]byte
	hedefipaddress		[4]byte
}

var arpmesgBoyut uint32 = (64+92+64)/8 + 2

type Arpİleti struct {
	donanımTür		uint16
	protocol		uint16
	donanımaddressBoyut	uint8
	protocoladdressBoyut	uint8
	komut			uint16

	kaynakmacaddress	uint64
	kaynakipaddress		uint32
	hedefmacaddress		uint64
	hedefipaddress		uint32
}

func (self *Arpİleti) Init(buffer_2 *Arpİletibuffer) {

	self.donanımTür = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.donanımTür))
	self.protocol = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.protocol))
	self.donanımaddressBoyut = byte(buffer_2.donanımaddressBoyut)
	self.protocoladdressBoyut = byte(buffer_2.protocoladdressBoyut)
	self.komut = Unsignedinteger16r(Dizitounsignedinteger16(buffer_2.komut))

	self.kaynakmacaddress = Unsignedinteger48r(Dizitounsignedinteger48(buffer_2.kaynakmacaddress))
	self.kaynakipaddress = Unsignedinteger32r(Dizitounsignedinteger32(buffer_2.kaynakipaddress))
	self.hedefmacaddress = Unsignedinteger48r(Dizitounsignedinteger48(buffer_2.hedefmacaddress))
	self.hedefipaddress = Unsignedinteger32r(Dizitounsignedinteger32(buffer_2.hedefipaddress))
}
func (self *Arpİleti) Ayarlabuffer(buffer_2 *Arpİletibuffer) {
	buffer_2.donanımTür = Unsignedinteger16toDizi(self.donanımTür)
	buffer_2.protocol = Unsignedinteger16toDizi(self.protocol)
	buffer_2.donanımaddressBoyut = uint8(self.donanımaddressBoyut)
	buffer_2.protocoladdressBoyut = uint8(self.protocoladdressBoyut)

	buffer_2.komut = Unsignedinteger16toDizi(self.komut)
	buffer_2.kaynakmacaddress = Unsignedinteger48toDizi(self.kaynakmacaddress)
	buffer_2.kaynakipaddress = Unsignedinteger32toDizi(self.kaynakipaddress)
	buffer_2.hedefmacaddress = Unsignedinteger48toDizi(self.hedefmacaddress)
	buffer_2.hedefipaddress = Unsignedinteger32toDizi(self.hedefipaddress)
}

type ArpEternetÇerçevehandler struct {
	TEternetÇerçevehandler
}

var arpprovider Arpprovider
var ortak_ortam_ağ_çerçevesi_sağlayıcısı TOrtak_ortam_ağ_çerçevesi_sağlayıcısı

func (self *ArpEternetÇerçevehandler) EternetÇerçevereceivewhen(dataBelirteç uintptr, boyut int) bool {
	arpKonsol.MYazdırxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EternetÇerçevereceivewhen(dataBelirteç, uint32(boyut))

}
func (self *ArpEternetÇerçevehandler) Gönder(hedefmacbe uint64, dataBelirteç uintptr, boyut uint32) {
	arpKonsol.MYazdırxy([]byte("arp send:"), 0, 24)
	var eternetTürbe = Unsignedinteger16r(0x0806)
	self.TEternetÇerçevehandler.ÇerçeveGönder(hedefmacbe, eternetTürbe, dataBelirteç, boyut)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	sayıcachegirdi	int

	handler	IEternetÇerçevehandler
}

var handler IEternetÇerçevehandler

func (self *Arpprovider) Init(backend TOrtak_ortam_ağ_çerçevesi_sağlayıcısı, userhandler IEternetÇerçevehandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Ayarlahandler(userhandler, 0x0806)
	self.sayıcachegirdi = 0
	arpprovider = *self

}

func (self *Arpprovider) EternetÇerçevereceivewhen(dataBelirteç uintptr, boyut uint32) bool {

	if boyut < arpmesgBoyut {
		return false
	}
	var arpbuffer *Arpİletibuffer = (*Arpİletibuffer)(Pointer(dataBelirteç))
	var arp Arpİleti = Arpİleti{}
	arp.Init(arpbuffer)

	if arp.donanımTür == 0x0100 {

		if arp.protocol == 0x0008 && arp.donanımaddressBoyut == 6 && arp.protocoladdressBoyut == 4 && uint64(arp.hedefipaddress) == handler.Getipaddress() {

			arpKonsol.MYazdır([]byte("arp onetherframe"))
			arpKonsol.MUnsignedinteger16Yazdır(arp.protocol)
			arpKonsol.MYazdır([]byte(":"))
			arpKonsol.MUnsignedinteger64Yazdır(uint64(arp.hedefmacaddress))
			arpKonsol.MYazdır([]byte(":"))
			arpKonsol.MUnsignedinteger16Yazdır(arp.komut)
			arpKonsol.MYazdır([]byte(":"))
			arpKonsol.MUnsignedinteger64Yazdır(handler.Getmacaddress())

			switch arp.komut {
			case 0x0100:

				if self.Getmacfromcache(arp.kaynakipaddress) == 0xFFFFFFFFFFFF {
					if self.sayıcachegirdi < 128 {
						self.Ipcache[self.sayıcachegirdi] = arp.kaynakipaddress
						self.Maccache[self.sayıcachegirdi] = arp.kaynakmacaddress
						self.sayıcachegirdi++
					}
				}
				arp.komut = 0x0200
				arp.hedefipaddress = arp.kaynakipaddress
				arp.hedefmacaddress = arp.kaynakmacaddress
				arp.kaynakipaddress = uint32(handler.Getipaddress())
				arp.kaynakmacaddress = handler.Getmacaddress()
				arp.Ayarlabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsol.MYazdır(([]byte)("self.numCacheEntries"))

				if self.sayıcachegirdi < 128 {
					self.Ipcache[self.sayıcachegirdi] = arp.kaynakipaddress
					self.Maccache[self.sayıcachegirdi] = arp.kaynakmacaddress
					self.sayıcachegirdi++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpAğbyteorder uint32) {

	var arp Arpİleti = Arpİleti{}
	arp.donanımTür = 0x0100
	arp.protocol = 0x0008
	arp.donanımaddressBoyut = 6
	arp.protocoladdressBoyut = 4
	arp.komut = 0x0200

	arp.kaynakipaddress = uint32(handler.Getipaddress())

	arp.hedefmacaddress = self.Resolve(IpAğbyteorder)
	arp.hedefipaddress = IpAğbyteorder
	arpKonsol.MYazdırxy([]byte("broad mac"), 0, 15)

	arp.kaynakmacaddress = handler.Getmacaddress()

	var arpbuffer Arpİletibuffer = Arpİletibuffer{}
	arp.Ayarlabuffer(&arpbuffer)

	var adres_başvurusu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Gönder(arp.hedefmacaddress, adres_başvurusu, arpmesgBoyut)
}
func (self *Arpprovider) Requestmacaddress(IpAğbyteorder uint32) {

	var arp Arpİleti = Arpİleti{}
	arp.donanımTür = 0x0100

	arp.protocol = 0x0008
	arp.donanımaddressBoyut = 6
	arp.protocoladdressBoyut = 4
	arp.komut = 0x0100

	arp.kaynakmacaddress = handler.Getmacaddress()
	arp.kaynakipaddress = uint32(handler.Getipaddress())

	arp.hedefmacaddress = 0xFFFFFFFFFFFF
	arp.hedefipaddress = IpAğbyteorder

	var arpbuffer Arpİletibuffer = Arpİletibuffer{}
	arp.Ayarlabuffer(&arpbuffer)

	var adres_başvurusu uintptr = uintptr(Pointer(&arpbuffer))
	handler.Gönder(arp.hedefmacaddress, adres_başvurusu, arpmesgBoyut)
}
func (self *Arpprovider) DeneYazdır(data *[]byte, boyut uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonsol.MYazdırxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsol.MHexadecimalYazdır(buffer_2[i])
		arpKonsol.MYazdır([]byte(":"))
	}
	arpKonsol.MYazdır([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpAğbyteorder uint32) uint64 {
	for i := 0; i < self.sayıcachegirdi; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsol.MYazdır(([]byte)("["))
		arpKonsol.MUnsignedinteger32Yazdır(self.Ipcache[i])
		arpKonsol.MYazdır(([]byte)(":"))
		arpKonsol.MUnsignedinteger32Yazdır(IpAğbyteorder)
		arpKonsol.MYazdır(([]byte)(":"))
		arpKonsol.MYazdır(([]byte)(":"))
		arpKonsol.MUnsignedinteger64Yazdır(self.Maccache[i])
		arpKonsol.MYazdır(([]byte)("]\n"))

		if self.Ipcache[i] == IpAğbyteorder {
			arpKonsol.MYazdır([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpAğbyteorder uint32) uint64 {
	var sONUÇ uint64 = self.Getmacfromcache(IpAğbyteorder)
	if sONUÇ == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpAğbyteorder)
	}
	for i := 0; i < 128 && sONUÇ == 0xFFFFFFFFFFFF; i++ {
		sONUÇ = self.Getmacfromcache(IpAğbyteorder)

	}

	return sONUÇ
}
