/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package arp

import . "unsafe"
import . "консоль"
import . "кадр_мережі_зі_спільним_середовищем"
import . "util"

var arpКонсоль TКонсоль = TКонсоль{}

type ArpПовідомленняbuffer struct {
	пристроїТип		[2]byte
	protocol		[2]byte
	пристроїАдресаРозмір	byte
	protocolАдресаРозмір	byte
	команда			[2]byte

	джерелоmacАдреса	[6]byte
	джерелоipАдреса		[4]byte
	призначенняmacАдреса	[6]byte
	призначенняipАдреса	[4]byte
}

var arpmesgРозмір uint32 = (64+92+64)/8 + 2

type ArpПовідомлення struct {
	пристроїТип		uint16
	protocol		uint16
	пристроїАдресаРозмір	uint8
	protocolАдресаРозмір	uint8
	команда			uint16

	джерелоmacАдреса	uint64
	джерелоipАдреса		uint32
	призначенняmacАдреса	uint64
	призначенняipАдреса	uint32
}

func (поточний *ArpПовідомлення) Init(buffer_2 *ArpПовідомленняbuffer) {

	поточний.пристроїТип = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.пристроїТип))
	поточний.protocol = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.protocol))
	поточний.пристроїАдресаРозмір = byte(buffer_2.пристроїАдресаРозмір)
	поточний.protocolАдресаРозмір = byte(buffer_2.protocolАдресаРозмір)
	поточний.команда = Unsignedinteger16r(Масивтоunsignedinteger16(buffer_2.команда))

	поточний.джерелоmacАдреса = Unsignedinteger48r(Масивтоunsignedinteger48(buffer_2.джерелоmacАдреса))
	поточний.джерелоipАдреса = Unsignedinteger32r(Масивтоunsignedinteger32(buffer_2.джерелоipАдреса))
	поточний.призначенняmacАдреса = Unsignedinteger48r(Масивтоunsignedinteger48(buffer_2.призначенняmacАдреса))
	поточний.призначенняipАдреса = Unsignedinteger32r(Масивтоunsignedinteger32(buffer_2.призначенняipАдреса))
}
func (поточний *ArpПовідомлення) Множинаbuffer(buffer_2 *ArpПовідомленняbuffer) {
	buffer_2.пристроїТип = Unsignedinteger16тоМасив(поточний.пристроїТип)
	buffer_2.protocol = Unsignedinteger16тоМасив(поточний.protocol)
	buffer_2.пристроїАдресаРозмір = uint8(поточний.пристроїАдресаРозмір)
	buffer_2.protocolАдресаРозмір = uint8(поточний.protocolАдресаРозмір)

	buffer_2.команда = Unsignedinteger16тоМасив(поточний.команда)
	buffer_2.джерелоmacАдреса = Unsignedinteger48тоМасив(поточний.джерелоmacАдреса)
	buffer_2.джерелоipАдреса = Unsignedinteger32тоМасив(поточний.джерелоipАдреса)
	buffer_2.призначенняmacАдреса = Unsignedinteger48тоМасив(поточний.призначенняmacАдреса)
	buffer_2.призначенняipАдреса = Unsignedinteger32тоМасив(поточний.призначенняipАдреса)
}

type ArpethernetБлокhandler struct {
	TEthernetБлокhandler
}

var arpprovider Arpprovider
var постачальник_кадрів_мережі_зі_спільним_середовищем TПостачальник_кадрів_мережі_зі_спільним_середовищем

func (поточний *ArpethernetБлокhandler) EthernetБлокreceivewhen(dataВказівник uintptr, розмір int) bool {
	arpКонсоль.MДрукxy([]byte("arp recv:"), 0, 23)
	return arpprovider.EthernetБлокreceivewhen(dataВказівник, uint32(розмір))

}
func (поточний *ArpethernetБлокhandler) Надіслати(призначенняmacbe uint64, dataВказівник uintptr, розмір uint32) {
	arpКонсоль.MДрукxy([]byte("arp send:"), 0, 24)
	var ethernetТипbe = Unsignedinteger16r(0x0806)
	поточний.TEthernetБлокhandler.БлокНадіслати(призначенняmacbe, ethernetТипbe, dataВказівник, розмір)
}

type Arpprovider struct {
	Ipcache		[128]uint32
	Maccache	[128]uint64
	числоcacheзапис	int

	handler	IEthernetБлокhandler
}

var handler IEthernetБлокhandler

func (поточний *Arpprovider) Init(backend TПостачальник_кадрів_мережі_зі_спільним_середовищем, userhandler IEthernetБлокhandler) {

	handler = userhandler
	handler.Init(backend)
	handler.Множинаhandler(userhandler, 0x0806)
	поточний.числоcacheзапис = 0
	arpprovider = *поточний

}

func (поточний *Arpprovider) EthernetБлокreceivewhen(dataВказівник uintptr, розмір uint32) bool {

	if розмір < arpmesgРозмір {
		return false
	}
	var arpbuffer *ArpПовідомленняbuffer = (*ArpПовідомленняbuffer)(Pointer(dataВказівник))
	var arp ArpПовідомлення = ArpПовідомлення{}
	arp.Init(arpbuffer)

	if arp.пристроїТип == 0x0100 {

		if arp.protocol == 0x0008 && arp.пристроїАдресаРозмір == 6 && arp.protocolАдресаРозмір == 4 && uint64(arp.призначенняipАдреса) == handler.GetipАдреса() {

			arpКонсоль.MДрук([]byte("arp onetherframe"))
			arpКонсоль.MUnsignedinteger16Друк(arp.protocol)
			arpКонсоль.MДрук([]byte(":"))
			arpКонсоль.MUnsignedinteger64Друк(uint64(arp.призначенняmacАдреса))
			arpКонсоль.MДрук([]byte(":"))
			arpКонсоль.MUnsignedinteger16Друк(arp.команда)
			arpКонсоль.MДрук([]byte(":"))
			arpКонсоль.MUnsignedinteger64Друк(handler.GetmacАдреса())

			switch arp.команда {
			case 0x0100:

				if поточний.Getmacзcache(arp.джерелоipАдреса) == 0xFFFFFFFFFFFF {
					if поточний.числоcacheзапис < 128 {
						поточний.Ipcache[поточний.числоcacheзапис] = arp.джерелоipАдреса
						поточний.Maccache[поточний.числоcacheзапис] = arp.джерелоmacАдреса
						поточний.числоcacheзапис++
					}
				}
				arp.команда = 0x0200
				arp.призначенняipАдреса = arp.джерелоipАдреса
				arp.призначенняmacАдреса = arp.джерелоmacАдреса
				arp.джерелоipАдреса = uint32(handler.GetipАдреса())
				arp.джерелоmacАдреса = handler.GetmacАдреса()
				arp.Множинаbuffer(arpbuffer)

				return true
				break

			case 0x0200:
				arpКонсоль.MДрук(([]byte)("self.numCacheEntries"))

				if поточний.числоcacheзапис < 128 {
					поточний.Ipcache[поточний.числоcacheзапис] = arp.джерелоipАдреса
					поточний.Maccache[поточний.числоcacheзапис] = arp.джерелоmacАдреса
					поточний.числоcacheзапис++
				}
				break
			}

		}
	}
	return false

}

func (поточний *Arpprovider) BroadcastmacАдреса(IpМережаbyteorder uint32) {

	var arp ArpПовідомлення = ArpПовідомлення{}
	arp.пристроїТип = 0x0100
	arp.protocol = 0x0008
	arp.пристроїАдресаРозмір = 6
	arp.protocolАдресаРозмір = 4
	arp.команда = 0x0200

	arp.джерелоipАдреса = uint32(handler.GetipАдреса())

	arp.призначенняmacАдреса = поточний.Resolve(IpМережаbyteorder)
	arp.призначенняipАдреса = IpМережаbyteorder
	arpКонсоль.MДрукxy([]byte("broad mac"), 0, 15)

	arp.джерелоmacАдреса = handler.GetmacАдреса()

	var arpbuffer ArpПовідомленняbuffer = ArpПовідомленняbuffer{}
	arp.Множинаbuffer(&arpbuffer)

	var посилання_на_адресу uintptr = uintptr(Pointer(&arpbuffer))
	handler.Надіслати(arp.призначенняmacАдреса, посилання_на_адресу, arpmesgРозмір)
}
func (поточний *Arpprovider) RequestmacАдреса(IpМережаbyteorder uint32) {

	var arp ArpПовідомлення = ArpПовідомлення{}
	arp.пристроїТип = 0x0100

	arp.protocol = 0x0008
	arp.пристроїАдресаРозмір = 6
	arp.protocolАдресаРозмір = 4
	arp.команда = 0x0100

	arp.джерелоmacАдреса = handler.GetmacАдреса()
	arp.джерелоipАдреса = uint32(handler.GetipАдреса())

	arp.призначенняmacАдреса = 0xFFFFFFFFFFFF
	arp.призначенняipАдреса = IpМережаbyteorder

	var arpbuffer ArpПовідомленняbuffer = ArpПовідомленняbuffer{}
	arp.Множинаbuffer(&arpbuffer)

	var посилання_на_адресу uintptr = uintptr(Pointer(&arpbuffer))
	handler.Надіслати(arp.призначенняmacАдреса, посилання_на_адресу, arpmesgРозмір)
}
func (поточний *Arpprovider) ТестДрук(data *[]byte, розмір uint32) {
	var buffer_2 [4096]byte = *(*([4096]byte))(Pointer(data))
	arpКонсоль.MДрукxy([]byte("["), 0, 17)
	for i := 0; i < 128; i++ {
		arpКонсоль.MHexadecimalДрук(buffer_2[i])
		arpКонсоль.MДрук([]byte(":"))
	}
	arpКонсоль.MДрук([]byte("]"))
}

func (поточний *Arpprovider) Getmacзcache(IpМережаbyteorder uint32) uint64 {
	for i := 0; i < поточний.числоcacheзапис; i++ {
		for ipidx := 0; ipidx < 4; ipidx++ {

		}

		for macidx := 0; macidx < 6; macidx++ {

		}

		arpКонсоль.MДрук(([]byte)("["))
		arpКонсоль.MUnsignedinteger32Друк(поточний.Ipcache[i])
		arpКонсоль.MДрук(([]byte)(":"))
		arpКонсоль.MUnsignedinteger32Друк(IpМережаbyteorder)
		arpКонсоль.MДрук(([]byte)(":"))
		arpКонсоль.MДрук(([]byte)(":"))
		arpКонсоль.MUnsignedinteger64Друк(поточний.Maccache[i])
		arpКонсоль.MДрук(([]byte)("]\n"))

		if поточний.Ipcache[i] == IpМережаbyteorder {
			arpКонсоль.MДрук([]byte("getmacfromcache"))
			return поточний.Maccache[i]
		}
	}
	return 0xFFFFFFFFFFFF
}
func (поточний *Arpprovider) Resolve(IpМережаbyteorder uint32) uint64 {
	var яРЛИК uint64 = поточний.Getmacзcache(IpМережаbyteorder)
	if яРЛИК == 0xFFFFFFFFFFFF {
		поточний.RequestmacАдреса(IpМережаbyteorder)
	}
	for i := 0; i < 128 && яРЛИК == 0xFFFFFFFFFFFF; i++ {
		яРЛИК = поточний.Getmacзcache(IpМережаbyteorder)

	}

	return яРЛИК
}
