// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.prozor;
import 한국어.자체.oznaka;
import 한국어.자체.tekstualno_polje;
import 한국어.자체.taster;
import 한국어.자체.događaj_red;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.radnja_obaveštavanje;

/** 자체 커널의 Swing prozor: српски 입력 → taster → 안내 SMS osvežiti. */
public class 창예제 implements 실행할일, 동작받이 {
    private prozor 인사창;
    private tekstualno_polje ime_polje;
    private oznaka 인사말;
    private int 인사횟수;

    public void otvoren_prozor() {
        인사창 = new prozor("српски Swing", 460, 300);
        인사창.Dodaj_element(new oznaka("српски", 20, 20, 420, 28));
        ime_polje = new tekstualno_polje("српски", 20, 64, 420, 30);
        인사말 = new oznaka("српски", 20, 152, 420, 28);
        인사창.Dodaj_element(ime_polje);
        인사창.Dodaj_element(new taster("인사하기", 20, 108, 180, 32, this));
        인사창.Dodaj_element(인사말);
        인사창.Dodaj_element(new oznaka("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.emisija_prozor();
        출력.줄쓰기("GUI 예제 Pripremi: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.글쓰기("српски, " + ime_polje.글읽기() + "님! (" + 인사횟수 + ")");
        출력.줄쓰기("GUI 인사: " + 인사말.글읽기());
    }

    public void Izvrši_obaveza() { otvoren_prozor(); }
    public void primiti_radnja(radnja_obaveštavanje obaveštavanje) {
        출력.줄쓰기("radnja obaveštavanje: " + obaveštavanje.komanda_SMS());
        인사하기();
    }
    public static void koristiti() {
        događaj_red.나중에실행(new 창예제());
    }
}
