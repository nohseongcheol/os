/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ゲート

import ()

type I割込みnumber uint8

const (
	D除算by数値の0	= I割込みnumber(0)

	Nmi	= I割込みnumber(2)

	Overflow	= I割込みnumber(4)

	Boundrangeexceeded	= I割込みnumber(5)

	I不正opcode	= I割込みnumber(6)

	Dデバイスインストールされていません使用可能	= I割込みnumber(7)

	D二重線障害	= I割込みnumber(8)

	I不正tss	= I割込みnumber(10)

	Segmentインストールされていません現在	= I割込みnumber(11)

	Stacksegment障害	= I割込みnumber(12)

	Gpfexception	= I割込みnumber(13)

	Pページ障害exception	= I割込みnumber(14)

	Fフローティングpointexception	= I割込みnumber(16)

	Alignmentcheck	= I割込みnumber(17)

	Machinecheck	= I割込みnumber(18)

	Simdフローティングpointexception	= I割込みnumber(19)
)

func Init() {
	インストールidt()
}

func H取っ手割込み(intnumber I割込みnumber, istoffset uint8, handler func(*Registers))

func インストールidt()

func dispatch割込み()

func 割込みゲートentry()
