#ifndef _せんげん_たいけい_たいけいじょうほう
#define _せんげん_たいけい_たいけいじょうほう

struct たいけいじょうほう {
    char たいけいめい[65];
    char きかいめい[65];
    char たいけいはいふばん[65];
    char たいけいかいていばん[65];
    char きかいしゅるい[65];
};

#ifdef __cplusplus
extern "C" {
#endif
int たいけいじょうほうをえる(struct たいけいじょうほう *なまえ);
#ifdef __cplusplus
}
#endif

#endif
