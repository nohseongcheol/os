// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 cuir_VALUE 버퍼와 8KiB 수신 lùb_VALUE. 인터럽트 대신 폴링한다. */
public final class lìonra_dràibhear {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] uidheam_ADDRESS = new int[6];
    static int 송신수 = 0, 수신수 = 0, mearachd_COUNT = 0;

    static int 설정읽기(int 장치번호, int suidhich) {
        uidheam_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | suidhich);
        return uidheam_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Ullaich() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int luach_bunaiteach = 설정읽기(장치번호, 0x10);
        if ((luach_bunaiteach & 1) == 0 || (luach_bunaiteach & 0xfffffffc) < 0x100 || (luach_bunaiteach & 0xfffffffc) > 65535) return false;
        입출력기준주소 = luach_bunaiteach & 0xfffc;
        int àithne = 설정읽기(장치번호, 4);
        uidheam_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        uidheam_VALUE.입출력짧은수쓰기(0xcfc, àithne | 5); // I/O 및 bus master Ceadaich_VALUE, PCI cor_VALUE 비트는 건드리지 않음
        uidheam_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!ath_shuidhich_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) uidheam_ADDRESS[INDEX] = uidheam_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean ath_shuidhich_VALUE() {
        uidheam_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int ruith = uidheam_VALUE.밀리초();
        while ((uidheam_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (uidheam_VALUE.밀리초() - ruith > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        uidheam_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, uidheam_VALUE.lìonra_cuimhne());
        for (int INDEX = 0; INDEX < 4; INDEX++) uidheam_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, uidheam_VALUE.lìonra_cuimhne() + 12288);
        uidheam_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        uidheam_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        uidheam_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        uidheam_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/craoladh_VALUE, wrap 연속 Store_VALUE, 8KiB
        uidheam_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int cuir(int[] dàta, int faid_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (faid_VALUE < 14 || faid_VALUE > 1514) return -90;
        int cor_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int ruith = uidheam_VALUE.밀리초();
        while ((uidheam_VALUE.입출력정수읽기(cor_port) & 0x2000) == 0)
            if (uidheam_VALUE.밀리초() - ruith > 100) return -110;
        int atharraich_am_meud = faid_VALUE < 60 ? 60 : faid_VALUE;
        for (int INDEX = 0; INDEX < atharraich_am_meud; INDEX++)
            uidheam_VALUE.sgrìobh_cuimhne(uidheam_VALUE.lìonra_cuimhne() + 12288 + INDEX, INDEX < faid_VALUE ? dàta[INDEX] : 0);
        uidheam_VALUE.입출력정수쓰기(cor_port, atharraich_am_meud | 0x00080000);
        ruith = uidheam_VALUE.밀리초();
        while ((uidheam_VALUE.입출력정수읽기(cor_port) & 0xe0008000) == 0)
            if (uidheam_VALUE.밀리초() - ruith > 100) return -110;
        if ((uidheam_VALUE.입출력정수읽기(cor_port) & 0x8000) == 0) { mearachd_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return faid_VALUE;
    }

    static int 받기(int[] dàta) {
        if (입출력기준주소 == 0) return 0;
        if ((uidheam_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            mearachd_COUNT++;
            if (!ath_shuidhich_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((uidheam_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = uidheam_VALUE.lìonra_cuimhne() + 수신위치;
        int cor_VALUE = 실행관리.짧은수(머리), atharraich_am_meud = 실행관리.짧은수(머리 + 2);
        if (atharraich_am_meud == 0xfff0) return 0; // DMA 진행 중
        if (atharraich_am_meud < 4 || atharraich_am_meud > 1518) {
            mearachd_COUNT++;
            if (!ath_shuidhich_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int faid_VALUE = atharraich_am_meud - 4;
        if ((cor_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < faid_VALUE; INDEX++) dàta[INDEX] = uidheam_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { faid_VALUE = 0; mearachd_COUNT++; }
        수신위치 = (수신위치 + atharraich_am_meud + 4 + 3) & ~3;
        수신위치 &= 8191;
        uidheam_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        uidheam_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return faid_VALUE;
    }
}
