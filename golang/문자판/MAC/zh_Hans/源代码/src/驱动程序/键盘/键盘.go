package 键盘

import . "unsafe"

import . "端口"
import . "中断"

import . "控制台"
import . "系统调用"

type I键盘事件handler interface {
	O时关键下(关键 byte)
	O时关键向上(关键 byte)
}

var i键盘事件handler I键盘事件handler
var 默认键盘事件handler T默认键盘事件handler

type T默认键盘事件handler struct {
}

func (self *T默认键盘事件handler) O时关键下(关键 byte) {
	十六进制 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = 十六进制[((关键 >> 4) & 0xF)]
	buffer[18] = 十六进制[关键&0xF]

	控制台_2 := T控制台{}
	控制台_2.M打印(buffer)

}
func (self *T默认键盘事件handler) O时关键向上(关键 byte) {
}

type T键盘驱动程序 struct {
	T中断handler
}

var 活跃键盘驱动程序 *T键盘驱动程序
var 中断handler func(uint32) uint32

var 数据端口_2 uint16 = 0x60
var 命令端口_2 uint16 = 0x64

const ps2等待限定 = 100000

func 等待ps2输入空() bool {
	for i := 0; i < ps2等待限定; i++ {
		if (P端口读取字节(命令端口_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func 等待ps2输出全部() bool {
	for i := 0; i < ps2等待限定; i++ {
		if (P端口读取字节(命令端口_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func 写入ps2命令(值 uint8) bool {
	if !等待ps2输入空() {
		return false
	}
	P端口写入字节(命令端口_2, 值)
	return true
}

func 写入ps2数据(值 uint8) bool {
	if !等待ps2输入空() {
		return false
	}
	P端口写入字节(数据端口_2, 值)
	return true
}

func 读取ps2数据() (uint8, bool) {
	if !等待ps2输出全部() {
		return 0, false
	}
	return P端口读取字节(数据端口_2), true
}

func (self *T键盘驱动程序) Init驱动程序(管理器 *T中断管理器, 键盘事件handler I键盘事件handler) {

	i键盘事件handler = &默认键盘事件handler
	if 键盘事件handler != nil {
		i键盘事件handler = 键盘事件handler
	}

	活跃键盘驱动程序 = self
	中断handler = 控制器键盘中断
	var address uintptr
	address = uintptr(Pointer(&中断handler))

	self.Init(0x21, uintptr(Pointer(管理器)), address)

	for i := 0; i < 32 && (P端口读取字节(命令端口_2)&0x01) != 0; i++ {
		P端口读取字节(数据端口_2)
	}

	if !写入ps2命令(0xAE) || !写入ps2命令(0x20) {
		return
	}
	状态, 确定 := 读取ps2数据()
	if !确定 {
		return
	}
	状态 |= 0x01
	状态 &^= 0x10
	if !写入ps2命令(0x60) || !写入ps2数据(状态) {
		return
	}

	if !写入ps2数据(0xF4) {
		return
	}
	ack, 确定 := 读取ps2数据()
	if !确定 || ack != 0xFA {
		return
	}

}

func 控制器键盘中断(esp uint32) uint32 {
	if 活跃键盘驱动程序 == nil {
		P端口读取字节(数据端口_2)
		return esp
	}
	return 活跃键盘驱动程序.H控制器中断(esp)
}

const 键盘队列大小 = 64

var 键盘队列 [键盘队列大小]byte
var 键盘队列读取 uint8
var 键盘队列写入 uint8
var 左shift bool
var 右shift bool
var extended扫描code bool

func 队列键盘字节(关键 byte) {
	下一个 := (键盘队列写入 + 1) % 键盘队列大小
	if 下一个 == 键盘队列读取 {
		return
	}
	键盘队列[键盘队列写入] = 关键
	键盘队列写入 = 下一个
}

func P进程待处理键盘事件集() {
	for 键盘队列读取 != 键盘队列写入 {
		关键 := 键盘队列[键盘队列读取]
		键盘队列读取 = (键盘队列读取 + 1) % 键盘队列大小
		Stdinput字节(关键)
		if i键盘事件handler != nil {
			i键盘事件handler.O时关键下(关键)
		}
	}
}

func 扫描codeto字节(扫描code uint8) (byte, bool) {
	shift := 左shift || 右shift

	if 扫描code >= 0x02 && 扫描code <= 0x0B {
		if shift {
			return "!@#$%^&*()"[扫描code-0x02], true
		}
		return "1234567890"[扫描code-0x02], true
	}
	if 扫描code >= 0x10 && 扫描code <= 0x19 {
		关键 := "qwertyuiop"[扫描code-0x10]
		if shift {
			关键 -= 'a' - 'A'
		}
		return 关键, true
	}
	if 扫描code >= 0x1E && 扫描code <= 0x26 {
		关键 := "asdfghjkl"[扫描code-0x1E]
		if shift {
			关键 -= 'a' - 'A'
		}
		return 关键, true
	}
	if 扫描code >= 0x2C && 扫描code <= 0x32 {
		关键 := "zxcvbnm"[扫描code-0x2C]
		if shift {
			关键 -= 'a' - 'A'
		}
		return 关键, true
	}

	switch 扫描code {
	case 0x0C:
		if shift {
			return '_', true
		}
		return '-', true
	case 0x0D:
		if shift {
			return '+', true
		}
		return '=', true
	case 0x1A:
		if shift {
			return '{', true
		}
		return '[', true
	case 0x1B:
		if shift {
			return '}', true
		}
		return ']', true
	case 0x1C:
		return '\n', true
	case 0x27:
		if shift {
			return ':', true
		}
		return ';', true
	case 0x28:
		if shift {
			return '"', true
		}
		return '\'', true
	case 0x29:
		if shift {
			return '~', true
		}
		return '`', true
	case 0x2B:
		if shift {
			return '|', true
		}
		return '\\', true
	case 0x33:
		if shift {
			return '<', true
		}
		return ',', true
	case 0x34:
		if shift {
			return '>', true
		}
		return '.', true
	case 0x35:
		if shift {
			return '?', true
		}
		return '/', true
	case 0x39:
		return ' ', true
	}
	return 0, false
}

func (self *T键盘驱动程序) H控制器中断(esp uint32) uint32 {
	状态 := P端口读取字节(命令端口_2)
	if (状态&0x01) == 0 || (状态&0x20) != 0 {
		return esp
	}

	扫描code := P端口读取字节(数据端口_2)
	if 扫描code == 0xE0 {
		extended扫描code = true
		return esp
	}
	if extended扫描code {
		extended扫描code = false
		return esp
	}

	released := (扫描code & 0x80) != 0
	basecode := 扫描code & 0x7F
	if basecode == 0x2A {
		左shift = !released
		return esp
	}
	if basecode == 0x36 {
		右shift = !released
		return esp
	}
	if released {
		return esp
	}

	if 关键, 确定 := 扫描codeto字节(basecode); 确定 {
		队列键盘字节(关键)
	}

	return esp
}
