// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 yuborish_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Tarmoq_drayver {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] qurilma_manzil = new int[6];
    static int 송신수 = 0, 수신수 = 0, xato_COUNT = 0;

    static int 설정읽기(int 장치번호, int Holati) {
        qurilma_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Holati);
        return qurilma_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Tayyorlamoq() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int sukut_bo_yicha_qiymat = 설정읽기(장치번호, 0x10);
        if ((sukut_bo_yicha_qiymat & 1) == 0 || (sukut_bo_yicha_qiymat & 0xfffffffc) < 0x100 || (sukut_bo_yicha_qiymat & 0xfffffffc) > 65535) return false;
        입출력기준주소 = sukut_bo_yicha_qiymat & 0xfffc;
        int Buyruq = 설정읽기(장치번호, 4);
        qurilma_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        qurilma_VALUE.입출력짧은수쓰기(0xcfc, Buyruq | 5); // I/O 및 bus master Ruxsatnoma_VALUE, PCI holat_VALUE_e10195a1 비트는 건드리지 않음
        qurilma_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!Tashlamoq_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) qurilma_manzil[INDEX] = qurilma_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean Tashlamoq_VALUE() {
        qurilma_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Bajarish = qurilma_VALUE.밀리초();
        while ((qurilma_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (qurilma_VALUE.밀리초() - Bajarish > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        qurilma_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, qurilma_VALUE.Tarmoq_Xotira());
        for (int INDEX = 0; INDEX < 4; INDEX++) qurilma_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, qurilma_VALUE.Tarmoq_Xotira() + 12288);
        qurilma_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        qurilma_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        qurilma_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        qurilma_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/translyatsiya_qilish_VALUE, wrap 연속 Store_VALUE, 8KiB
        qurilma_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int yuborish(int[] ma_lumotlar, int uzunlik_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (uzunlik_VALUE < 14 || uzunlik_VALUE > 1514) return -90;
        int holat_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Bajarish = qurilma_VALUE.밀리초();
        while ((qurilma_VALUE.입출력정수읽기(holat_port) & 0x2000) == 0)
            if (qurilma_VALUE.밀리초() - Bajarish > 100) return -110;
        int Hajmi = uzunlik_VALUE < 60 ? 60 : uzunlik_VALUE;
        for (int INDEX = 0; INDEX < Hajmi; INDEX++)
            qurilma_VALUE.yozmoq_Xotira(qurilma_VALUE.Tarmoq_Xotira() + 12288 + INDEX, INDEX < uzunlik_VALUE ? ma_lumotlar[INDEX] : 0);
        qurilma_VALUE.입출력정수쓰기(holat_port, Hajmi | 0x00080000);
        Bajarish = qurilma_VALUE.밀리초();
        while ((qurilma_VALUE.입출력정수읽기(holat_port) & 0xe0008000) == 0)
            if (qurilma_VALUE.밀리초() - Bajarish > 100) return -110;
        if ((qurilma_VALUE.입출력정수읽기(holat_port) & 0x8000) == 0) { xato_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return uzunlik_VALUE;
    }

    static int 받기(int[] ma_lumotlar) {
        if (입출력기준주소 == 0) return 0;
        if ((qurilma_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            xato_COUNT++;
            if (!Tashlamoq_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((qurilma_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = qurilma_VALUE.Tarmoq_Xotira() + 수신위치;
        int holat_VALUE_e10195a1 = 실행관리.짧은수(머리), Hajmi = 실행관리.짧은수(머리 + 2);
        if (Hajmi == 0xfff0) return 0; // DMA 진행 중
        if (Hajmi < 4 || Hajmi > 1518) {
            xato_COUNT++;
            if (!Tashlamoq_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int uzunlik_VALUE = Hajmi - 4;
        if ((holat_VALUE_e10195a1 & 1) != 0) {
            for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) ma_lumotlar[INDEX] = qurilma_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { uzunlik_VALUE = 0; xato_COUNT++; }
        수신위치 = (수신위치 + Hajmi + 4 + 3) & ~3;
        수신위치 &= 8191;
        qurilma_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        qurilma_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return uzunlik_VALUE;
    }
}
