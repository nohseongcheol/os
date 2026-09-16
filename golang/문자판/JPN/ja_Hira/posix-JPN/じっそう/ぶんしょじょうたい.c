/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <たいけい/ぶんしょじょうたい.h>
#include <たいけい/たいけいじょうほう.h>
#include <たいけい/たいけいよびだし.h>

enum { たいけいよびだし_ぶんしょじょうたい = 106, たいけいよびだし_れんけつじたいのじょうたいをえる = 107, たいけいよびだし_ひらいたぶんしょのじょうたいをえる = 108, たいけいよびだし_たいけいじょうほうをえる = 122 };

int ぶんしょじょうたい(const char *けいろ, struct ぶんしょじょうたい *かんしょうりょういき)
{
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_ぶんしょじょうたい, (long)けいろ, (long)かんしょうりょういき, 0, 0, 0, 0));
}

int れんけつじたいのじょうたいをえる(const char *けいろ, struct ぶんしょじょうたい *かんしょうりょういき)
{
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_れんけつじたいのじょうたいをえる, (long)けいろ, (long)かんしょうりょういき, 0, 0, 0, 0));
}

int ひらいたぶんしょのじょうたいをえる(int ぶんしょきじゅつばんごう, struct ぶんしょじょうたい *かんしょうりょういき)
{
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_ひらいたぶんしょのじょうたいをえる, ぶんしょきじゅつばんごう, (long)かんしょうりょういき, 0, 0, 0, 0));
}

int たいけいじょうほうをえる(struct たいけいじょうほう *なまえ)
{
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_たいけいじょうほうをえる, (long)なまえ, 0, 0, 0, 0, 0));
}
