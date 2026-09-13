package مؤقت

import . "unsafe"

import . "مقاطعة"
import . "طرفية"

type Iمؤقتحدثhandler interface {
	Oعندtick()
}

var iمؤقتحدثhandler Iمؤقتحدثhandler

type Tالافتراضيمؤقتحدثhandler struct {
}

func (نفسه *Tالافتراضيمؤقتحدثhandler) Oعندtick() {
}

type Tمؤقتمشغل struct {
	Tمقاطعةhandler
}

var مقاطعةhandler func(*Tمؤقتمشغل, uint32) uint32

func (نفسه *Tمؤقتمشغل) Init(مدير *Tمقاطعةمدير, لوحةمفاتيححدثhandler Iمؤقتحدثhandler) {
	iمؤقتحدثhandler = &Tالافتراضيمؤقتحدثhandler{}
	if لوحةمفاتيححدثhandler != nil {
		iمؤقتحدثhandler = لوحةمفاتيححدثhandler
	}

	مقاطعةhandler = (*Tمؤقتمشغل).Hالتعاملمقاطعة
	var address uintptr
	address = uintptr(Pointer(&مقاطعةhandler))

	نفسه.Tمقاطعةhandler.Init(0x20, uintptr(Pointer(مدير)), address)

}

var tickcount uint32 = 0

func (نفسه *Tمؤقتمشغل) Hالتعاملمقاطعة(esp uint32) uint32 {
	طرفية_2 := Tطرفية{}
	طرفية_2.MUnsignedinteger32اطبعxy(tickcount, 3, 1)
	tickcount++

	return esp
}
