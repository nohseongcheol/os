// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 göndərmək_VALUE 버퍼와 8KiB 수신 Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Şəbəkə_drayver {
    static int 입출력기준주소 = 0;
    static int 수신위치 = 0, 송신칸 = 0;
    static int[] cihaz_ünvan = new int[6];
    static int 송신수 = 0, 수신수 = 0, səhv_COUNT = 0;

    static int 설정읽기(int 장치번호, int yerinə_qoymaq) {
        cihaz_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | yerinə_qoymaq);
        return cihaz_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Hazırla() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int standart_qiymət = 설정읽기(장치번호, 0x10);
        if ((standart_qiymət & 1) == 0 || (standart_qiymət & 0xfffffffc) < 0x100 || (standart_qiymət & 0xfffffffc) > 65535) return false;
        입출력기준주소 = standart_qiymət & 0xfffc;
        int Əmr = 설정읽기(장치번호, 4);
        cihaz_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        cihaz_VALUE.입출력짧은수쓰기(0xcfc, Əmr | 5); // I/O 및 bus master İcazə_ver_VALUE, PCI vəziyyət_VALUE 비트는 건드리지 않음
        cihaz_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!sıfırlamaq_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) cihaz_ünvan[INDEX] = cihaz_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean sıfırlamaq_VALUE() {
        cihaz_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int İcra_Et = cihaz_VALUE.밀리초();
        while ((cihaz_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (cihaz_VALUE.밀리초() - İcra_Et > 100) return false;
        수신위치 = 0; 송신칸 = 0;
        cihaz_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, cihaz_VALUE.Şəbəkə_Yaddaş());
        for (int INDEX = 0; INDEX < 4; INDEX++) cihaz_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, cihaz_VALUE.Şəbəkə_Yaddaş() + 12288);
        cihaz_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        cihaz_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        cihaz_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        cihaz_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/yayım_VALUE, wrap 연속 Store_VALUE, 8KiB
        cihaz_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int göndərmək(int[] verilənlər, int uzunluq_VALUE) {
        if (입출력기준주소 == 0) return -19;
        if (uzunluq_VALUE < 14 || uzunluq_VALUE > 1514) return -90;
        int vəziyyət_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int İcra_Et = cihaz_VALUE.밀리초();
        while ((cihaz_VALUE.입출력정수읽기(vəziyyət_port) & 0x2000) == 0)
            if (cihaz_VALUE.밀리초() - İcra_Et > 100) return -110;
        int Böyüklük = uzunluq_VALUE < 60 ? 60 : uzunluq_VALUE;
        for (int INDEX = 0; INDEX < Böyüklük; INDEX++)
            cihaz_VALUE.yazmaq_Yaddaş(cihaz_VALUE.Şəbəkə_Yaddaş() + 12288 + INDEX, INDEX < uzunluq_VALUE ? verilənlər[INDEX] : 0);
        cihaz_VALUE.입출력정수쓰기(vəziyyət_port, Böyüklük | 0x00080000);
        İcra_Et = cihaz_VALUE.밀리초();
        while ((cihaz_VALUE.입출력정수읽기(vəziyyət_port) & 0xe0008000) == 0)
            if (cihaz_VALUE.밀리초() - İcra_Et > 100) return -110;
        if ((cihaz_VALUE.입출력정수읽기(vəziyyət_port) & 0x8000) == 0) { səhv_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return uzunluq_VALUE;
    }

    static int 받기(int[] verilənlər) {
        if (입출력기준주소 == 0) return 0;
        if ((cihaz_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            səhv_COUNT++;
            if (!sıfırlamaq_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((cihaz_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = cihaz_VALUE.Şəbəkə_Yaddaş() + 수신위치;
        int vəziyyət_VALUE = 실행관리.짧은수(머리), Böyüklük = 실행관리.짧은수(머리 + 2);
        if (Böyüklük == 0xfff0) return 0; // DMA 진행 중
        if (Böyüklük < 4 || Böyüklük > 1518) {
            səhv_COUNT++;
            if (!sıfırlamaq_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int uzunluq_VALUE = Böyüklük - 4;
        if ((vəziyyət_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) verilənlər[INDEX] = cihaz_VALUE.기억읽기(머리 + 4 + INDEX);
            수신수++;
        } else { uzunluq_VALUE = 0; səhv_COUNT++; }
        수신위치 = (수신위치 + Böyüklük + 4 + 3) & ~3;
        수신위치 &= 8191;
        cihaz_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (수신위치 - 16) & 65535);
        cihaz_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return uzunluq_VALUE;
    }
}
