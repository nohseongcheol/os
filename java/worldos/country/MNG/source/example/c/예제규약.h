#ifndef 자체예제규약머리
#define 자체예제규약머리
#include <파일규약.h>
#include <화면규약.h>
static int Бичвэр_урт(const char *Бичвэр) { int урт_утга=0;while(Бичвэр[урт_утга])урт_утга++;return урт_утга; }
static int 출력(const char *Бичвэр) { int урт_утга=Бичвэр_урт(Бичвэр);return бичих_файл_өгөгдөл(1,Бичвэр,урт_утга)==урт_утга?0:1; }
#endif
