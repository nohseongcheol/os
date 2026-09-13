package प्रणाली_आह्वान

import . "unsafe"

import . "interrupt"
import . "console"
import . "util"
import . "multitasking"
import . "drivers/ata"
import . "filesystem/msdospart"
import . "filesystem/fat"
import . "filesystem/elf"
import mem "स्मृति"
import . "paging"
import . "port"
import . "tasking/scheduler"
import . "tasking/निष्पादन_धारा"
import . "virtmem"

var 콘솔 = T콘솔{}

type TSyscall struct {
	TInterruptHandler
}

const (
	SYS_EXIT		uint32	= 1
	SYS_FORK		uint32	= 2
	SYS_READ	uint32	= 3
	SYS_WRITE	uint32	= 4
	SYS_OPEN		uint32	= 5
	SYS_CLOSE	uint32	= 6
	SYS_WAITPID	uint32	= 7
	SYS_CREAT	uint32	= 8
	SYS_EXECVE	uint32	= 11
	SYS_CHDIR	uint32	= 12
	SYS_LSEEK	uint32	= 19
	SYS_GETPID	uint32	= 20
	SYS_GETUID	uint32	= 24
	SYS_ACCESS	uint32	= 33
	SYS_SYNC		uint32	= 36
	SYS_DUP		uint32	= 41
	SYS_BRK		uint32	= 45
	SYS_GETGID	uint32	= 47
	SYS_GETEUID	uint32	= 49
	SYS_GETEGID	uint32	= 50
	SYS_FCNTL	uint32	= 55
	SYS_DUP2		uint32	= 63
	SYS_GETPPID	uint32	= 64
	SYS_SOCKETCALL	uint32	= 102
	SYS_STAT		uint32	= 106
	SYS_LSTAT	uint32	= 107
	SYS_FSTAT	uint32	= 108
	SYS_FSYNC	uint32	= 118
	SYS_UNAME	uint32	= 122
	SYS_GETCWD	uint32	= 183
	SYS_RT_EXIT	uint32	= 252

	EPERM		int32	= -1
	ENOENT		int32	= -2
	ESRCH		int32	= -3
	EINTR		int32	= -4
	EIO		int32	= -5
	E2BIG		int32	= -7
	ENOEXEC		int32	= -8
	EBADF		int32	= -9
	ECHILD		int32	= -10
	EAGAIN		int32	= -11
	ENOMEM		int32	= -12
	EACCES		int32	= -13
	EFAULT		int32	= -14
	EBUSY		int32	= -16
	EEXIST		int32	= -17
	ENODEV		int32	= -19
	ENOTDIR		int32	= -20
	EISDIR		int32	= -21
	EINVAL		int32	= -22
	ENFILE		int32	= -23
	EMFILE		int32	= -24
	ENOTTY		int32	= -25
	EFBIG		int32	= -27
	ENOSPC		int32	= -28
	ESPIPE		int32	= -29
	EROFS		int32	= -30
	ERANGE		int32	= -34
	ENOSYS		int32	= -38
	EMSGSIZE	int32	= -90
	EPROTONOSUPPORT	int32	= -93
	EOPNOTSUPP	int32	= -95
	EAFNOSUPPORT	int32	= -97
	EADDRINUSE	int32	= -98
	ENETUNREACH	int32	= -101
	ENOTCONN	int32	= -107
)

const (
	stdinFD		int32	= 0
	stdoutFD	int32	= 1
	stderrFD	int32	= 2
	maxFD			= 32
	maxOpenFiles		= 128
)

type fdEntry struct {
	used		bool
	description	int32
	fdFlags		uint32
}

type openFileDescription struct {
	used		bool
	refs		uint32
	kind		uint32
	flags		uint32
	pos	uint32
	आकार		uint32
	name		[12]byte
	nameLen		uint32
	aux		uint32
}

const (
	fdKindNone		uint32	= 0
	fdKindFat		uint32	= 1
	fdKindStdin		uint32	= 2
	fdKindConsole		uint32	= 3
	fdKindRootDir	uint32	= 4
	fdKindSocket		uint32	= 5

	oReadOnly	uint32	= 0
	oWriteOnly	uint32	= 1
	oReadWrite	uint32	= 2
	oCreate		uint32	= 0x40
	oTruncate	uint32	= 0x200
	oAppend		uint32	= 0x400
	oDirectory	uint32	= 0x10000

	seekSet		uint32	= 0
	seekCur	uint32	= 1
	seekEnd		uint32	= 2

	fDupFD		uint32	= 0
	fGetFD		uint32	= 1
	fSetFD		uint32	= 2
	fGetFL		uint32	= 3
	fSetFL		uint32	= 4
	fdCloexec	uint32	= 1

	sIfmt	uint32	= 0170000
	sIfdir	uint32	= 0040000
	sIfreg	uint32	= 0100000
	sIfchr	uint32	= 0020000
	sIfsock	uint32	= 0140000
)

const (
	afInet			= 2
	sockDatagram		= 2
	ipProtocolUDP		= 17
	maxSockets		= 32
	maxSocketPackets	= 8
	maxDatagramSize		= 512
)

type socketAddressIPv4 struct {
	Family	uint16
	Port	uint16
	Address	uint32
	Zero	[8]byte
}

type socketPacket struct {
	used	bool
	आकार	uint32
	source	socketAddressIPv4
	data	[maxDatagramSize]byte
}

type localDatagramSocket struct {
	used		bool
	bound		bool
	connected	bool
	local		socketAddressIPv4
	remote		socketAddressIPv4
	head		uint32
	tail		uint32
	count		uint32
	packets		[maxSocketPackets]socketPacket
}

type posixStat struct {
	Dev		uint32
	Ino		uint32
	Mode		uint32
	Nlink		uint32
	Uid		uint32
	Gid		uint32
	Rdev		uint32
	Vआकार		int32
	Blksize		int32
	Blocks		int32
	Atime		int32
	AtimeNsec	int32
	Mtime		int32
	MtimeNsec	int32
	Ctime		int32
	CtimeNsec	int32
}

type posixUtsname struct {
	Sysname		[65]byte
	Nodename	[65]byte
	Release		[65]byte
	Version		[65]byte
	Machine		[65]byte
}

const (
	maxExecVectorEntries	= 16
	maxExecStringLength	= 63
)

type execVector struct {
	count	uint32
	lengths	[maxExecVectorEntries]uint32
	values	[maxExecVectorEntries][maxExecStringLength + 1]byte
}

type processEntry struct {
	used		bool
	pid		uint32
	parent		uint32
	exited		bool
	status		uint32
	programBreak	uint32
	fds		[maxFD]fdEntry
}

type stringHeader struct {
	Data	uintptr
	Len	int
}

func syscallError(err int32) uint32 {
	return *(*uint32)(Pointer(&err))
}

var openFileTable [maxOpenFiles]openFileDescription
var processTable [32]processEntry
var localSockets [maxSockets]localDatagramSocket
var nextEphemeralPort uint16 = 49152

const (
	userHeapBase	uint32	= 0x06000000
	userHeapLimit	uint32	= 0x07000000
)

var stdinBuffer [128]byte
var stdinRead uint32
var stdinWrite uint32

func Interrupt(eax, ebx, ecx, edx, esi, edi uint32) uint32

func Sys_exit(index uint32) {
	Syscall(SYS_EXIT, index)
}

func Sys_read(fd uint32, buf []byte) int32 {
	if len(buf) == 0 {
		return 0
	}
	return int32(Syscall(SYS_READ, fd, uint32(uintptr(Pointer(&buf[0]))), uint32(len(buf))))
}

func Sys_printStr(buf string) {
	h := (*stringHeader)(Pointer(&buf))
	Syscall(SYS_WRITE, uint32(stdoutFD), uint32(h.Data), uint32(h.Len))
}

func Sys_printUint32(buf uint32) {
	Syscall(9, buf)
}

func Sys_printf(buf []byte) {
	if len(buf) == 0 {
		return
	}
	Syscall(SYS_WRITE, uint32(stdoutFD), uint32(uintptr(Pointer(&buf[0]))), uint32(len(buf)))
}

func Sys_mousemove(x uint, y uint) {
	var eax uint32 = 100
	Syscall(eax, uint32(x), uint32(y))
}

func Sys_open(path uintptr, flags uint32, mode uint32) int32 {
	return int32(Syscall(SYS_OPEN, uint32(path), flags, mode))
}

func Sys_close(fd uint32) int32 {
	return int32(Syscall(SYS_CLOSE, fd))
}

func Sys_getpid() uint32 {
	return Syscall(SYS_GETPID)
}

func Sys_brk(addr uint32) uint32 {
	return Syscall(SYS_BRK, addr)
}

func Syscall(params ...uint32) uint32 {

	l := len(params)
	switch l {
	case 1:
		return Interrupt(params[0], 0, 0, 0, 0, 0)
	case 2:
		return Interrupt(params[0], params[1], 0, 0, 0, 0)
	case 3:
		return Interrupt(params[0], params[1], params[2], 0, 0, 0)
	case 4:
		return Interrupt(params[0], params[1], params[2], params[3], 0, 0)
	case 5:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], 0)
	case 6:
		return Interrupt(params[0], params[1], params[2], params[3], params[4], params[5])
	default:
		return syscallError(ENOSYS)
	}
}

func (self *TSyscall) Vआरंभ_करब(manager *TInterruptManager) {
	initFileDescriptors()

	interruptHandler = handleInterrupt

	var addr uintptr
	addr = uintptr(Pointer(&interruptHandler))

	self.TInterruptHandler.Vआरंभ_करब(0x80, uintptr(Pointer(manager)), addr)
}

var interruptHandler func(uint32) uint32

func handleInterrupt(esp uint32) uint32 {
	var cpu = (*TCPUState)(Pointer(uintptr(esp)))

	switch cpu.Eax {
	case SYS_EXIT:
		sysExit(cpu.Ebx)
		return uint32(uintptr(Pointer(StopCurrentThread(cpu))))
	case SYS_RT_EXIT:
		sysExit(cpu.Ebx)
		return uint32(uintptr(Pointer(StopCurrentThread(cpu))))
	case SYS_FORK:
		cpu.Eax = uint32(sysFork(cpu))
		return esp
	case SYS_READ:
		cpu.Eax = uint32(sysRead(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SYS_WRITE:
		cpu.Eax = uint32(sysWrite(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SYS_OPEN:
		cpu.Eax = uint32(sysOpen(cpu.Ebx, cpu.Ecx, cpu.Edx))
		return esp
	case SYS_CREAT:
		cpu.Eax = uint32(sysOpen(cpu.Ebx, oCreate|oWriteOnly|oTruncate, cpu.Ecx))
		return esp
	case SYS_CLOSE:
		cpu.Eax = uint32(sysClose(int32(cpu.Ebx)))
		return esp
	case SYS_WAITPID:
		cpu.Eax = uint32(sysWaitpid(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SYS_LSEEK:
		cpu.Eax = uint32(sysLseek(int32(cpu.Ebx), int32(cpu.Ecx), cpu.Edx))
		return esp
	case SYS_EXECVE:
		cpu.Eax = uint32(sysExecve(cpu, cpu.Ebx))
		return esp
	case SYS_GETPID:
		cpu.Eax = CurrentPID()
		return esp
	case SYS_GETPPID:
		cpu.Eax = CurrentParentPID()
		return esp
	case SYS_GETUID, SYS_GETGID, SYS_GETEUID, SYS_GETEGID:
		cpu.Eax = 0
		return esp
	case SYS_ACCESS:
		cpu.Eax = uint32(sysAccess(cpu.Ebx, cpu.Ecx))
		return esp
	case SYS_CHDIR:
		cpu.Eax = uint32(sysChdir(cpu.Ebx))
		return esp
	case SYS_GETCWD:
		cpu.Eax = uint32(sysGetcwd(cpu.Ebx, cpu.Ecx))
		return esp
	case SYS_DUP:
		cpu.Eax = uint32(sysDup(int32(cpu.Ebx), 0))
		return esp
	case SYS_DUP2:
		cpu.Eax = uint32(sysDup2(int32(cpu.Ebx), int32(cpu.Ecx)))
		return esp
	case SYS_SOCKETCALL:
		cpu.Eax = uint32(sysSocketCall(cpu.Ebx, cpu.Ecx))
		return esp
	case SYS_FCNTL:
		cpu.Eax = uint32(sysFcntl(int32(cpu.Ebx), cpu.Ecx, cpu.Edx))
		return esp
	case SYS_STAT, SYS_LSTAT:
		cpu.Eax = uint32(sysStat(cpu.Ebx, cpu.Ecx))
		return esp
	case SYS_FSTAT:
		cpu.Eax = uint32(sysFstat(int32(cpu.Ebx), cpu.Ecx))
		return esp
	case SYS_FSYNC:
		cpu.Eax = uint32(sysFsync(int32(cpu.Ebx)))
		return esp
	case SYS_SYNC:
		cpu.Eax = 0
		return esp
	case SYS_UNAME:
		cpu.Eax = uint32(sysUname(cpu.Ebx))
		return esp
	case SYS_BRK:
		cpu.Eax = sysBrk(cpu.Ebx)
		return esp
	case 9:
		콘솔.MUint32출력(cpu.Ebx)
		return esp

	default:
		콘솔.M출력XY(([]byte)("sys["), 1, 23)
		콘솔.MUint32출력(esp)
		콘솔.M출력(([]byte)(":"))
		콘솔.MUint32출력(cpu.Eax)
		콘솔.M출력(([]byte)(":"))
		콘솔.MUint32출력(cpu.Ebx)
		콘솔.M출력(([]byte)(":"))
		콘솔.MUint32출력(cpu.Ecx)
		콘솔.M출력(([]byte)(":"))
		콘솔.MUint32출력(cpu.Edx)
		콘솔.M출력(([]byte)("]"))
		cpu.Eax = syscallError(ENOSYS)
		return esp
	}

	return esp
}

func initFileDescriptors() {
	for i := 0; i < maxOpenFiles; i++ {
		openFileTable[i] = openFileDescription{}
	}
	for i := 0; i < len(processTable); i++ {
		processTable[i] = processEntry{}
	}
	for i := 0; i < len(localSockets); i++ {
		localSockets[i] = localDatagramSocket{}
	}
	nextEphemeralPort = 49152
	openFileTable[0] = openFileDescription{used: true, kind: fdKindStdin, flags: oReadOnly}
	openFileTable[1] = openFileDescription{used: true, kind: fdKindConsole, flags: oWriteOnly}
	openFileTable[2] = openFileDescription{used: true, kind: fdKindConsole, flags: oWriteOnly}
}

func findProcess(pid uint32) *processEntry {
	for i := 0; i < len(processTable); i++ {
		if processTable[i].used && processTable[i].pid == pid {
			return &processTable[i]
		}
	}
	return nil
}

func initializeProcessFDs(process *processEntry) {
	for fd := int32(0); fd <= stderrFD; fd++ {
		process.fds[fd] = fdEntry{used: true, description: fd}
		openFileTable[fd].refs++
	}
}

func ensureCurrentProcess() *processEntry {
	pid := CurrentPID()
	if process := findProcess(pid); process != nil {
		return process
	}
	for i := 0; i < len(processTable); i++ {
		if !processTable[i].used {
			processTable[i] = processEntry{
				used:		true,
				pid:		pid,
				parent:		CurrentParentPID(),
				programBreak:	userHeapBase,
			}
			initializeProcessFDs(&processTable[i])
			return &processTable[i]
		}
	}
	return nil
}

func getOpenFileFor(process *processEntry, fd int32) *openFileDescription {
	if process == nil || fd < 0 || fd >= maxFD || !process.fds[fd].used {
		return nil
	}
	description := process.fds[fd].description
	if description < 0 || description >= maxOpenFiles || !openFileTable[description].used {
		return nil
	}
	return &openFileTable[description]
}

func getOpenFile(fd int32) *openFileDescription {
	return getOpenFileFor(ensureCurrentProcess(), fd)
}

func allocOpenFile() int32 {
	for i := int32(3); i < maxOpenFiles; i++ {
		if !openFileTable[i].used {
			openFileTable[i] = openFileDescription{used: true, refs: 1}
			return i
		}
	}
	return ENFILE
}

func allocFD(process *processEntry, description int32, minimum int32) int32 {
	if process == nil {
		return ENFILE
	}
	if minimum < 0 || minimum >= maxFD {
		return EINVAL
	}
	for fd := minimum; fd < maxFD; fd++ {
		if !process.fds[fd].used {
			process.fds[fd] = fdEntry{used: true, description: description}
			return fd
		}
	}
	return EMFILE
}

func releaseOpenFile(description int32) {
	if description < 0 || description >= maxOpenFiles {
		return
	}
	entry := &openFileTable[description]
	if entry.refs > 0 {
		entry.refs--
	}

	if entry.refs == 0 && description > stderrFD {
		if entry.kind == fdKindSocket && entry.aux < maxSockets {
			localSockets[entry.aux] = localDatagramSocket{}
		}
		*entry = openFileDescription{}
	}
}

func closeProcessFD(process *processEntry, fd int32) int32 {
	if process == nil || getOpenFileFor(process, fd) == nil {
		return EBADF
	}
	description := process.fds[fd].description
	process.fds[fd] = fdEntry{}
	releaseOpenFile(description)
	return 0
}

func sysWrite(fd int32, addr uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if addr == 0 || addr+count < addr {
		return EFAULT
	}
	if count > 4096 {
		return EINVAL
	}
	entry := getOpenFile(fd)
	if entry == nil {
		return EBADF
	}
	if entry.kind != fdKindConsole {
		if entry.kind == fdKindSocket {
			return socketSendTo(fd, addr, count, 0, 0)
		}
		if entry.kind == fdKindFat || entry.kind == fdKindRootDir {
			return EROFS
		}
		return EBADF
	}
	buf := GetBytesFromPtr(uintptr(addr), int(count), int(count))
	콘솔.M출력(buf)
	return int32(count)
}

func sysRead(fd int32, addr uint32, count uint32) int32 {
	if count == 0 {
		return 0
	}
	if addr == 0 || addr+count < addr {
		return EFAULT
	}
	entry := getOpenFile(fd)
	if entry == nil {
		return EBADF
	}
	if entry.kind == fdKindStdin {
		return readStdin(addr, count)
	}
	if entry.kind == fdKindRootDir {
		return EISDIR
	}
	if entry.kind == fdKindSocket {
		return socketReceiveFrom(fd, addr, count, 0, 0)
	}
	if entry.kind != fdKindFat {
		return EBADF
	}
	if entry.pos >= entry.आकार {
		return 0
	}
	remaining := entry.आकार - entry.pos
	if count > remaining {
		count = remaining
	}
	buf := GetBytesFromPtr(uintptr(addr), int(count), int(count))
	return readVFSFile(entry, buf, count)
}

func sysOpen(pathAddr uint32, flags uint32, mode uint32) int32 {
	_ = mode
	if pathAddr == 0 {
		return EFAULT
	}
	accessMode := flags & 3
	if accessMode == oWriteOnly || accessMode == oReadWrite || (flags&(oCreate|oTruncate|oAppend)) != 0 {
		return EROFS
	}

	process := ensureCurrentProcess()
	if process == nil {
		return ENFILE
	}
	description := allocOpenFile()
	if description < 0 {
		return description
	}
	entry := &openFileTable[description]
	entry.flags = flags
	if isRootPath(pathAddr) {
		entry.kind = fdKindRootDir
		entry.आकार = 0
	} else {
		nameLen, name := copyPath(pathAddr)
		if nameLen == 0 {
			*entry = openFileDescription{}
			return ENOENT
		}
		आकार := fileSize(name[:nameLen])
		if आकार == 0 {
			*entry = openFileDescription{}
			return ENOENT
		}
		if (flags & oDirectory) != 0 {
			*entry = openFileDescription{}
			return ENOTDIR
		}
		entry.kind = fdKindFat
		entry.आकार = आकार
		entry.nameLen = nameLen
		entry.name = name
	}

	fd := allocFD(process, description, 3)
	if fd < 0 {
		*entry = openFileDescription{}
		return fd
	}
	return fd
}

func sysClose(fd int32) int32 {
	return closeProcessFD(ensureCurrentProcess(), fd)
}

func sysDup(fd int32, minimum int32) int32 {
	process := ensureCurrentProcess()
	entry := getOpenFileFor(process, fd)
	if entry == nil {
		return EBADF
	}
	newFD := allocFD(process, process.fds[fd].description, minimum)
	if newFD >= 0 {
		entry.refs++
	}
	return newFD
}

func sysDup2(oldFD int32, newFD int32) int32 {
	process := ensureCurrentProcess()
	entry := getOpenFileFor(process, oldFD)
	if entry == nil {
		return EBADF
	}
	if newFD < 0 || newFD >= maxFD {
		return EBADF
	}
	if oldFD == newFD {
		return newFD
	}
	if process.fds[newFD].used {
		closeProcessFD(process, newFD)
	}
	process.fds[newFD] = fdEntry{used: true, description: process.fds[oldFD].description}
	entry.refs++
	return newFD
}

func sysFcntl(fd int32, command uint32, argument uint32) int32 {
	process := ensureCurrentProcess()
	entry := getOpenFileFor(process, fd)
	if entry == nil {
		return EBADF
	}
	switch command {
	case fDupFD:
		return sysDup(fd, int32(argument))
	case fGetFD:
		return int32(process.fds[fd].fdFlags)
	case fSetFD:
		process.fds[fd].fdFlags = argument & fdCloexec
		return 0
	case fGetFL:
		return int32(entry.flags)
	case fSetFL:
		entry.flags = (entry.flags & 3) | (argument & oAppend)
		return 0
	}
	return EINVAL
}

func sysLseek(fd int32, offset int32, whence uint32) int32 {
	entry := getOpenFile(fd)
	if entry == nil {
		return EBADF
	}
	if entry.kind != fdKindFat {
		return ESPIPE
	}
	var base int64
	switch whence {
	case seekSet:
		base = 0
	case seekCur:
		base = int64(entry.pos)
	case seekEnd:
		base = int64(entry.आकार)
	default:
		return EINVAL
	}
	position := base + int64(offset)
	if position < 0 || position > 0x7FFFFFFF {
		return EINVAL
	}
	entry.pos = uint32(position)
	return int32(entry.pos)
}

func readVFSFile(entry *openFileDescription, dst []byte, count uint32) int32 {
	memoryManager := &mem.TMemoryManager{}
	tmpPtr := memoryManager.Malloc(entry.आकार)
	if tmpPtr == nil {
		return EINVAL
	}
	tmp := GetBytesFromPtr(uintptr(tmpPtr), int(entry.आकार), int(entry.आकार))
	readFile(entry.name[:entry.nameLen], tmp)
	copy(dst[:count], tmp[entry.pos:entry.pos+count])
	entry.pos += count
	memoryManager.Free(tmpPtr)
	return int32(count)
}

func isRootPath(pathAddr uint32) bool {
	if pathAddr == 0 {
		return false
	}
	path := GetBytesFromPtr(uintptr(pathAddr), 4, 4)
	if path[0] == '/' && path[1] == 0 {
		return true
	}
	if path[0] == '.' && path[1] == 0 {
		return true
	}
	if path[0] == '/' && path[1] == '.' && path[2] == 0 {
		return true
	}
	return false
}

func sysAccess(pathAddr uint32, mode uint32) int32 {
	if pathAddr == 0 {
		return EFAULT
	}
	if (mode & ^uint32(7)) != 0 {
		return EINVAL
	}
	isRoot := isRootPath(pathAddr)
	exists := isRoot
	if !exists {
		nameLen, name := copyPath(pathAddr)
		exists = nameLen != 0 && fileSize(name[:nameLen]) != 0
	}
	if !exists {
		return ENOENT
	}
	if (mode & 2) != 0 {
		return EACCES
	}

	if (mode&1) != 0 && !isRoot {
		return EACCES
	}
	return 0
}

func sysChdir(pathAddr uint32) int32 {
	if pathAddr == 0 {
		return EFAULT
	}
	if !isRootPath(pathAddr) {
		return ENOTDIR
	}
	return 0
}

func sysGetcwd(bufferAddr uint32, आकार uint32) int32 {
	if bufferAddr == 0 {
		return EFAULT
	}
	if आकार < 2 {
		return ERANGE
	}
	buffer := GetBytesFromPtr(uintptr(bufferAddr), int(आकार), int(आकार))
	buffer[0] = '/'
	buffer[1] = 0
	return 2
}

func fillPosixStat(statAddr uint32, mode uint32, आकार uint32, inode uint32) int32 {
	if statAddr == 0 {
		return EFAULT
	}
	stat := (*posixStat)(Pointer(uintptr(statAddr)))
	*stat = posixStat{}
	stat.Dev = 1
	stat.Ino = inode
	stat.Mode = mode
	stat.Nlink = 1
	stat.Vआकार = int32(आकार)
	stat.Blksize = 512
	stat.Blocks = int32((आकार + 511) / 512)
	return 0
}

func sysStat(pathAddr uint32, statAddr uint32) int32 {
	if pathAddr == 0 {
		return EFAULT
	}
	if isRootPath(pathAddr) {
		return fillPosixStat(statAddr, sIfdir|0555, 0, 1)
	}
	nameLen, name := copyPath(pathAddr)
	if nameLen == 0 {
		return ENOENT
	}
	आकार := fileSize(name[:nameLen])
	if आकार == 0 {
		return ENOENT
	}
	inode := uint32(2)
	for i := uint32(0); i < nameLen; i++ {
		inode = inode*33 + uint32(name[i])
	}
	return fillPosixStat(statAddr, sIfreg|0444, आकार, inode)
}

func sysFstat(fd int32, statAddr uint32) int32 {
	entry := getOpenFile(fd)
	if entry == nil {
		return EBADF
	}
	switch entry.kind {
	case fdKindStdin, fdKindConsole:
		return fillPosixStat(statAddr, sIfchr|0666, 0, uint32(fd+1))
	case fdKindRootDir:
		return fillPosixStat(statAddr, sIfdir|0555, 0, 1)
	case fdKindFat:
		return fillPosixStat(statAddr, sIfreg|0444, entry.आकार, uint32(fd+2))
	case fdKindSocket:
		return fillPosixStat(statAddr, sIfsock|0666, 0, uint32(fd+2))
	}
	return EBADF
}

func sysFsync(fd int32) int32 {
	if getOpenFile(fd) == nil {
		return EBADF
	}
	return 0
}

func sysBrk(address uint32) uint32 {
	process := ensureCurrentProcess()
	if process == nil {
		return 0
	}
	if process.programBreak == 0 {
		process.programBreak = userHeapBase
	}
	if address == 0 {
		return process.programBreak
	}
	if address < userHeapBase || address > userHeapLimit {
		return process.programBreak
	}
	process.programBreak = address
	return process.programBreak
}

func copyUtsField(destination *[65]byte, value string) {
	limit := len(value)
	if limit > 64 {
		limit = 64
	}
	for i := 0; i < limit; i++ {
		destination[i] = value[i]
	}
	destination[limit] = 0
}

func sysUname(address uint32) int32 {
	if address == 0 {
		return EFAULT
	}
	name := (*posixUtsname)(Pointer(uintptr(address)))
	*name = posixUtsname{}
	copyUtsField(&name.Sysname, "EngOS")
	copyUtsField(&name.Nodename, "engos")
	copyUtsField(&name.Release, "0.1-posix")
	copyUtsField(&name.Version, "POSIX.1-2017 phase 1")
	copyUtsField(&name.Machine, "i386")
	return 0
}

func swapUint16(value uint16) uint16 {
	return (value << 8) | (value >> 8)
}

func socketCallArgument(arguments uint32, index uint32) uint32 {
	return *(*uint32)(Pointer(uintptr(arguments + index*4)))
}

func socketForFD(fd int32) (*localDatagramSocket, int32) {
	entry := getOpenFile(fd)
	if entry == nil || entry.kind != fdKindSocket || entry.aux >= maxSockets {
		return nil, EBADF
	}
	socket := &localSockets[entry.aux]
	if !socket.used {
		return nil, EBADF
	}
	return socket, 0
}

func allocateSocket(domain uint32, socketType uint32, protocol uint32) int32 {
	if domain != afInet {
		return EAFNOSUPPORT
	}
	if socketType != sockDatagram {
		return EPROTONOSUPPORT
	}
	if protocol != 0 && protocol != ipProtocolUDP {
		return EPROTONOSUPPORT
	}
	process := ensureCurrentProcess()
	if process == nil {
		return ENFILE
	}
	socketIndex := -1
	for i := 0; i < maxSockets; i++ {
		if !localSockets[i].used {
			socketIndex = i
			break
		}
	}
	if socketIndex < 0 {
		return ENFILE
	}
	description := allocOpenFile()
	if description < 0 {
		return description
	}
	localSockets[socketIndex] = localDatagramSocket{used: true}
	entry := &openFileTable[description]
	entry.kind = fdKindSocket
	entry.flags = oReadWrite
	entry.aux = uint32(socketIndex)
	fd := allocFD(process, description, 3)
	if fd < 0 {
		localSockets[socketIndex] = localDatagramSocket{}
		*entry = openFileDescription{}
		return fd
	}
	return fd
}

func socketAddress(address uint32, length uint32) (*socketAddressIPv4, int32) {
	if address == 0 {
		return nil, EFAULT
	}
	if length < 16 {
		return nil, EINVAL
	}
	result := (*socketAddressIPv4)(Pointer(uintptr(address)))
	if result.Family != afInet {
		return nil, EAFNOSUPPORT
	}
	return result, 0
}

func portInUse(port uint16, except *localDatagramSocket) bool {
	for i := 0; i < maxSockets; i++ {
		socket := &localSockets[i]
		if socket != except && socket.used && socket.bound && socket.local.Port == port {
			return true
		}
	}
	return false
}

func bindEphemeral(socket *localDatagramSocket) int32 {
	for attempts := 0; attempts < 16384; attempts++ {
		port := swapUint16(nextEphemeralPort)
		nextEphemeralPort++
		if nextEphemeralPort < 49152 {
			nextEphemeralPort = 49152
		}
		if !portInUse(port, socket) {
			socket.local = socketAddressIPv4{Family: afInet, Port: port, Address: 0x0100007F}
			socket.bound = true
			return 0
		}
	}
	return EADDRINUSE
}

func socketBind(fd int32, address uint32, length uint32) int32 {
	socket, err := socketForFD(fd)
	if err != 0 {
		return err
	}
	requested, err := socketAddress(address, length)
	if err != 0 {
		return err
	}
	if socket.bound {
		return EINVAL
	}
	if requested.Port == 0 {
		return bindEphemeral(socket)
	}
	if portInUse(requested.Port, socket) {
		return EADDRINUSE
	}
	socket.local = *requested
	socket.bound = true
	return 0
}

func socketConnect(fd int32, address uint32, length uint32) int32 {
	socket, err := socketForFD(fd)
	if err != 0 {
		return err
	}
	remote, err := socketAddress(address, length)
	if err != 0 {
		return err
	}
	if !socket.bound {
		if err := bindEphemeral(socket); err != 0 {
			return err
		}
	}
	socket.remote = *remote
	socket.connected = true
	return 0
}

func socketSendTo(fd int32, bufferAddress uint32, length uint32, destinationAddress uint32, destinationLength uint32) int32 {
	socket, err := socketForFD(fd)
	if err != 0 {
		return err
	}
	if length > maxDatagramSize {
		return EMSGSIZE
	}
	if length != 0 && bufferAddress == 0 {
		return EFAULT
	}
	var destination socketAddressIPv4
	if destinationAddress != 0 {
		address, addressError := socketAddress(destinationAddress, destinationLength)
		if addressError != 0 {
			return addressError
		}
		destination = *address
	} else {
		if !socket.connected {
			return ENOTCONN
		}
		destination = socket.remote
	}
	if !socket.bound {
		if bindError := bindEphemeral(socket); bindError != 0 {
			return bindError
		}
	}
	var receiver *localDatagramSocket
	for i := 0; i < maxSockets; i++ {
		candidate := &localSockets[i]
		if candidate.used && candidate.bound && candidate.local.Port == destination.Port &&
			(candidate.local.Address == 0 || candidate.local.Address == destination.Address) {
			receiver = candidate
			break
		}
	}
	if receiver == nil {
		return ENETUNREACH
	}
	if receiver.count >= maxSocketPackets {
		return EAGAIN
	}
	packet := &receiver.packets[receiver.tail]
	*packet = socketPacket{used: true, आकार: length, source: socket.local}
	if length != 0 {
		source := GetBytesFromPtr(uintptr(bufferAddress), int(length), int(length))
		copy(packet.data[:length], source)
	}
	receiver.tail = (receiver.tail + 1) % maxSocketPackets
	receiver.count++
	return int32(length)
}

func socketReceiveFrom(fd int32, bufferAddress uint32, length uint32, sourceAddress uint32, sourceLengthAddress uint32) int32 {
	socket, err := socketForFD(fd)
	if err != 0 {
		return err
	}
	if length != 0 && bufferAddress == 0 {
		return EFAULT
	}
	if socket.count == 0 {
		return EAGAIN
	}
	packet := &socket.packets[socket.head]
	copyLength := packet.आकार
	if copyLength > length {
		copyLength = length
	}
	if copyLength != 0 {
		destination := GetBytesFromPtr(uintptr(bufferAddress), int(copyLength), int(copyLength))
		copy(destination, packet.data[:copyLength])
	}
	if sourceAddress != 0 {
		if sourceLengthAddress == 0 {
			return EFAULT
		}
		providedLength := (*uint32)(Pointer(uintptr(sourceLengthAddress)))
		if *providedLength >= 16 {
			*(*socketAddressIPv4)(Pointer(uintptr(sourceAddress))) = packet.source
		}
		*providedLength = 16
	}
	*packet = socketPacket{}
	socket.head = (socket.head + 1) % maxSocketPackets
	socket.count--
	return int32(copyLength)
}

func copySocketName(fd int32, address uint32, lengthAddress uint32, peer bool) int32 {
	socket, err := socketForFD(fd)
	if err != 0 {
		return err
	}
	if address == 0 || lengthAddress == 0 {
		return EFAULT
	}
	length := (*uint32)(Pointer(uintptr(lengthAddress)))
	if *length < 16 {
		*length = 16
		return EINVAL
	}
	if peer {
		if !socket.connected {
			return ENOTCONN
		}
		*(*socketAddressIPv4)(Pointer(uintptr(address))) = socket.remote
	} else {
		if !socket.bound {
			if bindError := bindEphemeral(socket); bindError != 0 {
				return bindError
			}
		}
		*(*socketAddressIPv4)(Pointer(uintptr(address))) = socket.local
	}
	*length = 16
	return 0
}

func sysSocketCall(call uint32, arguments uint32) int32 {
	if arguments == 0 {
		return EFAULT
	}
	switch call {
	case 1:
		return allocateSocket(socketCallArgument(arguments, 0), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2))
	case 2:
		return socketBind(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2))
	case 3:
		return socketConnect(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2))
	case 4, 5:
		return EOPNOTSUPP
	case 6:
		return copySocketName(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), false)
	case 7:
		return copySocketName(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), true)
	case 9:
		return socketSendTo(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), 0, 0)
	case 10:
		return socketReceiveFrom(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), 0, 0)
	case 11:
		return socketSendTo(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), socketCallArgument(arguments, 4), socketCallArgument(arguments, 5))
	case 12:
		return socketReceiveFrom(int32(socketCallArgument(arguments, 0)), socketCallArgument(arguments, 1), socketCallArgument(arguments, 2), socketCallArgument(arguments, 4), socketCallArgument(arguments, 5))
	case 13:
		if _, err := socketForFD(int32(socketCallArgument(arguments, 0))); err != 0 {
			return err
		}
		return 0
	case 14:
		if _, err := socketForFD(int32(socketCallArgument(arguments, 0))); err != 0 {
			return err
		}
		return 0
	}
	return EOPNOTSUPP
}

func readStdin(addr uint32, count uint32) int32 {
	if addr == 0 {
		return EINVAL
	}
	buf := GetBytesFromPtr(uintptr(addr), int(count), int(count))
	var n uint32
	for n < count {
		c := stdinGetBlocking()
		buf[n] = c
		n++
		if c == '\n' {
			break
		}
	}
	return int32(n)
}

func StdinPutByte(c byte) {
	next := (stdinWrite + 1) % uint32(len(stdinBuffer))
	if next == stdinRead {
		return
	}
	stdinBuffer[stdinWrite] = c
	stdinWrite = next
}

func stdinGetBlocking() byte {
	for stdinRead == stdinWrite {
		sc := pollKeyboardScancode()
		if sc != 0 {
			StdinPutByte(sc)
		}
	}
	c := stdinBuffer[stdinRead]
	stdinRead = (stdinRead + 1) % uint32(len(stdinBuffer))
	return c
}

func pollKeyboardScancode() byte {
	for (PortReadByte(0x64) & 0x01) == 0 {
	}
	sc := PortReadByte(0x60)
	return scancodeToByte(sc)
}

func scancodeToByte(sc uint8) byte {
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

func copyExecVector(address uint32, result *execVector) int32 {
	*result = execVector{}
	if address == 0 {
		return 0
	}
	for index := uint32(0); index < maxExecVectorEntries; index++ {
		stringAddress := *(*uint32)(Pointer(uintptr(address + index*4)))
		if stringAddress == 0 {
			result.count = index
			return 0
		}
		terminated := false
		for length := uint32(0); length <= maxExecStringLength; length++ {
			value := *(*byte)(Pointer(uintptr(stringAddress + length)))
			result.values[index][length] = value
			if value == 0 {
				result.lengths[index] = length
				terminated = true
				break
			}
		}
		if !terminated {
			return E2BIG
		}
	}
	return E2BIG
}

func pushExecUint32(stack *uint32, value uint32) {
	*stack -= 4
	*(*uint32)(Pointer(uintptr(*stack))) = value
}

func setupExecStack(cpu *TCPUState, arguments *execVector, environment *execVector) int32 {
	const stackBytes uint32 = 4096
	if !MakeRangePrivateWritable(getCR3(), USER_STACK_TOP-stackBytes, stackBytes) {
		return ENOMEM
	}
	stack := USER_STACK_TOP
	var argumentPointers [maxExecVectorEntries]uint32
	var environmentPointers [maxExecVectorEntries]uint32

	for i := int(environment.count) - 1; i >= 0; i-- {
		length := environment.lengths[i] + 1
		stack -= length
		destination := GetBytesFromPtr(uintptr(stack), int(length), int(length))
		copy(destination, environment.values[i][:length])
		environmentPointers[i] = stack
	}
	for i := int(arguments.count) - 1; i >= 0; i-- {
		length := arguments.lengths[i] + 1
		stack -= length
		destination := GetBytesFromPtr(uintptr(stack), int(length), int(length))
		copy(destination, arguments.values[i][:length])
		argumentPointers[i] = stack
	}
	stack &= ^uint32(3)
	pushExecUint32(&stack, 0)
	for i := int(environment.count) - 1; i >= 0; i-- {
		pushExecUint32(&stack, environmentPointers[i])
	}
	pushExecUint32(&stack, 0)
	for i := int(arguments.count) - 1; i >= 0; i-- {
		pushExecUint32(&stack, argumentPointers[i])
	}
	pushExecUint32(&stack, arguments.count)
	cpu.Esp = stack
	cpu.Ebp = 0
	return 0
}

func closeOnExec(process *processEntry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxFD; fd++ {
		if process.fds[fd].used && (process.fds[fd].fdFlags&fdCloexec) != 0 {
			closeProcessFD(process, fd)
		}
	}
}

func sysExecve(cpu *TCPUState, pathAddr uint32) int32 {
	if pathAddr == 0 {
		return EFAULT
	}
	var arguments execVector
	var environment execVector
	if result := copyExecVector(cpu.Ecx, &arguments); result < 0 {
		return result
	}
	if result := copyExecVector(cpu.Edx, &environment); result < 0 {
		return result
	}
	nameLen, name := copyPath(pathAddr)
	if nameLen == 0 {
		return ENOENT
	}
	आकार := fileSize(name[:nameLen])
	if आकार == 0 {
		return ENOENT
	}
	memoryManager := &mem.TMemoryManager{}
	filePtr := memoryManager.Malloc(आकार)
	if filePtr == nil {
		return EINVAL
	}
	data := GetBytesFromPtr(uintptr(filePtr), int(आकार), int(आकार))
	readFile(name[:nameLen], data)
	if आकार < 52 || data[0] != 0x7F || data[1] != 'E' || data[2] != 'L' || data[3] != 'F' {
		memoryManager.Free(filePtr)
		return ENOEXEC
	}
	loader := Elf{}
	entry := loader.GetEntry(data)
	loader.Parse(data, getCR3())
	memoryManager.Free(filePtr)
	if result := setupExecStack(cpu, &arguments, &environment); result < 0 {
		return result
	}
	closeOnExec(ensureCurrentProcess())
	cpu.Eip = entry
	cpu.Eax = 0
	return 0
}

func sysFork(cpu *TCPUState) int32 {
	parentPID := CurrentPID()
	if ensureCurrentProcess() == nil {
		return ENFILE
	}
	pid := allocProcess(parentPID)
	if pid == 0 {
		return EINVAL
	}
	memoryManager := &mem.TMemoryManager{}
	threadPtr := memoryManager.Malloc(uint32(Sizeof(Tनिष्पादन_धारा{})))
	stackPtr := memoryManager.Malloc(THREAD_STACK_SIZE)
	childPageDir := CloneAddressSpaceCOW(getCR3())
	if threadPtr == nil || stackPtr == nil || childPageDir == 0 {
		discardProcess(pid)
		return EINVAL
	}
	child := (*Tनिष्पादन_धारा)(threadPtr)
	child.Stack = uint32(uintptr(stackPtr))
	child.CpuState = (*TCPUState)(Pointer(uintptr(stackPtr) + THREAD_STACK_SIZE - Sizeof(TCPUState{})))
	*child.CpuState = *cpu
	child.CpuState.Eax = 0
	child.UserStack = cpu.Esp
	child.UserStackSize = 0
	child.Pid = pid
	child.ParentPid = parentPID
	child.PageDirEntry = childPageDir
	child.ThreadState = Ready
	child.FPUOffset = 0xffffffff
	child.IsKernel = false
	AddRunnableThread(child)
	return int32(pid)
}

func sysExit(status uint32) {
	pid := CurrentPID()
	for i := 0; i < len(processTable); i++ {
		if processTable[i].used && processTable[i].pid == pid {
			closeAllProcessFDs(&processTable[i])
			processTable[i].exited = true
			processTable[i].status = (status & 0xFF) << 8
			return
		}
	}
}

func sysWaitpid(pid int32, statusAddr uint32, options uint32) int32 {
	if (options & ^uint32(1)) != 0 {
		return EINVAL
	}
	parentPID := CurrentPID()
	foundChild := false
	for i := 0; i < len(processTable); i++ {
		p := &processTable[i]
		matches := pid == -1 || pid == 0 || p.pid == uint32(pid)
		if p.used && matches && p.parent == parentPID {
			foundChild = true
			if p.exited {
				if statusAddr != 0 {
					*(*uint32)(Pointer(uintptr(statusAddr))) = p.status
				}
				childPID := p.pid
				*p = processEntry{}
				return int32(childPID)
			}
		}
	}
	if !foundChild {
		return ECHILD
	}

	if (options & 1) != 0 {
		return 0
	}
	return EAGAIN
}

func allocProcess(parent uint32) uint32 {
	parentProcess := findProcess(parent)
	pid := AllocatePID()
	for i := 0; i < len(processTable); i++ {
		if !processTable[i].used {
			processTable[i] = processEntry{
				used:		true,
				pid:		pid,
				parent:		parent,
				programBreak:	userHeapBase,
			}
			if parentProcess != nil {
				processTable[i].programBreak = parentProcess.programBreak
				for fd := 0; fd < maxFD; fd++ {
					if parentProcess.fds[fd].used {
						processTable[i].fds[fd] = parentProcess.fds[fd]
						description := parentProcess.fds[fd].description
						if description >= 0 && description < maxOpenFiles {
							openFileTable[description].refs++
						}
					}
				}
			} else {
				initializeProcessFDs(&processTable[i])
			}
			return pid
		}
	}
	return 0
}

func closeAllProcessFDs(process *processEntry) {
	if process == nil {
		return
	}
	for fd := int32(0); fd < maxFD; fd++ {
		if process.fds[fd].used {
			closeProcessFD(process, fd)
		}
	}
}

func discardProcess(pid uint32) {
	process := findProcess(pid)
	if process == nil {
		return
	}
	closeAllProcessFDs(process)
	*process = processEntry{}
}

func copyPath(pathAddr uint32) (uint32, [12]byte) {
	var name [12]byte
	if pathAddr == 0 {
		return 0, name
	}
	raw := GetBytesFromPtr(uintptr(pathAddr), 64, 64)
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
		name[n] = c
		n++
	}
	return n, name
}

func fileSize(filename []byte) uint32 {
	var ata0s = TAdvancedTechnologyAttachment{}
	ata0s.Vआरंभ_करब(false, 0x1F0)
	ata0s.Identify()

	partition := TMSDOSPartitionTable{}
	partition.ReadPartitions(&ata0s)

	bios := TBiosParameterBlock32{}
	आकार := bios.Len(&ata0s, partition.MBR.PrimaryPartition[0], filename)
	ata0s.Flush()
	return आकार
}

func readFile(filename []byte, data []byte) {
	var ata0s = TAdvancedTechnologyAttachment{}
	ata0s.Vआरंभ_करब(false, 0x1F0)
	ata0s.Identify()

	partition := TMSDOSPartitionTable{}
	partition.ReadPartitions(&ata0s)

	bios := TBiosParameterBlock32{}
	bios.Vपढ़ब(&ata0s, partition.MBR.PrimaryPartition[0], filename, data)
	ata0s.Flush()
}

func getCR3() uint32
