// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ব্যবহারকারী ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ব্যবহারকারী {
    public static native int 파일서술자열기(int[] ফাইল_ভুক্তি_নাম, int খোলা_সেটিংস);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int বাইট_মান);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] নাম, int[] ডাটা);
    public static native int লেখা_অক্ষর_মান(int 문자);
    public static native int লেখা_ফাইল(int[] নাম, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int লেখা(String সামগ্রি_মান);
    public static native int 인수개수();
    public static native String আর্গুমেন্ট_তালিকা(int সূচি);
    public static native int 실행권한();
    public static native int খোলা_নেটওয়ার্ক(int স্থানীয়_পোর্ট);
    public static native int পাঠান_ডাটা(int হাতল_মান, int ইমেইল, int গন্তব্য_পোর্ট, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int 자료받기(int হাতল_মান, int[] ডাটা, int 제한밀리초);
    public static native int বন্ধ_নেটওয়ার্ক(int হাতল_মান);
    public static native int 내주소();
    public static native int 보낸주소(int হাতল_মান);
    public static native int 보낸창구(int হাতল_মান);
}
