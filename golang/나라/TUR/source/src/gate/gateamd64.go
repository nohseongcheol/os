/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"girdiÇıktı"
)

type KesmeSayı uint8

const (
	BölbySıfır	= KesmeSayı(0)

	Nmi	= KesmeSayı(2)

	Overflow	= KesmeSayı(4)

	BoundAralıkexceeded	= KesmeSayı(5)

	Geçersizopcode	= KesmeSayı(6)

	AygıtnotUlaşılabilir	= KesmeSayı(7)

	Çiftfault	= KesmeSayı(8)

	Geçersiztss	= KesmeSayı(10)

	SegmentnotMevcut	= KesmeSayı(11)

	Stacksegmentfault	= KesmeSayı(12)

	Gpfexception	= KesmeSayı(13)

	Sayfafaultexception	= KesmeSayı(14)

	Kayanpointexception	= KesmeSayı(16)

	Alignmentcheck	= KesmeSayı(17)

	Machinecheck	= KesmeSayı(18)

	SimdKayanpointexception	= KesmeSayı(19)
)

func Init() {
	kuridt()
}

func HandleKesme(intSayı KesmeSayı, istoffset uint8, handler func(*Registers))

func kuridt()

func dispatchKesme()

func kesmegategirdi()
