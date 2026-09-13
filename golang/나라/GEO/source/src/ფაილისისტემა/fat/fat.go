package fat

import . "util"
import . "console"
import . "driver/ata"
import . "ფაილისისტემა/msdospartition"
import . "მეხსიერებაmanager"

type TBiosparameterblock32 struct {
	jmp			[3]uint8
	softსახელი		[8]byte
	ბაიტიpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatდააკოპირე		uint8
	rootდასტაentry		uint16
	სულsectors		uint16
	მედიატიპი		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	სულsectorcount		uint32

	ცხრილიზომა		uint32
	extალმები		uint16
	fatversion		uint16
	rootcluster		uint32
	fatinfo			uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveრიცხვი		uint8
	reserved		uint8
	ჩატვირთვაsignature	uint8
	volumeid		uint32
	volumeსათაური		[11]byte
	fatტიპისათაური		[8]byte
}

func (self *TBiosparameterblock32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softსახელი[:8], data[3:11])

	self.ბაიტიpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatდააკოპირე = data[16]
	self.rootდასტაentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.სულsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.მედიატიპი = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.hiddensectors = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.სულsectorcount = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.ცხრილიზომა = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer1))

	self.extალმები = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer1))

	self.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveრიცხვი = data[64]
	self.reserved = data[65]
	self.ჩატვირთვაsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.volumeid = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer1))

	copy(self.volumeსათაური[:11], data[71:82])
	copy(self.fatტიპისათაური[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterblock32) Len(hd *Tდეტალურიtechnologyattachment, partentry TPartitionცხრილიentry, ფაილისსახელი []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	მეხსიერებაmanager := Tმეხსიერებაmanager{}
	bpbკურსორი := მეხსიერებაmanager.Malloc(90)
	bpbბაიტი := Getბაიტიfromკურსორი(uintptr(bpbკურსორი), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Rკითხვა28(partitionoffset, &bpbბაიტი, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbბაიტი)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatზომა = bpb.ცხრილიზომა

	var datastart = fatstart + fatზომა*uint32(bpb.fatდააკოპირე)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntკურსორი := მეხსიერებაmanager.Malloc(512)
	direntბაიტი := Getბაიტიfromკურსორი(uintptr(direntკურსორი), 512, 512)
	hd.Rკითხვა28(rootstart, &direntბაიტი, 512)

	var dirent = [16]Tდასტაentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntბაიტი[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].სახელი[0] == 0x00 {
			break
		}

		if dirent[i].ზომა >= 0xFFFFFFFF {
			continue
		}

		if !Equalბაიტი(ფაილისსახელი, dirent[i].სახელი[:len(ფაილისსახელი)]) {
			continue
		}

		მეხსიერებაmanager.Fთავისუფალი(bpbკურსორი)
		მეხსიერებაmanager.Fთავისუფალი(direntკურსორი)
		return dirent[i].ზომა
	}
	მეხსიერებაmanager.Fთავისუფალი(bpbკურსორი)
	მეხსიერებაmanager.Fთავისუფალი(direntკურსორი)
	return 0
}
func (self *TBiosparameterblock32) Rკითხვა(hd *Tდეტალურიtechnologyattachment, partentry TPartitionცხრილიentry, ფაილისსახელი []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	მეხსიერებაmanager := Tმეხსიერებაmanager{}
	bpbკურსორი := მეხსიერებაmanager.Malloc(90)
	bpbბაიტი := Getბაიტიfromკურსორი(uintptr(bpbკურსორი), 90, 90)
	var partitionoffset = partentry.Startlba

	hd.Rკითხვა28(partitionoffset, &bpbბაიტი, 90)

	var bpb = TBiosparameterblock32{}
	bpb.Init(bpbბაიტი)

	var fatstart = partitionoffset + uint32(bpb.reservedsectors)
	var fatზომა = bpb.ცხრილიზომა

	var datastart = fatstart + fatზომა*uint32(bpb.fatდააკოპირე)

	var rootstart = datastart + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntკურსორი := მეხსიერებაmanager.Malloc(512)
	direntბაიტი := Getბაიტიfromკურსორი(uintptr(direntკურსორი), 512, 512)
	hd.Rკითხვა28(rootstart, &direntბაიტი, 512)

	var dirent = [16]Tდასტაentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntბაიტი[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].სახელი[0] == 0x00 {
			break
		}

		if dirent[i].ზომა >= 0xFFFFFFFF {
			continue
		}

		if !Equalბაიტი(ფაილისსახელი, dirent[i].სახელი[:len(ფაილისსახელი)]) {
			continue
		}

		var firstფაილიcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterlow))

		var Sზომა = int32(dirent[i].ზომა)
		var შემდეგიფაილიcluster = int32(firstფაილიcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sზომა > 0 {
			var ფაილიsector = datastart + uint32(bpb.sectorspercluster)*uint32(შემდეგიფაილიcluster-2)
			var sectoroffset int = 0

			for ; Sზომა > 0; Sზომა -= 512 {

				var buffer3 []byte

				if dirent[i].ზომა > 512 {
					buffer3 = buffer_2[:512]
					hd.Rკითხვა28(ფაილიsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].ზომა]
					hd.Rკითხვა28(ფაილიsector+uint32(sectoroffset), &buffer3, int(dirent[i].ზომა))
				}

				copy(data[int32(dirent[i].ზომა)-Sზომა:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(შემდეგიფაილიcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rკითხვა28(fatstart+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetგადიდებაsectorforcurrentcluster = შემდეგიფაილიcluster % 128
			var startoffset = fatoffsetგადიდებაsectorforcurrentcluster * 4
			var endoffset = fatoffsetგადიდებაsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startoffset:endoffset])

			შემდეგიფაილიcluster = int32(Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer4)))
		}
	}
	მეხსიერებაmanager.Fთავისუფალი(bpbკურსორი)
	მეხსიერებაmanager.Fთავისუფალი(direntკურსორი)
}

type Tდასტაentryfat32 struct {
	სახელი		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cდროtenth	uint8
	cდრო		uint16
	cთარიღი		uint16
	aდრო		uint16
	firstclusterhi	uint16
	wდრო		uint16
	wთარიღი		uint16
	firstclusterlow	uint16
	ზომა		uint32
}

func (self *Tდასტაentryfat32) Init(data [32]byte) {
	copy(self.სახელი[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cდროtenth = data[13]
	self.cდრო = uint16(data[14]) | uint16(data[15])<<8
	self.cთარიღი = uint16(data[16]) | uint16(data[17])<<8
	self.aდრო = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wდრო = uint16(data[22]) | uint16(data[23])<<8
	self.wთარიღი = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterlow = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.ზომა = Unsignedinteger32r(Aმასივიtounsignedinteger32(buffer))
}
