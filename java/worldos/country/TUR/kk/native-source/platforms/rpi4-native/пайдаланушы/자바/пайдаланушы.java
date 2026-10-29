// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Құралдар 전용 SVC Байланысу. 기존 x86 Құралдар 원문을 함께 빌드한다. */
public final class пайдаланушы {
    public static native int 파일서술자열기(int[] Аты, int Баптаулар);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int мән);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Аты, int[] деректер);
    public static native int жазу_файл(int[] Аты, int[] деректер, int ұзындық_мән);
    public static native int Жазу(String Мәтін);
    public static native int жазу_таңба_мән(int мән);
    public static native int 인수개수();
    public static native String Аргументтер(int индекс);
    public static native int 도구번호();
    public static native int 화면연결(int Әрекет, int индекс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int индекс, int[] Мәтін, int ұзындық_мән);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ағым_Басқару(int Әрекет, int 서술자, int мән);
    public static native int қосу_ағым(int 서술자, int мекенжай, int порт_мән);
    public static native int ашу_желі(int порт_мән);
    public static native int жіберу_желі(int 서술자, int мекенжай, int порт_мән, int[] деректер, int ұзындық_мән);
    public static native int 통신받기(int 서술자, int[] деректер, int ұзындық_мән);
    public static native int желі_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int тік_төртбұрыш(int 가로, int Тік_лауазым, int 폭, int 높이, int 색);
}
