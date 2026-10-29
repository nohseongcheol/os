// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 Tresnak 전용 SVC Konektatu. 기존 x86 Tresnak 원문을 함께 빌드한다. */
public final class erabiltzaile {
    public static native int 파일서술자열기(int[] Izena, int Ezarpenak);
    public static native int 파일한바이트읽기(int 서술자);
    public static native int 파일한바이트쓰기(int 서술자, int balio);
    public static native int 파일서술자닫기(int 서술자);
    public static native int 파일읽기(int[] Izena, int[] datuak);
    public static native int idatzi_fitxategi(int[] Izena, int[] datuak, int luzera_balio);
    public static native int Idatzi(String Testua);
    public static native int idatzi_karaktere_balio(int balio);
    public static native int 인수개수();
    public static native String Argumentuak(int INDIZE);
    public static native int 도구번호();
    public static native int 화면연결(int Ekintza, int INDIZE, int 가, int 나, int 다, int 라);
    public static native int 화면글(int INDIZE, int[] Testua, int luzera_balio);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_kontrol(int Ekintza, int 서술자, int balio);
    public static native int KONEKTATU_Stream(int 서술자, int helbide, int ataka_balio);
    public static native int ireki_sare(int ataka_balio);
    public static native int bidali_sare(int 서술자, int helbide, int ataka_balio, int[] datuak, int luzera_balio);
    public static native int 통신받기(int 서술자, int[] datuak, int luzera_balio);
    public static native int sare_ataka(int 서술자);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int 사각형(int 가로, int Bertikala_kargu, int 폭, int 높이, int 색);
}
