/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type InterruptBroj uint8

const (
	Dividebyzero	= InterruptBroj(0)

	Nmi	= InterruptBroj(2)

	Overflow	= InterruptBroj(4)

	Boundrangeexceeded	= InterruptBroj(5)

	Nevažećeopcode	= InterruptBroj(6)

	UređajnotDostupan	= InterruptBroj(7)

	Doublefault	= InterruptBroj(8)

	Nevažećetss	= InterruptBroj(10)

	Segmentnotpresent	= InterruptBroj(11)

	Stacksegmentfault	= InterruptBroj(12)

	Gpfexception	= InterruptBroj(13)

	Stranicafaultexception	= InterruptBroj(14)

	Floatingpointexception	= InterruptBroj(16)

	Alignmentcheck	= InterruptBroj(17)

	Machinecheck	= InterruptBroj(18)

	Simdfloatingpointexception	= InterruptBroj(19)
)

func Init() {
	instalirajidt()
}

func Handleinterrupt(intBroj InterruptBroj, istoffset uint8, handler func(*Registers))

func instalirajidt()

func dispatchinterrupt()

func interruptgateunos()
