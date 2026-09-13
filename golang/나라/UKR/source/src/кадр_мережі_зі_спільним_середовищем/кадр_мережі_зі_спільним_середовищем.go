package кадр_мережі_зі_спільним_середовищем

import . "консоль"

import . "amdam79c973"
import . "unsafe"
import . "util"

var ethernetКонсоль TКонсоль = TКонсоль{}

type TEthernetБлокheaderbuffer struct {
	призначенняmacbe	[6]byte
	джерелоmacbe		[6]byte
	ethernetТипbe		[2]byte
}

var блокheaderРозмір int = 14

type TЗаголовок_кадру_мережі_зі_спільним_середовищем struct {
	призначенняmacbe	uint64
	джерелоmacbe		uint64
	ethernetТипbe		uint16
}

func (поточний *TЗаголовок_кадру_мережі_зі_спільним_середовищем) Init(buffer_2 TEthernetБлокheaderbuffer) {
	поточний.призначенняmacbe = (Масивтоunsignedinteger48(buffer_2.призначенняmacbe))
	поточний.джерелоmacbe = (Масивтоunsignedinteger48(buffer_2.джерелоmacbe))
	поточний.ethernetТипbe = (Масивтоunsignedinteger16(buffer_2.ethernetТипbe))

}
func (поточний *TЗаголовок_кадру_мережі_зі_спільним_середовищем) Множинаbuffer(buffer_2 *TEthernetБлокheaderbuffer) {
	buffer_2.призначенняmacbe = Unsignedinteger48тоМасив(Unsignedinteger48r(поточний.призначенняmacbe))
	buffer_2.джерелоmacbe = Unsignedinteger48тоМасив(Unsignedinteger48r(поточний.джерелоmacbe))
	buffer_2.ethernetТипbe = Unsignedinteger16тоМасив(Unsignedinteger16r(поточний.ethernetТипbe))
}

type IEthernetБлокhandler interface {
	Init(backend TПостачальник_кадрів_мережі_зі_спільним_середовищем)
	Множинаhandler(handler IEthernetБлокhandler, ethernetТип uint16)
	EthernetБлокreceivewhen(dataВказівник uintptr, розмір int) bool
	Надіслати(призначенняmacbe uint64, dataВказівник uintptr, розмір uint32)
	БлокНадіслати(призначенняmacbe uint64, ethernetТипbe uint16, dataВказівник uintptr, розмір uint32)
	Providerget() TПостачальник_кадрів_мережі_зі_спільним_середовищем
	GetmacАдреса() uint64
	GetipАдреса() uint64
}

type TEthernetБлокhandler struct {
}

var блок TЗаголовок_кадру_мережі_зі_спільним_середовищем
var Backend TПостачальник_кадрів_мережі_зі_спільним_середовищем
var handler_2 [65535]IEthernetБлокhandler
var efhandler *TEthernetБлокhandler = nil

func (поточний *TEthernetБлокhandler) Init(backend TПостачальник_кадрів_мережі_зі_спільним_середовищем) {
	Backend = backend
}

func (поточний *TEthernetБлокhandler) Множинаhandler(handler IEthernetБлокhandler, pethernetТип uint16) {
	handler_2[pethernetТип] = handler
}
func (поточний *TEthernetБлокhandler) Множинаbackend(backend TПостачальник_кадрів_мережі_зі_спільним_середовищем) {
	Backend = backend
}
func (поточний *TEthernetБлокhandler) Getbackend() TПостачальник_кадрів_мережі_зі_спільним_середовищем {
	return Backend
}
func (поточний *TEthernetБлокhandler) EthernetБлокreceivewhen(dataВказівник uintptr, розмір int) bool {
	ethernetКонсоль.MДрук(([]byte)("OnEtherFrameReceived"))
	return false
}
func (поточний *TEthernetБлокhandler) Надіслати(призначенняmacbe uint64, dataВказівник uintptr, розмір uint32) {
	Backend.БлокНадіслати(призначенняmacbe, блок.ethernetТипbe, dataВказівник, розмір)
}
func (поточний *TEthernetБлокhandler) БлокНадіслати(призначенняmacbe uint64, ethernetТипbe uint16, dataВказівник uintptr, розмір uint32) {
	Backend.БлокНадіслати(призначенняmacbe, ethernetТипbe, dataВказівник, розмір)
}
func (поточний *TEthernetБлокhandler) GetmacАдреса() uint64 {
	return Backend.GetmacАдреса()
}
func (поточний *TEthernetБлокhandler) GetipАдреса() uint64 {
	return Backend.GetipАдреса()
}
func (поточний *TEthernetБлокhandler) Providerget() TПостачальник_кадрів_мережі_зі_спільним_середовищем {
	return Backend
}

type TEthernetБлокrawdatahandler struct {
	TRawdatahandler
}

var provider TПостачальник_кадрів_мережі_зі_спільним_середовищем

func (поточний *TEthernetБлокrawdatahandler) Init(pprovider TПостачальник_кадрів_мережі_зі_спільним_середовищем, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (поточний *TEthernetБлокrawdatahandler) Увімкненоrawdatareceive(dataВказівник uintptr, розмір int) bool {
	return provider.Увімкненоrawdatareceive(dataВказівник, розмір)
}
func (поточний *TEthernetБлокrawdatahandler) Надіслати(dataВказівник uintptr, розмір uint32) {
	provider.Надіслати(dataВказівник, розмір)
}
func (поточний *TEthernetБлокrawdatahandler) GetmacАдреса() uint64 {
	return provider.GetmacАдреса()
}
func (поточний *TEthernetБлокrawdatahandler) GetipАдреса() uint64 {
	return provider.GetipАдреса()
}
func (поточний *TEthernetБлокrawdatahandler) Providerget() TПостачальник_кадрів_мережі_зі_спільним_середовищем {
	return provider
}

type TПостачальник_кадрів_мережі_зі_спільним_середовищем struct {
	мережаКарткові	Tamdam79c973
	handler_2	[65565]IEthernetБлокhandler
}

func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) Init(backend Tamdam79c973) {

	поточний.мережаКарткові = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		поточний.handler_2[i] = nil
	}
}

var відлік uint16 = 0

func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) Увімкненоrawdatareceive(dataВказівник uintptr, розмір int) bool {

	var buffer_2 *TEthernetБлокheaderbuffer = (*TEthernetБлокheaderbuffer)(Pointer(dataВказівник))
	var блок TЗаголовок_кадру_мережі_зі_спільним_середовищем = TЗаголовок_кадру_мережі_зі_спільним_середовищем{}
	блок.Init(*buffer_2)
	var reply bool = false

	if блок.призначенняmacbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(блок.призначенняmacbe) == поточний.GetmacАдреса() {
		if handler_2[блок.ethernetТипbe] != nil {
			ethernetКонсоль.MДрук(([]byte)("provider\n"))

			var посилання_на_адресу uintptr = uintptr(Pointer(dataВказівник)) + uintptr(блокheaderРозмір)
			reply = handler_2[блок.ethernetТипbe].EthernetБлокreceivewhen(посилання_на_адресу, розмір-блокheaderРозмір)

		}
	}

	if reply {
		блок.призначенняmacbe = блок.джерелоmacbe
		блок.джерелоmacbe = Unsignedinteger48r(поточний.GetmacАдреса())
		блок.Множинаbuffer(buffer_2)

	}

	ethernetКонсоль.MДрукxy(([]byte)("spro["), 0, 1)
	ethernetКонсоль.MUnsignedinteger64Друк(блок.джерелоmacbe)
	ethernetКонсоль.MДрук(([]byte)(":"))
	ethernetКонсоль.MUnsignedinteger64Друк(блок.призначенняmacbe)
	ethernetКонсоль.MДрук(([]byte)(":]["))
	ethernetКонсоль.MUnsignedinteger64Друк(поточний.GetmacАдреса())
	ethernetКонсоль.MДрук(([]byte)(":"))
	ethernetКонсоль.MUnsignedinteger16Друк(блок.ethernetТипbe)
	ethernetКонсоль.MДрук(([]byte)("]"))

	return reply

}
func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) Надіслати(dataВказівник uintptr, розмір uint32) {
	поточний.мережаКарткові.Надіслати(dataВказівник, розмір)
}
func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) БлокНадіслати(призначенняmacbe uint64, ethernetТипbe uint16, dataВказівник uintptr, розмір uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *TEthernetБлокheaderbuffer = (*TEthernetБлокheaderbuffer)(Pointer(&buffer2_2))

	var блок TЗаголовок_кадру_мережі_зі_спільним_середовищем = TЗаголовок_кадру_мережі_зі_спільним_середовищем{}
	блок.Init(*buffer_2)

	блок.призначенняmacbe = Unsignedinteger48r(призначенняmacbe)
	блок.джерелоmacbe = Unsignedinteger48r(поточний.мережаКарткові.GetmacАдреса())
	блок.ethernetТипbe = Unsignedinteger16r(ethernetТипbe)

	блок.Множинаbuffer(buffer_2)
	var джерело_2 [4096]byte = *(*([4096]byte))(Pointer(dataВказівник))

	var i uint32 = 0
	for i = 0; i < розмір; i++ {
		buffer2_2[uint32(блокheaderРозмір)+i] = джерело_2[i]

	}

	var посилання_на_адресу uintptr = uintptr(Pointer(&buffer2_2))

	поточний.мережаКарткові.Надіслати(посилання_на_адресу, розмір+uint32(блокheaderРозмір))

}
func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) GetmacАдреса() uint64 {
	return поточний.мережаКарткові.GetmacАдреса()
}
func (поточний *TПостачальник_кадрів_мережі_зі_спільним_середовищем) GetipАдреса() uint64 {
	return поточний.мережаКарткові.GetipАдреса()
}
