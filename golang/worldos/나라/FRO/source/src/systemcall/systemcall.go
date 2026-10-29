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
import . "fílasystem/msdospartition"
import . "fílasystem/fat"
import . "fílasystem/elf"
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
	Syslesa		uint32	= 3
	Sysskriva	uint32	= 4
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
	frágreiðing	int32
	fdflags		uint32
}

type openFílaFrágreiðing struct {
	used		bool
	refs		uint32
	kind		uint32
	flags		uint32
	position	uint32
	stødd		uint32
	navn		[12]byte
	navnlen		uint32
	aux		uint32
}

const (
	fdkindEingi		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindrootFíluskrá	uint32	= 4
	fdkindsocket		uint32	= 5

	olesaonly	uint32	= 0
	oskrivaonly	uint32	= 1
	olesaskriva	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oFíluskrá	uint32	= 0x10000

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
	maxsocketpakkar		= 8
	maxdatagramStødd	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	used	bool
	stødd	uint32
	source	socketaddressipv4
	data	[maxdatagramStødd]byte
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
	pakkar		[maxsocketpakkar]socketpacket
}

type posixstat struct {
	Device		uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Stødd_2		int32
	Blksize		int32
	Blokkur		int32
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
	maxexecstringLongd	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecstringLongd + 1]byte
}

type processentry struct {
	used		bool
	pid		uint32
	parent		uint32
	exited		bool
	status		uint32
	programbreak	uint32
	fds		[maxfd]fdentry
}

type stringheader struct {
	Data	uintptr
	Len	int
}

func syscallBrek(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var openFílatable [maxopenfiles]openFílaFrágreiðing
var processtable [32]processentry
var localsockets [maxsockets]localdatagramsocket
var næstaephemeralport uint16 = 49152

const (
	brúkariheapbase		uint32	= 0x06000000
	brúkariheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinlesa uint32
var stdinskriva uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func Syslesa_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Syslesa, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysprintstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(Sysskriva, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysprintunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysskriva, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysopen_2(path uintptr, flags uint32, mode uint32) int32 {
	return int32(Syscall(Sysopen, uint32(path), flags, mode))
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
		return syscallBrek(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initFíladescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*TcpuStøða)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Steðgacurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Steðgacurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Syslesa:
		cpu.Eax = uint32(syslesa(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysskriva:
		cpu.Eax = uint32(sysskriva(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysopen:
		cpu.Eax = uint32(sysopen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysopen(cpu.Ebx, ocreate|oskrivaonly|otruncate, cpu.Ecx))
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
		cpu.Eax = syscallBrek(Enosys)
		return esp
	}

	return esp
}

func initFíladescriptor() {
	for i := 0; i < maxopenfiles; i++ {
		openFílatable[i] = openFílaFrágreiðing{}
	}
	for i := 0; i < len(processtable); i++ {
		processtable[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	næstaephemeralport = 49152
	openFílatable[0] = openFílaFrágreiðing{used: true, kind: fdkindstdin, flags: olesaonly}
	openFílatable[1] = openFílaFrágreiðing{used: true, kind: fdkindconsole, flags: oskrivaonly}
	openFílatable[2] = openFílaFrágreiðing{used: true, kind: fdkindconsole, flags: oskrivaonly}
}

func findprocess(pid uint32) *processentry {
	for i := 0; i < len(processtable); i++ {
		if processtable[i].used && processtable[i].pid == pid {
			return &processtable[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{used: true, frágreiðing: fd}
		openFílatable[fd].refs++
	}
}

func ensurecurrentprocess() *processentry {
	pid := Currentpid()
	if process := findprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].used {
			processtable[i] = processentry{
				used:		true,
				pid:		pid,
				parent:		Currentparentpid(),
				programbreak:	brúkariheapbase,
			}
			initializeprocessfds(&processtable[i])
			return &processtable[i]
		}
	}
	return nil
}

func getopenFílafor(process *processentry, fd int32) *openFílaFrágreiðing {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].used {
		return nil
	}
	frágreiðing := process.fds[fd].frágreiðing
	if frágreiðing < 0 || frágreiðing >= maxopenfiles || !openFílatable[frágreiðing].used {
		return nil
	}
	return &openFílatable[frágreiðing]
}

func getopenFíla(fd int32) *openFílaFrágreiðing {
	return getopenFílafor(ensurecurrentprocess(), fd)
}

func allocateopenFíla() int32 {
	for i := int32(3); i < maxopenfiles; i++ {
		if !openFílatable[i].used {
			openFílatable[i] = openFílaFrágreiðing{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, frágreiðing int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].used {
			process.fds[fd] = fdentry{used: true, frágreiðing: frágreiðing}
			return fd
		}
	}
	return Emfile
}

func releaseopenFíla(frágreiðing int32) {
	if frágreiðing < 0 || frágreiðing >= maxopenfiles {
		return
	}
	entry := &openFílatable[frágreiðing]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && frágreiðing > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = openFílaFrágreiðing{}
	}
}

func closeprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getopenFílafor(process, fd) == nil {
		return Ebadf
	}
	frágreiðing := process.fds[fd].frágreiðing
	process.fds[fd] = fdentry{}
	releaseopenFíla(frágreiðing)
	return 0
}

func sysskriva(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getopenFíla(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootFíluskrá {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getbýtfrompointer(uintptr(address), int(count), int(count))
	console_2.MPrint(buffer)
	return int32(count)
}

func syslesa(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getopenFíla(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return lesastdin(address, count)
	}
	if entry.kind == fdkindrootFíluskrá {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.stødd {
		return 0
	}
	remaining := entry.stødd - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := Getbýtfrompointer(uintptr(address), int(count), int(count))
	return lesavfsFíla(entry, buffer, count)
}

func sysopen(pathaddress uint32, flags uint32, mode uint32) int32 {
	_ = mode
	if pathaddress == 0 {
		return Efault
	}
	accessmode := flags & 3
	if accessmode == oskrivaonly || accessmode == olesaskriva || (flags&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	frágreiðing := allocateopenFíla()
	if frágreiðing < 0 {
		return frágreiðing
	}
	entry := &openFílatable[frágreiðing]
	entry.flags = flags
	if isrootpath(pathaddress) {
		entry.kind = fdkindrootFíluskrá
		entry.stødd = 0
	} else {
		navnlen, navn := copypath(pathaddress)
		if navnlen == 0 {
			*entry = openFílaFrágreiðing{}
			return Enoent
		}
		stødd := fílaStødd(navn[:navnlen])
		if stødd == 0 {
			*entry = openFílaFrágreiðing{}
			return Enoent
		}
		if (flags & oFíluskrá) != 0 {
			*entry = openFílaFrágreiðing{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.stødd = stødd
		entry.navnlen = navnlen
		entry.navn = navn
	}

	fd := allocatefd(process, frágreiðing, 3)
	if fd < 0 {
		*entry = openFílaFrágreiðing{}
		return fd
	}
	return fd
}

func sysclose(fd int32) int32 {
	return closeprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getopenFílafor(process, fd)
	if entry == nil {
		return Ebadf
	}
	newfd := allocatefd(process, process.fds[fd].frágreiðing, minimum)
	if newfd >= 0 {
		entry.refs++
	}
	return newfd
}

func sysdup2(oldfd int32, newfd int32) int32 {
	process := ensurecurrentprocess()
	entry := getopenFílafor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if newfd < 0 || newfd >= maxfd {
		return Ebadf
	}
	if oldfd == newfd {
		return newfd
	}
	if process.fds[newfd].used {
		closeprocessfd(process, newfd)
	}
	process.fds[newfd] = fdentry{used: true, frágreiðing: process.fds[oldfd].frágreiðing}
	entry.refs++
	return newfd
}

func sysfcntl(fd int32, stýriboð uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getopenFílafor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch stýriboð {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdflags)
	case fsetfd:
		process.fds[fd].fdflags = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.flags)
	case fsetfl:
		entry.flags = (entry.flags & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getopenFíla(fd)
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
		base = int64(entry.position)
	case seekend:
		base = int64(entry.stødd)
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

func lesavfsFíla(entry *openFílaFrágreiðing, destination_2 []byte, count uint32) int32 {
	memorymanager := &mem.TMemorymanager{}
	tmppointer := memorymanager.Malloc(entry.stødd)
	if tmppointer == nil {
		return Einval
	}
	tmp := Getbýtfrompointer(uintptr(tmppointer), int(entry.stødd), int(entry.stødd))
	lesaFíla(entry.navn[:entry.navnlen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	memorymanager.Free(tmppointer)
	return int32(count)
}

func isrootpath(pathaddress uint32) bool {
	if pathaddress == 0 {
		return false
	}
	path := Getbýtfrompointer(uintptr(pathaddress), 4, 4)
	if path[0] == '/' && path[1] == 0 {
		return true
	}
	if path[0] == '.' && path[1] == 0 {
		return true
	}
	if path[0] == '/' && path[1] == '.' && path[2] == 0 {
		return true
	}
	return false
}

func sysaccess(pathaddress uint32, mode uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootpath(pathaddress)
	exists := isroot
	if !exists {
		navnlen, navn := copypath(pathaddress)
		exists = navnlen != 0 && fílaStødd(navn[:navnlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mode & 2) != 0 {
		return Eacces
	}

	if (mode&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(pathaddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if !isrootpath(pathaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, stødd uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if stødd < 2 {
		return Erange
	}
	buffer_2 := Getbýtfrompointer(uintptr(bufferaddress), int(stødd), int(stødd))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, stødd uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Device = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Stødd_2 = int32(stødd)
	stat.Blksize = 512
	stat.Blokkur = int32((stødd + 511) / 512)
	return 0
}

func sysstat(pathaddress uint32, stataddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if isrootpath(pathaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	navnlen, navn := copypath(pathaddress)
	if navnlen == 0 {
		return Enoent
	}
	stødd := fílaStødd(navn[:navnlen])
	if stødd == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < navnlen; i++ {
		inode = inode*33 + uint32(navn[i])
	}
	return fillposixstat(stataddress, sifreg|0444, stødd, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getopenFíla(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootFíluskrá:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.stødd, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getopenFíla(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensurecurrentprocess()
	if process == nil {
		return 0
	}
	if process.programbreak == 0 {
		process.programbreak = brúkariheapbase
	}
	if address_2 == 0 {
		return process.programbreak
	}
	if address_2 < brúkariheapbase || address_2 > brúkariheaplimit {
		return process.programbreak
	}
	process.programbreak = address_2
	return process.programbreak
}

func copyutsfield(destination *[65]byte, value string) {
	limit := len(value)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = value[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	navn := (*posixutsname)(Pointer(uintptr(address_2)))
	*navn = posixutsname{}
	copyutsfield(&navn.Sysname, "EngOS")
	copyutsfield(&navn.Nodename, "engos")
	copyutsfield(&navn.Release, "0.1-posix")
	copyutsfield(&navn.Version, "POSIX.1-2017 phase 1")
	copyutsfield(&navn.Machine, "i386")
	return 0
}

func swapunsignedinteger16(value uint16) uint16 {
	return (value << 8) | (value >> 8)
}

func socketcallargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getopenFíla(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.used {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, sockettype uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if sockettype != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensurecurrentprocess()
	if process == nil {
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
	frágreiðing := allocateopenFíla()
	if frágreiðing < 0 {
		return frágreiðing
	}
	localsockets[socketindex] = localdatagramsocket{used: true}
	entry := &openFílatable[frágreiðing]
	entry.kind = fdkindsocket
	entry.flags = olesaskriva
	entry.aux = uint32(socketindex)
	fd := allocatefd(process, frágreiðing, 3)
	if fd < 0 {
		localsockets[socketindex] = localdatagramsocket{}
		*entry = openFílaFrágreiðing{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, longd uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if longd < 16 {
		return nil, Einval
	}
	result := (*socketaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func portinuse(port uint16, except *localdatagramsocket) bool {
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
		port := swapunsignedinteger16(næstaephemeralport)
		næstaephemeralport++
		if næstaephemeralport < 49152 {
			næstaephemeralport = 49152
		}
		if !portinuse(port, socket) {
			socket.local = socketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, longd uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, longd)
	if err != 0 {
		return err
	}
	if socket.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(socket)
	}
	if portinuse(requested.Port, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketconnect(fd int32, address_2 uint32, longd uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, longd)
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

func socketsendto(fd int32, bufferaddress_2 uint32, longd uint32, destinationaddress uint32, destinationLongd uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if longd > maxdatagramStødd {
		return Emsgsize
	}
	if longd != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressBrek := socketaddress(destinationaddress, destinationLongd)
		if addressBrek != 0 {
			return addressBrek
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindBrek := bindephemeral(socket); bindBrek != 0 {
			return bindBrek
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.used && candidate.bound && candidate.local.Port == destination.Port &&
			(candidate.local.Address == 0 || candidate.local.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxsocketpakkar {
		return Eagain
	}
	packet := &receiver.pakkar[receiver.tail]
	*packet = socketpacket{used: true, stødd: longd, source: socket.local}
	if longd != 0 {
		source := Getbýtfrompointer(uintptr(bufferaddress_2), int(longd), int(longd))
		copy(packet.data[:longd], source)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpakkar
	receiver.count++
	return int32(longd)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, longd uint32, sourceaddress uint32, sourceLongdaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if longd != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.pakkar[socket.head]
	copyLongd := packet.stødd
	if copyLongd > longd {
		copyLongd = longd
	}
	if copyLongd != 0 {
		destination := Getbýtfrompointer(uintptr(bufferaddress_2), int(copyLongd), int(copyLongd))
		copy(destination, packet.data[:copyLongd])
	}
	if sourceaddress != 0 {
		if sourceLongdaddress == 0 {
			return Efault
		}
		providedLongd := (*uint32)(Pointer(uintptr(sourceLongdaddress)))
		if *providedLongd >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(sourceaddress))) = packet.source
		}
		*providedLongd = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpakkar
	socket.count--
	return int32(copyLongd)
}

func copysocketNavn(fd int32, address_2 uint32, longdaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || longdaddress == 0 {
		return Efault
	}
	longd := (*uint32)(Pointer(uintptr(longdaddress)))
	if *longd < 16 {
		*longd = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindBrek := bindephemeral(socket); bindBrek != 0 {
				return bindBrek
			}
		}
		*(*socketaddressipv4)(Pointer(uintptr(address_2))) = socket.local
	}
	*longd = 16
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
		return copysocketNavn(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return copysocketNavn(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
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

func lesastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getbýtfrompointer(uintptr(address), int(count), int(count))
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
	næsta := (stdinskriva + 1) % uint32(len(stdinbuffer))
	if næsta == stdinlesa {
		return
	}
	stdinbuffer[stdinskriva] = c
	stdinskriva = næsta
}

func stdingetblocking() byte {
	for stdinlesa == stdinskriva {
		sc := pollKnappaborðscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinlesa]
	stdinlesa = (stdinlesa + 1) % uint32(len(stdinbuffer))
	return c
}

func pollKnappaborðscancode() byte {
	for (Portlesabyte(0x64) & 0x01) == 0 {
	}
	sc := Portlesabyte(0x60)
	return scancodetobyte_2(sc)
}

func scancodetobyte_2(sc uint8) byte {
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

func copyexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < maxexecvectorentry; index++ {
		stringaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if stringaddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for longd := uint32(0); longd <= maxexecstringLongd; longd++ {
			value := *(*byte)(Pointer(uintptr(stringaddress + longd)))
			result.values[index][longd] = value
			if value == 0 {
				result.lengths[index] = longd
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

func pushexecunsignedinteger32(stack *uint32, value uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = value
}

func setupexecstack(cpu *TcpuStøða, arguments_2 *execvector, environment *execvector) int32 {
	const stackbýt uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), BrúkaristackToppur-stackbýt, stackbýt) {
		return Enomem
	}
	stack := BrúkaristackToppur
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		longd := environment.lengths[i] + 1
		stack -= longd
		destination := Getbýtfrompointer(uintptr(stack), int(longd), int(longd))
		copy(destination, environment.values[i][:longd])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		longd := arguments_2.lengths[i] + 1
		stack -= longd
		destination := Getbýtfrompointer(uintptr(stack), int(longd), int(longd))
		copy(destination, arguments_2.values[i][:longd])
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
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func closeonexec(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used && (process.fds[fd].fdflags&fdcloexec) != 0 {
			closeprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *TcpuStøða, pathaddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := copyexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := copyexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	navnlen, navn := copypath(pathaddress)
	if navnlen == 0 {
		return Enoent
	}
	stødd := fílaStødd(navn[:navnlen])
	if stødd == 0 {
		return Enoent
	}
	memorymanager := &mem.TMemorymanager{}
	fílapointer := memorymanager.Malloc(stødd)
	if fílapointer == nil {
		return Einval
	}
	data := Getbýtfrompointer(uintptr(fílapointer), int(stødd), int(stødd))
	lesaFíla(navn[:navnlen], data)
	if stødd < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorymanager.Free(fílapointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memorymanager.Free(fílapointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	closeonexec(ensurecurrentprocess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStøða) int32 {
	parentpid := Currentpid()
	if ensurecurrentprocess() == nil {
		return Enfile
	}
	pid := allocateprocess(parentpid)
	if pid == 0 {
		return Einval
	}
	memorymanager := &mem.TMemorymanager{}
	threadpointer := memorymanager.Malloc(uint32(Sizeof(TThread{})))
	stackpointer := memorymanager.Malloc(ThreadstackStødd)
	childpageFíluskrá := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childpageFíluskrá == 0 {
		discardprocess(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.CpuStøða = (*TcpuStøða)(Pointer(uintptr(stackpointer) + ThreadstackStødd - Sizeof(TcpuStøða{})))
	*child.CpuStøða = *cpu
	child.CpuStøða.Eax = 0
	child.Brúkaristack_2 = cpu.Esp
	child.BrúkaristackStødd_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.PageFíluskráentry = childpageFíluskrá
	child.ThreadStøða = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Addrunnablethread(child)
	return int32(pid)
}

func sysexit(status uint32) {
	pid := Currentpid()
	for i := 0; i < len(processtable); i++ {
		if processtable[i].used && processtable[i].pid == pid {
			closeAllarprocessfds(&processtable[i])
			processtable[i].exited = true
			processtable[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, statusaddress uint32, options uint32) int32 {
	if (options & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(processtable); i++ {
		p := &processtable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.used && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if statusaddress != 0 {
					*(*uint32)(Pointer(uintptr(statusaddress))) = p.status
				}
				childpid := p.pid
				*p = processentry{}
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

func allocateprocess(parent uint32) uint32 {
	parentprocess := findprocess(parent)
	pid := Allocatepid()
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].used {
			processtable[i] = processentry{
				used:		true,
				pid:		pid,
				parent:		parent,
				programbreak:	brúkariheapbase,
			}
			if parentprocess != nil {
				processtable[i].programbreak = parentprocess.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocess.fds[fd].used {
						processtable[i].fds[fd] = parentprocess.fds[fd]
						frágreiðing := parentprocess.fds[fd].frágreiðing
						if frágreiðing >= 0 && frágreiðing < maxopenfiles {
							openFílatable[frágreiðing].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processtable[i])
			}
			return pid
		}
	}
	return 0
}

func closeAllarprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used {
			closeprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := findprocess(pid)
	if process == nil {
		return
	}
	closeAllarprocessfds(process)
	*process = processentry{}
}

func copypath(pathaddress uint32) (uint32, [12]byte) {
	var navn [12]byte
	if pathaddress == 0 {
		return 0, navn
	}
	raw := Getbýtfrompointer(uintptr(pathaddress), 64, 64)
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

func fílaStødd(filename []byte) uint32 {
	var ata0s = TFramkomiðtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Lesapartition(&ata0s)

	bios := TBiosparameterBlokkur32{}
	stødd := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()
	return stødd
}

func lesaFíla(filename []byte, data []byte) {
	var ata0s = TFramkomiðtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Lesapartition(&ata0s)

	bios := TBiosparameterBlokkur32{}
	bios.Lesa(&ata0s, partition.Mbr.Primarypartition[0], filename, data)
	ata0s.Flush()
}

func getcr3() uint32
