// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktiki_verilənlər 부팅 후 호출되는 Java daxiletmə_p. JVM과 host 운영체제에 의존하지 않는다. */
public final class nüvə {
    static int 합계(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int bölmə_ölçü = -1;
        int INDEX = 기억공간.ayırmaq_Yaddaş();
        boolean ötürmək_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / bölmə_ölçü == 최소
            && 최소 % bölmə_ölçü == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.geri_qaytarmaq_ölçü(INDEX) && !기억공간.geri_qaytarmaq_ölçü(INDEX);
        SMS_Terminal.Yazma(ötürmək_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return ötürmək_VALUE;
    }

    public static void İcra_Et() {
        SMS_Terminal.Hazırla();
        SMS_Terminal.Yazma("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Yazma("자바 기계어 nüvə_VALUE İcra_Et\n");
        if (cihaz_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Yazma("BAD MULTIBOOT MAGIC\n");
            cihaz_VALUE.정지();
        }
        if (!시험()) cihaz_VALUE.정지();
        if (기억공간.UPPER_Yaddaş_ölçünü_dəyişmək() < 15360) {
            SMS_Terminal.Yazma("At least 16 MiB RAM required\n");
            cihaz_VALUE.정지();
        }
        cihaz_VALUE.Hazırla_istifadəçi_proqram();
        SMS_Terminal.Yazma("USER ELF: ring 3 / paging / int 0x80\n");
        Şəbəkə_drayver.Hazırla();
        Şəbəkə_Yığın.CLEAN_Proses();
        Yaddaş_fayl_sistemi.Hazırla();
        파일보존.Hazırla();
        명령해석기.İcra_Et();
    }
}
