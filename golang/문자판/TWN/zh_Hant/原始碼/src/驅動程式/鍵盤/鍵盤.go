package 鍵盤

import . "unsafe"

import . "連接埠"
import . "中斷"

import . "控制台"
import . "系統呼叫"

type I鍵盤事件handler interface {
	O時設定鍵下(設定鍵 byte)
	O時設定鍵上(設定鍵 byte)
}

var i鍵盤事件handler I鍵盤事件handler
var 預設鍵盤事件handler T預設鍵盤事件handler

type T預設鍵盤事件handler struct {
}

func (self *T預設鍵盤事件handler) O時設定鍵下(設定鍵 byte) {
	十六進位 := [16]byte{'0', '1', '2', '3',
		'4', '5', '6', '7',
		'8', '9', 'A', 'B',
		'C', 'D', 'E', 'F'}

	buffer := []byte("\n\n\n\n\n\nkeyboard :    ")

	buffer[17] = 十六進位[((設定鍵 >> 4) & 0xF)]
	buffer[18] = 十六進位[設定鍵&0xF]

	控制台_2 := T控制台{}
	控制台_2.M列印(buffer)

}
func (self *T預設鍵盤事件handler) O時設定鍵上(設定鍵 byte) {
}

type T鍵盤驅動程式 struct {
	T中斷handler
}

var 啟用鍵盤驅動程式 *T鍵盤驅動程式
var 中斷handler func(uint32) uint32

var 資料連接埠_2 uint16 = 0x60
var 指令連接埠_2 uint16 = 0x64

const ps2等待限制 = 100000

func 等待ps2輸入空() bool {
	for i := 0; i < ps2等待限制; i++ {
		if (P連接埠讀取位元組(指令連接埠_2) & 0x02) == 0 {
			return true
		}
	}
	return false
}

func 等待ps2輸出完全() bool {
	for i := 0; i < ps2等待限制; i++ {
		if (P連接埠讀取位元組(指令連接埠_2) & 0x01) != 0 {
			return true
		}
	}
	return false
}

func 寫入ps2指令(數值 uint8) bool {
	if !等待ps2輸入空() {
		return false
	}
	P連接埠寫入位元組(指令連接埠_2, 數值)
	return true
}

func 寫入ps2資料(數值 uint8) bool {
	if !等待ps2輸入空() {
		return false
	}
	P連接埠寫入位元組(資料連接埠_2, 數值)
	return true
}

func 讀取ps2資料() (uint8, bool) {
	if !等待ps2輸出完全() {
		return 0, false
	}
	return P連接埠讀取位元組(資料連接埠_2), true
}

func (self *T鍵盤驅動程式) Init驅動程式(管理器 *T中斷管理器, 鍵盤事件handler I鍵盤事件handler) {

	i鍵盤事件handler = &預設鍵盤事件handler
	if 鍵盤事件handler != nil {
		i鍵盤事件handler = 鍵盤事件handler
	}

	啟用鍵盤驅動程式 = self
	中斷handler = 控制把鍵盤中斷
	var address uintptr
	address = uintptr(Pointer(&中斷handler))

	self.Init(0x21, uintptr(Pointer(管理器)), address)

	for i := 0; i < 32 && (P連接埠讀取位元組(指令連接埠_2)&0x01) != 0; i++ {
		P連接埠讀取位元組(資料連接埠_2)
	}

	if !寫入ps2指令(0xAE) || !寫入ps2指令(0x20) {
		return
	}
	狀態, 確定 := 讀取ps2資料()
	if !確定 {
		return
	}
	狀態 |= 0x01
	狀態 &^= 0x10
	if !寫入ps2指令(0x60) || !寫入ps2資料(狀態) {
		return
	}

	if !寫入ps2資料(0xF4) {
		return
	}
	ack, 確定 := 讀取ps2資料()
	if !確定 || ack != 0xFA {
		return
	}

}

func 控制把鍵盤中斷(esp uint32) uint32 {
	if 啟用鍵盤驅動程式 == nil {
		P連接埠讀取位元組(資料連接埠_2)
		return esp
	}
	return 啟用鍵盤驅動程式.H控制把中斷(esp)
}

const 鍵盤佇列大小 = 64

var 鍵盤佇列 [鍵盤佇列大小]byte
var 鍵盤佇列讀取 uint8
var 鍵盤佇列寫入 uint8
var 左shift bool
var 右shift bool
var extended掃描code bool

func 佇列鍵盤位元組(設定鍵 byte) {
	下一個 := (鍵盤佇列寫入 + 1) % 鍵盤佇列大小
	if 下一個 == 鍵盤佇列讀取 {
		return
	}
	鍵盤佇列[鍵盤佇列寫入] = 設定鍵
	鍵盤佇列寫入 = 下一個
}

func P程序待處理鍵盤事件集() {
	for 鍵盤佇列讀取 != 鍵盤佇列寫入 {
		設定鍵 := 鍵盤佇列[鍵盤佇列讀取]
		鍵盤佇列讀取 = (鍵盤佇列讀取 + 1) % 鍵盤佇列大小
		Stdinput位元組(設定鍵)
		if i鍵盤事件handler != nil {
			i鍵盤事件handler.O時設定鍵下(設定鍵)
		}
	}
}

func 掃描codeto位元組(掃描code uint8) (byte, bool) {
	shift := 左shift || 右shift

	if 掃描code >= 0x02 && 掃描code <= 0x0B {
		if shift {
			return "!@#$%^&*()"[掃描code-0x02], true
		}
		return "1234567890"[掃描code-0x02], true
	}
	if 掃描code >= 0x10 && 掃描code <= 0x19 {
		設定鍵 := "qwertyuiop"[掃描code-0x10]
		if shift {
			設定鍵 -= 'a' - 'A'
		}
		return 設定鍵, true
	}
	if 掃描code >= 0x1E && 掃描code <= 0x26 {
		設定鍵 := "asdfghjkl"[掃描code-0x1E]
		if shift {
			設定鍵 -= 'a' - 'A'
		}
		return 設定鍵, true
	}
	if 掃描code >= 0x2C && 掃描code <= 0x32 {
		設定鍵 := "zxcvbnm"[掃描code-0x2C]
		if shift {
			設定鍵 -= 'a' - 'A'
		}
		return 設定鍵, true
	}

	switch 掃描code {
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

func (self *T鍵盤驅動程式) H控制把中斷(esp uint32) uint32 {
	狀態 := P連接埠讀取位元組(指令連接埠_2)
	if (狀態&0x01) == 0 || (狀態&0x20) != 0 {
		return esp
	}

	掃描code := P連接埠讀取位元組(資料連接埠_2)
	if 掃描code == 0xE0 {
		extended掃描code = true
		return esp
	}
	if extended掃描code {
		extended掃描code = false
		return esp
	}

	released := (掃描code & 0x80) != 0
	basecode := 掃描code & 0x7F
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

	if 設定鍵, 確定 := 掃描codeto位元組(basecode); 確定 {
		佇列鍵盤位元組(設定鍵)
	}

	return esp
}
