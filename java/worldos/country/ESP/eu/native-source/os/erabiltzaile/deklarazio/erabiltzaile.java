// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros erabiltzaile ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class erabiltzaile {
    public static native int 파일서술자열기(int[] fitxategi_sarrera_izen, int ireki_Ezarpenak);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_balio);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int 파일저장확정(int 파일서술자);
    public static native int 파일읽기(int[] Izena, int[] datuak);
    public static native int idatzi_karaktere_balio(int 문자);
    public static native int idatzi_fitxategi(int[] Izena, int[] datuak, int luzera_balio);
    public static native int Idatzi(String eduki_balio);
    public static native int 인수개수();
    public static native String Argumentuak(int INDIZE);
    public static native int 실행권한();
    public static native int ireki_sare(int lokal_ataka);
    public static native int bidali_datuak(int helduleku_balio, int helbide, int helburu_ataka, int[] datuak, int luzera_balio);
    public static native int 자료받기(int helduleku_balio, int[] datuak, int 제한밀리초);
    public static native int itxi_sare(int helduleku_balio);
    public static native int 내주소();
    public static native int 보낸주소(int helduleku_balio);
    public static native int 보낸창구(int helduleku_balio);
}
