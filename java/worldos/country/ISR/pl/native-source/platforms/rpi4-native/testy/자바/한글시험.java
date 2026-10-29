// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.własny.문자;
import polski.własny.nazwa_pliku;
import polski.własny.wpis_Lista;
import polski.własny.słownik;
import polski.własny.pozycja_wyjścia;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        pozycja_wyjścia.zapis_linia(문자.odszyfrować_dane(문자.kodować(인사))); pozycja_wyjścia.zapis_identyfikator(문자.kod_znaku_ILE_LICZB("한글😀"));
        nazwa_pliku.Zapis("한글자료.txt", 인사); pozycja_wyjścia.zapis_linia(nazwa_pliku.Odczyt("한글자료.txt"));
        wpis_Lista 이름들 = new wpis_Lista(); 이름들.더하기("가람"); 이름들.더하기("누리"); pozycja_wyjścia.zapis_linia(이름들.Odczyt(1));
        słownik 뜻 = new słownik(); 뜻.넣기("가람", "강"); System.gc(); pozycja_wyjścia.zapis_linia(뜻.ZNAJDŹ_wpis("가람"));
        try { 문자.odszyfrować_dane(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { pozycja_wyjścia.zapis_linia("UTF-8 błąd odrzucić_WARTOŚĆ"); }
        pozycja_wyjścia.zapis_linia("polski biblioteka 완료");
    }
}
