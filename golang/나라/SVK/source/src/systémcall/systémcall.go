/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systémcall

import . "unsafe"

import . "prerušenie"
import . "konzola"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "súborSystém/msdospartition"
import . "súborSystém/fat"
import . "súborSystém/elf"
import mem "pamäťmanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuálnyPamäť"

var konzola_2 = TKonzola{}

type TSyscall struct {
	TPrerušeniehandler
}

const (
	SysKoniec	uint32	= 1
	Sysfork		uint32	= 2
	SysČítanie	uint32	= 3
	SysZápis	uint32	= 4
	SysOtvoriť	uint32	= 5
	SysZavrieť	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	SysPrístup	uint32	= 33
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
	SysrtKoniec	uint32	= 252

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
	maxOtvoriťSúbory		= 128
)

type fdpoložka struct {
	využité		bool
	popis		int32
	fdPríznaky	uint32
}

type otvoriťSúborPopis struct {
	využité		bool
	refs		uint32
	typ		uint32
	príznaky	uint32
	pozícia		uint32
	veľkosť		uint32
	názov		[12]byte
	názovlen	uint32
	aux		uint32
}

const (
	fdTypŽiadne		uint32	= 0
	fdTypfat		uint32	= 1
	fdTypstdin		uint32	= 2
	fdTypKonzola		uint32	= 3
	fdTypKoreňAdresár	uint32	= 4
	fdTypSoket		uint32	= 5

	oČítanieonly	uint32	= 0
	oZápisonly	uint32	= 1
	oČítanieZápis	uint32	= 2
	ocreate		uint32	= 0x40
	oOrezať		uint32	= 0x200
	oappend		uint32	= 0x400
	oAdresár	uint32	= 0x10000

	seeksada	uint32	= 0
	seekAktuálny	uint32	= 1
	seekKoniec	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fsadafd		uint32	= 2
	fgetfl		uint32	= 3
	fsadafl		uint32	= 4
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
	maxSoketpaketov		= 8
	maxdatagramVeľkosť	= 512
)

type soketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Nula	[8]byte
}

type soketpacket struct {
	využité	bool
	veľkosť	uint32
	zdroj	soketaddressipv4
	data	[maxdatagramVeľkosť]byte
}

type miestnydatagramSoket struct {
	využité		bool
	bound		bool
	connected	bool
	miestny		soketaddressipv4
	remote		soketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	paketov		[maxSoketpaketov]soketpacket
}

type posixstat struct {
	Zariadenie	uint32
	Ino		uint32
	Režim		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Veľkosť_2	int32
	Blksize		int32
	Blok		int32
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
	Verzia		[65]byte
	Machine		[65]byte
}

const (
	maxSpúšťanievectorpoložka	= 16
	maxSpúšťaniereťazecDĺžka	= 63
)

type spúšťanievector struct {
	count	uint32
	lengths	[maxSpúšťanievectorpoložka]uint32
	hodnoty	[maxSpúšťanievectorpoložka][maxSpúšťaniereťazecDĺžka + 1]byte
}

type procespoložka struct {
	využité		bool
	pid		uint32
	rodič		uint32
	ukončené	bool
	stav		uint32
	programbreak	uint32
	fds		[maxfd]fdpoložka
}

type reťazecheader struct {
	Data	uintptr
	Len	int
}

func syscallChyba(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var otvoriťSúborTabuľka [maxOtvoriťSúbory]otvoriťSúborPopis
var procesTabuľka [32]procespoložka
var miestnysockets [maxsockets]miestnydatagramSoket
var nasledujúciephemeralport uint16 = 49152

const (
	používateľheapbase		uint32	= 0x06000000
	používateľheapObmedzenie	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinČítanie uint32
var stdinZápis uint32

func Prerušenie(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysKoniec_2(index uint32) {
	Syscall(SysKoniec, index)
}

func SysČítanie_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysČítanie, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysTlačiťstr(buffer string) {
	h := (*reťazecheader)(Pointer(&buffer))
	Syscall(SysZápis, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysTlačiťunsignedinteger32(buffer uint32) {
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

func SysOtvoriť_2(cESTA uintptr, príznaky uint32, režim uint32) int32 {
	return int32(Syscall(SysOtvoriť, uint32(cESTA), príznaky, režim))
}

func SysZavrieť_2(fd uint32) int32 {
	return int32(Syscall(SysZavrieť, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametre ...uint32) uint32 {

	l := len(parametre)
	switch l {
	case 1:
		return Prerušenie(parametre[0], 0, 0, 0, 0, 0)
	case 2:
		return Prerušenie(parametre[0], parametre[1], 0, 0, 0, 0)
	case 3:
		return Prerušenie(parametre[0], parametre[1], parametre[2], 0, 0, 0)
	case 4:
		return Prerušenie(parametre[0], parametre[1], parametre[2], parametre[3], 0, 0)
	case 5:
		return Prerušenie(parametre[0], parametre[1], parametre[2], parametre[3], parametre[4], 0)
	case 6:
		return Prerušenie(parametre[0], parametre[1], parametre[2], parametre[3], parametre[4], parametre[5])
	default:
		return syscallChyba(Enosys)
	}
}

func (vlastný *TSyscall) Init(manager *TPrerušeniemanager) {
	initSúbordescriptor()

	prerušeniehandler = uškoPrerušenie

	var address uintptr
	address = uintptr(Pointer(&prerušeniehandler))

	vlastný.TPrerušeniehandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var prerušeniehandler func(uint32) uint32

func uškoPrerušenie(esp uint32) uint32 {
	var procesor = (*TcpuStav)(Pointer(uintptr(esp)))

	switch procesor.Eax {
	case SysKoniec:
		sysKoniec(procesor.Ebx)
		return uint32(uintptr(Pointer(ZastaviťAktuálnythread(procesor))))
	case SysrtKoniec:
		sysKoniec(procesor.Ebx)
		return uint32(uintptr(Pointer(ZastaviťAktuálnythread(procesor))))
	case Sysfork:
		procesor.Eax = uint32(sysfork(procesor))
		return esp
	case SysČítanie:
		procesor.Eax = uint32(sysČítanie(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysZápis:
		procesor.Eax = uint32(sysZápis(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysOtvoriť:
		procesor.Eax = uint32(sysOtvoriť(procesor.Ebx, procesor.Ecx, procesor.Edx))
		return esp
	case Syscreat:
		procesor.Eax = uint32(sysOtvoriť(procesor.Ebx, ocreate|oZápisonly|oOrezať, procesor.Ecx))
		return esp
	case SysZavrieť:
		procesor.Eax = uint32(sysZavrieť(int32(procesor.Ebx)))
		return esp
	case Syswaitpid:
		procesor.Eax = uint32(syswaitpid(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Syslseek:
		procesor.Eax = uint32(syslseek(int32(procesor.Ebx), int32(procesor.Ecx), procesor.Edx))
		return esp
	case Sysexecve:
		procesor.Eax = uint32(sysexecve(procesor, procesor.Ebx))
		return esp
	case Sysgetpid:
		procesor.Eax = Aktuálnypid()
		return esp
	case Sysgetppid:
		procesor.Eax = Aktuálnyrodičpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		procesor.Eax = 0
		return esp
	case SysPrístup:
		procesor.Eax = uint32(sysPrístup(procesor.Ebx, procesor.Ecx))
		return esp
	case Syschdir:
		procesor.Eax = uint32(syschdir(procesor.Ebx))
		return esp
	case Sysgetcwd:
		procesor.Eax = uint32(sysgetcwd(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysdup:
		procesor.Eax = uint32(sysdup(int32(procesor.Ebx), 0))
		return esp
	case Sysdup2:
		procesor.Eax = uint32(sysdup2(int32(procesor.Ebx), int32(procesor.Ecx)))
		return esp
	case Syssocketcall:
		procesor.Eax = uint32(sysSoketcall(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfcntl:
		procesor.Eax = uint32(sysfcntl(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Sysstat, Syslstat:
		procesor.Eax = uint32(sysstat(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfstat:
		procesor.Eax = uint32(sysfstat(int32(procesor.Ebx), procesor.Ecx))
		return esp
	case Sysfsync:
		procesor.Eax = uint32(sysfsync(int32(procesor.Ebx)))
		return esp
	case Syssync:
		procesor.Eax = 0
		return esp
	case Sysuname:
		procesor.Eax = uint32(sysuname(procesor.Ebx))
		return esp
	case Sysbrk:
		procesor.Eax = sysbrk(procesor.Ebx)
		return esp
	case 9:
		konzola_2.MUnsignedinteger32Tlačiť(procesor.Ebx)
		return esp

	default:
		konzola_2.MTlačiťxy(([]byte)("sys["), 1, 23)
		konzola_2.MUnsignedinteger32Tlačiť(esp)
		konzola_2.MTlačiť(([]byte)(":"))
		konzola_2.MUnsignedinteger32Tlačiť(procesor.Eax)
		konzola_2.MTlačiť(([]byte)(":"))
		konzola_2.MUnsignedinteger32Tlačiť(procesor.Ebx)
		konzola_2.MTlačiť(([]byte)(":"))
		konzola_2.MUnsignedinteger32Tlačiť(procesor.Ecx)
		konzola_2.MTlačiť(([]byte)(":"))
		konzola_2.MUnsignedinteger32Tlačiť(procesor.Edx)
		konzola_2.MTlačiť(([]byte)("]"))
		procesor.Eax = syscallChyba(Enosys)
		return esp
	}

	return esp
}

func initSúbordescriptor() {
	for i := 0; i < maxOtvoriťSúbory; i++ {
		otvoriťSúborTabuľka[i] = otvoriťSúborPopis{}
	}
	for i := 0; i < len(procesTabuľka); i++ {
		procesTabuľka[i] = procespoložka{}
	}
	for i := 0; i < len(miestnysockets); i++ {
		miestnysockets[i] = miestnydatagramSoket{}
	}
	nasledujúciephemeralport = 49152
	otvoriťSúborTabuľka[0] = otvoriťSúborPopis{využité: true, typ: fdTypstdin, príznaky: oČítanieonly}
	otvoriťSúborTabuľka[1] = otvoriťSúborPopis{využité: true, typ: fdTypKonzola, príznaky: oZápisonly}
	otvoriťSúborTabuľka[2] = otvoriťSúborPopis{využité: true, typ: fdTypKonzola, príznaky: oZápisonly}
}

func nájsťProces(pid uint32) *procespoložka {
	for i := 0; i < len(procesTabuľka); i++ {
		if procesTabuľka[i].využité && procesTabuľka[i].pid == pid {
			return &procesTabuľka[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procespoložka) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proces.fds[fd] = fdpoložka{využité: true, popis: fd}
		otvoriťSúborTabuľka[fd].refs++
	}
}

func ensureAktuálnyProces() *procespoložka {
	pid := Aktuálnypid()
	if proces := nájsťProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabuľka); i++ {
		if !procesTabuľka[i].využité {
			procesTabuľka[i] = procespoložka{
				využité:	true,
				pid:		pid,
				rodič:		Aktuálnyrodičpid(),
				programbreak:	používateľheapbase,
			}
			initializeProcesfds(&procesTabuľka[i])
			return &procesTabuľka[i]
		}
	}
	return nil
}

func getOtvoriťSúborfor(proces *procespoložka, fd int32) *otvoriťSúborPopis {
	if proces == nil || fd < 0 || fd >= maxfd || !proces.fds[fd].využité {
		return nil
	}
	popis := proces.fds[fd].popis
	if popis < 0 || popis >= maxOtvoriťSúbory || !otvoriťSúborTabuľka[popis].využité {
		return nil
	}
	return &otvoriťSúborTabuľka[popis]
}

func getOtvoriťSúbor(fd int32) *otvoriťSúborPopis {
	return getOtvoriťSúborfor(ensureAktuálnyProces(), fd)
}

func allocateOtvoriťSúbor() int32 {
	for i := int32(3); i < maxOtvoriťSúbory; i++ {
		if !otvoriťSúborTabuľka[i].využité {
			otvoriťSúborTabuľka[i] = otvoriťSúborPopis{využité: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proces *procespoložka, popis int32, minimum int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !proces.fds[fd].využité {
			proces.fds[fd] = fdpoložka{využité: true, popis: popis}
			return fd
		}
	}
	return Emfile
}

func releaseOtvoriťSúbor(popis int32) {
	if popis < 0 || popis >= maxOtvoriťSúbory {
		return
	}
	položka := &otvoriťSúborTabuľka[popis]
	if položka.refs > 0 {
		položka.refs--
	}

	if položka.refs == 0 && popis > stderrfd {
		if položka.typ == fdTypSoket && položka.aux < maxsockets {
			miestnysockets[položka.aux] = miestnydatagramSoket{}
		}
		*položka = otvoriťSúborPopis{}
	}
}

func zavrieťProcesfd(proces *procespoložka, fd int32) int32 {
	if proces == nil || getOtvoriťSúborfor(proces, fd) == nil {
		return Ebadf
	}
	popis := proces.fds[fd].popis
	proces.fds[fd] = fdpoložka{}
	releaseOtvoriťSúbor(popis)
	return 0
}

func sysZápis(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	položka := getOtvoriťSúbor(fd)
	if položka == nil {
		return Ebadf
	}
	if položka.typ != fdTypKonzola {
		if položka.typ == fdTypSoket {
			return soketPoslaťto(fd, address, count, 0, 0)
		}
		if položka.typ == fdTypfat || položka.typ == fdTypKoreňAdresár {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtyzKurzor(uintptr(address), int(count), int(count))
	konzola_2.MTlačiť(buffer)
	return int32(count)
}

func sysČítanie(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	položka := getOtvoriťSúbor(fd)
	if položka == nil {
		return Ebadf
	}
	if položka.typ == fdTypstdin {
		return čítaniestdin(address, count)
	}
	if položka.typ == fdTypKoreňAdresár {
		return Eisdir
	}
	if položka.typ == fdTypSoket {
		return soketreceivez(fd, address, count, 0, 0)
	}
	if položka.typ != fdTypfat {
		return Ebadf
	}
	if položka.pozícia >= položka.veľkosť {
		return 0
	}
	remaining := položka.veľkosť - položka.pozícia
	if count > remaining {
		count = remaining
	}
	buffer := GetBajtyzKurzor(uintptr(address), int(count), int(count))
	return čítanievfsSúbor(položka, buffer, count)
}

func sysOtvoriť(cESTAaddress uint32, príznaky uint32, režim uint32) int32 {
	_ = režim
	if cESTAaddress == 0 {
		return Efault
	}
	prístuprežim := príznaky & 3
	if prístuprežim == oZápisonly || prístuprežim == oČítanieZápis || (príznaky&(ocreate|oOrezať|oappend)) != 0 {
		return Erofs
	}

	proces := ensureAktuálnyProces()
	if proces == nil {
		return Enfile
	}
	popis := allocateOtvoriťSúbor()
	if popis < 0 {
		return popis
	}
	položka := &otvoriťSúborTabuľka[popis]
	položka.príznaky = príznaky
	if isKoreňCESTA(cESTAaddress) {
		položka.typ = fdTypKoreňAdresár
		položka.veľkosť = 0
	} else {
		názovlen, názov := kopírovaťCESTA(cESTAaddress)
		if názovlen == 0 {
			*položka = otvoriťSúborPopis{}
			return Enoent
		}
		veľkosť := súborVeľkosť(názov[:názovlen])
		if veľkosť == 0 {
			*položka = otvoriťSúborPopis{}
			return Enoent
		}
		if (príznaky & oAdresár) != 0 {
			*položka = otvoriťSúborPopis{}
			return Enotdir
		}
		položka.typ = fdTypfat
		položka.veľkosť = veľkosť
		položka.názovlen = názovlen
		položka.názov = názov
	}

	fd := allocatefd(proces, popis, 3)
	if fd < 0 {
		*položka = otvoriťSúborPopis{}
		return fd
	}
	return fd
}

func sysZavrieť(fd int32) int32 {
	return zavrieťProcesfd(ensureAktuálnyProces(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	proces := ensureAktuálnyProces()
	položka := getOtvoriťSúborfor(proces, fd)
	if položka == nil {
		return Ebadf
	}
	novýfd := allocatefd(proces, proces.fds[fd].popis, minimum)
	if novýfd >= 0 {
		položka.refs++
	}
	return novýfd
}

func sysdup2(oldfd int32, novýfd int32) int32 {
	proces := ensureAktuálnyProces()
	položka := getOtvoriťSúborfor(proces, oldfd)
	if položka == nil {
		return Ebadf
	}
	if novýfd < 0 || novýfd >= maxfd {
		return Ebadf
	}
	if oldfd == novýfd {
		return novýfd
	}
	if proces.fds[novýfd].využité {
		zavrieťProcesfd(proces, novýfd)
	}
	proces.fds[novýfd] = fdpoložka{využité: true, popis: proces.fds[oldfd].popis}
	položka.refs++
	return novýfd
}

func sysfcntl(fd int32, príkaz uint32, argument uint32) int32 {
	proces := ensureAktuálnyProces()
	položka := getOtvoriťSúborfor(proces, fd)
	if položka == nil {
		return Ebadf
	}
	switch príkaz {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proces.fds[fd].fdPríznaky)
	case fsadafd:
		proces.fds[fd].fdPríznaky = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(položka.príznaky)
	case fsadafl:
		položka.príznaky = (položka.príznaky & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, posunutie int32, whence uint32) int32 {
	položka := getOtvoriťSúbor(fd)
	if položka == nil {
		return Ebadf
	}
	if položka.typ != fdTypfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seeksada:
		base = 0
	case seekAktuálny:
		base = int64(položka.pozícia)
	case seekKoniec:
		base = int64(položka.veľkosť)
	default:
		return Einval
	}
	pozícia_2 := base + int64(posunutie)
	if pozícia_2 < 0 || pozícia_2 > 0x7FFFFFFF {
		return Einval
	}
	položka.pozícia = uint32(pozícia_2)
	return int32(položka.pozícia)
}

func čítanievfsSúbor(položka *otvoriťSúborPopis, cieľ_2 []byte, count uint32) int32 {
	pamäťmanager := &mem.TPamäťmanager{}
	tmpKurzor := pamäťmanager.Malloc(položka.veľkosť)
	if tmpKurzor == nil {
		return Einval
	}
	tmp := GetBajtyzKurzor(uintptr(tmpKurzor), int(položka.veľkosť), int(položka.veľkosť))
	čítanieSúbor(položka.názov[:položka.názovlen], tmp)
	copy(cieľ_2[:count], tmp[položka.pozícia:položka.pozícia+count])
	položka.pozícia += count
	pamäťmanager.Voľné(tmpKurzor)
	return int32(count)
}

func isKoreňCESTA(cESTAaddress uint32) bool {
	if cESTAaddress == 0 {
		return false
	}
	cESTA := GetBajtyzKurzor(uintptr(cESTAaddress), 4, 4)
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

func sysPrístup(cESTAaddress uint32, režim uint32) int32 {
	if cESTAaddress == 0 {
		return Efault
	}
	if (režim & ^uint32(7)) != 0 {
		return Einval
	}
	isKoreň := isKoreňCESTA(cESTAaddress)
	exists := isKoreň
	if !exists {
		názovlen, názov := kopírovaťCESTA(cESTAaddress)
		exists = názovlen != 0 && súborVeľkosť(názov[:názovlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (režim & 2) != 0 {
		return Eacces
	}

	if (režim&1) != 0 && !isKoreň {
		return Eacces
	}
	return 0
}

func syschdir(cESTAaddress uint32) int32 {
	if cESTAaddress == 0 {
		return Efault
	}
	if !isKoreňCESTA(cESTAaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, veľkosť uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if veľkosť < 2 {
		return Erange
	}
	buffer_2 := GetBajtyzKurzor(uintptr(bufferaddress), int(veľkosť), int(veľkosť))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, režim uint32, veľkosť uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Zariadenie = 1
	stat.Ino = inode
	stat.Režim = režim
	stat.Nlink = 1
	stat.Veľkosť_2 = int32(veľkosť)
	stat.Blksize = 512
	stat.Blok = int32((veľkosť + 511) / 512)
	return 0
}

func sysstat(cESTAaddress uint32, stataddress uint32) int32 {
	if cESTAaddress == 0 {
		return Efault
	}
	if isKoreňCESTA(cESTAaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	názovlen, názov := kopírovaťCESTA(cESTAaddress)
	if názovlen == 0 {
		return Enoent
	}
	veľkosť := súborVeľkosť(názov[:názovlen])
	if veľkosť == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < názovlen; i++ {
		inode = inode*33 + uint32(názov[i])
	}
	return fillposixstat(stataddress, sifreg|0444, veľkosť, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	položka := getOtvoriťSúbor(fd)
	if položka == nil {
		return Ebadf
	}
	switch položka.typ {
	case fdTypstdin, fdTypKonzola:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdTypKoreňAdresár:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdTypfat:
		return fillposixstat(stataddress, sifreg|0444, položka.veľkosť, uint32(fd+2))
	case fdTypSoket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOtvoriťSúbor(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureAktuálnyProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = používateľheapbase
	}
	if address_2 == 0 {
		return proces.programbreak
	}
	if address_2 < používateľheapbase || address_2 > používateľheapObmedzenie {
		return proces.programbreak
	}
	proces.programbreak = address_2
	return proces.programbreak
}

func kopírovaťutspole(cieľ *[65]byte, hodnota string) {
	obmedzenie := len(hodnota)
	if obmedzenie > 64 {
		obmedzenie = 64
	}
	for i := 0; i < obmedzenie; i++ {
		cieľ[i] = hodnota[i]
	}
	cieľ[obmedzenie] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	názov := (*posixutsname)(Pointer(uintptr(address_2)))
	*názov = posixutsname{}
	kopírovaťutspole(&názov.Sysname, "EngOS")
	kopírovaťutspole(&názov.Nodename, "engos")
	kopírovaťutspole(&názov.Release, "0.1-posix")
	kopírovaťutspole(&názov.Verzia, "POSIX.1-2017 phase 1")
	kopírovaťutspole(&názov.Machine, "i386")
	return 0
}

func odkladacípriestorunsignedinteger16(hodnota uint16) uint16 {
	return (hodnota << 8) | (hodnota >> 8)
}

func soketcallargument(argumenty_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenty_2 + index*4)))
}

func soketforfd(fd int32) (*miestnydatagramSoket, int32) {
	položka := getOtvoriťSúbor(fd)
	if položka == nil || položka.typ != fdTypSoket || položka.aux >= maxsockets {
		return nil, Ebadf
	}
	soket := &miestnysockets[položka.aux]
	if !soket.využité {
		return nil, Ebadf
	}
	return soket, 0
}

func allocateSoket(doména uint32, soketTyp uint32, protocol uint32) int32 {
	if doména != afinet {
		return Eafnosupport
	}
	if soketTyp != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureAktuálnyProces()
	if proces == nil {
		return Enfile
	}
	soketindex := -1
	for i := 0; i < maxsockets; i++ {
		if !miestnysockets[i].využité {
			soketindex = i
			break
		}
	}
	if soketindex < 0 {
		return Enfile
	}
	popis := allocateOtvoriťSúbor()
	if popis < 0 {
		return popis
	}
	miestnysockets[soketindex] = miestnydatagramSoket{využité: true}
	položka := &otvoriťSúborTabuľka[popis]
	položka.typ = fdTypSoket
	položka.príznaky = oČítanieZápis
	položka.aux = uint32(soketindex)
	fd := allocatefd(proces, popis, 3)
	if fd < 0 {
		miestnysockets[soketindex] = miestnydatagramSoket{}
		*položka = otvoriťSúborPopis{}
		return fd
	}
	return fd
}

func soketaddress(address_2 uint32, dĺžka uint32) (*soketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if dĺžka < 16 {
		return nil, Einval
	}
	result := (*soketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portnaPoužiť(port uint16, except *miestnydatagramSoket) bool {
	for i := 0; i < maxsockets; i++ {
		soket := &miestnysockets[i]
		if soket != except && soket.využité && soket.bound && soket.miestny.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(soket *miestnydatagramSoket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := odkladacípriestorunsignedinteger16(nasledujúciephemeralport)
		nasledujúciephemeralport++
		if nasledujúciephemeralport < 49152 {
			nasledujúciephemeralport = 49152
		}
		if !portnaPoužiť(port, soket) {
			soket.miestny = soketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			soket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func soketbind(fd int32, address_2 uint32, dĺžka uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := soketaddress(address_2, dĺžka)
	if err != 0 {
		return err
	}
	if soket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(soket)
	}
	if portnaPoužiť(requested.Port, soket) {
		return Eaddrinuse
	}
	soket.miestny = *requested
	soket.bound = true
	return 0
}

func soketPripojiť(fd int32, address_2 uint32, dĺžka uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := soketaddress(address_2, dĺžka)
	if err != 0 {
		return err
	}
	if !soket.bound {
		if err := bindephemeral(soket); err != 0 {
			return err
		}
	}
	soket.remote = *remote
	soket.connected = true
	return 0
}

func soketPoslaťto(fd int32, bufferaddress_2 uint32, dĺžka uint32, cieľaddress uint32, cieľDĺžka uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if dĺžka > maxdatagramVeľkosť {
		return Emsgsize
	}
	if dĺžka != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var cieľ soketaddressipv4
	if cieľaddress != 0 {
		address_2, addressChyba := soketaddress(cieľaddress, cieľDĺžka)
		if addressChyba != 0 {
			return addressChyba
		}
		cieľ = *address_2
	} else {
		if !soket.connected {
			return Enotconn
		}
		cieľ = soket.remote
	}
	if !soket.bound {
		if bindChyba := bindephemeral(soket); bindChyba != 0 {
			return bindChyba
		}
	}
	var receiver *miestnydatagramSoket
	for i := 0; i < maxsockets; i++ {
		candidate := &miestnysockets[i]
		if candidate.využité && candidate.bound && candidate.miestny.Port == cieľ.Port &&
			(candidate.miestny.Address == 0 || candidate.miestny.Address == cieľ.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxSoketpaketov {
		return Eagain
	}
	packet := &receiver.paketov[receiver.tail]
	*packet = soketpacket{využité: true, veľkosť: dĺžka, zdroj: soket.miestny}
	if dĺžka != 0 {
		zdroj := GetBajtyzKurzor(uintptr(bufferaddress_2), int(dĺžka), int(dĺžka))
		copy(packet.data[:dĺžka], zdroj)
	}
	receiver.tail = (receiver.tail + 1) % maxSoketpaketov
	receiver.count++
	return int32(dĺžka)
}

func soketreceivez(fd int32, bufferaddress_2 uint32, dĺžka uint32, zdrojaddress uint32, zdrojDĺžkaaddress uint32) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if dĺžka != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if soket.count == 0 {
		return Eagain
	}
	packet := &soket.paketov[soket.head]
	kopírovaťDĺžka := packet.veľkosť
	if kopírovaťDĺžka > dĺžka {
		kopírovaťDĺžka = dĺžka
	}
	if kopírovaťDĺžka != 0 {
		cieľ := GetBajtyzKurzor(uintptr(bufferaddress_2), int(kopírovaťDĺžka), int(kopírovaťDĺžka))
		copy(cieľ, packet.data[:kopírovaťDĺžka])
	}
	if zdrojaddress != 0 {
		if zdrojDĺžkaaddress == 0 {
			return Efault
		}
		providedDĺžka := (*uint32)(Pointer(uintptr(zdrojDĺžkaaddress)))
		if *providedDĺžka >= 16 {
			*(*soketaddressipv4)(Pointer(uintptr(zdrojaddress))) = packet.zdroj
		}
		*providedDĺžka = 16
	}
	*packet = soketpacket{}
	soket.head = (soket.head + 1) % maxSoketpaketov
	soket.count--
	return int32(kopírovaťDĺžka)
}

func kopírovaťSoketNázov(fd int32, address_2 uint32, dĺžkaaddress uint32, peer bool) int32 {
	soket, err := soketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || dĺžkaaddress == 0 {
		return Efault
	}
	dĺžka := (*uint32)(Pointer(uintptr(dĺžkaaddress)))
	if *dĺžka < 16 {
		*dĺžka = 16
		return Einval
	}
	if peer {
		if !soket.connected {
			return Enotconn
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.remote
	} else {
		if !soket.bound {
			if bindChyba := bindephemeral(soket); bindChyba != 0 {
				return bindChyba
			}
		}
		*(*soketaddressipv4)(Pointer(uintptr(address_2))) = soket.miestny
	}
	*dĺžka = 16
	return 0
}

func sysSoketcall(call uint32, argumenty_2 uint32) int32 {
	if argumenty_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSoket(soketcallargument(argumenty_2, 0), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2))
	case 2:
		return soketbind(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2))
	case 3:
		return soketPripojiť(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopírovaťSoketNázov(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), false)
	case 7:
		return kopírovaťSoketNázov(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), true)
	case 9:
		return soketPoslaťto(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), 0, 0)
	case 10:
		return soketreceivez(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), 0, 0)
	case 11:
		return soketPoslaťto(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), soketcallargument(argumenty_2, 4), soketcallargument(argumenty_2, 5))
	case 12:
		return soketreceivez(int32(soketcallargument(argumenty_2, 0)), soketcallargument(argumenty_2, 1), soketcallargument(argumenty_2, 2), soketcallargument(argumenty_2, 4), soketcallargument(argumenty_2, 5))
	case 13:
		if _, err := soketforfd(int32(soketcallargument(argumenty_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := soketforfd(int32(soketcallargument(argumenty_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func čítaniestdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBajtyzKurzor(uintptr(address), int(count), int(count))
	var n uint32
	for n < count {
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
	nasledujúci := (stdinZápis + 1) % uint32(len(stdinbuffer))
	if nasledujúci == stdinČítanie {
		return
	}
	stdinbuffer[stdinZápis] = c
	stdinZápis = nasledujúci
}

func stdingetblocking() byte {
	for stdinČítanie == stdinZápis {
		sc := pollKlávesnicascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinČítanie]
	stdinČítanie = (stdinČítanie + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKlávesnicascancode() byte {
	for (PortČítaniebyte(0x64) & 0x01) == 0 {
	}
	sc := PortČítaniebyte(0x60)
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

func kopírovaťSpúšťanievector(address_2 uint32, result *spúšťanievector) int32 {
	*result = spúšťanievector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxSpúšťanievectorpoložka; index++ {
		reťazecaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if reťazecaddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for dĺžka := uint32(0); dĺžka <= maxSpúšťaniereťazecDĺžka; dĺžka++ {
			hodnota := *(*byte)(Pointer(uintptr(reťazecaddress + dĺžka)))
			result.hodnoty[index][dĺžka] = hodnota
			if hodnota == 0 {
				result.lengths[index] = dĺžka
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

func pushSpúšťanieunsignedinteger32(stack *uint32, hodnota uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = hodnota
}

func setupSpúšťaniestack(procesor *TcpuStav, argumenty_2 *spúšťanievector, environment *spúšťanievector) int32 {
	const stackBajty uint32 = 4096
	if !MakeRozsahSúkromnáwritable(getcr3(), PoužívateľstackHore-stackBajty, stackBajty) {
		return Enomem
	}
	stack := PoužívateľstackHore
	var argumentpointers [maxSpúšťanievectorpoložka]uint32
	var environmentpointers [maxSpúšťanievectorpoložka]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		dĺžka := environment.lengths[i] + 1
		stack -= dĺžka
		cieľ := GetBajtyzKurzor(uintptr(stack), int(dĺžka), int(dĺžka))
		copy(cieľ, environment.hodnoty[i][:dĺžka])
		environmentpointers[i] = stack
	}
	for i := int(argumenty_2.count) - 1; i >= 0; i-- {
		dĺžka := argumenty_2.lengths[i] + 1
		stack -= dĺžka
		cieľ := GetBajtyzKurzor(uintptr(stack), int(dĺžka), int(dĺžka))
		copy(cieľ, argumenty_2.hodnoty[i][:dĺžka])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushSpúšťanieunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushSpúšťanieunsignedinteger32(&stack, environmentpointers[i])
	}
	pushSpúšťanieunsignedinteger32(&stack, 0)
	for i := int(argumenty_2.count) - 1; i >= 0; i-- {
		pushSpúšťanieunsignedinteger32(&stack, argumentpointers[i])
	}
	pushSpúšťanieunsignedinteger32(&stack, argumenty_2.count)
	procesor.Esp = stack
	procesor.Ebp = 0
	return 0
}

func zavrieťZapnutéSpúšťanie(proces *procespoložka) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].využité && (proces.fds[fd].fdPríznaky&fdcloexec) != 0 {
			zavrieťProcesfd(proces, fd)
		}
	}
}

func sysexecve(procesor *TcpuStav, cESTAaddress uint32) int32 {
	if cESTAaddress == 0 {
		return Efault
	}
	var argumenty_2 spúšťanievector
	var environment spúšťanievector
	if result := kopírovaťSpúšťanievector(procesor.Ecx, &argumenty_2); result < 0 {
		return result
	}
	if result := kopírovaťSpúšťanievector(procesor.Edx, &environment); result < 0 {
		return result
	}
	názovlen, názov := kopírovaťCESTA(cESTAaddress)
	if názovlen == 0 {
		return Enoent
	}
	veľkosť := súborVeľkosť(názov[:názovlen])
	if veľkosť == 0 {
		return Enoent
	}
	pamäťmanager := &mem.TPamäťmanager{}
	súborKurzor := pamäťmanager.Malloc(veľkosť)
	if súborKurzor == nil {
		return Einval
	}
	data := GetBajtyzKurzor(uintptr(súborKurzor), int(veľkosť), int(veľkosť))
	čítanieSúbor(názov[:názovlen], data)
	if veľkosť < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		pamäťmanager.Voľné(súborKurzor)
		return Enoexec
	}
	loader := Elf{}
	položka := loader.Getpoložka(data)
	loader.Parse(data, getcr3())
	pamäťmanager.Voľné(súborKurzor)
	if result := setupSpúšťaniestack(procesor, &argumenty_2, &environment); result < 0 {
		return result
	}
	zavrieťZapnutéSpúšťanie(ensureAktuálnyProces())
	procesor.Eip = položka
	procesor.Eax = 0
	return 0
}

func sysfork(procesor *TcpuStav) int32 {
	rodičpid := Aktuálnypid()
	if ensureAktuálnyProces() == nil {
		return Enfile
	}
	pid := allocateProces(rodičpid)
	if pid == 0 {
		return Einval
	}
	pamäťmanager := &mem.TPamäťmanager{}
	threadKurzor := pamäťmanager.Malloc(uint32(Sizeof(TThread{})))
	stackKurzor := pamäťmanager.Malloc(ThreadstackVeľkosť)
	dieťaSTRANAAdresár := CloneaddressMedzeracow(getcr3())
	if threadKurzor == nil || stackKurzor == nil || dieťaSTRANAAdresár == 0 {
		zahodiťProces(pid)
		return Einval
	}
	dieťa := (*TThread)(threadKurzor)
	dieťa.Stack = uint32(uintptr(stackKurzor))
	dieťa.ProcesorStav = (*TcpuStav)(Pointer(uintptr(stackKurzor) + ThreadstackVeľkosť - Sizeof(TcpuStav{})))
	*dieťa.ProcesorStav = *procesor
	dieťa.ProcesorStav.Eax = 0
	dieťa.Používateľstack_2 = procesor.Esp
	dieťa.PoužívateľstackVeľkosť_2 = 0
	dieťa.Pid = pid
	dieťa.Rodičpid = rodičpid
	dieťa.STRANAAdresárpoložka = dieťaSTRANAAdresár
	dieťa.ThreadStav = Pripravený
	dieťa.FpuPosunutie = 0xffffffff
	dieťa.Iskernel = false
	Pridaťrunnablethread(dieťa)
	return int32(pid)
}

func sysKoniec(stav uint32) {
	pid := Aktuálnypid()
	for i := 0; i < len(procesTabuľka); i++ {
		if procesTabuľka[i].využité && procesTabuľka[i].pid == pid {
			zavrieťVšetkyProcesfds(&procesTabuľka[i])
			procesTabuľka[i].ukončené = true
			procesTabuľka[i].stav = (stav & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, stavaddress uint32, možnosti uint32) int32 {
	if (možnosti & ^uint32(1)) != 0 {
		return Einval
	}
	rodičpid := Aktuálnypid()
	founddieťa := false
	for i := 0; i < len(procesTabuľka); i++ {
		p := &procesTabuľka[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.využité && matches && p.rodič == rodičpid {
			founddieťa = true
			if p.ukončené {
				if stavaddress != 0 {
					*(*uint32)(Pointer(uintptr(stavaddress))) = p.stav
				}
				dieťapid := p.pid
				*p = procespoložka{}
				return int32(dieťapid)
			}
		}
	}
	if !founddieťa {
		return Echild
	}

	if (možnosti & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(rodič uint32) uint32 {
	rodičProces := nájsťProces(rodič)
	pid := Allocatepid()
	for i := 0; i < len(procesTabuľka); i++ {
		if !procesTabuľka[i].využité {
			procesTabuľka[i] = procespoložka{
				využité:	true,
				pid:		pid,
				rodič:		rodič,
				programbreak:	používateľheapbase,
			}
			if rodičProces != nil {
				procesTabuľka[i].programbreak = rodičProces.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if rodičProces.fds[fd].využité {
						procesTabuľka[i].fds[fd] = rodičProces.fds[fd]
						popis := rodičProces.fds[fd].popis
						if popis >= 0 && popis < maxOtvoriťSúbory {
							otvoriťSúborTabuľka[popis].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabuľka[i])
			}
			return pid
		}
	}
	return 0
}

func zavrieťVšetkyProcesfds(proces *procespoložka) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].využité {
			zavrieťProcesfd(proces, fd)
		}
	}
}

func zahodiťProces(pid uint32) {
	proces := nájsťProces(pid)
	if proces == nil {
		return
	}
	zavrieťVšetkyProcesfds(proces)
	*proces = procespoložka{}
}

func kopírovaťCESTA(cESTAaddress uint32) (uint32, [12]byte) {
	var názov [12]byte
	if cESTAaddress == 0 {
		return 0, názov
	}
	raw := GetBajtyzKurzor(uintptr(cESTAaddress), 64, 64)
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
		názov[n] = c
		n++
	}
	return n, názov
}

func súborVeľkosť(názovsúboru []byte) uint32 {
	var ata0s = TPokročiléTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabuľka{}
	partition.Čítaniepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	veľkosť := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru)
	ata0s.Flush()
	return veľkosť
}

func čítanieSúbor(názovsúboru []byte, data []byte) {
	var ata0s = TPokročiléTechnológiaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabuľka{}
	partition.Čítaniepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Čítanie(&ata0s, partition.Mbr.Primarypartition[0], názovsúboru, data)
	ata0s.Flush()
}

func getcr3() uint32
