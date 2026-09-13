package fat

import . "util"
import . "console"
import . "driver/ata"
import . "tậptinHệthống/msdospartition"
import . "bộnhớmanager"

type TTham_số_hệ_thống_tệp32 struct {
	jmp			[3]uint8
	softTên			[8]byte
	bytepersector		uint16
	sectorspercluster	uint8
	reservedsectors		uint16
	fatSaochép		uint8
	gốcThưmụcentry		uint16
	tổngsectors		uint16
	vậtchứaKiểu		uint8
	fatsectorSốlượng	uint16
	sectorpertrack		uint16
	headSốlượng		uint16
	ẩnsectors		uint32
	tổngsectorSốlượng	uint32

	bảngCỡ		uint32
	extCờ		uint16
	fatPhiênbản	uint16
	gốccluster	uint32
	fatThôngtin	uint16
	backupsector	uint16
	reserved0	[12]uint8
	driveSỐ		uint8
	reserved	uint8
	bootsignature	uint8
	ổđĩaMãsố	uint32
	ổđĩaNhãn	[11]byte
	fatKiểuNhãn	[8]byte
}

func (mình *TTham_số_hệ_thống_tệp32) Init(data []byte) {
	copy(mình.jmp[:3], data[0:3])
	copy(mình.softTên[:8], data[3:11])

	mình.bytepersector = (uint16(data[11]) | uint16(data[12])<<8)
	mình.sectorspercluster = data[13]
	mình.reservedsectors = (uint16(data[14]) | uint16(data[15])<<8)
	mình.fatSaochép = data[16]
	mình.gốcThưmụcentry = (uint16(data[17]) | uint16(data[18])<<8)
	mình.tổngsectors = (uint16(data[19]) | uint16(data[20])<<8)
	mình.vậtchứaKiểu = data[21]
	mình.fatsectorSốlượng = (uint16(data[22]) | uint16(data[23])<<8)
	mình.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	mình.headSốlượng = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	mình.ẩnsectors = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	mình.tổngsectorSốlượng = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	mình.bảngCỡ = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	mình.extCờ = (uint16(data[40]) | uint16(data[41])<<8)
	mình.fatPhiênbản = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	mình.gốccluster = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	mình.fatThôngtin = (uint16(data[48]) | uint16(data[49])<<8)
	mình.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(mình.reserved0[:12], data[52:64])

	mình.driveSỐ = data[64]
	mình.reserved = data[65]
	mình.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	mình.ổđĩaMãsố = Unsignedinteger32r(Mảngtounsignedinteger32(buffer1))

	copy(mình.ổđĩaNhãn[:11], data[71:82])
	copy(mình.fatKiểuNhãn[:8], data[82:90])

}

var console_2 = TConsole{}

func (mình *TTham_số_hệ_thống_tệp32) Len(hd *TNângcaoCôngnghệattachment, partentry TPartitionBảngentry, têntậptin []byte) uint32 {

	if partentry.PartitionMãsố == 0x00 {
		return 0
	}

	bộnhớmanager := TBộnhớmanager{}
	bpbContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(90)
	bpbByte := GetBytefromContrỏ(uintptr(bpbContrỏ), 90, 90)
	var partitionoffset = partentry.Chạylba

	hd.Đọc28(partitionoffset, &bpbByte, 90)

	var tham_số_hệ_thống_tệp = TTham_số_hệ_thống_tệp32{}
	tham_số_hệ_thống_tệp.Init(bpbByte)

	var fatChạy = partitionoffset + uint32(tham_số_hệ_thống_tệp.reservedsectors)
	var fatCỡ = tham_số_hệ_thống_tệp.bảngCỡ

	var dataChạy = fatChạy + fatCỡ*uint32(tham_số_hệ_thống_tệp.fatSaochép)

	var gốcChạy = dataChạy + uint32(tham_số_hệ_thống_tệp.sectorspercluster)*(tham_số_hệ_thống_tệp.gốccluster-2)

	direntContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(512)
	direntByte := GetBytefromContrỏ(uintptr(direntContrỏ), 512, 512)
	hd.Đọc28(gốcChạy, &direntByte, 512)

	var dirent = [16]TThưmụcentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].tên[0] == 0x00 {
			break
		}

		if dirent[i].cỡ >= 0xFFFFFFFF {
			continue
		}

		if !EqualByte(têntậptin, dirent[i].tên[:len(têntậptin)]) {
			continue
		}

		bộnhớmanager.Rảnh(bpbContrỏ)
		bộnhớmanager.Rảnh(direntContrỏ)
		return dirent[i].cỡ
	}
	bộnhớmanager.Rảnh(bpbContrỏ)
	bộnhớmanager.Rảnh(direntContrỏ)
	return 0
}
func (mình *TTham_số_hệ_thống_tệp32) Đọc(hd *TNângcaoCôngnghệattachment, partentry TPartitionBảngentry, têntậptin []byte, data []byte) {

	if partentry.PartitionMãsố == 0x00 {
		return
	}

	bộnhớmanager := TBộnhớmanager{}
	bpbContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(90)
	bpbByte := GetBytefromContrỏ(uintptr(bpbContrỏ), 90, 90)
	var partitionoffset = partentry.Chạylba

	hd.Đọc28(partitionoffset, &bpbByte, 90)

	var tham_số_hệ_thống_tệp = TTham_số_hệ_thống_tệp32{}
	tham_số_hệ_thống_tệp.Init(bpbByte)

	var fatChạy = partitionoffset + uint32(tham_số_hệ_thống_tệp.reservedsectors)
	var fatCỡ = tham_số_hệ_thống_tệp.bảngCỡ

	var dataChạy = fatChạy + fatCỡ*uint32(tham_số_hệ_thống_tệp.fatSaochép)

	var gốcChạy = dataChạy + uint32(tham_số_hệ_thống_tệp.sectorspercluster)*(tham_số_hệ_thống_tệp.gốccluster-2)

	direntContrỏ := bộnhớmanager.Cấp_phát_bộ_nhớ(512)
	direntByte := GetBytefromContrỏ(uintptr(direntContrỏ), 512, 512)
	hd.Đọc28(gốcChạy, &direntByte, 512)

	var dirent = [16]TThưmụcentryfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].tên[0] == 0x00 {
			break
		}

		if dirent[i].cỡ >= 0xFFFFFFFF {
			continue
		}

		if !EqualByte(têntậptin, dirent[i].tên[:len(têntậptin)]) {
			continue
		}

		var đầuTậptincluster = (uint32(dirent[i].đầuclusterhi)<<16 | uint32(dirent[i].đầuclusterThấp))

		var Cỡ = int32(dirent[i].cỡ)
		var kếTậptincluster = int32(đầuTậptincluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Cỡ > 0 {
			var tậptinsector = dataChạy + uint32(tham_số_hệ_thống_tệp.sectorspercluster)*uint32(kếTậptincluster-2)
			var sectoroffset int = 0

			for ; Cỡ > 0; Cỡ -= 512 {

				var buffer3 []byte

				if dirent[i].cỡ > 512 {
					buffer3 = buffer_2[:512]
					hd.Đọc28(tậptinsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].cỡ]
					hd.Đọc28(tậptinsector+uint32(sectoroffset), &buffer3, int(dirent[i].cỡ))
				}

				copy(data[int32(dirent[i].cỡ)-Cỡ:], buffer3)

				sectoroffset++

				if sectoroffset > int(tham_số_hệ_thống_tệp.sectorspercluster) {
					break
				}

			}

			var fatsectorforHiệnhànhcluster = uint32(kếTậptincluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Đọc28(fatChạy+fatsectorforHiệnhànhcluster, &fatbuf, 512)

			var fatoffsetVàosectorforHiệnhànhcluster = kếTậptincluster % 128
			var chạyoffset = fatoffsetVàosectorforHiệnhànhcluster * 4
			var kếtthúcoffset = fatoffsetVàosectorforHiệnhànhcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[chạyoffset:kếtthúcoffset])

			kếTậptincluster = int32(Unsignedinteger32r(Mảngtounsignedinteger32(buffer4)))
		}
	}
	bộnhớmanager.Rảnh(bpbContrỏ)
	bộnhớmanager.Rảnh(direntContrỏ)
}

type TThưmụcentryfat32 struct {
	tên		[8]byte
	ext		[3]byte
	attributes	uint8
	reserved	uint8
	cGiờtenth	uint8
	cGiờ		uint16
	cNgàytháng	uint16
	aGiờ		uint16
	đầuclusterhi	uint16
	wGiờ		uint16
	wNgàytháng	uint16
	đầuclusterThấp	uint16
	cỡ		uint32
}

func (mình *TThưmụcentryfat32) Init(data [32]byte) {
	copy(mình.tên[:8], data[0:8])
	copy(mình.ext[:3], data[8:11])
	mình.attributes = data[11]
	mình.reserved = data[12]
	mình.cGiờtenth = data[13]
	mình.cGiờ = uint16(data[14]) | uint16(data[15])<<8
	mình.cNgàytháng = uint16(data[16]) | uint16(data[17])<<8
	mình.aGiờ = uint16(data[18]) | uint16(data[19])<<8
	mình.đầuclusterhi = uint16(data[20]) | uint16(data[21])<<8
	mình.wGiờ = uint16(data[22]) | uint16(data[23])<<8
	mình.wNgàytháng = uint16(data[24]) | uint16(data[25])<<8
	mình.đầuclusterThấp = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	mình.cỡ = Unsignedinteger32r(Mảngtounsignedinteger32(buffer))
}
