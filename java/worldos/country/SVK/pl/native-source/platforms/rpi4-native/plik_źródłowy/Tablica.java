// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 maszyna granica_WARTOŚĆ. 포인터를 Java int로 잘라 넘기지 않는다. */
public final class Tablica {
    public static native int 표시화소읽기(int 가로, int gałąź_stanowisko);
    public static native void zapis_wyświetlać_piksel(int 가로, int gałąź_stanowisko, int 색);
    public static native int obserwowanie(int Rodzaj_WARTOŚĆ, int Akcja);
    public static native void Koniec_zdalny_polecenie(int Stan_WARTOŚĆ);
    public static native void zdalny_chwileczkę(int Stan_WARTOŚĆ);
    public static native void 직렬쓰기(int WARTOŚĆ);
    public static native int 직렬읽기();
    public static native int 밀리초();
    public static native int CPU_uprawnienie_poziom();
    public static native int 화면준비();
    public static native int 화면너비();
    public static native int 화면높이();
    public static native void 화면점(int 가로, int gałąź_stanowisko, int 색);
    public static native void Dochód_CPU();
    public static native int Twórca_zadanie(int INDEKS);
    public static native int zadanie_Stan(int INDEKS);
    public static native void Zatrzymaj(int Stan_WARTOŚĆ);
    public static native int 씨플러스시험();
    public static native int przebieg_użytkownik_program(int INDEKS);
    public static native int czek_użytkownik_program();
    public static native int 인수준비(int towar_ILE_LICZB);
    public static native int Wykonaj_użytkownik_Plik();
    public static native int 리눅스파일실행();
    public static native int argument_bajt(int INDEKS, int pozycja, int WARTOŚĆ);
    public static native int interpretator_poleceń(int Akcja);
    public static native int kontrola_użytkownik_program(int Akcja);
    public static native void 입출력전환(int Akcja);
    public static native int transfer_plików_usługa(int Akcja);
    public static native int sieć_stan(int wpis_WARTOŚĆ, int INDEKS);
    public static native int sieć_Ustawienia(int Akcja, int Adres, int maska_WARTOŚĆ, int brama_WARTOŚĆ);
    public static native int wysłać_odpowiedź(int Adres, int zamówić_WARTOŚĆ);
    public static native int 응답읽기(int wpis_WARTOŚĆ);
    public static native int zapytanie_System(int wpis_WARTOŚĆ, int INDEKS);
    public static native void 전원끄기();
}
