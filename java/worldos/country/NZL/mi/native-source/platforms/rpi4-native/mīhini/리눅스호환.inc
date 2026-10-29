/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(kaiwhakamahi_tāpare *kōnae_tāurunga) {
    kaiwhakamahi_tāpare 변환값 = *kōnae_tāurunga;
    uintptr_t 수치 = kōnae_tāurunga->rēhita_raraunga[8];
    switch (수치) {
    case 63: 변환값.rēhita_raraunga[8] = 2; break;   /* read */
    case 64: 변환값.rēhita_raraunga[8] = 1; break;   /* write */
    case 57: 변환값.rēhita_raraunga[8] = 4; break;   /* close */
    case 62: 변환값.rēhita_raraunga[8] = 5; break;   /* lseek */
    case 46: 변환값.rēhita_raraunga[8] = 10; break;  /* ftruncate */
    case 82: 변환값.rēhita_raraunga[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ara[65]; int 반환값 = tārua_ara(kōnae_tāurunga->rēhita_raraunga[1], ara); if (반환값) return 반환값;
        if ((int)kōnae_tāurunga->rēhita_raraunga[0] != -100 && ara[0] != '/') return -95;
        if (수치 == 35 && kōnae_tāurunga->rēhita_raraunga[2]) return -95;
        if (수치 == 56 && (kōnae_tāurunga->rēhita_raraunga[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.rēhita_raraunga[8] = 수치 == 56 ? 3 : 11;
        변환값.rēhita_raraunga[0] = kōnae_tāurunga->rēhita_raraunga[1];
        변환값.rēhita_raraunga[1] = kōnae_tāurunga->rēhita_raraunga[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.rēhita_raraunga[2] = kōnae_tāurunga->rēhita_raraunga[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.rēhita_raraunga[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (kōnae_tāurunga->rēhita_raraunga[0] != 1) return -22;
        if (!사용자범위(kōnae_tāurunga->rēhita_raraunga[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), uara[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)kōnae_tāurunga->rēhita_raraunga[1], uara, sizeof(uara)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return kaipupuri_ahanoa + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t tāurunga_ira) {
    uintptr_t 맨위 = kaiwhakamahi_mutu, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned tuemi_COUNT = 전달인수길이[순번] + 1;
        맨위 -= tuemi_COUNT; memcpy((void *)맨위, 전달인수[순번], tuemi_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Huinga_Rokiroki = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *raraunga_tūranga = (uint64_t *)Huinga_Rokiroki;
    *raraunga_tūranga++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *raraunga_tūranga++ = 주소목록[순번];
    *raraunga_tūranga++ = 0; *raraunga_tūranga++ = 0;
    *raraunga_tūranga++ = 6; *raraunga_tūranga++ = rahinga_whārangi;
    *raraunga_tūranga++ = 9; *raraunga_tūranga++ = tāurunga_ira;
    *raraunga_tūranga++ = 0; *raraunga_tūranga++ = 0;
    return Huinga_Rokiroki;
}
