// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** kgonthe_data 부팅 후 호출되는 Java go_tsenya_tshedimošo_ntlha. JVM과 go_nea_ditirelo 운영체제에 의존하지 않는다. */
public final class khenele {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int lokela = 1; lokela <= 끝; lokela++) 합 += lokela;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int lokela = 기억공간.aba_Bobolokelo();
        boolean feta_boleng = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && lokela >= 0 && 기억공간.반환(lokela) && !기억공간.반환(lokela);
        문자단말.Ngwala(feta_boleng ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return feta_boleng;
    }

    public static void Diriša() {
        문자단말.Lokišetša();
        문자단말.Ngwala("JKOROS NATIVE JAVA\n");
        문자단말.Ngwala("자바 기계어 khenele_boleng Diriša\n");
        if (sedirišwa_boleng.부팅표식() != 0x2badb002) {
            문자단말.Ngwala("BAD MULTIBOOT MAGIC\n");
            sedirišwa_boleng.정지();
        }
        if (!시험()) sedirišwa_boleng.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Ngwala("At least 16 MiB RAM required\n");
            sedirišwa_boleng.정지();
        }
        sedirišwa_boleng.Lokišetša_mošomiši_tirišo();
        문자단말.Ngwala("USER ELF: ring 3 / paging / int 0x80\n");
        Netweke_teraeba.Lokišetša();
        Netweke_kgoboko.과정정리();
        memori_tshepedišo_ya_difaele.Lokišetša();
        파일보존.Lokišetša();
        명령해석기.Diriša();
    }
}
