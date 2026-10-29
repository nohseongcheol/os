// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ring 3에서 동작하는 제한형 JVM. iFayili/스택/Isalathiso/isebe 경계를 ukwenza_umyalelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] iFayili = new int[16384], ifayile_igama_I_SMS = new int[64];
    static int[] engajikiyo_thega = new int[512], 상가 = new int[512], 상나 = new int[512], uluhlu_lweekharektha_Isalathiso = new int[512];
    static int[] imethodi_igama_I_SMS = new int[32], imethodi_uhlobo = new int[32], imethodi_fikelela = new int[32];
    static int[] imethodi_qala = new int[32], imethodi_phela = new int[32], imethodi_fumba = new int[32], 함수지역 = new int[32];
    static int[] 함수인수수 = new int[32], imethodi_isiniki_myalelo_uhlobo = new int[512], 함수반환 = new int[32];
    static int[] 경계 = new int[16384];
    static int[] eyale_ndawo_ixabiso = new int[4096], eyale_ndawo_uhlobo = new int[4096], 스택값 = new int[4096], 스택형 = new int[4096];
    static int[] ifreyim_imethodi = new int[32], 틀위치 = new int[32], ifreyim_fumba = new int[32];
    static int[] 힙 = new int[8192];
    static int Ubukhulu, 읽기위치, 상수수, 함수수, iklasi_igama, ifreyim_indeksa = -1, 힙끝 = 1, 반환형;
    static boolean Impazamo;

    static void ukungaphumeleli_ixabiso(String Igama_I_SMS) {
        if (!Impazamo) { umsebenzisi.Bhala("JVM error: "); umsebenzisi.Bhala(Igama_I_SMS); umsebenzisi.bhala_ikharakhtha_ixabiso(10); }
        Impazamo = true;
    }
    static boolean ikliphu(int Phumeza, int ubude_ixabiso) { return Phumeza >= 0 && ubude_ixabiso >= 0 && Phumeza <= Ubukhulu - ubude_ixabiso; }
    static int ibhayithi_ixabiso() {
        if (!ikliphu(읽기위치, 1)) { ukungaphumeleli_ixabiso("truncated class file"); return 0; }
        return iFayili[읽기위치++];
    }
    static int 짧은수() { return ibhayithi_ixabiso() << 8 | ibhayithi_ixabiso(); }
    static int inani_elipheleleyo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ubude_ixabiso) { if (!ikliphu(읽기위치, ubude_ixabiso)) ukungaphumeleli_ixabiso("invalid attribute size"); else 읽기위치 += ubude_ixabiso; }
    static boolean jonga_engajikiyo(int 수, int 종류) {
        if (수 <= 0 || 수 >= 상수수 || engajikiyo_thega[수] != 종류) { ukungaphumeleli_ixabiso("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Phumeza, int ubude_ixabiso, String Igama_I_SMS) {
        if (!ikliphu(Phumeza, ubude_ixabiso) || ubude_ixabiso != Igama_I_SMS.length()) return false;
        for (int 수 = 0; 수 < ubude_ixabiso; 수++) if (iFayili[Phumeza + 수] != Igama_I_SMS.charAt(수)) return false;
        return true;
    }
    static boolean Igama_I_SMS(int engajikiyo_ixabiso, String Igama_I_SMS) { return jonga_engajikiyo(engajikiyo_ixabiso, 1) && 구간(상가[engajikiyo_ixabiso], 상나[engajikiyo_ixabiso], Igama_I_SMS); }
    static boolean 같은말(int 가, int 나) {
        if (!jonga_engajikiyo(가, 1) || !jonga_engajikiyo(나, 1) || 상나[가] != 상나[나]) return false;
        for (int 수 = 0; 수 < 상나[가]; 수++) if (iFayili[상가[가] + 수] != iFayili[상가[나] + 수]) return false;
        return true;
    }
    static int iklasi_igama_I_SMS(int 수) { return jonga_engajikiyo(수, 7) && jonga_engajikiyo(상가[수], 1) ? 상가[수] : 0; }
    static int Isalathiso_igama(int 수) { return jonga_engajikiyo(수, 12) && jonga_engajikiyo(상가[수], 1) ? 상가[수] : 0; }
    static int Isalathiso_uhlobo(int 수) { return jonga_engajikiyo(수, 12) && jonga_engajikiyo(상나[수], 1) ? 상나[수] : 0; }
    static int 서술형(int 끝, boolean engenanto_uhlobo) {
        if (읽기위치 >= 끝) { ukungaphumeleli_ixabiso("invalid descriptor"); return 0; }
        int ixabiso = ibhayithi_ixabiso();
        if (ixabiso == 'V' && engenanto_uhlobo) return 0;
        if (ixabiso == 'I' || ixabiso == 'B' || ixabiso == 'C' || ixabiso == 'S' || ixabiso == 'Z') return 1;
        if (ixabiso == '[') { 서술형(끝, false); return 2; }
        if (ixabiso == 'L') {
            int Phumeza = 읽기위치;
            while (읽기위치 < 끝 && iFayili[읽기위치] != ';') 읽기위치++;
            if (읽기위치 == 끝 || 읽기위치 == Phumeza) ukungaphumeleli_ixabiso("invalid reference descriptor");
            else 읽기위치++;
            return 2;
        }
        ukungaphumeleli_ixabiso("unsupported descriptor type"); return 0;
    }
    static void 서술읽기(int INKQUBO_ixabiso) {
        int 이전 = 읽기위치, 수 = imethodi_uhlobo[INKQUBO_ixabiso];
        if (!jonga_engajikiyo(수, 1)) return;
        읽기위치 = 상가[수]; int 끝 = 읽기위치 + 상나[수];
        if (ibhayithi_ixabiso() != '(') ukungaphumeleli_ixabiso("invalid method descriptor");
        int 개수 = 0;
        while (!Impazamo && 읽기위치 < 끝 && iFayili[읽기위치] != ')') {
            if (개수 == 16) { ukungaphumeleli_ixabiso("too many method arguments"); break; }
            imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 개수++] = 서술형(끝, false);
        }
        if (읽기위치 >= 끝 || ibhayithi_ixabiso() != ')') ukungaphumeleli_ixabiso("invalid method descriptor");
        함수반환[INKQUBO_ixabiso] = 서술형(끝, true); 함수인수수[INKQUBO_ixabiso] = 개수;
        if (읽기위치 != 끝) ukungaphumeleli_ixabiso("invalid method descriptor");
        읽기위치 = 이전;
    }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Impazamo; 수++) { jonga_engajikiyo(짧은수(), 1); 건너(inani_elipheleleyo()); }
    }
    static int umyalelo_ubude(int ixabiso) {
        if (ixabiso == 16 || ixabiso == 18 || ixabiso == 21 || ixabiso == 25 || ixabiso == 54 || ixabiso == 58 || ixabiso == 188) return 2;
        if (ixabiso == 17 || ixabiso == 19 || ixabiso == 132 || ixabiso >= 153 && ixabiso <= 167
            || ixabiso >= 178 && ixabiso <= 184 || ixabiso == 187 || ixabiso == 189 || ixabiso == 192 || ixabiso == 198 || ixabiso == 199) return 3;
        if (ixabiso >= 0 && ixabiso <= 8 || ixabiso >= 26 && ixabiso <= 29 || ixabiso >= 42 && ixabiso <= 46 || ixabiso == 50
            || ixabiso >= 59 && ixabiso <= 62 || ixabiso >= 75 && ixabiso <= 79 || ixabiso == 83 || ixabiso == 87 || ixabiso == 89 || ixabiso == 95
            || ixabiso == 96 || ixabiso == 100 || ixabiso == 104 || ixabiso == 108 || ixabiso == 112 || ixabiso == 116
            || ixabiso == 120 || ixabiso == 122 || ixabiso == 124 || ixabiso == 126 || ixabiso == 128 || ixabiso == 130
            || ixabiso >= 145 && ixabiso <= 147 || ixabiso == 172 || ixabiso == 176 || ixabiso == 177 || ixabiso == 190) return 1;
        return 0;
    }
    static void 클래스읽기() {
        if (inani_elipheleleyo() != 0xcafebabe) ukungaphumeleli_ixabiso("not a class file");
        int 부판 = 짧은수(), inguqulelo_ixabiso = 짧은수();
        if (inguqulelo_ixabiso < 45 || inguqulelo_ixabiso > 52 || 부판 != 0) ukungaphumeleli_ixabiso("supported class versions: 45..52, minor 0");
        상수수 = 짧은수();
        if (상수수 < 1 || 상수수 > 512) { ukungaphumeleli_ixabiso("constant pool limit (511)"); return; }
        for (int 수 = 1; 수 < 상수수 && !Impazamo; 수++) {
            int 종류 = ibhayithi_ixabiso(); engajikiyo_thega[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = inani_elipheleleyo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 짧은수();
            else if (종류 == 9 || 종류 == 10 || 종류 == 12) { 상가[수] = 짧은수(); 상나[수] = 짧은수(); }
            else ukungaphumeleli_ixabiso("unsupported constant type");
        }
        int imvume_ixabiso = 짧은수();
        if ((imvume_ixabiso & (0x200 | 0x400 | 0x2000 | 0x4000)) != 0) ukungaphumeleli_ixabiso("unsupported class flags");
        iklasi_igama = iklasi_igama_I_SMS(짧은수());
        if (!Igama_I_SMS(iklasi_igama_I_SMS(짧은수()), "java/lang/Object")) ukungaphumeleli_ixabiso("inheritance unsupported");
        if (짧은수() != 0) ukungaphumeleli_ixabiso("interfaces unsupported");
        if (짧은수() != 0) ukungaphumeleli_ixabiso("fields unsupported");
        함수수 = 짧은수();
        if (함수수 < 1 || 함수수 > 32) { ukungaphumeleli_ixabiso("method count limit (32)"); return; }
        for (int 수 = 0; 수 < 함수수 && !Impazamo; 수++) {
            imethodi_fikelela[수] = 짧은수(); imethodi_igama_I_SMS[수] = 짧은수(); imethodi_uhlobo[수] = 짧은수();
            jonga_engajikiyo(imethodi_igama_I_SMS[수], 1); 서술읽기(수);
            if ((imethodi_fikelela[수] & (0x100 | 0x400 | 0x20)) != 0) ukungaphumeleli_ixabiso("native, abstract and synchronized methods unsupported");
            if ((imethodi_fikelela[수] & 8) == 0 && !Igama_I_SMS(imethodi_igama_I_SMS[수], "<init>")) ukungaphumeleli_ixabiso("instance methods unsupported");
            if (Igama_I_SMS(imethodi_igama_I_SMS[수], "<clinit>")) ukungaphumeleli_ixabiso("class initializers unsupported");
            for (int 앞 = 0; 앞 < 수; 앞++) if (같은말(imethodi_igama_I_SMS[앞], imethodi_igama_I_SMS[수]) && 같은말(imethodi_uhlobo[앞], imethodi_uhlobo[수])) ukungaphumeleli_ixabiso("duplicate method");
            int 개수 = 짧은수();
            for (int uphawu_ixabiso = 0; uphawu_ixabiso < 개수 && !Impazamo; uphawu_ixabiso++) {
                int Igama = 짧은수(), ubude_ixabiso = inani_elipheleleyo(), Phumeza = 읽기위치;
                if (!ikliphu(Phumeza, ubude_ixabiso)) { ukungaphumeleli_ixabiso("truncated method attribute"); break; }
                if (Igama_I_SMS(Igama, "Code")) {
                    if (imethodi_qala[수] != 0) ukungaphumeleli_ixabiso("duplicate Code attribute");
                    imethodi_fumba[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = inani_elipheleleyo();
                    if (imethodi_fumba[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ukungaphumeleli_ixabiso("method memory limits exceeded");
                    imethodi_qala[수] = 읽기위치; 건너(코드길이); imethodi_phela[수] = 읽기위치;
                    if (짧은수() != 0) ukungaphumeleli_ixabiso("exception handlers unsupported");
                    속성건너();
                    if (읽기위치 != Phumeza + ubude_ixabiso) ukungaphumeleli_ixabiso("Code attribute size mismatch");
                } else 건너(ubude_ixabiso);
            }
            if (imethodi_qala[수] == 0) ukungaphumeleli_ixabiso("missing Code attribute");
            int isithuba_ufako_nkcukacha = imethodi_qala[수];
            while (isithuba_ufako_nkcukacha < imethodi_phela[수] && !Impazamo) {
                int ubude_ixabiso = umyalelo_ubude(iFayili[isithuba_ufako_nkcukacha]);
                if (ubude_ixabiso == 0 || ubude_ixabiso > imethodi_phela[수] - isithuba_ufako_nkcukacha) { ukungaphumeleli_ixabiso("unsupported or truncated bytecode"); break; }
                경계[isithuba_ufako_nkcukacha] = 수 + 1; isithuba_ufako_nkcukacha += ubude_ixabiso;
            }
            // 실행하지 않는 경로에도 잘못된 isebe 목적지를 허용하지 않는다.
            isithuba_ufako_nkcukacha = imethodi_qala[수];
            while (isithuba_ufako_nkcukacha < imethodi_phela[수] && !Impazamo) {
                int ixabiso = iFayili[isithuba_ufako_nkcukacha];
                if (ixabiso >= 153 && ixabiso <= 167 || ixabiso == 198 || ixabiso == 199) {
                    int indawo_ekuyiwa_kuyo_ixabiso = isithuba_ufako_nkcukacha + (short)(iFayili[isithuba_ufako_nkcukacha + 1] << 8 | iFayili[isithuba_ufako_nkcukacha + 2]);
                    if (indawo_ekuyiwa_kuyo_ixabiso < imethodi_qala[수] || indawo_ekuyiwa_kuyo_ixabiso >= imethodi_phela[수] || 경계[indawo_ekuyiwa_kuyo_ixabiso] != 수 + 1) ukungaphumeleli_ixabiso("invalid branch target");
                }
                isithuba_ufako_nkcukacha += umyalelo_ubude(ixabiso);
            }
        }
        if (!Impazamo) 속성건너();
        if (읽기위치 != Ubukhulu) ukungaphumeleli_ixabiso("extra class file data");
    }
    static int yabela_Ugcino(int 종류, int ubude_ixabiso) {
        if (ubude_ixabiso < 0 || ubude_ixabiso > 힙.length - 힙끝 - 2) { ukungaphumeleli_ixabiso("object heap exhausted or negative array size"); return 0; }
        int Isalathiso = 힙끝; 힙끝 += ubude_ixabiso + 2; 힙[Isalathiso] = 종류; 힙[Isalathiso + 1] = ubude_ixabiso;
        return Isalathiso;
    }
    static boolean into_ixabiso(int Isalathiso, int 종류) {
        if (Isalathiso < 1 || Isalathiso >= 힙끝 - 1 || 힙[Isalathiso] != 종류) { ukungaphumeleli_ixabiso("null or invalid object reference"); return false; }
        return true;
    }
    static int engajikiyo_I_SMS(int indeksa) {
        if (!jonga_engajikiyo(indeksa, 1)) return 0;
        if (uluhlu_lweekharektha_Isalathiso[indeksa] != 0) return uluhlu_lweekharektha_Isalathiso[indeksa];
        int Isalathiso = yabela_Ugcino(1, 상나[indeksa]); if (Impazamo) return 0;
        int 끝 = 상가[indeksa] + 상나[indeksa], 수 = 상가[indeksa], ubude_ixabiso = 0;
        while (수 < 끝 && !Impazamo) {
            int ixabiso = iFayili[수++];
            if (ixabiso == 0) ukungaphumeleli_ixabiso("invalid modified UTF-8");
            else if (ixabiso >= 192 && ixabiso <= 223 && 수 < 끝) {
                int 다음 = iFayili[수++];
                if ((다음 & 192) != 128) ukungaphumeleli_ixabiso("invalid modified UTF-8");
                ixabiso = (ixabiso & 31) << 6 | 다음 & 63;
                if (ixabiso != 0 && ixabiso < 128) ukungaphumeleli_ixabiso("overlong modified UTF-8");
            } else if (ixabiso >= 224 && ixabiso <= 239 && 수 + 1 < 끝) {
                int 가 = iFayili[수++], 나 = iFayili[수++];
                if ((가 & 192) != 128 || (나 & 192) != 128) ukungaphumeleli_ixabiso("invalid modified UTF-8");
                ixabiso = (ixabiso & 15) << 12 | (가 & 63) << 6 | 나 & 63;
                if (ixabiso < 2048) ukungaphumeleli_ixabiso("overlong modified UTF-8");
            } else if (ixabiso >= 128) ukungaphumeleli_ixabiso("invalid modified UTF-8");
            힙[Isalathiso + 2 + ubude_ixabiso++] = ixabiso;
        }
        힙[Isalathiso + 1] = ubude_ixabiso; uluhlu_lweekharektha_Isalathiso[indeksa] = Isalathiso; return Isalathiso;
    }
    static int umsingathi_ikharakhtha(String ixabiso) {
        int Isalathiso = yabela_Ugcino(1, ixabiso.length()); if (Impazamo) return 0;
        for (int 수 = 0; 수 < ixabiso.length(); 수++) 힙[Isalathiso + 2 + 수] = ixabiso.charAt(수);
        return Isalathiso;
    }
    static void bhala_I_SMS(int Isalathiso) {
        if (Isalathiso == 0) { umsebenzisi.Bhala("null"); return; }
        if (!into_ixabiso(Isalathiso, 1)) return;
        for (int 수 = 0; 수 < 힙[Isalathiso + 1]; 수++) umsebenzisi.bhala_ikharakhtha_ixabiso(힙[Isalathiso + 2 + 수]);
    }
    static int inani_ikharakhtha(int ixabiso) {
        int Isalathiso = yabela_Ugcino(1, 11); if (Impazamo) return 0;
        int ubude_ixabiso = 0;
        if (ixabiso < 0) 힙[Isalathiso + 2 + ubude_ixabiso++] = '-'; else ixabiso = -ixabiso;
        int 자리 = 1000000000; boolean Phumeza = false;
        while (자리 != 0) {
            int 수 = -(ixabiso / 자리);
            if (수 != 0 || Phumeza || 자리 == 1) { 힙[Isalathiso + 2 + ubude_ixabiso++] = '0' + 수; Phumeza = true; }
            ixabiso %= 자리; 자리 /= 10;
        }
        힙[Isalathiso + 1] = ubude_ixabiso; return Isalathiso;
    }
    static int 정수해독(int Isalathiso) {
        if (!into_ixabiso(Isalathiso, 1)) return 0;
        int ubude_ixabiso = 힙[Isalathiso + 1], 수 = 0, ixabiso = 0; boolean 음수 = false;
        if (ubude_ixabiso > 0 && (힙[Isalathiso + 2] == '-' || 힙[Isalathiso + 2] == '+')) { 음수 = 힙[Isalathiso + 2] == '-'; 수++; }
        if (수 == ubude_ixabiso) ukungaphumeleli_ixabiso("NumberFormatException");
        for (; 수 < ubude_ixabiso && !Impazamo; 수++) {
            int inani_ixabiso = 힙[Isalathiso + 2 + 수] - '0';
            if (inani_ixabiso < 0 || inani_ixabiso > 9 || ixabiso < -214748364 || ixabiso == -214748364 && inani_ixabiso > (음수 ? 8 : 7)) ukungaphumeleli_ixabiso("NumberFormatException");
            ixabiso = ixabiso * 10 - inani_ixabiso;
        }
        return 음수 ? ixabiso : -ixabiso;
    }
    static void 넣기(int ixabiso, int uhlobo_ixabiso) {
        if (Impazamo) return;
        if (ifreyim_indeksa < 0 || ifreyim_fumba[ifreyim_indeksa] >= imethodi_fumba[ifreyim_imethodi[ifreyim_indeksa]]) { ukungaphumeleli_ixabiso("operand stack overflow"); return; }
        int isithuba_ufako_nkcukacha = ifreyim_indeksa * 128 + ifreyim_fumba[ifreyim_indeksa]++; 스택값[isithuba_ufako_nkcukacha] = ixabiso; 스택형[isithuba_ufako_nkcukacha] = uhlobo_ixabiso;
    }
    static int 빼기(int uhlobo_ixabiso) {
        if (Impazamo) return 0;
        if (ifreyim_indeksa < 0 || ifreyim_fumba[ifreyim_indeksa] < 1) { ukungaphumeleli_ixabiso("operand stack underflow"); return 0; }
        int isithuba_ufako_nkcukacha = ifreyim_indeksa * 128 + --ifreyim_fumba[ifreyim_indeksa]; 반환형 = 스택형[isithuba_ufako_nkcukacha];
        if (uhlobo_ixabiso != 0 && 반환형 != uhlobo_ixabiso) ukungaphumeleli_ixabiso("operand type mismatch");
        return 스택값[isithuba_ufako_nkcukacha];
    }
    static void 지역읽기(int indeksa, int uhlobo_ixabiso) {
        if (indeksa >= 함수지역[ifreyim_imethodi[ifreyim_indeksa]] || indeksa < 0 || eyale_ndawo_uhlobo[ifreyim_indeksa * 128 + indeksa] != uhlobo_ixabiso) { ukungaphumeleli_ixabiso("invalid or uninitialized local"); return; }
        넣기(eyale_ndawo_ixabiso[ifreyim_indeksa * 128 + indeksa], uhlobo_ixabiso);
    }
    static void bhala_eyale_ndawo(int indeksa, int uhlobo_ixabiso) {
        if (indeksa >= 함수지역[ifreyim_imethodi[ifreyim_indeksa]] || indeksa < 0) { ukungaphumeleli_ixabiso("local index out of range"); return; }
        int ixabiso = 빼기(uhlobo_ixabiso); eyale_ndawo_ixabiso[ifreyim_indeksa * 128 + indeksa] = ixabiso; eyale_ndawo_uhlobo[ifreyim_indeksa * 128 + indeksa] = uhlobo_ixabiso;
    }
    static int 명바() {
        int 위치 = 틀위치[ifreyim_indeksa];
        if (위치 < imethodi_qala[ifreyim_imethodi[ifreyim_indeksa]] || 위치 >= imethodi_phela[ifreyim_imethodi[ifreyim_indeksa]]) { ukungaphumeleli_ixabiso("instruction pointer out of range"); return 0; }
        틀위치[ifreyim_indeksa]++; return iFayili[위치];
    }
    static int 명짧() { return 명바() << 8 | 명바(); }
    static void fudusa_ixabiso(int 위치) {
        int INKQUBO_ixabiso = ifreyim_imethodi[ifreyim_indeksa];
        if (위치 < imethodi_qala[INKQUBO_ixabiso] || 위치 >= imethodi_phela[INKQUBO_ixabiso] || 경계[위치] != INKQUBO_ixabiso + 1) ukungaphumeleli_ixabiso("invalid branch target");
        else 틀위치[ifreyim_indeksa] = 위치;
    }
    static void 호출(int INKQUBO_ixabiso) {
        if (ifreyim_indeksa == 31) { ukungaphumeleli_ixabiso("call stack limit (32)"); return; }
        int 다음 = ifreyim_indeksa + 1;
        for (int 수 = 0; 수 < 128; 수++) eyale_ndawo_uhlobo[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[INKQUBO_ixabiso] - 1; 수 >= 0; 수--) {
            eyale_ndawo_ixabiso[다음 * 128 + 수] = 빼기(imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수]); eyale_ndawo_uhlobo[다음 * 128 + 수] = imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수];
        }
        ifreyim_indeksa = 다음; ifreyim_imethodi[ifreyim_indeksa] = INKQUBO_ixabiso; 틀위치[ifreyim_indeksa] = imethodi_qala[INKQUBO_ixabiso]; ifreyim_fumba[ifreyim_indeksa] = 0;
    }
    static void 반환(int uhlobo_ixabiso) {
        if (uhlobo_ixabiso != 함수반환[ifreyim_imethodi[ifreyim_indeksa]]) { ukungaphumeleli_ixabiso("return type mismatch"); return; }
        int ixabiso = uhlobo_ixabiso == 0 ? 0 : 빼기(uhlobo_ixabiso);
        ifreyim_indeksa--; if (ifreyim_indeksa >= 0 && uhlobo_ixabiso != 0) 넣기(ixabiso, uhlobo_ixabiso);
    }
    static int[] Stream_ifayile_igama = new int[64];
    static void ifayile_Stream_fowuna(int umnini_ixabiso, int Igama, int fomatha_ixabiso, int Umyalelo) {
        boolean 출력 = Igama_I_SMS(umnini_ixabiso, "java/io/FileOutputStream");
        int 종류 = 출력 ? 6 : 5;
        if (Umyalelo == 183 && Igama_I_SMS(Igama, "<init>")) {
            boolean 이어 = false;
            if (출력 && Igama_I_SMS(fomatha_ixabiso, "(Ljava/lang/String;Z)V")) 이어 = 빼기(1) != 0;
            else if (!Igama_I_SMS(fomatha_ixabiso, "(Ljava/lang/String;)V")) { ukungaphumeleli_ixabiso("unsupported file stream constructor"); return; }
            int ifayile_ufako_nkcukacha_igama = 빼기(2), Stream_ixabiso = 빼기(2);
            if (!into_ixabiso(ifayile_ufako_nkcukacha_igama, 1) || !into_ixabiso(Stream_ixabiso, 종류) || Impazamo) return;
            if (힙[Stream_ixabiso + 3] != 0) { ukungaphumeleli_ixabiso("file stream already initialized"); return; }
            int ubude_ixabiso = 힙[ifayile_ufako_nkcukacha_igama + 1];
            if (ubude_ixabiso < 1 || ubude_ixabiso > 63) { ukungaphumeleli_ixabiso("invalid file name length"); return; }
            for (int isithuba_ufako_nkcukacha = 0; isithuba_ufako_nkcukacha < ubude_ixabiso; isithuba_ufako_nkcukacha++) {
                int ixabiso = 힙[ifayile_ufako_nkcukacha_igama + 2 + isithuba_ufako_nkcukacha];
                if (ixabiso < 1 || ixabiso > 127) { ukungaphumeleli_ixabiso("file stream paths currently require ASCII"); return; }
                Stream_ifayile_igama[isithuba_ufako_nkcukacha] = ixabiso;
            }
            Stream_ifayile_igama[ubude_ixabiso] = 0;
            int 서술자 = umsebenzisi.파일서술자열기(Stream_ifayile_igama, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ukungaphumeleli_ixabiso("FileNotFoundException: file open failed"); return; }
            힙[Stream_ixabiso + 2] = 서술자; 힙[Stream_ixabiso + 3] = 1;
            return;
        }
        if (Umyalelo != 182) { ukungaphumeleli_ixabiso("invalid file stream invocation"); return; }
        int Intshukumo = -1, ixabiso = 0;
        if (Igama_I_SMS(Igama, "close") && Igama_I_SMS(fomatha_ixabiso, "()V")) Intshukumo = 0;
        if (!출력 && Igama_I_SMS(Igama, "read") && Igama_I_SMS(fomatha_ixabiso, "()I")) Intshukumo = 1;
        if (출력 && Igama_I_SMS(Igama, "write") && Igama_I_SMS(fomatha_ixabiso, "(I)V")) { Intshukumo = 2; ixabiso = 빼기(1); }
        if (Intshukumo < 0) { ukungaphumeleli_ixabiso("unsupported file stream method"); return; }
        int Stream_ixabiso = 빼기(2);
        if (!into_ixabiso(Stream_ixabiso, 종류) || Impazamo) return;
        if (힙[Stream_ixabiso + 3] == 0) { ukungaphumeleli_ixabiso("uninitialized file stream"); return; }
        int 서술자 = 힙[Stream_ixabiso + 2];
        if (Intshukumo == 0) {
            if (서술자 >= 0 && umsebenzisi.파일서술자닫기(서술자) < 0) ukungaphumeleli_ixabiso("IOException: close failed");
            힙[Stream_ixabiso + 2] = -1; return;
        }
        if (서술자 < 0) { ukungaphumeleli_ixabiso("IOException: stream closed"); return; }
        if (Intshukumo == 1) {
            int 결과 = umsebenzisi.파일한바이트읽기(서술자);
            if (결과 < -1) ukungaphumeleli_ixabiso("IOException: read failed"); else 넣기(결과, 1);
        } else if (umsebenzisi.파일한바이트쓰기(서술자, ixabiso) != 1) ukungaphumeleli_ixabiso("IOException: write failed");
    }
    static void fowuna_imethodi(int indeksa, int Umyalelo) {
        if (!jonga_engajikiyo(indeksa, 10)) return;
        int umnini_ixabiso = iklasi_igama_I_SMS(상가[indeksa]), Igama = Isalathiso_igama(상나[indeksa]), fomatha_ixabiso = Isalathiso_uhlobo(상나[indeksa]);
        if (Impazamo) return;
        if (같은말(umnini_ixabiso, iklasi_igama)) {
            if (Umyalelo != 184) { ukungaphumeleli_ixabiso("only static user methods are supported"); return; }
            for (int 수 = 0; 수 < 함수수; 수++) if (같은말(Igama, imethodi_igama_I_SMS[수]) && 같은말(fomatha_ixabiso, imethodi_uhlobo[수])) {
                if ((imethodi_fikelela[수] & 8) == 0) ukungaphumeleli_ixabiso("method is not static"); else 호출(수);
                return;
            }
            ukungaphumeleli_ixabiso("NoSuchMethodError"); return;
        }
        if (Igama_I_SMS(umnini_ixabiso, "java/io/FileInputStream") || Igama_I_SMS(umnini_ixabiso, "java/io/FileOutputStream")) {
            ifayile_Stream_fowuna(umnini_ixabiso, Igama, fomatha_ixabiso, Umyalelo); return;
        }
        if (Umyalelo == 184 && Igama_I_SMS(umnini_ixabiso, "java/lang/Integer") && Igama_I_SMS(Igama, "parseInt") && Igama_I_SMS(fomatha_ixabiso, "(Ljava/lang/String;)I")) {
            넣기(정수해독(빼기(2)), 1); return;
        }
        if (Umyalelo == 182 && Igama_I_SMS(umnini_ixabiso, "java/io/PrintStream") && (Igama_I_SMS(Igama, "println") || Igama_I_SMS(Igama, "print"))) {
            int uhlobo_ixabiso = 0, ixabiso = 0;
            if (Igama_I_SMS(fomatha_ixabiso, "(I)V")) { uhlobo_ixabiso = 1; ixabiso = 빼기(1); }
            else if (Igama_I_SMS(fomatha_ixabiso, "(Z)V")) { uhlobo_ixabiso = 2; ixabiso = 빼기(1); }
            else if (Igama_I_SMS(fomatha_ixabiso, "(C)V")) { uhlobo_ixabiso = 3; ixabiso = 빼기(1); }
            else if (Igama_I_SMS(fomatha_ixabiso, "(Ljava/lang/String;)V")) { uhlobo_ixabiso = 4; ixabiso = 빼기(2); }
            else if (!Igama_I_SMS(fomatha_ixabiso, "()V") || !Igama_I_SMS(Igama, "println")) ukungaphumeleli_ixabiso("unsupported print descriptor");
            if (빼기(2) != -1) ukungaphumeleli_ixabiso("invalid PrintStream receiver");
            if (Impazamo) return;
            if (uhlobo_ixabiso == 1) 자바도구.수쓰기(ixabiso);
            if (uhlobo_ixabiso == 2) umsebenzisi.Bhala(ixabiso == 0 ? "false" : "true");
            if (uhlobo_ixabiso == 3) umsebenzisi.bhala_ikharakhtha_ixabiso(ixabiso & 65535);
            if (uhlobo_ixabiso == 4) bhala_I_SMS(ixabiso);
            if (Igama_I_SMS(Igama, "println")) umsebenzisi.bhala_ikharakhtha_ixabiso(10);
            return;
        }
        if (Umyalelo == 182 && Igama_I_SMS(umnini_ixabiso, "java/lang/String")) {
            if (Igama_I_SMS(Igama, "length") && Igama_I_SMS(fomatha_ixabiso, "()I")) {
                int Isalathiso = 빼기(2); if (into_ixabiso(Isalathiso, 1)) 넣기(힙[Isalathiso + 1], 1); return;
            }
            if (Igama_I_SMS(Igama, "charAt") && Igama_I_SMS(fomatha_ixabiso, "(I)C")) {
                int umbhalo_omncinane_ixabiso = 빼기(1), Isalathiso = 빼기(2);
                if (into_ixabiso(Isalathiso, 1)) {
                    if (umbhalo_omncinane_ixabiso < 0 || umbhalo_omncinane_ixabiso >= 힙[Isalathiso + 1]) ukungaphumeleli_ixabiso("StringIndexOutOfBoundsException"); else 넣기(힙[Isalathiso + 2 + umbhalo_omncinane_ixabiso], 1);
                }
                return;
            }
        }
        if (Igama_I_SMS(umnini_ixabiso, "java/lang/StringBuilder")) {
            if (Umyalelo == 183 && Igama_I_SMS(Igama, "<init>") && Igama_I_SMS(fomatha_ixabiso, "()V")) { into_ixabiso(빼기(2), 4); return; }
            if (Umyalelo == 182 && Igama_I_SMS(Igama, "toString") && Igama_I_SMS(fomatha_ixabiso, "()Ljava/lang/String;")) {
                int Isalathiso = 빼기(2); if (into_ixabiso(Isalathiso, 4)) 넣기(힙[Isalathiso + 2] == 0 ? umsingathi_ikharakhtha("") : 힙[Isalathiso + 2], 2); return;
            }
            if (Umyalelo == 182 && Igama_I_SMS(Igama, "append")) {
                int Umbhalo = 0;
                if (Igama_I_SMS(fomatha_ixabiso, "(I)Ljava/lang/StringBuilder;")) Umbhalo = inani_ikharakhtha(빼기(1));
                else if (Igama_I_SMS(fomatha_ixabiso, "(Z)Ljava/lang/StringBuilder;")) Umbhalo = umsingathi_ikharakhtha(빼기(1) == 0 ? "false" : "true");
                else if (Igama_I_SMS(fomatha_ixabiso, "(C)Ljava/lang/StringBuilder;")) {
                    int ixabiso = 빼기(1); Umbhalo = yabela_Ugcino(1, 1); if (!Impazamo) 힙[Umbhalo + 2] = ixabiso & 65535;
                }
                else if (Igama_I_SMS(fomatha_ixabiso, "(Ljava/lang/String;)Ljava/lang/StringBuilder;")) { Umbhalo = 빼기(2); if (Umbhalo == 0) Umbhalo = umsingathi_ikharakhtha("null"); }
                else { ukungaphumeleli_ixabiso("unsupported StringBuilder append"); return; }
                int Isalathiso = 빼기(2); if (!into_ixabiso(Isalathiso, 4) || !into_ixabiso(Umbhalo, 1)) return;
                int 앞 = 힙[Isalathiso + 2], 앞길이 = 앞 == 0 ? 0 : 힙[앞 + 1], Emva_ixabiso_ubude = 힙[Umbhalo + 1];
                int 새글 = yabela_Ugcino(1, 앞길이 + Emva_ixabiso_ubude); if (Impazamo) return;
                for (int 수 = 0; 수 < 앞길이; 수++) 힙[새글 + 2 + 수] = 힙[앞 + 2 + 수];
                for (int 수 = 0; 수 < Emva_ixabiso_ubude; 수++) 힙[새글 + 2 + 앞길이 + 수] = 힙[Umbhalo + 2 + 수];
                힙[Isalathiso + 2] = 새글; 넣기(Isalathiso, 2); return;
            }
        }
        ukungaphumeleli_ixabiso("unsupported library method");
    }
    static int ULUHLU_isithuba(int Isalathiso, int umbhalo_omncinane_ixabiso, int uhlobo_ixabiso) {
        if (!into_ixabiso(Isalathiso, uhlobo_ixabiso)) return 0;
        if (umbhalo_omncinane_ixabiso < 0 || umbhalo_omncinane_ixabiso >= 힙[Isalathiso + 1]) { ukungaphumeleli_ixabiso("ArrayIndexOutOfBoundsException"); return 0; }
        return Isalathiso + 2 + umbhalo_omncinane_ixabiso;
    }
    static void ukwenza_umyalelo() {
        int 남음 = 500000;
        while (ifreyim_indeksa >= 0 && !Impazamo) {
            if (--남음 == 0) { ukungaphumeleli_ixabiso("instruction limit (500000)"); break; }
            int Phumeza = 틀위치[ifreyim_indeksa], ixabiso = 명바();
            if (Impazamo) break;
            if (ixabiso == 0) continue;
            if (ixabiso == 1) { 넣기(0, 2); continue; }
            if (ixabiso >= 2 && ixabiso <= 8) { 넣기(ixabiso - 3, 1); continue; }
            if (ixabiso == 16) { 넣기((byte)명바(), 1); continue; }
            if (ixabiso == 17) { 넣기((short)명짧(), 1); continue; }
            if (ixabiso == 18 || ixabiso == 19) {
                int 수 = ixabiso == 18 ? 명바() : 명짧();
                if (수 <= 0 || 수 >= 상수수) ukungaphumeleli_ixabiso("invalid ldc constant");
                else if (engajikiyo_thega[수] == 3) 넣기(상가[수], 1);
                else if (engajikiyo_thega[수] == 8) 넣기(engajikiyo_I_SMS(상가[수]), 2);
                else ukungaphumeleli_ixabiso("unsupported ldc constant");
                continue;
            }
            if (ixabiso == 21 || ixabiso == 25) { 지역읽기(명바(), ixabiso == 21 ? 1 : 2); continue; }
            if (ixabiso >= 26 && ixabiso <= 29) { 지역읽기(ixabiso - 26, 1); continue; }
            if (ixabiso >= 42 && ixabiso <= 45) { 지역읽기(ixabiso - 42, 2); continue; }
            if (ixabiso == 54 || ixabiso == 58) { bhala_eyale_ndawo(명바(), ixabiso == 54 ? 1 : 2); continue; }
            if (ixabiso >= 59 && ixabiso <= 62) { bhala_eyale_ndawo(ixabiso - 59, 1); continue; }
            if (ixabiso >= 75 && ixabiso <= 78) { bhala_eyale_ndawo(ixabiso - 75, 2); continue; }
            if (ixabiso == 46 || ixabiso == 50) {
                int umbhalo_omncinane_ixabiso = 빼기(1), Isalathiso = 빼기(2), isithuba_ufako_nkcukacha = ULUHLU_isithuba(Isalathiso, umbhalo_omncinane_ixabiso, ixabiso == 46 ? 2 : 3);
                if (!Impazamo) 넣기(힙[isithuba_ufako_nkcukacha], ixabiso == 46 ? 1 : 2); continue;
            }
            if (ixabiso == 79 || ixabiso == 83) {
                int into_ielement = 빼기(ixabiso == 79 ? 1 : 2), umbhalo_omncinane_ixabiso = 빼기(1), Isalathiso = 빼기(2), isithuba_ufako_nkcukacha = ULUHLU_isithuba(Isalathiso, umbhalo_omncinane_ixabiso, ixabiso == 79 ? 2 : 3);
                if (ixabiso == 83 && into_ielement != 0) into_ixabiso(into_ielement, 1);
                if (!Impazamo) 힙[isithuba_ufako_nkcukacha] = into_ielement; continue;
            }
            if (ixabiso == 87) { 빼기(0); continue; }
            if (ixabiso == 89) { int 가 = 빼기(0), uhlobo_ixabiso = 반환형; 넣기(가, uhlobo_ixabiso); 넣기(가, uhlobo_ixabiso); continue; }
            if (ixabiso == 95) { int 가 = 빼기(0), 가형 = 반환형, 나 = 빼기(0), 나형 = 반환형; 넣기(가, 가형); 넣기(나, 나형); continue; }
            if (ixabiso == 96 || ixabiso == 100 || ixabiso == 104 || ixabiso == 108 || ixabiso == 112 || ixabiso == 120
                || ixabiso == 122 || ixabiso == 124 || ixabiso == 126 || ixabiso == 128 || ixabiso == 130) {
                int 나 = 빼기(1), 가 = 빼기(1), 결과 = 0;
                if ((ixabiso == 108 || ixabiso == 112) && 나 == 0) { ukungaphumeleli_ixabiso("ArithmeticException: / by zero"); continue; }
                if (ixabiso == 96) 결과 = 가 + 나;
                if (ixabiso == 100) 결과 = 가 - 나;
                if (ixabiso == 104) 결과 = 가 * 나;
                if (ixabiso == 108) 결과 = 가 / 나;
                if (ixabiso == 112) 결과 = 가 % 나;
                if (ixabiso == 120) 결과 = 가 << 나;
                if (ixabiso == 122) 결과 = 가 >> 나;
                if (ixabiso == 124) 결과 = 가 >>> 나;
                if (ixabiso == 126) 결과 = 가 & 나;
                if (ixabiso == 128) 결과 = 가 | 나;
                if (ixabiso == 130) 결과 = 가 ^ 나;
                넣기(결과, 1); continue;
            }
            if (ixabiso == 116) { 넣기(-빼기(1), 1); continue; }
            if (ixabiso == 132) {
                int eyale_ndawo_umda = 명바(), 증분 = (byte)명바(); 지역읽기(eyale_ndawo_umda, 1); 넣기(빼기(1) + 증분, 1); bhala_eyale_ndawo(eyale_ndawo_umda, 1); continue;
            }
            if (ixabiso >= 145 && ixabiso <= 147) {
                int 수 = 빼기(1); 넣기(ixabiso == 145 ? (byte)수 : ixabiso == 146 ? (char)수 : (short)수, 1); continue;
            }
            if (ixabiso >= 153 && ixabiso <= 167 || ixabiso == 198 || ixabiso == 199) {
                int indawo_ekuyiwa_kuyo_ixabiso = Phumeza + (short)명짧(); boolean 갈까 = ixabiso == 167;
                if (ixabiso >= 153 && ixabiso <= 158) {
                    int 수 = 빼기(1); 갈까 = ixabiso == 153 ? 수 == 0 : ixabiso == 154 ? 수 != 0 : ixabiso == 155 ? 수 < 0 : ixabiso == 156 ? 수 >= 0 : ixabiso == 157 ? 수 > 0 : 수 <= 0;
                } else if (ixabiso >= 159 && ixabiso <= 166) {
                    int 나 = 빼기(ixabiso >= 165 ? 2 : 1), 가 = 빼기(ixabiso >= 165 ? 2 : 1);
                    갈까 = ixabiso == 159 || ixabiso == 165 ? 가 == 나 : ixabiso == 160 || ixabiso == 166 ? 가 != 나 : ixabiso == 161 ? 가 < 나 : ixabiso == 162 ? 가 >= 나 : ixabiso == 163 ? 가 > 나 : 가 <= 나;
                } else if (ixabiso == 198 || ixabiso == 199) { int 수 = 빼기(2); 갈까 = ixabiso == 198 ? 수 == 0 : 수 != 0; }
                if (갈까) fudusa_ixabiso(indawo_ekuyiwa_kuyo_ixabiso); continue;
            }
            if (ixabiso == 172 || ixabiso == 176 || ixabiso == 177) { 반환(ixabiso == 172 ? 1 : ixabiso == 176 ? 2 : 0); continue; }
            if (ixabiso == 178) {
                int 수 = 명짧(); if (!jonga_engajikiyo(수, 9)) continue;
                if (!Igama_I_SMS(iklasi_igama_I_SMS(상가[수]), "java/lang/System") || !Igama_I_SMS(Isalathiso_igama(상나[수]), "out")
                    || !Igama_I_SMS(Isalathiso_uhlobo(상나[수]), "Ljava/io/PrintStream;")) ukungaphumeleli_ixabiso("unsupported static field");
                else 넣기(-1, 2); continue;
            }
            if (ixabiso == 182 || ixabiso == 183 || ixabiso == 184) { fowuna_imethodi(명짧(), ixabiso); continue; }
            if (ixabiso == 187) {
                int Igama = iklasi_igama_I_SMS(명짧());
                if (Igama_I_SMS(Igama, "java/lang/StringBuilder")) 넣기(yabela_Ugcino(4, 1), 2);
                else if (Igama_I_SMS(Igama, "java/io/FileInputStream") || Igama_I_SMS(Igama, "java/io/FileOutputStream")) {
                    int Isalathiso = yabela_Ugcino(Igama_I_SMS(Igama, "java/io/FileOutputStream") ? 6 : 5, 2);
                    if (!Impazamo) { 힙[Isalathiso + 2] = -1; 넣기(Isalathiso, 2); }
                } else ukungaphumeleli_ixabiso("unsupported object construction");
                continue;
            }
            if (ixabiso == 188 || ixabiso == 189) {
                if (ixabiso == 188) { if (명바() != 10) ukungaphumeleli_ixabiso("only int[] newarray is supported"); }
                else if (!Igama_I_SMS(iklasi_igama_I_SMS(명짧()), "java/lang/String")) ukungaphumeleli_ixabiso("only String[] anewarray is supported");
                int ubude_ixabiso = 빼기(1); 넣기(yabela_Ugcino(ixabiso == 188 ? 2 : 3, ubude_ixabiso), 2); continue;
            }
            if (ixabiso == 190) {
                int Isalathiso = 빼기(2);
                if (Isalathiso < 1 || Isalathiso >= 힙끝 - 1 || (힙[Isalathiso] != 2 && 힙[Isalathiso] != 3)) ukungaphumeleli_ixabiso("null or invalid array");
                else 넣기(힙[Isalathiso + 1], 1); continue;
            }
            if (ixabiso == 192) {
                int Igama = iklasi_igama_I_SMS(명짧()), Isalathiso = 빼기(2);
                if (!Igama_I_SMS(Igama, "java/lang/String")) ukungaphumeleli_ixabiso("unsupported checkcast");
                else if (Isalathiso != 0) into_ixabiso(Isalathiso, 1);
                넣기(Isalathiso, 2); continue;
            }
            ukungaphumeleli_ixabiso("unsupported bytecode");
        }
    }
    public static int Phumeza() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros JVM 0.1 (class 45..52 subset; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() < 1) { umsebenzisi.Bhala("Usage: java CLASS [ARGS]\n"); return 2; }
        int ubude_ixabiso = 자바도구.Igama(ifayile_igama_I_SMS, umsebenzisi.인수(0));
        if (ubude_ixabiso < 1 || ubude_ixabiso > 57) { umsebenzisi.Bhala("java: invalid class name\n"); return 2; }
        ifayile_igama_I_SMS[ubude_ixabiso] = '.'; ifayile_igama_I_SMS[ubude_ixabiso + 1] = 'c'; ifayile_igama_I_SMS[ubude_ixabiso + 2] = 'l'; ifayile_igama_I_SMS[ubude_ixabiso + 3] = 'a'; ifayile_igama_I_SMS[ubude_ixabiso + 4] = 's'; ifayile_igama_I_SMS[ubude_ixabiso + 5] = 's';
        Ubukhulu = umsebenzisi.파일읽기(ifayile_igama_I_SMS, iFayili);
        if (Ubukhulu < 0) { umsebenzisi.Bhala("java: cannot read class: "); 자바도구.수쓰기(Ubukhulu); umsebenzisi.bhala_ikharakhtha_ixabiso(10); return 1; }
        클래스읽기(); if (Impazamo) return 1;
        int ikharakhtha_igama = engajikiyo_I_SMS(iklasi_igama);
        if (!Impazamo && 힙[ikharakhtha_igama + 1] != ubude_ixabiso) ukungaphumeleli_ixabiso("class name does not match file");
        for (int 수 = 0; 수 < ubude_ixabiso && !Impazamo; 수++) if (힙[ikharakhtha_igama + 2 + 수] != ifayile_igama_I_SMS[수]) ukungaphumeleli_ixabiso("class name does not match file");
        int ufako_nkcukacha_inqaku_ixabiso = -1;
        for (int 수 = 0; 수 < 함수수; 수++) if (Igama_I_SMS(imethodi_igama_I_SMS[수], "main") && Igama_I_SMS(imethodi_uhlobo[수], "([Ljava/lang/String;)V") && (imethodi_fikelela[수] & 9) == 9) ufako_nkcukacha_inqaku_ixabiso = 수;
        if (ufako_nkcukacha_inqaku_ixabiso < 0) ukungaphumeleli_ixabiso("public static void main(String[] args) required");
        if (Impazamo) return 1;
        int 인수 = yabela_Ugcino(3, umsebenzisi.인수개수() - 1);
        for (int 수 = 1; 수 < umsebenzisi.인수개수() && !Impazamo; 수++) 힙[인수 + 1 + 수] = umsingathi_ikharakhtha(umsebenzisi.인수(수));
        ifreyim_indeksa = 0; ifreyim_imethodi[0] = ufako_nkcukacha_inqaku_ixabiso; 틀위치[0] = imethodi_qala[ufako_nkcukacha_inqaku_ixabiso]; eyale_ndawo_ixabiso[0] = 인수; eyale_ndawo_uhlobo[0] = 2;
        ukwenza_umyalelo(); return Impazamo ? 1 : 0;
    }
}
