// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ትኽክለኛ_ሓበሬታ 부팅 후 호출되는 Java ምእታው_ነጥቢ. JVM과 አዐንግድ 운영체제에 의존하지 않는다. */
public final class ፍረ {
    static int 합계(int 끝) {
        int 합 = 0;
        for (int መሐበሪ = 1; መሐበሪ <= 끝; መሐበሪ++) 합 += መሐበሪ;
        return 합;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int 나눔 = -1;
        int መሐበሪ = 기억공간.ምምዳብ_መኽዘን();
        boolean 통과 = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / 나눔 == 최소
            && 최소 % 나눔 == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && መሐበሪ >= 0 && 기억공간.반환(መሐበሪ) && !기억공간.반환(መሐበሪ);
        문자단말.ጸሓፍ(통과 ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return 통과;
    }

    public static void ኣኺድ() {
        문자단말.ኣዳልው();
        문자단말.ጸሓፍ("JKOROS NATIVE JAVA\n");
        문자단말.ጸሓፍ("자바 기계어 ፍረ_ዋጋ ኣኺድ\n");
        if (መሳርሒ_ዋጋ.부팅표식() != 0x2badb002) {
            문자단말.ጸሓፍ("BAD MULTIBOOT MAGIC\n");
            መሳርሒ_ዋጋ.정지();
        }
        if (!시험()) መሳርሒ_ዋጋ.정지();
        if (기억공간.위쪽기억크기() < 15360) {
            문자단말.ጸሓፍ("At least 16 MiB RAM required\n");
            መሳርሒ_ዋጋ.정지();
        }
        መሳርሒ_ዋጋ.ኣዳልው_ተጠቃሚ_መተግበሪ();
        문자단말.ጸሓፍ("USER ELF: ring 3 / paging / int 0x80\n");
        ማሕበራዊ_ኔትወርክ_መወሃዲ.ኣዳልው();
        ማሕበራዊ_ኔትወርክ_ድርደራ.과정정리();
        ማህደር_ዝኽረት_ናይ_ፋይል_ስርዓት.ኣዳልው();
        파일보존.ኣዳልው();
        명령해석기.ኣኺድ();
    }
}
