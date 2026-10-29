// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 أدوات 전용 SVC اتصال. 기존 x86 أدوات 원문을 함께 빌드한다. */
public final class فضاء_المستخدم {
    public static native int 파일서술자열기(int[] اسم, int إعدادات);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int قيمة);
    public static native int 파일서술자닫기(int 서술자);
    public static native int يقرأ_ملف(int[] اسم, int[] بيانات);
    public static native int كتابة_ملف(int[] اسم, int[] بيانات, int 길이);
    public static native int كتابة(String نص);
    public static native int كتابة_حرف_قيمة(int قيمة);
    public static native int 인수개수();
    public static native String وسائط(int فهرس);
    public static native int أداة_رقم();
    public static native int 화면연결(int إجراء, int فهرس, int 가, int 나, int 다, int 라);
    public static native int 화면글(int فهرس, int[] نص, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int بث_تحكم(int إجراء, int 서술자, int قيمة);
    public static native int يتصل_بث(int 서술자, int عنوان, int منفذ_قيمة);
    public static native int فتح_شبكة(int منفذ_قيمة);
    public static native int يرسل_شبكة(int 서술자, int عنوان, int منفذ_قيمة, int[] بيانات, int 길이);
    public static native int يستلم_شبكة(int 서술자, int[] بيانات, int 길이);
    public static native int شبكة_منفذ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int مستطيل(int 가로, int عمودي_منصب, int 폭, int ارتفاع_قيمة, int 색);
}
