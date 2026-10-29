// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 সঁজুলিসমূহ 전용 SVC সংযোগ_স্থাপনা. 기존 x86 সঁজুলিসমূহ 원문을 함께 빌드한다. */
public final class ব্যৱহাৰকৰ্তা {
    public static native int 파일서술자열기(int[] নাম, int বৈশিষ্ট্য);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int মান);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] নাম, int[] ডাটা);
    public static native int লিখক_ফাইল(int[] নাম, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int লিখা(String টেক্সট);
    public static native int লিখক_বৰ্ণ_মান(int মান);
    public static native int 인수개수();
    public static native String 인수(int ইনডেক্স);
    public static native int 도구번호();
    public static native int 화면연결(int কাৰ্য্য, int ইনডেক্স, int 가, int 나, int 다, int 라);
    public static native int 화면글(int ইনডেক্স, int[] টেক্সট, int দৈর্ঘ্য_মান);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ষ্ট্ৰিম_নিয়ন্ত্রণ(int কাৰ্য্য, int 서술자, int মান);
    public static native int সংযোগ_ষ্ট্ৰিম(int 서술자, int ঠিকনা, int পৰ্ট_মান);
    public static native int খোলক_নেটৱৰ্ক(int পৰ্ট_মান);
    public static native int ই_মেইল_কৰক_নেটৱৰ্ক(int 서술자, int ঠিকনা, int পৰ্ট_মান, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int 통신받기(int 서술자, int[] ডাটা, int দৈর্ঘ্য_মান);
    public static native int নেটৱৰ্ক_পৰ্ট(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int উলম্ব_স্থান_সলনি_কৰক, int 폭, int 높이, int 색);
}
