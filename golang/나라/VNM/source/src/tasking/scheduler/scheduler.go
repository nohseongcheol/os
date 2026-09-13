package scheduler

import . "unsafe"
import . "reflect"

import . "console"
import . "gdt"
import . "cổng"
import . "util/liệtkê"

import . "giánđoạn"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "bộnhớmanager"

const SchedulerĐộthườngxuyên = 1
const KernelheapChạy = 1024 * 1024
const schedulerdebug = false
const pitĐộthườngxuyên = 100

var liệtkê Linkedliệtkê

type Schedulerdata struct {
	độthườngxuyên	uint32
	tickSốlượng	uint32

	switchforced	bool

	Bật_2	bool

	hiệnhànhthread	*TThread
	tss		*Tssentry
}

var schedata Schedulerdata = Schedulerdata{}

func (mình *Schedulerdata) Init() {
	schedata.tickSốlượng = 0
	schedata.độthườngxuyên = SchedulerĐộthườngxuyên
	schedata.hiệnhànhthread = nil
	schedata.Bật_2 = false
	schedata.switchforced = false

}

var console_2 = TConsole{}
var hiệnhànhthreadChỉmục int = 0
var kếTiếntrìnhMãsố uint32 = 1

func Allocatepid() uint32 {
	pid := kếTiếntrìnhMãsố
	kếTiếntrìnhMãsố++
	return pid
}

func (mình *Schedulerdata) GetKếSẵnsàngthread() *TThread {
	if liệtkê.Cỡ_2 <= 0 {
		return nil
	}

	if schedata.hiệnhànhthread != nil {
		hiệnhànhthreadChỉmục = liệtkê.Chỉmụctrên(uintptr(Pointer(schedata.hiệnhànhthread)))
		if hiệnhànhthreadChỉmục < 0 {
			hiệnhànhthreadChỉmục = 0
		}
	} else {
		hiệnhànhthreadChỉmục = -1
	}

	for checked := 0; checked < liệtkê.Cỡ_2; checked++ {
		hiệnhànhthreadChỉmục++
		if hiệnhànhthreadChỉmục >= liệtkê.Cỡ_2 {
			hiệnhànhthreadChỉmục = 0
		}
		thread := (*TThread)(liệtkê.Getat(hiệnhànhthreadChỉmục))
		if thread != nil && thread.ThreadTrạngthái != Blocked && thread.ThreadTrạngthái != Bịdừng {
			if schedulerdebug {
				console_2.MIn("ti:")
				console_2.MUnsignedinteger32In(uint32(hiệnhànhthreadChỉmục))
				console_2.MIn(":")
				console_2.MUnsignedinteger32In(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.hiệnhànhthread

}
func (mình *Scheduler) Thêmthread(thread *TThread) {
	if thread == nil {
		return
	}
	liệtkê.Thêm_vào_cuối_danh_sách(uintptr(Pointer(thread)))
}
func Thêmrunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	liệtkê.Thêm_vào_cuối_danh_sách(uintptr(Pointer(thread)))
}

func Hiệnhànhpid() uint32 {
	if schedata.hiệnhànhthread == nil || schedata.hiệnhànhthread.Pid == 0 {
		return 1
	}
	return schedata.hiệnhànhthread.Pid
}

func Hiệnhànhmẹpid() uint32 {
	if schedata.hiệnhànhthread == nil {
		return 0
	}
	return schedata.hiệnhànhthread.Mẹpid
}
func (mình *Scheduler) Bỏthread(thread *TThread) {
	liệtkê.Bỏ(uintptr(Pointer(thread)))
}

func (mình *Scheduler) Bỏthreadat(chỉmục int) {
	liệtkê.Bỏat(chỉmục)
}

type Scheduler struct {
	TGiánđoạnhandler
}

func (mình *Scheduler) Init(manager *TGiánđoạnmanager, mem *mem.TBộnhớmanager, tss *Tssentry) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitĐộthườngxuyên)

	liệtkê = Linkedliệtkê{}
	liệtkê.Init(mem)
	console_2.MIn("list:")
	console_2.MUnsignedinteger32In(uint32(uintptr(Pointer(&liệtkê))))

	giánđoạnhandler = handleGiánđoạn
	var address uintptr
	address = uintptr(Pointer(&giánđoạnhandler))
	mình.TGiánđoạnhandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (mình *Scheduler) Bật_2(bật bool) {
	schedata.Bật_2 = bật
}

func initpit(độthườngxuyên uint32) {
	if độthườngxuyên == 0 {
		return
	}
	divisor := uint32(1193180) / độthườngxuyên
	CổngGhibyte(0x43, 0x36)
	CổngGhibyte(0x40, uint8(divisor&0xFF))
	CổngGhibyte(0x40, uint8((divisor>>8)&0xFF))
}

func đặtds(dssegment uint32)
func đặtgs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func khôiphụcfpregs(buffer_2 uintptr)

var jmpNgườidùng uint32 = 0
var giánđoạnhandler func(uint32) uint32

func schedulestack(fn func())
func đặtcr3(address uint32)
func getcr3() uint32

func handleGiánđoạn(esp uint32) uint32 {

	schedata.tickSốlượng++

	if schedulerdebug {
		console_2.MInxy(([]byte)("sche1:"), 1, 17)

		console_2.MIn(":")
		console_2.MUnsignedinteger32In(esp)
		console_2.MIn(":")

		console_2.MUnsignedinteger32In(uint32(schedata.tickSốlượng))
		console_2.MIn(":")
		console_2.MUnsignedinteger32In(KernelheapChạy)
	}

	if schedata.tickSốlượng == schedata.độthườngxuyên {
		schedata.tickSốlượng = 0

		if liệtkê.Cỡ_2 > 0 && schedata.Bật_2 == true {
			var kếthread = schedata.GetKếSẵnsàngthread()
			if kếthread == nil {
				return esp
			}
			if schedata.hiệnhànhthread == nil {
				MEmergencylogCHUỖI("\nSCHED first esp=")
				MEmergencylogunsignedinteger32(esp)
				MEmergencylogCHUỖI(" thread=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(kếthread))))
				MEmergencylogCHUỖI(" cpu=")
				MEmergencylogunsignedinteger32(uint32(uintptr(Pointer(kếthread.CpuTrạngthái))))
				MEmergencylogCHUỖI(" state=")
				MEmergencylogunsignedinteger32(uint32(kếthread.ThreadTrạngthái))
				MEmergencylogCHUỖI(" eip=")
				MEmergencylogunsignedinteger32(kếthread.CpuTrạngthái.Eip)
				MEmergencylogCHUỖI(" cs=")
				MEmergencylogunsignedinteger32(kếthread.CpuTrạngthái.Cs)
				MEmergencylogCHUỖI("\n")
			}

			if esp >= KernelheapChạy && schedata.hiệnhànhthread != nil {
				schedata.hiệnhànhthread.CpuTrạngthái = (*TcpuTrạngthái)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.hiệnhànhthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.hiệnhànhthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerdebug {
					console_2.MIn(([]byte)("backup"))
					console_2.MUnsignedinteger32In(esp)
				}
			}

			address := uintptr(Pointer(&(kếthread.Fpubuffer)))
			offset := kếthread.Fpuoffset
			if offset != 0xffffffff {
				khôiphụcfpregs(address + offset)
				if schedulerdebug {
					console_2.MIn(([]byte)("restore"))
				}
			}

			schedata.hiệnhànhthread = kếthread

			if schedata.hiệnhànhthread.ThreadTrạngthái == Đãbắtđầu {
				schedata.hiệnhànhthread.ThreadTrạngthái = Sẵnsàng

				InitialthreadNgườidùngjump(schedata.hiệnhànhthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(kếthread.CpuTrạngthái)))
			if kếthread.Stack != 0 {
				schedata.tss.Đặtstack(Segkerneldata, kếthread.Stack+ThreadstackCỡ)
			}

			đặtcr3(kếthread.TrangThưmụcentry)
			đặtgs(kếthread.CpuTrạngthái.Gs)

		}

	}

	return esp
}

func jumpusermodeiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Vôhiệuhóaint()

func getesp() uint32
func threadThoátVònglặp()

func đặtthreadThoátVònglặpTrạngthái(cpuTrạngthái *TcpuTrạngthái) {
	cpuTrạngthái.Eip = uint32(ValueOf(threadThoátVònglặp).Pointer())
	cpuTrạngthái.Cs = Segkernelcode
	cpuTrạngthái.Ds = Segkerneldata
	cpuTrạngthái.Es = Segkerneldata
	cpuTrạngthái.Fs = Segkerneldata
	cpuTrạngthái.Gs = Segkernelgs
	cpuTrạngthái.Ss = Segkerneldata
	cpuTrạngthái.Eflags = 0x202
}

func DừngHiệnhànhthread(cpuTrạngthái *TcpuTrạngthái) *TcpuTrạngthái {
	if schedata.hiệnhànhthread == nil {
		đặtthreadThoátVònglặpTrạngthái(cpuTrạngthái)
		return cpuTrạngthái
	}

	bịdừngthread := schedata.hiệnhànhthread
	for i := 0; i < liệtkê.Cỡ_2; i++ {
		thread := (*TThread)(liệtkê.Getat(i))
		if thread != nil && thread.CpuTrạngthái == cpuTrạngthái {
			bịdừngthread = thread
			break
		}
	}
	bịdừngthread.CpuTrạngthái = cpuTrạngthái
	bịdừngthread.ThreadTrạngthái = Bịdừng
	schedata.hiệnhànhthread = bịdừngthread

	kếthread := schedata.GetKếSẵnsàngthread()
	if kếthread == nil || kếthread == bịdừngthread || kếthread.CpuTrạngthái == nil || kếthread.CpuTrạngthái == cpuTrạngthái {
		đặtthreadThoátVònglặpTrạngthái(cpuTrạngthái)
		return cpuTrạngthái
	}

	schedata.hiệnhànhthread = kếthread
	if kếthread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Đặtstack(Segkerneldata, kếthread.Stack+ThreadstackCỡ)
	}
	đặtcr3(kếthread.TrangThưmụcentry)
	đặtgs(kếthread.CpuTrạngthái.Gs)
	return kếthread.CpuTrạngthái
}

func InitialthreadNgườidùngjump(thread *TThread) {

	Vôhiệuhóaint()

	schedata.tss.Đặtstack(Segkerneldata, thread.Stack+ThreadstackCỡ)

	đặtcr3(thread.TrangThưmụcentry)
	đặtgs(thread.CpuTrạngthái.Gs)

	schedata.hiệnhànhthread = thread
	schedata.Bật_2 = true

	eip := thread.CpuTrạngthái.Eip
	ngườidùngesp := thread.Ngườidùngstack_2 + thread.NgườidùngstackCỡ_2
	eflags := thread.CpuTrạngthái.Eflags
	cs := thread.CpuTrạngthái.Cs
	esp := schedata.tss.Getesp0()

	console_2.MIn(([]byte)("jump["))
	console_2.MUnsignedinteger32In(eip)
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger32In(ngườidùngesp)
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger32In(eflags)
	console_2.MIn(([]byte)(":"))
	console_2.MUnsignedinteger32In(cs)
	console_2.MIn(([]byte)(":"))

	console_2.MUnsignedinteger32In(esp)
	console_2.MIn(([]byte)("]"))

	userprocentry := thread.CpuTrạngthái.Ecx
	toàncụcoffsetBảng_2 := thread.CpuTrạngthái.Edx
	năngđộng := thread.CpuTrạngthái.Esi

	CổngGhibyte(0x20, 0x20)
	jumpusermodeiret(eip, ngườidùngesp, eflags, userprocentry, toàncụcoffsetBảng_2, năngđộng)
	console_2.MIn(([]byte)("usermode end"))
}
func inesp(esp uint32) {
	console_2.MIn(([]byte)("esp["))
	console_2.MUnsignedinteger32In(esp)
}
