/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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

import . "virtuelnoMemorija"
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

import . "memorijamanager"
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

func (isti *TMyТастатураДогађајhandler) NaКључНиже(кључ byte) {
	foo := [1]byte{' '}
	foo[0] = кључ

	тастатураКонзола.MŠtampajBajtovaxy(foo[:], 1000, 1000)
}

func (isti *TMyТастатураДогађајhandler) NaКључGore(кључ byte)	{}

var iМишДогађајhandler IМишДогађајhandler

type TMyМишДогађајhandler struct {
}

var мишКонзола TКонзола = TКонзола{}
var previousx int16 = 0
var previousy int16 = 0
var xПоложај int16 = 0
var yПоложај int16 = 0

func (isti *TMyМишДогађајhandler) NaМишНиже(дугме int8) {
	buffer := []byte("x")
	мишКонзола.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (isti *TMyМишДогађајhandler) NaМишGore(дугме int8)	{}
func (isti *TMyМишДогађајhandler) NaМишПремести(x int8, y int8) {

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
	мишКонзола.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	мишКонзола.MŠtampajxy(buffer, uint16(xПоложај), uint16(yПоложај))

	previousx = xПоложај
	previousy = yПоложај
}

var уређајdescriptor TPeripheralcomponentinterconnectУређајdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var конзола TКонзола = TКонзола{}
var drivercount uint16 = 0

func (isti TMypcicontrollerhandler) Nagetdriver(уређај TPeripheralcomponentinterconnectУређајdescriptor) {
	if уређај.ProizvođačIB == 0x1022 && уређај.УређајIB == 0x2000 {
		конзола.MŠtampajxy([]byte("["), 0, 12)
		конзола.MŠtampaj(([]byte)("AMD am79c973"))
		конзола.MŠtampaj([]byte(":"))
		конзола.MUnsignedinteger16Štampaj(уређај.ProizvođačIB)
		конзола.MŠtampaj([]byte(":"))
		конзола.MUnsignedinteger16Štampaj(уређај.УређајIB)
		конзола.MŠtampaj([]byte(":"))
		конзола.MUnsignedinteger16Štampaj(uint16(уређај.Портbase))
		конзола.MŠtampaj([]byte(":"))
		конзола.MUnsignedinteger32Štampaj(уређај.Ометање)

		конзола.MŠtampaj([]byte("]\n"))
		уређајdescriptor = уређај
		drivercount++
	}
}
func (isti TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectУређајdescriptor {
	return уређајdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Štampajstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	конзола.MŠtampaj(str)
}

func GetДатотекаВеличина(датотека []byte) uint32 {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var величина uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], датотека)
	ata0s.Flush()

	return величина
}

func ЧитањеДатотека(датотека []byte, data []byte) {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Читање(&ata0s, partition.Mbr.Primarypartition[0], датотека, data)

	ata0s.Flush()
}
func Оптерећењеelf() {

	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterBlok32{}

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

		SysŠtampajunsignedinteger32(esi)

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
		ПроцесpendingТастатураDogađaji()
		ПроцесpendingМишDogađaji()
		halt()
	}
}

func memorytest(y int) {
	memorijamanager := &TMemorijamanager{}
	allocated := uint32(uintptr(memorijamanager.Malloc(1024)))
	конзола.MUnsignedinteger32Štampajxy(allocated, 10, uint16(y))
	if y == 11 {
		memorijamanager.Slobodno(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzaloop()
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
	var funcBajtova []byte = []byte(funcНазив)

	задатакКонзола.MŠtampajxy(funcBajtova, 1, 5)
	задатакКонзола.MŠtampaj(([]byte)(":"))
	задатакКонзола.MUnsignedinteger32Štampaj(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	задатакКонзола.MŠtampajunsignedinteger32(cr0, 2, 1)
}

var tss *Tssунос = &Tssунос{}

func KKernelEntry(ListDirektorijumунос uintptr, stacktop uintptr, stackbottom uintptr) {

	MСеријскиДневникinit()
	конзола.MŠtampaj("\n=== MNE BOOT ===\n")

	конзола.MŠtampajunsignedinteger32(uint32(ListDirektorijumунос), 0, 2)
	конзола.MŠtampajunsignedinteger32(uint32(ListDirektorijumунос), 10, 2)
	конзола.MŠtampajunsignedinteger32(uint32(stacktop), 0, 3)
	конзола.MŠtampajunsignedinteger32(uint32(stackbottom), 10, 3)

	memorijamanager := &TMemorijamanager{}
	memorijamanager.Init(0, МаксqueueВеличина)

	paging := &Paging{}
	paging.Init(ListDirektorijumунос, 0x500000, memorijamanager)
	paging.SharedMemorijaregion()

	Скупcr3(uint32(ListDirektorijumунос))
	Укљученоpaging()

	shareddescriptorTabela := &TShareddescriptorTabela{}
	shareddescriptorTabela.Init()

	конзола.MŠtampaj("esp:")

	esp := getesp()
	конзола.MUnsignedinteger32Štampaj(uint32(esp))

	tls := gettls()
	конзола.MŠtampaj(([]byte)("tls:"))
	конзола.MUnsignedinteger32Štampaj(tls)

	tss.Instaliraj(shareddescriptorTabela, 7, Segkerneldata, esp)

	VirtТест()

	cr3 := Освежиcr3()
	конзола.MŠtampaj(([]byte)(":cr3:"))
	конзола.MUnsignedinteger32Štampaj(cr3)

	cr0 := Getcr0()
	конзола.MŠtampaj(([]byte)(":cr0:"))
	конзола.MUnsignedinteger32Štampaj(cr0)

	cr4 := Getcr4()
	конзола.MŠtampaj(([]byte)(":cr4:"))
	конзола.MUnsignedinteger32Štampaj(cr4)

	задатакmanager_2 := &TЗадатакmanager{}
	задатакmanager_2.Init()

	Ометањеmanager := &TОметањеmanager{}
	Ометањеmanager.Init(0x20, shareddescriptorTabela, задатакmanager_2)

	paging.Listfault(Ометањеmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorijamanager)

	процесhelper := Процесhelper{}
	процесhelper.Init(memorijamanager, ListDirektorijumунос)

	sche := &Scheduler{}
	sche.Init(Ометањеmanager, memorijamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Ометањеmanager)

	процесhelper.Spawn(задатакa, threadhelper, sche, uint32(ListDirektorijumунос), true)
	процесhelper.Spawn(задатакb, threadhelper, sche, uint32(ListDirektorijumунос), true)
	процесhelper.Spawn(задатакc, threadhelper, sche, uint32(ListDirektorijumунос), true)
	процесhelper.Spawn(задатакd1, threadhelper, sche, uint32(ListDirektorijumунос), true)
	процесhelper.Spawn(улазДогађајЗадатак, threadhelper, sche, uint32(ListDirektorijumунос), true)

	var величина uint32

	var linkerДатотека []byte = ([]byte)("LINKER")
	величина = GetДатотекаВеличина(linkerДатотека)
	linkeraddress := memorijamanager.Malloc(величина)
	linkerdata := GetBajtovasaPokazivač(uintptr(linkeraddress), int(величина), int(величина))
	ЧитањеДатотека(linkerДатотека, linkerdata)

	elf0 := Elf{}
	linkerунос := elf0.Getунос(linkerdata)
	elf0.Parse(linkerdata[:], uint32(ListDirektorijumунос))

	везаmap := Везаmap{}
	везаmap.Init(memorijamanager)

	var либ1Датотека []byte = ([]byte)("LIB1")
	величина = GetДатотекаВеличина(либ1Датотека)

	либ1address := memorijamanager.Malloc(величина)
	либ1data := GetBajtovasaPokazivač(uintptr(либ1address), int(величина), int(величина))
	ЧитањеДатотека(либ1Датотека, либ1data)

	либ1elf := Elf{}
	либ1elf.Parse(либ1data[:], uint32(ListDirektorijumунос))
	memorijamanager.Slobodno(либ1address)

	везаmap.Append_to_list(uintptr(либ1elf.Rastegǉivo))

	var либ2Датотека []byte = ([]byte)("LIB2")
	величина = GetДатотекаВеличина(либ2Датотека)

	либ2address := memorijamanager.Malloc(величина)
	либ2data := GetBajtovasaPokazivač(uintptr(либ2address), int(величина), int(величина))
	ЧитањеДатотека(либ2Датотека, либ2data)

	либ2elf := Elf{}
	либ2elf.Parse(либ2data[:], uint32(ListDirektorijumунос))
	memorijamanager.Slobodno(либ2address)

	везаmap.Append_to_list(uintptr(либ2elf.Rastegǉivo))

	либВезаmap := везаmap.Clone()
	везаmapaddress := uint32(uintptr(Pointer(либВезаmap.First)))

	либ1got := Getunsignedinteger32НизsaPokazivač(uintptr(либ1elf.Got), 4, 4)
	либ1got[1] = везаmapaddress
	либ1got[2] = 0x4000000

	либ2got := Getunsignedinteger32НизsaPokazivač(uintptr(либ2elf.Got), 4, 4)
	либ2got[1] = везаmapaddress
	либ2got[2] = 0x4000000

	конзола.MŠtampajxy("lib1: ", 1, 8)
	конзола.MUnsignedinteger32Štampaj(либ1elf.Got)
	конзола.MŠtampaj(":")
	конзола.MUnsignedinteger32Štampaj(либ1elf.Rastegǉivo)

	конзола.MŠtampajxy("lib2: ", 1, 9)
	конзола.MUnsignedinteger32Štampaj(либ2elf.Got)
	конзола.MŠtampaj(":")
	конзола.MUnsignedinteger32Štampaj(либ2elf.Rastegǉivo)

	var korisnik1Датотека []byte = ([]byte)("USER1")
	величина = GetДатотекаВеличина(korisnik1Датотека)
	korisnik1address := memorijamanager.Malloc(величина)
	korisnik1data := GetBajtovasaPokazivač(uintptr(korisnik1address), int(величина), int(величина))
	ЧитањеДатотека(korisnik1Датотека, korisnik1data)

	elf2 := Elf{}

	korisnik1унос := elf2.Getунос(korisnik1data)
	elf2.Parse(korisnik1data[:], uint32(ListDirektorijumунос+0x1000))
	општеoffsetTabela := elf2.Got

	PВредност1Везаmap := везаmap.Clone()
	PВредност1Везаmap.Append_to_list(uintptr(elf2.Rastegǉivo))

	memorijamanager.Slobodno(korisnik1address)

	var code1Pokazivač *uintptr
	var func1val func()

	code1Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code1Pokazivač = uintptr(linkerунос)
	func1val = *(*func())(Pointer(&code1Pokazivač))

	proc2 := процесhelper.Spawn(func1val, threadhelper, sche, uint32(ListDirektorijumунос+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ПроцесорСтање.Ecx = korisnik1унос
	thr2.ПроцесорСтање.Edx = општеoffsetTabela
	thr2.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност1Везаmap.First)))

	конзола.MŠtampajxy("user1: ", 1, 10)
	конзола.MUnsignedinteger32Štampaj(elf2.Got)

	var korisnik2Датотека []byte = ([]byte)("USER2")
	величина = GetДатотекаВеличина(korisnik2Датотека)
	korisnik2address := memorijamanager.Malloc(величина)
	korisnik2data := GetBajtovasaPokazivač(uintptr(korisnik2address), int(величина), int(величина))
	ЧитањеДатотека(korisnik2Датотека, korisnik2data)

	elf3 := Elf{}

	korisnik2унос := elf3.Getунос(korisnik2data)
	elf3.Parse(korisnik2data[:], uint32(ListDirektorijumунос+0x2000))
	општеoffsetTabela = elf3.Got

	PВредност2Везаmap := везаmap.Clone()
	PВредност2Везаmap.Append_to_list(uintptr(elf3.Rastegǉivo))

	memorijamanager.Slobodno(korisnik2address)

	var code2Pokazivač *uintptr
	var func2val func()

	code2Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code2Pokazivač = uintptr(linkerунос)
	func2val = *(*func())(Pointer(&code2Pokazivač))

	proc3 := процесhelper.Spawn(func2val, threadhelper, sche, uint32(ListDirektorijumунос+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ПроцесорСтање.Ecx = korisnik2унос
	thr3.ПроцесорСтање.Edx = општеoffsetTabela
	thr3.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност2Везаmap.First)))

	конзола.MŠtampajxy("user2: ", 1, 11)
	конзола.MUnsignedinteger32Štampaj(thr3.ПроцесорСтање.Esi)

	либВезаmap.Štampaj(1, 11)

	var korisnik3Датотека []byte = ([]byte)("USER3")
	величина = GetДатотекаВеличина(korisnik3Датотека)
	korisnik3address := memorijamanager.Malloc(величина)
	korisnik3data := GetBajtovasaPokazivač(uintptr(korisnik3address), int(величина), int(величина))
	ЧитањеДатотека(korisnik3Датотека, korisnik3data)

	elf4 := Elf{}

	korisnik3унос := elf4.Getунос(korisnik3data)
	elf4.Parse(korisnik3data[:], uint32(ListDirektorijumунос+0x3000))
	општеoffsetTabela = elf4.Got

	PВредност3Везаmap := везаmap.Clone()
	PВредност3Везаmap.Append_to_list(uintptr(elf4.Rastegǉivo))

	memorijamanager.Slobodno(korisnik3address)

	var code3Pokazivač *uintptr
	var func3val func()

	code3Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code3Pokazivač = uintptr(linkerунос)
	func3val = *(*func())(Pointer(&code3Pokazivač))

	proc4 := процесhelper.Spawn(func3val, threadhelper, sche, uint32(ListDirektorijumунос+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ПроцесорСтање.Ecx = korisnik3унос
	thr4.ПроцесорСтање.Edx = општеoffsetTabela
	thr4.ПроцесорСтање.Esi = uint32(uintptr(Pointer(PВредност3Везаmap.First)))

	процесhelper.Spawn(TФункција1, threadhelper, sche, uint32(ListDirektorijumунос+0x4000), true)

	iТастатураДогађајhandler = &myТастатураДогађајhandler
	тастатураdriver.Initdriver(Ометањеmanager, iТастатураДогађајhandler)

	мишdriver.Initdriver(Ометањеmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Изабериdriver(&Drivermanager, Ометањеmanager)
	уређајdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Омогућено(true)
	Ометањеmanager.Aktivna()

	for {
		halt()
	}

}
