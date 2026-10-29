/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t 리눅스체계호출(користувач_кадр *Файл_запис) {
    користувач_кадр 변환값 = *Файл_запис;
    uintptr_t 수치 = Файл_запис->реєстр_дані[8];
    switch (수치) {
    case 63: 변환값.реєстр_дані[8] = 2; break;   /* read */
    case 64: 변환값.реєстр_дані[8] = 1; break;   /* write */
    case 57: 변환값.реєстр_дані[8] = 4; break;   /* close */
    case 62: 변환값.реєстр_дані[8] = 5; break;   /* lseek */
    case 46: 변환값.реєстр_дані[8] = 10; break;  /* ftruncate */
    case 82: 변환값.реєстр_дані[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char шлях[65]; int 반환값 = екземпляр_шлях(Файл_запис->реєстр_дані[1], шлях); if (반환값) return 반환값;
        if ((int)Файл_запис->реєстр_дані[0] != -100 && шлях[0] != '/') return -95;
        if (수치 == 35 && Файл_запис->реєстр_дані[2]) return -95;
        if (수치 == 56 && (Файл_запис->реєстр_дані[2] & ~(0x7fful | 0x80000ul))) return -95;
        변환값.реєстр_дані[8] = 수치 == 56 ? 3 : 11;
        변환값.реєстр_дані[0] = Файл_запис->реєстр_дані[1];
        변환값.реєстр_дані[1] = Файл_запис->реєстр_дані[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        변환값.реєстр_дані[2] = Файл_запис->реєстр_дані[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t 이전항목 = динамічна_пам_ять_завершити_виклик;
        변환값.реєстр_дані[8] = 8;
        intptr_t 반환값 = 자체체계호출(&변환값);
        return 반환값 < 0 ? (intptr_t)이전항목 : 반환값;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (Файл_запис->реєстр_дані[0] != 1) return -22;
        if (!користувач_діапазон(Файл_запис->реєстр_дані[1], 16, 1)) return -14;
        uint64_t 밀리초 = 보드밀리초(), значення[2] = {밀리초 / 1000, (밀리초 % 1000) * 1000000};
        memcpy((void *)Файл_запис->реєстр_дані[1], значення, sizeof(значення)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return власник_об_єкт + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return 자체체계호출(&변환값);
}

static uintptr_t 리눅스시작쌓임(uintptr_t запис_бал) {
    uintptr_t 맨위 = користувач_завершити_виклик, 주소목록[8];
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) {
        unsigned 개수 = 전달인수길이[순번] + 1;
        맨위 -= 개수; memcpy((void *)맨위, 전달인수[순번], 개수); 주소목록[순번] = 맨위;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t стекова_памʼять = (맨위 - (전달인수개수 + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *дані_посада = (uint64_t *)стекова_памʼять;
    *дані_посада++ = 전달인수개수;
    for (unsigned 순번 = 0; 순번 < 전달인수개수; 순번++) *дані_посада++ = 주소목록[순번];
    *дані_посада++ = 0; *дані_посада++ = 0;
    *дані_посада++ = 6; *дані_посада++ = розмір_сторінки;
    *дані_посада++ = 9; *дані_посада++ = запис_бал;
    *дані_посада++ = 0; *дані_посада++ = 0;
    return стекова_памʼять;
}
