package сістэмаcall

import . "unsafe"

import . "перарыванне"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "файлСістэма/msdospartition"
import . "файлСістэма/fat"
import . "файлСістэма/elf"
import mem "памяцьmanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualПамяць"

var console_2 = TConsole{}

type TSyscall struct {
	TПерарываннеhandler
}

const (
	SysВыхад	uint32	= 1
	Sysfork		uint32	= 2
	SysЧытанне	uint32	= 3
	SysЗапіс	uint32	= 4
	SysАдкрыць	uint32	= 5
	SysЗакрыць	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysдоступ	uint32	= 33
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
	SysrtВыхад	uint32	= 252

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
	maxАдкрыцьФАЙЛЫ		= 128
)

type fdentry struct {
	выкарыстана	bool
	апісанне	int32
	fdСцяжкі	uint32
}

type адкрыцьФайлАпісанне struct {
	выкарыстана	bool
	refs		uint32
	kind		uint32
	сцяжкі		uint32
	пазіцыя		uint32
	памер		uint32
	назва		[12]byte
	назваlen	uint32
	aux		uint32
}

const (
	fdkindНяма		uint32	= 0
	fdkindfat		uint32	= 1
	fdkindstdin		uint32	= 2
	fdkindconsole		uint32	= 3
	fdkindКораньКаталог	uint32	= 4
	fdkindСокет		uint32	= 5

	oЧытаннеonly	uint32	= 0
	oЗапісonly	uint32	= 1
	oЧытаннеЗапіс	uint32	= 2
	ocreate		uint32	= 0x40
	oУсячэнне	uint32	= 0x200
	oappend		uint32	= 0x400
	oКаталог	uint32	= 0x10000

	seekвызначана	uint32	= 0
	seekДзейны	uint32	= 1
	seekКанец	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fвызначанаfd	uint32	= 2
	fgetfl		uint32	= 3
	fвызначанаfl	uint32	= 4
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
	maxСокетпакетаў		= 8
	maxdatagramПамер	= 512
)

type сокетaddressiБгЗн4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type сокетpacket struct {
	выкарыстана	bool
	памер		uint32
	крыніца		сокетaddressiБгЗн4
	data		[maxdatagramПамер]byte
}

type лакальныяdatagramСокет struct {
	выкарыстана	bool
	bound		bool
	connected	bool
	лакальныя	сокетaddressiБгЗн4
	аддалены	сокетaddressiБгЗн4
	head		uint32
	tail		uint32
	count		uint32
	пакетаў		[maxСокетпакетаў]сокетpacket
}

type posixstat struct {
	Прылада		uint32
	Ino		uint32
	РЭЖЫМ		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Памер_2		int32
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
	maxВыкананнеvectorentry		= 16
	maxВыкананнеРадокДаўжыня	= 63
)

type выкананнеvector struct {
	count	uint32
	lengths	[maxВыкананнеvectorentry]uint32
	values	[maxВыкананнеvectorentry][maxВыкананнеРадокДаўжыня + 1]byte
}

type працэсentry struct {
	выкарыстана	bool
	pid		uint32
	parent		uint32
	exited		bool
	стан		uint32
	праграмаbreak	uint32
	fds		[maxfd]fdentry
}

type радокheader struct {
	Data	uintptr
	Len	int
}

func syscallПамылка(пам int32) uint32 {
	return *(*uint32)(Pointer(&пам))
}

var адкрыцьФайлТабліца [maxАдкрыцьФАЙЛЫ]адкрыцьФайлАпісанне
var працэсТабліца [32]працэсentry
var лакальныяsockets [maxsockets]лакальныяdatagramСокет
var наступныephemeralПорт uint16 = 49152

const (
	карыстальнікheapbase		uint32	= 0x06000000
	карыстальнікheapАбмежаваць	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinЧытанне uint32
var stdinЗапіс uint32

func Перарыванне(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysВыхад_2(змест uint32) {
	Syscall(SysВыхад, змест)
}

func SysЧытанне_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysЧытанне, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysДрукавацьstr(buffer string) {
	h := (*радокheader)(Pointer(&buffer))
	Syscall(SysЗапіс, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysДрукавацьunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysЗапіс, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysАдкрыць_2(шЛЯХ uintptr, сцяжкі uint32, рЭЖЫМ uint32) int32 {
	return int32(Syscall(SysАдкрыць, uint32(шЛЯХ), сцяжкі, рЭЖЫМ))
}

func SysЗакрыць_2(fd uint32) int32 {
	return int32(Syscall(SysЗакрыць, fd))
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
		return Перарыванне(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Перарыванне(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Перарыванне(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Перарыванне(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Перарыванне(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Перарыванне(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallПамылка(Enosys)
	}
}

func (self *TSyscall) Init(manager *TПерарываннеmanager) {
	initФайлdescriptor()

	перарываннеhandler = handleПерарыванне

	var address uintptr
	address = uintptr(Pointer(&перарываннеhandler))

	self.TПерарываннеhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var перарываннеhandler func(uint32) uint32

func handleПерарыванне(esp uint32) uint32 {
	var цП = (*TcpuСтан)(Pointer(uintptr(esp)))

	switch цП.Eax {
	case SysВыхад:
		sysВыхад(цП.Ebx)
		return uint32(uintptr(Pointer(СпыніцьДзейныthread(цП))))
	case SysrtВыхад:
		sysВыхад(цП.Ebx)
		return uint32(uintptr(Pointer(СпыніцьДзейныthread(цП))))
	case Sysfork:
		цП.Eax = uint32(sysfork(цП))
		return esp
	case SysЧытанне:
		цП.Eax = uint32(sysЧытанне(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case SysЗапіс:
		цП.Eax = uint32(sysЗапіс(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case SysАдкрыць:
		цП.Eax = uint32(sysАдкрыць(цП.Ebx, цП.Ecx, цП.Edx))
		return esp
	case Syscreat:
		цП.Eax = uint32(sysАдкрыць(цП.Ebx, ocreate|oЗапісonly|oУсячэнне, цП.Ecx))
		return esp
	case SysЗакрыць:
		цП.Eax = uint32(sysЗакрыць(int32(цП.Ebx)))
		return esp
	case Syswaitpid:
		цП.Eax = uint32(syswaitpid(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case Syslseek:
		цП.Eax = uint32(syslseek(int32(цП.Ebx), int32(цП.Ecx), цП.Edx))
		return esp
	case Sysexecve:
		цП.Eax = uint32(sysexecve(цП, цП.Ebx))
		return esp
	case Sysgetpid:
		цП.Eax = Дзейныpid()
		return esp
	case Sysgetppid:
		цП.Eax = Дзейныparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		цП.Eax = 0
		return esp
	case Sysдоступ:
		цП.Eax = uint32(sysдоступ(цП.Ebx, цП.Ecx))
		return esp
	case Syschdir:
		цП.Eax = uint32(syschdir(цП.Ebx))
		return esp
	case Sysgetcwd:
		цП.Eax = uint32(sysgetcwd(цП.Ebx, цП.Ecx))
		return esp
	case Sysdup:
		цП.Eax = uint32(sysdup(int32(цП.Ebx), 0))
		return esp
	case Sysdup2:
		цП.Eax = uint32(sysdup2(int32(цП.Ebx), int32(цП.Ecx)))
		return esp
	case Syssocketcall:
		цП.Eax = uint32(sysСокетcall(цП.Ebx, цП.Ecx))
		return esp
	case Sysfcntl:
		цП.Eax = uint32(sysfcntl(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case Sysstat, Syslstat:
		цП.Eax = uint32(sysstat(цП.Ebx, цП.Ecx))
		return esp
	case Sysfstat:
		цП.Eax = uint32(sysfstat(int32(цП.Ebx), цП.Ecx))
		return esp
	case Sysfsync:
		цП.Eax = uint32(sysfsync(int32(цП.Ebx)))
		return esp
	case Syssync:
		цП.Eax = 0
		return esp
	case Sysuname:
		цП.Eax = uint32(sysuname(цП.Ebx))
		return esp
	case Sysbrk:
		цП.Eax = sysbrk(цП.Ebx)
		return esp
	case 9:
		console_2.MUnsignedinteger32Друкаваць(цП.Ebx)
		return esp

	default:
		console_2.MДрукавацьxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Друкаваць(esp)
		console_2.MДрукаваць(([]byte)(":"))
		console_2.MUnsignedinteger32Друкаваць(цП.Eax)
		console_2.MДрукаваць(([]byte)(":"))
		console_2.MUnsignedinteger32Друкаваць(цП.Ebx)
		console_2.MДрукаваць(([]byte)(":"))
		console_2.MUnsignedinteger32Друкаваць(цП.Ecx)
		console_2.MДрукаваць(([]byte)(":"))
		console_2.MUnsignedinteger32Друкаваць(цП.Edx)
		console_2.MДрукаваць(([]byte)("]"))
		цП.Eax = syscallПамылка(Enosys)
		return esp
	}

	return esp
}

func initФайлdescriptor() {
	for i := 0; i < maxАдкрыцьФАЙЛЫ; i++ {
		адкрыцьФайлТабліца[i] = адкрыцьФайлАпісанне{}
	}
	for i := 0; i < len(працэсТабліца); i++ {
		працэсТабліца[i] = працэсentry{}
	}
	for i := 0; i < len(лакальныяsockets); i++ {
		лакальныяsockets[i] = лакальныяdatagramСокет{}
	}
	наступныephemeralПорт = 49152
	адкрыцьФайлТабліца[0] = адкрыцьФайлАпісанне{выкарыстана: true, kind: fdkindstdin, сцяжкі: oЧытаннеonly}
	адкрыцьФайлТабліца[1] = адкрыцьФайлАпісанне{выкарыстана: true, kind: fdkindconsole, сцяжкі: oЗапісonly}
	адкрыцьФайлТабліца[2] = адкрыцьФайлАпісанне{выкарыстана: true, kind: fdkindconsole, сцяжкі: oЗапісonly}
}

func пошукПрацэс(pid uint32) *працэсentry {
	for i := 0; i < len(працэсТабліца); i++ {
		if працэсТабліца[i].выкарыстана && працэсТабліца[i].pid == pid {
			return &працэсТабліца[i]
		}
	}
	return nil
}

func initializeПрацэсfds(працэс *працэсentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		працэс.fds[fd] = fdentry{выкарыстана: true, апісанне: fd}
		адкрыцьФайлТабліца[fd].refs++
	}
}

func ensureДзейныПрацэс() *працэсentry {
	pid := Дзейныpid()
	if працэс := пошукПрацэс(pid); працэс != nil {
		return працэс
	}
	for i := 0; i < len(працэсТабліца); i++ {
		if !працэсТабліца[i].выкарыстана {
			працэсТабліца[i] = працэсentry{
				выкарыстана:	true,
				pid:		pid,
				parent:		Дзейныparentpid(),
				праграмаbreak:	карыстальнікheapbase,
			}
			initializeПрацэсfds(&працэсТабліца[i])
			return &працэсТабліца[i]
		}
	}
	return nil
}

func getАдкрыцьФайлfor(працэс *працэсentry, fd int32) *адкрыцьФайлАпісанне {
	if працэс == nil || fd < 0 || fd >= maxfd || !працэс.fds[fd].выкарыстана {
		return nil
	}
	апісанне := працэс.fds[fd].апісанне
	if апісанне < 0 || апісанне >= maxАдкрыцьФАЙЛЫ || !адкрыцьФайлТабліца[апісанне].выкарыстана {
		return nil
	}
	return &адкрыцьФайлТабліца[апісанне]
}

func getАдкрыцьФайл(fd int32) *адкрыцьФайлАпісанне {
	return getАдкрыцьФайлfor(ensureДзейныПрацэс(), fd)
}

func allocateАдкрыцьФайл() int32 {
	for i := int32(3); i < maxАдкрыцьФАЙЛЫ; i++ {
		if !адкрыцьФайлТабліца[i].выкарыстана {
			адкрыцьФайлТабліца[i] = адкрыцьФайлАпісанне{выкарыстана: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(працэс *працэсentry, апісанне int32, мінімум int32) int32 {
	if працэс == nil {
		return Enfile
	}
	if мінімум < 0 || мінімум >= maxfd {
		return Einval
	}
	for fd := мінімум; fd < maxfd; fd++ {
		if !працэс.fds[fd].выкарыстана {
			працэс.fds[fd] = fdentry{выкарыстана: true, апісанне: апісанне}
			return fd
		}
	}
	return Emfile
}

func releaseАдкрыцьФайл(апісанне int32) {
	if апісанне < 0 || апісанне >= maxАдкрыцьФАЙЛЫ {
		return
	}
	entry := &адкрыцьФайлТабліца[апісанне]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && апісанне > stderrfd {
		if entry.kind == fdkindСокет && entry.aux < maxsockets {
			лакальныяsockets[entry.aux] = лакальныяdatagramСокет{}
		}
		*entry = адкрыцьФайлАпісанне{}
	}
}

func закрыцьПрацэсfd(працэс *працэсentry, fd int32) int32 {
	if працэс == nil || getАдкрыцьФайлfor(працэс, fd) == nil {
		return Ebadf
	}
	апісанне := працэс.fds[fd].апісанне
	працэс.fds[fd] = fdentry{}
	releaseАдкрыцьФайл(апісанне)
	return 0
}

func sysЗапіс(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	entry := getАдкрыцьФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindconsole {
		if entry.kind == fdkindСокет {
			return сокетДаслацьto(fd, address, count, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindКораньКаталог {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтаўfromПаказальнік(uintptr(address), int(count), int(count))
	console_2.MДрукаваць(buffer)
	return int32(count)
}

func sysЧытанне(fd int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	entry := getАдкрыцьФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return чытаннеstdin(address, count)
	}
	if entry.kind == fdkindКораньКаталог {
		return Eisdir
	}
	if entry.kind == fdkindСокет {
		return сокетreceivefrom(fd, address, count, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.пазіцыя >= entry.памер {
		return 0
	}
	remaining := entry.памер - entry.пазіцыя
	if count > remaining {
		count = remaining
	}
	buffer := GetБайтаўfromПаказальнік(uintptr(address), int(count), int(count))
	return чытаннеvfsФайл(entry, buffer, count)
}

func sysАдкрыць(шЛЯХaddress uint32, сцяжкі uint32, рЭЖЫМ uint32) int32 {
	_ = рЭЖЫМ
	if шЛЯХaddress == 0 {
		return Efault
	}
	доступРЭЖЫМ := сцяжкі & 3
	if доступРЭЖЫМ == oЗапісonly || доступРЭЖЫМ == oЧытаннеЗапіс || (сцяжкі&(ocreate|oУсячэнне|oappend)) != 0 {
		return Erofs
	}

	працэс := ensureДзейныПрацэс()
	if працэс == nil {
		return Enfile
	}
	апісанне := allocateАдкрыцьФайл()
	if апісанне < 0 {
		return апісанне
	}
	entry := &адкрыцьФайлТабліца[апісанне]
	entry.сцяжкі = сцяжкі
	if isКораньШЛЯХ(шЛЯХaddress) {
		entry.kind = fdkindКораньКаталог
		entry.памер = 0
	} else {
		назваlen, назва := скапіявацьШЛЯХ(шЛЯХaddress)
		if назваlen == 0 {
			*entry = адкрыцьФайлАпісанне{}
			return Enoent
		}
		памер := файлПамер(назва[:назваlen])
		if памер == 0 {
			*entry = адкрыцьФайлАпісанне{}
			return Enoent
		}
		if (сцяжкі & oКаталог) != 0 {
			*entry = адкрыцьФайлАпісанне{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.памер = памер
		entry.назваlen = назваlen
		entry.назва = назва
	}

	fd := allocatefd(працэс, апісанне, 3)
	if fd < 0 {
		*entry = адкрыцьФайлАпісанне{}
		return fd
	}
	return fd
}

func sysЗакрыць(fd int32) int32 {
	return закрыцьПрацэсfd(ensureДзейныПрацэс(), fd)
}

func sysdup(fd int32, мінімум int32) int32 {
	працэс := ensureДзейныПрацэс()
	entry := getАдкрыцьФайлfor(працэс, fd)
	if entry == nil {
		return Ebadf
	}
	новыfd := allocatefd(працэс, працэс.fds[fd].апісанне, мінімум)
	if новыfd >= 0 {
		entry.refs++
	}
	return новыfd
}

func sysdup2(oldfd int32, новыfd int32) int32 {
	працэс := ensureДзейныПрацэс()
	entry := getАдкрыцьФайлfor(працэс, oldfd)
	if entry == nil {
		return Ebadf
	}
	if новыfd < 0 || новыfd >= maxfd {
		return Ebadf
	}
	if oldfd == новыfd {
		return новыfd
	}
	if працэс.fds[новыfd].выкарыстана {
		закрыцьПрацэсfd(працэс, новыfd)
	}
	працэс.fds[новыfd] = fdentry{выкарыстана: true, апісанне: працэс.fds[oldfd].апісанне}
	entry.refs++
	return новыfd
}

func sysfcntl(fd int32, загад uint32, argument uint32) int32 {
	працэс := ensureДзейныПрацэс()
	entry := getАдкрыцьФайлfor(працэс, fd)
	if entry == nil {
		return Ebadf
	}
	switch загад {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(працэс.fds[fd].fdСцяжкі)
	case fвызначанаfd:
		працэс.fds[fd].fdСцяжкі = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.сцяжкі)
	case fвызначанаfl:
		entry.сцяжкі = (entry.сцяжкі & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getАдкрыцьФайл(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekвызначана:
		base = 0
	case seekДзейны:
		base = int64(entry.пазіцыя)
	case seekКанец:
		base = int64(entry.памер)
	default:
		return Einval
	}
	пазіцыя_2 := base + int64(offset)
	if пазіцыя_2 < 0 || пазіцыя_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.пазіцыя = uint32(пазіцыя_2)
	return int32(entry.пазіцыя)
}

func чытаннеvfsФайл(entry *адкрыцьФайлАпісанне, destination_2 []byte, count uint32) int32 {
	памяцьmanager := &mem.TПамяцьmanager{}
	tmpПаказальнік := памяцьmanager.Malloc(entry.памер)
	if tmpПаказальнік == nil {
		return Einval
	}
	tmp := GetБайтаўfromПаказальнік(uintptr(tmpПаказальнік), int(entry.памер), int(entry.памер))
	чытаннеФайл(entry.назва[:entry.назваlen], tmp)
	copy(destination_2[:count], tmp[entry.пазіцыя:entry.пазіцыя+count])
	entry.пазіцыя += count
	памяцьmanager.Вольна(tmpПаказальнік)
	return int32(count)
}

func isКораньШЛЯХ(шЛЯХaddress uint32) bool {
	if шЛЯХaddress == 0 {
		return false
	}
	шЛЯХ := GetБайтаўfromПаказальнік(uintptr(шЛЯХaddress), 4, 4)
	if шЛЯХ[0] == '/' && шЛЯХ[1] == 0 {
		return true
	}
	if шЛЯХ[0] == '.' && шЛЯХ[1] == 0 {
		return true
	}
	if шЛЯХ[0] == '/' && шЛЯХ[1] == '.' && шЛЯХ[2] == 0 {
		return true
	}
	return false
}

func sysдоступ(шЛЯХaddress uint32, рЭЖЫМ uint32) int32 {
	if шЛЯХaddress == 0 {
		return Efault
	}
	if (рЭЖЫМ & ^uint32(7)) != 0 {
		return Einval
	}
	isКорань := isКораньШЛЯХ(шЛЯХaddress)
	exists := isКорань
	if !exists {
		назваlen, назва := скапіявацьШЛЯХ(шЛЯХaddress)
		exists = назваlen != 0 && файлПамер(назва[:назваlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (рЭЖЫМ & 2) != 0 {
		return Eacces
	}

	if (рЭЖЫМ&1) != 0 && !isКорань {
		return Eacces
	}
	return 0
}

func syschdir(шЛЯХaddress uint32) int32 {
	if шЛЯХaddress == 0 {
		return Efault
	}
	if !isКораньШЛЯХ(шЛЯХaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, памер uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if памер < 2 {
		return Erange
	}
	buffer_2 := GetБайтаўfromПаказальнік(uintptr(bufferaddress), int(памер), int(памер))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, рЭЖЫМ uint32, памер uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Прылада = 1
	stat.Ino = inode
	stat.РЭЖЫМ = рЭЖЫМ
	stat.Nlink = 1
	stat.Памер_2 = int32(памер)
	stat.Blksize = 512
	stat.Блок = int32((памер + 511) / 512)
	return 0
}

func sysstat(шЛЯХaddress uint32, stataddress uint32) int32 {
	if шЛЯХaddress == 0 {
		return Efault
	}
	if isКораньШЛЯХ(шЛЯХaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	назваlen, назва := скапіявацьШЛЯХ(шЛЯХaddress)
	if назваlen == 0 {
		return Enoent
	}
	памер := файлПамер(назва[:назваlen])
	if памер == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < назваlen; i++ {
		inode = inode*33 + uint32(назва[i])
	}
	return fillposixstat(stataddress, sifreg|0444, памер, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getАдкрыцьФайл(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindКораньКаталог:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.памер, uint32(fd+2))
	case fdkindСокет:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getАдкрыцьФайл(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	працэс := ensureДзейныПрацэс()
	if працэс == nil {
		return 0
	}
	if працэс.праграмаbreak == 0 {
		працэс.праграмаbreak = карыстальнікheapbase
	}
	if address_2 == 0 {
		return працэс.праграмаbreak
	}
	if address_2 < карыстальнікheapbase || address_2 > карыстальнікheapАбмежаваць {
		return працэс.праграмаbreak
	}
	працэс.праграмаbreak = address_2
	return працэс.праграмаbreak
}

func скапіявацьutsfield(destination *[65]byte, значэнне string) {
	абмежаваць := len(значэнне)
	if абмежаваць > 64 {
		абмежаваць = 64
	}
	for i := 0; i < абмежаваць; i++ {
		destination[i] = значэнне[i]
	}
	destination[абмежаваць] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	назва := (*posixutsname)(Pointer(uintptr(address_2)))
	*назва = posixutsname{}
	скапіявацьutsfield(&назва.Sysname, "EngOS")
	скапіявацьutsfield(&назва.Nodename, "engos")
	скапіявацьutsfield(&назва.Release, "0.1-posix")
	скапіявацьutsfield(&назва.Version, "POSIX.1-2017 phase 1")
	скапіявацьutsfield(&назва.Machine, "i386")
	return 0
}

func swapunsignedinteger16(значэнне uint16) uint16 {
	return (значэнне << 8) | (значэнне >> 8)
}

func сокетcallargument(arguments_2 uint32, змест uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments_2 + змест*4)))
}

func сокетforfd(fd int32) (*лакальныяdatagramСокет, int32) {
	entry := getАдкрыцьФайл(fd)
	if entry == nil || entry.kind != fdkindСокет || entry.aux >= maxsockets {
		return nil, Ebadf
	}
	сокет := &лакальныяsockets[entry.aux]
	if !сокет.выкарыстана {
		return nil, Ebadf
	}
	return сокет, 0
}

func allocateСокет(дамен uint32, сокетТып uint32, protocol uint32) int32 {
	if дамен != afinet {
		return Eafnosupport
	}
	if сокетТып != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	працэс := ensureДзейныПрацэс()
	if працэс == nil {
		return Enfile
	}
	сокетЗмест := -1
	for i := 0; i < maxsockets; i++ {
		if !лакальныяsockets[i].выкарыстана {
			сокетЗмест = i
			break
		}
	}
	if сокетЗмест < 0 {
		return Enfile
	}
	апісанне := allocateАдкрыцьФайл()
	if апісанне < 0 {
		return апісанне
	}
	лакальныяsockets[сокетЗмест] = лакальныяdatagramСокет{выкарыстана: true}
	entry := &адкрыцьФайлТабліца[апісанне]
	entry.kind = fdkindСокет
	entry.сцяжкі = oЧытаннеЗапіс
	entry.aux = uint32(сокетЗмест)
	fd := allocatefd(працэс, апісанне, 3)
	if fd < 0 {
		лакальныяsockets[сокетЗмест] = лакальныяdatagramСокет{}
		*entry = адкрыцьФайлАпісанне{}
		return fd
	}
	return fd
}

func сокетaddress(address_2 uint32, даўжыня uint32) (*сокетaddressiБгЗн4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if даўжыня < 16 {
		return nil, Einval
	}
	result := (*сокетaddressiБгЗн4)(Pointer(uintptr(address_2)))
	if result.Family != afinet {
		return nil, Eafnosupport
	}
	return result, 0
}

func портуУжыць(порт uint16, except *лакальныяdatagramСокет) bool {
	for i := 0; i < maxsockets; i++ {
		сокет := &лакальныяsockets[i]
		if сокет != except && сокет.выкарыстана && сокет.bound && сокет.лакальныя.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(сокет *лакальныяdatagramСокет) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := swapunsignedinteger16(наступныephemeralПорт)
		наступныephemeralПорт++
		if наступныephemeralПорт < 49152 {
			наступныephemeralПорт = 49152
		}
		if !портуУжыць(порт, сокет) {
			сокет.лакальныя = сокетaddressiБгЗн4{Family: afinet, Порт: порт, Address: 0x0100007F}
			сокет.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func сокетbind(fd int32, address_2 uint32, даўжыня uint32) int32 {
	сокет, пам := сокетforfd(fd)
	if пам != 0 {
		return пам
	}
	requested, пам := сокетaddress(address_2, даўжыня)
	if пам != 0 {
		return пам
	}
	if сокет.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return bindephemeral(сокет)
	}
	if портуУжыць(requested.Порт, сокет) {
		return Eaddrinuse
	}
	сокет.лакальныя = *requested
	сокет.bound = true
	return 0
}

func сокетЗлучыцца(fd int32, address_2 uint32, даўжыня uint32) int32 {
	сокет, пам := сокетforfd(fd)
	if пам != 0 {
		return пам
	}
	аддалены, пам := сокетaddress(address_2, даўжыня)
	if пам != 0 {
		return пам
	}
	if !сокет.bound {
		if пам := bindephemeral(сокет); пам != 0 {
			return пам
		}
	}
	сокет.аддалены = *аддалены
	сокет.connected = true
	return 0
}

func сокетДаслацьto(fd int32, bufferaddress_2 uint32, даўжыня uint32, destinationaddress uint32, destinationДаўжыня uint32) int32 {
	сокет, пам := сокетforfd(fd)
	if пам != 0 {
		return пам
	}
	if даўжыня > maxdatagramПамер {
		return Emsgsize
	}
	if даўжыня != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var destination сокетaddressiБгЗн4
	if destinationaddress != 0 {
		address_2, addressПамылка := сокетaddress(destinationaddress, destinationДаўжыня)
		if addressПамылка != 0 {
			return addressПамылка
		}
		destination = *address_2
	} else {
		if !сокет.connected {
			return Enotconn
		}
		destination = сокет.аддалены
	}
	if !сокет.bound {
		if bindПамылка := bindephemeral(сокет); bindПамылка != 0 {
			return bindПамылка
		}
	}
	var receiver *лакальныяdatagramСокет
	for i := 0; i < maxsockets; i++ {
		candidate := &лакальныяsockets[i]
		if candidate.выкарыстана && candidate.bound && candidate.лакальныя.Порт == destination.Порт &&
			(candidate.лакальныя.Address == 0 || candidate.лакальныя.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maxСокетпакетаў {
		return Eagain
	}
	packet := &receiver.пакетаў[receiver.tail]
	*packet = сокетpacket{выкарыстана: true, памер: даўжыня, крыніца: сокет.лакальныя}
	if даўжыня != 0 {
		крыніца := GetБайтаўfromПаказальнік(uintptr(bufferaddress_2), int(даўжыня), int(даўжыня))
		copy(packet.data[:даўжыня], крыніца)
	}
	receiver.tail = (receiver.tail + 1) % maxСокетпакетаў
	receiver.count++
	return int32(даўжыня)
}

func сокетreceivefrom(fd int32, bufferaddress_2 uint32, даўжыня uint32, крыніцаaddress uint32, крыніцаДаўжыняaddress uint32) int32 {
	сокет, пам := сокетforfd(fd)
	if пам != 0 {
		return пам
	}
	if даўжыня != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if сокет.count == 0 {
		return Eagain
	}
	packet := &сокет.пакетаў[сокет.head]
	скапіявацьДаўжыня := packet.памер
	if скапіявацьДаўжыня > даўжыня {
		скапіявацьДаўжыня = даўжыня
	}
	if скапіявацьДаўжыня != 0 {
		destination := GetБайтаўfromПаказальнік(uintptr(bufferaddress_2), int(скапіявацьДаўжыня), int(скапіявацьДаўжыня))
		copy(destination, packet.data[:скапіявацьДаўжыня])
	}
	if крыніцаaddress != 0 {
		if крыніцаДаўжыняaddress == 0 {
			return Efault
		}
		providedДаўжыня := (*uint32)(Pointer(uintptr(крыніцаДаўжыняaddress)))
		if *providedДаўжыня >= 16 {
			*(*сокетaddressiБгЗн4)(Pointer(uintptr(крыніцаaddress))) = packet.крыніца
		}
		*providedДаўжыня = 16
	}
	*packet = сокетpacket{}
	сокет.head = (сокет.head + 1) % maxСокетпакетаў
	сокет.count--
	return int32(скапіявацьДаўжыня)
}

func скапіявацьСокетНазва(fd int32, address_2 uint32, даўжыняaddress uint32, peer bool) int32 {
	сокет, пам := сокетforfd(fd)
	if пам != 0 {
		return пам
	}
	if address_2 == 0 || даўжыняaddress == 0 {
		return Efault
	}
	даўжыня := (*uint32)(Pointer(uintptr(даўжыняaddress)))
	if *даўжыня < 16 {
		*даўжыня = 16
		return Einval
	}
	if peer {
		if !сокет.connected {
			return Enotconn
		}
		*(*сокетaddressiБгЗн4)(Pointer(uintptr(address_2))) = сокет.аддалены
	} else {
		if !сокет.bound {
			if bindПамылка := bindephemeral(сокет); bindПамылка != 0 {
				return bindПамылка
			}
		}
		*(*сокетaddressiБгЗн4)(Pointer(uintptr(address_2))) = сокет.лакальныя
	}
	*даўжыня = 16
	return 0
}

func sysСокетcall(call uint32, arguments_2 uint32) int32 {
	if arguments_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateСокет(сокетcallargument(arguments_2, 0), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2))
	case 2:
		return сокетbind(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2))
	case 3:
		return сокетЗлучыцца(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return скапіявацьСокетНазва(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), false)
	case 7:
		return скапіявацьСокетНазва(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), true)
	case 9:
		return сокетДаслацьto(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), 0, 0)
	case 10:
		return сокетreceivefrom(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), 0, 0)
	case 11:
		return сокетДаслацьto(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), сокетcallargument(arguments_2, 4), сокетcallargument(arguments_2, 5))
	case 12:
		return сокетreceivefrom(int32(сокетcallargument(arguments_2, 0)), сокетcallargument(arguments_2, 1), сокетcallargument(arguments_2, 2), сокетcallargument(arguments_2, 4), сокетcallargument(arguments_2, 5))
	case 13:
		if _, пам := сокетforfd(int32(сокетcallargument(arguments_2, 0))); пам != 0 {
			return пам
		}
		return 0
	case 14:
		if _, пам := сокетforfd(int32(сокетcallargument(arguments_2, 0))); пам != 0 {
			return пам
		}
		return 0
	}
	return Eopnotsupp
}

func чытаннеstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБайтаўfromПаказальнік(uintptr(address), int(count), int(count))
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
	наступны := (stdinЗапіс + 1) % uint32(len(stdinbuffer))
	if наступны == stdinЧытанне {
		return
	}
	stdinbuffer[stdinЗапіс] = c
	stdinЗапіс = наступны
}

func stdingetblocking() byte {
	for stdinЧытанне == stdinЗапіс {
		sc := pollКлавіятураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinЧытанне]
	stdinЧытанне = (stdinЧытанне + 1) % uint32(len(stdinbuffer))
	return c
}

func pollКлавіятураscancode() byte {
	for (ПортЧытаннеbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортЧытаннеbyte(0x60)
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

func скапіявацьВыкананнеvector(address_2 uint32, result *выкананнеvector) int32 {
	*result = выкананнеvector{}
	if address_2 == 0 {
		return 0
	}
	for змест := uint32(0); змест < maxВыкананнеvectorentry; змест++ {
		радокaddress := *(*uint32)(Pointer(uintptr(address_2 + змест*4)))
		if радокaddress == 0 {
			result.count = змест
			return 0
		}
		terminated := false
		for даўжыня := uint32(0); даўжыня <= maxВыкананнеРадокДаўжыня; даўжыня++ {
			значэнне := *(*byte)(Pointer(uintptr(радокaddress + даўжыня)))
			result.values[змест][даўжыня] = значэнне
			if значэнне == 0 {
				result.lengths[змест] = даўжыня
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

func pushВыкананнеunsignedinteger32(stack *uint32, значэнне uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = значэнне
}

func setupВыкананнеstack(цП *TcpuСтан, arguments_2 *выкананнеvector, environment *выкананнеvector) int32 {
	const stackБайтаў uint32 = 4096
	if !MakeДыяпазонПрыватныwritable(getcr3(), КарыстальнікstackЗверху-stackБайтаў, stackБайтаў) {
		return Enomem
	}
	stack := КарыстальнікstackЗверху
	var argumentpointers [maxВыкананнеvectorentry]uint32
	var environmentpointers [maxВыкананнеvectorentry]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		даўжыня := environment.lengths[i] + 1
		stack -= даўжыня
		destination := GetБайтаўfromПаказальнік(uintptr(stack), int(даўжыня), int(даўжыня))
		copy(destination, environment.values[i][:даўжыня])
		environmentpointers[i] = stack
	}
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		даўжыня := arguments_2.lengths[i] + 1
		stack -= даўжыня
		destination := GetБайтаўfromПаказальнік(uintptr(stack), int(даўжыня), int(даўжыня))
		copy(destination, arguments_2.values[i][:даўжыня])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushВыкананнеunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushВыкананнеunsignedinteger32(&stack, environmentpointers[i])
	}
	pushВыкананнеunsignedinteger32(&stack, 0)
	for i := int(arguments_2.count) - 1; i >= 0; i-- {
		pushВыкананнеunsignedinteger32(&stack, argumentpointers[i])
	}
	pushВыкананнеunsignedinteger32(&stack, arguments_2.count)
	цП.Esp = stack
	цП.Ebp = 0
	return 0
}

func закрыцьonВыкананне(працэс *працэсentry) {
	if працэс == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if працэс.fds[fd].выкарыстана && (працэс.fds[fd].fdСцяжкі&fdcloexec) != 0 {
			закрыцьПрацэсfd(працэс, fd)
		}
	}
}

func sysexecve(цП *TcpuСтан, шЛЯХaddress uint32) int32 {
	if шЛЯХaddress == 0 {
		return Efault
	}
	var arguments_2 выкананнеvector
	var environment выкананнеvector
	if result := скапіявацьВыкананнеvector(цП.Ecx, &arguments_2); result < 0 {
		return result
	}
	if result := скапіявацьВыкананнеvector(цП.Edx, &environment); result < 0 {
		return result
	}
	назваlen, назва := скапіявацьШЛЯХ(шЛЯХaddress)
	if назваlen == 0 {
		return Enoent
	}
	памер := файлПамер(назва[:назваlen])
	if памер == 0 {
		return Enoent
	}
	памяцьmanager := &mem.TПамяцьmanager{}
	файлПаказальнік := памяцьmanager.Malloc(памер)
	if файлПаказальнік == nil {
		return Einval
	}
	data := GetБайтаўfromПаказальнік(uintptr(файлПаказальнік), int(памер), int(памер))
	чытаннеФайл(назва[:назваlen], data)
	if памер < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		памяцьmanager.Вольна(файлПаказальнік)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(data)
	loader.Parse(data, getcr3())
	памяцьmanager.Вольна(файлПаказальнік)
	if result := setupВыкананнеstack(цП, &arguments_2, &environment); result < 0 {
		return result
	}
	закрыцьonВыкананне(ensureДзейныПрацэс())
	цП.Eip = entry
	цП.Eax = 0
	return 0
}

func sysfork(цП *TcpuСтан) int32 {
	parentpid := Дзейныpid()
	if ensureДзейныПрацэс() == nil {
		return Enfile
	}
	pid := allocateПрацэс(parentpid)
	if pid == 0 {
		return Einval
	}
	памяцьmanager := &mem.TПамяцьmanager{}
	threadПаказальнік := памяцьmanager.Malloc(uint32(Sizeof(TThread{})))
	stackПаказальнік := памяцьmanager.Malloc(ThreadstackПамер)
	childСтаронкаКаталог := CloneaddressПрагалcow(getcr3())
	if threadПаказальнік == nil || stackПаказальнік == nil || childСтаронкаКаталог == 0 {
		discardПрацэс(pid)
		return Einval
	}
	child := (*TThread)(threadПаказальнік)
	child.Stack = uint32(uintptr(stackПаказальнік))
	child.ЦПСтан = (*TcpuСтан)(Pointer(uintptr(stackПаказальнік) + ThreadstackПамер - Sizeof(TcpuСтан{})))
	*child.ЦПСтан = *цП
	child.ЦПСтан.Eax = 0
	child.Карыстальнікstack_2 = цП.Esp
	child.КарыстальнікstackПамер_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.СтаронкаКаталогentry = childСтаронкаКаталог
	child.ThreadСтан = Гатова
	child.Fpuoffset = 0xffffffff
	child.Iskernel = false
	Дадацьrunnablethread(child)
	return int32(pid)
}

func sysВыхад(стан uint32) {
	pid := Дзейныpid()
	for i := 0; i < len(працэсТабліца); i++ {
		if працэсТабліца[i].выкарыстана && працэсТабліца[i].pid == pid {
			закрыцьУсеПрацэсfds(&працэсТабліца[i])
			працэсТабліца[i].exited = true
			працэсТабліца[i].стан = (стан & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, станaddress uint32, парамэтры uint32) int32 {
	if (парамэтры & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Дзейныpid()
	foundchild := false
	for i := 0; i < len(працэсТабліца); i++ {
		p := &працэсТабліца[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.выкарыстана && matches && p.parent == parentpid {
			foundchild = true
			if p.exited {
				if станaddress != 0 {
					*(*uint32)(Pointer(uintptr(станaddress))) = p.стан
				}
				childpid := p.pid
				*p = працэсentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (парамэтры & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПрацэс(parent uint32) uint32 {
	parentПрацэс := пошукПрацэс(parent)
	pid := Allocatepid()
	for i := 0; i < len(працэсТабліца); i++ {
		if !працэсТабліца[i].выкарыстана {
			працэсТабліца[i] = працэсentry{
				выкарыстана:	true,
				pid:		pid,
				parent:		parent,
				праграмаbreak:	карыстальнікheapbase,
			}
			if parentПрацэс != nil {
				працэсТабліца[i].праграмаbreak = parentПрацэс.праграмаbreak
				for fd := 0; fd < maxfd; fd++ {
					if parentПрацэс.fds[fd].выкарыстана {
						працэсТабліца[i].fds[fd] = parentПрацэс.fds[fd]
						апісанне := parentПрацэс.fds[fd].апісанне
						if апісанне >= 0 && апісанне < maxАдкрыцьФАЙЛЫ {
							адкрыцьФайлТабліца[апісанне].refs++
						}
					}
				}
			} else {
				initializeПрацэсfds(&працэсТабліца[i])
			}
			return pid
		}
	}
	return 0
}

func закрыцьУсеПрацэсfds(працэс *працэсentry) {
	if працэс == nil {
		return
	}
	for fd := int32(0); fd < maxfd; fd++ {
		if працэс.fds[fd].выкарыстана {
			закрыцьПрацэсfd(працэс, fd)
		}
	}
}

func discardПрацэс(pid uint32) {
	працэс := пошукПрацэс(pid)
	if працэс == nil {
		return
	}
	закрыцьУсеПрацэсfds(працэс)
	*працэс = працэсentry{}
}

func скапіявацьШЛЯХ(шЛЯХaddress uint32) (uint32, [12]byte) {
	var назва [12]byte
	if шЛЯХaddress == 0 {
		return 0, назва
	}
	raw := GetБайтаўfromПаказальнік(uintptr(шЛЯХaddress), 64, 64)
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
		назва[n] = c
		n++
	}
	return n, назва
}

func файлПамер(назвафайла []byte) uint32 {
	var ata0s = TДадатковаТэхналогіяattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабліца{}
	partition.Чытаннеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	памер := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], назвафайла)
	ata0s.Flush()
	return памер
}

func чытаннеФайл(назвафайла []byte, data []byte) {
	var ata0s = TДадатковаТэхналогіяattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабліца{}
	partition.Чытаннеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Чытанне(&ata0s, partition.Mbr.Primarypartition[0], назвафайла, data)
	ata0s.Flush()
}

func getcr3() uint32
