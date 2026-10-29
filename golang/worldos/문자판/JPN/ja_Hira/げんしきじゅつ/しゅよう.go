/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package main

import . "unsafe"
import reflect "reflect"
import runtime "runtime"
import . "はんよう"
import . "gdt"
import . "こんそーる"
import . "わりこみ"
import . "ふくすうたすくかんり"
import . "たすくかんり/tss"

import . "かそうめもり"
import . "ぺーじかんり"
import . "たすくかんり/すれっど"
import . "たすくかんり/すけじゅーら"
import . "たすくかんり/ぷろせす"
import . "どらいばー/どらいばー"

import . "どらいばー/きーぼーど"
import . "どらいばー/いちにゅうりょくそうち"

import . "どらいばー/ata"
import . "ふぁいるしすてむ/msdosくぶん"
import . "ふぁいるしすてむ/fat"

import . "ふぁいるしすてむ/じっこうれんけつけいしき"

import . "しすてむよびだし"

import . "めもりかんりしゃ"
import . "pci"

func halt()

var iきーぼーどじしょうhandler Iきーぼーどじしょうhandler

type TMyきーぼーどじしょうhandler struct {
}

var myきーぼーどじしょうhandler TMyきーぼーどじしょうhandler
var きーぼーどどらいばー Tきーぼーどどらいばー
var まうすどらいばー Tまうすどらいばー
var pciせいぎょき TPeripheralcomponentinterconnectせいぎょき

var きーぼーどこんそーる Tこんそーる = Tこんそーる{}

func (self *TMyきーぼーどじしょうhandler) Oときかぎした(かぎ byte) {
	foo := [1]byte{' '}
	foo[0] = かぎ

	きーぼーどこんそーる.Mいんさつばいとxy(foo[:], 1000, 1000)
}

func (self *TMyきーぼーどじしょうhandler) Oときかぎうえへ(かぎ byte)	{}

var iまうすじしょうhandler Iまうすじしょうhandler

type TMyまうすじしょうhandler struct {
}

var まうすこんそーる Tこんそーる = Tこんそーる{}
var previousx int16 = 0
var previousy int16 = 0
var xはいち int16 = 0
var yはいち int16 = 0

func (self *TMyまうすじしょうhandler) Oときまうすした(ぼたん int8) {
	buffer := []byte("x")
	まうすこんそーる.Mいんさつxy(buffer, uint16(previousx), uint16(previousy))
}
func (self *TMyまうすじしょうhandler) Oときまうすうえへ(ぼたん int8)	{}
func (self *TMyまうすじしょうhandler) Oときまうすいどう(x int8, y int8) {

	xはいち += int16(x)
	if xはいち < 0 {
		xはいち = 0
	}
	if xはいち >= 80 {
		xはいち = 79
	}

	yはいち -= int16(y)

	if yはいち < 0 {
		yはいち = 0
	}
	if yはいち >= 25 {
		yはいち = 24
	}

	buffer := []byte(" ")
	まうすこんそーる.Mいんさつxy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("+")
	まうすこんそーる.Mいんさつxy(buffer, uint16(xはいち), uint16(yはいち))

	previousx = xはいち
	previousy = yはいち
}

var でばいすdescriptor TPeripheralcomponentinterconnectでばいすdescriptor
var ipciせいぎょきhandler Ipciせいぎょきhandler

type TMypciせいぎょきhandler struct {
}

var こんそーる Tこんそーる = Tこんそーる{}
var どらいばーかうんと uint16 = 0

func (self TMypciせいぎょきhandler) Oときgetどらいばー(でばいす TPeripheralcomponentinterconnectでばいすdescriptor) {
	if でばいす.Vせいぞうもとid == 0x1022 && でばいす.Dでばいすid == 0x2000 {
		こんそーる.Mいんさつxy([]byte("["), 0, 12)
		こんそーる.Mいんさつ(([]byte)("AMD am79c973"))
		こんそーる.Mいんさつ([]byte(":"))
		こんそーる.MUnsignedinteger16いんさつ(でばいす.Vせいぞうもとid)
		こんそーる.Mいんさつ([]byte(":"))
		こんそーる.MUnsignedinteger16いんさつ(でばいす.Dでばいすid)
		こんそーる.Mいんさつ([]byte(":"))
		こんそーる.MUnsignedinteger16いんさつ(uint16(でばいす.Pぽーとbase))
		こんそーる.Mいんさつ([]byte(":"))
		こんそーる.MUnsignedinteger32いんさつ(でばいす.Iわりこみ)

		こんそーる.Mいんさつ([]byte("]\n"))
		でばいすdescriptor = でばいす
		どらいばーかうんと++
	}
}
func (self TMypciせいぎょきhandler) Getどらいばー() TPeripheralcomponentinterconnectでばいすdescriptor {
	return でばいすdescriptor
}

var str []byte = ([]byte)("GetStr")

func Getstr() uint32 {
	var b uint32 = uint32(uintptr(Pointer(&str)))
	return b
}
func Pいんさつstr(pstr uint32) {
	var str []byte = *(*[]byte)(Pointer(uintptr(pstr)))
	こんそーる.Mいんさつ(str)
}

func Getふぁいるさいず(ふぁいるめい []byte) uint32 {
	var ata0s = Tしょうさいしようぎじゅつattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	くぶん := Tmsdosくぶんtable{}
	くぶん.Rよみこみくぶん(&ata0s)

	bios := Tふぁいるたいけいせっていち32{}

	var さいず uint32 = bios.Len(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい)
	ata0s.Flush()

	return さいず
}

func Mふぁいるをよむ(ふぁいるめい []byte, でーた []byte) {
	var ata0s = Tしょうさいしようぎじゅつattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	くぶん := Tmsdosくぶんtable{}
	くぶん.Rよみこみくぶん(&ata0s)

	bios := Tふぁいるたいけいせっていち32{}
	bios.Rよみこみ(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい, でーた)

	ata0s.Flush()
}
func Lよみこみelf() {

	var ata0s = Tしょうさいしようぎじゅつattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	くぶん := Tmsdosくぶんtable{}
	くぶん.Rよみこみくぶん(&ata0s)

	bios := Tふぁいるたいけいせっていち32{}

	var ふぁいるめい []byte = ([]byte)("TEST")
	var さいず uint32 = bios.Len(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい)
	var でーたbuffer [100 * 1024]byte
	var でーた []byte = でーたbuffer[:]
	bios.Rよみこみ(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい, でーた)

	じっこうれんけつけいしき := Elf{}

	じっこうれんけつけいしき.Parse(でーた[:さいず], 0x4f00000)

}

var たすくこんそーる Tこんそーる = Tこんそーる{}

func Tかんすう1() {
	buffer := []byte("--TFunc1--")
	for {
		Sysprintf(buffer)
	}
}
func たすくa() {
	buffer := []byte("A")
	for {
		Sysprintf(buffer)

	}
}
func たすくb() {
	buffer := []byte("B")
	for {
		Sysprintf(buffer)
	}
}

func たすくc() {
	buffer := []byte("C")
	for {
		Sysprintf(buffer)
	}
}
func たすくd()

func たすくd0() {
	esi := getesi()
	for {

		Sysいんさつunsignedinteger32(esi)

	}
}

func たすくd1() {
	buffer := ([]byte)("taskD1")
	for {
		Sysprintf(buffer)
	}
}

func にゅうりょくじしょうたすく() {
	for {
		Pぷろせすほりゅうきーぼーどじしょういちらん()
		Pぷろせすほりゅうまうすじしょういちらん()
		halt()
	}
}

func memorytest(y int) {
	めもりかんりしゃ := &Tめもりかんりしゃ{}
	allocated := uint32(uintptr(めもりかんりしゃ.Mきおくりょういきをかくほ(1024)))
	こんそーる.MUnsignedinteger32いんさつxy(allocated, 10, uint16(y))
	if y == 11 {
		めもりかんりしゃ.Fあき(Pointer(uintptr(allocated)))
	}
}

func getesp() uint32
func getesi() uint32
func getgs() uint32
func gettls() uint32
func Pいちじていしloop()
func Rさいどくみこみcr3() uint32

func Getcr0() uint32
func Getcr2() uint32
func Getcr3() uint32
func Sありcr3(cr3 uint32)
func Getcr4() uint32
func Enableぺーじかんり()

func main() {
	KKernelEntry(0, 0, 0)
	for {
		halt()
	}
}

func Getかんすうめいまえ(i interface{}) {
	var address = reflect.ValueOf(i).Pointer()
	var funcなまえ = runtime.FuncForPC(address).Name()
	var funcばいと []byte = []byte(funcなまえ)

	たすくこんそーる.Mいんさつxy(funcばいと, 1, 5)
	たすくこんそーる.Mいんさつ(([]byte)(":"))
	たすくこんそーる.MUnsignedinteger32いんさつ(uint32(uintptr(address)))
}

func printreg() {
	cr0 := Getcr0()
	たすくこんそーる.Mいんさつunsignedinteger32(cr0, 2, 1)
}

var tss *Tssentry = &Tssentry{}

func KKernelEntry(Pぺーじでぃれくとりentry uintptr, stacktop uintptr, stackbottom uintptr) {

	Mちょくれつろぐinit()
	こんそーる.Mいんさつ("\n=== JPN BOOT ===\n")

	こんそーる.Mいんさつunsignedinteger32(uint32(Pぺーじでぃれくとりentry), 0, 2)
	こんそーる.Mいんさつunsignedinteger32(uint32(Pぺーじでぃれくとりentry), 10, 2)
	こんそーる.Mいんさつunsignedinteger32(uint32(stacktop), 0, 3)
	こんそーる.Mいんさつunsignedinteger32(uint32(stackbottom), 10, 3)

	めもりかんりしゃ := &Tめもりかんりしゃ{}
	めもりかんりしゃ.Init(0, Mさいだいまちぎょうれつさいず)

	ぺーじかんり := &Pぺーじかんり{}
	ぺーじかんり.Init(Pぺーじでぃれくとりentry, 0x500000, めもりかんりしゃ)
	ぺーじかんり.Sharedめもりregion()

	Sありcr3(uint32(Pぺーじでぃれくとりentry))
	Enableぺーじかんり()

	shareddescriptortable := &TShareddescriptortable{}
	shareddescriptortable.Init()

	こんそーる.Mいんさつ("esp:")

	esp := getesp()
	こんそーる.MUnsignedinteger32いんさつ(uint32(esp))

	tls := gettls()
	こんそーる.Mいんさつ(([]byte)("tls:"))
	こんそーる.MUnsignedinteger32いんさつ(tls)

	tss.Iいんすとーる(shareddescriptortable, 7, Segちゅうかくでーた, esp)

	Virtてすと()

	cr3 := Rさいどくみこみcr3()
	こんそーる.Mいんさつ(([]byte)(":cr3:"))
	こんそーる.MUnsignedinteger32いんさつ(cr3)

	cr0 := Getcr0()
	こんそーる.Mいんさつ(([]byte)(":cr0:"))
	こんそーる.MUnsignedinteger32いんさつ(cr0)

	cr4 := Getcr4()
	こんそーる.Mいんさつ(([]byte)(":cr4:"))
	こんそーる.MUnsignedinteger32いんさつ(cr4)

	たすくかんりしゃ_2 := &Tたすくかんりしゃ{}
	たすくかんりしゃ_2.Init()

	Iわりこみかんりしゃ := &Tわりこみかんりしゃ{}
	Iわりこみかんりしゃ.Init(0x20, shareddescriptortable, たすくかんりしゃ_2)

	ぺーじかんり.Pぺーじしょうがい(Iわりこみかんりしゃ)

	Dどらいばーかんりしゃ := Tどらいばーかんりしゃ{}
	Dどらいばーかんりしゃ.Init()

	すれっどhelper := &Tすれっどhelper{}
	すれっどhelper.Init(めもりかんりしゃ)

	ぷろせすhelper := Pぷろせすhelper{}
	ぷろせすhelper.Init(めもりかんりしゃ, Pぺーじでぃれくとりentry)

	sche := &Sすけじゅーら{}
	sche.Init(Iわりこみかんりしゃ, めもりかんりしゃ, tss)

	sysよびだし := &TSyscall{}
	sysよびだし.Init(Iわりこみかんりしゃ)

	ぷろせすhelper.Spawn(たすくa, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry), true)
	ぷろせすhelper.Spawn(たすくb, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry), true)
	ぷろせすhelper.Spawn(たすくc, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry), true)
	ぷろせすhelper.Spawn(たすくd1, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry), true)
	ぷろせすhelper.Spawn(にゅうりょくじしょうたすく, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry), true)

	var さいず uint32

	var linkerふぁいる []byte = ([]byte)("LINKER")
	さいず = Getふぁいるさいず(linkerふぁいる)
	linkeraddress := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	linkerでーた := Getばいとからぽいんた(uintptr(linkeraddress), int(さいず), int(さいず))
	Mふぁいるをよむ(linkerふぁいる, linkerでーた)

	elf0 := Elf{}
	linkerentry := elf0.Getentry(linkerでーた)
	elf0.Parse(linkerでーた[:], uint32(Pぺーじでぃれくとりentry))

	れんけつたいおうひょう := Lれんけつたいおうひょう{}
	れんけつたいおうひょう.Init(めもりかんりしゃ)

	var lib1ふぁいる []byte = ([]byte)("LIB1")
	さいず = Getふぁいるさいず(lib1ふぁいる)

	lib1address := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	lib1でーた := Getばいとからぽいんた(uintptr(lib1address), int(さいず), int(さいず))
	Mふぁいるをよむ(lib1ふぁいる, lib1でーた)

	lib1elf := Elf{}
	lib1elf.Parse(lib1でーた[:], uint32(Pぺーじでぃれくとりentry))
	めもりかんりしゃ.Fあき(lib1address)

	れんけつたいおうひょう.Mまつびについか(uintptr(lib1elf.Dどうてきに))

	var lib2ふぁいる []byte = ([]byte)("LIB2")
	さいず = Getふぁいるさいず(lib2ふぁいる)

	lib2address := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	lib2でーた := Getばいとからぽいんた(uintptr(lib2address), int(さいず), int(さいず))
	Mふぁいるをよむ(lib2ふぁいる, lib2でーた)

	lib2elf := Elf{}
	lib2elf.Parse(lib2でーた[:], uint32(Pぺーじでぃれくとりentry))
	めもりかんりしゃ.Fあき(lib2address)

	れんけつたいおうひょう.Mまつびについか(uintptr(lib2elf.Dどうてきに))

	libれんけつたいおうひょう := れんけつたいおうひょう.Clone()
	れんけつたいおうひょうaddress := uint32(uintptr(Pointer(libれんけつたいおうひょう.First)))

	lib1got := Getunsignedinteger32はいれつからぽいんた(uintptr(lib1elf.Got), 4, 4)
	lib1got[1] = れんけつたいおうひょうaddress
	lib1got[2] = 0x4000000

	lib2got := Getunsignedinteger32はいれつからぽいんた(uintptr(lib2elf.Got), 4, 4)
	lib2got[1] = れんけつたいおうひょうaddress
	lib2got[2] = 0x4000000

	こんそーる.Mいんさつxy("lib1: ", 1, 8)
	こんそーる.MUnsignedinteger32いんさつ(lib1elf.Got)
	こんそーる.Mいんさつ(":")
	こんそーる.MUnsignedinteger32いんさつ(lib1elf.Dどうてきに)

	こんそーる.Mいんさつxy("lib2: ", 1, 9)
	こんそーる.MUnsignedinteger32いんさつ(lib2elf.Got)
	こんそーる.Mいんさつ(":")
	こんそーる.MUnsignedinteger32いんさつ(lib2elf.Dどうてきに)

	var りようしゃ1ふぁいる []byte = ([]byte)("USER1")
	さいず = Getふぁいるさいず(りようしゃ1ふぁいる)
	りようしゃ1address := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	りようしゃ1でーた := Getばいとからぽいんた(uintptr(りようしゃ1address), int(さいず), int(さいず))
	Mふぁいるをよむ(りようしゃ1ふぁいる, りようしゃ1でーた)

	elf2 := Elf{}

	りようしゃ1entry := elf2.Getentry(りようしゃ1でーた)
	elf2.Parse(りようしゃ1でーた[:], uint32(Pぺーじでぃれくとりentry+0x1000))
	ぜんぱんoffsettable := elf2.Got

	Pあたい1れんけつたいおうひょう := れんけつたいおうひょう.Clone()
	Pあたい1れんけつたいおうひょう.Mまつびについか(uintptr(elf2.Dどうてきに))

	めもりかんりしゃ.Fあき(りようしゃ1address)

	var code1ぽいんた *uintptr
	var func1val func()

	code1ぽいんた = (*uintptr)(めもりかんりしゃ.Mきおくりょういきをかくほ(4))
	*code1ぽいんた = uintptr(linkerentry)
	func1val = *(*func())(Pointer(&code1ぽいんた))

	proc2 := ぷろせすhelper.Spawn(func1val, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry+0x1000), false)
	thr2 := (*Tすれっど)(proc2.Threads.Getat(0))
	thr2.Cpuじょうたい.Ecx = りようしゃ1entry
	thr2.Cpuじょうたい.Edx = ぜんぱんoffsettable
	thr2.Cpuじょうたい.Esi = uint32(uintptr(Pointer(Pあたい1れんけつたいおうひょう.First)))

	こんそーる.Mいんさつxy("user1: ", 1, 10)
	こんそーる.MUnsignedinteger32いんさつ(elf2.Got)

	var りようしゃ2ふぁいる []byte = ([]byte)("USER2")
	さいず = Getふぁいるさいず(りようしゃ2ふぁいる)
	りようしゃ2address := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	りようしゃ2でーた := Getばいとからぽいんた(uintptr(りようしゃ2address), int(さいず), int(さいず))
	Mふぁいるをよむ(りようしゃ2ふぁいる, りようしゃ2でーた)

	elf3 := Elf{}

	りようしゃ2entry := elf3.Getentry(りようしゃ2でーた)
	elf3.Parse(りようしゃ2でーた[:], uint32(Pぺーじでぃれくとりentry+0x2000))
	ぜんぱんoffsettable = elf3.Got

	Pあたい2れんけつたいおうひょう := れんけつたいおうひょう.Clone()
	Pあたい2れんけつたいおうひょう.Mまつびについか(uintptr(elf3.Dどうてきに))

	めもりかんりしゃ.Fあき(りようしゃ2address)

	var code2ぽいんた *uintptr
	var func2val func()

	code2ぽいんた = (*uintptr)(めもりかんりしゃ.Mきおくりょういきをかくほ(4))
	*code2ぽいんた = uintptr(linkerentry)
	func2val = *(*func())(Pointer(&code2ぽいんた))

	proc3 := ぷろせすhelper.Spawn(func2val, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry+0x2000), false)
	thr3 := (*Tすれっど)(proc3.Threads.Getat(0))
	thr3.Cpuじょうたい.Ecx = りようしゃ2entry
	thr3.Cpuじょうたい.Edx = ぜんぱんoffsettable
	thr3.Cpuじょうたい.Esi = uint32(uintptr(Pointer(Pあたい2れんけつたいおうひょう.First)))

	こんそーる.Mいんさつxy("user2: ", 1, 11)
	こんそーる.MUnsignedinteger32いんさつ(thr3.Cpuじょうたい.Esi)

	libれんけつたいおうひょう.Pいんさつ(1, 11)

	var りようしゃ3ふぁいる []byte = ([]byte)("USER3")
	さいず = Getふぁいるさいず(りようしゃ3ふぁいる)
	りようしゃ3address := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	りようしゃ3でーた := Getばいとからぽいんた(uintptr(りようしゃ3address), int(さいず), int(さいず))
	Mふぁいるをよむ(りようしゃ3ふぁいる, りようしゃ3でーた)

	elf4 := Elf{}

	りようしゃ3entry := elf4.Getentry(りようしゃ3でーた)
	elf4.Parse(りようしゃ3でーた[:], uint32(Pぺーじでぃれくとりentry+0x3000))
	ぜんぱんoffsettable = elf4.Got

	Pあたい3れんけつたいおうひょう := れんけつたいおうひょう.Clone()
	Pあたい3れんけつたいおうひょう.Mまつびについか(uintptr(elf4.Dどうてきに))

	めもりかんりしゃ.Fあき(りようしゃ3address)

	var code3ぽいんた *uintptr
	var func3val func()

	code3ぽいんた = (*uintptr)(めもりかんりしゃ.Mきおくりょういきをかくほ(4))
	*code3ぽいんた = uintptr(linkerentry)
	func3val = *(*func())(Pointer(&code3ぽいんた))

	proc4 := ぷろせすhelper.Spawn(func3val, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry+0x3000), false)
	thr4 := (*Tすれっど)(proc4.Threads.Getat(0))
	thr4.Cpuじょうたい.Ecx = りようしゃ3entry
	thr4.Cpuじょうたい.Edx = ぜんぱんoffsettable
	thr4.Cpuじょうたい.Esi = uint32(uintptr(Pointer(Pあたい3れんけつたいおうひょう.First)))

	ぷろせすhelper.Spawn(Tかんすう1, すれっどhelper, sche, uint32(Pぺーじでぃれくとりentry+0x4000), true)

	iきーぼーどじしょうhandler = &myきーぼーどじしょうhandler
	きーぼーどどらいばー.Initどらいばー(Iわりこみかんりしゃ, iきーぼーどじしょうhandler)

	まうすどらいばー.Initどらいばー(Iわりこみかんりしゃ, nil)

	mypciせいぎょきhandler := TMypciせいぎょきhandler{}
	pciせいぎょき.Init(mypciせいぎょきhandler)
	pciせいぎょき.Sせんたくどらいばー(&Dどらいばーかんりしゃ, Iわりこみかんりしゃ)
	でばいすdescriptor = mypciせいぎょきhandler.Getどらいばー()

	sche.Eゆうこう(true)
	Iわりこみかんりしゃ.Aゆうこう()

	for {
		halt()
	}

}
