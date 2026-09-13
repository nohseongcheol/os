package protokol_mesej_kawalan_rangkaian_saling_terhubung

import . "unsafe"
import . "console"
import . "ingatanmanager"
import . "bingkai_rangkaian_medium_bersama"
import . "protokol_rangkaian_saling_terhubung_4"
import . "util"

var icmpconsole = TConsole{}

type TInternetKawalanmesejprotocolmesejbuffer struct {
	Jenis	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpSaiz int = 64

type TInternetKawalanmesejprotocolmesej struct {
	Jenis	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (diri *TInternetKawalanmesejprotocolmesej) Init(buffer_2 TInternetKawalanmesejprotocolmesejbuffer) {
	diri.Jenis = buffer_2.Jenis
	diri.code = buffer_2.code

	diri.checksum = Unsignedinteger16r(Tatasusunantounsignedinteger16(buffer_2.checksum))
	diri.data = Unsignedinteger32r(Tatasusunantounsignedinteger32(buffer_2.data))
}

func (diri *TInternetKawalanmesejprotocolmesej) Tetapkanbuffer(buffer_2 *TInternetKawalanmesejprotocolmesejbuffer) {
	buffer_2.Jenis = diri.Jenis
	buffer_2.code = diri.code

	buffer_2.checksum = Unsignedinteger16toTatasusunan(diri.checksum)
	buffer_2.data = Unsignedinteger32toTatasusunan(diri.data)
}

type Icmphandler struct {
	TInternetprotocolhandler
}

var protokol_mesej_kawalan_rangkaian_saling_terhubung *TProtokol_mesej_kawalan_rangkaian_saling_terhubung

func (diri *Icmphandler) Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder uint32, destinationipaddressRangkaianbyteorder uint32, dataPenuding uintptr, saiz uint32) bool {
	return protokol_mesej_kawalan_rangkaian_saling_terhubung.Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder, destinationipaddressRangkaianbyteorder, dataPenuding, saiz)
}

var iphandler IInternetprotocolhandler

type TProtokol_mesej_kawalan_rangkaian_saling_terhubung struct {
}

func (diri *TProtokol_mesej_kawalan_rangkaian_saling_terhubung) Init(backend TPembekal_protokol_rangkaian_saling_terhubung, handler IInternetprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	protokol_mesej_kawalan_rangkaian_saling_terhubung = diri
}
func (diri *TProtokol_mesej_kawalan_rangkaian_saling_terhubung) Internetprotocolreceivewhen(sumberipaddressRangkaianbyteorder uint32, destinationipaddressRangkaianbyteorder uint32, dataPenuding uintptr, saiz uint32) bool {
	if saiz < uint32(icmpSaiz) {
		return false
	}

	var buffer_2 *TInternetKawalanmesejprotocolmesejbuffer = (*TInternetKawalanmesejprotocolmesejbuffer)(Pointer(dataPenuding))
	var msg TInternetKawalanmesejprotocolmesej = TInternetKawalanmesejprotocolmesej{}
	msg.Init(*buffer_2)

	icmpconsole.MCetak(([]byte)("icmp:OnInternet"))
	icmpconsole.MUnsignedinteger16Cetak(uint16(msg.Jenis))
	icmpconsole.MCetak(([]byte)(":"))

	switch msg.Jenis {
	case 0:
		icmpconsole.MCetak(([]byte)("ping response from "))
		break

	case 8:
		icmpconsole.MCetak(([]byte)("ping send "))
		msg.Jenis = 0

		msg.checksum = 0
		msg.Tetapkanbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataPenuding)), uint32(icmpSaiz))

		msg.Tetapkanbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (diri *TProtokol_mesej_kawalan_rangkaian_saling_terhubung) EchorequestHantar(ipRangkaianbyteorder uint32) bool {
	var protokol_mesej_kawalan_rangkaian_saling_terhubung TInternetKawalanmesejprotocolmesej = TInternetKawalanmesejprotocolmesej{}

	var ingatanmanager = &TIngatanmanager{}
	var buffer_2 = (*TInternetKawalanmesejprotocolmesejbuffer)(ingatanmanager.Peruntukkan_ingatan(1024))

	protokol_mesej_kawalan_rangkaian_saling_terhubung.Jenis = 8
	protokol_mesej_kawalan_rangkaian_saling_terhubung.code = 0
	protokol_mesej_kawalan_rangkaian_saling_terhubung.data = 0x3713
	protokol_mesej_kawalan_rangkaian_saling_terhubung.checksum = 0
	protokol_mesej_kawalan_rangkaian_saling_terhubung.Tetapkanbuffer(buffer_2)
	protokol_mesej_kawalan_rangkaian_saling_terhubung.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpSaiz))
	protokol_mesej_kawalan_rangkaian_saling_terhubung.Tetapkanbuffer(buffer_2)

	var dataPenuding uintptr = uintptr(Pointer(buffer_2))
	iphandler.Hantar(ipRangkaianbyteorder, 0x01, dataPenuding, uint32(icmpSaiz))

	return false

}
