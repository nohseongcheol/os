/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(ব্যবহারকারী_ফ্রেম *ফাইল_ভুক্তি) {
    ব্যবহারকারী_ফ্রেম 변환값 = *ফাইল_ভুক্তি;
    uintptr_t 수치 = ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[8];
    switch (수치) {
    case 63: 변환값.নিবন্ধন_করুন_ডাটা[8] = 2; break;   /* read */
    case 64: 변환값.নিবন্ধন_করুন_ডাটা[8] = 1; break;   /* write */
    case 57: 변환값.নিবন্ধন_করুন_ডাটা[8] = 4; break;   /* close */
    case 62: 변환값.নিবন্ধন_করুন_ডাটা[8] = 5; break;   /* lseek */
    case 46: 변환값.নিবন্ধন_করুন_ডাটা[8] = 10; break;  /* ftruncate */
    case 82: 변환값.নিবন্ধন_করুন_ডাটা[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char পথ_2[65]; int 반환값 = নজির_পথ(ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[1], পথ_2); if (반환값) return 반환값;
        if ((int)ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[0] != -100 && পথ_2[0] != '/') return -95;
        if (수치 == 35 && ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[2]) return -95;
        if (수치 == 56 && (ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.নিবন্ধন_করুন_ডাটা[8] = 수치 == 56 ? 3 : 11;
        변환값.নিবন্ধন_করুন_ডাটা[0] = ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[1];
        변환값.নিবন্ধন_করুন_ডাটা[1] = ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.নিবন্ধন_করুন_ডাটা[2] = ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.নিবন্ধন_করুন_ডাটা[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[0] != 1) return -22;
        if (!사용자범위(ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), মান[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)ফাইল_ভুক্তি->নিবন্ধন_করুন_ডাটা[1], মান, sizeof(মান)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return মালিক_বস্তু + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ভুক্তি_বিন্দু) {
    uintptr_t 맨위 = ব্যবহারকারী_শেষ_করা, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t গাদা_স্টোরেজ = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *ডাটা_পদ = (uint64_t *)গাদা_স্টোরেজ;
    *ডাটা_পদ++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *ডাটা_পদ++ = 주소목록[순번];
    *ডাটা_পদ++ = 0; *ডাটা_পদ++ = 0;
    *ডাটা_পদ++ = 6; *ডাটা_পদ++ = পৃষ্ঠার_মাপ;
    *ডাটা_পদ++ = 9; *ডাটা_পদ++ = ভুক্তি_বিন্দু;
    *ডাটা_পদ++ = 0; *ডাটা_পদ++ = 0;
    return গাদা_স্টোরেজ;
}
