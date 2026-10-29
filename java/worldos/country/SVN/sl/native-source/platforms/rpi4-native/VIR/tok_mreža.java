// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** jedro_VALUE 안의 연결형 bajt_VALUE tok_VALUE. Ethernet/TCP 패킷 스택이 아닌 루프백 socket sloj_VALUE. */
public final class tok_mreža {
    static int[] stanje_VALUE = new int[16], vrata_VALUE = new int[16], 짝 = new int[16], enakovreden_vrata = new int[16], počakaj_VALUE = new int[16], informacijska_tehnologija_meja = new int[16];
    static int[] sprednja_VALUE = new int[16], 수 = new int[16], podatki = new int[16 * 1024];
    static int Naprej_element = 50000;
    static int 확인(int 열린파일번호) { return 열린파일번호 >= 40 && 열린파일번호 < 56 && stanje_VALUE[열린파일번호 - 40] != 0 ? 열린파일번호 - 40 : -1; }
    static boolean 사용중(int številka_vrat) { for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stanje_VALUE[Loop_INDEX] != 0 && informacijska_tehnologija_meja[Loop_INDEX] != 0 && vrata_VALUE[Loop_INDEX] == številka_vrat) return true; return false; }
    public static int Ustvari_vnos() {
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (stanje_VALUE[Loop_INDEX] == 0) { stanje_VALUE[Loop_INDEX] = 1; enakovreden_vrata[Loop_INDEX] = vrata_VALUE[Loop_INDEX] = sprednja_VALUE[Loop_INDEX] = 수[Loop_INDEX] = počakaj_VALUE[Loop_INDEX] = informacijska_tehnologija_meja[Loop_INDEX] = 0; 짝[Loop_INDEX] = -1; return Loop_INDEX + 40; }
        return -24;
    }
    public static int BIND_končna_točka(int 열린파일번호, int vtičnica_naslov, int številka_vrat) {
        int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (vtičnica_naslov != 0 && vtičnica_naslov != 0x7f000001) return -99;
        if (stanje_VALUE[Loop_INDEX] != 1 || številka_vrat < 0 || številka_vrat > 65535) return -22;
        if (številka_vrat == 0) { do { številka_vrat = Naprej_element++; if (Naprej_element > 65535) Naprej_element = 50000; } while (사용중(številka_vrat)); }
        if (사용중(številka_vrat)) return -98; vrata_VALUE[Loop_INDEX] = številka_vrat; informacijska_tehnologija_meja[Loop_INDEX] = 1; stanje_VALUE[Loop_INDEX] = 2; return 0;
    }
    public static int poslušati_končna_točka(int 열린파일번호, int 연결대기한도) { int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 2 || 연결대기한도 < 1) return -22; stanje_VALUE[Loop_INDEX] = 3; return 0; }
    public static int Poveži(int 열린파일번호, int vtičnica_naslov, int številka_vrat) {
        int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9; if (vtičnica_naslov != 0x7f000001) return -101;
        if (številka_vrat < 1 || številka_vrat > 65535 || stanje_VALUE[Loop_INDEX] > 2) return -22;
        int sprejeti_sprejemati_prejeti_prejemati_stran = -1; for (int notranje_položaj = 0; notranje_položaj < 16; notranje_položaj++) if (stanje_VALUE[notranje_položaj] == 3 && vrata_VALUE[notranje_položaj] == številka_vrat) sprejeti_sprejemati_prejeti_prejemati_stran = notranje_položaj;
        if (sprejeti_sprejemati_prejeti_prejemati_stran < 0) return -111;
        int 대기여부 = 0; for (int notranje_položaj = 0; notranje_položaj < 16; notranje_položaj++) if (počakaj_VALUE[notranje_položaj] == sprejeti_sprejemati_prejeti_prejemati_stran + 1) 대기여부++;
        if (대기여부 >= 4) return -11;
        if (stanje_VALUE[Loop_INDEX] == 1) { int 처리값 = BIND_končna_točka(열린파일번호, 0x7f000001, 0); if (처리값 < 0) return 처리값; }
        int Drugo = Ustvari_vnos(); if (Drugo < 0) return Drugo; Drugo -= 40;
        stanje_VALUE[Loop_INDEX] = stanje_VALUE[Drugo] = 4; 짝[Loop_INDEX] = Drugo; 짝[Drugo] = Loop_INDEX; vrata_VALUE[Drugo] = številka_vrat; enakovreden_vrata[Loop_INDEX] = številka_vrat; enakovreden_vrata[Drugo] = vrata_VALUE[Loop_INDEX]; počakaj_VALUE[Drugo] = sprejeti_sprejemati_prejeti_prejemati_stran + 1; return 0;
    }
    public static int sprejeti_povezava(int 열린파일번호) { int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 3) return -22; for (int notranje_položaj = 0; notranje_položaj < 16; notranje_položaj++) if (stanje_VALUE[notranje_položaj] != 0 && počakaj_VALUE[notranje_položaj] == Loop_INDEX + 1) { počakaj_VALUE[notranje_položaj] = 0; return notranje_položaj + 40; } return -11; }
    public static int Pisanje(int 열린파일번호, int vnos_COUNT) {
        int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 4) return -107;
        if (vnos_COUNT < 0 || vnos_COUNT > 512) return -22; if (vnos_COUNT == 0) return 0;
        int notranje_položaj = 짝[Loop_INDEX]; if (notranje_položaj < 0) return -32; int skupaj_COUNT = 1024 - 수[notranje_položaj]; if (skupaj_COUNT == 0) return -11; if (skupaj_COUNT > vnos_COUNT) skupaj_COUNT = vnos_COUNT;
        for (int Primerjava_položaj = 0; Primerjava_položaj < skupaj_COUNT; Primerjava_položaj++) podatki[notranje_položaj * 1024 + (sprednja_VALUE[notranje_položaj] + 수[notranje_položaj] + Primerjava_položaj) % 1024] = povratna_zanka_mreža.Naprej_VALUE[Primerjava_položaj]; 수[notranje_položaj] += skupaj_COUNT; return skupaj_COUNT;
    }
    public static int Branje(int 열린파일번호, int vnos_COUNT) {
        int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9; if (stanje_VALUE[Loop_INDEX] != 4) return -107; if (vnos_COUNT < 0 || vnos_COUNT > 512) return -22;
        if (vnos_COUNT == 0) return 0; if (수[Loop_INDEX] == 0) return 짝[Loop_INDEX] < 0 ? 0 : -11; if (vnos_COUNT > 수[Loop_INDEX]) vnos_COUNT = 수[Loop_INDEX];
        for (int Primerjava_položaj = 0; Primerjava_položaj < vnos_COUNT; Primerjava_položaj++) povratna_zanka_mreža.Naprej_VALUE[Primerjava_položaj] = podatki[Loop_INDEX * 1024 + (sprednja_VALUE[Loop_INDEX] + Primerjava_položaj) % 1024]; sprednja_VALUE[Loop_INDEX] = (sprednja_VALUE[Loop_INDEX] + vnos_COUNT) % 1024; 수[Loop_INDEX] -= vnos_COUNT; return vnos_COUNT;
    }
    public static int 창구읽기(int 열린파일번호) { int Loop_INDEX = 확인(열린파일번호); return Loop_INDEX < 0 ? -9 : vrata_VALUE[Loop_INDEX]; }
    public static int 상대창구읽기(int 열린파일번호) { int Loop_INDEX = 확인(열린파일번호); return Loop_INDEX < 0 ? -9 : enakovreden_vrata[Loop_INDEX]; }
    public static int Zapri(int 열린파일번호) {
        int Loop_INDEX = 확인(열린파일번호); if (Loop_INDEX < 0) return -9;
        if (stanje_VALUE[Loop_INDEX] == 3) for (int notranje_položaj = 0; notranje_položaj < 16; notranje_položaj++) if (počakaj_VALUE[notranje_položaj] == Loop_INDEX + 1) { if (짝[notranje_položaj] >= 0) 짝[짝[notranje_položaj]] = -1; stanje_VALUE[notranje_položaj] = počakaj_VALUE[notranje_položaj] = informacijska_tehnologija_meja[notranje_položaj] = 0; }
        if (짝[Loop_INDEX] >= 0) 짝[짝[Loop_INDEX]] = -1; stanje_VALUE[Loop_INDEX] = informacijska_tehnologija_meja[Loop_INDEX] = 수[Loop_INDEX] = počakaj_VALUE[Loop_INDEX] = 0; return 0;
    }
}
