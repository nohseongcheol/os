package համակարգcall

import . "unsafe"

import . "ընդհատել"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "ֆայլՀամակարգ/msdospartition"
import . "ֆայլՀամակարգ/fat"
import . "ֆայլՀամակարգ/elf"
import mem "հիշողությունmanager"
import . "paging"
import . "պորտ"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualՀիշողություն"

var console_2 = TConsole{}

type TSyscall struct {
	TԸնդհատելhandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	SysԸնթերցում	uint32	= 3
	SysԳրել		uint32	= 4
	SysԲացել	uint32	= 5
	SysՓակել	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysմուտք	uint32	= 33
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
	stdinՖայլայինդեսկրիպտոր		int32	= 0
	stdoutՖայլայինդեսկրիպտոր	int32	= 1
	stderrՖայլայինդեսկրիպտոր	int32	= 2
	maxՖայլայինդեսկրիպտոր			= 32
	maxԲացելfiles				= 128
)

type ֆայլայինդեսկրիպտորentry struct {
	օգտագործված			bool
	նկարագրություն			int32
	ֆայլայինդեսկրիպտորԴրոշներ	uint32
}

type բացելՖայլՆկարագրություն struct {
	օգտագործված	bool
	refs		uint32
	kind		uint32
	դրոշներ		uint32
	դիրք		uint32
	չափս		uint32
	անուն		[12]byte
	անունlen	uint32
	aux		uint32
}

const (
	ֆայլայինդեսկրիպտորkindՈչինչ		uint32	= 0
	ֆայլայինդեսկրիպտորkindfat		uint32	= 1
	ֆայլայինդեսկրիպտորkindstdin		uint32	= 2
	ֆայլայինդեսկրիպտորkindconsole		uint32	= 3
	ֆայլայինդեսկրիպտորkindԱրմատֆայլապանակ	uint32	= 4
	ֆայլայինդեսկրիպտորkindsocket		uint32	= 5

	oԸնթերցումonly	uint32	= 0
	oԳրելonly	uint32	= 1
	oԸնթերցումԳրել	uint32	= 2
	ocreate		uint32	= 0x40
	oԿտրել		uint32	= 0x200
	oappend		uint32	= 0x400
	oֆայլապանակ	uint32	= 0x10000

	seekset		uint32	= 0
	seekcurrent	uint32	= 1
	seekվերջ	uint32	= 2

	fdupՖայլայինդեսկրիպտոր		uint32	= 0
	fgetՖայլայինդեսկրիպտոր		uint32	= 1
	fsetՖայլայինդեսկրիպտոր		uint32	= 2
	fgetfl				uint32	= 3
	fsetfl				uint32	= 4
	ֆայլայինդեսկրիպտորcloexec	uint32	= 1

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
	maxdatagramՉափս		= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Պորտ	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	օգտագործված	bool
	չափս		uint32
	աղբյուր		socketaddressipv4
	data		[maxdatagramՉափս]byte
}

type տեղայինdatagramsocket struct {
	օգտագործված	bool
	bound		bool
	connected	bool
	տեղային		socketaddressipv4
	remote		socketaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Սարք		uint32
	Ino		uint32
	Ռեժիմ		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Չափս_2		int32
	Blksize		int32
	Արգելափակել	int32
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
	maxexecՏՈՂԵրկարություն	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecՏՈՂԵրկարություն + 1]byte
}

type գործընթացentry struct {
	օգտագործված	bool
	pid		uint32
	ծնող		uint32
	exited		bool
	կարգավիճակ	uint32
	ծրագիրbreak	uint32
	fds		[maxՖայլայինդեսկրիպտոր]ֆայլայինդեսկրիպտորentry
}

type տՈՂheader struct {
	Data	uintptr
	Len	int
}

func syscallՍխալ(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var բացելՖայլԱղյուսակ [maxԲացելfiles]բացելՖայլՆկարագրություն
var գործընթացԱղյուսակ [32]գործընթացentry
var տեղայինsockets [maxsockets]տեղայինdatagramsocket
var հաջորդephemeralՊորտ uint16 = 49152

const (
	օգտագործողheapbase	uint32	= 0x06000000
	օգտագործողheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinԸնթերցում uint32
var stdinԳրել uint32

func Ընդհատել(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(ինդեքս uint32) {
	Syscall(Sysexit, ինդեքս)
}

func SysԸնթերցում_2(ֆայլայինդեսկրիպտոր uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysԸնթերցում, ֆայլայինդեսկրիպտոր, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysՏպելstr(buffer string) {
	h := (*տՈՂheader)(Pointer(&buffer))
	Syscall(SysԳրել, uint32(stdoutՖայլայինդեսկրիպտոր), uint32(h.Data), uint32(h.Len))
}

func SysՏպելunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysԳրել, uint32(stdoutՖայլայինդեսկրիպտոր), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysԲացել_2(ոՒՂԻ uintptr, դրոշներ uint32, ռեժիմ uint32) int32 {
	return int32(Syscall(SysԲացել, uint32(ոՒՂԻ), դրոշներ, ռեժիմ))
}

func SysՓակել_2(ֆայլայինդեսկրիպտոր uint32) int32 {
	return int32(Syscall(SysՓակել, ֆայլայինդեսկրիպտոր))
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
		return Ընդհատել(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Ընդհատել(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Ընդհատել(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Ընդհատել(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Ընդհատել(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Ընդհատել(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallՍխալ(Enosys)
	}
}

func (ինքնուրույն *TSyscall) Init(manager *TԸնդհատելmanager) {
	initՖայլdescriptor()

	ընդհատելhandler = handleԸնդհատել

	var address uintptr
	address = uintptr(Pointer(&ընդհատելhandler))

	ինքնուրույն.TԸնդհատելhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var ընդհատելhandler func(uint32) uint32

func handleԸնդհատել(esp uint32) uint32 {
	var կՄՀ = (*TcpuՎիճակ)(Pointer(uintptr(esp)))

	switch կՄՀ.Eax {
	case Sysexit:
		sysexit(կՄՀ.Ebx)
		return uint32(uintptr(Pointer(Կանգառcurrentthread(կՄՀ))))
	case Sysrtexit:
		sysexit(կՄՀ.Ebx)
		return uint32(uintptr(Pointer(Կանգառcurrentthread(կՄՀ))))
	case Sysfork:
		կՄՀ.Eax = uint32(sysfork(կՄՀ))
		return esp
	case SysԸնթերցում:
		կՄՀ.Eax = uint32(sysԸնթերցում(int32(կՄՀ.Ebx), կՄՀ.Ecx, կՄՀ.Edx))
		return esp
	case SysԳրել:
		կՄՀ.Eax = uint32(sysԳրել(int32(կՄՀ.Ebx), կՄՀ.Ecx, կՄՀ.Edx))
		return esp
	case SysԲացել:
		կՄՀ.Eax = uint32(sysԲացել(կՄՀ.Ebx, կՄՀ.Ecx, կՄՀ.Edx))
		return esp
	case Syscreat:
		կՄՀ.Eax = uint32(sysԲացել(կՄՀ.Ebx, ocreate|oԳրելonly|oԿտրել, կՄՀ.Ecx))
		return esp
	case SysՓակել:
		կՄՀ.Eax = uint32(sysՓակել(int32(կՄՀ.Ebx)))
		return esp
	case Syswaitpid:
		կՄՀ.Eax = uint32(syswaitpid(int32(կՄՀ.Ebx), կՄՀ.Ecx, կՄՀ.Edx))
		return esp
	case Syslseek:
		կՄՀ.Eax = uint32(syslseek(int32(կՄՀ.Ebx), int32(կՄՀ.Ecx), կՄՀ.Edx))
		return esp
	case Sysexecve:
		կՄՀ.Eax = uint32(sysexecve(կՄՀ, կՄՀ.Ebx))
		return esp
	case Sysgetpid:
		կՄՀ.Eax = Currentpid()
		return esp
	case Sysgetppid:
		կՄՀ.Eax = Currentծնողpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		կՄՀ.Eax = 0
		return esp
	case Sysմուտք:
		կՄՀ.Eax = uint32(sysմուտք(կՄՀ.Ebx, կՄՀ.Ecx))
		return esp
	case Syschdir:
		կՄՀ.Eax = uint32(syschdir(կՄՀ.Ebx))
		return esp
	case Sysgetcwd:
		կՄՀ.Eax = uint32(sysgetcwd(կՄՀ.Ebx, կՄՀ.Ecx))
		return esp
	case Sysdup:
		կՄՀ.Eax = uint32(sysdup(int32(կՄՀ.Ebx), 0))
		return esp
	case Sysdup2:
		կՄՀ.Eax = uint32(sysdup2(int32(կՄՀ.Ebx), int32(կՄՀ.Ecx)))
		return esp
	case Syssocketcall:
		կՄՀ.Eax = uint32(syssocketcall(կՄՀ.Ebx, կՄՀ.Ecx))
		return esp
	case Sysfcntl:
		կՄՀ.Eax = uint32(sysfcntl(int32(կՄՀ.Ebx), կՄՀ.Ecx, կՄՀ.Edx))
		return esp
	case Sysstat, Syslstat:
		կՄՀ.Eax = uint32(sysstat(կՄՀ.Ebx, կՄՀ.Ecx))
		return esp
	case Sysfstat:
		կՄՀ.Eax = uint32(sysfstat(int32(կՄՀ.Ebx), կՄՀ.Ecx))
		return esp
	case Sysfsync:
		կՄՀ.Eax = uint32(sysfsync(int32(կՄՀ.Ebx)))
		return esp
	case Syssync:
		կՄՀ.Eax = 0
		return esp
	case Sysuname:
		կՄՀ.Eax = uint32(sysuname(կՄՀ.Ebx))
		return esp
	case Sysbrk:
		կՄՀ.Eax = sysbrk(կՄՀ.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Տպել(կՄՀ.Ebx)
		return esp

	default:
		console_2.MՏպելxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Տպել(esp)
		console_2.MՏպել(([]byte)(":"))
		console_2.MUnsignedinteger32Տպել(կՄՀ.Eax)
		console_2.MՏպել(([]byte)(":"))
		console_2.MUnsignedinteger32Տպել(կՄՀ.Ebx)
		console_2.MՏպել(([]byte)(":"))
		console_2.MUnsignedinteger32Տպել(կՄՀ.Ecx)
		console_2.MՏպել(([]byte)(":"))
		console_2.MUnsignedinteger32Տպել(կՄՀ.Edx)
		console_2.MՏպել(([]byte)("]"))
		կՄՀ.Eax = syscallՍխալ(Enosys)
		return esp
	}

	return esp
}

func initՖայլdescriptor() {
	for i := 0; i < maxԲացելfiles; i++ {
		բացելՖայլԱղյուսակ[i] = բացելՖայլՆկարագրություն{}
	}
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		գործընթացԱղյուսակ[i] = գործընթացentry{}
	}
	for i := 0; i < len(տեղայինsockets); i++ {
		տեղայինsockets[i] = տեղայինdatagramsocket{}
	}
	հաջորդephemeralՊորտ = 49152
	բացելՖայլԱղյուսակ[0] = բացելՖայլՆկարագրություն{օգտագործված: true, kind: ֆայլայինդեսկրիպտորkindstdin, դրոշներ: oԸնթերցումonly}
	բացելՖայլԱղյուսակ[1] = բացելՖայլՆկարագրություն{օգտագործված: true, kind: ֆայլայինդեսկրիպտորkindconsole, դրոշներ: oԳրելonly}
	բացելՖայլԱղյուսակ[2] = բացելՖայլՆկարագրություն{օգտագործված: true, kind: ֆայլայինդեսկրիպտորkindconsole, դրոշներ: oԳրելonly}
}

func գտնելԳործընթաց(pid uint32) *գործընթացentry {
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		if գործընթացԱղյուսակ[i].օգտագործված && գործընթացԱղյուսակ[i].pid == pid {
			return &գործընթացԱղյուսակ[i]
		}
	}
	return nil
}

func initializeԳործընթացfds(գործընթաց *գործընթացentry) {
	for ֆայլայինդեսկրիպտոր := int32(0); ֆայլայինդեսկրիպտոր <= stderrՖայլայինդեսկրիպտոր; ֆայլայինդեսկրիպտոր++ {
		գործընթաց.fds[ֆայլայինդեսկրիպտոր] = ֆայլայինդեսկրիպտորentry{օգտագործված: true, նկարագրություն: ֆայլայինդեսկրիպտոր}
		բացելՖայլԱղյուսակ[ֆայլայինդեսկրիպտոր].refs++
	}
}

func ensurecurrentԳործընթաց() *գործընթացentry {
	pid := Currentpid()
	if գործընթաց := գտնելԳործընթաց(pid); գործընթաց != nil {
		return գործընթաց
	}
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		if !գործընթացԱղյուսակ[i].օգտագործված {
			գործընթացԱղյուսակ[i] = գործընթացentry{
				օգտագործված:	true,
				pid:		pid,
				ծնող:		Currentծնողpid(),
				ծրագիրbreak:	օգտագործողheapbase,
			}
			initializeԳործընթացfds(&գործընթացԱղյուսակ[i])
			return &գործընթացԱղյուսակ[i]
		}
	}
	return nil
}

func getԲացելՖայլfor(գործընթաց *գործընթացentry, ֆայլայինդեսկրիպտոր int32) *բացելՖայլՆկարագրություն {
	if գործընթաց == nil || ֆայլայինդեսկրիպտոր < 0 || ֆայլայինդեսկրիպտոր >= maxՖայլայինդեսկրիպտոր || !գործընթաց.fds[ֆայլայինդեսկրիպտոր].օգտագործված {
		return nil
	}
	նկարագրություն := գործընթաց.fds[ֆայլայինդեսկրիպտոր].նկարագրություն
	if նկարագրություն < 0 || նկարագրություն >= maxԲացելfiles || !բացելՖայլԱղյուսակ[նկարագրություն].օգտագործված {
		return nil
	}
	return &բացելՖայլԱղյուսակ[նկարագրություն]
}

func getԲացելՖայլ(ֆայլայինդեսկրիպտոր int32) *բացելՖայլՆկարագրություն {
	return getԲացելՖայլfor(ensurecurrentԳործընթաց(), ֆայլայինդեսկրիպտոր)
}

func allocateԲացելՖայլ() int32 {
	for i := int32(3); i < maxԲացելfiles; i++ {
		if !բացելՖայլԱղյուսակ[i].օգտագործված {
			բացելՖայլԱղյուսակ[i] = բացելՖայլՆկարագրություն{օգտագործված: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateՖայլայինդեսկրիպտոր(գործընթաց *գործընթացentry, նկարագրություն int32, նվազագույն int32) int32 {
	if գործընթաց == nil {
		return Enfile
	}
	if նվազագույն < 0 || նվազագույն >= maxՖայլայինդեսկրիպտոր {
		return Einval
	}
	for ֆայլայինդեսկրիպտոր := նվազագույն; ֆայլայինդեսկրիպտոր < maxՖայլայինդեսկրիպտոր; ֆայլայինդեսկրիպտոր++ {
		if !գործընթաց.fds[ֆայլայինդեսկրիպտոր].օգտագործված {
			գործընթաց.fds[ֆայլայինդեսկրիպտոր] = ֆայլայինդեսկրիպտորentry{օգտագործված: true, նկարագրություն: նկարագրություն}
			return ֆայլայինդեսկրիպտոր
		}
	}
	return Emfile
}

func releaseԲացելՖայլ(նկարագրություն int32) {
	if նկարագրություն < 0 || նկարագրություն >= maxԲացելfiles {
		return
	}
	entry := &բացելՖայլԱղյուսակ[նկարագրություն]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && նկարագրություն > stderrՖայլայինդեսկրիպտոր {
		if entry.kind == ֆայլայինդեսկրիպտորkindsocket && entry.aux < maxsockets {
			տեղայինsockets[entry.aux] = տեղայինdatagramsocket{}
		}
		*entry = բացելՖայլՆկարագրություն{}
	}
}

func փակելԳործընթացՖայլայինդեսկրիպտոր(գործընթաց *գործընթացentry, ֆայլայինդեսկրիպտոր int32) int32 {
	if գործընթաց == nil || getԲացելՖայլfor(գործընթաց, ֆայլայինդեսկրիպտոր) == nil {
		return Ebadf
	}
	նկարագրություն := գործընթաց.fds[ֆայլայինդեսկրիպտոր].նկարագրություն
	գործընթաց.fds[ֆայլայինդեսկրիպտոր] = ֆայլայինդեսկրիպտորentry{}
	releaseԲացելՖայլ(նկարագրություն)
	return 0
}

func sysԳրել(ֆայլայինդեսկրիպտոր int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getԲացելՖայլ(ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != ֆայլայինդեսկրիպտորkindconsole {
		if entry.kind == ֆայլայինդեսկրիպտորkindsocket {
			return socketՈՒղարկելto(ֆայլայինդեսկրիպտոր, address, count, 0, 0)
		}
		if entry.kind == ֆայլայինդեսկրիպտորkindfat || entry.kind == ֆայլայինդեսկրիպտորkindԱրմատֆայլապանակ {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetԲայթերիցՑուցիչ(uintptr(address), int(count), int(count))
	console_2.MՏպել(buffer)
	return int32(count)
}

func sysԸնթերցում(ֆայլայինդեսկրիպտոր int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getԲացելՖայլ(ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == ֆայլայինդեսկրիպտորkindstdin {
		return ընթերցումstdin(address, count)
	}
	if entry.kind == ֆայլայինդեսկրիպտորkindԱրմատֆայլապանակ {
		return Eisdir
	}
	if entry.kind == ֆայլայինդեսկրիպտորkindsocket {
		return socketreceiveից(ֆայլայինդեսկրիպտոր, address, count, 0, 0)
	}
	if entry.kind != ֆայլայինդեսկրիպտորkindfat {
		return Ebadf
	}
	if entry.դիրք >= entry.չափս {
		return 0
	}
	remaining := entry.չափս - entry.դիրք
	if count > remaining {
		count = remaining
	}
	buffer := GetԲայթերիցՑուցիչ(uintptr(address), int(count), int(count))
	return ընթերցումvfsՖայլ(entry, buffer, count)
}

func sysԲացել(ոՒՂԻaddress uint32, դրոշներ uint32, ռեժիմ uint32) int32 {
	_ = ռեժիմ
	if ոՒՂԻaddress == 0 {
		return Efault
	}
	մուտքՌեժիմ := դրոշներ & 3
	if մուտքՌեժիմ == oԳրելonly || մուտքՌեժիմ == oԸնթերցումԳրել || (դրոշներ&(ocreate|oԿտրել|oappend)) != 0 {
		return Erofs
	}

	գործընթաց := ensurecurrentԳործընթաց()
	if գործընթաց == nil {
		return Enfile
	}
	նկարագրություն := allocateԲացելՖայլ()
	if նկարագրություն < 0 {
		return նկարագրություն
	}
	entry := &բացելՖայլԱղյուսակ[նկարագրություն]
	entry.դրոշներ = դրոշներ
	if isԱրմատՈՒՂԻ(ոՒՂԻaddress) {
		entry.kind = ֆայլայինդեսկրիպտորkindԱրմատֆայլապանակ
		entry.չափս = 0
	} else {
		անունlen, անուն := պատճենելՈՒՂԻ(ոՒՂԻaddress)
		if անունlen == 0 {
			*entry = բացելՖայլՆկարագրություն{}
			return Enoent
		}
		չափս := ֆայլՉափս(անուն[:անունlen])
		if չափս == 0 {
			*entry = բացելՖայլՆկարագրություն{}
			return Enoent
		}
		if (դրոշներ & oֆայլապանակ) != 0 {
			*entry = բացելՖայլՆկարագրություն{}
			return Enotdir
		}
		entry.kind = ֆայլայինդեսկրիպտորkindfat
		entry.չափս = չափս
		entry.անունlen = անունlen
		entry.անուն = անուն
	}

	ֆայլայինդեսկրիպտոր := allocateՖայլայինդեսկրիպտոր(գործընթաց, նկարագրություն, 3)
	if ֆայլայինդեսկրիպտոր < 0 {
		*entry = բացելՖայլՆկարագրություն{}
		return ֆայլայինդեսկրիպտոր
	}
	return ֆայլայինդեսկրիպտոր
}

func sysՓակել(ֆայլայինդեսկրիպտոր int32) int32 {
	return փակելԳործընթացՖայլայինդեսկրիպտոր(ensurecurrentԳործընթաց(), ֆայլայինդեսկրիպտոր)
}

func sysdup(ֆայլայինդեսկրիպտոր int32, նվազագույն int32) int32 {
	գործընթաց := ensurecurrentԳործընթաց()
	entry := getԲացելՖայլfor(գործընթաց, ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	նորՖայլայինդեսկրիպտոր := allocateՖայլայինդեսկրիպտոր(գործընթաց, գործընթաց.fds[ֆայլայինդեսկրիպտոր].նկարագրություն, նվազագույն)
	if նորՖայլայինդեսկրիպտոր >= 0 {
		entry.refs++
	}
	return նորՖայլայինդեսկրիպտոր
}

func sysdup2(oldՖայլայինդեսկրիպտոր int32, նորՖայլայինդեսկրիպտոր int32) int32 {
	գործընթաց := ensurecurrentԳործընթաց()
	entry := getԲացելՖայլfor(գործընթաց, oldՖայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	if նորՖայլայինդեսկրիպտոր < 0 || նորՖայլայինդեսկրիպտոր >= maxՖայլայինդեսկրիպտոր {
		return Ebadf
	}
	if oldՖայլայինդեսկրիպտոր == նորՖայլայինդեսկրիպտոր {
		return նորՖայլայինդեսկրիպտոր
	}
	if գործընթաց.fds[նորՖայլայինդեսկրիպտոր].օգտագործված {
		փակելԳործընթացՖայլայինդեսկրիպտոր(գործընթաց, նորՖայլայինդեսկրիպտոր)
	}
	գործընթաց.fds[նորՖայլայինդեսկրիպտոր] = ֆայլայինդեսկրիպտորentry{օգտագործված: true, նկարագրություն: գործընթաց.fds[oldՖայլայինդեսկրիպտոր].նկարագրություն}
	entry.refs++
	return նորՖայլայինդեսկրիպտոր
}

func sysfcntl(ֆայլայինդեսկրիպտոր int32, հրահանգ uint32, argument uint32) int32 {
	գործընթաց := ensurecurrentԳործընթաց()
	entry := getԲացելՖայլfor(գործընթաց, ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	switch հրահանգ {
	case fdupՖայլայինդեսկրիպտոր:
		return sysdup(ֆայլայինդեսկրիպտոր, int32(argument))
	case fgetՖայլայինդեսկրիպտոր:
		return int32(գործընթաց.fds[ֆայլայինդեսկրիպտոր].ֆայլայինդեսկրիպտորԴրոշներ)
	case fsetՖայլայինդեսկրիպտոր:
		գործընթաց.fds[ֆայլայինդեսկրիպտոր].ֆայլայինդեսկրիպտորԴրոշներ = argument & ֆայլայինդեսկրիպտորcloexec
		return 0
	case fgetfl:
		return int32(entry.դրոշներ)
	case fsetfl:
		entry.դրոշներ = (entry.դրոշներ & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(ֆայլայինդեսկրիպտոր int32, offset int32, whence uint32) int32 {
	entry := getԲացելՖայլ(ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != ֆայլայինդեսկրիպտորkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekset:
		base = 0
	case seekcurrent:
		base = int64(entry.դիրք)
	case seekվերջ:
		base = int64(entry.չափս)
	default:
		return Einval
	}
	դիրք_2 := base + int64(offset)
	if դիրք_2 < 0 || դիրք_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.դիրք = uint32(դիրք_2)
	return int32(entry.դիրք)
}

func ընթերցումvfsՖայլ(entry *բացելՖայլՆկարագրություն, destination_2 []byte, count uint32) int32 {
	հիշողությունmanager := &mem.TՀիշողությունmanager{}
	tmpՑուցիչ := հիշողությունmanager.Malloc(entry.չափս)
	if tmpՑուցիչ == nil {
		return Einval
	}
	tmp := GetԲայթերիցՑուցիչ(uintptr(tmpՑուցիչ), int(entry.չափս), int(entry.չափս))
	ընթերցումՖայլ(entry.անուն[:entry.անունlen], tmp)
	copy(destination_2[:count], tmp[entry.դիրք:entry.դիրք+count])
	entry.դիրք += count
	հիշողությունmanager.Ազատ(tmpՑուցիչ)
	return int32(count)
}

func isԱրմատՈՒՂԻ(ոՒՂԻaddress uint32) bool {
	if ոՒՂԻaddress == 0 {
		return false
	}
	ոՒՂԻ := GetԲայթերիցՑուցիչ(uintptr(ոՒՂԻaddress), 4, 4)
	if ոՒՂԻ[0] == '/' && ոՒՂԻ[1] == 0 {
		return true
	}
	if ոՒՂԻ[0] == '.' && ոՒՂԻ[1] == 0 {
		return true
	}
	if ոՒՂԻ[0] == '/' && ոՒՂԻ[1] == '.' && ոՒՂԻ[2] == 0 {
		return true
	}
	return false
}

func sysմուտք(ոՒՂԻaddress uint32, ռեժիմ uint32) int32 {
	if ոՒՂԻaddress == 0 {
		return Efault
	}
	if (ռեժիմ & ^uint32(7)) != 0 {
		return Einval
	}
	isԱրմատ := isԱրմատՈՒՂԻ(ոՒՂԻaddress)
	exists := isԱրմատ
	if !exists {
		անունlen, անուն := պատճենելՈՒՂԻ(ոՒՂԻaddress)
		exists = անունlen != 0 && ֆայլՉափս(անուն[:անունlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (ռեժիմ & 2) != 0 {
		return Eacces
	}

	if (ռեժիմ&1) != 0 && !isԱրմատ {
		return Eacces
	}
	return 0
}

func syschdir(ոՒՂԻaddress uint32) int32 {
	if ոՒՂԻaddress == 0 {
		return Efault
	}
	if !isԱրմատՈՒՂԻ(ոՒՂԻaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, չափս uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if չափս < 2 {
		return Erange
	}
	buffer_2 := GetԲայթերիցՑուցիչ(uintptr(bufferaddress), int(չափս), int(չափս))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, ռեժիմ uint32, չափս uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Սարք = 1
	stat.Ino = inode
	stat.Ռեժիմ = ռեժիմ
	stat.Nlink = 1
	stat.Չափս_2 = int32(չափս)
	stat.Blksize = 512
	stat.Արգելափակել = int32((չափս + 511) / 512)
	return 0
}

func sysstat(ոՒՂԻaddress uint32, stataddress uint32) int32 {
	if ոՒՂԻaddress == 0 {
		return Efault
	}
	if isԱրմատՈՒՂԻ(ոՒՂԻaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	անունlen, անուն := պատճենելՈՒՂԻ(ոՒՂԻaddress)
	if անունlen == 0 {
		return Enoent
	}
	չափս := ֆայլՉափս(անուն[:անունlen])
	if չափս == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < անունlen; i++ {
		inode = inode*33 + uint32(անուն[i])
	}
	return fillposixstat(stataddress, sifreg|0444, չափս, inode)
}

func sysfstat(ֆայլայինդեսկրիպտոր int32, stataddress uint32) int32 {
	entry := getԲացելՖայլ(ֆայլայինդեսկրիպտոր)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case ֆայլայինդեսկրիպտորkindstdin, ֆայլայինդեսկրիպտորkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(ֆայլայինդեսկրիպտոր+1))
	case ֆայլայինդեսկրիպտորkindԱրմատֆայլապանակ:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case ֆայլայինդեսկրիպտորkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.չափս, uint32(ֆայլայինդեսկրիպտոր+2))
	case ֆայլայինդեսկրիպտորkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(ֆայլայինդեսկրիպտոր+2))
	}
	return Ebadf
}

func sysfsync(ֆայլայինդեսկրիպտոր int32) int32 {
	if getԲացելՖայլ(ֆայլայինդեսկրիպտոր) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	գործընթաց := ensurecurrentԳործընթաց()
	if գործընթաց == nil {
		return 0
	}
	if գործընթաց.ծրագիրbreak == 0 {
		գործընթաց.ծրագիրbreak = օգտագործողheapbase
	}
	if address_2 == 0 {
		return գործընթաց.ծրագիրbreak
	}
	if address_2 < օգտագործողheapbase || address_2 > օգտագործողheaplimit {
		return գործընթաց.ծրագիրbreak
	}
	գործընթաց.ծրագիրbreak = address_2
	return գործընթաց.ծրագիրbreak
}

func պատճենելutsfield(destination *[65]byte, արժեք string) {
	limit := len(արժեք)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = արժեք[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	անուն := (*posixutsname)(Pointer(uintptr(address_2)))
	*անուն = posixutsname{}
	պատճենելutsfield(&անուն.Sysname, "EngOS")
	պատճենելutsfield(&անուն.Nodename, "engos")
	պատճենելutsfield(&անուն.Release, "0.1-posix")
	պատճենելutsfield(&անուն.Version, "POSIX.1-2017 phase 1")
	պատճենելutsfield(&անուն.Machine, "i386")
	return 0
}

func փոխանակությունunsignedinteger16(արժեք uint16) uint16 {
	return (արժեք << 8) | (արժեք >> 8)
}

func socketcallargument(arguments_2 uint32, ինդեքս uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + ինդեքս*4)))
}

func socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր int32) (*տեղայինdatagramsocket, int32) {
	entry := getԲացելՖայլ(ֆայլայինդեսկրիպտոր)
	if entry == nil || entry.kind != ֆայլայինդեսկրիպտորkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &տեղայինsockets[entry.aux]
	if !socket.օգտագործված {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketՏիպ uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketՏիպ != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	գործընթաց := ensurecurrentԳործընթաց()
	if գործընթաց == nil {
		return Enfile
	}
	socketԻնդեքս := -1
	for i := 0; i < maxsockets; i++ {
		if !տեղայինsockets[i].օգտագործված {
			socketԻնդեքս = i
			break
		}
	}
	if socketԻնդեքս < 0 {
		return Enfile
	}
	նկարագրություն := allocateԲացելՖայլ()
	if նկարագրություն < 0 {
		return նկարագրություն
	}
	տեղայինsockets[socketԻնդեքս] = տեղայինdatagramsocket{օգտագործված: true}
	entry := &բացելՖայլԱղյուսակ[նկարագրություն]
	entry.kind = ֆայլայինդեսկրիպտորkindsocket
	entry.դրոշներ = oԸնթերցումԳրել
	entry.aux = uint32(socketԻնդեքս)
	ֆայլայինդեսկրիպտոր := allocateՖայլայինդեսկրիպտոր(գործընթաց, նկարագրություն, 3)
	if ֆայլայինդեսկրիպտոր < 0 {
		տեղայինsockets[socketԻնդեքս] = տեղայինdatagramsocket{}
		*entry = բացելՖայլՆկարագրություն{}
		return ֆայլայինդեսկրիպտոր
	}
	return ֆայլայինդեսկրիպտոր
}

func socketaddress(address_2 uint32, երկարություն uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if երկարություն < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func պորտՄեջuse(պորտ uint16, except *տեղայինdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &տեղայինsockets[i]
		if socket != except && socket.օգտագործված && socket.bound && socket.տեղային.Պորտ == պորտ {
			return true
		}
	}
	return false
}

func bindephemeral(socket *տեղայինdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		պորտ := փոխանակությունunsignedinteger16(հաջորդephemeralՊորտ)
		հաջորդephemeralՊորտ++
		if հաջորդephemeralՊորտ < 49152 {
			հաջորդephemeralՊորտ = 49152
		}
		if !պորտՄեջuse(պորտ, socket) {
			socket.տեղային = socketaddressipv4{Family: afinet, Պորտ: պորտ, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(ֆայլայինդեսկրիպտոր int32, address_2 uint32, երկարություն uint32) int32 {
	socket, err := socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, երկարություն)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Պորտ == 0 {
		return bindephemeral(socket)
	}
	if պորտՄեջuse(requested.Պորտ, socket) {
		return Eaddrinuse
	}
	socket.տեղային = *requested
	socket.bound = true
	return 0
}

func socketՄիացնել(ֆայլայինդեսկրիպտոր int32, address_2 uint32, երկարություն uint32) int32 {
	socket, err := socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, երկարություն)
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

func socketՈՒղարկելto(ֆայլայինդեսկրիպտոր int32, bufferaddress_2 uint32, երկարություն uint32, destinationaddress uint32, destinationԵրկարություն uint32) int32 {
	socket, err := socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր)
	if err != 0 {
		return err
	}
	if երկարություն > maxdatagramՉափս {
		return Emsgsize
	}
	if երկարություն != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressՍխալ := socketaddress(destinationaddress, destinationԵրկարություն)
		if addressՍխալ != 0 {
			return addressՍխալ
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindՍխալ := bindephemeral(socket); bindՍխալ != 0 {
			return bindՍխալ
		}
	}
	var receiver *տեղայինdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &տեղայինsockets[i]
		if candidate.օգտագործված && candidate.bound && candidate.տեղային.Պորտ == destination.Պորտ &&
			(candidate.տեղային.Address == 0 || candidate.տեղային.Address == destination.Address) {
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
	*packet = socketpacket{օգտագործված: true, չափս: երկարություն, աղբյուր: socket.տեղային}
	if երկարություն != 0 {
		աղբյուր := GetԲայթերիցՑուցիչ(uintptr(bufferaddress_2), int(երկարություն), int(երկարություն))
		copy(packet.data[:երկարություն], աղբյուր)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(երկարություն)
}

func socketreceiveից(ֆայլայինդեսկրիպտոր int32, bufferaddress_2 uint32, երկարություն uint32, աղբյուրaddress uint32, աղբյուրԵրկարությունaddress uint32) int32 {
	socket, err := socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր)
	if err != 0 {
		return err
	}
	if երկարություն != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	պատճենելԵրկարություն := packet.չափս
	if պատճենելԵրկարություն > երկարություն {
		պատճենելԵրկարություն = երկարություն
	}
	if պատճենելԵրկարություն != 0 {
		destination := GetԲայթերիցՑուցիչ(uintptr(bufferaddress_2), int(պատճենելԵրկարություն), int(պատճենելԵրկարություն))
		copy(destination, packet.data[:պատճենելԵրկարություն])
	}
	if աղբյուրaddress != 0 {
		if աղբյուրԵրկարությունaddress == 0 {
			return Efault
		}
		providedԵրկարություն := (*uint32)(Pointer(uintptr(աղբյուրԵրկարությունaddress)))
		if *providedԵրկարություն >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(աղբյուրaddress))) = packet.աղբյուր
		}
		*providedԵրկարություն = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(պատճենելԵրկարություն)
}

func պատճենելsocketԱնուն(ֆայլայինդեսկրիպտոր int32, address_2 uint32, երկարությունaddress uint32, peer bool) int32 {
	socket, err := socketforՖայլայինդեսկրիպտոր(ֆայլայինդեսկրիպտոր)
	if err != 0 {
		return err
	}
	if address_2 == 0 || երկարությունaddress == 0 {
		return Efault
	}
	երկարություն := (*uint32)(Pointer(uintptr(երկարությունaddress)))
	if *երկարություն < 16 {
		*երկարություն = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindՍխալ := bindephemeral(socket); bindՍխալ != 0 {
				return bindՍխալ
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.տեղային
	}
	*երկարություն = 16
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
		return socketՄիացնել(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return պատճենելsocketԱնուն(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return պատճենելsocketԱնուն(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
	case 9:
		return socketՈՒղարկելto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 10:
		return socketreceiveից(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), 0, 0)
	case 11:
		return socketՈՒղարկելto(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 12:
		return socketreceiveից(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), socketcallargument(arguments_2, 4), socketcallargument(arguments_2, 5))
	case 13:
		if _, err := socketforՖայլայինդեսկրիպտոր(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketforՖայլայինդեսկրիպտոր(int32(socketcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func ընթերցումstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetԲայթերիցՑուցիչ(uintptr(address), int(count), int(count))
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
	հաջորդ := (stdinԳրել + 1) % uint32(len(stdinbuffer))
	if հաջորդ == stdinԸնթերցում {
		return
	}
	stdinbuffer[stdinԳրել] = c
	stdinԳրել = հաջորդ
}

func stdingetblocking() byte {
	for stdinԸնթերցում == stdinԳրել {
		sc := pollՍտեղնաշարscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinԸնթերցում]
	stdinԸնթերցում = (stdinԸնթերցում + 1) % uint32(len(stdinbuffer))
	return c
}

func pollՍտեղնաշարscancode() byte {
	for (ՊորտԸնթերցումbyte(0x64) & 0x01) == 0 {
	}
	sc := ՊորտԸնթերցումbyte(0x60)
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

func պատճենելexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for ինդեքս := uint32(0); ինդեքս < maxexecvectorentry; ինդեքս++ {
		տՈՂaddress := *(*uint32)(Pointer(uintptr(address_2 + ինդեքս*4)))
		if տՈՂaddress == 0 {
			result.count = ինդեքս
			return 0
		}
		terminated := false
		for երկարություն := uint32(0); երկարություն <= maxexecՏՈՂԵրկարություն; երկարություն++ {
			արժեք := *(*byte)(Pointer(uintptr(տՈՂaddress + երկարություն)))
			result.values[ինդեքս][երկարություն] = արժեք
			if արժեք == 0 {
				result.lengths[ինդեքս] = երկարություն
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

func pushexecunsignedinteger32(stack *uint32, արժեք uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = արժեք
}

func setupexecstack(կՄՀ *TcpuՎիճակ, arguments_2 *execvector, environment *execvector) int32 {
	const stackԲայթեր uint32 = 4096
	if !MakeՄիջակայքprivatewritable(getcr3(), ՕգտագործողstackՎերև-stackԲայթեր, stackԲայթեր) {
		return Enomem
	}
	stack := ՕգտագործողstackՎերև
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		երկարություն := environment.lengths[i] + 1
		stack -= երկարություն
		destination := GetԲայթերիցՑուցիչ(uintptr(stack), int(երկարություն), int(երկարություն))
		copy(destination, environment.values[i][:երկարություն])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		երկարություն := arguments_2.lengths[i] + 1
		stack -= երկարություն
		destination := GetԲայթերիցՑուցիչ(uintptr(stack), int(երկարություն), int(երկարություն))
		copy(destination, arguments_2.values[i][:երկարություն])
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
	կՄՀ.Esp = stack
	կՄՀ.Ebp = 0
	return 0
}

func փակելՄիացնելexec(գործընթաց *գործընթացentry) {
	if գործընթաց == nil {
		return
	}
	for ֆայլայինդեսկրիպտոր := int32(0); ֆայլայինդեսկրիպտոր < maxՖայլայինդեսկրիպտոր; ֆայլայինդեսկրիպտոր++ {
		if գործընթաց.fds[ֆայլայինդեսկրիպտոր].օգտագործված && (գործընթաց.fds[ֆայլայինդեսկրիպտոր].ֆայլայինդեսկրիպտորԴրոշներ&ֆայլայինդեսկրիպտորcloexec) != 0 {
			փակելԳործընթացՖայլայինդեսկրիպտոր(գործընթաց, ֆայլայինդեսկրիպտոր)
		}
	}
}

func sysexecve(կՄՀ *TcpuՎիճակ, ոՒՂԻaddress uint32) int32 {
	if ոՒՂԻaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := պատճենելexecvector(կՄՀ.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := պատճենելexecvector(կՄՀ.Edx, &environment); result < 0 {
		return result
	}
	անունlen, անուն := պատճենելՈՒՂԻ(ոՒՂԻaddress)
	if անունlen == 0 {
		return Enoent
	}
	չափս := ֆայլՉափս(անուն[:անունlen])
	if չափս == 0 {
		return Enoent
	}
	հիշողությունmanager := &mem.TՀիշողությունmanager{}
	ֆայլՑուցիչ := հիշողությունmanager.Malloc(չափս)
	if ֆայլՑուցիչ == nil {
		return Einval
	}
	data := GetԲայթերիցՑուցիչ(uintptr(ֆայլՑուցիչ), int(չափս), int(չափս))
	ընթերցումՖայլ(անուն[:անունlen], data)
	if չափս < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		հիշողությունmanager.Ազատ(ֆայլՑուցիչ)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	հիշողությունmanager.Ազատ(ֆայլՑուցիչ)
	if result := setupexecstack(կՄՀ, &arguments_2, &environment); result < 0 {
		return result
	}
	փակելՄիացնելexec(ensurecurrentԳործընթաց())
	կՄՀ.Eip = entry
	կՄՀ.Eax = 0
	return 0
}

func sysfork(կՄՀ *TcpuՎիճակ) int32 {
	ծնողpid := Currentpid()
	if ensurecurrentԳործընթաց() == nil {
		return Enfile
	}
	pid := allocateԳործընթաց(ծնողpid)
	if pid == 0 {
		return Einval
	}
	հիշողությունmanager := &mem.TՀիշողությունmanager{}
	threadՑուցիչ := հիշողությունmanager.Malloc(uint32(Sizeof(TThread{})))
	stackՑուցիչ := հիշողությունmanager.Malloc(ThreadstackՉափս)
	երեխաԷջֆայլապանակ := CloneaddressԲացատcow(getcr3())
	if threadՑուցիչ == nil || stackՑուցիչ == nil || երեխաԷջֆայլապանակ == 0 {
		discardԳործընթաց(pid)
		return Einval
	}
	երեխա := (*TThread)(threadՑուցիչ)
	երեխա.Stack = uint32(uintptr(stackՑուցիչ))
	երեխա.ԿՄՀՎիճակ = (*TcpuՎիճակ)(Pointer(uintptr(stackՑուցիչ) + ThreadstackՉափս - Sizeof(TcpuՎիճակ{})))
	*երեխա.ԿՄՀՎիճակ = *կՄՀ
	երեխա.ԿՄՀՎիճակ.Eax = 0
	երեխա.Օգտագործողstack_2 = կՄՀ.Esp
	երեխա.ՕգտագործողstackՉափս_2 = 0
	երեխա.Pid = pid
	երեխա.Ծնողpid = ծնողpid
	երեխա.Էջֆայլապանակentry = երեխաԷջֆայլապանակ
	երեխա.ThreadՎիճակ = Պատրաստ
	երեխա.Fpuoffset = 0xffffffff
	երեխա.Iskernel = false
	Ավելացնելrunnablethread(երեխա)
	return int32(pid)
}

func sysexit(կարգավիճակ uint32) {
	pid := Currentpid()
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		if գործընթացԱղյուսակ[i].օգտագործված && գործընթացԱղյուսակ[i].pid == pid {
			փակելԲոլորըԳործընթացfds(&գործընթացԱղյուսակ[i])
			գործընթացԱղյուսակ[i].exited = true
			գործընթացԱղյուսակ[i].կարգավիճակ = (կարգավիճակ & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, կարգավիճակaddress uint32, տարբերակներ uint32) int32 {
	if (տարբերակներ & ^uint32(1)) != 0 {
		return Einval
	}
	ծնողpid := Currentpid()
	foundերեխա := false
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		p := &գործընթացԱղյուսակ[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.օգտագործված && matches && p.ծնող == ծնողpid {
			foundերեխա = true
			if p.exited {
				if կարգավիճակaddress != 0 {
					*(*uint32)(Pointer(uintptr(կարգավիճակaddress))) = p.կարգավիճակ
				}
				երեխաpid := p.pid
				*p = գործընթացentry{}
				return int32(երեխաpid)
			}
		}
	}
	if !foundերեխա {
		return Echild
	}

	if (տարբերակներ & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateԳործընթաց(ծնող uint32) uint32 {
	ծնողԳործընթաց := գտնելԳործընթաց(ծնող)
	pid := Allocatepid()
	for i := 0; i < len(գործընթացԱղյուսակ); i++ {
		if !գործընթացԱղյուսակ[i].օգտագործված {
			գործընթացԱղյուսակ[i] = գործընթացentry{
				օգտագործված:	true,
				pid:		pid,
				ծնող:		ծնող,
				ծրագիրbreak:	օգտագործողheapbase,
			}
			if ծնողԳործընթաց != nil {
				գործընթացԱղյուսակ[i].ծրագիրbreak = ծնողԳործընթաց.ծրագիրbreak
				for ֆայլայինդեսկրիպտոր := 0; ֆայլայինդեսկրիպտոր < maxՖայլայինդեսկրիպտոր; ֆայլայինդեսկրիպտոր++ {
					if ծնողԳործընթաց.fds[ֆայլայինդեսկրիպտոր].օգտագործված {
						գործընթացԱղյուսակ[i].fds[ֆայլայինդեսկրիպտոր] = ծնողԳործընթաց.fds[ֆայլայինդեսկրիպտոր]
						նկարագրություն := ծնողԳործընթաց.fds[ֆայլայինդեսկրիպտոր].նկարագրություն
						if նկարագրություն >= 0 && նկարագրություն < maxԲացելfiles {
							բացելՖայլԱղյուսակ[նկարագրություն].refs++
						}
					}
				}
			} else {
				initializeԳործընթացfds(&գործընթացԱղյուսակ[i])
			}
			return pid
		}
	}
	return 0
}

func փակելԲոլորըԳործընթացfds(գործընթաց *գործընթացentry) {
	if գործընթաց == nil {
		return
	}
	for ֆայլայինդեսկրիպտոր := int32(0); ֆայլայինդեսկրիպտոր < maxՖայլայինդեսկրիպտոր; ֆայլայինդեսկրիպտոր++ {
		if գործընթաց.fds[ֆայլայինդեսկրիպտոր].օգտագործված {
			փակելԳործընթացՖայլայինդեսկրիպտոր(գործընթաց, ֆայլայինդեսկրիպտոր)
		}
	}
}

func discardԳործընթաց(pid uint32) {
	գործընթաց := գտնելԳործընթաց(pid)
	if գործընթաց == nil {
		return
	}
	փակելԲոլորըԳործընթացfds(գործընթաց)
	*գործընթաց = գործընթացentry{}
}

func պատճենելՈՒՂԻ(ոՒՂԻaddress uint32) (uint32, [12]byte) {
	var անուն [12]byte
	if ոՒՂԻaddress == 0 {
		return 0, անուն
	}
	raw := GetԲայթերիցՑուցիչ(uintptr(ոՒՂԻaddress), 64, 64)
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
		անուն[n] = c
		n++
	}
	return n, անուն
}

func ֆայլՉափս(ֆայլիանուն []byte) uint32 {
	var ata0s = TԸնդլայնվածՏեխնոլոգիաattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionԱղյուսակ{}
	partition.Ընթերցումpartition(&ata0s)

	bios := TBiosparameterԱրգելափակել32{}
	չափս := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն)
	ata0s.Flush()
	return չափս
}

func ընթերցումՖայլ(ֆայլիանուն []byte, data []byte) {
	var ata0s = TԸնդլայնվածՏեխնոլոգիաattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionԱղյուսակ{}
	partition.Ընթերցումpartition(&ata0s)

	bios := TBiosparameterԱրգելափակել32{}
	bios.Ընթերցում(&ata0s, partition.Mbr.Primarypartition[0], ֆայլիանուն, data)
	ata0s.Flush()
}

func getcr3() uint32
