// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Nutsmiddels 전용 SVC Koppel. 기존 x86 Nutsmiddels 원문을 함께 빌드한다. */
public final class gebruiker {
    public static native int 파일서술자열기(int[] Naam, int Instellings);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int VALUE);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Naam, int[] data);
    public static native int skryf_lêer(int[] Naam, int[] data, int lengte_VALUE);
    public static native int Skryf(String Teks);
    public static native int skryf_karakter_VALUE(int VALUE);
    public static native int 인수개수();
    public static native String 인수(int INDEX);
    public static native int 도구번호();
    public static native int 화면연결(int Aksie, int INDEX, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDEX, int[] Teks, int lengte_VALUE);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_kontrole(int Aksie, int 서술자, int VALUE);
    public static native int KOPPEL_Stream(int 서술자, int adres, int ombou_VALUE);
    public static native int skep_Netwerk(int ombou_VALUE);
    public static native int e_pos_Netwerk(int 서술자, int adres, int ombou_VALUE, int[] data, int lengte_VALUE);
    public static native int 통신받기(int 서술자, int[] data, int lengte_VALUE);
    public static native int Netwerk_ombou(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Vertikaal_plaas, int 폭, int 높이, int 색);
}
