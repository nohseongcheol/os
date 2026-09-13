package 调度器

import . "unsafe"
import . "reflect"

import . "控制台"
import . "gdt"
import . "端口"
import . "工具/列表"

import . "中断"
import . "任务管理/线程"
import . "任务管理/tss"
import . "多重任务管理"
import mem "内存管理器"

const S调度器频率 = 1
const K内核heap开始 = 1024 * 1024
const 调度器调试 = false
const pit频率 = 100

var 列表 Linked列表

type S调度器数据 struct {
	频率	uint32
	tick计数	uint32

	switchforced	bool

	E启用	bool

	当前线程	*T线程
	tss	*Tss条目
}

var sche数据 S调度器数据 = S调度器数据{}

func (self *S调度器数据) Init() {
	sche数据.tick计数 = 0
	sche数据.频率 = S调度器频率
	sche数据.当前线程 = nil
	sche数据.E启用 = false
	sche数据.switchforced = false

}

var 控制台_2 = T控制台{}
var 当前线程索引 int = 0
var 下一个进程id uint32 = 1

func Allocate进程号() uint32 {
	进程号 := 下一个进程id
	下一个进程id++
	return 进程号
}

func (self *S调度器数据) Get下一个就绪线程() *T线程 {
	if 列表.S大小_2 <= 0 {
		return nil
	}

	if sche数据.当前线程 != nil {
		当前线程索引 = 列表.I索引of(uintptr(Pointer(sche数据.当前线程)))
		if 当前线程索引 < 0 {
			当前线程索引 = 0
		}
	} else {
		当前线程索引 = -1
	}

	for checked := 0; checked < 列表.S大小_2; checked++ {
		当前线程索引++
		if 当前线程索引 >= 列表.S大小_2 {
			当前线程索引 = 0
		}
		线程 := (*T线程)(列表.Getat(当前线程索引))
		if 线程 != nil && 线程.T线程状态 != Blocked && 线程.T线程状态 != S已停止 {
			if 调度器调试 {
				控制台_2.M打印("ti:")
				控制台_2.MUnsignedinteger32打印(uint32(当前线程索引))
				控制台_2.M打印(":")
				控制台_2.MUnsignedinteger32打印(uint32(uintptr(Pointer(线程))))
			}
			return 线程
		}
	}
	return sche数据.当前线程

}
func (self *S调度器) A添加线程(线程 *T线程) {
	if 线程 == nil {
		return
	}
	列表.M追加到表尾(uintptr(Pointer(线程)))
}
func A添加runnable线程(线程 *T线程) {
	if 线程 == nil {
		return
	}
	列表.M追加到表尾(uintptr(Pointer(线程)))
}

func C当前进程号() uint32 {
	if sche数据.当前线程 == nil || sche数据.当前线程.P进程号 == 0 {
		return 1
	}
	return sche数据.当前线程.P进程号
}

func C当前parent进程号() uint32 {
	if sche数据.当前线程 == nil {
		return 0
	}
	return sche数据.当前线程.Parent进程号
}
func (self *S调度器) R删除线程(线程 *T线程) {
	列表.R删除(uintptr(Pointer(线程)))
}

func (self *S调度器) R删除线程at(索引 int) {
	列表.R删除at(索引)
}

type S调度器 struct {
	T中断handler
}

func (self *S调度器) Init(管理器 *T中断管理器, mem *mem.T内存管理器, tss *Tss条目) {
	sche数据.Init()
	sche数据.tss = tss
	initpit(pit频率)

	列表 = Linked列表{}
	列表.Init(mem)
	控制台_2.M打印("list:")
	控制台_2.MUnsignedinteger32打印(uint32(uintptr(Pointer(&列表))))

	中断handler = 控制器中断
	var address uintptr
	address = uintptr(Pointer(&中断handler))
	self.T中断handler.Init(0x20, uintptr(Pointer(管理器)), address)
}

func (self *S调度器) E启用(启用 bool) {
	sche数据.E启用 = 启用
}

func initpit(频率 uint32) {
	if 频率 == 0 {
		return
	}
	divisor := uint32(1193180) / 频率
	P端口写入字节(0x43, 0x36)
	P端口写入字节(0x40, uint8(divisor&0xFF))
	P端口写入字节(0x40, uint8((divisor>>8)&0xFF))
}

func 集合ds(dssegment uint32)
func 集合gs(gssegment uint32)

func fxsave(uint32)
func fxrstor(uint32)

func backupfpregs(buffer_2 uintptr)
func 恢复fpregs(buffer_2 uintptr)

var jmp用户 uint32 = 0
var 中断handler func(uint32) uint32

func schedulestack(fn func())
func 集合cr3(address uint32)
func getcr3() uint32

func 控制器中断(esp uint32) uint32 {

	sche数据.tick计数++

	if 调度器调试 {
		控制台_2.M打印xy(([]byte)("sche1:"), 1, 17)

		控制台_2.M打印(":")
		控制台_2.MUnsignedinteger32打印(esp)
		控制台_2.M打印(":")

		控制台_2.MUnsignedinteger32打印(uint32(sche数据.tick计数))
		控制台_2.M打印(":")
		控制台_2.MUnsignedinteger32打印(K内核heap开始)
	}

	if sche数据.tick计数 == sche数据.频率 {
		sche数据.tick计数 = 0

		if 列表.S大小_2 > 0 && sche数据.E启用 == true {
			var 下一个线程 = sche数据.Get下一个就绪线程()
			if 下一个线程 == nil {
				return esp
			}
			if sche数据.当前线程 == nil {
				MEmergency日志字符串("\nSCHED first esp=")
				MEmergency日志unsignedinteger32(esp)
				MEmergency日志字符串(" thread=")
				MEmergency日志unsignedinteger32(uint32(uintptr(Pointer(下一个线程))))
				MEmergency日志字符串(" cpu=")
				MEmergency日志unsignedinteger32(uint32(uintptr(Pointer(下一个线程.Cpu状态))))
				MEmergency日志字符串(" state=")
				MEmergency日志unsignedinteger32(uint32(下一个线程.T线程状态))
				MEmergency日志字符串(" eip=")
				MEmergency日志unsignedinteger32(下一个线程.Cpu状态.Eip)
				MEmergency日志字符串(" cs=")
				MEmergency日志unsignedinteger32(下一个线程.Cpu状态.Cs)
				MEmergency日志字符串("\n")
			}

			if esp >= K内核heap开始 && sche数据.当前线程 != nil {
				sche数据.当前线程.Cpu状态 = (*Tcpu状态)(Pointer(uintptr(esp)))

				address := uintptr(Pointer(&(sche数据.当前线程.Fpubuffer)))
				位移 := (16 - (address % 16)) & 0xF
				sche数据.当前线程.Fpu位移 = 位移
				backupfpregs(address + 位移)
				if 调度器调试 {
					控制台_2.M打印(([]byte)("backup"))
					控制台_2.MUnsignedinteger32打印(esp)
				}
			}

			address := uintptr(Pointer(&(下一个线程.Fpubuffer)))
			位移 := 下一个线程.Fpu位移
			if 位移 != 0xffffffff {
				恢复fpregs(address + 位移)
				if 调度器调试 {
					控制台_2.M打印(([]byte)("restore"))
				}
			}

			sche数据.当前线程 = 下一个线程

			if sche数据.当前线程.T线程状态 == S开始于 {
				sche数据.当前线程.T线程状态 = R就绪

				Initial线程用户jump(sche数据.当前线程)
				return esp
			}

			esp = uint32(uintptr(Pointer(下一个线程.Cpu状态)))
			if 下一个线程.Stack != 0 {
				sche数据.tss.S集合stack(Seg内核数据, 下一个线程.Stack+T线程stack大小)
			}

			集合cr3(下一个线程.P页目录条目)
			集合gs(下一个线程.Cpu状态.Gs)

		}

	}

	return esp
}

func jump用户模式iret(uint32, uint32, uint32, uint32, uint32, uint32)
func D禁用整型()

func getesp() uint32
func 线程退出loop()

func 集合线程退出loop状态(cpu状态 *Tcpu状态) {
	cpu状态.Eip = uint32(ValueOf(线程退出loop).Pointer())
	cpu状态.Cs = Seg内核code
	cpu状态.Ds = Seg内核数据
	cpu状态.Es = Seg内核数据
	cpu状态.Fs = Seg内核数据
	cpu状态.Gs = Seg内核gs
	cpu状态.Ss = Seg内核数据
	cpu状态.Eflags = 0x202
}

func S停止当前线程(cpu状态 *Tcpu状态) *Tcpu状态 {
	if sche数据.当前线程 == nil {
		集合线程退出loop状态(cpu状态)
		return cpu状态
	}

	已停止线程 := sche数据.当前线程
	for i := 0; i < 列表.S大小_2; i++ {
		线程 := (*T线程)(列表.Getat(i))
		if 线程 != nil && 线程.Cpu状态 == cpu状态 {
			已停止线程 = 线程
			break
		}
	}
	已停止线程.Cpu状态 = cpu状态
	已停止线程.T线程状态 = S已停止
	sche数据.当前线程 = 已停止线程

	下一个线程 := sche数据.Get下一个就绪线程()
	if 下一个线程 == nil || 下一个线程 == 已停止线程 || 下一个线程.Cpu状态 == nil || 下一个线程.Cpu状态 == cpu状态 {
		集合线程退出loop状态(cpu状态)
		return cpu状态
	}

	sche数据.当前线程 = 下一个线程
	if 下一个线程.Stack != 0 && sche数据.tss != nil {
		sche数据.tss.S集合stack(Seg内核数据, 下一个线程.Stack+T线程stack大小)
	}
	集合cr3(下一个线程.P页目录条目)
	集合gs(下一个线程.Cpu状态.Gs)
	return 下一个线程.Cpu状态
}

func Initial线程用户jump(线程 *T线程) {

	D禁用整型()

	sche数据.tss.S集合stack(Seg内核数据, 线程.Stack+T线程stack大小)

	集合cr3(线程.P页目录条目)
	集合gs(线程.Cpu状态.Gs)

	sche数据.当前线程 = 线程
	sche数据.E启用 = true

	eip := 线程.Cpu状态.Eip
	用户esp := 线程.U用户stack_2 + 线程.U用户stack大小_2
	eflags := 线程.Cpu状态.Eflags
	cs := 线程.Cpu状态.Cs
	esp := sche数据.tss.Getesp0()

	控制台_2.M打印(([]byte)("jump["))
	控制台_2.MUnsignedinteger32打印(eip)
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger32打印(用户esp)
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger32打印(eflags)
	控制台_2.M打印(([]byte)(":"))
	控制台_2.MUnsignedinteger32打印(cs)
	控制台_2.M打印(([]byte)(":"))

	控制台_2.MUnsignedinteger32打印(esp)
	控制台_2.M打印(([]byte)("]"))

	userproc条目 := 线程.Cpu状态.Ecx
	全局位移表格_2 := 线程.Cpu状态.Edx
	动态 := 线程.Cpu状态.Esi

	P端口写入字节(0x20, 0x20)
	jump用户模式iret(eip, 用户esp, eflags, userproc条目, 全局位移表格_2, 动态)
	控制台_2.M打印(([]byte)("usermode end"))
}
func 打印esp(esp uint32) {
	控制台_2.M打印(([]byte)("esp["))
	控制台_2.MUnsignedinteger32打印(esp)
}
