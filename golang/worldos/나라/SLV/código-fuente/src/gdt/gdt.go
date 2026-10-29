/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "consola"

const (
	Segnúcleocode	uint32	= 0x08
	Segnúcleodatos	uint32	= 0x10
	Segnúcleogs	uint32	= 0x18

	Segusuariocode	uint32	= 0x23
	Segusuariodatos	uint32	= 0x2B
	Segusuariogs	uint32	= 0x33
	SegtareaEstado	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitarBaja_2		uint16
	baseBaja_2		uint16
	baseAlta_2		uint8
	tipo_2			uint8
	banderasLimitarAlta	uint8
	baseveryAlta		uint8
}

func (propio_2 *TSegmentdescriptor) Init(base_2 uint32, limitar_2 uint32, tipo_2 uint8, banderas_2 uint8) {

	propio_2.baseBaja_2 = uint16(base_2 & 0xFFFF)
	propio_2.baseAlta_2 = uint8((base_2 >> 16) & 0xFF)
	propio_2.baseveryAlta = uint8((base_2 >> 24) & 0xFF)

	propio_2.limitarBaja_2 = uint16(limitar_2 & 0xFFFF)
	propio_2.banderasLimitarAlta = uint8((limitar_2 >> 24) & 0x0F)
	propio_2.banderasLimitarAlta |= (banderas_2 & 0xF0)

	propio_2.tipo_2 = tipo_2

}

type TShareddescriptorTabladatos struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var datos_2 TShareddescriptorTabladatos

type TShareddescriptorTabla struct {
}

func (propio_2 *TShareddescriptorTabla) Init() {

	var gdtentrada TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtDirección := uintptr(uint32(gdtdescriptor.GdtDirecciónBaja) |
		uint32(gdtdescriptor.GdtDirecciónAlta)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtTamaño+1) / Sizeof(gdtentrada))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtDirección,
	}))
	copy(datos_2.segmentdescriptor[:], oldgdt)

	datos_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	datos_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	datos_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destino_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseDirección := (*uint32)(Pointer(&destino_3[2]))
	(*baseDirección) = uint32(uintptr(Pointer(&datos_2)))

	tamaño_2 := (*uint16)(Pointer(&destino_3[0]))
	(*tamaño_2) = (uint16)((Sizeof(datos_2)))

	gdtfunc(uintptr(Pointer(&destino_3)))

	terminal := new(TConsola)
	terminal.MImprimirxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Imprimir(uint32(uintptr(Pointer(&datos_2.segmentdescriptor[3]))))

}
func (propio_2 *TShareddescriptorTabla) Establecerdescriptor(idx int, base_2 uint32, limitar_2 uint32, tipo_2 uint8, banderas_2 uint8) {
	datos_2.segmentdescriptor[idx].Init(base_2, limitar_2, tipo_2, banderas_2)
}

const (
	KcsÍndice	= 1
	KdsÍndice	= 2
	KgsÍndice	= 3

	Kcsselector	= KcsÍndice * 8
	Kdsselector	= KdsÍndice * 8
	Kgsselector	= KgsÍndice * 8

	Seggranocteto	= 0 << 7
	Seggran4kpágina	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segsistema	= 0 << 4
	Segnormal	= 1 << 4

	Segnoexec	= 0 << 3
	SegEjecutar	= 1 << 3

	Privnúcleo	= 0 << 5
	Privusuario	= 3 << 5

	Segbigmodo	= 1 << 6

	Presente	= 1 << 7

	Udesc32seg			= 1 << 0
	UdescÍndice			= 3 << 1
	Udescrxsolo			= 1 << 3
	UdescLimitarEntradapages	= 1 << 4
	UdescsegnotPresente		= 1 << 5
	Udescusable			= 1 << 6

	Gdtentrada	= 256
	TlsIniciar	= 16
)

var (
	gdtTabla	= [Gdtentrada]Gdtentrada_2{}
	gdtdescriptor	Gdtdescriptor
	gdtTablalen	= 0
)

type Gdtentrada_2 struct {
	limitarBaja		uint16
	baseBaja		uint16
	basemid			uint8
	acceso			uint8
	limitarAltayBanderas	uint8
	baseAlta		uint8
}

func (e *Gdtentrada_2) IsPresente() bool {
	return e.acceso&Presente != 0
}

func (e *Gdtentrada_2) Fill(base uint32, limitar uint32, acceso uint8, banderas uint8) {
	e.limitarAltayBanderas = uint8((limitar >> 16) & 0x000F)
	e.limitarAltayBanderas |= banderas
	e.acceso = acceso
	e.basemid = uint8(base >> 16)
	e.baseAlta = uint8(base >> 24)
	e.baseBaja = uint16(base & 0xFFFF)
	e.limitarBaja = uint16(limitar & 0x0000FFFF)
}

func (e *Gdtentrada_2) Limpiar() {
	e.limitarAltayBanderas = 0
	e.acceso = 0
	e.basemid = 0
	e.baseAlta = 0
	e.baseBaja = 0
	e.limitarBaja = 0

}

type Gdtdescriptor struct {
	GdtTamaño		uint16
	GdtDirecciónBaja	uint16
	GdtDirecciónAlta	uint16
}
type Usuariodescriptor struct {
	EntradaNúmero	uint32
	BaseDirección	uint32
	Limitar		uint32
	Banderas	uint8
}

func Establecertlssegment(índice uint32, descriptor *Usuariodescriptor, tabla []Gdtentrada_2) bool {
	if índice < TlsIniciar || índice > uint32(len(gdtTabla)) {
		return false
	}

	if descriptor.Banderas == Udescrxsolo|UdescsegnotPresente {

		tabla[índice].Limpiar()
		return true
	}

	banderas := uint8(Seggranocteto)
	if descriptor.Banderas&UdescLimitarEntradapages != 0 {
		banderas = Seggran4kpágina
	}
	acceso := uint8(Privusuario | Segnormal | Presente)
	if descriptor.Banderas&Udescrxsolo != 0 {
		acceso |= SegEjecutar
	} else {
		acceso |= Segw
	}
	if acceso&Segnormal != 0 {
		banderas |= Segbigmodo
	}

	tabla[índice].Fill(descriptor.BaseDirección, descriptor.Limitar, acceso, banderas)
	flushtlsTabla(tabla)

	return true
}

func flushtlsTabla(tabla []Gdtentrada_2) {
	copy(gdtTabla[TlsIniciar:], tabla[TlsIniciar:])
}
func FlushtlsTabla(tabla []TSegmentdescriptor) {
	copy(datos_2.segmentdescriptor[TlsIniciar:], tabla[TlsIniciar:])
}
