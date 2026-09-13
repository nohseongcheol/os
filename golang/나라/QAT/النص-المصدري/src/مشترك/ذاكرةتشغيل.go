package مشترك

type Mذاكرةoper struct {
}

func (نفسه *Mذاكرةoper) Memتحديد(bufferالمؤشر uintptr, القيمة byte, الحجم uint32) uintptr {
	return bufferالمؤشر
}
func (نفسه *Mذاكرةoper) Memانقل(المقصدالمؤشر_2 uintptr, srcptr uintptr, الحجم uint32) uintptr {
	return المقصدالمؤشر_2
}

func (نفسه *Mذاكرةoper) Memنسخ(المقصدالمؤشر_2 uintptr, srcptr uintptr, الحجم uint32) uintptr {
	return المقصدالمؤشر_2
}
func (نفسه *Mذاكرةoper) Memcmp(المقصدالمؤشر_2 uintptr, srcptr uintptr, الحجم uint32) bool {
	return true
}
