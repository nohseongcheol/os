// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** makine_başlatma msinfo32_exe 조회와 4KiB 고정 Boyut 작업 bölüm_değer_366e0bfa ayırmak_Depolama/İade_KR. 일반 물리 sayfa_değer 관리자는 아니다. */
public final class Bellek_bölge {
    static int[] bölüm_değer_366e0bfa = new int[8192];
    static int[] kullanmak_değer = new int[8];

    static int ayrıştırmak_bilgi(int ADRES) {
        return cihaz_değer.기억읽기(ADRES) | (cihaz_değer.기억읽기(ADRES + 1) << 8)
            | (cihaz_değer.기억읽기(ADRES + 2) << 16) | (cihaz_değer.기억읽기(ADRES + 3) << 24);
    }

    static int BÜYÜKHARF_Bellek_boyutlandırmak() {
        int msinfo32_exe = cihaz_değer.부팅정보();
        if (cihaz_değer.부팅표식() != 0x2badb002 || msinfo32_exe == 0 || (ayrıştırmak_bilgi(msinfo32_exe) & 1) == 0) return -1;
        return ayrıştırmak_bilgi(msinfo32_exe + 8);
    }

    static int ayırmak_Depolama() {
        for (int Dizin = 0; Dizin < kullanmak_değer.length; Dizin++) {
            if (kullanmak_değer[Dizin] == 0) {
                kullanmak_değer[Dizin] = 1;
                for (int yuva_girdi = 0; yuva_girdi < 1024; yuva_girdi++) bölüm_değer_366e0bfa[Dizin * 1024 + yuva_girdi] = 0;
                return Dizin;
            }
        }
        return -1;
    }

    static boolean İade_KR(int Dizin) {
        if (Dizin < 0 || Dizin >= kullanmak_değer.length || kullanmak_değer[Dizin] == 0) return false;
        kullanmak_değer[Dizin] = 0;
        return true;
    }

    static int 사용개수() {
        int öğe_BAĞ_DEĞ_SAY = 0;
        for (int Dizin = 0; Dizin < kullanmak_değer.length; Dizin++) öğe_BAĞ_DEĞ_SAY += kullanmak_değer[Dizin];
        return öğe_BAĞ_DEĞ_SAY;
    }
}
