/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package gate

import (
	"io"
)

type ПрекъсванеЧисло uint8

const (
	Dividebyzero	= ПрекъсванеЧисло(0)

	Nmi	= ПрекъсванеЧисло(2)

	Overflow	= ПрекъсванеЧисло(4)

	BoundДиапазонexceeded	= ПрекъсванеЧисло(5)

	Невалиденopcode	= ПрекъсванеЧисло(6)

	УстройствоnotНалично	= ПрекъсванеЧисло(7)

	Дублиранеfault	= ПрекъсванеЧисло(8)

	Невалиденtss	= ПрекъсванеЧисло(10)

	SegmentnotНалична	= ПрекъсванеЧисло(11)

	Stacksegmentfault	= ПрекъсванеЧисло(12)

	Gpfexception	= ПрекъсванеЧисло(13)

	Страницаfaultexception	= ПрекъсванеЧисло(14)

	Плаващоpointexception	= ПрекъсванеЧисло(16)

	Alignmentcheck	= ПрекъсванеЧисло(17)

	Machinecheck	= ПрекъсванеЧисло(18)

	Simdплаващоpointexception	= ПрекъсванеЧисло(19)
)

func Init() {
	инсталиранеidt()
}

func РъкохваткаПрекъсване(цялочислоЧисло ПрекъсванеЧисло, istoffset uint8, handler func(*Registers))

func инсталиранеidt()

func dispatchПрекъсване()

func прекъсванеgateзапис()
