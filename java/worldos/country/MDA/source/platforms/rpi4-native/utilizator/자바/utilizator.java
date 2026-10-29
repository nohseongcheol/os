// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Instrumente 전용 SVC Conectează. 기존 x86 Instrumente 원문을 함께 빌드한다. */
public final class utilizator {
    public static native int 파일서술자열기(int[] Nume, int Setări);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nume, int[] date);
    public static native int scriere_Fișier(int[] Nume, int[] date, int lungime_VALUE);
    public static native int Scriere(String SMS);
    public static native int scriere_caracter_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumente(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Acțiuni, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int lungime_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int flux_control(int Acțiuni, int 서술자, int VALUE);
    public static native int conecta_flux(int 서술자, int adresa, int muta_VALUE);
    public static native int crea_rețea(int muta_VALUE);
    public static native int trimite_rețea(int 서술자, int adresa, int muta_VALUE, int[] date, int lungime_VALUE);
    public static native int primi_rețea(int 서술자, int[] date, int lungime_VALUE);
    public static native int rețea_muta(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int dreptunghi(int 가로, int Verticală_poziție, int 폭, int 높이, int 색);
}
