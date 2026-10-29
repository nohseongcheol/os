/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systemcall

import . "unsafe"

import . "avbrudd"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "filsystem/msdospartition"
import . "filsystem/fat"
import . "filsystem/elf"
import mem "minnemanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuellMinne"

var console_2 = TConsole{}

type TSyscall struct {
	TAvbruddhandler
}

const (
	SysAvslutt	uint32	= 1
	Sysfork		uint32	= 2
	SysLes		uint32	= 3
	SysSkriv	uint32	= 4
	SysÅpne		uint32	= 5
	SysLukk		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Systilgang	uint32	= 33
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
	SysrtAvslutt	uint32	= 252

	Eperm		int32	= -1
	Enoent		int32	= -2
	Esrch		int32	= -3
	Eintr		int32	= -4
	Eio		int32	= -5
	E2Stor		int32	= -7
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
	stdinfd		int32	= 0
	stdoutfd	int32	= 1
	stderrfd	int32	= 2
	maksfd			= 32
	maksÅpneFILER		= 128
)

type fdentry struct {
	brukt		bool
	beskrivelse	int32
	fdFlagg		uint32
}

type åpneFilBeskrivelse struct {
	brukt		bool
	refs		uint32
	slag		uint32
	flagg		uint32
	posisjon	uint32
	størrelse	uint32
	navn		[12]byte
	navnlen		uint32
	aux		uint32
}

const (
	fdSlagIngen		uint32	= 0
	fdSlagfat		uint32	= 1
	fdSlagstdin		uint32	= 2
	fdSlagconsole		uint32	= 3
	fdSlagRotKatalog	uint32	= 4
	fdSlagsokkel		uint32	= 5

	oLesonly	uint32	= 0
	oSkrivonly	uint32	= 1
	oLesSkriv	uint32	= 2
	ocreate		uint32	= 0x40
	oAvkort		uint32	= 0x200
	oappend		uint32	= 0x400
	oKatalog	uint32	= 0x10000

	seekSett	uint32	= 0
	seekGjeldende	uint32	= 1
	seekSlutt	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fSettfd		uint32	= 2
	fgetfl		uint32	= 3
	fSettfl		uint32	= 4
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
	makssockets		= 32
	makssokkelpakker	= 8
	maksdatagramStørrelse	= 512
)

type sokkeladdressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type sokkelpacket struct {
	brukt		bool
	størrelse	uint32
	kilde		sokkeladdressipv4
	data		[maksdatagramStørrelse]byte
}

type lokaldatagramsokkel struct {
	brukt		bool
	bound		bool
	connected	bool
	lokal		sokkeladdressipv4
	remote		sokkeladdressipv4
	head		uint32
	tail		uint32
	antall		uint32
	pakker		[makssokkelpakker]sokkelpacket
}

type posixstat struct {
	Enhet		uint32
	Ino		uint32
	Modus		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Størrelse_2	int32
	Blksize		int32
	Blokk		int32
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
	Versjon		[65]byte
	Machine		[65]byte
}

const (
	maksKjørbarvectorentry	= 16
	maksKjørbarStrengLengde	= 63
)

type kjørbarvector struct {
	antall	uint32
	lengths	[maksKjørbarvectorentry]uint32
	vardier	[maksKjørbarvectorentry][maksKjørbarStrengLengde + 1]byte
}

type prosessentry struct {
	brukt		bool
	pid		uint32
	opphav		uint32
	avsluttet	bool
	status		uint32
	programbreak	uint32
	fds		[maksfd]fdentry
}

type strengTopptekst struct {
	Data	uintptr
	Len	int
}

func syscallFeil(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var åpneFilTabell [maksÅpneFILER]åpneFilBeskrivelse
var prosessTabell [32]prosessentry
var lokalsockets [makssockets]lokaldatagramsokkel
var nesteephemeralport uint16 = 49152

const (
	brukerheapbase		uint32	= 0x06000000
	brukerheapGrense	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLes uint32
var stdinSkriv uint32

func Avbrudd(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysAvslutt_2(indeks uint32) {
	Syscall(SysAvslutt, indeks)
}

func SysLes_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLes, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysSkrivutstr(buffer string) {
	h := (*strengTopptekst)(Pointer(&buffer))
	Syscall(SysSkriv, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysSkrivutunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSkriv, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysÅpne_2(sTI uintptr, flagg uint32, modus uint32) int32 {
	return int32(Syscall(SysÅpne, uint32(sTI), flagg, modus))
}

func SysLukk_2(fd uint32) int32 {
	return int32(Syscall(SysLukk, fd))
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
		return Avbrudd(parametre[0], 0, 0, 0, 0, 0)
	case 2:
		return Avbrudd(parametre[0], parametre[1], 0, 0, 0, 0)
	case 3:
		return Avbrudd(parametre[0], parametre[1], parametre[2], 0, 0, 0)
	case 4:
		return Avbrudd(parametre[0], parametre[1], parametre[2], parametre[3], 0, 0)
	case 5:
		return Avbrudd(parametre[0], parametre[1], parametre[2], parametre[3], parametre[4], 0)
	case 6:
		return Avbrudd(parametre[0], parametre[1], parametre[2], parametre[3], parametre[4], parametre[5])
	default:
		return syscallFeil(Enosys)
	}
}

func (selv *TSyscall) Init(manager *TAvbruddmanager) {
	initFildescriptor()

	avbruddhandler = håndtakAvbrudd

	var address uintptr
	address = uintptr(Pointer(&avbruddhandler))

	selv.TAvbruddhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var avbruddhandler func(uint32) uint32

func håndtakAvbrudd(esp uint32) uint32 {
	var cpu = (*TcpuStatus)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysAvslutt:
		sysAvslutt(cpu.Ebx)
		return uint32(uintptr(Pointer(StoppGjeldendethread(cpu))))
	case SysrtAvslutt:
		sysAvslutt(cpu.Ebx)
		return uint32(uintptr(Pointer(StoppGjeldendethread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLes:
		cpu.Eax = uint32(sysLes(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSkriv:
		cpu.Eax = uint32(sysSkriv(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysÅpne:
		cpu.Eax = uint32(sysÅpne(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysÅpne(cpu.Ebx, ocreate|oSkrivonly|oAvkort, cpu.Ecx))
		return esp
	case SysLukk:
		cpu.Eax = uint32(sysLukk(int32(cpu.Ebx)))
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
		cpu.Eax = Gjeldendepid()
		return esp
	case Sysgetppid:
		cpu.Eax = Gjeldendeopphavpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Systilgang:
		cpu.Eax = uint32(systilgang(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(syssokkelcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Skrivut(cpu.Ebx)
		return esp

	default:
		console_2.MSkrivutxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Skrivut(esp)
		console_2.MSkrivut(([]byte)(":"))
		console_2.MUnsignedinteger32Skrivut(cpu.Eax)
		console_2.MSkrivut(([]byte)(":"))
		console_2.MUnsignedinteger32Skrivut(cpu.Ebx)
		console_2.MSkrivut(([]byte)(":"))
		console_2.MUnsignedinteger32Skrivut(cpu.Ecx)
		console_2.MSkrivut(([]byte)(":"))
		console_2.MUnsignedinteger32Skrivut(cpu.Edx)
		console_2.MSkrivut(([]byte)("]"))
		cpu.Eax = syscallFeil(Enosys)
		return esp
	}

	return esp
}

func initFildescriptor() {
	for i := 0; i < maksÅpneFILER; i++ {
		åpneFilTabell[i] = åpneFilBeskrivelse{}
	}
	for i := 0; i < len(prosessTabell); i++ {
		prosessTabell[i] = prosessentry{}
	}
	for i := 0; i < len(lokalsockets); i++ {
		lokalsockets[i] = lokaldatagramsokkel{}
	}
	nesteephemeralport = 49152
	åpneFilTabell[0] = åpneFilBeskrivelse{brukt: true, slag: fdSlagstdin, flagg: oLesonly}
	åpneFilTabell[1] = åpneFilBeskrivelse{brukt: true, slag: fdSlagconsole, flagg: oSkrivonly}
	åpneFilTabell[2] = åpneFilBeskrivelse{brukt: true, slag: fdSlagconsole, flagg: oSkrivonly}
}

func finnProsess(pid uint32) *prosessentry {
	for i := 0; i < len(prosessTabell); i++ {
		if prosessTabell[i].brukt && prosessTabell[i].pid == pid {
			return &prosessTabell[i]
		}
	}
	return nil
}

func initializeProsessfds(prosess *prosessentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		prosess.fds[fd] = fdentry{brukt: true, beskrivelse: fd}
		åpneFilTabell[fd].refs++
	}
}

func ensureGjeldendeProsess() *prosessentry {
	pid := Gjeldendepid()
	if prosess := finnProsess(pid); prosess != nil {
		return prosess
	}
	for i := 0; i < len(prosessTabell); i++ {
		if !prosessTabell[i].brukt {
			prosessTabell[i] = prosessentry{
				brukt:		true,
				pid:		pid,
				opphav:		Gjeldendeopphavpid(),
				programbreak:	brukerheapbase,
			}
			initializeProsessfds(&prosessTabell[i])
			return &prosessTabell[i]
		}
	}
	return nil
}

func getÅpneFilfor(prosess *prosessentry, fd int32) *åpneFilBeskrivelse {
	if prosess == nil || fd < 0 || fd >= maksfd || !prosess.fds[fd].brukt {
		return nil
	}
	beskrivelse := prosess.fds[fd].beskrivelse
	if beskrivelse < 0 || beskrivelse >= maksÅpneFILER || !åpneFilTabell[beskrivelse].brukt {
		return nil
	}
	return &åpneFilTabell[beskrivelse]
}

func getÅpneFil(fd int32) *åpneFilBeskrivelse {
	return getÅpneFilfor(ensureGjeldendeProsess(), fd)
}

func allocateÅpneFil() int32 {
	for i := int32(3); i < maksÅpneFILER; i++ {
		if !åpneFilTabell[i].brukt {
			åpneFilTabell[i] = åpneFilBeskrivelse{brukt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(prosess *prosessentry, beskrivelse int32, minimum int32) int32 {
	if prosess == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maksfd {
		return Einval
	}
	for fd := minimum; fd < maksfd; fd++ {
		if !prosess.fds[fd].brukt {
			prosess.fds[fd] = fdentry{brukt: true, beskrivelse: beskrivelse}
			return fd
		}
	}
	return Emfile
}

func releaseÅpneFil(beskrivelse int32) {
	if beskrivelse < 0 || beskrivelse >= maksÅpneFILER {
		return
	}
	entry := &åpneFilTabell[beskrivelse]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && beskrivelse > stderrfd {
		if entry.slag == fdSlagsokkel && entry.aux < makssockets {
			lokalsockets[entry.aux] = lokaldatagramsokkel{}
		}
		*entry = åpneFilBeskrivelse{}
	}
}

func lukkProsessfd(prosess *prosessentry, fd int32) int32 {
	if prosess == nil || getÅpneFilfor(prosess, fd) == nil {
		return Ebadf
	}
	beskrivelse := prosess.fds[fd].beskrivelse
	prosess.fds[fd] = fdentry{}
	releaseÅpneFil(beskrivelse)
	return 0
}

func sysSkriv(fd int32, address uint32, antall uint32) int32 {
	if antall == 0 {
		return 0
	}
	if address == 0 || address+antall < address {
		return Efault
	}
	if antall > 4096 {
		return Einval
	}
	entry := getÅpneFil(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.slag != fdSlagconsole {
		if entry.slag == fdSlagsokkel {
			return sokkelsendto(fd, address, antall, 0, 0)
		}
		if entry.slag == fdSlagfat || entry.slag == fdSlagRotKatalog {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefromPeker(uintptr(address), int(antall), int(antall))
	console_2.MSkrivut(buffer)
	return int32(antall)
}

func sysLes(fd int32, address uint32, antall uint32) int32 {
	if antall == 0 {
		return 0
	}
	if address == 0 || address+antall < address {
		return Efault
	}
	entry := getÅpneFil(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.slag == fdSlagstdin {
		return lesstdin(address, antall)
	}
	if entry.slag == fdSlagRotKatalog {
		return Eisdir
	}
	if entry.slag == fdSlagsokkel {
		return sokkelreceivefrom(fd, address, antall, 0, 0)
	}
	if entry.slag != fdSlagfat {
		return Ebadf
	}
	if entry.posisjon >= entry.størrelse {
		return 0
	}
	remaining := entry.størrelse - entry.posisjon
	if antall > remaining {
		antall = remaining
	}
	buffer := GetBytefromPeker(uintptr(address), int(antall), int(antall))
	return lesvfsFil(entry, buffer, antall)
}

func sysÅpne(sTIaddress uint32, flagg uint32, modus uint32) int32 {
	_ = modus
	if sTIaddress == 0 {
		return Efault
	}
	tilgangmodus := flagg & 3
	if tilgangmodus == oSkrivonly || tilgangmodus == oLesSkriv || (flagg&(ocreate|oAvkort|oappend)) != 0 {
		return Erofs
	}

	prosess := ensureGjeldendeProsess()
	if prosess == nil {
		return Enfile
	}
	beskrivelse := allocateÅpneFil()
	if beskrivelse < 0 {
		return beskrivelse
	}
	entry := &åpneFilTabell[beskrivelse]
	entry.flagg = flagg
	if isRotSTI(sTIaddress) {
		entry.slag = fdSlagRotKatalog
		entry.størrelse = 0
	} else {
		navnlen, navn := kopierSTI(sTIaddress)
		if navnlen == 0 {
			*entry = åpneFilBeskrivelse{}
			return Enoent
		}
		størrelse := filStørrelse(navn[:navnlen])
		if størrelse == 0 {
			*entry = åpneFilBeskrivelse{}
			return Enoent
		}
		if (flagg & oKatalog) != 0 {
			*entry = åpneFilBeskrivelse{}
			return Enotdir
		}
		entry.slag = fdSlagfat
		entry.størrelse = størrelse
		entry.navnlen = navnlen
		entry.navn = navn
	}

	fd := allocatefd(prosess, beskrivelse, 3)
	if fd < 0 {
		*entry = åpneFilBeskrivelse{}
		return fd
	}
	return fd
}

func sysLukk(fd int32) int32 {
	return lukkProsessfd(ensureGjeldendeProsess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	prosess := ensureGjeldendeProsess()
	entry := getÅpneFilfor(prosess, fd)
	if entry == nil {
		return Ebadf
	}
	nyfd := allocatefd(prosess, prosess.fds[fd].beskrivelse, minimum)
	if nyfd >= 0 {
		entry.refs++
	}
	return nyfd
}

func sysdup2(gammelfd int32, nyfd int32) int32 {
	prosess := ensureGjeldendeProsess()
	entry := getÅpneFilfor(prosess, gammelfd)
	if entry == nil {
		return Ebadf
	}
	if nyfd < 0 || nyfd >= maksfd {
		return Ebadf
	}
	if gammelfd == nyfd {
		return nyfd
	}
	if prosess.fds[nyfd].brukt {
		lukkProsessfd(prosess, nyfd)
	}
	prosess.fds[nyfd] = fdentry{brukt: true, beskrivelse: prosess.fds[gammelfd].beskrivelse}
	entry.refs++
	return nyfd
}

func sysfcntl(fd int32, kommando uint32, argument uint32) int32 {
	prosess := ensureGjeldendeProsess()
	entry := getÅpneFilfor(prosess, fd)
	if entry == nil {
		return Ebadf
	}
	switch kommando {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(prosess.fds[fd].fdFlagg)
	case fSettfd:
		prosess.fds[fd].fdFlagg = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.flagg)
	case fSettfl:
		entry.flagg = (entry.flagg & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, avstand int32, whence uint32) int32 {
	entry := getÅpneFil(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.slag != fdSlagfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekSett:
		base = 0
	case seekGjeldende:
		base = int64(entry.posisjon)
	case seekSlutt:
		base = int64(entry.størrelse)
	default:
		return Einval
	}
	posisjon_2 := base + int64(avstand)
	if posisjon_2 < 0 || posisjon_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.posisjon = uint32(posisjon_2)
	return int32(entry.posisjon)
}

func lesvfsFil(entry *åpneFilBeskrivelse, mål_2 []byte, antall uint32) int32 {
	minnemanager := &mem.TMinnemanager{}
	tmpPeker := minnemanager.Malloc(entry.størrelse)
	if tmpPeker == nil {
		return Einval
	}
	tmp := GetBytefromPeker(uintptr(tmpPeker), int(entry.størrelse), int(entry.størrelse))
	lesFil(entry.navn[:entry.navnlen], tmp)
	copy(mål_2[:antall], tmp[entry.posisjon:entry.posisjon+antall])
	entry.posisjon += antall
	minnemanager.Ledig(tmpPeker)
	return int32(antall)
}

func isRotSTI(sTIaddress uint32) bool {
	if sTIaddress == 0 {
		return false
	}
	sTI := GetBytefromPeker(uintptr(sTIaddress), 4, 4)
	if sTI[0] == '/' && sTI[1] == 0 {
		return true
	}
	if sTI[0] == '.' && sTI[1] == 0 {
		return true
	}
	if sTI[0] == '/' && sTI[1] == '.' && sTI[2] == 0 {
		return true
	}
	return false
}

func systilgang(sTIaddress uint32, modus uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if (modus & ^uint32(7)) != 0 {
		return Einval
	}
	isRot := isRotSTI(sTIaddress)
	exists := isRot
	if !exists {
		navnlen, navn := kopierSTI(sTIaddress)
		exists = navnlen != 0 && filStørrelse(navn[:navnlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (modus & 2) != 0 {
		return Eacces
	}

	if (modus&1) != 0 && !isRot {
		return Eacces
	}
	return 0
}

func syschdir(sTIaddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if !isRotSTI(sTIaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, størrelse uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if størrelse < 2 {
		return Erange
	}
	buffer_2 := GetBytefromPeker(uintptr(bufferaddress), int(størrelse), int(størrelse))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, modus uint32, størrelse uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Enhet = 1
	stat.Ino = inode
	stat.Modus = modus
	stat.Nlink = 1
	stat.Størrelse_2 = int32(størrelse)
	stat.Blksize = 512
	stat.Blokk = int32((størrelse + 511) / 512)
	return 0
}

func sysstat(sTIaddress uint32, stataddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if isRotSTI(sTIaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	navnlen, navn := kopierSTI(sTIaddress)
	if navnlen == 0 {
		return Enoent
	}
	størrelse := filStørrelse(navn[:navnlen])
	if størrelse == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < navnlen; i++ {
		inode = inode*33 + uint32(navn[i])
	}
	return fillposixstat(stataddress, sifreg|0444, størrelse, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getÅpneFil(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.slag {
	case fdSlagstdin, fdSlagconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdSlagRotKatalog:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdSlagfat:
		return fillposixstat(stataddress, sifreg|0444, entry.størrelse, uint32(fd+2))
	case fdSlagsokkel:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getÅpneFil(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	prosess := ensureGjeldendeProsess()
	if prosess == nil {
		return 0
	}
	if prosess.programbreak == 0 {
		prosess.programbreak = brukerheapbase
	}
	if address_2 == 0 {
		return prosess.programbreak
	}
	if address_2 < brukerheapbase || address_2 > brukerheapGrense {
		return prosess.programbreak
	}
	prosess.programbreak = address_2
	return prosess.programbreak
}

func kopierutsfelt(mål *[65]byte, verdi string) {
	grense := len(verdi)
	if grense > 64 {
		grense = 64
	}
	for i := 0; i < grense; i++ {
		mål[i] = verdi[i]
	}
	mål[grense] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	navn := (*posixutsname)(Pointer(uintptr(address_2)))
	*navn = posixutsname{}
	kopierutsfelt(&navn.Sysname, "EngOS")
	kopierutsfelt(&navn.Nodename, "engos")
	kopierutsfelt(&navn.Release, "0.1-posix")
	kopierutsfelt(&navn.Versjon, "POSIX.1-2017 phase 1")
	kopierutsfelt(&navn.Machine, "i386")
	return 0
}

func swapunsignedinteger16(verdi uint16) uint16 {
	return (verdi << 8) | (verdi >> 8)
}

func sokkelcallargument(argumenter_2 uint32, indeks uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenter_2 + indeks*4)))
}

func sokkelforfd(fd int32) (*lokaldatagramsokkel, int32) {
	entry := getÅpneFil(fd)
	if entry == nil || entry.slag != fdSlagsokkel || entry.aux >= makssockets {
		return nil, Ebadf
	}
	sokkel := &lokalsockets[entry.aux]
	if !sokkel.brukt {
		return nil, Ebadf
	}
	return sokkel, 0
}

func allocatesokkel(domene uint32, sokkelFiltype uint32, protocol uint32) int32 {
	if domene != afinet {
		return Eafnosupport
	}
	if sokkelFiltype != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	prosess := ensureGjeldendeProsess()
	if prosess == nil {
		return Enfile
	}
	sokkelIndeks := -1
	for i := 0; i < makssockets; i++ {
		if !lokalsockets[i].brukt {
			sokkelIndeks = i
			break
		}
	}
	if sokkelIndeks < 0 {
		return Enfile
	}
	beskrivelse := allocateÅpneFil()
	if beskrivelse < 0 {
		return beskrivelse
	}
	lokalsockets[sokkelIndeks] = lokaldatagramsokkel{brukt: true}
	entry := &åpneFilTabell[beskrivelse]
	entry.slag = fdSlagsokkel
	entry.flagg = oLesSkriv
	entry.aux = uint32(sokkelIndeks)
	fd := allocatefd(prosess, beskrivelse, 3)
	if fd < 0 {
		lokalsockets[sokkelIndeks] = lokaldatagramsokkel{}
		*entry = åpneFilBeskrivelse{}
		return fd
	}
	return fd
}

func sokkeladdress(address_2 uint32, lengde uint32) (*sokkeladdressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if lengde < 16 {
		return nil, Einval
	}
	result := (*sokkeladdressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portInnBruk(port uint16, except *lokaldatagramsokkel) bool {
	for i := 0; i < makssockets; i++ {
		sokkel := &lokalsockets[i]
		if sokkel != except && sokkel.brukt && sokkel.bound && sokkel.lokal.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(sokkel *lokaldatagramsokkel) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(nesteephemeralport)
		nesteephemeralport++
		if nesteephemeralport < 49152 {
			nesteephemeralport = 49152
		}
		if !portInnBruk(port, sokkel) {
			sokkel.lokal = sokkeladdressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			sokkel.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func sokkelbind(fd int32, address_2 uint32, lengde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := sokkeladdress(address_2, lengde)
	if err != 0 {
		return err
	}
	if sokkel.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(sokkel)
	}
	if portInnBruk(requested.Port, sokkel) {
		return Eaddrinuse
	}
	sokkel.lokal = *requested
	sokkel.bound = true
	return 0
}

func sokkelKobletil(fd int32, address_2 uint32, lengde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := sokkeladdress(address_2, lengde)
	if err != 0 {
		return err
	}
	if !sokkel.bound {
		if err := bindephemeral(sokkel); err != 0 {
			return err
		}
	}
	sokkel.remote = *remote
	sokkel.connected = true
	return 0
}

func sokkelsendto(fd int32, bufferaddress_2 uint32, lengde uint32, måladdress uint32, målLengde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if lengde > maksdatagramStørrelse {
		return Emsgsize
	}
	if lengde != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var mål sokkeladdressipv4
	if måladdress != 0 {
		address_2, addressFeil := sokkeladdress(måladdress, målLengde)
		if addressFeil != 0 {
			return addressFeil
		}
		mål = *address_2
	} else {
		if !sokkel.connected {
			return Enotconn
		}
		mål = sokkel.remote
	}
	if !sokkel.bound {
		if bindFeil := bindephemeral(sokkel); bindFeil != 0 {
			return bindFeil
		}
	}
	var receiver *lokaldatagramsokkel
	for i := 0; i < makssockets; i++ {
		candidate := &lokalsockets[i]
		if candidate.brukt && candidate.bound && candidate.lokal.Port == mål.Port &&
			(candidate.lokal.Address == 0 || candidate.lokal.Address == mål.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.antall >= makssokkelpakker {
		return Eagain
	}
	packet := &receiver.pakker[receiver.tail]
	*packet = sokkelpacket{brukt: true, størrelse: lengde, kilde: sokkel.lokal}
	if lengde != 0 {
		kilde := GetBytefromPeker(uintptr(bufferaddress_2), int(lengde), int(lengde))
		copy(packet.data[:lengde], kilde)
	}
	receiver.tail = (receiver.tail + 1) % makssokkelpakker
	receiver.antall++
	return int32(lengde)
}

func sokkelreceivefrom(fd int32, bufferaddress_2 uint32, lengde uint32, kildeaddress uint32, kildeLengdeaddress uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if lengde != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if sokkel.antall == 0 {
		return Eagain
	}
	packet := &sokkel.pakker[sokkel.head]
	kopierLengde := packet.størrelse
	if kopierLengde > lengde {
		kopierLengde = lengde
	}
	if kopierLengde != 0 {
		mål := GetBytefromPeker(uintptr(bufferaddress_2), int(kopierLengde), int(kopierLengde))
		copy(mål, packet.data[:kopierLengde])
	}
	if kildeaddress != 0 {
		if kildeLengdeaddress == 0 {
			return Efault
		}
		providedLengde := (*uint32)(Pointer(uintptr(kildeLengdeaddress)))
		if *providedLengde >= 16 {
			*(*sokkeladdressipv4)(Pointer(uintptr(kildeaddress))) = packet.kilde
		}
		*providedLengde = 16
	}
	*packet = sokkelpacket{}
	sokkel.head = (sokkel.head + 1) % makssokkelpakker
	sokkel.antall--
	return int32(kopierLengde)
}

func kopiersokkelNavn(fd int32, address_2 uint32, lengdeaddress uint32, peer bool) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || lengdeaddress == 0 {
		return Efault
	}
	lengde := (*uint32)(Pointer(uintptr(lengdeaddress)))
	if *lengde < 16 {
		*lengde = 16
		return Einval
	}
	if peer {
		if !sokkel.connected {
			return Enotconn
		}
		*(*sokkeladdressipv4)(Pointer(uintptr(address_2))) = sokkel.remote
	} else {
		if !sokkel.bound {
			if bindFeil := bindephemeral(sokkel); bindFeil != 0 {
				return bindFeil
			}
		}
		*(*sokkeladdressipv4)(Pointer(uintptr(address_2))) = sokkel.lokal
	}
	*lengde = 16
	return 0
}

func syssokkelcall(call uint32, argumenter_2 uint32) int32 {
	if argumenter_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesokkel(sokkelcallargument(argumenter_2, 0), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 2:
		return sokkelbind(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 3:
		return sokkelKobletil(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopiersokkelNavn(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), false)
	case 7:
		return kopiersokkelNavn(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), true)
	case 9:
		return sokkelsendto(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), 0, 0)
	case 10:
		return sokkelreceivefrom(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), 0, 0)
	case 11:
		return sokkelsendto(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), sokkelcallargument(argumenter_2, 4), sokkelcallargument(argumenter_2, 5))
	case 12:
		return sokkelreceivefrom(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), sokkelcallargument(argumenter_2, 4), sokkelcallargument(argumenter_2, 5))
	case 13:
		if _, err := sokkelforfd(int32(sokkelcallargument(argumenter_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := sokkelforfd(int32(sokkelcallargument(argumenter_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func lesstdin(address uint32, antall uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytefromPeker(uintptr(address), int(antall), int(antall))
	var n uint32
	for n < antall {
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
	neste := (stdinSkriv + 1) % uint32(len(stdinbuffer))
	if neste == stdinLes {
		return
	}
	stdinbuffer[stdinSkriv] = c
	stdinSkriv = neste
}

func stdingetblocking() byte {
	for stdinLes == stdinSkriv {
		sc := pollTastaturscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLes]
	stdinLes = (stdinLes + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastaturscancode() byte {
	for (PortLesbyte(0x64) & 0x01) == 0 {
	}
	sc := PortLesbyte(0x60)
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

func kopierKjørbarvector(address_2 uint32, result *kjørbarvector) int32 {
	*result = kjørbarvector{}
	if address_2 == 0 {
		return 0
	}
	for indeks := uint32(0); indeks < maksKjørbarvectorentry; indeks++ {
		strengaddress := *(*uint32)(Pointer(uintptr(address_2 + indeks*4)))
		if strengaddress == 0 {
			result.antall = indeks
			return 0
		}
		terminated := false
		for lengde := uint32(0); lengde <= maksKjørbarStrengLengde; lengde++ {
			verdi := *(*byte)(Pointer(uintptr(strengaddress + lengde)))
			result.vardier[indeks][lengde] = verdi
			if verdi == 0 {
				result.lengths[indeks] = lengde
				terminated = true
				break
			}
		}
		if !terminated {
			return E2Stor
		}
	}
	return E2Stor
}

func pushKjørbarunsignedinteger32(stack *uint32, verdi uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = verdi
}

func setupKjørbarstack(cpu *TcpuStatus, argumenter_2 *kjørbarvector, environment *kjørbarvector) int32 {
	const stackByte uint32 = 4096
	if !MakeOmrådePrivatwritable(getcr3(), BrukerstackOppe-stackByte, stackByte) {
		return Enomem
	}
	stack := BrukerstackOppe
	var argumentpointers [maksKjørbarvectorentry]uint32
	var environmentpointers [maksKjørbarvectorentry]uint32

	for i := int(environment.antall) - 1; i >= 0; i-- {
		lengde := environment.lengths[i] + 1
		stack -= lengde
		mål := GetBytefromPeker(uintptr(stack), int(lengde), int(lengde))
		copy(mål, environment.vardier[i][:lengde])
		environmentpointers[i] = stack
	}
	for i := int(argumenter_2.antall) - 1; i >= 0; i-- {
		lengde := argumenter_2.lengths[i] + 1
		stack -= lengde
		mål := GetBytefromPeker(uintptr(stack), int(lengde), int(lengde))
		copy(mål, argumenter_2.vardier[i][:lengde])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushKjørbarunsignedinteger32(&stack, 0)
	for i := int(environment.antall) - 1; i >= 0; i-- {
		pushKjørbarunsignedinteger32(&stack, environmentpointers[i])
	}
	pushKjørbarunsignedinteger32(&stack, 0)
	for i := int(argumenter_2.antall) - 1; i >= 0; i-- {
		pushKjørbarunsignedinteger32(&stack, argumentpointers[i])
	}
	pushKjørbarunsignedinteger32(&stack, argumenter_2.antall)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func lukkPåKjørbar(prosess *prosessentry) {
	if prosess == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if prosess.fds[fd].brukt && (prosess.fds[fd].fdFlagg&fdcloexec) != 0 {
			lukkProsessfd(prosess, fd)
		}
	}
}

func sysexecve(cpu *TcpuStatus, sTIaddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	var argumenter_2 kjørbarvector
	var environment kjørbarvector
	if result := kopierKjørbarvector(cpu.Ecx, &argumenter_2); result < 0 {
		return result
	}
	if result := kopierKjørbarvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	navnlen, navn := kopierSTI(sTIaddress)
	if navnlen == 0 {
		return Enoent
	}
	størrelse := filStørrelse(navn[:navnlen])
	if størrelse == 0 {
		return Enoent
	}
	minnemanager := &mem.TMinnemanager{}
	filPeker := minnemanager.Malloc(størrelse)
	if filPeker == nil {
		return Einval
	}
	data := GetBytefromPeker(uintptr(filPeker), int(størrelse), int(størrelse))
	lesFil(navn[:navnlen], data)
	if størrelse < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		minnemanager.Ledig(filPeker)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	minnemanager.Ledig(filPeker)
	if result := setupKjørbarstack(cpu, &argumenter_2, &environment); result < 0 {
		return result
	}
	lukkPåKjørbar(ensureGjeldendeProsess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStatus) int32 {
	opphavpid := Gjeldendepid()
	if ensureGjeldendeProsess() == nil {
		return Enfile
	}
	pid := allocateProsess(opphavpid)
	if pid == 0 {
		return Einval
	}
	minnemanager := &mem.TMinnemanager{}
	threadPeker := minnemanager.Malloc(uint32(Sizeof(TThread{})))
	stackPeker := minnemanager.Malloc(ThreadstackStørrelse)
	barnSideKatalog := CloneaddressMellomromcow(getcr3())
	if threadPeker == nil || stackPeker == nil || barnSideKatalog == 0 {
		forkastProsess(pid)
		return Einval
	}
	barn := (*TThread)(threadPeker)
	barn.Stack = uint32(uintptr(stackPeker))
	barn.CpuStatus = (*TcpuStatus)(Pointer(uintptr(stackPeker) + ThreadstackStørrelse - Sizeof(TcpuStatus{})))
	*barn.CpuStatus = *cpu
	barn.CpuStatus.Eax = 0
	barn.Brukerstack_2 = cpu.Esp
	barn.BrukerstackStørrelse_2 = 0
	barn.Pid = pid
	barn.Opphavpid = opphavpid
	barn.SideKatalogentry = barnSideKatalog
	barn.ThreadStatus = Klar
	barn.FpuAvstand = 0xffffffff
	barn.Iskernel = false
	Leggtilrunnablethread(barn)
	return int32(pid)
}

func sysAvslutt(status uint32) {
	pid := Gjeldendepid()
	for i := 0; i < len(prosessTabell); i++ {
		if prosessTabell[i].brukt && prosessTabell[i].pid == pid {
			lukkAlleProsessfds(&prosessTabell[i])
			prosessTabell[i].avsluttet = true
			prosessTabell[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statusaddress uint32, alternativer uint32) int32 {
	if (alternativer & ^uint32(1)) != 0 {
		return Einval
	}
	opphavpid := Gjeldendepid()
	foundbarn := false
	for i := 0; i < len(prosessTabell); i++ {
		p := &prosessTabell[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.brukt && matches && p.opphav == opphavpid {
			foundbarn = true
			if p.avsluttet {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				barnpid := p.pid
				*p = prosessentry{}
				return int32(barnpid)
			}
		}
	}
	if !foundbarn {
		return Echild
	}

	if (alternativer & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProsess(opphav uint32) uint32 {
	opphavProsess := finnProsess(opphav)
	pid := Allocatepid()
	for i := 0; i < len(prosessTabell); i++ {
		if !prosessTabell[i].brukt {
			prosessTabell[i] = prosessentry{
				brukt:		true,
				pid:		pid,
				opphav:		opphav,
				programbreak:	brukerheapbase,
			}
			if opphavProsess != nil {
				prosessTabell[i].programbreak = opphavProsess.programbreak
				for fd := 0; fd < maksfd; fd++ {
					if opphavProsess.fds[fd].brukt {
						prosessTabell[i].fds[fd] = opphavProsess.fds[fd]
						beskrivelse := opphavProsess.fds[fd].beskrivelse
						if beskrivelse >= 0 && beskrivelse < maksÅpneFILER {
							åpneFilTabell[beskrivelse].refs++
						}
					}
				}
			} else {
				initializeProsessfds(&prosessTabell[i])
			}
			return pid
		}
	}
	return 0
}

func lukkAlleProsessfds(prosess *prosessentry) {
	if prosess == nil {
		return
	}
	for fd := int32(0); fd < maksfd; fd++ {
		if prosess.fds[fd].brukt {
			lukkProsessfd(prosess, fd)
		}
	}
}

func forkastProsess(pid uint32) {
	prosess := finnProsess(pid)
	if prosess == nil {
		return
	}
	lukkAlleProsessfds(prosess)
	*prosess = prosessentry{}
}

func kopierSTI(sTIaddress uint32) (uint32, [12]byte) {
	var navn [12]byte
	if sTIaddress == 0 {
		return 0, navn
	}
	raw := GetBytefromPeker(uintptr(sTIaddress), 64, 64)
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
		navn[n] = c
		n++
	}
	return n, navn
}

func filStørrelse(filnavn []byte) uint32 {
	var ata0s = TAvansertTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Lespartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	størrelse := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	ata0s.Flush()
	return størrelse
}

func lesFil(filnavn []byte, data []byte) {
	var ata0s = TAvansertTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabell{}
	partition.Lespartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Les(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)
	ata0s.Flush()
}

func getcr3() uint32
