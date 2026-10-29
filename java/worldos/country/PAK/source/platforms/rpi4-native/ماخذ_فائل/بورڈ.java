// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 مشین 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class بورڈ {
    public static native int 표시화소읽기(int 가로, int عمودی_پوزیشن_ٹھیک_کریں);
    public static native void لکھیں_ڈسپلے_پکسل(int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 색);
    public static native int سایہ_کاری(int 종류, int عمل);
    public static native void اختتام_بعید_حکم(int حالت_قدر);
    public static native void بعید_انتظار(int حالت_قدر);
    public static native void 직렬쓰기(int قدر);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int پراسیسر_اجازت_سطح();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 색);
    public static native void معطل_کریں_پراسیسر();
    public static native int بنائیں_ٹاسک(int اشاریہ);
    public static native int ٹاسک_حالت(int اشاریہ);
    public static native void روکیں(int حالت_قدر);
    public static native int 씨플러스시험();
    public static native int چلائیں_صارف_ایپ(int اشاریہ);
    public static native int پڑتال_کریں_صارف_ایپ();
    public static native int 인수준비(int 개수);
    public static native int نفاذ_کریں_صارف_فائل();
    public static native int 리눅스파일실행();
    public static native int دلائل_بائٹ(int اشاریہ, int مقام, int قدر);
    public static native int حکم_کی_تشریح_کرنے_والا(int عمل);
    public static native int کنٹرول_صارف_ایپ(int عمل);
    public static native void 입출력전환(int عمل);
    public static native int فائل_منتقلی_خدمت(int عمل);
    public static native int نیٹ_ورک_حالت(int اندراج_قدر, int اشاریہ);
    public static native int نیٹ_ورک_سیٹنگز(int عمل, int پتہ, int ماسک_پہنائیں_قدر, int گیٹ_وے_قدر);
    public static native int 응답보내기(int پتہ, int ترتیم_قدر);
    public static native int 응답읽기(int اندراج_قدر);
    public static native int طلب_نظام(int اندراج_قدر, int اشاریہ);
    public static native void 전원끄기();
}
