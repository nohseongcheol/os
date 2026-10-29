// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 tavu_ARVO 경계를 지키는 삽입/삭제, 방향키, komento LOG_TIETUE, Tab valmis_ARVO. */
public final class rivi_editori {
    static boolean komentorivi;
    static int[] LOG_TIETUE = new int[16 * 1024], LOG_kesto = new int[16], Store_ARVO = new int[4096], 후보 = new int[64];
    static int LOG_LASKE, LOG_TIETUE_lopettaa_puhelu, Hae_ARVO, 저장길이, Koko, kohdistin_ARVO, 후보수, 후보길이, alku_ikkuna;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd suojattu_liittymä etä_näyttö run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String merkintä_luettelo, int alku_toimi, int lopettaa_puhelu_toimi, int syöte_kesto) {
        int tavu_LASKE=0;
        for(int sijainti=alku_toimi;sijainti<lopettaa_puhelu_toimi;sijainti++) {
            int merkkikoodi=merkintä_luettelo.charAt(sijainti);
            if(merkkikoodi>=0xd800 && merkkikoodi<=0xdbff && sijainti+1<lopettaa_puhelu_toimi)merkkikoodi=0x10000+((merkkikoodi-0xd800)<<10)+merkintä_luettelo.charAt(++sijainti)-0xdc00;
            int numero=merkkikoodi<128?1:merkkikoodi<2048?2:merkkikoodi<65536?3:4;
            if(tavu_LASKE+numero>62)return;
            for(int JONO_ARVO=numero-1;JONO_ARVO>=0;JONO_ARVO--)명령후보[tavu_LASKE++]=numero==1?merkkikoodi:JONO_ARVO==numero-1?(numero==2?0xc0:numero==3?0xe0:0xf0)|(merkkikoodi>>(6*JONO_ARVO)):0x80|((merkkikoodi>>(6*JONO_ARVO))&63);
        }
        if(tavu_LASKE<syöte_kesto)return;
        for(int sijainti=0;sijainti<syöte_kesto;sijainti++)if(명령후보[sijainti]!=명령해석기.syöterivi[sijainti])return;
        후보수++;후보길이=tavu_LASKE+1;
        for(int sijainti=0;sijainti<tavu_LASKE;sijainti++)후보[sijainti]=명령후보[sijainti];후보[tavu_LASKE]=' ';
    }
    static int etukamera_ARVO(int lukea_kohdistin) { if (lukea_kohdistin > 0) { lukea_kohdistin--; while (lukea_kohdistin > 0 && (명령해석기.syöterivi[lukea_kohdistin] & 192) == 128) lukea_kohdistin--; } return lukea_kohdistin; }
    static int BACK_ARVO(int lukea_kohdistin) { if (lukea_kohdistin < Koko) { lukea_kohdistin++; while (lukea_kohdistin < Koko && (명령해석기.syöterivi[lukea_kohdistin] & 192) == 128) lukea_kohdistin++; } return lukea_kohdistin; }
    static int 폭(int alku_toimi, int kohde_ARVO_INDEKSI) {
        int 글칸수 = 0;
        for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < kohde_ARVO_INDEKSI; Loop_INDEKSI++) { int tavu_data = 명령해석기.syöterivi[Loop_INDEKSI]; if ((tavu_data & 192) == 128) continue; 글칸수 += tavu_data >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void yrittää_uudelleen_ARVO() {
        단말.Kirjoitus("\r\u001b[2K");
        단말.Kirjoitus(komentorivi ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 syöterivi 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int SARAKKEET = Taulu.komentotulkki(13) & 65535; return SARAKKEET - (komentorivi ? 18 : 9); }
    static void 보이는줄() {
        if (kohdistin_ARVO < alku_ikkuna) alku_ikkuna = kohdistin_ARVO;
        while (폭(alku_ikkuna, kohdistin_ARVO) > 보이는폭()) alku_ikkuna = BACK_ARVO(alku_ikkuna);
        int lopettaa_puhelu_toimi = alku_ikkuna;
        while (lopettaa_puhelu_toimi < Koko && 폭(alku_ikkuna, BACK_ARVO(lopettaa_puhelu_toimi)) <= 보이는폭()) lopettaa_puhelu_toimi = BACK_ARVO(lopettaa_puhelu_toimi);
        단말.Kirjoitus("\r\u001b["); 단말.numero(komentorivi ? 16 : 7); 단말.Kirjoitus("G\u001b[K");
        if (alku_ikkuna > 0) 단말.문자('<');
        for (int Loop_INDEKSI = alku_ikkuna; Loop_INDEKSI < lopettaa_puhelu_toimi; Loop_INDEKSI++) Taulu.직렬쓰기(명령해석기.syöterivi[Loop_INDEKSI]);
        단말.문자(lopettaa_puhelu_toimi < Koko ? '>' : ' ');
        단말.Kirjoitus("\u001b["); 단말.numero(폭(kohdistin_ARVO, lopettaa_puhelu_toimi) + 1); 단말.문자('D');
        가로보기 = alku_ikkuna > 0 || lopettaa_puhelu_toimi < Koko || 폭(0, Koko) > 보이는폭();
    }
    static void liitä_LOG() {
        if (!komentorivi || Koko == 0 || Koko > 1024) return;
        if (LOG_LASKE > 0) {
            int 마지막자리 = (LOG_TIETUE_lopettaa_puhelu + 15) % 16; boolean 같은여부 = LOG_kesto[마지막자리] == Koko;
            for (int Loop_INDEKSI = 0; 같은여부 && Loop_INDEKSI < Koko; Loop_INDEKSI++) if (LOG_TIETUE[마지막자리 * 1024 + Loop_INDEKSI] != 명령해석기.syöterivi[Loop_INDEKSI]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_kesto[LOG_TIETUE_lopettaa_puhelu] = Koko; for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) LOG_TIETUE[LOG_TIETUE_lopettaa_puhelu * 1024 + Loop_INDEKSI] = 명령해석기.syöterivi[Loop_INDEKSI];
        LOG_TIETUE_lopettaa_puhelu = (LOG_TIETUE_lopettaa_puhelu + 1) % 16; if (LOG_LASKE < 16) LOG_LASKE++;
    }
    static void 기록이동(int SAMA_ARVO_ARVO) {
        if (!komentorivi) return;
        if (Hae_ARVO == 0 && SAMA_ARVO_ARVO > 0) { 저장길이 = Koko; for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) Store_ARVO[Loop_INDEKSI] = 명령해석기.syöterivi[Loop_INDEKSI]; }
        int Seuraava_toimi = Hae_ARVO + SAMA_ARVO_ARVO; if (Seuraava_toimi < 0 || Seuraava_toimi > LOG_LASKE) return; Hae_ARVO = Seuraava_toimi;
        if (Hae_ARVO == 0) { Koko = 저장길이; for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) 명령해석기.syöterivi[Loop_INDEKSI] = Store_ARVO[Loop_INDEKSI]; }
        else { int 보관칸 = (LOG_TIETUE_lopettaa_puhelu + 16 - Hae_ARVO) % 16; Koko = LOG_kesto[보관칸]; for (int Loop_INDEKSI = 0; Loop_INDEKSI < Koko; Loop_INDEKSI++) 명령해석기.syöterivi[Loop_INDEKSI] = LOG_TIETUE[보관칸 * 1024 + Loop_INDEKSI]; }
        kohdistin_ARVO = Koko; yrittää_uudelleen_ARVO();
    }
    static void näyttää_LOG() {
        for (int merkintä_LASKE = 0; merkintä_LASKE < LOG_LASKE; merkintä_LASKE++) {
            int 보관칸 = (LOG_TIETUE_lopettaa_puhelu + 16 - LOG_LASKE + merkintä_LASKE) % 16; 단말.numero(merkintä_LASKE + 1); 단말.Kirjoitus("  ");
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < LOG_kesto[보관칸]; Loop_INDEKSI++) Taulu.직렬쓰기(LOG_TIETUE[보관칸 * 1024 + Loop_INDEKSI]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] data_MATRIISI, int alku_toimi, int merkintä_LASKE, int 접두말, int summa_LASKE, boolean Directory_numero) {
        if (merkintä_LASKE < summa_LASKE || merkintä_LASKE > 62) return;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < summa_LASKE; Loop_INDEKSI++) if (data_MATRIISI[alku_toimi + Loop_INDEKSI] != 명령해석기.syöterivi[접두말 + Loop_INDEKSI]) return;
        후보수++; 후보길이 = merkintä_LASKE + 1;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) 후보[Loop_INDEKSI] = data_MATRIISI[alku_toimi + Loop_INDEKSI]; 후보[merkintä_LASKE] = Directory_numero ? '/' : ' ';
    }
    static void valmis_ARVO() {
        if (!komentorivi || kohdistin_ARVO != Koko) return;
        int 시작점 = Koko; while (시작점 > 0 && 명령해석기.syöterivi[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEKSI = 시작점; Loop_INDEKSI < Koko; Loop_INDEKSI++) if (명령해석기.syöterivi[Loop_INDEKSI] == '/' || 명령해석기.syöterivi[Loop_INDEKSI] == '"' || 명령해석기.syöterivi[Loop_INDEKSI] == 39 || 명령해석기.syöterivi[Loop_INDEKSI] == '\\') return;
        후보수 = 0; int merkintä_LASKE = Koko - 시작점;
        if (시작점 == 0) {
            for(int luetteloindeksi=0;luetteloindeksi<2;luetteloindeksi++) {
                String merkintä_luettelo=luetteloindeksi==0?명령들:관리명령.valmis_Word();
                int lukea_kohdistin=0;
                while(lukea_kohdistin<merkintä_luettelo.length()) {
                    int lopettaa_puhelu_toimi=lukea_kohdistin;while(lopettaa_puhelu_toimi<merkintä_luettelo.length() && merkintä_luettelo.charAt(lopettaa_puhelu_toimi)!=' ')lopettaa_puhelu_toimi++;
                    명령후보넣기(merkintä_luettelo,lukea_kohdistin,lopettaa_puhelu_toimi,merkintä_LASKE);lukea_kohdistin=lopettaa_puhelu_toimi+1;
                }
            }
        } else {
            Muisti_Files.polku_alku(1); Muisti_Files.polku_tavu(0, '.'); Muisti_Files.normalisoida_ARVO();
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < Muisti_Files.Tiedosto_LASKE; Loop_INDEKSI++) {
                int alku_toimi = Muisti_Files.merkintä_alku(Muisti_Files.Nimi, Loop_INDEKSI * 64, Muisti_Files.이름길이[Loop_INDEKSI]);
                if (alku_toimi >= 0) 후보넣기(Muisti_Files.Nimi, Loop_INDEKSI * 64 + alku_toimi, Muisti_Files.이름길이[Loop_INDEKSI] - alku_toimi, 시작점, merkintä_LASKE, false);
            }
            for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) {
                int alku_toimi = Muisti_Files.merkintä_alku(Muisti_Files.Directory_nimi, Loop_INDEKSI * 64, Muisti_Files.Directory_kesto[Loop_INDEKSI]);
                if (alku_toimi >= 0) 후보넣기(Muisti_Files.Directory_nimi, Loop_INDEKSI * 64 + alku_toimi, Muisti_Files.Directory_kesto[Loop_INDEKSI] - alku_toimi, 시작점, merkintä_LASKE, true);
            }
        }
        if (후보수 != 1) { Taulu.직렬쓰기(7); return; }
        for (int Loop_INDEKSI = merkintä_LASKE; Loop_INDEKSI < 후보길이 && Koko < 명령해석기.syöterivi.length - 1; Loop_INDEKSI++) {
            if (후보[Loop_INDEKSI] == ' ' && Loop_INDEKSI != 후보길이 - 1) 명령해석기.syöterivi[Koko++] = '\\';
            명령해석기.syöterivi[Koko++] = 후보[Loop_INDEKSI];
        }
        kohdistin_ARVO = Koko; yrittää_uudelleen_ARVO();
    }
    static int 탈출읽기() {
        int 시작점 = Taulu.밀리초();
        while (Taulu.밀리초() - 시작점 < 80) { int tavu_data = Taulu.직렬읽기(); if (tavu_data >= 0) return tavu_data; Taulu.TUOTTO_suoritin(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int merkintä_LASKE = 0, lopettaa_puhelu_toimi = -1;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 12; Loop_INDEKSI++) { int tavu_data = 탈출읽기(); if (tavu_data < 0) return; if (tavu_data >= '0' && tavu_data <= '9') merkintä_LASKE = merkintä_LASKE * 10 + tavu_data - '0'; else { lopettaa_puhelu_toimi = tavu_data; break; } }
        if (lopettaa_puhelu_toimi == 'A') 기록이동(1);
        else if (lopettaa_puhelu_toimi == 'B') 기록이동(-1);
        else if (lopettaa_puhelu_toimi == 'C') { kohdistin_ARVO = BACK_ARVO(kohdistin_ARVO); yrittää_uudelleen_ARVO(); }
        else if (lopettaa_puhelu_toimi == 'D') { kohdistin_ARVO = etukamera_ARVO(kohdistin_ARVO); yrittää_uudelleen_ARVO(); }
        else if (lopettaa_puhelu_toimi == 'H' || lopettaa_puhelu_toimi == '~' && (merkintä_LASKE == 1 || merkintä_LASKE == 7)) { kohdistin_ARVO = 0; yrittää_uudelleen_ARVO(); }
        else if (lopettaa_puhelu_toimi == 'F' || lopettaa_puhelu_toimi == '~' && (merkintä_LASKE == 4 || merkintä_LASKE == 8)) { kohdistin_ARVO = Koko; yrittää_uudelleen_ARVO(); }
        else if (lopettaa_puhelu_toimi == '~' && merkintä_LASKE == 3 && kohdistin_ARVO < Koko) {
            int Seuraava_toimi = BACK_ARVO(kohdistin_ARVO); for (int Loop_INDEKSI = Seuraava_toimi; Loop_INDEKSI < Koko; Loop_INDEKSI++) 명령해석기.syöterivi[Loop_INDEKSI - Seuraava_toimi + kohdistin_ARVO] = 명령해석기.syöterivi[Loop_INDEKSI]; Koko -= Seuraava_toimi - kohdistin_ARVO; yrittää_uudelleen_ARVO();
        }
        else if (lopettaa_puhelu_toimi == '~' && (merkintä_LASKE == 5 || merkintä_LASKE == 6)) Taulu.komentotulkki(merkintä_LASKE == 5 ? 5 : 6);
        else if (lopettaa_puhelu_toimi == '~' && merkintä_LASKE == 24 && komentorivi) { 명령해석기.komentotulkki(true); }
    }
    static int Luku() {
        if (!ikkuna_istunto.이어읽기) { Koko = kohdistin_ARVO = Hae_ARVO = alku_ikkuna = 0; 가로보기 = false; }
        else { ikkuna_istunto.이어읽기 = false; yrittää_uudelleen_ARVO(); } boolean ylivuoto = false;
        while (true) {
            int tavu_data = Taulu.직렬읽기(); if (tavu_data == -4096) return -3;
            if (Taulu.komentotulkki(14) != 0) yrittää_uudelleen_ARVO(); if (tavu_data < 0) { Taulu.TUOTTO_suoritin(); continue; }
            if (tavu_data == 10 && 명령해석기.Edellinen_rivi) { 명령해석기.Edellinen_rivi = false; continue; } 명령해석기.Edellinen_rivi = tavu_data == 13;
            if (tavu_data == 27) { 탈출(); continue; }
            if (tavu_data == 3) { 단말.Kirjoitus("^C\n"); return -1; }
            if (tavu_data == 4 && Koko == 0 && komentorivi) { if (Taulu.komentotulkki(2) != 0) 명령해석기.komentotulkki(true); return -1; }
            if (tavu_data == 13 || tavu_data == 10) { 단말.문자(10); if (!ylivuoto) liitä_LOG(); return ylivuoto ? -2 : Koko; }
            if (tavu_data == 9 && komentorivi) { valmis_ARVO(); continue; }
            if (tavu_data == 1 || tavu_data == 5) { kohdistin_ARVO = tavu_data == 1 ? 0 : Koko; yrittää_uudelleen_ARVO(); continue; }
            if (tavu_data == 8 || tavu_data == 127 || tavu_data == 21) {
                if (tavu_data == 21) { for (int Loop_INDEKSI = kohdistin_ARVO; Loop_INDEKSI < Koko; Loop_INDEKSI++) 명령해석기.syöterivi[Loop_INDEKSI - kohdistin_ARVO] = 명령해석기.syöterivi[Loop_INDEKSI]; Koko -= kohdistin_ARVO; kohdistin_ARVO = 0; }
                else if (kohdistin_ARVO > 0) { int 변경전 = etukamera_ARVO(kohdistin_ARVO); for (int Loop_INDEKSI = kohdistin_ARVO; Loop_INDEKSI < Koko; Loop_INDEKSI++) 명령해석기.syöterivi[Loop_INDEKSI - kohdistin_ARVO + 변경전] = 명령해석기.syöterivi[Loop_INDEKSI]; Koko -= kohdistin_ARVO - 변경전; kohdistin_ARVO = 변경전; }
                yrittää_uudelleen_ARVO(); continue;
            }
            if (tavu_data == 11) { Koko = kohdistin_ARVO; yrittää_uudelleen_ARVO(); continue; }
            if (tavu_data < 32 && tavu_data != 9) continue;
            if (Koko == 명령해석기.syöterivi.length) { ylivuoto = true; continue; }
            for (int Loop_INDEKSI = Koko; Loop_INDEKSI > kohdistin_ARVO; Loop_INDEKSI--) 명령해석기.syöterivi[Loop_INDEKSI] = 명령해석기.syöterivi[Loop_INDEKSI - 1];
            명령해석기.syöterivi[kohdistin_ARVO++] = tavu_data; Koko++;
            if (kohdistin_ARVO == Koko && !가로보기 && 폭(0, Koko) <= 보이는폭()) Taulu.직렬쓰기(tavu_data);
            else if (kohdistin_ARVO == Koko) 보이는줄(); else yrittää_uudelleen_ARVO();
        }
    }
}
