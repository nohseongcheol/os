/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 鍵盤

import . "unsafe"

import . "連接埠"
import . "中斷"
import . "控制台"

type I滑鼠事件handler interface {
	O時滑鼠下(按鈕 int8)
	O時滑鼠上(按鈕 int8)
	O時滑鼠移動(x int8, y int8)
}

var i滑鼠事件handler I滑鼠事件handler

type T預設滑鼠事件handler struct {
}

var 控制台_2 T控制台 = T控制台{}
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self T預設滑鼠事件handler) O時滑鼠下(按鈕 int8) {
	buffer := []byte("+")
	控制台_2.M列印xy(buffer, uint16(previousx), uint16(previousy))
}
func (self T預設滑鼠事件handler) O時滑鼠上(按鈕 int8)	{}
func (self T預設滑鼠事件handler) O時滑鼠移動(x int8, y int8) {

	x位置 += int16(x)
	if x位置 < 0 {
		x位置 = 0
	}
	if x位置 >= 80 {
		x位置 = 79
	}

	y位置 -= int16(y)

	if y位置 < 0 {
		y位置 = 0
	}
	if y位置 >= 25 {
		y位置 = 24
	}

	buffer := []byte(" ")
	控制台_2.M列印xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	控制台_2.M列印xy(buffer, uint16(x位置), uint16(y位置))

	previousx = x位置
	previousy = y位置
}

type T滑鼠驅動程式 struct {
	T中斷handler
}

var 啟用滑鼠驅動程式 *T滑鼠驅動程式
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

func 送出滑鼠指令(數值 uint8) bool {
	if !寫入ps2指令(0xD4) || !寫入ps2資料(數值) {
		return false
	}
	ack, 確定 := 讀取ps2資料()
	return 確定 && ack == 0xFA
}

func (self *T滑鼠驅動程式) Init驅動程式(管理器 *T中斷管理器, 滑鼠事件handler I滑鼠事件handler) {

	i滑鼠事件handler = T預設滑鼠事件handler{}

	if 滑鼠事件handler != nil {
		i滑鼠事件handler = 滑鼠事件handler
	}

	啟用滑鼠驅動程式 = self
	中斷handler = 控制把滑鼠中斷
	var address uintptr
	address = uintptr(Pointer(&中斷handler))
	self.Init(0x2C, uintptr(Pointer(管理器)), address)

	for i := 0; i < 32 && (P連接埠讀取位元組(指令連接埠_2)&0x01) != 0; i++ {
		P連接埠讀取位元組(資料連接埠_2)
	}

	if !寫入ps2指令(0xA8) || !寫入ps2指令(0x20) {
		return
	}
	狀態, 確定 := 讀取ps2資料()
	if !確定 {
		return
	}
	狀態 |= 0x02
	狀態 &^= 0x20
	if !寫入ps2指令(0x60) || !寫入ps2資料(狀態) {
		return
	}

	if !送出滑鼠指令(0xF6) || !送出滑鼠指令(0xF4) {
		return
	}
	位移 = 0

}

func 控制把滑鼠中斷(esp uint32) uint32 {
	if 啟用滑鼠驅動程式 == nil {
		P連接埠讀取位元組(資料連接埠_2)
		return esp
	}
	return 啟用滑鼠驅動程式.H控制把中斷(esp)
}

var 計數 uint8 = 0
var buffer_2 [3]int8
var 位移 uint8 = 0

var 按鈕_2 int8
var 待處理x int16
var 待處理y int16
var 待處理按鈕 int8
var 待處理滑鼠事件 bool

func (self *T滑鼠驅動程式) H控制把中斷(esp uint32) uint32 {
	狀態 := P連接埠讀取位元組(指令連接埠_2)
	if (狀態&0x01) == 0 || (狀態&0x20) == 0 {
		return esp
	}

	資料 := P連接埠讀取位元組(資料連接埠_2)

	if 位移 == 0 && (資料&0x08) == 0 {
		return esp
	}
	buffer_2[位移] = int8(資料)
	位移 = (位移 + 1) % 3
	if 位移 == 0 {
		packet狀態 := uint8(buffer_2[0])

		if (packet狀態 & 0xC0) == 0 {
			待處理x += int16(buffer_2[1])
			待處理y += int16(buffer_2[2])
			if 待處理x > 127 {
				待處理x = 127
			} else if 待處理x < -127 {
				待處理x = -127
			}
			if 待處理y > 127 {
				待處理y = 127
			} else if 待處理y < -127 {
				待處理y = -127
			}
		}
		待處理按鈕 = int8(packet狀態 & 0x07)
		待處理滑鼠事件 = true
	}

	return esp

}

func P程序待處理滑鼠事件集() {
	if i滑鼠事件handler == nil {
		return
	}

	I中斷deactive()
	if !待處理滑鼠事件 {
		I中斷啟用()
		return
	}
	x := int8(待處理x)
	y := int8(待處理y)
	新增按鈕 := 待處理按鈕
	old按鈕 := 按鈕_2

	待處理x = 0
	待處理y = 0
	待處理滑鼠事件 = false
	I中斷啟用()

	if x != 0 || y != 0 {
		i滑鼠事件handler.O時滑鼠移動(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		遮罩 := int8(0x1 << i)
		if (新增按鈕 & 遮罩) != (old按鈕 & 遮罩) {
			if (新增按鈕 & 遮罩) != 0 {
				i滑鼠事件handler.O時滑鼠下(int8(i + 1))
			} else {
				i滑鼠事件handler.O時滑鼠上(int8(i + 1))
			}
		}
	}
	按鈕_2 = 新增按鈕
}
