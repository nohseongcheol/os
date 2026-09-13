package fat

import . "util"
import . "console"
import . "driver/ata"
import . "ֆայլՀամակարգ/msdospartition"
import . "հիշողությունmanager"

type TBiosparameterԱրգելափակել32 struct {
	jmp			[3]uint8
	softԱնուն		[8]byte
	բայթերpersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatՊատճենել		uint8
	արմատֆայլապանակentry	uint16
	ընդհանուրsectors	uint16
	մեդիաՏիպ		uint8
	fatsectorcount		uint16
	sectorpertrack		uint16
	headcount		uint16
	hiddensectors		uint32
	ընդհանուրsectorcount	uint32

	աղյուսակՉափս	uint32
	extԴրոշներ	uint16
	fatversion	uint16
	արմատcluster	uint32
	fatinfo		uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveՀԱՄԱՐ	uint8
	reserved	uint8
	bootsignature	uint8
	ծավալid		uint32
	ծավալՊիտակ	[11]byte
	fatՏիպՊիտակ	[8]byte
}

func (ինքնուրույն *TBiosparameterԱրգելափակել32) Init(data []byte) {
	copy(ինքնուրույն.jmp[:3], data[0:3])
	copy(ինքնուրույն.softԱնուն[:8], data[3:11])

	ինքնուրույն.բայթերpersector = (uint16(data[11]) | uint16(data[12])<<8)
	ինքնուրույն.sectorspercluster = data[13]
	ինքնուրույն.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	ինքնուրույն.fatՊատճենել = data[16]
	ինքնուրույն.արմատֆայլապանակentry = (uint16(data[17]) | uint16(data[18])<<8)
	ինքնուրույն.ընդհանուրsectors = (uint16(data[19]) | uint16(data[20])<<8)
	ինքնուրույն.մեդիաՏիպ = data[21]
	ինքնուրույն.fatsectorcount = (uint16(data[22]) | uint16(data[23])<<8)
	ինքնուրույն.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	ինքնուրույն.headcount = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	ինքնուրույն.hiddensectors = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	ինքնուրույն.ընդհանուրsectorcount = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	ինքնուրույն.աղյուսակՉափս = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	ինքնուրույն.extԴրոշներ = (uint16(data[40]) | uint16(data[41])<<8)
	ինքնուրույն.fatversion = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	ինքնուրույն.արմատcluster = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	ինքնուրույն.fatinfo = (uint16(data[48]) | uint16(data[49])<<8)
	ինքնուրույն.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(ինքնուրույն.reserved0[:12], data[52:64])

	ինքնուրույն.driveՀԱՄԱՐ = data[64]
	ինքնուրույն.reserved = data[65]
	ինքնուրույն.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	ինքնուրույն.ծավալid = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer1))

	copy(ինքնուրույն.ծավալՊիտակ[:11], data[71:82])
	copy(ինքնուրույն.fatՏիպՊիտակ[:8], data[82:90])

}

var console_2 = TConsole{}

func (ինքնուրույն *TBiosparameterԱրգելափակել32) Len(hd *TԸնդլայնվածՏեխնոլոգիաattachment, partentry TPartitionԱղյուսակentry, ֆայլիանուն []byte) uint32 {

	if partentry.Partitionid == 0x00 {
		return 0
	}

	հիշողությունmanager := TՀիշողությունmanager{}
	bpbՑուցիչ := հիշողությունmanager.Malloc(90)
	bpbԲայթեր := GetԲայթերիցՑուցիչ(uintptr(bpbՑուցիչ), 90, 90)
	var partitionoffset = partentry.Սկիզբlba

	hd.Ընթերցում28(partitionoffset, &bpbԲայթեր, 90)

	var bpb = TBiosparameterԱրգելափակել32{}
	bpb.Init(bpbԲայթեր)

	var fatՍկիզբ = partitionoffset + uint32(bpb.reservedsectors)
	var fatՉափս = bpb.աղյուսակՉափս

	var dataՍկիզբ = fatՍկիզբ + fatՉափս*uint32(bpb.fatՊատճենել)

	var արմատՍկիզբ = dataՍկիզբ + uint32(bpb.sectorspercluster)*(bpb.արմատcluster-2)

	direntՑուցիչ := հիշողությունmanager.Malloc(512)
	direntԲայթեր := GetԲայթերիցՑուցիչ(uintptr(direntՑուցիչ), 512, 512)
	hd.Ընթերցում28(արմատՍկիզբ, &direntԲայթեր, 512)

	var dirent = [16]TՖայլապանակentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntԲայթեր[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].անուն[0] == 0x00 {
			break
		}

		if dirent[i].չափս >= 0xFFFFFFFF {
			continue
		}

		if !EqualԲայթեր(ֆայլիանուն, dirent[i].անուն[:len(ֆայլիանուն)]) {
			continue
		}

		հիշողությունmanager.Ազատ(bpbՑուցիչ)
		հիշողությունmanager.Ազատ(direntՑուցիչ)
		return dirent[i].չափս
	}
	հիշողությունmanager.Ազատ(bpbՑուցիչ)
	հիշողությունmanager.Ազատ(direntՑուցիչ)
	return 0
}
func (ինքնուրույն *TBiosparameterԱրգելափակել32) Ընթերցում(hd *TԸնդլայնվածՏեխնոլոգիաattachment, partentry TPartitionԱղյուսակentry, ֆայլիանուն []byte, data []byte) {

	if partentry.Partitionid == 0x00 {
		return
	}

	հիշողությունmanager := TՀիշողությունmanager{}
	bpbՑուցիչ := հիշողությունmanager.Malloc(90)
	bpbԲայթեր := GetԲայթերիցՑուցիչ(uintptr(bpbՑուցիչ), 90, 90)
	var partitionoffset = partentry.Սկիզբlba

	hd.Ընթերցում28(partitionoffset, &bpbԲայթեր, 90)

	var bpb = TBiosparameterԱրգելափակել32{}
	bpb.Init(bpbԲայթեր)

	var fatՍկիզբ = partitionoffset + uint32(bpb.reservedsectors)
	var fatՉափս = bpb.աղյուսակՉափս

	var dataՍկիզբ = fatՍկիզբ + fatՉափս*uint32(bpb.fatՊատճենել)

	var արմատՍկիզբ = dataՍկիզբ + uint32(bpb.sectorspercluster)*(bpb.արմատcluster-2)

	direntՑուցիչ := հիշողությունmanager.Malloc(512)
	direntԲայթեր := GetԲայթերիցՑուցիչ(uintptr(direntՑուցիչ), 512, 512)
	hd.Ընթերցում28(արմատՍկիզբ, &direntԲայթեր, 512)

	var dirent = [16]TՖայլապանակentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntԲայթեր[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].անուն[0] == 0x00 {
			break
		}

		if dirent[i].չափս >= 0xFFFFFFFF {
			continue
		}

		if !EqualԲայթեր(ֆայլիանուն, dirent[i].անուն[:len(ֆայլիանուն)]) {
			continue
		}

		var firstՖայլcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterՑածր))

		var Չափս = int32(dirent[i].չափս)
		var հաջորդՖայլcluster = int32(firstՖայլcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Չափս > 0 {
			var ֆայլsector = dataՍկիզբ + uint32(bpb.sectorspercluster)*uint32(հաջորդՖայլcluster-2)
			var sectoroffset int = 0

			for ; Չափս > 0; Չափս -= 512 {

				var buffer3 []byte

				if dirent[i].չափս > 512 {
					buffer3 = buffer_2[:512]
					hd.Ընթերցում28(ֆայլsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].չափս]
					hd.Ընթերցում28(ֆայլsector+uint32(sectoroffset), &buffer3, int(dirent[i].չափս))
				}

				copy(data[int32(dirent[i].չափս)-Չափս:], buffer3)

				sectoroffset++

				if sectoroffset > int(bpb.sectorspercluster) {
					break
				}

			}

			var fatsectorforcurrentcluster = uint32(հաջորդՖայլcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Ընթերցում28(fatՍկիզբ+fatsectorforcurrentcluster, &fatbuf, 512)

			var fatoffsetՄեջsectorforcurrentcluster = հաջորդՖայլcluster % 128
			var սկիզբoffset = fatoffsetՄեջsectorforcurrentcluster * 4
			var վերջoffset = fatoffsetՄեջsectorforcurrentcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[սկիզբoffset:վերջoffset])

			հաջորդՖայլcluster = int32(Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer4)))
		}
	}
	հիշողությունmanager.Ազատ(bpbՑուցիչ)
	հիշողությունmanager.Ազատ(direntՑուցիչ)
}

type TՖայլապանակentryfat32 struct {
	անուն			[8]byte
	ext			[3]byte
	attributes		uint8
	reserved		uint8
	cԺամանակtenth		uint8
	cԺամանակ		uint16
	cdate			uint16
	aԺամանակ		uint16
	firstclusterhi		uint16
	wԺամանակ		uint16
	wdate			uint16
	firstclusterՑածր	uint16
	չափս			uint32
}

func (ինքնուրույն *TՖայլապանակentryfat32) Init(data [32]byte) {
	copy(ինքնուրույն.անուն[:8], data[0:8])
	copy(ինքնուրույն.ext[:3], data[8:11])
	ինքնուրույն.attributes = data[11]
	ինքնուրույն.reserved = data[12]
	ինքնուրույն.cԺամանակtenth = data[13]
	ինքնուրույն.cԺամանակ = uint16(data[14]) | uint16(data[15])<<8
	ինքնուրույն.cdate = uint16(data[16]) | uint16(data[17])<<8
	ինքնուրույն.aԺամանակ = uint16(data[18]) | uint16(data[19])<<8
	ինքնուրույն.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	ինքնուրույն.wԺամանակ = uint16(data[22]) | uint16(data[23])<<8
	ինքնուրույն.wdate = uint16(data[24]) | uint16(data[25])<<8
	ինքնուրույն.firstclusterՑածր = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	ինքնուրույն.չափս = Unsignedinteger32r(Զանգվածtounsignedinteger32(buffer))
}
