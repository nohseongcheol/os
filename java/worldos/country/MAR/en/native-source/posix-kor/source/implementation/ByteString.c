#include <string.h>
#include <stdio.h>
#include <unistd.h>
size_t strlen(const char *stringValue) { size_t lengthValue = 0; while (stringValue[lengthValue]) lengthValue++; return lengthValue; }
int strcmp(const char *frontValue, const char *backValue) {
    while (*frontValue && *frontValue == *backValue) { frontValue++; backValue++; }
    return (unsigned char)*frontValue - (unsigned char)*backValue;
}
int memcmp(const void *frontValue, const void *backValue, size_t byteCount) {
    const unsigned char *firstOperand = frontValue, *secondOperand = backValue;
    for (size_t slotEntry = 0; slotEntry < byteCount; slotEntry++) if (firstOperand[slotEntry] != secondOperand[slotEntry]) return firstOperand[slotEntry] - secondOperand[slotEntry];
    return 0;
}
void *memcpy(void *destinationValue, const void *original, size_t byteCount) {
    unsigned char *firstOperand = destinationValue; const unsigned char *secondOperand = original;
    for (size_t slotEntry = 0; slotEntry < byteCount; slotEntry++) firstOperand[slotEntry] = secondOperand[slotEntry];
    return destinationValue;
}
void *memset(void *destinationValue, int value, size_t byteCount) {
    unsigned char *data = destinationValue;
    for (size_t slotEntry = 0; slotEntry < byteCount; slotEntry++) data[slotEntry] = value;
    return destinationValue;
}
int putchar(int Characters) { unsigned char value = Characters; return write(1, &value, 1) == 1 ? value : EOF; }
int puts(const char *stringValue) {
    size_t lengthValue = strlen(stringValue), position = 0;
    while (position < lengthValue) { ssize_t result = write(1, stringValue + position, lengthValue - position); if (result <= 0) return EOF; position += result; }
    return putchar('\n') == EOF ? EOF : 0;
}
