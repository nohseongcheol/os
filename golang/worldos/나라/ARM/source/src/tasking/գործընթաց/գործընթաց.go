/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package գործընթաց

import . "unsafe"
import . "util/ցուցակ"
import mem "հիշողությունmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcՕգտագործողheapՉափս = 1 * 1024 * 1024

type Գործընթաց struct {
	id			uint32
	syscallid		int
	IsՕգտագործողԲացատ	bool
	arguments		*[]byte

	ThreadՑուցակ	LinkedՑուցակ
	Threads		*LinkedՑուցակ
	ՖայլԱնուն	[]byte

	Էջֆայլապանակentry	uintptr
}

func (ինքնուրույն *Գործընթաց) Init(mem *mem.TՀիշողությունmanager) {
	ինքնուրույն.ThreadՑուցակ = LinkedՑուցակ{}
	ինքնուրույն.Threads = &ինքնուրույն.ThreadՑուցակ
	ինքնուրույն.Threads.Init(mem)
}

type Գործընթացhelper struct {
	գործընթացներ		LinkedՑուցակ
	mem			*mem.TՀիշողությունmanager
	kernelԷջֆայլապանակentry	uintptr
}

func (ինքնուրույն *Գործընթացhelper) Init(mem *mem.TՀիշողությունmanager, kernelԷջֆայլապանակentry uintptr) {
	ինքնուրույն.mem = mem
	ինքնուրույն.գործընթացներ = LinkedՑուցակ{}
	ինքնուրույն.գործընթացներ.Init(ինքնուրույն.mem)
	ինքնուրույն.kernelԷջֆայլապանակentry = kernelԷջֆայլապանակentry
}

func (ինքնուրույն *Գործընթացhelper) Create(entrypoint func(), threadhelper *TThreadhelper, Էջֆայլապանակentry uint32, iskernel bool) Գործընթաց {
	գործընթաց := (*Գործընթաց)(ինքնուրույն.mem.Malloc(uint32(Sizeof(Գործընթաց{}))))
	if գործընթաց == nil {
		return Գործընթաց{}
	}
	գործընթաց.Init(ինքնուրույն.mem)
	գործընթաց.id = Allocatepid()
	գործընթաց.Էջֆայլապանակentry = uintptr(Էջֆայլապանակentry)
	գլխավորthread := threadhelper.CreateՑուցիչիցfunction(entrypoint, Էջֆայլապանակentry, iskernel)
	if գլխավորthread != nil {
		գլխավորthread.Pid = գործընթաց.id
		գլխավորthread.Ծնողpid = 0
		գործընթաց.Threads.Append_to_list(uintptr(Pointer(գլխավորthread)))
	}

	ինքնուրույն.գործընթացներ.Append_to_list(uintptr(Pointer(գործընթաց)))

	return *գործընթաց
}

func (ինքնուրույն *Գործընթացhelper) Spawn(entrypoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, Էջֆայլապանակentry uint32, iskernel bool) Գործընթաց {
	գործընթաց := ինքնուրույն.Create(entrypoint, threadhelper, Էջֆայլապանակentry, iskernel)
	if գործընթաց.Threads != nil && գործընթաց.Threads.Չափս_2 > 0 {
		thread := (*TThread)(գործընթաց.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Ավելացնելthread(thread)
		}
	}
	return գործընթաց
}

func (ինքնուրույն *Գործընթացhelper) պատճենելԷջֆայլապանակ(աղբյուրentry uintptr, destinationentry uintptr) {
	աղբյուր_2 := Getunsignedinteger32ԶանգվածիցՑուցիչ(աղբյուրentry, 1024, 1024)
	destination_2 := Getunsignedinteger32ԶանգվածիցՑուցիչ(destinationentry, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		destination_2[i] = աղբյուր_2[i]
	}
}
func (ինքնուրույն *Գործընթացhelper) Createիցdata() Գործընթաց {
	գործընթաց := Գործընթաց{}
	return գործընթաց
}
