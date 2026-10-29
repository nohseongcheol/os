// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 검사합과 두 보존본을 사용하는 작은 전용 lota_boleng fomete_boleng. fsync/sync에서만 영구 반영한다. */
public final class 파일보존 {
    static int 현재보존본 = -1, 세대번호 = 0;
    static int[] faele_tafola = new int[1024];
    static int 바이트해시(int boleng, int data) { return (boleng ^ data) * 16777619; }
    static void tloša_data() {
        for (int lokela = 0; lokela < 512; lokela++) Bobolokelo_sedirišwa_kgokaganya.karolo_data[lokela] = 0;
    }
    static int tafola_palotlalo(int 위치) {
        return faele_tafola[위치] | faele_tafola[위치 + 1] << 8 | faele_tafola[위치 + 2] << 16 | faele_tafola[위치 + 3] << 24;
    }
    static void ngwala_tafola_palotlalo(int 위치, int boleng) {
        for (int lokela = 0; lokela < 4; lokela++) faele_tafola[위치 + lokela] = (boleng >>> (lokela * 8)) & 255;
    }
    static boolean lekola_tafola() {
        for (int Faele = 0; Faele < 8; Faele++) {
            int botelele_boleng = 0;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64; sekgobana_go_tsenya_tshedimošo++) memori_tshepedišo_ya_difaele.Leina[sekgobana_go_tsenya_tshedimošo] = faele_tafola[Faele * 72 + sekgobana_go_tsenya_tshedimošo];
            while (botelele_boleng < 64 && memori_tshepedišo_ya_difaele.Leina[botelele_boleng] != 0) botelele_boleng++;
            if (botelele_boleng == 0) continue;
            if (!memori_tshepedišo_ya_difaele.lekola_leina(memori_tshepedišo_ya_difaele.Leina, botelele_boleng)
                || tafola_palotlalo(Faele * 72 + 64) < 0 || tafola_palotlalo(Faele * 72 + 64) > 16384) return false;
            for (int 앞 = 0; 앞 < Faele; 앞++) {
                boolean 같음 = faele_tafola[앞 * 72 + botelele_boleng] == 0;
                for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < botelele_boleng; sekgobana_go_tsenya_tshedimošo++) if (faele_tafola[앞 * 72 + sekgobana_go_tsenya_tshedimošo] != memori_tshepedišo_ya_difaele.Leina[sekgobana_go_tsenya_tshedimošo]) 같음 = false;
                if (같음) return false;
            }
        }
        return true;
    }
    static int 보존본검사(int 보존본) {
        int Thomišo_karolo = 1 + 보존본 * 259;
        if (Bobolokelo_sedirišwa_kgokaganya.Bala(Thomišo_karolo) < 0 || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(0) != 0x4a4b534e) return -1;
        int 세대 = Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(4), 검사합 = Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(8);
        if (세대 < 1 || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(12) != (세대 ^ 검사합 ^ 0x4a4b534e)) return -1;
        int haše_faele = 0x811c9dc5;
        for (int karolo_boleng = 0; karolo_boleng < 258; karolo_boleng++) {
            if (Bobolokelo_sedirišwa_kgokaganya.Bala(Thomišo_karolo + 1 + karolo_boleng) < 0) return -1;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 512; sekgobana_go_tsenya_tshedimošo++) {
                int boleng = Bobolokelo_sedirišwa_kgokaganya.karolo_data[sekgobana_go_tsenya_tshedimošo];
                haše_faele = 바이트해시(haše_faele, boleng);
                if (karolo_boleng < 2) faele_tafola[karolo_boleng * 512 + sekgobana_go_tsenya_tshedimošo] = boleng;
            }
        }
        return haše_faele == 검사합 && lekola_tafola() ? 세대 : -1;
    }
    static int laiša(int 보존본) {
        int Thomišo_karolo = 1 + 보존본 * 259;
        for (int karolo_boleng = 0; karolo_boleng < 2; karolo_boleng++) {
            if (Bobolokelo_sedirišwa_kgokaganya.Bala(Thomišo_karolo + 1 + karolo_boleng) < 0) return -5;
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 512; sekgobana_go_tsenya_tshedimošo++) faele_tafola[karolo_boleng * 512 + sekgobana_go_tsenya_tshedimošo] = Bobolokelo_sedirišwa_kgokaganya.karolo_data[sekgobana_go_tsenya_tshedimošo];
        }
        for (int Faele = 0; Faele < 8; Faele++) {
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64; sekgobana_go_tsenya_tshedimošo++) memori_tshepedišo_ya_difaele.이름들[Faele * 64 + sekgobana_go_tsenya_tshedimošo] = faele_tafola[Faele * 72 + sekgobana_go_tsenya_tshedimošo];
            memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele] = faele_tafola[Faele * 72] == 0 ? 0 : tafola_palotlalo(Faele * 72 + 64);
            memori_tshepedišo_ya_difaele.허가들[Faele] = tafola_palotlalo(Faele * 72 + 68) & 511;
            for (int karolo_boleng = 0; karolo_boleng < 32; karolo_boleng++) {
                if (Bobolokelo_sedirišwa_kgokaganya.Bala(Thomišo_karolo + 3 + Faele * 32 + karolo_boleng) < 0) return -5;
                int atrese = sedirišwa_boleng.faele_memori() + Faele * 16384 + karolo_boleng * 512;
                for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 512; sekgobana_go_tsenya_tshedimošo++) sedirišwa_boleng.ngwala_memori(atrese + sekgobana_go_tsenya_tshedimošo, Bobolokelo_sedirišwa_kgokaganya.karolo_data[sekgobana_go_tsenya_tshedimošo]);
            }
        }
        return 0;
    }
    static void Lokišetša() {
        if (Bobolokelo_sedirišwa_kgokaganya.Bala(0) < 0 || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(0) != 0x54534b4a
            || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(4) != 0x3145524f || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(8) != 2048
            || Bobolokelo_sedirišwa_kgokaganya.ripaganya_palotlalo(12) != 0x3153464a) {
            문자단말.Ngwala("STORE RAM only (no JKSTORE1 disk)\n"); return;
        }
        Bobolokelo_sedirišwa_kgokaganya.사용가능 = true;
        int 첫째 = 보존본검사(0), 둘째 = 보존본검사(1);
        if (첫째 < 0 && 둘째 < 0) { 문자단말.Ngwala("STORE ready; no valid snapshot\n"); return; }
        현재보존본 = 첫째 >= 둘째 ? 0 : 1; 세대번호 = 첫째 >= 둘째 ? 첫째 : 둘째;
        if (laiša(현재보존본) < 0) {
            문자단말.Ngwala("STORE read failed; halted to preserve files\n"); sedirišwa_boleng.정지();
        }
        문자단말.Ngwala("STORE restored generation "); 문자단말.수쓰기(세대번호); 문자단말.문자(10);
    }
    static int kopanya() {
        if (!Bobolokelo_sedirišwa_kgokaganya.사용가능) return -19;
        if (세대번호 == 2147483647) return -75;
        int 다음 = 현재보존본 == 0 ? 1 : 0, Thomišo_karolo = 1 + 다음 * 259;
        // 새 본문보다 먼저 이전 commit을 무효화하고 sedirišwa_boleng 캐시를 비운다.
        tloša_data();
        if (Bobolokelo_sedirišwa_kgokaganya.Ngwala(Thomišo_karolo) < 0 || Bobolokelo_sedirišwa_kgokaganya.밀어쓰기() < 0) return -5;
        for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 1024; sekgobana_go_tsenya_tshedimošo++) faele_tafola[sekgobana_go_tsenya_tshedimošo] = 0;
        for (int Faele = 0; Faele < 8; Faele++) if (memori_tshepedišo_ya_difaele.이름들[Faele * 64] != 0) {
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 64; sekgobana_go_tsenya_tshedimošo++) faele_tafola[Faele * 72 + sekgobana_go_tsenya_tshedimošo] = memori_tshepedišo_ya_difaele.이름들[Faele * 64 + sekgobana_go_tsenya_tshedimošo];
            ngwala_tafola_palotlalo(Faele * 72 + 64, memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele]);
            ngwala_tafola_palotlalo(Faele * 72 + 68, memori_tshepedišo_ya_difaele.허가들[Faele]);
        }
        int haše_faele = 0x811c9dc5;
        for (int karolo_boleng = 0; karolo_boleng < 258; karolo_boleng++) {
            for (int sekgobana_go_tsenya_tshedimošo = 0; sekgobana_go_tsenya_tshedimošo < 512; sekgobana_go_tsenya_tshedimošo++) {
                int boleng = 0;
                if (karolo_boleng < 2) boleng = faele_tafola[karolo_boleng * 512 + sekgobana_go_tsenya_tshedimošo];
                else {
                    int Faele = (karolo_boleng - 2) / 32, 위치 = (karolo_boleng - 2) % 32 * 512 + sekgobana_go_tsenya_tshedimošo;
                    if (faele_tafola[Faele * 72] != 0 && 위치 < memori_tshepedišo_ya_difaele.bogolo_Lenaneo[Faele])
                        boleng = sedirišwa_boleng.기억읽기(sedirišwa_boleng.faele_memori() + Faele * 16384 + 위치);
                }
                Bobolokelo_sedirišwa_kgokaganya.karolo_data[sekgobana_go_tsenya_tshedimošo] = boleng; haše_faele = 바이트해시(haše_faele, boleng);
            }
            if (Bobolokelo_sedirišwa_kgokaganya.Ngwala(Thomišo_karolo + 1 + karolo_boleng) < 0) return -5;
        }
        if (Bobolokelo_sedirišwa_kgokaganya.밀어쓰기() < 0) return -5;
        tloša_data(); Bobolokelo_sedirišwa_kgokaganya.ngwala_palotlalo_boleng(0, 0x4a4b534e);
        Bobolokelo_sedirišwa_kgokaganya.ngwala_palotlalo_boleng(4, 세대번호 + 1); Bobolokelo_sedirišwa_kgokaganya.ngwala_palotlalo_boleng(8, haše_faele);
        Bobolokelo_sedirišwa_kgokaganya.ngwala_palotlalo_boleng(12, (세대번호 + 1) ^ haše_faele ^ 0x4a4b534e);
        if (Bobolokelo_sedirišwa_kgokaganya.Ngwala(Thomišo_karolo) < 0 || Bobolokelo_sedirišwa_kgokaganya.밀어쓰기() < 0) return -5;
        현재보존본 = 다음; 세대번호++;
        return 0;
    }
}
