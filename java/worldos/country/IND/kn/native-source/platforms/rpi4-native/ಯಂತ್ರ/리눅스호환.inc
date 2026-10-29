/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(ಬಳಕೆದಾರ_ಫ್ರೇಮ್ *ಫೈಲ್_ನಮೂದು) {
    ಬಳಕೆದಾರ_ಫ್ರೇಮ್ 변환값 = *ಫೈಲ್_ನಮೂದು;
    uintptr_t 수치 = ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[8];
    switch (수치) {
    case 63: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 2; break;   /* read */
    case 64: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 1; break;   /* write */
    case 57: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 4; break;   /* close */
    case 62: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 5; break;   /* lseek */
    case 46: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 10; break;  /* ftruncate */
    case 82: 변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char ಮಾರ್ಗ[65]; int 반환값 = ನಕಲಿಸು_ಹಾದಿ(ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[1], ಮಾರ್ಗ); if (반환값) return 반환값;
        if ((int)ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[0] != -100 && ಮಾರ್ಗ[0] != '/') return -95;
        if (수치 == 35 && ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[2]) return -95;
        if (수치 == 56 && (ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 수치 == 56 ? 3 : 11;
        변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[0] = ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[1];
        변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[1] = ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[2] = ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.ನೋಂದಾಯಿಸು_ಡೇಟಾ[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[0] != 1) return -22;
        if (!사용자범위(ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), ಮೌಲ್ಯ[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)ಫೈಲ್_ನಮೂದು->ನೋಂದಾಯಿಸು_ಡೇಟಾ[1], ಮೌಲ್ಯ, sizeof(ಮೌಲ್ಯ)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return ಮಾಲೀಕ_ಆಬ್ಜೆಕ್ಟ್ + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ನಮೂದು_ಬಿಂದು) {
    uintptr_t 맨위 = ಬಳಕೆದಾರ_ಅಂತ್ಯಗೊಳಿಸು, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t ಸ್ಟ್ಯಾಕ್_ಸಂಗ್ರಹ = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *ಡೇಟಾ_ಹುದ್ದೆ = (uint64_t *)ಸ್ಟ್ಯಾಕ್_ಸಂಗ್ರಹ;
    *ಡೇಟಾ_ಹುದ್ದೆ++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *ಡೇಟಾ_ಹುದ್ದೆ++ = 주소목록[순번];
    *ಡೇಟಾ_ಹುದ್ದೆ++ = 0; *ಡೇಟಾ_ಹುದ್ದೆ++ = 0;
    *ಡೇಟಾ_ಹುದ್ದೆ++ = 6; *ಡೇಟಾ_ಹುದ್ದೆ++ = ಪುಟದ_ಗಾತ್ರ;
    *ಡೇಟಾ_ಹುದ್ದೆ++ = 9; *ಡೇಟಾ_ಹುದ್ದೆ++ = ನಮೂದು_ಬಿಂದು;
    *ಡೇಟಾ_ಹುದ್ದೆ++ = 0; *ಡೇಟಾ_ಹುದ್ದೆ++ = 0;
    return ಸ್ಟ್ಯಾಕ್_ಸಂಗ್ರಹ;
}
