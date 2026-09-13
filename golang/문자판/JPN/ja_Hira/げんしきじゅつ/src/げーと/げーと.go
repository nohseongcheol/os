package げーと

import ()

type Iわりこみnumber uint8

const (
	Dじょざんbyすうちの0	= Iわりこみnumber(0)

	Nmi	= Iわりこみnumber(2)

	Overflow	= Iわりこみnumber(4)

	Boundrangeexceeded	= Iわりこみnumber(5)

	Iふせいopcode	= Iわりこみnumber(6)

	Dでばいすいんすとーるされていませんしようかのう	= Iわりこみnumber(7)

	Dにじゅうせんしょうがい	= Iわりこみnumber(8)

	Iふせいtss	= Iわりこみnumber(10)

	Segmentいんすとーるされていませんげんざい	= Iわりこみnumber(11)

	Stacksegmentしょうがい	= Iわりこみnumber(12)

	Gpfexception	= Iわりこみnumber(13)

	Pぺーじしょうがいexception	= Iわりこみnumber(14)

	Fふろーてぃんぐpointexception	= Iわりこみnumber(16)

	Alignmentcheck	= Iわりこみnumber(17)

	Machinecheck	= Iわりこみnumber(18)

	Simdふろーてぃんぐpointexception	= Iわりこみnumber(19)
)

func Init() {
	いんすとーるidt()
}

func Hとってわりこみ(intnumber Iわりこみnumber, istoffset uint8, handler func(*Registers))

func いんすとーるidt()

func dispatchわりこみ()

func わりこみげーとentry()
