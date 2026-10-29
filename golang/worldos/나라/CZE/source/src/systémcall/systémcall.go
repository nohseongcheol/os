/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systémcall

import . "unsafe"

import . "přerušení"
import . "konzole"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "souborSystém/msdospartition"
import . "souborSystém/fat"
import . "souborSystém/spustitelný_a_spojitelný_formát"
import mem "paměťmanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuálníPaměť"

var konzole_2 = TKonzole{}

type TSyscall struct {
	TPřerušeníhandler
}

const (
	SysKonec	uint32	= 1
	Sysfork		uint32	= 2
	SysČtení	uint32	= 3
	SysZápis	uint32	= 4
	SysOtevřít	uint32	= 5
	SysZavřít	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syspřístup	uint32	= 33
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
	SysrtKonec	uint32	= 252

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
	stdinfd			int32	= 0
	stdoutfd		int32	= 1
	stderrfd		int32	= 2
	maxfd				= 32
	maxOtevřítSOUBORY		= 128
)

type fdZáznam struct {
	použito		bool
	popis		int32
	fdPříznaky	uint32
}

type otevřítSouborPopis struct {
	použito		bool
	refs		uint32
	typ		uint32
	příznaky	uint32
	umístění	uint32
	velikost	uint32
	název		[12]byte
	názevlen	uint32
	aux		uint32
}

const (
	fdTypŽádné		uint32	= 0
	fdTypfat		uint32	= 1
	fdTypstdin		uint32	= 2
	fdTypKonzole		uint32	= 3
	fdTypKořenadresář	uint32	= 4
	fdTypsocket		uint32	= 5

	oČteníonly		uint32	= 0
	oZápisonly		uint32	= 1
	oČteníZápis		uint32	= 2
	ocreate			uint32	= 0x40
	oOříznouthodnotu	uint32	= 0x200
	oappend			uint32	= 0x400
	oadresář		uint32	= 0x10000

	seekNastavit	uint32	= 0
	seekSoučasný	uint32	= 1
	seekKonec	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fNastavitfd	uint32	= 2
	fgetfl		uint32	= 3
	fNastavitfl	uint32	= 4
	fdcloexec	uint32	= 1

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
	maxsockets		= 32
	maxsocketpaketů		= 8
	maxdatagramVelikost	= 512
)

type socketAdresaipv4 struct {
	Family	uint16
	Port	uint16
	Adresa	uint32
	Nula	[8]byte
}

type socketPAKET struct {
	použito		bool
	velikost	uint32
	zdroj		socketAdresaipv4
	data		[maxdatagramVelikost]byte
}

type místnídatagramsocket struct {
	použito		bool
	bound		bool
	connected	bool
	místní		socketAdresaipv4
	vzdálený	socketAdresaipv4
	head		uint32
	tail		uint32
	počet		uint32
	paketů		[maxsocketpaketů]socketPAKET
}

type posixstat struct {
	Zařízení	uint32
	Ino		uint32
	MÓD		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Velikost_2	int32
	Blksize		int32
	Blokový		int32
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
	Verze		[65]byte
	Machine		[65]byte
}

const (
	maxVykonánívectorZáznam	= 16
	maxVykonánířetězecDélka	= 63
)

type vykonánívector struct {
	počet	uint32
	lengths	[maxVykonánívectorZáznam]uint32
	hodnoty	[maxVykonánívectorZáznam][maxVykonánířetězecDélka + 1]byte
}

type procesZáznam struct {
	použito		bool
	pid		uint32
	rodič		uint32
	skončil		bool
	stav		uint32
	programbreak	uint32
	fds		[maxfd]fdZáznam
}

type řetězecheader struct {
	Data	uintptr
	Len	int
}

func syscallChyba(chyba int32) uint32 {
	return *(*uint32)(Pointer(&chyba))
}

var otevřítSouborTabulka [maxOtevřítSOUBORY]otevřítSouborPopis
var procesTabulka [32]procesZáznam
var místnísockets [maxsockets]místnídatagramsocket
var následujícíephemeralport uint16 = 49152

const (
	uživatelheapbase	uint32	= 0x06000000
	uživatelheapOmezení	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinČtení uint32
var stdinZápis uint32

func Přerušení(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysKonec_2(rejstřík uint32) {
	Syscall(SysKonec, rejstřík)
}

func SysČtení_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysČtení, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysTisknoutstr(buffer string) {
	h := (*řetězecheader)(Pointer(&buffer))
	Syscall(SysZápis, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysTisknoutunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysZápis, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOtevřít_2(cESTA uintptr, příznaky uint32, mÓD uint32) int32 {
	return int32(Syscall(SysOtevřít, uint32(cESTA), příznaky, mÓD))
}

func SysZavřít_2(fd uint32) int32 {
	return int32(Syscall(SysZavřít, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(adresa uint32) uint32 {
	return Syscall(Sysbrk, adresa)
}

func Syscall(parametry ...uint32) uint32 {

	l := len(parametry)
	switch l {
	case 1:
		return Přerušení(parametry[0], 0, 0, 0, 0, 0)
	case 2:
		return Přerušení(parametry[0], parametry[1], 0, 0, 0, 0)
	case 3:
		return Přerušení(parametry[0], parametry[1], parametry[2], 0, 0, 0)
	case 4:
		return Přerušení(parametry[0], parametry[1], parametry[2], parametry[3], 0, 0)
	case 5:
		return Přerušení(parametry[0], parametry[1], parametry[2], parametry[3], parametry[4], 0)
	case 6:
		return Přerušení(parametry[0], parametry[1], parametry[2], parametry[3], parametry[4], parametry[5])
	default:
		return syscallChyba(Enosys)
	}
}

func (self *TSyscall) Init(manager *TPřerušenímanager) {
	initSoubordescriptor()

	přerušeníhandler = úchytkaPřerušení

	var adresa uintptr
	adresa = uintptr(Pointer(&přerušeníhandler))

	self.TPřerušeníhandler.Init(0x80, uintptr(Pointer(manager)), adresa)
}

var přerušeníhandler func(uint32) uint32

func úchytkaPřerušení(esp uint32) uint32 {
	var cpu = (*TcpuStav)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysKonec:
		sysKonec(cpu.Ebx)
		return uint32(uintptr(Pointer(ZastavitSoučasnýthread(cpu))))
	case SysrtKonec:
		sysKonec(cpu.Ebx)
		return uint32(uintptr(Pointer(ZastavitSoučasnýthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysČtení:
		cpu.Eax = uint32(sysČtení(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysZápis:
		cpu.Eax = uint32(sysZápis(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysOtevřít:
		cpu.Eax = uint32(sysOtevřít(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysOtevřít(cpu.Ebx, ocreate|oZápisonly|oOříznouthodnotu, cpu.Ecx))
		return esp
	case SysZavřít:
		cpu.Eax = uint32(sysZavřít(int32(cpu.Ebx)))
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
		cpu.Eax = Současnýpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Současnýrodičpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Syspřístup:
		cpu.Eax = uint32(syspřístup(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(syssocketcall(cpu.Ebx, cpu.Ecx))
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
		konzole_2.MUnsignedinteger32Tisknout(cpu.Ebx)
		return esp

	default:
		konzole_2.MTisknoutxy(([]byte)("sys["), 1, 23)
		konzole_2.MUnsignedinteger32Tisknout(esp)
		konzole_2.MTisknout(([]byte)(":"))
		konzole_2.MUnsignedinteger32Tisknout(cpu.Eax)
		konzole_2.MTisknout(([]byte)(":"))
		konzole_2.MUnsignedinteger32Tisknout(cpu.Ebx)
		konzole_2.MTisknout(([]byte)(":"))
		konzole_2.MUnsignedinteger32Tisknout(cpu.Ecx)
		konzole_2.MTisknout(([]byte)(":"))
		konzole_2.MUnsignedinteger32Tisknout(cpu.Edx)
		konzole_2.MTisknout(([]byte)("]"))
		cpu.Eax = syscallChyba(Enosys)
		return esp
	}

	return esp
}

func initSoubordescriptor() {
	for i := 0; i < maxOtevřítSOUBORY; i++ {
		otevřítSouborTabulka[i] = otevřítSouborPopis{}
	}
	for i := 0; i < len(procesTabulka); i++ {
		procesTabulka[i] = procesZáznam{}
	}
	for i := 0; i < len(místnísockets); i++ {
		místnísockets[i] = místnídatagramsocket{}
	}
	následujícíephemeralport = 49152
	otevřítSouborTabulka[0] = otevřítSouborPopis{použito: true, typ: fdTypstdin, příznaky: oČteníonly}
	otevřítSouborTabulka[1] = otevřítSouborPopis{použito: true, typ: fdTypKonzole, příznaky: oZápisonly}
	otevřítSouborTabulka[2] = otevřítSouborPopis{použito: true, typ: fdTypKonzole, příznaky: oZápisonly}
}

func hledatProces(pid uint32) *procesZáznam {
	for i := 0; i < len(procesTabulka); i++ {
		if procesTabulka[i].použito && procesTabulka[i].pid == pid {
			return &procesTabulka[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesZáznam) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proces.fds[fd] = fdZáznam{použito: true, popis: fd}
		otevřítSouborTabulka[fd].refs++
	}
}

func ensureSoučasnýProces() *procesZáznam {
	pid := Současnýpid()
	if proces := hledatProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabulka); i++ {
		if !procesTabulka[i].použito {
			procesTabulka[i] = procesZáznam{
				použito:	true,
				pid:		pid,
				rodič:		Současnýrodičpid(),
				programbreak:	uživatelheapbase,
			}
			initializeProcesfds(&procesTabulka[i])
			return &procesTabulka[i]
		}
	}
	return nil
}

func getOtevřítSouborfor(proces *procesZáznam, fd int32) *otevřítSouborPopis {
	if proces == nil || fd < 0 || fd >= maxfd || !proces.fds[fd].použito {
		return nil
	}
	popis := proces.fds[fd].popis
	if popis < 0 || popis >= maxOtevřítSOUBORY || !otevřítSouborTabulka[popis].použito {
		return nil
	}
	return &otevřítSouborTabulka[popis]
}

func getOtevřítSoubor(fd int32) *otevřítSouborPopis {
	return getOtevřítSouborfor(ensureSoučasnýProces(), fd)
}

func allocateOtevřítSoubor() int32 {
	for i := int32(3); i < maxOtevřítSOUBORY; i++ {
		if !otevřítSouborTabulka[i].použito {
			otevřítSouborTabulka[i] = otevřítSouborPopis{použito: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proces *procesZáznam, popis int32, minimum int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !proces.fds[fd].použito {
			proces.fds[fd] = fdZáznam{použito: true, popis: popis}
			return fd
		}
	}
	return Emfile
}

func releaseOtevřítSoubor(popis int32) {
	if popis < 0 || popis >= maxOtevřítSOUBORY {
		return
	}
	záznam := &otevřítSouborTabulka[popis]
	if záznam.refs > 0 {
		záznam.refs--
	}

	if záznam.refs == 0 && popis > stderrfd {
		if záznam.typ == fdTypsocket && záznam.aux < maxsockets {
			místnísockets[záznam.aux] = místnídatagramsocket{}
		}
		*záznam = otevřítSouborPopis{}
	}
}

func zavřítProcesfd(proces *procesZáznam, fd int32) int32 {
	if proces == nil || getOtevřítSouborfor(proces, fd) == nil {
		return Ebadf
	}
	popis := proces.fds[fd].popis
	proces.fds[fd] = fdZáznam{}
	releaseOtevřítSoubor(popis)
	return 0
}

func sysZápis(fd int32, adresa uint32, počet uint32) int32 {
	if počet == 0 {
		return 0
	}
	if adresa == 0 || adresa+počet < adresa {
		return Efault
	}
	if počet > 4096 {
		return Einval
	}
	záznam := getOtevřítSoubor(fd)
	if záznam == nil {
		return Ebadf
	}
	if záznam.typ != fdTypKonzole {
		if záznam.typ == fdTypsocket {
			return socketPoslatdo(fd, adresa, počet, 0, 0)
		}
		if záznam.typ == fdTypfat || záznam.typ == fdTypKořenadresář {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytůzKurzor(uintptr(adresa), int(počet), int(počet))
	konzole_2.MTisknout(buffer)
	return int32(počet)
}

func sysČtení(fd int32, adresa uint32, počet uint32) int32 {
	if počet == 0 {
		return 0
	}
	if adresa == 0 || adresa+počet < adresa {
		return Efault
	}
	záznam := getOtevřítSoubor(fd)
	if záznam == nil {
		return Ebadf
	}
	if záznam.typ == fdTypstdin {
		return čtenístdin(adresa, počet)
	}
	if záznam.typ == fdTypKořenadresář {
		return Eisdir
	}
	if záznam.typ == fdTypsocket {
		return socketreceivez(fd, adresa, počet, 0, 0)
	}
	if záznam.typ != fdTypfat {
		return Ebadf
	}
	if záznam.umístění >= záznam.velikost {
		return 0
	}
	remaining := záznam.velikost - záznam.umístění
	if počet > remaining {
		počet = remaining
	}
	buffer := GetBytůzKurzor(uintptr(adresa), int(počet), int(počet))
	return čtenívfsSoubor(záznam, buffer, počet)
}

func sysOtevřít(cESTAAdresa uint32, příznaky uint32, mÓD uint32) int32 {
	_ = mÓD
	if cESTAAdresa == 0 {
		return Efault
	}
	přístupMÓD := příznaky & 3
	if přístupMÓD == oZápisonly || přístupMÓD == oČteníZápis || (příznaky&(ocreate|oOříznouthodnotu|oappend)) != 0 {
		return Erofs
	}

	proces := ensureSoučasnýProces()
	if proces == nil {
		return Enfile
	}
	popis := allocateOtevřítSoubor()
	if popis < 0 {
		return popis
	}
	záznam := &otevřítSouborTabulka[popis]
	záznam.příznaky = příznaky
	if isKořenCESTA(cESTAAdresa) {
		záznam.typ = fdTypKořenadresář
		záznam.velikost = 0
	} else {
		názevlen, název := kopírovatCESTA(cESTAAdresa)
		if názevlen == 0 {
			*záznam = otevřítSouborPopis{}
			return Enoent
		}
		velikost := souborVelikost(název[:názevlen])
		if velikost == 0 {
			*záznam = otevřítSouborPopis{}
			return Enoent
		}
		if (příznaky & oadresář) != 0 {
			*záznam = otevřítSouborPopis{}
			return Enotdir
		}
		záznam.typ = fdTypfat
		záznam.velikost = velikost
		záznam.názevlen = názevlen
		záznam.název = název
	}

	fd := allocatefd(proces, popis, 3)
	if fd < 0 {
		*záznam = otevřítSouborPopis{}
		return fd
	}
	return fd
}

func sysZavřít(fd int32) int32 {
	return zavřítProcesfd(ensureSoučasnýProces(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	proces := ensureSoučasnýProces()
	záznam := getOtevřítSouborfor(proces, fd)
	if záznam == nil {
		return Ebadf
	}
	novýfd := allocatefd(proces, proces.fds[fd].popis, minimum)
	if novýfd >= 0 {
		záznam.refs++
	}
	return novýfd
}

func sysdup2(oldfd int32, novýfd int32) int32 {
	proces := ensureSoučasnýProces()
	záznam := getOtevřítSouborfor(proces, oldfd)
	if záznam == nil {
		return Ebadf
	}
	if novýfd < 0 || novýfd >= maxfd {
		return Ebadf
	}
	if oldfd == novýfd {
		return novýfd
	}
	if proces.fds[novýfd].použito {
		zavřítProcesfd(proces, novýfd)
	}
	proces.fds[novýfd] = fdZáznam{použito: true, popis: proces.fds[oldfd].popis}
	záznam.refs++
	return novýfd
}

func sysfcntl(fd int32, příkaz uint32, argument uint32) int32 {
	proces := ensureSoučasnýProces()
	záznam := getOtevřítSouborfor(proces, fd)
	if záznam == nil {
		return Ebadf
	}
	switch příkaz {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proces.fds[fd].fdPříznaky)
	case fNastavitfd:
		proces.fds[fd].fdPříznaky = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(záznam.příznaky)
	case fNastavitfl:
		záznam.příznaky = (záznam.příznaky & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	záznam := getOtevřítSoubor(fd)
	if záznam == nil {
		return Ebadf
	}
	if záznam.typ != fdTypfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekNastavit:
		base = 0
	case seekSoučasný:
		base = int64(záznam.umístění)
	case seekKonec:
		base = int64(záznam.velikost)
	default:
		return Einval
	}
	umístění_2 := base + int64(offset)
	if umístění_2 < 0 || umístění_2 > 0x7FFFFFFF {
		return Einval
	}
	záznam.umístění = uint32(umístění_2)
	return int32(záznam.umístění)
}

func čtenívfsSoubor(záznam *otevřítSouborPopis, cíl_2 []byte, počet uint32) int32 {
	paměťmanager := &mem.TPaměťmanager{}
	tmpKurzor := paměťmanager.Přidělit_paměť(záznam.velikost)
	if tmpKurzor == nil {
		return Einval
	}
	tmp := GetBytůzKurzor(uintptr(tmpKurzor), int(záznam.velikost), int(záznam.velikost))
	čteníSoubor(záznam.název[:záznam.názevlen], tmp)
	copy(cíl_2[:počet], tmp[záznam.umístění:záznam.umístění+počet])
	záznam.umístění += počet
	paměťmanager.Volné(tmpKurzor)
	return int32(počet)
}

func isKořenCESTA(cESTAAdresa uint32) bool {
	if cESTAAdresa == 0 {
		return false
	}
	cESTA := GetBytůzKurzor(uintptr(cESTAAdresa), 4, 4)
	if cESTA[0] == '/' && cESTA[1] == 0 {
		return true
	}
	if cESTA[0] == '.' && cESTA[1] == 0 {
		return true
	}
	if cESTA[0] == '/' && cESTA[1] == '.' && cESTA[2] == 0 {
		return true
	}
	return false
}

func syspřístup(cESTAAdresa uint32, mÓD uint32) int32 {
	if cESTAAdresa == 0 {
		return Efault
	}
	if (mÓD & ^uint32(7)) != 0 {
		return Einval
	}
	isKořen := isKořenCESTA(cESTAAdresa)
	exists := isKořen
	if !exists {
		názevlen, název := kopírovatCESTA(cESTAAdresa)
		exists = názevlen != 0 && souborVelikost(název[:názevlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mÓD & 2) != 0 {
		return Eacces
	}

	if (mÓD&1) != 0 && !isKořen {
		return Eacces
	}
	return 0
}

func syschdir(cESTAAdresa uint32) int32 {
	if cESTAAdresa == 0 {
		return Efault
	}
	if !isKořenCESTA(cESTAAdresa) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferAdresa uint32, velikost uint32) int32 {
	if bufferAdresa == 0 {
		return Efault
	}
	if velikost < 2 {
		return Erange
	}
	buffer_2 := GetBytůzKurzor(uintptr(bufferAdresa), int(velikost), int(velikost))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statAdresa uint32, mÓD uint32, velikost uint32, iuzel uint32) int32 {
	if statAdresa == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statAdresa)))
	*stat = posixstat{}
	stat.Zařízení = 1
	stat.Ino = iuzel
	stat.MÓD = mÓD
	stat.Nlink = 1
	stat.Velikost_2 = int32(velikost)
	stat.Blksize = 512
	stat.Blokový = int32((velikost + 511) / 512)
	return 0
}

func sysstat(cESTAAdresa uint32, statAdresa uint32) int32 {
	if cESTAAdresa == 0 {
		return Efault
	}
	if isKořenCESTA(cESTAAdresa) {
		return fillposixstat(statAdresa, sifdir|0555, 0, 1)
	}
	názevlen, název := kopírovatCESTA(cESTAAdresa)
	if názevlen == 0 {
		return Enoent
	}
	velikost := souborVelikost(název[:názevlen])
	if velikost == 0 {
		return Enoent
	}
	iuzel := uint32(2)
	for i := uint32(0); i < názevlen; i++ {
		iuzel = iuzel*33 + uint32(název[i])
	}
	return fillposixstat(statAdresa, sifreg|0444, velikost, iuzel)
}

func sysfstat(fd int32, statAdresa uint32) int32 {
	záznam := getOtevřítSoubor(fd)
	if záznam == nil {
		return Ebadf
	}
	switch záznam.typ {
	case fdTypstdin, fdTypKonzole:
		return fillposixstat(statAdresa, sifchr|0666, 0, uint32(fd+1))
	case fdTypKořenadresář:
		return fillposixstat(statAdresa, sifdir|0555, 0, 1)
	case fdTypfat:
		return fillposixstat(statAdresa, sifreg|0444, záznam.velikost, uint32(fd+2))
	case fdTypsocket:
		return fillposixstat(statAdresa, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOtevřítSoubor(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(adresa_2 uint32) uint32 {
	proces := ensureSoučasnýProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = uživatelheapbase
	}
	if adresa_2 == 0 {
		return proces.programbreak
	}
	if adresa_2 < uživatelheapbase || adresa_2 > uživatelheapOmezení {
		return proces.programbreak
	}
	proces.programbreak = adresa_2
	return proces.programbreak
}

func kopírovatutsfield(cíl *[65]byte, hodnota string) {
	omezení := len(hodnota)
	if omezení > 64 {
		omezení = 64
	}
	for i := 0; i < omezení; i++ {
		cíl[i] = hodnota[i]
	}
	cíl[omezení] = 0
}

func sysuname(adresa_2 uint32) int32 {
	if adresa_2 == 0 {
		return Efault
	}
	název := (*posixutsname)(Pointer(uintptr(adresa_2)))
	*název = posixutsname{}
	kopírovatutsfield(&název.Sysname, "EngOS")
	kopírovatutsfield(&název.Nodename, "engos")
	kopírovatutsfield(&název.Release, "0.1-posix")
	kopírovatutsfield(&název.Verze, "POSIX.1-2017 phase 1")
	kopírovatutsfield(&název.Machine, "i386")
	return 0
}

func odkládacíprostorunsignedinteger16(hodnota uint16) uint16 {
	return (hodnota << 8) | (hodnota >> 8)
}

func socketcallargument(argumenty_2 uint32, rejstřík uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenty_2 + rejstřík*4)))
}

func socketforfd(fd int32) (*místnídatagramsocket, int32) {
	záznam := getOtevřítSoubor(fd)
	if záznam == nil || záznam.typ != fdTypsocket || záznam.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &místnísockets[záznam.aux]
	if !socket.použito {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(doména uint32, socketTyp uint32, protocol uint32) int32 {
	if doména != afinet {
		return Eafnosupport
	}
	if socketTyp != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureSoučasnýProces()
	if proces == nil {
		return Enfile
	}
	socketRejstřík := -1
	for i := 0; i < maxsockets; i++ {
		if !místnísockets[i].použito {
			socketRejstřík = i
			break
		}
	}
	if socketRejstřík < 0 {
		return Enfile
	}
	popis := allocateOtevřítSoubor()
	if popis < 0 {
		return popis
	}
	místnísockets[socketRejstřík] = místnídatagramsocket{použito: true}
	záznam := &otevřítSouborTabulka[popis]
	záznam.typ = fdTypsocket
	záznam.příznaky = oČteníZápis
	záznam.aux = uint32(socketRejstřík)
	fd := allocatefd(proces, popis, 3)
	if fd < 0 {
		místnísockets[socketRejstřík] = místnídatagramsocket{}
		*záznam = otevřítSouborPopis{}
		return fd
	}
	return fd
}

func socketAdresa(adresa_2 uint32, délka uint32) (*socketAdresaipv4, int32) {
	if adresa_2 == 0 {
		return nil, Efault
	}
	if délka < 16 {
		return nil, Einval
	}
	vÝSLEDEK := (*socketAdresaipv4)(Pointer(uintptr(adresa_2)))
	if vÝSLEDEK.Family != afinet {
		return nil, Eafnosupport
	}
	return vÝSLEDEK, 0
}

func portVstupPoužít(port uint16, except *místnídatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &místnísockets[i]
		if socket != except && socket.použito && socket.bound && socket.místní.Port == port {
			return true
		}
	}
	return false
}

func svázatephemeral(socket *místnídatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := odkládacíprostorunsignedinteger16(následujícíephemeralport)
		následujícíephemeralport++
		if následujícíephemeralport < 49152 {
			následujícíephemeralport = 49152
		}
		if !portVstupPoužít(port, socket) {
			socket.místní = socketAdresaipv4{Family: afinet, Port: port, Adresa: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketSvázat(fd int32, adresa_2 uint32, délka uint32) int32 {
	socket, chyba := socketforfd(fd)
	if chyba != 0 {
		return chyba
	}
	requested, chyba := socketAdresa(adresa_2, délka)
	if chyba != 0 {
		return chyba
	}
	if socket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return svázatephemeral(socket)
	}
	if portVstupPoužít(requested.Port, socket) {
		return Eaddrinuse
	}
	socket.místní = *requested
	socket.bound = true
	return 0
}

func socketSpojení(fd int32, adresa_2 uint32, délka uint32) int32 {
	socket, chyba := socketforfd(fd)
	if chyba != 0 {
		return chyba
	}
	vzdálený, chyba := socketAdresa(adresa_2, délka)
	if chyba != 0 {
		return chyba
	}
	if !socket.bound {
		if chyba := svázatephemeral(socket); chyba != 0 {
			return chyba
		}
	}
	socket.vzdálený = *vzdálený
	socket.connected = true
	return 0
}

func socketPoslatdo(fd int32, bufferAdresa_2 uint32, délka uint32, cílAdresa uint32, cílDélka uint32) int32 {
	socket, chyba := socketforfd(fd)
	if chyba != 0 {
		return chyba
	}
	if délka > maxdatagramVelikost {
		return Emsgsize
	}
	if délka != 0 && bufferAdresa_2 == 0 {
		return Efault
	}
	var cíl socketAdresaipv4
	if cílAdresa != 0 {
		adresa_2, adresaChyba := socketAdresa(cílAdresa, cílDélka)
		if adresaChyba != 0 {
			return adresaChyba
		}
		cíl = *adresa_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		cíl = socket.vzdálený
	}
	if !socket.bound {
		if svázatChyba := svázatephemeral(socket); svázatChyba != 0 {
			return svázatChyba
		}
	}
	var receiver *místnídatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &místnísockets[i]
		if candidate.použito && candidate.bound && candidate.místní.Port == cíl.Port &&
			(candidate.místní.Adresa == 0 || candidate.místní.Adresa == cíl.Adresa) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.počet >= maxsocketpaketů {
		return Eagain
	}
	pAKET := &receiver.paketů[receiver.tail]
	*pAKET = socketPAKET{použito: true, velikost: délka, zdroj: socket.místní}
	if délka != 0 {
		zdroj := GetBytůzKurzor(uintptr(bufferAdresa_2), int(délka), int(délka))
		copy(pAKET.data[:délka], zdroj)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpaketů
	receiver.počet++
	return int32(délka)
}

func socketreceivez(fd int32, bufferAdresa_2 uint32, délka uint32, zdrojAdresa uint32, zdrojDélkaAdresa uint32) int32 {
	socket, chyba := socketforfd(fd)
	if chyba != 0 {
		return chyba
	}
	if délka != 0 && bufferAdresa_2 == 0 {
		return Efault
	}
	if socket.počet == 0 {
		return Eagain
	}
	pAKET := &socket.paketů[socket.head]
	kopírovatDélka := pAKET.velikost
	if kopírovatDélka > délka {
		kopírovatDélka = délka
	}
	if kopírovatDélka != 0 {
		cíl := GetBytůzKurzor(uintptr(bufferAdresa_2), int(kopírovatDélka), int(kopírovatDélka))
		copy(cíl, pAKET.data[:kopírovatDélka])
	}
	if zdrojAdresa != 0 {
		if zdrojDélkaAdresa == 0 {
			return Efault
		}
		providedDélka := (*uint32)(Pointer(uintptr(zdrojDélkaAdresa)))
		if *providedDélka >= 16 {
			*(*socketAdresaipv4)(Pointer(uintptr(zdrojAdresa))) = pAKET.zdroj
		}
		*providedDélka = 16
	}
	*pAKET = socketPAKET{}
	socket.head = (socket.head + 1) % maxsocketpaketů
	socket.počet--
	return int32(kopírovatDélka)
}

func kopírovatsocketNázev(fd int32, adresa_2 uint32, délkaAdresa uint32, peer bool) int32 {
	socket, chyba := socketforfd(fd)
	if chyba != 0 {
		return chyba
	}
	if adresa_2 == 0 || délkaAdresa == 0 {
		return Efault
	}
	délka := (*uint32)(Pointer(uintptr(délkaAdresa)))
	if *délka < 16 {
		*délka = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketAdresaipv4)(Pointer(uintptr(adresa_2))) = socket.vzdálený
	} else {
		if !socket.bound {
			if svázatChyba := svázatephemeral(socket); svázatChyba != 0 {
				return svázatChyba
			}
		}
		*(*socketAdresaipv4)(Pointer(uintptr(adresa_2))) = socket.místní
	}
	*délka = 16
	return 0
}

func syssocketcall(call uint32, argumenty_2 uint32) int32 {
	if argumenty_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(argumenty_2, 0), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2))
	case 2:
		return socketSvázat(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2))
	case 3:
		return socketSpojení(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopírovatsocketNázev(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), false)
	case 7:
		return kopírovatsocketNázev(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), true)
	case 9:
		return socketPoslatdo(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), 0, 0)
	case 10:
		return socketreceivez(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), 0, 0)
	case 11:
		return socketPoslatdo(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), socketcallargument(argumenty_2, 4), socketcallargument(argumenty_2, 5))
	case 12:
		return socketreceivez(int32(socketcallargument(argumenty_2, 0)), socketcallargument(argumenty_2, 1), socketcallargument(argumenty_2, 2), socketcallargument(argumenty_2, 4), socketcallargument(argumenty_2, 5))
	case 13:
		if _, chyba := socketforfd(int32(socketcallargument(argumenty_2, 0))); chyba != 0 {
			return chyba
		}
		return 0
	case 14:
		if _, chyba := socketforfd(int32(socketcallargument(argumenty_2, 0))); chyba != 0 {
			return chyba
		}
		return 0
	}
	return Eopnotsupp
}

func čtenístdin(adresa uint32, počet uint32) int32 {
	if adresa == 0 {
		return Einval
	}
	buffer := GetBytůzKurzor(uintptr(adresa), int(počet), int(počet))
	var n uint32
	for n < počet {
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
	následující := (stdinZápis + 1) % uint32(len(stdinbuffer))
	if následující == stdinČtení {
		return
	}
	stdinbuffer[stdinZápis] = c
	stdinZápis = následující
}

func stdingetblocking() byte {
	for stdinČtení == stdinZápis {
		sc := pollKlávesnicescancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinČtení]
	stdinČtení = (stdinČtení + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlávesnicescancode() byte {
	for (PortČteníbyte(0x64) & 0x01) == 0 {
	}
	sc := PortČteníbyte(0x60)
	return scancodedobyte(sc)
}

func scancodedobyte(sc uint8) byte {
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

func kopírovatVykonánívector(adresa_2 uint32, vÝSLEDEK *vykonánívector) int32 {
	*vÝSLEDEK = vykonánívector{}
	if adresa_2 == 0 {
		return 0
	}
	for rejstřík := uint32(0); rejstřík < maxVykonánívectorZáznam; rejstřík++ {
		řetězecAdresa := *(*uint32)(Pointer(uintptr(adresa_2 + rejstřík*4)))
		if řetězecAdresa == 0 {
			vÝSLEDEK.počet = rejstřík
			return 0
		}
		terminated := false
		for délka := uint32(0); délka <= maxVykonánířetězecDélka; délka++ {
			hodnota := *(*byte)(Pointer(uintptr(řetězecAdresa + délka)))
			vÝSLEDEK.hodnoty[rejstřík][délka] = hodnota
			if hodnota == 0 {
				vÝSLEDEK.lengths[rejstřík] = délka
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

func pushVykonáníunsignedinteger32(paměť_zásobníku *uint32, hodnota uint32) {
	*paměť_zásobníku -= 4
	*(*uint32)(Pointer(uintptr(*paměť_zásobníku))) = hodnota
}

func setupVykonánístack(cpu *TcpuStav, argumenty_2 *vykonánívector, environment *vykonánívector) int32 {
	const stackBytů uint32 = 4096
	if !MakeRozsahPrivátníwritable(getcr3(), UživatelstackNahoře-stackBytů, stackBytů) {
		return Enomem
	}
	paměť_zásobníku := UživatelstackNahoře
	var argumentpointers [maxVykonánívectorZáznam]uint32
	var environmentpointers [maxVykonánívectorZáznam]uint32

	for i := int(environment.počet) - 1; i >= 0; i-- {
		délka := environment.lengths[i] + 1
		paměť_zásobníku -= délka
		cíl := GetBytůzKurzor(uintptr(paměť_zásobníku), int(délka), int(délka))
		copy(cíl, environment.hodnoty[i][:délka])
		environmentpointers[i] = paměť_zásobníku
	}
	for i := int(argumenty_2.počet) - 1; i >= 0; i-- {
		délka := argumenty_2.lengths[i] + 1
		paměť_zásobníku -= délka
		cíl := GetBytůzKurzor(uintptr(paměť_zásobníku), int(délka), int(délka))
		copy(cíl, argumenty_2.hodnoty[i][:délka])
		argumentpointers[i] = paměť_zásobníku
	}
	paměť_zásobníku &= ^uint32(3)
	pushVykonáníunsignedinteger32(&paměť_zásobníku, 0)
	for i := int(environment.počet) - 1; i >= 0; i-- {
		pushVykonáníunsignedinteger32(&paměť_zásobníku, environmentpointers[i])
	}
	pushVykonáníunsignedinteger32(&paměť_zásobníku, 0)
	for i := int(argumenty_2.počet) - 1; i >= 0; i-- {
		pushVykonáníunsignedinteger32(&paměť_zásobníku, argumentpointers[i])
	}
	pushVykonáníunsignedinteger32(&paměť_zásobníku, argumenty_2.počet)
	cpu.Esp = paměť_zásobníku
	cpu.Ebp = 0
	return 0
}

func zavřítZapnutoVykonání(proces *procesZáznam) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].použito && (proces.fds[fd].fdPříznaky&fdcloexec) != 0 {
			zavřítProcesfd(proces, fd)
		}
	}
}

func sysexecve(cpu *TcpuStav, cESTAAdresa uint32) int32 {
	if cESTAAdresa == 0 {
		return Efault
	}
	var argumenty_2 vykonánívector
	var environment vykonánívector
	if vÝSLEDEK := kopírovatVykonánívector(cpu.Ecx, &argumenty_2); vÝSLEDEK < 0 {
		return vÝSLEDEK
	}
	if vÝSLEDEK := kopírovatVykonánívector(cpu.Edx, &environment); vÝSLEDEK < 0 {
		return vÝSLEDEK
	}
	názevlen, název := kopírovatCESTA(cESTAAdresa)
	if názevlen == 0 {
		return Enoent
	}
	velikost := souborVelikost(název[:názevlen])
	if velikost == 0 {
		return Enoent
	}
	paměťmanager := &mem.TPaměťmanager{}
	souborKurzor := paměťmanager.Přidělit_paměť(velikost)
	if souborKurzor == nil {
		return Einval
	}
	data := GetBytůzKurzor(uintptr(souborKurzor), int(velikost), int(velikost))
	čteníSoubor(název[:názevlen], data)
	if velikost < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		paměťmanager.Volné(souborKurzor)
		return Enoexec
	}
	loader := Elf{}
	záznam := loader.GetZáznam(data)
	loader.Parse(data, getcr3())
	paměťmanager.Volné(souborKurzor)
	if vÝSLEDEK := setupVykonánístack(cpu, &argumenty_2, &environment); vÝSLEDEK < 0 {
		return vÝSLEDEK
	}
	zavřítZapnutoVykonání(ensureSoučasnýProces())
	cpu.Eip = záznam
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStav) int32 {
	rodičpid := Současnýpid()
	if ensureSoučasnýProces() == nil {
		return Enfile
	}
	pid := allocateProces(rodičpid)
	if pid == 0 {
		return Einval
	}
	paměťmanager := &mem.TPaměťmanager{}
	threadKurzor := paměťmanager.Přidělit_paměť(uint32(Sizeof(TThread{})))
	stackKurzor := paměťmanager.Přidělit_paměť(ThreadstackVelikost)
	synStránkaadresář := CloneAdresaMezeracow(getcr3())
	if threadKurzor == nil || stackKurzor == nil || synStránkaadresář == 0 {
		zahoditProces(pid)
		return Einval
	}
	syn := (*TThread)(threadKurzor)
	syn.Stack = uint32(uintptr(stackKurzor))
	syn.CpuStav = (*TcpuStav)(Pointer(uintptr(stackKurzor) + ThreadstackVelikost - Sizeof(TcpuStav{})))
	*syn.CpuStav = *cpu
	syn.CpuStav.Eax = 0
	syn.Uživatelstack_2 = cpu.Esp
	syn.UživatelstackVelikost_2 = 0
	syn.Pid = pid
	syn.Rodičpid = rodičpid
	syn.StránkaadresářZáznam = synStránkaadresář
	syn.ThreadStav = Připraven
	syn.Fpuoffset = 0xffffffff
	syn.Iskernel = false
	Přidatrunnablethread(syn)
	return int32(pid)
}

func sysKonec(stav uint32) {
	pid := Současnýpid()
	for i := 0; i < len(procesTabulka); i++ {
		if procesTabulka[i].použito && procesTabulka[i].pid == pid {
			zavřítVšeProcesfds(&procesTabulka[i])
			procesTabulka[i].skončil = true
			procesTabulka[i].stav = (stav & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, stavAdresa uint32, možnosti uint32) int32 {
	if (možnosti & ^uint32(1)) != 0 {
		return Einval
	}
	rodičpid := Současnýpid()
	foundsyn := false
	for i := 0; i < len(procesTabulka); i++ {
		p := &procesTabulka[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.použito && matches && p.rodič == rodičpid {
			foundsyn = true
			if p.skončil {
				if stavAdresa != 0 {
					*(*uint32)(Pointer(uintptr(stavAdresa))) = p.stav
				}
				synpid := p.pid
				*p = procesZáznam{}
				return int32(synpid)
			}
		}
	}
	if !foundsyn {
		return Echild
	}

	if (možnosti & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(rodič uint32) uint32 {
	rodičProces := hledatProces(rodič)
	pid := Allocatepid()
	for i := 0; i < len(procesTabulka); i++ {
		if !procesTabulka[i].použito {
			procesTabulka[i] = procesZáznam{
				použito:	true,
				pid:		pid,
				rodič:		rodič,
				programbreak:	uživatelheapbase,
			}
			if rodičProces != nil {
				procesTabulka[i].programbreak = rodičProces.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if rodičProces.fds[fd].použito {
						procesTabulka[i].fds[fd] = rodičProces.fds[fd]
						popis := rodičProces.fds[fd].popis
						if popis >= 0 && popis < maxOtevřítSOUBORY {
							otevřítSouborTabulka[popis].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabulka[i])
			}
			return pid
		}
	}
	return 0
}

func zavřítVšeProcesfds(proces *procesZáznam) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].použito {
			zavřítProcesfd(proces, fd)
		}
	}
}

func zahoditProces(pid uint32) {
	proces := hledatProces(pid)
	if proces == nil {
		return
	}
	zavřítVšeProcesfds(proces)
	*proces = procesZáznam{}
}

func kopírovatCESTA(cESTAAdresa uint32) (uint32, [12]byte) {
	var název [12]byte
	if cESTAAdresa == 0 {
		return 0, název
	}
	raw := GetBytůzKurzor(uintptr(cESTAAdresa), 64, 64)
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
		název[n] = c
		n++
	}
	return n, název
}

func souborVelikost(názevsouboru []byte) uint32 {
	var ata0s = TPokročiléTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabulka{}
	partition.Čtenípartition(&ata0s)

	bios := TParametry_souborového_systému32{}
	velikost := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru)
	ata0s.Flush()
	return velikost
}

func čteníSoubor(názevsouboru []byte, data []byte) {
	var ata0s = TPokročiléTechnologieattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabulka{}
	partition.Čtenípartition(&ata0s)

	bios := TParametry_souborového_systému32{}
	bios.Čtení(&ata0s, partition.Mbr.Primarypartition[0], názevsouboru, data)
	ata0s.Flush()
}

func getcr3() uint32
