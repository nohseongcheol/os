package fat

import . "ハンヨウ"
import . "コンソール"
import . "ドライバー/ata"
import . "ファイルシステム/msdosクブン"
import . "メモリカンリシャ"

type Tファイルタイケイセッテイチ32 struct {
	jmp			[3]uint8
	softナマエ			[8]byte
	バイトpersector		uint16
	sectorspercluster	uint8
	ヨヤクsectors		uint16
	fatフクセイ			uint8
	ルートディレクトリentry		uint16
	ゴウケイsectors		uint16
	メディアカタ			uint8
	fatsectorカウント		uint16
	sectorpertrack		uint16
	headカウント		uint16
	ヒヒョウジsectors		uint32
	ゴウケイsectorカウント		uint32

	tableサイズ	uint32
	extフラグ		uint16
	fatバージョン	uint16
	ルートcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	ヨヤク0		[12]uint8
	drivenumber	uint8
	ヨヤク		uint8
	bootsignature	uint8
	オンリョウid		uint32
	オンリョウラベル		[11]byte
	fatカタラベル		[8]byte
}

func (self *Tファイルタイケイセッテイチ32) Init(データ []byte) {
	copy(self.jmp[:3], データ[0:3])
	copy(self.softナマエ[:8], データ[3:11])

	self.バイトpersector = (uint16(データ[11]) | uint16(データ[12])<<8)
	self.sectorspercluster = データ[13]
	self.ヨヤクsectors = (uint16(データ[14]) | uint16(データ[15])<<8)
	self.fatフクセイ = データ[16]
	self.ルートディレクトリentry = (uint16(データ[17]) | uint16(データ[18])<<8)
	self.ゴウケイsectors = (uint16(データ[19]) | uint16(データ[20])<<8)
	self.メディアカタ = データ[21]
	self.fatsectorカウント = (uint16(データ[22]) | uint16(データ[23])<<8)
	self.sectorpertrack = (uint16(データ[24]) | uint16(データ[25])<<8)
	self.headカウント = (uint16(データ[26]) | uint16(データ[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], データ[28:32])
	self.ヒヒョウジsectors = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	copy(buffer1[:4], データ[32:36])
	self.ゴウケイsectorカウント = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	copy(buffer1[:4], データ[36:40])
	self.tableサイズ = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	self.extフラグ = (uint16(データ[40]) | uint16(データ[41])<<8)
	self.fatバージョン = (uint16(データ[42]) | uint16(データ[43])<<8)

	copy(buffer1[:4], データ[44:48])
	self.ルートcluster = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	self.fatinfo = (uint16(データ[48]) | uint16(データ[49])<<8)
	self.backupsector = (uint16(データ[50]) | uint16(データ[51])<<8)

	copy(self.ヨヤク0[:12], データ[52:64])

	self.drivenumber = データ[64]
	self.ヨヤク = データ[65]
	self.bootsignature = データ[66]

	copy(buffer1[:4], データ[67:71])
	self.オンリョウid = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer1))

	copy(self.オンリョウラベル[:11], データ[71:82])
	copy(self.fatカタラベル[:8], データ[82:90])

}

var コンソール_2 = Tコンソール{}

func (self *Tファイルタイケイセッテイチ32) Len(hd *Tショウサイシヨウギジュツattachment, partentry Tクブンtableentry, ファイルメイ []byte) uint32 {

	if partentry.Pクブンid == 0x00 {
		return 0
	}

	メモリカンリシャ := Tメモリカンリシャ{}
	bpbポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(90)
	bpbバイト := Getバイトカラポインタ(uintptr(bpbポインタ), 90, 90)
	var クブンoffset = partentry.Sカイシlba

	hd.Rヨミコミ28(クブンoffset, &bpbバイト, 90)

	var ファイルタイケイセッテイチ = Tファイルタイケイセッテイチ32{}
	ファイルタイケイセッテイチ.Init(bpbバイト)

	var fatカイシ = クブンoffset + uint32(ファイルタイケイセッテイチ.ヨヤクsectors)
	var fatサイズ = ファイルタイケイセッテイチ.tableサイズ

	var データカイシ = fatカイシ + fatサイズ*uint32(ファイルタイケイセッテイチ.fatフクセイ)

	var ルートカイシ = データカイシ + uint32(ファイルタイケイセッテイチ.sectorspercluster)*(ファイルタイケイセッテイチ.ルートcluster-2)

	direntポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(512)
	direntバイト := Getバイトカラポインタ(uintptr(direntポインタ), 512, 512)
	hd.Rヨミコミ28(ルートカイシ, &direntバイト, 512)

	var dirent = [16]Tディレクトリentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntバイト[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ナマエ[0] == 0x00 {
			break
		}

		if dirent[i].サイズ >= 0xFFFFFFFF {
			continue
		}

		if !Eスベテオナジバイト(ファイルメイ, dirent[i].ナマエ[:len(ファイルメイ)]) {
			continue
		}

		メモリカンリシャ.Fアキ(bpbポインタ)
		メモリカンリシャ.Fアキ(direntポインタ)
		return dirent[i].サイズ
	}
	メモリカンリシャ.Fアキ(bpbポインタ)
	メモリカンリシャ.Fアキ(direntポインタ)
	return 0
}
func (self *Tファイルタイケイセッテイチ32) Rヨミコミ(hd *Tショウサイシヨウギジュツattachment, partentry Tクブンtableentry, ファイルメイ []byte, データ []byte) {

	if partentry.Pクブンid == 0x00 {
		return
	}

	メモリカンリシャ := Tメモリカンリシャ{}
	bpbポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(90)
	bpbバイト := Getバイトカラポインタ(uintptr(bpbポインタ), 90, 90)
	var クブンoffset = partentry.Sカイシlba

	hd.Rヨミコミ28(クブンoffset, &bpbバイト, 90)

	var ファイルタイケイセッテイチ = Tファイルタイケイセッテイチ32{}
	ファイルタイケイセッテイチ.Init(bpbバイト)

	var fatカイシ = クブンoffset + uint32(ファイルタイケイセッテイチ.ヨヤクsectors)
	var fatサイズ = ファイルタイケイセッテイチ.tableサイズ

	var データカイシ = fatカイシ + fatサイズ*uint32(ファイルタイケイセッテイチ.fatフクセイ)

	var ルートカイシ = データカイシ + uint32(ファイルタイケイセッテイチ.sectorspercluster)*(ファイルタイケイセッテイチ.ルートcluster-2)

	direntポインタ := メモリカンリシャ.Mキオクリョウイキヲカクホ(512)
	direntバイト := Getバイトカラポインタ(uintptr(direntポインタ), 512, 512)
	hd.Rヨミコミ28(ルートカイシ, &direntバイト, 512)

	var dirent = [16]Tディレクトリentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntバイト[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ナマエ[0] == 0x00 {
			break
		}

		if dirent[i].サイズ >= 0xFFFFFFFF {
			continue
		}

		if !Eスベテオナジバイト(ファイルメイ, dirent[i].ナマエ[:len(ファイルメイ)]) {
			continue
		}

		var firstファイルcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterヒクイ))

		var Sサイズ = int32(dirent[i].サイズ)
		var ツギファイルcluster = int32(firstファイルcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sサイズ > 0 {
			var ファイルsector = データカイシ + uint32(ファイルタイケイセッテイチ.sectorspercluster)*uint32(ツギファイルcluster-2)
			var sectoroffset int = 0

			for ; Sサイズ > 0; Sサイズ -= 512 {

				var buffer3 []byte

				if dirent[i].サイズ > 512 {
					buffer3 = buffer_2[:512]
					hd.Rヨミコミ28(ファイルsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].サイズ]
					hd.Rヨミコミ28(ファイルsector+uint32(sectoroffset), &buffer3, int(dirent[i].サイズ))
				}

				copy(データ[int32(dirent[i].サイズ)-Sサイズ:], buffer3)

				sectoroffset++

				if sectoroffset > int(ファイルタイケイセッテイチ.sectorspercluster) {
					break
				}

			}

			var fatsectorforゲンザイノニチジcluster = uint32(ツギファイルcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rヨミコミ28(fatカイシ+fatsectorforゲンザイノニチジcluster, &fatbuf, 512)

			var fatoffsetジュシンsectorforゲンザイノニチジcluster = ツギファイルcluster % 128
			var カイシoffset = fatoffsetジュシンsectorforゲンザイノニチジcluster * 4
			var ブンマツoffset = fatoffsetジュシンsectorforゲンザイノニチジcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[カイシoffset:ブンマツoffset])

			ツギファイルcluster = int32(Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer4)))
		}
	}
	メモリカンリシャ.Fアキ(bpbポインタ)
	メモリカンリシャ.Fアキ(direntポインタ)
}

type Tディレクトリentryfat32 struct {
	ナマエ		[8]byte
	ext		[3]byte
	ゾクセイ_2		uint8
	ヨヤク		uint8
	cジカンtenth	uint8
	cジカン		uint16
	cヒヅケ		uint16
	aジカン		uint16
	firstclusterhi	uint16
	wジカン		uint16
	wヒヅケ		uint16
	firstclusterヒクイ	uint16
	サイズ		uint32
}

func (self *Tディレクトリentryfat32) Init(データ [32]byte) {
	copy(self.ナマエ[:8], データ[0:8])
	copy(self.ext[:3], データ[8:11])
	self.ゾクセイ_2 = データ[11]
	self.ヨヤク = データ[12]
	self.cジカンtenth = データ[13]
	self.cジカン = uint16(データ[14]) | uint16(データ[15])<<8
	self.cヒヅケ = uint16(データ[16]) | uint16(データ[17])<<8
	self.aジカン = uint16(データ[18]) | uint16(データ[19])<<8
	self.firstclusterhi = uint16(データ[20]) | uint16(データ[21])<<8
	self.wジカン = uint16(データ[22]) | uint16(データ[23])<<8
	self.wヒヅケ = uint16(データ[24]) | uint16(データ[25])<<8
	self.firstclusterヒクイ = uint16(データ[26]) | uint16(データ[27])<<8

	var buffer [4]byte
	copy(buffer[:4], データ[28:32])
	self.サイズ = Unsignedinteger32r(Aハイレツtounsignedinteger32(buffer))
}
