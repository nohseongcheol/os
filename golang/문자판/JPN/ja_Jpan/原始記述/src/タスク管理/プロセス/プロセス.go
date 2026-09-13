package プロセス

import . "unsafe"
import . "汎用/一覧"
import mem "メモリ管理者"
import . "タスク管理/スレッド"
import . "タスク管理/スケジューラ"
import . "汎用"

const Proc利用者heapサイズ = 1 * 1024 * 1024

type Pプロセス struct {
	id		uint32
	syscallid	int
	Is利用者スペース	bool
	引数		*[]byte

	Tスレッド一覧	Linked一覧
	Threads	*Linked一覧
	Fファイル名前	[]byte

	Pページディレクトリentry	uintptr
}

func (self *Pプロセス) Init(mem *mem.Tメモリ管理者) {
	self.Tスレッド一覧 = Linked一覧{}
	self.Threads = &self.Tスレッド一覧
	self.Threads.Init(mem)
}

type Pプロセスhelper struct {
	プロセス_2			Linked一覧
	mem			*mem.Tメモリ管理者
	中核ページディレクトリentry	uintptr
}

func (self *Pプロセスhelper) Init(mem *mem.Tメモリ管理者, 中核ページディレクトリentry uintptr) {
	self.mem = mem
	self.プロセス_2 = Linked一覧{}
	self.プロセス_2.Init(self.mem)
	self.中核ページディレクトリentry = 中核ページディレクトリentry
}

func (self *Pプロセスhelper) C作成(entrypoint func(), スレッドhelper *Tスレッドhelper, Pページディレクトリentry uint32, is中核 bool) Pプロセス {
	プロセス := (*Pプロセス)(self.mem.M記憶領域を確保(uint32(Sizeof(Pプロセス{}))))
	if プロセス == nil {
		return Pプロセス{}
	}
	プロセス.Init(self.mem)
	プロセス.id = Allocatepid()
	プロセス.Pページディレクトリentry = uintptr(Pページディレクトリentry)
	主要スレッド := スレッドhelper.C作成ポインタから関数(entrypoint, Pページディレクトリentry, is中核)
	if 主要スレッド != nil {
		主要スレッド.Pid = プロセス.id
		主要スレッド.Parentpid = 0
		プロセス.Threads.M末尾に追加(uintptr(Pointer(主要スレッド)))
	}

	self.プロセス_2.M末尾に追加(uintptr(Pointer(プロセス)))

	return *プロセス
}

func (self *Pプロセスhelper) Spawn(entrypoint func(), スレッドhelper *Tスレッドhelper, スケジューラ *Sスケジューラ, Pページディレクトリentry uint32, is中核 bool) Pプロセス {
	プロセス := self.C作成(entrypoint, スレッドhelper, Pページディレクトリentry, is中核)
	if プロセス.Threads != nil && プロセス.Threads.Sサイズ_2 > 0 {
		スレッド := (*Tスレッド)(プロセス.Threads.Getat(0))
		if スレッド != nil && スケジューラ != nil {
			スケジューラ.A追加スレッド(スレッド)
		}
	}
	return プロセス
}

func (self *Pプロセスhelper) 複製ページディレクトリ(転送元entry uintptr, 転送先entry uintptr) {
	転送元_2 := Getunsignedinteger32配列からポインタ(転送元entry, 1024, 1024)
	転送先_2 := Getunsignedinteger32配列からポインタ(転送先entry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		転送先_2[i] = 転送元_2[i]
	}
}
func (self *Pプロセスhelper) C作成からデータ() Pプロセス {
	プロセス := Pプロセス{}
	return プロセス
}
