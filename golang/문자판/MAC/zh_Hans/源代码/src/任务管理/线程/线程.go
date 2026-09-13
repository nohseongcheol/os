package T线程_2

import . "unsafe"
import . "reflect"
import . "gdt"
import . "控制台"
import . "多重任务管理"
import mem "内存管理器"
import . "虚拟内存"

const (
	Blocked	= 1
	R就绪	= 2
	S已停止	= 3
	S开始于	= 4
)

const T线程stack大小 = 32 * 1024

type T线程 struct {
	Cpu状态		*Tcpu状态
	Stack		uint32
	U用户stack_2	uint32
	U用户stack大小_2	uint32
	P进程号		uint32
	Parent进程号	uint32

	P页目录条目	uint32

	T线程状态		uint8
	Blocked状态	uint8

	时间三角州	uint32

	Tlssegments		[Gdt条目]TSegmentdescriptor
	Fpu位移		uintptr
	Fpubuffer	[512 + 16]byte
	Is内核		bool
}

func (self *T线程) N新建() {
}

type T线程helper struct {
	mem *mem.T内存管理器
}

var 控制台_2 = T控制台{}

func (self *T线程helper) Init(mem *mem.T内存管理器) {
	self.mem = mem
	控制台_2.M打印xy(([]byte)("thread:"), 1, 14)
}
func (self *T线程helper) C创建from函数(条目point_2 func(), P页目录条目 uint32, is内核 bool) T线程 {
	结果 := T线程{}

	结果.Stack = uint32(uintptr(self.mem.M分配内存(T线程stack大小)))
	if 结果.Stack == 0 {
		return 结果
	}
	控制台_2.M打印(([]byte)("[mem:"))
	控制台_2.MUnsignedinteger32打印(结果.Stack)

	结果.Cpu状态 = (*Tcpu状态)(Pointer(uintptr(结果.Stack) + T线程stack大小 - Sizeof(Tcpu状态{})))
	结果.Cpu状态.Esp = 结果.Stack + T线程stack大小
	结果.Cpu状态.Ebp = 结果.Cpu状态.Esp
	结果.Cpu状态.Eip = uint32(ValueOf(条目point_2).Pointer())
	结果.U用户stack_2 = U用户stack
	结果.U用户stack大小_2 = U用户stack大小
	结果.P进程号 = 0
	结果.Parent进程号 = 0
	结果.P页目录条目 = P页目录条目
	控制台_2.M打印((([]byte)("cpu")))

	控制台_2.MUnsignedinteger32打印(uint32(uintptr(Pointer(结果.Cpu状态))))

	控制台_2.M打印((([]byte)(":")))
	控制台_2.MUnsignedinteger32打印(结果.Cpu状态.Eip)

	控制台_2.M打印("]")
	if is内核 == true {
		结果.Cpu状态.Cs = Seg内核code
		结果.Cpu状态.Ds = Seg内核数据
		结果.Cpu状态.Es = Seg内核数据
		结果.Cpu状态.Fs = Seg内核数据
		结果.Cpu状态.Gs = Seg内核gs
		结果.Cpu状态.Ss = Seg内核数据
		结果.T线程状态 = R就绪
		结果.Cpu状态.Eflags = 0x202
	} else {
		结果.Cpu状态.Cs = Seg用户code
		结果.Cpu状态.Ds = Seg用户数据
		结果.Cpu状态.Es = Seg用户数据
		结果.Cpu状态.Fs = Seg用户数据
		结果.Cpu状态.Gs = Seg用户gs
		结果.Cpu状态.Ss = Seg用户数据
		结果.T线程状态 = S开始于
		结果.Cpu状态.Eflags = 0x222
	}
	结果.Is内核 = is内核
	结果.Fpu位移 = 0xffffffff

	return 结果
}

func (self *T线程helper) C创建指针from函数(条目point_2 func(), P页目录条目 uint32, is内核 bool) *T线程 {
	结果 := (*T线程)(self.mem.M分配内存(uint32(Sizeof(T线程{}))))
	if 结果 == nil {
		return nil
	}
	*结果 = self.C创建from函数(条目point_2, P页目录条目, is内核)
	if 结果.Cpu状态 == nil {
		self.mem.F空闲(Pointer(结果))
		return nil
	}
	return 结果
}
