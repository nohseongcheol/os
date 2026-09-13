package gate

import (
	"io"
)

type InterruptNumero uint8

const (
	Dividibyzero	= InterruptNumero(0)

	NM	= InterruptNumero(2)

	Overflow	= InterruptNumero(4)

	BoundIntervalloexceeded	= InterruptNumero(5)

	Nonvalidoopcode	= InterruptNumero(6)

	DispositivonotDisponibile	= InterruptNumero(7)

	Doppiafault	= InterruptNumero(8)

	Nonvalidotss	= InterruptNumero(10)

	SegmentnotPresente	= InterruptNumero(11)

	Stacksegmentfault	= InterruptNumero(12)

	Gpfexception	= InterruptNumero(13)

	PAGINAfaultexception	= InterruptNumero(14)

	Fluttuantepointexception	= InterruptNumero(16)

	Alignmentcheck	= InterruptNumero(17)

	Machinecheck	= InterruptNumero(18)

	SimdFluttuantepointexception	= InterruptNumero(19)
)

func Init() {
	installaidt()
}

func Manigliainterrupt(interoNumero InterruptNumero, istoffset uint8, handler func(*Registers))

func installaidt()

func dispatchinterrupt()

func interruptgatevoce()
