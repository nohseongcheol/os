package ระบบcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "fileระบบ/msdospartition"
import . "fileระบบ/fat"
import . "fileระบบ/elf"
import mem "memorymanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualmemory"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	Sysan		uint32	= 3
	Syskhian	uint32	= 4
	Sysopen		uint32	= 5
	Sysclose	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaccess	uint32	= 33
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
	maxopenfiles		= 128
)

type fdentry struct {
	used		bool
	คำบรรยาย	int32
	fdflags		uint32
}

type openfileคำบรรยาย struct {
	used		bool
	refs		uint32
	kind		uint32
	flags		uint32
	position	uint32
	ขนาด		uint32
	name		[12]byte
	namelen		uint32
	aux		uint32
}

const (
	fdkindnone		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindรากdirectory	uint32	= 4
	fdkindsocket		uint32	= 5

	oanonly		uint32	= 0
	okhianonly	uint32	= 1
	oankhian	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	odirectory	uint32	= 0x10000

	seekกำหนด	uint32	= 0
	seekcurrent	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fกำหนดfd	uint32	= 2
	fgetfl		uint32	= 3
	fกำหนดfl	uint32	= 4
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
	maxdatagramขนาด		= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	used	bool
	ขนาด	uint32
	source	socketaddressipv4
	data	[maxdatagramขนาด]byte
}

type localdatagramsocket struct {
	used		bool
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
	Device		uint32
	Ino		uint32
	Mโหมด		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sขนาด_2		int32
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
	maxประมวลผลvectorentry		= 16
	maxประมวลผลstringความยาว	= 63
)

type ประมวลผลvector struct {
	count	uint32
	lengths	[maxประมวลผลvectorentry]uint32
	values	[maxประมวลผลvectorentry][maxประมวลผลstringความยาว + 1]byte
}

type โพรเซสentry struct {
	used		bool
	pid		uint32
	parent		uint32
	exited		bool
	สถานะ		uint32
	โปรแกรมbreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallerror(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var openfileตาราง [maxopenfiles]openfileคำบรรยาย
var โพรเซสตาราง [32]โพรเซสentry
var localsockets [maxsockets]localdatagramsocket
var nextephemeralport uint16 = 49152

const (
	userheapbase	uint32	= 0x06000000
	userheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinan uint32
var stdinkhian uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func Sysan_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysan, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysprintstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(Syskhian, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysprintunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Syskhian, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysopen_2(พาธ uintptr, flags uint32, โหมด uint32) int32 {
	return int32(Syscall(Sysopen, uint32(พาธ), flags, โหมด))
}

func Sysclose_2(fd uint32) int32 {
	return int32(Syscall(Sysclose, fd))
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
		return syscallerror(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initfiledescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpuสถานะ)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Stopcurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Stopcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysan:
		cpu.Eax = uint32(sysan(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Syskhian:
		cpu.Eax = uint32(syskhian(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysopen:
		cpu.Eax = uint32(sysopen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysopen(cpu.Ebx, ocreate|okhianonly|otruncate, cpu.Ecx))
		return esp
	case Sysclose:
		cpu.Eax = uint32(sysclose(int32(cpu.Ebx)))
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
	case Sysaccess:
		cpu.Eax = uint32(sysaccess(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32print(cpu.Ebx)
		return esp

	default:
		console_2.MPrintxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32print(esp)
		console_2.MPrint(([]byte)(":"))
		console_2.MUnsignedinteger32print(cpu.Eax)
		console_2.MPrint(([]byte)(":"))
		console_2.MUnsignedinteger32print(cpu.Ebx)
		console_2.MPrint(([]byte)(":"))
		console_2.MUnsignedinteger32print(cpu.Ecx)
		console_2.MPrint(([]byte)(":"))
		console_2.MUnsignedinteger32print(cpu.Edx)
		console_2.MPrint(([]byte)("]"))
		cpu.Eax = syscallerror(Enosys)
		return esp
	}

	return esp
}

func initfiledescriptor() {
	for i := 0; i < maxopenfiles; i++ {
		openfileตาราง[i] = openfileคำบรรยาย{}
	}
	for i := 0; i < len(โพรเซสตาราง); i++ {
		โพรเซสตาราง[i] = โพรเซสentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	nextephemeralport = 49152
	openfileตาราง[0] = openfileคำบรรยาย{used: true, kind: fdkindstdin, flags: oanonly}
	openfileตาราง[1] = openfileคำบรรยาย{used: true, kind: fdkindconsole, flags: okhianonly}
	openfileตาราง[2] = openfileคำบรรยาย{used: true, kind: fdkindconsole, flags: okhianonly}
}

func หาโพรเซส(pid uint32) *โพรเซสentry {
	for i := 0; i < len(โพรเซสตาราง); i++ {
		if โพรเซสตาราง[i].used && โพรเซสตาราง[i].pid == pid {
			return &โพรเซสตาราง[i]
		}
	}
	return nil
}

func initializeโพรเซสfds(โพรเซส *โพรเซสentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		โพรเซส.fds[fd] = fdentry{used: true, คำบรรยาย: fd}
		openfileตาราง[fd].refs++
	}
}

func ensurecurrentโพรเซส() *โพรเซสentry {
	pid := Currentpid()
	if โพรเซส := หาโพรเซส(pid); โพรเซส != nil {
		return โพรเซส
	}
	for i := 0; i < len(โพรเซสตาราง); i++ {
		if !โพรเซสตาราง[i].used {
			โพรเซสตาราง[i] = โพรเซสentry{
				used:	true,
				pid:	pid,
				parent:	Currentparentpid(),
				โปรแกรมbreak:	userheapbase,
			}
			initializeโพรเซสfds(&โพรเซสตาราง[i])
			return &โพรเซสตาราง[i]
		}
	}
	return nil
}

func getopenfilefor(โพรเซส *โพรเซสentry, fd int32) *openfileคำบรรยาย {
	if โพรเซส == nil || fd < 0 || fd >= maxfd || !โพรเซส.fds[fd].used {
		return nil
	}
	คำบรรยาย := โพรเซส.fds[fd].คำบรรยาย
	if คำบรรยาย < 0 || คำบรรยาย >= maxopenfiles || !openfileตาราง[คำบรรยาย].used {
		return nil
	}
	return &openfileตาราง[คำบรรยาย]
}

func getopenfile(fd int32) *openfileคำบรรยาย {
	return getopenfilefor(ensurecurrentโพรเซส(), fd)
}

func allocateopenfile() int32 {
	for i := int32(3); i < maxopenfiles; i++ {
		if !openfileตาราง[i].used {
			openfileตาราง[i] = openfileคำบรรยาย{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(โพรเซส *โพรเซสentry, คำบรรยาย int32, minimum int32) int32 {
	if โพรเซส == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !โพรเซส.fds[fd].used {
			โพรเซส.fds[fd] = fdentry{used: true, คำบรรยาย: คำบรรยาย}
			return fd
		}
	}
	return Emfile
}

func releaseopenfile(คำบรรยาย int32) {
	if คำบรรยาย < 0 || คำบรรยาย >= maxopenfiles {
		return
	}
	entry := &openfileตาราง[คำบรรยาย]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && คำบรรยาย > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = openfileคำบรรยาย{}
	}
}

func closeโพรเซสfd(โพรเซส *โพรเซสentry, fd int32) int32 {
	if โพรเซส == nil || getopenfilefor(โพรเซส, fd) == nil {
		return Ebadf
	}
	คำบรรยาย := โพรเซส.fds[fd].คำบรรยาย
	โพรเซส.fds[fd] = fdentry{}
	releaseopenfile(คำบรรยาย)
	return 0
}

func syskhian(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getopenfile(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindรากdirectory {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getbytesfrompointer(uintptr(address), int(count), int(count))
	console_2.MPrint(buffer)
	return int32(count)
}

func sysan(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getopenfile(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return anstdin(address, count)
	}
	if entry.kind == fdkindรากdirectory {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.ขนาด {
		return 0
	}
	remaining := entry.ขนาด - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := Getbytesfrompointer(uintptr(address), int(count), int(count))
	return anvfsfile(entry, buffer, count)
}

func sysopen(พาธaddress uint32, flags uint32, โหมด uint32) int32 {
	_ = โหมด
	if พาธaddress == 0 {
		return Efault
	}
	accessโหมด := flags & 3
	if accessโหมด == okhianonly || accessโหมด == oankhian || (flags&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	โพรเซส := ensurecurrentโพรเซส()
	if โพรเซส == nil {
		return Enfile
	}
	คำบรรยาย := allocateopenfile()
	if คำบรรยาย < 0 {
		return คำบรรยาย
	}
	entry := &openfileตาราง[คำบรรยาย]
	entry.flags = flags
	if isรากพาธ(พาธaddress) {
		entry.kind = fdkindรากdirectory
		entry.ขนาด = 0
	} else {
		namelen, name := copyพาธ(พาธaddress)
		if namelen == 0 {
			*entry = openfileคำบรรยาย{}
			return Enoent
		}
		ขนาด := fileขนาด(name[:namelen])
		if ขนาด == 0 {
			*entry = openfileคำบรรยาย{}
			return Enoent
		}
		if (flags & odirectory) != 0 {
			*entry = openfileคำบรรยาย{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.ขนาด = ขนาด
		entry.namelen = namelen
		entry.name = name
	}

	fd := allocatefd(โพรเซส, คำบรรยาย, 3)
	if fd < 0 {
		*entry = openfileคำบรรยาย{}
		return fd
	}
	return fd
}

func sysclose(fd int32) int32 {
	return closeโพรเซสfd(ensurecurrentโพรเซส(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	โพรเซส := ensurecurrentโพรเซส()
	entry := getopenfilefor(โพรเซส, fd)
	if entry == nil {
		return Ebadf
	}
	newfd := allocatefd(โพรเซส, โพรเซส.fds[fd].คำบรรยาย, minimum)
	if newfd >= 0 {
		entry.refs++
	}
	return newfd
}

func sysdup2(oldfd int32, newfd int32) int32 {
	โพรเซส := ensurecurrentโพรเซส()
	entry := getopenfilefor(โพรเซส, oldfd)
	if entry == nil {
		return Ebadf
	}
	if newfd < 0 || newfd >= maxfd {
		return Ebadf
	}
	if oldfd == newfd {
		return newfd
	}
	if โพรเซส.fds[newfd].used {
		closeโพรเซสfd(โพรเซส, newfd)
	}
	โพรเซส.fds[newfd] = fdentry{used: true, คำบรรยาย: โพรเซส.fds[oldfd].คำบรรยาย}
	entry.refs++
	return newfd
}

func sysfcntl(fd int32, command uint32, argument uint32) int32 {
	โพรเซส := ensurecurrentโพรเซส()
	entry := getopenfilefor(โพรเซส, fd)
	if entry == nil {
		return Ebadf
	}
	switch command {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(โพรเซส.fds[fd].fdflags)
	case fกำหนดfd:
		โพรเซส.fds[fd].fdflags = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.flags)
	case fกำหนดfl:
		entry.flags = (entry.flags & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getopenfile(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekกำหนด:
		base = 0
	case seekcurrent:
		base = int64(entry.position)
	case seekend:
		base = int64(entry.ขนาด)
	default:
		return Einval
	}
	position_2 := base + int64(offset)
	if position_2 < 0 || position_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.position = uint32(position_2)
	return int32(entry.position)
}

func anvfsfile(entry *openfileคำบรรยาย, ปลายทาง_2 []byte, count uint32) int32 {
	memorymanager := &mem.TMemorymanager{}
	tmppointer := memorymanager.Malloc(entry.ขนาด)
	if tmppointer == nil {
		return Einval
	}
	tmp := Getbytesfrompointer(uintptr(tmppointer), int(entry.ขนาด), int(entry.ขนาด))
	anfile(entry.name[:entry.namelen], tmp)
	copy(ปลายทาง_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	memorymanager.Free(tmppointer)
	return int32(count)
}

func isรากพาธ(พาธaddress uint32) bool {
	if พาธaddress == 0 {
		return false
	}
	พาธ := Getbytesfrompointer(uintptr(พาธaddress), 4, 4)
	if พาธ[0] == '/' && พาธ[1] == 0 {
		return true
	}
	if พาธ[0] == '.' && พาธ[1] == 0 {
		return true
	}
	if พาธ[0] == '/' && พาธ[1] == '.' && พาธ[2] == 0 {
		return true
	}
	return false
}

func sysaccess(พาธaddress uint32, โหมด uint32) int32 {
	if พาธaddress == 0 {
		return Efault
	}
	if (โหมด & ^uint32(7)) != 0 {
		return Einval
	}
	isราก := isรากพาธ(พาธaddress)
	exists := isราก
	if !exists {
		namelen, name := copyพาธ(พาธaddress)
		exists = namelen != 0 && fileขนาด(name[:namelen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (โหมด & 2) != 0 {
		return Eacces
	}

	if (โหมด&1) != 0 && !isราก {
		return Eacces
	}
	return 0
}

func syschdir(พาธaddress uint32) int32 {
	if พาธaddress == 0 {
		return Efault
	}
	if !isรากพาธ(พาธaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, ขนาด uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if ขนาด < 2 {
		return Erange
	}
	buffer_2 := Getbytesfrompointer(uintptr(bufferaddress), int(ขนาด), int(ขนาด))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, โหมด uint32, ขนาด uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Device = 1
	stat.Ino = inode
	stat.Mโหมด = โหมด
	stat.Nlink = 1
	stat.Sขนาด_2 = int32(ขนาด)
	stat.Blksize = 512
	stat.Block = int32((ขนาด + 511) / 512)
	return 0
}

func sysstat(พาธaddress uint32, stataddress uint32) int32 {
	if พาธaddress == 0 {
		return Efault
	}
	if isรากพาธ(พาธaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	namelen, name := copyพาธ(พาธaddress)
	if namelen == 0 {
		return Enoent
	}
	ขนาด := fileขนาด(name[:namelen])
	if ขนาด == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < namelen; i++ {
		inode = inode*33 + uint32(name[i])
	}
	return fillposixstat(stataddress, sifreg|0444, ขนาด, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getopenfile(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindรากdirectory:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.ขนาด, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getopenfile(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	โพรเซส := ensurecurrentโพรเซส()
	if โพรเซส == nil {
		return 0
	}
	if โพรเซส.โปรแกรมbreak == 0 {
		โพรเซส.โปรแกรมbreak = userheapbase
	}
	if address_2 == 0 {
		return โพรเซส.โปรแกรมbreak
	}
	if address_2 < userheapbase || address_2 > userheaplimit {
		return โพรเซส.โปรแกรมbreak
	}
	โพรเซส.โปรแกรมbreak = address_2
	return โพรเซส.โปรแกรมbreak
}

func copyutsfield(ปลายทาง *[65]byte, value string) {
	limit := len(value)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		ปลายทาง[i] = value[i]
	}
	ปลายทาง[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	name := (*posixutsname)(Pointer(uintptr(address_2)))
	*name = posixutsname{}
	copyutsfield(&name.Sysname, "EngOS")
	copyutsfield(&name.Nodename, "engos")
	copyutsfield(&name.Release, "0.1-posix")
	copyutsfield(&name.Version, "POSIX.1-2017 phase 1")
	copyutsfield(&name.Machine, "i386")
	return 0
}

func swapunsignedinteger16(value uint16) uint16 {
	return (value << 8) | (value >> 8)
}

func socketcallargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getopenfile(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.used {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(โดเมน uint32, socketประเภท uint32, protocol uint32) int32 {
	if โดเมน != afinet {
		return Eafnosupport
	}
	if socketประเภท != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	โพรเซส := ensurecurrentโพรเซส()
	if โพรเซส == nil {
		return Enfile
	}
	socketindex := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].used {
			socketindex = i
			break
		}
	}
	if socketindex < 0 {
		return Enfile
	}
	คำบรรยาย := allocateopenfile()
	if คำบรรยาย < 0 {
		return คำบรรยาย
	}
	localsockets[socketindex] = localdatagramsocket{used: true}
	entry := &openfileตาราง[คำบรรยาย]
	entry.kind = fdkindsocket
	entry.flags = oankhian
	entry.aux = uint32(socketindex)
	fd := allocatefd(โพรเซส, คำบรรยาย, 3)
	if fd < 0 {
		localsockets[socketindex] = localdatagramsocket{}
		*entry = openfileคำบรรยาย{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, ความยาว uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if ความยาว < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portขยายuse(port uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.used && socket.bound && socket.local.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(nextephemeralport)
		nextephemeralport++
		if nextephemeralport < 49152 {
			nextephemeralport = 49152
		}
		if !portขยายuse(port, socket) {
			socket.local = socketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, ความยาว uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, ความยาว)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(socket)
	}
	if portขยายuse(requested.Port, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketconnect(fd int32, address_2 uint32, ความยาว uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, ความยาว)
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

func socketsendto(fd int32, bufferaddress_2 uint32, ความยาว uint32, ปลายทางaddress uint32, ปลายทางความยาว uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if ความยาว > maxdatagramขนาด {
		return Emsgsize
	}
	if ความยาว != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var ปลายทาง socketaddressipv4
	if ปลายทางaddress != 0 {
		address_2, addresserror := socketaddress(ปลายทางaddress, ปลายทางความยาว)
		if addresserror != 0 {
			return addresserror
		}
		ปลายทาง = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		ปลายทาง = socket.remote
	}
	if !socket.bound {
		if binderror := bindephemeral(socket); binderror != 0 {
			return binderror
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.used && candidate.bound && candidate.local.Port == ปลายทาง.Port &&
			(candidate.local.Address == 0 || candidate.local.Address == ปลายทาง.Address) {
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
	*packet = socketpacket{used: true, ขนาด: ความยาว, source: socket.local}
	if ความยาว != 0 {
		source := Getbytesfrompointer(uintptr(bufferaddress_2), int(ความยาว), int(ความยาว))
		copy(packet.data[:ความยาว], source)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(ความยาว)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, ความยาว uint32, sourceaddress uint32, sourceความยาวaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if ความยาว != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	copyความยาว := packet.ขนาด
	if copyความยาว > ความยาว {
		copyความยาว = ความยาว
	}
	if copyความยาว != 0 {
		ปลายทาง := Getbytesfrompointer(uintptr(bufferaddress_2), int(copyความยาว), int(copyความยาว))
		copy(ปลายทาง, packet.data[:copyความยาว])
	}
	if sourceaddress != 0 {
		if sourceความยาวaddress == 0 {
			return Efault
		}
		providedความยาว := (*uint32)(Pointer(uintptr(sourceความยาวaddress)))
		if *providedความยาว >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(sourceaddress))) = packet.source
		}
		*providedความยาว = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(copyความยาว)
}

func copysocketname(fd int32, address_2 uint32, ความยาวaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || ความยาวaddress == 0 {
		return Efault
	}
	ความยาว := (*uint32)(Pointer(uintptr(ความยาวaddress)))
	if *ความยาว < 16 {
		*ความยาว = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if binderror := bindephemeral(socket); binderror != 0 {
				return binderror
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*ความยาว = 16
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
		return socketconnect(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return copysocketname(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return copysocketname(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
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

func anstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getbytesfrompointer(uintptr(address), int(count), int(count))
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
	next := (stdinkhian + 1) % uint32(len(stdinbuffer))
	if next == stdinan {
		return
	}
	stdinbuffer[stdinkhian] = c
	stdinkhian = next
}

func stdingetblocking() byte {
	for stdinan == stdinkhian {
		sc := pollkeyboardscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinan]
	stdinan = (stdinan + 1) % uint32(len(stdinbuffer))
	return c
}

func pollkeyboardscancode() byte {
	for (Portanbyte(0x64) & 0x01) == 0 {
	}
	sc := Portanbyte(0x60)
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

func copyประมวลผลvector(address_2 uint32, result *ประมวลผลvector) int32 {
	*result = ประมวลผลvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxประมวลผลvectorentry; index++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if stringaddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for ความยาว := uint32(0); ความยาว <= maxประมวลผลstringความยาว; ความยาว++ {
			value := *(*byte)(Pointer(uintptr(stringaddress + ความยาว)))
			result.values[index][ความยาว] = value
			if value == 0 {
				result.lengths[index] = ความยาว
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

func pushประมวลผลunsignedinteger32(stack *uint32, value uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = value
}

func setupประมวลผลstack(cpu *Tcpuสถานะ, arguments_2 *ประมวลผลvector, environment *ประมวลผลvector) int32 {
	const stackbytes uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Userstackบน-stackbytes, stackbytes) {
		return Enomem
	}
	stack := Userstackบน
	var argumentpointers [maxประมวลผลvectorentry]uint32
	var environmentpointers [maxประมวลผลvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		ความยาว := environment.lengths[i] + 1
		stack -= ความยาว
		ปลายทาง := Getbytesfrompointer(uintptr(stack), int(ความยาว), int(ความยาว))
		copy(ปลายทาง, environment.values[i][:ความยาว])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		ความยาว := arguments_2.lengths[i] + 1
		stack -= ความยาว
		ปลายทาง := Getbytesfrompointer(uintptr(stack), int(ความยาว), int(ความยาว))
		copy(ปลายทาง, arguments_2.values[i][:ความยาว])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushประมวลผลunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushประมวลผลunsignedinteger32(&stack, environmentpointers[i])
	}
	pushประมวลผลunsignedinteger32(&stack, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushประมวลผลunsignedinteger32(&stack, argumentpointers[i])
	}
	pushประมวลผลunsignedinteger32(&stack, arguments_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func closeonประมวลผล(โพรเซส *โพรเซสentry) {
	if โพรเซส == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if โพรเซส.fds[fd].used && (โพรเซส.fds[fd].fdflags&fdcloexec) != 0 {
			closeโพรเซสfd(โพรเซส, fd)
		}
	}
}

func sysexecve(cpu *Tcpuสถานะ, พาธaddress uint32) int32 {
	if พาธaddress == 0 {
		return Efault
	}
	var arguments_2 ประมวลผลvector
	var environment ประมวลผลvector
	if result := copyประมวลผลvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := copyประมวลผลvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	namelen, name := copyพาธ(พาธaddress)
	if namelen == 0 {
		return Enoent
	}
	ขนาด := fileขนาด(name[:namelen])
	if ขนาด == 0 {
		return Enoent
	}
	memorymanager := &mem.TMemorymanager{}
	filepointer := memorymanager.Malloc(ขนาด)
	if filepointer == nil {
		return Einval
	}
	data := Getbytesfrompointer(uintptr(filepointer), int(ขนาด), int(ขนาด))
	anfile(name[:namelen], data)
	if ขนาด < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorymanager.Free(filepointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memorymanager.Free(filepointer)
	if result := setupประมวลผลstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	closeonประมวลผล(ensurecurrentโพรเซส())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpuสถานะ) int32 {
	parentpid := Currentpid()
	if ensurecurrentโพรเซส() == nil {
		return Enfile
	}
	pid := allocateโพรเซส(parentpid)
	if pid == 0 {
		return Einval
	}
	memorymanager := &mem.TMemorymanager{}
	threadpointer := memorymanager.Malloc(uint32(Sizeof(TThread{})))
	stackpointer := memorymanager.Malloc(Threadstackขนาด)
	childpagedirectory := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childpagedirectory == 0 {
		discardโพรเซส(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.Cpuสถานะ = (*Tcpuสถานะ)(Pointer(uintptr(stackpointer) + Threadstackขนาด - Sizeof(Tcpuสถานะ{})))
	*child.Cpuสถานะ = *cpu
	child.Cpuสถานะ.Eax = 0
	child.Userstack_2 = cpu.Esp
	child.Userstackขนาด_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pagedirectoryentry = childpagedirectory
	child.Threadสถานะ = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Addrunnablethread(child)
	return int32(pid)
}

func sysexit(สถานะ uint32) {
	pid := Currentpid()
	for i := 0; i < len(โพรเซสตาราง); i++ {
		if โพรเซสตาราง[i].used && โพรเซสตาราง[i].pid == pid {
			closeallโพรเซสfds(&โพรเซสตาราง[i])
			โพรเซสตาราง[i].exited = true
			โพรเซสตาราง[i].สถานะ = (สถานะ & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, สถานะaddress uint32, options uint32) int32 {
	if (options & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(โพรเซสตาราง); i++ {
		p := &โพรเซสตาราง[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.used && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if สถานะaddress != 0 {
					*(*uint32)(Pointer(uintptr(สถานะaddress))) = p.สถานะ
				}
				childpid := p.pid
				*p = โพรเซสentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (options & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateโพรเซส(parent uint32) uint32 {
	parentโพรเซส := หาโพรเซส(parent)
	pid := Allocatepid()
	for i := 0; i < len(โพรเซสตาราง); i++ {
		if !โพรเซสตาราง[i].used {
			โพรเซสตาราง[i] = โพรเซสentry{
				used:	true,
				pid:	pid,
				parent:	parent,
				โปรแกรมbreak:	userheapbase,
			}
			if parentโพรเซส != nil {
				โพรเซสตาราง[i].โปรแกรมbreak = parentโพรเซส.โปรแกรมbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentโพรเซส.fds[fd].used {
						โพรเซสตาราง[i].fds[fd] = parentโพรเซส.fds[fd]
						คำบรรยาย := parentโพรเซส.fds[fd].คำบรรยาย
						if คำบรรยาย >= 0 && คำบรรยาย < maxopenfiles {
							openfileตาราง[คำบรรยาย].refs++
						}
					}
				}
			} else {
				initializeโพรเซสfds(&โพรเซสตาราง[i])
			}
			return pid
		}
	}
	return 0
}

func closeallโพรเซสfds(โพรเซส *โพรเซสentry) {
	if โพรเซส == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if โพรเซส.fds[fd].used {
			closeโพรเซสfd(โพรเซส, fd)
		}
	}
}

func discardโพรเซส(pid uint32) {
	โพรเซส := หาโพรเซส(pid)
	if โพรเซส == nil {
		return
	}
	closeallโพรเซสfds(โพรเซส)
	*โพรเซส = โพรเซสentry{}
}

func copyพาธ(พาธaddress uint32) (uint32, [12]byte) {
	var name [12]byte
	if พาธaddress == 0 {
		return 0, name
	}
	raw := Getbytesfrompointer(uintptr(พาธaddress), 64, 64)
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
		name[n] = c
		n++
	}
	return n, name
}

func fileขนาด(filename []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionตาราง{}
	partition.Anpartition(&ata0s)

	bios := TBiosparameterblock32{}
	ขนาด := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()
	return ขนาด
}

func anfile(filename []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionตาราง{}
	partition.Anpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.An(&ata0s, partition.Mbr.Primarypartition[0], filename, data)
	ata0s.Flush()
}

func getcr3() uint32
