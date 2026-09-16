/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "はんよう"
import . "こんそーる"
import . "どらいばー/ata"
import . "ふぁいるしすてむ/msdosくぶん"
import . "めもりかんりしゃ"

type Tふぁいるたいけいせっていち32 struct {
	jmp			[3]uint8
	softなまえ			[8]byte
	ばいとpersector		uint16
	sectorspercluster	uint8
	よやくsectors		uint16
	fatふくせい			uint8
	るーとでぃれくとりentry		uint16
	ごうけいsectors		uint16
	めでぃあかた			uint8
	fatsectorかうんと		uint16
	sectorpertrack		uint16
	headかうんと		uint16
	ひひょうじsectors		uint32
	ごうけいsectorかうんと		uint32

	tableさいず	uint32
	extふらぐ		uint16
	fatばーじょん	uint16
	るーとcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	よやく0		[12]uint8
	drivenumber	uint8
	よやく		uint8
	bootsignature	uint8
	おんりょうid		uint32
	おんりょうらべる		[11]byte
	fatかたらべる		[8]byte
}

func (self *Tふぁいるたいけいせっていち32) Init(でーた []byte) {
	copy(self.jmp[:3], でーた[0:3])
	copy(self.softなまえ[:8], でーた[3:11])

	self.ばいとpersector = (uint16(でーた[11]) | uint16(でーた[12])<<8)
	self.sectorspercluster = でーた[13]
	self.よやくsectors = (uint16(でーた[14]) | uint16(でーた[15])<<8)
	self.fatふくせい = でーた[16]
	self.るーとでぃれくとりentry = (uint16(でーた[17]) | uint16(でーた[18])<<8)
	self.ごうけいsectors = (uint16(でーた[19]) | uint16(でーた[20])<<8)
	self.めでぃあかた = でーた[21]
	self.fatsectorかうんと = (uint16(でーた[22]) | uint16(でーた[23])<<8)
	self.sectorpertrack = (uint16(でーた[24]) | uint16(でーた[25])<<8)
	self.headかうんと = (uint16(でーた[26]) | uint16(でーた[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], でーた[28:32])
	self.ひひょうじsectors = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	copy(buffer1[:4], でーた[32:36])
	self.ごうけいsectorかうんと = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	copy(buffer1[:4], でーた[36:40])
	self.tableさいず = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	self.extふらぐ = (uint16(でーた[40]) | uint16(でーた[41])<<8)
	self.fatばーじょん = (uint16(でーた[42]) | uint16(でーた[43])<<8)

	copy(buffer1[:4], でーた[44:48])
	self.るーとcluster = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	self.fatinfo = (uint16(でーた[48]) | uint16(でーた[49])<<8)
	self.backupsector = (uint16(でーた[50]) | uint16(でーた[51])<<8)

	copy(self.よやく0[:12], でーた[52:64])

	self.drivenumber = でーた[64]
	self.よやく = でーた[65]
	self.bootsignature = でーた[66]

	copy(buffer1[:4], でーた[67:71])
	self.おんりょうid = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer1))

	copy(self.おんりょうらべる[:11], でーた[71:82])
	copy(self.fatかたらべる[:8], でーた[82:90])

}

var こんそーる_2 = Tこんそーる{}

func (self *Tふぁいるたいけいせっていち32) Len(hd *Tしょうさいしようぎじゅつattachment, partentry Tくぶんtableentry, ふぁいるめい []byte) uint32 {

	if partentry.Pくぶんid == 0x00 {
		return 0
	}

	めもりかんりしゃ := Tめもりかんりしゃ{}
	bpbぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(90)
	bpbばいと := Getばいとからぽいんた(uintptr(bpbぽいんた), 90, 90)
	var くぶんoffset = partentry.Sかいしlba

	hd.Rよみこみ28(くぶんoffset, &bpbばいと, 90)

	var ふぁいるたいけいせっていち = Tふぁいるたいけいせっていち32{}
	ふぁいるたいけいせっていち.Init(bpbばいと)

	var fatかいし = くぶんoffset + uint32(ふぁいるたいけいせっていち.よやくsectors)
	var fatさいず = ふぁいるたいけいせっていち.tableさいず

	var でーたかいし = fatかいし + fatさいず*uint32(ふぁいるたいけいせっていち.fatふくせい)

	var るーとかいし = でーたかいし + uint32(ふぁいるたいけいせっていち.sectorspercluster)*(ふぁいるたいけいせっていち.るーとcluster-2)

	direntぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(512)
	direntばいと := Getばいとからぽいんた(uintptr(direntぽいんた), 512, 512)
	hd.Rよみこみ28(るーとかいし, &direntばいと, 512)

	var dirent = [16]Tでぃれくとりentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntばいと[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].なまえ[0] == 0x00 {
			break
		}

		if dirent[i].さいず >= 0xFFFFFFFF {
			continue
		}

		if !Eすべておなじばいと(ふぁいるめい, dirent[i].なまえ[:len(ふぁいるめい)]) {
			continue
		}

		めもりかんりしゃ.Fあき(bpbぽいんた)
		めもりかんりしゃ.Fあき(direntぽいんた)
		return dirent[i].さいず
	}
	めもりかんりしゃ.Fあき(bpbぽいんた)
	めもりかんりしゃ.Fあき(direntぽいんた)
	return 0
}
func (self *Tふぁいるたいけいせっていち32) Rよみこみ(hd *Tしょうさいしようぎじゅつattachment, partentry Tくぶんtableentry, ふぁいるめい []byte, でーた []byte) {

	if partentry.Pくぶんid == 0x00 {
		return
	}

	めもりかんりしゃ := Tめもりかんりしゃ{}
	bpbぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(90)
	bpbばいと := Getばいとからぽいんた(uintptr(bpbぽいんた), 90, 90)
	var くぶんoffset = partentry.Sかいしlba

	hd.Rよみこみ28(くぶんoffset, &bpbばいと, 90)

	var ふぁいるたいけいせっていち = Tふぁいるたいけいせっていち32{}
	ふぁいるたいけいせっていち.Init(bpbばいと)

	var fatかいし = くぶんoffset + uint32(ふぁいるたいけいせっていち.よやくsectors)
	var fatさいず = ふぁいるたいけいせっていち.tableさいず

	var でーたかいし = fatかいし + fatさいず*uint32(ふぁいるたいけいせっていち.fatふくせい)

	var るーとかいし = でーたかいし + uint32(ふぁいるたいけいせっていち.sectorspercluster)*(ふぁいるたいけいせっていち.るーとcluster-2)

	direntぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(512)
	direntばいと := Getばいとからぽいんた(uintptr(direntぽいんた), 512, 512)
	hd.Rよみこみ28(るーとかいし, &direntばいと, 512)

	var dirent = [16]Tでぃれくとりentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntばいと[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].なまえ[0] == 0x00 {
			break
		}

		if dirent[i].さいず >= 0xFFFFFFFF {
			continue
		}

		if !Eすべておなじばいと(ふぁいるめい, dirent[i].なまえ[:len(ふぁいるめい)]) {
			continue
		}

		var firstふぁいるcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterひくい))

		var Sさいず = int32(dirent[i].さいず)
		var つぎふぁいるcluster = int32(firstふぁいるcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sさいず > 0 {
			var ふぁいるsector = でーたかいし + uint32(ふぁいるたいけいせっていち.sectorspercluster)*uint32(つぎふぁいるcluster-2)
			var sectoroffset int = 0

			for ; Sさいず > 0; Sさいず -= 512 {

				var buffer3 []byte

				if dirent[i].さいず > 512 {
					buffer3 = buffer_2[:512]
					hd.Rよみこみ28(ふぁいるsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].さいず]
					hd.Rよみこみ28(ふぁいるsector+uint32(sectoroffset), &buffer3, int(dirent[i].さいず))
				}

				copy(でーた[int32(dirent[i].さいず)-Sさいず:], buffer3)

				sectoroffset++

				if sectoroffset > int(ふぁいるたいけいせっていち.sectorspercluster) {
					break
				}

			}

			var fatsectorforげんざいのにちじcluster = uint32(つぎふぁいるcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rよみこみ28(fatかいし+fatsectorforげんざいのにちじcluster, &fatbuf, 512)

			var fatoffsetじゅしんsectorforげんざいのにちじcluster = つぎふぁいるcluster % 128
			var かいしoffset = fatoffsetじゅしんsectorforげんざいのにちじcluster * 4
			var ぶんまつoffset = fatoffsetじゅしんsectorforげんざいのにちじcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[かいしoffset:ぶんまつoffset])

			つぎふぁいるcluster = int32(Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer4)))
		}
	}
	めもりかんりしゃ.Fあき(bpbぽいんた)
	めもりかんりしゃ.Fあき(direntぽいんた)
}

type Tでぃれくとりentryfat32 struct {
	なまえ		[8]byte
	ext		[3]byte
	ぞくせい_2		uint8
	よやく		uint8
	cじかんtenth	uint8
	cじかん		uint16
	cひづけ		uint16
	aじかん		uint16
	firstclusterhi	uint16
	wじかん		uint16
	wひづけ		uint16
	firstclusterひくい	uint16
	さいず		uint32
}

func (self *Tでぃれくとりentryfat32) Init(でーた [32]byte) {
	copy(self.なまえ[:8], でーた[0:8])
	copy(self.ext[:3], でーた[8:11])
	self.ぞくせい_2 = でーた[11]
	self.よやく = でーた[12]
	self.cじかんtenth = でーた[13]
	self.cじかん = uint16(でーた[14]) | uint16(でーた[15])<<8
	self.cひづけ = uint16(でーた[16]) | uint16(でーた[17])<<8
	self.aじかん = uint16(でーた[18]) | uint16(でーた[19])<<8
	self.firstclusterhi = uint16(でーた[20]) | uint16(でーた[21])<<8
	self.wじかん = uint16(でーた[22]) | uint16(でーた[23])<<8
	self.wひづけ = uint16(でーた[24]) | uint16(でーた[25])<<8
	self.firstclusterひくい = uint16(でーた[26]) | uint16(でーた[27])<<8

	var buffer [4]byte
	copy(buffer[:4], でーた[28:32])
	self.さいず = Unsignedinteger32r(Aはいれつtounsignedinteger32(buffer))
}
