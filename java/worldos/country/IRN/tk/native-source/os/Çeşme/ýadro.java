// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** hakyky_maglumat 부팅 후 호출되는 Java girizmeklik_utuk. JVM과 esasy 운영체제에 의존하지 않는다. */
public final class ýadro {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int indeks = 1; indeks <= 끝; indeks++) 합 += indeks;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int indeks = 기억공간.bölüp_aýyr_Ammar();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && indeks >= 0 && 기억공간.반환(indeks) && !기억공간.반환(indeks);
        문자단말.Ýaz(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void Bitir() {
        문자단말.Taýýarla();
        문자단말.Ýaz("JKOROS NATIVE JAVA\n");
        문자단말.Ýaz("자바 기계어 ýadro_baha Bitir\n");
        if (enjam_baha.부팅표식() != 0x2badb002) {
            문자단말.Ýaz("BAD MULTIBOOT MAGIC\n");
            enjam_baha.정지();
        }
        if (!시험()) enjam_baha.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Ýaz("At least 16 MiB RAM required\n");
            enjam_baha.정지();
        }
        enjam_baha.Taýýarla_ulanyjy_programma();
        문자단말.Ýaz("USER ELF: ring 3 / paging / int 0x80\n");
        Tor_draýwer.Taýýarla();
        Tor_Desse.Päkize_Proses();
        ýat_faýl_ulgamy.Taýýarla();
        파일보존.Taýýarla();
        명령해석기.Bitir();
    }
}
