// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java umthombo_umthi -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] UMTHOMBO = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], ithokeni_ubude = new int[2048];
    static int[] engajikiyo_ixabiso = new int[4096], engajikiyo_Ukulinganisa = new int[512];
    static int[] 문자 = new int[512], ifayile_igama_I_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int umthombo_isayizi, 토큰수, 위치, 코드크기, engajikiyo_isayizi, 상수수 = 1, 출력크기, ikharakhtha_ubude;
    static boolean Impazamo;
    static int iklasi_ithokeni, iklasi_engajikiyo, 부모상수, 코드상수;
    static int[] imethodi_ufako_nkcukacha_igama = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] imethodi_isiniki_myalelo_igama = new int[512], imethodi_isiniki_myalelo_uhlobo = new int[512];
    static int[] 함수본문 = new int[32], imethodi_phela = new int[32], 함수코드 = new int[32];
    static int[] imethodi_ubude = new int[32], 함수지역 = new int[32], imethodi_igama_engajikiyo = new int[32], 함수서술 = new int[32];
    static int[] imethodi_fikelela = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] eyale_ndawo_igama = new int[128], eyale_ndawo_uhlobo = new int[128], 지역깊이 = new int[128];

    static void ukungaphumeleli_ixabiso(String 이유) {
        if (!Impazamo) {
            umsebenzisi.Bhala("javac error: "); umsebenzisi.Bhala(이유);
            umsebenzisi.Bhala(" at line ");
            int umgca = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : umthombo_isayizi;
            for (int 수 = 0; 수 < 끝; 수++) if (UMTHOMBO[수] == 10) umgca++;
            자바도구.수쓰기(umgca); umsebenzisi.bhala_ikharakhtha_ixabiso(10);
        }
        Impazamo = true;
    }
    static boolean ikharakhtha_ixabiso(int ixabiso) { return 문자이름규칙.첫글자(ixabiso); }
    static boolean inani_ixabiso(int ixabiso) { return ixabiso >= '0' && ixabiso <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || ithokeni_ubude[가] != ithokeni_ubude[나]) return false;
        for (int 수 = 0; 수 < ithokeni_ubude[가]; 수++) if (UMTHOMBO[토큰위치[가] + 수] != UMTHOMBO[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Igama_ixabiso(int ithokeni_ixabiso, String Igama_I_SMS) {
        if (ithokeni_ixabiso < 0 || ithokeni_ixabiso >= 토큰수 || ithokeni_ubude[ithokeni_ixabiso] != Igama_I_SMS.length()) return false;
        for (int 수 = 0; 수 < Igama_I_SMS.length(); 수++) if (UMTHOMBO[토큰위치[ithokeni_ixabiso] + 수] != Igama_I_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int ixabiso) { if (종류() != ixabiso) return false; 위치++; return true; }
    static void 요구(int ixabiso) { if (!받기(ixabiso)) ukungaphumeleli_ixabiso("unexpected token"); }
    static boolean 말받기(String Igama_I_SMS) { if (!Igama_ixabiso(위치, Igama_I_SMS)) return false; 위치++; return true; }
    static void 말요구(String Igama_I_SMS) { if (!말받기(Igama_I_SMS)) ukungaphumeleli_ixabiso(Igama_I_SMS); }
    static int isalathisi_ixabiso() {
        int 결과 = 위치;
        if (종류() != 256) ukungaphumeleli_ixabiso("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Phumeza = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Phumeza == ithokeni_ubude[결과];
                for (int isithuba_ufako_nkcukacha = Phumeza; 같음 && isithuba_ufako_nkcukacha < 수; isithuba_ufako_nkcukacha++) if (예약어.charAt(isithuba_ufako_nkcukacha) != UMTHOMBO[토큰위치[결과] + isithuba_ufako_nkcukacha - Phumeza]) 같음 = false;
                if (같음) ukungaphumeleli_ixabiso("reserved word cannot be an identifier");
                Phumeza = 수 + 1;
            }
        }
        return 결과;
    }
    static void sika_ixabiso() {
        int 수 = 0;
        while (수 < umthombo_isayizi && !Impazamo) {
            int ixabiso = UMTHOMBO[수], Phumeza = 수, 종류 = ixabiso;
            if (ixabiso == 32 || ixabiso == 9 || ixabiso == 10 || ixabiso == 13) { 수++; continue; }
            if (ixabiso == '/' && 수 + 1 < umthombo_isayizi && UMTHOMBO[수 + 1] == '/') {
                while (수 < umthombo_isayizi && UMTHOMBO[수] != 10) 수++;
                continue;
            }
            if (ixabiso == '/' && 수 + 1 < umthombo_isayizi && UMTHOMBO[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < umthombo_isayizi && !(UMTHOMBO[수] == '*' && UMTHOMBO[수 + 1] == '/')) 수++;
                if (수 + 1 >= umthombo_isayizi) { ukungaphumeleli_ixabiso("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (ikharakhtha_ixabiso(ixabiso)) { 종류 = 256; while (수 < umthombo_isayizi && 문자이름규칙.이어진글자(UMTHOMBO[수])) 수++; }
            else if (inani_ixabiso(ixabiso)) { 종류 = 257; while (수 < umthombo_isayizi && inani_ixabiso(UMTHOMBO[수])) 수++; }
            else if (ixabiso == '"' || ixabiso == '\'') {
                종류 = ixabiso == '"' ? 258 : 259; 수++;
                while (수 < umthombo_isayizi && UMTHOMBO[수] != ixabiso && UMTHOMBO[수] != 10 && UMTHOMBO[수] != 13) {
                    if (UMTHOMBO[수] == '\\') 수++;
                    수++;
                }
                if (수 >= umthombo_isayizi || UMTHOMBO[수] != ixabiso) { ukungaphumeleli_ixabiso("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < umthombo_isayizi) {
                    int 다음 = UMTHOMBO[수];
                    if (ixabiso == '=' && 다음 == '=') 종류 = 300;
                    if (ixabiso == '!' && 다음 == '=') 종류 = 301;
                    if (ixabiso == '<' && 다음 == '=') 종류 = 302;
                    if (ixabiso == '>' && 다음 == '=') 종류 = 303;
                    if (ixabiso == '&' && 다음 == '&') 종류 = 304;
                    if (ixabiso == '|' && 다음 == '|') 종류 = 305;
                    if (ixabiso == '+' && 다음 == '+') 종류 = 306;
                    if (ixabiso == '-' && 다음 == '-') 종류 = 307;
                    if (ixabiso == '+' && 다음 == '=') 종류 = 308;
                    if (ixabiso == '-' && 다음 == '=') 종류 = 309;
                    if (ixabiso == '*' && 다음 == '=') 종류 = 310;
                    if (ixabiso == '/' && 다음 == '=') 종류 = 311;
                    if (ixabiso == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { ukungaphumeleli_ixabiso("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Phumeza; ithokeni_ubude[토큰수++] = 수 - Phumeza;
        }
    }
    static void bhala_engajikiyo_ibhayithi(int ixabiso) {
        if (engajikiyo_isayizi == engajikiyo_ixabiso.length) { ukungaphumeleli_ixabiso("constant pool too large"); return; }
        engajikiyo_ixabiso[engajikiyo_isayizi++] = ixabiso & 255;
    }
    static void 상짧(int ixabiso) { bhala_engajikiyo_ibhayithi(ixabiso >> 8); bhala_engajikiyo_ibhayithi(ixabiso); }
    static int bhalisa_engajikiyo(int Phumeza) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = engajikiyo_Ukulinganisa[수], ubude_ixabiso = (수 + 1 < 상수수 ? engajikiyo_Ukulinganisa[수 + 1] : Phumeza) - 앞;
            if (ubude_ixabiso != engajikiyo_isayizi - Phumeza) continue;
            boolean 같음 = true;
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) if (engajikiyo_ixabiso[앞 + isithuba_ufako_nkcukacha] != engajikiyo_ixabiso[Phumeza + isithuba_ufako_nkcukacha]) 같음 = false;
            if (같음) { engajikiyo_isayizi = Phumeza; return 수; }
        }
        if (상수수 == engajikiyo_Ukulinganisa.length) { ukungaphumeleli_ixabiso("too many constants"); return 0; }
        engajikiyo_Ukulinganisa[상수수] = Phumeza;
        return 상수수++;
    }
    static void 글추가(int ixabiso) {
        if (ikharakhtha_ubude == 문자.length) { ukungaphumeleli_ixabiso("text too long"); return; }
        문자[ikharakhtha_ubude++] = ixabiso;
    }
    static void 말추가(String Igama_I_SMS) { for (int 수 = 0; 수 < Igama_I_SMS.length(); 수++) 글추가(Igama_I_SMS.charAt(수)); }
    static int ikharakhtha_engajikiyo() {
        int Phumeza = engajikiyo_isayizi; bhala_engajikiyo_ibhayithi(1); 상짧(0);
        for (int 수 = 0; 수 < ikharakhtha_ubude; 수++) {
            int ixabiso = 문자[수];
            if (ixabiso > 0 && ixabiso < 128) bhala_engajikiyo_ibhayithi(ixabiso);
            else if (ixabiso < 2048) { bhala_engajikiyo_ibhayithi(192 | ixabiso >> 6); bhala_engajikiyo_ibhayithi(128 | ixabiso & 63); }
            else { bhala_engajikiyo_ibhayithi(224 | ixabiso >> 12); bhala_engajikiyo_ibhayithi(128 | ixabiso >> 6 & 63); bhala_engajikiyo_ibhayithi(128 | ixabiso & 63); }
        }
        if (Impazamo) return 0;
        int ubude_ixabiso = engajikiyo_isayizi - Phumeza - 3;
        engajikiyo_ixabiso[Phumeza + 1] = ubude_ixabiso >> 8; engajikiyo_ixabiso[Phumeza + 2] = ubude_ixabiso & 255;
        return bhalisa_engajikiyo(Phumeza);
    }
    static int Igama_engajikiyo(String Igama_I_SMS) { ikharakhtha_ubude = 0; 말추가(Igama_I_SMS); return ikharakhtha_engajikiyo(); }
    static int ithokeni_engajikiyo(int ithokeni_ixabiso) {
        ikharakhtha_ubude = 0;
        for (int 수 = 0; 수 < ithokeni_ubude[ithokeni_ixabiso]; 수++) 글추가(UMTHOMBO[토큰위치[ithokeni_ixabiso] + 수]);
        return ikharakhtha_engajikiyo();
    }
    static int Isalathiso(int 종류, int 가, int 나) {
        int Phumeza = engajikiyo_isayizi; bhala_engajikiyo_ibhayithi(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return bhalisa_engajikiyo(Phumeza);
    }
    static int 외부참조(int 종류, String umnini_ixabiso, String Igama, String 서술) {
        int umnini_isalathisi = Isalathiso(7, Igama_engajikiyo(umnini_ixabiso), 0);
        int 이름수 = Igama_engajikiyo(Igama), 형식수 = Igama_engajikiyo(서술);
        return Isalathiso(종류, umnini_isalathisi, Isalathiso(12, 이름수, 형식수));
    }
    static void 내보내기(int ixabiso) {
        if (코드크기 == 코드.length) { ukungaphumeleli_ixabiso("bytecode too large"); return; }
        코드[코드크기++] = ixabiso & 255;
    }
    static void Umyalelo(int ixabiso, int 인수) { 내보내기(ixabiso); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int ixabiso) {
        if (ixabiso >= -1 && ixabiso <= 5) { 내보내기(ixabiso + 3); return; }
        int Phumeza = engajikiyo_isayizi; bhala_engajikiyo_ibhayithi(3); 상짧(ixabiso >>> 16); 상짧(ixabiso);
        Umyalelo(19, bhalisa_engajikiyo(Phumeza));
    }
    static int isebe(int Umyalelo) { int 결과 = 코드크기; Umyalelo(Umyalelo, 0); return 결과; }
    static void Ilinki_ixabiso(int isebe, int ithagethi_into) {
        if (Impazamo) return;
        int 거리 = ithagethi_into - isebe;
        if (거리 < -32768 || 거리 > 32767 || isebe < 0 || isebe + 2 >= 코드크기) { ukungaphumeleli_ixabiso("invalid branch"); return; }
        코드[isebe + 1] = 거리 >> 8 & 255; 코드[isebe + 2] = 거리 & 255;
    }
    static void 비교값(int Umyalelo) {
        int 참 = isebe(Umyalelo); 내보내기(3); int 끝 = isebe(167);
        Ilinki_ixabiso(참, 코드크기); 내보내기(4); Ilinki_ixabiso(끝, 코드크기);
    }
    static int fomatha_ixabiso() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        ukungaphumeleli_ixabiso("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void yongeza_fomatha(int uhlobo_ixabiso) {
        if (uhlobo_ixabiso == 0) 글추가('V');
        if (uhlobo_ixabiso == 1) 글추가('I');
        if (uhlobo_ixabiso == 2) 글추가('Z');
        if (uhlobo_ixabiso == 3) 말추가("Ljava/lang/String;");
        if (uhlobo_ixabiso == 4) 말추가("[Ljava/lang/String;");
        if (uhlobo_ixabiso == 5) 글추가('C');
        if (uhlobo_ixabiso == 6) 말추가("Ljava/io/FileInputStream;");
        if (uhlobo_ixabiso == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Inkqubo_ixabiso_ufako_nkcukacha 본문은 umsingathi javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("isiXhosa");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("ULUHLU_Store_ukungaphumeleli") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        ukungaphumeleli_ixabiso("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Igama_ixabiso(위치, "isiXhosa")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) ukungaphumeleli_ixabiso("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); iklasi_ithokeni = isalathisi_ixabiso();
        iklasi_engajikiyo = Isalathiso(7, ithokeni_engajikiyo(iklasi_ithokeni), 0);
        부모상수 = Isalathiso(7, Igama_engajikiyo("java/lang/Object"), 0); 코드상수 = Igama_engajikiyo("Code"); 요구('{');
        while (!Impazamo && 종류() != '}') {
            if (함수수 == 32) { ukungaphumeleli_ixabiso("too many methods"); break; }
            int fikelela_ufako_nkcukacha = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int INKQUBO_ixabiso = 함수수++;
            imethodi_fikelela[INKQUBO_ixabiso] = fikelela_ufako_nkcukacha | 8;
            함수반환[INKQUBO_ixabiso] = fomatha_ixabiso(); imethodi_ufako_nkcukacha_igama[INKQUBO_ixabiso] = isalathisi_ixabiso(); 요구('(');
            for (int 앞 = 0; 앞 < INKQUBO_ixabiso; 앞++) if (이름같음(imethodi_ufako_nkcukacha_igama[앞], imethodi_ufako_nkcukacha_igama[INKQUBO_ixabiso])) ukungaphumeleli_ixabiso("duplicate method (overloading unsupported)");
            while (!Impazamo && 종류() != ')') {
                int 수 = 함수인수수[INKQUBO_ixabiso];
                if (수 == 16) { ukungaphumeleli_ixabiso("too many parameters"); break; }
                int uhlobo_ixabiso = fomatha_ixabiso(); if (uhlobo_ixabiso == 0) ukungaphumeleli_ixabiso("void parameter");
                imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수] = uhlobo_ixabiso; imethodi_isiniki_myalelo_igama[INKQUBO_ixabiso * 16 + 수] = isalathisi_ixabiso();
                함수인수수[INKQUBO_ixabiso]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!Impazamo && 받기(','));
            }
            함수본문[INKQUBO_ixabiso] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) ukungaphumeleli_ixabiso("unclosed method body");
            imethodi_phela[INKQUBO_ixabiso] = 위치;
            imethodi_igama_engajikiyo[INKQUBO_ixabiso] = ithokeni_engajikiyo(imethodi_ufako_nkcukacha_igama[INKQUBO_ixabiso]);
            ikharakhtha_ubude = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[INKQUBO_ixabiso]; 수++) yongeza_fomatha(imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수]);
            글추가(')'); yongeza_fomatha(함수반환[INKQUBO_ixabiso]); 함수서술[INKQUBO_ixabiso] = ikharakhtha_engajikiyo();
        }
        요구('}'); if (위치 != 토큰수) ukungaphumeleli_ixabiso("extra input after class");
    }
    static int fumana_eyale_ndawo(int Igama) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(eyale_ndawo_igama[수], Igama)) return 수;
        ukungaphumeleli_ixabiso("unknown variable"); return 0;
    }
    static int yongeza_eyale_ndawo(int Igama, int uhlobo_ixabiso) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(eyale_ndawo_igama[수], Igama)) ukungaphumeleli_ixabiso("duplicate local variable");
        if (지역수 == 128) { ukungaphumeleli_ixabiso("too many locals"); return 0; }
        eyale_ndawo_igama[지역수] = Igama; eyale_ndawo_uhlobo[지역수] = uhlobo_ixabiso; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean inani_elipheleleyo_uhlobo(int uhlobo_ixabiso) { return uhlobo_ixabiso == 1 || uhlobo_ixabiso == 5; }
    static void 지역읽기(int 수) { 내보내기(eyale_ndawo_uhlobo[수] <= 2 || eyale_ndawo_uhlobo[수] == 5 ? 21 : 25); 내보내기(수); }
    static void bhala_eyale_ndawo(int 수) { 내보내기(eyale_ndawo_uhlobo[수] <= 2 || eyale_ndawo_uhlobo[수] == 5 ? 54 : 58); 내보내기(수); }
    static void ngqinisisa_uhlobo(int eyona_yenzekileyo_iingcombolo, int 기대) { if (eyona_yenzekileyo_iingcombolo != 기대 && !(eyona_yenzekileyo_iingcombolo == 5 && 기대 == 1)) ukungaphumeleli_ixabiso("type mismatch"); }
    static void 문자읽기(int ithokeni_ixabiso) {
        ikharakhtha_ubude = 0; int Phumeza = 토큰위치[ithokeni_ixabiso] + 1, 끝 = 토큰위치[ithokeni_ixabiso] + ithokeni_ubude[ithokeni_ixabiso] - 1;
        while (Phumeza < 끝 && !Impazamo) {
            int ixabiso = UMTHOMBO[Phumeza++];
            if (ixabiso == '\\') {
                if (Phumeza == 끝) { ukungaphumeleli_ixabiso("invalid escape"); break; }
                ixabiso = UMTHOMBO[Phumeza++];
                if (ixabiso == 'n') ixabiso = 10;
                else if (ixabiso == 'r') ixabiso = 13;
                else if (ixabiso == 't') ixabiso = 9;
                else if (ixabiso == 'b') ixabiso = 8;
                else if (ixabiso == 'f') ixabiso = 12;
                else if (ixabiso != '\\' && ixabiso != '"' && ixabiso != '\'') ukungaphumeleli_ixabiso("unsupported escape");
            }
            글추가(ixabiso);
        }
    }
    static int ingcaciso_yegama_inani_elipheleleyo(int ithokeni_ixabiso, boolean 음수) {
        if (ithokeni_ubude[ithokeni_ixabiso] > 1 && UMTHOMBO[토큰위치[ithokeni_ixabiso]] == '0') ukungaphumeleli_ixabiso("octal literals unsupported");
        int ixabiso = 0;
        for (int 수 = 0; 수 < ithokeni_ubude[ithokeni_ixabiso]; 수++) {
            int inani_into = UMTHOMBO[토큰위치[ithokeni_ixabiso] + 수] - '0';
            if (ixabiso < -214748364 || ixabiso == -214748364 && inani_into > (음수 ? 8 : 7)) ukungaphumeleli_ixabiso("integer literal out of range");
            ixabiso = ixabiso * 10 - inani_into;
        }
        return 음수 ? ixabiso : -ixabiso;
    }
    static int 기본식() {
        if (말받기("new")) {
            int uhlobo_ixabiso = fomatha_ixabiso();
            if (uhlobo_ixabiso != 6 && uhlobo_ixabiso != 7) { ukungaphumeleli_ixabiso("only file streams supported by new in source"); return 0; }
            String umnini_ixabiso = uhlobo_ixabiso == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Umyalelo(187, Isalathiso(7, Igama_engajikiyo(umnini_ixabiso), 0)); 내보내기(89);
            요구('('); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 3); boolean 이어 = false;
            if (받기(',')) { if (uhlobo_ixabiso != 7) ukungaphumeleli_ixabiso("input stream constructor arguments"); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 2); 이어 = true; }
            요구(')');
            Umyalelo(183, 외부참조(10, umnini_ixabiso, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return uhlobo_ixabiso;
        }
        if (받기('(')) { int uhlobo_ixabiso = usetyenziso_oluxubileyo_ixabiso(); 요구(')'); return uhlobo_ixabiso; }
        if (종류() == 257) { 수상수(ingcaciso_yegama_inani_elipheleleyo(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Umyalelo(19, Isalathiso(8, ikharakhtha_engajikiyo(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (ikharakhtha_ubude != 1) ukungaphumeleli_ixabiso("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("isiXhosa")) {
            요구('.'); 말요구("자체"); 요구('.');
            String umnini_ixabiso = "", imethodi_ixabiso = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                umnini_ixabiso = "isiXhosa/자체/출력"; 요구('.');
                if (말받기("bhala_umgca")) { imethodi_ixabiso = "bhala_umgca"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Bhala")) { imethodi_ixabiso = "Bhala"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { imethodi_ixabiso = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else ukungaphumeleli_ixabiso("unknown Korean output method");
            } else if (말받기("문자")) {
                umnini_ixabiso = "isiXhosa/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("ubude_ixabiso")) { imethodi_ixabiso = "ubude_ixabiso"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { imethodi_ixabiso = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("ingcaciso_yegama_inani_elipheleleyo")) { imethodi_ixabiso = "ingcaciso_yegama_inani_elipheleleyo"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("bhala_inani_elipheleleyo_ixabiso")) { imethodi_ixabiso = "bhala_inani_elipheleleyo_ixabiso"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { imethodi_ixabiso = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("beka_I_SMS")) { imethodi_ixabiso = "beka_I_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("sika_ixabiso")) { imethodi_ixabiso = "sika_ixabiso"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else ukungaphumeleli_ixabiso("unknown Korean text method");
            } else if (말받기("iFayili")) {
                umnini_ixabiso = "isiXhosa/자체/iFayili"; 요구('.'); 가 = 3;
                if (말받기("Funda")) { imethodi_ixabiso = "Funda"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Bhala")) { imethodi_ixabiso = "Bhala"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else ukungaphumeleli_ixabiso("unknown Korean file method");
            } else if (말받기("화면")) {
                umnini_ixabiso = "isiXhosa/자체/화면"; 요구('.');
                if (말받기("너비")) { imethodi_ixabiso = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { imethodi_ixabiso = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { imethodi_ixabiso = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { imethodi_ixabiso = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { imethodi_ixabiso = "기다리기"; 서술 = "()V"; }
                else ukungaphumeleli_ixabiso("unknown Korean framebuffer method");
            } else ukungaphumeleli_ixabiso("unsupported Korean library class");
            요구('('); if (가 != 0) ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 가);
            if (나 != 0) { 요구(','); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 나); }
            if (다 != 0) { 요구(','); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 다); }
            if (라 != 0) { 요구(','); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 라); }
            if (마 != 0) { 요구(','); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 마); }
            요구(')'); Umyalelo(184, 외부참조(10, umnini_ixabiso, imethodi_ixabiso, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 3); 요구(')');
            Umyalelo(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Igama = isalathisi_ixabiso();
        if (받기('(')) {
            int INKQUBO_ixabiso = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Igama, imethodi_ufako_nkcukacha_igama[수])) INKQUBO_ixabiso = 수;
            if (INKQUBO_ixabiso < 0) { ukungaphumeleli_ixabiso("unknown static method"); return 0; }
            int 수 = 0;
            while (!Impazamo && 종류() != ')') {
                if (수 >= 함수인수수[INKQUBO_ixabiso]) { ukungaphumeleli_ixabiso("too many arguments"); break; }
                ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[INKQUBO_ixabiso]) ukungaphumeleli_ixabiso("argument count mismatch");
            Umyalelo(184, Isalathiso(10, iklasi_engajikiyo, Isalathiso(12, imethodi_igama_engajikiyo[INKQUBO_ixabiso], 함수서술[INKQUBO_ixabiso])));
            return 함수반환[INKQUBO_ixabiso];
        }
        int eyale_ndawo_umda = fumana_eyale_ndawo(Igama), uhlobo_ixabiso = eyale_ndawo_uhlobo[eyale_ndawo_umda]; 지역읽기(eyale_ndawo_umda);
        while (!Impazamo) {
            if (받기('[')) { ngqinisisa_uhlobo(uhlobo_ixabiso, 4); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 1); 요구(']'); 내보내기(50); uhlobo_ixabiso = 3; }
            else if (받기('.')) {
                if (uhlobo_ixabiso == 6 || uhlobo_ixabiso == 7) {
                    String umnini_ixabiso = uhlobo_ixabiso == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Umyalelo(182, 외부참조(10, umnini_ixabiso, "close", "()V")); uhlobo_ixabiso = 0; }
                    else if (uhlobo_ixabiso == 6 && 말받기("read")) { 요구('('); 요구(')'); Umyalelo(182, 외부참조(10, umnini_ixabiso, "read", "()I")); uhlobo_ixabiso = 1; }
                    else if (uhlobo_ixabiso == 7 && 말받기("write")) { 요구('('); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 1); 요구(')'); Umyalelo(182, 외부참조(10, umnini_ixabiso, "write", "(I)V")); uhlobo_ixabiso = 0; }
                    else { ukungaphumeleli_ixabiso("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (uhlobo_ixabiso == 4) { 내보내기(190); uhlobo_ixabiso = 1; }
                else { ngqinisisa_uhlobo(uhlobo_ixabiso, 3); 요구('('); 요구(')'); Umyalelo(182, 외부참조(10, "java/lang/String", "length", "()I")); uhlobo_ixabiso = 1; }
            } else break;
        }
        return uhlobo_ixabiso;
    }
    static int 단항() {
        if (++식깊이 > 64) { ukungaphumeleli_ixabiso("expression nesting too deep"); 식깊이--; return 0; }
        int uhlobo_ixabiso;
        if (받기('!')) { ngqinisisa_uhlobo(단항(), 2); 비교값(153); uhlobo_ixabiso = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(ingcaciso_yegama_inani_elipheleleyo(위치++, true));
            else { ngqinisisa_uhlobo(단항(), 1); 내보내기(116); }
            uhlobo_ixabiso = 1;
        } else if (받기('+')) { ngqinisisa_uhlobo(단항(), 1); uhlobo_ixabiso = 1; }
        else uhlobo_ixabiso = 기본식();
        식깊이--; return uhlobo_ixabiso;
    }
    static int 곱식() {
        int uhlobo_ixabiso = 단항();
        while (!Impazamo && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = 종류(); 위치++; ngqinisisa_uhlobo(uhlobo_ixabiso, 1); ngqinisisa_uhlobo(단항(), 1);
            내보내기(ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '*' ? 104 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '/' ? 108 : 112); uhlobo_ixabiso = 1;
        }
        return uhlobo_ixabiso;
    }
    static int 합식() {
        int uhlobo_ixabiso = 곱식();
        while (!Impazamo && (종류() == '+' || 종류() == '-')) {
            int ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = 종류(); 위치++; int 경계 = 코드크기, Emva_ixabiso_uhlobo = 곱식();
            if (ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '+' && (uhlobo_ixabiso == 3 || Emva_ixabiso_uhlobo == 3)) { 결합(경계, uhlobo_ixabiso, Emva_ixabiso_uhlobo); uhlobo_ixabiso = 3; }
            else { ngqinisisa_uhlobo(uhlobo_ixabiso, 1); ngqinisisa_uhlobo(Emva_ixabiso_uhlobo, 1); 내보내기(ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '+' ? 96 : 100); uhlobo_ixabiso = 1; }
        }
        return uhlobo_ixabiso;
    }
    static int 붙임참조(int uhlobo_ixabiso) {
        if (uhlobo_ixabiso != 1 && uhlobo_ixabiso != 2 && uhlobo_ixabiso != 3 && uhlobo_ixabiso != 5) ukungaphumeleli_ixabiso("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", uhlobo_ixabiso == 1 ? "(I)Ljava/lang/StringBuilder;"
            : uhlobo_ixabiso == 2 ? "(Z)Ljava/lang/StringBuilder;" : uhlobo_ixabiso == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Emva_ixabiso_uhlobo) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 usetyenziso_oluxubileyo_ixabiso 내부의 untanga_ixabiso isebe 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Umyalelo(187, Isalathiso(7, Igama_engajikiyo("java/lang/StringBuilder"), 0)); 내보내기(89);
        Umyalelo(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Umyalelo(182, 붙임참조(앞형));
        if (Impazamo) return;
        int ubude_ixabiso = 코드크기 - 끝;
        for (int 수 = 0; 수 < ubude_ixabiso; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + ubude_ixabiso] = 코드[수];
        for (int 수 = 0; 수 < ubude_ixabiso; 수++) 코드[경계 + 수] = 삽입코드[수];
        Umyalelo(182, 붙임참조(Emva_ixabiso_uhlobo)); Umyalelo(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int uhlobo_ixabiso = 합식();
        while (!Impazamo && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = 종류(); 위치++; ngqinisisa_uhlobo(uhlobo_ixabiso, 1); ngqinisisa_uhlobo(합식(), 1);
            비교값(ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '<' ? 161 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == '>' ? 163 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 302 ? 164 : 162); uhlobo_ixabiso = 2;
        }
        return uhlobo_ixabiso;
    }
    static int 동등식() {
        int uhlobo_ixabiso = 비교식();
        while (!Impazamo && (종류() == 300 || 종류() == 301)) {
            int ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = 종류(); 위치++; int Emva_ixabiso_uhlobo = 비교식();
            if (uhlobo_ixabiso == 0 || Emva_ixabiso_uhlobo == 0) ukungaphumeleli_ixabiso("void expression");
            if (!(inani_elipheleleyo_uhlobo(uhlobo_ixabiso) && inani_elipheleleyo_uhlobo(Emva_ixabiso_uhlobo))) ngqinisisa_uhlobo(Emva_ixabiso_uhlobo, uhlobo_ixabiso);
            비교값((uhlobo_ixabiso <= 2 || uhlobo_ixabiso == 5 ? 159 : 165) + (ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 301 ? 1 : 0)); uhlobo_ixabiso = 2;
        }
        return uhlobo_ixabiso;
    }
    static int 논리곱() {
        int uhlobo_ixabiso = 동등식();
        while (!Impazamo && 받기(304)) {
            ngqinisisa_uhlobo(uhlobo_ixabiso, 2); int 가 = isebe(153); ngqinisisa_uhlobo(동등식(), 2); int 나 = isebe(153);
            내보내기(4); int 끝 = isebe(167); Ilinki_ixabiso(가, 코드크기); Ilinki_ixabiso(나, 코드크기); 내보내기(3); Ilinki_ixabiso(끝, 코드크기); uhlobo_ixabiso = 2;
        }
        return uhlobo_ixabiso;
    }
    static int usetyenziso_oluxubileyo_ixabiso() {
        int uhlobo_ixabiso = 논리곱();
        while (!Impazamo && 받기(305)) {
            ngqinisisa_uhlobo(uhlobo_ixabiso, 2); int 가 = isebe(154); ngqinisisa_uhlobo(논리곱(), 2); int 나 = isebe(154);
            내보내기(3); int 끝 = isebe(167); Ilinki_ixabiso(가, 코드크기); Ilinki_ixabiso(나, 코드크기); 내보내기(4); Ilinki_ixabiso(끝, 코드크기); uhlobo_ixabiso = 2;
        }
        return uhlobo_ixabiso;
    }
    static void umsebenzi_womfundi_ixabiso(boolean 선언허용) {
        if (Igama_ixabiso(위치, "int") || Igama_ixabiso(위치, "boolean") || Igama_ixabiso(위치, "String") || Igama_ixabiso(위치, "char")
            || Igama_ixabiso(위치, "FileInputStream") || Igama_ixabiso(위치, "FileOutputStream")) {
            if (!선언허용) ukungaphumeleli_ixabiso("declaration not allowed here");
            int uhlobo_ixabiso = fomatha_ixabiso(), Igama = isalathisi_ixabiso(); 요구('='); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), uhlobo_ixabiso);
            bhala_eyale_ndawo(yongeza_eyale_ndawo(Igama, uhlobo_ixabiso)); return;
        }
        int Igama = isalathisi_ixabiso(), eyale_ndawo_umda = fumana_eyale_ndawo(Igama);
        if (받기('=')) { ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), eyale_ndawo_uhlobo[eyale_ndawo_umda]); bhala_eyale_ndawo(eyale_ndawo_umda); }
        else if (종류() >= 308 && 종류() <= 312) {
            int ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = 종류(); 위치++; 지역읽기(eyale_ndawo_umda); int 경계 = 코드크기, Emva_ixabiso_uhlobo = usetyenziso_oluxubileyo_ixabiso();
            if (ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 308 && eyale_ndawo_uhlobo[eyale_ndawo_umda] == 3) 결합(경계, 3, Emva_ixabiso_uhlobo);
            else {
                ngqinisisa_uhlobo(eyale_ndawo_uhlobo[eyale_ndawo_umda], 1); ngqinisisa_uhlobo(Emva_ixabiso_uhlobo, 1);
                내보내기(ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 308 ? 96 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 309 ? 100 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 310 ? 104 : ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 311 ? 108 : 112);
                if (eyale_ndawo_uhlobo[eyale_ndawo_umda] == 5) 내보내기(146);
            }
            bhala_eyale_ndawo(eyale_ndawo_umda);
        }
        else if (종류() == 306 || 종류() == 307) {
            ngqinisisa_uhlobo(eyale_ndawo_uhlobo[eyale_ndawo_umda], 1); 내보내기(132); 내보내기(eyale_ndawo_umda); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (eyale_ndawo_uhlobo[eyale_ndawo_umda] == 5) { 지역읽기(eyale_ndawo_umda); 내보내기(146); bhala_eyale_ndawo(eyale_ndawo_umda); }
        } else ukungaphumeleli_ixabiso("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Umyalelo(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean engenanto_isiniki_myalelo = 종류() == ')';
        int uhlobo_ixabiso = engenanto_isiniki_myalelo ? 0 : usetyenziso_oluxubileyo_ixabiso(); 요구(')'); 요구(';');
        String 서술 = uhlobo_ixabiso == 0 ? "()V" : uhlobo_ixabiso == 1 ? "(I)V" : uhlobo_ixabiso == 2 ? "(Z)V" : uhlobo_ixabiso == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (uhlobo_ixabiso == 4 || uhlobo_ixabiso >= 6 || uhlobo_ixabiso == 0 && (!줄바꿈 || !engenanto_isiniki_myalelo)) ukungaphumeleli_ixabiso("unsupported print argument");
        Umyalelo(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean ingxelo_ixabiso() {
        if (Impazamo) return false;
        if (깊이 > 32) { ukungaphumeleli_ixabiso("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Impazamo && 종류() != '}') { if (반환) ukungaphumeleli_ixabiso("unreachable statement"); 반환 = ingxelo_ixabiso(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int uhlobo_ixabiso = 종류() == ';' ? 0 : usetyenziso_oluxubileyo_ixabiso(); ngqinisisa_uhlobo(uhlobo_ixabiso, 함수반환[현재함수]); 요구(';');
            내보내기(uhlobo_ixabiso == 0 ? 177 : uhlobo_ixabiso <= 2 || uhlobo_ixabiso == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 2); 요구(')'); int 거짓 = isebe(153);
            깊이++; boolean 가 = isilawuli_ingxelo(); 깊이--;
            if (말받기("else")) { int 끝 = isebe(167); Ilinki_ixabiso(거짓, 코드크기); 깊이++; boolean 나 = isilawuli_ingxelo(); 깊이--; Ilinki_ixabiso(끝, 코드크기); return 가 && 나; }
            Ilinki_ixabiso(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Phumeza = 코드크기; 요구('('); ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 2); 요구(')'); int 끝 = isebe(153);
            깊이++; isilawuli_ingxelo(); 깊이--; Ilinki_ixabiso(isebe(167), Phumeza); Ilinki_ixabiso(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') umsebenzi_womfundi_ixabiso(true); 요구(';');
            int imo = 코드크기; if (종류() == ';') 내보내기(4); else ngqinisisa_uhlobo(usetyenziso_oluxubileyo_ixabiso(), 2); 요구(';');
            int 끝 = isebe(153), isiqu_sombhalo = isebe(167), qalela_ngokutsha = 코드크기;
            if (종류() != ')') umsebenzi_womfundi_ixabiso(false); 요구(')'); Ilinki_ixabiso(isebe(167), imo); Ilinki_ixabiso(isiqu_sombhalo, 코드크기);
            isilawuli_ingxelo(); Ilinki_ixabiso(isebe(167), qalela_ngokutsha); Ilinki_ixabiso(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Igama_ixabiso(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int uhlobo_ixabiso = usetyenziso_oluxubileyo_ixabiso(); if (uhlobo_ixabiso != 0) 내보내기(87); 요구(';'); return false;
        }
        umsebenzi_womfundi_ixabiso(true); 요구(';'); return false;
    }
    static boolean isilawuli_ingxelo() {
        if (Igama_ixabiso(위치, "int") || Igama_ixabiso(위치, "boolean") || Igama_ixabiso(위치, "char") || Igama_ixabiso(위치, "String")
            || Igama_ixabiso(위치, "FileInputStream") || Igama_ixabiso(위치, "FileOutputStream")) ukungaphumeleli_ixabiso("local declaration requires braces");
        return ingxelo_ixabiso();
    }
    static void 출바(int ixabiso) { if (출력크기 == 출력.length) ukungaphumeleli_ixabiso("class file too large"); else 출력[출력크기++] = ixabiso & 255; }
    static void 출짧(int ixabiso) { 출바(ixabiso >> 8); 출바(ixabiso); }
    static void 출정(int ixabiso) { 출짧(ixabiso >>> 16); 출짧(ixabiso); }
    static void bhala_iklasi() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < engajikiyo_isayizi; 수++) 출바(engajikiyo_ixabiso[수]);
        출짧(0x21); 출짧(iklasi_engajikiyo); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(imethodi_fikelela[수]); 출짧(imethodi_igama_engajikiyo[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + imethodi_ubude[수]); 출짧(128); 출짧(함수지역[수]); 출정(imethodi_ubude[수]);
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < imethodi_ubude[수]; isithuba_ufako_nkcukacha++) 출바(코드[함수코드[수] + isithuba_ufako_nkcukacha]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Phumeza() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() != 1) { umsebenzisi.Bhala("Usage: javac FILE.java\n"); return 2; }
        int igama_isayizi = 자바도구.Igama(ifayile_igama_I_SMS, umsebenzisi.인수(0));
        if (igama_isayizi < 6 || igama_isayizi > 62 || ifayile_igama_I_SMS[igama_isayizi - 5] != '.' || ifayile_igama_I_SMS[igama_isayizi - 4] != 'j'
            || ifayile_igama_I_SMS[igama_isayizi - 3] != 'a' || ifayile_igama_I_SMS[igama_isayizi - 2] != 'v' || ifayile_igama_I_SMS[igama_isayizi - 1] != 'a') {
            umsebenzisi.Bhala("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        umthombo_isayizi = umsebenzisi.파일읽기(ifayile_igama_I_SMS, UMTHOMBO);
        if (umthombo_isayizi < 0) { umsebenzisi.Bhala("javac: cannot read source: "); 자바도구.수쓰기(umthombo_isayizi); umsebenzisi.bhala_ikharakhtha_ixabiso(10); return 1; }
        umthombo_isayizi = 자바도구.원문해독(UMTHOMBO, umthombo_isayizi);
        if (umthombo_isayizi < 0) { umsebenzisi.Bhala("javac error: invalid UTF-8 source\n"); return 1; }
        sika_ixabiso(); if (!Impazamo) 선언읽기();
        if (!Impazamo) {
            if (ithokeni_ubude[iklasi_ithokeni] != igama_isayizi - 5) ukungaphumeleli_ixabiso("class name must match file name");
            for (int 수 = 0; 수 < igama_isayizi - 5; 수++) if (UMTHOMBO[토큰위치[iklasi_ithokeni] + 수] != ifayile_igama_I_SMS[수]) ukungaphumeleli_ixabiso("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !Impazamo; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) yongeza_eyale_ndawo(imethodi_isiniki_myalelo_igama[현재함수 * 16 + 수], imethodi_isiniki_myalelo_uhlobo[현재함수 * 16 + 수]);
            boolean 반환 = ingxelo_ixabiso();
            if (!반환 && 함수반환[현재함수] != 0) ukungaphumeleli_ixabiso("missing return");
            // isebe 뒤의 합류 지점은 반드시 eyona_yenzekileyo_iingcombolo 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean inani_elipheleleyo = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(inani_elipheleleyo ? 3 : 1); 내보내기(inani_elipheleleyo ? 172 : 176); }
            if (위치 != imethodi_phela[현재함수]) ukungaphumeleli_ixabiso("invalid method body");
            함수지역[현재함수] = 지역수; imethodi_ubude[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (Impazamo) return 1;
        bhala_iklasi(); if (Impazamo) return 1;
        ifayile_igama_I_SMS[igama_isayizi - 4] = 'c'; ifayile_igama_I_SMS[igama_isayizi - 3] = 'l'; ifayile_igama_I_SMS[igama_isayizi - 2] = 'a';
        ifayile_igama_I_SMS[igama_isayizi - 1] = 's'; ifayile_igama_I_SMS[igama_isayizi] = 's'; ifayile_igama_I_SMS[igama_isayizi + 1] = 0;
        int 결과 = umsebenzisi.bhala_ifayile(ifayile_igama_I_SMS, 출력, 출력크기);
        if (결과 < 0) { umsebenzisi.Bhala("javac: cannot save class: "); 자바도구.수쓰기(결과); umsebenzisi.bhala_ikharakhtha_ixabiso(10); return 1; }
        umsebenzisi.Bhala("Compiled: "); for (int 수 = 0; ifayile_igama_I_SMS[수] != 0; 수++) umsebenzisi.bhala_ikharakhtha_ixabiso(ifayile_igama_I_SMS[수]);
        umsebenzisi.Bhala(" (JVM class version 49)\n"); return 0;
    }
}
