/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "console"
import . "trama_della_rete_a_mezzo_condiviso"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpMessaggiobuffer struct {
	hardwareTipo			[2]byte
	protocol			[2]byte
	hardwareaddressDimensione	byte
	protocoladdressDimensione	byte
	comando				[2]byte

	originemacaddress	[6]byte
	origineipaddress	[4]byte
	destinazionemacaddress	[6]byte
	destinazioneipaddress	[4]byte
}

var arpmesgDimensione uint32 = (64+92+64)/8 + 2

type ArpMessaggio struct {
	hardwareTipo			uint16
	protocol			uint16
	hardwareaddressDimensione	uint8
	protocoladdressDimensione	uint8
	comando				uint16

	originemacaddress	uint64
	origineipaddress	uint32
	destinazionemacaddress	uint64
	destinazioneipaddress	uint32
}

func (séstesso *ArpMessaggio) Init(buffer_2 *ArpMessaggiobuffer) {

	séstesso.hardwareTipo = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.hardwareTipo))
	séstesso.protocol = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.protocol))
	séstesso.hardwareaddressDimensione = byte(buffer_2.hardwareaddressDimensione)
	séstesso.protocoladdressDimensione = byte(buffer_2.protocoladdressDimensione)
	séstesso.comando = Unsignedinteger16r(Serietounsignedinteger16(buffer_2.comando))

	séstesso.originemacaddress = Unsignedinteger48r(Serietounsignedinteger48(buffer_2.originemacaddress))
	séstesso.origineipaddress = Unsignedinteger32r(Serietounsignedinteger32(buffer_2.origineipaddress))
	séstesso.destinazionemacaddress = Unsignedinteger48r(Serietounsignedinteger48(buffer_2.destinazionemacaddress))
	séstesso.destinazioneipaddress = Unsignedinteger32r(Serietounsignedinteger32(buffer_2.destinazioneipaddress))
}
func (séstesso *ArpMessaggio) Impostabuffer(buffer_2 *ArpMessaggiobuffer) {
	buffer_2.hardwareTipo = Unsignedinteger16toSerie(séstesso.hardwareTipo)
	buffer_2.protocol = Unsignedinteger16toSerie(séstesso.protocol)
	buffer_2.hardwareaddressDimensione = uint8(séstesso.hardwareaddressDimensione)
	buffer_2.protocoladdressDimensione = uint8(séstesso.protocoladdressDimensione)

	buffer_2.comando = Unsignedinteger16toSerie(séstesso.comando)
	buffer_2.originemacaddress = Unsignedinteger48toSerie(séstesso.originemacaddress)
	buffer_2.origineipaddress = Unsignedinteger32toSerie(séstesso.origineipaddress)
	buffer_2.destinazionemacaddress = Unsignedinteger48toSerie(séstesso.destinazionemacaddress)
	buffer_2.destinazioneipaddress = Unsignedinteger32toSerie(séstesso.destinazioneipaddress)
}

type ArpethernetRiquadrohandler struct {
	TEthernetRiquadrohandler
}

var arpprovider Arpprovider
var fornitore_di_trame_di_rete_a_mezzo_condiviso TFornitore_di_trame_di_rete_a_mezzo_condiviso

func (séstesso *ArpethernetRiquadrohandler) EthernetRiquadroreceivewhen(dataPuntatore uintptr, dimensione int) bool {
	arpconsole.MStampaxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetRiquadroreceivewhen(dataPuntatore, uint32(dimensione))

}
func (séstesso *ArpethernetRiquadrohandler) Spedisci(destinazionemacbe uint64, dataPuntatore uintptr, dimensione uint32) {
	arpconsole.MStampaxy([]byte("arp send:"), 0, 24)
	var ethernetTipobe = Unsignedinteger16r(0x0806)
	séstesso.TEthernetRiquadrohandler.RiquadroSpedisci(destinazionemacbe, ethernetTipobe, dataPuntatore, dimensione)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	numerocachevoce	int

	handler	IEthernetRiquadrohandler
}

var handler IEthernetRiquadrohandler

func (séstesso *Arpprovider) Init(backend TFornitore_di_trame_di_rete_a_mezzo_condiviso, userhandler IEthernetRiquadrohandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Impostahandler(userhandler, 0x0806)
	séstesso.numerocachevoce = 0
	arpprovider = *séstesso

}

func (séstesso *Arpprovider) EthernetRiquadroreceivewhen(dataPuntatore uintptr, dimensione uint32) bool {

	if dimensione < arpmesgDimensione {
		return false
	}
	var arpbuffer *ArpMessaggiobuffer = (*ArpMessaggiobuffer)(Pointer(dataPuntatore))
	var arp ArpMessaggio = ArpMessaggio{}
	arp.Init(arpbuffer)

	if arp.hardwareTipo == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardwareaddressDimensione == 6 && arp.protocoladdressDimensione == 4 && uint64(arp.destinazioneipaddress) == handler.Getipaddress() {

			arpconsole.MStampa([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Stampa(arp.protocol)
			arpconsole.MStampa([]byte(":"))
			arpconsole.MUnsignedinteger64Stampa(uint64(arp.destinazionemacaddress))
			arpconsole.MStampa([]byte(":"))
			arpconsole.MUnsignedinteger16Stampa(arp.comando)
			arpconsole.MStampa([]byte(":"))
			arpconsole.MUnsignedinteger64Stampa(handler.Getmacaddress())

			switch arp.comando {
			case 0x0100:

				if séstesso.Getmacfromcache(arp.origineipaddress) == 0xFFFFFFFFFFFF {
					if séstesso.numerocachevoce < 128 {
						séstesso.Ipcache[séstesso.numerocachevoce] = arp.origineipaddress
						séstesso.Maccache[séstesso.numerocachevoce] = arp.originemacaddress
						séstesso.numerocachevoce++
					}
				}
				arp.comando = 0x0200
				arp.destinazioneipaddress = arp.origineipaddress
				arp.destinazionemacaddress = arp.originemacaddress
				arp.origineipaddress = uint32(handler.Getipaddress())
				arp.originemacaddress = handler.Getmacaddress()
				arp.Impostabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MStampa(([]byte)("self.numCacheEntries"))

				if séstesso.numerocachevoce < 128 {
					séstesso.Ipcache[séstesso.numerocachevoce] = arp.origineipaddress
					séstesso.Maccache[séstesso.numerocachevoce] = arp.originemacaddress
					séstesso.numerocachevoce++
				}
				break
			}

		}
	}
	return false

}

func (séstesso *Arpprovider) Broadcastmacaddress(IpRetebyteorder uint32) {

	var arp ArpMessaggio = ArpMessaggio{}
	arp.hardwareTipo = 0x0100
	arp.protocol = 0x0008
	arp.hardwareaddressDimensione = 6
	arp.protocoladdressDimensione = 4
	arp.comando = 0x0200

	arp.origineipaddress = uint32(handler.Getipaddress())

	arp.destinazionemacaddress = séstesso.Resolve(IpRetebyteorder)
	arp.destinazioneipaddress = IpRetebyteorder
	arpconsole.MStampaxy([]byte("broad mac"), 0, 15)

	arp.originemacaddress = handler.Getmacaddress()

	var arpbuffer ArpMessaggiobuffer = ArpMessaggiobuffer{}
	arp.Impostabuffer(&arpbuffer)

	var riferimento_di_memoria uintptr = uintptr(Pointer(&arpbuffer))
	handler.Spedisci(arp.destinazionemacaddress, riferimento_di_memoria, arpmesgDimensione)
}
func (séstesso *Arpprovider) Requestmacaddress(IpRetebyteorder uint32) {

	var arp ArpMessaggio = ArpMessaggio{}
	arp.hardwareTipo = 0x0100

	arp.protocol = 0x0008
	arp.hardwareaddressDimensione = 6
	arp.protocoladdressDimensione = 4
	arp.comando = 0x0100

	arp.originemacaddress = handler.Getmacaddress()
	arp.origineipaddress = uint32(handler.Getipaddress())

	arp.destinazionemacaddress = 0xFFFFFFFFFFFF
	arp.destinazioneipaddress = IpRetebyteorder

	var arpbuffer ArpMessaggiobuffer = ArpMessaggiobuffer{}
	arp.Impostabuffer(&arpbuffer)

	var riferimento_di_memoria uintptr = uintptr(Pointer(&arpbuffer))
	handler.Spedisci(arp.destinazionemacaddress, riferimento_di_memoria, arpmesgDimensione)
}
func (séstesso *Arpprovider) ProvaStampa(data *[]byte, dimensione uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MStampaxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalStampa(buffer_2[i])
		arpconsole.MStampa([]byte(":"))
	}
	arpconsole.MStampa([]byte("]"))
}

func (séstesso *Arpprovider) Getmacfromcache(IpRetebyteorder uint32) uint64 {
	for i := 0; i < séstesso.numerocachevoce; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MStampa(([]byte)("["))
		arpconsole.MUnsignedinteger32Stampa(séstesso.Ipcache[i])
		arpconsole.MStampa(([]byte)(":"))
		arpconsole.MUnsignedinteger32Stampa(IpRetebyteorder)
		arpconsole.MStampa(([]byte)(":"))
		arpconsole.MStampa(([]byte)(":"))
		arpconsole.MUnsignedinteger64Stampa(séstesso.Maccache[i])
		arpconsole.MStampa(([]byte)("]\n"))

		if séstesso.Ipcache[i] == IpRetebyteorder {
			arpconsole.MStampa([]byte("getmacfromcache"))
			return séstesso.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (séstesso *Arpprovider) Resolve(IpRetebyteorder uint32) uint64 {
	var rISULTATO uint64 = séstesso.Getmacfromcache(IpRetebyteorder)
	if rISULTATO == 0xFFFFFFFFFFFF {
		séstesso.Requestmacaddress(IpRetebyteorder)
	}
	for i := 0; i < 128 && rISULTATO == 0xFFFFFFFFFFFF; i++ {
		rISULTATO = séstesso.Getmacfromcache(IpRetebyteorder)

	}

	return rISULTATO
}
