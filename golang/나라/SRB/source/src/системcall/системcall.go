/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package системcall

import . "unsafe"

import . "ометање"
import . "конзола"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "датотекаСистем/msdospartition"
import . "датотекаСистем/fat"
import . "датотекаСистем/elf"
import mem "меморијаmanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "виртуелноМеморија"

var конзола_2 = TКонзола{}

type TSyscall struct {
	TОметањеhandler
}

const (
	SysИзлаз	uint32	= 1
	Sysfork		uint32	= 2
	Sysчитање	uint32	= 3
	SysПише		uint32	= 4
	SysОтвори	uint32	= 5
	SysЗатвори	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysприступање	uint32	= 33
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
	SysrtИзлаз	uint32	= 252

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
	stdinОписник		int32	= 0
	stdoutОписник		int32	= 1
	stderrОписник		int32	= 2
	максОписник			= 32
	максОтвориДАТОТЕКЕ		= 128
)

type описникунос struct {
	заузето_2		bool
	опис			int32
	описникПараметри	uint32
}

type отвориДатотекаОпис struct {
	заузето_2	bool
	refs		uint32
	врста		uint32
	параметри	uint32
	положај		uint32
	величина	uint32
	назив		[12]byte
	називlen	uint32
	aux		uint32
}

const (
	описникврстаНишта		uint32	= 0
	описникврстаfat			uint32	= 1
	описникврстаstdin		uint32	= 2
	описникврстаКонзола		uint32	= 3
	описникврстаКоренДиректоријум	uint32	= 4
	описникврстаПрикључница		uint32	= 5

	oчитањеonly	uint32	= 0
	oПишеonly	uint32	= 1
	oчитањеПише	uint32	= 2
	ocreate		uint32	= 0x40
	oОдсеците	uint32	= 0x200
	oappend		uint32	= 0x400
	oДиректоријум	uint32	= 0x10000

	seekскуп	uint32	= 0
	seekТренутно	uint32	= 1
	seekKraj	uint32	= 2

	fdupОписник	uint32	= 0
	fgetОписник	uint32	= 1
	fскупОписник	uint32	= 2
	fgetfl		uint32	= 3
	fскупfl		uint32	= 4
	описникcloexec	uint32	= 1

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
	максПрикључницапакета	= 8
	максdatagramВеличина	= 512
)

type прикључницаaddressiТревр4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type прикључницаpacket struct {
	заузето_2	bool
	величина	uint32
	извор		прикључницаaddressiТревр4
	data		[максdatagramВеличина]byte
}

type локалнаdatagramПрикључница struct {
	заузето_2	bool
	bound		bool
	connected	bool
	локална		прикључницаaddressiТревр4
	удаљено		прикључницаaddressiТревр4
	head		uint32
	tail		uint32
	count		uint32
	пакета		[максПрикључницапакета]прикључницаpacket
}

type posixstat struct {
	Уређај		uint32
	Ino		uint32
	РЕЖИМ		uint32
	Nlink		uint32
	ЈЛБ		uint32
	Gid		uint32
	Rdev		uint32
	Величина_2	int32
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
	Издање		[65]byte
	Machine		[65]byte
}

const (
	максизвршнаvectorунос	= 16
	максизвршнанискаДужина	= 63
)

type извршнаvector struct {
	count		uint32
	lengths		[максизвршнаvectorунос]uint32
	вредности	[максизвршнаvectorунос][максизвршнанискаДужина + 1]byte
}

type процесунос struct {
	заузето_2	bool
	пИД		uint32
	надређени	uint32
	изашаосам	bool
	стање		uint32
	програмbreak	uint32
	fds		[максОписник]описникунос
}

type нискаheader struct {
	Data	uintptr
	Len	int
}

func syscallГрешка(грешка int32) uint32 {
	return *(*uint32)(Pointer(&грешка))
}

var отвориДатотекаТабела [максОтвориДАТОТЕКЕ]отвориДатотекаОпис
var процесТабела [32]процесунос
var локалнаsockets [максsockets]локалнаdatagramПрикључница
var следећеephemeralПорт uint16 = 49152

const (
	корисникheapbase	uint32	= 0x06000000
	корисникheapОграничи	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinчитање uint32
var stdinПише uint32

func Ометање(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysИзлаз_2(попис uint32) {
	Syscall(SysИзлаз, попис)
}

func Sysчитање_2(описник uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysчитање, описник, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysШтампајstr(buffer string) {
	h := (*нискаheader)(Pointer(&buffer))
	Syscall(SysПише, uint32(stdoutОписник), uint32(h.Data), uint32(h.Len))
}

func SysШтампајunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysПише, uint32(stdoutОписник), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysОтвори_2(пУТАЊА uintptr, параметри uint32, рЕЖИМ uint32) int32 {
	return int32(Syscall(SysОтвори, uint32(пУТАЊА), параметри, рЕЖИМ))
}

func SysЗатвори_2(описник uint32) int32 {
	return int32(Syscall(SysЗатвори, описник))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(параметри_2 ...uint32) uint32 {

	l := len(параметри_2)
	switch l {
	case 1:
		return Ометање(параметри_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Ометање(параметри_2[0], параметри_2[1], 0, 0, 0, 0)
	case 3:
		return Ометање(параметри_2[0], параметри_2[1], параметри_2[2], 0, 0, 0)
	case 4:
		return Ометање(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], 0, 0)
	case 5:
		return Ометање(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], параметри_2[4], 0)
	case 6:
		return Ометање(параметри_2[0], параметри_2[1], параметри_2[2], параметри_2[3], параметри_2[4], параметри_2[5])
	default:
		return syscallГрешка(Enosys)
	}
}

func (исти *TSyscall) Init(manager *TОметањеmanager) {
	initДатотекаdescriptor()

	ометањеhandler = ручкаОметање

	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))

	исти.TОметањеhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var ометањеhandler func(uint32) uint32

func ручкаОметање(esp uint32) uint32 {
	var процесор = (*TcpuСтање)(Pointer(uintptr(esp)))

	switch процесор.Eax {
	case SysИзлаз:
		sysИзлаз(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗауставиТренутноthread(процесор))))
	case SysrtИзлаз:
		sysИзлаз(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗауставиТренутноthread(процесор))))
	case Sysfork:
		процесор.Eax = uint32(sysfork(процесор))
		return esp
	case Sysчитање:
		процесор.Eax = uint32(sysчитање(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysПише:
		процесор.Eax = uint32(sysПише(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysОтвори:
		процесор.Eax = uint32(sysОтвори(процесор.Ebx, процесор.Ecx, процесор.Edx))
		return esp
	case Syscreat:
		процесор.Eax = uint32(sysОтвори(процесор.Ebx, ocreate|oПишеonly|oОдсеците, процесор.Ecx))
		return esp
	case SysЗатвори:
		процесор.Eax = uint32(sysЗатвори(int32(процесор.Ebx)))
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
		процесор.Eax = ТренутноПИД()
		return esp
	case Sysgetppid:
		процесор.Eax = ТренутнонадређениПИД()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		процесор.Eax = 0
		return esp
	case Sysприступање:
		процесор.Eax = uint32(sysприступање(процесор.Ebx, процесор.Ecx))
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
		процесор.Eax = uint32(sysПрикључницаcall(процесор.Ebx, процесор.Ecx))
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
		конзола_2.MUnsignedinteger32Штампај(процесор.Ebx)
		return esp

	default:
		конзола_2.MШтампајxy(([]byte)("sys["), 1, 23)
		конзола_2.MUnsignedinteger32Штампај(esp)
		конзола_2.MШтампај(([]byte)(":"))
		конзола_2.MUnsignedinteger32Штампај(процесор.Eax)
		конзола_2.MШтампај(([]byte)(":"))
		конзола_2.MUnsignedinteger32Штампај(процесор.Ebx)
		конзола_2.MШтампај(([]byte)(":"))
		конзола_2.MUnsignedinteger32Штампај(процесор.Ecx)
		конзола_2.MШтампај(([]byte)(":"))
		конзола_2.MUnsignedinteger32Штампај(процесор.Edx)
		конзола_2.MШтампај(([]byte)("]"))
		процесор.Eax = syscallГрешка(Enosys)
		return esp
	}

	return esp
}

func initДатотекаdescriptor() {
	for i := 0; i < максОтвориДАТОТЕКЕ; i++ {
		отвориДатотекаТабела[i] = отвориДатотекаОпис{}
	}
	for i := 0; i < len(процесТабела); i++ {
		процесТабела[i] = процесунос{}
	}
	for i := 0; i < len(локалнаsockets); i++ {
		локалнаsockets[i] = локалнаdatagramПрикључница{}
	}
	следећеephemeralПорт = 49152
	отвориДатотекаТабела[0] = отвориДатотекаОпис{заузето_2: true, врста: описникврстаstdin, параметри: oчитањеonly}
	отвориДатотекаТабела[1] = отвориДатотекаОпис{заузето_2: true, врста: описникврстаКонзола, параметри: oПишеonly}
	отвориДатотекаТабела[2] = отвориДатотекаОпис{заузето_2: true, врста: описникврстаКонзола, параметри: oПишеonly}
}

func нађиПроцес(пИД uint32) *процесунос {
	for i := 0; i < len(процесТабела); i++ {
		if процесТабела[i].заузето_2 && процесТабела[i].пИД == пИД {
			return &процесТабела[i]
		}
	}
	return nil
}

func initializeПроцесfds(процес *процесунос) {
	for описник := int32(0); описник <= stderrОписник; описник++ {
		процес.fds[описник] = описникунос{заузето_2: true, опис: описник}
		отвориДатотекаТабела[описник].refs++
	}
}

func ensureТренутноПроцес() *процесунос {
	пИД := ТренутноПИД()
	if процес := нађиПроцес(пИД); процес != nil {
		return процес
	}
	for i := 0; i < len(процесТабела); i++ {
		if !процесТабела[i].заузето_2 {
			процесТабела[i] = процесунос{
				заузето_2:	true,
				пИД:		пИД,
				надређени:	ТренутнонадређениПИД(),
				програмbreak:	корисникheapbase,
			}
			initializeПроцесfds(&процесТабела[i])
			return &процесТабела[i]
		}
	}
	return nil
}

func getОтвориДатотекаfor(процес *процесунос, описник int32) *отвориДатотекаОпис {
	if процес == nil || описник < 0 || описник >= максОписник || !процес.fds[описник].заузето_2 {
		return nil
	}
	опис := процес.fds[описник].опис
	if опис < 0 || опис >= максОтвориДАТОТЕКЕ || !отвориДатотекаТабела[опис].заузето_2 {
		return nil
	}
	return &отвориДатотекаТабела[опис]
}

func getОтвориДатотека(описник int32) *отвориДатотекаОпис {
	return getОтвориДатотекаfor(ensureТренутноПроцес(), описник)
}

func allocateОтвориДатотека() int32 {
	for i := int32(3); i < максОтвориДАТОТЕКЕ; i++ {
		if !отвориДатотекаТабела[i].заузето_2 {
			отвориДатотекаТабела[i] = отвориДатотекаОпис{заузето_2: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateОписник(процес *процесунос, опис int32, најтише int32) int32 {
	if процес == nil {
		return Enfile
	}
	if најтише < 0 || најтише >= максОписник {
		return Einval
	}
	for описник := најтише; описник < максОписник; описник++ {
		if !процес.fds[описник].заузето_2 {
			процес.fds[описник] = описникунос{заузето_2: true, опис: опис}
			return описник
		}
	}
	return Emfile
}

func releaseОтвориДатотека(опис int32) {
	if опис < 0 || опис >= максОтвориДАТОТЕКЕ {
		return
	}
	унос := &отвориДатотекаТабела[опис]
	if унос.refs > 0 {
		унос.refs--
	}

	if унос.refs == 0 && опис > stderrОписник {
		if унос.врста == описникврстаПрикључница && унос.aux < максsockets {
			локалнаsockets[унос.aux] = локалнаdatagramПрикључница{}
		}
		*унос = отвориДатотекаОпис{}
	}
}

func затвориПроцесОписник(процес *процесунос, описник int32) int32 {
	if процес == nil || getОтвориДатотекаfor(процес, описник) == nil {
		return Ebadf
	}
	опис := процес.fds[описник].опис
	процес.fds[описник] = описникунос{}
	releaseОтвориДатотека(опис)
	return 0
}

func sysПише(описник int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	унос := getОтвориДатотека(описник)
	if унос == nil {
		return Ebadf
	}
	if унос.врста != описникврстаКонзола {
		if унос.врста == описникврстаПрикључница {
			return прикључницаПошаљиto(описник, address, count, 0, 0)
		}
		if унос.врста == описникврстаfat || унос.врста == описникврстаКоренДиректоријум {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetБајтовасаПоказивач(uintptr(address), int(count), int(count))
	конзола_2.MШтампај(buffer)
	return int32(count)
}

func sysчитање(описник int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	унос := getОтвориДатотека(описник)
	if унос == nil {
		return Ebadf
	}
	if унос.врста == описникврстаstdin {
		return читањеstdin(address, count)
	}
	if унос.врста == описникврстаКоренДиректоријум {
		return Eisdir
	}
	if унос.врста == описникврстаПрикључница {
		return прикључницаreceiveса(описник, address, count, 0, 0)
	}
	if унос.врста != описникврстаfat {
		return Ebadf
	}
	if унос.положај >= унос.величина {
		return 0
	}
	remaining := унос.величина - унос.положај
	if count > remaining {
		count = remaining
	}
	buffer := GetБајтовасаПоказивач(uintptr(address), int(count), int(count))
	return читањеvfsДатотека(унос, buffer, count)
}

func sysОтвори(пУТАЊАaddress uint32, параметри uint32, рЕЖИМ uint32) int32 {
	_ = рЕЖИМ
	if пУТАЊАaddress == 0 {
		return Efault
	}
	приступањеРЕЖИМ := параметри & 3
	if приступањеРЕЖИМ == oПишеonly || приступањеРЕЖИМ == oчитањеПише || (параметри&(ocreate|oОдсеците|oappend)) != 0 {
		return Erofs
	}

	процес := ensureТренутноПроцес()
	if процес == nil {
		return Enfile
	}
	опис := allocateОтвориДатотека()
	if опис < 0 {
		return опис
	}
	унос := &отвориДатотекаТабела[опис]
	унос.параметри = параметри
	if isКоренПУТАЊА(пУТАЊАaddress) {
		унос.врста = описникврстаКоренДиректоријум
		унос.величина = 0
	} else {
		називlen, назив := умножиПУТАЊА(пУТАЊАaddress)
		if називlen == 0 {
			*унос = отвориДатотекаОпис{}
			return Enoent
		}
		величина := датотекаВеличина(назив[:називlen])
		if величина == 0 {
			*унос = отвориДатотекаОпис{}
			return Enoent
		}
		if (параметри & oДиректоријум) != 0 {
			*унос = отвориДатотекаОпис{}
			return Enotdir
		}
		унос.врста = описникврстаfat
		унос.величина = величина
		унос.називlen = називlen
		унос.назив = назив
	}

	описник := allocateОписник(процес, опис, 3)
	if описник < 0 {
		*унос = отвориДатотекаОпис{}
		return описник
	}
	return описник
}

func sysЗатвори(описник int32) int32 {
	return затвориПроцесОписник(ensureТренутноПроцес(), описник)
}

func sysdup(описник int32, најтише int32) int32 {
	процес := ensureТренутноПроцес()
	унос := getОтвориДатотекаfor(процес, описник)
	if унос == nil {
		return Ebadf
	}
	новаОписник := allocateОписник(процес, процес.fds[описник].опис, најтише)
	if новаОписник >= 0 {
		унос.refs++
	}
	return новаОписник
}

func sysdup2(oldОписник int32, новаОписник int32) int32 {
	процес := ensureТренутноПроцес()
	унос := getОтвориДатотекаfor(процес, oldОписник)
	if унос == nil {
		return Ebadf
	}
	if новаОписник < 0 || новаОписник >= максОписник {
		return Ebadf
	}
	if oldОписник == новаОписник {
		return новаОписник
	}
	if процес.fds[новаОписник].заузето_2 {
		затвориПроцесОписник(процес, новаОписник)
	}
	процес.fds[новаОписник] = описникунос{заузето_2: true, опис: процес.fds[oldОписник].опис}
	унос.refs++
	return новаОписник
}

func sysfcntl(описник int32, наредба uint32, argument uint32) int32 {
	процес := ensureТренутноПроцес()
	унос := getОтвориДатотекаfor(процес, описник)
	if унос == nil {
		return Ebadf
	}
	switch наредба {
	case fdupОписник:
		return sysdup(описник, int32(argument))
	case fgetОписник:
		return int32(процес.fds[описник].описникПараметри)
	case fскупОписник:
		процес.fds[описник].описникПараметри = argument & описникcloexec
		return 0
	case fgetfl:
		return int32(унос.параметри)
	case fскупfl:
		унос.параметри = (унос.параметри & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(описник int32, offset int32, whence uint32) int32 {
	унос := getОтвориДатотека(описник)
	if унос == nil {
		return Ebadf
	}
	if унос.врста != описникврстаfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekскуп:
		base = 0
	case seekТренутно:
		base = int64(унос.положај)
	case seekKraj:
		base = int64(унос.величина)
	default:
		return Einval
	}
	положај_2 := base + int64(offset)
	if положај_2 < 0 || положај_2 > 0x7FFFFFFF {
		return Einval
	}
	унос.положај = uint32(положај_2)
	return int32(унос.положај)
}

func читањеvfsДатотека(унос *отвориДатотекаОпис, одредиште_2 []byte, count uint32) int32 {
	меморијаmanager := &mem.TМеморијаmanager{}
	tmpПоказивач := меморијаmanager.Malloc(унос.величина)
	if tmpПоказивач == nil {
		return Einval
	}
	tmp := GetБајтовасаПоказивач(uintptr(tmpПоказивач), int(унос.величина), int(унос.величина))
	читањеДатотека(унос.назив[:унос.називlen], tmp)
	copy(одредиште_2[:count], tmp[унос.положај:унос.положај+count])
	унос.положај += count
	меморијаmanager.Слободно(tmpПоказивач)
	return int32(count)
}

func isКоренПУТАЊА(пУТАЊАaddress uint32) bool {
	if пУТАЊАaddress == 0 {
		return false
	}
	пУТАЊА := GetБајтовасаПоказивач(uintptr(пУТАЊАaddress), 4, 4)
	if пУТАЊА[0] == '/' && пУТАЊА[1] == 0 {
		return true
	}
	if пУТАЊА[0] == '.' && пУТАЊА[1] == 0 {
		return true
	}
	if пУТАЊА[0] == '/' && пУТАЊА[1] == '.' && пУТАЊА[2] == 0 {
		return true
	}
	return false
}

func sysприступање(пУТАЊАaddress uint32, рЕЖИМ uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if (рЕЖИМ & ^uint32(7)) != 0 {
		return Einval
	}
	isКорен := isКоренПУТАЊА(пУТАЊАaddress)
	exists := isКорен
	if !exists {
		називlen, назив := умножиПУТАЊА(пУТАЊАaddress)
		exists = називlen != 0 && датотекаВеличина(назив[:називlen]) != 0
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

func syschdir(пУТАЊАaddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if !isКоренПУТАЊА(пУТАЊАaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, величина uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if величина < 2 {
		return Erange
	}
	buffer_2 := GetБајтовасаПоказивач(uintptr(bufferaddress), int(величина), int(величина))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, рЕЖИМ uint32, величина uint32, ичвор uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Уређај = 1
	stat.Ino = ичвор
	stat.РЕЖИМ = рЕЖИМ
	stat.Nlink = 1
	stat.Величина_2 = int32(величина)
	stat.Blksize = 512
	stat.Блок = int32((величина + 511) / 512)
	return 0
}

func sysstat(пУТАЊАaddress uint32, stataddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if isКоренПУТАЊА(пУТАЊАaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	називlen, назив := умножиПУТАЊА(пУТАЊАaddress)
	if називlen == 0 {
		return Enoent
	}
	величина := датотекаВеличина(назив[:називlen])
	if величина == 0 {
		return Enoent
	}
	ичвор := uint32(2)
	for i := uint32(0); i < називlen; i++ {
		ичвор = ичвор*33 + uint32(назив[i])
	}
	return fillposixstat(stataddress, sifreg|0444, величина, ичвор)
}

func sysfstat(описник int32, stataddress uint32) int32 {
	унос := getОтвориДатотека(описник)
	if унос == nil {
		return Ebadf
	}
	switch унос.врста {
	case описникврстаstdin, описникврстаКонзола:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(описник+1))
	case описникврстаКоренДиректоријум:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case описникврстаfat:
		return fillposixstat(stataddress, sifreg|0444, унос.величина, uint32(описник+2))
	case описникврстаПрикључница:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(описник+2))
	}
	return Ebadf
}

func sysfsync(описник int32) int32 {
	if getОтвориДатотека(описник) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	процес := ensureТренутноПроцес()
	if процес == nil {
		return 0
	}
	if процес.програмbreak == 0 {
		процес.програмbreak = корисникheapbase
	}
	if address_2 == 0 {
		return процес.програмbreak
	}
	if address_2 < корисникheapbase || address_2 > корисникheapОграничи {
		return процес.програмbreak
	}
	процес.програмbreak = address_2
	return процес.програмbreak
}

func умножиutsпоље(одредиште *[65]byte, вредност string) {
	ограничи := len(вредност)
	if ограничи > 64 {
		ограничи = 64
	}
	for i := 0; i < ограничи; i++ {
		одредиште[i] = вредност[i]
	}
	одредиште[ограничи] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	назив := (*posixutsname)(Pointer(uintptr(address_2)))
	*назив = posixutsname{}
	умножиutsпоље(&назив.Sysname, "EngOS")
	умножиutsпоље(&назив.Nodename, "engos")
	умножиutsпоље(&назив.Release, "0.1-posix")
	умножиutsпоље(&назив.Издање, "POSIX.1-2017 phase 1")
	умножиutsпоље(&назив.Machine, "i386")
	return 0
}

func виртуелнамеморијаunsignedinteger16(вредност uint16) uint16 {
	return (вредност << 8) | (вредност >> 8)
}

func прикључницаcallargument(аргументи_2 uint32, попис uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(аргументи_2 + попис*4)))
}

func прикључницаforОписник(описник int32) (*локалнаdatagramПрикључница, int32) {
	унос := getОтвориДатотека(описник)
	if унос == nil || унос.врста != описникврстаПрикључница || унос.aux >= максsockets {
		return nil, Ebadf
	}
	прикључница := &локалнаsockets[унос.aux]
	if !прикључница.заузето_2 {
		return nil, Ebadf
	}
	return прикључница, 0
}

func allocateПрикључница(домен uint32, прикључницаВрста uint32, protocol uint32) int32 {
	if домен != afinet {
		return Eafnosupport
	}
	if прикључницаВрста != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	процес := ensureТренутноПроцес()
	if процес == nil {
		return Enfile
	}
	прикључницаПопис := -1
	for i := 0; i < максsockets; i++ {
		if !локалнаsockets[i].заузето_2 {
			прикључницаПопис = i
			break
		}
	}
	if прикључницаПопис < 0 {
		return Enfile
	}
	опис := allocateОтвориДатотека()
	if опис < 0 {
		return опис
	}
	локалнаsockets[прикључницаПопис] = локалнаdatagramПрикључница{заузето_2: true}
	унос := &отвориДатотекаТабела[опис]
	унос.врста = описникврстаПрикључница
	унос.параметри = oчитањеПише
	унос.aux = uint32(прикључницаПопис)
	описник := allocateОписник(процес, опис, 3)
	if описник < 0 {
		локалнаsockets[прикључницаПопис] = локалнаdatagramПрикључница{}
		*унос = отвориДатотекаОпис{}
		return описник
	}
	return описник
}

func прикључницаaddress(address_2 uint32, дужина uint32) (*прикључницаaddressiТревр4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if дужина < 16 {
		return nil, Einval
	}
	иСХОД := (*прикључницаaddressiТревр4)(Pointer(uintptr(address_2)))
	if иСХОД.Family != afinet {
		return nil, Eafnosupport
	}
	return иСХОД, 0
}

func портПримљеноКористи(порт uint16, except *локалнаdatagramПрикључница) bool {
	for i := 0; i < максsockets; i++ {
		прикључница := &локалнаsockets[i]
		if прикључница != except && прикључница.заузето_2 && прикључница.bound && прикључница.локална.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(прикључница *локалнаdatagramПрикључница) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := виртуелнамеморијаunsignedinteger16(следећеephemeralПорт)
		следећеephemeralПорт++
		if следећеephemeralПорт < 49152 {
			следећеephemeralПорт = 49152
		}
		if !портПримљеноКористи(порт, прикључница) {
			прикључница.локална = прикључницаaddressiТревр4{Family: afinet, Порт: порт, Address: 0x0100007F}
			прикључница.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func прикључницаbind(описник int32, address_2 uint32, дужина uint32) int32 {
	прикључница, грешка := прикључницаforОписник(описник)
	if грешка != 0 {
		return грешка
	}
	requested, грешка := прикључницаaddress(address_2, дужина)
	if грешка != 0 {
		return грешка
	}
	if прикључница.bound {
		return Einval
	}
	if requested.Порт == 0 {
		return bindephemeral(прикључница)
	}
	if портПримљеноКористи(requested.Порт, прикључница) {
		return Eaddrinuse
	}
	прикључница.локална = *requested
	прикључница.bound = true
	return 0
}

func прикључницаПовежисе(описник int32, address_2 uint32, дужина uint32) int32 {
	прикључница, грешка := прикључницаforОписник(описник)
	if грешка != 0 {
		return грешка
	}
	удаљено, грешка := прикључницаaddress(address_2, дужина)
	if грешка != 0 {
		return грешка
	}
	if !прикључница.bound {
		if грешка := bindephemeral(прикључница); грешка != 0 {
			return грешка
		}
	}
	прикључница.удаљено = *удаљено
	прикључница.connected = true
	return 0
}

func прикључницаПошаљиto(описник int32, bufferaddress_2 uint32, дужина uint32, одредиштеaddress uint32, одредиштеДужина uint32) int32 {
	прикључница, грешка := прикључницаforОписник(описник)
	if грешка != 0 {
		return грешка
	}
	if дужина > максdatagramВеличина {
		return Emsgsize
	}
	if дужина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var одредиште прикључницаaddressiТревр4
	if одредиштеaddress != 0 {
		address_2, addressГрешка := прикључницаaddress(одредиштеaddress, одредиштеДужина)
		if addressГрешка != 0 {
			return addressГрешка
		}
		одредиште = *address_2
	} else {
		if !прикључница.connected {
			return Enotconn
		}
		одредиште = прикључница.удаљено
	}
	if !прикључница.bound {
		if bindГрешка := bindephemeral(прикључница); bindГрешка != 0 {
			return bindГрешка
		}
	}
	var receiver *локалнаdatagramПрикључница
	for i := 0; i < максsockets; i++ {
		candidate := &локалнаsockets[i]
		if candidate.заузето_2 && candidate.bound && candidate.локална.Порт == одредиште.Порт &&
			(candidate.локална.Address == 0 || candidate.локална.Address == одредиште.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= максПрикључницапакета {
		return Eagain
	}
	packet := &receiver.пакета[receiver.tail]
	*packet = прикључницаpacket{заузето_2: true, величина: дужина, извор: прикључница.локална}
	if дужина != 0 {
		извор := GetБајтовасаПоказивач(uintptr(bufferaddress_2), int(дужина), int(дужина))
		copy(packet.data[:дужина], извор)
	}
	receiver.tail = (receiver.tail + 1) % максПрикључницапакета
	receiver.count++
	return int32(дужина)
}

func прикључницаreceiveса(описник int32, bufferaddress_2 uint32, дужина uint32, изворaddress uint32, изворДужинаaddress uint32) int32 {
	прикључница, грешка := прикључницаforОписник(описник)
	if грешка != 0 {
		return грешка
	}
	if дужина != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if прикључница.count == 0 {
		return Eagain
	}
	packet := &прикључница.пакета[прикључница.head]
	умножиДужина := packet.величина
	if умножиДужина > дужина {
		умножиДужина = дужина
	}
	if умножиДужина != 0 {
		одредиште := GetБајтовасаПоказивач(uintptr(bufferaddress_2), int(умножиДужина), int(умножиДужина))
		copy(одредиште, packet.data[:умножиДужина])
	}
	if изворaddress != 0 {
		if изворДужинаaddress == 0 {
			return Efault
		}
		providedДужина := (*uint32)(Pointer(uintptr(изворДужинаaddress)))
		if *providedДужина >= 16 {
			*(*прикључницаaddressiТревр4)(Pointer(uintptr(изворaddress))) = packet.извор
		}
		*providedДужина = 16
	}
	*packet = прикључницаpacket{}
	прикључница.head = (прикључница.head + 1) % максПрикључницапакета
	прикључница.count--
	return int32(умножиДужина)
}

func умножиПрикључницаНазив(описник int32, address_2 uint32, дужинаaddress uint32, peer bool) int32 {
	прикључница, грешка := прикључницаforОписник(описник)
	if грешка != 0 {
		return грешка
	}
	if address_2 == 0 || дужинаaddress == 0 {
		return Efault
	}
	дужина := (*uint32)(Pointer(uintptr(дужинаaddress)))
	if *дужина < 16 {
		*дужина = 16
		return Einval
	}
	if peer {
		if !прикључница.connected {
			return Enotconn
		}
		*(*прикључницаaddressiТревр4)(Pointer(uintptr(address_2))) = прикључница.удаљено
	} else {
		if !прикључница.bound {
			if bindГрешка := bindephemeral(прикључница); bindГрешка != 0 {
				return bindГрешка
			}
		}
		*(*прикључницаaddressiТревр4)(Pointer(uintptr(address_2))) = прикључница.локална
	}
	*дужина = 16
	return 0
}

func sysПрикључницаcall(call uint32, аргументи_2 uint32) int32 {
	if аргументи_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateПрикључница(прикључницаcallargument(аргументи_2, 0), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2))
	case 2:
		return прикључницаbind(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2))
	case 3:
		return прикључницаПовежисе(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return умножиПрикључницаНазив(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), false)
	case 7:
		return умножиПрикључницаНазив(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), true)
	case 9:
		return прикључницаПошаљиto(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), 0, 0)
	case 10:
		return прикључницаreceiveса(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), 0, 0)
	case 11:
		return прикључницаПошаљиto(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), прикључницаcallargument(аргументи_2, 4), прикључницаcallargument(аргументи_2, 5))
	case 12:
		return прикључницаreceiveса(int32(прикључницаcallargument(аргументи_2, 0)), прикључницаcallargument(аргументи_2, 1), прикључницаcallargument(аргументи_2, 2), прикључницаcallargument(аргументи_2, 4), прикључницаcallargument(аргументи_2, 5))
	case 13:
		if _, грешка := прикључницаforОписник(int32(прикључницаcallargument(аргументи_2, 0))); грешка != 0 {
			return грешка
		}
		return 0
	case 14:
		if _, грешка := прикључницаforОписник(int32(прикључницаcallargument(аргументи_2, 0))); грешка != 0 {
			return грешка
		}
		return 0
	}
	return Eopnotsupp
}

func читањеstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetБајтовасаПоказивач(uintptr(address), int(count), int(count))
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
	следеће := (stdinПише + 1) % uint32(len(stdinbuffer))
	if следеће == stdinчитање {
		return
	}
	stdinbuffer[stdinПише] = c
	stdinПише = следеће
}

func stdingetblocking() byte {
	for stdinчитање == stdinПише {
		sc := pollТастатураscancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinчитање]
	stdinчитање = (stdinчитање + 1) % uint32(len(stdinbuffer))
	return c
}

func pollТастатураscancode() byte {
	for (Портчитањеbyte(0x64) & 0x01) == 0 {
	}
	sc := Портчитањеbyte(0x60)
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

func умножиизвршнаvector(address_2 uint32, иСХОД *извршнаvector) int32 {
	*иСХОД = извршнаvector{}
	if address_2 == 0 {
		return 0
	}
	for попис := uint32(0); попис < максизвршнаvectorунос; попис++ {
		нискаaddress := *(*uint32)(Pointer(uintptr(address_2 + попис*4)))
		if нискаaddress == 0 {
			иСХОД.count = попис
			return 0
		}
		terminated := false
		for дужина := uint32(0); дужина <= максизвршнанискаДужина; дужина++ {
			вредност := *(*byte)(Pointer(uintptr(нискаaddress + дужина)))
			иСХОД.вредности[попис][дужина] = вредност
			if вредност == 0 {
				иСХОД.lengths[попис] = дужина
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

func pushизвршнаunsignedinteger32(stack *uint32, вредност uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = вредност
}

func setupизвршнаstack(процесор *TcpuСтање, аргументи_2 *извршнаvector, environment *извршнаvector) int32 {
	const stackБајтова uint32 = 4096
	if !MakeОпсегПриватноwritable(getcr3(), КорисникstackГоре-stackБајтова, stackБајтова) {
		return Enomem
	}
	stack := КорисникstackГоре
	var argumentpointers [максизвршнаvectorунос]uint32
	var environmentpointers [максизвршнаvectorунос]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		дужина := environment.lengths[i] + 1
		stack -= дужина
		одредиште := GetБајтовасаПоказивач(uintptr(stack), int(дужина), int(дужина))
		copy(одредиште, environment.вредности[i][:дужина])
		environmentpointers[i] = stack
	}
	for i := int(аргументи_2.count) - 1; i >= 0; i-- {
		дужина := аргументи_2.lengths[i] + 1
		stack -= дужина
		одредиште := GetБајтовасаПоказивач(uintptr(stack), int(дужина), int(дужина))
		copy(одредиште, аргументи_2.вредности[i][:дужина])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushизвршнаunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushизвршнаunsignedinteger32(&stack, environmentpointers[i])
	}
	pushизвршнаunsignedinteger32(&stack, 0)
	for i := int(аргументи_2.count) - 1; i >= 0; i-- {
		pushизвршнаunsignedinteger32(&stack, argumentpointers[i])
	}
	pushизвршнаunsignedinteger32(&stack, аргументи_2.count)
	процесор.Esp = stack
	процесор.Ebp = 0
	return 0
}

func затворинаизвршна(процес *процесунос) {
	if процес == nil {
		return
	}
	for описник := int32(0); описник < максОписник; описник++ {
		if процес.fds[описник].заузето_2 && (процес.fds[описник].описникПараметри&описникcloexec) != 0 {
			затвориПроцесОписник(процес, описник)
		}
	}
}

func sysexecve(процесор *TcpuСтање, пУТАЊАaddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	var аргументи_2 извршнаvector
	var environment извршнаvector
	if иСХОД := умножиизвршнаvector(процесор.Ecx, &аргументи_2); иСХОД < 0 {
		return иСХОД
	}
	if иСХОД := умножиизвршнаvector(процесор.Edx, &environment); иСХОД < 0 {
		return иСХОД
	}
	називlen, назив := умножиПУТАЊА(пУТАЊАaddress)
	if називlen == 0 {
		return Enoent
	}
	величина := датотекаВеличина(назив[:називlen])
	if величина == 0 {
		return Enoent
	}
	меморијаmanager := &mem.TМеморијаmanager{}
	датотекаПоказивач := меморијаmanager.Malloc(величина)
	if датотекаПоказивач == nil {
		return Einval
	}
	data := GetБајтовасаПоказивач(uintptr(датотекаПоказивач), int(величина), int(величина))
	читањеДатотека(назив[:називlen], data)
	if величина < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		меморијаmanager.Слободно(датотекаПоказивач)
		return Enoexec
	}
	loader := Elf{}
	унос := loader.Getунос(data)
	loader.Parse(data, getcr3())
	меморијаmanager.Слободно(датотекаПоказивач)
	if иСХОД := setupизвршнаstack(процесор, &аргументи_2, &environment); иСХОД < 0 {
		return иСХОД
	}
	затворинаизвршна(ensureТренутноПроцес())
	процесор.Eip = унос
	процесор.Eax = 0
	return 0
}

func sysfork(процесор *TcpuСтање) int32 {
	надређениПИД := ТренутноПИД()
	if ensureТренутноПроцес() == nil {
		return Enfile
	}
	пИД := allocateПроцес(надређениПИД)
	if пИД == 0 {
		return Einval
	}
	меморијаmanager := &mem.TМеморијаmanager{}
	threadПоказивач := меморијаmanager.Malloc(uint32(Sizeof(TThread{})))
	stackПоказивач := меморијаmanager.Malloc(ThreadstackВеличина)
	садржаниСТРАНАДиректоријум := Cloneaddressразмакcow(getcr3())
	if threadПоказивач == nil || stackПоказивач == nil || садржаниСТРАНАДиректоријум == 0 {
		одбациПроцес(пИД)
		return Einval
	}
	садржани := (*TThread)(threadПоказивач)
	садржани.Stack = uint32(uintptr(stackПоказивач))
	садржани.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(stackПоказивач) + ThreadstackВеличина - Sizeof(TcpuСтање{})))
	*садржани.ПроцесорСтање = *процесор
	садржани.ПроцесорСтање.Eax = 0
	садржани.Корисникstack_2 = процесор.Esp
	садржани.КорисникstackВеличина_2 = 0
	садржани.ПИД = пИД
	садржани.НадређениПИД = надређениПИД
	садржани.СТРАНАДиректоријумунос = садржаниСТРАНАДиректоријум
	садржани.ThreadСтање = Спреман
	садржани.Fpuoffset = 0xffffffff
	садржани.Iskernel = false
	Додајrunnablethread(садржани)
	return int32(пИД)
}

func sysИзлаз(стање uint32) {
	пИД := ТренутноПИД()
	for i := 0; i < len(процесТабела); i++ {
		if процесТабела[i].заузето_2 && процесТабела[i].пИД == пИД {
			затвориСвеПроцесfds(&процесТабела[i])
			процесТабела[i].изашаосам = true
			процесТабела[i].стање = (стање & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(пИД int32, стањеaddress uint32, опције uint32) int32 {
	if (опције & ^uint32(1)) != 0 {
		return Einval
	}
	надређениПИД := ТренутноПИД()
	foundсадржани := false
	for i := 0; i < len(процесТабела); i++ {
		p := &процесТабела[i]
		matches := пИД == -1 || пИД == 0 || p.пИД == uint32(пИД)
		if p.заузето_2 && matches && p.надређени == надређениПИД {
			foundсадржани = true
			if p.изашаосам {
				if стањеaddress != 0 {
					*(*uint32)(Pointer(uintptr(стањеaddress))) = p.стање
				}
				садржаниПИД := p.пИД
				*p = процесунос{}
				return int32(садржаниПИД)
			}
		}
	}
	if !foundсадржани {
		return Echild
	}

	if (опције & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцес(надређени uint32) uint32 {
	надређениПроцес := нађиПроцес(надређени)
	пИД := AllocateПИД()
	for i := 0; i < len(процесТабела); i++ {
		if !процесТабела[i].заузето_2 {
			процесТабела[i] = процесунос{
				заузето_2:	true,
				пИД:		пИД,
				надређени:	надређени,
				програмbreak:	корисникheapbase,
			}
			if надређениПроцес != nil {
				процесТабела[i].програмbreak = надређениПроцес.програмbreak
				for описник := 0; описник < максОписник; описник++ {
					if надређениПроцес.fds[описник].заузето_2 {
						процесТабела[i].fds[описник] = надређениПроцес.fds[описник]
						опис := надређениПроцес.fds[описник].опис
						if опис >= 0 && опис < максОтвориДАТОТЕКЕ {
							отвориДатотекаТабела[опис].refs++
						}
					}
				}
			} else {
				initializeПроцесfds(&процесТабела[i])
			}
			return пИД
		}
	}
	return 0
}

func затвориСвеПроцесfds(процес *процесунос) {
	if процес == nil {
		return
	}
	for описник := int32(0); описник < максОписник; описник++ {
		if процес.fds[описник].заузето_2 {
			затвориПроцесОписник(процес, описник)
		}
	}
}

func одбациПроцес(пИД uint32) {
	процес := нађиПроцес(пИД)
	if процес == nil {
		return
	}
	затвориСвеПроцесfds(процес)
	*процес = процесунос{}
}

func умножиПУТАЊА(пУТАЊАaddress uint32) (uint32, [12]byte) {
	var назив [12]byte
	if пУТАЊАaddress == 0 {
		return 0, назив
	}
	raw := GetБајтовасаПоказивач(uintptr(пУТАЊАaddress), 64, 64)
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
		назив[n] = c
		n++
	}
	return n, назив
}

func датотекаВеличина(датотека []byte) uint32 {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	величина := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], датотека)
	ata0s.Flush()
	return величина
}

func читањеДатотека(датотека []byte, data []byte) {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionТабела{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterБлок32{}
	bios.Читање(&ata0s, partition.Mbr.Primarypartition[0], датотека, data)
	ata0s.Flush()
}

func getcr3() uint32
