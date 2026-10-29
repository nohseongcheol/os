// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 byte_VALUE 경계를 지키는 삽입/삭제, 방향키, Comandă LOG_RECORD, Tab Finalizate_VALUE. */
public final class editor_de_linii {
    static boolean linie_de_comandă;
    static int[] LOG_RECORD = new int[16 * 1024], LOG_lungime = new int[16], Store_VALUE = new int[4096], 후보 = new int[64];
    static int LOG_COUNT, LOG_RECORD_termina_un_apel, căuta_VALUE, 저장길이, Mărime, cursor_VALUE, 후보수, 후보길이, buta_fereastră;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd securizat_shell la_distanță_afișa run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String intrare_Listă, int buta_poziție, int termina_un_apel_poziție, int 입력길이) {
        int byte_COUNT=0;
        for(int index_de_poziție=buta_poziție;index_de_poziție<termina_un_apel_poziție;index_de_poziție++) {
            int cod_caracter=intrare_Listă.charAt(index_de_poziție);
            if(cod_caracter>=0xd800 && cod_caracter<=0xdbff && index_de_poziție+1<termina_un_apel_poziție)cod_caracter=0x10000+((cod_caracter-0xd800)<<10)+intrare_Listă.charAt(++index_de_poziție)-0xdc00;
            int 수=cod_caracter<128?1:cod_caracter<2048?2:cod_caracter<65536?3:4;
            if(byte_COUNT+수>62)return;
            for(int SEQUENCE_VALUE=수-1;SEQUENCE_VALUE>=0;SEQUENCE_VALUE--)명령후보[byte_COUNT++]=수==1?cod_caracter:SEQUENCE_VALUE==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(cod_caracter>>(6*SEQUENCE_VALUE)):0x80|((cod_caracter>>(6*SEQUENCE_VALUE))&63);
        }
        if(byte_COUNT<입력길이)return;
        for(int index_de_poziție=0;index_de_poziție<입력길이;index_de_poziție++)if(명령후보[index_de_poziție]!=명령해석기.Linie[index_de_poziție])return;
        후보수++;후보길이=byte_COUNT+1;
        for(int index_de_poziție=0;index_de_poziție<byte_COUNT;index_de_poziție++)후보[index_de_poziție]=명령후보[index_de_poziție];후보[byte_COUNT]=' ';
    }
    static int frontală_VALUE(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.Linie[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int ÎNAPOI_VALUE(int 읽는자리) { if (읽는자리 < Mărime) { 읽는자리++; while (읽는자리 < Mărime && (명령해석기.Linie[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int buta_poziție, int destinație_VALUE_INDEX) {
        int 글칸수 = 0;
        for (int Loop_INDEX = buta_poziție; Loop_INDEX < destinație_VALUE_INDEX; Loop_INDEX++) { int byte_date = 명령해석기.Linie[Loop_INDEX]; if ((byte_date & 192) == 128) continue; 글칸수 += byte_date >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void reîncerca_VALUE() {
        단말.Scriere("\r\u001b[2K");
        단말.Scriere(linie_de_comandă ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 Linie 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int COLUMNS = Avizier.Terminal(13) & 65535; return COLUMNS - (linie_de_comandă ? 18 : 9); }
    static void 보이는줄() {
        if (cursor_VALUE < buta_fereastră) buta_fereastră = cursor_VALUE;
        while (폭(buta_fereastră, cursor_VALUE) > 보이는폭()) buta_fereastră = ÎNAPOI_VALUE(buta_fereastră);
        int termina_un_apel_poziție = buta_fereastră;
        while (termina_un_apel_poziție < Mărime && 폭(buta_fereastră, ÎNAPOI_VALUE(termina_un_apel_poziție)) <= 보이는폭()) termina_un_apel_poziție = ÎNAPOI_VALUE(termina_un_apel_poziție);
        단말.Scriere("\r\u001b["); 단말.수(linie_de_comandă ? 16 : 7); 단말.Scriere("G\u001b[K");
        if (buta_fereastră > 0) 단말.문자('<');
        for (int Loop_INDEX = buta_fereastră; Loop_INDEX < termina_un_apel_poziție; Loop_INDEX++) Avizier.직렬쓰기(명령해석기.Linie[Loop_INDEX]);
        단말.문자(termina_un_apel_poziție < Mărime ? '>' : ' ');
        단말.Scriere("\u001b["); 단말.수(폭(cursor_VALUE, termina_un_apel_poziție) + 1); 단말.문자('D');
        가로보기 = buta_fereastră > 0 || termina_un_apel_poziție < Mărime || 폭(0, Mărime) > 보이는폭();
    }
    static void adăuga_LOG() {
        if (!linie_de_comandă || Mărime == 0 || Mărime > 1024) return;
        if (LOG_COUNT > 0) {
            int 마지막자리 = (LOG_RECORD_termina_un_apel + 15) % 16; boolean 같은여부 = LOG_lungime[마지막자리] == Mărime;
            for (int Loop_INDEX = 0; 같은여부 && Loop_INDEX < Mărime; Loop_INDEX++) if (LOG_RECORD[마지막자리 * 1024 + Loop_INDEX] != 명령해석기.Linie[Loop_INDEX]) 같은여부 = false;
            if (같은여부) return;
        }
        LOG_lungime[LOG_RECORD_termina_un_apel] = Mărime; for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) LOG_RECORD[LOG_RECORD_termina_un_apel * 1024 + Loop_INDEX] = 명령해석기.Linie[Loop_INDEX];
        LOG_RECORD_termina_un_apel = (LOG_RECORD_termina_un_apel + 1) % 16; if (LOG_COUNT < 16) LOG_COUNT++;
    }
    static void 기록이동(int DELTA_VALUE) {
        if (!linie_de_comandă) return;
        if (căuta_VALUE == 0 && DELTA_VALUE > 0) { 저장길이 = Mărime; for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) Store_VALUE[Loop_INDEX] = 명령해석기.Linie[Loop_INDEX]; }
        int Următorul_poziție = căuta_VALUE + DELTA_VALUE; if (Următorul_poziție < 0 || Următorul_poziție > LOG_COUNT) return; căuta_VALUE = Următorul_poziție;
        if (căuta_VALUE == 0) { Mărime = 저장길이; for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) 명령해석기.Linie[Loop_INDEX] = Store_VALUE[Loop_INDEX]; }
        else { int 보관칸 = (LOG_RECORD_termina_un_apel + 16 - căuta_VALUE) % 16; Mărime = LOG_lungime[보관칸]; for (int Loop_INDEX = 0; Loop_INDEX < Mărime; Loop_INDEX++) 명령해석기.Linie[Loop_INDEX] = LOG_RECORD[보관칸 * 1024 + Loop_INDEX]; }
        cursor_VALUE = Mărime; reîncerca_VALUE();
    }
    static void afișa_LOG() {
        for (int intrare_COUNT = 0; intrare_COUNT < LOG_COUNT; intrare_COUNT++) {
            int 보관칸 = (LOG_RECORD_termina_un_apel + 16 - LOG_COUNT + intrare_COUNT) % 16; 단말.수(intrare_COUNT + 1); 단말.Scriere("  ");
            for (int Loop_INDEX = 0; Loop_INDEX < LOG_lungime[보관칸]; Loop_INDEX++) Avizier.직렬쓰기(LOG_RECORD[보관칸 * 1024 + Loop_INDEX]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] date_ARRAY, int buta_poziție, int intrare_COUNT, int 접두말, int total_COUNT, boolean 폴더번호) {
        if (intrare_COUNT < total_COUNT || intrare_COUNT > 62) return;
        for (int Loop_INDEX = 0; Loop_INDEX < total_COUNT; Loop_INDEX++) if (date_ARRAY[buta_poziție + Loop_INDEX] != 명령해석기.Linie[접두말 + Loop_INDEX]) return;
        후보수++; 후보길이 = intrare_COUNT + 1;
        for (int Loop_INDEX = 0; Loop_INDEX < intrare_COUNT; Loop_INDEX++) 후보[Loop_INDEX] = date_ARRAY[buta_poziție + Loop_INDEX]; 후보[intrare_COUNT] = 폴더번호 ? '/' : ' ';
    }
    static void Finalizate_VALUE() {
        if (!linie_de_comandă || cursor_VALUE != Mărime) return;
        int 시작점 = Mărime; while (시작점 > 0 && 명령해석기.Linie[시작점 - 1] != ' ') 시작점--;
        for (int Loop_INDEX = 시작점; Loop_INDEX < Mărime; Loop_INDEX++) if (명령해석기.Linie[Loop_INDEX] == '/' || 명령해석기.Linie[Loop_INDEX] == '"' || 명령해석기.Linie[Loop_INDEX] == 39 || 명령해석기.Linie[Loop_INDEX] == '\\') return;
        후보수 = 0; int intrare_COUNT = Mărime - 시작점;
        if (시작점 == 0) {
            for(int index_de_listă=0;index_de_listă<2;index_de_listă++) {
                String intrare_Listă=index_de_listă==0?명령들:관리명령.Finalizate_Word();
                int 읽는자리=0;
                while(읽는자리<intrare_Listă.length()) {
                    int termina_un_apel_poziție=읽는자리;while(termina_un_apel_poziție<intrare_Listă.length() && intrare_Listă.charAt(termina_un_apel_poziție)!=' ')termina_un_apel_poziție++;
                    명령후보넣기(intrare_Listă,읽는자리,termina_un_apel_poziție,intrare_COUNT);읽는자리=termina_un_apel_poziție+1;
                }
            }
        } else {
            Memorie_Fișiere.cale_buta(1); Memorie_Fișiere.cale_byte(0, '.'); Memorie_Fișiere.normaliza_VALUE();
            for (int Loop_INDEX = 0; Loop_INDEX < Memorie_Fișiere.Fișier_COUNT; Loop_INDEX++) {
                int buta_poziție = Memorie_Fișiere.intrare_buta(Memorie_Fișiere.Nume, Loop_INDEX * 64, Memorie_Fișiere.이름길이[Loop_INDEX]);
                if (buta_poziție >= 0) 후보넣기(Memorie_Fișiere.Nume, Loop_INDEX * 64 + buta_poziție, Memorie_Fișiere.이름길이[Loop_INDEX] - buta_poziție, 시작점, intrare_COUNT, false);
            }
            for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
                int buta_poziție = Memorie_Fișiere.intrare_buta(Memorie_Fișiere.Director_nume, Loop_INDEX * 64, Memorie_Fișiere.Director_lungime[Loop_INDEX]);
                if (buta_poziție >= 0) 후보넣기(Memorie_Fișiere.Director_nume, Loop_INDEX * 64 + buta_poziție, Memorie_Fișiere.Director_lungime[Loop_INDEX] - buta_poziție, 시작점, intrare_COUNT, true);
            }
        }
        if (후보수 != 1) { Avizier.직렬쓰기(7); return; }
        for (int Loop_INDEX = intrare_COUNT; Loop_INDEX < 후보길이 && Mărime < 명령해석기.Linie.length - 1; Loop_INDEX++) {
            if (후보[Loop_INDEX] == ' ' && Loop_INDEX != 후보길이 - 1) 명령해석기.Linie[Mărime++] = '\\';
            명령해석기.Linie[Mărime++] = 후보[Loop_INDEX];
        }
        cursor_VALUE = Mărime; reîncerca_VALUE();
    }
    static int 탈출읽기() {
        int 시작점 = Avizier.밀리초();
        while (Avizier.밀리초() - 시작점 < 80) { int byte_date = Avizier.직렬읽기(); if (byte_date >= 0) return byte_date; Avizier.YIELD_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int intrare_COUNT = 0, termina_un_apel_poziție = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 12; Loop_INDEX++) { int byte_date = 탈출읽기(); if (byte_date < 0) return; if (byte_date >= '0' && byte_date <= '9') intrare_COUNT = intrare_COUNT * 10 + byte_date - '0'; else { termina_un_apel_poziție = byte_date; break; } }
        if (termina_un_apel_poziție == 'A') 기록이동(1);
        else if (termina_un_apel_poziție == 'B') 기록이동(-1);
        else if (termina_un_apel_poziție == 'C') { cursor_VALUE = ÎNAPOI_VALUE(cursor_VALUE); reîncerca_VALUE(); }
        else if (termina_un_apel_poziție == 'D') { cursor_VALUE = frontală_VALUE(cursor_VALUE); reîncerca_VALUE(); }
        else if (termina_un_apel_poziție == 'H' || termina_un_apel_poziție == '~' && (intrare_COUNT == 1 || intrare_COUNT == 7)) { cursor_VALUE = 0; reîncerca_VALUE(); }
        else if (termina_un_apel_poziție == 'F' || termina_un_apel_poziție == '~' && (intrare_COUNT == 4 || intrare_COUNT == 8)) { cursor_VALUE = Mărime; reîncerca_VALUE(); }
        else if (termina_un_apel_poziție == '~' && intrare_COUNT == 3 && cursor_VALUE < Mărime) {
            int Următorul_poziție = ÎNAPOI_VALUE(cursor_VALUE); for (int Loop_INDEX = Următorul_poziție; Loop_INDEX < Mărime; Loop_INDEX++) 명령해석기.Linie[Loop_INDEX - Următorul_poziție + cursor_VALUE] = 명령해석기.Linie[Loop_INDEX]; Mărime -= Următorul_poziție - cursor_VALUE; reîncerca_VALUE();
        }
        else if (termina_un_apel_poziție == '~' && (intrare_COUNT == 5 || intrare_COUNT == 6)) Avizier.Terminal(intrare_COUNT == 5 ? 5 : 6);
        else if (termina_un_apel_poziție == '~' && intrare_COUNT == 24 && linie_de_comandă) { 명령해석기.Terminal(true); }
    }
    static int Citire() {
        if (!fereastră_sesiune.이어읽기) { Mărime = cursor_VALUE = căuta_VALUE = buta_fereastră = 0; 가로보기 = false; }
        else { fereastră_sesiune.이어읽기 = false; reîncerca_VALUE(); } boolean depășire = false;
        while (true) {
            int byte_date = Avizier.직렬읽기(); if (byte_date == -4096) return -3;
            if (Avizier.Terminal(14) != 0) reîncerca_VALUE(); if (byte_date < 0) { Avizier.YIELD_CPU(); continue; }
            if (byte_date == 10 && 명령해석기.Anteriorul_linie) { 명령해석기.Anteriorul_linie = false; continue; } 명령해석기.Anteriorul_linie = byte_date == 13;
            if (byte_date == 27) { 탈출(); continue; }
            if (byte_date == 3) { 단말.Scriere("^C\n"); return -1; }
            if (byte_date == 4 && Mărime == 0 && linie_de_comandă) { if (Avizier.Terminal(2) != 0) 명령해석기.Terminal(true); return -1; }
            if (byte_date == 13 || byte_date == 10) { 단말.문자(10); if (!depășire) adăuga_LOG(); return depășire ? -2 : Mărime; }
            if (byte_date == 9 && linie_de_comandă) { Finalizate_VALUE(); continue; }
            if (byte_date == 1 || byte_date == 5) { cursor_VALUE = byte_date == 1 ? 0 : Mărime; reîncerca_VALUE(); continue; }
            if (byte_date == 8 || byte_date == 127 || byte_date == 21) {
                if (byte_date == 21) { for (int Loop_INDEX = cursor_VALUE; Loop_INDEX < Mărime; Loop_INDEX++) 명령해석기.Linie[Loop_INDEX - cursor_VALUE] = 명령해석기.Linie[Loop_INDEX]; Mărime -= cursor_VALUE; cursor_VALUE = 0; }
                else if (cursor_VALUE > 0) { int 변경전 = frontală_VALUE(cursor_VALUE); for (int Loop_INDEX = cursor_VALUE; Loop_INDEX < Mărime; Loop_INDEX++) 명령해석기.Linie[Loop_INDEX - cursor_VALUE + 변경전] = 명령해석기.Linie[Loop_INDEX]; Mărime -= cursor_VALUE - 변경전; cursor_VALUE = 변경전; }
                reîncerca_VALUE(); continue;
            }
            if (byte_date == 11) { Mărime = cursor_VALUE; reîncerca_VALUE(); continue; }
            if (byte_date < 32 && byte_date != 9) continue;
            if (Mărime == 명령해석기.Linie.length) { depășire = true; continue; }
            for (int Loop_INDEX = Mărime; Loop_INDEX > cursor_VALUE; Loop_INDEX--) 명령해석기.Linie[Loop_INDEX] = 명령해석기.Linie[Loop_INDEX - 1];
            명령해석기.Linie[cursor_VALUE++] = byte_date; Mărime++;
            if (cursor_VALUE == Mărime && !가로보기 && 폭(0, Mărime) <= 보이는폭()) Avizier.직렬쓰기(byte_date);
            else if (cursor_VALUE == Mărime) 보이는줄(); else reîncerca_VALUE();
        }
    }
}
