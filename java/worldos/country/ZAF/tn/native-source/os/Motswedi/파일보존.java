// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 Store_Boleng fometa_Boleng. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] faele_lenaneothalo = new int[1024];
    static int 바이트해시(int Boleng, int tshedimosetso) { return (Boleng ^ tshedimosetso) * 16777619; }
    static void phimola_tshedimosetso() {
        for (int tshupane = 0; tshupane < 512; tshupane++) Polokelo_mobaele_Kgolagano.karolo_tshedimosetso_93985c38[tshupane] = 0;
    }
    static int lenaneothalo_Palotlalo(int 위치) {
        return faele_lenaneothalo[위치] | faele_lenaneothalo[위치 + 1] << 8 | faele_lenaneothalo[위치 + 2] << 16 | faele_lenaneothalo[위치 + 3] << 24;
    }
    static void kwala_lenaneothalo_Palotlalo(int 위치, int Boleng) {
        for (int tshupane = 0; tshupane < 4; tshupane++) faele_lenaneothalo[위치 + tshupane] = (Boleng >>> (tshupane * 8)) & 255;
    }
    static boolean tlhola_lenaneothalo() {
        for (int faele = 0; faele < 8; faele++) {
            int boleele_Boleng = 0;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64; sebaka_tsenyo++) memori_setsamaisadifaele.leina[sebaka_tsenyo] = faele_lenaneothalo[faele * 72 + sebaka_tsenyo];
            while (boleele_Boleng < 64 && memori_setsamaisadifaele.leina[boleele_Boleng] != 0) boleele_Boleng++;
            if (boleele_Boleng == 0) continue;
            if (!memori_setsamaisadifaele.tlhola_leina(memori_setsamaisadifaele.leina, boleele_Boleng)
                || lenaneothalo_Palotlalo(faele * 72 + 64) < 0 || lenaneothalo_Palotlalo(faele * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < faele; 앞++) {
                boolean 같음 = faele_lenaneothalo[앞 * 72 + boleele_Boleng] == 0;
                for (int sebaka_tsenyo = 0; sebaka_tsenyo < boleele_Boleng; sebaka_tsenyo++) if (faele_lenaneothalo[앞 * 72 + sebaka_tsenyo] != memori_setsamaisadifaele.leina[sebaka_tsenyo]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int simolola_karolo = 1 + 보존본 * 259;
        if (Polokelo_mobaele_Kgolagano.읽기(simolola_karolo) < 0 || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(0) != 0x4a4b534e) return -1;
        int 세대 = Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(4), 검사합 = Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(8);
        if (세대 < 1 || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int heše_faele = 0x811c9dc5;
        for (int karolo_Boleng = 0; karolo_Boleng < 258; karolo_Boleng++) {
            if (Polokelo_mobaele_Kgolagano.읽기(simolola_karolo + 1 + karolo_Boleng) < 0) return -1;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 512; sebaka_tsenyo++) {
                int Boleng = Polokelo_mobaele_Kgolagano.karolo_tshedimosetso_93985c38[sebaka_tsenyo];
                heše_faele = 바이트해시(heše_faele, Boleng);
                if (karolo_Boleng < 2) faele_lenaneothalo[karolo_Boleng * 512 + sebaka_tsenyo] = Boleng;
            }
        }
        return heše_faele == 검사합 && tlhola_lenaneothalo() ? 세대 : -1;
    }
    static int tsenya(int 보존본) {
        int simolola_karolo = 1 + 보존본 * 259;
        for (int karolo_Boleng = 0; karolo_Boleng < 2; karolo_Boleng++) {
            if (Polokelo_mobaele_Kgolagano.읽기(simolola_karolo + 1 + karolo_Boleng) < 0) return -5;
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 512; sebaka_tsenyo++) faele_lenaneothalo[karolo_Boleng * 512 + sebaka_tsenyo] = Polokelo_mobaele_Kgolagano.karolo_tshedimosetso_93985c38[sebaka_tsenyo];
        }
        for (int faele = 0; faele < 8; faele++) {
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64; sebaka_tsenyo++) memori_setsamaisadifaele.이름들[faele * 64 + sebaka_tsenyo] = faele_lenaneothalo[faele * 72 + sebaka_tsenyo];
            memori_setsamaisadifaele.lekanya_lenaane[faele] = faele_lenaneothalo[faele * 72] == 0 ? 0 : lenaneothalo_Palotlalo(faele * 72 + 64);
            memori_setsamaisadifaele.허가들[faele] = lenaneothalo_Palotlalo(faele * 72 + 68) & 511;
            for (int karolo_Boleng = 0; karolo_Boleng < 32; karolo_Boleng++) {
                if (Polokelo_mobaele_Kgolagano.읽기(simolola_karolo + 3 + faele * 32 + karolo_Boleng) < 0) return -5;
                int aterese = mobaele_Boleng.faele_memori() + faele * 16384 + karolo_Boleng * 512;
                for (int sebaka_tsenyo = 0; sebaka_tsenyo < 512; sebaka_tsenyo++) mobaele_Boleng.kwala_memori(aterese + sebaka_tsenyo, Polokelo_mobaele_Kgolagano.karolo_tshedimosetso_93985c38[sebaka_tsenyo]);
            }
        }
        return 0;
    }
    static void Baakanya() {
        if (Polokelo_mobaele_Kgolagano.읽기(0) < 0 || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(0) != 0x54534b4a
            || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(4) != 0x3145524f || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(8) != 2048
            || Polokelo_mobaele_Kgolagano.go_lokolola_Palotlalo(12) != 0x3153464a) {
            문자단말.kwala("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Polokelo_mobaele_Kgolagano.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.kwala("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (tsenya(현재보존본) < 0) {
            문자단말.kwala("STORE read failed; halted to preserve files\n"); mobaele_Boleng.정지();
        }
        문자단말.kwala("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int tsamaisanya() {
        if (!Polokelo_mobaele_Kgolagano.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, simolola_karolo = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 mobaele_Boleng 캐시를 비운다.
        phimola_tshedimosetso();
        if (Polokelo_mobaele_Kgolagano.kwala(simolola_karolo) < 0 || Polokelo_mobaele_Kgolagano.밀어쓰기() < 0) return -5;
        for (int sebaka_tsenyo = 0; sebaka_tsenyo < 1024; sebaka_tsenyo++) faele_lenaneothalo[sebaka_tsenyo] = 0;
        for (int faele = 0; faele < 8; faele++) if (memori_setsamaisadifaele.이름들[faele * 64] != 0) {
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 64; sebaka_tsenyo++) faele_lenaneothalo[faele * 72 + sebaka_tsenyo] = memori_setsamaisadifaele.이름들[faele * 64 + sebaka_tsenyo];
            kwala_lenaneothalo_Palotlalo(faele * 72 + 64, memori_setsamaisadifaele.lekanya_lenaane[faele]);
            kwala_lenaneothalo_Palotlalo(faele * 72 + 68, memori_setsamaisadifaele.허가들[faele]);
        }
        int heše_faele = 0x811c9dc5;
        for (int karolo_Boleng = 0; karolo_Boleng < 258; karolo_Boleng++) {
            for (int sebaka_tsenyo = 0; sebaka_tsenyo < 512; sebaka_tsenyo++) {
                int Boleng = 0;
                if (karolo_Boleng < 2) Boleng = faele_lenaneothalo[karolo_Boleng * 512 + sebaka_tsenyo];
                else {
                    int faele = (karolo_Boleng - 2) / 32, 위치 = (karolo_Boleng - 2) % 32 * 512 + sebaka_tsenyo;
                    if (faele_lenaneothalo[faele * 72] != 0 && 위치 < memori_setsamaisadifaele.lekanya_lenaane[faele])
                        Boleng = mobaele_Boleng.기억읽기(mobaele_Boleng.faele_memori() + faele * 16384 + 위치);
                }
                Polokelo_mobaele_Kgolagano.karolo_tshedimosetso_93985c38[sebaka_tsenyo] = Boleng; heše_faele = 바이트해시(heše_faele, Boleng);
            }
            if (Polokelo_mobaele_Kgolagano.kwala(simolola_karolo + 1 + karolo_Boleng) < 0) return -5;
        }
        if (Polokelo_mobaele_Kgolagano.밀어쓰기() < 0) return -5;
        phimola_tshedimosetso(); Polokelo_mobaele_Kgolagano.kwala_Palotlalo_Boleng(0, 0x4a4b534e);
        Polokelo_mobaele_Kgolagano.kwala_Palotlalo_Boleng(4, 세대번호 + 1); Polokelo_mobaele_Kgolagano.kwala_Palotlalo_Boleng(8, heše_faele);
        Polokelo_mobaele_Kgolagano.kwala_Palotlalo_Boleng(12, (세대번호 + 1) ^ heše_faele ^ 0x4a4b534e);
        if (Polokelo_mobaele_Kgolagano.kwala(simolola_karolo) < 0 || Polokelo_mobaele_Kgolagano.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
