// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Tools 전용 SVC Verbannen. 기존 x86 Tools 원문을 함께 빌드한다. */
public final class Benotzer {
    public static native int 파일서술자열기(int[] Numm, int Astellungen);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Numm, int[] Daten);
    public static native int schreiwen_Fichier(int[] Numm, int[] Daten, int Längt_VALUE);
    public static native int schreiwen(String SMS);
    public static native int schreiwen_Zeechen_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Aktioun, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int Längt_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_Kontroll(int Aktioun, int 서술자, int VALUE);
    public static native int Verbannen_Stream(int 서술자, int Adress, int Port_VALUE);
    public static native int ariichten_Reseau(int Port_VALUE);
    public static native int mailen_Reseau(int 서술자, int Adress, int Port_VALUE, int[] Daten, int Längt_VALUE);
    public static native int 통신받기(int 서술자, int[] Daten, int Längt_VALUE);
    public static native int Reseau_Port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertikal_positionéieren, int 폭, int 높이, int 색);
}
