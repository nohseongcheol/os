package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "перарыванне"
import . "multitasking"
import . "tasking/tss"

import . "virtualПамяць"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/працэс"
import . "driver/driver"

import . "driver/клавіятура"
import . "driver/мыш"

import . "driver/ata"
import . "файлСістэма/msdospartition"
import . "файлСістэма/fat"

import . "файлСістэма/elf"

import . "сістэмаcall"

import . "памяцьmanager"
import . "pci"

func halt()

var iКлавіятураПадзеяhandler IКлавіятураПадзеяhandler

type TMyКлавіятураПадзеяhandler struct {
}

var myКлавіятураПадзеяhandler TMyКлавіятураПадзеяhandler
var клавіятураdriver TКлавіятураdriver
var мышdriver TМышdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var клавіятураconsole TConsole = TConsole{}

func (self *TMyКлавіятураПадзеяhandler) OnКлючУніз(ключ byte) {
	foo := [1]byte{' '}
	foo[0] = ключ

	клавіятураconsole.MДрукавацьБайтаўxy(foo[:], 1000, 1000)
}

func (self *TMyКлавіятураПадзеяhandler) OnКлючВышэй(ключ byte)	{}

var iМышПадзеяhandler IМышПадзеяhandler

type TMyМышПадзеяhandler struct {
}

var мышconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xПазіцыя int16 = 0
var yПазіцыя int16 = 0

func (self *TMyМышПадзеяhandler) OnМышУніз(кнопка int8) {
	buffer := []byte("x")
	мышconsole.MДрукавацьxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyМышПадзеяhandler) OnМышВышэй(кнопка int8)	{}
func (self *TMyМышПадзеяhandler) OnМышПеранесці(x int8, y int8) {

	xПазіцыя += int16(x)
	if xПазіцыя < 0 {
		xПазіцыя = 0
	}
	if xПазіцыя >= 80 {
		xПазіцыя = 79
	}

	yПазіцыя -= int16(y)

	if yПазіцыя < 0 {
		yПазіцыя = 0
	}
	if yПазіцыя >= 25 {
		yПазіцыя = 24
	}

	buffer := []byte(" ")
	мышconsole.MДрукавацьxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мышconsole.MДрукавацьxy(buffer, uint16(xПазіцыя), uint16(yПазіцыя))

	previousx = xПазіцыя
	previousy = yПазіцыя
}

var прыладаdescriptor TPeripheralcomponentinterconnectПрыладаdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Ongetdriver(прылада TPeripheralcomponentinterconnectПрыладаdescriptor) {
	if прылада.ВытворцаІДЭНТЫФІКАТАР == 0x1022 && прылада.ПрыладаІДЭНТЫФІКАТАР == 0x2000 {
		console.MДрукавацьxy([]byte("["), 0, 12)
		console.MДрукаваць(([]byte)("AMD am79c973"))
		console.MДрукаваць([]byte(":"))
		console.MUnsignedinteger16Друкаваць(прылада.ВытворцаІДЭНТЫФІКАТАР)
		console.MДрукаваць([]byte(":"))
		console.MUnsignedinteger16Друкаваць(прылада.ПрыладаІДЭНТЫФІКАТАР)
		console.MДрукаваць([]byte(":"))
		console.MUnsignedinteger16Друкаваць(uint16(прылада.Портbase))
		console.MДрукаваць([]byte(":"))
		console.MUnsignedinteger32Друкаваць(прылада.Перарыванне)

		console.MДрукаваць([]byte("]\n"))
		прыладаdescriptor = прылада
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectПрыладаdescriptor {
	return прыладаdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Друкавацьstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MДрукаваць(str)
}

func GetФайлПамер(назвафайла []byte) uint32 {
	var ata0s = TДадатковаТэхналогіяattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабліца{}
	partition.Чытаннеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var памер uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], назвафайла)
	ata0s.Flush()

	return памер
}

func ЧытаннеФайл(назвафайла []byte, data []byte) {
	var ata0s = TДадатковаТэхналогіяattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабліца{}
	partition.Чытаннеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Чытанне(&ata0s, partition.Mbr.Primarypartition[0], назвафайла, data)

	ata0s.Flush()
}
func Загрузкаelf() {

	var ata0s = TДадатковаТэхналогіяattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабліца{}
	partition.Чытаннеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var назвафайла []byte = ([]byte)("TEST")
	var памер uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], назвафайла)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Чытанне(&ata0s, partition.Mbr.Primarypartition[0], назвафайла, data)

	elf := Elf{}

	elf.Parse(data[:памер], 0x4f00000)

}

var задачаconsole TConsole = TConsole{}

func TФункцыя1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func задачаa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func задачаb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func задачаc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func задачаd()

func задачаd0() {
	esi := getesi()
	for {

		SysДрукавацьunsignedinteger32(esi)

	}
}

func задачаd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func уводПадзеяЗадача() {
	for {
		ПрацэсpendingКлавіятураevents()
		ПрацэсpendingМышevents()
		halt()
	}
}

func memorytest(y int) {
	памяцьmanager := &TПамяцьmanager{}
	allocated := uint32(uintptr(памяцьmanager.Malloc(1024)))
	console.MUnsignedinteger32Друкавацьxy(allocated, 10, uint16(y))
	if y == 11 {
		памяцьmanager.Вольна(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Паўзаloop()
func Перачытацьcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Вызначанаcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetФункцыяНазва(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcНазва = runtime.FuncForPC(address).Name()
	var funcБайтаў []byte = []byte(funcНазва)

	задачаconsole.MДрукавацьxy(funcБайтаў, 1, 5)
	задачаconsole.MДрукаваць(([]byte)(":"))
	задачаconsole.MUnsignedinteger32Друкаваць(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	задачаconsole.MДрукавацьunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(СтаронкаКаталогentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MДрукаваць("\n=== BLR BOOT ===\n")

	console.MДрукавацьunsignedinteger32(uint32(СтаронкаКаталогentry), 0, 2)
	console.MДрукавацьunsignedinteger32(uint32(СтаронкаКаталогentry), 10, 2)
	console.MДрукавацьunsignedinteger32(uint32(stacktop), 0, 3)
	console.MДрукавацьunsignedinteger32(uint32(stackbottom), 10, 3)

	памяцьmanager := &TПамяцьmanager{}
	памяцьmanager.Init(0, MaxqueueПамер)

	paging := &Paging{}
	paging.Init(СтаронкаКаталогentry, 0x500000, памяцьmanager)
	paging.SharedПамяцьregion()

	Вызначанаcr3(uint32(СтаронкаКаталогentry))
	Enablepaging()

	shareddescriptorТабліца := &TShareddescriptorТабліца{}
	shareddescriptorТабліца.Init()

	console.MДрукаваць("esp:")

	esp := getesp()
	console.MUnsignedinteger32Друкаваць(uint32(esp))

	tls := gettls()
	console.MДрукаваць(([]byte)("tls:"))
	console.MUnsignedinteger32Друкаваць(tls)

	tss.Устанавіць(shareddescriptorТабліца, 7, Segkerneldata, esp)

	VirtПраверка()

	cr3 := Перачытацьcr3()
	console.MДрукаваць(([]byte)(":cr3:"))
	console.MUnsignedinteger32Друкаваць(cr3)

	cr0 := Getcr0()
	console.MДрукаваць(([]byte)(":cr0:"))
	console.MUnsignedinteger32Друкаваць(cr0)

	cr4 := Getcr4()
	console.MДрукаваць(([]byte)(":cr4:"))
	console.MUnsignedinteger32Друкаваць(cr4)

	задачаmanager_2 := &TЗадачаmanager{}
	задачаmanager_2.Init()

	Перарываннеmanager := &TПерарываннеmanager{}
	Перарываннеmanager.Init(0x20, shareddescriptorТабліца, задачаmanager_2)

	paging.Старонкаfault(Перарываннеmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(памяцьmanager)

	працэсhelper := Працэсhelper{}
	працэсhelper.Init(памяцьmanager, СтаронкаКаталогentry)

	sche := &Scheduler{}
	sche.Init(Перарываннеmanager, памяцьmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Перарываннеmanager)

	працэсhelper.Spawn(задачаa, threadhelper, sche, uint32(СтаронкаКаталогentry), true)
	працэсhelper.Spawn(задачаb, threadhelper, sche, uint32(СтаронкаКаталогentry), true)
	працэсhelper.Spawn(задачаc, threadhelper, sche, uint32(СтаронкаКаталогentry), true)
	працэсhelper.Spawn(задачаd1, threadhelper, sche, uint32(СтаронкаКаталогentry), true)
	працэсhelper.Spawn(уводПадзеяЗадача, threadhelper, sche, uint32(СтаронкаКаталогentry), true)

	var памер uint32

	var linkerФайл []byte = ([]byte)("LINKER")
	памер = GetФайлПамер(linkerФайл)
	linkeraddress := памяцьmanager.Malloc(памер)
	linkerdata := GetБайтаўfromПаказальнік(uintptr(linkeraddress), int(памер), int(памер))
	ЧытаннеФайл(linkerФайл, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(СтаронкаКаталогentry))

	спасылкаmap := Спасылкаmap{}
	спасылкаmap.Init(памяцьmanager)

	var ліб1Файл []byte = ([]byte)("LIB1")
	памер = GetФайлПамер(ліб1Файл)

	ліб1address := памяцьmanager.Malloc(памер)
	ліб1data := GetБайтаўfromПаказальнік(uintptr(ліб1address), int(памер), int(памер))
	ЧытаннеФайл(ліб1Файл, ліб1data)

	ліб1elf := Elf{}
	ліб1elf.Parse(ліб1data[:], uint32(СтаронкаКаталогentry))
	памяцьmanager.Вольна(ліб1address)

	спасылкаmap.Append_to_list(uintptr(ліб1elf.Данамічна))

	var ліб2Файл []byte = ([]byte)("LIB2")
	памер = GetФайлПамер(ліб2Файл)

	ліб2address := памяцьmanager.Malloc(памер)
	ліб2data := GetБайтаўfromПаказальнік(uintptr(ліб2address), int(памер), int(памер))
	ЧытаннеФайл(ліб2Файл, ліб2data)

	ліб2elf := Elf{}
	ліб2elf.Parse(ліб2data[:], uint32(СтаронкаКаталогentry))
	памяцьmanager.Вольна(ліб2address)

	спасылкаmap.Append_to_list(uintptr(ліб2elf.Данамічна))

	лібСпасылкаmap := спасылкаmap.Clone()
	спасылкаmapaddress := uint32(uintptr(Pointer(лібСпасылкаmap.First)))

	ліб1got := Getunsignedinteger32МасіўfromПаказальнік(uintptr(ліб1elf.Got), 4, 4)
	ліб1got[1] = спасылкаmapaddress
	ліб1got[2] = 0x4000000

	ліб2got := Getunsignedinteger32МасіўfromПаказальнік(uintptr(ліб2elf.Got), 4, 4)
	ліб2got[1] = спасылкаmapaddress
	ліб2got[2] = 0x4000000

	console.MДрукавацьxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Друкаваць(ліб1elf.Got)
	console.MДрукаваць(":")
	console.MUnsignedinteger32Друкаваць(ліб1elf.Данамічна)

	console.MДрукавацьxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Друкаваць(ліб2elf.Got)
	console.MДрукаваць(":")
	console.MUnsignedinteger32Друкаваць(ліб2elf.Данамічна)

	var карыстальнік1Файл []byte = ([]byte)("USER1")
	памер = GetФайлПамер(карыстальнік1Файл)
	карыстальнік1address := памяцьmanager.Malloc(памер)
	карыстальнік1data := GetБайтаўfromПаказальнік(uintptr(карыстальнік1address), int(памер), int(памер))
	ЧытаннеФайл(карыстальнік1Файл, карыстальнік1data)

	elf2 := Elf{}

	карыстальнік1entry := elf2.Getentry(карыстальнік1data)
	elf2.Parse(карыстальнік1data[:], uint32(СтаронкаКаталогentry+0x1000))
	агульныяoffsetТабліца := elf2.Got

	PЗначэнне1Спасылкаmap := спасылкаmap.Clone()
	PЗначэнне1Спасылкаmap.Append_to_list(uintptr(elf2.Данамічна))

	памяцьmanager.Вольна(карыстальнік1address)

	var code1Паказальнік *uintptr
	var func1val func()

	code1Паказальнік = (*uintptr)(памяцьmanager.Malloc(4))
	*code1Паказальнік = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Паказальнік))

	proc2 := працэсhelper.Spawn(func1val, threadhelper, sche, uint32(СтаронкаКаталогentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ЦПСтан.Ecx = карыстальнік1entry
	thr2.ЦПСтан.Edx = агульныяoffsetТабліца
	thr2.ЦПСтан.Esi = uint32(uintptr(Pointer(PЗначэнне1Спасылкаmap.First)))

	console.MДрукавацьxy("user1: ", 1, 10)
	console.MUnsignedinteger32Друкаваць(elf2.Got)

	var карыстальнік2Файл []byte = ([]byte)("USER2")
	памер = GetФайлПамер(карыстальнік2Файл)
	карыстальнік2address := памяцьmanager.Malloc(памер)
	карыстальнік2data := GetБайтаўfromПаказальнік(uintptr(карыстальнік2address), int(памер), int(памер))
	ЧытаннеФайл(карыстальнік2Файл, карыстальнік2data)

	elf3 := Elf{}

	карыстальнік2entry := elf3.Getentry(карыстальнік2data)
	elf3.Parse(карыстальнік2data[:], uint32(СтаронкаКаталогentry+0x2000))
	агульныяoffsetТабліца = elf3.Got

	PЗначэнне2Спасылкаmap := спасылкаmap.Clone()
	PЗначэнне2Спасылкаmap.Append_to_list(uintptr(elf3.Данамічна))

	памяцьmanager.Вольна(карыстальнік2address)

	var code2Паказальнік *uintptr
	var func2val func()

	code2Паказальнік = (*uintptr)(памяцьmanager.Malloc(4))
	*code2Паказальнік = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Паказальнік))

	proc3 := працэсhelper.Spawn(func2val, threadhelper, sche, uint32(СтаронкаКаталогentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ЦПСтан.Ecx = карыстальнік2entry
	thr3.ЦПСтан.Edx = агульныяoffsetТабліца
	thr3.ЦПСтан.Esi = uint32(uintptr(Pointer(PЗначэнне2Спасылкаmap.First)))

	console.MДрукавацьxy("user2: ", 1, 11)
	console.MUnsignedinteger32Друкаваць(thr3.ЦПСтан.Esi)

	лібСпасылкаmap.Друкаваць(1, 11)

	var карыстальнік3Файл []byte = ([]byte)("USER3")
	памер = GetФайлПамер(карыстальнік3Файл)
	карыстальнік3address := памяцьmanager.Malloc(памер)
	карыстальнік3data := GetБайтаўfromПаказальнік(uintptr(карыстальнік3address), int(памер), int(памер))
	ЧытаннеФайл(карыстальнік3Файл, карыстальнік3data)

	elf4 := Elf{}

	карыстальнік3entry := elf4.Getentry(карыстальнік3data)
	elf4.Parse(карыстальнік3data[:], uint32(СтаронкаКаталогentry+0x3000))
	агульныяoffsetТабліца = elf4.Got

	PЗначэнне3Спасылкаmap := спасылкаmap.Clone()
	PЗначэнне3Спасылкаmap.Append_to_list(uintptr(elf4.Данамічна))

	памяцьmanager.Вольна(карыстальнік3address)

	var code3Паказальнік *uintptr
	var func3val func()

	code3Паказальнік = (*uintptr)(памяцьmanager.Malloc(4))
	*code3Паказальнік = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Паказальнік))

	proc4 := працэсhelper.Spawn(func3val, threadhelper, sche, uint32(СтаронкаКаталогentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ЦПСтан.Ecx = карыстальнік3entry
	thr4.ЦПСтан.Edx = агульныяoffsetТабліца
	thr4.ЦПСтан.Esi = uint32(uintptr(Pointer(PЗначэнне3Спасылкаmap.First)))

	працэсhelper.Spawn(TФункцыя1, threadhelper, sche, uint32(СтаронкаКаталогentry+0x4000), true)

	iКлавіятураПадзеяhandler = &myКлавіятураПадзеяhandler
	клавіятураdriver.Initdriver(Перарываннеmanager, iКлавіятураПадзеяhandler)

	мышdriver.Initdriver(Перарываннеmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Вылучыцьdriver(&Drivermanager, Перарываннеmanager)
	прыладаdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Уключаны(true)
	Перарываннеmanager.Актыўна()

	for {
		halt()
	}

}
