/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ぷろせす

import . "unsafe"
import . "はんよう/いちらん"
import mem "めもりかんりしゃ"
import . "たすくかんり/すれっど"
import . "たすくかんり/すけじゅーら"
import . "はんよう"

const Procりようしゃheapさいず = 1 * 1024 * 1024

type Pぷろせす struct {
	id		uint32
	syscallid	int
	Isりようしゃすぺーす	bool
	ひきすう		*[]byte

	Tすれっどいちらん	Linkedいちらん
	Threads	*Linkedいちらん
	Fふぁいるなまえ	[]byte

	Pぺーじでぃれくとりentry	uintptr
}

func (self *Pぷろせす) Init(mem *mem.Tめもりかんりしゃ) {
	self.Tすれっどいちらん = Linkedいちらん{}
	self.Threads = &self.Tすれっどいちらん
	self.Threads.Init(mem)
}

type Pぷろせすhelper struct {
	ぷろせす_2			Linkedいちらん
	mem			*mem.Tめもりかんりしゃ
	ちゅうかくぺーじでぃれくとりentry	uintptr
}

func (self *Pぷろせすhelper) Init(mem *mem.Tめもりかんりしゃ, ちゅうかくぺーじでぃれくとりentry uintptr) {
	self.mem = mem
	self.ぷろせす_2 = Linkedいちらん{}
	self.ぷろせす_2.Init(self.mem)
	self.ちゅうかくぺーじでぃれくとりentry = ちゅうかくぺーじでぃれくとりentry
}

func (self *Pぷろせすhelper) Cさくせい(entrypoint func(), すれっどhelper *Tすれっどhelper, Pぺーじでぃれくとりentry uint32, isちゅうかく bool) Pぷろせす {
	ぷろせす := (*Pぷろせす)(self.mem.Mきおくりょういきをかくほ(uint32(Sizeof(Pぷろせす{}))))
	if ぷろせす == nil {
		return Pぷろせす{}
	}
	ぷろせす.Init(self.mem)
	ぷろせす.id = Allocatepid()
	ぷろせす.Pぺーじでぃれくとりentry = uintptr(Pぺーじでぃれくとりentry)
	しゅようすれっど := すれっどhelper.Cさくせいぽいんたからかんすう(entrypoint, Pぺーじでぃれくとりentry, isちゅうかく)
	if しゅようすれっど != nil {
		しゅようすれっど.Pid = ぷろせす.id
		しゅようすれっど.Parentpid = 0
		ぷろせす.Threads.Mまつびについか(uintptr(Pointer(しゅようすれっど)))
	}

	self.ぷろせす_2.Mまつびについか(uintptr(Pointer(ぷろせす)))

	return *ぷろせす
}

func (self *Pぷろせすhelper) Spawn(entrypoint func(), すれっどhelper *Tすれっどhelper, すけじゅーら *Sすけじゅーら, Pぺーじでぃれくとりentry uint32, isちゅうかく bool) Pぷろせす {
	ぷろせす := self.Cさくせい(entrypoint, すれっどhelper, Pぺーじでぃれくとりentry, isちゅうかく)
	if ぷろせす.Threads != nil && ぷろせす.Threads.Sさいず_2 > 0 {
		すれっど := (*Tすれっど)(ぷろせす.Threads.Getat(0))
		if すれっど != nil && すけじゅーら != nil {
			すけじゅーら.Aついかすれっど(すれっど)
		}
	}
	return ぷろせす
}

func (self *Pぷろせすhelper) ふくせいぺーじでぃれくとり(てんそうもとentry uintptr, てんそうさきentry uintptr) {
	てんそうもと_2 := Getunsignedinteger32はいれつからぽいんた(てんそうもとentry, 1024, 1024)
	てんそうさき_2 := Getunsignedinteger32はいれつからぽいんた(てんそうさきentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		てんそうさき_2[i] = てんそうもと_2[i]
	}
}
func (self *Pぷろせすhelper) Cさくせいからでーた() Pぷろせす {
	ぷろせす := Pぷろせす{}
	return ぷろせす
}
