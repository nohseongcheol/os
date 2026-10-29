// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.własny.Okno;
import polski.własny.element_ekranu;
import polski.własny.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Okno 화면;
    Etykieta plik_README_eb81d7d9;
    pole_tekstowe wejście_WARTOŚĆ;
    public void Uruchom() {
        검사.참인지(konkurs_kolejka.사건처리중인가(), "polski 화면 작업 큐");
        화면 = new Okno("polski biblioteka Okno", 400, 280);
        plik_README_eb81d7d9 = element_ekranu.tag_WARTOŚĆ("한글로 Java 코딩", 20, 20, 340, 30);
        wejście_WARTOŚĆ = element_ekranu.pole_tekstowe("Nazwa", 20, 65, 340, 30);
        화면.Dodaj_element(plik_README_eb81d7d9);
        화면.Dodaj_element(wejście_WARTOŚĆ);
        화면.Dodaj_element(element_ekranu.przycisk("인사하기", 20, 110, 180, 32, this));
        화면.program_okno();
        pozycja_wyjścia.zapis_linia("KOREAN SWING READY");
    }
    public void odbierać_akcja(akcja_powiadomienie Wydarzenie) {
        검사.참인지(konkurs_kolejka.사건처리중인가(), "polski Akcja 되부름");
        검사.참인지(Wydarzenie.INDEKS() == 1001 && Wydarzenie.źródło_zdarzenia() instanceof przycisk, "polski Wydarzenie 객체와 źródło_WARTOŚĆ");
        검사.참인지(!((Object)Wydarzenie.źródło_zdarzenia() instanceof javax.swing.JButton), "표준 단추와 독립된 format_WARTOŚĆ");
        검사.참인지(!((Object)Wydarzenie instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_WARTOŚĆ");
        plik_README_eb81d7d9.zapis_SMS("안녕하세요 " + wejście_WARTOŚĆ.글읽기());
        pozycja_wyjścia.zapis_linia("KOREAN SWING CLICK " + wejście_WARTOŚĆ.글읽기());
    }
    public static void main(String[] argumenty) {
        konkurs_kolejka.나중에실행(new 한글창시험());
    }
}
