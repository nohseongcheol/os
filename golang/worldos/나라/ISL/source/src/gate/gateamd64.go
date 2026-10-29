/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"io"
)

type Interruptnumber uint8

const (
	Dividebyzero	= Interruptnumber(0)

	Nmi	= Interruptnumber(2)

	Overflow	= Interruptnumber(4)

	BoundSviðexceeded	= Interruptnumber(5)

	Ógiltopcode	= Interruptnumber(6)

	Tækinotavailable	= Interruptnumber(7)

	Tvöfaldfault	= Interruptnumber(8)

	Ógilttss	= Interruptnumber(10)

	Segmentnotpresent	= Interruptnumber(11)

	Stacksegmentfault	= Interruptnumber(12)

	Gpfexception	= Interruptnumber(13)

	Síðafaultexception	= Interruptnumber(14)

	Floatingpointexception	= Interruptnumber(16)

	Alignmentcheck	= Interruptnumber(17)

	Machinecheck	= Interruptnumber(18)

	Simdfloatingpointexception	= Interruptnumber(19)
)

func Init() {
	setjauppidt()
}

func Haldfanginterrupt(intnumber Interruptnumber, istoffset uint8, handler func(*Registers))

func setjauppidt()

func dispatchinterrupt()

func interruptgateentry()
