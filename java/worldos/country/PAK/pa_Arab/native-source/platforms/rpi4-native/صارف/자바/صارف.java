// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 اوزار 전용 SVC جڑو. 기존 x86 اوزار 원문을 함께 빌드한다. */
public final class صارف {
    public static native int 파일서술자열기(int[] ناں, int سیٹنگاں);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int قدر);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ناں, int[] کوائف);
    public static native int لکھو_فائل(int[] ناں, int[] کوائف, int لمبائی_قدر);
    public static native int لکھو(String متن);
    public static native int لکھو_کریکٹر_قدر(int قدر);
    public static native int 인수개수();
    public static native String 인수(int اشاریہ);
    public static native int 도구번호();
    public static native int 화면연결(int کم, int اشاریہ, int 가, int 나, int 다, int 라);
    public static native int 화면글(int اشاریہ, int[] متن, int لمبائی_قدر);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int سٹریم_کنٹرول(int کم, int 서술자, int قدر);
    public static native int جڑو_سٹریم(int 서술자, int پتا, int دہانہ_قدر);
    public static native int بنڑاؤ_نیٹ_ورک(int دہانہ_قدر);
    public static native int بھیجو_نیٹ_ورک(int 서술자, int پتا, int دہانہ_قدر, int[] کوائف, int لمبائی_قدر);
    public static native int 통신받기(int 서술자, int[] کوائف, int لمبائی_قدر);
    public static native int نیٹ_ورک_دہانہ(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int 세로, int 폭, int 높이, int 색);
}
