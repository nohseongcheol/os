// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 সরঞ্জামগুলি 전용 SVC সংযোগ_স্থাপনা. 기존 x86 সরঞ্জামগুলি 원문을 함께 빌드한다. */
public final class ব্যবহারকারী {
    public static native int 파일서술자열기(int[] নাম, int সেটিংস);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int মান);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] নাম, int[] ডাটা);
    public static native int লেখা_ফাইল(int[] নাম, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int লেখা(String পাঠ);
    public static native int লেখা_অক্ষর_মান(int মান);
    public static native int 인수개수();
    public static native String আর্গুমেন্ট_তালিকা(int সূচি);
    public static native int 도구번호();
    public static native int 화면연결(int কাজ, int সূচি, int 가, int 나, int 다, int 라);
    public static native int 화면글(int সূচি, int[] পাঠ, int দৈর্ঘ্য_মান);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int প্রবাহ_নিয়ন্ত্রণ(int কাজ, int 서술자, int মান);
    public static native int সংযোগ_প্রবাহ(int 서술자, int ইমেইল, int পোর্ট_মান);
    public static native int খোলা_নেটওয়ার্ক(int পোর্ট_মান);
    public static native int পাঠান_নেটওয়ার্ক(int 서술자, int ইমেইল, int পোর্ট_মান, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int 통신받기(int 서술자, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int নেটওয়ার্ক_পোর্ট(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int উল্লম্ব_পদ, int 폭, int 높이, int 색);
}
