/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <ぶんしょせいぎょ.h>
#include <たいけい/たいけいよびだし.h>

enum { たいけいよびだし_ひらく = 5, たいけいよびだし_ぶんしょをつくる = 8, たいけいよびだし_ぶんしょをせいぎょする = 55 };

int ひらく(const char *けいろ, int ひらくさいのしてい, ...)
{
    ぶんしょほうしきがた りようほうしき = 0;
    if ((ひらくさいのしてい & なければつくる) != 0) {
        __builtin_va_list かへんひきすう;
        __builtin_va_start(かへんひきすう, ひらくさいのしてい);
        りようほうしき = __builtin_va_arg(かへんひきすう, ぶんしょほうしきがた);
        __builtin_va_end(かへんひきすう);
    }
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_ひらく, (long)けいろ, ひらくさいのしてい, りようほうしき, 0, 0, 0));
}

int ぶんしょをつくる(const char *けいろ, ぶんしょほうしきがた りようほうしき)
{
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_ぶんしょをつくる, (long)けいろ, りようほうしき, 0, 0, 0, 0));
}

int ぶんしょをせいぎょする(int ぶんしょきじゅつばんごう, int せいぎょめいれい, ...)
{
    long ひきすうち = 0;
    if (せいぎょめいれい == きじゅつばんごうふくせい || せいぎょめいれい == きじゅつばんごうひょうしきせってい || せいぎょめいれい == ぶんしょじょうたいひょうしきせってい) {
        __builtin_va_list かへんひきすう;
        __builtin_va_start(かへんひきすう, せいぎょめいれい);
        ひきすうち = __builtin_va_arg(かへんひきすう, long);
        __builtin_va_end(かへんひきすう);
    }
    return (int)__syscall_result(
        __syscall6(たいけいよびだし_ぶんしょをせいぎょする, ぶんしょきじゅつばんごう, せいぎょめいれい, ひきすうち, 0, 0, 0));
}
