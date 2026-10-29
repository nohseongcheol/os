/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "konsolë"
import . "multitasking"
import mem "memoriaManazhuesi"
import . "virtualMemoria"

const (
	Blocked		= 1
	Gati		= 2
	Undërpre	= 3
	Nisur		= 4
)

const ThreadstackMadhësia = 32 * 1024

type TThread struct {
	CpuGjendje			*TcpuGjendje
	Stack				uint32
	Përdoruesistack_2		uint32
	PërdoruesistackMadhësia_2	uint32
	Pid				uint32
	Prindpid			uint32

	FaqeDosjeentry	uint32

	ThreadGjendje	uint8
	BlockedGjendje	uint8

	oradelta	uint32

	Tlssegments	[Gdtentry]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (vetvetja *TThread) IRi() {
}

type TThreadhelper struct {
	mem *mem.TMemoriaManazhuesi
}

var konsolë_2 = TKonsolë{}

func (vetvetja *TThreadhelper) Init(mem *mem.TMemoriaManazhuesi) {
	vetvetja.mem = mem
	konsolë_2.MPrintoxy(([]byte)("thread:"), 1, 14)
}
func (vetvetja *TThreadhelper) CreatefromFunksion(entrypoint_2 func(), FaqeDosjeentry uint32, iskernel bool) TThread {
	result := TThread{}

	result.Stack = uint32(uintptr(vetvetja.mem.Malloc(ThreadstackMadhësia)))
	if result.Stack == 0 {
		return result
	}
	konsolë_2.MPrinto(([]byte)("[mem:"))
	konsolë_2.MUnsignedinteger32Printo(result.Stack)

	result.CpuGjendje = (*TcpuGjendje)(Pointer(uintptr(result.Stack) + ThreadstackMadhësia - Sizeof(TcpuGjendje{})))
	result.CpuGjendje.Esp = result.Stack + ThreadstackMadhësia
	result.CpuGjendje.Ebp = result.CpuGjendje.Esp
	result.CpuGjendje.Eip = uint32(ValueOf(entrypoint_2).Pointer())
	result.Përdoruesistack_2 = Përdoruesistack
	result.PërdoruesistackMadhësia_2 = PërdoruesistackMadhësia
	result.Pid = 0
	result.Prindpid = 0
	result.FaqeDosjeentry = FaqeDosjeentry
	konsolë_2.MPrinto((([]byte)("cpu")))

	konsolë_2.MUnsignedinteger32Printo(uint32(uintptr(Pointer(result.CpuGjendje))))

	konsolë_2.MPrinto((([]byte)(":")))
	konsolë_2.MUnsignedinteger32Printo(result.CpuGjendje.Eip)

	konsolë_2.MPrinto("]")
	if iskernel == true {
		result.CpuGjendje.Cs = Segkernelcode
		result.CpuGjendje.Ds = Segkerneldata
		result.CpuGjendje.Es = Segkerneldata
		result.CpuGjendje.Fs = Segkerneldata
		result.CpuGjendje.Gs = Segkernelgs
		result.CpuGjendje.Ss = Segkerneldata
		result.ThreadGjendje = Gati
		result.CpuGjendje.Eflags = 0x202
	} else {
		result.CpuGjendje.Cs = SegPërdoruesicode
		result.CpuGjendje.Ds = SegPërdoruesidata
		result.CpuGjendje.Es = SegPërdoruesidata
		result.CpuGjendje.Fs = SegPërdoruesidata
		result.CpuGjendje.Gs = SegPërdoruesigs
		result.CpuGjendje.Ss = SegPërdoruesidata
		result.ThreadGjendje = Nisur
		result.CpuGjendje.Eflags = 0x222
	}
	result.Iskernel = iskernel
	result.Fpuoffset = 0xffffffff

	return result
}

func (vetvetja *TThreadhelper) CreateKursorifromFunksion(entrypoint_2 func(), FaqeDosjeentry uint32, iskernel bool) *TThread {
	result := (*TThread)(vetvetja.mem.Malloc(uint32(Sizeof(TThread{}))))
	if result == nil {
		return nil
	}
	*result = vetvetja.CreatefromFunksion(entrypoint_2, FaqeDosjeentry, iskernel)
	if result.CpuGjendje == nil {
		vetvetja.mem.Elirë(Pointer(result))
		return nil
	}
	return result
}
