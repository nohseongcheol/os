/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package системаcall

import . "unsafe"

import . "переривання"
import . "консоль"
import . "util"
import . "multitasking"
import . "driver/ата"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"
import . "файлСистема/виконуваний_і_компонований_формат"
import mem "памятьmanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "віртуальнийПамять"

var консоль_2 = TКонсоль{}

type TSyscall struct {
	TПерериванняhandler
}

const (
	SysВийти	uint32	= 1
	Sysfork		uint32	= 2
	SysЧитання	uint32	= 3
	SysЗапис	uint32	= 4
	SysВідкрити	uint32	= 5
	SysЗакрити	uint32	= 6
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
	SysrtВийти	uint32	= 252

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
	максимумfd			= 32
	максимумВідкритиФайли		= 128
)

type fdзапис struct {
	використано	bool
	опис		int32
	fdПрапори	uint32
}

type відкритиФайлОпис struct {
	використано	bool
	refs		uint32
	тип		uint32
	прапори		uint32
	позиція		uint32
	розмір		uint32
	назва		[12]byte
	назваlen	uint32
	aux		uint32
}

const (
	fdТипНемає	uint32	= 0
	fdТипfat	uint32	= 1
	fdТипstdin	uint32	= 2
	fdТипКонсоль	uint32	= 3
	fdТипКоріньТека	uint32	= 4
	fdТипСокет	uint32	= 5

	oЧитанняonly	uint32	= 0
	oЗаписonly	uint32	= 1
	oЧитанняЗапис	uint32	= 2
	ocreate		uint32	= 0x40
	oСкоротити	uint32	= 0x200
	oappend		uint32	= 0x400
	oТека		uint32	= 0x10000

	seekмножина	uint32	= 0
	seekПоточна	uint32	= 1
	seekКінець	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fмножинаfd	uint32	= 2
	fgetfl		uint32	= 3
	fмножинаfl	uint32	= 4
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
	максимумsockets		= 32
	максимумСокетпакетів	= 8
	максимумdatagramРозмір	= 512
)

type сокетАдресаipv4 struct {
	Family	uint16
	Порт	uint16
	Адреса	uint32
	Нуль	[8]byte
}

type сокетПАКЕТ struct {
	використано	bool
	розмір		uint32
	джерело		сокетАдресаipv4
	data		[максимумdatagramРозмір]byte
}

type локальнийdatagramСокет struct {
	використано	bool
	bound		bool
	connected	bool
	локальний	сокетАдресаipv4
	віддалене	сокетАдресаipv4
	head		uint32
	tail		uint32
	відлік		uint32
	пакетів		[максимумСокетпакетів]сокетПАКЕТ
}

type posixstat struct {
	Пристрій	uint32
	Ino		uint32
	РЕЖИМ		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Розмір_2	int32
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
	Версія		[65]byte
	Machine		[65]byte
}

const (
	максимумВиконатиvectorзапис	= 16
	максимумВиконатиРядокДовжина	= 63
)

type виконатиvector struct {
	відлік		uint32
	lengths		[максимумВиконатиvectorзапис]uint32
	значення_2	[максимумВиконатиvectorзапис][максимумВиконатиРядокДовжина + 1]byte
}

type процесизапис struct {
	використано		bool
	ідентифікаторPID	uint32
	батько			uint32
	вийти			bool
	статус			uint32
	програмаbreak		uint32
	fds			[максимумfd]fdзапис
}

type рядокheader struct {
	Data	uintptr
	Len	int
}

func syscallПомилка(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var відкритиФайлТаблиця [максимумВідкритиФайли]відкритиФайлОпис
var процесиТаблиця [32]процесизапис
var локальнийsockets [максимумsockets]локальнийdatagramСокет
var наступнеephemeralПорт uint16 = 49152

const (
	користувачheapbase	uint32	= 0x06000000
	користувачheapОбмеження	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinЧитання uint32
var stdinЗапис uint32

func Переривання(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysВийти_2(індекс uint32) {
	Syscall(SysВийти, індекс)
}

func SysЧитання_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysЧитання, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysДрукstr(buffer string) {
	h := (*рядокheader)(Pointer(&buffer))
	Syscall(SysЗапис, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysДрукunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysЗапис, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysВідкрити_2(шЛЯХ uintptr, прапори uint32, рЕЖИМ uint32) int32 {
	return int32(Syscall(SysВідкрити, uint32(шЛЯХ), прапори, рЕЖИМ))
}

func SysЗакрити_2(fd uint32) int32 {
	return int32(Syscall(SysЗакрити, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(адреса uint32) uint32 {
	return Syscall(Sysbrk, адреса)
}

func Syscall(параметри_2 ...uint32) uint32 {

	l := len(параметри_2)
	switch l {
	case 1:
		return Переривання(параметри_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Переривання(параметри_2[0], параметри_2[1], 0, 0, 0, 0)
	case 3:
		return Переривання(параметри_2[0], параметри_2[1], параметри_2[2], 0, 0, 0)
	case 4:
		return Переривання(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], 0, 0)
	case 5:
		return Переривання(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], параметри_2[4], 0)
	case 6:
		return Переривання(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], параметри_2[4], параметри_2[5])
	default:
		return syscallПомилка(Enosys)
	}
}

func (поточний *TSyscall) Init(manager *TПерериванняmanager) {
	initФайлdescriptor()

	перериванняhandler = елементкеруванняПереривання

	var адреса uintptr
	адреса = uintptr(Pointer(&перериванняhandler))

	поточний.TПерериванняhandler.Init(0x80, uintptr(Pointer(manager)), адреса)
}

var перериванняhandler func(uint32) uint32

func елементкеруванняПереривання(esp uint32) uint32 {
	var процесор = (*TcpuСтан)(Pointer(uintptr(esp)))

	switch процесор.Eax {
	case SysВийти:
		sysВийти(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗупинитиПоточнаthread(процесор))))
	case SysrtВийти:
		sysВийти(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗупинитиПоточнаthread(процесор))))
	case Sysfork:
		процесор.Eax = uint32(sysfork(процесор))
		return esp
	case SysЧитання:
		процесор.Eax = uint32(sysЧитання(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysЗапис:
		процесор.Eax = uint32(sysЗапис(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysВідкрити:
		процесор.Eax = uint32(sysВідкрити(процесор.Ebx, процесор.Ecx, процесор.Edx))
		return esp
	case Syscreat:
		процесор.Eax = uint32(sysВідкрити(процесор.Ebx, ocreate|oЗаписonly|oСкоротити, процесор.Ecx))
		return esp
	case SysЗакрити:
		процесор.Eax = uint32(sysЗакрити(int32(процесор.Ebx)))
		return esp
	case Syswaitpid:
		процесор.Eax = uint32(syswaitpid(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case Syslseek:
		процесор.Eax = uint32(syslseek(int32(процесор.Ebx), int32(процесор.Ecx), процесор.Edx))
		return esp
	case Sysexecve:
		процесор.Eax = uint32(sysexecve(процесор, процесор.Ebx))
		return esp
	case Sysgetpid:
		процесор.Eax = ПоточнаІдентифікаторPID()
		return esp
	case Sysgetppid:
		процесор.Eax = ПоточнабатькоІдентифікаторPID()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		процесор.Eax = 0
		return esp
	case Sysдоступ:
		процесор.Eax = uint32(sysдоступ(процесор.Ebx, процесор.Ecx))
		return esp
	case Syschdir:
		процесор.Eax = uint32(syschdir(процесор.Ebx))
		return esp
	case Sysgetcwd:
		процесор.Eax = uint32(sysgetcwd(процесор.Ebx, процесор.Ecx))
		return esp
	case Sysdup:
		процесор.Eax = uint32(sysdup(int32(процесор.Ebx), 0))
		return esp
	case Sysdup2:
		процесор.Eax = uint32(sysdup2(int32(процесор.Ebx), int32(процесор.Ecx)))
		return esp
	case Syssocketcall:
		процесор.Eax = uint32(sysСокетcall(процесор.Ebx, процесор.Ecx))
		return esp
	case Sysfcntl:
		процесор.Eax = uint32(sysfcntl(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case Sysstat, Syslstat:
		процесор.Eax = uint32(sysstat(процесор.Ebx, процесор.Ecx))
		return esp
	case Sysfstat:
		процесор.Eax = uint32(sysfstat(int32(процесор.Ebx), процесор.Ecx))
		return esp
	case Sysfsync:
		процесор.Eax = uint32(sysfsync(int32(процесор.Ebx)))
		return esp
	case Syssync:
		процесор.Eax = 0
		return esp
	case Sysuname:
		процесор.Eax = uint32(sysuname(процесор.Ebx))
		return esp
	case Sysbrk:
		процесор.Eax = sysbrk(процесор.Ebx)
		return esp
	case 9:
		консоль_2.MUnsignedinteger32Друк(процесор.Ebx)
		return esp

	default:
		консоль_2.MДрукxy(([]byte)("sys["), 1, 23)
		консоль_2.MUnsignedinteger32Друк(esp)
		консоль_2.MДрук(([]byte)(":"))
		консоль_2.MUnsignedinteger32Друк(процесор.Eax)
		консоль_2.MДрук(([]byte)(":"))
		консоль_2.MUnsignedinteger32Друк(процесор.Ebx)
		консоль_2.MДрук(([]byte)(":"))
		консоль_2.MUnsignedinteger32Друк(процесор.Ecx)
		консоль_2.MДрук(([]byte)(":"))
		консоль_2.MUnsignedinteger32Друк(процесор.Edx)
		консоль_2.MДрук(([]byte)("]"))
		процесор.Eax = syscallПомилка(Enosys)
		return esp
	}

	return esp
}

func initФайлdescriptor() {
	for i := 0; i < максимумВідкритиФайли; i++ {
		відкритиФайлТаблиця[i] = відкритиФайлОпис{}
	}
	for i := 0; i < len(процесиТаблиця); i++ {
		процесиТаблиця[i] = процесизапис{}
	}
	for i := 0; i < len(локальнийsockets); i++ {
		локальнийsockets[i] = локальнийdatagramСокет{}
	}
	наступнеephemeralПорт = 49152
	відкритиФайлТаблиця[0] = відкритиФайлОпис{використано: true, тип: fdТипstdin, прапори: oЧитанняonly}
	відкритиФайлТаблиця[1] = відкритиФайлОпис{використано: true, тип: fdТипКонсоль, прапори: oЗаписonly}
	відкритиФайлТаблиця[2] = відкритиФайлОпис{використано: true, тип: fdТипКонсоль, прапори: oЗаписonly}
}

func знайтиПроцеси(ідентифікаторPID uint32) *процесизапис {
	for i := 0; i < len(процесиТаблиця); i++ {
		if процесиТаблиця[i].використано && процесиТаблиця[i].ідентифікаторPID == ідентифікаторPID {
			return &процесиТаблиця[i]
		}
	}
	return nil
}

func initializeПроцесиfds(процеси *процесизапис) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		процеси.fds[fd] = fdзапис{використано: true, опис: fd}
		відкритиФайлТаблиця[fd].refs++
	}
}

func ensureПоточнаПроцеси() *процесизапис {
	ідентифікаторPID := ПоточнаІдентифікаторPID()
	if процеси := знайтиПроцеси(ідентифікаторPID); процеси != nil {
		return процеси
	}
	for i := 0; i < len(процесиТаблиця); i++ {
		if !процесиТаблиця[i].використано {
			процесиТаблиця[i] = процесизапис{
				використано:		true,
				ідентифікаторPID:	ідентифікаторPID,
				батько:			ПоточнабатькоІдентифікаторPID(),
				програмаbreak:		користувачheapbase,
			}
			initializeПроцесиfds(&процесиТаблиця[i])
			return &процесиТаблиця[i]
		}
	}
	return nil
}

func getВідкритиФайлfor(процеси *процесизапис, fd int32) *відкритиФайлОпис {
	if процеси == nil || fd < 0 || fd >= максимумfd || !процеси.fds[fd].використано {
		return nil
	}
	опис := процеси.fds[fd].опис
	if опис < 0 || опис >= максимумВідкритиФайли || !відкритиФайлТаблиця[опис].використано {
		return nil
	}
	return &відкритиФайлТаблиця[опис]
}

func getВідкритиФайл(fd int32) *відкритиФайлОпис {
	return getВідкритиФайлfor(ensureПоточнаПроцеси(), fd)
}

func allocateВідкритиФайл() int32 {
	for i := int32(3); i < максимумВідкритиФайли; i++ {
		if !відкритиФайлТаблиця[i].використано {
			відкритиФайлТаблиця[i] = відкритиФайлОпис{використано: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(процеси *процесизапис, опис int32, мінімум int32) int32 {
	if процеси == nil {
		return Enfile
	}
	if мінімум < 0 || мінімум >= максимумfd {
		return Einval
	}
	for fd := мінімум; fd < максимумfd; fd++ {
		if !процеси.fds[fd].використано {
			процеси.fds[fd] = fdзапис{використано: true, опис: опис}
			return fd
		}
	}
	return Emfile
}

func releaseВідкритиФайл(опис int32) {
	if опис < 0 || опис >= максимумВідкритиФайли {
		return
	}
	запис := &відкритиФайлТаблиця[опис]
	if запис.refs > 0 {
		запис.refs--
	}

	if запис.refs == 0 && опис > stderrfd {
		if запис.тип == fdТипСокет && запис.aux < максимумsockets {
			локальнийsockets[запис.aux] = локальнийdatagramСокет{}
		}
		*запис = відкритиФайлОпис{}
	}
}

func закритиПроцесиfd(процеси *процесизапис, fd int32) int32 {
	if процеси == nil || getВідкритиФайлfor(процеси, fd) == nil {
		return Ebadf
	}
	опис := процеси.fds[fd].опис
	процеси.fds[fd] = fdзапис{}
	releaseВідкритиФайл(опис)
	return 0
}

func sysЗапис(fd int32, адреса uint32, відлік uint32) int32 {
	if відлік == 0 {
		return 0
	}
	if адреса == 0 || адреса+відлік < адреса {
		return Efault
	}
	if відлік > 4096 {
		return Einval
	}
	запис := getВідкритиФайл(fd)
	if запис == nil {
		return Ebadf
	}
	if запис.тип != fdТипКонсоль {
		if запис.тип == fdТипСокет {
			return сокетНадіслатито(fd, адреса, відлік, 0, 0)
		}
		if запис.тип == fdТипfat || запис.тип == fdТипКоріньТека {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтзВказівник(uintptr(адреса), int(відлік), int(відлік))
	консоль_2.MДрук(buffer)
	return int32(відлік)
}

func sysЧитання(fd int32, адреса uint32, відлік uint32) int32 {
	if відлік == 0 {
		return 0
	}
	if адреса == 0 || адреса+відлік < адреса {
		return Efault
	}
	запис := getВідкритиФайл(fd)
	if запис == nil {
		return Ebadf
	}
	if запис.тип == fdТипstdin {
		return читанняstdin(адреса, відлік)
	}
	if запис.тип == fdТипКоріньТека {
		return Eisdir
	}
	if запис.тип == fdТипСокет {
		return сокетreceiveз(fd, адреса, відлік, 0, 0)
	}
	if запис.тип != fdТипfat {
		return Ebadf
	}
	if запис.позиція >= запис.розмір {
		return 0
	}
	remaining := запис.розмір - запис.позиція
	if відлік > remaining {
		відлік = remaining
	}
	buffer := GetБайтзВказівник(uintptr(адреса), int(відлік), int(відлік))
	return читанняvfsФайл(запис, buffer, відлік)
}

func sysВідкрити(шЛЯХАдреса uint32, прапори uint32, рЕЖИМ uint32) int32 {
	_ = рЕЖИМ
	if шЛЯХАдреса == 0 {
		return Efault
	}
	доступРЕЖИМ := прапори & 3
	if доступРЕЖИМ == oЗаписonly || доступРЕЖИМ == oЧитанняЗапис || (прапори&(ocreate|oСкоротити|oappend)) != 0 {
		return Erofs
	}

	процеси := ensureПоточнаПроцеси()
	if процеси == nil {
		return Enfile
	}
	опис := allocateВідкритиФайл()
	if опис < 0 {
		return опис
	}
	запис := &відкритиФайлТаблиця[опис]
	запис.прапори = прапори
	if isКоріньШЛЯХ(шЛЯХАдреса) {
		запис.тип = fdТипКоріньТека
		запис.розмір = 0
	} else {
		назваlen, назва := копіюватиШЛЯХ(шЛЯХАдреса)
		if назваlen == 0 {
			*запис = відкритиФайлОпис{}
			return Enoent
		}
		розмір := файлРозмір(назва[:назваlen])
		if розмір == 0 {
			*запис = відкритиФайлОпис{}
			return Enoent
		}
		if (прапори & oТека) != 0 {
			*запис = відкритиФайлОпис{}
			return Enotdir
		}
		запис.тип = fdТипfat
		запис.розмір = розмір
		запис.назваlen = назваlen
		запис.назва = назва
	}

	fd := allocatefd(процеси, опис, 3)
	if fd < 0 {
		*запис = відкритиФайлОпис{}
		return fd
	}
	return fd
}

func sysЗакрити(fd int32) int32 {
	return закритиПроцесиfd(ensureПоточнаПроцеси(), fd)
}

func sysdup(fd int32, мінімум int32) int32 {
	процеси := ensureПоточнаПроцеси()
	запис := getВідкритиФайлfor(процеси, fd)
	if запис == nil {
		return Ebadf
	}
	новийfd := allocatefd(процеси, процеси.fds[fd].опис, мінімум)
	if новийfd >= 0 {
		запис.refs++
	}
	return новийfd
}

func sysdup2(oldfd int32, новийfd int32) int32 {
	процеси := ensureПоточнаПроцеси()
	запис := getВідкритиФайлfor(процеси, oldfd)
	if запис == nil {
		return Ebadf
	}
	if новийfd < 0 || новийfd >= максимумfd {
		return Ebadf
	}
	if oldfd == новийfd {
		return новийfd
	}
	if процеси.fds[новийfd].використано {
		закритиПроцесиfd(процеси, новийfd)
	}
	процеси.fds[новийfd] = fdзапис{використано: true, опис: процеси.fds[oldfd].опис}
	запис.refs++
	return новийfd
}

func sysfcntl(fd int32, команда uint32, argument uint32) int32 {
	процеси := ensureПоточнаПроцеси()
	запис := getВідкритиФайлfor(процеси, fd)
	if запис == nil {
		return Ebadf
	}
	switch команда {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(процеси.fds[fd].fdПрапори)
	case fмножинаfd:
		процеси.fds[fd].fdПрапори = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(запис.прапори)
	case fмножинаfl:
		запис.прапори = (запис.прапори & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	запис := getВідкритиФайл(fd)
	if запис == nil {
		return Ebadf
	}
	if запис.тип != fdТипfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekмножина:
		base = 0
	case seekПоточна:
		base = int64(запис.позиція)
	case seekКінець:
		base = int64(запис.розмір)
	default:
		return Einval
	}
	позиція_2 := base + int64(offset)
	if позиція_2 < 0 || позиція_2 > 0x7FFFFFFF {
		return Einval
	}
	запис.позиція = uint32(позиція_2)
	return int32(запис.позиція)
}

func читанняvfsФайл(запис *відкритиФайлОпис, призначення_2 []byte, відлік uint32) int32 {
	памятьmanager := &mem.TПамятьmanager{}
	tmpВказівник := памятьmanager.Виділити_памʼять(запис.розмір)
	if tmpВказівник == nil {
		return Einval
	}
	tmp := GetБайтзВказівник(uintptr(tmpВказівник), int(запис.розмір), int(запис.розмір))
	читанняФайл(запис.назва[:запис.назваlen], tmp)
	copy(призначення_2[:відлік], tmp[запис.позиція:запис.позиція+відлік])
	запис.позиція += відлік
	памятьmanager.Вільно(tmpВказівник)
	return int32(відлік)
}

func isКоріньШЛЯХ(шЛЯХАдреса uint32) bool {
	if шЛЯХАдреса == 0 {
		return false
	}
	шЛЯХ := GetБайтзВказівник(uintptr(шЛЯХАдреса), 4, 4)
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

func sysдоступ(шЛЯХАдреса uint32, рЕЖИМ uint32) int32 {
	if шЛЯХАдреса == 0 {
		return Efault
	}
	if (рЕЖИМ & ^uint32(7)) != 0 {
		return Einval
	}
	isКорінь := isКоріньШЛЯХ(шЛЯХАдреса)
	exists := isКорінь
	if !exists {
		назваlen, назва := копіюватиШЛЯХ(шЛЯХАдреса)
		exists = назваlen != 0 && файлРозмір(назва[:назваlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (рЕЖИМ & 2) != 0 {
		return Eacces
	}

	if (рЕЖИМ&1) != 0 && !isКорінь {
		return Eacces
	}
	return 0
}

func syschdir(шЛЯХАдреса uint32) int32 {
	if шЛЯХАдреса == 0 {
		return Efault
	}
	if !isКоріньШЛЯХ(шЛЯХАдреса) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferАдреса uint32, розмір uint32) int32 {
	if bufferАдреса == 0 {
		return Efault
	}
	if розмір < 2 {
		return Erange
	}
	buffer_2 := GetБайтзВказівник(uintptr(bufferАдреса), int(розмір), int(розмір))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(statАдреса uint32, рЕЖИМ uint32, розмір uint32, iвузол uint32) int32 {
	if statАдреса == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(statАдреса)))
	*stat = posixstat{}
	stat.Пристрій = 1
	stat.Ino = iвузол
	stat.РЕЖИМ = рЕЖИМ
	stat.Nlink = 1
	stat.Розмір_2 = int32(розмір)
	stat.Blksize = 512
	stat.Блок = int32((розмір + 511) / 512)
	return 0
}

func sysstat(шЛЯХАдреса uint32, statАдреса uint32) int32 {
	if шЛЯХАдреса == 0 {
		return Efault
	}
	if isКоріньШЛЯХ(шЛЯХАдреса) {
		return fillposixstat(statАдреса, sifdir|0555, 0, 1)
	}
	назваlen, назва := копіюватиШЛЯХ(шЛЯХАдреса)
	if назваlen == 0 {
		return Enoent
	}
	розмір := файлРозмір(назва[:назваlen])
	if розмір == 0 {
		return Enoent
	}
	iвузол := uint32(2)
	for i := uint32(0); i < назваlen; i++ {
		iвузол = iвузол*33 + uint32(назва[i])
	}
	return fillposixstat(statАдреса, sifreg|0444, розмір, iвузол)
}

func sysfstat(fd int32, statАдреса uint32) int32 {
	запис := getВідкритиФайл(fd)
	if запис == nil {
		return Ebadf
	}
	switch запис.тип {
	case fdТипstdin, fdТипКонсоль:
		return fillposixstat(statАдреса, sifchr|0666, 0, uint32(fd+1))
	case fdТипКоріньТека:
		return fillposixstat(statАдреса, sifdir|0555, 0, 1)
	case fdТипfat:
		return fillposixstat(statАдреса, sifreg|0444, запис.розмір, uint32(fd+2))
	case fdТипСокет:
		return fillposixstat(statАдреса, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getВідкритиФайл(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(адреса_2 uint32) uint32 {
	процеси := ensureПоточнаПроцеси()
	if процеси == nil {
		return 0
	}
	if процеси.програмаbreak == 0 {
		процеси.програмаbreak = користувачheapbase
	}
	if адреса_2 == 0 {
		return процеси.програмаbreak
	}
	if адреса_2 < користувачheapbase || адреса_2 > користувачheapОбмеження {
		return процеси.програмаbreak
	}
	процеси.програмаbreak = адреса_2
	return процеси.програмаbreak
}

func копіюватиutsполе(призначення *[65]byte, значення string) {
	обмеження := len(значення)
	if обмеження > 64 {
		обмеження = 64
	}
	for i := 0; i < обмеження; i++ {
		призначення[i] = значення[i]
	}
	призначення[обмеження] = 0
}

func sysuname(адреса_2 uint32) int32 {
	if адреса_2 == 0 {
		return Efault
	}
	назва := (*posixutsname)(Pointer(uintptr(адреса_2)))
	*назва = posixutsname{}
	копіюватиutsполе(&назва.Sysname, "EngOS")
	копіюватиutsполе(&назва.Nodename, "engos")
	копіюватиutsполе(&назва.Release, "0.1-posix")
	копіюватиutsполе(&назва.Версія, "POSIX.1-2017 phase 1")
	копіюватиutsполе(&назва.Machine, "i386")
	return 0
}

func свопunsignedinteger16(значення uint16) uint16 {
	return (значення << 8) | (значення >> 8)
}

func сокетcallargument(аргументи_2 uint32, індекс uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(аргументи_2 + індекс*4)))
}

func сокетforfd(fd int32) (*локальнийdatagramСокет, int32) {
	запис := getВідкритиФайл(fd)
	if запис == nil || запис.тип != fdТипСокет || запис.aux >= максимумsockets {
		return nil, Ebadf
	}
	сокет := &локальнийsockets[запис.aux]
	if !сокет.використано {
		return nil, Ebadf
	}
	return сокет, 0
}

func allocateСокет(домен uint32, сокетТип uint32, protocol uint32) int32 {
	if домен != afinet {
		return Eafnosupport
	}
	if сокетТип != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процеси := ensureПоточнаПроцеси()
	if процеси == nil {
		return Enfile
	}
	сокетІндекс := -1
	for i := 0; i < максимумsockets; i++ {
		if !локальнийsockets[i].використано {
			сокетІндекс = i
			break
		}
	}
	if сокетІндекс < 0 {
		return Enfile
	}
	опис := allocateВідкритиФайл()
	if опис < 0 {
		return опис
	}
	локальнийsockets[сокетІндекс] = локальнийdatagramСокет{використано: true}
	запис := &відкритиФайлТаблиця[опис]
	запис.тип = fdТипСокет
	запис.прапори = oЧитанняЗапис
	запис.aux = uint32(сокетІндекс)
	fd := allocatefd(процеси, опис, 3)
	if fd < 0 {
		локальнийsockets[сокетІндекс] = локальнийdatagramСокет{}
		*запис = відкритиФайлОпис{}
		return fd
	}
	return fd
}

func сокетАдреса(адреса_2 uint32, довжина uint32) (*сокетАдресаipv4, int32) {
	if адреса_2 == 0 {
		return nil, Efault
	}
	if довжина < 16 {
		return nil, Einval
	}
	яРЛИК := (*сокетАдресаipv4)(Pointer(uintptr(адреса_2)))
	if яРЛИК.Family != afinet {
		return nil, Eafnosupport
	}
	return яРЛИК, 0
}

func портВхіднийВикористати(порт uint16, except *локальнийdatagramСокет) bool {
	for i := 0; i < максимумsockets; i++ {
		сокет := &локальнийsockets[i]
		if сокет != except && сокет.використано && сокет.bound && сокет.локальний.Порт == порт {
			return true
		}
	}
	return false
}

func повязатиephemeral(сокет *локальнийdatagramСокет) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := свопunsignedinteger16(наступнеephemeralПорт)
		наступнеephemeralПорт++
		if наступнеephemeralПорт < 49152 {
			наступнеephemeralПорт = 49152
		}
		if !портВхіднийВикористати(порт, сокет) {
			сокет.локальний = сокетАдресаipv4{Family: afinet, Порт: порт, Адреса: 0x0100007F}
			сокет.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func сокетПовязати(fd int32, адреса_2 uint32, довжина uint32) int32 {
	сокет, err := сокетforfd(fd)
	if err != 0 {
		return err
	}
	requested, err := сокетАдреса(адреса_2, довжина)
	if err != 0 {
		return err
	}
	if сокет.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return повязатиephemeral(сокет)
	}
	if портВхіднийВикористати(requested.Порт, сокет) {
		return Eaddrinuse
	}
	сокет.локальний = *requested
	сокет.bound = true
	return 0
}

func сокетЗєднати(fd int32, адреса_2 uint32, довжина uint32) int32 {
	сокет, err := сокетforfd(fd)
	if err != 0 {
		return err
	}
	віддалене, err := сокетАдреса(адреса_2, довжина)
	if err != 0 {
		return err
	}
	if !сокет.bound {
		if err := повязатиephemeral(сокет); err != 0 {
			return err
		}
	}
	сокет.віддалене = *віддалене
	сокет.connected = true
	return 0
}

func сокетНадіслатито(fd int32, bufferАдреса_2 uint32, довжина uint32, призначенняАдреса uint32, призначенняДовжина uint32) int32 {
	сокет, err := сокетforfd(fd)
	if err != 0 {
		return err
	}
	if довжина > максимумdatagramРозмір {
		return Emsgsize
	}
	if довжина != 0 && bufferАдреса_2 == 0 {
		return Efault
	}
	var призначення сокетАдресаipv4
	if призначенняАдреса != 0 {
		адреса_2, адресаПомилка := сокетАдреса(призначенняАдреса, призначенняДовжина)
		if адресаПомилка != 0 {
			return адресаПомилка
		}
		призначення = *адреса_2
	} else {
		if !сокет.connected {
			return Enotconn
		}
		призначення = сокет.віддалене
	}
	if !сокет.bound {
		if повязатиПомилка := повязатиephemeral(сокет); повязатиПомилка != 0 {
			return повязатиПомилка
		}
	}
	var receiver *локальнийdatagramСокет
	for i := 0; i < максимумsockets; i++ {
		candidate := &локальнийsockets[i]
		if candidate.використано && candidate.bound && candidate.локальний.Порт == призначення.Порт &&
			(candidate.локальний.Адреса == 0 || candidate.локальний.Адреса == призначення.Адреса) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.відлік >= максимумСокетпакетів {
		return Eagain
	}
	пАКЕТ := &receiver.пакетів[receiver.tail]
	*пАКЕТ = сокетПАКЕТ{використано: true, розмір: довжина, джерело: сокет.локальний}
	if довжина != 0 {
		джерело := GetБайтзВказівник(uintptr(bufferАдреса_2), int(довжина), int(довжина))
		copy(пАКЕТ.data[:довжина], джерело)
	}
	receiver.tail = (receiver.tail + 1) % максимумСокетпакетів
	receiver.відлік++
	return int32(довжина)
}

func сокетreceiveз(fd int32, bufferАдреса_2 uint32, довжина uint32, джерелоАдреса uint32, джерелоДовжинаАдреса uint32) int32 {
	сокет, err := сокетforfd(fd)
	if err != 0 {
		return err
	}
	if довжина != 0 && bufferАдреса_2 == 0 {
		return Efault
	}
	if сокет.відлік == 0 {
		return Eagain
	}
	пАКЕТ := &сокет.пакетів[сокет.head]
	копіюватиДовжина := пАКЕТ.розмір
	if копіюватиДовжина > довжина {
		копіюватиДовжина = довжина
	}
	if копіюватиДовжина != 0 {
		призначення := GetБайтзВказівник(uintptr(bufferАдреса_2), int(копіюватиДовжина), int(копіюватиДовжина))
		copy(призначення, пАКЕТ.data[:копіюватиДовжина])
	}
	if джерелоАдреса != 0 {
		if джерелоДовжинаАдреса == 0 {
			return Efault
		}
		providedДовжина := (*uint32)(Pointer(uintptr(джерелоДовжинаАдреса)))
		if *providedДовжина >= 16 {
			*(*сокетАдресаipv4)(Pointer(uintptr(джерелоАдреса))) = пАКЕТ.джерело
		}
		*providedДовжина = 16
	}
	*пАКЕТ = сокетПАКЕТ{}
	сокет.head = (сокет.head + 1) % максимумСокетпакетів
	сокет.відлік--
	return int32(копіюватиДовжина)
}

func копіюватиСокетНазва(fd int32, адреса_2 uint32, довжинаАдреса uint32, peer bool) int32 {
	сокет, err := сокетforfd(fd)
	if err != 0 {
		return err
	}
	if адреса_2 == 0 || довжинаАдреса == 0 {
		return Efault
	}
	довжина := (*uint32)(Pointer(uintptr(довжинаАдреса)))
	if *довжина < 16 {
		*довжина = 16
		return Einval
	}
	if peer {
		if !сокет.connected {
			return Enotconn
		}
		*(*сокетАдресаipv4)(Pointer(uintptr(адреса_2))) = сокет.віддалене
	} else {
		if !сокет.bound {
			if повязатиПомилка := повязатиephemeral(сокет); повязатиПомилка != 0 {
				return повязатиПомилка
			}
		}
		*(*сокетАдресаipv4)(Pointer(uintptr(адреса_2))) = сокет.локальний
	}
	*довжина = 16
	return 0
}

func sysСокетcall(call uint32, аргументи_2 uint32) int32 {
	if аргументи_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateСокет(сокетcallargument(аргументи_2, 0), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2))
	case 2:
		return сокетПовязати(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2))
	case 3:
		return сокетЗєднати(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return копіюватиСокетНазва(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), false)
	case 7:
		return копіюватиСокетНазва(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), true)
	case 9:
		return сокетНадіслатито(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), 0, 0)
	case 10:
		return сокетreceiveз(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), 0, 0)
	case 11:
		return сокетНадіслатито(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), сокетcallargument(аргументи_2, 4), сокетcallargument(аргументи_2, 5))
	case 12:
		return сокетreceiveз(int32(сокетcallargument(аргументи_2, 0)), сокетcallargument(аргументи_2, 1), сокетcallargument(аргументи_2, 2), сокетcallargument(аргументи_2, 4), сокетcallargument(аргументи_2, 5))
	case 13:
		if _, err := сокетforfd(int32(сокетcallargument(аргументи_2, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := сокетforfd(int32(сокетcallargument(аргументи_2, 0))); err != 0 {
			return err
		}
		return 0
	}
	return Eopnotsupp
}

func читанняstdin(адреса uint32, відлік uint32) int32 {
	if адреса == 0 {
		return Einval
	}
	buffer := GetБайтзВказівник(uintptr(адреса), int(відлік), int(відлік))
	var n uint32
	for n < відлік {
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
	наступне := (stdinЗапис + 1) % uint32(len(stdinbuffer))
	if наступне == stdinЧитання {
		return
	}
	stdinbuffer[stdinЗапис] = c
	stdinЗапис = наступне
}

func stdingetblocking() byte {
	for stdinЧитання == stdinЗапис {
		sc := pollКлавіатураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinЧитання]
	stdinЧитання = (stdinЧитання + 1) % uint32(len(stdinbuffer))
	return c
}

func pollКлавіатураscancode() byte {
	for (ПортЧитанняbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортЧитанняbyte(0x60)
	return scancodeтоbyte(sc)
}

func scancodeтоbyte(sc uint8) byte {
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

func копіюватиВиконатиvector(адреса_2 uint32, яРЛИК *виконатиvector) int32 {
	*яРЛИК = виконатиvector{}
	if адреса_2 == 0 {
		return 0
	}
	for індекс := uint32(0); індекс < максимумВиконатиvectorзапис; індекс++ {
		рядокАдреса := *(*uint32)(Pointer(uintptr(адреса_2 + індекс*4)))
		if рядокАдреса == 0 {
			яРЛИК.відлік = індекс
			return 0
		}
		terminated := false
		for довжина := uint32(0); довжина <= максимумВиконатиРядокДовжина; довжина++ {
			значення := *(*byte)(Pointer(uintptr(рядокАдреса + довжина)))
			яРЛИК.значення_2[індекс][довжина] = значення
			if значення == 0 {
				яРЛИК.lengths[індекс] = довжина
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

func pushВиконатиunsignedinteger32(стекова_памʼять *uint32, значення uint32) {
	*стекова_памʼять -= 4
	*(*uint32)(Pointer(uintptr(*стекова_памʼять))) = значення
}

func setupВиконатиstack(процесор *TcpuСтан, аргументи_2 *виконатиvector, environment *виконатиvector) int32 {
	const stackБайт uint32 = 4096
	if !MakeДіяпазонЗакритаwritable(getcr3(), КористувачstackЗверху-stackБайт, stackБайт) {
		return Enomem
	}
	стекова_памʼять := КористувачstackЗверху
	var argumentpointers [максимумВиконатиvectorзапис]uint32
	var environmentpointers [максимумВиконатиvectorзапис]uint32

	for i := int(environment.відлік) - 1; i >= 0; i-- {
		довжина := environment.lengths[i] + 1
		стекова_памʼять -= довжина
		призначення := GetБайтзВказівник(uintptr(стекова_памʼять), int(довжина), int(довжина))
		copy(призначення, environment.значення_2[i][:довжина])
		environmentpointers[i] = стекова_памʼять
	}
	for i := int(аргументи_2.відлік) - 1; i >= 0; i-- {
		довжина := аргументи_2.lengths[i] + 1
		стекова_памʼять -= довжина
		призначення := GetБайтзВказівник(uintptr(стекова_памʼять), int(довжина), int(довжина))
		copy(призначення, аргументи_2.значення_2[i][:довжина])
		argumentpointers[i] = стекова_памʼять
	}
	стекова_памʼять &= ^uint32(3)
	pushВиконатиunsignedinteger32(&стекова_памʼять, 0)
	for i := int(environment.відлік) - 1; i >= 0; i-- {
		pushВиконатиunsignedinteger32(&стекова_памʼять, environmentpointers[i])
	}
	pushВиконатиunsignedinteger32(&стекова_памʼять, 0)
	for i := int(аргументи_2.відлік) - 1; i >= 0; i-- {
		pushВиконатиunsignedinteger32(&стекова_памʼять, argumentpointers[i])
	}
	pushВиконатиunsignedinteger32(&стекова_памʼять, аргументи_2.відлік)
	процесор.Esp = стекова_памʼять
	процесор.Ebp = 0
	return 0
}

func закритиУвімкненоВиконати(процеси *процесизапис) {
	if процеси == nil {
		return
	}
	for fd := int32(0); fd < максимумfd; fd++ {
		if процеси.fds[fd].використано && (процеси.fds[fd].fdПрапори&fdcloexec) != 0 {
			закритиПроцесиfd(процеси, fd)
		}
	}
}

func sysexecve(процесор *TcpuСтан, шЛЯХАдреса uint32) int32 {
	if шЛЯХАдреса == 0 {
		return Efault
	}
	var аргументи_2 виконатиvector
	var environment виконатиvector
	if яРЛИК := копіюватиВиконатиvector(процесор.Ecx, &аргументи_2); яРЛИК < 0 {
		return яРЛИК
	}
	if яРЛИК := копіюватиВиконатиvector(процесор.Edx, &environment); яРЛИК < 0 {
		return яРЛИК
	}
	назваlen, назва := копіюватиШЛЯХ(шЛЯХАдреса)
	if назваlen == 0 {
		return Enoent
	}
	розмір := файлРозмір(назва[:назваlen])
	if розмір == 0 {
		return Enoent
	}
	памятьmanager := &mem.TПамятьmanager{}
	файлВказівник := памятьmanager.Виділити_памʼять(розмір)
	if файлВказівник == nil {
		return Einval
	}
	data := GetБайтзВказівник(uintptr(файлВказівник), int(розмір), int(розмір))
	читанняФайл(назва[:назваlen], data)
	if розмір < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		памятьmanager.Вільно(файлВказівник)
		return Enoexec
	}
	loader := Elf{}
	запис := loader.Getзапис(data)
	loader.Parse(data, getcr3())
	памятьmanager.Вільно(файлВказівник)
	if яРЛИК := setupВиконатиstack(процесор, &аргументи_2, &environment); яРЛИК < 0 {
		return яРЛИК
	}
	закритиУвімкненоВиконати(ensureПоточнаПроцеси())
	процесор.Eip = запис
	процесор.Eax = 0
	return 0
}

func sysfork(процесор *TcpuСтан) int32 {
	батькоІдентифікаторPID := ПоточнаІдентифікаторPID()
	if ensureПоточнаПроцеси() == nil {
		return Enfile
	}
	ідентифікаторPID := allocateПроцеси(батькоІдентифікаторPID)
	if ідентифікаторPID == 0 {
		return Einval
	}
	памятьmanager := &mem.TПамятьmanager{}
	threadВказівник := памятьmanager.Виділити_памʼять(uint32(Sizeof(TThread{})))
	stackВказівник := памятьmanager.Виділити_памʼять(ThreadstackРозмір)
	дочірнійобєктСторінкаТека := CloneАдресаПробілcow(getcr3())
	if threadВказівник == nil || stackВказівник == nil || дочірнійобєктСторінкаТека == 0 {
		відкинутиПроцеси(ідентифікаторPID)
		return Einval
	}
	дочірнійобєкт := (*TThread)(threadВказівник)
	дочірнійобєкт.Stack = uint32(uintptr(stackВказівник))
	дочірнійобєкт.ПроцесорСтан = (*TcpuСтан)(Pointer(uintptr(stackВказівник) + ThreadstackРозмір - Sizeof(TcpuСтан{})))
	*дочірнійобєкт.ПроцесорСтан = *процесор
	дочірнійобєкт.ПроцесорСтан.Eax = 0
	дочірнійобєкт.Користувачstack_2 = процесор.Esp
	дочірнійобєкт.КористувачstackРозмір_2 = 0
	дочірнійобєкт.ІдентифікаторPID = ідентифікаторPID
	дочірнійобєкт.БатькоІдентифікаторPID = батькоІдентифікаторPID
	дочірнійобєкт.СторінкаТеказапис = дочірнійобєктСторінкаТека
	дочірнійобєкт.ThreadСтан = Готово
	дочірнійобєкт.Fpuoffset = 0xffffffff
	дочірнійобєкт.Iskernel = false
	Додатиrunnablethread(дочірнійобєкт)
	return int32(ідентифікаторPID)
}

func sysВийти(статус uint32) {
	ідентифікаторPID := ПоточнаІдентифікаторPID()
	for i := 0; i < len(процесиТаблиця); i++ {
		if процесиТаблиця[i].використано && процесиТаблиця[i].ідентифікаторPID == ідентифікаторPID {
			закритиВсіПроцесиfds(&процесиТаблиця[i])
			процесиТаблиця[i].вийти = true
			процесиТаблиця[i].статус = (статус & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(ідентифікаторPID int32, статусАдреса uint32, параметри uint32) int32 {
	if (параметри & ^uint32(1)) != 0 {
		return Einval
	}
	батькоІдентифікаторPID := ПоточнаІдентифікаторPID()
	foundдочірнійобєкт := false
	for i := 0; i < len(процесиТаблиця); i++ {
		p := &процесиТаблиця[i]
		matches := ідентифікаторPID == -1 || ідентифікаторPID == 0 || p.ідентифікаторPID == uint32(ідентифікаторPID)
		if p.використано && matches && p.батько == батькоІдентифікаторPID {
			foundдочірнійобєкт = true
			if p.вийти {
				if статусАдреса != 0 {
					*(*uint32)(Pointer(uintptr(статусАдреса))) = p.статус
				}
				дочірнійобєктІдентифікаторPID := p.ідентифікаторPID
				*p = процесизапис{}
				return int32(дочірнійобєктІдентифікаторPID)
			}
		}
	}
	if !foundдочірнійобєкт {
		return Echild
	}

	if (параметри & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцеси(батько uint32) uint32 {
	батькоПроцеси := знайтиПроцеси(батько)
	ідентифікаторPID := AllocateІдентифікаторPID()
	for i := 0; i < len(процесиТаблиця); i++ {
		if !процесиТаблиця[i].використано {
			процесиТаблиця[i] = процесизапис{
				використано:		true,
				ідентифікаторPID:	ідентифікаторPID,
				батько:			батько,
				програмаbreak:		користувачheapbase,
			}
			if батькоПроцеси != nil {
				процесиТаблиця[i].програмаbreak = батькоПроцеси.програмаbreak
				for fd := 0; fd < максимумfd; fd++ {
					if батькоПроцеси.fds[fd].використано {
						процесиТаблиця[i].fds[fd] = батькоПроцеси.fds[fd]
						опис := батькоПроцеси.fds[fd].опис
						if опис >= 0 && опис < максимумВідкритиФайли {
							відкритиФайлТаблиця[опис].refs++
						}
					}
				}
			} else {
				initializeПроцесиfds(&процесиТаблиця[i])
			}
			return ідентифікаторPID
		}
	}
	return 0
}

func закритиВсіПроцесиfds(процеси *процесизапис) {
	if процеси == nil {
		return
	}
	for fd := int32(0); fd < максимумfd; fd++ {
		if процеси.fds[fd].використано {
			закритиПроцесиfd(процеси, fd)
		}
	}
}

func відкинутиПроцеси(ідентифікаторPID uint32) {
	процеси := знайтиПроцеси(ідентифікаторPID)
	if процеси == nil {
		return
	}
	закритиВсіПроцесиfds(процеси)
	*процеси = процесизапис{}
}

func копіюватиШЛЯХ(шЛЯХАдреса uint32) (uint32, [12]byte) {
	var назва [12]byte
	if шЛЯХАдреса == 0 {
		return 0, назва
	}
	raw := GetБайтзВказівник(uintptr(шЛЯХАдреса), 64, 64)
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

func файлРозмір(назвафайлу []byte) uint32 {
	var ата0s = TДодатковоТехнологіяattachment{}
	ата0s.Init(false, 0x1F0)
	ата0s.Identify()

	partition := TmsdospartitionТаблиця{}
	partition.Читанняpartition(&ата0s)

	bios := TПараметри_файлової_системи32{}
	розмір := bios.Len(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу)
	ата0s.Flush()
	return розмір
}

func читанняФайл(назвафайлу []byte, data []byte) {
	var ата0s = TДодатковоТехнологіяattachment{}
	ата0s.Init(false, 0x1F0)
	ата0s.Identify()

	partition := TmsdospartitionТаблиця{}
	partition.Читанняpartition(&ата0s)

	bios := TПараметри_файлової_системи32{}
	bios.Читання(&ата0s, partition.Mbr.Primarypartition[0], назвафайлу, data)
	ата0s.Flush()
}

func getcr3() uint32
