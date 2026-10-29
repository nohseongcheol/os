/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"io"
)

type Iማቋረጫቁጥር uint8

const (
	Dividebyzero	= Iማቋረጫቁጥር(0)

	Nmi	= Iማቋረጫቁጥር(2)

	Overflow	= Iማቋረጫቁጥር(4)

	Boundመጠንexceeded	= Iማቋረጫቁጥር(5)

	Iየማይሰራopcode	= Iማቋረጫቁጥር(6)

	Dዲቫይስnotዝግጁ	= Iማቋረጫቁጥር(7)

	Doublefault	= Iማቋረጫቁጥር(8)

	Iየማይሰራtss	= Iማቋረጫቁጥር(10)

	Segmentnotአሁን	= Iማቋረጫቁጥር(11)

	Stacksegmentfault	= Iማቋረጫቁጥር(12)

	Gpfexception	= Iማቋረጫቁጥር(13)

	Pገጽfaultexception	= Iማቋረጫቁጥር(14)

	Fተንሳፋፊpointexception	= Iማቋረጫቁጥር(16)

	Alignmentcheck	= Iማቋረጫቁጥር(17)

	Machinecheck	= Iማቋረጫቁጥር(18)

	Simdተንሳፋፊpointexception	= Iማቋረጫቁጥር(19)
)

func Init() {
	መግጠምidt()
}

func Handleማቋረጫ(intቁጥር Iማቋረጫቁጥር, istoffset uint8, handler func(*Registers))

func መግጠምidt()

func dispatchማቋረጫ()

func ማቋረጫgateentry()
