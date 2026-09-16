/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 键盘

import . "unsafe"

import . "端口"
import . "中断"
import . "控制台"

type I鼠标事件handler interface {
	O时鼠标下(按钮 int8)
	O时鼠标向上(按钮 int8)
	O时鼠标移动(x int8, y int8)
}

var i鼠标事件handler I鼠标事件handler

type T默认鼠标事件handler struct {
}

var 控制台_2 T控制台 = T控制台{}
var previousx int16 = 0
var previousy int16 = 0
var x位置 int16 = 0
var y位置 int16 = 0

func (self T默认鼠标事件handler) O时鼠标下(按钮 int8) {
	buffer := []byte("+")
	控制台_2.M打印xy(buffer, uint16(previousx), uint16(previousy))
}
func (self T默认鼠标事件handler) O时鼠标向上(按钮 int8)	{}
func (self T默认鼠标事件handler) O时鼠标移动(x int8, y int8) {

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
	控制台_2.M打印xy(buffer, uint16(previousx), uint16(previousy))

	buffer = []byte("0")
	控制台_2.M打印xy(buffer, uint16(x位置), uint16(y位置))

	previousx = x位置
	previousy = y位置
}

type T鼠标驱动程序 struct {
	T中断handler
}

var 活跃鼠标驱动程序 *T鼠标驱动程序
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

func 发送鼠标命令(值 uint8) bool {
	if !写入ps2命令(0xD4) || !写入ps2数据(值) {
		return false
	}
	ack, 确定 := 读取ps2数据()
	return 确定 && ack == 0xFA
}

func (self *T鼠标驱动程序) Init驱动程序(管理器 *T中断管理器, 鼠标事件handler I鼠标事件handler) {

	i鼠标事件handler = T默认鼠标事件handler{}

	if 鼠标事件handler != nil {
		i鼠标事件handler = 鼠标事件handler
	}

	活跃鼠标驱动程序 = self
	中断handler = 控制器鼠标中断
	var address uintptr
	address = uintptr(Pointer(&中断handler))
	self.Init(0x2C, uintptr(Pointer(管理器)), address)

	for i := 0; i < 32 && (P端口读取字节(命令端口_2)&0x01) != 0; i++ {
		P端口读取字节(数据端口_2)
	}

	if !写入ps2命令(0xA8) || !写入ps2命令(0x20) {
		return
	}
	状态, 确定 := 读取ps2数据()
	if !确定 {
		return
	}
	状态 |= 0x02
	状态 &^= 0x20
	if !写入ps2命令(0x60) || !写入ps2数据(状态) {
		return
	}

	if !发送鼠标命令(0xF6) || !发送鼠标命令(0xF4) {
		return
	}
	位移 = 0

}

func 控制器鼠标中断(esp uint32) uint32 {
	if 活跃鼠标驱动程序 == nil {
		P端口读取字节(数据端口_2)
		return esp
	}
	return 活跃鼠标驱动程序.H控制器中断(esp)
}

var 计数 uint8 = 0
var buffer_2 [3]int8
var 位移 uint8 = 0

var 按钮_2 int8
var 待处理x int16
var 待处理y int16
var 待处理按钮 int8
var 待处理鼠标事件 bool

func (self *T鼠标驱动程序) H控制器中断(esp uint32) uint32 {
	状态 := P端口读取字节(命令端口_2)
	if (状态&0x01) == 0 || (状态&0x20) == 0 {
		return esp
	}

	数据 := P端口读取字节(数据端口_2)

	if 位移 == 0 && (数据&0x08) == 0 {
		return esp
	}
	buffer_2[位移] = int8(数据)
	位移 = (位移 + 1) % 3
	if 位移 == 0 {
		packet状态 := uint8(buffer_2[0])

		if (packet状态 & 0xC0) == 0 {
			待处理x += int16(buffer_2[1])
			待处理y += int16(buffer_2[2])
			if 待处理x > 127 {
				待处理x = 127
			} else if 待处理x < -127 {
				待处理x = -127
			}
			if 待处理y > 127 {
				待处理y = 127
			} else if 待处理y < -127 {
				待处理y = -127
			}
		}
		待处理按钮 = int8(packet状态 & 0x07)
		待处理鼠标事件 = true
	}

	return esp

}

func P进程待处理鼠标事件集() {
	if i鼠标事件handler == nil {
		return
	}

	I中断deactive()
	if !待处理鼠标事件 {
		I中断活跃()
		return
	}
	x := int8(待处理x)
	y := int8(待处理y)
	新建按钮 := 待处理按钮
	old按钮 := 按钮_2

	待处理x = 0
	待处理y = 0
	待处理鼠标事件 = false
	I中断活跃()

	if x != 0 || y != 0 {
		i鼠标事件handler.O时鼠标移动(x, y)
	}

	var i uint8 = 0
	for i = 0; i < 3; i++ {
		掩码 := int8(0x1 << i)
		if (新建按钮 & 掩码) != (old按钮 & 掩码) {
			if (新建按钮 & 掩码) != 0 {
				i鼠标事件handler.O时鼠标下(int8(i + 1))
			} else {
				i鼠标事件handler.O时鼠标向上(int8(i + 1))
			}
		}
	}
	按钮_2 = 新建按钮
}
