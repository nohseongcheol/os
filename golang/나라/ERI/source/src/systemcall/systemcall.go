package systemcall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "filesystem/msdospartition"
import . "filesystem/fat"
import . "filesystem/elf"
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
	Sysanbeb	uint32	= 3
	Systsahaf	uint32	= 4
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
	description	int32
	fdflags		uint32
}

type openfiledescription struct {
	used		bool
	refs		uint32
	kind		uint32
	flags		uint32
	position	uint32
	size		uint32
	name		[12]byte
	namelen		uint32
	aux		uint32
}

const (
	fdkindnone		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindrootdirectory	uint32	= 4
	fdkindsocket		uint32	= 5

	oanbebonly	uint32	= 0
	otsahafonly	uint32	= 1
	oanbebtsahaf	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	odirectory	uint32	= 0x10000

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
	maxdatagramsize		= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	used	bool
	size	uint32
	source	socketaddressipv4
	data	[maxdatagramsize]byte
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
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Size_2		int32
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
	maxexecvectorentry	= 16
	maxexecstringlength	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecstringlength + 1]byte
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

func syscallerror(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var openfiletable [maxopenfiles]openfiledescription
var processtable [32]processentry
var localsockets [maxsockets]localdatagramsocket
var nextephemeralport uint16 = 49152

const (
	userheapbase	uint32	= 0x06000000
	userheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinanbeb uint32
var stdintsahaf uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func Sysanbeb_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysanbeb, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysprintstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(Systsahaf, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysprintunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Systsahaf, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
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
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

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
	case Sysanbeb:
		cpu.Eax = uint32(sysanbeb(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Systsahaf:
		cpu.Eax = uint32(systsahaf(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysopen:
		cpu.Eax = uint32(sysopen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysopen(cpu.Ebx, ocreate|otsahafonly|otruncate, cpu.Ecx))
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
		openfiletable[i] = openfiledescription{}
	}
	for i := 0; i < len(processtable); i++ {
		processtable[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	nextephemeralport = 49152
	openfiletable[0] = openfiledescription{used: true, kind: fdkindstdin, flags: oanbebonly}
	openfiletable[1] = openfiledescription{used: true, kind: fdkindconsole, flags: otsahafonly}
	openfiletable[2] = openfiledescription{used: true, kind: fdkindconsole, flags: otsahafonly}
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
		process.fds[fd] = fdentry{used: true, description: fd}
		openfiletable[fd].refs++
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
				programbreak:	userheapbase,
			}
			initializeprocessfds(&processtable[i])
			return &processtable[i]
		}
	}
	return nil
}

func getopenfilefor(process *processentry, fd int32) *openfiledescription {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].used {
		return nil
	}
	description := process.fds[fd].description
	if description < 0 || description >= maxopenfiles || !openfiletable[description].used {
		return nil
	}
	return &openfiletable[description]
}

func getopenfile(fd int32) *openfiledescription {
	return getopenfilefor(ensurecurrentprocess(), fd)
}

func allocateopenfile() int32 {
	for i := int32(3); i < maxopenfiles; i++ {
		if !openfiletable[i].used {
			openfiletable[i] = openfiledescription{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, description int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].used {
			process.fds[fd] = fdentry{used: true, description: description}
			return fd
		}
	}
	return Emfile
}

func releaseopenfile(description int32) {
	if description < 0 || description >= maxopenfiles {
		return
	}
	entry := &openfiletable[description]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && description > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = openfiledescription{}
	}
}

func closeprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getopenfilefor(process, fd) == nil {
		return Ebadf
	}
	description := process.fds[fd].description
	process.fds[fd] = fdentry{}
	releaseopenfile(description)
	return 0
}

func systsahaf(fd int32, address uint32, count uint32) int32 {
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
		if entry.kind == fdkindfat || entry.kind == fdkindrootdirectory {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getbytesfrompointer(uintptr(address), int(count), int(count))
	console_2.MPrint(buffer)
	return int32(count)
}

func sysanbeb(fd int32, address uint32, count uint32) int32 {
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
		return anbebstdin(address, count)
	}
	if entry.kind == fdkindrootdirectory {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.size {
		return 0
	}
	remaining := entry.size - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := Getbytesfrompointer(uintptr(address), int(count), int(count))
	return anbebvfsfile(entry, buffer, count)
}

func sysopen(pathaddress uint32, flags uint32, mode uint32) int32 {
	_ = mode
	if pathaddress == 0 {
		return Efault
	}
	accessmode := flags & 3
	if accessmode == otsahafonly || accessmode == oanbebtsahaf || (flags&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	description := allocateopenfile()
	if description < 0 {
		return description
	}
	entry := &openfiletable[description]
	entry.flags = flags
	if isrootpath(pathaddress) {
		entry.kind = fdkindrootdirectory
		entry.size = 0
	} else {
		namelen, name := copypath(pathaddress)
		if namelen == 0 {
			*entry = openfiledescription{}
			return Enoent
		}
		size := filesize(name[:namelen])
		if size == 0 {
			*entry = openfiledescription{}
			return Enoent
		}
		if (flags & odirectory) != 0 {
			*entry = openfiledescription{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.size = size
		entry.namelen = namelen
		entry.name = name
	}

	fd := allocatefd(process, description, 3)
	if fd < 0 {
		*entry = openfiledescription{}
		return fd
	}
	return fd
}

func sysclose(fd int32) int32 {
	return closeprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getopenfilefor(process, fd)
	if entry == nil {
		return Ebadf
	}
	newfd := allocatefd(process, process.fds[fd].description, minimum)
	if newfd >= 0 {
		entry.refs++
	}
	return newfd
}

func sysdup2(oldfd int32, newfd int32) int32 {
	process := ensurecurrentprocess()
	entry := getopenfilefor(process, oldfd)
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
	process.fds[newfd] = fdentry{used: true, description: process.fds[oldfd].description}
	entry.refs++
	return newfd
}

func sysfcntl(fd int32, command uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getopenfilefor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch command {
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
	entry := getopenfile(fd)
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
		base = int64(entry.size)
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

func anbebvfsfile(entry *openfiledescription, destination_2 []byte, count uint32) int32 {
	memorymanager := &mem.TMemorymanager{}
	tmppointer := memorymanager.Malloc(entry.size)
	if tmppointer == nil {
		return Einval
	}
	tmp := Getbytesfrompointer(uintptr(tmppointer), int(entry.size), int(entry.size))
	anbebfile(entry.name[:entry.namelen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	memorymanager.Free(tmppointer)
	return int32(count)
}

func isrootpath(pathaddress uint32) bool {
	if pathaddress == 0 {
		return false
	}
	path := Getbytesfrompointer(uintptr(pathaddress), 4, 4)
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
		namelen, name := copypath(pathaddress)
		exists = namelen != 0 && filesize(name[:namelen]) != 0
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

func sysgetcwd(bufferaddress uint32, size uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if size < 2 {
		return Erange
	}
	buffer_2 := Getbytesfrompointer(uintptr(bufferaddress), int(size), int(size))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, size uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Device = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Size_2 = int32(size)
	stat.Blksize = 512
	stat.Block = int32((size + 511) / 512)
	return 0
}

func sysstat(pathaddress uint32, stataddress uint32) int32 {
	if pathaddress == 0 {
		return Efault
	}
	if isrootpath(pathaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	namelen, name := copypath(pathaddress)
	if namelen == 0 {
		return Enoent
	}
	size := filesize(name[:namelen])
	if size == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < namelen; i++ {
		inode = inode*33 + uint32(name[i])
	}
	return fillposixstat(stataddress, sifreg|0444, size, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getopenfile(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootdirectory:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.size, uint32(fd+2))
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
	process := ensurecurrentprocess()
	if process == nil {
		return 0
	}
	if process.programbreak == 0 {
		process.programbreak = userheapbase
	}
	if address_2 == 0 {
		return process.programbreak
	}
	if address_2 < userheapbase || address_2 > userheaplimit {
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
	description := allocateopenfile()
	if description < 0 {
		return description
	}
	localsockets[socketindex] = localdatagramsocket{used: true}
	entry := &openfiletable[description]
	entry.kind = fdkindsocket
	entry.flags = oanbebtsahaf
	entry.aux = uint32(socketindex)
	fd := allocatefd(process, description, 3)
	if fd < 0 {
		localsockets[socketindex] = localdatagramsocket{}
		*entry = openfiledescription{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, length uint32) (*socketaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if length < 16 {
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
		port := swapunsignedinteger16(nextephemeralport)
		nextephemeralport++
		if nextephemeralport < 49152 {
			nextephemeralport = 49152
		}
		if !portinuse(port, socket) {
			socket.local = socketaddressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(fd int32, address_2 uint32, length uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := socketaddress(address_2, length)
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

func socketconnect(fd int32, address_2 uint32, length uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := socketaddress(address_2, length)
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

func socketsendto(fd int32, bufferaddress_2 uint32, length uint32, destinationaddress uint32, destinationlength uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if length > maxdatagramsize {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addresserror := socketaddress(destinationaddress, destinationlength)
		if addresserror != 0 {
			return addresserror
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if binderror := bindephemeral(socket); binderror != 0 {
			return binderror
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
	if receiver.count >= maxsocketpackets {
		return Eagain
	}
	packet := &receiver.packets[receiver.tail]
	*packet = socketpacket{used: true, size: length, source: socket.local}
	if length != 0 {
		source := Getbytesfrompointer(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], source)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, sourceaddress uint32, sourcelengthaddress uint32) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.packets[socket.head]
	copylength := packet.size
	if copylength > length {
		copylength = length
	}
	if copylength != 0 {
		destination := Getbytesfrompointer(uintptr(bufferaddress_2), int(copylength), int(copylength))
		copy(destination, packet.data[:copylength])
	}
	if sourceaddress != 0 {
		if sourcelengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(sourcelengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(sourceaddress))) = packet.source
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(copylength)
}

func copysocketname(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
	socket, err := socketforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || lengthaddress == 0 {
		return Efault
	}
	length := (*uint32)(Pointer(uintptr(lengthaddress)))
	if *length < 16 {
		*length = 16
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
	*length = 16
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

func anbebstdin(address uint32, count uint32) int32 {
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
	next := (stdintsahaf + 1) % uint32(len(stdinbuffer))
	if next == stdinanbeb {
		return
	}
	stdinbuffer[stdintsahaf] = c
	stdintsahaf = next
}

func stdingetblocking() byte {
	for stdinanbeb == stdintsahaf {
		sc := pollkeyboardscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinanbeb]
	stdinanbeb = (stdinanbeb + 1) % uint32(len(stdinbuffer))
	return c
}

func pollkeyboardscancode() byte {
	for (Portanbebbyte(0x64) & 0x01) == 0 {
	}
	sc := Portanbebbyte(0x60)
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
		for length := uint32(0); length <= maxexecstringlength; length++ {
			value := *(*byte)(Pointer(uintptr(stringaddress + length)))
			result.values[index][length] = value
			if value == 0 {
				result.lengths[index] = length
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

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackbytes uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Userstacktop-stackbytes, stackbytes) {
		return Enomem
	}
	stack := Userstacktop
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := Getbytesfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := Getbytesfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, arguments_2.values[i][:length])
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

func sysexecve(cpu *Tcpustate, pathaddress uint32) int32 {
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
	namelen, name := copypath(pathaddress)
	if namelen == 0 {
		return Enoent
	}
	size := filesize(name[:namelen])
	if size == 0 {
		return Enoent
	}
	memorymanager := &mem.TMemorymanager{}
	filepointer := memorymanager.Malloc(size)
	if filepointer == nil {
		return Einval
	}
	data := Getbytesfrompointer(uintptr(filepointer), int(size), int(size))
	anbebfile(name[:namelen], data)
	if size < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorymanager.Free(filepointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memorymanager.Free(filepointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	closeonexec(ensurecurrentprocess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpustate) int32 {
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
	stackpointer := memorymanager.Malloc(Threadstacksize)
	childpagedirectory := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childpagedirectory == 0 {
		discardprocess(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackpointer) + Threadstacksize - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Userstack_2 = cpu.Esp
	child.Userstacksize_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pagedirectoryentry = childpagedirectory
	child.Threadstate = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Addrunnablethread(child)
	return int32(pid)
}

func sysexit(status uint32) {
	pid := Currentpid()
	for i := 0; i < len(processtable); i++ {
		if processtable[i].used && processtable[i].pid == pid {
			closeallprocessfds(&processtable[i])
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
				programbreak:	userheapbase,
			}
			if parentprocess != nil {
				processtable[i].programbreak = parentprocess.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocess.fds[fd].used {
						processtable[i].fds[fd] = parentprocess.fds[fd]
						description := parentprocess.fds[fd].description
						if description >= 0 && description < maxopenfiles {
							openfiletable[description].refs++
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

func closeallprocessfds(process *processentry) {
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
	closeallprocessfds(process)
	*process = processentry{}
}

func copypath(pathaddress uint32) (uint32, [12]byte) {
	var name [12]byte
	if pathaddress == 0 {
		return 0, name
	}
	raw := Getbytesfrompointer(uintptr(pathaddress), 64, 64)
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

func filesize(filename []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Anbebpartition(&ata0s)

	bios := TBiosparameterblock32{}
	size := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], filename)
	ata0s.Flush()
	return size
}

func anbebfile(filename []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Anbebpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Anbeb(&ata0s, partition.Mbr.Primarypartition[0], filename, data)
	ata0s.Flush()
}

func getcr3() uint32
