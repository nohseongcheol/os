// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** RAM Ficheiro 64개, 파일당 16384바이트, 서술자 16개. 모든 datos/정책은 Java에 있다.
 * 호출 도중 양보하지 않으므로 현재의 단일 코어 협력식 작업 사이에서 원자적이다.
 * 디스크 저장이나 POSIX 전체 구현을 뜻하지 않는다. 음수 반환은 ERRO 번호다.
 */
public final class Memoria_Ficheiros {
    static final int Ficheiro_CONTAR = 64;
    static int[] Nome = new int[Ficheiro_CONTAR * 64];
    static int[] 이름길이 = new int[Ficheiro_CONTAR];
    // Pack four bytes in each Java int, preserving the old content heap budget.
    static int[] Contido_VALOR = new int[Ficheiro_CONTAR * 4096];
    static int[] duración_VALOR = new int[Ficheiro_CONTAR];
    static int[] Material_de_referencia_CONTAR = new int[Ficheiro_CONTAR];
    static int[] 사용 = new int[16];
    static int[] obxectivo_VALOR = new int[16];
    static int[] Posición = new int[16];
    static int[] 방식 = new int[16];
    static int[] CAMIÑO = new int[64];
    static int camiño_duración;

    public static int 파일한도() { return Ficheiro_CONTAR; }
    static int 자료읽기(int Ficheiro, int cargo_ÍNDICE) { return (Contido_VALOR[Ficheiro * 4096 + cargo_ÍNDICE / 4] >>> ((cargo_ÍNDICE & 3) * 8)) & 255; }
    static void escribir_datos(int Ficheiro, int cargo_ÍNDICE, int VALOR) {
        int 칸 = Ficheiro * 4096 + cargo_ÍNDICE / 4, mover_VALOR = (cargo_ÍNDICE & 3) * 8;
        Contido_VALOR[칸] = (Contido_VALOR[칸] & ~(255 << mover_VALOR)) | ((VALOR & 255) << mover_VALOR);
    }

    public static int camiño_START(int Tamaño) {
        camiño_duración = 0;
        if (Tamaño < 1 || Tamaño > 63) return -36;
        camiño_duración = Tamaño;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Tamaño; Loop_ÍNDICE++) CAMIÑO[Loop_ÍNDICE] = 0;
        return 0;
    }
    public static int camiño_byte(int ÍNDICE, int VALOR) {
        if (ÍNDICE < 0 || ÍNDICE >= camiño_duración || VALOR < 1 || VALOR > 255) return -22;
        CAMIÑO[ÍNDICE] = VALOR; return 0;
    }
    static int Busca_introdución() {
        for (int Ficheiro_ÍNDICE = 0; Ficheiro_ÍNDICE < Ficheiro_CONTAR; Ficheiro_ÍNDICE++) if (이름길이[Ficheiro_ÍNDICE] > 0 && 이름길이[Ficheiro_ÍNDICE] == 정규길이 && 접두(Nome, Ficheiro_ÍNDICE * 64, 이름길이[Ficheiro_ÍNDICE], 정규, 정규길이)) return Ficheiro_ÍNDICE;
        return -1;
    }
    public static int Abrir(int 플래그) {
        if (camiño_duración == 0 || (플래그 & ~0x6c3) != 0 || (플래그 & 3) == 3) return -22;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < camiño_duración; Loop_ÍNDICE++) if (CAMIÑO[Loop_ÍNDICE] == 0) return -22;
        if ((플래그 & 0x200) != 0 && (플래그 & 3) == 0) return -22;
        int RESULTANTE = organizar_VALOR(); if (RESULTANTE < 0) return RESULTANTE;
        if (Busca_directorio(정규길이) >= 0) return -21;
        RESULTANTE = 부모확인(); if (RESULTANTE < 0) return RESULTANTE;
        int Ficheiro = Busca_introdución();
        if (Ficheiro >= 0 && (플래그 & 0xc0) == 0xc0) return -17;
        if (Ficheiro < 0 && (플래그 & 0x40) == 0) return -2;
        int 서술자 = -1;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (사용[Loop_ÍNDICE] == 0) { 서술자 = Loop_ÍNDICE; break; }
        if (서술자 < 0) return -24;
        if (Ficheiro < 0) {
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Ficheiro_CONTAR; Loop_ÍNDICE++) if (이름길이[Loop_ÍNDICE] == 0 && Material_de_referencia_CONTAR[Loop_ÍNDICE] == 0) { Ficheiro = Loop_ÍNDICE; break; }
            if (Ficheiro < 0) return -28;
            이름길이[Ficheiro] = 정규길이;
            for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 정규길이; Loop_ÍNDICE++) Nome[Ficheiro * 64 + Loop_ÍNDICE] = 정규[Loop_ÍNDICE];
            duración_VALOR[Ficheiro] = 0;
        }
        if ((플래그 & 0x200) != 0) duración_VALOR[Ficheiro] = 0;
        사용[서술자] = 1; obxectivo_VALOR[서술자] = Ficheiro; Posición[서술자] = 0; 방식[서술자] = 플래그;
        Material_de_referencia_CONTAR[Ficheiro]++;
        return 서술자 + 3;
    }
    static int verificar(int 서술자) {
        return 서술자 >= 3 && 서술자 < 19 && 사용[서술자 - 3] != 0 ? 서술자 - 3 : -1;
    }
    public static int Lectura(int 서술자) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 1) return -9;
        int Ficheiro = obxectivo_VALOR[칸];
        if (Posición[칸] >= duración_VALOR[Ficheiro]) return 256; // EOF와 real_datos 0x00..0xff 구별
        return 자료읽기(Ficheiro, Posición[칸]++);
    }
    public static int Escritura(int 서술자, int VALOR) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        int Ficheiro = obxectivo_VALOR[칸];
        if ((방식[칸] & 0x400) != 0) Posición[칸] = duración_VALOR[Ficheiro];
        if (Posición[칸] >= 16384) return -28;
        while (duración_VALOR[Ficheiro] < Posición[칸]) escribir_datos(Ficheiro, duración_VALOR[Ficheiro]++, 0);
        escribir_datos(Ficheiro, Posición[칸]++, VALOR);
        if (duración_VALOR[Ficheiro] < Posición[칸]) duración_VALOR[Ficheiro] = Posición[칸];
        return 1;
    }
    public static int buscar_cargo(int 서술자, int 거리, int Project_raíz) {
        int 칸 = verificar(서술자);
        if (칸 < 0) return -9;
        if (Project_raíz < 0 || Project_raíz > 2 || 거리 < -16384 || 거리 > 16384) return -22;
        int 새위치 = 거리 + (Project_raíz == 0 ? 0 : Project_raíz == 1 ? Posición[칸] : duración_VALOR[obxectivo_VALOR[칸]]);
        if (새위치 < 0 || 새위치 > 16384) return -22;
        Posición[칸] = 새위치; return 새위치;
    }
    public static int Pechar(int 서술자) {
        int 칸 = verificar(서술자);
        if (칸 < 0) return -9;
        Material_de_referencia_CONTAR[obxectivo_VALOR[칸]]--; 사용[칸] = 0; return 0;
    }
    public static int Tamaño(int 서술자) {
        int 칸 = verificar(서술자); return 칸 < 0 ? -9 : duración_VALOR[obxectivo_VALOR[칸]];
    }
    public static int conxunto_duración(int 서술자, int Tamaño) {
        int 칸 = verificar(서술자);
        if (칸 < 0 || (방식[칸] & 3) == 0) return -9;
        if (Tamaño < 0 || Tamaño > 16384) return -22;
        int Ficheiro = obxectivo_VALOR[칸];
        while (duración_VALOR[Ficheiro] < Tamaño) escribir_datos(Ficheiro, duración_VALOR[Ficheiro]++, 0);
        duración_VALOR[Ficheiro] = Tamaño; return 0;
    }
    public static int borrar_introdución() {
        if (camiño_duración == 0) return -22;
        int RESULTANTE = organizar_VALOR(); if (RESULTANTE < 0) return RESULTANTE;
        if (Busca_directorio(정규길이) >= 0) return -21;
        RESULTANTE = 부모확인(); if (RESULTANTE < 0) return RESULTANTE;
        int Ficheiro = Busca_introdución();
        if (Ficheiro < 0) return -2;
        이름길이[Ficheiro] = 0; return 0; // 열려 있는 파일은 마지막 close까지 유지
    }
    static void introdución_Lista() {
        camiño_START(1); camiño_byte(0, '.'); 경로목록();
    }
    public static int 공개이름길이(int ÍNDICE) {
        if (ÍNDICE < 0 || ÍNDICE >= Ficheiro_CONTAR || 이름길이[ÍNDICE] == 0) return 0;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 이름길이[ÍNDICE]; Loop_ÍNDICE++) if (Nome[ÍNDICE * 64 + Loop_ÍNDICE] == '/') return 0;
        return 이름길이[ÍNDICE];
    }
    public static int 공개이름바이트(int ÍNDICE, int cargo_ÍNDICE) {
        return ÍNDICE >= 0 && ÍNDICE < Ficheiro_CONTAR && cargo_ÍNDICE >= 0 && cargo_ÍNDICE < 이름길이[ÍNDICE] ? Nome[ÍNDICE * 64 + cargo_ÍNDICE] : -22;
    }
    public static int 공개파일크기(int ÍNDICE) { return ÍNDICE >= 0 && ÍNDICE < Ficheiro_CONTAR ? duración_VALOR[ÍNDICE] : -22; }
    static int[] 정규 = new int[64], ao_corrente_elemento = new int[64], directorio_nome = new int[16 * 64], directorio_duración = new int[16];
    static int 정규길이, ao_corrente_duración;
    static boolean 접두(int[] 이름들, int Executar_2, int camiño_VALOR, int[] frontal_VALOR, int espazamento_entre_liñas_camiño) {
        if (camiño_VALOR < espazamento_entre_liñas_camiño) return false;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < espazamento_entre_liñas_camiño; Loop_ÍNDICE++) if (이름들[Executar_2 + Loop_ÍNDICE] != frontal_VALOR[Loop_ÍNDICE]) return false;
        return true;
    }
    static int organizar_VALOR() {
        if (camiño_duración == 0) return -22;
        정규길이 = CAMIÑO[0] == '/' ? 0 : ao_corrente_duración;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 정규길이; Loop_ÍNDICE++) 정규[Loop_ÍNDICE] = ao_corrente_elemento[Loop_ÍNDICE];
        int 읽는자리 = 0;
        while (읽는자리 < camiño_duración) {
            while (읽는자리 < camiño_duración && CAMIÑO[읽는자리] == '/') 읽는자리++;
            int START_cargo = 읽는자리; while (읽는자리 < camiño_duración && CAMIÑO[읽는자리] != '/') { if (CAMIÑO[읽는자리] == 0) return -22; 읽는자리++; }
            int introdución_CONTAR = 읽는자리 - START_cargo; if (introdución_CONTAR == 0 || introdución_CONTAR == 1 && CAMIÑO[START_cargo] == '.') continue;
            if (introdución_CONTAR == 2 && CAMIÑO[START_cargo] == '.' && CAMIÑO[START_cargo + 1] == '.') {
                while (정규길이 > 0 && 정규[정규길이 - 1] != '/') 정규길이--;
                if (정규길이 > 0) 정규길이--;
                continue;
            }
            if (정규길이 + introdución_CONTAR + (정규길이 == 0 ? 0 : 1) > 63) return -36;
            if (정규길이 > 0) 정규[정규길이++] = '/';
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < 읽는자리; Loop_ÍNDICE++) 정규[정규길이++] = CAMIÑO[Loop_ÍNDICE];
        }
        return 0;
    }
    static int Busca_directorio(int introdución_CONTAR) {
        if (introdución_CONTAR == 0) return 0;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (directorio_duración[Loop_ÍNDICE] == introdución_CONTAR && 접두(directorio_nome, Loop_ÍNDICE * 64, introdución_CONTAR, 정규, introdución_CONTAR)) return Loop_ÍNDICE;
        return -1;
    }
    static int 부모확인() {
        int introdución_CONTAR = 정규길이; while (introdución_CONTAR > 0 && 정규[introdución_CONTAR - 1] != '/') introdución_CONTAR--;
        return Busca_directorio(introdución_CONTAR == 0 ? 0 : introdución_CONTAR - 1) < 0 ? -2 : 0;
    }
    public static int crear_directorio() {
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        if (Busca_directorio(정규길이) >= 0 || Busca_introdución() >= 0) return -17;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        for (int Loop_ÍNDICE = 1; Loop_ÍNDICE < 16; Loop_ÍNDICE++) if (directorio_duración[Loop_ÍNDICE] == 0) {
            directorio_duración[Loop_ÍNDICE] = 정규길이; for (int interna_cargo = 0; interna_cargo < 정규길이; interna_cargo++) directorio_nome[Loop_ÍNDICE * 64 + interna_cargo] = 정규[interna_cargo]; return 0;
        }
        return -28;
    }
    public static int 항목종류() {
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        if (Busca_directorio(정규길이) >= 0) return 2;
        return Busca_introdución() >= 0 ? 1 : 0;
    }
    public static int modificar_directorio() {
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        if (Busca_directorio(정규길이) < 0) return -2;
        ao_corrente_duración = 정규길이; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < ao_corrente_duración; Loop_ÍNDICE++) ao_corrente_elemento[Loop_ÍNDICE] = 정규[Loop_ÍNDICE]; return 0;
    }
    public static int eliminar_directorio() {
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        int 폴더번호 = Busca_directorio(정규길이); if (폴더번호 < 0) return -2; if (폴더번호 == 0) return -16;
        if (ao_corrente_duración == 정규길이 && 접두(ao_corrente_elemento, 0, ao_corrente_duración, 정규, 정규길이)) return -16;
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < Ficheiro_CONTAR; Loop_ÍNDICE++) {
            if (이름길이[Loop_ÍNDICE] > 정규길이 && 접두(Nome, Loop_ÍNDICE * 64, 이름길이[Loop_ÍNDICE], 정규, 정규길이) && Nome[Loop_ÍNDICE * 64 + 정규길이] == '/') return -39;
        }
        for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 16; Loop_ÍNDICE++) {
            if (directorio_duración[Loop_ÍNDICE] > 정규길이 && 접두(directorio_nome, Loop_ÍNDICE * 64, directorio_duración[Loop_ÍNDICE], 정규, 정규길이) && directorio_nome[Loop_ÍNDICE * 64 + 정규길이] == '/') return -39;
        }
        directorio_duración[폴더번호] = 0; return 0;
    }
    public static int 이름바꾸기(int 원본번호) {
        if (원본번호 < 0 || 원본번호 >= Ficheiro_CONTAR || 이름길이[원본번호] == 0) return -2;
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        if (Busca_directorio(정규길이) >= 0) return -21;
        처리값 = 부모확인(); if (처리값 < 0) return 처리값;
        int 이전값 = Busca_introdución(); if (이전값 == 원본번호) return 0;
        if (이전값 >= 0) 이름길이[이전값] = 0;
        이름길이[원본번호] = 정규길이; for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 정규길이; Loop_ÍNDICE++) Nome[원본번호 * 64 + Loop_ÍNDICE] = 정규[Loop_ÍNDICE]; return 0;
    }
    static int introdución_START(int[] datos_MATRIZ, int 시작점, int introdución_CONTAR) {
        if (!접두(datos_MATRIZ, 시작점, introdución_CONTAR, 정규, 정규길이)) return -1;
        int START_cargo = 정규길이;
        if (START_cargo > 0) { if (introdución_CONTAR <= START_cargo || datos_MATRIZ[시작점 + START_cargo] != '/') return -1; START_cargo++; }
        if (introdución_CONTAR <= START_cargo) return -1;
        for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < introdución_CONTAR; Loop_ÍNDICE++) if (datos_MATRIZ[시작점 + Loop_ÍNDICE] == '/') return -1;
        return START_cargo;
    }
    static void ao_corrente_escribir() { 단말.문자('/'); for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < ao_corrente_duración; Loop_ÍNDICE++) Panel.직렬쓰기(ao_corrente_elemento[Loop_ÍNDICE]); }
    static int 경로목록() {
        int 처리값 = organizar_VALOR(); if (처리값 < 0) return 처리값;
        int Ficheiro_obxectivo_VALOR = Busca_introdución();
        if (Ficheiro_obxectivo_VALOR >= 0) { for (int Loop_ÍNDICE = 0; Loop_ÍNDICE < 정규길이; Loop_ÍNDICE++) Panel.직렬쓰기(정규[Loop_ÍNDICE]); 단말.Escritura("  "); 단말.수(duración_VALOR[Ficheiro_obxectivo_VALOR]); 단말.Escritura("byte_VALOR(주기억 Ficheiro)\n"); return 0; }
        if (Busca_directorio(정규길이) < 0) return -2;
        for (int 뒷값 = 1; 뒷값 < 16; 뒷값++) if (directorio_duración[뒷값] > 0) {
            int START_cargo = introdución_START(directorio_nome, 뒷값 * 64, directorio_duración[뒷값]); if (START_cargo < 0) continue;
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < directorio_duración[뒷값]; Loop_ÍNDICE++) Panel.직렬쓰기(directorio_nome[뒷값 * 64 + Loop_ÍNDICE]); 단말.Escritura("/\n");
        }
        for (int Ficheiro_ÍNDICE = 0; Ficheiro_ÍNDICE < Ficheiro_CONTAR; Ficheiro_ÍNDICE++) if (이름길이[Ficheiro_ÍNDICE] > 0) {
            int START_cargo = introdución_START(Nome, Ficheiro_ÍNDICE * 64, 이름길이[Ficheiro_ÍNDICE]); if (START_cargo < 0) continue;
            for (int Loop_ÍNDICE = START_cargo; Loop_ÍNDICE < 이름길이[Ficheiro_ÍNDICE]; Loop_ÍNDICE++) Panel.직렬쓰기(Nome[Ficheiro_ÍNDICE * 64 + Loop_ÍNDICE]);
            단말.Escritura("  "); 단말.수(duración_VALOR[Ficheiro_ÍNDICE]); 단말.Escritura("byte_VALOR(주기억 Ficheiro)\n");
        }
        return 0;
    }
}
