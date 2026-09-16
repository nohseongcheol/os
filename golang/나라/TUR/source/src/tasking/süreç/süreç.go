/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package süreç

import . "unsafe"
import . "util/liste"
import mem "bellekmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcKullanıcıheapBoyut = 1 * 1024 * 1024

type Süreç struct {
	no			uint32
	syscallNo		int
	IsKullanıcıBoşluk	bool
	argümanlar		*[]byte

	ThreadListe	LinkedListe
	Threads		*LinkedListe
	Dosyaİsim	[]byte

	SayfaDizingirdi	uintptr
}

func (self *Süreç) Init(mem *mem.TBellekmanager) {
	self.ThreadListe = LinkedListe{}
	self.Threads = &self.ThreadListe
	self.Threads.Init(mem)
}

type Süreçhelper struct {
	süreçler		LinkedListe
	mem			*mem.TBellekmanager
	kernelSayfaDizingirdi	uintptr
}

func (self *Süreçhelper) Init(mem *mem.TBellekmanager, kernelSayfaDizingirdi uintptr) {
	self.mem = mem
	self.süreçler = LinkedListe{}
	self.süreçler.Init(self.mem)
	self.kernelSayfaDizingirdi = kernelSayfaDizingirdi
}

func (self *Süreçhelper) Create(girdipoint func(), threadhelper *TThreadhelper, SayfaDizingirdi uint32, iskernel bool) Süreç {
	süreç := (*Süreç)(self.mem.Bellek_ayır(uint32(Sizeof(Süreç{}))))
	if süreç == nil {
		return Süreç{}
	}
	süreç.Init(self.mem)
	süreç.no = Allocatepid()
	süreç.SayfaDizingirdi = uintptr(SayfaDizingirdi)
	anathread := threadhelper.CreateBelirteçfromFonksiyon(girdipoint, SayfaDizingirdi, iskernel)
	if anathread != nil {
		anathread.Pid = süreç.no
		anathread.Üstpid = 0
		süreç.Threads.Listenin_sonuna_ekle(uintptr(Pointer(anathread)))
	}

	self.süreçler.Listenin_sonuna_ekle(uintptr(Pointer(süreç)))

	return *süreç
}

func (self *Süreçhelper) Spawn(girdipoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, SayfaDizingirdi uint32, iskernel bool) Süreç {
	süreç := self.Create(girdipoint, threadhelper, SayfaDizingirdi, iskernel)
	if süreç.Threads != nil && süreç.Threads.Boyut_2 > 0 {
		thread := (*TThread)(süreç.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Eklethread(thread)
		}
	}
	return süreç
}

func (self *Süreçhelper) kopyalaSayfaDizin(kaynakgirdi uintptr, hedefgirdi uintptr) {
	kaynak_2 := Getunsignedinteger32DizifromBelirteç(kaynakgirdi, 1024, 1024)
	hedef_2 := Getunsignedinteger32DizifromBelirteç(hedefgirdi, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		hedef_2[i] = kaynak_2[i]
	}
}
func (self *Süreçhelper) Createfromdata() Süreç {
	süreç := Süreç{}
	return süreç
}
