package arp

import . "unsafe"
import . "console"
import . "ethernetCadru"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpMesajbuffer struct {
	componenteTip		[2]byte
	protocol		[2]byte
	componenteaddressMărime	byte
	protocoladdressMărime	byte
	comandă			[2]byte

	sursămacaddress		[6]byte
	sursăipaddress		[4]byte
	destinațiemacaddress	[6]byte
	destinațieipaddress	[4]byte
}

var arpmesgMărime uint32 = (64+92+64)/8 + 2

type ArpMesaj struct {
	componenteTip		uint16
	protocol		uint16
	componenteaddressMărime	uint8
	protocoladdressMărime	uint8
	comandă			uint16

	sursămacaddress		uint64
	sursăipaddress		uint32
	destinațiemacaddress	uint64
	destinațieipaddress	uint32
}

func (sine *ArpMesaj) Init(buffer_2 *ArpMesajbuffer) {

	sine.componenteTip = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.componenteTip))
	sine.protocol = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.protocol))
	sine.componenteaddressMărime = byte(buffer_2.componenteaddressMărime)
	sine.protocoladdressMărime = byte(buffer_2.protocoladdressMărime)
	sine.comandă = Unsignedinteger16r(Vectortounsignedinteger16(buffer_2.comandă))

	sine.sursămacaddress = Unsignedinteger48r(Vectortounsignedinteger48(buffer_2.sursămacaddress))
	sine.sursăipaddress = Unsignedinteger32r(Vectortounsignedinteger32(buffer_2.sursăipaddress))
	sine.destinațiemacaddress = Unsignedinteger48r(Vectortounsignedinteger48(buffer_2.destinațiemacaddress))
	sine.destinațieipaddress = Unsignedinteger32r(Vectortounsignedinteger32(buffer_2.destinațieipaddress))
}
func (sine *ArpMesaj) Definitbuffer(buffer_2 *ArpMesajbuffer) {
	buffer_2.componenteTip = Unsignedinteger16toVector(sine.componenteTip)
	buffer_2.protocol = Unsignedinteger16toVector(sine.protocol)
	buffer_2.componenteaddressMărime = uint8(sine.componenteaddressMărime)
	buffer_2.protocoladdressMărime = uint8(sine.protocoladdressMărime)

	buffer_2.comandă = Unsignedinteger16toVector(sine.comandă)
	buffer_2.sursămacaddress = Unsignedinteger48toVector(sine.sursămacaddress)
	buffer_2.sursăipaddress = Unsignedinteger32toVector(sine.sursăipaddress)
	buffer_2.destinațiemacaddress = Unsignedinteger48toVector(sine.destinațiemacaddress)
	buffer_2.destinațieipaddress = Unsignedinteger32toVector(sine.destinațieipaddress)
}

type ArpethernetCadruhandler struct {
	TEthernetCadruhandler
}

var arpprovider Arpprovider
var ethernetCadruprovider TEthernetCadruprovider

func (sine *ArpethernetCadruhandler) EthernetCadrureceivewhen(dataIndicator uintptr, mărime int) bool {
	arpconsole.MTipăreștexy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetCadrureceivewhen(dataIndicator, uint32(mărime))

}
func (sine *ArpethernetCadruhandler) Trimite(destinațiemacbe uint64, dataIndicator uintptr, mărime uint32) {
	arpconsole.MTipăreștexy([]byte("arp send:"), 0, 24)
	var ethernetTipbe = Unsignedinteger16r(0x0806)
	sine.TEthernetCadruhandler.CadruTrimite(destinațiemacbe, ethernetTipbe, dataIndicator, mărime)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	numărcacheînregistrare	int

	handler	IEthernetCadruhandler
}

var handler IEthernetCadruhandler

func (sine *Arpprovider) Init(backend TEthernetCadruprovider, userhandler IEthernetCadruhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Definithandler(userhandler, 0x0806)
	sine.numărcacheînregistrare = 0
	arpprovider = *sine

}

func (sine *Arpprovider) EthernetCadrureceivewhen(dataIndicator uintptr, mărime uint32) bool {

	if mărime < arpmesgMărime {
		return false
	}
	var arpbuffer *ArpMesajbuffer = (*ArpMesajbuffer)(Pointer(dataIndicator))
	var arp ArpMesaj = ArpMesaj{}
	arp.Init(arpbuffer)

	if arp.componenteTip == 0x0100 {

		if arp.protocol == 0x0008 && arp.componenteaddressMărime == 6 && arp.protocoladdressMărime == 4 && uint64(arp.destinațieipaddress) == handler.Getipaddress() {

			arpconsole.MTipărește([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Tipărește(arp.protocol)
			arpconsole.MTipărește([]byte(":"))
			arpconsole.MUnsignedinteger64Tipărește(uint64(arp.destinațiemacaddress))
			arpconsole.MTipărește([]byte(":"))
			arpconsole.MUnsignedinteger16Tipărește(arp.comandă)
			arpconsole.MTipărește([]byte(":"))
			arpconsole.MUnsignedinteger64Tipărește(handler.Getmacaddress())

			switch arp.comandă {
			case 0x0100:

				if sine.Getmacfromcache(arp.sursăipaddress) == 0xFFFFFFFFFFFF {
					if sine.numărcacheînregistrare < 128 {
						sine.Ipcache[sine.numărcacheînregistrare] = arp.sursăipaddress
						sine.Maccache[sine.numărcacheînregistrare] = arp.sursămacaddress
						sine.numărcacheînregistrare++
					}
				}
				arp.comandă = 0x0200
				arp.destinațieipaddress = arp.sursăipaddress
				arp.destinațiemacaddress = arp.sursămacaddress
				arp.sursăipaddress = uint32(handler.Getipaddress())
				arp.sursămacaddress = handler.Getmacaddress()
				arp.Definitbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MTipărește(([]byte)("self.numCacheEntries"))

				if sine.numărcacheînregistrare < 128 {
					sine.Ipcache[sine.numărcacheînregistrare] = arp.sursăipaddress
					sine.Maccache[sine.numărcacheînregistrare] = arp.sursămacaddress
					sine.numărcacheînregistrare++
				}
				break
			}

		}
	}
	return false

}

func (sine *Arpprovider) Broadcastmacaddress(IpRețeabyteorder uint32) {

	var arp ArpMesaj = ArpMesaj{}
	arp.componenteTip = 0x0100
	arp.protocol = 0x0008
	arp.componenteaddressMărime = 6
	arp.protocoladdressMărime = 4
	arp.comandă = 0x0200

	arp.sursăipaddress = uint32(handler.Getipaddress())

	arp.destinațiemacaddress = sine.Resolve(IpRețeabyteorder)
	arp.destinațieipaddress = IpRețeabyteorder
	arpconsole.MTipăreștexy([]byte("broad mac"), 0, 15)

	arp.sursămacaddress = handler.Getmacaddress()

	var arpbuffer ArpMesajbuffer = ArpMesajbuffer{}
	arp.Definitbuffer(&arpbuffer)

	var indicator uintptr = uintptr(Pointer(&arpbuffer))
	handler.Trimite(arp.destinațiemacaddress, indicator, arpmesgMărime)
}
func (sine *Arpprovider) Requestmacaddress(IpRețeabyteorder uint32) {

	var arp ArpMesaj = ArpMesaj{}
	arp.componenteTip = 0x0100

	arp.protocol = 0x0008
	arp.componenteaddressMărime = 6
	arp.protocoladdressMărime = 4
	arp.comandă = 0x0100

	arp.sursămacaddress = handler.Getmacaddress()
	arp.sursăipaddress = uint32(handler.Getipaddress())

	arp.destinațiemacaddress = 0xFFFFFFFFFFFF
	arp.destinațieipaddress = IpRețeabyteorder

	var arpbuffer ArpMesajbuffer = ArpMesajbuffer{}
	arp.Definitbuffer(&arpbuffer)

	var indicator uintptr = uintptr(Pointer(&arpbuffer))
	handler.Trimite(arp.destinațiemacaddress, indicator, arpmesgMărime)
}
func (sine *Arpprovider) TesteazăTipărește(data *[]byte, mărime uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MTipăreștexy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalTipărește(buffer_2[i])
		arpconsole.MTipărește([]byte(":"))
	}
	arpconsole.MTipărește([]byte("]"))
}

func (sine *Arpprovider) Getmacfromcache(IpRețeabyteorder uint32) uint64 {
	for i := 0; i < sine.numărcacheînregistrare; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MTipărește(([]byte)("["))
		arpconsole.MUnsignedinteger32Tipărește(sine.Ipcache[i])
		arpconsole.MTipărește(([]byte)(":"))
		arpconsole.MUnsignedinteger32Tipărește(IpRețeabyteorder)
		arpconsole.MTipărește(([]byte)(":"))
		arpconsole.MTipărește(([]byte)(":"))
		arpconsole.MUnsignedinteger64Tipărește(sine.Maccache[i])
		arpconsole.MTipărește(([]byte)("]\n"))

		if sine.Ipcache[i] == IpRețeabyteorder {
			arpconsole.MTipărește([]byte("getmacfromcache"))
			return sine.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (sine *Arpprovider) Resolve(IpRețeabyteorder uint32) uint64 {
	var result uint64 = sine.Getmacfromcache(IpRețeabyteorder)
	if result == 0xFFFFFFFFFFFF {
		sine.Requestmacaddress(IpRețeabyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = sine.Getmacfromcache(IpRețeabyteorder)

	}

	return result
}
