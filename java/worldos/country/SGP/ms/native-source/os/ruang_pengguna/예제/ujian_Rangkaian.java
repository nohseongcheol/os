// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class ujian_Rangkaian {
    public static int Jalan() {
        int 첫째 = ruang_pengguna.buka_rangkaian(45000);
        if (첫째 < 0) { ruang_pengguna.Tulis("NETWORK UNAVAILABLE\n"); return 3; }
        int[] data = new int[8];
        boolean hantar_VALUE = ruang_pengguna.buka_rangkaian(45000) == -98
            && ruang_pengguna.자료받기(첫째, data, 0) == -11
            && ruang_pengguna.자료받기(첫째, data, 50) == -110
            && ruang_pengguna.자료받기(첫째, data, 3000) == -22
            && ruang_pengguna.e_mel_data_5b5410b2(첫째, 0x0a000202, 9, data, 9) == -90
            && ruang_pengguna.자료받기(첫째, null, 0) == -14
            && ruang_pengguna.Tutup_rangkaian(첫째) == 0 && ruang_pengguna.Tutup_rangkaian(첫째) == -9;
        ruang_pengguna.Tulis(hantar_VALUE ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return hantar_VALUE ? 0 : 1;
    }
}
