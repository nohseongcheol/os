// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 مشین 경계. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class 보드 {
    public static native int 표시화소읽기(int 가로, int 세로);
    public static native void لکھو_ڈسپلے_دانہ(int 가로, int 세로, int 색);
    public static native int سایہ_کای(int 종류, int کم);
    public static native void ختم_کرو_بعيد_حکم(int حالت_قدر);
    public static native void 원격대기(int حالت_قدر);
    public static native void 직렬쓰기(int قدر);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int 시피유권한();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int 세로, int 색);
    public static native void معطل_کیتا_گیا_عمل_کار();
    public static native int بنڑاؤ_ٹاسک(int اشاریہ);
    public static native int ٹاسک_حالت(int اشاریہ);
    public static native void روکو(int حالت_قدر);
    public static native int 씨플러스시험();
    public static native int چلاؤ_صارف_ایپ(int اشاریہ);
    public static native int پڑتال_صارف_ایپ();
    public static native int 인수준비(int 개수);
    public static native int نفاذ_کرو_صارف_فائل();
    public static native int 리눅스파일실행();
    public static native int دلیل_بائٹ(int اشاریہ, int 위치, int قدر);
    public static native int 터미널(int کم);
    public static native int کنٹرول_صارف_ایپ(int کم);
    public static native void 입출력전환(int کم);
    public static native int فائل_منتقلی_خدمت(int کم);
    public static native int نیٹ_ورک_حالت(int داخلہ_قدر, int اشاریہ);
    public static native int نیٹ_ورک_سیٹنگاں(int کم, int پتا, int 가림, int 관문);
    public static native int 응답보내기(int پتا, int ترتیب_قدر);
    public static native int 응답읽기(int داخلہ_قدر);
    public static native int طلب_نظام(int داخلہ_قدر, int اشاریہ);
    public static native void 전원끄기();
}
