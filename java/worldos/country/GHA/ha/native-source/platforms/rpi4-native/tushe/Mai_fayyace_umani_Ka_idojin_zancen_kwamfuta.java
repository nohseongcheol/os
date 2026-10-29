// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 Shigar_da_umarni_na_kwamfuta Mai_fayyace_umani 문법. 파이프는 순차 gudanar_Umarni, 환경은 같은 셸에서 공유한다. */
public final class Mai_fayyace_umani_Ka_idojin_zancen_kwamfuta {
    static int[] tushe = new int[4 * 4096], 종류 = new int[4 * 128], Tafiyar_da = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], Daraja_Tsawo = new int[16];
    static int[] skript_Daraja = new int[4 * 16384];
    static int Matsayi_Daraja, 깊이, 쓴수;
    static boolean 연결중, skript_Ƙarshe, faɗi_Kuskure;
    static boolean Suna_Harafi(int Lambar_sirrin_harafi) { return Lambar_sirrin_harafi >= 'a' && Lambar_sirrin_harafi <= 'z' || Lambar_sirrin_harafi >= 'A' && Lambar_sirrin_harafi <= 'Z' || Lambar_sirrin_harafi == '_' || Lambar_sirrin_harafi >= 128; }
    static boolean 이름뒤(int Lambar_sirrin_harafi) { return Suna_Harafi(Lambar_sirrin_harafi) || Lambar_sirrin_harafi >= '0' && Lambar_sirrin_harafi <= '9'; }
    static void Kuskure(String SMS) { 보드.입출력전환(0); 단말.Yi_Rubutu("Umarni Daddatse_Daraja: "); 단말.Yi_Rubutu(SMS); 단말.문자(10); Matsayi_Daraja = 2; }
    static int Yi_Karatu(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, harafi_na_musamman = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (tushe[기준자리 + 현재자리] == 32 || tushe[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || tushe[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { Kuskure("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, Lambar_sirrin_harafi = tushe[기준자리 + 현재자리], 자료종류 = 0;
            if (Lambar_sirrin_harafi == ';') { 자료종류 = 1; 현재자리++; }
            else if (Lambar_sirrin_harafi == '&') { if (현재자리 + 1 >= 항목수 || tushe[기준자리 + 현재자리 + 1] != '&') { Kuskure("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (Lambar_sirrin_harafi == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && tushe[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (Lambar_sirrin_harafi == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && tushe[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (Lambar_sirrin_harafi == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    Lambar_sirrin_harafi = tushe[기준자리 + 현재자리];
                    if (Lambar_sirrin_harafi == '`' && 따옴표 != 39 || Lambar_sirrin_harafi == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && tushe[기준자리 + 현재자리 + 1] == '(') { Kuskure("Umarni 결과 치환은 지원하지 않습니다"); return -1; }
                    if (Lambar_sirrin_harafi == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { Kuskure("Layi 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (Lambar_sirrin_harafi == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (Lambar_sirrin_harafi == 39 || Lambar_sirrin_harafi == 34)) { 따옴표 = Lambar_sirrin_harafi; 현재자리++; continue; }
                    if (따옴표 == 0 && (Lambar_sirrin_harafi == 32 || Lambar_sirrin_harafi == 9 || Lambar_sirrin_harafi == ';' || Lambar_sirrin_harafi == '&' || Lambar_sirrin_harafi == '|' || Lambar_sirrin_harafi == '<' || Lambar_sirrin_harafi == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { Kuskure("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (tushe[기준자리 + 현재자리] == '>' || tushe[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int Warware_Indes = 시작자리; Warware_Indes < 현재자리; Warware_Indes++) if (tushe[기준자리 + Warware_Indes] < '0' || tushe[기준자리 + Warware_Indes] > '9') 수치 = false;
                    if (수치) { Kuskure("번호를 지정한 Fayil 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[harafi_na_musamman + 총수] = 자료종류; Tafiyar_da[harafi_na_musamman + 총수] = 시작자리; 끝[harafi_na_musamman + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int Warware_Indes = 0; Warware_Indes < 총수; Warware_Indes++) {
            int 임시값 = 종류[harafi_na_musamman + Warware_Indes];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Warware_Indes == 총수 || 종류[harafi_na_musamman + Warware_Indes] != 0) { Kuskure("I_O 전환에 Fayil 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Warware_Indes == 총수 - 1 && 임시값 != 1) { Kuskure("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[harafi_na_musamman + 총수 - 1] != 1) { Kuskure("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] Tarin_bayani_TSARI, int na_gida_Fara, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) if (Tarin_bayani_TSARI[na_gida_Fara + Warware_Indes] != 문자위치.charAt(Warware_Indes)) return false; return true;
    }
    static void 넣기(int bayit_Tarin_bayani) {
        if (쓴수 >= 명령해석기.token_Daraja.length) { if (!faɗi_Kuskure) Kuskure("변수를 펼친 명령이 너무 깁니다"); faɗi_Kuskure = true; return; }
        명령해석기.token_Daraja[쓴수++] = bayit_Tarin_bayani;
    }
    static void 변수(int[] Tarin_bayani_TSARI, int 시작자리, int 항목수) {
        if (구간말(Tarin_bayani_TSARI, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int Warware_Indes = 0; Warware_Indes < Mahardatar_kwamfuta_Fayiloli.현재길이; Warware_Indes++) 넣기(Mahardatar_kwamfuta_Fayiloli.현재[Warware_Indes]); return; }
        if (구간말(Tarin_bayani_TSARI, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(Tarin_bayani_TSARI, 시작자리, 항목수, "?")) {
            int Tarin_bayani_Daraja = Matsayi_Daraja, lamba = 100; boolean 시작여부 = false;
            while (lamba > 0) { int 뒷값 = Tarin_bayani_Daraja / lamba; if (뒷값 != 0 || 시작여부 || lamba == 1) { 넣기('0' + 뒷값); 시작여부 = true; } Tarin_bayani_Daraja %= lamba; lamba /= 10; } return;
        }
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) if (이름길이[Warware_Indes] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[Warware_Indes * 32 + 안쪽자리] != Tarin_bayani_TSARI[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < Daraja_Tsawo[Warware_Indes]; 안쪽자리++) 넣기(변수값[Warware_Indes * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Microsoft_Word_Daraja(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Tafiyar_da[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && tushe[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || tushe[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int Lambar_sirrin_harafi = tushe[기준자리 + 읽는자리++];
            if (Lambar_sirrin_harafi == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (Lambar_sirrin_harafi == 39 || Lambar_sirrin_harafi == 34)) { 따옴표 = Lambar_sirrin_harafi; continue; }
            if (Lambar_sirrin_harafi == '\\' && 따옴표 != 39) { int 다음자리 = tushe[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (Lambar_sirrin_harafi == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = tushe[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && tushe[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(tushe[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || tushe[기준자리 + 읽는자리] != '}')) { Kuskure("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(tushe, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(Lambar_sirrin_harafi);
        }
        return !faɗi_Kuskure;
    }
    static int 환경설정(int Tubalin_aiki_Indes, boolean Cire) {
        int na_gida_Fara = 명령해석기.시작점[Tubalin_aiki_Indes], 끝자리 = na_gida_Fara + 명령해석기.Tsawo_Daraja[Tubalin_aiki_Indes], 같음자리 = na_gida_Fara;
        while (같음자리 < 끝자리 && 명령해석기.token_Daraja[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - na_gida_Fara;
        if (항목수 < 1 || 항목수 > 31 || !Suna_Harafi(명령해석기.token_Daraja[na_gida_Fara]) || !Cire && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int Warware_Indes = na_gida_Fara; Warware_Indes < 같음자리; Warware_Indes++) if (!이름뒤(명령해석기.token_Daraja[Warware_Indes])) return 2;
        if (구간말(명령해석기.token_Daraja, na_gida_Fara, 항목수, "PWD") || 구간말(명령해석기.token_Daraja, na_gida_Fara, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, kimiyar_bayanai_holoko_Matsayi = -1;
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) {
            if (이름길이[Warware_Indes] == 0) kimiyar_bayanai_holoko_Matsayi = Warware_Indes;
            if (이름길이[Warware_Indes] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[Warware_Indes * 32 + 안쪽자리] != 명령해석기.token_Daraja[na_gida_Fara + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = Warware_Indes;
        }
        if (Cire) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = kimiyar_bayanai_holoko_Matsayi; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; Daraja_Tsawo[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) 변수이름[찾은여부 * 32 + Warware_Indes] = 명령해석기.token_Daraja[na_gida_Fara + Warware_Indes];
        for (int Warware_Indes = 같음자리 + 1; Warware_Indes < 끝자리; Warware_Indes++) 변수값[찾은여부 * 256 + Warware_Indes - 같음자리 - 1] = 명령해석기.token_Daraja[Warware_Indes];
        return 0;
    }
    static void 환경보기() {
        단말.Yi_Rubutu("HOME=/\nPWD="); Mahardatar_kwamfuta_Fayiloli.현재쓰기(); 단말.문자(10);
        for (int Warware_Indes = 0; Warware_Indes < 16; Warware_Indes++) if (이름길이[Warware_Indes] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[Warware_Indes]; 안쪽자리++) 보드.직렬쓰기(변수이름[Warware_Indes * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < Daraja_Tsawo[Warware_Indes]; 안쪽자리++) 보드.직렬쓰기(변수값[Warware_Indes * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void gudanar_Umarni(int[] Tarin_bayani_TSARI, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { Kuskure("Umarni 파일의 sarƙaƙewa_Daraja 또는 Layi Tsawo_Daraja 제한을 넘었습니다"); return; }
        for (int Warware_Indes = 0; Warware_Indes < 항목수; Warware_Indes++) tushe[중첩깊이 * 4096 + Warware_Indes] = Tarin_bayani_TSARI[시작변위 + Warware_Indes];
        int 총수 = Yi_Karatu(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int gungu_Ƙarshe = 읽는자리;
            while (gungu_Ƙarshe < 총수 && (종류[중첩깊이 * 128 + gungu_Ƙarshe] == 0 || 종류[중첩깊이 * 128 + gungu_Ƙarshe] >= 4)) gungu_Ƙarshe++;
            boolean gudanar = 조건성립 == 1 || 조건성립 == 2 && Matsayi_Daraja == 0 || 조건성립 == 3 && Matsayi_Daraja != 0;
            if (gudanar) {
                boolean 이전자리 = false;
                while (읽는자리 < gungu_Ƙarshe) {
                    int 다음자리 = 읽는자리; while (다음자리 < gungu_Ƙarshe && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean HAƊI_watsuwa = 다음자리 < gungu_Ƙarshe; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; faɗi_Kuskure = false;
                    for (int Warware_Indes = 읽는자리; Warware_Indes < 다음자리; Warware_Indes++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Warware_Indes];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { Kuskure("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Warware_Indes; } else { if (출력쪽 >= 0) { Kuskure("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++Warware_Indes; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { Kuskure("인수가 너무 많습니다"); return; }
                        int Tubalin_aiki_Indes = 명령해석기.토큰수++; 명령해석기.시작점[Tubalin_aiki_Indes] = 쓴수;
                        if (!Microsoft_Word_Daraja(Warware_Indes, 중첩깊이)) return;
                        명령해석기.Tsawo_Daraja[Tubalin_aiki_Indes] = 쓴수 - 명령해석기.시작점[Tubalin_aiki_Indes];
                    }
                    연결중 = 이전자리 || HAƊI_watsuwa || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { Kuskure("Shigar_da_umarni_na_kwamfuta 명령과 Umarni 파일은 I_O 전환이나 watsuwa_Daraja 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Tafiyar_da(이전자리, HAƊI_watsuwa);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Microsoft_Word_Daraja(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_Fara(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = Mahardatar_kwamfuta_Fayiloli.Hanyar_shiga_bayit(안쪽자리 - 시작자리, 명령해석기.token_Daraja[안쪽자리]);
                        if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.Buɗe(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.Kuskure(처리값); Matsayi_Daraja = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.makunshin_shirye_shiryen_da_aka_kirkira = 처리값;
                    }
                    셸입출력.Bada_izini_Shigar_da_umarni_na_kwamfuta = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Umarni();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, watsuwa_Kuskure = 셸입출력.Kasa_aiki_Daraja;
                    셸입출력.끝(); 연결중 = false;
                    Matsayi_Daraja = watsuwa_Kuskure < 0 ? 1 : 반환값;
                    if (watsuwa_Kuskure < 0) { 명령해석기.Kuskure(watsuwa_Kuskure); return; }
                    if (skript_Ƙarshe || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (gungu_Ƙarshe < 총수) 조건성립 = 종류[중첩깊이 * 128 + gungu_Ƙarshe];
            읽는자리 = gungu_Ƙarshe + 1;
        }
    }
    static void gudanar_Fayil() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Yi_Rubutu("사용법: sh Fayil (sarƙaƙewa_Daraja 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.Hanyar_shiga(1); if (처리값 >= 0) 처리값 = Mahardatar_kwamfuta_Fayiloli.Buɗe(0);
        if (처리값 < 0) { 명령해석기.Kuskure(처리값); return; }
        int 항목수 = 0, bayit_Tarin_bayani;
        while ((bayit_Tarin_bayani = Mahardatar_kwamfuta_Fayiloli.Yi_Karatu(처리값)) != 256 && bayit_Tarin_bayani >= 0 && 항목수 < 16384) skript_Daraja[중첩깊이 * 16384 + 항목수++] = bayit_Tarin_bayani;
        Mahardatar_kwamfuta_Fayiloli.Rufe(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !skript_Ƙarshe;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && skript_Daraja[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && skript_Daraja[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            gudanar_Umarni(skript_Daraja, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = Matsayi_Daraja; skript_Ƙarshe = false; 깊이 = 중첩깊이 - 1;
    }
}
