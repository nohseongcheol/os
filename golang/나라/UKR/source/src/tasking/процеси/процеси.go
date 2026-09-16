/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package процеси

import . "unsafe"
import . "util/перелік"
import mem "памятьmanager"
import . "tasking/thread"
import . "tasking/scheduler"
import . "util"

const ProcКористувачheapРозмір = 1 * 1024 * 1024

type Процеси struct {
	іДЕНТИФІКАТОР		uint32
	syscallІДЕНТИФІКАТОР	int
	IsКористувачПробіл	bool
	аргументи		*[]byte

	ThreadПерелік	LinkedПерелік
	Threads		*LinkedПерелік
	ФайлНазва	[]byte

	СторінкаТеказапис	uintptr
}

func (поточний *Процеси) Init(mem *mem.TПамятьmanager) {
	поточний.ThreadПерелік = LinkedПерелік{}
	поточний.Threads = &поточний.ThreadПерелік
	поточний.Threads.Init(mem)
}

type Процесиhelper struct {
	процеси_2		LinkedПерелік
	mem			*mem.TПамятьmanager
	kernelСторінкаТеказапис	uintptr
}

func (поточний *Процесиhelper) Init(mem *mem.TПамятьmanager, kernelСторінкаТеказапис uintptr) {
	поточний.mem = mem
	поточний.процеси_2 = LinkedПерелік{}
	поточний.процеси_2.Init(поточний.mem)
	поточний.kernelСторінкаТеказапис = kernelСторінкаТеказапис
}

func (поточний *Процесиhelper) Create(записpoint func(), threadhelper *TThreadhelper, СторінкаТеказапис uint32, iskernel bool) Процеси {
	процеси := (*Процеси)(поточний.mem.Виділити_памʼять(uint32(Sizeof(Процеси{}))))
	if процеси == nil {
		return Процеси{}
	}
	процеси.Init(поточний.mem)
	процеси.іДЕНТИФІКАТОР = AllocateІдентифікаторPID()
	процеси.СторінкаТеказапис = uintptr(СторінкаТеказапис)
	головнийthread := threadhelper.CreateВказівникзФункція(записpoint, СторінкаТеказапис, iskernel)
	if головнийthread != nil {
		головнийthread.ІдентифікаторPID = процеси.іДЕНТИФІКАТОР
		головнийthread.БатькоІдентифікаторPID = 0
		процеси.Threads.Додати_в_кінець_списку(uintptr(Pointer(головнийthread)))
	}

	поточний.процеси_2.Додати_в_кінець_списку(uintptr(Pointer(процеси)))

	return *процеси
}

func (поточний *Процесиhelper) Spawn(записpoint func(), threadhelper *TThreadhelper, scheduler *Scheduler, СторінкаТеказапис uint32, iskernel bool) Процеси {
	процеси := поточний.Create(записpoint, threadhelper, СторінкаТеказапис, iskernel)
	if процеси.Threads != nil && процеси.Threads.Розмір_2 > 0 {
		thread := (*TThread)(процеси.Threads.Getat(0))
		if thread != nil && scheduler != nil {
			scheduler.Додатиthread(thread)
		}
	}
	return процеси
}

func (поточний *Процесиhelper) копіюватиСторінкаТека(джерелозапис uintptr, призначеннязапис uintptr) {
	джерело_2 := Getunsignedinteger32МасивзВказівник(джерелозапис, 1024, 1024)
	призначення_2 := Getunsignedinteger32МасивзВказівник(призначеннязапис, 1024, 1024)

	for i := uint32(0); i < 1024; i++ {
		призначення_2[i] = джерело_2[i]
	}
}
func (поточний *Процесиhelper) Createзdata() Процеси {
	процеси := Процеси{}
	return процеси
}
