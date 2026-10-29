// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 anfon_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Rhwydwaith_gyrrwr {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] dyfais_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, gwall_COUNT = 0;

    static int 설정읽기(int 장치번호, int safle) {
        dyfais_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | safle);
        return dyfais_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Paratoi() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int gwerth_diofyn = 설정읽기(장치번호, 0x10);
        if ((gwerth_diofyn & 1) == 0 || (gwerth_diofyn & 0xfffffffc) < 0x100 || (gwerth_diofyn & 0xfffffffc) > 65535) return false;
        입출력기준주소 = gwerth_diofyn & 0xfffc;
        int Gorchymyn = 설정읽기(장치번호, 4);
        dyfais_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        dyfais_VALUE.입출력짧은수쓰기(0xcfc, Gorchymyn | 5); // I/O 및 bus master Caniatáu_VALUE, PCI cyflwr_VALUE 비트는 건드리지 않음
        dyfais_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Ailosod_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) dyfais_ADDRESS[INDEX] = dyfais_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Ailosod_VALUE() {
        dyfais_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Gweithredu_2 = dyfais_VALUE.밀리초();
        while ((dyfais_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (dyfais_VALUE.밀리초() - Gweithredu_2 > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        dyfais_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, dyfais_VALUE.Rhwydwaith_Cof());
        for (int INDEX = 0; INDEX < 4; INDEX++) dyfais_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, dyfais_VALUE.Rhwydwaith_Cof() + 12288);
        dyfais_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        dyfais_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        dyfais_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        dyfais_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/darlledu_VALUE, wrap 연속 Store_VALUE, 8KiB
        dyfais_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int anfon(int[] data, int hyd_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (hyd_VALUE < 14 || hyd_VALUE > 1514) return -90;
        int cyflwr_porth = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Gweithredu_2 = dyfais_VALUE.밀리초();
        while ((dyfais_VALUE.입출력정수읽기(cyflwr_porth) & 0x2000) == 0)
            if (dyfais_VALUE.밀리초() - Gweithredu_2 > 100) return -110;
        int Maint = hyd_VALUE < 60 ? 60 : hyd_VALUE;
        for (int INDEX = 0; INDEX < Maint; INDEX++)
            dyfais_VALUE.ysgrifennu_Cof(dyfais_VALUE.Rhwydwaith_Cof() + 12288 + INDEX, INDEX < hyd_VALUE ? data[INDEX] : 0);
        dyfais_VALUE.입출력정수쓰기(cyflwr_porth, Maint | 0x00080000);
        Gweithredu_2 = dyfais_VALUE.밀리초();
        while ((dyfais_VALUE.입출력정수읽기(cyflwr_porth) & 0xe0008000) == 0)
            if (dyfais_VALUE.밀리초() - Gweithredu_2 > 100) return -110;
        if ((dyfais_VALUE.입출력정수읽기(cyflwr_porth) & 0x8000) == 0) { gwall_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return hyd_VALUE;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((dyfais_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            gwall_COUNT++;
            if (!Ailosod_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((dyfais_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = dyfais_VALUE.Rhwydwaith_Cof() + 수신위치;
        int cyflwr_VALUE = 실행관리.짧은수(머리), Maint = 실행관리.짧은수(머리 + 2);
        if (Maint == 0xfff0) return 0; // DMA 진행 중
        if (Maint < 4 || Maint > 1518) {
            gwall_COUNT++;
            if (!Ailosod_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int hyd_VALUE = Maint - 4;
        if ((cyflwr_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < hyd_VALUE; INDEX++) data[INDEX] = dyfais_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { hyd_VALUE = 0; gwall_COUNT++; }
        수신위치 = (수신위치 + Maint + 4 + 3) & ~3;
        수신위치 &= 8191;
        dyfais_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        dyfais_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return hyd_VALUE;
    }
}
