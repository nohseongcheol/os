// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 ফাংছন_মান. */
public final class ৱিজেট {
    private ৱিজেট() {}
    public static void 나중에실행(실행할일 কার্য্য_কাৰ্য) { ইভেণ্ট_লানি.나중에실행(কার্য্য_কাৰ্য); }
    public static লেবেল টেগ_মান(String টেক্সট, int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 폭, int 높이) {
        return new লেবেল(টেক্সট, 가로, উলম্ব_স্থান_সলনি_কৰক, 폭, 높이);
    }
    public static বুটাম বুটাম(String টেক্সট, int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 폭, int 높이, 동작받이 받이) {
        return new বুটাম(টেক্সট, 가로, উলম্ব_স্থান_সলনি_কৰক, 폭, 높이, 받이);
    }
    public static পাঠৰ_ক্ষেত্ৰ পাঠৰ_ক্ষেত্ৰ(String টেক্সট, int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 폭, int 높이) {
        return new পাঠৰ_ক্ষেত্ৰ(টেক্সট, 가로, উলম্ব_স্থান_সলনি_কৰক, 폭, 높이);
    }
}
