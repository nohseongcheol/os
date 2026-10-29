// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.oma.Ikkuna;
import suomi.oma.Nimike;
import suomi.oma.tekstikenttä;
import suomi.oma.painike;
import suomi.oma.tapahtuma_jono;
import suomi.oma.tulostuspaikka;
import suomi.oma.실행할일;
import suomi.oma.동작받이;
import suomi.oma.동작알림;

/** oma 커널의 Swing Ikkuna: fi syöte_ARVO → painike → Lueminut_eb81d7d9 teksti päivittää. */
public class Ikkunaesimerkki implements 실행할일, 동작받이 {
    private Ikkuna 인사창;
    private tekstikenttä nimi_kenttä;
    private Nimike 인사말;
    private int 인사횟수;

    public void avata_ikkuna() {
        인사창 = new Ikkuna("fi Swing", 460, 300);
        인사창.Lisää_elementti(new Nimike("Hei", 20, 20, 420, 28));
        nimi_kenttä = new tekstikenttä("fi", 20, 64, 420, 30);
        인사말 = new Nimike("Hei", 20, 152, 420, 28);
        인사창.Lisää_elementti(nimi_kenttä);
        인사창.Lisää_elementti(new painike("인사하기", 20, 108, 180, 32, this));
        인사창.Lisää_elementti(인사말);
        인사창.Lisää_elementti(new Nimike("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.näyttää_ikkuna();
        tulostuspaikka.kirjoitus_rivi("GUI 예제 Valmistele: Ikkunaesimerkki");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kirjoitus_SMS("Hei, " + nimi_kenttä.lukea_SMS() + "님! (" + 인사횟수 + ")");
        tulostuspaikka.kirjoitus_rivi("GUI 인사: " + 인사말.lukea_SMS());
    }

    public void Suorita() { avata_ikkuna(); }
    public void saada_toimi(동작알림 알림) {
        tulostuspaikka.kirjoitus_rivi("Toiminto 알림: " + 알림.komento_SMS());
        인사하기();
    }
    public static void Suorita_2() {
        tapahtuma_jono.나중에실행(new Ikkunaesimerkki());
    }
}
