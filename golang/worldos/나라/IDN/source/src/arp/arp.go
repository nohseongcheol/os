/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "bingkai_jaringan_media_bersama"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpPesanbuffer struct {
	perangkatkerasTipe		[2]byte
	protocol			[2]byte
	perangkatkerasaddressUkuran	byte
	protocoladdressUkuran		byte
	perintah			[2]byte

	sumbermacaddress	[6]byte
	sumberipaddress		[4]byte
	tujuanmacaddress	[6]byte
	tujuanipaddress		[4]byte
}

var arpmesgUkuran uint32 = (64+92+64)/8 + 2

type ArpPesan struct {
	perangkatkerasTipe		uint16
	protocol			uint16
	perangkatkerasaddressUkuran	uint8
	protocoladdressUkuran		uint8
	perintah			uint16

	sumbermacaddress	uint64
	sumberipaddress		uint32
	tujuanmacaddress	uint64
	tujuanipaddress		uint32
}

func (dirisendiri *ArpPesan) Init(buffer_2 *ArpPesanbuffer) {

	dirisendiri.perangkatkerasTipe = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.perangkatkerasTipe))
	dirisendiri.protocol = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.protocol))
	dirisendiri.perangkatkerasaddressUkuran = byte(buffer_2.perangkatkerasaddressUkuran)
	dirisendiri.protocoladdressUkuran = byte(buffer_2.protocoladdressUkuran)
	dirisendiri.perintah = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.perintah))

	dirisendiri.sumbermacaddress = Unsignedinteger48r(Jajarantounsignedinteger48(buffer_2.sumbermacaddress))
	dirisendiri.sumberipaddress = Unsignedinteger32r(Jajarantounsignedinteger32(buffer_2.sumberipaddress))
	dirisendiri.tujuanmacaddress = Unsignedinteger48r(Jajarantounsignedinteger48(buffer_2.tujuanmacaddress))
	dirisendiri.tujuanipaddress = Unsignedinteger32r(Jajarantounsignedinteger32(buffer_2.tujuanipaddress))
}
func (dirisendiri *ArpPesan) Aturbuffer(buffer_2 *ArpPesanbuffer) {
	buffer_2.perangkatkerasTipe = Unsignedinteger16toJajaran(dirisendiri.perangkatkerasTipe)
	buffer_2.protocol = Unsignedinteger16toJajaran(dirisendiri.protocol)
	buffer_2.perangkatkerasaddressUkuran = uint8(dirisendiri.perangkatkerasaddressUkuran)
	buffer_2.protocoladdressUkuran = uint8(dirisendiri.protocoladdressUkuran)

	buffer_2.perintah = Unsignedinteger16toJajaran(dirisendiri.perintah)
	buffer_2.sumbermacaddress = Unsignedinteger48toJajaran(dirisendiri.sumbermacaddress)
	buffer_2.sumberipaddress = Unsignedinteger32toJajaran(dirisendiri.sumberipaddress)
	buffer_2.tujuanmacaddress = Unsignedinteger48toJajaran(dirisendiri.tujuanmacaddress)
	buffer_2.tujuanipaddress = Unsignedinteger32toJajaran(dirisendiri.tujuanipaddress)
}

type ArpethernetBingkaihandler struct {
	TEthernetBingkaihandler
}

var arpprovider Arpprovider
var penyedia_bingkai_jaringan_media_bersama TPenyedia_bingkai_jaringan_media_bersama

func (dirisendiri *ArpethernetBingkaihandler) EthernetBingkaireceivewhen(dataPenunjuk uintptr, ukuran int) bool {
	arpconsole.MCetakxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetBingkaireceivewhen(dataPenunjuk, uint32(ukuran))

}
func (dirisendiri *ArpethernetBingkaihandler) Kirim(tujuanmacbe uint64, dataPenunjuk uintptr, ukuran uint32) {
	arpconsole.MCetakxy([]byte("arp send:"), 0, 24)
	var ethernetTipebe = Unsignedinteger16r(0x0806)
	dirisendiri.TEthernetBingkaihandler.BingkaiKirim(tujuanmacbe, ethernetTipebe, dataPenunjuk, ukuran)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	nomorcacheentri	int

	handler	IEthernetBingkaihandler
}

var handler IEthernetBingkaihandler

func (dirisendiri *Arpprovider) Init(backend TPenyedia_bingkai_jaringan_media_bersama, userhandler IEthernetBingkaihandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Aturhandler(userhandler, 0x0806)
	dirisendiri.nomorcacheentri = 0
	arpprovider = *dirisendiri

}

func (dirisendiri *Arpprovider) EthernetBingkaireceivewhen(dataPenunjuk uintptr, ukuran uint32) bool {

	if ukuran < arpmesgUkuran {
		return false
	}
	var arpbuffer *ArpPesanbuffer = (*ArpPesanbuffer)(Pointer(dataPenunjuk))
	var arp ArpPesan = ArpPesan{}
	arp.Init(arpbuffer)

	if arp.perangkatkerasTipe == 0x0100 {

		if arp.protocol == 0x0008 && arp.perangkatkerasaddressUkuran == 6 && arp.protocoladdressUkuran == 4 && uint64(arp.tujuanipaddress) == handler.Getipaddress() {

			arpconsole.MCetak([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Cetak(arp.protocol)
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger64Cetak(uint64(arp.tujuanmacaddress))
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger16Cetak(arp.perintah)
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger64Cetak(handler.Getmacaddress())

			switch arp.perintah {
			case 0x0100:

				if dirisendiri.Getmacfromcache(arp.sumberipaddress) == 0xFFFFFFFFFFFF {
					if dirisendiri.nomorcacheentri < 128 {
						dirisendiri.Ipcache[dirisendiri.nomorcacheentri] = arp.sumberipaddress
						dirisendiri.Maccache[dirisendiri.nomorcacheentri] = arp.sumbermacaddress
						dirisendiri.nomorcacheentri++
					}
				}
				arp.perintah = 0x0200
				arp.tujuanipaddress = arp.sumberipaddress
				arp.tujuanmacaddress = arp.sumbermacaddress
				arp.sumberipaddress = uint32(handler.Getipaddress())
				arp.sumbermacaddress = handler.Getmacaddress()
				arp.Aturbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MCetak(([]byte)("self.numCacheEntries"))

				if dirisendiri.nomorcacheentri < 128 {
					dirisendiri.Ipcache[dirisendiri.nomorcacheentri] = arp.sumberipaddress
					dirisendiri.Maccache[dirisendiri.nomorcacheentri] = arp.sumbermacaddress
					dirisendiri.nomorcacheentri++
				}
				break
			}

		}
	}
	return false

}

func (dirisendiri *Arpprovider) Broadcastmacaddress(IpJaringanbyteorder uint32) {

	var arp ArpPesan = ArpPesan{}
	arp.perangkatkerasTipe = 0x0100
	arp.protocol = 0x0008
	arp.perangkatkerasaddressUkuran = 6
	arp.protocoladdressUkuran = 4
	arp.perintah = 0x0200

	arp.sumberipaddress = uint32(handler.Getipaddress())

	arp.tujuanmacaddress = dirisendiri.Resolve(IpJaringanbyteorder)
	arp.tujuanipaddress = IpJaringanbyteorder
	arpconsole.MCetakxy([]byte("broad mac"), 0, 15)

	arp.sumbermacaddress = handler.Getmacaddress()

	var arpbuffer ArpPesanbuffer = ArpPesanbuffer{}
	arp.Aturbuffer(&arpbuffer)

	var acuan_alamat uintptr = uintptr(Pointer(&arpbuffer))
	handler.Kirim(arp.tujuanmacaddress, acuan_alamat, arpmesgUkuran)
}
func (dirisendiri *Arpprovider) Requestmacaddress(IpJaringanbyteorder uint32) {

	var arp ArpPesan = ArpPesan{}
	arp.perangkatkerasTipe = 0x0100

	arp.protocol = 0x0008
	arp.perangkatkerasaddressUkuran = 6
	arp.protocoladdressUkuran = 4
	arp.perintah = 0x0100

	arp.sumbermacaddress = handler.Getmacaddress()
	arp.sumberipaddress = uint32(handler.Getipaddress())

	arp.tujuanmacaddress = 0xFFFFFFFFFFFF
	arp.tujuanipaddress = IpJaringanbyteorder

	var arpbuffer ArpPesanbuffer = ArpPesanbuffer{}
	arp.Aturbuffer(&arpbuffer)

	var acuan_alamat uintptr = uintptr(Pointer(&arpbuffer))
	handler.Kirim(arp.tujuanmacaddress, acuan_alamat, arpmesgUkuran)
}
func (dirisendiri *Arpprovider) TesCetak(data *[]byte, ukuran uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MCetakxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalCetak(buffer_2[i])
		arpconsole.MCetak([]byte(":"))
	}
	arpconsole.MCetak([]byte("]"))
}

func (dirisendiri *Arpprovider) Getmacfromcache(IpJaringanbyteorder uint32) uint64 {
	for i := 0; i < dirisendiri.nomorcacheentri; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MCetak(([]byte)("["))
		arpconsole.MUnsignedinteger32Cetak(dirisendiri.Ipcache[i])
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MUnsignedinteger32Cetak(IpJaringanbyteorder)
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MUnsignedinteger64Cetak(dirisendiri.Maccache[i])
		arpconsole.MCetak(([]byte)("]\n"))

		if dirisendiri.Ipcache[i] == IpJaringanbyteorder {
			arpconsole.MCetak([]byte("getmacfromcache"))
			return dirisendiri.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (dirisendiri *Arpprovider) Resolve(IpJaringanbyteorder uint32) uint64 {
	var hASIL uint64 = dirisendiri.Getmacfromcache(IpJaringanbyteorder)
	if hASIL == 0xFFFFFFFFFFFF {
		dirisendiri.Requestmacaddress(IpJaringanbyteorder)
	}
	for i := 0; i < 128 && hASIL == 0xFFFFFFFFFFFF; i++ {
		hASIL = dirisendiri.Getmacfromcache(IpJaringanbyteorder)

	}

	return hASIL
}
