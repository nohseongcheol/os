// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.okno;
import slovenščina.lastno.pripomoček;
import slovenščina.lastno.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    okno 화면;
    Oznaka 안내;
    SMS_polje 입력;
    public void Izvedi() {
        검사.참인지(dogodek_čakalna_vrsta.사건처리중인가(), "slovenščina 화면 작업 큐");
        화면 = new okno("slovenščina knjižnica okno", 400, 280);
        안내 = pripomoček.oznaka_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = pripomoček.SMS_polje("Ime", 20, 65, 340, 30);
        화면.Dodaj_element(안내);
        화면.Dodaj_element(입력);
        화면.Dodaj_element(pripomoček.Gumb("인사하기", 20, 110, 180, 32, this));
        화면.oddaja_okno();
        Izpis.pisati_linija("KOREAN SWING READY");
    }
    public void sprejeti_sprejemati_prejeti_prejemati_akcija(akcija_obvestilo dogodek) {
        검사.참인지(dogodek_čakalna_vrsta.사건처리중인가(), "slovenščina Dejanje 되부름");
        검사.참인지(dogodek.INDEX() == 1001 && dogodek.vir_dogodka() instanceof Gumb, "slovenščina dogodek 객체와 출처");
        검사.참인지(!((Object)dogodek.vir_dogodka() instanceof javax.swing.JButton), "표준 단추와 독립된 oblika_VALUE");
        검사.참인지(!((Object)dogodek instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 oblika_VALUE");
        안내.pisati_SMS("안녕하세요 " + 입력.글읽기());
        Izpis.pisati_linija("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumenti) {
        dogodek_čakalna_vrsta.나중에실행(new 한글창시험());
    }
}
