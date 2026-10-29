// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Rīki 전용 SVC Savienoties. 기존 x86 Rīki 원문을 함께 빌드한다. */
public final class lietotājs {
    public static native int 파일서술자열기(int[] Nosaukums, int Uzstādījumi);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Nosaukums, int[] dati);
    public static native int rakstīšana_Fails(int[] Nosaukums, int[] dati, int 길이);
    public static native int Rakstīt(String Teksts);
    public static native int rakstīšana_rakstzīme_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String Parametri(int INDEX);
    public static native int rīks_numurs();
    public static native int 화면연결(int Darbība, int INDEX, int 가, int SECOND_operands, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Teksts, int 길이);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_vadība(int Darbība, int 서술자, int VALUE);
    public static native int saziņa_Stream(int 서술자, int adrese, int ports_VALUE);
    public static native int atvērt_tīkls(int ports_VALUE);
    public static native int sūtīt_tīkls(int 서술자, int adrese, int ports_VALUE, int[] dati, int 길이);
    public static native int saņemt_tīkls(int 서술자, int[] dati, int 길이);
    public static native int tīkls_ports(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int taisnstūris(int 가로, int vertikāle_amats, int 폭, int 높이, int 색);
}
