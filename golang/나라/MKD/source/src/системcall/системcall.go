package системcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "датотекаСистем/fat"
import . "датотекаСистем/elf"
import mem "меморијаmanager"
import . "paging"
import . "порта"
import . "tasking/scheduler"
import . "tasking/thread"
import . "виртуелноМеморија"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysИзлез	uint32	= 1
	Sysfork		uint32	= 2
	SysЧитај	uint32	= 3
	SysЗапиши	uint32	= 4
	SysОтвори	uint32	= 5
	SysЗатвори	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysпристап	uint32	= 33
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
	SysrtИзлез	uint32	= 252

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
	stdinfd		int32	= 0
	stdoutfd	int32	= 1
	stderrfd	int32	= 2
	maxfd			= 32
	maxОтвориfiles		= 128
)

type fdentry struct {
	искористено	bool
	опис		int32
	fdАтрибути	uint32
}

type отвориДатотекаОпис struct {
	искористено	bool
	refs		uint32
	kind		uint32
	атрибути	uint32
	позиција	uint32
	големина	uint32
	име		[12]byte
	имеlen		uint32
	aux		uint32
}

const (
	fdkindНишто		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindКоренДиректориум	uint32	= 4
	fdkindsocket		uint32	= 5

	oЧитајonly	uint32	= 0
	oЗапишиonly	uint32	= 1
	oЧитајЗапиши	uint32	= 2
	ocreate		uint32	= 0x40
	oСкрати		uint32	= 0x200
	oappend		uint32	= 0x400
	oДиректориум	uint32	= 0x10000

	seekпостави	uint32	= 0
	seekcurrent	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fпоставиfd	uint32	= 2
	fgetfl		uint32	= 3
	fпоставиfl	uint32	= 4
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
	maxsocketpackets	= 8
	maxdatagramГолемина	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Порта	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	искористено	bool
	големина	uint32
	извор		socketaddressipv4
	data		[maxdatagramГолемина]byte
}

type localdatagramsocket struct {
	искористено	bool
	bound		bool
	connected	bool
	local		socketaddressipv4
	remote		socketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Уред		uint32
	Ino		uint32
	Режим		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Големина_2	int32
	Blksize		int32
	Block		int32
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
	maxИзвршнаvectorentry	= 16
	maxИзвршнаstringДолжина	= 63
)

type извршнаvector struct {
	count	uint32
	lengths	[maxИзвршнаvectorentry]uint32
	values	[maxИзвршнаvectorentry][maxИзвршнаstringДолжина + 1]byte
}

type процесentry struct {
	искористено	bool
	pid		uint32
	parent		uint32
	exited		bool
	статус		uint32
	програмаbreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallГрешка(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var отвориДатотекаТабела [maxОтвориfiles]отвориДатотекаОпис
var процесТабела [32]процесentry
var localsockets [maxsockets]localdatagramsocket
var следнаephemeralПорта uint16 = 49152

const (
	корисникheapbase	uint32	= 0x06000000
	корисникheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinЧитај uint32
var stdinЗапиши uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysИзлез_2(индекс uint32) {
	Syscall(SysИзлез, индекс)
}

func SysЧитај_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysЧитај, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysПечатиstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(SysЗапиши, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysПечатиunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysЗапиши, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysОтвори_2(пАТЕКА uintptr, атрибути uint32, режим uint32) int32 {
	return int32(Syscall(SysОтвори, uint32(пАТЕКА), атрибути, режим))
}

func SysЗатвори_2(fd uint32) int32 {
	return int32(Syscall(SysЗатвори, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(params ...uint32) uint32 {

	l := len(params)
	switch l {
	case 1:
		return Interrupt(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Interrupt(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallГрешка(Enosys)
	}
}

func (само *TSyscall) Init(manager *TInterruptmanager) {
	initДатотекаdescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	само.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysИзлез:
		sysИзлез(cpu.Ebx)
		return uint32(uintptr(Pointer(Стопcurrentthread(cpu))))
	case SysrtИзлез:
		sysИзлез(cpu.Ebx)
		return uint32(uintptr(Pointer(Стопcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysЧитај:
		cpu.Eax = uint32(sysЧитај(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysЗапиши:
		cpu.Eax = uint32(sysЗапиши(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysОтвори:
		cpu.Eax = uint32(sysОтвори(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysОтвори(cpu.Ebx, ocreate|oЗапишиonly|oСкрати, cpu.Ecx))
		return esp
	case SysЗатвори:
		cpu.Eax = uint32(sysЗатвори(int32(cpu.Ebx)))
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
		cpu.Eax = Currentpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Currentparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysпристап:
		cpu.Eax = uint32(sysпристап(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Печати(cpu.Ebx)
		return esp

	default:
		console_2.MПечатиxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Печати(esp)
		console_2.MПечати(([]byte)(":"))
		console_2.MUnsignedinteger32Печати(cpu.Eax)
		console_2.MПечати(([]byte)(":"))
		console_2.MUnsignedinteger32Печати(cpu.Ebx)
		console_2.MПечати(([]byte)(":"))
		console_2.MUnsignedinteger32Печати(cpu.Ecx)
		console_2.MПечати(([]byte)(":"))
		console_2.MUnsignedinteger32Печати(cpu.Edx)
		console_2.MПечати(([]byte)("]"))
		cpu.Eax = syscallГрешка(Enosys)
		return esp
	}

	return esp
}

func initДатотекаdescriptor() {
	for i := 0; i < maxОтвориfiles; i++ {
		отвориДатотекаТабела[i] = отвориДатотекаОпис{}
	}
	for i := 0; i < len(процесТабела); i++ {
		процесТабела[i] = процесentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	следнаephemeralПорта = 49152
	отвориДатотекаТабела[0] = отвориДатотекаОпис{искористено: true, kind: fdkindstdin, атрибути: oЧитајonly}
	отвориДатотекаТабела[1] = отвориДатотекаОпис{искористено: true, kind: fdkindconsole, атрибути: oЗапишиonly}
	отвориДатотекаТабела[2] = отвориДатотекаОпис{искористено: true, kind: fdkindconsole, атрибути: oЗапишиonly}
}

func пронајдиПроцес(pid uint32) *процесentry {
	for i := 0; i < len(процесТабела); i++ {
		if процесТабела[i].искористено && процесТабела[i].pid == pid {
			return &процесТабела[i]
		}
	}
	return nil
}

func initializeПроцесfds(процес *процесentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		процес.fds[fd] = fdentry{искористено: true, опис: fd}
		отвориДатотекаТабела[fd].refs++
	}
}

func ensurecurrentПроцес() *процесentry {
	pid := Currentpid()
	if процес := пронајдиПроцес(pid); процес != nil {
		return процес
	}
	for i := 0; i < len(процесТабела); i++ {
		if !процесТабела[i].искористено {
			процесТабела[i] = процесentry{
				искористено:	true,
				pid:		pid,
				parent:		Currentparentpid(),
				програмаbreak:	корисникheapbase,
			}
			initializeПроцесfds(&процесТабела[i])
			return &процесТабела[i]
		}
	}
	return nil
}

func getОтвориДатотекаfor(процес *процесentry, fd int32) *отвориДатотекаОпис {
	if процес == nil || fd < 0 || fd >= maxfd || !процес.fds[fd].искористено {
		return nil
	}
	опис := процес.fds[fd].опис
	if опис < 0 || опис >= maxОтвориfiles || !отвориДатотекаТабела[опис].искористено {
		return nil
	}
	return &отвориДатотекаТабела[опис]
}

func getОтвориДатотека(fd int32) *отвориДатотекаОпис {
	return getОтвориДатотекаfor(ensurecurrentПроцес(), fd)
}

func allocateОтвориДатотека() int32 {
	for i := int32(3); i < maxОтвориfiles; i++ {
		if !отвориДатотекаТабела[i].искористено {
			отвориДатотекаТабела[i] = отвориДатотекаОпис{искористено: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(процес *процесentry, опис int32, minimum int32) int32 {
	if процес == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !процес.fds[fd].искористено {
			процес.fds[fd] = fdentry{искористено: true, опис: опис}
			return fd
		}
	}
	return Emfile
}

func releaseОтвориДатотека(опис int32) {
	if опис < 0 || опис >= maxОтвориfiles {
		return
	}
	entry := &отвориДатотекаТабела[опис]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && опис > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = отвориДатотекаОпис{}
	}
}

func затвориПроцесfd(процес *процесentry, fd int32) int32 {
	if процес == nil || getОтвориДатотекаfor(процес, fd) == nil {
		return Ebadf
	}
	опис := процес.fds[fd].опис
	процес.fds[fd] = fdentry{}
	releaseОтвориДатотека(опис)
	return 0
}

func sysЗапиши(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getОтвориДатотека(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketИспратиto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindКоренДиректориум {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetбајтиfromСтрелка(uintptr(address), int(count), int(count))
	console_2.MПечати(buffer)
	return int32(count)
}

func sysЧитај(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getОтвориДатотека(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return читајstdin(address, count)
	}
	if entry.kind == fdkindКоренДиректориум {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.позиција >= entry.големина {
		return 0
	}
	remaining := entry.големина - entry.позиција
	if count > remaining {
		count = remaining
	}
	buffer := GetбајтиfromСтрелка(uintptr(address), int(count), int(count))
	return читајvfsДатотека(entry, buffer, count)
}

func sysОтвори(пАТЕКАaddress uint32, атрибути uint32, режим uint32) int32 {
	_ = режим
	if пАТЕКАaddress == 0 {
		return Efault
	}
	пристапРежим := атрибути & 3
	if пристапРежим == oЗапишиonly || пристапРежим == oЧитајЗапиши || (атрибути&(ocreate|oСкрати|oappend)) != 0 {
		return Erofs
	}

	процес := ensurecurrentПроцес()
	if процес == nil {
		return Enfile
	}
	опис := allocateОтвориДатотека()
	if опис < 0 {
		return опис
	}
	entry := &отвориДатотекаТабела[опис]
	entry.атрибути = атрибути
	if isКоренПАТЕКА(пАТЕКАaddress) {
		entry.kind = fdkindКоренДиректориум
		entry.големина = 0
	} else {
		имеlen, име := копирајПАТЕКА(пАТЕКАaddress)
		if имеlen == 0 {
			*entry = отвориДатотекаОпис{}
			return Enoent
		}
		големина := датотекаГолемина(име[:имеlen])
		if големина == 0 {
			*entry = отвориДатотекаОпис{}
			return Enoent
		}
		if (атрибути & oДиректориум) != 0 {
			*entry = отвориДатотекаОпис{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.големина = големина
		entry.имеlen = имеlen
		entry.име = име
	}

	fd := allocatefd(процес, опис, 3)
	if fd < 0 {
		*entry = отвориДатотекаОпис{}
		return fd
	}
	return fd
}

func sysЗатвори(fd int32) int32 {
	return затвориПроцесfd(ensurecurrentПроцес(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	процес := ensurecurrentПроцес()
	entry := getОтвориДатотекаfor(процес, fd)
	if entry == nil {
		return Ebadf
	}
	новfd := allocatefd(процес, процес.fds[fd].опис, minimum)
	if новfd >= 0 {
		entry.refs++
	}
	return новfd
}

func sysdup2(oldfd int32, новfd int32) int32 {
	процес := ensurecurrentПроцес()
	entry := getОтвориДатотекаfor(процес, oldfd)
	if entry == nil {
		return Ebadf
	}
	if новfd < 0 || новfd >= maxfd {
		return Ebadf
	}
	if oldfd == новfd {
		return новfd
	}
	if процес.fds[новfd].искористено {
		затвориПроцесfd(процес, новfd)
	}
	процес.fds[новfd] = fdentry{искористено: true, опис: процес.fds[oldfd].опис}
	entry.refs++
	return новfd
}

func sysfcntl(fd int32, команда uint32, argument uint32) int32 {
	процес := ensurecurrentПроцес()
	entry := getОтвориДатотекаfor(процес, fd)
	if entry == nil {
		return Ebadf
	}
	switch команда {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(процес.fds[fd].fdАтрибути)
	case fпоставиfd:
		процес.fds[fd].fdАтрибути = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.атрибути)
	case fпоставиfl:
		entry.атрибути = (entry.атрибути & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getОтвориДатотека(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekпостави:
		base = 0
	case seekcurrent:
		base = int64(entry.позиција)
	case seekend:
		base = int64(entry.големина)
	default:
		return Einval
	}
	позиција_2 := base + int64(offset)
	if позиција_2 < 0 || позиција_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.позиција = uint32(позиција_2)
	return int32(entry.позиција)
}

func читајvfsДатотека(entry *отвориДатотекаОпис, одредиште_2 []byte, count uint32) int32 {
	меморијаmanager := &mem.TМеморијаmanager{}
	tmpСтрелка := меморијаmanager.Malloc(entry.големина)
	if tmpСтрелка == nil {
		return Einval
	}
	tmp := GetбајтиfromСтрелка(uintptr(tmpСтрелка), int(entry.големина), int(entry.големина))
	читајДатотека(entry.име[:entry.имеlen], tmp)
	copy(одредиште_2[:count], tmp[entry.позиција:entry.позиција+count])
	entry.позиција += count
	меморијаmanager.Слободни(tmpСтрелка)
	return int32(count)
}

func isКоренПАТЕКА(пАТЕКАaddress uint32) bool {
	if пАТЕКАaddress == 0 {
		return false
	}
	пАТЕКА := GetбајтиfromСтрелка(uintptr(пАТЕКАaddress), 4, 4)
	if пАТЕКА[0] == '/' && пАТЕКА[1] == 0 {
		return true
	}
	if пАТЕКА[0] == '.' && пАТЕКА[1] == 0 {
		return true
	}
	if пАТЕКА[0] == '/' && пАТЕКА[1] == '.' && пАТЕКА[2] == 0 {
		return true
	}
	return false
}

func sysпристап(пАТЕКАaddress uint32, режим uint32) int32 {
	if пАТЕКАaddress == 0 {
		return Efault
	}
	if (режим & ^uint32(7)) != 0 {
		return Einval
	}
	isКорен := isКоренПАТЕКА(пАТЕКАaddress)
	exists := isКорен
	if !exists {
		имеlen, име := копирајПАТЕКА(пАТЕКАaddress)
		exists = имеlen != 0 && датотекаГолемина(име[:имеlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (режим & 2) != 0 {
		return Eacces
	}

	if (режим&1) != 0 && !isКорен {
		return Eacces
	}
	return 0
}

func syschdir(пАТЕКАaddress uint32) int32 {
	if пАТЕКАaddress == 0 {
		return Efault
	}
	if !isКоренПАТЕКА(пАТЕКАaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, големина uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if големина < 2 {
		return Erange
	}
	buffer_2 := GetбајтиfromСтрелка(uintptr(bufferaddress), int(големина), int(големина))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, режим uint32, големина uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Уред = 1
	stat.Ino = inode
	stat.Режим = режим
	stat.Nlink = 1
	stat.Големина_2 = int32(големина)
	stat.Blksize = 512
	stat.Block = int32((големина + 511) / 512)
	return 0
}

func sysstat(пАТЕКАaddress uint32, stataddress uint32) int32 {
	if пАТЕКАaddress == 0 {
		return Efault
	}
	if isКоренПАТЕКА(пАТЕКАaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	имеlen, име := копирајПАТЕКА(пАТЕКАaddress)
	if имеlen == 0 {
		return Enoent
	}
	големина := датотекаГолемина(име[:имеlen])
	if големина == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < имеlen; i++ {
		inode = inode*33 + uint32(име[i])
	}
	return fillposixstat(stataddress, sifreg|0444, големина, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getОтвориДатотека(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindКоренДиректориум:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.големина, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getОтвориДатотека(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	процес := ensurecurrentПроцес()
	if процес == nil {
		return 0
	}
	if процес.програмаbreak == 0 {
		процес.програмаbreak = корисникheapbase
	}
	if address_2 == 0 {
		return процес.програмаbreak
	}
	if address_2 < корисникheapbase || address_2 > корисникheaplimit {
		return процес.програмаbreak
	}
	процес.програмаbreak = address_2
	return процес.програмаbreak
}

func копирајutsfield(одредиште *[65]byte, вредност string) {
	limit := len(вредност)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		одредиште[i] = вредност[i]
	}
	одредиште[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	име := (*posixutsname)(Pointer(uintptr(address_2)))
	*име = posixutsname{}
	копирајutsfield(&име.Sysname, "EngOS")
	копирајutsfield(&име.Nodename, "engos")
	копирајutsfield(&име.Release, "0.1-posix")
	копирајutsfield(&име.Version, "POSIX.1-2017 phase 1")
	копирајutsfield(&име.Machine, "i386")
	return 0
}

func swapunsignedinteger16(вредност uint16) uint16 {
	return (вредност << 8) | (вредност >> 8)
}

func socketcallargument(аргументи_2 uint32, индекс uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(аргументи_2 + индекс*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getОтвориДатотека(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.искористено {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(домен uint32, socketТип uint32, protocol uint32) int32 {
	if домен != afinet {
		return Eafnosupport
	}
	if socketТип != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процес := ensurecurrentПроцес()
	if процес == nil {
		return Enfile
	}
	socketИндекс := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].искористено {
			socketИндекс = i
			break
		}
	}
	if socketИндекс < 0 {
		return Enfile
	}
	опис := allocateОтвориДатотека()
	if опис < 0 {
		return опис
	}
	localsockets[socketИндекс] = localdatagramsocket{искористено: true}
	entry := &отвориДатотекаТабела[опис]
	entry.kind = fdkindsocket
	entry.атрибути = oЧитајЗапиши
	entry.aux = uint32(socketИндекс)
	fd := allocatefd(процес, опис, 3)
	if fd < 0 {
		localsockets[socketИндекс] = localdatagramsocket{}
		*entry = отвориДатотекаОпис{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, должина uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if должина < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func портавоuse(порта uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.искористено && socket.bound && socket.local.Порта == порта {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порта := swapunsignedinteger16(следнаephemeralПорта)
		следнаephemeralПорта++
		if следнаephemeralПорта < 49152 {
			следнаephemeralПорта = 49152
		}
		if !портавоuse(порта, socket) {
			socket.local = socketaddressipv4{Family: afinet, Порта: порта, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, должина uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, должина)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Порта == 0 {
		return bindephemeral(socket)
	}
	if портавоuse(requested.Порта, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketВрзисе(fd int32, address_2 uint32, должина uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, должина)
	if err != 0 {
		return err
	}
	if !socket.bound {
		if err := bindephemeral(socket); err != 0 {
			return err
		}
	}
	socket.remote = *remote
	socket.connected = true
	return 0
}

func socketИспратиto(fd int32, bufferaddress_2 uint32, должина uint32, одредиштеaddress uint32, одредиштеДолжина uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if должина > maxdatagramГолемина {
		return Emsgsize
	}
	if должина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var одредиште socketaddressipv4
	if одредиштеaddress != 0 {
		address_2, addressГрешка := socketaddress(одредиштеaddress, одредиштеДолжина)
		if addressГрешка != 0 {
			return addressГрешка
		}
		одредиште = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		одредиште = socket.remote
	}
	if !socket.bound {
		if bindГрешка := bindephemeral(socket); bindГрешка != 0 {
			return bindГрешка
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.искористено && candidate.bound && candidate.local.Порта == одредиште.Порта &&
			(candidate.local.Address == 0 || candidate.local.Address == одредиште.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxsocketpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = socketpacket{искористено: true, големина: должина, извор: socket.local}
	if должина != 0 {
		извор := GetбајтиfromСтрелка(uintptr(bufferaddress_2), int(должина), int(должина))
		copy(packet.data[:должина], извор)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(должина)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, должина uint32, изворaddress uint32, изворДолжинаaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if должина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	копирајДолжина := packet.големина
	if копирајДолжина > должина {
		копирајДолжина = должина
	}
	if копирајДолжина != 0 {
		одредиште := GetбајтиfromСтрелка(uintptr(bufferaddress_2), int(копирајДолжина), int(копирајДолжина))
		copy(одредиште, packet.data[:копирајДолжина])
	}
	if изворaddress != 0 {
		if изворДолжинаaddress == 0 {
			return Efault
		}
		providedДолжина := (*uint32)(Pointer(uintptr(изворДолжинаaddress)))
		if *providedДолжина >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(изворaddress))) = packet.извор
		}
		*providedДолжина = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(копирајДолжина)
}

func копирајsocketИме(fd int32, address_2 uint32, должинаaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || должинаaddress == 0 {
		return Efault
	}
	должина := (*uint32)(Pointer(uintptr(должинаaddress)))
	if *должина < 16 {
		*должина = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindГрешка := bindephemeral(socket); bindГрешка != 0 {
				return bindГрешка
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*должина = 16
	return 0
}

func syssocketcall(call uint32, аргументи_2 uint32) int32 {
	if аргументи_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(аргументи_2, 0), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2))
	case 3:
		return socketВрзисе(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return копирајsocketИме(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), false)
	case 7:
		return копирајsocketИме(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), true)
	case 9:
		return socketИспратиto(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), 0, 0)
	case 11:
		return socketИспратиto(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), socketcallargument(аргументи_2, 4), socketcallargument(аргументи_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(аргументи_2, 0)), socketcallargument(аргументи_2, 1), socketcallargument(аргументи_2, 2), socketcallargument(аргументи_2, 4), socketcallargument(аргументи_2, 5))
	case 13:
		if _, err := socketforfd(int32(socketcallargument(аргументи_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketforfd(int32(socketcallargument(аргументи_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func читајstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetбајтиfromСтрелка(uintptr(address), int(count), int(count))
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
	следна := (stdinЗапиши + 1) % uint32(len(stdinbuffer))
	if следна == stdinЧитај {
		return
	}
	stdinbuffer[stdinЗапиши] = c
	stdinЗапиши = следна
}

func stdingetblocking() byte {
	for stdinЧитај == stdinЗапиши {
		sc := pollТастатураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinЧитај]
	stdinЧитај = (stdinЧитај + 1) % uint32(len(stdinbuffer))
	return c
}

func pollТастатураscancode() byte {
	for (ПортаЧитајbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортаЧитајbyte(0x60)
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

func копирајИзвршнаvector(address_2 uint32, result *извршнаvector) int32 {
	*result = извршнаvector{}
	if address_2 == 0 {
		return 0
	}
	for индекс := uint32(0); индекс < maxИзвршнаvectorentry; индекс++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + индекс*4)))
		if stringaddress == 0 {
			result.count = индекс
			return 0
		}
		terminated := false
		for должина := uint32(0); должина <= maxИзвршнаstringДолжина; должина++ {
			вредност := *(*byte)(Pointer(uintptr(stringaddress + должина)))
			result.values[индекс][должина] = вредност
			if вредност == 0 {
				result.lengths[индекс] = должина
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

func pushИзвршнаunsignedinteger32(stack *uint32, вредност uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = вредност
}

func setupИзвршнаstack(cpu *Tcpustate, аргументи_2 *извршнаvector, environment *извршнаvector) int32 {
	const stackбајти uint32 = 4096
	if !MakeОпсегПриватноwritable(getcr3(), КорисникstackГоре-stackбајти, stackбајти) {
		return Enomem
	}
	stack := КорисникstackГоре
	var argumentpointers [maxИзвршнаvectorentry]uint32
	var environmentpointers [maxИзвршнаvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		должина := environment.lengths[i] + 1
		stack -= должина
		одредиште := GetбајтиfromСтрелка(uintptr(stack), int(должина), int(должина))
		copy(одредиште, environment.values[i][:должина])
		environmentpointers[i] = stack
	}
	for i := int(аргументи_2.count) - 1; i >= 0; i-- {
		должина := аргументи_2.lengths[i] + 1
		stack -= должина
		одредиште := GetбајтиfromСтрелка(uintptr(stack), int(должина), int(должина))
		copy(одредиште, аргументи_2.values[i][:должина])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushИзвршнаunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushИзвршнаunsignedinteger32(&stack, environmentpointers[i])
	}
	pushИзвршнаunsignedinteger32(&stack, 0)
	for i := int(аргументи_2.count) - 1; i >= 0; i-- {
		pushИзвршнаunsignedinteger32(&stack, argumentpointers[i])
	}
	pushИзвршнаunsignedinteger32(&stack, аргументи_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func затвориВклученоИзвршна(процес *процесentry) {
	if процес == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if процес.fds[fd].искористено && (процес.fds[fd].fdАтрибути&fdcloexec) != 0 {
			затвориПроцесfd(процес, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, пАТЕКАaddress uint32) int32 {
	if пАТЕКАaddress == 0 {
		return Efault
	}
	var аргументи_2 извршнаvector
	var environment извршнаvector
	if result := копирајИзвршнаvector(cpu.Ecx, &аргументи_2); result < 0 {
		return result
	}
	if result := копирајИзвршнаvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	имеlen, име := копирајПАТЕКА(пАТЕКАaddress)
	if имеlen == 0 {
		return Enoent
	}
	големина := датотекаГолемина(име[:имеlen])
	if големина == 0 {
		return Enoent
	}
	меморијаmanager := &mem.TМеморијаmanager{}
	датотекаСтрелка := меморијаmanager.Malloc(големина)
	if датотекаСтрелка == nil {
		return Einval
	}
	data := GetбајтиfromСтрелка(uintptr(датотекаСтрелка), int(големина), int(големина))
	читајДатотека(име[:имеlen], data)
	if големина < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		меморијаmanager.Слободни(датотекаСтрелка)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	меморијаmanager.Слободни(датотекаСтрелка)
	if result := setupИзвршнаstack(cpu, &аргументи_2, &environment); result < 0 {
		return result
	}
	затвориВклученоИзвршна(ensurecurrentПроцес())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
	parentpid := Currentpid()
	if ensurecurrentПроцес() == nil {
		return Enfile
	}
	pid := allocateПроцес(parentpid)
	if pid == 0 {
		return Einval
	}
	меморијаmanager := &mem.TМеморијаmanager{}
	threadСтрелка := меморијаmanager.Malloc(uint32(Sizeof(TThread{})))
	stackСтрелка := меморијаmanager.Malloc(ThreadstackГолемина)
	детеСтраницаДиректориум := Cloneaddressspacecow(getcr3())
	if threadСтрелка == nil || stackСтрелка == nil || детеСтраницаДиректориум == 0 {
		discardПроцес(pid)
		return Einval
	}
	дете := (*TThread)(threadСтрелка)
	дете.Stack = uint32(uintptr(stackСтрелка))
	дете.Cpustate = (*Tcpustate)(Pointer(uintptr(stackСтрелка) + ThreadstackГолемина - Sizeof(Tcpustate{})))
	*дете.Cpustate = *cpu
	дете.Cpustate.Eax = 0
	дете.Корисникstack_2 = cpu.Esp
	дете.КорисникstackГолемина_2 = 0
	дете.Pid = pid
	дете.Parentpid = parentpid
	дете.СтраницаДиректориумentry = детеСтраницаДиректориум
	дете.Threadstate = Подготвено
	дете.Fpuoffset = 0xffffffff
	дете.Iskernel = false
	Додајrunnablethread(дете)
	return int32(pid)
}

func sysИзлез(статус uint32) {
	pid := Currentpid()
	for i := 0; i < len(процесТабела); i++ {
		if процесТабела[i].искористено && процесТабела[i].pid == pid {
			затвориСѐПроцесfds(&процесТабела[i])
			процесТабела[i].exited = true
			процесТабела[i].статус = (статус & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, статусaddress uint32, опции uint32) int32 {
	if (опции & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundдете := false
	for i := 0; i < len(процесТабела); i++ {
		p := &процесТабела[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.искористено && matches && p.parent == parentpid {
			foundдете = true
			if p.exited {
				if статусaddress != 0 {
					*(*uint32)(Pointer(uintptr(статусaddress))) = p.статус
				}
				детеpid := p.pid
				*p = процесentry{}
				return int32(детеpid)
			}
		}
	}
	if !foundдете {
		return Echild
	}

	if (опции & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцес(parent uint32) uint32 {
	parentПроцес := пронајдиПроцес(parent)
	pid := Allocatepid()
	for i := 0; i < len(процесТабела); i++ {
		if !процесТабела[i].искористено {
			процесТабела[i] = процесentry{
				искористено:	true,
				pid:		pid,
				parent:		parent,
				програмаbreak:	корисникheapbase,
			}
			if parentПроцес != nil {
				процесТабела[i].програмаbreak = parentПроцес.програмаbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentПроцес.fds[fd].искористено {
						процесТабела[i].fds[fd] = parentПроцес.fds[fd]
						опис := parentПроцес.fds[fd].опис
						if опис >= 0 && опис < maxОтвориfiles {
							отвориДатотекаТабела[опис].refs++
						}
					}
				}
			} else {
				initializeПроцесfds(&процесТабела[i])
			}
			return pid
		}
	}
	return 0
}

func затвориСѐПроцесfds(процес *процесentry) {
	if процес == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if процес.fds[fd].искористено {
			затвориПроцесfd(процес, fd)
		}
	}
}

func discardПроцес(pid uint32) {
	процес := пронајдиПроцес(pid)
	if процес == nil {
		return
	}
	затвориСѐПроцесfds(процес)
	*процес = процесentry{}
}

func копирајПАТЕКА(пАТЕКАaddress uint32) (uint32, [12]byte) {
	var име [12]byte
	if пАТЕКАaddress == 0 {
		return 0, име
	}
	raw := GetбајтиfromСтрелка(uintptr(пАТЕКАaddress), 64, 64)
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
		име[n] = c
		n++
	}
	return n, име
}

func датотекаГолемина(именадатотека []byte) uint32 {
	var ata0s = TНапредноtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читајpartition(&ata0s)

	bios := TBiosparameterblock32{}
	големина := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именадатотека)
	ata0s.Flush()
	return големина
}

func читајДатотека(именадатотека []byte, data []byte) {
	var ata0s = TНапредноtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читајpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Читај(&ata0s, partition.Mbr.Primarypartition[0], именадатотека, data)
	ata0s.Flush()
}

func getcr3() uint32
