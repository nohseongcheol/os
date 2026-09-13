package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "θύρα"
import . "util/λίστα"

import . "διακοπή"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "μνήμηmanager"

const SchedulerΣυχνότητα = 1
const KernelheapΈναρξη = 1024 * 1024
const schedulerΔιόρθωση = false
const pitΣυχνότητα = 100

var λίστα LinkedΛίστα

type Schedulerdata struct {
	συχνότητα	uint32
	tickcount	uint32

	switchforced	bool

	Ενεργό_2	bool

	τρέχονthread	*TThread
	tss		*Tssκαταχώρηση
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.συχνότητα = SchedulerΣυχνότητα
	schedata.τρέχονthread = nil
	schedata.Ενεργό_2 = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var τρέχονthreadΚατάλογος int = 0
var επόμενοΔιεργασίαΤΑΥΤΌΤΗΤΑ uint32 = 1

func Allocatepid() uint32 {
	pid := επόμενοΔιεργασίαΤΑΥΤΌΤΗΤΑ
	επόμενοΔιεργασίαΤΑΥΤΌΤΗΤΑ++
	return pid
}

func (self *Schedulerdata) GetΕπόμενοΈτοιμοthread() *TThread {
	if λίστα.Μέγεθος_2 <= 0 {
		return nil
	}

	if schedata.τρέχονthread != nil {
		τρέχονthreadΚατάλογος = λίστα.Κατάλογοςαπό(uintptr(Pointer(schedata.τρέχονthread)))
		if τρέχονthreadΚατάλογος < 0 {
			τρέχονthreadΚατάλογος = 0
		}
	} else {
		τρέχονthreadΚατάλογος = -1
	}

	for checked := 0; checked < λίστα.Μέγεθος_2; checked++ {
		τρέχονthreadΚατάλογος++
		if τρέχονthreadΚατάλογος >= λίστα.Μέγεθος_2 {
			τρέχονthreadΚατάλογος = 0
		}
		thread := (*TThread)(λίστα.Getat(τρέχονthreadΚατάλογος))
		if thread != nil && thread.ThreadΚατάσταση != Blocked && thread.ThreadΚατάσταση != Τερματισμός {
			if schedulerΔιόρθωση {
				console_2.MΕκτύπωση("ti:")
				console_2.MUnsignedinteger32Εκτύπωση(uint32(τρέχονthreadΚατάλογος))
				console_2.MΕκτύπωση(":")
				console_2.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.τρέχονthread

}
func (self *Scheduler) Προσθήκηthread(thread *TThread) {
	if thread == nil {
		return
	}
	λίστα.Append_to_list(uintptr(Pointer(thread)))
}
func Προσθήκηrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	λίστα.Append_to_list(uintptr(Pointer(thread)))
}

func Τρέχονpid() uint32 {
	if schedata.τρέχονthread == nil || schedata.τρέχονthread.Pid == 0 {
		return 1
	}
	return schedata.τρέχονthread.Pid
}

func Τρέχονγονικόpid() uint32 {
	if schedata.τρέχονthread == nil {
		return 0
	}
	return schedata.τρέχονthread.Γονικόpid
}
func (self *Scheduler) Αφαίρεσηthread(thread *TThread) {
	λίστα.Αφαίρεση(uintptr(Pointer(thread)))
}

func (self *Scheduler) Αφαίρεσηthreadat(κατάλογος int) {
	λίστα.Αφαίρεσηat(κατάλογος)
}

type Scheduler struct {
	TΔιακοπήhandler
}

func (self *Scheduler) Init(manager *TΔιακοπήmanager, mem *mem.TΜνήμηmanager, tss *Tssκαταχώρηση) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitΣυχνότητα)

	λίστα = LinkedΛίστα{}
	λίστα.Init(mem)
	console_2.MΕκτύπωση("list:")
	console_2.MUnsignedinteger32Εκτύπωση(uint32(uintptr(Pointer(&λίστα))))

	διακοπήhandler = χειρολαβήΔιακοπή
	var address uintptr
	address = uintptr(Pointer(&διακοπήhandler))
	self.TΔιακοπήhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Ενεργό_2(ενεργό bool) {
	schedata.Ενεργό_2 = ενεργό
}

func initpit(συχνότητα uint32) {
	if συχνότητα == 0 {
		return
	}
	divisor := uint32(1193180) / συχνότητα
	ΘύραΕγγραφήbyte(0x43, 0x36)
	ΘύραΕγγραφήbyte(0x40, uint8(divisor&0xFF))
	ΘύραΕγγραφήbyte(0x40, uint8((divisor>>8)&0xFF))
}

func σύνολοds(dssegment uint32)
func σύνολοgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func επαναφοράfpregs(buffer_2 uintptr)

var jmpΧρήστης uint32 = 0
var διακοπήhandler func(uint32) uint32

func schedulestack(fn func())
func σύνολοcr3(address uint32)
func getcr3() uint32

func χειρολαβήΔιακοπή(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerΔιόρθωση {
		console_2.MΕκτύπωσηxy(([]byte)("sche1:"), 1, 17)

		console_2.MΕκτύπωση(":")
		console_2.MUnsignedinteger32Εκτύπωση(esp)
		console_2.MΕκτύπωση(":")

		console_2.MUnsignedinteger32Εκτύπωση(uint32(schedata.tickcount))
		console_2.MΕκτύπωση(":")
		console_2.MUnsignedinteger32Εκτύπωση(KernelheapΈναρξη)
	}

	if schedata.tickcount == schedata.συχνότητα {
		schedata.tickcount = 0

		if λίστα.Μέγεθος_2 > 0 && schedata.Ενεργό_2 == true {
			var επόμενοthread = schedata.GetΕπόμενοΈτοιμοthread()
			if επόμενοthread == nil {
				return esp
			}
			if schedata.τρέχονthread == nil {
				MEmergencyΚαταγραφήΣυμβολοσειρά("\nSCHED first esp=")
				MEmergencyΚαταγραφήunsignedinteger32(esp)
				MEmergencyΚαταγραφήΣυμβολοσειρά(" thread=")
				MEmergencyΚαταγραφήunsignedinteger32(uint32(uintptr(Pointer(επόμενοthread))))
				MEmergencyΚαταγραφήΣυμβολοσειρά(" cpu=")
				MEmergencyΚαταγραφήunsignedinteger32(uint32(uintptr(Pointer(επόμενοthread.ΕπεξεργαστήςΚατάσταση))))
				MEmergencyΚαταγραφήΣυμβολοσειρά(" state=")
				MEmergencyΚαταγραφήunsignedinteger32(uint32(επόμενοthread.ThreadΚατάσταση))
				MEmergencyΚαταγραφήΣυμβολοσειρά(" eip=")
				MEmergencyΚαταγραφήunsignedinteger32(επόμενοthread.ΕπεξεργαστήςΚατάσταση.Eip)
				MEmergencyΚαταγραφήΣυμβολοσειρά(" cs=")
				MEmergencyΚαταγραφήunsignedinteger32(επόμενοthread.ΕπεξεργαστήςΚατάσταση.Cs)
				MEmergencyΚαταγραφήΣυμβολοσειρά("\n")
			}

			if esp >= KernelheapΈναρξη && schedata.τρέχονthread != nil {
				schedata.τρέχονthread.ΕπεξεργαστήςΚατάσταση = (*TcpuΚατάσταση)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.τρέχονthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.τρέχονthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerΔιόρθωση {
					console_2.MΕκτύπωση(([]byte)("backup"))
					console_2.MUnsignedinteger32Εκτύπωση(esp)
				}
			}

			address := uintptr(Pointer(&(επόμενοthread.Fpubuffer)))
			offset := επόμενοthread.Fpuoffset
			if offset != 0xffffffff {
				επαναφοράfpregs(address + offset)
				if schedulerΔιόρθωση {
					console_2.MΕκτύπωση(([]byte)("restore"))
				}
			}

			schedata.τρέχονthread = επόμενοthread

			if schedata.τρέχονthread.ThreadΚατάσταση == Ξεκίνησε {
				schedata.τρέχονthread.ThreadΚατάσταση = Έτοιμο

				InitialthreadΧρήστηςjump(schedata.τρέχονthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(επόμενοthread.ΕπεξεργαστήςΚατάσταση)))
			if επόμενοthread.Stack != 0 {
				schedata.tss.Σύνολοstack(Segkerneldata, επόμενοthread.Stack+ThreadstackΜέγεθος)
			}

			σύνολοcr3(επόμενοthread.ΣελίδαΚατάλογοςκαταχώρηση)
			σύνολοgs(επόμενοthread.ΕπεξεργαστήςΚατάσταση.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func ΑπενεργοποίησηΑκέραιος()

func getesp() uint32
func threadΈξοδοςloop()

func σύνολοthreadΈξοδοςloopΚατάσταση(επεξεργαστήςΚατάσταση *TcpuΚατάσταση) {
	επεξεργαστήςΚατάσταση.Eip = uint32(ValueOf(threadΈξοδοςloop).Pointer())
	επεξεργαστήςΚατάσταση.Cs = Segkernelcode
	επεξεργαστήςΚατάσταση.Ds = Segkerneldata
	επεξεργαστήςΚατάσταση.Es = Segkerneldata
	επεξεργαστήςΚατάσταση.Fs = Segkerneldata
	επεξεργαστήςΚατάσταση.Gs = Segkernelgs
	επεξεργαστήςΚατάσταση.Ss = Segkerneldata
	επεξεργαστήςΚατάσταση.Eflags = 0x202
}

func ΔιακοπήΤρέχονthread(επεξεργαστήςΚατάσταση *TcpuΚατάσταση) *TcpuΚατάσταση {
	if schedata.τρέχονthread == nil {
		σύνολοthreadΈξοδοςloopΚατάσταση(επεξεργαστήςΚατάσταση)
		return επεξεργαστήςΚατάσταση
	}

	τερματισμόςthread := schedata.τρέχονthread
	for i := 0; i < λίστα.Μέγεθος_2; i++ {
		thread := (*TThread)(λίστα.Getat(i))
		if thread != nil && thread.ΕπεξεργαστήςΚατάσταση == επεξεργαστήςΚατάσταση {
			τερματισμόςthread = thread
			break
		}
	}
	τερματισμόςthread.ΕπεξεργαστήςΚατάσταση = επεξεργαστήςΚατάσταση
	τερματισμόςthread.ThreadΚατάσταση = Τερματισμός
	schedata.τρέχονthread = τερματισμόςthread

	επόμενοthread := schedata.GetΕπόμενοΈτοιμοthread()
	if επόμενοthread == nil || επόμενοthread == τερματισμόςthread || επόμενοthread.ΕπεξεργαστήςΚατάσταση == nil || επόμενοthread.ΕπεξεργαστήςΚατάσταση == επεξεργαστήςΚατάσταση {
		σύνολοthreadΈξοδοςloopΚατάσταση(επεξεργαστήςΚατάσταση)
		return επεξεργαστήςΚατάσταση
	}

	schedata.τρέχονthread = επόμενοthread
	if επόμενοthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Σύνολοstack(Segkerneldata, επόμενοthread.Stack+ThreadstackΜέγεθος)
	}
	σύνολοcr3(επόμενοthread.ΣελίδαΚατάλογοςκαταχώρηση)
	σύνολοgs(επόμενοthread.ΕπεξεργαστήςΚατάσταση.Gs)
	return επόμενοthread.ΕπεξεργαστήςΚατάσταση
}

func InitialthreadΧρήστηςjump(thread *TThread) {

	ΑπενεργοποίησηΑκέραιος()

	schedata.tss.Σύνολοstack(Segkerneldata, thread.Stack+ThreadstackΜέγεθος)

	σύνολοcr3(thread.ΣελίδαΚατάλογοςκαταχώρηση)
	σύνολοgs(thread.ΕπεξεργαστήςΚατάσταση.Gs)

	schedata.τρέχονthread = thread
	schedata.Ενεργό_2 = true

	eip := thread.ΕπεξεργαστήςΚατάσταση.Eip
	χρήστηςesp := thread.Χρήστηςstack_2 + thread.ΧρήστηςstackΜέγεθος_2
	eflags := thread.ΕπεξεργαστήςΚατάσταση.Eflags
	cs := thread.ΕπεξεργαστήςΚατάσταση.Cs
	esp := schedata.tss.Getesp0()

	console_2.MΕκτύπωση(([]byte)("jump["))
	console_2.MUnsignedinteger32Εκτύπωση(eip)
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger32Εκτύπωση(χρήστηςesp)
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger32Εκτύπωση(eflags)
	console_2.MΕκτύπωση(([]byte)(":"))
	console_2.MUnsignedinteger32Εκτύπωση(cs)
	console_2.MΕκτύπωση(([]byte)(":"))

	console_2.MUnsignedinteger32Εκτύπωση(esp)
	console_2.MΕκτύπωση(([]byte)("]"))

	userprocκαταχώρηση := thread.ΕπεξεργαστήςΚατάσταση.Ecx
	καθολικάoffsetΠίνακας_2 := thread.ΕπεξεργαστήςΚατάσταση.Edx
	δυναμικό := thread.ΕπεξεργαστήςΚατάσταση.Esi

	ΘύραΕγγραφήbyte(0x20, 0x20)
	jumpusermodeiret(eip, χρήστηςesp, eflags, userprocκαταχώρηση, καθολικάoffsetΠίνακας_2, δυναμικό)
	console_2.MΕκτύπωση(([]byte)("usermode end"))
}
func εκτύπωσηesp(esp uint32) {
	console_2.MΕκτύπωση(([]byte)("esp["))
	console_2.MUnsignedinteger32Εκτύπωση(esp)
}
