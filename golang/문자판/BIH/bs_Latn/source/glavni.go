package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "interrupt"
import . "multitasking"
import . "tasking/tss"

import . "virtuelnoMemorija"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/process"
import . "driver/driver"

import . "driver/tastatura"
import . "driver/miš"

import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "datotekaSistem/fat"

import . "datotekaSistem/elf"

import . "sistemcall"

import . "memorijamanager"
import . "pci"

func halt()

var iTastaturaeventhandler ITastaturaeventhandler

type TMyTastaturaeventhandler struct {
}

var myTastaturaeventhandler TMyTastaturaeventhandler
var tastaturadriver TTastaturadriver
var mišdriver TMišdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastaturaconsole TConsole = TConsole{}

func (self *TMyTastaturaeventhandler) UključenKljučdown(ključ byte) {
	foo := [1]byte{' '}
	foo[0] = ključ

	tastaturaconsole.MŠtampajBajtovaxy(foo[:], 1000, 1000)
}

func (self *TMyTastaturaeventhandler) UključenKljučGore(ključ byte)	{}

var iMiševenthandler IMiševenthandler

type TMyMiševenthandler struct {
}

var mišconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xpoložaj int16 = 0
var ypoložaj int16 = 0

func (self *TMyMiševenthandler) UključenMišdown(button int8) {
	buffer := []byte("x")
	mišconsole.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyMiševenthandler) UključenMišGore(button int8)	{}
func (self *TMyMiševenthandler) UključenMišPremjesti(x int8, y int8) {

	xpoložaj += int16(x)
	if xpoložaj < 0 {
		xpoložaj = 0
	}
	if xpoložaj >= 80 {
		xpoložaj = 79
	}

	ypoložaj -= int16(y)

	if ypoložaj < 0 {
		ypoložaj = 0
	}
	if ypoložaj >= 25 {
		ypoložaj = 24
	}

	buffer := []byte(" ")
	mišconsole.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mišconsole.MŠtampajxy(buffer, uint16(xpoložaj), uint16(ypoložaj))

	previousx = xpoložaj
	previousy = ypoložaj
}

var uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (self TMypcicontrollerhandler) Uključengetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
	if uređaj.Vendorid == 0x1022 && uređaj.Uređajid == 0x2000 {
		console.MŠtampajxy([]byte("["), 0, 12)
		console.MŠtampaj(([]byte)("AMD am79c973"))
		console.MŠtampaj([]byte(":"))
		console.MUnsignedinteger16Štampaj(uređaj.Vendorid)
		console.MŠtampaj([]byte(":"))
		console.MUnsignedinteger16Štampaj(uređaj.Uređajid)
		console.MŠtampaj([]byte(":"))
		console.MUnsignedinteger16Štampaj(uint16(uređaj.Portbase))
		console.MŠtampaj([]byte(":"))
		console.MUnsignedinteger32Štampaj(uređaj.Interrupt)

		console.MŠtampaj([]byte("]\n"))
		uređajdescriptor = uređaj
		drivercount++
	}
}
func (self TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectUređajdescriptor {
	return uređajdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Štampajstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MŠtampaj(str)
}

func GetDatotekaVeličina(imedatoteke []byte) uint32 {
	var ata0s = TNaprednotechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterblok32{}

	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	ata0s.Flush()

	return veličina
}

func ČitajDatoteka(imedatoteke []byte, data []byte) {
	var ata0s = TNaprednotechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterblok32{}
	bios.Čitaj(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	ata0s.Flush()
}
func Opterećenjeelf() {

	var ata0s = TNaprednotechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterblok32{}

	var imedatoteke []byte = ([]byte)("TEST")
	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Čitaj(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	elf := Elf{}

	elf.Parse(data[:veličina], 0x4f00000)

}

var taskconsole TConsole = TConsole{}

func TFunkcija1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func taska() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func taskb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func taskc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func taskd()

func taskd0() {
	esi := getesi()
	for {

		SysŠtampajunsignedinteger32(esi)

	}
}

func taskd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ulazeventtask() {
	for {
		ProcesspendingTastaturaevents()
		ProcesspendingMiševents()
		halt()
	}
}

func memorytest(y int) {
	memorijamanager := &TMemorijamanager{}
	allocated := uint32(uintptr(memorijamanager.Malloc(1024)))
	console.MUnsignedinteger32Štampajxy(allocated, 10, uint16(y))
	if y == 11 {
		memorijamanager.Slobodno(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzaloop()
func Učitajponovocr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Skupcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcijaNaziv(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNaziv = runtime.FuncForPC(address).Name()
	var funcBajtova []byte = []byte(funcNaziv)

	taskconsole.MŠtampajxy(funcBajtova, 1, 5)
	taskconsole.MŠtampaj(([]byte)(":"))
	taskconsole.MUnsignedinteger32Štampaj(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	taskconsole.MŠtampajunsignedinteger32(cr0, 2, 1)
}

var tss *Tssunos = &Tssunos{}

func KKernelEntry(StranicaDirektorijunos uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MŠtampaj("\n=== BIH BOOT ===\n")

	console.MŠtampajunsignedinteger32(uint32(StranicaDirektorijunos), 0, 2)
	console.MŠtampajunsignedinteger32(uint32(StranicaDirektorijunos), 10, 2)
	console.MŠtampajunsignedinteger32(uint32(stacktop), 0, 3)
	console.MŠtampajunsignedinteger32(uint32(stackbottom), 10, 3)

	memorijamanager := &TMemorijamanager{}
	memorijamanager.Init(0, MaxqueueVeličina)

	paging := &Paging{}
	paging.Init(StranicaDirektorijunos, 0x500000, memorijamanager)
	paging.SharedMemorijaregion()

	Skupcr3(uint32(StranicaDirektorijunos))
	Enablepaging()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	console.MŠtampaj("esp:")

	esp := getesp()
	console.MUnsignedinteger32Štampaj(uint32(esp))

	tls := gettls()
	console.MŠtampaj(([]byte)("tls:"))
	console.MUnsignedinteger32Štampaj(tls)

	tss.Instaliraj(shareddescriptortable, 7, Segkerneldata, esp)

	Virttest()

	cr3 := Učitajponovocr3()
	console.MŠtampaj(([]byte)(":cr3:"))
	console.MUnsignedinteger32Štampaj(cr3)

	cr0 := Getcr0()
	console.MŠtampaj(([]byte)(":cr0:"))
	console.MUnsignedinteger32Štampaj(cr0)

	cr4 := Getcr4()
	console.MŠtampaj(([]byte)(":cr4:"))
	console.MUnsignedinteger32Štampaj(cr4)

	taskmanager_2 := &TTaskmanager{}
	taskmanager_2.Init()

	Interruptmanager := &TInterruptmanager{}
	Interruptmanager.Init(0x20, shareddescriptortable, taskmanager_2)

	paging.Stranicafault(Interruptmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorijamanager)

	processhelper := Processhelper{}
	processhelper.Init(memorijamanager, StranicaDirektorijunos)

	sche := &Scheduler{}
	sche.Init(Interruptmanager, memorijamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interruptmanager)

	processhelper.Spawn(taska, threadhelper, sche, uint32(StranicaDirektorijunos), true)
	processhelper.Spawn(taskb, threadhelper, sche, uint32(StranicaDirektorijunos), true)
	processhelper.Spawn(taskc, threadhelper, sche, uint32(StranicaDirektorijunos), true)
	processhelper.Spawn(taskd1, threadhelper, sche, uint32(StranicaDirektorijunos), true)
	processhelper.Spawn(ulazeventtask, threadhelper, sche, uint32(StranicaDirektorijunos), true)

	var veličina uint32

	var linkerDatoteka []byte = ([]byte)("LINKER")
	veličina = GetDatotekaVeličina(linkerDatoteka)
	linkeraddress := memorijamanager.Malloc(veličina)
	linkerdata := GetBajtovafrompointer(uintptr(linkeraddress), int(veličina), int(veličina))
	ČitajDatoteka(linkerDatoteka, linkerdata)

	elf0 := Elf{}
	linkerunos := elf0.Getunos(linkerdata)
	elf0.Parse(linkerdata[:], uint32(StranicaDirektorijunos))

	vezamap := Vezamap{}
	vezamap.Init(memorijamanager)

	var lib1Datoteka []byte = ([]byte)("LIB1")
	veličina = GetDatotekaVeličina(lib1Datoteka)

	lib1address := memorijamanager.Malloc(veličina)
	lib1data := GetBajtovafrompointer(uintptr(lib1address), int(veličina), int(veličina))
	ČitajDatoteka(lib1Datoteka, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(StranicaDirektorijunos))
	memorijamanager.Slobodno(lib1address)

	vezamap.Append_to_list(uintptr(lib1elf.Dynamic))

	var lib2Datoteka []byte = ([]byte)("LIB2")
	veličina = GetDatotekaVeličina(lib2Datoteka)

	lib2address := memorijamanager.Malloc(veličina)
	lib2data := GetBajtovafrompointer(uintptr(lib2address), int(veličina), int(veličina))
	ČitajDatoteka(lib2Datoteka, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(StranicaDirektorijunos))
	memorijamanager.Slobodno(lib2address)

	vezamap.Append_to_list(uintptr(lib2elf.Dynamic))

	libVezamap := vezamap.Clone()
	vezamapaddress := uint32(uintptr(Pointer(libVezamap.First)))

	lib1got := Getunsignedinteger32arrayfrompointer(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = vezamapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32arrayfrompointer(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = vezamapaddress
	lib2got[2] = 0x4000000

	console.MŠtampajxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Štampaj(lib1elf.Got)
	console.MŠtampaj(":")
	console.MUnsignedinteger32Štampaj(lib1elf.Dynamic)

	console.MŠtampajxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Štampaj(lib2elf.Got)
	console.MŠtampaj(":")
	console.MUnsignedinteger32Štampaj(lib2elf.Dynamic)

	var korisnik1Datoteka []byte = ([]byte)("USER1")
	veličina = GetDatotekaVeličina(korisnik1Datoteka)
	korisnik1address := memorijamanager.Malloc(veličina)
	korisnik1data := GetBajtovafrompointer(uintptr(korisnik1address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik1Datoteka, korisnik1data)

	elf2 := Elf{}

	korisnik1unos := elf2.Getunos(korisnik1data)
	elf2.Parse(korisnik1data[:], uint32(StranicaDirektorijunos+0x1000))
	globalnaoffsettable := elf2.Got

	PVrijednost1Vezamap := vezamap.Clone()
	PVrijednost1Vezamap.Append_to_list(uintptr(elf2.Dynamic))

	memorijamanager.Slobodno(korisnik1address)

	var code1pointer *uintptr
	var func1val func()

	code1pointer = (*uintptr)(memorijamanager.Malloc(4))
	*code1pointer = uintptr(linkerunos)
	func1val = *(*func())(Pointer(&code1pointer))

	proc2 := processhelper.Spawn(func1val, threadhelper, sche, uint32(StranicaDirektorijunos+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.Cpustate.Ecx = korisnik1unos
	thr2.Cpustate.Edx = globalnaoffsettable
	thr2.Cpustate.Esi = uint32(uintptr(Pointer(PVrijednost1Vezamap.First)))

	console.MŠtampajxy("user1: ", 1, 10)
	console.MUnsignedinteger32Štampaj(elf2.Got)

	var korisnik2Datoteka []byte = ([]byte)("USER2")
	veličina = GetDatotekaVeličina(korisnik2Datoteka)
	korisnik2address := memorijamanager.Malloc(veličina)
	korisnik2data := GetBajtovafrompointer(uintptr(korisnik2address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik2Datoteka, korisnik2data)

	elf3 := Elf{}

	korisnik2unos := elf3.Getunos(korisnik2data)
	elf3.Parse(korisnik2data[:], uint32(StranicaDirektorijunos+0x2000))
	globalnaoffsettable = elf3.Got

	PVrijednost2Vezamap := vezamap.Clone()
	PVrijednost2Vezamap.Append_to_list(uintptr(elf3.Dynamic))

	memorijamanager.Slobodno(korisnik2address)

	var code2pointer *uintptr
	var func2val func()

	code2pointer = (*uintptr)(memorijamanager.Malloc(4))
	*code2pointer = uintptr(linkerunos)
	func2val = *(*func())(Pointer(&code2pointer))

	proc3 := processhelper.Spawn(func2val, threadhelper, sche, uint32(StranicaDirektorijunos+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.Cpustate.Ecx = korisnik2unos
	thr3.Cpustate.Edx = globalnaoffsettable
	thr3.Cpustate.Esi = uint32(uintptr(Pointer(PVrijednost2Vezamap.First)))

	console.MŠtampajxy("user2: ", 1, 11)
	console.MUnsignedinteger32Štampaj(thr3.Cpustate.Esi)

	libVezamap.Štampaj(1, 11)

	var korisnik3Datoteka []byte = ([]byte)("USER3")
	veličina = GetDatotekaVeličina(korisnik3Datoteka)
	korisnik3address := memorijamanager.Malloc(veličina)
	korisnik3data := GetBajtovafrompointer(uintptr(korisnik3address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik3Datoteka, korisnik3data)

	elf4 := Elf{}

	korisnik3unos := elf4.Getunos(korisnik3data)
	elf4.Parse(korisnik3data[:], uint32(StranicaDirektorijunos+0x3000))
	globalnaoffsettable = elf4.Got

	PVrijednost3Vezamap := vezamap.Clone()
	PVrijednost3Vezamap.Append_to_list(uintptr(elf4.Dynamic))

	memorijamanager.Slobodno(korisnik3address)

	var code3pointer *uintptr
	var func3val func()

	code3pointer = (*uintptr)(memorijamanager.Malloc(4))
	*code3pointer = uintptr(linkerunos)
	func3val = *(*func())(Pointer(&code3pointer))

	proc4 := processhelper.Spawn(func3val, threadhelper, sche, uint32(StranicaDirektorijunos+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.Cpustate.Ecx = korisnik3unos
	thr4.Cpustate.Edx = globalnaoffsettable
	thr4.Cpustate.Esi = uint32(uintptr(Pointer(PVrijednost3Vezamap.First)))

	processhelper.Spawn(TFunkcija1, threadhelper, sche, uint32(StranicaDirektorijunos+0x4000), true)

	iTastaturaeventhandler = &myTastaturaeventhandler
	tastaturadriver.Initdriver(Interruptmanager, iTastaturaeventhandler)

	mišdriver.Initdriver(Interruptmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Selectdriver(&Drivermanager, Interruptmanager)
	uređajdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Enabled(true)
	Interruptmanager.Active()

	for {
		halt()
	}

}
