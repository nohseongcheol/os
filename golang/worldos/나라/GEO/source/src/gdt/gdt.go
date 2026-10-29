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

	Segმომხმარებელიcode	uint32	= 0x23
	Segმომხმარებელიdata	uint32	= 0x2B
	Segმომხმარებელიgs	uint32	= 0x33
	Segtaskstate		uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	limitlow_2	uint16
	baselow_2	uint16
	basehigh_2	uint8
	ტიპი		uint8
	ალმებიlimithigh	uint8
	baseveryhigh	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, limit_2 uint32, ტიპი uint8, ალმები_2 uint8) {

	self_2.baselow_2 = uint16(base_2 & 0xFFFF)
	self_2.basehigh_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryhigh = uint8((base_2 >> 24) & 0xFF)

	self_2.limitlow_2 = uint16(limit_2 & 0xFFFF)
	self_2.ალმებიlimithigh = uint8((limit_2 >> 24) & 0x0F)
	self_2.ალმებიlimithigh |= (ალმები_2 & 0xF0)

	self_2.ტიპი = ტიპი

}

type TShareddescriptorცხრილიdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorცხრილიdata

type TShareddescriptorცხრილი struct {
}

func (self_2 *TShareddescriptorცხრილი) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddresslow) |
		uint32(gdtdescriptor.Gdtaddresshigh)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtზომა+1) / Sizeof(gdtentry))
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

	ზომა_2 := (*uint16)(Pointer(&destination_3[0]))
	(*ზომა_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.Mბეჭდვაxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32ბეჭდვა(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorცხრილი) Setdescriptor(idx int, base_2 uint32, limit_2 uint32, ტიპი uint8, ალმები_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, limit_2, ტიპი, ალმები_2)
}

const (
	Kcsინდექსი	= 1
	Kdsინდექსი	= 2
	Kgsინდექსი	= 3

	Kcsselector	= Kcsინდექსი * 8
	Kdsselector	= Kdsინდექსი * 8
	Kgsselector	= Kgsინდექსი * 8

	Seggranbyte	= 0 << 7
	Seggran4kგვერდი	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segსისტემა	= 0 << 4
	Segჩვეულებრივი	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel		= 0 << 5
	Privმომხმარებელი	= 3 << 5

	Segbigრეჟიმი	= 1 << 6

	Present	= 1 << 7

	Udesc32seg		= 1 << 0
	Udescშინაარსი		= 3 << 1
	Udescrxonly		= 1 << 3
	Udesclimitგადიდებაpages	= 1 << 4
	Udescsegnotpresent	= 1 << 5
	Udescusable		= 1 << 6

	Gdtentry	= 256
	Tlsstart	= 16
)

var (
	gdtცხრილი	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtცხრილიlen	= 0
)

type Gdtentry_2 struct {
	limitlow		uint16
	baselow			uint16
	basemid			uint8
	წვდომა			uint8
	limithighandალმები	uint8
	basehigh		uint8
}

func (e *Gdtentry_2) Ispresent() bool {
	return e.წვდომა&Present != 0
}

func (e *Gdtentry_2) Fill(base uint32, limit uint32, წვდომა uint8, ალმები uint8) {
	e.limithighandალმები = uint8((limit >> 16) & 0x000F)
	e.limithighandალმები |= ალმები
	e.წვდომა = წვდომა
	e.basemid = uint8(base >> 16)
	e.basehigh = uint8(base >> 24)
	e.baselow = uint16(base & 0xFFFF)
	e.limitlow = uint16(limit & 0x0000FFFF)
}

func (e *Gdtentry_2) Cგაწმენდა() {
	e.limithighandალმები = 0
	e.წვდომა = 0
	e.basemid = 0
	e.basehigh = 0
	e.baselow = 0
	e.limitlow = 0

}

type Gdtdescriptor struct {
	Gdtზომა		uint16
	Gdtaddresslow	uint16
	Gdtaddresshigh	uint16
}
type Uმომხმარებელიdescriptor struct {
	Entryრიცხვი	uint32
	Baseaddress	uint32
	Limit		uint32
	Fალმები		uint8
}

func Settlssegment(ინდექსი uint32, descriptor *Uმომხმარებელიdescriptor, ცხრილი []Gdtentry_2) bool {
	if ინდექსი < Tlsstart || ინდექსი > uint32(len(gdtცხრილი)) {
		return false
	}

	if descriptor.Fალმები == Udescrxonly|Udescsegnotpresent {

		ცხრილი[ინდექსი].Cგაწმენდა()
		return true
	}

	ალმები := uint8(Seggranbyte)
	if descriptor.Fალმები&Udesclimitგადიდებაpages != 0 {
		ალმები = Seggran4kგვერდი
	}
	წვდომა := uint8(Privმომხმარებელი | Segჩვეულებრივი | Present)
	if descriptor.Fალმები&Udescrxonly != 0 {
		წვდომა |= Segexec
	} else {
		წვდომა |= Segw
	}
	if წვდომა&Segჩვეულებრივი != 0 {
		ალმები |= Segbigრეჟიმი
	}

	ცხრილი[ინდექსი].Fill(descriptor.Baseaddress, descriptor.Limit, წვდომა, ალმები)
	flushtlsცხრილი(ცხრილი)

	return true
}

func flushtlsცხრილი(ცხრილი []Gdtentry_2) {
	copy(gdtცხრილი[Tlsstart:], ცხრილი[Tlsstart:])
}
func Flushtlsცხრილი(ცხრილი []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsstart:], ცხრილი[Tlsstart:])
}
