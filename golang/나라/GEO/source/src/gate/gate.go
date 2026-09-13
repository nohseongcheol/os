package gate

import ()

type Interruptრიცხვი uint8

const (
	Dividebyzero	= Interruptრიცხვი(0)

	Nmi	= Interruptრიცხვი(2)

	Overflow	= Interruptრიცხვი(4)

	Boundrangeexceeded	= Interruptრიცხვი(5)

	Iმიუღებელიopcode	= Interruptრიცხვი(6)

	Dმოწყობილობაnotხელმისაწვდომი	= Interruptრიცხვი(7)

	Doublefault	= Interruptრიცხვი(8)

	Iმიუღებელიtss	= Interruptრიცხვი(10)

	Segmentnotpresent	= Interruptრიცხვი(11)

	Stacksegmentfault	= Interruptრიცხვი(12)

	Gpfexception	= Interruptრიცხვი(13)

	Pგვერდიfaultexception	= Interruptრიცხვი(14)

	Floatingpointexception	= Interruptრიცხვი(16)

	Alignmentcheck	= Interruptრიცხვი(17)

	Machinecheck	= Interruptრიცხვი(18)

	Simdfloatingpointexception	= Interruptრიცხვი(19)
)

func Init() {
	დაყენებაidt()
}

func Handleinterrupt(intრიცხვი Interruptრიცხვი, istoffset uint8, handler func(*Registers))

func დაყენებაidt()

func dispatchinterrupt()

func interruptgateentry()
