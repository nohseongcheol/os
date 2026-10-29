/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(gumagamit_frame *file_pagpasok) {
    gumagamit_frame 변환값 = *file_pagpasok;
    uintptr_t 수치 = file_pagpasok->magrehistro_data[8];
    switch (수치) {
    case 63: 변환값.magrehistro_data[8] = 2; break;   /* read */
    case 64: 변환값.magrehistro_data[8] = 1; break;   /* write */
    case 57: 변환값.magrehistro_data[8] = 4; break;   /* close */
    case 62: 변환값.magrehistro_data[8] = 5; break;   /* lseek */
    case 46: 변환값.magrehistro_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.magrehistro_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char path[65]; int 반환값 = gumawa_ng_kopya_path(file_pagpasok->magrehistro_data[1], path); if (반환값) return 반환값;
        if ((int)file_pagpasok->magrehistro_data[0] != -100 && path[0] != '/') return -95;
        if (수치 == 35 && file_pagpasok->magrehistro_data[2]) return -95;
        if (수치 == 56 && (file_pagpasok->magrehistro_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.magrehistro_data[8] = 수치 == 56 ? 3 : 11;
        변환값.magrehistro_data[0] = file_pagpasok->magrehistro_data[1];
        변환값.magrehistro_data[1] = file_pagpasok->magrehistro_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.magrehistro_data[2] = file_pagpasok->magrehistro_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = 동적기억끝;
        변환값.magrehistro_data[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (file_pagpasok->magrehistro_data[0] != 1) return -22;
        if (!사용자범위(file_pagpasok->magrehistro_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), VALUE[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)file_pagpasok->magrehistro_data[1], VALUE, sizeof(VALUE)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return may_ari_bagay + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t pagpasok_point) {
    uintptr_t 맨위 = gumagamit_tapusin, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned item_COUNT = 전달인수길이[순번] + 1;
        맨위 -= item_COUNT; memcpy((void *)맨위, 전달인수[순번], item_COUNT); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t Stack_Storage = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_posisyon = (uint64_t *)Stack_Storage;
    *data_posisyon++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_posisyon++ = 주소목록[순번];
    *data_posisyon++ = 0; *data_posisyon++ = 0;
    *data_posisyon++ = 6; *data_posisyon++ = laki_ng_pahina;
    *data_posisyon++ = 9; *data_posisyon++ = pagpasok_point;
    *data_posisyon++ = 0; *data_posisyon++ = 0;
    return Stack_Storage;
}
