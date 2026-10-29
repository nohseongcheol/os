/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package systemcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "filsystem/msdospartition"
import . "filsystem/fat"
import . "filsystem/elf"
import mem "hukommelsemanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuelHukommelse"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysAfslut	uint32	= 1
	Sysfork		uint32	= 2
	SysLæse		uint32	= 3
	SysSkrive	uint32	= 4
	SysÅbn		uint32	= 5
	SysLuk		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Systilgå	uint32	= 33
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
	SysrtAfslut	uint32	= 252

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
	maxfd			= 32
	maxÅbnFILER		= 128
)

type fdemne struct {
	brugt		bool
	beskrivelse	int32
	fdFlag		uint32
}

type åbnFilBeskrivelse struct {
	brugt		bool
	refs		uint32
	typeVærdi	uint32
	flag		uint32
	placering	uint32
	størrelse	uint32
	navn		[12]byte
	navnlen		uint32
	aux		uint32
}

const (
	fdTypeIngen	uint32	= 0
	fdTypefat	uint32	= 1
	fdTypestdin	uint32	= 2
	fdTypeconsole	uint32	= 3
	fdTypeRodMappe	uint32	= 4
	fdTypeSokkel	uint32	= 5

	oLæseonly	uint32	= 0
	oSkriveonly	uint32	= 1
	oLæseSkrive	uint32	= 2
	ocreate		uint32	= 0x40
	oTrunker	uint32	= 0x200
	oappend		uint32	= 0x400
	oMappe		uint32	= 0x10000

	seeksat		uint32	= 0
	seekAktive	uint32	= 1
	seekSlutningen	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fsatfd		uint32	= 2
	fgetfl		uint32	= 3
	fsatfl		uint32	= 4
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
	maxSokkelpakker		= 8
	maxdatagramStørrelse	= 512
)

type sokkeladdressiNv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type sokkelpacket struct {
	brugt		bool
	størrelse	uint32
	kilde		sokkeladdressiNv4
	data		[maxdatagramStørrelse]byte
}

type lokaldatagramSokkel struct {
	brugt		bool
	bound		bool
	connected	bool
	lokal		sokkeladdressiNv4
	ekstern		sokkeladdressiNv4
	head		uint32
	tail		uint32
	antal		uint32
	pakker		[maxSokkelpakker]sokkelpacket
}

type posixstat struct {
	Enhed		uint32
	Ino		uint32
	Tilstand	uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Størrelse_2	int32
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
	Version		[65]byte
	Machine		[65]byte
}

const (
	maxexecvectoremne	= 16
	maxexecStrengLængde	= 63
)

type execvector struct {
	antal	uint32
	lengths	[maxexecvectoremne]uint32
	værdier	[maxexecvectoremne][maxexecStrengLængde + 1]byte
}

type procesemne struct {
	brugt		bool
	pid		uint32
	forælder	uint32
	afsluttet	bool
	status		uint32
	programbreak	uint32
	fds		[maxfd]fdemne
}

type strengheader struct {
	Data	uintptr
	Len	int
}

func syscallFejl(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var åbnFilTabel [maxÅbnFILER]åbnFilBeskrivelse
var procesTabel [32]procesemne
var lokalsockets [maxsockets]lokaldatagramSokkel
var næsteephemeralport uint16 = 49152

const (
	brugerheapbase	uint32	= 0x06000000
	brugerheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLæse uint32
var stdinSkrive uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysAfslut_2(indeks uint32) {
	Syscall(SysAfslut, indeks)
}

func SysLæse_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLæse, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysUdskrivstr(buffer string) {
	h := (*strengheader)(Pointer(&buffer))
	Syscall(SysSkrive, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysUdskrivunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSkrive, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysÅbn_2(sTI uintptr, flag uint32, tilstand uint32) int32 {
	return int32(Syscall(SysÅbn, uint32(sTI), flag, tilstand))
}

func SysLuk_2(fd uint32) int32 {
	return int32(Syscall(SysLuk, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(paramer ...uint32) uint32 {

	l := len(paramer)
	switch l {
	case 1:
		return Interrupt(paramer[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(paramer[0], paramer[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(paramer[0], paramer[1], paramer[2], 0, 0, 0)
	case 4:
		return Interrupt(paramer[0], paramer[1], paramer[2], paramer[3], 0, 0)
	case 5:
		return Interrupt(paramer[0], paramer[1], paramer[2], paramer[3], paramer[4], 0)
	case 6:
		return Interrupt(paramer[0], paramer[1], paramer[2], paramer[3], paramer[4], paramer[5])
	default:
		return syscallFejl(Enosys)
	}
}

func (selv *TSyscall) Init(manager *TInterruptmanager) {
	initFildescriptor()

	interrupthandler = håndtaginterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	selv.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func håndtaginterrupt(esp uint32) uint32 {
	var cpu = (*TcpuStatus)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysAfslut:
		sysAfslut(cpu.Ebx)
		return uint32(uintptr(Pointer(StopAktivethread(cpu))))
	case SysrtAfslut:
		sysAfslut(cpu.Ebx)
		return uint32(uintptr(Pointer(StopAktivethread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLæse:
		cpu.Eax = uint32(sysLæse(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSkrive:
		cpu.Eax = uint32(sysSkrive(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysÅbn:
		cpu.Eax = uint32(sysÅbn(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysÅbn(cpu.Ebx, ocreate|oSkriveonly|oTrunker, cpu.Ecx))
		return esp
	case SysLuk:
		cpu.Eax = uint32(sysLuk(int32(cpu.Ebx)))
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
		cpu.Eax = Aktivepid()
		return esp
	case Sysgetppid:
		cpu.Eax = Aktiveforælderpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Systilgå:
		cpu.Eax = uint32(systilgå(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysSokkelcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Udskriv(cpu.Ebx)
		return esp

	default:
		console_2.MUdskrivxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Udskriv(esp)
		console_2.MUdskriv(([]byte)(":"))
		console_2.MUnsignedinteger32Udskriv(cpu.Eax)
		console_2.MUdskriv(([]byte)(":"))
		console_2.MUnsignedinteger32Udskriv(cpu.Ebx)
		console_2.MUdskriv(([]byte)(":"))
		console_2.MUnsignedinteger32Udskriv(cpu.Ecx)
		console_2.MUdskriv(([]byte)(":"))
		console_2.MUnsignedinteger32Udskriv(cpu.Edx)
		console_2.MUdskriv(([]byte)("]"))
		cpu.Eax = syscallFejl(Enosys)
		return esp
	}

	return esp
}

func initFildescriptor() {
	for i := 0; i < maxÅbnFILER; i++ {
		åbnFilTabel[i] = åbnFilBeskrivelse{}
	}
	for i := 0; i < len(procesTabel); i++ {
		procesTabel[i] = procesemne{}
	}
	for i := 0; i < len(lokalsockets); i++ {
		lokalsockets[i] = lokaldatagramSokkel{}
	}
	næsteephemeralport = 49152
	åbnFilTabel[0] = åbnFilBeskrivelse{brugt: true, typeVærdi: fdTypestdin, flag: oLæseonly}
	åbnFilTabel[1] = åbnFilBeskrivelse{brugt: true, typeVærdi: fdTypeconsole, flag: oSkriveonly}
	åbnFilTabel[2] = åbnFilBeskrivelse{brugt: true, typeVærdi: fdTypeconsole, flag: oSkriveonly}
}

func søgProces(pid uint32) *procesemne {
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].brugt && procesTabel[i].pid == pid {
			return &procesTabel[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesemne) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		proces.fds[fd] = fdemne{brugt: true, beskrivelse: fd}
		åbnFilTabel[fd].refs++
	}
}

func ensureAktiveProces() *procesemne {
	pid := Aktivepid()
	if proces := søgProces(pid); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].brugt {
			procesTabel[i] = procesemne{
				brugt:		true,
				pid:		pid,
				forælder:	Aktiveforælderpid(),
				programbreak:	brugerheapbase,
			}
			initializeProcesfds(&procesTabel[i])
			return &procesTabel[i]
		}
	}
	return nil
}

func getÅbnFilfor(proces *procesemne, fd int32) *åbnFilBeskrivelse {
	if proces == nil || fd < 0 || fd >= maxfd || !proces.fds[fd].brugt {
		return nil
	}
	beskrivelse := proces.fds[fd].beskrivelse
	if beskrivelse < 0 || beskrivelse >= maxÅbnFILER || !åbnFilTabel[beskrivelse].brugt {
		return nil
	}
	return &åbnFilTabel[beskrivelse]
}

func getÅbnFil(fd int32) *åbnFilBeskrivelse {
	return getÅbnFilfor(ensureAktiveProces(), fd)
}

func allocateÅbnFil() int32 {
	for i := int32(3); i < maxÅbnFILER; i++ {
		if !åbnFilTabel[i].brugt {
			åbnFilTabel[i] = åbnFilBeskrivelse{brugt: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(proces *procesemne, beskrivelse int32, minimum int32) int32 {
	if proces == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !proces.fds[fd].brugt {
			proces.fds[fd] = fdemne{brugt: true, beskrivelse: beskrivelse}
			return fd
		}
	}
	return Emfile
}

func releaseÅbnFil(beskrivelse int32) {
	if beskrivelse < 0 || beskrivelse >= maxÅbnFILER {
		return
	}
	emne := &åbnFilTabel[beskrivelse]
	if emne.refs > 0 {
		emne.refs--
	}

	if emne.refs == 0 && beskrivelse > stderrfd {
		if emne.typeVærdi == fdTypeSokkel && emne.aux < maxsockets {
			lokalsockets[emne.aux] = lokaldatagramSokkel{}
		}
		*emne = åbnFilBeskrivelse{}
	}
}

func lukProcesfd(proces *procesemne, fd int32) int32 {
	if proces == nil || getÅbnFilfor(proces, fd) == nil {
		return Ebadf
	}
	beskrivelse := proces.fds[fd].beskrivelse
	proces.fds[fd] = fdemne{}
	releaseÅbnFil(beskrivelse)
	return 0
}

func sysSkrive(fd int32, address uint32, antal uint32) int32 {
	if antal == 0 {
		return 0
	}
	if address == 0 || address+antal < address {
		return Efault
	}
	if antal > 4096 {
		return Einval
	}
	emne := getÅbnFil(fd)
	if emne == nil {
		return Ebadf
	}
	if emne.typeVærdi != fdTypeconsole {
		if emne.typeVærdi == fdTypeSokkel {
			return sokkelsendto(fd, address, antal, 0, 0)
		}
		if emne.typeVærdi == fdTypefat || emne.typeVærdi == fdTypeRodMappe {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBytefraMarkør(uintptr(address), int(antal), int(antal))
	console_2.MUdskriv(buffer)
	return int32(antal)
}

func sysLæse(fd int32, address uint32, antal uint32) int32 {
	if antal == 0 {
		return 0
	}
	if address == 0 || address+antal < address {
		return Efault
	}
	emne := getÅbnFil(fd)
	if emne == nil {
		return Ebadf
	}
	if emne.typeVærdi == fdTypestdin {
		return læsestdin(address, antal)
	}
	if emne.typeVærdi == fdTypeRodMappe {
		return Eisdir
	}
	if emne.typeVærdi == fdTypeSokkel {
		return sokkelreceivefra(fd, address, antal, 0, 0)
	}
	if emne.typeVærdi != fdTypefat {
		return Ebadf
	}
	if emne.placering >= emne.størrelse {
		return 0
	}
	remaining := emne.størrelse - emne.placering
	if antal > remaining {
		antal = remaining
	}
	buffer := GetBytefraMarkør(uintptr(address), int(antal), int(antal))
	return læsevfsFil(emne, buffer, antal)
}

func sysÅbn(sTIaddress uint32, flag uint32, tilstand uint32) int32 {
	_ = tilstand
	if sTIaddress == 0 {
		return Efault
	}
	tilgåtilstand := flag & 3
	if tilgåtilstand == oSkriveonly || tilgåtilstand == oLæseSkrive || (flag&(ocreate|oTrunker|oappend)) != 0 {
		return Erofs
	}

	proces := ensureAktiveProces()
	if proces == nil {
		return Enfile
	}
	beskrivelse := allocateÅbnFil()
	if beskrivelse < 0 {
		return beskrivelse
	}
	emne := &åbnFilTabel[beskrivelse]
	emne.flag = flag
	if isRodSTI(sTIaddress) {
		emne.typeVærdi = fdTypeRodMappe
		emne.størrelse = 0
	} else {
		navnlen, navn := kopiérSTI(sTIaddress)
		if navnlen == 0 {
			*emne = åbnFilBeskrivelse{}
			return Enoent
		}
		størrelse := filStørrelse(navn[:navnlen])
		if størrelse == 0 {
			*emne = åbnFilBeskrivelse{}
			return Enoent
		}
		if (flag & oMappe) != 0 {
			*emne = åbnFilBeskrivelse{}
			return Enotdir
		}
		emne.typeVærdi = fdTypefat
		emne.størrelse = størrelse
		emne.navnlen = navnlen
		emne.navn = navn
	}

	fd := allocatefd(proces, beskrivelse, 3)
	if fd < 0 {
		*emne = åbnFilBeskrivelse{}
		return fd
	}
	return fd
}

func sysLuk(fd int32) int32 {
	return lukProcesfd(ensureAktiveProces(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	proces := ensureAktiveProces()
	emne := getÅbnFilfor(proces, fd)
	if emne == nil {
		return Ebadf
	}
	nyfd := allocatefd(proces, proces.fds[fd].beskrivelse, minimum)
	if nyfd >= 0 {
		emne.refs++
	}
	return nyfd
}

func sysdup2(gammelfd int32, nyfd int32) int32 {
	proces := ensureAktiveProces()
	emne := getÅbnFilfor(proces, gammelfd)
	if emne == nil {
		return Ebadf
	}
	if nyfd < 0 || nyfd >= maxfd {
		return Ebadf
	}
	if gammelfd == nyfd {
		return nyfd
	}
	if proces.fds[nyfd].brugt {
		lukProcesfd(proces, nyfd)
	}
	proces.fds[nyfd] = fdemne{brugt: true, beskrivelse: proces.fds[gammelfd].beskrivelse}
	emne.refs++
	return nyfd
}

func sysfcntl(fd int32, kommando uint32, argument uint32) int32 {
	proces := ensureAktiveProces()
	emne := getÅbnFilfor(proces, fd)
	if emne == nil {
		return Ebadf
	}
	switch kommando {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(proces.fds[fd].fdFlag)
	case fsatfd:
		proces.fds[fd].fdFlag = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(emne.flag)
	case fsatfl:
		emne.flag = (emne.flag & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, forskydning int32, whence uint32) int32 {
	emne := getÅbnFil(fd)
	if emne == nil {
		return Ebadf
	}
	if emne.typeVærdi != fdTypefat {
		return Espipe
	}
	var base int64
	switch whence {
	case seeksat:
		base = 0
	case seekAktive:
		base = int64(emne.placering)
	case seekSlutningen:
		base = int64(emne.størrelse)
	default:
		return Einval
	}
	placering_2 := base + int64(forskydning)
	if placering_2 < 0 || placering_2 > 0x7FFFFFFF {
		return Einval
	}
	emne.placering = uint32(placering_2)
	return int32(emne.placering)
}

func læsevfsFil(emne *åbnFilBeskrivelse, destination_2 []byte, antal uint32) int32 {
	hukommelsemanager := &mem.THukommelsemanager{}
	tmpMarkør := hukommelsemanager.Malloc(emne.størrelse)
	if tmpMarkør == nil {
		return Einval
	}
	tmp := GetBytefraMarkør(uintptr(tmpMarkør), int(emne.størrelse), int(emne.størrelse))
	læseFil(emne.navn[:emne.navnlen], tmp)
	copy(destination_2[:antal], tmp[emne.placering:emne.placering+antal])
	emne.placering += antal
	hukommelsemanager.Fri(tmpMarkør)
	return int32(antal)
}

func isRodSTI(sTIaddress uint32) bool {
	if sTIaddress == 0 {
		return false
	}
	sTI := GetBytefraMarkør(uintptr(sTIaddress), 4, 4)
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

func systilgå(sTIaddress uint32, tilstand uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if (tilstand & ^uint32(7)) != 0 {
		return Einval
	}
	isRod := isRodSTI(sTIaddress)
	exists := isRod
	if !exists {
		navnlen, navn := kopiérSTI(sTIaddress)
		exists = navnlen != 0 && filStørrelse(navn[:navnlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (tilstand & 2) != 0 {
		return Eacces
	}

	if (tilstand&1) != 0 && !isRod {
		return Eacces
	}
	return 0
}

func syschdir(sTIaddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if !isRodSTI(sTIaddress) {
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
	buffer_2 := GetBytefraMarkør(uintptr(bufferaddress), int(størrelse), int(størrelse))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, tilstand uint32, størrelse uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Enhed = 1
	stat.Ino = inode
	stat.Tilstand = tilstand
	stat.Nlink = 1
	stat.Størrelse_2 = int32(størrelse)
	stat.Blksize = 512
	stat.Blok = int32((størrelse + 511) / 512)
	return 0
}

func sysstat(sTIaddress uint32, stataddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	if isRodSTI(sTIaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	navnlen, navn := kopiérSTI(sTIaddress)
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
	emne := getÅbnFil(fd)
	if emne == nil {
		return Ebadf
	}
	switch emne.typeVærdi {
	case fdTypestdin, fdTypeconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdTypeRodMappe:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdTypefat:
		return fillposixstat(stataddress, sifreg|0444, emne.størrelse, uint32(fd+2))
	case fdTypeSokkel:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getÅbnFil(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureAktiveProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = brugerheapbase
	}
	if address_2 == 0 {
		return proces.programbreak
	}
	if address_2 < brugerheapbase || address_2 > brugerheaplimit {
		return proces.programbreak
	}
	proces.programbreak = address_2
	return proces.programbreak
}

func kopiérutsfelt(destination *[65]byte, værdi string) {
	limit := len(værdi)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = værdi[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	navn := (*posixutsname)(Pointer(uintptr(address_2)))
	*navn = posixutsname{}
	kopiérutsfelt(&navn.Sysname, "EngOS")
	kopiérutsfelt(&navn.Nodename, "engos")
	kopiérutsfelt(&navn.Release, "0.1-posix")
	kopiérutsfelt(&navn.Version, "POSIX.1-2017 phase 1")
	kopiérutsfelt(&navn.Machine, "i386")
	return 0
}

func swapunsignedinteger16(værdi uint16) uint16 {
	return (værdi << 8) | (værdi >> 8)
}

func sokkelcallargument(argumenter_2 uint32, indeks uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenter_2 + indeks*4)))
}

func sokkelforfd(fd int32) (*lokaldatagramSokkel, int32) {
	emne := getÅbnFil(fd)
	if emne == nil || emne.typeVærdi != fdTypeSokkel || emne.aux >= maxsockets {
		return nil, Ebadf
	}
	sokkel := &lokalsockets[emne.aux]
	if !sokkel.brugt {
		return nil, Ebadf
	}
	return sokkel, 0
}

func allocateSokkel(domæne uint32, sokkeltype uint32, protocol uint32) int32 {
	if domæne != afinet {
		return Eafnosupport
	}
	if sokkeltype != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureAktiveProces()
	if proces == nil {
		return Enfile
	}
	sokkelIndeks := -1
	for i := 0; i < maxsockets; i++ {
		if !lokalsockets[i].brugt {
			sokkelIndeks = i
			break
		}
	}
	if sokkelIndeks < 0 {
		return Enfile
	}
	beskrivelse := allocateÅbnFil()
	if beskrivelse < 0 {
		return beskrivelse
	}
	lokalsockets[sokkelIndeks] = lokaldatagramSokkel{brugt: true}
	emne := &åbnFilTabel[beskrivelse]
	emne.typeVærdi = fdTypeSokkel
	emne.flag = oLæseSkrive
	emne.aux = uint32(sokkelIndeks)
	fd := allocatefd(proces, beskrivelse, 3)
	if fd < 0 {
		lokalsockets[sokkelIndeks] = lokaldatagramSokkel{}
		*emne = åbnFilBeskrivelse{}
		return fd
	}
	return fd
}

func sokkeladdress(address_2 uint32, længde uint32) (*sokkeladdressiNv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if længde < 16 {
		return nil, Einval
	}
	result := (*sokkeladdressiNv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portIndBrug(port uint16, except *lokaldatagramSokkel) bool {
	for i := 0; i < maxsockets; i++ {
		sokkel := &lokalsockets[i]
		if sokkel != except && sokkel.brugt && sokkel.bound && sokkel.lokal.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(sokkel *lokaldatagramSokkel) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(næsteephemeralport)
		næsteephemeralport++
		if næsteephemeralport < 49152 {
			næsteephemeralport = 49152
		}
		if !portIndBrug(port, sokkel) {
			sokkel.lokal = sokkeladdressiNv4{Family: afinet, Port: port, Address: 0x0100007F}
			sokkel.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func sokkelbind(fd int32, address_2 uint32, længde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := sokkeladdress(address_2, længde)
	if err != 0 {
		return err
	}
	if sokkel.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(sokkel)
	}
	if portIndBrug(requested.Port, sokkel) {
		return Eaddrinuse
	}
	sokkel.lokal = *requested
	sokkel.bound = true
	return 0
}

func sokkelTilslut(fd int32, address_2 uint32, længde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	ekstern, err := sokkeladdress(address_2, længde)
	if err != 0 {
		return err
	}
	if !sokkel.bound {
		if err := bindephemeral(sokkel); err != 0 {
			return err
		}
	}
	sokkel.ekstern = *ekstern
	sokkel.connected = true
	return 0
}

func sokkelsendto(fd int32, bufferaddress_2 uint32, længde uint32, destinationaddress uint32, destinationLængde uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if længde > maxdatagramStørrelse {
		return Emsgsize
	}
	if længde != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination sokkeladdressiNv4
	if destinationaddress != 0 {
		address_2, addressFejl := sokkeladdress(destinationaddress, destinationLængde)
		if addressFejl != 0 {
			return addressFejl
		}
		destination = *address_2
	} else {
		if !sokkel.connected {
			return Enotconn
		}
		destination = sokkel.ekstern
	}
	if !sokkel.bound {
		if bindFejl := bindephemeral(sokkel); bindFejl != 0 {
			return bindFejl
		}
	}
	var receiver *lokaldatagramSokkel
	for i := 0; i < maxsockets; i++ {
		candidate := &lokalsockets[i]
		if candidate.brugt && candidate.bound && candidate.lokal.Port == destination.Port &&
			(candidate.lokal.Address == 0 || candidate.lokal.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.antal >= maxSokkelpakker {
		return Eagain
	}
	packet := &receiver.pakker[receiver.tail]
	*packet = sokkelpacket{brugt: true, størrelse: længde, kilde: sokkel.lokal}
	if længde != 0 {
		kilde := GetBytefraMarkør(uintptr(bufferaddress_2), int(længde), int(længde))
		copy(packet.data[:længde], kilde)
	}
	receiver.tail = (receiver.tail + 1) % maxSokkelpakker
	receiver.antal++
	return int32(længde)
}

func sokkelreceivefra(fd int32, bufferaddress_2 uint32, længde uint32, kildeaddress uint32, kildeLængdeaddress uint32) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if længde != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if sokkel.antal == 0 {
		return Eagain
	}
	packet := &sokkel.pakker[sokkel.head]
	kopiérLængde := packet.størrelse
	if kopiérLængde > længde {
		kopiérLængde = længde
	}
	if kopiérLængde != 0 {
		destination := GetBytefraMarkør(uintptr(bufferaddress_2), int(kopiérLængde), int(kopiérLængde))
		copy(destination, packet.data[:kopiérLængde])
	}
	if kildeaddress != 0 {
		if kildeLængdeaddress == 0 {
			return Efault
		}
		providedLængde := (*uint32)(Pointer(uintptr(kildeLængdeaddress)))
		if *providedLængde >= 16 {
			*(*sokkeladdressiNv4)(Pointer(uintptr(kildeaddress))) = packet.kilde
		}
		*providedLængde = 16
	}
	*packet = sokkelpacket{}
	sokkel.head = (sokkel.head + 1) % maxSokkelpakker
	sokkel.antal--
	return int32(kopiérLængde)
}

func kopiérSokkelNavn(fd int32, address_2 uint32, længdeaddress uint32, peer bool) int32 {
	sokkel, err := sokkelforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || længdeaddress == 0 {
		return Efault
	}
	længde := (*uint32)(Pointer(uintptr(længdeaddress)))
	if *længde < 16 {
		*længde = 16
		return Einval
	}
	if peer {
		if !sokkel.connected {
			return Enotconn
		}
		*(*sokkeladdressiNv4)(Pointer(uintptr(address_2))) = sokkel.ekstern
	} else {
		if !sokkel.bound {
			if bindFejl := bindephemeral(sokkel); bindFejl != 0 {
				return bindFejl
			}
		}
		*(*sokkeladdressiNv4)(Pointer(uintptr(address_2))) = sokkel.lokal
	}
	*længde = 16
	return 0
}

func sysSokkelcall(call uint32, argumenter_2 uint32) int32 {
	if argumenter_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSokkel(sokkelcallargument(argumenter_2, 0), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 2:
		return sokkelbind(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 3:
		return sokkelTilslut(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return kopiérSokkelNavn(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), false)
	case 7:
		return kopiérSokkelNavn(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), true)
	case 9:
		return sokkelsendto(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), 0, 0)
	case 10:
		return sokkelreceivefra(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), 0, 0)
	case 11:
		return sokkelsendto(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), sokkelcallargument(argumenter_2, 4), sokkelcallargument(argumenter_2, 5))
	case 12:
		return sokkelreceivefra(int32(sokkelcallargument(argumenter_2, 0)), sokkelcallargument(argumenter_2, 1), sokkelcallargument(argumenter_2, 2), sokkelcallargument(argumenter_2, 4), sokkelcallargument(argumenter_2, 5))
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

func læsestdin(address uint32, antal uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBytefraMarkør(uintptr(address), int(antal), int(antal))
	var n uint32
	for n < antal {
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
	næste := (stdinSkrive + 1) % uint32(len(stdinbuffer))
	if næste == stdinLæse {
		return
	}
	stdinbuffer[stdinSkrive] = c
	stdinSkrive = næste
}

func stdingetblocking() byte {
	for stdinLæse == stdinSkrive {
		sc := pollTastaturscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLæse]
	stdinLæse = (stdinLæse + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastaturscancode() byte {
	for (PortLæsebyte(0x64) & 0x01) == 0 {
	}
	sc := PortLæsebyte(0x60)
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

func kopiérexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for indeks := uint32(0); indeks < maxexecvectoremne; indeks++ {
		strengaddress := *(*uint32)(Pointer(uintptr(address_2 + indeks*4)))
		if strengaddress == 0 {
			result.antal = indeks
			return 0
		}
		terminated := false
		for længde := uint32(0); længde <= maxexecStrengLængde; længde++ {
			værdi := *(*byte)(Pointer(uintptr(strengaddress + længde)))
			result.værdier[indeks][længde] = værdi
			if værdi == 0 {
				result.lengths[indeks] = længde
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

func pushexecunsignedinteger32(stack *uint32, værdi uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = værdi
}

func setupexecstack(cpu *TcpuStatus, argumenter_2 *execvector, environment *execvector) int32 {
	const stackByte uint32 = 4096
	if !MakeIntervalPrivatwritable(getcr3(), BrugerstackØverst-stackByte, stackByte) {
		return Enomem
	}
	stack := BrugerstackØverst
	var argumentpointers [maxexecvectoremne]uint32
	var environmentpointers [maxexecvectoremne]uint32

	for i := int(environment.antal) - 1; i >= 0; i-- {
		længde := environment.lengths[i] + 1
		stack -= længde
		destination := GetBytefraMarkør(uintptr(stack), int(længde), int(længde))
		copy(destination, environment.værdier[i][:længde])
		environmentpointers[i] = stack
	}
	for i := int(argumenter_2.antal) - 1; i >= 0; i-- {
		længde := argumenter_2.lengths[i] + 1
		stack -= længde
		destination := GetBytefraMarkør(uintptr(stack), int(længde), int(længde))
		copy(destination, argumenter_2.værdier[i][:længde])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushexecunsignedinteger32(&stack, 0)
	for i := int(environment.antal) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, environmentpointers[i])
	}
	pushexecunsignedinteger32(&stack, 0)
	for i := int(argumenter_2.antal) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, argumentpointers[i])
	}
	pushexecunsignedinteger32(&stack, argumenter_2.antal)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func luktændtexec(proces *procesemne) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].brugt && (proces.fds[fd].fdFlag&fdcloexec) != 0 {
			lukProcesfd(proces, fd)
		}
	}
}

func sysexecve(cpu *TcpuStatus, sTIaddress uint32) int32 {
	if sTIaddress == 0 {
		return Efault
	}
	var argumenter_2 execvector
	var environment execvector
	if result := kopiérexecvector(cpu.Ecx, &argumenter_2); result < 0 {
		return result
	}
	if result := kopiérexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	navnlen, navn := kopiérSTI(sTIaddress)
	if navnlen == 0 {
		return Enoent
	}
	størrelse := filStørrelse(navn[:navnlen])
	if størrelse == 0 {
		return Enoent
	}
	hukommelsemanager := &mem.THukommelsemanager{}
	filMarkør := hukommelsemanager.Malloc(størrelse)
	if filMarkør == nil {
		return Einval
	}
	data := GetBytefraMarkør(uintptr(filMarkør), int(størrelse), int(størrelse))
	læseFil(navn[:navnlen], data)
	if størrelse < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		hukommelsemanager.Fri(filMarkør)
		return Enoexec
	}
	loader := Elf{}
	emne := loader.Getemne(data)
	loader.Parse(data, getcr3())
	hukommelsemanager.Fri(filMarkør)
	if result := setupexecstack(cpu, &argumenter_2, &environment); result < 0 {
		return result
	}
	luktændtexec(ensureAktiveProces())
	cpu.Eip = emne
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStatus) int32 {
	forælderpid := Aktivepid()
	if ensureAktiveProces() == nil {
		return Enfile
	}
	pid := allocateProces(forælderpid)
	if pid == 0 {
		return Einval
	}
	hukommelsemanager := &mem.THukommelsemanager{}
	threadMarkør := hukommelsemanager.Malloc(uint32(Sizeof(TThread{})))
	stackMarkør := hukommelsemanager.Malloc(ThreadstackStørrelse)
	barnSideMappe := CloneaddressMellemrumcow(getcr3())
	if threadMarkør == nil || stackMarkør == nil || barnSideMappe == 0 {
		kassérProces(pid)
		return Einval
	}
	barn := (*TThread)(threadMarkør)
	barn.Stack = uint32(uintptr(stackMarkør))
	barn.CpuStatus = (*TcpuStatus)(Pointer(uintptr(stackMarkør) + ThreadstackStørrelse - Sizeof(TcpuStatus{})))
	*barn.CpuStatus = *cpu
	barn.CpuStatus.Eax = 0
	barn.Brugerstack_2 = cpu.Esp
	barn.BrugerstackStørrelse_2 = 0
	barn.Pid = pid
	barn.Forælderpid = forælderpid
	barn.SideMappeemne = barnSideMappe
	barn.ThreadStatus = Klar
	barn.FpuForskydning = 0xffffffff
	barn.Iskernel = false
	Tilføjrunnablethread(barn)
	return int32(pid)
}

func sysAfslut(status uint32) {
	pid := Aktivepid()
	for i := 0; i < len(procesTabel); i++ {
		if procesTabel[i].brugt && procesTabel[i].pid == pid {
			lukAlleProcesfds(&procesTabel[i])
			procesTabel[i].afsluttet = true
			procesTabel[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statusaddress uint32, indstillinger uint32) int32 {
	if (indstillinger & ^uint32(1)) != 0 {
		return Einval
	}
	forælderpid := Aktivepid()
	foundbarn := false
	for i := 0; i < len(procesTabel); i++ {
		p := &procesTabel[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.brugt && matches && p.forælder == forælderpid {
			foundbarn = true
			if p.afsluttet {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				barnpid := p.pid
				*p = procesemne{}
				return int32(barnpid)
			}
		}
	}
	if !foundbarn {
		return Echild
	}

	if (indstillinger & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(forælder uint32) uint32 {
	forælderProces := søgProces(forælder)
	pid := Allocatepid()
	for i := 0; i < len(procesTabel); i++ {
		if !procesTabel[i].brugt {
			procesTabel[i] = procesemne{
				brugt:		true,
				pid:		pid,
				forælder:	forælder,
				programbreak:	brugerheapbase,
			}
			if forælderProces != nil {
				procesTabel[i].programbreak = forælderProces.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if forælderProces.fds[fd].brugt {
						procesTabel[i].fds[fd] = forælderProces.fds[fd]
						beskrivelse := forælderProces.fds[fd].beskrivelse
						if beskrivelse >= 0 && beskrivelse < maxÅbnFILER {
							åbnFilTabel[beskrivelse].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabel[i])
			}
			return pid
		}
	}
	return 0
}

func lukAlleProcesfds(proces *procesemne) {
	if proces == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if proces.fds[fd].brugt {
			lukProcesfd(proces, fd)
		}
	}
}

func kassérProces(pid uint32) {
	proces := søgProces(pid)
	if proces == nil {
		return
	}
	lukAlleProcesfds(proces)
	*proces = procesemne{}
}

func kopiérSTI(sTIaddress uint32) (uint32, [12]byte) {
	var navn [12]byte
	if sTIaddress == 0 {
		return 0, navn
	}
	raw := GetBytefraMarkør(uintptr(sTIaddress), 64, 64)
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
	var ata0s = TAvanceretTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Læsepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	størrelse := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filnavn)
	ata0s.Flush()
	return størrelse
}

func læseFil(filnavn []byte, data []byte) {
	var ata0s = TAvanceretTeknologiattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabel{}
	partition.Læsepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Læse(&ata0s, partition.Mbr.Primarypartition[0], filnavn, data)
	ata0s.Flush()
}

func getcr3() uint32
