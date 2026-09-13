package arp

import . "unsafe"
import . "console"
import . "ethernetIetvars"
import . "util"

var arpconsole TConsole = TConsole{}

type ArpZiņojumsbuffer struct {
	aparatūraTips		[2]byte
	protocol		[2]byte
	aparatūraaddressIzmērs	byte
	protocoladdressIzmērs	byte
	komanda			[2]byte

	avotsmacaddress		[6]byte
	avotsipaddress		[4]byte
	mērķismacaddress	[6]byte
	mērķisipaddress		[4]byte
}

var arpmesgIzmērs uint32 = (64+92+64)/8 + 2

type ArpZiņojums struct {
	aparatūraTips		uint16
	protocol		uint16
	aparatūraaddressIzmērs	uint8
	protocoladdressIzmērs	uint8
	komanda			uint16

	avotsmacaddress		uint64
	avotsipaddress		uint32
	mērķismacaddress	uint64
	mērķisipaddress		uint32
}

func (pats *ArpZiņojums) Init(buffer_2 *ArpZiņojumsbuffer) {

	pats.aparatūraTips = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.aparatūraTips))
	pats.protocol = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.protocol))
	pats.aparatūraaddressIzmērs = byte(buffer_2.aparatūraaddressIzmērs)
	pats.protocoladdressIzmērs = byte(buffer_2.protocoladdressIzmērs)
	pats.komanda = Unsignedinteger16r(Masīvstounsignedinteger16(buffer_2.komanda))

	pats.avotsmacaddress = Unsignedinteger48r(Masīvstounsignedinteger48(buffer_2.avotsmacaddress))
	pats.avotsipaddress = Unsignedinteger32r(Masīvstounsignedinteger32(buffer_2.avotsipaddress))
	pats.mērķismacaddress = Unsignedinteger48r(Masīvstounsignedinteger48(buffer_2.mērķismacaddress))
	pats.mērķisipaddress = Unsignedinteger32r(Masīvstounsignedinteger32(buffer_2.mērķisipaddress))
}
func (pats *ArpZiņojums) Kopabuffer(buffer_2 *ArpZiņojumsbuffer) {
	buffer_2.aparatūraTips = Unsignedinteger16toMasīvs(pats.aparatūraTips)
	buffer_2.protocol = Unsignedinteger16toMasīvs(pats.protocol)
	buffer_2.aparatūraaddressIzmērs = uint8(pats.aparatūraaddressIzmērs)
	buffer_2.protocoladdressIzmērs = uint8(pats.protocoladdressIzmērs)

	buffer_2.komanda = Unsignedinteger16toMasīvs(pats.komanda)
	buffer_2.avotsmacaddress = Unsignedinteger48toMasīvs(pats.avotsmacaddress)
	buffer_2.avotsipaddress = Unsignedinteger32toMasīvs(pats.avotsipaddress)
	buffer_2.mērķismacaddress = Unsignedinteger48toMasīvs(pats.mērķismacaddress)
	buffer_2.mērķisipaddress = Unsignedinteger32toMasīvs(pats.mērķisipaddress)
}

type ArpethernetIetvarshandler struct {
	TEthernetIetvarshandler
}

var arpprovider Arpprovider
var ethernetIetvarsprovider TEthernetIetvarsprovider

func (pats *ArpethernetIetvarshandler) EthernetIetvarsreceivewhen(dataKursors uintptr, izmērs int) bool {
	arpconsole.MDrukātxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetIetvarsreceivewhen(dataKursors, uint32(izmērs))

}
func (pats *ArpethernetIetvarshandler) Sūtīt(mērķismacbe uint64, dataKursors uintptr, izmērs uint32) {
	arpconsole.MDrukātxy([]byte("arp send:"), 0, 24)
	var ethernetTipsbe = Unsignedinteger16r(0x0806)
	pats.TEthernetIetvarshandler.IetvarsSūtīt(mērķismacbe, ethernetTipsbe, dataKursors, izmērs)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	skaitliscacheieraksts	int

	handler	IEthernetIetvarshandler
}

var handler IEthernetIetvarshandler

func (pats *Arpprovider) Init(backend TEthernetIetvarsprovider, userhandler IEthernetIetvarshandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Kopahandler(userhandler, 0x0806)
	pats.skaitliscacheieraksts = 0
	arpprovider = *pats

}

func (pats *Arpprovider) EthernetIetvarsreceivewhen(dataKursors uintptr, izmērs uint32) bool {

	if izmērs < arpmesgIzmērs {
		return false
	}
	var arpbuffer *ArpZiņojumsbuffer = (*ArpZiņojumsbuffer)(Pointer(dataKursors))
	var arp ArpZiņojums = ArpZiņojums{}
	arp.Init(arpbuffer)

	if arp.aparatūraTips == 0x0100 {

		if arp.protocol == 0x0008 && arp.aparatūraaddressIzmērs == 6 && arp.protocoladdressIzmērs == 4 && uint64(arp.mērķisipaddress) == handler.Getipaddress() {

			arpconsole.MDrukāt([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Drukāt(arp.protocol)
			arpconsole.MDrukāt([]byte(":"))
			arpconsole.MUnsignedinteger64Drukāt(uint64(arp.mērķismacaddress))
			arpconsole.MDrukāt([]byte(":"))
			arpconsole.MUnsignedinteger16Drukāt(arp.komanda)
			arpconsole.MDrukāt([]byte(":"))
			arpconsole.MUnsignedinteger64Drukāt(handler.Getmacaddress())

			switch arp.komanda {
			case 0x0100:

				if pats.Getmacfromcache(arp.avotsipaddress) == 0xFFFFFFFFFFFF {
					if pats.skaitliscacheieraksts < 128 {
						pats.Ipcache[pats.skaitliscacheieraksts] = arp.avotsipaddress
						pats.Maccache[pats.skaitliscacheieraksts] = arp.avotsmacaddress
						pats.skaitliscacheieraksts++
					}
				}
				arp.komanda = 0x0200
				arp.mērķisipaddress = arp.avotsipaddress
				arp.mērķismacaddress = arp.avotsmacaddress
				arp.avotsipaddress = uint32(handler.Getipaddress())
				arp.avotsmacaddress = handler.Getmacaddress()
				arp.Kopabuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MDrukāt(([]byte)("self.numCacheEntries"))

				if pats.skaitliscacheieraksts < 128 {
					pats.Ipcache[pats.skaitliscacheieraksts] = arp.avotsipaddress
					pats.Maccache[pats.skaitliscacheieraksts] = arp.avotsmacaddress
					pats.skaitliscacheieraksts++
				}
				break
			}

		}
	}
	return false

}

func (pats *Arpprovider) Broadcastmacaddress(IpTīklsbyteorder uint32) {

	var arp ArpZiņojums = ArpZiņojums{}
	arp.aparatūraTips = 0x0100
	arp.protocol = 0x0008
	arp.aparatūraaddressIzmērs = 6
	arp.protocoladdressIzmērs = 4
	arp.komanda = 0x0200

	arp.avotsipaddress = uint32(handler.Getipaddress())

	arp.mērķismacaddress = pats.Resolve(IpTīklsbyteorder)
	arp.mērķisipaddress = IpTīklsbyteorder
	arpconsole.MDrukātxy([]byte("broad mac"), 0, 15)

	arp.avotsmacaddress = handler.Getmacaddress()

	var arpbuffer ArpZiņojumsbuffer = ArpZiņojumsbuffer{}
	arp.Kopabuffer(&arpbuffer)

	var kursors uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sūtīt(arp.mērķismacaddress, kursors, arpmesgIzmērs)
}
func (pats *Arpprovider) Requestmacaddress(IpTīklsbyteorder uint32) {

	var arp ArpZiņojums = ArpZiņojums{}
	arp.aparatūraTips = 0x0100

	arp.protocol = 0x0008
	arp.aparatūraaddressIzmērs = 6
	arp.protocoladdressIzmērs = 4
	arp.komanda = 0x0100

	arp.avotsmacaddress = handler.Getmacaddress()
	arp.avotsipaddress = uint32(handler.Getipaddress())

	arp.mērķismacaddress = 0xFFFFFFFFFFFF
	arp.mērķisipaddress = IpTīklsbyteorder

	var arpbuffer ArpZiņojumsbuffer = ArpZiņojumsbuffer{}
	arp.Kopabuffer(&arpbuffer)

	var kursors uintptr = uintptr(Pointer(&arpbuffer))
	handler.Sūtīt(arp.mērķismacaddress, kursors, arpmesgIzmērs)
}
func (pats *Arpprovider) PārbaudītDrukāt(data *[]byte, izmērs uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MDrukātxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalDrukāt(buffer_2[i])
		arpconsole.MDrukāt([]byte(":"))
	}
	arpconsole.MDrukāt([]byte("]"))
}

func (pats *Arpprovider) Getmacfromcache(IpTīklsbyteorder uint32) uint64 {
	for i := 0; i < pats.skaitliscacheieraksts; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MDrukāt(([]byte)("["))
		arpconsole.MUnsignedinteger32Drukāt(pats.Ipcache[i])
		arpconsole.MDrukāt(([]byte)(":"))
		arpconsole.MUnsignedinteger32Drukāt(IpTīklsbyteorder)
		arpconsole.MDrukāt(([]byte)(":"))
		arpconsole.MDrukāt(([]byte)(":"))
		arpconsole.MUnsignedinteger64Drukāt(pats.Maccache[i])
		arpconsole.MDrukāt(([]byte)("]\n"))

		if pats.Ipcache[i] == IpTīklsbyteorder {
			arpconsole.MDrukāt([]byte("getmacfromcache"))
			return pats.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (pats *Arpprovider) Resolve(IpTīklsbyteorder uint32) uint64 {
	var result uint64 = pats.Getmacfromcache(IpTīklsbyteorder)
	if result == 0xFFFFFFFFFFFF {
		pats.Requestmacaddress(IpTīklsbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = pats.Getmacfromcache(IpTīklsbyteorder)

	}

	return result
}
