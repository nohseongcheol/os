/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package Thread

import . "unsafe"
import . "reflect"
import . "gdt"
import . "конзола"
import . "multitasking"
import mem "меморијаmanager"
import . "виртуелноМеморија"

const (
	Blocked		= 1
	Спреман		= 2
	Заустављен	= 3
	Покренут		= 4
)

const ThreadstackВеличина = 32 * 1024

type TThread struct {
	ПроцесорСтање		*TcpuСтање
	Stack			uint32
	Корисникstack_2		uint32
	КорисникstackВеличина_2	uint32
	ПИД			uint32
	НадређениПИД		uint32

	СТРАНАДиректоријумунос	uint32

	ThreadСтање	uint8
	BlockedСтање	uint8

	времеДелта	uint32

	Tlssegments	[Gdtунос]TSegmentdescriptor
	Fpuoffset	uintptr
	Fpubuffer	[512 + 16]byte
	Iskernel	bool
}

func (исти *TThread) Нова() {
}

type TThreadhelper struct {
	mem *mem.TМеморијаmanager
}

var конзола_2 = TКонзола{}

func (исти *TThreadhelper) Init(mem *mem.TМеморијаmanager) {
	исти.mem = mem
	конзола_2.MШтампајxy(([]byte)("thread:"), 1, 14)
}
func (исти *TThreadhelper) Createсафункција(уносpoint_2 func(), СТРАНАДиректоријумунос uint32, iskernel bool) TThread {
	иСХОД := TThread{}

	иСХОД.Stack = uint32(uintptr(исти.mem.Malloc(ThreadstackВеличина)))
	if иСХОД.Stack == 0 {
		return иСХОД
	}
	конзола_2.MШтампај(([]byte)("[mem:"))
	конзола_2.MUnsignedinteger32Штампај(иСХОД.Stack)

	иСХОД.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(иСХОД.Stack) + ThreadstackВеличина - Sizeof(TcpuСтање{})))
	иСХОД.ПроцесорСтање.Esp = иСХОД.Stack + ThreadstackВеличина
	иСХОД.ПроцесорСтање.Ebp = иСХОД.ПроцесорСтање.Esp
	иСХОД.ПроцесорСтање.Eip = uint32(ValueOf(уносpoint_2).Pointer())
	иСХОД.Корисникstack_2 = Корисникstack
	иСХОД.КорисникstackВеличина_2 = КорисникstackВеличина
	иСХОД.ПИД = 0
	иСХОД.НадређениПИД = 0
	иСХОД.СТРАНАДиректоријумунос = СТРАНАДиректоријумунос
	конзола_2.MШтампај((([]byte)("cpu")))

	конзола_2.MUnsignedinteger32Штампај(uint32(uintptr(Pointer(иСХОД.ПроцесорСтање))))

	конзола_2.MШтампај((([]byte)(":")))
	конзола_2.MUnsignedinteger32Штампај(иСХОД.ПроцесорСтање.Eip)

	конзола_2.MШтампај("]")
	if iskernel == true {
		иСХОД.ПроцесорСтање.Cs = Segkernelcode
		иСХОД.ПроцесорСтање.Ds = Segkerneldata
		иСХОД.ПроцесорСтање.Es = Segkerneldata
		иСХОД.ПроцесорСтање.Fs = Segkerneldata
		иСХОД.ПроцесорСтање.Gs = Segkernelgs
		иСХОД.ПроцесорСтање.Ss = Segkerneldata
		иСХОД.ThreadСтање = Спреман
		иСХОД.ПроцесорСтање.Eflags = 0x202
	} else {
		иСХОД.ПроцесорСтање.Cs = SegКорисникcode
		иСХОД.ПроцесорСтање.Ds = SegКорисникdata
		иСХОД.ПроцесорСтање.Es = SegКорисникdata
		иСХОД.ПроцесорСтање.Fs = SegКорисникdata
		иСХОД.ПроцесорСтање.Gs = SegКорисникgs
		иСХОД.ПроцесорСтање.Ss = SegКорисникdata
		иСХОД.ThreadСтање = Покренут
		иСХОД.ПроцесорСтање.Eflags = 0x222
	}
	иСХОД.Iskernel = iskernel
	иСХОД.Fpuoffset = 0xffffffff

	return иСХОД
}

func (исти *TThreadhelper) CreateПоказивачсафункција(уносpoint_2 func(), СТРАНАДиректоријумунос uint32, iskernel bool) *TThread {
	иСХОД := (*TThread)(исти.mem.Malloc(uint32(Sizeof(TThread{}))))
	if иСХОД == nil {
		return nil
	}
	*иСХОД = исти.Createсафункција(уносpoint_2, СТРАНАДиректоријумунос, iskernel)
	if иСХОД.ПроцесорСтање == nil {
		исти.mem.Слободно(Pointer(иСХОД))
		return nil
	}
	return иСХОД
}
