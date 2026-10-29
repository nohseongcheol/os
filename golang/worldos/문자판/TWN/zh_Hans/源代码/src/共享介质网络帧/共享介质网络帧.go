/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 共享介质网络帧

import . "控制台"

import . "amdam79c973"
import . "unsafe"
import . "工具"

var 以太网控制台 T控制台 = T控制台{}

type T以太网帧头部buffer struct {
	目的macbe	[6]byte
	源macbe		[6]byte
	以太网类型be	[2]byte
}

var 帧头部大小 int = 14

type T共享介质网络帧头 struct {
	目的macbe	uint64
	源macbe		uint64
	以太网类型be	uint16
}

func (self *T共享介质网络帧头) Init(buffer_2 T以太网帧头部buffer) {
	self.目的macbe = (A数组tounsignedinteger48(buffer_2.目的macbe))
	self.源macbe = (A数组tounsignedinteger48(buffer_2.源macbe))
	self.以太网类型be = (A数组tounsignedinteger16(buffer_2.以太网类型be))

}
func (self *T共享介质网络帧头) S集合buffer(buffer_2 *T以太网帧头部buffer) {
	buffer_2.目的macbe = Unsignedinteger48to数组(Unsignedinteger48r(self.目的macbe))
	buffer_2.源macbe = Unsignedinteger48to数组(Unsignedinteger48r(self.源macbe))
	buffer_2.以太网类型be = Unsignedinteger16to数组(Unsignedinteger16r(self.以太网类型be))
}

type I以太网帧handler interface {
	Init(backend T共享介质网络帧提供器)
	S集合handler(handler I以太网帧handler, 以太网类型 uint16)
	O以太网帧receivewhen(数据指针 uintptr, 大小 int) bool
	S发送(目的macbe uint64, 数据指针 uintptr, 大小 uint32)
	S帧发送(目的macbe uint64, 以太网类型be uint16, 数据指针 uintptr, 大小 uint32)
	Providerget() T共享介质网络帧提供器
	Getmacaddress() uint64
	Getipaddress() uint64
}

type T以太网帧handler struct {
}

var 帧 T共享介质网络帧头
var Backend T共享介质网络帧提供器
var handler_2 [65535]I以太网帧handler
var efhandler *T以太网帧handler = nil

func (self *T以太网帧handler) Init(backend T共享介质网络帧提供器) {
	Backend = backend
}

func (self *T以太网帧handler) S集合handler(handler I以太网帧handler, p以太网类型 uint16) {
	handler_2[p以太网类型] = handler
}
func (self *T以太网帧handler) S集合backend(backend T共享介质网络帧提供器) {
	Backend = backend
}
func (self *T以太网帧handler) Getbackend() T共享介质网络帧提供器 {
	return Backend
}
func (self *T以太网帧handler) O以太网帧receivewhen(数据指针 uintptr, 大小 int) bool {
	以太网控制台.M打印(([]byte)("OnEtherFrameReceived"))
	return false
}
func (self *T以太网帧handler) S发送(目的macbe uint64, 数据指针 uintptr, 大小 uint32) {
	Backend.S帧发送(目的macbe, 帧.以太网类型be, 数据指针, 大小)
}
func (self *T以太网帧handler) S帧发送(目的macbe uint64, 以太网类型be uint16, 数据指针 uintptr, 大小 uint32) {
	Backend.S帧发送(目的macbe, 以太网类型be, 数据指针, 大小)
}
func (self *T以太网帧handler) Getmacaddress() uint64 {
	return Backend.Getmacaddress()
}
func (self *T以太网帧handler) Getipaddress() uint64 {
	return Backend.Getipaddress()
}
func (self *T以太网帧handler) Providerget() T共享介质网络帧提供器 {
	return Backend
}

type T以太网帧raw数据handler struct {
	TRaw数据handler
}

var provider T共享介质网络帧提供器

func (self *T以太网帧raw数据handler) Init(pprovider T共享介质网络帧提供器, pbackend Tamdam79c973) {
	provider = pprovider
	provider.Init(pbackend)
}
func (self *T以太网帧raw数据handler) O时raw数据receive(数据指针 uintptr, 大小 int) bool {
	return provider.O时raw数据receive(数据指针, 大小)
}
func (self *T以太网帧raw数据handler) S发送(数据指针 uintptr, 大小 uint32) {
	provider.S发送(数据指针, 大小)
}
func (self *T以太网帧raw数据handler) Getmacaddress() uint64 {
	return provider.Getmacaddress()
}
func (self *T以太网帧raw数据handler) Getipaddress() uint64 {
	return provider.Getipaddress()
}
func (self *T以太网帧raw数据handler) Providerget() T共享介质网络帧提供器 {
	return provider
}

type T共享介质网络帧提供器 struct {
	网络纸牌类		Tamdam79c973
	handler_2	[65565]I以太网帧handler
}

func (self *T共享介质网络帧提供器) Init(backend Tamdam79c973) {

	self.网络纸牌类 = backend
	for i := 0; i < 65535; i++ {
		handler_2[i] = nil
		self.handler_2[i] = nil
	}
}

var 计数 uint16 = 0

func (self *T共享介质网络帧提供器) O时raw数据receive(数据指针 uintptr, 大小 int) bool {

	var buffer_2 *T以太网帧头部buffer = (*T以太网帧头部buffer)(Pointer(数据指针))
	var 帧 T共享介质网络帧头 = T共享介质网络帧头{}
	帧.Init(*buffer_2)
	var reply bool = false

	if 帧.目的macbe == 0x0000FFFFFFFFFFFF || Unsignedinteger48r(帧.目的macbe) == self.Getmacaddress() {
		if handler_2[帧.以太网类型be] != nil {
			以太网控制台.M打印(([]byte)("provider\n"))

			var 地址引用 uintptr = uintptr(Pointer(数据指针)) + uintptr(帧头部大小)
			reply = handler_2[帧.以太网类型be].O以太网帧receivewhen(地址引用, 大小-帧头部大小)

		}
	}

	if reply {
		帧.目的macbe = 帧.源macbe
		帧.源macbe = Unsignedinteger48r(self.Getmacaddress())
		帧.S集合buffer(buffer_2)

	}

	以太网控制台.M打印xy(([]byte)("spro["), 0, 1)
	以太网控制台.MUnsignedinteger64打印(帧.源macbe)
	以太网控制台.M打印(([]byte)(":"))
	以太网控制台.MUnsignedinteger64打印(帧.目的macbe)
	以太网控制台.M打印(([]byte)(":]["))
	以太网控制台.MUnsignedinteger64打印(self.Getmacaddress())
	以太网控制台.M打印(([]byte)(":"))
	以太网控制台.MUnsignedinteger16打印(帧.以太网类型be)
	以太网控制台.M打印(([]byte)("]"))

	return reply

}
func (self *T共享介质网络帧提供器) S发送(数据指针 uintptr, 大小 uint32) {
	self.网络纸牌类.S发送(数据指针, 大小)
}
func (self *T共享介质网络帧提供器) S帧发送(目的macbe uint64, 以太网类型be uint16, 数据指针 uintptr, 大小 uint32) {

	var buffer2_2 [4096]byte
	var buffer_2 *T以太网帧头部buffer = (*T以太网帧头部buffer)(Pointer(&buffer2_2))

	var 帧 T共享介质网络帧头 = T共享介质网络帧头{}
	帧.Init(*buffer_2)

	帧.目的macbe = Unsignedinteger48r(目的macbe)
	帧.源macbe = Unsignedinteger48r(self.网络纸牌类.Getmacaddress())
	帧.以太网类型be = Unsignedinteger16r(以太网类型be)

	帧.S集合buffer(buffer_2)
	var 源_2 [4096]byte = *(*([4096]byte))(Pointer(数据指针))

	var i uint32 = 0
	for i = 0; i < 大小; i++ {
		buffer2_2[uint32(帧头部大小)+i] = 源_2[i]

	}

	var 地址引用 uintptr = uintptr(Pointer(&buffer2_2))

	self.网络纸牌类.S发送(地址引用, 大小+uint32(帧头部大小))

}
func (self *T共享介质网络帧提供器) Getmacaddress() uint64 {
	return self.网络纸牌类.Getmacaddress()
}
func (self *T共享介质网络帧提供器) Getipaddress() uint64 {
	return self.网络纸牌类.Getipaddress()
}
