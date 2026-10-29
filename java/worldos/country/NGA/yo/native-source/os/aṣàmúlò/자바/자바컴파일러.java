// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 게스트에서 실행되는 제한형 Java orísun_ètò_afigijúwe -> 표준 버전 49 class 컴파일러. */
public final class 자바컴파일러 {
    static int[] orísun = new int[16384], 출력 = new int[16384], 코드 = new int[4096];
    static int[] 토큰종류 = new int[2048], 토큰위치 = new int[2048], kóòdù_káàdì_àsansílẹ̀_gígùn = new int[2048];
    static int[] aláìṣeéyípadà_iye = new int[4096], aláìṣeéyípadà_Ìtayọ = new int[512];
    static int[] 문자 = new int[512], fáìlì_orúkọ_SMS = new int[64];
    static int[] 삽입코드 = new int[16];
    static int orísun_ìwọn, 토큰수, 위치, 코드크기, aláìṣeéyípadà_ìwọn, 상수수 = 1, 출력크기, ẹyọ_ọ̀rọ̀_gígùn;
    static boolean àṣìṣe;
    static int ọ̀wọ́_kóòdù_káàdì_àsansílẹ̀, ọ̀wọ́_aláìṣeéyípadà, 부모상수, 코드상수;
    static int[] ìlànà_ìgbéwọlé_orúkọ = new int[32], 함수반환 = new int[32], 함수인수수 = new int[32];
    static int[] ìlànà_ágúmẹ́ntì_orúkọ = new int[512], ìlànà_ágúmẹ́ntì_irú = new int[512];
    static int[] 함수본문 = new int[32], ìlànà_parí = new int[32], 함수코드 = new int[32];
    static int[] ìlànà_gígùn = new int[32], 함수지역 = new int[32], ìlànà_orúkọ_aláìṣeéyípadà = new int[32], 함수서술 = new int[32];
    static int[] ìlànà_wáyè_sí = new int[32];
    static int 함수수, 현재함수, 지역수, 깊이, 식깊이;
    static int[] agbègbè_orúkọ = new int[128], agbègbè_irú = new int[128], 지역깊이 = new int[128];

    static void ìkùnà_iye(String 이유) {
        if (!àṣìṣe) {
            aṣàmúlò.Kọ("javac error: "); aṣàmúlò.Kọ(이유);
            aṣàmúlò.Kọ(" at line ");
            int ìlà = 1, 끝 = 위치 < 토큰수 ? 토큰위치[위치] : orísun_ìwọn;
            for (int 수 = 0; 수 < 끝; 수++) if (orísun[수] == 10) ìlà++;
            자바도구.수쓰기(ìlà); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10);
        }
        àṣìṣe = true;
    }
    static boolean ẹyọ_ọ̀rọ̀_iye(int iye) { return 문자이름규칙.첫글자(iye); }
    static boolean díjììtì_iye(int iye) { return iye >= '0' && iye <= '9'; }
    static boolean 이름같음(int 가, int 나) {
        if (가 < 0 || 나 < 0 || 가 >= 토큰수 || 나 >= 토큰수 || kóòdù_káàdì_àsansílẹ̀_gígùn[가] != kóòdù_káàdì_àsansílẹ̀_gígùn[나]) return false;
        for (int 수 = 0; 수 < kóòdù_káàdì_àsansílẹ̀_gígùn[가]; 수++) if (orísun[토큰위치[가] + 수] != orísun[토큰위치[나] + 수]) return false;
        return true;
    }
    static boolean Ọ̀rọ̀_iye(int kóòdù_káàdì_àsansílẹ̀_iye, String Ọ̀rọ̀_SMS) {
        if (kóòdù_káàdì_àsansílẹ̀_iye < 0 || kóòdù_káàdì_àsansílẹ̀_iye >= 토큰수 || kóòdù_káàdì_àsansílẹ̀_gígùn[kóòdù_káàdì_àsansílẹ̀_iye] != Ọ̀rọ̀_SMS.length()) return false;
        for (int 수 = 0; 수 < Ọ̀rọ̀_SMS.length(); 수++) if (orísun[토큰위치[kóòdù_káàdì_àsansílẹ̀_iye] + 수] != Ọ̀rọ̀_SMS.charAt(수)) return false;
        return true;
    }
    static int 종류() { return 위치 < 토큰수 ? 토큰종류[위치] : 0; }
    static boolean 받기(int iye) { if (종류() != iye) return false; 위치++; return true; }
    static void 요구(int iye) { if (!받기(iye)) ìkùnà_iye("unexpected token"); }
    static boolean 말받기(String Ọ̀rọ̀_SMS) { if (!Ọ̀rọ̀_iye(위치, Ọ̀rọ̀_SMS)) return false; 위치++; return true; }
    static void 말요구(String Ọ̀rọ̀_SMS) { if (!말받기(Ọ̀rọ̀_SMS)) ìkùnà_iye(Ọ̀rọ̀_SMS); }
    static int Àfidámọ̀_iye() {
        int 결과 = 위치;
        if (종류() != 256) ìkùnà_iye("identifier required"); else 위치++;
        String 예약어 = "abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null";
        int Rọ́ọ̀nù = 0;
        for (int 수 = 0; 수 <= 예약어.length(); 수++) {
            if (수 == 예약어.length() || 예약어.charAt(수) == ' ') {
                boolean 같음 = 수 - Rọ́ọ̀nù == kóòdù_káàdì_àsansílẹ̀_gígùn[결과];
                for (int ààyè_ìfàyọkàsí_ìgbéwọlé = Rọ́ọ̀nù; 같음 && ààyè_ìfàyọkàsí_ìgbéwọlé < 수; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (예약어.charAt(ààyè_ìfàyọkàsí_ìgbéwọlé) != orísun[토큰위치[결과] + ààyè_ìfàyọkàsí_ìgbéwọlé - Rọ́ọ̀nù]) 같음 = false;
                if (같음) ìkùnà_iye("reserved word cannot be an identifier");
                Rọ́ọ̀nù = 수 + 1;
            }
        }
        return 결과;
    }
    static void gé_kúrò_iye() {
        int 수 = 0;
        while (수 < orísun_ìwọn && !àṣìṣe) {
            int iye = orísun[수], Rọ́ọ̀nù = 수, 종류 = iye;
            if (iye == 32 || iye == 9 || iye == 10 || iye == 13) { 수++; continue; }
            if (iye == '/' && 수 + 1 < orísun_ìwọn && orísun[수 + 1] == '/') {
                while (수 < orísun_ìwọn && orísun[수] != 10) 수++;
                continue;
            }
            if (iye == '/' && 수 + 1 < orísun_ìwọn && orísun[수 + 1] == '*') {
                수 += 2;
                while (수 + 1 < orísun_ìwọn && !(orísun[수] == '*' && orísun[수 + 1] == '/')) 수++;
                if (수 + 1 >= orísun_ìwọn) { ìkùnà_iye("unterminated comment"); break; }
                수 += 2; continue;
            }
            if (ẹyọ_ọ̀rọ̀_iye(iye)) { 종류 = 256; while (수 < orísun_ìwọn && 문자이름규칙.이어진글자(orísun[수])) 수++; }
            else if (díjììtì_iye(iye)) { 종류 = 257; while (수 < orísun_ìwọn && díjììtì_iye(orísun[수])) 수++; }
            else if (iye == '"' || iye == '\'') {
                종류 = iye == '"' ? 258 : 259; 수++;
                while (수 < orísun_ìwọn && orísun[수] != iye && orísun[수] != 10 && orísun[수] != 13) {
                    if (orísun[수] == '\\') 수++;
                    수++;
                }
                if (수 >= orísun_ìwọn || orísun[수] != iye) { ìkùnà_iye("unterminated literal"); break; }
                수++;
            } else {
                수++;
                if (수 < orísun_ìwọn) {
                    int 다음 = orísun[수];
                    if (iye == '=' && 다음 == '=') 종류 = 300;
                    if (iye == '!' && 다음 == '=') 종류 = 301;
                    if (iye == '<' && 다음 == '=') 종류 = 302;
                    if (iye == '>' && 다음 == '=') 종류 = 303;
                    if (iye == '&' && 다음 == '&') 종류 = 304;
                    if (iye == '|' && 다음 == '|') 종류 = 305;
                    if (iye == '+' && 다음 == '+') 종류 = 306;
                    if (iye == '-' && 다음 == '-') 종류 = 307;
                    if (iye == '+' && 다음 == '=') 종류 = 308;
                    if (iye == '-' && 다음 == '=') 종류 = 309;
                    if (iye == '*' && 다음 == '=') 종류 = 310;
                    if (iye == '/' && 다음 == '=') 종류 = 311;
                    if (iye == '%' && 다음 == '=') 종류 = 312;
                    if (종류 >= 300) 수++;
                }
            }
            if (토큰수 == 토큰종류.length - 1) { ìkùnà_iye("too many tokens (2047 maximum)"); break; }
            토큰종류[토큰수] = 종류; 토큰위치[토큰수] = Rọ́ọ̀nù; kóòdù_káàdì_àsansílẹ̀_gígùn[토큰수++] = 수 - Rọ́ọ̀nù;
        }
    }
    static void kọ_aláìṣeéyípadà_báìtì(int iye) {
        if (aláìṣeéyípadà_ìwọn == aláìṣeéyípadà_iye.length) { ìkùnà_iye("constant pool too large"); return; }
        aláìṣeéyípadà_iye[aláìṣeéyípadà_ìwọn++] = iye & 255;
    }
    static void 상짧(int iye) { kọ_aláìṣeéyípadà_báìtì(iye >> 8); kọ_aláìṣeéyípadà_báìtì(iye); }
    static int forúkọsílẹ̀_aláìṣeéyípadà(int Rọ́ọ̀nù) {
        for (int 수 = 1; 수 < 상수수; 수++) {
            int 앞 = aláìṣeéyípadà_Ìtayọ[수], gígùn_iye = (수 + 1 < 상수수 ? aláìṣeéyípadà_Ìtayọ[수 + 1] : Rọ́ọ̀nù) - 앞;
            if (gígùn_iye != aláìṣeéyípadà_ìwọn - Rọ́ọ̀nù) continue;
            boolean 같음 = true;
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < gígùn_iye; ààyè_ìfàyọkàsí_ìgbéwọlé++) if (aláìṣeéyípadà_iye[앞 + ààyè_ìfàyọkàsí_ìgbéwọlé] != aláìṣeéyípadà_iye[Rọ́ọ̀nù + ààyè_ìfàyọkàsí_ìgbéwọlé]) 같음 = false;
            if (같음) { aláìṣeéyípadà_ìwọn = Rọ́ọ̀nù; return 수; }
        }
        if (상수수 == aláìṣeéyípadà_Ìtayọ.length) { ìkùnà_iye("too many constants"); return 0; }
        aláìṣeéyípadà_Ìtayọ[상수수] = Rọ́ọ̀nù;
        return 상수수++;
    }
    static void 글추가(int iye) {
        if (ẹyọ_ọ̀rọ̀_gígùn == 문자.length) { ìkùnà_iye("text too long"); return; }
        문자[ẹyọ_ọ̀rọ̀_gígùn++] = iye;
    }
    static void 말추가(String Ọ̀rọ̀_SMS) { for (int 수 = 0; 수 < Ọ̀rọ̀_SMS.length(); 수++) 글추가(Ọ̀rọ̀_SMS.charAt(수)); }
    static int ẹyọ_ọ̀rọ̀_aláìṣeéyípadà() {
        int Rọ́ọ̀nù = aláìṣeéyípadà_ìwọn; kọ_aláìṣeéyípadà_báìtì(1); 상짧(0);
        for (int 수 = 0; 수 < ẹyọ_ọ̀rọ̀_gígùn; 수++) {
            int iye = 문자[수];
            if (iye > 0 && iye < 128) kọ_aláìṣeéyípadà_báìtì(iye);
            else if (iye < 2048) { kọ_aláìṣeéyípadà_báìtì(192 | iye >> 6); kọ_aláìṣeéyípadà_báìtì(128 | iye & 63); }
            else { kọ_aláìṣeéyípadà_báìtì(224 | iye >> 12); kọ_aláìṣeéyípadà_báìtì(128 | iye >> 6 & 63); kọ_aláìṣeéyípadà_báìtì(128 | iye & 63); }
        }
        if (àṣìṣe) return 0;
        int gígùn_iye = aláìṣeéyípadà_ìwọn - Rọ́ọ̀nù - 3;
        aláìṣeéyípadà_iye[Rọ́ọ̀nù + 1] = gígùn_iye >> 8; aláìṣeéyípadà_iye[Rọ́ọ̀nù + 2] = gígùn_iye & 255;
        return forúkọsílẹ̀_aláìṣeéyípadà(Rọ́ọ̀nù);
    }
    static int Ọ̀rọ̀_aláìṣeéyípadà(String Ọ̀rọ̀_SMS) { ẹyọ_ọ̀rọ̀_gígùn = 0; 말추가(Ọ̀rọ̀_SMS); return ẹyọ_ọ̀rọ̀_aláìṣeéyípadà(); }
    static int kóòdù_káàdì_àsansílẹ̀_aláìṣeéyípadà(int kóòdù_káàdì_àsansílẹ̀_iye) {
        ẹyọ_ọ̀rọ̀_gígùn = 0;
        for (int 수 = 0; 수 < kóòdù_káàdì_àsansílẹ̀_gígùn[kóòdù_káàdì_àsansílẹ̀_iye]; 수++) 글추가(orísun[토큰위치[kóòdù_káàdì_àsansílẹ̀_iye] + 수]);
        return ẹyọ_ọ̀rọ̀_aláìṣeéyípadà();
    }
    static int Ìtọ́ka(int 종류, int 가, int 나) {
        int Rọ́ọ̀nù = aláìṣeéyípadà_ìwọn; kọ_aláìṣeéyípadà_báìtì(종류); 상짧(가);
        if (종류 == 9 || 종류 == 10 || 종류 == 12) 상짧(나);
        return forúkọsílẹ̀_aláìṣeéyípadà(Rọ́ọ̀nù);
    }
    static int 외부참조(int 종류, String Oníǹkan_iye, String Orúkọ, String 서술) {
        int Oníǹkan_Àfidámọ̀ = Ìtọ́ka(7, Ọ̀rọ̀_aláìṣeéyípadà(Oníǹkan_iye), 0);
        int 이름수 = Ọ̀rọ̀_aláìṣeéyípadà(Orúkọ), 형식수 = Ọ̀rọ̀_aláìṣeéyípadà(서술);
        return Ìtọ́ka(종류, Oníǹkan_Àfidámọ̀, Ìtọ́ka(12, 이름수, 형식수));
    }
    static void 내보내기(int iye) {
        if (코드크기 == 코드.length) { ìkùnà_iye("bytecode too large"); return; }
        코드[코드크기++] = iye & 255;
    }
    static void Àṣẹ(int iye, int 인수) { 내보내기(iye); 내보내기(인수 >> 8); 내보내기(인수); }
    static void 수상수(int iye) {
        if (iye >= -1 && iye <= 5) { 내보내기(iye + 3); return; }
        int Rọ́ọ̀nù = aláìṣeéyípadà_ìwọn; kọ_aláìṣeéyípadà_báìtì(3); 상짧(iye >>> 16); 상짧(iye);
        Àṣẹ(19, forúkọsílẹ̀_aláìṣeéyípadà(Rọ́ọ̀nù));
    }
    static int ẹ̀ka(int Àṣẹ) { int 결과 = 코드크기; Àṣẹ(Àṣẹ, 0); return 결과; }
    static void ṣàsopọ̀_iye_ff3cc3dc(int ẹ̀ka, int àfojúsùn_nǹkan) {
        if (àṣìṣe) return;
        int 거리 = àfojúsùn_nǹkan - ẹ̀ka;
        if (거리 < -32768 || 거리 > 32767 || ẹ̀ka < 0 || ẹ̀ka + 2 >= 코드크기) { ìkùnà_iye("invalid branch"); return; }
        코드[ẹ̀ka + 1] = 거리 >> 8 & 255; 코드[ẹ̀ka + 2] = 거리 & 255;
    }
    static void 비교값(int Àṣẹ) {
        int 참 = ẹ̀ka(Àṣẹ); 내보내기(3); int 끝 = ẹ̀ka(167);
        ṣàsopọ̀_iye_ff3cc3dc(참, 코드크기); 내보내기(4); ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기);
    }
    static int ìgúnrégé_iye() {
        if (말받기("void")) return 0;
        if (말받기("int")) return 1;
        if (말받기("boolean")) return 2;
        if (말받기("char")) return 5;
        if (말받기("FileInputStream")) return 6;
        if (말받기("FileOutputStream")) return 7;
        if (말받기("String")) { if (받기('[')) { 요구(']'); return 4; } return 3; }
        ìkùnà_iye("supported types: int, boolean, String, String[] and void"); return 0;
    }
    static void ròmọ́_ìgúnrégé(int irú_iye) {
        if (irú_iye == 0) 글추가('V');
        if (irú_iye == 1) 글추가('I');
        if (irú_iye == 2) 글추가('Z');
        if (irú_iye == 3) 말추가("Ljava/lang/String;");
        if (irú_iye == 4) 말추가("[Ljava/lang/String;");
        if (irú_iye == 5) 글추가('C');
        if (irú_iye == 6) 말추가("Ljava/io/FileInputStream;");
        if (irú_iye == 7) 말추가("Ljava/io/FileOutputStream;");
    }
    // 제한형 컴파일러의 throws 선언. 예외 Ìlànà_iye_ìgbéwọlé 본문은 olùpèsè javac를 사용한다.
    static void 예외이름읽기() {
        boolean 한국어묶음 = 말받기("한국어");
        if (한국어묶음) { 요구('.'); 말요구("자체"); 요구('.'); }
        if (!한국어묶음 && (말받기("Exception") || 말받기("IOException"))) return;
        if (말받기("예외") || 말받기("실행예외") || 말받기("입출력예외") || 말받기("대기시간초과예외") || 말받기("주소확인예외") || 말받기("파일없음예외") || 말받기("통신예외") || 말받기("잘못된인수예외") || 말받기("숫자형식예외") || 말받기("범위예외") || 말받기("배열범위예외") || 말받기("문자열범위예외") || 말받기("빈참조예외") || 말받기("산술예외") || 말받기("상태예외") || 말받기("형변환예외") || 말받기("음수배열크기예외") || 말받기("ÀRÉÈ_Store_ìkùnà") || 말받기("가닥상태예외") || 말받기("대기중단예외")) return;
        ìkùnà_iye("unsupported throws type");
    }
    static void 선언읽기() {
        while (말받기("import")) {
            if (Ọ̀rọ̀_iye(위치, "한국어")) 예외이름읽기();
            else {
                말요구("java"); 요구('.'); 말요구("io"); 요구('.');
                if (!(말받기("FileInputStream") || 말받기("FileOutputStream") || 말받기("IOException"))) ìkùnà_iye("unsupported import");
            }
            요구(';');
        }
        말받기("public"); 말받기("final"); 말요구("class"); ọ̀wọ́_kóòdù_káàdì_àsansílẹ̀ = Àfidámọ̀_iye();
        ọ̀wọ́_aláìṣeéyípadà = Ìtọ́ka(7, kóòdù_káàdì_àsansílẹ̀_aláìṣeéyípadà(ọ̀wọ́_kóòdù_káàdì_àsansílẹ̀), 0);
        부모상수 = Ìtọ́ka(7, Ọ̀rọ̀_aláìṣeéyípadà("java/lang/Object"), 0); 코드상수 = Ọ̀rọ̀_aláìṣeéyípadà("Code"); 요구('{');
        while (!àṣìṣe && 종류() != '}') {
            if (함수수 == 32) { ìkùnà_iye("too many methods"); break; }
            int wáyè_sí_ìgbéwọlé = 말받기("public") ? 1 : 말받기("private") ? 2 : 0; 말요구("static");
            int ÀKÀNṢEFỌMÚLÀ_iye = 함수수++;
            ìlànà_wáyè_sí[ÀKÀNṢEFỌMÚLÀ_iye] = wáyè_sí_ìgbéwọlé | 8;
            함수반환[ÀKÀNṢEFỌMÚLÀ_iye] = ìgúnrégé_iye(); ìlànà_ìgbéwọlé_orúkọ[ÀKÀNṢEFỌMÚLÀ_iye] = Àfidámọ̀_iye(); 요구('(');
            for (int 앞 = 0; 앞 < ÀKÀNṢEFỌMÚLÀ_iye; 앞++) if (이름같음(ìlànà_ìgbéwọlé_orúkọ[앞], ìlànà_ìgbéwọlé_orúkọ[ÀKÀNṢEFỌMÚLÀ_iye])) ìkùnà_iye("duplicate method (overloading unsupported)");
            while (!àṣìṣe && 종류() != ')') {
                int 수 = 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye];
                if (수 == 16) { ìkùnà_iye("too many parameters"); break; }
                int irú_iye = ìgúnrégé_iye(); if (irú_iye == 0) ìkùnà_iye("void parameter");
                ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수] = irú_iye; ìlànà_ágúmẹ́ntì_orúkọ[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수] = Àfidámọ̀_iye();
                함수인수수[ÀKÀNṢEFỌMÚLÀ_iye]++;
                if (!받기(',')) break;
            }
            요구(')');
            if (말받기("throws")) {
                do { 예외이름읽기(); } while (!àṣìṣe && 받기(','));
            }
            함수본문[ÀKÀNṢEFỌMÚLÀ_iye] = 위치; 요구('{');
            int 중첩 = 1;
            while (위치 < 토큰수 && 중첩 > 0) {
                if (종류() == '{') 중첩++;
                if (종류() == '}') 중첩--;
                위치++;
            }
            if (중첩 != 0) ìkùnà_iye("unclosed method body");
            ìlànà_parí[ÀKÀNṢEFỌMÚLÀ_iye] = 위치;
            ìlànà_orúkọ_aláìṣeéyípadà[ÀKÀNṢEFỌMÚLÀ_iye] = kóòdù_káàdì_àsansílẹ̀_aláìṣeéyípadà(ìlànà_ìgbéwọlé_orúkọ[ÀKÀNṢEFỌMÚLÀ_iye]);
            ẹyọ_ọ̀rọ̀_gígùn = 0; 글추가('(');
            for (int 수 = 0; 수 < 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye]; 수++) ròmọ́_ìgúnrégé(ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수]);
            글추가(')'); ròmọ́_ìgúnrégé(함수반환[ÀKÀNṢEFỌMÚLÀ_iye]); 함수서술[ÀKÀNṢEFỌMÚLÀ_iye] = ẹyọ_ọ̀rọ̀_aláìṣeéyípadà();
        }
        요구('}'); if (위치 != 토큰수) ìkùnà_iye("extra input after class");
    }
    static int wá_agbègbè(int Orúkọ) {
        for (int 수 = 지역수 - 1; 수 >= 0; 수--) if (지역깊이[수] >= 0 && 이름같음(agbègbè_orúkọ[수], Orúkọ)) return 수;
        ìkùnà_iye("unknown variable"); return 0;
    }
    static int ròmọ́_agbègbè(int Orúkọ, int irú_iye) {
        for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] >= 0 && 이름같음(agbègbè_orúkọ[수], Orúkọ)) ìkùnà_iye("duplicate local variable");
        if (지역수 == 128) { ìkùnà_iye("too many locals"); return 0; }
        agbègbè_orúkọ[지역수] = Orúkọ; agbègbè_irú[지역수] = irú_iye; 지역깊이[지역수] = 깊이;
        return 지역수++;
    }
    static boolean nọ́ńbà_odindi_irú(int irú_iye) { return irú_iye == 1 || irú_iye == 5; }
    static void 지역읽기(int 수) { 내보내기(agbègbè_irú[수] <= 2 || agbègbè_irú[수] == 5 ? 21 : 25); 내보내기(수); }
    static void kọ_agbègbè(int 수) { 내보내기(agbègbè_irú[수] <= 2 || agbègbè_irú[수] == 5 ? 54 : 58); 내보내기(수); }
    static void ridájú_irú(int gangan_détà, int 기대) { if (gangan_détà != 기대 && !(gangan_détà == 5 && 기대 == 1)) ìkùnà_iye("type mismatch"); }
    static void 문자읽기(int kóòdù_káàdì_àsansílẹ̀_iye) {
        ẹyọ_ọ̀rọ̀_gígùn = 0; int Rọ́ọ̀nù = 토큰위치[kóòdù_káàdì_àsansílẹ̀_iye] + 1, 끝 = 토큰위치[kóòdù_káàdì_àsansílẹ̀_iye] + kóòdù_káàdì_àsansílẹ̀_gígùn[kóòdù_káàdì_àsansílẹ̀_iye] - 1;
        while (Rọ́ọ̀nù < 끝 && !àṣìṣe) {
            int iye = orísun[Rọ́ọ̀nù++];
            if (iye == '\\') {
                if (Rọ́ọ̀nù == 끝) { ìkùnà_iye("invalid escape"); break; }
                iye = orísun[Rọ́ọ̀nù++];
                if (iye == 'n') iye = 10;
                else if (iye == 'r') iye = 13;
                else if (iye == 't') iye = 9;
                else if (iye == 'b') iye = 8;
                else if (iye == 'f') iye = 12;
                else if (iye != '\\' && iye != '"' && iye != '\'') ìkùnà_iye("unsupported escape");
            }
            글추가(iye);
        }
    }
    static int ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(int kóòdù_káàdì_àsansílẹ̀_iye, boolean 음수) {
        if (kóòdù_káàdì_àsansílẹ̀_gígùn[kóòdù_káàdì_àsansílẹ̀_iye] > 1 && orísun[토큰위치[kóòdù_káàdì_àsansílẹ̀_iye]] == '0') ìkùnà_iye("octal literals unsupported");
        int iye = 0;
        for (int 수 = 0; 수 < kóòdù_káàdì_àsansílẹ̀_gígùn[kóòdù_káàdì_àsansílẹ̀_iye]; 수++) {
            int díjììtì_wúnrẹ̀n = orísun[토큰위치[kóòdù_káàdì_àsansílẹ̀_iye] + 수] - '0';
            if (iye < -214748364 || iye == -214748364 && díjììtì_wúnrẹ̀n > (음수 ? 8 : 7)) ìkùnà_iye("integer literal out of range");
            iye = iye * 10 - díjììtì_wúnrẹ̀n;
        }
        return 음수 ? iye : -iye;
    }
    static int 기본식() {
        if (말받기("new")) {
            int irú_iye = ìgúnrégé_iye();
            if (irú_iye != 6 && irú_iye != 7) { ìkùnà_iye("only file streams supported by new in source"); return 0; }
            String Oníǹkan_iye = irú_iye == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
            Àṣẹ(187, Ìtọ́ka(7, Ọ̀rọ̀_aláìṣeéyípadà(Oníǹkan_iye), 0)); 내보내기(89);
            요구('('); ridájú_irú(ìsọ̀rọ̀sí_iye(), 3); boolean 이어 = false;
            if (받기(',')) { if (irú_iye != 7) ìkùnà_iye("input stream constructor arguments"); ridájú_irú(ìsọ̀rọ̀sí_iye(), 2); 이어 = true; }
            요구(')');
            Àṣẹ(183, 외부참조(10, Oníǹkan_iye, "<init>", 이어 ? "(Ljava/lang/String;Z)V" : "(Ljava/lang/String;)V"));
            return irú_iye;
        }
        if (받기('(')) { int irú_iye = ìsọ̀rọ̀sí_iye(); 요구(')'); return irú_iye; }
        if (종류() == 257) { 수상수(ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(위치++, false)); return 1; }
        if (종류() == 258) { 문자읽기(위치++); Àṣẹ(19, Ìtọ́ka(8, ẹyọ_ọ̀rọ̀_aláìṣeéyípadà(), 0)); return 3; }
        if (종류() == 259) { 문자읽기(위치++); if (ẹyọ_ọ̀rọ̀_gígùn != 1) ìkùnà_iye("character literal length"); 수상수(문자[0]); return 5; }
        if (말받기("true")) { 내보내기(4); return 2; }
        if (말받기("false")) { 내보내기(3); return 2; }
        if (말받기("한국어")) {
            요구('.'); 말요구("자체"); 요구('.');
            String Oníǹkan_iye = "", ìlànà_iye = "", 서술 = ""; int 가 = 0, 나 = 0, 다 = 0, 라 = 0, 마 = 0, 결과 = 0;
            if (말받기("출력")) {
                Oníǹkan_iye = "한국어/자체/출력"; 요구('.');
                if (말받기("kọ_ìlà")) { ìlànà_iye = "kọ_ìlà"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("Kọ")) { ìlànà_iye = "Kọ"; 서술 = "(Ljava/lang/String;)V"; 가 = 3; }
                else if (말받기("수쓰기")) { ìlànà_iye = "수쓰기"; 서술 = "(I)V"; 가 = 1; }
                else ìkùnà_iye("unknown Korean output method");
            } else if (말받기("문자")) {
                Oníǹkan_iye = "한국어/자체/문자"; 요구('.'); 가 = 3;
                if (말받기("gígùn_iye")) { ìlànà_iye = "gígùn_iye"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("코드포인트수")) { ìlànà_iye = "코드포인트수"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("ìpínsíwẹ́wẹ́_nọ́ńbà_odindi")) { ìlànà_iye = "ìpínsíwẹ́wẹ́_nọ́ńbà_odindi"; 서술 = "(Ljava/lang/String;)I"; 결과 = 1; }
                else if (말받기("kọ_nọ́ńbà_odindi_iye")) { ìlànà_iye = "kọ_nọ́ńbà_odindi_iye"; 서술 = "(I)Ljava/lang/String;"; 가 = 1; 결과 = 3; }
                else if (말받기("같음")) { ìlànà_iye = "같음"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Z"; 나 = 3; 결과 = 2; }
                else if (말받기("lẹ_SMS")) { ìlànà_iye = "lẹ_SMS"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;"; 나 = 3; 결과 = 3; }
                else if (말받기("gé_kúrò_iye")) { ìlànà_iye = "gé_kúrò_iye"; 서술 = "(Ljava/lang/String;II)Ljava/lang/String;"; 나 = 1; 다 = 1; 결과 = 3; }
                else ìkùnà_iye("unknown Korean text method");
            } else if (말받기("Fáìlì")) {
                Oníǹkan_iye = "한국어/자체/Fáìlì"; 요구('.'); 가 = 3;
                if (말받기("Kàá")) { ìlànà_iye = "Kàá"; 서술 = "(Ljava/lang/String;)Ljava/lang/String;"; 결과 = 3; }
                else if (말받기("Kọ")) { ìlànà_iye = "Kọ"; 서술 = "(Ljava/lang/String;Ljava/lang/String;)V"; 나 = 3; }
                else ìkùnà_iye("unknown Korean file method");
            } else if (말받기("화면")) {
                Oníǹkan_iye = "한국어/자체/화면"; 요구('.');
                if (말받기("너비")) { ìlànà_iye = "너비"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("높이")) { ìlànà_iye = "높이"; 서술 = "()I"; 결과 = 1; }
                else if (말받기("사각형")) { ìlànà_iye = "사각형"; 서술 = "(IIIII)V"; 가 = 1; 나 = 1; 다 = 1; 라 = 1; 마 = 1; }
                else if (말받기("지우기")) { ìlànà_iye = "지우기"; 서술 = "(I)V"; 가 = 1; }
                else if (말받기("기다리기")) { ìlànà_iye = "기다리기"; 서술 = "()V"; }
                else ìkùnà_iye("unknown Korean framebuffer method");
            } else ìkùnà_iye("unsupported Korean library class");
            요구('('); if (가 != 0) ridájú_irú(ìsọ̀rọ̀sí_iye(), 가);
            if (나 != 0) { 요구(','); ridájú_irú(ìsọ̀rọ̀sí_iye(), 나); }
            if (다 != 0) { 요구(','); ridájú_irú(ìsọ̀rọ̀sí_iye(), 다); }
            if (라 != 0) { 요구(','); ridájú_irú(ìsọ̀rọ̀sí_iye(), 라); }
            if (마 != 0) { 요구(','); ridájú_irú(ìsọ̀rọ̀sí_iye(), 마); }
            요구(')'); Àṣẹ(184, 외부참조(10, Oníǹkan_iye, ìlànà_iye, 서술)); return 결과;
        }
        if (말받기("Integer")) {
            요구('.'); 말요구("parseInt"); 요구('('); ridájú_irú(ìsọ̀rọ̀sí_iye(), 3); 요구(')');
            Àṣẹ(184, 외부참조(10, "java/lang/Integer", "parseInt", "(Ljava/lang/String;)I")); return 1;
        }
        int Orúkọ = Àfidámọ̀_iye();
        if (받기('(')) {
            int ÀKÀNṢEFỌMÚLÀ_iye = -1;
            for (int 수 = 0; 수 < 함수수; 수++) if (이름같음(Orúkọ, ìlànà_ìgbéwọlé_orúkọ[수])) ÀKÀNṢEFỌMÚLÀ_iye = 수;
            if (ÀKÀNṢEFỌMÚLÀ_iye < 0) { ìkùnà_iye("unknown static method"); return 0; }
            int 수 = 0;
            while (!àṣìṣe && 종류() != ')') {
                if (수 >= 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye]) { ìkùnà_iye("too many arguments"); break; }
                ridájú_irú(ìsọ̀rọ̀sí_iye(), ìlànà_ágúmẹ́ntì_irú[ÀKÀNṢEFỌMÚLÀ_iye * 16 + 수++]); if (!받기(',')) break;
            }
            요구(')'); if (수 != 함수인수수[ÀKÀNṢEFỌMÚLÀ_iye]) ìkùnà_iye("argument count mismatch");
            Àṣẹ(184, Ìtọ́ka(10, ọ̀wọ́_aláìṣeéyípadà, Ìtọ́ka(12, ìlànà_orúkọ_aláìṣeéyípadà[ÀKÀNṢEFỌMÚLÀ_iye], 함수서술[ÀKÀNṢEFỌMÚLÀ_iye])));
            return 함수반환[ÀKÀNṢEFỌMÚLÀ_iye];
        }
        int agbègbè_sàkání = wá_agbègbè(Orúkọ), irú_iye = agbègbè_irú[agbègbè_sàkání]; 지역읽기(agbègbè_sàkání);
        while (!àṣìṣe) {
            if (받기('[')) { ridájú_irú(irú_iye, 4); ridájú_irú(ìsọ̀rọ̀sí_iye(), 1); 요구(']'); 내보내기(50); irú_iye = 3; }
            else if (받기('.')) {
                if (irú_iye == 6 || irú_iye == 7) {
                    String Oníǹkan_iye = irú_iye == 6 ? "java/io/FileInputStream" : "java/io/FileOutputStream";
                    if (말받기("close")) { 요구('('); 요구(')'); Àṣẹ(182, 외부참조(10, Oníǹkan_iye, "close", "()V")); irú_iye = 0; }
                    else if (irú_iye == 6 && 말받기("read")) { 요구('('); 요구(')'); Àṣẹ(182, 외부참조(10, Oníǹkan_iye, "read", "()I")); irú_iye = 1; }
                    else if (irú_iye == 7 && 말받기("write")) { 요구('('); ridájú_irú(ìsọ̀rọ̀sí_iye(), 1); 요구(')'); Àṣẹ(182, 외부참조(10, Oníǹkan_iye, "write", "(I)V")); irú_iye = 0; }
                    else { ìkùnà_iye("unsupported file stream method"); }
                    continue;
                }
                말요구("length");
                if (irú_iye == 4) { 내보내기(190); irú_iye = 1; }
                else { ridájú_irú(irú_iye, 3); 요구('('); 요구(')'); Àṣẹ(182, 외부참조(10, "java/lang/String", "length", "()I")); irú_iye = 1; }
            } else break;
        }
        return irú_iye;
    }
    static int 단항() {
        if (++식깊이 > 64) { ìkùnà_iye("expression nesting too deep"); 식깊이--; return 0; }
        int irú_iye;
        if (받기('!')) { ridájú_irú(단항(), 2); 비교값(153); irú_iye = 2; }
        else if (받기('-')) {
            if (종류() == 257) 수상수(ìpínsíwẹ́wẹ́_nọ́ńbà_odindi(위치++, true));
            else { ridájú_irú(단항(), 1); 내보내기(116); }
            irú_iye = 1;
        } else if (받기('+')) { ridájú_irú(단항(), 1); irú_iye = 1; }
        else irú_iye = 기본식();
        식깊이--; return irú_iye;
    }
    static int 곱식() {
        int irú_iye = 단항();
        while (!àṣìṣe && (종류() == '*' || 종류() == '/' || 종류() == '%')) {
            int pípàrokò_iye = 종류(); 위치++; ridájú_irú(irú_iye, 1); ridájú_irú(단항(), 1);
            내보내기(pípàrokò_iye == '*' ? 104 : pípàrokò_iye == '/' ? 108 : 112); irú_iye = 1;
        }
        return irú_iye;
    }
    static int 합식() {
        int irú_iye = 곱식();
        while (!àṣìṣe && (종류() == '+' || 종류() == '-')) {
            int pípàrokò_iye = 종류(); 위치++; int 경계 = 코드크기, Padà_sẹ́yìn_iye_irú = 곱식();
            if (pípàrokò_iye == '+' && (irú_iye == 3 || Padà_sẹ́yìn_iye_irú == 3)) { 결합(경계, irú_iye, Padà_sẹ́yìn_iye_irú); irú_iye = 3; }
            else { ridájú_irú(irú_iye, 1); ridájú_irú(Padà_sẹ́yìn_iye_irú, 1); 내보내기(pípàrokò_iye == '+' ? 96 : 100); irú_iye = 1; }
        }
        return irú_iye;
    }
    static int 붙임참조(int irú_iye) {
        if (irú_iye != 1 && irú_iye != 2 && irú_iye != 3 && irú_iye != 5) ìkùnà_iye("unsupported concatenation type");
        return 외부참조(10, "java/lang/StringBuilder", "append", irú_iye == 1 ? "(I)Ljava/lang/StringBuilder;"
            : irú_iye == 2 ? "(Z)Ljava/lang/StringBuilder;" : irú_iye == 5 ? "(C)Ljava/lang/StringBuilder;" : "(Ljava/lang/String;)Ljava/lang/StringBuilder;");
    }
    static void 결합(int 경계, int 앞형, int Padà_sẹ́yìn_iye_irú) {
        // 이미 계산한 왼쪽 값을 먼저 append하도록 오른쪽 코드 앞에 생성 코드를 삽입한다.
        // 오른쪽 ìsọ̀rọ̀sí_iye 내부의 ọ̀gbà_iye ẹ̀ka 거리는 전체 구간을 함께 옮기므로 유지된다.
        int 끝 = 코드크기;
        Àṣẹ(187, Ìtọ́ka(7, Ọ̀rọ̀_aláìṣeéyípadà("java/lang/StringBuilder"), 0)); 내보내기(89);
        Àṣẹ(183, 외부참조(10, "java/lang/StringBuilder", "<init>", "()V")); 내보내기(95); Àṣẹ(182, 붙임참조(앞형));
        if (àṣìṣe) return;
        int gígùn_iye = 코드크기 - 끝;
        for (int 수 = 0; 수 < gígùn_iye; 수++) 삽입코드[수] = 코드[끝 + 수];
        for (int 수 = 끝 - 1; 수 >= 경계; 수--) 코드[수 + gígùn_iye] = 코드[수];
        for (int 수 = 0; 수 < gígùn_iye; 수++) 코드[경계 + 수] = 삽입코드[수];
        Àṣẹ(182, 붙임참조(Padà_sẹ́yìn_iye_irú)); Àṣẹ(182, 외부참조(10, "java/lang/StringBuilder", "toString", "()Ljava/lang/String;"));
    }
    static int 비교식() {
        int irú_iye = 합식();
        while (!àṣìṣe && (종류() == '<' || 종류() == '>' || 종류() == 302 || 종류() == 303)) {
            int pípàrokò_iye = 종류(); 위치++; ridájú_irú(irú_iye, 1); ridájú_irú(합식(), 1);
            비교값(pípàrokò_iye == '<' ? 161 : pípàrokò_iye == '>' ? 163 : pípàrokò_iye == 302 ? 164 : 162); irú_iye = 2;
        }
        return irú_iye;
    }
    static int 동등식() {
        int irú_iye = 비교식();
        while (!àṣìṣe && (종류() == 300 || 종류() == 301)) {
            int pípàrokò_iye = 종류(); 위치++; int Padà_sẹ́yìn_iye_irú = 비교식();
            if (irú_iye == 0 || Padà_sẹ́yìn_iye_irú == 0) ìkùnà_iye("void expression");
            if (!(nọ́ńbà_odindi_irú(irú_iye) && nọ́ńbà_odindi_irú(Padà_sẹ́yìn_iye_irú))) ridájú_irú(Padà_sẹ́yìn_iye_irú, irú_iye);
            비교값((irú_iye <= 2 || irú_iye == 5 ? 159 : 165) + (pípàrokò_iye == 301 ? 1 : 0)); irú_iye = 2;
        }
        return irú_iye;
    }
    static int 논리곱() {
        int irú_iye = 동등식();
        while (!àṣìṣe && 받기(304)) {
            ridájú_irú(irú_iye, 2); int 가 = ẹ̀ka(153); ridájú_irú(동등식(), 2); int 나 = ẹ̀ka(153);
            내보내기(4); int 끝 = ẹ̀ka(167); ṣàsopọ̀_iye_ff3cc3dc(가, 코드크기); ṣàsopọ̀_iye_ff3cc3dc(나, 코드크기); 내보내기(3); ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기); irú_iye = 2;
        }
        return irú_iye;
    }
    static int ìsọ̀rọ̀sí_iye() {
        int irú_iye = 논리곱();
        while (!àṣìṣe && 받기(305)) {
            ridájú_irú(irú_iye, 2); int 가 = ẹ̀ka(154); ridájú_irú(논리곱(), 2); int 나 = ẹ̀ka(154);
            내보내기(3); int 끝 = ẹ̀ka(167); ṣàsopọ̀_iye_ff3cc3dc(가, 코드크기); ṣàsopọ̀_iye_ff3cc3dc(나, 코드크기); 내보내기(4); ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기); irú_iye = 2;
        }
        return irú_iye;
    }
    static void aṣetiléwá_iye(boolean 선언허용) {
        if (Ọ̀rọ̀_iye(위치, "int") || Ọ̀rọ̀_iye(위치, "boolean") || Ọ̀rọ̀_iye(위치, "String") || Ọ̀rọ̀_iye(위치, "char")
            || Ọ̀rọ̀_iye(위치, "FileInputStream") || Ọ̀rọ̀_iye(위치, "FileOutputStream")) {
            if (!선언허용) ìkùnà_iye("declaration not allowed here");
            int irú_iye = ìgúnrégé_iye(), Orúkọ = Àfidámọ̀_iye(); 요구('='); ridájú_irú(ìsọ̀rọ̀sí_iye(), irú_iye);
            kọ_agbègbè(ròmọ́_agbègbè(Orúkọ, irú_iye)); return;
        }
        int Orúkọ = Àfidámọ̀_iye(), agbègbè_sàkání = wá_agbègbè(Orúkọ);
        if (받기('=')) { ridájú_irú(ìsọ̀rọ̀sí_iye(), agbègbè_irú[agbègbè_sàkání]); kọ_agbègbè(agbègbè_sàkání); }
        else if (종류() >= 308 && 종류() <= 312) {
            int pípàrokò_iye = 종류(); 위치++; 지역읽기(agbègbè_sàkání); int 경계 = 코드크기, Padà_sẹ́yìn_iye_irú = ìsọ̀rọ̀sí_iye();
            if (pípàrokò_iye == 308 && agbègbè_irú[agbègbè_sàkání] == 3) 결합(경계, 3, Padà_sẹ́yìn_iye_irú);
            else {
                ridájú_irú(agbègbè_irú[agbègbè_sàkání], 1); ridájú_irú(Padà_sẹ́yìn_iye_irú, 1);
                내보내기(pípàrokò_iye == 308 ? 96 : pípàrokò_iye == 309 ? 100 : pípàrokò_iye == 310 ? 104 : pípàrokò_iye == 311 ? 108 : 112);
                if (agbègbè_irú[agbègbè_sàkání] == 5) 내보내기(146);
            }
            kọ_agbègbè(agbègbè_sàkání);
        }
        else if (종류() == 306 || 종류() == 307) {
            ridájú_irú(agbègbè_irú[agbègbè_sàkání], 1); 내보내기(132); 내보내기(agbègbè_sàkání); 내보내기(종류() == 306 ? 1 : 255); 위치++;
            if (agbègbè_irú[agbègbè_sàkání] == 5) { 지역읽기(agbègbè_sàkání); 내보내기(146); kọ_agbègbè(agbègbè_sàkání); }
        } else ìkùnà_iye("assignment or postfix increment required");
    }
    static void 화면출력() {
        말요구("System"); 요구('.'); 말요구("out"); 요구('.');
        boolean 줄바꿈 = 말받기("println"); if (!줄바꿈) 말요구("print"); 요구('(');
        Àṣẹ(178, 외부참조(9, "java/lang/System", "out", "Ljava/io/PrintStream;"));
        boolean òfìfo_ágúmẹ́ntì = 종류() == ')';
        int irú_iye = òfìfo_ágúmẹ́ntì ? 0 : ìsọ̀rọ̀sí_iye(); 요구(')'); 요구(';');
        String 서술 = irú_iye == 0 ? "()V" : irú_iye == 1 ? "(I)V" : irú_iye == 2 ? "(Z)V" : irú_iye == 5 ? "(C)V" : "(Ljava/lang/String;)V";
        if (irú_iye == 4 || irú_iye >= 6 || irú_iye == 0 && (!줄바꿈 || !òfìfo_ágúmẹ́ntì)) ìkùnà_iye("unsupported print argument");
        Àṣẹ(182, 외부참조(10, "java/io/PrintStream", 줄바꿈 ? "println" : "print", 서술));
    }
    static boolean àlàyé_iye() {
        if (àṣìṣe) return false;
        if (깊이 > 32) { ìkùnà_iye("statement nesting too deep"); return false; }
        if (받기('{')) {
            깊이++; boolean 반환 = false;
            while (!àṣìṣe && 종류() != '}') { if (반환) ìkùnà_iye("unreachable statement"); 반환 = àlàyé_iye(); }
            요구('}'); for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return 반환;
        }
        if (받기(';')) return false;
        if (말받기("return")) {
            int irú_iye = 종류() == ';' ? 0 : ìsọ̀rọ̀sí_iye(); ridájú_irú(irú_iye, 함수반환[현재함수]); 요구(';');
            내보내기(irú_iye == 0 ? 177 : irú_iye <= 2 || irú_iye == 5 ? 172 : 176); return true;
        }
        if (말받기("if")) {
            요구('('); ridájú_irú(ìsọ̀rọ̀sí_iye(), 2); 요구(')'); int 거짓 = ẹ̀ka(153);
            깊이++; boolean 가 = ìdarí_àlàyé(); 깊이--;
            if (말받기("else")) { int 끝 = ẹ̀ka(167); ṣàsopọ̀_iye_ff3cc3dc(거짓, 코드크기); 깊이++; boolean 나 = ìdarí_àlàyé(); 깊이--; ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기); return 가 && 나; }
            ṣàsopọ̀_iye_ff3cc3dc(거짓, 코드크기); return false;
        }
        if (말받기("while")) {
            int Rọ́ọ̀nù = 코드크기; 요구('('); ridájú_irú(ìsọ̀rọ̀sí_iye(), 2); 요구(')'); int 끝 = ẹ̀ka(153);
            깊이++; ìdarí_àlàyé(); 깊이--; ṣàsopọ̀_iye_ff3cc3dc(ẹ̀ka(167), Rọ́ọ̀nù); ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기); return false;
        }
        if (말받기("for")) {
            깊이++; 요구('('); if (종류() != ';') aṣetiléwá_iye(true); 요구(';');
            int kání = 코드크기; if (종류() == ';') 내보내기(4); else ridájú_irú(ìsọ̀rọ̀sí_iye(), 2); 요구(';');
            int 끝 = ẹ̀ka(153), kókó_ọ̀rọ̀_ìkọ = ẹ̀ka(167), sọdọ̀tun = 코드크기;
            if (종류() != ')') aṣetiléwá_iye(false); 요구(')'); ṣàsopọ̀_iye_ff3cc3dc(ẹ̀ka(167), kání); ṣàsopọ̀_iye_ff3cc3dc(kókó_ọ̀rọ̀_ìkọ, 코드크기);
            ìdarí_àlàyé(); ṣàsopọ̀_iye_ff3cc3dc(ẹ̀ka(167), sọdọ̀tun); ṣàsopọ̀_iye_ff3cc3dc(끝, 코드크기);
            for (int 수 = 0; 수 < 지역수; 수++) if (지역깊이[수] == 깊이) 지역깊이[수] = -1;
            깊이--; return false;
        }
        if (Ọ̀rọ̀_iye(위치, "System")) { 화면출력(); return false; }
        if (종류() == 256 && 위치 + 1 < 토큰수 && (토큰종류[위치 + 1] == '(' || 토큰종류[위치 + 1] == '.')) {
            int irú_iye = ìsọ̀rọ̀sí_iye(); if (irú_iye != 0) 내보내기(87); 요구(';'); return false;
        }
        aṣetiléwá_iye(true); 요구(';'); return false;
    }
    static boolean ìdarí_àlàyé() {
        if (Ọ̀rọ̀_iye(위치, "int") || Ọ̀rọ̀_iye(위치, "boolean") || Ọ̀rọ̀_iye(위치, "char") || Ọ̀rọ̀_iye(위치, "String")
            || Ọ̀rọ̀_iye(위치, "FileInputStream") || Ọ̀rọ̀_iye(위치, "FileOutputStream")) ìkùnà_iye("local declaration requires braces");
        return àlàyé_iye();
    }
    static void 출바(int iye) { if (출력크기 == 출력.length) ìkùnà_iye("class file too large"); else 출력[출력크기++] = iye & 255; }
    static void 출짧(int iye) { 출바(iye >> 8); 출바(iye); }
    static void 출정(int iye) { 출짧(iye >>> 16); 출짧(iye); }
    static void kọ_ọ̀wọ́() {
        출정(0xcafebabe); 출짧(0); 출짧(49); 출짧(상수수);
        for (int 수 = 0; 수 < aláìṣeéyípadà_ìwọn; 수++) 출바(aláìṣeéyípadà_iye[수]);
        출짧(0x21); 출짧(ọ̀wọ́_aláìṣeéyípadà); 출짧(부모상수); 출짧(0); 출짧(0); 출짧(함수수);
        for (int 수 = 0; 수 < 함수수; 수++) {
            출짧(ìlànà_wáyè_sí[수]); 출짧(ìlànà_orúkọ_aláìṣeéyípadà[수]); 출짧(함수서술[수]); 출짧(1); 출짧(코드상수);
            출정(12 + ìlànà_gígùn[수]); 출짧(128); 출짧(함수지역[수]); 출정(ìlànà_gígùn[수]);
            for (int ààyè_ìfàyọkàsí_ìgbéwọlé = 0; ààyè_ìfàyọkàsí_ìgbéwọlé < ìlànà_gígùn[수]; ààyè_ìfàyọkàsí_ìgbéwọlé++) 출바(코드[함수코드[수] + ààyè_ìfàyọkàsí_ìgbéwọlé]);
            출짧(0); 출짧(0);
        }
        출짧(0);
    }
    public static int Rọ́ọ̀nù() {
        if (aṣàmúlò.인수개수() == 1 && 자바도구.같음(aṣàmúlò.인수(0), "-version")) {
            aṣàmúlò.Kọ("jkoros javac 0.1 (subset compiler; not OpenJDK)\n"); return 0;
        }
        if (aṣàmúlò.인수개수() != 1) { aṣàmúlò.Kọ("Usage: javac FILE.java\n"); return 2; }
        int orúkọ_ìwọn = 자바도구.Orúkọ(fáìlì_orúkọ_SMS, aṣàmúlò.인수(0));
        if (orúkọ_ìwọn < 6 || orúkọ_ìwọn > 62 || fáìlì_orúkọ_SMS[orúkọ_ìwọn - 5] != '.' || fáìlì_orúkọ_SMS[orúkọ_ìwọn - 4] != 'j'
            || fáìlì_orúkọ_SMS[orúkọ_ìwọn - 3] != 'a' || fáìlì_orúkọ_SMS[orúkọ_ìwọn - 2] != 'v' || fáìlì_orúkọ_SMS[orúkọ_ìwọn - 1] != 'a') {
            aṣàmúlò.Kọ("javac error: expected FILE.java (name up to 62 characters)\n"); return 2;
        }
        orísun_ìwọn = aṣàmúlò.파일읽기(fáìlì_orúkọ_SMS, orísun);
        if (orísun_ìwọn < 0) { aṣàmúlò.Kọ("javac: cannot read source: "); 자바도구.수쓰기(orísun_ìwọn); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); return 1; }
        orísun_ìwọn = 자바도구.원문해독(orísun, orísun_ìwọn);
        if (orísun_ìwọn < 0) { aṣàmúlò.Kọ("javac error: invalid UTF-8 source\n"); return 1; }
        gé_kúrò_iye(); if (!àṣìṣe) 선언읽기();
        if (!àṣìṣe) {
            if (kóòdù_káàdì_àsansílẹ̀_gígùn[ọ̀wọ́_kóòdù_káàdì_àsansílẹ̀] != orúkọ_ìwọn - 5) ìkùnà_iye("class name must match file name");
            for (int 수 = 0; 수 < orúkọ_ìwọn - 5; 수++) if (orísun[토큰위치[ọ̀wọ́_kóòdù_káàdì_àsansílẹ̀] + 수] != fáìlì_orúkọ_SMS[수]) ìkùnà_iye("class name must match file name");
        }
        for (현재함수 = 0; 현재함수 < 함수수 && !àṣìṣe; 현재함수++) {
            위치 = 함수본문[현재함수]; 함수코드[현재함수] = 코드크기; 지역수 = 0; 깊이 = 0;
            for (int 수 = 0; 수 < 함수인수수[현재함수]; 수++) ròmọ́_agbègbè(ìlànà_ágúmẹ́ntì_orúkọ[현재함수 * 16 + 수], ìlànà_ágúmẹ́ntì_irú[현재함수 * 16 + 수]);
            boolean 반환 = àlàyé_iye();
            if (!반환 && 함수반환[현재함수] != 0) ìkùnà_iye("missing return");
            // ẹ̀ka 뒤의 합류 지점은 반드시 gangan_détà 명령이어야 한다 (버전 49 검증기).
            if (함수반환[현재함수] == 0) 내보내기(177);
            else { boolean nọ́ńbà_odindi = 함수반환[현재함수] <= 2 || 함수반환[현재함수] == 5; 내보내기(nọ́ńbà_odindi ? 3 : 1); 내보내기(nọ́ńbà_odindi ? 172 : 176); }
            if (위치 != ìlànà_parí[현재함수]) ìkùnà_iye("invalid method body");
            함수지역[현재함수] = 지역수; ìlànà_gígùn[현재함수] = 코드크기 - 함수코드[현재함수];
        }
        if (àṣìṣe) return 1;
        kọ_ọ̀wọ́(); if (àṣìṣe) return 1;
        fáìlì_orúkọ_SMS[orúkọ_ìwọn - 4] = 'c'; fáìlì_orúkọ_SMS[orúkọ_ìwọn - 3] = 'l'; fáìlì_orúkọ_SMS[orúkọ_ìwọn - 2] = 'a';
        fáìlì_orúkọ_SMS[orúkọ_ìwọn - 1] = 's'; fáìlì_orúkọ_SMS[orúkọ_ìwọn] = 's'; fáìlì_orúkọ_SMS[orúkọ_ìwọn + 1] = 0;
        int 결과 = aṣàmúlò.kọ_fáìlì(fáìlì_orúkọ_SMS, 출력, 출력크기);
        if (결과 < 0) { aṣàmúlò.Kọ("javac: cannot save class: "); 자바도구.수쓰기(결과); aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(10); return 1; }
        aṣàmúlò.Kọ("Compiled: "); for (int 수 = 0; fáìlì_orúkọ_SMS[수] != 0; 수++) aṣàmúlò.kọ_ẹyọ_ọ̀rọ̀_iye(fáìlì_orúkọ_SMS[수]);
        aṣàmúlò.Kọ(" (JVM class version 49)\n"); return 0;
    }
}
