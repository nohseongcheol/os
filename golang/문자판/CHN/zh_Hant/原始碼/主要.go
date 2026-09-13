package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "工具"
import . "gdt"
import . "控制台"
import . "中斷"
import . "多重工作管理"
import . "工作管理/tss"

import . "虛擬記憶體"
import . "分頁管理"
import . "工作管理/執行緒"
import . "工作管理/排程器"
import . "工作管理/程序"
import . "驅動程式/驅動程式"

import . "驅動程式/鍵盤"
import . "驅動程式/指向裝置"

import . "驅動程式/ata"
import . "檔案系統/msdos分割區"
import . "檔案系統/fat"

import . "檔案系統/可執行與可連結格式"

import . "系統呼叫"

import . "記憶體管理器"
import . "pci"

func halt()

var i鍵盤事件handler I鍵盤事件handler

type TMy鍵盤事件handler struct {
}

var my鍵盤事件handler TMy鍵盤事件handler
var 鍵盤驅動程式 T鍵盤驅動程式
var 滑鼠驅動程式 T滑鼠驅動程式
var pci控制器 TPeripheralcomponentinterconnect控制器

var 鍵盤控制台 T控制台 = T控制台{}

func (self *TMy鍵盤事件handler) O時設定鍵下(設定鍵 byte) {
	foo := [1]byte{' '}
	foo[0] = 設定鍵

	鍵盤控制台.M列印位元組xy(foo[:], 1000, 1000)
}

func (self *TMy鍵盤事件handler) O時設定鍵上(設定鍵 byte)	{}

var i滑鼠事件handler I滑鼠事件handler

type TMy滑鼠事件handler struct {
}

var 滑鼠控制台 T控制台 = T控制台{}
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self *TMy滑鼠事件handler) O時滑鼠下(按鈕 int8) {
	buffer := []byte("x")
	滑鼠控制台.M列印xy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMy滑鼠事件handler) O時滑鼠上(按鈕 int8)	{}
func (self *TMy滑鼠事件handler) O時滑鼠移動(x int8, y int8) {

	x位置 += int16(x)
	if x位置 < 0 {
		x位置 = 0
	}
	if x位置 >= 80 {
		x位置 = 79
	}

	y位置 -= int16(y)

	if y位置 < 0 {
		y位置 = 0
	}
	if y位置 >= 25 {
		y位置 = 24
	}

	buffer := []byte(" ")
	滑鼠控制台.M列印xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	滑鼠控制台.M列印xy(buffer, uint16(x位置), uint16(y位置))

	previousx = x位置
	previousy = y位置
}

var 裝置descriptor TPeripheralcomponentinterconnect裝置descriptor
var ipci控制器handler Ipci控制器handler

type TMypci控制器handler struct {
}

var 控制台 T控制台 = T控制台{}
var 驅動程式計數 uint16 = 0

func (self TMypci控制器handler) O時get驅動程式(裝置 TPeripheralcomponentinterconnect裝置descriptor) {
	if 裝置.V廠商識別號 == 0x1022 && 裝置.D裝置識別號 == 0x2000 {
		控制台.M列印xy([]byte("["), 0, 12)
		控制台.M列印(([]byte)("AMD am79c973"))
		控制台.M列印([]byte(":"))
		控制台.MUnsignedinteger16列印(裝置.V廠商識別號)
		控制台.M列印([]byte(":"))
		控制台.MUnsignedinteger16列印(裝置.D裝置識別號)
		控制台.M列印([]byte(":"))
		控制台.MUnsignedinteger16列印(uint16(裝置.P連接埠base))
		控制台.M列印([]byte(":"))
		控制台.MUnsignedinteger32列印(裝置.I中斷)

		控制台.M列印([]byte("]\n"))
		裝置descriptor = 裝置
		驅動程式計數++
	}
}
func (self TMypci控制器handler) Get驅動程式() TPeripheralcomponentinterconnect裝置descriptor {
	return 裝置descriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func P列印str(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	控制台.M列印(str)
}

func Get檔案大小(檔案名稱 []byte) uint32 {
	var ata0s = T進階科技attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分割區 := Tmsdos分割區table{}
	分割區.R讀取分割區(&ata0s)

	bios := T檔案系統參數32{}

	var 大小 uint32 = bios.Len(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱)
	ata0s.Flush()

	return 大小
}

func M讀取檔案(檔案名稱 []byte, 資料 []byte) {
	var ata0s = T進階科技attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分割區 := Tmsdos分割區table{}
	分割區.R讀取分割區(&ata0s)

	bios := T檔案系統參數32{}
	bios.R讀取(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱, 資料)

	ata0s.Flush()
}
func L載入elf() {

	var ata0s = T進階科技attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分割區 := Tmsdos分割區table{}
	分割區.R讀取分割區(&ata0s)

	bios := T檔案系統參數32{}

	var 檔案名稱 []byte = ([]byte)("TEST")
	var 大小 uint32 = bios.Len(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱)
	var 資料buffer [100 * 1024]byte
	var 資料 []byte = 資料buffer[:]
	bios.R讀取(&ata0s, 分割區.Mbr.Primary分割區[0], 檔案名稱, 資料)

	可執行與可連結格式 := Elf{}

	可執行與可連結格式.Parse(資料[:大小], 0x4f00000)

}

var 工作控制台 T控制台 = T控制台{}

func T函式1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func 工作a() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func 工作b() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func 工作c() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func 工作d()

func 工作d0() {
	esi := getesi()
	for {

		Sys列印unsignedinteger32(esi)

	}
}

func 工作d1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func 輸入事件工作() {
	for {
		P程序待處理鍵盤事件集()
		P程序待處理滑鼠事件集()
		halt()
	}
}

func memorytest(y int) {
	記憶體管理器 := &T記憶體管理器{}
	allocated := uint32(uintptr(記憶體管理器.M配置記憶體(1024)))
	控制台.MUnsignedinteger32列印xy(allocated, 10, uint16(y))
	if y == 11 {
		記憶體管理器.F剩餘(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func P暫停迴圈()
func R重新載入cr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func S設定cr3(cr3 uint32)
func Getcr4() uint32
func E啟用分頁管理()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Get函式名稱(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var func名稱 = runtime.FuncForPC(address).Name()
	var func位元組 []byte = []byte(func名稱)

	工作控制台.M列印xy(func位元組, 1, 5)
	工作控制台.M列印(([]byte)(":"))
	工作控制台.MUnsignedinteger32列印(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	工作控制台.M列印unsignedinteger32(cr0, 2, 1)
}

var tss *Tss項目 = &Tss項目{}

func KKernelEntry(P頁目錄項目 uintptr, stacktop uintptr, stackbottom uintptr) {

	M串列記錄init()
	控制台.M列印("\n=== CHN BOOT ===\n")

	控制台.M列印unsignedinteger32(uint32(P頁目錄項目), 0, 2)
	控制台.M列印unsignedinteger32(uint32(P頁目錄項目), 10, 2)
	控制台.M列印unsignedinteger32(uint32(stacktop), 0, 3)
	控制台.M列印unsignedinteger32(uint32(stackbottom), 10, 3)

	記憶體管理器 := &T記憶體管理器{}
	記憶體管理器.Init(0, M最大佇列大小)

	分頁管理 := &P分頁管理{}
	分頁管理.Init(P頁目錄項目, 0x500000, 記憶體管理器)
	分頁管理.Shared記憶體region()

	S設定cr3(uint32(P頁目錄項目))
	E啟用分頁管理()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	控制台.M列印("esp:")

	esp := getesp()
	控制台.MUnsignedinteger32列印(uint32(esp))

	tls := gettls()
	控制台.M列印(([]byte)("tls:"))
	控制台.MUnsignedinteger32列印(tls)

	tss.I安裝(shareddescriptortable, 7, Seg核心資料, esp)

	Virt測試()

	cr3 := R重新載入cr3()
	控制台.M列印(([]byte)(":cr3:"))
	控制台.MUnsignedinteger32列印(cr3)

	cr0 := Getcr0()
	控制台.M列印(([]byte)(":cr0:"))
	控制台.MUnsignedinteger32列印(cr0)

	cr4 := Getcr4()
	控制台.M列印(([]byte)(":cr4:"))
	控制台.MUnsignedinteger32列印(cr4)

	工作管理器_2 := &T工作管理器{}
	工作管理器_2.Init()

	I中斷管理器 := &T中斷管理器{}
	I中斷管理器.Init(0x20, shareddescriptortable, 工作管理器_2)

	分頁管理.P頁故障(I中斷管理器)

	D驅動程式管理器 := T驅動程式管理器{}
	D驅動程式管理器.Init()

	執行緒helper := &T執行緒helper{}
	執行緒helper.Init(記憶體管理器)

	程序helper := P程序helper{}
	程序helper.Init(記憶體管理器, P頁目錄項目)

	sche := &S排程器{}
	sche.Init(I中斷管理器, 記憶體管理器, tss)

	sys呼叫 := &TSyscall{}
	sys呼叫.Init(I中斷管理器)

	程序helper.Spawn(工作a, 執行緒helper, sche, uint32(P頁目錄項目), true)
	程序helper.Spawn(工作b, 執行緒helper, sche, uint32(P頁目錄項目), true)
	程序helper.Spawn(工作c, 執行緒helper, sche, uint32(P頁目錄項目), true)
	程序helper.Spawn(工作d1, 執行緒helper, sche, uint32(P頁目錄項目), true)
	程序helper.Spawn(輸入事件工作, 執行緒helper, sche, uint32(P頁目錄項目), true)

	var 大小 uint32

	var linker檔案 []byte = ([]byte)("LINKER")
	大小 = Get檔案大小(linker檔案)
	linkeraddress := 記憶體管理器.M配置記憶體(大小)
	linker資料 := Get位元組from指標(uintptr(linkeraddress), int(大小), int(大小))
	M讀取檔案(linker檔案, linker資料)

	elf0 := Elf{}
	linker項目 := elf0.Get項目(linker資料)
	elf0.Parse(linker資料[:], uint32(P頁目錄項目))

	連結對映 := L連結對映{}
	連結對映.Init(記憶體管理器)

	var lib1檔案 []byte = ([]byte)("LIB1")
	大小 = Get檔案大小(lib1檔案)

	lib1address := 記憶體管理器.M配置記憶體(大小)
	lib1資料 := Get位元組from指標(uintptr(lib1address), int(大小), int(大小))
	M讀取檔案(lib1檔案, lib1資料)

	lib1elf := Elf{}
	lib1elf.Parse(lib1資料[:], uint32(P頁目錄項目))
	記憶體管理器.F剩餘(lib1address)

	連結對映.M附加至串列尾端(uintptr(lib1elf.D動態))

	var lib2檔案 []byte = ([]byte)("LIB2")
	大小 = Get檔案大小(lib2檔案)

	lib2address := 記憶體管理器.M配置記憶體(大小)
	lib2資料 := Get位元組from指標(uintptr(lib2address), int(大小), int(大小))
	M讀取檔案(lib2檔案, lib2資料)

	lib2elf := Elf{}
	lib2elf.Parse(lib2資料[:], uint32(P頁目錄項目))
	記憶體管理器.F剩餘(lib2address)

	連結對映.M附加至串列尾端(uintptr(lib2elf.D動態))

	lib連結對映 := 連結對映.Clone()
	連結對映address := uint32(uintptr(Pointer(lib連結對映.First)))

	lib1got := Getunsignedinteger32陣列from指標(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = 連結對映address
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32陣列from指標(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = 連結對映address
	lib2got[2] = 0x4000000

	控制台.M列印xy("lib1: ", 1, 8)
	控制台.MUnsignedinteger32列印(lib1elf.Got)
	控制台.M列印(":")
	控制台.MUnsignedinteger32列印(lib1elf.D動態)

	控制台.M列印xy("lib2: ", 1, 9)
	控制台.MUnsignedinteger32列印(lib2elf.Got)
	控制台.M列印(":")
	控制台.MUnsignedinteger32列印(lib2elf.D動態)

	var 使用者1檔案 []byte = ([]byte)("USER1")
	大小 = Get檔案大小(使用者1檔案)
	使用者1address := 記憶體管理器.M配置記憶體(大小)
	使用者1資料 := Get位元組from指標(uintptr(使用者1address), int(大小), int(大小))
	M讀取檔案(使用者1檔案, 使用者1資料)

	elf2 := Elf{}

	使用者1項目 := elf2.Get項目(使用者1資料)
	elf2.Parse(使用者1資料[:], uint32(P頁目錄項目+0x1000))
	全域位移table := elf2.Got

	P數值1連結對映 := 連結對映.Clone()
	P數值1連結對映.M附加至串列尾端(uintptr(elf2.D動態))

	記憶體管理器.F剩餘(使用者1address)

	var code1指標 *uintptr
	var func1val func()

	code1指標 = (*uintptr)(記憶體管理器.M配置記憶體(4))
	*code1指標 = uintptr(linker項目)
	func1val = *(*func())(Pointer(&code1指標))

	proc2 := 程序helper.Spawn(func1val, 執行緒helper, sche, uint32(P頁目錄項目+0x1000), false)
	thr2 := (*T執行緒)(proc2.Threads.Getat(0))
	thr2.Cpu狀態.Ecx = 使用者1項目
	thr2.Cpu狀態.Edx = 全域位移table
	thr2.Cpu狀態.Esi = uint32(uintptr(Pointer(P數值1連結對映.First)))

	控制台.M列印xy("user1: ", 1, 10)
	控制台.MUnsignedinteger32列印(elf2.Got)

	var 使用者2檔案 []byte = ([]byte)("USER2")
	大小 = Get檔案大小(使用者2檔案)
	使用者2address := 記憶體管理器.M配置記憶體(大小)
	使用者2資料 := Get位元組from指標(uintptr(使用者2address), int(大小), int(大小))
	M讀取檔案(使用者2檔案, 使用者2資料)

	elf3 := Elf{}

	使用者2項目 := elf3.Get項目(使用者2資料)
	elf3.Parse(使用者2資料[:], uint32(P頁目錄項目+0x2000))
	全域位移table = elf3.Got

	P數值2連結對映 := 連結對映.Clone()
	P數值2連結對映.M附加至串列尾端(uintptr(elf3.D動態))

	記憶體管理器.F剩餘(使用者2address)

	var code2指標 *uintptr
	var func2val func()

	code2指標 = (*uintptr)(記憶體管理器.M配置記憶體(4))
	*code2指標 = uintptr(linker項目)
	func2val = *(*func())(Pointer(&code2指標))

	proc3 := 程序helper.Spawn(func2val, 執行緒helper, sche, uint32(P頁目錄項目+0x2000), false)
	thr3 := (*T執行緒)(proc3.Threads.Getat(0))
	thr3.Cpu狀態.Ecx = 使用者2項目
	thr3.Cpu狀態.Edx = 全域位移table
	thr3.Cpu狀態.Esi = uint32(uintptr(Pointer(P數值2連結對映.First)))

	控制台.M列印xy("user2: ", 1, 11)
	控制台.MUnsignedinteger32列印(thr3.Cpu狀態.Esi)

	lib連結對映.P列印(1, 11)

	var 使用者3檔案 []byte = ([]byte)("USER3")
	大小 = Get檔案大小(使用者3檔案)
	使用者3address := 記憶體管理器.M配置記憶體(大小)
	使用者3資料 := Get位元組from指標(uintptr(使用者3address), int(大小), int(大小))
	M讀取檔案(使用者3檔案, 使用者3資料)

	elf4 := Elf{}

	使用者3項目 := elf4.Get項目(使用者3資料)
	elf4.Parse(使用者3資料[:], uint32(P頁目錄項目+0x3000))
	全域位移table = elf4.Got

	P數值3連結對映 := 連結對映.Clone()
	P數值3連結對映.M附加至串列尾端(uintptr(elf4.D動態))

	記憶體管理器.F剩餘(使用者3address)

	var code3指標 *uintptr
	var func3val func()

	code3指標 = (*uintptr)(記憶體管理器.M配置記憶體(4))
	*code3指標 = uintptr(linker項目)
	func3val = *(*func())(Pointer(&code3指標))

	proc4 := 程序helper.Spawn(func3val, 執行緒helper, sche, uint32(P頁目錄項目+0x3000), false)
	thr4 := (*T執行緒)(proc4.Threads.Getat(0))
	thr4.Cpu狀態.Ecx = 使用者3項目
	thr4.Cpu狀態.Edx = 全域位移table
	thr4.Cpu狀態.Esi = uint32(uintptr(Pointer(P數值3連結對映.First)))

	程序helper.Spawn(T函式1, 執行緒helper, sche, uint32(P頁目錄項目+0x4000), true)

	i鍵盤事件handler = &my鍵盤事件handler
	鍵盤驅動程式.Init驅動程式(I中斷管理器, i鍵盤事件handler)

	滑鼠驅動程式.Init驅動程式(I中斷管理器, nil)

	mypci控制器handler := TMypci控制器handler{}
	pci控制器.Init(mypci控制器handler)
	pci控制器.S選取驅動程式(&D驅動程式管理器, I中斷管理器)
	裝置descriptor = mypci控制器handler.Get驅動程式()

	sche.E已啟用(true)
	I中斷管理器.A啟用()

	for {
		halt()
	}

}
