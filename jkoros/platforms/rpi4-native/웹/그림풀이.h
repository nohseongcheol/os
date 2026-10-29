/* stb_image의 MIT 조건은 외부원문/stb/stb_image.h 끝에 보존한다. */
static union {uint64_t 정렬;unsigned char 자료[2*1024*1024];} 그림기억;
static unsigned 그림기억자리;
static void *그림할당(size_t 크기){if(크기>sizeof 그림기억.자료-16)return 0;unsigned 수=((unsigned)크기+15)&~15u;if(수+16>sizeof 그림기억.자료-그림기억자리)return 0;unsigned char *곳=그림기억.자료+그림기억자리;*(size_t*)곳=크기;그림기억자리+=수+16;return 곳+16;}
static void *그림재할당(void *원본,size_t 크기){if(!원본)return 그림할당(크기);size_t 이전=*(size_t*)((unsigned char*)원본-16);void *새것=그림할당(크기);if(새것)memcpy(새것,원본,이전<크기?이전:크기);return 새것;}
#define STBI_MALLOC 그림할당
#define STBI_REALLOC 그림재할당
#define STBI_FREE(곳) ((void)(곳))
#define STBI_ASSERT(조건) ((void)0)
#define STBI_NO_STDIO
#define STBI_NO_SIMD
#define STBI_NO_THREAD_LOCALS
#define STBI_NO_HDR
#define STBI_NO_LINEAR
#define STBI_NO_FAILURE_STRINGS
#define STBI_ONLY_PNG
#define STBI_ONLY_JPEG
#define STBI_ONLY_GIF
#define STBI_ONLY_BMP
#define STBI_MAX_DIMENSIONS 2048
#include <stdlib.h>
static int 그림절댓값(int 값){return 값<0?-값:값;}
#define abs 그림절댓값
#define STB_IMAGE_IMPLEMENTATION
#include "../vendor/stb/stb_image.h"

#undef abs
