package fat

import . "util"
import . "консоль"
import . "driver/ата"
import . "файлСистема/msdospartition"
import . "памятьmanager"

type TПараметри_файлової_системи32 struct {
	jmp			[3]uint8
	softНазва		[8]byte
	байтpersector		uint16
	sectorspercluster	uint8
	зарезервованаsectors	uint16
	fatКопіювати		uint8
	коріньТеказапис		uint16
	усьогоsectors		uint16
	носіїТип		uint8
	fatsectorВідлік		uint16
	sectorpertrack		uint16
	headВідлік		uint16
	прихованоsectors	uint32
	усьогоsectorВідлік	uint32

	таблицяРозмір		uint32
	extПрапори		uint16
	fatВерсія		uint16
	коріньcluster		uint32
	fatІнфо			uint16
	backupsector		uint16
	зарезервована0		[12]uint8
	driveЧисло		uint8
	зарезервована		uint8
	bootsignature		uint8
	гучністьІДЕНТИФІКАТОР	uint32
	гучністьмітка		[11]byte
	fatТипмітка		[8]byte
}

func (поточний *TПараметри_файлової_системи32) Init(data []byte) {
	copy(поточний.jmp[:3], data[0:3])
	copy(поточний.softНазва[:8], data[3:11])

	поточний.байтpersector = (uint16(data[11]) | uint16(data[12])<<8)
	поточний.sectorspercluster = data[13]
	поточний.зарезервованаsectors = (uint16(data[14]) | uint16(data[15])<<8)
	поточний.fatКопіювати = data[16]
	поточний.коріньТеказапис = (uint16(data[17]) | uint16(data[18])<<8)
	поточний.усьогоsectors = (uint16(data[19]) | uint16(data[20])<<8)
	поточний.носіїТип = data[21]
	поточний.fatsectorВідлік = (uint16(data[22]) | uint16(data[23])<<8)
	поточний.sectorpertrack = (uint16(data[24]) | uint16(data[25])<<8)
	поточний.headВідлік = (uint16(data[26]) | uint16(data[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], data[28:32])
	поточний.прихованоsectors = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	copy(buffer1[:4], data[32:36])
	поточний.усьогоsectorВідлік = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	copy(buffer1[:4], data[36:40])
	поточний.таблицяРозмір = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	поточний.extПрапори = (uint16(data[40]) | uint16(data[41])<<8)
	поточний.fatВерсія = (uint16(data[42]) | uint16(data[43])<<8)

	copy(buffer1[:4], data[44:48])
	поточний.коріньcluster = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	поточний.fatІнфо = (uint16(data[48]) | uint16(data[49])<<8)
	поточний.backupsector = (uint16(data[50]) | uint16(data[51])<<8)

	copy(поточний.зарезервована0[:12], data[52:64])

	поточний.driveЧисло = data[64]
	поточний.зарезервована = data[65]
	поточний.bootsignature = data[66]

	copy(buffer1[:4], data[67:71])
	поточний.гучністьІДЕНТИФІКАТОР = Unsignedinteger32r(Масивтоunsignedinteger32(buffer1))

	copy(поточний.гучністьмітка[:11], data[71:82])
	copy(поточний.fatТипмітка[:8], data[82:90])

}

var консоль_2 = TКонсоль{}

func (поточний *TПараметри_файлової_системи32) Len(hd *TДодатковоТехнологіяattachment, partзапис TPartitionТаблицязапис, назвафайлу []byte) uint32 {

	if partзапис.PartitionІДЕНТИФІКАТОР == 0x00 {
		return 0
	}

	памятьmanager := TПамятьmanager{}
	bpbВказівник := памятьmanager.Виділити_памʼять(90)
	bpbБайт := GetБайтзВказівник(uintptr(bpbВказівник), 90, 90)
	var partitionoffset = partзапис.Запуститиlba

	hd.Читання28(partitionoffset, &bpbБайт, 90)

	var параметри_файлової_системи = TПараметри_файлової_системи32{}
	параметри_файлової_системи.Init(bpbБайт)

	var fatЗапустити = partitionoffset + uint32(параметри_файлової_системи.зарезервованаsectors)
	var fatРозмір = параметри_файлової_системи.таблицяРозмір

	var dataЗапустити = fatЗапустити + fatРозмір*uint32(параметри_файлової_системи.fatКопіювати)

	var коріньЗапустити = dataЗапустити + uint32(параметри_файлової_системи.sectorspercluster)*(параметри_файлової_системи.коріньcluster-2)

	direntВказівник := памятьmanager.Виділити_памʼять(512)
	direntБайт := GetБайтзВказівник(uintptr(direntВказівник), 512, 512)
	hd.Читання28(коріньЗапустити, &direntБайт, 512)

	var dirent = [16]TТеказаписfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назва[0] == 0x00 {
			break
		}

		if dirent[i].розмір >= 0xFFFFFFFF {
			continue
		}

		if !РівноБайт(назвафайлу, dirent[i].назва[:len(назвафайлу)]) {
			continue
		}

		памятьmanager.Вільно(bpbВказівник)
		памятьmanager.Вільно(direntВказівник)
		return dirent[i].розмір
	}
	памятьmanager.Вільно(bpbВказівник)
	памятьmanager.Вільно(direntВказівник)
	return 0
}
func (поточний *TПараметри_файлової_системи32) Читання(hd *TДодатковоТехнологіяattachment, partзапис TPartitionТаблицязапис, назвафайлу []byte, data []byte) {

	if partзапис.PartitionІДЕНТИФІКАТОР == 0x00 {
		return
	}

	памятьmanager := TПамятьmanager{}
	bpbВказівник := памятьmanager.Виділити_памʼять(90)
	bpbБайт := GetБайтзВказівник(uintptr(bpbВказівник), 90, 90)
	var partitionoffset = partзапис.Запуститиlba

	hd.Читання28(partitionoffset, &bpbБайт, 90)

	var параметри_файлової_системи = TПараметри_файлової_системи32{}
	параметри_файлової_системи.Init(bpbБайт)

	var fatЗапустити = partitionoffset + uint32(параметри_файлової_системи.зарезервованаsectors)
	var fatРозмір = параметри_файлової_системи.таблицяРозмір

	var dataЗапустити = fatЗапустити + fatРозмір*uint32(параметри_файлової_системи.fatКопіювати)

	var коріньЗапустити = dataЗапустити + uint32(параметри_файлової_системи.sectorspercluster)*(параметри_файлової_системи.коріньcluster-2)

	direntВказівник := памятьmanager.Виділити_памʼять(512)
	direntБайт := GetБайтзВказівник(uintptr(direntВказівник), 512, 512)
	hd.Читання28(коріньЗапустити, &direntБайт, 512)

	var dirent = [16]TТеказаписfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].назва[0] == 0x00 {
			break
		}

		if dirent[i].розмір >= 0xFFFFFFFF {
			continue
		}

		if !РівноБайт(назвафайлу, dirent[i].назва[:len(назвафайлу)]) {
			continue
		}

		var firstФайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterНизька))

		var Розмір = int32(dirent[i].розмір)
		var наступнеФайлcluster = int32(firstФайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Розмір > 0 {
			var файлsector = dataЗапустити + uint32(параметри_файлової_системи.sectorspercluster)*uint32(наступнеФайлcluster-2)
			var sectoroffset int = 0

			for ; Розмір > 0; Розмір -= 512 {

				var buffer3 []byte

				if dirent[i].розмір > 512 {
					buffer3 = buffer_2[:512]
					hd.Читання28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].розмір]
					hd.Читання28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].розмір))
				}

				copy(data[int32(dirent[i].розмір)-Розмір:], buffer3)

				sectoroffset++

				if sectoroffset > int(параметри_файлової_системи.sectorspercluster) {
					break
				}

			}

			var fatsectorforПоточнаcluster = uint32(наступнеФайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Читання28(fatЗапустити+fatsectorforПоточнаcluster, &fatbuf, 512)

			var fatoffsetВхіднийsectorforПоточнаcluster = наступнеФайлcluster % 128
			var запуститиoffset = fatoffsetВхіднийsectorforПоточнаcluster * 4
			var кінецьoffset = fatoffsetВхіднийsectorforПоточнаcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[запуститиoffset:кінецьoffset])

			наступнеФайлcluster = int32(Unsignedinteger32r(Масивтоunsignedinteger32(buffer4)))
		}
	}
	памятьmanager.Вільно(bpbВказівник)
	памятьmanager.Вільно(direntВказівник)
}

type TТеказаписfat32 struct {
	назва			[8]byte
	ext			[3]byte
	атрибути		uint8
	зарезервована		uint8
	cЧасtenth		uint8
	cЧас			uint16
	cДата			uint16
	aЧас			uint16
	firstclusterhi		uint16
	wЧас			uint16
	wДата			uint16
	firstclusterНизька	uint16
	розмір			uint32
}

func (поточний *TТеказаписfat32) Init(data [32]byte) {
	copy(поточний.назва[:8], data[0:8])
	copy(поточний.ext[:3], data[8:11])
	поточний.атрибути = data[11]
	поточний.зарезервована = data[12]
	поточний.cЧасtenth = data[13]
	поточний.cЧас = uint16(data[14]) | uint16(data[15])<<8
	поточний.cДата = uint16(data[16]) | uint16(data[17])<<8
	поточний.aЧас = uint16(data[18]) | uint16(data[19])<<8
	поточний.firstclusterhi = uint16(data[20]) | uint16(data[21])<<8
	поточний.wЧас = uint16(data[22]) | uint16(data[23])<<8
	поточний.wДата = uint16(data[24]) | uint16(data[25])<<8
	поточний.firstclusterНизька = uint16(data[26]) | uint16(data[27])<<8

	var buffer [4]byte
	copy(buffer[:4], data[28:32])
	поточний.розмір = Unsignedinteger32r(Масивтоunsignedinteger32(buffer))
}
