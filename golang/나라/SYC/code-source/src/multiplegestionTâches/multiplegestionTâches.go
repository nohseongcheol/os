package multiplegestionTâches

import . "unsafe"
import . "console"
import . "reflect"
import mem "mémoiregestionnaire"
import . "gdt"

var Tester uint8

func halt()

type TcpuÉtat struct {
	p1	uint32
	p2	uint32

	Eax	uint32
	Ebx	uint32
	Ecx	uint32
	Edx	uint32

	Esi	uint32
	Edi	uint32
	Ebp	uint32

	Gs	uint32
	Fs	uint32
	Es	uint32
	Ds	uint32

	Eip	uint32

	Cs	uint32
	Eflags	uint32

	Esp	uint32
	Ss	uint32
}

type TTâche struct {
	mémoire_de_pile		[4096]uint8
	processeurÉtat	*TcpuÉtat
}

func (self *TTâche) Init(gdt *TShareddescriptorTableau, mem *mem.TMémoiregestionnaire, élémentpoint_2 func()) {

	self.processeurÉtat = (*TcpuÉtat)(Pointer(uintptr(mem.Allouer_la_mémoire(1024*1024)) + 1024*1024 - Sizeof(TcpuÉtat{})))

	self.processeurÉtat.Eax = 0
	self.processeurÉtat.Ebx = 0
	self.processeurÉtat.Ecx = 0
	self.processeurÉtat.Edx = 0

	self.processeurÉtat.Esi = 0
	self.processeurÉtat.Edi = 0

	self.processeurÉtat.Gs = 0
	self.processeurÉtat.Fs = 0
	self.processeurÉtat.Es = 0
	self.processeurÉtat.Ds = 0

	self.processeurÉtat.Eip = uint32(ValueOf(élémentpoint_2).Pointer())
	self.processeurÉtat.Cs = Segnoyaucode
	self.processeurÉtat.Eflags = 0x202

	var stackaddress = uint32(uintptr(Pointer(self.processeurÉtat)))

	self.processeurÉtat.Esp = stackaddress
	self.processeurÉtat.Ebp = stackaddress
	self.processeurÉtat.Ss = 0

}

type TTâchegestionnaire struct {
}

var tâches [256]TTâche
var nombreTâches int
var courantetâche int

func (self *TTâchegestionnaire) Init() {
	nombreTâches = 0
	courantetâche = -1
}

func (self *TTâchegestionnaire) Ajoutertâche(tâche TTâche) bool {
	if nombreTâches >= 255 {
		return false
	}
	tâches[nombreTâches] = tâche
	nombreTâches++
	return true
}

func (self *TTâchegestionnaire) Schedule(processeurÉtat *TcpuÉtat) *TcpuÉtat {

	console_2 := TConsole{}
	for i := 0; i < nombreTâches; i++ {
		var x uint32 = (uint32)(uintptr(Pointer(tâches[i].processeurÉtat)))

		console_2.MUnsignedinteger32Imprimerxy(x, 10, uint16(15+i))
	}
	if nombreTâches <= 0 {
		return processeurÉtat
	}

	if courantetâche >= 0 {
		tâches[courantetâche].processeurÉtat = processeurÉtat
	}

	courantetâche++
	if courantetâche >= nombreTâches {
		courantetâche %= nombreTâches

	}

	return tâches[courantetâche].processeurÉtat
}
