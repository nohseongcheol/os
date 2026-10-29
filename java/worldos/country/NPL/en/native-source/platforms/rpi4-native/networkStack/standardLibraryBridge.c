#include "string.h"
size_t strlen(const char *stringData) { const char *dataPosition = stringData; while (*dataPosition) dataPosition++; return dataPosition - stringData; }
int memcmp(const void *firstValue, const void *secondValue, size_t itemCount) { const unsigned char *xCoordinate = firstValue, *yCoordinate = secondValue; while (itemCount--) { if (*xCoordinate != *yCoordinate) return (int)*xCoordinate - *yCoordinate; xCoordinate++; yCoordinate++; } return 0; }
void *memmove(void *destinationData, const void *stringData, size_t itemCount) { unsigned char *xCoordinate = destinationData; const unsigned char *yCoordinate = stringData; if (xCoordinate < yCoordinate) { for (size_t ordinalIndex = 0; ordinalIndex < itemCount; ordinalIndex++) xCoordinate[ordinalIndex] = yCoordinate[ordinalIndex]; } else { while (itemCount) { itemCount--; xCoordinate[itemCount] = yCoordinate[itemCount]; } } return destinationData; }
int strncmp(const char *firstValue, const char *secondValue, size_t itemCount) { while (itemCount--) { unsigned char xCoordinate = *firstValue++, yCoordinate = *secondValue++; if (xCoordinate != yCoordinate) return (int)xCoordinate-yCoordinate; if (!xCoordinate) return 0; } return 0; }
/* lwIP only uses this for small decimal interface numbers. */
long strtol(const char *stringData, char **endOffset, int backgroundValue) {
    const char *startOffset = stringData; unsigned long value = 0; int encodingValue = 1, anyValue = 0;
    while (*stringData == ' ' || (*stringData >= 9 && *stringData <= 13)) stringData++;
    if (*stringData == '-' || *stringData == '+') { if (*stringData == '-') encodingValue = -1; stringData++; }
    if (backgroundValue == 0) backgroundValue = 10;
    while (*stringData >= '0' && *stringData <= '9' && *stringData - '0' < backgroundValue) {
        unsigned digitValue = *stringData++ - '0'; anyValue = 1;
        if (value > (0x7ffffffffffffffful - digitValue) / (unsigned)backgroundValue) value = 0x7ffffffffffffffful;
        else value = value * backgroundValue + digitValue;
    }
    if (endOffset) *endOffset = (char *)(anyValue ? stringData : startOffset); return encodingValue > 0 ? (long)value : -(long)value;
}
int atoi(const char *stringData) { return (int)strtol(stringData, 0, 10); }
