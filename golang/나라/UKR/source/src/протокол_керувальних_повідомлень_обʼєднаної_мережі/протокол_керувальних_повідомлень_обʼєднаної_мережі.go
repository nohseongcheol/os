package протокол_керувальних_повідомлень_обʼєднаної_мережі

import . "unsafe"
import . "консоль"
import . "памятьmanager"
import . "кадр_мережі_зі_спільним_середовищем"
import . "протокол_обʼєднаної_мережі_4"
import . "util"

var icmpКонсоль = TКонсоль{}

type TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer struct {
	Тип	byte
	code	byte

	checksum	[2]byte
	data		[4]byte
}

var icmpРозмір int = 64

type TІнтернетКонтрольПовідомленняprotocolПовідомлення struct {
	Тип	uint8
	code	uint8

	checksum	uint16
	data		uint32
}

func (поточний *TІнтернетКонтрольПовідомленняprotocolПовідомлення) Init(buffer_2 TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer) {
	поточний.Тип = buffer_2.Тип
	поточний.code = buffer_2.code

	поточний.checksum = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.checksum))
	поточний.data = Unsignedinteger32r(Масивтоunsignedinteger32(buffer_2.data))
}

func (поточний *TІнтернетКонтрольПовідомленняprotocolПовідомлення) Множинаbuffer(buffer_2 *TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer) {
	buffer_2.Тип = поточний.Тип
	buffer_2.code = поточний.code

	buffer_2.checksum = Unsignedinteger16тоМасив(поточний.checksum)
	buffer_2.data = Unsignedinteger32тоМасив(поточний.data)
}

type Icmphandler struct {
	TІнтернетprotocolhandler
}

var протокол_керувальних_повідомлень_обʼєднаної_мережі *TПротокол_керувальних_повідомлень_обʼєднаної_мережі

func (поточний *Icmphandler) Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder uint32, призначенняipАдресаМережаbyteorder uint32, dataВказівник uintptr, розмір uint32) bool {
	return протокол_керувальних_повідомлень_обʼєднаної_мережі.Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder, призначенняipАдресаМережаbyteorder, dataВказівник, розмір)
}

var iphandler IІнтернетprotocolhandler

type TПротокол_керувальних_повідомлень_обʼєднаної_мережі struct {
}

func (поточний *TПротокол_керувальних_повідомлень_обʼєднаної_мережі) Init(backend TПостачальник_протоколу_обʼєднаної_мережі, handler IІнтернетprotocolhandler) {
	iphandler = handler
	iphandler.Init(backend, handler, 0x01)
	протокол_керувальних_повідомлень_обʼєднаної_мережі = поточний
}
func (поточний *TПротокол_керувальних_повідомлень_обʼєднаної_мережі) Інтернетprotocolreceivewhen(джерелоipАдресаМережаbyteorder uint32, призначенняipАдресаМережаbyteorder uint32, dataВказівник uintptr, розмір uint32) bool {
	if розмір < uint32(icmpРозмір) {
		return false
	}

	var buffer_2 *TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer = (*TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer)(Pointer(dataВказівник))
	var msg TІнтернетКонтрольПовідомленняprotocolПовідомлення = TІнтернетКонтрольПовідомленняprotocolПовідомлення{}
	msg.Init(*buffer_2)

	icmpКонсоль.MДрук(([]byte)("icmp:OnInternet"))
	icmpКонсоль.MUnsignedinteger16Друк(uint16(msg.Тип))
	icmpКонсоль.MДрук(([]byte)(":"))

	switch msg.Тип {
	case 0:
		icmpКонсоль.MДрук(([]byte)("ping response from "))
		break

	case 8:
		icmpКонсоль.MДрук(([]byte)("ping send "))
		msg.Тип = 0

		msg.checksum = 0
		msg.Множинаbuffer(buffer_2)
		msg.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(dataВказівник)), uint32(icmpРозмір))

		msg.Множинаbuffer(buffer_2)

		return true
		break
	}
	return false
}

func (поточний *TПротокол_керувальних_повідомлень_обʼєднаної_мережі) EchorequestНадіслати(ipМережаbyteorder uint32) bool {
	var протокол_керувальних_повідомлень_обʼєднаної_мережі TІнтернетКонтрольПовідомленняprotocolПовідомлення = TІнтернетКонтрольПовідомленняprotocolПовідомлення{}

	var памятьmanager = &TПамятьmanager{}
	var buffer_2 = (*TІнтернетКонтрольПовідомленняprotocolПовідомленняbuffer)(памятьmanager.Виділити_памʼять(1024))

	протокол_керувальних_повідомлень_обʼєднаної_мережі.Тип = 8
	протокол_керувальних_повідомлень_обʼєднаної_мережі.code = 0
	протокол_керувальних_повідомлень_обʼєднаної_мережі.data = 0x3713
	протокол_керувальних_повідомлень_обʼєднаної_мережі.checksum = 0
	протокол_керувальних_повідомлень_обʼєднаної_мережі.Множинаbuffer(buffer_2)
	протокол_керувальних_повідомлень_обʼєднаної_мережі.checksum = iphandler.Providerget().Checksum((*([4096]uint16))(Pointer(&buffer_2)), uint32(icmpРозмір))
	протокол_керувальних_повідомлень_обʼєднаної_мережі.Множинаbuffer(buffer_2)

	var dataВказівник uintptr = uintptr(Pointer(buffer_2))
	iphandler.Надіслати(ipМережаbyteorder, 0x01, dataВказівник, uint32(icmpРозмір))

	return false

}
