// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** stvaran_podaci 부팅 후 호출되는 Java unos_p. JVM과 organizator 운영체제에 의존하지 않는다. */
public final class jezgro {
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
        int dijeljenje_mjera = -1;
        int INDEX = 기억공간.dodijeliti_Pohrana();
        boolean proslijediti_VALUE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / dijeljenje_mjera == 최소
            && 최소 % dijeljenje_mjera == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.vratiti_mjera(INDEX) && !기억공간.vratiti_mjera(INDEX);
        SMS_Terminal.Piši(proslijediti_VALUE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return proslijediti_VALUE;
    }

    public static void Pokreni() {
        SMS_Terminal.Pripremiti();
        SMS_Terminal.Piši("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Piši("자바 기계어 jezgro_VALUE Pokreni\n");
        if (uređaj_VALUE.부팅표식() != 0x2badb002) {
            SMS_Terminal.Piši("BAD MULTIBOOT MAGIC\n");
            uređaj_VALUE.정지();
        }
        if (!시험()) uređaj_VALUE.정지();
        if (기억공간.UPPER_Memorija_podesiti_veličinu() < 15360) {
            SMS_Terminal.Piši("At least 16 MiB RAM required\n");
            uređaj_VALUE.정지();
        }
        uređaj_VALUE.Pripremiti_korisnik_program();
        SMS_Terminal.Piši("USER ELF: ring 3 / paging / int 0x80\n");
        Mreža_drajver_uređaja.Pripremiti();
        Mreža_snop.CLEAN_proces();
        Memorija_fajl_sistem.Pripremiti();
        파일보존.Pripremiti();
        명령해석기.Pokreni();
    }
}
