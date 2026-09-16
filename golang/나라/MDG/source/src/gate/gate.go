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

	BoundElanelanaexceeded	= Interruptnumber(5)

	Tsymetyopcode	= Interruptnumber(6)

	PeriferikanotAzoampiasaina	= Interruptnumber(7)

	Doublefault	= Interruptnumber(8)

	Tsymetytss	= Interruptnumber(10)

	Segmentnotpresent	= Interruptnumber(11)

	Stacksegmentfault	= Interruptnumber(12)

	Gpfexception	= Interruptnumber(13)

	PEJYfaultexception	= Interruptnumber(14)

	Floatingpointexception	= Interruptnumber(16)

	Alignmentcheck	= Interruptnumber(17)

	Machinecheck	= Interruptnumber(18)

	Simdfloatingpointexception	= Interruptnumber(19)
)

func Init() {
	hametrakaidt()
}

func Handleinterrupt(intnumber Interruptnumber, istoffset uint8, handler func(*Registers))

func hametrakaidt()

func dispatchinterrupt()

func interruptgateentry()
