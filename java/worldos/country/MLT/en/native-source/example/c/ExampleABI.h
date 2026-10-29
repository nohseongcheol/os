#ifndef NativeExampleHeader
#define NativeExampleHeader
#include <FileABI.h>
#include <ScreenABI.h>
static int textLength(const char *text) { int lengthValue=0;while(text[lengthValue])lengthValue++;return lengthValue; }
static int Output(const char *text) { int lengthValue=textLength(text);return writeFileData(1,text,lengthValue)==lengthValue?0:1; }
#endif
