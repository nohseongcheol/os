/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 入口

import (
	"输入输出"
)

type I中斷數字 uint8

const (
	D除by零	= I中斷數字(0)

	Nmi	= I中斷數字(2)

	Overflow	= I中斷數字(4)

	Boundrangeexceeded	= I中斷數字(5)

	I無效opcode	= I中斷數字(6)

	D裝置not可用空間	= I中斷數字(7)

	D倍精度故障	= I中斷數字(8)

	I無效tss	= I中斷數字(10)

	Segmentnot目前	= I中斷數字(11)

	Stacksegment故障	= I中斷數字(12)

	Gpfexception	= I中斷數字(13)

	P頁故障exception	= I中斷數字(14)

	F浮動pointexception	= I中斷數字(16)

	Alignmentcheck	= I中斷數字(17)

	Machinecheck	= I中斷數字(18)

	Simd浮動pointexception	= I中斷數字(19)
)

func Init() {
	安裝idt()
}

func H控制把中斷(整數數字 I中斷數字, ist位移 uint8, handler func(*Registers))

func 安裝idt()

func dispatch中斷()

func 中斷入口項目()
