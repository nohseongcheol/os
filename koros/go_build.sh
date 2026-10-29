WORK="/home/user/koros/build"
alias pack='go tool pack'
export CGO_ENABLED=0
export GOPATH=/home/user/koros/build
export GOROOT=/usr/lib/go-1.10
export GOARCH=386
export GOOS=linux
set -e

#
# gdt
#

mkdir -p /home/user/koros/build/b004/
cat >/home/user/koros/build/b004/importcfg << 'EOF' # internal
# import config
EOF
cd /home/user/koros/src/gdt
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b004/_pkg_.a -trimpath $WORK/b004 -p gdt -buildid i9MrfDt-QjzYbnEx0n7z/i9MrfDt-QjzYbnEx0n7z -goversion go1.10.4 -D "" -importcfg $WORK/b004/importcfg -pack -asmhdr $WORK/b004/go_asm.h -c=2 ./gdt.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b004 -I $WORK/b004/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b004/gdt.o ./gdt.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b004/_pkg_.a $WORK/b004/gdt.o # internal

#
# port
#

mkdir -p /home/user/koros/build/b006/
cat >/home/user/koros/build/b006/importcfg << 'EOF' # internal
# import config
EOF
cd /home/user/koros/src/port
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b006/_pkg_.a -trimpath $WORK/b006 -p port -buildid T1Ejk46fUihHHf10Skyu/T1Ejk46fUihHHf10Skyu -goversion go1.10.4 -D "" -importcfg $WORK/b006/importcfg -pack -asmhdr $WORK/b006/go_asm.h -c=2 ./port.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b006 -I $WORK/b006/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b006/port.o ./port.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b006/_pkg_.a $WORK/b006/port.o # internal

#
# math
#

mkdir -p /home/user/koros/build/b008/
cat >/home/user/koros/build/b008/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/math
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b008/_pkg_.a -trimpath $WORK/b008 -p math -std -buildid GXbUU8WLgIujkGMrXH9m/GXbUU8WLgIujkGMrXH9m -goversion go1.10.4 -D "" -importcfg $WORK/b008/importcfg -pack -asmhdr $WORK/b008/go_asm.h -c=2 ./abs.go ./acosh.go ./asin.go ./asinh.go ./atan.go ./atan2.go ./atanh.go ./bits.go ./cbrt.go ./const.go ./copysign.go ./dim.go ./erf.go ./erfinv.go ./exp.go ./expm1.go ./floor.go ./frexp.go ./gamma.go ./hypot.go ./j0.go ./j1.go ./jn.go ./ldexp.go ./lgamma.go ./log.go ./log10.go ./log1p.go ./logb.go ./mod.go ./modf.go ./nextafter.go ./pow.go ./pow10.go ./remainder.go ./signbit.go ./sin.go ./sincos_386.go ./sinh.go ./sqrt.go ./tan.go ./tanh.go ./unsafe.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/asin_386.o ./asin_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/asinh_stub.o ./asinh_stub.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/atan2_386.o ./atan2_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/atan_386.o ./atan_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/cbrt_stub.o ./cbrt_stub.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/dim_386.o ./dim_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/erf_stub.o ./erf_stub.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/exp2_386.o ./exp2_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/exp_386.o ./exp_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/expm1_386.o ./expm1_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/floor_386.o ./floor_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/frexp_386.o ./frexp_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/hypot_386.o ./hypot_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/ldexp_386.o ./ldexp_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/log10_386.o ./log10_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/log1p_386.o ./log1p_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/log_386.o ./log_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/mod_386.o ./mod_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/modf_386.o ./modf_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/pow_stub.o ./pow_stub.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/remainder_386.o ./remainder_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/sin_386.o ./sin_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/sincos_386.o ./sincos_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/sinh_stub.o ./sinh_stub.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/sqrt_386.o ./sqrt_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b008 -I $WORK/b008/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b008/tan_386.o ./tan_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b008/_pkg_.a $WORK/b008/asin_386.o $WORK/b008/asinh_stub.o $WORK/b008/atan2_386.o $WORK/b008/atan_386.o $WORK/b008/cbrt_stub.o $WORK/b008/dim_386.o $WORK/b008/erf_stub.o $WORK/b008/exp2_386.o $WORK/b008/exp_386.o $WORK/b008/expm1_386.o $WORK/b008/floor_386.o $WORK/b008/frexp_386.o $WORK/b008/hypot_386.o $WORK/b008/ldexp_386.o $WORK/b008/log10_386.o $WORK/b008/log1p_386.o $WORK/b008/log_386.o $WORK/b008/mod_386.o $WORK/b008/modf_386.o $WORK/b008/pow_stub.o $WORK/b008/remainder_386.o $WORK/b008/sin_386.o $WORK/b008/sincos_386.o $WORK/b008/sinh_stub.o $WORK/b008/sqrt_386.o $WORK/b008/tan_386.o # internal

#
# runtime/internal/atomic
#

mkdir -p /home/user/koros/build/b010/
cat >/home/user/koros/build/b010/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/runtime/internal/atomic
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b010/_pkg_.a -trimpath $WORK/b010 -p runtime/internal/atomic -std -+ -buildid vDdO0_AhuwCf1rgwY6bT/vDdO0_AhuwCf1rgwY6bT -goversion go1.10.4 -D "" -importcfg $WORK/b010/importcfg -pack -asmhdr $WORK/b010/go_asm.h -c=2 ./atomic_386.go ./stubs.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b010 -I $WORK/b010/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b010/asm_386.o ./asm_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b010/_pkg_.a $WORK/b010/asm_386.o # internal

#
# runtime/internal/sys
#

mkdir -p /home/user/koros/build/b011/
cat >/home/user/koros/build/b011/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/runtime/internal/sys
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b011/_pkg_.a -trimpath $WORK/b011 -p runtime/internal/sys -std -+ -buildid GRLrX-1a8lQK1HikNPiB/GRLrX-1a8lQK1HikNPiB -goversion go1.10.4 -D "" -importcfg $WORK/b011/importcfg -pack -asmhdr $WORK/b011/go_asm.h -c=2 ./arch.go ./arch_386.go ./intrinsics_stubs.go ./stubs.go ./sys.go ./zgoarch_386.go ./zgoos_linux.go ./zversion.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b011 -I $WORK/b011/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b011/intrinsics_386.o ./intrinsics_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b011/_pkg_.a $WORK/b011/intrinsics_386.o # internal

#
# runtime
#

mkdir -p /home/user/koros/build/b009/
cat >/home/user/koros/build/b009/importcfg << 'EOF' # internal
# import config
packagefile runtime/internal/atomic=/home/user/koros/build/b010/_pkg_.a
packagefile runtime/internal/sys=/home/user/koros/build/b011/_pkg_.a
EOF
cd /usr/lib/go-1.10/src/runtime
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b009/_pkg_.a -trimpath $WORK/b009 -p runtime -std -+ -buildid HRtTg3Kp0OrKdnI1LKIU/HRtTg3Kp0OrKdnI1LKIU -goversion go1.10.4 -D "" -importcfg $WORK/b009/importcfg -pack -asmhdr $WORK/b009/go_asm.h -c=2 ./alg.go ./atomic_pointer.go ./cgo.go ./cgocall.go ./cgocallback.go ./cgocheck.go ./chan.go ./compiler.go ./complex.go ./cpuprof.go ./cputicks.go ./debug.go ./defs_linux_386.go ./env_posix.go ./error.go ./extern.go ./fastlog2.go ./fastlog2table.go ./float.go ./hash32.go ./hashmap.go ./hashmap_fast.go ./heapdump.go ./iface.go ./lfstack.go ./lfstack_32bit.go ./lock_futex.go ./malloc.go ./mbarrier.go ./mbitmap.go ./mcache.go ./mcentral.go ./mem_linux.go ./mfinal.go ./mfixalloc.go ./mgc.go ./mgclarge.go ./mgcmark.go ./mgcsweep.go ./mgcsweepbuf.go ./mgcwork.go ./mheap.go ./mmap.go ./mprof.go ./msan0.go ./msize.go ./mstats.go ./mwbbuf.go ./netpoll.go ./netpoll_epoll.go ./os_linux.go ./os_linux_generic.go ./panic.go ./plugin.go ./print.go ./proc.go ./profbuf.go ./proflabel.go ./race0.go ./rdebug.go ./relax_stub.go ./runtime.go ./runtime1.go ./runtime2.go ./rwmutex.go ./select.go ./sema.go ./sigaction_linux.go ./signal_386.go ./signal_linux_386.go ./signal_sighandler.go ./signal_unix.go ./sigqueue.go ./sigtab_linux_generic.go ./sizeclasses.go ./slice.go ./softfloat64.go ./sqrt.go ./stack.go ./string.go ./stubs.go ./stubs2.go ./stubs32.go ./stubs_asm.go ./stubs_linux.go ./symtab.go ./sys_nonppc64x.go ./sys_x86.go ./time.go ./timestub.go ./trace.go ./traceback.go ./type.go ./typekind.go ./unaligned1.go ./utf8.go ./vdso_linux.go ./vdso_linux_386.go ./vlrt.go ./write_err.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/asm.o ./asm.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/asm_386.o ./asm_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/duff_386.o ./duff_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/memclr_386.o ./memclr_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/memmove_386.o ./memmove_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/rt0_linux_386.o ./rt0_linux_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/sys_linux_386.o ./sys_linux_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b009 -I $WORK/b009/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b009/vlop_386.o ./vlop_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b009/_pkg_.a $WORK/b009/asm.o $WORK/b009/asm_386.o $WORK/b009/duff_386.o $WORK/b009/memclr_386.o $WORK/b009/memmove_386.o $WORK/b009/rt0_linux_386.o $WORK/b009/sys_linux_386.o $WORK/b009/vlop_386.o # internal

#
# errors
#

mkdir -p /home/user/koros/build/b013/
cat >/home/user/koros/build/b013/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/errors
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b013/_pkg_.a -trimpath $WORK/b013 -p errors -std -complete -buildid QmOSQcO7MfUw1iQh6F67/QmOSQcO7MfUw1iQh6F67 -goversion go1.10.4 -D "" -importcfg $WORK/b013/importcfg -pack -c=2 ./errors.go

#
# unicode/utf8
#

mkdir -p /home/user/koros/build/b014/
cat >/home/user/koros/build/b014/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/unicode/utf8
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b014/_pkg_.a -trimpath $WORK/b014 -p unicode/utf8 -std -complete -buildid 2bBikm2sukF6q0eJfibp/2bBikm2sukF6q0eJfibp -goversion go1.10.4 -D "" -importcfg $WORK/b014/importcfg -pack -c=2 ./utf8.go

#
# strconv
#

mkdir -p /home/user/koros/build/b012/
cat >/home/user/koros/build/b012/importcfg << 'EOF' # internal
# import config
packagefile errors=/home/user/koros/build/b013/_pkg_.a
packagefile math=/home/user/koros/build/b008/_pkg_.a
packagefile unicode/utf8=/home/user/koros/build/b014/_pkg_.a
EOF
cd /usr/lib/go-1.10/src/strconv
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b012/_pkg_.a -trimpath $WORK/b012 -p strconv -std -complete -buildid PttOezEe7FNPgpR_VG3D/PttOezEe7FNPgpR_VG3D -goversion go1.10.4 -D "" -importcfg $WORK/b012/importcfg -pack -c=2 ./atob.go ./atof.go ./atoi.go ./decimal.go ./doc.go ./extfloat.go ./ftoa.go ./isprint.go ./itoa.go ./quote.go

#
# internal/race
#

mkdir -p /home/user/koros/build/b016/
cat >/home/user/koros/build/b016/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/internal/race
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b016/_pkg_.a -trimpath $WORK/b016 -p internal/race -std -complete -buildid j-6NiD0yLNtPhFTtIFJK/j-6NiD0yLNtPhFTtIFJK -goversion go1.10.4 -D "" -importcfg $WORK/b016/importcfg -pack -c=2 ./doc.go ./norace.go

#
# sync/atomic
#

mkdir -p /home/user/koros/build/b017/
cat >/home/user/koros/build/b017/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/sync/atomic
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b017/_pkg_.a -trimpath $WORK/b017 -p sync/atomic -std -buildid T-DCWa2CaZ-93sqU14xf/T-DCWa2CaZ-93sqU14xf -goversion go1.10.4 -D "" -importcfg $WORK/b017/importcfg -pack -asmhdr $WORK/b017/go_asm.h -c=2 ./doc.go ./value.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b017 -I $WORK/b017/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b017/asm_386.o ./asm_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b017/_pkg_.a $WORK/b017/asm_386.o # internal

#
# sync
#

mkdir -p /home/user/koros/build/b015/
cat >/home/user/koros/build/b015/importcfg << 'EOF' # internal
# import config
packagefile internal/race=/home/user/koros/build/b016/_pkg_.a
packagefile runtime=/home/user/koros/build/b009/_pkg_.a
packagefile sync/atomic=/home/user/koros/build/b017/_pkg_.a
EOF
cd /usr/lib/go-1.10/src/sync
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b015/_pkg_.a -trimpath $WORK/b015 -p sync -std -buildid EhQKdo4MPyVzZCleASeN/EhQKdo4MPyVzZCleASeN -goversion go1.10.4 -D "" -importcfg $WORK/b015/importcfg -pack -c=2 ./cond.go ./map.go ./mutex.go ./once.go ./pool.go ./runtime.go ./rwmutex.go ./waitgroup.go

#
# unicode
#

mkdir -p /home/user/koros/build/b018/
cat >/home/user/koros/build/b018/importcfg << 'EOF' # internal
# import config
EOF
cd /usr/lib/go-1.10/src/unicode
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b018/_pkg_.a -trimpath $WORK/b018 -p unicode -std -complete -buildid FasBGHtKmLI8yH9XDJG6/FasBGHtKmLI8yH9XDJG6 -goversion go1.10.4 -D "" -importcfg $WORK/b018/importcfg -pack -c=2 ./casetables.go ./digit.go ./graphic.go ./letter.go ./tables.go

#
# reflect
#

mkdir -p /home/user/koros/build/b007/
cat >/home/user/koros/build/b007/importcfg << 'EOF' # internal
# import config
packagefile math=/home/user/koros/build/b008/_pkg_.a
packagefile runtime=/home/user/koros/build/b009/_pkg_.a
packagefile strconv=/home/user/koros/build/b012/_pkg_.a
packagefile sync=/home/user/koros/build/b015/_pkg_.a
packagefile unicode=/home/user/koros/build/b018/_pkg_.a
packagefile unicode/utf8=/home/user/koros/build/b014/_pkg_.a
EOF
cd /usr/lib/go-1.10/src/reflect
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b007/_pkg_.a -trimpath $WORK/b007 -p reflect -std -buildid 2A24EXKPwH9iLy0sYIUV/2A24EXKPwH9iLy0sYIUV -goversion go1.10.4 -D "" -importcfg $WORK/b007/importcfg -pack -asmhdr $WORK/b007/go_asm.h -c=2 ./deepequal.go ./makefunc.go ./swapper.go ./type.go ./value.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b007 -I $WORK/b007/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b007/asm_386.o ./asm_386.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b007/_pkg_.a $WORK/b007/asm_386.o # internal

#
# 단말기
#

mkdir -p /home/user/koros/build/b019/
cat >/home/user/koros/build/b019/importcfg << 'EOF' # internal
# import config
EOF
cd /home/user/koros/src/단말기
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b019/_pkg_.a -trimpath $WORK/b019 -p 단말기 -complete -buildid OY-6j0sglZupkuZSluj8/OY-6j0sglZupkuZSluj8 -goversion go1.10.4 -D "" -importcfg $WORK/b019/importcfg -pack -c=2 ./단말기.go

#
# 기억공간관리자
#

mkdir -p /home/user/koros/build/b021/
cat >/home/user/koros/build/b021/importcfg << 'EOF' # internal
# import config
EOF
cd /home/user/koros/src/기억공간관리자
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b021/_pkg_.a -trimpath $WORK/b021 -p 기억공간관리자 -complete -buildid 4DPaBkfAPYIrA52ikzEf/4DPaBkfAPYIrA52ikzEf -goversion go1.10.4 -D "" -importcfg $WORK/b021/importcfg -pack -c=2 ./기억공간관리자.go

#
# 작업관리자
#

mkdir -p /home/user/koros/build/b020/
cat >/home/user/koros/build/b020/importcfg << 'EOF' # internal
# import config
packagefile gdt=/home/user/koros/build/b004/_pkg_.a
packagefile reflect=/home/user/koros/build/b007/_pkg_.a
packagefile 기억공간관리자=/home/user/koros/build/b021/_pkg_.a
EOF
cd /home/user/koros/src/작업관리자
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b020/_pkg_.a -trimpath $WORK/b020 -p 작업관리자 -complete -buildid 2epIHttC5Ze0dK3ppWhS/2epIHttC5Ze0dK3ppWhS -goversion go1.10.4 -D "" -importcfg $WORK/b020/importcfg -pack -c=2 ./작업관리자.go

#
# interrupt
#

mkdir -p /home/user/koros/build/b003/
cat >/home/user/koros/build/b003/importcfg << 'EOF' # internal
# import config
packagefile gdt=/home/user/koros/build/b004/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile reflect=/home/user/koros/build/b007/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 작업관리자=/home/user/koros/build/b020/_pkg_.a
EOF
cd /home/user/koros/src/interrupt
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b003/_pkg_.a -trimpath $WORK/b003 -p interrupt -buildid IFp4DsGiP-Qb37-mb1JO/IFp4DsGiP-Qb37-mb1JO -goversion go1.10.4 -D "" -importcfg $WORK/b003/importcfg -pack -asmhdr $WORK/b003/go_asm.h -c=2 ./interrupt.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b003 -I $WORK/b003/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b003/interrupt.o ./interrupt.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b003/_pkg_.a $WORK/b003/interrupt.o # internal

#
# 구동장치들/장치제어기관리자
#

mkdir -p /home/user/koros/build/b023/
cat >/home/user/koros/build/b023/importcfg << 'EOF' # internal
# import config
EOF
cd /home/user/koros/src/구동장치들/장치제어기관리자
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b023/_pkg_.a -trimpath $WORK/b023 -p 구동장치들/장치제어기관리자 -complete -buildid WthbVrWI-U7tSOMwaVLy/WthbVrWI-U7tSOMwaVLy -goversion go1.10.4 -D "" -importcfg $WORK/b023/importcfg -pack -c=2 ./장치제어기관리자.go

#
# pci
#

mkdir -p /home/user/koros/build/b022/
cat >/home/user/koros/build/b022/importcfg << 'EOF' # internal
# import config
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile 구동장치들/장치제어기관리자=/home/user/koros/build/b023/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/pci
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b022/_pkg_.a -trimpath $WORK/b022 -p pci -complete -buildid bZSo9lJBvTM_xpclY-ue/bZSo9lJBvTM_xpclY-ue -goversion go1.10.4 -D "" -importcfg $WORK/b022/importcfg -pack -c=2 ./pci.go

#
# util
#

mkdir -p /home/user/koros/build/b024/
cat >/home/user/koros/build/b024/importcfg << 'EOF' # internal
# import config
packagefile reflect=/home/user/koros/build/b007/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/util
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b024/_pkg_.a -trimpath $WORK/b024 -p util -complete -buildid KufXZGoimc6w2KEwEBcy/KufXZGoimc6w2KEwEBcy -goversion go1.10.4 -D "" -importcfg $WORK/b024/importcfg -pack -c=2 ./util.go

#
# amd_am79c973
#

mkdir -p /home/user/koros/build/b002/
cat >/home/user/koros/build/b002/importcfg << 'EOF' # internal
# import config
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile pci=/home/user/koros/build/b022/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/amd_am79c973
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b002/_pkg_.a -trimpath $WORK/b002 -p amd_am79c973 -complete -buildid 5G7L1bkcuk1uV_7NlWpa/5G7L1bkcuk1uV_7NlWpa -goversion go1.10.4 -D "" -importcfg $WORK/b002/importcfg -pack -c=2 ./amd_am79c973.go

#
# 구동장치들/마우스
#

mkdir -p /home/user/koros/build/b025/
cat >/home/user/koros/build/b025/importcfg << 'EOF' # internal
# import config
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/구동장치들/마우스
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b025/_pkg_.a -trimpath $WORK/b025 -p 구동장치들/마우스 -complete -buildid GK9CCXSTORkfsxDMJEna/GK9CCXSTORkfsxDMJEna -goversion go1.10.4 -D "" -importcfg $WORK/b025/importcfg -pack -c=2 ./기본마우스사건처리기.go ./마우스.go

#
# 구동장치들/자판
#

mkdir -p /home/user/koros/build/b026/
cat >/home/user/koros/build/b026/importcfg << 'EOF' # internal
# import config
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/구동장치들/자판
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b026/_pkg_.a -trimpath $WORK/b026 -p 구동장치들/자판 -complete -buildid 0D8M3hP4-nQZC_inaTv1/0D8M3hP4-nQZC_inaTv1 -goversion go1.10.4 -D "" -importcfg $WORK/b026/importcfg -pack -c=2 ./기본자판사건처리기.go ./자판.go

#
# 시스템호출
#

mkdir -p /home/user/koros/build/b027/
cat >/home/user/koros/build/b027/importcfg << 'EOF' # internal
# import config
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 작업관리자=/home/user/koros/build/b020/_pkg_.a
EOF
cd /home/user/koros/src/시스템호출
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b027/_pkg_.a -trimpath $WORK/b027 -p 시스템호출 -buildid J9GRY96yRqqChCNDWans/J9GRY96yRqqChCNDWans -goversion go1.10.4 -D "" -importcfg $WORK/b027/importcfg -pack -asmhdr $WORK/b027/go_asm.h -c=2 ./시스템호출.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b027 -I $WORK/b027/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b027/시스템호출.o ./시스템호출.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b027/_pkg_.a $WORK/b027/시스템호출.o # internal

#
# 통신/신호통신망형태
#

mkdir -p /home/user/koros/build/b030/
cat >/home/user/koros/build/b030/importcfg << 'EOF' # internal
# import config
packagefile amd_am79c973=/home/user/koros/build/b002/_pkg_.a
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
EOF
cd /home/user/koros/src/통신/신호통신망형태
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b030/_pkg_.a -trimpath $WORK/b030 -p 통신/신호통신망형태 -complete -buildid vRS-18jTYH2Y34KQCCK0/vRS-18jTYH2Y34KQCCK0 -goversion go1.10.4 -D "" -importcfg $WORK/b030/importcfg -pack -c=2 ./신호통신망형태.go

#
# 통신/주소결정규약
#

mkdir -p /home/user/koros/build/b031/
cat >/home/user/koros/build/b031/importcfg << 'EOF' # internal
# import config
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 통신/신호통신망형태=/home/user/koros/build/b030/_pkg_.a
EOF
cd /home/user/koros/src/통신/주소결정규약
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b031/_pkg_.a -trimpath $WORK/b031 -p 통신/주소결정규약 -complete -buildid SiTc8xJbvaCNFRR_zRr0/SiTc8xJbvaCNFRR_zRr0 -goversion go1.10.4 -D "" -importcfg $WORK/b031/importcfg -pack -c=2 ./주소결정규약.go

#
# 통신/상호통신망규약V4
#

mkdir -p /home/user/koros/build/b029/
cat >/home/user/koros/build/b029/importcfg << 'EOF' # internal
# import config
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 통신/신호통신망형태=/home/user/koros/build/b030/_pkg_.a
packagefile 통신/주소결정규약=/home/user/koros/build/b031/_pkg_.a
EOF
cd /home/user/koros/src/통신/상호통신망규약V4
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b029/_pkg_.a -trimpath $WORK/b029 -p 통신/상호통신망규약V4 -complete -buildid WcpFvsJDCTUDmGAT18vr/WcpFvsJDCTUDmGAT18vr -goversion go1.10.4 -D "" -importcfg $WORK/b029/importcfg -pack -c=2 ./상호통신망규약V4.go

#
# 통신/사용자자료단위규약
#

mkdir -p /home/user/koros/build/b028/
cat >/home/user/koros/build/b028/importcfg << 'EOF' # internal
# import config
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 기억공간관리자=/home/user/koros/build/b021/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 통신/상호통신망규약V4=/home/user/koros/build/b029/_pkg_.a
EOF
cd /home/user/koros/src/통신/사용자자료단위규약
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b028/_pkg_.a -trimpath $WORK/b028 -p 통신/사용자자료단위규약 -complete -buildid xeNrqwLU_AF0up1xRMq8/xeNrqwLU_AF0up1xRMq8 -goversion go1.10.4 -D "" -importcfg $WORK/b028/importcfg -pack -c=2 ./사용자자료단위규약.go

#
# 통신/상호통신망제어메시지규약
#

mkdir -p /home/user/koros/build/b032/
cat >/home/user/koros/build/b032/importcfg << 'EOF' # internal
# import config
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 통신/상호통신망규약V4=/home/user/koros/build/b029/_pkg_.a
EOF
cd /home/user/koros/src/통신/상호통신망제어메시지규약
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b032/_pkg_.a -trimpath $WORK/b032 -p 통신/상호통신망제어메시지규약 -complete -buildid Lofo_LdHcYmKw78jjtK9/Lofo_LdHcYmKw78jjtK9 -goversion go1.10.4 -D "" -importcfg $WORK/b032/importcfg -pack -c=2 ./상호통신망제어메시지규약.go

#
# 통신/전송제어규약
#

mkdir -p /home/user/koros/build/b033/
cat >/home/user/koros/build/b033/importcfg << 'EOF' # internal
# import config
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 기억공간관리자=/home/user/koros/build/b021/_pkg_.a
packagefile 통신/상호통신망규약V4=/home/user/koros/build/b029/_pkg_.a
EOF
cd /home/user/koros/src/통신/전송제어규약
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b033/_pkg_.a -trimpath $WORK/b033 -p 통신/전송제어규약 -complete -buildid o_aR_40-tFdoGNiMDQ1-/o_aR_40-tFdoGNiMDQ1- -goversion go1.10.4 -D "" -importcfg $WORK/b033/importcfg -pack -c=2 ./전송제어규약.go

#
# _/home/user/koros
#

mkdir -p /home/user/koros/build/b001/
cat >/home/user/koros/build/b001/importcfg << 'EOF' # internal
# import config
packagefile amd_am79c973=/home/user/koros/build/b002/_pkg_.a
packagefile gdt=/home/user/koros/build/b004/_pkg_.a
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile pci=/home/user/koros/build/b022/_pkg_.a
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 구동장치들/마우스=/home/user/koros/build/b025/_pkg_.a
packagefile 구동장치들/자판=/home/user/koros/build/b026/_pkg_.a
packagefile 구동장치들/장치제어기관리자=/home/user/koros/build/b023/_pkg_.a
packagefile 기억공간관리자=/home/user/koros/build/b021/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 시스템호출=/home/user/koros/build/b027/_pkg_.a
packagefile 작업관리자=/home/user/koros/build/b020/_pkg_.a
packagefile 통신/사용자자료단위규약=/home/user/koros/build/b028/_pkg_.a
packagefile 통신/상호통신망규약V4=/home/user/koros/build/b029/_pkg_.a
packagefile 통신/상호통신망제어메시지규약=/home/user/koros/build/b032/_pkg_.a
packagefile 통신/신호통신망형태=/home/user/koros/build/b030/_pkg_.a
packagefile 통신/전송제어규약=/home/user/koros/build/b033/_pkg_.a
packagefile 통신/주소결정규약=/home/user/koros/build/b031/_pkg_.a
packagefile runtime=/home/user/koros/build/b009/_pkg_.a
EOF
cd /home/user/koros
/usr/lib/go-1.10/pkg/tool/linux_amd64/compile -o /home/user/koros/build/b001/_pkg_.a -trimpath $WORK/b001 -N -l -p main -buildid hrQ6PE0OU3nw--Yp6A07/hrQ6PE0OU3nw--Yp6A07 -goversion go1.10.4 -D _/home/user/koros -importcfg $WORK/b001/importcfg -pack -asmhdr $WORK/b001/go_asm.h -c=2 ./main.go
/usr/lib/go-1.10/pkg/tool/linux_amd64/asm -trimpath /home/user/koros/build/b001 -I $WORK/b001/ -I /usr/lib/go-1.10/pkg/include -D GOOS_linux -D GOARCH_386 -o $WORK/b001/main.o ./main.s
/usr/lib/go-1.10/pkg/tool/linux_amd64/pack r /home/user/koros/build/b001/_pkg_.a $WORK/b001/main.o # internal
cat >/home/user/koros/build/b001/importcfg.link << 'EOF' # internal
packagefile _/home/user/koros=/home/user/koros/build/b001/_pkg_.a
packagefile amd_am79c973=/home/user/koros/build/b002/_pkg_.a
packagefile gdt=/home/user/koros/build/b004/_pkg_.a
packagefile interrupt=/home/user/koros/build/b003/_pkg_.a
packagefile pci=/home/user/koros/build/b022/_pkg_.a
packagefile util=/home/user/koros/build/b024/_pkg_.a
packagefile 구동장치들/마우스=/home/user/koros/build/b025/_pkg_.a
packagefile 구동장치들/자판=/home/user/koros/build/b026/_pkg_.a
packagefile 구동장치들/장치제어기관리자=/home/user/koros/build/b023/_pkg_.a
packagefile 기억공간관리자=/home/user/koros/build/b021/_pkg_.a
packagefile 단말기=/home/user/koros/build/b019/_pkg_.a
packagefile 시스템호출=/home/user/koros/build/b027/_pkg_.a
packagefile 작업관리자=/home/user/koros/build/b020/_pkg_.a
packagefile 통신/사용자자료단위규약=/home/user/koros/build/b028/_pkg_.a
packagefile 통신/상호통신망규약V4=/home/user/koros/build/b029/_pkg_.a
packagefile 통신/상호통신망제어메시지규약=/home/user/koros/build/b032/_pkg_.a
packagefile 통신/신호통신망형태=/home/user/koros/build/b030/_pkg_.a
packagefile 통신/전송제어규약=/home/user/koros/build/b033/_pkg_.a
packagefile 통신/주소결정규약=/home/user/koros/build/b031/_pkg_.a
packagefile runtime=/home/user/koros/build/b009/_pkg_.a
packagefile port=/home/user/koros/build/b006/_pkg_.a
packagefile reflect=/home/user/koros/build/b007/_pkg_.a
packagefile runtime/internal/atomic=/home/user/koros/build/b010/_pkg_.a
packagefile runtime/internal/sys=/home/user/koros/build/b011/_pkg_.a
packagefile math=/home/user/koros/build/b008/_pkg_.a
packagefile strconv=/home/user/koros/build/b012/_pkg_.a
packagefile sync=/home/user/koros/build/b015/_pkg_.a
packagefile unicode=/home/user/koros/build/b018/_pkg_.a
packagefile unicode/utf8=/home/user/koros/build/b014/_pkg_.a
packagefile errors=/home/user/koros/build/b013/_pkg_.a
packagefile internal/race=/home/user/koros/build/b016/_pkg_.a
packagefile sync/atomic=/home/user/koros/build/b017/_pkg_.a
EOF
mkdir -p /home/user/koros/build/b001/exe/
cd .
BUILD_PATH_PREFIX_MAP='/tmp/go-build=/home/user/koros/build:' /usr/lib/go-1.10/pkg/tool/linux_amd64/link -o $WORK/b001/exe/a.out -importcfg $WORK/b001/importcfg.link -buildmode=exe -buildid=LJ0WFhWn72QD7FYRMzhq/hrQ6PE0OU3nw--Yp6A07/hrQ6PE0OU3nw--Yp6A07/LJ0WFhWn72QD7FYRMzhq -tmpdir='/home/user/koros/build'  -linkmode=external -extldflags='-nostdlib -r' -extld=gcc $WORK/b001/_pkg_.a
