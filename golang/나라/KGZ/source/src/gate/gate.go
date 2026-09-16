/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type InterruptНОМЕР uint8

const (
	Dividebyzero	= InterruptНОМЕР(0)

	Деңизмилясы	= InterruptНОМЕР(2)

	Overflow	= InterruptНОМЕР(4)

	BoundДиапазонexceeded	= InterruptНОМЕР(5)

	Invalidopcode	= InterruptНОМЕР(6)

	ТүзүлүшүnotЖеткиликтүүсү	= InterruptНОМЕР(7)

	Doublefault	= InterruptНОМЕР(8)

	Invalidtss	= InterruptНОМЕР(10)

	Segmentnotpresent	= InterruptНОМЕР(11)

	Stacksegmentfault	= InterruptНОМЕР(12)

	Gpfexception	= InterruptНОМЕР(13)

	БАРАКfaultexception	= InterruptНОМЕР(14)

	Floatingpointexception	= InterruptНОМЕР(16)

	Alignmentcheck	= InterruptНОМЕР(17)

	Machinecheck	= InterruptНОМЕР(18)

	Simdfloatingpointexception	= InterruptНОМЕР(19)
)

func Init() {
	орнотууidt()
}

func Handleinterrupt(intНОМЕР InterruptНОМЕР, istoffset uint8, handler func(*Registers))

func орнотууidt()

func dispatchinterrupt()

func interruptgateentry()
