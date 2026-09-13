package gdt

import . "unsafe"
import "reflect"
import . "console"

const (
	Segkernelcode	uint32	= 0x08
	Segkerneldata	uint32	= 0x10
	Segkernelgs	uint32	= 0x18

	Segተጠቃሚcode	uint32	= 0x23
	Segተጠቃሚdata	uint32	= 0x2B
	Segተጠቃሚgs	uint32	= 0x33
	Segtaskሁኔታ	uint32	= 0x3B
)

func gdtfunc(x uintptr)
func getgdt() *Gdtdescriptor

var getdescriptor Gdtdescriptor

type TSegmentdescriptor struct {
	ገደብዝቅተኛ_2	uint16
	baseዝቅተኛ_2	uint16
	baseከፍተኛ_2	uint8
	አይነት		uint8
	ባንዲራዎችገደብከፍተኛ	uint8
	baseveryከፍተኛ	uint8
}

func (self_2 *TSegmentdescriptor) Init(base_2 uint32, ገደብ_2 uint32, አይነት uint8, ባንዲራዎች_2 uint8) {

	self_2.baseዝቅተኛ_2 = uint16(base_2 & 0xFFFF)
	self_2.baseከፍተኛ_2 = uint8((base_2 >> 16) & 0xFF)
	self_2.baseveryከፍተኛ = uint8((base_2 >> 24) & 0xFF)

	self_2.ገደብዝቅተኛ_2 = uint16(ገደብ_2 & 0xFFFF)
	self_2.ባንዲራዎችገደብከፍተኛ = uint8((ገደብ_2 >> 24) & 0x0F)
	self_2.ባንዲራዎችገደብከፍተኛ |= (ባንዲራዎች_2 & 0xF0)

	self_2.አይነት = አይነት

}

type TShareddescriptorሰንጠረዥdata struct {
	segmentdescriptor [255]TSegmentdescriptor
}

var data_2 TShareddescriptorሰንጠረዥdata

type TShareddescriptorሰንጠረዥ struct {
}

func (self_2 *TShareddescriptorሰንጠረዥ) Init() {

	var gdtentry TSegmentdescriptor

	gdtdescriptor = *getgdt()
	oldgdtaddress := uintptr(uint32(gdtdescriptor.Gdtaddressዝቅተኛ) |
		uint32(gdtdescriptor.Gdtaddressከፍተኛ)<<16)
	oldgdtlen := int(uintptr(gdtdescriptor.Gdtመጠን+1) / Sizeof(gdtentry))
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

	መጠን_2 := (*uint16)(Pointer(&destination_3[0]))
	(*መጠን_2) = (uint16)((Sizeof(data_2)))

	gdtfunc(uintptr(Pointer(&destination_3)))

	terminal := new(TConsole)
	terminal.Mማተሚያxy("gdt:", 1, 4)
	terminal.MUnsignedinteger32ማተሚያ(uint32(uintptr(Pointer(&data_2.segmentdescriptor[3]))))

}
func (self_2 *TShareddescriptorሰንጠረዥ) Setdescriptor(idx int, base_2 uint32, ገደብ_2 uint32, አይነት uint8, ባንዲራዎች_2 uint8) {
	data_2.segmentdescriptor[idx].Init(base_2, ገደብ_2, አይነት, ባንዲራዎች_2)
}

const (
	Kcsማውጫ	= 1
	Kdsማውጫ	= 2
	Kgsማውጫ	= 3

	Kcsselector	= Kcsማውጫ * 8
	Kdsselector	= Kdsማውጫ * 8
	Kgsselector	= Kgsማውጫ * 8

	Seggranbyte	= 0 << 7
	Seggran4kገጽ	= 1 << 7

	Segnorw	= 0 << 1
	Segr	= 1 << 1
	Segw	= 1 << 1

	Segስርአት	= 0 << 4
	Segመደበኛ	= 1 << 4

	Segnoexec	= 0 << 3
	Segexec		= 1 << 3

	Privkernel	= 0 << 5
	Privተጠቃሚ	= 3 << 5

	Segbigዘዴ	= 1 << 6

	Pአሁን	= 1 << 7

	Udesc32seg	= 1 << 0
	Udescይዞታዎች	= 3 << 1
	Udescrxonly	= 1 << 3
	Udescገደብውስጥገጾች	= 1 << 4
	Udescsegnotአሁን	= 1 << 5
	Udescusable	= 1 << 6

	Gdtentry	= 256
	Tlsማስጀመሪያ	= 16
)

var (
	gdtሰንጠረዥ	= [Gdtentry]Gdtentry_2{}
	gdtdescriptor	Gdtdescriptor
	gdtሰንጠረዥlen	= 0
)

type Gdtentry_2 struct {
	ገደብዝቅተኛ			uint16
	baseዝቅተኛ		uint16
	basemid			uint8
	መድረሻ			uint8
	ገደብከፍተኛandባንዲራዎች	uint8
	baseከፍተኛ		uint8
}

func (e *Gdtentry_2) Isአሁን() bool {
	return e.መድረሻ&Pአሁን != 0
}

func (e *Gdtentry_2) Fill(base uint32, ገደብ uint32, መድረሻ uint8, ባንዲራዎች uint8) {
	e.ገደብከፍተኛandባንዲራዎች = uint8((ገደብ >> 16) & 0x000F)
	e.ገደብከፍተኛandባንዲራዎች |= ባንዲራዎች
	e.መድረሻ = መድረሻ
	e.basemid = uint8(base >> 16)
	e.baseከፍተኛ = uint8(base >> 24)
	e.baseዝቅተኛ = uint16(base & 0xFFFF)
	e.ገደብዝቅተኛ = uint16(ገደብ & 0x0000FFFF)
}

func (e *Gdtentry_2) Cማጽጃ() {
	e.ገደብከፍተኛandባንዲራዎች = 0
	e.መድረሻ = 0
	e.basemid = 0
	e.baseከፍተኛ = 0
	e.baseዝቅተኛ = 0
	e.ገደብዝቅተኛ = 0

}

type Gdtdescriptor struct {
	Gdtመጠን		uint16
	Gdtaddressዝቅተኛ	uint16
	Gdtaddressከፍተኛ	uint16
}
type Uተጠቃሚdescriptor struct {
	Entryቁጥር	uint32
	Baseaddress	uint32
	Lገደብ		uint32
	Fባንዲራዎች		uint8
}

func Settlssegment(ማውጫ uint32, descriptor *Uተጠቃሚdescriptor, ሰንጠረዥ []Gdtentry_2) bool {
	if ማውጫ < Tlsማስጀመሪያ || ማውጫ > uint32(len(gdtሰንጠረዥ)) {
		return false
	}

	if descriptor.Fባንዲራዎች == Udescrxonly|Udescsegnotአሁን {

		ሰንጠረዥ[ማውጫ].Cማጽጃ()
		return true
	}

	ባንዲራዎች := uint8(Seggranbyte)
	if descriptor.Fባንዲራዎች&Udescገደብውስጥገጾች != 0 {
		ባንዲራዎች = Seggran4kገጽ
	}
	መድረሻ := uint8(Privተጠቃሚ | Segመደበኛ | Pአሁን)
	if descriptor.Fባንዲራዎች&Udescrxonly != 0 {
		መድረሻ |= Segexec
	} else {
		መድረሻ |= Segw
	}
	if መድረሻ&Segመደበኛ != 0 {
		ባንዲራዎች |= Segbigዘዴ
	}

	ሰንጠረዥ[ማውጫ].Fill(descriptor.Baseaddress, descriptor.Lገደብ, መድረሻ, ባንዲራዎች)
	flushtlsሰንጠረዥ(ሰንጠረዥ)

	return true
}

func flushtlsሰንጠረዥ(ሰንጠረዥ []Gdtentry_2) {
	copy(gdtሰንጠረዥ[Tlsማስጀመሪያ:], ሰንጠረዥ[Tlsማስጀመሪያ:])
}
func Flushtlsሰንጠረዥ(ሰንጠረዥ []TSegmentdescriptor) {
	copy(data_2.segmentdescriptor[Tlsማስጀመሪያ:], ሰንጠረዥ[Tlsማስጀመሪያ:])
}
