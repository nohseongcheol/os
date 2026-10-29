/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package しすてむよびだし

import . "unsafe"

import . "わりこみ"
import . "こんそーる"
import . "はんよう"
import . "ふくすうたすくかんり"
import . "どらいばー/ata"
import . "ふぁいるしすてむ/msdosくぶん"
import . "ふぁいるしすてむ/fat"
import . "ふぁいるしすてむ/じっこうれんけつけいしき"
import mem "めもりかんりしゃ"
import . "ぺーじかんり"
import . "ぽーと"
import . "たすくかんり/すけじゅーら"
import . "たすくかんり/すれっど"
import . "かそうめもり"

var こんそーる_2 = Tこんそーる{}

type TSyscall struct {
	Tわりこみhandler
}

const (
	Sysしゅうりょう		uint32	= 1
	Sysfork		uint32	= 2
	Sysよみこみ		uint32	= 3
	Sysかきこみ		uint32	= 4
	Sysひらく		uint32	= 5
	Sysとじる		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sysあくせす		uint32	= 33
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
	Sysrtしゅうりょう		uint32	= 252

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
	さいだいfd			= 32
	さいだいひらくふぁいる		= 128
)

type fdentry struct {
	しようちゅう	bool
	せつめい	int32
	fdふらぐ	uint32
}

type ひらくふぁいるせつめい struct {
	しようちゅう	bool
	refs	uint32
	kind	uint32
	ふらぐ	uint32
	はいち	uint32
	さいず	uint32
	なまえ	[12]byte
	なまえlen	uint32
	aux	uint32
}

const (
	fdkindなし	uint32	= 0
	fdkindfat	uint32	= 1
	fdkindstdin	uint32	= 2
	fdkindこんそーる	uint32	= 3
	fdkindるーとでぃれくとり	uint32	= 4
	fdkindそけっと	uint32	= 5

	oよみこみせんよう	uint32	= 0
	oかきこみせんよう	uint32	= 1
	oよみこみかきこみ	uint32	= 2
	oさくせい	uint32	= 0x40
	oきりすて	uint32	= 0x200
	oappend	uint32	= 0x400
	oでぃれくとり	uint32	= 0x10000

	seekあり		uint32	= 0
	seekげんざいのにちじ	uint32	= 1
	seekぶんまつ		uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	fありfd		uint32	= 2
	fgetfl		uint32	= 3
	fありfl		uint32	= 4
	fdcloexec	uint32	= 1

	sifmt	uint32	= 0170000
	sifdir	uint32	= 0040000
	sifreg	uint32	= 0100000
	sifchr	uint32	= 0020000
	sifsock	uint32	= 0140000
)

const (
	afinet		= 2
	sockdatagram	= 2
	ipprotocoludp	= 17
	さいだいsockets	= 32
	さいだいそけっとぱけっと	= 8
	さいだいdatagramさいず	= 512
)

type そけっとaddressipv4 struct {
	Family	uint16
	Pぽーと	uint16
	Address	uint32
	Zすうちの0	[8]byte
}

type そけっとpacket struct {
	しようちゅう	bool
	さいず	uint32
	てんそうもと	そけっとaddressipv4
	でーた	[さいだいdatagramさいず]byte
}

type ろーかるdatagramそけっと struct {
	しようちゅう		bool
	bound		bool
	connected	bool
	ろーかる		そけっとaddressipv4
	りもーと		そけっとaddressipv4
	head		uint32
	tail		uint32
	かうんと		uint32
	ぱけっと		[さいだいそけっとぱけっと]そけっとpacket
}

type posixstat struct {
	Dでばいす		uint32
	Ino		uint32
	Mもーど		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Sさいず_2		int32
	Blksize		int32
	Bぶろっく		int32
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
	Vばーじょん		[65]byte
	Machine		[65]byte
}

const (
	さいだいじっこうvectorentry	= 16
	さいだいじっこうぶんじれつながさ	= 63
)

type じっこうvector struct {
	かうんと	uint32
	lengths	[さいだいじっこうvectorentry]uint32
	すうち	[さいだいじっこうvectorentry][さいだいじっこうぶんじれつながさ + 1]byte
}

type ぷろせすentry struct {
	しようちゅう		bool
	pid		uint32
	parent		uint32
	しゅうりょう		bool
	じょうたい		uint32
	ぷろぐらむbreak	uint32
	fds		[さいだいfd]fdentry
}

type もじれつへっだ struct {
	Data	uintptr
	Len	int
}

func syscallえらー(えらー int32) uint32 {
	return *(*uint32)(Pointer(&えらー))
}

var ひらくふぁいるtable [さいだいひらくふぁいる]ひらくふぁいるせつめい
var ぷろせすtable [32]ぷろせすentry
var ろーかるsockets [さいだいsockets]ろーかるdatagramそけっと
var つぎephemeralぽーと uint16 = 49152

const (
	りようしゃheapbase	uint32	= 0x06000000
	りようしゃheapせいげん	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdinよみこみ uint32
var stdinかきこみ uint32

func Iわりこみ(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sysしゅうりょう_2(もくじ uint32) {
	Syscall(Sysしゅうりょう, もくじ)
}

func Sysよみこみ_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sysよみこみ, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sysいんさつstr(buffer string) {
	h := (*もじれつへっだ)(Pointer(&buffer))
	Syscall(Sysかきこみ, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sysいんさつunsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sysかきこみ, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sysひらく_2(ぱす uintptr, ふらぐ uint32, もーど uint32) int32 {
	return int32(Syscall(Sysひらく, uint32(ぱす), ふらぐ, もーど))
}

func Sysとじる_2(fd uint32) int32 {
	return int32(Syscall(Sysとじる, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(ぱらめーた ...uint32) uint32 {

	l := len(ぱらめーた)
	switch l {
	case 1:
		return Iわりこみ(ぱらめーた[0], 0, 0, 0, 0, 0)
	case 2:
		return Iわりこみ(ぱらめーた[0], ぱらめーた[1], 0, 0, 0, 0)
	case 3:
		return Iわりこみ(ぱらめーた[0], ぱらめーた[1], ぱらめーた[2], 0, 0, 0)
	case 4:
		return Iわりこみ(ぱらめーた[0], ぱらめーた[1], ぱらめーた[2], ぱらめーた[3], 0, 0)
	case 5:
		return Iわりこみ(ぱらめーた[0], ぱらめーた[1], ぱらめーた[2], ぱらめーた[3], ぱらめーた[4], 0)
	case 6:
		return Iわりこみ(ぱらめーた[0], ぱらめーた[1], ぱらめーた[2], ぱらめーた[3], ぱらめーた[4], ぱらめーた[5])
	default:
		return syscallえらー(Enosys)
	}
}

func (self *TSyscall) Init(かんりしゃ *Tわりこみかんりしゃ) {
	initふぁいるdescriptor()

	わりこみhandler = とってわりこみ

	var address uintptr
	address = uintptr(Pointer(&わりこみhandler))

	self.Tわりこみhandler.Init(0x80, uintptr(Pointer(かんりしゃ)), address)
}

var わりこみhandler func(uint32) uint32

func とってわりこみ(esp uint32) uint32 {
	var cpu = (*Tcpuじょうたい)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sysしゅうりょう:
		sysしゅうりょう(cpu.Ebx)
		return uint32(uintptr(Pointer(Sていしげんざいのにちじすれっど(cpu))))
	case Sysrtしゅうりょう:
		sysしゅうりょう(cpu.Ebx)
		return uint32(uintptr(Pointer(Sていしげんざいのにちじすれっど(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sysよみこみ:
		cpu.Eax = uint32(sysよみこみ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysかきこみ:
		cpu.Eax = uint32(sysかきこみ(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sysひらく:
		cpu.Eax = uint32(sysひらく(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sysひらく(cpu.Ebx, oさくせい|oかきこみせんよう|oきりすて, cpu.Ecx))
		return esp
	case Sysとじる:
		cpu.Eax = uint32(sysとじる(int32(cpu.Ebx)))
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
		cpu.Eax = Cげんざいのにちじpid()
		return esp
	case Sysgetppid:
		cpu.Eax = Cげんざいのにちじparentpid()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sysあくせす:
		cpu.Eax = uint32(sysあくせす(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sysそけっとよびだし(cpu.Ebx, cpu.Ecx))
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
		こんそーる_2.MUnsignedinteger32いんさつ(cpu.Ebx)
		return esp

	default:
		こんそーる_2.Mいんさつxy(([]byte)("sys["), 1, 23)
		こんそーる_2.MUnsignedinteger32いんさつ(esp)
		こんそーる_2.Mいんさつ(([]byte)(":"))
		こんそーる_2.MUnsignedinteger32いんさつ(cpu.Eax)
		こんそーる_2.Mいんさつ(([]byte)(":"))
		こんそーる_2.MUnsignedinteger32いんさつ(cpu.Ebx)
		こんそーる_2.Mいんさつ(([]byte)(":"))
		こんそーる_2.MUnsignedinteger32いんさつ(cpu.Ecx)
		こんそーる_2.Mいんさつ(([]byte)(":"))
		こんそーる_2.MUnsignedinteger32いんさつ(cpu.Edx)
		こんそーる_2.Mいんさつ(([]byte)("]"))
		cpu.Eax = syscallえらー(Enosys)
		return esp
	}

	return esp
}

func initふぁいるdescriptor() {
	for i := 0; i < さいだいひらくふぁいる; i++ {
		ひらくふぁいるtable[i] = ひらくふぁいるせつめい{}
	}
	for i := 0; i < len(ぷろせすtable); i++ {
		ぷろせすtable[i] = ぷろせすentry{}
	}
	for i := 0; i < len(ろーかるsockets); i++ {
		ろーかるsockets[i] = ろーかるdatagramそけっと{}
	}
	つぎephemeralぽーと = 49152
	ひらくふぁいるtable[0] = ひらくふぁいるせつめい{しようちゅう: true, kind: fdkindstdin, ふらぐ: oよみこみせんよう}
	ひらくふぁいるtable[1] = ひらくふぁいるせつめい{しようちゅう: true, kind: fdkindこんそーる, ふらぐ: oかきこみせんよう}
	ひらくふぁいるtable[2] = ひらくふぁいるせつめい{しようちゅう: true, kind: fdkindこんそーる, ふらぐ: oかきこみせんよう}
}

func けんさくぷろせす(pid uint32) *ぷろせすentry {
	for i := 0; i < len(ぷろせすtable); i++ {
		if ぷろせすtable[i].しようちゅう && ぷろせすtable[i].pid == pid {
			return &ぷろせすtable[i]
		}
	}
	return nil
}

func initializeぷろせすfds(ぷろせす *ぷろせすentry) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		ぷろせす.fds[fd] = fdentry{しようちゅう: true, せつめい: fd}
		ひらくふぁいるtable[fd].refs++
	}
}

func ensureげんざいのにちじぷろせす() *ぷろせすentry {
	pid := Cげんざいのにちじpid()
	if ぷろせす := けんさくぷろせす(pid); ぷろせす != nil {
		return ぷろせす
	}
	for i := 0; i < len(ぷろせすtable); i++ {
		if !ぷろせすtable[i].しようちゅう {
			ぷろせすtable[i] = ぷろせすentry{
				しようちゅう:		true,
				pid:		pid,
				parent:		Cげんざいのにちじparentpid(),
				ぷろぐらむbreak:	りようしゃheapbase,
			}
			initializeぷろせすfds(&ぷろせすtable[i])
			return &ぷろせすtable[i]
		}
	}
	return nil
}

func getひらくふぁいるfor(ぷろせす *ぷろせすentry, fd int32) *ひらくふぁいるせつめい {
	if ぷろせす == nil || fd < 0 || fd >= さいだいfd || !ぷろせす.fds[fd].しようちゅう {
		return nil
	}
	せつめい := ぷろせす.fds[fd].せつめい
	if せつめい < 0 || せつめい >= さいだいひらくふぁいる || !ひらくふぁいるtable[せつめい].しようちゅう {
		return nil
	}
	return &ひらくふぁいるtable[せつめい]
}

func getひらくふぁいる(fd int32) *ひらくふぁいるせつめい {
	return getひらくふぁいるfor(ensureげんざいのにちじぷろせす(), fd)
}

func allocateひらくふぁいる() int32 {
	for i := int32(3); i < さいだいひらくふぁいる; i++ {
		if !ひらくふぁいるtable[i].しようちゅう {
			ひらくふぁいるtable[i] = ひらくふぁいるせつめい{しようちゅう: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(ぷろせす *ぷろせすentry, せつめい int32, さいしょう int32) int32 {
	if ぷろせす == nil {
		return Enfile
	}
	if さいしょう < 0 || さいしょう >= さいだいfd {
		return Einval
	}
	for fd := さいしょう; fd < さいだいfd; fd++ {
		if !ぷろせす.fds[fd].しようちゅう {
			ぷろせす.fds[fd] = fdentry{しようちゅう: true, せつめい: せつめい}
			return fd
		}
	}
	return Emfile
}

func releaseひらくふぁいる(せつめい int32) {
	if せつめい < 0 || せつめい >= さいだいひらくふぁいる {
		return
	}
	entry := &ひらくふぁいるtable[せつめい]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && せつめい > stderrfd {
		if entry.kind == fdkindそけっと && entry.aux < さいだいsockets {
			ろーかるsockets[entry.aux] = ろーかるdatagramそけっと{}
		}
		*entry = ひらくふぁいるせつめい{}
	}
}

func とじるぷろせすfd(ぷろせす *ぷろせすentry, fd int32) int32 {
	if ぷろせす == nil || getひらくふぁいるfor(ぷろせす, fd) == nil {
		return Ebadf
	}
	せつめい := ぷろせす.fds[fd].せつめい
	ぷろせす.fds[fd] = fdentry{}
	releaseひらくふぁいる(せつめい)
	return 0
}

func sysかきこみ(fd int32, address uint32, かうんと uint32) int32 {
	if かうんと == 0 {
		return 0
	}
	if address == 0 || address+かうんと < address {
		return Efault
	}
	if かうんと > 4096 {
		return Einval
	}
	entry := getひらくふぁいる(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindこんそーる {
		if entry.kind == fdkindそけっと {
			return そけっとそうしんto(fd, address, かうんと, 0, 0)
		}
		if entry.kind == fdkindfat || entry.kind == fdkindるーとでぃれくとり {
			return Erofs
		}
		return Ebadf
	}
	buffer := Getばいとからぽいんた(uintptr(address), int(かうんと), int(かうんと))
	こんそーる_2.Mいんさつ(buffer)
	return int32(かうんと)
}

func sysよみこみ(fd int32, address uint32, かうんと uint32) int32 {
	if かうんと == 0 {
		return 0
	}
	if address == 0 || address+かうんと < address {
		return Efault
	}
	entry := getひらくふぁいる(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind == fdkindstdin {
		return よみこみstdin(address, かうんと)
	}
	if entry.kind == fdkindるーとでぃれくとり {
		return Eisdir
	}
	if entry.kind == fdkindそけっと {
		return そけっとreceiveから(fd, address, かうんと, 0, 0)
	}
	if entry.kind != fdkindfat {
		return Ebadf
	}
	if entry.はいち >= entry.さいず {
		return 0
	}
	remaining := entry.さいず - entry.はいち
	if かうんと > remaining {
		かうんと = remaining
	}
	buffer := Getばいとからぽいんた(uintptr(address), int(かうんと), int(かうんと))
	return よみこみvfsふぁいる(entry, buffer, かうんと)
}

func sysひらく(ぱすaddress uint32, ふらぐ uint32, もーど uint32) int32 {
	_ = もーど
	if ぱすaddress == 0 {
		return Efault
	}
	あくせすもーど := ふらぐ & 3
	if あくせすもーど == oかきこみせんよう || あくせすもーど == oよみこみかきこみ || (ふらぐ&(oさくせい|oきりすて|oappend)) != 0 {
		return Erofs
	}

	ぷろせす := ensureげんざいのにちじぷろせす()
	if ぷろせす == nil {
		return Enfile
	}
	せつめい := allocateひらくふぁいる()
	if せつめい < 0 {
		return せつめい
	}
	entry := &ひらくふぁいるtable[せつめい]
	entry.ふらぐ = ふらぐ
	if isるーとぱす(ぱすaddress) {
		entry.kind = fdkindるーとでぃれくとり
		entry.さいず = 0
	} else {
		なまえlen, なまえ := ふくせいぱす(ぱすaddress)
		if なまえlen == 0 {
			*entry = ひらくふぁいるせつめい{}
			return Enoent
		}
		さいず := ふぁいるさいず(なまえ[:なまえlen])
		if さいず == 0 {
			*entry = ひらくふぁいるせつめい{}
			return Enoent
		}
		if (ふらぐ & oでぃれくとり) != 0 {
			*entry = ひらくふぁいるせつめい{}
			return Enotdir
		}
		entry.kind = fdkindfat
		entry.さいず = さいず
		entry.なまえlen = なまえlen
		entry.なまえ = なまえ
	}

	fd := allocatefd(ぷろせす, せつめい, 3)
	if fd < 0 {
		*entry = ひらくふぁいるせつめい{}
		return fd
	}
	return fd
}

func sysとじる(fd int32) int32 {
	return とじるぷろせすfd(ensureげんざいのにちじぷろせす(), fd)
}

func sysdup(fd int32, さいしょう int32) int32 {
	ぷろせす := ensureげんざいのにちじぷろせす()
	entry := getひらくふぁいるfor(ぷろせす, fd)
	if entry == nil {
		return Ebadf
	}
	しんきfd := allocatefd(ぷろせす, ぷろせす.fds[fd].せつめい, さいしょう)
	if しんきfd >= 0 {
		entry.refs++
	}
	return しんきfd
}

func sysdup2(oldfd int32, しんきfd int32) int32 {
	ぷろせす := ensureげんざいのにちじぷろせす()
	entry := getひらくふぁいるfor(ぷろせす, oldfd)
	if entry == nil {
		return Ebadf
	}
	if しんきfd < 0 || しんきfd >= さいだいfd {
		return Ebadf
	}
	if oldfd == しんきfd {
		return しんきfd
	}
	if ぷろせす.fds[しんきfd].しようちゅう {
		とじるぷろせすfd(ぷろせす, しんきfd)
	}
	ぷろせす.fds[しんきfd] = fdentry{しようちゅう: true, せつめい: ぷろせす.fds[oldfd].せつめい}
	entry.refs++
	return しんきfd
}

func sysfcntl(fd int32, こまんど uint32, argument uint32) int32 {
	ぷろせす := ensureげんざいのにちじぷろせす()
	entry := getひらくふぁいるfor(ぷろせす, fd)
	if entry == nil {
		return Ebadf
	}
	switch こまんど {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(ぷろせす.fds[fd].fdふらぐ)
	case fありfd:
		ぷろせす.fds[fd].fdふらぐ = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(entry.ふらぐ)
	case fありfl:
		entry.ふらぐ = (entry.ふらぐ & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, offset int32, whence uint32) int32 {
	entry := getひらくふぁいる(fd)
	if entry == nil {
		return Ebadf
	}
	if entry.kind != fdkindfat {
		return Espipe
	}
	var base int64
	switch whence {
	case seekあり:
		base = 0
	case seekげんざいのにちじ:
		base = int64(entry.はいち)
	case seekぶんまつ:
		base = int64(entry.さいず)
	default:
		return Einval
	}
	はいち_2 := base + int64(offset)
	if はいち_2 < 0 || はいち_2 > 0x7FFFFFFF {
		return Einval
	}
	entry.はいち = uint32(はいち_2)
	return int32(entry.はいち)
}

func よみこみvfsふぁいる(entry *ひらくふぁいるせつめい, てんそうさき_2 []byte, かうんと uint32) int32 {
	めもりかんりしゃ := &mem.Tめもりかんりしゃ{}
	tmpぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(entry.さいず)
	if tmpぽいんた == nil {
		return Einval
	}
	tmp := Getばいとからぽいんた(uintptr(tmpぽいんた), int(entry.さいず), int(entry.さいず))
	よみこみふぁいる(entry.なまえ[:entry.なまえlen], tmp)
	copy(てんそうさき_2[:かうんと], tmp[entry.はいち:entry.はいち+かうんと])
	entry.はいち += かうんと
	めもりかんりしゃ.Fあき(tmpぽいんた)
	return int32(かうんと)
}

func isるーとぱす(ぱすaddress uint32) bool {
	if ぱすaddress == 0 {
		return false
	}
	ぱす := Getばいとからぽいんた(uintptr(ぱすaddress), 4, 4)
	if ぱす[0] == '/' && ぱす[1] == 0 {
		return true
	}
	if ぱす[0] == '.' && ぱす[1] == 0 {
		return true
	}
	if ぱす[0] == '/' && ぱす[1] == '.' && ぱす[2] == 0 {
		return true
	}
	return false
}

func sysあくせす(ぱすaddress uint32, もーど uint32) int32 {
	if ぱすaddress == 0 {
		return Efault
	}
	if (もーど & ^uint32(7)) != 0 {
		return Einval
	}
	isるーと := isるーとぱす(ぱすaddress)
	exists := isるーと
	if !exists {
		なまえlen, なまえ := ふくせいぱす(ぱすaddress)
		exists = なまえlen != 0 && ふぁいるさいず(なまえ[:なまえlen]) != 0
	}
	if !exists {
		return Enoent
	}
	if (もーど & 2) != 0 {
		return Eacces
	}

	if (もーど&1) != 0 && !isるーと {
		return Eacces
	}
	return 0
}

func syschdir(ぱすaddress uint32) int32 {
	if ぱすaddress == 0 {
		return Efault
	}
	if !isるーとぱす(ぱすaddress) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, さいず uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if さいず < 2 {
		return Erange
	}
	buffer_2 := Getばいとからぽいんた(uintptr(bufferaddress), int(さいず), int(さいず))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, もーど uint32, さいず uint32, iのーど uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.Dでばいす = 1
	stat.Ino = iのーど
	stat.Mもーど = もーど
	stat.Nlink = 1
	stat.Sさいず_2 = int32(さいず)
	stat.Blksize = 512
	stat.Bぶろっく = int32((さいず + 511) / 512)
	return 0
}

func sysstat(ぱすaddress uint32, stataddress uint32) int32 {
	if ぱすaddress == 0 {
		return Efault
	}
	if isるーとぱす(ぱすaddress) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	なまえlen, なまえ := ふくせいぱす(ぱすaddress)
	if なまえlen == 0 {
		return Enoent
	}
	さいず := ふぁいるさいず(なまえ[:なまえlen])
	if さいず == 0 {
		return Enoent
	}
	iのーど := uint32(2)
	for i := uint32(0); i < なまえlen; i++ {
		iのーど = iのーど*33 + uint32(なまえ[i])
	}
	return fillposixstat(stataddress, sifreg|0444, さいず, iのーど)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	entry := getひらくふぁいる(fd)
	if entry == nil {
		return Ebadf
	}
	switch entry.kind {
	case fdkindstdin, fdkindこんそーる:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fdkindるーとでぃれくとり:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fdkindfat:
		return fillposixstat(stataddress, sifreg|0444, entry.さいず, uint32(fd+2))
	case fdkindそけっと:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if getひらくふぁいる(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	ぷろせす := ensureげんざいのにちじぷろせす()
	if ぷろせす == nil {
		return 0
	}
	if ぷろせす.ぷろぐらむbreak == 0 {
		ぷろせす.ぷろぐらむbreak = りようしゃheapbase
	}
	if address_2 == 0 {
		return ぷろせす.ぷろぐらむbreak
	}
	if address_2 < りようしゃheapbase || address_2 > りようしゃheapせいげん {
		return ぷろせす.ぷろぐらむbreak
	}
	ぷろせす.ぷろぐらむbreak = address_2
	return ぷろせす.ぷろぐらむbreak
}

func ふくせいutsfield(てんそうさき *[65]byte, あたい string) {
	せいげん := len(あたい)
	if せいげん > 64 {
		せいげん = 64
	}
	for i := 0; i < せいげん; i++ {
		てんそうさき[i] = あたい[i]
	}
	てんそうさき[せいげん] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	なまえ := (*posixutsname)(Pointer(uintptr(address_2)))
	*なまえ = posixutsname{}
	ふくせいutsfield(&なまえ.Sysname, "EngOS")
	ふくせいutsfield(&なまえ.Nodename, "engos")
	ふくせいutsfield(&なまえ.Release, "0.1-posix")
	ふくせいutsfield(&なまえ.Vばーじょん, "POSIX.1-2017 phase 1")
	ふくせいutsfield(&なまえ.Machine, "i386")
	return 0
}

func すわっぷunsignedinteger16(あたい uint16) uint16 {
	return (あたい << 8) | (あたい >> 8)
}

func そけっとよびだしargument(ひきすう_2 uint32, もくじ uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(ひきすう_2 + もくじ*4)))
}

func そけっとforfd(fd int32) (*ろーかるdatagramそけっと, int32) {
	entry := getひらくふぁいる(fd)
	if entry == nil || entry.kind != fdkindそけっと || entry.aux >= さいだいsockets {
		return nil, Ebadf
	}
	そけっと := &ろーかるsockets[entry.aux]
	if !そけっと.しようちゅう {
		return nil, Ebadf
	}
	return そけっと, 0
}

func allocateそけっと(どめいん uint32, そけっとかた uint32, protocol uint32) int32 {
	if どめいん != afinet {
		return Eafnosupport
	}
	if そけっとかた != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	ぷろせす := ensureげんざいのにちじぷろせす()
	if ぷろせす == nil {
		return Enfile
	}
	そけっともくじ := -1
	for i := 0; i < さいだいsockets; i++ {
		if !ろーかるsockets[i].しようちゅう {
			そけっともくじ = i
			break
		}
	}
	if そけっともくじ < 0 {
		return Enfile
	}
	せつめい := allocateひらくふぁいる()
	if せつめい < 0 {
		return せつめい
	}
	ろーかるsockets[そけっともくじ] = ろーかるdatagramそけっと{しようちゅう: true}
	entry := &ひらくふぁいるtable[せつめい]
	entry.kind = fdkindそけっと
	entry.ふらぐ = oよみこみかきこみ
	entry.aux = uint32(そけっともくじ)
	fd := allocatefd(ぷろせす, せつめい, 3)
	if fd < 0 {
		ろーかるsockets[そけっともくじ] = ろーかるdatagramそけっと{}
		*entry = ひらくふぁいるせつめい{}
		return fd
	}
	return fd
}

func そけっとaddress(address_2 uint32, ながさ uint32) (*そけっとaddressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if ながさ < 16 {
		return nil, Einval
	}
	せいせいさき := (*そけっとaddressipv4)(Pointer(uintptr(address_2)))
	if せいせいさき.Family != afinet {
		return nil, Eafnosupport
	}
	return せいせいさき, 0
}

func ぽーとじゅしんON(ぽーと uint16, except *ろーかるdatagramそけっと) bool {
	for i := 0; i < さいだいsockets; i++ {
		そけっと := &ろーかるsockets[i]
		if そけっと != except && そけっと.しようちゅう && そけっと.bound && そけっと.ろーかる.Pぽーと == ぽーと {
			return true
		}
	}
	return false
}

func ばいんどephemeral(そけっと *ろーかるdatagramそけっと) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		ぽーと := すわっぷunsignedinteger16(つぎephemeralぽーと)
		つぎephemeralぽーと++
		if つぎephemeralぽーと < 49152 {
			つぎephemeralぽーと = 49152
		}
		if !ぽーとじゅしんON(ぽーと, そけっと) {
			そけっと.ろーかる = そけっとaddressipv4{Family: afinet, Pぽーと: ぽーと, Address: 0x0100007F}
			そけっと.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func そけっとばいんど(fd int32, address_2 uint32, ながさ uint32) int32 {
	そけっと, えらー := そけっとforfd(fd)
	if えらー != 0 {
		return えらー
	}
	requested, えらー := そけっとaddress(address_2, ながさ)
	if えらー != 0 {
		return えらー
	}
	if そけっと.bound {
		return Einval
	}
	if requested.Pぽーと == 0 {
		return ばいんどephemeral(そけっと)
	}
	if ぽーとじゅしんON(requested.Pぽーと, そけっと) {
		return Eaddrinuse
	}
	そけっと.ろーかる = *requested
	そけっと.bound = true
	return 0
}

func そけっとせつぞく(fd int32, address_2 uint32, ながさ uint32) int32 {
	そけっと, えらー := そけっとforfd(fd)
	if えらー != 0 {
		return えらー
	}
	りもーと, えらー := そけっとaddress(address_2, ながさ)
	if えらー != 0 {
		return えらー
	}
	if !そけっと.bound {
		if えらー := ばいんどephemeral(そけっと); えらー != 0 {
			return えらー
		}
	}
	そけっと.りもーと = *りもーと
	そけっと.connected = true
	return 0
}

func そけっとそうしんto(fd int32, bufferaddress_2 uint32, ながさ uint32, てんそうさきaddress uint32, てんそうさきながさ uint32) int32 {
	そけっと, えらー := そけっとforfd(fd)
	if えらー != 0 {
		return えらー
	}
	if ながさ > さいだいdatagramさいず {
		return Emsgsize
	}
	if ながさ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var てんそうさき そけっとaddressipv4
	if てんそうさきaddress != 0 {
		address_2, addressえらー := そけっとaddress(てんそうさきaddress, てんそうさきながさ)
		if addressえらー != 0 {
			return addressえらー
		}
		てんそうさき = *address_2
	} else {
		if !そけっと.connected {
			return Enotconn
		}
		てんそうさき = そけっと.りもーと
	}
	if !そけっと.bound {
		if ばいんどえらー := ばいんどephemeral(そけっと); ばいんどえらー != 0 {
			return ばいんどえらー
		}
	}
	var receiver *ろーかるdatagramそけっと
	for i := 0; i < さいだいsockets; i++ {
		candidate := &ろーかるsockets[i]
		if candidate.しようちゅう && candidate.bound && candidate.ろーかる.Pぽーと == てんそうさき.Pぽーと &&
			(candidate.ろーかる.Address == 0 || candidate.ろーかる.Address == てんそうさき.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.かうんと >= さいだいそけっとぱけっと {
		return Eagain
	}
	packet := &receiver.ぱけっと[receiver.tail]
	*packet = そけっとpacket{しようちゅう: true, さいず: ながさ, てんそうもと: そけっと.ろーかる}
	if ながさ != 0 {
		てんそうもと := Getばいとからぽいんた(uintptr(bufferaddress_2), int(ながさ), int(ながさ))
		copy(packet.でーた[:ながさ], てんそうもと)
	}
	receiver.tail = (receiver.tail + 1) % さいだいそけっとぱけっと
	receiver.かうんと++
	return int32(ながさ)
}

func そけっとreceiveから(fd int32, bufferaddress_2 uint32, ながさ uint32, てんそうもとaddress uint32, てんそうもとながさaddress uint32) int32 {
	そけっと, えらー := そけっとforfd(fd)
	if えらー != 0 {
		return えらー
	}
	if ながさ != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if そけっと.かうんと == 0 {
		return Eagain
	}
	packet := &そけっと.ぱけっと[そけっと.head]
	ふくせいながさ := packet.さいず
	if ふくせいながさ > ながさ {
		ふくせいながさ = ながさ
	}
	if ふくせいながさ != 0 {
		てんそうさき := Getばいとからぽいんた(uintptr(bufferaddress_2), int(ふくせいながさ), int(ふくせいながさ))
		copy(てんそうさき, packet.でーた[:ふくせいながさ])
	}
	if てんそうもとaddress != 0 {
		if てんそうもとながさaddress == 0 {
			return Efault
		}
		providedながさ := (*uint32)(Pointer(uintptr(てんそうもとながさaddress)))
		if *providedながさ >= 16 {
			*(*そけっとaddressipv4)(Pointer(uintptr(てんそうもとaddress))) = packet.てんそうもと
		}
		*providedながさ = 16
	}
	*packet = そけっとpacket{}
	そけっと.head = (そけっと.head + 1) % さいだいそけっとぱけっと
	そけっと.かうんと--
	return int32(ふくせいながさ)
}

func ふくせいそけっとなまえ(fd int32, address_2 uint32, ながさaddress uint32, peer bool) int32 {
	そけっと, えらー := そけっとforfd(fd)
	if えらー != 0 {
		return えらー
	}
	if address_2 == 0 || ながさaddress == 0 {
		return Efault
	}
	ながさ := (*uint32)(Pointer(uintptr(ながさaddress)))
	if *ながさ < 16 {
		*ながさ = 16
		return Einval
	}
	if peer {
		if !そけっと.connected {
			return Enotconn
		}
		*(*そけっとaddressipv4)(Pointer(uintptr(address_2))) = そけっと.りもーと
	} else {
		if !そけっと.bound {
			if ばいんどえらー := ばいんどephemeral(そけっと); ばいんどえらー != 0 {
				return ばいんどえらー
			}
		}
		*(*そけっとaddressipv4)(Pointer(uintptr(address_2))) = そけっと.ろーかる
	}
	*ながさ = 16
	return 0
}

func sysそけっとよびだし(よびだし uint32, ひきすう_2 uint32) int32 {
	if ひきすう_2 == 0 {
		return Efault
	}
	switch よびだし {
	case 1:
		return allocateそけっと(そけっとよびだしargument(ひきすう_2, 0), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2))
	case 2:
		return そけっとばいんど(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2))
	case 3:
		return そけっとせつぞく(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return ふくせいそけっとなまえ(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), false)
	case 7:
		return ふくせいそけっとなまえ(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), true)
	case 9:
		return そけっとそうしんto(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), 0, 0)
	case 10:
		return そけっとreceiveから(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), 0, 0)
	case 11:
		return そけっとそうしんto(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), そけっとよびだしargument(ひきすう_2, 4), そけっとよびだしargument(ひきすう_2, 5))
	case 12:
		return そけっとreceiveから(int32(そけっとよびだしargument(ひきすう_2, 0)), そけっとよびだしargument(ひきすう_2, 1), そけっとよびだしargument(ひきすう_2, 2), そけっとよびだしargument(ひきすう_2, 4), そけっとよびだしargument(ひきすう_2, 5))
	case 13:
		if _, えらー := そけっとforfd(int32(そけっとよびだしargument(ひきすう_2, 0))); えらー != 0 {
			return えらー
		}
		return 0
	case 14:
		if _, えらー := そけっとforfd(int32(そけっとよびだしargument(ひきすう_2, 0))); えらー != 0 {
			return えらー
		}
		return 0
	}
	return Eopnotsupp
}

func よみこみstdin(address uint32, かうんと uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Getばいとからぽいんた(uintptr(address), int(かうんと), int(かうんと))
	var n uint32
	for n < かうんと {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinputばいと(c byte) {
	つぎ := (stdinかきこみ + 1) % uint32(len(stdinbuffer))
	if つぎ == stdinよみこみ {
		return
	}
	stdinbuffer[stdinかきこみ] = c
	stdinかきこみ = つぎ
}

func stdingetblocking() byte {
	for stdinよみこみ == stdinかきこみ {
		sc := pollきーぼーどscancode()
		if sc != 0 {
			Stdinputばいと(sc)
		}
	}
	c := stdinbuffer[stdinよみこみ]
	stdinよみこみ = (stdinよみこみ + 1) % uint32(len(stdinbuffer))
	return c
}

func pollきーぼーどscancode() byte {
	for (Pぽーとよみこみばいと(0x64) & 0x01) == 0 {
	}
	sc := Pぽーとよみこみばいと(0x60)
	return scancodetoばいと(sc)
}

func scancodetoばいと(sc uint8) byte {
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

func ふくせいじっこうvector(address_2 uint32, せいせいさき *じっこうvector) int32 {
	*せいせいさき = じっこうvector{}
	if address_2 == 0 {
		return 0
	}
	for もくじ := uint32(0); もくじ < さいだいじっこうvectorentry; もくじ++ {
		もじれつaddress := *(*uint32)(Pointer(uintptr(address_2 + もくじ*4)))
		if もじれつaddress == 0 {
			せいせいさき.かうんと = もくじ
			return 0
		}
		terminated := false
		for ながさ := uint32(0); ながさ <= さいだいじっこうぶんじれつながさ; ながさ++ {
			あたい := *(*byte)(Pointer(uintptr(もじれつaddress + ながさ)))
			せいせいさき.すうち[もくじ][ながさ] = あたい
			if あたい == 0 {
				せいせいさき.lengths[もくじ] = ながさ
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

func pushじっこうunsignedinteger32(つみかさねきおくりょういき *uint32, あたい uint32) {
	*つみかさねきおくりょういき -= 4
	*(*uint32)(Pointer(uintptr(*つみかさねきおくりょういき))) = あたい
}

func setupじっこうstack(cpu *Tcpuじょうたい, ひきすう_2 *じっこうvector, environment *じっこうvector) int32 {
	const stackばいと uint32 = 4096
	if !Makerangeぷらいべーとwritable(getcr3(), Uりようしゃstackうえ-stackばいと, stackばいと) {
		return Enomem
	}
	つみかさねきおくりょういき := Uりようしゃstackうえ
	var argumentpointers [さいだいじっこうvectorentry]uint32
	var environmentpointers [さいだいじっこうvectorentry]uint32

	for i := int(environment.かうんと) - 1; i >= 0; i-- {
		ながさ := environment.lengths[i] + 1
		つみかさねきおくりょういき -= ながさ
		てんそうさき := Getばいとからぽいんた(uintptr(つみかさねきおくりょういき), int(ながさ), int(ながさ))
		copy(てんそうさき, environment.すうち[i][:ながさ])
		environmentpointers[i] = つみかさねきおくりょういき
	}
	for i := int(ひきすう_2.かうんと) - 1; i >= 0; i-- {
		ながさ := ひきすう_2.lengths[i] + 1
		つみかさねきおくりょういき -= ながさ
		てんそうさき := Getばいとからぽいんた(uintptr(つみかさねきおくりょういき), int(ながさ), int(ながさ))
		copy(てんそうさき, ひきすう_2.すうち[i][:ながさ])
		argumentpointers[i] = つみかさねきおくりょういき
	}
	つみかさねきおくりょういき &= ^uint32(3)
	pushじっこうunsignedinteger32(&つみかさねきおくりょういき, 0)
	for i := int(environment.かうんと) - 1; i >= 0; i-- {
		pushじっこうunsignedinteger32(&つみかさねきおくりょういき, environmentpointers[i])
	}
	pushじっこうunsignedinteger32(&つみかさねきおくりょういき, 0)
	for i := int(ひきすう_2.かうんと) - 1; i >= 0; i-- {
		pushじっこうunsignedinteger32(&つみかさねきおくりょういき, argumentpointers[i])
	}
	pushじっこうunsignedinteger32(&つみかさねきおくりょういき, ひきすう_2.かうんと)
	cpu.Esp = つみかさねきおくりょういき
	cpu.Ebp = 0
	return 0
}

func とじるときじっこう(ぷろせす *ぷろせすentry) {
	if ぷろせす == nil {
		return
	}
	for fd := int32(0); fd < さいだいfd; fd++ {
		if ぷろせす.fds[fd].しようちゅう && (ぷろせす.fds[fd].fdふらぐ&fdcloexec) != 0 {
			とじるぷろせすfd(ぷろせす, fd)
		}
	}
}

func sysexecve(cpu *Tcpuじょうたい, ぱすaddress uint32) int32 {
	if ぱすaddress == 0 {
		return Efault
	}
	var ひきすう_2 じっこうvector
	var environment じっこうvector
	if せいせいさき := ふくせいじっこうvector(cpu.Ecx, &ひきすう_2); せいせいさき < 0 {
		return せいせいさき
	}
	if せいせいさき := ふくせいじっこうvector(cpu.Edx, &environment); せいせいさき < 0 {
		return せいせいさき
	}
	なまえlen, なまえ := ふくせいぱす(ぱすaddress)
	if なまえlen == 0 {
		return Enoent
	}
	さいず := ふぁいるさいず(なまえ[:なまえlen])
	if さいず == 0 {
		return Enoent
	}
	めもりかんりしゃ := &mem.Tめもりかんりしゃ{}
	ふぁいるぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(さいず)
	if ふぁいるぽいんた == nil {
		return Einval
	}
	でーた := Getばいとからぽいんた(uintptr(ふぁいるぽいんた), int(さいず), int(さいず))
	よみこみふぁいる(なまえ[:なまえlen], でーた)
	if さいず < 52 || でーた[0] != 0x7F || でーた[1] != 'E' || でーた[2] != 'L' || でーた[3] != 'F' {
		めもりかんりしゃ.Fあき(ふぁいるぽいんた)
		return Enoexec
	}
	loader := Elf{}
	entry := loader.Getentry(でーた)
	loader.Parse(でーた, getcr3())
	めもりかんりしゃ.Fあき(ふぁいるぽいんた)
	if せいせいさき := setupじっこうstack(cpu, &ひきすう_2, &environment); せいせいさき < 0 {
		return せいせいさき
	}
	とじるときじっこう(ensureげんざいのにちじぷろせす())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpuじょうたい) int32 {
	parentpid := Cげんざいのにちじpid()
	if ensureげんざいのにちじぷろせす() == nil {
		return Enfile
	}
	pid := allocateぷろせす(parentpid)
	if pid == 0 {
		return Einval
	}
	めもりかんりしゃ := &mem.Tめもりかんりしゃ{}
	すれっどぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(uint32(Sizeof(Tすれっど{})))
	stackぽいんた := めもりかんりしゃ.Mきおくりょういきをかくほ(Tすれっどstackさいず)
	childぺーじでぃれくとり := Cloneaddressすぺーすcow(getcr3())
	if すれっどぽいんた == nil || stackぽいんた == nil || childぺーじでぃれくとり == 0 {
		はきぷろせす(pid)
		return Einval
	}
	child := (*Tすれっど)(すれっどぽいんた)
	child.Stack = uint32(uintptr(stackぽいんた))
	child.Cpuじょうたい = (*Tcpuじょうたい)(Pointer(uintptr(stackぽいんた) + Tすれっどstackさいず - Sizeof(Tcpuじょうたい{})))
	*child.Cpuじょうたい = *cpu
	child.Cpuじょうたい.Eax = 0
	child.Uりようしゃstack_2 = cpu.Esp
	child.Uりようしゃstackさいず_2 = 0
	child.Pid = pid
	child.Parentpid = parentpid
	child.Pぺーじでぃれくとりentry = childぺーじでぃれくとり
	child.Tすれっどじょうたい = RじゅんびOK
	child.Fpuoffset = 0xffffffff
	child.Isちゅうかく = false
	Aついかrunnableすれっど(child)
	return int32(pid)
}

func sysしゅうりょう(じょうたい uint32) {
	pid := Cげんざいのにちじpid()
	for i := 0; i < len(ぷろせすtable); i++ {
		if ぷろせすtable[i].しようちゅう && ぷろせすtable[i].pid == pid {
			とじるすべてぷろせすfds(&ぷろせすtable[i])
			ぷろせすtable[i].しゅうりょう = true
			ぷろせすtable[i].じょうたい = (じょうたい & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(pid int32, じょうたいaddress uint32, おぷしょん uint32) int32 {
	if (おぷしょん & ^uint32(1)) != 0 {
		return Einval
	}
	parentpid := Cげんざいのにちじpid()
	foundchild := false
	for i := 0; i < len(ぷろせすtable); i++ {
		p := &ぷろせすtable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.しようちゅう && matches && p.parent == parentpid {
			foundchild = true
			if p.しゅうりょう {
				if じょうたいaddress != 0 {
					*(*uint32)(Pointer(uintptr(じょうたいaddress))) = p.じょうたい
				}
				childpid := p.pid
				*p = ぷろせすentry{}
				return int32(childpid)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (おぷしょん & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocateぷろせす(parent uint32) uint32 {
	parentぷろせす := けんさくぷろせす(parent)
	pid := Allocatepid()
	for i := 0; i < len(ぷろせすtable); i++ {
		if !ぷろせすtable[i].しようちゅう {
			ぷろせすtable[i] = ぷろせすentry{
				しようちゅう:		true,
				pid:		pid,
				parent:		parent,
				ぷろぐらむbreak:	りようしゃheapbase,
			}
			if parentぷろせす != nil {
				ぷろせすtable[i].ぷろぐらむbreak = parentぷろせす.ぷろぐらむbreak
				for fd := 0; fd < さいだいfd; fd++ {
					if parentぷろせす.fds[fd].しようちゅう {
						ぷろせすtable[i].fds[fd] = parentぷろせす.fds[fd]
						せつめい := parentぷろせす.fds[fd].せつめい
						if せつめい >= 0 && せつめい < さいだいひらくふぁいる {
							ひらくふぁいるtable[せつめい].refs++
						}
					}
				}
			} else {
				initializeぷろせすfds(&ぷろせすtable[i])
			}
			return pid
		}
	}
	return 0
}

func とじるすべてぷろせすfds(ぷろせす *ぷろせすentry) {
	if ぷろせす == nil {
		return
	}
	for fd := int32(0); fd < さいだいfd; fd++ {
		if ぷろせす.fds[fd].しようちゅう {
			とじるぷろせすfd(ぷろせす, fd)
		}
	}
}

func はきぷろせす(pid uint32) {
	ぷろせす := けんさくぷろせす(pid)
	if ぷろせす == nil {
		return
	}
	とじるすべてぷろせすfds(ぷろせす)
	*ぷろせす = ぷろせすentry{}
}

func ふくせいぱす(ぱすaddress uint32) (uint32, [12]byte) {
	var なまえ [12]byte
	if ぱすaddress == 0 {
		return 0, なまえ
	}
	raw := Getばいとからぽいんた(uintptr(ぱすaddress), 64, 64)
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
		なまえ[n] = c
		n++
	}
	return n, なまえ
}

func ふぁいるさいず(ふぁいるめい []byte) uint32 {
	var ata0s = Tしょうさいしようぎじゅつattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	くぶん := Tmsdosくぶんtable{}
	くぶん.Rよみこみくぶん(&ata0s)

	bios := Tふぁいるたいけいせっていち32{}
	さいず := bios.Len(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい)
	ata0s.Flush()
	return さいず
}

func よみこみふぁいる(ふぁいるめい []byte, でーた []byte) {
	var ata0s = Tしょうさいしようぎじゅつattachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	くぶん := Tmsdosくぶんtable{}
	くぶん.Rよみこみくぶん(&ata0s)

	bios := Tふぁいるたいけいせっていち32{}
	bios.Rよみこみ(&ata0s, くぶん.Mbr.Primaryくぶん[0], ふぁいるめい, でーた)
	ata0s.Flush()
}

func getcr3() uint32
