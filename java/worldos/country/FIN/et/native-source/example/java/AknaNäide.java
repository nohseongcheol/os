// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Eesti.oma.aken;
import Eesti.oma.Silt;
import Eesti.oma.tekstiväli;
import Eesti.oma.nupp;
import Eesti.oma.sündmus_järjekord;
import Eesti.oma.Väljund;
import Eesti.oma.실행할일;
import Eesti.oma.동작받이;
import Eesti.oma.Toiming_teatamine;

/** oma 커널의 Swing aken: et 입력 → nupp → 안내 Tekst värskendama. */
public class AknaNäide implements 실행할일, 동작받이 {
    private aken 인사창;
    private tekstiväli nimetus_väli;
    private Silt 인사말;
    private int 인사횟수;

    public void avama_aken() {
        인사창 = new aken("et Swing", 460, 300);
        인사창.Lisa_element(new Silt("et", 20, 20, 420, 28));
        nimetus_väli = new tekstiväli("et", 20, 64, 420, 30);
        인사말 = new Silt("et", 20, 152, 420, 28);
        인사창.Lisa_element(nimetus_väli);
        인사창.Lisa_element(new nupp("인사하기", 20, 108, 180, 32, this));
        인사창.Lisa_element(인사말);
        인사창.Lisa_element(new Silt("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.saade_aken();
        Väljund.kirjutamine_liin("GUI 예제 Ettevalmistamine: AknaNäide");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kirjutamine_SMS("et, " + nimetus_väli.글읽기() + "님! (" + 인사횟수 + ")");
        Väljund.kirjutamine_liin("GUI 인사: " + 인사말.글읽기());
    }

    public void Käivita() { avama_aken(); }
    public void saama_Toiming(Toiming_teatamine teatamine) {
        Väljund.kirjutamine_liin("Nimi teatamine: " + teatamine.käsk_SMS());
        인사하기();
    }
    public static void Käivita_2() {
        sündmus_järjekord.나중에실행(new AknaNäide());
    }
}
