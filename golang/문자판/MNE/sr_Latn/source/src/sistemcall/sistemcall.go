package sistemcall

import . "unsafe"

import . "ometanje"
import . "konzola"
import . "util"
import . "multitasking"
import . "driver/ata"
import . "datotekaSistem/msdospartition"
import . "datotekaSistem/fat"
import . "datotekaSistem/elf"
import mem "memorijamanager"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/thread"
import . "virtuelnoMemorija"

var konzola_2 = TKonzola{}

type TSyscall struct {
	TOmetanjehandler
}

const (
	SysIzlaz	uint32	= 1
	Sysfork		uint32	= 2
	Sysčitanje	uint32	= 3
	SysPiše		uint32	= 4
	SysOtvori	uint32	= 5
	SysZatvori	uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Syspristupanje	uint32	= 33
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
	stdinOpisnik		int32	= 0
	stdoutOpisnik		int32	= 1
	stderrOpisnik		int32	= 2
	maksOpisnik			= 32
	maksOtvoriDATOTEKE		= 128
)

type opisnikunos struct {
	zauzeto_2		bool
	opis			int32
	opisnikParametri	uint32
}

type otvoriDatotekaOpis struct {
	zauzeto_2	bool
	refs		uint32
	vrsta		uint32
	parametri	uint32
	položaj		uint32
	veličina	uint32
	naziv		[12]byte
	nazivlen	uint32
	aux		uint32
}

const (
	opisnikvrstaNišta		uint32	= 0
	opisnikvrstafat			uint32	= 1
	opisnikvrstastdin		uint32	= 2
	opisnikvrstaKonzola		uint32	= 3
	opisnikvrstaKorenDirektorijum	uint32	= 4
	opisnikvrstaPriključnica		uint32	= 5

	očitanjeonly	uint32	= 0
	oPišeonly	uint32	= 1
	očitanjePiše	uint32	= 2
	ocreate		uint32	= 0x40
	oOdsecite	uint32	= 0x200
	oappend		uint32	= 0x400
	oDirektorijum	uint32	= 0x10000

	seekskup	uint32	= 0
	seekTrenutno	uint32	= 1
	seekKraj	uint32	= 2

	fdupOpisnik	uint32	= 0
	fgetOpisnik	uint32	= 1
	fskupOpisnik	uint32	= 2
	fgetfl		uint32	= 3
	fskupfl		uint32	= 4
	opisnikcloexec	uint32	= 1

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
	makssockets		= 32
	maksPriključnicapaketa	= 8
	maksdatagramVeličina	= 512
)

type priključnicaaddressiTrevr4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type priključnicapacket struct {
	zauzeto_2	bool
	veličina	uint32
	izvor		priključnicaaddressiTrevr4
	data		[maksdatagramVeličina]byte
}

type lokalnadatagramPriključnica struct {
	zauzeto_2	bool
	bound		bool
	connected	bool
	lokalna		priključnicaaddressiTrevr4
	udaljeno		priključnicaaddressiTrevr4
	head		uint32
	tail		uint32
	count		uint32
	paketa		[maksPriključnicapaketa]priključnicapacket
}

type posixstat struct {
	Uređaj		uint32
	Ino		uint32
	REŽIM		uint32
	Nlink		uint32
	JLB		uint32
	Gid		uint32
	Rdev		uint32
	Veličina_2	int32
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
	Izdanje		[65]byte
	Machine		[65]byte
}

const (
	maksizvršnavectorunos	= 16
	maksizvršnaniskaDužina	= 63
)

type izvršnavector struct {
	count		uint32
	lengths		[maksizvršnavectorunos]uint32
	vrednosti	[maksizvršnavectorunos][maksizvršnaniskaDužina + 1]byte
}

type procesunos struct {
	zauzeto_2	bool
	pID		uint32
	nadređeni	uint32
	izašaosam	bool
	stanje		uint32
	programbreak	uint32
	fds		[maksOpisnik]opisnikunos
}

type niskaheader struct {
	Data	uintptr
	Len	int
}

func syscallGreška(greška int32) uint32 {
	return *(*uint32)(Pointer(&greška))
}

var otvoriDatotekaTabela [maksOtvoriDATOTEKE]otvoriDatotekaOpis
var procesTabela [32]procesunos
var lokalnasockets [makssockets]lokalnadatagramPriključnica
var sledećeephemeralPort uint16 = 49152

const (
	korisnikheapbase	uint32	= 0x06000000
	korisnikheapOgraniči	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinčitanje uint32
var stdinPiše uint32

func Ometanje(eax, ebx, ecx, edx, esi, edi uint32) uint32

func SysIzlaz_2(popis uint32) {
	Syscall(SysIzlaz, popis)
}

func Sysčitanje_2(opisnik uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysčitanje, opisnik, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func SysŠtampajstr(buffer string) {
	h := (*niskaheader)(Pointer(&buffer))
	Syscall(SysPiše, uint32(stdoutOpisnik), uint32(h.Data), uint32(h.Len))
}

func SysŠtampajunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(SysPiše, uint32(stdoutOpisnik), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func SysOtvori_2(pUTANjA uintptr, parametri uint32, rEŽIM uint32) int32 {
	return int32(Syscall(SysOtvori, uint32(pUTANjA), parametri, rEŽIM))
}

func SysZatvori_2(opisnik uint32) int32 {
	return int32(Syscall(SysZatvori, opisnik))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(parametri_2 ...uint32) uint32 {

	l := len(parametri_2)
	switch l {
	case 1:
		return Ometanje(parametri_2[0], 0, 0, 0, 0, 0)
	case 2:
		return Ometanje(parametri_2[0], parametri_2[1], 0, 0, 0, 0)
	case 3:
		return Ometanje(parametri_2[0], parametri_2[1], parametri_2[2], 0, 0, 0)
	case 4:
		return Ometanje(parametri_2[0], parametri_2[1], parametri_2[2], parametri_2[3], 0, 0)
	case 5:
		return Ometanje(parametri_2[0], parametri_2[1], parametri_2[2], parametri_2[3], parametri_2[4], 0)
	case 6:
		return Ometanje(parametri_2[0], parametri_2[1], parametri_2[2], parametri_2[3], parametri_2[4], parametri_2[5])
	default:
		return syscallGreška(Enosys)
	}
}

func (isti *TSyscall) Init(manager *TOmetanjemanager) {
	initDatotekadescriptor()

	ometanjehandler = ručkaOmetanje

	var address uintptr
	address = uintptr(Pointer(&ometanjehandler))

	isti.TOmetanjehandler.Init(0x80, uintptr(Pointer(manager)), address)
}

var ometanjehandler func(uint32) uint32

func ručkaOmetanje(esp uint32) uint32 {
	var procesor = (*TcpuStanje)(Pointer(uintptr(esp)))

	switch procesor.Eax {
	case SysIzlaz:
		sysIzlaz(procesor.Ebx)
		return uint32(uintptr(Pointer(ZaustaviTrenutnothread(procesor))))
	case SysrtIzlaz:
		sysIzlaz(procesor.Ebx)
		return uint32(uintptr(Pointer(ZaustaviTrenutnothread(procesor))))
	case Sysfork:
		procesor.Eax = uint32(sysfork(procesor))
		return esp
	case Sysčitanje:
		procesor.Eax = uint32(sysčitanje(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysPiše:
		procesor.Eax = uint32(sysPiše(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case SysOtvori:
		procesor.Eax = uint32(sysOtvori(procesor.Ebx, procesor.Ecx, procesor.Edx))
		return esp
	case Syscreat:
		procesor.Eax = uint32(sysOtvori(procesor.Ebx, ocreate|oPišeonly|oOdsecite, procesor.Ecx))
		return esp
	case SysZatvori:
		procesor.Eax = uint32(sysZatvori(int32(procesor.Ebx)))
		return esp
	case Syswaitpid:
		procesor.Eax = uint32(syswaitpid(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Syslseek:
		procesor.Eax = uint32(syslseek(int32(procesor.Ebx), int32(procesor.Ecx), procesor.Edx))
		return esp
	case Sysexecve:
		procesor.Eax = uint32(sysexecve(procesor, procesor.Ebx))
		return esp
	case Sysgetpid:
		procesor.Eax = TrenutnoPID()
		return esp
	case Sysgetppid:
		procesor.Eax = TrenutnonadređeniPID()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		procesor.Eax = 0
		return esp
	case Syspristupanje:
		procesor.Eax = uint32(syspristupanje(procesor.Ebx, procesor.Ecx))
		return esp
	case Syschdir:
		procesor.Eax = uint32(syschdir(procesor.Ebx))
		return esp
	case Sysgetcwd:
		procesor.Eax = uint32(sysgetcwd(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysdup:
		procesor.Eax = uint32(sysdup(int32(procesor.Ebx), 0))
		return esp
	case Sysdup2:
		procesor.Eax = uint32(sysdup2(int32(procesor.Ebx), int32(procesor.Ecx)))
		return esp
	case Syssocketcall:
		procesor.Eax = uint32(sysPriključnicacall(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfcntl:
		procesor.Eax = uint32(sysfcntl(int32(procesor.Ebx), procesor.Ecx, procesor.Edx))
		return esp
	case Sysstat, Syslstat:
		procesor.Eax = uint32(sysstat(procesor.Ebx, procesor.Ecx))
		return esp
	case Sysfstat:
		procesor.Eax = uint32(sysfstat(int32(procesor.Ebx), procesor.Ecx))
		return esp
	case Sysfsync:
		procesor.Eax = uint32(sysfsync(int32(procesor.Ebx)))
		return esp
	case Syssync:
		procesor.Eax = 0
		return esp
	case Sysuname:
		procesor.Eax = uint32(sysuname(procesor.Ebx))
		return esp
	case Sysbrk:
		procesor.Eax = sysbrk(procesor.Ebx)
		return esp
	case 9:
		konzola_2.MUnsignedinteger32Štampaj(procesor.Ebx)
		return esp

	default:
		konzola_2.MŠtampajxy(([]byte)("sys["), 1, 23)
		konzola_2.MUnsignedinteger32Štampaj(esp)
		konzola_2.MŠtampaj(([]byte)(":"))
		konzola_2.MUnsignedinteger32Štampaj(procesor.Eax)
		konzola_2.MŠtampaj(([]byte)(":"))
		konzola_2.MUnsignedinteger32Štampaj(procesor.Ebx)
		konzola_2.MŠtampaj(([]byte)(":"))
		konzola_2.MUnsignedinteger32Štampaj(procesor.Ecx)
		konzola_2.MŠtampaj(([]byte)(":"))
		konzola_2.MUnsignedinteger32Štampaj(procesor.Edx)
		konzola_2.MŠtampaj(([]byte)("]"))
		procesor.Eax = syscallGreška(Enosys)
		return esp
	}

	return esp
}

func initDatotekadescriptor() {
	for i := 0; i < maksOtvoriDATOTEKE; i++ {
		otvoriDatotekaTabela[i] = otvoriDatotekaOpis{}
	}
	for i := 0; i < len(procesTabela); i++ {
		procesTabela[i] = procesunos{}
	}
	for i := 0; i < len(lokalnasockets); i++ {
		lokalnasockets[i] = lokalnadatagramPriključnica{}
	}
	sledećeephemeralPort = 49152
	otvoriDatotekaTabela[0] = otvoriDatotekaOpis{zauzeto_2: true, vrsta: opisnikvrstastdin, parametri: očitanjeonly}
	otvoriDatotekaTabela[1] = otvoriDatotekaOpis{zauzeto_2: true, vrsta: opisnikvrstaKonzola, parametri: oPišeonly}
	otvoriDatotekaTabela[2] = otvoriDatotekaOpis{zauzeto_2: true, vrsta: opisnikvrstaKonzola, parametri: oPišeonly}
}

func nađiProces(pID uint32) *procesunos {
	for i := 0; i < len(procesTabela); i++ {
		if procesTabela[i].zauzeto_2 && procesTabela[i].pID == pID {
			return &procesTabela[i]
		}
	}
	return nil
}

func initializeProcesfds(proces *procesunos) {
	for opisnik := int32(0); opisnik <= stderrOpisnik; opisnik++ {
		proces.fds[opisnik] = opisnikunos{zauzeto_2: true, opis: opisnik}
		otvoriDatotekaTabela[opisnik].refs++
	}
}

func ensureTrenutnoProces() *procesunos {
	pID := TrenutnoPID()
	if proces := nađiProces(pID); proces != nil {
		return proces
	}
	for i := 0; i < len(procesTabela); i++ {
		if !procesTabela[i].zauzeto_2 {
			procesTabela[i] = procesunos{
				zauzeto_2:	true,
				pID:		pID,
				nadređeni:	TrenutnonadređeniPID(),
				programbreak:	korisnikheapbase,
			}
			initializeProcesfds(&procesTabela[i])
			return &procesTabela[i]
		}
	}
	return nil
}

func getOtvoriDatotekafor(proces *procesunos, opisnik int32) *otvoriDatotekaOpis {
	if proces == nil || opisnik < 0 || opisnik >= maksOpisnik || !proces.fds[opisnik].zauzeto_2 {
		return nil
	}
	opis := proces.fds[opisnik].opis
	if opis < 0 || opis >= maksOtvoriDATOTEKE || !otvoriDatotekaTabela[opis].zauzeto_2 {
		return nil
	}
	return &otvoriDatotekaTabela[opis]
}

func getOtvoriDatoteka(opisnik int32) *otvoriDatotekaOpis {
	return getOtvoriDatotekafor(ensureTrenutnoProces(), opisnik)
}

func allocateOtvoriDatoteka() int32 {
	for i := int32(3); i < maksOtvoriDATOTEKE; i++ {
		if !otvoriDatotekaTabela[i].zauzeto_2 {
			otvoriDatotekaTabela[i] = otvoriDatotekaOpis{zauzeto_2: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocateOpisnik(proces *procesunos, opis int32, najtiše int32) int32 {
	if proces == nil {
		return Enfile
	}
	if najtiše < 0 || najtiše >= maksOpisnik {
		return Einval
	}
	for opisnik := najtiše; opisnik < maksOpisnik; opisnik++ {
		if !proces.fds[opisnik].zauzeto_2 {
			proces.fds[opisnik] = opisnikunos{zauzeto_2: true, opis: opis}
			return opisnik
		}
	}
	return Emfile
}

func releaseOtvoriDatoteka(opis int32) {
	if opis < 0 || opis >= maksOtvoriDATOTEKE {
		return
	}
	unos := &otvoriDatotekaTabela[opis]
	if unos.refs > 0 {
		unos.refs--
	}

	if unos.refs == 0 && opis > stderrOpisnik {
		if unos.vrsta == opisnikvrstaPriključnica && unos.aux < makssockets {
			lokalnasockets[unos.aux] = lokalnadatagramPriključnica{}
		}
		*unos = otvoriDatotekaOpis{}
	}
}

func zatvoriProcesOpisnik(proces *procesunos, opisnik int32) int32 {
	if proces == nil || getOtvoriDatotekafor(proces, opisnik) == nil {
		return Ebadf
	}
	opis := proces.fds[opisnik].opis
	proces.fds[opisnik] = opisnikunos{}
	releaseOtvoriDatoteka(opis)
	return 0
}

func sysPiše(opisnik int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	if count > 4096 {
		return Einval
	}
	unos := getOtvoriDatoteka(opisnik)
	if unos == nil {
		return Ebadf
	}
	if unos.vrsta != opisnikvrstaKonzola {
		if unos.vrsta == opisnikvrstaPriključnica {
			return priključnicaPošaljito(opisnik, address, count, 0, 0)
		}
		if unos.vrsta == opisnikvrstafat || unos.vrsta == opisnikvrstaKorenDirektorijum {
			return Erofs
		}
		return Ebadf
	}
	buffer := GetBajtovasaPokazivač(uintptr(address), int(count), int(count))
	konzola_2.MŠtampaj(buffer)
	return int32(count)
}

func sysčitanje(opisnik int32, address uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if address == 0 || address+count < address {
		return Efault
	}
	unos := getOtvoriDatoteka(opisnik)
	if unos == nil {
		return Ebadf
	}
	if unos.vrsta == opisnikvrstastdin {
		return čitanjestdin(address, count)
	}
	if unos.vrsta == opisnikvrstaKorenDirektorijum {
		return Eisdir
	}
	if unos.vrsta == opisnikvrstaPriključnica {
		return priključnicareceivesa(opisnik, address, count, 0, 0)
	}
	if unos.vrsta != opisnikvrstafat {
		return Ebadf
	}
	if unos.položaj >= unos.veličina {
		return 0
	}
	remaining := unos.veličina - unos.položaj
	if count > remaining {
		count = remaining
	}
	buffer := GetBajtovasaPokazivač(uintptr(address), int(count), int(count))
	return čitanjevfsDatoteka(unos, buffer, count)
}

func sysOtvori(pUTANjAaddress uint32, parametri uint32, rEŽIM uint32) int32 {
	_ = rEŽIM
	if pUTANjAaddress == 0 {
		return Efault
	}
	pristupanjeREŽIM := parametri & 3
	if pristupanjeREŽIM == oPišeonly || pristupanjeREŽIM == očitanjePiše || (parametri&(ocreate|oOdsecite|oappend)) != 0 {
		return Erofs
	}

	proces := ensureTrenutnoProces()
	if proces == nil {
		return Enfile
	}
	opis := allocateOtvoriDatoteka()
	if opis < 0 {
		return opis
	}
	unos := &otvoriDatotekaTabela[opis]
	unos.parametri = parametri
	if isKorenPUTANjA(pUTANjAaddress) {
		unos.vrsta = opisnikvrstaKorenDirektorijum
		unos.veličina = 0
	} else {
		nazivlen, naziv := umnožiPUTANjA(pUTANjAaddress)
		if nazivlen == 0 {
			*unos = otvoriDatotekaOpis{}
			return Enoent
		}
		veličina := datotekaVeličina(naziv[:nazivlen])
		if veličina == 0 {
			*unos = otvoriDatotekaOpis{}
			return Enoent
		}
		if (parametri & oDirektorijum) != 0 {
			*unos = otvoriDatotekaOpis{}
			return Enotdir
		}
		unos.vrsta = opisnikvrstafat
		unos.veličina = veličina
		unos.nazivlen = nazivlen
		unos.naziv = naziv
	}

	opisnik := allocateOpisnik(proces, opis, 3)
	if opisnik < 0 {
		*unos = otvoriDatotekaOpis{}
		return opisnik
	}
	return opisnik
}

func sysZatvori(opisnik int32) int32 {
	return zatvoriProcesOpisnik(ensureTrenutnoProces(), opisnik)
}

func sysdup(opisnik int32, najtiše int32) int32 {
	proces := ensureTrenutnoProces()
	unos := getOtvoriDatotekafor(proces, opisnik)
	if unos == nil {
		return Ebadf
	}
	novaOpisnik := allocateOpisnik(proces, proces.fds[opisnik].opis, najtiše)
	if novaOpisnik >= 0 {
		unos.refs++
	}
	return novaOpisnik
}

func sysdup2(oldOpisnik int32, novaOpisnik int32) int32 {
	proces := ensureTrenutnoProces()
	unos := getOtvoriDatotekafor(proces, oldOpisnik)
	if unos == nil {
		return Ebadf
	}
	if novaOpisnik < 0 || novaOpisnik >= maksOpisnik {
		return Ebadf
	}
	if oldOpisnik == novaOpisnik {
		return novaOpisnik
	}
	if proces.fds[novaOpisnik].zauzeto_2 {
		zatvoriProcesOpisnik(proces, novaOpisnik)
	}
	proces.fds[novaOpisnik] = opisnikunos{zauzeto_2: true, opis: proces.fds[oldOpisnik].opis}
	unos.refs++
	return novaOpisnik
}

func sysfcntl(opisnik int32, naredba uint32, argument uint32) int32 {
	proces := ensureTrenutnoProces()
	unos := getOtvoriDatotekafor(proces, opisnik)
	if unos == nil {
		return Ebadf
	}
	switch naredba {
	case fdupOpisnik:
		return sysdup(opisnik, int32(argument))
	case fgetOpisnik:
		return int32(proces.fds[opisnik].opisnikParametri)
	case fskupOpisnik:
		proces.fds[opisnik].opisnikParametri = argument & opisnikcloexec
		return 0
	case fgetfl:
		return int32(unos.parametri)
	case fskupfl:
		unos.parametri = (unos.parametri & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(opisnik int32, offset int32, whence uint32) int32 {
	unos := getOtvoriDatoteka(opisnik)
	if unos == nil {
		return Ebadf
	}
	if unos.vrsta != opisnikvrstafat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekskup:
		base = 0
	case seekTrenutno:
		base = int64(unos.položaj)
	case seekKraj:
		base = int64(unos.veličina)
	default:
		return Einval
	}
	položaj_2 := base + int64(offset)
	if položaj_2 < 0 || položaj_2 > 0x7FFFFFFF {
		return Einval
	}
	unos.položaj = uint32(položaj_2)
	return int32(unos.položaj)
}

func čitanjevfsDatoteka(unos *otvoriDatotekaOpis, odredište_2 []byte, count uint32) int32 {
	memorijamanager := &mem.TMemorijamanager{}
	tmpPokazivač := memorijamanager.Malloc(unos.veličina)
	if tmpPokazivač == nil {
		return Einval
	}
	tmp := GetBajtovasaPokazivač(uintptr(tmpPokazivač), int(unos.veličina), int(unos.veličina))
	čitanjeDatoteka(unos.naziv[:unos.nazivlen], tmp)
	copy(odredište_2[:count], tmp[unos.položaj:unos.položaj+count])
	unos.položaj += count
	memorijamanager.Slobodno(tmpPokazivač)
	return int32(count)
}

func isKorenPUTANjA(pUTANjAaddress uint32) bool {
	if pUTANjAaddress == 0 {
		return false
	}
	pUTANjA := GetBajtovasaPokazivač(uintptr(pUTANjAaddress), 4, 4)
	if pUTANjA[0] == '/' && pUTANjA[1] == 0 {
		return true
	}
	if pUTANjA[0] == '.' && pUTANjA[1] == 0 {
		return true
	}
	if pUTANjA[0] == '/' && pUTANjA[1] == '.' && pUTANjA[2] == 0 {
		return true
	}
	return false
}

func syspristupanje(pUTANjAaddress uint32, rEŽIM uint32) int32 {
	if pUTANjAaddress == 0 {
		return Efault
	}
	if (rEŽIM & ^uint32(7)) != 0 {
		return Einval
	}
	isKoren := isKorenPUTANjA(pUTANjAaddress)
	exists := isKoren
	if !exists {
		nazivlen, naziv := umnožiPUTANjA(pUTANjAaddress)
		exists = nazivlen != 0 && datotekaVeličina(naziv[:nazivlen]) != 0
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

func syschdir(pUTANjAaddress uint32) int32 {
	if pUTANjAaddress == 0 {
		return Efault
	}
	if !isKorenPUTANjA(pUTANjAaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, veličina uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if veličina < 2 {
		return Erange
	}
	buffer_2 := GetBajtovasaPokazivač(uintptr(bufferaddress), int(veličina), int(veličina))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, rEŽIM uint32, veličina uint32, ičvor uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Uređaj = 1
	stat.Ino = ičvor
	stat.REŽIM = rEŽIM
	stat.Nlink = 1
	stat.Veličina_2 = int32(veličina)
	stat.Blksize = 512
	stat.Blok = int32((veličina + 511) / 512)
	return 0
}

func sysstat(pUTANjAaddress uint32, stataddress uint32) int32 {
	if pUTANjAaddress == 0 {
		return Efault
	}
	if isKorenPUTANjA(pUTANjAaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	nazivlen, naziv := umnožiPUTANjA(pUTANjAaddress)
	if nazivlen == 0 {
		return Enoent
	}
	veličina := datotekaVeličina(naziv[:nazivlen])
	if veličina == 0 {
		return Enoent
	}
	ičvor := uint32(2)
	for i := uint32(0); i < nazivlen; i++ {
		ičvor = ičvor*33 + uint32(naziv[i])
	}
	return fillposixstat(stataddress, sifreg|0444, veličina, ičvor)
}

func sysfstat(opisnik int32, stataddress uint32) int32 {
	unos := getOtvoriDatoteka(opisnik)
	if unos == nil {
		return Ebadf
	}
	switch unos.vrsta {
	case opisnikvrstastdin, opisnikvrstaKonzola:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(opisnik+1))
	case opisnikvrstaKorenDirektorijum:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case opisnikvrstafat:
		return fillposixstat(stataddress, sifreg|0444, unos.veličina, uint32(opisnik+2))
	case opisnikvrstaPriključnica:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(opisnik+2))
	}
	return Ebadf
}

func sysfsync(opisnik int32) int32 {
	if getOtvoriDatoteka(opisnik) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	proces := ensureTrenutnoProces()
	if proces == nil {
		return 0
	}
	if proces.programbreak == 0 {
		proces.programbreak = korisnikheapbase
	}
	if address_2 == 0 {
		return proces.programbreak
	}
	if address_2 < korisnikheapbase || address_2 > korisnikheapOgraniči {
		return proces.programbreak
	}
	proces.programbreak = address_2
	return proces.programbreak
}

func umnožiutspolje(odredište *[65]byte, vrednost string) {
	ograniči := len(vrednost)
	if ograniči > 64 {
		ograniči = 64
	}
	for i := 0; i < ograniči; i++ {
		odredište[i] = vrednost[i]
	}
	odredište[ograniči] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	naziv := (*posixutsname)(Pointer(uintptr(address_2)))
	*naziv = posixutsname{}
	umnožiutspolje(&naziv.Sysname, "EngOS")
	umnožiutspolje(&naziv.Nodename, "engos")
	umnožiutspolje(&naziv.Release, "0.1-posix")
	umnožiutspolje(&naziv.Izdanje, "POSIX.1-2017 phase 1")
	umnožiutspolje(&naziv.Machine, "i386")
	return 0
}

func virtuelnamemorijaunsignedinteger16(vrednost uint16) uint16 {
	return (vrednost << 8) | (vrednost >> 8)
}

func priključnicacallargument(argumenti_2 uint32, popis uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(argumenti_2 + popis*4)))
}

func priključnicaforOpisnik(opisnik int32) (*lokalnadatagramPriključnica, int32) {
	unos := getOtvoriDatoteka(opisnik)
	if unos == nil || unos.vrsta != opisnikvrstaPriključnica || unos.aux >= makssockets {
		return nil, Ebadf
	}
	priključnica := &lokalnasockets[unos.aux]
	if !priključnica.zauzeto_2 {
		return nil, Ebadf
	}
	return priključnica, 0
}

func allocatePriključnica(domen uint32, priključnicaVrsta uint32, protocol uint32) int32 {
	if domen != afinet {
		return Eafnosupport
	}
	if priključnicaVrsta != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	proces := ensureTrenutnoProces()
	if proces == nil {
		return Enfile
	}
	priključnicaPopis := -1
	for i := 0; i < makssockets; i++ {
		if !lokalnasockets[i].zauzeto_2 {
			priključnicaPopis = i
			break
		}
	}
	if priključnicaPopis < 0 {
		return Enfile
	}
	opis := allocateOtvoriDatoteka()
	if opis < 0 {
		return opis
	}
	lokalnasockets[priključnicaPopis] = lokalnadatagramPriključnica{zauzeto_2: true}
	unos := &otvoriDatotekaTabela[opis]
	unos.vrsta = opisnikvrstaPriključnica
	unos.parametri = očitanjePiše
	unos.aux = uint32(priključnicaPopis)
	opisnik := allocateOpisnik(proces, opis, 3)
	if opisnik < 0 {
		lokalnasockets[priključnicaPopis] = lokalnadatagramPriključnica{}
		*unos = otvoriDatotekaOpis{}
		return opisnik
	}
	return opisnik
}

func priključnicaaddress(address_2 uint32, dužina uint32) (*priključnicaaddressiTrevr4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if dužina < 16 {
		return nil, Einval
	}
	iSHOD := (*priključnicaaddressiTrevr4)(Pointer(uintptr(address_2)))
	if iSHOD.Family != afinet {
		return nil, Eafnosupport
	}
	return iSHOD, 0
}

func portPrimljenoKoristi(port uint16, except *lokalnadatagramPriključnica) bool {
	for i := 0; i < makssockets; i++ {
		priključnica := &lokalnasockets[i]
		if priključnica != except && priključnica.zauzeto_2 && priključnica.bound && priključnica.lokalna.Port == port {
			return true
		}
	}
	return false
}

func bindephemeral(priključnica *lokalnadatagramPriključnica) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := virtuelnamemorijaunsignedinteger16(sledećeephemeralPort)
		sledećeephemeralPort++
		if sledećeephemeralPort < 49152 {
			sledećeephemeralPort = 49152
		}
		if !portPrimljenoKoristi(port, priključnica) {
			priključnica.lokalna = priključnicaaddressiTrevr4{Family: afinet, Port: port, Address: 0x0100007F}
			priključnica.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func priključnicabind(opisnik int32, address_2 uint32, dužina uint32) int32 {
	priključnica, greška := priključnicaforOpisnik(opisnik)
	if greška != 0 {
		return greška
	}
	requested, greška := priključnicaaddress(address_2, dužina)
	if greška != 0 {
		return greška
	}
	if priključnica.bound {
		return Einval
	}
	if requested.Port == 0 {
		return bindephemeral(priključnica)
	}
	if portPrimljenoKoristi(requested.Port, priključnica) {
		return Eaddrinuse
	}
	priključnica.lokalna = *requested
	priključnica.bound = true
	return 0
}

func priključnicaPovežise(opisnik int32, address_2 uint32, dužina uint32) int32 {
	priključnica, greška := priključnicaforOpisnik(opisnik)
	if greška != 0 {
		return greška
	}
	udaljeno, greška := priključnicaaddress(address_2, dužina)
	if greška != 0 {
		return greška
	}
	if !priključnica.bound {
		if greška := bindephemeral(priključnica); greška != 0 {
			return greška
		}
	}
	priključnica.udaljeno = *udaljeno
	priključnica.connected = true
	return 0
}

func priključnicaPošaljito(opisnik int32, bufferaddress_2 uint32, dužina uint32, odredišteaddress uint32, odredišteDužina uint32) int32 {
	priključnica, greška := priključnicaforOpisnik(opisnik)
	if greška != 0 {
		return greška
	}
	if dužina > maksdatagramVeličina {
		return Emsgsize
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var odredište priključnicaaddressiTrevr4
	if odredišteaddress != 0 {
		address_2, addressGreška := priključnicaaddress(odredišteaddress, odredišteDužina)
		if addressGreška != 0 {
			return addressGreška
		}
		odredište = *address_2
	} else {
		if !priključnica.connected {
			return Enotconn
		}
		odredište = priključnica.udaljeno
	}
	if !priključnica.bound {
		if bindGreška := bindephemeral(priključnica); bindGreška != 0 {
			return bindGreška
		}
	}
	var receiver *lokalnadatagramPriključnica
	for i := 0; i < makssockets; i++ {
		candidate := &lokalnasockets[i]
		if candidate.zauzeto_2 && candidate.bound && candidate.lokalna.Port == odredište.Port &&
			(candidate.lokalna.Address == 0 || candidate.lokalna.Address == odredište.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.count >= maksPriključnicapaketa {
		return Eagain
	}
	packet := &receiver.paketa[receiver.tail]
	*packet = priključnicapacket{zauzeto_2: true, veličina: dužina, izvor: priključnica.lokalna}
	if dužina != 0 {
		izvor := GetBajtovasaPokazivač(uintptr(bufferaddress_2), int(dužina), int(dužina))
		copy(packet.data[:dužina], izvor)
	}
	receiver.tail = (receiver.tail + 1) % maksPriključnicapaketa
	receiver.count++
	return int32(dužina)
}

func priključnicareceivesa(opisnik int32, bufferaddress_2 uint32, dužina uint32, izvoraddress uint32, izvorDužinaaddress uint32) int32 {
	priključnica, greška := priključnicaforOpisnik(opisnik)
	if greška != 0 {
		return greška
	}
	if dužina != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if priključnica.count == 0 {
		return Eagain
	}
	packet := &priključnica.paketa[priključnica.head]
	umnožiDužina := packet.veličina
	if umnožiDužina > dužina {
		umnožiDužina = dužina
	}
	if umnožiDužina != 0 {
		odredište := GetBajtovasaPokazivač(uintptr(bufferaddress_2), int(umnožiDužina), int(umnožiDužina))
		copy(odredište, packet.data[:umnožiDužina])
	}
	if izvoraddress != 0 {
		if izvorDužinaaddress == 0 {
			return Efault
		}
		providedDužina := (*uint32)(Pointer(uintptr(izvorDužinaaddress)))
		if *providedDužina >= 16 {
			*(*priključnicaaddressiTrevr4)(Pointer(uintptr(izvoraddress))) = packet.izvor
		}
		*providedDužina = 16
	}
	*packet = priključnicapacket{}
	priključnica.head = (priključnica.head + 1) % maksPriključnicapaketa
	priključnica.count--
	return int32(umnožiDužina)
}

func umnožiPriključnicaNaziv(opisnik int32, address_2 uint32, dužinaaddress uint32, peer bool) int32 {
	priključnica, greška := priključnicaforOpisnik(opisnik)
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
		if !priključnica.connected {
			return Enotconn
		}
		*(*priključnicaaddressiTrevr4)(Pointer(uintptr(address_2))) = priključnica.udaljeno
	} else {
		if !priključnica.bound {
			if bindGreška := bindephemeral(priključnica); bindGreška != 0 {
				return bindGreška
			}
		}
		*(*priključnicaaddressiTrevr4)(Pointer(uintptr(address_2))) = priključnica.lokalna
	}
	*dužina = 16
	return 0
}

func sysPriključnicacall(call uint32, argumenti_2 uint32) int32 {
	if argumenti_2 == 0 {
		return Efault
	}
	switch call {
	case 1:
		return allocatePriključnica(priključnicacallargument(argumenti_2, 0), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2))
	case 2:
		return priključnicabind(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2))
	case 3:
		return priključnicaPovežise(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return umnožiPriključnicaNaziv(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), false)
	case 7:
		return umnožiPriključnicaNaziv(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), true)
	case 9:
		return priključnicaPošaljito(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), 0, 0)
	case 10:
		return priključnicareceivesa(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), 0, 0)
	case 11:
		return priključnicaPošaljito(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), priključnicacallargument(argumenti_2, 4), priključnicacallargument(argumenti_2, 5))
	case 12:
		return priključnicareceivesa(int32(priključnicacallargument(argumenti_2, 0)), priključnicacallargument(argumenti_2, 1), priključnicacallargument(argumenti_2, 2), priključnicacallargument(argumenti_2, 4), priključnicacallargument(argumenti_2, 5))
	case 13:
		if _, greška := priključnicaforOpisnik(int32(priključnicacallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	case 14:
		if _, greška := priključnicaforOpisnik(int32(priključnicacallargument(argumenti_2, 0))); greška != 0 {
			return greška
		}
		return 0
	}
	return Eopnotsupp
}

func čitanjestdin(address uint32, count uint32) int32 {
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
	sledeće := (stdinPiše + 1) % uint32(len(stdinbuffer))
	if sledeće == stdinčitanje {
		return
	}
	stdinbuffer[stdinPiše] = c
	stdinPiše = sledeće
}

func stdingetblocking() byte {
	for stdinčitanje == stdinPiše {
		sc := pollTastaturascancode()
		if sc != 0 {
			Stdinputbyte(sc)
		}
	}
	c := stdinbuffer[stdinčitanje]
	stdinčitanje = (stdinčitanje + 1) % uint32(len(stdinbuffer))
	return c
}

func pollTastaturascancode() byte {
	for (Portčitanjebyte(0x64) & 0x01) == 0 {
	}
	sc := Portčitanjebyte(0x60)
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

func umnožiizvršnavector(address_2 uint32, iSHOD *izvršnavector) int32 {
	*iSHOD = izvršnavector{}
	if address_2 == 0 {
		return 0
	}
	for popis := uint32(0); popis < maksizvršnavectorunos; popis++ {
		niskaaddress := *(*uint32)(Pointer(uintptr(address_2 + popis*4)))
		if niskaaddress == 0 {
			iSHOD.count = popis
			return 0
		}
		terminated := false
		for dužina := uint32(0); dužina <= maksizvršnaniskaDužina; dužina++ {
			vrednost := *(*byte)(Pointer(uintptr(niskaaddress + dužina)))
			iSHOD.vrednosti[popis][dužina] = vrednost
			if vrednost == 0 {
				iSHOD.lengths[popis] = dužina
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

func pushizvršnaunsignedinteger32(stack *uint32, vrednost uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = vrednost
}

func setupizvršnastack(procesor *TcpuStanje, argumenti_2 *izvršnavector, environment *izvršnavector) int32 {
	const stackBajtova uint32 = 4096
	if !MakeOpsegPrivatnowritable(getcr3(), KorisnikstackGore-stackBajtova, stackBajtova) {
		return Enomem
	}
	stack := KorisnikstackGore
	var argumentpointers [maksizvršnavectorunos]uint32
	var environmentpointers [maksizvršnavectorunos]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		dužina := environment.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovasaPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, environment.vrednosti[i][:dužina])
		environmentpointers[i] = stack
	}
	for i := int(argumenti_2.count) - 1; i >= 0; i-- {
		dužina := argumenti_2.lengths[i] + 1
		stack -= dužina
		odredište := GetBajtovasaPokazivač(uintptr(stack), int(dužina), int(dužina))
		copy(odredište, argumenti_2.vrednosti[i][:dužina])
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
	procesor.Esp = stack
	procesor.Ebp = 0
	return 0
}

func zatvorinaizvršna(proces *procesunos) {
	if proces == nil {
		return
	}
	for opisnik := int32(0); opisnik < maksOpisnik; opisnik++ {
		if proces.fds[opisnik].zauzeto_2 && (proces.fds[opisnik].opisnikParametri&opisnikcloexec) != 0 {
			zatvoriProcesOpisnik(proces, opisnik)
		}
	}
}

func sysexecve(procesor *TcpuStanje, pUTANjAaddress uint32) int32 {
	if pUTANjAaddress == 0 {
		return Efault
	}
	var argumenti_2 izvršnavector
	var environment izvršnavector
	if iSHOD := umnožiizvršnavector(procesor.Ecx, &argumenti_2); iSHOD < 0 {
		return iSHOD
	}
	if iSHOD := umnožiizvršnavector(procesor.Edx, &environment); iSHOD < 0 {
		return iSHOD
	}
	nazivlen, naziv := umnožiPUTANjA(pUTANjAaddress)
	if nazivlen == 0 {
		return Enoent
	}
	veličina := datotekaVeličina(naziv[:nazivlen])
	if veličina == 0 {
		return Enoent
	}
	memorijamanager := &mem.TMemorijamanager{}
	datotekaPokazivač := memorijamanager.Malloc(veličina)
	if datotekaPokazivač == nil {
		return Einval
	}
	data := GetBajtovasaPokazivač(uintptr(datotekaPokazivač), int(veličina), int(veličina))
	čitanjeDatoteka(naziv[:nazivlen], data)
	if veličina < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memorijamanager.Slobodno(datotekaPokazivač)
		return Enoexec
	}
	loader := Elf{}
	unos := loader.Getunos(data)
	loader.Parse(data, getcr3())
	memorijamanager.Slobodno(datotekaPokazivač)
	if iSHOD := setupizvršnastack(procesor, &argumenti_2, &environment); iSHOD < 0 {
		return iSHOD
	}
	zatvorinaizvršna(ensureTrenutnoProces())
	procesor.Eip = unos
	procesor.Eax = 0
	return 0
}

func sysfork(procesor *TcpuStanje) int32 {
	nadređeniPID := TrenutnoPID()
	if ensureTrenutnoProces() == nil {
		return Enfile
	}
	pID := allocateProces(nadređeniPID)
	if pID == 0 {
		return Einval
	}
	memorijamanager := &mem.TMemorijamanager{}
	threadPokazivač := memorijamanager.Malloc(uint32(Sizeof(TThread{})))
	stackPokazivač := memorijamanager.Malloc(ThreadstackVeličina)
	sadržaniSTRANADirektorijum := Cloneaddressrazmakcow(getcr3())
	if threadPokazivač == nil || stackPokazivač == nil || sadržaniSTRANADirektorijum == 0 {
		odbaciProces(pID)
		return Einval
	}
	sadržani := (*TThread)(threadPokazivač)
	sadržani.Stack = uint32(uintptr(stackPokazivač))
	sadržani.ProcesorStanje = (*TcpuStanje)(Pointer(uintptr(stackPokazivač) + ThreadstackVeličina - Sizeof(TcpuStanje{})))
	*sadržani.ProcesorStanje = *procesor
	sadržani.ProcesorStanje.Eax = 0
	sadržani.Korisnikstack_2 = procesor.Esp
	sadržani.KorisnikstackVeličina_2 = 0
	sadržani.PID = pID
	sadržani.NadređeniPID = nadređeniPID
	sadržani.STRANADirektorijumunos = sadržaniSTRANADirektorijum
	sadržani.ThreadStanje = Spreman
	sadržani.Fpuoffset = 0xffffffff
	sadržani.Iskernel = false
	Dodajrunnablethread(sadržani)
	return int32(pID)
}

func sysIzlaz(stanje uint32) {
	pID := TrenutnoPID()
	for i := 0; i < len(procesTabela); i++ {
		if procesTabela[i].zauzeto_2 && procesTabela[i].pID == pID {
			zatvoriSveProcesfds(&procesTabela[i])
			procesTabela[i].izašaosam = true
			procesTabela[i].stanje = (stanje & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pID int32, stanjeaddress uint32, opcije uint32) int32 {
	if (opcije & ^uint32(1)) != 0 {
		return Einval
	}
	nadređeniPID := TrenutnoPID()
	foundsadržani := false
	for i := 0; i < len(procesTabela); i++ {
		p := &procesTabela[i]
		matches := pID == -1 || pID == 0 || p.pID == uint32(pID)
		if p.zauzeto_2 && matches && p.nadređeni == nadređeniPID {
			foundsadržani = true
			if p.izašaosam {
				if stanjeaddress != 0 {
					*(*uint32)(Pointer(uintptr(stanjeaddress))) = p.stanje
				}
				sadržaniPID := p.pID
				*p = procesunos{}
				return int32(sadržaniPID)
			}
		}
	}
	if !foundsadržani {
		return Echild
	}

	if (opcije & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateProces(nadređeni uint32) uint32 {
	nadređeniProces := nađiProces(nadređeni)
	pID := AllocatePID()
	for i := 0; i < len(procesTabela); i++ {
		if !procesTabela[i].zauzeto_2 {
			procesTabela[i] = procesunos{
				zauzeto_2:	true,
				pID:		pID,
				nadređeni:	nadređeni,
				programbreak:	korisnikheapbase,
			}
			if nadređeniProces != nil {
				procesTabela[i].programbreak = nadređeniProces.programbreak
				for opisnik := 0; opisnik < maksOpisnik; opisnik++ {
					if nadređeniProces.fds[opisnik].zauzeto_2 {
						procesTabela[i].fds[opisnik] = nadređeniProces.fds[opisnik]
						opis := nadređeniProces.fds[opisnik].opis
						if opis >= 0 && opis < maksOtvoriDATOTEKE {
							otvoriDatotekaTabela[opis].refs++
						}
					}
				}
			} else {
				initializeProcesfds(&procesTabela[i])
			}
			return pID
		}
	}
	return 0
}

func zatvoriSveProcesfds(proces *procesunos) {
	if proces == nil {
		return
	}
	for opisnik := int32(0); opisnik < maksOpisnik; opisnik++ {
		if proces.fds[opisnik].zauzeto_2 {
			zatvoriProcesOpisnik(proces, opisnik)
		}
	}
}

func odbaciProces(pID uint32) {
	proces := nađiProces(pID)
	if proces == nil {
		return
	}
	zatvoriSveProcesfds(proces)
	*proces = procesunos{}
}

func umnožiPUTANjA(pUTANjAaddress uint32) (uint32, [12]byte) {
	var naziv [12]byte
	if pUTANjAaddress == 0 {
		return 0, naziv
	}
	raw := GetBajtovasaPokazivač(uintptr(pUTANjAaddress), 64, 64)
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
		naziv[n] = c
		n++
	}
	return n, naziv
}

func datotekaVeličina(datoteka []byte) uint32 {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Čitanjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	veličina := bios.Len(&ata0s, partition.Mbr.Primarypartition[0], datoteka)
	ata0s.Flush()
	return veličina
}

func čitanjeDatoteka(datoteka []byte, data []byte) {
	var ata0s = TNaprednoTehnologijaattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	partition := TmsdospartitionTabela{}
	partition.Čitanjepartition(&ata0s)

	bios := TBiosparameterBlok32{}
	bios.Čitanje(&ata0s, partition.Mbr.Primarypartition[0], datoteka, data)
	ata0s.Flush()
}

func getcr3() uint32
