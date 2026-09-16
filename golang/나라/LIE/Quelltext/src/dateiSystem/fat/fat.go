/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "hilfswerkzeug"
import . "konsole"
import . "treiber/ata"
import . "dateiSystem/msdosPartition"
import . "speicherVerwalter"

type TDateisystemparameter32 struct {
	jmp				[3]uint8
	softElementname			[8]byte
	bytepersector			uint16
	sectorspercluster		uint8
	reserviertsectors		uint16
	fatKopieren			uint8
	basisordnerOrdnerEintrag	uint16
	gesamtsectors			uint16
	datenträgerTyp			uint8
	fatsectorAnzahl			uint16
	sectorpertrack			uint16
	headAnzahl			uint16
	verstecktsectors		uint32
	gesamtsectorAnzahl		uint32

	tabelleGröße		uint32
	extOptionen		uint16
	fatversion		uint16
	basisordnercluster	uint32
	fatinfo			uint16
	backupsector		uint16
	reserviert0		[12]uint8
	driveNummer		uint8
	reserviert		uint8
	bootsignature		uint8
	lautstärkeKennung	uint32
	lautstärkeBeschriftung	[11]byte
	fatTypBeschriftung	[8]byte
}

func (selbst *TDateisystemparameter32) Init(daten []byte) {
	copy(selbst.jmp[:3], daten[0:3])
	copy(selbst.softElementname[:8], daten[3:11])

	selbst.bytepersector = (uint16(daten[11]) | uint16(daten[12])<<8)
	selbst.sectorspercluster = daten[13]
	selbst.reserviertsectors = (uint16(daten[14]) | uint16(daten[15])<<8)
	selbst.fatKopieren = daten[16]
	selbst.basisordnerOrdnerEintrag = (uint16(daten[17]) | uint16(daten[18])<<8)
	selbst.gesamtsectors = (uint16(daten[19]) | uint16(daten[20])<<8)
	selbst.datenträgerTyp = daten[21]
	selbst.fatsectorAnzahl = (uint16(daten[22]) | uint16(daten[23])<<8)
	selbst.sectorpertrack = (uint16(daten[24]) | uint16(daten[25])<<8)
	selbst.headAnzahl = (uint16(daten[26]) | uint16(daten[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], daten[28:32])
	selbst.verstecktsectors = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	copy(buffer1[:4], daten[32:36])
	selbst.gesamtsectorAnzahl = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	copy(buffer1[:4], daten[36:40])
	selbst.tabelleGröße = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	selbst.extOptionen = (uint16(daten[40]) | uint16(daten[41])<<8)
	selbst.fatversion = (uint16(daten[42]) | uint16(daten[43])<<8)

	copy(buffer1[:4], daten[44:48])
	selbst.basisordnercluster = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	selbst.fatinfo = (uint16(daten[48]) | uint16(daten[49])<<8)
	selbst.backupsector = (uint16(daten[50]) | uint16(daten[51])<<8)

	copy(selbst.reserviert0[:12], daten[52:64])

	selbst.driveNummer = daten[64]
	selbst.reserviert = daten[65]
	selbst.bootsignature = daten[66]

	copy(buffer1[:4], daten[67:71])
	selbst.lautstärkeKennung = Unsignedinteger32r(Feldtounsignedinteger32(buffer1))

	copy(selbst.lautstärkeBeschriftung[:11], daten[71:82])
	copy(selbst.fatTypBeschriftung[:8], daten[82:90])

}

var konsole_2 = TKonsole{}

func (selbst *TDateisystemparameter32) Len(hd *TErweitertTechnikattachment, partEintrag TPartitionTabelleEintrag, dateiname []byte) uint32 {

	if partEintrag.PartitionKennung == 0x00 {
		return 0
	}

	speicherVerwalter := TSpeicherVerwalter{}
	bpbZeiger := speicherVerwalter.Speicher_reservieren(90)
	bpbByte := GetBytevonZeiger(uintptr(bpbZeiger), 90, 90)
	var partitionVersatz = partEintrag.Startenlba

	hd.Lesen28(partitionVersatz, &bpbByte, 90)

	var dateisystemparameter = TDateisystemparameter32{}
	dateisystemparameter.Init(bpbByte)

	var fatStarten = partitionVersatz + uint32(dateisystemparameter.reserviertsectors)
	var fatGröße = dateisystemparameter.tabelleGröße

	var datenStarten = fatStarten + fatGröße*uint32(dateisystemparameter.fatKopieren)

	var basisordnerStarten = datenStarten + uint32(dateisystemparameter.sectorspercluster)*(dateisystemparameter.basisordnercluster-2)

	direntZeiger := speicherVerwalter.Speicher_reservieren(512)
	direntByte := GetBytevonZeiger(uintptr(direntZeiger), 512, 512)
	hd.Lesen28(basisordnerStarten, &direntByte, 512)

	var dirent = [16]TOrdnerEintragfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].elementname[0] == 0x00 {
			break
		}

		if dirent[i].größe >= 0xFFFFFFFF {
			continue
		}

		if !EntsprechendByte(dateiname, dirent[i].elementname[:len(dateiname)]) {
			continue
		}

		speicherVerwalter.Frei(bpbZeiger)
		speicherVerwalter.Frei(direntZeiger)
		return dirent[i].größe
	}
	speicherVerwalter.Frei(bpbZeiger)
	speicherVerwalter.Frei(direntZeiger)
	return 0
}
func (selbst *TDateisystemparameter32) Lesen(hd *TErweitertTechnikattachment, partEintrag TPartitionTabelleEintrag, dateiname []byte, daten []byte) {

	if partEintrag.PartitionKennung == 0x00 {
		return
	}

	speicherVerwalter := TSpeicherVerwalter{}
	bpbZeiger := speicherVerwalter.Speicher_reservieren(90)
	bpbByte := GetBytevonZeiger(uintptr(bpbZeiger), 90, 90)
	var partitionVersatz = partEintrag.Startenlba

	hd.Lesen28(partitionVersatz, &bpbByte, 90)

	var dateisystemparameter = TDateisystemparameter32{}
	dateisystemparameter.Init(bpbByte)

	var fatStarten = partitionVersatz + uint32(dateisystemparameter.reserviertsectors)
	var fatGröße = dateisystemparameter.tabelleGröße

	var datenStarten = fatStarten + fatGröße*uint32(dateisystemparameter.fatKopieren)

	var basisordnerStarten = datenStarten + uint32(dateisystemparameter.sectorspercluster)*(dateisystemparameter.basisordnercluster-2)

	direntZeiger := speicherVerwalter.Speicher_reservieren(512)
	direntByte := GetBytevonZeiger(uintptr(direntZeiger), 512, 512)
	hd.Lesen28(basisordnerStarten, &direntByte, 512)

	var dirent = [16]TOrdnerEintragfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntByte[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].elementname[0] == 0x00 {
			break
		}

		if dirent[i].größe >= 0xFFFFFFFF {
			continue
		}

		if !EntsprechendByte(dateiname, dirent[i].elementname[:len(dateiname)]) {
			continue
		}

		var firstDateicluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterNiedrig))

		var Größe = int32(dirent[i].größe)
		var weiterDateicluster = int32(firstDateicluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Größe > 0 {
			var dateisector = datenStarten + uint32(dateisystemparameter.sectorspercluster)*uint32(weiterDateicluster-2)
			var sectorVersatz int = 0

			for ; Größe > 0; Größe -= 512 {

				var buffer3 []byte

				if dirent[i].größe > 512 {
					buffer3 = buffer_2[:512]
					hd.Lesen28(dateisector+uint32(sectorVersatz), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].größe]
					hd.Lesen28(dateisector+uint32(sectorVersatz), &buffer3, int(dirent[i].größe))
				}

				copy(daten[int32(dirent[i].größe)-Größe:], buffer3)

				sectorVersatz++

				if sectorVersatz > int(dateisystemparameter.sectorspercluster) {
					break
				}

			}

			var fatsectorforSystemzeitcluster = uint32(weiterDateicluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lesen28(fatStarten+fatsectorforSystemzeitcluster, &fatbuf, 512)

			var fatVersatzEinsectorforSystemzeitcluster = weiterDateicluster % 128
			var startenVersatz = fatVersatzEinsectorforSystemzeitcluster * 4
			var endeVersatz = fatVersatzEinsectorforSystemzeitcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[startenVersatz:endeVersatz])

			weiterDateicluster = int32(Unsignedinteger32r(Feldtounsignedinteger32(buffer4)))
		}
	}
	speicherVerwalter.Frei(bpbZeiger)
	speicherVerwalter.Frei(direntZeiger)
}

type TOrdnerEintragfat32 struct {
	elementname		[8]byte
	ext			[3]byte
	attribute		uint8
	reserviert		uint8
	cZeittenth		uint8
	cZeit			uint16
	cDatum			uint16
	aZeit			uint16
	firstclusterhi		uint16
	wZeit			uint16
	wDatum			uint16
	firstclusterNiedrig	uint16
	größe			uint32
}

func (selbst *TOrdnerEintragfat32) Init(daten [32]byte) {
	copy(selbst.elementname[:8], daten[0:8])
	copy(selbst.ext[:3], daten[8:11])
	selbst.attribute = daten[11]
	selbst.reserviert = daten[12]
	selbst.cZeittenth = daten[13]
	selbst.cZeit = uint16(daten[14]) | uint16(daten[15])<<8
	selbst.cDatum = uint16(daten[16]) | uint16(daten[17])<<8
	selbst.aZeit = uint16(daten[18]) | uint16(daten[19])<<8
	selbst.firstclusterhi = uint16(daten[20]) | uint16(daten[21])<<8
	selbst.wZeit = uint16(daten[22]) | uint16(daten[23])<<8
	selbst.wDatum = uint16(daten[24]) | uint16(daten[25])<<8
	selbst.firstclusterNiedrig = uint16(daten[26]) | uint16(daten[27])<<8

	var buffer [4]byte
	copy(buffer[:4], daten[28:32])
	selbst.größe = Unsignedinteger32r(Feldtounsignedinteger32(buffer))
}
