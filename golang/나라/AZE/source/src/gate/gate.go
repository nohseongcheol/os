package gate

import ()

type Interruptnumber uint8

const (
	Dividebyzero	= Interruptnumber(0)

	Nmi	= Interruptnumber(2)

	Overflow	= Interruptnumber(4)

	Boundrangeexceeded	= Interruptnumber(5)

	Hökmsüzopcode	= Interruptnumber(6)

	Avadanlıqnotavailable	= Interruptnumber(7)

	Doublefault	= Interruptnumber(8)

	Hökmsüztss	= Interruptnumber(10)

	Segmentnotpresent	= Interruptnumber(11)

	Stacksegmentfault	= Interruptnumber(12)

	Gpfexception	= Interruptnumber(13)

	Səhifəfaultexception	= Interruptnumber(14)

	Floatingpointexception	= Interruptnumber(16)

	Alignmentcheck	= Interruptnumber(17)

	Machinecheck	= Interruptnumber(18)

	Simdfloatingpointexception	= Interruptnumber(19)
)

func Init() {
	quraşdıridt()
}

func Handleinterrupt(intnumber Interruptnumber, istoffset uint8, handler func(*Registers))

func quraşdıridt()

func dispatchinterrupt()

func interruptgateentry()
