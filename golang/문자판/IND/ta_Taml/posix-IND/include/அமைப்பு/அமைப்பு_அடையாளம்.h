/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _include_அமைப்பு_அமைப்பு_அடையாளம்
#define _include_அமைப்பு_அமைப்பு_அடையாளம்

struct utsname {
    char sysname[65];
    char nodename[65];
    char release[65];
    char version[65];
    char machine[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int அமைப்புத்_தகவலைப்_பெறு(struct utsname *அமைப்பின்_அடையாளம்);
#ifdef __cplusplus
}
#endif

#endif
