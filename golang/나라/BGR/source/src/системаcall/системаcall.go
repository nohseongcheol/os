/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package системаcall

import . "unsafe"

import . "прекъсване"
import . "console"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "файлСистема/msdospartition"
import . "файлСистема/fat"
import . "файлСистема/elf"
import mem "паметmanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtualПамет"

var console_2 = TConsole{}

type TSyscall struct {
	TПрекъсванеhandler
}

const (
	SysИзход	uint32	= 1
	Sysfork		uint32	= 2
	SysЧетене	uint32	= 3
	SysПисане	uint32	= 4
	SysОтваряне	uint32	= 5
	SysЗатваряне	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysдостъп	uint32	= 33
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
	SysrtИзход	uint32	= 252

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
	stdinУкФ		int32	= 0
	stdoutУкФ		int32	= 1
	stderrУкФ		int32	= 2
	максУкФ				= 32
	максОтварянеФайлове		= 128
)

type укФзапис struct {
	използвано	bool
	описание	int32
	укФФлагове	uint32
}

type отварянеФайлОписание struct {
	използвано	bool
	refs		uint32
	kind		uint32
	флагове		uint32
	позиция		uint32
	размер		uint32
	име		[12]byte
	имеlen		uint32
	aux		uint32
}

const (
	укФkindНяма		uint32	= 0
	укФkindfat		uint32	= 1
	укФkindstdin		uint32	= 2
	укФkindconsole		uint32	= 3
	укФkindКоренпапка	uint32	= 4
	укФkindsocket		uint32	= 5

	oЧетенеonly		uint32	= 0
	oПисанеonly		uint32	= 1
	oЧетенеПисане		uint32	= 2
	ocreate			uint32	= 0x40
	oОтрязваненастройността	uint32	= 0x200
	oappend			uint32	= 0x400
	oпапка			uint32	= 0x10000

	seekЗадай	uint32	= 0
	seekТекущадата	uint32	= 1
	seekКрай	uint32	= 2

	fdupУкФ		uint32	= 0
	fgetУкФ		uint32	= 1
	fЗадайУкФ	uint32	= 2
	fgetfl		uint32	= 3
	fЗадайfl	uint32	= 4
	укФcloexec	uint32	= 1

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
	максsockets		= 32
	максsocketпакети	= 8
	максdatagramРазмер	= 512
)

type socketaddressiТСт4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type socketpacket struct {
	използвано	bool
	размер		uint32
	източник	socketaddressiТСт4
	data		[максdatagramРазмер]byte
}

type локалноdatagramsocket struct {
	използвано	bool
	bound		bool
	connected	bool
	локално		socketaddressiТСт4
	отдалечен	socketaddressiТСт4
	head		uint32
	tail		uint32
	count		uint32
	пакети		[максsocketпакети]socketpacket
}

type posixstat struct {
	Устройство	uint32
	Ino		uint32
	РЕЖИМ		uint32
	Nlink		uint32
	ЮИД		uint32
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
	максИзпълнениеvectorзапис	= 16
	максИзпълнениеНиздължина	= 63
)

type изпълнениеvector struct {
	count		uint32
	lengths		[максИзпълнениеvectorзапис]uint32
	стойности	[максИзпълнениеvectorзапис][максИзпълнениеНиздължина + 1]byte
}

type процесзапис struct {
	използвано	bool
	идПр		uint32
	родител		uint32
	exited		bool
	състояние	uint32
	програмаbreak	uint32
	fds		[максУкФ]укФзапис
}

type низheader struct {
	Data	uintptr
	Len	int
}

func syscallГрешка(грешка int32) uint32 {
	return *(*uint32)(Pointer(&грешка))
}

var отварянеФайлТаблица [максОтварянеФайлове]отварянеФайлОписание
var процесТаблица [32]процесзапис
var локалноsockets [максsockets]локалноdatagramsocket
var следващоephemeralПорт uint16 = 49152

const (
	собственикheapbase		uint32	= 0x06000000
	собственикheapОграничение	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinЧетене uint32
var stdinПисане uint32

func Прекъсване(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysИзход_2(съдържание uint32) {
	Syscall(SysИзход, съдържание)
}

func SysЧетене_2(укФ uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(SysЧетене, укФ, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysПечатstr(buffer string) {
	h := (*низheader)(Pointer(&buffer))
	Syscall(SysПисане, uint32(stdoutУкФ), uint32(h.Data), uint32(h.Len))
}

func SysПечатunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysПисане, uint32(stdoutУкФ), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysОтваряне_2(пЪТ uintptr, флагове uint32, рЕЖИМ uint32) int32 {
	return int32(Syscall(SysОтваряне, uint32(пЪТ), флагове, рЕЖИМ))
}

func SysЗатваряне_2(укФ uint32) int32 {
	return int32(Syscall(SysЗатваряне, укФ))
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
		return Прекъсване(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Прекъсване(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Прекъсване(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Прекъсване(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Прекъсване(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Прекъсване(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallГрешка(Enosys)
	}
}

func (себеси *TSyscall) Init(manager *TПрекъсванеmanager) {
	initФайлdescriptor()

	прекъсванеhandler = ръкохваткаПрекъсване

	var address uintptr
	address = uintptr(Pointer(&прекъсванеhandler))

	себеси.TПрекъсванеhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var прекъсванеhandler func(uint32) uint32

func ръкохваткаПрекъсване(esp uint32) uint32 {
	var процесор = (*TcpuСъстояние)(Pointer(uintptr(esp)))

	switch процесор.Eax {
	case SysИзход:
		sysИзход(процесор.Ebx)
		return uint32(uintptr(Pointer(СпиранеТекущадатаthread(процесор))))
	case SysrtИзход:
		sysИзход(процесор.Ebx)
		return uint32(uintptr(Pointer(СпиранеТекущадатаthread(процесор))))
	case Sysfork:
		процесор.Eax = uint32(sysfork(процесор))
		return esp
	case SysЧетене:
		процесор.Eax = uint32(sysЧетене(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysПисане:
		процесор.Eax = uint32(sysПисане(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysОтваряне:
		процесор.Eax = uint32(sysОтваряне(процесор.Ebx, процесор.Ecx, процесор.Edx))
		return esp
	case Syscreat:
		процесор.Eax = uint32(sysОтваряне(процесор.Ebx, ocreate|oПисанеonly|oОтрязваненастройността, процесор.Ecx))
		return esp
	case SysЗатваряне:
		процесор.Eax = uint32(sysЗатваряне(int32(процесор.Ebx)))
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
		процесор.Eax = ТекущадатаИдПр()
		return esp
	case Sysgetppid:
		процесор.Eax = ТекущадатародителИдПр()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		процесор.Eax = 0
		return esp
	case Sysдостъп:
		процесор.Eax = uint32(sysдостъп(процесор.Ebx, процесор.Ecx))
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
		процесор.Eax = uint32(syssocketcall(процесор.Ebx, процесор.Ecx))
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
		console_2.MUnsignedinteger32Печат(процесор.Ebx)
		return esp

	default:
		console_2.MПечатxy(([]byte)("sys["), 1, 23)
		console_2.MUnsignedinteger32Печат(esp)
		console_2.MПечат(([]byte)(":"))
		console_2.MUnsignedinteger32Печат(процесор.Eax)
		console_2.MПечат(([]byte)(":"))
		console_2.MUnsignedinteger32Печат(процесор.Ebx)
		console_2.MПечат(([]byte)(":"))
		console_2.MUnsignedinteger32Печат(процесор.Ecx)
		console_2.MПечат(([]byte)(":"))
		console_2.MUnsignedinteger32Печат(процесор.Edx)
		console_2.MПечат(([]byte)("]"))
		процесор.Eax = syscallГрешка(Enosys)
		return esp
	}

	return esp
}

func initФайлdescriptor() {
	for i := 0; i < максОтварянеФайлове; i++ {
		отварянеФайлТаблица[i] = отварянеФайлОписание{}
	}
	for i := 0; i < len(процесТаблица); i++ {
		процесТаблица[i] = процесзапис{}
	}
	for i := 0; i < len(локалноsockets); i++ {
		локалноsockets[i] = локалноdatagramsocket{}
	}
	следващоephemeralПорт = 49152
	отварянеФайлТаблица[0] = отварянеФайлОписание{използвано: true, kind: укФkindstdin, флагове: oЧетенеonly}
	отварянеФайлТаблица[1] = отварянеФайлОписание{използвано: true, kind: укФkindconsole, флагове: oПисанеonly}
	отварянеФайлТаблица[2] = отварянеФайлОписание{използвано: true, kind: укФkindconsole, флагове: oПисанеonly}
}

func търсенеПроцес(идПр uint32) *процесзапис {
	for i := 0; i < len(процесТаблица); i++ {
		if процесТаблица[i].използвано && процесТаблица[i].идПр == идПр {
			return &процесТаблица[i]
		}
	}
	return nil
}

func initializeПроцесfds(процес *процесзапис) {
	for укФ := int32(0); укФ <= stderrУкФ; укФ++ {
		процес.fds[укФ] = укФзапис{използвано: true, описание: укФ}
		отварянеФайлТаблица[укФ].refs++
	}
}

func ensureТекущадатаПроцес() *процесзапис {
	идПр := ТекущадатаИдПр()
	if процес := търсенеПроцес(идПр); процес != nil {
		return процес
	}
	for i := 0; i < len(процесТаблица); i++ {
		if !процесТаблица[i].използвано {
			процесТаблица[i] = процесзапис{
				използвано:	true,
				идПр:		идПр,
				родител:	ТекущадатародителИдПр(),
				програмаbreak:	собственикheapbase,
			}
			initializeПроцесfds(&процесТаблица[i])
			return &процесТаблица[i]
		}
	}
	return nil
}

func getОтварянеФайлfor(процес *процесзапис, укФ int32) *отварянеФайлОписание {
	if процес == nil || укФ < 0 || укФ >= максУкФ || !процес.fds[укФ].използвано {
		return nil
	}
	описание := процес.fds[укФ].описание
	if описание < 0 || описание >= максОтварянеФайлове || !отварянеФайлТаблица[описание].използвано {
		return nil
	}
	return &отварянеФайлТаблица[описание]
}

func getОтварянеФайл(укФ int32) *отварянеФайлОписание {
	return getОтварянеФайлfor(ensureТекущадатаПроцес(), укФ)
}

func allocateОтварянеФайл() int32 {
	for i := int32(3); i < максОтварянеФайлове; i++ {
		if !отварянеФайлТаблица[i].използвано {
			отварянеФайлТаблица[i] = отварянеФайлОписание{използвано: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateУкФ(процес *процесзапис, описание int32, минимум int32) int32 {
	if процес == nil {
		return Enfile
	}
	if минимум < 0 || минимум >= максУкФ {
		return Einval
	}
	for укФ := минимум; укФ < максУкФ; укФ++ {
		if !процес.fds[укФ].използвано {
			процес.fds[укФ] = укФзапис{използвано: true, описание: описание}
			return укФ
		}
	}
	return Emfile
}

func releaseОтварянеФайл(описание int32) {
	if описание < 0 || описание >= максОтварянеФайлове {
		return
	}
	запис := &отварянеФайлТаблица[описание]
	if запис.refs > 0 {
		запис.refs--
	}

	if запис.refs == 0 && описание > stderrУкФ {
		if запис.kind == укФkindsocket && запис.aux < максsockets {
			локалноsockets[запис.aux] = локалноdatagramsocket{}
		}
		*запис = отварянеФайлОписание{}
	}
}

func затварянеПроцесУкФ(процес *процесзапис, укФ int32) int32 {
	if процес == nil || getОтварянеФайлfor(процес, укФ) == nil {
		return Ebadf
	}
	описание := процес.fds[укФ].описание
	процес.fds[укФ] = укФзапис{}
	releaseОтварянеФайл(описание)
	return 0
}

func sysПисане(укФ int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	запис := getОтварянеФайл(укФ)
	if запис == nil {
		return Ebadf
	}
	if запис.kind != укФkindconsole {
		if запис.kind == укФkindsocket {
			return socketИзпращанеto(укФ, address, count, 0, 0)
		}
		if запис.kind == укФkindfat || запис.kind == укФkindКоренпапка {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБайтовеfromПоказалци(uintptr(address), int(count), int(count))
	console_2.MПечат(buffer)
	return int32(count)
}

func sysЧетене(укФ int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	запис := getОтварянеФайл(укФ)
	if запис == nil {
		return Ebadf
	}
	if запис.kind == укФkindstdin {
		return четенеstdin(address, count)
	}
	if запис.kind == укФkindКоренпапка {
		return Eisdir
	}
	if запис.kind == укФkindsocket {
		return socketreceivefrom(укФ, address, count, 0, 0)
	}
	if запис.kind != укФkindfat {
		return Ebadf
	}
	if запис.позиция >= запис.размер {
		return 0
	}
	remaining := запис.размер - запис.позиция
	if count > remaining {
		count = remaining
	}
	buffer := GetБайтовеfromПоказалци(uintptr(address), int(count), int(count))
	return четенеvfsФайл(запис, buffer, count)
}

func sysОтваряне(пЪТaddress uint32, флагове uint32, рЕЖИМ uint32) int32 {
	_ = рЕЖИМ
	if пЪТaddress == 0 {
		return Efault
	}
	достъпРЕЖИМ := флагове & 3
	if достъпРЕЖИМ == oПисанеonly || достъпРЕЖИМ == oЧетенеПисане || (флагове&(ocreate|oОтрязваненастройността|oappend)) != 0 {
		return Erofs
	}

	процес := ensureТекущадатаПроцес()
	if процес == nil {
		return Enfile
	}
	описание := allocateОтварянеФайл()
	if описание < 0 {
		return описание
	}
	запис := &отварянеФайлТаблица[описание]
	запис.флагове = флагове
	if isКоренПЪТ(пЪТaddress) {
		запис.kind = укФkindКоренпапка
		запис.размер = 0
	} else {
		имеlen, име := копиранеПЪТ(пЪТaddress)
		if имеlen == 0 {
			*запис = отварянеФайлОписание{}
			return Enoent
		}
		размер := файлРазмер(име[:имеlen])
		if размер == 0 {
			*запис = отварянеФайлОписание{}
			return Enoent
		}
		if (флагове & oпапка) != 0 {
			*запис = отварянеФайлОписание{}
			return Enotdir
		}
		запис.kind = укФkindfat
		запис.размер = размер
		запис.имеlen = имеlen
		запис.име = име
	}

	укФ := allocateУкФ(процес, описание, 3)
	if укФ < 0 {
		*запис = отварянеФайлОписание{}
		return укФ
	}
	return укФ
}

func sysЗатваряне(укФ int32) int32 {
	return затварянеПроцесУкФ(ensureТекущадатаПроцес(), укФ)
}

func sysdup(укФ int32, минимум int32) int32 {
	процес := ensureТекущадатаПроцес()
	запис := getОтварянеФайлfor(процес, укФ)
	if запис == nil {
		return Ebadf
	}
	новУкФ := allocateУкФ(процес, процес.fds[укФ].описание, минимум)
	if новУкФ >= 0 {
		запис.refs++
	}
	return новУкФ
}

func sysdup2(oldУкФ int32, новУкФ int32) int32 {
	процес := ensureТекущадатаПроцес()
	запис := getОтварянеФайлfor(процес, oldУкФ)
	if запис == nil {
		return Ebadf
	}
	if новУкФ < 0 || новУкФ >= максУкФ {
		return Ebadf
	}
	if oldУкФ == новУкФ {
		return новУкФ
	}
	if процес.fds[новУкФ].използвано {
		затварянеПроцесУкФ(процес, новУкФ)
	}
	процес.fds[новУкФ] = укФзапис{използвано: true, описание: процес.fds[oldУкФ].описание}
	запис.refs++
	return новУкФ
}

func sysfcntl(укФ int32, команда uint32, argument uint32) int32 {
	процес := ensureТекущадатаПроцес()
	запис := getОтварянеФайлfor(процес, укФ)
	if запис == nil {
		return Ebadf
	}
	switch команда {
	case fdupУкФ:
		return sysdup(укФ, int32(argument))
	case fgetУкФ:
		return int32(процес.fds[укФ].укФФлагове)
	case fЗадайУкФ:
		процес.fds[укФ].укФФлагове = argument & укФcloexec
		return 0
	case fgetfl:
		return int32(запис.флагове)
	case fЗадайfl:
		запис.флагове = (запис.флагове & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(укФ int32, offset int32, whence uint32) int32 {
	запис := getОтварянеФайл(укФ)
	if запис == nil {
		return Ebadf
	}
	if запис.kind != укФkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekЗадай:
		base = 0
	case seekТекущадата:
		base = int64(запис.позиция)
	case seekКрай:
		base = int64(запис.размер)
	default:
		return Einval
	}
	позиция_2 := base + int64(offset)
	if позиция_2 < 0 || позиция_2 > 0x7FFFFFFF {
		return Einval
	}
	запис.позиция = uint32(позиция_2)
	return int32(запис.позиция)
}

func четенеvfsФайл(запис *отварянеФайлОписание, назначение_2 []byte, count uint32) int32 {
	паметmanager := &mem.TПаметmanager{}
	tmpПоказалци := паметmanager.Malloc(запис.размер)
	if tmpПоказалци == nil {
		return Einval
	}
	tmp := GetБайтовеfromПоказалци(uintptr(tmpПоказалци), int(запис.размер), int(запис.размер))
	четенеФайл(запис.име[:запис.имеlen], tmp)
	copy(назначение_2[:count], tmp[запис.позиция:запис.позиция+count])
	запис.позиция += count
	паметmanager.Свободно(tmpПоказалци)
	return int32(count)
}

func isКоренПЪТ(пЪТaddress uint32) bool {
	if пЪТaddress == 0 {
		return false
	}
	пЪТ := GetБайтовеfromПоказалци(uintptr(пЪТaddress), 4, 4)
	if пЪТ[0] == '/' && пЪТ[1] == 0 {
		return true
	}
	if пЪТ[0] == '.' && пЪТ[1] == 0 {
		return true
	}
	if пЪТ[0] == '/' && пЪТ[1] == '.' && пЪТ[2] == 0 {
		return true
	}
	return false
}

func sysдостъп(пЪТaddress uint32, рЕЖИМ uint32) int32 {
	if пЪТaddress == 0 {
		return Efault
	}
	if (рЕЖИМ & ^uint32(7)) != 0 {
		return Einval
	}
	isКорен := isКоренПЪТ(пЪТaddress)
	exists := isКорен
	if !exists {
		имеlen, име := копиранеПЪТ(пЪТaddress)
		exists = имеlen != 0 && файлРазмер(име[:имеlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (рЕЖИМ & 2) != 0 {
		return Eacces
	}

	if (рЕЖИМ&1) != 0 && !isКорен {
		return Eacces
	}
	return 0
}

func syschdir(пЪТaddress uint32) int32 {
	if пЪТaddress == 0 {
		return Efault
	}
	if !isКоренПЪТ(пЪТaddress) {
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
	buffer_2 := GetБайтовеfromПоказалци(uintptr(bufferaddress), int(размер), int(размер))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, рЕЖИМ uint32, размер uint32, iвъзел uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Устройство = 1
	stat.Ino = iвъзел
	stat.РЕЖИМ = рЕЖИМ
	stat.Nlink = 1
	stat.Размер_2 = int32(размер)
	stat.Blksize = 512
	stat.Блок = int32((размер + 511) / 512)
	return 0
}

func sysstat(пЪТaddress uint32, stataddress uint32) int32 {
	if пЪТaddress == 0 {
		return Efault
	}
	if isКоренПЪТ(пЪТaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	имеlen, име := копиранеПЪТ(пЪТaddress)
	if имеlen == 0 {
		return Enoent
	}
	размер := файлРазмер(име[:имеlen])
	if размер == 0 {
		return Enoent
	}
	iвъзел := uint32(2)
	for i := uint32(0); i < имеlen; i++ {
		iвъзел = iвъзел*33 + uint32(име[i])
	}
	return fillposixstat(stataddress, sifreg|0444, размер, iвъзел)
}

func sysfstat(укФ int32, stataddress uint32) int32 {
	запис := getОтварянеФайл(укФ)
	if запис == nil {
		return Ebadf
	}
	switch запис.kind {
	case укФkindstdin, укФkindconsole:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(укФ+1))
	case укФkindКоренпапка:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case укФkindfat:
		return fillposixstat(stataddress, sifreg|0444, запис.размер, uint32(укФ+2))
	case укФkindsocket:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(укФ+2))
	}
	return Ebadf
}

func sysfsync(укФ int32) int32 {
	if getОтварянеФайл(укФ) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	процес := ensureТекущадатаПроцес()
	if процес == nil {
		return 0
	}
	if процес.програмаbreak == 0 {
		процес.програмаbreak = собственикheapbase
	}
	if address_2 == 0 {
		return процес.програмаbreak
	}
	if address_2 < собственикheapbase || address_2 > собственикheapОграничение {
		return процес.програмаbreak
	}
	процес.програмаbreak = address_2
	return процес.програмаbreak
}

func копиранеutsполе(назначение *[65]byte, стойност string) {
	ограничение := len(стойност)
	if ограничение > 64 {
		ограничение = 64
	}
	for i := 0; i < ограничение; i++ {
		назначение[i] = стойност[i]
	}
	назначение[ограничение] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	име := (*posixutsname)(Pointer(uintptr(address_2)))
	*име = posixutsname{}
	копиранеutsполе(&име.Sysname, "EngOS")
	копиранеutsполе(&име.Nodename, "engos")
	копиранеutsполе(&име.Release, "0.1-posix")
	копиранеutsполе(&име.Версия, "POSIX.1-2017 phase 1")
	копиранеutsполе(&име.Machine, "i386")
	return 0
}

func странициранеunsignedinteger16(стойност uint16) uint16 {
	return (стойност << 8) | (стойност >> 8)
}

func socketcallargument(параметри_2 uint32, съдържание uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(параметри_2 + съдържание*4)))
}

func socketforУкФ(укФ int32) (*локалноdatagramsocket, int32) {
	запис := getОтварянеФайл(укФ)
	if запис == nil || запис.kind != укФkindsocket || запис.aux >= максsockets {
		return nil, Ebadf
	}
	socket := &локалноsockets[запис.aux]
	if !socket.използвано {
		return nil, Ebadf
	}
	return socket, 0
}

func allocatesocket(сайт uint32, socketТип uint32, protocol uint32) int32 {
	if сайт != afinet {
		return Eafnosupport
	}
	if socketТип != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процес := ensureТекущадатаПроцес()
	if процес == nil {
		return Enfile
	}
	socketСъдържание := -1
	for i := 0; i < максsockets; i++ {
		if !локалноsockets[i].използвано {
			socketСъдържание = i
			break
		}
	}
	if socketСъдържание < 0 {
		return Enfile
	}
	описание := allocateОтварянеФайл()
	if описание < 0 {
		return описание
	}
	локалноsockets[socketСъдържание] = локалноdatagramsocket{използвано: true}
	запис := &отварянеФайлТаблица[описание]
	запис.kind = укФkindsocket
	запис.флагове = oЧетенеПисане
	запис.aux = uint32(socketСъдържание)
	укФ := allocateУкФ(процес, описание, 3)
	if укФ < 0 {
		локалноsockets[socketСъдържание] = локалноdatagramsocket{}
		*запис = отварянеФайлОписание{}
		return укФ
	}
	return укФ
}

func socketaddress(address_2 uint32, дължина uint32) (*socketaddressiТСт4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if дължина < 16 {
		return nil, Einval
	}
	рЕЗУЛТАТ := (*socketaddressiТСт4)(Pointer(uintptr(address_2)))
	if рЕЗУЛТАТ.Family != afinet {
		return nil, Eafnosupport
	}
	return рЕЗУЛТАТ, 0
}

func портВходящИзползване(порт uint16, except *локалноdatagramsocket) bool {
	for i := 0; i < максsockets; i++ {
		socket := &локалноsockets[i]
		if socket != except && socket.използвано && socket.bound && socket.локално.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(socket *локалноdatagramsocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := странициранеunsignedinteger16(следващоephemeralПорт)
		следващоephemeralПорт++
		if следващоephemeralПорт < 49152 {
			следващоephemeralПорт = 49152
		}
		if !портВходящИзползване(порт, socket) {
			socket.локално = socketaddressiТСт4{Family: afinet, Порт: порт, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func socketbind(укФ int32, address_2 uint32, дължина uint32) int32 {
	socket, грешка := socketforУкФ(укФ)
	if грешка != 0 {
		return грешка
	}
	requested, грешка := socketaddress(address_2, дължина)
	if грешка != 0 {
		return грешка
	}
	if socket.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return bindephemeral(socket)
	}
	if портВходящИзползване(requested.Порт, socket) {
		return Eaddrinuse
	}
	socket.локално = *requested
	socket.bound = true
	return 0
}

func socketСвързване(укФ int32, address_2 uint32, дължина uint32) int32 {
	socket, грешка := socketforУкФ(укФ)
	if грешка != 0 {
		return грешка
	}
	отдалечен, грешка := socketaddress(address_2, дължина)
	if грешка != 0 {
		return грешка
	}
	if !socket.bound {
		if грешка := bindephemeral(socket); грешка != 0 {
			return грешка
		}
	}
	socket.отдалечен = *отдалечен
	socket.connected = true
	return 0
}

func socketИзпращанеto(укФ int32, bufferaddress_2 uint32, дължина uint32, назначениеaddress uint32, назначениедължина uint32) int32 {
	socket, грешка := socketforУкФ(укФ)
	if грешка != 0 {
		return грешка
	}
	if дължина > максdatagramРазмер {
		return Emsgsize
	}
	if дължина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var назначение socketaddressiТСт4
	if назначениеaddress != 0 {
		address_2, addressГрешка := socketaddress(назначениеaddress, назначениедължина)
		if addressГрешка != 0 {
			return addressГрешка
		}
		назначение = *address_2
	} else {
		if !socket.connected {
			return Enotconn
		}
		назначение = socket.отдалечен
	}
	if !socket.bound {
		if bindГрешка := bindephemeral(socket); bindГрешка != 0 {
			return bindГрешка
		}
	}
	var receiver *локалноdatagramsocket
	for i := 0; i < максsockets; i++ {
		candidate := &локалноsockets[i]
		if candidate.използвано && candidate.bound && candidate.локално.Порт == назначение.Порт &&
			(candidate.локално.Address == 0 || candidate.локално.Address == назначение.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= максsocketпакети {
		return Eagain
	}
	packet := &receiver.пакети[receiver.tail]
	*packet = socketpacket{използвано: true, размер: дължина, източник: socket.локално}
	if дължина != 0 {
		източник := GetБайтовеfromПоказалци(uintptr(bufferaddress_2), int(дължина), int(дължина))
		copy(packet.data[:дължина], източник)
	}
	receiver.tail = (receiver.tail + 1) % максsocketпакети
	receiver.count++
	return int32(дължина)
}

func socketreceivefrom(укФ int32, bufferaddress_2 uint32, дължина uint32, източникaddress uint32, източникдължинаaddress uint32) int32 {
	socket, грешка := socketforУкФ(укФ)
	if грешка != 0 {
		return грешка
	}
	if дължина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if socket.count == 0 {
		return Eagain
	}
	packet := &socket.пакети[socket.head]
	копиранедължина := packet.размер
	if копиранедължина > дължина {
		копиранедължина = дължина
	}
	if копиранедължина != 0 {
		назначение := GetБайтовеfromПоказалци(uintptr(bufferaddress_2), int(копиранедължина), int(копиранедължина))
		copy(назначение, packet.data[:копиранедължина])
	}
	if източникaddress != 0 {
		if източникдължинаaddress == 0 {
			return Efault
		}
		providedдължина := (*uint32)(Pointer(uintptr(източникдължинаaddress)))
		if *providedдължина >= 16 {
			*(*socketaddressiТСт4)(Pointer(uintptr(източникaddress))) = packet.източник
		}
		*providedдължина = 16
	}
	*packet = socketpacket{}
	socket.head = (socket.head + 1) % максsocketпакети
	socket.count--
	return int32(копиранедължина)
}

func копиранеsocketИме(укФ int32, address_2 uint32, дължинаaddress uint32, peer bool) int32 {
	socket, грешка := socketforУкФ(укФ)
	if грешка != 0 {
		return грешка
	}
	if address_2 == 0 || дължинаaddress == 0 {
		return Efault
	}
	дължина := (*uint32)(Pointer(uintptr(дължинаaddress)))
	if *дължина < 16 {
		*дължина = 16
		return Einval
	}
	if peer {
		if !socket.connected {
			return Enotconn
		}
		*(*socketaddressiТСт4)(Pointer(uintptr(address_2))) = socket.отдалечен
	} else {
		if !socket.bound {
			if bindГрешка := bindephemeral(socket); bindГрешка != 0 {
				return bindГрешка
			}
		}
		*(*socketaddressiТСт4)(Pointer(uintptr(address_2))) = socket.локално
	}
	*дължина = 16
	return 0
}

func syssocketcall(call uint32, параметри_2 uint32) int32 {
	if параметри_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatesocket(socketcallargument(параметри_2, 0), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2))
	case 2:
		return socketbind(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2))
	case 3:
		return socketСвързване(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return копиранеsocketИме(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), false)
	case 7:
		return копиранеsocketИме(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), true)
	case 9:
		return socketИзпращанеto(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), 0, 0)
	case 10:
		return socketreceivefrom(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), 0, 0)
	case 11:
		return socketИзпращанеto(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), socketcallargument(параметри_2, 4), socketcallargument(параметри_2, 5))
	case 12:
		return socketreceivefrom(int32(socketcallargument(параметри_2, 0)), socketcallargument(параметри_2, 1), socketcallargument(параметри_2, 2), socketcallargument(параметри_2, 4), socketcallargument(параметри_2, 5))
	case 13:
		if _, грешка := socketforУкФ(int32(socketcallargument(параметри_2, 0))); грешка != 0 {
			return грешка
		}
		return 0
	case 14:
		if _, грешка := socketforУкФ(int32(socketcallargument(параметри_2, 0))); грешка != 0 {
			return грешка
		}
		return 0
	}
	return Eopnotsupp
}

func четенеstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБайтовеfromПоказалци(uintptr(address), int(count), int(count))
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
	следващо := (stdinПисане + 1) % uint32(len(stdinbuffer))
	if следващо == stdinЧетене {
		return
	}
	stdinbuffer[stdinПисане] = c
	stdinПисане = следващо
}

func stdingetblocking() byte {
	for stdinЧетене == stdinПисане {
		sc := pollКлавиатураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinЧетене]
	stdinЧетене = (stdinЧетене + 1) % uint32(len(stdinbuffer))
	return c
}

func pollКлавиатураscancode() byte {
	for (ПортЧетенеbyte(0x64) & 0x01) == 0 {
	}
	sc := ПортЧетенеbyte(0x60)
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

func копиранеИзпълнениеvector(address_2 uint32, рЕЗУЛТАТ *изпълнениеvector) int32 {
	*рЕЗУЛТАТ = изпълнениеvector{}
	if address_2 == 0 {
		return 0
	}
	for съдържание := uint32(0); съдържание < максИзпълнениеvectorзапис; съдържание++ {
		низaddress := *(*uint32)(Pointer(uintptr(address_2 + съдържание*4)))
		if низaddress == 0 {
			рЕЗУЛТАТ.count = съдържание
			return 0
		}
		terminated := false
		for дължина := uint32(0); дължина <= максИзпълнениеНиздължина; дължина++ {
			стойност := *(*byte)(Pointer(uintptr(низaddress + дължина)))
			рЕЗУЛТАТ.стойности[съдържание][дължина] = стойност
			if стойност == 0 {
				рЕЗУЛТАТ.lengths[съдържание] = дължина
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

func pushИзпълнениеunsignedinteger32(stack *uint32, стойност uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = стойност
}

func setupИзпълнениеstack(процесор *TcpuСъстояние, параметри_2 *изпълнениеvector, environment *изпълнениеvector) int32 {
	const stackБайтове uint32 = 4096
	if !MakeДиапазонЧастноwritable(getcr3(), СобственикstackГоре-stackБайтове, stackБайтове) {
		return Enomem
	}
	stack := СобственикstackГоре
	var argumentpointers [максИзпълнениеvectorзапис]uint32
	var environmentpointers [максИзпълнениеvectorзапис]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		дължина := environment.lengths[i] + 1
		stack -= дължина
		назначение := GetБайтовеfromПоказалци(uintptr(stack), int(дължина), int(дължина))
		copy(назначение, environment.стойности[i][:дължина])
		environmentpointers[i] = stack
	}
	for i := int(параметри_2.count) - 1; i >= 0; i-- {
		дължина := параметри_2.lengths[i] + 1
		stack -= дължина
		назначение := GetБайтовеfromПоказалци(uintptr(stack), int(дължина), int(дължина))
		copy(назначение, параметри_2.стойности[i][:дължина])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushИзпълнениеunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushИзпълнениеunsignedinteger32(&stack, environmentpointers[i])
	}
	pushИзпълнениеunsignedinteger32(&stack, 0)
	for i := int(параметри_2.count) - 1; i >= 0; i-- {
		pushИзпълнениеunsignedinteger32(&stack, argumentpointers[i])
	}
	pushИзпълнениеunsignedinteger32(&stack, параметри_2.count)
	процесор.Esp = stack
	процесор.Ebp = 0
	return 0
}

func затварянеВклИзпълнение(процес *процесзапис) {
	if процес == nil {
		return
	}
	for укФ := int32(0); укФ < максУкФ; укФ++ {
		if процес.fds[укФ].използвано && (процес.fds[укФ].укФФлагове&укФcloexec) != 0 {
			затварянеПроцесУкФ(процес, укФ)
		}
	}
}

func sysexecve(процесор *TcpuСъстояние, пЪТaddress uint32) int32 {
	if пЪТaddress == 0 {
		return Efault
	}
	var параметри_2 изпълнениеvector
	var environment изпълнениеvector
	if рЕЗУЛТАТ := копиранеИзпълнениеvector(процесор.Ecx, &параметри_2); рЕЗУЛТАТ < 0 {
		return рЕЗУЛТАТ
	}
	if рЕЗУЛТАТ := копиранеИзпълнениеvector(процесор.Edx, &environment); рЕЗУЛТАТ < 0 {
		return рЕЗУЛТАТ
	}
	имеlen, име := копиранеПЪТ(пЪТaddress)
	if имеlen == 0 {
		return Enoent
	}
	размер := файлРазмер(име[:имеlen])
	if размер == 0 {
		return Enoent
	}
	паметmanager := &mem.TПаметmanager{}
	файлПоказалци := паметmanager.Malloc(размер)
	if файлПоказалци == nil {
		return Einval
	}
	data := GetБайтовеfromПоказалци(uintptr(файлПоказалци), int(размер), int(размер))
	четенеФайл(име[:имеlen], data)
	if размер < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		паметmanager.Свободно(файлПоказалци)
		return Enoexec
	}
	loader := Elf{}
	запис := loader.Getзапис(data)
	loader.Parse(data, getcr3())
	паметmanager.Свободно(файлПоказалци)
	if рЕЗУЛТАТ := setupИзпълнениеstack(процесор, &параметри_2, &environment); рЕЗУЛТАТ < 0 {
		return рЕЗУЛТАТ
	}
	затварянеВклИзпълнение(ensureТекущадатаПроцес())
	процесор.Eip = запис
	процесор.Eax = 0
	return 0
}

func sysfork(процесор *TcpuСъстояние) int32 {
	родителИдПр := ТекущадатаИдПр()
	if ensureТекущадатаПроцес() == nil {
		return Enfile
	}
	идПр := allocateПроцес(родителИдПр)
	if идПр == 0 {
		return Einval
	}
	паметmanager := &mem.TПаметmanager{}
	threadПоказалци := паметmanager.Malloc(uint32(Sizeof(TThread{})))
	stackПоказалци := паметmanager.Malloc(ThreadstackРазмер)
	детеСтраницапапка := CloneaddressИнтервалcow(getcr3())
	if threadПоказалци == nil || stackПоказалци == nil || детеСтраницапапка == 0 {
		discardПроцес(идПр)
		return Einval
	}
	дете := (*TThread)(threadПоказалци)
	дете.Stack = uint32(uintptr(stackПоказалци))
	дете.ПроцесорСъстояние = (*TcpuСъстояние)(Pointer(uintptr(stackПоказалци) + ThreadstackРазмер - Sizeof(TcpuСъстояние{})))
	*дете.ПроцесорСъстояние = *процесор
	дете.ПроцесорСъстояние.Eax = 0
	дете.Собственикstack_2 = процесор.Esp
	дете.СобственикstackРазмер_2 = 0
	дете.ИдПр = идПр
	дете.РодителИдПр = родителИдПр
	дете.Страницапапказапис = детеСтраницапапка
	дете.ThreadСъстояние = Готово
	дете.Fpuoffset = 0xffffffff
	дете.Iskernel = false
	Добавянеrunnablethread(дете)
	return int32(идПр)
}

func sysИзход(състояние uint32) {
	идПр := ТекущадатаИдПр()
	for i := 0; i < len(процесТаблица); i++ {
		if процесТаблица[i].използвано && процесТаблица[i].идПр == идПр {
			затварянеВсичкиПроцесfds(&процесТаблица[i])
			процесТаблица[i].exited = true
			процесТаблица[i].състояние = (състояние & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(идПр int32, състояниеaddress uint32, настройки uint32) int32 {
	if (настройки & ^uint32(1)) != 0 {
		return Einval
	}
	родителИдПр := ТекущадатаИдПр()
	foundдете := false
	for i := 0; i < len(процесТаблица); i++ {
		p := &процесТаблица[i]
		matches := идПр == -1 || идПр == 0 || p.идПр == uint32(идПр)
		if p.използвано && matches && p.родител == родителИдПр {
			foundдете = true
			if p.exited {
				if състояниеaddress != 0 {
					*(*uint32)(Pointer(uintptr(състояниеaddress))) = p.състояние
				}
				детеИдПр := p.идПр
				*p = процесзапис{}
				return int32(детеИдПр)
			}
		}
	}
	if !foundдете {
		return Echild
	}

	if (настройки & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцес(родител uint32) uint32 {
	родителПроцес := търсенеПроцес(родител)
	идПр := AllocateИдПр()
	for i := 0; i < len(процесТаблица); i++ {
		if !процесТаблица[i].използвано {
			процесТаблица[i] = процесзапис{
				използвано:	true,
				идПр:		идПр,
				родител:	родител,
				програмаbreak:	собственикheapbase,
			}
			if родителПроцес != nil {
				процесТаблица[i].програмаbreak = родителПроцес.програмаbreak
				for укФ := 0; укФ < максУкФ; укФ++ {
					if родителПроцес.fds[укФ].използвано {
						процесТаблица[i].fds[укФ] = родителПроцес.fds[укФ]
						описание := родителПроцес.fds[укФ].описание
						if описание >= 0 && описание < максОтварянеФайлове {
							отварянеФайлТаблица[описание].refs++
						}
					}
				}
			} else {
				initializeПроцесfds(&процесТаблица[i])
			}
			return идПр
		}
	}
	return 0
}

func затварянеВсичкиПроцесfds(процес *процесзапис) {
	if процес == nil {
		return
	}
	for укФ := int32(0); укФ < максУкФ; укФ++ {
		if процес.fds[укФ].използвано {
			затварянеПроцесУкФ(процес, укФ)
		}
	}
}

func discardПроцес(идПр uint32) {
	процес := търсенеПроцес(идПр)
	if процес == nil {
		return
	}
	затварянеВсичкиПроцесfds(процес)
	*процес = процесзапис{}
}

func копиранеПЪТ(пЪТaddress uint32) (uint32, [12]byte) {
	var име [12]byte
	if пЪТaddress == 0 {
		return 0, име
	}
	raw := GetБайтовеfromПоказалци(uintptr(пЪТaddress), 64, 64)
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
		име[n] = c
		n++
	}
	return n, име
}

func файлРазмер(именафайл []byte) uint32 {
	var ata0s = TДопълнителниТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТаблица{}
	partition.Четенеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	размер := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], именафайл)
	ata0s.Flush()
	return размер
}

func четенеФайл(именафайл []byte, data []byte) {
	var ata0s = TДопълнителниТехнологияattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТаблица{}
	partition.Четенеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Четене(&ata0s, partition.Mbr.Primarypartition[0], именафайл, data)
	ata0s.Flush()
}

func getcr3() uint32
