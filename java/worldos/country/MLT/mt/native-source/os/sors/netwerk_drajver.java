// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 bagħat_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class netwerk_drajver {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] mowbajl_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, żball_COUNT = 0;

    static int 설정읽기(int 장치번호, int pożizzjoni) {
        mowbajl_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | pożizzjoni);
        return mowbajl_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Ħejji() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int valur_default = 설정읽기(장치번호, 0x10);
        if ((valur_default & 1) == 0 || (valur_default & 0xfffffffc) < 0x100 || (valur_default & 0xfffffffc) > 65535) return false;
        입출력기준주소 = valur_default & 0xfffc;
        int kmand = 설정읽기(장치번호, 4);
        mowbajl_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        mowbajl_VALUE.입출력짧은수쓰기(0xcfc, kmand | 5); // I/O 및 bus master ppermetti_VALUE, PCI stat_VALUE 비트는 건드리지 않음
        mowbajl_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!rrisettja_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) mowbajl_ADDRESS[INDEX] = mowbajl_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean rrisettja_VALUE() {
        mowbajl_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int serje = mowbajl_VALUE.밀리초();
        while ((mowbajl_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (mowbajl_VALUE.밀리초() - serje > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        mowbajl_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, mowbajl_VALUE.netwerk_Memorja());
        for (int INDEX = 0; INDEX < 4; INDEX++) mowbajl_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, mowbajl_VALUE.netwerk_Memorja() + 12288);
        mowbajl_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        mowbajl_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        mowbajl_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        mowbajl_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/xandira_VALUE, wrap 연속 Store_VALUE, 8KiB
        mowbajl_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int bagħat(int[] data, int tul_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (tul_VALUE < 14 || tul_VALUE > 1514) return -90;
        int stat_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int serje = mowbajl_VALUE.밀리초();
        while ((mowbajl_VALUE.입출력정수읽기(stat_port) & 0x2000) == 0)
            if (mowbajl_VALUE.밀리초() - serje > 100) return -110;
        int daqqas = tul_VALUE < 60 ? 60 : tul_VALUE;
        for (int INDEX = 0; INDEX < daqqas; INDEX++)
            mowbajl_VALUE.kiteb_Memorja(mowbajl_VALUE.netwerk_Memorja() + 12288 + INDEX, INDEX < tul_VALUE ? data[INDEX] : 0);
        mowbajl_VALUE.입출력정수쓰기(stat_port, daqqas | 0x00080000);
        serje = mowbajl_VALUE.밀리초();
        while ((mowbajl_VALUE.입출력정수읽기(stat_port) & 0xe0008000) == 0)
            if (mowbajl_VALUE.밀리초() - serje > 100) return -110;
        if ((mowbajl_VALUE.입출력정수읽기(stat_port) & 0x8000) == 0) { żball_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return tul_VALUE;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((mowbajl_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            żball_COUNT++;
            if (!rrisettja_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((mowbajl_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = mowbajl_VALUE.netwerk_Memorja() + 수신위치;
        int stat_VALUE = 실행관리.짧은수(머리), daqqas = 실행관리.짧은수(머리 + 2);
        if (daqqas == 0xfff0) return 0; // DMA 진행 중
        if (daqqas < 4 || daqqas > 1518) {
            żball_COUNT++;
            if (!rrisettja_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int tul_VALUE = daqqas - 4;
        if ((stat_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < tul_VALUE; INDEX++) data[INDEX] = mowbajl_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { tul_VALUE = 0; żball_COUNT++; }
        수신위치 = (수신위치 + daqqas + 4 + 3) & ~3;
        수신위치 &= 8191;
        mowbajl_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        mowbajl_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return tul_VALUE;
    }
}
