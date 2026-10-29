// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 mailen_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Reseau_Driver {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] Mobil_Adress = new int[6];
    static int 송신수 = 0, 수신수 = 0, Feeler_COUNT = 0;

    static int 설정읽기(int 장치번호, int positionéieren) {
        Mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | positionéieren);
        return Mobil_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Préparéieren() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int Standardwäert = 설정읽기(장치번호, 0x10);
        if ((Standardwäert & 1) == 0 || (Standardwäert & 0xfffffffc) < 0x100 || (Standardwäert & 0xfffffffc) > 65535) return false;
        입출력기준주소 = Standardwäert & 0xfffc;
        int Befeel = 설정읽기(장치번호, 4);
        Mobil_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        Mobil_VALUE.입출력짧은수쓰기(0xcfc, Befeel | 5); // I/O 및 bus master Erlaben_VALUE, PCI Status_VALUE 비트는 건드리지 않음
        Mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!reset_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) Mobil_Adress[INDEX] = Mobil_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean reset_VALUE() {
        Mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Laf = Mobil_VALUE.밀리초();
        while ((Mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (Mobil_VALUE.밀리초() - Laf > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        Mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, Mobil_VALUE.Reseau_Späicher());
        for (int INDEX = 0; INDEX < 4; INDEX++) Mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, Mobil_VALUE.Reseau_Späicher() + 12288);
        Mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        Mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        Mobil_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        Mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/Iwwerdroung_VALUE, wrap 연속 Store_VALUE, 8KiB
        Mobil_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int mailen(int[] Daten, int Längt_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (Längt_VALUE < 14 || Längt_VALUE > 1514) return -90;
        int Status_Port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Laf = Mobil_VALUE.밀리초();
        while ((Mobil_VALUE.입출력정수읽기(Status_Port) & 0x2000) == 0)
            if (Mobil_VALUE.밀리초() - Laf > 100) return -110;
        int d_Gréisst_veränneren = Längt_VALUE < 60 ? 60 : Längt_VALUE;
        for (int INDEX = 0; INDEX < d_Gréisst_veränneren; INDEX++)
            Mobil_VALUE.schreiwen_Späicher(Mobil_VALUE.Reseau_Späicher() + 12288 + INDEX, INDEX < Längt_VALUE ? Daten[INDEX] : 0);
        Mobil_VALUE.입출력정수쓰기(Status_Port, d_Gréisst_veränneren | 0x00080000);
        Laf = Mobil_VALUE.밀리초();
        while ((Mobil_VALUE.입출력정수읽기(Status_Port) & 0xe0008000) == 0)
            if (Mobil_VALUE.밀리초() - Laf > 100) return -110;
        if ((Mobil_VALUE.입출력정수읽기(Status_Port) & 0x8000) == 0) { Feeler_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return Längt_VALUE;
    }

    static int 받기(int[] Daten) {
        if (입출력기준주소 == 0) return 0;
        if ((Mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            Feeler_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((Mobil_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = Mobil_VALUE.Reseau_Späicher() + 수신위치;
        int Status_VALUE = 실행관리.짧은수(머리), d_Gréisst_veränneren = 실행관리.짧은수(머리 + 2);
        if (d_Gréisst_veränneren == 0xfff0) return 0; // DMA 진행 중
        if (d_Gréisst_veränneren < 4 || d_Gréisst_veränneren > 1518) {
            Feeler_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int Längt_VALUE = d_Gréisst_veränneren - 4;
        if ((Status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Daten[INDEX] = Mobil_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { Längt_VALUE = 0; Feeler_COUNT++; }
        수신위치 = (수신위치 + d_Gréisst_veränneren + 4 + 3) & ~3;
        수신위치 &= 8191;
        Mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        Mobil_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return Längt_VALUE;
    }
}
