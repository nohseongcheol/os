package fat

import . "汎用"
import . "コンソール"
import . "ドライバー/ata"
import . "ファイルシステム/msdos区分"
import . "メモリ管理者"

type Tファイル体系設定値32 struct {
	jmp			[3]uint8
	soft名前			[8]byte
	バイトpersector		uint16
	sectorspercluster	uint8
	予約sectors		uint16
	fat複製			uint8
	ルートディレクトリentry		uint16
	合計sectors		uint16
	メディア型			uint8
	fatsectorカウント		uint16
	sectorpertrack		uint16
	headカウント		uint16
	非表示sectors		uint32
	合計sectorカウント		uint32

	tableサイズ	uint32
	extフラグ		uint16
	fatバージョン	uint16
	ルートcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	予約0		[12]uint8
	drivenumber	uint8
	予約		uint8
	bootsignature	uint8
	音量id		uint32
	音量ラベル		[11]byte
	fat型ラベル		[8]byte
}

func (self *Tファイル体系設定値32) Init(データ []byte) {
	copy(self.jmp[:3], データ[0:3])
	copy(self.soft名前[:8], データ[3:11])

	self.バイトpersector = (uint16(データ[11]) | uint16(データ[12])<<8)
	self.sectorspercluster = データ[13]
	self.予約sectors = (uint16(データ[14]) | uint16(データ[15])<<8)
	self.fat複製 = データ[16]
	self.ルートディレクトリentry = (uint16(データ[17]) | uint16(データ[18])<<8)
	self.合計sectors = (uint16(データ[19]) | uint16(データ[20])<<8)
	self.メディア型 = データ[21]
	self.fatsectorカウント = (uint16(データ[22]) | uint16(データ[23])<<8)
	self.sectorpertrack = (uint16(データ[24]) | uint16(データ[25])<<8)
	self.headカウント = (uint16(データ[26]) | uint16(データ[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], データ[28:32])
	self.非表示sectors = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	copy(buffer1[:4], データ[32:36])
	self.合計sectorカウント = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	copy(buffer1[:4], データ[36:40])
	self.tableサイズ = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	self.extフラグ = (uint16(データ[40]) | uint16(データ[41])<<8)
	self.fatバージョン = (uint16(データ[42]) | uint16(データ[43])<<8)

	copy(buffer1[:4], データ[44:48])
	self.ルートcluster = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	self.fatinfo = (uint16(データ[48]) | uint16(データ[49])<<8)
	self.backupsector = (uint16(データ[50]) | uint16(データ[51])<<8)

	copy(self.予約0[:12], データ[52:64])

	self.drivenumber = データ[64]
	self.予約 = データ[65]
	self.bootsignature = データ[66]

	copy(buffer1[:4], データ[67:71])
	self.音量id = Unsignedinteger32r(A配列tounsignedinteger32(buffer1))

	copy(self.音量ラベル[:11], データ[71:82])
	copy(self.fat型ラベル[:8], データ[82:90])

}

var コンソール_2 = Tコンソール{}

func (self *Tファイル体系設定値32) Len(hd *T詳細使用技術attachment, partentry T区分tableentry, ファイル名 []byte) uint32 {

	if partentry.P区分id == 0x00 {
		return 0
	}

	メモリ管理者 := Tメモリ管理者{}
	bpbポインタ := メモリ管理者.M記憶領域を確保(90)
	bpbバイト := Getバイトからポインタ(uintptr(bpbポインタ), 90, 90)
	var 区分offset = partentry.S開始lba

	hd.R読込み28(区分offset, &bpbバイト, 90)

	var ファイル体系設定値 = Tファイル体系設定値32{}
	ファイル体系設定値.Init(bpbバイト)

	var fat開始 = 区分offset + uint32(ファイル体系設定値.予約sectors)
	var fatサイズ = ファイル体系設定値.tableサイズ

	var データ開始 = fat開始 + fatサイズ*uint32(ファイル体系設定値.fat複製)

	var ルート開始 = データ開始 + uint32(ファイル体系設定値.sectorspercluster)*(ファイル体系設定値.ルートcluster-2)

	direntポインタ := メモリ管理者.M記憶領域を確保(512)
	direntバイト := Getバイトからポインタ(uintptr(direntポインタ), 512, 512)
	hd.R読込み28(ルート開始, &direntバイト, 512)

	var dirent = [16]Tディレクトリentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntバイト[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名前[0] == 0x00 {
			break
		}

		if dirent[i].サイズ >= 0xFFFFFFFF {
			continue
		}

		if !Eすべて同じバイト(ファイル名, dirent[i].名前[:len(ファイル名)]) {
			continue
		}

		メモリ管理者.F空き(bpbポインタ)
		メモリ管理者.F空き(direntポインタ)
		return dirent[i].サイズ
	}
	メモリ管理者.F空き(bpbポインタ)
	メモリ管理者.F空き(direntポインタ)
	return 0
}
func (self *Tファイル体系設定値32) R読込み(hd *T詳細使用技術attachment, partentry T区分tableentry, ファイル名 []byte, データ []byte) {

	if partentry.P区分id == 0x00 {
		return
	}

	メモリ管理者 := Tメモリ管理者{}
	bpbポインタ := メモリ管理者.M記憶領域を確保(90)
	bpbバイト := Getバイトからポインタ(uintptr(bpbポインタ), 90, 90)
	var 区分offset = partentry.S開始lba

	hd.R読込み28(区分offset, &bpbバイト, 90)

	var ファイル体系設定値 = Tファイル体系設定値32{}
	ファイル体系設定値.Init(bpbバイト)

	var fat開始 = 区分offset + uint32(ファイル体系設定値.予約sectors)
	var fatサイズ = ファイル体系設定値.tableサイズ

	var データ開始 = fat開始 + fatサイズ*uint32(ファイル体系設定値.fat複製)

	var ルート開始 = データ開始 + uint32(ファイル体系設定値.sectorspercluster)*(ファイル体系設定値.ルートcluster-2)

	direntポインタ := メモリ管理者.M記憶領域を確保(512)
	direntバイト := Getバイトからポインタ(uintptr(direntポインタ), 512, 512)
	hd.R読込み28(ルート開始, &direntバイト, 512)

	var dirent = [16]Tディレクトリentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntバイト[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].名前[0] == 0x00 {
			break
		}

		if dirent[i].サイズ >= 0xFFFFFFFF {
			continue
		}

		if !Eすべて同じバイト(ファイル名, dirent[i].名前[:len(ファイル名)]) {
			continue
		}

		var firstファイルcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstcluster低い))

		var Sサイズ = int32(dirent[i].サイズ)
		var 次ファイルcluster = int32(firstファイルcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sサイズ > 0 {
			var ファイルsector = データ開始 + uint32(ファイル体系設定値.sectorspercluster)*uint32(次ファイルcluster-2)
			var sectoroffset int = 0

			for ; Sサイズ > 0; Sサイズ -= 512 {

				var buffer3 []byte

				if dirent[i].サイズ > 512 {
					buffer3 = buffer_2[:512]
					hd.R読込み28(ファイルsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].サイズ]
					hd.R読込み28(ファイルsector+uint32(sectoroffset), &buffer3, int(dirent[i].サイズ))
				}

				copy(データ[int32(dirent[i].サイズ)-Sサイズ:], buffer3)

				sectoroffset++

				if sectoroffset > int(ファイル体系設定値.sectorspercluster) {
					break
				}

			}

			var fatsectorfor現在の日時cluster = uint32(次ファイルcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.R読込み28(fat開始+fatsectorfor現在の日時cluster, &fatbuf, 512)

			var fatoffset受信sectorfor現在の日時cluster = 次ファイルcluster % 128
			var 開始offset = fatoffset受信sectorfor現在の日時cluster * 4
			var 文末offset = fatoffset受信sectorfor現在の日時cluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[開始offset:文末offset])

			次ファイルcluster = int32(Unsignedinteger32r(A配列tounsignedinteger32(buffer4)))
		}
	}
	メモリ管理者.F空き(bpbポインタ)
	メモリ管理者.F空き(direntポインタ)
}

type Tディレクトリentryfat32 struct {
	名前		[8]byte
	ext		[3]byte
	属性_2		uint8
	予約		uint8
	c時間tenth	uint8
	c時間		uint16
	c日付		uint16
	a時間		uint16
	firstclusterhi	uint16
	w時間		uint16
	w日付		uint16
	firstcluster低い	uint16
	サイズ		uint32
}

func (self *Tディレクトリentryfat32) Init(データ [32]byte) {
	copy(self.名前[:8], データ[0:8])
	copy(self.ext[:3], データ[8:11])
	self.属性_2 = データ[11]
	self.予約 = データ[12]
	self.c時間tenth = データ[13]
	self.c時間 = uint16(データ[14]) | uint16(データ[15])<<8
	self.c日付 = uint16(データ[16]) | uint16(データ[17])<<8
	self.a時間 = uint16(データ[18]) | uint16(データ[19])<<8
	self.firstclusterhi = uint16(データ[20]) | uint16(データ[21])<<8
	self.w時間 = uint16(データ[22]) | uint16(データ[23])<<8
	self.w日付 = uint16(データ[24]) | uint16(データ[25])<<8
	self.firstcluster低い = uint16(データ[26]) | uint16(データ[27])<<8

	var buffer [4]byte
	copy(buffer[:4], データ[28:32])
	self.サイズ = Unsignedinteger32r(A配列tounsignedinteger32(buffer))
}
