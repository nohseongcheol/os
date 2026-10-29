/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "工具"
import . "gdt"
import . "控制台"
import . "中断"
import . "多重任务管理"
import . "任务管理/tss"

import . "虚拟内存"
import . "分页管理"
import . "任务管理/线程"
import . "任务管理/调度器"
import . "任务管理/进程"
import . "驱动程序/驱动程序"

import . "驱动程序/键盘"
import . "驱动程序/指向设备"

import . "驱动程序/ata"
import . "文件系统/msdos分区"
import . "文件系统/fat"

import . "文件系统/可执行与可链接格式"

import . "系统调用"

import . "内存管理器"
import . "pci"

func halt()

var i键盘事件handler I键盘事件handler

type TMy键盘事件handler struct {
}

var my键盘事件handler TMy键盘事件handler
var 键盘驱动程序 T键盘驱动程序
var 鼠标驱动程序 T鼠标驱动程序
var pci控制器 TPeripheralcomponentinterconnect控制器

var 键盘控制台 T控制台 = T控制台{}

func (self *TMy键盘事件handler) O时关键下(关键 byte) {
	foo := [1]byte{' '}
	foo[0] = 关键

	键盘控制台.M打印字节xy(foo[:], 1000, 1000)
}

func (self *TMy键盘事件handler) O时关键向上(关键 byte)	{}

var i鼠标事件handler I鼠标事件handler

type TMy鼠标事件handler struct {
}

var 鼠标控制台 T控制台 = T控制台{}
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self *TMy鼠标事件handler) O时鼠标下(按钮 int8) {
	buffer := []byte("x")
	鼠标控制台.M打印xy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMy鼠标事件handler) O时鼠标向上(按钮 int8)	{}
func (self *TMy鼠标事件handler) O时鼠标移动(x int8, y int8) {

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
	鼠标控制台.M打印xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	鼠标控制台.M打印xy(buffer, uint16(x位置), uint16(y位置))

	previousx = x位置
	previousy = y位置
}

var 设备descriptor TPeripheralcomponentinterconnect设备descriptor
var ipci控制器handler Ipci控制器handler

type TMypci控制器handler struct {
}

var 控制台 T控制台 = T控制台{}
var 驱动程序计数 uint16 = 0

func (self TMypci控制器handler) O时get驱动程序(设备 TPeripheralcomponentinterconnect设备descriptor) {
	if 设备.V发行商id == 0x1022 && 设备.D设备id == 0x2000 {
		控制台.M打印xy([]byte("["), 0, 12)
		控制台.M打印(([]byte)("AMD am79c973"))
		控制台.M打印([]byte(":"))
		控制台.MUnsignedinteger16打印(设备.V发行商id)
		控制台.M打印([]byte(":"))
		控制台.MUnsignedinteger16打印(设备.D设备id)
		控制台.M打印([]byte(":"))
		控制台.MUnsignedinteger16打印(uint16(设备.P端口base))
		控制台.M打印([]byte(":"))
		控制台.MUnsignedinteger32打印(设备.I中断)

		控制台.M打印([]byte("]\n"))
		设备descriptor = 设备
		驱动程序计数++
	}
}
func (self TMypci控制器handler) Get驱动程序() TPeripheralcomponentinterconnect设备descriptor {
	return 设备descriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func P打印str(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	控制台.M打印(str)
}

func Get文件大小(文件名 []byte) uint32 {
	var ata0s = T高级技术attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分区 := Tmsdos分区表格{}
	分区.R读取分区(&ata0s)

	bios := T文件系统参数32{}

	var 大小 uint32 = bios.Len(&ata0s, 分区.Mbr.Primary分区[0], 文件名)
	ata0s.Flush()

	return 大小
}

func M读取文件(文件名 []byte, 数据 []byte) {
	var ata0s = T高级技术attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分区 := Tmsdos分区表格{}
	分区.R读取分区(&ata0s)

	bios := T文件系统参数32{}
	bios.R读取(&ata0s, 分区.Mbr.Primary分区[0], 文件名, 数据)

	ata0s.Flush()
}
func L加载elf() {

	var ata0s = T高级技术attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分区 := Tmsdos分区表格{}
	分区.R读取分区(&ata0s)

	bios := T文件系统参数32{}

	var 文件名 []byte = ([]byte)("TEST")
	var 大小 uint32 = bios.Len(&ata0s, 分区.Mbr.Primary分区[0], 文件名)
	var 数据buffer [100 * 1024]byte
	var 数据 []byte = 数据buffer[:]
	bios.R读取(&ata0s, 分区.Mbr.Primary分区[0], 文件名, 数据)

	可执行与可链接格式 := Elf{}

	可执行与可链接格式.Parse(数据[:大小], 0x4f00000)

}

var 任务控制台 T控制台 = T控制台{}

func T函数1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func 任务a() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func 任务b() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func 任务c() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func 任务d()

func 任务d0() {
	esi := getesi()
	for {

		Sys打印unsignedinteger32(esi)

	}
}

func 任务d1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func 输入事件任务() {
	for {
		P进程待处理键盘事件集()
		P进程待处理鼠标事件集()
		halt()
	}
}

func memorytest(y int) {
	内存管理器 := &T内存管理器{}
	allocated := uint32(uintptr(内存管理器.M分配内存(1024)))
	控制台.MUnsignedinteger32打印xy(allocated, 10, uint16(y))
	if y == 11 {
		内存管理器.F空闲(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func P暂停loop()
func R重新载入cr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func S集合cr3(cr3 uint32)
func Getcr4() uint32
func E启用分页管理()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Get函数名称(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var func名称 = runtime.FuncForPC(address).Name()
	var func字节 []byte = []byte(func名称)

	任务控制台.M打印xy(func字节, 1, 5)
	任务控制台.M打印(([]byte)(":"))
	任务控制台.MUnsignedinteger32打印(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	任务控制台.M打印unsignedinteger32(cr0, 2, 1)
}

var tss *Tss条目 = &Tss条目{}

func KKernelEntry(P页目录条目 uintptr, stacktop uintptr, stackbottom uintptr) {

	M串行日志init()
	控制台.M打印("\n=== HKG BOOT ===\n")

	控制台.M打印unsignedinteger32(uint32(P页目录条目), 0, 2)
	控制台.M打印unsignedinteger32(uint32(P页目录条目), 10, 2)
	控制台.M打印unsignedinteger32(uint32(stacktop), 0, 3)
	控制台.M打印unsignedinteger32(uint32(stackbottom), 10, 3)

	内存管理器 := &T内存管理器{}
	内存管理器.Init(0, M最大值队列大小)

	分页管理 := &P分页管理{}
	分页管理.Init(P页目录条目, 0x500000, 内存管理器)
	分页管理.Shared内存region()

	S集合cr3(uint32(P页目录条目))
	E启用分页管理()

	shareddescriptor表格 := &TShareddescriptor表格{}
	shareddescriptor表格.Init()

	控制台.M打印("esp:")

	esp := getesp()
	控制台.MUnsignedinteger32打印(uint32(esp))

	tls := gettls()
	控制台.M打印(([]byte)("tls:"))
	控制台.MUnsignedinteger32打印(tls)

	tss.I安装(shareddescriptor表格, 7, Seg内核数据, esp)

	Virt测试()

	cr3 := R重新载入cr3()
	控制台.M打印(([]byte)(":cr3:"))
	控制台.MUnsignedinteger32打印(cr3)

	cr0 := Getcr0()
	控制台.M打印(([]byte)(":cr0:"))
	控制台.MUnsignedinteger32打印(cr0)

	cr4 := Getcr4()
	控制台.M打印(([]byte)(":cr4:"))
	控制台.MUnsignedinteger32打印(cr4)

	任务管理器_2 := &T任务管理器{}
	任务管理器_2.Init()

	I中断管理器 := &T中断管理器{}
	I中断管理器.Init(0x20, shareddescriptor表格, 任务管理器_2)

	分页管理.P页故障(I中断管理器)

	D驱动程序管理器 := T驱动程序管理器{}
	D驱动程序管理器.Init()

	线程helper := &T线程helper{}
	线程helper.Init(内存管理器)

	进程helper := P进程helper{}
	进程helper.Init(内存管理器, P页目录条目)

	sche := &S调度器{}
	sche.Init(I中断管理器, 内存管理器, tss)

	sys调用 := &TSyscall{}
	sys调用.Init(I中断管理器)

	进程helper.Spawn(任务a, 线程helper, sche, uint32(P页目录条目), true)
	进程helper.Spawn(任务b, 线程helper, sche, uint32(P页目录条目), true)
	进程helper.Spawn(任务c, 线程helper, sche, uint32(P页目录条目), true)
	进程helper.Spawn(任务d1, 线程helper, sche, uint32(P页目录条目), true)
	进程helper.Spawn(输入事件任务, 线程helper, sche, uint32(P页目录条目), true)

	var 大小 uint32

	var linker文件 []byte = ([]byte)("LINKER")
	大小 = Get文件大小(linker文件)
	linkeraddress := 内存管理器.M分配内存(大小)
	linker数据 := Get字节from指针(uintptr(linkeraddress), int(大小), int(大小))
	M读取文件(linker文件, linker数据)

	elf0 := Elf{}
	linker条目 := elf0.Get条目(linker数据)
	elf0.Parse(linker数据[:], uint32(P页目录条目))

	链接映射 := L链接映射{}
	链接映射.Init(内存管理器)

	var 里布1文件 []byte = ([]byte)("LIB1")
	大小 = Get文件大小(里布1文件)

	里布1address := 内存管理器.M分配内存(大小)
	里布1数据 := Get字节from指针(uintptr(里布1address), int(大小), int(大小))
	M读取文件(里布1文件, 里布1数据)

	里布1elf := Elf{}
	里布1elf.Parse(里布1数据[:], uint32(P页目录条目))
	内存管理器.F空闲(里布1address)

	链接映射.M追加到表尾(uintptr(里布1elf.D动态))

	var 里布2文件 []byte = ([]byte)("LIB2")
	大小 = Get文件大小(里布2文件)

	里布2address := 内存管理器.M分配内存(大小)
	里布2数据 := Get字节from指针(uintptr(里布2address), int(大小), int(大小))
	M读取文件(里布2文件, 里布2数据)

	里布2elf := Elf{}
	里布2elf.Parse(里布2数据[:], uint32(P页目录条目))
	内存管理器.F空闲(里布2address)

	链接映射.M追加到表尾(uintptr(里布2elf.D动态))

	里布链接映射 := 链接映射.Clone()
	链接映射address := uint32(uintptr(Pointer(里布链接映射.First)))

	里布1got := Getunsignedinteger32数组from指针(uintptr(里布1elf.Got), 4, 4)
	里布1got[1] = 链接映射address
	里布1got[2] = 0x4000000

	里布2got := Getunsignedinteger32数组from指针(uintptr(里布2elf.Got), 4, 4)
	里布2got[1] = 链接映射address
	里布2got[2] = 0x4000000

	控制台.M打印xy("lib1: ", 1, 8)
	控制台.MUnsignedinteger32打印(里布1elf.Got)
	控制台.M打印(":")
	控制台.MUnsignedinteger32打印(里布1elf.D动态)

	控制台.M打印xy("lib2: ", 1, 9)
	控制台.MUnsignedinteger32打印(里布2elf.Got)
	控制台.M打印(":")
	控制台.MUnsignedinteger32打印(里布2elf.D动态)

	var 用户1文件 []byte = ([]byte)("USER1")
	大小 = Get文件大小(用户1文件)
	用户1address := 内存管理器.M分配内存(大小)
	用户1数据 := Get字节from指针(uintptr(用户1address), int(大小), int(大小))
	M读取文件(用户1文件, 用户1数据)

	elf2 := Elf{}

	用户1条目 := elf2.Get条目(用户1数据)
	elf2.Parse(用户1数据[:], uint32(P页目录条目+0x1000))
	全局位移表格 := elf2.Got

	P值1链接映射 := 链接映射.Clone()
	P值1链接映射.M追加到表尾(uintptr(elf2.D动态))

	内存管理器.F空闲(用户1address)

	var code1指针 *uintptr
	var func1val func()

	code1指针 = (*uintptr)(内存管理器.M分配内存(4))
	*code1指针 = uintptr(linker条目)
	func1val = *(*func())(Pointer(&code1指针))

	proc2 := 进程helper.Spawn(func1val, 线程helper, sche, uint32(P页目录条目+0x1000), false)
	thr2 := (*T线程)(proc2.Threads.Getat(0))
	thr2.Cpu状态.Ecx = 用户1条目
	thr2.Cpu状态.Edx = 全局位移表格
	thr2.Cpu状态.Esi = uint32(uintptr(Pointer(P值1链接映射.First)))

	控制台.M打印xy("user1: ", 1, 10)
	控制台.MUnsignedinteger32打印(elf2.Got)

	var 用户2文件 []byte = ([]byte)("USER2")
	大小 = Get文件大小(用户2文件)
	用户2address := 内存管理器.M分配内存(大小)
	用户2数据 := Get字节from指针(uintptr(用户2address), int(大小), int(大小))
	M读取文件(用户2文件, 用户2数据)

	elf3 := Elf{}

	用户2条目 := elf3.Get条目(用户2数据)
	elf3.Parse(用户2数据[:], uint32(P页目录条目+0x2000))
	全局位移表格 = elf3.Got

	P值2链接映射 := 链接映射.Clone()
	P值2链接映射.M追加到表尾(uintptr(elf3.D动态))

	内存管理器.F空闲(用户2address)

	var code2指针 *uintptr
	var func2val func()

	code2指针 = (*uintptr)(内存管理器.M分配内存(4))
	*code2指针 = uintptr(linker条目)
	func2val = *(*func())(Pointer(&code2指针))

	proc3 := 进程helper.Spawn(func2val, 线程helper, sche, uint32(P页目录条目+0x2000), false)
	thr3 := (*T线程)(proc3.Threads.Getat(0))
	thr3.Cpu状态.Ecx = 用户2条目
	thr3.Cpu状态.Edx = 全局位移表格
	thr3.Cpu状态.Esi = uint32(uintptr(Pointer(P值2链接映射.First)))

	控制台.M打印xy("user2: ", 1, 11)
	控制台.MUnsignedinteger32打印(thr3.Cpu状态.Esi)

	里布链接映射.P打印(1, 11)

	var 用户3文件 []byte = ([]byte)("USER3")
	大小 = Get文件大小(用户3文件)
	用户3address := 内存管理器.M分配内存(大小)
	用户3数据 := Get字节from指针(uintptr(用户3address), int(大小), int(大小))
	M读取文件(用户3文件, 用户3数据)

	elf4 := Elf{}

	用户3条目 := elf4.Get条目(用户3数据)
	elf4.Parse(用户3数据[:], uint32(P页目录条目+0x3000))
	全局位移表格 = elf4.Got

	P值3链接映射 := 链接映射.Clone()
	P值3链接映射.M追加到表尾(uintptr(elf4.D动态))

	内存管理器.F空闲(用户3address)

	var code3指针 *uintptr
	var func3val func()

	code3指针 = (*uintptr)(内存管理器.M分配内存(4))
	*code3指针 = uintptr(linker条目)
	func3val = *(*func())(Pointer(&code3指针))

	proc4 := 进程helper.Spawn(func3val, 线程helper, sche, uint32(P页目录条目+0x3000), false)
	thr4 := (*T线程)(proc4.Threads.Getat(0))
	thr4.Cpu状态.Ecx = 用户3条目
	thr4.Cpu状态.Edx = 全局位移表格
	thr4.Cpu状态.Esi = uint32(uintptr(Pointer(P值3链接映射.First)))

	进程helper.Spawn(T函数1, 线程helper, sche, uint32(P页目录条目+0x4000), true)

	i键盘事件handler = &my键盘事件handler
	键盘驱动程序.Init驱动程序(I中断管理器, i键盘事件handler)

	鼠标驱动程序.Init驱动程序(I中断管理器, nil)

	mypci控制器handler := TMypci控制器handler{}
	pci控制器.Init(mypci控制器handler)
	pci控制器.S选择驱动程序(&D驱动程序管理器, I中断管理器)
	设备descriptor = mypci控制器handler.Get驱动程序()

	sche.E启用(true)
	I中断管理器.A活跃()

	for {
		halt()
	}

}
