// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros ব্যৱহাৰকৰ্তা ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class ব্যৱহাৰকৰ্তা {
    public static native int 파일서술자열기(int[] ফাইল_প্রবিষ্ট_নাম, int খোলক_ছেটিংছ);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int বাইট_মান);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] নাম, int[] ডাটা);
    public static native int লিখক_বৰ্ণ_মান(int 문자);
    public static native int লিখক_ফাইল(int[] নাম, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int লিখা(String সামগ্ৰী_মান);
    public static native int 인수개수();
    public static native String 인수(int ইনডেক্স);
    public static native int 실행권한();
    public static native int খোলক_নেটৱৰ্ক(int স্থানীয়_পৰ্ট);
    public static native int ই_মেইল_কৰক_ডাটা(int হেণ্ডেল_মান, int ঠিকনা, int গন্তব্য_স্থান_পৰ্ট, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int 자료받기(int হেণ্ডেল_মান, int[] ডাটা, int 제한밀리초);
    public static native int বন্ধ_কৰক_নেটৱৰ্ক(int হেণ্ডেল_মান);
    public static native int 내주소();
    public static native int 보낸주소(int হেণ্ডেল_মান);
    public static native int 보낸창구(int হেণ্ডেল_মান);
}
