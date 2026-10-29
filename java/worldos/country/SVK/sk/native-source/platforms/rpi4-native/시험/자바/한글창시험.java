// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.Okno;
import Slovenský.vlastné.widget;
import Slovenský.vlastné.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Okno 화면;
    Nápis 안내;
    textové_pole vstup_VALUE;
    public void Spustiť() {
        검사.참인지(udalosť_front.사건처리중인가(), "Slovenský 화면 작업 큐");
        화면 = new Okno("Slovenský knižnica Okno", 400, 280);
        안내 = widget.značka_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        vstup_VALUE = widget.textové_pole("Názov", 20, 65, 340, 30);
        화면.Pridať_prvok(안내);
        화면.Pridať_prvok(vstup_VALUE);
        화면.Pridať_prvok(widget.Tlačidlo("인사하기", 20, 110, 180, 32, this));
        화면.zobraziť_okno();
        Výstup.zapísať_linka("KOREAN SWING READY");
    }
    public void dostať_Akcia(Akcia_upozornenie Udalosť) {
        검사.참인지(udalosť_front.사건처리중인가(), "Slovenský Akcia 되부름");
        검사.참인지(Udalosť.INDEX() == 1001 && Udalosť.zdroj_udalosti() instanceof Tlačidlo, "Slovenský Udalosť 객체와 출처");
        검사.참인지(!((Object)Udalosť.zdroj_udalosti() instanceof javax.swing.JButton), "표준 단추와 독립된 formát_VALUE");
        검사.참인지(!((Object)Udalosť instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formát_VALUE");
        안내.zapísať_SMS("안녕하세요 " + vstup_VALUE.글읽기());
        Výstup.zapísať_linka("KOREAN SWING CLICK " + vstup_VALUE.글읽기());
    }
    public static void main(String[] Argumenty) {
        udalosť_front.나중에실행(new 한글창시험());
    }
}
