/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 使用者資料報協定

import . "unsafe"
import . "控制台"
import . "工具"
import . "記憶體管理器"
import . "互聯網路協定4"

var udp控制台 = T控制台{}

type T使用者datagramprotocol標頭buffer struct {
	來源通訊埠號		[2]byte
	目的通訊埠號	[2]byte

	長度		[2]byte
	checksum	[2]byte
}

var udp標頭大小 uint32 = 8

type T使用者資料報標頭 struct {
	來源通訊埠號		uint16
	目的通訊埠號	uint16

	長度		uint16
	checksum	uint16
}

func (self *T使用者資料報標頭) Init(buffer_2 *T使用者datagramprotocol標頭buffer) {
	self.來源通訊埠號 = A陣列tounsignedinteger16(buffer_2.來源通訊埠號)
	self.目的通訊埠號 = A陣列tounsignedinteger16(buffer_2.目的通訊埠號)

	self.長度 = A陣列tounsignedinteger16(buffer_2.長度)
	self.checksum = A陣列tounsignedinteger16(buffer_2.checksum)
}
func (self *T使用者資料報標頭) S設定buffer(buffer_2 *T使用者datagramprotocol標頭buffer) {

	buffer_2.來源通訊埠號 = Unsignedinteger16to陣列(self.來源通訊埠號)
	buffer_2.目的通訊埠號 = Unsignedinteger16to陣列(self.目的通訊埠號)

	buffer_2.長度 = Unsignedinteger16to陣列(self.長度)
	buffer_2.checksum = Unsignedinteger16to陣列(self.checksum)

}

type I使用者datagramprotocolhandler interface {
	H控制把使用者datagramprotocol訊息(通訊端 *T使用者資料報通訊端點, 資料 uintptr, 大小 uint16)
}

type T使用者datagramprotocolhandler struct {
}

func (self *T使用者datagramprotocolhandler) Init(backend T互聯網路協定提供器) {
}
func (self *T使用者datagramprotocolhandler) H控制把使用者datagramprotocol訊息(通訊端 *T使用者資料報通訊端點, 資料 uintptr, 大小 uint16) {
}

type I使用者datagramprotocol通訊端 interface {
	H控制把使用者datagramprotocol訊息(資料 uintptr, 大小 uint16)
}
type T使用者資料報通訊端點 struct {
	遠端連接埠數字	uint16
	遠端ip	uint32
	本地連接埠數字	uint16
	本地ip	uint32

	listening	bool
}

var udpprovider T使用者datagramprotocolprovider
var udphandler I使用者datagramprotocolhandler

func (self *T使用者資料報通訊端點) T測試() {
}
func (self *T使用者資料報通訊端點) Init(pudpprovider T使用者datagramprotocolprovider, pudphandler I使用者datagramprotocolhandler) {
	udpprovider = pudpprovider
	if udphandler == nil && pudphandler != nil {
		udphandler = pudphandler
	}
	self.listening = false
}
func (self *T使用者資料報通訊端點) H控制把使用者datagramprotocol訊息(資料 uintptr, 大小 uint16) {
	if udphandler != nil {
		udphandler.H控制把使用者datagramprotocol訊息(self, 資料, 大小)
	}
}
func (self *T使用者資料報通訊端點) S送出(p資料 []byte, 大小 uint16) {
	var buffer_2 [4096]byte
	for i := 0; i < int(大小); i++ {
		buffer_2[i] = p資料[i]
	}
	var 資料 = uintptr(Pointer(&buffer_2))
	udpprovider.S送出(self, 資料, 大小)
}
func (self *T使用者資料報通訊端點) D斷線() {
	udpprovider.D斷線(self)
}

type T使用者datagramprotocolprovider struct {
}

var iphandler I互聯網protocolhandler
var sockets [65535]T使用者資料報通訊端點
var 數字sockets int
var 剩餘連接埠 uint16

func (self *T使用者datagramprotocolprovider) Init(pipprovider T互聯網路協定提供器, piphandler I互聯網protocolhandler) {
	iphandler = piphandler
	iphandler.Init(pipprovider, piphandler, 0x11)
	數字sockets = 0
	剩餘連接埠 = 1024
}
func (self *T使用者datagramprotocolprovider) O互聯網protocolreceivewhen(來源ipaddress網路位元組order uint32, 目的地ipaddress網路位元組order uint32, 互聯網protocolpayload uintptr, 大小 uint32) bool {
	if 大小 < udp標頭大小 {
		return false
	}

	var buffer_2 *T使用者datagramprotocol標頭buffer = (*T使用者datagramprotocol標頭buffer)(Pointer(互聯網protocolpayload))
	var msg T使用者資料報標頭
	msg.Init(buffer_2)

	var 通訊端 *T使用者資料報通訊端點 = nil

	for i := 0; i < 數字sockets && 通訊端 == nil; i++ {
		if sockets[i].本地連接埠數字 == msg.目的通訊埠號 && sockets[i].本地ip == 目的地ipaddress網路位元組order && sockets[i].listening == true {
			通訊端 = &sockets[i]
			通訊端.listening = false
			通訊端.遠端連接埠數字 = msg.來源通訊埠號
			通訊端.遠端ip = 來源ipaddress網路位元組order
		} else if sockets[i].本地連接埠數字 == msg.目的通訊埠號 && sockets[i].本地ip == 目的地ipaddress網路位元組order && sockets[i].遠端連接埠數字 == msg.來源通訊埠號 && sockets[i].遠端ip == 來源ipaddress網路位元組order {
			通訊端 = &sockets[i]

		}
	}

	msg.S設定buffer(buffer_2)
	if 通訊端 != nil {
		通訊端.H控制把使用者datagramprotocol訊息(互聯網protocolpayload+uintptr(udp標頭大小), uint16(大小-udp標頭大小))
	}

	return false
}

func (self *T使用者datagramprotocolprovider) C連接(ip uint32, 連接埠 uint16) *T使用者資料報通訊端點 {
	var 記憶體管理器 = &T記憶體管理器{}
	var 通訊端 = (*T使用者資料報通訊端點)(記憶體管理器.M配置記憶體(50))

	if 通訊端 != nil {

		通訊端.Init(*self, nil)
		通訊端.遠端連接埠數字 = 連接埠
		通訊端.遠端ip = ip
		通訊端.本地連接埠數字 = 剩餘連接埠
		剩餘連接埠++
		通訊端.本地ip = uint32((*iphandler.Providerget()).Getipaddress())

		通訊端.遠端連接埠數字 = Unsignedinteger16r(通訊端.遠端連接埠數字)
		通訊端.本地連接埠數字 = Unsignedinteger16r(通訊端.本地連接埠數字)

		sockets[數字sockets] = *通訊端
		數字sockets++

	}
	return 通訊端

}
func (self *T使用者datagramprotocolprovider) Listen(連接埠 uint16) *T使用者資料報通訊端點 {
	var 通訊端 = &T使用者資料報通訊端點{}
	通訊端 = nil
	if 通訊端 != nil {
		通訊端.Init(*self, nil)
		通訊端.listening = true
		通訊端.本地連接埠數字 = 連接埠
		通訊端.本地ip = uint32((*iphandler.Providerget()).Getipaddress())

		通訊端.本地連接埠數字 = Unsignedinteger16r(通訊端.本地連接埠數字)
	}
	return 通訊端
}
func (self *T使用者datagramprotocolprovider) D斷線(通訊端 *T使用者資料報通訊端點) {
	for i := 0; i < 數字sockets && 通訊端 == nil; i++ {
		if sockets[i] == *通訊端 {
			數字sockets--
			sockets[i] = sockets[數字sockets]
			break
		}
	}
}
func (self *T使用者datagramprotocolprovider) S送出(通訊端 *T使用者資料報通訊端點, p資料 uintptr, 大小 uint16) {
	var 總數長度 = uint32(大小) + udp標頭大小

	var buffer_2 [4096]byte

	var msgbuffer = (*T使用者datagramprotocol標頭buffer)(Pointer(&buffer_2))

	var msg = T使用者資料報標頭{}

	msg.來源通訊埠號 = 通訊端.本地連接埠數字
	msg.目的通訊埠號 = 通訊端.遠端連接埠數字
	msg.長度 = Unsignedinteger16r(uint16(總數長度))

	msg.checksum = 0x0
	msg.S設定buffer(msgbuffer)

	var 資料位元組 [4096]byte = *(*[4096]byte)(Pointer(p資料))
	for i := 0; i < int(大小); i++ {
		buffer_2[int(udp標頭大小)+i] = 資料位元組[i]
	}

	var 資料 uintptr = uintptr(Pointer(&buffer_2))

	iphandler.S送出(通訊端.遠端ip, 0x11, 資料, 總數長度)

}
func (self *T使用者datagramprotocolprovider) Bind(通訊端 *T使用者資料報通訊端點, handler *T使用者datagramprotocolhandler) {
}
