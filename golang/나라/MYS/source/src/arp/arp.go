package arp

import . "unsafe"
import . "console"
import . "bingkai_rangkaian_medium_bersama"
import . "util"

var arpconsole TConsole = TConsole{}

type Arpmesejbuffer struct {
	perkakasanJenis		[2]byte
	protocol		[2]byte
	perkakasanaddressSaiz	byte
	protocoladdressSaiz	byte
	perintah		[2]byte

	sumbermacaddress	[6]byte
	sumberipaddress		[4]byte
	destinationmacaddress	[6]byte
	destinationipaddress	[4]byte
}

var arpmesgSaiz uint32 = (64+92+64)/8 + 2

type Arpmesej struct {
	perkakasanJenis		uint16
	protocol		uint16
	perkakasanaddressSaiz	uint8
	protocoladdressSaiz	uint8
	perintah		uint16

	sumbermacaddress	uint64
	sumberipaddress		uint32
	destinationmacaddress	uint64
	destinationipaddress	uint32
}

func (diri *Arpmesej) Init(buffer_2 *Arpmesejbuffer) {

	diri.perkakasanJenis = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.perkakasanJenis))
	diri.protocol = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.protocol))
	diri.perkakasanaddressSaiz = byte(buffer_2.perkakasanaddressSaiz)
	diri.protocoladdressSaiz = byte(buffer_2.protocoladdressSaiz)
	diri.perintah = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.perintah))

	diri.sumbermacaddress = Unsignedinteger48r(Tatasusunantounsignedinteger48(buffer_2.sumbermacaddress))
	diri.sumberipaddress = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer_2.sumberipaddress))
	diri.destinationmacaddress = Unsignedinteger48r(Tatasusunantounsignedinteger48(buffer_2.destinationmacaddress))
	diri.destinationipaddress = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer_2.destinationipaddress))
}
func (diri *Arpmesej) Tetapkanbuffer(buffer_2 *Arpmesejbuffer) {
	buffer_2.perkakasanJenis = Unsignedinteger16toTatasusunan(diri.perkakasanJenis)
	buffer_2.protocol = Unsignedinteger16toTatasusunan(diri.protocol)
	buffer_2.perkakasanaddressSaiz = uint8(diri.perkakasanaddressSaiz)
	buffer_2.protocoladdressSaiz = uint8(diri.protocoladdressSaiz)

	buffer_2.perintah = Unsignedinteger16toTatasusunan(diri.perintah)
	buffer_2.sumbermacaddress = Unsignedinteger48toTatasusunan(diri.sumbermacaddress)
	buffer_2.sumberipaddress = Unsignedinteger32toTatasusunan(diri.sumberipaddress)
	buffer_2.destinationmacaddress = Unsignedinteger48toTatasusunan(diri.destinationmacaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toTatasusunan(diri.destinationipaddress)
}

type ArpEternetBingkaihandler struct {
	TEternetBingkaihandler
}

var arpprovider Arpprovider
var pembekal_bingkai_rangkaian_medium_bersama TPembekal_bingkai_rangkaian_medium_bersama

func (diri *ArpEternetBingkaihandler) EternetBingkaireceivewhen(dataPenuding uintptr, saiz int) bool {
	arpconsole.MCetakxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EternetBingkaireceivewhen(dataPenuding, uint32(saiz))

}
func (diri *ArpEternetBingkaihandler) Hantar(destinationmacbe uint64, dataPenuding uintptr, saiz uint32) {
	arpconsole.MCetakxy([]byte("arp send:"), 0, 24)
	var eternetJenisbe = Unsignedinteger16r(0x0806)
	diri.TEternetBingkaihandler.BingkaiHantar(destinationmacbe, eternetJenisbe, dataPenuding, saiz)
}

type Arpprovider struct {
	Ipcache			[128]uint32
	Maccache		[128]uint64
	nOMBORcacheentry	int

	handler	IEternetBingkaihandler
}

var handler IEternetBingkaihandler

func (diri *Arpprovider) Init(backend TPembekal_bingkai_rangkaian_medium_bersama, userhandler IEternetBingkaihandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Tetapkanhandler(userhandler, 0x0806)
	diri.nOMBORcacheentry = 0
	arpprovider = *diri

}

func (diri *Arpprovider) EternetBingkaireceivewhen(dataPenuding uintptr, saiz uint32) bool {

	if saiz < arpmesgSaiz {
		return false
	}
	var arpbuffer *Arpmesejbuffer = (*Arpmesejbuffer)(Pointer(dataPenuding))
	var arp Arpmesej = Arpmesej{}
	arp.Init(arpbuffer)

	if arp.perkakasanJenis == 0x0100 {

		if arp.protocol == 0x0008 && arp.perkakasanaddressSaiz == 6 && arp.protocoladdressSaiz == 4 && uint64(arp.destinationipaddress) == handler.Getipaddress() {

			arpconsole.MCetak([]byte("arp onetherframe"))
			arpconsole.MUnsignedinteger16Cetak(arp.protocol)
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger64Cetak(uint64(arp.destinationmacaddress))
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger16Cetak(arp.perintah)
			arpconsole.MCetak([]byte(":"))
			arpconsole.MUnsignedinteger64Cetak(handler.Getmacaddress())

			switch arp.perintah {
			case 0x0100:

				if diri.Getmacfromcache(arp.sumberipaddress) == 0xFFFFFFFFFFFF {
					if diri.nOMBORcacheentry < 128 {
						diri.Ipcache[diri.nOMBORcacheentry] = arp.sumberipaddress
						diri.Maccache[diri.nOMBORcacheentry] = arp.sumbermacaddress
						diri.nOMBORcacheentry++
					}
				}
				arp.perintah = 0x0200
				arp.destinationipaddress = arp.sumberipaddress
				arp.destinationmacaddress = arp.sumbermacaddress
				arp.sumberipaddress = uint32(handler.Getipaddress())
				arp.sumbermacaddress = handler.Getmacaddress()
				arp.Tetapkanbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpconsole.MCetak(([]byte)("self.numCacheEntries"))

				if diri.nOMBORcacheentry < 128 {
					diri.Ipcache[diri.nOMBORcacheentry] = arp.sumberipaddress
					diri.Maccache[diri.nOMBORcacheentry] = arp.sumbermacaddress
					diri.nOMBORcacheentry++
				}
				break
			}

		}
	}
	return false

}

func (diri *Arpprovider) Broadcastmacaddress(IpRangkaianbyteorder uint32) {

	var arp Arpmesej = Arpmesej{}
	arp.perkakasanJenis = 0x0100
	arp.protocol = 0x0008
	arp.perkakasanaddressSaiz = 6
	arp.protocoladdressSaiz = 4
	arp.perintah = 0x0200

	arp.sumberipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = diri.Resolve(IpRangkaianbyteorder)
	arp.destinationipaddress = IpRangkaianbyteorder
	arpconsole.MCetakxy([]byte("broad mac"), 0, 15)

	arp.sumbermacaddress = handler.Getmacaddress()

	var arpbuffer Arpmesejbuffer = Arpmesejbuffer{}
	arp.Tetapkanbuffer(&arpbuffer)

	var rujukan_alamat uintptr = uintptr(Pointer(&arpbuffer))
	handler.Hantar(arp.destinationmacaddress, rujukan_alamat, arpmesgSaiz)
}
func (diri *Arpprovider) Requestmacaddress(IpRangkaianbyteorder uint32) {

	var arp Arpmesej = Arpmesej{}
	arp.perkakasanJenis = 0x0100

	arp.protocol = 0x0008
	arp.perkakasanaddressSaiz = 6
	arp.protocoladdressSaiz = 4
	arp.perintah = 0x0100

	arp.sumbermacaddress = handler.Getmacaddress()
	arp.sumberipaddress = uint32(handler.Getipaddress())

	arp.destinationmacaddress = 0xFFFFFFFFFFFF
	arp.destinationipaddress = IpRangkaianbyteorder

	var arpbuffer Arpmesejbuffer = Arpmesejbuffer{}
	arp.Tetapkanbuffer(&arpbuffer)

	var rujukan_alamat uintptr = uintptr(Pointer(&arpbuffer))
	handler.Hantar(arp.destinationmacaddress, rujukan_alamat, arpmesgSaiz)
}
func (diri *Arpprovider) UjiCetak(data *[]byte, saiz uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpconsole.MCetakxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpconsole.MHexadecimalCetak(buffer_2[i])
		arpconsole.MCetak([]byte(":"))
	}
	arpconsole.MCetak([]byte("]"))
}

func (diri *Arpprovider) Getmacfromcache(IpRangkaianbyteorder uint32) uint64 {
	for i := 0; i < diri.nOMBORcacheentry; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpconsole.MCetak(([]byte)("["))
		arpconsole.MUnsignedinteger32Cetak(diri.Ipcache[i])
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MUnsignedinteger32Cetak(IpRangkaianbyteorder)
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MCetak(([]byte)(":"))
		arpconsole.MUnsignedinteger64Cetak(diri.Maccache[i])
		arpconsole.MCetak(([]byte)("]\n"))

		if diri.Ipcache[i] == IpRangkaianbyteorder {
			arpconsole.MCetak([]byte("getmacfromcache"))
			return diri.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (diri *Arpprovider) Resolve(IpRangkaianbyteorder uint32) uint64 {
	var result uint64 = diri.Getmacfromcache(IpRangkaianbyteorder)
	if result == 0xFFFFFFFFFFFF {
		diri.Requestmacaddress(IpRangkaianbyteorder)
	}
	for i := 0; i < 128 && result == 0xFFFFFFFFFFFF; i++ {
		result = diri.Getmacfromcache(IpRangkaianbyteorder)

	}

	return result
}
