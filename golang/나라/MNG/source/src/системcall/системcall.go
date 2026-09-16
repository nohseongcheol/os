/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package системcall

import . "unsafe"

import . "interrupt"
import . "консол"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "файлСистем/msdospartition"
import . "файлСистем/fat"
import . "файлСистем/elf"
import mem "санахойЗохицуулагч"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualСанахой"

var консол_2 = TКонсол{}

type TSyscall struct {
	TInterrupthandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	SysУнших	uint32	= 3
	SysБичих	uint32	= 4
	SysНээх		uint32	= 5
	SysХаах		uint32	= 6
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
	maxНээхФайлууд		= 128
)

type fdentry struct {
	хэрэглэгдсэн	bool
	тодорхойлолт	int32
	fdТөлвүүд	uint32
}

type нээхФайлТодорхойлолт struct {
	хэрэглэгдсэн	bool
	refs		uint32
	kind		uint32
	төлвүүд		uint32
	position	uint32
	хэмжээ		uint32
	нэр		[12]byte
	нэрlen		uint32
	aux		uint32
}

const (
	fdkindХоосон		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindКонсол		uint32	= 3
	fdkindrootЛавлах	uint32	= 4
	fdkindsocket		uint32	= 5

	oУншихonly	uint32	= 0
	oБичихonly	uint32	= 1
	oУншихБичих	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oЛавлах		uint32	= 0x10000

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
	maxdatagramХэмжээ	= 512
)

type socketaddressiОу4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	хэрэглэгдсэн	bool
	хэмжээ		uint32
	эх		socketaddressiОу4
	data		[maxdatagramХэмжээ]byte
}

type localdatagramsocket struct {
	хэрэглэгдсэн	bool
	bound		bool
	connected	bool
	local		socketaddressiОу4
	remote		socketaddressiОу4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxsocketpackets]socketpacket
}

type posixstat struct {
	Төхөөрөмж	uint32
	Ino		uint32
	Горим		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Хэмжээ_2	int32
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
	maxexecБИЧВЭРlength	= 63
)

type execvector struct {
	count	uint32
	lengths	[maxexecvectorentry]uint32
	values	[maxexecvectorentry][maxexecБИЧВЭРlength + 1]byte
}

type processentry struct {
	хэрэглэгдсэн	bool
	pid		uint32
	parent		uint32
	exited		bool
	төлөв		uint32
	програмbreak	uint32
	fds		[maxfd]fdentry
}

type бИЧВЭРheader struct {
	Data	uintptr
	Len	int
}

func syscallАлдаа(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var нээхФайлtable [maxНээхФайлууд]нээхФайлТодорхойлолт
var processtable [32]processentry
var localsockets [maxsockets]localdatagramsocket
var дараахephemeralПорт uint16 = 49152

const (
	хэрэглэгчheapbase	uint32	= 0x06000000
	хэрэглэгчheaplimit	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinУнших uint32
var stdinБичих uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(үзүүлэлт uint32) {
	Syscall(Sysexit, үзүүлэлт)
}

func SysУнших_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysУнших, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysХэвлэхstr(buffer string) {
	h := (*бИЧВЭРheader)(Pointer(&buffer))
	Syscall(SysБичих, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysХэвлэхunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysБичих, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysНээх_2(зАМ uintptr, төлвүүд uint32, горим uint32) int32 {
	return int32(Syscall(SysНээх, uint32(зАМ), төлвүүд, горим))
}

func SysХаах_2(fd uint32) int32 {
	return int32(Syscall(SysХаах, fd))
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
		return syscallАлдаа(Enosys)
	}
}

func (self *TSyscall) Init(зохицуулагч *TInterruptЗохицуулагч) {
	initФайлdescriptor()

	interrupthandler = handleinterrupt

	var address uintptr
	address = uintptr(Pointer(&interrupthandler))

	self.TInterrupthandler.Init(0x80, uintptr(Pointer(зохицуулагч)), address)
}

var interrupthandler func(uint32) uint32

func handleinterrupt(esp uint32) uint32 {
	var cpu = (*Tcpustate)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Зогсcurrentthread(cpu))))
	case Sysrtexit:
		sysexit(cpu.Ebx)
		return uint32(uintptr(Pointer(Зогсcurrentthread(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case SysУнших:
		cpu.Eax = uint32(sysУнших(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysБичих:
		cpu.Eax = uint32(sysБичих(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SysНээх:
		cpu.Eax = uint32(sysНээх(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysНээх(cpu.Ebx, ocreate|oБичихonly|otruncate, cpu.Ecx))
		return esp
	case SysХаах:
		cpu.Eax = uint32(sysХаах(int32(cpu.Ebx)))
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
		консол_2.MUnsignedinteger32Хэвлэх(cpu.Ebx)
		return esp

	default:
		консол_2.MХэвлэхxy(([]byte)("sys["), 1, 23)
		консол_2.MUnsignedinteger32Хэвлэх(esp)
		консол_2.MХэвлэх(([]byte)(":"))
		консол_2.MUnsignedinteger32Хэвлэх(cpu.Eax)
		консол_2.MХэвлэх(([]byte)(":"))
		консол_2.MUnsignedinteger32Хэвлэх(cpu.Ebx)
		консол_2.MХэвлэх(([]byte)(":"))
		консол_2.MUnsignedinteger32Хэвлэх(cpu.Ecx)
		консол_2.MХэвлэх(([]byte)(":"))
		консол_2.MUnsignedinteger32Хэвлэх(cpu.Edx)
		консол_2.MХэвлэх(([]byte)("]"))
		cpu.Eax = syscallАлдаа(Enosys)
		return esp
	}

	return esp
}

func initФайлdescriptor() {
	for i := 0; i < maxНээхФайлууд; i++ {
		нээхФайлtable[i] = нээхФайлТодорхойлолт{}
	}
	for i := 0; i < len(processtable); i++ {
		processtable[i] = processentry{}
	}
	for i := 0; i < len(localsockets); i++ {
		localsockets[i] = localdatagramsocket{}
	}
	дараахephemeralПорт = 49152
	нээхФайлtable[0] = нээхФайлТодорхойлолт{хэрэглэгдсэн: true, kind: fdkindstdin, төлвүүд: oУншихonly}
	нээхФайлtable[1] = нээхФайлТодорхойлолт{хэрэглэгдсэн: true, kind: fdkindКонсол, төлвүүд: oБичихonly}
	нээхФайлtable[2] = нээхФайлТодорхойлолт{хэрэглэгдсэн: true, kind: fdkindКонсол, төлвүүд: oБичихonly}
}

func хайхprocess(pid uint32) *processentry {
	for i := 0; i < len(processtable); i++ {
		if processtable[i].хэрэглэгдсэн && processtable[i].pid == pid {
			return &processtable[i]
		}
	}
	return nil
}

func initializeprocessfds(process *processentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		process.fds[fd] = fdentry{хэрэглэгдсэн: true, тодорхойлолт: fd}
		нээхФайлtable[fd].refs++
	}
}

func ensurecurrentprocess() *processentry {
	pid := Currentpid()
	if process := хайхprocess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].хэрэглэгдсэн {
			processtable[i] = processentry{
				хэрэглэгдсэн:	true,
				pid:		pid,
				parent:		Currentparentpid(),
				програмbreak:	хэрэглэгчheapbase,
			}
			initializeprocessfds(&processtable[i])
			return &processtable[i]
		}
	}
	return nil
}

func getНээхФайлfor(process *processentry, fd int32) *нээхФайлТодорхойлолт {
	if process == nil || fd < 0 || fd >= maxfd || !process.fds[fd].хэрэглэгдсэн {
		return nil
	}
	тодорхойлолт := process.fds[fd].тодорхойлолт
	if тодорхойлолт < 0 || тодорхойлолт >= maxНээхФайлууд || !нээхФайлtable[тодорхойлолт].хэрэглэгдсэн {
		return nil
	}
	return &нээхФайлtable[тодорхойлолт]
}

func getНээхФайл(fd int32) *нээхФайлТодорхойлолт {
	return getНээхФайлfor(ensurecurrentprocess(), fd)
}

func allocateНээхФайл() int32 {
	for i := int32(3); i < maxНээхФайлууд; i++ {
		if !нээхФайлtable[i].хэрэглэгдсэн {
			нээхФайлtable[i] = нээхФайлТодорхойлолт{хэрэглэгдсэн: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(process *processentry, тодорхойлолт int32, minimum int32) int32 {
	if process == nil {
		return Enfile
	}
	if minimum < 0 || minimum >= maxfd {
		return Einval
	}
	for fd := minimum; fd < maxfd; fd++ {
		if !process.fds[fd].хэрэглэгдсэн {
			process.fds[fd] = fdentry{хэрэглэгдсэн: true, тодорхойлолт: тодорхойлолт}
			return fd
		}
	}
	return Emfile
}

func releaseНээхФайл(тодорхойлолт int32) {
	if тодорхойлолт < 0 || тодорхойлолт >= maxНээхФайлууд {
		return
	}
	entry := &нээхФайлtable[тодорхойлолт]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && тодорхойлолт > stderrfd {
		if entry.kind == fdkindsocket && entry.aux < maxsockets {
			localsockets[entry.aux] = localdatagramsocket{}
		}
		*entry = нээхФайлТодорхойлолт{}
	}
}

func хаахprocessfd(process *processentry, fd int32) int32 {
	if process == nil || getНээхФайлfor(process, fd) == nil {
		return Ebadf
	}
	тодорхойлолт := process.fds[fd].тодорхойлолт
	process.fds[fd] = fdentry{}
	releaseНээхФайл(тодорхойлолт)
	return 0
}

func sysБичих(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getНээхФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindКонсол {
		if entry.kind == fdkindsocket {
			return socketsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindrootЛавлах {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтfrompointer(uintptr(address), int(count), int(count))
	консол_2.MХэвлэх(buffer)
	return int32(count)
}

func sysУнших(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getНээхФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return уншихstdin(address, count)
	}
	if entry.kind == fdkindrootЛавлах {
		return Eisdir
	}
	if entry.kind == fdkindsocket {
		return socketreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.хэмжээ {
		return 0
	}
	remaining := entry.хэмжээ - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := GetБайтfrompointer(uintptr(address), int(count), int(count))
	return уншихvfsФайл(entry, buffer, count)
}

func sysНээх(зАМaddress uint32, төлвүүд uint32, горим uint32) int32 {
	_ = горим
	if зАМaddress == 0 {
		return Efault
	}
	accessГорим := төлвүүд & 3
	if accessГорим == oБичихonly || accessГорим == oУншихБичих || (төлвүүд&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	тодорхойлолт := allocateНээхФайл()
	if тодорхойлолт < 0 {
		return тодорхойлолт
	}
	entry := &нээхФайлtable[тодорхойлолт]
	entry.төлвүүд = төлвүүд
	if isrootЗАМ(зАМaddress) {
		entry.kind = fdkindrootЛавлах
		entry.хэмжээ = 0
	} else {
		нэрlen, нэр := хуулахЗАМ(зАМaddress)
		if нэрlen == 0 {
			*entry = нээхФайлТодорхойлолт{}
			return Enoent
		}
		хэмжээ := файлХэмжээ(нэр[:нэрlen])
		if хэмжээ == 0 {
			*entry = нээхФайлТодорхойлолт{}
			return Enoent
		}
		if (төлвүүд & oЛавлах) != 0 {
			*entry = нээхФайлТодорхойлолт{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.хэмжээ = хэмжээ
		entry.нэрlen = нэрlen
		entry.нэр = нэр
	}

	fd := allocatefd(process, тодорхойлолт, 3)
	if fd < 0 {
		*entry = нээхФайлТодорхойлолт{}
		return fd
	}
	return fd
}

func sysХаах(fd int32) int32 {
	return хаахprocessfd(ensurecurrentprocess(), fd)
}

func sysdup(fd int32, minimum int32) int32 {
	process := ensurecurrentprocess()
	entry := getНээхФайлfor(process, fd)
	if entry == nil {
		return Ebadf
	}
	шинэfd := allocatefd(process, process.fds[fd].тодорхойлолт, minimum)
	if шинэfd >= 0 {
		entry.refs++
	}
	return шинэfd
}

func sysdup2(oldfd int32, шинэfd int32) int32 {
	process := ensurecurrentprocess()
	entry := getНээхФайлfor(process, oldfd)
	if entry == nil {
		return Ebadf
	}
	if шинэfd < 0 || шинэfd >= maxfd {
		return Ebadf
	}
	if oldfd == шинэfd {
		return шинэfd
	}
	if process.fds[шинэfd].хэрэглэгдсэн {
		хаахprocessfd(process, шинэfd)
	}
	process.fds[шинэfd] = fdentry{хэрэглэгдсэн: true, тодорхойлолт: process.fds[oldfd].тодорхойлолт}
	entry.refs++
	return шинэfd
}

func sysfcntl(fd int32, тушаал uint32, argument uint32) int32 {
	process := ensurecurrentprocess()
	entry := getНээхФайлfor(process, fd)
	if entry == nil {
		return Ebadf
	}
	switch тушаал {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(process.fds[fd].fdТөлвүүд)
	case fsetfd:
		process.fds[fd].fdТөлвүүд = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.төлвүүд)
	case fsetfl:
		entry.төлвүүд = (entry.төлвүүд & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getНээхФайл(fd)
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
		base = int64(entry.хэмжээ)
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

func уншихvfsФайл(entry *нээхФайлТодорхойлолт, destination_2 []byte, count uint32) int32 {
	санахойЗохицуулагч := &mem.TСанахойЗохицуулагч{}
	tmppointer := санахойЗохицуулагч.Malloc(entry.хэмжээ)
	if tmppointer == nil {
		return Einval
	}
	tmp := GetБайтfrompointer(uintptr(tmppointer), int(entry.хэмжээ), int(entry.хэмжээ))
	уншихФайл(entry.нэр[:entry.нэрlen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	санахойЗохицуулагч.Чөлөөт(tmppointer)
	return int32(count)
}

func isrootЗАМ(зАМaddress uint32) bool {
	if зАМaddress == 0 {
		return false
	}
	зАМ := GetБайтfrompointer(uintptr(зАМaddress), 4, 4)
	if зАМ[0] == '/' && зАМ[1] == 0 {
		return true
	}
	if зАМ[0] == '.' && зАМ[1] == 0 {
		return true
	}
	if зАМ[0] == '/' && зАМ[1] == '.' && зАМ[2] == 0 {
		return true
	}
	return false
}

func sysaccess(зАМaddress uint32, горим uint32) int32 {
	if зАМaddress == 0 {
		return Efault
	}
	if (горим & ^uint32(7)) != 0 {
		return Einval
	}
	isroot := isrootЗАМ(зАМaddress)
	exists := isroot
	if !exists {
		нэрlen, нэр := хуулахЗАМ(зАМaddress)
		exists = нэрlen != 0 && файлХэмжээ(нэр[:нэрlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (горим & 2) != 0 {
		return Eacces
	}

	if (горим&1) != 0 && !isroot {
		return Eacces
	}
	return 0
}

func syschdir(зАМaddress uint32) int32 {
	if зАМaddress == 0 {
		return Efault
	}
	if !isrootЗАМ(зАМaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, хэмжээ uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if хэмжээ < 2 {
		return Erange
	}
	buffer_2 := GetБайтfrompointer(uintptr(bufferaddress), int(хэмжээ), int(хэмжээ))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, горим uint32, хэмжээ uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Төхөөрөмж = 1
	stat.Ino = inode
	stat.Горим = горим
	stat.Nlink = 1
	stat.Хэмжээ_2 = int32(хэмжээ)
	stat.Blksize = 512
	stat.Block = int32((хэмжээ + 511) / 512)
	return 0
}

func sysstat(зАМaddress uint32, stataddress uint32) int32 {
	if зАМaddress == 0 {
		return Efault
	}
	if isrootЗАМ(зАМaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	нэрlen, нэр := хуулахЗАМ(зАМaddress)
	if нэрlen == 0 {
		return Enoent
	}
	хэмжээ := файлХэмжээ(нэр[:нэрlen])
	if хэмжээ == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < нэрlen; i++ {
		inode = inode*33 + uint32(нэр[i])
	}
	return fillposixstat(stataddress, sifreg|0444, хэмжээ, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getНээхФайл(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindКонсол:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindrootЛавлах:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.хэмжээ, uint32(fd+2))
	case fdkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getНээхФайл(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	process := ensurecurrentprocess()
	if process == nil {
		return 0
	}
	if process.програмbreak == 0 {
		process.програмbreak = хэрэглэгчheapbase
	}
	if address_2 == 0 {
		return process.програмbreak
	}
	if address_2 < хэрэглэгчheapbase || address_2 > хэрэглэгчheaplimit {
		return process.програмbreak
	}
	process.програмbreak = address_2
	return process.програмbreak
}

func хуулахutsfield(destination *[65]byte, утга string) {
	limit := len(утга)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = утга[i]
	}
	destination[limit] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	нэр := (*posixutsname)(Pointer(uintptr(address_2)))
	*нэр = posixutsname{}
	хуулахutsfield(&нэр.Sysname, "EngOS")
	хуулахutsfield(&нэр.Nodename, "engos")
	хуулахutsfield(&нэр.Release, "0.1-posix")
	хуулахutsfield(&нэр.Version, "POSIX.1-2017 phase 1")
	хуулахutsfield(&нэр.Machine, "i386")
	return 0
}

func swapunsignedinteger16(утга uint16) uint16 {
	return (утга << 8) | (утга >> 8)
}

func socketcallargument(arguments_2 uint32, үзүүлэлт uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + үзүүлэлт*4)))
}

func socketforfd(fd int32) (*localdatagramsocket, int32) {
	entry := getНээхФайл(fd)
	if entry == nil || entry.kind != fdkindsocket || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	socket := &localsockets[entry.aux]
	if !socket.хэрэглэгдсэн {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(domain uint32, socketТөрөл uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if socketТөрөл != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	process := ensurecurrentprocess()
	if process == nil {
		return Enfile
	}
	socketҮзүүлэлт := -1
	for i := 0; i < maxsockets; i++ {
		if !localsockets[i].хэрэглэгдсэн {
			socketҮзүүлэлт = i
			break
		}
	}
	if socketҮзүүлэлт < 0 {
		return Enfile
	}
	тодорхойлолт := allocateНээхФайл()
	if тодорхойлолт < 0 {
		return тодорхойлолт
	}
	localsockets[socketҮзүүлэлт] = localdatagramsocket{хэрэглэгдсэн: true}
	entry := &нээхФайлtable[тодорхойлолт]
	entry.kind = fdkindsocket
	entry.төлвүүд = oУншихБичих
	entry.aux = uint32(socketҮзүүлэлт)
	fd := allocatefd(process, тодорхойлолт, 3)
	if fd < 0 {
		localsockets[socketҮзүүлэлт] = localdatagramsocket{}
		*entry = нээхФайлТодорхойлолт{}
		return fd
	}
	return fd
}

func socketaddress(address_2 uint32, length uint32) (*socketaddressiОу4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if length < 16 {
		return nil, Einval
	}
	result := (*socketaddressiОу4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func портinuse(порт uint16, except *localdatagramsocket) bool {
	for i := 0; i < maxsockets; i++ {
		socket := &localsockets[i]
		if socket != except && socket.хэрэглэгдсэн && socket.bound && socket.local.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(socket *localdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := swapunsignedinteger16(дараахephemeralПорт)
		дараахephemeralПорт++
		if дараахephemeralПорт < 49152 {
			дараахephemeralПорт = 49152
		}
		if !портinuse(порт, socket) {
			socket.local = socketaddressiОу4{Family: afinet, Порт: порт, Address: 0x0100007F}
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
	if requested.Порт == 0 {
		return bindephemeral(socket)
	}
	if портinuse(requested.Порт, socket) {
		return Eaddrinuse
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketХолбох(fd int32, address_2 uint32, length uint32) int32 {
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
	if length > maxdatagramХэмжээ {
		return Emsgsize
	}
	if length != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination socketaddressiОу4
	if destinationaddress != 0 {
		address_2, addressАлдаа := socketaddress(destinationaddress, destinationlength)
		if addressАлдаа != 0 {
			return addressАлдаа
		}
		destination = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindАлдаа := bindephemeral(socket); bindАлдаа != 0 {
			return bindАлдаа
		}
	}
	var receiver *localdatagramsocket
	for i := 0; i < maxsockets; i++ {
		candidate := &localsockets[i]
		if candidate.хэрэглэгдсэн && candidate.bound && candidate.local.Порт == destination.Порт &&
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
	*packet = socketpacket{хэрэглэгдсэн: true, хэмжээ: length, эх: socket.local}
	if length != 0 {
		эх := GetБайтfrompointer(uintptr(bufferaddress_2), int(length), int(length))
		copy(packet.data[:length], эх)
	}
	receiver.tail = (receiver.tail + 1) % maxsocketpackets
	receiver.count++
	return int32(length)
}

func socketreceivefrom(fd int32, bufferaddress_2 uint32, length uint32, эхaddress uint32, эхlengthaddress uint32) int32 {
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
	хуулахlength := packet.хэмжээ
	if хуулахlength > length {
		хуулахlength = length
	}
	if хуулахlength != 0 {
		destination := GetБайтfrompointer(uintptr(bufferaddress_2), int(хуулахlength), int(хуулахlength))
		copy(destination, packet.data[:хуулахlength])
	}
	if эхaddress != 0 {
		if эхlengthaddress == 0 {
			return Efault
		}
		providedlength := (*uint32)(Pointer(uintptr(эхlengthaddress)))
		if *providedlength >= 16 {
			*(*socketaddressiОу4)(Pointer(uintptr(эхaddress))) = packet.эх
		}
		*providedlength = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % maxsocketpackets
	socket.count--
	return int32(хуулахlength)
}

func хуулахsocketНэр(fd int32, address_2 uint32, lengthaddress uint32, peer bool) int32 {
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
		*(*socketaddressiОу4)(Pointer(uintptr(address_2))) = socket.remote
	} else {
		if !socket.bound {
			if bindАлдаа := bindephemeral(socket); bindАлдаа != 0 {
				return bindАлдаа
			}
		}
		*(*socketaddressiОу4)(Pointer(uintptr(address_2))) = socket.local
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
		return socketХолбох(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return хуулахsocketНэр(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), false)
	case 7:
		return хуулахsocketНэр(int32(socketcallargument(arguments_2, 0)), socketcallargument(arguments_2, 1), socketcallargument(arguments_2, 2), true)
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

func уншихstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБайтfrompointer(uintptr(address), int(count), int(count))
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
	дараах := (stdinБичих + 1) % uint32(len(stdinbuffer))
	if дараах == stdinУнших {
		return
	}
	stdinbuffer[stdinБичих] = c
	stdinБичих = дараах
}

func stdingetblocking() byte {
	for stdinУнших == stdinБичих {
		sc := pollГарscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinУнших]
	stdinУнших = (stdinУнших + 1) % uint32(len(stdinbuffer))
	return c
}

func pollГарscancode() byte {
	for (ПортУншихbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортУншихbyte(0x60)
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

func хуулахexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for үзүүлэлт := uint32(0); үзүүлэлт < maxexecvectorentry; үзүүлэлт++ {
		бИЧВЭРaddress := *(*uint32)(Pointer(uintptr(address_2 + үзүүлэлт*4)))
		if бИЧВЭРaddress == 0 {
			result.count = үзүүлэлт
			return 0
		}
		terminated := false
		for length := uint32(0); length <= maxexecБИЧВЭРlength; length++ {
			утга := *(*byte)(Pointer(uintptr(бИЧВЭРaddress + length)))
			result.values[үзүүлэлт][length] = утга
			if утга == 0 {
				result.lengths[үзүүлэлт] = length
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

func pushexecunsignedinteger32(stack *uint32, утга uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = утга
}

func setupexecstack(cpu *Tcpustate, arguments_2 *execvector, environment *execvector) int32 {
	const stackБайт uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Хэрэглэгчstackдээр-stackБайт, stackБайт) {
		return Enomem
	}
	stack := Хэрэглэгчstackдээр
	var argumentpointers [maxexecvectorentry]uint32
	var environmentpointers [maxexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := GetБайтfrompointer(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		length := arguments_2.lengths[i] + 1
		stack -= length
		destination := GetБайтfrompointer(uintptr(stack), int(length), int(length))
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

func хаахonexec(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].хэрэглэгдсэн && (process.fds[fd].fdТөлвүүд&fdcloexec) != 0 {
			хаахprocessfd(process, fd)
		}
	}
}

func sysexecve(cpu *Tcpustate, зАМaddress uint32) int32 {
	if зАМaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := хуулахexecvector(cpu.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := хуулахexecvector(cpu.Edx, &environment); result < 0 {
		return result
	}
	нэрlen, нэр := хуулахЗАМ(зАМaddress)
	if нэрlen == 0 {
		return Enoent
	}
	хэмжээ := файлХэмжээ(нэр[:нэрlen])
	if хэмжээ == 0 {
		return Enoent
	}
	санахойЗохицуулагч := &mem.TСанахойЗохицуулагч{}
	файлpointer := санахойЗохицуулагч.Malloc(хэмжээ)
	if файлpointer == nil {
		return Einval
	}
	data := GetБайтfrompointer(uintptr(файлpointer), int(хэмжээ), int(хэмжээ))
	уншихФайл(нэр[:нэрlen], data)
	if хэмжээ < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		санахойЗохицуулагч.Чөлөөт(файлpointer)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	санахойЗохицуулагч.Чөлөөт(файлpointer)
	if result := setupexecstack(cpu, &arguments_2, &environment); result < 0 {
		return result
	}
	хаахonexec(ensurecurrentprocess())
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
	санахойЗохицуулагч := &mem.TСанахойЗохицуулагч{}
	threadpointer := санахойЗохицуулагч.Malloc(uint32(Sizeof(TThread{})))
	stackpointer := санахойЗохицуулагч.Malloc(ThreadstackХэмжээ)
	childХУУДАСЛавлах := Cloneaddressspacecow(getcr3())
	if threadpointer == nil || stackpointer == nil || childХУУДАСЛавлах == 0 {
		discardprocess(pid)
		return Einval
	}
	child := (*TThread)(threadpointer)
	child.Stack = uint32(uintptr(stackpointer))
	child.Cpustate = (*Tcpustate)(Pointer(uintptr(stackpointer) + ThreadstackХэмжээ - Sizeof(Tcpustate{})))
	*child.Cpustate = *cpu
	child.Cpustate.Eax = 0
	child.Хэрэглэгчstack_2 = cpu.Esp
	child.ХэрэглэгчstackХэмжээ_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.ХУУДАСЛавлахentry = childХУУДАСЛавлах
	child.Threadstate = Ready
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Нэмэхrunnablethread(child)
	return int32(pid)
}

func sysexit(төлөв uint32) {
	pid := Currentpid()
	for i := 0; i < len(processtable); i++ {
		if processtable[i].хэрэглэгдсэн && processtable[i].pid == pid {
			хаахБүхprocessfds(&processtable[i])
			processtable[i].exited = true
			processtable[i].төлөв = (төлөв & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, төлөвaddress uint32, параметрууд uint32) int32 {
	if (параметрууд & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Currentpid()
	foundchild := false
	for i := 0; i < len(processtable); i++ {
		p := &processtable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.хэрэглэгдсэн && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if төлөвaddress != 0 {
					*(*uint32)(Pointer(uintptr(төлөвaddress))) = p.төлөв
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

	if (параметрууд & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateprocess(parent uint32) uint32 {
	parentprocess := хайхprocess(parent)
	pid := Allocatepid()
	for i := 0; i < len(processtable); i++ {
		if !processtable[i].хэрэглэгдсэн {
			processtable[i] = processentry{
				хэрэглэгдсэн:	true,
				pid:		pid,
				parent:		parent,
				програмbreak:	хэрэглэгчheapbase,
			}
			if parentprocess != nil {
				processtable[i].програмbreak = parentprocess.програмbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentprocess.fds[fd].хэрэглэгдсэн {
						processtable[i].fds[fd] = parentprocess.fds[fd]
						тодорхойлолт := parentprocess.fds[fd].тодорхойлолт
						if тодорхойлолт >= 0 && тодорхойлолт < maxНээхФайлууд {
							нээхФайлtable[тодорхойлолт].refs++
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

func хаахБүхprocessfds(process *processentry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if process.fds[fd].хэрэглэгдсэн {
			хаахprocessfd(process, fd)
		}
	}
}

func discardprocess(pid uint32) {
	process := хайхprocess(pid)
	if process == nil {
		return
	}
	хаахБүхprocessfds(process)
	*process = processentry{}
}

func хуулахЗАМ(зАМaddress uint32) (uint32, [12]byte) {
	var нэр [12]byte
	if зАМaddress == 0 {
		return 0, нэр
	}
	raw := GetБайтfrompointer(uintptr(зАМaddress), 64, 64)
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
		нэр[n] = c
		n++
	}
	return n, нэр
}

func файлХэмжээ(файлыннэр []byte) uint32 {
	var ata0s = TӨргөтгөсөнtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Уншихpartition(&ata0s)

	bios := TBiosparameterblock32{}
	хэмжээ := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр)
	ata0s.Flush()
	return хэмжээ
}

func уншихФайл(файлыннэр []byte, data []byte) {
	var ata0s = TӨргөтгөсөнtechnologyattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitiontable{}
	partition.Уншихpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Унших(&ata0s, partition.Mbr.Primarypartition[0], файлыннэр, data)
	ata0s.Flush()
}

func getcr3() uint32
