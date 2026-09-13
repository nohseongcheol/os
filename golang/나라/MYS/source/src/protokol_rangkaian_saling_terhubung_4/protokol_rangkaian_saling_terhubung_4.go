package protokol_rangkaian_saling_terhubung_4

import . "unsafe"
import . "util"
import . "console"
import . "bingkai_rangkaian_medium_bersama"
import . "arp"

var ipconsole TConsole = TConsole{}

type TInternetprotocolv4mesejbuffer struct {
	lenver		byte
	tos		byte
	jumlahJarak	[2]byte

	ident			[2]byte
	benderaandoffset	[2]byte

	masatolive	byte
	protocol	byte
	checksum	[2]byte

	sumberipaddress		[4]byte
	destinationipaddress	[4]byte
}

var ipSaiz uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4mesej struct {
	headerJarak	uint8
	versi		uint8
	tos		uint8
	jumlahJarak	uint16

	ident			uint16
	benderaandoffset	uint16

	masatolive	uint8
	protocol	uint8
	checksum	uint16

	sumberipaddress		uint32
	destinationipaddress	uint32
}

func (diri *TInternetprotocolv4mesej) Init(buffer_2 TInternetprotocolv4mesejbuffer) {

	diri.versi = ((buffer_2.lenver & 0xF0) >> 4)
	diri.headerJarak = buffer_2.lenver & 0x0F
	diri.tos = buffer_2.tos
	diri.jumlahJarak = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.jumlahJarak))

	diri.ident = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.ident))
	diri.benderaandoffset = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.benderaandoffset))

	diri.masatolive = buffer_2.masatolive
	diri.protocol = buffer_2.protocol
	diri.checksum = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.checksum))

	diri.sumberipaddress = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer_2.sumberipaddress))
	diri.destinationipaddress = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer_2.destinationipaddress))

}
func (diri *TInternetprotocolv4mesej) Tetapkanbuffer(buffer_2 *TInternetprotocolv4mesejbuffer) {

	buffer_2.lenver = byte(((diri.versi & 0x0F) << 4) | (diri.headerJarak & 0x0F))
	buffer_2.tos = diri.tos
	buffer_2.jumlahJarak = Unsignedinteger16toTatasusunan(diri.jumlahJarak)

	buffer_2.ident = Unsignedinteger16toTatasusunan(diri.ident)
	buffer_2.benderaandoffset = Unsignedinteger16toTatasusunan(diri.benderaandoffset)

	buffer_2.masatolive = diri.masatolive
	buffer_2.protocol = diri.protocol
	buffer_2.checksum = Unsignedinteger16toTatasusunan(diri.checksum)

	buffer_2.sumberipaddress = Unsignedinteger32toTatasusunan(diri.sumberipaddress)
	buffer_2.destinationipaddress = Unsignedinteger32toTatasusunan(diri.destinationipaddress)

}

type IInternetprotocolhandler interface {
	Init(backend TPembekal_protokol_rangkaian_saling_terhubung, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder uint32, destinationipaddressRangkaianbyteorder uint32, dataPenuding uintptr, saiz uint32) bool
	Hantar(destinationipaddressRangkaianbyteorder uint32, pprotocol uint8, dataPenuding uintptr, saiz uint32)
	Providerget() *TPembekal_protokol_rangkaian_saling_terhubung
}

type TInternetprotocolhandler struct {
}

var ipEternetBingkaihandler IpEternetBingkaihandler = IpEternetBingkaihandler{}
var protocol uint8

func (diri *TInternetprotocolhandler) Init(backend TPembekal_protokol_rangkaian_saling_terhubung, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (diri *TInternetprotocolhandler) Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder uint32, destinationipaddressRangkaianbyteorder uint32, dataPenuding uintptr, saiz uint32) bool {
	ipconsole.MCetak(([]byte)("ipHandler:OnInternet"))
	return false
}
func (diri *TInternetprotocolhandler) Hantar(destinationipaddressRangkaianbyteorder uint32, pprotocol uint8, dataPenuding uintptr, saiz uint32) {

	pembekal_protokol_rangkaian_saling_terhubung.Hantar(destinationipaddressRangkaianbyteorder, pprotocol, dataPenuding, saiz)
}
func (diri *TInternetprotocolhandler) Providerget() *TPembekal_protokol_rangkaian_saling_terhubung {
	return &pembekal_protokol_rangkaian_saling_terhubung
}

type IpEternetBingkaihandler struct {
	TEternetBingkaihandler
}

var pembekal_protokol_rangkaian_saling_terhubung TPembekal_protokol_rangkaian_saling_terhubung

func (diri *IpEternetBingkaihandler) EternetBingkaireceivewhen(dataPenuding uintptr, saiz int) bool {
	ipconsole.MCetak(([]byte)("iphandler:onEtherfameRecv\n"))
	return pembekal_protokol_rangkaian_saling_terhubung.EternetBingkaireceivewhen(dataPenuding, uint32(saiz))

}

func (diri *IpEternetBingkaihandler) Hantar(destinationipaddressRangkaianbyteorder uint64, dataPenuding uintptr, saiz uint32) {
	ipconsole.MCetak(([]byte)("ipefhandler:send\n"))
	var eternetJenisbe = Unsignedinteger16r(0x0800)
	diri.TEternetBingkaihandler.BingkaiHantar(destinationipaddressRangkaianbyteorder, eternetJenisbe, dataPenuding, saiz)

}

var handler_2 [255]IInternetprotocolhandler

type TPembekal_protokol_rangkaian_saling_terhubung struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	Subnetmask	uint32
}

var efhandler IEternetBingkaihandler

func (diri *TPembekal_protokol_rangkaian_saling_terhubung) Init(pefprovider TPembekal_bingkai_rangkaian_medium_bersama, pefhandler IEternetBingkaihandler, arp Arpprovider, gatewayip uint32, subnetmask uint32) {

	efhandler = pefhandler
	efhandler.Tetapkanhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	diri.arpprovider = arp
	diri.Gatewayip = gatewayip
	diri.Subnetmask = subnetmask
	pembekal_protokol_rangkaian_saling_terhubung = *diri
}
func (diri *TPembekal_protokol_rangkaian_saling_terhubung) EternetBingkaireceivewhen(eternetBingkaipayload uintptr, saiz uint32) bool {
	if saiz < uint32(ipSaiz) {
		return false
	}

	var buffer_2 *TInternetprotocolv4mesejbuffer = (*TInternetprotocolv4mesejbuffer)(Pointer(eternetBingkaipayload))
	var internetprotocolmesej TInternetprotocolv4mesej
	internetprotocolmesej.Init(*buffer_2)

	var reply bool = false

	if internetprotocolmesej.destinationipaddress == uint32(efhandler.Getipaddress()) {

		var jarak uint32 = uint32(internetprotocolmesej.jumlahJarak)
		if jarak > saiz {
			jarak = saiz
		}
		if handler_2[internetprotocolmesej.protocol] != nil {
			reply = handler_2[internetprotocolmesej.protocol].Internetprotocolreceivewhen(internetprotocolmesej.sumberipaddress, internetprotocolmesej.destinationipaddress, eternetBingkaipayload+uintptr(4*internetprotocolmesej.headerJarak), uint32(jarak-uint32(4*internetprotocolmesej.headerJarak)))

		}
	}

	if reply {

		var temporary = internetprotocolmesej.destinationipaddress
		internetprotocolmesej.destinationipaddress = internetprotocolmesej.sumberipaddress
		internetprotocolmesej.sumberipaddress = temporary

		internetprotocolmesej.masatolive = 0x40
		internetprotocolmesej.checksum = 0

		internetprotocolmesej.Tetapkanbuffer(buffer_2)
		internetprotocolmesej.checksum = diri.Checksum((*([4096]uint16))(Pointer(eternetBingkaipayload)), uint32(4*internetprotocolmesej.headerJarak))

		internetprotocolmesej.Tetapkanbuffer(buffer_2)

	}

	ipconsole.MCetak(([]byte)("ipmessage"))
	ipconsole.MUnsignedinteger32Cetak(internetprotocolmesej.sumberipaddress)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger32Cetak(internetprotocolmesej.destinationipaddress)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(uint16(internetprotocolmesej.headerJarak))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(uint16(internetprotocolmesej.versi))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger16Cetak(internetprotocolmesej.jumlahJarak)
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MUnsignedinteger32Cetak(uint32(efhandler.Getipaddress()))
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MCetak(([]byte)("\n"))

	return reply

}
func (diri *TPembekal_protokol_rangkaian_saling_terhubung) Hantar(destinationipaddressRangkaianbyteorder uint32, protocol uint8, dataPenuding uintptr, saiz uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4mesejbuffer = (*TInternetprotocolv4mesejbuffer)(Pointer(&buffer1_2))
	var mesej TInternetprotocolv4mesej = TInternetprotocolv4mesej{}
	mesej.versi = 4
	mesej.headerJarak = ipSaiz / 4
	mesej.tos = 0
	mesej.jumlahJarak = Unsignedinteger16r(uint16(saiz + uint32(ipSaiz)))

	mesej.ident = 0x0100
	mesej.benderaandoffset = 0x0040
	mesej.masatolive = 0x40
	mesej.protocol = protocol

	mesej.destinationipaddress = destinationipaddressRangkaianbyteorder

	mesej.sumberipaddress = uint32(efhandler.Getipaddress())

	mesej.checksum = 0

	mesej.Tetapkanbuffer(buffer_2)
	mesej.checksum = diri.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipSaiz))
	mesej.Tetapkanbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataPenuding))

	for i := 0; i < int(saiz); i++ {

		buffer1_2[i+int(ipSaiz)] = databuffer_2[i]
	}

	ipconsole.MCetakxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(saiz)+int(ipSaiz); i++ {
		ipconsole.MHexadecimalCetak(buffer1_2[i])
	}
	ipconsole.MCetak(([]byte)(":"))
	ipconsole.MCetak(([]byte)("]\n"))

	var berikutnyahopipaddressRangkaianbyteorder uint32 = destinationipaddressRangkaianbyteorder
	if (destinationipaddressRangkaianbyteorder & diri.Subnetmask) != (mesej.sumberipaddress & diri.Subnetmask) {
		berikutnyahopipaddressRangkaianbyteorder = diri.Gatewayip
	}

	var hantardataPenuding = uintptr(Pointer(&buffer1_2))
	ipconsole.MUnsignedinteger32Cetak(berikutnyahopipaddressRangkaianbyteorder)

	var eternetJenisbe = Unsignedinteger16r(0x0800)
	efhandler.BingkaiHantar(diri.arpprovider.Resolve(berikutnyahopipaddressRangkaianbyteorder), eternetJenisbe, hantardataPenuding, uint32(ipSaiz)+uint32(saiz))

}
func (diri *TPembekal_protokol_rangkaian_saling_terhubung) Checksum(pdata *[4096]uint16, jarakMasukBait uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBait [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (jarakMasukBait % 2) != 0 {
		temporary += uint32(uint16(dataBait[jarakMasukBait-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (diri *TPembekal_protokol_rangkaian_saling_terhubung) Getipaddress() uint64 {
	return efhandler.Getipaddress()
}
