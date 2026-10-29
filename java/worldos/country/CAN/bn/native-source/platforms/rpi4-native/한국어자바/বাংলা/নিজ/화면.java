// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলা.নিজ;
/** 화면(畫面): 부팅 때 선택한 크기의 নিজ কারনেল_মান RGB32 프레임버퍼. */
public final class 화면 {
    private 화면() {}
    public static int 너비() { int মান = কারনেল_মান.화면너비(); if (মান < 0) throw new অবস্হা_ব্যতিক্রম("프레임버퍼 없음"); return মান; }
    public static int 높이() { int মান = কারনেল_মান.화면높이(); if (মান < 0) throw new অবস্হা_ব্যতিক্রম("프레임버퍼 없음"); return মান; }
    public static void 사각형(int 가로, int উল্লম্ব_পদ, int 폭, int 높이, int 색) {
        if (가로 < 0 || উল্লম্ব_পদ < 0 || 폭 < 0 || 높이 < 0 || 가로 > 너비() || উল্লম্ব_পদ > 높이() || 폭 > 너비() - 가로 || 높이 > 높이() - উল্লম্ব_পদ) throw new অবৈধ_যুক্তি_ব্যতিক্রম("화면 ক্লিপ");
        if (কারনেল_মান.사각형(가로, উল্লম্ব_পদ, 폭, 높이, 색) < 0) throw new অবস্হা_ব্যতিক্রম("프레임버퍼 없음");
    }
    public static void মুছুন_ভুক্তি(int 색) { 사각형(0, 0, 너비(), 높이(), 색); }
    public static void 기다리기() { if (কারনেল_মান.그림대기() < 0) throw new অবস্হা_ব্যতিক্রম("মিথস্ক্রিয় 입력 필요"); }
}
