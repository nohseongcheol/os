// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 vuorovaikutteinen liittymä 문법. 파이프는 순차 Suorita_komento, 환경은 같은 셸에서 공유한다. */
public final class liittymä_syntaksi {
    static int[] lähdetiedosto = new int[4 * 4096], 종류 = new int[4 * 128], Suorita_2 = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] muuttuja_nimi = new int[16 * 32], muuttuja_data = new int[16 * 256], 이름길이 = new int[16], ARVO_kesto = new int[16];
    static int[] komentosarja_ARVO = new int[4 * 16384];
    static int Tila_ARVO, 깊이, 쓴수;
    static boolean 연결중, komentosarja_lopettaa_puhelu, tarkenne_virhe;
    static boolean nimi_merkki(int merkkikoodi) { return merkkikoodi >= 'a' && merkkikoodi <= 'z' || merkkikoodi >= 'A' && merkkikoodi <= 'Z' || merkkikoodi == '_' || merkkikoodi >= 128; }
    static boolean 이름뒤(int merkkikoodi) { return nimi_merkki(merkkikoodi) || merkkikoodi >= '0' && merkkikoodi <= '9'; }
    static void VIRHE(String teksti) { Taulu.입출력전환(0); 단말.Kirjoitus("komento jäsentää_ARVO: "); 단말.Kirjoitus(teksti); 단말.문자(10); Tila_ARVO = 2; }
    static int Luku(int merkintä_LASKE, int 중첩깊이) {
        int nykyinen_INDEKSI = 0, summa_LASKE = 0, PERUS_toimi = 중첩깊이 * 4096, erikoismerkki = 중첩깊이 * 128;
        while (nykyinen_INDEKSI < merkintä_LASKE) {
            while (nykyinen_INDEKSI < merkintä_LASKE && (lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == 32 || lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == 9)) nykyinen_INDEKSI++;
            if (nykyinen_INDEKSI == merkintä_LASKE || lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == '#') break;
            if (summa_LASKE == 128) { VIRHE("낱말이 너무 많습니다"); return -1; }
            int alku_toimi = nykyinen_INDEKSI, merkkikoodi = lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI], 자료종류 = 0;
            if (merkkikoodi == ';') { 자료종류 = 1; nykyinen_INDEKSI++; }
            else if (merkkikoodi == '&') { if (nykyinen_INDEKSI + 1 >= merkintä_LASKE || lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI + 1] != '&') { VIRHE("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; nykyinen_INDEKSI += 2; }
            else if (merkkikoodi == '|') { nykyinen_INDEKSI++; 자료종류 = nykyinen_INDEKSI < merkintä_LASKE && lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == '|' ? 3 : 4; if (자료종류 == 3) nykyinen_INDEKSI++; }
            else if (merkkikoodi == '>') { nykyinen_INDEKSI++; 자료종류 = nykyinen_INDEKSI < merkintä_LASKE && lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == '>' ? 6 : 5; if (자료종류 == 6) nykyinen_INDEKSI++; }
            else if (merkkikoodi == '<') { 자료종류 = 7; nykyinen_INDEKSI++; }
            else {
                int Lainaus = 0;
                while (nykyinen_INDEKSI < merkintä_LASKE) {
                    merkkikoodi = lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI];
                    if (merkkikoodi == '`' && Lainaus != 39 || merkkikoodi == '$' && Lainaus != 39 && nykyinen_INDEKSI + 1 < merkintä_LASKE && lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI + 1] == '(') { VIRHE("komento TULOS 치환은 지원하지 않습니다"); return -1; }
                    if (merkkikoodi == '\\' && Lainaus != 39) { if (++nykyinen_INDEKSI == merkintä_LASKE) { VIRHE("syöterivi 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } nykyinen_INDEKSI++; continue; }
                    if (merkkikoodi == Lainaus) { Lainaus = 0; nykyinen_INDEKSI++; continue; }
                    if (Lainaus == 0 && (merkkikoodi == 39 || merkkikoodi == 34)) { Lainaus = merkkikoodi; nykyinen_INDEKSI++; continue; }
                    if (Lainaus == 0 && (merkkikoodi == 32 || merkkikoodi == 9 || merkkikoodi == ';' || merkkikoodi == '&' || merkkikoodi == '|' || merkkikoodi == '<' || merkkikoodi == '>')) break;
                    nykyinen_INDEKSI++;
                }
                if (Lainaus != 0) { VIRHE("따옴표가 닫히지 않았습니다"); return -1; }
                if (nykyinen_INDEKSI < merkintä_LASKE && (lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == '>' || lähdetiedosto[PERUS_toimi + nykyinen_INDEKSI] == '<')) {
                    boolean 수치 = nykyinen_INDEKSI > alku_toimi;
                    for (int Loop_INDEKSI = alku_toimi; Loop_INDEKSI < nykyinen_INDEKSI; Loop_INDEKSI++) if (lähdetiedosto[PERUS_toimi + Loop_INDEKSI] < '0' || lähdetiedosto[PERUS_toimi + Loop_INDEKSI] > '9') 수치 = false;
                    if (수치) { VIRHE("번호를 지정한 tiedoston_nimi 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[erikoismerkki + summa_LASKE] = 자료종류; Suorita_2[erikoismerkki + summa_LASKE] = alku_toimi; 끝[erikoismerkki + summa_LASKE] = nykyinen_INDEKSI; summa_LASKE++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < summa_LASKE; Loop_INDEKSI++) {
            int 임시값 = 종류[erikoismerkki + Loop_INDEKSI];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEKSI == summa_LASKE || 종류[erikoismerkki + Loop_INDEKSI] != 0) { VIRHE("I_O 전환에 tiedoston_nimi 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEKSI == summa_LASKE - 1 && 임시값 != 1) { VIRHE("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (summa_LASKE > 0 && !낱말 && 종류[erikoismerkki + summa_LASKE - 1] != 1) { VIRHE("명령이 빠졌습니다"); return -1; }
        return summa_LASKE;
    }
    static boolean alue_SMS(int[] data_MATRIISI, int paikallinen_alku, int merkintä_LASKE, String merkki_toimi) {
        if (merkintä_LASKE != merkki_toimi.length()) return false; for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) if (data_MATRIISI[paikallinen_alku + Loop_INDEKSI] != merkki_toimi.charAt(Loop_INDEKSI)) return false; return true;
    }
    static void 넣기(int tavu_data) {
        if (쓴수 >= 명령해석기.tunnus_ARVO_eb540501.length) { if (!tarkenne_virhe) VIRHE("변수를 펼친 명령이 너무 깁니다"); tarkenne_virhe = true; return; }
        명령해석기.tunnus_ARVO_eb540501[쓴수++] = tavu_data;
    }
    static void muuttuja_ARVO(int[] data_MATRIISI, int alku_toimi, int merkintä_LASKE) {
        if (alue_SMS(data_MATRIISI, alku_toimi, merkintä_LASKE, "PWD")) { 넣기('/'); for (int Loop_INDEKSI = 0; Loop_INDEKSI < Muisti_Files.nykyinen_kesto; Loop_INDEKSI++) 넣기(Muisti_Files.nykyinen_kohde[Loop_INDEKSI]); return; }
        if (alue_SMS(data_MATRIISI, alku_toimi, merkintä_LASKE, "HOME")) { 넣기('/'); return; }
        if (alue_SMS(data_MATRIISI, alku_toimi, merkintä_LASKE, "?")) {
            int data_ARVO = Tila_ARVO, numero_2b3a32b5 = 100; boolean 시작여부 = false;
            while (numero_2b3a32b5 > 0) { int seuraava_ARVO = data_ARVO / numero_2b3a32b5; if (seuraava_ARVO != 0 || 시작여부 || numero_2b3a32b5 == 1) { 넣기('0' + seuraava_ARVO); 시작여부 = true; } data_ARVO %= numero_2b3a32b5; numero_2b3a32b5 /= 10; } return;
        }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) if (이름길이[Loop_INDEKSI] == merkintä_LASKE) {
            boolean VASTINE = true; for (int sisäliitos_toimi = 0; sisäliitos_toimi < merkintä_LASKE; sisäliitos_toimi++) if (muuttuja_nimi[Loop_INDEKSI * 32 + sisäliitos_toimi] != data_MATRIISI[alku_toimi + sisäliitos_toimi]) VASTINE = false;
            if (VASTINE) { for (int sisäliitos_toimi = 0; sisäliitos_toimi < ARVO_kesto[Loop_INDEKSI]; sisäliitos_toimi++) 넣기(muuttuja_data[Loop_INDEKSI * 256 + sisäliitos_toimi]); return; }
        }
    }
    static boolean Word_ARVO(int 낱말번호, int 중첩깊이) {
        int lukea_kohdistin = Suorita_2[중첩깊이 * 128 + 낱말번호], lopettaa_puhelu_toimi = 끝[중첩깊이 * 128 + 낱말번호], PERUS_toimi = 중첩깊이 * 4096, Lainaus = 0;
        if (lukea_kohdistin < lopettaa_puhelu_toimi && lähdetiedosto[PERUS_toimi + lukea_kohdistin] == '~' && (lukea_kohdistin + 1 == lopettaa_puhelu_toimi || lähdetiedosto[PERUS_toimi + lukea_kohdistin + 1] == '/')) { 넣기('/'); lukea_kohdistin++; }
        while (lukea_kohdistin < lopettaa_puhelu_toimi) {
            int merkkikoodi = lähdetiedosto[PERUS_toimi + lukea_kohdistin++];
            if (merkkikoodi == Lainaus) { Lainaus = 0; continue; }
            if (Lainaus == 0 && (merkkikoodi == 39 || merkkikoodi == 34)) { Lainaus = merkkikoodi; continue; }
            if (merkkikoodi == '\\' && Lainaus != 39) { int Seuraava_toimi = lähdetiedosto[PERUS_toimi + lukea_kohdistin++]; if (Lainaus == 34 && Seuraava_toimi != '$' && Seuraava_toimi != '"' && Seuraava_toimi != '\\') 넣기('\\'); 넣기(Seuraava_toimi); continue; }
            if (merkkikoodi == '$' && Lainaus != 39 && lukea_kohdistin < lopettaa_puhelu_toimi) {
                boolean 중괄호자리 = lähdetiedosto[PERUS_toimi + lukea_kohdistin] == '{'; if (중괄호자리) lukea_kohdistin++;
                int 처음자리 = lukea_kohdistin;
                if (lukea_kohdistin < lopettaa_puhelu_toimi && lähdetiedosto[PERUS_toimi + lukea_kohdistin] == '?') lukea_kohdistin++;
                else while (lukea_kohdistin < lopettaa_puhelu_toimi && 이름뒤(lähdetiedosto[PERUS_toimi + lukea_kohdistin])) lukea_kohdistin++;
                if (중괄호자리 && (lukea_kohdistin == lopettaa_puhelu_toimi || lähdetiedosto[PERUS_toimi + lukea_kohdistin] != '}')) { VIRHE("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (lukea_kohdistin == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                muuttuja_ARVO(lähdetiedosto, PERUS_toimi + 처음자리, lukea_kohdistin - 처음자리); if (중괄호자리) lukea_kohdistin++; continue;
            }
            넣기(merkkikoodi);
        }
        return !tarkenne_virhe;
    }
    static int ympäristö_Asetukset(int argumentti_INDEKSI, boolean poistaa) {
        int paikallinen_alku = 명령해석기.시작점[argumentti_INDEKSI], lopettaa_puhelu_toimi = paikallinen_alku + 명령해석기.kesto_ARVO[argumentti_INDEKSI], 같음자리 = paikallinen_alku;
        while (같음자리 < lopettaa_puhelu_toimi && 명령해석기.tunnus_ARVO_eb540501[같음자리] != '=') 같음자리++;
        int merkintä_LASKE = 같음자리 - paikallinen_alku;
        if (merkintä_LASKE < 1 || merkintä_LASKE > 31 || !nimi_merkki(명령해석기.tunnus_ARVO_eb540501[paikallinen_alku]) || !poistaa && 같음자리 == lopettaa_puhelu_toimi || lopettaa_puhelu_toimi - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEKSI = paikallinen_alku; Loop_INDEKSI < 같음자리; Loop_INDEKSI++) if (!이름뒤(명령해석기.tunnus_ARVO_eb540501[Loop_INDEKSI])) return 2;
        if (alue_SMS(명령해석기.tunnus_ARVO_eb540501, paikallinen_alku, merkintä_LASKE, "PWD") || alue_SMS(명령해석기.tunnus_ARVO_eb540501, paikallinen_alku, merkintä_LASKE, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) {
            if (이름길이[Loop_INDEKSI] == 0) 빈여부 = Loop_INDEKSI;
            if (이름길이[Loop_INDEKSI] != merkintä_LASKE) continue;
            boolean VASTINE = true; for (int sisäliitos_toimi = 0; sisäliitos_toimi < merkintä_LASKE; sisäliitos_toimi++) if (muuttuja_nimi[Loop_INDEKSI * 32 + sisäliitos_toimi] != 명령해석기.tunnus_ARVO_eb540501[paikallinen_alku + sisäliitos_toimi]) VASTINE = false;
            if (VASTINE) 찾은여부 = Loop_INDEKSI;
        }
        if (poistaa) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = merkintä_LASKE; ARVO_kesto[찾은여부] = lopettaa_puhelu_toimi - 같음자리 - 1;
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) muuttuja_nimi[찾은여부 * 32 + Loop_INDEKSI] = 명령해석기.tunnus_ARVO_eb540501[paikallinen_alku + Loop_INDEKSI];
        for (int Loop_INDEKSI = 같음자리 + 1; Loop_INDEKSI < lopettaa_puhelu_toimi; Loop_INDEKSI++) muuttuja_data[찾은여부 * 256 + Loop_INDEKSI - 같음자리 - 1] = 명령해석기.tunnus_ARVO_eb540501[Loop_INDEKSI];
        return 0;
    }
    static void näyttää_ympäristö() {
        단말.Kirjoitus("HOME=/\nPWD="); Muisti_Files.nykyinen_kirjoitus(); 단말.문자(10);
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < 16; Loop_INDEKSI++) if (이름길이[Loop_INDEKSI] > 0) {
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < 이름길이[Loop_INDEKSI]; sisäliitos_toimi++) Taulu.직렬쓰기(muuttuja_nimi[Loop_INDEKSI * 32 + sisäliitos_toimi]); 단말.문자('=');
            for (int sisäliitos_toimi = 0; sisäliitos_toimi < ARVO_kesto[Loop_INDEKSI]; sisäliitos_toimi++) Taulu.직렬쓰기(muuttuja_data[Loop_INDEKSI * 256 + sisäliitos_toimi]); 단말.문자(10);
        }
    }
    static void Suorita_komento(int[] data_MATRIISI, int 시작변위, int merkintä_LASKE, int 중첩깊이) {
        if (중첩깊이 >= 4 || merkintä_LASKE > 4096) { VIRHE("komento 파일의 sisäkkäistäminen_ARVO 또는 syöterivi kesto_ARVO 제한을 넘었습니다"); return; }
        for (int Loop_INDEKSI = 0; Loop_INDEKSI < merkintä_LASKE; Loop_INDEKSI++) lähdetiedosto[중첩깊이 * 4096 + Loop_INDEKSI] = data_MATRIISI[시작변위 + Loop_INDEKSI];
        int summa_LASKE = Luku(merkintä_LASKE, 중첩깊이); if (summa_LASKE < 0) return;
        int lukea_kohdistin = 0, 조건성립 = 1;
        while (lukea_kohdistin < summa_LASKE) {
            int Ryhmä_lopettaa_puhelu = lukea_kohdistin;
            while (Ryhmä_lopettaa_puhelu < summa_LASKE && (종류[중첩깊이 * 128 + Ryhmä_lopettaa_puhelu] == 0 || 종류[중첩깊이 * 128 + Ryhmä_lopettaa_puhelu] >= 4)) Ryhmä_lopettaa_puhelu++;
            boolean Suorita_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Tila_ARVO == 0 || 조건성립 == 3 && Tila_ARVO != 0;
            if (Suorita_cc685ae5) {
                boolean Edellinen_kohde_INDEKSI = false;
                while (lukea_kohdistin < Ryhmä_lopettaa_puhelu) {
                    int Seuraava_toimi = lukea_kohdistin; while (Seuraava_toimi < Ryhmä_lopettaa_puhelu && 종류[중첩깊이 * 128 + Seuraava_toimi] != 4) Seuraava_toimi++;
                    boolean YHDISTÄ_virta = Seuraava_toimi < Ryhmä_lopettaa_puhelu; int syöte_page = -1, tulos_page = -1, 출력방식 = 0;
                    명령해석기.tunnus_LASKE = 0; 쓴수 = 0; tarkenne_virhe = false;
                    for (int Loop_INDEKSI = lukea_kohdistin; Loop_INDEKSI < Seuraava_toimi; Loop_INDEKSI++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEKSI];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (syöte_page >= 0) { VIRHE("syöte_ARVO 전환이 겹쳤습니다"); return; } syöte_page = ++Loop_INDEKSI; } else { if (tulos_page >= 0) { VIRHE("tulostuspaikka 전환이 겹쳤습니다"); return; } tulos_page = ++Loop_INDEKSI; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.tunnus_LASKE == 32) { VIRHE("인수가 너무 많습니다"); return; }
                        int argumentti_INDEKSI = 명령해석기.tunnus_LASKE++; 명령해석기.시작점[argumentti_INDEKSI] = 쓴수;
                        if (!Word_ARVO(Loop_INDEKSI, 중첩깊이)) return;
                        명령해석기.kesto_ARVO[argumentti_INDEKSI] = 쓴수 - 명령해석기.시작점[argumentti_INDEKSI];
                    }
                    연결중 = Edellinen_kohde_INDEKSI || YHDISTÄ_virta || syöte_page >= 0 || tulos_page >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { VIRHE("vuorovaikutteinen 명령과 komento 파일은 I_O 전환이나 virta_ARVO 연결에 쓸 numero 없습니다"); return; }
                    셸입출력.Suorita_2(Edellinen_kohde_INDEKSI, YHDISTÄ_virta);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int merkintä_toimi = 입출력바꿈 == 0 ? syöte_page : tulos_page; if (merkintä_toimi < 0) continue;
                        int alku_toimi = 쓴수; if (!Word_ARVO(merkintä_toimi, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Muisti_Files.polku_alku(쓴수 - alku_toimi);
                        for (int sisäliitos_toimi = alku_toimi; 처리값 >= 0 && sisäliitos_toimi < 쓴수; sisäliitos_toimi++) 처리값 = Muisti_Files.polku_tavu(sisäliitos_toimi - alku_toimi, 명령해석기.tunnus_ARVO_eb540501[sisäliitos_toimi]);
                        if (처리값 >= 0) 처리값 = Muisti_Files.Avaa(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.VIRHE(처리값); Tila_ARVO = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.syötetiedosto = 처리값; else 셸입출력.kohdetiedosto_9ceb7bd4 = 처리값;
                    }
                    셸입출력.Salli_vuorovaikutteinen = 중첩깊이 == 0 && lukea_kohdistin == 0 && Seuraava_toimi == summa_LASKE;
                    깊이 = 중첩깊이; 명령해석기.TULOS = 0; Taulu.입출력전환(1);
                    명령해석기.komento();
                    Taulu.komentotulkki(3);
                    int 반환값 = 명령해석기.TULOS, virta_virhe = 셸입출력.virhe_ARVO;
                    셸입출력.끝(); 연결중 = false;
                    Tila_ARVO = virta_virhe < 0 ? 1 : 반환값;
                    if (virta_virhe < 0) { 명령해석기.VIRHE(virta_virhe); return; }
                    if (komentosarja_lopettaa_puhelu || 반환값 == -1005) return;
                    Edellinen_kohde_INDEKSI = true; lukea_kohdistin = Seuraava_toimi + 1;
                }
            }
            if (Ryhmä_lopettaa_puhelu < summa_LASKE) 조건성립 = 종류[중첩깊이 * 128 + Ryhmä_lopettaa_puhelu];
            lukea_kohdistin = Ryhmä_lopettaa_puhelu + 1;
        }
    }
    static void Suorita_Tiedosto() {
        if (명령해석기.tunnus_LASKE != 2 || 깊이 >= 3) { 명령해석기.TULOS = 2; 단말.Kirjoitus("사용법: sh tiedoston_nimi (sisäkkäistäminen_ARVO 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.polku_2(1); if (처리값 >= 0) 처리값 = Muisti_Files.Avaa(0);
        if (처리값 < 0) { 명령해석기.VIRHE(처리값); return; }
        int merkintä_LASKE = 0, tavu_data;
        while ((tavu_data = Muisti_Files.Luku(처리값)) != 256 && tavu_data >= 0 && merkintä_LASKE < 16384) komentosarja_ARVO[중첩깊이 * 16384 + merkintä_LASKE++] = tavu_data;
        Muisti_Files.Sulje(처리값); Taulu.입출력전환(0);
        for (int lukea_kohdistin = 0; lukea_kohdistin < merkintä_LASKE && !komentosarja_lopettaa_puhelu;) {
            int lopettaa_puhelu_toimi = lukea_kohdistin; while (lopettaa_puhelu_toimi < merkintä_LASKE && komentosarja_ARVO[중첩깊이 * 16384 + lopettaa_puhelu_toimi] != 10) lopettaa_puhelu_toimi++;
            int kelvollinen_kesto = lopettaa_puhelu_toimi - lukea_kohdistin; if (kelvollinen_kesto > 0 && komentosarja_ARVO[중첩깊이 * 16384 + lopettaa_puhelu_toimi - 1] == 13) kelvollinen_kesto--;
            Suorita_komento(komentosarja_ARVO, 중첩깊이 * 16384 + lukea_kohdistin, kelvollinen_kesto, 중첩깊이); lukea_kohdistin = lopettaa_puhelu_toimi + 1;
        }
        명령해석기.TULOS = Tila_ARVO; komentosarja_lopettaa_puhelu = false; 깊이 = 중첩깊이 - 1;
    }
}
