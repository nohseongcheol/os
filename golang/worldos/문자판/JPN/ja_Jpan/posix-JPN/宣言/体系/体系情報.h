#ifndef _宣言_体系_体系情報
#define _宣言_体系_体系情報

struct 体系情報 {
    char 体系名[65];
    char 機械名[65];
    char 体系配布版[65];
    char 体系改訂版[65];
    char 機械種類[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int 体系情報を得る(struct 体系情報 *名前);
#ifdef __cplusplus
}
#endif

#endif
