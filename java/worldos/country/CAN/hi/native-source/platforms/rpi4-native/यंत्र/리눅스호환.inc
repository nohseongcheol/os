/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(उपयोगकर्ता_फ़्रेम *फ़ाइल_एन्ट्री) {
    उपयोगकर्ता_फ़्रेम 변환값 = *फ़ाइल_एन्ट्री;
    uintptr_t 수치 = फ़ाइल_एन्ट्री->रजिस्टर_डेटा[8];
    switch (수치) {
    case 63: 변환값.रजिस्टर_डेटा[8] = 2; break;   /* read */
    case 64: 변환값.रजिस्टर_डेटा[8] = 1; break;   /* write */
    case 57: 변환값.रजिस्टर_डेटा[8] = 4; break;   /* close */
    case 62: 변환값.रजिस्टर_डेटा[8] = 5; break;   /* lseek */
    case 46: 변환값.रजिस्टर_डेटा[8] = 10; break;  /* ftruncate */
    case 82: 변환값.रजिस्टर_डेटा[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char पथ[65]; int 반환값 = आवृत्ति_पथ(फ़ाइल_एन्ट्री->रजिस्टर_डेटा[1], पथ); if (반환값) return 반환값;
        if ((int)फ़ाइल_एन्ट्री->रजिस्टर_डेटा[0] != -100 && पथ[0] != '/') return -95;
        if (수치 == 35 && फ़ाइल_एन्ट्री->रजिस्टर_डेटा[2]) return -95;
        if (수치 == 56 && (फ़ाइल_एन्ट्री->रजिस्टर_डेटा[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.रजिस्टर_डेटा[8] = 수치 == 56 ? 3 : 11;
        변환값.रजिस्टर_डेटा[0] = फ़ाइल_एन्ट्री->रजिस्टर_डेटा[1];
        변환값.रजिस्टर_डेटा[1] = फ़ाइल_एन्ट्री->रजिस्टर_डेटा[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.रजिस्टर_डेटा[2] = फ़ाइल_एन्ट्री->रजिस्टर_डेटा[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = ढ़ेर_समाप्त_करें;
        변환값.रजिस्टर_डेटा[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (फ़ाइल_एन्ट्री->रजिस्टर_डेटा[0] != 1) return -22;
        if (!उपयोगकर्ता_श्रेणी(फ़ाइल_एन्ट्री->रजिस्टर_डेटा[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), मान[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)फ़ाइल_एन्ट्री->रजिस्टर_डेटा[1], मान, sizeof(मान)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return स्वामी_ऑब्जेक्ट + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t प्रवेश_बिदुं) {
    uintptr_t 맨위 = उपयोगकर्ता_समाप्त_करें, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t स्टैक_संग्रहण = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *डेटा_पद = (uint64_t *)स्टैक_संग्रहण;
    *डेटा_पद++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *डेटा_पद++ = 주소목록[순번];
    *डेटा_पद++ = 0; *डेटा_पद++ = 0;
    *डेटा_पद++ = 6; *डेटा_पद++ = पृष्ठ_आकार;
    *डेटा_पद++ = 9; *डेटा_पद++ = प्रवेश_बिदुं;
    *डेटा_पद++ = 0; *डेटा_पद++ = 0;
    return स्टैक_संग्रहण;
}
