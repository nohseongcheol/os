// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java ebensìbịa_èsèrèsè_osisi -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] ebensìbịa = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], akara_ogologo = new int[2048];
    static int[] ihendịgide_valuu = new int[4096], ihendịgide_Nnokwata = new int[512];
    static int[] 문자 = new int[512], ọbọakwụkwọ_akara_ahà_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int ebensìbịa_ụha, 토큰수, 위치, 코드크기, ihendịgide_ụha, 상수수 = 1, 출력크기, mkpụrụedemede_ogologo;
    static boolean mmejọ;
    static int klaàsị_akara, klaàsị_ihendịgide, 부모상수, 코드상수;
    static int[] usoro_ndebà_akara_ahà = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] usoro_agụment_akara_ahà = new int[512], usoro_agụment_pinye = new int[512];
    static int[] 함수본문 = new int[32], usoro_mèdebe = new int[32], 함수코드 = new int[32];
    static int[] usoro_ogologo = new int[32], 함수지역 = new int[32], usoro_akara_ahà_ihendịgide = new int[32], 함수서술 = new int[32];
    static int[] usoro_òhèrè = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] otù_ebe_akara_ahà = new int[128], otù_ebe_pinye = new int[128], 지역깊이 = new int[128];

    static void ọdịdà_valuu(String 이유) {
        if (!mmejọ) {
            òjìàrụ.Chekwaa_ozi("javac error: "); òjìàrụ.Chekwaa_ozi(이유);
            òjìàrụ.Chekwaa_ozi(" at line ");
            int ahịrī = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : ebensìbịa_ụha;
            for (int 수 = 0; 수 < 끝; 수++) if (ebensìbịa[수] == 10) ahịrī++;
            자바도구.수쓰기(ahịrī); òjìàrụ.dee_mkpụrụedemede_valuu(10);
        }
        mmejọ = true;
    }
    static boolean mkpụrụedemede_valuu(int valuu) { return 문자이름규칙.첫글자(valuu); }
    static boolean ọbula_valuu(int valuu) { return valuu >= '0' && valuu <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || akara_ogologo[가] != akara_ogologo[나]) return false;
        for (int 수 = 0; 수 < akara_ogologo[가]; 수++) if (ebensìbịa[토큰위치[가] + 수] != ebensìbịa[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Mkpụrụokwu_valuu(int akara_valuu_eb540501, String Mkpụrụokwu_SMS) {
        if (akara_valuu_eb540501 < 0 || akara_valuu_eb540501 >= 토큰수 || akara_ogologo[akara_valuu_eb540501] != Mkpụrụokwu_SMS.length()) return false;
        for (int 수 = 0; 수 < Mkpụrụokwu_SMS.length(); 수++) if (ebensìbịa[토큰위치[akara_valuu_eb540501] + 수] != Mkpụrụokwu_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int valuu) { if (종류() != valuu) return false; 위치++; return true; }
    static void 요구(int valuu) { if (!받기(valuu)) ọdịdà_valuu("unexpected token"); }
    static boolean 말받기(String Mkpụrụokwu_SMS) { if (!Mkpụrụokwu_valuu(위치, Mkpụrụokwu_SMS)) return false; 위치++; return true; }
    static void 말요구(String Mkpụrụokwu_SMS) { if (!말받기(Mkpụrụokwu_SMS)) ọdịdà_valuu(Mkpụrụokwu_SMS); }
    static int ihe_nkọwapụta_valuu() {
        int 결과 = 위치;
        if (종류() != 256) ọdịdà_valuu("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Bido = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Bido == akara_ogologo[결과];
                for (int oghere_ndebà = Bido; 같음 && oghere_ndebà < 수; oghere_ndebà++) if (예약어.charAt(oghere_ndebà) != ebensìbịa[토큰위치[결과] + oghere_ndebà - Bido]) 같음 = false;
                if (같음) ọdịdà_valuu("reserved word cannot be an identifier");
                Bido = 수 + 1;
            }
        }
        return 결과;
    }
    static void gbubìte_valuu() {
        int 수 = 0;
        while (수 < ebensìbịa_ụha && !mmejọ) {
            int valuu = ebensìbịa[수], Bido = 수, 종류 = valuu;
            if (valuu == 32 || valuu == 9 || valuu == 10 || valuu == 13) { 수++; continue; }
            if (valuu == '/' && 수 + 1 < ebensìbịa_ụha && ebensìbịa[수 + 1] == '/') {
                while (수 < ebensìbịa_ụha && ebensìbịa[수] != 10) 수++;
                continue;
            }
            if (valuu == '/' && 수 + 1 < ebensìbịa_ụha && ebensìbịa[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < ebensìbịa_ụha && !(ebensìbịa[수] == '*' && ebensìbịa[수 + 1] == '/')) 수++;
                if (수 + 1 >= ebensìbịa_ụha) { ọdịdà_valuu("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (mkpụrụedemede_valuu(valuu)) { 종류 = 256; while (수 < ebensìbịa_ụha && 문자이름규칙.이어진글자(ebensìbịa[수])) 수++; }
            else if (ọbula_valuu(valuu)) { 종류 = 257; while (수 < ebensìbịa_ụha && ọbula_valuu(ebensìbịa[수])) 수++; }
            else if (valuu == '"' || valuu == '\'') {
                종류 = valuu == '"' ? 258 : 259; 수++;
                while (수 < ebensìbịa_ụha && ebensìbịa[수] != valuu && ebensìbịa[수] != 10 && ebensìbịa[수] != 13) {
                    if (ebensìbịa[수] == '\\') 수++;
                    수++;
                }
                if (수 >= ebensìbịa_ụha || ebensìbịa[수] != valuu) { ọdịdà_valuu("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < ebensìbịa_ụha) {
                    int 다음 = ebensìbịa[수];
                    if (valuu == '=' && 다음 == '=') 종류 = 300;
                    if (valuu == '!' && 다음 == '=') 종류 = 301;
                    if (valuu == '<' && 다음 == '=') 종류 = 302;
                    if (valuu == '>' && 다음 == '=') 종류 = 303;
                    if (valuu == '&' && 다음 == '&') 종류 = 304;
                    if (valuu == '|' && 다음 == '|') 종류 = 305;
                    if (valuu == '+' && 다음 == '+') 종류 = 306;
                    if (valuu == '-' && 다음 == '-') 종류 = 307;
                    if (valuu == '+' && 다음 == '=') 종류 = 308;
                    if (valuu == '-' && 다음 == '=') 종류 = 309;
                    if (valuu == '*' && 다음 == '=') 종류 = 310;
                    if (valuu == '/' && 다음 == '=') 종류 = 311;
                    if (valuu == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { ọdịdà_valuu("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Bido; akara_ogologo[토큰수++] = 수 - Bido;
        }
    }
    static void dee_ihendịgide_baịtị(int valuu) {
        if (ihendịgide_ụha == ihendịgide_valuu.length) { ọdịdà_valuu("constant pool too large"); return; }
        ihendịgide_valuu[ihendịgide_ụha++] = valuu & 255;
    }
    static void 상짧(int valuu) { dee_ihendịgide_baịtị(valuu >> 8); dee_ihendịgide_baịtị(valuu); }
    static int 상등록(int Bido) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = ihendịgide_Nnokwata[수], ogologo_valuu = (수 + 1 < 상수수 ? ihendịgide_Nnokwata[수 + 1] : Bido) - 앞;
            if (ogologo_valuu != ihendịgide_ụha - Bido) continue;
            boolean 같음 = true;
            for (int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) if (ihendịgide_valuu[앞 + oghere_ndebà] != ihendịgide_valuu[Bido + oghere_ndebà]) 같음 = false;
            if (같음) { ihendịgide_ụha = Bido; return 수; }
        }
        if (상수수 == ihendịgide_Nnokwata.length) { ọdịdà_valuu("too many constants"); return 0; }
        ihendịgide_Nnokwata[상수수] = Bido;
        return 상수수++;
    }
    static void 글추가(int valuu) {
        if (mkpụrụedemede_ogologo == 문자.length) { ọdịdà_valuu("text too long"); return; }
        문자[mkpụrụedemede_ogologo++] = valuu;
    }
    static void 말추가(String Mkpụrụokwu_SMS) { for (int 수 = 0; 수 < Mkpụrụokwu_SMS.length(); 수++) 글추가(Mkpụrụokwu_SMS.charAt(수)); }
    static int mkpụrụedemede_ihendịgide() {
        int Bido = ihendịgide_ụha; dee_ihendịgide_baịtị(1); 상짧(0);
        for (int 수 = 0; 수 < mkpụrụedemede_ogologo; 수++) {
            int valuu = 문자[수];
            if (valuu > 0 && valuu < 128) dee_ihendịgide_baịtị(valuu);
            else if (valuu < 2048) { dee_ihendịgide_baịtị(192 | valuu >> 6); dee_ihendịgide_baịtị(128 | valuu & 63); }
            else { dee_ihendịgide_baịtị(224 | valuu >> 12); dee_ihendịgide_baịtị(128 | valuu >> 6 & 63); dee_ihendịgide_baịtị(128 | valuu & 63); }
        }
        if (mmejọ) return 0;
        int ogologo_valuu = ihendịgide_ụha - Bido - 3;
        ihendịgide_valuu[Bido + 1] = ogologo_valuu >> 8; ihendịgide_valuu[Bido + 2] = ogologo_valuu & 255;
        return 상등록(Bido);
    }
    static int Mkpụrụokwu_ihendịgide(String Mkpụrụokwu_SMS) { mkpụrụedemede_ogologo = 0; 말추가(Mkpụrụokwu_SMS); return mkpụrụedemede_ihendịgide(); }
    static int akara_ihendịgide(int akara_valuu_eb540501) {
        mkpụrụedemede_ogologo = 0;
        for (int 수 = 0; 수 < akara_ogologo[akara_valuu_eb540501]; 수++) 글추가(ebensìbịa[토큰위치[akara_valuu_eb540501] + 수]);
        return mkpụrụedemede_ihendịgide();
    }
    static int Nrụtụ_aka(int 종류, int 가, int 나) {
        int Bido = ihendịgide_ụha; dee_ihendịgide_baịtị(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return 상등록(Bido);
    }
    static int 외부참조(int 종류, String nwe_valuu, String Aha, String 서술) {
        int nwe_ihe_nkọwapụta = Nrụtụ_aka(7, Mkpụrụokwu_ihendịgide(nwe_valuu), 0);
        int 이름수 = Mkpụrụokwu_ihendịgide(Aha), 형식수 = Mkpụrụokwu_ihendịgide(서술);
        return Nrụtụ_aka(종류, nwe_ihe_nkọwapụta, Nrụtụ_aka(12, 이름수, 형식수));
    }
    static void 내보내기(int valuu) {
        if (코드크기 == 코드.length) { ọdịdà_valuu("bytecode too large"); return; }
        코드[코드크기++] = valuu & 255;
    }
    static void Ntiiwu(int valuu, int 인수) { 내보내기(valuu); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int valuu) {
        if (valuu >= -1 && valuu <= 5) { 내보내기(valuu + 3); return; }
        int Bido = ihendịgide_ụha; dee_ihendịgide_baịtị(3); 상짧(valuu >>> 16); 상짧(valuu);
        Ntiiwu(19, 상등록(Bido));
    }
    static int ogbè(int Ntiiwu) { int 결과 = 코드크기; Ntiiwu(Ntiiwu, 0); return 결과; }
    static void Njikọ_valuu(int ogbè, int ebenlereanya_ihe) {
        if (mmejọ) return;
        int 거리 = ebenlereanya_ihe - ogbè;
        if (거리 < -32768 || 거리 > 32767 || ogbè < 0 || ogbè + 2 >= 코드크기) { ọdịdà_valuu("invalid branch"); return; }
        코드[ogbè + 1] = 거리 >> 8 & 255; 코드[ogbè + 2] = 거리 & 255;
    }
    static void 비교값(int Ntiiwu) {
        int 참 = ogbè(Ntiiwu); 내보내기(3); int 끝 = ogbè(167);
        Njikọ_valuu(참, 코드크기); 내보내기(4); Njikọ_valuu(끝, 코드크기);
    }
    static int hàzie_valuu() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        ọdịdà_valuu("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void gbakwụnye_hàzie(int pinye_valuu) {
        if (pinye_valuu == 0) 글추가('V');
        if (pinye_valuu == 1) 글추가('I');
        if (pinye_valuu == 2) 글추가('Z');
        if (pinye_valuu == 3) 말추가("Ljava/lang/String;");
        if (pinye_valuu == 4) 말추가("[Ljava/lang/String;");
        if (pinye_valuu == 5) 글추가('C');
        if (pinye_valuu == 6) 말추가("Ljava/io/FileInputStream;");
        if (pinye_valuu == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 ùsòrò_valuu_ndebà 본문은 usu javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("MKPOKỌTA_Store_ọdịdà") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        ọdịdà_valuu("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Mkpụrụokwu_valuu(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) ọdịdà_valuu("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); klaàsị_akara = ihe_nkọwapụta_valuu();
        klaàsị_ihendịgide = Nrụtụ_aka(7, akara_ihendịgide(klaàsị_akara), 0);
        부모상수 = Nrụtụ_aka(7, Mkpụrụokwu_ihendịgide("java/lang/Object"), 0); 코드상수 = Mkpụrụokwu_ihendịgide("Code"); 요구('{');
        while (!mmejọ && 종류() != '}') {
            if (함수수 == 32) { ọdịdà_valuu("too many methods"); break; }
            int òhèrè_ndebà = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int ọrụ_valuu = 함수수++;
            usoro_òhèrè[ọrụ_valuu] = òhèrè_ndebà | 8;
            함수반환[ọrụ_valuu] = hàzie_valuu(); usoro_ndebà_akara_ahà[ọrụ_valuu] = ihe_nkọwapụta_valuu(); 요구('(');
            for (int 앞 = 0; 앞 < ọrụ_valuu; 앞++) if (이름같음(usoro_ndebà_akara_ahà[앞], usoro_ndebà_akara_ahà[ọrụ_valuu])) ọdịdà_valuu("duplicate method (overloading unsupported)");
            while (!mmejọ && 종류() != ')') {
                int 수 = 함수인수수[ọrụ_valuu];
                if (수 == 16) { ọdịdà_valuu("too many parameters"); break; }
                int pinye_valuu = hàzie_valuu(); if (pinye_valuu == 0) ọdịdà_valuu("void parameter");
                usoro_agụment_pinye[ọrụ_valuu * 16 + 수] = pinye_valuu; usoro_agụment_akara_ahà[ọrụ_valuu * 16 + 수] = ihe_nkọwapụta_valuu();
                함수인수수[ọrụ_valuu]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!mmejọ && 받기(','));
            }
            함수본문[ọrụ_valuu] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) ọdịdà_valuu("unclosed method body");
            usoro_mèdebe[ọrụ_valuu] = 위치;
            usoro_akara_ahà_ihendịgide[ọrụ_valuu] = akara_ihendịgide(usoro_ndebà_akara_ahà[ọrụ_valuu]);
            mkpụrụedemede_ogologo = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[ọrụ_valuu]; 수++) gbakwụnye_hàzie(usoro_agụment_pinye[ọrụ_valuu * 16 + 수]);
            글추가(')'); gbakwụnye_hàzie(함수반환[ọrụ_valuu]); 함수서술[ọrụ_valuu] = mkpụrụedemede_ihendịgide();
        }
        요구('}'); if (위치 != 토큰수) ọdịdà_valuu("extra input after class");
    }
    static int chọta_otù_ebe(int Aha) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(otù_ebe_akara_ahà[수], Aha)) return 수;
        ọdịdà_valuu("unknown variable"); return 0;
    }
    static int gbakwụnye_otù_ebe(int Aha, int pinye_valuu) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(otù_ebe_akara_ahà[수], Aha)) ọdịdà_valuu("duplicate local variable");
        if (지역수 == 128) { ọdịdà_valuu("too many locals"); return 0; }
        otù_ebe_akara_ahà[지역수] = Aha; otù_ebe_pinye[지역수] = pinye_valuu; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean ọnụọgụ_nzùrùòkè_pinye(int pinye_valuu) { return pinye_valuu == 1 || pinye_valuu == 5; }
    static void 지역읽기(int 수) { 내보내기(otù_ebe_pinye[수] <= 2 || otù_ebe_pinye[수] == 5 ? 21 : 25); 내보내기(수); }
    static void dee_otù_ebe(int 수) { 내보내기(otù_ebe_pinye[수] <= 2 || otù_ebe_pinye[수] == 5 ? 54 : 58); 내보내기(수); }
    static void nkwàdo_eziokwū_pinye(int ǹdịnezie_datà, int 기대) { if (ǹdịnezie_datà != 기대 && !(ǹdịnezie_datà == 5 && 기대 == 1)) ọdịdà_valuu("type mismatch"); }
    static void 문자읽기(int akara_valuu_eb540501) {
        mkpụrụedemede_ogologo = 0; int Bido = 토큰위치[akara_valuu_eb540501] + 1, 끝 = 토큰위치[akara_valuu_eb540501] + akara_ogologo[akara_valuu_eb540501] - 1;
        while (Bido < 끝 && !mmejọ) {
            int valuu = ebensìbịa[Bido++];
            if (valuu == '\\') {
                if (Bido == 끝) { ọdịdà_valuu("invalid escape"); break; }
                valuu = ebensìbịa[Bido++];
                if (valuu == 'n') valuu = 10;
                else if (valuu == 'r') valuu = 13;
                else if (valuu == 't') valuu = 9;
                else if (valuu == 'b') valuu = 8;
                else if (valuu == 'f') valuu = 12;
                else if (valuu != '\\' && valuu != '"' && valuu != '\'') ọdịdà_valuu("unsupported escape");
            }
            글추가(valuu);
        }
    }
    static int kerìsịa_ọnụọgụ_nzùrùòkè(int akara_valuu_eb540501, boolean 음수) {
        if (akara_ogologo[akara_valuu_eb540501] > 1 && ebensìbịa[토큰위치[akara_valuu_eb540501]] == '0') ọdịdà_valuu("octal literals unsupported");
        int valuu = 0;
        for (int 수 = 0; 수 < akara_ogologo[akara_valuu_eb540501]; 수++) {
            int ọbula_ihe = ebensìbịa[토큰위치[akara_valuu_eb540501] + 수] - '0';
            if (valuu < -214748364 || valuu == -214748364 && ọbula_ihe > (음수 ? 8 : 7)) ọdịdà_valuu("integer literal out of range");
            valuu = valuu * 10 - ọbula_ihe;
        }
        return 음수 ? valuu : -valuu;
    }
    static int 기본식() {
        if (말받기("new")) {
            int pinye_valuu = hàzie_valuu();
            if (pinye_valuu != 6 && pinye_valuu != 7) { ọdịdà_valuu("only file streams supported by new in source"); return 0; }
            String nwe_valuu = pinye_valuu == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Ntiiwu(187, Nrụtụ_aka(7, Mkpụrụokwu_ihendịgide(nwe_valuu), 0)); 내보내기(89);
            요구('('); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 3); boolean 이어 = false;
            if (받기(',')) { if (pinye_valuu != 7) ọdịdà_valuu("input stream constructor arguments"); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 2); 이어 = true; }
            요구(')');
            Ntiiwu(183, 외부참조(10, nwe_valuu, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return pinye_valuu;
        }
        if (받기('(')) { int pinye_valuu = njìekwu_valuu(); 요구(')'); return pinye_valuu; }
        if (종류() == 257) { 수상수(kerìsịa_ọnụọgụ_nzùrùòkè(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Ntiiwu(19, Nrụtụ_aka(8, mkpụrụedemede_ihendịgide(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (mkpụrụedemede_ogologo != 1) ọdịdà_valuu("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String nwe_valuu = "", usoro_valuu = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                nwe_valuu = "한국어/자체/출력"; 요구('.');
                if (말받기("dee_ahịrī")) { usoro_valuu = "dee_ahịrī"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Chekwaa_ozi")) { usoro_valuu = "Chekwaa_ozi"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { usoro_valuu = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else ọdịdà_valuu("unknown Korean output method");
            } else if (말받기("문자")) {
                nwe_valuu = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("ogologo_valuu")) { usoro_valuu = "ogologo_valuu"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { usoro_valuu = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("kerìsịa_ọnụọgụ_nzùrùòkè")) { usoro_valuu = "kerìsịa_ọnụọgụ_nzùrùòkè"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("dee_ọnụọgụ_nzùrùòkè_valuu")) { usoro_valuu = "dee_ọnụọgụ_nzùrùòkè_valuu"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { usoro_valuu = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("nyàpanye_SMS")) { usoro_valuu = "nyàpanye_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("gbubìte_valuu")) { usoro_valuu = "gbubìte_valuu"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else ọdịdà_valuu("unknown Korean text method");
            } else if (말받기("Faịlụ")) {
                nwe_valuu = "한국어/자체/Faịlụ"; 요구('.'); 가 = 3;
                if (말받기("Wepụta_ọzi")) { usoro_valuu = "Wepụta_ọzi"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Chekwaa_ozi")) { usoro_valuu = "Chekwaa_ozi"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else ọdịdà_valuu("unknown Korean file method");
            } else if (말받기("화면")) {
                nwe_valuu = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { usoro_valuu = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { usoro_valuu = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { usoro_valuu = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { usoro_valuu = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { usoro_valuu = "기다리기"; 서술 = "()V"; }
                else ọdịdà_valuu("unknown Korean framebuffer method");
            } else ọdịdà_valuu("unsupported Korean library class");
            요구('('); if (가 != 0) nkwàdo_eziokwū_pinye(njìekwu_valuu(), 가);
            if (나 != 0) { 요구(','); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 나); }
            if (다 != 0) { 요구(','); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 다); }
            if (라 != 0) { 요구(','); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 라); }
            if (마 != 0) { 요구(','); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 마); }
            요구(')'); Ntiiwu(184, 외부참조(10, nwe_valuu, usoro_valuu, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 3); 요구(')');
            Ntiiwu(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Aha = ihe_nkọwapụta_valuu();
        if (받기('(')) {
            int ọrụ_valuu = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Aha, usoro_ndebà_akara_ahà[수])) ọrụ_valuu = 수;
            if (ọrụ_valuu < 0) { ọdịdà_valuu("unknown static method"); return 0; }
            int 수 = 0;
            while (!mmejọ && 종류() != ')') {
                if (수 >= 함수인수수[ọrụ_valuu]) { ọdịdà_valuu("too many arguments"); break; }
                nkwàdo_eziokwū_pinye(njìekwu_valuu(), usoro_agụment_pinye[ọrụ_valuu * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[ọrụ_valuu]) ọdịdà_valuu("argument count mismatch");
            Ntiiwu(184, Nrụtụ_aka(10, klaàsị_ihendịgide, Nrụtụ_aka(12, usoro_akara_ahà_ihendịgide[ọrụ_valuu], 함수서술[ọrụ_valuu])));
            return 함수반환[ọrụ_valuu];
        }
        int otù_ebe_ọgba = chọta_otù_ebe(Aha), pinye_valuu = otù_ebe_pinye[otù_ebe_ọgba]; 지역읽기(otù_ebe_ọgba);
        while (!mmejọ) {
            if (받기('[')) { nkwàdo_eziokwū_pinye(pinye_valuu, 4); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 1); 요구(']'); 내보내기(50); pinye_valuu = 3; }
            else if (받기('.')) {
                if (pinye_valuu == 6 || pinye_valuu == 7) {
                    String nwe_valuu = pinye_valuu == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Ntiiwu(182, 외부참조(10, nwe_valuu, "close", "()V")); pinye_valuu = 0; }
                    else if (pinye_valuu == 6 && 말받기("read")) { 요구('('); 요구(')'); Ntiiwu(182, 외부참조(10, nwe_valuu, "read", "()I")); pinye_valuu = 1; }
                    else if (pinye_valuu == 7 && 말받기("write")) { 요구('('); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 1); 요구(')'); Ntiiwu(182, 외부참조(10, nwe_valuu, "write", "(I)V")); pinye_valuu = 0; }
                    else { ọdịdà_valuu("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (pinye_valuu == 4) { 내보내기(190); pinye_valuu = 1; }
                else { nkwàdo_eziokwū_pinye(pinye_valuu, 3); 요구('('); 요구(')'); Ntiiwu(182, 외부참조(10, "java/lang/String", "length", "()I")); pinye_valuu = 1; }
            } else break;
        }
        return pinye_valuu;
    }
    static int 단항() {
        if (++식깊이 > 64) { ọdịdà_valuu("expression nesting too deep"); 식깊이--; return 0; }
        int pinye_valuu;
        if (받기('!')) { nkwàdo_eziokwū_pinye(단항(), 2); 비교값(153); pinye_valuu = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(kerìsịa_ọnụọgụ_nzùrùòkè(위치++, true));
            else { nkwàdo_eziokwū_pinye(단항(), 1); 내보내기(116); }
            pinye_valuu = 1;
        } else if (받기('+')) { nkwàdo_eziokwū_pinye(단항(), 1); pinye_valuu = 1; }
        else pinye_valuu = 기본식();
        식깊이--; return pinye_valuu;
    }
    static int 곱식() {
        int pinye_valuu = 단항();
        while (!mmejọ && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int ntinye_koòdù_valuu = 종류(); 위치++; nkwàdo_eziokwū_pinye(pinye_valuu, 1); nkwàdo_eziokwū_pinye(단항(), 1);
            내보내기(ntinye_koòdù_valuu == '*' ? 104 : ntinye_koòdù_valuu == '/' ? 108 : 112); pinye_valuu = 1;
        }
        return pinye_valuu;
    }
    static int 합식() {
        int pinye_valuu = 곱식();
        while (!mmejọ && (종류() == '+' || 종류() == '-')) {
            int ntinye_koòdù_valuu = 종류(); 위치++; int 경계 = 코드크기, Àzụ_valuu_pinye = 곱식();
            if (ntinye_koòdù_valuu == '+' && (pinye_valuu == 3 || Àzụ_valuu_pinye == 3)) { 결합(경계, pinye_valuu, Àzụ_valuu_pinye); pinye_valuu = 3; }
            else { nkwàdo_eziokwū_pinye(pinye_valuu, 1); nkwàdo_eziokwū_pinye(Àzụ_valuu_pinye, 1); 내보내기(ntinye_koòdù_valuu == '+' ? 96 : 100); pinye_valuu = 1; }
        }
        return pinye_valuu;
    }
    static int 붙임참조(int pinye_valuu) {
        if (pinye_valuu != 1 && pinye_valuu != 2 && pinye_valuu != 3 && pinye_valuu != 5) ọdịdà_valuu("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", pinye_valuu == 1 ? "(I)Ljava/lang/StringBuilder;"
            : pinye_valuu == 2 ? "(Z)Ljava/lang/StringBuilder;" : pinye_valuu == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Àzụ_valuu_pinye) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 njìekwu_valuu 내부의 ibè_valuu ogbè 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Ntiiwu(187, Nrụtụ_aka(7, Mkpụrụokwu_ihendịgide("java/lang/StringBuilder"), 0)); 내보내기(89);
        Ntiiwu(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Ntiiwu(182, 붙임참조(앞형));
        if (mmejọ) return;
        int ogologo_valuu = 코드크기 - 끝;
        for (int 수 = 0; 수 < ogologo_valuu; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + ogologo_valuu] = 코드[수];
        for (int 수 = 0; 수 < ogologo_valuu; 수++) 코드[경계 + 수] = 삽입코드[수];
        Ntiiwu(182, 붙임참조(Àzụ_valuu_pinye)); Ntiiwu(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int pinye_valuu = 합식();
        while (!mmejọ && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int ntinye_koòdù_valuu = 종류(); 위치++; nkwàdo_eziokwū_pinye(pinye_valuu, 1); nkwàdo_eziokwū_pinye(합식(), 1);
            비교값(ntinye_koòdù_valuu == '<' ? 161 : ntinye_koòdù_valuu == '>' ? 163 : ntinye_koòdù_valuu == 302 ? 164 : 162); pinye_valuu = 2;
        }
        return pinye_valuu;
    }
    static int 동등식() {
        int pinye_valuu = 비교식();
        while (!mmejọ && (종류() == 300 || 종류() == 301)) {
            int ntinye_koòdù_valuu = 종류(); 위치++; int Àzụ_valuu_pinye = 비교식();
            if (pinye_valuu == 0 || Àzụ_valuu_pinye == 0) ọdịdà_valuu("void expression");
            if (!(ọnụọgụ_nzùrùòkè_pinye(pinye_valuu) && ọnụọgụ_nzùrùòkè_pinye(Àzụ_valuu_pinye))) nkwàdo_eziokwū_pinye(Àzụ_valuu_pinye, pinye_valuu);
            비교값((pinye_valuu <= 2 || pinye_valuu == 5 ? 159 : 165) + (ntinye_koòdù_valuu == 301 ? 1 : 0)); pinye_valuu = 2;
        }
        return pinye_valuu;
    }
    static int 논리곱() {
        int pinye_valuu = 동등식();
        while (!mmejọ && 받기(304)) {
            nkwàdo_eziokwū_pinye(pinye_valuu, 2); int 가 = ogbè(153); nkwàdo_eziokwū_pinye(동등식(), 2); int 나 = ogbè(153);
            내보내기(4); int 끝 = ogbè(167); Njikọ_valuu(가, 코드크기); Njikọ_valuu(나, 코드크기); 내보내기(3); Njikọ_valuu(끝, 코드크기); pinye_valuu = 2;
        }
        return pinye_valuu;
    }
    static int njìekwu_valuu() {
        int pinye_valuu = 논리곱();
        while (!mmejọ && 받기(305)) {
            nkwàdo_eziokwū_pinye(pinye_valuu, 2); int 가 = ogbè(154); nkwàdo_eziokwū_pinye(논리곱(), 2); int 나 = ogbè(154);
            내보내기(3); int 끝 = ogbè(167); Njikọ_valuu(가, 코드크기); Njikọ_valuu(나, 코드크기); 내보내기(4); Njikọ_valuu(끝, 코드크기); pinye_valuu = 2;
        }
        return pinye_valuu;
    }
    static void Ihe_nnwale_valuu(boolean 선언허용) {
        if (Mkpụrụokwu_valuu(위치, "int") || Mkpụrụokwu_valuu(위치, "boolean") || Mkpụrụokwu_valuu(위치, "String") || Mkpụrụokwu_valuu(위치, "char")
            || Mkpụrụokwu_valuu(위치, "FileInputStream") || Mkpụrụokwu_valuu(위치, "FileOutputStream")) {
            if (!선언허용) ọdịdà_valuu("declaration not allowed here");
            int pinye_valuu = hàzie_valuu(), Aha = ihe_nkọwapụta_valuu(); 요구('='); nkwàdo_eziokwū_pinye(njìekwu_valuu(), pinye_valuu);
            dee_otù_ebe(gbakwụnye_otù_ebe(Aha, pinye_valuu)); return;
        }
        int Aha = ihe_nkọwapụta_valuu(), otù_ebe_ọgba = chọta_otù_ebe(Aha);
        if (받기('=')) { nkwàdo_eziokwū_pinye(njìekwu_valuu(), otù_ebe_pinye[otù_ebe_ọgba]); dee_otù_ebe(otù_ebe_ọgba); }
        else if (종류() >= 308 && 종류() <= 312) {
            int ntinye_koòdù_valuu = 종류(); 위치++; 지역읽기(otù_ebe_ọgba); int 경계 = 코드크기, Àzụ_valuu_pinye = njìekwu_valuu();
            if (ntinye_koòdù_valuu == 308 && otù_ebe_pinye[otù_ebe_ọgba] == 3) 결합(경계, 3, Àzụ_valuu_pinye);
            else {
                nkwàdo_eziokwū_pinye(otù_ebe_pinye[otù_ebe_ọgba], 1); nkwàdo_eziokwū_pinye(Àzụ_valuu_pinye, 1);
                내보내기(ntinye_koòdù_valuu == 308 ? 96 : ntinye_koòdù_valuu == 309 ? 100 : ntinye_koòdù_valuu == 310 ? 104 : ntinye_koòdù_valuu == 311 ? 108 : 112);
                if (otù_ebe_pinye[otù_ebe_ọgba] == 5) 내보내기(146);
            }
            dee_otù_ebe(otù_ebe_ọgba);
        }
        else if (종류() == 306 || 종류() == 307) {
            nkwàdo_eziokwū_pinye(otù_ebe_pinye[otù_ebe_ọgba], 1); 내보내기(132); 내보내기(otù_ebe_ọgba); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (otù_ebe_pinye[otù_ebe_ọgba] == 5) { 지역읽기(otù_ebe_ọgba); 내보내기(146); dee_otù_ebe(otù_ebe_ọgba); }
        } else ọdịdà_valuu("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Ntiiwu(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean oghere_agụment = 종류() == ')';
        int pinye_valuu = oghere_agụment ? 0 : njìekwu_valuu(); 요구(')'); 요구(';');
        String 서술 = pinye_valuu == 0 ? "()V" : pinye_valuu == 1 ? "(I)V" : pinye_valuu == 2 ? "(Z)V" : pinye_valuu == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (pinye_valuu == 4 || pinye_valuu >= 6 || pinye_valuu == 0 && (!줄바꿈 || !oghere_agụment)) ọdịdà_valuu("unsupported print argument");
        Ntiiwu(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean nkwupute_valuu() {
        if (mmejọ) return false;
        if (깊이 > 32) { ọdịdà_valuu("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!mmejọ && 종류() != '}') { if (반환) ọdịdà_valuu("unreachable statement"); 반환 = nkwupute_valuu(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int pinye_valuu = 종류() == ';' ? 0 : njìekwu_valuu(); nkwàdo_eziokwū_pinye(pinye_valuu, 함수반환[현재함수]); 요구(';');
            내보내기(pinye_valuu == 0 ? 177 : pinye_valuu <= 2 || pinye_valuu == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 2); 요구(')'); int 거짓 = ogbè(153);
            깊이++; boolean 가 = njizi_nkwupute(); 깊이--;
            if (말받기("else")) { int 끝 = ogbè(167); Njikọ_valuu(거짓, 코드크기); 깊이++; boolean 나 = njizi_nkwupute(); 깊이--; Njikọ_valuu(끝, 코드크기); return 가 && 나; }
            Njikọ_valuu(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Bido = 코드크기; 요구('('); nkwàdo_eziokwū_pinye(njìekwu_valuu(), 2); 요구(')'); int 끝 = ogbè(153);
            깊이++; njizi_nkwupute(); 깊이--; Njikọ_valuu(ogbè(167), Bido); Njikọ_valuu(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') Ihe_nnwale_valuu(true); 요구(';');
            int ọnọdụ = 코드크기; if (종류() == ';') 내보내기(4); else nkwàdo_eziokwū_pinye(njìekwu_valuu(), 2); 요구(';');
            int 끝 = ogbè(153), àhụngwè = ogbè(167), mèkwa_ọhụrụ = 코드크기;
            if (종류() != ')') Ihe_nnwale_valuu(false); 요구(')'); Njikọ_valuu(ogbè(167), ọnọdụ); Njikọ_valuu(àhụngwè, 코드크기);
            njizi_nkwupute(); Njikọ_valuu(ogbè(167), mèkwa_ọhụrụ); Njikọ_valuu(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Mkpụrụokwu_valuu(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int pinye_valuu = njìekwu_valuu(); if (pinye_valuu != 0) 내보내기(87); 요구(';'); return false;
        }
        Ihe_nnwale_valuu(true); 요구(';'); return false;
    }
    static boolean njizi_nkwupute() {
        if (Mkpụrụokwu_valuu(위치, "int") || Mkpụrụokwu_valuu(위치, "boolean") || Mkpụrụokwu_valuu(위치, "char") || Mkpụrụokwu_valuu(위치, "String")
            || Mkpụrụokwu_valuu(위치, "FileInputStream") || Mkpụrụokwu_valuu(위치, "FileOutputStream")) ọdịdà_valuu("local declaration requires braces");
        return nkwupute_valuu();
    }
    static void 출바(int valuu) { if (출력크기 == 출력.length) ọdịdà_valuu("class file too large"); else 출력[출력크기++] = valuu & 255; }
    static void 출짧(int valuu) { 출바(valuu >> 8); 출바(valuu); }
    static void 출정(int valuu) { 출짧(valuu >>> 16); 출짧(valuu); }
    static void dee_klaàsị() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < ihendịgide_ụha; 수++) 출바(ihendịgide_valuu[수]);
        출짧(0x21); 출짧(klaàsị_ihendịgide); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(usoro_òhèrè[수]); 출짧(usoro_akara_ahà_ihendịgide[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + usoro_ogologo[수]); 출짧(128); 출짧(함수지역[수]); 출정(usoro_ogologo[수]);
            for (int oghere_ndebà = 0; oghere_ndebà < usoro_ogologo[수]; oghere_ndebà++) 출바(코드[함수코드[수] + oghere_ndebà]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Bido() {
        if (òjìàrụ.인수개수() == 1 && 자바도구.같음(òjìàrụ.인수(0), "-version")) {
            òjìàrụ.Chekwaa_ozi("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (òjìàrụ.인수개수() != 1) { òjìàrụ.Chekwaa_ozi("Usage: javac FILE.java\n"); return 2; }
        int akara_ahà_ụha = 자바도구.Aha(ọbọakwụkwọ_akara_ahà_SMS, òjìàrụ.인수(0));
        if (akara_ahà_ụha < 6 || akara_ahà_ụha > 62 || ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 5] != '.' || ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 4] != 'j'
            || ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 3] != 'a' || ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 2] != 'v' || ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 1] != 'a') {
            òjìàrụ.Chekwaa_ozi("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        ebensìbịa_ụha = òjìàrụ.파일읽기(ọbọakwụkwọ_akara_ahà_SMS, ebensìbịa);
        if (ebensìbịa_ụha < 0) { òjìàrụ.Chekwaa_ozi("javac: cannot read source: "); 자바도구.수쓰기(ebensìbịa_ụha); òjìàrụ.dee_mkpụrụedemede_valuu(10); return 1; }
        ebensìbịa_ụha = 자바도구.원문해독(ebensìbịa, ebensìbịa_ụha);
        if (ebensìbịa_ụha < 0) { òjìàrụ.Chekwaa_ozi("javac error: invalid UTF-8 source\n"); return 1; }
        gbubìte_valuu(); if (!mmejọ) 선언읽기();
        if (!mmejọ) {
            if (akara_ogologo[klaàsị_akara] != akara_ahà_ụha - 5) ọdịdà_valuu("class name must match file name");
            for (int 수 = 0; 수 < akara_ahà_ụha - 5; 수++) if (ebensìbịa[토큰위치[klaàsị_akara] + 수] != ọbọakwụkwọ_akara_ahà_SMS[수]) ọdịdà_valuu("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !mmejọ; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) gbakwụnye_otù_ebe(usoro_agụment_akara_ahà[현재함수 * 16 + 수], usoro_agụment_pinye[현재함수 * 16 + 수]);
            boolean 반환 = nkwupute_valuu();
            if (!반환 && 함수반환[현재함수] != 0) ọdịdà_valuu("missing return");
            // ogbè 뒤의 합류 지점은 반드시 ǹdịnezie_datà 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean ọnụọgụ_nzùrùòkè = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(ọnụọgụ_nzùrùòkè ? 3 : 1); 내보내기(ọnụọgụ_nzùrùòkè ? 172 : 176); }
            if (위치 != usoro_mèdebe[현재함수]) ọdịdà_valuu("invalid method body");
            함수지역[현재함수] = 지역수; usoro_ogologo[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (mmejọ) return 1;
        dee_klaàsị(); if (mmejọ) return 1;
        ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 4] = 'c'; ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 3] = 'l'; ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 2] = 'a';
        ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha - 1] = 's'; ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha] = 's'; ọbọakwụkwọ_akara_ahà_SMS[akara_ahà_ụha + 1] = 0;
        int 결과 = òjìàrụ.dee_ọbọakwụkwọ(ọbọakwụkwọ_akara_ahà_SMS, 출력, 출력크기);
        if (결과 < 0) { òjìàrụ.Chekwaa_ozi("javac: cannot save class: "); 자바도구.수쓰기(결과); òjìàrụ.dee_mkpụrụedemede_valuu(10); return 1; }
        òjìàrụ.Chekwaa_ozi("Compiled: "); for (int 수 = 0; ọbọakwụkwọ_akara_ahà_SMS[수] != 0; 수++) òjìàrụ.dee_mkpụrụedemede_valuu(ọbọakwụkwọ_akara_ahà_SMS[수]);
        òjìàrụ.Chekwaa_ozi(" (JVM class version 49)\n"); return 0;
    }
}
