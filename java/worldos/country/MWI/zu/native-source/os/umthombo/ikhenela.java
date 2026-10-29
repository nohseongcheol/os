// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ulwazi_ngokwenzekile_imininingwane 부팅 후 호출되는 Java okufakwayo_iphoyinti. JVM과 singatha 운영체제에 의존하지 않는다. */
public final class ikhenela {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int thola_inkomba = 1; thola_inkomba <= 끝; thola_inkomba++) 합 += thola_inkomba;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int thola_inkomba = 기억공간.abela_Indawo_yokugcina();
        boolean dlulisa_inani = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && thola_inkomba >= 0 && 기억공간.반환(thola_inkomba) && !기억공간.반환(thola_inkomba);
        문자단말.Bhala(dlulisa_inani ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return dlulisa_inani;
    }

    public static void Sebenzisa() {
        문자단말.Hlela();
        문자단말.Bhala("JKOROS NATIVE JAVA\n");
        문자단말.Bhala("자바 기계어 ikhenela_inani Sebenzisa\n");
        if (idivayisi_inani.부팅표식() != 0x2badb002) {
            문자단말.Bhala("BAD MULTIBOOT MAGIC\n");
            idivayisi_inani.정지();
        }
        if (!시험()) idivayisi_inani.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Bhala("At least 16 MiB RAM required\n");
            idivayisi_inani.정지();
        }
        idivayisi_inani.Hlela_umsebenzisi_i_app();
        문자단말.Bhala("USER ELF: ring 3 / paging / int 0x80\n");
        iNethiwekhi_idrayiva.Hlela();
        iNethiwekhi_Isitaki.과정정리();
        inkumbulo_isistimu_yefayela.Hlela();
        파일보존.Hlela();
        명령해석기.Sebenzisa();
    }
}
