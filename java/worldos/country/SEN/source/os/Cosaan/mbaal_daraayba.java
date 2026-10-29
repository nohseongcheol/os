// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 Yónnee_xëyma 버퍼와 8KiB 수신 wërngël_xëyma. 인터럽트 대신 폴링한다. */
public final class mbaal_daraayba {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] toftal_dëkkuwaay = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        toftal_xëyma.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return toftal_xëyma.입출력정수읽기(0xcfc);
    }

    static boolean jël_matuwaay() {
        int 장치번호 = -1;
        for (int àlluwa_tur = 0; àlluwa_tur < 32; àlluwa_tur++) {
            if (설정읽기(àlluwa_tur, 0) == 0x813910ec) { 장치번호 = àlluwa_tur; break; }
        }
        if (장치번호 < 0) return false;
        int xayma_bi_teew = 설정읽기(장치번호, 0x10);
        if ((xayma_bi_teew & 1) == 0 || (xayma_bi_teew & 0xfffffffc) < 0x100 || (xayma_bi_teew & 0xfffffffc) > 65535) return false;
        입출력기준주소 = xayma_bi_teew & 0xfffc;
        int ndigel = 설정읽기(장치번호, 4);
        toftal_xëyma.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        toftal_xëyma.입출력짧은수쓰기(0xcfc, ndigel | 5); // I/O 및 bus master Maye_xëyma, PCI nekkin_xëyma 비트는 건드리지 않음
        toftal_xëyma.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!besal_xëyma()) { 입출력기준주소 = 0; return false; }
        for (int àlluwa_tur = 0; àlluwa_tur < 6; àlluwa_tur++) toftal_dëkkuwaay[àlluwa_tur] = toftal_xëyma.입출력바이트읽기(입출력기준주소 + àlluwa_tur);
        return true;
    }

    static boolean besal_xëyma() {
        toftal_xëyma.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int daw = toftal_xëyma.밀리초();
        while ((toftal_xëyma.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (toftal_xëyma.밀리초() - daw > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        toftal_xëyma.입출력정수쓰기(입출력기준주소 + 0x30, toftal_xëyma.mbaal_fatlekookaay());
        for (int àlluwa_tur = 0; àlluwa_tur < 4; àlluwa_tur++) toftal_xëyma.입출력정수쓰기(입출력기준주소 + 0x20 + àlluwa_tur * 4, toftal_xëyma.mbaal_fatlekookaay() + 12288);
        toftal_xëyma.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        toftal_xëyma.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        toftal_xëyma.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        toftal_xëyma.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/teg_xëyma, wrap 연속 Store_xëyma, 8KiB
        toftal_xëyma.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int Yónnee(int[] mbir, int diir_xëyma) {
        if (입출력기준주소 == 0) return -19;
        if (diir_xëyma < 14 || diir_xëyma > 1514) return -90;
        int nekkin_jël = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int daw = toftal_xëyma.밀리초();
        while ((toftal_xëyma.입출력정수읽기(nekkin_jël) & 0x2000) == 0)
            if (toftal_xëyma.밀리초() - daw > 100) return -110;
        int tolluwaay = diir_xëyma < 60 ? 60 : diir_xëyma;
        for (int àlluwa_tur = 0; àlluwa_tur < tolluwaay; àlluwa_tur++)
            toftal_xëyma.biir_fatlekookaay(toftal_xëyma.mbaal_fatlekookaay() + 12288 + àlluwa_tur, àlluwa_tur < diir_xëyma ? mbir[àlluwa_tur] : 0);
        toftal_xëyma.입출력정수쓰기(nekkin_jël, tolluwaay | 0x00080000);
        daw = toftal_xëyma.밀리초();
        while ((toftal_xëyma.입출력정수읽기(nekkin_jël) & 0xe0008000) == 0)
            if (toftal_xëyma.밀리초() - daw > 100) return -110;
        if ((toftal_xëyma.입출력정수읽기(nekkin_jël) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return diir_xëyma;
    }

    static int 받기(int[] mbir) {
        if (입출력기준주소 == 0) return 0;
        if ((toftal_xëyma.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!besal_xëyma()) 입출력기준주소 = 0;
            return 0;
        }
        if ((toftal_xëyma.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = toftal_xëyma.mbaal_fatlekookaay() + 수신위치;
        int nekkin_xëyma = 실행관리.짧은수(머리), tolluwaay = 실행관리.짧은수(머리 + 2);
        if (tolluwaay == 0xfff0) return 0; // DMA 진행 중
        if (tolluwaay < 4 || tolluwaay > 1518) {
            오류수++;
            if (!besal_xëyma()) 입출력기준주소 = 0;
            return 0;
        }
        int diir_xëyma = tolluwaay - 4;
        if ((nekkin_xëyma & 1) != 0) {
            for (int àlluwa_tur = 0; àlluwa_tur < diir_xëyma; àlluwa_tur++) mbir[àlluwa_tur] = toftal_xëyma.기억읽기(머리 + 4 + àlluwa_tur);
            수신수++;
        } else { diir_xëyma = 0; 오류수++; }
        수신위치 = (수신위치 + tolluwaay + 4 + 3) & ~3;
        수신위치 &= 8191;
        toftal_xëyma.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        toftal_xëyma.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return diir_xëyma;
    }
}
