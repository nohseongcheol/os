/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package صيغة_التنفيذ_والربط

import . "unsafe"
import . "طرفية"

import mem "ذاكرةمدير"

type Lرابط struct {
	Dynamic		uintptr
	Previous	*Lرابط
	Nالتالي		*Lرابط
}
type Lرابطخريطة struct {
	First	*Lرابط
	Lالأخير	*Lرابط

	Sالحجم_2	int

	mem	*mem.Tذاكرةمدير
}

func (نفسه *Lرابطخريطة) Init(mem *mem.Tذاكرةمدير) {
	نفسه.mem = mem
}
func (نفسه *Lرابطخريطة) Clone() Lرابطخريطة {
	var رابطخريطة Lرابطخريطة

	رابطخريطة.Init(نفسه.mem)

	Lرابط := نفسه.First

	for ; Lرابط != nil; Lرابط = Lرابط.Nالتالي {
		رابطخريطة.Mإضافة_إلى_نهاية_القائمة(Lرابط.Dynamic)
	}
	return رابطخريطة
}
func (نفسه *Lرابطخريطة) Mإضافة_إلى_بداية_القائمة(Dynamic uintptr) {
	جديدرابط := (*Lرابط)(نفسه.mem.Mتخصيص_الذاكرة(uint32(Sizeof(Lرابط{}))))
	جديدرابط.Dynamic = Dynamic
	جديدرابط.Nالتالي = نفسه.First
	نفسه.First = جديدرابط
	نفسه.Sالحجم_2++

	if نفسه.First.Nالتالي == nil {
		نفسه.Lالأخير = نفسه.First
	}
}
func (نفسه *Lرابطخريطة) Mإضافة_إلى_نهاية_القائمة(Dynamic uintptr) {
	if Dynamic == 0 {
		return
	}

	if نفسه.Sالحجم_2 == 0 {
		نفسه.Mإضافة_إلى_بداية_القائمة(Dynamic)
	} else {
		جديدرابط := (*Lرابط)(نفسه.mem.Mتخصيص_الذاكرة(uint32(Sizeof(Lرابط{}))))
		جديدرابط.Dynamic = Dynamic
		جديدرابط.Nالتالي = nil
		نفسه.Lالأخير.Nالتالي = جديدرابط
		نفسه.Lالأخير = جديدرابط
		نفسه.Sالحجم_2++
	}
}
func (نفسه *Lرابطخريطة) Pاطبع(x uint16, y uint16) {
	Lرابط := نفسه.First
	طرفية_2 := Tطرفية{}
	طرفية_2.Mاطبعxy("linkmap : ", x, y)
	for ; Lرابط != nil; Lرابط = Lرابط.Nالتالي {
		طرفية_2.MUnsignedinteger32اطبع(uint32(Lرابط.Dynamic))
		طرفية_2.Mاطبع("+")

	}
}
