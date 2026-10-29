// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public class 한글소스 {
    public static void main(String[] argumenty) throws polski.własny.We_Wy_wyjątek {
        polski.własny.pozycja_wyjścia.zapis_linia("własny 컴파일러와 polski biblioteka");
        int znak_ILE_LICZB = polski.własny.문자.kod_znaku_ILE_LICZB("한글😀");
        polski.własny.pozycja_wyjścia.zapis_identyfikator(znak_ILE_LICZB);
        polski.własny.nazwa_pliku.Zapis("한글자료.txt", "własny jądro_WARTOŚĆ 안에서 저장한 한글😀");
        polski.własny.pozycja_wyjścia.zapis_linia(polski.własny.nazwa_pliku.Odczyt("한글자료.txt"));
    }
}
