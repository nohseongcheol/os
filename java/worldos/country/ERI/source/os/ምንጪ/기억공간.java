// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 ናይ_ስርዓት_ሓበሬታ 조회와 4KiB 고정 መጠን 작업 ክፋል_ዋጋ ምምዳብ_መኽዘን/반환. 일반 물리 ገጽ_ዋጋ 관리자는 아니다. */
public final class 기억공간 {
    static int[] ክፋል_ዋጋ = new int[8192];
    static int[] 사용 = new int[8];

    static int 정수읽기(int ኣድራሻ) {
        return መሳርሒ_ዋጋ.기억읽기(ኣድራሻ) | (መሳርሒ_ዋጋ.기억읽기(ኣድራሻ + 1) << 8)
            | (መሳርሒ_ዋጋ.기억읽기(ኣድራሻ + 2) << 16) | (መሳርሒ_ዋጋ.기억읽기(ኣድራሻ + 3) << 24);
    }

    static int 위쪽기억크기() {
        int ናይ_ስርዓት_ሓበሬታ = መሳርሒ_ዋጋ.부팅정보();
        if (መሳርሒ_ዋጋ.부팅표식() != 0x2badb002 || ናይ_ስርዓት_ሓበሬታ == 0 || (정수읽기(ናይ_ስርዓት_ሓበሬታ) & 1) == 0) return -1;
        return 정수읽기(ናይ_ስርዓት_ሓበሬታ + 8);
    }

    static int ምምዳብ_መኽዘን() {
        for (int መሐበሪ = 0; መሐበሪ < 사용.length; መሐበሪ++) {
            if (사용[መሐበሪ] == 0) {
                사용[መሐበሪ] = 1;
                for (int መሰኩዒ_ምእታው = 0; መሰኩዒ_ምእታው < 1024; መሰኩዒ_ምእታው++) ክፋል_ዋጋ[መሐበሪ * 1024 + መሰኩዒ_ምእታው] = 0;
                return መሐበሪ;
            }
        }
        return -1;
    }

    static boolean 반환(int መሐበሪ) {
        if (መሐበሪ < 0 || መሐበሪ >= 사용.length || 사용[መሐበሪ] == 0) return false;
        사용[መሐበሪ] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int መሐበሪ = 0; መሐበሪ < 사용.length; መሐበሪ++) 개수 += 사용[መሐበሪ];
        return 개수;
    }
}
