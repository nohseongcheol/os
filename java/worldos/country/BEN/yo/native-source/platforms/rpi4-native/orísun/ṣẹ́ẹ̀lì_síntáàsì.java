// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 ìjọṣepọ̀ ṣẹ́ẹ̀lì 문법. 파이프는 순차 ṣiṣẹ́_àṣẹ, 환경은 같은 셸에서 공유한다. */
public final class ṣẹ́ẹ̀lì_síntáàsì {
    static int[] orísun = new int[4 * 4096], 종류 = new int[4 * 128], Rọ́ọ̀nù = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], iye_gígùn = new int[16];
    static int[] ìlànà_ìṣe_léréfèé_iye = new int[4 * 16384];
    static int ipò_iye, 깊이, 쓴수;
    static boolean 연결중, ìlànà_ìṣe_léréfèé_parí, Àfikún_àṣìṣe;
    static boolean orúkọ_ẹyọ_ọ̀rọ̀(int kóòdù_ẹyọ_ọ̀rọ̀) { return kóòdù_ẹyọ_ọ̀rọ̀ >= 'a' && kóòdù_ẹyọ_ọ̀rọ̀ <= 'z' || kóòdù_ẹyọ_ọ̀rọ̀ >= 'A' && kóòdù_ẹyọ_ọ̀rọ̀ <= 'Z' || kóòdù_ẹyọ_ọ̀rọ̀ == '_' || kóòdù_ẹyọ_ọ̀rọ̀ >= 128; }
    static boolean 이름뒤(int kóòdù_ẹyọ_ọ̀rọ̀) { return orúkọ_ẹyọ_ọ̀rọ̀(kóòdù_ẹyọ_ọ̀rọ̀) || kóòdù_ẹyọ_ọ̀rọ̀ >= '0' && kóòdù_ẹyọ_ọ̀rọ̀ <= '9'; }
    static void àṣìṣe(String SMS) { 보드.입출력전환(0); 단말.Kọ("Àṣẹ ìpínsíwẹ́wẹ́_iye: "); 단말.Kọ(SMS); 단말.문자(10); ipò_iye = 2; }
    static int Kàá(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, ẹyọ_ọ̀rọ̀_tódáyàtọ̀ = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (orísun[기준자리 + 현재자리] == 32 || orísun[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || orísun[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { àṣìṣe("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, kóòdù_ẹyọ_ọ̀rọ̀ = orísun[기준자리 + 현재자리], 자료종류 = 0;
            if (kóòdù_ẹyọ_ọ̀rọ̀ == ';') { 자료종류 = 1; 현재자리++; }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ == '&') { if (현재자리 + 1 >= 항목수 || orísun[기준자리 + 현재자리 + 1] != '&') { àṣìṣe("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && orísun[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && orísun[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (kóòdù_ẹyọ_ọ̀rọ̀ == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    kóòdù_ẹyọ_ọ̀rọ̀ = orísun[기준자리 + 현재자리];
                    if (kóòdù_ẹyọ_ọ̀rọ̀ == '`' && 따옴표 != 39 || kóòdù_ẹyọ_ọ̀rọ̀ == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && orísun[기준자리 + 현재자리 + 1] == '(') { àṣìṣe("Àṣẹ 결과 치환은 지원하지 않습니다"); return -1; }
                    if (kóòdù_ẹyọ_ọ̀rọ̀ == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { àṣìṣe("ìlà 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (kóòdù_ẹyọ_ọ̀rọ̀ == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (kóòdù_ẹyọ_ọ̀rọ̀ == 39 || kóòdù_ẹyọ_ọ̀rọ̀ == 34)) { 따옴표 = kóòdù_ẹyọ_ọ̀rọ̀; 현재자리++; continue; }
                    if (따옴표 == 0 && (kóòdù_ẹyọ_ọ̀rọ̀ == 32 || kóòdù_ẹyọ_ọ̀rọ̀ == 9 || kóòdù_ẹyọ_ọ̀rọ̀ == ';' || kóòdù_ẹyọ_ọ̀rọ̀ == '&' || kóòdù_ẹyọ_ọ̀rọ̀ == '|' || kóòdù_ẹyọ_ọ̀rọ̀ == '<' || kóòdù_ẹyọ_ọ̀rọ̀ == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { àṣìṣe("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (orísun[기준자리 + 현재자리] == '>' || orísun[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 시작자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 현재자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (orísun[기준자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú] < '0' || orísun[기준자리 + ṣetúnṣe_wá_atọ̀ka_àkóónú] > '9') 수치 = false;
                    if (수치) { àṣìṣe("번호를 지정한 Fáìlì 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + 총수] = 자료종류; Rọ́ọ̀nù[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + 총수] = 시작자리; 끝[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 총수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            int 임시값 = 종류[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + ṣetúnṣe_wá_atọ̀ka_àkóónú];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++ṣetúnṣe_wá_atọ̀ka_àkóónú == 총수 || 종류[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + ṣetúnṣe_wá_atọ̀ka_àkóónú] != 0) { àṣìṣe("I_O 전환에 Fáìlì 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || ṣetúnṣe_wá_atọ̀ka_àkóónú == 총수 - 1 && 임시값 != 1) { àṣìṣe("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[ẹyọ_ọ̀rọ̀_tódáyàtọ̀ + 총수 - 1] != 1) { àṣìṣe("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] détà_ÀRÉÈ, int agbègbè_bẹ̀rẹ̀, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (détà_ÀRÉÈ[agbègbè_bẹ̀rẹ̀ + ṣetúnṣe_wá_atọ̀ka_àkóónú] != 문자위치.charAt(ṣetúnṣe_wá_atọ̀ka_àkóónú)) return false; return true;
    }
    static void 넣기(int báìtì_détà) {
        if (쓴수 >= 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye.length) { if (!Àfikún_àṣìṣe) àṣìṣe("변수를 펼친 명령이 너무 깁니다"); Àfikún_àṣìṣe = true; return; }
        명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[쓴수++] = báìtì_détà;
    }
    static void 변수(int[] détà_ÀRÉÈ, int 시작자리, int 항목수) {
        if (구간말(détà_ÀRÉÈ, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < ibi_ìpamọ́_Àwọn_fáìlì.현재길이; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 넣기(ibi_ìpamọ́_Àwọn_fáìlì.현재[ṣetúnṣe_wá_atọ̀ka_àkóónú]); return; }
        if (구간말(détà_ÀRÉÈ, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(détà_ÀRÉÈ, 시작자리, 항목수, "?")) {
            int détà_iye = ipò_iye, díjììtì = 100; boolean 시작여부 = false;
            while (díjììtì > 0) { int 뒷값 = détà_iye / díjììtì; if (뒷값 != 0 || 시작여부 || díjììtì == 1) { 넣기('0' + 뒷값); 시작여부 = true; } détà_iye %= díjììtì; díjììtì /= 10; } return;
        }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[ṣetúnṣe_wá_atọ̀ka_àkóónú * 32 + 안쪽자리] != détà_ÀRÉÈ[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < iye_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú]; 안쪽자리++) 넣기(변수값[ṣetúnṣe_wá_atọ̀ka_àkóónú * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Ọ̀rọ̀_iye(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Rọ́ọ̀nù[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && orísun[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || orísun[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int kóòdù_ẹyọ_ọ̀rọ̀ = orísun[기준자리 + 읽는자리++];
            if (kóòdù_ẹyọ_ọ̀rọ̀ == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (kóòdù_ẹyọ_ọ̀rọ̀ == 39 || kóòdù_ẹyọ_ọ̀rọ̀ == 34)) { 따옴표 = kóòdù_ẹyọ_ọ̀rọ̀; continue; }
            if (kóòdù_ẹyọ_ọ̀rọ̀ == '\\' && 따옴표 != 39) { int 다음자리 = orísun[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (kóòdù_ẹyọ_ọ̀rọ̀ == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = orísun[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && orísun[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(orísun[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || orísun[기준자리 + 읽는자리] != '}')) { àṣìṣe("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(orísun, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(kóòdù_ẹyọ_ọ̀rọ̀);
        }
        return !Àfikún_àṣìṣe;
    }
    static int 환경설정(int ágúmẹ́ntì_wá_atọ̀ka_àkóónú, boolean ṣèmúkúro) {
        int agbègbè_bẹ̀rẹ̀ = 명령해석기.시작점[ágúmẹ́ntì_wá_atọ̀ka_àkóónú], 끝자리 = agbègbè_bẹ̀rẹ̀ + 명령해석기.gígùn_iye[ágúmẹ́ntì_wá_atọ̀ka_àkóónú], 같음자리 = agbègbè_bẹ̀rẹ̀;
        while (같음자리 < 끝자리 && 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - agbègbè_bẹ̀rẹ̀;
        if (항목수 < 1 || 항목수 > 31 || !orúkọ_ẹyọ_ọ̀rọ̀(명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[agbègbè_bẹ̀rẹ̀]) || !ṣèmúkúro && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = agbègbè_bẹ̀rẹ̀; ṣetúnṣe_wá_atọ̀ka_àkóónú < 같음자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (!이름뒤(명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú])) return 2;
        if (구간말(명령해석기.kóòdù_káàdì_àsansílẹ̀_iye, agbègbè_bẹ̀rẹ̀, 항목수, "PWD") || 구간말(명령해석기.kóòdù_káàdì_àsansílẹ̀_iye, agbègbè_bẹ̀rẹ̀, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
            if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] == 0) 빈여부 = ṣetúnṣe_wá_atọ̀ka_àkóónú;
            if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[ṣetúnṣe_wá_atọ̀ka_àkóónú * 32 + 안쪽자리] != 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[agbègbè_bẹ̀rẹ̀ + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = ṣetúnṣe_wá_atọ̀ka_àkóónú;
        }
        if (ṣèmúkúro) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; iye_gígùn[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 변수이름[찾은여부 * 32 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[agbègbè_bẹ̀rẹ̀ + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 같음자리 + 1; ṣetúnṣe_wá_atọ̀ka_àkóónú < 끝자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) 변수값[찾은여부 * 256 + ṣetúnṣe_wá_atọ̀ka_àkóónú - 같음자리 - 1] = 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[ṣetúnṣe_wá_atọ̀ka_àkóónú];
        return 0;
    }
    static void 환경보기() {
        단말.Kọ("HOME=/\nPWD="); ibi_ìpamọ́_Àwọn_fáìlì.현재쓰기(); 단말.문자(10);
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 16; ṣetúnṣe_wá_atọ̀ka_àkóónú++) if (이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[ṣetúnṣe_wá_atọ̀ka_àkóónú]; 안쪽자리++) 보드.직렬쓰기(변수이름[ṣetúnṣe_wá_atọ̀ka_àkóónú * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < iye_gígùn[ṣetúnṣe_wá_atọ̀ka_àkóónú]; 안쪽자리++) 보드.직렬쓰기(변수값[ṣetúnṣe_wá_atọ̀ka_àkóónú * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void ṣiṣẹ́_àṣẹ(int[] détà_ÀRÉÈ, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { àṣìṣe("Àṣẹ 파일의 중첩 또는 ìlà gígùn_iye 제한을 넘었습니다"); return; }
        for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 0; ṣetúnṣe_wá_atọ̀ka_àkóónú < 항목수; ṣetúnṣe_wá_atọ̀ka_àkóónú++) orísun[중첩깊이 * 4096 + ṣetúnṣe_wá_atọ̀ka_àkóónú] = détà_ÀRÉÈ[시작변위 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
        int 총수 = Kàá(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int Àjọṣe_parí = 읽는자리;
            while (Àjọṣe_parí < 총수 && (종류[중첩깊이 * 128 + Àjọṣe_parí] == 0 || 종류[중첩깊이 * 128 + Àjọṣe_parí] >= 4)) Àjọṣe_parí++;
            boolean ṣiṣẹ́ = 조건성립 == 1 || 조건성립 == 2 && ipò_iye == 0 || 조건성립 == 3 && ipò_iye != 0;
            if (ṣiṣẹ́) {
                boolean 이전자리 = false;
                while (읽는자리 < Àjọṣe_parí) {
                    int 다음자리 = 읽는자리; while (다음자리 < Àjọṣe_parí && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean SOMỌ́_Stream = 다음자리 < Àjọṣe_parí; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; Àfikún_àṣìṣe = false;
                    for (int ṣetúnṣe_wá_atọ̀ka_àkóónú = 읽는자리; ṣetúnṣe_wá_atọ̀ka_àkóónú < 다음자리; ṣetúnṣe_wá_atọ̀ka_àkóónú++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + ṣetúnṣe_wá_atọ̀ka_àkóónú];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { àṣìṣe("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++ṣetúnṣe_wá_atọ̀ka_àkóónú; } else { if (출력쪽 >= 0) { àṣìṣe("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++ṣetúnṣe_wá_atọ̀ka_àkóónú; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { àṣìṣe("인수가 너무 많습니다"); return; }
                        int ágúmẹ́ntì_wá_atọ̀ka_àkóónú = 명령해석기.토큰수++; 명령해석기.시작점[ágúmẹ́ntì_wá_atọ̀ka_àkóónú] = 쓴수;
                        if (!Ọ̀rọ̀_iye(ṣetúnṣe_wá_atọ̀ka_àkóónú, 중첩깊이)) return;
                        명령해석기.gígùn_iye[ágúmẹ́ntì_wá_atọ̀ka_àkóónú] = 쓴수 - 명령해석기.시작점[ágúmẹ́ntì_wá_atọ̀ka_àkóónú];
                    }
                    연결중 = 이전자리 || SOMỌ́_Stream || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { àṣìṣe("ìjọṣepọ̀ 명령과 Àṣẹ 파일은 I_O 전환이나 Stream_iye 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Rọ́ọ̀nù(이전자리, SOMỌ́_Stream);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Ọ̀rọ̀_iye(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_bẹ̀rẹ̀(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.ọ̀nà_báìtì(안쪽자리 - 시작자리, 명령해석기.kóòdù_káàdì_àsansílẹ̀_iye[안쪽자리]);
                        if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.àṣìṣe(처리값); ipò_iye = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.fáìlì_ìgbéjáde = 처리값;
                    }
                    셸입출력.Fún_Lááyè_ìjọṣepọ̀ = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Àṣẹ();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, Stream_àṣìṣe = 셸입출력.ìkùnà_iye;
                    셸입출력.끝(); 연결중 = false;
                    ipò_iye = Stream_àṣìṣe < 0 ? 1 : 반환값;
                    if (Stream_àṣìṣe < 0) { 명령해석기.àṣìṣe(Stream_àṣìṣe); return; }
                    if (ìlànà_ìṣe_léréfèé_parí || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (Àjọṣe_parí < 총수) 조건성립 = 종류[중첩깊이 * 128 + Àjọṣe_parí];
            읽는자리 = Àjọṣe_parí + 1;
        }
    }
    static void ṣiṣẹ́_fáìlì() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Kọ("사용법: sh Fáìlì (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.ọ̀nà(1); if (처리값 >= 0) 처리값 = ibi_ìpamọ́_Àwọn_fáìlì.Ṣi(0);
        if (처리값 < 0) { 명령해석기.àṣìṣe(처리값); return; }
        int 항목수 = 0, báìtì_détà;
        while ((báìtì_détà = ibi_ìpamọ́_Àwọn_fáìlì.Kàá(처리값)) != 256 && báìtì_détà >= 0 && 항목수 < 16384) ìlànà_ìṣe_léréfèé_iye[중첩깊이 * 16384 + 항목수++] = báìtì_détà;
        ibi_ìpamọ́_Àwọn_fáìlì.Ti(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !ìlànà_ìṣe_léréfèé_parí;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && ìlànà_ìṣe_léréfèé_iye[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && ìlànà_ìṣe_léréfèé_iye[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            ṣiṣẹ́_àṣẹ(ìlànà_ìṣe_léréfèé_iye, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = ipò_iye; ìlànà_ìṣe_léréfèé_parí = false; 깊이 = 중첩깊이 - 1;
    }
}
