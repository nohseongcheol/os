/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package protokół_datagramów_użytkownika

import . "unsafe"
import . "konsola"
import . "util"
import . "pamięćmanager"
import . "protokół_połączonych_sieci_4"

var udpKonsola = TKonsola{}

type TUżytkownikdatagramprotocolheaderbuffer struct {
	numer_portu_źródłowego	[2]byte
	numer_portu_docelowego		[2]byte

	długość		[2]byte
	sumakontrolna	[2]byte
}

var udpheaderRozmiar uint32 = 8

type TNagłówek_datagramu_użytkownika struct {
	numer_portu_źródłowego	uint16
	numer_portu_docelowego		uint16

	długość		uint16
	sumakontrolna	uint16
}

func (bieżący *TNagłówek_datagramu_użytkownika) Init(buffer_2 *TUżytkownikdatagramprotocolheaderbuffer) {
	bieżący.numer_portu_źródłowego = Tablicatounsignedinteger16(buffer_2.numer_portu_źródłowego)
	bieżący.numer_portu_docelowego = Tablicatounsignedinteger16(buffer_2.numer_portu_docelowego)

	bieżący.długość = Tablicatounsignedinteger16(buffer_2.długość)
	bieżący.sumakontrolna = Tablicatounsignedinteger16(buffer_2.sumakontrolna)
}
func (bieżący *TNagłówek_datagramu_użytkownika) Zbiórbuffer(buffer_2 *TUżytkownikdatagramprotocolheaderbuffer) {

	buffer_2.numer_portu_źródłowego = Unsignedinteger16toTablica(bieżący.numer_portu_źródłowego)
	buffer_2.numer_portu_docelowego = Unsignedinteger16toTablica(bieżący.numer_portu_docelowego)

	buffer_2.długość = Unsignedinteger16toTablica(bieżący.długość)
	buffer_2.sumakontrolna = Unsignedinteger16toTablica(bieżący.sumakontrolna)

}

type IUżytkownikdatagramprotocolhandler interface {
	UchwytUżytkownikdatagramprotocolWiadomość(gniazdo *TPunkt_końcowy_datagramów_użytkownika, data uintptr, rozmiar uint16)
}

type TUżytkownikdatagramprotocolhandler struct {
}

func (bieżący *TUżytkownikdatagramprotocolhandler) Init(backend TDostawca_protokołu_połączonych_sieci) {
}
func (bieżący *TUżytkownikdatagramprotocolhandler) UchwytUżytkownikdatagramprotocolWiadomość(gniazdo *TPunkt_końcowy_datagramów_użytkownika, data uintptr, rozmiar uint16) {
}

type IUżytkownikdatagramprotocolGniazdo interface {
	UchwytUżytkownikdatagramprotocolWiadomość(data uintptr, rozmiar uint16)
}
type TPunkt_końcowy_datagramów_użytkownika struct {
	zdalneportLiczba	uint16
	zdalneip		uint32
	lokalnyportLiczba	uint16
	lokalnyip		uint32

	listening	bool
}

var udpprovider TUżytkownikdatagramprotocolprovider
var udphandler IUżytkownikdatagramprotocolhandler

func (bieżący *TPunkt_końcowy_datagramów_użytkownika) Przetestuj() {
}
func (bieżący *TPunkt_końcowy_datagramów_użytkownika) Init(pudpprovider TUżytkownikdatagramprotocolprovider, pudphandler IUżytkownikdatagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	bieżący.listening = false
}
func (bieżący *TPunkt_końcowy_datagramów_użytkownika) UchwytUżytkownikdatagramprotocolWiadomość(data uintptr, rozmiar uint16) {
	if udphandler != nil {
		udphandler.UchwytUżytkownikdatagramprotocolWiadomość(bieżący, data, rozmiar)
	}
}
func (bieżący *TPunkt_końcowy_datagramów_użytkownika) Wyślij(pdata []byte, rozmiar uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(rozmiar); i++ {
		buffer_2[i] = pdata[i]
	}
	var data = uintptr(Pointer(&buffer_2))
	udpprovider.Wyślij(bieżący, data, rozmiar)
}
func (bieżący *TPunkt_końcowy_datagramów_użytkownika) Rozłącz() {
	udpprovider.Rozłącz(bieżący)
}

type TUżytkownikdatagramprotocolprovider struct {
}

var iphandler IInternetprotocolhandler
var sockets [65535]TPunkt_końcowy_datagramów_użytkownika
var liczbasockets int
var wolneport uint16

func (bieżący *TUżytkownikdatagramprotocolprovider) Init(pipprovider TDostawca_protokołu_połączonych_sieci, piphandler IInternetprotocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	liczbasockets = 0
	wolneport = 1024
}
func (bieżący *TUżytkownikdatagramprotocolprovider) Internetprotocolreceivewhen(źródłoipAdresSiećbyteorder uint32, celipAdresSiećbyteorder uint32, internetprotocolpayload uintptr, rozmiar uint32) bool {
	if rozmiar < udpheaderRozmiar {
		return false
	}

	var buffer_2 *TUżytkownikdatagramprotocolheaderbuffer = (*TUżytkownikdatagramprotocolheaderbuffer)(Pointer(internetprotocolpayload))
	var msg TNagłówek_datagramu_użytkownika
	msg.Init(buffer_2)

	var gniazdo *TPunkt_końcowy_datagramów_użytkownika = nil

	for i := 0; i < liczbasockets && gniazdo == nil; i++ {
		if sockets[i].lokalnyportLiczba == msg.numer_portu_docelowego && sockets[i].lokalnyip == celipAdresSiećbyteorder && sockets[i].listening == true {
			gniazdo = &sockets[i]
			gniazdo.listening = false
			gniazdo.zdalneportLiczba = msg.numer_portu_źródłowego
			gniazdo.zdalneip = źródłoipAdresSiećbyteorder
		} else if sockets[i].lokalnyportLiczba == msg.numer_portu_docelowego && sockets[i].lokalnyip == celipAdresSiećbyteorder && sockets[i].zdalneportLiczba == msg.numer_portu_źródłowego && sockets[i].zdalneip == źródłoipAdresSiećbyteorder {
			gniazdo = &sockets[i]

		}
	}

	msg.Zbiórbuffer(buffer_2)
	if gniazdo != nil {
		gniazdo.UchwytUżytkownikdatagramprotocolWiadomość(internetprotocolpayload+uintptr(udpheaderRozmiar), uint16(rozmiar-udpheaderRozmiar))
	}

	return false
}

func (bieżący *TUżytkownikdatagramprotocolprovider) Połącz(ip uint32, port uint16) *TPunkt_końcowy_datagramów_użytkownika {
	var pamięćmanager = &TPamięćmanager{}
	var gniazdo = (*TPunkt_końcowy_datagramów_użytkownika)(pamięćmanager.Przydziel_pamięć(50))

	if gniazdo != nil {

		gniazdo.Init(*bieżący, nil)
		gniazdo.zdalneportLiczba = port
		gniazdo.zdalneip = ip
		gniazdo.lokalnyportLiczba = wolneport
		wolneport++
		gniazdo.lokalnyip = uint32((*iphandler.Providerget()).GetipAdres())

		gniazdo.zdalneportLiczba = Unsignedinteger16r(gniazdo.zdalneportLiczba)
		gniazdo.lokalnyportLiczba = Unsignedinteger16r(gniazdo.lokalnyportLiczba)

		sockets[liczbasockets] = *gniazdo
		liczbasockets++

	}
	return gniazdo

}
func (bieżący *TUżytkownikdatagramprotocolprovider) Listen(port uint16) *TPunkt_końcowy_datagramów_użytkownika {
	var gniazdo = &TPunkt_końcowy_datagramów_użytkownika{}
	gniazdo = nil
	if gniazdo != nil {
		gniazdo.Init(*bieżący, nil)
		gniazdo.listening = true
		gniazdo.lokalnyportLiczba = port
		gniazdo.lokalnyip = uint32((*iphandler.Providerget()).GetipAdres())

		gniazdo.lokalnyportLiczba = Unsignedinteger16r(gniazdo.lokalnyportLiczba)
	}
	return gniazdo
}
func (bieżący *TUżytkownikdatagramprotocolprovider) Rozłącz(gniazdo *TPunkt_końcowy_datagramów_użytkownika) {
	for i := 0; i < liczbasockets && gniazdo == nil; i++ {
		if sockets[i] == *gniazdo {
			liczbasockets--
			sockets[i] = sockets[liczbasockets]
			break
		}
	}
}
func (bieżący *TUżytkownikdatagramprotocolprovider) Wyślij(gniazdo *TPunkt_końcowy_datagramów_użytkownika, pdata uintptr, rozmiar uint16) {
	var łącznieDługość = uint32(rozmiar) + udpheaderRozmiar

	var buffer_2 [4096]byte

	var msgbuffer = (*TUżytkownikdatagramprotocolheaderbuffer)(Pointer(&buffer_2))

	var msg = TNagłówek_datagramu_użytkownika{}

	msg.numer_portu_źródłowego = gniazdo.lokalnyportLiczba
	msg.numer_portu_docelowego = gniazdo.zdalneportLiczba
	msg.długość = Unsignedinteger16r(uint16(łącznieDługość))

	msg.sumakontrolna = 0x0
	msg.Zbiórbuffer(msgbuffer)

	var dataBajty [4096]byte = *(*[4096]byte)(Pointer(pdata))
	for i := 0; i < int(rozmiar); i++ {
		buffer_2[int(udpheaderRozmiar)+i] = dataBajty[i]
	}

	var data uintptr = uintptr(Pointer(&buffer_2))

	iphandler.Wyślij(gniazdo.zdalneip, 0x11, data, łącznieDługość)

}
func (bieżący *TUżytkownikdatagramprotocolprovider) Dowiąż(gniazdo *TPunkt_końcowy_datagramów_użytkownika, handler *TUżytkownikdatagramprotocolhandler,) {
}
