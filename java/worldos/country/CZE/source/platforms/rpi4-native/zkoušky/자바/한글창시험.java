// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.Okno;
import čeština.vlastní.prvek_obrazovky;
import čeština.vlastní.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Okno 화면;
    Popisek 안내;
    textové_pole vstup_HODNOTA;
    public void Spustit() {
        검사.참인지(událost_fronta.사건처리중인가(), "čeština 화면 작업 큐");
        화면 = new Okno("čeština knihovna Okno", 400, 280);
        안내 = prvek_obrazovky.značka_HODNOTA("한글로 Java 코딩", 20, 20, 340, 30);
        vstup_HODNOTA = prvek_obrazovky.textové_pole("Název", 20, 65, 340, 30);
        화면.Přidat_prvek(안내);
        화면.Přidat_prvek(vstup_HODNOTA);
        화면.Přidat_prvek(prvek_obrazovky.tlačítko("인사하기", 20, 110, 180, 32, this));
        화면.zobrazit_okno();
        výstupní_pozice.zápis_čára("KOREAN SWING READY");
    }
    public void dostat_Akce(Akce_povinnost_zvěřejnit Události) {
        검사.참인지(událost_fronta.사건처리중인가(), "čeština Akce 되부름");
        검사.참인지(Události.INDEX() == 1001 && Události.zdroj_události() instanceof tlačítko, "čeština Události 객체와 origin_HODNOTA");
        검사.참인지(!((Object)Události.zdroj_události() instanceof javax.swing.JButton), "표준 단추와 독립된 formát_HODNOTA");
        검사.참인지(!((Object)Události instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formát_HODNOTA");
        안내.zápis_SMS("안녕하세요 " + vstup_HODNOTA.글읽기());
        výstupní_pozice.zápis_čára("KOREAN SWING CLICK " + vstup_HODNOTA.글읽기());
    }
    public static void main(String[] argumenty) {
        událost_fronta.나중에실행(new 한글창시험());
    }
}
