// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 빛 {
    public static void main(String[] argumenty) throws Exception {
        int SUMA_WARTOŚĆ = 0;
        int identyfikator = 1;
        while (identyfikator <= 10) {
            SUMA_WARTOŚĆ = SUMA_WARTOŚĆ + identyfikator;
            identyfikator = identyfikator + 1;
        }
        polski.własny.pozycja_wyjścia.zapis_identyfikator(SUMA_WARTOŚĆ);
        polski.własny.nazwa_pliku.Zapis("aot.txt", "한글 AOT nazwa_pliku 😀");
        polski.własny.pozycja_wyjścia.zapis_linia(polski.własny.nazwa_pliku.Odczyt("aot.txt"));
    }
}
