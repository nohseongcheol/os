/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "interupsi"
import . "multitasking"
import . "tasking/tss"

import . "virtualMemori"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/proses"
import . "driver/driver"

import . "driver/papanketik"
import . "driver/perangkat_penunjuk"

import . "driver/ata"
import . "berkasSistem/msdospartition"
import . "berkasSistem/fat"

import . "berkasSistem/format_eksekusi_dan_penautan"

import . "sistemcall"

import . "memorimanager"
import . "pci"

func halt()

var iPapanketikEvenhandler IPapanketikEvenhandler

type TMyPapanketikEvenhandler struct {
}

var myPapanketikEvenhandler TMyPapanketikEvenhandler
var papanketikdriver TPapanketikdriver
var tetikusdriver TTetikusdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var papanketikconsole TConsole = TConsole{}

func (dirisendiri *TMyPapanketikEvenhandler) HidupKunciBawah(kunci byte) {
	foo := [1]byte{' '}
	foo[0] = kunci

	papanketikconsole.MCetakBytexy(foo[:], 1000, 1000)
}

func (dirisendiri *TMyPapanketikEvenhandler) HidupKunciNaik(kunci byte)	{}

var iTetikusEvenhandler ITetikusEvenhandler

type TMyTetikusEvenhandler struct {
}

var tetikusconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xPosisi int16 = 0
var yPosisi int16 = 0

func (dirisendiri *TMyTetikusEvenhandler) HidupTetikusBawah(tombol int8) {
	buffer := []byte("x")
	tetikusconsole.MCetakxy(buffer, uint16(previousx), uint16(previousy))
}
func (dirisendiri *TMyTetikusEvenhandler) HidupTetikusNaik(tombol int8)	{}
func (dirisendiri *TMyTetikusEvenhandler) HidupTetikusPindah(x int8, y int8) {

	xPosisi += int16(x)
	if xPosisi < 0 {
		xPosisi = 0
	}
	if xPosisi >= 80 {
		xPosisi = 79
	}

	yPosisi -= int16(y)

	if yPosisi < 0 {
		yPosisi = 0
	}
	if yPosisi >= 25 {
		yPosisi = 24
	}

	buffer := []byte(" ")
	tetikusconsole.MCetakxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	tetikusconsole.MCetakxy(buffer, uint16(xPosisi), uint16(yPosisi))

	previousx = xPosisi
	previousy = yPosisi
}

var perangkatdescriptor TPeripheralcomponentinterconnectPerangkatdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var drivercount uint16 = 0

func (dirisendiri TMypcicontrollerhandler) Hidupgetdriver(perangkat TPeripheralcomponentinterconnectPerangkatdescriptor) {
	if perangkat.Vendorid == 0x1022 && perangkat.Perangkatid == 0x2000 {
		console.MCetakxy([]byte("["), 0, 12)
		console.MCetak(([]byte)("AMD am79c973"))
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(perangkat.Vendorid)
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(perangkat.Perangkatid)
		console.MCetak([]byte(":"))
		console.MUnsignedinteger16Cetak(uint16(perangkat.Portbase))
		console.MCetak([]byte(":"))
		console.MUnsignedinteger32Cetak(perangkat.Interupsi)

		console.MCetak([]byte("]\n"))
		perangkatdescriptor = perangkat
		drivercount++
	}
}
func (dirisendiri TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectPerangkatdescriptor {
	return perangkatdescriptor
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

func GetBerkasUkuran(namaberkas []byte) uint32 {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_berkas32{}

	var ukuran uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namaberkas)
	ata0s.Flush()

	return ukuran
}

func Baca_berkas(namaberkas []byte, data []byte) {
	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_berkas32{}
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namaberkas, data)

	ata0s.Flush()
}
func Bebanelf() {

	var ata0s = TLanjutanTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Bacapartition(&ata0s)

	bios := TParameter_sistem_berkas32{}

	var namaberkas []byte = ([]byte)("TEST")
	var ukuran uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], namaberkas)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Baca(&ata0s, partition.Mbr.Primarypartition[0], namaberkas, data)

	format_eksekusi_dan_penautan := Elf{}

	format_eksekusi_dan_penautan.Parse(data[:ukuran], 0x4f00000)

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

func masukanEvenTugas() {
	for {
		ProsespendingPapanketikKejadian()
		ProsespendingTetikusKejadian()
		halt()
	}
}

func memorytest(y int) {
	memorimanager := &TMemorimanager{}
	allocated := uint32(uintptr(memorimanager.Alokasikan_memori(1024)))
	console.MUnsignedinteger32Cetakxy(allocated, 10, uint16(y))
	if y == 11 {
		memorimanager.Bebas(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Jedaloop()
func MuatUlangcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Aturcr3(cr3 uint32)
func Getcr4() uint32
func Aktifkanpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFungsiNama(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcNama = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcNama)

	tugasconsole.MCetakxy(funcByte, 1, 5)
	tugasconsole.MCetak(([]byte)(":"))
	tugasconsole.MUnsignedinteger32Cetak(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	tugasconsole.MCetakunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentri = &Tssentri{}

func KKernelEntry(HalamanDirektorientri uintptr, stacktop uintptr, stackbottom uintptr) {

	MSerialloginit()
	console.MCetak("\n=== IDN BOOT ===\n")

	console.MCetakunsignedinteger32(uint32(HalamanDirektorientri), 0, 2)
	console.MCetakunsignedinteger32(uint32(HalamanDirektorientri), 10, 2)
	console.MCetakunsignedinteger32(uint32(stacktop), 0, 3)
	console.MCetakunsignedinteger32(uint32(stackbottom), 10, 3)

	memorimanager := &TMemorimanager{}
	memorimanager.Init(0, MaksqueueUkuran)

	paging := &Paging{}
	paging.Init(HalamanDirektorientri, 0x500000, memorimanager)
	paging.SharedMemoriregion()

	Aturcr3(uint32(HalamanDirektorientri))
	Aktifkanpaging()

	shareddescriptorTabel := &TShareddescriptorTabel{}
	shareddescriptorTabel.Init()

	console.MCetak("esp:")

	esp := getesp()
	console.MUnsignedinteger32Cetak(uint32(esp))

	tls := gettls()
	console.MCetak(([]byte)("tls:"))
	console.MUnsignedinteger32Cetak(tls)

	tss.Pasang(shareddescriptorTabel, 7, Segkerneldata, esp)

	VirtTes()

	cr3 := MuatUlangcr3()
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

	Interupsimanager := &TInterupsimanager{}
	Interupsimanager.Init(0x20, shareddescriptorTabel, tugasmanager_2)

	paging.Halamanfault(Interupsimanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(memorimanager)

	proseshelper := Proseshelper{}
	proseshelper.Init(memorimanager, HalamanDirektorientri)

	sche := &Scheduler{}
	sche.Init(Interupsimanager, memorimanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Interupsimanager)

	proseshelper.Spawn(tugasa, threadhelper, sche, uint32(HalamanDirektorientri), true)
	proseshelper.Spawn(tugasb, threadhelper, sche, uint32(HalamanDirektorientri), true)
	proseshelper.Spawn(tugasc, threadhelper, sche, uint32(HalamanDirektorientri), true)
	proseshelper.Spawn(tugasd1, threadhelper, sche, uint32(HalamanDirektorientri), true)
	proseshelper.Spawn(masukanEvenTugas, threadhelper, sche, uint32(HalamanDirektorientri), true)

	var ukuran uint32

	var linkerBerkas []byte = ([]byte)("LINKER")
	ukuran = GetBerkasUkuran(linkerBerkas)
	linkeraddress := memorimanager.Alokasikan_memori(ukuran)
	linkerdata := GetBytefromPenunjuk(uintptr(linkeraddress), int(ukuran), int(ukuran))
	Baca_berkas(linkerBerkas, linkerdata)

	elf0 := Elf{}
	linkerentri := elf0.Getentri(linkerdata)
	elf0.Parse(linkerdata[:], uint32(HalamanDirektorientri))

	tautmap := Tautmap{}
	tautmap.Init(memorimanager)

	var lib1Berkas []byte = ([]byte)("LIB1")
	ukuran = GetBerkasUkuran(lib1Berkas)

	lib1address := memorimanager.Alokasikan_memori(ukuran)
	lib1data := GetBytefromPenunjuk(uintptr(lib1address), int(ukuran), int(ukuran))
	Baca_berkas(lib1Berkas, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(HalamanDirektorientri))
	memorimanager.Bebas(lib1address)

	tautmap.Tambah_di_akhir_daftar(uintptr(lib1elf.Dinamis))

	var lib2Berkas []byte = ([]byte)("LIB2")
	ukuran = GetBerkasUkuran(lib2Berkas)

	lib2address := memorimanager.Alokasikan_memori(ukuran)
	lib2data := GetBytefromPenunjuk(uintptr(lib2address), int(ukuran), int(ukuran))
	Baca_berkas(lib2Berkas, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(HalamanDirektorientri))
	memorimanager.Bebas(lib2address)

	tautmap.Tambah_di_akhir_daftar(uintptr(lib2elf.Dinamis))

	libTautmap := tautmap.Clone()
	tautmapaddress := uint32(uintptr(Pointer(libTautmap.First)))

	lib1got := Getunsignedinteger32JajaranfromPenunjuk(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = tautmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32JajaranfromPenunjuk(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = tautmapaddress
	lib2got[2] = 0x4000000

	console.MCetakxy("lib1: ", 1, 8)
	console.MUnsignedinteger32Cetak(lib1elf.Got)
	console.MCetak(":")
	console.MUnsignedinteger32Cetak(lib1elf.Dinamis)

	console.MCetakxy("lib2: ", 1, 9)
	console.MUnsignedinteger32Cetak(lib2elf.Got)
	console.MCetak(":")
	console.MUnsignedinteger32Cetak(lib2elf.Dinamis)

	var pengguna1Berkas []byte = ([]byte)("USER1")
	ukuran = GetBerkasUkuran(pengguna1Berkas)
	pengguna1address := memorimanager.Alokasikan_memori(ukuran)
	pengguna1data := GetBytefromPenunjuk(uintptr(pengguna1address), int(ukuran), int(ukuran))
	Baca_berkas(pengguna1Berkas, pengguna1data)

	elf2 := Elf{}

	pengguna1entri := elf2.Getentri(pengguna1data)
	elf2.Parse(pengguna1data[:], uint32(HalamanDirektorientri+0x1000))
	globaloffsetTabel := elf2.Got

	PNilai1Tautmap := tautmap.Clone()
	PNilai1Tautmap.Tambah_di_akhir_daftar(uintptr(elf2.Dinamis))

	memorimanager.Bebas(pengguna1address)

	var code1Penunjuk *uintptr
	var func1val func()

	code1Penunjuk = (*uintptr)(memorimanager.Alokasikan_memori(4))
	*code1Penunjuk = uintptr(linkerentri)
	func1val = *(*func())(Pointer(&code1Penunjuk))

	proc2 := proseshelper.Spawn(func1val, threadhelper, sche, uint32(HalamanDirektorientri+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuStatus.Ecx = pengguna1entri
	thr2.CpuStatus.Edx = globaloffsetTabel
	thr2.CpuStatus.Esi = uint32(uintptr(Pointer(PNilai1Tautmap.First)))

	console.MCetakxy("user1: ", 1, 10)
	console.MUnsignedinteger32Cetak(elf2.Got)

	var pengguna2Berkas []byte = ([]byte)("USER2")
	ukuran = GetBerkasUkuran(pengguna2Berkas)
	pengguna2address := memorimanager.Alokasikan_memori(ukuran)
	pengguna2data := GetBytefromPenunjuk(uintptr(pengguna2address), int(ukuran), int(ukuran))
	Baca_berkas(pengguna2Berkas, pengguna2data)

	elf3 := Elf{}

	pengguna2entri := elf3.Getentri(pengguna2data)
	elf3.Parse(pengguna2data[:], uint32(HalamanDirektorientri+0x2000))
	globaloffsetTabel = elf3.Got

	PNilai2Tautmap := tautmap.Clone()
	PNilai2Tautmap.Tambah_di_akhir_daftar(uintptr(elf3.Dinamis))

	memorimanager.Bebas(pengguna2address)

	var code2Penunjuk *uintptr
	var func2val func()

	code2Penunjuk = (*uintptr)(memorimanager.Alokasikan_memori(4))
	*code2Penunjuk = uintptr(linkerentri)
	func2val = *(*func())(Pointer(&code2Penunjuk))

	proc3 := proseshelper.Spawn(func2val, threadhelper, sche, uint32(HalamanDirektorientri+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuStatus.Ecx = pengguna2entri
	thr3.CpuStatus.Edx = globaloffsetTabel
	thr3.CpuStatus.Esi = uint32(uintptr(Pointer(PNilai2Tautmap.First)))

	console.MCetakxy("user2: ", 1, 11)
	console.MUnsignedinteger32Cetak(thr3.CpuStatus.Esi)

	libTautmap.Cetak(1, 11)

	var pengguna3Berkas []byte = ([]byte)("USER3")
	ukuran = GetBerkasUkuran(pengguna3Berkas)
	pengguna3address := memorimanager.Alokasikan_memori(ukuran)
	pengguna3data := GetBytefromPenunjuk(uintptr(pengguna3address), int(ukuran), int(ukuran))
	Baca_berkas(pengguna3Berkas, pengguna3data)

	elf4 := Elf{}

	pengguna3entri := elf4.Getentri(pengguna3data)
	elf4.Parse(pengguna3data[:], uint32(HalamanDirektorientri+0x3000))
	globaloffsetTabel = elf4.Got

	PNilai3Tautmap := tautmap.Clone()
	PNilai3Tautmap.Tambah_di_akhir_daftar(uintptr(elf4.Dinamis))

	memorimanager.Bebas(pengguna3address)

	var code3Penunjuk *uintptr
	var func3val func()

	code3Penunjuk = (*uintptr)(memorimanager.Alokasikan_memori(4))
	*code3Penunjuk = uintptr(linkerentri)
	func3val = *(*func())(Pointer(&code3Penunjuk))

	proc4 := proseshelper.Spawn(func3val, threadhelper, sche, uint32(HalamanDirektorientri+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuStatus.Ecx = pengguna3entri
	thr4.CpuStatus.Edx = globaloffsetTabel
	thr4.CpuStatus.Esi = uint32(uintptr(Pointer(PNilai3Tautmap.First)))

	proseshelper.Spawn(TFungsi1, threadhelper, sche, uint32(HalamanDirektorientri+0x4000), true)

	iPapanketikEvenhandler = &myPapanketikEvenhandler
	papanketikdriver.Initdriver(Interupsimanager, iPapanketikEvenhandler)

	tetikusdriver.Initdriver(Interupsimanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Pilihdriver(&Drivermanager, Interupsimanager)
	perangkatdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Diaktifkan(true)
	Interupsimanager.Aktif()

	for {
		halt()
	}

}
