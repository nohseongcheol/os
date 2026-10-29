/* Deliberate opt-in, limited Linux AArch64 syscall ABI. No Linux kernel/libc.
 * Included after native_system_call so the same pointer/FD checks are reused.
 */
static intptr_t linuxSystemCall(userFrame *fileEntry) {
    userFrame translated = *fileEntry;
    uintptr_t numericValue = fileEntry->registerData[8];
    switch (numericValue) {
    case 63: translated.registerData[8] = 2; break;   /* read */
    case 64: translated.registerData[8] = 1; break;   /* write */
    case 57: translated.registerData[8] = 4; break;   /* close */
    case 62: translated.registerData[8] = 5; break;   /* lseek */
    case 46: translated.registerData[8] = 10; break;  /* ftruncate */
    case 82: translated.registerData[8] = 12; break;  /* fsync */
    case 56:                              /* openat */
    case 35: {                            /* unlinkat, ordinary files */
        char path[65]; int returnedValue = copyPath(fileEntry->registerData[1], path); if (returnedValue) return returnedValue;
        if ((int)fileEntry->registerData[0] != -100 && path[0] != '/') return -95;
        if (numericValue == 35 && fileEntry->registerData[2]) return -95;
        if (numericValue == 56 && (fileEntry->registerData[2] & ~(0x7fful | 0x80000ul))) return -95;
        translated.registerData[8] = numericValue == 56 ? 3 : 11;
        translated.registerData[0] = fileEntry->registerData[1];
        translated.registerData[1] = fileEntry->registerData[2] & ~0x80000ul; /* O_CLOEXEC: no execve yet */
        translated.registerData[2] = fileEntry->registerData[3];
        break;
    }
    case 214: {                           /* brk: failure returns old break */
        uintptr_t previous = heapEnd;
        translated.registerData[8] = 8;
        intptr_t returnedValue = nativeSystemCall(&translated);
        return returnedValue < 0 ? (intptr_t)previous : returnedValue;
    }
    case 113: {                           /* clock_gettime, MONOTONIC only */
        if (fileEntry->registerData[0] != 1) return -22;
        if (!userRange(fileEntry->registerData[1], 16, 1)) return -14;
        uint64_t milliseconds = boardMillis(), value[2] = {milliseconds / 1000, (milliseconds % 1000) * 1000000};
        memcpy((void *)fileEntry->registerData[1], value, sizeof(value)); return 0;
    }
    case 172:                             /* getpid */
    case 178: return ownerObject + 1;            /* gettid: one native thread */
    default: return -38;                   /* ENOSYS; never use native numbers */
    }
    return nativeSystemCall(&translated);
}

static uintptr_t linuxStartStack(uintptr_t entryPoint) {
    uintptr_t topEntry = userEnd, addresses[8];
    for (unsigned ordinalIndex = 0; ordinalIndex < forwardedArgumentCount; ordinalIndex++) {
        unsigned itemCount = forwardedArgumentLength[ordinalIndex] + 1;
        topEntry -= itemCount; memcpy((void *)topEntry, forwardedArgument[ordinalIndex], itemCount); addresses[ordinalIndex] = topEntry;
    }
    /* argc, argv[], NULL, empty envp, AT_PAGESZ, AT_ENTRY, AT_NULL. */
    uintptr_t stackStorage = (topEntry - (forwardedArgumentCount + 9) * sizeof(uint64_t)) & ~15ul;
    uint64_t *dataPosition = (uint64_t *)stackStorage;
    *dataPosition++ = forwardedArgumentCount;
    for (unsigned ordinalIndex = 0; ordinalIndex < forwardedArgumentCount; ordinalIndex++) *dataPosition++ = addresses[ordinalIndex];
    *dataPosition++ = 0; *dataPosition++ = 0;
    *dataPosition++ = 6; *dataPosition++ = pageSize;
    *dataPosition++ = 9; *dataPosition++ = entryPoint;
    *dataPosition++ = 0; *dataPosition++ = 0;
    return stackStorage;
}
