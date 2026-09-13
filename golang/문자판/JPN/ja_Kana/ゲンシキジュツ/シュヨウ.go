package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "ハンヨウ"
import . "gdt"
import . "コンソール"
import . "ワリコミ"
import . "フクスウタスクカンリ"
import . "タスクカンリ/tss"

import . "カソウメモリ"
import . "ページカンリ"
import . "タスクカンリ/スレッド"
import . "タスクカンリ/スケジューラ"
import . "タスクカンリ/プロセス"
import . "ドライバー/ドライバー"

import . "ドライバー/キーボード"
import . "ドライバー/イチニュウリョクソウチ"

import . "ドライバー/ata"
import . "ファイルシステム/msdosクブン"
import . "ファイルシステム/fat"

import . "ファイルシステム/ジッコウレンケツケイシキ"

import . "システムヨビダシ"

import . "メモリカンリシャ"
import . "pci"

func halt()

var iキーボードジショウhandler Iキーボードジショウhandler

type TMyキーボードジショウhandler struct {
}

var myキーボードジショウhandler TMyキーボードジショウhandler
var キーボードドライバー Tキーボードドライバー
var マウスドライバー Tマウスドライバー
var pciセイギョキ TPeripheralcomponentinterconnectセイギョキ

var キーボードコンソール Tコンソール = Tコンソール{}

func (self *TMyキーボードジショウhandler) Oトキカギシタ(カギ byte) {
	foo := [1]byte{' '}
	foo[0] = カギ

	キーボードコンソール.Mインサツバイトxy(foo[:], 1000, 1000)
}

func (self *TMyキーボードジショウhandler) Oトキカギウエヘ(カギ byte)	{}

var iマウスジショウhandler Iマウスジショウhandler

type TMyマウスジショウhandler struct {
}

var マウスコンソール Tコンソール = Tコンソール{}
var previousx int16 = 0
var previousy int16 = 0
var xハイチ int16 = 0
var yハイチ int16 = 0

func (self *TMyマウスジショウhandler) Oトキマウスシタ(ボタン int8) {
	buffer := []byte("x")
	マウスコンソール.Mインサツxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyマウスジショウhandler) Oトキマウスウエヘ(ボタン int8)	{}
func (self *TMyマウスジショウhandler) Oトキマウスイドウ(x int8, y int8) {

	xハイチ += int16(x)
	if xハイチ < 0 {
		xハイチ = 0
	}
	if xハイチ >= 80 {
		xハイチ = 79
	}

	yハイチ -= int16(y)

	if yハイチ < 0 {
		yハイチ = 0
	}
	if yハイチ >= 25 {
		yハイチ = 24
	}

	buffer := []byte(" ")
	マウスコンソール.Mインサツxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	マウスコンソール.Mインサツxy(buffer, uint16(xハイチ), uint16(yハイチ))

	previousx = xハイチ
	previousy = yハイチ
}

var デバイスdescriptor TPeripheralcomponentinterconnectデバイスdescriptor
var ipciセイギョキhandler Ipciセイギョキhandler

type TMypciセイギョキhandler struct {
}

var コンソール Tコンソール = Tコンソール{}
var ドライバーカウント uint16 = 0

func (self TMypciセイギョキhandler) Oトキgetドライバー(デバイス TPeripheralcomponentinterconnectデバイスdescriptor) {
	if デバイス.Vセイゾウモトid == 0x1022 && デバイス.Dデバイスid == 0x2000 {
		コンソール.Mインサツxy([]byte("["), 0, 12)
		コンソール.Mインサツ(([]byte)("AMD am79c973"))
		コンソール.Mインサツ([]byte(":"))
		コンソール.MUnsignedinteger16インサツ(デバイス.Vセイゾウモトid)
		コンソール.Mインサツ([]byte(":"))
		コンソール.MUnsignedinteger16インサツ(デバイス.Dデバイスid)
		コンソール.Mインサツ([]byte(":"))
		コンソール.MUnsignedinteger16インサツ(uint16(デバイス.Pポートbase))
		コンソール.Mインサツ([]byte(":"))
		コンソール.MUnsignedinteger32インサツ(デバイス.Iワリコミ)

		コンソール.Mインサツ([]byte("]\n"))
		デバイスdescriptor = デバイス
		ドライバーカウント++
	}
}
func (self TMypciセイギョキhandler) Getドライバー() TPeripheralcomponentinterconnectデバイスdescriptor {
	return デバイスdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pインサツstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	コンソール.Mインサツ(str)
}

func Getファイルサイズ(ファイルメイ []byte) uint32 {
	var ata0s = Tショウサイシヨウギジュツattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	クブン := Tmsdosクブンtable{}
	クブン.Rヨミコミクブン(&ata0s)

	bios := Tファイルタイケイセッテイチ32{}

	var サイズ uint32 = bios.Len(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ)
	ata0s.Flush()

	return サイズ
}

func Mファイルヲヨム(ファイルメイ []byte, データ []byte) {
	var ata0s = Tショウサイシヨウギジュツattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	クブン := Tmsdosクブンtable{}
	クブン.Rヨミコミクブン(&ata0s)

	bios := Tファイルタイケイセッテイチ32{}
	bios.Rヨミコミ(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ, データ)

	ata0s.Flush()
}
func Lヨミコミelf() {

	var ata0s = Tショウサイシヨウギジュツattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	クブン := Tmsdosクブンtable{}
	クブン.Rヨミコミクブン(&ata0s)

	bios := Tファイルタイケイセッテイチ32{}

	var ファイルメイ []byte = ([]byte)("TEST")
	var サイズ uint32 = bios.Len(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ)
	var データbuffer [100 * 1024]byte
	var データ []byte = データbuffer[:]
	bios.Rヨミコミ(&ata0s, クブン.Mbr.Primaryクブン[0], ファイルメイ, データ)

	ジッコウレンケツケイシキ := Elf{}

	ジッコウレンケツケイシキ.Parse(データ[:サイズ], 0x4f00000)

}

var タスクコンソール Tコンソール = Tコンソール{}

func Tカンスウ1() {
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

		Sysインサツunsignedinteger32(esi)

	}
}

func タスクd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func ニュウリョクジショウタスク() {
	for {
		Pプロセスホリュウキーボードジショウイチラン()
		Pプロセスホリュウマウスジショウイチラン()
		halt()
	}
}

func memorytest(y int) {
	メモリカンリシャ := &Tメモリカンリシャ{}
	allocated := uint32(uintptr(メモリカンリシャ.Mキオクリョウイキヲカクホ(1024)))
	コンソール.MUnsignedinteger32インサツxy(allocated, 10, uint16(y))
	if y == 11 {
		メモリカンリシャ.Fアキ(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pイチジテイシloop()
func Rサイドクミコミcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sアリcr3(cr3 uint32)
func Getcr4() uint32
func Enableページカンリ()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getカンスウメイマエ(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcナマエ = runtime.FuncForPC(address).Name()
	var funcバイト []byte = []byte(funcナマエ)

	タスクコンソール.Mインサツxy(funcバイト, 1, 5)
	タスクコンソール.Mインサツ(([]byte)(":"))
	タスクコンソール.MUnsignedinteger32インサツ(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	タスクコンソール.Mインサツunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pページディレクトリentry uintptr, stacktop uintptr, stackbottom uintptr) {

	Mチョクレツログinit()
	コンソール.Mインサツ("\n=== JPN BOOT ===\n")

	コンソール.Mインサツunsignedinteger32(uint32(Pページディレクトリentry), 0, 2)
	コンソール.Mインサツunsignedinteger32(uint32(Pページディレクトリentry), 10, 2)
	コンソール.Mインサツunsignedinteger32(uint32(stacktop), 0, 3)
	コンソール.Mインサツunsignedinteger32(uint32(stackbottom), 10, 3)

	メモリカンリシャ := &Tメモリカンリシャ{}
	メモリカンリシャ.Init(0, Mサイダイマチギョウレツサイズ)

	ページカンリ := &Pページカンリ{}
	ページカンリ.Init(Pページディレクトリentry, 0x500000, メモリカンリシャ)
	ページカンリ.Sharedメモリregion()

	Sアリcr3(uint32(Pページディレクトリentry))
	Enableページカンリ()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	コンソール.Mインサツ("esp:")

	esp := getesp()
	コンソール.MUnsignedinteger32インサツ(uint32(esp))

	tls := gettls()
	コンソール.Mインサツ(([]byte)("tls:"))
	コンソール.MUnsignedinteger32インサツ(tls)

	tss.Iインストール(shareddescriptortable, 7, Segチュウカクデータ, esp)

	Virtテスト()

	cr3 := Rサイドクミコミcr3()
	コンソール.Mインサツ(([]byte)(":cr3:"))
	コンソール.MUnsignedinteger32インサツ(cr3)

	cr0 := Getcr0()
	コンソール.Mインサツ(([]byte)(":cr0:"))
	コンソール.MUnsignedinteger32インサツ(cr0)

	cr4 := Getcr4()
	コンソール.Mインサツ(([]byte)(":cr4:"))
	コンソール.MUnsignedinteger32インサツ(cr4)

	タスクカンリシャ_2 := &Tタスクカンリシャ{}
	タスクカンリシャ_2.Init()

	Iワリコミカンリシャ := &Tワリコミカンリシャ{}
	Iワリコミカンリシャ.Init(0x20, shareddescriptortable, タスクカンリシャ_2)

	ページカンリ.Pページショウガイ(Iワリコミカンリシャ)

	Dドライバーカンリシャ := Tドライバーカンリシャ{}
	Dドライバーカンリシャ.Init()

	スレッドhelper := &Tスレッドhelper{}
	スレッドhelper.Init(メモリカンリシャ)

	プロセスhelper := Pプロセスhelper{}
	プロセスhelper.Init(メモリカンリシャ, Pページディレクトリentry)

	sche := &Sスケジューラ{}
	sche.Init(Iワリコミカンリシャ, メモリカンリシャ, tss)

	sysヨビダシ := &TSyscall{}
	sysヨビダシ.Init(Iワリコミカンリシャ)

	プロセスhelper.Spawn(タスクa, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクb, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクc, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(タスクd1, スレッドhelper, sche, uint32(Pページディレクトリentry), true)
	プロセスhelper.Spawn(ニュウリョクジショウタスク, スレッドhelper, sche, uint32(Pページディレクトリentry), true)

	var サイズ uint32

	var linkerファイル []byte = ([]byte)("LINKER")
	サイズ = Getファイルサイズ(linkerファイル)
	linkeraddress := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	linkerデータ := Getバイトカラポインタ(uintptr(linkeraddress), int(サイズ), int(サイズ))
	Mファイルヲヨム(linkerファイル, linkerデータ)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerデータ)
	elf0.Parse(linkerデータ[:], uint32(Pページディレクトリentry))

	レンケツタイオウヒョウ := Lレンケツタイオウヒョウ{}
	レンケツタイオウヒョウ.Init(メモリカンリシャ)

	var lib1ファイル []byte = ([]byte)("LIB1")
	サイズ = Getファイルサイズ(lib1ファイル)

	lib1address := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	lib1データ := Getバイトカラポインタ(uintptr(lib1address), int(サイズ), int(サイズ))
	Mファイルヲヨム(lib1ファイル, lib1データ)

	lib1elf := Elf{}
	lib1elf.Parse(lib1データ[:], uint32(Pページディレクトリentry))
	メモリカンリシャ.Fアキ(lib1address)

	レンケツタイオウヒョウ.Mマツビニツイカ(uintptr(lib1elf.Dドウテキニ))

	var lib2ファイル []byte = ([]byte)("LIB2")
	サイズ = Getファイルサイズ(lib2ファイル)

	lib2address := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	lib2データ := Getバイトカラポインタ(uintptr(lib2address), int(サイズ), int(サイズ))
	Mファイルヲヨム(lib2ファイル, lib2データ)

	lib2elf := Elf{}
	lib2elf.Parse(lib2データ[:], uint32(Pページディレクトリentry))
	メモリカンリシャ.Fアキ(lib2address)

	レンケツタイオウヒョウ.Mマツビニツイカ(uintptr(lib2elf.Dドウテキニ))

	libレンケツタイオウヒョウ := レンケツタイオウヒョウ.Clone()
	レンケツタイオウヒョウaddress := uint32(uintptr(Pointer(libレンケツタイオウヒョウ.First)))

	lib1got := Getunsignedinteger32ハイレツカラポインタ(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = レンケツタイオウヒョウaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32ハイレツカラポインタ(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = レンケツタイオウヒョウaddress
	lib2got[2] = 0x4000000

	コンソール.Mインサツxy("lib1: ", 1, 8)
	コンソール.MUnsignedinteger32インサツ(lib1elf.Got)
	コンソール.Mインサツ(":")
	コンソール.MUnsignedinteger32インサツ(lib1elf.Dドウテキニ)

	コンソール.Mインサツxy("lib2: ", 1, 9)
	コンソール.MUnsignedinteger32インサツ(lib2elf.Got)
	コンソール.Mインサツ(":")
	コンソール.MUnsignedinteger32インサツ(lib2elf.Dドウテキニ)

	var リヨウシャ1ファイル []byte = ([]byte)("USER1")
	サイズ = Getファイルサイズ(リヨウシャ1ファイル)
	リヨウシャ1address := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	リヨウシャ1データ := Getバイトカラポインタ(uintptr(リヨウシャ1address), int(サイズ), int(サイズ))
	Mファイルヲヨム(リヨウシャ1ファイル, リヨウシャ1データ)

	elf2 := Elf{}

	リヨウシャ1entry := elf2.Getentry(リヨウシャ1データ)
	elf2.Parse(リヨウシャ1データ[:], uint32(Pページディレクトリentry+0x1000))
	ゼンパンoffsettable := elf2.Got

	Pアタイ1レンケツタイオウヒョウ := レンケツタイオウヒョウ.Clone()
	Pアタイ1レンケツタイオウヒョウ.Mマツビニツイカ(uintptr(elf2.Dドウテキニ))

	メモリカンリシャ.Fアキ(リヨウシャ1address)

	var code1ポインタ *uintptr
	var func1val func()

	code1ポインタ = (*uintptr)(メモリカンリシャ.Mキオクリョウイキヲカクホ(4))
	*code1ポインタ = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1ポインタ))

	proc2 := プロセスhelper.Spawn(func1val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x1000), false)
	thr2 := (*Tスレッド)(proc2.Threads.Getat(0))
	thr2.Cpuジョウタイ.Ecx = リヨウシャ1entry
	thr2.Cpuジョウタイ.Edx = ゼンパンoffsettable
	thr2.Cpuジョウタイ.Esi = uint32(uintptr(Pointer(Pアタイ1レンケツタイオウヒョウ.First)))

	コンソール.Mインサツxy("user1: ", 1, 10)
	コンソール.MUnsignedinteger32インサツ(elf2.Got)

	var リヨウシャ2ファイル []byte = ([]byte)("USER2")
	サイズ = Getファイルサイズ(リヨウシャ2ファイル)
	リヨウシャ2address := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	リヨウシャ2データ := Getバイトカラポインタ(uintptr(リヨウシャ2address), int(サイズ), int(サイズ))
	Mファイルヲヨム(リヨウシャ2ファイル, リヨウシャ2データ)

	elf3 := Elf{}

	リヨウシャ2entry := elf3.Getentry(リヨウシャ2データ)
	elf3.Parse(リヨウシャ2データ[:], uint32(Pページディレクトリentry+0x2000))
	ゼンパンoffsettable = elf3.Got

	Pアタイ2レンケツタイオウヒョウ := レンケツタイオウヒョウ.Clone()
	Pアタイ2レンケツタイオウヒョウ.Mマツビニツイカ(uintptr(elf3.Dドウテキニ))

	メモリカンリシャ.Fアキ(リヨウシャ2address)

	var code2ポインタ *uintptr
	var func2val func()

	code2ポインタ = (*uintptr)(メモリカンリシャ.Mキオクリョウイキヲカクホ(4))
	*code2ポインタ = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2ポインタ))

	proc3 := プロセスhelper.Spawn(func2val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x2000), false)
	thr3 := (*Tスレッド)(proc3.Threads.Getat(0))
	thr3.Cpuジョウタイ.Ecx = リヨウシャ2entry
	thr3.Cpuジョウタイ.Edx = ゼンパンoffsettable
	thr3.Cpuジョウタイ.Esi = uint32(uintptr(Pointer(Pアタイ2レンケツタイオウヒョウ.First)))

	コンソール.Mインサツxy("user2: ", 1, 11)
	コンソール.MUnsignedinteger32インサツ(thr3.Cpuジョウタイ.Esi)

	libレンケツタイオウヒョウ.Pインサツ(1, 11)

	var リヨウシャ3ファイル []byte = ([]byte)("USER3")
	サイズ = Getファイルサイズ(リヨウシャ3ファイル)
	リヨウシャ3address := メモリカンリシャ.Mキオクリョウイキヲカクホ(サイズ)
	リヨウシャ3データ := Getバイトカラポインタ(uintptr(リヨウシャ3address), int(サイズ), int(サイズ))
	Mファイルヲヨム(リヨウシャ3ファイル, リヨウシャ3データ)

	elf4 := Elf{}

	リヨウシャ3entry := elf4.Getentry(リヨウシャ3データ)
	elf4.Parse(リヨウシャ3データ[:], uint32(Pページディレクトリentry+0x3000))
	ゼンパンoffsettable = elf4.Got

	Pアタイ3レンケツタイオウヒョウ := レンケツタイオウヒョウ.Clone()
	Pアタイ3レンケツタイオウヒョウ.Mマツビニツイカ(uintptr(elf4.Dドウテキニ))

	メモリカンリシャ.Fアキ(リヨウシャ3address)

	var code3ポインタ *uintptr
	var func3val func()

	code3ポインタ = (*uintptr)(メモリカンリシャ.Mキオクリョウイキヲカクホ(4))
	*code3ポインタ = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3ポインタ))

	proc4 := プロセスhelper.Spawn(func3val, スレッドhelper, sche, uint32(Pページディレクトリentry+0x3000), false)
	thr4 := (*Tスレッド)(proc4.Threads.Getat(0))
	thr4.Cpuジョウタイ.Ecx = リヨウシャ3entry
	thr4.Cpuジョウタイ.Edx = ゼンパンoffsettable
	thr4.Cpuジョウタイ.Esi = uint32(uintptr(Pointer(Pアタイ3レンケツタイオウヒョウ.First)))

	プロセスhelper.Spawn(Tカンスウ1, スレッドhelper, sche, uint32(Pページディレクトリentry+0x4000), true)

	iキーボードジショウhandler = &myキーボードジショウhandler
	キーボードドライバー.Initドライバー(Iワリコミカンリシャ, iキーボードジショウhandler)

	マウスドライバー.Initドライバー(Iワリコミカンリシャ, nil)

	mypciセイギョキhandler := TMypciセイギョキhandler{}
	pciセイギョキ.Init(mypciセイギョキhandler)
	pciセイギョキ.Sセンタクドライバー(&Dドライバーカンリシャ, Iワリコミカンリシャ)
	デバイスdescriptor = mypciセイギョキhandler.Getドライバー()

	sche.Eユウコウ(true)
	Iワリコミカンリシャ.Aユウコウ()

	for {
		halt()
	}

}
