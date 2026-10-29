/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 入口

import (
	"io"
)

type I中断数字 uint8

const (
	D除法by零	= I中断数字(0)

	Nmi	= I中断数字(2)

	Overflow	= I中断数字(4)

	Bound范围exceeded	= I中断数字(5)

	I无效opcode	= I中断数字(6)

	D设备not可用	= I中断数字(7)

	D双精度故障	= I中断数字(8)

	I无效tss	= I中断数字(10)

	Segmentnot当前电池	= I中断数字(11)

	Stacksegment故障	= I中断数字(12)

	Gpfexception	= I中断数字(13)

	P页故障exception	= I中断数字(14)

	F浮动pointexception	= I中断数字(16)

	Alignmentcheck	= I中断数字(17)

	Machinecheck	= I中断数字(18)

	Simd浮动pointexception	= I中断数字(19)
)

func Init() {
	安装idt()
}

func H控制器中断(整型数字 I中断数字, ist位移 uint8, handler func(*Registers))

func 安装idt()

func dispatch中断()

func 中断入口条目()
