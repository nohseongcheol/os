// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros کاربر ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class کاربر {
    public static native int 파일서술자열기(int[] فایل_ورودی_نام, int ایجاد_تنظیمات);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int بایت_مقدار);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] نام, int[] داده_ها);
    public static native int نوشتن_نویسه_مقدار(int 문자);
    public static native int نوشتن_فایل(int[] نام, int[] داده_ها, int طول_مقدار);
    public static native int نوشتن(String محتوا_مقدار);
    public static native int 인수개수();
    public static native String نشانوندها(int فهرست);
    public static native int 실행권한();
    public static native int ایجاد_شبکه(int محلی_تبدیل);
    public static native int ارسال_داده_ها(int دستگیره_مقدار, int آدرس, int مقصد_تبدیل, int[] داده_ها, int طول_مقدار);
    public static native int 자료받기(int دستگیره_مقدار, int[] داده_ها, int 제한밀리초);
    public static native int بستن_شبکه(int دستگیره_مقدار);
    public static native int 내주소();
    public static native int 보낸주소(int دستگیره_مقدار);
    public static native int 보낸창구(int دستگیره_مقدار);
}
