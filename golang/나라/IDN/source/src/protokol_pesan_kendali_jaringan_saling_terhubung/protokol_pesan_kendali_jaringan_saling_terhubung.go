/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokol_pesan_kendali_jaringan_saling_terhubung

import . "unsafe"
import . "console"
import . "memorimanager"
import . "bingkai_jaringan_media_bersama"
import . "protokol_jaringan_saling_terhubung_4"
import . "util"

var icmpconsole = TConsole{}

type TInternetKontrolPesanprotocolPesanbuffer struct {
	Tipe	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpUkuran int = 64

type TInternetKontrolPesanprotocolPesan struct {
	Tipe	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (dirisendiri *TInternetKontrolPesanprotocolPesan) Init(buffer_2 TInternetKontrolPesanprotocolPesanbuffer) {
	dirisendiri.Tipe = buffer_2.Tipe
	dirisendiri.code = buffer_2.code

	dirisendiri.checksum = Unsignedinteger16r(Jajarantounsignedinteger16(buffer_2.checksum))
	dirisendiri.data = Unsignedinteger32r(Jajarantounsignedinteger32(buffer_2.data))
}

func (dirisendiri *TInternetKontrolPesanprotocolPesan) Aturbuffer(buffer_2 *TInternetKontrolPesanprotocolPesanbuffer) {
	buffer_2.Tipe = dirisendiri.Tipe
	buffer_2.code = dirisendiri.code

	buffer_2.checksum = Unsignedinteger16toJajaran(dirisendiri.checksum)
	buffer_2.data = Unsignedinteger32toJajaran(dirisendiri.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protokol_pesan_kendali_jaringan_saling_terhubung *TProtokol_pesan_kendali_jaringan_saling_terhubung

func (dirisendiri *Icmphandler) Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder uint32, tujuanipaddressJaringanbyteorder uint32, dataPenunjuk uintptr, ukuran uint32) bool {
	return protokol_pesan_kendali_jaringan_saling_terhubung.Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder, tujuanipaddressJaringanbyteorder, dataPenunjuk, ukuran)
}

var iphandler IInternetprotocolhandler

type TProtokol_pesan_kendali_jaringan_saling_terhubung struct {
}

func (dirisendiri *TProtokol_pesan_kendali_jaringan_saling_terhubung) Init(backend TPenyedia_protokol_jaringan_saling_terhubung, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protokol_pesan_kendali_jaringan_saling_terhubung = dirisendiri
}
func (dirisendiri *TProtokol_pesan_kendali_jaringan_saling_terhubung) Internetprotocolreceivewhen(sumberipaddressJaringanbyteorder uint32, tujuanipaddressJaringanbyteorder uint32, dataPenunjuk uintptr, ukuran uint32) bool {
	if ukuran < uint32(icmpUkuran) {
		return false
	}

	var buffer_2 *TInternetKontrolPesanprotocolPesanbuffer = (*TInternetKontrolPesanprotocolPesanbuffer)(Pointer(dataPenunjuk))
	var msg TInternetKontrolPesanprotocolPesan = TInternetKontrolPesanprotocolPesan{}
	msg.Init(*buffer_2)

	icmpconsole.MCetak(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Cetak(uint16(msg.Tipe))
	icmpconsole.MCetak(([]byte)(":"))

	switch msg.Tipe {
	case 0:
		icmpconsole.MCetak(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MCetak(([]byte)("ping send "))
		msg.Tipe = 0

		msg.checksum = 0
		msg.Aturbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPenunjuk)), uint32(icmpUkuran))

		msg.Aturbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (dirisendiri *TProtokol_pesan_kendali_jaringan_saling_terhubung) EchorequestKirim(ipJaringanbyteorder uint32) bool {
	var protokol_pesan_kendali_jaringan_saling_terhubung TInternetKontrolPesanprotocolPesan = TInternetKontrolPesanprotocolPesan{}

	var memorimanager = &TMemorimanager{}
	var buffer_2 = (*TInternetKontrolPesanprotocolPesanbuffer)(memorimanager.Alokasikan_memori(1024))

	protokol_pesan_kendali_jaringan_saling_terhubung.Tipe = 8
	protokol_pesan_kendali_jaringan_saling_terhubung.code = 0
	protokol_pesan_kendali_jaringan_saling_terhubung.data = 0x3713
	protokol_pesan_kendali_jaringan_saling_terhubung.checksum = 0
	protokol_pesan_kendali_jaringan_saling_terhubung.Aturbuffer(buffer_2)
	protokol_pesan_kendali_jaringan_saling_terhubung.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpUkuran))
	protokol_pesan_kendali_jaringan_saling_terhubung.Aturbuffer(buffer_2)

	var dataPenunjuk uintptr = uintptr(Pointer(buffer_2))
	iphandler.Kirim(ipJaringanbyteorder, 0x01, dataPenunjuk, uint32(icmpUkuran))

	return false

}
