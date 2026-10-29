#ifndef nativeUserCallHeader
#define nativeUserCallHeader
#include <stdint.h>
#include <stddef.h>
// JKOROS ABI v1: x8=invoke index, x0..x5=arguments, x0=result/negativeValue error. Linux ABI 아님.
static inline intptr_t userInvoke(uintptr_t index, uintptr_t firstOperand, uintptr_t secondOperand, uintptr_t thirdOperand,
                                uintptr_t fourthOperand, uintptr_t fifthOperand, uintptr_t sixthOperand) {
    register uintptr_t registerZero __asm__("x0") = firstOperand;
    register uintptr_t registerOne __asm__("x1") = secondOperand;
    register uintptr_t registerTwo __asm__("x2") = thirdOperand;
    register uintptr_t registerThree __asm__("x3") = fourthOperand;
    register uintptr_t registerFour __asm__("x4") = fifthOperand;
    register uintptr_t registerFive __asm__("x5") = sixthOperand;
    register uintptr_t registerEight __asm__("x8") = index;
    __asm__ volatile("svc #0" : "+r"(registerZero) : "r"(registerOne), "r"(registerTwo), "r"(registerThree), "r"(registerFour), "r"(registerFive), "r"(registerEight) : "memory", "cc");
    return (intptr_t)registerZero;
}
static inline intptr_t screenRectangle(unsigned xCoordinate, unsigned yCoordinate, unsigned requestedWidthValue, unsigned requestedHeightValue, unsigned rgbColour) {
    return userInvoke(13, xCoordinate, yCoordinate, rgbColour, requestedWidthValue, requestedHeightValue, 0);
}
static inline intptr_t userMemoryEnd(uintptr_t ending) { return userInvoke(8, ending, 0, 0, 0, 0, 0); }
static inline intptr_t readScreenWidth(void) { return userInvoke(22, 0, 0, 0, 0, 0, 0); }
static inline intptr_t readScreenHeight(void) { return userInvoke(22, 1, 0, 0, 0, 0, 0); }
static inline intptr_t waitForScreenKey(void) {
    intptr_t result = userInvoke(16, 0, 0, 0, 0, 0, 0);
    if (result < 0) return result;
    do { result = userInvoke(16, 1, 0, 0, 0, 0, 0); } while (result == -11);
    userInvoke(16, 2, 0, 0, 0, 0, 0);
    return result;
}
static inline intptr_t userArgumentCount(void) { return userInvoke(15, UINTPTR_MAX, 0, 0, 0, 0, 0); }
static inline intptr_t userArgument(unsigned index, char *contentValue, size_t size) {
    return userInvoke(15, index, (uintptr_t)contentValue, size, 0, 0, 0);
}
#endif
