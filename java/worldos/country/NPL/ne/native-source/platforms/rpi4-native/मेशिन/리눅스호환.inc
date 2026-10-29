/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(प्रयोगकर्ता_फ्रेम *फाइल_प्रविष्टि) {
    प्रयोगकर्ता_फ्रेम 변환값 = *फाइल_प्रविष्टि;
    uintptr_t 수치 = फाइल_प्रविष्टि->दर्ता_लगत[8];
    switch (수치) {
    case 63: 변환값.दर्ता_लगत[8] = 2; break;   /* read */
    case 64: 변환값.दर्ता_लगत[8] = 1; break;   /* write */
    case 57: 변환값.दर्ता_लगत[8] = 4; break;   /* close */
    case 62: 변환값.दर्ता_लगत[8] = 5; break;   /* lseek */
    case 46: 변환값.दर्ता_लगत[8] = 10; break;  /* ftruncate */
    case 82: 변환값.दर्ता_लगत[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char मार्ग[65]; int 반환값 = उद्धरण_बाटो(फाइल_प्रविष्टि->दर्ता_लगत[1], मार्ग); if (반환값) return 반환값;
        if ((int)फाइल_प्रविष्टि->दर्ता_लगत[0] != -100 && मार्ग[0] != '/') return -95;
        if (수치 == 35 && फाइल_प्रविष्टि->दर्ता_लगत[2]) return -95;
        if (수치 == 56 && (फाइल_प्रविष्टि->दर्ता_लगत[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.दर्ता_लगत[8] = 수치 == 56 ? 3 : 11;
        변환값.दर्ता_लगत[0] = फाइल_प्रविष्टि->दर्ता_लगत[1];
        변환값.दर्ता_लगत[1] = फाइल_प्रविष्टि->दर्ता_लगत[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.दर्ता_लगत[2] = फाइल_प्रविष्टि->दर्ता_लगत[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.दर्ता_लगत[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (फाइल_प्रविष्टि->दर्ता_लगत[0] != 1) return -22;
        if (!사용자범위(फाइल_प्रविष्टि->दर्ता_लगत[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), मान[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)फाइल_प्रविष्टि->दर्ता_लगत[1], मान, sizeof(मान)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return मालिक_वस्तु + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t प्रविष्टि_अंक) {
    uintptr_t 맨위 = प्रयोगकर्ता_समाप्त_गर्नुहोस्, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t चाङ_भण्डारण = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *लगत_राख्नुहोस् = (uint64_t *)चाङ_भण्डारण;
    *लगत_राख्नुहोस्++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *लगत_राख्नुहोस्++ = 주소목록[순번];
    *लगत_राख्नुहोस्++ = 0; *लगत_राख्नुहोस्++ = 0;
    *लगत_राख्नुहोस्++ = 6; *लगत_राख्नुहोस्++ = पृष्ठ_साइज;
    *लगत_राख्नुहोस्++ = 9; *लगत_राख्नुहोस्++ = प्रविष्टि_अंक;
    *लगत_राख्नुहोस्++ = 0; *लगत_राख्नुहोस्++ = 0;
    return चाङ_भण्डारण;
}
