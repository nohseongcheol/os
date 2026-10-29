/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(பயனர்_ஃபிரேம் *கோப்பு_உள்ளீடு) {
    பயனர்_ஃபிரேம் 변환값 = *கோப்பு_உள்ளீடு;
    uintptr_t 수치 = கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[8];
    switch (수치) {
    case 63: 변환값.பதிவு_செய்_தரவு[8] = 2; break;   /* read */
    case 64: 변환값.பதிவு_செய்_தரவு[8] = 1; break;   /* write */
    case 57: 변환값.பதிவு_செய்_தரவு[8] = 4; break;   /* close */
    case 62: 변환값.பதிவு_செய்_தரவு[8] = 5; break;   /* lseek */
    case 46: 변환값.பதிவு_செய்_தரவு[8] = 10; break;  /* ftruncate */
    case 82: 변환값.பதிவு_செய்_தரவு[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char பாதை_2[65]; int 반환값 = நகலெடு_பாதை(கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[1], பாதை_2); if (반환값) return 반환값;
        if ((int)கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[0] != -100 && பாதை_2[0] != '/') return -95;
        if (수치 == 35 && கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[2]) return -95;
        if (수치 == 56 && (கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.பதிவு_செய்_தரவு[8] = 수치 == 56 ? 3 : 11;
        변환값.பதிவு_செய்_தரவு[0] = கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[1];
        변환값.பதிவு_செய்_தரவு[1] = கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.பதிவு_செய்_தரவு[2] = கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = குவியல்_முடி;
        변환값.பதிவு_செய்_தரவு[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[0] != 1) return -22;
        if (!사용자범위(கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), மதிப்பு[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)கோப்பு_உள்ளீடு->பதிவு_செய்_தரவு[1], மதிப்பு, sizeof(மதிப்பு)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return உரிமையாளர்_பொருள் + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t நுழைவுப்_புள்ளி) {
    uintptr_t 맨위 = பயனர்_முடி, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t அடுக்கு_சேமிப்பகம் = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *தரவு_நிலை = (uint64_t *)அடுக்கு_சேமிப்பகம்;
    *தரவு_நிலை++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *தரவு_நிலை++ = 주소목록[순번];
    *தரவு_நிலை++ = 0; *தரவு_நிலை++ = 0;
    *தரவு_நிலை++ = 6; *தரவு_நிலை++ = பக்க_அளவு;
    *தரவு_நிலை++ = 9; *தரவு_நிலை++ = நுழைவுப்_புள்ளி;
    *தரவு_நிலை++ = 0; *தரவு_நிலை++ = 0;
    return அடுக்கு_சேமிப்பகம்;
}
