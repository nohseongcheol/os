package gate

import (
	"io"
)

type ԸնդհատելՀԱՄԱՐ uint8

const (
	Dividebyzero	= ԸնդհատելՀԱՄԱՐ(0)

	Ծմղ	= ԸնդհատելՀԱՄԱՐ(2)

	Overflow	= ԸնդհատելՀԱՄԱՐ(4)

	BoundՄիջակայքexceeded	= ԸնդհատելՀԱՄԱՐ(5)

	Անթույլատրելիopcode	= ԸնդհատելՀԱՄԱՐ(6)

	ՍարքnotՀասանելի	= ԸնդհատելՀԱՄԱՐ(7)

	Doublefault	= ԸնդհատելՀԱՄԱՐ(8)

	Անթույլատրելիtss	= ԸնդհատելՀԱՄԱՐ(10)

	SegmentnotՆերկա	= ԸնդհատելՀԱՄԱՐ(11)

	Stacksegmentfault	= ԸնդհատելՀԱՄԱՐ(12)

	Gpfexception	= ԸնդհատելՀԱՄԱՐ(13)

	Էջfaultexception	= ԸնդհատելՀԱՄԱՐ(14)

	Floatingpointexception	= ԸնդհատելՀԱՄԱՐ(16)

	Alignmentcheck	= ԸնդհատելՀԱՄԱՐ(17)

	Machinecheck	= ԸնդհատելՀԱՄԱՐ(18)

	Simdfloatingpointexception	= ԸնդհատելՀԱՄԱՐ(19)
)

func Init() {
	տեղադրելidt()
}

func HandleԸնդհատել(intՀԱՄԱՐ ԸնդհատելՀԱՄԱՐ, istoffset uint8, handler func(*Registers))

func տեղադրելidt()

func dispatchԸնդհատել()

func ընդհատելgateentry()
