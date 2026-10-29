// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 دستگاه 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class تخته_ای {
    public static native int 표시화소읽기(int 가로, int عمودی_مرتب_کردن);
    public static native void نوشتن_صفحه_نمایش_پیکسل(int 가로, int عمودی_مرتب_کردن, int 색);
    public static native int کنترل_از_راه_دور(int 종류, int کنش);
    public static native void پایان_دادن_راه_دور_فرمان(int وضعیت_مقدار);
    public static native void راه_دور_منتظر_ماندن(int وضعیت_مقدار);
    public static native void 직렬쓰기(int مقدار);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int پردازشگر_مجوز_سطح();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int عمودی_مرتب_کردن, int 색);
    public static native void تعلیق_پردازشگر();
    public static native int ایجاد_کار(int فهرست);
    public static native int کار_وضعیت(int فهرست);
    public static native void توقف(int وضعیت_مقدار);
    public static native int 씨플러스시험();
    public static native int اجرا_کاربر_برنامه(int فهرست);
    public static native int بررسی_کاربر_برنامه();
    public static native int 인수준비(int 개수);
    public static native int اجرا_کاربر_فایل();
    public static native int 리눅스파일실행();
    public static native int آرگومان_بایت(int فهرست, int مرتب_کردن, int مقدار);
    public static native int پایانه(int کنش);
    public static native int کنترل_کاربر_برنامه(int کنش);
    public static native void 입출력전환(int کنش);
    public static native int فایل_انتقال_خدمت(int کنش);
    public static native int شبکه_وضعیت(int ورودی_مقدار, int فهرست);
    public static native int شبکه_تنظیمات(int کنش, int آدرس, int ماسک_مقدار, int دروازه_مقدار);
    public static native int 응답보내기(int آدرس, int ترتیب_مقدار);
    public static native int 응답읽기(int ورودی_مقدار);
    public static native int جستار_سیستم(int ورودی_مقدار, int فهرست);
    public static native void 전원끄기();
}
