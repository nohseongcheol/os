/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type PārtraukumsSkaitlis uint8

const (
	Dividebyzero	= PārtraukumsSkaitlis(0)

	Nmi	= PārtraukumsSkaitlis(2)

	Overflow	= PārtraukumsSkaitlis(4)

	BoundApgabalsexceeded	= PārtraukumsSkaitlis(5)

	Nederīgsopcode	= PārtraukumsSkaitlis(6)

	IerīcenotPieejams	= PārtraukumsSkaitlis(7)

	Doublefault	= PārtraukumsSkaitlis(8)

	Nederīgstss	= PārtraukumsSkaitlis(10)

	SegmentnotKlātesošs	= PārtraukumsSkaitlis(11)

	Stacksegmentfault	= PārtraukumsSkaitlis(12)

	Gpfexception	= PārtraukumsSkaitlis(13)

	Lapafaultexception	= PārtraukumsSkaitlis(14)

	Peldošspointexception	= PārtraukumsSkaitlis(16)

	Alignmentcheck	= PārtraukumsSkaitlis(17)

	Machinecheck	= PārtraukumsSkaitlis(18)

	Simdpeldošspointexception	= PārtraukumsSkaitlis(19)
)

func Init() {
	instalētidt()
}

func HandlePārtraukums(intSkaitlis PārtraukumsSkaitlis, istoffset uint8, handler func(*Registers))

func instalētidt()

func dispatchPārtraukums()

func pārtraukumsgateieraksts()
