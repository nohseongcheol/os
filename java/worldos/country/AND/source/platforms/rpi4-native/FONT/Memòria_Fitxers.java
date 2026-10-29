// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Fitxer 64개, 파일당 16384바이트, 서술자 16개. 모든 dades/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 s_ha_produït_un_error 번호다.
 */
public final class Memòria_Fitxers {
    static final int arxiu_COMPT = 64;
    static int[] Nom = new int[arxiu_COMPT * 64];
    static int[] 이름길이 = new int[arxiu_COMPT];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] contingut_VALOR = new int[arxiu_COMPT * 4096];
    static int[] durada_VALOR = new int[arxiu_COMPT];
    static int[] Referència_COMPT = new int[arxiu_COMPT];
    static int[] ús_VALOR = new int[16];
    static int[] objectiu = new int[16];
    static int[] Posició = new int[16];
    static int[] 방식 = new int[16];
    static int[] Camí = new int[64];
    static int camí_durada;

    public static int 파일한도() { return arxiu_COMPT; }
    static int tancar_dades(int Fitxer, int càrrec_INDEX) { return (contingut_VALOR[Fitxer * 4096 + càrrec_INDEX / 4] >>> ((càrrec_INDEX & 3) * 8)) & 255; }
    static void escriure_dades(int Fitxer, int càrrec_INDEX, int VALOR) {
        int 칸 = Fitxer * 4096 + càrrec_INDEX / 4, moure_VALOR = (càrrec_INDEX & 3) * 8;
        contingut_VALOR[칸] = (contingut_VALOR[칸] & ~(255 << moure_VALOR)) | ((VALOR & 255) << moure_VALOR);
    }

    public static int camí_Inici(int Mida) {
        camí_durada = 0;
        if (Mida < 1 || Mida > 63) return -36;
        camí_durada = Mida;
        for (int Loop_INDEX = 0; Loop_INDEX < Mida; Loop_INDEX++) Camí[Loop_INDEX] = 0;
        return 0;
    }
    public static int camí_byte(int INDEX, int VALOR) {
        if (INDEX < 0 || INDEX >= camí_durada || VALOR < 1 || VALOR > 255) return -22;
        Camí[INDEX] = VALOR; return 0;
    }
    static int BUSCA_introducció() {
        for (int arxiu_INDEX = 0; arxiu_INDEX < arxiu_COMPT; arxiu_INDEX++) if (이름길이[arxiu_INDEX] > 0 && 이름길이[arxiu_INDEX] == 정규길이 && 접두(Nom, arxiu_INDEX * 64, 이름길이[arxiu_INDEX], 정규, 정규길이)) return arxiu_INDEX;
        return -1;
    }
    public static int Obre(int 플래그) {
        if (camí_durada == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_INDEX = 0; Loop_INDEX < camí_durada; Loop_INDEX++) if (Camí[Loop_INDEX] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int RESULTAT = normalitzar_VALOR(); if (RESULTAT < 0) return RESULTAT;
        if (BUSCA_directori(정규길이) >= 0) return -21;
        RESULTAT = 부모확인(); if (RESULTAT < 0) return RESULTAT;
        int Fitxer = BUSCA_introducció();
        if (Fitxer >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Fitxer < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (ús_VALOR[Loop_INDEX] == 0) { 서술자 = Loop_INDEX; break; }
        if (서술자 < 0) return -24;
        if (Fitxer < 0) {
            for (int Loop_INDEX = 0; Loop_INDEX < arxiu_COMPT; Loop_INDEX++) if (이름길이[Loop_INDEX] == 0 && Referència_COMPT[Loop_INDEX] == 0) { Fitxer = Loop_INDEX; break; }
            if (Fitxer < 0) return -28;
            이름길이[Fitxer] = 정규길이;
            for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nom[Fitxer * 64 + Loop_INDEX] = 정규[Loop_INDEX];
            durada_VALOR[Fitxer] = 0;
        }
        if ((플래그 & 0x200) != 0) durada_VALOR[Fitxer] = 0;
        ús_VALOR[서술자] = 1; objectiu[서술자] = Fitxer; Posició[서술자] = 0; 방식[서술자] = 플래그;
        Referència_COMPT[Fitxer]++;
        return 서술자 + 3;
    }
    static int verificar(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && ús_VALOR[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lectura(int 서술자) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int Fitxer = objectiu[칸];
        if (Posició[칸] >= durada_VALOR[Fitxer]) return 256; // EOF와 real_dades 0x00..0xff 구별
        return tancar_dades(Fitxer, Posició[칸]++);
    }
    public static int Escriptura(int 서술자, int VALOR) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int Fitxer = objectiu[칸];
        if ((방식[칸] & 0x400) != 0) Posició[칸] = durada_VALOR[Fitxer];
        if (Posició[칸] >= 16384) return -28;
        while (durada_VALOR[Fitxer] < Posició[칸]) escriure_dades(Fitxer, durada_VALOR[Fitxer]++, 0);
        escriure_dades(Fitxer, Posició[칸]++, VALOR);
        if (durada_VALOR[Fitxer] < Posició[칸]) durada_VALOR[Fitxer] = Posició[칸];
        return 1;
    }
    public static int cercar_càrrec(int 서술자, int 거리, int Project_rel) {
        int 칸 = verificar(서술자);
        if (칸 < 0) return -9;
        if (Project_rel < 0 || Project_rel > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_rel == 0 ? 0 : Project_rel == 1 ? Posició[칸] : durada_VALOR[objectiu[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posició[칸] = 새위치; return 새위치;
    }
    public static int Tanca(int 서술자) {
        int 칸 = verificar(서술자);
        if (칸 < 0) return -9;
        Referència_COMPT[objectiu[칸]]--; ús_VALOR[칸] = 0; return 0;
    }
    public static int Mida(int 서술자) {
        int 칸 = verificar(서술자); return 칸 < 0 ? -9 : durada_VALOR[objectiu[칸]];
    }
    public static int conjunt_durada(int 서술자, int Mida) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (Mida < 0 || Mida > 16384) return -22;
        int Fitxer = objectiu[칸];
        while (durada_VALOR[Fitxer] < Mida) escriure_dades(Fitxer, durada_VALOR[Fitxer]++, 0);
        durada_VALOR[Fitxer] = Mida; return 0;
    }
    public static int esborrar_introducció() {
        if (camí_durada == 0) return -22;
        int RESULTAT = normalitzar_VALOR(); if (RESULTAT < 0) return RESULTAT;
        if (BUSCA_directori(정규길이) >= 0) return -21;
        RESULTAT = 부모확인(); if (RESULTAT < 0) return RESULTAT;
        int Fitxer = BUSCA_introducció();
        if (Fitxer < 0) return -2;
        이름길이[Fitxer] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void introducció_Llista() {
        camí_Inici(1); camí_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int INDEX) {
        if (INDEX < 0 || INDEX >= arxiu_COMPT || 이름길이[INDEX] == 0) return 0;
        for (int Loop_INDEX = 0; Loop_INDEX < 이름길이[INDEX]; Loop_INDEX++) if (Nom[INDEX * 64 + Loop_INDEX] == '/') return 0;
        return 이름길이[INDEX];
    }
    public static int 공개이름바이트(int INDEX, int càrrec_INDEX) {
        return INDEX >= 0 && INDEX < arxiu_COMPT && càrrec_INDEX >= 0 && càrrec_INDEX < 이름길이[INDEX] ? Nom[INDEX * 64 + càrrec_INDEX] : -22;
    }
    public static int 공개파일크기(int INDEX) { return INDEX >= 0 && INDEX < arxiu_COMPT ? durada_VALOR[INDEX] : -22; }
    static int[] 정규 = new int[64], 현재 = new int[64], directori_nom = new int[16 * 64], directori_durada = new int[16];
    static int 정규길이, 현재길이;
    static boolean 접두(int[] 이름들, int Executa_2, int camí_VALOR, int[] frontal_VALOR, int interlineat_camí) {
        if (camí_VALOR < interlineat_camí) return false;
        for (int Loop_INDEX = 0; Loop_INDEX < interlineat_camí; Loop_INDEX++) if (이름들[Executa_2 + Loop_INDEX] != frontal_VALOR[Loop_INDEX]) return false;
        return true;
    }
    static int normalitzar_VALOR() {
        if (camí_durada == 0) return -22;
        정규길이 = Camí[0] == '/' ? 0 : 현재길이;
        for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) 정규[Loop_INDEX] = 현재[Loop_INDEX];
        int tancar_cursor = 0;
        while (tancar_cursor < camí_durada) {
            while (tancar_cursor < camí_durada && Camí[tancar_cursor] == '/') tancar_cursor++;
            int Inici_càrrec = tancar_cursor; while (tancar_cursor < camí_durada && Camí[tancar_cursor] != '/') { if (Camí[tancar_cursor] == 0) return -22; tancar_cursor++; }
            int introducció_COMPT = tancar_cursor - Inici_càrrec; if (introducció_COMPT == 0 || introducció_COMPT == 1 && Camí[Inici_càrrec] == '.') continue;
            if (introducció_COMPT == 2 && Camí[Inici_càrrec] == '.' && Camí[Inici_càrrec + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + introducció_COMPT + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < tancar_cursor; Loop_INDEX++) 정규[정규길이++] = Camí[Loop_INDEX];
        }
        return 0;
    }
    static int BUSCA_directori(int introducció_COMPT) {
        if (introducció_COMPT == 0) return 0;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (directori_durada[Loop_INDEX] == introducció_COMPT && 접두(directori_nom, Loop_INDEX * 64, introducció_COMPT, 정규, introducció_COMPT)) return Loop_INDEX;
        return -1;
    }
    static int 부모확인() {
        int introducció_COMPT = 정규길이; while (introducció_COMPT > 0 && 정규[introducció_COMPT - 1] != '/') introducció_COMPT--;
        return BUSCA_directori(introducció_COMPT == 0 ? 0 : introducció_COMPT - 1) < 0 ? -2 : 0;
    }
    public static int Crear_directori() {
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        if (BUSCA_directori(정규길이) >= 0 || BUSCA_introducció() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_INDEX = 1; Loop_INDEX < 16; Loop_INDEX++) if (directori_durada[Loop_INDEX] == 0) {
            directori_durada[Loop_INDEX] = 정규길이; for (int interna_càrrec = 0; interna_càrrec < 정규길이; interna_càrrec++) directori_nom[Loop_INDEX * 64 + interna_càrrec] = 정규[interna_càrrec]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        if (BUSCA_directori(정규길이) >= 0) return 2;
        return BUSCA_introducció() >= 0 ? 1 : 0;
    }
    public static int canviar_directori() {
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        if (BUSCA_directori(정규길이) < 0) return -2;
        현재길이 = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) 현재[Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    public static int suprimir_directori() {
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        int 폴더번호 = BUSCA_directori(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (현재길이 == 정규길이 && 접두(현재, 0, 현재길이, 정규, 정규길이)) return -16;
        for (int Loop_INDEX = 0; Loop_INDEX < arxiu_COMPT; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] > 정규길이 && 접두(Nom, Loop_INDEX * 64, 이름길이[Loop_INDEX], 정규, 정규길이) && Nom[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (directori_durada[Loop_INDEX] > 정규길이 && 접두(directori_nom, Loop_INDEX * 64, directori_durada[Loop_INDEX], 정규, 정규길이) && directori_nom[Loop_INDEX * 64 + 정규길이] == '/') return -39;
        }
        directori_durada[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= arxiu_COMPT || 이름길이[원본번호] == 0) return -2;
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        if (BUSCA_directori(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = BUSCA_introducció(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Nom[원본번호 * 64 + Loop_INDEX] = 정규[Loop_INDEX]; return 0;
    }
    static int introducció_Inici(int[] dades_MATRIU, int 시작점, int introducció_COMPT) {
        if (!접두(dades_MATRIU, 시작점, introducció_COMPT, 정규, 정규길이)) return -1;
        int Inici_càrrec = 정규길이;
        if (Inici_càrrec > 0) { if (introducció_COMPT <= Inici_càrrec || dades_MATRIU[시작점 + Inici_càrrec] != '/') return -1; Inici_càrrec++; }
        if (introducció_COMPT <= Inici_càrrec) return -1;
        for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < introducció_COMPT; Loop_INDEX++) if (dades_MATRIU[시작점 + Loop_INDEX] == '/') return -1;
        return Inici_càrrec;
    }
    static void 현재쓰기() { 단말.문자('/'); for (int Loop_INDEX = 0; Loop_INDEX < 현재길이; Loop_INDEX++) Tauler.직렬쓰기(현재[Loop_INDEX]); }
    static int 경로목록() {
        int 처리값 = normalitzar_VALOR(); if (처리값 < 0) return 처리값;
        int arxiu_objectiu = BUSCA_introducció();
        if (arxiu_objectiu >= 0) { for (int Loop_INDEX = 0; Loop_INDEX < 정규길이; Loop_INDEX++) Tauler.직렬쓰기(정규[Loop_INDEX]); 단말.Escriptura("  "); 단말.수(durada_VALOR[arxiu_objectiu]); 단말.Escriptura("byte_VALOR(주기억 Fitxer)\n"); return 0; }
        if (BUSCA_directori(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (directori_durada[뒷값] > 0) {
            int Inici_càrrec = introducció_Inici(directori_nom, 뒷값 * 64, directori_durada[뒷값]); if (Inici_càrrec < 0) continue;
            for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < directori_durada[뒷값]; Loop_INDEX++) Tauler.직렬쓰기(directori_nom[뒷값 * 64 + Loop_INDEX]); 단말.Escriptura("/\n");
        }
        for (int arxiu_INDEX = 0; arxiu_INDEX < arxiu_COMPT; arxiu_INDEX++) if (이름길이[arxiu_INDEX] > 0) {
            int Inici_càrrec = introducció_Inici(Nom, arxiu_INDEX * 64, 이름길이[arxiu_INDEX]); if (Inici_càrrec < 0) continue;
            for (int Loop_INDEX = Inici_càrrec; Loop_INDEX < 이름길이[arxiu_INDEX]; Loop_INDEX++) Tauler.직렬쓰기(Nom[arxiu_INDEX * 64 + Loop_INDEX]);
            단말.Escriptura("  "); 단말.수(durada_VALOR[arxiu_INDEX]); 단말.Escriptura("byte_VALOR(주기억 Fitxer)\n");
        }
        return 0;
    }
}
