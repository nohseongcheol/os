// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 seol_VALUE 버퍼와 8KiB 수신 lúb_VALUE. 인터럽트 대신 폴링한다. */
public final class Líonra_tiománaí {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] gléas_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, earráid_COUNT = 0;

    static int 설정읽기(int 장치번호, int suíomh) {
        gléas_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | suíomh);
        return gléas_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Ullmhaigh() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int luach_réamhshocraithe = 설정읽기(장치번호, 0x10);
        if ((luach_réamhshocraithe & 1) == 0 || (luach_réamhshocraithe & 0xfffffffc) < 0x100 || (luach_réamhshocraithe & 0xfffffffc) > 65535) return false;
        입출력기준주소 = luach_réamhshocraithe & 0xfffc;
        int Ordú = 설정읽기(장치번호, 4);
        gléas_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        gléas_VALUE.입출력짧은수쓰기(0xcfc, Ordú | 5); // I/O 및 bus master Ceadaigh_VALUE, PCI staid_VALUE 비트는 건드리지 않음
        gléas_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!athshocraigh_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) gléas_ADDRESS[INDEX] = gléas_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean athshocraigh_VALUE() {
        gléas_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Rith_2 = gléas_VALUE.밀리초();
        while ((gléas_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (gléas_VALUE.밀리초() - Rith_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        gléas_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, gléas_VALUE.Líonra_Cuimhne());
        for (int INDEX = 0; INDEX < 4; INDEX++) gléas_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, gléas_VALUE.Líonra_Cuimhne() + 12288);
        gléas_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        gléas_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        gléas_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        gléas_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/craolachán_VALUE, wrap 연속 Store_VALUE, 8KiB
        gléas_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int seol(int[] sonraí, int fad_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (fad_VALUE < 14 || fad_VALUE > 1514) return -90;
        int staid_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Rith_2 = gléas_VALUE.밀리초();
        while ((gléas_VALUE.입출력정수읽기(staid_port) & 0x2000) == 0)
            if (gléas_VALUE.밀리초() - Rith_2 > 100) return -110;
        int Méid = fad_VALUE < 60 ? 60 : fad_VALUE;
        for (int INDEX = 0; INDEX < Méid; INDEX++)
            gléas_VALUE.scríobh_Cuimhne(gléas_VALUE.Líonra_Cuimhne() + 12288 + INDEX, INDEX < fad_VALUE ? sonraí[INDEX] : 0);
        gléas_VALUE.입출력정수쓰기(staid_port, Méid | 0x00080000);
        Rith_2 = gléas_VALUE.밀리초();
        while ((gléas_VALUE.입출력정수읽기(staid_port) & 0xe0008000) == 0)
            if (gléas_VALUE.밀리초() - Rith_2 > 100) return -110;
        if ((gléas_VALUE.입출력정수읽기(staid_port) & 0x8000) == 0) { earráid_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return fad_VALUE;
    }

    static int 받기(int[] sonraí) {
        if (입출력기준주소 == 0) return 0;
        if ((gléas_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            earráid_COUNT++;
            if (!athshocraigh_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((gléas_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = gléas_VALUE.Líonra_Cuimhne() + 수신위치;
        int staid_VALUE = 실행관리.짧은수(머리), Méid = 실행관리.짧은수(머리 + 2);
        if (Méid == 0xfff0) return 0; // DMA 진행 중
        if (Méid < 4 || Méid > 1518) {
            earráid_COUNT++;
            if (!athshocraigh_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int fad_VALUE = Méid - 4;
        if ((staid_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < fad_VALUE; INDEX++) sonraí[INDEX] = gléas_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { fad_VALUE = 0; earráid_COUNT++; }
        수신위치 = (수신위치 + Méid + 4 + 3) & ~3;
        수신위치 &= 8191;
        gléas_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        gléas_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return fad_VALUE;
    }
}
