// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.eigin.Gluggi;
import Íslenska.eigin.Skýring;
import Íslenska.eigin.SMS_reitur;
import Íslenska.eigin.hnappur;
import Íslenska.eigin.atvik_biðröð;
import Íslenska.eigin.úttak;
import Íslenska.eigin.실행할일;
import Íslenska.eigin.동작받이;
import Íslenska.eigin.동작알림;

/** eigin 커널의 Swing Gluggi: Íslenska 입력 → hnappur → LESTUMIG_eb81d7d9 Texti uppfæra. */
public class Gluggadæmi implements 실행할일, 동작받이 {
    private Gluggi 인사창;
    private SMS_reitur heiti_reitur;
    private Skýring 인사말;
    private int 인사횟수;

    public void opið_gluggi() {
        인사창 = new Gluggi("Íslenska Swing", 460, 300);
        인사창.bæta_við_eining(new Skýring("Íslenska", 20, 20, 420, 28));
        heiti_reitur = new SMS_reitur("Íslenska", 20, 64, 420, 30);
        인사말 = new Skýring("Íslenska", 20, 152, 420, 28);
        인사창.bæta_við_eining(heiti_reitur);
        인사창.bæta_við_eining(new hnappur("인사하기", 20, 108, 180, 32, this));
        인사창.bæta_við_eining(인사말);
        인사창.bæta_við_eining(new Skýring("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.sýna_gluggi();
        úttak.skrifa_lína("GUI 예제 Undirbúa: Gluggadæmi");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skrifa_SMS("Íslenska, " + heiti_reitur.글읽기() + "님! (" + 인사횟수 + ")");
        úttak.skrifa_lína("GUI 인사: " + 인사말.글읽기());
    }

    public void Keyra() { opið_gluggi(); }
    public void 동작받기(동작알림 알림) {
        úttak.skrifa_lína("Aðgerð 알림: " + 알림.skipun_SMS());
        인사하기();
    }
    public static void Keyra_2() {
        atvik_biðröð.나중에실행(new Gluggadæmi());
    }
}
