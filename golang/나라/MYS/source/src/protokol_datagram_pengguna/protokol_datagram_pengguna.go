package protokol_datagram_pengguna

import . "unsafe"
import . "console"
import . "util"
import . "ingatanmanager"
import . "protokol_rangkaian_saling_terhubung_4"

var udpconsole = TConsole{}

type TPenggunadatagramprotocolheaderbuffer struct {
	nombor_port_sumber	[2]byte
	nombor_port_destinasi	[2]byte

	jarak		[2]byte
	checksum	[2]byte
}

var udpheaderSaiz uint32 = 8

type TPengepala_datagram_pengguna struct {
	nombor_port_sumber	uint16
	nombor_port_destinasi	uint16

	jarak		uint16
	checksum	uint16
}

func (diri *TPengepala_datagram_pengguna) Init(buffer_2 *TPenggunadatagramprotocolheaderbuffer) {
	diri.nombor_port_sumber = Tatasusunantounsignedinteger16(buffer_2.nombor_port_sumber)
	diri.nombor_port_destinasi = Tatasusunantounsignedinteger16(buffer_2.nombor_port_destinasi)

	diri.jarak = Tatasusunantounsignedinteger16(buffer_2.jarak)
	diri.checksum = Tatasusunantounsignedinteger16(buffer_2.checksum)
}
func (diri *TPengepala_datagram_pengguna) Tetapkanbuffer(buffer_2 *TPenggunadatagramprotocolheaderbuffer) {

	buffer_2.nombor_port_sumber = Unsignedinteger16toTatasusunan(diri.nombor_port_sumber)
	buffer_2.nombor_port_destinasi = Unsignedinteger16toTatasusunan(diri.nombor_port_destinasi)

	buffer_2.jarak = Unsignedinteger16toTatasusunan(diri.jarak)
	buffer_2.checksum = Unsignedinteger16toTatasusunan(diri.checksum)

}

type IPenggunadatagramprotocolhandler interface {
	KendaliPenggunadatagramprotocolmesej(soket *TTitik_akhir_datagram_pengguna, data uintptr, saiz uint16)
}

type TPenggunadatagramprotocolhandler struct {
}

func (diri *TPenggunadatagramprotocolhandler) Init(backend TPembekal_protokol_rangkaian_saling_terhubung) {
}
func (diri *TPenggunadatagramprotocolhandler) KendaliPenggunadatagramprotocolmesej(soket *TTitik_akhir_datagram_pengguna, data uintptr, saiz uint16) {
}

type IPenggunadatagramprotocolSoket interface {
	KendaliPenggunadatagramprotocolmesej(data uintptr, saiz uint16)
}
type TTitik_akhir_datagram_pengguna struct {
	remoteportNOMBOR	uint16
	remoteip		uint32
	setempatportNOMBOR	uint16
	setempatip		uint32

	listening	bool
}

var udpprovider TPenggunadatagramprotocolprovider
var udphandler IPenggunadatagramprotocolhandler

func (diri *TTitik_akhir_datagram_pengguna) Uji() {
}
func (diri *TTitik_akhir_datagram_pengguna) Init(pudpprovider TPenggunadatagramprotocolprovider, pudphandler IPenggunadatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	diri.listening = false
}
func (diri *TTitik_akhir_datagram_pengguna) KendaliPenggunadatagramprotocolmesej(data uintptr, saiz uint16) {
	if udphandler != nil {
		udphandler.KendaliPenggunadatagramprotocolmesej(diri, data, saiz)
	}
}
func (diri *TTitik_akhir_datagram_pengguna) Hantar(pdata []byte, saiz uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(saiz); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Hantar(diri, data, saiz)
}
func (diri *TTitik_akhir_datagram_pengguna) Putus() {
	udpprovider.Putus(diri)
}

type TPenggunadatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TTitik_akhir_datagram_pengguna
var nOMBORsockets int
var bebasport uint16

func (diri *TPenggunadatagramprotocolprovider) Init(pipprovider TPembekal_protokol_rangkaian_saling_terhubung, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nOMBORsockets = 0
	bebasport = 1024
}
func (diri *TPenggunadatagramprotocolprovider) Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder uint32, destinationipaddressRangkaianbyteorder uint32, internetprotocolpayload uintptr, saiz uint32) bool {
	if saiz < udpheaderSaiz {
		return false
	}

	var buffer_2 *TPenggunadatagramprotocolheaderbuffer = (*TPenggunadatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TPengepala_datagram_pengguna
	msg.Init(buffer_2)

	var soket *TTitik_akhir_datagram_pengguna = nil

	for i := 0; i < nOMBORsockets && soket == nil; i++ {
		if sockets[i].setempatportNOMBOR == msg.nombor_port_destinasi && sockets[i].setempatip == destinationipaddressRangkaianbyteorder && sockets[i].listening == true {
			soket = &sockets[i]
			soket.listening = false
			soket.remoteportNOMBOR = msg.nombor_port_sumber
			soket.remoteip = sumberipaddressRangkaianbyteorder
		} else if sockets[i].setempatportNOMBOR == msg.nombor_port_destinasi && sockets[i].setempatip == destinationipaddressRangkaianbyteorder && sockets[i].remoteportNOMBOR == msg.nombor_port_sumber && sockets[i].remoteip == sumberipaddressRangkaianbyteorder {
			soket = &sockets[i]

		}
	}

	msg.Tetapkanbuffer(buffer_2)
	if soket != nil {
		soket.KendaliPenggunadatagramprotocolmesej(internetprotocolpayload+uintptr(udpheaderSaiz), uint16(saiz-udpheaderSaiz))
	}

	return false
}

func (diri *TPenggunadatagramprotocolprovider) Sambung(ip uint32, port uint16) *TTitik_akhir_datagram_pengguna {
	var ingatanmanager = &TIngatanmanager{}
	var soket = (*TTitik_akhir_datagram_pengguna)(ingatanmanager.Peruntukkan_ingatan(50))

	if soket != nil {

		soket.Init(*diri, nil)
		soket.remoteportNOMBOR = port
		soket.remoteip = ip
		soket.setempatportNOMBOR = bebasport
		bebasport++
		soket.setempatip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.remoteportNOMBOR = Unsignedinteger16r(soket.remoteportNOMBOR)
		soket.setempatportNOMBOR = Unsignedinteger16r(soket.setempatportNOMBOR)

		sockets[nOMBORsockets] = *soket
		nOMBORsockets++

	}
	return soket

}
func (diri *TPenggunadatagramprotocolprovider) Listen(port uint16) *TTitik_akhir_datagram_pengguna {
	var soket = &TTitik_akhir_datagram_pengguna{}
	soket = nil
	if soket != nil {
		soket.Init(*diri, nil)
		soket.listening = true
		soket.setempatportNOMBOR = port
		soket.setempatip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.setempatportNOMBOR = Unsignedinteger16r(soket.setempatportNOMBOR)
	}
	return soket
}
func (diri *TPenggunadatagramprotocolprovider) Putus(soket *TTitik_akhir_datagram_pengguna) {
	for i := 0; i < nOMBORsockets && soket == nil; i++ {
		if sockets[i] == *soket {
			nOMBORsockets--
			sockets[i] = sockets[nOMBORsockets]
			break
		}
	}
}
func (diri *TPenggunadatagramprotocolprovider) Hantar(soket *TTitik_akhir_datagram_pengguna, pdata uintptr, saiz uint16) {
	var jumlahJarak = uint32(saiz) + udpheaderSaiz

	var buffer_2 [4096]byte

	var msgbuffer = (*TPenggunadatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TPengepala_datagram_pengguna{}

	msg.nombor_port_sumber = soket.setempatportNOMBOR
	msg.nombor_port_destinasi = soket.remoteportNOMBOR
	msg.jarak = Unsignedinteger16r(uint16(jumlahJarak))

	msg.checksum = 0x0
	msg.Tetapkanbuffer(msgbuffer)

	var dataBait [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(saiz); i++ {
		buffer_2[int(udpheaderSaiz)+i] = dataBait[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Hantar(soket.remoteip, 0x11, data, jumlahJarak)

}
func (diri *TPenggunadatagramprotocolprovider) Bind(soket *TTitik_akhir_datagram_pengguna, handler *TPenggunadatagramprotocolhandler) {
}
