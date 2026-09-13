package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konzola"
import . "ometanje"
import . "multitasking"
import . "tasking/tss"

import . "virtuelnoMemorija"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proces"
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

var iTastaturaDogađajhandler ITastaturaDogađajhandler

type TMyTastaturaDogađajhandler struct {
}

var myTastaturaDogađajhandler TMyTastaturaDogađajhandler
var tastaturadriver TTastaturadriver
var mišdriver TMišdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var tastaturaKonzola TKonzola = TKonzola{}

func (isti *TMyTastaturaDogađajhandler) NaKljučNiže(ključ byte) {
	foo := [1]byte{' '}
	foo[0] = ključ

	tastaturaKonzola.MŠtampajBajtovaxy(foo[:], 1000, 1000)
}

func (isti *TMyTastaturaDogađajhandler) NaKljučGore(ključ byte)	{}

var iMišDogađajhandler IMišDogađajhandler

type TMyMišDogađajhandler struct {
}

var mišKonzola TKonzola = TKonzola{}
var previousx int16 = 0
var previousy int16 = 0
var xPoložaj int16 = 0
var yPoložaj int16 = 0

func (isti *TMyMišDogađajhandler) NaMišNiže(dugme int8) {
	buffer := []byte("x")
	mišKonzola.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))
}
func (isti *TMyMišDogađajhandler) NaMišGore(dugme int8)	{}
func (isti *TMyMišDogađajhandler) NaMišPremesti(x int8, y int8) {

	xPoložaj += int16(x)
	if xPoložaj < 0 {
		xPoložaj = 0
	}
	if xPoložaj >= 80 {
		xPoložaj = 79
	}

	yPoložaj -= int16(y)

	if yPoložaj < 0 {
		yPoložaj = 0
	}
	if yPoložaj >= 25 {
		yPoložaj = 24
	}

	buffer := []byte(" ")
	mišKonzola.MŠtampajxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	mišKonzola.MŠtampajxy(buffer, uint16(xPoložaj), uint16(yPoložaj))

	previousx = xPoložaj
	previousy = yPoložaj
}

var uređajdescriptor TPeripheralcomponentinterconnectUređajdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var konzola TKonzola = TKonzola{}
var drivercount uint16 = 0

func (isti TMypcicontrollerhandler) Nagetdriver(uređaj TPeripheralcomponentinterconnectUređajdescriptor) {
	if uređaj.ProizvođačIB == 0x1022 && uređaj.UređajIB == 0x2000 {
		konzola.MŠtampajxy([]byte("["), 0, 12)
		konzola.MŠtampaj(([]byte)("AMD am79c973"))
		konzola.MŠtampaj([]byte(":"))
		konzola.MUnsignedinteger16Štampaj(uređaj.ProizvođačIB)
		konzola.MŠtampaj([]byte(":"))
		konzola.MUnsignedinteger16Štampaj(uređaj.UređajIB)
		konzola.MŠtampaj([]byte(":"))
		konzola.MUnsignedinteger16Štampaj(uint16(uređaj.Portbase))
		konzola.MŠtampaj([]byte(":"))
		konzola.MUnsignedinteger32Štampaj(uređaj.Ometanje)

		konzola.MŠtampaj([]byte("]\n"))
		uređajdescriptor = uređaj
		drivercount++
	}
}
func (isti TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectUređajdescriptor {
	return uređajdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Štampajstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konzola.MŠtampaj(str)
}

func GetDatotekaVeličina(datoteka []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Čitanjepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], datoteka)
	ata0s.Flush()

	return veličina
}

func ČitanjeDatoteka(datoteka []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Čitanjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Čitanje(&ata0s, partition.Mbr.Primarypartition[0], datoteka, data)

	ata0s.Flush()
}
func Opterećenjeelf() {

	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Čitanjepartition(&ata0s)

	bios := TBiosparameterBlok32{}

	var datoteka []byte = ([]byte)("TEST")
	var veličina uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], datoteka)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Čitanje(&ata0s, partition.Mbr.Primarypartition[0], datoteka, data)

	elf := Elf{}

	elf.Parse(data[:veličina], 0x4f00000)

}

var zadatakKonzola TKonzola = TKonzola{}

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

		SysŠtampajunsignedinteger32(esi)

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
		ProcespendingTastaturaDogađaji()
		ProcespendingMišDogađaji()
		halt()
	}
}

func memorytest(y int) {
	memorijamanager := &TMemorijamanager{}
	allocated := uint32(uintptr(memorijamanager.Malloc(1024)))
	konzola.MUnsignedinteger32Štampajxy(allocated, 10, uint16(y))
	if y == 11 {
		memorijamanager.Slobodno(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pauzaloop()
func Osvežicr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Skupcr3(cr3 uint32)
func Getcr4() uint32
func Uključenopaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetfunkcijaNaziv(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNaziv = runtime.FuncForPC(address).Name()
	var funcBajtova []byte = []byte(funcNaziv)

	zadatakKonzola.MŠtampajxy(funcBajtova, 1, 5)
	zadatakKonzola.MŠtampaj(([]byte)(":"))
	zadatakKonzola.MUnsignedinteger32Štampaj(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	zadatakKonzola.MŠtampajunsignedinteger32(cr0, 2, 1)
}

var tss *Tssunos = &Tssunos{}

func KKernelEntry(STRANADirektorijumunos uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerijskiDnevnikinit()
	konzola.MŠtampaj("\n=== MNE BOOT ===\n")

	konzola.MŠtampajunsignedinteger32(uint32(STRANADirektorijumunos), 0, 2)
	konzola.MŠtampajunsignedinteger32(uint32(STRANADirektorijumunos), 10, 2)
	konzola.MŠtampajunsignedinteger32(uint32(stacktop), 0, 3)
	konzola.MŠtampajunsignedinteger32(uint32(stackbottom), 10, 3)

	memorijamanager := &TMemorijamanager{}
	memorijamanager.Init(0, MaksqueueVeličina)

	paging := &Paging{}
	paging.Init(STRANADirektorijumunos, 0x500000, memorijamanager)
	paging.SharedMemorijaregion()

	Skupcr3(uint32(STRANADirektorijumunos))
	Uključenopaging()

	shareddescriptorTabela := &TShareddescriptorTabela{}
	shareddescriptorTabela.Init()

	konzola.MŠtampaj("esp:")

	esp := getesp()
	konzola.MUnsignedinteger32Štampaj(uint32(esp))

	tls := gettls()
	konzola.MŠtampaj(([]byte)("tls:"))
	konzola.MUnsignedinteger32Štampaj(tls)

	tss.Instaliraj(shareddescriptorTabela, 7, Segkerneldata, esp)

	VirtTest()

	cr3 := Osvežicr3()
	konzola.MŠtampaj(([]byte)(":cr3:"))
	konzola.MUnsignedinteger32Štampaj(cr3)

	cr0 := Getcr0()
	konzola.MŠtampaj(([]byte)(":cr0:"))
	konzola.MUnsignedinteger32Štampaj(cr0)

	cr4 := Getcr4()
	konzola.MŠtampaj(([]byte)(":cr4:"))
	konzola.MUnsignedinteger32Štampaj(cr4)

	zadatakmanager_2 := &TZadatakmanager{}
	zadatakmanager_2.Init()

	Ometanjemanager := &TOmetanjemanager{}
	Ometanjemanager.Init(0x20, shareddescriptorTabela, zadatakmanager_2)

	paging.STRANAfault(Ometanjemanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorijamanager)

	proceshelper := Proceshelper{}
	proceshelper.Init(memorijamanager, STRANADirektorijumunos)

	sche := &Scheduler{}
	sche.Init(Ometanjemanager, memorijamanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Ometanjemanager)

	proceshelper.Spawn(zadataka, threadhelper, sche, uint32(STRANADirektorijumunos), true)
	proceshelper.Spawn(zadatakb, threadhelper, sche, uint32(STRANADirektorijumunos), true)
	proceshelper.Spawn(zadatakc, threadhelper, sche, uint32(STRANADirektorijumunos), true)
	proceshelper.Spawn(zadatakd1, threadhelper, sche, uint32(STRANADirektorijumunos), true)
	proceshelper.Spawn(ulazDogađajZadatak, threadhelper, sche, uint32(STRANADirektorijumunos), true)

	var veličina uint32

	var linkerDatoteka []byte = ([]byte)("LINKER")
	veličina = GetDatotekaVeličina(linkerDatoteka)
	linkeraddress := memorijamanager.Malloc(veličina)
	linkerdata := GetBajtovasaPokazivač(uintptr(linkeraddress), int(veličina), int(veličina))
	ČitanjeDatoteka(linkerDatoteka, linkerdata)

	elf0 := Elf{}
	linkerunos := elf0.Getunos(linkerdata)
	elf0.Parse(linkerdata[:], uint32(STRANADirektorijumunos))

	vezamap := Vezamap{}
	vezamap.Init(memorijamanager)

	var lib1Datoteka []byte = ([]byte)("LIB1")
	veličina = GetDatotekaVeličina(lib1Datoteka)

	lib1address := memorijamanager.Malloc(veličina)
	lib1data := GetBajtovasaPokazivač(uintptr(lib1address), int(veličina), int(veličina))
	ČitanjeDatoteka(lib1Datoteka, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(STRANADirektorijumunos))
	memorijamanager.Slobodno(lib1address)

	vezamap.Append_to_list(uintptr(lib1elf.Rastegljivo))

	var lib2Datoteka []byte = ([]byte)("LIB2")
	veličina = GetDatotekaVeličina(lib2Datoteka)

	lib2address := memorijamanager.Malloc(veličina)
	lib2data := GetBajtovasaPokazivač(uintptr(lib2address), int(veličina), int(veličina))
	ČitanjeDatoteka(lib2Datoteka, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(STRANADirektorijumunos))
	memorijamanager.Slobodno(lib2address)

	vezamap.Append_to_list(uintptr(lib2elf.Rastegljivo))

	libVezamap := vezamap.Clone()
	vezamapaddress := uint32(uintptr(Pointer(libVezamap.First)))

	lib1got := Getunsignedinteger32NizsaPokazivač(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = vezamapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32NizsaPokazivač(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = vezamapaddress
	lib2got[2] = 0x4000000

	konzola.MŠtampajxy("lib1: ", 1, 8)
	konzola.MUnsignedinteger32Štampaj(lib1elf.Got)
	konzola.MŠtampaj(":")
	konzola.MUnsignedinteger32Štampaj(lib1elf.Rastegljivo)

	konzola.MŠtampajxy("lib2: ", 1, 9)
	konzola.MUnsignedinteger32Štampaj(lib2elf.Got)
	konzola.MŠtampaj(":")
	konzola.MUnsignedinteger32Štampaj(lib2elf.Rastegljivo)

	var korisnik1Datoteka []byte = ([]byte)("USER1")
	veličina = GetDatotekaVeličina(korisnik1Datoteka)
	korisnik1address := memorijamanager.Malloc(veličina)
	korisnik1data := GetBajtovasaPokazivač(uintptr(korisnik1address), int(veličina), int(veličina))
	ČitanjeDatoteka(korisnik1Datoteka, korisnik1data)

	elf2 := Elf{}

	korisnik1unos := elf2.Getunos(korisnik1data)
	elf2.Parse(korisnik1data[:], uint32(STRANADirektorijumunos+0x1000))
	opšteoffsetTabela := elf2.Got

	PVrednost1Vezamap := vezamap.Clone()
	PVrednost1Vezamap.Append_to_list(uintptr(elf2.Rastegljivo))

	memorijamanager.Slobodno(korisnik1address)

	var code1Pokazivač *uintptr
	var func1val func()

	code1Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code1Pokazivač = uintptr(linkerunos)
	func1val = *(*func())(Pointer(&code1Pokazivač))

	proc2 := proceshelper.Spawn(func1val, threadhelper, sche, uint32(STRANADirektorijumunos+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.ProcesorStanje.Ecx = korisnik1unos
	thr2.ProcesorStanje.Edx = opšteoffsetTabela
	thr2.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrednost1Vezamap.First)))

	konzola.MŠtampajxy("user1: ", 1, 10)
	konzola.MUnsignedinteger32Štampaj(elf2.Got)

	var korisnik2Datoteka []byte = ([]byte)("USER2")
	veličina = GetDatotekaVeličina(korisnik2Datoteka)
	korisnik2address := memorijamanager.Malloc(veličina)
	korisnik2data := GetBajtovasaPokazivač(uintptr(korisnik2address), int(veličina), int(veličina))
	ČitanjeDatoteka(korisnik2Datoteka, korisnik2data)

	elf3 := Elf{}

	korisnik2unos := elf3.Getunos(korisnik2data)
	elf3.Parse(korisnik2data[:], uint32(STRANADirektorijumunos+0x2000))
	opšteoffsetTabela = elf3.Got

	PVrednost2Vezamap := vezamap.Clone()
	PVrednost2Vezamap.Append_to_list(uintptr(elf3.Rastegljivo))

	memorijamanager.Slobodno(korisnik2address)

	var code2Pokazivač *uintptr
	var func2val func()

	code2Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code2Pokazivač = uintptr(linkerunos)
	func2val = *(*func())(Pointer(&code2Pokazivač))

	proc3 := proceshelper.Spawn(func2val, threadhelper, sche, uint32(STRANADirektorijumunos+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.ProcesorStanje.Ecx = korisnik2unos
	thr3.ProcesorStanje.Edx = opšteoffsetTabela
	thr3.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrednost2Vezamap.First)))

	konzola.MŠtampajxy("user2: ", 1, 11)
	konzola.MUnsignedinteger32Štampaj(thr3.ProcesorStanje.Esi)

	libVezamap.Štampaj(1, 11)

	var korisnik3Datoteka []byte = ([]byte)("USER3")
	veličina = GetDatotekaVeličina(korisnik3Datoteka)
	korisnik3address := memorijamanager.Malloc(veličina)
	korisnik3data := GetBajtovasaPokazivač(uintptr(korisnik3address), int(veličina), int(veličina))
	ČitanjeDatoteka(korisnik3Datoteka, korisnik3data)

	elf4 := Elf{}

	korisnik3unos := elf4.Getunos(korisnik3data)
	elf4.Parse(korisnik3data[:], uint32(STRANADirektorijumunos+0x3000))
	opšteoffsetTabela = elf4.Got

	PVrednost3Vezamap := vezamap.Clone()
	PVrednost3Vezamap.Append_to_list(uintptr(elf4.Rastegljivo))

	memorijamanager.Slobodno(korisnik3address)

	var code3Pokazivač *uintptr
	var func3val func()

	code3Pokazivač = (*uintptr)(memorijamanager.Malloc(4))
	*code3Pokazivač = uintptr(linkerunos)
	func3val = *(*func())(Pointer(&code3Pokazivač))

	proc4 := proceshelper.Spawn(func3val, threadhelper, sche, uint32(STRANADirektorijumunos+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.ProcesorStanje.Ecx = korisnik3unos
	thr4.ProcesorStanje.Edx = opšteoffsetTabela
	thr4.ProcesorStanje.Esi = uint32(uintptr(Pointer(PVrednost3Vezamap.First)))

	proceshelper.Spawn(TFunkcija1, threadhelper, sche, uint32(STRANADirektorijumunos+0x4000), true)

	iTastaturaDogađajhandler = &myTastaturaDogađajhandler
	tastaturadriver.Initdriver(Ometanjemanager, iTastaturaDogađajhandler)

	mišdriver.Initdriver(Ometanjemanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Izaberidriver(&Drivermanager, Ometanjemanager)
	uređajdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Omogućeno(true)
	Ometanjemanager.Aktivna()

	for {
		halt()
	}

}
