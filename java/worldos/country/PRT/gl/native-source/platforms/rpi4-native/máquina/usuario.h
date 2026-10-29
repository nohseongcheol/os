#ifndef 자체사용자머리
#define 자체사용자머리
#include <stdint.h>
#include <stddef.h>
#define usuario_BASE 0x02000000ul
#define usuario_IMAXE_finalizar 0x02c00000ul
#define 사용자동적기억끝 0x02ed0000ul
#define usuario_Montón_ENDEREZO 0x02f00000ul
#define usuario_finalizar 0x03000000ul
#define usuario_páxina_CONTAR ((usuario_finalizar - usuario_BASE) / 4096ul)
#define 사용자실행파일오류 (-8)
#define usuario_datos_erro (-1001)
#define 사용자실행오류 (-1002)
#define usuario_non_válido_instrución (-1003)
#define usuario_TIMEOUT (-1004)
#define 사용자중단됨 (-1005)
typedef struct { uint64_t rexistrarse_datos[31], comando_cargo, Estado_CÓDIGO, Montón_ENDEREZO; } usuario_marco;
void 사용자체계준비(void);
int usuario_excepción(usuario_marco *, unsigned);
int 사용자실행파일검사(const unsigned char *, size_t);
uintptr_t Panel_usuario_executar(uintptr_t);
uintptr_t Panel_usuario_validar(void);
uintptr_t Panel_control_do_usuario(uintptr_t);
uint32_t 사용자상태읽기(unsigned, unsigned);
#endif
