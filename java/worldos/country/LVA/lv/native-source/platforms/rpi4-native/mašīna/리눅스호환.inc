/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(lietotājs_kadrs *Fails_ievade) {
    lietotājs_kadrs 변환값 = *Fails_ievade;
    uintptr_t 수치 = Fails_ievade->reģistrs_dati[8];
    switch (수치) {
    case 63: 변환값.reģistrs_dati[8] = 2; break;   /* read */
    case 64: 변환값.reģistrs_dati[8] = 1; break;   /* write */
    case 57: 변환값.reģistrs_dati[8] = 4; break;   /* close */
    case 62: 변환값.reģistrs_dati[8] = 5; break;   /* lseek */
    case 46: 변환값.reģistrs_dati[8] = 10; break;  /* ftruncate */
    case 82: 변환값.reģistrs_dati[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char CEĻŠ[65]; int 반환값 = kopēt_ceļš(Fails_ievade->reģistrs_dati[1], CEĻŠ); if (반환값) return 반환값;
        if ((int)Fails_ievade->reģistrs_dati[0] != -100 && CEĻŠ[0] != '/') return -95;
        if (수치 == 35 && Fails_ievade->reģistrs_dati[2]) return -95;
        if (수치 == 56 && (Fails_ievade->reģistrs_dati[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.reģistrs_dati[8] = 수치 == 56 ? 3 : 11;
        변환값.reģistrs_dati[0] = Fails_ievade->reģistrs_dati[1];
        변환값.reģistrs_dati[1] = Fails_ievade->reģistrs_dati[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.reģistrs_dati[2] = Fails_ievade->reģistrs_dati[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = kaudze_beigt_zvanu;
        변환값.reģistrs_dati[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fails_ievade->reģistrs_dati[0] != 1) return -22;
        if (!lietotājs_diapazons(Fails_ievade->reģistrs_dati[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fails_ievade->reģistrs_dati[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return īpašnieks_objekts + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ieejas_punkts) {
    uintptr_t 맨위 = lietotājs_beigt_zvanu, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned krājums_COUNT = 전달인수길이[순번] + 1;
        맨위 -= krājums_COUNT; memcpy((void *)맨위, 전달인수[순번], krājums_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t kopa_Krātuve = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dati_amats = (uint64_t *)kopa_Krātuve;
    *dati_amats++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *dati_amats++ = 주소목록[순번];
    *dati_amats++ = 0; *dati_amats++ = 0;
    *dati_amats++ = 6; *dati_amats++ = lappuses_izmēri;
    *dati_amats++ = 9; *dati_amats++ = ieejas_punkts;
    *dati_amats++ = 0; *dati_amats++ = 0;
    return kopa_Krātuve;
}
