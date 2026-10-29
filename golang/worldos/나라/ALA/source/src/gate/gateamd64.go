/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"io"
)

type AvbrottNummer uint8

const (
	DelabyNoll	= AvbrottNummer(0)

	M	= AvbrottNummer(2)

	Overflow	= AvbrottNummer(4)

	BoundIntervallexceeded	= AvbrottNummer(5)

	Ogiltigopcode	= AvbrottNummer(6)

	EnhetnotTillgängligt	= AvbrottNummer(7)

	Doublefault	= AvbrottNummer(8)

	Ogiltigtss	= AvbrottNummer(10)

	SegmentnotAnsluten	= AvbrottNummer(11)

	Stacksegmentfault	= AvbrottNummer(12)

	Gpfexception	= AvbrottNummer(13)

	Sidafaultexception	= AvbrottNummer(14)

	Svävandepointexception	= AvbrottNummer(16)

	Alignmentcheck	= AvbrottNummer(17)

	Machinecheck	= AvbrottNummer(18)

	SimdSvävandepointexception	= AvbrottNummer(19)
)

func Init() {
	installeraidt()
}

func HandtagAvbrott(intNummer AvbrottNummer, istFörskjutning uint8, handler func(*Registers))

func installeraidt()

func dispatchAvbrott()

func avbrottgatepost()
