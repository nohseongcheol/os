/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "util"
import . "console"
import . "driver/ata"
import . "ፋይልስርአት/msdospartition"
import . "ማስታወሻmanager"

type TBiosparameterመከልከያ32 struct {
	jmp			[3]uint8
	softስም			[8]byte
	ባይትስpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatኮፒ			uint8
	rootዳይሬክቶሪentry		uint16
	ጠቅላላsectors		uint16
	መገናኛአይነት		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	ድብቅsectors		uint32
	ጠቅላላsectorcount		uint32

	ሰንጠረዥመጠን	uint32
	extባንዲራዎች	uint16
	fatእትም		uint16
	rootcluster	uint32
	fatመረጃ		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveቁጥር	uint8
	reserved	uint8
	bootsignature	uint8
	መጠንመለያ		uint32
	መጠንምልክት		[11]byte
	fatአይነትምልክት	[8]byte
}

func (self *TBiosparameterመከልከያ32) Init(data []byte) {
	copy(self.jmp[:3], data[0:3])
	copy(self.softስም[:8], data[3:11])

	self.ባይትስpersector = (uint16(data[11]) | uint16(data[12])<<8)
	self.sectorspercluster = data[13]
	self.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	self.fatኮፒ = data[16]
	self.rootዳይሬክቶሪentry = (uint16(data[17]) | uint16(data[18])<<8)
	self.ጠቅላላsectors = (uint16(data[19]) | uint16(data[20])<<8)
	self.መገናኛአይነት = data[21]
	self.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	self.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	self.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	self.ድብቅsectors = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	self.ጠቅላላsectorcount = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	self.ሰንጠረዥመጠን = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	self.extባንዲራዎች = (uint16(data[40]) | uint16(data[41])<<8)
	self.fatእትም = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	self.rootcluster = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	self.fatመረጃ = (uint16(data[48]) | uint16(data[49])<<8)
	self.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(self.reserved0[:12], data[52:64])

	self.driveቁጥር = data[64]
	self.reserved = data[65]
	self.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	self.መጠንመለያ = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer1))

	copy(self.መጠንምልክት[:11], data[71:82])
	copy(self.fatአይነትምልክት[:8], data[82:90])

}

var console_2 = TConsole{}

func (self *TBiosparameterመከልከያ32) Len(hd *Tጠለቅቴክኖሎጂattachment, partentry TPartitionሰንጠረዥentry, የፋይልስም []byte) uint32 {

	if partentry.Partitionመለያ == 0x00 {
		return 0
	}

	ማስታወሻmanager := Tማስታወሻmanager{}
	bpbጠቋሚ := ማስታወሻmanager.Malloc(90)
	bpbባይትስ := Getባይትስfromጠቋሚ(uintptr(bpbጠቋሚ), 90, 90)
	var partitionoffset = partentry.Sማስጀመሪያlba

	hd.Rማንበቢያ28(partitionoffset, &bpbባይትስ, 90)

	var bpb = TBiosparameterመከልከያ32{}
	bpb.Init(bpbባይትስ)

	var fatማስጀመሪያ = partitionoffset + uint32(bpb.reservedsectors)
	var fatመጠን = bpb.ሰንጠረዥመጠን

	var dataማስጀመሪያ = fatማስጀመሪያ + fatመጠን*uint32(bpb.fatኮፒ)

	var rootማስጀመሪያ = dataማስጀመሪያ + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntጠቋሚ := ማስታወሻmanager.Malloc(512)
	direntባይትስ := Getባይትስfromጠቋሚ(uintptr(direntጠቋሚ), 512, 512)
	hd.Rማንበቢያ28(rootማስጀመሪያ, &direntባይትስ, 512)

	var dirent = [16]Tዳይሬክቶሪentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntባይትስ[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ስም[0] == 0x00 {
			break
		}

		if dirent[i].መጠን >= 0xFFFFFFFF {
			continue
		}

		if !Equalባይትስ(የፋይልስም, dirent[i].ስም[:len(የፋይልስም)]) {
			continue
		}

		ማስታወሻmanager.Fነፃ(bpbጠቋሚ)
		ማስታወሻmanager.Fነፃ(direntጠቋሚ)
		return dirent[i].መጠን
	}
	ማስታወሻmanager.Fነፃ(bpbጠቋሚ)
	ማስታወሻmanager.Fነፃ(direntጠቋሚ)
	return 0
}
func (self *TBiosparameterመከልከያ32) Rማንበቢያ(hd *Tጠለቅቴክኖሎጂattachment, partentry TPartitionሰንጠረዥentry, የፋይልስም []byte, data []byte) {

	if partentry.Partitionመለያ == 0x00 {
		return
	}

	ማስታወሻmanager := Tማስታወሻmanager{}
	bpbጠቋሚ := ማስታወሻmanager.Malloc(90)
	bpbባይትስ := Getባይትስfromጠቋሚ(uintptr(bpbጠቋሚ), 90, 90)
	var partitionoffset = partentry.Sማስጀመሪያlba

	hd.Rማንበቢያ28(partitionoffset, &bpbባይትስ, 90)

	var bpb = TBiosparameterመከልከያ32{}
	bpb.Init(bpbባይትስ)

	var fatማስጀመሪያ = partitionoffset + uint32(bpb.reservedsectors)
	var fatመጠን = bpb.ሰንጠረዥመጠን

	var dataማስጀመሪያ = fatማስጀመሪያ + fatመጠን*uint32(bpb.fatኮፒ)

	var rootማስጀመሪያ = dataማስጀመሪያ + uint32(bpb.sectorspercluster)*(bpb.rootcluster-2)

	direntጠቋሚ := ማስታወሻmanager.Malloc(512)
	direntባይትስ := Getባይትስfromጠቋሚ(uintptr(direntጠቋሚ), 512, 512)
	hd.Rማንበቢያ28(rootማስጀመሪያ, &direntባይትስ, 512)

	var dirent = [16]Tዳይሬክቶሪentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntባይትስ[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].ስም[0] == 0x00 {
			break
		}

		if dirent[i].መጠን >= 0xFFFFFFFF {
			continue
		}

		if !Equalባይትስ(የፋይልስም, dirent[i].ስም[:len(የፋይልስም)]) {
			continue
		}

		var firstፋይልcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterዝቅተኛ))

		var Sመጠን = int32(dirent[i].መጠን)
		var የሚቀጥለውፋይልcluster = int32(firstፋይልcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Sመጠን > 0 {
			var ፋይልsector = dataማስጀመሪያ + uint32(bpb.sectorspercluster)*uint32(የሚቀጥለውፋይልcluster-2)
			var sectoroffset int = 0

			for ; Sመጠን > 0; Sመጠን -= 512 {

				var buffer3 []byte

				if dirent[i].መጠን > 512 {
					buffer3 = buffer_2[:512]
					hd.Rማንበቢያ28(ፋይልsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].መጠን]
					hd.Rማንበቢያ28(ፋይልsector+uint32(sectoroffset), &buffer3, int(dirent[i].መጠን))
				}

				copy(data[int32(dirent[i].መጠን)-Sመጠን:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(የሚቀጥለውፋይልcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Rማንበቢያ28(fatማስጀመሪያ+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetውስጥsectorforcurrentcluster = የሚቀጥለውፋይልcluster % 128
			var ማስጀመሪያoffset = fatoffsetውስጥsectorforcurrentcluster * 4
			var መጨረሻoffset = fatoffsetውስጥsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[ማስጀመሪያoffset:መጨረሻoffset])

			የሚቀጥለውፋይልcluster = int32(Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer4)))
		}
	}
	ማስታወሻmanager.Fነፃ(bpbጠቋሚ)
	ማስታወሻmanager.Fነፃ(direntጠቋሚ)
}

type Tዳይሬክቶሪentryfat32 struct {
	ስም			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cሰዓትtenth		uint8
	cሰዓት			uint16
	cቀን			uint16
	aሰዓት			uint16
	firstclusterhi		uint16
	wሰዓት			uint16
	wቀን			uint16
	firstclusterዝቅተኛ	uint16
	መጠን			uint32
}

func (self *Tዳይሬክቶሪentryfat32) Init(data [32]byte) {
	copy(self.ስም[:8], data[0:8])
	copy(self.ext[:3], data[8:11])
	self.attributes = data[11]
	self.reserved = data[12]
	self.cሰዓትtenth = data[13]
	self.cሰዓት = uint16(data[14]) | uint16(data[15])<<8
	self.cቀን = uint16(data[16]) | uint16(data[17])<<8
	self.aሰዓት = uint16(data[18]) | uint16(data[19])<<8
	self.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	self.wሰዓት = uint16(data[22]) | uint16(data[23])<<8
	self.wቀን = uint16(data[24]) | uint16(data[25])<<8
	self.firstclusterዝቅተኛ = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	self.መጠን = Unsignedinteger32r(Aማዘጋጃtounsignedinteger32(buffer))
}
