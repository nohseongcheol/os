package arp

import . "unsafe"
import . "konzola"
import . "žičanavezaOkvir"
import . "util"

var arpKonzola TKonzola = TKonzola{}

type Arpporukabuffer struct {
	hardverVrsta		[2]byte
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

type Arpporuka struct {
	hardverVrsta		uint16
	protocol		uint16
	hardveraddressVeličina	uint8
	protocoladdressVeličina	uint8
	naredba			uint16

	izvormacaddress		uint64
	izvoripaddress		uint32
	odredištemacaddress	uint64
	odredišteipaddress	uint32
}

func (isti *Arpporuka) Init(buffer_2 *Arpporukabuffer) {

	isti.hardverVrsta = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.hardverVrsta))
	isti.protocol = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.protocol))
	isti.hardveraddressVeličina = byte(buffer_2.hardveraddressVeličina)
	isti.protocoladdressVeličina = byte(buffer_2.protocoladdressVeličina)
	isti.naredba = Unsignedinteger16r(Niztounsignedinteger16(buffer_2.naredba))

	isti.izvormacaddress = Unsignedinteger48r(Niztounsignedinteger48(buffer_2.izvormacaddress))
	isti.izvoripaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.izvoripaddress))
	isti.odredištemacaddress = Unsignedinteger48r(Niztounsignedinteger48(buffer_2.odredištemacaddress))
	isti.odredišteipaddress = Unsignedinteger32r(Niztounsignedinteger32(buffer_2.odredišteipaddress))
}
func (isti *Arpporuka) Skupbuffer(buffer_2 *Arpporukabuffer) {
	buffer_2.hardverVrsta = Unsignedinteger16toNiz(isti.hardverVrsta)
	buffer_2.protocol = Unsignedinteger16toNiz(isti.protocol)
	buffer_2.hardveraddressVeličina = uint8(isti.hardveraddressVeličina)
	buffer_2.protocoladdressVeličina = uint8(isti.protocoladdressVeličina)

	buffer_2.naredba = Unsignedinteger16toNiz(isti.naredba)
	buffer_2.izvormacaddress = Unsignedinteger48toNiz(isti.izvormacaddress)
	buffer_2.izvoripaddress = Unsignedinteger32toNiz(isti.izvoripaddress)
	buffer_2.odredištemacaddress = Unsignedinteger48toNiz(isti.odredištemacaddress)
	buffer_2.odredišteipaddress = Unsignedinteger32toNiz(isti.odredišteipaddress)
}

type ArpŽičanavezaOkvirhandler struct {
	TŽičanavezaOkvirhandler
}

var arpprovider Arpprovider
var žičanavezaOkvirprovider TŽičanavezaOkvirprovider

func (isti *ArpŽičanavezaOkvirhandler) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, veličina int) bool {
	arpKonzola.MŠtampajxy([]byte("arp recv:"), 0, 23)
	return arpprovider.ŽičanavezaOkvirreceivewhen(dataPokazivač, uint32(veličina))

}
func (isti *ArpŽičanavezaOkvirhandler) Pošalji(odredištemacbe uint64, dataPokazivač uintptr, veličina uint32) {
	arpKonzola.MŠtampajxy([]byte("arp send:"), 0, 24)
	var žičanavezaVrstabe = Unsignedinteger16r(0x0806)
	isti.TŽičanavezaOkvirhandler.OkvirPošalji(odredištemacbe, žičanavezaVrstabe, dataPokazivač, veličina)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	brojcacheunos	int

	handler	IŽičanavezaOkvirhandler
}

var handler IŽičanavezaOkvirhandler

func (isti *Arpprovider) Init(backend TŽičanavezaOkvirprovider, userhandler IŽičanavezaOkvirhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Skuphandler(userhandler, 0x0806)
	isti.brojcacheunos = 0
	arpprovider = *isti

}

func (isti *Arpprovider) ŽičanavezaOkvirreceivewhen(dataPokazivač uintptr, veličina uint32) bool {

	if veličina < arpmesgVeličina {
		return false
	}
	var arpbuffer *Arpporukabuffer = (*Arpporukabuffer)(Pointer(dataPokazivač))
	var arp Arpporuka = Arpporuka{}
	arp.Init(arpbuffer)

	if arp.hardverVrsta == 0x0100 {

		if arp.protocol == 0x0008 && arp.hardveraddressVeličina == 6 && arp.protocoladdressVeličina == 4 && uint64(arp.odredišteipaddress) == handler.Getipaddress() {

			arpKonzola.MŠtampaj([]byte("arp onetherframe"))
			arpKonzola.MUnsignedinteger16Štampaj(arp.protocol)
			arpKonzola.MŠtampaj([]byte(":"))
			arpKonzola.MUnsignedinteger64Štampaj(uint64(arp.odredištemacaddress))
			arpKonzola.MŠtampaj([]byte(":"))
			arpKonzola.MUnsignedinteger16Štampaj(arp.naredba)
			arpKonzola.MŠtampaj([]byte(":"))
			arpKonzola.MUnsignedinteger64Štampaj(handler.Getmacaddress())

			switch arp.naredba {
			case 0x0100:

				if isti.Getmacsacache(arp.izvoripaddress) == 0xFFFFFFFFFFFF {
					if isti.brojcacheunos < 128 {
						isti.Ipcache[isti.brojcacheunos] = arp.izvoripaddress
						isti.Maccache[isti.brojcacheunos] = arp.izvormacaddress
						isti.brojcacheunos++
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
				arpKonzola.MŠtampaj(([]byte)("self.numCacheEntries"))

				if isti.brojcacheunos < 128 {
					isti.Ipcache[isti.brojcacheunos] = arp.izvoripaddress
					isti.Maccache[isti.brojcacheunos] = arp.izvormacaddress
					isti.brojcacheunos++
				}
				break
			}

		}
	}
	return false

}

func (isti *Arpprovider) Broadcastmacaddress(IpMrežabyteorder uint32) {

	var arp Arpporuka = Arpporuka{}
	arp.hardverVrsta = 0x0100
	arp.protocol = 0x0008
	arp.hardveraddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0200

	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = isti.Resolve(IpMrežabyteorder)
	arp.odredišteipaddress = IpMrežabyteorder
	arpKonzola.MŠtampajxy([]byte("broad mac"), 0, 15)

	arp.izvormacaddress = handler.Getmacaddress()

	var arpbuffer Arpporukabuffer = Arpporukabuffer{}
	arp.Skupbuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pokazivač, arpmesgVeličina)
}
func (isti *Arpprovider) Requestmacaddress(IpMrežabyteorder uint32) {

	var arp Arpporuka = Arpporuka{}
	arp.hardverVrsta = 0x0100

	arp.protocol = 0x0008
	arp.hardveraddressVeličina = 6
	arp.protocoladdressVeličina = 4
	arp.naredba = 0x0100

	arp.izvormacaddress = handler.Getmacaddress()
	arp.izvoripaddress = uint32(handler.Getipaddress())

	arp.odredištemacaddress = 0xFFFFFFFFFFFF
	arp.odredišteipaddress = IpMrežabyteorder

	var arpbuffer Arpporukabuffer = Arpporukabuffer{}
	arp.Skupbuffer(&arpbuffer)

	var pokazivač uintptr = uintptr(Pointer(&arpbuffer))
	handler.Pošalji(arp.odredištemacaddress, pokazivač, arpmesgVeličina)
}
func (isti *Arpprovider) TestŠtampaj(data *[]byte, veličina uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpKonzola.MŠtampajxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpKonzola.MHexadecimalŠtampaj(buffer_2[i])
		arpKonzola.MŠtampaj([]byte(":"))
	}
	arpKonzola.MŠtampaj([]byte("]"))
}

func (isti *Arpprovider) Getmacsacache(IpMrežabyteorder uint32) uint64 {
	for i := 0; i < isti.brojcacheunos; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpKonzola.MŠtampaj(([]byte)("["))
		arpKonzola.MUnsignedinteger32Štampaj(isti.Ipcache[i])
		arpKonzola.MŠtampaj(([]byte)(":"))
		arpKonzola.MUnsignedinteger32Štampaj(IpMrežabyteorder)
		arpKonzola.MŠtampaj(([]byte)(":"))
		arpKonzola.MŠtampaj(([]byte)(":"))
		arpKonzola.MUnsignedinteger64Štampaj(isti.Maccache[i])
		arpKonzola.MŠtampaj(([]byte)("]\n"))

		if isti.Ipcache[i] == IpMrežabyteorder {
			arpKonzola.MŠtampaj([]byte("getmacfromcache"))
			return isti.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (isti *Arpprovider) Resolve(IpMrežabyteorder uint32) uint64 {
	var iSHOD uint64 = isti.Getmacsacache(IpMrežabyteorder)
	if iSHOD == 0xFFFFFFFFFFFF {
		isti.Requestmacaddress(IpMrežabyteorder)
	}
	for i := 0; i < 128 && iSHOD == 0xFFFFFFFFFFFF; i++ {
		iSHOD = isti.Getmacsacache(IpMrežabyteorder)

	}

	return iSHOD
}
