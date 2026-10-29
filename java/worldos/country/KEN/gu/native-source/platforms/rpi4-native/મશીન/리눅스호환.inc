/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(ઉપયોગકર્તા_ફ્રેમ *ફાઇલ_પ્રવેશ) {
    ઉપયોગકર્તા_ફ્રેમ 변환값 = *ફાઇલ_પ્રવેશ;
    uintptr_t 수치 = ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[8];
    switch (수치) {
    case 63: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 2; break;   /* read */
    case 64: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 1; break;   /* write */
    case 57: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 4; break;   /* close */
    case 62: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 5; break;   /* lseek */
    case 46: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 10; break;  /* ftruncate */
    case 82: 변환값.રજિસ્ટર_કરો_ડેટા[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char પથ[65]; int 반환값 = ઉદાહરણ_પાથ(ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[1], પથ); if (반환값) return 반환값;
        if ((int)ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[0] != -100 && પથ[0] != '/') return -95;
        if (수치 == 35 && ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[2]) return -95;
        if (수치 == 56 && (ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.રજિસ્ટર_કરો_ડેટા[8] = 수치 == 56 ? 3 : 11;
        변환값.રજિસ્ટર_કરો_ડેટા[0] = ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[1];
        변환값.રજિસ્ટર_કરો_ડેટા[1] = ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.રજિસ્ટર_કરો_ડેટા[2] = ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.રજિસ્ટર_કરો_ડેટા[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[0] != 1) return -22;
        if (!사용자범위(ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), મૂલ્ય[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)ફાઇલ_પ્રવેશ->રજિસ્ટર_કરો_ડેટા[1], મૂલ્ય, sizeof(મૂલ્ય)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return સ્વામી_ઑબ્જેક્ટ + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t પ્રવેશ_બિંદુ) {
    uintptr_t 맨위 = ઉપયોગકર્તા_અંત_કરો, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t સ્ટેક_સંગ્રહ = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *ડેટા_સ્થિતિ = (uint64_t *)સ્ટેક_સંગ્રહ;
    *ડેટા_સ્થિતિ++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *ડેટા_સ્થિતિ++ = 주소목록[순번];
    *ડેટા_સ્થિતિ++ = 0; *ડેટા_સ્થિતિ++ = 0;
    *ડેટા_સ્થિતિ++ = 6; *ડેટા_સ્થિતિ++ = પેજ_આકાર;
    *ડેટા_સ્થિતિ++ = 9; *ડેટા_સ્થિતિ++ = પ્રવેશ_બિંદુ;
    *ડેટા_સ્થિતિ++ = 0; *ડેટા_સ્થિતિ++ = 0;
    return સ્ટેક_સંગ્રહ;
}
