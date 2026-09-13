package tiếntrình

import . "unsafe"
import . "util/liệtkê"
import mem "bộnhớmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcNgườidùngheapCỡ = 1 * 1024 * 1024

type Tiếntrình struct {
	mãsố			uint32
	syscallMãsố		int
	IsNgườidùngspace	bool
	đốisố			*[]byte

	Threadliệtkê	Linkedliệtkê
	Threads		*Linkedliệtkê
	TậptinTên	[]byte

	TrangThưmụcentry	uintptr
}

func (mình *Tiếntrình) Init(mem *mem.TBộnhớmanager) {
	mình.Threadliệtkê = Linkedliệtkê{}
	mình.Threads = &mình.Threadliệtkê
	mình.Threads.Init(mem)
}

type Tiếntrìnhhelper struct {
	tiếntrình_2		Linkedliệtkê
	mem			*mem.TBộnhớmanager
	kernelTrangThưmụcentry	uintptr
}

func (mình *Tiếntrìnhhelper) Init(mem *mem.TBộnhớmanager, kernelTrangThưmụcentry uintptr) {
	mình.mem = mem
	mình.tiếntrình_2 = Linkedliệtkê{}
	mình.tiếntrình_2.Init(mình.mem)
	mình.kernelTrangThưmụcentry = kernelTrangThưmụcentry
}

func (mình *Tiếntrìnhhelper) Create(entrypoint func(), threadhelper *TThreadhelper, TrangThưmụcentry uint32, iskernel bool) Tiếntrình {
	tiếntrình := (*Tiếntrình)(mình.mem.Cấp_phát_bộ_nhớ(uint32(Sizeof(Tiếntrình{}))))
	if tiếntrình == nil {
		return Tiếntrình{}
	}
	tiếntrình.Init(mình.mem)
	tiếntrình.mãsố = Allocatepid()
	tiếntrình.TrangThưmụcentry = uintptr(TrangThưmụcentry)
	chínhthread := threadhelper.CreateContrỏfromHàm(entrypoint, TrangThưmụcentry, iskernel)
	if chínhthread != nil {
		chínhthread.Pid = tiếntrình.mãsố
		chínhthread.Mẹpid = 0
		tiếntrình.Threads.Thêm_vào_cuối_danh_sách(uintptr(Pointer(chínhthread)))
	}

	mình.tiếntrình_2.Thêm_vào_cuối_danh_sách(uintptr(Pointer(tiếntrình)))

	return *tiếntrình
}

func (mình *Tiếntrìnhhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, TrangThưmụcentry uint32, iskernel bool) Tiếntrình {
	tiếntrình := mình.Create(entrypoint, threadhelper, TrangThưmụcentry, iskernel)
	if tiếntrình.Threads != nil && tiếntrình.Threads.Cỡ_2 > 0 {
		thread := (*TThread)(tiếntrình.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Thêmthread(thread)
		}
	}
	return tiếntrình
}

func (mình *Tiếntrìnhhelper) saochépTrangThưmục(mãnguồnentry uintptr, destinationentry uintptr) {
	mãnguồn_2 := Getunsignedinteger32MảngfromContrỏ(mãnguồnentry, 1024, 1024)
	destination_2 := Getunsignedinteger32MảngfromContrỏ(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = mãnguồn_2[i]
	}
}
func (mình *Tiếntrìnhhelper) Createfromdata() Tiếntrình {
	tiếntrình := Tiếntrình{}
	return tiếntrình
}
