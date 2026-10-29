/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ماديذاكرة

import (
	. "مشترك"
	. "unsafe"
)

const (
	Bحظرالحجم	uint32	= 4 * 1024
	Bحظرperبايت	uint32	= 8
)

type multibootذاكرةخريطة struct {
	الحجم			uint32
	baseaddressمنخفض	uint64
	baseaddressعالية	uint64
	المدةمنخفض		uint64
	المدةعالية		uint64
	Tنوع			uint32
}

func Phymemتجريب() {
}

var ذاكرةoper Mذاكرةoper = Mذاكرةoper{}

type Pماديذاكرةمدير struct {
	ذاكرةالحجم	uint32
	usedحظر		uint32
	أقصىحظر		uint32
	ذاكرةمصفوفة	[]uint32
}

var (
	أقصىحظر				uint32	= 0
	ذاكرةمصفوفة			[]uint32
	grubmultibootذاكرةخريطةt	multibootذاكرةخريطة
)

func (نفسه *Pماديذاكرةمدير) Sتحديدbit(bit uint32) uint32 {
	نفسه.ذاكرةمصفوفة[bit/32] = نفسه.ذاكرةمصفوفة[bit/32] | (1 << (bit % 32))
	return نفسه.ذاكرةمصفوفة[bit/32]
}
func (نفسه *Pماديذاكرةمدير) Mعكس_بت_التخصيص(bit uint32) uint32 {
	نفسه.ذاكرةمصفوفة[bit/32] = نفسه.ذاكرةمصفوفة[bit/32] ^ (1 << (bit % 32))
	return نفسه.ذاكرةمصفوفة[bit/32]
}
func (نفسه *Pماديذاكرةمدير) Tتجريبbit(bit uint32) uint32 {
	ret := نفسه.ذاكرةمصفوفة[bit/32] & (1 << (bit % 32))
	return ret
}
func (نفسه *Pماديذاكرةمدير) Tالمجموعحظر() uint32 {
	return نفسه.أقصىحظر
}
func (نفسه *Pماديذاكرةمدير) Usedحظر() uint32 {
	return نفسه.usedحظر
}
func (نفسه *Pماديذاكرةمدير) Amountofذاكرة() uint32 {
	return نفسه.ذاكرةالحجم
}
func (نفسه *Pماديذاكرةمدير) Getbitmaspالحجم() uint32 {
	return نفسه.ذاكرةالحجم / Bحظرالحجم / Bحظرperبايت
}

func (نفسه *Pماديذاكرةمدير) Firstخالي() uint32 {
	for i := uint32(0); i < نفسه.Tالمجموعحظر(); i++ {
		if نفسه.ذاكرةمصفوفة[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				bit := uint32(1 << j)
				if (ذاكرةمصفوفة[i] & bit) == 0 {
					return i*4*8 + j
				}
			}
		}
	}
	return 0xffffffff
}
func (نفسه *Pماديذاكرةمدير) Firstخاليالحجم(الحجم uint32) uint32 {
	if الحجم == 0 {
		return 0xffffffff
	}
	if الحجم == 1 {
		return نفسه.Firstخالي()
	}

	for i := uint32(0); i < نفسه.Tالمجموعحظر(); i++ {
		if نفسه.ذاكرةمصفوفة[i] != 0xffffffff {
			for j := uint32(0); j < 32; j++ {
				var bit uint32 = 1 << j

				if نفسه.ذاكرةمصفوفة[j]&bit == 0 {
					var startingbit uint32 = i * 32
					startingbit += j

					var خالي uint32 = 0
					for count := uint32(0); count <= الحجم; count++ {
						if نفسه.Tتجريبbit(startingbit+count) == 0 {
							خالي++
						}

						if خالي == الحجم {
							return i*4*8 + j
						}
					}
				}
			}
		}
	}

	return 0xffffffff
}

func (نفسه *Pماديذاكرةمدير) Init(الحجم uint32, خريطة_التخصيص []uint32) {
	نفسه.ذاكرةالحجم = الحجم
	نفسه.ذاكرةمصفوفة = خريطة_التخصيص
	نفسه.أقصىحظر = الحجم / Bحظرالحجم
	نفسه.usedحظر = نفسه.أقصىحظر
	ذاكرةoper.Memتحديد(uintptr(Pointer(&نفسه.ذاكرةمصفوفة)), 0xFF, نفسه.usedحظر/Bحظرperبايت)
}
func (نفسه *Pماديذاكرةمدير) Allocateحظر() uintptr {
	if FreeBlocks() <= 0 {
		return 0
	}
	return 0
}
func (نفسه *Pماديذاكرةمدير) Pصفحةroundأعلى(address_2 uint32) uint32 {
	if (address_2 & 0xFFFFF000) != address_2 {
		address_2 = address_2 & 0xFFFFF000
		address_2 = address_2 + 0x1000
	}
	return address_2
}
func (نفسه *Pماديذاكرةمدير) Pصفحةroundأسفل(address_2 uint32) uint32 {
	return address_2 & 0xFFFFF000
}
