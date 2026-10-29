// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** werkelijk_gegevens machineopstart 후 호출되는 Java beginpunt. JVM과 host 운영체제에 의존하지 않는다. */
public final class Kern {
    static int totaal_WAARDE(int 끝) {
        int SOM_WAARDE = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SOM_WAARDE += INDEX;
        return SOM_WAARDE;
    }

    static boolean tests() {
        int[] 값들 = new int[4];
        값들[2] = totaal_WAARDE(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int deling_HR = -1;
        int INDEX = Geheugen_regio.toewijzen_Opslag();
        boolean doorgeven_WAARDE = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / deling_HR == 최소
            && 최소 % deling_HR == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && Geheugen_regio.Retour_HR(INDEX) && !Geheugen_regio.Retour_HR(INDEX);
        sms_Terminal.Schrijven(doorgeven_WAARDE ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return doorgeven_WAARDE;
    }

    public static void starten() {
        sms_Terminal.Bereid_voor();
        sms_Terminal.Schrijven("JKOROS NATIVE JAVA\n");
        sms_Terminal.Schrijven("자바 기계어 kernel_WAARDE starten\n");
        if (mobiel_WAARDE.부팅표식() != 0x2badb002) {
            sms_Terminal.Schrijven("BAD MULTIBOOT MAGIC\n");
            mobiel_WAARDE.정지();
        }
        if (!tests()) mobiel_WAARDE.정지();
        if (Geheugen_regio.HOOFDLETTERS_Geheugen_formaat_wijzigen() < 15360) {
            sms_Terminal.Schrijven("At least 16 MiB RAM required\n");
            mobiel_WAARDE.정지();
        }
        mobiel_WAARDE.Bereid_voor_gebruiker_app();
        sms_Terminal.Schrijven("USER ELF: ring 3 / paging / int 0x80\n");
        net_stuurprogramma.Bereid_voor();
        net_stack.Verscherpt_Proces();
        Geheugen_bestandssysteem.Bereid_voor();
        파일보존.Bereid_voor();
        Opdrachtvertolker.starten();
    }
}
