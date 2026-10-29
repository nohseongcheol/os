// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.Fereastră;
import Română.propriu.widget;
import Română.propriu.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Fereastră 화면;
    Etichetă 안내;
    câmp_text 입력;
    public void Execută() {
        검사.참인지(eveniment_coadă.사건처리중인가(), "Română 화면 작업 큐");
        화면 = new Fereastră("Română bibliotecă Fereastră", 400, 280);
        안내 = widget.eticheta_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.câmp_text("Nume", 20, 65, 340, 30);
        화면.adăuga_element(안내);
        화면.adăuga_element(입력);
        화면.adăuga_element(widget.buton("인사하기", 20, 110, 180, 32, this));
        화면.afișa_fereastră();
        Rezultat.scriere_linie("KOREAN SWING READY");
    }
    public void primi_Acțiune(Acțiune_înștiințare Eveniment) {
        검사.참인지(eveniment_coadă.사건처리중인가(), "Română Acțiuni 되부름");
        검사.참인지(Eveniment.INDEX() == 1001 && Eveniment.sursă_eveniment() instanceof buton, "Română Eveniment 객체와 출처");
        검사.참인지(!((Object)Eveniment.sursă_eveniment() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)Eveniment instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        안내.scriere_SMS("안녕하세요 " + 입력.글읽기());
        Rezultat.scriere_linie("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumente) {
        eveniment_coadă.나중에실행(new 한글창시험());
    }
}
