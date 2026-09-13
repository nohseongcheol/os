package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "prekid"
import . "multitasking"
import . "tasking/tss"

import . "virtualnoMemorija"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
import . "driver/driver"

import . "driver/tipkovnica"
import . "driver/miš"

import . "driver/ata"
import . "datotekaSustav/msdospartition"
import . "datotekaSustav/fat"

import . "datotekaSustav/elf"

import . "sustavcall"

import . "memorijamanager"
import . "pci"

func halt()

var iTipkovnicaDogađajhandler ITipkovnicaDogađajhandler

type TMyTipkovnicaDogađajhandler struct {
}

var myTipkovnicaDogađajhandler TMyTipkovnicaDogađajhandler
var tipkovnicadriver TTipkovnicadriver
var mišdriver TMišdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tipkovnicaconsole TConsole = TConsole{}

func (sam *TMyTipkovnicaDogađajhandler) UključenoKljučDolje(ključ byte) {
	foo := [1]byte{' '}
	foo[0] = ključ

	tipkovnicaconsole.MIspisBajtovaxy(foo[:], 1000, 1000)
}

func (sam *TMyTipkovnicaDogađajhandler) UključenoKljučGore(ključ byte)	{}

var iMišDogađajhandler IMišDogađajhandler

type TMyMišDogađajhandler struct {
}

var mišconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPozicija int16 = 0
var yPozicija int16 = 0

func (sam *TMyMišDogađajhandler) UključenoMišDolje(dugme int8) {
	buffer := []byte("x")
	mišconsole.MIspisxy(buffer, uint16(previousx), uint16(previousy))
}
func (sam *TMyMišDogađajhandler) UključenoMišGore(dugme int8)	{}
func (sam *TMyMišDogađajhandler) UključenoMišPremjesti(x int8, y int8) {

	xPozicija += int16(x)
	if xPozicija < 0 {
		xPozicija = 0
	}
	if xPozicija >= 80 {
		xPozicija = 79
	}

	yPozicija -= int16(y)

	if yPozicija < 0 {
		yPozicija = 0
	}
	if yPozicija >= 25 {
		yPozicija = 24
	}

	buffer := []byte(" ")
	mišconsole.MIspisxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mišconsole.MIspisxy(buffer, uint16(xPozicija), uint16(yPozicija))

	previousx = xPozicija
	previousy = yPozicija
}

var uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (sam TMypcicontrollerhandler) Uključenogetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
	if uređaj.ProdavačIdentifikacija == 0x1022 && uređaj.UređajIdentifikacija == 0x2000 {
		console.MIspisxy([]byte("["), 0, 12)
		console.MIspis(([]byte)("AMD am79c973"))
		console.MIspis([]byte(":"))
		console.MUnsignedinteger16Ispis(uređaj.ProdavačIdentifikacija)
		console.MIspis([]byte(":"))
		console.MUnsignedinteger16Ispis(uređaj.UređajIdentifikacija)
		console.MIspis([]byte(":"))
		console.MUnsignedinteger16Ispis(uint16(uređaj.Portbase))
		console.MIspis([]byte(":"))
		console.MUnsignedinteger32Ispis(uređaj.Prekid)

		console.MIspis([]byte("]\n"))
		uređajdescriptor = uređaj
		drivercount++
	}
}
func (sam TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectUređajdescriptor {
	return uređajdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Ispisstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MIspis(str)
}

func GetDatotekaVeličina(imedatoteke []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablica{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterBlokiraj32{}

	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	ata0s.Flush()

	return veličina
}

func ČitajDatoteka(imedatoteke []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablica{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterBlokiraj32{}
	bios.Čitaj(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	ata0s.Flush()
}
func Opterećenjeelf() {

	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablica{}
	partition.Čitajpartition(&ata0s)

	bios := TBiosparameterBlokiraj32{}

	var imedatoteke []byte = ([]byte)("TEST")
	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Čitaj(&ata0s, partition.Mbr.Primarypartition[0], imedatoteke, data)

	elf := Elf{}

	elf.Parse(data[:veličina], 0x4f00000)

}

var zadatakconsole TConsole = TConsole{}

func TFunkcija1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func zadataka() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func zadatakb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func zadatakc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func zadatakd()

func zadatakd0() {
	esi := getesi()
	for {

		SysIspisunsignedinteger32(esi)

	}
}

func zadatakd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ulazDogađajZadatak() {
	for {
		ProcespendingTipkovnicaevents()
		ProcespendingMiševents()
		halt()
	}
}

func memorytest(y int) {
	memorijamanager := &TMemorijamanager{}
	allocated := uint32(uintptr(memorijamanager.Malloc(1024)))
	console.MUnsignedinteger32Ispisxy(allocated, 10, uint16(y))
	if y == 11 {
		memorijamanager.Slobodno(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzaloop()
func Ponovnoučitavanjecr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Postavicr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFunkcijaIme(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcIme = runtime.FuncForPC(address).Name()
	var funcBajtova []byte = []byte(funcIme)

	zadatakconsole.MIspisxy(funcBajtova, 1, 5)
	zadatakconsole.MIspis(([]byte)(":"))
	zadatakconsole.MUnsignedinteger32Ispis(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	zadatakconsole.MIspisunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(StranicaDirektorijentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerijskiZapisujinit()
	console.MIspis("\n=== HRV BOOT ===\n")

	console.MIspisunsignedinteger32(uint32(StranicaDirektorijentry), 0, 2)
	console.MIspisunsignedinteger32(uint32(StranicaDirektorijentry), 10, 2)
	console.MIspisunsignedinteger32(uint32(stacktop), 0, 3)
	console.MIspisunsignedinteger32(uint32(stackbottom), 10, 3)

	memorijamanager := &TMemorijamanager{}
	memorijamanager.Init(0, MaksqueueVeličina)

	paging := &Paging{}
	paging.Init(StranicaDirektorijentry, 0x500000, memorijamanager)
	paging.SharedMemorijaregion()

	Postavicr3(uint32(StranicaDirektorijentry))
	Enablepaging()

	shareddescriptorTablica := &TShareddescriptorTablica{}
	shareddescriptorTablica.Init()

	console.MIspis("esp:")

	esp := getesp()
	console.MUnsignedinteger32Ispis(uint32(esp))

	tls := gettls()
	console.MIspis(([]byte)("tls:"))
	console.MUnsignedinteger32Ispis(tls)

	tss.Instaliraj(shareddescriptorTablica, 7, Segkerneldata, esp)

	VirtProvjeri()

	cr3 := Ponovnoučitavanjecr3()
	console.MIspis(([]byte)(":cr3:"))
	console.MUnsignedinteger32Ispis(cr3)

	cr0 := Getcr0()
	console.MIspis(([]byte)(":cr0:"))
	console.MUnsignedinteger32Ispis(cr0)

	cr4 := Getcr4()
	console.MIspis(([]byte)(":cr4:"))
	console.MUnsignedinteger32Ispis(cr4)

	zadatakmanager_2 := &TZadatakmanager{}
	zadatakmanager_2.Init()

	Prekidmanager := &TPrekidmanager{}
	Prekidmanager.Init(0x20, shareddescriptorTablica, zadatakmanager_2)

	paging.Stranicafault(Prekidmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorijamanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(memorijamanager, StranicaDirektorijentry)

	sche := &Scheduler{}
	sche.Init(Prekidmanager, memorijamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Prekidmanager)

	proceshelper.Spawn(zadataka, threadhelper, sche, uint32(StranicaDirektorijentry), true)
	proceshelper.Spawn(zadatakb, threadhelper, sche, uint32(StranicaDirektorijentry), true)
	proceshelper.Spawn(zadatakc, threadhelper, sche, uint32(StranicaDirektorijentry), true)
	proceshelper.Spawn(zadatakd1, threadhelper, sche, uint32(StranicaDirektorijentry), true)
	proceshelper.Spawn(ulazDogađajZadatak, threadhelper, sche, uint32(StranicaDirektorijentry), true)

	var veličina uint32

	var linkerDatoteka []byte = ([]byte)("LINKER")
	veličina = GetDatotekaVeličina(linkerDatoteka)
	linkeraddress := memorijamanager.Malloc(veličina)
	linkerdata := GetBajtovafromPokazivač(uintptr(linkeraddress), int(veličina), int(veličina))
	ČitajDatoteka(linkerDatoteka, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(StranicaDirektorijentry))

	poveznicamap := Poveznicamap{}
	poveznicamap.Init(memorijamanager)

	var lib1Datoteka []byte = ([]byte)("LIB1")
	veličina = GetDatotekaVeličina(lib1Datoteka)

	lib1address := memorijamanager.Malloc(veličina)
	lib1data := GetBajtovafromPokazivač(uintptr(lib1address), int(veličina), int(veličina))
	ČitajDatoteka(lib1Datoteka, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(StranicaDirektorijentry))
	memorijamanager.Slobodno(lib1address)

	poveznicamap.Append_to_list(uintptr(lib1elf.Dinamično))

	var lib2Datoteka []byte = ([]byte)("LIB2")
	veličina = GetDatotekaVeličina(lib2Datoteka)

	lib2address := memorijamanager.Malloc(veličina)
	lib2data := GetBajtovafromPokazivač(uintptr(lib2address), int(veličina), int(veličina))
	ČitajDatoteka(lib2Datoteka, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(StranicaDirektorijentry))
	memorijamanager.Slobodno(lib2address)

	poveznicamap.Append_to_list(uintptr(lib2elf.Dinamično))

	libPoveznicamap := poveznicamap.Clone()
	poveznicamapaddress := uint32(uintptr(Pointer(libPoveznicamap.First)))

	lib1got := Getunsignedinteger32NizfromPokazivač(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = poveznicamapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32NizfromPokazivač(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = poveznicamapaddress
	lib2got[2] = 0x4000000

	console.MIspisxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Ispis(lib1elf.Got)
	console.MIspis(":")
	console.MUnsignedinteger32Ispis(lib1elf.Dinamično)

	console.MIspisxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Ispis(lib2elf.Got)
	console.MIspis(":")
	console.MUnsignedinteger32Ispis(lib2elf.Dinamično)

	var korisnik1Datoteka []byte = ([]byte)("USER1")
	veličina = GetDatotekaVeličina(korisnik1Datoteka)
	korisnik1address := memorijamanager.Malloc(veličina)
	korisnik1data := GetBajtovafromPokazivač(uintptr(korisnik1address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik1Datoteka, korisnik1data)

	elf2 := Elf{}

	korisnik1entry := elf2.Getentry(korisnik1data)
	elf2.Parse(korisnik1data[:], uint32(StranicaDirektorijentry+0x1000))
	općioffsetTablica := elf2.Got

	PVrijednost1Poveznicamap := poveznicamap.Clone()
	PVrijednost1Poveznicamap.Append_to_list(uintptr(elf2.Dinamično))

	memorijamanager.Slobodno(korisnik1address)

	var code1Pokazivač *uintptr
	var func1val func()

	code1Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code1Pokazivač = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Pokazivač))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(StranicaDirektorijentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProcesorStanje.Ecx = korisnik1entry
	thr2.ProcesorStanje.Edx = općioffsetTablica
	thr2.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrijednost1Poveznicamap.First)))

	console.MIspisxy("user1: ", 1, 10)
	console.MUnsignedinteger32Ispis(elf2.Got)

	var korisnik2Datoteka []byte = ([]byte)("USER2")
	veličina = GetDatotekaVeličina(korisnik2Datoteka)
	korisnik2address := memorijamanager.Malloc(veličina)
	korisnik2data := GetBajtovafromPokazivač(uintptr(korisnik2address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik2Datoteka, korisnik2data)

	elf3 := Elf{}

	korisnik2entry := elf3.Getentry(korisnik2data)
	elf3.Parse(korisnik2data[:], uint32(StranicaDirektorijentry+0x2000))
	općioffsetTablica = elf3.Got

	PVrijednost2Poveznicamap := poveznicamap.Clone()
	PVrijednost2Poveznicamap.Append_to_list(uintptr(elf3.Dinamično))

	memorijamanager.Slobodno(korisnik2address)

	var code2Pokazivač *uintptr
	var func2val func()

	code2Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code2Pokazivač = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Pokazivač))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(StranicaDirektorijentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProcesorStanje.Ecx = korisnik2entry
	thr3.ProcesorStanje.Edx = općioffsetTablica
	thr3.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrijednost2Poveznicamap.First)))

	console.MIspisxy("user2: ", 1, 11)
	console.MUnsignedinteger32Ispis(thr3.ProcesorStanje.Esi)

	libPoveznicamap.Ispis(1, 11)

	var korisnik3Datoteka []byte = ([]byte)("USER3")
	veličina = GetDatotekaVeličina(korisnik3Datoteka)
	korisnik3address := memorijamanager.Malloc(veličina)
	korisnik3data := GetBajtovafromPokazivač(uintptr(korisnik3address), int(veličina), int(veličina))
	ČitajDatoteka(korisnik3Datoteka, korisnik3data)

	elf4 := Elf{}

	korisnik3entry := elf4.Getentry(korisnik3data)
	elf4.Parse(korisnik3data[:], uint32(StranicaDirektorijentry+0x3000))
	općioffsetTablica = elf4.Got

	PVrijednost3Poveznicamap := poveznicamap.Clone()
	PVrijednost3Poveznicamap.Append_to_list(uintptr(elf4.Dinamično))

	memorijamanager.Slobodno(korisnik3address)

	var code3Pokazivač *uintptr
	var func3val func()

	code3Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code3Pokazivač = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Pokazivač))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(StranicaDirektorijentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProcesorStanje.Ecx = korisnik3entry
	thr4.ProcesorStanje.Edx = općioffsetTablica
	thr4.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrijednost3Poveznicamap.First)))

	proceshelper.Spawn(TFunkcija1, threadhelper, sche, uint32(StranicaDirektorijentry+0x4000), true)

	iTipkovnicaDogađajhandler = &myTipkovnicaDogađajhandler
	tipkovnicadriver.Initdriver(Prekidmanager, iTipkovnicaDogađajhandler)

	mišdriver.Initdriver(Prekidmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Odaberidriver(&Drivermanager, Prekidmanager)
	uređajdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Omogućeno(true)
	Prekidmanager.Aktivan()

	for {
		halt()
	}

}
