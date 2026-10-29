// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Failas 64개, 파일당 16384바이트, 서술자 16개. 모든 duomenys/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 KLAIDA 번호다.
 */
public final class atmintis_Failai {
    static final int Failas_COUNT = 64;
    static int[] Pavadinimas_2 = new int[Failas_COUNT * 64];
    static int[] 이름길이 = new int[Failas_COUNT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Turinys_VALUE = new int[Failas_COUNT * 4096];
    static int[] 길이 = new int[Failas_COUNT];
    static int[] nuoroda_COUNT = new int[Failas_COUNT];
    static int[] naudoti_VALUE = new int[16];
    static int[] tikslas = new int[16];
    static int[] Pozicija = new int[16];
    static int[] metodas_MODE = new int[16];
    static int[] KELIAS = new int[64];
    static int 경로길이;

    public static int 파일한도() { return Failas_COUNT; }
    static int 자료읽기(int Failas, int vietos_rodyklė) { return (Turinys_VALUE[Failas * 4096 + vietos_rodyklė / 4] >>> ((vietos_rodyklė & 3) * 8)) & 255; }
    static void rašymas_duomenys(int Failas, int vietos_rodyklė, int VALUE) {
        int 칸 = Failas * 4096 + vietos_rodyklė / 4, judėti_VALUE = (vietos_rodyklė & 3) * 8;
        Turinys_VALUE[칸] = (Turinys_VALUE[칸] & ~(255 << judėti_VALUE)) | ((VALUE & 255) << judėti_VALUE);
    }

    public static int kelias_Start(int Dydis) {
        경로길이 = 0;
        if (Dydis < 1 || Dydis > 63) return -36;
        경로길이 = Dydis;
        for (int Loop_INDEX = 0; Loop_INDEX < Dydis; Loop_INDEX++) KELIAS[Loop_INDEX] = 0;
        return 0;
    }
    public static int kelias_baitas(int INDEX, int VALUE) {
        if (INDEX < 0 || INDEX >= 경로길이 || VALUE < 1 || VALUE > 255) return -22;
        KELIAS[INDEX] = VALUE; return 0;
    }
    static int FIND_įrašas() {
        for (int Failas_INDEX = 0; Failas_INDEX < Failas_COUNT; Failas_INDEX++) if (이름길이[Failas_INDEX] > 0 && 이름길이[Failas_INDEX] == 정규길이 && 접두(Pavadinimas_2, Failas_INDEX * 64, 이름길이[Failas_INDEX], 정규, 정규길이)) return Failas_INDEX;
        return -1;
    }
    public static int Atverti(int 플래그) {
        if (경로길이 == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < 경로길이; Loop_INDEX++) if (KELIAS[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int REZULTATAS = normalizuoti_VALUE(); if (REZULTATAS < 0) return REZULTATAS;
        if (FIND_Katalogas(정규길이) >= 0) return -21;
        REZULTATAS = čekis_pirminis(); if (REZULTATAS < 0) return REZULTATAS;
        int Failas = FIND_įrašas();
        if (Failas >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Failas < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (naudoti_VALUE[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Failas < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < Failas_COUNT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && nuoroda_COUNT[Loop_INDEX] == 0) { Failas = Loop_INDEX; break; }
            if (Failas < 0) return -28;
            이름길이[Failas] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Pavadinimas_2[Failas * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            길이[Failas] = 0;
        }
        if ((플래그 & 0x200) != 0) 길이[Failas] = 0;
        naudoti_VALUE[서술자] = 1; tikslas[서술자] = Failas; Pozicija[서술자] = 0; metodas_MODE[서술자] = 플래그;
        nuoroda_COUNT[Failas]++;
        return 서술자 + 3;
    }
    static int patvirtinti(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && naudoti_VALUE[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Skaitymas(int 서술자) {
        int 칸 = patvirtinti(서술자);
        if (칸 < 0 || (metodas_MODE[칸] & 3) == 1) return -9;
        int Failas = tikslas[칸];
        if (Pozicija[칸] >= 길이[Failas]) return 256; // EOF와 faktinis_duomenys 0x00..0xff 구별
        return 자료읽기(Failas, Pozicija[칸]++);
    }
    public static int Rašymas(int 서술자, int VALUE) {
        int 칸 = patvirtinti(서술자);
        if (칸 < 0 || (metodas_MODE[칸] & 3) == 0) return -9;
        int Failas = tikslas[칸];
        if ((metodas_MODE[칸] & 0x400) != 0) Pozicija[칸] = 길이[Failas];
        if (Pozicija[칸] >= 16384) return -28;
        while (길이[Failas] < Pozicija[칸]) rašymas_duomenys(Failas, 길이[Failas]++, 0);
        rašymas_duomenys(Failas, Pozicija[칸]++, VALUE);
        if (길이[Failas] < Pozicija[칸]) 길이[Failas] = Pozicija[칸];
        return 1;
    }
    public static int ieškoti_padėtis(int 서술자, int 거리, int Project_šaknis) {
        int 칸 = patvirtinti(서술자);
        if (칸 < 0) return -9;
        if (Project_šaknis < 0 || Project_šaknis > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_šaknis == 0 ? 0 : Project_šaknis == 1 ? Pozicija[칸] : 길이[tikslas[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Pozicija[칸] = 새위치; return 새위치;
    }
    public static int Užverti(int 서술자) {
        int 칸 = patvirtinti(서술자);
        if (칸 < 0) return -9;
        nuoroda_COUNT[tikslas[칸]]--; naudoti_VALUE[칸] = 0; return 0;
    }
    public static int Dydis(int 서술자) {
        int 칸 = patvirtinti(서술자); return 칸 < 0 ? -9 : 길이[tikslas[칸]];
    }
    public static int 길이정하기(int 서술자, int Dydis) {
        int 칸 = patvirtinti(서술자);
        if (칸 < 0 || (metodas_MODE[칸] & 3) == 0) return -9;
        if (Dydis < 0 || Dydis > 16384) return -22;
        int Failas = tikslas[칸];
        while (길이[Failas] < Dydis) rašymas_duomenys(Failas, 길이[Failas]++, 0);
        길이[Failas] = Dydis; return 0;
    }
    public static int ištrinti_įrašas() {
        if (경로길이 == 0) return -22;
        int REZULTATAS = normalizuoti_VALUE(); if (REZULTATAS < 0) return REZULTATAS;
        if (FIND_Katalogas(정규길이) >= 0) return -21;
        REZULTATAS = čekis_pirminis(); if (REZULTATAS < 0) return REZULTATAS;
        int Failas = FIND_įrašas();
        if (Failas < 0) return -2;
        이름길이[Failas] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void įrašas_Sąrašas() {
        kelias_Start(1); kelias_baitas(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= Failas_COUNT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Pavadinimas_2[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int vietos_rodyklė) {
        return INDEX >= 0 && INDEX < Failas_COUNT && vietos_rodyklė >= 0 && vietos_rodyklė < 이름길이[INDEX] ? Pavadinimas_2[INDEX * 64 + vietos_rodyklė] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < Failas_COUNT ? 길이[INDEX] : -22; }
    static int[] 정규 = new int[64], dabartinis_prekė = new int[64], Katalogas_pavadinimas = new int[16 * 64], 폴더길이 = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Paleisti, int kelias_VALUE, int[] priekinis_VALUE, int eilučių_intervalas_kelias) {
        if (kelias_VALUE < eilučių_intervalas_kelias) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < eilučių_intervalas_kelias; Loop_INDEX++) if (이름들[Paleisti + Loop_INDEX] != priekinis_VALUE[Loop_INDEX]) return false;
        return true;
    }
    static int normalizuoti_VALUE() {
        if (경로길이 == 0) return -22;
        정규길이 = KELIAS[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = dabartinis_prekė[Loop_INDEX];
        int 읽는자리 = 0;
        while (읽는자리 < 경로길이) {
            while (읽는자리 < 경로길이 && KELIAS[읽는자리] == '/') 읽는자리++;
            int Start_padėtis = 읽는자리; while (읽는자리 < 경로길이 && KELIAS[읽는자리] != '/') { if (KELIAS[읽는자리] == 0) return -22; 읽는자리++; }
            int įrašas_COUNT = 읽는자리 - Start_padėtis; if (įrašas_COUNT == 0 || įrašas_COUNT == 1 && KELIAS[Start_padėtis] == '.') continue;
            if (įrašas_COUNT == 2 && KELIAS[Start_padėtis] == '.' && KELIAS[Start_padėtis + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + įrašas_COUNT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Start_padėtis; Loop_INDEX < 읽는자리; Loop_INDEX++) 정규[정규길이++] = KELIAS[Loop_INDEX];
        }
        return 0;
    }
    static int FIND_Katalogas(int įrašas_COUNT) {
        if (įrašas_COUNT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == įrašas_COUNT && 접두(Katalogas_pavadinimas, Loop_INDEX * 64, įrašas_COUNT, 정규, įrašas_COUNT)) return Loop_INDEX;
        return -1;
    }
    static int čekis_pirminis() {
        int įrašas_COUNT = 정규길이; while (įrašas_COUNT > 0 && 정규[įrašas_COUNT - 1] != '/') įrašas_COUNT--;
        return FIND_Katalogas(įrašas_COUNT == 0 ? 0 : įrašas_COUNT - 1) < 0 ? -2 : 0;
    }
    public static int kurti_Katalogas() {
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Katalogas(정규길이) >= 0 || FIND_įrašas() >= 0) return -17;
        처리값 = čekis_pirminis(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (폴더길이[Loop_INDEX] == 0) {
            폴더길이[Loop_INDEX] = 정규길이; for (int vidinis_padėtis = 0; vidinis_padėtis < 정규길이; vidinis_padėtis++) Katalogas_pavadinimas[Loop_INDEX * 64 + vidinis_padėtis] = 정규[vidinis_padėtis]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Katalogas(정규길이) >= 0) return 2;
        return FIND_įrašas() >= 0 ? 1 : 0;
    }
    public static int keisti_Katalogas() {
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Katalogas(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) dabartinis_prekė[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int pašalinti_Katalogas() {
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        int Katalogas_numeris = FIND_Katalogas(정규길이); if (Katalogas_numeris < 0) return -2; if (Katalogas_numeris == 0) return -16;
        if (현재길이 == 정규길이 && 접두(dabartinis_prekė, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < Failas_COUNT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Pavadinimas_2, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Pavadinimas_2[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (폴더길이[Loop_INDEX] > 정규길이 && 접두(Katalogas_pavadinimas, Loop_INDEX * 64, 폴더길이[Loop_INDEX], 정규, 정규길이) && Katalogas_pavadinimas[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        폴더길이[Katalogas_numeris] = 0; return 0;
    }
    public static int Pervardyti_įrašas(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Failas_COUNT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        if (FIND_Katalogas(정규길이) >= 0) return -21;
        처리값 = čekis_pirminis(); if (처리값 < 0) return 처리값;
        int 이전값 = FIND_įrašas(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Pavadinimas_2[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int įrašas_Start(int[] duomenys_ARRAY, int 시작점, int įrašas_COUNT) {
        if (!접두(duomenys_ARRAY, 시작점, įrašas_COUNT, 정규, 정규길이)) return -1;
        int Start_padėtis = 정규길이;
        if (Start_padėtis > 0) { if (įrašas_COUNT <= Start_padėtis || duomenys_ARRAY[시작점 + Start_padėtis] != '/') return -1; Start_padėtis++; }
        if (įrašas_COUNT <= Start_padėtis) return -1;
        for (int Loop_INDEX = Start_padėtis; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) if (duomenys_ARRAY[시작점 + Loop_INDEX] == '/') return -1;
        return Start_padėtis;
    }
    static void dabartinis_rašymas() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Lenta.직렬쓰기(dabartinis_prekė[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalizuoti_VALUE(); if (처리값 < 0) return 처리값;
        int Failas_tikslas = FIND_įrašas();
        if (Failas_tikslas >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Lenta.직렬쓰기(정규[Loop_INDEX]); 단말.Rašymas("  "); 단말.numeris(길이[Failas_tikslas]); 단말.Rašymas("baitas_VALUE(주기억 Failas)\n"); return 0; }
        if (FIND_Katalogas(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (폴더길이[뒷값] > 0) {
            int Start_padėtis = įrašas_Start(Katalogas_pavadinimas, 뒷값 * 64, 폴더길이[뒷값]); if (Start_padėtis < 0) continue;
            for (int Loop_INDEX = Start_padėtis; Loop_INDEX < 폴더길이[뒷값]; Loop_INDEX++) Lenta.직렬쓰기(Katalogas_pavadinimas[뒷값 * 64 + Loop_INDEX]); 단말.Rašymas("/\n");
        }
        for (int Failas_INDEX = 0; Failas_INDEX < Failas_COUNT; Failas_INDEX++) if (이름길이[Failas_INDEX] > 0) {
            int Start_padėtis = įrašas_Start(Pavadinimas_2, Failas_INDEX * 64, 이름길이[Failas_INDEX]); if (Start_padėtis < 0) continue;
            for (int Loop_INDEX = Start_padėtis; Loop_INDEX < 이름길이[Failas_INDEX]; Loop_INDEX++) Lenta.직렬쓰기(Pavadinimas_2[Failas_INDEX * 64 + Loop_INDEX]);
            단말.Rašymas("  "); 단말.numeris(길이[Failas_INDEX]); 단말.Rašymas("baitas_VALUE(주기억 Failas)\n");
        }
        return 0;
    }
}
