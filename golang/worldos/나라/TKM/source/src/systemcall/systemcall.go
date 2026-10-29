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
import . "faýlsystem/msdospartition"
import . "faýlsystem/fat"
import . "faýlsystem/elf"
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
	SysOka		uint32	= 3
	SysÝaz		uint32	= 4
	SysAç		uint32	= 5
	SysÝap		uint32	= 6
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
	maxAçfiles		= 128
)

type fdentry struct {
	used	bool
	wasp	int32
	fdflags	uint32
}

type açFaýlWasp struct {
	used		bool
	refs		uint32
	kind		uint32
	flags		uint32
	position	uint32
	ululyk		uint32
	ad		[12]byte
	adlen		uint32
	aux		uint32
}

const (
	fdkindHiç		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindrootdirectory	uint32	= 4
	fdkindsocket		uint32	= 5

	oOkaonly	uint32	= 0
	oÝazonly	uint32	= 1
	oOkaÝaz		uint32	= 2
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
	maxdatagramUlulyk	= 512
)

type socketaddressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	used	bool
	ululyk	uint32
	çeşme	socketaddressipv4
	data	[maxdatagramUlulyk]byte
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
	Ululyk_2	int32
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

func syscallHata(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var açFaýltable [maxAçfiles]açFaýlWasp
var processtable [32]processentry
var localsockets [maxsockets]localdatagramsocket
var nextephemeralport uint16 = 49152

const (
	ullançyheapbase		uint32	= 0x06000000
	ullançyheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinOka uint32
var stdinÝaz uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func SysOka_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysOka, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysÇapstr(buffer string) {
	h := (*stringheader)(Pointer(&buffer))
	Syscall(SysÝaz, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysÇapunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysÝaz, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysAç_2(ýol uintptr, flags uint32, mode uint32) int32 {
	return int32(Syscall(SysAç, uint32(ýol), flags, mode))
}

func SysÝap_2(fd uint32) int32 {
	return int32(Syscall(SysÝap, fd))
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
		return syscallHata(Enosys)
	}
}

func (self *TSyscall) Init(manager *TInterruptmanager) {
	initFaýldescriptor()

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
		return uint32(uintptr(Pointer(Durcurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Durcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysOka:
		cpu.Eax = uint32(sysOka(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysÝaz:
		cpu.Eax = uint32(sysÝaz(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysAç:
		cpu.Eax = uint32(sysAç(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysAç(cpu.Ebx, ocreate|oÝazonly|otruncate, cpu.Ecx))
		return esp
	case SysÝap:
		cpu.Eax = uint32(sysÝap(int32(cpu.Ebx)))
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
		console_2.MUnsignedinteger32Çap(cpu.Ebx)
		return esp

	default:
		console_2.MÇapxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Çap(esp)
		console_2.MÇap(([]byte)(":"))
		console_2.MUnsignedinteger32Çap(cpu.Eax)
		console_2.MÇap(([]byte)(":"))
		console_2.MUnsignedinteger32Çap(cpu.Ebx)
		console_2.MÇap(([]byte)(":"))
		console_2.MUnsignedinteger32Çap(cpu.Ecx)
		console_2.MÇap(([]byte)(":"))
		console_2.MUnsignedinteger32Çap(cpu.Edx)
		console_2.MÇap(([]byte)("]"))
		cpu.Eax = syscallHata(Enosys)
		return esp
	}

	return esp
}

func initFaýldescriptor() {
	for i := 0; i < maxAçfiles; i++ {
		açFaýltable[i] = açFaýlWasp{}
	}
	for i := 0; i < len(processtable); i++ {
		processtable[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	nextephemeralport = 49152
	açFaýltable[0] = açFaýlWasp{used: true, kind: fdkindstdin, flags: oOkaonly}
	açFaýltable[1] = açFaýlWasp{used: true, kind: fdkindconsole, flags: oÝazonly}
	açFaýltable[2] = açFaýlWasp{used: true, kind: fdkindconsole, flags: oÝazonly}
}

func tapprocess(pid uint32) *processentry {
	for i := 0; i < len(processtable); i++ {
		if processtable[i].used && processtable[i].pid == pid {
			return &processtable[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{used: true, wasp: fd}
		açFaýltable[fd].refs++
	}
}

func ensurecurrentprocess() *processentry {
	pid := Currentpid()
	if process := tapprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].used {
			processtable[i] = processentry{
				used:		true,
				pid:		pid,
				parent:		Currentparentpid(),
				programbreak:	ullançyheapbase,
			}
			initializeprocessfds(&processtable[i])
			return &processtable[i]
		}
	}
	return nil
}

func getAçFaýlfor(process *processentry, fd int32) *açFaýlWasp {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].used {
		return nil
	}
	wasp := process.fds[fd].wasp
	if wasp < 0 || wasp >= maxAçfiles || !açFaýltable[wasp].used {
		return nil
	}
	return &açFaýltable[wasp]
}

func getAçFaýl(fd int32) *açFaýlWasp {
	return getAçFaýlfor(ensurecurrentprocess(), fd)
}

func allocateAçFaýl() int32 {
	for i := int32(3); i < maxAçfiles; i++ {
		if !açFaýltable[i].used {
			açFaýltable[i] = açFaýlWasp{used: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, wasp int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].used {
			process.fds[fd] = fdentry{used: true, wasp: wasp}
			return fd
		}
	}
	return Emfile
}

func releaseAçFaýl(wasp int32) {
	if wasp < 0 || wasp >= maxAçfiles {
		return
	}
	entry := &açFaýltable[wasp]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && wasp > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = açFaýlWasp{}
	}
}

func ýapprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getAçFaýlfor(process, fd) == nil {
		return Ebadf
	}
	wasp := process.fds[fd].wasp
	process.fds[fd] = fdentry{}
	releaseAçFaýl(wasp)
	return 0
}

func sysÝaz(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getAçFaýl(fd)
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
	buffer := GetBaýtlarfrompointer(uintptr(address), int(count), int(count))
	console_2.MÇap(buffer)
	return int32(count)
}

func sysOka(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getAçFaýl(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return okastdin(address, count)
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
	if entry.position >= entry.ululyk {
		return 0
	}
	remaining := entry.ululyk - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := GetBaýtlarfrompointer(uintptr(address), int(count), int(count))
	return okavfsFaýl(entry, buffer, count)
}

func sysAç(ýoladdress uint32, flags uint32, mode uint32) int32 {
	_ = mode
	if ýoladdress == 0 {
		return Efault
	}
	accessmode := flags & 3
	if accessmode == oÝazonly || accessmode == oOkaÝaz || (flags&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	wasp := allocateAçFaýl()
	if wasp < 0 {
		return wasp
	}
	entry := &açFaýltable[wasp]
	entry.flags = flags
	if isrootÝol(ýoladdress) {
		entry.kind = fdkindrootdirectory
		entry.ululyk = 0
	} else {
		adlen, ad := nusgalaÝol(ýoladdress)
		if adlen == 0 {
			*entry = açFaýlWasp{}
			return Enoent
		}
		ululyk := faýlUlulyk(ad[:adlen])
		if ululyk == 0 {
			*entry = açFaýlWasp{}
			return Enoent
		}
		if (flags & odirectory) != 0 {
			*entry = açFaýlWasp{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.ululyk = ululyk
		entry.adlen = adlen
		entry.ad = ad
	}

	fd := allocatefd(process, wasp, 3)
	if fd < 0 {
		*entry = açFaýlWasp{}
		return fd
	}
	return fd
}

func sysÝap(fd int32) int32 {
	return ýapprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getAçFaýlfor(process, fd)
	if entry == nil {
		return Ebadf
	}
	täzefd := allocatefd(process, process.fds[fd].wasp, minimum)
	if täzefd >= 0 {
		entry.refs++
	}
	return täzefd
}

func sysdup2(oldfd int32, täzefd int32) int32 {
	process := ensurecurrentprocess()
	entry := getAçFaýlfor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if täzefd < 0 || täzefd >= maxfd {
		return Ebadf
	}
	if oldfd == täzefd {
		return täzefd
	}
	if process.fds[täzefd].used {
		ýapprocessfd(process, täzefd)
	}
	process.fds[täzefd] = fdentry{used: true, wasp: process.fds[oldfd].wasp}
	entry.refs++
	return täzefd
}

func sysfcntl(fd int32, command uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getAçFaýlfor(process, fd)
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
	entry := getAçFaýl(fd)
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
		base = int64(entry.ululyk)
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

func okavfsFaýl(entry *açFaýlWasp, destination_2 []byte, count uint32) int32 {
	memorymanager := &mem.TMemorymanager{}
	tmppointer := memorymanager.Malloc(entry.ululyk)
	if tmppointer == nil {
		return Einval
	}
	tmp := GetBaýtlarfrompointer(uintptr(tmppointer), int(entry.ululyk), int(entry.ululyk))
	okaFaýl(entry.ad[:entry.adlen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	memorymanager.Free(tmppointer)
	return int32(count)
}

func isrootÝol(ýoladdress uint32) bool {
	if ýoladdress == 0 {
		return false
	}
	ýol := GetBaýtlarfrompointer(uintptr(ýoladdress), 4, 4)
	if ýol[0] == '/' && ýol[1] == 0 {
		return true
	}
	if ýol[0] == '.' && ýol[1] == 0 {
		return true
	}
	if ýol[0] == '/' && ýol[1] == '.' && ýol[2] == 0 {
		return true
	}
	return false
}

func sysaccess(ýoladdress uint32, mode uint32) int32 {
	if ýoladdress == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootÝol(ýoladdress)
	exists := isroot
	if !exists {
		adlen, ad := nusgalaÝol(ýoladdress)
		exists = adlen != 0 && faýlUlulyk(ad[:adlen]) != 0
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

func syschdir(ýoladdress uint32) int32 {
	if ýoladdress == 0 {
		return Efault
	}
	if !isrootÝol(ýoladdress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, ululyk uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if ululyk < 2 {
		return Erange
	}
	buffer_2 := GetBaýtlarfrompointer(uintptr(bufferaddress), int(ululyk), int(ululyk))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, ululyk uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Device = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Ululyk_2 = int32(ululyk)
	stat.Blksize = 512
	stat.Block = int32((ululyk + 511) / 512)
	return 0
}

func sysstat(ýoladdress uint32, stataddress uint32) int32 {
	if ýoladdress == 0 {
		return Efault
	}
	if isrootÝol(ýoladdress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	adlen, ad := nusgalaÝol(ýoladdress)
	if adlen == 0 {
		return Enoent
	}
	ululyk := faýlUlulyk(ad[:adlen])
	if ululyk == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < adlen; i++ {
		inode = inode*33 + uint32(ad[i])
	}
	return fillposixstat(stataddress, sifreg|0444, ululyk, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getAçFaýl(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootdirectory:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.ululyk, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getAçFaýl(fd) == nil {
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
		process.programbreak = ullançyheapbase
	}
	if address_2 == 0 {
		return process.programbreak
	}
	if address_2 < ullançyheapbase || address_2 > ullançyheaplimit {
		return process.programbreak
	}
	process.programbreak = address_2
	return process.programbreak
}

func nusgalautsfield(destination *[65]byte, mykdar string) {
	limit := len(mykdar)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = mykdar[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	ad := (*posixutsname)(Pointer(uintptr(address_2)))
	*ad = posixutsname{}
	nusgalautsfield(&ad.Sysname, "EngOS")
	nusgalautsfield(&ad.Nodename, "engos")
	nusgalautsfield(&ad.Release, "0.1-posix")
	nusgalautsfield(&ad.Version, "POSIX.1-2017 phase 1")
	nusgalautsfield(&ad.Machine, "i386")
	return 0
}

func swapunsignedinteger16(mykdar uint16) uint16 {
	return (mykdar << 8) | (mykdar >> 8)
}

func socketcallargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getAçFaýl(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.used {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketHil uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketHil != sockdatagram {
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
	wasp := allocateAçFaýl()
	if wasp < 0 {
		return wasp
	}
	localsockets[socketindex] = localdatagramsocket{used: true}
	entry := &açFaýltable[wasp]
	entry.kind = fdkindsocket
	entry.flags = oOkaÝaz
	entry.aux = uint32(socketindex)
	fd := allocatefd(process, wasp, 3)
	if fd < 0 {
		localsockets[socketindex] = localdatagramsocket{}
		*entry = açFaýlWasp{}
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
	if length > maxdatagramUlulyk {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressipv4
	if destinationaddress != 0 {
		address_2, addressHata := socketaddress(destinationaddress, destinationlength)
		if addressHata != 0 {
			return addressHata
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindHata := bindephemeral(socket); bindHata != 0 {
			return bindHata
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
	*packet = socketpacket{used: true, ululyk: length, çeşme: socket.local}
	if length != 0 {
		çeşme := GetBaýtlarfrompointer(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], çeşme)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, çeşmeaddress uint32, çeşmelengthaddress uint32) int32 {
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
	nusgalalength := packet.ululyk
	if nusgalalength > length {
		nusgalalength = length
	}
	if nusgalalength != 0 {
		destination := GetBaýtlarfrompointer(uintptr(bufferaddress_2), int(nusgalalength), int(nusgalalength))
		copy(destination, packet.data[:nusgalalength])
	}
	if çeşmeaddress != 0 {
		if çeşmelengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(çeşmelengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressipv4)(Pointer(uintptr(çeşmeaddress))) = packet.çeşme
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(nusgalalength)
}

func nusgalasocketAd(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
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
			if bindHata := bindephemeral(socket); bindHata != 0 {
				return bindHata
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
		return nusgalasocketAd(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return nusgalasocketAd(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
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

func okastdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBaýtlarfrompointer(uintptr(address), int(count), int(count))
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
	next := (stdinÝaz + 1) % uint32(len(stdinbuffer))
	if next == stdinOka {
		return
	}
	stdinbuffer[stdinÝaz] = c
	stdinÝaz = next
}

func stdingetblocking() byte {
	for stdinOka == stdinÝaz {
		sc := pollkeyboardscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinOka]
	stdinOka = (stdinOka + 1) % uint32(len(stdinbuffer))
	return c
}

func pollkeyboardscancode() byte {
	for (PortOkabyte(0x64) & 0x01) == 0 {
	}
	sc := PortOkabyte(0x60)
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

func nusgalaexecvector(address_2 uint32, result *execvector) int32 {
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
			mykdar := *(*byte)(Pointer(uintptr(stringaddress + length)))
			result.values[index][length] = mykdar
			if mykdar == 0 {
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

func pushexecunsignedinteger32(stack *uint32, mykdar uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = mykdar
}

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackBaýtlar uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Ullançystacküst-stackBaýtlar, stackBaýtlar) {
		return Enomem
	}
	stack := Ullançystacküst
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := GetBaýtlarfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := GetBaýtlarfrompointer(uintptr(stack), int(length), int(length))
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

func ýaponexec(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used && (process.fds[fd].fdflags&fdcloexec) != 0 {
			ýapprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, ýoladdress uint32) int32 {
	if ýoladdress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := nusgalaexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := nusgalaexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	adlen, ad := nusgalaÝol(ýoladdress)
	if adlen == 0 {
		return Enoent
	}
	ululyk := faýlUlulyk(ad[:adlen])
	if ululyk == 0 {
		return Enoent
	}
	memorymanager := &mem.TMemorymanager{}
	faýlpointer := memorymanager.Malloc(ululyk)
	if faýlpointer == nil {
		return Einval
	}
	data := GetBaýtlarfrompointer(uintptr(faýlpointer), int(ululyk), int(ululyk))
	okaFaýl(ad[:adlen], data)
	if ululyk < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorymanager.Free(faýlpointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	memorymanager.Free(faýlpointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	ýaponexec(ensurecurrentprocess())
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
	stackpointer := memorymanager.Malloc(ThreadstackUlulyk)
	childpagedirectory := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childpagedirectory == 0 {
		discardprocess(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackpointer) + ThreadstackUlulyk - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Ullançystack_2 = cpu.Esp
	child.UllançystackUlulyk_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pagedirectoryentry = childpagedirectory
	child.Threadstate = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Eklerunnablethread(child)
	return int32(pid)
}

func sysexit(status uint32) {
	pid := Currentpid()
	for i := 0; i < len(processtable); i++ {
		if processtable[i].used && processtable[i].pid == pid {
			ýapallprocessfds(&processtable[i])
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
	parentprocess := tapprocess(parent)
	pid := Allocatepid()
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].used {
			processtable[i] = processentry{
				used:		true,
				pid:		pid,
				parent:		parent,
				programbreak:	ullançyheapbase,
			}
			if parentprocess != nil {
				processtable[i].programbreak = parentprocess.programbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocess.fds[fd].used {
						processtable[i].fds[fd] = parentprocess.fds[fd]
						wasp := parentprocess.fds[fd].wasp
						if wasp >= 0 && wasp < maxAçfiles {
							açFaýltable[wasp].refs++
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

func ýapallprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].used {
			ýapprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := tapprocess(pid)
	if process == nil {
		return
	}
	ýapallprocessfds(process)
	*process = processentry{}
}

func nusgalaÝol(ýoladdress uint32) (uint32, [12]byte) {
	var ad [12]byte
	if ýoladdress == 0 {
		return 0, ad
	}
	raw := GetBaýtlarfrompointer(uintptr(ýoladdress), 64, 64)
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
		ad[n] = c
		n++
	}
	return n, ad
}

func faýlUlulyk(faýlady []byte) uint32 {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Okapartition(&ata0s)

	bios := TBiosparameterblock32{}
	ululyk := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], faýlady)
	ata0s.Flush()
	return ululyk
}

func okaFaýl(faýlady []byte, data []byte) {
	var ata0s = TAdvancedtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Okapartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Oka(&ata0s, partition.Mbr.Primarypartition[0], faýlady, data)
	ata0s.Flush()
}

func getcr3() uint32
