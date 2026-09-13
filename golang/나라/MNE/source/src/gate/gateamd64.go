package gate

import (
	"уИ"
)

type Ометањеброј uint8

const (
	Dividebyzero	= Ометањеброј(0)

	Нми	= Ометањеброј(2)

	Overflow	= Ометањеброј(4)

	BoundOpsegexceeded	= Ометањеброј(5)

	Neispravnoopcode	= Ометањеброј(6)

	УређајnotRaspoloživo	= Ометањеброј(7)

	Двострукоfault	= Ометањеброј(8)

	Neispravnotss	= Ометањеброј(10)

	SegmentnotPrisutno	= Ометањеброј(11)

	Stacksegmentfault	= Ометањеброј(12)

	Gpfexception	= Ометањеброј(13)

	Listfaultexception	= Ометањеброј(14)

	Lebdećipointexception	= Ометањеброј(16)

	Alignmentcheck	= Ометањеброј(17)

	Machinecheck	= Ометањеброј(18)

	SimdLebdećipointexception	= Ометањеброј(19)
)

func Init() {
	instalirajidt()
}

func РучкаОметање(целибројброј Ометањеброј, istoffset uint8, handler func(*Registers))

func instalirajidt()

func dispatchОметање()

func ометањеgateунос()
