/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(aṣàmúlò_férèmù *fáìlì_ìgbéwọlé) {
    aṣàmúlò_férèmù 변환값 = *fáìlì_ìgbéwọlé;
    uintptr_t 수치 = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[8];
    switch (수치) {
    case 63: 변환값.forúkọsílẹ̀_détà[8] = 2; break;   /* read */
    case 64: 변환값.forúkọsílẹ̀_détà[8] = 1; break;   /* write */
    case 57: 변환값.forúkọsílẹ̀_détà[8] = 4; break;   /* close */
    case 62: 변환값.forúkọsílẹ̀_détà[8] = 5; break;   /* lseek */
    case 46: 변환값.forúkọsílẹ̀_détà[8] = 10; break;  /* ftruncate */
    case 82: 변환값.forúkọsílẹ̀_détà[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ọ̀nà[65]; int 반환값 = ṣẹ̀dà_ọ̀nà(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[1], ọ̀nà); if (반환값) return 반환값;
        if ((int)fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0] != -100 && ọ̀nà[0] != '/') return -95;
        if (수치 == 35 && fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[2]) return -95;
        if (수치 == 56 && (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.forúkọsílẹ̀_détà[8] = 수치 == 56 ? 3 : 11;
        변환값.forúkọsílẹ̀_détà[0] = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[1];
        변환값.forúkọsílẹ̀_détà[1] = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.forúkọsílẹ̀_détà[2] = fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.forúkọsílẹ̀_détà[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[0] != 1) return -22;
        if (!사용자범위(fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), iye[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)fáìlì_ìgbéwọlé->forúkọsílẹ̀_détà[1], iye, sizeof(iye)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return Oníǹkan_nǹkan + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ìgbéwọlé_kókó) {
    uintptr_t 맨위 = aṣàmúlò_parí, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t kójọ_Ibi_ìpamọ́ = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *자료위치 = (uint64_t *)kójọ_Ibi_ìpamọ́;
    *자료위치++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *자료위치++ = 주소목록[순번];
    *자료위치++ = 0; *자료위치++ = 0;
    *자료위치++ = 6; *자료위치++ = ìwọ̀n_ojú_ìwé;
    *자료위치++ = 9; *자료위치++ = ìgbéwọlé_kókó;
    *자료위치++ = 0; *자료위치++ = 0;
    return kójọ_Ibi_ìpamọ́;
}
