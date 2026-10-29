// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class test_Ağ {
    public static int çalıştır() {
        int 첫째 = kullanıcı_alanı.açık_ağ(45000);
        if (첫째 < 0) { kullanıcı_alanı.Yazma("NETWORK UNAVAILABLE\n"); return 3; }
        int[] veri = new int[8];
        boolean geçirmek_değer = kullanıcı_alanı.açık_ağ(45000) == -98
            && kullanıcı_alanı.almak_veri(첫째, veri, 0) == -11
            && kullanıcı_alanı.almak_veri(첫째, veri, 50) == -110
            && kullanıcı_alanı.almak_veri(첫째, veri, 3000) == -22
            && kullanıcı_alanı.göndermek_veri(첫째, 0x0a000202, 9, veri, 9) == -90
            && kullanıcı_alanı.almak_veri(첫째, null, 0) == -14
            && kullanıcı_alanı.Kapat_ağ(첫째) == 0 && kullanıcı_alanı.Kapat_ağ(첫째) == -9;
        kullanıcı_alanı.Yazma(geçirmek_değer ? "UDP API CHECK PASS\n" : "UDP API CHECK FAIL\n");
        return geçirmek_değer ? 0 : 1;
    }
}
