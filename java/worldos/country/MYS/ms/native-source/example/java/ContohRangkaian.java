// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.Asli.hubungan;
import Melayu.Asli.실행인수;
import Melayu.Asli.전문통로;
import Melayu.Asli.문자;
import Melayu.Asli.출력;
import Melayu.Asli.검사;
import Melayu.Asli.strim_input;
import Melayu.Asli.I_O_pengecualian;

public class ContohRangkaian {
    public static void Jalan() throws I_O_pengecualian {
        // hos: python3 alat/예제되돌림.py --tcp-port 9000 --udp-port 9001
        hubungan Sambung = hubungan.Buka("10.0.2.2", 문자.hurai_integer(실행인수.Teks(0)));
        try {
            Sambung.TIMEOUT(700);
            byte[] e_mel_8c783e64 = 문자.부호화("JAVA TCP ms\n");
            Sambung.출력().Tulis(e_mel_8c783e64);
            strim_input 입력 = Sambung.입력();
            for (int 수 = 0; 수 < 문자.bait_COUNT(e_mel_8c783e64); 수++) {
                검사.참인지(입력.Baca() == (e_mel_8c783e64[수] & 255), "TCP balas 불일치");
            }
        } finally { Sambung.Tutup(); }
        전문통로 peserta = 전문통로.Buka(0);
        try {
            peserta.TIMEOUT(700);
            peserta.e_mel_9aee63bd("10.0.2.2", 문자.hurai_integer(실행인수.Teks(1)), "JAVA UDP ms");
            검사.참인지(문자.같음(peserta.받기(), "JAVA UDP ms"), "UDP balas 불일치");
        } finally { peserta.Tutup(); }
        출력.tulis_baris("JAVA 네트워크 tentu_sahkan: TCP UDP ms");
    }
}
