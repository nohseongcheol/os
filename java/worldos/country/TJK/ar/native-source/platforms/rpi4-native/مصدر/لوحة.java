// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 جهاز 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class لوحة {
    public static native int قراءةبكسلالعرض(int 가로, int عمودي_منصب);
    public static native void كتابةبكسلالعرض(int 가로, int عمودي_منصب, int 색);
    public static native int تحكم_عن_بعد(int 종류, int إجراء);
    public static native void إنهاء_مكالمة_بعيد_أمر(int حالة_قيمة);
    public static native void بعيد_انتظر(int حالة_قيمة);
    public static native void 직렬쓰기(int قيمة);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int معالج_إذن_مستوى();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int عمودي_منصب, int 색);
    public static native void العائد_معالج();
    public static native int فتح_مهمة(int فهرس);
    public static native int مهمة_حالة(int فهرس);
    public static native void إيقاف(int حالة_قيمة);
    public static native int 씨플러스시험();
    public static native int يشغّل_مستخدم_تطبيق(int فهرس);
    public static native int شيك_مستخدم_تطبيق();
    public static native int 인수준비(int 개수);
    public static native int ينفذ_مستخدم_ملف();
    public static native int 리눅스파일실행();
    public static native int وسيطة_بايت(int فهرس, int موضع, int قيمة);
    public static native int طرفية(int إجراء);
    public static native int تحكم_مستخدم_تطبيق(int إجراء);
    public static native void 입출력전환(int إجراء);
    public static native int نقل_الملفات_خدمة(int إجراء);
    public static native int شبكة_توفر(int إدخال_قيمة_962f286b, int فهرس);
    public static native int شبكة_إعدادات(int إجراء, int عنوان, int قناع_قيمة, int بوابة_قيمة);
    public static native int يرسل_رد(int عنوان, int أمر_قيمة);
    public static native int يقرأ_رد(int إدخال_قيمة_962f286b);
    public static native int يستعلم_نظام(int إدخال_قيمة_962f286b, int فهرس);
    public static native void 전원끄기();
}
