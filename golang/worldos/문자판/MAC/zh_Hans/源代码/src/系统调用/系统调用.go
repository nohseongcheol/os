/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

package 系统调用

import . "unsafe"

import . "中断"
import . "控制台"
import . "工具"
import . "多重任务管理"
import . "驱动程序/ata"
import . "文件系统/msdos分区"
import . "文件系统/fat"
import . "文件系统/可执行与可链接格式"
import mem "内存管理器"
import . "分页管理"
import . "端口"
import . "任务管理/调度器"
import . "任务管理/线程"
import . "虚拟内存"

var 控制台_2 = T控制台{}

type TSyscall struct {
	T中断handler
}

const (
	Sys退出		uint32	= 1
	Sysfork		uint32	= 2
	Sys读取		uint32	= 3
	Sys写入		uint32	= 4
	Sys打开		uint32	= 5
	Sys关闭		uint32	= 6
	Syswaitpid	uint32	= 7
	Syscreat	uint32	= 8
	Sysexecve	uint32	= 11
	Syschdir	uint32	= 12
	Syslseek	uint32	= 19
	Sysgetpid	uint32	= 20
	Sysgetuid	uint32	= 24
	Sys访问		uint32	= 33
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
	Sysrt退出		uint32	= 252

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
	最大值fd			= 32
	最大值打开文件			= 128
)

type fd条目 struct {
	已用	bool
	描述	int32
	fd标志	uint32
}

type 打开文件描述 struct {
	已用	bool
	refs	uint32
	类别	uint32
	标志	uint32
	位置	uint32
	大小	uint32
	名称	[12]byte
	名称len	uint32
	aux	uint32
}

const (
	fd类别无		uint32	= 0
	fd类别fat		uint32	= 1
	fd类别stdin	uint32	= 2
	fd类别控制台		uint32	= 3
	fd类别根目录	uint32	= 4
	fd类别套接字		uint32	= 5

	o读取仅用	uint32	= 0
	o写入仅用	uint32	= 1
	o读取写入	uint32	= 2
	o创建	uint32	= 0x40
	o截断	uint32	= 0x200
	oappend	uint32	= 0x400
	o目录	uint32	= 0x10000

	seek集合	uint32	= 0
	seek当前	uint32	= 1
	seek结尾	uint32	= 2

	fdupfd		uint32	= 0
	fgetfd		uint32	= 1
	f集合fd		uint32	= 2
	fgetfl		uint32	= 3
	f集合fl		uint32	= 4
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
	最大值sockets	= 32
	最大值套接字数据包		= 8
	最大值datagram大小	= 512
)

type 套接字addressipv4 struct {
	Family	uint16
	P端口	uint16
	Address	uint32
	Z零	[8]byte
}

type 套接字packet struct {
	已用	bool
	大小	uint32
	源	套接字addressipv4
	数据	[最大值datagram大小]byte
}

type 本地datagram套接字 struct {
	已用		bool
	bound		bool
	connected	bool
	本地		套接字addressipv4
	远程		套接字addressipv4
	head		uint32
	tail		uint32
	计数		uint32
	数据包		[最大值套接字数据包]套接字packet
}

type posixstat struct {
	D设备		uint32
	Ino		uint32
	M模式		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	S大小_2		int32
	Blksize		int32
	B块		int32
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
	V版本		[65]byte
	Machine		[65]byte
}

const (
	最大值执行vector条目	= 16
	最大值执行字符串长度	= 63
)

type 执行vector struct {
	计数	uint32
	lengths	[最大值执行vector条目]uint32
	文字	[最大值执行vector条目][最大值执行字符串长度 + 1]byte
}

type 进程条目 struct {
	已用	bool
	进程号	uint32
	parent	uint32
	已退出	bool
	状态	uint32
	程序break	uint32
	fds	[最大值fd]fd条目
}

type 字符串头部 struct {
	Data	uintptr
	Len	int
}

func syscall错误(错误 int32) uint32 {
	return *(*uint32)(Pointer(&错误))
}

var 打开文件表格 [最大值打开文件]打开文件描述
var 进程表格 [32]进程条目
var 本地sockets [最大值sockets]本地datagram套接字
var 下一个ephemeral端口 uint16 = 49152

const (
	用户heapbase	uint32	= 0x06000000
	用户heap限定	uint32	= 0x07000000
)

var stdinbuffer [128]byte
var stdin读取 uint32
var stdin写入 uint32

func I中断(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sys退出_2(索引 uint32) {
	Syscall(Sys退出, 索引)
}

func Sys读取_2(fd uint32, buffer []byte) int32 {
	if len(buffer) == 0 {
		return 0
	}
	return int32(Syscall(Sys读取, fd, uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer))))
}

func Sys打印str(buffer string) {
	h := (*字符串头部)(Pointer(&buffer))
	Syscall(Sys写入, uint32(stdoutfd), uint32(h.Data), uint32(h.Len))
}

func Sys打印unsignedinteger32(buffer uint32) {
	Syscall(9, buffer)
}

func Sysprintf(buffer []byte) {
	if len(buffer) == 0 {
		return
	}
	Syscall(Sys写入, uint32(stdoutfd), uint32(uintptr(Pointer(&buffer[0]))), uint32(len(buffer)))
}

func Sysmousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sys打开_2(路径 uintptr, 标志 uint32, 模式 uint32) int32 {
	return int32(Syscall(Sys打开, uint32(路径), 标志, 模式))
}

func Sys关闭_2(fd uint32) int32 {
	return int32(Syscall(Sys关闭, fd))
}

func Sysgetpid_2() uint32 {
	return Syscall(Sysgetpid)
}

func Sysbrk_2(address uint32) uint32 {
	return Syscall(Sysbrk, address)
}

func Syscall(参数_3 ...uint32) uint32 {

	l := len(参数_3)
	switch l {
	case 1:
		return I中断(参数_3[0], 0, 0, 0, 0, 0)
	case 2:
		return I中断(参数_3[0], 参数_3[1], 0, 0, 0, 0)
	case 3:
		return I中断(参数_3[0], 参数_3[1], 参数_3[2], 0, 0, 0)
	case 4:
		return I中断(参数_3[0], 参数_3[1], 参数_3[2], 参数_3[3], 0, 0)
	case 5:
		return I中断(参数_3[0], 参数_3[1], 参数_3[2], 参数_3[3], 参数_3[4], 0)
	case 6:
		return I中断(参数_3[0], 参数_3[1], 参数_3[2], 参数_3[3], 参数_3[4], 参数_3[5])
	default:
		return syscall错误(Enosys)
	}
}

func (self *TSyscall) Init(管理器 *T中断管理器) {
	init文件descriptor()

	中断handler = 控制器中断

	var address uintptr
	address = uintptr(Pointer(&中断handler))

	self.T中断handler.Init(0x80, uintptr(Pointer(管理器)), address)
}

var 中断handler func(uint32) uint32

func 控制器中断(esp uint32) uint32 {
	var cpu = (*Tcpu状态)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case Sys退出:
		sys退出(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止当前线程(cpu))))
	case Sysrt退出:
		sys退出(cpu.Ebx)
		return uint32(uintptr(Pointer(S停止当前线程(cpu))))
	case Sysfork:
		cpu.Eax = uint32(sysfork(cpu))
		return esp
	case Sys读取:
		cpu.Eax = uint32(sys读取(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys写入:
		cpu.Eax = uint32(sys写入(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case Sys打开:
		cpu.Eax = uint32(sys打开(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case Syscreat:
		cpu.Eax = uint32(sys打开(cpu.Ebx, o创建|o写入仅用|o截断, cpu.Ecx))
		return esp
	case Sys关闭:
		cpu.Eax = uint32(sys关闭(int32(cpu.Ebx)))
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
		cpu.Eax = C当前进程号()
		return esp
	case Sysgetppid:
		cpu.Eax = C当前parent进程号()
		return esp
	case Sysgetuid, Sysgetgid, Sysgeteuid, Sysgetegid:
		cpu.Eax = 0
		return esp
	case Sys访问:
		cpu.Eax = uint32(sys访问(cpu.Ebx, cpu.Ecx))
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
		cpu.Eax = uint32(sys套接字调用(cpu.Ebx, cpu.Ecx))
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
		控制台_2.MUnsignedinteger32打印(cpu.Ebx)
		return esp

	default:
		控制台_2.M打印xy(([]byte)("sys["), 1, 23)
		控制台_2.MUnsignedinteger32打印(esp)
		控制台_2.M打印(([]byte)(":"))
		控制台_2.MUnsignedinteger32打印(cpu.Eax)
		控制台_2.M打印(([]byte)(":"))
		控制台_2.MUnsignedinteger32打印(cpu.Ebx)
		控制台_2.M打印(([]byte)(":"))
		控制台_2.MUnsignedinteger32打印(cpu.Ecx)
		控制台_2.M打印(([]byte)(":"))
		控制台_2.MUnsignedinteger32打印(cpu.Edx)
		控制台_2.M打印(([]byte)("]"))
		cpu.Eax = syscall错误(Enosys)
		return esp
	}

	return esp
}

func init文件descriptor() {
	for i := 0; i < 最大值打开文件; i++ {
		打开文件表格[i] = 打开文件描述{}
	}
	for i := 0; i < len(进程表格); i++ {
		进程表格[i] = 进程条目{}
	}
	for i := 0; i < len(本地sockets); i++ {
		本地sockets[i] = 本地datagram套接字{}
	}
	下一个ephemeral端口 = 49152
	打开文件表格[0] = 打开文件描述{已用: true, 类别: fd类别stdin, 标志: o读取仅用}
	打开文件表格[1] = 打开文件描述{已用: true, 类别: fd类别控制台, 标志: o写入仅用}
	打开文件表格[2] = 打开文件描述{已用: true, 类别: fd类别控制台, 标志: o写入仅用}
}

func 查找进程(进程号 uint32) *进程条目 {
	for i := 0; i < len(进程表格); i++ {
		if 进程表格[i].已用 && 进程表格[i].进程号 == 进程号 {
			return &进程表格[i]
		}
	}
	return nil
}

func initialize进程fds(进程 *进程条目) {
	for fd := int32(0); fd <= stderrfd; fd++ {
		进程.fds[fd] = fd条目{已用: true, 描述: fd}
		打开文件表格[fd].refs++
	}
}

func ensure当前进程() *进程条目 {
	进程号 := C当前进程号()
	if 进程 := 查找进程(进程号); 进程 != nil {
		return 进程
	}
	for i := 0; i < len(进程表格); i++ {
		if !进程表格[i].已用 {
			进程表格[i] = 进程条目{
				已用:		true,
				进程号:		进程号,
				parent:		C当前parent进程号(),
				程序break:	用户heapbase,
			}
			initialize进程fds(&进程表格[i])
			return &进程表格[i]
		}
	}
	return nil
}

func get打开文件for(进程 *进程条目, fd int32) *打开文件描述 {
	if 进程 == nil || fd < 0 || fd >= 最大值fd || !进程.fds[fd].已用 {
		return nil
	}
	描述 := 进程.fds[fd].描述
	if 描述 < 0 || 描述 >= 最大值打开文件 || !打开文件表格[描述].已用 {
		return nil
	}
	return &打开文件表格[描述]
}

func get打开文件(fd int32) *打开文件描述 {
	return get打开文件for(ensure当前进程(), fd)
}

func allocate打开文件() int32 {
	for i := int32(3); i < 最大值打开文件; i++ {
		if !打开文件表格[i].已用 {
			打开文件表格[i] = 打开文件描述{已用: true, refs: 1}
			return i
		}
	}
	return Enfile
}

func allocatefd(进程 *进程条目, 描述 int32, 最小值 int32) int32 {
	if 进程 == nil {
		return Enfile
	}
	if 最小值 < 0 || 最小值 >= 最大值fd {
		return Einval
	}
	for fd := 最小值; fd < 最大值fd; fd++ {
		if !进程.fds[fd].已用 {
			进程.fds[fd] = fd条目{已用: true, 描述: 描述}
			return fd
		}
	}
	return Emfile
}

func release打开文件(描述 int32) {
	if 描述 < 0 || 描述 >= 最大值打开文件 {
		return
	}
	条目 := &打开文件表格[描述]
	if 条目.refs > 0 {
		条目.refs--
	}

	if 条目.refs == 0 && 描述 > stderrfd {
		if 条目.类别 == fd类别套接字 && 条目.aux < 最大值sockets {
			本地sockets[条目.aux] = 本地datagram套接字{}
		}
		*条目 = 打开文件描述{}
	}
}

func 关闭进程fd(进程 *进程条目, fd int32) int32 {
	if 进程 == nil || get打开文件for(进程, fd) == nil {
		return Ebadf
	}
	描述 := 进程.fds[fd].描述
	进程.fds[fd] = fd条目{}
	release打开文件(描述)
	return 0
}

func sys写入(fd int32, address uint32, 计数 uint32) int32 {
	if 计数 == 0 {
		return 0
	}
	if address == 0 || address+计数 < address {
		return Efault
	}
	if 计数 > 4096 {
		return Einval
	}
	条目 := get打开文件(fd)
	if 条目 == nil {
		return Ebadf
	}
	if 条目.类别 != fd类别控制台 {
		if 条目.类别 == fd类别套接字 {
			return 套接字发送to(fd, address, 计数, 0, 0)
		}
		if 条目.类别 == fd类别fat || 条目.类别 == fd类别根目录 {
			return Erofs
		}
		return Ebadf
	}
	buffer := Get字节from指针(uintptr(address), int(计数), int(计数))
	控制台_2.M打印(buffer)
	return int32(计数)
}

func sys读取(fd int32, address uint32, 计数 uint32) int32 {
	if 计数 == 0 {
		return 0
	}
	if address == 0 || address+计数 < address {
		return Efault
	}
	条目 := get打开文件(fd)
	if 条目 == nil {
		return Ebadf
	}
	if 条目.类别 == fd类别stdin {
		return 读取stdin(address, 计数)
	}
	if 条目.类别 == fd类别根目录 {
		return Eisdir
	}
	if 条目.类别 == fd类别套接字 {
		return 套接字receivefrom(fd, address, 计数, 0, 0)
	}
	if 条目.类别 != fd类别fat {
		return Ebadf
	}
	if 条目.位置 >= 条目.大小 {
		return 0
	}
	remaining := 条目.大小 - 条目.位置
	if 计数 > remaining {
		计数 = remaining
	}
	buffer := Get字节from指针(uintptr(address), int(计数), int(计数))
	return 读取vfs文件(条目, buffer, 计数)
}

func sys打开(路径address uint32, 标志 uint32, 模式 uint32) int32 {
	_ = 模式
	if 路径address == 0 {
		return Efault
	}
	访问模式 := 标志 & 3
	if 访问模式 == o写入仅用 || 访问模式 == o读取写入 || (标志&(o创建|o截断|oappend)) != 0 {
		return Erofs
	}

	进程 := ensure当前进程()
	if 进程 == nil {
		return Enfile
	}
	描述 := allocate打开文件()
	if 描述 < 0 {
		return 描述
	}
	条目 := &打开文件表格[描述]
	条目.标志 = 标志
	if is根路径(路径address) {
		条目.类别 = fd类别根目录
		条目.大小 = 0
	} else {
		名称len, 名称 := 复制路径(路径address)
		if 名称len == 0 {
			*条目 = 打开文件描述{}
			return Enoent
		}
		大小 := 文件大小(名称[:名称len])
		if 大小 == 0 {
			*条目 = 打开文件描述{}
			return Enoent
		}
		if (标志 & o目录) != 0 {
			*条目 = 打开文件描述{}
			return Enotdir
		}
		条目.类别 = fd类别fat
		条目.大小 = 大小
		条目.名称len = 名称len
		条目.名称 = 名称
	}

	fd := allocatefd(进程, 描述, 3)
	if fd < 0 {
		*条目 = 打开文件描述{}
		return fd
	}
	return fd
}

func sys关闭(fd int32) int32 {
	return 关闭进程fd(ensure当前进程(), fd)
}

func sysdup(fd int32, 最小值 int32) int32 {
	进程 := ensure当前进程()
	条目 := get打开文件for(进程, fd)
	if 条目 == nil {
		return Ebadf
	}
	新建fd := allocatefd(进程, 进程.fds[fd].描述, 最小值)
	if 新建fd >= 0 {
		条目.refs++
	}
	return 新建fd
}

func sysdup2(oldfd int32, 新建fd int32) int32 {
	进程 := ensure当前进程()
	条目 := get打开文件for(进程, oldfd)
	if 条目 == nil {
		return Ebadf
	}
	if 新建fd < 0 || 新建fd >= 最大值fd {
		return Ebadf
	}
	if oldfd == 新建fd {
		return 新建fd
	}
	if 进程.fds[新建fd].已用 {
		关闭进程fd(进程, 新建fd)
	}
	进程.fds[新建fd] = fd条目{已用: true, 描述: 进程.fds[oldfd].描述}
	条目.refs++
	return 新建fd
}

func sysfcntl(fd int32, 命令 uint32, argument uint32) int32 {
	进程 := ensure当前进程()
	条目 := get打开文件for(进程, fd)
	if 条目 == nil {
		return Ebadf
	}
	switch 命令 {
	case fdupfd:
		return sysdup(fd, int32(argument))
	case fgetfd:
		return int32(进程.fds[fd].fd标志)
	case f集合fd:
		进程.fds[fd].fd标志 = argument & fdcloexec
		return 0
	case fgetfl:
		return int32(条目.标志)
	case f集合fl:
		条目.标志 = (条目.标志 & 3) | (argument & oappend)
		return 0
	}
	return Einval
}

func syslseek(fd int32, 位移 int32, whence uint32) int32 {
	条目 := get打开文件(fd)
	if 条目 == nil {
		return Ebadf
	}
	if 条目.类别 != fd类别fat {
		return Espipe
	}
	var base int64
	switch whence {
	case seek集合:
		base = 0
	case seek当前:
		base = int64(条目.位置)
	case seek结尾:
		base = int64(条目.大小)
	default:
		return Einval
	}
	位置_2 := base + int64(位移)
	if 位置_2 < 0 || 位置_2 > 0x7FFFFFFF {
		return Einval
	}
	条目.位置 = uint32(位置_2)
	return int32(条目.位置)
}

func 读取vfs文件(条目 *打开文件描述, 目的_2 []byte, 计数 uint32) int32 {
	内存管理器 := &mem.T内存管理器{}
	tmp指针 := 内存管理器.M分配内存(条目.大小)
	if tmp指针 == nil {
		return Einval
	}
	tmp := Get字节from指针(uintptr(tmp指针), int(条目.大小), int(条目.大小))
	读取文件(条目.名称[:条目.名称len], tmp)
	copy(目的_2[:计数], tmp[条目.位置:条目.位置+计数])
	条目.位置 += 计数
	内存管理器.F空闲(tmp指针)
	return int32(计数)
}

func is根路径(路径address uint32) bool {
	if 路径address == 0 {
		return false
	}
	路径 := Get字节from指针(uintptr(路径address), 4, 4)
	if 路径[0] == '/' && 路径[1] == 0 {
		return true
	}
	if 路径[0] == '.' && 路径[1] == 0 {
		return true
	}
	if 路径[0] == '/' && 路径[1] == '.' && 路径[2] == 0 {
		return true
	}
	return false
}

func sys访问(路径address uint32, 模式 uint32) int32 {
	if 路径address == 0 {
		return Efault
	}
	if (模式 & ^uint32(7)) != 0 {
		return Einval
	}
	is根 := is根路径(路径address)
	exists := is根
	if !exists {
		名称len, 名称 := 复制路径(路径address)
		exists = 名称len != 0 && 文件大小(名称[:名称len]) != 0
	}
	if !exists {
		return Enoent
	}
	if (模式 & 2) != 0 {
		return Eacces
	}

	if (模式&1) != 0 && !is根 {
		return Eacces
	}
	return 0
}

func syschdir(路径address uint32) int32 {
	if 路径address == 0 {
		return Efault
	}
	if !is根路径(路径address) {
		return Enotdir
	}
	return 0
}

func sysgetcwd(bufferaddress uint32, 大小 uint32) int32 {
	if bufferaddress == 0 {
		return Efault
	}
	if 大小 < 2 {
		return Erange
	}
	buffer_2 := Get字节from指针(uintptr(bufferaddress), int(大小), int(大小))
	buffer_2[0] = '/'
	buffer_2[1] = 0
	return 2
}

func fillposixstat(stataddress uint32, 模式 uint32, 大小 uint32, inode uint32) int32 {
	if stataddress == 0 {
		return Efault
	}
	stat := (*posixstat)(Pointer(uintptr(stataddress)))
	*stat = posixstat{}
	stat.D设备 = 1
	stat.Ino = inode
	stat.M模式 = 模式
	stat.Nlink = 1
	stat.S大小_2 = int32(大小)
	stat.Blksize = 512
	stat.B块 = int32((大小 + 511) / 512)
	return 0
}

func sysstat(路径address uint32, stataddress uint32) int32 {
	if 路径address == 0 {
		return Efault
	}
	if is根路径(路径address) {
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	}
	名称len, 名称 := 复制路径(路径address)
	if 名称len == 0 {
		return Enoent
	}
	大小 := 文件大小(名称[:名称len])
	if 大小 == 0 {
		return Enoent
	}
	inode := uint32(2)
	for i := uint32(0); i < 名称len; i++ {
		inode = inode*33 + uint32(名称[i])
	}
	return fillposixstat(stataddress, sifreg|0444, 大小, inode)
}

func sysfstat(fd int32, stataddress uint32) int32 {
	条目 := get打开文件(fd)
	if 条目 == nil {
		return Ebadf
	}
	switch 条目.类别 {
	case fd类别stdin, fd类别控制台:
		return fillposixstat(stataddress, sifchr|0666, 0, uint32(fd+1))
	case fd类别根目录:
		return fillposixstat(stataddress, sifdir|0555, 0, 1)
	case fd类别fat:
		return fillposixstat(stataddress, sifreg|0444, 条目.大小, uint32(fd+2))
	case fd类别套接字:
		return fillposixstat(stataddress, sifsock|0666, 0, uint32(fd+2))
	}
	return Ebadf
}

func sysfsync(fd int32) int32 {
	if get打开文件(fd) == nil {
		return Ebadf
	}
	return 0
}

func sysbrk(address_2 uint32) uint32 {
	进程 := ensure当前进程()
	if 进程 == nil {
		return 0
	}
	if 进程.程序break == 0 {
		进程.程序break = 用户heapbase
	}
	if address_2 == 0 {
		return 进程.程序break
	}
	if address_2 < 用户heapbase || address_2 > 用户heap限定 {
		return 进程.程序break
	}
	进程.程序break = address_2
	return 进程.程序break
}

func 复制uts字段(目的 *[65]byte, 值 string) {
	限定 := len(值)
	if 限定 > 64 {
		限定 = 64
	}
	for i := 0; i < 限定; i++ {
		目的[i] = 值[i]
	}
	目的[限定] = 0
}

func sysuname(address_2 uint32) int32 {
	if address_2 == 0 {
		return Efault
	}
	名称 := (*posixutsname)(Pointer(uintptr(address_2)))
	*名称 = posixutsname{}
	复制uts字段(&名称.Sysname, "EngOS")
	复制uts字段(&名称.Nodename, "engos")
	复制uts字段(&名称.Release, "0.1-posix")
	复制uts字段(&名称.V版本, "POSIX.1-2017 phase 1")
	复制uts字段(&名称.Machine, "i386")
	return 0
}

func 交换unsignedinteger16(值 uint16) uint16 {
	return (值 << 8) | (值 >> 8)
}

func 套接字调用argument(参数_2 uint32, 索引 uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(参数_2 + 索引*4)))
}

func 套接字forfd(fd int32) (*本地datagram套接字, int32) {
	条目 := get打开文件(fd)
	if 条目 == nil || 条目.类别 != fd类别套接字 || 条目.aux >= 最大值sockets {
		return nil, Ebadf
	}
	套接字 := &本地sockets[条目.aux]
	if !套接字.已用 {
		return nil, Ebadf
	}
	return 套接字, 0
}

func allocate套接字(域 uint32, 套接字类型 uint32, protocol uint32) int32 {
	if 域 != afinet {
		return Eafnosupport
	}
	if 套接字类型 != sockdatagram {
		return Eprotonosupport
	}
	if protocol != 0 && protocol != ipprotocoludp {
		return Eprotonosupport
	}
	进程 := ensure当前进程()
	if 进程 == nil {
		return Enfile
	}
	套接字索引 := -1
	for i := 0; i < 最大值sockets; i++ {
		if !本地sockets[i].已用 {
			套接字索引 = i
			break
		}
	}
	if 套接字索引 < 0 {
		return Enfile
	}
	描述 := allocate打开文件()
	if 描述 < 0 {
		return 描述
	}
	本地sockets[套接字索引] = 本地datagram套接字{已用: true}
	条目 := &打开文件表格[描述]
	条目.类别 = fd类别套接字
	条目.标志 = o读取写入
	条目.aux = uint32(套接字索引)
	fd := allocatefd(进程, 描述, 3)
	if fd < 0 {
		本地sockets[套接字索引] = 本地datagram套接字{}
		*条目 = 打开文件描述{}
		return fd
	}
	return fd
}

func 套接字address(address_2 uint32, 长度 uint32) (*套接字addressipv4, int32) {
	if address_2 == 0 {
		return nil, Efault
	}
	if 长度 < 16 {
		return nil, Einval
	}
	结果 := (*套接字addressipv4)(Pointer(uintptr(address_2)))
	if 结果.Family != afinet {
		return nil, Eafnosupport
	}
	return 结果, 0
}

func 端口进使用(端口 uint16, except *本地datagram套接字) bool {
	for i := 0; i < 最大值sockets; i++ {
		套接字 := &本地sockets[i]
		if 套接字 != except && 套接字.已用 && 套接字.bound && 套接字.本地.P端口 == 端口 {
			return true
		}
	}
	return false
}

func 绑定ephemeral(套接字 *本地datagram套接字) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		端口 := 交换unsignedinteger16(下一个ephemeral端口)
		下一个ephemeral端口++
		if 下一个ephemeral端口 < 49152 {
			下一个ephemeral端口 = 49152
		}
		if !端口进使用(端口, 套接字) {
			套接字.本地 = 套接字addressipv4{Family: afinet, P端口: 端口, Address: 0x0100007F}
			套接字.bound = true
			return 0
		}
	}
	return Eaddrinuse
}

func 套接字绑定(fd int32, address_2 uint32, 长度 uint32) int32 {
	套接字, 错误 := 套接字forfd(fd)
	if 错误 != 0 {
		return 错误
	}
	requested, 错误 := 套接字address(address_2, 长度)
	if 错误 != 0 {
		return 错误
	}
	if 套接字.bound {
		return Einval
	}
	if requested.P端口 == 0 {
		return 绑定ephemeral(套接字)
	}
	if 端口进使用(requested.P端口, 套接字) {
		return Eaddrinuse
	}
	套接字.本地 = *requested
	套接字.bound = true
	return 0
}

func 套接字连接(fd int32, address_2 uint32, 长度 uint32) int32 {
	套接字, 错误 := 套接字forfd(fd)
	if 错误 != 0 {
		return 错误
	}
	远程, 错误 := 套接字address(address_2, 长度)
	if 错误 != 0 {
		return 错误
	}
	if !套接字.bound {
		if 错误 := 绑定ephemeral(套接字); 错误 != 0 {
			return 错误
		}
	}
	套接字.远程 = *远程
	套接字.connected = true
	return 0
}

func 套接字发送to(fd int32, bufferaddress_2 uint32, 长度 uint32, 目的address uint32, 目的长度 uint32) int32 {
	套接字, 错误 := 套接字forfd(fd)
	if 错误 != 0 {
		return 错误
	}
	if 长度 > 最大值datagram大小 {
		return Emsgsize
	}
	if 长度 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	var 目的 套接字addressipv4
	if 目的address != 0 {
		address_2, address错误 := 套接字address(目的address, 目的长度)
		if address错误 != 0 {
			return address错误
		}
		目的 = *address_2
	} else {
		if !套接字.connected {
			return Enotconn
		}
		目的 = 套接字.远程
	}
	if !套接字.bound {
		if 绑定错误 := 绑定ephemeral(套接字); 绑定错误 != 0 {
			return 绑定错误
		}
	}
	var receiver *本地datagram套接字
	for i := 0; i < 最大值sockets; i++ {
		candidate := &本地sockets[i]
		if candidate.已用 && candidate.bound && candidate.本地.P端口 == 目的.P端口 &&
			(candidate.本地.Address == 0 || candidate.本地.Address == 目的.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return Enetunreach
	}
	if receiver.计数 >= 最大值套接字数据包 {
		return Eagain
	}
	packet := &receiver.数据包[receiver.tail]
	*packet = 套接字packet{已用: true, 大小: 长度, 源: 套接字.本地}
	if 长度 != 0 {
		源 := Get字节from指针(uintptr(bufferaddress_2), int(长度), int(长度))
		copy(packet.数据[:长度], 源)
	}
	receiver.tail = (receiver.tail + 1) % 最大值套接字数据包
	receiver.计数++
	return int32(长度)
}

func 套接字receivefrom(fd int32, bufferaddress_2 uint32, 长度 uint32, 源address uint32, 源长度address uint32) int32 {
	套接字, 错误 := 套接字forfd(fd)
	if 错误 != 0 {
		return 错误
	}
	if 长度 != 0 && bufferaddress_2 == 0 {
		return Efault
	}
	if 套接字.计数 == 0 {
		return Eagain
	}
	packet := &套接字.数据包[套接字.head]
	复制长度 := packet.大小
	if 复制长度 > 长度 {
		复制长度 = 长度
	}
	if 复制长度 != 0 {
		目的 := Get字节from指针(uintptr(bufferaddress_2), int(复制长度), int(复制长度))
		copy(目的, packet.数据[:复制长度])
	}
	if 源address != 0 {
		if 源长度address == 0 {
			return Efault
		}
		provided长度 := (*uint32)(Pointer(uintptr(源长度address)))
		if *provided长度 >= 16 {
			*(*套接字addressipv4)(Pointer(uintptr(源address))) = packet.源
		}
		*provided长度 = 16
	}
	*packet = 套接字packet{}
	套接字.head = (套接字.head + 1) % 最大值套接字数据包
	套接字.计数--
	return int32(复制长度)
}

func 复制套接字名称(fd int32, address_2 uint32, 长度address uint32, peer bool) int32 {
	套接字, 错误 := 套接字forfd(fd)
	if 错误 != 0 {
		return 错误
	}
	if address_2 == 0 || 长度address == 0 {
		return Efault
	}
	长度 := (*uint32)(Pointer(uintptr(长度address)))
	if *长度 < 16 {
		*长度 = 16
		return Einval
	}
	if peer {
		if !套接字.connected {
			return Enotconn
		}
		*(*套接字addressipv4)(Pointer(uintptr(address_2))) = 套接字.远程
	} else {
		if !套接字.bound {
			if 绑定错误 := 绑定ephemeral(套接字); 绑定错误 != 0 {
				return 绑定错误
			}
		}
		*(*套接字addressipv4)(Pointer(uintptr(address_2))) = 套接字.本地
	}
	*长度 = 16
	return 0
}

func sys套接字调用(调用 uint32, 参数_2 uint32) int32 {
	if 参数_2 == 0 {
		return Efault
	}
	switch 调用 {
	case 1:
		return allocate套接字(套接字调用argument(参数_2, 0), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2))
	case 2:
		return 套接字绑定(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2))
	case 3:
		return 套接字连接(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2))
	case 4, 5:
		return Eopnotsupp
	case 6:
		return 复制套接字名称(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), false)
	case 7:
		return 复制套接字名称(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), true)
	case 9:
		return 套接字发送to(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), 0, 0)
	case 10:
		return 套接字receivefrom(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), 0, 0)
	case 11:
		return 套接字发送to(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), 套接字调用argument(参数_2, 4), 套接字调用argument(参数_2, 5))
	case 12:
		return 套接字receivefrom(int32(套接字调用argument(参数_2, 0)), 套接字调用argument(参数_2, 1), 套接字调用argument(参数_2, 2), 套接字调用argument(参数_2, 4), 套接字调用argument(参数_2, 5))
	case 13:
		if _, 错误 := 套接字forfd(int32(套接字调用argument(参数_2, 0))); 错误 != 0 {
			return 错误
		}
		return 0
	case 14:
		if _, 错误 := 套接字forfd(int32(套接字调用argument(参数_2, 0))); 错误 != 0 {
			return 错误
		}
		return 0
	}
	return Eopnotsupp
}

func 读取stdin(address uint32, 计数 uint32) int32 {
	if address == 0 {
		return Einval
	}
	buffer := Get字节from指针(uintptr(address), int(计数), int(计数))
	var n uint32
	for n < 计数 {
		c := stdingetblocking()
		buffer[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func Stdinput字节(c byte) {
	下一个 := (stdin写入 + 1) % uint32(len(stdinbuffer))
	if 下一个 == stdin读取 {
		return
	}
	stdinbuffer[stdin写入] = c
	stdin写入 = 下一个
}

func stdingetblocking() byte {
	for stdin读取 == stdin写入 {
		sc := poll键盘scancode()
		if sc != 0 {
			Stdinput字节(sc)
		}
	}
	c := stdinbuffer[stdin读取]
	stdin读取 = (stdin读取 + 1) % uint32(len(stdinbuffer))
	return c
}

func poll键盘scancode() byte {
	for (P端口读取字节(0x64) & 0x01) == 0 {
	}
	sc := P端口读取字节(0x60)
	return scancodeto字节(sc)
}

func scancodeto字节(sc uint8) byte {
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

func 复制执行vector(address_2 uint32, 结果 *执行vector) int32 {
	*结果 = 执行vector{}
	if address_2 == 0 {
		return 0
	}
	for 索引 := uint32(0); 索引 < 最大值执行vector条目; 索引++ {
		字符串address := *(*uint32)(Pointer(uintptr(address_2 + 索引*4)))
		if 字符串address == 0 {
			结果.计数 = 索引
			return 0
		}
		terminated := false
		for 长度 := uint32(0); 长度 <= 最大值执行字符串长度; 长度++ {
			值 := *(*byte)(Pointer(uintptr(字符串address + 长度)))
			结果.文字[索引][长度] = 值
			if 值 == 0 {
				结果.lengths[索引] = 长度
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

func push执行unsignedinteger32(栈存储区 *uint32, 值 uint32) {
	*栈存储区 -= 4
	*(*uint32)(Pointer(uintptr(*栈存储区))) = 值
}

func setup执行stack(cpu *Tcpu状态, 参数_2 *执行vector, environment *执行vector) int32 {
	const stack字节 uint32 = 4096
	if !Make范围专用writable(getcr3(), U用户stack上-stack字节, stack字节) {
		return Enomem
	}
	栈存储区 := U用户stack上
	var argumentpointers [最大值执行vector条目]uint32
	var environmentpointers [最大值执行vector条目]uint32

	for i := int(environment.计数) - 1; i >= 0; i-- {
		长度 := environment.lengths[i] + 1
		栈存储区 -= 长度
		目的 := Get字节from指针(uintptr(栈存储区), int(长度), int(长度))
		copy(目的, environment.文字[i][:长度])
		environmentpointers[i] = 栈存储区
	}
	for i := int(参数_2.计数) - 1; i >= 0; i-- {
		长度 := 参数_2.lengths[i] + 1
		栈存储区 -= 长度
		目的 := Get字节from指针(uintptr(栈存储区), int(长度), int(长度))
		copy(目的, 参数_2.文字[i][:长度])
		argumentpointers[i] = 栈存储区
	}
	栈存储区 &= ^uint32(3)
	push执行unsignedinteger32(&栈存储区, 0)
	for i := int(environment.计数) - 1; i >= 0; i-- {
		push执行unsignedinteger32(&栈存储区, environmentpointers[i])
	}
	push执行unsignedinteger32(&栈存储区, 0)
	for i := int(参数_2.计数) - 1; i >= 0; i-- {
		push执行unsignedinteger32(&栈存储区, argumentpointers[i])
	}
	push执行unsignedinteger32(&栈存储区, 参数_2.计数)
	cpu.Esp = 栈存储区
	cpu.Ebp = 0
	return 0
}

func 关闭时执行(进程 *进程条目) {
	if 进程 == nil {
		return
	}
	for fd := int32(0); fd < 最大值fd; fd++ {
		if 进程.fds[fd].已用 && (进程.fds[fd].fd标志&fdcloexec) != 0 {
			关闭进程fd(进程, fd)
		}
	}
}

func sysexecve(cpu *Tcpu状态, 路径address uint32) int32 {
	if 路径address == 0 {
		return Efault
	}
	var 参数_2 执行vector
	var environment 执行vector
	if 结果 := 复制执行vector(cpu.Ecx, &参数_2); 结果 < 0 {
		return 结果
	}
	if 结果 := 复制执行vector(cpu.Edx, &environment); 结果 < 0 {
		return 结果
	}
	名称len, 名称 := 复制路径(路径address)
	if 名称len == 0 {
		return Enoent
	}
	大小 := 文件大小(名称[:名称len])
	if 大小 == 0 {
		return Enoent
	}
	内存管理器 := &mem.T内存管理器{}
	文件指针 := 内存管理器.M分配内存(大小)
	if 文件指针 == nil {
		return Einval
	}
	数据 := Get字节from指针(uintptr(文件指针), int(大小), int(大小))
	读取文件(名称[:名称len], 数据)
	if 大小 < 52 || 数据[0] != 0x7F || 数据[1] != 'E' || 数据[2] != 'L' || 数据[3] != 'F' {
		内存管理器.F空闲(文件指针)
		return Enoexec
	}
	loader := Elf{}
	条目 := loader.Get条目(数据)
	loader.Parse(数据, getcr3())
	内存管理器.F空闲(文件指针)
	if 结果 := setup执行stack(cpu, &参数_2, &environment); 结果 < 0 {
		return 结果
	}
	关闭时执行(ensure当前进程())
	cpu.Eip = 条目
	cpu.Eax = 0
	return 0
}

func sysfork(cpu *Tcpu状态) int32 {
	parent进程号 := C当前进程号()
	if ensure当前进程() == nil {
		return Enfile
	}
	进程号 := allocate进程(parent进程号)
	if 进程号 == 0 {
		return Einval
	}
	内存管理器 := &mem.T内存管理器{}
	线程指针 := 内存管理器.M分配内存(uint32(Sizeof(T线程{})))
	stack指针 := 内存管理器.M分配内存(T线程stack大小)
	child页目录 := Cloneaddress空格cow(getcr3())
	if 线程指针 == nil || stack指针 == nil || child页目录 == 0 {
		忽略进程(进程号)
		return Einval
	}
	child := (*T线程)(线程指针)
	child.Stack = uint32(uintptr(stack指针))
	child.Cpu状态 = (*Tcpu状态)(Pointer(uintptr(stack指针) + T线程stack大小 - Sizeof(Tcpu状态{})))
	*child.Cpu状态 = *cpu
	child.Cpu状态.Eax = 0
	child.U用户stack_2 = cpu.Esp
	child.U用户stack大小_2 = 0
	child.P进程号 = 进程号
	child.Parent进程号 = parent进程号
	child.P页目录条目 = child页目录
	child.T线程状态 = R就绪
	child.Fpu位移 = 0xffffffff
	child.Is内核 = false
	A添加runnable线程(child)
	return int32(进程号)
}

func sys退出(状态 uint32) {
	进程号 := C当前进程号()
	for i := 0; i < len(进程表格); i++ {
		if 进程表格[i].已用 && 进程表格[i].进程号 == 进程号 {
			关闭全部进程fds(&进程表格[i])
			进程表格[i].已退出 = true
			进程表格[i].状态 = (状态 & 0xFF) << 8
			return
		}
	}
}

func syswaitpid(进程号 int32, 状态address uint32, 选项 uint32) int32 {
	if (选项 & ^uint32(1)) != 0 {
		return Einval
	}
	parent进程号 := C当前进程号()
	foundchild := false
	for i := 0; i < len(进程表格); i++ {
		p := &进程表格[i]
		matches := 进程号 == -1 || 进程号 == 0 || p.进程号 == uint32(进程号)
		if p.已用 && matches && p.parent == parent进程号 {
			foundchild = true
			if p.已退出 {
				if 状态address != 0 {
					*(*uint32)(Pointer(uintptr(状态address))) = p.状态
				}
				child进程号 := p.进程号
				*p = 进程条目{}
				return int32(child进程号)
			}
		}
	}
	if !foundchild {
		return Echild
	}

	if (选项 & 1) != 0 {
		return 0
	}
	return Eagain
}

func allocate进程(parent uint32) uint32 {
	parent进程 := 查找进程(parent)
	进程号 := Allocate进程号()
	for i := 0; i < len(进程表格); i++ {
		if !进程表格[i].已用 {
			进程表格[i] = 进程条目{
				已用:		true,
				进程号:		进程号,
				parent:		parent,
				程序break:	用户heapbase,
			}
			if parent进程 != nil {
				进程表格[i].程序break = parent进程.程序break
				for fd := 0; fd < 最大值fd; fd++ {
					if parent进程.fds[fd].已用 {
						进程表格[i].fds[fd] = parent进程.fds[fd]
						描述 := parent进程.fds[fd].描述
						if 描述 >= 0 && 描述 < 最大值打开文件 {
							打开文件表格[描述].refs++
						}
					}
				}
			} else {
				initialize进程fds(&进程表格[i])
			}
			return 进程号
		}
	}
	return 0
}

func 关闭全部进程fds(进程 *进程条目) {
	if 进程 == nil {
		return
	}
	for fd := int32(0); fd < 最大值fd; fd++ {
		if 进程.fds[fd].已用 {
			关闭进程fd(进程, fd)
		}
	}
}

func 忽略进程(进程号 uint32) {
	进程 := 查找进程(进程号)
	if 进程 == nil {
		return
	}
	关闭全部进程fds(进程)
	*进程 = 进程条目{}
}

func 复制路径(路径address uint32) (uint32, [12]byte) {
	var 名称 [12]byte
	if 路径address == 0 {
		return 0, 名称
	}
	raw := Get字节from指针(uintptr(路径address), 64, 64)
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
		名称[n] = c
		n++
	}
	return n, 名称
}

func 文件大小(文件名 []byte) uint32 {
	var ata0s = T高级技术attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分区 := Tmsdos分区表格{}
	分区.R读取分区(&ata0s)

	bios := T文件系统参数32{}
	大小 := bios.Len(&ata0s, 分区.Mbr.Primary分区[0], 文件名)
	ata0s.Flush()
	return 大小
}

func 读取文件(文件名 []byte, 数据 []byte) {
	var ata0s = T高级技术attachment{}
	ata0s.Init(false, 0x1F0)
	ata0s.Identify()

	分区 := Tmsdos分区表格{}
	分区.R读取分区(&ata0s)

	bios := T文件系统参数32{}
	bios.R读取(&ata0s, 分区.Mbr.Primary分区[0], 文件名, 数据)
	ata0s.Flush()
}

func getcr3() uint32
