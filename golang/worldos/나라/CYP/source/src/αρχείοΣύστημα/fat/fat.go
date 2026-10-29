/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "αρχείοΣύστημα/msdospartition"
import . "μνήμηmanager"

type TBiosparameterΜπλοκ32 struct {
	jmp					[3]uint8
	softΌνομα				[8]byte
	bytespersector				uint16
	sectorspercluster			uint8
	reservedsectors				uint16
	fatΑντιγραφή				uint8
	ριζικόςκατάλογοςΚατάλογοςκαταχώρηση	uint16
	σύνολοsectors				uint16
	μέσαΤύπος				uint8
	fatsectorcount				uint16
	sectorpertrack				uint16
	headcount				uint16
	κρυφόsectors				uint32
	σύνολοsectorcount			uint32

	πίνακαςΜέγεθος		uint32
	extΔιακόπτες		uint16
	fatΈκδοση		uint16
	ριζικόςκατάλογοςcluster	uint32
	fatπληροφορία		uint16
	backupsector		uint16
	reserved0		[12]uint8
	driveΑριθμός		uint8
	reserved		uint8
	bootsignature		uint8
	όγκοςΤΑΥΤΌΤΗΤΑ		uint32
	όγκοςΕτικέτα		[11]byte
	fatΤύποςΕτικέτα		[8]byte
}

func (self *TBiosparameterΜπλοκ32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softΌνομα[:8], data[3:11])

	self.bytespersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatΑντιγραφή = data[16]
	self.ριζικόςκατάλογοςΚατάλογοςκαταχώρηση = (uint16(data[17]) | uint16(data[18])<<8)
	self.σύνολοsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.μέσαΤύπος = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.κρυφόsectors = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.σύνολοsectorcount = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.πίνακαςΜέγεθος = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	self.extΔιακόπτες = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatΈκδοση = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.ριζικόςκατάλογοςcluster = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	self.fatπληροφορία = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveΑριθμός = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.όγκοςΤΑΥΤΌΤΗΤΑ = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer1))

	copy(self.όγκοςΕτικέτα[:11], data[71:82])
	copy(self.fatΤύποςΕτικέτα[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterΜπλοκ32) Len(hd *TΓιαπροχωρημένουςΤεχνολογίαattachment, partκαταχώρηση TPartitionΠίνακαςκαταχώρηση, όνομααρχείου []byte) uint32 {

	if partκαταχώρηση.PartitionΤΑΥΤΌΤΗΤΑ == 0x00 {
		return 0
	}

	μνήμηmanager := TΜνήμηmanager{}
	bpbΔείκτης := μνήμηmanager.Malloc(90)
	bpbbytes := GetbytesfromΔείκτης(uintptr(bpbΔείκτης), 90, 90)
	var partitionoffset = partκαταχώρηση.Έναρξηlba

	hd.Ανάγνωση28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterΜπλοκ32{}
	bpb.Init(bpbbytes)

	var fatΈναρξη = partitionoffset + uint32(bpb.reservedsectors)
	var fatΜέγεθος = bpb.πίνακαςΜέγεθος

	var dataΈναρξη = fatΈναρξη + fatΜέγεθος*uint32(bpb.fatΑντιγραφή)

	var ριζικόςκατάλογοςΈναρξη = dataΈναρξη + uint32(bpb.sectorspercluster)*(bpb.ριζικόςκατάλογοςcluster-2)

	direntΔείκτης := μνήμηmanager.Malloc(512)
	direntbytes := GetbytesfromΔείκτης(uintptr(direntΔείκτης), 512, 512)
	hd.Ανάγνωση28(ριζικόςκατάλογοςΈναρξη, &direntbytes, 512)

	var dirent = [16]TΚατάλογοςκαταχώρησηfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].όνομα[0] == 0x00 {
			break
		}

		if dirent[i].μέγεθος >= 0xFFFFFFFF {
			continue
		}

		if !Ίσοbytes(όνομααρχείου, dirent[i].όνομα[:len(όνομααρχείου)]) {
			continue
		}

		μνήμηmanager.Ελεύθερα(bpbΔείκτης)
		μνήμηmanager.Ελεύθερα(direntΔείκτης)
		return dirent[i].μέγεθος
	}
	μνήμηmanager.Ελεύθερα(bpbΔείκτης)
	μνήμηmanager.Ελεύθερα(direntΔείκτης)
	return 0
}
func (self *TBiosparameterΜπλοκ32) Ανάγνωση(hd *TΓιαπροχωρημένουςΤεχνολογίαattachment, partκαταχώρηση TPartitionΠίνακαςκαταχώρηση, όνομααρχείου []byte, data []byte) {

	if partκαταχώρηση.PartitionΤΑΥΤΌΤΗΤΑ == 0x00 {
		return
	}

	μνήμηmanager := TΜνήμηmanager{}
	bpbΔείκτης := μνήμηmanager.Malloc(90)
	bpbbytes := GetbytesfromΔείκτης(uintptr(bpbΔείκτης), 90, 90)
	var partitionoffset = partκαταχώρηση.Έναρξηlba

	hd.Ανάγνωση28(partitionoffset, &bpbbytes, 90)

	var bpb = TBiosparameterΜπλοκ32{}
	bpb.Init(bpbbytes)

	var fatΈναρξη = partitionoffset + uint32(bpb.reservedsectors)
	var fatΜέγεθος = bpb.πίνακαςΜέγεθος

	var dataΈναρξη = fatΈναρξη + fatΜέγεθος*uint32(bpb.fatΑντιγραφή)

	var ριζικόςκατάλογοςΈναρξη = dataΈναρξη + uint32(bpb.sectorspercluster)*(bpb.ριζικόςκατάλογοςcluster-2)

	direntΔείκτης := μνήμηmanager.Malloc(512)
	direntbytes := GetbytesfromΔείκτης(uintptr(direntΔείκτης), 512, 512)
	hd.Ανάγνωση28(ριζικόςκατάλογοςΈναρξη, &direntbytes, 512)

	var dirent = [16]TΚατάλογοςκαταχώρησηfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].όνομα[0] == 0x00 {
			break
		}

		if dirent[i].μέγεθος >= 0xFFFFFFFF {
			continue
		}

		if !Ίσοbytes(όνομααρχείου, dirent[i].όνομα[:len(όνομααρχείου)]) {
			continue
		}

		var firstΑρχείοcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterΧαμηλή))

		var Μέγεθος = int32(dirent[i].μέγεθος)
		var επόμενοΑρχείοcluster = int32(firstΑρχείοcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Μέγεθος > 0 {
			var αρχείοsector = dataΈναρξη + uint32(bpb.sectorspercluster)*uint32(επόμενοΑρχείοcluster-2)
			var sectoroffset int = 0

			for ; Μέγεθος > 0; Μέγεθος -= 512 {

				var buffer3 []byte

				if dirent[i].μέγεθος > 512 {
					buffer3 = buffer_2[:512]
					hd.Ανάγνωση28(αρχείοsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].μέγεθος]
					hd.Ανάγνωση28(αρχείοsector+uint32(sectoroffset), &buffer3, int(dirent[i].μέγεθος))
				}

				copy(data[int32(dirent[i].μέγεθος)-Μέγεθος:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforΤρέχονcluster = uint32(επόμενοΑρχείοcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Ανάγνωση28(fatΈναρξη+fatsectorforΤρέχονcluster, &fatbuf, 512)

			var fatoffsetσεsectorforΤρέχονcluster = επόμενοΑρχείοcluster % 128
			var έναρξηoffset = fatoffsetσεsectorforΤρέχονcluster * 4
			var τέλοςoffset = fatoffsetσεsectorforΤρέχονcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[έναρξηoffset:τέλοςoffset])

			επόμενοΑρχείοcluster = int32(Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer4)))
		}
	}
	μνήμηmanager.Ελεύθερα(bpbΔείκτης)
	μνήμηmanager.Ελεύθερα(direntΔείκτης)
}

type TΚατάλογοςκαταχώρησηfat32 struct {
	όνομα			[8]byte
	ext			[3]byte
	ιδιότητες		uint8
	reserved		uint8
	cΏραtenth		uint8
	cΏρα			uint16
	cΗμερομηνία		uint16
	aΏρα			uint16
	firstclusterhi		uint16
	wΏρα			uint16
	wΗμερομηνία		uint16
	firstclusterΧαμηλή	uint16
	μέγεθος			uint32
}

func (self *TΚατάλογοςκαταχώρησηfat32) Init(data [32]byte) {
	copy(self.όνομα[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.ιδιότητες = data[11]
	self.reserved = data[12]
	self.cΏραtenth = data[13]
	self.cΏρα = uint16(data[14]) | uint16(data[15])<<8
	self.cΗμερομηνία = uint16(data[16]) | uint16(data[17])<<8
	self.aΏρα = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wΏρα = uint16(data[22]) | uint16(data[23])<<8
	self.wΗμερομηνία = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterΧαμηλή = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.μέγεθος = Unsignedinteger32r(Διάταξηtounsignedinteger32(buffer))
}
