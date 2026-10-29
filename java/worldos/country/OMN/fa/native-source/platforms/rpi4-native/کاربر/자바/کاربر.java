// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ابزارها 전용 SVC اتصال. 기존 x86 ابزارها 원문을 함께 빌드한다. */
public final class کاربر {
    public static native int 파일서술자열기(int[] نام, int تنظیمات);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int مقدار);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] نام, int[] داده_ها);
    public static native int نوشتن_فایل(int[] نام, int[] داده_ها, int طول_مقدار);
    public static native int نوشتن(String متن);
    public static native int نوشتن_نویسه_مقدار(int مقدار);
    public static native int 인수개수();
    public static native String نشانوندها(int فهرست);
    public static native int 도구번호();
    public static native int 화면연결(int کنش, int فهرست, int 가, int 나, int 다, int 라);
    public static native int 화면글(int فهرست, int[] متن, int طول_مقدار);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int جریان_کنترل(int کنش, int 서술자, int مقدار);
    public static native int اتصال_جریان(int 서술자, int آدرس, int تبدیل_مقدار);
    public static native int ایجاد_شبکه(int تبدیل_مقدار);
    public static native int ارسال_شبکه(int 서술자, int آدرس, int تبدیل_مقدار, int[] داده_ها, int طول_مقدار);
    public static native int 통신받기(int 서술자, int[] داده_ها, int طول_مقدار);
    public static native int شبکه_تبدیل(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int عمودی_مرتب_کردن, int 폭, int 높이, int 색);
}
