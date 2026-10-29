// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** PCI RTL8139 (10ec:8139), 단일 poslati_VALUE 버퍼와 8KiB primiti_VALUE Loop_VALUE. 인터럽트 대신 폴링한다. */
public final class Mreža_Upravljački_program {
    static int 입출력기준주소 = 0;
    static int primiti_pozicija = 0, 송신칸 = 0;
    static int[] uređaj_adresa = new int[6];
    static int 송신수 = 0, primiti_COUNT = 0, greška_COUNT = 0;

    static int 설정읽기(int 장치번호, int pozicija) {
        uređaj_VALUE.입출력정수쓰기(0xcf8, 0x80000000 | (장치번호 << 11) | pozicija);
        return uređaj_VALUE.입출력정수읽기(0xcfc);
    }

    static boolean Pripremi() {
        int 장치번호 = -1;
        for (int INDEX = 0; INDEX < 32; INDEX++) {
            if (설정읽기(INDEX, 0) == 0x813910ec) { 장치번호 = INDEX; break; }
        }
        if (장치번호 < 0) return false;
        int podrazumevana_vrednost = 설정읽기(장치번호, 0x10);
        if ((podrazumevana_vrednost & 1) == 0 || (podrazumevana_vrednost & 0xfffffffc) < 0x100 || (podrazumevana_vrednost & 0xfffffffc) > 65535) return false;
        입출력기준주소 = podrazumevana_vrednost & 0xfffc;
        int komanda = 설정읽기(장치번호, 4);
        uređaj_VALUE.입출력정수쓰기(0xcf8, 0x80000004 | (장치번호 << 11));
        uređaj_VALUE.입출력짧은수쓰기(0xcfc, komanda | 5); // I/O 및 bus master Dozvoli_VALUE, PCI Status_VALUE 비트는 건드리지 않음
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x52, 0);
        if (!vrati_VALUE()) { 입출력기준주소 = 0; return false; }
        for (int INDEX = 0; INDEX < 6; INDEX++) uređaj_adresa[INDEX] = uređaj_VALUE.입출력바이트읽기(입출력기준주소 + INDEX);
        return true;
    }

    static boolean vrati_VALUE() {
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x10);
        int koristiti = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 0x10) != 0)
            if (uređaj_VALUE.밀리초() - koristiti > 100) return false;
        primiti_pozicija = 0; 송신칸 = 0;
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x30, uređaj_VALUE.Mreža_Memorija());
        for (int INDEX = 0; INDEX < 4; INDEX++) uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x20 + INDEX * 4, uređaj_VALUE.Mreža_Memorija() + 12288);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3c, 0);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0xffff);
        uređaj_VALUE.입출력바이트쓰기(입출력기준주소 + 0x37, 0x0c);
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x44, 0x0000e78a); // 자기주소/emitovati_VALUE, wrap 연속 Store_VALUE, 8KiB
        uređaj_VALUE.입출력정수쓰기(입출력기준주소 + 0x40, 0x03000600);
        return true;
    }

    static int poslati(int[] podaci, int 길이) {
        if (입출력기준주소 == 0) return -19;
        if (길이 < 14 || 길이 > 1514) return -90;
        int status_port = 입출력기준주소 + 0x10 + 송신칸 * 4;
        int koristiti = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(status_port) & 0x2000) == 0)
            if (uređaj_VALUE.밀리초() - koristiti > 100) return -110;
        int promeniti_veličinu = 길이 < 60 ? 60 : 길이;
        for (int INDEX = 0; INDEX < promeniti_veličinu; INDEX++)
            uređaj_VALUE.기억쓰기(uređaj_VALUE.Mreža_Memorija() + 12288 + INDEX, INDEX < 길이 ? podaci[INDEX] : 0);
        uređaj_VALUE.입출력정수쓰기(status_port, promeniti_veličinu | 0x00080000);
        koristiti = uređaj_VALUE.밀리초();
        while ((uređaj_VALUE.입출력정수읽기(status_port) & 0xe0008000) == 0)
            if (uređaj_VALUE.밀리초() - koristiti > 100) return -110;
        if ((uređaj_VALUE.입출력정수읽기(status_port) & 0x8000) == 0) { greška_COUNT++; return -5; }
        송신칸 = (송신칸 + 1) & 3;
        송신수++;
        return 길이;
    }

    static int primiti(int[] podaci) {
        if (입출력기준주소 == 0) return 0;
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x3e) & 0x50) != 0) {
            greška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        if ((uređaj_VALUE.입출력바이트읽기(입출력기준주소 + 0x37) & 1) != 0) return 0;
        int 머리 = uređaj_VALUE.Mreža_Memorija() + primiti_pozicija;
        int Status_VALUE = 실행관리.짧은수(머리), promeniti_veličinu = 실행관리.짧은수(머리 + 2);
        if (promeniti_veličinu == 0xfff0) return 0; // DMA 진행 중
        if (promeniti_veličinu < 4 || promeniti_veličinu > 1518) {
            greška_COUNT++;
            if (!vrati_VALUE()) 입출력기준주소 = 0;
            return 0;
        }
        int 길이 = promeniti_veličinu - 4;
        if ((Status_VALUE & 1) != 0) {
            for (int INDEX = 0; INDEX < 길이; INDEX++) podaci[INDEX] = uređaj_VALUE.기억읽기(머리 + 4 + INDEX);
            primiti_COUNT++;
        } else { 길이 = 0; greška_COUNT++; }
        primiti_pozicija = (primiti_pozicija + promeniti_veličinu + 4 + 3) & ~3;
        primiti_pozicija &= 8191;
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x38, (primiti_pozicija - 16) & 65535);
        uređaj_VALUE.입출력짧은수쓰기(입출력기준주소 + 0x3e, 0x000f);
        return 길이;
    }
}
