/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(उपेगकर्तो_फ्रेम *फायल_प्रवेश) {
    उपेगकर्तो_फ्रेम 변환값 = *फायल_प्रवेश;
    uintptr_t 수치 = फायल_प्रवेश->नोंदणी_डेटा[8];
    switch (수치) {
    case 63: 변환값.नोंदणी_डेटा[8] = 2; break;   /* read */
    case 64: 변환값.नोंदणी_डेटा[8] = 1; break;   /* write */
    case 57: 변환값.नोंदणी_डेटा[8] = 4; break;   /* close */
    case 62: 변환값.नोंदणी_डेटा[8] = 5; break;   /* lseek */
    case 46: 변환값.नोंदणी_डेटा[8] = 10; break;  /* ftruncate */
    case 82: 변환값.नोंदणी_डेटा[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char पाथ[65]; int 반환값 = इन्सटन्स_पाथ(फायल_प्रवेश->नोंदणी_डेटा[1], पाथ); if (반환값) return 반환값;
        if ((int)फायल_प्रवेश->नोंदणी_डेटा[0] != -100 && पाथ[0] != '/') return -95;
        if (수치 == 35 && फायल_प्रवेश->नोंदणी_डेटा[2]) return -95;
        if (수치 == 56 && (फायल_प्रवेश->नोंदणी_डेटा[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.नोंदणी_डेटा[8] = 수치 == 56 ? 3 : 11;
        변환값.नोंदणी_डेटा[0] = फायल_प्रवेश->नोंदणी_डेटा[1];
        변환값.नोंदणी_डेटा[1] = फायल_प्रवेश->नोंदणी_डेटा[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.नोंदणी_डेटा[2] = फायल_प्रवेश->नोंदणी_डेटा[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.नोंदणी_डेटा[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (फायल_प्रवेश->नोंदणी_डेटा[0] != 1) return -22;
        if (!사용자범위(फायल_प्रवेश->नोंदणी_डेटा[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), मोल[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)फायल_प्रवेश->नोंदणी_डेटा[1], मोल, sizeof(मोल)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return धनी_ऑब्जॅक्ट + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t प्रवेश_पॉयंट) {
    uintptr_t 맨위 = उपेगकर्तो_सोपोवचें, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned आयटम_COUNT = 전달인수길이[순번] + 1;
        맨위 -= आयटम_COUNT; memcpy((void *)맨위, 전달인수[순번], आयटम_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t स्टॅक_सांठवण = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *डेटा_स्थिती = (uint64_t *)स्टॅक_सांठवण;
    *डेटा_स्थिती++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *डेटा_स्थिती++ = 주소목록[순번];
    *डेटा_स्थिती++ = 0; *डेटा_स्थिती++ = 0;
    *डेटा_स्थिती++ = 6; *डेटा_स्थिती++ = पानाचो_आंवाठ;
    *डेटा_स्थिती++ = 9; *डेटा_स्थिती++ = प्रवेश_पॉयंट;
    *डेटा_स्थिती++ = 0; *डेटा_स्थिती++ = 0;
    return स्टॅक_सांठवण;
}
