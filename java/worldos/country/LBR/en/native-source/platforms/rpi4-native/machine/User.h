#ifndef nativeUserHeader
#define nativeUserHeader
#include <stdint.h>
#include <stddef.h>
#define userBase 0x02000000ul
#define userImageEnd 0x02c00000ul
#define userHeapEnd 0x02ed0000ul
#define userStackAddress 0x02f00000ul
#define userEnd 0x03000000ul
#define userPageCount ((userEnd - userBase) / 4096ul)
#define userExecutableError (-8)
#define userDataError (-1001)
#define userExecutionError (-1002)
#define userInvalidInstruction (-1003)
#define userTimeout (-1004)
#define userInterrupted (-1005)
typedef struct { uint64_t registerData[31], commandPosition, stateCode, stackAddress; } userFrame;
void userSystemInit(void);
int userException(userFrame *, unsigned);
int userValidateElf(const unsigned char *, size_t);
uintptr_t boardUserRun(uintptr_t);
uintptr_t boardUserValidate(void);
uintptr_t boardUserControl(uintptr_t);
uint32_t readUserState(unsigned, unsigned);
#endif
