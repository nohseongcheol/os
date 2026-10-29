// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros فضاء_المستخدم ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class فضاء_المستخدم {
    public static native int 파일서술자열기(int[] ملف_إدخال_اسم, int فتح_إعدادات);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بايت_قيمة);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int تثبيت_تخزين_الملفات(int 파일서술자);
    public static native int يقرأ_ملف(int[] اسم, int[] بيانات);
    public static native int كتابة_حرف_قيمة(int 문자);
    public static native int كتابة_ملف(int[] اسم, int[] بيانات, int 길이);
    public static native int كتابة(String محتوى_قيمة);
    public static native int 인수개수();
    public static native String وسائط(int فهرس);
    public static native int 실행권한();
    public static native int فتح_شبكة(int محلي_منفذ);
    public static native int يرسل_بيانات(int مؤشر_قيمة, int عنوان, int وجهة_منفذ, int[] بيانات, int 길이);
    public static native int يستلم_بيانات(int مؤشر_قيمة, int[] بيانات, int 제한밀리초);
    public static native int يغلق_شبكة(int مؤشر_قيمة);
    public static native int 내주소();
    public static native int 보낸주소(int مؤشر_قيمة);
    public static native int 보낸창구(int مؤشر_قيمة);
}
