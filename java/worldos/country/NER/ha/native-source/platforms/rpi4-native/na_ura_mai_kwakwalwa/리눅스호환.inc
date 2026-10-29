/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(Mai_anfani_da_kwamfuta_allo *Fayil_Mashigar_bayanai) {
    Mai_anfani_da_kwamfuta_allo 변환값 = *Fayil_Mashigar_bayanai;
    uintptr_t 수치 = Fayil_Mashigar_bayanai->저장기값[8];
    switch (수치) {
    case 63: 변환값.저장기값[8] = 2; break;   /* read */
    case 64: 변환값.저장기값[8] = 1; break;   /* write */
    case 57: 변환값.저장기값[8] = 4; break;   /* close */
    case 62: 변환값.저장기값[8] = 5; break;   /* lseek */
    case 46: 변환값.저장기값[8] = 10; break;  /* ftruncate */
    case 82: 변환값.저장기값[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Hanyar_shiga[65]; int 반환값 = Kwafi_Hanyar_shiga(Fayil_Mashigar_bayanai->저장기값[1], Hanyar_shiga); if (반환값) return 반환값;
        if ((int)Fayil_Mashigar_bayanai->저장기값[0] != -100 && Hanyar_shiga[0] != '/') return -95;
        if (수치 == 35 && Fayil_Mashigar_bayanai->저장기값[2]) return -95;
        if (수치 == 56 && (Fayil_Mashigar_bayanai->저장기값[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.저장기값[8] = 수치 == 56 ? 3 : 11;
        변환값.저장기값[0] = Fayil_Mashigar_bayanai->저장기값[1];
        변환값.저장기값[1] = Fayil_Mashigar_bayanai->저장기값[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.저장기값[2] = Fayil_Mashigar_bayanai->저장기값[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.저장기값[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fayil_Mashigar_bayanai->저장기값[0] != 1) return -22;
        if (!사용자범위(Fayil_Mashigar_bayanai->저장기값[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), Daraja[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fayil_Mashigar_bayanai->저장기값[1], Daraja, sizeof(Daraja)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return mamallaki_abu + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t Mashigar_bayanai_maki) {
    uintptr_t 맨위 = Mai_anfani_da_kwamfuta_Ƙarshe, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t tara_Wurin_adana = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *자료위치 = (uint64_t *)tara_Wurin_adana;
    *자료위치++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *자료위치++ = 주소목록[순번];
    *자료위치++ = 0; *자료위치++ = 0;
    *자료위치++ = 6; *자료위치++ = Girman_shafi;
    *자료위치++ = 9; *자료위치++ = Mashigar_bayanai_maki;
    *자료위치++ = 0; *자료위치++ = 0;
    return tara_Wurin_adana;
}
