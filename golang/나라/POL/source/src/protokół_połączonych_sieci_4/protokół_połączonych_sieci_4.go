/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokół_połączonych_sieci_4

import . "unsafe"
import . "util"
import . "konsola"
import . "ramka_sieci_o_wspólnym_medium"
import . "arp"

var ipKonsola TKonsola = TKonsola{}

type TInternetprotocolv4Wiadomośćbuffer struct {
	lenver		byte
	tos		byte
	łącznieDługość	[2]byte

	ident				[2]byte
	znacznikiorazPrzesunięcie	[2]byte

	czastolive	byte
	protocol	byte
	sumakontrolna	[2]byte

	źródłoipAdres	[4]byte
	celipAdres	[4]byte
}

var ipRozmiar uint8 = (4 + 4 + 4 + 8)

type TInternetprotocolv4Wiadomość struct {
	headerDługość	uint8
	wersja		uint8
	tos		uint8
	łącznieDługość	uint16

	ident				uint16
	znacznikiorazPrzesunięcie	uint16

	czastolive	uint8
	protocol	uint8
	sumakontrolna	uint16

	źródłoipAdres	uint32
	celipAdres	uint32
}

func (bieżący *TInternetprotocolv4Wiadomość) Init(buffer_2 TInternetprotocolv4Wiadomośćbuffer) {

	bieżący.wersja = ((buffer_2.lenver & 0xF0) >> 4)
	bieżący.headerDługość = buffer_2.lenver & 0x0F
	bieżący.tos = buffer_2.tos
	bieżący.łącznieDługość = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.łącznieDługość))

	bieżący.ident = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.ident))
	bieżący.znacznikiorazPrzesunięcie = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.znacznikiorazPrzesunięcie))

	bieżący.czastolive = buffer_2.czastolive
	bieżący.protocol = buffer_2.protocol
	bieżący.sumakontrolna = Unsignedinteger16r(Tablicatounsignedinteger16(buffer_2.sumakontrolna))

	bieżący.źródłoipAdres = Unsignedinteger32r(Tablicatounsignedinteger32(buffer_2.źródłoipAdres))
	bieżący.celipAdres = Unsignedinteger32r(Tablicatounsignedinteger32(buffer_2.celipAdres))

}
func (bieżący *TInternetprotocolv4Wiadomość) Zbiórbuffer(buffer_2 *TInternetprotocolv4Wiadomośćbuffer) {

	buffer_2.lenver = byte(((bieżący.wersja & 0x0F) << 4) | (bieżący.headerDługość & 0x0F))
	buffer_2.tos = bieżący.tos
	buffer_2.łącznieDługość = Unsignedinteger16toTablica(bieżący.łącznieDługość)

	buffer_2.ident = Unsignedinteger16toTablica(bieżący.ident)
	buffer_2.znacznikiorazPrzesunięcie = Unsignedinteger16toTablica(bieżący.znacznikiorazPrzesunięcie)

	buffer_2.czastolive = bieżący.czastolive
	buffer_2.protocol = bieżący.protocol
	buffer_2.sumakontrolna = Unsignedinteger16toTablica(bieżący.sumakontrolna)

	buffer_2.źródłoipAdres = Unsignedinteger32toTablica(bieżący.źródłoipAdres)
	buffer_2.celipAdres = Unsignedinteger32toTablica(bieżący.celipAdres)

}

type IInternetprotocolhandler interface {
	Init(backend TDostawca_protokołu_połączonych_sieci, pihandler IInternetprotocolhandler, pprotocol uint8)
	Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder uint32, celipAdresSiećbyteorder uint32, dataKursor uintptr, rozmiar uint32) bool
	Wyślij(celipAdresSiećbyteorder uint32, pprotocol uint8, dataKursor uintptr, rozmiar uint32)
	Providerget() *TDostawca_protokołu_połączonych_sieci
}

type TInternetprotocolhandler struct {
}

var ipethernetRamkahandler IpethernetRamkahandler = IpethernetRamkahandler{}
var protocol uint8

func (bieżący *TInternetprotocolhandler) Init(backend TDostawca_protokołu_połączonych_sieci, pihandler IInternetprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (bieżący *TInternetprotocolhandler) Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder uint32, celipAdresSiećbyteorder uint32, dataKursor uintptr, rozmiar uint32) bool {
	ipKonsola.MWydrukuj(([]byte)("ipHandler:OnInternet"))
	return false
}
func (bieżący *TInternetprotocolhandler) Wyślij(celipAdresSiećbyteorder uint32, pprotocol uint8, dataKursor uintptr, rozmiar uint32) {

	dostawca_protokołu_połączonych_sieci.Wyślij(celipAdresSiećbyteorder, pprotocol, dataKursor, rozmiar)
}
func (bieżący *TInternetprotocolhandler) Providerget() *TDostawca_protokołu_połączonych_sieci {
	return &dostawca_protokołu_połączonych_sieci
}

type IpethernetRamkahandler struct {
	TEthernetRamkahandler
}

var dostawca_protokołu_połączonych_sieci TDostawca_protokołu_połączonych_sieci

func (bieżący *IpethernetRamkahandler) EthernetRamkareceivewhen(dataKursor uintptr, rozmiar int) bool {
	ipKonsola.MWydrukuj(([]byte)("iphandler:onEtherfameRecv\n"))
	return dostawca_protokołu_połączonych_sieci.EthernetRamkareceivewhen(dataKursor, uint32(rozmiar))

}

func (bieżący *IpethernetRamkahandler) Wyślij(celipAdresSiećbyteorder uint64, dataKursor uintptr, rozmiar uint32) {
	ipKonsola.MWydrukuj(([]byte)("ipefhandler:send\n"))
	var ethernetTypbe = Unsignedinteger16r(0x0800)
	bieżący.TEthernetRamkahandler.RamkaWyślij(celipAdresSiećbyteorder, ethernetTypbe, dataKursor, rozmiar)

}

var handler_2 [255]IInternetprotocolhandler

type TDostawca_protokołu_połączonych_sieci struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetMaska	uint32
}

var efhandler IEthernetRamkahandler

func (bieżący *TDostawca_protokołu_połączonych_sieci) Init(pefprovider TDostawca_ramek_sieci_o_wspólnym_medium, pefhandler IEthernetRamkahandler, arp Arpprovider, gatewayip uint32, subnetMaska uint32) {

	efhandler = pefhandler
	efhandler.Zbiórhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	bieżący.arpprovider = arp
	bieżący.Gatewayip = gatewayip
	bieżący.SubnetMaska = subnetMaska
	dostawca_protokołu_połączonych_sieci = *bieżący
}
func (bieżący *TDostawca_protokołu_połączonych_sieci) EthernetRamkareceivewhen(ethernetRamkapayload uintptr, rozmiar uint32) bool {
	if rozmiar < uint32(ipRozmiar) {
		return false
	}

	var buffer_2 *TInternetprotocolv4Wiadomośćbuffer = (*TInternetprotocolv4Wiadomośćbuffer)(Pointer(ethernetRamkapayload))
	var internetprotocolWiadomość TInternetprotocolv4Wiadomość
	internetprotocolWiadomość.Init(*buffer_2)

	var reply bool = false

	if internetprotocolWiadomość.celipAdres == uint32(efhandler.GetipAdres()) {

		var długość uint32 = uint32(internetprotocolWiadomość.łącznieDługość)
		if długość > rozmiar {
			długość = rozmiar
		}
		if handler_2[internetprotocolWiadomość.protocol] != nil {
			reply = handler_2[internetprotocolWiadomość.protocol].Internetprotocolreceivewhen(internetprotocolWiadomość.źródłoipAdres, internetprotocolWiadomość.celipAdres, ethernetRamkapayload+uintptr(4*internetprotocolWiadomość.headerDługość), uint32(długość-uint32(4*internetprotocolWiadomość.headerDługość)))

		}
	}

	if reply {

		var temporary = internetprotocolWiadomość.celipAdres
		internetprotocolWiadomość.celipAdres = internetprotocolWiadomość.źródłoipAdres
		internetprotocolWiadomość.źródłoipAdres = temporary

		internetprotocolWiadomość.czastolive = 0x40
		internetprotocolWiadomość.sumakontrolna = 0

		internetprotocolWiadomość.Zbiórbuffer(buffer_2)
		internetprotocolWiadomość.sumakontrolna = bieżący.Sumakontrolna((*([4096]uint16))(Pointer(ethernetRamkapayload)), uint32(4*internetprotocolWiadomość.headerDługość))

		internetprotocolWiadomość.Zbiórbuffer(buffer_2)

	}

	ipKonsola.MWydrukuj(([]byte)("ipmessage"))
	ipKonsola.MUnsignedinteger32Wydrukuj(internetprotocolWiadomość.źródłoipAdres)
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MUnsignedinteger32Wydrukuj(internetprotocolWiadomość.celipAdres)
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MUnsignedinteger16Wydrukuj(uint16(internetprotocolWiadomość.headerDługość))
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MUnsignedinteger16Wydrukuj(uint16(internetprotocolWiadomość.wersja))
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MUnsignedinteger16Wydrukuj(internetprotocolWiadomość.łącznieDługość)
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MUnsignedinteger32Wydrukuj(uint32(efhandler.GetipAdres()))
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MWydrukuj(([]byte)("\n"))

	return reply

}
func (bieżący *TDostawca_protokołu_połączonych_sieci) Wyślij(celipAdresSiećbyteorder uint32, protocol uint8, dataKursor uintptr, rozmiar uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TInternetprotocolv4Wiadomośćbuffer = (*TInternetprotocolv4Wiadomośćbuffer)(Pointer(&buffer1_2))
	var wiadomość TInternetprotocolv4Wiadomość = TInternetprotocolv4Wiadomość{}
	wiadomość.wersja = 4
	wiadomość.headerDługość = ipRozmiar / 4
	wiadomość.tos = 0
	wiadomość.łącznieDługość = Unsignedinteger16r(uint16(rozmiar + uint32(ipRozmiar)))

	wiadomość.ident = 0x0100
	wiadomość.znacznikiorazPrzesunięcie = 0x0040
	wiadomość.czastolive = 0x40
	wiadomość.protocol = protocol

	wiadomość.celipAdres = celipAdresSiećbyteorder

	wiadomość.źródłoipAdres = uint32(efhandler.GetipAdres())

	wiadomość.sumakontrolna = 0

	wiadomość.Zbiórbuffer(buffer_2)
	wiadomość.sumakontrolna = bieżący.Sumakontrolna((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipRozmiar))
	wiadomość.Zbiórbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataKursor))

	for i := 0; i < int(rozmiar); i++ {

		buffer1_2[i+int(ipRozmiar)] = databuffer_2[i]
	}

	ipKonsola.MWydrukujxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(rozmiar)+int(ipRozmiar); i++ {
		ipKonsola.MHexadecimalWydrukuj(buffer1_2[i])
	}
	ipKonsola.MWydrukuj(([]byte)(":"))
	ipKonsola.MWydrukuj(([]byte)("]\n"))

	var następnyhopipAdresSiećbyteorder uint32 = celipAdresSiećbyteorder
	if (celipAdresSiećbyteorder & bieżący.SubnetMaska) != (wiadomość.źródłoipAdres & bieżący.SubnetMaska) {
		następnyhopipAdresSiećbyteorder = bieżący.Gatewayip
	}

	var wyślijdataKursor = uintptr(Pointer(&buffer1_2))
	ipKonsola.MUnsignedinteger32Wydrukuj(następnyhopipAdresSiećbyteorder)

	var ethernetTypbe = Unsignedinteger16r(0x0800)
	efhandler.RamkaWyślij(bieżący.arpprovider.Resolve(następnyhopipAdresSiećbyteorder), ethernetTypbe, wyślijdataKursor, uint32(ipRozmiar)+uint32(rozmiar))

}
func (bieżący *TDostawca_protokołu_połączonych_sieci) Sumakontrolna(pdata *[4096]uint16, długośćWchodzącyBajty uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataBajty [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (długośćWchodzącyBajty % 2) != 0 {
		temporary += uint32(uint16(dataBajty[długośćWchodzącyBajty-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (bieżący *TDostawca_protokołu_połączonych_sieci) GetipAdres() uint64 {
	return efhandler.GetipAdres()
}
