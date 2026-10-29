// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java umthombo_isihlahla -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] umthombo = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], ithokhini_ubude = new int[2048];
    static int[] okungaguquki_inani = new int[4096], okungaguquki_I_ofisethi = new int[512];
    static int[] 문자 = new int[512], ifayela_igama_I_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int umthombo_linganisa, 토큰수, 위치, 코드크기, okungaguquki_linganisa, 상수수 = 1, 출력크기, uhlamvusimo_ubude;
    static boolean Iphutha;
    static int uhlobo_ithokhini, uhlobo_okungaguquki, 부모상수, 코드상수;
    static int[] indlela_okufakwayo_igama = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] indlela_i_agumenti_igama = new int[512], indlela_i_agumenti_thayipha = new int[512];
    static int[] 함수본문 = new int[32], indlela_yekisa = new int[32], 함수코드 = new int[32];
    static int[] indlela_ubude = new int[32], 함수지역 = new int[32], indlela_igama_okungaguquki = new int[32], 함수서술 = new int[32];
    static int[] indlela_ungeno = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] endaweni_igama = new int[128], endaweni_thayipha = new int[128], 지역깊이 = new int[128];

    static void ukwehluleka_inani(String 이유) {
        if (!Iphutha) {
            umsebenzisi.Bhala("javac error: "); umsebenzisi.Bhala(이유);
            umsebenzisi.Bhala(" at line ");
            int umugqa = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : umthombo_linganisa;
            for (int 수 = 0; 수 < 끝; 수++) if (umthombo[수] == 10) umugqa++;
            자바도구.수쓰기(umugqa); umsebenzisi.bhala_uhlamvusimo_inani(10);
        }
        Iphutha = true;
    }
    static boolean uhlamvusimo_inani(int inani) { return 문자이름규칙.첫글자(inani); }
    static boolean idijithi_inani(int inani) { return inani >= '0' && inani <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || ithokhini_ubude[가] != ithokhini_ubude[나]) return false;
        for (int 수 = 0; 수 < ithokhini_ubude[가]; 수++) if (umthombo[토큰위치[가] + 수] != umthombo[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Amagama_inani(int ithokhini_inani, String Amagama_I_SMS) {
        if (ithokhini_inani < 0 || ithokhini_inani >= 토큰수 || ithokhini_ubude[ithokhini_inani] != Amagama_I_SMS.length()) return false;
        for (int 수 = 0; 수 < Amagama_I_SMS.length(); 수++) if (umthombo[토큰위치[ithokhini_inani] + 수] != Amagama_I_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int inani) { if (종류() != inani) return false; 위치++; return true; }
    static void 요구(int inani) { if (!받기(inani)) ukwehluleka_inani("unexpected token"); }
    static boolean 말받기(String Amagama_I_SMS) { if (!Amagama_inani(위치, Amagama_I_SMS)) return false; 위치++; return true; }
    static void 말요구(String Amagama_I_SMS) { if (!말받기(Amagama_I_SMS)) ukwehluleka_inani(Amagama_I_SMS); }
    static int isivezi_inani() {
        int 결과 = 위치;
        if (종류() != 256) ukwehluleka_inani("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Sebenzisa = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Sebenzisa == ithokhini_ubude[결과];
                for (int isikhala_okufakwayo = Sebenzisa; 같음 && isikhala_okufakwayo < 수; isikhala_okufakwayo++) if (예약어.charAt(isikhala_okufakwayo) != umthombo[토큰위치[결과] + isikhala_okufakwayo - Sebenzisa]) 같음 = false;
                if (같음) ukwehluleka_inani("reserved word cannot be an identifier");
                Sebenzisa = 수 + 1;
            }
        }
        return 결과;
    }
    static void sika_inani() {
        int 수 = 0;
        while (수 < umthombo_linganisa && !Iphutha) {
            int inani = umthombo[수], Sebenzisa = 수, 종류 = inani;
            if (inani == 32 || inani == 9 || inani == 10 || inani == 13) { 수++; continue; }
            if (inani == '/' && 수 + 1 < umthombo_linganisa && umthombo[수 + 1] == '/') {
                while (수 < umthombo_linganisa && umthombo[수] != 10) 수++;
                continue;
            }
            if (inani == '/' && 수 + 1 < umthombo_linganisa && umthombo[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < umthombo_linganisa && !(umthombo[수] == '*' && umthombo[수 + 1] == '/')) 수++;
                if (수 + 1 >= umthombo_linganisa) { ukwehluleka_inani("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (uhlamvusimo_inani(inani)) { 종류 = 256; while (수 < umthombo_linganisa && 문자이름규칙.이어진글자(umthombo[수])) 수++; }
            else if (idijithi_inani(inani)) { 종류 = 257; while (수 < umthombo_linganisa && idijithi_inani(umthombo[수])) 수++; }
            else if (inani == '"' || inani == '\'') {
                종류 = inani == '"' ? 258 : 259; 수++;
                while (수 < umthombo_linganisa && umthombo[수] != inani && umthombo[수] != 10 && umthombo[수] != 13) {
                    if (umthombo[수] == '\\') 수++;
                    수++;
                }
                if (수 >= umthombo_linganisa || umthombo[수] != inani) { ukwehluleka_inani("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < umthombo_linganisa) {
                    int 다음 = umthombo[수];
                    if (inani == '=' && 다음 == '=') 종류 = 300;
                    if (inani == '!' && 다음 == '=') 종류 = 301;
                    if (inani == '<' && 다음 == '=') 종류 = 302;
                    if (inani == '>' && 다음 == '=') 종류 = 303;
                    if (inani == '&' && 다음 == '&') 종류 = 304;
                    if (inani == '|' && 다음 == '|') 종류 = 305;
                    if (inani == '+' && 다음 == '+') 종류 = 306;
                    if (inani == '-' && 다음 == '-') 종류 = 307;
                    if (inani == '+' && 다음 == '=') 종류 = 308;
                    if (inani == '-' && 다음 == '=') 종류 = 309;
                    if (inani == '*' && 다음 == '=') 종류 = 310;
                    if (inani == '/' && 다음 == '=') 종류 = 311;
                    if (inani == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { ukwehluleka_inani("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Sebenzisa; ithokhini_ubude[토큰수++] = 수 - Sebenzisa;
        }
    }
    static void bhala_okungaguquki_ibhayithi(int inani) {
        if (okungaguquki_linganisa == okungaguquki_inani.length) { ukwehluleka_inani("constant pool too large"); return; }
        okungaguquki_inani[okungaguquki_linganisa++] = inani & 255;
    }
    static void 상짧(int inani) { bhala_okungaguquki_ibhayithi(inani >> 8); bhala_okungaguquki_ibhayithi(inani); }
    static int bhalisa_okungaguquki(int Sebenzisa) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = okungaguquki_I_ofisethi[수], ubude_inani = (수 + 1 < 상수수 ? okungaguquki_I_ofisethi[수 + 1] : Sebenzisa) - 앞;
            if (ubude_inani != okungaguquki_linganisa - Sebenzisa) continue;
            boolean 같음 = true;
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < ubude_inani; isikhala_okufakwayo++) if (okungaguquki_inani[앞 + isikhala_okufakwayo] != okungaguquki_inani[Sebenzisa + isikhala_okufakwayo]) 같음 = false;
            if (같음) { okungaguquki_linganisa = Sebenzisa; return 수; }
        }
        if (상수수 == okungaguquki_I_ofisethi.length) { ukwehluleka_inani("too many constants"); return 0; }
        okungaguquki_I_ofisethi[상수수] = Sebenzisa;
        return 상수수++;
    }
    static void 글추가(int inani) {
        if (uhlamvusimo_ubude == 문자.length) { ukwehluleka_inani("text too long"); return; }
        문자[uhlamvusimo_ubude++] = inani;
    }
    static void 말추가(String Amagama_I_SMS) { for (int 수 = 0; 수 < Amagama_I_SMS.length(); 수++) 글추가(Amagama_I_SMS.charAt(수)); }
    static int uhlamvusimo_okungaguquki() {
        int Sebenzisa = okungaguquki_linganisa; bhala_okungaguquki_ibhayithi(1); 상짧(0);
        for (int 수 = 0; 수 < uhlamvusimo_ubude; 수++) {
            int inani = 문자[수];
            if (inani > 0 && inani < 128) bhala_okungaguquki_ibhayithi(inani);
            else if (inani < 2048) { bhala_okungaguquki_ibhayithi(192 | inani >> 6); bhala_okungaguquki_ibhayithi(128 | inani & 63); }
            else { bhala_okungaguquki_ibhayithi(224 | inani >> 12); bhala_okungaguquki_ibhayithi(128 | inani >> 6 & 63); bhala_okungaguquki_ibhayithi(128 | inani & 63); }
        }
        if (Iphutha) return 0;
        int ubude_inani = okungaguquki_linganisa - Sebenzisa - 3;
        okungaguquki_inani[Sebenzisa + 1] = ubude_inani >> 8; okungaguquki_inani[Sebenzisa + 2] = ubude_inani & 255;
        return bhalisa_okungaguquki(Sebenzisa);
    }
    static int Amagama_okungaguquki(String Amagama_I_SMS) { uhlamvusimo_ubude = 0; 말추가(Amagama_I_SMS); return uhlamvusimo_okungaguquki(); }
    static int ithokhini_okungaguquki(int ithokhini_inani) {
        uhlamvusimo_ubude = 0;
        for (int 수 = 0; 수 < ithokhini_ubude[ithokhini_inani]; 수++) 글추가(umthombo[토큰위치[ithokhini_inani] + 수]);
        return uhlamvusimo_okungaguquki();
    }
    static int Ireferensi(int 종류, int 가, int 나) {
        int Sebenzisa = okungaguquki_linganisa; bhala_okungaguquki_ibhayithi(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return bhalisa_okungaguquki(Sebenzisa);
    }
    static int 외부참조(int 종류, String umnikazi_inani, String Igama, String 서술) {
        int umnikazi_isivezi = Ireferensi(7, Amagama_okungaguquki(umnikazi_inani), 0);
        int 이름수 = Amagama_okungaguquki(Igama), 형식수 = Amagama_okungaguquki(서술);
        return Ireferensi(종류, umnikazi_isivezi, Ireferensi(12, 이름수, 형식수));
    }
    static void 내보내기(int inani) {
        if (코드크기 == 코드.length) { ukwehluleka_inani("bytecode too large"); return; }
        코드[코드크기++] = inani & 255;
    }
    static void Umlayelo(int inani, int 인수) { 내보내기(inani); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int inani) {
        if (inani >= -1 && inani <= 5) { 내보내기(inani + 3); return; }
        int Sebenzisa = okungaguquki_linganisa; bhala_okungaguquki_ibhayithi(3); 상짧(inani >>> 16); 상짧(inani);
        Umlayelo(19, bhalisa_okungaguquki(Sebenzisa));
    }
    static int igatsha(int Umlayelo) { int 결과 = 코드크기; Umlayelo(Umlayelo, 0); return 결과; }
    static void xhuma_inani(int igatsha, int impokophelo_into) {
        if (Iphutha) return;
        int 거리 = impokophelo_into - igatsha;
        if (거리 < -32768 || 거리 > 32767 || igatsha < 0 || igatsha + 2 >= 코드크기) { ukwehluleka_inani("invalid branch"); return; }
        코드[igatsha + 1] = 거리 >> 8 & 255; 코드[igatsha + 2] = 거리 & 255;
    }
    static void 비교값(int Umlayelo) {
        int 참 = igatsha(Umlayelo); 내보내기(3); int 끝 = igatsha(167);
        xhuma_inani(참, 코드크기); 내보내기(4); xhuma_inani(끝, 코드크기);
    }
    static int misa_inani() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        ukwehluleka_inani("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void hlanganisa_misa(int thayipha_inani) {
        if (thayipha_inani == 0) 글추가('V');
        if (thayipha_inani == 1) 글추가('I');
        if (thayipha_inani == 2) 글추가('Z');
        if (thayipha_inani == 3) 말추가("Ljava/lang/String;");
        if (thayipha_inani == 4) 말추가("[Ljava/lang/String;");
        if (thayipha_inani == 5) 글추가('C');
        if (thayipha_inani == 6) 말추가("Ljava/io/FileInputStream;");
        if (thayipha_inani == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Inqubo_inani_okufakwayo 본문은 singatha javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("Isi_Zulu");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("AMALUNGU_AFANAYO_Store_ukwehluleka") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        ukwehluleka_inani("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Amagama_inani(위치, "Isi_Zulu")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) ukwehluleka_inani("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); uhlobo_ithokhini = isivezi_inani();
        uhlobo_okungaguquki = Ireferensi(7, ithokhini_okungaguquki(uhlobo_ithokhini), 0);
        부모상수 = Ireferensi(7, Amagama_okungaguquki("java/lang/Object"), 0); 코드상수 = Amagama_okungaguquki("Code"); 요구('{');
        while (!Iphutha && 종류() != '}') {
            if (함수수 == 32) { ukwehluleka_inani("too many methods"); break; }
            int ungeno_okufakwayo = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int umsebenzi_inani = 함수수++;
            indlela_ungeno[umsebenzi_inani] = ungeno_okufakwayo | 8;
            함수반환[umsebenzi_inani] = misa_inani(); indlela_okufakwayo_igama[umsebenzi_inani] = isivezi_inani(); 요구('(');
            for (int 앞 = 0; 앞 < umsebenzi_inani; 앞++) if (이름같음(indlela_okufakwayo_igama[앞], indlela_okufakwayo_igama[umsebenzi_inani])) ukwehluleka_inani("duplicate method (overloading unsupported)");
            while (!Iphutha && 종류() != ')') {
                int 수 = 함수인수수[umsebenzi_inani];
                if (수 == 16) { ukwehluleka_inani("too many parameters"); break; }
                int thayipha_inani = misa_inani(); if (thayipha_inani == 0) ukwehluleka_inani("void parameter");
                indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수] = thayipha_inani; indlela_i_agumenti_igama[umsebenzi_inani * 16 + 수] = isivezi_inani();
                함수인수수[umsebenzi_inani]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!Iphutha && 받기(','));
            }
            함수본문[umsebenzi_inani] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) ukwehluleka_inani("unclosed method body");
            indlela_yekisa[umsebenzi_inani] = 위치;
            indlela_igama_okungaguquki[umsebenzi_inani] = ithokhini_okungaguquki(indlela_okufakwayo_igama[umsebenzi_inani]);
            uhlamvusimo_ubude = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[umsebenzi_inani]; 수++) hlanganisa_misa(indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수]);
            글추가(')'); hlanganisa_misa(함수반환[umsebenzi_inani]); 함수서술[umsebenzi_inani] = uhlamvusimo_okungaguquki();
        }
        요구('}'); if (위치 != 토큰수) ukwehluleka_inani("extra input after class");
    }
    static int thola_endaweni(int Igama) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(endaweni_igama[수], Igama)) return 수;
        ukwehluleka_inani("unknown variable"); return 0;
    }
    static int hlanganisa_endaweni(int Igama, int thayipha_inani) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(endaweni_igama[수], Igama)) ukwehluleka_inani("duplicate local variable");
        if (지역수 == 128) { ukwehluleka_inani("too many locals"); return 0; }
        endaweni_igama[지역수] = Igama; endaweni_thayipha[지역수] = thayipha_inani; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean inamba_thayipha(int thayipha_inani) { return thayipha_inani == 1 || thayipha_inani == 5; }
    static void 지역읽기(int 수) { 내보내기(endaweni_thayipha[수] <= 2 || endaweni_thayipha[수] == 5 ? 21 : 25); 내보내기(수); }
    static void bhala_endaweni(int 수) { 내보내기(endaweni_thayipha[수] <= 2 || endaweni_thayipha[수] == 5 ? 54 : 58); 내보내기(수); }
    static void qiniseka_thayipha(int ulwazi_ngokwenzekile_imininingwane, int 기대) { if (ulwazi_ngokwenzekile_imininingwane != 기대 && !(ulwazi_ngokwenzekile_imininingwane == 5 && 기대 == 1)) ukwehluleka_inani("type mismatch"); }
    static void 문자읽기(int ithokhini_inani) {
        uhlamvusimo_ubude = 0; int Sebenzisa = 토큰위치[ithokhini_inani] + 1, 끝 = 토큰위치[ithokhini_inani] + ithokhini_ubude[ithokhini_inani] - 1;
        while (Sebenzisa < 끝 && !Iphutha) {
            int inani = umthombo[Sebenzisa++];
            if (inani == '\\') {
                if (Sebenzisa == 끝) { ukwehluleka_inani("invalid escape"); break; }
                inani = umthombo[Sebenzisa++];
                if (inani == 'n') inani = 10;
                else if (inani == 'r') inani = 13;
                else if (inani == 't') inani = 9;
                else if (inani == 'b') inani = 8;
                else if (inani == 'f') inani = 12;
                else if (inani != '\\' && inani != '"' && inani != '\'') ukwehluleka_inani("unsupported escape");
            }
            글추가(inani);
        }
    }
    static int zawula_inamba(int ithokhini_inani, boolean 음수) {
        if (ithokhini_ubude[ithokhini_inani] > 1 && umthombo[토큰위치[ithokhini_inani]] == '0') ukwehluleka_inani("octal literals unsupported");
        int inani = 0;
        for (int 수 = 0; 수 < ithokhini_ubude[ithokhini_inani]; 수++) {
            int idijithi_utho = umthombo[토큰위치[ithokhini_inani] + 수] - '0';
            if (inani < -214748364 || inani == -214748364 && idijithi_utho > (음수 ? 8 : 7)) ukwehluleka_inani("integer literal out of range");
            inani = inani * 10 - idijithi_utho;
        }
        return 음수 ? inani : -inani;
    }
    static int 기본식() {
        if (말받기("new")) {
            int thayipha_inani = misa_inani();
            if (thayipha_inani != 6 && thayipha_inani != 7) { ukwehluleka_inani("only file streams supported by new in source"); return 0; }
            String umnikazi_inani = thayipha_inani == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Umlayelo(187, Ireferensi(7, Amagama_okungaguquki(umnikazi_inani), 0)); 내보내기(89);
            요구('('); qiniseka_thayipha(ukusho_inani(), 3); boolean 이어 = false;
            if (받기(',')) { if (thayipha_inani != 7) ukwehluleka_inani("input stream constructor arguments"); qiniseka_thayipha(ukusho_inani(), 2); 이어 = true; }
            요구(')');
            Umlayelo(183, 외부참조(10, umnikazi_inani, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return thayipha_inani;
        }
        if (받기('(')) { int thayipha_inani = ukusho_inani(); 요구(')'); return thayipha_inani; }
        if (종류() == 257) { 수상수(zawula_inamba(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Umlayelo(19, Ireferensi(8, uhlamvusimo_okungaguquki(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (uhlamvusimo_ubude != 1) ukwehluleka_inani("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("Isi_Zulu")) {
            요구('.'); 말요구("자체"); 요구('.');
            String umnikazi_inani = "", indlela_inani = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                umnikazi_inani = "Isi_Zulu/자체/출력"; 요구('.');
                if (말받기("bhala_umugqa")) { indlela_inani = "bhala_umugqa"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Bhala")) { indlela_inani = "Bhala"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { indlela_inani = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else ukwehluleka_inani("unknown Korean output method");
            } else if (말받기("문자")) {
                umnikazi_inani = "Isi_Zulu/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("ubude_inani")) { indlela_inani = "ubude_inani"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { indlela_inani = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("zawula_inamba")) { indlela_inani = "zawula_inamba"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("bhala_inamba_inani")) { indlela_inani = "bhala_inamba_inani"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { indlela_inani = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("namathisela_I_SMS")) { indlela_inani = "namathisela_I_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("sika_inani")) { indlela_inani = "sika_inani"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else ukwehluleka_inani("unknown Korean text method");
            } else if (말받기("Ihele")) {
                umnikazi_inani = "Isi_Zulu/자체/Ihele"; 요구('.'); 가 = 3;
                if (말받기("Funda")) { indlela_inani = "Funda"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Bhala")) { indlela_inani = "Bhala"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else ukwehluleka_inani("unknown Korean file method");
            } else if (말받기("화면")) {
                umnikazi_inani = "Isi_Zulu/자체/화면"; 요구('.');
                if (말받기("너비")) { indlela_inani = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { indlela_inani = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { indlela_inani = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { indlela_inani = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { indlela_inani = "기다리기"; 서술 = "()V"; }
                else ukwehluleka_inani("unknown Korean framebuffer method");
            } else ukwehluleka_inani("unsupported Korean library class");
            요구('('); if (가 != 0) qiniseka_thayipha(ukusho_inani(), 가);
            if (나 != 0) { 요구(','); qiniseka_thayipha(ukusho_inani(), 나); }
            if (다 != 0) { 요구(','); qiniseka_thayipha(ukusho_inani(), 다); }
            if (라 != 0) { 요구(','); qiniseka_thayipha(ukusho_inani(), 라); }
            if (마 != 0) { 요구(','); qiniseka_thayipha(ukusho_inani(), 마); }
            요구(')'); Umlayelo(184, 외부참조(10, umnikazi_inani, indlela_inani, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); qiniseka_thayipha(ukusho_inani(), 3); 요구(')');
            Umlayelo(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Igama = isivezi_inani();
        if (받기('(')) {
            int umsebenzi_inani = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Igama, indlela_okufakwayo_igama[수])) umsebenzi_inani = 수;
            if (umsebenzi_inani < 0) { ukwehluleka_inani("unknown static method"); return 0; }
            int 수 = 0;
            while (!Iphutha && 종류() != ')') {
                if (수 >= 함수인수수[umsebenzi_inani]) { ukwehluleka_inani("too many arguments"); break; }
                qiniseka_thayipha(ukusho_inani(), indlela_i_agumenti_thayipha[umsebenzi_inani * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[umsebenzi_inani]) ukwehluleka_inani("argument count mismatch");
            Umlayelo(184, Ireferensi(10, uhlobo_okungaguquki, Ireferensi(12, indlela_igama_okungaguquki[umsebenzi_inani], 함수서술[umsebenzi_inani])));
            return 함수반환[umsebenzi_inani];
        }
        int endaweni_umklamo = thola_endaweni(Igama), thayipha_inani = endaweni_thayipha[endaweni_umklamo]; 지역읽기(endaweni_umklamo);
        while (!Iphutha) {
            if (받기('[')) { qiniseka_thayipha(thayipha_inani, 4); qiniseka_thayipha(ukusho_inani(), 1); 요구(']'); 내보내기(50); thayipha_inani = 3; }
            else if (받기('.')) {
                if (thayipha_inani == 6 || thayipha_inani == 7) {
                    String umnikazi_inani = thayipha_inani == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Umlayelo(182, 외부참조(10, umnikazi_inani, "close", "()V")); thayipha_inani = 0; }
                    else if (thayipha_inani == 6 && 말받기("read")) { 요구('('); 요구(')'); Umlayelo(182, 외부참조(10, umnikazi_inani, "read", "()I")); thayipha_inani = 1; }
                    else if (thayipha_inani == 7 && 말받기("write")) { 요구('('); qiniseka_thayipha(ukusho_inani(), 1); 요구(')'); Umlayelo(182, 외부참조(10, umnikazi_inani, "write", "(I)V")); thayipha_inani = 0; }
                    else { ukwehluleka_inani("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (thayipha_inani == 4) { 내보내기(190); thayipha_inani = 1; }
                else { qiniseka_thayipha(thayipha_inani, 3); 요구('('); 요구(')'); Umlayelo(182, 외부참조(10, "java/lang/String", "length", "()I")); thayipha_inani = 1; }
            } else break;
        }
        return thayipha_inani;
    }
    static int 단항() {
        if (++식깊이 > 64) { ukwehluleka_inani("expression nesting too deep"); 식깊이--; return 0; }
        int thayipha_inani;
        if (받기('!')) { qiniseka_thayipha(단항(), 2); 비교값(153); thayipha_inani = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(zawula_inamba(위치++, true));
            else { qiniseka_thayipha(단항(), 1); 내보내기(116); }
            thayipha_inani = 1;
        } else if (받기('+')) { qiniseka_thayipha(단항(), 1); thayipha_inani = 1; }
        else thayipha_inani = 기본식();
        식깊이--; return thayipha_inani;
    }
    static int 곱식() {
        int thayipha_inani = 단항();
        while (!Iphutha && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int ukubhala_ngokufihla_inani = 종류(); 위치++; qiniseka_thayipha(thayipha_inani, 1); qiniseka_thayipha(단항(), 1);
            내보내기(ukubhala_ngokufihla_inani == '*' ? 104 : ukubhala_ngokufihla_inani == '/' ? 108 : 112); thayipha_inani = 1;
        }
        return thayipha_inani;
    }
    static int 합식() {
        int thayipha_inani = 곱식();
        while (!Iphutha && (종류() == '+' || 종류() == '-')) {
            int ukubhala_ngokufihla_inani = 종류(); 위치++; int 경계 = 코드크기, Impindamuva_inani_thayipha = 곱식();
            if (ukubhala_ngokufihla_inani == '+' && (thayipha_inani == 3 || Impindamuva_inani_thayipha == 3)) { 결합(경계, thayipha_inani, Impindamuva_inani_thayipha); thayipha_inani = 3; }
            else { qiniseka_thayipha(thayipha_inani, 1); qiniseka_thayipha(Impindamuva_inani_thayipha, 1); 내보내기(ukubhala_ngokufihla_inani == '+' ? 96 : 100); thayipha_inani = 1; }
        }
        return thayipha_inani;
    }
    static int 붙임참조(int thayipha_inani) {
        if (thayipha_inani != 1 && thayipha_inani != 2 && thayipha_inani != 3 && thayipha_inani != 5) ukwehluleka_inani("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", thayipha_inani == 1 ? "(I)Ljava/lang/StringBuilder;"
            : thayipha_inani == 2 ? "(Z)Ljava/lang/StringBuilder;" : thayipha_inani == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Impindamuva_inani_thayipha) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 ukusho_inani 내부의 untanga_inani igatsha 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Umlayelo(187, Ireferensi(7, Amagama_okungaguquki("java/lang/StringBuilder"), 0)); 내보내기(89);
        Umlayelo(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Umlayelo(182, 붙임참조(앞형));
        if (Iphutha) return;
        int ubude_inani = 코드크기 - 끝;
        for (int 수 = 0; 수 < ubude_inani; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + ubude_inani] = 코드[수];
        for (int 수 = 0; 수 < ubude_inani; 수++) 코드[경계 + 수] = 삽입코드[수];
        Umlayelo(182, 붙임참조(Impindamuva_inani_thayipha)); Umlayelo(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int thayipha_inani = 합식();
        while (!Iphutha && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int ukubhala_ngokufihla_inani = 종류(); 위치++; qiniseka_thayipha(thayipha_inani, 1); qiniseka_thayipha(합식(), 1);
            비교값(ukubhala_ngokufihla_inani == '<' ? 161 : ukubhala_ngokufihla_inani == '>' ? 163 : ukubhala_ngokufihla_inani == 302 ? 164 : 162); thayipha_inani = 2;
        }
        return thayipha_inani;
    }
    static int 동등식() {
        int thayipha_inani = 비교식();
        while (!Iphutha && (종류() == 300 || 종류() == 301)) {
            int ukubhala_ngokufihla_inani = 종류(); 위치++; int Impindamuva_inani_thayipha = 비교식();
            if (thayipha_inani == 0 || Impindamuva_inani_thayipha == 0) ukwehluleka_inani("void expression");
            if (!(inamba_thayipha(thayipha_inani) && inamba_thayipha(Impindamuva_inani_thayipha))) qiniseka_thayipha(Impindamuva_inani_thayipha, thayipha_inani);
            비교값((thayipha_inani <= 2 || thayipha_inani == 5 ? 159 : 165) + (ukubhala_ngokufihla_inani == 301 ? 1 : 0)); thayipha_inani = 2;
        }
        return thayipha_inani;
    }
    static int 논리곱() {
        int thayipha_inani = 동등식();
        while (!Iphutha && 받기(304)) {
            qiniseka_thayipha(thayipha_inani, 2); int 가 = igatsha(153); qiniseka_thayipha(동등식(), 2); int 나 = igatsha(153);
            내보내기(4); int 끝 = igatsha(167); xhuma_inani(가, 코드크기); xhuma_inani(나, 코드크기); 내보내기(3); xhuma_inani(끝, 코드크기); thayipha_inani = 2;
        }
        return thayipha_inani;
    }
    static int ukusho_inani() {
        int thayipha_inani = 논리곱();
        while (!Iphutha && 받기(305)) {
            qiniseka_thayipha(thayipha_inani, 2); int 가 = igatsha(154); qiniseka_thayipha(논리곱(), 2); int 나 = igatsha(154);
            내보내기(3); int 끝 = igatsha(167); xhuma_inani(가, 코드크기); xhuma_inani(나, 코드크기); 내보내기(4); xhuma_inani(끝, 코드크기); thayipha_inani = 2;
        }
        return thayipha_inani;
    }
    static void umsebenzi_womfundi_inani(boolean 선언허용) {
        if (Amagama_inani(위치, "int") || Amagama_inani(위치, "boolean") || Amagama_inani(위치, "String") || Amagama_inani(위치, "char")
            || Amagama_inani(위치, "FileInputStream") || Amagama_inani(위치, "FileOutputStream")) {
            if (!선언허용) ukwehluleka_inani("declaration not allowed here");
            int thayipha_inani = misa_inani(), Igama = isivezi_inani(); 요구('='); qiniseka_thayipha(ukusho_inani(), thayipha_inani);
            bhala_endaweni(hlanganisa_endaweni(Igama, thayipha_inani)); return;
        }
        int Igama = isivezi_inani(), endaweni_umklamo = thola_endaweni(Igama);
        if (받기('=')) { qiniseka_thayipha(ukusho_inani(), endaweni_thayipha[endaweni_umklamo]); bhala_endaweni(endaweni_umklamo); }
        else if (종류() >= 308 && 종류() <= 312) {
            int ukubhala_ngokufihla_inani = 종류(); 위치++; 지역읽기(endaweni_umklamo); int 경계 = 코드크기, Impindamuva_inani_thayipha = ukusho_inani();
            if (ukubhala_ngokufihla_inani == 308 && endaweni_thayipha[endaweni_umklamo] == 3) 결합(경계, 3, Impindamuva_inani_thayipha);
            else {
                qiniseka_thayipha(endaweni_thayipha[endaweni_umklamo], 1); qiniseka_thayipha(Impindamuva_inani_thayipha, 1);
                내보내기(ukubhala_ngokufihla_inani == 308 ? 96 : ukubhala_ngokufihla_inani == 309 ? 100 : ukubhala_ngokufihla_inani == 310 ? 104 : ukubhala_ngokufihla_inani == 311 ? 108 : 112);
                if (endaweni_thayipha[endaweni_umklamo] == 5) 내보내기(146);
            }
            bhala_endaweni(endaweni_umklamo);
        }
        else if (종류() == 306 || 종류() == 307) {
            qiniseka_thayipha(endaweni_thayipha[endaweni_umklamo], 1); 내보내기(132); 내보내기(endaweni_umklamo); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (endaweni_thayipha[endaweni_umklamo] == 5) { 지역읽기(endaweni_umklamo); 내보내기(146); bhala_endaweni(endaweni_umklamo); }
        } else ukwehluleka_inani("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Umlayelo(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean okungasho_lutho_i_agumenti = 종류() == ')';
        int thayipha_inani = okungasho_lutho_i_agumenti ? 0 : ukusho_inani(); 요구(')'); 요구(';');
        String 서술 = thayipha_inani == 0 ? "()V" : thayipha_inani == 1 ? "(I)V" : thayipha_inani == 2 ? "(Z)V" : thayipha_inani == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (thayipha_inani == 4 || thayipha_inani >= 6 || thayipha_inani == 0 && (!줄바꿈 || !okungasho_lutho_i_agumenti)) ukwehluleka_inani("unsupported print argument");
        Umlayelo(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean isitatimende_inani() {
        if (Iphutha) return false;
        if (깊이 > 32) { ukwehluleka_inani("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!Iphutha && 종류() != '}') { if (반환) ukwehluleka_inani("unreachable statement"); 반환 = isitatimende_inani(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int thayipha_inani = 종류() == ';' ? 0 : ukusho_inani(); qiniseka_thayipha(thayipha_inani, 함수반환[현재함수]); 요구(';');
            내보내기(thayipha_inani == 0 ? 177 : thayipha_inani <= 2 || thayipha_inani == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); qiniseka_thayipha(ukusho_inani(), 2); 요구(')'); int 거짓 = igatsha(153);
            깊이++; boolean 가 = isilawuli_isitatimende(); 깊이--;
            if (말받기("else")) { int 끝 = igatsha(167); xhuma_inani(거짓, 코드크기); 깊이++; boolean 나 = isilawuli_isitatimende(); 깊이--; xhuma_inani(끝, 코드크기); return 가 && 나; }
            xhuma_inani(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Sebenzisa = 코드크기; 요구('('); qiniseka_thayipha(ukusho_inani(), 2); 요구(')'); int 끝 = igatsha(153);
            깊이++; isilawuli_isitatimende(); 깊이--; xhuma_inani(igatsha(167), Sebenzisa); xhuma_inani(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') umsebenzi_womfundi_inani(true); 요구(';');
            int isimo = 코드크기; if (종류() == ';') 내보내기(4); else qiniseka_thayipha(ukusho_inani(), 2); 요구(';');
            int 끝 = igatsha(153), umzimba_wombhalo = igatsha(167), vuselela = 코드크기;
            if (종류() != ')') umsebenzi_womfundi_inani(false); 요구(')'); xhuma_inani(igatsha(167), isimo); xhuma_inani(umzimba_wombhalo, 코드크기);
            isilawuli_isitatimende(); xhuma_inani(igatsha(167), vuselela); xhuma_inani(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Amagama_inani(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int thayipha_inani = ukusho_inani(); if (thayipha_inani != 0) 내보내기(87); 요구(';'); return false;
        }
        umsebenzi_womfundi_inani(true); 요구(';'); return false;
    }
    static boolean isilawuli_isitatimende() {
        if (Amagama_inani(위치, "int") || Amagama_inani(위치, "boolean") || Amagama_inani(위치, "char") || Amagama_inani(위치, "String")
            || Amagama_inani(위치, "FileInputStream") || Amagama_inani(위치, "FileOutputStream")) ukwehluleka_inani("local declaration requires braces");
        return isitatimende_inani();
    }
    static void 출바(int inani) { if (출력크기 == 출력.length) ukwehluleka_inani("class file too large"); else 출력[출력크기++] = inani & 255; }
    static void 출짧(int inani) { 출바(inani >> 8); 출바(inani); }
    static void 출정(int inani) { 출짧(inani >>> 16); 출짧(inani); }
    static void bhala_uhlobo() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < okungaguquki_linganisa; 수++) 출바(okungaguquki_inani[수]);
        출짧(0x21); 출짧(uhlobo_okungaguquki); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(indlela_ungeno[수]); 출짧(indlela_igama_okungaguquki[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + indlela_ubude[수]); 출짧(128); 출짧(함수지역[수]); 출정(indlela_ubude[수]);
            for (int isikhala_okufakwayo = 0; isikhala_okufakwayo < indlela_ubude[수]; isikhala_okufakwayo++) 출바(코드[함수코드[수] + isikhala_okufakwayo]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Sebenzisa() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() != 1) { umsebenzisi.Bhala("Usage: javac FILE.java\n"); return 2; }
        int igama_linganisa = 자바도구.Igama(ifayela_igama_I_SMS, umsebenzisi.인수(0));
        if (igama_linganisa < 6 || igama_linganisa > 62 || ifayela_igama_I_SMS[igama_linganisa - 5] != '.' || ifayela_igama_I_SMS[igama_linganisa - 4] != 'j'
            || ifayela_igama_I_SMS[igama_linganisa - 3] != 'a' || ifayela_igama_I_SMS[igama_linganisa - 2] != 'v' || ifayela_igama_I_SMS[igama_linganisa - 1] != 'a') {
            umsebenzisi.Bhala("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        umthombo_linganisa = umsebenzisi.파일읽기(ifayela_igama_I_SMS, umthombo);
        if (umthombo_linganisa < 0) { umsebenzisi.Bhala("javac: cannot read source: "); 자바도구.수쓰기(umthombo_linganisa); umsebenzisi.bhala_uhlamvusimo_inani(10); return 1; }
        umthombo_linganisa = 자바도구.원문해독(umthombo, umthombo_linganisa);
        if (umthombo_linganisa < 0) { umsebenzisi.Bhala("javac error: invalid UTF-8 source\n"); return 1; }
        sika_inani(); if (!Iphutha) 선언읽기();
        if (!Iphutha) {
            if (ithokhini_ubude[uhlobo_ithokhini] != igama_linganisa - 5) ukwehluleka_inani("class name must match file name");
            for (int 수 = 0; 수 < igama_linganisa - 5; 수++) if (umthombo[토큰위치[uhlobo_ithokhini] + 수] != ifayela_igama_I_SMS[수]) ukwehluleka_inani("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !Iphutha; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) hlanganisa_endaweni(indlela_i_agumenti_igama[현재함수 * 16 + 수], indlela_i_agumenti_thayipha[현재함수 * 16 + 수]);
            boolean 반환 = isitatimende_inani();
            if (!반환 && 함수반환[현재함수] != 0) ukwehluleka_inani("missing return");
            // igatsha 뒤의 합류 지점은 반드시 ulwazi_ngokwenzekile_imininingwane 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean inamba = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(inamba ? 3 : 1); 내보내기(inamba ? 172 : 176); }
            if (위치 != indlela_yekisa[현재함수]) ukwehluleka_inani("invalid method body");
            함수지역[현재함수] = 지역수; indlela_ubude[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (Iphutha) return 1;
        bhala_uhlobo(); if (Iphutha) return 1;
        ifayela_igama_I_SMS[igama_linganisa - 4] = 'c'; ifayela_igama_I_SMS[igama_linganisa - 3] = 'l'; ifayela_igama_I_SMS[igama_linganisa - 2] = 'a';
        ifayela_igama_I_SMS[igama_linganisa - 1] = 's'; ifayela_igama_I_SMS[igama_linganisa] = 's'; ifayela_igama_I_SMS[igama_linganisa + 1] = 0;
        int 결과 = umsebenzisi.bhala_ifayela(ifayela_igama_I_SMS, 출력, 출력크기);
        if (결과 < 0) { umsebenzisi.Bhala("javac: cannot save class: "); 자바도구.수쓰기(결과); umsebenzisi.bhala_uhlamvusimo_inani(10); return 1; }
        umsebenzisi.Bhala("Compiled: "); for (int 수 = 0; ifayela_igama_I_SMS[수] != 0; 수++) umsebenzisi.bhala_uhlamvusimo_inani(ifayela_igama_I_SMS[수]);
        umsebenzisi.Bhala(" (JVM class version 49)\n"); return 0;
    }
}
