// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. Faịlụ/스택/Nrụtụ_aka/ogbè 경계를 mee_nnyemiwu 중 검사한다. */
public final class 자바가상기계 {
    static int[] Faịlụ = new int[16 * 16384], 임시파일 = new int[16384], ọbọakwụkwọ_akara_ahà_SMS = new int[512];
    static int[] ihendịgide_hụbaamā = new int[8192], 상가 = new int[8192], 상나 = new int[8192], ùsòròokwū_Nrụtụ_aka = new int[8192];
    static int[] usoro_akara_ahà_SMS = new int[512], usoro_pinye = new int[512], usoro_òhèrè = new int[512], usoro_nwe = new int[512];
    static int[] usoro_Mbido = new int[512], usoro_mèdebe = new int[512], usoro_ikpo = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], usoro_agụment_pinye = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] otù_ebe_valuu = new int[16384], otù_ebe_pinye = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] okpokoro_usoro = new int[128], 틀위치 = new int[128], okpokoro_ikpo = new int[128], okpokoro_okwunkụzi = new int[128], kwàdo_mmàlite_okpokoro = new int[128];
    static int[] klaàsị_Nkwuke_akara_ahà = new int[16], klaàsị_Nkwuke_ụha = new int[16], 종부모 = new int[16], klaàsị_Nkwuke_ọnọdụ = new int[16], 종칸수 = new int[16], kwàdo_mmàlite_klaàsị_Nkwuke = new int[16];
    static int[] klaàsị_ihuọrụ = new int[16 * 16], 종접면수 = new int[16];
    static int[] oghere_akara_ahà = new int[512], oghere_pinye = new int[512], oghere_nwe = new int[512], oghere_Òhèrèikike = new int[512], 칸위치 = new int[512], oghere_datà = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], MKPOKỌTA_njìmebe = new int[32768], Store_ọnụọgụ_nzùrùòkè = new int[256];
    static int Ụhara, 읽기위치, 함수수, klaàsị_akara_ahà, okpokoro_indèks = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, ndebà_klaàsị_Nkwuke;
    static int[] treèd_okpokoro = new int[4], treèd_ọnọdụ = new int[4], treèd_ihe = new int[4], treèd_ebenlereanya = new int[4], 가닥대기 = new int[4];
    static boolean mmejọ, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], klaàsị_treèd = new int[16];

    static void ọdịdà_valuu(String Mkpụrụokwu_SMS) {
        if (mmejọ) return;
        int 분류코드 = 0;
        if (자바도구.같음(Mkpụrụokwu_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Mkpụrụokwu_SMS, "NullPointerException") || 자바도구.같음(Mkpụrụokwu_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Mkpụrụokwu_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Mkpụrụokwu_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Mkpụrụokwu_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Mkpụrụokwu_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Mkpụrụokwu_SMS, "IOException: stream closed") || 자바도구.같음(Mkpụrụokwu_SMS, "IOException: read failed") || 자바도구.같음(Mkpụrụokwu_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Mkpụrụokwu_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Mkpụrụokwu_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && okpokoro_indèks >= 0) { 예외던짐(분류코드, Mkpụrụokwu_SMS); return; }
        òjìàrụ.Chekwaa_ozi("JVM error: "); òjìàrụ.Chekwaa_ozi(Mkpụrụokwu_SMS); òjìàrụ.dee_mkpụrụedemede_valuu(10); mmejọ = true;
    }
    static boolean ntipanye(int Bido, int ogologo_valuu) {
        if (Bido < 0 || Bido >= Faịlụ.length || ogologo_valuu < 0) return false;
        int klaàsị_Nkwuke = Bido / 16384;
        return Bido % 16384 <= klaàsị_Nkwuke_ụha[klaàsị_Nkwuke] && ogologo_valuu <= klaàsị_Nkwuke_ụha[klaàsị_Nkwuke] - Bido % 16384;
    }
    static int baịtị_valuu() {
        if (!ntipanye(읽기위치, 1)) { ọdịdà_valuu("truncated class file"); return 0; }
        return Faịlụ[읽기위치++];
    }
    static int 짧은수() { return baịtị_valuu() << 8 | baịtị_valuu(); }
    static int ọnụọgụ_nzùrùòkè() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ogologo_valuu) { if (!ntipanye(읽기위치, ogologo_valuu)) ọdịdà_valuu("invalid attribute size"); else 읽기위치 += ogologo_valuu; }
    static boolean cheèk_ihendịgide(int 수, int 종류) {
        if (수 <= 0 || 수 >= ihendịgide_hụbaamā.length || ihendịgide_hụbaamā[수] != 종류) { ọdịdà_valuu("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Bido, int ogologo_valuu, String Mkpụrụokwu_SMS) {
        if (!ntipanye(Bido, ogologo_valuu)) return false;
        int 읽는자리 = Bido, 끝 = Bido + ogologo_valuu;
        for (int memmenwè_indèks = 0; memmenwè_indèks < Mkpụrụokwu_SMS.length(); memmenwè_indèks++) {
            int koòdù_nkeakàrà = Mkpụrụokwu_SMS.charAt(memmenwè_indèks);
            if (koòdù_nkeakàrà > 0 && koòdù_nkeakàrà < 128) { if (읽는자리 >= 끝 || Faịlụ[읽는자리++] != koòdù_nkeakàrà) return false; }
            else if (koòdù_nkeakàrà < 2048) {
                if (읽는자리 + 2 > 끝 || Faịlụ[읽는자리++] != (192 | (koòdù_nkeakàrà >> 6)) || Faịlụ[읽는자리++] != (128 | (koòdù_nkeakàrà & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || Faịlụ[읽는자리++] != (224 | (koòdù_nkeakàrà >> 12)) || Faịlụ[읽는자리++] != (128 | ((koòdù_nkeakàrà >> 6) & 63)) || Faịlụ[읽는자리++] != (128 | (koòdù_nkeakàrà & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int valuu = 짧은수(); return valuu == 0 ? 0 : 현재읽는종 * 512 + valuu; }
    static int 명상수() { return usoro_nwe[okpokoro_usoro[okpokoro_indèks]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !mmejọ; 수++) { cheèk_ihendịgide(상번호(), 1); 건너(ọnụọgụ_nzùrùòkè()); }
    }
    static int nnyemiwu_ogologo(int valuu) {
        if (valuu == 16 || valuu == 18 || valuu == 21 || valuu == 25 || valuu == 54 || valuu == 58 || valuu == 188) return 2;
        if (valuu == 17 || valuu == 19 || valuu == 132 || valuu >= 153 && valuu <= 167
            || valuu >= 178 && valuu <= 184 || valuu == 187 || valuu == 189 || valuu == 192 || valuu == 193 || valuu == 198 || valuu == 199) return 3;
        if (valuu == 185 || valuu == 200) return 5;
        if (valuu >= 0 && valuu <= 8 || valuu >= 26 && valuu <= 29 || valuu >= 42 && valuu <= 46 || valuu >= 50 && valuu <= 53
            || valuu >= 59 && valuu <= 62 || valuu >= 75 && valuu <= 79 || valuu >= 83 && valuu <= 95
            || valuu == 96 || valuu == 100 || valuu == 104 || valuu == 108 || valuu == 112 || valuu == 116
            || valuu == 120 || valuu == 122 || valuu == 124 || valuu == 126 || valuu == 128 || valuu == 130
            || valuu >= 145 && valuu <= 147 || valuu == 172 || valuu == 176 || valuu == 177 || valuu == 190 || valuu == 191
            || valuu == 194 || valuu == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!ntipanye(읽는자리, 4)) { ọdịdà_valuu("truncated bytecode operand"); return 0; }
        return Faịlụ[읽는자리] << 24 | Faịlụ[읽는자리 + 1] << 16 | Faịlụ[읽는자리 + 2] << 8 | Faịlụ[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Bido, int 끝) {
        int valuu = Faịlụ[읽는자리], ogologo_valuu = nnyemiwu_ogologo(valuu);
        if (valuu == 170 || valuu == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Bido) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (valuu == 170 ? 12 : 8)) return 0;
            int 항목수 = valuu == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            ogologo_valuu = 기준자리 - 읽는자리 + (valuu == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (valuu == 196 && 읽는자리 + 1 < 끝) {
            int Mkpụrụokwu_datà = Faịlụ[읽는자리 + 1]; ogologo_valuu = Mkpụrụokwu_datà == 132 ? 6 : (Mkpụrụokwu_datà == 21 || Mkpụrụokwu_datà == 25 || Mkpụrụokwu_datà == 54 || Mkpụrụokwu_datà == 58) ? 4 : 0;
        }
        return ogologo_valuu > 0 && ogologo_valuu <= 끝 - 읽는자리 ? ogologo_valuu : 0;
    }
    static void cheèk_ebemwèga_valuu(int ebemwèga_valuu, int ọrụ_valuu) {
        if (ebemwèga_valuu < usoro_Mbido[ọrụ_valuu] || ebemwèga_valuu >= usoro_mèdebe[ọrụ_valuu] || 경계[ebemwèga_valuu] != ọrụ_valuu + 1) ọdịdà_valuu("invalid branch target");
    }
    static void 클래스읽기(int klaàsị_Nkwuke) {
        현재읽는종 = klaàsị_Nkwuke; 읽기위치 = klaàsị_Nkwuke * 16384; Ụhara = 읽기위치 + klaàsị_Nkwuke_ụha[klaàsị_Nkwuke];
        if (ọnụọgụ_nzùrùòkè() != 0xcafebabe) { ọdịdà_valuu("not a class file"); return; }
        int 부판 = 짧은수(), ụdị_valuu = 짧은수();
        if (ụdị_valuu < 45 || ụdị_valuu > 52 || 부판 != 0) { ọdịdà_valuu("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = klaàsị_Nkwuke * 512;
        if (상수수 < 1 || 상수수 > 512) { ọdịdà_valuu("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !mmejọ; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = baịtị_valuu(); ihendịgide_hụbaamā[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = ọnụọgụ_nzùrùòkè();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ọdịdà_valuu("unsupported constant type");
        }
        int ikikere_valuu = 짧은수();
        if ((ikikere_valuu & (0x2000 | 0x4000)) != 0) ọdịdà_valuu("annotation/enum class unsupported");
        klaàsị_Nkwuke_akara_ahà[klaàsị_Nkwuke] = klaàsị_akara_ahà_SMS(상번호());
        종부모[klaàsị_Nkwuke] = klaàsị_akara_ahà_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ọdịdà_valuu("interface count limit"); return; }
        종접면수[klaàsị_Nkwuke] = 접면수;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 접면수; memmenwè_indèks++) klaàsị_ihuọrụ[klaàsị_Nkwuke * 16 + memmenwè_indèks] = klaàsị_akara_ahà_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ọdịdà_valuu("field count limit (512)"); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 필드수 && !mmejọ; memmenwè_indèks++) {
            int ọbọakwụkwọ_indèks = 칸수++; oghere_nwe[ọbọakwụkwọ_indèks] = klaàsị_Nkwuke; oghere_Òhèrèikike[ọbọakwụkwọ_indèks] = 짧은수(); oghere_akara_ahà[ọbọakwụkwọ_indèks] = 상번호(); oghere_pinye[ọbọakwụkwọ_indèks] = 상번호();
            cheèk_ihendịgide(oghere_akara_ahà[ọbọakwụkwọ_indèks], 1); cheèk_ihendịgide(oghere_pinye[ọbọakwụkwọ_indèks], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[oghere_pinye[ọbọakwụkwọ_indèks]]; int 분류코드 = 서술형(읽기위치 + 상나[oghere_pinye[ọbọakwụkwọ_indèks]], false); 읽기위치 = 보존값;
            if ((oghere_Òhèrèikike[ọbọakwụkwọ_indèks] & 8) == 0) 칸위치[ọbọakwụkwọ_indèks] = 종칸수[klaàsị_Nkwuke]++;
            int njìama_datà = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < njìama_datà && !mmejọ; 안쪽자리++) {
                int akara_ahà_ihendịgide = 상번호(), 유효길이 = ọnụọgụ_nzùrùòkè();
                if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "ConstantValue") && 유효길이 == 2) {
                    int datà_valuu = 상번호();
                    if (분류코드 == 1 && cheèk_ihendịgide(datà_valuu, 3)) oghere_datà[ọbọakwụkwọ_indèks] = 상가[datà_valuu];
                    else if (분류코드 == 2 && cheèk_ihendịgide(datà_valuu, 8)) oghere_datà[ọbọakwụkwọ_indèks] = ihendịgide_SMS(상가[datà_valuu]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ọdịdà_valuu("method count limit (512)"); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 개수 && !mmejọ; memmenwè_indèks++) {
            int 수 = 함수수++; usoro_nwe[수] = klaàsị_Nkwuke;
            usoro_òhèrè[수] = 짧은수(); usoro_akara_ahà_SMS[수] = 상번호(); usoro_pinye[수] = 상번호();
            cheèk_ihendịgide(usoro_akara_ahà_SMS[수], 1); 서술읽기(수);
            if ((usoro_òhèrè[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ọdịdà_valuu("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) usoro_agụment_pinye[수 * 16 + 비교자리] = usoro_agụment_pinye[수 * 16 + 비교자리 - 1];
                usoro_agụment_pinye[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((usoro_òhèrè[수] & 0x100) != 0) ọdịdà_valuu("user native method unsupported");
            if (Mkpụrụokwu_SMS(usoro_akara_ahà_SMS[수], "<clinit>")) kwàdo_mmàlite_klaàsị_Nkwuke[klaàsị_Nkwuke] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (usoro_nwe[앞] == klaàsị_Nkwuke && 같은말(usoro_akara_ahà_SMS[앞], usoro_akara_ahà_SMS[수]) && 같은말(usoro_pinye[앞], usoro_pinye[수])) ọdịdà_valuu("duplicate method");
            int 속성수 = 짧은수();
            for (int njìama_valuu = 0; njìama_valuu < 속성수 && !mmejọ; njìama_valuu++) {
                int Aha = 상번호(), ogologo_valuu = ọnụọgụ_nzùrùòkè(), Bido = 읽기위치;
                if (!ntipanye(Bido, ogologo_valuu)) { ọdịdà_valuu("truncated method attribute"); break; }
                if (Mkpụrụokwu_SMS(Aha, "Code")) {
                    if (usoro_Mbido[수] != 0) ọdịdà_valuu("duplicate Code attribute");
                    usoro_ikpo[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = ọnụọgụ_nzùrùòkè();
                    if (usoro_ikpo[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ọdịdà_valuu("method memory limits exceeded");
                    usoro_Mbido[수] = 읽기위치; 건너(코드길이); usoro_mèdebe[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ọdịdà_valuu("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int mmejọ_Nrụtụ_aka = 잡기수++; 잡기함수[mmejọ_Nrụtụ_aka] = 수;
                        잡기시작[mmejọ_Nrụtụ_aka] = usoro_Mbido[수] + 짧은수(); 잡기끝[mmejọ_Nrụtụ_aka] = usoro_Mbido[수] + 짧은수();
                        잡기위치[mmejọ_Nrụtụ_aka] = usoro_Mbido[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[mmejọ_Nrụtụ_aka] = 부호값 == 0 ? 0 : klaàsị_akara_ahà_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Bido + ogologo_valuu) ọdịdà_valuu("Code attribute size mismatch");
                } else 건너(ogologo_valuu);
            }
            if ((usoro_òhèrè[수] & 0x400) != 0) continue;
            if (usoro_Mbido[수] == 0) ọdịdà_valuu("missing Code attribute");
            int oghere_ndebà = usoro_Mbido[수];
            while (oghere_ndebà < usoro_mèdebe[수] && !mmejọ) {
                int ogologo_valuu = 길이읽기(oghere_ndebà, usoro_Mbido[수], usoro_mèdebe[수]);
                if (ogologo_valuu == 0) { ọdịdà_valuu("unsupported or truncated bytecode"); break; }
                경계[oghere_ndebà] = 수 + 1; oghere_ndebà += ogologo_valuu;
            }
            oghere_ndebà = usoro_Mbido[수];
            while (oghere_ndebà < usoro_mèdebe[수] && !mmejọ) {
                int valuu = Faịlụ[oghere_ndebà];
                if (valuu >= 153 && valuu <= 167 || valuu == 198 || valuu == 199) cheèk_ebemwèga_valuu(oghere_ndebà + (short)(Faịlụ[oghere_ndebà + 1] << 8 | Faịlụ[oghere_ndebà + 2]), 수);
                if (valuu == 200) cheèk_ebemwèga_valuu(oghere_ndebà + 위치정수(oghere_ndebà + 1), 수);
                if (valuu == 170 || valuu == 171) {
                    int 읽는자리 = oghere_ndebà + 1; while ((읽는자리 - usoro_Mbido[수]) % 4 != 0) 읽는자리++;
                    cheèk_ebemwèga_valuu(oghere_ndebà + 위치정수(읽는자리), 수);
                    int 항목수 = valuu == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += valuu == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) cheèk_ebemwèga_valuu(oghere_ndebà + 위치정수(읽는자리 + 안쪽자리 * (valuu == 170 ? 4 : 8) + (valuu == 170 ? 0 : 4)), 수);
                }
                oghere_ndebà += 길이읽기(oghere_ndebà, usoro_Mbido[수], usoro_mèdebe[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                cheèk_ebemwèga_valuu(잡기시작[안쪽자리], 수); cheèk_ebemwèga_valuu(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != usoro_mèdebe[수]) cheèk_ebemwèga_valuu(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ọdịdà_valuu("invalid exception range");
            }
        }
        if (!mmejọ) 속성건너();
        if (읽기위치 != Ụhara) ọdịdà_valuu("extra class file data");
    }
    static int kepụta_Nchekwa(int 종류, int ogologo_valuu) { return 새기억(종류, ogologo_valuu); }
    static boolean ihe_valuu(int Nrụtụ_aka, int 종류) {
        if (!객체유효(Nrụtụ_aka)) return false;
        if (힙[Nrụtụ_aka] != 종류) { ọdịdà_valuu("object type mismatch"); return false; }
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
        if (반환형 == 2) nchedo_valuu(스택값[oghere_ndebà]);
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
        if (okpokoro_indèks % 32 == 31) { ọdịdà_valuu("call stack limit (32)"); return; }
        int 다음 = okpokoro_indèks + 1;
        for (int 수 = 0; 수 < 128; 수++) otù_ebe_pinye[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[ọrụ_valuu] - 1; 수 >= 0; 수--) {
            otù_ebe_valuu[다음 * 128 + 수] = 빼기(usoro_agụment_pinye[ọrụ_valuu * 16 + 수]); otù_ebe_pinye[다음 * 128 + 수] = usoro_agụment_pinye[ọrụ_valuu * 16 + 수];
        }
        if (mmejọ) return;
        okpokoro_indèks = 다음; kwàdo_mmàlite_okpokoro[okpokoro_indèks] = 0; okpokoro_usoro[okpokoro_indèks] = ọrụ_valuu; 틀위치[okpokoro_indèks] = usoro_Mbido[ọrụ_valuu]; okpokoro_ikpo[okpokoro_indèks] = 0;
    }
    static void 반환(int pinye_valuu) {
        if (pinye_valuu != 함수반환[okpokoro_usoro[okpokoro_indèks]]) { ọdịdà_valuu("return type mismatch"); return; }
        int valuu = pinye_valuu == 0 ? 0 : 빼기(pinye_valuu);
        if (kwàdo_mmàlite_okpokoro[okpokoro_indèks] != 0) klaàsị_Nkwuke_ọnọdụ[kwàdo_mmàlite_okpokoro[okpokoro_indèks] - 1] = 2;
        if (틀잠금[okpokoro_indèks] != 0) { 잠금풀기(틀잠금[okpokoro_indèks]); 틀잠금[okpokoro_indèks] = 0; }
        okpokoro_indèks--; if (okpokoro_indèks >= 현재가닥 * 32 && pinye_valuu != 0) 넣기(valuu, pinye_valuu);
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
                if (valuu < 1) { ọdịdà_valuu("invalid file stream path"); return; }
                agịrị_ọbọakwụkwọ_akara_ahà[oghere_ndebà] = valuu;
            }
            agịrị_ọbọakwụkwọ_akara_ahà[ogologo_valuu] = 0;
            int 서술자 = òjìàrụ.파일서술자열기(agịrị_ọbọakwụkwọ_akara_ahà, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ọdịdà_valuu("FileNotFoundException: file open failed"); return; }
            힙[agịrị_valuu + 2] = 서술자; 힙[agịrị_valuu + 3] = 1;
            return;
        }
        if (Ntiiwu != 182) { ọdịdà_valuu("invalid file stream invocation"); return; }
        if ((출력 && Mkpụrụokwu_SMS(Aha, "write") || !출력 && Mkpụrụokwu_SMS(Aha, "read"))
            && (Mkpụrụokwu_SMS(hàzie_valuu, 출력 ? "([B)V" : "([B)I") || Mkpụrụokwu_SMS(hàzie_valuu, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean ntipanye_valuu = Mkpụrụokwu_SMS(hàzie_valuu, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = ntipanye_valuu ? 빼기(1) : 0, 시작점 = ntipanye_valuu ? 빼기(1) : 0, datà_MKPOKỌTA = 빼기(2), ihe_Nrụtụ_aka = 빼기(2);
            if (!ihe_valuu(datà_MKPOKỌTA, 20) || !ihe_valuu(ihe_Nrụtụ_aka, 종류)) return;
            if (!ntipanye_valuu) 항목수 = 힙[datà_MKPOKỌTA + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[datà_MKPOKỌTA + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[ihe_Nrụtụ_aka + 3] == 0 || 힙[ihe_Nrụtụ_aka + 2] < 0) { ọdịdà_valuu("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !mmejọ) {
                int 반환값 = 출력 ? òjìàrụ.파일한바이트쓰기(힙[ihe_Nrụtụ_aka + 2], 힙[datà_MKPOKỌTA + 2 + 시작점 + 완료수]) : òjìàrụ.파일한바이트읽기(힙[ihe_Nrụtụ_aka + 2]);
                if (반환값 < 0) { ọdịdà_valuu(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[datà_MKPOKỌTA + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Mkpụrụokwu_SMS(Aha, "flush") && Mkpụrụokwu_SMS(hàzie_valuu, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 종류) && 힙[ihe_Nrụtụ_aka + 2] < 0) ọdịdà_valuu("IOException: stream closed"); return; }
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
            if (결과 < -1) ọdịdà_valuu("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (òjìàrụ.파일한바이트쓰기(서술자, valuu) != 1) ọdịdà_valuu("IOException: write failed");
    }
    static void oku_usoro(int indèks, int Ntiiwu) {
        if (indèks <= 0 || indèks >= ihendịgide_hụbaamā.length || (ihendịgide_hụbaamā[indèks] != 10 && ihendịgide_hụbaamā[indèks] != 11)) { ọdịdà_valuu("invalid method reference"); return; }
        int nwe_valuu = klaàsị_akara_ahà_SMS(상가[indèks]), Aha = Nrụtụ_aka_akara_ahà(상나[indèks]), hàzie_valuu = Nrụtụ_aka_pinye(상나[indèks]);
        if (mmejọ) return;
        if (기본호출(nwe_valuu, Aha, hàzie_valuu, Ntiiwu)) return;
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
        int klaàsị_Nkwuke = chọta_klaàsị_Nkwuke(nwe_valuu); if (klaàsị_Nkwuke < 0 || mmejọ) return;
        int ọbọakwụkwọ_indèks = chọta_usoro(klaàsị_Nkwuke, Aha, hàzie_valuu);
        if (ọbọakwụkwọ_indèks < 0) {
            for (int koòdù_nkeakàrà = klaàsị_Nkwuke, 항목수 = 0; koòdù_nkeakàrà >= 0 && 항목수 < 16; 항목수++, koòdù_nkeakàrà = 부모종(koòdù_nkeakàrà))
                if (Mkpụrụokwu_SMS(종부모[koòdù_nkeakàrà], "java/lang/Thread")) { 가닥호출(Aha, hàzie_valuu, Ntiiwu); return; }
            ọdịdà_valuu("NoSuchMethodError"); return;
        }
        if (((usoro_òhèrè[ọbọakwụkwọ_indèks] & 8) != 0) != (Ntiiwu == 184)) { ọdịdà_valuu("method static/instance mismatch"); return; }
        if (Ntiiwu == 184) { if (!kwàdo_mmàlite(usoro_nwe[ọbọakwụkwọ_indèks], okpokoro_okwunkụzi[okpokoro_indèks])) return; }
        else {
            int 읽는자리 = okpokoro_ikpo[okpokoro_indèks] - 함수인수수[ọbọakwụkwọ_indèks];
            if (읽는자리 < 0 || 스택형[okpokoro_indèks * 128 + 읽는자리] != 2) { ọdịdà_valuu("invalid method receiver"); return; }
            int ihe_Nrụtụ_aka = 스택값[okpokoro_indèks * 128 + 읽는자리];
            if (!객체유효(ihe_Nrụtụ_aka)) return;
            if (힙[ihe_Nrụtụ_aka] < 32 || !종포함(힙[ihe_Nrụtụ_aka] - 32, nwe_valuu)) { ọdịdà_valuu("method receiver type mismatch"); return; }
            if (Ntiiwu != 183) ọbọakwụkwọ_indèks = chọta_usoro(힙[ihe_Nrụtụ_aka] - 32, Aha, hàzie_valuu);
        }
        if (ọbọakwụkwọ_indèks < 0 || (usoro_òhèrè[ọbọakwụkwọ_indèks] & 0x400) != 0) { ọdịdà_valuu("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((usoro_òhèrè[ọbọakwụkwọ_indèks] & 32) != 0) {
            if (Ntiiwu == 184) { int koòdù_nkeakàrà = usoro_nwe[ọbọakwụkwọ_indèks]; if (종잠금[koòdù_nkeakàrà] == 0) 종잠금[koòdù_nkeakàrà] = kepụta_Nchekwa(8, 0); 잠금참조 = 종잠금[koòdù_nkeakàrà]; }
            else 잠금참조 = 스택값[okpokoro_indèks * 128 + okpokoro_ikpo[okpokoro_indèks] - 함수인수수[ọbọakwụkwọ_indèks]];
            if (!잠금얻기(잠금참조)) { if (!mmejọ) 틀위치[okpokoro_indèks] = okpokoro_okwunkụzi[okpokoro_indèks]; return; }
        }
        호출(ọbọakwụkwọ_indèks); if (!mmejọ) 틀잠금[okpokoro_indèks] = 잠금참조;
    }
    static boolean 배열저장가능(int MKPOKỌTA_Nrụtụ_aka, int datà_valuu) {
        if (datà_valuu == 0 || MKPOKỌTA_njìmebe[MKPOKỌTA_Nrụtụ_aka] == 0) return true;
        boolean 성공여부 = MKPOKỌTA_njìmebe[MKPOKỌTA_Nrụtụ_aka] == -1 ? (datà_valuu > 0 && datà_valuu < 힙끝 && 힙[datà_valuu] == 1) : 맞는객체(datà_valuu, MKPOKỌTA_njìmebe[MKPOKỌTA_Nrụtụ_aka]);
        if (!성공여부 && !mmejọ) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int MKPOKỌTA_oghere(int Nrụtụ_aka, int ntụkwàsa_n_akụkụ_n_àlà_valuu, int pinye_valuu) {
        if (!ihe_valuu(Nrụtụ_aka, pinye_valuu)) return 0;
        if (ntụkwàsa_n_akụkụ_n_àlà_valuu < 0 || ntụkwàsa_n_akụkụ_n_àlà_valuu >= 힙[Nrụtụ_aka + 1]) { ọdịdà_valuu("ArrayIndexOutOfBoundsException"); return 0; }
        return Nrụtụ_aka + 2 + ntụkwàsa_n_akụkụ_n_àlà_valuu;
    }
    static void mee_nnyemiwu() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (mmejọ) { if (던진객체 != 0) 예외처리(); if (mmejọ || okpokoro_indèks < 현재가닥 * 32) break; }
            if (okpokoro_indèks < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!ngbanwụ_treèd()) break; 조각 = 100; }
            if (okpokoro_indèks == 0 && klaàsị_Nkwuke_ọnọdụ[ndebà_klaàsị_Nkwuke] != 2 && !kwàdo_mmàlite(ndebà_klaàsị_Nkwuke, 틀위치[okpokoro_indèks])) continue;
            if (okpokoro_indèks == 현재가닥 * 32 && 현재가닥 != 0 && (usoro_òhèrè[okpokoro_usoro[okpokoro_indèks]] & 32) != 0 && 틀잠금[okpokoro_indèks] == 0) {
                int ihe_Nrụtụ_aka = treèd_ebenlereanya[현재가닥]; if (!잠금얻기(ihe_Nrụtụ_aka)) { if (mmejọ) break; continue; } 틀잠금[okpokoro_indèks] = ihe_Nrụtụ_aka;
            }
            잠시수 = 0;
            if (--남음 == 0) { ọdịdà_valuu("instruction limit (500000)"); break; }
            int Bido = 틀위치[okpokoro_indèks]; okpokoro_okwunkụzi[okpokoro_indèks] = Bido; int valuu = 명바();
            if (mmejọ) break;
            if (valuu == 0) continue;
            if (valuu == 1) { 넣기(0, 2); continue; }
            if (valuu >= 2 && valuu <= 8) { 넣기(valuu - 3, 1); continue; }
            if (valuu == 16) { 넣기((byte)명바(), 1); continue; }
            if (valuu == 17) { 넣기((short)명짧(), 1); continue; }
            if (valuu == 18 || valuu == 19) {
                int 수 = usoro_nwe[okpokoro_usoro[okpokoro_indèks]] * 512 + (valuu == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= ihendịgide_hụbaamā.length) ọdịdà_valuu("invalid ldc constant");
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
            if (valuu == 46 || valuu >= 50 && valuu <= 53) {
                int 항목자리 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2), 분류코드 = valuu == 46 ? 2 : valuu == 50 ? 3 : valuu == 51 ? 20 : valuu == 52 ? 22 : 23;
                if (valuu == 51 && ihe_Nrụtụ_aka > 0 && ihe_Nrụtụ_aka < 힙끝 && 힙[ihe_Nrụtụ_aka] == 21) 분류코드 = 21;
                int 읽는자리 = MKPOKỌTA_oghere(ihe_Nrụtụ_aka, 항목자리, 분류코드); if (!mmejọ) 넣기(힙[읽는자리], valuu == 50 ? 2 : 1); continue;
            }
            if (valuu == 79 || valuu >= 83 && valuu <= 86) {
                int ndebà_Nrụtụ_aka = 빼기(valuu == 83 ? 2 : 1), 항목자리 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2), 분류코드 = valuu == 79 ? 2 : valuu == 83 ? 3 : valuu == 84 ? 20 : valuu == 85 ? 22 : 23;
                if (valuu == 84 && ihe_Nrụtụ_aka > 0 && ihe_Nrụtụ_aka < 힙끝 && 힙[ihe_Nrụtụ_aka] == 21) 분류코드 = 21;
                int 읽는자리 = MKPOKỌTA_oghere(ihe_Nrụtụ_aka, 항목자리, 분류코드);
                if (!mmejọ && 분류코드 == 3 && !배열저장가능(ihe_Nrụtụ_aka, ndebà_Nrụtụ_aka)) continue;
                if (!mmejọ) 힙[읽는자리] = 분류코드 == 20 ? (byte)ndebà_Nrụtụ_aka : 분류코드 == 21 ? ndebà_Nrụtụ_aka & 1 : 분류코드 == 22 ? (char)ndebà_Nrụtụ_aka : 분류코드 == 23 ? (short)ndebà_Nrụtụ_aka : ndebà_Nrụtụ_aka;
                continue;
            }
            if (valuu >= 87 && valuu <= 95) { ikpo_okwunkụzi(valuu); continue; }
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
            if (valuu >= 178 && valuu <= 181) { 필드호출(명상수(), valuu, Bido); continue; }
            if (valuu >= 182 && valuu <= 185) {
                int 부호값 = 명상수();
                if (valuu == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ọdịdà_valuu("invalid invokeinterface operands"); continue; } }
                oku_usoro(부호값, valuu); continue;
            }
            if (valuu == 187) { 새객체(klaàsị_akara_ahà_SMS(명상수()), Bido); continue; }
            if (valuu == 188 || valuu == 189) {
                int 분류코드 = 3, ǹsòmebe = 0;
                if (valuu == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else ǹsòmebe = klaàsị_akara_ahà_SMS(명상수());
                if (분류코드 == 0) { ọdịdà_valuu("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), ihe_Nrụtụ_aka = kepụta_Nchekwa(분류코드, 유효길이); if (!mmejọ) MKPOKỌTA_njìmebe[ihe_Nrụtụ_aka] = ǹsòmebe; 넣기(ihe_Nrụtụ_aka, 2); continue;
            }
            if (valuu == 190) {
                int ihe_Nrụtụ_aka = 빼기(2);
                if (객체유효(ihe_Nrụtụ_aka)) { int 비교자리 = 힙[ihe_Nrụtụ_aka]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ọdịdà_valuu("not an array"); else 넣기(힙[ihe_Nrụtụ_aka + 1], 1); }
                continue;
            }
            if (valuu == 191) {
                int ihe_Nrụtụ_aka = 빼기(2); if (객체유효(ihe_Nrụtụ_aka)) { if (힙[ihe_Nrụtụ_aka] != 9) ọdịdà_valuu("athrow requires supported Throwable"); else { 던진객체 = ihe_Nrụtụ_aka; mmejọ = true; } }
                continue;
            }
            if (valuu == 192 || valuu == 193) {
                int akara_ahà_ihendịgide = klaàsị_akara_ahà_SMS(명상수()), ihe_Nrụtụ_aka = 빼기(2); boolean 일치여부 = 맞는객체(ihe_Nrụtụ_aka, akara_ahà_ihendịgide);
                if (valuu == 193) 넣기(ihe_Nrụtụ_aka != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !mmejọ) ọdịdà_valuu("ClassCastException"); 넣기(ihe_Nrụtụ_aka, 2); }
                continue;
            }
            if (valuu == 170 || valuu == 171) {
                int 읽는자리 = Bido + 1, ọbọakwụkwọ_indèks = okpokoro_usoro[okpokoro_indèks], ọtụgwo_Nrụtụ_aka = 빼기(1);
                while ((읽는자리 - usoro_Mbido[ọbọakwụkwọ_indèks]) % 4 != 0) 읽는자리++;
                int ebenlereanya_àdreèsì = 위치정수(읽는자리);
                if (valuu == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (ọtụgwo_Nrụtụ_aka >= 낮은값 && ọtụgwo_Nrụtụ_aka <= 높은값) ebenlereanya_àdreèsì = 위치정수(읽는자리 + 12 + (ọtụgwo_Nrụtụ_aka - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int memmenwè_indèks = 0; memmenwè_indèks < 총수; memmenwè_indèks++) if (위치정수(읽는자리 + 8 + memmenwè_indèks * 8) == ọtụgwo_Nrụtụ_aka) ebenlereanya_àdreèsì = 위치정수(읽는자리 + 12 + memmenwè_indèks * 8); }
                gàa_valuu(Bido + ebenlereanya_àdreèsì); continue;
            }
            if (valuu == 200) { gàa_valuu(Bido + 위치정수(Bido + 1)); continue; }
            if (valuu == 194 || valuu == 195) {
                int ihe_Nrụtụ_aka = 빼기(2);
                if (valuu == 195) 잠금풀기(ihe_Nrụtụ_aka);
                else if (!잠금얻기(ihe_Nrụtụ_aka) && !mmejọ) { 넣기(ihe_Nrụtụ_aka, 2); 틀위치[okpokoro_indèks] = Bido; }
                continue;
            }
            if (valuu == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) dee_otù_ebe(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); dee_otù_ebe(항목자리, 1); }
                else ọdịdà_valuu("unsupported wide opcode");
                continue;
            }
            ọdịdà_valuu("unsupported bytecode");
        }
    }
    static int chọta_klaàsị_Nkwuke(int Aha) {
        for (int memmenwè_indèks = 0; memmenwè_indèks < 종수; memmenwè_indèks++) if (klaàsị_Nkwuke_akara_ahà[memmenwè_indèks] != 0 && 같은말(klaàsị_Nkwuke_akara_ahà[memmenwè_indèks], Aha)) return memmenwè_indèks;
        return ibu_klaàsị_Nkwuke(ihendịgide_SMS(Aha));
    }
    static int ibu_klaàsị_Nkwuke(int akara_ahà_ùsòròokwū) {
        if (!ihe_valuu(akara_ahà_ùsòròokwū, 1)) return -1;
        int ogologo_valuu = 힙[akara_ahà_ùsòròokwū + 1];
        if (ogologo_valuu < 1 || ogologo_valuu > 505 || 종수 == 16) { ọdịdà_valuu("class name/count limit"); return -1; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < ogologo_valuu; memmenwè_indèks++) { int koòdù_nkeakàrà = 힙[akara_ahà_ùsòròokwū + 2 + memmenwè_indèks]; ọbọakwụkwọ_akara_ahà_SMS[memmenwè_indèks] = koòdù_nkeakàrà == '/' ? '.' : koòdù_nkeakàrà; }
        ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu] = '.'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 1] = 'c'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 2] = 'l'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 3] = 'a'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 4] = 's'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 5] = 's'; ọbọakwụkwọ_akara_ahà_SMS[ogologo_valuu + 6] = 0;
        int Ụhara = òjìàrụ.파일읽기(ọbọakwụkwọ_akara_ahà_SMS, 임시파일);
        if (Ụhara < 0) { ọdịdà_valuu("ClassNotFoundException"); return -1; }
        int klaàsị_Nkwuke = 종수++; klaàsị_Nkwuke_ụha[klaàsị_Nkwuke] = Ụhara;
        for (int memmenwè_indèks = 0; memmenwè_indèks < Ụhara; memmenwè_indèks++) Faịlụ[klaàsị_Nkwuke * 16384 + memmenwè_indèks] = 임시파일[memmenwè_indèks];
        클래스읽기(klaàsị_Nkwuke); if (mmejọ) return -1;
        int ǹdịnezie_datà = ihendịgide_SMS(klaàsị_Nkwuke_akara_ahà[klaàsị_Nkwuke]);
        if (!글같음(ǹdịnezie_datà, akara_ahà_ùsòròokwū, true)) { ọdịdà_valuu("class name does not match file"); return -1; }
        int 부모 = 종부모[klaàsị_Nkwuke];
        if (부모 != 0 && !Mkpụrụokwu_SMS(부모, "java/lang/Object") && !Mkpụrụokwu_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = chọta_klaàsị_Nkwuke(부모);
            if (mmejọ || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == klaàsị_Nkwuke) { ọdịdà_valuu("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int ọbọakwụkwọ_indèks = 0; ọbọakwụkwọ_indèks < 칸수; ọbọakwụkwọ_indèks++) if (oghere_nwe[ọbọakwụkwọ_indèks] == klaàsị_Nkwuke && (oghere_Òhèrèikike[ọbọakwụkwọ_indèks] & 8) == 0) 칸위치[ọbọakwụkwọ_indèks] += 시작변위;
            종칸수[klaàsị_Nkwuke] += 시작변위;
        }
        return klaàsị_Nkwuke;
    }
    static int 부모종(int klaàsị_Nkwuke) {
        int Aha = 종부모[klaàsị_Nkwuke];
        for (int memmenwè_indèks = 0; memmenwè_indèks < 종수; memmenwè_indèks++) if (Aha != 0 && klaàsị_Nkwuke_akara_ahà[memmenwè_indèks] != 0 && 같은말(klaàsị_Nkwuke_akara_ahà[memmenwè_indèks], Aha)) return memmenwè_indèks;
        return -1;
    }
    static int chọta_usoro(int klaàsị_Nkwuke, int Aha, int hàzie_valuu) {
        for (int 깊이 = 0; klaàsị_Nkwuke >= 0 && 깊이 < 16; 깊이++, klaàsị_Nkwuke = 부모종(klaàsị_Nkwuke)) {
            for (int memmenwè_indèks = 0; memmenwè_indèks < 함수수; memmenwè_indèks++) if (usoro_nwe[memmenwè_indèks] == klaàsị_Nkwuke && 같은말(usoro_akara_ahà_SMS[memmenwè_indèks], Aha) && 같은말(usoro_pinye[memmenwè_indèks], hàzie_valuu)) return memmenwè_indèks;
        }
        return -1;
    }
    static int akara_ahà_usoro(int klaàsị_Nkwuke, String Aha, String hàzie_valuu) {
        for (int 깊이 = 0; klaàsị_Nkwuke >= 0 && 깊이 < 16; 깊이++, klaàsị_Nkwuke = 부모종(klaàsị_Nkwuke))
            for (int memmenwè_indèks = 0; memmenwè_indèks < 함수수; memmenwè_indèks++) if (usoro_nwe[memmenwè_indèks] == klaàsị_Nkwuke && Mkpụrụokwu_SMS(usoro_akara_ahà_SMS[memmenwè_indèks], Aha) && Mkpụrụokwu_SMS(usoro_pinye[memmenwè_indèks], hàzie_valuu)) return memmenwè_indèks;
        return -1;
    }
    static int 형종류(int Aha) { return Faịlụ[상가[Aha]] == 'L' || Faịlụ[상가[Aha]] == '[' ? 2 : 1; }
    static boolean kwàdo_mmàlite(int klaàsị_Nkwuke, int nnyemiwu_Mbido) {
        if (klaàsị_Nkwuke < 0 || mmejọ) return false;
        if (klaàsị_Nkwuke_ọnọdụ[klaàsị_Nkwuke] == 3) { ọdịdà_valuu("NoClassDefFoundError: initialization failed"); return false; }
        if (klaàsị_Nkwuke_ọnọdụ[klaàsị_Nkwuke] == 1 && klaàsị_treèd[klaàsị_Nkwuke] != 현재가닥) { 틀위치[okpokoro_indèks] = nnyemiwu_Mbido; 바꿈요청 = true; return false; }
        if (klaàsị_Nkwuke_ọnọdụ[klaàsị_Nkwuke] != 0) return true;
        int 위 = 부모종(klaàsị_Nkwuke);
        if (위 >= 0 && !kwàdo_mmàlite(위, nnyemiwu_Mbido)) return false;
        klaàsị_Nkwuke_ọnọdụ[klaàsị_Nkwuke] = 1; klaàsị_treèd[klaàsị_Nkwuke] = 현재가닥;
        if (kwàdo_mmàlite_klaàsị_Nkwuke[klaàsị_Nkwuke] != 0) {
            틀위치[okpokoro_indèks] = nnyemiwu_Mbido;
            호출(kwàdo_mmàlite_klaàsị_Nkwuke[klaàsị_Nkwuke] - 1); if (!mmejọ) kwàdo_mmàlite_okpokoro[okpokoro_indèks] = klaàsị_Nkwuke + 1;
            return false;
        }
        klaàsị_Nkwuke_ọnọdụ[klaàsị_Nkwuke] = 2; return true;
    }
    static void 필드호출(int indèks, int Ntiiwu, int Bido) {
        if (!cheèk_ihendịgide(indèks, 9)) return;
        int nwe_valuu = klaàsị_akara_ahà_SMS(상가[indèks]), Aha = Nrụtụ_aka_akara_ahà(상나[indèks]), hàzie_valuu = Nrụtụ_aka_pinye(상나[indèks]);
        if (Mkpụrụokwu_SMS(nwe_valuu, "java/lang/System") && (Mkpụrụokwu_SMS(Aha, "out") || Mkpụrụokwu_SMS(Aha, "err")) && Mkpụrụokwu_SMS(hàzie_valuu, "Ljava/io/PrintStream;") && Ntiiwu == 178) { 넣기(-1, 2); return; }
        int klaàsị_Nkwuke = chọta_klaàsị_Nkwuke(nwe_valuu); if (klaàsị_Nkwuke < 0 || mmejọ) return;
        int 찾음 = -1;
        for (int 읽는자리 = klaàsị_Nkwuke, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int ọbọakwụkwọ_indèks = 0; ọbọakwụkwọ_indèks < 칸수; ọbọakwụkwọ_indèks++) if (oghere_nwe[ọbọakwụkwọ_indèks] == 읽는자리 && 같은말(oghere_akara_ahà[ọbọakwụkwọ_indèks], Aha) && 같은말(oghere_pinye[ọbọakwụkwọ_indèks], hàzie_valuu)) 찾음 = ọbọakwụkwọ_indèks;
        if (찾음 < 0) { ọdịdà_valuu("NoSuchFieldError"); return; }
        boolean adịmgbanwò_valuu = Ntiiwu == 178 || Ntiiwu == 179;
        if (adịmgbanwò_valuu != ((oghere_Òhèrèikike[찾음] & 8) != 0)) { ọdịdà_valuu("field static/instance mismatch"); return; }
        if (adịmgbanwò_valuu && !kwàdo_mmàlite(oghere_nwe[찾음], Bido)) return;
        int pinye_valuu = 형종류(hàzie_valuu), valuu = 0;
        if (Ntiiwu == 179 || Ntiiwu == 181) valuu = 빼기(pinye_valuu);
        if (adịmgbanwò_valuu) { if (Ntiiwu == 178) 넣기(oghere_datà[찾음], pinye_valuu); else if (!mmejọ) oghere_datà[찾음] = valuu; return; }
        int ihe_Nrụtụ_aka = 빼기(2);
        if (!객체유효(ihe_Nrụtụ_aka)) return;
        if (힙[ihe_Nrụtụ_aka] < 32 || !종포함(힙[ihe_Nrụtụ_aka] - 32, nwe_valuu)) { ọdịdà_valuu("field receiver type mismatch"); return; }
        int 보관칸 = ihe_Nrụtụ_aka + 2 + 칸위치[찾음];
        if (Ntiiwu == 180) 넣기(힙[보관칸], pinye_valuu);
        else if (!mmejọ) { 힙[보관칸] = valuu; 힙참조[보관칸] = pinye_valuu == 2 ? 1 : 0; }
    }
    static boolean 종포함(int klaàsị_Nkwuke, int Aha) {
        for (int 중첩깊이 = 0; klaàsị_Nkwuke >= 0 && 중첩깊이 < 16; 중첩깊이++, klaàsị_Nkwuke = 부모종(klaàsị_Nkwuke)) {
            if (같은말(klaàsị_Nkwuke_akara_ahà[klaàsị_Nkwuke], Aha) || (종부모[klaàsị_Nkwuke] != 0 && 같은말(종부모[klaàsị_Nkwuke], Aha))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[klaàsị_Nkwuke]; 안쪽자리++) if (같은말(klaàsị_ihuọrụ[klaàsị_Nkwuke * 16 + 안쪽자리], Aha)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int baịtị_datà, boolean ụzọ_ozi) {
        if (첫값 == baịtị_datà) return true;
        if (첫값 <= 0 || baịtị_datà <= 0 || 힙[첫값] != 1 || 힙[baịtị_datà] != 1 || 힙[첫값 + 1] != 힙[baịtị_datà + 1]) return false;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 힙[첫값 + 1]; memmenwè_indèks++) {
            int ngakọrịta_x = 힙[첫값 + 2 + memmenwè_indèks], 세로좌표 = 힙[baịtị_datà + 2 + memmenwè_indèks];
            if (ụzọ_ozi) { if (ngakọrịta_x == '.') ngakọrịta_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (ngakọrịta_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int ihe_Nrụtụ_aka) {
        if (ihe_Nrụtụ_aka == 0) { ọdịdà_valuu("NullPointerException"); return false; }
        if (ihe_Nrụtụ_aka < 1 || ihe_Nrụtụ_aka >= 힙끝 || 힙폭[ihe_Nrụtụ_aka] < 2 || 힙[ihe_Nrụtụ_aka] == 0) { ọdịdà_valuu("invalid object reference"); return false; }
        return true;
    }
    static void nchedo_valuu(int ihe_Nrụtụ_aka) {
        if (ihe_Nrụtụ_aka > 0 && ihe_Nrụtụ_aka < 힙끝 && 힙폭[ihe_Nrụtụ_aka] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = ihe_Nrụtụ_aka;
    }
    static void gòsi_valuu(int ihe_Nrụtụ_aka) {
        if (ihe_Nrụtụ_aka > 0 && ihe_Nrụtụ_aka < 힙끝 && 힙폭[ihe_Nrụtụ_aka] >= 2 && 힙[ihe_Nrụtụ_aka] != 0 && 힙표시[ihe_Nrụtụ_aka] == 0) {
            힙표시[ihe_Nrụtụ_aka] = 1; 표시대기[표시수++] = ihe_Nrụtụ_aka;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < ùsòròokwū_Nrụtụ_aka.length; memmenwè_indèks++) gòsi_valuu(ùsòròokwū_Nrụtụ_aka[memmenwè_indèks]);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 칸수; memmenwè_indèks++) if ((oghere_Òhèrèikike[memmenwè_indèks] & 8) != 0 && 형종류(oghere_pinye[memmenwè_indèks]) == 2) gòsi_valuu(oghere_datà[memmenwè_indèks]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            gòsi_valuu(treèd_ihe[임시값]); gòsi_valuu(treèd_ebenlereanya[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? okpokoro_indèks : treèd_okpokoro[임시값];
            for (int ọbọakwụkwọ_indèks = 임시값 * 32; ọbọakwụkwọ_indèks <= 꼭대기자리; ọbọakwụkwọ_indèks++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[okpokoro_usoro[ọbọakwụkwọ_indèks]]; 안쪽자리++) if (otù_ebe_pinye[ọbọakwụkwọ_indèks * 128 + 안쪽자리] == 2) gòsi_valuu(otù_ebe_valuu[ọbọakwụkwọ_indèks * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < okpokoro_ikpo[ọbọakwụkwọ_indèks]; 안쪽자리++) if (스택형[ọbọakwụkwọ_indèks * 128 + 안쪽자리] == 2) gòsi_valuu(스택값[ọbọakwụkwọ_indèks * 128 + 안쪽자리]);
            }
        }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 화면참조.length; memmenwè_indèks++) gòsi_valuu(화면참조[memmenwè_indèks]);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 나중수; memmenwè_indèks++) gòsi_valuu(나중실행[memmenwè_indèks]);
        for (int memmenwè_indèks = 0; memmenwè_indèks < Store_ọnụọgụ_nzùrùòkè.length; memmenwè_indèks++) gòsi_valuu(Store_ọnụọgụ_nzùrùòkè[memmenwè_indèks]);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 종수; memmenwè_indèks++) gòsi_valuu(종잠금[memmenwè_indèks]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) gòsi_valuu(검사자리);
        gòsi_valuu(던진객체);
        for (int memmenwè_indèks = 0; memmenwè_indèks < 잠시수; memmenwè_indèks++) gòsi_valuu(잠시참조[memmenwè_indèks]);
        while (표시수 > 0) {
            int ihe_Nrụtụ_aka = 표시대기[--표시수], 분류코드 = 힙[ihe_Nrụtụ_aka];
            for (int memmenwè_indèks = ihe_Nrụtụ_aka + 2; memmenwè_indèks < ihe_Nrụtụ_aka + 힙폭[ihe_Nrụtụ_aka]; memmenwè_indèks++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[memmenwè_indèks] != 0) gòsi_valuu(힙[memmenwè_indèks]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int ogologo_valuu) {
        if (ogologo_valuu < 0) { ọdịdà_valuu("NegativeArraySizeException"); return 0; }
        if (ogologo_valuu > 힙.length - 3) { ọdịdà_valuu("object heap exhausted"); return 0; }
        int 필요수 = ogologo_valuu + 2, ihe_Nrụtụ_aka = 0;
        if (필요수 <= 힙.length - 힙끝) { ihe_Nrụtụ_aka = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { ihe_Nrụtụ_aka = 읽는자리; break; }
            if (ihe_Nrụtụ_aka != 0) {
                int 남은길이 = 힙폭[ihe_Nrụtụ_aka] - 필요수;
                if (남은길이 >= 2) { 힙폭[ihe_Nrụtụ_aka + 필요수] = 남은길이; 힙[ihe_Nrụtụ_aka + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { ihe_Nrụtụ_aka = 힙끝; 힙끝 += 필요수; }
        }
        if (ihe_Nrụtụ_aka == 0) { ọdịdà_valuu("object heap exhausted"); return 0; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 필요수; memmenwè_indèks++) { 힙[ihe_Nrụtụ_aka + memmenwè_indèks] = 0; 힙참조[ihe_Nrụtụ_aka + memmenwè_indèks] = 0; 힙폭[ihe_Nrụtụ_aka + memmenwè_indèks] = 0; }
        MKPOKỌTA_njìmebe[ihe_Nrụtụ_aka] = 0;
        힙폭[ihe_Nrụtụ_aka] = 필요수; 힙[ihe_Nrụtụ_aka] = 종류; 힙[ihe_Nrụtụ_aka + 1] = ogologo_valuu; nchedo_valuu(ihe_Nrụtụ_aka); return ihe_Nrụtụ_aka;
    }
    static int 예외종(String akara_ahà_ihendịgide) {
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/Throwable")) return 1;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/Exception")) return 2;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/io/IOException")) return 11;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(akara_ahà_ihendịgide, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Aha) {
        for (int memmenwè_indèks = 1; memmenwè_indèks <= 41; memmenwè_indèks++) if (Mkpụrụokwu_SMS(Aha, 예외이름(memmenwè_indèks))) return memmenwè_indèks;
        return 0;
    }
    static String 예외이름(int akaụntụ_valuu) {
        if (akaụntụ_valuu == 40) return "java/lang/InterruptedException";
        if (akaụntụ_valuu == 41) return "한국어/자체/대기중단예외";
        if (akaụntụ_valuu == 39) return "java/net/SocketException";
        if (akaụntụ_valuu == 20) return "한국어/자체/예외";
        if (akaụntụ_valuu == 21) return "한국어/자체/실행예외";
        if (akaụntụ_valuu == 22) return "한국어/자체/입출력예외";
        if (akaụntụ_valuu == 23) return "한국어/자체/대기시간초과예외";
        if (akaụntụ_valuu == 24) return "한국어/자체/주소확인예외";
        if (akaụntụ_valuu == 25) return "한국어/자체/파일없음예외";
        if (akaụntụ_valuu == 26) return "한국어/자체/통신예외";
        if (akaụntụ_valuu == 27) return "한국어/자체/잘못된인수예외";
        if (akaụntụ_valuu == 28) return "한국어/자체/숫자형식예외";
        if (akaụntụ_valuu == 29) return "한국어/자체/범위예외";
        if (akaụntụ_valuu == 30) return "한국어/자체/배열범위예외";
        if (akaụntụ_valuu == 31) return "한국어/자체/문자열범위예외";
        if (akaụntụ_valuu == 32) return "한국어/자체/빈참조예외";
        if (akaụntụ_valuu == 33) return "한국어/자체/산술예외";
        if (akaụntụ_valuu == 34) return "한국어/자체/상태예외";
        if (akaụntụ_valuu == 35) return "한국어/자체/형변환예외";
        if (akaụntụ_valuu == 36) return "한국어/자체/음수배열크기예외";
        if (akaụntụ_valuu == 37) return "한국어/자체/MKPOKỌTA_Store_ọdịdà";
        if (akaụntụ_valuu == 38) return "한국어/자체/가닥상태예외";
        if (akaụntụ_valuu == 1) return "java/lang/Throwable"; if (akaụntụ_valuu == 2) return "java/lang/Exception";
        if (akaụntụ_valuu == 3) return "java/lang/RuntimeException"; if (akaụntụ_valuu == 4) return "java/lang/ArithmeticException";
        if (akaụntụ_valuu == 5) return "java/lang/NullPointerException"; if (akaụntụ_valuu == 6) return "java/lang/IndexOutOfBoundsException";
        if (akaụntụ_valuu == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (akaụntụ_valuu == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (akaụntụ_valuu == 9) return "java/lang/IllegalArgumentException"; if (akaụntụ_valuu == 10) return "java/lang/NumberFormatException";
        if (akaụntụ_valuu == 11) return "java/io/IOException"; if (akaụntụ_valuu == 12) return "java/io/FileNotFoundException";
        if (akaụntụ_valuu == 17) return "java/lang/ArrayStoreException";
        if (akaụntụ_valuu == 18) return "java/net/UnknownHostException";
        if (akaụntụ_valuu == 19) return "java/net/SocketTimeoutException";
        if (akaụntụ_valuu == 16) return "java/lang/IllegalThreadStateException";
        if (akaụntụ_valuu == 13) return "java/lang/IllegalStateException"; if (akaụntụ_valuu == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int akaụntụ_valuu) {
        if (akaụntụ_valuu == 40) return 2;
        if (akaụntụ_valuu == 41) return 40;
        if (akaụntụ_valuu == 39) return 11;
        if (akaụntụ_valuu == 1) return 0;
        if (akaụntụ_valuu == 2) return 1;
        if (akaụntụ_valuu == 3) return 2;
        if (akaụntụ_valuu == 4) return 3;
        if (akaụntụ_valuu == 5) return 3;
        if (akaụntụ_valuu == 6) return 3;
        if (akaụntụ_valuu == 7) return 6;
        if (akaụntụ_valuu == 8) return 6;
        if (akaụntụ_valuu == 9) return 3;
        if (akaụntụ_valuu == 10) return 9;
        if (akaụntụ_valuu == 11) return 2;
        if (akaụntụ_valuu == 12) return 11;
        if (akaụntụ_valuu == 13) return 3;
        if (akaụntụ_valuu == 14) return 3;
        if (akaụntụ_valuu == 15) return 3;
        if (akaụntụ_valuu == 16) return 9;
        if (akaụntụ_valuu == 17) return 3;
        if (akaụntụ_valuu == 18) return 11;
        if (akaụntụ_valuu == 19) return 11;
        if (akaụntụ_valuu == 20) return 2;
        if (akaụntụ_valuu == 21) return 3;
        if (akaụntụ_valuu == 22) return 11;
        if (akaụntụ_valuu == 23) return 22;
        if (akaụntụ_valuu == 24) return 22;
        if (akaụntụ_valuu == 25) return 22;
        if (akaụntụ_valuu == 26) return 22;
        if (akaụntụ_valuu == 27) return 9;
        if (akaụntụ_valuu == 28) return 27;
        if (akaụntụ_valuu == 29) return 6;
        if (akaụntụ_valuu == 30) return 29;
        if (akaụntụ_valuu == 31) return 29;
        if (akaụntụ_valuu == 32) return 5;
        if (akaụntụ_valuu == 33) return 4;
        if (akaụntụ_valuu == 34) return 13;
        if (akaụntụ_valuu == 35) return 14;
        if (akaụntụ_valuu == 36) return 15;
        if (akaụntụ_valuu == 37) return 17;
        if (akaụntụ_valuu == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int ǹdịnezie_valuu, int 요구값) {
        for (int 깊이 = 0; ǹdịnezie_valuu != 0 && 깊이 < 16; 깊이++, ǹdịnezie_valuu = 예외부모(ǹdịnezie_valuu))
            if (ǹdịnezie_valuu == 요구값) return true;
        return false;
    }
    static void 예외던짐(int akaụntụ_valuu, String GỤ̀ỌM_Nrụtụ_aka) {
        int ihe_Nrụtụ_aka = 새기억(9, 2); if (mmejọ) return;
        힙[ihe_Nrụtụ_aka + 2] = akaụntụ_valuu; 힙[ihe_Nrụtụ_aka + 3] = usu_mkpụrụedemede(GỤ̀ỌM_Nrụtụ_aka); 힙참조[ihe_Nrụtụ_aka + 3] = 1;
        던진객체 = ihe_Nrụtụ_aka; mmejọ = true;
    }
    static boolean 맞는객체(int ihe_Nrụtụ_aka, int Aha) {
        if (ihe_Nrụtụ_aka == 0) return true;
        if (!객체유효(ihe_Nrụtụ_aka)) return false;
        int 분류코드 = 힙[ihe_Nrụtụ_aka];
        if (Mkpụrụokwu_SMS(Aha, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Aha);
        if (분류코드 == 9) { int ebenlereanya_àdreèsì = 예외상수(Aha); return ebenlereanya_àdreèsì != 0 && 예외포함(힙[ihe_Nrụtụ_aka + 2], ebenlereanya_àdreèsì); }
        if (분류코드 == 1) return Mkpụrụokwu_SMS(Aha, "java/lang/String") || Mkpụrụokwu_SMS(Aha, "java/lang/CharSequence");
        if (분류코드 == 4) return Mkpụrụokwu_SMS(Aha, "java/lang/StringBuilder") || Mkpụrụokwu_SMS(Aha, "java/lang/CharSequence");
        if (분류코드 == 10) return Mkpụrụokwu_SMS(Aha, "java/util/ArrayList") || Mkpụrụokwu_SMS(Aha, "java/util/List");
        if (분류코드 == 11) return Mkpụrụokwu_SMS(Aha, "java/util/HashMap") || Mkpụrụokwu_SMS(Aha, "java/util/Map");
        if (분류코드 == 12) return Mkpụrụokwu_SMS(Aha, "java/lang/Integer") || Mkpụrụokwu_SMS(Aha, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[ihe_Nrụtụ_aka + 13] != 0) return 한국어화면종(Aha) == 분류코드 || Mkpụrụokwu_SMS(Aha, "한국어/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Aha) == 0 && 화면종(Aha) == 분류코드) || Mkpụrụokwu_SMS(Aha, "java/awt/Component") || Mkpụrụokwu_SMS(Aha, "java/awt/Container") || Mkpụrụokwu_SMS(Aha, "javax/swing/JComponent");
        if (분류코드 == 29) return Mkpụrụokwu_SMS(Aha, 힙[ihe_Nrụtụ_aka + 3] != 0 ? "한국어/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Mkpụrụokwu_SMS(Aha, "java/awt/FlowLayout") || Mkpụrụokwu_SMS(Aha, "java/awt/LayoutManager");
        if (분류코드 == 17) return Mkpụrụokwu_SMS(Aha, "java/net/Socket");
        if (분류코드 == 18) return Mkpụrụokwu_SMS(Aha, "java/net/ServerSocket");
        if (분류코드 == 19) return Mkpụrụokwu_SMS(Aha, 힙[ihe_Nrụtụ_aka + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Mkpụrụokwu_SMS(Aha, "java/net/InetAddress");
        if (분류코드 == 15) return Mkpụrụokwu_SMS(Aha, "java/net/DatagramSocket");
        if (분류코드 == 16) return Mkpụrụokwu_SMS(Aha, "java/net/DatagramPacket");
        if (분류코드 == 13) return Mkpụrụokwu_SMS(Aha, 힙[ihe_Nrụtụ_aka + 3] != 0 ? "한국어/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Mkpụrụokwu_SMS(Aha, "[I"); if (분류코드 == 20) return Mkpụrụokwu_SMS(Aha, "[B"); if (분류코드 == 21) return Mkpụrụokwu_SMS(Aha, "[Z");
        if (분류코드 == 22) return Mkpụrụokwu_SMS(Aha, "[C"); if (분류코드 == 23) return Mkpụrụokwu_SMS(Aha, "[S");
        if (분류코드 != 3) return false;
        if (Mkpụrụokwu_SMS(Aha, "[Ljava/lang/Object;")) return true;
        int ǹsòmebe = MKPOKỌTA_njìmebe[ihe_Nrụtụ_aka];
        if (ǹsòmebe == -1) return Mkpụrụokwu_SMS(Aha, "[Ljava/lang/String;") || Mkpụrụokwu_SMS(Aha, "[Ljava/lang/CharSequence;");
        if (ǹsòmebe == 0) return false;
        if (배열종비교(ǹsòmebe, Aha)) return true;
        if ((Mkpụrụokwu_SMS(ǹsòmebe, "java/lang/String") || Mkpụrụokwu_SMS(ǹsòmebe, "java/lang/StringBuilder")) && Mkpụrụokwu_SMS(Aha, "[Ljava/lang/CharSequence;")) return true;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 종수; memmenwè_indèks++) if (같은말(klaàsị_Nkwuke_akara_ahà[memmenwè_indèks], ǹsòmebe)) {
            for (int koòdù_nkeakàrà = memmenwè_indèks, 중첩깊이 = 0; koòdù_nkeakàrà >= 0 && 중첩깊이 < 16; 중첩깊이++, koòdù_nkeakàrà = 부모종(koòdù_nkeakàrà)) {
                if (배열종비교(종부모[koòdù_nkeakàrà], Aha)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[koòdù_nkeakàrà]; 안쪽자리++) if (배열종비교(klaàsị_ihuọrụ[koòdù_nkeakàrà * 16 + 안쪽자리], Aha)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int akara_ahà_ihendịgide, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (akara_ahà_ihendịgide == 0 || 항목수 < 4 || Faịlụ[검사자리] != '[' || Faịlụ[검사자리 + 1] != 'L' || Faịlụ[검사자리 + 항목수 - 1] != ';' || 상나[akara_ahà_ihendịgide] != 항목수 - 3) return false;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수 - 3; memmenwè_indèks++) if (Faịlụ[상가[akara_ahà_ihendịgide] + memmenwè_indèks] != Faịlụ[검사자리 + 2 + memmenwè_indèks]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        mmejọ = false;
        while (okpokoro_indèks >= 현재가닥 * 32) {
            int ọbọakwụkwọ_indèks = okpokoro_usoro[okpokoro_indèks], 읽는자리 = okpokoro_okwunkụzi[okpokoro_indèks];
            for (int memmenwè_indèks = 0; memmenwè_indèks < 잡기수; memmenwè_indèks++) if (잡기함수[memmenwè_indèks] == ọbọakwụkwọ_indèks && 읽는자리 >= 잡기시작[memmenwè_indèks] && 읽는자리 < 잡기끝[memmenwè_indèks]
                && (잡기종[memmenwè_indèks] == 0 || 맞는객체(던진객체, 잡기종[memmenwè_indèks]))) {
                틀위치[okpokoro_indèks] = 잡기위치[memmenwè_indèks]; okpokoro_ikpo[okpokoro_indèks] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (kwàdo_mmàlite_okpokoro[okpokoro_indèks] != 0) klaàsị_Nkwuke_ọnọdụ[kwàdo_mmàlite_okpokoro[okpokoro_indèks] - 1] = 3;
            if (틀잠금[okpokoro_indèks] != 0) { 잠금풀기(틀잠금[okpokoro_indèks]); 틀잠금[okpokoro_indèks] = 0; }
            okpokoro_indèks--;
        }
        òjìàrụ.Chekwaa_ozi("Uncaught ");
        if (힙[던진객체] == 9) { òjìàrụ.Chekwaa_ozi(예외이름(힙[던진객체 + 2])); òjìàrụ.Chekwaa_ozi(": "); dee_SMS(힙[던진객체 + 3]); }
        else òjìàrụ.Chekwaa_ozi("user exception");
        òjìàrụ.dee_mkpụrụedemede_valuu(10); 던진객체 = 0; mmejọ = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void ikpo_okwunkụzi(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int baịtị_datà = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(baịtị_datà, 둘째형식); return; }
        int koòdù_nkeakàrà = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(koòdù_nkeakàrà, 셋째형식); 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); 넣기(koòdù_nkeakàrà, 셋째형식); 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(koòdù_nkeakàrà, 셋째형식); 넣기(baịtị_datà, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int akara_ahà_ihendịgide, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(akara_ahà_ihendịgide);
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/lang/Thread") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(akara_ahà_ihendịgide) != 0) { 분류코드 = 화면종(akara_ahà_ihendịgide); 유효길이 = 12; }
        if (분류코드 == 0) {
            int koòdù_nkeakàrà = chọta_klaàsị_Nkwuke(akara_ahà_ihendịgide); if (koòdù_nkeakàrà < 0 || mmejọ || !kwàdo_mmàlite(koòdù_nkeakàrà, 시작점)) return;
            분류코드 = 32 + koòdù_nkeakàrà; 유효길이 = 종칸수[koòdù_nkeakàrà];
        }
        int ihe_Nrụtụ_aka = kepụta_Nchekwa(분류코드, 유효길이); if (mmejọ) return;
        if (분류코드 == 13 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/작업가닥")) 힙[ihe_Nrụtụ_aka + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(akara_ahà_ihendịgide) != 0) 힙[ihe_Nrụtụ_aka + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[ihe_Nrụtụ_aka + 2] = -1;
        if (분류코드 == 9) 힙[ihe_Nrụtụ_aka + 2] = 예외참조;
        넣기(ihe_Nrụtụ_aka, 2);
    }
    static boolean 값같음(int 첫값, int baịtị_datà) {
        if (첫값 == baịtị_datà) return true;
        if (첫값 == 0 || baịtị_datà == 0 || 첫값 < 0 || baịtị_datà < 0 || 첫값 >= 힙끝 || baịtị_datà >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[baịtị_datà] == 1) return 글같음(첫값, baịtị_datà, false);
        return 힙[첫값] == 12 && 힙[baịtị_datà] == 12 && 힙[첫값 + 2] == 힙[baịtị_datà + 2];
    }
    static int 글조각(int ihe_Nrụtụ_aka, int 시작자리, int 끝자리) {
        if (!ihe_valuu(ihe_Nrụtụ_aka, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[ihe_Nrụtụ_aka + 1]) { ọdịdà_valuu("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = kepụta_Nchekwa(1, 끝자리 - 시작자리); if (mmejọ) return 0;
        for (int memmenwè_indèks = 시작자리; memmenwè_indèks < 끝자리; memmenwè_indèks++) 힙[반환값 + 2 + memmenwè_indèks - 시작자리] = 힙[ihe_Nrụtụ_aka + 2 + memmenwè_indèks];
        return 반환값;
    }
    static int sonye_SMS(int 첫값, int baịtị_datà) {
        if (!ihe_valuu(첫값, 1) || !ihe_valuu(baịtị_datà, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], usoro_indèks = 힙[baịtị_datà + 1], 반환값 = kepụta_Nchekwa(1, 항목수 + usoro_indèks); if (mmejọ) return 0;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 힙[반환값 + 2 + memmenwè_indèks] = 힙[첫값 + 2 + memmenwè_indèks];
        for (int memmenwè_indèks = 0; memmenwè_indèks < usoro_indèks; memmenwè_indèks++) 힙[반환값 + 2 + 항목수 + memmenwè_indèks] = 힙[baịtị_datà + 2 + memmenwè_indèks];
        return 반환값;
    }
    static boolean 기본호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        if (Mkpụrụokwu_SMS(nwe, "한국어/자체/실행인수") && 명령코드 == 184) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "개수") && Mkpụrụokwu_SMS(서술상수, "()I")) { 넣기(òjìàrụ.인수개수() - 1, 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "SMS") && Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= òjìàrụ.인수개수() - 1) 예외던짐(29, "mee_nnyemiwu 인수 범위를 벗어났습니다");
                else 넣기(usu_mkpụrụedemede(òjìàrụ.인수(순번 + 1)), 2);
                return true;
            }
            ọdịdà_valuu("지원하지 않는 한국어 mee_nnyemiwu 인수 호출"); return true;
        }
        if (Mkpụrụokwu_SMS(nwe, "한국어/자체/작업가닥")) { ùsòrò_treèd(akara_ahà_ihendịgide, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(nwe)) { 한국어화면호출(nwe, akara_ahà_ihendịgide, 서술상수, 명령코드); return true; }
        if (화면소유(nwe)) { 화면호출(nwe, akara_ahà_ihendịgide, 서술상수, 명령코드); return true; }
        if (Mkpụrụokwu_SMS(nwe, "java/net/Socket") || Mkpụrụokwu_SMS(nwe, "java/net/ServerSocket") || Mkpụrụokwu_SMS(nwe, "java/io/InputStream") || Mkpụrụokwu_SMS(nwe, "java/io/OutputStream")) { 흐름호출(nwe, akara_ahà_ihendịgide, 서술상수, 명령코드); return true; }
        if (Mkpụrụokwu_SMS(nwe, "한국어/자체/mkpụrụobī_kọmpùta_valuu") && 명령코드 == 184) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "화면너비") && Mkpụrụokwu_SMS(서술상수, "()I")) { 넣기(òjìàrụ.화면너비(), 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "화면높이") && Mkpụrụokwu_SMS(서술상수, "()I")) { 넣기(òjìàrụ.화면높이(), 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "밀리초") && Mkpụrụokwu_SMS(서술상수, "()I")) { 넣기(òjìàrụ.밀리초(), 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "그림대기") && Mkpụrụokwu_SMS(서술상수, "()I")) { 넣기(òjìàrụ.그림대기(), 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "사각형") && Mkpụrụokwu_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), ngakọrịta_x = 빼기(1); 넣기(òjìàrụ.사각형(ngakọrịta_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/net/InetAddress") || Mkpụrụokwu_SMS(nwe, "java/net/DatagramPacket") || Mkpụrụokwu_SMS(nwe, "java/net/DatagramSocket")) { 통신호출(nwe, akara_ahà_ihendịgide, 서술상수, 명령코드); return true; }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/Thread")) { 가닥호출(akara_ahà_ihendịgide, 서술상수, 명령코드); return true; }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/Object")) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && Mkpụrụokwu_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "equals") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baịtị_datà = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == baịtị_datà ? 1 : 0, 1); return true; }
        }
        if (예외상수(nwe) != 0) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && 명령코드 == 183 && (Mkpụrụokwu_SMS(서술상수, "()V") || Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int mkpalite = Mkpụrụokwu_SMS(서술상수, "()V") ? 0 : 빼기(2), ihe_Nrụtụ_aka = 빼기(2);
                if (ihe_valuu(ihe_Nrụtụ_aka, 9)) { 힙[ihe_Nrụtụ_aka + 3] = mkpalite; 힙참조[ihe_Nrụtụ_aka + 3] = 1; } return true;
            }
            if ((Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getMessage") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "설명")) && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 9)) 넣기(힙[ihe_Nrụtụ_aka + 3], 2); return true; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/String")) {
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getBytes") && (Mkpụrụokwu_SMS(서술상수, "()[B") || Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int ntinye_koòdù_akara_ahà = Mkpụrụokwu_SMS(서술상수, "()[B") ? 0 : 빼기(2), ihe_Nrụtụ_aka = 빼기(2);
                if (!ihe_valuu(ihe_Nrụtụ_aka, 1)) return true;
                if (ntinye_koòdù_akara_ahà != 0 && !글같음(ntinye_koòdù_akara_ahà, usu_mkpụrụedemede("UTF-8"), false) && !글같음(ntinye_koòdù_akara_ahà, usu_mkpụrụedemede("UTF8"), false) && !글같음(ntinye_koòdù_akara_ahà, usu_mkpụrụedemede("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[ihe_Nrụtụ_aka + 1], 반환값 = kepụta_Nchekwa(20, 항목수 * 3), 사용수 = 0; if (mmejọ) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int koòdù_nkeakàrà = 힙[ihe_Nrụtụ_aka + 2 + 안쪽자리];
                    if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[ihe_Nrụtụ_aka + 3 + 안쪽자리] >= 0xdc00 && 힙[ihe_Nrụtụ_aka + 3 + 안쪽자리] <= 0xdfff) koòdù_nkeakàrà = 0x10000 + ((koòdù_nkeakàrà - 0xd800) << 10) + 힙[ihe_Nrụtụ_aka + 2 + ++안쪽자리] - 0xdc00;
                    else if (koòdù_nkeakàrà >= 0xd800 && koòdù_nkeakàrà <= 0xdfff) koòdù_nkeakàrà = '?';
                    if (koòdù_nkeakàrà < 128) 힙[반환값 + 2 + 사용수++] = koòdù_nkeakàrà;
                    else { int 바이트수 = koòdù_nkeakàrà < 2048 ? 2 : koòdù_nkeakàrà < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | koòdù_nkeakàrà >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | koòdù_nkeakàrà >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "valueOf") && Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(ọbula_mkpụrụedemede(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "equals") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int baịtị_datà = 빼기(2), 첫값 = 빼기(2); if (ihe_valuu(첫값, 1)) 넣기(글같음(첫값, baịtị_datà, false) ? 1 : 0, 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isEmpty") && Mkpụrụokwu_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (ihe_valuu(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "substring") && (Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/String;") || Mkpụrụokwu_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Mkpụrụokwu_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (ihe_valuu(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "concat") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int baịtị_datà = 빼기(2), 첫값 = 빼기(2); 넣기(sonye_SMS(첫값, baịtị_datà), 2); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "hashCode") && Mkpụrụokwu_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), di_ike_valuu = 0; if (ihe_valuu(첫값, 1)) { for (int memmenwè_indèks = 0; memmenwè_indèks < 힙[첫값 + 1]; memmenwè_indèks++) di_ike_valuu = di_ike_valuu * 31 + 힙[첫값 + 2 + memmenwè_indèks]; 넣기(di_ike_valuu, 1); } return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "toString") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (ihe_valuu(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/Integer")) {
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "valueOf") && Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int datà_valuu = 빼기(1), ihe_Nrụtụ_aka = datà_valuu >= -128 && datà_valuu <= 127 ? Store_ọnụọgụ_nzùrùòkè[datà_valuu + 128] : 0; if (ihe_Nrụtụ_aka == 0) { ihe_Nrụtụ_aka = kepụta_Nchekwa(12, 1); if (!mmejọ) { 힙[ihe_Nrụtụ_aka + 2] = datà_valuu; if (datà_valuu >= -128 && datà_valuu <= 127) Store_ọnụọgụ_nzùrùòkè[datà_valuu + 128] = ihe_Nrụtụ_aka; } } 넣기(ihe_Nrụtụ_aka, 2); return true; }
            if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && Mkpụrụokwu_SMS(서술상수, "(I)V")) { int datà_valuu = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 12)) 힙[ihe_Nrụtụ_aka + 2] = datà_valuu; return true; }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "intValue") && Mkpụrụokwu_SMS(서술상수, "()I")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 12)) 넣기(힙[ihe_Nrụtụ_aka + 2], 1); return true; }
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "toString") && Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(ọbula_mkpụrụedemede(빼기(1)), 2); return true; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/Math") && 명령코드 == 184) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "abs") && Mkpụrụokwu_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "min") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "max")) && Mkpụrụokwu_SMS(서술상수, "(II)I")) { int baịtị_datà = 빼기(1), 첫값 = 빼기(1); 넣기(Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "min") ? (첫값 < baịtị_datà ? 첫값 : baịtị_datà) : (첫값 > baịtị_datà ? 첫값 : baịtị_datà), 1); return true; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/lang/System") && 명령코드 == 184) {
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "gc") && Mkpụrụokwu_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "arraycopy") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), ebemwèga_valuu_indèks = 빼기(1), baịtị_datà = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(baịtị_datà)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[baịtị_datà] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ọdịdà_valuu("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || ebemwèga_valuu_indèks < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || ebemwèga_valuu_indèks > 힙[baịtị_datà + 1] - 항목수) ọdịdà_valuu("ArrayIndexOutOfBoundsException");
                    else if (첫값 == baịtị_datà && ebemwèga_valuu_indèks > 시작자리) { for (int memmenwè_indèks = 항목수 - 1; memmenwè_indèks >= 0; memmenwè_indèks--) 힙[baịtị_datà + 2 + ebemwèga_valuu_indèks + memmenwè_indèks] = 힙[첫값 + 2 + 시작자리 + memmenwè_indèks]; }
                    else { for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수 && !mmejọ; memmenwè_indèks++) { int datà_valuu = 힙[첫값 + 2 + 시작자리 + memmenwè_indèks]; if (분류코드 != 3 || 배열저장가능(baịtị_datà, datà_valuu)) 힙[baịtị_datà + 2 + ebemwèga_valuu_indèks + memmenwè_indèks] = datà_valuu; } }
                }
                return true;
            }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/util/ArrayList") || Mkpụrụokwu_SMS(nwe, "java/util/List") || Mkpụrụokwu_SMS(nwe, "java/util/HashMap") || Mkpụrụokwu_SMS(nwe, "java/util/Map")) {
            모음호출(nwe, akara_ahà_ihendịgide, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int ihe_Nrụtụ_aka, int 필요수) {
        int 이전값 = 힙[ihe_Nrụtụ_aka + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int datà_MKPOKỌTA = kepụta_Nchekwa(3, 다음자리); if (mmejọ) return;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 용량값; memmenwè_indèks++) 힙[datà_MKPOKỌTA + 2 + memmenwè_indèks] = 힙[이전값 + 2 + memmenwè_indèks];
        힙[ihe_Nrụtụ_aka + 2] = datà_MKPOKỌTA; 힙참조[ihe_Nrụtụ_aka + 2] = 1;
    }
    static void 모음호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        boolean 대응참조 = Mkpụrụokwu_SMS(nwe, "java/util/HashMap") || Mkpụrụokwu_SMS(nwe, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && 명령코드 == 183 && Mkpụrụokwu_SMS(서술상수, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 분류코드)) 모음늘리기(ihe_Nrụtụ_aka, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ọdịdà_valuu("invalid collection invocation"); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "size") && Mkpụrụokwu_SMS(서술상수, "()I") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isEmpty") && Mkpụrụokwu_SMS(서술상수, "()Z")) {
            int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 분류코드)) 넣기(Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "size") ? 힙[ihe_Nrụtụ_aka + 3] : 힙[ihe_Nrụtụ_aka + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "clear") && Mkpụrụokwu_SMS(서술상수, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 분류코드)) { int datà_MKPOKỌTA = 힙[ihe_Nrụtụ_aka + 2]; for (int memmenwè_indèks = 0; memmenwè_indèks < 힙[datà_MKPOKỌTA + 1]; memmenwè_indèks++) 힙[datà_MKPOKỌTA + 2 + memmenwè_indèks] = 0; 힙[ihe_Nrụtụ_aka + 3] = 0; } return; }
        if (!대응참조 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "add") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int datà_valuu = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 10)) return;
            int 항목수 = 힙[ihe_Nrụtụ_aka + 3]; 모음늘리기(ihe_Nrụtụ_aka, 항목수 + 1); if (!mmejọ) { 힙[힙[ihe_Nrụtụ_aka + 2] + 2 + 항목수] = datà_valuu; 힙[ihe_Nrụtụ_aka + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "get") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "remove")) && Mkpụrụokwu_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "set") && Mkpụrụokwu_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "set"); int datà_valuu = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2);
            if (!ihe_valuu(ihe_Nrụtụ_aka, 10)) return;
            int 항목수 = 힙[ihe_Nrụtụ_aka + 3], datà_MKPOKỌTA = 힙[ihe_Nrụtụ_aka + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[datà_MKPOKỌTA + 2 + 항목자리];
            if (지정여부) 힙[datà_MKPOKỌTA + 2 + 항목자리] = datà_valuu;
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "remove")) { for (int memmenwè_indèks = 항목자리 + 1; memmenwè_indèks < 항목수; memmenwè_indèks++) 힙[datà_MKPOKỌTA + 1 + memmenwè_indèks] = 힙[datà_MKPOKỌTA + 2 + memmenwè_indèks]; 힙[datà_MKPOKỌTA + 1 + 항목수] = 0; 힙[ihe_Nrụtụ_aka + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "get") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "remove")) && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "put") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "containsKey") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "put"), wepụ = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "remove");
            int datà_valuu = 넣기여부 ? 빼기(2) : 0, ọtụgwo_Nrụtụ_aka = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 11)) return;
            int 항목수 = 힙[ihe_Nrụtụ_aka + 3], datà_MKPOKỌTA = 힙[ihe_Nrụtụ_aka + 2], 찾은여부 = -1;
            for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) if (값같음(ọtụgwo_Nrụtụ_aka, 힙[datà_MKPOKỌTA + 2 + 2 * memmenwè_indèks])) { 찾은여부 = memmenwè_indèks; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[datà_MKPOKỌTA + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(ihe_Nrụtụ_aka, (항목수 + 1) * 2); datà_MKPOKỌTA = 힙[ihe_Nrụtụ_aka + 2]; 찾은여부 = 항목수; if (!mmejọ) 힙[ihe_Nrụtụ_aka + 3] = 항목수 + 1; }
                if (!mmejọ) { 힙[datà_MKPOKỌTA + 2 + 2 * 찾은여부] = ọtụgwo_Nrụtụ_aka; 힙[datà_MKPOKỌTA + 3 + 2 * 찾은여부] = datà_valuu; }
            }
            if (wepụ && 찾은여부 >= 0) { for (int memmenwè_indèks = 찾은여부 + 1; memmenwè_indèks < 항목수; memmenwè_indèks++) { 힙[datà_MKPOKỌTA + 2 * memmenwè_indèks] = 힙[datà_MKPOKỌTA + 2 + 2 * memmenwè_indèks]; 힙[datà_MKPOKỌTA + 1 + 2 * memmenwè_indèks] = 힙[datà_MKPOKỌTA + 3 + 2 * memmenwè_indèks]; } 힙[datà_MKPOKỌTA + 2 * 항목수] = 0; 힙[datà_MKPOKỌTA + 1 + 2 * 항목수] = 0; 힙[ihe_Nrụtụ_aka + 3] = 항목수 - 1; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ọdịdà_valuu("unsupported collection method");
    }
    static boolean 잠금얻기(int ihe_Nrụtụ_aka) {
        if (!객체유효(ihe_Nrụtụ_aka)) return false;
        if (잠금깊이[ihe_Nrụtụ_aka] != 0 && 잠금주인[ihe_Nrụtụ_aka] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[ihe_Nrụtụ_aka] = 현재가닥 + 1; 잠금깊이[ihe_Nrụtụ_aka]++; return true;
    }
    static void 잠금풀기(int ihe_Nrụtụ_aka) {
        if (!객체유효(ihe_Nrụtụ_aka)) return;
        if (잠금깊이[ihe_Nrụtụ_aka] == 0 || 잠금주인[ihe_Nrụtụ_aka] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[ihe_Nrụtụ_aka] == 0) 잠금주인[ihe_Nrụtụ_aka] = 0;
    }
    static boolean ngbanwụ_treèd() {
        treèd_okpokoro[현재가닥] = okpokoro_indèks;
        if (okpokoro_indèks < 현재가닥 * 32) treèd_ọnọdụ[현재가닥] = 3;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 가닥수; memmenwè_indèks++) if (treèd_ọnọdụ[memmenwè_indèks] == 2 && treèd_ọnọdụ[가닥대기[memmenwè_indèks]] == 3) treèd_ọnọdụ[memmenwè_indèks] = 1;
        for (int memmenwè_indèks = 1; memmenwè_indèks <= 가닥수; memmenwè_indèks++) {
            int 다음자리 = (현재가닥 + memmenwè_indèks) % 가닥수;
            if (treèd_ọnọdụ[다음자리] == 1) { 현재가닥 = 다음자리; okpokoro_indèks = treèd_okpokoro[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 가닥수; memmenwè_indèks++) if (treèd_ọnọdụ[memmenwè_indèks] != 3) { ọdịdà_valuu("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int akara_ahà_ihendịgide, int 서술상수, int 명령코드) { ùsòrò_treèd(akara_ahà_ihendịgide, 서술상수, 명령코드, false); }
    static void ùsòrò_treèd(int akara_ahà_ihendịgide, int 서술상수, int 명령코드, boolean 한국어) {
        if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "kwụsịtụ_ọrụ" : "yield") && Mkpụrụokwu_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "currentThread") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(treèd_ihe[현재가닥], 2); return; }
        if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && (Mkpụrụokwu_SMS(서술상수, "()V") || Mkpụrụokwu_SMS(서술상수, 한국어 ? "(L한국어/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int ebenlereanya_àdreèsì = Mkpụrụokwu_SMS(서술상수, "()V") ? 0 : 빼기(2), ihe_Nrụtụ_aka = 빼기(2);
            if (!객체유효(ihe_Nrụtụ_aka)) return;
            if (힙[ihe_Nrụtụ_aka] == 13) { 힙[ihe_Nrụtụ_aka + 2] = ebenlereanya_àdreèsì; 힙참조[ihe_Nrụtụ_aka + 2] = 1; }
            else if (ebenlereanya_àdreèsì != 0) ọdịdà_valuu("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "Mbido_ọrụ" : "start") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "기다리기" : "join")) && Mkpụrụokwu_SMS(서술상수, "()V") || 명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "살아있는가" : "isAlive") && Mkpụrụokwu_SMS(서술상수, "()Z")) {
            int ihe_Nrụtụ_aka = 빼기(2); if (!객체유효(ihe_Nrụtụ_aka)) return;
            int akaụntụ_valuu = -1; for (int memmenwè_indèks = 0; memmenwè_indèks < 가닥수; memmenwè_indèks++) if (treèd_ihe[memmenwè_indèks] == ihe_Nrụtụ_aka) akaụntụ_valuu = memmenwè_indèks;
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "살아있는가" : "isAlive")) { 넣기(akaụntụ_valuu >= 0 && treèd_ọnọdụ[akaụntụ_valuu] != 3 ? 1 : 0, 1); return; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, 한국어 ? "기다리기" : "join")) { if (akaụntụ_valuu >= 0 && treèd_ọnọdụ[akaụntụ_valuu] != 3) { 가닥대기[현재가닥] = akaụntụ_valuu; treèd_ọnọdụ[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (akaụntụ_valuu >= 0) { 예외던짐(한국어 ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ọdịdà_valuu("thread limit (4 including main)"); return; }
            int ebenlereanya_àdreèsì = 힙[ihe_Nrụtụ_aka] == 13 ? 힙[ihe_Nrụtụ_aka + 2] : ihe_Nrụtụ_aka;
            int ọbọakwụkwọ_indèks = ebenlereanya_àdreèsì > 0 && 힙[ebenlereanya_àdreèsì] >= 32 ? akara_ahà_usoro(힙[ebenlereanya_àdreèsì] - 32, 한국어 ? "mee_ọrụ" : "run", "()V") : -1;
            if (ebenlereanya_àdreèsì != 0 && ọbọakwụkwọ_indèks < 0) { ọdịdà_valuu("Runnable.run required"); return; }
            akaụntụ_valuu = 가닥수++; treèd_ihe[akaụntụ_valuu] = ihe_Nrụtụ_aka; treèd_ebenlereanya[akaụntụ_valuu] = ebenlereanya_àdreèsì;
            int okpokoro = akaụntụ_valuu * 32; treèd_okpokoro[akaụntụ_valuu] = ọbọakwụkwọ_indèks < 0 ? okpokoro - 1 : okpokoro; treèd_ọnọdụ[akaụntụ_valuu] = ọbọakwụkwọ_indèks < 0 ? 3 : 1;
            if (ọbọakwụkwọ_indèks >= 0) { okpokoro_usoro[okpokoro] = ọbọakwụkwọ_indèks; 틀위치[okpokoro] = usoro_Mbido[ọbọakwụkwọ_indèks]; otù_ebe_valuu[okpokoro * 128] = ebenlereanya_àdreèsì; otù_ebe_pinye[okpokoro * 128] = 2; }
            return;
        }
        ọdịdà_valuu("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], àdreèsì_SMS = new int[16];
    static int otù_ebe_àdreèsì() { return àdreèsì_ihe(0x7f000001); }
    static int àdreèsì_ihe(int valuu) { int ihe_Nrụtụ_aka = kepụta_Nchekwa(14, 1); if (!mmejọ) 힙[ihe_Nrụtụ_aka + 2] = valuu; return ihe_Nrụtụ_aka; }
    static int 주소해독(int ihe_Nrụtụ_aka) {
        if (ihe_Nrụtụ_aka == 0 || 글같음(ihe_Nrụtụ_aka, usu_mkpụrụedemede("localhost"), false)) return 0x7f000001;
        if (!ihe_valuu(ihe_Nrụtụ_aka, 1)) return 0;
        int datà_valuu = 0, 총수 = 0, àdreèsì_baịtị = 0, 자릿수 = 0, 항목수 = 힙[ihe_Nrụtụ_aka + 1];
        for (int memmenwè_indèks = 0; memmenwè_indèks <= 항목수; memmenwè_indèks++) {
            int koòdù_nkeakàrà = memmenwè_indèks == 항목수 ? '.' : 힙[ihe_Nrụtụ_aka + 2 + memmenwè_indèks];
            if (koòdù_nkeakàrà == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } datà_valuu = datà_valuu << 8 | àdreèsì_baịtị; 총수++; àdreèsì_baịtị = 자릿수 = 0; }
            else { if (koòdù_nkeakàrà < '0' || koòdù_nkeakàrà > '9' || ++자릿수 > 3 || (àdreèsì_baịtị = àdreèsì_baịtị * 10 + koòdù_nkeakàrà - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return datà_valuu;
    }
    static int àdreèsì_mkpụrụedemede(int datà_valuu) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int àdreèsì_baịtị = datà_valuu >>> 이동비트 & 255;
            if (àdreèsì_baịtị >= 100) àdreèsì_SMS[항목수++] = '0' + àdreèsì_baịtị / 100;
            if (àdreèsì_baịtị >= 10) àdreèsì_SMS[항목수++] = '0' + àdreèsì_baịtị / 10 % 10;
            àdreèsì_SMS[항목수++] = '0' + àdreèsì_baịtị % 10; if (이동비트 != 0) àdreèsì_SMS[항목수++] = '.';
        }
        int ihe_Nrụtụ_aka = kepụta_Nchekwa(1, 항목수); if (!mmejọ) for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 힙[ihe_Nrụtụ_aka + 2 + memmenwè_indèks] = àdreèsì_SMS[memmenwè_indèks]; return ihe_Nrụtụ_aka;
    }
    static void 통신호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        if (Mkpụrụokwu_SMS(nwe, "java/net/InetAddress")) {
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getLoopbackAddress") && Mkpụrụokwu_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(otù_ebe_àdreèsì(), 2); return; }
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getByName") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int datà_valuu = 주소해독(빼기(2)); if (던진객체 == 0 && !mmejọ) 넣기(àdreèsì_ihe(datà_valuu), 2); return;
            }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getHostAddress") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 14)) 넣기(àdreèsì_mkpụrụedemede(힙[ihe_Nrụtụ_aka + 2]), 2); return; }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && (Mkpụrụokwu_SMS(서술상수, "([BI)V") || Mkpụrụokwu_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean ebemwèga_valuu_Nrụtụ_aka = Mkpụrụokwu_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = ebemwèga_valuu_Nrụtụ_aka ? 빼기(1) : 0, àdreèsì_Nrụtụ_aka = ebemwèga_valuu_Nrụtụ_aka ? 빼기(2) : 0;
                int 항목수 = 빼기(1), datà_MKPOKỌTA = 빼기(2), ihe_Nrụtụ_aka = 빼기(2);
                if (!ihe_valuu(ihe_Nrụtụ_aka, 16) || !ihe_valuu(datà_MKPOKỌTA, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[datà_MKPOKỌTA + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (àdreèsì_Nrụtụ_aka != 0 && !ihe_valuu(àdreèsì_Nrụtụ_aka, 14)) return;
                힙[ihe_Nrụtụ_aka + 2] = datà_MKPOKỌTA; 힙참조[ihe_Nrụtụ_aka + 2] = 1; 힙[ihe_Nrụtụ_aka + 3] = 항목수;
                힙[ihe_Nrụtụ_aka + 4] = àdreèsì_Nrụtụ_aka; 힙참조[ihe_Nrụtụ_aka + 4] = 1; 힙[ihe_Nrụtụ_aka + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setLength") && Mkpụrụokwu_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[ihe_Nrụtụ_aka + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[ihe_Nrụtụ_aka + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getData") && Mkpụrụokwu_SMS(서술상수, "()[B") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getLength") && Mkpụrụokwu_SMS(서술상수, "()I") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getAddress") && Mkpụrụokwu_SMS(서술상수, "()Ljava/net/InetAddress;") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getPort") && Mkpụrụokwu_SMS(서술상수, "()I"))) {
                int ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 16)) return;
                int 항목자리 = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getData") ? 2 : Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getLength") ? 3 : Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getAddress") ? 4 : 5;
                넣기(힙[ihe_Nrụtụ_aka + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Mkpụrụokwu_SMS(nwe, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>") && (Mkpụrụokwu_SMS(서술상수, "()V") || Mkpụrụokwu_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Mkpụrụokwu_SMS(서술상수, "()V") ? 0 : 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = òjìàrụ.mepee_Netwọọkụ(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[ihe_Nrụtụ_aka + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setSoTimeout") && Mkpụrụokwu_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ihe_Nrụtụ_aka + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getLocalPort") && Mkpụrụokwu_SMS(서술상수, "()I")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 15)) 넣기(힙[ihe_Nrụtụ_aka + 2] < 0 ? -1 : òjìàrụ.Netwọọkụ_pọọt(힙[ihe_Nrụtụ_aka + 2]), 1); return; }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isClosed") && Mkpụrụokwu_SMS(서술상수, "()Z")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 15)) 넣기(힙[ihe_Nrụtụ_aka + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "close") && Mkpụrụokwu_SMS(서술상수, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 15) && 힙[ihe_Nrụtụ_aka + 2] >= 0) { òjìàrụ.파일서술자닫기(힙[ihe_Nrụtụ_aka + 2]); 힙[ihe_Nrụtụ_aka + 2] = -1; } return; }
            if (명령코드 == 182 && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "send") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "receive")) && Mkpụrụokwu_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int ngwùgwù = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ngwùgwù, 16) || !ihe_valuu(ihe_Nrụtụ_aka, 15)) return;
                int datà_MKPOKỌTA = 힙[ngwùgwù + 2], 유효길이 = 힙[ngwùgwù + 3], 열린파일번호 = 힙[ihe_Nrụtụ_aka + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "send")) {
                    if (!ihe_valuu(힙[ngwùgwù + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int memmenwè_indèks = 0; memmenwè_indèks < 유효길이; memmenwè_indèks++) 통신임시[memmenwè_indèks] = 힙[datà_MKPOKỌTA + 2 + memmenwè_indèks];
                    if (òjìàrụ.zìga_Netwọọkụ(열린파일번호, 힙[힙[ngwùgwù + 4] + 2], 힙[ngwùgwù + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = òjìàrụ.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = òjìàrụ.밀리초();
                        if (힙[ihe_Nrụtụ_aka + 4] == 0) 힙[ihe_Nrụtụ_aka + 4] = 현재시각 + 1;
                        if (힙[ihe_Nrụtụ_aka + 3] > 0 && 현재시각 - (힙[ihe_Nrụtụ_aka + 4] - 1) >= 힙[ihe_Nrụtụ_aka + 3]) { 힙[ihe_Nrụtụ_aka + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(ihe_Nrụtụ_aka, 2); 넣기(ngwùgwù, 2); 틀위치[okpokoro_indèks] = okpokoro_okwunkụzi[okpokoro_indèks]; 바꿈요청 = true; return;
                    }
                    힙[ihe_Nrụtụ_aka + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 힙[datà_MKPOKỌTA + 2 + memmenwè_indèks] = (byte)통신임시[memmenwè_indèks];
                    힙[ngwùgwù + 3] = 항목수; 힙[ngwùgwù + 4] = àdreèsì_ihe(통신임시[513]); 힙참조[ngwùgwù + 4] = 1; 힙[ngwùgwù + 5] = 통신임시[512];
                }
                return;
            }
        }
        ọdịdà_valuu("unsupported java.net method");
    }
    static boolean 흐름대기(int ihe_Nrụtụ_aka) {
        int 현재시각 = òjìàrụ.밀리초();
        if (힙[ihe_Nrụtụ_aka + 5] == 0) 힙[ihe_Nrụtụ_aka + 5] = 현재시각 + 1;
        if (힙[ihe_Nrụtụ_aka + 3] > 0 && 현재시각 - (힙[ihe_Nrụtụ_aka + 5] - 1) >= 힙[ihe_Nrụtụ_aka + 3]) { 힙[ihe_Nrụtụ_aka + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[okpokoro_indèks] = okpokoro_okwunkụzi[okpokoro_indèks]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Mkpụrụokwu_SMS(nwe, "java/net/ServerSocket"), agịrị = Mkpụrụokwu_SMS(nwe, "java/io/InputStream") || Mkpụrụokwu_SMS(nwe, "java/io/OutputStream");
        if (!agịrị && 명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>")) {
            boolean 빈여부 = Mkpụrụokwu_SMS(서술상수, "()V"), 이름지정여부 = Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Mkpụrụokwu_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Mkpụrụokwu_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ọdịdà_valuu("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), àdreèsì_Nrụtụ_aka = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, ihe_Nrụtụ_aka = 빼기(2);
            if (!ihe_valuu(ihe_Nrụtụ_aka, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !ihe_valuu(àdreèsì_Nrụtụ_aka, 14)) return;
            int Netwọọkụ_àdreèsì = 이름지정여부 ? 주소해독(àdreèsì_Nrụtụ_aka) : 주소지정여부 ? 힙[àdreèsì_Nrụtụ_aka + 2] : 0x7f000001;
            if (mmejọ || 던진객체 != 0) return;
            int 열린파일번호 = òjìàrụ.agịrị_njizi(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? òjìàrụ.agịrị_njizi(1, 열린파일번호, 접속번호) : òjìàrụ.JIKỌ_agịrị(열린파일번호, Netwọọkụ_àdreèsì, 접속번호);
            if (처리값 < 0) { òjìàrụ.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[ihe_Nrụtụ_aka + 2] = 열린파일번호; 힙[ihe_Nrụtụ_aka + 4] = 접속번호; 힙[ihe_Nrụtụ_aka + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!agịrị && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setSoTimeout") && Mkpụrụokwu_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[ihe_Nrụtụ_aka + 3] = 밀리초값; return; }
        if (!agịrị && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "close") && Mkpụrụokwu_SMS(서술상수, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (ihe_valuu(ihe_Nrụtụ_aka, 수신쪽 ? 18 : 17) && 힙[ihe_Nrụtụ_aka + 2] >= 0) { òjìàrụ.파일서술자닫기(힙[ihe_Nrụtụ_aka + 2]); 힙[ihe_Nrụtụ_aka + 2] = -1; } return; }
        if (!agịrị && (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getLocalPort") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getPort") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isClosed") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isConnected"))) {
            int ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 수신쪽 ? 18 : 17)) return;
            넣기(Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isClosed") ? 힙[ihe_Nrụtụ_aka + 2] < 0 ? 1 : 0 : Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isConnected") ? 힙[ihe_Nrụtụ_aka + 6] : Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getPort") ? 힙[ihe_Nrụtụ_aka + 4] : 힙[ihe_Nrụtụ_aka + 2] < 0 ? -1 : òjìàrụ.agịrị_njizi(4, 힙[ihe_Nrụtụ_aka + 2], 0), 1); return;
        }
        if (수신쪽 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "accept") && Mkpụrụokwu_SMS(서술상수, "()Ljava/net/Socket;")) {
            int ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 18)) return; int 열린파일번호 = òjìàrụ.agịrị_njizi(3, 힙[ihe_Nrụtụ_aka + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(ihe_Nrụtụ_aka)) 넣기(ihe_Nrụtụ_aka, 2); return; }
            힙[ihe_Nrụtụ_aka + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = kepụta_Nchekwa(17, 5); if (mmejọ) { òjìàrụ.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = òjìàrụ.agịrị_njizi(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !agịrị && ((Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getInputStream") && Mkpụrụokwu_SMS(서술상수, "()Ljava/io/InputStream;")) || (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getOutputStream") && Mkpụrụokwu_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 17)) return; if (힙[ihe_Nrụtụ_aka + 2] < 0 || 힙[ihe_Nrụtụ_aka + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = kepụta_Nchekwa(19, 4); if (mmejọ) return; 힙[반환값 + 2] = ihe_Nrụtụ_aka; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (agịrị) {
            boolean 읽기여부 = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "read"), 쓰기여부 = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "write"), gbochie = Mkpụrụokwu_SMS(서술상수, "([B)I") || Mkpụrụokwu_SMS(서술상수, "([B)V"), 부분배열여부 = Mkpụrụokwu_SMS(서술상수, "([BII)I") || Mkpụrụokwu_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, datà_MKPOKỌTA = gbochie || 부분배열여부 ? 빼기(2) : 0;
            int datà_valuu = 쓰기여부 && Mkpụrụokwu_SMS(서술상수, "(I)V") ? 빼기(1) : 0, ihe_Nrụtụ_aka = 빼기(2);
            if (!ihe_valuu(ihe_Nrụtụ_aka, 19)) return; int 부모참조 = 힙[ihe_Nrụtụ_aka + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "close") && Mkpụrụokwu_SMS(서술상수, "()V")) { òjìàrụ.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "flush") && Mkpụrụokwu_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[ihe_Nrụtụ_aka + 3] == 0)) { ọdịdà_valuu("unsupported stream operation"); return; }
            if (gbochie || 부분배열여부) { if (!ihe_valuu(datà_MKPOKỌTA, 20)) return; if (gbochie) 항목수 = 힙[datà_MKPOKỌTA + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[datà_MKPOKỌTA + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[ihe_Nrụtụ_aka + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? òjìàrụ.파일한바이트읽기(열린파일번호) : òjìàrụ.파일한바이트쓰기(열린파일번호, gbochie || 부분배열여부 ? 힙[datà_MKPOKỌTA + 2 + 시작변위 + 완료수] : datà_valuu);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (gbochie || 부분배열여부)) 힙[datà_MKPOKỌTA + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(gbochie || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[ihe_Nrụtụ_aka + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(ihe_Nrụtụ_aka, 2); if (gbochie || 부분배열여부) 넣기(datà_MKPOKỌTA, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(gbochie || 부분배열여부)) 넣기(datà_valuu, 1); } return;
            }
            힙[ihe_Nrụtụ_aka + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : gbochie || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ọdịdà_valuu("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int akara_ahà_ihendịgide) {
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/windò")) return 24;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/nnyeahà")) return 26;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/ọdụmbi")) return 27;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/SMS_fild")) return 28;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int akara_ahà_ihendịgide) {
        return 한국어화면종(akara_ahà_ihendịgide) != 0 || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/화면구성요소") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "한국어/자체/mmèrème_ọgbàrànchere");
    }
    static int 화면종(int akara_ahà_ihendịgide) {
        int 한국어종 = 한국어화면종(akara_ahà_ihendịgide); if (한국어종 != 0) return 한국어종;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JFrame")) return 24;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JPanel")) return 25;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JLabel")) return 26;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JButton")) return 27;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JTextField")) return 28;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/awt/event/ActionEvent")) return 29;
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int akara_ahà_ihendịgide) {
        return 화면종(akara_ahà_ihendịgide) != 0 || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/awt/Component") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "java/awt/Container") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/JComponent") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/AbstractButton") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/text/JTextComponent") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int ihe_Nrụtụ_aka) { if (!객체유효(ihe_Nrụtụ_aka)) return false; if (힙[ihe_Nrụtụ_aka] < 24 || 힙[ihe_Nrụtụ_aka] > 28) { ọdịdà_valuu("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int ihe_Nrụtụ_aka, int SMS_Nrụtụ_aka) {
        if (SMS_Nrụtụ_aka != 0 && !ihe_valuu(SMS_Nrụtụ_aka, 1)) return;
        int 항목수 = SMS_Nrụtụ_aka == 0 ? 0 : 힙[SMS_Nrụtụ_aka + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) 화면글임시[memmenwè_indèks] = 힙[SMS_Nrụtụ_aka + 2 + memmenwè_indèks];
        if (òjìàrụ.화면글(힙[ihe_Nrụtụ_aka + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[ihe_Nrụtụ_aka + 3] = SMS_Nrụtụ_aka; 힙참조[ihe_Nrụtụ_aka + 3] = 1;
    }
    static int 화면문자읽기(int ihe_Nrụtụ_aka) {
        int akaụntụ_valuu = 힙[ihe_Nrụtụ_aka + 2], 항목수 = òjìàrụ.화면연결(8, akaụntụ_valuu, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ọdịdà_valuu("GUI text read failed"); return 0; }
        for (int memmenwè_indèks = 0; memmenwè_indèks < 항목수; memmenwè_indèks++) { int 부호값 = òjìàrụ.화면연결(9, akaụntụ_valuu, memmenwè_indèks, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = kepụta_Nchekwa(1, 사용수); if (!mmejọ) for (int memmenwè_indèks = 0; memmenwè_indèks < 사용수; memmenwè_indèks++) 힙[반환값 + 2 + memmenwè_indèks] = 화면글임시[memmenwè_indèks]; return 반환값;
    }
    /* 한국어 객체를 직접 만들고 mkpụrụobī_kọmpùta_valuu 화면 기능에 연결한다. Swing ihe_valuu/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        if (Mkpụrụokwu_SMS(nwe, "한국어/자체/mmèrème_ọgbàrànchere")) {
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "나중에실행") && Mkpụrụokwu_SMS(서술상수, "(L한국어/자체/실행할일;)V")) {
                int ọrụ_mmèm = 빼기(2); if (!객체유효(ọrụ_mmèm)) return;
                if (나중수 == 8) { ọdịdà_valuu("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = ọrụ_mmèm; return;
            }
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "사건처리중인가") && Mkpụrụokwu_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ọdịdà_valuu("지원하지 않는 한국어 화면 일정 호출"); return;
        }
        if (Mkpụrụokwu_SMS(nwe, "한국어/자체/동작알림")) {
            int 알림 = 빼기(2); if (!ihe_valuu(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "mmèrème_ebensìbịa") && Mkpụrụokwu_SMS(서술상수, "()L한국어/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "nnyemiwu_SMS") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "indèks") && Mkpụrụokwu_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ọdịdà_valuu("지원하지 않는 한국어 mmèm 알림 호출"); return;
        }
        if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>")) {
            int 종류 = 한국어화면종(nwe), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (òjìàrụ.화면너비() - 폭) / 2; 세로 = (òjìàrụ.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;IIIIL한국어/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ọdịdà_valuu("지원하지 않는 한국어 화면 생성자"); return; }
            int SMS = 빼기(2), njìmebe_valuu = 빼기(2); if (!화면객체(njìmebe_valuu)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > òjìàrụ.화면너비() - 가로 || 높이 > òjìàrụ.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int indèks = òjìàrụ.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (indèks < 1 || indèks > 32) { ọdịdà_valuu("화면 njìmebe_valuu 자리가 가득 찼습니다"); return; }
            힙[njìmebe_valuu + 2] = indèks; 화면참조[indèks - 1] = njìmebe_valuu;
            힙[njìmebe_valuu + 5] = 가로; 힙[njìmebe_valuu + 6] = 세로; 힙[njìmebe_valuu + 7] = 폭; 힙[njìmebe_valuu + 8] = 높이; 힙[njìmebe_valuu + 10] = 2;
            힙[njìmebe_valuu + 4] = 받이; 힙참조[njìmebe_valuu + 4] = 1; 힙[njìmebe_valuu + 12] = 1;
            òjìàrụ.화면연결(1, indèks, 가로, 세로, 폭, 높이);
            if (종류 == 24) òjìàrụ.화면연결(7, indèks, 2, 0, 0, 0);
            화면문자설정(njìmebe_valuu, SMS); return;
        }
        if (명령코드 != 182) { ọdịdà_valuu("잘못된 한국어 화면 호출 Ntiiwu"); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "dee_SMS") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int SMS = 빼기(2), njìmebe_valuu = 빼기(2); if (화면객체(njìmebe_valuu)) 화면문자설정(njìmebe_valuu, SMS); return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "글읽기") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) {
            int njìmebe_valuu = 빼기(2); if (화면객체(njìmebe_valuu)) 넣기(화면문자읽기(njìmebe_valuu), 2); return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "동작맡기기") && Mkpụrụokwu_SMS(서술상수, "(L한국어/자체/동작받이;)V")) {
            int 받이 = 빼기(2), njìmebe_valuu = 빼기(2);
            if (화면객체(njìmebe_valuu)) { 힙[njìmebe_valuu + 4] = 받이; 힙참조[njìmebe_valuu + 4] = 1; 힙[njìmebe_valuu + 12] = 1; } return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "gbakwụnye_njìmebe") && Mkpụrụokwu_SMS(서술상수, "(L한국어/자체/화면구성요소;)V")) {
            int njìmebe_nnwā_valuu = 빼기(2), 부모 = 빼기(2); if (!화면객체(njìmebe_nnwā_valuu) || !화면객체(부모)) return;
            if (òjìàrụ.화면연결(2, 힙[부모 + 2], 힙[njìmebe_nnwā_valuu + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[njìmebe_nnwā_valuu + 11] = 부모; 힙참조[njìmebe_nnwā_valuu + 11] = 1; return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "자리정하기") && Mkpụrụokwu_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), njìmebe_valuu = 빼기(2); if (!화면객체(njìmebe_valuu)) return;
            if (òjìàrụ.화면연결(1, 힙[njìmebe_valuu + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[njìmebe_valuu + 5] = 가로; 힙[njìmebe_valuu + 6] = 세로; 힙[njìmebe_valuu + 7] = 폭; 힙[njìmebe_valuu + 8] = 높이; return;
        }
        if ((Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "gòsi_windò") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "Mechie")) && Mkpụrụokwu_SMS(서술상수, "()V")) {
            boolean mgbàràìhè_valuu = Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "gòsi_windò"); int njìmebe_valuu = 빼기(2); if (!화면객체(njìmebe_valuu)) return;
            if (òjìàrụ.화면연결(mgbàràìhè_valuu ? 3 : 4, 힙[njìmebe_valuu + 2], mgbàràìhè_valuu ? 1 : 0, 0, 0, 0) < 0) { ọdịdà_valuu("화면은 kèmmekọrịta 명령에서 실행해야 합니다"); return; }
            힙[njìmebe_valuu + 9] = mgbàràìhè_valuu ? 1 : 0; return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "보이는가") && Mkpụrụokwu_SMS(서술상수, "()Z")) { int njìmebe_valuu = 빼기(2); if (화면객체(njìmebe_valuu)) 넣기(힙[njìmebe_valuu + 9], 1); return; }
        ọdịdà_valuu("지원하지 않는 한국어 화면 usoro_valuu");
    }
    static void 화면호출(int nwe, int akara_ahà_ihendịgide, int 서술상수, int 명령코드) {
        if (Mkpụrụokwu_SMS(nwe, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "invokeLater") && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int ihe_Nrụtụ_aka = 빼기(2); if (!객체유효(ihe_Nrụtụ_aka)) return; if (나중수 == 8) { ọdịdà_valuu("invokeLater queue full"); return; } 나중실행[나중수++] = ihe_Nrụtụ_aka; return; }
            if (명령코드 == 184 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isEventDispatchThread") && Mkpụrụokwu_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ọdịdà_valuu("unsupported SwingUtilities method"); return;
        }
        if (Mkpụrụokwu_SMS(nwe, "java/awt/event/ActionEvent")) {
            int ihe_Nrụtụ_aka = 빼기(2); if (!ihe_valuu(ihe_Nrụtụ_aka, 29)) return;
            if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getSource") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[ihe_Nrụtụ_aka + 2], 2);
            else if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getActionCommand") && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[ihe_Nrụtụ_aka + 2]), 2);
            else if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getID") && Mkpụrụokwu_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ọdịdà_valuu("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "<init>")) {
            int 열수 = 0, SMS_Nrụtụ_aka = 0;
            if (Mkpụrụokwu_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); SMS_Nrụtụ_aka = 빼기(2); }
            else if (Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)V")) SMS_Nrụtụ_aka = 빼기(2);
            else if (Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Mkpụrụokwu_SMS(서술상수, "()V")) { ọdịdà_valuu("unsupported Swing constructor"); return; }
            int ihe_Nrụtụ_aka = 빼기(2); if (!객체유효(ihe_Nrụtụ_aka)) return;
            if (힙[ihe_Nrụtụ_aka] == 30) { ọdịdà_valuu("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(ihe_Nrụtụ_aka) || 열수 < 0) return;
            int akaụntụ_valuu = òjìàrụ.화면연결(0, 힙[ihe_Nrụtụ_aka] - 23, 0, 0, 0, 0);
            if (akaụntụ_valuu < 1 || akaụntụ_valuu > 32) { ọdịdà_valuu("GUI widget slots exhausted"); return; }
            힙[ihe_Nrụtụ_aka + 2] = akaụntụ_valuu; 화면참조[akaụntụ_valuu - 1] = ihe_Nrụtụ_aka; 힙[ihe_Nrụtụ_aka + 5] = 힙[ihe_Nrụtụ_aka] == 24 ? 130 : 16; 힙[ihe_Nrụtụ_aka + 6] = 힙[ihe_Nrụtụ_aka] == 24 ? 110 : 16;
            힙[ihe_Nrụtụ_aka + 7] = 힙[ihe_Nrụtụ_aka] == 24 ? 380 : 220; 힙[ihe_Nrụtụ_aka + 8] = 힙[ihe_Nrụtụ_aka] == 24 ? 240 : 28; 힙[ihe_Nrụtụ_aka + 10] = 1;
            화면문자설정(ihe_Nrụtụ_aka, SMS_Nrụtụ_aka); return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setText") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setTitle")) { int SMS_Nrụtụ_aka = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka) && Mkpụrụokwu_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(ihe_Nrụtụ_aka, SMS_Nrụtụ_aka); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getText") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getTitle")) { int ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka) && Mkpụrụokwu_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(ihe_Nrụtụ_aka), 2); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "addActionListener") && Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) { 힙[ihe_Nrụtụ_aka + 4] = 수신참조; 힙참조[ihe_Nrụtụ_aka + 4] = 1; } return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "getContentPane") && Mkpụrụokwu_SMS(서술상수, "()Ljava/awt/Container;")) { int ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) 넣기(ihe_Nrụtụ_aka, 2); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setLayout") && Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int Nhàzi_Nrụtụ_aka = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka) && Nhàzi_Nrụtụ_aka != 0) ọdịdà_valuu("only absolute layout (null) is supported"); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "add") && (Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean Nhàzi_ọnọdụ = Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (Nhàzi_ọnọdụ) 빼기(2);
            int njìmebe_nnwā_Nrụtụ_aka = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (!화면객체(njìmebe_nnwā_Nrụtụ_aka) || !화면객체(ihe_Nrụtụ_aka)) return;
            if (òjìàrụ.화면연결(2, 힙[ihe_Nrụtụ_aka + 2], 힙[njìmebe_nnwā_Nrụtụ_aka + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[njìmebe_nnwā_Nrụtụ_aka + 11] = ihe_Nrụtụ_aka; 힙참조[njìmebe_nnwā_Nrụtụ_aka + 11] = 1; if (!Nhàzi_ọnọdụ) 넣기(njìmebe_nnwā_Nrụtụ_aka, 2); return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setBounds") && Mkpụrụokwu_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), ngakọrịta_x = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!화면객체(ihe_Nrụtụ_aka)) return;
            if (òjìàrụ.화면연결(1, 힙[ihe_Nrụtụ_aka + 2], ngakọrịta_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[ihe_Nrụtụ_aka + 5] = ngakọrịta_x; 힙[ihe_Nrụtụ_aka + 6] = 세로좌표; 힙[ihe_Nrụtụ_aka + 7] = 너비; 힙[ihe_Nrụtụ_aka + 8] = 높이; return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setSize") && Mkpụrụokwu_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (!화면객체(ihe_Nrụtụ_aka)) return;
            if (òjìàrụ.화면연결(1, 힙[ihe_Nrụtụ_aka + 2], 힙[ihe_Nrụtụ_aka + 5], 힙[ihe_Nrụtụ_aka + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[ihe_Nrụtụ_aka + 7] = 너비; 힙[ihe_Nrụtụ_aka + 8] = 높이; } return;
        }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setLocationRelativeTo") && Mkpụrụokwu_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), ihe_Nrụtụ_aka = 빼기(2); if (!화면객체(ihe_Nrụtụ_aka)) return; if (상대배치 != 0) { ọdịdà_valuu("only screen centering supported"); return; } 힙[ihe_Nrụtụ_aka + 5] = (òjìàrụ.화면너비() - 힙[ihe_Nrụtụ_aka + 7]) / 2; 힙[ihe_Nrụtụ_aka + 6] = (òjìàrụ.화면높이() - 힙[ihe_Nrụtụ_aka + 8]) / 2; òjìàrụ.화면연결(1, 힙[ihe_Nrụtụ_aka + 2], 힙[ihe_Nrụtụ_aka + 5], 힙[ihe_Nrụtụ_aka + 6], 힙[ihe_Nrụtụ_aka + 7], 힙[ihe_Nrụtụ_aka + 8]); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setDefaultCloseOperation") && Mkpụrụokwu_SMS(서술상수, "(I)V")) { int iwuikikere = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) { if (iwuikikere < 0 || iwuikikere > 3) 예외던짐(9, "close policy"); else { 힙[ihe_Nrụtụ_aka + 10] = iwuikikere; òjìàrụ.화면연결(7, 힙[ihe_Nrụtụ_aka + 2], iwuikikere, 0, 0, 0); } } return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "setVisible") && Mkpụrụokwu_SMS(서술상수, "(Z)V")) { int datà_valuu = 빼기(1), ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) { int 처리값 = òjìàrụ.화면연결(3, 힙[ihe_Nrụtụ_aka + 2], datà_valuu, 0, 0, 0); if (처리값 < 0) ọdịdà_valuu("Swing requires a standalone interactive command"); else 힙[ihe_Nrụtụ_aka + 9] = datà_valuu; } return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "dispose") && Mkpụrụokwu_SMS(서술상수, "()V")) { int ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) { òjìàrụ.화면연결(4, 힙[ihe_Nrụtụ_aka + 2], 0, 0, 0, 0); 힙[ihe_Nrụtụ_aka + 9] = 0; } return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "repaint") || Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "validate")) { int ihe_Nrụtụ_aka = 빼기(2); if (!화면객체(ihe_Nrụtụ_aka) || !Mkpụrụokwu_SMS(서술상수, "()V")) return; òjìàrụ.화면연결(1, 힙[ihe_Nrụtụ_aka + 2], 힙[ihe_Nrụtụ_aka + 5], 힙[ihe_Nrụtụ_aka + 6], 힙[ihe_Nrụtụ_aka + 7], 힙[ihe_Nrụtụ_aka + 8]); return; }
        if (Mkpụrụokwu_SMS(akara_ahà_ihendịgide, "isVisible") && Mkpụrụokwu_SMS(서술상수, "()Z")) { int ihe_Nrụtụ_aka = 빼기(2); if (화면객체(ihe_Nrụtụ_aka)) 넣기(힙[ihe_Nrụtụ_aka + 9], 1); return; }
        ọdịdà_valuu("unsupported Swing method (native subset)");
    }
    static void 사건실행(int ebenlereanya_àdreèsì, int 사건번호, boolean 한국어) {
        if (ebenlereanya_àdreèsì < 1 || 힙[ebenlereanya_àdreèsì] < 32) { ọdịdà_valuu("Java event listener required"); return; }
        int ọbọakwụkwọ_indèks = akara_ahà_usoro(힙[ebenlereanya_àdreèsì] - 32, 사건번호 == 0 ? (한국어 ? "mee_ọrụ" : "run") : (한국어 ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (한국어 ? "(L한국어/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (ọbọakwụkwọ_indèks < 0) { ọdịdà_valuu("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; okpokoro_indèks = 0; treèd_ọnọdụ[0] = 1; okpokoro_ikpo[0] = 0; 틀잠금[0] = kwàdo_mmàlite_okpokoro[0] = 0; 바꿈요청 = false;
        for (int memmenwè_indèks = 0; memmenwè_indèks < 128; memmenwè_indèks++) { otù_ebe_valuu[memmenwè_indèks] = otù_ebe_pinye[memmenwè_indèks] = 0; }
        okpokoro_usoro[0] = ọbọakwụkwọ_indèks; 틀위치[0] = usoro_Mbido[ọbọakwụkwọ_indèks]; otù_ebe_valuu[0] = ebenlereanya_àdreèsì; otù_ebe_pinye[0] = 2;
        if (사건번호 != 0) { otù_ebe_valuu[1] = 사건번호; otù_ebe_pinye[1] = 2; }
        사건중 = true; mee_nnyemiwu(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!mmejọ) {
            if (나중수 > 0) { int ebenlereanya_àdreèsì = 나중실행[0], 한국어 = 나중한국어[0]; for (int memmenwè_indèks = 1; memmenwè_indèks < 나중수; memmenwè_indèks++) { 나중실행[memmenwè_indèks - 1] = 나중실행[memmenwè_indèks]; 나중한국어[memmenwè_indèks - 1] = 나중한국어[memmenwè_indèks]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(ebenlereanya_àdreèsì, 0, 한국어 != 0); continue; }
            if (òjìàrụ.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = òjìàrụ.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ọdịdà_valuu("GUI event I/O failed"); return; }
            int akaụntụ_valuu = 사건번호 & 65535; if (akaụntụ_valuu < 1 || akaụntụ_valuu > 32) continue; int ihe_Nrụtụ_aka = 화면참조[akaụntụ_valuu - 1]; if (ihe_Nrụtụ_aka == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[ihe_Nrụtụ_aka + 10] != 0) 힙[ihe_Nrụtụ_aka + 9] = 0;
                if (힙[ihe_Nrụtụ_aka + 10] == 3) for (int memmenwè_indèks = 0; memmenwè_indèks < 32; memmenwè_indèks++) if (화면참조[memmenwè_indèks] != 0 && 힙[화면참조[memmenwè_indèks]] == 24) òjìàrụ.화면연결(4, memmenwè_indèks + 1, 0, 0, 0, 0);
            } else if (힙[ihe_Nrụtụ_aka + 4] != 0) {
                int GỤ̀ỌM_Nrụtụ_aka = kepụta_Nchekwa(29, 2); if (mmejọ) return; 힙[GỤ̀ỌM_Nrụtụ_aka + 2] = ihe_Nrụtụ_aka; 힙[GỤ̀ỌM_Nrụtụ_aka + 3] = 힙[ihe_Nrụtụ_aka + 12]; 힙참조[GỤ̀ỌM_Nrụtụ_aka + 2] = 1; 사건실행(힙[ihe_Nrụtụ_aka + 4], GỤ̀ỌM_Nrụtụ_aka, 힙[ihe_Nrụtụ_aka + 12] != 0);
            }
        }
    }
    public static int Bido() {
        if (òjìàrụ.인수개수() == 1 && 자바도구.같음(òjìàrụ.인수(0), "-version")) {
            òjìàrụ.Chekwaa_ozi("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (òjìàrụ.인수개수() < 1) { òjìàrụ.Chekwaa_ozi("Usage: java CLASS [ARGS]\n"); return 2; }
        ndebà_klaàsị_Nkwuke = ibu_klaàsị_Nkwuke(usu_mkpụrụedemede(òjìàrụ.인수(0))); if (mmejọ || ndebà_klaàsị_Nkwuke < 0) return 1;
        int ndebà_akara_valuu = akara_ahà_usoro(ndebà_klaàsị_Nkwuke, "Bido", "()V");
        boolean 한국어진입 = ndebà_akara_valuu >= 0 && (usoro_òhèrè[ndebà_akara_valuu] & 9) == 9;
        if (!한국어진입) ndebà_akara_valuu = akara_ahà_usoro(ndebà_klaàsị_Nkwuke, "main", "([Ljava/lang/String;)V");
        if (ndebà_akara_valuu < 0 || (usoro_òhèrè[ndebà_akara_valuu] & 9) != 9) ọdịdà_valuu("public static void Bido() or main(String[] args) required");
        if (mmejọ) return 1;
        int 인수 = kepụta_Nchekwa(3, òjìàrụ.인수개수() - 1); MKPOKỌTA_njìmebe[인수] = -1;
        for (int 수 = 1; 수 < òjìàrụ.인수개수() && !mmejọ; 수++) 힙[인수 + 1 + 수] = usu_mkpụrụedemede(òjìàrụ.인수(수));
        okpokoro_indèks = 0; okpokoro_usoro[0] = ndebà_akara_valuu; 틀위치[0] = usoro_Mbido[ndebà_akara_valuu]; otù_ebe_valuu[0] = 한국어진입 ? 0 : 인수; otù_ebe_pinye[0] = 한국어진입 ? 0 : 2;
        treèd_ọnọdụ[0] = 1; treèd_ihe[0] = kepụta_Nchekwa(13, 2);
        mee_nnyemiwu(); if (!mmejọ) 화면사건들(); return mmejọ ? 1 : 0;
    }
}
