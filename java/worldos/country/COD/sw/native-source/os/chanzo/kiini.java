// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** halisi_data 부팅 후 호출되는 Java ingizo_pointi. JVM과 mwenyeji 운영체제에 의존하지 않는다. */
public final class kiini {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int kielezo = 1; kielezo <= 끝; kielezo++) 합 += kielezo;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int kielezo = 기억공간.tengea_Hifadhi();
        boolean pitisha_thamani = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && kielezo >= 0 && 기억공간.반환(kielezo) && !기억공간.반환(kielezo);
        문자단말.andika(pitisha_thamani ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return pitisha_thamani;
    }

    public static void endesha() {
        문자단말.Andaa();
        문자단말.andika("JKOROS NATIVE JAVA\n");
        문자단말.andika("자바 기계어 kiini_thamani_0611a8a8 endesha\n");
        if (kifaa_thamani.부팅표식() != 0x2badb002) {
            문자단말.andika("BAD MULTIBOOT MAGIC\n");
            kifaa_thamani.정지();
        }
        if (!시험()) kifaa_thamani.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.andika("At least 16 MiB RAM required\n");
            kifaa_thamani.정지();
        }
        kifaa_thamani.Andaa_mtumiaji_programu();
        문자단말.andika("USER ELF: ring 3 / paging / int 0x80\n");
        Mtandao_kiendeshaji.Andaa();
        Mtandao_Mpororo.Safi_Mchakato();
        kumbukumbu_mfumo_ya_mafaili.Andaa();
        파일보존.Andaa();
        명령해석기.endesha();
    }
}
