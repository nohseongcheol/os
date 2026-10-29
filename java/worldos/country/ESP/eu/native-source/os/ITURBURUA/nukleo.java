// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** benetako_datuak 부팅 후 호출되는 Java sarrera_p. JVM과 Ostalari 운영체제에 의존하지 않는다. */
public final class nukleo {
    static int 합계(int 끝) {
        int BATU_balio = 0;
        for (int INDIZE = 1; INDIZE <= 끝; INDIZE++) BATU_balio += INDIZE;
        return BATU_balio;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int zatiketa_neurria = -1;
        int INDIZE = 기억공간.esleitu_biltegi();
        boolean pasatu_balio = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / zatiketa_neurria == 최소
            && 최소 % zatiketa_neurria == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDIZE >= 0 && 기억공간.itzuli_neurria(INDIZE) && !기억공간.itzuli_neurria(INDIZE);
        SMS_Terminal.Idatzi(pasatu_balio ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return pasatu_balio;
    }

    public static void Exekutatu_2() {
        SMS_Terminal.준비();
        SMS_Terminal.Idatzi("JKOROS NATIVE JAVA\n");
        SMS_Terminal.Idatzi("자바 기계어 nukleo_balio Exekutatu_2\n");
        if (gailu_balio.부팅표식() != 0x2badb002) {
            SMS_Terminal.Idatzi("BAD MULTIBOOT MAGIC\n");
            gailu_balio.정지();
        }
        if (!시험()) gailu_balio.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            SMS_Terminal.Idatzi("At least 16 MiB RAM required\n");
            gailu_balio.정지();
        }
        gailu_balio.사용자준비();
        SMS_Terminal.Idatzi("USER ELF: ring 3 / paging / int 0x80\n");
        sare_kontrolatzaile.준비();
        sare_pila.GARBITU_prozesu();
        Memoria_fitxategi_sistema.준비();
        파일보존.준비();
        명령해석기.Exekutatu_2();
    }
}
