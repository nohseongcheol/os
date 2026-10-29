/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "konsol"
import . "driver/ata"
import . "dosyaSistem/msdospartition"
import . "bellekmanager"

type TDosya_sistemi_parametreleri32 struct {
	jmp			[3]uint8
	softİsim		[8]byte
	baytpersector		uint16
	sectorspercluster	uint8
	rezervesectors		uint16
	fatKopyala		uint8
	kökDizinDizingirdi	uint16
	toplamsectors		uint16
	ortamTür		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	gizlisectors		uint32
	toplamsectorcount	uint32

	tabloBoyut	uint32
	extİmler	uint16
	fatSürüm	uint16
	kökDizincluster	uint32
	fatBilgi	uint16
	backupsector	uint16
	rezerve0	[12]uint8
	driveSayı	uint8
	rezerve		uint8
	bootsignature	uint8
	hacimNo		uint32
	hacimetiket	[11]byte
	fatTüretiket	[8]byte
}

func (self *TDosya_sistemi_parametreleri32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softİsim[:8], data[3:11])

	self.baytpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.rezervesectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatKopyala = data[16]
	self.kökDizinDizingirdi = (uint16(data[17]) | uint16(data[18])<<8)
	self.toplamsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.ortamTür = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.gizlisectors = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.toplamsectorcount = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tabloBoyut = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	self.extİmler = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatSürüm = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.kökDizincluster = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	self.fatBilgi = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.rezerve0[:12], data[52:64])

	self.driveSayı = data[64]
	self.rezerve = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.hacimNo = Unsignedinteger32r(Dizitounsignedinteger32(buffer1))

	copy(self.hacimetiket[:11], data[71:82])
	copy(self.fatTüretiket[:8], data[82:90])

}

var konsol_2 = TKonsol{}

func (self *TDosya_sistemi_parametreleri32) Len(hd *TGelişmişTeknolojiattachment, partgirdi TPartitionTablogirdi, dosyaadı []byte) uint32 {

	if partgirdi.PartitionNo == 0x00 {
		return 0
	}

	bellekmanager := TBellekmanager{}
	bpbBelirteç := bellekmanager.Bellek_ayır(90)
	bpbBayt := GetBaytfromBelirteç(uintptr(bpbBelirteç), 90, 90)
	var partitionoffset = partgirdi.Başlatlba

	hd.Okuma28(partitionoffset, &bpbBayt, 90)

	var dosya_sistemi_parametreleri = TDosya_sistemi_parametreleri32{}
	dosya_sistemi_parametreleri.Init(bpbBayt)

	var fatBaşlat = partitionoffset + uint32(dosya_sistemi_parametreleri.rezervesectors)
	var fatBoyut = dosya_sistemi_parametreleri.tabloBoyut

	var dataBaşlat = fatBaşlat + fatBoyut*uint32(dosya_sistemi_parametreleri.fatKopyala)

	var kökDizinBaşlat = dataBaşlat + uint32(dosya_sistemi_parametreleri.sectorspercluster)*(dosya_sistemi_parametreleri.kökDizincluster-2)

	direntBelirteç := bellekmanager.Bellek_ayır(512)
	direntBayt := GetBaytfromBelirteç(uintptr(direntBelirteç), 512, 512)
	hd.Okuma28(kökDizinBaşlat, &direntBayt, 512)

	var dirent = [16]TDizingirdifat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].isim[0] == 0x00 {
			break
		}

		if dirent[i].boyut >= 0xFFFFFFFF {
			continue
		}

		if !EşitBayt(dosyaadı, dirent[i].isim[:len(dosyaadı)]) {
			continue
		}

		bellekmanager.Boş(bpbBelirteç)
		bellekmanager.Boş(direntBelirteç)
		return dirent[i].boyut
	}
	bellekmanager.Boş(bpbBelirteç)
	bellekmanager.Boş(direntBelirteç)
	return 0
}
func (self *TDosya_sistemi_parametreleri32) Okuma(hd *TGelişmişTeknolojiattachment, partgirdi TPartitionTablogirdi, dosyaadı []byte, data []byte) {

	if partgirdi.PartitionNo == 0x00 {
		return
	}

	bellekmanager := TBellekmanager{}
	bpbBelirteç := bellekmanager.Bellek_ayır(90)
	bpbBayt := GetBaytfromBelirteç(uintptr(bpbBelirteç), 90, 90)
	var partitionoffset = partgirdi.Başlatlba

	hd.Okuma28(partitionoffset, &bpbBayt, 90)

	var dosya_sistemi_parametreleri = TDosya_sistemi_parametreleri32{}
	dosya_sistemi_parametreleri.Init(bpbBayt)

	var fatBaşlat = partitionoffset + uint32(dosya_sistemi_parametreleri.rezervesectors)
	var fatBoyut = dosya_sistemi_parametreleri.tabloBoyut

	var dataBaşlat = fatBaşlat + fatBoyut*uint32(dosya_sistemi_parametreleri.fatKopyala)

	var kökDizinBaşlat = dataBaşlat + uint32(dosya_sistemi_parametreleri.sectorspercluster)*(dosya_sistemi_parametreleri.kökDizincluster-2)

	direntBelirteç := bellekmanager.Bellek_ayır(512)
	direntBayt := GetBaytfromBelirteç(uintptr(direntBelirteç), 512, 512)
	hd.Okuma28(kökDizinBaşlat, &direntBayt, 512)

	var dirent = [16]TDizingirdifat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntBayt[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].isim[0] == 0x00 {
			break
		}

		if dirent[i].boyut >= 0xFFFFFFFF {
			continue
		}

		if !EşitBayt(dosyaadı, dirent[i].isim[:len(dosyaadı)]) {
			continue
		}

		var firstDosyacluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterDüşük))

		var Boyut = int32(dirent[i].boyut)
		var sonrakiDosyacluster = int32(firstDosyacluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Boyut > 0 {
			var dosyasector = dataBaşlat + uint32(dosya_sistemi_parametreleri.sectorspercluster)*uint32(sonrakiDosyacluster-2)
			var sectoroffset int = 0

			for ; Boyut > 0; Boyut -= 512 {

				var buffer3 []byte

				if dirent[i].boyut > 512 {
					buffer3 = buffer_2[:512]
					hd.Okuma28(dosyasector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].boyut]
					hd.Okuma28(dosyasector+uint32(sectoroffset), &buffer3, int(dirent[i].boyut))
				}

				copy(data[int32(dirent[i].boyut)-Boyut:], buffer3)

				sectoroffset++

				if sectoroffset > int(dosya_sistemi_parametreleri.sectorspercluster) {
					break
				}

			}

			var fatsectorforŞuancluster = uint32(sonrakiDosyacluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Okuma28(fatBaşlat+fatsectorforŞuancluster, &fatbuf, 512)

			var fatoffsetGelensectorforŞuancluster = sonrakiDosyacluster % 128
			var başlatoffset = fatoffsetGelensectorforŞuancluster * 4
			var sonoffset = fatoffsetGelensectorforŞuancluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[başlatoffset:sonoffset])

			sonrakiDosyacluster = int32(Unsignedinteger32r(Dizitounsignedinteger32(buffer4)))
		}
	}
	bellekmanager.Boş(bpbBelirteç)
	bellekmanager.Boş(direntBelirteç)
}

type TDizingirdifat32 struct {
	isim			[8]byte
	ext			[3]byte
	öznitelikler		uint8
	rezerve			uint8
	cSaattenth		uint8
	cSaat			uint16
	cTarih			uint16
	aSaat			uint16
	firstclusterhi		uint16
	wSaat			uint16
	wTarih			uint16
	firstclusterDüşük	uint16
	boyut			uint32
}

func (self *TDizingirdifat32) Init(data [32]byte) {
	copy(self.isim[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.öznitelikler = data[11]
	self.rezerve = data[12]
	self.cSaattenth = data[13]
	self.cSaat = uint16(data[14]) | uint16(data[15])<<8
	self.cTarih = uint16(data[16]) | uint16(data[17])<<8
	self.aSaat = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wSaat = uint16(data[22]) | uint16(data[23])<<8
	self.wTarih = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterDüşük = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.boyut = Unsignedinteger32r(Dizitounsignedinteger32(buffer))
}
