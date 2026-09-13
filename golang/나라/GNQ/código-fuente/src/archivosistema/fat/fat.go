package fat

import . "utilidad"
import . "consola"
import . "controlador/ata"
import . "archivosistema/msdospartición"
import . "memoriagestor"

type TParámetros_del_sistema_de_archivos32 struct {
	jmp			[3]uint8
	softNombre		[8]byte
	bytespersector		uint16
	sectorspercluster	uint8
	reservadosectors	uint16
	fatcopiar		uint8
	raízdirectorioentrada	uint16
	totalsectors		uint16
	soportetipo		uint8
	fatsectorRecuento	uint16
	sectorpertrack		uint16
	headRecuento		uint16
	ocultarsectors		uint32
	totalsectorRecuento	uint32

	tablaTamaño	uint32
	extBanderas	uint16
	fatVersión	uint16
	raízcluster	uint32
	fatInformación	uint16
	backupsector	uint16
	reservado0	[12]uint8
	driveNúmero	uint8
	reservado	uint8
	bootsignature	uint8
	volumenid	uint32
	volumenetiqueta	[11]byte
	fattipoetiqueta	[8]byte
}

func (propio *TParámetros_del_sistema_de_archivos32) Init(datos []byte) {
	copy(propio.jmp[:3], datos[0:3])
	copy(propio.softNombre[:8], datos[3:11])

	propio.bytespersector = (uint16(datos[11]) | uint16(datos[12])<<8)
	propio.sectorspercluster = datos[13]
	propio.reservadosectors = (uint16(datos[14]) | uint16(datos[15])<<8)
	propio.fatcopiar = datos[16]
	propio.raízdirectorioentrada = (uint16(datos[17]) | uint16(datos[18])<<8)
	propio.totalsectors = (uint16(datos[19]) | uint16(datos[20])<<8)
	propio.soportetipo = datos[21]
	propio.fatsectorRecuento = (uint16(datos[22]) | uint16(datos[23])<<8)
	propio.sectorpertrack = (uint16(datos[24]) | uint16(datos[25])<<8)
	propio.headRecuento = (uint16(datos[26]) | uint16(datos[27])<<8)

	var buffer1 [4]byte
	copy(buffer1[:4], datos[28:32])
	propio.ocultarsectors = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	copy(buffer1[:4], datos[32:36])
	propio.totalsectorRecuento = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	copy(buffer1[:4], datos[36:40])
	propio.tablaTamaño = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	propio.extBanderas = (uint16(datos[40]) | uint16(datos[41])<<8)
	propio.fatVersión = (uint16(datos[42]) | uint16(datos[43])<<8)

	copy(buffer1[:4], datos[44:48])
	propio.raízcluster = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	propio.fatInformación = (uint16(datos[48]) | uint16(datos[49])<<8)
	propio.backupsector = (uint16(datos[50]) | uint16(datos[51])<<8)

	copy(propio.reservado0[:12], datos[52:64])

	propio.driveNúmero = datos[64]
	propio.reservado = datos[65]
	propio.bootsignature = datos[66]

	copy(buffer1[:4], datos[67:71])
	propio.volumenid = Unsignedinteger32r(Matriztounsignedinteger32(buffer1))

	copy(propio.volumenetiqueta[:11], datos[71:82])
	copy(propio.fattipoetiqueta[:8], datos[82:90])

}

var consola_2 = TConsola{}

func (propio *TParámetros_del_sistema_de_archivos32) Len(hd *TAvanzadoTecnologíaattachment, partentrada TParticiónTablaentrada, nombredearchivo []byte) uint32 {

	if partentrada.Particiónid == 0x00 {
		return 0
	}

	memoriagestor := TMemoriagestor{}
	bpbPuntero := memoriagestor.Asignar_memoria(90)
	bpbbytes := GetbytesdesdePuntero(uintptr(bpbPuntero), 90, 90)
	var particiónDesplazamiento = partentrada.Iniciarlba

	hd.Leer28(particiónDesplazamiento, &bpbbytes, 90)

	var parámetros_del_sistema_de_archivos = TParámetros_del_sistema_de_archivos32{}
	parámetros_del_sistema_de_archivos.Init(bpbbytes)

	var fatIniciar = particiónDesplazamiento + uint32(parámetros_del_sistema_de_archivos.reservadosectors)
	var fatTamaño = parámetros_del_sistema_de_archivos.tablaTamaño

	var datosIniciar = fatIniciar + fatTamaño*uint32(parámetros_del_sistema_de_archivos.fatcopiar)

	var raízIniciar = datosIniciar + uint32(parámetros_del_sistema_de_archivos.sectorspercluster)*(parámetros_del_sistema_de_archivos.raízcluster-2)

	direntPuntero := memoriagestor.Asignar_memoria(512)
	direntbytes := GetbytesdesdePuntero(uintptr(direntPuntero), 512, 512)
	hd.Leer28(raízIniciar, &direntbytes, 512)

	var dirent = [16]TDirectorioentradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nombre[0] == 0x00 {
			break
		}

		if dirent[i].tamaño >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nombredearchivo, dirent[i].nombre[:len(nombredearchivo)]) {
			continue
		}

		memoriagestor.Libre(bpbPuntero)
		memoriagestor.Libre(direntPuntero)
		return dirent[i].tamaño
	}
	memoriagestor.Libre(bpbPuntero)
	memoriagestor.Libre(direntPuntero)
	return 0
}
func (propio *TParámetros_del_sistema_de_archivos32) Leer(hd *TAvanzadoTecnologíaattachment, partentrada TParticiónTablaentrada, nombredearchivo []byte, datos []byte) {

	if partentrada.Particiónid == 0x00 {
		return
	}

	memoriagestor := TMemoriagestor{}
	bpbPuntero := memoriagestor.Asignar_memoria(90)
	bpbbytes := GetbytesdesdePuntero(uintptr(bpbPuntero), 90, 90)
	var particiónDesplazamiento = partentrada.Iniciarlba

	hd.Leer28(particiónDesplazamiento, &bpbbytes, 90)

	var parámetros_del_sistema_de_archivos = TParámetros_del_sistema_de_archivos32{}
	parámetros_del_sistema_de_archivos.Init(bpbbytes)

	var fatIniciar = particiónDesplazamiento + uint32(parámetros_del_sistema_de_archivos.reservadosectors)
	var fatTamaño = parámetros_del_sistema_de_archivos.tablaTamaño

	var datosIniciar = fatIniciar + fatTamaño*uint32(parámetros_del_sistema_de_archivos.fatcopiar)

	var raízIniciar = datosIniciar + uint32(parámetros_del_sistema_de_archivos.sectorspercluster)*(parámetros_del_sistema_de_archivos.raízcluster-2)

	direntPuntero := memoriagestor.Asignar_memoria(512)
	direntbytes := GetbytesdesdePuntero(uintptr(direntPuntero), 512, 512)
	hd.Leer28(raízIniciar, &direntbytes, 512)

	var dirent = [16]TDirectorioentradafat32{}

	for i := 0; i < 16; i++ {

		var buffer3 [32]byte
		copy(buffer3[:32], direntbytes[i*32:(i+1)*32])
		dirent[i].Init(buffer3)

		if dirent[i].nombre[0] == 0x00 {
			break
		}

		if dirent[i].tamaño >= 0xFFFFFFFF {
			continue
		}

		if !Igualbytes(nombredearchivo, dirent[i].nombre[:len(nombredearchivo)]) {
			continue
		}

		var firstarchivocluster = (uint32(dirent[i].firstclusterhi)<<16 | uint32(dirent[i].firstclusterBaja))

		var Tamaño = int32(dirent[i].tamaño)
		var siguientearchivocluster = int32(firstarchivocluster)
		var buffer_2 [513]byte
		var fatbuffer [513]byte

		for Tamaño > 0 {
			var archivosector = datosIniciar + uint32(parámetros_del_sistema_de_archivos.sectorspercluster)*uint32(siguientearchivocluster-2)
			var sectorDesplazamiento int = 0

			for ; Tamaño > 0; Tamaño -= 512 {

				var buffer3 []byte

				if dirent[i].tamaño > 512 {
					buffer3 = buffer_2[:512]
					hd.Leer28(archivosector+uint32(sectorDesplazamiento), &buffer3, 512)

				} else {
					buffer3 = buffer_2[:dirent[i].tamaño]
					hd.Leer28(archivosector+uint32(sectorDesplazamiento), &buffer3, int(dirent[i].tamaño))
				}

				copy(datos[int32(dirent[i].tamaño)-Tamaño:], buffer3)

				sectorDesplazamiento++

				if sectorDesplazamiento > int(parámetros_del_sistema_de_archivos.sectorspercluster) {
					break
				}

			}

			var fatsectorforActualcluster = uint32(siguientearchivocluster / 128)
			var fatbuf = fatbuffer[:512]
			hd.Leer28(fatIniciar+fatsectorforActualcluster, &fatbuf, 512)

			var fatDesplazamientoEntradasectorforActualcluster = siguientearchivocluster % 128
			var iniciarDesplazamiento = fatDesplazamientoEntradasectorforActualcluster * 4
			var finDesplazamiento = fatDesplazamientoEntradasectorforActualcluster*4 + 4

			var buffer4 [4]byte
			copy(buffer4[:4], fatbuffer[iniciarDesplazamiento:finDesplazamiento])

			siguientearchivocluster = int32(Unsignedinteger32r(Matriztounsignedinteger32(buffer4)))
		}
	}
	memoriagestor.Libre(bpbPuntero)
	memoriagestor.Libre(direntPuntero)
}

type TDirectorioentradafat32 struct {
	nombre			[8]byte
	ext			[3]byte
	atributos		uint8
	reservado		uint8
	cHoratenth		uint8
	cHora			uint16
	cFecha			uint16
	aHora			uint16
	firstclusterhi		uint16
	wHora			uint16
	wFecha			uint16
	firstclusterBaja	uint16
	tamaño			uint32
}

func (propio *TDirectorioentradafat32) Init(datos [32]byte) {
	copy(propio.nombre[:8], datos[0:8])
	copy(propio.ext[:3], datos[8:11])
	propio.atributos = datos[11]
	propio.reservado = datos[12]
	propio.cHoratenth = datos[13]
	propio.cHora = uint16(datos[14]) | uint16(datos[15])<<8
	propio.cFecha = uint16(datos[16]) | uint16(datos[17])<<8
	propio.aHora = uint16(datos[18]) | uint16(datos[19])<<8
	propio.firstclusterhi = uint16(datos[20]) | uint16(datos[21])<<8
	propio.wHora = uint16(datos[22]) | uint16(datos[23])<<8
	propio.wFecha = uint16(datos[24]) | uint16(datos[25])<<8
	propio.firstclusterBaja = uint16(datos[26]) | uint16(datos[27])<<8

	var buffer [4]byte
	copy(buffer[:4], datos[28:32])
	propio.tamaño = Unsignedinteger32r(Matriztounsignedinteger32(buffer))
}
