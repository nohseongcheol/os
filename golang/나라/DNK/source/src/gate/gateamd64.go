package gate

import (
	"io"
)

type InterruptTal uint8

const (
	Dividebyzero	= InterruptTal(0)

	Sm	= InterruptTal(2)

	Overflow	= InterruptTal(4)

	BoundIntervalexceeded	= InterruptTal(5)

	Ugyldigopcode	= InterruptTal(6)

	EnhedIkkeTilgængelig	= InterruptTal(7)

	Doublefault	= InterruptTal(8)

	Ugyldigtss	= InterruptTal(10)

	SegmentIkkeTilstedeværende	= InterruptTal(11)

	Stacksegmentfault	= InterruptTal(12)

	Gpfexception	= InterruptTal(13)

	Sidefaultexception	= InterruptTal(14)

	Svævendepointexception	= InterruptTal(16)

	Alignmentcheck	= InterruptTal(17)

	Machinecheck	= InterruptTal(18)

	SimdSvævendepointexception	= InterruptTal(19)
)

func Init() {
	installéridt()
}

func Håndtaginterrupt(heltalTal InterruptTal, istForskydning uint8, handler func(*Registers))

func installéridt()

func dispatchinterrupt()

func interruptgateemne()
