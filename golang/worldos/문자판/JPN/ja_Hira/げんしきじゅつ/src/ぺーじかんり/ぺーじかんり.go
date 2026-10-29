/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ぺーじかんり

import unsafe "unsafe"
import . "わりこみ"
import . "めもりかんりしゃ"
import . "はんよう"

type Pぺーじでぃれくとりentry_2 uintptr

const (
	Pぺーじげんざい		uint32	= 0x001
	Pぺーじwritable	uint32	= 0x002
	Pぺーじりようしゃ		uint32	= 0x004
	Pぺーじふれーむ	uint32	= 0xFFFFF000
	Pぺーじcow		uint32	= 0x200
)

func Sありばいとataddress(x byte, address uint32)
func Sありunsignedinteger8ataddress(x uint8, address uint32)
func Sありunsignedinteger32ataddress(x uint32, address uint32)

func getcr2() uint32

func ありcr3(きおくぺーじじょういおもて uint32)
func getcr3() uint32

type Pぺーじかんり struct {
	Tわりこみhandler
}
type Tcowふれーむかんりしゃ struct {
	mem		*Tめもりかんりしゃ
	refs		[]uint16
	ふれーむかうんと	uint32
}

var (
	Pぺーじでぃれくとりentry	uintptr
	Pぺーじtableentry	uint32
	pdelen		uint32
	virtlen		uint32
	cowふれーむかんりしゃ	Tcowふれーむかんりしゃ
)

func (self *Tcowふれーむかんりしゃ) Init(mem *Tめもりかんりしゃ, ふれーむかうんと uint32) bool {
	self.mem = mem
	self.ふれーむかうんと = ふれーむかうんと
	referenceばいと := ふれーむかうんと * uint32(unsafe.Sizeof(uint16(0)))
	referenceぽいんた := mem.Mきおくりょういきをかくほ(referenceばいと)
	if referenceぽいんた == nil {
		self.refs = nil
		self.ふれーむかうんと = 0
		return false
	}
	self.refs = (*[1 << 28]uint16)(referenceぽいんた)[:ふれーむかうんと:ふれーむかうんと]
	for i := uint32(0); i < ふれーむかうんと; i++ {
		self.refs[i] = 0
	}
	return true
}

func (self *Tcowふれーむかんりしゃ) Reference(ふれーむ uint32) uint16 {
	idx := ふれーむ >> 12
	if idx >= self.ふれーむかうんと || self.refs == nil {
		return 0
	}
	return self.refs[idx]
}

func (self *Tcowふれーむかんりしゃ) Increment(ふれーむ uint32) {
	idx := ふれーむ >> 12
	if idx >= self.ふれーむかうんと || self.refs == nil {
		return
	}
	if self.refs[idx] == 0 {
		self.refs[idx] = 2
	} else {
		self.refs[idx]++
	}
}

func (self *Tcowふれーむかんりしゃ) Decrement(ふれーむ uint32) {
	idx := ふれーむ >> 12
	if idx >= self.ふれーむかうんと || self.refs == nil || self.refs[idx] == 0 {
		return
	}
	self.refs[idx]--
}

func (self *Pぺーじかんり) Init(ぺーじでぃれくとりentry uintptr, ぺーじtableentry uint32, めもりかんりしゃ *Tめもりかんりしゃ) {

	Pぺーじでぃれくとりentry = ぺーじでぃれくとりentry
	Pぺーじtableentry = ぺーじtableentry

	virtlen = uint32(6)
	pdelen = uint32(32)

	cowふれーむかんりしゃ.Init(めもりかんりしゃ, (512*1024*1024)>>12)

	for i := uint32(0); i <= virtlen; i++ {

		for pde := uint32(0); pde < pdelen; pde++ {

			addressぽいんた, _ := めもりかんりしゃ.Alignedmalloc(0x1000)
			if addressぽいんた == nil {
				return
			}
			address := uint32(uintptr(addressぽいんた))

			Sありunsignedinteger32ataddress(address|0x87, uint32(ぺーじでぃれくとりentry)+pde*4)

			for pte := uint32(0); pte < 1024; pte++ {
				Sありunsignedinteger32ataddress((((pde+i*pdelen)*1024+pte)*0x1000)|0x117, address+pte*4)
			}
		}
		ぺーじでぃれくとりentry = ぺーじでぃれくとりentry + 0x1000
	}

}
func (self *Pぺーじかんり) Sharedめもりregion() {

	ぺーじでぃれくとりentry := Pぺーじでぃれくとりentry
	kぺーじでぃれくとりentry := Pぺーじでぃれくとりentry

	for i := uint32(1); i <= virtlen; i++ {

		ぺーじでぃれくとりentry = ぺーじでぃれくとりentry + 0x1000

		pde := uint32(0)

		for ; pde < 12; pde++ {
			v := Getあたい(uint32(kぺーじでぃれくとりentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sありunsignedinteger32ataddress(v|0x87, uint32(ぺーじでぃれくとりentry)+pde*4)

		}

		pde = 16
		for ; pde < 20; pde++ {
			v := Getあたい(uint32(kぺーじでぃれくとりentry) + pde*4)
			v = (v & 0xFFFFF000)
			Sありunsignedinteger32ataddress(v|0x87, uint32(ぺーじでぃれくとりentry)+pde*4)

		}

	}
}
func (self *Pぺーじかんり) Pぺーじしょうがい(かんりしゃ *Tわりこみかんりしゃ) {
	わりこみhandler = とってぺーじかんりわりこみ

	var address uintptr
	address = uintptr(unsafe.Pointer(&わりこみhandler))
	self.Tわりこみhandler.Init(0xE, uintptr(unsafe.Pointer(かんりしゃ)), address)
}

var わりこみhandler func(uint32) uint32

func とってぺーじかんりわりこみ(esp uint32) uint32 {
	if Rかいけつふくせいときかきこみしょうがい() {
		return esp
	}
	return Hとってfatalわりこみふれーむ(esp, 0x0E)
}

func Cloneaddressすぺーすcow(てんそうもとぺーじでぃれくとり uint32) uint32 {
	if Aゆうこうめもりかんりしゃ == nil || てんそうもとぺーじでぃれくとり == 0 {
		return 0
	}
	てんそうさきぽいんた, _ := Aゆうこうめもりかんりしゃ.Alignedmalloc(0x1000)
	if てんそうさきぽいんた == nil {
		return 0
	}
	てんそうさきぺーじでぃれくとり := uint32(uintptr(てんそうさきぽいんた))
	for i := uint32(0); i < 1024; i++ {
		Sありunsignedinteger32ataddress(0, てんそうさきぺーじでぃれくとり+i*4)
	}

	for pde := uint32(0); pde < 1024; pde++ {
		てんそうもとpdeaddress := てんそうもとぺーじでぃれくとり + pde*4
		てんそうもとpde := Getあたい(てんそうもとpdeaddress)
		if (てんそうもとpde & Pぺーじげんざい) == 0 {
			continue
		}
		if issharedpde(pde) {
			Sありunsignedinteger32ataddress(てんそうもとpde, てんそうさきぺーじでぃれくとり+pde*4)
			continue
		}

		てんそうさきptぽいんた, _ := Aゆうこうめもりかんりしゃ.Alignedmalloc(0x1000)
		if てんそうさきptぽいんた == nil {
			continue
		}
		てんそうもとpt := てんそうもとpde & Pぺーじふれーむ
		てんそうさきpt := uint32(uintptr(てんそうさきptぽいんた))
		Sありunsignedinteger32ataddress((てんそうさきpt | (てんそうもとpde & 0xFFF)), てんそうさきぺーじでぃれくとり+pde*4)

		for pte := uint32(0); pte < 1024; pte++ {
			pteaddress := てんそうもとpt + pte*4
			entry := Getあたい(pteaddress)
			if (entry & Pぺーじげんざい) != 0 {
				if (entry & Pぺーじwritable) != 0 {
					entry = (entry &^ Pぺーじwritable) | Pぺーじcow
					Sありunsignedinteger32ataddress(entry, pteaddress)
					cowふれーむかんりしゃ.Increment(entry & Pぺーじふれーむ)
				} else if (entry & Pぺーじcow) != 0 {
					cowふれーむかんりしゃ.Increment(entry & Pぺーじふれーむ)
				}
			}
			Sありunsignedinteger32ataddress(entry, てんそうさきpt+pte*4)
		}
	}
	さいどくみこみcr3()
	return てんそうさきぺーじでぃれくとり
}

func Rかいけつふくせいときかきこみしょうがい() bool {
	if Aゆうこうめもりかんりしゃ == nil {
		return false
	}
	しょうがいaddress := getcr2()
	きおくぺーじじょういおもて := getcr3()
	pdeaddress := きおくぺーじじょういおもて + ((しょうがいaddress>>22)&0x3FF)*4
	pde := Getあたい(pdeaddress)
	if (pde & Pぺーじげんざい) == 0 {
		return false
	}
	pt := pde & Pぺーじふれーむ
	pteaddress := pt + ((しょうがいaddress>>12)&0x3FF)*4
	pte := Getあたい(pteaddress)
	if (pte&Pぺーじcow) == 0 || (pte&Pぺーじげんざい) == 0 {
		return false
	}
	oldふれーむ := pte & Pぺーじふれーむ
	if cowふれーむかんりしゃ.Reference(oldふれーむ) <= 1 {
		Sありunsignedinteger32ataddress((pte|Pぺーじwritable)&^Pぺーじcow, pteaddress)
		さいどくみこみcr3()
		return true
	}

	しんきぽいんた, _ := Aゆうこうめもりかんりしゃ.Alignedmalloc(0x1000)
	if しんきぽいんた == nil {
		return false
	}
	しんきふれーむ := uint32(uintptr(しんきぽいんた)) & Pぺーじふれーむ

	てんそうもと_2 := Getばいとからぽいんた(uintptr(しょうがいaddress&Pぺーじふれーむ), 0x1000, 0x1000)
	てんそうさき_2 := Getばいとからぽいんた(uintptr(しんきふれーむ), 0x1000, 0x1000)
	copy(てんそうさき_2, てんそうもと_2)
	cowふれーむかんりしゃ.Decrement(oldふれーむ)
	Sありunsignedinteger32ataddress((しんきふれーむ|(pte&0xFFF)|Pぺーじwritable)&^Pぺーじcow, pteaddress)
	さいどくみこみcr3()
	return true
}

func issharedpde(pde uint32) bool {
	if pde < 12 {
		return true
	}
	if pde >= 16 && pde < 20 {
		return true
	}
	return false
}

func さいどくみこみcr3() {
	cr3 := getcr3()
	ありcr3(cr3)
}

func Sありばいとじゅしんぺーじでぃれくとり(x byte, address uint32, きおくぺーじじょういおもて uint32) {
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	Sありばいとataddress(x, address)
	ありcr3(oldcr3)
}

func Sありぶろっくじゅしんぺーじでぃれくとり(てんそうもと_2 []byte, てんそうさき_2 []byte, さいず uint32, きおくぺーじじょういおもて uint32) {
	if さいず == 0 || きおくぺーじじょういおもて == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	makerangeぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて, uint32(uintptr(unsafe.Pointer(&てんそうさき_2[0]))), さいず)

	for i := uint32(0); i < さいず; i++ {
		てんそうさき_2[i] = てんそうもと_2[i]
	}
	ありcr3(oldcr3)
}

func Zすうちの0ぶろっくじゅしんぺーじでぃれくとり(address uint32, さいず uint32, きおくぺーじじょういおもて uint32) {
	if さいず == 0 || きおくぺーじじょういおもて == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	makerangeぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて, address, さいず)
	てんそうさき_2 := Getばいとからぽいんた(uintptr(address), int(さいず), int(さいず))
	for i := uint32(0); i < さいず; i++ {
		てんそうさき_2[i] = 0
	}
	ありcr3(oldcr3)
}

func makeぺーじぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて uint32, かそうaddress uint32) bool {
	pde := Getあたい(きおくぺーじじょういおもて + ((かそうaddress>>22)&0x3FF)*4)
	if (pde & Pぺーじげんざい) == 0 {
		return false
	}
	pteaddress := (pde & Pぺーじふれーむ) + ((かそうaddress>>12)&0x3FF)*4
	pte := Getあたい(pteaddress)
	if (pte & Pぺーじげんざい) == 0 {
		return false
	}
	if (pte & Pぺーじcow) == 0 {
		return (pte & Pぺーじwritable) != 0
	}
	if Aゆうこうめもりかんりしゃ == nil {
		return false
	}
	しんきぽいんた, _ := Aゆうこうめもりかんりしゃ.Alignedmalloc(0x1000)
	if しんきぽいんた == nil {
		return false
	}
	しんきふれーむ := uint32(uintptr(しんきぽいんた)) & Pぺーじふれーむ
	てんそうもと_2 := Getばいとからぽいんた(uintptr(かそうaddress&Pぺーじふれーむ), 0x1000, 0x1000)
	てんそうさき_2 := Getばいとからぽいんた(uintptr(しんきふれーむ), 0x1000, 0x1000)
	copy(てんそうさき_2, てんそうもと_2)
	cowふれーむかんりしゃ.Decrement(pte & Pぺーじふれーむ)
	Sありunsignedinteger32ataddress((しんきふれーむ|(pte&0xFFF)|Pぺーじwritable)&^Pぺーじcow, pteaddress)
	// Publish the new physical frame before writing through its virtual address.
	さいどくみこみcr3()
	return true
}

func makerangeぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて uint32, address uint32, さいず uint32) bool {
	if さいず == 0 {
		return true
	}
	さいご := address + さいず - 1
	if さいご < address {
		return false
	}
	for ぺーじ := address & Pぺーじふれーむ; ; ぺーじ += 0x1000 {
		if !makeぺーじぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて, ぺーじ) {
			return false
		}
		if ぺーじ == (さいご & Pぺーじふれーむ) {
			break
		}
	}
	return true
}

func Makerangeぷらいべーとwritable(きおくぺーじじょういおもて uint32, address uint32, さいず uint32) bool {
	if きおくぺーじじょういおもて == 0 {
		return false
	}
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	ok := makerangeぷらいべーとwritableげんざいのにちじ(きおくぺーじじょういおもて, address, さいず)
	ありcr3(oldcr3)
	return ok
}

func Sありunsignedinteger32じゅしんぺーじでぃれくとり(x uint32, address uint32, きおくぺーじじょういおもて uint32) {
	if きおくぺーじじょういおもて == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	Sありunsignedinteger32ataddress(x, address)
	ありcr3(oldcr3)
}

func Getあたい(address uint32) uint32 {
	var orgあたい uint32 = *(*uint32)(unsafe.Pointer(uintptr(address)))
	return orgあたい
}
func Getあたいじゅしんぺーじでぃれくとり(address uint32, きおくぺーじじょういおもて uint32) uint32 {
	if きおくぺーじじょういおもて == 0 {
		return 0
	}
	oldcr3 := getcr3()
	ありcr3(きおくぺーじじょういおもて)
	v := Getあたい(address)
	ありcr3(oldcr3)
	return v
}

var v uint32 = 0

func Cふくせいぺーじふれーむぶろっく(xぺーじでぃれくとり uint32, yぺーじでぃれくとり uint32, vaddress uint32) {
	if xぺーじでぃれくとり == 0 || yぺーじでぃれくとり == 0 {
		return
	}
	oldcr3 := getcr3()
	ありcr3(xぺーじでぃれくとり)
	v = Getあたい(vaddress)
	Sありunsignedinteger32じゅしんぺーじでぃれくとり(v, vaddress, yぺーじでぃれくとり)

	ありcr3(oldcr3)
}
