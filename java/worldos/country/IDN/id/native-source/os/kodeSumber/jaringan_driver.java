// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 kirim_VALUE 버퍼와 8KiB terima_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class jaringan_driver {
    static int 입출력기준주소 = 0;
    static int terima_posisi = 0, 송신칸 = 0;
    static int[] Ponsel_surel = new int[6];
    static int 송신수 = 0, terima_COUNT = 0, kesalahan_COUNT = 0;

    static int 설정읽기(int 장치번호, int posisi) {
        Ponsel_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | posisi);
        return Ponsel_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Siapkan() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int nilai_default = 설정읽기(장치번호, 0x10);
        if ((nilai_default & 1) == 0 || (nilai_default & 0xfffffffc) < 0x100 || (nilai_default & 0xfffffffc) > 65535) return false;
        입출력기준주소 = nilai_default & 0xfffc;
        int perintah = 설정읽기(장치번호, 4);
        Ponsel_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        Ponsel_VALUE.입출력짧은수쓰기(0xcfc, perintah | 5); // I/O 및 bus master Perbolehkan_VALUE, PCI Status_VALUE 비트는 건드리지 않음
        Ponsel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!reset_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) Ponsel_surel[INDEX] = Ponsel_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean reset_VALUE() {
        Ponsel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int jalankan = Ponsel_VALUE.밀리초();
        while ((Ponsel_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (Ponsel_VALUE.밀리초() - jalankan > 100) return false;
        terima_posisi = 0; 송신칸 = 0;
        Ponsel_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, Ponsel_VALUE.jaringan_Memori());
        for (int INDEX = 0; INDEX < 4; INDEX++) Ponsel_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, Ponsel_VALUE.jaringan_Memori() + 12288);
        Ponsel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        Ponsel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        Ponsel_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        Ponsel_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/siar_VALUE, wrap 연속 Store_VALUE, 8KiB
        Ponsel_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int kirim(int[] data, int panjang_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (panjang_VALUE < 14 || panjang_VALUE > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int jalankan = Ponsel_VALUE.밀리초();
        while ((Ponsel_VALUE.입출력정수읽기(status_port) & 0x2000) == 0)
            if (Ponsel_VALUE.밀리초() - jalankan > 100) return -110;
        int Ukuran = panjang_VALUE < 60 ? 60 : panjang_VALUE;
        for (int INDEX = 0; INDEX < Ukuran; INDEX++)
            Ponsel_VALUE.tulis_Memori(Ponsel_VALUE.jaringan_Memori() + 12288 + INDEX, INDEX < panjang_VALUE ? data[INDEX] : 0);
        Ponsel_VALUE.입출력정수쓰기(status_port, Ukuran | 0x00080000);
        jalankan = Ponsel_VALUE.밀리초();
        while ((Ponsel_VALUE.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (Ponsel_VALUE.밀리초() - jalankan > 100) return -110;
        if ((Ponsel_VALUE.입출력정수읽기(status_port) & 0x8000) == 0) { kesalahan_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return panjang_VALUE;
    }

    static int terima(int[] data) {
        if (입출력기준주소 == 0) return 0;
        if ((Ponsel_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            kesalahan_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((Ponsel_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int kepala_VALUE = Ponsel_VALUE.jaringan_Memori() + terima_posisi;
        int Status_VALUE = 실행관리.짧은수(kepala_VALUE), Ukuran = 실행관리.짧은수(kepala_VALUE + 2);
        if (Ukuran == 0xfff0) return 0; // DMA 진행 중
        if (Ukuran < 4 || Ukuran > 1518) {
            kesalahan_COUNT++;
            if (!reset_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int panjang_VALUE = Ukuran - 4;
        if ((Status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) data[INDEX] = Ponsel_VALUE.기억읽기(kepala_VALUE + 4 + INDEX);
            terima_COUNT++;
        } else { panjang_VALUE = 0; kesalahan_COUNT++; }
        terima_posisi = (terima_posisi + Ukuran + 4 + 3) & ~3;
        terima_posisi &= 8191;
        Ponsel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (terima_posisi - 16) & 65535);
        Ponsel_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return panjang_VALUE;
    }
}
