/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type InterruptRAQAM uint8

const (
	Dividebyzero	= InterruptRAQAM(0)

	Nmi	= InterruptRAQAM(2)

	Overflow	= InterruptRAQAM(4)

	Boundrangeexceeded	= InterruptRAQAM(5)

	Yaroqsizopcode	= InterruptRAQAM(6)

	UskunanotMavjud	= InterruptRAQAM(7)

	Doublefault	= InterruptRAQAM(8)

	Yaroqsiztss	= InterruptRAQAM(10)

	Segmentnotpresent	= InterruptRAQAM(11)

	Stacksegmentfault	= InterruptRAQAM(12)

	Gpfexception	= InterruptRAQAM(13)

	SAHIFAfaultexception	= InterruptRAQAM(14)

	Floatingpointexception	= InterruptRAQAM(16)

	Alignmentcheck	= InterruptRAQAM(17)

	Machinecheck	= InterruptRAQAM(18)

	Simdfloatingpointexception	= InterruptRAQAM(19)
)

func Init() {
	oʻrnatishidt()
}

func Handleinterrupt(intRAQAM InterruptRAQAM, istoffset uint8, handler func(*Registers))

func oʻrnatishidt()

func dispatchinterrupt()

func interruptgateentry()
