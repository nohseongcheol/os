#ifndef nativeRemoteConnectionHeader
#define nativeRemoteConnectionHeader
#include "../naming/machineLinkNames.h"
#include <stdint.h>
void prepareRemote(void);
void inspectRemote(void);
void remoteOutput(unsigned char);
int remoteInput(void);
int feedRemoteInput(const unsigned char *,unsigned);
uintptr_t boardRemoteControl(uintptr_t,uintptr_t);
uintptr_t boardEndRemoteCommand(uintptr_t);
uintptr_t boardRemoteWait(uintptr_t);
void inspectRemoteDisplay(void);
int controlRemoteDisplay(unsigned);
#endif
