// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 부팅 Ozi_Sistèm 조회와 4KiB 고정 Ụhara 작업 nkebì_valuu kepụta_Nchekwa/반환. 일반 물리 ihuakwụkwọ_valuu 관리자는 아니다. */
public final class 기억공간 {
    static int[] nkebì_valuu = new int[8192];
    static int[] 사용 = new int[8];

    static int kerìsịa_ọnụọgụ_nzùrùòkè(int àdreèsì) {
        return njìarụ_valuu.기억읽기(àdreèsì) | (njìarụ_valuu.기억읽기(àdreèsì + 1) << 8)
            | (njìarụ_valuu.기억읽기(àdreèsì + 2) << 16) | (njìarụ_valuu.기억읽기(àdreèsì + 3) << 24);
    }

    static int 위쪽기억크기() {
        int Ozi_Sistèm = njìarụ_valuu.부팅정보();
        if (njìarụ_valuu.부팅표식() != 0x2badb002 || Ozi_Sistèm == 0 || (kerìsịa_ọnụọgụ_nzùrùòkè(Ozi_Sistèm) & 1) == 0) return -1;
        return kerìsịa_ọnụọgụ_nzùrùòkè(Ozi_Sistèm + 8);
    }

    static int kepụta_Nchekwa() {
        for (int indèks = 0; indèks < 사용.length; indèks++) {
            if (사용[indèks] == 0) {
                사용[indèks] = 1;
                for (int oghere_ndebà = 0; oghere_ndebà < 1024; oghere_ndebà++) nkebì_valuu[indèks * 1024 + oghere_ndebà] = 0;
                return indèks;
            }
        }
        return -1;
    }

    static boolean 반환(int indèks) {
        if (indèks < 0 || indèks >= 사용.length || 사용[indèks] == 0) return false;
        사용[indèks] = 0;
        return true;
    }

    static int 사용개수() {
        int 개수 = 0;
        for (int indèks = 0; indèks < 사용.length; indèks++) 개수 += 사용[indèks];
        return 개수;
    }
}
