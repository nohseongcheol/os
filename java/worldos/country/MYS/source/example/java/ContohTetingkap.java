// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.Asli.Tetingkap;
import Melayu.Asli.label;
import Melayu.Asli.medan_teks;
import Melayu.Asli.Butang;
import Melayu.Asli.acara_baris;
import Melayu.Asli.출력;
import Melayu.Asli.실행할일;
import Melayu.Asli.동작받이;
import Melayu.Asli.동작알림;

/** Asli 커널의 Swing Tetingkap: Malay (macrolanguage) 입력 → Butang → README_eb81d7d9 Teks segar_semula. */
public class ContohTetingkap implements 실행할일, 동작받이 {
    private Tetingkap 인사창;
    private medan_teks nama_medan;
    private label 인사말;
    private int 인사횟수;

    public void buka_tetingkap() {
        인사창 = new Tetingkap("Malay (macrolanguage) Swing", 460, 300);
        인사창.tambah_unsur(new label("Selamat datang", 20, 20, 420, 28));
        nama_medan = new medan_teks("Malay (macrolanguage)", 20, 64, 420, 30);
        인사말 = new label("Selamat datang", 20, 152, 420, 28);
        인사창.tambah_unsur(nama_medan);
        인사창.tambah_unsur(new Butang("인사하기", 20, 108, 180, 32, this));
        인사창.tambah_unsur(인사말);
        인사창.tambah_unsur(new label("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.tayang_tetingkap();
        출력.tulis_baris("GUI 예제 Sediakan: ContohTetingkap");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.tulis_SMS("Selamat datang, " + nama_medan.글읽기() + "님! (" + 인사횟수 + ")");
        출력.tulis_baris("GUI 인사: " + 인사말.글읽기());
    }

    public void Lakukan() { buka_tetingkap(); }
    public void 동작받기(동작알림 알림) {
        출력.tulis_baris("Aksi 알림: " + 알림.perintah_SMS());
        인사하기();
    }
    public static void Jalan() {
        acara_baris.나중에실행(new ContohTetingkap());
    }
}
