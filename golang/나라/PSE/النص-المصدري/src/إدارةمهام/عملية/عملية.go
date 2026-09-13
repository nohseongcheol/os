package عملية

import . "unsafe"
import . "أداة/قائمة"
import mem "ذاكرةمدير"
import . "إدارةمهام/خيطتنفيذ"
import . "إدارةمهام/مجدول"
import . "أداة"

const Procمستخدمheapالحجم = 1 * 1024 * 1024

type Pعملية struct {
	الهوية		uint32
	syscallالهوية	int
	Isمستخدمspace	bool
	arguments	*[]byte

	Tخيطتنفيذقائمة	Linkedقائمة
	Threads		*Linkedقائمة
	Fملفالاسم	[]byte

	Pصفحةدليلentry	uintptr
}

func (نفسه *Pعملية) Init(mem *mem.Tذاكرةمدير) {
	نفسه.Tخيطتنفيذقائمة = Linkedقائمة{}
	نفسه.Threads = &نفسه.Tخيطتنفيذقائمة
	نفسه.Threads.Init(mem)
}

type Pعمليةhelper struct {
	processes		Linkedقائمة
	mem			*mem.Tذاكرةمدير
	نواةصفحةدليلentry	uintptr
}

func (نفسه *Pعمليةhelper) Init(mem *mem.Tذاكرةمدير, نواةصفحةدليلentry uintptr) {
	نفسه.mem = mem
	نفسه.processes = Linkedقائمة{}
	نفسه.processes.Init(نفسه.mem)
	نفسه.نواةصفحةدليلentry = نواةصفحةدليلentry
}

func (نفسه *Pعمليةhelper) Cإنشاء(entrypoint func(), خيطتنفيذhelper *Tخيطتنفيذhelper, Pصفحةدليلentry uint32, isنواة bool) Pعملية {
	عملية := (*Pعملية)(نفسه.mem.Mتخصيص_الذاكرة(uint32(Sizeof(Pعملية{}))))
	if عملية == nil {
		return Pعملية{}
	}
	عملية.Init(نفسه.mem)
	عملية.الهوية = Allocateالهوية()
	عملية.Pصفحةدليلentry = uintptr(Pصفحةدليلentry)
	رئيسيخيطتنفيذ := خيطتنفيذhelper.Cإنشاءالمؤشرfromfunction(entrypoint, Pصفحةدليلentry, isنواة)
	if رئيسيخيطتنفيذ != nil {
		رئيسيخيطتنفيذ.Pالهوية = عملية.الهوية
		رئيسيخيطتنفيذ.Pأبالهوية = 0
		عملية.Threads.Mإضافة_إلى_نهاية_القائمة(uintptr(Pointer(رئيسيخيطتنفيذ)))
	}

	نفسه.processes.Mإضافة_إلى_نهاية_القائمة(uintptr(Pointer(عملية)))

	return *عملية
}

func (نفسه *Pعمليةhelper) Spawn(entrypoint func(), خيطتنفيذhelper *Tخيطتنفيذhelper, مجدول *Sمجدول, Pصفحةدليلentry uint32, isنواة bool) Pعملية {
	عملية := نفسه.Cإنشاء(entrypoint, خيطتنفيذhelper, Pصفحةدليلentry, isنواة)
	if عملية.Threads != nil && عملية.Threads.Sالحجم_2 > 0 {
		خيطتنفيذ := (*Tخيطتنفيذ)(عملية.Threads.Getat(0))
		if خيطتنفيذ != nil && مجدول != nil {
			مجدول.Aأضفخيطتنفيذ(خيطتنفيذ)
		}
	}
	return عملية
}

func (نفسه *Pعمليةhelper) نسخصفحةدليل(المصدرentry uintptr, المقصدentry uintptr) {
	المصدر_2 := Getunsignedinteger32مصفوفةfromالمؤشر(المصدرentry, 1024, 1024)
	المقصد_2 := Getunsignedinteger32مصفوفةfromالمؤشر(المقصدentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		المقصد_2[i] = المصدر_2[i]
	}
}
func (نفسه *Pعمليةhelper) Cإنشاءfromبيانات() Pعملية {
	عملية := Pعملية{}
	return عملية
}
