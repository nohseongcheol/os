// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ǹdịnezie_datà 부팅 후 호출되는 Java ndebà_akara. JVM과 usu 운영체제에 의존하지 않는다. */
public final class mkpụrụobī_kọmpùta {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int indèks = 1; indèks <= 끝; indèks++) 합 += indèks;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int indèks = 기억공간.kepụta_Nchekwa();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && indèks >= 0 && 기억공간.반환(indèks) && !기억공간.반환(indèks);
        문자단말.Chekwaa_ozi(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void Bido() {
        문자단말.Kwado();
        문자단말.Chekwaa_ozi("JKOROS NATIVE JAVA\n");
        문자단말.Chekwaa_ozi("자바 기계어 mkpụrụobī_kọmpùta_valuu Bido\n");
        if (njìarụ_valuu.부팅표식() != 0x2badb002) {
            문자단말.Chekwaa_ozi("BAD MULTIBOOT MAGIC\n");
            njìarụ_valuu.정지();
        }
        if (!시험()) njìarụ_valuu.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.Chekwaa_ozi("At least 16 MiB RAM required\n");
            njìarụ_valuu.정지();
        }
        njìarụ_valuu.Kwado_òjìàrụ_app();
        문자단말.Chekwaa_ozi("USER ELF: ring 3 / paging / int 0x80\n");
        Netwọọkụ_ǹnyà.Kwado();
        Netwọọkụ_ikpo.과정정리();
        memọrị_sistèm_ọbọakwụkwo.Kwado();
        파일보존.Kwado();
        명령해석기.Bido();
    }
}
