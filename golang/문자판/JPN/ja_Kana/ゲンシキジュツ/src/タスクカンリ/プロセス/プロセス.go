package プロセス

import . "unsafe"
import . "ハンヨウ/イチラン"
import mem "メモリカンリシャ"
import . "タスクカンリ/スレッド"
import . "タスクカンリ/スケジューラ"
import . "ハンヨウ"

const Procリヨウシャheapサイズ = 1 * 1024 * 1024

type Pプロセス struct {
	id		uint32
	syscallid	int
	Isリヨウシャスペース	bool
	ヒキスウ		*[]byte

	Tスレッドイチラン	Linkedイチラン
	Threads	*Linkedイチラン
	Fファイルナマエ	[]byte

	Pページディレクトリentry	uintptr
}

func (self *Pプロセス) Init(mem *mem.Tメモリカンリシャ) {
	self.Tスレッドイチラン = Linkedイチラン{}
	self.Threads = &self.Tスレッドイチラン
	self.Threads.Init(mem)
}

type Pプロセスhelper struct {
	プロセス_2			Linkedイチラン
	mem			*mem.Tメモリカンリシャ
	チュウカクページディレクトリentry	uintptr
}

func (self *Pプロセスhelper) Init(mem *mem.Tメモリカンリシャ, チュウカクページディレクトリentry uintptr) {
	self.mem = mem
	self.プロセス_2 = Linkedイチラン{}
	self.プロセス_2.Init(self.mem)
	self.チュウカクページディレクトリentry = チュウカクページディレクトリentry
}

func (self *Pプロセスhelper) Cサクセイ(entrypoint func(), スレッドhelper *Tスレッドhelper, Pページディレクトリentry uint32, isチュウカク bool) Pプロセス {
	プロセス := (*Pプロセス)(self.mem.Mキオクリョウイキヲカクホ(uint32(Sizeof(Pプロセス{}))))
	if プロセス == nil {
		return Pプロセス{}
	}
	プロセス.Init(self.mem)
	プロセス.id = Allocatepid()
	プロセス.Pページディレクトリentry = uintptr(Pページディレクトリentry)
	シュヨウスレッド := スレッドhelper.Cサクセイポインタカラカンスウ(entrypoint, Pページディレクトリentry, isチュウカク)
	if シュヨウスレッド != nil {
		シュヨウスレッド.Pid = プロセス.id
		シュヨウスレッド.Parentpid = 0
		プロセス.Threads.Mマツビニツイカ(uintptr(Pointer(シュヨウスレッド)))
	}

	self.プロセス_2.Mマツビニツイカ(uintptr(Pointer(プロセス)))

	return *プロセス
}

func (self *Pプロセスhelper) Spawn(entrypoint func(), スレッドhelper *Tスレッドhelper, スケジューラ *Sスケジューラ, Pページディレクトリentry uint32, isチュウカク bool) Pプロセス {
	プロセス := self.Cサクセイ(entrypoint, スレッドhelper, Pページディレクトリentry, isチュウカク)
	if プロセス.Threads != nil && プロセス.Threads.Sサイズ_2 > 0 {
		スレッド := (*Tスレッド)(プロセス.Threads.Getat(0))
		if スレッド != nil && スケジューラ != nil {
			スケジューラ.Aツイカスレッド(スレッド)
		}
	}
	return プロセス
}

func (self *Pプロセスhelper) フクセイページディレクトリ(テンソウモトentry uintptr, テンソウサキentry uintptr) {
	テンソウモト_2 := Getunsignedinteger32ハイレツカラポインタ(テンソウモトentry, 1024, 1024)
	テンソウサキ_2 := Getunsignedinteger32ハイレツカラポインタ(テンソウサキentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		テンソウサキ_2[i] = テンソウモト_2[i]
	}
}
func (self *Pプロセスhelper) Cサクセイカラデータ() Pプロセス {
	プロセス := Pプロセス{}
	return プロセス
}
