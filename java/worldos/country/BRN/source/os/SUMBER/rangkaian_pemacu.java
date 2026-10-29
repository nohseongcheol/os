// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 e_mel_VALUE_f993dacd 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class rangkaian_pemacu {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] peranti_e_mel = new int[6];
    static int 송신수 = 0, 수신수 = 0, ralat_COUNT = 0;

    static int 설정읽기(int 장치번호, int Kedudukan) {
        peranti_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | Kedudukan);
        return peranti_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Sediakan() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int nilai_lalai = 설정읽기(장치번호, 0x10);
        if ((nilai_lalai & 1) == 0 || (nilai_lalai & 0xfffffffc) < 0x100 || (nilai_lalai & 0xfffffffc) > 65535) return false;
        입출력기준주소 = nilai_lalai & 0xfffc;
        int Perintah = 설정읽기(장치번호, 4);
        peranti_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        peranti_VALUE.입출력짧은수쓰기(0xcfc, Perintah | 5); // I/O 및 bus master Izin_VALUE, PCI status_VALUE 비트는 건드리지 않음
        peranti_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!set_semula_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) peranti_e_mel[INDEX] = peranti_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean set_semula_VALUE() {
        peranti_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int Jalan = peranti_VALUE.밀리초();
        while ((peranti_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (peranti_VALUE.밀리초() - Jalan > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        peranti_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, peranti_VALUE.rangkaian_Memori());
        for (int INDEX = 0; INDEX < 4; INDEX++) peranti_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, peranti_VALUE.rangkaian_Memori() + 12288);
        peranti_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        peranti_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        peranti_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        peranti_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/siaran_VALUE, wrap 연속 stor_VALUE, 8KiB
        peranti_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int e_mel_9aee63bd(int[] data, int kepanjangan_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (kepanjangan_VALUE < 14 || kepanjangan_VALUE > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int Jalan = peranti_VALUE.밀리초();
        while ((peranti_VALUE.입출력정수읽기(status_port) & 0x2000) == 0)
            if (peranti_VALUE.밀리초() - Jalan > 100) return -110;
        int Saiz = kepanjangan_VALUE < 60 ? 60 : kepanjangan_VALUE;
        for (int INDEX = 0; INDEX < Saiz; INDEX++)
            peranti_VALUE.tulis_Memori(peranti_VALUE.rangkaian_Memori() + 12288 + INDEX, INDEX < kepanjangan_VALUE ? data[INDEX] : 0);
        peranti_VALUE.입출력정수쓰기(status_port, Saiz | 0x00080000);
        Jalan = peranti_VALUE.밀리초();
        while ((peranti_VALUE.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (peranti_VALUE.밀리초() - Jalan > 100) return -110;
        if ((peranti_VALUE.입출력정수읽기(status_port) & 0x8000) == 0) { ralat_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return kepanjangan_VALUE;
    }

    static int 받기(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((peranti_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            ralat_COUNT++;
            if (!set_semula_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((peranti_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = peranti_VALUE.rangkaian_Memori() + 수신위치;
        int status_VALUE = 실행관리.짧은수(머리), Saiz = 실행관리.짧은수(머리 + 2);
        if (Saiz == 0xfff0) return 0; // DMA 진행 중
        if (Saiz < 4 || Saiz > 1518) {
            ralat_COUNT++;
            if (!set_semula_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int kepanjangan_VALUE = Saiz - 4;
        if ((status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) data[INDEX] = peranti_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { kepanjangan_VALUE = 0; ralat_COUNT++; }
        수신위치 = (수신위치 + Saiz + 4 + 3) & ~3;
        수신위치 &= 8191;
        peranti_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        peranti_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return kepanjangan_VALUE;
    }
}
