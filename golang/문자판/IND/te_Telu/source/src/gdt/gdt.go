package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	SEG_KERNEL_CODE	uint32	= 0x08
	SEG_KERNEL_DATA	uint32	= 0x10
	SEG_KERNEL_GS	uint32	= 0x18

	SEG_USER_CODE	uint32	= 0x23
	SEG_USER_DATA	uint32	= 0x2B
	SEG_USER_GS	uint32	= 0x33
	SEG_TASK_STATE	uint32	= 0x3B
)

func gdt_func(x uintptr)
func getGDT() *GdtDescriptor

var getDescriptor GdtDescriptor

type T조각설명자 struct {
	한도_낮은	uint16
	기준_낮은	uint16
	기준_높은	uint8
	유형	uint8
	표시들_한도_높은	uint8
	기준_매우높은	uint8
}

func (자신 *T조각설명자) Vప్రారంభించు(기준 uint32, 한도 uint32, 유형 uint8, 표시들 uint8) {

	자신.기준_낮은 = uint16(기준 & 0xFFFF)
	자신.기준_높은 = uint8((기준 >> 16) & 0xFF)
	자신.기준_매우높은 = uint8((기준 >> 24) & 0xFF)

	자신.한도_낮은 = uint16(한도 & 0xFFFF)
	자신.표시들_한도_높은 = uint8((한도 >> 24) & 0x0F)
	자신.표시들_한도_높은 |= (표시들 & 0xF0)

	자신.유형 = 유형

}

type T공용서술자테이블_자료 struct {
	조각설명자 [255]T조각설명자
}

var 자료 T공용서술자테이블_자료

type T공용서술자테이블 struct {
}

func (자신 *T공용서술자테이블) Vప్రారంభించు() {

	var gdtEntry T조각설명자

	gdtDescriptor = *getGDT()
	oldGdtAddr := uintptr(uint32(gdtDescriptor.GdtAddressLow) |
		uint32(gdtDescriptor.GdtAddressHigh)<<16)
	oldGdtLen := int(uintptr(gdtDescriptor.GdtSize+1) / Sizeof(gdtEntry))
	oldGdt := *(*[]T조각설명자)(Pointer(&reflect.SliceHeader{
		Len:	oldGdtLen,
		Cap:	oldGdtLen,
		Data:	oldGdtAddr,
	}))
	copy(자료.조각설명자[:], oldGdt)

	자료.조각설명자[4].Vప్రారంభించు(0, 64*1024*1024, 0xFA, 0xCF)
	자료.조각설명자[5].Vప్రారంభించు(0, 64*1024*1024, 0xF2, 0xCF)
	자료.조각설명자[6].Vప్రారంభించు(0x61f004, 0xffffff, 0xF2, 0x4F)

	목적 := [6]uint8{0, 0, 0, 0, 0, 0}
	기준주소 := (*uint32)(Pointer(&목적[2]))
	(*기준주소) = uint32(uintptr(Pointer(&자료)))

	크기 := (*uint16)(Pointer(&목적[0]))
	(*크기) = (uint16)((Sizeof(자료)))

	gdt_func(uintptr(Pointer(&목적)))

	단말기 := new(T콘솔)
	단말기.M출력XY("gdt:", 1, 4)
	단말기.MUint32출력(uint32(uintptr(Pointer(&자료.조각설명자[3]))))

}
func (자신 *T공용서술자테이블) SetDescriptor(idx int, 기준 uint32, 한도 uint32, 유형 uint8, 표시들 uint8) {
	자료.조각설명자[idx].Vప్రారంభించు(기준, 한도, 유형, 표시들)
}

const (
	KCS_INDEX	= 1
	KDS_INDEX	= 2
	KGS_INDEX	= 3

	KCS_SELECTOR	= KCS_INDEX * 8
	KDS_SELECTOR	= KDS_INDEX * 8
	KGS_SELECTOR	= KGS_INDEX * 8

	SEG_GRAN_BYTE	= 0 << 7
	SEG_GRAN_4K_PAGE	= 1 << 7

	SEG_NORW	= 0 << 1
	SEG_R	= 1 << 1
	SEG_W	= 1 << 1

	SEG_SYSTEM	= 0 << 4
	SEG_NORMAL	= 1 << 4

	SEG_NOEXEC	= 0 << 3
	SEG_EXEC		= 1 << 3

	PRIV_KERNEL	= 0 << 5
	PRIV_USER	= 3 << 5

	SEG_BIG_MODE	= 1 << 6

	PRESENT	= 1 << 7

	UDESC_32SEG		= 1 << 0
	UDESC_CONTENTS		= 3 << 1
	UDESC_RX_ONLY		= 1 << 3
	UDESC_LIMIT_IN_PAGES	= 1 << 4
	UDESC_SEG_NOT_PRESENT	= 1 << 5
	UDESC_USABLE		= 1 << 6

	GDT_ENTRIES	= 256
	TLS_START	= 16
)

var (
	gdtTable	= [GDT_ENTRIES]GdtEntry{}
	gdtDescriptor	GdtDescriptor
	gdtTableLen	= 0
)

type GdtEntry struct {
	limitLow		uint16
	baseLow			uint16
	baseMid			uint8
	access			uint8
	limitHighAndFlags	uint8
	baseHigh		uint8
}

func (e *GdtEntry) IsPresent() bool {
	return e.access&PRESENT != 0
}

func (e *GdtEntry) Fill(base uint32, limit uint32, access uint8, flags uint8) {
	e.limitHighAndFlags = uint8((limit >> 16) & 0x000F)
	e.limitHighAndFlags |= flags
	e.access = access
	e.baseMid = uint8(base >> 16)
	e.baseHigh = uint8(base >> 24)
	e.baseLow = uint16(base & 0xFFFF)
	e.limitLow = uint16(limit & 0x0000FFFF)
}

func (e *GdtEntry) Clear() {
	e.limitHighAndFlags = 0
	e.access = 0
	e.baseMid = 0
	e.baseHigh = 0
	e.baseLow = 0
	e.limitLow = 0

}

type GdtDescriptor struct {
	GdtSize		uint16
	GdtAddressLow	uint16
	GdtAddressHigh	uint16
}
type UserDesc struct {
	EntryNumber	uint32
	BaseAddr	uint32
	Limit		uint32
	Flags		uint8
}

func SetTlsSegment(index uint32, desc *UserDesc, table []GdtEntry) bool {
	if index < TLS_START || index > uint32(len(gdtTable)) {
		return false
	}

	if desc.Flags == UDESC_RX_ONLY|UDESC_SEG_NOT_PRESENT {

		table[index].Clear()
		return true
	}

	flags := uint8(SEG_GRAN_BYTE)
	if desc.Flags&UDESC_LIMIT_IN_PAGES != 0 {
		flags = SEG_GRAN_4K_PAGE
	}
	access := uint8(PRIV_USER | SEG_NORMAL | PRESENT)
	if desc.Flags&UDESC_RX_ONLY != 0 {
		access |= SEG_EXEC
	} else {
		access |= SEG_W
	}
	if access&SEG_NORMAL != 0 {
		flags |= SEG_BIG_MODE
	}

	table[index].Fill(desc.BaseAddr, desc.Limit, access, flags)
	flushTlsTable(table)

	return true
}

func flushTlsTable(table []GdtEntry) {
	copy(gdtTable[TLS_START:], table[TLS_START:])
}
func FlushTlsTable(table []T조각설명자) {
	copy(자료.조각설명자[TLS_START:], table[TLS_START:])
}
