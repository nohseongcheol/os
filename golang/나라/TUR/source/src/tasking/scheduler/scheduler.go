/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package scheduler

import . "unsafe"
import . "reflect"

import . "konsol"
import . "gdt"
import . "bağlantıNoktası"
import . "util/liste"

import . "kesme"
import . "tasking/thread"
import . "tasking/tss"
import . "multitasking"
import mem "bellekmanager"

const SchedulerSıklık = 1
const KernelheapBaşlat = 1024 * 1024
const schedulerHataAyıkla = false
const pitSıklık = 100

var liste LinkedListe

type Schedulerdata struct {
	sıklık		uint32
	tickcount	uint32

	switchforced	bool

	Etkin	bool

	şuanthread	*TThread
	tss		*Tssgirdi
}

var schedata Schedulerdata = Schedulerdata{}

func (self *Schedulerdata) Init() {
	schedata.tickcount = 0
	schedata.sıklık = SchedulerSıklık
	schedata.şuanthread = nil
	schedata.Etkin = false
	schedata.switchforced = false

}

var konsol_2 = TKonsol{}
var şuanthreadİçindekiler int = 0
var sonrakiSüreçNo uint32 = 1

func Allocatepid() uint32 {
	pid := sonrakiSüreçNo
	sonrakiSüreçNo++
	return pid
}

func (self *Schedulerdata) GetSonrakiHazırthread() *TThread {
	if liste.Boyut_2 <= 0 {
		return nil
	}

	if schedata.şuanthread != nil {
		şuanthreadİçindekiler = liste.İçindekilerof(uintptr(Pointer(schedata.şuanthread)))
		if şuanthreadİçindekiler < 0 {
			şuanthreadİçindekiler = 0
		}
	} else {
		şuanthreadİçindekiler = -1
	}

	for checked := 0; checked < liste.Boyut_2; checked++ {
		şuanthreadİçindekiler++
		if şuanthreadİçindekiler >= liste.Boyut_2 {
			şuanthreadİçindekiler = 0
		}
		thread := (*TThread)(liste.Getat(şuanthreadİçindekiler))
		if thread != nil && thread.ThreadDurum != Blocked && thread.ThreadDurum != Durdurulmuş {
			if schedulerHataAyıkla {
				konsol_2.MYazdır("ti:")
				konsol_2.MUnsignedinteger32Yazdır(uint32(şuanthreadİçindekiler))
				konsol_2.MYazdır(":")
				konsol_2.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(thread))))
			}
			return thread
		}
	}
	return schedata.şuanthread

}
func (self *Scheduler) Eklethread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Listenin_sonuna_ekle(uintptr(Pointer(thread)))
}
func Eklerunnablethread(thread *TThread) {
	if thread == nil {
		return
	}
	liste.Listenin_sonuna_ekle(uintptr(Pointer(thread)))
}

func Şuanpid() uint32 {
	if schedata.şuanthread == nil || schedata.şuanthread.Pid == 0 {
		return 1
	}
	return schedata.şuanthread.Pid
}

func Şuanüstpid() uint32 {
	if schedata.şuanthread == nil {
		return 0
	}
	return schedata.şuanthread.Üstpid
}
func (self *Scheduler) Kaldırthread(thread *TThread) {
	liste.Kaldır(uintptr(Pointer(thread)))
}

func (self *Scheduler) Kaldırthreadat(içindekiler int) {
	liste.Kaldırat(içindekiler)
}

type Scheduler struct {
	TKesmehandler
}

func (self *Scheduler) Init(manager *TKesmemanager, mem *mem.TBellekmanager, tss *Tssgirdi) {
	schedata.Init()
	schedata.tss = tss
	initpit(pitSıklık)

	liste = LinkedListe{}
	liste.Init(mem)
	konsol_2.MYazdır("list:")
	konsol_2.MUnsignedinteger32Yazdır(uint32(uintptr(Pointer(&liste))))

	kesmehandler = handleKesme
	var address uintptr
	address = uintptr(Pointer(&kesmehandler))
	self.TKesmehandler.Init(0x20, uintptr(Pointer(manager)), address)
}

func (self *Scheduler) Etkin(etkin bool) {
	schedata.Etkin = etkin
}

func initpit(sıklık uint32) {
	if sıklık == 0 {
		return
	}
	divisor := uint32(1193180) / sıklık
	BağlantıNoktasıYazmabyte(0x43, 0x36)
	BağlantıNoktasıYazmabyte(0x40, uint8(divisor&0xFF))
	BağlantıNoktasıYazmabyte(0x40, uint8((divisor>>8)&0xFF))
}

func ayarlads(dssegment uint32)
func ayarlags(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func geriAlfpregs(buffer_2 uintptr)

var jmpKullanıcı uint32 = 0
var kesmehandler func(uint32) uint32

func schedulestack(fn func())
func ayarlacr3(address uint32)
func getcr3() uint32

func handleKesme(esp uint32) uint32 {

	schedata.tickcount++

	if schedulerHataAyıkla {
		konsol_2.MYazdırxy(([]byte)("sche1:"), 1, 17)

		konsol_2.MYazdır(":")
		konsol_2.MUnsignedinteger32Yazdır(esp)
		konsol_2.MYazdır(":")

		konsol_2.MUnsignedinteger32Yazdır(uint32(schedata.tickcount))
		konsol_2.MYazdır(":")
		konsol_2.MUnsignedinteger32Yazdır(KernelheapBaşlat)
	}

	if schedata.tickcount == schedata.sıklık {
		schedata.tickcount = 0

		if liste.Boyut_2 > 0 && schedata.Etkin == true {
			var sonrakithread = schedata.GetSonrakiHazırthread()
			if sonrakithread == nil {
				return esp
			}
			if schedata.şuanthread == nil {
				MEmergencyGünlükKatar("\nSCHED first esp=")
				MEmergencyGünlükunsignedinteger32(esp)
				MEmergencyGünlükKatar(" thread=")
				MEmergencyGünlükunsignedinteger32(uint32(uintptr(Pointer(sonrakithread))))
				MEmergencyGünlükKatar(" cpu=")
				MEmergencyGünlükunsignedinteger32(uint32(uintptr(Pointer(sonrakithread.MİBDurum))))
				MEmergencyGünlükKatar(" state=")
				MEmergencyGünlükunsignedinteger32(uint32(sonrakithread.ThreadDurum))
				MEmergencyGünlükKatar(" eip=")
				MEmergencyGünlükunsignedinteger32(sonrakithread.MİBDurum.Eip)
				MEmergencyGünlükKatar(" cs=")
				MEmergencyGünlükunsignedinteger32(sonrakithread.MİBDurum.Cs)
				MEmergencyGünlükKatar("\n")
			}

			if esp >= KernelheapBaşlat && schedata.şuanthread != nil {
				schedata.şuanthread.MİBDurum = (*TcpuDurum)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(schedata.şuanthread.Fpubuffer)))
				offset := (16 - (address % 16)) & 0xF
				schedata.şuanthread.Fpuoffset = offset
				backupfpregs(address + offset)
				if schedulerHataAyıkla {
					konsol_2.MYazdır(([]byte)("backup"))
					konsol_2.MUnsignedinteger32Yazdır(esp)
				}
			}

			address := uintptr(Pointer(&(sonrakithread.Fpubuffer)))
			offset := sonrakithread.Fpuoffset
			if offset != 0xffffffff {
				geriAlfpregs(address + offset)
				if schedulerHataAyıkla {
					konsol_2.MYazdır(([]byte)("restore"))
				}
			}

			schedata.şuanthread = sonrakithread

			if schedata.şuanthread.ThreadDurum == Başlamış {
				schedata.şuanthread.ThreadDurum = Hazır

				InitialthreadKullanıcıjump(schedata.şuanthread)
				return esp
			}

			esp = uint32(uintptr(Pointer(sonrakithread.MİBDurum)))
			if sonrakithread.Stack != 0 {
				schedata.tss.Ayarlastack(Segkerneldata, sonrakithread.Stack+ThreadstackBoyut)
			}

			ayarlacr3(sonrakithread.SayfaDizingirdi)
			ayarlags(sonrakithread.MİBDurum.Gs)

		}

	}

	return esp
}

func jumpKullanıcıModuiret(uint32, uint32, uint32, uint32, uint32, uint32)
func Kapatint()

func getesp() uint32
func threadÇıkloop()

func ayarlathreadÇıkloopDurum(mİBDurum *TcpuDurum) {
	mİBDurum.Eip = uint32(ValueOf(threadÇıkloop).Pointer())
	mİBDurum.Cs = Segkernelcode
	mİBDurum.Ds = Segkerneldata
	mİBDurum.Es = Segkerneldata
	mİBDurum.Fs = Segkerneldata
	mİBDurum.Gs = Segkernelgs
	mİBDurum.Ss = Segkerneldata
	mİBDurum.Eflags = 0x202
}

func DurdurŞuanthread(mİBDurum *TcpuDurum) *TcpuDurum {
	if schedata.şuanthread == nil {
		ayarlathreadÇıkloopDurum(mİBDurum)
		return mİBDurum
	}

	durdurulmuşthread := schedata.şuanthread
	for i := 0; i < liste.Boyut_2; i++ {
		thread := (*TThread)(liste.Getat(i))
		if thread != nil && thread.MİBDurum == mİBDurum {
			durdurulmuşthread = thread
			break
		}
	}
	durdurulmuşthread.MİBDurum = mİBDurum
	durdurulmuşthread.ThreadDurum = Durdurulmuş
	schedata.şuanthread = durdurulmuşthread

	sonrakithread := schedata.GetSonrakiHazırthread()
	if sonrakithread == nil || sonrakithread == durdurulmuşthread || sonrakithread.MİBDurum == nil || sonrakithread.MİBDurum == mİBDurum {
		ayarlathreadÇıkloopDurum(mİBDurum)
		return mİBDurum
	}

	schedata.şuanthread = sonrakithread
	if sonrakithread.Stack != 0 && schedata.tss != nil {
		schedata.tss.Ayarlastack(Segkerneldata, sonrakithread.Stack+ThreadstackBoyut)
	}
	ayarlacr3(sonrakithread.SayfaDizingirdi)
	ayarlags(sonrakithread.MİBDurum.Gs)
	return sonrakithread.MİBDurum
}

func InitialthreadKullanıcıjump(thread *TThread) {

	Kapatint()

	schedata.tss.Ayarlastack(Segkerneldata, thread.Stack+ThreadstackBoyut)

	ayarlacr3(thread.SayfaDizingirdi)
	ayarlags(thread.MİBDurum.Gs)

	schedata.şuanthread = thread
	schedata.Etkin = true

	eip := thread.MİBDurum.Eip
	kullanıcıesp := thread.Kullanıcıstack_2 + thread.KullanıcıstackBoyut_2
	eflags := thread.MİBDurum.Eflags
	cs := thread.MİBDurum.Cs
	esp := schedata.tss.Getesp0()

	konsol_2.MYazdır(([]byte)("jump["))
	konsol_2.MUnsignedinteger32Yazdır(eip)
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger32Yazdır(kullanıcıesp)
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger32Yazdır(eflags)
	konsol_2.MYazdır(([]byte)(":"))
	konsol_2.MUnsignedinteger32Yazdır(cs)
	konsol_2.MYazdır(([]byte)(":"))

	konsol_2.MUnsignedinteger32Yazdır(esp)
	konsol_2.MYazdır(([]byte)("]"))

	userprocgirdi := thread.MİBDurum.Ecx
	geneloffsetTablo_2 := thread.MİBDurum.Edx
	devingen := thread.MİBDurum.Esi

	BağlantıNoktasıYazmabyte(0x20, 0x20)
	jumpKullanıcıModuiret(eip, kullanıcıesp, eflags, userprocgirdi, geneloffsetTablo_2, devingen)
	konsol_2.MYazdır(([]byte)("usermode end"))
}
func yazdıresp(esp uint32) {
	konsol_2.MYazdır(([]byte)("esp["))
	konsol_2.MUnsignedinteger32Yazdır(esp)
}
