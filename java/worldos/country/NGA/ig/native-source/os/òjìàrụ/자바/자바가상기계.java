// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. Faịlụ/스택/Nrụtụ_aka/ogbè 경계를 mee_nnyemiwu 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faịlụ = new int[16384], ọbọakwụkwọ_akara_ahà_SMS = new int[64];
    static int[] ihendịgide_hụbaamā = new int[512], 상가 = new int[512], 상나 = new int[512], ùsòròokwū_Nrụtụ_aka = new int[512];
    static int[] usoro_akara_ahà_SMS = new int[32], usoro_pinye = new int[32], usoro_òhèrè = new int[32];
    static int[] usoro_Mbido = new int[32], usoro_mèdebe = new int[32], usoro_ikpo = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], usoro_agụment_pinye = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] otù_ebe_valuu = new int[4096], otù_ebe_pinye = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] okpokoro_usoro = new int[32], 틀위치 = new int[32], okpokoro_ikpo = new int[32];
    static int[] 힙 = new int[8192];
    static int Ụhara, 읽기위치, 상수수, 함수수, klaàsị_akara_ahà, okpokoro_indèks = -1, 힙끝 = 1, 반환형;
    static boolean mmejọ;

    static void ọdịdà_valuu(String Mkpụrụokwu_SMS) {
        if (!mmejọ) { òjìàrụ.Chekwaa_ozi("JVM error: "); òjìàrụ.Chekwaa_ozi(Mkpụrụokwu_SMS); òjìàrụ.dee_mkpụrụedemede_valuu(10); }
        mmejọ = true;
    }
    static boolean ntipanye(int Bido, int ogologo_valuu) { return Bido >= 0 && ogologo_valuu >= 0 && Bido <= Ụhara - ogologo_valuu; }
    static int baịtị_valuu() {
        if (!ntipanye(읽기위치, 1)) { ọdịdà_valuu("truncated class file"); return 0; }
        return Faịlụ[읽기위치++];
    }
    static int 짧은수() { return baịtị_valuu() << 8 | baịtị_valuu(); }
    static int ọnụọgụ_nzùrùòkè() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ogologo_valuu) { if (!ntipanye(읽기위치, ogologo_valuu)) ọdịdà_valuu("invalid attribute size"); else 읽기위치 += ogologo_valuu; }
    static boolean cheèk_ihendịgide(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || ihendịgide_hụbaamā[수] != 종류) { ọdịdà_valuu("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bido, int ogologo_valuu, String Mkpụrụokwu_SMS) {
        if (!ntipanye(Bido, ogologo_valuu) || ogologo_valuu != Mkpụrụokwu_SMS.length()) return false;
        for (int 수 = 0; 수 < ogologo_valuu; 수++) if (Faịlụ[Bido + 수] != Mkpụrụokwu_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Mkpụrụokwu_SMS(int ihendịgide_valuu, String Mkpụrụokwu_SMS) { return cheèk_ihendịgide(ihendịgide_valuu, 1) && 구간(상가[ihendịgide_valuu], 상나[ihendịgide_valuu], Mkpụrụokwu_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!cheèk_ihendịgide(가, 1) || !cheèk_ihendịgide(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (Faịlụ[상가[가] + 수] != Faịlụ[상가[나] + 수]) return false;
        return true;
    }
    static int klaàsị_akara_ahà_SMS(int 수) { return cheèk_ihendịgide(수, 7) && cheèk_ihendịgide(상가[수], 1) ? 상가[수] : 0; }
    static int Nrụtụ_aka_akara_ahà(int 수) { return cheèk_ihendịgide(수, 12) && cheèk_ihendịgide(상가[수], 1) ? 상가[수] : 0; }
    static int Nrụtụ_aka_pinye(int 수) { return cheèk_ihendịgide(수, 12) && cheèk_ihendịgide(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean oghere_pinye_37698895) {
        if (읽기위치 >= 끝) { ọdịdà_valuu("invalid descriptor"); return 0; }
        int valuu = baịtị_valuu();
        if (valuu == 'V' && oghere_pinye_37698895) return 0;
        if (valuu == 'I' || valuu == 'B' || valuu == 'C' || valuu == 'S' || valuu == 'Z') return 1;
        if (valuu == '[') { 서술형(끝, false); return 2; }
        if (valuu == 'L') {
            int Bido = 읽기위치;
            while (읽기위치 < 끝 && Faịlụ[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Bido) ọdịdà_valuu("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ọdịdà_valuu("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int ọrụ_valuu) {
        int 이전 = 읽기위치, 수 = usoro_pinye[ọrụ_valuu];
        if (!cheèk_ihendịgide(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (baịtị_valuu() != '(') ọdịdà_valuu("invalid method descriptor");
        int 개수 = 0;
        while (!mmejọ && 읽기위치 < 끝 && Faịlụ[읽기위치] != ')') {
            if (개수 == 16) { ọdịdà_valuu("too many method arguments"); break; }
            usoro_agụment_pinye[ọrụ_valuu * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || baịtị_valuu() != ')') ọdịdà_valuu("invalid method descriptor");
        함수반환[ọrụ_valuu] = 서술형(끝, true); 함수인수수[ọrụ_valuu] = 개수;
        if (읽기위치 != 끝) ọdịdà_valuu("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !mmejọ; 수++) { cheèk_ihendịgide(짧은수(), 1); 건너(ọnụọgụ_nzùrùòkè()); }
    }
    static int nnyemiwu_ogologo(int valuu) {
        if (valuu == 16 || valuu == 18 || valuu == 21 || valuu == 25 || valuu == 54 || valuu == 58 || valuu == 188) return 2;
        if (valuu == 17 || valuu == 19 || valuu == 132 || valuu >= 153 && valuu <= 167
            || valuu >= 178 && valuu <= 184 || valuu == 187 || valuu == 189 || valuu == 192 || valuu == 198 || valuu == 199) return 3;
        if (valuu >= 0 && valuu <= 8 || valuu >= 26 && valuu <= 29 || valuu >= 42 && valuu <= 46 || valuu == 50
            || valuu >= 59 && valuu <= 62 || valuu >= 75 && valuu <= 79 || valuu == 83 || valuu == 87 || valuu == 89 || valuu == 95
            || valuu == 96 || valuu == 100 || valuu == 104 || valuu == 108 || valuu == 112 || valuu == 116
            || valuu == 120 || valuu == 122 || valuu == 124 || valuu == 126 || valuu == 128 || valuu == 130
            || valuu >= 145 && valuu <= 147 || valuu == 172 || valuu == 176 || valuu == 177 || valuu == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (ọnụọgụ_nzùrùòkè() != 0xcafebabe) ọdịdà_valuu("not a class file");
        int 부판 = 짧은수(), ụdị_valuu = 짧은수();
        if (ụdị_valuu < 45 || ụdị_valuu > 52 || 부판 != 0) ọdịdà_valuu("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ọdịdà_valuu("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !mmejọ; 수++) {
            int 종류 = baịtị_valuu(); ihendịgide_hụbaamā[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = ọnụọgụ_nzùrùòkè();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ọdịdà_valuu("unsupported constant type");
        }
        int ikikere_valuu = 짧은수();
        if ((ikikere_valuu & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ọdịdà_valuu("unsupported class flags");
        klaàsị_akara_ahà = klaàsị_akara_ahà_SMS(짧은수());
        if (!Mkpụrụokwu_SMS(klaàsị_akara_ahà_SMS(짧은수()), "java/lang/Object")) ọdịdà_valuu("inheritance unsupported");
        if (짧은수() != 0) ọdịdà_valuu("interfaces unsupported");
        if (짧은수() != 0) ọdịdà_valuu("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ọdịdà_valuu("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !mmejọ; 수++) {
            usoro_òhèrè[수] = 짧은수(); usoro_akara_ahà_SMS[수] = 짧은수(); usoro_pinye[수] = 짧은수();
            cheèk_ihendịgide(usoro_akara_ahà_SMS[수], 1); 서술읽기(수);
            if ((usoro_òhèrè[수] & (0x100 | 0x400 | 0x20)) != 0) ọdịdà_valuu("native, abstract and synchronized methods unsupported");
            if ((usoro_òhèrè[수] & 8) == 0 && !Mkpụrụokwu_SMS(usoro_akara_ahà_SMS[수], "<init>")) ọdịdà_valuu("instance methods unsupported");
            if (Mkpụrụokwu_SMS(usoro_akara_ahà_SMS[수], "<clinit>")) ọdịdà_valuu("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(usoro_akara_ahà_SMS[앞], usoro_akara_ahà_SMS[수]) && 같은말(usoro_pinye[앞], usoro_pinye[수])) ọdịdà_valuu("duplicate method");
            int 개수 = 짧은수();
            for (int njìama_valuu = 0; njìama_valuu < 개수 && !mmejọ; njìama_valuu++) {
                int Aha = 짧은수(), ogologo_valuu = ọnụọgụ_nzùrùòkè(), Bido = 읽기위치;
                if (!ntipanye(Bido, ogologo_valuu)) { ọdịdà_valuu("truncated method attribute"); break; }
                if (Mkpụrụokwu_SMS(Aha, "Code")) {
                    if (usoro_Mbido[수] != 0) ọdịdà_valuu("duplicate Code attribute");
                    usoro_ikpo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = ọnụọgụ_nzùrùòkè();
                    if (usoro_ikpo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ọdịdà_valuu("method memory limits exceeded");
                    usoro_Mbido[수] = 읽기위치; 건너(코드길이); usoro_mèdebe[수] = 읽기위치;
                    if (짧은수() != 0) ọdịdà_valuu("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Bido + ogologo_valuu) ọdịdà_valuu("Code attribute size mismatch");
                } else 건너(ogologo_valuu);
            }
            if (usoro_Mbido[수] == 0) ọdịdà_valuu("missing Code attribute");
            int oghere_ndebà = usoro_Mbido[수];
            while (oghere_ndebà < usoro_mèdebe[수] && !mmejọ) {
                int ogologo_valuu = nnyemiwu_ogologo(Faịlụ[oghere_ndebà]);
                if (ogologo_valuu == 0 || ogologo_valuu > usoro_mèdebe[수] - oghere_ndebà) { ọdịdà_valuu("unsupported or truncated bytecode"); break; }
                경계[oghere_ndebà] = 수 + 1; oghere_ndebà += ogologo_valuu;
            }
            // 실행하지 않는 경로에도 잘못된 ogbè 목적지를 허용하지 않는다.
            oghere_ndebà = usoro_Mbido[수];
            while (oghere_ndebà < usoro_mèdebe[수] && !mmejọ) {
                int valuu = Faịlụ[oghere_ndebà];
                if (valuu >= 153 && valuu <= 167 || valuu == 198 || valuu == 199) {
                    int ebemwèga_valuu = oghere_ndebà + (short)(Faịlụ[oghere_ndebà + 1] << 8 | Faịlụ[oghere_ndebà + 2]);
                    if (ebemwèga_valuu < usoro_Mbido[수] || ebemwèga_valuu >= usoro_mèdebe[수] || 경계[ebemwèga_valuu] != 수 + 1) ọdịdà_valuu("invalid branch target");
                }
                oghere_ndebà += nnyemiwu_ogologo(valuu);
            }
        }
        if (!mmejọ) 속성건너();
        if (읽기위치 != Ụhara) ọdịdà_valuu("extra class file data");
    }
    static int kepụta_Nchekwa(int 종류, int ogologo_valuu) {
        if (ogologo_valuu < 0 || ogologo_valuu > 힙.length - 힙끝 - 2) { ọdịdà_valuu("object heap exhausted or negative array size"); return 0; }
        int Nrụtụ_aka = 힙끝; 힙끝 += ogologo_valuu + 2; 힙[Nrụtụ_aka] = 종류; 힙[Nrụtụ_aka + 1] = ogologo_valuu;
        return Nrụtụ_aka;
    }
    static boolean ihe_valuu(int Nrụtụ_aka, int 종류) {
        if (Nrụtụ_aka < 1 || Nrụtụ_aka >= 힙끝 - 1 || 힙[Nrụtụ_aka] != 종류) { ọdịdà_valuu("null or invalid object reference"); return false; }
        return true;
    }
    static int ihendịgide_SMS(int indèks) {
        if (!cheèk_ihendịgide(indèks, 1)) return 0;
        if (ùsòròokwū_Nrụtụ_aka[indèks] != 0) return ùsòròokwū_Nrụtụ_aka[indèks];
        int Nrụtụ_aka = kepụta_Nchekwa(1, 상나[indèks]); if (mmejọ) return 0;
        int 끝 = 상가[indèks] + 상나[indèks], 수 = 상가[indèks], ogologo_valuu = 0;
        while (수 < 끝 && !mmejọ) {
            int valuu = Faịlụ[수++];
            if (valuu == 0) ọdịdà_valuu("invalid modified UTF-8");
            else if (valuu >= 192 && valuu <= 223 && 수 < 끝) {
                int 다음 = Faịlụ[수++];
                if ((다음 & 192) != 128) ọdịdà_valuu("invalid modified UTF-8");
                valuu = (valuu & 31) << 6 | 다음 & 63;
                if (valuu != 0 && valuu < 128) ọdịdà_valuu("overlong modified UTF-8");
            } else if (valuu >= 224 && valuu <= 239 && 수 + 1 < 끝) {
                int 가 = Faịlụ[수++], 나 = Faịlụ[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ọdịdà_valuu("invalid modified UTF-8");
                valuu = (valuu & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (valuu < 2048) ọdịdà_valuu("overlong modified UTF-8");
            } else if (valuu >= 128) ọdịdà_valuu("invalid modified UTF-8");
            힙[Nrụtụ_aka + 2 + ogologo_valuu++] = valuu;
        }
        힙[Nrụtụ_aka + 1] = ogologo_valuu; ùsòròokwū_Nrụtụ_aka[indèks] = Nrụtụ_aka; return Nrụtụ_aka;
    }
    static int usu_mkpụrụedemede(String valuu) {
        int Nrụtụ_aka = kepụta_Nchekwa(1, valuu.length()); if (mmejọ) return 0;
        for (int 수 = 0; 수 < valuu.length(); 수++) 힙[Nrụtụ_aka + 2 + 수] = valuu.charAt(수);
        return Nrụtụ_aka;
    }
    static void dee_SMS(int Nrụtụ_aka) {
        if (Nrụtụ_aka == 0) { òjìàrụ.Chekwaa_ozi("null"); return; }
        if (!ihe_valuu(Nrụtụ_aka, 1)) return;
        for (int 수 = 0; 수 < 힙[Nrụtụ_aka + 1]; 수++) òjìàrụ.dee_mkpụrụedemede_valuu(힙[Nrụtụ_aka + 2 + 수]);
    }
    static int ọbula_mkpụrụedemede(int valuu) {
        int Nrụtụ_aka = kepụta_Nchekwa(1, 11); if (mmejọ) return 0;
        int ogologo_valuu = 0;
        if (valuu < 0) 힙[Nrụtụ_aka + 2 + ogologo_valuu++] = '-'; else valuu = -valuu;
        int 자리 = 1000000000; boolean Bido = false;
        while (자리 != 0) {
            int 수 = -(valuu / 자리);
            if (수 != 0 || Bido || 자리 == 1) { 힙[Nrụtụ_aka + 2 + ogologo_valuu++] = '0' + 수; Bido = true; }
            valuu %= 자리; 자리 /= 10;
        }
        힙[Nrụtụ_aka + 1] = ogologo_valuu; return Nrụtụ_aka;
    }
    static int 정수해독(int Nrụtụ_aka) {
        if (!ihe_valuu(Nrụtụ_aka, 1)) return 0;
        int ogologo_valuu = 힙[Nrụtụ_aka + 1], 수 = 0, valuu = 0; boolean 음수 = false;
        if (ogologo_valuu > 0 && (힙[Nrụtụ_aka + 2] == '-' || 힙[Nrụtụ_aka + 2] == '+')) { 음수 = 힙[Nrụtụ_aka + 2] == '-'; 수++; }
        if (수 == ogologo_valuu) ọdịdà_valuu("NumberFormatException");
        for (; 수 < ogologo_valuu && !mmejọ; 수++) {
            int ọbula_valuu = 힙[Nrụtụ_aka + 2 + 수] - '0';
            if (ọbula_valuu < 0 || ọbula_valuu > 9 || valuu < -214748364 || valuu == -214748364 && ọbula_valuu > (음수 ? 8 : 7)) ọdịdà_valuu("NumberFormatException");
            valuu = valuu * 10 - ọbula_valuu;
        }
        return 음수 ? valuu : -valuu;
    }
    static void 넣기(int valuu, int pinye_valuu) {
        if (mmejọ) return;
        if (okpokoro_indèks < 0 || okpokoro_ikpo[okpokoro_indèks] >= usoro_ikpo[okpokoro_usoro[okpokoro_indèks]]) { ọdịdà_valuu("operand stack overflow"); return; }
        int oghere_ndebà = okpokoro_indèks * 128 + okpokoro_ikpo[okpokoro_indèks]++; 스택값[oghere_ndebà] = valuu; 스택형[oghere_ndebà] = pinye_valuu;
    }
    static int 빼기(int pinye_valuu) {
        if (mmejọ) return 0;
        if (okpokoro_indèks < 0 || okpokoro_ikpo[okpokoro_indèks] < 1) { ọdịdà_valuu("operand stack underflow"); return 0; }
        int oghere_ndebà = okpokoro_indèks * 128 + --okpokoro_ikpo[okpokoro_indèks]; 반환형 = 스택형[oghere_ndebà];
        if (pinye_valuu != 0 && 반환형 != pinye_valuu) ọdịdà_valuu("operand type mismatch");
        return 스택값[oghere_ndebà];
    }
    static void 지역읽기(int indèks, int pinye_valuu) {
        if (indèks >= 함수지역[okpokoro_usoro[okpokoro_indèks]] || indèks < 0 || otù_ebe_pinye[okpokoro_indèks * 128 + indèks] != pinye_valuu) { ọdịdà_valuu("invalid or uninitialized local"); return; }
        넣기(otù_ebe_valuu[okpokoro_indèks * 128 + indèks], pinye_valuu);
    }
    static void dee_otù_ebe(int indèks, int pinye_valuu) {
        if (indèks >= 함수지역[okpokoro_usoro[okpokoro_indèks]] || indèks < 0) { ọdịdà_valuu("local index out of range"); return; }
        int valuu = 빼기(pinye_valuu); otù_ebe_valuu[okpokoro_indèks * 128 + indèks] = valuu; otù_ebe_pinye[okpokoro_indèks * 128 + indèks] = pinye_valuu;
    }
    static int 명바() {
        int 위치 = 틀위치[okpokoro_indèks];
        if (위치 < usoro_Mbido[okpokoro_usoro[okpokoro_indèks]] || 위치 >= usoro_mèdebe[okpokoro_usoro[okpokoro_indèks]]) { ọdịdà_valuu("instruction pointer out of range"); return 0; }
        틀위치[okpokoro_indèks]++; return Faịlụ[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void gàa_valuu(int 위치) {
        int ọrụ_valuu = okpokoro_usoro[okpokoro_indèks];
        if (위치 < usoro_Mbido[ọrụ_valuu] || 위치 >= usoro_mèdebe[ọrụ_valuu] || 경계[위치] != ọrụ_valuu + 1) ọdịdà_valuu("invalid branch target");
        else 틀위치[okpokoro_indèks] = 위치;
    }
    static void 호출(int ọrụ_valuu) {
        if (okpokoro_indèks == 31) { ọdịdà_valuu("call stack limit (32)"); return; }
        int 다음 = okpokoro_indèks + 1;
        for (int 수 = 0; 수 < 128; 수++) otù_ebe_pinye[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[ọrụ_valuu] - 1; 수 >= 0; 수--) {
            otù_ebe_valuu[다음 * 128 + 수] = 빼기(usoro_agụment_pinye[ọrụ_valuu * 16 + 수]); otù_ebe_pinye[다음 * 128 + 수] = usoro_agụment_pinye[ọrụ_valuu * 16 + 수];
        }
        okpokoro_indèks = 다음; okpokoro_usoro[okpokoro_indèks] = ọrụ_valuu; 틀위치[okpokoro_indèks] = usoro_Mbido[ọrụ_valuu]; okpokoro_ikpo[okpokoro_indèks] = 0;
    }
    static void 반환(int pinye_valuu) {
        if (pinye_valuu != 함수반환[okpokoro_usoro[okpokoro_indèks]]) { ọdịdà_valuu("return type mismatch"); return; }
        int valuu = pinye_valuu == 0 ? 0 : 빼기(pinye_valuu);
        okpokoro_indèks--; if (okpokoro_indèks >= 0 && pinye_valuu != 0) 넣기(valuu, pinye_valuu);
    }
    static int[] agịrị_ọbọakwụkwọ_akara_ahà = new int[64];
    static void ọbọakwụkwọ_agịrị_oku(int nwe_valuu, int Aha, int hàzie_valuu, int Ntiiwu) {
        boolean 출력 = Mkpụrụokwu_SMS(nwe_valuu, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Ntiiwu == 183 && Mkpụrụokwu_SMS(Aha, "<init>")) {
            boolean 이어 = false;
            if (출력 && Mkpụrụokwu_SMS(hàzie_valuu, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Mkpụrụokwu_SMS(hàzie_valuu, "(Ljava/lang/String;)V")) { ọdịdà_valuu("unsupported file stream constructor"); return; }
            int ọbọakwụkwọ_ndebà_akara_ahà = 빼기(2), agịrị_valuu = 빼기(2);
            if (!ihe_valuu(ọbọakwụkwọ_ndebà_akara_ahà, 1) || !ihe_valuu(agịrị_valuu, 종류) || mmejọ) return;
            if (힙[agịrị_valuu + 3] != 0) { ọdịdà_valuu("file stream already initialized"); return; }
            int ogologo_valuu = 힙[ọbọakwụkwọ_ndebà_akara_ahà + 1];
            if (ogologo_valuu < 1 || ogologo_valuu > 63) { ọdịdà_valuu("invalid file name length"); return; }
            for (int oghere_ndebà = 0; oghere_ndebà < ogologo_valuu; oghere_ndebà++) {
                int valuu = 힙[ọbọakwụkwọ_ndebà_akara_ahà + 2 + oghere_ndebà];
                if (valuu < 1 || valuu > 127) { ọdịdà_valuu("file stream paths currently require ASCII"); return; }
                agịrị_ọbọakwụkwọ_akara_ahà[oghere_ndebà] = valuu;
            }
            agịrị_ọbọakwụkwọ_akara_ahà[ogologo_valuu] = 0;
            int 서술자 = òjìàrụ.파일서술자열기(agịrị_ọbọakwụkwọ_akara_ahà, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ọdịdà_valuu("FileNotFoundException: file open failed"); return; }
            힙[agịrị_valuu + 2] = 서술자; 힙[agịrị_valuu + 3] = 1;
            return;
        }
        if (Ntiiwu != 182) { ọdịdà_valuu("invalid file stream invocation"); return; }
        int mmèm = -1, valuu = 0;
        if (Mkpụrụokwu_SMS(Aha, "close") && Mkpụrụokwu_SMS(hàzie_valuu, "()V")) mmèm = 0;
        if (!출력 && Mkpụrụokwu_SMS(Aha, "read") && Mkpụrụokwu_SMS(hàzie_valuu, "()I")) mmèm = 1;
        if (출력 && Mkpụrụokwu_SMS(Aha, "write") && Mkpụrụokwu_SMS(hàzie_valuu, "(I)V")) { mmèm = 2; valuu = 빼기(1); }
        if (mmèm < 0) { ọdịdà_valuu("unsupported file stream method"); return; }
        int agịrị_valuu = 빼기(2);
        if (!ihe_valuu(agịrị_valuu, 종류) || mmejọ) return;
        if (힙[agịrị_valuu + 3] == 0) { ọdịdà_valuu("uninitialized file stream"); return; }
        int 서술자 = 힙[agịrị_valuu + 2];
        if (mmèm == 0) {
            if (서술자 >= 0 && òjìàrụ.파일서술자닫기(서술자) < 0) ọdịdà_valuu("IOException: close failed");
            힙[agịrị_valuu + 2] = -1; return;
        }
        if (서술자 < 0) { ọdịdà_valuu("IOException: stream closed"); return; }
        if (mmèm == 1) {
            int 결과 = òjìàrụ.파일한바이트읽기(서술자);
            if (결과 < -1) ọdịdà_valuu("IOException: read failed"); else 넣기(결과, 1);
        } else if (òjìàrụ.파일한바이트쓰기(서술자, valuu) != 1) ọdịdà_valuu("IOException: write failed");
    }
    static void oku_usoro(int indèks, int Ntiiwu) {
        if (!cheèk_ihendịgide(indèks, 10)) return;
        int nwe_valuu = klaàsị_akara_ahà_SMS(상가[indèks]), Aha = Nrụtụ_aka_akara_ahà(상나[indèks]), hàzie_valuu = Nrụtụ_aka_pinye(상나[indèks]);
        if (mmejọ) return;
        if (같은말(nwe_valuu, klaàsị_akara_ahà)) {
            if (Ntiiwu != 184) { ọdịdà_valuu("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Aha, usoro_akara_ahà_SMS[수]) && 같은말(hàzie_valuu, usoro_pinye[수])) {
                if ((usoro_òhèrè[수] & 8) == 0) ọdịdà_valuu("method is not static"); else 호출(수);
                return;
            }
            ọdịdà_valuu("NoSuchMethodError"); return;
        }
        if (Mkpụrụokwu_SMS(nwe_valuu, "java/io/FileInputStream") || Mkpụrụokwu_SMS(nwe_valuu, "java/io/FileOutputStream")) {
            ọbọakwụkwọ_agịrị_oku(nwe_valuu, Aha, hàzie_valuu, Ntiiwu); return;
        }
        if (Ntiiwu == 184 && Mkpụrụokwu_SMS(nwe_valuu, "java/lang/Integer") && Mkpụrụokwu_SMS(Aha, "parseInt") && Mkpụrụokwu_SMS(hàzie_valuu, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Ntiiwu == 182 && Mkpụrụokwu_SMS(nwe_valuu, "java/io/PrintStream") && (Mkpụrụokwu_SMS(Aha, "println") || Mkpụrụokwu_SMS(Aha, "print"))) {
            int pinye_valuu = 0, valuu = 0;
            if (Mkpụrụokwu_SMS(hàzie_valuu, "(I)V")) { pinye_valuu = 1; valuu = 빼기(1); }
            else if (Mkpụrụokwu_SMS(hàzie_valuu, "(Z)V")) { pinye_valuu = 2; valuu = 빼기(1); }
            else if (Mkpụrụokwu_SMS(hàzie_valuu, "(C)V")) { pinye_valuu = 3; valuu = 빼기(1); }
            else if (Mkpụrụokwu_SMS(hàzie_valuu, "(Ljava/lang/String;)V")) { pinye_valuu = 4; valuu = 빼기(2); }
            else if (!Mkpụrụokwu_SMS(hàzie_valuu, "()V") || !Mkpụrụokwu_SMS(Aha, "println")) ọdịdà_valuu("unsupported print descriptor");
            if (빼기(2) != -1) ọdịdà_valuu("invalid PrintStream receiver");
            if (mmejọ) return;
            if (pinye_valuu == 1) 자바도구.수쓰기(valuu);
            if (pinye_valuu == 2) òjìàrụ.Chekwaa_ozi(valuu == 0 ? "false" : "true");
            if (pinye_valuu == 3) òjìàrụ.dee_mkpụrụedemede_valuu(valuu & 65535);
            if (pinye_valuu == 4) dee_SMS(valuu);
            if (Mkpụrụokwu_SMS(Aha, "println")) òjìàrụ.dee_mkpụrụedemede_valuu(10);
            return;
        }
        if (Ntiiwu == 182 && Mkpụrụokwu_SMS(nwe_valuu, "java/lang/String")) {
            if (Mkpụrụokwu_SMS(Aha, "length") && Mkpụrụokwu_SMS(hàzie_valuu, "()I")) {
                int Nrụtụ_aka = 빼기(2); if (ihe_valuu(Nrụtụ_aka, 1)) 넣기(힙[Nrụtụ_aka + 1], 1); return;
            }
            if (Mkpụrụokwu_SMS(Aha, "charAt") && Mkpụrụokwu_SMS(hàzie_valuu, "(I)C")) {
                int ntụkwàsa_n_akụkụ_n_àlà_valuu = 빼기(1), Nrụtụ_aka = 빼기(2);
                if (ihe_valuu(Nrụtụ_aka, 1)) {
                    if (ntụkwàsa_n_akụkụ_n_àlà_valuu < 0 || ntụkwàsa_n_akụkụ_n_àlà_valuu >= 힙[Nrụtụ_aka + 1]) ọdịdà_valuu("StringIndexOutOfBoundsException"); else 넣기(힙[Nrụtụ_aka + 2 + ntụkwàsa_n_akụkụ_n_àlà_valuu], 1);
                }
                return;
            }
        }
        if (Mkpụrụokwu_SMS(nwe_valuu, "java/lang/StringBuilder")) {
            if (Ntiiwu == 183 && Mkpụrụokwu_SMS(Aha, "<init>") && Mkpụrụokwu_SMS(hàzie_valuu, "()V")) { ihe_valuu(빼기(2), 4); return; }
            if (Ntiiwu == 182 && Mkpụrụokwu_SMS(Aha, "toString") && Mkpụrụokwu_SMS(hàzie_valuu, "()Ljava/lang/String;")) {
                int Nrụtụ_aka = 빼기(2); if (ihe_valuu(Nrụtụ_aka, 4)) 넣기(힙[Nrụtụ_aka + 2] == 0 ? usu_mkpụrụedemede("") : 힙[Nrụtụ_aka + 2], 2); return;
            }
            if (Ntiiwu == 182 && Mkpụrụokwu_SMS(Aha, "append")) {
                int SMS = 0;
                if (Mkpụrụokwu_SMS(hàzie_valuu, "(I)Ljava/lang/StringBuilder;")) SMS = ọbula_mkpụrụedemede(빼기(1));
                else if (Mkpụrụokwu_SMS(hàzie_valuu, "(Z)Ljava/lang/StringBuilder;")) SMS = usu_mkpụrụedemede(빼기(1) == 0 ? "false" : "true");
                else if (Mkpụrụokwu_SMS(hàzie_valuu, "(C)Ljava/lang/StringBuilder;")) {
                    int valuu = 빼기(1); SMS = kepụta_Nchekwa(1, 1); if (!mmejọ) 힙[SMS + 2] = valuu & 65535;
                }
                else if (Mkpụrụokwu_SMS(hàzie_valuu, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { SMS = 빼기(2); if (SMS == 0) SMS = usu_mkpụrụedemede("null"); }
                else { ọdịdà_valuu("unsupported StringBuilder append"); return; }
                int Nrụtụ_aka = 빼기(2); if (!ihe_valuu(Nrụtụ_aka, 4) || !ihe_valuu(SMS, 1)) return;
                int 앞 = 힙[Nrụtụ_aka + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Àzụ_valuu_ogologo = 힙[SMS + 1];
                int 새글 = kepụta_Nchekwa(1, 앞길이 + Àzụ_valuu_ogologo); if (mmejọ) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Àzụ_valuu_ogologo; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[SMS + 2 + 수];
                힙[Nrụtụ_aka + 2] = 새글; 넣기(Nrụtụ_aka, 2); return;
            }
        }
        ọdịdà_valuu("unsupported library method");
    }
    static int MKPOKỌTA_oghere(int Nrụtụ_aka, int ntụkwàsa_n_akụkụ_n_àlà_valuu, int pinye_valuu) {
        if (!ihe_valuu(Nrụtụ_aka, pinye_valuu)) return 0;
        if (ntụkwàsa_n_akụkụ_n_àlà_valuu < 0 || ntụkwàsa_n_akụkụ_n_àlà_valuu >= 힙[Nrụtụ_aka + 1]) { ọdịdà_valuu("ArrayIndexOutOfBoundsException"); return 0; }
        return Nrụtụ_aka + 2 + ntụkwàsa_n_akụkụ_n_àlà_valuu;
    }
    static void mee_nnyemiwu() {
        int 남음 = 500000;
        while (okpokoro_indèks >= 0 && !mmejọ) {
            if (--남음 == 0) { ọdịdà_valuu("instruction limit (500000)"); break; }
            int Bido = 틀위치[okpokoro_indèks], valuu = 명바();
            if (mmejọ) break;
            if (valuu == 0) continue;
            if (valuu == 1) { 넣기(0, 2); continue; }
            if (valuu >= 2 && valuu <= 8) { 넣기(valuu - 3, 1); continue; }
            if (valuu == 16) { 넣기((byte)명바(), 1); continue; }
            if (valuu == 17) { 넣기((short)명짧(), 1); continue; }
            if (valuu == 18 || valuu == 19) {
                int 수 = valuu == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ọdịdà_valuu("invalid ldc constant");
                else if (ihendịgide_hụbaamā[수] == 3) 넣기(상가[수], 1);
                else if (ihendịgide_hụbaamā[수] == 8) 넣기(ihendịgide_SMS(상가[수]), 2);
                else ọdịdà_valuu("unsupported ldc constant");
                continue;
            }
            if (valuu == 21 || valuu == 25) { 지역읽기(명바(), valuu == 21 ? 1 : 2); continue; }
            if (valuu >= 26 && valuu <= 29) { 지역읽기(valuu - 26, 1); continue; }
            if (valuu >= 42 && valuu <= 45) { 지역읽기(valuu - 42, 2); continue; }
            if (valuu == 54 || valuu == 58) { dee_otù_ebe(명바(), valuu == 54 ? 1 : 2); continue; }
            if (valuu >= 59 && valuu <= 62) { dee_otù_ebe(valuu - 59, 1); continue; }
            if (valuu >= 75 && valuu <= 78) { dee_otù_ebe(valuu - 75, 2); continue; }
            if (valuu == 46 || valuu == 50) {
                int ntụkwàsa_n_akụkụ_n_àlà_valuu = 빼기(1), Nrụtụ_aka = 빼기(2), oghere_ndebà = MKPOKỌTA_oghere(Nrụtụ_aka, ntụkwàsa_n_akụkụ_n_àlà_valuu, valuu == 46 ? 2 : 3);
                if (!mmejọ) 넣기(힙[oghere_ndebà], valuu == 46 ? 1 : 2); continue;
            }
            if (valuu == 79 || valuu == 83) {
                int ihe_njìmebe = 빼기(valuu == 79 ? 1 : 2), ntụkwàsa_n_akụkụ_n_àlà_valuu = 빼기(1), Nrụtụ_aka = 빼기(2), oghere_ndebà = MKPOKỌTA_oghere(Nrụtụ_aka, ntụkwàsa_n_akụkụ_n_àlà_valuu, valuu == 79 ? 2 : 3);
                if (valuu == 83 && ihe_njìmebe != 0) ihe_valuu(ihe_njìmebe, 1);
                if (!mmejọ) 힙[oghere_ndebà] = ihe_njìmebe; continue;
            }
            if (valuu == 87) { 빼기(0); continue; }
            if (valuu == 89) { int 가 = 빼기(0), pinye_valuu = 반환형; 넣기(가, pinye_valuu); 넣기(가, pinye_valuu); continue; }
            if (valuu == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (valuu == 96 || valuu == 100 || valuu == 104 || valuu == 108 || valuu == 112 || valuu == 120
                || valuu == 122 || valuu == 124 || valuu == 126 || valuu == 128 || valuu == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((valuu == 108 || valuu == 112) && 나 == 0) { ọdịdà_valuu("ArithmeticException: / by zero"); continue; }
                if (valuu == 96) 결과 = 가 + 나;
                if (valuu == 100) 결과 = 가 - 나;
                if (valuu == 104) 결과 = 가 * 나;
                if (valuu == 108) 결과 = 가 / 나;
                if (valuu == 112) 결과 = 가 % 나;
                if (valuu == 120) 결과 = 가 << 나;
                if (valuu == 122) 결과 = 가 >> 나;
                if (valuu == 124) 결과 = 가 >>> 나;
                if (valuu == 126) 결과 = 가 & 나;
                if (valuu == 128) 결과 = 가 | 나;
                if (valuu == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (valuu == 116) { 넣기(-빼기(1), 1); continue; }
            if (valuu == 132) {
                int otù_ebe_ọgba = 명바(), 증분 = (byte)명바(); 지역읽기(otù_ebe_ọgba, 1); 넣기(빼기(1) + 증분, 1); dee_otù_ebe(otù_ebe_ọgba, 1); continue;
            }
            if (valuu >= 145 && valuu <= 147) {
                int 수 = 빼기(1); 넣기(valuu == 145 ? (byte)수 : valuu == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (valuu >= 153 && valuu <= 167 || valuu == 198 || valuu == 199) {
                int ebemwèga_valuu = Bido + (short)명짧(); boolean 갈까 = valuu == 167;
                if (valuu >= 153 && valuu <= 158) {
                    int 수 = 빼기(1); 갈까 = valuu == 153 ? 수 == 0 : valuu == 154 ? 수 != 0 : valuu == 155 ? 수 < 0 : valuu == 156 ? 수 >= 0 : valuu == 157 ? 수 > 0 : 수 <= 0;
                } else if (valuu >= 159 && valuu <= 166) {
                    int 나 = 빼기(valuu >= 165 ? 2 : 1), 가 = 빼기(valuu >= 165 ? 2 : 1);
                    갈까 = valuu == 159 || valuu == 165 ? 가 == 나 : valuu == 160 || valuu == 166 ? 가 != 나 : valuu == 161 ? 가 < 나 : valuu == 162 ? 가 >= 나 : valuu == 163 ? 가 > 나 : 가 <= 나;
                } else if (valuu == 198 || valuu == 199) { int 수 = 빼기(2); 갈까 = valuu == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) gàa_valuu(ebemwèga_valuu); continue;
            }
            if (valuu == 172 || valuu == 176 || valuu == 177) { 반환(valuu == 172 ? 1 : valuu == 176 ? 2 : 0); continue; }
            if (valuu == 178) {
                int 수 = 명짧(); if (!cheèk_ihendịgide(수, 9)) continue;
                if (!Mkpụrụokwu_SMS(klaàsị_akara_ahà_SMS(상가[수]), "java/lang/System") || !Mkpụrụokwu_SMS(Nrụtụ_aka_akara_ahà(상나[수]), "out")
                    || !Mkpụrụokwu_SMS(Nrụtụ_aka_pinye(상나[수]), "Ljava/io/PrintStream;")) ọdịdà_valuu("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (valuu == 182 || valuu == 183 || valuu == 184) { oku_usoro(명짧(), valuu); continue; }
            if (valuu == 187) {
                int Aha = klaàsị_akara_ahà_SMS(명짧());
                if (Mkpụrụokwu_SMS(Aha, "java/lang/StringBuilder")) 넣기(kepụta_Nchekwa(4, 1), 2);
                else if (Mkpụrụokwu_SMS(Aha, "java/io/FileInputStream") || Mkpụrụokwu_SMS(Aha, "java/io/FileOutputStream")) {
                    int Nrụtụ_aka = kepụta_Nchekwa(Mkpụrụokwu_SMS(Aha, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!mmejọ) { 힙[Nrụtụ_aka + 2] = -1; 넣기(Nrụtụ_aka, 2); }
                } else ọdịdà_valuu("unsupported object construction");
                continue;
            }
            if (valuu == 188 || valuu == 189) {
                if (valuu == 188) { if (명바() != 10) ọdịdà_valuu("only int[] newarray is supported"); }
                else if (!Mkpụrụokwu_SMS(klaàsị_akara_ahà_SMS(명짧()), "java/lang/String")) ọdịdà_valuu("only String[] anewarray is supported");
                int ogologo_valuu = 빼기(1); 넣기(kepụta_Nchekwa(valuu == 188 ? 2 : 3, ogologo_valuu), 2); continue;
            }
            if (valuu == 190) {
                int Nrụtụ_aka = 빼기(2);
                if (Nrụtụ_aka < 1 || Nrụtụ_aka >= 힙끝 - 1 || (힙[Nrụtụ_aka] != 2 && 힙[Nrụtụ_aka] != 3)) ọdịdà_valuu("null or invalid array");
                else 넣기(힙[Nrụtụ_aka + 1], 1); continue;
            }
            if (valuu == 192) {
                int Aha = klaàsị_akara_ahà_SMS(명짧()), Nrụtụ_aka = 빼기(2);
                if (!Mkpụrụokwu_SMS(Aha, "java/lang/String")) ọdịdà_valuu("unsupported checkcast");
                else if (Nrụtụ_aka != 0) ihe_valuu(Nrụtụ_aka, 1);
                넣기(Nrụtụ_aka, 2); continue;
            }
            ọdịdà_valuu("unsupported bytecode");
        }
    }
    public static int Bido() {
        if (òjìàrụ.인수개수() == 1 && 자바도구.같음(òjìàrụ.인수(0), "-version")) {
            òjìàrụ.Chekwaa_ozi("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (òjìàrụ.인수개수() < 1) { òjìàrụ.Chekwaa_ozi("Usage: java CLASS [ARGS]\n"); return 2; }
        int ogologo_valuu = 자바도구.Aha(ọbọakwụkwọ_akara_ahà_SMS, òjìàrụ.인수(0));
        if (ogologo_valuu < 1 || ogologo_valuu > 57) { òjìàrụ.Chekwaa_ozi("java: invalid class name\n"); return 2; }
        ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu] = '.'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 1] = 'c'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 2] = 'l'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 3] = 'a'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 4] = 's'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 5] = 's';
        Ụhara = òjìàrụ.파일읽기(ọbọakwụkwọ_akara_ahà_SMS, Faịlụ);
        if (Ụhara < 0) { òjìàrụ.Chekwaa_ozi("java: cannot read class: "); 자바도구.수쓰기(Ụhara); òjìàrụ.dee_mkpụrụedemede_valuu(10); return 1; }
        클래스읽기(); if (mmejọ) return 1;
        int mkpụrụedemede_akara_ahà = ihendịgide_SMS(klaàsị_akara_ahà);
        if (!mmejọ && 힙[mkpụrụedemede_akara_ahà + 1] != ogologo_valuu) ọdịdà_valuu("class name does not match file");
        for (int 수 = 0; 수 < ogologo_valuu && !mmejọ; 수++) if (힙[mkpụrụedemede_akara_ahà + 2 + 수] != ọbọakwụkwọ_akara_ahà_SMS[수]) ọdịdà_valuu("class name does not match file");
        int ndebà_akara_valuu = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Mkpụrụokwu_SMS(usoro_akara_ahà_SMS[수], "main") && Mkpụrụokwu_SMS(usoro_pinye[수], "([Ljava/lang/String;)V") && (usoro_òhèrè[수] & 9) == 9) ndebà_akara_valuu = 수;
        if (ndebà_akara_valuu < 0) ọdịdà_valuu("public static void main(String[] args) required");
        if (mmejọ) return 1;
        int 인수 = kepụta_Nchekwa(3, òjìàrụ.인수개수() - 1);
        for (int 수 = 1; 수 < òjìàrụ.인수개수() && !mmejọ; 수++) 힙[인수 + 1 + 수] = usu_mkpụrụedemede(òjìàrụ.인수(수));
        okpokoro_indèks = 0; okpokoro_usoro[0] = ndebà_akara_valuu; 틀위치[0] = usoro_Mbido[ndebà_akara_valuu]; otù_ebe_valuu[0] = 인수; otù_ebe_pinye[0] = 2;
        mee_nnyemiwu(); return mmejọ ? 1 : 0;
    }
}
