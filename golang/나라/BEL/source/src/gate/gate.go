package gate

import ()

type InterruptGetal uint8

const (
	Dividebyzero	= InterruptGetal(0)

	Nmi	= InterruptGetal(2)

	Overflow	= InterruptGetal(4)

	BoundBereikexceeded	= InterruptGetal(5)

	Ongeldigopcode	= InterruptGetal(6)

	ApparaatNietBeschikbaar	= InterruptGetal(7)

	Dubbelfault	= InterruptGetal(8)

	Ongeldigtss	= InterruptGetal(10)

	SegmentNietAanwezig	= InterruptGetal(11)

	Stacksegmentfault	= InterruptGetal(12)

	Gpfexception	= InterruptGetal(13)

	Paginafaultexception	= InterruptGetal(14)

	Zwevendpointexception	= InterruptGetal(16)

	Alignmentcheck	= InterruptGetal(17)

	Machinecheck	= InterruptGetal(18)

	Simdzwevendpointexception	= InterruptGetal(19)
)

func Init() {
	installerenidt()
}

func Handgreepinterrupt(intGetal InterruptGetal, istVerschuiving uint8, handler func(*Registers))

func installerenidt()

func dispatchinterrupt()

func interruptgateItem()
