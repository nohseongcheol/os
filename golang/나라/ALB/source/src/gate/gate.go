/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type Interruptnumber uint8

const (
	Dividebyzero	= Interruptnumber(0)

	Nmi	= Interruptnumber(2)

	Overflow	= Interruptnumber(4)

	BoundIntervalexceeded	= Interruptnumber(5)

	Epavlefshmeopcode	= Interruptnumber(6)

	DispozitivinotNëdispozicion	= Interruptnumber(7)

	Doublefault	= Interruptnumber(8)

	Epavlefshmetss	= Interruptnumber(10)

	Segmentnotpresent	= Interruptnumber(11)

	Stacksegmentfault	= Interruptnumber(12)

	Gpfexception	= Interruptnumber(13)

	Faqefaultexception	= Interruptnumber(14)

	Pezullpointexception	= Interruptnumber(16)

	Alignmentcheck	= Interruptnumber(17)

	Machinecheck	= Interruptnumber(18)

	Simdpezullpointexception	= Interruptnumber(19)
)

func Init() {
	instaloidt()
}

func Handleinterrupt(intnumber Interruptnumber, istoffset uint8, handler func(*Registers))

func instaloidt()

func dispatchinterrupt()

func interruptgateentry()
