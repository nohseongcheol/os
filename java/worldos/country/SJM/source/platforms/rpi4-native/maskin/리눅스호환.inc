/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(bruker_bilde *Fil_oppføring) {
    bruker_bilde 변환값 = *Fil_oppføring;
    uintptr_t 수치 = Fil_oppføring->register_data[8];
    switch (수치) {
    case 63: 변환값.register_data[8] = 2; break;   /* read */
    case 64: 변환값.register_data[8] = 1; break;   /* write */
    case 57: 변환값.register_data[8] = 4; break;   /* close */
    case 62: 변환값.register_data[8] = 5; break;   /* lseek */
    case 46: 변환값.register_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.register_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char Sti[65]; int 반환값 = kopiere_bane(Fil_oppføring->register_data[1], Sti); if (반환값) return 반환값;
        if ((int)Fil_oppføring->register_data[0] != -100 && Sti[0] != '/') return -95;
        if (수치 == 35 && Fil_oppføring->register_data[2]) return -95;
        if (수치 == 56 && (Fil_oppføring->register_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.register_data[8] = 수치 == 56 ? 3 : 11;
        변환값.register_data[0] = Fil_oppføring->register_data[1];
        변환값.register_data[1] = Fil_oppføring->register_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.register_data[2] = Fil_oppføring->register_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Forrige = heap_avslutte_en_samtale;
        변환값.register_data[8] = 8;
        intptr_t 반환값 = opprinnelig_System_Ring(&변환값);
        return 반환값 < 0 ? (intptr_t)Forrige : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Fil_oppføring->register_data[0] != 1) return -22;
        if (!bruker_område(Fil_oppføring->register_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VERDI[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Fil_oppføring->register_data[1], VERDI, sizeof(VERDI)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return eier_objekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return opprinnelig_System_Ring(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t inngangspunkt) {
    uintptr_t 맨위 = bruker_avslutte_en_samtale, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned vare_ANTALL = 전달인수길이[순번] + 1;
        맨위 -= vare_ANTALL; memcpy((void *)맨위, 전달인수[순번], vare_ANTALL); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t stakk_lager = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_plassere = (uint64_t *)stakk_lager;
    *data_plassere++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_plassere++ = 주소목록[순번];
    *data_plassere++ = 0; *data_plassere++ = 0;
    *data_plassere++ = 6; *data_plassere++ = sidestørrelse;
    *data_plassere++ = 9; *data_plassere++ = inngangspunkt;
    *data_plassere++ = 0; *data_plassere++ = 0;
    return stakk_lager;
}
