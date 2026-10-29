// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jkoros przestrzeń_użytkownika ELF 전용 API. Linux/JVM용 JNI 또는 java.net API가 아니다. */
public final class przestrzeń_użytkownika {
    public static native int otwarty_Plik_deskryptor(int[] Plik_wpis_nazwa, int otwarty_Ustawienia);
    public static native int 파일한바이트읽기(int Plik_deskryptor);
    public static native int 파일한바이트쓰기(int Plik_deskryptor, int bajt_WARTOŚĆ);
    public static native int Zamknij_Plik_deskryptor(int Plik_deskryptor);
    public static native int przekazywać_Files(int Plik_deskryptor);
    public static native int 파일읽기(int[] Nazwa, int[] dane);
    public static native int zapis_znak_WARTOŚĆ(int 문자);
    public static native int zapis_Plik(int[] Nazwa, int[] dane, int długość_WARTOŚĆ);
    public static native int Zapis(String treść_WARTOŚĆ_cb0f2404);
    public static native int 인수개수();
    public static native String argumenty(int INDEKS);
    public static native int wykonanie_pozwolenie();
    public static native int otwarty_sieć(int lokalny_port);
    public static native int wysłać_dane(int uchwyt_WARTOŚĆ, int Adres, int cel_port, int[] dane, int długość_WARTOŚĆ);
    public static native int odbierać_dane(int uchwyt_WARTOŚĆ, int[] dane, int 제한밀리초);
    public static native int Zamknij_sieć(int uchwyt_WARTOŚĆ);
    public static native int 내주소();
    public static native int 보낸주소(int uchwyt_WARTOŚĆ);
    public static native int 보낸창구(int uchwyt_WARTOŚĆ);
}
