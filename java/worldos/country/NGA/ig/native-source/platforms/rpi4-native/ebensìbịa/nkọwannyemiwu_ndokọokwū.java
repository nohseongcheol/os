// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 제한된 kèmmekọrịta nkọwannyemiwu 문법. 파이프는 순차 mee_nnyemiwu, 환경은 같은 셸에서 공유한다. */
public final class nkọwannyemiwu_ndokọokwū {
    static int[] ebensìbịa = new int[4 * 4096], 종류 = new int[4 * 128], Bido = new int[4 * 128], 끝 = new int[4 * 128];
    static int[] 변수이름 = new int[16 * 32], 변수값 = new int[16 * 256], 이름길이 = new int[16], valuu_ogologo = new int[16];
    static int[] Èdèrède_ntụziaka_valuu = new int[4 * 16384];
    static int ọnọdụ_valuu, 깊이, 쓴수;
    static boolean 연결중, Èdèrède_ntụziaka_mèdebe, mgbatị_mmejọ;
    static boolean akara_ahà_mkpụrụedemede(int koòdù_nkeakàrà) { return koòdù_nkeakàrà >= 'a' && koòdù_nkeakàrà <= 'z' || koòdù_nkeakàrà >= 'A' && koòdù_nkeakàrà <= 'Z' || koòdù_nkeakàrà == '_' || koòdù_nkeakàrà >= 128; }
    static boolean 이름뒤(int koòdù_nkeakàrà) { return akara_ahà_mkpụrụedemede(koòdù_nkeakàrà) || koòdù_nkeakàrà >= '0' && koòdù_nkeakàrà <= '9'; }
    static void mmejọ(String SMS) { 보드.입출력전환(0); 단말.Chekwaa_ozi("Ntiiwu kerìsịa_valuu: "); 단말.Chekwaa_ozi(SMS); 단말.문자(10); ọnọdụ_valuu = 2; }
    static int Wepụta_ọzi(int 항목수, int 중첩깊이) {
        int 현재자리 = 0, 총수 = 0, 기준자리 = 중첩깊이 * 4096, mkpụrụedemede_pụrụiche = 중첩깊이 * 128;
        while (현재자리 < 항목수) {
            while (현재자리 < 항목수 && (ebensìbịa[기준자리 + 현재자리] == 32 || ebensìbịa[기준자리 + 현재자리] == 9)) 현재자리++;
            if (현재자리 == 항목수 || ebensìbịa[기준자리 + 현재자리] == '#') break;
            if (총수 == 128) { mmejọ("낱말이 너무 많습니다"); return -1; }
            int 시작자리 = 현재자리, koòdù_nkeakàrà = ebensìbịa[기준자리 + 현재자리], 자료종류 = 0;
            if (koòdù_nkeakàrà == ';') { 자료종류 = 1; 현재자리++; }
            else if (koòdù_nkeakàrà == '&') { if (현재자리 + 1 >= 항목수 || ebensìbịa[기준자리 + 현재자리 + 1] != '&') { mmejọ("뒤에서 실행하는 작업은 지원하지 않습니다"); return -1; } 자료종류 = 2; 현재자리 += 2; }
            else if (koòdù_nkeakàrà == '|') { 현재자리++; 자료종류 = 현재자리 < 항목수 && ebensìbịa[기준자리 + 현재자리] == '|' ? 3 : 4; if (자료종류 == 3) 현재자리++; }
            else if (koòdù_nkeakàrà == '>') { 현재자리++; 자료종류 = 현재자리 < 항목수 && ebensìbịa[기준자리 + 현재자리] == '>' ? 6 : 5; if (자료종류 == 6) 현재자리++; }
            else if (koòdù_nkeakàrà == '<') { 자료종류 = 7; 현재자리++; }
            else {
                int 따옴표 = 0;
                while (현재자리 < 항목수) {
                    koòdù_nkeakàrà = ebensìbịa[기준자리 + 현재자리];
                    if (koòdù_nkeakàrà == '`' && 따옴표 != 39 || koòdù_nkeakàrà == '$' && 따옴표 != 39 && 현재자리 + 1 < 항목수 && ebensìbịa[기준자리 + 현재자리 + 1] == '(') { mmejọ("Ntiiwu 결과 치환은 지원하지 않습니다"); return -1; }
                    if (koòdù_nkeakàrà == '\\' && 따옴표 != 39) { if (++현재자리 == 항목수) { mmejọ("ahịrī 끝의 역빗금 뒤에 문자가 필요합니다"); return -1; } 현재자리++; continue; }
                    if (koòdù_nkeakàrà == 따옴표) { 따옴표 = 0; 현재자리++; continue; }
                    if (따옴표 == 0 && (koòdù_nkeakàrà == 39 || koòdù_nkeakàrà == 34)) { 따옴표 = koòdù_nkeakàrà; 현재자리++; continue; }
                    if (따옴표 == 0 && (koòdù_nkeakàrà == 32 || koòdù_nkeakàrà == 9 || koòdù_nkeakàrà == ';' || koòdù_nkeakàrà == '&' || koòdù_nkeakàrà == '|' || koòdù_nkeakàrà == '<' || koòdù_nkeakàrà == '>')) break;
                    현재자리++;
                }
                if (따옴표 != 0) { mmejọ("따옴표가 닫히지 않았습니다"); return -1; }
                if (현재자리 < 항목수 && (ebensìbịa[기준자리 + 현재자리] == '>' || ebensìbịa[기준자리 + 현재자리] == '<')) {
                    boolean 수치 = 현재자리 > 시작자리;
                    for (int memmenwè_indèks = 시작자리; memmenwè_indèks < 현재자리; memmenwè_indèks++) if (ebensìbịa[기준자리 + memmenwè_indèks] < '0' || ebensìbịa[기준자리 + memmenwè_indèks] > '9') 수치 = false;
                    if (수치) { mmejọ("번호를 지정한 Faịlụ 서술자 I_O 전환은 지원하지 않습니다"); return -1; }
                }
            }
            종류[mkpụrụedemede_pụrụiche + 총수] = 자료종류; Bido[mkpụrụedemede_pụrụiche + 총수] = 시작자리; 끝[mkpụrụedemede_pụrụiche + 총수] = 현재자리; 총수++;
        }
        boolean 낱말 = false;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 총수; memmenwè_indèks++) {
            int 임시값 = 종류[mkpụrụedemede_pụrụiche + memmenwè_indèks];
            if (임시값 == 0) 낱말 = true;
            else if (임시값 >= 5) { if (++memmenwè_indèks == 총수 || 종류[mkpụrụedemede_pụrụiche + memmenwè_indèks] != 0) { mmejọ("I_O 전환에 Faịlụ 이름이 필요합니다"); return -1; } }
            else { if (!낱말 || memmenwè_indèks == 총수 - 1 && 임시값 != 1) { mmejọ("명령이 빠졌습니다"); return -1; } 낱말 = false; }
        }
        if (총수 > 0 && !낱말 && 종류[mkpụrụedemede_pụrụiche + 총수 - 1] != 1) { mmejọ("명령이 빠졌습니다"); return -1; }
        return 총수;
    }
    static boolean 구간말(int[] datà_MKPOKỌTA, int otù_ebe_Mbido, int 항목수, String 문자위치) {
        if (항목수 != 문자위치.length()) return false; for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) if (datà_MKPOKỌTA[otù_ebe_Mbido + memmenwè_indèks] != 문자위치.charAt(memmenwè_indèks)) return false; return true;
    }
    static void 넣기(int baịtị_datà) {
        if (쓴수 >= 명령해석기.akara_valuu_eb540501.length) { if (!mgbatị_mmejọ) mmejọ("변수를 펼친 명령이 너무 깁니다"); mgbatị_mmejọ = true; return; }
        명령해석기.akara_valuu_eb540501[쓴수++] = baịtị_datà;
    }
    static void 변수(int[] datà_MKPOKỌTA, int 시작자리, int 항목수) {
        if (구간말(datà_MKPOKỌTA, 시작자리, 항목수, "PWD")) { 넣기('/'); for (int memmenwè_indèks = 0; memmenwè_indèks < memọrị_Ndi_ọbọakwụkwọ.현재길이; memmenwè_indèks++) 넣기(memọrị_Ndi_ọbọakwụkwọ.현재[memmenwè_indèks]); return; }
        if (구간말(datà_MKPOKỌTA, 시작자리, 항목수, "HOME")) { 넣기('/'); return; }
        if (구간말(datà_MKPOKỌTA, 시작자리, 항목수, "?")) {
            int datà_valuu = ọnọdụ_valuu, ọbula = 100; boolean 시작여부 = false;
            while (ọbula > 0) { int 뒷값 = datà_valuu / ọbula; if (뒷값 != 0 || 시작여부 || ọbula == 1) { 넣기('0' + 뒷값); 시작여부 = true; } datà_valuu %= ọbula; ọbula /= 10; } return;
        }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) if (이름길이[memmenwè_indèks] == 항목수) {
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[memmenwè_indèks * 32 + 안쪽자리] != datà_MKPOKỌTA[시작자리 + 안쪽자리]) 일치여부 = false;
            if (일치여부) { for (int 안쪽자리 = 0; 안쪽자리 < valuu_ogologo[memmenwè_indèks]; 안쪽자리++) 넣기(변수값[memmenwè_indèks * 256 + 안쪽자리]); return; }
        }
    }
    static boolean Mkpụrụokwu_valuu(int 낱말번호, int 중첩깊이) {
        int 읽는자리 = Bido[중첩깊이 * 128 + 낱말번호], 끝자리 = 끝[중첩깊이 * 128 + 낱말번호], 기준자리 = 중첩깊이 * 4096, 따옴표 = 0;
        if (읽는자리 < 끝자리 && ebensìbịa[기준자리 + 읽는자리] == '~' && (읽는자리 + 1 == 끝자리 || ebensìbịa[기준자리 + 읽는자리 + 1] == '/')) { 넣기('/'); 읽는자리++; }
        while (읽는자리 < 끝자리) {
            int koòdù_nkeakàrà = ebensìbịa[기준자리 + 읽는자리++];
            if (koòdù_nkeakàrà == 따옴표) { 따옴표 = 0; continue; }
            if (따옴표 == 0 && (koòdù_nkeakàrà == 39 || koòdù_nkeakàrà == 34)) { 따옴표 = koòdù_nkeakàrà; continue; }
            if (koòdù_nkeakàrà == '\\' && 따옴표 != 39) { int 다음자리 = ebensìbịa[기준자리 + 읽는자리++]; if (따옴표 == 34 && 다음자리 != '$' && 다음자리 != '"' && 다음자리 != '\\') 넣기('\\'); 넣기(다음자리); continue; }
            if (koòdù_nkeakàrà == '$' && 따옴표 != 39 && 읽는자리 < 끝자리) {
                boolean 중괄호자리 = ebensìbịa[기준자리 + 읽는자리] == '{'; if (중괄호자리) 읽는자리++;
                int 처음자리 = 읽는자리;
                if (읽는자리 < 끝자리 && ebensìbịa[기준자리 + 읽는자리] == '?') 읽는자리++;
                else while (읽는자리 < 끝자리 && 이름뒤(ebensìbịa[기준자리 + 읽는자리])) 읽는자리++;
                if (중괄호자리 && (읽는자리 == 끝자리 || ebensìbịa[기준자리 + 읽는자리] != '}')) { mmejọ("변수의 중괄호가 닫히지 않았습니다"); return false; }
                if (읽는자리 == 처음자리 && !중괄호자리) { 넣기('$'); continue; }
                변수(ebensìbịa, 기준자리 + 처음자리, 읽는자리 - 처음자리); if (중괄호자리) 읽는자리++; continue;
            }
            넣기(koòdù_nkeakàrà);
        }
        return !mgbatị_mmejọ;
    }
    static int 환경설정(int agụment_indèks, boolean wepụ) {
        int otù_ebe_Mbido = 명령해석기.시작점[agụment_indèks], 끝자리 = otù_ebe_Mbido + 명령해석기.ogologo_valuu[agụment_indèks], 같음자리 = otù_ebe_Mbido;
        while (같음자리 < 끝자리 && 명령해석기.akara_valuu_eb540501[같음자리] != '=') 같음자리++;
        int 항목수 = 같음자리 - otù_ebe_Mbido;
        if (항목수 < 1 || 항목수 > 31 || !akara_ahà_mkpụrụedemede(명령해석기.akara_valuu_eb540501[otù_ebe_Mbido]) || !wepụ && 같음자리 == 끝자리 || 끝자리 - 같음자리 - 1 > 255) return 2;
        for (int memmenwè_indèks = otù_ebe_Mbido; memmenwè_indèks < 같음자리; memmenwè_indèks++) if (!이름뒤(명령해석기.akara_valuu_eb540501[memmenwè_indèks])) return 2;
        if (구간말(명령해석기.akara_valuu_eb540501, otù_ebe_Mbido, 항목수, "PWD") || 구간말(명령해석기.akara_valuu_eb540501, otù_ebe_Mbido, 항목수, "HOME")) return 2;
        int 찾은여부 = -1, 빈여부 = -1;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) {
            if (이름길이[memmenwè_indèks] == 0) 빈여부 = memmenwè_indèks;
            if (이름길이[memmenwè_indèks] != 항목수) continue;
            boolean 일치여부 = true; for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) if (변수이름[memmenwè_indèks * 32 + 안쪽자리] != 명령해석기.akara_valuu_eb540501[otù_ebe_Mbido + 안쪽자리]) 일치여부 = false;
            if (일치여부) 찾은여부 = memmenwè_indèks;
        }
        if (wepụ) { if (찾은여부 >= 0) 이름길이[찾은여부] = 0; return 0; }
        if (찾은여부 < 0) 찾은여부 = 빈여부; if (찾은여부 < 0) return 1;
        이름길이[찾은여부] = 항목수; valuu_ogologo[찾은여부] = 끝자리 - 같음자리 - 1;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 변수이름[찾은여부 * 32 + memmenwè_indèks] = 명령해석기.akara_valuu_eb540501[otù_ebe_Mbido + memmenwè_indèks];
        for (int memmenwè_indèks = 같음자리 + 1; memmenwè_indèks < 끝자리; memmenwè_indèks++) 변수값[찾은여부 * 256 + memmenwè_indèks - 같음자리 - 1] = 명령해석기.akara_valuu_eb540501[memmenwè_indèks];
        return 0;
    }
    static void 환경보기() {
        단말.Chekwaa_ozi("HOME=/\nPWD="); memọrị_Ndi_ọbọakwụkwọ.현재쓰기(); 단말.문자(10);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) if (이름길이[memmenwè_indèks] > 0) {
            for (int 안쪽자리 = 0; 안쪽자리 < 이름길이[memmenwè_indèks]; 안쪽자리++) 보드.직렬쓰기(변수이름[memmenwè_indèks * 32 + 안쪽자리]); 단말.문자('=');
            for (int 안쪽자리 = 0; 안쪽자리 < valuu_ogologo[memmenwè_indèks]; 안쪽자리++) 보드.직렬쓰기(변수값[memmenwè_indèks * 256 + 안쪽자리]); 단말.문자(10);
        }
    }
    static void mee_nnyemiwu(int[] datà_MKPOKỌTA, int 시작변위, int 항목수, int 중첩깊이) {
        if (중첩깊이 >= 4 || 항목수 > 4096) { mmejọ("Ntiiwu 파일의 중첩 또는 ahịrī ogologo_valuu 제한을 넘었습니다"); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) ebensìbịa[중첩깊이 * 4096 + memmenwè_indèks] = datà_MKPOKỌTA[시작변위 + memmenwè_indèks];
        int 총수 = Wepụta_ọzi(항목수, 중첩깊이); if (총수 < 0) return;
        int 읽는자리 = 0, 조건성립 = 1;
        while (읽는자리 < 총수) {
            int otu_mèdebe = 읽는자리;
            while (otu_mèdebe < 총수 && (종류[중첩깊이 * 128 + otu_mèdebe] == 0 || 종류[중첩깊이 * 128 + otu_mèdebe] >= 4)) otu_mèdebe++;
            boolean mee = 조건성립 == 1 || 조건성립 == 2 && ọnọdụ_valuu == 0 || 조건성립 == 3 && ọnọdụ_valuu != 0;
            if (mee) {
                boolean 이전자리 = false;
                while (읽는자리 < otu_mèdebe) {
                    int 다음자리 = 읽는자리; while (다음자리 < otu_mèdebe && 종류[중첩깊이 * 128 + 다음자리] != 4) 다음자리++;
                    boolean JIKỌ_agịrị = 다음자리 < otu_mèdebe; int 입력쪽 = -1, 출력쪽 = -1, 출력방식 = 0;
                    명령해석기.토큰수 = 0; 쓴수 = 0; mgbatị_mmejọ = false;
                    for (int memmenwè_indèks = 읽는자리; memmenwè_indèks < 다음자리; memmenwè_indèks++) {
                        int 자료종류 = 종류[중첩깊이 * 128 + memmenwè_indèks];
                        if (자료종류 >= 5) { if (자료종류 == 7) { if (입력쪽 >= 0) { mmejọ("입력 전환이 겹쳤습니다"); return; } 입력쪽 = ++memmenwè_indèks; } else { if (출력쪽 >= 0) { mmejọ("출력 전환이 겹쳤습니다"); return; } 출력쪽 = ++memmenwè_indèks; 출력방식 = 자료종류; } continue; }
                        if (명령해석기.토큰수 == 32) { mmejọ("인수가 너무 많습니다"); return; }
                        int agụment_indèks = 명령해석기.토큰수++; 명령해석기.시작점[agụment_indèks] = 쓴수;
                        if (!Mkpụrụokwu_valuu(memmenwè_indèks, 중첩깊이)) return;
                        명령해석기.ogologo_valuu[agụment_indèks] = 쓴수 - 명령해석기.시작점[agụment_indèks];
                    }
                    연결중 = 이전자리 || JIKỌ_agịrị || 입력쪽 >= 0 || 출력쪽 >= 0;
                    if (연결중 && (명령해석기.같음(0, "vi") || 명령해석기.같음(0, "edit") || 명령해석기.같음(0, "load") || 명령해석기.같음(0, "gui") || 명령해석기.같음(0, "terminal") || 명령해석기.같음(0, "sh") || 명령해석기.같음(0, "source"))) { mmejọ("kèmmekọrịta 명령과 Ntiiwu 파일은 I_O 전환이나 agịrị_valuu 연결에 쓸 수 없습니다"); return; }
                    셸입출력.Bido(이전자리, JIKỌ_agịrị);
                    for (int 입출력바꿈 = 0; 입출력바꿈 < 2; 입출력바꿈++) {
                        int 항목자리 = 입출력바꿈 == 0 ? 입력쪽 : 출력쪽; if (항목자리 < 0) continue;
                        int 시작자리 = 쓴수; if (!Mkpụrụokwu_valuu(항목자리, 중첩깊이)) { 셸입출력.끝(); return; }
                        int 처리값 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(쓴수 - 시작자리);
                        for (int 안쪽자리 = 시작자리; 처리값 >= 0 && 안쪽자리 < 쓴수; 안쪽자리++) 처리값 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(안쪽자리 - 시작자리, 명령해석기.akara_valuu_eb540501[안쪽자리]);
                        if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.Mepee(입출력바꿈 == 0 ? 0 : 출력방식 == 6 ? 1089 : 577);
                        if (처리값 < 0) { 셸입출력.끝(); 명령해석기.mmejọ(처리값); ọnọdụ_valuu = 1; return; }
                        if (입출력바꿈 == 0) 셸입출력.입력파일 = 처리값; else 셸입출력.faịlụ_kènrụpụ = 처리값;
                    }
                    셸입출력.Kwère_kèmmekọrịta = 중첩깊이 == 0 && 읽는자리 == 0 && 다음자리 == 총수;
                    깊이 = 중첩깊이; 명령해석기.결과 = 0; 보드.입출력전환(1);
                    명령해석기.Ntiiwu();
                    보드.터미널(3);
                    int 반환값 = 명령해석기.결과, agịrị_mmejọ = 셸입출력.ọdịdà_valuu;
                    셸입출력.끝(); 연결중 = false;
                    ọnọdụ_valuu = agịrị_mmejọ < 0 ? 1 : 반환값;
                    if (agịrị_mmejọ < 0) { 명령해석기.mmejọ(agịrị_mmejọ); return; }
                    if (Èdèrède_ntụziaka_mèdebe || 반환값 == -1005) return;
                    이전자리 = true; 읽는자리 = 다음자리 + 1;
                }
            }
            if (otu_mèdebe < 총수) 조건성립 = 종류[중첩깊이 * 128 + otu_mèdebe];
            읽는자리 = otu_mèdebe + 1;
        }
    }
    static void mee_ọbọakwụkwọ() {
        if (명령해석기.토큰수 != 2 || 깊이 >= 3) { 명령해석기.결과 = 2; 단말.Chekwaa_ozi("사용법: sh Faịlụ (중첩 깊이 <= 3)\n"); return; }
        int 중첩깊이 = 깊이 + 1, 처리값 = 명령해석기.ụzọ_ozi(1); if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.Mepee(0);
        if (처리값 < 0) { 명령해석기.mmejọ(처리값); return; }
        int 항목수 = 0, baịtị_datà;
        while ((baịtị_datà = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(처리값)) != 256 && baịtị_datà >= 0 && 항목수 < 16384) Èdèrède_ntụziaka_valuu[중첩깊이 * 16384 + 항목수++] = baịtị_datà;
        memọrị_Ndi_ọbọakwụkwọ.Mechie(처리값); 보드.입출력전환(0);
        for (int 읽는자리 = 0; 읽는자리 < 항목수 && !Èdèrède_ntụziaka_mèdebe;) {
            int 끝자리 = 읽는자리; while (끝자리 < 항목수 && Èdèrède_ntụziaka_valuu[중첩깊이 * 16384 + 끝자리] != 10) 끝자리++;
            int 유효길이 = 끝자리 - 읽는자리; if (유효길이 > 0 && Èdèrède_ntụziaka_valuu[중첩깊이 * 16384 + 끝자리 - 1] == 13) 유효길이--;
            mee_nnyemiwu(Èdèrède_ntụziaka_valuu, 중첩깊이 * 16384 + 읽는자리, 유효길이, 중첩깊이); 읽는자리 = 끝자리 + 1;
        }
        명령해석기.결과 = ọnọdụ_valuu; Èdèrède_ntụziaka_mèdebe = false; 깊이 = 중첩깊이 - 1;
    }
}
