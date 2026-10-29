// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Indonesia.Asli.koneksi;
import Indonesia.Asli.실행인수;
import Indonesia.Asli.전문통로;
import Indonesia.Asli.문자;
import Indonesia.Asli.keluaranTeks;
import Indonesia.Asli.검사;
import Indonesia.Asli.aliran_input;
import Indonesia.Asli.I_O_pengecualian;

public class ContohJaringan {
    public static void jalankan() throws I_O_pengecualian {
        // host: python3 alat/예제되돌림.py --tcp-port 9000 --udp-port 9001
        koneksi Sambung = koneksi.Buka("10.0.2.2", 문자.urai_bilangan_bulat(실행인수.teks(0)));
        try {
            Sambung.TIMEOUT(700);
            byte[] email = 문자.부호화("JAVA TCP Indonesian\n");
            Sambung.keluaranTeks().Tulis(email);
            aliran_input 입력 = Sambung.입력();
            for (int 수 = 0; 수 < 문자.byte_COUNT(email); 수++) {
                검사.참인지(입력.Baca() == (email[수] & 255), "TCP balas 불일치");
            }
        } finally { Sambung.Tutup(); }
        전문통로 peserta = 전문통로.Buka(0);
        try {
            peserta.TIMEOUT(700);
            peserta.kirim("10.0.2.2", 문자.urai_bilangan_bulat(실행인수.teks(1)), "JAVA UDP Indonesian");
            검사.참인지(문자.같음(peserta.terima(), "JAVA UDP Indonesian"), "UDP balas 불일치");
        } finally { peserta.Tutup(); }
        keluaranTeks.tulis_baris("JAVA 네트워크 periksa: TCP UDP Indonesian");
    }
}
