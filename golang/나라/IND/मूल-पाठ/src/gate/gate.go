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

	Boundrangeexceeded	= Interruptnumber(5)

	Invalidopcode	= Interruptnumber(6)

	Dउपकरणnotavailable	= Interruptnumber(7)

	Doublefault	= Interruptnumber(8)

	Invalidtss	= Interruptnumber(10)

	Segmentnotpresent	= Interruptnumber(11)

	Stacksegmentfault	= Interruptnumber(12)

	Gpfexception	= Interruptnumber(13)

	Pagefaultexception	= Interruptnumber(14)

	Floatingpointexception	= Interruptnumber(16)

	Alignmentcheck	= Interruptnumber(17)

	Machinecheck	= Interruptnumber(18)

	Simdfloatingpointexception	= Interruptnumber(19)
)

func Init() {
	installidt()
}

func Handleinterrupt(intnumber Interruptnumber, istoffset uint8, handler func(*Registers))

func installidt()

func dispatchinterrupt()

func interruptgateentry()
