#ifndef ကိုယ်ပိုင်ဥပမာခေါင်းစီး
#define ကိုယ်ပိုင်ဥပမာခေါင်းစီး
#include <파일규약.h>
#include <화면규약.h>
static int စာသားအလျား(const char *စာသား) { int အလျား=0;while(စာသား[အလျား])အလျား++;return အလျား; }
static int အထွက်(const char *စာသား) { int အလျား=စာသားအလျား(စာသား);return ဖိုင်ဒေတာရေး(1,စာသား,အလျား)==အလျား?0:1; }
#endif
