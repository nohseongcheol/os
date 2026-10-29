#include "../naming/machineLinkNames.h"
#include "invoke.h"
typedef void (*initializerMethod)(void);
extern initializerMethod __init_array_start[], __init_array_end[], __fini_array_start[], __fini_array_end[];
extern int startUserProgram(int);
int userStart(int forwardedValue) {
    for (initializerMethod *dataPosition = __init_array_start; dataPosition < __init_array_end; dataPosition++) (*dataPosition)();
    int result = startUserProgram(forwardedValue);
    for (initializerMethod *dataPosition = __fini_array_end; dataPosition != __fini_array_start;) (*--dataPosition)();
    return result;
}
void *memset(void *dataPosition, int value, size_t entryCount) { unsigned char *destinationData = dataPosition; while (entryCount--) *destinationData++ = value; return dataPosition; }
void *memcpy(void *destinationData, const void *stringData, size_t entryCount) { unsigned char *firstValue = destinationData; const unsigned char *secondValue = stringData; while (entryCount--) *firstValue++ = *secondValue++; return destinationData; }
