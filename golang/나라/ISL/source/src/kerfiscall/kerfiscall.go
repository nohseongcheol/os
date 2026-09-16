/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package kerfiscall

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "skráKerfis/msdospartition"
import . "skráKerfis/fat"
import . "skráKerfis/elf"
import mem "minnimanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "sýndarMinni"

var console_2 = TConsole{}

type TSyscall struct {
	TInterrupthandler
}

const (
	SysHætta	uint32	= 1
	Sysfork		uint32	= 2
	SysLestur	uint32	= 3
	SysSkrift	uint32	= 4
	SysOpna		uint32	= 5
	SysLoka		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysaðgangur	uint32	= 33
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
	SysrtHætta	uint32	= 252

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
	hámarkfd		= 32
	hámarkOpnafiles		= 128
)

type fdentry struct {
	notað	bool
	lýsing	int32
	fdflags	uint32
}

type opnaSkráLýsing struct {
	notað		bool
	refs		uint32
	kind		uint32
	flags		uint32
	staða		uint32
	stærð		uint32
	heiti		[12]byte
	heitilen	uint32
	aux		uint32
}

const (
	fdkindEkkert			uint32	= 0
	fdkindfat			uint32	= 1
	fdkindstdin			uint32	= 2
	fdkindconsole			uint32	= 3
	fdkindKerfisstjórirootmappa	uint32	= 4
	fdkindSökkull			uint32	= 5

	oLesturonly	uint32	= 0
	oSkriftonly	uint32	= 1
	oLesturSkrift	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	omappa		uint32	= 0x10000

	seekSetja	uint32	= 0
	seekNúverandi	uint32	= 1
	seekend		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fSetjafd	uint32	= 2
	fgetfl		uint32	= 3
	fSetjafl	uint32	= 4
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
	hámarksockets		= 32
	hámarkSökkullpakkar	= 8
	hámarkdatagramStærð	= 512
)

type sökkulladdressipv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type sökkullpacket struct {
	notað	bool
	stærð	uint32
	uppruni	sökkulladdressipv4
	data	[hámarkdatagramStærð]byte
}

type staðbundiðdatagramSökkull struct {
	notað		bool
	bound		bool
	connected	bool
	staðbundið	sökkulladdressipv4
	fjarlægt	sökkulladdressipv4
	head		uint32
	tail		uint32
	count		uint32
	pakkar		[hámarkSökkullpakkar]sökkullpacket
}

type posixstat struct {
	Tæki		uint32
	Ino		uint32
	HAMUR		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Stærð_2		int32
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
	Version		[65]byte
	Machine		[65]byte
}

const (
	hámarkKeyravectorentry		= 16
	hámarkKeyraStrengurLengd	= 63
)

type keyravector struct {
	count	uint32
	lengths	[hámarkKeyravectorentry]uint32
	gildi_2	[hámarkKeyravectorentry][hámarkKeyraStrengurLengd + 1]byte
}

type processentry struct {
	notað		bool
	pid		uint32
	foreldri	uint32
	exited		bool
	staða_3		uint32
	forritbreak	uint32
	fds		[hámarkfd]fdentry
}

type strengurheader struct {
	Data	uintptr
	Len	int
}

func syscallVilla(villa int32) uint32 {
	return *(*uint32)(Pointer(&villa))
}

var opnaSkráTafla [hámarkOpnafiles]opnaSkráLýsing
var processTafla [32]processentry
var staðbundiðsockets [hámarksockets]staðbundiðdatagramSökkull
var næstaephemeralport uint16 = 49152

const (
	notandiheapbase		uint32	= 0x06000000
	notandiheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinLestur uint32
var stdinSkrift uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysHætta_2(index uint32) {
	Syscall(SysHætta, index)
}

func SysLestur_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysLestur, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysPrentastr(buffer string) {
	h := (*strengurheader)(Pointer(&buffer))
	Syscall(SysSkrift, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysPrentaunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysSkrift, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOpna_2(sLÓÐ uintptr, flags uint32, hAMUR uint32) int32 {
	return int32(Syscall(SysOpna, uint32(sLÓÐ), flags, hAMUR))
}

func SysLoka_2(fd uint32) int32 {
	return int32(Syscall(SysLoka, fd))
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
		return syscallVilla(Enosys)
	}
}

func (sjálft *TSyscall) Init(manager *TInterruptmanager) {
	initSkrádescriptor()

	interrupthandler = haldfanginterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	sjálft.TInterrupthandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var interrupthandler func(uint32) uint32

func haldfanginterrupt(esp uint32) uint32 {
	var cpu = (*TcpuStaða)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SysHætta:
		sysHætta(cpu.Ebx)
		return uint32(uintptr(Pointer(StöðvaNúverandithread(cpu))))
	case SysrtHætta:
		sysHætta(cpu.Ebx)
		return uint32(uintptr(Pointer(StöðvaNúverandithread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysLestur:
		cpu.Eax = uint32(sysLestur(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysSkrift:
		cpu.Eax = uint32(sysSkrift(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysOpna:
		cpu.Eax = uint32(sysOpna(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysOpna(cpu.Ebx, ocreate|oSkriftonly|otruncate, cpu.Ecx))
		return esp
	case SysLoka:
		cpu.Eax = uint32(sysLoka(int32(cpu.Ebx)))
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
		cpu.Eax = Núverandipid()
		return esp
	case Sysgetppid:
		cpu.Eax = Núverandiforeldripid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysaðgangur:
		cpu.Eax = uint32(sysaðgangur(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysSökkullcall(cpu.Ebx, cpu.Ecx))
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
		console_2.MUnsignedinteger32Prenta(cpu.Ebx)
		return esp

	default:
		console_2.MPrentaxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Prenta(esp)
		console_2.MPrenta(([]byte)(":"))
		console_2.MUnsignedinteger32Prenta(cpu.Eax)
		console_2.MPrenta(([]byte)(":"))
		console_2.MUnsignedinteger32Prenta(cpu.Ebx)
		console_2.MPrenta(([]byte)(":"))
		console_2.MUnsignedinteger32Prenta(cpu.Ecx)
		console_2.MPrenta(([]byte)(":"))
		console_2.MUnsignedinteger32Prenta(cpu.Edx)
		console_2.MPrenta(([]byte)("]"))
		cpu.Eax = syscallVilla(Enosys)
		return esp
	}

	return esp
}

func initSkrádescriptor() {
	for i := 0; i < hámarkOpnafiles; i++ {
		opnaSkráTafla[i] = opnaSkráLýsing{}
	}
	for i := 0; i < len(processTafla); i++ {
		processTafla[i] = processentry{}
	}
	for i := 0; i < len(staðbundiðsockets); i++ {
		staðbundiðsockets[i] = staðbundiðdatagramSökkull{}
	}
	næstaephemeralport = 49152
	opnaSkráTafla[0] = opnaSkráLýsing{notað: true, kind: fdkindstdin, flags: oLesturonly}
	opnaSkráTafla[1] = opnaSkráLýsing{notað: true, kind: fdkindconsole, flags: oSkriftonly}
	opnaSkráTafla[2] = opnaSkráLýsing{notað: true, kind: fdkindconsole, flags: oSkriftonly}
}

func finnaprocess(pid uint32) *processentry {
	for i := 0; i < len(processTafla); i++ {
		if processTafla[i].notað && processTafla[i].pid == pid {
			return &processTafla[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{notað: true, lýsing: fd}
		opnaSkráTafla[fd].refs++
	}
}

func ensureNúverandiprocess() *processentry {
	pid := Núverandipid()
	if process := finnaprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processTafla); i++ {
		if !processTafla[i].notað {
			processTafla[i] = processentry{
				notað:		true,
				pid:		pid,
				foreldri:	Núverandiforeldripid(),
				forritbreak:	notandiheapbase,
			}
			initializeprocessfds(&processTafla[i])
			return &processTafla[i]
		}
	}
	return nil
}

func getOpnaSkráfor(process *processentry, fd int32) *opnaSkráLýsing {
	if process == nil || fd < 0 || fd >= hámarkfd || !process.fds[fd].notað {
		return nil
	}
	lýsing := process.fds[fd].lýsing
	if lýsing < 0 || lýsing >= hámarkOpnafiles || !opnaSkráTafla[lýsing].notað {
		return nil
	}
	return &opnaSkráTafla[lýsing]
}

func getOpnaSkrá(fd int32) *opnaSkráLýsing {
	return getOpnaSkráfor(ensureNúverandiprocess(), fd)
}

func allocateOpnaSkrá() int32 {
	for i := int32(3); i < hámarkOpnafiles; i++ {
		if !opnaSkráTafla[i].notað {
			opnaSkráTafla[i] = opnaSkráLýsing{notað: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, lýsing int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= hámarkfd {
		return Einval
	}
	for fd := minimum; fd < hámarkfd; fd++ {
		if !process.fds[fd].notað {
			process.fds[fd] = fdentry{notað: true, lýsing: lýsing}
			return fd
		}
	}
	return Emfile
}

func releaseOpnaSkrá(lýsing int32) {
	if lýsing < 0 || lýsing >= hámarkOpnafiles {
		return
	}
	entry := &opnaSkráTafla[lýsing]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && lýsing > stderrfd {
		if entry.kind == fdkindSökkull && entry.aux < hámarksockets {
			staðbundiðsockets[entry.aux] = staðbundiðdatagramSökkull{}
		}
		*entry = opnaSkráLýsing{}
	}
}

func lokaprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getOpnaSkráfor(process, fd) == nil {
		return Ebadf
	}
	lýsing := process.fds[fd].lýsing
	process.fds[fd] = fdentry{}
	releaseOpnaSkrá(lýsing)
	return 0
}

func sysSkrift(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getOpnaSkrá(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindSökkull {
			return sökkullSendato(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindKerfisstjórirootmappa {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBætifromBendill(uintptr(address), int(count), int(count))
	console_2.MPrenta(buffer)
	return int32(count)
}

func sysLestur(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getOpnaSkrá(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return lesturstdin(address, count)
	}
	if entry.kind == fdkindKerfisstjórirootmappa {
		return Eisdir
	}
	if entry.kind == fdkindSökkull {
		return sökkullreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.staða >= entry.stærð {
		return 0
	}
	remaining := entry.stærð - entry.staða
	if count > remaining {
		count = remaining
	}
	buffer := GetBætifromBendill(uintptr(address), int(count), int(count))
	return lesturvfsSkrá(entry, buffer, count)
}

func sysOpna(sLÓÐaddress uint32, flags uint32, hAMUR uint32) int32 {
	_ = hAMUR
	if sLÓÐaddress == 0 {
		return Efault
	}
	aðgangurHAMUR := flags & 3
	if aðgangurHAMUR == oSkriftonly || aðgangurHAMUR == oLesturSkrift || (flags&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensureNúverandiprocess()
	if process == nil {
		return Enfile
	}
	lýsing := allocateOpnaSkrá()
	if lýsing < 0 {
		return lýsing
	}
	entry := &opnaSkráTafla[lýsing]
	entry.flags = flags
	if isKerfisstjórirootSLÓÐ(sLÓÐaddress) {
		entry.kind = fdkindKerfisstjórirootmappa
		entry.stærð = 0
	} else {
		heitilen, heiti := afritaSLÓÐ(sLÓÐaddress)
		if heitilen == 0 {
			*entry = opnaSkráLýsing{}
			return Enoent
		}
		stærð := skráStærð(heiti[:heitilen])
		if stærð == 0 {
			*entry = opnaSkráLýsing{}
			return Enoent
		}
		if (flags & omappa) != 0 {
			*entry = opnaSkráLýsing{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.stærð = stærð
		entry.heitilen = heitilen
		entry.heiti = heiti
	}

	fd := allocatefd(process, lýsing, 3)
	if fd < 0 {
		*entry = opnaSkráLýsing{}
		return fd
	}
	return fd
}

func sysLoka(fd int32) int32 {
	return lokaprocessfd(ensureNúverandiprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensureNúverandiprocess()
	entry := getOpnaSkráfor(process, fd)
	if entry == nil {
		return Ebadf
	}
	nýttfd := allocatefd(process, process.fds[fd].lýsing, minimum)
	if nýttfd >= 0 {
		entry.refs++
	}
	return nýttfd
}

func sysdup2(oldfd int32, nýttfd int32) int32 {
	process := ensureNúverandiprocess()
	entry := getOpnaSkráfor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if nýttfd < 0 || nýttfd >= hámarkfd {
		return Ebadf
	}
	if oldfd == nýttfd {
		return nýttfd
	}
	if process.fds[nýttfd].notað {
		lokaprocessfd(process, nýttfd)
	}
	process.fds[nýttfd] = fdentry{notað: true, lýsing: process.fds[oldfd].lýsing}
	entry.refs++
	return nýttfd
}

func sysfcntl(fd int32, skipun uint32, argument uint32) int32 {
	process := ensureNúverandiprocess()
	entry := getOpnaSkráfor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch skipun {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdflags)
	case fSetjafd:
		process.fds[fd].fdflags = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.flags)
	case fSetjafl:
		entry.flags = (entry.flags & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getOpnaSkrá(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekSetja:
		base = 0
	case seekNúverandi:
		base = int64(entry.staða)
	case seekend:
		base = int64(entry.stærð)
	default:
		return Einval
	}
	staða_2 := base + int64(offset)
	if staða_2 < 0 || staða_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.staða = uint32(staða_2)
	return int32(entry.staða)
}

func lesturvfsSkrá(entry *opnaSkráLýsing, áfangastaður_2 []byte, count uint32) int32 {
	minnimanager := &mem.TMinnimanager{}
	tmpBendill := minnimanager.Malloc(entry.stærð)
	if tmpBendill == nil {
		return Einval
	}
	tmp := GetBætifromBendill(uintptr(tmpBendill), int(entry.stærð), int(entry.stærð))
	lesturSkrá(entry.heiti[:entry.heitilen], tmp)
	copy(áfangastaður_2[:count], tmp[entry.staða:entry.staða+count])
	entry.staða += count
	minnimanager.Laust(tmpBendill)
	return int32(count)
}

func isKerfisstjórirootSLÓÐ(sLÓÐaddress uint32) bool {
	if sLÓÐaddress == 0 {
		return false
	}
	sLÓÐ := GetBætifromBendill(uintptr(sLÓÐaddress), 4, 4)
	if sLÓÐ[0] == '/' && sLÓÐ[1] == 0 {
		return true
	}
	if sLÓÐ[0] == '.' && sLÓÐ[1] == 0 {
		return true
	}
	if sLÓÐ[0] == '/' && sLÓÐ[1] == '.' && sLÓÐ[2] == 0 {
		return true
	}
	return false
}

func sysaðgangur(sLÓÐaddress uint32, hAMUR uint32) int32 {
	if sLÓÐaddress == 0 {
		return Efault
	}
	if (hAMUR & ^uint32(7)) != 0 {
		return Einval
	}
	isKerfisstjóriroot := isKerfisstjórirootSLÓÐ(sLÓÐaddress)
	exists := isKerfisstjóriroot
	if !exists {
		heitilen, heiti := afritaSLÓÐ(sLÓÐaddress)
		exists = heitilen != 0 && skráStærð(heiti[:heitilen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (hAMUR & 2) != 0 {
		return Eacces
	}

	if (hAMUR&1) != 0 && !isKerfisstjóriroot {
		return Eacces
	}
	return 0
}

func syschdir(sLÓÐaddress uint32) int32 {
	if sLÓÐaddress == 0 {
		return Efault
	}
	if !isKerfisstjórirootSLÓÐ(sLÓÐaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, stærð uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if stærð < 2 {
		return Erange
	}
	buffer_2 := GetBætifromBendill(uintptr(bufferaddress), int(stærð), int(stærð))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, hAMUR uint32, stærð uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Tæki = 1
	stat.Ino = inode
	stat.HAMUR = hAMUR
	stat.Nlink = 1
	stat.Stærð_2 = int32(stærð)
	stat.Blksize = 512
	stat.Blokk = int32((stærð + 511) / 512)
	return 0
}

func sysstat(sLÓÐaddress uint32, stataddress uint32) int32 {
	if sLÓÐaddress == 0 {
		return Efault
	}
	if isKerfisstjórirootSLÓÐ(sLÓÐaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	heitilen, heiti := afritaSLÓÐ(sLÓÐaddress)
	if heitilen == 0 {
		return Enoent
	}
	stærð := skráStærð(heiti[:heitilen])
	if stærð == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < heitilen; i++ {
		inode = inode*33 + uint32(heiti[i])
	}
	return fillposixstat(stataddress, sifreg|0444, stærð, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getOpnaSkrá(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindKerfisstjórirootmappa:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.stærð, uint32(fd+2))
	case fdkindSökkull:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getOpnaSkrá(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensureNúverandiprocess()
	if process == nil {
		return 0
	}
	if process.forritbreak == 0 {
		process.forritbreak = notandiheapbase
	}
	if address_2 == 0 {
		return process.forritbreak
	}
	if address_2 < notandiheapbase || address_2 > notandiheaplimit {
		return process.forritbreak
	}
	process.forritbreak = address_2
	return process.forritbreak
}

func afritautsfield(áfangastaður *[65]byte, gildi string) {
	limit := len(gildi)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		áfangastaður[i] = gildi[i]
	}
	áfangastaður[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	heiti := (*posixutsname)(Pointer(uintptr(address_2)))
	*heiti = posixutsname{}
	afritautsfield(&heiti.Sysname, "EngOS")
	afritautsfield(&heiti.Nodename, "engos")
	afritautsfield(&heiti.Release, "0.1-posix")
	afritautsfield(&heiti.Version, "POSIX.1-2017 phase 1")
	afritautsfield(&heiti.Machine, "i386")
	return 0
}

func swapunsignedinteger16(gildi uint16) uint16 {
	return (gildi << 8) | (gildi >> 8)
}

func sökkullcallargument(viðföng_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(viðföng_2 + index*4)))
}

func sökkullforfd(fd int32) (*staðbundiðdatagramSökkull, int32) {
	entry := getOpnaSkrá(fd)
	if entry == nil || entry.kind != fdkindSökkull || entry.aux >= hámarksockets {
		return nil, Ebadf
	}
	sökkull := &staðbundiðsockets[entry.aux]
	if !sökkull.notað {
		return nil, Ebadf
	}
	return sökkull, 0
}

func allocateSökkull(lén uint32, sökkullTegund uint32, protocol uint32) int32 {
	if lén != afinet {
		return Eafnosupport
	}
	if sökkullTegund != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensureNúverandiprocess()
	if process == nil {
		return Enfile
	}
	sökkullindex := -1
	for i := 0; i < hámarksockets; i++ {
		if !staðbundiðsockets[i].notað {
			sökkullindex = i
			break
		}
	}
	if sökkullindex < 0 {
		return Enfile
	}
	lýsing := allocateOpnaSkrá()
	if lýsing < 0 {
		return lýsing
	}
	staðbundiðsockets[sökkullindex] = staðbundiðdatagramSökkull{notað: true}
	entry := &opnaSkráTafla[lýsing]
	entry.kind = fdkindSökkull
	entry.flags = oLesturSkrift
	entry.aux = uint32(sökkullindex)
	fd := allocatefd(process, lýsing, 3)
	if fd < 0 {
		staðbundiðsockets[sökkullindex] = staðbundiðdatagramSökkull{}
		*entry = opnaSkráLýsing{}
		return fd
	}
	return fd
}

func sökkulladdress(address_2 uint32, lengd uint32) (*sökkulladdressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if lengd < 16 {
		return nil, Einval
	}
	nIÐURSTAÐA := (*sökkulladdressipv4)(Pointer(uintptr(address_2)))
	if nIÐURSTAÐA.Family != afinet {
		return nil, Eafnosupport
	}
	return nIÐURSTAÐA, 0
}

func portInnuse(port uint16, except *staðbundiðdatagramSökkull) bool {
	for i := 0; i < hámarksockets; i++ {
		sökkull := &staðbundiðsockets[i]
		if sökkull != except && sökkull.notað && sökkull.bound && sökkull.staðbundið.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(sökkull *staðbundiðdatagramSökkull) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapunsignedinteger16(næstaephemeralport)
		næstaephemeralport++
		if næstaephemeralport < 49152 {
			næstaephemeralport = 49152
		}
		if !portInnuse(port, sökkull) {
			sökkull.staðbundið = sökkulladdressipv4{Family: afinet, Port: port, Address: 0x0100007F}
			sökkull.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func sökkullbind(fd int32, address_2 uint32, lengd uint32) int32 {
	sökkull, villa := sökkullforfd(fd)
	if villa != 0 {
		return villa
	}
	requested, villa := sökkulladdress(address_2, lengd)
	if villa != 0 {
		return villa
	}
	if sökkull.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(sökkull)
	}
	if portInnuse(requested.Port, sökkull) {
		return Eaddrinuse
	}
	sökkull.staðbundið = *requested
	sökkull.bound = true
	return 0
}

func sökkullTengjast(fd int32, address_2 uint32, lengd uint32) int32 {
	sökkull, villa := sökkullforfd(fd)
	if villa != 0 {
		return villa
	}
	fjarlægt, villa := sökkulladdress(address_2, lengd)
	if villa != 0 {
		return villa
	}
	if !sökkull.bound {
		if villa := bindephemeral(sökkull); villa != 0 {
			return villa
		}
	}
	sökkull.fjarlægt = *fjarlægt
	sökkull.connected = true
	return 0
}

func sökkullSendato(fd int32, bufferaddress_2 uint32, lengd uint32, áfangastaðuraddress uint32, áfangastaðurLengd uint32) int32 {
	sökkull, villa := sökkullforfd(fd)
	if villa != 0 {
		return villa
	}
	if lengd > hámarkdatagramStærð {
		return Emsgsize
	}
	if lengd != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var áfangastaður sökkulladdressipv4
	if áfangastaðuraddress != 0 {
		address_2, addressVilla := sökkulladdress(áfangastaðuraddress, áfangastaðurLengd)
		if addressVilla != 0 {
			return addressVilla
		}
		áfangastaður = *address_2
	} else {
		if !sökkull.connected {
			return Enotconn
		}
		áfangastaður = sökkull.fjarlægt
	}
	if !sökkull.bound {
		if bindVilla := bindephemeral(sökkull); bindVilla != 0 {
			return bindVilla
		}
	}
	var receiver *staðbundiðdatagramSökkull
	for i := 0; i < hámarksockets; i++ {
		candidate := &staðbundiðsockets[i]
		if candidate.notað && candidate.bound && candidate.staðbundið.Port == áfangastaður.Port &&
			(candidate.staðbundið.Address == 0 || candidate.staðbundið.Address == áfangastaður.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= hámarkSökkullpakkar {
		return Eagain
	}
	packet := &receiver.pakkar[receiver.tail]
	*packet = sökkullpacket{notað: true, stærð: lengd, uppruni: sökkull.staðbundið}
	if lengd != 0 {
		uppruni := GetBætifromBendill(uintptr(bufferaddress_2), int(lengd), int(lengd))
		copy(packet.data[:lengd], uppruni)
	}
	receiver.tail = (receiver.tail + 1) % hámarkSökkullpakkar
	receiver.count++
	return int32(lengd)
}

func sökkullreceivefrom(fd int32, bufferaddress_2 uint32, lengd uint32, uppruniaddress uint32, uppruniLengdaddress uint32) int32 {
	sökkull, villa := sökkullforfd(fd)
	if villa != 0 {
		return villa
	}
	if lengd != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if sökkull.count == 0 {
		return Eagain
	}
	packet := &sökkull.pakkar[sökkull.head]
	afritaLengd := packet.stærð
	if afritaLengd > lengd {
		afritaLengd = lengd
	}
	if afritaLengd != 0 {
		áfangastaður := GetBætifromBendill(uintptr(bufferaddress_2), int(afritaLengd), int(afritaLengd))
		copy(áfangastaður, packet.data[:afritaLengd])
	}
	if uppruniaddress != 0 {
		if uppruniLengdaddress == 0 {
			return Efault
		}
		providedLengd := (*uint32)(Pointer(uintptr(uppruniLengdaddress)))
		if *providedLengd >= 16 {
			*(*sökkulladdressipv4)(Pointer(uintptr(uppruniaddress))) = packet.uppruni
		}
		*providedLengd = 16
	}
	*packet = sökkullpacket{}
	sökkull.head = (sökkull.head + 1) % hámarkSökkullpakkar
	sökkull.count--
	return int32(afritaLengd)
}

func afritaSökkullHeiti(fd int32, address_2 uint32, lengdaddress uint32, peer bool) int32 {
	sökkull, villa := sökkullforfd(fd)
	if villa != 0 {
		return villa
	}
	if address_2 == 0 || lengdaddress == 0 {
		return Efault
	}
	lengd := (*uint32)(Pointer(uintptr(lengdaddress)))
	if *lengd < 16 {
		*lengd = 16
		return Einval
	}
	if peer {
		if !sökkull.connected {
			return Enotconn
		}
		*(*sökkulladdressipv4)(Pointer(uintptr(address_2))) = sökkull.fjarlægt
	} else {
		if !sökkull.bound {
			if bindVilla := bindephemeral(sökkull); bindVilla != 0 {
				return bindVilla
			}
		}
		*(*sökkulladdressipv4)(Pointer(uintptr(address_2))) = sökkull.staðbundið
	}
	*lengd = 16
	return 0
}

func sysSökkullcall(call uint32, viðföng_2 uint32) int32 {
	if viðföng_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateSökkull(sökkullcallargument(viðföng_2, 0), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2))
	case 2:
		return sökkullbind(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2))
	case 3:
		return sökkullTengjast(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return afritaSökkullHeiti(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), false)
	case 7:
		return afritaSökkullHeiti(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), true)
	case 9:
		return sökkullSendato(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), 0, 0)
	case 10:
		return sökkullreceivefrom(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), 0, 0)
	case 11:
		return sökkullSendato(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), sökkullcallargument(viðföng_2, 4), sökkullcallargument(viðföng_2, 5))
	case 12:
		return sökkullreceivefrom(int32(sökkullcallargument(viðföng_2, 0)), sökkullcallargument(viðföng_2, 1), sökkullcallargument(viðföng_2, 2), sökkullcallargument(viðföng_2, 4), sökkullcallargument(viðföng_2, 5))
	case 13:
		if _, villa := sökkullforfd(int32(sökkullcallargument(viðföng_2, 0))); villa != 0 {
			return villa
		}
		return 0
	case 14:
		if _, villa := sökkullforfd(int32(sökkullcallargument(viðföng_2, 0))); villa != 0 {
			return villa
		}
		return 0
	}
	return Eopnotsupp
}

func lesturstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBætifromBendill(uintptr(address), int(count), int(count))
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
	næsta := (stdinSkrift + 1) % uint32(len(stdinbuffer))
	if næsta == stdinLestur {
		return
	}
	stdinbuffer[stdinSkrift] = c
	stdinSkrift = næsta
}

func stdingetblocking() byte {
	for stdinLestur == stdinSkrift {
		sc := pollLyklaborðscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinLestur]
	stdinLestur = (stdinLestur + 1) % uint32(len(stdinbuffer))
	return c
}

func pollLyklaborðscancode() byte {
	for (PortLesturbyte(0x64) & 0x01) == 0 {
	}
	sc := PortLesturbyte(0x60)
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

func afritaKeyravector(address_2 uint32, nIÐURSTAÐA *keyravector) int32 {
	*nIÐURSTAÐA = keyravector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < hámarkKeyravectorentry; index++ {
		strenguraddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if strenguraddress == 0 {
			nIÐURSTAÐA.count = index
			return 0
		}
		terminated := false
		for lengd := uint32(0); lengd <= hámarkKeyraStrengurLengd; lengd++ {
			gildi := *(*byte)(Pointer(uintptr(strenguraddress + lengd)))
			nIÐURSTAÐA.gildi_2[index][lengd] = gildi
			if gildi == 0 {
				nIÐURSTAÐA.lengths[index] = lengd
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

func pushKeyraunsignedinteger32(stack *uint32, gildi uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = gildi
}

func setupKeyrastack(cpu *TcpuStaða, viðföng_2 *keyravector, environment *keyravector) int32 {
	const stackBæti uint32 = 4096
	if !MakeSviðLokaðprivatewritable(getcr3(), NotandistackEfst-stackBæti, stackBæti) {
		return Enomem
	}
	stack := NotandistackEfst
	var argumentpointers [hámarkKeyravectorentry]uint32
	var environmentpointers [hámarkKeyravectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		lengd := environment.lengths[i] + 1
		stack -= lengd
		áfangastaður := GetBætifromBendill(uintptr(stack), int(lengd), int(lengd))
		copy(áfangastaður, environment.gildi_2[i][:lengd])
		environmentpointers[i] = stack
	}
	for i := int(viðföng_2.count) - 1; i >= 0; i-- {
		lengd := viðföng_2.lengths[i] + 1
		stack -= lengd
		áfangastaður := GetBætifromBendill(uintptr(stack), int(lengd), int(lengd))
		copy(áfangastaður, viðföng_2.gildi_2[i][:lengd])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushKeyraunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushKeyraunsignedinteger32(&stack, environmentpointers[i])
	}
	pushKeyraunsignedinteger32(&stack, 0)
	for i := int(viðföng_2.count) - 1; i >= 0; i-- {
		pushKeyraunsignedinteger32(&stack, argumentpointers[i])
	}
	pushKeyraunsignedinteger32(&stack, viðföng_2.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func lokaNotaKeyra(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < hámarkfd; fd++ {
		if process.fds[fd].notað && (process.fds[fd].fdflags&fdcloexec) != 0 {
			lokaprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *TcpuStaða, sLÓÐaddress uint32) int32 {
	if sLÓÐaddress == 0 {
		return Efault
	}
	var viðföng_2 keyravector
	var environment keyravector
	if nIÐURSTAÐA := afritaKeyravector(cpu.Ecx, &viðföng_2); nIÐURSTAÐA < 0 {
		return nIÐURSTAÐA
	}
	if nIÐURSTAÐA := afritaKeyravector(cpu.Edx, &environment); nIÐURSTAÐA < 0 {
		return nIÐURSTAÐA
	}
	heitilen, heiti := afritaSLÓÐ(sLÓÐaddress)
	if heitilen == 0 {
		return Enoent
	}
	stærð := skráStærð(heiti[:heitilen])
	if stærð == 0 {
		return Enoent
	}
	minnimanager := &mem.TMinnimanager{}
	skráBendill := minnimanager.Malloc(stærð)
	if skráBendill == nil {
		return Einval
	}
	data := GetBætifromBendill(uintptr(skráBendill), int(stærð), int(stærð))
	lesturSkrá(heiti[:heitilen], data)
	if stærð < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		minnimanager.Laust(skráBendill)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	minnimanager.Laust(skráBendill)
	if nIÐURSTAÐA := setupKeyrastack(cpu, &viðföng_2, &environment); nIÐURSTAÐA < 0 {
		return nIÐURSTAÐA
	}
	lokaNotaKeyra(ensureNúverandiprocess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *TcpuStaða) int32 {
	foreldripid := Núverandipid()
	if ensureNúverandiprocess() == nil {
		return Enfile
	}
	pid := allocateprocess(foreldripid)
	if pid == 0 {
		return Einval
	}
	minnimanager := &mem.TMinnimanager{}
	threadBendill := minnimanager.Malloc(uint32(Sizeof(TThread{})))
	stackBendill := minnimanager.Malloc(ThreadstackStærð)
	afkvæmisíðamappa := CloneaddressBilslácow(getcr3())
	if threadBendill == nil || stackBendill == nil || afkvæmisíðamappa == 0 {
		discardprocess(pid)
		return Einval
	}
	afkvæmi := (*TThread)(threadBendill)
	afkvæmi.Stack = uint32(uintptr(stackBendill))
	afkvæmi.CpuStaða = (*TcpuStaða)(Pointer(uintptr(stackBendill) + ThreadstackStærð - Sizeof(TcpuStaða{})))
	*afkvæmi.CpuStaða = *cpu
	afkvæmi.CpuStaða.Eax = 0
	afkvæmi.Notandistack_2 = cpu.Esp
	afkvæmi.NotandistackStærð_2 = 0
	afkvæmi.Pid = pid
	afkvæmi.Foreldripid = foreldripid
	afkvæmi.Síðamappaentry = afkvæmisíðamappa
	afkvæmi.ThreadStaða = Tilbúið
	afkvæmi.Fpuoffset = 0xffffffff
	afkvæmi.Iskernel = false
	Bætaviðrunnablethread(afkvæmi)
	return int32(pid)
}

func sysHætta(staða_3 uint32) {
	pid := Núverandipid()
	for i := 0; i < len(processTafla); i++ {
		if processTafla[i].notað && processTafla[i].pid == pid {
			lokaAlltprocessfds(&processTafla[i])
			processTafla[i].exited = true
			processTafla[i].staða_3 = (staða_3 & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, staðaaddress uint32, valkostir uint32) int32 {
	if (valkostir & ^uint32(1)) != 0 {
		return Einval
	}
	foreldripid := Núverandipid()
	foundafkvæmi := false
	for i := 0; i < len(processTafla); i++ {
		p := &processTafla[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.notað && matches && p.foreldri == foreldripid {
			foundafkvæmi = true
			if p.exited {
				if staðaaddress != 0 {
					*(*uint32)(Pointer(uintptr(staðaaddress))) = p.staða_3
				}
				afkvæmipid := p.pid
				*p = processentry{}
				return int32(afkvæmipid)
			}
		}
	}
	if !foundafkvæmi {
		return Echild
	}

	if (valkostir & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(foreldri uint32) uint32 {
	foreldriprocess := finnaprocess(foreldri)
	pid := Allocatepid()
	for i := 0; i < len(processTafla); i++ {
		if !processTafla[i].notað {
			processTafla[i] = processentry{
				notað:		true,
				pid:		pid,
				foreldri:	foreldri,
				forritbreak:	notandiheapbase,
			}
			if foreldriprocess != nil {
				processTafla[i].forritbreak = foreldriprocess.forritbreak
				for fd := 0; fd < hámarkfd; fd++ {
					if foreldriprocess.fds[fd].notað {
						processTafla[i].fds[fd] = foreldriprocess.fds[fd]
						lýsing := foreldriprocess.fds[fd].lýsing
						if lýsing >= 0 && lýsing < hámarkOpnafiles {
							opnaSkráTafla[lýsing].refs++
						}
					}
				}
			} else {
				initializeprocessfds(&processTafla[i])
			}
			return pid
		}
	}
	return 0
}

func lokaAlltprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < hámarkfd; fd++ {
		if process.fds[fd].notað {
			lokaprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := finnaprocess(pid)
	if process == nil {
		return
	}
	lokaAlltprocessfds(process)
	*process = processentry{}
}

func afritaSLÓÐ(sLÓÐaddress uint32) (uint32, [12]byte) {
	var heiti [12]byte
	if sLÓÐaddress == 0 {
		return 0, heiti
	}
	raw := GetBætifromBendill(uintptr(sLÓÐaddress), 64, 64)
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
		heiti[n] = c
		n++
	}
	return n, heiti
}

func skráStærð(skráarheiti []byte) uint32 {
	var ata0s = TNánarTækniattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTafla{}
	partition.Lesturpartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	stærð := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti)
	ata0s.Flush()
	return stærð
}

func lesturSkrá(skráarheiti []byte, data []byte) {
	var ata0s = TNánarTækniattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTafla{}
	partition.Lesturpartition(&ata0s)

	bios := TBiosparameterBlokk32{}
	bios.Lestur(&ata0s, partition.Mbr.Primarypartition[0], skráarheiti, data)
	ata0s.Flush()
}

func getcr3() uint32
