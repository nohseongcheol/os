/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(kasutaja_raam *Fail_kirje) {
    kasutaja_raam 변환값 = *Fail_kirje;
    uintptr_t 수치 = Fail_kirje->register_andmed[8];
    switch (수치) {
    case 63: 변환값.register_andmed[8] = 2; break;   /* read */
    case 64: 변환값.register_andmed[8] = 1; break;   /* write */
    case 57: 변환값.register_andmed[8] = 4; break;   /* close */
    case 62: 변환값.register_andmed[8] = 5; break;   /* lseek */
    case 46: 변환값.register_andmed[8] = 10; break;  /* ftruncate */
    case 82: 변환값.register_andmed[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char RADA[65]; int 반환값 = eksemplar_tee(Fail_kirje->register_andmed[1], RADA); if (반환값) return 반환값;
        if ((int)Fail_kirje->register_andmed[0] != -100 && RADA[0] != '/') return -95;
        if (수치 == 35 && Fail_kirje->register_andmed[2]) return -95;
        if (수치 == 56 && (Fail_kirje->register_andmed[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.register_andmed[8] = 수치 == 56 ? 3 : 11;
        변환값.register_andmed[0] = Fail_kirje->register_andmed[1];
        변환값.register_andmed[1] = Fail_kirje->register_andmed[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.register_andmed[2] = Fail_kirje->register_andmed[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.register_andmed[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fail_kirje->register_andmed[0] != 1) return -22;
        if (!kasutaja_vahemik(Fail_kirje->register_andmed[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fail_kirje->register_andmed[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return omanik_objekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t kirje_p) {
    uintptr_t 맨위 = kasutaja_lõpeta_kõne, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned kaup_COUNT = 전달인수길이[순번] + 1;
        맨위 -= kaup_COUNT; memcpy((void *)맨위, 전달인수[순번], kaup_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Virn_salvesti = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *andmed_ametikoht = (uint64_t *)Virn_salvesti;
    *andmed_ametikoht++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *andmed_ametikoht++ = 주소목록[순번];
    *andmed_ametikoht++ = 0; *andmed_ametikoht++ = 0;
    *andmed_ametikoht++ = 6; *andmed_ametikoht++ = lehekülje_suurus;
    *andmed_ametikoht++ = 9; *andmed_ametikoht++ = kirje_p;
    *andmed_ametikoht++ = 0; *andmed_ametikoht++ = 0;
    return Virn_salvesti;
}
