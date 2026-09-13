package fat

import . "util"
import . "console"
import . "driver/ata"
import . "فائلنظام/msdospartition"
import . "یادداشتmanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softنام			[8]byte
	بائٹسpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatکاپی			uint8
	روٹڈائریکٹریentry	uint16
	میزانsectors		uint16
	میڈیانوعیت		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	خفیہsectors		uint32
	میزانsectorcount	uint32

	جدولحجم		uint32
	extجھنڈیاں	uint16
	fatورژن		uint16
	روٹcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	drivenumber	uint8
	reserved	uint8
	bootsignature	uint8
	آوازآئیڈی	uint32
	آوازلیبل	[11]byte
	fatنوعیتلیبل	[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softنام[:8], data[3:11])

	self.بائٹسpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatکاپی = data[16]
	self.روٹڈائریکٹریentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.میزانsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.میڈیانوعیت = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.خفیہsectors = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.میزانsectorcount = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.جدولحجم = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	self.extجھنڈیاں = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatورژن = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.روٹcluster = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.drivenumber = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.آوازآئیڈی = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer1))

	copy(self.آوازلیبل[:11], data[71:82])
	copy(self.fatنوعیتلیبل[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *Tاعلیٹیکنالوجیattachment, partentry TPartitionجدولentry, فائلکانام []byte) uint32 {

	if partentry.Partitionآئیڈی == 0x00 {
		return 0
	}

	یادداشتmanager := Tیادداشتmanager{}
	bpbپؤائنٹر := یادداشتmanager.Malloc(90)
	bpbبائٹس := Getبائٹسfromپؤائنٹر(uintptr(bpbپؤائنٹر), 90, 90)
	var partitionoffset = partentry.Sچلائیںlba

	hd.Rپڑھیں28(partitionoffset, &bpbبائٹس, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbبائٹس)

	var fatچلائیں = partitionoffset + uint32(bpb.reservedsectors)
	var fatحجم = bpb.جدولحجم

	var dataچلائیں = fatچلائیں + fatحجم*uint32(bpb.fatکاپی)

	var روٹچلائیں = dataچلائیں + uint32(bpb.sectorspercluster)*(bpb.روٹcluster-2)

	direntپؤائنٹر := یادداشتmanager.Malloc(512)
	direntبائٹس := Getبائٹسfromپؤائنٹر(uintptr(direntپؤائنٹر), 512, 512)
	hd.Rپڑھیں28(روٹچلائیں, &direntبائٹس, 512)

	var dirent = [16]Tڈائریکٹریentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبائٹس[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].نام[0] == 0x00 {
			break
		}

		if dirent[i].حجم >= 0xFFFFFFFF {
			continue
		}

		if !Eبرابربائٹس(فائلکانام, dirent[i].نام[:len(فائلکانام)]) {
			continue
		}

		یادداشتmanager.Fخالی(bpbپؤائنٹر)
		یادداشتmanager.Fخالی(direntپؤائنٹر)
		return dirent[i].حجم
	}
	یادداشتmanager.Fخالی(bpbپؤائنٹر)
	یادداشتmanager.Fخالی(direntپؤائنٹر)
	return 0
}
func (self *TBiosparameterblock32) Rپڑھیں(hd *Tاعلیٹیکنالوجیattachment, partentry TPartitionجدولentry, فائلکانام []byte, data []byte) {

	if partentry.Partitionآئیڈی == 0x00 {
		return
	}

	یادداشتmanager := Tیادداشتmanager{}
	bpbپؤائنٹر := یادداشتmanager.Malloc(90)
	bpbبائٹس := Getبائٹسfromپؤائنٹر(uintptr(bpbپؤائنٹر), 90, 90)
	var partitionoffset = partentry.Sچلائیںlba

	hd.Rپڑھیں28(partitionoffset, &bpbبائٹس, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbبائٹس)

	var fatچلائیں = partitionoffset + uint32(bpb.reservedsectors)
	var fatحجم = bpb.جدولحجم

	var dataچلائیں = fatچلائیں + fatحجم*uint32(bpb.fatکاپی)

	var روٹچلائیں = dataچلائیں + uint32(bpb.sectorspercluster)*(bpb.روٹcluster-2)

	direntپؤائنٹر := یادداشتmanager.Malloc(512)
	direntبائٹس := Getبائٹسfromپؤائنٹر(uintptr(direntپؤائنٹر), 512, 512)
	hd.Rپڑھیں28(روٹچلائیں, &direntبائٹس, 512)

	var dirent = [16]Tڈائریکٹریentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntبائٹس[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].نام[0] == 0x00 {
			break
		}

		if dirent[i].حجم >= 0xFFFFFFFF {
			continue
		}

		if !Eبرابربائٹس(فائلکانام, dirent[i].نام[:len(فائلکانام)]) {
			continue
		}

		var firstفائلcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterکم))

		var Sحجم = int32(dirent[i].حجم)
		var اگلافائلcluster = int32(firstفائلcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sحجم > 0 {
			var فائلsector = dataچلائیں + uint32(bpb.sectorspercluster)*uint32(اگلافائلcluster-2)
			var sectoroffset int = 0

			for ; Sحجم > 0; Sحجم -= 512 {

				var buffer3 []byte

				if dirent[i].حجم > 512 {
					buffer3 = buffer_2[:512]
					hd.Rپڑھیں28(فائلsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].حجم]
					hd.Rپڑھیں28(فائلsector+uint32(sectoroffset), &buffer3, int(dirent[i].حجم))
				}

				copy(data[int32(dirent[i].حجم)-Sحجم:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforحالیہcluster = uint32(اگلافائلcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rپڑھیں28(fatچلائیں+fatsectorforحالیہcluster, &fatbuf, 512)

			var fatoffsetاندرsectorforحالیہcluster = اگلافائلcluster % 128
			var چلائیںoffset = fatoffsetاندرsectorforحالیہcluster * 4
			var آخرoffset = fatoffsetاندرsectorforحالیہcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[چلائیںoffset:آخرoffset])

			اگلافائلcluster = int32(Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer4)))
		}
	}
	یادداشتmanager.Fخالی(bpbپؤائنٹر)
	یادداشتmanager.Fخالی(direntپؤائنٹر)
}

type Tڈائریکٹریentryfat32 struct {
	نام		[8]byte
	ext		[3]byte
	صفتیں		uint8
	reserved	uint8
	cوقتtenth	uint8
	cوقت		uint16
	cتاریخ		uint16
	aوقت		uint16
	firstclusterhi	uint16
	wوقت		uint16
	wتاریخ		uint16
	firstclusterکم	uint16
	حجم		uint32
}

func (self *Tڈائریکٹریentryfat32) Init(data [32]byte) {
	copy(self.نام[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.صفتیں = data[11]
	self.reserved = data[12]
	self.cوقتtenth = data[13]
	self.cوقت = uint16(data[14]) | uint16(data[15])<<8
	self.cتاریخ = uint16(data[16]) | uint16(data[17])<<8
	self.aوقت = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wوقت = uint16(data[22]) | uint16(data[23])<<8
	self.wتاریخ = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterکم = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.حجم = Unsignedinteger32r(Aلڑیtounsignedinteger32(buffer))
}
