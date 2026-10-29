// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 대화형 apvalkalas 문법. 파이프는 순차 Vykdyti_komanda, 환경은 같은 셸에서 공유한다. */
public final class apvalkalas_sintaksė {
    static int[] ŠALTINIS = new int[4 * 4096], 종류 = new int[4 * 128], Paleisti = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] kintamasis_pavadinimas = new int[16 * 32], kintamasis_duomenys = new int[16 * 256], 이름길이 = new int[16], 값길이 = new int[16];
    static int[] scenarijus_VALUE = new int[4 * 16384];
    static int Būsena_VALUE, 깊이, 쓴수;
    static boolean 연결중, scenarijus_baigti_pokalbį, 확장오류;
    static boolean pavadinimas_simbolis(int simbolio_kodas) { return simbolio_kodas >= 'a' && simbolio_kodas <= 'z' || simbolio_kodas >= 'A' && simbolio_kodas <= 'Z' || simbolio_kodas == '_' || simbolio_kodas >= 128; }
    static boolean 이름뒤(int simbolio_kodas) { return pavadinimas_simbolis(simbolio_kodas) || simbolio_kodas >= '0' && simbolio_kodas <= '9'; }
    static void KLAIDA(String Tekstas) { Lenta.입출력전환(0); 단말.Rašymas("Komanda analizuoti_sintaksę_VALUE: "); 단말.Rašymas(Tekstas); 단말.문자(10); Būsena_VALUE = 2; }
    static int Skaitymas(int įrašas_COUNT, int 중첩깊이) {
        int dabartinis_INDEX = 0, bendras_COUNT = 0, BASE_padėtis = 중첩깊이 * 4096, specialusis_simbolis = 중첩깊이 * 128;
        while (dabartinis_INDEX < įrašas_COUNT) {
            while (dabartinis_INDEX < įrašas_COUNT && (ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == 32 || ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == 9)) dabartinis_INDEX++;
            if (dabartinis_INDEX == įrašas_COUNT || ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == '#') break;
            if (bendras_COUNT == 128) { KLAIDA("낱말이 너무 많습니다"); return -1; }
            int Start_padėtis = dabartinis_INDEX, simbolio_kodas = ŠALTINIS[BASE_padėtis + dabartinis_INDEX], 자료종류 = 0;
            if (simbolio_kodas == ';') { 자료종류 = 1; dabartinis_INDEX++; }
            else if (simbolio_kodas == '&') { if (dabartinis_INDEX + 1 >= įrašas_COUNT || ŠALTINIS[BASE_padėtis + dabartinis_INDEX + 1] != '&') { KLAIDA("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; dabartinis_INDEX += 2; }
            else if (simbolio_kodas == '|') { dabartinis_INDEX++; 자료종류 = dabartinis_INDEX < įrašas_COUNT && ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == '|' ? 3 : 4; if (자료종류 == 3) dabartinis_INDEX++; }
            else if (simbolio_kodas == '>') { dabartinis_INDEX++; 자료종류 = dabartinis_INDEX < įrašas_COUNT && ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == '>' ? 6 : 5; if (자료종류 == 6) dabartinis_INDEX++; }
            else if (simbolio_kodas == '<') { 자료종류 = 7; dabartinis_INDEX++; }
            else {
                int Citavimas = 0;
                while (dabartinis_INDEX < įrašas_COUNT) {
                    simbolio_kodas = ŠALTINIS[BASE_padėtis + dabartinis_INDEX];
                    if (simbolio_kodas == '`' && Citavimas != 39 || simbolio_kodas == '$' && Citavimas != 39 && dabartinis_INDEX + 1 < įrašas_COUNT && ŠALTINIS[BASE_padėtis + dabartinis_INDEX + 1] == '(') { KLAIDA("Komanda REZULTATAS 치환은 지원하지 않습니다"); return -1; }
                    if (simbolio_kodas == '\\' && Citavimas != 39) { if (++dabartinis_INDEX == įrašas_COUNT) { KLAIDA("Eilutė 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } dabartinis_INDEX++; continue; }
                    if (simbolio_kodas == Citavimas) { Citavimas = 0; dabartinis_INDEX++; continue; }
                    if (Citavimas == 0 && (simbolio_kodas == 39 || simbolio_kodas == 34)) { Citavimas = simbolio_kodas; dabartinis_INDEX++; continue; }
                    if (Citavimas == 0 && (simbolio_kodas == 32 || simbolio_kodas == 9 || simbolio_kodas == ';' || simbolio_kodas == '&' || simbolio_kodas == '|' || simbolio_kodas == '<' || simbolio_kodas == '>')) break;
                    dabartinis_INDEX++;
                }
                if (Citavimas != 0) { KLAIDA("따옴표가 닫히지 않았습니다"); return -1; }
                if (dabartinis_INDEX < įrašas_COUNT && (ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == '>' || ŠALTINIS[BASE_padėtis + dabartinis_INDEX] == '<')) {
                    boolean 수치 = dabartinis_INDEX > Start_padėtis;
                    for (int Loop_INDEX = Start_padėtis; Loop_INDEX < dabartinis_INDEX; Loop_INDEX++) if (ŠALTINIS[BASE_padėtis + Loop_INDEX] < '0' || ŠALTINIS[BASE_padėtis + Loop_INDEX] > '9') 수치 = false;
                    if (수치) { KLAIDA("번호를 지정한 Failas 서술자 Į_I 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[specialusis_simbolis + bendras_COUNT] = 자료종류; Paleisti[specialusis_simbolis + bendras_COUNT] = Start_padėtis; 끝[specialusis_simbolis + bendras_COUNT] = dabartinis_INDEX; bendras_COUNT++;
        }
        boolean 낱말 = false;
        for (int Loop_INDEX = 0; Loop_INDEX < bendras_COUNT; Loop_INDEX++) {
            int 임시값 = 종류[specialusis_simbolis + Loop_INDEX];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++Loop_INDEX == bendras_COUNT || 종류[specialusis_simbolis + Loop_INDEX] != 0) { KLAIDA("Į_I 전환에 Failas 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || Loop_INDEX == bendras_COUNT - 1 && 임시값 != 1) { KLAIDA("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (bendras_COUNT > 0 && !낱말 && 종류[specialusis_simbolis + bendras_COUNT - 1] != 1) { KLAIDA("명령이 빠졌습니다"); return -1; }
        return bendras_COUNT;
    }
    static boolean diapazonas_SMS(int[] duomenys_ARRAY, int vietinis_Start, int įrašas_COUNT, String simbolis_padėtis) {
        if (įrašas_COUNT != simbolis_padėtis.length()) return false; for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) if (duomenys_ARRAY[vietinis_Start + Loop_INDEX] != simbolis_padėtis.charAt(Loop_INDEX)) return false; return true;
    }
    static void 넣기(int baitas_duomenys) {
        if (쓴수 >= 명령해석기.žetonas_VALUE.length) { if (!확장오류) KLAIDA("변수를 펼친 명령이 너무 깁니다"); 확장오류 = true; return; }
        명령해석기.žetonas_VALUE[쓴수++] = baitas_duomenys;
    }
    static void kintamasis_VALUE(int[] duomenys_ARRAY, int Start_padėtis, int įrašas_COUNT) {
        if (diapazonas_SMS(duomenys_ARRAY, Start_padėtis, įrašas_COUNT, "PWD")) { 넣기('/'); for (int Loop_INDEX = 0; Loop_INDEX < atmintis_Failai.현재길이; Loop_INDEX++) 넣기(atmintis_Failai.dabartinis_prekė[Loop_INDEX]); return; }
        if (diapazonas_SMS(duomenys_ARRAY, Start_padėtis, įrašas_COUNT, "HOME")) { 넣기('/'); return; }
        if (diapazonas_SMS(duomenys_ARRAY, Start_padėtis, įrašas_COUNT, "?")) {
            int duomenys_VALUE = Būsena_VALUE, skaitmuo = 100; boolean 시작여부 = false;
            while (skaitmuo > 0) { int 뒷값 = duomenys_VALUE / skaitmuo; if (뒷값 != 0 || 시작여부 || skaitmuo == 1) { 넣기('0' + 뒷값); 시작여부 = true; } duomenys_VALUE %= skaitmuo; skaitmuo /= 10; } return;
        }
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] == įrašas_COUNT) {
            boolean MATCH = true; for (int vidinis_padėtis = 0; vidinis_padėtis < įrašas_COUNT; vidinis_padėtis++) if (kintamasis_pavadinimas[Loop_INDEX * 32 + vidinis_padėtis] != duomenys_ARRAY[Start_padėtis + vidinis_padėtis]) MATCH = false;
            if (MATCH) { for (int vidinis_padėtis = 0; vidinis_padėtis < 값길이[Loop_INDEX]; vidinis_padėtis++) 넣기(kintamasis_duomenys[Loop_INDEX * 256 + vidinis_padėtis]); return; }
        }
    }
    static boolean Word_VALUE(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Paleisti[중첩깊이 * 128 + 낱말번호], baigti_pokalbį_padėtis = 끝[중첩깊이 * 128 + 낱말번호], BASE_padėtis = 중첩깊이 * 4096, Citavimas = 0;
        if (읽는자리 < baigti_pokalbį_padėtis && ŠALTINIS[BASE_padėtis + 읽는자리] == '~' && (읽는자리 + 1 == baigti_pokalbį_padėtis || ŠALTINIS[BASE_padėtis + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < baigti_pokalbį_padėtis) {
            int simbolio_kodas = ŠALTINIS[BASE_padėtis + 읽는자리++];
            if (simbolio_kodas == Citavimas) { Citavimas = 0; continue; }
            if (Citavimas == 0 && (simbolio_kodas == 39 || simbolio_kodas == 34)) { Citavimas = simbolio_kodas; continue; }
            if (simbolio_kodas == '\\' && Citavimas != 39) { int toliau_padėtis = ŠALTINIS[BASE_padėtis + 읽는자리++]; if (Citavimas == 34 && toliau_padėtis != '$' && toliau_padėtis != '"' && toliau_padėtis != '\\') 넣기('\\'); 넣기(toliau_padėtis); continue; }
            if (simbolio_kodas == '$' && Citavimas != 39 && 읽는자리 < baigti_pokalbį_padėtis) {
                boolean 중괄호자리 = ŠALTINIS[BASE_padėtis + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < baigti_pokalbį_padėtis && ŠALTINIS[BASE_padėtis + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < baigti_pokalbį_padėtis && 이름뒤(ŠALTINIS[BASE_padėtis + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == baigti_pokalbį_padėtis || ŠALTINIS[BASE_padėtis + 읽는자리] != '}')) { KLAIDA("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                kintamasis_VALUE(ŠALTINIS, BASE_padėtis + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(simbolio_kodas);
        }
        return !확장오류;
    }
    static int 환경설정(int argumentas_INDEX, boolean pašalinti) {
        int vietinis_Start = 명령해석기.시작점[argumentas_INDEX], baigti_pokalbį_padėtis = vietinis_Start + 명령해석기.길이[argumentas_INDEX], 같음자리 = vietinis_Start;
        while (같음자리 < baigti_pokalbį_padėtis && 명령해석기.žetonas_VALUE[같음자리] != '=') 같음자리++;
        int įrašas_COUNT = 같음자리 - vietinis_Start;
        if (įrašas_COUNT < 1 || įrašas_COUNT > 31 || !pavadinimas_simbolis(명령해석기.žetonas_VALUE[vietinis_Start]) || !pašalinti && 같음자리 == baigti_pokalbį_padėtis || baigti_pokalbį_padėtis - 같음자리 - 1 > 255) return 2;
        for (int Loop_INDEX = vietinis_Start; Loop_INDEX < 같음자리; Loop_INDEX++) if (!이름뒤(명령해석기.žetonas_VALUE[Loop_INDEX])) return 2;
        if (diapazonas_SMS(명령해석기.žetonas_VALUE, vietinis_Start, įrašas_COUNT, "PWD") || diapazonas_SMS(명령해석기.žetonas_VALUE, vietinis_Start, įrašas_COUNT, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) {
            if (이름길이[Loop_INDEX] == 0) 빈여부 = Loop_INDEX;
            if (이름길이[Loop_INDEX] != įrašas_COUNT) continue;
            boolean MATCH = true; for (int vidinis_padėtis = 0; vidinis_padėtis < įrašas_COUNT; vidinis_padėtis++) if (kintamasis_pavadinimas[Loop_INDEX * 32 + vidinis_padėtis] != 명령해석기.žetonas_VALUE[vietinis_Start + vidinis_padėtis]) MATCH = false;
            if (MATCH) 찾은여부 = Loop_INDEX;
        }
        if (pašalinti) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = įrašas_COUNT; 값길이[찾은여부] = baigti_pokalbį_padėtis - 같음자리 - 1;
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) kintamasis_pavadinimas[찾은여부 * 32 + Loop_INDEX] = 명령해석기.žetonas_VALUE[vietinis_Start + Loop_INDEX];
        for (int Loop_INDEX = 같음자리 + 1; Loop_INDEX < baigti_pokalbį_padėtis; Loop_INDEX++) kintamasis_duomenys[찾은여부 * 256 + Loop_INDEX - 같음자리 - 1] = 명령해석기.žetonas_VALUE[Loop_INDEX];
        return 0;
    }
    static void 환경보기() {
        단말.Rašymas("HOME=/\nPWD="); atmintis_Failai.dabartinis_rašymas(); 단말.문자(10);
        for (int Loop_INDEX = 0; Loop_INDEX < 16; Loop_INDEX++) if (이름길이[Loop_INDEX] > 0) {
            for (int vidinis_padėtis = 0; vidinis_padėtis < 이름길이[Loop_INDEX]; vidinis_padėtis++) Lenta.직렬쓰기(kintamasis_pavadinimas[Loop_INDEX * 32 + vidinis_padėtis]); 단말.문자('=');
            for (int vidinis_padėtis = 0; vidinis_padėtis < 값길이[Loop_INDEX]; vidinis_padėtis++) Lenta.직렬쓰기(kintamasis_duomenys[Loop_INDEX * 256 + vidinis_padėtis]); 단말.문자(10);
        }
    }
    static void Vykdyti_komanda(int[] duomenys_ARRAY, int 시작변위, int įrašas_COUNT, int 중첩깊이) {
        if (중첩깊이 >= 4 || įrašas_COUNT > 4096) { KLAIDA("Komanda 파일의 įdėjimas_VALUE 또는 Eilutė 길이 제한을 넘었습니다"); return; }
        for (int Loop_INDEX = 0; Loop_INDEX < įrašas_COUNT; Loop_INDEX++) ŠALTINIS[중첩깊이 * 4096 + Loop_INDEX] = duomenys_ARRAY[시작변위 + Loop_INDEX];
        int bendras_COUNT = Skaitymas(įrašas_COUNT, 중첩깊이); if (bendras_COUNT < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < bendras_COUNT) {
            int Grupė_baigti_pokalbį = 읽는자리;
            while (Grupė_baigti_pokalbį < bendras_COUNT && (종류[중첩깊이 * 128 + Grupė_baigti_pokalbį] == 0 || 종류[중첩깊이 * 128 + Grupė_baigti_pokalbį] >= 4)) Grupė_baigti_pokalbį++;
            boolean Vykdyti_cc685ae5 = 조건성립 == 1 || 조건성립 == 2 && Būsena_VALUE == 0 || 조건성립 == 3 && Būsena_VALUE != 0;
            if (Vykdyti_cc685ae5) {
                boolean 이전자리 = false;
                while (읽는자리 < Grupė_baigti_pokalbį) {
                    int toliau_padėtis = 읽는자리; while (toliau_padėtis < Grupė_baigti_pokalbį && 종류[중첩깊이 * 128 + toliau_padėtis] != 4) toliau_padėtis++;
                    boolean ryšys_Stream = toliau_padėtis < Grupė_baigti_pokalbį; int 입력쪽 = -1, išeiga_puslapis = -1, 출력방식 = 0;
                    명령해석기.žetonas_COUNT = 0; 쓴수 = 0; 확장오류 = false;
                    for (int Loop_INDEX = 읽는자리; Loop_INDEX < toliau_padėtis; Loop_INDEX++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + Loop_INDEX];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { KLAIDA("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++Loop_INDEX; } else { if (išeiga_puslapis >= 0) { KLAIDA("Išvestis 전환이 겹쳤습니다"); return; } išeiga_puslapis = ++Loop_INDEX; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.žetonas_COUNT == 32) { KLAIDA("인수가 너무 많습니다"); return; }
                        int argumentas_INDEX = 명령해석기.žetonas_COUNT++; 명령해석기.시작점[argumentas_INDEX] = 쓴수;
                        if (!Word_VALUE(Loop_INDEX, 중첩깊이)) return;
                        명령해석기.길이[argumentas_INDEX] = 쓴수 - 명령해석기.시작점[argumentas_INDEX];
                    }
                    연결중 = 이전자리 || ryšys_Stream || 입력쪽 >= 0 || išeiga_puslapis >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { KLAIDA("대화형 명령과 Komanda 파일은 Į_I 전환이나 Stream_VALUE 연결에 쓸 numeris 없습니다"); return; }
                    셸입출력.Paleisti(이전자리, ryšys_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int įrašas_padėtis = 입출력바꿈 == 0 ? 입력쪽 : išeiga_puslapis; if (įrašas_padėtis < 0) continue;
                        int Start_padėtis = 쓴수; if (!Word_VALUE(įrašas_padėtis, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = atmintis_Failai.kelias_Start(쓴수 - Start_padėtis);
                        for (int vidinis_padėtis = Start_padėtis; 처리값 >= 0 && vidinis_padėtis < 쓴수; vidinis_padėtis++) 처리값 = atmintis_Failai.kelias_baitas(vidinis_padėtis - Start_padėtis, 명령해석기.žetonas_VALUE[vidinis_padėtis]);
                        if (처리값 >= 0) 처리값 = atmintis_Failai.Atverti(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.KLAIDA(처리값); Būsena_VALUE = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.įvesties_failas = 처리값; else 셸입출력.išvesties_failas = 처리값;
                    }
                    셸입출력.대화허용 = 중첩깊이 == 0 && 읽는자리 == 0 && toliau_padėtis == bendras_COUNT;
                    깊이 = 중첩깊이; 명령해석기.REZULTATAS = 0; Lenta.입출력전환(1);
                    명령해석기.Komanda();
                    Lenta.Terminalas(3);
                    int 반환값 = 명령해석기.REZULTATAS, 흐름오류 = 셸입출력.triktis_VALUE;
                    셸입출력.끝(); 연결중 = false;
                    Būsena_VALUE = 흐름오류 < 0 ? 1 : 반환값;
                    if (흐름오류 < 0) { 명령해석기.KLAIDA(흐름오류); return; }
                    if (scenarijus_baigti_pokalbį || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = toliau_padėtis + 1;
                }
            }
            if (Grupė_baigti_pokalbį < bendras_COUNT) 조건성립 = 종류[중첩깊이 * 128 + Grupė_baigti_pokalbį];
            읽는자리 = Grupė_baigti_pokalbį + 1;
        }
    }
    static void Vykdyti_Failas() {
        if (명령해석기.žetonas_COUNT != 2 || 깊이 >= 3) { 명령해석기.REZULTATAS = 2; 단말.Rašymas("사용법: sh Failas (įdėjimas_VALUE 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.KELIAS(1); if (처리값 >= 0) 처리값 = atmintis_Failai.Atverti(0);
        if (처리값 < 0) { 명령해석기.KLAIDA(처리값); return; }
        int įrašas_COUNT = 0, baitas_duomenys;
        while ((baitas_duomenys = atmintis_Failai.Skaitymas(처리값)) != 256 && baitas_duomenys >= 0 && įrašas_COUNT < 16384) scenarijus_VALUE[중첩깊이 * 16384 + įrašas_COUNT++] = baitas_duomenys;
        atmintis_Failai.Užverti(처리값); Lenta.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < įrašas_COUNT && !scenarijus_baigti_pokalbį;) {
            int baigti_pokalbį_padėtis = 읽는자리; while (baigti_pokalbį_padėtis < įrašas_COUNT && scenarijus_VALUE[중첩깊이 * 16384 + baigti_pokalbį_padėtis] != 10) baigti_pokalbį_padėtis++;
            int 유효길이 = baigti_pokalbį_padėtis - 읽는자리; if (유효길이 > 0 && scenarijus_VALUE[중첩깊이 * 16384 + baigti_pokalbį_padėtis - 1] == 13) 유효길이--;
            Vykdyti_komanda(scenarijus_VALUE, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = baigti_pokalbį_padėtis + 1;
        }
        명령해석기.REZULTATAS = Būsena_VALUE; scenarijus_baigti_pokalbį = false; 깊이 = 중첩깊이 - 1;
    }
}
