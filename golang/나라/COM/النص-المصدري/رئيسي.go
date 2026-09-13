package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "أداة"
import . "gdt"
import . "طرفية"
import . "مقاطعة"
import . "متعددإدارةمهام"
import . "إدارةمهام/tss"

import . "افتراضيذاكرة"
import . "إدارةصفحات"
import . "إدارةمهام/خيطتنفيذ"
import . "إدارةمهام/مجدول"
import . "إدارةمهام/عملية"
import . "مشغل/مشغل"

import . "مشغل/لوحةمفاتيح"
import . "مشغل/جهاز_تأشير"

import . "مشغل/ata"
import . "ملفنظام/msdosتجزئة"
import . "ملفنظام/fat"

import . "ملفنظام/صيغة_التنفيذ_والربط"

import . "نظامنداء"

import . "ذاكرةمدير"
import . "pci"

func halt()

var iلوحةمفاتيححدثhandler Iلوحةمفاتيححدثhandler

type TMyلوحةمفاتيححدثhandler struct {
}

var myلوحةمفاتيححدثhandler TMyلوحةمفاتيححدثhandler
var لوحةمفاتيحمشغل Tلوحةمفاتيحمشغل
var فأرةمشغل Tفأرةمشغل
var pciمتحكم TPeripheralcomponentinterconnectمتحكم

var لوحةمفاتيحطرفية Tطرفية = Tطرفية{}

func (نفسه *TMyلوحةمفاتيححدثhandler) Oعندمفتاحأسفل(مفتاح byte) {
	foo := [1]byte{' '}
	foo[0] = مفتاح

	لوحةمفاتيحطرفية.Mاطبعبايتxy(foo[:], 1000, 1000)
}

func (نفسه *TMyلوحةمفاتيححدثhandler) Oعندمفتاحأعلى(مفتاح byte)	{}

var iفأرةحدثhandler Iفأرةحدثhandler

type TMyفأرةحدثhandler struct {
}

var فأرةطرفية Tطرفية = Tطرفية{}
var previousx int16 = 0
var previousy int16 = 0
var xالموضع int16 = 0
var yالموضع int16 = 0

func (نفسه *TMyفأرةحدثhandler) Oعندفأرةأسفل(زر int8) {
	buffer := []byte("x")
	فأرةطرفية.Mاطبعxy(buffer, uint16(previousx), uint16(previousy))
}
func (نفسه *TMyفأرةحدثhandler) Oعندفأرةأعلى(زر int8)	{}
func (نفسه *TMyفأرةحدثhandler) Oعندفأرةانقل(x int8, y int8) {

	xالموضع += int16(x)
	if xالموضع < 0 {
		xالموضع = 0
	}
	if xالموضع >= 80 {
		xالموضع = 79
	}

	yالموضع -= int16(y)

	if yالموضع < 0 {
		yالموضع = 0
	}
	if yالموضع >= 25 {
		yالموضع = 24
	}

	buffer := []byte(" ")
	فأرةطرفية.Mاطبعxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	فأرةطرفية.Mاطبعxy(buffer, uint16(xالموضع), uint16(yالموضع))

	previousx = xالموضع
	previousy = yالموضع
}

var الجهازdescriptor TPeripheralcomponentinterconnectالجهازdescriptor
var ipciمتحكمhandler Ipciمتحكمhandler

type TMypciمتحكمhandler struct {
}

var طرفية Tطرفية = Tطرفية{}
var مشغلcount uint16 = 0

func (نفسه TMypciمتحكمhandler) Oعندgetمشغل(الجهاز TPeripheralcomponentinterconnectالجهازdescriptor) {
	if الجهاز.Vبائعالهوية == 0x1022 && الجهاز.Dالجهازالهوية == 0x2000 {
		طرفية.Mاطبعxy([]byte("["), 0, 12)
		طرفية.Mاطبع(([]byte)("AMD am79c973"))
		طرفية.Mاطبع([]byte(":"))
		طرفية.MUnsignedinteger16اطبع(الجهاز.Vبائعالهوية)
		طرفية.Mاطبع([]byte(":"))
		طرفية.MUnsignedinteger16اطبع(الجهاز.Dالجهازالهوية)
		طرفية.Mاطبع([]byte(":"))
		طرفية.MUnsignedinteger16اطبع(uint16(الجهاز.Pمنفذbase))
		طرفية.Mاطبع([]byte(":"))
		طرفية.MUnsignedinteger32اطبع(الجهاز.Iمقاطعة)

		طرفية.Mاطبع([]byte("]\n"))
		الجهازdescriptor = الجهاز
		مشغلcount++
	}
}
func (نفسه TMypciمتحكمhandler) Getمشغل() TPeripheralcomponentinterconnectالجهازdescriptor {
	return الجهازdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pاطبعstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	طرفية.Mاطبع(str)
}

func Getملفالحجم(اسمالملف []byte) uint32 {
	var ata0s = Tمتقدمالتقنيةattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	تجزئة := Tmsdosتجزئةجدول{}
	تجزئة.Rقراءةتجزئة(&ata0s)

	bios := Tمعلمات_نظام_الملفات32{}

	var الحجم uint32 = bios.Len(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف)
	ata0s.Flush()

	return الحجم
}

func Mقراءة_الملف(اسمالملف []byte, بيانات []byte) {
	var ata0s = Tمتقدمالتقنيةattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	تجزئة := Tmsdosتجزئةجدول{}
	تجزئة.Rقراءةتجزئة(&ata0s)

	bios := Tمعلمات_نظام_الملفات32{}
	bios.Rقراءة(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف, بيانات)

	ata0s.Flush()
}
func Lتحميلelf() {

	var ata0s = Tمتقدمالتقنيةattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	تجزئة := Tmsdosتجزئةجدول{}
	تجزئة.Rقراءةتجزئة(&ata0s)

	bios := Tمعلمات_نظام_الملفات32{}

	var اسمالملف []byte = ([]byte)("TEST")
	var الحجم uint32 = bios.Len(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف)
	var بياناتbuffer [100 * 1024]byte
	var بيانات []byte = بياناتbuffer[:]
	bios.Rقراءة(&ata0s, تجزئة.Mbr.Primaryتجزئة[0], اسمالملف, بيانات)

	صيغة_التنفيذ_والربط := Elf{}

	صيغة_التنفيذ_والربط.Parse(بيانات[:الحجم], 0x4f00000)

}

var مهمةطرفية Tطرفية = Tطرفية{}

func TFunction1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func مهمةa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func مهمةb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func مهمةc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func مهمةd()

func مهمةd0() {
	esi := getesi()
	for {

		Sysاطبعunsignedinteger32(esi)

	}
}

func مهمةd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func دخلحدثمهمة() {
	for {
		Pعمليةمعلقلوحةمفاتيحأحداث()
		Pعمليةمعلقفأرةأحداث()
		halt()
	}
}

func memorytest(y int) {
	ذاكرةمدير := &Tذاكرةمدير{}
	allocated := uint32(uintptr(ذاكرةمدير.Mتخصيص_الذاكرة(1024)))
	طرفية.MUnsignedinteger32اطبعxy(allocated, 10, uint16(y))
	if y == 11 {
		ذاكرةمدير.Fخالي(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pألبثloop()
func Rأعدالتحميلcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sتحديدcr3(cr3 uint32)
func Getcr4() uint32
func Enableإدارةصفحات()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getfunctionالاسم(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcالاسم = runtime.FuncForPC(address).Name()
	var funcبايت []byte = []byte(funcالاسم)

	مهمةطرفية.Mاطبعxy(funcبايت, 1, 5)
	مهمةطرفية.Mاطبع(([]byte)(":"))
	مهمةطرفية.MUnsignedinteger32اطبع(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	مهمةطرفية.Mاطبعunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pصفحةدليلentry uintptr, stacktop uintptr, stackbottom uintptr) {

	Mتسلسليالسجلinit()
	طرفية.Mاطبع("\n=== COM BOOT ===\n")

	طرفية.Mاطبعunsignedinteger32(uint32(Pصفحةدليلentry), 0, 2)
	طرفية.Mاطبعunsignedinteger32(uint32(Pصفحةدليلentry), 10, 2)
	طرفية.Mاطبعunsignedinteger32(uint32(stacktop), 0, 3)
	طرفية.Mاطبعunsignedinteger32(uint32(stackbottom), 10, 3)

	ذاكرةمدير := &Tذاكرةمدير{}
	ذاكرةمدير.Init(0, Mأقصىطابورالحجم)

	إدارةصفحات := &Pإدارةصفحات{}
	إدارةصفحات.Init(Pصفحةدليلentry, 0x500000, ذاكرةمدير)
	إدارةصفحات.Sharedذاكرةregion()

	Sتحديدcr3(uint32(Pصفحةدليلentry))
	Enableإدارةصفحات()

	shareddescriptorجدول := &TShareddescriptorجدول{}
	shareddescriptorجدول.Init()

	طرفية.Mاطبع("esp:")

	esp := getesp()
	طرفية.MUnsignedinteger32اطبع(uint32(esp))

	tls := gettls()
	طرفية.Mاطبع(([]byte)("tls:"))
	طرفية.MUnsignedinteger32اطبع(tls)

	tss.Install(shareddescriptorجدول, 7, Segنواةبيانات, esp)

	Virtتجريب()

	cr3 := Rأعدالتحميلcr3()
	طرفية.Mاطبع(([]byte)(":cr3:"))
	طرفية.MUnsignedinteger32اطبع(cr3)

	cr0 := Getcr0()
	طرفية.Mاطبع(([]byte)(":cr0:"))
	طرفية.MUnsignedinteger32اطبع(cr0)

	cr4 := Getcr4()
	طرفية.Mاطبع(([]byte)(":cr4:"))
	طرفية.MUnsignedinteger32اطبع(cr4)

	مهمةمدير_2 := &Tمهمةمدير{}
	مهمةمدير_2.Init()

	Iمقاطعةمدير := &Tمقاطعةمدير{}
	Iمقاطعةمدير.Init(0x20, shareddescriptorجدول, مهمةمدير_2)

	إدارةصفحات.Pصفحةخلل(Iمقاطعةمدير)

	Dمشغلمدير := Tمشغلمدير{}
	Dمشغلمدير.Init()

	خيطتنفيذhelper := &Tخيطتنفيذhelper{}
	خيطتنفيذhelper.Init(ذاكرةمدير)

	عمليةhelper := Pعمليةhelper{}
	عمليةhelper.Init(ذاكرةمدير, Pصفحةدليلentry)

	sche := &Sمجدول{}
	sche.Init(Iمقاطعةمدير, ذاكرةمدير, tss)

	sysنداء := &TSyscall{}
	sysنداء.Init(Iمقاطعةمدير)

	عمليةhelper.Spawn(مهمةa, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry), true)
	عمليةhelper.Spawn(مهمةb, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry), true)
	عمليةhelper.Spawn(مهمةc, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry), true)
	عمليةhelper.Spawn(مهمةd1, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry), true)
	عمليةhelper.Spawn(دخلحدثمهمة, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry), true)

	var الحجم uint32

	var linkerملف []byte = ([]byte)("LINKER")
	الحجم = Getملفالحجم(linkerملف)
	linkeraddress := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	linkerبيانات := Getبايتfromالمؤشر(uintptr(linkeraddress), int(الحجم), int(الحجم))
	Mقراءة_الملف(linkerملف, linkerبيانات)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerبيانات)
	elf0.Parse(linkerبيانات[:], uint32(Pصفحةدليلentry))

	رابطخريطة := Lرابطخريطة{}
	رابطخريطة.Init(ذاكرةمدير)

	var lib1ملف []byte = ([]byte)("LIB1")
	الحجم = Getملفالحجم(lib1ملف)

	lib1address := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	lib1بيانات := Getبايتfromالمؤشر(uintptr(lib1address), int(الحجم), int(الحجم))
	Mقراءة_الملف(lib1ملف, lib1بيانات)

	lib1elf := Elf{}
	lib1elf.Parse(lib1بيانات[:], uint32(Pصفحةدليلentry))
	ذاكرةمدير.Fخالي(lib1address)

	رابطخريطة.Mإضافة_إلى_نهاية_القائمة(uintptr(lib1elf.Dynamic))

	var lib2ملف []byte = ([]byte)("LIB2")
	الحجم = Getملفالحجم(lib2ملف)

	lib2address := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	lib2بيانات := Getبايتfromالمؤشر(uintptr(lib2address), int(الحجم), int(الحجم))
	Mقراءة_الملف(lib2ملف, lib2بيانات)

	lib2elf := Elf{}
	lib2elf.Parse(lib2بيانات[:], uint32(Pصفحةدليلentry))
	ذاكرةمدير.Fخالي(lib2address)

	رابطخريطة.Mإضافة_إلى_نهاية_القائمة(uintptr(lib2elf.Dynamic))

	libرابطخريطة := رابطخريطة.Clone()
	رابطخريطةaddress := uint32(uintptr(Pointer(libرابطخريطة.First)))

	lib1got := Getunsignedinteger32مصفوفةfromالمؤشر(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = رابطخريطةaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32مصفوفةfromالمؤشر(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = رابطخريطةaddress
	lib2got[2] = 0x4000000

	طرفية.Mاطبعxy("lib1: ", 1, 8)
	طرفية.MUnsignedinteger32اطبع(lib1elf.Got)
	طرفية.Mاطبع(":")
	طرفية.MUnsignedinteger32اطبع(lib1elf.Dynamic)

	طرفية.Mاطبعxy("lib2: ", 1, 9)
	طرفية.MUnsignedinteger32اطبع(lib2elf.Got)
	طرفية.Mاطبع(":")
	طرفية.MUnsignedinteger32اطبع(lib2elf.Dynamic)

	var مستخدم1ملف []byte = ([]byte)("USER1")
	الحجم = Getملفالحجم(مستخدم1ملف)
	مستخدم1address := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	مستخدم1بيانات := Getبايتfromالمؤشر(uintptr(مستخدم1address), int(الحجم), int(الحجم))
	Mقراءة_الملف(مستخدم1ملف, مستخدم1بيانات)

	elf2 := Elf{}

	مستخدم1entry := elf2.Getentry(مستخدم1بيانات)
	elf2.Parse(مستخدم1بيانات[:], uint32(Pصفحةدليلentry+0x1000))
	الاختصارالعامoffsetجدول := elf2.Got

	Pالقيمة1رابطخريطة := رابطخريطة.Clone()
	Pالقيمة1رابطخريطة.Mإضافة_إلى_نهاية_القائمة(uintptr(elf2.Dynamic))

	ذاكرةمدير.Fخالي(مستخدم1address)

	var code1المؤشر *uintptr
	var func1val func()

	code1المؤشر = (*uintptr)(ذاكرةمدير.Mتخصيص_الذاكرة(4))
	*code1المؤشر = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1المؤشر))

	proc2 := عمليةhelper.Spawn(func1val, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry+0x1000), false)
	thr2 := (*Tخيطتنفيذ)(proc2.Threads.Getat(0))
	thr2.Cالمعالجالحالة.Ecx = مستخدم1entry
	thr2.Cالمعالجالحالة.Edx = الاختصارالعامoffsetجدول
	thr2.Cالمعالجالحالة.Esi = uint32(uintptr(Pointer(Pالقيمة1رابطخريطة.First)))

	طرفية.Mاطبعxy("user1: ", 1, 10)
	طرفية.MUnsignedinteger32اطبع(elf2.Got)

	var مستخدم2ملف []byte = ([]byte)("USER2")
	الحجم = Getملفالحجم(مستخدم2ملف)
	مستخدم2address := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	مستخدم2بيانات := Getبايتfromالمؤشر(uintptr(مستخدم2address), int(الحجم), int(الحجم))
	Mقراءة_الملف(مستخدم2ملف, مستخدم2بيانات)

	elf3 := Elf{}

	مستخدم2entry := elf3.Getentry(مستخدم2بيانات)
	elf3.Parse(مستخدم2بيانات[:], uint32(Pصفحةدليلentry+0x2000))
	الاختصارالعامoffsetجدول = elf3.Got

	Pالقيمة2رابطخريطة := رابطخريطة.Clone()
	Pالقيمة2رابطخريطة.Mإضافة_إلى_نهاية_القائمة(uintptr(elf3.Dynamic))

	ذاكرةمدير.Fخالي(مستخدم2address)

	var code2المؤشر *uintptr
	var func2val func()

	code2المؤشر = (*uintptr)(ذاكرةمدير.Mتخصيص_الذاكرة(4))
	*code2المؤشر = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2المؤشر))

	proc3 := عمليةhelper.Spawn(func2val, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry+0x2000), false)
	thr3 := (*Tخيطتنفيذ)(proc3.Threads.Getat(0))
	thr3.Cالمعالجالحالة.Ecx = مستخدم2entry
	thr3.Cالمعالجالحالة.Edx = الاختصارالعامoffsetجدول
	thr3.Cالمعالجالحالة.Esi = uint32(uintptr(Pointer(Pالقيمة2رابطخريطة.First)))

	طرفية.Mاطبعxy("user2: ", 1, 11)
	طرفية.MUnsignedinteger32اطبع(thr3.Cالمعالجالحالة.Esi)

	libرابطخريطة.Pاطبع(1, 11)

	var مستخدم3ملف []byte = ([]byte)("USER3")
	الحجم = Getملفالحجم(مستخدم3ملف)
	مستخدم3address := ذاكرةمدير.Mتخصيص_الذاكرة(الحجم)
	مستخدم3بيانات := Getبايتfromالمؤشر(uintptr(مستخدم3address), int(الحجم), int(الحجم))
	Mقراءة_الملف(مستخدم3ملف, مستخدم3بيانات)

	elf4 := Elf{}

	مستخدم3entry := elf4.Getentry(مستخدم3بيانات)
	elf4.Parse(مستخدم3بيانات[:], uint32(Pصفحةدليلentry+0x3000))
	الاختصارالعامoffsetجدول = elf4.Got

	Pالقيمة3رابطخريطة := رابطخريطة.Clone()
	Pالقيمة3رابطخريطة.Mإضافة_إلى_نهاية_القائمة(uintptr(elf4.Dynamic))

	ذاكرةمدير.Fخالي(مستخدم3address)

	var code3المؤشر *uintptr
	var func3val func()

	code3المؤشر = (*uintptr)(ذاكرةمدير.Mتخصيص_الذاكرة(4))
	*code3المؤشر = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3المؤشر))

	proc4 := عمليةhelper.Spawn(func3val, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry+0x3000), false)
	thr4 := (*Tخيطتنفيذ)(proc4.Threads.Getat(0))
	thr4.Cالمعالجالحالة.Ecx = مستخدم3entry
	thr4.Cالمعالجالحالة.Edx = الاختصارالعامoffsetجدول
	thr4.Cالمعالجالحالة.Esi = uint32(uintptr(Pointer(Pالقيمة3رابطخريطة.First)))

	عمليةhelper.Spawn(TFunction1, خيطتنفيذhelper, sche, uint32(Pصفحةدليلentry+0x4000), true)

	iلوحةمفاتيححدثhandler = &myلوحةمفاتيححدثhandler
	لوحةمفاتيحمشغل.Initمشغل(Iمقاطعةمدير, iلوحةمفاتيححدثhandler)

	فأرةمشغل.Initمشغل(Iمقاطعةمدير, nil)

	mypciمتحكمhandler := TMypciمتحكمhandler{}
	pciمتحكم.Init(mypciمتحكمhandler)
	pciمتحكم.Sإختيارمشغل(&Dمشغلمدير, Iمقاطعةمدير)
	الجهازdescriptor = mypciمتحكمhandler.Getمشغل()

	sche.Eمفعل(true)
	Iمقاطعةمدير.Aنشط()

	for {
		halt()
	}

}
