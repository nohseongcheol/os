package fat

import . "工具"
import . "控制台"
import . "驅動程式/ata"
import . "檔案系統/msdos分割區"
import . "記憶體管理器"

type T檔案系統參數32 struct {
	jmp			[3]uint8
	soft名稱			[8]byte
	位元組persector		uint16
	sectorspercluster	uint8
	預留sectors		uint16
	fat複製			uint8
	根目錄目錄項目			uint16
	總數sectors		uint16
	媒體類型			uint8
	fatsector計數		uint16
	sectorpertrack		uint16
	head計數			uint16
	隱藏sectors		uint32
	總數sector計數		uint32

	table大小		uint32
	ext旗標		uint16
	fat版本		uint16
	根目錄cluster	uint32
	fat資訊		uint16
	backupsector	uint16
	預留0		[12]uint8
	drive數字		uint8
	預留		uint8
	bootsignature	uint8
	音量識別號		uint32
	音量標籤		[11]byte
	fat類型標籤		[8]byte
}

func (self *T檔案系統參數32) Init(資料 []byte) {
	copy(self.jmp[:3], 資料[0:3])
	copy(self.soft名稱[:8], 資料[3:11])

	self.位元組persector = (uint16(資料[11]) | uint16(資料[12])<<8)
	self.sectorspercluster = 資料[13]
	self.預留sectors = (uint16(資料[14]) | uint16(資料[15])<<8)
	self.fat複製 = 資料[16]
	self.根目錄目錄項目 = (uint16(資料[17]) | uint16(資料[18])<<8)
	self.總數sectors = (uint16(資料[19]) | uint16(資料[20])<<8)
	self.媒體類型 = 資料[21]
	self.fatsector計數 = (uint16(資料[22]) | uint16(資料[23])<<8)
	self.sectorpertrack = (uint16(資料[24]) | uint16(資料[25])<<8)
	self.head計數 = (uint16(資料[26]) | uint16(資料[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], 資料[28:32])
	self.隱藏sectors = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	copy(buffer1[:4], 資料[32:36])
	self.總數sector計數 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	copy(buffer1[:4], 資料[36:40])
	self.table大小 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	self.ext旗標 = (uint16(資料[40]) | uint16(資料[41])<<8)
	self.fat版本 = (uint16(資料[42]) | uint16(資料[43])<<8)

	copy(buffer1[:4], 資料[44:48])
	self.根目錄cluster = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	self.fat資訊 = (uint16(資料[48]) | uint16(資料[49])<<8)
	self.backupsector = (uint16(資料[50]) | uint16(資料[51])<<8)

	copy(self.預留0[:12], 資料[52:64])

	self.drive數字 = 資料[64]
	self.預留 = 資料[65]
	self.bootsignature = 資料[66]

	copy(buffer1[:4], 資料[67:71])
	self.音量識別號 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer1))

	copy(self.音量標籤[:11], 資料[71:82])
	copy(self.fat類型標籤[:8], 資料[82:90])

}

var 控制台_2 = T控制台{}

func (self *T檔案系統參數32) Len(hd *T進階科技attachment, part項目 T分割區table項目, 檔案名稱 []byte) uint32 {

	if part項目.P分割區識別號 == 0x00 {
		return 0
	}

	記憶體管理器 := T記憶體管理器{}
	bpb指標 := 記憶體管理器.M配置記憶體(90)
	bpb位元組 := Get位元組from指標(uintptr(bpb指標), 90, 90)
	var 分割區位移 = part項目.S啟動lba

	hd.R讀取28(分割區位移, &bpb位元組, 90)

	var 檔案系統參數 = T檔案系統參數32{}
	檔案系統參數.Init(bpb位元組)

	var fat啟動 = 分割區位移 + uint32(檔案系統參數.預留sectors)
	var fat大小 = 檔案系統參數.table大小

	var 資料啟動 = fat啟動 + fat大小*uint32(檔案系統參數.fat複製)

	var 根目錄啟動 = 資料啟動 + uint32(檔案系統參數.sectorspercluster)*(檔案系統參數.根目錄cluster-2)

	dirent指標 := 記憶體管理器.M配置記憶體(512)
	dirent位元組 := Get位元組from指標(uintptr(dirent指標), 512, 512)
	hd.R讀取28(根目錄啟動, &dirent位元組, 512)

	var dirent = [16]T目錄項目fat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], dirent位元組[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名稱[0] == 0x00 {
			break
		}

		if dirent[i].大小 >= 0xFFFFFFFF {
			continue
		}

		if !E相等位元組(檔案名稱, dirent[i].名稱[:len(檔案名稱)]) {
			continue
		}

		記憶體管理器.F剩餘(bpb指標)
		記憶體管理器.F剩餘(dirent指標)
		return dirent[i].大小
	}
	記憶體管理器.F剩餘(bpb指標)
	記憶體管理器.F剩餘(dirent指標)
	return 0
}
func (self *T檔案系統參數32) R讀取(hd *T進階科技attachment, part項目 T分割區table項目, 檔案名稱 []byte, 資料 []byte) {

	if part項目.P分割區識別號 == 0x00 {
		return
	}

	記憶體管理器 := T記憶體管理器{}
	bpb指標 := 記憶體管理器.M配置記憶體(90)
	bpb位元組 := Get位元組from指標(uintptr(bpb指標), 90, 90)
	var 分割區位移 = part項目.S啟動lba

	hd.R讀取28(分割區位移, &bpb位元組, 90)

	var 檔案系統參數 = T檔案系統參數32{}
	檔案系統參數.Init(bpb位元組)

	var fat啟動 = 分割區位移 + uint32(檔案系統參數.預留sectors)
	var fat大小 = 檔案系統參數.table大小

	var 資料啟動 = fat啟動 + fat大小*uint32(檔案系統參數.fat複製)

	var 根目錄啟動 = 資料啟動 + uint32(檔案系統參數.sectorspercluster)*(檔案系統參數.根目錄cluster-2)

	dirent指標 := 記憶體管理器.M配置記憶體(512)
	dirent位元組 := Get位元組from指標(uintptr(dirent指標), 512, 512)
	hd.R讀取28(根目錄啟動, &dirent位元組, 512)

	var dirent = [16]T目錄項目fat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], dirent位元組[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名稱[0] == 0x00 {
			break
		}

		if dirent[i].大小 >= 0xFFFFFFFF {
			continue
		}

		if !E相等位元組(檔案名稱, dirent[i].名稱[:len(檔案名稱)]) {
			continue
		}

		var first檔案cluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstcluster低))

		var S大小 = int32(dirent[i].大小)
		var 下一個檔案cluster = int32(first檔案cluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for S大小 > 0 {
			var 檔案sector = 資料啟動 + uint32(檔案系統參數.sectorspercluster)*uint32(下一個檔案cluster-2)
			var sector位移 int = 0

			for ; S大小 > 0; S大小 -= 512 {

				var buffer3 []byte

				if dirent[i].大小 > 512 {
					buffer3 = buffer_2[:512]
					hd.R讀取28(檔案sector+uint32(sector位移), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].大小]
					hd.R讀取28(檔案sector+uint32(sector位移), &buffer3, int(dirent[i].大小))
				}

				copy(資料[int32(dirent[i].大小)-S大小:], buffer3)

				sector位移++

				if sector位移 > int(檔案系統參數.sectorspercluster) {
					break
				}

			}

			var fatsectorfor目前cluster = uint32(下一個檔案cluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.R讀取28(fat啟動+fatsectorfor目前cluster, &fatbuf, 512)

			var fat位移進sectorfor目前cluster = 下一個檔案cluster % 128
			var 啟動位移 = fat位移進sectorfor目前cluster * 4
			var 結束位移 = fat位移進sectorfor目前cluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[啟動位移:結束位移])

			下一個檔案cluster = int32(Unsignedinteger32r(A陣列tounsignedinteger32(buffer4)))
		}
	}
	記憶體管理器.F剩餘(bpb指標)
	記憶體管理器.F剩餘(dirent指標)
}

type T目錄項目fat32 struct {
	名稱		[8]byte
	ext		[3]byte
	屬性_2		uint8
	預留		uint8
	c時間tenth	uint8
	c時間		uint16
	c日期		uint16
	a時間		uint16
	firstclusterhi	uint16
	w時間		uint16
	w日期		uint16
	firstcluster低	uint16
	大小		uint32
}

func (self *T目錄項目fat32) Init(資料 [32]byte) {
	copy(self.名稱[:8], 資料[0:8])
	copy(self.ext[:3], 資料[8:11])
	self.屬性_2 = 資料[11]
	self.預留 = 資料[12]
	self.c時間tenth = 資料[13]
	self.c時間 = uint16(資料[14]) | uint16(資料[15])<<8
	self.c日期 = uint16(資料[16]) | uint16(資料[17])<<8
	self.a時間 = uint16(資料[18]) | uint16(資料[19])<<8
	self.firstclusterhi = uint16(資料[20]) | uint16(資料[21])<<8
	self.w時間 = uint16(資料[22]) | uint16(資料[23])<<8
	self.w日期 = uint16(資料[24]) | uint16(資料[25])<<8
	self.firstcluster低 = uint16(資料[26]) | uint16(資料[27])<<8

	var buffer [4]byte
	copy(buffer[:4], 資料[28:32])
	self.大小 = Unsignedinteger32r(A陣列tounsignedinteger32(buffer))
}
