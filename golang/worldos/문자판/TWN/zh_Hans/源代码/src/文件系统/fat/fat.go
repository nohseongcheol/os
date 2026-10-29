/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "工具"
import . "控制台"
import . "驱动程序/ata"
import . "文件系统/msdos分区"
import . "内存管理器"

type T文件系统参数32 struct {
	jmp			[3]uint8
	soft名称			[8]byte
	字节persector		uint16
	sectorspercluster	uint8
	保留的sectors		uint16
	fat复制			uint8
	根目录条目			uint16
	总数sectors		uint16
	介质类型			uint8
	fatsector计数		uint16
	sectorpertrack		uint16
	head计数			uint16
	隐藏sectors		uint32
	总数sector计数		uint32

	表格大小		uint32
	ext标志		uint16
	fat版本		uint16
	根cluster	uint32
	fat信息		uint16
	backupsector	uint16
	保留的0		[12]uint8
	drive数字		uint8
	保留的		uint8
	bootsignature	uint8
	音量id		uint32
	音量标签		[11]byte
	fat类型标签		[8]byte
}

func (self *T文件系统参数32) Init(数据 []byte) {
	copy(self.jmp[:3], 数据[0:3])
	copy(self.soft名称[:8], 数据[3:11])

	self.字节persector = (uint16(数据[11]) | uint16(数据[12])<<8)
	self.sectorspercluster = 数据[13]
	self.保留的sectors = (uint16(数据[14]) | uint16(数据[15])<<8)
	self.fat复制 = 数据[16]
	self.根目录条目 = (uint16(数据[17]) | uint16(数据[18])<<8)
	self.总数sectors = (uint16(数据[19]) | uint16(数据[20])<<8)
	self.介质类型 = 数据[21]
	self.fatsector计数 = (uint16(数据[22]) | uint16(数据[23])<<8)
	self.sectorpertrack = (uint16(数据[24]) | uint16(数据[25])<<8)
	self.head计数 = (uint16(数据[26]) | uint16(数据[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], 数据[28:32])
	self.隐藏sectors = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	copy(buffer1[:4], 数据[32:36])
	self.总数sector计数 = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	copy(buffer1[:4], 数据[36:40])
	self.表格大小 = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	self.ext标志 = (uint16(数据[40]) | uint16(数据[41])<<8)
	self.fat版本 = (uint16(数据[42]) | uint16(数据[43])<<8)

	copy(buffer1[:4], 数据[44:48])
	self.根cluster = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	self.fat信息 = (uint16(数据[48]) | uint16(数据[49])<<8)
	self.backupsector = (uint16(数据[50]) | uint16(数据[51])<<8)

	copy(self.保留的0[:12], 数据[52:64])

	self.drive数字 = 数据[64]
	self.保留的 = 数据[65]
	self.bootsignature = 数据[66]

	copy(buffer1[:4], 数据[67:71])
	self.音量id = Unsignedinteger32r(A数组tounsignedinteger32(buffer1))

	copy(self.音量标签[:11], 数据[71:82])
	copy(self.fat类型标签[:8], 数据[82:90])

}

var 控制台_2 = T控制台{}

func (self *T文件系统参数32) Len(hd *T高级技术attachment, part条目 T分区表格条目, 文件名 []byte) uint32 {

	if part条目.P分区id == 0x00 {
		return 0
	}

	内存管理器 := T内存管理器{}
	bpb指针 := 内存管理器.M分配内存(90)
	bpb字节 := Get字节from指针(uintptr(bpb指针), 90, 90)
	var 分区位移 = part条目.S开始lba

	hd.R读取28(分区位移, &bpb字节, 90)

	var 文件系统参数 = T文件系统参数32{}
	文件系统参数.Init(bpb字节)

	var fat开始 = 分区位移 + uint32(文件系统参数.保留的sectors)
	var fat大小 = 文件系统参数.表格大小

	var 数据开始 = fat开始 + fat大小*uint32(文件系统参数.fat复制)

	var 根开始 = 数据开始 + uint32(文件系统参数.sectorspercluster)*(文件系统参数.根cluster-2)

	dirent指针 := 内存管理器.M分配内存(512)
	dirent字节 := Get字节from指针(uintptr(dirent指针), 512, 512)
	hd.R读取28(根开始, &dirent字节, 512)

	var dirent = [16]T目录条目fat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], dirent字节[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名称[0] == 0x00 {
			break
		}

		if dirent[i].大小 >= 0xFFFFFFFF {
			continue
		}

		if !E相同字节(文件名, dirent[i].名称[:len(文件名)]) {
			continue
		}

		内存管理器.F空闲(bpb指针)
		内存管理器.F空闲(dirent指针)
		return dirent[i].大小
	}
	内存管理器.F空闲(bpb指针)
	内存管理器.F空闲(dirent指针)
	return 0
}
func (self *T文件系统参数32) R读取(hd *T高级技术attachment, part条目 T分区表格条目, 文件名 []byte, 数据 []byte) {

	if part条目.P分区id == 0x00 {
		return
	}

	内存管理器 := T内存管理器{}
	bpb指针 := 内存管理器.M分配内存(90)
	bpb字节 := Get字节from指针(uintptr(bpb指针), 90, 90)
	var 分区位移 = part条目.S开始lba

	hd.R读取28(分区位移, &bpb字节, 90)

	var 文件系统参数 = T文件系统参数32{}
	文件系统参数.Init(bpb字节)

	var fat开始 = 分区位移 + uint32(文件系统参数.保留的sectors)
	var fat大小 = 文件系统参数.表格大小

	var 数据开始 = fat开始 + fat大小*uint32(文件系统参数.fat复制)

	var 根开始 = 数据开始 + uint32(文件系统参数.sectorspercluster)*(文件系统参数.根cluster-2)

	dirent指针 := 内存管理器.M分配内存(512)
	dirent字节 := Get字节from指针(uintptr(dirent指针), 512, 512)
	hd.R读取28(根开始, &dirent字节, 512)

	var dirent = [16]T目录条目fat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], dirent字节[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名称[0] == 0x00 {
			break
		}

		if dirent[i].大小 >= 0xFFFFFFFF {
			continue
		}

		if !E相同字节(文件名, dirent[i].名称[:len(文件名)]) {
			continue
		}

		var first文件cluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstcluster低))

		var S大小 = int32(dirent[i].大小)
		var 下一个文件cluster = int32(first文件cluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for S大小 > 0 {
			var 文件sector = 数据开始 + uint32(文件系统参数.sectorspercluster)*uint32(下一个文件cluster-2)
			var sector位移 int = 0

			for ; S大小 > 0; S大小 -= 512 {

				var buffer3 []byte

				if dirent[i].大小 > 512 {
					buffer3 = buffer_2[:512]
					hd.R读取28(文件sector+uint32(sector位移), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].大小]
					hd.R读取28(文件sector+uint32(sector位移), &buffer3, int(dirent[i].大小))
				}

				copy(数据[int32(dirent[i].大小)-S大小:], buffer3)

				sector位移++

				if sector位移 > int(文件系统参数.sectorspercluster) {
					break
				}

			}

			var fatsectorfor当前cluster = uint32(下一个文件cluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.R读取28(fat开始+fatsectorfor当前cluster, &fatbuf, 512)

			var fat位移进sectorfor当前cluster = 下一个文件cluster % 128
			var 开始位移 = fat位移进sectorfor当前cluster * 4
			var 结尾位移 = fat位移进sectorfor当前cluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[开始位移:结尾位移])

			下一个文件cluster = int32(Unsignedinteger32r(A数组tounsignedinteger32(buffer4)))
		}
	}
	内存管理器.F空闲(bpb指针)
	内存管理器.F空闲(dirent指针)
}

type T目录条目fat32 struct {
	名称		[8]byte
	ext		[3]byte
	属性_2		uint8
	保留的		uint8
	c时间tenth	uint8
	c时间		uint16
	c日期		uint16
	a时间		uint16
	firstclusterhi	uint16
	w时间		uint16
	w日期		uint16
	firstcluster低	uint16
	大小		uint32
}

func (self *T目录条目fat32) Init(数据 [32]byte) {
	copy(self.名称[:8], 数据[0:8])
	copy(self.ext[:3], 数据[8:11])
	self.属性_2 = 数据[11]
	self.保留的 = 数据[12]
	self.c时间tenth = 数据[13]
	self.c时间 = uint16(数据[14]) | uint16(数据[15])<<8
	self.c日期 = uint16(数据[16]) | uint16(数据[17])<<8
	self.a时间 = uint16(数据[18]) | uint16(数据[19])<<8
	self.firstclusterhi = uint16(数据[20]) | uint16(数据[21])<<8
	self.w时间 = uint16(数据[22]) | uint16(数据[23])<<8
	self.w日期 = uint16(数据[24]) | uint16(数据[25])<<8
	self.firstcluster低 = uint16(数据[26]) | uint16(数据[27])<<8

	var buffer [4]byte
	copy(buffer[:4], 数据[28:32])
	self.大小 = Unsignedinteger32r(A数组tounsignedinteger32(buffer))
}
