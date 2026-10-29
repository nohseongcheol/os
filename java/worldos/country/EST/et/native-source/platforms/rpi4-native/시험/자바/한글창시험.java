// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.aken;
import Eesti.oma.vidin;
import Eesti.oma.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    aken 화면;
    Silt 안내;
    tekstiväli 입력;
    public void Käivita() {
        검사.참인지(sündmus_järjekord.사건처리중인가(), "Eesti 화면 작업 큐");
        화면 = new aken("Eesti teek aken", 400, 280);
        안내 = vidin.silt_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = vidin.tekstiväli("Nimi_2", 20, 65, 340, 30);
        화면.Lisa_element(안내);
        화면.Lisa_element(입력);
        화면.Lisa_element(vidin.nupp("인사하기", 20, 110, 180, 32, this));
        화면.saade_aken();
        Väljund.kirjutamine_liin("KOREAN SWING READY");
    }
    public void saama_Toiming(Toiming_teatamine Sündmus) {
        검사.참인지(sündmus_järjekord.사건처리중인가(), "Eesti Nimi 되부름");
        검사.참인지(Sündmus.INDEX() == 1001 && Sündmus.sündmuse_allikas() instanceof nupp, "Eesti Sündmus 객체와 출처");
        검사.참인지(!((Object)Sündmus.sündmuse_allikas() instanceof javax.swing.JButton), "표준 단추와 독립된 vorming_VALUE");
        검사.참인지(!((Object)Sündmus instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 vorming_VALUE");
        안내.kirjutamine_SMS("안녕하세요 " + 입력.글읽기());
        Väljund.kirjutamine_liin("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumendid) {
        sündmus_järjekord.나중에실행(new 한글창시험());
    }
}
