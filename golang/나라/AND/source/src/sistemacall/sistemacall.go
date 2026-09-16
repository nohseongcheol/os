/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package sistemacall

import . "unsafe"

import . "interrupció"
import . "consola"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "fitxerSistema/msdospartition"
import . "fitxerSistema/fat"
import . "fitxerSistema/elf"
import mem "memòriamanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualMemòria"

var consola_2 = TConsola{}

type TSyscall struct {
	TInterrupcióhandler
}

const (
	SysSurt		uint32	= 1
	Sysfork		uint32	= 2
	SysLectura	uint32	= 3
	SysEscriptura	uint32	= 4
	SysObre		uint32	= 5
	SysTanca	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaccés	uint32	= 33
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
	SysrtSurt	uint32	= 252

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
	stdinDF		int32	= 0
	stdoutDF	int32	= 1
	stderrDF	int32	= 2
	màxDF			= 32
	màxObreFITXERS		= 128
)

type dFentrada struct {
	utilitzat	bool
	descripció	int32
	dFSenyaladors	uint32
}

type obreFitxerDescripció struct {
	utilitzat	bool
	refs		uint32
	classe		uint32
	senyaladors	uint32
	posició		uint32
	mida		uint32
	nom		[12]byte
	nomlen		uint32
	aux		uint32
}

const (
	dFClasseCap		uint32	= 0
	dFClassefat		uint32	= 1
	dFClassestdin		uint32	= 2
	dFClasseConsola		uint32	= 3
	dFClasseArrelDirectori	uint32	= 4
	dFClasseSòcol		uint32	= 5

	oLecturaonly		uint32	= 0
	oEscripturaonly		uint32	= 1
	oLecturaEscriptura	uint32	= 2
	ocreate			uint32	= 0x40
	oTrunca			uint32	= 0x200
	oappend			uint32	= 0x400
	oDirectori		uint32	= 0x10000

	seekestableix	uint32	= 0
	seekActual	uint32	= 1
	seekFinal	uint32	= 2

	fdupDF		uint32	= 0
	fgetDF		uint32	= 1
	festableixDF	uint32	= 2
	fgetfl		uint32	= 3
	festableixfl	uint32	= 4
	dFcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet		= 2
	sockdatagram	= 2
	ipprotocoludp	= 17
	màxsockets	= 32
	màxSòcolpaquets	= 8
	màxdatagramMida	= 512
)

type sòcolAdreçaipv4 struct {
	Family	uint16
	Port	uint16
	Adreça	uint32
	Zero	[8]byte
}

type sòcolPAQUET struct {
	utilitzat	bool
	mida		uint32
	origen		sòcolAdreçaipv4
	data		[màxdatagramMida]byte
}

type localdatagramSòcol struct {
	utilitzat	bool
	bound		bool
	connected	bool
	local		sòcolAdreçaipv4
	remot		sòcolAdreçaipv4
	head		uint32
	tail		uint32
	recompte	uint32
	paquets		[màxSòcolpaquets]sòcolPAQUET
}

type posixstat struct {
	Dispositiu	uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Mida_2		int32
	Blksize		int32
	Bloc		int32
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
	Versió		[65]byte
	Machine		[65]byte
}

const (
	màxExecucióvectorentrada	= 16
	màxExecucióCadenaDurada		= 63
)

type execucióvector struct {
	recompte	uint32
	lengths		[màxExecucióvectorentrada]uint32
	valors		[màxExecucióvectorentrada][màxExecucióCadenaDurada + 1]byte
}

type procésentrada struct {
	utilitzat	bool
	pid		uint32
	pare		uint32
	hasortit	bool
	estat		uint32
	programabreak	uint32
	fds		[màxDF]dFentrada
}

type cadenaheader struct {
	Data	uintptr
	Len	int
}

func syscallshaproduïtunerror(error int32) uint32 {
	return *(*uint32)(Pointer(&error))
}

var obreFitxerTaula [màxObreFITXERS]obreFitxerDescripció
var procésTaula [32]procésentrada
var localsockets [màxsockets]localdatagramSòcol
var següentephemeralport uint16 = 49152

const (
	usuariheapbase	uint32	= 0x06000000
	usuariheapLímit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLectura uint32
var stdinEscriptura uint32

func Interrupció(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysSurt_2(índex uint32) {
	Syscall(SysSurt, índex)
}

func SysLectura_2(dF uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLectura, dF, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysImprimeixstr(buffer string) {
	h := (*cadenaheader)(Pointer(&buffer))
	Syscall(SysEscriptura, uint32(stdoutDF), uint32(h.Data), uint32(h.Len))
}

func SysImprimeixunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysEscriptura, uint32(stdoutDF), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysObre_2(cAMÍ uintptr, senyaladors uint32, mode uint32) int32 {
	return int32(Syscall(SysObre, uint32(cAMÍ), senyaladors, mode))
}

func SysTanca_2(dF uint32) int32 {
	return int32(Syscall(SysTanca, dF))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(adreça uint32) uint32 {
	return Syscall(Sysbrk, adreça)
}

func Syscall(paràmetres ...uint32) uint32 {

	l := len(paràmetres)
	switch l {
	case 1:
		return Interrupció(paràmetres[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupció(paràmetres[0], paràmetres[1], 0, 0, 0, 0)
	case 3:
		return Interrupció(paràmetres[0], paràmetres[1], paràmetres[2], 0, 0, 0)
	case 4:
		return Interrupció(paràmetres[0], paràmetres[1], paràmetres[2], paràmetres[3], 0, 0)
	case 5:
		return Interrupció(paràmetres[0], paràmetres[1], paràmetres[2], paràmetres[3], paràmetres[4], 0)
	case 6:
		return Interrupció(paràmetres[0], paràmetres[1], paràmetres[2], paràmetres[3], paràmetres[4], paràmetres[5])
	default:
		return syscallshaproduïtunerror(Enosys)
	}
}

func (unmateix *TSyscall) Init(manager *TInterrupciómanager) {
	initFitxerdescriptor()

	interrupcióhandler = gestorInterrupció

	var adreça uintptr
	adreça = uintptr(Pointer(&interrupcióhandler))

	unmateix.TInterrupcióhandler.Init(0x80, uintptr(Pointer(manager)), adreça)
}

var interrupcióhandler func(uint32) uint32

func gestorInterrupció(esp uint32) uint32 {
	var cpu = (*TcpuEstat)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysSurt:
		sysSurt(cpu.Ebx)
		return uint32(uintptr(Pointer(AturaActualthread(cpu))))
	case SysrtSurt:
		sysSurt(cpu.Ebx)
		return uint32(uintptr(Pointer(AturaActualthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLectura:
		cpu.Eax = uint32(sysLectura(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysEscriptura:
		cpu.Eax = uint32(sysEscriptura(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysObre:
		cpu.Eax = uint32(sysObre(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysObre(cpu.Ebx, ocreate|oEscripturaonly|oTrunca, cpu.Ecx))
		return esp
	case SysTanca:
		cpu.Eax = uint32(sysTanca(int32(cpu.Ebx)))
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
		cpu.Eax = Actualparepid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysaccés:
		cpu.Eax = uint32(sysaccés(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysSòcolcall(cpu.Ebx, cpu.Ecx))
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
		consola_2.MUnsignedinteger32Imprimeix(cpu.Ebx)
		return esp

	default:
		consola_2.MImprimeixxy(([]byte)("sys["), 1, 23)
		consola_2.MUnsignedinteger32Imprimeix(esp)
		consola_2.MImprimeix(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimeix(cpu.Eax)
		consola_2.MImprimeix(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimeix(cpu.Ebx)
		consola_2.MImprimeix(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimeix(cpu.Ecx)
		consola_2.MImprimeix(([]byte)(":"))
		consola_2.MUnsignedinteger32Imprimeix(cpu.Edx)
		consola_2.MImprimeix(([]byte)("]"))
		cpu.Eax = syscallshaproduïtunerror(Enosys)
		return esp
	}

	return esp
}

func initFitxerdescriptor() {
	for i := 0; i < màxObreFITXERS; i++ {
		obreFitxerTaula[i] = obreFitxerDescripció{}
	}
	for i := 0; i < len(procésTaula); i++ {
		procésTaula[i] = procésentrada{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramSòcol{}
	}
	següentephemeralport = 49152
	obreFitxerTaula[0] = obreFitxerDescripció{utilitzat: true, classe: dFClassestdin, senyaladors: oLecturaonly}
	obreFitxerTaula[1] = obreFitxerDescripció{utilitzat: true, classe: dFClasseConsola, senyaladors: oEscripturaonly}
	obreFitxerTaula[2] = obreFitxerDescripció{utilitzat: true, classe: dFClasseConsola, senyaladors: oEscripturaonly}
}

func trobaProcés(pid uint32) *procésentrada {
	for i := 0; i < len(procésTaula); i++ {
		if procésTaula[i].utilitzat && procésTaula[i].pid == pid {
			return &procésTaula[i]
		}
	}
	return nil
}

func initializeProcésfds(procés *procésentrada) {
	for dF := int32(0); dF <= stderrDF; dF++ {
		procés.fds[dF] = dFentrada{utilitzat: true, descripció: dF}
		obreFitxerTaula[dF].refs++
	}
}

func ensureActualProcés() *procésentrada {
	pid := Actualpid()
	if procés := trobaProcés(pid); procés != nil {
		return procés
	}
	for i := 0; i < len(procésTaula); i++ {
		if !procésTaula[i].utilitzat {
			procésTaula[i] = procésentrada{
				utilitzat:	true,
				pid:		pid,
				pare:		Actualparepid(),
				programabreak:	usuariheapbase,
			}
			initializeProcésfds(&procésTaula[i])
			return &procésTaula[i]
		}
	}
	return nil
}

func getObreFitxerfor(procés *procésentrada, dF int32) *obreFitxerDescripció {
	if procés == nil || dF < 0 || dF >= màxDF || !procés.fds[dF].utilitzat {
		return nil
	}
	descripció := procés.fds[dF].descripció
	if descripció < 0 || descripció >= màxObreFITXERS || !obreFitxerTaula[descripció].utilitzat {
		return nil
	}
	return &obreFitxerTaula[descripció]
}

func getObreFitxer(dF int32) *obreFitxerDescripció {
	return getObreFitxerfor(ensureActualProcés(), dF)
}

func allocateObreFitxer() int32 {
	for i := int32(3); i < màxObreFITXERS; i++ {
		if !obreFitxerTaula[i].utilitzat {
			obreFitxerTaula[i] = obreFitxerDescripció{utilitzat: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateDF(procés *procésentrada, descripció int32, mínim int32) int32 {
	if procés == nil {
		return Enfile
	}
	if mínim < 0 || mínim >= màxDF {
		return Einval
	}
	for dF := mínim; dF < màxDF; dF++ {
		if !procés.fds[dF].utilitzat {
			procés.fds[dF] = dFentrada{utilitzat: true, descripció: descripció}
			return dF
		}
	}
	return Emfile
}

func releaseObreFitxer(descripció int32) {
	if descripció < 0 || descripció >= màxObreFITXERS {
		return
	}
	entrada := &obreFitxerTaula[descripció]
	if entrada.refs > 0 {
		entrada.refs--
	}

	if entrada.refs == 0 && descripció > stderrDF {
		if entrada.classe == dFClasseSòcol && entrada.aux < màxsockets {
			localsockets[entrada.aux] = localdatagramSòcol{}
		}
		*entrada = obreFitxerDescripció{}
	}
}

func tancaProcésDF(procés *procésentrada, dF int32) int32 {
	if procés == nil || getObreFitxerfor(procés, dF) == nil {
		return Ebadf
	}
	descripció := procés.fds[dF].descripció
	procés.fds[dF] = dFentrada{}
	releaseObreFitxer(descripció)
	return 0
}

func sysEscriptura(dF int32, adreça uint32, recompte uint32) int32 {
	if recompte == 0 {
		return 0
	}
	if adreça == 0 || adreça+recompte < adreça {
		return Efault
	}
	if recompte > 4096 {
		return Einval
	}
	entrada := getObreFitxer(dF)
	if entrada == nil {
		return Ebadf
	}
	if entrada.classe != dFClasseConsola {
		if entrada.classe == dFClasseSòcol {
			return sòcolEnviato(dF, adreça, recompte, 0, 0)
		}
		if entrada.classe == dFClassefat || entrada.classe == dFClasseArrelDirectori {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetbytesdesdePunter(uintptr(adreça), int(recompte), int(recompte))
	consola_2.MImprimeix(buffer)
	return int32(recompte)
}

func sysLectura(dF int32, adreça uint32, recompte uint32) int32 {
	if recompte == 0 {
		return 0
	}
	if adreça == 0 || adreça+recompte < adreça {
		return Efault
	}
	entrada := getObreFitxer(dF)
	if entrada == nil {
		return Ebadf
	}
	if entrada.classe == dFClassestdin {
		return lecturastdin(adreça, recompte)
	}
	if entrada.classe == dFClasseArrelDirectori {
		return Eisdir
	}
	if entrada.classe == dFClasseSòcol {
		return sòcolreceivedesde(dF, adreça, recompte, 0, 0)
	}
	if entrada.classe != dFClassefat {
		return Ebadf
	}
	if entrada.posició >= entrada.mida {
		return 0
	}
	remaining := entrada.mida - entrada.posició
	if recompte > remaining {
		recompte = remaining
	}
	buffer := GetbytesdesdePunter(uintptr(adreça), int(recompte), int(recompte))
	return lecturavfsFitxer(entrada, buffer, recompte)
}

func sysObre(cAMÍAdreça uint32, senyaladors uint32, mode uint32) int32 {
	_ = mode
	if cAMÍAdreça == 0 {
		return Efault
	}
	accésmode := senyaladors & 3
	if accésmode == oEscripturaonly || accésmode == oLecturaEscriptura || (senyaladors&(ocreate|oTrunca|oappend)) != 0 {
		return Erofs
	}

	procés := ensureActualProcés()
	if procés == nil {
		return Enfile
	}
	descripció := allocateObreFitxer()
	if descripció < 0 {
		return descripció
	}
	entrada := &obreFitxerTaula[descripció]
	entrada.senyaladors = senyaladors
	if isArrelCAMÍ(cAMÍAdreça) {
		entrada.classe = dFClasseArrelDirectori
		entrada.mida = 0
	} else {
		nomlen, nom := copiaCAMÍ(cAMÍAdreça)
		if nomlen == 0 {
			*entrada = obreFitxerDescripció{}
			return Enoent
		}
		mida := fitxerMida(nom[:nomlen])
		if mida == 0 {
			*entrada = obreFitxerDescripció{}
			return Enoent
		}
		if (senyaladors & oDirectori) != 0 {
			*entrada = obreFitxerDescripció{}
			return Enotdir
		}
		entrada.classe = dFClassefat
		entrada.mida = mida
		entrada.nomlen = nomlen
		entrada.nom = nom
	}

	dF := allocateDF(procés, descripció, 3)
	if dF < 0 {
		*entrada = obreFitxerDescripció{}
		return dF
	}
	return dF
}

func sysTanca(dF int32) int32 {
	return tancaProcésDF(ensureActualProcés(), dF)
}

func sysdup(dF int32, mínim int32) int32 {
	procés := ensureActualProcés()
	entrada := getObreFitxerfor(procés, dF)
	if entrada == nil {
		return Ebadf
	}
	nouDF := allocateDF(procés, procés.fds[dF].descripció, mínim)
	if nouDF >= 0 {
		entrada.refs++
	}
	return nouDF
}

func sysdup2(oldDF int32, nouDF int32) int32 {
	procés := ensureActualProcés()
	entrada := getObreFitxerfor(procés, oldDF)
	if entrada == nil {
		return Ebadf
	}
	if nouDF < 0 || nouDF >= màxDF {
		return Ebadf
	}
	if oldDF == nouDF {
		return nouDF
	}
	if procés.fds[nouDF].utilitzat {
		tancaProcésDF(procés, nouDF)
	}
	procés.fds[nouDF] = dFentrada{utilitzat: true, descripció: procés.fds[oldDF].descripció}
	entrada.refs++
	return nouDF
}

func sysfcntl(dF int32, ordre uint32, argument uint32) int32 {
	procés := ensureActualProcés()
	entrada := getObreFitxerfor(procés, dF)
	if entrada == nil {
		return Ebadf
	}
	switch ordre {
	case fdupDF:
		return sysdup(dF, int32(argument))
	case fgetDF:
		return int32(procés.fds[dF].dFSenyaladors)
	case festableixDF:
		procés.fds[dF].dFSenyaladors = argument & dFcloexec
		return 0
	case fgetfl:
		return int32(entrada.senyaladors)
	case festableixfl:
		entrada.senyaladors = (entrada.senyaladors & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(dF int32, offset int32, whence uint32) int32 {
	entrada := getObreFitxer(dF)
	if entrada == nil {
		return Ebadf
	}
	if entrada.classe != dFClassefat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekestableix:
		base = 0
	case seekActual:
		base = int64(entrada.posició)
	case seekFinal:
		base = int64(entrada.mida)
	default:
		return Einval
	}
	posició_2 := base + int64(offset)
	if posició_2 < 0 || posició_2 > 0x7FFFFFFF {
		return Einval
	}
	entrada.posició = uint32(posició_2)
	return int32(entrada.posició)
}

func lecturavfsFitxer(entrada *obreFitxerDescripció, destinació_2 []byte, recompte uint32) int32 {
	memòriamanager := &mem.TMemòriamanager{}
	tmpPunter := memòriamanager.Malloc(entrada.mida)
	if tmpPunter == nil {
		return Einval
	}
	tmp := GetbytesdesdePunter(uintptr(tmpPunter), int(entrada.mida), int(entrada.mida))
	lecturaFitxer(entrada.nom[:entrada.nomlen], tmp)
	copy(destinació_2[:recompte], tmp[entrada.posició:entrada.posició+recompte])
	entrada.posició += recompte
	memòriamanager.Lliure(tmpPunter)
	return int32(recompte)
}

func isArrelCAMÍ(cAMÍAdreça uint32) bool {
	if cAMÍAdreça == 0 {
		return false
	}
	cAMÍ := GetbytesdesdePunter(uintptr(cAMÍAdreça), 4, 4)
	if cAMÍ[0] == '/' && cAMÍ[1] == 0 {
		return true
	}
	if cAMÍ[0] == '.' && cAMÍ[1] == 0 {
		return true
	}
	if cAMÍ[0] == '/' && cAMÍ[1] == '.' && cAMÍ[2] == 0 {
		return true
	}
	return false
}

func sysaccés(cAMÍAdreça uint32, mode uint32) int32 {
	if cAMÍAdreça == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isArrel := isArrelCAMÍ(cAMÍAdreça)
	exists := isArrel
	if !exists {
		nomlen, nom := copiaCAMÍ(cAMÍAdreça)
		exists = nomlen != 0 && fitxerMida(nom[:nomlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mode & 2) != 0 {
		return Eacces
	}

	if (mode&1) != 0 && !isArrel {
		return Eacces
	}
	return 0
}

func syschdir(cAMÍAdreça uint32) int32 {
	if cAMÍAdreça == 0 {
		return Efault
	}
	if !isArrelCAMÍ(cAMÍAdreça) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferAdreça uint32, mida uint32) int32 {
	if bufferAdreça == 0 {
		return Efault
	}
	if mida < 2 {
		return Erange
	}
	buffer_2 := GetbytesdesdePunter(uintptr(bufferAdreça), int(mida), int(mida))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statAdreça uint32, mode uint32, mida uint32, inode uint32) int32 {
	if statAdreça == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statAdreça)))
	*stat = posixstat{}
	stat.Dispositiu = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Mida_2 = int32(mida)
	stat.Blksize = 512
	stat.Bloc = int32((mida + 511) / 512)
	return 0
}

func sysstat(cAMÍAdreça uint32, statAdreça uint32) int32 {
	if cAMÍAdreça == 0 {
		return Efault
	}
	if isArrelCAMÍ(cAMÍAdreça) {
		return fillposixstat(statAdreça, sifdir|0555, 0, 1)
	}
	nomlen, nom := copiaCAMÍ(cAMÍAdreça)
	if nomlen == 0 {
		return Enoent
	}
	mida := fitxerMida(nom[:nomlen])
	if mida == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < nomlen; i++ {
		inode = inode*33 + uint32(nom[i])
	}
	return fillposixstat(statAdreça, sifreg|0444, mida, inode)
}

func sysfstat(dF int32, statAdreça uint32) int32 {
	entrada := getObreFitxer(dF)
	if entrada == nil {
		return Ebadf
	}
	switch entrada.classe {
	case dFClassestdin, dFClasseConsola:
		return fillposixstat(statAdreça, sifchr|0666, 0, uint32(dF+1))
	case dFClasseArrelDirectori:
		return fillposixstat(statAdreça, sifdir|0555, 0, 1)
	case dFClassefat:
		return fillposixstat(statAdreça, sifreg|0444, entrada.mida, uint32(dF+2))
	case dFClasseSòcol:
		return fillposixstat(statAdreça, sifsock|0666, 0, uint32(dF+2))
	}
	return Ebadf
}

func sysfsync(dF int32) int32 {
	if getObreFitxer(dF) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(adreça_2 uint32) uint32 {
	procés := ensureActualProcés()
	if procés == nil {
		return 0
	}
	if procés.programabreak == 0 {
		procés.programabreak = usuariheapbase
	}
	if adreça_2 == 0 {
		return procés.programabreak
	}
	if adreça_2 < usuariheapbase || adreça_2 > usuariheapLímit {
		return procés.programabreak
	}
	procés.programabreak = adreça_2
	return procés.programabreak
}

func copiautscamp(destinació *[65]byte, valor string) {
	límit := len(valor)
	if límit > 64 {
		límit = 64
	}
	for i := 0; i < límit; i++ {
		destinació[i] = valor[i]
	}
	destinació[límit] = 0
}

func sysuname(adreça_2 uint32) int32 {
	if adreça_2 == 0 {
		return Efault
	}
	nom := (*posixutsname)(Pointer(uintptr(adreça_2)))
	*nom = posixutsname{}
	copiautscamp(&nom.Sysname, "EngOS")
	copiautscamp(&nom.Nodename, "engos")
	copiautscamp(&nom.Release, "0.1-posix")
	copiautscamp(&nom.Versió, "POSIX.1-2017 phase 1")
	copiautscamp(&nom.Machine, "i386")
	return 0
}

func espaidintercanviunsignedinteger16(valor uint16) uint16 {
	return (valor << 8) | (valor >> 8)
}

func sòcolcallargument(arguments_2 uint32, índex uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + índex*4)))
}

func sòcolforDF(dF int32) (*localdatagramSòcol, int32) {
	entrada := getObreFitxer(dF)
	if entrada == nil || entrada.classe != dFClasseSòcol || entrada.aux >= màxsockets {
		return nil, Ebadf
	}
	sòcol := &localsockets[entrada.aux]
	if !sòcol.utilitzat {
		return nil, Ebadf
	}
	return sòcol, 0
}

func allocateSòcol(domini uint32, sòcolTipus uint32, protocol uint32) int32 {
	if domini != afinet {
		return Eafnosupport
	}
	if sòcolTipus != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	procés := ensureActualProcés()
	if procés == nil {
		return Enfile
	}
	sòcolÍndex := -1
	for i := 0; i < màxsockets; i++ {
		if !localsockets[i].utilitzat {
			sòcolÍndex = i
			break
		}
	}
	if sòcolÍndex < 0 {
		return Enfile
	}
	descripció := allocateObreFitxer()
	if descripció < 0 {
		return descripció
	}
	localsockets[sòcolÍndex] = localdatagramSòcol{utilitzat: true}
	entrada := &obreFitxerTaula[descripció]
	entrada.classe = dFClasseSòcol
	entrada.senyaladors = oLecturaEscriptura
	entrada.aux = uint32(sòcolÍndex)
	dF := allocateDF(procés, descripció, 3)
	if dF < 0 {
		localsockets[sòcolÍndex] = localdatagramSòcol{}
		*entrada = obreFitxerDescripció{}
		return dF
	}
	return dF
}

func sòcolAdreça(adreça_2 uint32, durada uint32) (*sòcolAdreçaipv4, int32) {
	if adreça_2 == 0 {
		return nil, Efault
	}
	if durada < 16 {
		return nil, Einval
	}
	rESULTAT := (*sòcolAdreçaipv4)(Pointer(uintptr(adreça_2)))
	if rESULTAT.Family != afinet {
		return nil, Eafnosupport
	}
	return rESULTAT, 0
}

func portaUsa(port uint16, except *localdatagramSòcol) bool {
	for i := 0; i < màxsockets; i++ {
		sòcol := &localsockets[i]
		if sòcol != except && sòcol.utilitzat && sòcol.bound && sòcol.local.Port == port {
			return true
		}
	}
	return false
}

func vinculaephemeral(sòcol *localdatagramSòcol) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := espaidintercanviunsignedinteger16(següentephemeralport)
		següentephemeralport++
		if següentephemeralport < 49152 {
			següentephemeralport = 49152
		}
		if !portaUsa(port, sòcol) {
			sòcol.local = sòcolAdreçaipv4{Family: afinet, Port: port, Adreça: 0x0100007F}
			sòcol.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func sòcolVincula(dF int32, adreça_2 uint32, durada uint32) int32 {
	sòcol, error := sòcolforDF(dF)
	if error != 0 {
		return error
	}
	requested, error := sòcolAdreça(adreça_2, durada)
	if error != 0 {
		return error
	}
	if sòcol.bound {
		return Einval
	}
	if requested.Port == 0 {
		return vinculaephemeral(sòcol)
	}
	if portaUsa(requested.Port, sòcol) {
		return Eaddrinuse
	}
	sòcol.local = *requested
	sòcol.bound = true
	return 0
}

func sòcolConnecta(dF int32, adreça_2 uint32, durada uint32) int32 {
	sòcol, error := sòcolforDF(dF)
	if error != 0 {
		return error
	}
	remot, error := sòcolAdreça(adreça_2, durada)
	if error != 0 {
		return error
	}
	if !sòcol.bound {
		if error := vinculaephemeral(sòcol); error != 0 {
			return error
		}
	}
	sòcol.remot = *remot
	sòcol.connected = true
	return 0
}

func sòcolEnviato(dF int32, bufferAdreça_2 uint32, durada uint32, destinacióAdreça uint32, destinacióDurada uint32) int32 {
	sòcol, error := sòcolforDF(dF)
	if error != 0 {
		return error
	}
	if durada > màxdatagramMida {
		return Emsgsize
	}
	if durada != 0 && bufferAdreça_2 == 0 {
		return Efault
	}
	var destinació sòcolAdreçaipv4
	if destinacióAdreça != 0 {
		adreça_2, adreçashaproduïtunerror := sòcolAdreça(destinacióAdreça, destinacióDurada)
		if adreçashaproduïtunerror != 0 {
			return adreçashaproduïtunerror
		}
		destinació = *adreça_2
	} else {
		if !sòcol.connected {
			return Enotconn
		}
		destinació = sòcol.remot
	}
	if !sòcol.bound {
		if vinculashaproduïtunerror := vinculaephemeral(sòcol); vinculashaproduïtunerror != 0 {
			return vinculashaproduïtunerror
		}
	}
	var receiver *localdatagramSòcol
	for i := 0; i < màxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.utilitzat && candidate.bound && candidate.local.Port == destinació.Port &&
			(candidate.local.Adreça == 0 || candidate.local.Adreça == destinació.Adreça) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.recompte >= màxSòcolpaquets {
		return Eagain
	}
	pAQUET := &receiver.paquets[receiver.tail]
	*pAQUET = sòcolPAQUET{utilitzat: true, mida: durada, origen: sòcol.local}
	if durada != 0 {
		origen := GetbytesdesdePunter(uintptr(bufferAdreça_2), int(durada), int(durada))
		copy(pAQUET.data[:durada], origen)
	}
	receiver.tail = (receiver.tail + 1) % màxSòcolpaquets
	receiver.recompte++
	return int32(durada)
}

func sòcolreceivedesde(dF int32, bufferAdreça_2 uint32, durada uint32, origenAdreça uint32, origenDuradaAdreça uint32) int32 {
	sòcol, error := sòcolforDF(dF)
	if error != 0 {
		return error
	}
	if durada != 0 && bufferAdreça_2 == 0 {
		return Efault
	}
	if sòcol.recompte == 0 {
		return Eagain
	}
	pAQUET := &sòcol.paquets[sòcol.head]
	copiaDurada := pAQUET.mida
	if copiaDurada > durada {
		copiaDurada = durada
	}
	if copiaDurada != 0 {
		destinació := GetbytesdesdePunter(uintptr(bufferAdreça_2), int(copiaDurada), int(copiaDurada))
		copy(destinació, pAQUET.data[:copiaDurada])
	}
	if origenAdreça != 0 {
		if origenDuradaAdreça == 0 {
			return Efault
		}
		providedDurada := (*uint32)(Pointer(uintptr(origenDuradaAdreça)))
		if *providedDurada >= 16 {
			*(*sòcolAdreçaipv4)(Pointer(uintptr(origenAdreça))) = pAQUET.origen
		}
		*providedDurada = 16
	}
	*pAQUET = sòcolPAQUET{}
	sòcol.head = (sòcol.head + 1) % màxSòcolpaquets
	sòcol.recompte--
	return int32(copiaDurada)
}

func copiaSòcolNom(dF int32, adreça_2 uint32, duradaAdreça uint32, peer bool) int32 {
	sòcol, error := sòcolforDF(dF)
	if error != 0 {
		return error
	}
	if adreça_2 == 0 || duradaAdreça == 0 {
		return Efault
	}
	durada := (*uint32)(Pointer(uintptr(duradaAdreça)))
	if *durada < 16 {
		*durada = 16
		return Einval
	}
	if peer {
		if !sòcol.connected {
			return Enotconn
		}
		*(*sòcolAdreçaipv4)(Pointer(uintptr(adreça_2))) = sòcol.remot
	} else {
		if !sòcol.bound {
			if vinculashaproduïtunerror := vinculaephemeral(sòcol); vinculashaproduïtunerror != 0 {
				return vinculashaproduïtunerror
			}
		}
		*(*sòcolAdreçaipv4)(Pointer(uintptr(adreça_2))) = sòcol.local
	}
	*durada = 16
	return 0
}

func sysSòcolcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSòcol(sòcolcallargument(arguments_2, 0), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2))
	case 2:
		return sòcolVincula(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2))
	case 3:
		return sòcolConnecta(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copiaSòcolNom(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), false)
	case 7:
		return copiaSòcolNom(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), true)
	case 9:
		return sòcolEnviato(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), 0, 0)
	case 10:
		return sòcolreceivedesde(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), 0, 0)
	case 11:
		return sòcolEnviato(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), sòcolcallargument(arguments_2, 4), sòcolcallargument(arguments_2, 5))
	case 12:
		return sòcolreceivedesde(int32(sòcolcallargument(arguments_2, 0)), sòcolcallargument(arguments_2, 1), sòcolcallargument(arguments_2, 2), sòcolcallargument(arguments_2, 4), sòcolcallargument(arguments_2, 5))
	case 13:
		if _, error := sòcolforDF(int32(sòcolcallargument(arguments_2, 0))); error != 0 {
			return error
		}
		return 0
	case 14:
		if _, error := sòcolforDF(int32(sòcolcallargument(arguments_2, 0))); error != 0 {
			return error
		}
		return 0
	}
	return Eopnotsupp
}

func lecturastdin(adreça uint32, recompte uint32) int32 {
	if adreça == 0 {
		return Einval
	}
	buffer := GetbytesdesdePunter(uintptr(adreça), int(recompte), int(recompte))
	var n uint32
	for n < recompte {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputbyte(c byte) {
	següent := (stdinEscriptura + 1) % uint32(len(stdinbuffer))
	if següent == stdinLectura {
		return
	}
	stdinbuffer[stdinEscriptura] = c
	stdinEscriptura = següent
}

func stdingetblocking() byte {
	for stdinLectura == stdinEscriptura {
		sc := pollTeclatscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLectura]
	stdinLectura = (stdinLectura + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTeclatscancode() byte {
	for (PortLecturabyte(0x64) & 0x01) == 0 {
	}
	sc := PortLecturabyte(0x60)
	return scancodetobyte(sc)
}

func scancodetobyte(sc uint8) byte {
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

func copiaExecucióvector(adreça_2 uint32, rESULTAT *execucióvector) int32 {
	*rESULTAT = execucióvector{}
	if adreça_2 == 0 {
		return 0
	}
	for índex := uint32(0); índex < màxExecucióvectorentrada; índex++ {
		cadenaAdreça := *(*uint32)(Pointer(uintptr(adreça_2 + índex*4)))
		if cadenaAdreça == 0 {
			rESULTAT.recompte = índex
			return 0
		}
		terminated := false
		for durada := uint32(0); durada <= màxExecucióCadenaDurada; durada++ {
			valor := *(*byte)(Pointer(uintptr(cadenaAdreça + durada)))
			rESULTAT.valors[índex][durada] = valor
			if valor == 0 {
				rESULTAT.lengths[índex] = durada
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

func pushExecucióunsignedinteger32(stack *uint32, valor uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = valor
}

func setupExecucióstack(cpu *TcpuEstat, arguments_2 *execucióvector, environment *execucióvector) int32 {
	const stackbytes uint32 = 4096
	if !MakeIntervalPrivatwritable(getcr3(), UsuaristackAdalt-stackbytes, stackbytes) {
		return Enomem
	}
	stack := UsuaristackAdalt
	var argumentpointers [màxExecucióvectorentrada]uint32
	var environmentpointers [màxExecucióvectorentrada]uint32

	for i := int(environment.recompte) - 1; i >= 0; i-- {
		durada := environment.lengths[i] + 1
		stack -= durada
		destinació := GetbytesdesdePunter(uintptr(stack), int(durada), int(durada))
		copy(destinació, environment.valors[i][:durada])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.recompte) - 1; i >= 0; i-- {
		durada := arguments_2.lengths[i] + 1
		stack -= durada
		destinació := GetbytesdesdePunter(uintptr(stack), int(durada), int(durada))
		copy(destinació, arguments_2.valors[i][:durada])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushExecucióunsignedinteger32(&stack, 0)
	for i := int(environment.recompte) - 1; i >= 0; i-- {
		pushExecucióunsignedinteger32(&stack, environmentpointers[i])
	}
	pushExecucióunsignedinteger32(&stack, 0)
	for i := int(arguments_2.recompte) - 1; i >= 0; i-- {
		pushExecucióunsignedinteger32(&stack, argumentpointers[i])
	}
	pushExecucióunsignedinteger32(&stack, arguments_2.recompte)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func tancaEngegatExecució(procés *procésentrada) {
	if procés == nil {
		return
	}
	for dF := int32(0); dF < màxDF; dF++ {
		if procés.fds[dF].utilitzat && (procés.fds[dF].dFSenyaladors&dFcloexec) != 0 {
			tancaProcésDF(procés, dF)
		}
	}
}

func sysexecve(cpu *TcpuEstat, cAMÍAdreça uint32) int32 {
	if cAMÍAdreça == 0 {
		return Efault
	}
	var arguments_2 execucióvector
	var environment execucióvector
	if rESULTAT := copiaExecucióvector(cpu.Ecx, &arguments_2); rESULTAT < 0 {
		return rESULTAT
	}
	if rESULTAT := copiaExecucióvector(cpu.Edx, &environment); rESULTAT < 0 {
		return rESULTAT
	}
	nomlen, nom := copiaCAMÍ(cAMÍAdreça)
	if nomlen == 0 {
		return Enoent
	}
	mida := fitxerMida(nom[:nomlen])
	if mida == 0 {
		return Enoent
	}
	memòriamanager := &mem.TMemòriamanager{}
	fitxerPunter := memòriamanager.Malloc(mida)
	if fitxerPunter == nil {
		return Einval
	}
	data := GetbytesdesdePunter(uintptr(fitxerPunter), int(mida), int(mida))
	lecturaFitxer(nom[:nomlen], data)
	if mida < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memòriamanager.Lliure(fitxerPunter)
		return Enoexec
	}
	loader := Elf{}
	entrada := loader.Getentrada(data)
	loader.Parse(data, getcr3())
	memòriamanager.Lliure(fitxerPunter)
	if rESULTAT := setupExecucióstack(cpu, &arguments_2, &environment); rESULTAT < 0 {
		return rESULTAT
	}
	tancaEngegatExecució(ensureActualProcés())
	cpu.Eip = entrada
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuEstat) int32 {
	parepid := Actualpid()
	if ensureActualProcés() == nil {
		return Enfile
	}
	pid := allocateProcés(parepid)
	if pid == 0 {
		return Einval
	}
	memòriamanager := &mem.TMemòriamanager{}
	threadPunter := memòriamanager.Malloc(uint32(Sizeof(TThread{})))
	stackPunter := memòriamanager.Malloc(ThreadstackMida)
	fillPàginaDirectori := CloneAdreçaEspaicow(getcr3())
	if threadPunter == nil || stackPunter == nil || fillPàginaDirectori == 0 {
		descartaProcés(pid)
		return Einval
	}
	fill := (*TThread)(threadPunter)
	fill.Stack = uint32(uintptr(stackPunter))
	fill.CpuEstat = (*TcpuEstat)(Pointer(uintptr(stackPunter) + ThreadstackMida - Sizeof(TcpuEstat{})))
	*fill.CpuEstat = *cpu
	fill.CpuEstat.Eax = 0
	fill.Usuaristack_2 = cpu.Esp
	fill.UsuaristackMida_2 = 0
	fill.Pid = pid
	fill.Parepid = parepid
	fill.PàginaDirectorientrada = fillPàginaDirectori
	fill.ThreadEstat = Preparat
	fill.Fpuoffset = 0xffffffff
	fill.Iskernel = false
	Afegeixrunnablethread(fill)
	return int32(pid)
}

func sysSurt(estat uint32) {
	pid := Actualpid()
	for i := 0; i < len(procésTaula); i++ {
		if procésTaula[i].utilitzat && procésTaula[i].pid == pid {
			tancaTotProcésfds(&procésTaula[i])
			procésTaula[i].hasortit = true
			procésTaula[i].estat = (estat & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, estatAdreça uint32, opcions uint32) int32 {
	if (opcions & ^uint32(1)) != 0 {
		return Einval
	}
	parepid := Actualpid()
	foundfill := false
	for i := 0; i < len(procésTaula); i++ {
		p := &procésTaula[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.utilitzat && matches && p.pare == parepid {
			foundfill = true
			if p.hasortit {
				if estatAdreça != 0 {
					*(*uint32)(Pointer(uintptr(estatAdreça))) = p.estat
				}
				fillpid := p.pid
				*p = procésentrada{}
				return int32(fillpid)
			}
		}
	}
	if !foundfill {
		return Echild
	}

	if (opcions & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProcés(pare uint32) uint32 {
	pareProcés := trobaProcés(pare)
	pid := Allocatepid()
	for i := 0; i < len(procésTaula); i++ {
		if !procésTaula[i].utilitzat {
			procésTaula[i] = procésentrada{
				utilitzat:	true,
				pid:		pid,
				pare:		pare,
				programabreak:	usuariheapbase,
			}
			if pareProcés != nil {
				procésTaula[i].programabreak = pareProcés.programabreak
				for dF := 0; dF < màxDF; dF++ {
					if pareProcés.fds[dF].utilitzat {
						procésTaula[i].fds[dF] = pareProcés.fds[dF]
						descripció := pareProcés.fds[dF].descripció
						if descripció >= 0 && descripció < màxObreFITXERS {
							obreFitxerTaula[descripció].refs++
						}
					}
				}
			} else {
				initializeProcésfds(&procésTaula[i])
			}
			return pid
		}
	}
	return 0
}

func tancaTotProcésfds(procés *procésentrada) {
	if procés == nil {
		return
	}
	for dF := int32(0); dF < màxDF; dF++ {
		if procés.fds[dF].utilitzat {
			tancaProcésDF(procés, dF)
		}
	}
}

func descartaProcés(pid uint32) {
	procés := trobaProcés(pid)
	if procés == nil {
		return
	}
	tancaTotProcésfds(procés)
	*procés = procésentrada{}
}

func copiaCAMÍ(cAMÍAdreça uint32) (uint32, [12]byte) {
	var nom [12]byte
	if cAMÍAdreça == 0 {
		return 0, nom
	}
	raw := GetbytesdesdePunter(uintptr(cAMÍAdreça), 64, 64)
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
		nom[n] = c
		n++
	}
	return n, nom
}

func fitxerMida(nomdelfitxer []byte) uint32 {
	var ata0s = TAvançatTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaula{}
	partition.Lecturapartition(&ata0s)

	bios := TBiosparameterBloc32{}
	mida := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer)
	ata0s.Flush()
	return mida
}

func lecturaFitxer(nomdelfitxer []byte, data []byte) {
	var ata0s = TAvançatTecnologiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTaula{}
	partition.Lecturapartition(&ata0s)

	bios := TBiosparameterBloc32{}
	bios.Lectura(&ata0s, partition.Mbr.Primarypartition[0], nomdelfitxer, data)
	ata0s.Flush()
}

func getcr3() uint32
