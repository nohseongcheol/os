// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Алатки 전용 SVC Врзи_се. 기존 x86 Алатки 원문을 함께 빌드한다. */
public final class корисник {
    public static native int 파일서술자열기(int[] Име, int Подесувања);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Име, int[] податоци);
    public static native int запиши_датотека(int[] Име, int[] податоци, int должина_VALUE);
    public static native int Запиши(String Текст);
    public static native int запиши_знак_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Аргументи(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Дејство, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Текст, int должина_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_контрола(int Дејство, int 서술자, int VALUE);
    public static native int ПОВРЗИ_Stream(int 서술자, int адреса, int порта_VALUE);
    public static native int отвори_Мрежа(int порта_VALUE);
    public static native int испрати_Мрежа(int 서술자, int адреса, int порта_VALUE, int[] податоци, int должина_VALUE);
    public static native int 통신받기(int 서술자, int[] податоци, int должина_VALUE);
    public static native int Мрежа_порта(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int вертикала_позиционирање, int 폭, int 높이, int 색);
}
