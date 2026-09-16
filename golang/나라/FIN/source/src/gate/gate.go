/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import ()

type KeskeytysNumero uint8

const (
	Dividebyzero	= KeskeytysNumero(0)

	Nmi	= KeskeytysNumero(2)

	Overflow	= KeskeytysNumero(4)

	BoundAlueexceeded	= KeskeytysNumero(5)

	Epäkelpoopcode	= KeskeytysNumero(6)

	LaitenotKäytettävissä	= KeskeytysNumero(7)

	Liukulukufault	= KeskeytysNumero(8)

	Epäkelpotss	= KeskeytysNumero(10)

	SegmentnotLiitetty	= KeskeytysNumero(11)

	Stacksegmentfault	= KeskeytysNumero(12)

	Gpfexception	= KeskeytysNumero(13)

	Sivufaultexception	= KeskeytysNumero(14)

	Kelluvapointexception	= KeskeytysNumero(16)

	Alignmentcheck	= KeskeytysNumero(17)

	Machinecheck	= KeskeytysNumero(18)

	SimdKelluvapointexception	= KeskeytysNumero(19)
)

func Init() {
	asennaidt()
}

func KahvaKeskeytys(kokonaislukuNumero KeskeytysNumero, istoffset uint8, handler func(*Registers))

func asennaidt()

func dispatchKeskeytys()

func keskeytysgatehakusana()
