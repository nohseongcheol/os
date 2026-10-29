// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Tööriistad 전용 SVC Ühendu. 기존 x86 Tööriistad 원문을 함께 빌드한다. */
public final class kasutaja {
    public static native int 파일서술자열기(int[] Nimi_2, int Seaded);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nimi_2, int[] andmed);
    public static native int kirjutamine_Fail(int[] Nimi_2, int[] andmed, int 길이);
    public static native int Kirjutamine(String Tekst);
    public static native int kirjutamine_märk_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Argumendid(int INDEX);
    public static native int tööriist_number();
    public static native int 화면연결(int Nimi, int INDEX, int 가, int SECOND_operand, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Tekst, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int voog_meede(int Nimi, int 서술자, int VALUE);
    public static native int Ühenda_voog(int 서술자, int ADDRESS, int port_VALUE);
    public static native int avama_võrk(int port_VALUE);
    public static native int saatma_võrk(int 서술자, int ADDRESS, int port_VALUE, int[] andmed, int 길이);
    public static native int saama_võrk(int 서술자, int[] andmed, int 길이);
    public static native int võrk_port(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int ristkülik(int 가로, int vertikaal_ametikoht, int 폭, int 높이, int 색);
}
