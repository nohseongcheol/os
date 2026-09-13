package gate

import (
	"io"
)

type InterruptNumber uint8

const (
	DivideByZero	= InterruptNumber(0)

	NMI	= InterruptNumber(2)

	Overflow	= InterruptNumber(4)

	BoundRangeExceeded	= InterruptNumber(5)

	InvalidOpcode	= InterruptNumber(6)

	DeviceNotAvailable	= InterruptNumber(7)

	DoubleFault	= InterruptNumber(8)

	InvalidTSS	= InterruptNumber(10)

	SegmentNotPresent	= InterruptNumber(11)

	StackSegmentFault	= InterruptNumber(12)

	GPFException	= InterruptNumber(13)

	PageFaultException	= InterruptNumber(14)

	FloatingPointException	= InterruptNumber(16)

	AlignmentCheck	= InterruptNumber(17)

	MachineCheck	= InterruptNumber(18)

	SIMDFloatingPointException	= InterruptNumber(19)
)

func Vআরম্ভ_করা() {
	installIDT()
}

func HandleInterrupt(intNumber InterruptNumber, istOffset uint8, handler func(*Registers))

func installIDT()

func dispatchInterrupt()

func interruptGateEntries()
