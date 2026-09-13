package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "sampuk"
import . "multitasking"
import . "tasking/tss"

import . "virtualIngatan"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proses"
import . "driver/driver"

import . "driver/papankekunci"
import . "driver/peranti_penuding"

import . "driver/ata"
import . "failSistem/msdospartition"
import . "failSistem/fat"

import . "failSistem/format_pelaksanaan_dan_pemautan"

import . "sistemcall"

import . "ingatanmanager"
import . "pci"

func halt()

var iPapankekunciPeristiwahandler IPapankekunciPeristiwahandler

type TMyPapankekunciPeristiwahandler struct {
}

var myPapankekunciPeristiwahandler TMyPapankekunciPeristiwahandler
var papankekuncidriver TPapankekuncidriver
var tetikusdriver TTetikusdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var papankekunciconsole TConsole = TConsole{}

func (diri *TMyPapankekunciPeristiwahandler) BukaKunciTurun(kunci byte) {
	foo := [1]byte{' '}
	foo[0] = kunci

	papankekunciconsole.MCetakBaitxy(foo[:], 1000, 1000)
}

func (diri *TMyPapankekunciPeristiwahandler) BukaKunciNaik(kunci byte)	{}

var iTetikusPeristiwahandler ITetikusPeristiwahandler

type TMyTetikusPeristiwahandler struct {
}

var tetikusconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xKedudukan int16 = 0
var yKedudukan int16 = 0

func (diri *TMyTetikusPeristiwahandler) BukaTetikusTurun(butang int8) {
	buffer := []byte("x")
	tetikusconsole.MCetakxy(buffer, uint16(previousx), uint16(previousy))
}
func (diri *TMyTetikusPeristiwahandler) BukaTetikusNaik(butang int8)	{}
func (diri *TMyTetikusPeristiwahandler) BukaTetikusAlih(x int8, y int8) {

	xKedudukan += int16(x)
	if xKedudukan < 0 {
		xKedudukan = 0
	}
	if xKedudukan >= 80 {
		xKedudukan = 79
	}

	yKedudukan -= int16(y)

	if yKedudukan < 0 {
		yKedudukan = 0
	}
	if yKedudukan >= 25 {
		yKedudukan = 24
	}

	buffer := []byte(" ")
	tetikusconsole.MCetakxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	tetikusconsole.MCetakxy(buffer, uint16(xKedudukan), uint16(yKedudukan))

	previousx = xKedudukan
	previousy = yKedudukan
}

var perantidescriptor TPeripheralcomponentinterconnectPerantidescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (diri TMypcicontrollerhandler) Bukagetdriver(peranti TPeripheralcomponentinterconnectPerantidescriptor) {
	if peranti.Pembekalid == 0x1022 && peranti.Perantiid == 0x2000 {
		console.MCetakxy([]byte("["), 0, 12)
		console.MCetak(([]byte)("AMD am79c973"))
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(peranti.Pembekalid)
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(peranti.Perantiid)
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(uint16(peranti.Portbase))
		console.MCetak([]byte(":"))
		console.MUnsignedinteger32Cetak(peranti.Sampuk)

		console.MCetak([]byte("]\n"))
		perantidescriptor = peranti
		drivercount++
	}
}
func (diri TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectPerantidescriptor {
	return perantidescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Cetakstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MCetak(str)
}

func GetFailSaiz(namafail []byte) uint32 {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionJadual{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_fail32{}

	var saiz uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namafail)
	ata0s.Flush()

	return saiz
}

func Baca_fail(namafail []byte, data []byte) {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionJadual{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_fail32{}
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namafail, data)

	ata0s.Flush()
}
func Muatanelf() {

	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionJadual{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_fail32{}

	var namafail []byte = ([]byte)("TEST")
	var saiz uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namafail)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namafail, data)

	format_pelaksanaan_dan_pemautan := Elf{}

	format_pelaksanaan_dan_pemautan.Parse(data[:saiz], 0x4f00000)

}

var tugasconsole TConsole = TConsole{}

func TFungsi1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tugasa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tugasb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tugasc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tugasd()

func tugasd0() {
	esi := getesi()
	for {

		SysCetakunsignedinteger32(esi)

	}
}

func tugasd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func masukanPeristiwaTugas() {
	for {
		ProsespendingPapankekuncievents()
		ProsespendingTetikusevents()
		halt()
	}
}

func memorytest(y int) {
	ingatanmanager := &TIngatanmanager{}
	allocated := uint32(uintptr(ingatanmanager.Peruntukkan_ingatan(1024)))
	console.MUnsignedinteger32Cetakxy(allocated, 10, uint16(y))
	if y == 11 {
		ingatanmanager.Bebas(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func HentiSebentarloop()
func MuatSemulacr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Tetapkancr3(cr3 uint32)
func Getcr4() uint32
func Benarkanpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFungsiNama(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNama = runtime.FuncForPC(address).Name()
	var funcBait []byte = []byte(funcNama)

	tugasconsole.MCetakxy(funcBait, 1, 5)
	tugasconsole.MCetak(([]byte)(":"))
	tugasconsole.MUnsignedinteger32Cetak(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	tugasconsole.MCetakunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Halamandirektorientry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSiriloginit()
	console.MCetak("\n=== BRN BOOT ===\n")

	console.MCetakunsignedinteger32(uint32(Halamandirektorientry), 0, 2)
	console.MCetakunsignedinteger32(uint32(Halamandirektorientry), 10, 2)
	console.MCetakunsignedinteger32(uint32(stacktop), 0, 3)
	console.MCetakunsignedinteger32(uint32(stackbottom), 10, 3)

	ingatanmanager := &TIngatanmanager{}
	ingatanmanager.Init(0, MaksqueueSaiz)

	paging := &Paging{}
	paging.Init(Halamandirektorientry, 0x500000, ingatanmanager)
	paging.SharedIngatanregion()

	Tetapkancr3(uint32(Halamandirektorientry))
	Benarkanpaging()

	shareddescriptorJadual := &TShareddescriptorJadual{}
	shareddescriptorJadual.Init()

	console.MCetak("esp:")

	esp := getesp()
	console.MUnsignedinteger32Cetak(uint32(esp))

	tls := gettls()
	console.MCetak(([]byte)("tls:"))
	console.MUnsignedinteger32Cetak(tls)

	tss.Pasang(shareddescriptorJadual, 7, Segkerneldata, esp)

	VirtUji()

	cr3 := MuatSemulacr3()
	console.MCetak(([]byte)(":cr3:"))
	console.MUnsignedinteger32Cetak(cr3)

	cr0 := Getcr0()
	console.MCetak(([]byte)(":cr0:"))
	console.MUnsignedinteger32Cetak(cr0)

	cr4 := Getcr4()
	console.MCetak(([]byte)(":cr4:"))
	console.MUnsignedinteger32Cetak(cr4)

	tugasmanager_2 := &TTugasmanager{}
	tugasmanager_2.Init()

	Sampukmanager := &TSampukmanager{}
	Sampukmanager.Init(0x20, shareddescriptorJadual, tugasmanager_2)

	paging.Halamanfault(Sampukmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(ingatanmanager)

	proseshelper := Proseshelper{}
	proseshelper.Init(ingatanmanager, Halamandirektorientry)

	sche := &Scheduler{}
	sche.Init(Sampukmanager, ingatanmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Sampukmanager)

	proseshelper.Spawn(tugasa, threadhelper, sche, uint32(Halamandirektorientry), true)
	proseshelper.Spawn(tugasb, threadhelper, sche, uint32(Halamandirektorientry), true)
	proseshelper.Spawn(tugasc, threadhelper, sche, uint32(Halamandirektorientry), true)
	proseshelper.Spawn(tugasd1, threadhelper, sche, uint32(Halamandirektorientry), true)
	proseshelper.Spawn(masukanPeristiwaTugas, threadhelper, sche, uint32(Halamandirektorientry), true)

	var saiz uint32

	var linkerFail []byte = ([]byte)("LINKER")
	saiz = GetFailSaiz(linkerFail)
	linkeraddress := ingatanmanager.Peruntukkan_ingatan(saiz)
	linkerdata := GetBaitfromPenuding(uintptr(linkeraddress), int(saiz), int(saiz))
	Baca_fail(linkerFail, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(Halamandirektorientry))

	pautanmap := Pautanmap{}
	pautanmap.Init(ingatanmanager)

	var lib1Fail []byte = ([]byte)("LIB1")
	saiz = GetFailSaiz(lib1Fail)

	lib1address := ingatanmanager.Peruntukkan_ingatan(saiz)
	lib1data := GetBaitfromPenuding(uintptr(lib1address), int(saiz), int(saiz))
	Baca_fail(lib1Fail, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(Halamandirektorientry))
	ingatanmanager.Bebas(lib1address)

	pautanmap.Tambah_di_hujung_senarai(uintptr(lib1elf.Dynamic))

	var lib2Fail []byte = ([]byte)("LIB2")
	saiz = GetFailSaiz(lib2Fail)

	lib2address := ingatanmanager.Peruntukkan_ingatan(saiz)
	lib2data := GetBaitfromPenuding(uintptr(lib2address), int(saiz), int(saiz))
	Baca_fail(lib2Fail, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(Halamandirektorientry))
	ingatanmanager.Bebas(lib2address)

	pautanmap.Tambah_di_hujung_senarai(uintptr(lib2elf.Dynamic))

	libPautanmap := pautanmap.Clone()
	pautanmapaddress := uint32(uintptr(Pointer(libPautanmap.First)))

	lib1got := Getunsignedinteger32TatasusunanfromPenuding(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = pautanmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32TatasusunanfromPenuding(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = pautanmapaddress
	lib2got[2] = 0x4000000

	console.MCetakxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Cetak(lib1elf.Got)
	console.MCetak(":")
	console.MUnsignedinteger32Cetak(lib1elf.Dynamic)

	console.MCetakxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Cetak(lib2elf.Got)
	console.MCetak(":")
	console.MUnsignedinteger32Cetak(lib2elf.Dynamic)

	var pengguna1Fail []byte = ([]byte)("USER1")
	saiz = GetFailSaiz(pengguna1Fail)
	pengguna1address := ingatanmanager.Peruntukkan_ingatan(saiz)
	pengguna1data := GetBaitfromPenuding(uintptr(pengguna1address), int(saiz), int(saiz))
	Baca_fail(pengguna1Fail, pengguna1data)

	elf2 := Elf{}

	pengguna1entry := elf2.Getentry(pengguna1data)
	elf2.Parse(pengguna1data[:], uint32(Halamandirektorientry+0x1000))
	sejagatoffsetJadual := elf2.Got

	PNilai1Pautanmap := pautanmap.Clone()
	PNilai1Pautanmap.Tambah_di_hujung_senarai(uintptr(elf2.Dynamic))

	ingatanmanager.Bebas(pengguna1address)

	var code1Penuding *uintptr
	var func1val func()

	code1Penuding = (*uintptr)(ingatanmanager.Peruntukkan_ingatan(4))
	*code1Penuding = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Penuding))

	proc2 := proseshelper.Spawn(func1val, threadhelper, sche, uint32(Halamandirektorientry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuKeadaan.Ecx = pengguna1entry
	thr2.CpuKeadaan.Edx = sejagatoffsetJadual
	thr2.CpuKeadaan.Esi = uint32(uintptr(Pointer(PNilai1Pautanmap.First)))

	console.MCetakxy("user1: ", 1, 10)
	console.MUnsignedinteger32Cetak(elf2.Got)

	var pengguna2Fail []byte = ([]byte)("USER2")
	saiz = GetFailSaiz(pengguna2Fail)
	pengguna2address := ingatanmanager.Peruntukkan_ingatan(saiz)
	pengguna2data := GetBaitfromPenuding(uintptr(pengguna2address), int(saiz), int(saiz))
	Baca_fail(pengguna2Fail, pengguna2data)

	elf3 := Elf{}

	pengguna2entry := elf3.Getentry(pengguna2data)
	elf3.Parse(pengguna2data[:], uint32(Halamandirektorientry+0x2000))
	sejagatoffsetJadual = elf3.Got

	PNilai2Pautanmap := pautanmap.Clone()
	PNilai2Pautanmap.Tambah_di_hujung_senarai(uintptr(elf3.Dynamic))

	ingatanmanager.Bebas(pengguna2address)

	var code2Penuding *uintptr
	var func2val func()

	code2Penuding = (*uintptr)(ingatanmanager.Peruntukkan_ingatan(4))
	*code2Penuding = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Penuding))

	proc3 := proseshelper.Spawn(func2val, threadhelper, sche, uint32(Halamandirektorientry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuKeadaan.Ecx = pengguna2entry
	thr3.CpuKeadaan.Edx = sejagatoffsetJadual
	thr3.CpuKeadaan.Esi = uint32(uintptr(Pointer(PNilai2Pautanmap.First)))

	console.MCetakxy("user2: ", 1, 11)
	console.MUnsignedinteger32Cetak(thr3.CpuKeadaan.Esi)

	libPautanmap.Cetak(1, 11)

	var pengguna3Fail []byte = ([]byte)("USER3")
	saiz = GetFailSaiz(pengguna3Fail)
	pengguna3address := ingatanmanager.Peruntukkan_ingatan(saiz)
	pengguna3data := GetBaitfromPenuding(uintptr(pengguna3address), int(saiz), int(saiz))
	Baca_fail(pengguna3Fail, pengguna3data)

	elf4 := Elf{}

	pengguna3entry := elf4.Getentry(pengguna3data)
	elf4.Parse(pengguna3data[:], uint32(Halamandirektorientry+0x3000))
	sejagatoffsetJadual = elf4.Got

	PNilai3Pautanmap := pautanmap.Clone()
	PNilai3Pautanmap.Tambah_di_hujung_senarai(uintptr(elf4.Dynamic))

	ingatanmanager.Bebas(pengguna3address)

	var code3Penuding *uintptr
	var func3val func()

	code3Penuding = (*uintptr)(ingatanmanager.Peruntukkan_ingatan(4))
	*code3Penuding = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Penuding))

	proc4 := proseshelper.Spawn(func3val, threadhelper, sche, uint32(Halamandirektorientry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuKeadaan.Ecx = pengguna3entry
	thr4.CpuKeadaan.Edx = sejagatoffsetJadual
	thr4.CpuKeadaan.Esi = uint32(uintptr(Pointer(PNilai3Pautanmap.First)))

	proseshelper.Spawn(TFungsi1, threadhelper, sche, uint32(Halamandirektorientry+0x4000), true)

	iPapankekunciPeristiwahandler = &myPapankekunciPeristiwahandler
	papankekuncidriver.Initdriver(Sampukmanager, iPapankekunciPeristiwahandler)

	tetikusdriver.Initdriver(Sampukmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Pilihdriver(&Drivermanager, Sampukmanager)
	perantidescriptor = mypcicontrollerhandler.Getdriver()

	sche.Dibenarkan(true)
	Sampukmanager.Aktif()

	for {
		halt()
	}

}
