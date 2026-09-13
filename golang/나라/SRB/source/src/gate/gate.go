package gate

import ()

type Ометањеброј uint8

const (
	Dividebyzero	= Ометањеброј(0)

	Нми	= Ометањеброј(2)

	Overflow	= Ометањеброј(4)

	BoundОпсегexceeded	= Ометањеброј(5)

	Неисправноopcode	= Ометањеброј(6)

	УређајnotРасположиво	= Ометањеброј(7)

	Двострукоfault	= Ометањеброј(8)

	Неисправноtss	= Ометањеброј(10)

	SegmentnotПрисутна	= Ометањеброј(11)

	Stacksegmentfault	= Ометањеброј(12)

	Gpfexception	= Ометањеброј(13)

	СТРАНАfaultexception	= Ометањеброј(14)

	Лебдећиpointexception	= Ометањеброј(16)

	Alignmentcheck	= Ометањеброј(17)

	Machinecheck	= Ометањеброј(18)

	SimdЛебдећиpointexception	= Ометањеброј(19)
)

func Init() {
	инсталирајidt()
}

func РучкаОметање(целибројброј Ометањеброј, istoffset uint8, handler func(*Registers))

func инсталирајidt()

func dispatchОметање()

func ометањеgateунос()
