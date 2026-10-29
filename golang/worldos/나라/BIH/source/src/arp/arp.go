/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "ethernetOkvir"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpPorukabuffer struct {
	hardverTip		[2]byte
	protocol		[2]byte
	hardveraddressVeličina	byte
	protocoladdressVeličina	byte
	naredba			[2]byte

	izvormacaddress		[6]byte
	izvoripaddress		[4]byte
	odredištemacaddress	[6]byte
	odredišteipaddress	[4]byte
}

var arpmesgVeličina uint32 = (64+92+64)/8 + 2

type ArpPoruka struct {
	hardverTip		uint16
	protocol		uint16
	hardveraddressVeličina	uint8
	protocoladdressVeličina	uint8
	naredba			uint16

	izvormacaddress		uint64
	izvoripaddress		uint32
	odredištemacaddress	uint64
	odredišteipaddress	uint32
}

func (self *ArpPoruka) Init(buffer_2 *ArpPorukabuffer) {

	self.hardverTip = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.hardverTip))
	self.protocol = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.protocol))
	self.hardveraddressVeličina = byte(buffer_2.hardveraddressVeličina)
	self.protocoladdressVeličina = byte(buffer_2.protocoladdressVeličina)
	self.naredba = Unsignedinteger16r(Arraytounsignedinteger16(buffer_2.naredba))

	self.izvormacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.izvormacaddress))
	self.izvoripaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.izvoripaddress))
	self.odredištemacaddress = Unsignedinteger48r(Arraytounsignedinteger48(buffer_2.odredištemacaddress))
	self.odredišteipaddress = Unsignedinteger32r(Arraytounsignedinteger32(buffer_2.odredišteipaddress))
}
func (self *ArpPoruka) Skupbuffer(buffer_2 *ArpPorukabuffer) {
	buffer_2.hardverTip = Unsignedinteger16toarray(self.hardverTip)
	buffer_2.protocol = Unsignedinteger16toarray(self.protocol)
	buffer_2.hardveraddressVeličina = uint8(self.hardveraddressVeličina)
	buffer_2.protocoladdressVeličina = uint8(self.protocoladdressVeličina)

	buffer_2.naredba = Unsignedinteger16toarray(self.naredba)
	buffer_2.izvormacaddress = Unsignedinteger48toarray(self.izvormacaddress)
	buffer_2.izvoripaddress = Unsignedinteger32toarray(self.izvoripaddress)
	buffer_2.odredištemacaddress = Unsignedinteger48toarray(self.odredištemacaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toarray(self.odredišteipaddress)
}

type ArpethernetOkvirhandler struct {
	TEthernetOkvirhandler
}

var arpprovider Arpprovider
var ethernetOkvirprovider TEthernetOkvirprovider

func (self *ArpethernetOkvirhandler) EthernetOkvirreceivewhen(datapointer uintptr, veličina int) bool {
	arpconsole.MŠtampajxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetOkvirreceivewhen(datapointer, uint32(veličina))

}
func (self *ArpethernetOkvirhandler) Pošalji(odredištemacbe uint64, datapointer uintptr, veličina uint32) {
	arpconsole.MŠtampajxy([]byte("arp send:"), 0, 24)
	var ethernetTipbe = Unsignedinteger16r(0x0806)
	self.TEthernetOkvirhandler.OkvirPošalji(odredištemacbe, ethernetTipbe, datapointer, veličina)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	brojcacheunos	int

	handler	IEthernetOkvirhandler
}

var handler IEthernetOkvirhandler

func (self *Arpprovider) Init(backend TEthernetOkvirprovider, userhandler IEthernetOkvirhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Skuphandler(userhandler, 0x0806)
	self.brojcacheunos = 0
	arpprovider = *self

}

func (self *Arpprovider) EthernetOkvirreceivewhen(datapointer uintptr, veličina uint32) bool {

	if veličina < arpmesgVeličina {
		return false
	}
	var arpbuffer *ArpPorukabuffer = (*ArpPorukabuffer)(Pointer(datapointer))
	var arp ArpPoruka = ArpPoruka{}
	arp.Init(arpbuffer)

	if arp.hardverTip == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardveraddressVeličina == 6 && arp.protocoladdressVeličina == 4 && uint64(arp.odredišteipaddress) == handler.Getipaddress() {

			arpconsole.MŠtampaj([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Štampaj(arp.protocol)
			arpconsole.MŠtampaj([]byte(":"))
			arpconsole.MUnsignedinteger64Štampaj(uint64(arp.odredištemacaddress))
			arpconsole.MŠtampaj([]byte(":"))
			arpconsole.MUnsignedinteger16Štampaj(arp.naredba)
			arpconsole.MŠtampaj([]byte(":"))
			arpconsole.MUnsignedinteger64Štampaj(handler.Getmacaddress())

			switch arp.naredba {
			case 0x0100:

				if self.Getmacfromcache(arp.izvoripaddress) == 0xFFFFFFFFFFFF {
					if self.brojcacheunos < 128 {
						self.Ipcache[self.brojcacheunos] = arp.izvoripaddress
						self.Maccache[self.brojcacheunos] = arp.izvormacaddress
						self.brojcacheunos++
					}
				}
				arp.naredba = 0x0200
				arp.odredišteipaddress = arp.izvoripaddress
				arp.odredištemacaddress = arp.izvormacaddress
				arp.izvoripaddress = uint32(handler.Getipaddress())
				arp.izvormacaddress = handler.Getmacaddress()
				arp.Skupbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MŠtampaj(([]byte)("self.numCacheEntries"))

				if self.brojcacheunos < 128 {
					self.Ipcache[self.brojcacheunos] = arp.izvoripaddress
					self.Maccache[self.brojcacheunos] = arp.izvormacaddress
					self.brojcacheunos++
				}
				break
			}

		}
	}
	return false

}

func (self *Arpprovider) Broadcastmacaddress(IpMrežabyteorder uint32) {

	var arp ArpPoruka = ArpPoruka{}
	arp.hardverTip = 0x0100
	arp.protocol = 0x0008
	arp.hardveraddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0200

	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = self.Resolve(IpMrežabyteorder)
	arp.odredišteipaddress = IpMrežabyteorder
	arpconsole.MŠtampajxy([]byte("broad mac"), 0, 15)

	arp.izvormacaddress = handler.Getmacaddress()

	var arpbuffer ArpPorukabuffer = ArpPorukabuffer{}
	arp.Skupbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pointer, arpmesgVeličina)
}
func (self *Arpprovider) Requestmacaddress(IpMrežabyteorder uint32) {

	var arp ArpPoruka = ArpPoruka{}
	arp.hardverTip = 0x0100

	arp.protocol = 0x0008
	arp.hardveraddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0100

	arp.izvormacaddress = handler.Getmacaddress()
	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = 0xFFFFFFFFFFFF
	arp.odredišteipaddress = IpMrežabyteorder

	var arpbuffer ArpPorukabuffer = ArpPorukabuffer{}
	arp.Skupbuffer(&arpbuffer)

	var pointer uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pointer, arpmesgVeličina)
}
func (self *Arpprovider) TestŠtampaj(data *[]byte, veličina uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MŠtampajxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalŠtampaj(buffer_2[i])
		arpconsole.MŠtampaj([]byte(":"))
	}
	arpconsole.MŠtampaj([]byte("]"))
}

func (self *Arpprovider) Getmacfromcache(IpMrežabyteorder uint32) uint64 {
	for i := 0; i < self.brojcacheunos; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MŠtampaj(([]byte)("["))
		arpconsole.MUnsignedinteger32Štampaj(self.Ipcache[i])
		arpconsole.MŠtampaj(([]byte)(":"))
		arpconsole.MUnsignedinteger32Štampaj(IpMrežabyteorder)
		arpconsole.MŠtampaj(([]byte)(":"))
		arpconsole.MŠtampaj(([]byte)(":"))
		arpconsole.MUnsignedinteger64Štampaj(self.Maccache[i])
		arpconsole.MŠtampaj(([]byte)("]\n"))

		if self.Ipcache[i] == IpMrežabyteorder {
			arpconsole.MŠtampaj([]byte("getmacfromcache"))
			return self.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (self *Arpprovider) Resolve(IpMrežabyteorder uint32) uint64 {
	var result uint64 = self.Getmacfromcache(IpMrežabyteorder)
	if result == 0xFFFFFFFFFFFF {
		self.Requestmacaddress(IpMrežabyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = self.Getmacfromcache(IpMrežabyteorder)

	}

	return result
}
