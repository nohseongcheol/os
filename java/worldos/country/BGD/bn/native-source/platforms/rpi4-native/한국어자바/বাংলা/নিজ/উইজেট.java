// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** বাংলা 화면 구성요소를 만드는 편의 ফাংশন_মান. */
public final class উইজেট {
    private উইজেট() {}
    public static void 나중에실행(실행할일 কার্য_কর্ম) { ঘটনা_সারিবদ্ধ.나중에실행(কার্য_কর্ম); }
    public static লেবেল ট্যাগ_মান(String পাঠ, int 가로, int উল্লম্ব_পদ, int 폭, int 높이) {
        return new লেবেল(পাঠ, 가로, উল্লম্ব_পদ, 폭, 높이);
    }
    public static বোতাম বোতাম(String পাঠ, int 가로, int উল্লম্ব_পদ, int 폭, int 높이, 동작받이 받이) {
        return new বোতাম(পাঠ, 가로, উল্লম্ব_পদ, 폭, 높이, 받이);
    }
    public static পাঠ্য_ক্ষেত্র পাঠ্য_ক্ষেত্র(String পাঠ, int 가로, int উল্লম্ব_পদ, int 폭, int 높이) {
        return new পাঠ্য_ক্ষেত্র(পাঠ, 가로, উল্লম্ব_পদ, 폭, 높이);
    }
}
