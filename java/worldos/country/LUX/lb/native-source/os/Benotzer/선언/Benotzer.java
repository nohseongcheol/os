// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros Benotzer ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class Benotzer {
    public static native int 파일서술자열기(int[] Fichier_Agab_Numm, int ariichten_Astellungen);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int Byte_VALUE);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Numm, int[] Daten);
    public static native int schreiwen_Zeechen_VALUE(int 문자);
    public static native int schreiwen_Fichier(int[] Numm, int[] Daten, int Längt_VALUE);
    public static native int schreiwen(String Inhalt_VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 실행권한();
    public static native int ariichten_Reseau(int lokal_Port);
    public static native int mailen_Daten(int Handle_VALUE, int Adress, int Zil_Port, int[] Daten, int Längt_VALUE);
    public static native int 자료받기(int Handle_VALUE, int[] Daten, int 제한밀리초);
    public static native int Clôture_Reseau(int Handle_VALUE);
    public static native int 내주소();
    public static native int 보낸주소(int Handle_VALUE);
    public static native int 보낸창구(int Handle_VALUE);
}
