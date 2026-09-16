/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "утилита"
import . "консоль"
import . "драйвер/ata"
import . "файлсистема/msdosразделДиска"
import . "памятьдиспетчер"

type TПараметры_файловой_системы32 struct {
	jmp				[3]uint8
	softИмя				[8]byte
	байтpersector			uint16
	sectorspercluster		uint8
	зарезервированнаяsectors	uint16
	fatкопировать			uint8
	коренькаталогзапись		uint16
	всегоsectors			uint16
	носителитип			uint8
	fatsectorКоличество		uint16
	sectorpertrack			uint16
	headКоличество			uint16
	скрытыеsectors			uint32
	всегоsectorКоличество		uint32

	таблицаРазмер		uint32
	extФлаги		uint16
	fatВерсия		uint16
	кореньcluster		uint32
	fatИнформация		uint16
	backupsector		uint16
	зарезервированная0	[12]uint8
	driveЧисло		uint8
	зарезервированная	uint8
	bootsignature		uint8
	громкостьИДЕНТИФИКАТОР	uint32
	громкостьметка		[11]byte
	fatтипметка		[8]byte
}

func (текущий *TПараметры_файловой_системы32) Init(данные []byte) {
	copy(текущий.jmp[:3], данные[0:3])
	copy(текущий.softИмя[:8], данные[3:11])

	текущий.байтpersector = (uint16(данные[11]) | uint16(данные[12])<<8)
	текущий.sectorspercluster = данные[13]
	текущий.зарезервированнаяsectors = (uint16(данные[14]) | uint16(данные[15])<<8)
	текущий.fatкопировать = данные[16]
	текущий.коренькаталогзапись = (uint16(данные[17]) | uint16(данные[18])<<8)
	текущий.всегоsectors = (uint16(данные[19]) | uint16(данные[20])<<8)
	текущий.носителитип = данные[21]
	текущий.fatsectorКоличество = (uint16(данные[22]) | uint16(данные[23])<<8)
	текущий.sectorpertrack = (uint16(данные[24]) | uint16(данные[25])<<8)
	текущий.headКоличество = (uint16(данные[26]) | uint16(данные[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], данные[28:32])
	текущий.скрытыеsectors = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	copy(buffer1[:4], данные[32:36])
	текущий.всегоsectorКоличество = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	copy(buffer1[:4], данные[36:40])
	текущий.таблицаРазмер = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	текущий.extФлаги = (uint16(данные[40]) | uint16(данные[41])<<8)
	текущий.fatВерсия = (uint16(данные[42]) | uint16(данные[43])<<8)

	copy(buffer1[:4], данные[44:48])
	текущий.кореньcluster = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	текущий.fatИнформация = (uint16(данные[48]) | uint16(данные[49])<<8)
	текущий.backupsector = (uint16(данные[50]) | uint16(данные[51])<<8)

	copy(текущий.зарезервированная0[:12], данные[52:64])

	текущий.driveЧисло = данные[64]
	текущий.зарезервированная = данные[65]
	текущий.bootsignature = данные[66]

	copy(buffer1[:4], данные[67:71])
	текущий.громкостьИДЕНТИФИКАТОР = Unsignedinteger32r(Массивкunsignedinteger32(buffer1))

	copy(текущий.громкостьметка[:11], данные[71:82])
	copy(текущий.fatтипметка[:8], данные[82:90])

}

var консоль_2 = TКонсоль{}

func (текущий *TПараметры_файловой_системы32) Len(hd *TДополнительноТехнологияattachment, partзапись TРазделДискаТаблицазапись, имяфайла []byte) uint32 {

	if partзапись.РазделДискаИДЕНТИФИКАТОР == 0x00 {
		return 0
	}

	памятьдиспетчер := TПамятьдиспетчер{}
	bpbУказатели := памятьдиспетчер.Выделить_память(90)
	bpbБайт := GetБайтfromУказатели(uintptr(bpbУказатели), 90, 90)
	var разделДискаoffset = partзапись.Пускlba

	hd.Читать28(разделДискаoffset, &bpbБайт, 90)

	var параметры_файловой_системы = TПараметры_файловой_системы32{}
	параметры_файловой_системы.Init(bpbБайт)

	var fatПуск = разделДискаoffset + uint32(параметры_файловой_системы.зарезервированнаяsectors)
	var fatРазмер = параметры_файловой_системы.таблицаРазмер

	var данныеПуск = fatПуск + fatРазмер*uint32(параметры_файловой_системы.fatкопировать)

	var кореньПуск = данныеПуск + uint32(параметры_файловой_системы.sectorspercluster)*(параметры_файловой_системы.кореньcluster-2)

	direntУказатели := памятьдиспетчер.Выделить_память(512)
	direntБайт := GetБайтfromУказатели(uintptr(direntУказатели), 512, 512)
	hd.Читать28(кореньПуск, &direntБайт, 512)

	var dirent = [16]TКаталогзаписьfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].имя[0] == 0x00 {
			break
		}

		if dirent[i].размер >= 0xFFFFFFFF {
			continue
		}

		if !РавныйБайт(имяфайла, dirent[i].имя[:len(имяфайла)]) {
			continue
		}

		памятьдиспетчер.Свободно(bpbУказатели)
		памятьдиспетчер.Свободно(direntУказатели)
		return dirent[i].размер
	}
	памятьдиспетчер.Свободно(bpbУказатели)
	памятьдиспетчер.Свободно(direntУказатели)
	return 0
}
func (текущий *TПараметры_файловой_системы32) Читать(hd *TДополнительноТехнологияattachment, partзапись TРазделДискаТаблицазапись, имяфайла []byte, данные []byte) {

	if partзапись.РазделДискаИДЕНТИФИКАТОР == 0x00 {
		return
	}

	памятьдиспетчер := TПамятьдиспетчер{}
	bpbУказатели := памятьдиспетчер.Выделить_память(90)
	bpbБайт := GetБайтfromУказатели(uintptr(bpbУказатели), 90, 90)
	var разделДискаoffset = partзапись.Пускlba

	hd.Читать28(разделДискаoffset, &bpbБайт, 90)

	var параметры_файловой_системы = TПараметры_файловой_системы32{}
	параметры_файловой_системы.Init(bpbБайт)

	var fatПуск = разделДискаoffset + uint32(параметры_файловой_системы.зарезервированнаяsectors)
	var fatРазмер = параметры_файловой_системы.таблицаРазмер

	var данныеПуск = fatПуск + fatРазмер*uint32(параметры_файловой_системы.fatкопировать)

	var кореньПуск = данныеПуск + uint32(параметры_файловой_системы.sectorspercluster)*(параметры_файловой_системы.кореньcluster-2)

	direntУказатели := памятьдиспетчер.Выделить_память(512)
	direntБайт := GetБайтfromУказатели(uintptr(direntУказатели), 512, 512)
	hd.Читать28(кореньПуск, &direntБайт, 512)

	var dirent = [16]TКаталогзаписьfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntБайт[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].имя[0] == 0x00 {
			break
		}

		if dirent[i].размер >= 0xFFFFFFFF {
			continue
		}

		if !РавныйБайт(имяфайла, dirent[i].имя[:len(имяфайла)]) {
			continue
		}

		var firstфайлcluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterНизкий))

		var Размер = int32(dirent[i].размер)
		var далеефайлcluster = int32(firstфайлcluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Размер > 0 {
			var файлsector = данныеПуск + uint32(параметры_файловой_системы.sectorspercluster)*uint32(далеефайлcluster-2)
			var sectoroffset int = 0

			for ; Размер > 0; Размер -= 512 {

				var buffer3 []byte

				if dirent[i].размер > 512 {
					buffer3 = buffer_2[:512]
					hd.Читать28(файлsector+uint32(sectoroffset), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].размер]
					hd.Читать28(файлsector+uint32(sectoroffset), &buffer3, int(dirent[i].размер))
				}

				copy(данные[int32(dirent[i].размер)-Размер:], buffer3)

				sectoroffset++

				if sectoroffset > int(параметры_файловой_системы.sectorspercluster) {
					break
				}

			}

			var fatsectorforТекущаядатаcluster = uint32(далеефайлcluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Читать28(fatПуск+fatsectorforТекущаядатаcluster, &fatbuf, 512)

			var fatoffsetИсходящийsectorforТекущаядатаcluster = далеефайлcluster % 128
			var пускoffset = fatoffsetИсходящийsectorforТекущаядатаcluster * 4
			var концеoffset = fatoffsetИсходящийsectorforТекущаядатаcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[пускoffset:концеoffset])

			далеефайлcluster = int32(Unsignedinteger32r(Массивкunsignedinteger32(buffer4)))
		}
	}
	памятьдиспетчер.Свободно(bpbУказатели)
	памятьдиспетчер.Свободно(direntУказатели)
}

type TКаталогзаписьfat32 struct {
	имя			[8]byte
	ext			[3]byte
	атрибуты		uint8
	зарезервированная	uint8
	cВремяtenth		uint8
	cВремя			uint16
	cДата			uint16
	aВремя			uint16
	firstclusterhi		uint16
	wВремя			uint16
	wДата			uint16
	firstclusterНизкий	uint16
	размер			uint32
}

func (текущий *TКаталогзаписьfat32) Init(данные [32]byte) {
	copy(текущий.имя[:8], данные[0:8])
	copy(текущий.ext[:3], данные[8:11])
	текущий.атрибуты = данные[11]
	текущий.зарезервированная = данные[12]
	текущий.cВремяtenth = данные[13]
	текущий.cВремя = uint16(данные[14]) | uint16(данные[15])<<8
	текущий.cДата = uint16(данные[16]) | uint16(данные[17])<<8
	текущий.aВремя = uint16(данные[18]) | uint16(данные[19])<<8
	текущий.firstclusterhi = uint16(данные[20]) | uint16(данные[21])<<8
	текущий.wВремя = uint16(данные[22]) | uint16(данные[23])<<8
	текущий.wДата = uint16(данные[24]) | uint16(данные[25])<<8
	текущий.firstclusterНизкий = uint16(данные[26]) | uint16(данные[27])<<8

	var buffer [4]byte
	copy(buffer[:4], данные[28:32])
	текущий.размер = Unsignedinteger32r(Массивкunsignedinteger32(buffer))
}
