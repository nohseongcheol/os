package системаcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"
import . "файлСистема/elf"
import mem "эсиmanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualЭси"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	SysОкуу		uint32	= 3
	SysЖазуу	uint32	= 4
	SysАчуу		uint32	= 5
	SysЖабуу	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysкирүү	uint32	= 33
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
	Sysrtexit	uint32	= 252

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
	maxАчууfiles		= 128
)

type fdentry struct {
	колдонулганы	bool
	баяндамасы	int32
	fdЖелектери	uint32
}

type ачууФайлБаяндамасы struct {
	колдонулганы	bool
	refs		uint32
	kind		uint32
	желектери	uint32
	турганжери	uint32
	өлчөм		uint32
	аты		[12]byte
	атыlen		uint32
	aux		uint32
}

const (
	fdkindЖок		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindТамыркаталог	uint32	= 4
	fdkindsocket		uint32	= 5

	oОкууonly	uint32	= 0
	oЖазууonly	uint32	= 1
	oОкууЖазуу	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oкаталог	uint32	= 0x10000

	seekset		uint32	= 0
	seekcurrent	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fsetfd		uint32	= 2
	fgetfl		uint32	= 3
	fsetfl		uint32	= 4
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
	maxdatagramӨлчөм	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	колдонулганы	bool
	өлчөм		uint32
	баштапкытекст	socketaddressipv4
	data		[maxdatagramӨлчөм]byte
}

type localdatagramsocket struct {
	колдонулганы	bool
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
	Түзүлүшү	uint32
	Ino		uint32
	Режим		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Өлчөм_2		int32
	Blksize		int32
	Блок		int32
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
	maxexecvectorentry	= 16
	maxexecСАПУзундук	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecСАПУзундук + 1]byte
}

type процессиentry struct {
	колдонулганы	bool
	pid		uint32
	атаэне		uint32
	exited		bool
	абалы		uint32
	программаbreak	uint32
	fds		[maxfd]fdentry
}

type сАПheader struct {
	Data	uintptr
	Len	int
}

func syscallКата(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var ачууФайлЖадыбал [maxАчууfiles]ачууФайлБаяндамасы
var процессиЖадыбал [32]процессиentry
var localsockets [maxsockets]localdatagramsocket
var кийинкиephemeralПорт uint16 = 49152

const (
	колдонуучуheapbase	uint32	= 0x06000000
	колдонуучуheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinОкуу uint32
var stdinЖазуу uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(мазмун uint32) {
	Syscall(Sysexit, мазмун)
}

func SysОкуу_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysОкуу, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysБасмаstr(buffer string) {
	h := (*сАПheader)(Pointer(&buffer))
	Syscall(SysЖазуу, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysБасмаunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysЖазуу, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysАчуу_2(жОЛ uintptr, желектери uint32, режим uint32) int32 {
	return int32(Syscall(SysАчуу, uint32(жОЛ), желектери, режим))
}

func SysЖабуу_2(fd uint32) int32 {
	return int32(Syscall(SysЖабуу, fd))
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
		return syscallКата(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initФайлdescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var бП = (*TcpuАбал)(Pointer(uintptr(esp)))

	switch бП.Eax {
	case Sysexit:
		sysexit(бП.Ebx)
		return uint32(uintptr(Pointer(Токтотууcurrentthread(бП))))
	case Sysrtexit:
		sysexit(бП.Ebx)
		return uint32(uintptr(Pointer(Токтотууcurrentthread(бП))))
	case Sysfork:
		бП.Eax = uint32(sysfork(бП))
		return esp
	case SysОкуу:
		бП.Eax = uint32(sysОкуу(int32(бП.Ebx), бП.Ecx, бП.Edx))
		return esp
	case SysЖазуу:
		бП.Eax = uint32(sysЖазуу(int32(бП.Ebx), бП.Ecx, бП.Edx))
		return esp
	case SysАчуу:
		бП.Eax = uint32(sysАчуу(бП.Ebx, бП.Ecx, бП.Edx))
		return esp
	case Syscreat:
		бП.Eax = uint32(sysАчуу(бП.Ebx, ocreate|oЖазууonly|otruncate, бП.Ecx))
		return esp
	case SysЖабуу:
		бП.Eax = uint32(sysЖабуу(int32(бП.Ebx)))
		return esp
	case Syswaitpid:
		бП.Eax = uint32(syswaitpid(int32(бП.Ebx), бП.Ecx, бП.Edx))
		return esp
	case Syslseek:
		бП.Eax = uint32(syslseek(int32(бП.Ebx), int32(бП.Ecx), бП.Edx))
		return esp
	case Sysexecve:
		бП.Eax = uint32(sysexecve(бП, бП.Ebx))
		return esp
	case Sysgetpid:
		бП.Eax = Currentpid()
		return esp
	case Sysgetppid:
		бП.Eax = Currentатаэнеpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		бП.Eax = 0
		return esp
	case Sysкирүү:
		бП.Eax = uint32(sysкирүү(бП.Ebx, бП.Ecx))
		return esp
	case Syschdir:
		бП.Eax = uint32(syschdir(бП.Ebx))
		return esp
	case Sysgetcwd:
		бП.Eax = uint32(sysgetcwd(бП.Ebx, бП.Ecx))
		return esp
	case Sysdup:
		бП.Eax = uint32(sysdup(int32(бП.Ebx), 0))
		return esp
	case Sysdup2:
		бП.Eax = uint32(sysdup2(int32(бП.Ebx), int32(бП.Ecx)))
		return esp
	case Syssocketcall:
		бП.Eax = uint32(syssocketcall(бП.Ebx, бП.Ecx))
		return esp
	case Sysfcntl:
		бП.Eax = uint32(sysfcntl(int32(бП.Ebx), бП.Ecx, бП.Edx))
		return esp
	case Sysstat, Syslstat:
		бП.Eax = uint32(sysstat(бП.Ebx, бП.Ecx))
		return esp
	case Sysfstat:
		бП.Eax = uint32(sysfstat(int32(бП.Ebx), бП.Ecx))
		return esp
	case Sysfsync:
		бП.Eax = uint32(sysfsync(int32(бП.Ebx)))
		return esp
	case Syssync:
		бП.Eax = 0
		return esp
	case Sysuname:
		бП.Eax = uint32(sysuname(бП.Ebx))
		return esp
	case Sysbrk:
		бП.Eax = sysbrk(бП.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Басма(бП.Ebx)
		return esp

	default:
		console_2.MБасмаxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Басма(esp)
		console_2.MБасма(([]byte)(":"))
		console_2.MUnsignedinteger32Басма(бП.Eax)
		console_2.MБасма(([]byte)(":"))
		console_2.MUnsignedinteger32Басма(бП.Ebx)
		console_2.MБасма(([]byte)(":"))
		console_2.MUnsignedinteger32Басма(бП.Ecx)
		console_2.MБасма(([]byte)(":"))
		console_2.MUnsignedinteger32Басма(бП.Edx)
		console_2.MБасма(([]byte)("]"))
		бП.Eax = syscallКата(Enosys)
		return esp
	}

	return esp
}

func initФайлdescriptor() {
	for i := 0; i < maxАчууfiles; i++ {
		ачууФайлЖадыбал[i] = ачууФайлБаяндамасы{}
	}
	for i := 0; i < len(процессиЖадыбал); i++ {
		процессиЖадыбал[i] = процессиentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	кийинкиephemeralПорт = 49152
	ачууФайлЖадыбал[0] = ачууФайлБаяндамасы{колдонулганы: true, kind: fdkindstdin, желектери: oОкууonly}
	ачууФайлЖадыбал[1] = ачууФайлБаяндамасы{колдонулганы: true, kind: fdkindconsole, желектери: oЖазууonly}
	ачууФайлЖадыбал[2] = ачууФайлБаяндамасы{колдонулганы: true, kind: fdkindconsole, желектери: oЖазууonly}
}

func табууПроцесси(pid uint32) *процессиentry {
	for i := 0; i < len(процессиЖадыбал); i++ {
		if процессиЖадыбал[i].колдонулганы && процессиЖадыбал[i].pid == pid {
			return &процессиЖадыбал[i]
		}
	}
	return nil
}

func initializeПроцессиfds(процесси *процессиentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		процесси.fds[fd] = fdentry{колдонулганы: true, баяндамасы: fd}
		ачууФайлЖадыбал[fd].refs++
	}
}

func ensurecurrentПроцесси() *процессиentry {
	pid := Currentpid()
	if процесси := табууПроцесси(pid); процесси != nil {
		return процесси
	}
	for i := 0; i < len(процессиЖадыбал); i++ {
		if !процессиЖадыбал[i].колдонулганы {
			процессиЖадыбал[i] = процессиentry{
				колдонулганы:	true,
				pid:		pid,
				атаэне:		Currentатаэнеpid(),
				программаbreak:	колдонуучуheapbase,
			}
			initializeПроцессиfds(&процессиЖадыбал[i])
			return &процессиЖадыбал[i]
		}
	}
	return nil
}

func getАчууФайлfor(процесси *процессиentry, fd int32) *ачууФайлБаяндамасы {
	if процесси == nil || fd < 0 || fd >= maxfd || !процесси.fds[fd].колдонулганы {
		return nil
	}
	баяндамасы := процесси.fds[fd].баяндамасы
	if баяндамасы < 0 || баяндамасы >= maxАчууfiles || !ачууФайлЖадыбал[баяндамасы].колдонулганы {
		return nil
	}
	return &ачууФайлЖадыбал[баяндамасы]
}

func getАчууФайл(fd int32) *ачууФайлБаяндамасы {
	return getАчууФайлfor(ensurecurrentПроцесси(), fd)
}

func allocateАчууФайл() int32 {
	for i := int32(3); i < maxАчууfiles; i++ {
		if !ачууФайлЖадыбал[i].колдонулганы {
			ачууФайлЖадыбал[i] = ачууФайлБаяндамасы{колдонулганы: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(процесси *процессиentry, баяндамасы int32, төмөнкүчеги int32) int32 {
	if процесси == nil {
		return Enfile
	}
	if төмөнкүчеги < 0 || төмөнкүчеги >= maxfd {
		return Einval
	}
	for fd := төмөнкүчеги; fd < maxfd; fd++ {
		if !процесси.fds[fd].колдонулганы {
			процесси.fds[fd] = fdentry{колдонулганы: true, баяндамасы: баяндамасы}
			return fd
		}
	}
	return Emfile
}

func releaseАчууФайл(баяндамасы int32) {
	if баяндамасы < 0 || баяндамасы >= maxАчууfiles {
		return
	}
	entry := &ачууФайлЖадыбал[баяндамасы]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && баяндамасы > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = ачууФайлБаяндамасы{}
	}
}

func жабууПроцессиfd(процесси *процессиentry, fd int32) int32 {
	if процесси == nil || getАчууФайлfor(процесси, fd) == nil {
		return Ebadf
	}
	баяндамасы := процесси.fds[fd].баяндамасы
	процесси.fds[fd] = fdentry{}
	releaseАчууФайл(баяндамасы)
	return 0
}

func sysЖазуу(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getАчууФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindТамыркаталог {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтfromКөрсөткүч(uintptr(address), int(count), int(count))
	console_2.MБасма(buffer)
	return int32(count)
}

func sysОкуу(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getАчууФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return окууstdin(address, count)
	}
	if entry.kind == fdkindТамыркаталог {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.турганжери >= entry.өлчөм {
		return 0
	}
	remaining := entry.өлчөм - entry.турганжери
	if count > remaining {
		count = remaining
	}
	buffer := GetБайтfromКөрсөткүч(uintptr(address), int(count), int(count))
	return окууvfsФайл(entry, buffer, count)
}

func sysАчуу(жОЛaddress uint32, желектери uint32, режим uint32) int32 {
	_ = режим
	if жОЛaddress == 0 {
		return Efault
	}
	кирүүРежим := желектери & 3
	if кирүүРежим == oЖазууonly || кирүүРежим == oОкууЖазуу || (желектери&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	процесси := ensurecurrentПроцесси()
	if процесси == nil {
		return Enfile
	}
	баяндамасы := allocateАчууФайл()
	if баяндамасы < 0 {
		return баяндамасы
	}
	entry := &ачууФайлЖадыбал[баяндамасы]
	entry.желектери = желектери
	if isТамырЖОЛ(жОЛaddress) {
		entry.kind = fdkindТамыркаталог
		entry.өлчөм = 0
	} else {
		атыlen, аты := көчүрүүЖОЛ(жОЛaddress)
		if атыlen == 0 {
			*entry = ачууФайлБаяндамасы{}
			return Enoent
		}
		өлчөм := файлӨлчөм(аты[:атыlen])
		if өлчөм == 0 {
			*entry = ачууФайлБаяндамасы{}
			return Enoent
		}
		if (желектери & oкаталог) != 0 {
			*entry = ачууФайлБаяндамасы{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.өлчөм = өлчөм
		entry.атыlen = атыlen
		entry.аты = аты
	}

	fd := allocatefd(процесси, баяндамасы, 3)
	if fd < 0 {
		*entry = ачууФайлБаяндамасы{}
		return fd
	}
	return fd
}

func sysЖабуу(fd int32) int32 {
	return жабууПроцессиfd(ensurecurrentПроцесси(), fd)
}

func sysdup(fd int32, төмөнкүчеги int32) int32 {
	процесси := ensurecurrentПроцесси()
	entry := getАчууФайлfor(процесси, fd)
	if entry == nil {
		return Ebadf
	}
	жаңыfd := allocatefd(процесси, процесси.fds[fd].баяндамасы, төмөнкүчеги)
	if жаңыfd >= 0 {
		entry.refs++
	}
	return жаңыfd
}

func sysdup2(oldfd int32, жаңыfd int32) int32 {
	процесси := ensurecurrentПроцесси()
	entry := getАчууФайлfor(процесси, oldfd)
	if entry == nil {
		return Ebadf
	}
	if жаңыfd < 0 || жаңыfd >= maxfd {
		return Ebadf
	}
	if oldfd == жаңыfd {
		return жаңыfd
	}
	if процесси.fds[жаңыfd].колдонулганы {
		жабууПроцессиfd(процесси, жаңыfd)
	}
	процесси.fds[жаңыfd] = fdentry{колдонулганы: true, баяндамасы: процесси.fds[oldfd].баяндамасы}
	entry.refs++
	return жаңыfd
}

func sysfcntl(fd int32, команда uint32, argument uint32) int32 {
	процесси := ensurecurrentПроцесси()
	entry := getАчууФайлfor(процесси, fd)
	if entry == nil {
		return Ebadf
	}
	switch команда {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(процесси.fds[fd].fdЖелектери)
	case fsetfd:
		процесси.fds[fd].fdЖелектери = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.желектери)
	case fsetfl:
		entry.желектери = (entry.желектери & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getАчууФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekset:
		base = 0
	case seekcurrent:
		base = int64(entry.турганжери)
	case seekend:
		base = int64(entry.өлчөм)
	default:
		return Einval
	}
	турганжери_2 := base + int64(offset)
	if турганжери_2 < 0 || турганжери_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.турганжери = uint32(турганжери_2)
	return int32(entry.турганжери)
}

func окууvfsФайл(entry *ачууФайлБаяндамасы, destination_2 []byte, count uint32) int32 {
	эсиmanager := &mem.TЭсиmanager{}
	tmpКөрсөткүч := эсиmanager.Malloc(entry.өлчөм)
	if tmpКөрсөткүч == nil {
		return Einval
	}
	tmp := GetБайтfromКөрсөткүч(uintptr(tmpКөрсөткүч), int(entry.өлчөм), int(entry.өлчөм))
	окууФайл(entry.аты[:entry.атыlen], tmp)
	copy(destination_2[:count], tmp[entry.турганжери:entry.турганжери+count])
	entry.турганжери += count
	эсиmanager.Бош(tmpКөрсөткүч)
	return int32(count)
}

func isТамырЖОЛ(жОЛaddress uint32) bool {
	if жОЛaddress == 0 {
		return false
	}
	жОЛ := GetБайтfromКөрсөткүч(uintptr(жОЛaddress), 4, 4)
	if жОЛ[0] == '/' && жОЛ[1] == 0 {
		return true
	}
	if жОЛ[0] == '.' && жОЛ[1] == 0 {
		return true
	}
	if жОЛ[0] == '/' && жОЛ[1] == '.' && жОЛ[2] == 0 {
		return true
	}
	return false
}

func sysкирүү(жОЛaddress uint32, режим uint32) int32 {
	if жОЛaddress == 0 {
		return Efault
	}
	if (режим & ^uint32(7)) != 0 {
		return Einval
	}
	isТамыр := isТамырЖОЛ(жОЛaddress)
	exists := isТамыр
	if !exists {
		атыlen, аты := көчүрүүЖОЛ(жОЛaddress)
		exists = атыlen != 0 && файлӨлчөм(аты[:атыlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (режим & 2) != 0 {
		return Eacces
	}

	if (режим&1) != 0 && !isТамыр {
		return Eacces
	}
	return 0
}

func syschdir(жОЛaddress uint32) int32 {
	if жОЛaddress == 0 {
		return Efault
	}
	if !isТамырЖОЛ(жОЛaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, өлчөм uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if өлчөм < 2 {
		return Erange
	}
	buffer_2 := GetБайтfromКөрсөткүч(uintptr(bufferaddress), int(өлчөм), int(өлчөм))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, режим uint32, өлчөм uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Түзүлүшү = 1
	stat.Ino = inode
	stat.Режим = режим
	stat.Nlink = 1
	stat.Өлчөм_2 = int32(өлчөм)
	stat.Blksize = 512
	stat.Блок = int32((өлчөм + 511) / 512)
	return 0
}

func sysstat(жОЛaddress uint32, stataddress uint32) int32 {
	if жОЛaddress == 0 {
		return Efault
	}
	if isТамырЖОЛ(жОЛaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	атыlen, аты := көчүрүүЖОЛ(жОЛaddress)
	if атыlen == 0 {
		return Enoent
	}
	өлчөм := файлӨлчөм(аты[:атыlen])
	if өлчөм == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < атыlen; i++ {
		inode = inode*33 + uint32(аты[i])
	}
	return fillposixstat(stataddress, sifreg|0444, өлчөм, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getАчууФайл(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindТамыркаталог:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.өлчөм, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getАчууФайл(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	процесси := ensurecurrentПроцесси()
	if процесси == nil {
		return 0
	}
	if процесси.программаbreak == 0 {
		процесси.программаbreak = колдонуучуheapbase
	}
	if address_2 == 0 {
		return процесси.программаbreak
	}
	if address_2 < колдонуучуheapbase || address_2 > колдонуучуheaplimit {
		return процесси.программаbreak
	}
	процесси.программаbreak = address_2
	return процесси.программаbreak
}

func көчүрүүutsfield(destination *[65]byte, мааниси string) {
	limit := len(мааниси)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = мааниси[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	аты := (*posixutsname)(Pointer(uintptr(address_2)))
	*аты = posixutsname{}
	көчүрүүutsfield(&аты.Sysname, "EngOS")
	көчүрүүutsfield(&аты.Nodename, "engos")
	көчүрүүutsfield(&аты.Release, "0.1-posix")
	көчүрүүutsfield(&аты.Version, "POSIX.1-2017 phase 1")
	көчүрүүutsfield(&аты.Machine, "i386")
	return 0
}

func куюштуруусуunsignedinteger16(мааниси uint16) uint16 {
	return (мааниси << 8) | (мааниси >> 8)
}

func socketcallargument(arguments_2 uint32, мазмун uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + мазмун*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getАчууФайл(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.колдонулганы {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketТүрү uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketТүрү != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процесси := ensurecurrentПроцесси()
	if процесси == nil {
		return Enfile
	}
	socketМазмун := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].колдонулганы {
			socketМазмун = i
			break
		}
	}
	if socketМазмун < 0 {
		return Enfile
	}
	баяндамасы := allocateАчууФайл()
	if баяндамасы < 0 {
		return баяндамасы
	}
	localsockets[socketМазмун] = localdatagramsocket{колдонулганы: true}
	entry := &ачууФайлЖадыбал[баяндамасы]
	entry.kind = fdkindsocket
	entry.желектери = oОкууЖазуу
	entry.aux = uint32(socketМазмун)
	fd := allocatefd(процесси, баяндамасы, 3)
	if fd < 0 {
		localsockets[socketМазмун] = localdatagramsocket{}
		*entry = ачууФайлБаяндамасы{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, узундук uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if узундук < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func портЧоңойтууuse(порт uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.колдонулганы && socket.bound && socket.local.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := куюштуруусуunsignedinteger16(кийинкиephemeralПорт)
		кийинкиephemeralПорт++
		if кийинкиephemeralПорт < 49152 {
			кийинкиephemeralПорт = 49152
		}
		if !портЧоңойтууuse(порт, socket) {
			socket.local = socketaddressipv4{Family: afinet, Порт: порт, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, узундук uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, узундук)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return bindephemeral(socket)
	}
	if портЧоңойтууuse(requested.Порт, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketТуташуу(fd int32, address_2 uint32, узундук uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, узундук)
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

func socketsendto(fd int32, bufferaddress_2 uint32, узундук uint32, destinationaddress uint32, destinationУзундук uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if узундук > maxdatagramӨлчөм {
		return Emsgsize
	}
	if узундук != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressКата := socketaddress(destinationaddress, destinationУзундук)
		if addressКата != 0 {
			return addressКата
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindКата := bindephemeral(socket); bindКата != 0 {
			return bindКата
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.колдонулганы && candidate.bound && candidate.local.Порт == destination.Порт &&
			(candidate.local.Address == 0 || candidate.local.Address == destination.Address) {
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
	*packet = socketpacket{колдонулганы: true, өлчөм: узундук, баштапкытекст: socket.local}
	if узундук != 0 {
		баштапкытекст := GetБайтfromКөрсөткүч(uintptr(bufferaddress_2), int(узундук), int(узундук))
		copy(packet.data[:узундук], баштапкытекст)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(узундук)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, узундук uint32, баштапкытекстaddress uint32, баштапкытекстУзундукaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if узундук != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	көчүрүүУзундук := packet.өлчөм
	if көчүрүүУзундук > узундук {
		көчүрүүУзундук = узундук
	}
	if көчүрүүУзундук != 0 {
		destination := GetБайтfromКөрсөткүч(uintptr(bufferaddress_2), int(көчүрүүУзундук), int(көчүрүүУзундук))
		copy(destination, packet.data[:көчүрүүУзундук])
	}
	if баштапкытекстaddress != 0 {
		if баштапкытекстУзундукaddress == 0 {
			return Efault
		}
		providedУзундук := (*uint32)(Pointer(uintptr(баштапкытекстУзундукaddress)))
		if *providedУзундук >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(баштапкытекстaddress))) = packet.баштапкытекст
		}
		*providedУзундук = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(көчүрүүУзундук)
}

func көчүрүүsocketАты(fd int32, address_2 uint32, узундукaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || узундукaddress == 0 {
		return Efault
	}
	узундук := (*uint32)(Pointer(uintptr(узундукaddress)))
	if *узундук < 16 {
		*узундук = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindКата := bindephemeral(socket); bindКата != 0 {
				return bindКата
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*узундук = 16
	return 0
}

func syssocketcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(arguments_2, 0), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 3:
		return socketТуташуу(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return көчүрүүsocketАты(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return көчүрүүsocketАты(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
	case 9:
		return socketsendto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return socketsendto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 13:
		if _, err := socketforfd(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketforfd(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func окууstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБайтfromКөрсөткүч(uintptr(address), int(count), int(count))
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
	кийинки := (stdinЖазуу + 1) % uint32(len(stdinbuffer))
	if кийинки == stdinОкуу {
		return
	}
	stdinbuffer[stdinЖазуу] = c
	stdinЖазуу = кийинки
}

func stdingetblocking() byte {
	for stdinОкуу == stdinЖазуу {
		sc := pollКлавиатураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinОкуу]
	stdinОкуу = (stdinОкуу + 1) % uint32(len(stdinbuffer))
	return c
}

func pollКлавиатураscancode() byte {
	for (ПортОкууbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортОкууbyte(0x60)
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

func көчүрүүexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for мазмун := uint32(0); мазмун < maxexecvectorentry; мазмун++ {
		сАПaddress := *(*uint32)(Pointer(uintptr(address_2 + мазмун*4)))
		if сАПaddress == 0 {
			result.count = мазмун
			return 0
		}
		terminated := false
		for узундук := uint32(0); узундук <= maxexecСАПУзундук; узундук++ {
			мааниси := *(*byte)(Pointer(uintptr(сАПaddress + узундук)))
			result.values[мазмун][узундук] = мааниси
			if мааниси == 0 {
				result.lengths[мазмун] = узундук
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

func pushexecunsignedinteger32(stack *uint32, мааниси uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = мааниси
}

func setupexecstack(бП *TcpuАбал, arguments_2 *execvector, environment *execvector) int32 {
	const stackБайт uint32 = 4096
	if !MakeДиапазонprivatewritable(getcr3(), КолдонуучуstackҮстү-stackБайт, stackБайт) {
		return Enomem
	}
	stack := КолдонуучуstackҮстү
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		узундук := environment.lengths[i] + 1
		stack -= узундук
		destination := GetБайтfromКөрсөткүч(uintptr(stack), int(узундук), int(узундук))
		copy(destination, environment.values[i][:узундук])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		узундук := arguments_2.lengths[i] + 1
		stack -= узундук
		destination := GetБайтfromКөрсөткүч(uintptr(stack), int(узундук), int(узундук))
		copy(destination, arguments_2.values[i][:узундук])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushexecunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, environmentpointers[i])
	}
	pushexecunsignedinteger32(&stack, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushexecunsignedinteger32(&stack, argumentpointers[i])
	}
	pushexecunsignedinteger32(&stack, arguments_2.count)
	бП.Esp = stack
	бП.Ebp = 0
	return 0
}

func жабууonexec(процесси *процессиentry) {
	if процесси == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if процесси.fds[fd].колдонулганы && (процесси.fds[fd].fdЖелектери&fdcloexec) != 0 {
			жабууПроцессиfd(процесси, fd)
		}
	}
}

func sysexecve(бП *TcpuАбал, жОЛaddress uint32) int32 {
	if жОЛaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := көчүрүүexecvector(бП.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := көчүрүүexecvector(бП.Edx, &environment); result < 0 {
		return result
	}
	атыlen, аты := көчүрүүЖОЛ(жОЛaddress)
	if атыlen == 0 {
		return Enoent
	}
	өлчөм := файлӨлчөм(аты[:атыlen])
	if өлчөм == 0 {
		return Enoent
	}
	эсиmanager := &mem.TЭсиmanager{}
	файлКөрсөткүч := эсиmanager.Malloc(өлчөм)
	if файлКөрсөткүч == nil {
		return Einval
	}
	data := GetБайтfromКөрсөткүч(uintptr(файлКөрсөткүч), int(өлчөм), int(өлчөм))
	окууФайл(аты[:атыlen], data)
	if өлчөм < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		эсиmanager.Бош(файлКөрсөткүч)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	эсиmanager.Бош(файлКөрсөткүч)
	if result := setupexecstack(бП, &arguments_2, &environment); result < 0 {
		return result
	}
	жабууonexec(ensurecurrentПроцесси())
	бП.Eip = entry
	бП.Eax = 0
	return 0
}

func sysfork(бП *TcpuАбал) int32 {
	атаэнеpid := Currentpid()
	if ensurecurrentПроцесси() == nil {
		return Enfile
	}
	pid := allocateПроцесси(атаэнеpid)
	if pid == 0 {
		return Einval
	}
	эсиmanager := &mem.TЭсиmanager{}
	threadКөрсөткүч := эсиmanager.Malloc(uint32(Sizeof(TThread{})))
	stackКөрсөткүч := эсиmanager.Malloc(ThreadstackӨлчөм)
	тукумБАРАКкаталог := Cloneaddressspacecow(getcr3())
	if threadКөрсөткүч == nil || stackКөрсөткүч == nil || тукумБАРАКкаталог == 0 {
		discardПроцесси(pid)
		return Einval
	}
	тукум := (*TThread)(threadКөрсөткүч)
	тукум.Stack = uint32(uintptr(stackКөрсөткүч))
	тукум.БПАбал = (*TcpuАбал)(Pointer(uintptr(stackКөрсөткүч) + ThreadstackӨлчөм - Sizeof(TcpuАбал{})))
	*тукум.БПАбал = *бП
	тукум.БПАбал.Eax = 0
	тукум.Колдонуучуstack_2 = бП.Esp
	тукум.КолдонуучуstackӨлчөм_2 = 0
	тукум.Pid = pid
	тукум.Атаэнеpid = атаэнеpid
	тукум.БАРАКкаталогentry = тукумБАРАКкаталог
	тукум.ThreadАбал = Даяр
	тукум.Fpuoffset = 0xffffffff
	тукум.Iskernel = false
	Кошууrunnablethread(тукум)
	return int32(pid)
}

func sysexit(абалы uint32) {
	pid := Currentpid()
	for i := 0; i < len(процессиЖадыбал); i++ {
		if процессиЖадыбал[i].колдонулганы && процессиЖадыбал[i].pid == pid {
			жабууallПроцессиfds(&процессиЖадыбал[i])
			процессиЖадыбал[i].exited = true
			процессиЖадыбал[i].абалы = (абалы & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, абалыaddress uint32, параметрлер uint32) int32 {
	if (параметрлер & ^uint32(1)) != 0 {
		return Einval
	}
	атаэнеpid := Currentpid()
	foundтукум := false
	for i := 0; i < len(процессиЖадыбал); i++ {
		p := &процессиЖадыбал[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.колдонулганы && matches && p.атаэне == атаэнеpid {
			foundтукум = true
			if p.exited {
				if абалыaddress != 0 {
					*(*uint32)(Pointer(uintptr(абалыaddress))) = p.абалы
				}
				тукумpid := p.pid
				*p = процессиentry{}
				return int32(тукумpid)
			}
		}
	}
	if !foundтукум {
		return Echild
	}

	if (параметрлер & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцесси(атаэне uint32) uint32 {
	атаэнеПроцесси := табууПроцесси(атаэне)
	pid := Allocatepid()
	for i := 0; i < len(процессиЖадыбал); i++ {
		if !процессиЖадыбал[i].колдонулганы {
			процессиЖадыбал[i] = процессиentry{
				колдонулганы:	true,
				pid:		pid,
				атаэне:		атаэне,
				программаbreak:	колдонуучуheapbase,
			}
			if атаэнеПроцесси != nil {
				процессиЖадыбал[i].программаbreak = атаэнеПроцесси.программаbreak
				for fd := 0; fd < maxfd; fd++ {
					if атаэнеПроцесси.fds[fd].колдонулганы {
						процессиЖадыбал[i].fds[fd] = атаэнеПроцесси.fds[fd]
						баяндамасы := атаэнеПроцесси.fds[fd].баяндамасы
						if баяндамасы >= 0 && баяндамасы < maxАчууfiles {
							ачууФайлЖадыбал[баяндамасы].refs++
						}
					}
				}
			} else {
				initializeПроцессиfds(&процессиЖадыбал[i])
			}
			return pid
		}
	}
	return 0
}

func жабууallПроцессиfds(процесси *процессиentry) {
	if процесси == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if процесси.fds[fd].колдонулганы {
			жабууПроцессиfd(процесси, fd)
		}
	}
}

func discardПроцесси(pid uint32) {
	процесси := табууПроцесси(pid)
	if процесси == nil {
		return
	}
	жабууallПроцессиfds(процесси)
	*процесси = процессиentry{}
}

func көчүрүүЖОЛ(жОЛaddress uint32) (uint32, [12]byte) {
	var аты [12]byte
	if жОЛaddress == 0 {
		return 0, аты
	}
	raw := GetБайтfromКөрсөткүч(uintptr(жОЛaddress), 64, 64)
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
		аты[n] = c
		n++
	}
	return n, аты
}

func файлӨлчөм(файлаты []byte) uint32 {
	var ata0s = TКеңейтилгенТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionЖадыбал{}
	partition.Окууpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	өлчөм := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлаты)
	ata0s.Flush()
	return өлчөм
}

func окууФайл(файлаты []byte, data []byte) {
	var ata0s = TКеңейтилгенТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionЖадыбал{}
	partition.Окууpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Окуу(&ata0s, partition.Mbr.Primarypartition[0], файлаты, data)
	ata0s.Flush()
}

func getcr3() uint32
