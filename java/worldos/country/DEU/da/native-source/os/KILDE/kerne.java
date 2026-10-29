// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** faktisk_data 부팅 후 호출되는 Java indgangspunkt. JVM과 vært 운영체제에 의존하지 않는다. */
public final class kerne {
    static int i_alt_VÆRDI(int 끝) {
        int SUM_VÆRDI = 0;
        for (int INDEKS = 1; INDEKS <= 끝; INDEKS++) SUM_VÆRDI += INDEKS;
        return SUM_VÆRDI;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = i_alt_VÆRDI(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int Division_KR = -1;
        int INDEKS = Hukommelse_område.tildel_Lager();
        boolean videregive_VÆRDI = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / Division_KR == 최소
            && 최소 % Division_KR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEKS >= 0 && Hukommelse_område.returnere_KR(INDEKS) && !Hukommelse_område.returnere_KR(INDEKS);
        sms_Terminal.Skrive(videregive_VÆRDI ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return videregive_VÆRDI;
    }

    public static void Kør_2() {
        sms_Terminal.Tilrettelæg();
        sms_Terminal.Skrive("JKOROS NATIVE JAVA\n");
        sms_Terminal.Skrive("자바 기계어 kerne_VÆRDI Kør_2\n");
        if (enhed_VÆRDI.부팅표식() != 0x2badb002) {
            sms_Terminal.Skrive("BAD MULTIBOOT MAGIC\n");
            enhed_VÆRDI.정지();
        }
        if (!시험()) enhed_VÆRDI.정지();
        if (Hukommelse_område.STORE_BOGSTAVER_Hukommelse_tilpasse_størrelse() < 15360) {
            sms_Terminal.Skrive("At least 16 MiB RAM required\n");
            enhed_VÆRDI.정지();
        }
        enhed_VÆRDI.Tilrettelæg_bruger_app();
        sms_Terminal.Skrive("USER ELF: ring 3 / paging / int 0x80\n");
        netværk_driver.Tilrettelæg();
        netværk_Stak.Ren_Proces();
        Hukommelse_filsystem.Tilrettelæg();
        파일보존.Tilrettelæg();
        명령해석기.Kør_2();
    }
}
