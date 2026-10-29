/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "konsoly"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	SegMpampiasacode	uint32	= 0x23
	SegMpampiasadata	uint32	= 0x2B
	SegMpampiasags		uint32	= 0x33
	Segtaskstate		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2	uint16
	baselow_2	uint16
	basehigh_2	uint8
	karazana	uint8
	sainalimithigh	uint8
	baseveryhigh	uint8
}

func (nytena_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, karazana uint8, saina_2 uint8) {

	nytena_2.baselow_2 = uint16(base_2 & 0xFFFF)
	nytena_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	nytena_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	nytena_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	nytena_2.sainalimithigh = uint8((limit_2 >> 24) & 0x0F)
	nytena_2.sainalimithigh |= (saina_2 & 0xF0)

	nytena_2.karazana = karazana

}

type TShareddescriptorFafanadata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorFafanadata

type TShareddescriptorFafana struct {
}

func (nytena_2 *TShareddescriptorFafana) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.GdtHabe+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	destination_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&destination_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	habe_2 := (*uint16)(Pointer(&destination_3[0]))
	(*habe_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TKonsoly)
	terminal.MAtontayxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32Atontay(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (nytena_2 *TShareddescriptorFafana) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, karazana uint8, saina_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, karazana, saina_2)
}

const (
	KcsFizahantakila	= 1
	KdsFizahantakila	= 2
	KgsFizahantakila	= 3

	Kcsselector	= KcsFizahantakila * 8
	Kdsselector	= KdsFizahantakila * 8
	Kgsselector	= KgsFizahantakila * 8

	Seggranbyte	= 0 << 7
	Seggran4kPEJY	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	SegRafitra	= 0 << 4
	SegTokonyhoizy	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	PrivMpampiasa	= 3 << 5

	SegbigFomba	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	UdescMpiaty		= 3 << 1
	Udescrxonly		= 1 << 3
	UdesclimitAnatypages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	TlsAtomboy	= 16
)

var (
	gdtFafana	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtFafanalen	= 0
)

type Gdtentry_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	access			uint8
	limithighandSaina	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.access&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, access uint8, saina uint8) {
	e.limithighandSaina = uint8((limit >> 16) & 0x000F)
	e.limithighandSaina |= saina
	e.access = access
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Foano() {
	e.limithighandSaina = 0
	e.access = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	GdtHabe		uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Mpampiasadescriptor struct {
	Entrynumber	uint32
	Baseaddress	uint32
	Limit		uint32
	Saina		uint8
}

func Settlssegment(fizahantakila uint32, descriptor *Mpampiasadescriptor, fafana []Gdtentry_2) bool {
	if fizahantakila < TlsAtomboy || fizahantakila > uint32(len(gdtFafana)) {
		return false
	}

	if descriptor.Saina == Udescrxonly|Udescsegnotpresent {

		fafana[fizahantakila].Foano()
		return true
	}

	saina := uint8(Seggranbyte)
	if descriptor.Saina&UdesclimitAnatypages != 0 {
		saina = Seggran4kPEJY
	}
	access := uint8(PrivMpampiasa | SegTokonyhoizy | Present)
	if descriptor.Saina&Udescrxonly != 0 {
		access |= Segexec
	} else {
		access |= Segw
	}
	if access&SegTokonyhoizy != 0 {
		saina |= SegbigFomba
	}

	fafana[fizahantakila].Fill(descriptor.Baseaddress, descriptor.Limit, access, saina)
	flushtlsFafana(fafana)

	return true
}

func flushtlsFafana(fafana []Gdtentry_2) {
	copy(gdtFafana[TlsAtomboy:], fafana[TlsAtomboy:])
}
func FlushtlsFafana(fafana []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[TlsAtomboy:], fafana[TlsAtomboy:])
}
