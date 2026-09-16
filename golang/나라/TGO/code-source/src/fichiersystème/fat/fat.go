/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "utilitaire"
import . "console"
import . "pilote/ata"
import . "fichiersystème/msdospartition"
import . "mémoiregestionnaire"

type TParamètres_du_système_de_fichiers32 struct {
	jmp			[3]uint8
	softNom			[8]byte
	octetspersector		uint16
	sectorspercluster	uint8
	réservésectors		uint16
	fatcopier		uint8
	racinerépertoireélément	uint16
	totalsectors		uint16
	supportstype		uint8
	fatsectorNombre		uint16
	sectorpertrack		uint16
	headNombre		uint16
	masquésectors		uint32
	totalsectorNombre	uint32

	tableauTaille		uint32
	extAttributs		uint16
	fatversion		uint16
	racinecluster		uint32
	fatinfo			uint16
	backupsector		uint16
	réservé0		[12]uint8
	driveNombre		uint8
	réservé			uint8
	bootsignature		uint8
	volumeIdentifiant	uint32
	volumeétiquette		[11]byte
	fattypeétiquette	[8]byte
}

func (self *TParamètres_du_système_de_fichiers32) Init(données []byte) {
	copy(self.jmp[:3], données[0:3])
	copy(self.softNom[:8], données[3:11])

	self.octetspersector = (uint16(données[11]) | uint16(données[12])<<8)
	self.sectorspercluster = données[13]
	self.réservésectors = (uint16(données[14]) | uint16(données[15])<<8)
	self.fatcopier = données[16]
	self.racinerépertoireélément = (uint16(données[17]) | uint16(données[18])<<8)
	self.totalsectors = (uint16(données[19]) | uint16(données[20])<<8)
	self.supportstype = données[21]
	self.fatsectorNombre = (uint16(données[22]) | uint16(données[23])<<8)
	self.sectorpertrack = (uint16(données[24]) | uint16(données[25])<<8)
	self.headNombre = (uint16(données[26]) | uint16(données[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], données[28:32])
	self.masquésectors = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	copy(buffer1[:4], données[32:36])
	self.totalsectorNombre = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	copy(buffer1[:4], données[36:40])
	self.tableauTaille = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	self.extAttributs = (uint16(données[40]) | uint16(données[41])<<8)
	self.fatversion = (uint16(données[42]) | uint16(données[43])<<8)

	copy(buffer1[:4], données[44:48])
	self.racinecluster = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	self.fatinfo = (uint16(données[48]) | uint16(données[49])<<8)
	self.backupsector = (uint16(données[50]) | uint16(données[51])<<8)

	copy(self.réservé0[:12], données[52:64])

	self.driveNombre = données[64]
	self.réservé = données[65]
	self.bootsignature = données[66]

	copy(buffer1[:4], données[67:71])
	self.volumeIdentifiant = Unsignedinteger32r(Tableautounsignedinteger32(buffer1))

	copy(self.volumeétiquette[:11], données[71:82])
	copy(self.fattypeétiquette[:8], données[82:90])

}

var console_2 = TConsole{}

func (self *TParamètres_du_système_de_fichiers32) Len(hd *TAvancéTechnologieattachment, partélément TPartitionTableauélément, nomdefichier []byte) uint32 {

	if partélément.PartitionIdentifiant == 0x00 {
		return 0
	}

	mémoiregestionnaire := TMémoiregestionnaire{}
	bpbPointeur := mémoiregestionnaire.Allouer_la_mémoire(90)
	bpbOctets := GetOctetsdePointeur(uintptr(bpbPointeur), 90, 90)
	var partitionDécalage = partélément.Démarrerlba

	hd.Lire28(partitionDécalage, &bpbOctets, 90)

	var paramètres_du_système_de_fichiers = TParamètres_du_système_de_fichiers32{}
	paramètres_du_système_de_fichiers.Init(bpbOctets)

	var fatDémarrer = partitionDécalage + uint32(paramètres_du_système_de_fichiers.réservésectors)
	var fatTaille = paramètres_du_système_de_fichiers.tableauTaille

	var donnéesDémarrer = fatDémarrer + fatTaille*uint32(paramètres_du_système_de_fichiers.fatcopier)

	var racineDémarrer = donnéesDémarrer + uint32(paramètres_du_système_de_fichiers.sectorspercluster)*(paramètres_du_système_de_fichiers.racinecluster-2)

	direntPointeur := mémoiregestionnaire.Allouer_la_mémoire(512)
	direntOctets := GetOctetsdePointeur(uintptr(direntPointeur), 512, 512)
	hd.Lire28(racineDémarrer, &direntOctets, 512)

	var dirent = [16]TRépertoireélémentfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOctets[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nom[0] == 0x00 {
			break
		}

		if dirent[i].taille >= 0xFFFFFFFF {
			continue
		}

		if !ÉgalOctets(nomdefichier, dirent[i].nom[:len(nomdefichier)]) {
			continue
		}

		mémoiregestionnaire.Libre(bpbPointeur)
		mémoiregestionnaire.Libre(direntPointeur)
		return dirent[i].taille
	}
	mémoiregestionnaire.Libre(bpbPointeur)
	mémoiregestionnaire.Libre(direntPointeur)
	return 0
}
func (self *TParamètres_du_système_de_fichiers32) Lire(hd *TAvancéTechnologieattachment, partélément TPartitionTableauélément, nomdefichier []byte, données []byte) {

	if partélément.PartitionIdentifiant == 0x00 {
		return
	}

	mémoiregestionnaire := TMémoiregestionnaire{}
	bpbPointeur := mémoiregestionnaire.Allouer_la_mémoire(90)
	bpbOctets := GetOctetsdePointeur(uintptr(bpbPointeur), 90, 90)
	var partitionDécalage = partélément.Démarrerlba

	hd.Lire28(partitionDécalage, &bpbOctets, 90)

	var paramètres_du_système_de_fichiers = TParamètres_du_système_de_fichiers32{}
	paramètres_du_système_de_fichiers.Init(bpbOctets)

	var fatDémarrer = partitionDécalage + uint32(paramètres_du_système_de_fichiers.réservésectors)
	var fatTaille = paramètres_du_système_de_fichiers.tableauTaille

	var donnéesDémarrer = fatDémarrer + fatTaille*uint32(paramètres_du_système_de_fichiers.fatcopier)

	var racineDémarrer = donnéesDémarrer + uint32(paramètres_du_système_de_fichiers.sectorspercluster)*(paramètres_du_système_de_fichiers.racinecluster-2)

	direntPointeur := mémoiregestionnaire.Allouer_la_mémoire(512)
	direntOctets := GetOctetsdePointeur(uintptr(direntPointeur), 512, 512)
	hd.Lire28(racineDémarrer, &direntOctets, 512)

	var dirent = [16]TRépertoireélémentfat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntOctets[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nom[0] == 0x00 {
			break
		}

		if dirent[i].taille >= 0xFFFFFFFF {
			continue
		}

		if !ÉgalOctets(nomdefichier, dirent[i].nom[:len(nomdefichier)]) {
			continue
		}

		var firstfichiercluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterBasse))

		var Taille = int32(dirent[i].taille)
		var suivantfichiercluster = int32(firstfichiercluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Taille > 0 {
			var fichiersector = donnéesDémarrer + uint32(paramètres_du_système_de_fichiers.sectorspercluster)*uint32(suivantfichiercluster-2)
			var sectorDécalage int = 0

			for ; Taille > 0; Taille -= 512 {

				var buffer3 []byte

				if dirent[i].taille > 512 {
					buffer3 = buffer_2[:512]
					hd.Lire28(fichiersector+uint32(sectorDécalage), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].taille]
					hd.Lire28(fichiersector+uint32(sectorDécalage), &buffer3, int(dirent[i].taille))
				}

				copy(données[int32(dirent[i].taille)-Taille:], buffer3)

				sectorDécalage++

				if sectorDécalage > int(paramètres_du_système_de_fichiers.sectorspercluster) {
					break
				}

			}

			var fatsectorforCourantecluster = uint32(suivantfichiercluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Lire28(fatDémarrer+fatsectorforCourantecluster, &fatbuf, 512)

			var fatDécalageEntrantesectorforCourantecluster = suivantfichiercluster % 128
			var démarrerDécalage = fatDécalageEntrantesectorforCourantecluster * 4
			var finDécalage = fatDécalageEntrantesectorforCourantecluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[démarrerDécalage:finDécalage])

			suivantfichiercluster = int32(Unsignedinteger32r(Tableautounsignedinteger32(buffer4)))
		}
	}
	mémoiregestionnaire.Libre(bpbPointeur)
	mémoiregestionnaire.Libre(direntPointeur)
}

type TRépertoireélémentfat32 struct {
	nom			[8]byte
	ext			[3]byte
	attributs		uint8
	réservé			uint8
	cHeuretenth		uint8
	cHeure			uint16
	cdate			uint16
	aHeure			uint16
	firstclusterhi		uint16
	wHeure			uint16
	wdate			uint16
	firstclusterBasse	uint16
	taille			uint32
}

func (self *TRépertoireélémentfat32) Init(données [32]byte) {
	copy(self.nom[:8], données[0:8])
	copy(self.ext[:3], données[8:11])
	self.attributs = données[11]
	self.réservé = données[12]
	self.cHeuretenth = données[13]
	self.cHeure = uint16(données[14]) | uint16(données[15])<<8
	self.cdate = uint16(données[16]) | uint16(données[17])<<8
	self.aHeure = uint16(données[18]) | uint16(données[19])<<8
	self.firstclusterhi = uint16(données[20]) | uint16(données[21])<<8
	self.wHeure = uint16(données[22]) | uint16(données[23])<<8
	self.wdate = uint16(données[24]) | uint16(données[25])<<8
	self.firstclusterBasse = uint16(données[26]) | uint16(données[27])<<8

	var buffer [4]byte
	copy(buffer[:4], données[28:32])
	self.taille = Unsignedinteger32r(Tableautounsignedinteger32(buffer))
}
