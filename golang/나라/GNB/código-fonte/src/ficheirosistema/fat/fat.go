/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package fat

import . "utilitário"
import . "console"
import . "controlador/ata"
import . "ficheirosistema/msdospartição"
import . "memóriagestor"

type TParâmetros_do_sistema_de_ficheiros32 struct {
	jmp				[3]uint8
	softNome			[8]byte
	bytespersector			uint16
	sectorspercluster		uint8
	reservadosectors		uint16
	fatcopiar			uint8
	raizdiretóriopontodeentrada	uint16
	totalsectors			uint16
	mediatipo			uint8
	fatsectorContar			uint16
	sectorpertrack			uint16
	headContar			uint16
	ocultosectors			uint32
	totalsectorContar		uint32

	tabelaTamanho	uint32
	extParâmetros	uint16
	fatVersão	uint16
	raizcluster	uint32
	fatInformações	uint16
	backupsector	uint16
	reservado0	[12]uint8
	driveNúmero	uint8
	reservado	uint8
	bootsignature	uint8
	volumeid	uint32
	volumeEtiqueta	[11]byte
	fattipoEtiqueta	[8]byte
}

func (próprio *TParâmetros_do_sistema_de_ficheiros32) Init(dados []byte) {
	copy(próprio.jmp[:3], dados[0:3])
	copy(próprio.softNome[:8], dados[3:11])

	próprio.bytespersector = (uint16(dados[11]) | uint16(dados[12])<<8)
	próprio.sectorspercluster = dados[13]
	próprio.reservadosectors = (uint16(dados[14]) | uint16(dados[15])<<8)
	próprio.fatcopiar = dados[16]
	próprio.raizdiretóriopontodeentrada = (uint16(dados[17]) | uint16(dados[18])<<8)
	próprio.totalsectors = (uint16(dados[19]) | uint16(dados[20])<<8)
	próprio.mediatipo = dados[21]
	próprio.fatsectorContar = (uint16(dados[22]) | uint16(dados[23])<<8)
	próprio.sectorpertrack = (uint16(dados[24]) | uint16(dados[25])<<8)
	próprio.headContar = (uint16(dados[26]) | uint16(dados[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], dados[28:32])
	próprio.ocultosectors = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	copy(buffer1[:4], dados[32:36])
	próprio.totalsectorContar = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	copy(buffer1[:4], dados[36:40])
	próprio.tabelaTamanho = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	próprio.extParâmetros = (uint16(dados[40]) | uint16(dados[41])<<8)
	próprio.fatVersão = (uint16(dados[42]) | uint16(dados[43])<<8)

	copy(buffer1[:4], dados[44:48])
	próprio.raizcluster = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	próprio.fatInformações = (uint16(dados[48]) | uint16(dados[49])<<8)
	próprio.backupsector = (uint16(dados[50]) | uint16(dados[51])<<8)

	copy(próprio.reservado0[:12], dados[52:64])

	próprio.driveNúmero = dados[64]
	próprio.reservado = dados[65]
	próprio.bootsignature = dados[66]

	copy(buffer1[:4], dados[67:71])
	próprio.volumeid = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer1))

	copy(próprio.volumeEtiqueta[:11], dados[71:82])
	copy(próprio.fattipoEtiqueta[:8], dados[82:90])

}

var console_2 = TConsole{}

func (próprio *TParâmetros_do_sistema_de_ficheiros32) Len(hd *TAvançadoTecnologiaattachment, partpontodeentrada TPartiçãoTabelapontodeentrada, nomedoficheiro []byte) uint32 {

	if partpontodeentrada.Partiçãoid == 0x00 {
		return 0
	}

	memóriagestor := TMemóriagestor{}
	bpbPonteiro := memóriagestor.Alocar_memória(90)
	bpbbytes := GetbytesdePonteiro(uintptr(bpbPonteiro), 90, 90)
	var partiçãoDeslocamento = partpontodeentrada.Iniciarlba

	hd.Ler28(partiçãoDeslocamento, &bpbbytes, 90)

	var parâmetros_do_sistema_de_ficheiros = TParâmetros_do_sistema_de_ficheiros32{}
	parâmetros_do_sistema_de_ficheiros.Init(bpbbytes)

	var fatIniciar = partiçãoDeslocamento + uint32(parâmetros_do_sistema_de_ficheiros.reservadosectors)
	var fatTamanho = parâmetros_do_sistema_de_ficheiros.tabelaTamanho

	var dadosIniciar = fatIniciar + fatTamanho*uint32(parâmetros_do_sistema_de_ficheiros.fatcopiar)

	var raizIniciar = dadosIniciar + uint32(parâmetros_do_sistema_de_ficheiros.sectorspercluster)*(parâmetros_do_sistema_de_ficheiros.raizcluster-2)

	direntPonteiro := memóriagestor.Alocar_memória(512)
	direntbytes := GetbytesdePonteiro(uintptr(direntPonteiro), 512, 512)
	hd.Ler28(raizIniciar, &direntbytes, 512)

	var dirent = [16]TDiretóriopontodeentradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nome[0] == 0x00 {
			break
		}

		if dirent[i].tamanho >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nomedoficheiro, dirent[i].nome[:len(nomedoficheiro)]) {
			continue
		}

		memóriagestor.Livre(bpbPonteiro)
		memóriagestor.Livre(direntPonteiro)
		return dirent[i].tamanho
	}
	memóriagestor.Livre(bpbPonteiro)
	memóriagestor.Livre(direntPonteiro)
	return 0
}
func (próprio *TParâmetros_do_sistema_de_ficheiros32) Ler(hd *TAvançadoTecnologiaattachment, partpontodeentrada TPartiçãoTabelapontodeentrada, nomedoficheiro []byte, dados []byte) {

	if partpontodeentrada.Partiçãoid == 0x00 {
		return
	}

	memóriagestor := TMemóriagestor{}
	bpbPonteiro := memóriagestor.Alocar_memória(90)
	bpbbytes := GetbytesdePonteiro(uintptr(bpbPonteiro), 90, 90)
	var partiçãoDeslocamento = partpontodeentrada.Iniciarlba

	hd.Ler28(partiçãoDeslocamento, &bpbbytes, 90)

	var parâmetros_do_sistema_de_ficheiros = TParâmetros_do_sistema_de_ficheiros32{}
	parâmetros_do_sistema_de_ficheiros.Init(bpbbytes)

	var fatIniciar = partiçãoDeslocamento + uint32(parâmetros_do_sistema_de_ficheiros.reservadosectors)
	var fatTamanho = parâmetros_do_sistema_de_ficheiros.tabelaTamanho

	var dadosIniciar = fatIniciar + fatTamanho*uint32(parâmetros_do_sistema_de_ficheiros.fatcopiar)

	var raizIniciar = dadosIniciar + uint32(parâmetros_do_sistema_de_ficheiros.sectorspercluster)*(parâmetros_do_sistema_de_ficheiros.raizcluster-2)

	direntPonteiro := memóriagestor.Alocar_memória(512)
	direntbytes := GetbytesdePonteiro(uintptr(direntPonteiro), 512, 512)
	hd.Ler28(raizIniciar, &direntbytes, 512)

	var dirent = [16]TDiretóriopontodeentradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nome[0] == 0x00 {
			break
		}

		if dirent[i].tamanho >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nomedoficheiro, dirent[i].nome[:len(nomedoficheiro)]) {
			continue
		}

		var firstficheirocluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterBaixo))

		var Tamanho = int32(dirent[i].tamanho)
		var seguinteficheirocluster = int32(firstficheirocluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Tamanho > 0 {
			var ficheirosector = dadosIniciar + uint32(parâmetros_do_sistema_de_ficheiros.sectorspercluster)*uint32(seguinteficheirocluster-2)
			var sectorDeslocamento int = 0

			for ; Tamanho > 0; Tamanho -= 512 {

				var buffer3 []byte

				if dirent[i].tamanho > 512 {
					buffer3 = buffer_2[:512]
					hd.Ler28(ficheirosector+uint32(sectorDeslocamento), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].tamanho]
					hd.Ler28(ficheirosector+uint32(sectorDeslocamento), &buffer3, int(dirent[i].tamanho))
				}

				copy(dados[int32(dirent[i].tamanho)-Tamanho:], buffer3)

				sectorDeslocamento++

				if sectorDeslocamento > int(parâmetros_do_sistema_de_ficheiros.sectorspercluster) {
					break
				}

			}

			var fatsectorforAtualcluster = uint32(seguinteficheirocluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Ler28(fatIniciar+fatsectorforAtualcluster, &fatbuf, 512)

			var fatDeslocamentoEntradasectorforAtualcluster = seguinteficheirocluster % 128
			var iniciarDeslocamento = fatDeslocamentoEntradasectorforAtualcluster * 4
			var fimDeslocamento = fatDeslocamentoEntradasectorforAtualcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[iniciarDeslocamento:fimDeslocamento])

			seguinteficheirocluster = int32(Unsignedinteger32r(Matrizparaunsignedinteger32(buffer4)))
		}
	}
	memóriagestor.Livre(bpbPonteiro)
	memóriagestor.Livre(direntPonteiro)
}

type TDiretóriopontodeentradafat32 struct {
	nome			[8]byte
	ext			[3]byte
	attributes		uint8
	reservado		uint8
	cHoratenth		uint8
	cHora			uint16
	cData			uint16
	aHora			uint16
	firstclusterhi		uint16
	wHora			uint16
	wData			uint16
	firstclusterBaixo	uint16
	tamanho			uint32
}

func (próprio *TDiretóriopontodeentradafat32) Init(dados [32]byte) {
	copy(próprio.nome[:8], dados[0:8])
	copy(próprio.ext[:3], dados[8:11])
	próprio.attributes = dados[11]
	próprio.reservado = dados[12]
	próprio.cHoratenth = dados[13]
	próprio.cHora = uint16(dados[14]) | uint16(dados[15])<<8
	próprio.cData = uint16(dados[16]) | uint16(dados[17])<<8
	próprio.aHora = uint16(dados[18]) | uint16(dados[19])<<8
	próprio.firstclusterhi = uint16(dados[20]) | uint16(dados[21])<<8
	próprio.wHora = uint16(dados[22]) | uint16(dados[23])<<8
	próprio.wData = uint16(dados[24]) | uint16(dados[25])<<8
	próprio.firstclusterBaixo = uint16(dados[26]) | uint16(dados[27])<<8

	var buffer [4]byte
	copy(buffer[:4], dados[28:32])
	próprio.tamanho = Unsignedinteger32r(Matrizparaunsignedinteger32(buffer))
}
