/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package بوابة

import (
	"io"
)

type Iمقاطعةالأرقام uint8

const (
	Dividebyzero	= Iمقاطعةالأرقام(0)

	Nميلبحري	= Iمقاطعةالأرقام(2)

	Overflow	= Iمقاطعةالأرقام(4)

	Boundمدىexceeded	= Iمقاطعةالأرقام(5)

	Iغيرصحيحopcode	= Iمقاطعةالأرقام(6)

	Dالجهازnotمتوفر	= Iمقاطعةالأرقام(7)

	Dمضاعفخلل	= Iمقاطعةالأرقام(8)

	Iغيرصحيحtss	= Iمقاطعةالأرقام(10)

	Segmentnotالحالي	= Iمقاطعةالأرقام(11)

	Stacksegmentخلل	= Iمقاطعةالأرقام(12)

	Gpfexception	= Iمقاطعةالأرقام(13)

	Pصفحةخللexception	= Iمقاطعةالأرقام(14)

	Fعائمpointexception	= Iمقاطعةالأرقام(16)

	Aالمحاذاةcheck	= Iمقاطعةالأرقام(17)

	Machinecheck	= Iمقاطعةالأرقام(18)

	Simdعائمpointexception	= Iمقاطعةالأرقام(19)
)

func Init() {
	installidt()
}

func Hالتعاملمقاطعة(عددصحيحالأرقام Iمقاطعةالأرقام, istoffset uint8, handler func(*Registers))

func installidt()

func dispatchمقاطعة()

func مقاطعةبوابةentry()
