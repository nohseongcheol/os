// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 مەکینه 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void ڕایت_کردن_نیشاندان_پێڵ(int 가로, int 세로, int 색);
    public static native int سێبەركردن(int 종류, int ئاکشن);
    public static native void دوایی_کردن_دوورەدەس_فەرمان(int دۆخ_نرخ);
    public static native void دوورەدەس_چاوەڕوان_کردن(int دۆخ_نرخ);
    public static native void 직렬쓰기(int نرخ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void هەڵپەساردن_CPU();
    public static native int دروستکردن_ئەرک(int پێرست);
    public static native int ئەرک_دۆخ(int پێرست);
    public static native void وەستان(int دۆخ_نرخ);
    public static native int 씨플러스시험();
    public static native int ڕادان_بەکارهێنەر_بەرنامە(int پێرست);
    public static native int پشکنین_بەکارهێنەر_بەرنامە();
    public static native int 인수준비(int 개수);
    public static native int جێبەجێکردن_بەکارهێنەر_فایل();
    public static native int 리눅스파일실행();
    public static native int ئارگیومێنت_بایت(int پێرست, int 위치, int نرخ);
    public static native int 터미널(int ئاکشن);
    public static native int کۆنترۆڵ_بەکارهێنەر_بەرنامە(int ئاکشن);
    public static native void 입출력전환(int ئاکشن);
    public static native int فایل_گواستنەوە_ڕاژه(int ئاکشن);
    public static native int تۆڕ_دۆخ(int تێنووسین_نرخ, int پێرست);
    public static native int تۆڕ_ڕێكبەندەكان(int ئاکشن, int ناونیشان, int 가림, int 관문);
    public static native int 응답보내기(int ناونیشان, int ئۆردەر_نرخ);
    public static native int 응답읽기(int تێنووسین_نرخ);
    public static native int پرس_سیستم(int تێنووسین_نرخ, int پێرست);
    public static native void 전원끄기();
}
