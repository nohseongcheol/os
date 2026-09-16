/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package tor

import ()

type UnterbrechungNummer uint8

const (
	DividierenbyNull	= UnterbrechungNummer(0)

	Sm	= UnterbrechungNummer(2)

	Overflow	= UnterbrechungNummer(4)

	BoundSpannweiteexceeded	= UnterbrechungNummer(5)

	Ungültigopcode	= UnterbrechungNummer(6)

	GerätNichtVerfügbar	= UnterbrechungNummer(7)

	GleitkommazahlFehler	= UnterbrechungNummer(8)

	Ungültigtss	= UnterbrechungNummer(10)

	SegmentNichtVorhanden	= UnterbrechungNummer(11)

	StacksegmentFehler	= UnterbrechungNummer(12)

	Gpfexception	= UnterbrechungNummer(13)

	SeiteFehlerexception	= UnterbrechungNummer(14)

	Gleitendpointexception	= UnterbrechungNummer(16)

	Alignmentcheck	= UnterbrechungNummer(17)

	Machinecheck	= UnterbrechungNummer(18)

	Simdgleitendpointexception	= UnterbrechungNummer(19)
)

func Init() {
	installierenidt()
}

func GriffUnterbrechung(ganzzahlNummer UnterbrechungNummer, istVersatz uint8, handler func(*Registers))

func installierenidt()

func dispatchUnterbrechung()

func unterbrechungTorEintrag()
