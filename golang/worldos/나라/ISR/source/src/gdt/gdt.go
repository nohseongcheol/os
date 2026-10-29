/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	Segמשתמשcode	uint32	= 0x23
	Segמשתמשdata	uint32	= 0x2B
	Segמשתמשgs	uint32	= 0x33
	Segמשימהמצב	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitנמוך_2	uint16
	baseנמוך_2	uint16
	baseגבוהה_2	uint8
	סוג_2		uint8
	דגליםlimitגבוהה	uint8
	baseveryגבוהה	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, סוג_2 uint8, דגלים_2 uint8) {

	self_2.baseנמוך_2 = uint16(base_2 & 0xFFFF)
	self_2.baseגבוהה_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryגבוהה = uint8((base_2 >> 24) & 0xFF)

	self_2.limitנמוך_2 = uint16(limit_2 & 0xFFFF)
	self_2.דגליםlimitגבוהה = uint8((limit_2 >> 24) & 0x0F)
	self_2.דגליםlimitגבוהה |= (דגלים_2 & 0xF0)

	self_2.סוג_2 = סוג_2

}

type TShareddescriptortabledata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptortabledata

type TShareddescriptortable struct {
}

func (self_2 *TShareddescriptortable) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressנמוך) |
		uint32(gdtdescriptor.Gdtaddressגבוהה)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtגודל+1) / Sizeof(gdtentry))
	oldgdt := *(*[]TSegmentdescriptor)(Pointer(&reflect.SliceHeader{
		Len:	oldgdtlen,
		Cap:	oldgdtlen,
		Data:	oldgdtaddress,
	}))
	copy(data_2.segmentdescriptor[:], oldgdt)

	data_2.segmentdescriptor[4].Init(0, 64*1024*1024, 0xFA, 0xCF)
	data_2.segmentdescriptor[5].Init(0, 64*1024*1024, 0xF2, 0xCF)
	data_2.segmentdescriptor[6].Init(0x61f004, 0xffffff, 0xF2, 0x4F)

	יעד_3 := [6]uint8{0, 0, 0, 0, 0, 0}
	baseaddress := (*uint32)(Pointer(&יעד_3[2]))
	(*baseaddress) = uint32(uintptr(Pointer(&data_2)))

	גודל_2 := (*uint16)(Pointer(&יעד_3[0]))
	(*גודל_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&יעד_3)))

	terminal := new(TConsole)
	terminal.Mהדפסהxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32הדפסה(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptortable) Sקבעdescriptor(idx int, base_2 uint32, limit_2 uint32, סוג_2 uint8, דגלים_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, סוג_2, דגלים_2)
}

const (
	Kcsמפתח	= 1
	Kdsמפתח	= 2
	Kgsמפתח	= 3

	Kcsselector	= Kcsמפתח * 8
	Kdsselector	= Kdsמפתח * 8
	Kgsselector	= Kgsמפתח * 8

	Seggranbyte	= 0 << 7
	Seggran4kעמוד	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segמערכת	= 0 << 4
	Segרגיל		= 1 << 4

	Segnoexec	= 0 << 3
	Segהפעלה	= 1 << 3

	Privkernel	= 0 << 5
	Privמשתמש	= 3 << 5

	Segbigמצב	= 1 << 6

	Pנוכח	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescתכנים		= 3 << 1
	Udescrxonly		= 1 << 3
	Udesclimitנכנסpages	= 1 << 4
	Udescsegnotנוכח		= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsהתחלה	= 16
)

var (
	gdttable	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdttablelen	= 0
)

type Gdtentry_2 struct {
	limitנמוך		uint16
	baseנמוך		uint16
	basemid			uint8
	גישה			uint8
	limitגבוההandדגלים	uint8
	baseגבוהה		uint8
}

func (e *Gdtentry_2) Isנוכח() bool {
	return e.גישה&Pנוכח != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, גישה uint8, דגלים uint8) {
	e.limitגבוההandדגלים = uint8((limit >> 16) & 0x000F)
	e.limitגבוההandדגלים |= דגלים
	e.גישה = גישה
	e.basemid = uint8(base >> 16)
	e.baseגבוהה = uint8(base >> 24)
	e.baseנמוך = uint16(base & 0xFFFF)
	e.limitנמוך = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Cנקה() {
	e.limitגבוההandדגלים = 0
	e.גישה = 0
	e.basemid = 0
	e.baseגבוהה = 0
	e.baseנמוך = 0
	e.limitנמוך = 0

}

type Gdtdescriptor struct {
	Gdtגודל		uint16
	Gdtaddressנמוך	uint16
	Gdtaddressגבוהה	uint16
}
type Uמשתמשdescriptor struct {
	Entryמספר	uint32
	Baseaddress	uint32
	Limit		uint32
	Fדגלים		uint8
}

func Sקבעtlssegment(מפתח uint32, descriptor *Uמשתמשdescriptor, table []Gdtentry_2) bool {
	if מפתח < Tlsהתחלה || מפתח > uint32(len(gdttable)) {
		return false
	}

	if descriptor.Fדגלים == Udescrxonly|Udescsegnotנוכח {

		table[מפתח].Cנקה()
		return true
	}

	דגלים := uint8(Seggranbyte)
	if descriptor.Fדגלים&Udesclimitנכנסpages != 0 {
		דגלים = Seggran4kעמוד
	}
	גישה := uint8(Privמשתמש | Segרגיל | Pנוכח)
	if descriptor.Fדגלים&Udescrxonly != 0 {
		גישה |= Segהפעלה
	} else {
		גישה |= Segw
	}
	if גישה&Segרגיל != 0 {
		דגלים |= Segbigמצב
	}

	table[מפתח].Fill(descriptor.Baseaddress, descriptor.Limit, גישה, דגלים)
	flushtlstable(table)

	return true
}

func flushtlstable(table []Gdtentry_2) {
	copy(gdttable[Tlsהתחלה:], table[Tlsהתחלה:])
}
func Flushtlstable(table []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsהתחלה:], table[Tlsהתחלה:])
}
