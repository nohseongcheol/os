/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package шлюз

import (
	"вводивывод"
)

type ПрерываниеЧисло uint8

const (
	ДелениеbyНоль	= ПрерываниеЧисло(0)

	Морскаямиля	= ПрерываниеЧисло(2)

	Overflow	= ПрерываниеЧисло(4)

	BoundДиапазонexceeded	= ПрерываниеЧисло(5)

	Недопустимыйopcode	= ПрерываниеЧисло(6)

	УстройствоnotДоступно	= ПрерываниеЧисло(7)

	Двойнойточностиошибка	= ПрерываниеЧисло(8)

	Недопустимыйtss	= ПрерываниеЧисло(10)

	SegmentnotПрисутствует	= ПрерываниеЧисло(11)

	Stacksegmentошибка	= ПрерываниеЧисло(12)

	Gpfexception	= ПрерываниеЧисло(13)

	Страницаошибкаexception	= ПрерываниеЧисло(14)

	Раздельноpointexception	= ПрерываниеЧисло(16)

	Alignmentcheck	= ПрерываниеЧисло(17)

	Machinecheck	= ПрерываниеЧисло(18)

	SimdРаздельноpointexception	= ПрерываниеЧисло(19)
)

func Init() {
	установитьidt()
}

func Ручкапрерывание(целоеЧисло ПрерываниеЧисло, istoffset uint8, handler func(*Registers))

func установитьidt()

func dispatchпрерывание()

func прерываниешлюззапись()
