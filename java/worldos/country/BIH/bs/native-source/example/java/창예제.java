// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.prozor;
import 한국어.자체.Oznaka;
import 한국어.자체.SMS_polje;
import 한국어.자체.dugme;
import 한국어.자체.događaj_redoslijed;
import 한국어.자체.Ispis;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing prozor: bs 입력 → dugme → Pročitaj_me_eb81d7d9 Tekst osvježiti. */
public class 창예제 implements 실행할일, 동작받이 {
    private prozor 인사창;
    private SMS_polje naziv_polje;
    private Oznaka 인사말;
    private int 인사횟수;

    public void kreirati_prozor() {
        인사창 = new prozor("bs Swing", 460, 300);
        인사창.dodati_element(new Oznaka("bs", 20, 20, 420, 28));
        naziv_polje = new SMS_polje("bs", 20, 64, 420, 30);
        인사말 = new Oznaka("bs", 20, 152, 420, 28);
        인사창.dodati_element(naziv_polje);
        인사창.dodati_element(new dugme("인사하기", 20, 108, 180, 32, this));
        인사창.dodati_element(인사말);
        인사창.dodati_element(new Oznaka("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.program_prozor();
        Ispis.pisati_redak("GUI 예제 Pripremiti: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.pisati_SMS("bs, " + naziv_polje.글읽기() + "님! (" + 인사횟수 + ")");
        Ispis.pisati_redak("GUI 인사: " + 인사말.글읽기());
    }

    public void Izvrši() { kreirati_prozor(); }
    public void 동작받기(동작알림 알림) {
        Ispis.pisati_redak("radnja 알림: " + 알림.komanda_SMS());
        인사하기();
    }
    public static void Pokreni() {
        događaj_redoslijed.나중에실행(new 창예제());
    }
}
