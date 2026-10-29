/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(кулланучы_кадр *файл_кертү) {
    кулланучы_кадр 변환값 = *файл_кертү;
    uintptr_t 수치 = файл_кертү->теркәлү_мәгълүмат[8];
    switch (수치) {
    case 63: 변환값.теркәлү_мәгълүмат[8] = 2; break;   /* read */
    case 64: 변환값.теркәлү_мәгълүмат[8] = 1; break;   /* write */
    case 57: 변환값.теркәлү_мәгълүмат[8] = 4; break;   /* close */
    case 62: 변환값.теркәлү_мәгълүмат[8] = 5; break;   /* lseek */
    case 46: 변환값.теркәлү_мәгълүмат[8] = 10; break;  /* ftruncate */
    case 82: 변환값.теркәлү_мәгълүмат[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Yul[65]; int 반환값 = экземпляр_юл(файл_кертү->теркәлү_мәгълүмат[1], Yul); if (반환값) return 반환값;
        if ((int)файл_кертү->теркәлү_мәгълүмат[0] != -100 && Yul[0] != '/') return -95;
        if (수치 == 35 && файл_кертү->теркәлү_мәгълүмат[2]) return -95;
        if (수치 == 56 && (файл_кертү->теркәлү_мәгълүмат[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.теркәлү_мәгълүмат[8] = 수치 == 56 ? 3 : 11;
        변환값.теркәлү_мәгълүмат[0] = файл_кертү->теркәлү_мәгълүмат[1];
        변환값.теркәлү_мәгълүмат[1] = файл_кертү->теркәлү_мәгълүмат[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.теркәлү_мәгълүмат[2] = файл_кертү->теркәлү_мәгълүмат[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.теркәлү_мәгълүмат[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (файл_кертү->теркәлү_мәгълүмат[0] != 1) return -22;
        if (!사용자범위(файл_кертү->теркәлү_мәгълүмат[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)файл_кертү->теркәлү_мәгълүмат[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return биләүче_объект + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t кертү_балл) {
    uintptr_t 맨위 = кулланучы_тәмамлау, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned элемент_COUNT = 전달인수길이[순번] + 1;
        맨위 -= элемент_COUNT; memcpy((void *)맨위, 전달인수[순번], элемент_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Стәк_Саклагыч = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *мәгълүмат_урнаштыру = (uint64_t *)Стәк_Саклагыч;
    *мәгълүмат_урнаштыру++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *мәгълүмат_урнаштыру++ = 주소목록[순번];
    *мәгълүмат_урнаштыру++ = 0; *мәгълүмат_урнаштыру++ = 0;
    *мәгълүмат_урнаштыру++ = 6; *мәгълүмат_урнаштыру++ = бит_зурлыгы;
    *мәгълүмат_урнаштыру++ = 9; *мәгълүмат_урнаштыру++ = кертү_балл;
    *мәгълүмат_урнаштыру++ = 0; *мәгълүмат_урнаштыру++ = 0;
    return Стәк_Саклагыч;
}
