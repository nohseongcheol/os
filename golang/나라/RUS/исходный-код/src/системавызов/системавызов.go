/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package системавызов

import . "unsafe"

import . "прерывание"
import . "консоль"
import . "утилита"
import . "многоуправлениеЗадачами"
import . "драйвер/ata"
import . "файлсистема/msdosразделДиска"
import . "файлсистема/fat"
import . "файлсистема/исполняемый_и_компонуемый_формат"
import mem "памятьдиспетчер"
import . "управлениеСтраницами"
import . "порт"
import . "управлениеЗадачами/планировщик"
import . "управлениеЗадачами/поток"
import . "виртуальныйпамять"

var консоль_2 = TКонсоль{}

type TSyscall struct {
	TПрерываниеhandler
}

const (
	SysВыход	uint32	= 1
	Sysfork		uint32	= 2
	Sysчитать	uint32	= 3
	Sysписать	uint32	= 4
	Sysоткрыть	uint32	= 5
	Sysзакрыть	uint32	= 6
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
	SysrtВыход	uint32	= 252

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
	максимумоткрытьФАЙЛЫ		= 128
)

type fdзапись struct {
	использовано	bool
	описание	int32
	fdФлаги		uint32
}

type открытьфайлОписание struct {
	использовано	bool
	refs		uint32
	тип		uint32
	флаги		uint32
	позиция		uint32
	размер		uint32
	имя		[12]byte
	имяlen		uint32
	aux		uint32
}

const (
	fdТипНет		uint32	= 0
	fdТипfat		uint32	= 1
	fdТипstdin		uint32	= 2
	fdТипконсоль		uint32	= 3
	fdТипКоренькаталог	uint32	= 4
	fdТипсокет		uint32	= 5

	oчитатьтолько		uint32	= 0
	oписатьтолько		uint32	= 1
	oчитатьписать		uint32	= 2
	oсоздать		uint32	= 0x40
	oЦелочисленнаячасть	uint32	= 0x200
	oappend			uint32	= 0x400
	oкаталог		uint32	= 0x10000

	seekуказать	uint32	= 0
	seekТекущаядата	uint32	= 1
	seekКонце	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fуказатьfd	uint32	= 2
	fgetfl		uint32	= 3
	fуказатьfl	uint32	= 4
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
	максимумсокетпакетов	= 8
	максимумdatagramРазмер	= 512
)

type сокетaddressipv4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Ноль	[8]byte
}

type сокетПАКЕТ struct {
	использовано	bool
	размер		uint32
	источник	сокетaddressipv4
	данные		[максимумdatagramРазмер]byte
}

type локальныйdatagramсокет struct {
	использовано	bool
	bound		bool
	connected	bool
	локальный	сокетaddressipv4
	сеть		сокетaddressipv4
	head		uint32
	tail		uint32
	количество	uint32
	пакетов		[максимумсокетпакетов]сокетПАКЕТ
}

type posixstat struct {
	Устройство	uint32
	Ino		uint32
	Режим		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Размер_2	int32
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
	Версия		[65]byte
	Machine		[65]byte
}

const (
	максимумВыполнениеvectorзапись	= 16
	максимумВыполнениеСтрокаДлина	= 63
)

type выполнениеvector struct {
	количество	uint32
	lengths		[максимумВыполнениеvectorзапись]uint32
	значений	[максимумВыполнениеvectorзапись][максимумВыполнениеСтрокаДлина + 1]byte
}

type процессзапись struct {
	использовано	bool
	pid		uint32
	родитель	uint32
	выход		bool
	состояние	uint32
	программаbreak	uint32
	fds		[максимумfd]fdзапись
}

type строказаголовок struct {
	Data	uintptr
	Len	int
}

func syscallОшибка(ошибка int32) uint32 {
	return *(*uint32)(Pointer(&ошибка))
}

var открытьфайлТаблица [максимумоткрытьФАЙЛЫ]открытьфайлОписание
var процессТаблица [32]процессзапись
var локальныйsockets [максимумsockets]локальныйdatagramсокет
var далееephemeralпорт uint16 = 49152

const (
	пользовательheapbase		uint32	= 0x06000000
	пользовательheapОграничение	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinчитать uint32
var stdinписать uint32

func Прерывание(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysВыход_2(содержание uint32) {
	Syscall(SysВыход, содержание)
}

func Sysчитать_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysчитать, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysПечатьstr(buffer string) {
	h := (*строказаголовок)(Pointer(&buffer))
	Syscall(Sysписать, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func SysПечатьunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysписать, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysоткрыть_2(пУТЬ uintptr, флаги uint32, режим uint32) int32 {
	return int32(Syscall(Sysоткрыть, uint32(пУТЬ), флаги, режим))
}

func Sysзакрыть_2(fd uint32) int32 {
	return int32(Syscall(Sysзакрыть, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(аргументы_3 ...uint32) uint32 {

	l := len(аргументы_3)
	switch l {
	case 1:
		return Прерывание(аргументы_3[0], 0, 0, 0, 0, 0)
	case 2:
		return Прерывание(аргументы_3[0], аргументы_3[1], 0, 0, 0, 0)
	case 3:
		return Прерывание(аргументы_3[0], аргументы_3[1], аргументы_3[2], 0, 0, 0)
	case 4:
		return Прерывание(аргументы_3[0], аргументы_3[1], аргументы_3[2], аргументы_3[3], 0, 0)
	case 5:
		return Прерывание(аргументы_3[0], аргументы_3[1], аргументы_3[2], аргументы_3[3], аргументы_3[4], 0)
	case 6:
		return Прерывание(аргументы_3[0], аргументы_3[1], аргументы_3[2], аргументы_3[3], аргументы_3[4], аргументы_3[5])
	default:
		return syscallОшибка(Enosys)
	}
}

func (текущий *TSyscall) Init(диспетчер *TПрерываниедиспетчер) {
	initфайлdescriptor()

	прерываниеhandler = ручкапрерывание

	var address uintptr
	address = uintptr(Pointer(&прерываниеhandler))

	текущий.TПрерываниеhandler.Init(0x80, uintptr(Pointer(диспетчер)), address)
}

var прерываниеhandler func(uint32) uint32

func ручкапрерывание(esp uint32) uint32 {
	var цП = (*TcpuСостояние)(Pointer(uintptr(esp)))

	switch цП.Eax {
	case SysВыход:
		sysВыход(цП.Ebx)
		return uint32(uintptr(Pointer(ОстановитьТекущаядатапоток(цП))))
	case SysrtВыход:
		sysВыход(цП.Ebx)
		return uint32(uintptr(Pointer(ОстановитьТекущаядатапоток(цП))))
	case Sysfork:
		цП.Eax = uint32(sysfork(цП))
		return esp
	case Sysчитать:
		цП.Eax = uint32(sysчитать(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case Sysписать:
		цП.Eax = uint32(sysписать(int32(цП.Ebx), цП.Ecx, цП.Edx))
		return esp
	case Sysоткрыть:
		цП.Eax = uint32(sysоткрыть(цП.Ebx, цП.Ecx, цП.Edx))
		return esp
	case Syscreat:
		цП.Eax = uint32(sysоткрыть(цП.Ebx, oсоздать|oписатьтолько|oЦелочисленнаячасть, цП.Ecx))
		return esp
	case Sysзакрыть:
		цП.Eax = uint32(sysзакрыть(int32(цП.Ebx)))
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
		цП.Eax = Текущаядатаpid()
		return esp
	case Sysgetppid:
		цП.Eax = Текущаядатародительpid()
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
		цП.Eax = uint32(sysсокетвызов(цП.Ebx, цП.Ecx))
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
		консоль_2.MUnsignedinteger32Печать(цП.Ebx)
		return esp

	default:
		консоль_2.MПечатьxy(([]byte)("sys["), 1, 23)
		консоль_2.MUnsignedinteger32Печать(esp)
		консоль_2.MПечать(([]byte)(":"))
		консоль_2.MUnsignedinteger32Печать(цП.Eax)
		консоль_2.MПечать(([]byte)(":"))
		консоль_2.MUnsignedinteger32Печать(цП.Ebx)
		консоль_2.MПечать(([]byte)(":"))
		консоль_2.MUnsignedinteger32Печать(цП.Ecx)
		консоль_2.MПечать(([]byte)(":"))
		консоль_2.MUnsignedinteger32Печать(цП.Edx)
		консоль_2.MПечать(([]byte)("]"))
		цП.Eax = syscallОшибка(Enosys)
		return esp
	}

	return esp
}

func initфайлdescriptor() {
	for i := 0; i < максимумоткрытьФАЙЛЫ; i++ {
		открытьфайлТаблица[i] = открытьфайлОписание{}
	}
	for i := 0; i < len(процессТаблица); i++ {
		процессТаблица[i] = процессзапись{}
	}
	for i := 0; i < len(локальныйsockets); i++ {
		локальныйsockets[i] = локальныйdatagramсокет{}
	}
	далееephemeralпорт = 49152
	открытьфайлТаблица[0] = открытьфайлОписание{использовано: true, тип: fdТипstdin, флаги: oчитатьтолько}
	открытьфайлТаблица[1] = открытьфайлОписание{использовано: true, тип: fdТипконсоль, флаги: oписатьтолько}
	открытьфайлТаблица[2] = открытьфайлОписание{использовано: true, тип: fdТипконсоль, флаги: oписатьтолько}
}

func найтипроцесс(pid uint32) *процессзапись {
	for i := 0; i < len(процессТаблица); i++ {
		if процессТаблица[i].использовано && процессТаблица[i].pid == pid {
			return &процессТаблица[i]
		}
	}
	return nil
}

func initializeпроцессfds(процесс *процессзапись) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		процесс.fds[fd] = fdзапись{использовано: true, описание: fd}
		открытьфайлТаблица[fd].refs++
	}
}

func ensureТекущаядатапроцесс() *процессзапись {
	pid := Текущаядатаpid()
	if процесс := найтипроцесс(pid); процесс != nil {
		return процесс
	}
	for i := 0; i < len(процессТаблица); i++ {
		if !процессТаблица[i].использовано {
			процессТаблица[i] = процессзапись{
				использовано:	true,
				pid:		pid,
				родитель:	Текущаядатародительpid(),
				программаbreak:	пользовательheapbase,
			}
			initializeпроцессfds(&процессТаблица[i])
			return &процессТаблица[i]
		}
	}
	return nil
}

func getоткрытьфайлfor(процесс *процессзапись, fd int32) *открытьфайлОписание {
	if процесс == nil || fd < 0 || fd >= максимумfd || !процесс.fds[fd].использовано {
		return nil
	}
	описание := процесс.fds[fd].описание
	if описание < 0 || описание >= максимумоткрытьФАЙЛЫ || !открытьфайлТаблица[описание].использовано {
		return nil
	}
	return &открытьфайлТаблица[описание]
}

func getоткрытьфайл(fd int32) *открытьфайлОписание {
	return getоткрытьфайлfor(ensureТекущаядатапроцесс(), fd)
}

func allocateоткрытьфайл() int32 {
	for i := int32(3); i < максимумоткрытьФАЙЛЫ; i++ {
		if !открытьфайлТаблица[i].использовано {
			открытьфайлТаблица[i] = открытьфайлОписание{использовано: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(процесс *процессзапись, описание int32, минимум int32) int32 {
	if процесс == nil {
		return Enfile
	}
	if минимум < 0 || минимум >= максимумfd {
		return Einval
	}
	for fd := минимум; fd < максимумfd; fd++ {
		if !процесс.fds[fd].использовано {
			процесс.fds[fd] = fdзапись{использовано: true, описание: описание}
			return fd
		}
	}
	return Emfile
}

func releaseоткрытьфайл(описание int32) {
	if описание < 0 || описание >= максимумоткрытьФАЙЛЫ {
		return
	}
	запись := &открытьфайлТаблица[описание]
	if запись.refs > 0 {
		запись.refs--
	}

	if запись.refs == 0 && описание > stderrfd {
		if запись.тип == fdТипсокет && запись.aux < максимумsockets {
			локальныйsockets[запись.aux] = локальныйdatagramсокет{}
		}
		*запись = открытьфайлОписание{}
	}
}

func закрытьпроцессfd(процесс *процессзапись, fd int32) int32 {
	if процесс == nil || getоткрытьфайлfor(процесс, fd) == nil {
		return Ebadf
	}
	описание := процесс.fds[fd].описание
	процесс.fds[fd] = fdзапись{}
	releaseоткрытьфайл(описание)
	return 0
}

func sysписать(fd int32, address uint32, количество uint32) int32 {
	if количество == 0 {
		return 0
	}
	if address == 0 || address+количество < address {
		return Efault
	}
	if количество > 4096 {
		return Einval
	}
	запись := getоткрытьфайл(fd)
	if запись == nil {
		return Ebadf
	}
	if запись.тип != fdТипконсоль {
		if запись.тип == fdТипсокет {
			return сокетОтправитьк(fd, address, количество, 0, 0)
		}
		if запись.тип == fdТипfat || запись.тип == fdТипКоренькаталог {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтfromУказатели(uintptr(address), int(количество), int(количество))
	консоль_2.MПечать(buffer)
	return int32(количество)
}

func sysчитать(fd int32, address uint32, количество uint32) int32 {
	if количество == 0 {
		return 0
	}
	if address == 0 || address+количество < address {
		return Efault
	}
	запись := getоткрытьфайл(fd)
	if запись == nil {
		return Ebadf
	}
	if запись.тип == fdТипstdin {
		return читатьstdin(address, количество)
	}
	if запись.тип == fdТипКоренькаталог {
		return Eisdir
	}
	if запись.тип == fdТипсокет {
		return сокетreceivefrom(fd, address, количество, 0, 0)
	}
	if запись.тип != fdТипfat {
		return Ebadf
	}
	if запись.позиция >= запись.размер {
		return 0
	}
	remaining := запись.размер - запись.позиция
	if количество > remaining {
		количество = remaining
	}
	buffer := GetБайтfromУказатели(uintptr(address), int(количество), int(количество))
	return читатьvfsфайл(запись, buffer, количество)
}

func sysоткрыть(пУТЬaddress uint32, флаги uint32, режим uint32) int32 {
	_ = режим
	if пУТЬaddress == 0 {
		return Efault
	}
	доступрежим := флаги & 3
	if доступрежим == oписатьтолько || доступрежим == oчитатьписать || (флаги&(oсоздать|oЦелочисленнаячасть|oappend)) != 0 {
		return Erofs
	}

	процесс := ensureТекущаядатапроцесс()
	if процесс == nil {
		return Enfile
	}
	описание := allocateоткрытьфайл()
	if описание < 0 {
		return описание
	}
	запись := &открытьфайлТаблица[описание]
	запись.флаги = флаги
	if isКореньПУТЬ(пУТЬaddress) {
		запись.тип = fdТипКоренькаталог
		запись.размер = 0
	} else {
		имяlen, имя := копироватьПУТЬ(пУТЬaddress)
		if имяlen == 0 {
			*запись = открытьфайлОписание{}
			return Enoent
		}
		размер := файлРазмер(имя[:имяlen])
		if размер == 0 {
			*запись = открытьфайлОписание{}
			return Enoent
		}
		if (флаги & oкаталог) != 0 {
			*запись = открытьфайлОписание{}
			return Enotdir
		}
		запись.тип = fdТипfat
		запись.размер = размер
		запись.имяlen = имяlen
		запись.имя = имя
	}

	fd := allocatefd(процесс, описание, 3)
	if fd < 0 {
		*запись = открытьфайлОписание{}
		return fd
	}
	return fd
}

func sysзакрыть(fd int32) int32 {
	return закрытьпроцессfd(ensureТекущаядатапроцесс(), fd)
}

func sysdup(fd int32, минимум int32) int32 {
	процесс := ensureТекущаядатапроцесс()
	запись := getоткрытьфайлfor(процесс, fd)
	if запись == nil {
		return Ebadf
	}
	новыйfd := allocatefd(процесс, процесс.fds[fd].описание, минимум)
	if новыйfd >= 0 {
		запись.refs++
	}
	return новыйfd
}

func sysdup2(oldfd int32, новыйfd int32) int32 {
	процесс := ensureТекущаядатапроцесс()
	запись := getоткрытьфайлfor(процесс, oldfd)
	if запись == nil {
		return Ebadf
	}
	if новыйfd < 0 || новыйfd >= максимумfd {
		return Ebadf
	}
	if oldfd == новыйfd {
		return новыйfd
	}
	if процесс.fds[новыйfd].использовано {
		закрытьпроцессfd(процесс, новыйfd)
	}
	процесс.fds[новыйfd] = fdзапись{использовано: true, описание: процесс.fds[oldfd].описание}
	запись.refs++
	return новыйfd
}

func sysfcntl(fd int32, команда uint32, argument uint32) int32 {
	процесс := ensureТекущаядатапроцесс()
	запись := getоткрытьфайлfor(процесс, fd)
	if запись == nil {
		return Ebadf
	}
	switch команда {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(процесс.fds[fd].fdФлаги)
	case fуказатьfd:
		процесс.fds[fd].fdФлаги = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(запись.флаги)
	case fуказатьfl:
		запись.флаги = (запись.флаги & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	запись := getоткрытьфайл(fd)
	if запись == nil {
		return Ebadf
	}
	if запись.тип != fdТипfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekуказать:
		base = 0
	case seekТекущаядата:
		base = int64(запись.позиция)
	case seekКонце:
		base = int64(запись.размер)
	default:
		return Einval
	}
	позиция_2 := base + int64(offset)
	if позиция_2 < 0 || позиция_2 > 0x7FFFFFFF {
		return Einval
	}
	запись.позиция = uint32(позиция_2)
	return int32(запись.позиция)
}

func читатьvfsфайл(запись *открытьфайлОписание, назначение_2 []byte, количество uint32) int32 {
	памятьдиспетчер := &mem.TПамятьдиспетчер{}
	tmpУказатели := памятьдиспетчер.Выделить_память(запись.размер)
	if tmpУказатели == nil {
		return Einval
	}
	tmp := GetБайтfromУказатели(uintptr(tmpУказатели), int(запись.размер), int(запись.размер))
	читатьфайл(запись.имя[:запись.имяlen], tmp)
	copy(назначение_2[:количество], tmp[запись.позиция:запись.позиция+количество])
	запись.позиция += количество
	памятьдиспетчер.Свободно(tmpУказатели)
	return int32(количество)
}

func isКореньПУТЬ(пУТЬaddress uint32) bool {
	if пУТЬaddress == 0 {
		return false
	}
	пУТЬ := GetБайтfromУказатели(uintptr(пУТЬaddress), 4, 4)
	if пУТЬ[0] == '/' && пУТЬ[1] == 0 {
		return true
	}
	if пУТЬ[0] == '.' && пУТЬ[1] == 0 {
		return true
	}
	if пУТЬ[0] == '/' && пУТЬ[1] == '.' && пУТЬ[2] == 0 {
		return true
	}
	return false
}

func sysдоступ(пУТЬaddress uint32, режим uint32) int32 {
	if пУТЬaddress == 0 {
		return Efault
	}
	if (режим & ^uint32(7)) != 0 {
		return Einval
	}
	isКорень := isКореньПУТЬ(пУТЬaddress)
	exists := isКорень
	if !exists {
		имяlen, имя := копироватьПУТЬ(пУТЬaddress)
		exists = имяlen != 0 && файлРазмер(имя[:имяlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (режим & 2) != 0 {
		return Eacces
	}

	if (режим&1) != 0 && !isКорень {
		return Eacces
	}
	return 0
}

func syschdir(пУТЬaddress uint32) int32 {
	if пУТЬaddress == 0 {
		return Efault
	}
	if !isКореньПУТЬ(пУТЬaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, размер uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if размер < 2 {
		return Erange
	}
	buffer_2 := GetБайтfromУказатели(uintptr(bufferaddress), int(размер), int(размер))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, режим uint32, размер uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Устройство = 1
	stat.Ino = inode
	stat.Режим = режим
	stat.Nlink = 1
	stat.Размер_2 = int32(размер)
	stat.Blksize = 512
	stat.Блок = int32((размер + 511) / 512)
	return 0
}

func sysstat(пУТЬaddress uint32, stataddress uint32) int32 {
	if пУТЬaddress == 0 {
		return Efault
	}
	if isКореньПУТЬ(пУТЬaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	имяlen, имя := копироватьПУТЬ(пУТЬaddress)
	if имяlen == 0 {
		return Enoent
	}
	размер := файлРазмер(имя[:имяlen])
	if размер == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < имяlen; i++ {
		inode = inode*33 + uint32(имя[i])
	}
	return fillposixstat(stataddress, sifreg|0444, размер, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	запись := getоткрытьфайл(fd)
	if запись == nil {
		return Ebadf
	}
	switch запись.тип {
	case fdТипstdin, fdТипконсоль:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdТипКоренькаталог:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdТипfat:
		return fillposixstat(stataddress, sifreg|0444, запись.размер, uint32(fd+2))
	case fdТипсокет:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getоткрытьфайл(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	процесс := ensureТекущаядатапроцесс()
	if процесс == nil {
		return 0
	}
	if процесс.программаbreak == 0 {
		процесс.программаbreak = пользовательheapbase
	}
	if address_2 == 0 {
		return процесс.программаbreak
	}
	if address_2 < пользовательheapbase || address_2 > пользовательheapОграничение {
		return процесс.программаbreak
	}
	процесс.программаbreak = address_2
	return процесс.программаbreak
}

func копироватьutsполе(назначение *[65]byte, значение string) {
	ограничение := len(значение)
	if ограничение > 64 {
		ограничение = 64
	}
	for i := 0; i < ограничение; i++ {
		назначение[i] = значение[i]
	}
	назначение[ограничение] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	имя := (*posixutsname)(Pointer(uintptr(address_2)))
	*имя = posixutsname{}
	копироватьutsполе(&имя.Sysname, "EngOS")
	копироватьutsполе(&имя.Nodename, "engos")
	копироватьutsполе(&имя.Release, "0.1-posix")
	копироватьutsполе(&имя.Версия, "POSIX.1-2017 phase 1")
	копироватьutsполе(&имя.Machine, "i386")
	return 0
}

func подкачкаunsignedinteger16(значение uint16) uint16 {
	return (значение << 8) | (значение >> 8)
}

func сокетвызовargument(аргументы_2 uint32, содержание uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(аргументы_2 + содержание*4)))
}

func сокетforfd(fd int32) (*локальныйdatagramсокет, int32) {
	запись := getоткрытьфайл(fd)
	if запись == nil || запись.тип != fdТипсокет || запись.aux >= максимумsockets {
		return nil, Ebadf
	}
	сокет := &локальныйsockets[запись.aux]
	if !сокет.использовано {
		return nil, Ebadf
	}
	return сокет, 0
}

func allocateсокет(домен uint32, сокеттип uint32, protocol uint32) int32 {
	if домен != afinet {
		return Eafnosupport
	}
	if сокеттип != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процесс := ensureТекущаядатапроцесс()
	if процесс == nil {
		return Enfile
	}
	сокетСодержание := -1
	for i := 0; i < максимумsockets; i++ {
		if !локальныйsockets[i].использовано {
			сокетСодержание = i
			break
		}
	}
	if сокетСодержание < 0 {
		return Enfile
	}
	описание := allocateоткрытьфайл()
	if описание < 0 {
		return описание
	}
	локальныйsockets[сокетСодержание] = локальныйdatagramсокет{использовано: true}
	запись := &открытьфайлТаблица[описание]
	запись.тип = fdТипсокет
	запись.флаги = oчитатьписать
	запись.aux = uint32(сокетСодержание)
	fd := allocatefd(процесс, описание, 3)
	if fd < 0 {
		локальныйsockets[сокетСодержание] = локальныйdatagramсокет{}
		*запись = открытьфайлОписание{}
		return fd
	}
	return fd
}

func сокетaddress(address_2 uint32, длина uint32) (*сокетaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if длина < 16 {
		return nil, Einval
	}
	рЕЗУЛЬТАТ := (*сокетaddressipv4)(Pointer(uintptr(address_2)))
	if рЕЗУЛЬТАТ.Family != afinet {
		return nil, Eafnosupport
	}
	return рЕЗУЛЬТАТ, 0
}

func портИсходящийИспользовать(порт uint16, except *локальныйdatagramсокет) bool {
	for i := 0; i < максимумsockets; i++ {
		сокет := &локальныйsockets[i]
		if сокет != except && сокет.использовано && сокет.bound && сокет.локальный.Порт == порт {
			return true
		}
	}
	return false
}

func прослушиватьephemeral(сокет *локальныйdatagramсокет) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := подкачкаunsignedinteger16(далееephemeralпорт)
		далееephemeralпорт++
		if далееephemeralпорт < 49152 {
			далееephemeralпорт = 49152
		}
		if !портИсходящийИспользовать(порт, сокет) {
			сокет.локальный = сокетaddressipv4{Family: afinet, Порт: порт, Address: 0x0100007F}
			сокет.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func сокетПрослушивать(fd int32, address_2 uint32, длина uint32) int32 {
	сокет, ошибка := сокетforfd(fd)
	if ошибка != 0 {
		return ошибка
	}
	requested, ошибка := сокетaddress(address_2, длина)
	if ошибка != 0 {
		return ошибка
	}
	if сокет.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return прослушиватьephemeral(сокет)
	}
	if портИсходящийИспользовать(requested.Порт, сокет) {
		return Eaddrinuse
	}
	сокет.локальный = *requested
	сокет.bound = true
	return 0
}

func сокетПодключить(fd int32, address_2 uint32, длина uint32) int32 {
	сокет, ошибка := сокетforfd(fd)
	if ошибка != 0 {
		return ошибка
	}
	сеть, ошибка := сокетaddress(address_2, длина)
	if ошибка != 0 {
		return ошибка
	}
	if !сокет.bound {
		if ошибка := прослушиватьephemeral(сокет); ошибка != 0 {
			return ошибка
		}
	}
	сокет.сеть = *сеть
	сокет.connected = true
	return 0
}

func сокетОтправитьк(fd int32, bufferaddress_2 uint32, длина uint32, назначениеaddress uint32, назначениеДлина uint32) int32 {
	сокет, ошибка := сокетforfd(fd)
	if ошибка != 0 {
		return ошибка
	}
	if длина > максимумdatagramРазмер {
		return Emsgsize
	}
	if длина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var назначение сокетaddressipv4
	if назначениеaddress != 0 {
		address_2, addressОшибка := сокетaddress(назначениеaddress, назначениеДлина)
		if addressОшибка != 0 {
			return addressОшибка
		}
		назначение = *address_2
	} else {
		if !сокет.connected {
			return Enotconn
		}
		назначение = сокет.сеть
	}
	if !сокет.bound {
		if прослушиватьОшибка := прослушиватьephemeral(сокет); прослушиватьОшибка != 0 {
			return прослушиватьОшибка
		}
	}
	var receiver *локальныйdatagramсокет
	for i := 0; i < максимумsockets; i++ {
		candidate := &локальныйsockets[i]
		if candidate.использовано && candidate.bound && candidate.локальный.Порт == назначение.Порт &&
			(candidate.локальный.Address == 0 || candidate.локальный.Address == назначение.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.количество >= максимумсокетпакетов {
		return Eagain
	}
	пАКЕТ := &receiver.пакетов[receiver.tail]
	*пАКЕТ = сокетПАКЕТ{использовано: true, размер: длина, источник: сокет.локальный}
	if длина != 0 {
		источник := GetБайтfromУказатели(uintptr(bufferaddress_2), int(длина), int(длина))
		copy(пАКЕТ.данные[:длина], источник)
	}
	receiver.tail = (receiver.tail + 1) % максимумсокетпакетов
	receiver.количество++
	return int32(длина)
}

func сокетreceivefrom(fd int32, bufferaddress_2 uint32, длина uint32, источникaddress uint32, источникДлинаaddress uint32) int32 {
	сокет, ошибка := сокетforfd(fd)
	if ошибка != 0 {
		return ошибка
	}
	if длина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if сокет.количество == 0 {
		return Eagain
	}
	пАКЕТ := &сокет.пакетов[сокет.head]
	копироватьДлина := пАКЕТ.размер
	if копироватьДлина > длина {
		копироватьДлина = длина
	}
	if копироватьДлина != 0 {
		назначение := GetБайтfromУказатели(uintptr(bufferaddress_2), int(копироватьДлина), int(копироватьДлина))
		copy(назначение, пАКЕТ.данные[:копироватьДлина])
	}
	if источникaddress != 0 {
		if источникДлинаaddress == 0 {
			return Efault
		}
		providedДлина := (*uint32)(Pointer(uintptr(источникДлинаaddress)))
		if *providedДлина >= 16 {
			*(*сокетaddressipv4)(Pointer(uintptr(источникaddress))) = пАКЕТ.источник
		}
		*providedДлина = 16
	}
	*пАКЕТ = сокетПАКЕТ{}
	сокет.head = (сокет.head + 1) % максимумсокетпакетов
	сокет.количество--
	return int32(копироватьДлина)
}

func копироватьсокетИмя(fd int32, address_2 uint32, длинаaddress uint32, peer bool) int32 {
	сокет, ошибка := сокетforfd(fd)
	if ошибка != 0 {
		return ошибка
	}
	if address_2 == 0 || длинаaddress == 0 {
		return Efault
	}
	длина := (*uint32)(Pointer(uintptr(длинаaddress)))
	if *длина < 16 {
		*длина = 16
		return Einval
	}
	if peer {
		if !сокет.connected {
			return Enotconn
		}
		*(*сокетaddressipv4)(Pointer(uintptr(address_2))) = сокет.сеть
	} else {
		if !сокет.bound {
			if прослушиватьОшибка := прослушиватьephemeral(сокет); прослушиватьОшибка != 0 {
				return прослушиватьОшибка
			}
		}
		*(*сокетaddressipv4)(Pointer(uintptr(address_2))) = сокет.локальный
	}
	*длина = 16
	return 0
}

func sysсокетвызов(вызов uint32, аргументы_2 uint32) int32 {
	if аргументы_2 == 0 {
		return Efault
	}
	switch вызов {
	case 1:
		return allocateсокет(сокетвызовargument(аргументы_2, 0), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2))
	case 2:
		return сокетПрослушивать(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2))
	case 3:
		return сокетПодключить(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return копироватьсокетИмя(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), false)
	case 7:
		return копироватьсокетИмя(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), true)
	case 9:
		return сокетОтправитьк(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), 0, 0)
	case 10:
		return сокетreceivefrom(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), 0, 0)
	case 11:
		return сокетОтправитьк(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), сокетвызовargument(аргументы_2, 4), сокетвызовargument(аргументы_2, 5))
	case 12:
		return сокетreceivefrom(int32(сокетвызовargument(аргументы_2, 0)), сокетвызовargument(аргументы_2, 1), сокетвызовargument(аргументы_2, 2), сокетвызовargument(аргументы_2, 4), сокетвызовargument(аргументы_2, 5))
	case 13:
		if _, ошибка := сокетforfd(int32(сокетвызовargument(аргументы_2, 0))); ошибка != 0 {
			return ошибка
		}
		return 0
	case 14:
		if _, ошибка := сокетforfd(int32(сокетвызовargument(аргументы_2, 0))); ошибка != 0 {
			return ошибка
		}
		return 0
	}
	return Eopnotsupp
}

func читатьstdin(address uint32, количество uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБайтfromУказатели(uintptr(address), int(количество), int(количество))
	var n uint32
	for n < количество {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputбайт(c byte) {
	далее := (stdinписать + 1) % uint32(len(stdinbuffer))
	if далее == stdinчитать {
		return
	}
	stdinbuffer[stdinписать] = c
	stdinписать = далее
}

func stdingetblocking() byte {
	for stdinчитать == stdinписать {
		sc := pollклавиатураscancode()
		if sc != 0 {
			Stdinputбайт(sc)
		}
	}
	c := stdinbuffer[stdinчитать]
	stdinчитать = (stdinчитать + 1) % uint32(len(stdinbuffer))
	return c
}

func pollклавиатураscancode() byte {
	for (Портчитатьбайт(0x64) & 0x01) == 0 {
	}
	sc := Портчитатьбайт(0x60)
	return scancodeкбайт(sc)
}

func scancodeкбайт(sc uint8) byte {
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

func копироватьВыполнениеvector(address_2 uint32, рЕЗУЛЬТАТ *выполнениеvector) int32 {
	*рЕЗУЛЬТАТ = выполнениеvector{}
	if address_2 == 0 {
		return 0
	}
	for содержание := uint32(0); содержание < максимумВыполнениеvectorзапись; содержание++ {
		строкаaddress := *(*uint32)(Pointer(uintptr(address_2 + содержание*4)))
		if строкаaddress == 0 {
			рЕЗУЛЬТАТ.количество = содержание
			return 0
		}
		terminated := false
		for длина := uint32(0); длина <= максимумВыполнениеСтрокаДлина; длина++ {
			значение := *(*byte)(Pointer(uintptr(строкаaddress + длина)))
			рЕЗУЛЬТАТ.значений[содержание][длина] = значение
			if значение == 0 {
				рЕЗУЛЬТАТ.lengths[содержание] = длина
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

func pushВыполнениеunsignedinteger32(стековая_память *uint32, значение uint32) {
	*стековая_память -= 4
	*(*uint32)(Pointer(uintptr(*стековая_память))) = значение
}

func setupВыполнениеstack(цП *TcpuСостояние, аргументы_2 *выполнениеvector, environment *выполнениеvector) int32 {
	const stackБайт uint32 = 4096
	if !MakeДиапазонЧастнаяwritable(getcr3(), ПользовательstackСверху-stackБайт, stackБайт) {
		return Enomem
	}
	стековая_память := ПользовательstackСверху
	var argumentpointers [максимумВыполнениеvectorзапись]uint32
	var environmentpointers [максимумВыполнениеvectorзапись]uint32

	for i := int(environment.количество) - 1; i >= 0; i-- {
		длина := environment.lengths[i] + 1
		стековая_память -= длина
		назначение := GetБайтfromУказатели(uintptr(стековая_память), int(длина), int(длина))
		copy(назначение, environment.значений[i][:длина])
		environmentpointers[i] = стековая_память
	}
	for i := int(аргументы_2.количество) - 1; i >= 0; i-- {
		длина := аргументы_2.lengths[i] + 1
		стековая_память -= длина
		назначение := GetБайтfromУказатели(uintptr(стековая_память), int(длина), int(длина))
		copy(назначение, аргументы_2.значений[i][:длина])
		argumentpointers[i] = стековая_память
	}
	стековая_память &= ^uint32(3)
	pushВыполнениеunsignedinteger32(&стековая_память, 0)
	for i := int(environment.количество) - 1; i >= 0; i-- {
		pushВыполнениеunsignedinteger32(&стековая_память, environmentpointers[i])
	}
	pushВыполнениеunsignedinteger32(&стековая_память, 0)
	for i := int(аргументы_2.количество) - 1; i >= 0; i-- {
		pushВыполнениеunsignedinteger32(&стековая_память, argumentpointers[i])
	}
	pushВыполнениеunsignedinteger32(&стековая_память, аргументы_2.количество)
	цП.Esp = стековая_память
	цП.Ebp = 0
	return 0
}

func закрытьприВыполнение(процесс *процессзапись) {
	if процесс == nil {
		return
	}
	for fd := int32(0); fd < максимумfd; fd++ {
		if процесс.fds[fd].использовано && (процесс.fds[fd].fdФлаги&fdcloexec) != 0 {
			закрытьпроцессfd(процесс, fd)
		}
	}
}

func sysexecve(цП *TcpuСостояние, пУТЬaddress uint32) int32 {
	if пУТЬaddress == 0 {
		return Efault
	}
	var аргументы_2 выполнениеvector
	var environment выполнениеvector
	if рЕЗУЛЬТАТ := копироватьВыполнениеvector(цП.Ecx, &аргументы_2); рЕЗУЛЬТАТ < 0 {
		return рЕЗУЛЬТАТ
	}
	if рЕЗУЛЬТАТ := копироватьВыполнениеvector(цП.Edx, &environment); рЕЗУЛЬТАТ < 0 {
		return рЕЗУЛЬТАТ
	}
	имяlen, имя := копироватьПУТЬ(пУТЬaddress)
	if имяlen == 0 {
		return Enoent
	}
	размер := файлРазмер(имя[:имяlen])
	if размер == 0 {
		return Enoent
	}
	памятьдиспетчер := &mem.TПамятьдиспетчер{}
	файлУказатели := памятьдиспетчер.Выделить_память(размер)
	if файлУказатели == nil {
		return Einval
	}
	данные := GetБайтfromУказатели(uintptr(файлУказатели), int(размер), int(размер))
	читатьфайл(имя[:имяlen], данные)
	if размер < 52 || данные[0] != 0x7F || данные[1] != 'E' || данные[2] != 'L' || данные[3] != 'F' {
		памятьдиспетчер.Свободно(файлУказатели)
		return Enoexec
	}
	loader := Elf{}
	запись := loader.Getзапись(данные)
	loader.Parse(данные, getcr3())
	памятьдиспетчер.Свободно(файлУказатели)
	if рЕЗУЛЬТАТ := setupВыполнениеstack(цП, &аргументы_2, &environment); рЕЗУЛЬТАТ < 0 {
		return рЕЗУЛЬТАТ
	}
	закрытьприВыполнение(ensureТекущаядатапроцесс())
	цП.Eip = запись
	цП.Eax = 0
	return 0
}

func sysfork(цП *TcpuСостояние) int32 {
	родительpid := Текущаядатаpid()
	if ensureТекущаядатапроцесс() == nil {
		return Enfile
	}
	pid := allocateпроцесс(родительpid)
	if pid == 0 {
		return Einval
	}
	памятьдиспетчер := &mem.TПамятьдиспетчер{}
	потокУказатели := памятьдиспетчер.Выделить_память(uint32(Sizeof(TПоток{})))
	stackУказатели := памятьдиспетчер.Выделить_память(ПотокstackРазмер)
	потомокстраницакаталог := CloneaddressПробелcow(getcr3())
	if потокУказатели == nil || stackУказатели == nil || потомокстраницакаталог == 0 {
		отклонитьпроцесс(pid)
		return Einval
	}
	потомок := (*TПоток)(потокУказатели)
	потомок.Stack = uint32(uintptr(stackУказатели))
	потомок.ЦПСостояние = (*TcpuСостояние)(Pointer(uintptr(stackУказатели) + ПотокstackРазмер - Sizeof(TcpuСостояние{})))
	*потомок.ЦПСостояние = *цП
	потомок.ЦПСостояние.Eax = 0
	потомок.Пользовательstack_2 = цП.Esp
	потомок.ПользовательstackРазмер_2 = 0
	потомок.Pid = pid
	потомок.Родительpid = родительpid
	потомок.Страницакаталогзапись = потомокстраницакаталог
	потомок.ПотокСостояние = Готово
	потомок.Fpuoffset = 0xffffffff
	потомок.Isядро = false
	Добавитьrunnableпоток(потомок)
	return int32(pid)
}

func sysВыход(состояние uint32) {
	pid := Текущаядатаpid()
	for i := 0; i < len(процессТаблица); i++ {
		if процессТаблица[i].использовано && процессТаблица[i].pid == pid {
			закрытьВсепроцессfds(&процессТаблица[i])
			процессТаблица[i].выход = true
			процессТаблица[i].состояние = (состояние & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, состояниеaddress uint32, параметры uint32) int32 {
	if (параметры & ^uint32(1)) != 0 {
		return Einval
	}
	родительpid := Текущаядатаpid()
	foundпотомок := false
	for i := 0; i < len(процессТаблица); i++ {
		p := &процессТаблица[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.использовано && matches && p.родитель == родительpid {
			foundпотомок = true
			if p.выход {
				if состояниеaddress != 0 {
					*(*uint32)(Pointer(uintptr(состояниеaddress))) = p.состояние
				}
				потомокpid := p.pid
				*p = процессзапись{}
				return int32(потомокpid)
			}
		}
	}
	if !foundпотомок {
		return Echild
	}

	if (параметры & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateпроцесс(родитель uint32) uint32 {
	родительпроцесс := найтипроцесс(родитель)
	pid := Allocatepid()
	for i := 0; i < len(процессТаблица); i++ {
		if !процессТаблица[i].использовано {
			процессТаблица[i] = процессзапись{
				использовано:	true,
				pid:		pid,
				родитель:	родитель,
				программаbreak:	пользовательheapbase,
			}
			if родительпроцесс != nil {
				процессТаблица[i].программаbreak = родительпроцесс.программаbreak
				for fd := 0; fd < максимумfd; fd++ {
					if родительпроцесс.fds[fd].использовано {
						процессТаблица[i].fds[fd] = родительпроцесс.fds[fd]
						описание := родительпроцесс.fds[fd].описание
						if описание >= 0 && описание < максимумоткрытьФАЙЛЫ {
							открытьфайлТаблица[описание].refs++
						}
					}
				}
			} else {
				initializeпроцессfds(&процессТаблица[i])
			}
			return pid
		}
	}
	return 0
}

func закрытьВсепроцессfds(процесс *процессзапись) {
	if процесс == nil {
		return
	}
	for fd := int32(0); fd < максимумfd; fd++ {
		if процесс.fds[fd].использовано {
			закрытьпроцессfd(процесс, fd)
		}
	}
}

func отклонитьпроцесс(pid uint32) {
	процесс := найтипроцесс(pid)
	if процесс == nil {
		return
	}
	закрытьВсепроцессfds(процесс)
	*процесс = процессзапись{}
}

func копироватьПУТЬ(пУТЬaddress uint32) (uint32, [12]byte) {
	var имя [12]byte
	if пУТЬaddress == 0 {
		return 0, имя
	}
	raw := GetБайтfromУказатели(uintptr(пУТЬaddress), 64, 64)
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
		имя[n] = c
		n++
	}
	return n, имя
}

func файлРазмер(имяфайла []byte) uint32 {
	var ata0s = TДополнительноТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	разделДиска := TmsdosразделДискаТаблица{}
	разделДиска.ЧитатьразделДиска(&ata0s)

	bios := TПараметры_файловой_системы32{}
	размер := bios.Len(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла)
	ata0s.Flush()
	return размер
}

func читатьфайл(имяфайла []byte, данные []byte) {
	var ata0s = TДополнительноТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	разделДиска := TmsdosразделДискаТаблица{}
	разделДиска.ЧитатьразделДиска(&ata0s)

	bios := TПараметры_файловой_системы32{}
	bios.Читать(&ata0s, разделДиска.Mbr.PrimaryразделДиска[0], имяфайла, данные)
	ata0s.Flush()
}

func getcr3() uint32
