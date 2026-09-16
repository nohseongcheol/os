/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 共享媒介網路框

import . "控制台"

import . "amdam79c973"
import . "unsafe"
import . "工具"

var 乙太網路控制台 T控制台 = T控制台{}

type T乙太網路框架標頭buffer struct {
	目的地macbe	[6]byte
	來源macbe		[6]byte
	乙太網路類型be	[2]byte
}

var 框架標頭大小 int = 14

type T共享媒介網路框標頭 struct {
	目的地macbe	uint64
	來源macbe		uint64
	乙太網路類型be	uint16
}

func (self *T共享媒介網路框標頭) Init(buffer_2 T乙太網路框架標頭buffer) {
	self.目的地macbe = (A陣列tounsignedinteger48(buffer_2.目的地macbe))
	self.來源macbe = (A陣列tounsignedinteger48(buffer_2.來源macbe))
	self.乙太網路類型be = (A陣列tounsignedinteger16(buffer_2.乙太網路類型be))

}
func (self *T共享媒介網路框標頭) S設定buffer(buffer_2 *T乙太網路框架標頭buffer) {
	buffer_2.目的地macbe = Unsignedinteger48to陣列(Unsignedinteger48r(self.目的地macbe))
	buffer_2.來源macbe = Unsignedinteger48to陣列(Unsignedinteger48r(self.來源macbe))
	buffer_2.乙太網路類型be = Unsignedinteger16to陣列(Unsignedinteger16r(self.乙太網路類型be))
}

type I乙太網路框架handler interface {
	Init(backend T共享媒介網路框提供器)
	S設定handler(handler I乙太網路框架handler, 乙太網路類型 uint16)
	O乙太網路框架receivewhen(資料指標 uintptr, 大小 int) bool
	S送出(目的地macbe uint64, 資料指標 uintptr, 大小 uint32)
	S框架送出(目的地macbe uint64, 乙太網路類型be uint16, 資料指標 uintptr, 大小 uint32)
	Providerget() T共享媒介網路框提供器
	Getmacaddress() uint64
	Getipaddress() uint64
}

type T乙太網路框架handler struct {
}

var 框架 T共享媒介網路框標頭
var Backend T共享媒介網路框提供器
var handler_2 [65535]I乙太網路框架handler
var efhandler *T乙太網路框架handler = nil

func (self *T乙太網路框架handler) Init(backend T共享媒介網路框提供器) {
	Backend = backend
}

func (self *T乙太網路框架handler) S設定handler(handler I乙太網路框架handler, p乙太網路類型 uint16) {
	handler_2[p乙太網路類型] = handler
}
func (self *T乙太網路框架handler) S設定backend(backend T共享媒介網路框提供器) {
	Backend = backend
}
func (self *T乙太網路框架handler) Getbackend() T共享媒介網路框提供器 {
	return Backend
}
func (self *T乙太網路框架handler) O乙太網路框架receivewhen(資料指標 uintptr, 大小 int) bool {
	乙太網路控制台.M列印(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *T乙太網路框架handler) S送出(目的地macbe uint64, 資料指標 uintptr, 大小 uint32) {
	Backend.S框架送出(目的地macbe, 框架.乙太網路類型be, 資料指標, 大小)
}
func (self *T乙太網路框架handler) S框架送出(目的地macbe uint64, 乙太網路類型be uint16, 資料指標 uintptr, 大小 uint32) {
	Backend.S框架送出(目的地macbe, 乙太網路類型be, 資料指標, 大小)
}
func (self *T乙太網路框架handler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *T乙太網路框架handler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *T乙太網路框架handler) Providerget() T共享媒介網路框提供器 {
	return Backend
}

type T乙太網路框架raw資料handler struct {
	TRaw資料handler
}

var provider T共享媒介網路框提供器

func (self *T乙太網路框架raw資料handler) Init(pprovider T共享媒介網路框提供器, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *T乙太網路框架raw資料handler) O時raw資料receive(資料指標 uintptr, 大小 int) bool {
	return provider.O時raw資料receive(資料指標, 大小)
}
func (self *T乙太網路框架raw資料handler) S送出(資料指標 uintptr, 大小 uint32) {
	provider.S送出(資料指標, 大小)
}
func (self *T乙太網路框架raw資料handler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *T乙太網路框架raw資料handler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *T乙太網路框架raw資料handler) Providerget() T共享媒介網路框提供器 {
	return provider
}

type T共享媒介網路框提供器 struct {
	網路紙牌		Tamdam79c973
	handler_2	[65565]I乙太網路框架handler
}

func (self *T共享媒介網路框提供器) Init(backend Tamdam79c973) {

	self.網路紙牌 = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var 計數 uint16 = 0

func (self *T共享媒介網路框提供器) O時raw資料receive(資料指標 uintptr, 大小 int) bool {

	var buffer_2 *T乙太網路框架標頭buffer = (*T乙太網路框架標頭buffer)(Pointer(資料指標))
	var 框架 T共享媒介網路框標頭 = T共享媒介網路框標頭{}
	框架.Init(*buffer_2)
	var reply bool = false

	if 框架.目的地macbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(框架.目的地macbe) == self.Getmacaddress() {
		if handler_2[框架.乙太網路類型be] != nil {
			乙太網路控制台.M列印(([]byte)("provider\n"))

			var 位址參照 uintptr = uintptr(Pointer(資料指標)) + uintptr(框架標頭大小)
			reply = handler_2[框架.乙太網路類型be].O乙太網路框架receivewhen(位址參照, 大小-框架標頭大小)

		}
	}

	if reply {
		框架.目的地macbe = 框架.來源macbe
		框架.來源macbe = Unsignedinteger48r(self.Getmacaddress())
		框架.S設定buffer(buffer_2)

	}

	乙太網路控制台.M列印xy(([]byte)("spro["), 0, 1)
	乙太網路控制台.MUnsignedinteger64列印(框架.來源macbe)
	乙太網路控制台.M列印(([]byte)(":"))
	乙太網路控制台.MUnsignedinteger64列印(框架.目的地macbe)
	乙太網路控制台.M列印(([]byte)(":]["))
	乙太網路控制台.MUnsignedinteger64列印(self.Getmacaddress())
	乙太網路控制台.M列印(([]byte)(":"))
	乙太網路控制台.MUnsignedinteger16列印(框架.乙太網路類型be)
	乙太網路控制台.M列印(([]byte)("]"))

	return reply

}
func (self *T共享媒介網路框提供器) S送出(資料指標 uintptr, 大小 uint32) {
	self.網路紙牌.S送出(資料指標, 大小)
}
func (self *T共享媒介網路框提供器) S框架送出(目的地macbe uint64, 乙太網路類型be uint16, 資料指標 uintptr, 大小 uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *T乙太網路框架標頭buffer = (*T乙太網路框架標頭buffer)(Pointer(&buffer2_2))

	var 框架 T共享媒介網路框標頭 = T共享媒介網路框標頭{}
	框架.Init(*buffer_2)

	框架.目的地macbe = Unsignedinteger48r(目的地macbe)
	框架.來源macbe = Unsignedinteger48r(self.網路紙牌.Getmacaddress())
	框架.乙太網路類型be = Unsignedinteger16r(乙太網路類型be)

	框架.S設定buffer(buffer_2)
	var 來源_2 [4096]byte = *(*([4096]byte))(Pointer(資料指標))

	var i uint32 = 0
	for i = 0; i < 大小; i++ {
		buffer2_2[uint32(框架標頭大小)+i] = 來源_2[i]

	}

	var 位址參照 uintptr = uintptr(Pointer(&buffer2_2))

	self.網路紙牌.S送出(位址參照, 大小+uint32(框架標頭大小))

}
func (self *T共享媒介網路框提供器) Getmacaddress() uint64 {
	return self.網路紙牌.Getmacaddress()
}
func (self *T共享媒介網路框提供器) Getipaddress() uint64 {
	return self.網路紙牌.Getipaddress()
}
