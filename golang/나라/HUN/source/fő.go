package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konzol"
import . "megszakítás"
import . "multitasking"
import . "tasking/tss"

import . "virtualMemória"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/folyamat"
import . "driver/driver"

import . "driver/billentyűzet"
import . "driver/egér"

import . "driver/ata"
import . "fájlRendszer/msdospartition"
import . "fájlRendszer/fat"

import . "fájlRendszer/elf"

import . "rendszercall"

import . "memóriamanager"
import . "pci"

func halt()

var iBillentyűzetEseményhandler IBillentyűzetEseményhandler

type TMyBillentyűzetEseményhandler struct {
}

var myBillentyűzetEseményhandler TMyBillentyűzetEseményhandler
var billentyűzetdriver TBillentyűzetdriver
var egérdriver TEgérdriver
var pciVezérlő TPeripheralcomponentinterconnectVezérlő

var billentyűzetKonzol TKonzol = TKonzol{}

func (self *TMyBillentyűzetEseményhandler) BeBillentyűLe(billentyű byte) {
	foo := [1]byte{' '}
	foo[0] = billentyű

	billentyűzetKonzol.MNyomtatásBájtxy(foo[:], 1000, 1000)
}

func (self *TMyBillentyűzetEseményhandler) BeBillentyűFel(billentyű byte)	{}

var iEgérEseményhandler IEgérEseményhandler

type TMyEgérEseményhandler struct {
}

var egérKonzol TKonzol = TKonzol{}
var previousx int16 = 0
var previousy int16 = 0
var xPozíció int16 = 0
var yPozíció int16 = 0

func (self *TMyEgérEseményhandler) BeEgérLe(gomb int8) {
	buffer := []byte("x")
	egérKonzol.MNyomtatásxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyEgérEseményhandler) BeEgérFel(gomb int8)	{}
func (self *TMyEgérEseményhandler) BeEgérÁthelyezés(x int8, y int8) {

	xPozíció += int16(x)
	if xPozíció < 0 {
		xPozíció = 0
	}
	if xPozíció >= 80 {
		xPozíció = 79
	}

	yPozíció -= int16(y)

	if yPozíció < 0 {
		yPozíció = 0
	}
	if yPozíció >= 25 {
		yPozíció = 24
	}

	buffer := []byte(" ")
	egérKonzol.MNyomtatásxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	egérKonzol.MNyomtatásxy(buffer, uint16(xPozíció), uint16(yPozíció))

	previousx = xPozíció
	previousy = yPozíció
}

var eszközdescriptor TPeripheralcomponentinterconnectEszközdescriptor
var ipciVezérlőhandler IpciVezérlőhandler

type TMypciVezérlőhandler struct {
}

var konzol TKonzol = TKonzol{}
var driverSzámláló uint16 = 0

func (self TMypciVezérlőhandler) Begetdriver(eszköz TPeripheralcomponentinterconnectEszközdescriptor) {
	if eszköz.GyártóAzonosító == 0x1022 && eszköz.EszközAzonosító == 0x2000 {
		konzol.MNyomtatásxy([]byte("["), 0, 12)
		konzol.MNyomtatás(([]byte)("AMD am79c973"))
		konzol.MNyomtatás([]byte(":"))
		konzol.MUnsignedinteger16Nyomtatás(eszköz.GyártóAzonosító)
		konzol.MNyomtatás([]byte(":"))
		konzol.MUnsignedinteger16Nyomtatás(eszköz.EszközAzonosító)
		konzol.MNyomtatás([]byte(":"))
		konzol.MUnsignedinteger16Nyomtatás(uint16(eszköz.Portbase))
		konzol.MNyomtatás([]byte(":"))
		konzol.MUnsignedinteger32Nyomtatás(eszköz.Megszakítás)

		konzol.MNyomtatás([]byte("]\n"))
		eszközdescriptor = eszköz
		driverSzámláló++
	}
}
func (self TMypciVezérlőhandler) Getdriver() TPeripheralcomponentinterconnectEszközdescriptor {
	return eszközdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Nyomtatásstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konzol.MNyomtatás(str)
}

func GetFájlMéret(fájlnév []byte) uint32 {
	var ata0s = THaladóTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTáblázat{}
	partition.Olvasáspartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var méret uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], fájlnév)
	ata0s.Flush()

	return méret
}

func OlvasásFájl(fájlnév []byte, data []byte) {
	var ata0s = THaladóTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTáblázat{}
	partition.Olvasáspartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Olvasás(&ata0s, partition.Mbr.Primarypartition[0], fájlnév, data)

	ata0s.Flush()
}
func Terheléself() {

	var ata0s = THaladóTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTáblázat{}
	partition.Olvasáspartition(&ata0s)

	bios := TBiosparameterBlokk32{}

	var fájlnév []byte = ([]byte)("TEST")
	var méret uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], fájlnév)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Olvasás(&ata0s, partition.Mbr.Primarypartition[0], fájlnév, data)

	elf := Elf{}

	elf.Parse(data[:méret], 0x4f00000)

}

var feladatKonzol TKonzol = TKonzol{}

func TFüggvény1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func feladata() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func feladatb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func feladatc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func feladatd()

func feladatd0() {
	esi := getesi()
	for {

		SysNyomtatásunsignedinteger32(esi)

	}
}

func feladatd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func bemenetEseményFeladat() {
	for {
		FolyamatpendingBillentyűzetEsemények()
		FolyamatpendingEgérEsemények()
		halt()
	}
}

func memorytest(y int) {
	memóriamanager := &TMemóriamanager{}
	allocated := uint32(uintptr(memóriamanager.Malloc(1024)))
	konzol.MUnsignedinteger32Nyomtatásxy(allocated, 10, uint16(y))
	if y == 11 {
		memóriamanager.Szabad(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func FelfüggesztésHurok()
func Újratöltéscr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Halmazcr3(cr3 uint32)
func Getcr4() uint32
func Engedélyezvepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFüggvényNév(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNév = runtime.FuncForPC(address).Name()
	var funcBájt []byte = []byte(funcNév)

	feladatKonzol.MNyomtatásxy(funcBájt, 1, 5)
	feladatKonzol.MNyomtatás(([]byte)(":"))
	feladatKonzol.MUnsignedinteger32Nyomtatás(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	feladatKonzol.MNyomtatásunsignedinteger32(cr0, 2, 1)
}

var tss *Tssbejegyzés = &Tssbejegyzés{}

func KKernelEntry(OldalKönyvtárbejegyzés uintptr, stacktop uintptr, stackbottom uintptr) {

	MSorosloginit()
	konzol.MNyomtatás("\n=== HUN BOOT ===\n")

	konzol.MNyomtatásunsignedinteger32(uint32(OldalKönyvtárbejegyzés), 0, 2)
	konzol.MNyomtatásunsignedinteger32(uint32(OldalKönyvtárbejegyzés), 10, 2)
	konzol.MNyomtatásunsignedinteger32(uint32(stacktop), 0, 3)
	konzol.MNyomtatásunsignedinteger32(uint32(stackbottom), 10, 3)

	memóriamanager := &TMemóriamanager{}
	memóriamanager.Init(0, MaximumqueueMéret)

	paging := &Paging{}
	paging.Init(OldalKönyvtárbejegyzés, 0x500000, memóriamanager)
	paging.SharedMemóriaregion()

	Halmazcr3(uint32(OldalKönyvtárbejegyzés))
	Engedélyezvepaging()

	shareddescriptorTáblázat := &TShareddescriptorTáblázat{}
	shareddescriptorTáblázat.Init()

	konzol.MNyomtatás("esp:")

	esp := getesp()
	konzol.MUnsignedinteger32Nyomtatás(uint32(esp))

	tls := gettls()
	konzol.MNyomtatás(([]byte)("tls:"))
	konzol.MUnsignedinteger32Nyomtatás(tls)

	tss.Telepítés(shareddescriptorTáblázat, 7, Segkerneldata, esp)

	VirtTeszt()

	cr3 := Újratöltéscr3()
	konzol.MNyomtatás(([]byte)(":cr3:"))
	konzol.MUnsignedinteger32Nyomtatás(cr3)

	cr0 := Getcr0()
	konzol.MNyomtatás(([]byte)(":cr0:"))
	konzol.MUnsignedinteger32Nyomtatás(cr0)

	cr4 := Getcr4()
	konzol.MNyomtatás(([]byte)(":cr4:"))
	konzol.MUnsignedinteger32Nyomtatás(cr4)

	feladatmanager_2 := &TFeladatmanager{}
	feladatmanager_2.Init()

	Megszakításmanager := &TMegszakításmanager{}
	Megszakításmanager.Init(0x20, shareddescriptorTáblázat, feladatmanager_2)

	paging.Oldalfault(Megszakításmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memóriamanager)

	folyamathelper := Folyamathelper{}
	folyamathelper.Init(memóriamanager, OldalKönyvtárbejegyzés)

	sche := &Scheduler{}
	sche.Init(Megszakításmanager, memóriamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Megszakításmanager)

	folyamathelper.Spawn(feladata, threadhelper, sche, uint32(OldalKönyvtárbejegyzés), true)
	folyamathelper.Spawn(feladatb, threadhelper, sche, uint32(OldalKönyvtárbejegyzés), true)
	folyamathelper.Spawn(feladatc, threadhelper, sche, uint32(OldalKönyvtárbejegyzés), true)
	folyamathelper.Spawn(feladatd1, threadhelper, sche, uint32(OldalKönyvtárbejegyzés), true)
	folyamathelper.Spawn(bemenetEseményFeladat, threadhelper, sche, uint32(OldalKönyvtárbejegyzés), true)

	var méret uint32

	var linkerFájl []byte = ([]byte)("LINKER")
	méret = GetFájlMéret(linkerFájl)
	linkeraddress := memóriamanager.Malloc(méret)
	linkerdata := GetBájtfromMutató(uintptr(linkeraddress), int(méret), int(méret))
	OlvasásFájl(linkerFájl, linkerdata)

	elf0 := Elf{}
	linkerbejegyzés := elf0.Getbejegyzés(linkerdata)
	elf0.Parse(linkerdata[:], uint32(OldalKönyvtárbejegyzés))

	hivatkozásmap := Hivatkozásmap{}
	hivatkozásmap.Init(memóriamanager)

	var lib1Fájl []byte = ([]byte)("LIB1")
	méret = GetFájlMéret(lib1Fájl)

	lib1address := memóriamanager.Malloc(méret)
	lib1data := GetBájtfromMutató(uintptr(lib1address), int(méret), int(méret))
	OlvasásFájl(lib1Fájl, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(OldalKönyvtárbejegyzés))
	memóriamanager.Szabad(lib1address)

	hivatkozásmap.Append_to_list(uintptr(lib1elf.Dinamikus))

	var lib2Fájl []byte = ([]byte)("LIB2")
	méret = GetFájlMéret(lib2Fájl)

	lib2address := memóriamanager.Malloc(méret)
	lib2data := GetBájtfromMutató(uintptr(lib2address), int(méret), int(méret))
	OlvasásFájl(lib2Fájl, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(OldalKönyvtárbejegyzés))
	memóriamanager.Szabad(lib2address)

	hivatkozásmap.Append_to_list(uintptr(lib2elf.Dinamikus))

	libHivatkozásmap := hivatkozásmap.Clone()
	hivatkozásmapaddress := uint32(uintptr(Pointer(libHivatkozásmap.First)))

	lib1got := Getunsignedinteger32TömbfromMutató(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = hivatkozásmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TömbfromMutató(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = hivatkozásmapaddress
	lib2got[2] = 0x4000000

	konzol.MNyomtatásxy("lib1: ", 1, 8)
	konzol.MUnsignedinteger32Nyomtatás(lib1elf.Got)
	konzol.MNyomtatás(":")
	konzol.MUnsignedinteger32Nyomtatás(lib1elf.Dinamikus)

	konzol.MNyomtatásxy("lib2: ", 1, 9)
	konzol.MUnsignedinteger32Nyomtatás(lib2elf.Got)
	konzol.MNyomtatás(":")
	konzol.MUnsignedinteger32Nyomtatás(lib2elf.Dinamikus)

	var felhasználó1Fájl []byte = ([]byte)("USER1")
	méret = GetFájlMéret(felhasználó1Fájl)
	felhasználó1address := memóriamanager.Malloc(méret)
	felhasználó1data := GetBájtfromMutató(uintptr(felhasználó1address), int(méret), int(méret))
	OlvasásFájl(felhasználó1Fájl, felhasználó1data)

	elf2 := Elf{}

	felhasználó1bejegyzés := elf2.Getbejegyzés(felhasználó1data)
	elf2.Parse(felhasználó1data[:], uint32(OldalKönyvtárbejegyzés+0x1000))
	globálisEltolásTáblázat := elf2.Got

	PÉrték1Hivatkozásmap := hivatkozásmap.Clone()
	PÉrték1Hivatkozásmap.Append_to_list(uintptr(elf2.Dinamikus))

	memóriamanager.Szabad(felhasználó1address)

	var code1Mutató *uintptr
	var func1val func()

	code1Mutató = (*uintptr)(memóriamanager.Malloc(4))
	*code1Mutató = uintptr(linkerbejegyzés)
	func1val = *(*func())(Pointer(&code1Mutató))

	proc2 := folyamathelper.Spawn(func1val, threadhelper, sche, uint32(OldalKönyvtárbejegyzés+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuÁllapot.Ecx = felhasználó1bejegyzés
	thr2.CpuÁllapot.Edx = globálisEltolásTáblázat
	thr2.CpuÁllapot.Esi = uint32(uintptr(Pointer(PÉrték1Hivatkozásmap.First)))

	konzol.MNyomtatásxy("user1: ", 1, 10)
	konzol.MUnsignedinteger32Nyomtatás(elf2.Got)

	var felhasználó2Fájl []byte = ([]byte)("USER2")
	méret = GetFájlMéret(felhasználó2Fájl)
	felhasználó2address := memóriamanager.Malloc(méret)
	felhasználó2data := GetBájtfromMutató(uintptr(felhasználó2address), int(méret), int(méret))
	OlvasásFájl(felhasználó2Fájl, felhasználó2data)

	elf3 := Elf{}

	felhasználó2bejegyzés := elf3.Getbejegyzés(felhasználó2data)
	elf3.Parse(felhasználó2data[:], uint32(OldalKönyvtárbejegyzés+0x2000))
	globálisEltolásTáblázat = elf3.Got

	PÉrték2Hivatkozásmap := hivatkozásmap.Clone()
	PÉrték2Hivatkozásmap.Append_to_list(uintptr(elf3.Dinamikus))

	memóriamanager.Szabad(felhasználó2address)

	var code2Mutató *uintptr
	var func2val func()

	code2Mutató = (*uintptr)(memóriamanager.Malloc(4))
	*code2Mutató = uintptr(linkerbejegyzés)
	func2val = *(*func())(Pointer(&code2Mutató))

	proc3 := folyamathelper.Spawn(func2val, threadhelper, sche, uint32(OldalKönyvtárbejegyzés+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuÁllapot.Ecx = felhasználó2bejegyzés
	thr3.CpuÁllapot.Edx = globálisEltolásTáblázat
	thr3.CpuÁllapot.Esi = uint32(uintptr(Pointer(PÉrték2Hivatkozásmap.First)))

	konzol.MNyomtatásxy("user2: ", 1, 11)
	konzol.MUnsignedinteger32Nyomtatás(thr3.CpuÁllapot.Esi)

	libHivatkozásmap.Nyomtatás(1, 11)

	var felhasználó3Fájl []byte = ([]byte)("USER3")
	méret = GetFájlMéret(felhasználó3Fájl)
	felhasználó3address := memóriamanager.Malloc(méret)
	felhasználó3data := GetBájtfromMutató(uintptr(felhasználó3address), int(méret), int(méret))
	OlvasásFájl(felhasználó3Fájl, felhasználó3data)

	elf4 := Elf{}

	felhasználó3bejegyzés := elf4.Getbejegyzés(felhasználó3data)
	elf4.Parse(felhasználó3data[:], uint32(OldalKönyvtárbejegyzés+0x3000))
	globálisEltolásTáblázat = elf4.Got

	PÉrték3Hivatkozásmap := hivatkozásmap.Clone()
	PÉrték3Hivatkozásmap.Append_to_list(uintptr(elf4.Dinamikus))

	memóriamanager.Szabad(felhasználó3address)

	var code3Mutató *uintptr
	var func3val func()

	code3Mutató = (*uintptr)(memóriamanager.Malloc(4))
	*code3Mutató = uintptr(linkerbejegyzés)
	func3val = *(*func())(Pointer(&code3Mutató))

	proc4 := folyamathelper.Spawn(func3val, threadhelper, sche, uint32(OldalKönyvtárbejegyzés+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuÁllapot.Ecx = felhasználó3bejegyzés
	thr4.CpuÁllapot.Edx = globálisEltolásTáblázat
	thr4.CpuÁllapot.Esi = uint32(uintptr(Pointer(PÉrték3Hivatkozásmap.First)))

	folyamathelper.Spawn(TFüggvény1, threadhelper, sche, uint32(OldalKönyvtárbejegyzés+0x4000), true)

	iBillentyűzetEseményhandler = &myBillentyűzetEseményhandler
	billentyűzetdriver.Initdriver(Megszakításmanager, iBillentyűzetEseményhandler)

	egérdriver.Initdriver(Megszakításmanager, nil)

	mypciVezérlőhandler := TMypciVezérlőhandler{}
	pciVezérlő.Init(mypciVezérlőhandler)
	pciVezérlő.Kijelölésdriver(&Drivermanager, Megszakításmanager)
	eszközdescriptor = mypciVezérlőhandler.Getdriver()

	sche.Engedélyezve(true)
	Megszakításmanager.Aktív()

	for {
		halt()
	}

}
