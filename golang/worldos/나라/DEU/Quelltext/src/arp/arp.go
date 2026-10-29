/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "konsole"
import . "rahmen_des_gemeinsamen_Übertragungsnetzes"
import . "hilfswerkzeug"

var arpKonsole TKonsole = TKonsole{}

type ArpNachrichtbuffer struct {
	geräteTyp		[2]byte
	protocol		[2]byte
	geräteaddressGröße	byte
	protocoladdressGröße	byte
	befehl			[2]byte

	quellemacaddress	[6]byte
	quelleipaddress		[4]byte
	zielmacaddress		[6]byte
	zielipaddress		[4]byte
}

var arpmesgGröße uint32 = (64+92+64)/8 + 2

type ArpNachricht struct {
	geräteTyp		uint16
	protocol		uint16
	geräteaddressGröße	uint8
	protocoladdressGröße	uint8
	befehl			uint16

	quellemacaddress	uint64
	quelleipaddress		uint32
	zielmacaddress		uint64
	zielipaddress		uint32
}

func (selbst *ArpNachricht) Init(buffer_2 *ArpNachrichtbuffer) {

	selbst.geräteTyp = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.geräteTyp))
	selbst.protocol = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.protocol))
	selbst.geräteaddressGröße = byte(buffer_2.geräteaddressGröße)
	selbst.protocoladdressGröße = byte(buffer_2.protocoladdressGröße)
	selbst.befehl = Unsignedinteger16r(Feldtounsignedinteger16(buffer_2.befehl))

	selbst.quellemacaddress = Unsignedinteger48r(Feldtounsignedinteger48(buffer_2.quellemacaddress))
	selbst.quelleipaddress = Unsignedinteger32r(Feldtounsignedinteger32(buffer_2.quelleipaddress))
	selbst.zielmacaddress = Unsignedinteger48r(Feldtounsignedinteger48(buffer_2.zielmacaddress))
	selbst.zielipaddress = Unsignedinteger32r(Feldtounsignedinteger32(buffer_2.zielipaddress))
}
func (selbst *ArpNachricht) Setzenbuffer(buffer_2 *ArpNachrichtbuffer) {
	buffer_2.geräteTyp = Unsignedinteger16toFeld(selbst.geräteTyp)
	buffer_2.protocol = Unsignedinteger16toFeld(selbst.protocol)
	buffer_2.geräteaddressGröße = uint8(selbst.geräteaddressGröße)
	buffer_2.protocoladdressGröße = uint8(selbst.protocoladdressGröße)

	buffer_2.befehl = Unsignedinteger16toFeld(selbst.befehl)
	buffer_2.quellemacaddress = Unsignedinteger48toFeld(selbst.quellemacaddress)
	buffer_2.quelleipaddress = Unsignedinteger32toFeld(selbst.quelleipaddress)
	buffer_2.zielmacaddress = Unsignedinteger48toFeld(selbst.zielmacaddress)
	buffer_2.zielipaddress = Unsignedinteger32toFeld(selbst.zielipaddress)
}

type ArpEthernetRahmenhandler struct {
	TEthernetRahmenhandler
}

var arpprovider Arpprovider
var rahmenanbieter_des_gemeinsamen_Übertragungsnetzes TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes

func (selbst *ArpEthernetRahmenhandler) EthernetRahmenreceivewhen(datenZeiger uintptr, größe int) bool {
	arpKonsole.MDruckenxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRahmenreceivewhen(datenZeiger, uint32(größe))

}
func (selbst *ArpEthernetRahmenhandler) Senden(zielmacbe uint64, datenZeiger uintptr, größe uint32) {
	arpKonsole.MDruckenxy([]byte("arp send:"), 0, 24)
	var ethernetTypbe = Unsignedinteger16r(0x0806)
	selbst.TEthernetRahmenhandler.RahmenSenden(zielmacbe, ethernetTypbe, datenZeiger, größe)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	nummercacheEintrag	int

	handler	IEthernetRahmenhandler
}

var handler IEthernetRahmenhandler

func (selbst *Arpprovider) Init(backend TRahmenanbieter_des_gemeinsamen_Übertragungsnetzes, userhandler IEthernetRahmenhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Setzenhandler(userhandler, 0x0806)
	selbst.nummercacheEintrag = 0
	arpprovider = *selbst

}

func (selbst *Arpprovider) EthernetRahmenreceivewhen(datenZeiger uintptr, größe uint32) bool {

	if größe < arpmesgGröße {
		return false
	}
	var arpbuffer *ArpNachrichtbuffer = (*ArpNachrichtbuffer)(Pointer(datenZeiger))
	var arp ArpNachricht = ArpNachricht{}
	arp.Init(arpbuffer)

	if arp.geräteTyp == 0x0100 {

		if arp.protocol == 0x0008 && arp.geräteaddressGröße == 6 && arp.protocoladdressGröße == 4 && uint64(arp.zielipaddress) == handler.Getipaddress() {

			arpKonsole.MDrucken([]byte("arp onetherframe"))
			arpKonsole.MUnsignedinteger16Drucken(arp.protocol)
			arpKonsole.MDrucken([]byte(":"))
			arpKonsole.MUnsignedinteger64Drucken(uint64(arp.zielmacaddress))
			arpKonsole.MDrucken([]byte(":"))
			arpKonsole.MUnsignedinteger16Drucken(arp.befehl)
			arpKonsole.MDrucken([]byte(":"))
			arpKonsole.MUnsignedinteger64Drucken(handler.Getmacaddress())

			switch arp.befehl {
			case 0x0100:

				if selbst.Getmacvoncache(arp.quelleipaddress) == 0xFFFFFFFFFFFF {
					if selbst.nummercacheEintrag < 128 {
						selbst.Ipcache[selbst.nummercacheEintrag] = arp.quelleipaddress
						selbst.Maccache[selbst.nummercacheEintrag] = arp.quellemacaddress
						selbst.nummercacheEintrag++
					}
				}
				arp.befehl = 0x0200
				arp.zielipaddress = arp.quelleipaddress
				arp.zielmacaddress = arp.quellemacaddress
				arp.quelleipaddress = uint32(handler.Getipaddress())
				arp.quellemacaddress = handler.Getmacaddress()
				arp.Setzenbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpKonsole.MDrucken(([]byte)("self.numCacheEntries"))

				if selbst.nummercacheEintrag < 128 {
					selbst.Ipcache[selbst.nummercacheEintrag] = arp.quelleipaddress
					selbst.Maccache[selbst.nummercacheEintrag] = arp.quellemacaddress
					selbst.nummercacheEintrag++
				}
				break
			}

		}
	}
	return false

}

func (selbst *Arpprovider) Broadcastmacaddress(IpNetzwerkByteorder uint32) {

	var arp ArpNachricht = ArpNachricht{}
	arp.geräteTyp = 0x0100
	arp.protocol = 0x0008
	arp.geräteaddressGröße = 6
	arp.protocoladdressGröße = 4
	arp.befehl = 0x0200

	arp.quelleipaddress = uint32(handler.Getipaddress())

	arp.zielmacaddress = selbst.Auflösen(IpNetzwerkByteorder)
	arp.zielipaddress = IpNetzwerkByteorder
	arpKonsole.MDruckenxy([]byte("broad mac"), 0, 15)

	arp.quellemacaddress = handler.Getmacaddress()

	var arpbuffer ArpNachrichtbuffer = ArpNachrichtbuffer{}
	arp.Setzenbuffer(&arpbuffer)

	var adressverweis uintptr = uintptr(Pointer(&arpbuffer))
	handler.Senden(arp.zielmacaddress, adressverweis, arpmesgGröße)
}
func (selbst *Arpprovider) Requestmacaddress(IpNetzwerkByteorder uint32) {

	var arp ArpNachricht = ArpNachricht{}
	arp.geräteTyp = 0x0100

	arp.protocol = 0x0008
	arp.geräteaddressGröße = 6
	arp.protocoladdressGröße = 4
	arp.befehl = 0x0100

	arp.quellemacaddress = handler.Getmacaddress()
	arp.quelleipaddress = uint32(handler.Getipaddress())

	arp.zielmacaddress = 0xFFFFFFFFFFFF
	arp.zielipaddress = IpNetzwerkByteorder

	var arpbuffer ArpNachrichtbuffer = ArpNachrichtbuffer{}
	arp.Setzenbuffer(&arpbuffer)

	var adressverweis uintptr = uintptr(Pointer(&arpbuffer))
	handler.Senden(arp.zielmacaddress, adressverweis, arpmesgGröße)
}
func (selbst *Arpprovider) TestenDrucken(daten *[]byte, größe uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(daten))
	arpKonsole.MDruckenxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonsole.MHexadecimalDrucken(buffer_2[i])
		arpKonsole.MDrucken([]byte(":"))
	}
	arpKonsole.MDrucken([]byte("]"))
}

func (selbst *Arpprovider) Getmacvoncache(IpNetzwerkByteorder uint32) uint64 {
	for i := 0; i < selbst.nummercacheEintrag; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonsole.MDrucken(([]byte)("["))
		arpKonsole.MUnsignedinteger32Drucken(selbst.Ipcache[i])
		arpKonsole.MDrucken(([]byte)(":"))
		arpKonsole.MUnsignedinteger32Drucken(IpNetzwerkByteorder)
		arpKonsole.MDrucken(([]byte)(":"))
		arpKonsole.MDrucken(([]byte)(":"))
		arpKonsole.MUnsignedinteger64Drucken(selbst.Maccache[i])
		arpKonsole.MDrucken(([]byte)("]\n"))

		if selbst.Ipcache[i] == IpNetzwerkByteorder {
			arpKonsole.MDrucken([]byte("getmacfromcache"))
			return selbst.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (selbst *Arpprovider) Auflösen(IpNetzwerkByteorder uint32) uint64 {
	var ergebnis uint64 = selbst.Getmacvoncache(IpNetzwerkByteorder)
	if ergebnis == 0xFFFFFFFFFFFF {
		selbst.Requestmacaddress(IpNetzwerkByteorder)
	}
	for i := 0; i < 128 && ergebnis == 0xFFFFFFFFFFFF; i++ {
		ergebnis = selbst.Getmacvoncache(IpNetzwerkByteorder)

	}

	return ergebnis
}
