// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.savas.Langas;
import Lietuvių.savas.valdiklis;
import Lietuvių.savas.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Langas 화면;
    Pavadinimas 안내;
    teksto_laukas 입력;
    public void Vykdyti() {
        검사.참인지(įvykis_eilė.사건처리중인가(), "Lietuvių 화면 작업 큐");
        화면 = new Langas("Lietuvių biblioteka Langas", 400, 280);
        안내 = valdiklis.žyma_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = valdiklis.teksto_laukas("Pavadinimas_2", 20, 65, 340, 30);
        화면.Įtraukti_elementas(안내);
        화면.Įtraukti_elementas(입력);
        화면.Įtraukti_elementas(valdiklis.mygtukas("인사하기", 20, 110, 180, 32, this));
        화면.laida_langas();
        Išvestis.rašymas_eilutė("KOREAN SWING READY");
    }
    public void gauti_gavinys(gavinys_pranešimas Įvykis) {
        검사.참인지(įvykis_eilė.사건처리중인가(), "Lietuvių Veiksmas 되부름");
        검사.참인지(Įvykis.INDEX() == 1001 && Įvykis.įvykio_šaltinis() instanceof mygtukas, "Lietuvių Įvykis 객체와 출처");
        검사.참인지(!((Object)Įvykis.įvykio_šaltinis() instanceof javax.swing.JButton), "표준 단추와 독립된 formatas_VALUE");
        검사.참인지(!((Object)Įvykis instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formatas_VALUE");
        안내.rašymas_SMS("안녕하세요 " + 입력.글읽기());
        Išvestis.rašymas_eilutė("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumentai) {
        įvykis_eilė.나중에실행(new 한글창시험());
    }
}
