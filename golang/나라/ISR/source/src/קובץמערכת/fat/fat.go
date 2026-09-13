package fat

import . "util"
import . "console"
import . "driver/ata"
import . "קובץמערכת/msdospartition"
import . "זיכרוןmanager"

type TBiosparameterבלוק32 struct {
	jmp			[3]uint8
	softשם			[8]byte
	בתיםpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatהעתק			uint8
	שורשספרייהentry		uint16
	totalsectors		uint16
	מדיהסוג			uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	נסתרsectors		uint32
	totalsectorcount	uint32

	tableגודל	uint32
	extדגלים	uint16
	fatגרסה		uint16
	שורשcluster	uint32
	fatמידע		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveמספר	uint8
	reserved	uint8
	bootsignature	uint8
	נפחמזהה		uint32
	נפחתווית	[11]byte
	fatסוגתווית	[8]byte
}

func (self *TBiosparameterבלוק32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softשם[:8], data[3:11])

	self.בתיםpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatהעתק = data[16]
	self.שורשספרייהentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.totalsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.מדיהסוג = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.נסתרsectors = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.totalsectorcount = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.tableגודל = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	self.extדגלים = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatגרסה = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.שורשcluster = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	self.fatמידע = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveמספר = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.נפחמזהה = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer1))

	copy(self.נפחתווית[:11], data[71:82])
	copy(self.fatסוגתווית[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterבלוק32) Len(hd *Tמתקדםטכנולוגיהattachment, partentry TPartitiontableentry, שםהקובץ []byte) uint32 {

	if partentry.Partitionמזהה == 0x00 {
		return 0
	}

	זיכרוןmanager := Tזיכרוןmanager{}
	bpbסמן := זיכרוןmanager.Malloc(90)
	bpbבתים := Getבתיםfromסמן(uintptr(bpbסמן), 90, 90)
	var partitionoffset = partentry.Sהתחלהlba

	hd.Rקריאה28(partitionoffset, &bpbבתים, 90)

	var bpb = TBiosparameterבלוק32{}
	bpb.Init(bpbבתים)

	var fatהתחלה = partitionoffset + uint32(bpb.reservedsectors)
	var fatגודל = bpb.tableגודל

	var dataהתחלה = fatהתחלה + fatגודל*uint32(bpb.fatהעתק)

	var שורשהתחלה = dataהתחלה + uint32(bpb.sectorspercluster)*(bpb.שורשcluster-2)

	direntסמן := זיכרוןmanager.Malloc(512)
	direntבתים := Getבתיםfromסמן(uintptr(direntסמן), 512, 512)
	hd.Rקריאה28(שורשהתחלה, &direntבתים, 512)

	var dirent = [16]Tספרייהentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntבתים[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].שם[0] == 0x00 {
			break
		}

		if dirent[i].גודל >= 0xFFFFFFFF {
			continue
		}

		if !Equalבתים(שםהקובץ, dirent[i].שם[:len(שםהקובץ)]) {
			continue
		}

		זיכרוןmanager.Fפנוי(bpbסמן)
		זיכרוןmanager.Fפנוי(direntסמן)
		return dirent[i].גודל
	}
	זיכרוןmanager.Fפנוי(bpbסמן)
	זיכרוןmanager.Fפנוי(direntסמן)
	return 0
}
func (self *TBiosparameterבלוק32) Rקריאה(hd *Tמתקדםטכנולוגיהattachment, partentry TPartitiontableentry, שםהקובץ []byte, data []byte) {

	if partentry.Partitionמזהה == 0x00 {
		return
	}

	זיכרוןmanager := Tזיכרוןmanager{}
	bpbסמן := זיכרוןmanager.Malloc(90)
	bpbבתים := Getבתיםfromסמן(uintptr(bpbסמן), 90, 90)
	var partitionoffset = partentry.Sהתחלהlba

	hd.Rקריאה28(partitionoffset, &bpbבתים, 90)

	var bpb = TBiosparameterבלוק32{}
	bpb.Init(bpbבתים)

	var fatהתחלה = partitionoffset + uint32(bpb.reservedsectors)
	var fatגודל = bpb.tableגודל

	var dataהתחלה = fatהתחלה + fatגודל*uint32(bpb.fatהעתק)

	var שורשהתחלה = dataהתחלה + uint32(bpb.sectorspercluster)*(bpb.שורשcluster-2)

	direntסמן := זיכרוןmanager.Malloc(512)
	direntבתים := Getבתיםfromסמן(uintptr(direntסמן), 512, 512)
	hd.Rקריאה28(שורשהתחלה, &direntבתים, 512)

	var dirent = [16]Tספרייהentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntבתים[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].שם[0] == 0x00 {
			break
		}

		if dirent[i].גודל >= 0xFFFFFFFF {
			continue
		}

		if !Equalבתים(שםהקובץ, dirent[i].שם[:len(שםהקובץ)]) {
			continue
		}

		var firstקובץcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterנמוך))

		var Sגודל = int32(dirent[i].גודל)
		var הבאקובץcluster = int32(firstקובץcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sגודל > 0 {
			var קובץsector = dataהתחלה + uint32(bpb.sectorspercluster)*uint32(הבאקובץcluster-2)
			var sectoroffset int = 0

			for ; Sגודל > 0; Sגודל -= 512 {

				var buffer3 []byte

				if dirent[i].גודל > 512 {
					buffer3 = buffer_2[:512]
					hd.Rקריאה28(קובץsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].גודל]
					hd.Rקריאה28(קובץsector+uint32(sectoroffset), &buffer3, int(dirent[i].גודל))
				}

				copy(data[int32(dirent[i].גודל)-Sגודל:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforנוכחיcluster = uint32(הבאקובץcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rקריאה28(fatהתחלה+fatsectorforנוכחיcluster, &fatbuf, 512)

			var fatoffsetנכנסsectorforנוכחיcluster = הבאקובץcluster % 128
			var התחלהoffset = fatoffsetנכנסsectorforנוכחיcluster * 4
			var סיוםoffset = fatoffsetנכנסsectorforנוכחיcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[התחלהoffset:סיוםoffset])

			הבאקובץcluster = int32(Unsignedinteger32r(Aמערךtounsignedinteger32(buffer4)))
		}
	}
	זיכרוןmanager.Fפנוי(bpbסמן)
	זיכרוןmanager.Fפנוי(direntסמן)
}

type Tספרייהentryfat32 struct {
	שם			[8]byte
	ext			[3]byte
	מאפיינים		uint8
	reserved		uint8
	cזמןtenth		uint8
	cזמן			uint16
	cתאריך			uint16
	aזמן			uint16
	firstclusterhi		uint16
	wזמן			uint16
	wתאריך			uint16
	firstclusterנמוך	uint16
	גודל			uint32
}

func (self *Tספרייהentryfat32) Init(data [32]byte) {
	copy(self.שם[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.מאפיינים = data[11]
	self.reserved = data[12]
	self.cזמןtenth = data[13]
	self.cזמן = uint16(data[14]) | uint16(data[15])<<8
	self.cתאריך = uint16(data[16]) | uint16(data[17])<<8
	self.aזמן = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wזמן = uint16(data[22]) | uint16(data[23])<<8
	self.wתאריך = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterנמוך = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.גודל = Unsignedinteger32r(Aמערךtounsignedinteger32(buffer))
}
