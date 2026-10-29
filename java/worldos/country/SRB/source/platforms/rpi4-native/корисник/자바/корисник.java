// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Алатке 전용 SVC Повежи_се. 기존 x86 Алатке 원문을 함께 빌드한다. */
public final class корисник {
    public static native int 파일서술자열기(int[] Назив, int Поставке);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int вриједност);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Назив, int[] подаци);
    public static native int писати_фајл(int[] Назив, int[] подаци, int дужина_вриједност);
    public static native int Пише(String Текст);
    public static native int писати_знак_вриједност(int вриједност);
    public static native int 인수개수();
    public static native String Аргументи(int индекс);
    public static native int 도구번호();
    public static native int 화면연결(int радња, int индекс, int 가, int 나, int 다, int 라);
    public static native int 화면글(int индекс, int[] Текст, int дужина_вриједност);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int ток_контрола(int радња, int 서술자, int вриједност);
    public static native int ПОВЕЖИ_ток(int 서술자, int адреса, int порт_вриједност);
    public static native int креирати_Мрежа(int порт_вриједност);
    public static native int послати_Мрежа(int 서술자, int адреса, int порт_вриједност, int[] подаци, int дужина_вриједност);
    public static native int 통신받기(int 서술자, int[] подаци, int дужина_вриједност);
    public static native int Мрежа_порт(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int вертикала_позиција, int 폭, int 높이, int 색);
}
