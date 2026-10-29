/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "локалнамрежаEthernetРамка"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpСЪОБЩЕНИЕbuffer struct {
	хардуерТип		[2]byte
	protocol		[2]byte
	хардуерaddressРазмер	byte
	protocoladdressРазмер	byte
	команда			[2]byte

	източникmacaddress	[6]byte
	източникipaddress	[4]byte
	назначениеmacaddress	[6]byte
	назначениеipaddress	[4]byte
}

var arpmesgРазмер uint32 = (64+92+64)/8 + 2

type ArpСЪОБЩЕНИЕ struct {
	хардуерТип		uint16
	protocol		uint16
	хардуерaddressРазмер	uint8
	protocoladdressРазмер	uint8
	команда			uint16

	източникmacaddress	uint64
	източникipaddress	uint32
	назначениеmacaddress	uint64
	назначениеipaddress	uint32
}

func (себеси *ArpСЪОБЩЕНИЕ) Init(buffer_2 *ArpСЪОБЩЕНИЕbuffer) {

	себеси.хардуерТип = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.хардуерТип))
	себеси.protocol = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.protocol))
	себеси.хардуерaddressРазмер = byte(buffer_2.хардуерaddressРазмер)
	себеси.protocoladdressРазмер = byte(buffer_2.protocoladdressРазмер)
	себеси.команда = Unsignedinteger16r(Масивtounsignedinteger16(buffer_2.команда))

	себеси.източникmacaddress = Unsignedinteger48r(Масивtounsignedinteger48(buffer_2.източникmacaddress))
	себеси.източникipaddress = Unsignedinteger32r(Масивtounsignedinteger32(buffer_2.източникipaddress))
	себеси.назначениеmacaddress = Unsignedinteger48r(Масивtounsignedinteger48(buffer_2.назначениеmacaddress))
	себеси.назначениеipaddress = Unsignedinteger32r(Масивtounsignedinteger32(buffer_2.назначениеipaddress))
}
func (себеси *ArpСЪОБЩЕНИЕ) Задайbuffer(buffer_2 *ArpСЪОБЩЕНИЕbuffer) {
	buffer_2.хардуерТип = Unsignedinteger16toМасив(себеси.хардуерТип)
	buffer_2.protocol = Unsignedinteger16toМасив(себеси.protocol)
	buffer_2.хардуерaddressРазмер = uint8(себеси.хардуерaddressРазмер)
	buffer_2.protocoladdressРазмер = uint8(себеси.protocoladdressРазмер)

	buffer_2.команда = Unsignedinteger16toМасив(себеси.команда)
	buffer_2.източникmacaddress = Unsignedinteger48toМасив(себеси.източникmacaddress)
	buffer_2.източникipaddress = Unsignedinteger32toМасив(себеси.източникipaddress)
	buffer_2.назначениеmacaddress = Unsignedinteger48toМасив(себеси.назначениеmacaddress)
	buffer_2.назначениеipaddress = Unsignedinteger32toМасив(себеси.назначениеipaddress)
}

type ArpЛокалнамрежаEthernetРамкаhandler struct {
	TЛокалнамрежаEthernetРамкаhandler
}

var arpprovider Arpprovider
var локалнамрежаEthernetРамкаprovider TЛокалнамрежаEthernetРамкаprovider

func (себеси *ArpЛокалнамрежаEthernetРамкаhandler) ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци uintptr, размер int) bool {
	arpconsole.MПечатxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци, uint32(размер))

}
func (себеси *ArpЛокалнамрежаEthernetРамкаhandler) Изпращане(назначениеmacbe uint64, dataПоказалци uintptr, размер uint32) {
	arpconsole.MПечатxy([]byte("arp send:"), 0, 24)
	var локалнамрежаEthernetТипbe = Unsignedinteger16r(0x0806)
	себеси.TЛокалнамрежаEthernetРамкаhandler.РамкаИзпращане(назначениеmacbe, локалнамрежаEthernetТипbe, dataПоказалци, размер)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	числоcacheзапис	int

	handler	IЛокалнамрежаEthernetРамкаhandler
}

var handler IЛокалнамрежаEthernetРамкаhandler

func (себеси *Arpprovider) Init(backend TЛокалнамрежаEthernetРамкаprovider, userhandler IЛокалнамрежаEthernetРамкаhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Задайhandler(userhandler, 0x0806)
	себеси.числоcacheзапис = 0
	arpprovider = *себеси

}

func (себеси *Arpprovider) ЛокалнамрежаEthernetРамкаreceivewhen(dataПоказалци uintptr, размер uint32) bool {

	if размер < arpmesgРазмер {
		return false
	}
	var arpbuffer *ArpСЪОБЩЕНИЕbuffer = (*ArpСЪОБЩЕНИЕbuffer)(Pointer(dataПоказалци))
	var arp ArpСЪОБЩЕНИЕ = ArpСЪОБЩЕНИЕ{}
	arp.Init(arpbuffer)

	if arp.хардуерТип == 0x0100 {

		if arp.protocol == 0x0008 && arp.хардуерaddressРазмер == 6 && arp.protocoladdressРазмер == 4 && uint64(arp.назначениеipaddress) == handler.Getipaddress() {

			arpconsole.MПечат([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Печат(arp.protocol)
			arpconsole.MПечат([]byte(":"))
			arpconsole.MUnsignedinteger64Печат(uint64(arp.назначениеmacaddress))
			arpconsole.MПечат([]byte(":"))
			arpconsole.MUnsignedinteger16Печат(arp.команда)
			arpconsole.MПечат([]byte(":"))
			arpconsole.MUnsignedinteger64Печат(handler.Getmacaddress())

			switch arp.команда {
			case 0x0100:

				if себеси.Getmacfromcache(arp.източникipaddress) == 0xFFFFFFFFFFFF {
					if себеси.числоcacheзапис < 128 {
						себеси.Ipcache[себеси.числоcacheзапис] = arp.източникipaddress
						себеси.Maccache[себеси.числоcacheзапис] = arp.източникmacaddress
						себеси.числоcacheзапис++
					}
				}
				arp.команда = 0x0200
				arp.назначениеipaddress = arp.източникipaddress
				arp.назначениеmacaddress = arp.източникmacaddress
				arp.източникipaddress = uint32(handler.Getipaddress())
				arp.източникmacaddress = handler.Getmacaddress()
				arp.Задайbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MПечат(([]byte)("self.numCacheEntries"))

				if себеси.числоcacheзапис < 128 {
					себеси.Ipcache[себеси.числоcacheзапис] = arp.източникipaddress
					себеси.Maccache[себеси.числоcacheзапис] = arp.източникmacaddress
					себеси.числоcacheзапис++
				}
				break
			}

		}
	}
	return false

}

func (себеси *Arpprovider) Broadcastmacaddress(IpМрежаbyteorder uint32) {

	var arp ArpСЪОБЩЕНИЕ = ArpСЪОБЩЕНИЕ{}
	arp.хардуерТип = 0x0100
	arp.protocol = 0x0008
	arp.хардуерaddressРазмер = 6
	arp.protocoladdressРазмер = 4
	arp.команда = 0x0200

	arp.източникipaddress = uint32(handler.Getipaddress())

	arp.назначениеmacaddress = себеси.Resolve(IpМрежаbyteorder)
	arp.назначениеipaddress = IpМрежаbyteorder
	arpconsole.MПечатxy([]byte("broad mac"), 0, 15)

	arp.източникmacaddress = handler.Getmacaddress()

	var arpbuffer ArpСЪОБЩЕНИЕbuffer = ArpСЪОБЩЕНИЕbuffer{}
	arp.Задайbuffer(&arpbuffer)

	var показалци uintptr = uintptr(Pointer(&arpbuffer))
	handler.Изпращане(arp.назначениеmacaddress, показалци, arpmesgРазмер)
}
func (себеси *Arpprovider) Requestmacaddress(IpМрежаbyteorder uint32) {

	var arp ArpСЪОБЩЕНИЕ = ArpСЪОБЩЕНИЕ{}
	arp.хардуерТип = 0x0100

	arp.protocol = 0x0008
	arp.хардуерaddressРазмер = 6
	arp.protocoladdressРазмер = 4
	arp.команда = 0x0100

	arp.източникmacaddress = handler.Getmacaddress()
	arp.източникipaddress = uint32(handler.Getipaddress())

	arp.назначениеmacaddress = 0xFFFFFFFFFFFF
	arp.назначениеipaddress = IpМрежаbyteorder

	var arpbuffer ArpСЪОБЩЕНИЕbuffer = ArpСЪОБЩЕНИЕbuffer{}
	arp.Задайbuffer(&arpbuffer)

	var показалци uintptr = uintptr(Pointer(&arpbuffer))
	handler.Изпращане(arp.назначениеmacaddress, показалци, arpmesgРазмер)
}
func (себеси *Arpprovider) ТестПечат(data *[]byte, размер uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MПечатxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalПечат(buffer_2[i])
		arpconsole.MПечат([]byte(":"))
	}
	arpconsole.MПечат([]byte("]"))
}

func (себеси *Arpprovider) Getmacfromcache(IpМрежаbyteorder uint32) uint64 {
	for i := 0; i < себеси.числоcacheзапис; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MПечат(([]byte)("["))
		arpconsole.MUnsignedinteger32Печат(себеси.Ipcache[i])
		arpconsole.MПечат(([]byte)(":"))
		arpconsole.MUnsignedinteger32Печат(IpМрежаbyteorder)
		arpconsole.MПечат(([]byte)(":"))
		arpconsole.MПечат(([]byte)(":"))
		arpconsole.MUnsignedinteger64Печат(себеси.Maccache[i])
		arpconsole.MПечат(([]byte)("]\n"))

		if себеси.Ipcache[i] == IpМрежаbyteorder {
			arpconsole.MПечат([]byte("getmacfromcache"))
			return себеси.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (себеси *Arpprovider) Resolve(IpМрежаbyteorder uint32) uint64 {
	var рЕЗУЛТАТ uint64 = себеси.Getmacfromcache(IpМрежаbyteorder)
	if рЕЗУЛТАТ == 0xFFFFFFFFFFFF {
		себеси.Requestmacaddress(IpМрежаbyteorder)
	}
	for i := 0; i < 128 && рЕЗУЛТАТ == 0xFFFFFFFFFFFF; i++ {
		рЕЗУЛТАТ = себеси.Getmacfromcache(IpМрежаbyteorder)

	}

	return рЕЗУЛТАТ
}
