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
import mem "memorijamanager"
import . "paging"
import . "порт"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuelnoMemorija"

var конзола_2 = TКонзола{}

type TSyscall struct {
	TОметањеhandler
}

const (
	SysIzlaz	uint32	= 1
	Sysfork		uint32	= 2
	Sysчитање	uint32	= 3
	Sysupis		uint32	= 4
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
	SysrtIzlaz	uint32	= 252

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
	максОтвориDATOTEKE		= 128
)

type описникунос struct {
	zauzeto_2		bool
	опис			int32
	описникParametri	uint32
}

type отвориДатотекаОпис struct {
	zauzeto_2	bool
	refs		uint32
	врста		uint32
	parametri	uint32
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
	описникврстаKorenDirektorijum	uint32	= 4
	описникврстаПрикључница		uint32	= 5

	oчитањеonly	uint32	= 0
	oupisonly	uint32	= 1
	oчитањеupis	uint32	= 2
	ocreate		uint32	= 0x40
	oOdsecite	uint32	= 0x200
	oappend		uint32	= 0x400
	oDirektorijum	uint32	= 0x10000

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
	максПрикључницаpaketa	= 8
	максdatagramВеличина	= 512
)

type прикључницаaddressiTv4 struct {
	Family	uint16
	Порт	uint16
	Address	uint32
	Zero	[8]byte
}

type прикључницаpacket struct {
	zauzeto_2	bool
	величина	uint32
	izvor		прикључницаaddressiTv4
	data		[максdatagramВеличина]byte
}

type локалнаdatagramПрикључница struct {
	zauzeto_2	bool
	bound		bool
	connected	bool
	локална		прикључницаaddressiTv4
	удаљено		прикључницаaddressiTv4
	head		uint32
	tail		uint32
	count		uint32
	paketa		[максПрикључницаpaketa]прикључницаpacket
}

type posixstat struct {
	Уређај		uint32
	Ino		uint32
	REŽIM		uint32
	Nlink		uint32
	ЈЛБ		uint32
	Gid		uint32
	Rdev		uint32
	Величина_2	int32
	Blksize		int32
	Blok		int32
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
	максizvršnavectorунос	= 16
	максizvršnaнискаDužina	= 63
)

type izvršnavector struct {
	count		uint32
	lengths		[максizvršnavectorунос]uint32
	вредности	[максizvršnavectorунос][максizvršnaнискаDužina + 1]byte
}

type процесунос struct {
	zauzeto_2	bool
	пИД		uint32
	nadređeni	uint32
	изашаосам	bool
	стање		uint32
	програмbreak	uint32
	fds		[максОписник]описникунос
}

type нискаheader struct {
	Data	uintptr
	Len	int
}

func syscallГрешка(greška int32) uint32 {
	return *(*uint32)(Pointer(&greška))
}

var отвориДатотекаTabela [максОтвориDATOTEKE]отвориДатотекаОпис
var процесTabela [32]процесунос
var локалнаsockets [максsockets]локалнаdatagramПрикључница
var следећеephemeralПорт uint16 = 49152

const (
	korisnikheapbase	uint32	= 0x06000000
	korisnikheapОграничи	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinчитање uint32
var stdinupis uint32

func Ометање(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIzlaz_2(popis uint32) {
	Syscall(SysIzlaz, popis)
}

func Sysчитање_2(описник uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysчитање, описник, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysŠtampajstr(buffer string) {
	h := (*нискаheader)(Pointer(&buffer))
	Syscall(Sysupis, uint32(stdoutОписник), uint32(h.Data), uint32(h.Len))
}

func SysŠtampajunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysupis, uint32(stdoutОписник), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysОтвори_2(пУТАЊА uintptr, parametri uint32, rEŽIM uint32) int32 {
	return int32(Syscall(SysОтвори, uint32(пУТАЊА), parametri, rEŽIM))
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

func Syscall(параметри ...uint32) uint32 {

	l := len(параметри)
	switch l {
	case 1:
		return Ометање(параметри[0], 0, 0, 0, 0, 0)
	case 2:
		return Ометање(параметри[0], параметри[1], 0, 0, 0, 0)
	case 3:
		return Ометање(параметри[0], параметри[1], параметри[2], 0, 0, 0)
	case 4:
		return Ометање(параметри[0], параметри[1], параметри[2], параметри[3], 0, 0)
	case 5:
		return Ометање(параметри[0], параметри[1], параметри[2], параметри[3], параметри[4], 0)
	case 6:
		return Ометање(параметри[0], параметри[1], параметри[2], параметри[3], параметри[4], параметри[5])
	default:
		return syscallГрешка(Enosys)
	}
}

func (isti *TSyscall) Init(manager *TОметањеmanager) {
	initДатотекаdescriptor()

	ометањеhandler = ручкаОметање

	var address uintptr
	address = uintptr(Pointer(&ометањеhandler))

	isti.TОметањеhandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var ометањеhandler func(uint32) uint32

func ручкаОметање(esp uint32) uint32 {
	var процесор = (*TcpuСтање)(Pointer(uintptr(esp)))

	switch процесор.Eax {
	case SysIzlaz:
		sysIzlaz(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗауставиТренутноthread(процесор))))
	case SysrtIzlaz:
		sysIzlaz(процесор.Ebx)
		return uint32(uintptr(Pointer(ЗауставиТренутноthread(процесор))))
	case Sysfork:
		процесор.Eax = uint32(sysfork(процесор))
		return esp
	case Sysчитање:
		процесор.Eax = uint32(sysчитање(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case Sysupis:
		процесор.Eax = uint32(sysupis(int32(процесор.Ebx), процесор.Ecx, процесор.Edx))
		return esp
	case SysОтвори:
		процесор.Eax = uint32(sysОтвори(процесор.Ebx, процесор.Ecx, процесор.Edx))
		return esp
	case Syscreat:
		процесор.Eax = uint32(sysОтвори(процесор.Ebx, ocreate|oupisonly|oOdsecite, процесор.Ecx))
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
		процесор.Eax = ТренутноnadređeniПИД()
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
		конзола_2.MUnsignedinteger32Štampaj(процесор.Ebx)
		return esp

	default:
		конзола_2.MŠtampajxy(([]byte)("sys["), 1, 23)
		конзола_2.MUnsignedinteger32Štampaj(esp)
		конзола_2.MŠtampaj(([]byte)(":"))
		конзола_2.MUnsignedinteger32Štampaj(процесор.Eax)
		конзола_2.MŠtampaj(([]byte)(":"))
		конзола_2.MUnsignedinteger32Štampaj(процесор.Ebx)
		конзола_2.MŠtampaj(([]byte)(":"))
		конзола_2.MUnsignedinteger32Štampaj(процесор.Ecx)
		конзола_2.MŠtampaj(([]byte)(":"))
		конзола_2.MUnsignedinteger32Štampaj(процесор.Edx)
		конзола_2.MŠtampaj(([]byte)("]"))
		процесор.Eax = syscallГрешка(Enosys)
		return esp
	}

	return esp
}

func initДатотекаdescriptor() {
	for i := 0; i < максОтвориDATOTEKE; i++ {
		отвориДатотекаTabela[i] = отвориДатотекаОпис{}
	}
	for i := 0; i < len(процесTabela); i++ {
		процесTabela[i] = процесунос{}
	}
	for i := 0; i < len(локалнаsockets); i++ {
		локалнаsockets[i] = локалнаdatagramПрикључница{}
	}
	следећеephemeralПорт = 49152
	отвориДатотекаTabela[0] = отвориДатотекаОпис{zauzeto_2: true, врста: описникврстаstdin, parametri: oчитањеonly}
	отвориДатотекаTabela[1] = отвориДатотекаОпис{zauzeto_2: true, врста: описникврстаКонзола, parametri: oupisonly}
	отвориДатотекаTabela[2] = отвориДатотекаОпис{zauzeto_2: true, врста: описникврстаКонзола, parametri: oupisonly}
}

func pronađiПроцес(пИД uint32) *процесунос {
	for i := 0; i < len(процесTabela); i++ {
		if процесTabela[i].zauzeto_2 && процесTabela[i].пИД == пИД {
			return &процесTabela[i]
		}
	}
	return nil
}

func initializeПроцесfds(процес *процесунос) {
	for описник := int32(0); описник <= stderrОписник; описник++ {
		процес.fds[описник] = описникунос{zauzeto_2: true, опис: описник}
		отвориДатотекаTabela[описник].refs++
	}
}

func ensureТренутноПроцес() *процесунос {
	пИД := ТренутноПИД()
	if процес := pronađiПроцес(пИД); процес != nil {
		return процес
	}
	for i := 0; i < len(процесTabela); i++ {
		if !процесTabela[i].zauzeto_2 {
			процесTabela[i] = процесунос{
				zauzeto_2:	true,
				пИД:		пИД,
				nadređeni:	ТренутноnadređeniПИД(),
				програмbreak:	korisnikheapbase,
			}
			initializeПроцесfds(&процесTabela[i])
			return &процесTabela[i]
		}
	}
	return nil
}

func getОтвориДатотекаfor(процес *процесунос, описник int32) *отвориДатотекаОпис {
	if процес == nil || описник < 0 || описник >= максОписник || !процес.fds[описник].zauzeto_2 {
		return nil
	}
	опис := процес.fds[описник].опис
	if опис < 0 || опис >= максОтвориDATOTEKE || !отвориДатотекаTabela[опис].zauzeto_2 {
		return nil
	}
	return &отвориДатотекаTabela[опис]
}

func getОтвориДатотека(описник int32) *отвориДатотекаОпис {
	return getОтвориДатотекаfor(ensureТренутноПроцес(), описник)
}

func allocateОтвориДатотека() int32 {
	for i := int32(3); i < максОтвориDATOTEKE; i++ {
		if !отвориДатотекаTabela[i].zauzeto_2 {
			отвориДатотекаTabela[i] = отвориДатотекаОпис{zauzeto_2: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateОписник(процес *процесунос, опис int32, majtiše int32) int32 {
	if процес == nil {
		return Enfile
	}
	if majtiše < 0 || majtiše >= максОписник {
		return Einval
	}
	for описник := majtiše; описник < максОписник; описник++ {
		if !процес.fds[описник].zauzeto_2 {
			процес.fds[описник] = описникунос{zauzeto_2: true, опис: опис}
			return описник
		}
	}
	return Emfile
}

func releaseОтвориДатотека(опис int32) {
	if опис < 0 || опис >= максОтвориDATOTEKE {
		return
	}
	унос := &отвориДатотекаTabela[опис]
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

func sysupis(описник int32, address uint32, count uint32) int32 {
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
		if унос.врста == описникврстаfat || унос.врста == описникврстаKorenDirektorijum {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtovasaPokazivač(uintptr(address), int(count), int(count))
	конзола_2.MŠtampaj(buffer)
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
	if унос.врста == описникврстаKorenDirektorijum {
		return Eisdir
	}
	if унос.врста == описникврстаПрикључница {
		return прикључницаreceivesa(описник, address, count, 0, 0)
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
	buffer := GetBajtovasaPokazivač(uintptr(address), int(count), int(count))
	return читањеvfsДатотека(унос, buffer, count)
}

func sysОтвори(пУТАЊАaddress uint32, parametri uint32, rEŽIM uint32) int32 {
	_ = rEŽIM
	if пУТАЊАaddress == 0 {
		return Efault
	}
	приступањеREŽIM := parametri & 3
	if приступањеREŽIM == oupisonly || приступањеREŽIM == oчитањеupis || (parametri&(ocreate|oOdsecite|oappend)) != 0 {
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
	унос := &отвориДатотекаTabela[опис]
	унос.parametri = parametri
	if isKorenПУТАЊА(пУТАЊАaddress) {
		унос.врста = описникврстаKorenDirektorijum
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
		if (parametri & oDirektorijum) != 0 {
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

func sysdup(описник int32, majtiše int32) int32 {
	процес := ensureТренутноПроцес()
	унос := getОтвориДатотекаfor(процес, описник)
	if унос == nil {
		return Ebadf
	}
	новаОписник := allocateОписник(процес, процес.fds[описник].опис, majtiše)
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
	if процес.fds[новаОписник].zauzeto_2 {
		затвориПроцесОписник(процес, новаОписник)
	}
	процес.fds[новаОписник] = описникунос{zauzeto_2: true, опис: процес.fds[oldОписник].опис}
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
		return int32(процес.fds[описник].описникParametri)
	case fскупОписник:
		процес.fds[описник].описникParametri = argument & описникcloexec
		return 0
	case fgetfl:
		return int32(унос.parametri)
	case fскупfl:
		унос.parametri = (унос.parametri & 3) | (argument & oappend)
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

func читањеvfsДатотека(унос *отвориДатотекаОпис, odredište_2 []byte, count uint32) int32 {
	memorijamanager := &mem.TMemorijamanager{}
	tmpPokazivač := memorijamanager.Malloc(унос.величина)
	if tmpPokazivač == nil {
		return Einval
	}
	tmp := GetBajtovasaPokazivač(uintptr(tmpPokazivač), int(унос.величина), int(унос.величина))
	читањеДатотека(унос.назив[:унос.називlen], tmp)
	copy(odredište_2[:count], tmp[унос.положај:унос.положај+count])
	унос.положај += count
	memorijamanager.Slobodno(tmpPokazivač)
	return int32(count)
}

func isKorenПУТАЊА(пУТАЊАaddress uint32) bool {
	if пУТАЊАaddress == 0 {
		return false
	}
	пУТАЊА := GetBajtovasaPokazivač(uintptr(пУТАЊАaddress), 4, 4)
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

func sysприступање(пУТАЊАaddress uint32, rEŽIM uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if (rEŽIM & ^uint32(7)) != 0 {
		return Einval
	}
	isKoren := isKorenПУТАЊА(пУТАЊАaddress)
	exists := isKoren
	if !exists {
		називlen, назив := умножиПУТАЊА(пУТАЊАaddress)
		exists = називlen != 0 && датотекаВеличина(назив[:називlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (rEŽIM & 2) != 0 {
		return Eacces
	}

	if (rEŽIM&1) != 0 && !isKoren {
		return Eacces
	}
	return 0
}

func syschdir(пУТАЊАaddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if !isKorenПУТАЊА(пУТАЊАaddress) {
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
	buffer_2 := GetBajtovasaPokazivač(uintptr(bufferaddress), int(величина), int(величина))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, rEŽIM uint32, величина uint32, ичвор uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Уређај = 1
	stat.Ino = ичвор
	stat.REŽIM = rEŽIM
	stat.Nlink = 1
	stat.Величина_2 = int32(величина)
	stat.Blksize = 512
	stat.Blok = int32((величина + 511) / 512)
	return 0
}

func sysstat(пУТАЊАaddress uint32, stataddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	if isKorenПУТАЊА(пУТАЊАaddress) {
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
	case описникврстаKorenDirektorijum:
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
		процес.програмbreak = korisnikheapbase
	}
	if address_2 == 0 {
		return процес.програмbreak
	}
	if address_2 < korisnikheapbase || address_2 > korisnikheapОграничи {
		return процес.програмbreak
	}
	процес.програмbreak = address_2
	return процес.програмbreak
}

func умножиutsпоље(odredište *[65]byte, вредност string) {
	ограничи := len(вредност)
	if ограничи > 64 {
		ограничи = 64
	}
	for i := 0; i < ограничи; i++ {
		odredište[i] = вредност[i]
	}
	odredište[ограничи] = 0
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

func svapunsignedinteger16(вредност uint16) uint16 {
	return (вредност << 8) | (вредност >> 8)
}

func прикључницаcallargument(argumenti_2 uint32, popis uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenti_2 + popis*4)))
}

func прикључницаforОписник(описник int32) (*локалнаdatagramПрикључница, int32) {
	унос := getОтвориДатотека(описник)
	if унос == nil || унос.врста != описникврстаПрикључница || унос.aux >= максsockets {
		return nil, Ebadf
	}
	прикључница := &локалнаsockets[унос.aux]
	if !прикључница.zauzeto_2 {
		return nil, Ebadf
	}
	return прикључница, 0
}

func allocateПрикључница(domen uint32, прикључницаВрста uint32, protocol uint32) int32 {
	if domen != afinet {
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
	прикључницаPopis := -1
	for i := 0; i < максsockets; i++ {
		if !локалнаsockets[i].zauzeto_2 {
			прикључницаPopis = i
			break
		}
	}
	if прикључницаPopis < 0 {
		return Enfile
	}
	опис := allocateОтвориДатотека()
	if опис < 0 {
		return опис
	}
	локалнаsockets[прикључницаPopis] = локалнаdatagramПрикључница{zauzeto_2: true}
	унос := &отвориДатотекаTabela[опис]
	унос.врста = описникврстаПрикључница
	унос.parametri = oчитањеupis
	унос.aux = uint32(прикључницаPopis)
	описник := allocateОписник(процес, опис, 3)
	if описник < 0 {
		локалнаsockets[прикључницаPopis] = локалнаdatagramПрикључница{}
		*унос = отвориДатотекаОпис{}
		return описник
	}
	return описник
}

func прикључницаaddress(address_2 uint32, dužina uint32) (*прикључницаaddressiTv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if dužina < 16 {
		return nil, Einval
	}
	иСХОД := (*прикључницаaddressiTv4)(Pointer(uintptr(address_2)))
	if иСХОД.Family != afinet {
		return nil, Eafnosupport
	}
	return иСХОД, 0
}

func портПримљеноКористи(порт uint16, except *локалнаdatagramПрикључница) bool {
	for i := 0; i < максsockets; i++ {
		прикључница := &локалнаsockets[i]
		if прикључница != except && прикључница.zauzeto_2 && прикључница.bound && прикључница.локална.Порт == порт {
			return true
		}
	}
	return false
}

func bindephemeral(прикључница *локалнаdatagramПрикључница) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		порт := svapunsignedinteger16(следећеephemeralПорт)
		следећеephemeralПорт++
		if следећеephemeralПорт < 49152 {
			следећеephemeralПорт = 49152
		}
		if !портПримљеноКористи(порт, прикључница) {
			прикључница.локална = прикључницаaddressiTv4{Family: afinet, Порт: порт, Address: 0x0100007F}
			прикључница.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func прикључницаbind(описник int32, address_2 uint32, dužina uint32) int32 {
	прикључница, greška := прикључницаforОписник(описник)
	if greška != 0 {
		return greška
	}
	requested, greška := прикључницаaddress(address_2, dužina)
	if greška != 0 {
		return greška
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

func прикључницаPovežise(описник int32, address_2 uint32, dužina uint32) int32 {
	прикључница, greška := прикључницаforОписник(описник)
	if greška != 0 {
		return greška
	}
	удаљено, greška := прикључницаaddress(address_2, dužina)
	if greška != 0 {
		return greška
	}
	if !прикључница.bound {
		if greška := bindephemeral(прикључница); greška != 0 {
			return greška
		}
	}
	прикључница.удаљено = *удаљено
	прикључница.connected = true
	return 0
}

func прикључницаПошаљиto(описник int32, bufferaddress_2 uint32, dužina uint32, odredišteaddress uint32, odredišteDužina uint32) int32 {
	прикључница, greška := прикључницаforОписник(описник)
	if greška != 0 {
		return greška
	}
	if dužina > максdatagramВеличина {
		return Emsgsize
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var odredište прикључницаaddressiTv4
	if odredišteaddress != 0 {
		address_2, addressГрешка := прикључницаaddress(odredišteaddress, odredišteDužina)
		if addressГрешка != 0 {
			return addressГрешка
		}
		odredište = *address_2
	} else {
		if !прикључница.connected {
			return Enotconn
		}
		odredište = прикључница.удаљено
	}
	if !прикључница.bound {
		if bindГрешка := bindephemeral(прикључница); bindГрешка != 0 {
			return bindГрешка
		}
	}
	var receiver *локалнаdatagramПрикључница
	for i := 0; i < максsockets; i++ {
		candidate := &локалнаsockets[i]
		if candidate.zauzeto_2 && candidate.bound && candidate.локална.Порт == odredište.Порт &&
			(candidate.локална.Address == 0 || candidate.локална.Address == odredište.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= максПрикључницаpaketa {
		return Eagain
	}
	packet := &receiver.paketa[receiver.tail]
	*packet = прикључницаpacket{zauzeto_2: true, величина: dužina, izvor: прикључница.локална}
	if dužina != 0 {
		izvor := GetBajtovasaPokazivač(uintptr(bufferaddress_2), int(dužina), int(dužina))
		copy(packet.data[:dužina], izvor)
	}
	receiver.tail = (receiver.tail + 1) % максПрикључницаpaketa
	receiver.count++
	return int32(dužina)
}

func прикључницаreceivesa(описник int32, bufferaddress_2 uint32, dužina uint32, izvoraddress uint32, izvorDužinaaddress uint32) int32 {
	прикључница, greška := прикључницаforОписник(описник)
	if greška != 0 {
		return greška
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if прикључница.count == 0 {
		return Eagain
	}
	packet := &прикључница.paketa[прикључница.head]
	умножиDužina := packet.величина
	if умножиDužina > dužina {
		умножиDužina = dužina
	}
	if умножиDužina != 0 {
		odredište := GetBajtovasaPokazivač(uintptr(bufferaddress_2), int(умножиDužina), int(умножиDužina))
		copy(odredište, packet.data[:умножиDužina])
	}
	if izvoraddress != 0 {
		if izvorDužinaaddress == 0 {
			return Efault
		}
		providedDužina := (*uint32)(Pointer(uintptr(izvorDužinaaddress)))
		if *providedDužina >= 16 {
			*(*прикључницаaddressiTv4)(Pointer(uintptr(izvoraddress))) = packet.izvor
		}
		*providedDužina = 16
	}
	*packet = прикључницаpacket{}
	прикључница.head = (прикључница.head + 1) % максПрикључницаpaketa
	прикључница.count--
	return int32(умножиDužina)
}

func умножиПрикључницаНазив(описник int32, address_2 uint32, dužinaaddress uint32, peer bool) int32 {
	прикључница, greška := прикључницаforОписник(описник)
	if greška != 0 {
		return greška
	}
	if address_2 == 0 || dužinaaddress == 0 {
		return Efault
	}
	dužina := (*uint32)(Pointer(uintptr(dužinaaddress)))
	if *dužina < 16 {
		*dužina = 16
		return Einval
	}
	if peer {
		if !прикључница.connected {
			return Enotconn
		}
		*(*прикључницаaddressiTv4)(Pointer(uintptr(address_2))) = прикључница.удаљено
	} else {
		if !прикључница.bound {
			if bindГрешка := bindephemeral(прикључница); bindГрешка != 0 {
				return bindГрешка
			}
		}
		*(*прикључницаaddressiTv4)(Pointer(uintptr(address_2))) = прикључница.локална
	}
	*dužina = 16
	return 0
}

func sysПрикључницаcall(call uint32, argumenti_2 uint32) int32 {
	if argumenti_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocateПрикључница(прикључницаcallargument(argumenti_2, 0), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2))
	case 2:
		return прикључницаbind(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2))
	case 3:
		return прикључницаPovežise(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return умножиПрикључницаНазив(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), false)
	case 7:
		return умножиПрикључницаНазив(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), true)
	case 9:
		return прикључницаПошаљиto(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), 0, 0)
	case 10:
		return прикључницаreceivesa(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), 0, 0)
	case 11:
		return прикључницаПошаљиto(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), прикључницаcallargument(argumenti_2, 4), прикључницаcallargument(argumenti_2, 5))
	case 12:
		return прикључницаreceivesa(int32(прикључницаcallargument(argumenti_2, 0)), прикључницаcallargument(argumenti_2, 1), прикључницаcallargument(argumenti_2, 2), прикључницаcallargument(argumenti_2, 4), прикључницаcallargument(argumenti_2, 5))
	case 13:
		if _, greška := прикључницаforОписник(int32(прикључницаcallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	case 14:
		if _, greška := прикључницаforОписник(int32(прикључницаcallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	}
	return Eopnotsupp
}

func читањеstdin(address uint32, count uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := GetBajtovasaPokazivač(uintptr(address), int(count), int(count))
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
	следеће := (stdinupis + 1) % uint32(len(stdinbuffer))
	if следеће == stdinчитање {
		return
	}
	stdinbuffer[stdinupis] = c
	stdinupis = следеће
}

func stdingetblocking() byte {
	for stdinчитање == stdinupis {
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

func умножиizvršnavector(address_2 uint32, иСХОД *izvršnavector) int32 {
	*иСХОД = izvršnavector{}
	if address_2 == 0 {
		return 0
	}
	for popis := uint32(0); popis < максizvršnavectorунос; popis++ {
		нискаaddress := *(*uint32)(Pointer(uintptr(address_2 + popis*4)))
		if нискаaddress == 0 {
			иСХОД.count = popis
			return 0
		}
		terminated := false
		for dužina := uint32(0); dužina <= максizvršnaнискаDužina; dužina++ {
			вредност := *(*byte)(Pointer(uintptr(нискаaddress + dužina)))
			иСХОД.вредности[popis][dužina] = вредност
			if вредност == 0 {
				иСХОД.lengths[popis] = dužina
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

func pushizvršnaunsignedinteger32(stack *uint32, вредност uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = вредност
}

func setupizvršnastack(процесор *TcpuСтање, argumenti_2 *izvršnavector, environment *izvršnavector) int32 {
	const stackBajtova uint32 = 4096
	if !MakeOpsegPrivatnowritable(getcr3(), KorisnikstackГоре-stackBajtova, stackBajtova) {
		return Enomem
	}
	stack := KorisnikstackГоре
	var argumentpointers [максizvršnavectorунос]uint32
	var environmentpointers [максizvršnavectorунос]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		dužina := environment.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovasaPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, environment.вредности[i][:dužina])
		environmentpointers[i] = stack
	}
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		dužina := argumenti_2.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovasaPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, argumenti_2.вредности[i][:dužina])
		argumentpointers[i] = stack
	}
	stack &= ^uint32(3)
	pushizvršnaunsignedinteger32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushizvršnaunsignedinteger32(&stack, environmentpointers[i])
	}
	pushizvršnaunsignedinteger32(&stack, 0)
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		pushizvršnaunsignedinteger32(&stack, argumentpointers[i])
	}
	pushizvršnaunsignedinteger32(&stack, argumenti_2.count)
	процесор.Esp = stack
	процесор.Ebp = 0
	return 0
}

func затвориnaizvršna(процес *процесунос) {
	if процес == nil {
		return
	}
	for описник := int32(0); описник < максОписник; описник++ {
		if процес.fds[описник].zauzeto_2 && (процес.fds[описник].описникParametri&описникcloexec) != 0 {
			затвориПроцесОписник(процес, описник)
		}
	}
}

func sysexecve(процесор *TcpuСтање, пУТАЊАaddress uint32) int32 {
	if пУТАЊАaddress == 0 {
		return Efault
	}
	var argumenti_2 izvršnavector
	var environment izvršnavector
	if иСХОД := умножиizvršnavector(процесор.Ecx, &argumenti_2); иСХОД < 0 {
		return иСХОД
	}
	if иСХОД := умножиizvršnavector(процесор.Edx, &environment); иСХОД < 0 {
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
	memorijamanager := &mem.TMemorijamanager{}
	датотекаPokazivač := memorijamanager.Malloc(величина)
	if датотекаPokazivač == nil {
		return Einval
	}
	data := GetBajtovasaPokazivač(uintptr(датотекаPokazivač), int(величина), int(величина))
	читањеДатотека(назив[:називlen], data)
	if величина < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorijamanager.Slobodno(датотекаPokazivač)
		return Enoexec
	}
	loader := Elf{}
	унос := loader.Getунос(data)
	loader.Parse(data, getcr3())
	memorijamanager.Slobodno(датотекаPokazivač)
	if иСХОД := setupizvršnastack(процесор, &argumenti_2, &environment); иСХОД < 0 {
		return иСХОД
	}
	затвориnaizvršna(ensureТренутноПроцес())
	процесор.Eip = унос
	процесор.Eax = 0
	return 0
}

func sysfork(процесор *TcpuСтање) int32 {
	nadređeniПИД := ТренутноПИД()
	if ensureТренутноПроцес() == nil {
		return Enfile
	}
	пИД := allocateПроцес(nadređeniПИД)
	if пИД == 0 {
		return Einval
	}
	memorijamanager := &mem.TMemorijamanager{}
	threadPokazivač := memorijamanager.Malloc(uint32(Sizeof(TThread{})))
	stackPokazivač := memorijamanager.Malloc(ThreadstackВеличина)
	sadržanilistDirektorijum := Cloneaddressrazmakcow(getcr3())
	if threadPokazivač == nil || stackPokazivač == nil || sadržanilistDirektorijum == 0 {
		odbaciПроцес(пИД)
		return Einval
	}
	sadržani := (*TThread)(threadPokazivač)
	sadržani.Stack = uint32(uintptr(stackPokazivač))
	sadržani.ПроцесорСтање = (*TcpuСтање)(Pointer(uintptr(stackPokazivač) + ThreadstackВеличина - Sizeof(TcpuСтање{})))
	*sadržani.ПроцесорСтање = *процесор
	sadržani.ПроцесорСтање.Eax = 0
	sadržani.Korisnikstack_2 = процесор.Esp
	sadržani.KorisnikstackВеличина_2 = 0
	sadržani.ПИД = пИД
	sadržani.NadređeniПИД = nadređeniПИД
	sadržani.ListDirektorijumунос = sadržanilistDirektorijum
	sadržani.ThreadСтање = Спреман
	sadržani.Fpuoffset = 0xffffffff
	sadržani.Iskernel = false
	Додајrunnablethread(sadržani)
	return int32(пИД)
}

func sysIzlaz(стање uint32) {
	пИД := ТренутноПИД()
	for i := 0; i < len(процесTabela); i++ {
		if процесTabela[i].zauzeto_2 && процесTabela[i].пИД == пИД {
			затвориSveПроцесfds(&процесTabela[i])
			процесTabela[i].изашаосам = true
			процесTabela[i].стање = (стање & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(пИД int32, стањеaddress uint32, опције uint32) int32 {
	if (опције & ^uint32(1)) != 0 {
		return Einval
	}
	nadređeniПИД := ТренутноПИД()
	foundsadržani := false
	for i := 0; i < len(процесTabela); i++ {
		p := &процесTabela[i]
		matches := пИД == -1 || пИД == 0 || p.пИД == uint32(пИД)
		if p.zauzeto_2 && matches && p.nadređeni == nadređeniПИД {
			foundsadržani = true
			if p.изашаосам {
				if стањеaddress != 0 {
					*(*uint32)(Pointer(uintptr(стањеaddress))) = p.стање
				}
				sadržaniПИД := p.пИД
				*p = процесунос{}
				return int32(sadržaniПИД)
			}
		}
	}
	if !foundsadržani {
		return Echild
	}

	if (опције & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateПроцес(nadređeni uint32) uint32 {
	nadređeniПроцес := pronađiПроцес(nadređeni)
	пИД := AllocateПИД()
	for i := 0; i < len(процесTabela); i++ {
		if !процесTabela[i].zauzeto_2 {
			процесTabela[i] = процесунос{
				zauzeto_2:	true,
				пИД:		пИД,
				nadređeni:	nadređeni,
				програмbreak:	korisnikheapbase,
			}
			if nadređeniПроцес != nil {
				процесTabela[i].програмbreak = nadređeniПроцес.програмbreak
				for описник := 0; описник < максОписник; описник++ {
					if nadređeniПроцес.fds[описник].zauzeto_2 {
						процесTabela[i].fds[описник] = nadređeniПроцес.fds[описник]
						опис := nadređeniПроцес.fds[описник].опис
						if опис >= 0 && опис < максОтвориDATOTEKE {
							отвориДатотекаTabela[опис].refs++
						}
					}
				}
			} else {
				initializeПроцесfds(&процесTabela[i])
			}
			return пИД
		}
	}
	return 0
}

func затвориSveПроцесfds(процес *процесунос) {
	if процес == nil {
		return
	}
	for описник := int32(0); описник < максОписник; описник++ {
		if процес.fds[описник].zauzeto_2 {
			затвориПроцесОписник(процес, описник)
		}
	}
}

func odbaciПроцес(пИД uint32) {
	процес := pronađiПроцес(пИД)
	if процес == nil {
		return
	}
	затвориSveПроцесfds(процес)
	*процес = процесунос{}
}

func умножиПУТАЊА(пУТАЊАaddress uint32) (uint32, [12]byte) {
	var назив [12]byte
	if пУТАЊАaddress == 0 {
		return 0, назив
	}
	raw := GetBajtovasaPokazivač(uintptr(пУТАЊАaddress), 64, 64)
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

	partition := TmsdospartitionTabela{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	величина := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], датотека)
	ata0s.Flush()
	return величина
}

func читањеДатотека(датотека []byte, data []byte) {
	var ata0s = TНапредноТехнологијаattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Читањеpartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Читање(&ata0s, partition.Mbr.Primarypartition[0], датотека, data)
	ata0s.Flush()
}

func getcr3() uint32
