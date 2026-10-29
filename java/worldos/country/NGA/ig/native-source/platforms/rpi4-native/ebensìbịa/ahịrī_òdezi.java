// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** UTF-8 baịtị_valuu 경계를 지키는 삽입/삭제, 방향키, Ntiiwu ndekọ_NDEKỌ, Tab 완성. */
public final class ahịrī_òdezi {
    static boolean ahịrị_nnyemiwu;
    static int[] ndekọ_NDEKỌ = new int[16 * 1024], ndekọ_ogologo = new int[16], Store_valuu = new int[4096], 후보 = new int[64];
    static int 기록수, ndekọ_NDEKỌ_mèdebe, Chọọ_valuu, 저장길이, Ụhara, akàran̄ziebe_valuu, 후보수, 후보길이, Mbido_windò;
    static boolean 가로보기;
    static String 명령들 = "help info pwd cd ls mkdir rmdir touch cp mv rm cat edit load hex echo clear wc grep head tail tee env export unset history sh source true false exit terminal gui vi javac java python pip jaot cc tcc ftpd sshd vncd nchedo_nkọwannyemiwu ebe_dị̀anyā_gosịpụta run samples example tasks selftest ipconfig ip ifconfig ping route netstat ss ps top free df uptime poweroff";
    static int[] 명령후보 = new int[128];
    static void 명령후보넣기(String ndebà_ndepụta, int 시작자리, int 끝자리, int 입력길이) {
        int 바이트수=0;
        for(int 자리=시작자리;자리<끝자리;자리++) {
            int koòdù_nkeakàrà=ndebà_ndepụta.charAt(자리);
            if(koòdù_nkeakàrà>=0xd800 && koòdù_nkeakàrà<=0xdbff && 자리+1<끝자리)koòdù_nkeakàrà=0x10000+((koòdù_nkeakàrà-0xd800)<<10)+ndebà_ndepụta.charAt(++자리)-0xdc00;
            int 수=koòdù_nkeakàrà<128?1:koòdù_nkeakàrà<2048?2:koòdù_nkeakàrà<65536?3:4;
            if(바이트수+수>62)return;
            for(int NSOTANSO_valuu=수-1;NSOTANSO_valuu>=0;NSOTANSO_valuu--)명령후보[바이트수++]=수==1?koòdù_nkeakàrà:NSOTANSO_valuu==수-1?(수==2?0xc0:수==3?0xe0:0xf0)|(koòdù_nkeakàrà>>(6*NSOTANSO_valuu)):0x80|((koòdù_nkeakàrà>>(6*NSOTANSO_valuu))&63);
        }
        if(바이트수<입력길이)return;
        for(int 자리=0;자리<입력길이;자리++)if(명령후보[자리]!=명령해석기.ahịrī[자리])return;
        후보수++;후보길이=바이트수+1;
        for(int 자리=0;자리<바이트수;자리++)후보[자리]=명령후보[자리];후보[바이트수]=' ';
    }
    static int 앞(int 읽는자리) { if (읽는자리 > 0) { 읽는자리--; while (읽는자리 > 0 && (명령해석기.ahịrī[읽는자리] & 192) == 128) 읽는자리--; } return 읽는자리; }
    static int Àzụ_valuu(int 읽는자리) { if (읽는자리 < Ụhara) { 읽는자리++; while (읽는자리 < Ụhara && (명령해석기.ahịrī[읽는자리] & 192) == 128) 읽는자리++; } return 읽는자리; }
    static int 폭(int 시작자리, int ebemwèga_valuu_indèks) {
        int 글칸수 = 0;
        for (int memmenwè_indèks = 시작자리; memmenwè_indèks < ebemwèga_valuu_indèks; memmenwè_indèks++) { int baịtị_datà = 명령해석기.ahịrī[memmenwè_indèks]; if ((baịtị_datà & 192) == 128) continue; 글칸수 += baịtị_datà >= 196 ? 2 : 1; }
        return 글칸수;
    }
    static void 다시() {
        단말.Chekwaa_ozi("\r\u001b[2K");
        단말.Chekwaa_ozi(ahịrị_nnyemiwu ? "jkoros-native> " : "edit> ");
        보이는줄();
    }
    // 한 물리 ahịrī 안에서 좌우로 이동한다. 긴 명령의 재표시가 위쪽 출력을 지우지 않는다.
    static int 보이는폭() { int 열수 = 보드.터미널(13) & 65535; return 열수 - (ahịrị_nnyemiwu ? 18 : 9); }
    static void 보이는줄() {
        if (akàran̄ziebe_valuu < Mbido_windò) Mbido_windò = akàran̄ziebe_valuu;
        while (폭(Mbido_windò, akàran̄ziebe_valuu) > 보이는폭()) Mbido_windò = Àzụ_valuu(Mbido_windò);
        int 끝자리 = Mbido_windò;
        while (끝자리 < Ụhara && 폭(Mbido_windò, Àzụ_valuu(끝자리)) <= 보이는폭()) 끝자리 = Àzụ_valuu(끝자리);
        단말.Chekwaa_ozi("\r\u001b["); 단말.수(ahịrị_nnyemiwu ? 16 : 7); 단말.Chekwaa_ozi("G\u001b[K");
        if (Mbido_windò > 0) 단말.문자('<');
        for (int memmenwè_indèks = Mbido_windò; memmenwè_indèks < 끝자리; memmenwè_indèks++) 보드.직렬쓰기(명령해석기.ahịrī[memmenwè_indèks]);
        단말.문자(끝자리 < Ụhara ? '>' : ' ');
        단말.Chekwaa_ozi("\u001b["); 단말.수(폭(akàran̄ziebe_valuu, 끝자리) + 1); 단말.문자('D');
        가로보기 = Mbido_windò > 0 || 끝자리 < Ụhara || 폭(0, Ụhara) > 보이는폭();
    }
    static void 기록넣기() {
        if (!ahịrị_nnyemiwu || Ụhara == 0 || Ụhara > 1024) return;
        if (기록수 > 0) {
            int 마지막자리 = (ndekọ_NDEKỌ_mèdebe + 15) % 16; boolean 같은여부 = ndekọ_ogologo[마지막자리] == Ụhara;
            for (int memmenwè_indèks = 0; 같은여부 && memmenwè_indèks < Ụhara; memmenwè_indèks++) if (ndekọ_NDEKỌ[마지막자리 * 1024 + memmenwè_indèks] != 명령해석기.ahịrī[memmenwè_indèks]) 같은여부 = false;
            if (같은여부) return;
        }
        ndekọ_ogologo[ndekọ_NDEKỌ_mèdebe] = Ụhara; for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) ndekọ_NDEKỌ[ndekọ_NDEKỌ_mèdebe * 1024 + memmenwè_indèks] = 명령해석기.ahịrī[memmenwè_indèks];
        ndekọ_NDEKỌ_mèdebe = (ndekọ_NDEKỌ_mèdebe + 1) % 16; if (기록수 < 16) 기록수++;
    }
    static void 기록이동(int 변화량) {
        if (!ahịrị_nnyemiwu) return;
        if (Chọọ_valuu == 0 && 변화량 > 0) { 저장길이 = Ụhara; for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) Store_valuu[memmenwè_indèks] = 명령해석기.ahịrī[memmenwè_indèks]; }
        int 다음자리 = Chọọ_valuu + 변화량; if (다음자리 < 0 || 다음자리 > 기록수) return; Chọọ_valuu = 다음자리;
        if (Chọọ_valuu == 0) { Ụhara = 저장길이; for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) 명령해석기.ahịrī[memmenwè_indèks] = Store_valuu[memmenwè_indèks]; }
        else { int 보관칸 = (ndekọ_NDEKỌ_mèdebe + 16 - Chọọ_valuu) % 16; Ụhara = ndekọ_ogologo[보관칸]; for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) 명령해석기.ahịrī[memmenwè_indèks] = ndekọ_NDEKỌ[보관칸 * 1024 + memmenwè_indèks]; }
        akàran̄ziebe_valuu = Ụhara; 다시();
    }
    static void gòsi_ndekọ() {
        for (int 항목수 = 0; 항목수 < 기록수; 항목수++) {
            int 보관칸 = (ndekọ_NDEKỌ_mèdebe + 16 - 기록수 + 항목수) % 16; 단말.수(항목수 + 1); 단말.Chekwaa_ozi("  ");
            for (int memmenwè_indèks = 0; memmenwè_indèks < ndekọ_ogologo[보관칸]; memmenwè_indèks++) 보드.직렬쓰기(ndekọ_NDEKỌ[보관칸 * 1024 + memmenwè_indèks]); 단말.문자(10);
        }
    }
    static void 후보넣기(int[] datà_MKPOKỌTA, int 시작자리, int 항목수, int 접두말, int 총수, boolean 폴더번호) {
        if (항목수 < 총수 || 항목수 > 62) return;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 총수; memmenwè_indèks++) if (datà_MKPOKỌTA[시작자리 + memmenwè_indèks] != 명령해석기.ahịrī[접두말 + memmenwè_indèks]) return;
        후보수++; 후보길이 = 항목수 + 1;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 후보[memmenwè_indèks] = datà_MKPOKỌTA[시작자리 + memmenwè_indèks]; 후보[항목수] = 폴더번호 ? '/' : ' ';
    }
    static void 완성() {
        if (!ahịrị_nnyemiwu || akàran̄ziebe_valuu != Ụhara) return;
        int 시작점 = Ụhara; while (시작점 > 0 && 명령해석기.ahịrī[시작점 - 1] != ' ') 시작점--;
        for (int memmenwè_indèks = 시작점; memmenwè_indèks < Ụhara; memmenwè_indèks++) if (명령해석기.ahịrī[memmenwè_indèks] == '/' || 명령해석기.ahịrī[memmenwè_indèks] == '"' || 명령해석기.ahịrī[memmenwè_indèks] == 39 || 명령해석기.ahịrī[memmenwè_indèks] == '\\') return;
        후보수 = 0; int 항목수 = Ụhara - 시작점;
        if (시작점 == 0) {
            for(int ndepụta_indèks=0;ndepụta_indèks<2;ndepụta_indèks++) {
                String ndebà_ndepụta=ndepụta_indèks==0?명령들:관리명령.완성어();
                int 읽는자리=0;
                while(읽는자리<ndebà_ndepụta.length()) {
                    int 끝자리=읽는자리;while(끝자리<ndebà_ndepụta.length() && ndebà_ndepụta.charAt(끝자리)!=' ')끝자리++;
                    명령후보넣기(ndebà_ndepụta,읽는자리,끝자리,항목수);읽는자리=끝자리+1;
                }
            }
        } else {
            memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_Mbido(1); memọrị_Ndi_ọbọakwụkwọ.ụzọ_ozi_baịtị(0, '.'); memọrị_Ndi_ọbọakwụkwọ.mèzima_valuu();
            for (int memmenwè_indèks = 0; memmenwè_indèks < memọrị_Ndi_ọbọakwụkwọ.파일수; memmenwè_indèks++) {
                int 시작자리 = memọrị_Ndi_ọbọakwụkwọ.ndebà_Mbido(memọrị_Ndi_ọbọakwụkwọ.Aha, memmenwè_indèks * 64, memọrị_Ndi_ọbọakwụkwọ.이름길이[memmenwè_indèks]);
                if (시작자리 >= 0) 후보넣기(memọrị_Ndi_ọbọakwụkwọ.Aha, memmenwè_indèks * 64 + 시작자리, memọrị_Ndi_ọbọakwụkwọ.이름길이[memmenwè_indèks] - 시작자리, 시작점, 항목수, false);
            }
            for (int memmenwè_indèks = 0; memmenwè_indèks < 16; memmenwè_indèks++) {
                int 시작자리 = memọrị_Ndi_ọbọakwụkwọ.ndebà_Mbido(memọrị_Ndi_ọbọakwụkwọ.dàịrektrị_akara_ahà, memmenwè_indèks * 64, memọrị_Ndi_ọbọakwụkwọ.dàịrektrị_ogologo[memmenwè_indèks]);
                if (시작자리 >= 0) 후보넣기(memọrị_Ndi_ọbọakwụkwọ.dàịrektrị_akara_ahà, memmenwè_indèks * 64 + 시작자리, memọrị_Ndi_ọbọakwụkwọ.dàịrektrị_ogologo[memmenwè_indèks] - 시작자리, 시작점, 항목수, true);
            }
        }
        if (후보수 != 1) { 보드.직렬쓰기(7); return; }
        for (int memmenwè_indèks = 항목수; memmenwè_indèks < 후보길이 && Ụhara < 명령해석기.ahịrī.length - 1; memmenwè_indèks++) {
            if (후보[memmenwè_indèks] == ' ' && memmenwè_indèks != 후보길이 - 1) 명령해석기.ahịrī[Ụhara++] = '\\';
            명령해석기.ahịrī[Ụhara++] = 후보[memmenwè_indèks];
        }
        akàran̄ziebe_valuu = Ụhara; 다시();
    }
    static int 탈출읽기() {
        int 시작점 = 보드.밀리초();
        while (보드.밀리초() - 시작점 < 80) { int baịtị_datà = 보드.직렬읽기(); if (baịtị_datà >= 0) return baịtị_datà; 보드.kwụsịtụ_CPU(); }
        return -1;
    }
    static void 탈출() {
        int 첫자리 = 탈출읽기(); if (첫자리 != '[' && 첫자리 != 'O') return;
        int 항목수 = 0, 끝자리 = -1;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 12; memmenwè_indèks++) { int baịtị_datà = 탈출읽기(); if (baịtị_datà < 0) return; if (baịtị_datà >= '0' && baịtị_datà <= '9') 항목수 = 항목수 * 10 + baịtị_datà - '0'; else { 끝자리 = baịtị_datà; break; } }
        if (끝자리 == 'A') 기록이동(1);
        else if (끝자리 == 'B') 기록이동(-1);
        else if (끝자리 == 'C') { akàran̄ziebe_valuu = Àzụ_valuu(akàran̄ziebe_valuu); 다시(); }
        else if (끝자리 == 'D') { akàran̄ziebe_valuu = 앞(akàran̄ziebe_valuu); 다시(); }
        else if (끝자리 == 'H' || 끝자리 == '~' && (항목수 == 1 || 항목수 == 7)) { akàran̄ziebe_valuu = 0; 다시(); }
        else if (끝자리 == 'F' || 끝자리 == '~' && (항목수 == 4 || 항목수 == 8)) { akàran̄ziebe_valuu = Ụhara; 다시(); }
        else if (끝자리 == '~' && 항목수 == 3 && akàran̄ziebe_valuu < Ụhara) {
            int 다음자리 = Àzụ_valuu(akàran̄ziebe_valuu); for (int memmenwè_indèks = 다음자리; memmenwè_indèks < Ụhara; memmenwè_indèks++) 명령해석기.ahịrī[memmenwè_indèks - 다음자리 + akàran̄ziebe_valuu] = 명령해석기.ahịrī[memmenwè_indèks]; Ụhara -= 다음자리 - akàran̄ziebe_valuu; 다시();
        }
        else if (끝자리 == '~' && (항목수 == 5 || 항목수 == 6)) 보드.터미널(항목수 == 5 ? 5 : 6);
        else if (끝자리 == '~' && 항목수 == 24 && ahịrị_nnyemiwu) { 명령해석기.터미널(true); }
    }
    static int Wepụta_ọzi() {
        if (!windò_oge.이어읽기) { Ụhara = akàran̄ziebe_valuu = Chọọ_valuu = Mbido_windò = 0; 가로보기 = false; }
        else { windò_oge.이어읽기 = false; 다시(); } boolean njubigaoke = false;
        while (true) {
            int baịtị_datà = 보드.직렬읽기(); if (baịtị_datà == -4096) return -3;
            if (보드.터미널(14) != 0) 다시(); if (baịtị_datà < 0) { 보드.kwụsịtụ_CPU(); continue; }
            if (baịtị_datà == 10 && 명령해석기.앞줄) { 명령해석기.앞줄 = false; continue; } 명령해석기.앞줄 = baịtị_datà == 13;
            if (baịtị_datà == 27) { 탈출(); continue; }
            if (baịtị_datà == 3) { 단말.Chekwaa_ozi("^C\n"); return -1; }
            if (baịtị_datà == 4 && Ụhara == 0 && ahịrị_nnyemiwu) { if (보드.터미널(2) != 0) 명령해석기.터미널(true); return -1; }
            if (baịtị_datà == 13 || baịtị_datà == 10) { 단말.문자(10); if (!njubigaoke) 기록넣기(); return njubigaoke ? -2 : Ụhara; }
            if (baịtị_datà == 9 && ahịrị_nnyemiwu) { 완성(); continue; }
            if (baịtị_datà == 1 || baịtị_datà == 5) { akàran̄ziebe_valuu = baịtị_datà == 1 ? 0 : Ụhara; 다시(); continue; }
            if (baịtị_datà == 8 || baịtị_datà == 127 || baịtị_datà == 21) {
                if (baịtị_datà == 21) { for (int memmenwè_indèks = akàran̄ziebe_valuu; memmenwè_indèks < Ụhara; memmenwè_indèks++) 명령해석기.ahịrī[memmenwè_indèks - akàran̄ziebe_valuu] = 명령해석기.ahịrī[memmenwè_indèks]; Ụhara -= akàran̄ziebe_valuu; akàran̄ziebe_valuu = 0; }
                else if (akàran̄ziebe_valuu > 0) { int 변경전 = 앞(akàran̄ziebe_valuu); for (int memmenwè_indèks = akàran̄ziebe_valuu; memmenwè_indèks < Ụhara; memmenwè_indèks++) 명령해석기.ahịrī[memmenwè_indèks - akàran̄ziebe_valuu + 변경전] = 명령해석기.ahịrī[memmenwè_indèks]; Ụhara -= akàran̄ziebe_valuu - 변경전; akàran̄ziebe_valuu = 변경전; }
                다시(); continue;
            }
            if (baịtị_datà == 11) { Ụhara = akàran̄ziebe_valuu; 다시(); continue; }
            if (baịtị_datà < 32 && baịtị_datà != 9) continue;
            if (Ụhara == 명령해석기.ahịrī.length) { njubigaoke = true; continue; }
            for (int memmenwè_indèks = Ụhara; memmenwè_indèks > akàran̄ziebe_valuu; memmenwè_indèks--) 명령해석기.ahịrī[memmenwè_indèks] = 명령해석기.ahịrī[memmenwè_indèks - 1];
            명령해석기.ahịrī[akàran̄ziebe_valuu++] = baịtị_datà; Ụhara++;
            if (akàran̄ziebe_valuu == Ụhara && !가로보기 && 폭(0, Ụhara) <= 보이는폭()) 보드.직렬쓰기(baịtị_datà);
            else if (akàran̄ziebe_valuu == Ụhara) 보이는줄(); else 다시();
        }
    }
}
