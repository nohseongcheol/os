package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "конзола"
import . "ометање"
import . "multitasking"
import . "tasking/tss"

import . "виртуелноМеморија"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/процес"
import . "driver/driver"

import . "driver/тастатура"
import . "driver/миш"

import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "датотекаСистем/fat"

import . "датотекаСистем/elf"

import . "системcall"

import . "меморијаmanager"
import . "pci"

func halt()

var iТастатураДогађајhandler IТастатураДогађајhandler

type TMyТастатураДогађајhandler struct {
}

var myТастатураДогађајhandler TMyТастатураДогађајhandler
var тастатураdriver TТастатураdriver
var мишdriver TМишdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var тастатураКонзола TКонзола = TКонзола{}

func (исти *TMyТастатураДогађајhandler) НаКључНиже(кључ byte) {
	foo := [1]byte{' '}
	foo[0] = кључ

	тастатураКонзола.MШтампајБајтоваxy(foo[:], 1000, 1000)
}

func (исти *TMyТастатураДогађајhandler) НаКључГоре(кључ byte)	{}

var iМишДогађајhandler IМишДогађајhandler

type TMyМишДогађајhandler struct {
}

var мишКонзола TКонзола = TКонзола{}
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (исти *TMyМишДогађајhandler) НаМишНиже(дугме int8) {
	buffer := []byte("x")
	мишКонзола.MШтампајxy(buffer, uint16(previousx), uint16(previousy))
}
func (исти *TMyМишДогађајhandler) НаМишГоре(дугме int8)	{}
func (исти *TMyМишДогађајhandler) НаМишПремести(x int8, y int8) {

	xПоложај += int16(x)
	if xПоложај < 0 {
		xПоложај = 0
	}
	if xПоложај >= 80 {
		xПоложај = 79
	}

	yПоложај -= int16(y)

	if yПоложај < 0 {
		yПоложај = 0
	}
	if yПоложај >= 25 {
		yПоложај = 24
	}

	buffer := []byte(" ")
	мишКонзола.MШтампајxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мишКонзола.MШтампајxy(buffer, uint16(xПоложај), uint16(yПоложај))

	previousx = xПоложај
	previousy = yПоложај
}

var уређајdescriptor TPeripheralcomponentinterconnectУређајdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var конзола TКонзола = TКонзола{}
var drivercount uint16 = 0

func (исти TMypcicontrollerhandler) Наgetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor) {
	if уређај.ПроизвођачИБ == 0x1022 && уређај.УређајИБ == 0x2000 {
		конзола.MШтампајxy([]byte("["), 0, 12)
		конзола.MШтампај(([]byte)("AMD am79c973"))
		конзола.MШтампај([]byte(":"))
		конзола.MUnsignedinteger16Штампај(уређај.ПроизвођачИБ)
		конзола.MШтампај([]byte(":"))
		конзола.MUnsignedinteger16Штампај(уређај.УређајИБ)
		конзола.MШтампај([]byte(":"))
		конзола.MUnsignedinteger16Штампај(uint16(уређај.Портbase))
		конзола.MШтампај([]byte(":"))
		конзола.MUnsignedinteger32Штампај(уређај.Ометање)

		конзола.MШтампај([]byte("]\n"))
		уређајdescriptor = уређај
		drivercount++
	}
}
func (исти TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectУређајdescriptor {
	return уређајdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Штампајstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	конзола.MШтампај(str)
}

func GetДатотекаВеличина(датотека []byte) uint32 {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var величина uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], датотека)
	ata0s.Flush()

	return величина
}

func ЧитањеДатотека(датотека []byte, data []byte) {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Читање(&ata0s, partition.Mbr.Primarypartition[0], датотека, data)

	ata0s.Flush()
}
func Оптерећењеelf() {

	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterБлок32{}

	var датотека []byte = ([]byte)("TEST")
	var величина uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], датотека)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Читање(&ata0s, partition.Mbr.Primarypartition[0], датотека, data)

	elf := Elf{}

	elf.Parse(data[:величина], 0x4f00000)

}

var задатакКонзола TКонзола = TКонзола{}

func TФункција1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func задатакa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func задатакb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func задатакc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func задатакd()

func задатакd0() {
	esi := getesi()
	for {

		SysШтампајunsignedinteger32(esi)

	}
}

func задатакd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func улазДогађајЗадатак() {
	for {
		ПроцесpendingТастатураДогађаји()
		ПроцесpendingМишДогађаји()
		halt()
	}
}

func memorytest(y int) {
	меморијаmanager := &TМеморијаmanager{}
	allocated := uint32(uintptr(меморијаmanager.Malloc(1024)))
	конзола.MUnsignedinteger32Штампајxy(allocated, 10, uint16(y))
	if y == 11 {
		меморијаmanager.Слободно(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Паузаloop()
func Освежиcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Скупcr3(cr3 uint32)
func Getcr4() uint32
func Укљученоpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetфункцијаНазив(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcНазив = runtime.FuncForPC(address).Name()
	var funcБајтова []byte = []byte(funcНазив)

	задатакКонзола.MШтампајxy(funcБајтова, 1, 5)
	задатакКонзола.MШтампај(([]byte)(":"))
	задатакКонзола.MUnsignedinteger32Штампај(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	задатакКонзола.MШтампајunsignedinteger32(cr0, 2, 1)
}

var tss *Tssунос = &Tssунос{}

func KKernelEntry(СТРАНАДиректоријумунос uintptr, stacktop uintptr, stackbottom uintptr) {

	MСеријскиДневникinit()
	конзола.MШтампај("\n=== SRB BOOT ===\n")

	конзола.MШтампајunsignedinteger32(uint32(СТРАНАДиректоријумунос), 0, 2)
	конзола.MШтампајunsignedinteger32(uint32(СТРАНАДиректоријумунос), 10, 2)
	конзола.MШтампајunsignedinteger32(uint32(stacktop), 0, 3)
	конзола.MШтампајunsignedinteger32(uint32(stackbottom), 10, 3)

	меморијаmanager := &TМеморијаmanager{}
	меморијаmanager.Init(0, МаксqueueВеличина)

	paging := &Paging{}
	paging.Init(СТРАНАДиректоријумунос, 0x500000, меморијаmanager)
	paging.SharedМеморијаregion()

	Скупcr3(uint32(СТРАНАДиректоријумунос))
	Укљученоpaging()

	shareddescriptorТабела := &TShareddescriptorТабела{}
	shareddescriptorТабела.Init()

	конзола.MШтампај("esp:")

	esp := getesp()
	конзола.MUnsignedinteger32Штампај(uint32(esp))

	tls := gettls()
	конзола.MШтампај(([]byte)("tls:"))
	конзола.MUnsignedinteger32Штампај(tls)

	tss.Инсталирај(shareddescriptorТабела, 7, Segkerneldata, esp)

	VirtТест()

	cr3 := Освежиcr3()
	конзола.MШтампај(([]byte)(":cr3:"))
	конзола.MUnsignedinteger32Штампај(cr3)

	cr0 := Getcr0()
	конзола.MШтампај(([]byte)(":cr0:"))
	конзола.MUnsignedinteger32Штампај(cr0)

	cr4 := Getcr4()
	конзола.MШтампај(([]byte)(":cr4:"))
	конзола.MUnsignedinteger32Штампај(cr4)

	задатакmanager_2 := &TЗадатакmanager{}
	задатакmanager_2.Init()

	Ометањеmanager := &TОметањеmanager{}
	Ометањеmanager.Init(0x20, shareddescriptorТабела, задатакmanager_2)

	paging.СТРАНАfault(Ометањеmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(меморијаmanager)

	процесhelper := Процесhelper{}
	процесhelper.Init(меморијаmanager, СТРАНАДиректоријумунос)

	sche := &Scheduler{}
	sche.Init(Ометањеmanager, меморијаmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Ометањеmanager)

	процесhelper.Spawn(задатакa, threadhelper, sche, uint32(СТРАНАДиректоријумунос), true)
	процесhelper.Spawn(задатакb, threadhelper, sche, uint32(СТРАНАДиректоријумунос), true)
	процесhelper.Spawn(задатакc, threadhelper, sche, uint32(СТРАНАДиректоријумунос), true)
	процесhelper.Spawn(задатакd1, threadhelper, sche, uint32(СТРАНАДиректоријумунос), true)
	процесhelper.Spawn(улазДогађајЗадатак, threadhelper, sche, uint32(СТРАНАДиректоријумунос), true)

	var величина uint32

	var linkerДатотека []byte = ([]byte)("LINKER")
	величина = GetДатотекаВеличина(linkerДатотека)
	linkeraddress := меморијаmanager.Malloc(величина)
	linkerdata := GetБајтовасаПоказивач(uintptr(linkeraddress), int(величина), int(величина))
	ЧитањеДатотека(linkerДатотека, linkerdata)

	elf0 := Elf{}
	linkerунос := elf0.Getунос(linkerdata)
	elf0.Parse(linkerdata[:], uint32(СТРАНАДиректоријумунос))

	везаmap := Везаmap{}
	везаmap.Init(меморијаmanager)

	var либ1Датотека []byte = ([]byte)("LIB1")
	величина = GetДатотекаВеличина(либ1Датотека)

	либ1address := меморијаmanager.Malloc(величина)
	либ1data := GetБајтовасаПоказивач(uintptr(либ1address), int(величина), int(величина))
	ЧитањеДатотека(либ1Датотека, либ1data)

	либ1elf := Elf{}
	либ1elf.Parse(либ1data[:], uint32(СТРАНАДиректоријумунос))
	меморијаmanager.Слободно(либ1address)

	везаmap.Append_to_list(uintptr(либ1elf.Растегљиво))

	var либ2Датотека []byte = ([]byte)("LIB2")
	величина = GetДатотекаВеличина(либ2Датотека)

	либ2address := меморијаmanager.Malloc(величина)
	либ2data := GetБајтовасаПоказивач(uintptr(либ2address), int(величина), int(величина))
	ЧитањеДатотека(либ2Датотека, либ2data)

	либ2elf := Elf{}
	либ2elf.Parse(либ2data[:], uint32(СТРАНАДиректоријумунос))
	меморијаmanager.Слободно(либ2address)

	везаmap.Append_to_list(uintptr(либ2elf.Растегљиво))

	либВезаmap := везаmap.Clone()
	везаmapaddress := uint32(uintptr(Pointer(либВезаmap.First)))

	либ1got := Getunsignedinteger32НизсаПоказивач(uintptr(либ1elf.Got), 4, 4)
	либ1got[1] = везаmapaddress
	либ1got[2] = 0x4000000

	либ2got := Getunsignedinteger32НизсаПоказивач(uintptr(либ2elf.Got), 4, 4)
	либ2got[1] = везаmapaddress
	либ2got[2] = 0x4000000

	конзола.MШтампајxy("lib1: ", 1, 8)
	конзола.MUnsignedinteger32Штампај(либ1elf.Got)
	конзола.MШтампај(":")
	конзола.MUnsignedinteger32Штампај(либ1elf.Растегљиво)

	конзола.MШтампајxy("lib2: ", 1, 9)
	конзола.MUnsignedinteger32Штампај(либ2elf.Got)
	конзола.MШтампај(":")
	конзола.MUnsignedinteger32Штампај(либ2elf.Растегљиво)

	var корисник1Датотека []byte = ([]byte)("USER1")
	величина = GetДатотекаВеличина(корисник1Датотека)
	корисник1address := меморијаmanager.Malloc(величина)
	корисник1data := GetБајтовасаПоказивач(uintptr(корисник1address), int(величина), int(величина))
	ЧитањеДатотека(корисник1Датотека, корисник1data)

	elf2 := Elf{}

	корисник1унос := elf2.Getунос(корисник1data)
	elf2.Parse(корисник1data[:], uint32(СТРАНАДиректоријумунос+0x1000))
	општеoffsetТабела := elf2.Got

	PВредност1Везаmap := везаmap.Clone()
	PВредност1Везаmap.Append_to_list(uintptr(elf2.Растегљиво))

	меморијаmanager.Слободно(корисник1address)

	var code1Показивач *uintptr
	var func1val func()

	code1Показивач = (*uintptr)(меморијаmanager.Malloc(4))
	*code1Показивач = uintptr(linkerунос)
	func1val = *(*func())(Pointer(&code1Показивач))

	proc2 := процесhelper.Spawn(func1val, threadhelper, sche, uint32(СТРАНАДиректоријумунос+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ПроцесорСтање.Ecx = корисник1унос
	thr2.ПроцесорСтање.Edx = општеoffsetТабела
	thr2.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност1Везаmap.First)))

	конзола.MШтампајxy("user1: ", 1, 10)
	конзола.MUnsignedinteger32Штампај(elf2.Got)

	var корисник2Датотека []byte = ([]byte)("USER2")
	величина = GetДатотекаВеличина(корисник2Датотека)
	корисник2address := меморијаmanager.Malloc(величина)
	корисник2data := GetБајтовасаПоказивач(uintptr(корисник2address), int(величина), int(величина))
	ЧитањеДатотека(корисник2Датотека, корисник2data)

	elf3 := Elf{}

	корисник2унос := elf3.Getунос(корисник2data)
	elf3.Parse(корисник2data[:], uint32(СТРАНАДиректоријумунос+0x2000))
	општеoffsetТабела = elf3.Got

	PВредност2Везаmap := везаmap.Clone()
	PВредност2Везаmap.Append_to_list(uintptr(elf3.Растегљиво))

	меморијаmanager.Слободно(корисник2address)

	var code2Показивач *uintptr
	var func2val func()

	code2Показивач = (*uintptr)(меморијаmanager.Malloc(4))
	*code2Показивач = uintptr(linkerунос)
	func2val = *(*func())(Pointer(&code2Показивач))

	proc3 := процесhelper.Spawn(func2val, threadhelper, sche, uint32(СТРАНАДиректоријумунос+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ПроцесорСтање.Ecx = корисник2унос
	thr3.ПроцесорСтање.Edx = општеoffsetТабела
	thr3.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност2Везаmap.First)))

	конзола.MШтампајxy("user2: ", 1, 11)
	конзола.MUnsignedinteger32Штампај(thr3.ПроцесорСтање.Esi)

	либВезаmap.Штампај(1, 11)

	var корисник3Датотека []byte = ([]byte)("USER3")
	величина = GetДатотекаВеличина(корисник3Датотека)
	корисник3address := меморијаmanager.Malloc(величина)
	корисник3data := GetБајтовасаПоказивач(uintptr(корисник3address), int(величина), int(величина))
	ЧитањеДатотека(корисник3Датотека, корисник3data)

	elf4 := Elf{}

	корисник3унос := elf4.Getунос(корисник3data)
	elf4.Parse(корисник3data[:], uint32(СТРАНАДиректоријумунос+0x3000))
	општеoffsetТабела = elf4.Got

	PВредност3Везаmap := везаmap.Clone()
	PВредност3Везаmap.Append_to_list(uintptr(elf4.Растегљиво))

	меморијаmanager.Слободно(корисник3address)

	var code3Показивач *uintptr
	var func3val func()

	code3Показивач = (*uintptr)(меморијаmanager.Malloc(4))
	*code3Показивач = uintptr(linkerунос)
	func3val = *(*func())(Pointer(&code3Показивач))

	proc4 := процесhelper.Spawn(func3val, threadhelper, sche, uint32(СТРАНАДиректоријумунос+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ПроцесорСтање.Ecx = корисник3унос
	thr4.ПроцесорСтање.Edx = општеoffsetТабела
	thr4.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност3Везаmap.First)))

	процесhelper.Spawn(TФункција1, threadhelper, sche, uint32(СТРАНАДиректоријумунос+0x4000), true)

	iТастатураДогађајhandler = &myТастатураДогађајhandler
	тастатураdriver.Initdriver(Ометањеmanager, iТастатураДогађајhandler)

	мишdriver.Initdriver(Ометањеmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Изабериdriver(&Drivermanager, Ометањеmanager)
	уређајdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Омогућено(true)
	Ометањеmanager.Активна()

	for {
		halt()
	}

}
