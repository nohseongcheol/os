/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(వినియోగదారు_చట్రం *ఫైలు_ప్రవేశం) {
    వినియోగదారు_చట్రం 변환값 = *ఫైలు_ప్రవేశం;
    uintptr_t 수치 = ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[8];
    switch (수치) {
    case 63: 변환값.నమోదు_చేయి_డేటా[8] = 2; break;   /* read */
    case 64: 변환값.నమోదు_చేయి_డేటా[8] = 1; break;   /* write */
    case 57: 변환값.నమోదు_చేయి_డేటా[8] = 4; break;   /* close */
    case 62: 변환값.నమోదు_చేయి_డేటా[8] = 5; break;   /* lseek */
    case 46: 변환값.నమోదు_చేయి_డేటా[8] = 10; break;  /* ftruncate */
    case 82: 변환값.నమోదు_చేయి_డేటా[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char పాత్[65]; int 반환값 = కాపీ_పథం(ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[1], పాత్); if (반환값) return 반환값;
        if ((int)ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[0] != -100 && పాత్[0] != '/') return -95;
        if (수치 == 35 && ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[2]) return -95;
        if (수치 == 56 && (ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.నమోదు_చేయి_డేటా[8] = 수치 == 56 ? 3 : 11;
        변환값.నమోదు_చేయి_డేటా[0] = ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[1];
        변환값.నమోదు_చేయి_డేటా[1] = ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.నమోదు_చేయి_డేటా[2] = ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.నమోదు_చేయి_డేటా[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[0] != 1) return -22;
        if (!사용자범위(ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), మూల్యం[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)ఫైలు_ప్రవేశం->నమోదు_చేయి_డేటా[1], మూల్యం, sizeof(మూల్యం)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return యజమాని_అంశం + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t ప్రవేశం_పాయింట్) {
    uintptr_t 맨위 = వినియోగదారు_ముగించు, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t దొంతర_నిల్వ = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *డేటా_స్థాయి = (uint64_t *)దొంతర_నిల్వ;
    *డేటా_స్థాయి++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *డేటా_స్థాయి++ = 주소목록[순번];
    *డేటా_స్థాయి++ = 0; *డేటా_స్థాయి++ = 0;
    *డేటా_స్థాయి++ = 6; *డేటా_స్థాయి++ = పుట_పరిమాణం;
    *డేటా_స్థాయి++ = 9; *డేటా_స్థాయి++ = ప్రవేశం_పాయింట్;
    *డేటా_స్థాయి++ = 0; *డేటా_స్థాయి++ = 0;
    return దొంతర_నిల్వ;
}
