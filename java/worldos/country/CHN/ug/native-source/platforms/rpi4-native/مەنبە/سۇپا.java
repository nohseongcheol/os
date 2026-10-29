// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 ماشىنا 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class سۇپا {
    public static native int 표시화소읽기(int 가로, int تىك_ئورۇنلاشتۇرۇش);
    public static native void يازماق_كۆرسەتكۈچ_پىكسېل(int 가로, int تىك_ئورۇنلاشتۇرۇش, int 색);
    public static native int سايىلەش(int 종류, int مەشغۇلات);
    public static native void تاماملىماق_يىراق_بۇيرۇق(int ھالەت_قىممىتى);
    public static native void 원격대기(int ھالەت_قىممىتى);
    public static native void 직렬쓰기(int قىممىتى);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int تىك_ئورۇنلاشتۇرۇش, int 색);
    public static native void توڭلىتىش_بىر_تەرەپ_قىلغۇچ();
    public static native int قۇرۇش_ۋەزىپە(int ئىندېكس);
    public static native int ۋەزىپە_ھالەت(int ئىندېكس);
    public static native void توختا(int ھالەت_قىممىتى);
    public static native int 씨플러스시험();
    public static native int قوزغىتىش_ئىشلەتكۈچى_ئەپ(int ئىندېكس);
    public static native int تەكشۈرۈش_ئىشلەتكۈچى_ئەپ();
    public static native int 인수준비(int 개수);
    public static native int ئىجرا_قىلىش_ئىشلەتكۈچى_ھۆججەت();
    public static native int 리눅스파일실행();
    public static native int دەلىل_بايت(int ئىندېكس, int ئورۇن, int قىممىتى);
    public static native int تېرمىنال(int مەشغۇلات);
    public static native int كونترول_ئىشلەتكۈچى_ئەپ(int مەشغۇلات);
    public static native void 입출력전환(int مەشغۇلات);
    public static native int ھۆججەت_يوللاش_مۇلازىمەت(int مەشغۇلات);
    public static native int تور_بىكار(int كىرگۈزۈش_قىممىتى, int ئىندېكس);
    public static native int تور_تەڭشەك(int مەشغۇلات, int ئادرېس, int 가림, int 관문);
    public static native int 응답보내기(int ئادرېس, int تەرتىپ_قىممىتى);
    public static native int 응답읽기(int كىرگۈزۈش_قىممىتى);
    public static native int تەكشۈرۈش_سىستېما(int كىرگۈزۈش_قىممىتى, int ئىندېكس);
    public static native void 전원끄기();
}
