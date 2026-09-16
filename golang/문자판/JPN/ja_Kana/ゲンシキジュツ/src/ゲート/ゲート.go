/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package ゲート

import ()

type Iワリコミnumber uint8

const (
	Dジョザンbyスウチノ0	= Iワリコミnumber(0)

	Nmi	= Iワリコミnumber(2)

	Overflow	= Iワリコミnumber(4)

	Boundrangeexceeded	= Iワリコミnumber(5)

	Iフセイopcode	= Iワリコミnumber(6)

	Dデバイスインストールサレテイマセンシヨウカノウ	= Iワリコミnumber(7)

	Dニジュウセンショウガイ	= Iワリコミnumber(8)

	Iフセイtss	= Iワリコミnumber(10)

	Segmentインストールサレテイマセンゲンザイ	= Iワリコミnumber(11)

	Stacksegmentショウガイ	= Iワリコミnumber(12)

	Gpfexception	= Iワリコミnumber(13)

	Pページショウガイexception	= Iワリコミnumber(14)

	Fフローティングpointexception	= Iワリコミnumber(16)

	Alignmentcheck	= Iワリコミnumber(17)

	Machinecheck	= Iワリコミnumber(18)

	Simdフローティングpointexception	= Iワリコミnumber(19)
)

func Init() {
	インストールidt()
}

func Hトッテワリコミ(intnumber Iワリコミnumber, istoffset uint8, handler func(*Registers))

func インストールidt()

func dispatchワリコミ()

func ワリコミゲートentry()
