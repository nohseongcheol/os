// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros användarutrymme ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class användarutrymme {
    public static native int 파일서술자열기(int[] fil_post_namn, int skapa_Inställningar);
    public static native int 파일한바이트읽기(int 파일서술자);
    public static native int 파일한바이트쓰기(int 파일서술자, int byte_värde);
    public static native int 파일서술자닫기(int 파일서술자);
    public static native int incheckning_Files(int 파일서술자);
    public static native int läsa_fil(int[] Namn, int[] data);
    public static native int skriva_tecken_värde(int 문자);
    public static native int skriva_fil(int[] Namn, int[] data, int längd_värde);
    public static native int Skriv(String Innehåll_värde);
    public static native int 인수개수();
    public static native String argument(int INDEX);
    public static native int körning_behörighet();
    public static native int skapa_nätverk(int lokal_port);
    public static native int skicka_data(int handtag_värde, int Adress, int mål_port, int[] data, int längd_värde);
    public static native int få_data(int handtag_värde, int[] data, int 제한밀리초);
    public static native int Stäng_nätverk(int handtag_värde);
    public static native int 내주소();
    public static native int 보낸주소(int handtag_värde);
    public static native int 보낸창구(int handtag_värde);
}
