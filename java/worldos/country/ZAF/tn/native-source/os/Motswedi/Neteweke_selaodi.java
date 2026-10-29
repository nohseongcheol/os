// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 romela_Boleng 버퍼와 8KiB 수신 lupu_Boleng. 인터럽트 대신 폴링한다. */
public final class Neteweke_selaodi {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] mobaele_aterese = new int[6];
    static int 송신수 = 0, 수신수 = 0, 오류수 = 0;

    static int 설정읽기(int 장치번호, int 위치) {
        mobaele_Boleng.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | 위치);
        return mobaele_Boleng.입출력정수읽기(0xcfc);
    }

    static boolean Baakanya() {
        int 장치번호 = -1;
        for (int tshupane = 0; tshupane < 32; tshupane++) {
            if (설정읽기(tshupane, 0) == 0x813910ec) { 장치번호 = tshupane; break; }
        }
        if (장치번호 < 0) return false;
        int boleng_jo_bo_rulaganyeditsweng_ruri = 설정읽기(장치번호, 0x10);
        if ((boleng_jo_bo_rulaganyeditsweng_ruri & 1) == 0 || (boleng_jo_bo_rulaganyeditsweng_ruri & 0xfffffffc) < 0x100 || (boleng_jo_bo_rulaganyeditsweng_ruri & 0xfffffffc) > 65535) return false;
        입출력기준주소 = boleng_jo_bo_rulaganyeditsweng_ruri & 0xfffc;
        int Taelo = 설정읽기(장치번호, 4);
        mobaele_Boleng.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        mobaele_Boleng.입출력짧은수쓰기(0xcfc, Taelo | 5); // I/O 및 bus master letla_Boleng, PCI kemo_Boleng 비트는 건드리지 않음
        mobaele_Boleng.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Tlhamagape_Boleng()) { 입출력기준주소 = 0; return false; }
        for (int tshupane = 0; tshupane < 6; tshupane++) mobaele_aterese[tshupane] = mobaele_Boleng.입출력바이트읽기(입출력기준주소 + tshupane);
        return true;
    }

    static boolean Tlhamagape_Boleng() {
        mobaele_Boleng.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int dirisa = mobaele_Boleng.밀리초();
        while ((mobaele_Boleng.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mobaele_Boleng.밀리초() - dirisa > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        mobaele_Boleng.입출력정수쓰기(입출력기준주소 + 0x30, mobaele_Boleng.Neteweke_memori());
        for (int tshupane = 0; tshupane < 4; tshupane++) mobaele_Boleng.입출력정수쓰기(입출력기준주소 + 0x20 + tshupane * 4, mobaele_Boleng.Neteweke_memori() + 12288);
        mobaele_Boleng.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mobaele_Boleng.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mobaele_Boleng.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mobaele_Boleng.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/kgaso_Boleng, wrap 연속 Store_Boleng, 8KiB
        mobaele_Boleng.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int romela(int[] tshedimosetso, int boleele_Boleng) {
        if (입출력기준주소 == 0) return -19;
        if (boleele_Boleng < 14 || boleele_Boleng > 1514) return -90;
        int kemo_gorogisetsa = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int dirisa = mobaele_Boleng.밀리초();
        while ((mobaele_Boleng.입출력정수읽기(kemo_gorogisetsa) & 0x2000) == 0)
            if (mobaele_Boleng.밀리초() - dirisa > 100) return -110;
        int lekanya = boleele_Boleng < 60 ? 60 : boleele_Boleng;
        for (int tshupane = 0; tshupane < lekanya; tshupane++)
            mobaele_Boleng.kwala_memori(mobaele_Boleng.Neteweke_memori() + 12288 + tshupane, tshupane < boleele_Boleng ? tshedimosetso[tshupane] : 0);
        mobaele_Boleng.입출력정수쓰기(kemo_gorogisetsa, lekanya | 0x00080000);
        dirisa = mobaele_Boleng.밀리초();
        while ((mobaele_Boleng.입출력정수읽기(kemo_gorogisetsa) & 0xe0008000) == 0)
            if (mobaele_Boleng.밀리초() - dirisa > 100) return -110;
        if ((mobaele_Boleng.입출력정수읽기(kemo_gorogisetsa) & 0x8000) == 0) { 오류수++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return boleele_Boleng;
    }

    static int 받기(int[] tshedimosetso) {
        if (입출력기준주소 == 0) return 0;
        if ((mobaele_Boleng.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            오류수++;
            if (!Tlhamagape_Boleng()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mobaele_Boleng.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mobaele_Boleng.Neteweke_memori() + 수신위치;
        int kemo_Boleng = 실행관리.짧은수(머리), lekanya = 실행관리.짧은수(머리 + 2);
        if (lekanya == 0xfff0) return 0; // DMA 진행 중
        if (lekanya < 4 || lekanya > 1518) {
            오류수++;
            if (!Tlhamagape_Boleng()) 입출력기준주소 = 0;
            return 0;
        }
        int boleele_Boleng = lekanya - 4;
        if ((kemo_Boleng & 1) != 0) {
            for (int tshupane = 0; tshupane < boleele_Boleng; tshupane++) tshedimosetso[tshupane] = mobaele_Boleng.기억읽기(머리 + 4 + tshupane);
            수신수++;
        } else { boleele_Boleng = 0; 오류수++; }
        수신위치 = (수신위치 + lekanya + 4 + 3) & ~3;
        수신위치 &= 8191;
        mobaele_Boleng.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        mobaele_Boleng.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return boleele_Boleng;
    }
}
