package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "konsol"
import . "kesme"
import . "multitasking"
import . "tasking/tss"

import . "sanalBellek"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/süreç"
import . "driver/driver"

import . "driver/klavye"
import . "driver/işaretleme_aygıtı"

import . "driver/ata"
import . "dosyaSistem/msdospartition"
import . "dosyaSistem/fat"

import . "dosyaSistem/çalıştırılabilir_ve_bağlanabilir_biçim"

import . "sistemcall"

import . "bellekmanager"
import . "pci"

func halt()

var iKlavyeOlayhandler IKlavyeOlayhandler

type TMyKlavyeOlayhandler struct {
}

var myKlavyeOlayhandler TMyKlavyeOlayhandler
var klavyedriver TKlavyedriver
var faredriver TFaredriver
var pciDenetleyici TPeripheralcomponentinterconnectDenetleyici

var klavyeKonsol TKonsol = TKonsol{}

func (self *TMyKlavyeOlayhandler) AçıkAnahtarAşağı(anahtar byte) {
	foo := [1]byte{' '}
	foo[0] = anahtar

	klavyeKonsol.MYazdırBaytxy(foo[:], 1000, 1000)
}

func (self *TMyKlavyeOlayhandler) AçıkAnahtarYukarı(anahtar byte)	{}

var iFareOlayhandler IFareOlayhandler

type TMyFareOlayhandler struct {
}

var fareKonsol TKonsol = TKonsol{}
var previousx int16 = 0
var previousy int16 = 0
var xKonum int16 = 0
var yKonum int16 = 0

func (self *TMyFareOlayhandler) AçıkFareAşağı(düğme int8) {
	buffer := []byte("x")
	fareKonsol.MYazdırxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyFareOlayhandler) AçıkFareYukarı(düğme int8)	{}
func (self *TMyFareOlayhandler) AçıkFareTaşı(x int8, y int8) {

	xKonum += int16(x)
	if xKonum < 0 {
		xKonum = 0
	}
	if xKonum >= 80 {
		xKonum = 79
	}

	yKonum -= int16(y)

	if yKonum < 0 {
		yKonum = 0
	}
	if yKonum >= 25 {
		yKonum = 24
	}

	buffer := []byte(" ")
	fareKonsol.MYazdırxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	fareKonsol.MYazdırxy(buffer, uint16(xKonum), uint16(yKonum))

	previousx = xKonum
	previousy = yKonum
}

var aygıtdescriptor TPeripheralcomponentinterconnectAygıtdescriptor
var ipciDenetleyicihandler IpciDenetleyicihandler

type TMypciDenetleyicihandler struct {
}

var konsol TKonsol = TKonsol{}
var drivercount uint16 = 0

func (self TMypciDenetleyicihandler) Açıkgetdriver(aygıt TPeripheralcomponentinterconnectAygıtdescriptor) {
	if aygıt.ÜreticiNo == 0x1022 && aygıt.AygıtNo == 0x2000 {
		konsol.MYazdırxy([]byte("["), 0, 12)
		konsol.MYazdır(([]byte)("AMD am79c973"))
		konsol.MYazdır([]byte(":"))
		konsol.MUnsignedinteger16Yazdır(aygıt.ÜreticiNo)
		konsol.MYazdır([]byte(":"))
		konsol.MUnsignedinteger16Yazdır(aygıt.AygıtNo)
		konsol.MYazdır([]byte(":"))
		konsol.MUnsignedinteger16Yazdır(uint16(aygıt.BağlantıNoktasıbase))
		konsol.MYazdır([]byte(":"))
		konsol.MUnsignedinteger32Yazdır(aygıt.Kesme)

		konsol.MYazdır([]byte("]\n"))
		aygıtdescriptor = aygıt
		drivercount++
	}
}
func (self TMypciDenetleyicihandler) Getdriver() TPeripheralcomponentinterconnectAygıtdescriptor {
	return aygıtdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Yazdırstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	konsol.MYazdır(str)
}

func GetDosyaBoyut(dosyaadı []byte) uint32 {
	var ata0s = TGelişmişTeknolojiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablo{}
	partition.Okumapartition(&ata0s)

	bios := TDosya_sistemi_parametreleri32{}

	var boyut uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı)
	ata0s.Flush()

	return boyut
}

func Dosya_oku(dosyaadı []byte, data []byte) {
	var ata0s = TGelişmişTeknolojiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablo{}
	partition.Okumapartition(&ata0s)

	bios := TDosya_sistemi_parametreleri32{}
	bios.Okuma(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı, data)

	ata0s.Flush()
}
func Yükelf() {

	var ata0s = TGelişmişTeknolojiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTablo{}
	partition.Okumapartition(&ata0s)

	bios := TDosya_sistemi_parametreleri32{}

	var dosyaadı []byte = ([]byte)("TEST")
	var boyut uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Okuma(&ata0s, partition.Mbr.Primarypartition[0], dosyaadı, data)

	çalıştırılabilir_ve_bağlanabilir_biçim := Elf{}

	çalıştırılabilir_ve_bağlanabilir_biçim.Parse(data[:boyut], 0x4f00000)

}

var görevKonsol TKonsol = TKonsol{}

func TFonksiyon1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func göreva() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func görevb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func görevc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func görevd()

func görevd0() {
	esi := getesi()
	for {

		SysYazdırunsignedinteger32(esi)

	}
}

func görevd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func girdiOlayGörev() {
	for {
		SüreçpendingKlavyeOlaylar()
		SüreçpendingFareOlaylar()
		halt()
	}
}

func memorytest(y int) {
	bellekmanager := &TBellekmanager{}
	allocated := uint32(uintptr(bellekmanager.Bellek_ayır(1024)))
	konsol.MUnsignedinteger32Yazdırxy(allocated, 10, uint16(y))
	if y == 11 {
		bellekmanager.Boş(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Duraklatloop()
func YenidenYüklecr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Ayarlacr3(cr3 uint32)
func Getcr4() uint32
func Etkinleştirpaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetFonksiyonİsim(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcİsim = runtime.FuncForPC(address).Name()
	var funcBayt []byte = []byte(funcİsim)

	görevKonsol.MYazdırxy(funcBayt, 1, 5)
	görevKonsol.MYazdır(([]byte)(":"))
	görevKonsol.MUnsignedinteger32Yazdır(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	görevKonsol.MYazdırunsignedinteger32(cr0, 2, 1)
}

var tss *Tssgirdi = &Tssgirdi{}

func KKernelEntry(SayfaDizingirdi uintptr, stacktop uintptr, stackbottom uintptr) {

	MSeriGünlükinit()
	konsol.MYazdır("\n=== TUR BOOT ===\n")

	konsol.MYazdırunsignedinteger32(uint32(SayfaDizingirdi), 0, 2)
	konsol.MYazdırunsignedinteger32(uint32(SayfaDizingirdi), 10, 2)
	konsol.MYazdırunsignedinteger32(uint32(stacktop), 0, 3)
	konsol.MYazdırunsignedinteger32(uint32(stackbottom), 10, 3)

	bellekmanager := &TBellekmanager{}
	bellekmanager.Init(0, MakqueueBoyut)

	paging := &Paging{}
	paging.Init(SayfaDizingirdi, 0x500000, bellekmanager)
	paging.SharedBellekregion()

	Ayarlacr3(uint32(SayfaDizingirdi))
	Etkinleştirpaging()

	shareddescriptorTablo := &TShareddescriptorTablo{}
	shareddescriptorTablo.Init()

	konsol.MYazdır("esp:")

	esp := getesp()
	konsol.MUnsignedinteger32Yazdır(uint32(esp))

	tls := gettls()
	konsol.MYazdır(([]byte)("tls:"))
	konsol.MUnsignedinteger32Yazdır(tls)

	tss.Kur(shareddescriptorTablo, 7, Segkerneldata, esp)

	VirtDene()

	cr3 := YenidenYüklecr3()
	konsol.MYazdır(([]byte)(":cr3:"))
	konsol.MUnsignedinteger32Yazdır(cr3)

	cr0 := Getcr0()
	konsol.MYazdır(([]byte)(":cr0:"))
	konsol.MUnsignedinteger32Yazdır(cr0)

	cr4 := Getcr4()
	konsol.MYazdır(([]byte)(":cr4:"))
	konsol.MUnsignedinteger32Yazdır(cr4)

	görevmanager_2 := &TGörevmanager{}
	görevmanager_2.Init()

	Kesmemanager := &TKesmemanager{}
	Kesmemanager.Init(0x20, shareddescriptorTablo, görevmanager_2)

	paging.Sayfafault(Kesmemanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(bellekmanager)

	süreçhelper := Süreçhelper{}
	süreçhelper.Init(bellekmanager, SayfaDizingirdi)

	sche := &Scheduler{}
	sche.Init(Kesmemanager, bellekmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Kesmemanager)

	süreçhelper.Spawn(göreva, threadhelper, sche, uint32(SayfaDizingirdi), true)
	süreçhelper.Spawn(görevb, threadhelper, sche, uint32(SayfaDizingirdi), true)
	süreçhelper.Spawn(görevc, threadhelper, sche, uint32(SayfaDizingirdi), true)
	süreçhelper.Spawn(görevd1, threadhelper, sche, uint32(SayfaDizingirdi), true)
	süreçhelper.Spawn(girdiOlayGörev, threadhelper, sche, uint32(SayfaDizingirdi), true)

	var boyut uint32

	var linkerDosya []byte = ([]byte)("LINKER")
	boyut = GetDosyaBoyut(linkerDosya)
	linkeraddress := bellekmanager.Bellek_ayır(boyut)
	linkerdata := GetBaytfromBelirteç(uintptr(linkeraddress), int(boyut), int(boyut))
	Dosya_oku(linkerDosya, linkerdata)

	elf0 := Elf{}
	linkergirdi := elf0.Getgirdi(linkerdata)
	elf0.Parse(linkerdata[:], uint32(SayfaDizingirdi))

	bağmap := Bağmap{}
	bağmap.Init(bellekmanager)

	var lib1Dosya []byte = ([]byte)("LIB1")
	boyut = GetDosyaBoyut(lib1Dosya)

	lib1address := bellekmanager.Bellek_ayır(boyut)
	lib1data := GetBaytfromBelirteç(uintptr(lib1address), int(boyut), int(boyut))
	Dosya_oku(lib1Dosya, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(SayfaDizingirdi))
	bellekmanager.Boş(lib1address)

	bağmap.Listenin_sonuna_ekle(uintptr(lib1elf.Devingen))

	var lib2Dosya []byte = ([]byte)("LIB2")
	boyut = GetDosyaBoyut(lib2Dosya)

	lib2address := bellekmanager.Bellek_ayır(boyut)
	lib2data := GetBaytfromBelirteç(uintptr(lib2address), int(boyut), int(boyut))
	Dosya_oku(lib2Dosya, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(SayfaDizingirdi))
	bellekmanager.Boş(lib2address)

	bağmap.Listenin_sonuna_ekle(uintptr(lib2elf.Devingen))

	libBağmap := bağmap.Clone()
	bağmapaddress := uint32(uintptr(Pointer(libBağmap.First)))

	lib1got := Getunsignedinteger32DizifromBelirteç(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = bağmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32DizifromBelirteç(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = bağmapaddress
	lib2got[2] = 0x4000000

	konsol.MYazdırxy("lib1: ", 1, 8)
	konsol.MUnsignedinteger32Yazdır(lib1elf.Got)
	konsol.MYazdır(":")
	konsol.MUnsignedinteger32Yazdır(lib1elf.Devingen)

	konsol.MYazdırxy("lib2: ", 1, 9)
	konsol.MUnsignedinteger32Yazdır(lib2elf.Got)
	konsol.MYazdır(":")
	konsol.MUnsignedinteger32Yazdır(lib2elf.Devingen)

	var kullanıcı1Dosya []byte = ([]byte)("USER1")
	boyut = GetDosyaBoyut(kullanıcı1Dosya)
	kullanıcı1address := bellekmanager.Bellek_ayır(boyut)
	kullanıcı1data := GetBaytfromBelirteç(uintptr(kullanıcı1address), int(boyut), int(boyut))
	Dosya_oku(kullanıcı1Dosya, kullanıcı1data)

	elf2 := Elf{}

	kullanıcı1girdi := elf2.Getgirdi(kullanıcı1data)
	elf2.Parse(kullanıcı1data[:], uint32(SayfaDizingirdi+0x1000))
	geneloffsetTablo := elf2.Got

	PDeğer1Bağmap := bağmap.Clone()
	PDeğer1Bağmap.Listenin_sonuna_ekle(uintptr(elf2.Devingen))

	bellekmanager.Boş(kullanıcı1address)

	var code1Belirteç *uintptr
	var func1val func()

	code1Belirteç = (*uintptr)(bellekmanager.Bellek_ayır(4))
	*code1Belirteç = uintptr(linkergirdi)
	func1val = *(*func())(Pointer(&code1Belirteç))

	proc2 := süreçhelper.Spawn(func1val, threadhelper, sche, uint32(SayfaDizingirdi+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.MİBDurum.Ecx = kullanıcı1girdi
	thr2.MİBDurum.Edx = geneloffsetTablo
	thr2.MİBDurum.Esi = uint32(uintptr(Pointer(PDeğer1Bağmap.First)))

	konsol.MYazdırxy("user1: ", 1, 10)
	konsol.MUnsignedinteger32Yazdır(elf2.Got)

	var kullanıcı2Dosya []byte = ([]byte)("USER2")
	boyut = GetDosyaBoyut(kullanıcı2Dosya)
	kullanıcı2address := bellekmanager.Bellek_ayır(boyut)
	kullanıcı2data := GetBaytfromBelirteç(uintptr(kullanıcı2address), int(boyut), int(boyut))
	Dosya_oku(kullanıcı2Dosya, kullanıcı2data)

	elf3 := Elf{}

	kullanıcı2girdi := elf3.Getgirdi(kullanıcı2data)
	elf3.Parse(kullanıcı2data[:], uint32(SayfaDizingirdi+0x2000))
	geneloffsetTablo = elf3.Got

	PDeğer2Bağmap := bağmap.Clone()
	PDeğer2Bağmap.Listenin_sonuna_ekle(uintptr(elf3.Devingen))

	bellekmanager.Boş(kullanıcı2address)

	var code2Belirteç *uintptr
	var func2val func()

	code2Belirteç = (*uintptr)(bellekmanager.Bellek_ayır(4))
	*code2Belirteç = uintptr(linkergirdi)
	func2val = *(*func())(Pointer(&code2Belirteç))

	proc3 := süreçhelper.Spawn(func2val, threadhelper, sche, uint32(SayfaDizingirdi+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.MİBDurum.Ecx = kullanıcı2girdi
	thr3.MİBDurum.Edx = geneloffsetTablo
	thr3.MİBDurum.Esi = uint32(uintptr(Pointer(PDeğer2Bağmap.First)))

	konsol.MYazdırxy("user2: ", 1, 11)
	konsol.MUnsignedinteger32Yazdır(thr3.MİBDurum.Esi)

	libBağmap.Yazdır(1, 11)

	var kullanıcı3Dosya []byte = ([]byte)("USER3")
	boyut = GetDosyaBoyut(kullanıcı3Dosya)
	kullanıcı3address := bellekmanager.Bellek_ayır(boyut)
	kullanıcı3data := GetBaytfromBelirteç(uintptr(kullanıcı3address), int(boyut), int(boyut))
	Dosya_oku(kullanıcı3Dosya, kullanıcı3data)

	elf4 := Elf{}

	kullanıcı3girdi := elf4.Getgirdi(kullanıcı3data)
	elf4.Parse(kullanıcı3data[:], uint32(SayfaDizingirdi+0x3000))
	geneloffsetTablo = elf4.Got

	PDeğer3Bağmap := bağmap.Clone()
	PDeğer3Bağmap.Listenin_sonuna_ekle(uintptr(elf4.Devingen))

	bellekmanager.Boş(kullanıcı3address)

	var code3Belirteç *uintptr
	var func3val func()

	code3Belirteç = (*uintptr)(bellekmanager.Bellek_ayır(4))
	*code3Belirteç = uintptr(linkergirdi)
	func3val = *(*func())(Pointer(&code3Belirteç))

	proc4 := süreçhelper.Spawn(func3val, threadhelper, sche, uint32(SayfaDizingirdi+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.MİBDurum.Ecx = kullanıcı3girdi
	thr4.MİBDurum.Edx = geneloffsetTablo
	thr4.MİBDurum.Esi = uint32(uintptr(Pointer(PDeğer3Bağmap.First)))

	süreçhelper.Spawn(TFonksiyon1, threadhelper, sche, uint32(SayfaDizingirdi+0x4000), true)

	iKlavyeOlayhandler = &myKlavyeOlayhandler
	klavyedriver.Initdriver(Kesmemanager, iKlavyeOlayhandler)

	faredriver.Initdriver(Kesmemanager, nil)

	mypciDenetleyicihandler := TMypciDenetleyicihandler{}
	pciDenetleyici.Init(mypciDenetleyicihandler)
	pciDenetleyici.Seçdriver(&Drivermanager, Kesmemanager)
	aygıtdescriptor = mypciDenetleyicihandler.Getdriver()

	sche.Etkin(true)
	Kesmemanager.Aktif()

	for {
		halt()
	}

}
