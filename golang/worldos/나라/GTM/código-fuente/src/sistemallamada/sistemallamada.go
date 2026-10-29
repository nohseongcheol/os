/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemallamada

import . "unsafe"

import . "interrupción"
import . "consola"
import . "utilidad"
import . "múltiplegestiónTareas"
import . "controlador/ata"
import . "archivosistema/msdospartición"
import . "archivosistema/fat"
import . "archivosistema/formato_ejecutable_y_enlazable"
import mem "memoriagestor"
import . "paginación"
import . "puerto"
import . "gestiónTareas/planificador"
import . "gestiónTareas/hilo"
import . "virtualmemoria"

var consola_2 = TConsola{}

type TSyscall struct {
	TInterrupciónhandler
}

const (
	SysSalir	uint32	= 1
	Sysfork		uint32	= 2
	Sysleer		uint32	= 3
	Sysescribir	uint32	= 4
	Sysabrir	uint32	= 5
	Syscerrar	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysacceso	uint32	= 33
	Syssync		uint32	= 36
	Sysdup		uint32	= 41
	Sysbrk		uint32	= 45
	Sysgetgid	uint32	= 47
	Sysgeteuid	uint32	= 49
	Sysgetegid	uint32	= 50
	Sysfcntl	uint32	= 55
	Sysdup2		uint32	= 63
	Sysgetppid	uint32	= 64
	Syssocketcall	uint32	= 102
	Sysstat		uint32	= 106
	Syslstat	uint32	= 107
	Sysfstat	uint32	= 108
	Sysfsync	uint32	= 118
	Sysuname	uint32	= 122
	Sysgetcwd	uint32	= 183
	SysrtSalir	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2big		int32	= -7
	Enoexec		int32	= -8
	Ebadf		int32	= -9
	Echild		int32	= -10
	Eagain		int32	= -11
	Enomem		int32	= -12
	Eacces		int32	= -13
	Efault		int32	= -14
	Ebusy		int32	= -16
	Eexist		int32	= -17
	Enodev		int32	= -19
	Enotdir		int32	= -20
	Eisdir		int32	= -21
	Einval		int32	= -22
	Enfile		int32	= -23
	Emfile		int32	= -24
	Enotty		int32	= -25
	Efbig		int32	= -27
	Enospc		int32	= -28
	Espipe		int32	= -29
	Erofs		int32	= -30
	Erange		int32	= -34
	Enosys		int32	= -38
	Emsgsize	int32	= -90
	Eprotonosupport	int32	= -93
	Eopnotsupp	int32	= -95
	Eafnosupport	int32	= -97
	Eaddrinuse	int32	= -98
	Enetunreach	int32	= -101
	Enotconn	int32	= -107
)

const (
	stdinDescriptor		int32	= 0
	stdoutDescriptor	int32	= 1
	stderrDescriptor	int32	= 2
	máxDescriptor			= 32
	máxabrirARCHIVOS		= 128
)

type descriptorentrada struct {
	enuso			bool
	descripción		int32
	descriptorBanderas	uint32
}

type abrirarchivoDescripción struct {
	enuso		bool
	refs		uint32
	tipo		uint32
	banderas	uint32
	posición	uint32
	tamaño		uint32
	nombre		[12]byte
	nombrelen	uint32
	aux		uint32
}

const (
	descriptorTipoNinguno		uint32	= 0
	descriptorTipofat		uint32	= 1
	descriptorTipostdin		uint32	= 2
	descriptorTipoconsola		uint32	= 3
	descriptorTipoRaízdirectorio	uint32	= 4
	descriptorTipoconectorRed	uint32	= 5

	oleersolo	uint32	= 0
	oescribirsolo	uint32	= 1
	oleerescribir	uint32	= 2
	ocrear		uint32	= 0x40
	oTruncar	uint32	= 0x200
	oappend		uint32	= 0x400
	odirectorio	uint32	= 0x10000

	seekestablecer	uint32	= 0
	seekActual	uint32	= 1
	seekFin		uint32	= 2

	fdupDescriptor		uint32	= 0
	fgetDescriptor		uint32	= 1
	festablecerDescriptor	uint32	= 2
	fgetfl			uint32	= 3
	festablecerfl		uint32	= 4
	descriptorcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet			= 2
	sockdatagram		= 2
	ipprotocoludp		= 17
	máxsockets		= 32
	máxconectorRedpaquetes	= 8
	máxdatagramTamaño	= 512
)

type conectorRedDireccióniVp4 struct {
	Family		uint16
	Puerto		uint16
	Dirección	uint32
	Cero		[8]byte
}

type conectorRedPAQUETE struct {
	enuso	bool
	tamaño	uint32
	origen	conectorRedDireccióniVp4
	datos	[máxdatagramTamaño]byte
}

type localdatagramconectorRed struct {
	enuso		bool
	bound		bool
	connected	bool
	local		conectorRedDireccióniVp4
	remoto		conectorRedDireccióniVp4
	head		uint32
	tail		uint32
	recuento	uint32
	paquetes	[máxconectorRedpaquetes]conectorRedPAQUETE
}

type posixstat struct {
	Dispositivo	uint32
	Ino		uint32
	Modo		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Tamaño_2	int32
	Blksize		int32
	Bloque		int32
	Atime		int32
	Atimensec	int32
	Mtime		int32
	Mtimensec	int32
	Ctime		int32
	Ctimensec	int32
}

type posixutsname struct {
	Sysname		[65]byte
	Nodename	[65]byte
	Release		[65]byte
	Versión		[65]byte
	Machine		[65]byte
}

const (
	máxEjecutarvectorentrada	= 16
	máxEjecutarCadenaDuración	= 63
)

type ejecutarvector struct {
	recuento	uint32
	lengths		[máxEjecutarvectorentrada]uint32
	valores		[máxEjecutarvectorentrada][máxEjecutarCadenaDuración + 1]byte
}

type procesoentrada struct {
	enuso		bool
	pid		uint32
	padre		uint32
	salió		bool
	estado		uint32
	programabreak	uint32
	fds		[máxDescriptor]descriptorentrada
}

type cadenaencabezado struct {
	Data	uintptr
	Len	int
}

func syscallerror(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var abrirarchivoTabla [máxabrirARCHIVOS]abrirarchivoDescripción
var procesoTabla [32]procesoentrada
var localsockets [máxsockets]localdatagramconectorRed
var siguienteephemeralpuerto uint16 = 49152

const (
	usuarioheapbase		uint32	= 0x06000000
	usuarioheapLimitar	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinleer uint32
var stdinescribir uint32

func Interrupción(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysSalir_2(índice uint32) {
	Syscall(SysSalir, índice)
}

func Sysleer_2(descriptor_2 uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysleer, descriptor_2, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysImprimirstr(buffer string) {
	h := (*cadenaencabezado)(Pointer(&buffer))
	Syscall(Sysescribir, uint32(stdoutDescriptor), uint32(h.Data), uint32(h.Len))
}

func SysImprimirunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysescribir, uint32(stdoutDescriptor), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysabrir_2(rUTA uintptr, banderas uint32, modo uint32) int32 {
	return int32(Syscall(Sysabrir, uint32(rUTA), banderas, modo))
}

func Syscerrar_2(descriptor_2 uint32) int32 {
	return int32(Syscall(Syscerrar, descriptor_2))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(dirección uint32) uint32 {
	return Syscall(Sysbrk, dirección)
}

func Syscall(parámetros ...uint32) uint32 {

	l := len(parámetros)
	switch l {
	case 1:
		return Interrupción(parámetros[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupción(parámetros[0], parámetros[1], 0, 0, 0, 0)
	case 3:
		return Interrupción(parámetros[0], parámetros[1], parámetros[2], 0, 0, 0)
	case 4:
		return Interrupción(parámetros[0], parámetros[1], parámetros[2], parámetros[3], 0, 0)
	case 5:
		return Interrupción(parámetros[0], parámetros[1], parámetros[2], parámetros[3], parámetros[4], 0)
	case 6:
		return Interrupción(parámetros[0], parámetros[1], parámetros[2], parámetros[3], parámetros[4], parámetros[5])
	default:
		return syscallerror(Enosys)
	}
}

func (propio *TSyscall) Init(gestor *TInterrupcióngestor) {
	initarchivodescriptor()

	interrupciónhandler = manijainterrupción

	var dirección uintptr
	dirección = uintptr(Pointer(&interrupciónhandler))

	propio.TInterrupciónhandler.Init(0x80, uintptr(Pointer(gestor)), dirección)
}

var interrupciónhandler func(uint32) uint32

func manijainterrupción(esp uint32) uint32 {
	var cpu = (*TcpuEstado)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysSalir:
		sysSalir(cpu.Ebx)
		return uint32(uintptr(Pointer(DetenerActualhilo(cpu))))
	case SysrtSalir:
		sysSalir(cpu.Ebx)
		return uint32(uintptr(Pointer(DetenerActualhilo(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysleer:
		cpu.Eax = uint32(sysleer(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysescribir:
		cpu.Eax = uint32(sysescribir(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysabrir:
		cpu.Eax = uint32(sysabrir(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysabrir(cpu.Ebx, ocrear|oescribirsolo|oTruncar, cpu.Ecx))
		return esp
	case Syscerrar:
		cpu.Eax = uint32(syscerrar(int32(cpu.Ebx)))
		return esp
	case Syswaitpid:
		cpu.Eax = uint32(syswaitpid(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Syslseek:
		cpu.Eax = uint32(syslseek(int32(cpu.Ebx), int32(cpu.Ecx), cpu.Edx))
		return esp
	case Sysexecve:
		cpu.Eax = uint32(sysexecve(cpu, cpu.Ebx))
		return esp
	case Sysgetpid:
		cpu.Eax = Actualpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Actualpadrepid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysacceso:
		cpu.Eax = uint32(sysacceso(cpu.Ebx, cpu.Ecx))
		return esp
	case Syschdir:
		cpu.Eax = uint32(syschdir(cpu.Ebx))
		return esp
	case Sysgetcwd:
		cpu.Eax = uint32(sysgetcwd(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysdup:
		cpu.Eax = uint32(sysdup(int32(cpu.Ebx), 0))
		return esp
	case Sysdup2:
		cpu.Eax = uint32(sysdup2(int32(cpu.Ebx), int32(cpu.Ecx)))
		return esp
	case Syssocketcall:
		cpu.Eax = uint32(sysconectorRedllamada(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfcntl:
		cpu.Eax = uint32(sysfcntl(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysstat, Syslstat:
		cpu.Eax = uint32(sysstat(cpu.Ebx, cpu.Ecx))
		return esp
	case Sysfstat:
		cpu.Eax = uint32(sysfstat(int32(cpu.Ebx), cpu.Ecx))
		return esp
	case Sysfsync:
		cpu.Eax = uint32(sysfsync(int32(cpu.Ebx)))
		return esp
	case Syssync:
		cpu.Eax = 0
		return esp
	case Sysuname:
		cpu.Eax = uint32(sysuname(cpu.Ebx))
		return esp
	case Sysbrk:
		cpu.Eax = sysbrk(cpu.Ebx)
		return esp
	case 9:
		consola_2.MUnsignedinteger32Imprimir(cpu.Ebx)
		return esp

	default:
		consola_2.MImprimirxy(([]byte)("sys["), 1, 23)
		consola_2.MUnsignedinteger32Imprimir(esp)
		consola_2.MImprimir(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimir(cpu.Eax)
		consola_2.MImprimir(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimir(cpu.Ebx)
		consola_2.MImprimir(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimir(cpu.Ecx)
		consola_2.MImprimir(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimir(cpu.Edx)
		consola_2.MImprimir(([]byte)("]"))
		cpu.Eax = syscallerror(Enosys)
		return esp
	}

	return esp
}

func initarchivodescriptor() {
	for i := 0; i < máxabrirARCHIVOS; i++ {
		abrirarchivoTabla[i] = abrirarchivoDescripción{}
	}
	for i := 0; i < len(procesoTabla); i++ {
		procesoTabla[i] = procesoentrada{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramconectorRed{}
	}
	siguienteephemeralpuerto = 49152
	abrirarchivoTabla[0] = abrirarchivoDescripción{enuso: true, tipo: descriptorTipostdin, banderas: oleersolo}
	abrirarchivoTabla[1] = abrirarchivoDescripción{enuso: true, tipo: descriptorTipoconsola, banderas: oescribirsolo}
	abrirarchivoTabla[2] = abrirarchivoDescripción{enuso: true, tipo: descriptorTipoconsola, banderas: oescribirsolo}
}

func buscarproceso(pid uint32) *procesoentrada {
	for i := 0; i < len(procesoTabla); i++ {
		if procesoTabla[i].enuso && procesoTabla[i].pid == pid {
			return &procesoTabla[i]
		}
	}
	return nil
}

func initializeprocesofds(proceso *procesoentrada) {
	for descriptor_2 := int32(0); descriptor_2 <= stderrDescriptor; descriptor_2++ {
		proceso.fds[descriptor_2] = descriptorentrada{enuso: true, descripción: descriptor_2}
		abrirarchivoTabla[descriptor_2].refs++
	}
}

func ensureActualproceso() *procesoentrada {
	pid := Actualpid()
	if proceso := buscarproceso(pid); proceso != nil {
		return proceso
	}
	for i := 0; i < len(procesoTabla); i++ {
		if !procesoTabla[i].enuso {
			procesoTabla[i] = procesoentrada{
				enuso:		true,
				pid:		pid,
				padre:		Actualpadrepid(),
				programabreak:	usuarioheapbase,
			}
			initializeprocesofds(&procesoTabla[i])
			return &procesoTabla[i]
		}
	}
	return nil
}

func getabrirarchivofor(proceso *procesoentrada, descriptor_2 int32) *abrirarchivoDescripción {
	if proceso == nil || descriptor_2 < 0 || descriptor_2 >= máxDescriptor || !proceso.fds[descriptor_2].enuso {
		return nil
	}
	descripción := proceso.fds[descriptor_2].descripción
	if descripción < 0 || descripción >= máxabrirARCHIVOS || !abrirarchivoTabla[descripción].enuso {
		return nil
	}
	return &abrirarchivoTabla[descripción]
}

func getabrirarchivo(descriptor_2 int32) *abrirarchivoDescripción {
	return getabrirarchivofor(ensureActualproceso(), descriptor_2)
}

func allocateabrirarchivo() int32 {
	for i := int32(3); i < máxabrirARCHIVOS; i++ {
		if !abrirarchivoTabla[i].enuso {
			abrirarchivoTabla[i] = abrirarchivoDescripción{enuso: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateDescriptor(proceso *procesoentrada, descripción int32, mínimo int32) int32 {
	if proceso == nil {
		return Enfile
	}
	if mínimo < 0 || mínimo >= máxDescriptor {
		return Einval
	}
	for descriptor_2 := mínimo; descriptor_2 < máxDescriptor; descriptor_2++ {
		if !proceso.fds[descriptor_2].enuso {
			proceso.fds[descriptor_2] = descriptorentrada{enuso: true, descripción: descripción}
			return descriptor_2
		}
	}
	return Emfile
}

func releaseabrirarchivo(descripción int32) {
	if descripción < 0 || descripción >= máxabrirARCHIVOS {
		return
	}
	entrada := &abrirarchivoTabla[descripción]
	if entrada.refs > 0 {
		entrada.refs--
	}

	if entrada.refs == 0 && descripción > stderrDescriptor {
		if entrada.tipo == descriptorTipoconectorRed && entrada.aux < máxsockets {
			localsockets[entrada.aux] = localdatagramconectorRed{}
		}
		*entrada = abrirarchivoDescripción{}
	}
}

func cerrarprocesoDescriptor(proceso *procesoentrada, descriptor_2 int32) int32 {
	if proceso == nil || getabrirarchivofor(proceso, descriptor_2) == nil {
		return Ebadf
	}
	descripción := proceso.fds[descriptor_2].descripción
	proceso.fds[descriptor_2] = descriptorentrada{}
	releaseabrirarchivo(descripción)
	return 0
}

func sysescribir(descriptor_2 int32, dirección uint32, recuento uint32) int32 {
	if recuento == 0 {
		return 0
	}
	if dirección == 0 || dirección+recuento < dirección {
		return Efault
	}
	if recuento > 4096 {
		return Einval
	}
	entrada := getabrirarchivo(descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	if entrada.tipo != descriptorTipoconsola {
		if entrada.tipo == descriptorTipoconectorRed {
			return conectorRedEnviarto(descriptor_2, dirección, recuento, 0, 0)
		}
		if entrada.tipo == descriptorTipofat || entrada.tipo == descriptorTipoRaízdirectorio {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesdesdePuntero(uintptr(dirección), int(recuento), int(recuento))
	consola_2.MImprimir(buffer)
	return int32(recuento)
}

func sysleer(descriptor_2 int32, dirección uint32, recuento uint32) int32 {
	if recuento == 0 {
		return 0
	}
	if dirección == 0 || dirección+recuento < dirección {
		return Efault
	}
	entrada := getabrirarchivo(descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	if entrada.tipo == descriptorTipostdin {
		return leerstdin(dirección, recuento)
	}
	if entrada.tipo == descriptorTipoRaízdirectorio {
		return Eisdir
	}
	if entrada.tipo == descriptorTipoconectorRed {
		return conectorRedreceivedesde(descriptor_2, dirección, recuento, 0, 0)
	}
	if entrada.tipo != descriptorTipofat {
		return Ebadf
	}
	if entrada.posición >= entrada.tamaño {
		return 0
	}
	remaining := entrada.tamaño - entrada.posición
	if recuento > remaining {
		recuento = remaining
	}
	buffer := GetbytesdesdePuntero(uintptr(dirección), int(recuento), int(recuento))
	return leervfsarchivo(entrada, buffer, recuento)
}

func sysabrir(rUTADirección uint32, banderas uint32, modo uint32) int32 {
	_ = modo
	if rUTADirección == 0 {
		return Efault
	}
	accesomodo := banderas & 3
	if accesomodo == oescribirsolo || accesomodo == oleerescribir || (banderas&(ocrear|oTruncar|oappend)) != 0 {
		return Erofs
	}

	proceso := ensureActualproceso()
	if proceso == nil {
		return Enfile
	}
	descripción := allocateabrirarchivo()
	if descripción < 0 {
		return descripción
	}
	entrada := &abrirarchivoTabla[descripción]
	entrada.banderas = banderas
	if isRaízRUTA(rUTADirección) {
		entrada.tipo = descriptorTipoRaízdirectorio
		entrada.tamaño = 0
	} else {
		nombrelen, nombre := copiarRUTA(rUTADirección)
		if nombrelen == 0 {
			*entrada = abrirarchivoDescripción{}
			return Enoent
		}
		tamaño := archivoTamaño(nombre[:nombrelen])
		if tamaño == 0 {
			*entrada = abrirarchivoDescripción{}
			return Enoent
		}
		if (banderas & odirectorio) != 0 {
			*entrada = abrirarchivoDescripción{}
			return Enotdir
		}
		entrada.tipo = descriptorTipofat
		entrada.tamaño = tamaño
		entrada.nombrelen = nombrelen
		entrada.nombre = nombre
	}

	descriptor_2 := allocateDescriptor(proceso, descripción, 3)
	if descriptor_2 < 0 {
		*entrada = abrirarchivoDescripción{}
		return descriptor_2
	}
	return descriptor_2
}

func syscerrar(descriptor_2 int32) int32 {
	return cerrarprocesoDescriptor(ensureActualproceso(), descriptor_2)
}

func sysdup(descriptor_2 int32, mínimo int32) int32 {
	proceso := ensureActualproceso()
	entrada := getabrirarchivofor(proceso, descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	nuevoDescriptor := allocateDescriptor(proceso, proceso.fds[descriptor_2].descripción, mínimo)
	if nuevoDescriptor >= 0 {
		entrada.refs++
	}
	return nuevoDescriptor
}

func sysdup2(oldDescriptor int32, nuevoDescriptor int32) int32 {
	proceso := ensureActualproceso()
	entrada := getabrirarchivofor(proceso, oldDescriptor)
	if entrada == nil {
		return Ebadf
	}
	if nuevoDescriptor < 0 || nuevoDescriptor >= máxDescriptor {
		return Ebadf
	}
	if oldDescriptor == nuevoDescriptor {
		return nuevoDescriptor
	}
	if proceso.fds[nuevoDescriptor].enuso {
		cerrarprocesoDescriptor(proceso, nuevoDescriptor)
	}
	proceso.fds[nuevoDescriptor] = descriptorentrada{enuso: true, descripción: proceso.fds[oldDescriptor].descripción}
	entrada.refs++
	return nuevoDescriptor
}

func sysfcntl(descriptor_2 int32, orden uint32, argument uint32) int32 {
	proceso := ensureActualproceso()
	entrada := getabrirarchivofor(proceso, descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	switch orden {
	case fdupDescriptor:
		return sysdup(descriptor_2, int32(argument))
	case fgetDescriptor:
		return int32(proceso.fds[descriptor_2].descriptorBanderas)
	case festablecerDescriptor:
		proceso.fds[descriptor_2].descriptorBanderas = argument & descriptorcloexec
		return 0
	case fgetfl:
		return int32(entrada.banderas)
	case festablecerfl:
		entrada.banderas = (entrada.banderas & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(descriptor_2 int32, desplazamiento int32, whence uint32) int32 {
	entrada := getabrirarchivo(descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	if entrada.tipo != descriptorTipofat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekestablecer:
		base = 0
	case seekActual:
		base = int64(entrada.posición)
	case seekFin:
		base = int64(entrada.tamaño)
	default:
		return Einval
	}
	posición_2 := base + int64(desplazamiento)
	if posición_2 < 0 || posición_2 > 0x7FFFFFFF {
		return Einval
	}
	entrada.posición = uint32(posición_2)
	return int32(entrada.posición)
}

func leervfsarchivo(entrada *abrirarchivoDescripción, destino_2 []byte, recuento uint32) int32 {
	memoriagestor := &mem.TMemoriagestor{}
	tmpPuntero := memoriagestor.Asignar_memoria(entrada.tamaño)
	if tmpPuntero == nil {
		return Einval
	}
	tmp := GetbytesdesdePuntero(uintptr(tmpPuntero), int(entrada.tamaño), int(entrada.tamaño))
	leerarchivo(entrada.nombre[:entrada.nombrelen], tmp)
	copy(destino_2[:recuento], tmp[entrada.posición:entrada.posición+recuento])
	entrada.posición += recuento
	memoriagestor.Libre(tmpPuntero)
	return int32(recuento)
}

func isRaízRUTA(rUTADirección uint32) bool {
	if rUTADirección == 0 {
		return false
	}
	rUTA := GetbytesdesdePuntero(uintptr(rUTADirección), 4, 4)
	if rUTA[0] == '/' && rUTA[1] == 0 {
		return true
	}
	if rUTA[0] == '.' && rUTA[1] == 0 {
		return true
	}
	if rUTA[0] == '/' && rUTA[1] == '.' && rUTA[2] == 0 {
		return true
	}
	return false
}

func sysacceso(rUTADirección uint32, modo uint32) int32 {
	if rUTADirección == 0 {
		return Efault
	}
	if (modo & ^uint32(7)) != 0 {
		return Einval
	}
	isRaíz := isRaízRUTA(rUTADirección)
	exists := isRaíz
	if !exists {
		nombrelen, nombre := copiarRUTA(rUTADirección)
		exists = nombrelen != 0 && archivoTamaño(nombre[:nombrelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (modo & 2) != 0 {
		return Eacces
	}

	if (modo&1) != 0 && !isRaíz {
		return Eacces
	}
	return 0
}

func syschdir(rUTADirección uint32) int32 {
	if rUTADirección == 0 {
		return Efault
	}
	if !isRaízRUTA(rUTADirección) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferDirección uint32, tamaño uint32) int32 {
	if bufferDirección == 0 {
		return Efault
	}
	if tamaño < 2 {
		return Erange
	}
	buffer_2 := GetbytesdesdePuntero(uintptr(bufferDirección), int(tamaño), int(tamaño))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statDirección uint32, modo uint32, tamaño uint32, nodoi uint32) int32 {
	if statDirección == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statDirección)))
	*stat = posixstat{}
	stat.Dispositivo = 1
	stat.Ino = nodoi
	stat.Modo = modo
	stat.Nlink = 1
	stat.Tamaño_2 = int32(tamaño)
	stat.Blksize = 512
	stat.Bloque = int32((tamaño + 511) / 512)
	return 0
}

func sysstat(rUTADirección uint32, statDirección uint32) int32 {
	if rUTADirección == 0 {
		return Efault
	}
	if isRaízRUTA(rUTADirección) {
		return fillposixstat(statDirección, sifdir|0555, 0, 1)
	}
	nombrelen, nombre := copiarRUTA(rUTADirección)
	if nombrelen == 0 {
		return Enoent
	}
	tamaño := archivoTamaño(nombre[:nombrelen])
	if tamaño == 0 {
		return Enoent
	}
	nodoi := uint32(2)
	for i := uint32(0); i < nombrelen; i++ {
		nodoi = nodoi*33 + uint32(nombre[i])
	}
	return fillposixstat(statDirección, sifreg|0444, tamaño, nodoi)
}

func sysfstat(descriptor_2 int32, statDirección uint32) int32 {
	entrada := getabrirarchivo(descriptor_2)
	if entrada == nil {
		return Ebadf
	}
	switch entrada.tipo {
	case descriptorTipostdin, descriptorTipoconsola:
		return fillposixstat(statDirección, sifchr|0666, 0, uint32(descriptor_2+1))
	case descriptorTipoRaízdirectorio:
		return fillposixstat(statDirección, sifdir|0555, 0, 1)
	case descriptorTipofat:
		return fillposixstat(statDirección, sifreg|0444, entrada.tamaño, uint32(descriptor_2+2))
	case descriptorTipoconectorRed:
		return fillposixstat(statDirección, sifsock|0666, 0, uint32(descriptor_2+2))
	}
	return Ebadf
}

func sysfsync(descriptor_2 int32) int32 {
	if getabrirarchivo(descriptor_2) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(dirección_2 uint32) uint32 {
	proceso := ensureActualproceso()
	if proceso == nil {
		return 0
	}
	if proceso.programabreak == 0 {
		proceso.programabreak = usuarioheapbase
	}
	if dirección_2 == 0 {
		return proceso.programabreak
	}
	if dirección_2 < usuarioheapbase || dirección_2 > usuarioheapLimitar {
		return proceso.programabreak
	}
	proceso.programabreak = dirección_2
	return proceso.programabreak
}

func copiarutscampo(destino *[65]byte, valor string) {
	limitar := len(valor)
	if limitar > 64 {
		limitar = 64
	}
	for i := 0; i < limitar; i++ {
		destino[i] = valor[i]
	}
	destino[limitar] = 0
}

func sysuname(dirección_2 uint32) int32 {
	if dirección_2 == 0 {
		return Efault
	}
	nombre := (*posixutsname)(Pointer(uintptr(dirección_2)))
	*nombre = posixutsname{}
	copiarutscampo(&nombre.Sysname, "EngOS")
	copiarutscampo(&nombre.Nodename, "engos")
	copiarutscampo(&nombre.Release, "0.1-posix")
	copiarutscampo(&nombre.Versión, "POSIX.1-2017 phase 1")
	copiarutscampo(&nombre.Machine, "i386")
	return 0
}

func intercambiounsignedinteger16(valor uint16) uint16 {
	return (valor << 8) | (valor >> 8)
}

func conectorRedllamadaargument(argumentos_2 uint32, índice uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumentos_2 + índice*4)))
}

func conectorRedforDescriptor(descriptor_2 int32) (*localdatagramconectorRed, int32) {
	entrada := getabrirarchivo(descriptor_2)
	if entrada == nil || entrada.tipo != descriptorTipoconectorRed || entrada.aux >= máxsockets {
		return nil, Ebadf
	}
	conectorRed := &localsockets[entrada.aux]
	if !conectorRed.enuso {
		return nil, Ebadf
	}
	return conectorRed, 0
}

func allocateconectorRed(dominio uint32, conectorRedtipo uint32, protocol uint32) int32 {
	if dominio != afinet {
		return Eafnosupport
	}
	if conectorRedtipo != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proceso := ensureActualproceso()
	if proceso == nil {
		return Enfile
	}
	conectorRedÍndice := -1
	for i := 0; i < máxsockets; i++ {
		if !localsockets[i].enuso {
			conectorRedÍndice = i
			break
		}
	}
	if conectorRedÍndice < 0 {
		return Enfile
	}
	descripción := allocateabrirarchivo()
	if descripción < 0 {
		return descripción
	}
	localsockets[conectorRedÍndice] = localdatagramconectorRed{enuso: true}
	entrada := &abrirarchivoTabla[descripción]
	entrada.tipo = descriptorTipoconectorRed
	entrada.banderas = oleerescribir
	entrada.aux = uint32(conectorRedÍndice)
	descriptor_2 := allocateDescriptor(proceso, descripción, 3)
	if descriptor_2 < 0 {
		localsockets[conectorRedÍndice] = localdatagramconectorRed{}
		*entrada = abrirarchivoDescripción{}
		return descriptor_2
	}
	return descriptor_2
}

func conectorRedDirección(dirección_2 uint32, duración uint32) (*conectorRedDireccióniVp4, int32) {
	if dirección_2 == 0 {
		return nil, Efault
	}
	if duración < 16 {
		return nil, Einval
	}
	rESULTADO := (*conectorRedDireccióniVp4)(Pointer(uintptr(dirección_2)))
	if rESULTADO.Family != afinet {
		return nil, Eafnosupport
	}
	return rESULTADO, 0
}

func puertoEntradaUsar(puerto uint16, except *localdatagramconectorRed) bool {
	for i := 0; i < máxsockets; i++ {
		conectorRed := &localsockets[i]
		if conectorRed != except && conectorRed.enuso && conectorRed.bound && conectorRed.local.Puerto == puerto {
			return true
		}
	}
	return false
}

func vínculaephemeral(conectorRed *localdatagramconectorRed) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		puerto := intercambiounsignedinteger16(siguienteephemeralpuerto)
		siguienteephemeralpuerto++
		if siguienteephemeralpuerto < 49152 {
			siguienteephemeralpuerto = 49152
		}
		if !puertoEntradaUsar(puerto, conectorRed) {
			conectorRed.local = conectorRedDireccióniVp4{Family: afinet, Puerto: puerto, Dirección: 0x0100007F}
			conectorRed.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func conectorRedVíncula(descriptor_2 int32, dirección_2 uint32, duración uint32) int32 {
	conectorRed, err := conectorRedforDescriptor(descriptor_2)
	if err != 0 {
		return err
	}
	requested, err := conectorRedDirección(dirección_2, duración)
	if err != 0 {
		return err
	}
	if conectorRed.bound {
		return Einval
	}
	if requested.Puerto == 0 {
		return vínculaephemeral(conectorRed)
	}
	if puertoEntradaUsar(requested.Puerto, conectorRed) {
		return Eaddrinuse
	}
	conectorRed.local = *requested
	conectorRed.bound = true
	return 0
}

func conectorRedConectar(descriptor_2 int32, dirección_2 uint32, duración uint32) int32 {
	conectorRed, err := conectorRedforDescriptor(descriptor_2)
	if err != 0 {
		return err
	}
	remoto, err := conectorRedDirección(dirección_2, duración)
	if err != 0 {
		return err
	}
	if !conectorRed.bound {
		if err := vínculaephemeral(conectorRed); err != 0 {
			return err
		}
	}
	conectorRed.remoto = *remoto
	conectorRed.connected = true
	return 0
}

func conectorRedEnviarto(descriptor_2 int32, bufferDirección_2 uint32, duración uint32, destinoDirección uint32, destinoDuración uint32) int32 {
	conectorRed, err := conectorRedforDescriptor(descriptor_2)
	if err != 0 {
		return err
	}
	if duración > máxdatagramTamaño {
		return Emsgsize
	}
	if duración != 0 && bufferDirección_2 == 0 {
		return Efault
	}
	var destino conectorRedDireccióniVp4
	if destinoDirección != 0 {
		dirección_2, direcciónerror := conectorRedDirección(destinoDirección, destinoDuración)
		if direcciónerror != 0 {
			return direcciónerror
		}
		destino = *dirección_2
	} else {
		if !conectorRed.connected {
			return Enotconn
		}
		destino = conectorRed.remoto
	}
	if !conectorRed.bound {
		if vínculaerror := vínculaephemeral(conectorRed); vínculaerror != 0 {
			return vínculaerror
		}
	}
	var receiver *localdatagramconectorRed
	for i := 0; i < máxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.enuso && candidate.bound && candidate.local.Puerto == destino.Puerto &&
			(candidate.local.Dirección == 0 || candidate.local.Dirección == destino.Dirección) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.recuento >= máxconectorRedpaquetes {
		return Eagain
	}
	pAQUETE := &receiver.paquetes[receiver.tail]
	*pAQUETE = conectorRedPAQUETE{enuso: true, tamaño: duración, origen: conectorRed.local}
	if duración != 0 {
		origen := GetbytesdesdePuntero(uintptr(bufferDirección_2), int(duración), int(duración))
		copy(pAQUETE.datos[:duración], origen)
	}
	receiver.tail = (receiver.tail + 1) % máxconectorRedpaquetes
	receiver.recuento++
	return int32(duración)
}

func conectorRedreceivedesde(descriptor_2 int32, bufferDirección_2 uint32, duración uint32, origenDirección uint32, origenDuraciónDirección uint32) int32 {
	conectorRed, err := conectorRedforDescriptor(descriptor_2)
	if err != 0 {
		return err
	}
	if duración != 0 && bufferDirección_2 == 0 {
		return Efault
	}
	if conectorRed.recuento == 0 {
		return Eagain
	}
	pAQUETE := &conectorRed.paquetes[conectorRed.head]
	copiarDuración := pAQUETE.tamaño
	if copiarDuración > duración {
		copiarDuración = duración
	}
	if copiarDuración != 0 {
		destino := GetbytesdesdePuntero(uintptr(bufferDirección_2), int(copiarDuración), int(copiarDuración))
		copy(destino, pAQUETE.datos[:copiarDuración])
	}
	if origenDirección != 0 {
		if origenDuraciónDirección == 0 {
			return Efault
		}
		providedDuración := (*uint32)(Pointer(uintptr(origenDuraciónDirección)))
		if *providedDuración >= 16 {
			*(*conectorRedDireccióniVp4)(Pointer(uintptr(origenDirección))) = pAQUETE.origen
		}
		*providedDuración = 16
	}
	*pAQUETE = conectorRedPAQUETE{}
	conectorRed.head = (conectorRed.head + 1) % máxconectorRedpaquetes
	conectorRed.recuento--
	return int32(copiarDuración)
}

func copiarconectorRedNombre(descriptor_2 int32, dirección_2 uint32, duraciónDirección uint32, peer bool) int32 {
	conectorRed, err := conectorRedforDescriptor(descriptor_2)
	if err != 0 {
		return err
	}
	if dirección_2 == 0 || duraciónDirección == 0 {
		return Efault
	}
	duración := (*uint32)(Pointer(uintptr(duraciónDirección)))
	if *duración < 16 {
		*duración = 16
		return Einval
	}
	if peer {
		if !conectorRed.connected {
			return Enotconn
		}
		*(*conectorRedDireccióniVp4)(Pointer(uintptr(dirección_2))) = conectorRed.remoto
	} else {
		if !conectorRed.bound {
			if vínculaerror := vínculaephemeral(conectorRed); vínculaerror != 0 {
				return vínculaerror
			}
		}
		*(*conectorRedDireccióniVp4)(Pointer(uintptr(dirección_2))) = conectorRed.local
	}
	*duración = 16
	return 0
}

func sysconectorRedllamada(llamada uint32, argumentos_2 uint32) int32 {
	if argumentos_2 == 0 {
		return Efault
	}
	switch llamada {
	case 1:
		return allocateconectorRed(conectorRedllamadaargument(argumentos_2, 0), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2))
	case 2:
		return conectorRedVíncula(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2))
	case 3:
		return conectorRedConectar(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copiarconectorRedNombre(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), false)
	case 7:
		return copiarconectorRedNombre(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), true)
	case 9:
		return conectorRedEnviarto(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), 0, 0)
	case 10:
		return conectorRedreceivedesde(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), 0, 0)
	case 11:
		return conectorRedEnviarto(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), conectorRedllamadaargument(argumentos_2, 4), conectorRedllamadaargument(argumentos_2, 5))
	case 12:
		return conectorRedreceivedesde(int32(conectorRedllamadaargument(argumentos_2, 0)), conectorRedllamadaargument(argumentos_2, 1), conectorRedllamadaargument(argumentos_2, 2), conectorRedllamadaargument(argumentos_2, 4), conectorRedllamadaargument(argumentos_2, 5))
	case 13:
		if _, err := conectorRedforDescriptor(int32(conectorRedllamadaargument(argumentos_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := conectorRedforDescriptor(int32(conectorRedllamadaargument(argumentos_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func leerstdin(dirección uint32, recuento uint32) int32 {
	if dirección == 0 {
		return Einval
	}
	buffer := GetbytesdesdePuntero(uintptr(dirección), int(recuento), int(recuento))
	var n uint32
	for n < recuento {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputocteto(c byte) {
	siguiente := (stdinescribir + 1) % uint32(len(stdinbuffer))
	if siguiente == stdinleer {
		return
	}
	stdinbuffer[stdinescribir] = c
	stdinescribir = siguiente
}

func stdingetblocking() byte {
	for stdinleer == stdinescribir {
		sc := polltecladoscancode()
		if sc != 0 {
			Stdinputocteto(sc)
		}
	}
	c := stdinbuffer[stdinleer]
	stdinleer = (stdinleer + 1) % uint32(len(stdinbuffer))
	return c
}

func polltecladoscancode() byte {
	for (Puertoleerocteto(0x64) & 0x01) == 0 {
	}
	sc := Puertoleerocteto(0x60)
	return scancodetoocteto(sc)
}

func scancodetoocteto(sc uint8) byte {
	if sc >= 0x80 {
		return 0
	}
	switch sc {
	case 0x02:
		return '1'
	case 0x03:
		return '2'
	case 0x04:
		return '3'
	case 0x05:
		return '4'
	case 0x06:
		return '5'
	case 0x07:
		return '6'
	case 0x08:
		return '7'
	case 0x09:
		return '8'
	case 0x0A:
		return '9'
	case 0x0B:
		return '0'
	case 0x10:
		return 'q'
	case 0x11:
		return 'w'
	case 0x12:
		return 'e'
	case 0x13:
		return 'r'
	case 0x14:
		return 't'
	case 0x15:
		return 'y'
	case 0x16:
		return 'u'
	case 0x17:
		return 'i'
	case 0x18:
		return 'o'
	case 0x19:
		return 'p'
	case 0x1E:
		return 'a'
	case 0x1F:
		return 's'
	case 0x20:
		return 'd'
	case 0x21:
		return 'f'
	case 0x22:
		return 'g'
	case 0x23:
		return 'h'
	case 0x24:
		return 'j'
	case 0x25:
		return 'k'
	case 0x26:
		return 'l'
	case 0x2C:
		return 'z'
	case 0x2D:
		return 'x'
	case 0x2E:
		return 'c'
	case 0x2F:
		return 'v'
	case 0x30:
		return 'b'
	case 0x31:
		return 'n'
	case 0x32:
		return 'm'
	case 0x33:
		return ','
	case 0x34:
		return '.'
	case 0x35:
		return '/'
	case 0x1C:
		return '\n'
	case 0x39:
		return ' '
	}
	return 0
}

func copiarEjecutarvector(dirección_2 uint32, rESULTADO *ejecutarvector) int32 {
	*rESULTADO = ejecutarvector{}
	if dirección_2 == 0 {
		return 0
	}
	for índice := uint32(0); índice < máxEjecutarvectorentrada; índice++ {
		cadenaDirección := *(*uint32)(Pointer(uintptr(dirección_2 + índice*4)))
		if cadenaDirección == 0 {
			rESULTADO.recuento = índice
			return 0
		}
		terminated := false
		for duración := uint32(0); duración <= máxEjecutarCadenaDuración; duración++ {
			valor := *(*byte)(Pointer(uintptr(cadenaDirección + duración)))
			rESULTADO.valores[índice][duración] = valor
			if valor == 0 {
				rESULTADO.lengths[índice] = duración
				terminated = true
				break
			}
		}
		if !terminated {
			return E2big
		}
	}
	return E2big
}

func pushEjecutarunsignedinteger32(memoria_de_pila *uint32, valor uint32) {
	*memoria_de_pila -= 4
	*(*uint32)(Pointer(uintptr(*memoria_de_pila))) = valor
}

func setupEjecutarstack(cpu *TcpuEstado, argumentos_2 *ejecutarvector, environment *ejecutarvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeIntervaloPrivadowritable(getcr3(), UsuariostackSuperior-stackbytes, stackbytes) {
		return Enomem
	}
	memoria_de_pila := UsuariostackSuperior
	var argumentpointers [máxEjecutarvectorentrada]uint32
	var environmentpointers [máxEjecutarvectorentrada]uint32

	for i := int(environment.recuento) - 1; i >= 0; i-- {
		duración := environment.lengths[i] + 1
		memoria_de_pila -= duración
		destino := GetbytesdesdePuntero(uintptr(memoria_de_pila), int(duración), int(duración))
		copy(destino, environment.valores[i][:duración])
		environmentpointers[i] = memoria_de_pila
	}
	for i := int(argumentos_2.recuento) - 1; i >= 0; i-- {
		duración := argumentos_2.lengths[i] + 1
		memoria_de_pila -= duración
		destino := GetbytesdesdePuntero(uintptr(memoria_de_pila), int(duración), int(duración))
		copy(destino, argumentos_2.valores[i][:duración])
		argumentpointers[i] = memoria_de_pila
	}
	memoria_de_pila &= ^uint32(3)
	pushEjecutarunsignedinteger32(&memoria_de_pila, 0)
	for i := int(environment.recuento) - 1; i >= 0; i-- {
		pushEjecutarunsignedinteger32(&memoria_de_pila, environmentpointers[i])
	}
	pushEjecutarunsignedinteger32(&memoria_de_pila, 0)
	for i := int(argumentos_2.recuento) - 1; i >= 0; i-- {
		pushEjecutarunsignedinteger32(&memoria_de_pila, argumentpointers[i])
	}
	pushEjecutarunsignedinteger32(&memoria_de_pila, argumentos_2.recuento)
	cpu.Esp = memoria_de_pila
	cpu.Ebp = 0
	return 0
}

func cerraralEjecutar(proceso *procesoentrada) {
	if proceso == nil {
		return
	}
	for descriptor_2 := int32(0); descriptor_2 < máxDescriptor; descriptor_2++ {
		if proceso.fds[descriptor_2].enuso && (proceso.fds[descriptor_2].descriptorBanderas&descriptorcloexec) != 0 {
			cerrarprocesoDescriptor(proceso, descriptor_2)
		}
	}
}

func sysexecve(cpu *TcpuEstado, rUTADirección uint32) int32 {
	if rUTADirección == 0 {
		return Efault
	}
	var argumentos_2 ejecutarvector
	var environment ejecutarvector
	if rESULTADO := copiarEjecutarvector(cpu.Ecx, &argumentos_2); rESULTADO < 0 {
		return rESULTADO
	}
	if rESULTADO := copiarEjecutarvector(cpu.Edx, &environment); rESULTADO < 0 {
		return rESULTADO
	}
	nombrelen, nombre := copiarRUTA(rUTADirección)
	if nombrelen == 0 {
		return Enoent
	}
	tamaño := archivoTamaño(nombre[:nombrelen])
	if tamaño == 0 {
		return Enoent
	}
	memoriagestor := &mem.TMemoriagestor{}
	archivoPuntero := memoriagestor.Asignar_memoria(tamaño)
	if archivoPuntero == nil {
		return Einval
	}
	datos := GetbytesdesdePuntero(uintptr(archivoPuntero), int(tamaño), int(tamaño))
	leerarchivo(nombre[:nombrelen], datos)
	if tamaño < 52 || datos[0] != 0x7F || datos[1] != 'E' || datos[2] != 'L' || datos[3] != 'F' {
		memoriagestor.Libre(archivoPuntero)
		return Enoexec
	}
	loader := Elf{}
	entrada := loader.Getentrada(datos)
	loader.Parse(datos, getcr3())
	memoriagestor.Libre(archivoPuntero)
	if rESULTADO := setupEjecutarstack(cpu, &argumentos_2, &environment); rESULTADO < 0 {
		return rESULTADO
	}
	cerraralEjecutar(ensureActualproceso())
	cpu.Eip = entrada
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuEstado) int32 {
	padrepid := Actualpid()
	if ensureActualproceso() == nil {
		return Enfile
	}
	pid := allocateproceso(padrepid)
	if pid == 0 {
		return Einval
	}
	memoriagestor := &mem.TMemoriagestor{}
	hiloPuntero := memoriagestor.Asignar_memoria(uint32(Sizeof(THilo{})))
	stackPuntero := memoriagestor.Asignar_memoria(HilostackTamaño)
	hijopáginadirectorio := CloneDirecciónEspaciocow(getcr3())
	if hiloPuntero == nil || stackPuntero == nil || hijopáginadirectorio == 0 {
		descartarproceso(pid)
		return Einval
	}
	hijo := (*THilo)(hiloPuntero)
	hijo.Stack = uint32(uintptr(stackPuntero))
	hijo.CpuEstado = (*TcpuEstado)(Pointer(uintptr(stackPuntero) + HilostackTamaño - Sizeof(TcpuEstado{})))
	*hijo.CpuEstado = *cpu
	hijo.CpuEstado.Eax = 0
	hijo.Usuariostack_2 = cpu.Esp
	hijo.UsuariostackTamaño_2 = 0
	hijo.Pid = pid
	hijo.Padrepid = padrepid
	hijo.Páginadirectorioentrada = hijopáginadirectorio
	hijo.HiloEstado = Preparado
	hijo.FpuDesplazamiento = 0xffffffff
	hijo.Isnúcleo = false
	Añadirrunnablehilo(hijo)
	return int32(pid)
}

func sysSalir(estado uint32) {
	pid := Actualpid()
	for i := 0; i < len(procesoTabla); i++ {
		if procesoTabla[i].enuso && procesoTabla[i].pid == pid {
			cerrarTodoprocesofds(&procesoTabla[i])
			procesoTabla[i].salió = true
			procesoTabla[i].estado = (estado & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, estadoDirección uint32, opciones uint32) int32 {
	if (opciones & ^uint32(1)) != 0 {
		return Einval
	}
	padrepid := Actualpid()
	foundhijo := false
	for i := 0; i < len(procesoTabla); i++ {
		p := &procesoTabla[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.enuso && matches && p.padre == padrepid {
			foundhijo = true
			if p.salió {
				if estadoDirección != 0 {
					*(*uint32)(Pointer(uintptr(estadoDirección))) = p.estado
				}
				hijopid := p.pid
				*p = procesoentrada{}
				return int32(hijopid)
			}
		}
	}
	if !foundhijo {
		return Echild
	}

	if (opciones & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateproceso(padre uint32) uint32 {
	padreproceso := buscarproceso(padre)
	pid := Allocatepid()
	for i := 0; i < len(procesoTabla); i++ {
		if !procesoTabla[i].enuso {
			procesoTabla[i] = procesoentrada{
				enuso:		true,
				pid:		pid,
				padre:		padre,
				programabreak:	usuarioheapbase,
			}
			if padreproceso != nil {
				procesoTabla[i].programabreak = padreproceso.programabreak
				for descriptor_2 := 0; descriptor_2 < máxDescriptor; descriptor_2++ {
					if padreproceso.fds[descriptor_2].enuso {
						procesoTabla[i].fds[descriptor_2] = padreproceso.fds[descriptor_2]
						descripción := padreproceso.fds[descriptor_2].descripción
						if descripción >= 0 && descripción < máxabrirARCHIVOS {
							abrirarchivoTabla[descripción].refs++
						}
					}
				}
			} else {
				initializeprocesofds(&procesoTabla[i])
			}
			return pid
		}
	}
	return 0
}

func cerrarTodoprocesofds(proceso *procesoentrada) {
	if proceso == nil {
		return
	}
	for descriptor_2 := int32(0); descriptor_2 < máxDescriptor; descriptor_2++ {
		if proceso.fds[descriptor_2].enuso {
			cerrarprocesoDescriptor(proceso, descriptor_2)
		}
	}
}

func descartarproceso(pid uint32) {
	proceso := buscarproceso(pid)
	if proceso == nil {
		return
	}
	cerrarTodoprocesofds(proceso)
	*proceso = procesoentrada{}
}

func copiarRUTA(rUTADirección uint32) (uint32, [12]byte) {
	var nombre [12]byte
	if rUTADirección == 0 {
		return 0, nombre
	}
	raw := GetbytesdesdePuntero(uintptr(rUTADirección), 64, 64)
	var n uint32
	for i := 0; i < 64 && n < 12; i++ {
		c := raw[i]
		if c == 0 {
			break
		}
		if c == '/' {
			n = 0
			continue
		}
		if c >= 'a' && c <= 'z' {
			c = c - 32
		}
		if c == '.' {
			continue
		}
		nombre[n] = c
		n++
	}
	return n, nombre
}

func archivoTamaño(nombredearchivo []byte) uint32 {
	var ata0s = TAvanzadoTecnologíaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partición := TmsdosparticiónTabla{}
	partición.Leerpartición(&ata0s)

	bios := TParámetros_del_sistema_de_archivos32{}
	tamaño := bios.Len(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo)
	ata0s.Flush()
	return tamaño
}

func leerarchivo(nombredearchivo []byte, datos []byte) {
	var ata0s = TAvanzadoTecnologíaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partición := TmsdosparticiónTabla{}
	partición.Leerpartición(&ata0s)

	bios := TParámetros_del_sistema_de_archivos32{}
	bios.Leer(&ata0s, partición.Mbr.Primarypartición[0], nombredearchivo, datos)
	ata0s.Flush()
}

func getcr3() uint32
