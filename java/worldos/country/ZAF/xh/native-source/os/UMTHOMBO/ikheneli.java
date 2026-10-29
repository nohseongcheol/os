// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** eyona_yenzekileyo_iingcombolo 부팅 후 호출되는 Java ufako_nkcukacha_inqaku. JVM과 umsingathi 운영체제에 의존하지 않는다. */
public final class ikheneli {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int indeksa = 1; indeksa <= 끝; indeksa++) 합 += indeksa;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int indeksa = 기억공간.yabela_Ugcino();
        boolean dlulisela_ixabiso = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && indeksa >= 0 && 기억공간.반환(indeksa) && !기억공간.반환(indeksa);
        문자단말.Bhala(dlulisela_ixabiso ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return dlulisela_ixabiso;
    }

    public static void Phumeza() {
        문자단말.lungisa();
        문자단말.Bhala("JKOROS NATIVE JAVA\n");
        문자단말.Bhala("자바 기계어 ikheneli_ixabiso Phumeza\n");
        if (isixhobo_ixabiso.부팅표식() != 0x2badb002) {
            문자단말.Bhala("BAD MULTIBOOT MAGIC\n");
            isixhobo_ixabiso.정지();
        }
        if (!시험()) isixhobo_ixabiso.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Bhala("At least 16 MiB RAM required\n");
            isixhobo_ixabiso.정지();
        }
        isixhobo_ixabiso.lungisa_umsebenzisi_inkqubo();
        문자단말.Bhala("USER ELF: ring 3 / paging / int 0x80\n");
        Inethiwekhi_idrayiva.lungisa();
        Inethiwekhi_fumba.과정정리();
        imemori_uhlobo_loseto_lwefayile.lungisa();
        파일보존.lungisa();
        명령해석기.Phumeza();
    }
}
