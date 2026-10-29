// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** fiili_veri makine_başlatma 후 호출되는 Java giriş_noktası. JVM과 konak 운영체제에 의존하지 않는다. */
public final class Çekirdek {
    static int toplam_değer(int 끝) {
        int SUM_değer = 0;
        for (int Dizin = 1; Dizin <= 끝; Dizin++) SUM_değer += Dizin;
        return SUM_değer;
    }

    static boolean sınamalar() {
        int[] 값들 = new int[4];
        값들[2] = toplam_değer(10);
        int Negatif_değer = -7;
        int 최소 = 0x80000000;
        int Bölge_KR = -1;
        int Dizin = Bellek_bölge.ayırmak_Depolama();
        boolean geçirmek_değer = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && Negatif_değer / 3 == -2 && Negatif_değer % 3 == -1 && 최소 / Bölge_KR == 최소
            && 최소 % Bölge_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && Dizin >= 0 && Bellek_bölge.İade_KR(Dizin) && !Bellek_bölge.İade_KR(Dizin);
        SMS_Terminal.Yazma(geçirmek_değer ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return geçirmek_değer;
    }

    public static void çalıştır() {
        SMS_Terminal.Hazırlan();
        SMS_Terminal.Yazma("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Yazma("자바 기계어 çekirdek_değer çalıştır\n");
        if (cihaz_değer.부팅표식() != 0x2badb002) {
            SMS_Terminal.Yazma("BAD MULTIBOOT MAGIC\n");
            cihaz_değer.정지();
        }
        if (!sınamalar()) cihaz_değer.정지();
        if (Bellek_bölge.BÜYÜKHARF_Bellek_boyutlandırmak() < 15360) {
            SMS_Terminal.Yazma("At least 16 MiB RAM required\n");
            cihaz_değer.정지();
        }
        cihaz_değer.Hazırlan_kullanıcı_program();
        SMS_Terminal.Yazma("USER ELF: ring 3 / paging / int 0x80\n");
        ağ_sürücü.Hazırlan();
        ağ_Yığın.TEMİZ_işlem();
        Bellek_dosya_sistemi.Hazırlan();
        파일보존.Hazırlan();
        KomutYorumlayıcı.çalıştır();
    }
}
