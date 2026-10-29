// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Инструменти 전용 SVC Свързване. 기존 x86 Инструменти 원문을 함께 빌드한다. */
public final class потребител {
    public static native int 파일서술자열기(int[] Име, int Настройки);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int стойност);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Име, int[] данни);
    public static native int записване_Файл(int[] Име, int[] данни, int 길이);
    public static native int Писане(String Текст);
    public static native int записване_знак_стойност(int стойност);
    public static native int 인수개수();
    public static native String Параметри(int индекс);
    public static native int 도구번호();
    public static native int 화면연결(int Операция, int индекс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int индекс, int[] Текст, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int поток_контрол(int Операция, int 서술자, int стойност);
    public static native int връзка_поток(int 서술자, int адрес, int порт_стойност);
    public static native int отварям_мрежа(int порт_стойност);
    public static native int изпращам_мрежа(int 서술자, int адрес, int порт_стойност, int[] данни, int 길이);
    public static native int получавам_мрежа(int 서술자, int[] данни, int 길이);
    public static native int мрежа_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int правоъгълник(int 가로, int вертикал_позиция, int 폭, int 높이, int 색);
}
