// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UART UTF-8 ahịrị_nnyemiwu. 따옴표, Backspace, Ctrl-U, Ctrl-C와 RAM 편집기를 제공한다. */
public final class 명령해석기 {
    static int[] ahịrī = new int[4096], akara_valuu_eb540501 = new int[4096], 시작점 = new int[32], ogologo_valuu = new int[32];
    static int[] 편집내용 = new int[16384], dezìmà_akara_ahà = new int[63];
    static int 토큰수, dezìmà_akara_ahà_ogologo, 결과;
    static boolean 앞줄;
    static void 원바이트(int valuu) { 보드.직렬쓰기(valuu); }
    static int 줄읽기() { return ahịrī_òdezi.Wepụta_ọzi(); }
    static boolean 나누기(int Ụhara) {
        int 위치 = 0, 끝 = 0; 토큰수 = 0;
        while (위치 < Ụhara) {
            while (위치 < Ụhara && (ahịrī[위치] == 32 || ahịrī[위치] == 9)) 위치++;
            if (위치 == Ụhara) break;
            if (토큰수 == 16) { 단말.Chekwaa_ozi("Ntiiwu kerìsịa_valuu: 인수가 너무 많습니다\n"); return false; }
            시작점[토큰수] = 끝; int 인용 = 0;
            while (위치 < Ụhara) {
                int valuu = ahịrī[위치++];
                if (인용 == 0 && (valuu == 32 || valuu == 9)) break;
                if (valuu == 인용) { 인용 = 0; continue; }
                if (인용 == 0 && (valuu == 39 || valuu == 34)) { 인용 = valuu; continue; }
                akara_valuu_eb540501[끝++] = valuu;
            }
            if (인용 != 0) { 단말.Chekwaa_ozi("Ntiiwu kerìsịa_valuu: 따옴표가 닫히지 않았습니다\n"); return false; }
            ogologo_valuu[토큰수] = 끝 - 시작점[토큰수]; 토큰수++;
        }
        return true;
    }
    static boolean 같음(int indèks, String Mkpụrụokwu_SMS) {
        if (indèks >= 토큰수) return false;
        int 자리=0;
        for (int 순번=0; 순번<Mkpụrụokwu_SMS.length(); 순번++) {
            int koòdù_nkeakàrà=Mkpụrụokwu_SMS.charAt(순번);
            if (koòdù_nkeakàrà>=0xd800 && koòdù_nkeakàrà<=0xdbff && 순번+1<Mkpụrụokwu_SMS.length()) koòdù_nkeakàrà=0x10000+((koòdù_nkeakàrà-0xd800)<<10)+Mkpụrụokwu_SMS.charAt(++순번)-0xdc00;
            int 바이트수=koòdù_nkeakàrà<128?1:koòdù_nkeakàrà<2048?2:koòdù_nkeakàrà<65536?3:4;
            for (int NSOTANSO_valuu=바이트수-1; NSOTANSO_valuu>=0; NSOTANSO_valuu--) {
                int valuu=바이트수==1?koòdù_nkeakàrà:NSOTANSO_valuu==바이트수-1?(바이트수==2?0xc0:바이트수==3?0xe0:0xf0)|(koòdù_nkeakàrà>>(6*NSOTANSO_valuu)):0x80|((koòdù_nkeakàrà>>(6*NSOTANSO_valuu))&63);
                if (자리>=ogologo_valuu[indèks] || akara_valuu_eb540501[시작점[indèks]+자리++]!=valuu) return false;
            }
        }
        return 자리==ogologo_valuu[indèks];
    }
    static int ụzọ_ozi(int indèks) {
        if (indèks >= 토큰수) return -22;
        int 결과 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(ogologo_valuu[indèks]); if (결과 < 0) return 결과;
        for (int memmenwè_indèks = 0; memmenwè_indèks < ogologo_valuu[indèks]; memmenwè_indèks++) {
            결과 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(memmenwè_indèks, akara_valuu_eb540501[시작점[indèks] + memmenwè_indèks]); if (결과 < 0) return 결과;
        }
        return 0;
    }
    static void mmejọ(int indèks) { 결과 = 1; 단말.Chekwaa_ozi("mmejọ "); 단말.수(indèks); 단말.문자(10); }
    static void lèe_valuu() {
        if (토큰수 != 2) { 단말.Chekwaa_ozi("사용법: cat Faịlụ\n"); return; }
        int 결과 = ụzọ_ozi(1); if (결과 < 0) { mmejọ(결과); return; }
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(0); if (Faịlụ < 0) { mmejọ(Faịlụ); return; }
        while (true) { int valuu = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ); if (valuu == 256) break; if (valuu < 0) { mmejọ(valuu); break; } 원바이트(valuu); }
        memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ); 단말.문자(10);
    }
    static void dezìmà_valuu() {
        if (토큰수 != 2) { 단말.Chekwaa_ozi("사용법: edit Faịlụ\n"); return; }
        int 결과 = ụzọ_ozi(1); if (결과 < 0) { mmejọ(결과); return; }
        dezìmà_akara_ahà_ogologo = ogologo_valuu[1];
        for (int memmenwè_indèks = 0; memmenwè_indèks < dezìmà_akara_ahà_ogologo; memmenwè_indèks++) dezìmà_akara_ahà[memmenwè_indèks] = akara_valuu_eb540501[시작점[1] + memmenwè_indèks];
        단말.Chekwaa_ozi("EDIT: Faịlụ 내용을 바꿉니다. .은 보존, Ctrl-C는 취소합니다(최대 16384바이트)\n");
        int Ụhara = 0;
        while (true) {
            단말.Chekwaa_ozi("edit> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Chekwaa_ozi("EDIT CANCELLED\n"); return; }
            if (입력 == 1 && ahịrī[0] == '.') break;
            if (입력 + 1 > 편집내용.length - Ụhara) { 단말.Chekwaa_ozi("EDIT CANCELLED: file too large\n"); return; }
            for (int memmenwè_indèks = 0; memmenwè_indèks < 입력; memmenwè_indèks++) 편집내용[Ụhara++] = ahịrī[memmenwè_indèks];
            편집내용[Ụhara++] = 10;
        }
        memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(dezìmà_akara_ahà_ogologo);
        for (int memmenwè_indèks = 0; memmenwè_indèks < dezìmà_akara_ahà_ogologo; memmenwè_indèks++) memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(memmenwè_indèks, dezìmà_akara_ahà[memmenwè_indèks]);
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(577); if (Faịlụ < 0) { mmejọ(Faịlụ); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(Faịlụ, 편집내용[memmenwè_indèks]);
        memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ); 단말.Chekwaa_ozi("SAVED "); 단말.수(Ụhara); 단말.Chekwaa_ozi("baịtị_valuu(주기억 Faịlụ)\n");
    }
    static int 십육(int valuu) {
        if (valuu >= '0' && valuu <= '9') return valuu - '0';
        if (valuu >= 'a' && valuu <= 'f') return valuu - 'a' + 10;
        if (valuu >= 'A' && valuu <= 'F') return valuu - 'A' + 10;
        return -1;
    }
    static void 이진입출력(boolean 넣기) {
        if (토큰수 != 2) { 단말.Chekwaa_ozi("사용법: load Faịlụ | hex Faịlụ\n"); return; }
        int 결과 = ụzọ_ozi(1); if (결과 < 0) { mmejọ(결과); return; }
        if (!넣기) {
            int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(0); if (Faịlụ < 0) { mmejọ(Faịlụ); return; }
            단말.Chekwaa_ozi("HEX BEGIN "); 단말.수(memọrị_Ndi_ọbọakwụkwọ.Ụhara(Faịlụ)); 단말.문자(10);
            int 항목수 = 0;
            while (true) {
                int valuu = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ); if (valuu < 0 || valuu == 256) break;
                단말.문자("0123456789abcdef".charAt(valuu >> 4)); 단말.문자("0123456789abcdef".charAt(valuu & 15));
                if (++항목수 % 32 == 0) 단말.문자(10);
            }
            if (항목수 % 32 != 0) 단말.문자(10);
            memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ); 단말.Chekwaa_ozi("HEX END\n"); return;
        }
        dezìmà_akara_ahà_ogologo = ogologo_valuu[1];
        for (int memmenwè_indèks = 0; memmenwè_indèks < dezìmà_akara_ahà_ogologo; memmenwè_indèks++) dezìmà_akara_ahà[memmenwè_indèks] = akara_valuu_eb540501[시작점[1] + memmenwè_indèks];
        단말.Chekwaa_ozi("LOAD: 두 자리씩 십육진수를 입력하세요. .은 보존, Ctrl-C는 취소합니다\n");
        int Ụhara = 0;
        while (true) {
            단말.Chekwaa_ozi("hex> "); int 입력 = 줄읽기();
            if (입력 < 0) { 단말.Chekwaa_ozi("LOAD CANCELLED\n"); return; }
            if (입력 == 1 && ahịrī[0] == '.') break;
            int 앞 = -1;
            for (int memmenwè_indèks = 0; memmenwè_indèks < 입력; memmenwè_indèks++) {
                if (ahịrī[memmenwè_indèks] == 32 || ahịrī[memmenwè_indèks] == 9) continue;
                int valuu = 십육(ahịrī[memmenwè_indèks]);
                if (valuu < 0 || Ụhara >= 편집내용.length) { 단말.Chekwaa_ozi("LOAD CANCELLED: 십육진수가 잘못되었거나 파일이 너무 큽니다\n"); return; }
                if (앞 < 0) 앞 = valuu; else { 편집내용[Ụhara++] = 앞 * 16 + valuu; 앞 = -1; }
            }
            if (앞 >= 0) { 단말.Chekwaa_ozi("LOAD CANCELLED: 한 바이트를 이루는 두 자리가 필요합니다\n"); return; }
        }
        memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(dezìmà_akara_ahà_ogologo);
        for (int memmenwè_indèks = 0; memmenwè_indèks < dezìmà_akara_ahà_ogologo; memmenwè_indèks++) memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(memmenwè_indèks, dezìmà_akara_ahà[memmenwè_indèks]);
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(577); if (Faịlụ < 0) { mmejọ(Faịlụ); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(Faịlụ, 편집내용[memmenwè_indèks]);
        memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ); 단말.Chekwaa_ozi("LOADED "); 단말.수(Ụhara); 단말.Chekwaa_ozi("baịtị_valuu(주기억 Faịlụ)\n");
    }
    static int Ngwaọrụ(int indèks) {
        return ngwaọrụ_ndebà(indèks, 1);
    }
    static int ngwaọrụ_ndebà(int indèks, int Bido) {
        if (토큰수 - Bido > 8) return -22;
        보드.인수준비(토큰수 - Bido);
        for (int 첫값 = Bido; 첫값 < 토큰수; 첫값++) {
            if (ogologo_valuu[첫값] > 255) return -36;
            for (int memmenwè_indèks = 0; memmenwè_indèks < ogologo_valuu[첫값]; memmenwè_indèks++) 보드.agụment_baịtị(첫값 - Bido, memmenwè_indèks, akara_valuu_eb540501[시작점[첫값] + memmenwè_indèks]);
        }
        return indèks == -2 ? 보드.리눅스파일실행() : indèks < 0 ? 보드.mee_òjìàrụ_ọbọakwụkwọ() : 보드.mee_òjìàrụ_app(indèks);
    }
    static int 파이썬꾸러미() {
        if (토큰수 > 8) return -22;
        보드.인수준비(토큰수);
        String ụzọ_ozi = "/lib/ngwungwu.py";
        // Java 문자열을 셸의 UTF-8 인수 버퍼에 기록한다.
        int 자리 = 0;
        for (int 순번 = 0; 순번 < ụzọ_ozi.length(); 순번++) {
            int mkpụrụedemede_valuu = ụzọ_ozi.charAt(순번);
            if (mkpụrụedemede_valuu < 128) 보드.agụment_baịtị(0, 자리++, mkpụrụedemede_valuu);
            else { 보드.agụment_baịtị(0, 자리++, 0xe0 | (mkpụrụedemede_valuu >> 12)); 보드.agụment_baịtị(0, 자리++, 0x80 | ((mkpụrụedemede_valuu >> 6) & 63)); 보드.agụment_baịtị(0, 자리++, 0x80 | (mkpụrụedemede_valuu & 63)); }
        }
        for (int 순번 = 1; 순번 < 토큰수; 순번++) {
            if (ogologo_valuu[순번] > 255) return -36;
            for (int mkpụrụedemede_valuu = 0; mkpụrụedemede_valuu < ogologo_valuu[순번]; mkpụrụedemede_valuu++) 보드.agụment_baịtị(순번, mkpụrụedemede_valuu, akara_valuu_eb540501[시작점[순번] + mkpụrụedemede_valuu]);
        }
        return 보드.mee_òjìàrụ_app(12);
    }
    static int 실행형식() {
        int 처리값 = ụzọ_ozi(0); if (처리값 < 0) return 처리값;
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(0); if (Faịlụ < 0) return Faịlụ;
        int 첫값 = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ), baịtị_datà = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ), koòdù_nkeakàrà = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ), 뒷값 = memọrị_Ndi_ọbọakwụkwọ.Wepụta_ọzi(Faịlụ);
        memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ);
        if (첫값 == 127 && baịtị_datà == 'E' && koòdù_nkeakàrà == 'L' && 뒷값 == 'F') return 1;
        if (첫값 == 'P' && baịtị_datà == 'K' && koòdù_nkeakàrà == 3 && 뒷값 == 4) return 2;
        return 0;
    }
    static int 예제실행(int indèks, String 인수) {
        보드.인수준비(1);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 인수.length(); memmenwè_indèks++) 보드.agụment_baịtị(0, memmenwè_indèks, 인수.charAt(memmenwè_indèks));
        return 보드.mee_òjìàrụ_app(indèks);
    }
    static void SMS_baịtị(int Faịlụ, int valuu) { memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(Faịlụ, valuu); }
    static void adịmgbanwò_ọbọakwụkwọ(String Aha, String ndịnà_valuu) {
        // ngwungwu 파일명은 ASCII. Faịlụ 내용은 UTF-8로 저장한다.
        memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(Aha.length());
        for (int memmenwè_indèks = 0; memmenwè_indèks < Aha.length(); memmenwè_indèks++) memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(memmenwè_indèks, Aha.charAt(memmenwè_indèks));
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(193); if (Faịlụ < 0) return;
        for (int memmenwè_indèks = 0; memmenwè_indèks < ndịnà_valuu.length(); memmenwè_indèks++) {
            int koòdù_nkeakàrà = ndịnà_valuu.charAt(memmenwè_indèks);
            if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff && memmenwè_indèks + 1 < ndịnà_valuu.length()) koòdù_nkeakàrà = 0x10000 + ((koòdù_nkeakàrà - 0xd800) << 10) + ndịnà_valuu.charAt(++memmenwè_indèks) - 0xdc00;
            if (koòdù_nkeakàrà < 128) SMS_baịtị(Faịlụ, koòdù_nkeakàrà);
            else {
                int 수 = koòdù_nkeakàrà < 2048 ? 2 : koòdù_nkeakàrà < 65536 ? 3 : 4;
                SMS_baịtị(Faịlụ, (수 == 2 ? 0xc0 : 수 == 3 ? 0xe0 : 0xf0) | (koòdù_nkeakàrà >> (6 * (수 - 1))));
                for (int 항목수 = 수 - 1; 항목수 > 0; 항목수--) SMS_baịtị(Faịlụ, 0x80 | ((koòdù_nkeakàrà >> (6 * (항목수 - 1))) & 63));
            }
        }
        memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ);
    }
    static void 한글도움말() {
        단말.Chekwaa_ozi("F9 / Shift+Space: [EN] ↔ [ig]\n");
        단말.Chekwaa_ozi("  [IG] keyboard; [EN] ASCII\n");
        단말.Chekwaa_ozi("  a → a\n");
        단말.Chekwaa_ozi("  F9: EN ↔ ig | Ctrl+Shift+V: UTF-8\n");
        단말.Chekwaa_ozi("  Ctrl+Shift+U: Unicode hex → Enter | Right Alt: AltGr\n");
        단말.Chekwaa_ozi("  help input | vi: i ... Esc :wq | Ctrl+Shift+T: + terminal\n");
    }
    static int 예제경로(String Aha) {
        int 바이트수 = 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < Aha.length(); memmenwè_indèks++) { int koòdù_nkeakàrà = Aha.charAt(memmenwè_indèks); if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff) return -22; 바이트수 += koòdù_nkeakàrà < 128 ? 1 : koòdù_nkeakàrà < 2048 ? 2 : 3; }
        int 처리값 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(바이트수); if (처리값 < 0) return 처리값;
        int 자리 = 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < Aha.length(); memmenwè_indèks++) {
            int koòdù_nkeakàrà = Aha.charAt(memmenwè_indèks);
            if (koòdù_nkeakàrà < 128) memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, koòdù_nkeakàrà);
            else if (koòdù_nkeakàrà < 2048) { memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, 0xc0 | (koòdù_nkeakàrà >> 6)); memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, 0x80 | (koòdù_nkeakàrà & 63)); }
            else { memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, 0xe0 | (koòdù_nkeakàrà >> 12)); memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, 0x80 | ((koòdù_nkeakàrà >> 6) & 63)); memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(자리++, 0x80 | (koòdù_nkeakàrà & 63)); }
        }
        return 0;
    }
    static int 예제폴더(String Aha) {
        int 처리값 = 예제경로(Aha); if (처리값 < 0) return 처리값;
        처리값 = memọrị_Ndi_ọbọakwụkwọ.mepụta_dàịrektrị(); return 처리값 == -17 ? 0 : 처리값;
    }
    static int 예제파일(String Aha, String datà) {
        int 처리값 = 예제경로(Aha); if (처리값 < 0) return 처리값;
        int Faịlụ = memọrị_Ndi_ọbọakwụkwọ.Mepee(193); if (Faịlụ == -17) return 0; if (Faịlụ < 0) return Faịlụ;
        for (int memmenwè_indèks = 0; memmenwè_indèks < datà.length(); memmenwè_indèks += 2) {
            처리값 = memọrị_Ndi_ọbọakwụkwọ.Chekwaa_ozi(Faịlụ, 십육(datà.charAt(memmenwè_indèks)) * 16 + 십육(datà.charAt(memmenwè_indèks + 1)));
            if (처리값 < 0) { memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ); return 처리값; }
        }
        return memọrị_Ndi_ọbọakwụkwọ.Mechie(Faịlụ);
    }
    static void gòsi_ènyèmaka() {
        sistèm_ngwaọrụ.gòsi_ènyèmaka();
        단말.Chekwaa_ozi("sshd / nchedo_nkọwannyemiwu start|stop|status: SSH :22 (user, 장치별 okwuntughe_valuu)\n");
        단말.Chekwaa_ozi("vncd / ebe_dị̀anyā_gosịpụta start|stop|status: VNC :5900 (장치별 okwuntughe_valuu)\n");
        단말.Chekwaa_ozi("SSH는 기존 콘솔 공유. RDP 서버는 아직 지원하지 않습니다.\n");
        단말.Chekwaa_ozi("help info pwd cd ls mkdir rmdir touch cp mv rm cat edit vi echo clear\n");
        단말.Chekwaa_ozi("wc grep head tail tee env export unset history sh source true false exit\n");
        단말.Chekwaa_ozi("Syntax: quotes, backslash, $NAME ${NAME} $? ; && || | < > >>\n");
        단말.Chekwaa_ozi("terminal / F12: GUI terminal; arrows/history/Tab; pipes <= 16384 bytes\n");
        단말.Chekwaa_ozi("모서리 + 왼쪽 버튼 dọkpụrụ_valuu: 터미널 Ụhara gbanwèe_valuu; terminal size: ọgbàràogō_valuu/ihendekọta_valuu\n");
        단말.Chekwaa_ozi("Ctrl+Shift+T: new terminal (max 4); F6: switch; drag title / X: close\n");
        단말.Chekwaa_ozi("vi FILE: i to insert; Esc then :wq to save and quit\n");
        단말.Chekwaa_ozi("load FILE | hex FILE | run FILE [ARGS] | ./FILE [ARGS] (ELF header, no suffix needed)\n");
        단말.Chekwaa_ozi("run --linux FILE [ARGS]: limited static ARM64 Linux syscall ABI\n");
        단말.Chekwaa_ozi("javac FILE.java | java CLASS [ARGS] (jkoros Java subset, not OpenJDK)\n");
        단말.Chekwaa_ozi("java -jar FILE.jar | ./FILE.jar [ARGS] (JVM subset)\n");
        단말.Chekwaa_ozi("jaot FILE.class|FILE.jar -o FILE.elf (static Java subset to native ARM64)\n");
        단말.Chekwaa_ozi("cc FILE.c -o FILE.elf | ftpd start|stop|status (TCP/SLIP)\n");
        단말.Chekwaa_ozi("python FILE.py | python -c 'CODE' (MicroPython)\n");
        단말.Chekwaa_ozi("pip install NAME[==VERSION] | pip list | pip uninstall NAME\n");
        단말.Chekwaa_ozi("pip: MicroPython ebensìbịa_èsèrèsè_osisi wùbe_valuu; usu --network --pip 필요; /lib는 RAM\n");
        단말.Chekwaa_ozi("gui | run cpp | net test | tasks | selftest | samples\n");
        단말.Chekwaa_ozi("C: guest TinyCC; C++: host SDK. RAM files disappear on reboot.\n");
        단말.Chekwaa_ozi("/example/java /example/c /example/python: examples ready at boot\n");
        단말.Chekwaa_ozi("example java|c|python: restore missing examples (keeps existing files)\n");
        한글도움말();
    }
    static void 터미널(boolean 전환여부) {
        if (전환여부 && 보드.터미널(2) != 0) { 보드.터미널(0); 단말.Chekwaa_ozi("TERMINAL CLOSED\n"); }
        else if (보드.터미널(1) < 0) mmejọ(-19);
        else 단말.Chekwaa_ozi("TERMINAL READY — ig terminal\nhelp: commands; F12: close; PgUp/PgDn: scroll\n");
    }
    static void Ntiiwu() {
        if (토큰수 == 0) return;
        if (sistèm_ngwaọrụ.mee_nnyemiwu()) return;
        if (같음(0,"sshd") || 같음(0,"nchedo_nkọwannyemiwu") || 같음(0,"vncd") || 같음(0,"ebe_dị̀anyā_gosịpụta")) {
            int 종류=같음(0,"vncd")||같음(0,"ebe_dị̀anyā_gosịpụta")?1:0;
            int mmèm=같음(1,"start")||같음(1,"Bido")?1:같음(1,"stop")||같음(1,"Kwụsị")?0:2;
            int ọnọdụ_valuu=보드.njizi_dị̀anyā(종류,mmèm);
            if(ọnọdụ_valuu<0)mmejọ(ọnọdụ_valuu);else 단말.Chekwaa_ozi(보드.njizi_dị̀anyā(종류,2)>0?"RUNNING\n":"STOPPED\n");return;
        }
        if (같음(0, "help") || 같음(0, "h")) { if (같음(1, "ko") || 같음(1, "input")) 한글도움말(); else gòsi_ènyèmaka(); }
        else if (같음(0, "info") || 같음(0, "i")) mkpụrụobī_kọmpùta.Ozi_Sistèm();
        else if (같음(0, "pwd")) { memọrị_Ndi_ọbọakwụkwọ.현재쓰기(); 단말.문자(10); }
        else if (같음(0, "cd")) {
            int 처리값;
            if (토큰수 == 1) { memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(1); 처리값 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(0, '/'); } else 처리값 = 토큰수 == 2 ? ụzọ_ozi(1) : -22;
            if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.gbanwèe_dàịrektrị(); if (처리값 < 0) mmejọ(처리값);
        }
        else if (같음(0, "ls") || 같음(0, "f")) {
            int agụment_indèks = 같음(1, "-l") ? 2 : 1, 처리값;
            if (토큰수 == agụment_indèks) { memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(1); 처리값 = memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(0, '.'); } else 처리값 = 토큰수 == agụment_indèks + 1 ? ụzọ_ozi(agụment_indèks) : -22;
            if (처리값 >= 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.경로목록(); if (처리값 < 0) mmejọ(처리값);
        }
        else if (같음(0, "mkdir") || 같음(0, "rmdir") || 같음(0, "touch")) nkọwannyemiwu_Ngwaọrụ.ọbọakwụkwọ_ọrụ(같음(0, "mkdir") ? "mkdir" : 같음(0, "rmdir") ? "rmdir" : "touch");
        else if (같음(0, "cp") || 같음(0, "mv")) nkọwannyemiwu_Ngwaọrụ.ṅomie_valuu(같음(0, "mv"));
        else if (같음(0, "cat")) nkọwannyemiwu_Ngwaọrụ.lèe_valuu();
        else if (같음(0, "wc")) nkọwannyemiwu_Ngwaọrụ.세기();
        else if (같음(0, "grep")) nkọwannyemiwu_Ngwaọrụ.chọta_ndebà();
        else if (같음(0, "head") || 같음(0, "tail")) nkọwannyemiwu_Ngwaọrụ.머리(같음(0, "tail"));
        else if (같음(0, "tee")) nkọwannyemiwu_Ngwaọrụ.함께쓰기();
        else if (같음(0, "env")) nkọwannyemiwu_ndokọokwū.환경보기();
        else if (같음(0, "export") || 같음(0, "unset")) {
            if (토큰수 == 1) nkọwannyemiwu_ndokọokwū.환경보기();
            for (int memmenwè_indèks = 1; memmenwè_indèks < 토큰수; memmenwè_indèks++) { int 처리값 = nkọwannyemiwu_ndokọokwū.환경설정(memmenwè_indèks, 같음(0, "unset")); if (처리값 != 0) { 결과 = 처리값; 단말.Chekwaa_ozi("Ntiiwu kerìsịa_valuu: 변수 이름이 잘못되었거나 예약된 이름이거나 환경 공간이 가득 찼습니다\n"); } }
        }
        else if (같음(0, "sh") || 같음(0, "source")) nkọwannyemiwu_ndokọokwū.mee_ọbọakwụkwọ();
        else if (같음(0, "true")) 결과 = 0;
        else if (같음(0, "false")) 결과 = 1;
        else if (같음(0, "history")) ahịrī_òdezi.gòsi_ndekọ();
        else if (같음(0, "exit")) {
            if (nkọwannyemiwu_ndokọokwū.깊이 > 0) { 결과 = 토큰수 == 1 ? nkọwannyemiwu_ndokọokwū.ọnọdụ_valuu : nkọwannyemiwu_Ngwaọrụ.ọbula_valuu(1); if (결과 < 0 || 결과 > 255) 결과 = 2; nkọwannyemiwu_ndokọokwū.Èdèrède_ntụziaka_mèdebe = true; }
            else if (보드.터미널(2) != 0) 터미널(true);
            else 단말.Chekwaa_ozi("Use Ctrl+A then X to stop QEMU.\n");
        }
        else if (같음(0, "edit")) dezìmà_valuu();
        else if (같음(0, "load") || 같음(0, "hex")) 이진입출력(같음(0, "load"));
        else if (같음(0, "rm")) {
            if (토큰수 < 2) { 결과 = 2; 단말.Chekwaa_ozi("사용법: rm Faịlụ...\n"); }
            for (int memmenwè_indèks = 1; memmenwè_indèks < 토큰수; memmenwè_indèks++) { int 처리값 = ụzọ_ozi(memmenwè_indèks); if (처리값 == 0) 처리값 = memọrị_Ndi_ọbọakwụkwọ.지우기(); if (처리값 < 0) mmejọ(처리값); }
        }
        else if (같음(0, "echo")) {
            int 시작자리 = 같음(1, "-n") ? 2 : 1;
            for (int 첫값 = 시작자리; 첫값 < 토큰수; 첫값++) { if (첫값 > 시작자리) 단말.문자(32); for (int memmenwè_indèks = 0; memmenwè_indèks < ogologo_valuu[첫값]; memmenwè_indèks++) 보드.직렬쓰기(akara_valuu_eb540501[시작점[첫값] + memmenwè_indèks]); }
            if (시작자리 == 1) 단말.문자(10);
        }
        else if (같음(0, "clear")) 단말.Chekwaa_ozi("\u001b[2J\u001b[H");
        else if (같음(0, "javac") || 같음(0, "java") || 같음(0, "python") || 같음(0, "pip")) {
            int 처리값 = 같음(0, "pip") ? 파이썬꾸러미() : Ngwaọrụ(같음(0, "javac") ? 10 : 같음(0, "java") ? 11 : 12); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
            if (처리값 != -1005 && !nkọwannyemiwu_ndokọokwū.연결중) { 단말.Chekwaa_ozi("exit "); 단말.수(처리값); 단말.문자(10); }
        }
        else if (같음(0, "vi")) { int 처리값 = Ngwaọrụ(13); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; }
        else if (같음(0, "cc") || 같음(0, "tcc")) { int 처리값 = Ngwaọrụ(15); 결과 = 처리값 < 0 ? 126 : 처리값; if (!nkọwannyemiwu_ndokọokwū.연결중) { 단말.Chekwaa_ozi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "jaot")) { int 처리값 = Ngwaọrụ(16); 결과 = 처리값 < 0 ? 126 : 처리값; if (!nkọwannyemiwu_ndokọokwū.연결중) { 단말.Chekwaa_ozi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "terminal")) {
            if (같음(1, "size")) { int Ụhara = 보드.터미널(13); 단말.Chekwaa_ozi("TERMINAL SIZE "); 단말.수(Ụhara & 65535); 단말.문자('x'); 단말.수(Ụhara >>> 16); 단말.문자(10); }
            else 터미널(false);
        }
        else if (같음(0, "gui") || 같음(0, "v")) { 보드.터미널(9); desktọpụ.mee_nnyemiwu(); }
        else if (같음(0, "c")) mkpụrụobī_kọmpùta.씨시험();
        else if (같음(0, "tasks") || 같음(0, "t")) mkpụrụobī_kọmpùta.작업시험();
        else if (같음(0, "g")) mkpụrụobī_kọmpùta.화면();
        else if (같음(0, "selftest") || 같음(0, "u")) mkpụrụobī_kọmpùta.사용자시험();
        else if (같음(0, "e") || (같음(0, "run") && 같음(1, "cpp"))) {
            int 처리값 = 보드.mee_òjìàrụ_app(0); if (처리값 == 0) 단말.Chekwaa_ozi("ELF DEMO PASS\n"); else mmejọ(처리값);
        }
        else if (같음(0, "run")) { int 처리값 = 같음(1, "--linux") ? ngwaọrụ_ndebà(-2, 2) : Ngwaọrụ(-1); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값; if (처리값 != -1005 && !nkọwannyemiwu_ndokọokwū.연결중) { 단말.Chekwaa_ozi("exit "); 단말.수(처리값); 단말.문자(10); } }
        else if (같음(0, "n") || (같음(0, "net") && 같음(1, "test"))) mkpụrụobī_kọmpùta.통신시험();
        else if (같음(0, "ftpd")) {
            if (같음(1, "start")) { int 처리값 = 보드.ọbọakwụkwọ_dògharịa_ọrụ(1); if (처리값 < 0) mmejọ(처리값); else { 단말.Chekwaa_ozi("FTP listening "); sistèm_ngwaọrụ.dee_àdreèsì(보드.Netwọọkụ_ọnọdụ(0,0)); 단말.Chekwaa_ozi(":21 (SLIP / anonymous / RAM)\n"); } }
            else if (같음(1, "stop")) { 보드.ọbọakwụkwọ_dògharịa_ọrụ(0); 단말.Chekwaa_ozi("FTP stopped\n"); }
            else 단말.Chekwaa_ozi(보드.ọbọakwụkwọ_dògharịa_ọrụ(2) != 0 ? "FTP running\n" : "FTP stopped; ftpd start | stop | status\n");
        }
        else if (같음(0, "samples")) { ngwungwu.Kwado(); 단말.Chekwaa_ozi("SAMPLES READY (existing files kept)\n"); }
        else if (같음(0, "example")) {
            int Asụsụ = 같음(1, "java") ? 0 : 같음(1, "c") ? 1 : 같음(1, "python") ? 2 : -1;
            if (토큰수 != 2 || Asụsụ < 0) 단말.Chekwaa_ozi("example java|c|python: 출력, Faịlụ, 네트워크, 그래픽, Java Swing windò 예제\n");
            else { int 처리값 = 예제꾸러미.wùbe_valuu(Asụsụ); if (처리값 < 0) { mmejọ(처리값); if (처리값 == -28) 단말.Chekwaa_ozi("RAM full: remove unused files, then retry example\n"); } else 단말.Chekwaa_ozi("EXAMPLES READY /example (existing files kept)\n"); }
        }
        else {
            int hàzie_valuu = 실행형식();
            if (hàzie_valuu == 1 || hàzie_valuu == 2) {
                int 처리값 = ngwaọrụ_ndebà(hàzie_valuu == 1 ? -1 : 14, 0); 결과 = 처리값 == -1005 ? -1005 : 처리값 < 0 ? 126 : 처리값;
                if (처리값 != -1005 && !nkọwannyemiwu_ndokọokwū.연결중) { 단말.Chekwaa_ozi("exit "); 단말.수(처리값); 단말.문자(10); }
            } else if (hàzie_valuu == 0) { 결과 = 126; 단말.Chekwaa_ozi("실행할 수 없습니다: ELF 또는 JAR 머리부가 필요합니다\n"); }
            else { 결과 = 127; 단말.Chekwaa_ozi("Unknown command. help: commands\n"); }
        }
    }
    public static void mee_nnyemiwu() {
        ngwungwu.Kwado();
        for (int Asụsụ = 0; Asụsụ < 3; Asụsụ++) { int 처리값 = 예제꾸러미.wùbe_valuu(Asụsụ); if (처리값 < 0) mmejọ(처리값); }
        gòsi_ènyèmaka();
        while (true) {
            windò_oge.ùsòrò_valuu_ndebà(); if (windò_oge.재개()) continue;
            if (!windò_oge.이어읽기) 단말.Chekwaa_ozi("jkoros-native> "); ahịrī_òdezi.ahịrị_nnyemiwu = true; 보드.원격대기(1); int Ụhara = 줄읽기(); 보드.원격대기(0); ahịrī_òdezi.ahịrị_nnyemiwu = false;
            if (Ụhara == -3) continue;
            if (Ụhara == -2) 단말.Chekwaa_ozi("Ntiiwu kerìsịa_valuu: 명령줄이 너무 깁니다\n");
            if (Ụhara >= 0) { nkọwannyemiwu_ndokọokwū.Èdèrède_ntụziaka_mèdebe = false; nkọwannyemiwu_ndokọokwū.mee_nnyemiwu(ahịrī, 0, Ụhara, 0); } else nkọwannyemiwu_ndokọokwū.ọnọdụ_valuu = 130;
            보드.mèdebe_ebe_dị̀anyā_nnyemiwu(nkọwannyemiwu_ndokọokwū.ọnọdụ_valuu);
            ahịrī_òdezi.Ụhara = ahịrī_òdezi.akàran̄ziebe_valuu = ahịrī_òdezi.Mbido_windò = 0;
        }
    }
}
