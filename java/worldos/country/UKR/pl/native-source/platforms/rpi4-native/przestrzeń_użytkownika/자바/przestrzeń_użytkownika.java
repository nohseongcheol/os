// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0 자바 narzędzia 전용 SVC Połącz. 기존 x86 narzędzia 원문을 함께 빌드한다. */
public final class przestrzeń_użytkownika {
    public static native int otwarty_Plik_deskryptor(int[] Nazwa, int Ustawienia);
    public static native int 파일한바이트읽기(int deskryptor_wpis);
    public static native int 파일한바이트쓰기(int deskryptor_wpis, int WARTOŚĆ);
    public static native int Zamknij_Plik_deskryptor(int deskryptor_wpis);
    public static native int 파일읽기(int[] Nazwa, int[] dane);
    public static native int zapis_Plik(int[] Nazwa, int[] dane, int długość_WARTOŚĆ);
    public static native int Zapis(String tekst);
    public static native int zapis_znak_WARTOŚĆ(int WARTOŚĆ);
    public static native int 인수개수();
    public static native String argumenty(int INDEKS);
    public static native int narzędzie_identyfikator();
    public static native int 화면연결(int Akcja, int INDEKS, int 가, int SEKUNDA_operand, int 다, int 라);
    public static native int 화면글(int INDEKS, int[] tekst, int długość_WARTOŚĆ);
    public static native int 화면너비();
    public static native int 화면높이();
    public static native int Stream_kontrola(int Akcja, int deskryptor_wpis, int WARTOŚĆ);
    public static native int POŁĄCZ_Stream(int deskryptor_wpis, int Adres, int port_WARTOŚĆ);
    public static native int otwarty_sieć(int port_WARTOŚĆ);
    public static native int wysłać_sieć(int deskryptor_wpis, int Adres, int port_WARTOŚĆ, int[] dane, int długość_WARTOŚĆ);
    public static native int odbierać_sieć(int deskryptor_wpis, int[] dane, int długość_WARTOŚĆ);
    public static native int sieć_port(int deskryptor_wpis);
    public static native int 밀리초();
    public static native int 그림대기();
    public static native int prostokąt(int 가로, int gałąź_stanowisko, int 폭, int wysokość_WARTOŚĆ, int 색);
}
