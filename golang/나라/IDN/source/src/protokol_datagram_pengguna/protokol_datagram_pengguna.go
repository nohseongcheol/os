package protokol_datagram_pengguna

import . "unsafe"
import . "console"
import . "util"
import . "memorimanager"
import . "protokol_jaringan_saling_terhubung_4"

var udpconsole = TConsole{}

type TPenggunadatagramprotocolheaderbuffer struct {
	nomor_porta_sumber	[2]byte
	nomor_porta_tujuan	[2]byte

	panjang		[2]byte
	checksum	[2]byte
}

var udpheaderUkuran uint32 = 8

type TKepala_datagram_pengguna struct {
	nomor_porta_sumber	uint16
	nomor_porta_tujuan	uint16

	panjang		uint16
	checksum	uint16
}

func (dirisendiri *TKepala_datagram_pengguna) Init(buffer_2 *TPenggunadatagramprotocolheaderbuffer) {
	dirisendiri.nomor_porta_sumber = Jajarantounsignedinteger16(buffer_2.nomor_porta_sumber)
	dirisendiri.nomor_porta_tujuan = Jajarantounsignedinteger16(buffer_2.nomor_porta_tujuan)

	dirisendiri.panjang = Jajarantounsignedinteger16(buffer_2.panjang)
	dirisendiri.checksum = Jajarantounsignedinteger16(buffer_2.checksum)
}
func (dirisendiri *TKepala_datagram_pengguna) Aturbuffer(buffer_2 *TPenggunadatagramprotocolheaderbuffer) {

	buffer_2.nomor_porta_sumber = Unsignedinteger16toJajaran(dirisendiri.nomor_porta_sumber)
	buffer_2.nomor_porta_tujuan = Unsignedinteger16toJajaran(dirisendiri.nomor_porta_tujuan)

	buffer_2.panjang = Unsignedinteger16toJajaran(dirisendiri.panjang)
	buffer_2.checksum = Unsignedinteger16toJajaran(dirisendiri.checksum)

}

type IPenggunadatagramprotocolhandler interface {
	PenangananPenggunadatagramprotocolPesan(soket *TTitik_akhir_datagram_pengguna, data uintptr, ukuran uint16)
}

type TPenggunadatagramprotocolhandler struct {
}

func (dirisendiri *TPenggunadatagramprotocolhandler) Init(backend TPenyedia_protokol_jaringan_saling_terhubung) {
}
func (dirisendiri *TPenggunadatagramprotocolhandler) PenangananPenggunadatagramprotocolPesan(soket *TTitik_akhir_datagram_pengguna, data uintptr, ukuran uint16) {
}

type IPenggunadatagramprotocolSoket interface {
	PenangananPenggunadatagramprotocolPesan(data uintptr, ukuran uint16)
}
type TTitik_akhir_datagram_pengguna struct {
	jauhportNomor	uint16
	jauhip		uint32
	lokalportNomor	uint16
	lokalip		uint32

	listening	bool
}

var udpprovider TPenggunadatagramprotocolprovider
var udphandler IPenggunadatagramprotocolhandler

func (dirisendiri *TTitik_akhir_datagram_pengguna) Tes() {
}
func (dirisendiri *TTitik_akhir_datagram_pengguna) Init(pudpprovider TPenggunadatagramprotocolprovider, pudphandler IPenggunadatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	dirisendiri.listening = false
}
func (dirisendiri *TTitik_akhir_datagram_pengguna) PenangananPenggunadatagramprotocolPesan(data uintptr, ukuran uint16) {
	if udphandler != nil {
		udphandler.PenangananPenggunadatagramprotocolPesan(dirisendiri, data, ukuran)
	}
}
func (dirisendiri *TTitik_akhir_datagram_pengguna) Kirim(pdata []byte, ukuran uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(ukuran); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Kirim(dirisendiri, data, ukuran)
}
func (dirisendiri *TTitik_akhir_datagram_pengguna) Terputus() {
	udpprovider.Terputus(dirisendiri)
}

type TPenggunadatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TTitik_akhir_datagram_pengguna
var nomorsockets int
var bebasport uint16

func (dirisendiri *TPenggunadatagramprotocolprovider) Init(pipprovider TPenyedia_protokol_jaringan_saling_terhubung, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	nomorsockets = 0
	bebasport = 1024
}
func (dirisendiri *TPenggunadatagramprotocolprovider) Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder uint32, tujuanipaddressJaringanbyteorder uint32, internetprotocolpayload uintptr, ukuran uint32) bool {
	if ukuran < udpheaderUkuran {
		return false
	}

	var buffer_2 *TPenggunadatagramprotocolheaderbuffer = (*TPenggunadatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TKepala_datagram_pengguna
	msg.Init(buffer_2)

	var soket *TTitik_akhir_datagram_pengguna = nil

	for i := 0; i < nomorsockets && soket == nil; i++ {
		if sockets[i].lokalportNomor == msg.nomor_porta_tujuan && sockets[i].lokalip == tujuanipaddressJaringanbyteorder && sockets[i].listening == true {
			soket = &sockets[i]
			soket.listening = false
			soket.jauhportNomor = msg.nomor_porta_sumber
			soket.jauhip = sumberipaddressJaringanbyteorder
		} else if sockets[i].lokalportNomor == msg.nomor_porta_tujuan && sockets[i].lokalip == tujuanipaddressJaringanbyteorder && sockets[i].jauhportNomor == msg.nomor_porta_sumber && sockets[i].jauhip == sumberipaddressJaringanbyteorder {
			soket = &sockets[i]

		}
	}

	msg.Aturbuffer(buffer_2)
	if soket != nil {
		soket.PenangananPenggunadatagramprotocolPesan(internetprotocolpayload+uintptr(udpheaderUkuran), uint16(ukuran-udpheaderUkuran))
	}

	return false
}

func (dirisendiri *TPenggunadatagramprotocolprovider) Sambung(ip uint32, port uint16) *TTitik_akhir_datagram_pengguna {
	var memorimanager = &TMemorimanager{}
	var soket = (*TTitik_akhir_datagram_pengguna)(memorimanager.Alokasikan_memori(50))

	if soket != nil {

		soket.Init(*dirisendiri, nil)
		soket.jauhportNomor = port
		soket.jauhip = ip
		soket.lokalportNomor = bebasport
		bebasport++
		soket.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.jauhportNomor = Unsignedinteger16r(soket.jauhportNomor)
		soket.lokalportNomor = Unsignedinteger16r(soket.lokalportNomor)

		sockets[nomorsockets] = *soket
		nomorsockets++

	}
	return soket

}
func (dirisendiri *TPenggunadatagramprotocolprovider) Listen(port uint16) *TTitik_akhir_datagram_pengguna {
	var soket = &TTitik_akhir_datagram_pengguna{}
	soket = nil
	if soket != nil {
		soket.Init(*dirisendiri, nil)
		soket.listening = true
		soket.lokalportNomor = port
		soket.lokalip = uint32((*iphandler.Providerget()).Getipaddress())

		soket.lokalportNomor = Unsignedinteger16r(soket.lokalportNomor)
	}
	return soket
}
func (dirisendiri *TPenggunadatagramprotocolprovider) Terputus(soket *TTitik_akhir_datagram_pengguna) {
	for i := 0; i < nomorsockets && soket == nil; i++ {
		if sockets[i] == *soket {
			nomorsockets--
			sockets[i] = sockets[nomorsockets]
			break
		}
	}
}
func (dirisendiri *TPenggunadatagramprotocolprovider) Kirim(soket *TTitik_akhir_datagram_pengguna, pdata uintptr, ukuran uint16) {
	var totalPanjang = uint32(ukuran) + udpheaderUkuran

	var buffer_2 [4096]byte

	var msgbuffer = (*TPenggunadatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TKepala_datagram_pengguna{}

	msg.nomor_porta_sumber = soket.lokalportNomor
	msg.nomor_porta_tujuan = soket.jauhportNomor
	msg.panjang = Unsignedinteger16r(uint16(totalPanjang))

	msg.checksum = 0x0
	msg.Aturbuffer(msgbuffer)

	var dataByte [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(ukuran); i++ {
		buffer_2[int(udpheaderUkuran)+i] = dataByte[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Kirim(soket.jauhip, 0x11, data, totalPanjang)

}
func (dirisendiri *TPenggunadatagramprotocolprovider) Bind(soket *TTitik_akhir_datagram_pengguna, handler *TPenggunadatagramprotocolhandler) {
}
