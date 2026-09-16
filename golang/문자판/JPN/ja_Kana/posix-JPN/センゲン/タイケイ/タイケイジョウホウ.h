/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _センゲン_タイケイ_タイケイジョウホウ
#define _センゲン_タイケイ_タイケイジョウホウ

struct タイケイジョウホウ {
    char タイケイメイ[65];
    char キカイメイ[65];
    char タイケイハイフバン[65];
    char タイケイカイテイバン[65];
    char キカイシュルイ[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int タイケイジョウホウヲエル(struct タイケイジョウホウ *ナマエ);
#ifdef __cplusplus
}
#endif

#endif
