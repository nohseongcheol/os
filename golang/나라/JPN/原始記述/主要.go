package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "汎用"
import . "gdt"
import . "コンソール"
import . "割込み"
import . "複数タスク管理"
import . "タスク管理/tss"

import . "仮想メモリ"
import . "ページ管理"
import . "タスク管理/スレッド"
import . "タスク管理/スケジューラ"
import . "タスク管理/プロセス"
import . "ドライバー/ドライバー"

import . "ドライバー/キーボード"
import . "ドライバー/位置入力装置"

import . "ドライバー/ata"
import . "ファイルシステム/msdos区分"
import . "ファイルシステム/fat"

import . "ファイルシステム/実行連結形式"

import . "システム呼出し"

import . "メモリ管理者"
import . "pci"

func halt()

var iキーボード事象handler Iキーボード事象handler

type TMyキーボード事象handler struct {
}

var myキーボード事象handler TMyキーボード事象handler
var キーボードドライバー Tキーボードドライバー
var マウスドライバー Tマウスドライバー
var pci制御器 TPeripheralcomponentinterconnect制御器

var キーボードコンソール Tコンソール = Tコンソール{}

func (self *TMyキーボード事象handler) O時鍵下(鍵 byte) {
	foo := [1]byte{' '}
	foo[0] = 鍵

	キーボードコンソール.M印刷バイトxy(foo[:], 1000, 1000)
}

func (self *TMyキーボード事象handler) O時鍵上へ(鍵 byte)	{}

var iマウス事象handler Iマウス事象handler

type TMyマウス事象handler struct {
}

var マウスコンソール Tコンソール = Tコンソール{}
var previousx int16 = 0
var previousy int16 = 0
var x配置 int16 = 0
var y配置 int16 = 0

func (self *TMyマウス事象handler) O時マウス下(ボタン int8) {
	buffer := []byte("x")
	マウスコンソール.M印刷xy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyマウス事象handler) O時マウス上へ(ボタン int8)	{}
func (self *TMyマウス事象handler) O時マウス移動(x int8, y int8) {

	x配置 += int16(x)
	if x配置 < 0 {
		x配置 = 0
	}
	if x配置 >= 80 {
		x配置 = 79
	}

	y配置 -= int16(y)

	if y配置 < 0 {
		y配置 = 0
	}
	if y配置 >= 25 {
		y配置 = 24
	}

	buffer := []byte(" ")
	マウスコンソール.M印刷xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	マウスコンソール.M印刷xy(buffer, uint16(x配置), uint16(y配置))

	previousx = x配置
	previousy = y配置
}

var デバイスdescriptor TPeripheralcomponentinterconnectデバイスdescriptor
var ipci制御器handler Ipci制御器handler

type TMypci制御器handler struct {
}

var コンソール Tコンソール = Tコンソール{}
var ドライバーカウント uint16 = 0

func (self TMypci制御器handler) O時getドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor) {
	if デバイス.V製造元id == 0x1022 && デバイス.Dデバイスid == 0x2000 {
		コンソール.M印刷xy([]byte("["), 0, 12)
		コンソール.M印刷(([]byte)("AMD am79c973"))
		コンソール.M印刷([]byte(":"))
		コンソール.MUnsignedinteger16印刷(デバイス.V製造元id)
		コンソール.M印刷([]byte(":"))
		コンソール.MUnsignedinteger16印刷(デバイス.Dデバイスid)
		コンソール.M印刷([]byte(":"))
		コンソール.MUnsignedinteger16印刷(uint16(デバイス.Pポートbase))
		コンソール.M印刷([]byte(":"))
		コンソール.MUnsignedinteger32印刷(デバイス.I割込み)

		コンソール.M印刷([]byte("]\n"))
		デバイスdescriptor = デバイス
		ドライバーカウント++
	}
}
func (self TMypci制御器handler) Getドライバー() TPeripheralcomponentinterconnectデバイスdescriptor {
	return デバイスdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func P印刷str(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	コンソール.M印刷(str)
}

func Getファイルサイズ(ファイル名 []byte) uint32 {
	var ata0s = T詳細使用技術attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	区分 := Tmsdos区分table{}
	区分.R読込み区分(&ata0s)

	bios := Tファイル体系設定値32{}

	var サイズ uint32 = bios.Len(&ata0s, 区分.Mbr.Primary区分[0], ファイル名)
	ata0s.Flush()

	return サイズ
}

func Mファイルを読む(ファイル名 []byte, データ []byte) {
	var ata0s = T詳細使用技術attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	区分 := Tmsdos区分table{}
	区分.R読込み区分(&ata0s)

	bios := Tファイル体系設定値32{}
	bios.R読込み(&ata0s, 区分.Mbr.Primary区分[0], ファイル名, データ)

	ata0s.Flush()
}
func L読込みelf() {

	var ata0s = T詳細使用技術attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	区分 := Tmsdos区分table{}
	区分.R読込み区分(&ata0s)

	bios := Tファイル体系設定値32{}

	var ファイル名 []byte = ([]byte)("TEST")
	var サイズ uint32 = bios.Len(&ata0s, 区分.Mbr.Primary区分[0], ファイル名)
	var データbuffer [100 * 1024]byte
	var データ []byte = データbuffer[:]
	bios.R読込み(&ata0s, 区分.Mbr.Primary区分[0], ファイル名, データ)

	実行連結形式 := Elf{}

	実行連結形式.Parse(データ[:サイズ], 0x4f00000)

}

var タスクコンソール Tコンソール = Tコンソール{}

func T関数1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func タスクa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func タスクb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func タスクc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func タスクd()

func タスクd0() {
	esi := getesi()
	for {

		Sys印刷unsignedinteger32(esi)

	}
}

func タスクd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func 入力事象タスク() {
	for {
		Pプロセス保留キーボード事象一覧()
		Pプロセス保留マウス事象一覧()
		halt()
	}
}

func memorytest(y int) {
	メモリ管理者 := &Tメモリ管理者{}
	allocated := uint32(uintptr(メモリ管理者.M記憶領域を確保(1024)))
	コンソール.MUnsignedinteger32印刷xy(allocated, 10, uint16(y))
	if y == 11 {
		メモリ管理者.F空き(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func P一時停止loop()
func R再読み込みcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sありcr3(cr3 uint32)
func Getcr4() uint32
func Enableページ管理()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Get関数名前(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var func名前 = runtime.FuncForPC(address).Name()
	var funcバイト []byte = []byte(func名前)

	タスクコンソール.M印刷xy(funcバイト, 1, 5)
	タスクコンソール.M印刷(([]byte)(":"))
	タスクコンソール.MUnsignedinteger32印刷(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	タスクコンソール.M印刷unsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pページディレクトリentry uintptr, stacktop uintptr, stackbottom uintptr) {

	M直列ログinit()
	コンソール.M印刷("\n=== JPN BOOT ===\n")

	コンソール.M印刷unsignedinteger32(uint32(Pページディレクトリentry), 0, 2)
	コンソール.M印刷unsignedinteger32(uint32(Pページディレクトリentry), 10, 2)
	コンソール.M印刷unsignedinteger32(uint32(stacktop), 0, 3)
	コンソール.M印刷unsignedinteger32(uint32(stackbottom), 10, 3)

	メモリ管理者 := &Tメモリ管理者{}
	メモリ管理者.Init(0, M最大待ち行列サイズ)

	ページ管理 := &Pページ管理{}
	ページ管理.Init(Pページディレクトリentry, 0x500000, メモリ管理者)
	ページ管理.Sharedメモリregion()

	Sありcr3(uint32(Pページディレクトリentry))
	Enableページ管理()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	コンソール.M印刷("esp:")

	esp := getesp()
	コンソール.MUnsignedinteger32印刷(uint32(esp))

	tls := gettls()
	コンソール.M印刷(([]byte)("tls:"))
	コンソール.MUnsignedinteger32印刷(tls)

	tss.Iインストール(shareddescriptortable, 7, Seg中核データ, esp)

	Virtテスト()

	cr3 := R再読み込みcr3()
	コンソール.M印刷(([]byte)(":cr3:"))
	コンソール.MUnsignedinteger32印刷(cr3)

	cr0 := Getcr0()
	コンソール.M印刷(([]byte)(":cr0:"))
	コンソール.MUnsignedinteger32印刷(cr0)

	cr4 := Getcr4()
	コンソール.M印刷(([]byte)(":cr4:"))
	コンソール.MUnsignedinteger32印刷(cr4)

	タスク管理者_2 := &Tタスク管理者{}
	タスク管理者_2.Init()

	I割込み管理者 := &T割込み管理者{}
	I割込み管理者.Init(0x20, shareddescriptortable, タスク管理者_2)

	ページ管理.Pページ障害(I割込み管理者)

	Dドライバー管理者 := Tドライバー管理者{}
	Dドライバー管理者.Init()

	スレッドhelper := &Tスレッドhelper{}
	スレッドhelper.Init(メモリ管理者)

	プロセスhelper := Pプロセスhelper{}
	プロセスhelper.Init(メモリ管理者, Pページディレクトリentry)

	sche := &Sスケジューラ{}
	sche.Init(I割込み管理者, メモリ管理者, tss)

	sys呼出し := &TSyscall{}
	sys呼出し.Init(I割込み管理者)

	プロセスhelper.Spawn(タスクa, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクb, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクc, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクd1, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(入力事象タスク, スレッドhelper, sche, uint32(Pページディレクトリentry), true)

	var サイズ uint32

	var linkerファイル []byte = ([]byte)("LINKER")
	サイズ = Getファイルサイズ(linkerファイル)
	linkeraddress := メモリ管理者.M記憶領域を確保(サイズ)
	linkerデータ := Getバイトからポインタ(uintptr(linkeraddress), int(サイズ), int(サイズ))
	Mファイルを読む(linkerファイル, linkerデータ)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerデータ)
	elf0.Parse(linkerデータ[:], uint32(Pページディレクトリentry))

	連結対応表 := L連結対応表{}
	連結対応表.Init(メモリ管理者)

	var lib1ファイル []byte = ([]byte)("LIB1")
	サイズ = Getファイルサイズ(lib1ファイル)

	lib1address := メモリ管理者.M記憶領域を確保(サイズ)
	lib1データ := Getバイトからポインタ(uintptr(lib1address), int(サイズ), int(サイズ))
	Mファイルを読む(lib1ファイル, lib1データ)

	lib1elf := Elf{}
	lib1elf.Parse(lib1データ[:], uint32(Pページディレクトリentry))
	メモリ管理者.F空き(lib1address)

	連結対応表.M末尾に追加(uintptr(lib1elf.D動的に))

	var lib2ファイル []byte = ([]byte)("LIB2")
	サイズ = Getファイルサイズ(lib2ファイル)

	lib2address := メモリ管理者.M記憶領域を確保(サイズ)
	lib2データ := Getバイトからポインタ(uintptr(lib2address), int(サイズ), int(サイズ))
	Mファイルを読む(lib2ファイル, lib2データ)

	lib2elf := Elf{}
	lib2elf.Parse(lib2データ[:], uint32(Pページディレクトリentry))
	メモリ管理者.F空き(lib2address)

	連結対応表.M末尾に追加(uintptr(lib2elf.D動的に))

	lib連結対応表 := 連結対応表.Clone()
	連結対応表address := uint32(uintptr(Pointer(lib連結対応表.First)))

	lib1got := Getunsignedinteger32配列からポインタ(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = 連結対応表address
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32配列からポインタ(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = 連結対応表address
	lib2got[2] = 0x4000000

	コンソール.M印刷xy("lib1: ", 1, 8)
	コンソール.MUnsignedinteger32印刷(lib1elf.Got)
	コンソール.M印刷(":")
	コンソール.MUnsignedinteger32印刷(lib1elf.D動的に)

	コンソール.M印刷xy("lib2: ", 1, 9)
	コンソール.MUnsignedinteger32印刷(lib2elf.Got)
	コンソール.M印刷(":")
	コンソール.MUnsignedinteger32印刷(lib2elf.D動的に)

	var 利用者1ファイル []byte = ([]byte)("USER1")
	サイズ = Getファイルサイズ(利用者1ファイル)
	利用者1address := メモリ管理者.M記憶領域を確保(サイズ)
	利用者1データ := Getバイトからポインタ(uintptr(利用者1address), int(サイズ), int(サイズ))
	Mファイルを読む(利用者1ファイル, 利用者1データ)

	elf2 := Elf{}

	利用者1entry := elf2.Getentry(利用者1データ)
	elf2.Parse(利用者1データ[:], uint32(Pページディレクトリentry+0x1000))
	全般offsettable := elf2.Got

	P値1連結対応表 := 連結対応表.Clone()
	P値1連結対応表.M末尾に追加(uintptr(elf2.D動的に))

	メモリ管理者.F空き(利用者1address)

	var code1ポインタ *uintptr
	var func1val func()

	code1ポインタ = (*uintptr)(メモリ管理者.M記憶領域を確保(4))
	*code1ポインタ = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1ポインタ))

	proc2 := プロセスhelper.Spawn(func1val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x1000), false)
	thr2 := (*Tスレッド)(proc2.Threads.Getat(0))
	thr2.Cpu状態.Ecx = 利用者1entry
	thr2.Cpu状態.Edx = 全般offsettable
	thr2.Cpu状態.Esi = uint32(uintptr(Pointer(P値1連結対応表.First)))

	コンソール.M印刷xy("user1: ", 1, 10)
	コンソール.MUnsignedinteger32印刷(elf2.Got)

	var 利用者2ファイル []byte = ([]byte)("USER2")
	サイズ = Getファイルサイズ(利用者2ファイル)
	利用者2address := メモリ管理者.M記憶領域を確保(サイズ)
	利用者2データ := Getバイトからポインタ(uintptr(利用者2address), int(サイズ), int(サイズ))
	Mファイルを読む(利用者2ファイル, 利用者2データ)

	elf3 := Elf{}

	利用者2entry := elf3.Getentry(利用者2データ)
	elf3.Parse(利用者2データ[:], uint32(Pページディレクトリentry+0x2000))
	全般offsettable = elf3.Got

	P値2連結対応表 := 連結対応表.Clone()
	P値2連結対応表.M末尾に追加(uintptr(elf3.D動的に))

	メモリ管理者.F空き(利用者2address)

	var code2ポインタ *uintptr
	var func2val func()

	code2ポインタ = (*uintptr)(メモリ管理者.M記憶領域を確保(4))
	*code2ポインタ = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2ポインタ))

	proc3 := プロセスhelper.Spawn(func2val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x2000), false)
	thr3 := (*Tスレッド)(proc3.Threads.Getat(0))
	thr3.Cpu状態.Ecx = 利用者2entry
	thr3.Cpu状態.Edx = 全般offsettable
	thr3.Cpu状態.Esi = uint32(uintptr(Pointer(P値2連結対応表.First)))

	コンソール.M印刷xy("user2: ", 1, 11)
	コンソール.MUnsignedinteger32印刷(thr3.Cpu状態.Esi)

	lib連結対応表.P印刷(1, 11)

	var 利用者3ファイル []byte = ([]byte)("USER3")
	サイズ = Getファイルサイズ(利用者3ファイル)
	利用者3address := メモリ管理者.M記憶領域を確保(サイズ)
	利用者3データ := Getバイトからポインタ(uintptr(利用者3address), int(サイズ), int(サイズ))
	Mファイルを読む(利用者3ファイル, 利用者3データ)

	elf4 := Elf{}

	利用者3entry := elf4.Getentry(利用者3データ)
	elf4.Parse(利用者3データ[:], uint32(Pページディレクトリentry+0x3000))
	全般offsettable = elf4.Got

	P値3連結対応表 := 連結対応表.Clone()
	P値3連結対応表.M末尾に追加(uintptr(elf4.D動的に))

	メモリ管理者.F空き(利用者3address)

	var code3ポインタ *uintptr
	var func3val func()

	code3ポインタ = (*uintptr)(メモリ管理者.M記憶領域を確保(4))
	*code3ポインタ = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3ポインタ))

	proc4 := プロセスhelper.Spawn(func3val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x3000), false)
	thr4 := (*Tスレッド)(proc4.Threads.Getat(0))
	thr4.Cpu状態.Ecx = 利用者3entry
	thr4.Cpu状態.Edx = 全般offsettable
	thr4.Cpu状態.Esi = uint32(uintptr(Pointer(P値3連結対応表.First)))

	プロセスhelper.Spawn(T関数1, スレッドhelper, sche, uint32(Pページディレクトリentry+0x4000), true)

	iキーボード事象handler = &myキーボード事象handler
	キーボードドライバー.Initドライバー(I割込み管理者, iキーボード事象handler)

	マウスドライバー.Initドライバー(I割込み管理者, nil)

	mypci制御器handler := TMypci制御器handler{}
	pci制御器.Init(mypci制御器handler)
	pci制御器.S選択ドライバー(&Dドライバー管理者, I割込み管理者)
	デバイスdescriptor = mypci制御器handler.Getドライバー()

	sche.E有効(true)
	I割込み管理者.A有効()

	for {
		halt()
	}

}
