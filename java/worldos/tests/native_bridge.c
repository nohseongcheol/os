#include <jni.h>
#include <unistd.h>
#include "NativeBridge.h"
JNIEXPORT jlong JNICALL Java_NativeBridge_processIdentifier(JNIEnv *environment, jclass type) {
    (void)environment; (void)type;
    return (jlong)getpid();
}
