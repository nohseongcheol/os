/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package протокол_обʼєднаної_мережі_4

import . "unsafe"
import . "util"
import . "консоль"
import . "кадр_мережі_зі_спільним_середовищем"
import . "arp"

var ipКонсоль TКонсоль = TКонсоль{}

type TІнтернетprotocolv4Повідомленняbuffer struct {
	lenver		byte
	tos		byte
	усьогоДовжина	[2]byte

	ident			[2]byte
	прапориandoffset	[2]byte

	частоlive	byte
	protocol	byte
	checksum	[2]byte

	джерелоipАдреса		[4]byte
	призначенняipАдреса	[4]byte
}

var ipРозмір uint8 = (4 + 4 + 4 + 8)

type TІнтернетprotocolv4Повідомлення struct {
	headerДовжина	uint8
	версія		uint8
	tos		uint8
	усьогоДовжина	uint16

	ident			uint16
	прапориandoffset	uint16

	частоlive	uint8
	protocol	uint8
	checksum	uint16

	джерелоipАдреса		uint32
	призначенняipАдреса	uint32
}

func (поточний *TІнтернетprotocolv4Повідомлення) Init(buffer_2 TІнтернетprotocolv4Повідомленняbuffer) {

	поточний.версія = ((buffer_2.lenver & 0xF0) >> 4)
	поточний.headerДовжина = buffer_2.lenver & 0x0F
	поточний.tos = buffer_2.tos
	поточний.усьогоДовжина = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.усьогоДовжина))

	поточний.ident = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.ident))
	поточний.прапориandoffset = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.прапориandoffset))

	поточний.частоlive = buffer_2.частоlive
	поточний.protocol = buffer_2.protocol
	поточний.checksum = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.checksum))

	поточний.джерелоipАдреса = Unsignedinteger32r(Масивтоunsignedinteger32(buffer_2.джерелоipАдреса))
	поточний.призначенняipАдреса = Unsignedinteger32r(Масивтоunsignedinteger32(buffer_2.призначенняipАдреса))

}
func (поточний *TІнтернетprotocolv4Повідомлення) Множинаbuffer(buffer_2 *TІнтернетprotocolv4Повідомленняbuffer) {

	buffer_2.lenver = byte(((поточний.версія & 0x0F) << 4) | (поточний.headerДовжина & 0x0F))
	buffer_2.tos = поточний.tos
	buffer_2.усьогоДовжина = Unsignedinteger16тоМасив(поточний.усьогоДовжина)

	buffer_2.ident = Unsignedinteger16тоМасив(поточний.ident)
	buffer_2.прапориandoffset = Unsignedinteger16тоМасив(поточний.прапориandoffset)

	buffer_2.частоlive = поточний.частоlive
	buffer_2.protocol = поточний.protocol
	buffer_2.checksum = Unsignedinteger16тоМасив(поточний.checksum)

	buffer_2.джерелоipАдреса = Unsignedinteger32тоМасив(поточний.джерелоipАдреса)
	buffer_2.призначенняipАдреса = Unsignedinteger32тоМасив(поточний.призначенняipАдреса)

}

type IІнтернетprotocolhandler interface {
	Init(backend TПостачальник_протоколу_обʼєднаної_мережі, pihandler IІнтернетprotocolhandler, pprotocol uint8)
	Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder uint32, призначенняipАдресаМережаbyteorder uint32, dataВказівник uintptr, розмір uint32) bool
	Надіслати(призначенняipАдресаМережаbyteorder uint32, pprotocol uint8, dataВказівник uintptr, розмір uint32)
	Providerget() *TПостачальник_протоколу_обʼєднаної_мережі
}

type TІнтернетprotocolhandler struct {
}

var ipethernetБлокhandler IpethernetБлокhandler = IpethernetБлокhandler{}
var protocol uint8

func (поточний *TІнтернетprotocolhandler) Init(backend TПостачальник_протоколу_обʼєднаної_мережі, pihandler IІнтернетprotocolhandler, pprotocol uint8) {
	protocol = pprotocol
	handler_2[protocol] = pihandler
}
func (поточний *TІнтернетprotocolhandler) Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder uint32, призначенняipАдресаМережаbyteorder uint32, dataВказівник uintptr, розмір uint32) bool {
	ipКонсоль.MДрук(([]byte)("ipHandler:OnInternet"))
	return false
}
func (поточний *TІнтернетprotocolhandler) Надіслати(призначенняipАдресаМережаbyteorder uint32, pprotocol uint8, dataВказівник uintptr, розмір uint32) {

	постачальник_протоколу_обʼєднаної_мережі.Надіслати(призначенняipАдресаМережаbyteorder, pprotocol, dataВказівник, розмір)
}
func (поточний *TІнтернетprotocolhandler) Providerget() *TПостачальник_протоколу_обʼєднаної_мережі {
	return &постачальник_протоколу_обʼєднаної_мережі
}

type IpethernetБлокhandler struct {
	TEthernetБлокhandler
}

var постачальник_протоколу_обʼєднаної_мережі TПостачальник_протоколу_обʼєднаної_мережі

func (поточний *IpethernetБлокhandler) EthernetБлокreceivewhen(dataВказівник uintptr, розмір int) bool {
	ipКонсоль.MДрук(([]byte)("iphandler:onEtherfameRecv\n"))
	return постачальник_протоколу_обʼєднаної_мережі.EthernetБлокreceivewhen(dataВказівник, uint32(розмір))

}

func (поточний *IpethernetБлокhandler) Надіслати(призначенняipАдресаМережаbyteorder uint64, dataВказівник uintptr, розмір uint32) {
	ipКонсоль.MДрук(([]byte)("ipefhandler:send\n"))
	var ethernetТипbe = Unsignedinteger16r(0x0800)
	поточний.TEthernetБлокhandler.БлокНадіслати(призначенняipАдресаМережаbyteorder, ethernetТипbe, dataВказівник, розмір)

}

var handler_2 [255]IІнтернетprotocolhandler

type TПостачальник_протоколу_обʼєднаної_мережі struct {
	arpprovider	Arpprovider
	Gatewayip	uint32
	SubnetМаска	uint32
}

var efhandler IEthernetБлокhandler

func (поточний *TПостачальник_протоколу_обʼєднаної_мережі) Init(pefprovider TПостачальник_кадрів_мережі_зі_спільним_середовищем, pefhandler IEthernetБлокhandler, arp Arpprovider, gatewayip uint32, subnetМаска uint32) {

	efhandler = pefhandler
	efhandler.Множинаhandler(pefhandler, 0x0800)

	for i := 0; i < 255; i++ {
		handler_2[i] = nil
	}

	поточний.arpprovider = arp
	поточний.Gatewayip = gatewayip
	поточний.SubnetМаска = subnetМаска
	постачальник_протоколу_обʼєднаної_мережі = *поточний
}
func (поточний *TПостачальник_протоколу_обʼєднаної_мережі) EthernetБлокreceivewhen(ethernetБлокpayload uintptr, розмір uint32) bool {
	if розмір < uint32(ipРозмір) {
		return false
	}

	var buffer_2 *TІнтернетprotocolv4Повідомленняbuffer = (*TІнтернетprotocolv4Повідомленняbuffer)(Pointer(ethernetБлокpayload))
	var інтернетprotocolПовідомлення TІнтернетprotocolv4Повідомлення
	інтернетprotocolПовідомлення.Init(*buffer_2)

	var reply bool = false

	if інтернетprotocolПовідомлення.призначенняipАдреса == uint32(efhandler.GetipАдреса()) {

		var довжина uint32 = uint32(інтернетprotocolПовідомлення.усьогоДовжина)
		if довжина > розмір {
			довжина = розмір
		}
		if handler_2[інтернетprotocolПовідомлення.protocol] != nil {
			reply = handler_2[інтернетprotocolПовідомлення.protocol].Інтернетprotocolreceivewhen(інтернетprotocolПовідомлення.джерелоipАдреса, інтернетprotocolПовідомлення.призначенняipАдреса, ethernetБлокpayload+uintptr(4*інтернетprotocolПовідомлення.headerДовжина), uint32(довжина-uint32(4*інтернетprotocolПовідомлення.headerДовжина)))

		}
	}

	if reply {

		var temporary = інтернетprotocolПовідомлення.призначенняipАдреса
		інтернетprotocolПовідомлення.призначенняipАдреса = інтернетprotocolПовідомлення.джерелоipАдреса
		інтернетprotocolПовідомлення.джерелоipАдреса = temporary

		інтернетprotocolПовідомлення.частоlive = 0x40
		інтернетprotocolПовідомлення.checksum = 0

		інтернетprotocolПовідомлення.Множинаbuffer(buffer_2)
		інтернетprotocolПовідомлення.checksum = поточний.Checksum((*([4096]uint16))(Pointer(ethernetБлокpayload)), uint32(4*інтернетprotocolПовідомлення.headerДовжина))

		інтернетprotocolПовідомлення.Множинаbuffer(buffer_2)

	}

	ipКонсоль.MДрук(([]byte)("ipmessage"))
	ipКонсоль.MUnsignedinteger32Друк(інтернетprotocolПовідомлення.джерелоipАдреса)
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MUnsignedinteger32Друк(інтернетprotocolПовідомлення.призначенняipАдреса)
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MUnsignedinteger16Друк(uint16(інтернетprotocolПовідомлення.headerДовжина))
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MUnsignedinteger16Друк(uint16(інтернетprotocolПовідомлення.версія))
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MUnsignedinteger16Друк(інтернетprotocolПовідомлення.усьогоДовжина)
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MUnsignedinteger32Друк(uint32(efhandler.GetipАдреса()))
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MДрук(([]byte)("\n"))

	return reply

}
func (поточний *TПостачальник_протоколу_обʼєднаної_мережі) Надіслати(призначенняipАдресаМережаbyteorder uint32, protocol uint8, dataВказівник uintptr, розмір uint32) {
	var buffer1_2 [4096]byte
	var buffer_2 *TІнтернетprotocolv4Повідомленняbuffer = (*TІнтернетprotocolv4Повідомленняbuffer)(Pointer(&buffer1_2))
	var повідомлення TІнтернетprotocolv4Повідомлення = TІнтернетprotocolv4Повідомлення{}
	повідомлення.версія = 4
	повідомлення.headerДовжина = ipРозмір / 4
	повідомлення.tos = 0
	повідомлення.усьогоДовжина = Unsignedinteger16r(uint16(розмір + uint32(ipРозмір)))

	повідомлення.ident = 0x0100
	повідомлення.прапориandoffset = 0x0040
	повідомлення.частоlive = 0x40
	повідомлення.protocol = protocol

	повідомлення.призначенняipАдреса = призначенняipАдресаМережаbyteorder

	повідомлення.джерелоipАдреса = uint32(efhandler.GetipАдреса())

	повідомлення.checksum = 0

	повідомлення.Множинаbuffer(buffer_2)
	повідомлення.checksum = поточний.Checksum((*([4096]uint16))(Pointer(&buffer1_2)), uint32(ipРозмір))
	повідомлення.Множинаbuffer(buffer_2)

	var databuffer_2 [4096]byte = *(*([4096]byte))(Pointer(dataВказівник))

	for i := 0; i < int(розмір); i++ {

		buffer1_2[i+int(ipРозмір)] = databuffer_2[i]
	}

	ipКонсоль.MДрукxy(([]byte)("ipprovider:send["), 1, 18)
	for i := 0; i < int(розмір)+int(ipРозмір); i++ {
		ipКонсоль.MHexadecimalДрук(buffer1_2[i])
	}
	ipКонсоль.MДрук(([]byte)(":"))
	ipКонсоль.MДрук(([]byte)("]\n"))

	var наступнеhopipАдресаМережаbyteorder uint32 = призначенняipАдресаМережаbyteorder
	if (призначенняipАдресаМережаbyteorder & поточний.SubnetМаска) != (повідомлення.джерелоipАдреса & поточний.SubnetМаска) {
		наступнеhopipАдресаМережаbyteorder = поточний.Gatewayip
	}

	var надіслатиdataВказівник = uintptr(Pointer(&buffer1_2))
	ipКонсоль.MUnsignedinteger32Друк(наступнеhopipАдресаМережаbyteorder)

	var ethernetТипbe = Unsignedinteger16r(0x0800)
	efhandler.БлокНадіслати(поточний.arpprovider.Resolve(наступнеhopipАдресаМережаbyteorder), ethernetТипbe, надіслатиdataВказівник, uint32(ipРозмір)+uint32(розмір))

}
func (поточний *TПостачальник_протоколу_обʼєднаної_мережі) Checksum(pdata *[4096]uint16, довжинаВхіднийБайт uint32) uint16 {
	var data [4096]uint16 = *pdata
	var temporary uint32 = 0
	var dataБайт [4096]byte = *(*([4096]byte))(Pointer(&data))
	if (довжинаВхіднийБайт % 2) != 0 {
		temporary += uint32(uint16(dataБайт[довжинаВхіднийБайт-1]) << 8)
	}

	for (temporary & 0xFFFF0000) != 0 {
		temporary = (temporary & 0xFFFF) + (temporary >> 16)
	}

	return uint16(((^temporary & 0xFF00) >> 8) | ((^temporary & 0x00FF) << 8))
}
func (поточний *TПостачальник_протоколу_обʼєднаної_мережі) GetipАдреса() uint64 {
	return efhandler.GetipАдреса()
}
