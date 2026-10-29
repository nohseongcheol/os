// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 ٹولز 전용 SVC متصل_ہوں. 기존 x86 ٹولز 원문을 함께 빌드한다. */
public final class صارف {
    public static native int 파일서술자열기(int[] نام, int ترتیبات);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int قدر);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] نام, int[] کوائف);
    public static native int لکھیں_فائل(int[] نام, int[] کوائف, int لمبا_ئی_قدر);
    public static native int لکھیں(String متن);
    public static native int لکھیں_کریکٹر_قدر(int قدر);
    public static native int 인수개수();
    public static native String دلائل(int اشاریہ);
    public static native int 도구번호();
    public static native int 화면연결(int عمل, int اشاریہ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int اشاریہ, int[] متن, int لمبا_ئی_قدر);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int بہاؤ_کنٹرول(int عمل, int 서술자, int قدر);
    public static native int جڑیں_بہاؤ(int 서술자, int پتہ, int پورٹ_قدر);
    public static native int بنائیں_نیٹ_ورک(int پورٹ_قدر);
    public static native int بھیجیں_نیٹ_ورک(int 서술자, int پتہ, int پورٹ_قدر, int[] کوائف, int لمبا_ئی_قدر);
    public static native int 통신받기(int 서술자, int[] کوائف, int لمبا_ئی_قدر);
    public static native int نیٹ_ورک_پورٹ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int عمودی_پوزیشن_ٹھیک_کریں, int 폭, int 높이, int 색);
}
