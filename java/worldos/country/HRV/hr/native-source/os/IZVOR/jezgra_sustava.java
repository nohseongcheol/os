// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvaran_podaci 부팅 후 호출되는 Java unos_p. JVM과 domaćin 운영체제에 의존하지 않는다. */
public final class jezgra_sustava {
    static int ukupni_zbroj_VALUE(int 끝) {
        int SUM_VALUE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_VALUE += INDEX;
        return SUM_VALUE;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = ukupni_zbroj_VALUE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int odjel_KR = -1;
        int INDEX = Memorija_regije.dodijeli_Pohrana();
        boolean proslijediti_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / odjel_KR == 최소
            && 최소 % odjel_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Memorija_regije.vratiti_KR(INDEX) && !Memorija_regije.vratiti_KR(INDEX);
        SMS_Terminal.Zapisuj(proslijediti_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return proslijediti_VALUE;
    }

    public static void Pokreni() {
        SMS_Terminal.Pripremi();
        SMS_Terminal.Zapisuj("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Zapisuj("자바 기계어 jezgra_sustava_VALUE Pokreni\n");
        if (uređaj_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Zapisuj("BAD MULTIBOOT MAGIC\n");
            uređaj_VALUE.정지();
        }
        if (!시험()) uređaj_VALUE.정지();
        if (Memorija_regije.UPPER_Memorija_promijeniti_veličinu() < 15360) {
            SMS_Terminal.Zapisuj("At least 16 MiB RAM required\n");
            uređaj_VALUE.정지();
        }
        uređaj_VALUE.Pripremi_korisnik_program();
        SMS_Terminal.Zapisuj("USER ELF: ring 3 / paging / int 0x80\n");
        mreža_upravljački_program.Pripremi();
        mreža_hrpa.CLEAN_Proces();
        Memorija_datotečni_sustav.Pripremi();
        파일보존.Pripremi();
        명령해석기.Pokreni();
    }
}
