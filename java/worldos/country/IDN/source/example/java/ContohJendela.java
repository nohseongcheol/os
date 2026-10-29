// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Indonesia.Asli.Jendela;
import Indonesia.Asli.Nama;
import Indonesia.Asli.bidang_teks;
import Indonesia.Asli.tombol;
import Indonesia.Asli.acara_antrean;
import Indonesia.Asli.keluaranTeks;
import Indonesia.Asli.실행할일;
import Indonesia.Asli.동작받이;
import Indonesia.Asli.동작알림;

/** Asli 커널의 Swing Jendela: Indonesian 입력 → tombol → baca_saya_eb81d7d9 teks refresh. */
public class ContohJendela implements 실행할일, 동작받이 {
    private Jendela 인사창;
    private bidang_teks nama_bidang;
    private Nama 인사말;
    private int 인사횟수;

    public void buat_jendela() {
        인사창 = new Jendela("Indonesian Swing", 460, 300);
        인사창.tambah_elemen(new Nama("Halo", 20, 20, 420, 28));
        nama_bidang = new bidang_teks("Indonesian", 20, 64, 420, 30);
        인사말 = new Nama("Halo", 20, 152, 420, 28);
        인사창.tambah_elemen(nama_bidang);
        인사창.tambah_elemen(new tombol("인사하기", 20, 108, 180, 32, this));
        인사창.tambah_elemen(인사말);
        인사창.tambah_elemen(new Nama("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.show_jendela();
        keluaranTeks.tulis_baris("GUI 예제 Siapkan: ContohJendela");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.tulis_SMS("Halo, " + nama_bidang.글읽기() + "님! (" + 인사횟수 + ")");
        keluaranTeks.tulis_baris("GUI 인사: " + 인사말.글읽기());
    }

    public void Eksekusi() { buat_jendela(); }
    public void terima_Tugas(동작알림 알림) {
        keluaranTeks.tulis_baris("Aksi 알림: " + 알림.perintah_SMS());
        인사하기();
    }
    public static void jalankan() {
        acara_antrean.나중에실행(new ContohJendela());
    }
}
