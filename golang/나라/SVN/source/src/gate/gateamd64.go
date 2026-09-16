/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"vI"
)

type PrekinitevŠtevilka uint8

const (
	Dividebyzero	= PrekinitevŠtevilka(0)

	Nmi	= PrekinitevŠtevilka(2)

	Overflow	= PrekinitevŠtevilka(4)

	BoundObmočjeexceeded	= PrekinitevŠtevilka(5)

	Neveljavnoopcode	= PrekinitevŠtevilka(6)

	NapravanotRazpoložljivo	= PrekinitevŠtevilka(7)

	Dvojnofault	= PrekinitevŠtevilka(8)

	Neveljavnotss	= PrekinitevŠtevilka(10)

	SegmentnotPrisotnost	= PrekinitevŠtevilka(11)

	Stacksegmentfault	= PrekinitevŠtevilka(12)

	Gpfexception	= PrekinitevŠtevilka(13)

	Stranfaultexception	= PrekinitevŠtevilka(14)

	Floatingpointexception	= PrekinitevŠtevilka(16)

	Alignmentcheck	= PrekinitevŠtevilka(17)

	Machinecheck	= PrekinitevŠtevilka(18)

	Simdfloatingpointexception	= PrekinitevŠtevilka(19)
)

func Init() {
	namestiidt()
}

func RočicaPrekinitev(številoŠtevilka PrekinitevŠtevilka, istoffset uint8, handler func(*Registers))

func namestiidt()

func dispatchPrekinitev()

func prekinitevgatevnos()
