/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"io"
)

type AvbruddTall uint8

const (
	Dividebyzero	= AvbruddTall(0)

	Nmi	= AvbruddTall(2)

	Overflow	= AvbruddTall(4)

	BoundOmrådeexceeded	= AvbruddTall(5)

	Ugyldigopcode	= AvbruddTall(6)

	EnhetnotTilgjengelig	= AvbruddTall(7)

	Dobbelfault	= AvbruddTall(8)

	Ugyldigtss	= AvbruddTall(10)

	SegmentnotTilstede	= AvbruddTall(11)

	Stacksegmentfault	= AvbruddTall(12)

	Gpfexception	= AvbruddTall(13)

	Sidefaultexception	= AvbruddTall(14)

	Flytendepointexception	= AvbruddTall(16)

	Alignmentcheck	= AvbruddTall(17)

	Machinecheck	= AvbruddTall(18)

	Simdflytendepointexception	= AvbruddTall(19)
)

func Init() {
	installeridt()
}

func HåndtakAvbrudd(intTall AvbruddTall, istAvstand uint8, handler func(*Registers))

func installeridt()

func dispatchAvbrudd()

func avbruddgateentry()
