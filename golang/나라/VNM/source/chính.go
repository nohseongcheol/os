package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "util"
import . "gdt"
import . "console"
import . "giánđoạn"
import . "multitasking"
import . "tasking/tss"

import . "ảoBộnhớ"
import . "paging"
import . "tasking/thread"
import . "tasking/scheduler"
import . "tasking/tiếntrình"
import . "driver/driver"

import . "driver/bànphím"
import . "driver/thiết_bị_trỏ"

import . "driver/ata"
import . "tậptinHệthống/msdospartition"
import . "tậptinHệthống/fat"

import . "tậptinHệthống/định_dạng_thực_thi_và_liên_kết"

import . "hệthốngcall"

import . "bộnhớmanager"
import . "pci"

func halt()

var iBànphímSựkiệnhandler IBànphímSựkiệnhandler

type TMyBànphímSựkiệnhandler struct {
}

var myBànphímSựkiệnhandler TMyBànphímSựkiệnhandler
var bànphímdriver TBànphímdriver
var chuộtdriver TChuộtdriver
var pcicontroller TPeripheralcomponentinterconnectcontroller

var bànphímconsole TConsole = TConsole{}

func (mình *TMyBànphímSựkiệnhandler) Bậtkeydown(key byte) {
	foo := [1]byte{' '}
	foo[0] = key

	bànphímconsole.MInBytexy(foo[:], 1000, 1000)
}

func (mình *TMyBànphímSựkiệnhandler) BậtkeyLên(key byte)	{}

var iChuộtSựkiệnhandler IChuộtSựkiệnhandler

type TMyChuộtSựkiệnhandler struct {
}

var chuộtconsole TConsole = TConsole{}
var previousx int16 = 0
var previousy int16 = 0
var xVịtrí int16 = 0
var yVịtrí int16 = 0

func (mình *TMyChuộtSựkiệnhandler) BậtChuộtdown(nút int8) {
	buffer := []byte("x")
	chuộtconsole.MInxy(buffer, uint16(previousx), uint16(previousy))
}
func (mình *TMyChuộtSựkiệnhandler) BậtChuộtLên(nút int8)	{}
func (mình *TMyChuộtSựkiệnhandler) BậtChuộtDichuyển(x int8, y int8) {

	xVịtrí += int16(x)
	if xVịtrí < 0 {
		xVịtrí = 0
	}
	if xVịtrí >= 80 {
		xVịtrí = 79
	}

	yVịtrí -= int16(y)

	if yVịtrí < 0 {
		yVịtrí = 0
	}
	if yVịtrí >= 25 {
		yVịtrí = 24
	}

	buffer := []byte(" ")
	chuộtconsole.MInxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	chuộtconsole.MInxy(buffer, uint16(xVịtrí), uint16(yVịtrí))

	previousx = xVịtrí
	previousy = yVịtrí
}

var thiếtbịdescriptor TPeripheralcomponentinterconnectThiếtbịdescriptor
var ipcicontrollerhandler Ipcicontrollerhandler

type TMypcicontrollerhandler struct {
}

var console TConsole = TConsole{}
var driverSốlượng uint16 = 0

func (mình TMypcicontrollerhandler) Bậtgetdriver(thiếtbị TPeripheralcomponentinterconnectThiếtbịdescriptor) {
	if thiếtbị.NhàsảnxuấtMãsố == 0x1022 && thiếtbị.ThiếtbịMãsố == 0x2000 {
		console.MInxy([]byte("["), 0, 12)
		console.MIn(([]byte)("AMD am79c973"))
		console.MIn([]byte(":"))
		console.MUnsignedinteger16In(thiếtbị.NhàsảnxuấtMãsố)
		console.MIn([]byte(":"))
		console.MUnsignedinteger16In(thiếtbị.ThiếtbịMãsố)
		console.MIn([]byte(":"))
		console.MUnsignedinteger16In(uint16(thiếtbị.Cổngbase))
		console.MIn([]byte(":"))
		console.MUnsignedinteger32In(thiếtbị.Giánđoạn)

		console.MIn([]byte("]\n"))
		thiếtbịdescriptor = thiếtbị
		driverSốlượng++
	}
}
func (mình TMypcicontrollerhandler) Getdriver() TPeripheralcomponentinterconnectThiếtbịdescriptor {
	return thiếtbịdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Instr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	console.MIn(str)
}

func GetTậptinCỡ(têntậptin []byte) uint32 {
	var ata0s = TNângcaoCôngnghệattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionBảng{}
	partition.Đọcpartition(&ata0s)

	bios := TTham_số_hệ_thống_tệp32{}

	var cỡ uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], têntậptin)
	ata0s.Flush()

	return cỡ
}

func Đọc_tệp(têntậptin []byte, data []byte) {
	var ata0s = TNângcaoCôngnghệattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionBảng{}
	partition.Đọcpartition(&ata0s)

	bios := TTham_số_hệ_thống_tệp32{}
	bios.Đọc(&ata0s, partition.Mbr.Primarypartition[0], têntậptin, data)

	ata0s.Flush()
}
func Trọngtảielf() {

	var ata0s = TNângcaoCôngnghệattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionBảng{}
	partition.Đọcpartition(&ata0s)

	bios := TTham_số_hệ_thống_tệp32{}

	var têntậptin []byte = ([]byte)("TEST")
	var cỡ uint32 = bios.Len(&ata0s, partition.Mbr.Primarypartition[0], têntậptin)
	var databuffer [100 * 1024]byte
	var data []byte = databuffer[:]
	bios.Đọc(&ata0s, partition.Mbr.Primarypartition[0], têntậptin, data)

	định_dạng_thực_thi_và_liên_kết := Elf{}

	định_dạng_thực_thi_và_liên_kết.Parse(data[:cỡ], 0x4f00000)

}

var tácvụconsole TConsole = TConsole{}

func THàm1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func tácvụa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func tácvụb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func tácvục() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func tácvụd()

func tácvụd0() {
	esi := getesi()
	for {

		SysInunsignedinteger32(esi)

	}
}

func tácvụd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func gõSựkiệnTácvụ() {
	for {
		TiếntrìnhpendingBànphímevents()
		TiếntrìnhpendingChuộtevents()
		halt()
	}
}

func memorytest(y int) {
	bộnhớmanager := &TBộnhớmanager{}
	allocated := uint32(uintptr(bộnhớmanager.Cấp_phát_bộ_nhớ(1024)))
	console.MUnsignedinteger32Inxy(allocated, 10, uint16(y))
	if y == 11 {
		bộnhớmanager.Rảnh(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func TạmdừngVònglặp()
func Nạplạicr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Đặtcr3(cr3 uint32)
func Getcr4() uint32
func Enablepaging()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func GetHàmTên(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcTên = runtime.FuncForPC(address).Name()
	var funcByte []byte = []byte(funcTên)

	tácvụconsole.MInxy(funcByte, 1, 5)
	tácvụconsole.MIn(([]byte)(":"))
	tácvụconsole.MUnsignedinteger32In(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	tácvụconsole.MInunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(TrangThưmụcentry uintptr, stacktop uintptr, stackbottom uintptr) {

	MSốxêriloginit()
	console.MIn("\n=== VNM BOOT ===\n")

	console.MInunsignedinteger32(uint32(TrangThưmụcentry), 0, 2)
	console.MInunsignedinteger32(uint32(TrangThưmụcentry), 10, 2)
	console.MInunsignedinteger32(uint32(stacktop), 0, 3)
	console.MInunsignedinteger32(uint32(stackbottom), 10, 3)

	bộnhớmanager := &TBộnhớmanager{}
	bộnhớmanager.Init(0, MaxqueueCỡ)

	paging := &Paging{}
	paging.Init(TrangThưmụcentry, 0x500000, bộnhớmanager)
	paging.SharedBộnhớregion()

	Đặtcr3(uint32(TrangThưmụcentry))
	Enablepaging()

	shareddescriptorBảng := &TShareddescriptorBảng{}
	shareddescriptorBảng.Init()

	console.MIn("esp:")

	esp := getesp()
	console.MUnsignedinteger32In(uint32(esp))

	tls := gettls()
	console.MIn(([]byte)("tls:"))
	console.MUnsignedinteger32In(tls)

	tss.Càiđặt(shareddescriptorBảng, 7, Segkerneldata, esp)

	VirtThử()

	cr3 := Nạplạicr3()
	console.MIn(([]byte)(":cr3:"))
	console.MUnsignedinteger32In(cr3)

	cr0 := Getcr0()
	console.MIn(([]byte)(":cr0:"))
	console.MUnsignedinteger32In(cr0)

	cr4 := Getcr4()
	console.MIn(([]byte)(":cr4:"))
	console.MUnsignedinteger32In(cr4)

	tácvụmanager_2 := &TTácvụmanager{}
	tácvụmanager_2.Init()

	Giánđoạnmanager := &TGiánđoạnmanager{}
	Giánđoạnmanager.Init(0x20, shareddescriptorBảng, tácvụmanager_2)

	paging.Trangfault(Giánđoạnmanager)

	Drivermanager := TDrivermanager{}
	Drivermanager.Init()

	threadhelper := &TThreadhelper{}
	threadhelper.Init(bộnhớmanager)

	tiếntrìnhhelper := Tiếntrìnhhelper{}
	tiếntrìnhhelper.Init(bộnhớmanager, TrangThưmụcentry)

	sche := &Scheduler{}
	sche.Init(Giánđoạnmanager, bộnhớmanager, tss)

	syscall := &TSyscall{}
	syscall.Init(Giánđoạnmanager)

	tiếntrìnhhelper.Spawn(tácvụa, threadhelper, sche, uint32(TrangThưmụcentry), true)
	tiếntrìnhhelper.Spawn(tácvụb, threadhelper, sche, uint32(TrangThưmụcentry), true)
	tiếntrìnhhelper.Spawn(tácvục, threadhelper, sche, uint32(TrangThưmụcentry), true)
	tiếntrìnhhelper.Spawn(tácvụd1, threadhelper, sche, uint32(TrangThưmụcentry), true)
	tiếntrìnhhelper.Spawn(gõSựkiệnTácvụ, threadhelper, sche, uint32(TrangThưmụcentry), true)

	var cỡ uint32

	var linkerTậptin []byte = ([]byte)("LINKER")
	cỡ = GetTậptinCỡ(linkerTậptin)
	linkeraddress := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	linkerdata := GetBytefromContrỏ(uintptr(linkeraddress), int(cỡ), int(cỡ))
	Đọc_tệp(linkerTậptin, linkerdata)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerdata)
	elf0.Parse(linkerdata[:], uint32(TrangThưmụcentry))

	liênkếtmap := Liênkếtmap{}
	liênkếtmap.Init(bộnhớmanager)

	var lib1Tậptin []byte = ([]byte)("LIB1")
	cỡ = GetTậptinCỡ(lib1Tậptin)

	lib1address := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	lib1data := GetBytefromContrỏ(uintptr(lib1address), int(cỡ), int(cỡ))
	Đọc_tệp(lib1Tậptin, lib1data)

	lib1elf := Elf{}
	lib1elf.Parse(lib1data[:], uint32(TrangThưmụcentry))
	bộnhớmanager.Rảnh(lib1address)

	liênkếtmap.Thêm_vào_cuối_danh_sách(uintptr(lib1elf.Năngđộng))

	var lib2Tậptin []byte = ([]byte)("LIB2")
	cỡ = GetTậptinCỡ(lib2Tậptin)

	lib2address := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	lib2data := GetBytefromContrỏ(uintptr(lib2address), int(cỡ), int(cỡ))
	Đọc_tệp(lib2Tậptin, lib2data)

	lib2elf := Elf{}
	lib2elf.Parse(lib2data[:], uint32(TrangThưmụcentry))
	bộnhớmanager.Rảnh(lib2address)

	liênkếtmap.Thêm_vào_cuối_danh_sách(uintptr(lib2elf.Năngđộng))

	libLiênkếtmap := liênkếtmap.Clone()
	liênkếtmapaddress := uint32(uintptr(Pointer(libLiênkếtmap.Đầu)))

	lib1got := Getunsignedinteger32MảngfromContrỏ(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = liênkếtmapaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32MảngfromContrỏ(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = liênkếtmapaddress
	lib2got[2] = 0x4000000

	console.MInxy("lib1: ", 1, 8)
	console.MUnsignedinteger32In(lib1elf.Got)
	console.MIn(":")
	console.MUnsignedinteger32In(lib1elf.Năngđộng)

	console.MInxy("lib2: ", 1, 9)
	console.MUnsignedinteger32In(lib2elf.Got)
	console.MIn(":")
	console.MUnsignedinteger32In(lib2elf.Năngđộng)

	var ngườidùng1Tậptin []byte = ([]byte)("USER1")
	cỡ = GetTậptinCỡ(ngườidùng1Tậptin)
	ngườidùng1address := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	ngườidùng1data := GetBytefromContrỏ(uintptr(ngườidùng1address), int(cỡ), int(cỡ))
	Đọc_tệp(ngườidùng1Tậptin, ngườidùng1data)

	elf2 := Elf{}

	ngườidùng1entry := elf2.Getentry(ngườidùng1data)
	elf2.Parse(ngườidùng1data[:], uint32(TrangThưmụcentry+0x1000))
	toàncụcoffsetBảng := elf2.Got

	PGiátrị1Liênkếtmap := liênkếtmap.Clone()
	PGiátrị1Liênkếtmap.Thêm_vào_cuối_danh_sách(uintptr(elf2.Năngđộng))

	bộnhớmanager.Rảnh(ngườidùng1address)

	var code1Contrỏ *uintptr
	var func1val func()

	code1Contrỏ = (*uintptr)(bộnhớmanager.Cấp_phát_bộ_nhớ(4))
	*code1Contrỏ = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1Contrỏ))

	proc2 := tiếntrìnhhelper.Spawn(func1val, threadhelper, sche, uint32(TrangThưmụcentry+0x1000), false)
	thr2 := (*TThread)(proc2.Threads.Getat(0))
	thr2.CpuTrạngthái.Ecx = ngườidùng1entry
	thr2.CpuTrạngthái.Edx = toàncụcoffsetBảng
	thr2.CpuTrạngthái.Esi = uint32(uintptr(Pointer(PGiátrị1Liênkếtmap.Đầu)))

	console.MInxy("user1: ", 1, 10)
	console.MUnsignedinteger32In(elf2.Got)

	var ngườidùng2Tậptin []byte = ([]byte)("USER2")
	cỡ = GetTậptinCỡ(ngườidùng2Tậptin)
	ngườidùng2address := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	ngườidùng2data := GetBytefromContrỏ(uintptr(ngườidùng2address), int(cỡ), int(cỡ))
	Đọc_tệp(ngườidùng2Tậptin, ngườidùng2data)

	elf3 := Elf{}

	ngườidùng2entry := elf3.Getentry(ngườidùng2data)
	elf3.Parse(ngườidùng2data[:], uint32(TrangThưmụcentry+0x2000))
	toàncụcoffsetBảng = elf3.Got

	PGiátrị2Liênkếtmap := liênkếtmap.Clone()
	PGiátrị2Liênkếtmap.Thêm_vào_cuối_danh_sách(uintptr(elf3.Năngđộng))

	bộnhớmanager.Rảnh(ngườidùng2address)

	var code2Contrỏ *uintptr
	var func2val func()

	code2Contrỏ = (*uintptr)(bộnhớmanager.Cấp_phát_bộ_nhớ(4))
	*code2Contrỏ = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2Contrỏ))

	proc3 := tiếntrìnhhelper.Spawn(func2val, threadhelper, sche, uint32(TrangThưmụcentry+0x2000), false)
	thr3 := (*TThread)(proc3.Threads.Getat(0))
	thr3.CpuTrạngthái.Ecx = ngườidùng2entry
	thr3.CpuTrạngthái.Edx = toàncụcoffsetBảng
	thr3.CpuTrạngthái.Esi = uint32(uintptr(Pointer(PGiátrị2Liênkếtmap.Đầu)))

	console.MInxy("user2: ", 1, 11)
	console.MUnsignedinteger32In(thr3.CpuTrạngthái.Esi)

	libLiênkếtmap.In(1, 11)

	var ngườidùng3Tậptin []byte = ([]byte)("USER3")
	cỡ = GetTậptinCỡ(ngườidùng3Tậptin)
	ngườidùng3address := bộnhớmanager.Cấp_phát_bộ_nhớ(cỡ)
	ngườidùng3data := GetBytefromContrỏ(uintptr(ngườidùng3address), int(cỡ), int(cỡ))
	Đọc_tệp(ngườidùng3Tậptin, ngườidùng3data)

	elf4 := Elf{}

	ngườidùng3entry := elf4.Getentry(ngườidùng3data)
	elf4.Parse(ngườidùng3data[:], uint32(TrangThưmụcentry+0x3000))
	toàncụcoffsetBảng = elf4.Got

	PGiátrị3Liênkếtmap := liênkếtmap.Clone()
	PGiátrị3Liênkếtmap.Thêm_vào_cuối_danh_sách(uintptr(elf4.Năngđộng))

	bộnhớmanager.Rảnh(ngườidùng3address)

	var code3Contrỏ *uintptr
	var func3val func()

	code3Contrỏ = (*uintptr)(bộnhớmanager.Cấp_phát_bộ_nhớ(4))
	*code3Contrỏ = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3Contrỏ))

	proc4 := tiếntrìnhhelper.Spawn(func3val, threadhelper, sche, uint32(TrangThưmụcentry+0x3000), false)
	thr4 := (*TThread)(proc4.Threads.Getat(0))
	thr4.CpuTrạngthái.Ecx = ngườidùng3entry
	thr4.CpuTrạngthái.Edx = toàncụcoffsetBảng
	thr4.CpuTrạngthái.Esi = uint32(uintptr(Pointer(PGiátrị3Liênkếtmap.Đầu)))

	tiếntrìnhhelper.Spawn(THàm1, threadhelper, sche, uint32(TrangThưmụcentry+0x4000), true)

	iBànphímSựkiệnhandler = &myBànphímSựkiệnhandler
	bànphímdriver.Initdriver(Giánđoạnmanager, iBànphímSựkiệnhandler)

	chuộtdriver.Initdriver(Giánđoạnmanager, nil)

	mypcicontrollerhandler := TMypcicontrollerhandler{}
	pcicontroller.Init(mypcicontrollerhandler)
	pcicontroller.Chọndriver(&Drivermanager, Giánđoạnmanager)
	thiếtbịdescriptor = mypcicontrollerhandler.Getdriver()

	sche.Bật_2(true)
	Giánđoạnmanager.Hoạtđộng()

	for {
		halt()
	}

}
