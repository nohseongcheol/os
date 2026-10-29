// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 মেশিন 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class বোর্ড {
    public static native int 표시화소읽기(int 가로, int উল্লম্ব_পদ);
    public static native void লেখা_ডিসপ্লে_পেল্(int 가로, int উল্লম্ব_পদ, int 색);
    public static native int শ্যাডো_করা(int 종류, int কাজ);
    public static native void শেষ_করা_দূরবর্তী_আদেশ(int অবস্হা_মান);
    public static native void দূরবর্তী_অপেক্ষা(int অবস্হা_মান);
    public static native void 직렬쓰기(int মান);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int প্রসেসর_অনুমতি_স্তর();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int উল্লম্ব_পদ, int 색);
    public static native void স্থগিত_করুন_প্রসেসর();
    public static native int ক্রিয়েট_কার্য(int সূচি);
    public static native int কার্য_অবস্হা(int সূচি);
    public static native void বন্ধ_করুন_2(int অবস্হা_মান);
    public static native int 씨플러스시험();
    public static native int রান_ব্যবহারকারী_অ্যাপ(int সূচি);
    public static native int চেক_ব্যবহারকারী_অ্যাপ();
    public static native int 인수준비(int 개수);
    public static native int কার্যকর_করুন_ব্যবহারকারী_ফাইল();
    public static native int 리눅스파일실행();
    public static native int যুক্তি_বাইট(int সূচি, int অবস্থান, int মান);
    public static native int আদেশ_ব্যাখ্যাকারী(int কাজ);
    public static native int নিয়ন্ত্রণ_ব্যবহারকারী_অ্যাপ(int কাজ);
    public static native void 입출력전환(int কাজ);
    public static native int ফাইল_স্থানান্তর_সেবা(int কাজ);
    public static native int নেটওয়ার্ক_অবস্থা(int ভুক্তি_মান, int সূচি);
    public static native int নেটওয়ার্ক_সেটিংস(int কাজ, int ইমেইল, int মাস্ক_মান, int গেটওয়ে_মান);
    public static native int 응답보내기(int ইমেইল, int ক্রম_মান);
    public static native int 응답읽기(int ভুক্তি_মান);
    public static native int জিজ্ঞাসা_সিস্টেম(int ভুক্তি_মান, int সূচি);
    public static native void 전원끄기();
}
