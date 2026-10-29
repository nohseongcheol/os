// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.Prozor;
import hrvatski.vlastiti.widget;
import hrvatski.vlastiti.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Prozor 화면;
    Natpis 안내;
    tekstno_polje 입력;
    public void Izvrši() {
        검사.참인지(događaj_red_čekanja.사건처리중인가(), "hrvatski 화면 작업 큐");
        화면 = new Prozor("hrvatski biblioteka Prozor", 400, 280);
        안내 = widget.oznaka_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.tekstno_polje("Ime", 20, 65, 340, 30);
        화면.Dodaj_element(안내);
        화면.Dodaj_element(입력);
        화면.Dodaj_element(widget.gumb("인사하기", 20, 110, 180, 32, this));
        화면.emisija_prozor();
        Izlaz.zapisivanje_red("KOREAN SWING READY");
    }
    public void primiti_akcija(akcija_obavijest Događaj) {
        검사.참인지(događaj_red_čekanja.사건처리중인가(), "hrvatski Aktivnost 되부름");
        검사.참인지(Događaj.INDEX() == 1001 && Događaj.izvor_događaja() instanceof gumb, "hrvatski Događaj 객체와 출처");
        검사.참인지(!((Object)Događaj.izvor_događaja() instanceof javax.swing.JButton), "표준 단추와 독립된 oblik_VALUE");
        검사.참인지(!((Object)Događaj instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 oblik_VALUE");
        안내.zapisivanje_SMS("안녕하세요 " + 입력.글읽기());
        Izlaz.zapisivanje_red("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumenti) {
        događaj_red_čekanja.나중에실행(new 한글창시험());
    }
}
