package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "port"
import . "util/list"

import . "interrupt"
import . "tasking/ନିଷ୍ପାଦନ_ଧାରା"
import . "tasking/tss"
import . "multitasking"
import mem "ସ୍ମୃତି"

const SCHEDULER_FREQUENCY = 1
const KERNEL_HEAP_START = 1024 * 1024
const schedulerDebug = false
const pitFrequency = 100

var list LinkedList

type SchedulerData struct {
	frequency	uint32
	tickCount	uint32

	switchForced	bool

	Enabled	bool

	currentThread	*Tନିଷ୍ପାଦନ_ଧାରା
	tss		*TSSEntry
}

var sche_data SchedulerData = SchedulerData{}

func (self *SchedulerData) Vଆରମ୍ଭ_କରିବା() {
	sche_data.tickCount = 0
	sche_data.frequency = SCHEDULER_FREQUENCY
	sche_data.currentThread = nil
	sche_data.Enabled = false
	sche_data.switchForced = false

}

var 콘솔 = T콘솔{}
var currentThreadIndex int = 0
var nextProcessID uint32 = 1

func AllocatePID() uint32 {
	pid := nextProcessID
	nextProcessID++
	return pid
}

func (self *SchedulerData) GetNextReadyThread() *Tନିଷ୍ପାଦନ_ଧାରା {
	if list.Vଆକାର <= 0 {
		return nil
	}

	if sche_data.currentThread != nil {
		currentThreadIndex = list.IndexOf(uintptr(Pointer(sche_data.currentThread)))
		if currentThreadIndex < 0 {
			currentThreadIndex = 0
		}
	} else {
		currentThreadIndex = -1
	}

	for checked := 0; checked < list.Vଆକାର; checked++ {
		currentThreadIndex++
		if currentThreadIndex >= list.Vଆକାର {
			currentThreadIndex = 0
		}
		thread := (*Tନିଷ୍ପାଦନ_ଧାରା)(list.GetAt(currentThreadIndex))
		if thread != nil && thread.ThreadState != Blocked && thread.ThreadState != Stopped {
			if schedulerDebug {
				콘솔.M출력("ti:")
				콘솔.MUint32출력(uint32(currentThreadIndex))
				콘솔.M출력(":")
				콘솔.MUint32출력(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return sche_data.currentThread

}
func (self *Scheduler) AddThread(thread *Tନିଷ୍ପାଦନ_ଧାରା) {
	if thread == nil {
		return
	}
	list.PushBack(uintptr(Pointer(thread)))
}
func AddRunnableThread(thread *Tନିଷ୍ପାଦନ_ଧାରା) {
	if thread == nil {
		return
	}
	list.PushBack(uintptr(Pointer(thread)))
}

func CurrentPID() uint32 {
	if sche_data.currentThread == nil || sche_data.currentThread.Pid == 0 {
		return 1
	}
	return sche_data.currentThread.Pid
}

func CurrentParentPID() uint32 {
	if sche_data.currentThread == nil {
		return 0
	}
	return sche_data.currentThread.ParentPid
}
func (self *Scheduler) RemoveThread(thread *Tନିଷ୍ପାଦନ_ଧାରା) {
	list.Remove(uintptr(Pointer(thread)))
}

func (self *Scheduler) RemoveThreadAt(index int) {
	list.RemoveAt(index)
}

type Scheduler struct {
	TInterruptHandler
}

func (self *Scheduler) Vଆରମ୍ଭ_କରିବା(manager *TInterruptManager, mem *mem.TMemoryManager, tss *TSSEntry) {
	sche_data.Vଆରମ୍ଭ_କରିବା()
	sche_data.tss = tss
	initPIT(pitFrequency)

	list = LinkedList{}
	list.Vଆରମ୍ଭ_କରିବା(mem)
	콘솔.M출력("list:")
	콘솔.MUint32출력(uint32(uintptr(Pointer(&list))))

	interruptHandler = handleInterrupt
	var addr uintptr
	addr = uintptr(Pointer(&interruptHandler))
	self.TInterruptHandler.Vଆରମ୍ଭ_କରିବା(0x20, uintptr(Pointer(manager)), addr)
}

func (self *Scheduler) Enabled(enabled bool) {
	sche_data.Enabled = enabled
}

func initPIT(frequency uint32) {
	if frequency == 0 {
		return
	}
	divisor := uint32(1193180) / frequency
	PortWriteByte(0x43, 0x36)
	PortWriteByte(0x40, uint8(divisor&0xFF))
	PortWriteByte(0x40, uint8((divisor>>8)&0xFF))
}

func setDS(ds_segment uint32)
func setGS(gs_segment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupFpRegs(buffer uintptr)
func restoreFpRegs(buffer uintptr)

var jmp_user uint32 = 0
var interruptHandler func(uint32) uint32

func scheduleStack(fn func())
func setCR3(addr uint32)
func getCR3() uint32

func handleInterrupt(esp uint32) uint32 {

	sche_data.tickCount++

	if schedulerDebug {
		콘솔.M출력XY(([]byte)("sche1:"), 1, 17)

		콘솔.M출력(":")
		콘솔.MUint32출력(esp)
		콘솔.M출력(":")

		콘솔.MUint32출력(uint32(sche_data.tickCount))
		콘솔.M출력(":")
		콘솔.MUint32출력(KERNEL_HEAP_START)
	}

	if sche_data.tickCount == sche_data.frequency {
		sche_data.tickCount = 0

		if list.Vଆକାର > 0 && sche_data.Enabled == true {
			var nextThread = sche_data.GetNextReadyThread()
			if nextThread == nil {
				return esp
			}
			if sche_data.currentThread == nil {
				M긴급로그문자열("\nSCHED first esp=")
				M긴급로그Uint32(esp)
				M긴급로그문자열(" thread=")
				M긴급로그Uint32(uint32(uintptr(Pointer(nextThread))))
				M긴급로그문자열(" cpu=")
				M긴급로그Uint32(uint32(uintptr(Pointer(nextThread.CpuState))))
				M긴급로그문자열(" state=")
				M긴급로그Uint32(uint32(nextThread.ThreadState))
				M긴급로그문자열(" eip=")
				M긴급로그Uint32(nextThread.CpuState.Eip)
				M긴급로그문자열(" cs=")
				M긴급로그Uint32(nextThread.CpuState.Cs)
				M긴급로그문자열("\n")
			}

			if esp >= KERNEL_HEAP_START && sche_data.currentThread != nil {
				sche_data.currentThread.CpuState = (*TCPUState)(Pointer(uintptr(esp)))

				addr := uintptr(Pointer(&(sche_data.currentThread.FPUBuffer)))
				offset := (16 - (addr % 16)) & 0xF
				sche_data.currentThread.FPUOffset = offset
				backupFpRegs(addr + offset)
				if schedulerDebug {
					콘솔.M출력(([]byte)("backup"))
					콘솔.MUint32출력(esp)
				}
			}

			addr := uintptr(Pointer(&(nextThread.FPUBuffer)))
			offset := nextThread.FPUOffset
			if offset != 0xffffffff {
				restoreFpRegs(addr + offset)
				if schedulerDebug {
					콘솔.M출력(([]byte)("restore"))
				}
			}

			sche_data.currentThread = nextThread

			if sche_data.currentThread.ThreadState == Started {
				sche_data.currentThread.ThreadState = Ready

				InitialThreadUserJump(sche_data.currentThread)
				return esp
			}

			esp = uint32(uintptr(Pointer(nextThread.CpuState)))
			if nextThread.Stack != 0 {
				sche_data.tss.SetStack(SEG_KERNEL_DATA, nextThread.Stack+THREAD_STACK_SIZE)
			}

			setCR3(nextThread.PageDirEntry)
			setGS(nextThread.CpuState.Gs)

		}

	}

	return esp
}

func jump_usermode_iret(uint32, uint32, uint32, uint32, uint32, uint32)
func DisableInt()

func getESP() uint32
func threadExitLoop()

func setThreadExitLoopState(cpustate *TCPUState) {
	cpustate.Eip = uint32(ValueOf(threadExitLoop).Pointer())
	cpustate.Cs = SEG_KERNEL_CODE
	cpustate.Ds = SEG_KERNEL_DATA
	cpustate.Es = SEG_KERNEL_DATA
	cpustate.Fs = SEG_KERNEL_DATA
	cpustate.Gs = SEG_KERNEL_GS
	cpustate.Ss = SEG_KERNEL_DATA
	cpustate.Eflags = 0x202
}

func StopCurrentThread(cpustate *TCPUState) *TCPUState {
	if sche_data.currentThread == nil {
		setThreadExitLoopState(cpustate)
		return cpustate
	}

	stoppedThread := sche_data.currentThread
	for i := 0; i < list.Vଆକାର; i++ {
		thread := (*Tନିଷ୍ପାଦନ_ଧାରା)(list.GetAt(i))
		if thread != nil && thread.CpuState == cpustate {
			stoppedThread = thread
			break
		}
	}
	stoppedThread.CpuState = cpustate
	stoppedThread.ThreadState = Stopped
	sche_data.currentThread = stoppedThread

	nextThread := sche_data.GetNextReadyThread()
	if nextThread == nil || nextThread == stoppedThread || nextThread.CpuState == nil || nextThread.CpuState == cpustate {
		setThreadExitLoopState(cpustate)
		return cpustate
	}

	sche_data.currentThread = nextThread
	if nextThread.Stack != 0 && sche_data.tss != nil {
		sche_data.tss.SetStack(SEG_KERNEL_DATA, nextThread.Stack+THREAD_STACK_SIZE)
	}
	setCR3(nextThread.PageDirEntry)
	setGS(nextThread.CpuState.Gs)
	return nextThread.CpuState
}

func InitialThreadUserJump(thread *Tନିଷ୍ପାଦନ_ଧାରା) {

	DisableInt()

	sche_data.tss.SetStack(SEG_KERNEL_DATA, thread.Stack+THREAD_STACK_SIZE)

	setCR3(thread.PageDirEntry)
	setGS(thread.CpuState.Gs)

	sche_data.currentThread = thread
	sche_data.Enabled = true

	eip := thread.CpuState.Eip
	user_esp := thread.UserStack + thread.UserStackSize
	eflags := thread.CpuState.Eflags
	cs := thread.CpuState.Cs
	esp := sche_data.tss.GetESP0()

	콘솔.M출력(([]byte)("jump["))
	콘솔.MUint32출력(eip)
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint32출력(user_esp)
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint32출력(eflags)
	콘솔.M출력(([]byte)(":"))
	콘솔.MUint32출력(cs)
	콘솔.M출력(([]byte)(":"))

	콘솔.MUint32출력(esp)
	콘솔.M출력(([]byte)("]"))

	userproc_entry := thread.CpuState.Ecx
	global_offset_table := thread.CpuState.Edx
	dynamic := thread.CpuState.Esi

	PortWriteByte(0x20, 0x20)
	jump_usermode_iret(eip, user_esp, eflags, userproc_entry, global_offset_table, dynamic)
	콘솔.M출력(([]byte)("usermode end"))
}
func printESP(esp uint32) {
	콘솔.M출력(([]byte)("esp["))
	콘솔.MUint32출력(esp)
}
