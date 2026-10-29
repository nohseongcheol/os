/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(משתמש_למסגר *קובץ_ערך) {
    משתמש_למסגר 변환값 = *קובץ_ערך;
    uintptr_t 수치 = קובץ_ערך->אוגר_נתונים[8];
    switch (수치) {
    case 63: 변환값.אוגר_נתונים[8] = 2; break;   /* read */
    case 64: 변환값.אוגר_נתונים[8] = 1; break;   /* write */
    case 57: 변환값.אוגר_נתונים[8] = 4; break;   /* close */
    case 62: 변환값.אוגר_נתונים[8] = 5; break;   /* lseek */
    case 46: 변환값.אוגר_נתונים[8] = 10; break;  /* ftruncate */
    case 82: 변환값.אוגר_נתונים[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char נתיב[65]; int 반환값 = מופע_נתיב(קובץ_ערך->אוגר_נתונים[1], נתיב); if (반환값) return 반환값;
        if ((int)קובץ_ערך->אוגר_נתונים[0] != -100 && נתיב[0] != '/') return -95;
        if (수치 == 35 && קובץ_ערך->אוגר_נתונים[2]) return -95;
        if (수치 == 56 && (קובץ_ערך->אוגר_נתונים[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.אוגר_נתונים[8] = 수치 == 56 ? 3 : 11;
        변환값.אוגר_נתונים[0] = קובץ_ערך->אוגר_נתונים[1];
        변환값.אוגר_נתונים[1] = קובץ_ערך->אוגר_נתונים[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.אוגר_נתונים[2] = קובץ_ערך->אוגר_נתונים[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = ערימה_סיים_שיחה;
        변환값.אוגר_נתונים[8] = 8;
        intptr_t 반환값 = מקורי_מערכת_שיחה(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (קובץ_ערך->אוגר_נתונים[0] != 1) return -22;
        if (!משתמש_טווח(קובץ_ערך->אוגר_נתונים[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), ערך[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)קובץ_ערך->אוגר_נתונים[1], ערך, sizeof(ערך)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return בעלים_אובייקט + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return מקורי_מערכת_שיחה(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t נקודת_כניסה) {
    uintptr_t 맨위 = משתמש_סיים_שיחה, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t רמז_אחסון = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *נתונים_עמדה = (uint64_t *)רמז_אחסון;
    *נתונים_עמדה++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *נתונים_עמדה++ = 주소목록[순번];
    *נתונים_עמדה++ = 0; *נתונים_עמדה++ = 0;
    *נתונים_עמדה++ = 6; *נתונים_עמדה++ = גודל_עמוד;
    *נתונים_עמדה++ = 9; *נתונים_עמדה++ = נקודת_כניסה;
    *נתונים_עמדה++ = 0; *נתונים_עמדה++ = 0;
    return רמז_אחסון;
}
