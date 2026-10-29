#ifndef _선언_체계_체제정보
#define _선언_체계_체제정보

struct 체제정보 {
    char 체제이름[65];
    char 기계이름[65];
    char 체제배포판[65];
    char 체제개정판[65];
    char 기계종류[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int 체제정보얻기(struct 체제정보 *이름);
#ifdef __cplusplus
}
#endif

#endif
