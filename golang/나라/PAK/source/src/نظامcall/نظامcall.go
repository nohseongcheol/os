package نظامcall

import . "unsafe"

import . "مداخلت"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "فائلنظام/msdospartition"
import . "فائلنظام/fat"
import . "فائلنظام/elf"
import mem "یادداشتmanager"
import . "paging"
import . "پورٹ"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualیادداشت"

var console_2 = TConsole{}

type TSyscall struct {
	Tمداخلتhandler
}

const (
	Sysexit		uint32	= 1
	Sysfork		uint32	= 2
	Sysپڑھیں	uint32	= 3
	Sysلکھیں	uint32	= 4
	Sysکھولیں	uint32	= 5
	Sysبندکریں	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysرسائی	uint32	= 33
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
	stdinfd			int32	= 0
	stdoutfd		int32	= 1
	stderrfd		int32	= 2
	زیادہfd				= 32
	زیادہکھولیںفائلیں		= 128
)

type fdentry struct {
	استعمالشدہ	bool
	تفصیل		int32
	fdجھنڈیاں	uint32
}

type کھولیںفائلتفصیل struct {
	استعمالشدہ	bool
	refs		uint32
	kind		uint32
	جھنڈیاں		uint32
	position	uint32
	حجم		uint32
	نام		[12]byte
	نامlen		uint32
	aux		uint32
}

const (
	fdkindکچھنہیں		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindروٹڈائریکٹری	uint32	= 4
	fdkindساکٹ		uint32	= 5

	oپڑھیںonly	uint32	= 0
	oلکھیںonly	uint32	= 1
	oپڑھیںلکھیں	uint32	= 2
	ocreate		uint32	= 0x40
	otruncate	uint32	= 0x200
	oappend		uint32	= 0x400
	oڈائریکٹری	uint32	= 0x10000

	seekسیٹ		uint32	= 0
	seekحالیہ	uint32	= 1
	seekآخر		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fسیٹfd		uint32	= 2
	fgetfl		uint32	= 3
	fسیٹfl		uint32	= 4
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
	زیادہsockets		= 32
	زیادہساکٹپیکٹس		= 8
	زیادہdatagramحجم	= 512
)

type ساکٹaddressipv4 struct {
	Family	uint16
	Pپورٹ	uint16
	Address	uint32
	Zero	[8]byte
}

type ساکٹpacket struct {
	استعمالشدہ	bool
	حجم		uint32
	مصدر		ساکٹaddressipv4
	data		[زیادہdatagramحجم]byte
}

type مقامیdatagramساکٹ struct {
	استعمالشدہ	bool
	bound		bool
	connected	bool
	مقامی		ساکٹaddressipv4
	remote		ساکٹaddressipv4
	head		uint32
	tail		uint32
	count		uint32
	پیکٹس		[زیادہساکٹپیکٹس]ساکٹpacket
}

type posixstat struct {
	Dآلہ		uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sحجم_2		int32
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
	Vورژن		[65]byte
	Machine		[65]byte
}

const (
	زیادہexecvectorentry	= 16
	زیادہexecڈوراطول	= 63
)

type execvector struct {
	count	uint32
	lengths	[زیادہexecvectorentry]uint32
	values	[زیادہexecvectorentry][زیادہexecڈوراطول + 1]byte
}

type عملکاریentry struct {
	استعمالشدہ	bool
	pid		uint32
	آبائی		uint32
	exited		bool
	حالت		uint32
	پروگرامbreak	uint32
	fds		[زیادہfd]fdentry
}

type ڈوراheader struct {
	Data	uintptr
	Len	int
}

func syscallغلطی(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var کھولیںفائلجدول [زیادہکھولیںفائلیں]کھولیںفائلتفصیل
var عملکاریجدول [32]عملکاریentry
var مقامیsockets [زیادہsockets]مقامیdatagramساکٹ
var اگلاephemeralپورٹ uint16 = 49152

const (
	صارفheapbase	uint32	= 0x06000000
	صارفheapحد	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinپڑھیں uint32
var stdinلکھیں uint32

func Iمداخلت(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysexit_2(index uint32) {
	Syscall(Sysexit, index)
}

func Sysپڑھیں_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysپڑھیں, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysچھاپیںstr(buffer string) {
	h := (*ڈوراheader)(Pointer(&buffer))
	Syscall(Sysلکھیں, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysچھاپیںunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysلکھیں, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysکھولیں_2(پاتھ uintptr, جھنڈیاں uint32, mode uint32) int32 {
	return int32(Syscall(Sysکھولیں, uint32(پاتھ), جھنڈیاں, mode))
}

func Sysبندکریں_2(fd uint32) int32 {
	return int32(Syscall(Sysبندکریں, fd))
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
		return Iمداخلت(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Iمداخلت(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Iمداخلت(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Iمداخلت(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Iمداخلت(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Iمداخلت(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallغلطی(Enosys)
	}
}

func (self *TSyscall) Init(manager *Tمداخلتmanager) {
	initفائلdescriptor()

	مداخلتhandler = handleمداخلت

	var address uintptr
	address = uintptr(Pointer(&مداخلتhandler))

	self.Tمداخلتhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var مداخلتhandler func(uint32) uint32

func handleمداخلت(esp uint32) uint32 {
	var سیپییو = (*Tcpuحالت)(Pointer(uintptr(esp)))

	switch سیپییو.Eax {
	case Sysexit:
		sysexit(سیپییو.Ebx)
		return uint32(uintptr(Pointer(Sروکیںحالیہthread(سیپییو))))
	case Sysrtexit:
		sysexit(سیپییو.Ebx)
		return uint32(uintptr(Pointer(Sروکیںحالیہthread(سیپییو))))
	case Sysfork:
		سیپییو.Eax = uint32(sysfork(سیپییو))
		return esp
	case Sysپڑھیں:
		سیپییو.Eax = uint32(sysپڑھیں(int32(سیپییو.Ebx), سیپییو.Ecx, سیپییو.Edx))
		return esp
	case Sysلکھیں:
		سیپییو.Eax = uint32(sysلکھیں(int32(سیپییو.Ebx), سیپییو.Ecx, سیپییو.Edx))
		return esp
	case Sysکھولیں:
		سیپییو.Eax = uint32(sysکھولیں(سیپییو.Ebx, سیپییو.Ecx, سیپییو.Edx))
		return esp
	case Syscreat:
		سیپییو.Eax = uint32(sysکھولیں(سیپییو.Ebx, ocreate|oلکھیںonly|otruncate, سیپییو.Ecx))
		return esp
	case Sysبندکریں:
		سیپییو.Eax = uint32(sysبندکریں(int32(سیپییو.Ebx)))
		return esp
	case Syswaitpid:
		سیپییو.Eax = uint32(syswaitpid(int32(سیپییو.Ebx), سیپییو.Ecx, سیپییو.Edx))
		return esp
	case Syslseek:
		سیپییو.Eax = uint32(syslseek(int32(سیپییو.Ebx), int32(سیپییو.Ecx), سیپییو.Edx))
		return esp
	case Sysexecve:
		سیپییو.Eax = uint32(sysexecve(سیپییو, سیپییو.Ebx))
		return esp
	case Sysgetpid:
		سیپییو.Eax = Cحالیہpid()
		return esp
	case Sysgetppid:
		سیپییو.Eax = Cحالیہآبائیpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		سیپییو.Eax = 0
		return esp
	case Sysرسائی:
		سیپییو.Eax = uint32(sysرسائی(سیپییو.Ebx, سیپییو.Ecx))
		return esp
	case Syschdir:
		سیپییو.Eax = uint32(syschdir(سیپییو.Ebx))
		return esp
	case Sysgetcwd:
		سیپییو.Eax = uint32(sysgetcwd(سیپییو.Ebx, سیپییو.Ecx))
		return esp
	case Sysdup:
		سیپییو.Eax = uint32(sysdup(int32(سیپییو.Ebx), 0))
		return esp
	case Sysdup2:
		سیپییو.Eax = uint32(sysdup2(int32(سیپییو.Ebx), int32(سیپییو.Ecx)))
		return esp
	case Syssocketcall:
		سیپییو.Eax = uint32(sysساکٹcall(سیپییو.Ebx, سیپییو.Ecx))
		return esp
	case Sysfcntl:
		سیپییو.Eax = uint32(sysfcntl(int32(سیپییو.Ebx), سیپییو.Ecx, سیپییو.Edx))
		return esp
	case Sysstat, Syslstat:
		سیپییو.Eax = uint32(sysstat(سیپییو.Ebx, سیپییو.Ecx))
		return esp
	case Sysfstat:
		سیپییو.Eax = uint32(sysfstat(int32(سیپییو.Ebx), سیپییو.Ecx))
		return esp
	case Sysfsync:
		سیپییو.Eax = uint32(sysfsync(int32(سیپییو.Ebx)))
		return esp
	case Syssync:
		سیپییو.Eax = 0
		return esp
	case Sysuname:
		سیپییو.Eax = uint32(sysuname(سیپییو.Ebx))
		return esp
	case Sysbrk:
		سیپییو.Eax = sysbrk(سیپییو.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32چھاپیں(سیپییو.Ebx)
		return esp

	default:
		console_2.Mچھاپیںxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32چھاپیں(esp)
		console_2.Mچھاپیں(([]byte)(":"))
		console_2.MUnsignedinteger32چھاپیں(سیپییو.Eax)
		console_2.Mچھاپیں(([]byte)(":"))
		console_2.MUnsignedinteger32چھاپیں(سیپییو.Ebx)
		console_2.Mچھاپیں(([]byte)(":"))
		console_2.MUnsignedinteger32چھاپیں(سیپییو.Ecx)
		console_2.Mچھاپیں(([]byte)(":"))
		console_2.MUnsignedinteger32چھاپیں(سیپییو.Edx)
		console_2.Mچھاپیں(([]byte)("]"))
		سیپییو.Eax = syscallغلطی(Enosys)
		return esp
	}

	return esp
}

func initفائلdescriptor() {
	for i := 0; i < زیادہکھولیںفائلیں; i++ {
		کھولیںفائلجدول[i] = کھولیںفائلتفصیل{}
	}
	for i := 0; i < len(عملکاریجدول); i++ {
		عملکاریجدول[i] = عملکاریentry{}
	}
	for i := 0; i < len(مقامیsockets); i++ {
		مقامیsockets[i] = مقامیdatagramساکٹ{}
	}
	اگلاephemeralپورٹ = 49152
	کھولیںفائلجدول[0] = کھولیںفائلتفصیل{استعمالشدہ: true, kind: fdkindstdin, جھنڈیاں: oپڑھیںonly}
	کھولیںفائلجدول[1] = کھولیںفائلتفصیل{استعمالشدہ: true, kind: fdkindconsole, جھنڈیاں: oلکھیںonly}
	کھولیںفائلجدول[2] = کھولیںفائلتفصیل{استعمالشدہ: true, kind: fdkindconsole, جھنڈیاں: oلکھیںonly}
}

func تلاشعملکاری(pid uint32) *عملکاریentry {
	for i := 0; i < len(عملکاریجدول); i++ {
		if عملکاریجدول[i].استعمالشدہ && عملکاریجدول[i].pid == pid {
			return &عملکاریجدول[i]
		}
	}
	return nil
}

func initializeعملکاریfds(عملکاری *عملکاریentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		عملکاری.fds[fd] = fdentry{استعمالشدہ: true, تفصیل: fd}
		کھولیںفائلجدول[fd].refs++
	}
}

func ensureحالیہعملکاری() *عملکاریentry {
	pid := Cحالیہpid()
	if عملکاری := تلاشعملکاری(pid); عملکاری != nil {
		return عملکاری
	}
	for i := 0; i < len(عملکاریجدول); i++ {
		if !عملکاریجدول[i].استعمالشدہ {
			عملکاریجدول[i] = عملکاریentry{
				استعمالشدہ:	true,
				pid:		pid,
				آبائی:		Cحالیہآبائیpid(),
				پروگرامbreak:	صارفheapbase,
			}
			initializeعملکاریfds(&عملکاریجدول[i])
			return &عملکاریجدول[i]
		}
	}
	return nil
}

func getکھولیںفائلfor(عملکاری *عملکاریentry, fd int32) *کھولیںفائلتفصیل {
	if عملکاری == nil || fd < 0 || fd >= زیادہfd || !عملکاری.fds[fd].استعمالشدہ {
		return nil
	}
	تفصیل := عملکاری.fds[fd].تفصیل
	if تفصیل < 0 || تفصیل >= زیادہکھولیںفائلیں || !کھولیںفائلجدول[تفصیل].استعمالشدہ {
		return nil
	}
	return &کھولیںفائلجدول[تفصیل]
}

func getکھولیںفائل(fd int32) *کھولیںفائلتفصیل {
	return getکھولیںفائلfor(ensureحالیہعملکاری(), fd)
}

func allocateکھولیںفائل() int32 {
	for i := int32(3); i < زیادہکھولیںفائلیں; i++ {
		if !کھولیںفائلجدول[i].استعمالشدہ {
			کھولیںفائلجدول[i] = کھولیںفائلتفصیل{استعمالشدہ: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(عملکاری *عملکاریentry, تفصیل int32, کمسےکم int32) int32 {
	if عملکاری == nil {
		return Enfile
	}
	if کمسےکم < 0 || کمسےکم >= زیادہfd {
		return Einval
	}
	for fd := کمسےکم; fd < زیادہfd; fd++ {
		if !عملکاری.fds[fd].استعمالشدہ {
			عملکاری.fds[fd] = fdentry{استعمالشدہ: true, تفصیل: تفصیل}
			return fd
		}
	}
	return Emfile
}

func releaseکھولیںفائل(تفصیل int32) {
	if تفصیل < 0 || تفصیل >= زیادہکھولیںفائلیں {
		return
	}
	entry := &کھولیںفائلجدول[تفصیل]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && تفصیل > stderrfd {
		if entry.kind == fdkindساکٹ && entry.aux < زیادہsockets {
			مقامیsockets[entry.aux] = مقامیdatagramساکٹ{}
		}
		*entry = کھولیںفائلتفصیل{}
	}
}

func بندکریںعملکاریfd(عملکاری *عملکاریentry, fd int32) int32 {
	if عملکاری == nil || getکھولیںفائلfor(عملکاری, fd) == nil {
		return Ebadf
	}
	تفصیل := عملکاری.fds[fd].تفصیل
	عملکاری.fds[fd] = fdentry{}
	releaseکھولیںفائل(تفصیل)
	return 0
}

func sysلکھیں(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getکھولیںفائل(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindساکٹ {
			return ساکٹsendto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindروٹڈائریکٹری {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getبائٹسfromپؤائنٹر(uintptr(address), int(count), int(count))
	console_2.Mچھاپیں(buffer)
	return int32(count)
}

func sysپڑھیں(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getکھولیںفائل(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return پڑھیںstdin(address, count)
	}
	if entry.kind == fdkindروٹڈائریکٹری {
		return Eisdir
	}
	if entry.kind == fdkindساکٹ {
		return ساکٹreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.position >= entry.حجم {
		return 0
	}
	remaining := entry.حجم - entry.position
	if count > remaining {
		count = remaining
	}
	buffer := Getبائٹسfromپؤائنٹر(uintptr(address), int(count), int(count))
	return پڑھیںvfsفائل(entry, buffer, count)
}

func sysکھولیں(پاتھaddress uint32, جھنڈیاں uint32, mode uint32) int32 {
	_ = mode
	if پاتھaddress == 0 {
		return Efault
	}
	رسائیmode := جھنڈیاں & 3
	if رسائیmode == oلکھیںonly || رسائیmode == oپڑھیںلکھیں || (جھنڈیاں&(ocreate|otruncate|oappend)) != 0 {
		return Erofs
	}

	عملکاری := ensureحالیہعملکاری()
	if عملکاری == nil {
		return Enfile
	}
	تفصیل := allocateکھولیںفائل()
	if تفصیل < 0 {
		return تفصیل
	}
	entry := &کھولیںفائلجدول[تفصیل]
	entry.جھنڈیاں = جھنڈیاں
	if isروٹپاتھ(پاتھaddress) {
		entry.kind = fdkindروٹڈائریکٹری
		entry.حجم = 0
	} else {
		نامlen, نام := کاپیپاتھ(پاتھaddress)
		if نامlen == 0 {
			*entry = کھولیںفائلتفصیل{}
			return Enoent
		}
		حجم := فائلحجم(نام[:نامlen])
		if حجم == 0 {
			*entry = کھولیںفائلتفصیل{}
			return Enoent
		}
		if (جھنڈیاں & oڈائریکٹری) != 0 {
			*entry = کھولیںفائلتفصیل{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.حجم = حجم
		entry.نامlen = نامlen
		entry.نام = نام
	}

	fd := allocatefd(عملکاری, تفصیل, 3)
	if fd < 0 {
		*entry = کھولیںفائلتفصیل{}
		return fd
	}
	return fd
}

func sysبندکریں(fd int32) int32 {
	return بندکریںعملکاریfd(ensureحالیہعملکاری(), fd)
}

func sysdup(fd int32, کمسےکم int32) int32 {
	عملکاری := ensureحالیہعملکاری()
	entry := getکھولیںفائلfor(عملکاری, fd)
	if entry == nil {
		return Ebadf
	}
	نیاfd := allocatefd(عملکاری, عملکاری.fds[fd].تفصیل, کمسےکم)
	if نیاfd >= 0 {
		entry.refs++
	}
	return نیاfd
}

func sysdup2(oldfd int32, نیاfd int32) int32 {
	عملکاری := ensureحالیہعملکاری()
	entry := getکھولیںفائلfor(عملکاری, oldfd)
	if entry == nil {
		return Ebadf
	}
	if نیاfd < 0 || نیاfd >= زیادہfd {
		return Ebadf
	}
	if oldfd == نیاfd {
		return نیاfd
	}
	if عملکاری.fds[نیاfd].استعمالشدہ {
		بندکریںعملکاریfd(عملکاری, نیاfd)
	}
	عملکاری.fds[نیاfd] = fdentry{استعمالشدہ: true, تفصیل: عملکاری.fds[oldfd].تفصیل}
	entry.refs++
	return نیاfd
}

func sysfcntl(fd int32, کمانڈ uint32, argument uint32) int32 {
	عملکاری := ensureحالیہعملکاری()
	entry := getکھولیںفائلfor(عملکاری, fd)
	if entry == nil {
		return Ebadf
	}
	switch کمانڈ {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(عملکاری.fds[fd].fdجھنڈیاں)
	case fسیٹfd:
		عملکاری.fds[fd].fdجھنڈیاں = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.جھنڈیاں)
	case fسیٹfl:
		entry.جھنڈیاں = (entry.جھنڈیاں & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getکھولیںفائل(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekسیٹ:
		base = 0
	case seekحالیہ:
		base = int64(entry.position)
	case seekآخر:
		base = int64(entry.حجم)
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

func پڑھیںvfsفائل(entry *کھولیںفائلتفصیل, destination_2 []byte, count uint32) int32 {
	یادداشتmanager := &mem.Tیادداشتmanager{}
	tmpپؤائنٹر := یادداشتmanager.Malloc(entry.حجم)
	if tmpپؤائنٹر == nil {
		return Einval
	}
	tmp := Getبائٹسfromپؤائنٹر(uintptr(tmpپؤائنٹر), int(entry.حجم), int(entry.حجم))
	پڑھیںفائل(entry.نام[:entry.نامlen], tmp)
	copy(destination_2[:count], tmp[entry.position:entry.position+count])
	entry.position += count
	یادداشتmanager.Fخالی(tmpپؤائنٹر)
	return int32(count)
}

func isروٹپاتھ(پاتھaddress uint32) bool {
	if پاتھaddress == 0 {
		return false
	}
	پاتھ := Getبائٹسfromپؤائنٹر(uintptr(پاتھaddress), 4, 4)
	if پاتھ[0] == '/' && پاتھ[1] == 0 {
		return true
	}
	if پاتھ[0] == '.' && پاتھ[1] == 0 {
		return true
	}
	if پاتھ[0] == '/' && پاتھ[1] == '.' && پاتھ[2] == 0 {
		return true
	}
	return false
}

func sysرسائی(پاتھaddress uint32, mode uint32) int32 {
	if پاتھaddress == 0 {
		return Efault
	}
	if (mode & ^uint32(7)) != 0 {
		return Einval
	}
	isروٹ := isروٹپاتھ(پاتھaddress)
	exists := isروٹ
	if !exists {
		نامlen, نام := کاپیپاتھ(پاتھaddress)
		exists = نامlen != 0 && فائلحجم(نام[:نامlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (mode & 2) != 0 {
		return Eacces
	}

	if (mode&1) != 0 && !isروٹ {
		return Eacces
	}
	return 0
}

func syschdir(پاتھaddress uint32) int32 {
	if پاتھaddress == 0 {
		return Efault
	}
	if !isروٹپاتھ(پاتھaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, حجم uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if حجم < 2 {
		return Erange
	}
	buffer_2 := Getبائٹسfromپؤائنٹر(uintptr(bufferaddress), int(حجم), int(حجم))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, mode uint32, حجم uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dآلہ = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Sحجم_2 = int32(حجم)
	stat.Blksize = 512
	stat.Block = int32((حجم + 511) / 512)
	return 0
}

func sysstat(پاتھaddress uint32, stataddress uint32) int32 {
	if پاتھaddress == 0 {
		return Efault
	}
	if isروٹپاتھ(پاتھaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	نامlen, نام := کاپیپاتھ(پاتھaddress)
	if نامlen == 0 {
		return Enoent
	}
	حجم := فائلحجم(نام[:نامlen])
	if حجم == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < نامlen; i++ {
		inode = inode*33 + uint32(نام[i])
	}
	return fillposixstat(stataddress, sifreg|0444, حجم, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getکھولیںفائل(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindروٹڈائریکٹری:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.حجم, uint32(fd+2))
	case fdkindساکٹ:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getکھولیںفائل(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	عملکاری := ensureحالیہعملکاری()
	if عملکاری == nil {
		return 0
	}
	if عملکاری.پروگرامbreak == 0 {
		عملکاری.پروگرامbreak = صارفheapbase
	}
	if address_2 == 0 {
		return عملکاری.پروگرامbreak
	}
	if address_2 < صارفheapbase || address_2 > صارفheapحد {
		return عملکاری.پروگرامbreak
	}
	عملکاری.پروگرامbreak = address_2
	return عملکاری.پروگرامbreak
}

func کاپیutsfield(destination *[65]byte, قدر string) {
	حد := len(قدر)
	if حد > 64 {
		حد = 64
	}
	for i := 0; i < حد; i++ {
		destination[i] = قدر[i]
	}
	destination[حد] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	نام := (*posixutsname)(Pointer(uintptr(address_2)))
	*نام = posixutsname{}
	کاپیutsfield(&نام.Sysname, "EngOS")
	کاپیutsfield(&نام.Nodename, "engos")
	کاپیutsfield(&نام.Release, "0.1-posix")
	کاپیutsfield(&نام.Vورژن, "POSIX.1-2017 phase 1")
	کاپیutsfield(&نام.Machine, "i386")
	return 0
}

func سویپunsignedinteger16(قدر uint16) uint16 {
	return (قدر << 8) | (قدر >> 8)
}

func ساکٹcallargument(arguments_2 uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + index*4)))
}

func ساکٹforfd(fd int32) (*مقامیdatagramساکٹ, int32) {
	entry := getکھولیںفائل(fd)
	if entry == nil || entry.kind != fdkindساکٹ || entry.aux >= زیادہsockets {
		return nil, Ebadf
	}
	ساکٹ := &مقامیsockets[entry.aux]
	if !ساکٹ.استعمالشدہ {
		return nil, Ebadf
	}
	return ساکٹ, 0
}

func allocateساکٹ(domain uint32, ساکٹنوعیت uint32, protocol uint32) int32 {
	if domain != afinet {
		return Eafnosupport
	}
	if ساکٹنوعیت != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	عملکاری := ensureحالیہعملکاری()
	if عملکاری == nil {
		return Enfile
	}
	ساکٹindex := -1
	for i := 0; i < زیادہsockets; i++ {
		if !مقامیsockets[i].استعمالشدہ {
			ساکٹindex = i
			break
		}
	}
	if ساکٹindex < 0 {
		return Enfile
	}
	تفصیل := allocateکھولیںفائل()
	if تفصیل < 0 {
		return تفصیل
	}
	مقامیsockets[ساکٹindex] = مقامیdatagramساکٹ{استعمالشدہ: true}
	entry := &کھولیںفائلجدول[تفصیل]
	entry.kind = fdkindساکٹ
	entry.جھنڈیاں = oپڑھیںلکھیں
	entry.aux = uint32(ساکٹindex)
	fd := allocatefd(عملکاری, تفصیل, 3)
	if fd < 0 {
		مقامیsockets[ساکٹindex] = مقامیdatagramساکٹ{}
		*entry = کھولیںفائلتفصیل{}
		return fd
	}
	return fd
}

func ساکٹaddress(address_2 uint32, طول uint32) (*ساکٹaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if طول < 16 {
		return nil, Einval
	}
	result := (*ساکٹaddressipv4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func پورٹاندراستعمال(پورٹ uint16, except *مقامیdatagramساکٹ) bool {
	for i := 0; i < زیادہsockets; i++ {
		ساکٹ := &مقامیsockets[i]
		if ساکٹ != except && ساکٹ.استعمالشدہ && ساکٹ.bound && ساکٹ.مقامی.Pپورٹ == پورٹ {
			return true
		}
	}
	return false
}

func bindephemeral(ساکٹ *مقامیdatagramساکٹ) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		پورٹ := سویپunsignedinteger16(اگلاephemeralپورٹ)
		اگلاephemeralپورٹ++
		if اگلاephemeralپورٹ < 49152 {
			اگلاephemeralپورٹ = 49152
		}
		if !پورٹاندراستعمال(پورٹ, ساکٹ) {
			ساکٹ.مقامی = ساکٹaddressipv4{Family: afinet, Pپورٹ: پورٹ, Address: 0x0100007F}
			ساکٹ.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func ساکٹbind(fd int32, address_2 uint32, طول uint32) int32 {
	ساکٹ, err := ساکٹforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := ساکٹaddress(address_2, طول)
	if err != 0 {
		return err
	}
	if ساکٹ.bound {
		return Einval
	}
	if requested.Pپورٹ == 0 {
		return bindephemeral(ساکٹ)
	}
	if پورٹاندراستعمال(requested.Pپورٹ, ساکٹ) {
		return Eaddrinuse
	}
	ساکٹ.مقامی = *requested
	ساکٹ.bound = true
	return 0
}

func ساکٹمتصلہوں(fd int32, address_2 uint32, طول uint32) int32 {
	ساکٹ, err := ساکٹforfd(fd)
	if err != 0 {
		return err
	}
	remote, err := ساکٹaddress(address_2, طول)
	if err != 0 {
		return err
	}
	if !ساکٹ.bound {
		if err := bindephemeral(ساکٹ); err != 0 {
			return err
		}
	}
	ساکٹ.remote = *remote
	ساکٹ.connected = true
	return 0
}

func ساکٹsendto(fd int32, bufferaddress_2 uint32, طول uint32, destinationaddress uint32, destinationطول uint32) int32 {
	ساکٹ, err := ساکٹforfd(fd)
	if err != 0 {
		return err
	}
	if طول > زیادہdatagramحجم {
		return Emsgsize
	}
	if طول != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination ساکٹaddressipv4
	if destinationaddress != 0 {
		address_2, addressغلطی := ساکٹaddress(destinationaddress, destinationطول)
		if addressغلطی != 0 {
			return addressغلطی
		}
		destination = *address_2
	} else {
		if !ساکٹ.connected {
			return Enotconn
		}
		destination = ساکٹ.remote
	}
	if !ساکٹ.bound {
		if bindغلطی := bindephemeral(ساکٹ); bindغلطی != 0 {
			return bindغلطی
		}
	}
	var receiver *مقامیdatagramساکٹ
	for i := 0; i < زیادہsockets; i++ {
		candidate := &مقامیsockets[i]
		if candidate.استعمالشدہ && candidate.bound && candidate.مقامی.Pپورٹ == destination.Pپورٹ &&
			(candidate.مقامی.Address == 0 || candidate.مقامی.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= زیادہساکٹپیکٹس {
		return Eagain
	}
	packet := &receiver.پیکٹس[receiver.tail]
	*packet = ساکٹpacket{استعمالشدہ: true, حجم: طول, مصدر: ساکٹ.مقامی}
	if طول != 0 {
		مصدر := Getبائٹسfromپؤائنٹر(uintptr(bufferaddress_2), int(طول), int(طول))
		copy(packet.data[:طول], مصدر)
	}
	receiver.tail = (receiver.tail + 1) % زیادہساکٹپیکٹس
	receiver.count++
	return int32(طول)
}

func ساکٹreceivefrom(fd int32, bufferaddress_2 uint32, طول uint32, مصدرaddress uint32, مصدرطولaddress uint32) int32 {
	ساکٹ, err := ساکٹforfd(fd)
	if err != 0 {
		return err
	}
	if طول != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if ساکٹ.count == 0 {
		return Eagain
	}
	packet := &ساکٹ.پیکٹس[ساکٹ.head]
	کاپیطول := packet.حجم
	if کاپیطول > طول {
		کاپیطول = طول
	}
	if کاپیطول != 0 {
		destination := Getبائٹسfromپؤائنٹر(uintptr(bufferaddress_2), int(کاپیطول), int(کاپیطول))
		copy(destination, packet.data[:کاپیطول])
	}
	if مصدرaddress != 0 {
		if مصدرطولaddress == 0 {
			return Efault
		}
		providedطول := (*uint32)(Pointer(uintptr(مصدرطولaddress)))
		if *providedطول >= 16 {
			*(*ساکٹaddressipv4)(Pointer(uintptr(مصدرaddress))) = packet.مصدر
		}
		*providedطول = 16
	}
	*packet = ساکٹpacket{}
	ساکٹ.head = (ساکٹ.head + 1) % زیادہساکٹپیکٹس
	ساکٹ.count--
	return int32(کاپیطول)
}

func کاپیساکٹنام(fd int32, address_2 uint32, طولaddress uint32, peer bool) int32 {
	ساکٹ, err := ساکٹforfd(fd)
	if err != 0 {
		return err
	}
	if address_2 == 0 || طولaddress == 0 {
		return Efault
	}
	طول := (*uint32)(Pointer(uintptr(طولaddress)))
	if *طول < 16 {
		*طول = 16
		return Einval
	}
	if peer {
		if !ساکٹ.connected {
			return Enotconn
		}
		*(*ساکٹaddressipv4)(Pointer(uintptr(address_2))) = ساکٹ.remote
	} else {
		if !ساکٹ.bound {
			if bindغلطی := bindephemeral(ساکٹ); bindغلطی != 0 {
				return bindغلطی
			}
		}
		*(*ساکٹaddressipv4)(Pointer(uintptr(address_2))) = ساکٹ.مقامی
	}
	*طول = 16
	return 0
}

func sysساکٹcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateساکٹ(ساکٹcallargument(arguments_2, 0), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2))
	case 2:
		return ساکٹbind(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2))
	case 3:
		return ساکٹمتصلہوں(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return کاپیساکٹنام(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), false)
	case 7:
		return کاپیساکٹنام(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), true)
	case 9:
		return ساکٹsendto(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), 0, 0)
	case 10:
		return ساکٹreceivefrom(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), 0, 0)
	case 11:
		return ساکٹsendto(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), ساکٹcallargument(arguments_2, 4), ساکٹcallargument(arguments_2, 5))
	case 12:
		return ساکٹreceivefrom(int32(ساکٹcallargument(arguments_2, 0)), ساکٹcallargument(arguments_2, 1), ساکٹcallargument(arguments_2, 2), ساکٹcallargument(arguments_2, 4), ساکٹcallargument(arguments_2, 5))
	case 13:
		if _, err := ساکٹforfd(int32(ساکٹcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := ساکٹforfd(int32(ساکٹcallargument(arguments_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func پڑھیںstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getبائٹسfromپؤائنٹر(uintptr(address), int(count), int(count))
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
	اگلا := (stdinلکھیں + 1) % uint32(len(stdinbuffer))
	if اگلا == stdinپڑھیں {
		return
	}
	stdinbuffer[stdinلکھیں] = c
	stdinلکھیں = اگلا
}

func stdingetblocking() byte {
	for stdinپڑھیں == stdinلکھیں {
		sc := pollکیبورڈscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinپڑھیں]
	stdinپڑھیں = (stdinپڑھیں + 1) % uint32(len(stdinbuffer))
	return c
}

func pollکیبورڈscancode() byte {
	for (Pپورٹپڑھیںbyte(0x64) & 0x01) == 0 {
	}
	sc := Pپورٹپڑھیںbyte(0x60)
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

func کاپیexecvector(address_2 uint32, result *execvector) int32 {
	*result = execvector{}
	if address_2 == 0 {
		return 0
	}
	for index := uint32(0); index < زیادہexecvectorentry; index++ {
		ڈوراaddress := *(*uint32)(Pointer(uintptr(address_2 + index*4)))
		if ڈوراaddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for طول := uint32(0); طول <= زیادہexecڈوراطول; طول++ {
			قدر := *(*byte)(Pointer(uintptr(ڈوراaddress + طول)))
			result.values[index][طول] = قدر
			if قدر == 0 {
				result.lengths[index] = طول
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

func pushexecunsignedinteger32(stack *uint32, قدر uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = قدر
}

func setupexecstack(سیپییو *Tcpuحالت, arguments_2 *execvector, environment *execvector) int32 {
	const stackبائٹس uint32 = 4096
	if !Makerangeprivatewritable(getcr3(), Uصارفstackاوپر-stackبائٹس, stackبائٹس) {
		return Enomem
	}
	stack := Uصارفstackاوپر
	var argumentpointers [زیادہexecvectorentry]uint32
	var environmentpointers [زیادہexecvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		طول := environment.lengths[i] + 1
		stack -= طول
		destination := Getبائٹسfromپؤائنٹر(uintptr(stack), int(طول), int(طول))
		copy(destination, environment.values[i][:طول])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		طول := arguments_2.lengths[i] + 1
		stack -= طول
		destination := Getبائٹسfromپؤائنٹر(uintptr(stack), int(طول), int(طول))
		copy(destination, arguments_2.values[i][:طول])
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
	سیپییو.Esp = stack
	سیپییو.Ebp = 0
	return 0
}

func بندکریںچالوexec(عملکاری *عملکاریentry) {
	if عملکاری == nil {
		return
	}
	for fd := int32(0); fd < زیادہfd; fd++ {
		if عملکاری.fds[fd].استعمالشدہ && (عملکاری.fds[fd].fdجھنڈیاں&fdcloexec) != 0 {
			بندکریںعملکاریfd(عملکاری, fd)
		}
	}
}

func sysexecve(سیپییو *Tcpuحالت, پاتھaddress uint32) int32 {
	if پاتھaddress == 0 {
		return Efault
	}
	var arguments_2 execvector
	var environment execvector
	if result := کاپیexecvector(سیپییو.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := کاپیexecvector(سیپییو.Edx, &environment); result < 0 {
		return result
	}
	نامlen, نام := کاپیپاتھ(پاتھaddress)
	if نامlen == 0 {
		return Enoent
	}
	حجم := فائلحجم(نام[:نامlen])
	if حجم == 0 {
		return Enoent
	}
	یادداشتmanager := &mem.Tیادداشتmanager{}
	فائلپؤائنٹر := یادداشتmanager.Malloc(حجم)
	if فائلپؤائنٹر == nil {
		return Einval
	}
	data := Getبائٹسfromپؤائنٹر(uintptr(فائلپؤائنٹر), int(حجم), int(حجم))
	پڑھیںفائل(نام[:نامlen], data)
	if حجم < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		یادداشتmanager.Fخالی(فائلپؤائنٹر)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	یادداشتmanager.Fخالی(فائلپؤائنٹر)
	if result := setupexecstack(سیپییو, &arguments_2, &environment); result < 0 {
		return result
	}
	بندکریںچالوexec(ensureحالیہعملکاری())
	سیپییو.Eip = entry
	سیپییو.Eax = 0
	return 0
}

func sysfork(سیپییو *Tcpuحالت) int32 {
	آبائیpid := Cحالیہpid()
	if ensureحالیہعملکاری() == nil {
		return Enfile
	}
	pid := allocateعملکاری(آبائیpid)
	if pid == 0 {
		return Einval
	}
	یادداشتmanager := &mem.Tیادداشتmanager{}
	threadپؤائنٹر := یادداشتmanager.Malloc(uint32(Sizeof(TThread{})))
	stackپؤائنٹر := یادداشتmanager.Malloc(Threadstackحجم)
	بچہصفحہڈائریکٹری := Cloneaddressspacecow(getcr3())
	if threadپؤائنٹر == nil || stackپؤائنٹر == nil || بچہصفحہڈائریکٹری == 0 {
		discardعملکاری(pid)
		return Einval
	}
	بچہ := (*TThread)(threadپؤائنٹر)
	بچہ.Stack = uint32(uintptr(stackپؤائنٹر))
	بچہ.Cسیپییوحالت = (*Tcpuحالت)(Pointer(uintptr(stackپؤائنٹر) + Threadstackحجم - Sizeof(Tcpuحالت{})))
	*بچہ.Cسیپییوحالت = *سیپییو
	بچہ.Cسیپییوحالت.Eax = 0
	بچہ.Uصارفstack_2 = سیپییو.Esp
	بچہ.Uصارفstackحجم_2 = 0
	بچہ.Pid = pid
	بچہ.Pآبائیpid = آبائیpid
	بچہ.Pصفحہڈائریکٹریentry = بچہصفحہڈائریکٹری
	بچہ.Threadحالت = Rتیار
	بچہ.Fpuoffset = 0xffffffff
	بچہ.Iskernel = false
	Aشاملکریںrunnablethread(بچہ)
	return int32(pid)
}

func sysexit(حالت uint32) {
	pid := Cحالیہpid()
	for i := 0; i < len(عملکاریجدول); i++ {
		if عملکاریجدول[i].استعمالشدہ && عملکاریجدول[i].pid == pid {
			بندکریںتمامعملکاریfds(&عملکاریجدول[i])
			عملکاریجدول[i].exited = true
			عملکاریجدول[i].حالت = (حالت & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, حالتaddress uint32, اختیارات uint32) int32 {
	if (اختیارات & ^uint32(1)) != 0 {
		return Einval
	}
	آبائیpid := Cحالیہpid()
	foundبچہ := false
	for i := 0; i < len(عملکاریجدول); i++ {
		p := &عملکاریجدول[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.استعمالشدہ && matches && p.آبائی == آبائیpid {
			foundبچہ = true
			if p.exited {
				if حالتaddress != 0 {
					*(*uint32)(Pointer(uintptr(حالتaddress))) = p.حالت
				}
				بچہpid := p.pid
				*p = عملکاریentry{}
				return int32(بچہpid)
			}
		}
	}
	if !foundبچہ {
		return Echild
	}

	if (اختیارات & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateعملکاری(آبائی uint32) uint32 {
	آبائیعملکاری := تلاشعملکاری(آبائی)
	pid := Allocatepid()
	for i := 0; i < len(عملکاریجدول); i++ {
		if !عملکاریجدول[i].استعمالشدہ {
			عملکاریجدول[i] = عملکاریentry{
				استعمالشدہ:	true,
				pid:		pid,
				آبائی:		آبائی,
				پروگرامbreak:	صارفheapbase,
			}
			if آبائیعملکاری != nil {
				عملکاریجدول[i].پروگرامbreak = آبائیعملکاری.پروگرامbreak
				for fd := 0; fd < زیادہfd; fd++ {
					if آبائیعملکاری.fds[fd].استعمالشدہ {
						عملکاریجدول[i].fds[fd] = آبائیعملکاری.fds[fd]
						تفصیل := آبائیعملکاری.fds[fd].تفصیل
						if تفصیل >= 0 && تفصیل < زیادہکھولیںفائلیں {
							کھولیںفائلجدول[تفصیل].refs++
						}
					}
				}
			} else {
				initializeعملکاریfds(&عملکاریجدول[i])
			}
			return pid
		}
	}
	return 0
}

func بندکریںتمامعملکاریfds(عملکاری *عملکاریentry) {
	if عملکاری == nil {
		return
	}
	for fd := int32(0); fd < زیادہfd; fd++ {
		if عملکاری.fds[fd].استعمالشدہ {
			بندکریںعملکاریfd(عملکاری, fd)
		}
	}
}

func discardعملکاری(pid uint32) {
	عملکاری := تلاشعملکاری(pid)
	if عملکاری == nil {
		return
	}
	بندکریںتمامعملکاریfds(عملکاری)
	*عملکاری = عملکاریentry{}
}

func کاپیپاتھ(پاتھaddress uint32) (uint32, [12]byte) {
	var نام [12]byte
	if پاتھaddress == 0 {
		return 0, نام
	}
	raw := Getبائٹسfromپؤائنٹر(uintptr(پاتھaddress), 64, 64)
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
		نام[n] = c
		n++
	}
	return n, نام
}

func فائلحجم(فائلکانام []byte) uint32 {
	var ata0s = Tاعلیٹیکنالوجیattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rپڑھیںpartition(&ata0s)

	bios := TBiosparameterblock32{}
	حجم := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام)
	ata0s.Flush()
	return حجم
}

func پڑھیںفائل(فائلکانام []byte, data []byte) {
	var ata0s = Tاعلیٹیکنالوجیattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := Tmsdospartitionجدول{}
	partition.Rپڑھیںpartition(&ata0s)

	bios := TBiosparameterblock32{}
	bios.Rپڑھیں(&ata0s, partition.Mbr.Primarypartition[0], فائلکانام, data)
	ata0s.Flush()
}

func getcr3() uint32
