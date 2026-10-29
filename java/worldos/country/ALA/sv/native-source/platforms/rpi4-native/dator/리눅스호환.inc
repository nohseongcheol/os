/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(användare_ram *fil_post) {
    användare_ram 변환값 = *fil_post;
    uintptr_t 수치 = fil_post->register_data[8];
    switch (수치) {
    case 63: 변환값.register_data[8] = 2; break;   /* read */
    case 64: 변환값.register_data[8] = 1; break;   /* write */
    case 57: 변환값.register_data[8] = 4; break;   /* close */
    case 62: 변환값.register_data[8] = 5; break;   /* lseek */
    case 46: 변환값.register_data[8] = 10; break;  /* ftruncate */
    case 82: 변환값.register_data[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char sökväg_2[65]; int 반환값 = kopia_väg(fil_post->register_data[1], sökväg_2); if (반환값) return 반환값;
        if ((int)fil_post->register_data[0] != -100 && sökväg_2[0] != '/') return -95;
        if (수치 == 35 && fil_post->register_data[2]) return -95;
        if (수치 == 56 && (fil_post->register_data[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.register_data[8] = 수치 == 56 ? 3 : 11;
        변환값.register_data[0] = fil_post->register_data[1];
        변환값.register_data[1] = fil_post->register_data[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.register_data[2] = fil_post->register_data[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t Föregående = heap_avsluta;
        변환값.register_data[8] = 8;
        intptr_t 반환값 = ursprunglig_System_ring(&변환값);
        return 반환값 < 0 ? (intptr_t)Föregående : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (fil_post->register_data[0] != 1) return -22;
        if (!användare_område(fil_post->register_data[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), värde[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)fil_post->register_data[1], värde, sizeof(värde)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return ägare_objekt + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return ursprunglig_System_ring(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t startpunkt) {
    uintptr_t 맨위 = användare_avsluta, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned objekt_ANTAL = 전달인수길이[순번] + 1;
        맨위 -= objekt_ANTAL; memcpy((void *)맨위, 전달인수[순번], objekt_ANTAL); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t stackminne = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *data_placera = (uint64_t *)stackminne;
    *data_placera++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *data_placera++ = 주소목록[순번];
    *data_placera++ = 0; *data_placera++ = 0;
    *data_placera++ = 6; *data_placera++ = sidstorlek;
    *data_placera++ = 9; *data_placera++ = startpunkt;
    *data_placera++ = 0; *data_placera++ = 0;
    return stackminne;
}
