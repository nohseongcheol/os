// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Alatke 전용 SVC veze. 기존 x86 Alatke 원문을 함께 빌드한다. */
public final class korisnik {
    public static native int 파일서술자열기(int[] ime, int Postavke);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] ime, int[] podaci);
    public static native int 파일쓰기(int[] ime, int[] podaci, int 길이);
    public static native int 쓰기(String SMS);
    public static native int 문자쓰기(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int radnja, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] SMS, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int tok_kontrola(int radnja, int 서술자, int VALUE);
    public static native int veze_tok(int 서술자, int adresa, int port_VALUE);
    public static native int otvoren_Mreža(int port_VALUE);
    public static native int poslati_Mreža(int 서술자, int adresa, int port_VALUE, int[] podaci, int 길이);
    public static native int primiti_Mreža(int 서술자, int[] podaci, int 길이);
    public static native int Mreža_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int vertikala_pozicija, int 폭, int 높이, int 색);
}
