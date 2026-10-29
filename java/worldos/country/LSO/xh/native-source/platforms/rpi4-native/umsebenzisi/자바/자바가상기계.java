// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** ARM64 EL0에서 동작하는 제한형 JVM. iFayili/스택/Isalathiso/isebe 경계를 ukwenza_umyalelo 중 검사한다. */
public final class 자바가상기계 {
    static int[] iFayili = new int[16 * 16384], 임시파일 = new int[16384], ifayile_igama_I_SMS = new int[512];
    static int[] engajikiyo_thega = new int[8192], 상가 = new int[8192], 상나 = new int[8192], uluhlu_lweekharektha_Isalathiso = new int[8192];
    static int[] imethodi_igama_I_SMS = new int[512], imethodi_uhlobo = new int[512], imethodi_fikelela = new int[512], imethodi_umnini = new int[512];
    static int[] imethodi_qala = new int[512], imethodi_phela = new int[512], imethodi_fumba = new int[512], 함수지역 = new int[512];
    static int[] 함수인수수 = new int[512], imethodi_isiniki_myalelo_uhlobo = new int[8192], 함수반환 = new int[512];
    static int[] 경계 = new int[16 * 16384];
    static int[] eyale_ndawo_ixabiso = new int[16384], eyale_ndawo_uhlobo = new int[16384], 스택값 = new int[16384], 스택형 = new int[16384];
    static int[] ifreyim_imethodi = new int[128], 틀위치 = new int[128], ifreyim_fumba = new int[128], ifreyim_umyalelo = new int[128], qalisa_umsebenzi_ifreyim = new int[128];
    static int[] iklasi_Ingcaciso_igama = new int[16], iklasi_Ingcaciso_isayizi = new int[16], 종부모 = new int[16], iklasi_Ingcaciso_imo = new int[16], 종칸수 = new int[16], qalisa_umsebenzi_iklasi_Ingcaciso = new int[16];
    static int[] iklasi_isinxulumanisi = new int[16 * 16], 종접면수 = new int[16];
    static int[] isithuba_igama = new int[512], isithuba_uhlobo = new int[512], isithuba_umnini = new int[512], isithuba_iimvume = new int[512], 칸위치 = new int[512], isithuba_iingcombolo = new int[512];
    static int[] 잡기시작 = new int[1024], 잡기끝 = new int[1024], 잡기위치 = new int[1024], 잡기종 = new int[1024], 잡기함수 = new int[1024];
    static int[] 힙 = new int[32768], 힙폭 = new int[32768], 힙표시 = new int[32768], 힙참조 = new int[32768], 표시대기 = new int[32768];
    static int[] 잠시참조 = new int[256], ULUHLU_ielement = new int[32768], Store_inani_elipheleleyo = new int[256];
    static int Ubukhulu, 읽기위치, 함수수, iklasi_igama, ifreyim_indeksa = -1, 힙끝 = 1, 반환형;
    static int 종수, 칸수, 잡기수, 현재읽는종, 던진객체, 잠시수, 표시수, 수거횟수;
    static int 현재가닥, 가닥수 = 1, ufako_nkcukacha_iklasi_Ingcaciso;
    static int[] ithredi_ifreyim = new int[4], ithredi_imo = new int[4], ithredi_into = new int[4], ithredi_ithagethi = new int[4], 가닥대기 = new int[4];
    static boolean Impazamo, 바꿈요청;
    static int[] 잠금주인 = new int[32768], 잠금깊이 = new int[32768], 틀잠금 = new int[128], 종잠금 = new int[16], iklasi_ithredi = new int[16];

    static void ukungaphumeleli_ixabiso(String Igama_I_SMS) {
        if (Impazamo) return;
        int 분류코드 = 0;
        if (자바도구.같음(Igama_I_SMS, "ArithmeticException: / by zero")) 분류코드 = 4;
        if (자바도구.같음(Igama_I_SMS, "NullPointerException") || 자바도구.같음(Igama_I_SMS, "null or invalid array")) 분류코드 = 5;
        if (자바도구.같음(Igama_I_SMS, "ArrayIndexOutOfBoundsException")) 분류코드 = 7;
        if (자바도구.같음(Igama_I_SMS, "StringIndexOutOfBoundsException")) 분류코드 = 8;
        if (자바도구.같음(Igama_I_SMS, "NumberFormatException")) 분류코드 = 10;
        if (자바도구.같음(Igama_I_SMS, "FileNotFoundException: file open failed")) 분류코드 = 12;
        if (자바도구.같음(Igama_I_SMS, "IOException: stream closed") || 자바도구.같음(Igama_I_SMS, "IOException: read failed") || 자바도구.같음(Igama_I_SMS, "IOException: write failed")) 분류코드 = 11;
        if (자바도구.같음(Igama_I_SMS, "ClassCastException")) 분류코드 = 14;
        if (자바도구.같음(Igama_I_SMS, "NegativeArraySizeException")) 분류코드 = 15;
        if (분류코드 != 0 && ifreyim_indeksa >= 0) { 예외던짐(분류코드, Igama_I_SMS); return; }
        umsebenzisi.Bhala("JVM error: "); umsebenzisi.Bhala(Igama_I_SMS); umsebenzisi.bhala_ikharakhtha_ixabiso(10); Impazamo = true;
    }
    static boolean ikliphu(int Phumeza, int ubude_ixabiso) {
        if (Phumeza < 0 || Phumeza >= iFayili.length || ubude_ixabiso < 0) return false;
        int iklasi_Ingcaciso = Phumeza / 16384;
        return Phumeza % 16384 <= iklasi_Ingcaciso_isayizi[iklasi_Ingcaciso] && ubude_ixabiso <= iklasi_Ingcaciso_isayizi[iklasi_Ingcaciso] - Phumeza % 16384;
    }
    static int ibhayithi_ixabiso() {
        if (!ikliphu(읽기위치, 1)) { ukungaphumeleli_ixabiso("truncated class file"); return 0; }
        return iFayili[읽기위치++];
    }
    static int 짧은수() { return ibhayithi_ixabiso() << 8 | ibhayithi_ixabiso(); }
    static int inani_elipheleleyo() { return 짧은수() << 16 | 짧은수(); }
    static void 건너(int ubude_ixabiso) { if (!ikliphu(읽기위치, ubude_ixabiso)) ukungaphumeleli_ixabiso("invalid attribute size"); else 읽기위치 += ubude_ixabiso; }
    static boolean jonga_engajikiyo(int 수, int 종류) {
        if (수 <= 0 || 수 >= engajikiyo_thega.length || engajikiyo_thega[수] != 종류) { ukungaphumeleli_ixabiso("invalid constant pool reference"); return false; }
        return true;
    }
    static boolean 구간(int Phumeza, int ubude_ixabiso, String Igama_I_SMS) {
        if (!ikliphu(Phumeza, ubude_ixabiso)) return false;
        int 읽는자리 = Phumeza, 끝 = Phumeza + ubude_ixabiso;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Igama_I_SMS.length(); iluphu_indeksa++) {
            int ikhowudi_yekharakhtha = Igama_I_SMS.charAt(iluphu_indeksa);
            if (ikhowudi_yekharakhtha > 0 && ikhowudi_yekharakhtha < 128) { if (읽는자리 >= 끝 || iFayili[읽는자리++] != ikhowudi_yekharakhtha) return false; }
            else if (ikhowudi_yekharakhtha < 2048) {
                if (읽는자리 + 2 > 끝 || iFayili[읽는자리++] != (192 | (ikhowudi_yekharakhtha >> 6)) || iFayili[읽는자리++] != (128 | (ikhowudi_yekharakhtha & 63))) return false;
            } else if (읽는자리 + 3 > 끝 || iFayili[읽는자리++] != (224 | (ikhowudi_yekharakhtha >> 12)) || iFayili[읽는자리++] != (128 | ((ikhowudi_yekharakhtha >> 6) & 63)) || iFayili[읽는자리++] != (128 | (ikhowudi_yekharakhtha & 63))) return false;
        }
        return 읽는자리 == 끝;
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
    static int 상번호() { int ixabiso = 짧은수(); return ixabiso == 0 ? 0 : 현재읽는종 * 512 + ixabiso; }
    static int 명상수() { return imethodi_umnini[ifreyim_imethodi[ifreyim_indeksa]] * 512 + 명짧(); }
    static void 속성건너() {
        int 개수 = 짧은수();
        for (int 수 = 0; 수 < 개수 && !Impazamo; 수++) { jonga_engajikiyo(상번호(), 1); 건너(inani_elipheleleyo()); }
    }
    static int umyalelo_ubude(int ixabiso) {
        if (ixabiso == 16 || ixabiso == 18 || ixabiso == 21 || ixabiso == 25 || ixabiso == 54 || ixabiso == 58 || ixabiso == 188) return 2;
        if (ixabiso == 17 || ixabiso == 19 || ixabiso == 132 || ixabiso >= 153 && ixabiso <= 167
            || ixabiso >= 178 && ixabiso <= 184 || ixabiso == 187 || ixabiso == 189 || ixabiso == 192 || ixabiso == 193 || ixabiso == 198 || ixabiso == 199) return 3;
        if (ixabiso == 185 || ixabiso == 200) return 5;
        if (ixabiso >= 0 && ixabiso <= 8 || ixabiso >= 26 && ixabiso <= 29 || ixabiso >= 42 && ixabiso <= 46 || ixabiso >= 50 && ixabiso <= 53
            || ixabiso >= 59 && ixabiso <= 62 || ixabiso >= 75 && ixabiso <= 79 || ixabiso >= 83 && ixabiso <= 95
            || ixabiso == 96 || ixabiso == 100 || ixabiso == 104 || ixabiso == 108 || ixabiso == 112 || ixabiso == 116
            || ixabiso == 120 || ixabiso == 122 || ixabiso == 124 || ixabiso == 126 || ixabiso == 128 || ixabiso == 130
            || ixabiso >= 145 && ixabiso <= 147 || ixabiso == 172 || ixabiso == 176 || ixabiso == 177 || ixabiso == 190 || ixabiso == 191
            || ixabiso == 194 || ixabiso == 195) return 1;
        return 0;
    }
    static int 위치정수(int 읽는자리) {
        if (!ikliphu(읽는자리, 4)) { ukungaphumeleli_ixabiso("truncated bytecode operand"); return 0; }
        return iFayili[읽는자리] << 24 | iFayili[읽는자리 + 1] << 16 | iFayili[읽는자리 + 2] << 8 | iFayili[읽는자리 + 3];
    }
    static int 길이읽기(int 읽는자리, int Phumeza, int 끝) {
        int ixabiso = iFayili[읽는자리], ubude_ixabiso = umyalelo_ubude(ixabiso);
        if (ixabiso == 170 || ixabiso == 171) {
            int 기준자리 = 읽는자리 + 1;
            while ((기준자리 - Phumeza) % 4 != 0) 기준자리++;
            if (끝 - 기준자리 < (ixabiso == 170 ? 12 : 8)) return 0;
            int 항목수 = ixabiso == 170 ? 위치정수(기준자리 + 8) - 위치정수(기준자리 + 4) + 1 : 위치정수(기준자리 + 4);
            if (항목수 < 0 || 항목수 > 2048) return 0;
            ubude_ixabiso = 기준자리 - 읽는자리 + (ixabiso == 170 ? 12 + 4 * 항목수 : 8 + 8 * 항목수);
        }
        if (ixabiso == 196 && 읽는자리 + 1 < 끝) {
            int Igama_iingcombolo = iFayili[읽는자리 + 1]; ubude_ixabiso = Igama_iingcombolo == 132 ? 6 : (Igama_iingcombolo == 21 || Igama_iingcombolo == 25 || Igama_iingcombolo == 54 || Igama_iingcombolo == 58) ? 4 : 0;
        }
        return ubude_ixabiso > 0 && ubude_ixabiso <= 끝 - 읽는자리 ? ubude_ixabiso : 0;
    }
    static void jonga_indawo_ekuyiwa_kuyo_ixabiso(int indawo_ekuyiwa_kuyo_ixabiso, int INKQUBO_ixabiso) {
        if (indawo_ekuyiwa_kuyo_ixabiso < imethodi_qala[INKQUBO_ixabiso] || indawo_ekuyiwa_kuyo_ixabiso >= imethodi_phela[INKQUBO_ixabiso] || 경계[indawo_ekuyiwa_kuyo_ixabiso] != INKQUBO_ixabiso + 1) ukungaphumeleli_ixabiso("invalid branch target");
    }
    static void 클래스읽기(int iklasi_Ingcaciso) {
        현재읽는종 = iklasi_Ingcaciso; 읽기위치 = iklasi_Ingcaciso * 16384; Ubukhulu = 읽기위치 + iklasi_Ingcaciso_isayizi[iklasi_Ingcaciso];
        if (inani_elipheleleyo() != 0xcafebabe) { ukungaphumeleli_ixabiso("not a class file"); return; }
        int 부판 = 짧은수(), inguqulelo_ixabiso = 짧은수();
        if (inguqulelo_ixabiso < 45 || inguqulelo_ixabiso > 52 || 부판 != 0) { ukungaphumeleli_ixabiso("supported class versions: 45..52, minor 0"); return; }
        int 상수수 = 짧은수(), 기준자리 = iklasi_Ingcaciso * 512;
        if (상수수 < 1 || 상수수 > 512) { ukungaphumeleli_ixabiso("constant pool limit (511)"); return; }
        for (int 항목수 = 1; 항목수 < 상수수 && !Impazamo; 항목수++) {
            int 수 = 기준자리 + 항목수, 종류 = ibhayithi_ixabiso(); engajikiyo_thega[수] = 종류;
            if (종류 == 1) { 상나[수] = 짧은수(); 상가[수] = 읽기위치; 건너(상나[수]); }
            else if (종류 == 3) 상가[수] = inani_elipheleleyo();
            else if (종류 == 7 || 종류 == 8) 상가[수] = 상번호();
            else if (종류 == 9 || 종류 == 10 || 종류 == 11 || 종류 == 12) { 상가[수] = 상번호(); 상나[수] = 상번호(); }
            else ukungaphumeleli_ixabiso("unsupported constant type");
        }
        int imvume_ixabiso = 짧은수();
        if ((imvume_ixabiso & (0x2000 | 0x4000)) != 0) ukungaphumeleli_ixabiso("annotation/enum class unsupported");
        iklasi_Ingcaciso_igama[iklasi_Ingcaciso] = iklasi_igama_I_SMS(상번호());
        종부모[iklasi_Ingcaciso] = iklasi_igama_I_SMS(상번호());
        int 접면수 = 짧은수(); if (접면수 > 16) { ukungaphumeleli_ixabiso("interface count limit"); return; }
        종접면수[iklasi_Ingcaciso] = 접면수;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 접면수; iluphu_indeksa++) iklasi_isinxulumanisi[iklasi_Ingcaciso * 16 + iluphu_indeksa] = iklasi_igama_I_SMS(상번호());
        int 필드수 = 짧은수();
        if (필드수 > 512 - 칸수) { ukungaphumeleli_ixabiso("field count limit (512)"); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 필드수 && !Impazamo; iluphu_indeksa++) {
            int ifayile_indeksa = 칸수++; isithuba_umnini[ifayile_indeksa] = iklasi_Ingcaciso; isithuba_iimvume[ifayile_indeksa] = 짧은수(); isithuba_igama[ifayile_indeksa] = 상번호(); isithuba_uhlobo[ifayile_indeksa] = 상번호();
            jonga_engajikiyo(isithuba_igama[ifayile_indeksa], 1); jonga_engajikiyo(isithuba_uhlobo[ifayile_indeksa], 1);
            int 보존값 = 읽기위치; 읽기위치 = 상가[isithuba_uhlobo[ifayile_indeksa]]; int 분류코드 = 서술형(읽기위치 + 상나[isithuba_uhlobo[ifayile_indeksa]], false); 읽기위치 = 보존값;
            if ((isithuba_iimvume[ifayile_indeksa] & 8) == 0) 칸위치[ifayile_indeksa] = 종칸수[iklasi_Ingcaciso]++;
            int uphawu_iingcombolo = 짧은수();
            for (int 안쪽자리 = 0; 안쪽자리 < uphawu_iingcombolo && !Impazamo; 안쪽자리++) {
                int igama_engajikiyo = 상번호(), 유효길이 = inani_elipheleleyo();
                if (Igama_I_SMS(igama_engajikiyo, "ConstantValue") && 유효길이 == 2) {
                    int iingcombolo_ixabiso = 상번호();
                    if (분류코드 == 1 && jonga_engajikiyo(iingcombolo_ixabiso, 3)) isithuba_iingcombolo[ifayile_indeksa] = 상가[iingcombolo_ixabiso];
                    else if (분류코드 == 2 && jonga_engajikiyo(iingcombolo_ixabiso, 8)) isithuba_iingcombolo[ifayile_indeksa] = engajikiyo_I_SMS(상가[iingcombolo_ixabiso]);
                } else 건너(유효길이);
            }
        }
        int 개수 = 짧은수();
        if (개수 > 512 - 함수수) { ukungaphumeleli_ixabiso("method count limit (512)"); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 개수 && !Impazamo; iluphu_indeksa++) {
            int 수 = 함수수++; imethodi_umnini[수] = iklasi_Ingcaciso;
            imethodi_fikelela[수] = 짧은수(); imethodi_igama_I_SMS[수] = 상번호(); imethodi_uhlobo[수] = 상번호();
            jonga_engajikiyo(imethodi_igama_I_SMS[수], 1); 서술읽기(수);
            if ((imethodi_fikelela[수] & 8) == 0) {
                if (함수인수수[수] == 16) { ukungaphumeleli_ixabiso("too many instance method arguments"); return; }
                for (int 비교자리 = 함수인수수[수]; 비교자리 > 0; 비교자리--) imethodi_isiniki_myalelo_uhlobo[수 * 16 + 비교자리] = imethodi_isiniki_myalelo_uhlobo[수 * 16 + 비교자리 - 1];
                imethodi_isiniki_myalelo_uhlobo[수 * 16] = 2; 함수인수수[수]++;
            }
            if ((imethodi_fikelela[수] & 0x100) != 0) ukungaphumeleli_ixabiso("user native method unsupported");
            if (Igama_I_SMS(imethodi_igama_I_SMS[수], "<clinit>")) qalisa_umsebenzi_iklasi_Ingcaciso[iklasi_Ingcaciso] = 수 + 1;
            for (int 앞 = 0; 앞 < 수; 앞++) if (imethodi_umnini[앞] == iklasi_Ingcaciso && 같은말(imethodi_igama_I_SMS[앞], imethodi_igama_I_SMS[수]) && 같은말(imethodi_uhlobo[앞], imethodi_uhlobo[수])) ukungaphumeleli_ixabiso("duplicate method");
            int 속성수 = 짧은수();
            for (int uphawu_ixabiso = 0; uphawu_ixabiso < 속성수 && !Impazamo; uphawu_ixabiso++) {
                int Igama = 상번호(), ubude_ixabiso = inani_elipheleleyo(), Phumeza = 읽기위치;
                if (!ikliphu(Phumeza, ubude_ixabiso)) { ukungaphumeleli_ixabiso("truncated method attribute"); break; }
                if (Igama_I_SMS(Igama, "Code")) {
                    if (imethodi_qala[수] != 0) ukungaphumeleli_ixabiso("duplicate Code attribute");
                    imethodi_fumba[수] = 짧은수(); 함수지역[수] = 짧은수(); int 코드길이 = inani_elipheleleyo();
                    if (imethodi_fumba[수] > 128 || 함수지역[수] > 128 || 함수지역[수] < 함수인수수[수]
                        || 코드길이 < 1 || 코드길이 > 8192) ukungaphumeleli_ixabiso("method memory limits exceeded");
                    imethodi_qala[수] = 읽기위치; 건너(코드길이); imethodi_phela[수] = 읽기위치;
                    int 잡는수 = 짧은수();
                    if (잡는수 > 1024 - 잡기수) { ukungaphumeleli_ixabiso("exception table limit"); return; }
                    for (int 안쪽자리 = 0; 안쪽자리 < 잡는수; 안쪽자리++) {
                        int impazamo_Isalathiso = 잡기수++; 잡기함수[impazamo_Isalathiso] = 수;
                        잡기시작[impazamo_Isalathiso] = imethodi_qala[수] + 짧은수(); 잡기끝[impazamo_Isalathiso] = imethodi_qala[수] + 짧은수();
                        잡기위치[impazamo_Isalathiso] = imethodi_qala[수] + 짧은수(); int 부호값 = 상번호(); 잡기종[impazamo_Isalathiso] = 부호값 == 0 ? 0 : iklasi_igama_I_SMS(부호값);
                    }
                    속성건너();
                    if (읽기위치 != Phumeza + ubude_ixabiso) ukungaphumeleli_ixabiso("Code attribute size mismatch");
                } else 건너(ubude_ixabiso);
            }
            if ((imethodi_fikelela[수] & 0x400) != 0) continue;
            if (imethodi_qala[수] == 0) ukungaphumeleli_ixabiso("missing Code attribute");
            int isithuba_ufako_nkcukacha = imethodi_qala[수];
            while (isithuba_ufako_nkcukacha < imethodi_phela[수] && !Impazamo) {
                int ubude_ixabiso = 길이읽기(isithuba_ufako_nkcukacha, imethodi_qala[수], imethodi_phela[수]);
                if (ubude_ixabiso == 0) { ukungaphumeleli_ixabiso("unsupported or truncated bytecode"); break; }
                경계[isithuba_ufako_nkcukacha] = 수 + 1; isithuba_ufako_nkcukacha += ubude_ixabiso;
            }
            isithuba_ufako_nkcukacha = imethodi_qala[수];
            while (isithuba_ufako_nkcukacha < imethodi_phela[수] && !Impazamo) {
                int ixabiso = iFayili[isithuba_ufako_nkcukacha];
                if (ixabiso >= 153 && ixabiso <= 167 || ixabiso == 198 || ixabiso == 199) jonga_indawo_ekuyiwa_kuyo_ixabiso(isithuba_ufako_nkcukacha + (short)(iFayili[isithuba_ufako_nkcukacha + 1] << 8 | iFayili[isithuba_ufako_nkcukacha + 2]), 수);
                if (ixabiso == 200) jonga_indawo_ekuyiwa_kuyo_ixabiso(isithuba_ufako_nkcukacha + 위치정수(isithuba_ufako_nkcukacha + 1), 수);
                if (ixabiso == 170 || ixabiso == 171) {
                    int 읽는자리 = isithuba_ufako_nkcukacha + 1; while ((읽는자리 - imethodi_qala[수]) % 4 != 0) 읽는자리++;
                    jonga_indawo_ekuyiwa_kuyo_ixabiso(isithuba_ufako_nkcukacha + 위치정수(읽는자리), 수);
                    int 항목수 = ixabiso == 170 ? 위치정수(읽는자리 + 8) - 위치정수(읽는자리 + 4) + 1 : 위치정수(읽는자리 + 4);
                    읽는자리 += ixabiso == 170 ? 12 : 8;
                    for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) jonga_indawo_ekuyiwa_kuyo_ixabiso(isithuba_ufako_nkcukacha + 위치정수(읽는자리 + 안쪽자리 * (ixabiso == 170 ? 4 : 8) + (ixabiso == 170 ? 0 : 4)), 수);
                }
                isithuba_ufako_nkcukacha += 길이읽기(isithuba_ufako_nkcukacha, imethodi_qala[수], imethodi_phela[수]);
            }
            for (int 안쪽자리 = 0; 안쪽자리 < 잡기수; 안쪽자리++) if (잡기함수[안쪽자리] == 수) {
                jonga_indawo_ekuyiwa_kuyo_ixabiso(잡기시작[안쪽자리], 수); jonga_indawo_ekuyiwa_kuyo_ixabiso(잡기위치[안쪽자리], 수);
                if (잡기끝[안쪽자리] != imethodi_phela[수]) jonga_indawo_ekuyiwa_kuyo_ixabiso(잡기끝[안쪽자리], 수);
                if (잡기시작[안쪽자리] >= 잡기끝[안쪽자리]) ukungaphumeleli_ixabiso("invalid exception range");
            }
        }
        if (!Impazamo) 속성건너();
        if (읽기위치 != Ubukhulu) ukungaphumeleli_ixabiso("extra class file data");
    }
    static int yabela_Ugcino(int 종류, int ubude_ixabiso) { return 새기억(종류, ubude_ixabiso); }
    static boolean into_ixabiso(int Isalathiso, int 종류) {
        if (!객체유효(Isalathiso)) return false;
        if (힙[Isalathiso] != 종류) { ukungaphumeleli_ixabiso("object type mismatch"); return false; }
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
        if (반환형 == 2) khusela_ixabiso(스택값[isithuba_ufako_nkcukacha]);
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
        if (ifreyim_indeksa % 32 == 31) { ukungaphumeleli_ixabiso("call stack limit (32)"); return; }
        int 다음 = ifreyim_indeksa + 1;
        for (int 수 = 0; 수 < 128; 수++) eyale_ndawo_uhlobo[다음 * 128 + 수] = 0;
        for (int 수 = 함수인수수[INKQUBO_ixabiso] - 1; 수 >= 0; 수--) {
            eyale_ndawo_ixabiso[다음 * 128 + 수] = 빼기(imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수]); eyale_ndawo_uhlobo[다음 * 128 + 수] = imethodi_isiniki_myalelo_uhlobo[INKQUBO_ixabiso * 16 + 수];
        }
        if (Impazamo) return;
        ifreyim_indeksa = 다음; qalisa_umsebenzi_ifreyim[ifreyim_indeksa] = 0; ifreyim_imethodi[ifreyim_indeksa] = INKQUBO_ixabiso; 틀위치[ifreyim_indeksa] = imethodi_qala[INKQUBO_ixabiso]; ifreyim_fumba[ifreyim_indeksa] = 0;
    }
    static void 반환(int uhlobo_ixabiso) {
        if (uhlobo_ixabiso != 함수반환[ifreyim_imethodi[ifreyim_indeksa]]) { ukungaphumeleli_ixabiso("return type mismatch"); return; }
        int ixabiso = uhlobo_ixabiso == 0 ? 0 : 빼기(uhlobo_ixabiso);
        if (qalisa_umsebenzi_ifreyim[ifreyim_indeksa] != 0) iklasi_Ingcaciso_imo[qalisa_umsebenzi_ifreyim[ifreyim_indeksa] - 1] = 2;
        if (틀잠금[ifreyim_indeksa] != 0) { 잠금풀기(틀잠금[ifreyim_indeksa]); 틀잠금[ifreyim_indeksa] = 0; }
        ifreyim_indeksa--; if (ifreyim_indeksa >= 현재가닥 * 32 && uhlobo_ixabiso != 0) 넣기(ixabiso, uhlobo_ixabiso);
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
                if (ixabiso < 1) { ukungaphumeleli_ixabiso("invalid file stream path"); return; }
                Stream_ifayile_igama[isithuba_ufako_nkcukacha] = ixabiso;
            }
            Stream_ifayile_igama[ubude_ixabiso] = 0;
            int 서술자 = umsebenzisi.파일서술자열기(Stream_ifayile_igama, 출력 ? (이어 ? 1089 : 577) : 0);
            if (서술자 < 0) { ukungaphumeleli_ixabiso("FileNotFoundException: file open failed"); return; }
            힙[Stream_ixabiso + 2] = 서술자; 힙[Stream_ixabiso + 3] = 1;
            return;
        }
        if (Umyalelo != 182) { ukungaphumeleli_ixabiso("invalid file stream invocation"); return; }
        if ((출력 && Igama_I_SMS(Igama, "write") || !출력 && Igama_I_SMS(Igama, "read"))
            && (Igama_I_SMS(fomatha_ixabiso, 출력 ? "([B)V" : "([B)I") || Igama_I_SMS(fomatha_ixabiso, 출력 ? "([BII)V" : "([BII)I"))) {
            boolean ikliphu_ixabiso = Igama_I_SMS(fomatha_ixabiso, 출력 ? "([BII)V" : "([BII)I");
            int 항목수 = ikliphu_ixabiso ? 빼기(1) : 0, 시작점 = ikliphu_ixabiso ? 빼기(1) : 0, iingcombolo_ULUHLU = 빼기(2), into_Isalathiso = 빼기(2);
            if (!into_ixabiso(iingcombolo_ULUHLU, 20) || !into_ixabiso(into_Isalathiso, 종류)) return;
            if (!ikliphu_ixabiso) 항목수 = 힙[iingcombolo_ULUHLU + 1];
            if (시작점 < 0 || 항목수 < 0 || 시작점 > 힙[iingcombolo_ULUHLU + 1] - 항목수) { 예외던짐(6, "file buffer bounds"); return; }
            if (힙[into_Isalathiso + 3] == 0 || 힙[into_Isalathiso + 2] < 0) { ukungaphumeleli_ixabiso("IOException: stream closed"); return; }
            int 완료수 = 0;
            while (완료수 < 항목수 && !Impazamo) {
                int 반환값 = 출력 ? umsebenzisi.파일한바이트쓰기(힙[into_Isalathiso + 2], 힙[iingcombolo_ULUHLU + 2 + 시작점 + 완료수]) : umsebenzisi.파일한바이트읽기(힙[into_Isalathiso + 2]);
                if (반환값 < 0) { ukungaphumeleli_ixabiso(출력 ? "IOException: write failed" : "IOException: read failed"); break; }
                if (!출력 && 반환값 == 256) break;
                if (!출력) 힙[iingcombolo_ULUHLU + 2 + 시작점 + 완료수] = (byte)반환값;
                완료수++;
            }
            if (!출력) 넣기(항목수 != 0 && 완료수 == 0 ? -1 : 완료수, 1);
            return;
        }
        if (출력 && Igama_I_SMS(Igama, "flush") && Igama_I_SMS(fomatha_ixabiso, "()V")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 종류) && 힙[into_Isalathiso + 2] < 0) ukungaphumeleli_ixabiso("IOException: stream closed"); return; }
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
            if (결과 < -1) ukungaphumeleli_ixabiso("IOException: read failed"); else 넣기(결과 == 256 ? -1 : 결과, 1);
        } else if (umsebenzisi.파일한바이트쓰기(서술자, ixabiso) != 1) ukungaphumeleli_ixabiso("IOException: write failed");
    }
    static void fowuna_imethodi(int indeksa, int Umyalelo) {
        if (indeksa <= 0 || indeksa >= engajikiyo_thega.length || (engajikiyo_thega[indeksa] != 10 && engajikiyo_thega[indeksa] != 11)) { ukungaphumeleli_ixabiso("invalid method reference"); return; }
        int umnini_ixabiso = iklasi_igama_I_SMS(상가[indeksa]), Igama = Isalathiso_igama(상나[indeksa]), fomatha_ixabiso = Isalathiso_uhlobo(상나[indeksa]);
        if (Impazamo) return;
        if (기본호출(umnini_ixabiso, Igama, fomatha_ixabiso, Umyalelo)) return;
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
        int iklasi_Ingcaciso = fumana_iklasi_Ingcaciso(umnini_ixabiso); if (iklasi_Ingcaciso < 0 || Impazamo) return;
        int ifayile_indeksa = fumana_imethodi(iklasi_Ingcaciso, Igama, fomatha_ixabiso);
        if (ifayile_indeksa < 0) {
            for (int ikhowudi_yekharakhtha = iklasi_Ingcaciso, 항목수 = 0; ikhowudi_yekharakhtha >= 0 && 항목수 < 16; 항목수++, ikhowudi_yekharakhtha = 부모종(ikhowudi_yekharakhtha))
                if (Igama_I_SMS(종부모[ikhowudi_yekharakhtha], "java/lang/Thread")) { 가닥호출(Igama, fomatha_ixabiso, Umyalelo); return; }
            ukungaphumeleli_ixabiso("NoSuchMethodError"); return;
        }
        if (((imethodi_fikelela[ifayile_indeksa] & 8) != 0) != (Umyalelo == 184)) { ukungaphumeleli_ixabiso("method static/instance mismatch"); return; }
        if (Umyalelo == 184) { if (!qalisa_umsebenzi(imethodi_umnini[ifayile_indeksa], ifreyim_umyalelo[ifreyim_indeksa])) return; }
        else {
            int 읽는자리 = ifreyim_fumba[ifreyim_indeksa] - 함수인수수[ifayile_indeksa];
            if (읽는자리 < 0 || 스택형[ifreyim_indeksa * 128 + 읽는자리] != 2) { ukungaphumeleli_ixabiso("invalid method receiver"); return; }
            int into_Isalathiso = 스택값[ifreyim_indeksa * 128 + 읽는자리];
            if (!객체유효(into_Isalathiso)) return;
            if (힙[into_Isalathiso] < 32 || !종포함(힙[into_Isalathiso] - 32, umnini_ixabiso)) { ukungaphumeleli_ixabiso("method receiver type mismatch"); return; }
            if (Umyalelo != 183) ifayile_indeksa = fumana_imethodi(힙[into_Isalathiso] - 32, Igama, fomatha_ixabiso);
        }
        if (ifayile_indeksa < 0 || (imethodi_fikelela[ifayile_indeksa] & 0x400) != 0) { ukungaphumeleli_ixabiso("AbstractMethodError"); return; }
        int 잠금참조 = 0;
        if ((imethodi_fikelela[ifayile_indeksa] & 32) != 0) {
            if (Umyalelo == 184) { int ikhowudi_yekharakhtha = imethodi_umnini[ifayile_indeksa]; if (종잠금[ikhowudi_yekharakhtha] == 0) 종잠금[ikhowudi_yekharakhtha] = yabela_Ugcino(8, 0); 잠금참조 = 종잠금[ikhowudi_yekharakhtha]; }
            else 잠금참조 = 스택값[ifreyim_indeksa * 128 + ifreyim_fumba[ifreyim_indeksa] - 함수인수수[ifayile_indeksa]];
            if (!잠금얻기(잠금참조)) { if (!Impazamo) 틀위치[ifreyim_indeksa] = ifreyim_umyalelo[ifreyim_indeksa]; return; }
        }
        호출(ifayile_indeksa); if (!Impazamo) 틀잠금[ifreyim_indeksa] = 잠금참조;
    }
    static boolean 배열저장가능(int ULUHLU_Isalathiso, int iingcombolo_ixabiso) {
        if (iingcombolo_ixabiso == 0 || ULUHLU_ielement[ULUHLU_Isalathiso] == 0) return true;
        boolean 성공여부 = ULUHLU_ielement[ULUHLU_Isalathiso] == -1 ? (iingcombolo_ixabiso > 0 && iingcombolo_ixabiso < 힙끝 && 힙[iingcombolo_ixabiso] == 1) : 맞는객체(iingcombolo_ixabiso, ULUHLU_ielement[ULUHLU_Isalathiso]);
        if (!성공여부 && !Impazamo) 예외던짐(17, "array element type mismatch");
        return 성공여부;
    }
    static int ULUHLU_isithuba(int Isalathiso, int umbhalo_omncinane_ixabiso, int uhlobo_ixabiso) {
        if (!into_ixabiso(Isalathiso, uhlobo_ixabiso)) return 0;
        if (umbhalo_omncinane_ixabiso < 0 || umbhalo_omncinane_ixabiso >= 힙[Isalathiso + 1]) { ukungaphumeleli_ixabiso("ArrayIndexOutOfBoundsException"); return 0; }
        return Isalathiso + 2 + umbhalo_omncinane_ixabiso;
    }
    static void ukwenza_umyalelo() {
        int 남음 = 500000, 조각 = 100;
        while (true) {
            if (Impazamo) { if (던진객체 != 0) 예외처리(); if (Impazamo || ifreyim_indeksa < 현재가닥 * 32) break; }
            if (ifreyim_indeksa < 현재가닥 * 32 || 바꿈요청 || --조각 == 0) { if (!tshintshela_ithredi()) break; 조각 = 100; }
            if (ifreyim_indeksa == 0 && iklasi_Ingcaciso_imo[ufako_nkcukacha_iklasi_Ingcaciso] != 2 && !qalisa_umsebenzi(ufako_nkcukacha_iklasi_Ingcaciso, 틀위치[ifreyim_indeksa])) continue;
            if (ifreyim_indeksa == 현재가닥 * 32 && 현재가닥 != 0 && (imethodi_fikelela[ifreyim_imethodi[ifreyim_indeksa]] & 32) != 0 && 틀잠금[ifreyim_indeksa] == 0) {
                int into_Isalathiso = ithredi_ithagethi[현재가닥]; if (!잠금얻기(into_Isalathiso)) { if (Impazamo) break; continue; } 틀잠금[ifreyim_indeksa] = into_Isalathiso;
            }
            잠시수 = 0;
            if (--남음 == 0) { ukungaphumeleli_ixabiso("instruction limit (500000)"); break; }
            int Phumeza = 틀위치[ifreyim_indeksa]; ifreyim_umyalelo[ifreyim_indeksa] = Phumeza; int ixabiso = 명바();
            if (Impazamo) break;
            if (ixabiso == 0) continue;
            if (ixabiso == 1) { 넣기(0, 2); continue; }
            if (ixabiso >= 2 && ixabiso <= 8) { 넣기(ixabiso - 3, 1); continue; }
            if (ixabiso == 16) { 넣기((byte)명바(), 1); continue; }
            if (ixabiso == 17) { 넣기((short)명짧(), 1); continue; }
            if (ixabiso == 18 || ixabiso == 19) {
                int 수 = imethodi_umnini[ifreyim_imethodi[ifreyim_indeksa]] * 512 + (ixabiso == 18 ? 명바() : 명짧());
                if (수 <= 0 || 수 >= engajikiyo_thega.length) ukungaphumeleli_ixabiso("invalid ldc constant");
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
            if (ixabiso == 46 || ixabiso >= 50 && ixabiso <= 53) {
                int 항목자리 = 빼기(1), into_Isalathiso = 빼기(2), 분류코드 = ixabiso == 46 ? 2 : ixabiso == 50 ? 3 : ixabiso == 51 ? 20 : ixabiso == 52 ? 22 : 23;
                if (ixabiso == 51 && into_Isalathiso > 0 && into_Isalathiso < 힙끝 && 힙[into_Isalathiso] == 21) 분류코드 = 21;
                int 읽는자리 = ULUHLU_isithuba(into_Isalathiso, 항목자리, 분류코드); if (!Impazamo) 넣기(힙[읽는자리], ixabiso == 50 ? 2 : 1); continue;
            }
            if (ixabiso == 79 || ixabiso >= 83 && ixabiso <= 86) {
                int ufako_nkcukacha_Isalathiso = 빼기(ixabiso == 83 ? 2 : 1), 항목자리 = 빼기(1), into_Isalathiso = 빼기(2), 분류코드 = ixabiso == 79 ? 2 : ixabiso == 83 ? 3 : ixabiso == 84 ? 20 : ixabiso == 85 ? 22 : 23;
                if (ixabiso == 84 && into_Isalathiso > 0 && into_Isalathiso < 힙끝 && 힙[into_Isalathiso] == 21) 분류코드 = 21;
                int 읽는자리 = ULUHLU_isithuba(into_Isalathiso, 항목자리, 분류코드);
                if (!Impazamo && 분류코드 == 3 && !배열저장가능(into_Isalathiso, ufako_nkcukacha_Isalathiso)) continue;
                if (!Impazamo) 힙[읽는자리] = 분류코드 == 20 ? (byte)ufako_nkcukacha_Isalathiso : 분류코드 == 21 ? ufako_nkcukacha_Isalathiso & 1 : 분류코드 == 22 ? (char)ufako_nkcukacha_Isalathiso : 분류코드 == 23 ? (short)ufako_nkcukacha_Isalathiso : ufako_nkcukacha_Isalathiso;
                continue;
            }
            if (ixabiso >= 87 && ixabiso <= 95) { fumba_umyalelo(ixabiso); continue; }
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
            if (ixabiso >= 178 && ixabiso <= 181) { 필드호출(명상수(), ixabiso, Phumeza); continue; }
            if (ixabiso >= 182 && ixabiso <= 185) {
                int 부호값 = 명상수();
                if (ixabiso == 185) { int 총수 = 명바(); if (총수 == 0 || 명바() != 0) { ukungaphumeleli_ixabiso("invalid invokeinterface operands"); continue; } }
                fowuna_imethodi(부호값, ixabiso); continue;
            }
            if (ixabiso == 187) { 새객체(iklasi_igama_I_SMS(명상수()), Phumeza); continue; }
            if (ixabiso == 188 || ixabiso == 189) {
                int 분류코드 = 3, inxenye_yento = 0;
                if (ixabiso == 188) { int 임시값 = 명바(); 분류코드 = 임시값 == 10 ? 2 : 임시값 == 8 ? 20 : 임시값 == 4 ? 21 : 임시값 == 5 ? 22 : 임시값 == 9 ? 23 : 0; }
                else inxenye_yento = iklasi_igama_I_SMS(명상수());
                if (분류코드 == 0) { ukungaphumeleli_ixabiso("unsupported primitive array type"); continue; }
                int 유효길이 = 빼기(1), into_Isalathiso = yabela_Ugcino(분류코드, 유효길이); if (!Impazamo) ULUHLU_ielement[into_Isalathiso] = inxenye_yento; 넣기(into_Isalathiso, 2); continue;
            }
            if (ixabiso == 190) {
                int into_Isalathiso = 빼기(2);
                if (객체유효(into_Isalathiso)) { int 비교자리 = 힙[into_Isalathiso]; if (비교자리 != 2 && 비교자리 != 3 && (비교자리 < 20 || 비교자리 > 23)) ukungaphumeleli_ixabiso("not an array"); else 넣기(힙[into_Isalathiso + 1], 1); }
                continue;
            }
            if (ixabiso == 191) {
                int into_Isalathiso = 빼기(2); if (객체유효(into_Isalathiso)) { if (힙[into_Isalathiso] != 9) ukungaphumeleli_ixabiso("athrow requires supported Throwable"); else { 던진객체 = into_Isalathiso; Impazamo = true; } }
                continue;
            }
            if (ixabiso == 192 || ixabiso == 193) {
                int igama_engajikiyo = iklasi_igama_I_SMS(명상수()), into_Isalathiso = 빼기(2); boolean 일치여부 = 맞는객체(into_Isalathiso, igama_engajikiyo);
                if (ixabiso == 193) 넣기(into_Isalathiso != 0 && 일치여부 ? 1 : 0, 1);
                else { if (!일치여부 && !Impazamo) ukungaphumeleli_ixabiso("ClassCastException"); 넣기(into_Isalathiso, 2); }
                continue;
            }
            if (ixabiso == 170 || ixabiso == 171) {
                int 읽는자리 = Phumeza + 1, ifayile_indeksa = ifreyim_imethodi[ifreyim_indeksa], iqhosha_Isalathiso = 빼기(1);
                while ((읽는자리 - imethodi_qala[ifayile_indeksa]) % 4 != 0) 읽는자리++;
                int ithagethi_idilesi = 위치정수(읽는자리);
                if (ixabiso == 170) { int 낮은값 = 위치정수(읽는자리 + 4), 높은값 = 위치정수(읽는자리 + 8); if (iqhosha_Isalathiso >= 낮은값 && iqhosha_Isalathiso <= 높은값) ithagethi_idilesi = 위치정수(읽는자리 + 12 + (iqhosha_Isalathiso - 낮은값) * 4); }
                else { int 총수 = 위치정수(읽는자리 + 4); for (int iluphu_indeksa = 0; iluphu_indeksa < 총수; iluphu_indeksa++) if (위치정수(읽는자리 + 8 + iluphu_indeksa * 8) == iqhosha_Isalathiso) ithagethi_idilesi = 위치정수(읽는자리 + 12 + iluphu_indeksa * 8); }
                fudusa_ixabiso(Phumeza + ithagethi_idilesi); continue;
            }
            if (ixabiso == 200) { fudusa_ixabiso(Phumeza + 위치정수(Phumeza + 1)); continue; }
            if (ixabiso == 194 || ixabiso == 195) {
                int into_Isalathiso = 빼기(2);
                if (ixabiso == 195) 잠금풀기(into_Isalathiso);
                else if (!잠금얻기(into_Isalathiso) && !Impazamo) { 넣기(into_Isalathiso, 2); 틀위치[ifreyim_indeksa] = Phumeza; }
                continue;
            }
            if (ixabiso == 196) {
                int 명령코드 = 명바(), 항목자리 = 명짧();
                if (명령코드 == 21 || 명령코드 == 25) 지역읽기(항목자리, 명령코드 == 21 ? 1 : 2);
                else if (명령코드 == 54 || 명령코드 == 58) bhala_eyale_ndawo(항목자리, 명령코드 == 54 ? 1 : 2);
                else if (명령코드 == 132) { int 변화량 = (short)명짧(); 지역읽기(항목자리, 1); 넣기(빼기(1) + 변화량, 1); bhala_eyale_ndawo(항목자리, 1); }
                else ukungaphumeleli_ixabiso("unsupported wide opcode");
                continue;
            }
            ukungaphumeleli_ixabiso("unsupported bytecode");
        }
    }
    static int fumana_iklasi_Ingcaciso(int Igama) {
        for (int iluphu_indeksa = 0; iluphu_indeksa < 종수; iluphu_indeksa++) if (iklasi_Ingcaciso_igama[iluphu_indeksa] != 0 && 같은말(iklasi_Ingcaciso_igama[iluphu_indeksa], Igama)) return iluphu_indeksa;
        return layisha_iklasi_Ingcaciso(engajikiyo_I_SMS(Igama));
    }
    static int layisha_iklasi_Ingcaciso(int igama_uluhlu_lweekharektha) {
        if (!into_ixabiso(igama_uluhlu_lweekharektha, 1)) return -1;
        int ubude_ixabiso = 힙[igama_uluhlu_lweekharektha + 1];
        if (ubude_ixabiso < 1 || ubude_ixabiso > 505 || 종수 == 16) { ukungaphumeleli_ixabiso("class name/count limit"); return -1; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < ubude_ixabiso; iluphu_indeksa++) { int ikhowudi_yekharakhtha = 힙[igama_uluhlu_lweekharektha + 2 + iluphu_indeksa]; ifayile_igama_I_SMS[iluphu_indeksa] = ikhowudi_yekharakhtha == '/' ? '.' : ikhowudi_yekharakhtha; }
        ifayile_igama_I_SMS[ubude_ixabiso] = '.'; ifayile_igama_I_SMS[ubude_ixabiso + 1] = 'c'; ifayile_igama_I_SMS[ubude_ixabiso + 2] = 'l'; ifayile_igama_I_SMS[ubude_ixabiso + 3] = 'a'; ifayile_igama_I_SMS[ubude_ixabiso + 4] = 's'; ifayile_igama_I_SMS[ubude_ixabiso + 5] = 's'; ifayile_igama_I_SMS[ubude_ixabiso + 6] = 0;
        int Ubukhulu = umsebenzisi.파일읽기(ifayile_igama_I_SMS, 임시파일);
        if (Ubukhulu < 0) { ukungaphumeleli_ixabiso("ClassNotFoundException"); return -1; }
        int iklasi_Ingcaciso = 종수++; iklasi_Ingcaciso_isayizi[iklasi_Ingcaciso] = Ubukhulu;
        for (int iluphu_indeksa = 0; iluphu_indeksa < Ubukhulu; iluphu_indeksa++) iFayili[iklasi_Ingcaciso * 16384 + iluphu_indeksa] = 임시파일[iluphu_indeksa];
        클래스읽기(iklasi_Ingcaciso); if (Impazamo) return -1;
        int eyona_yenzekileyo_iingcombolo = engajikiyo_I_SMS(iklasi_Ingcaciso_igama[iklasi_Ingcaciso]);
        if (!글같음(eyona_yenzekileyo_iingcombolo, igama_uluhlu_lweekharektha, true)) { ukungaphumeleli_ixabiso("class name does not match file"); return -1; }
        int 부모 = 종부모[iklasi_Ingcaciso];
        if (부모 != 0 && !Igama_I_SMS(부모, "java/lang/Object") && !Igama_I_SMS(부모, "java/lang/Thread")) {
            // 한 번 등록한 클래스를 다시 적재하지 않지만 상속 고리는 명시적으로 거부한다.
            int 위 = fumana_iklasi_Ingcaciso(부모);
            if (Impazamo || 위 < 0) return -1;
            int 읽는자리 = 위, 단계수 = 0;
            while (읽는자리 >= 0 && 단계수++ < 16) {
                if (읽는자리 == iklasi_Ingcaciso) { ukungaphumeleli_ixabiso("cyclic inheritance"); return -1; }
                읽는자리 = 부모종(읽는자리);
            }
            int 시작변위 = 종칸수[위];
            for (int ifayile_indeksa = 0; ifayile_indeksa < 칸수; ifayile_indeksa++) if (isithuba_umnini[ifayile_indeksa] == iklasi_Ingcaciso && (isithuba_iimvume[ifayile_indeksa] & 8) == 0) 칸위치[ifayile_indeksa] += 시작변위;
            종칸수[iklasi_Ingcaciso] += 시작변위;
        }
        return iklasi_Ingcaciso;
    }
    static int 부모종(int iklasi_Ingcaciso) {
        int Igama = 종부모[iklasi_Ingcaciso];
        for (int iluphu_indeksa = 0; iluphu_indeksa < 종수; iluphu_indeksa++) if (Igama != 0 && iklasi_Ingcaciso_igama[iluphu_indeksa] != 0 && 같은말(iklasi_Ingcaciso_igama[iluphu_indeksa], Igama)) return iluphu_indeksa;
        return -1;
    }
    static int fumana_imethodi(int iklasi_Ingcaciso, int Igama, int fomatha_ixabiso) {
        for (int 깊이 = 0; iklasi_Ingcaciso >= 0 && 깊이 < 16; 깊이++, iklasi_Ingcaciso = 부모종(iklasi_Ingcaciso)) {
            for (int iluphu_indeksa = 0; iluphu_indeksa < 함수수; iluphu_indeksa++) if (imethodi_umnini[iluphu_indeksa] == iklasi_Ingcaciso && 같은말(imethodi_igama_I_SMS[iluphu_indeksa], Igama) && 같은말(imethodi_uhlobo[iluphu_indeksa], fomatha_ixabiso)) return iluphu_indeksa;
        }
        return -1;
    }
    static int igama_imethodi(int iklasi_Ingcaciso, String Igama, String fomatha_ixabiso) {
        for (int 깊이 = 0; iklasi_Ingcaciso >= 0 && 깊이 < 16; 깊이++, iklasi_Ingcaciso = 부모종(iklasi_Ingcaciso))
            for (int iluphu_indeksa = 0; iluphu_indeksa < 함수수; iluphu_indeksa++) if (imethodi_umnini[iluphu_indeksa] == iklasi_Ingcaciso && Igama_I_SMS(imethodi_igama_I_SMS[iluphu_indeksa], Igama) && Igama_I_SMS(imethodi_uhlobo[iluphu_indeksa], fomatha_ixabiso)) return iluphu_indeksa;
        return -1;
    }
    static int 형종류(int Igama) { return iFayili[상가[Igama]] == 'L' || iFayili[상가[Igama]] == '[' ? 2 : 1; }
    static boolean qalisa_umsebenzi(int iklasi_Ingcaciso, int umyalelo_qala) {
        if (iklasi_Ingcaciso < 0 || Impazamo) return false;
        if (iklasi_Ingcaciso_imo[iklasi_Ingcaciso] == 3) { ukungaphumeleli_ixabiso("NoClassDefFoundError: initialization failed"); return false; }
        if (iklasi_Ingcaciso_imo[iklasi_Ingcaciso] == 1 && iklasi_ithredi[iklasi_Ingcaciso] != 현재가닥) { 틀위치[ifreyim_indeksa] = umyalelo_qala; 바꿈요청 = true; return false; }
        if (iklasi_Ingcaciso_imo[iklasi_Ingcaciso] != 0) return true;
        int 위 = 부모종(iklasi_Ingcaciso);
        if (위 >= 0 && !qalisa_umsebenzi(위, umyalelo_qala)) return false;
        iklasi_Ingcaciso_imo[iklasi_Ingcaciso] = 1; iklasi_ithredi[iklasi_Ingcaciso] = 현재가닥;
        if (qalisa_umsebenzi_iklasi_Ingcaciso[iklasi_Ingcaciso] != 0) {
            틀위치[ifreyim_indeksa] = umyalelo_qala;
            호출(qalisa_umsebenzi_iklasi_Ingcaciso[iklasi_Ingcaciso] - 1); if (!Impazamo) qalisa_umsebenzi_ifreyim[ifreyim_indeksa] = iklasi_Ingcaciso + 1;
            return false;
        }
        iklasi_Ingcaciso_imo[iklasi_Ingcaciso] = 2; return true;
    }
    static void 필드호출(int indeksa, int Umyalelo, int Phumeza) {
        if (!jonga_engajikiyo(indeksa, 9)) return;
        int umnini_ixabiso = iklasi_igama_I_SMS(상가[indeksa]), Igama = Isalathiso_igama(상나[indeksa]), fomatha_ixabiso = Isalathiso_uhlobo(상나[indeksa]);
        if (Igama_I_SMS(umnini_ixabiso, "java/lang/System") && (Igama_I_SMS(Igama, "out") || Igama_I_SMS(Igama, "err")) && Igama_I_SMS(fomatha_ixabiso, "Ljava/io/PrintStream;") && Umyalelo == 178) { 넣기(-1, 2); return; }
        int iklasi_Ingcaciso = fumana_iklasi_Ingcaciso(umnini_ixabiso); if (iklasi_Ingcaciso < 0 || Impazamo) return;
        int 찾음 = -1;
        for (int 읽는자리 = iklasi_Ingcaciso, 깊이 = 0; 읽는자리 >= 0 && 깊이 < 16 && 찾음 < 0; 깊이++, 읽는자리 = 부모종(읽는자리))
            for (int ifayile_indeksa = 0; ifayile_indeksa < 칸수; ifayile_indeksa++) if (isithuba_umnini[ifayile_indeksa] == 읽는자리 && 같은말(isithuba_igama[ifayile_indeksa], Igama) && 같은말(isithuba_uhlobo[ifayile_indeksa], fomatha_ixabiso)) 찾음 = ifayile_indeksa;
        if (찾음 < 0) { ukungaphumeleli_ixabiso("NoSuchFieldError"); return; }
        boolean imi_ndawonye_ixabiso = Umyalelo == 178 || Umyalelo == 179;
        if (imi_ndawonye_ixabiso != ((isithuba_iimvume[찾음] & 8) != 0)) { ukungaphumeleli_ixabiso("field static/instance mismatch"); return; }
        if (imi_ndawonye_ixabiso && !qalisa_umsebenzi(isithuba_umnini[찾음], Phumeza)) return;
        int uhlobo_ixabiso = 형종류(fomatha_ixabiso), ixabiso = 0;
        if (Umyalelo == 179 || Umyalelo == 181) ixabiso = 빼기(uhlobo_ixabiso);
        if (imi_ndawonye_ixabiso) { if (Umyalelo == 178) 넣기(isithuba_iingcombolo[찾음], uhlobo_ixabiso); else if (!Impazamo) isithuba_iingcombolo[찾음] = ixabiso; return; }
        int into_Isalathiso = 빼기(2);
        if (!객체유효(into_Isalathiso)) return;
        if (힙[into_Isalathiso] < 32 || !종포함(힙[into_Isalathiso] - 32, umnini_ixabiso)) { ukungaphumeleli_ixabiso("field receiver type mismatch"); return; }
        int 보관칸 = into_Isalathiso + 2 + 칸위치[찾음];
        if (Umyalelo == 180) 넣기(힙[보관칸], uhlobo_ixabiso);
        else if (!Impazamo) { 힙[보관칸] = ixabiso; 힙참조[보관칸] = uhlobo_ixabiso == 2 ? 1 : 0; }
    }
    static boolean 종포함(int iklasi_Ingcaciso, int Igama) {
        for (int 중첩깊이 = 0; iklasi_Ingcaciso >= 0 && 중첩깊이 < 16; 중첩깊이++, iklasi_Ingcaciso = 부모종(iklasi_Ingcaciso)) {
            if (같은말(iklasi_Ingcaciso_igama[iklasi_Ingcaciso], Igama) || (종부모[iklasi_Ingcaciso] != 0 && 같은말(종부모[iklasi_Ingcaciso], Igama))) return true;
            for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[iklasi_Ingcaciso]; 안쪽자리++) if (같은말(iklasi_isinxulumanisi[iklasi_Ingcaciso * 16 + 안쪽자리], Igama)) return true;
        }
        return false;
    }
    static boolean 글같음(int 첫값, int ibhayithi_iingcombolo, boolean INDLELA) {
        if (첫값 == ibhayithi_iingcombolo) return true;
        if (첫값 <= 0 || ibhayithi_iingcombolo <= 0 || 힙[첫값] != 1 || 힙[ibhayithi_iingcombolo] != 1 || 힙[첫값 + 1] != 힙[ibhayithi_iingcombolo + 1]) return false;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 힙[첫값 + 1]; iluphu_indeksa++) {
            int isilungelelanisi_x = 힙[첫값 + 2 + iluphu_indeksa], 세로좌표 = 힙[ibhayithi_iingcombolo + 2 + iluphu_indeksa];
            if (INDLELA) { if (isilungelelanisi_x == '.') isilungelelanisi_x = '/'; if (세로좌표 == '.') 세로좌표 = '/'; }
            if (isilungelelanisi_x != 세로좌표) return false;
        }
        return true;
    }
    static boolean 객체유효(int into_Isalathiso) {
        if (into_Isalathiso == 0) { ukungaphumeleli_ixabiso("NullPointerException"); return false; }
        if (into_Isalathiso < 1 || into_Isalathiso >= 힙끝 || 힙폭[into_Isalathiso] < 2 || 힙[into_Isalathiso] == 0) { ukungaphumeleli_ixabiso("invalid object reference"); return false; }
        return true;
    }
    static void khusela_ixabiso(int into_Isalathiso) {
        if (into_Isalathiso > 0 && into_Isalathiso < 힙끝 && 힙폭[into_Isalathiso] >= 2 && 잠시수 < 잠시참조.length) 잠시참조[잠시수++] = into_Isalathiso;
    }
    static void bonisa_ixabiso(int into_Isalathiso) {
        if (into_Isalathiso > 0 && into_Isalathiso < 힙끝 && 힙폭[into_Isalathiso] >= 2 && 힙[into_Isalathiso] != 0 && 힙표시[into_Isalathiso] == 0) {
            힙표시[into_Isalathiso] = 1; 표시대기[표시수++] = into_Isalathiso;
        }
    }
    static void 수거() {
        표시수 = 0; 수거횟수++;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) 힙표시[검사자리] = 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < uluhlu_lweekharektha_Isalathiso.length; iluphu_indeksa++) bonisa_ixabiso(uluhlu_lweekharektha_Isalathiso[iluphu_indeksa]);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 칸수; iluphu_indeksa++) if ((isithuba_iimvume[iluphu_indeksa] & 8) != 0 && 형종류(isithuba_uhlobo[iluphu_indeksa]) == 2) bonisa_ixabiso(isithuba_iingcombolo[iluphu_indeksa]);
        for (int 임시값 = 0; 임시값 < 가닥수; 임시값++) {
            bonisa_ixabiso(ithredi_into[임시값]); bonisa_ixabiso(ithredi_ithagethi[임시값]);
            int 꼭대기자리 = 임시값 == 현재가닥 ? ifreyim_indeksa : ithredi_ifreyim[임시값];
            for (int ifayile_indeksa = 임시값 * 32; ifayile_indeksa <= 꼭대기자리; ifayile_indeksa++) {
                for (int 안쪽자리 = 0; 안쪽자리 < 함수지역[ifreyim_imethodi[ifayile_indeksa]]; 안쪽자리++) if (eyale_ndawo_uhlobo[ifayile_indeksa * 128 + 안쪽자리] == 2) bonisa_ixabiso(eyale_ndawo_ixabiso[ifayile_indeksa * 128 + 안쪽자리]);
                for (int 안쪽자리 = 0; 안쪽자리 < ifreyim_fumba[ifayile_indeksa]; 안쪽자리++) if (스택형[ifayile_indeksa * 128 + 안쪽자리] == 2) bonisa_ixabiso(스택값[ifayile_indeksa * 128 + 안쪽자리]);
            }
        }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 화면참조.length; iluphu_indeksa++) bonisa_ixabiso(화면참조[iluphu_indeksa]);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 나중수; iluphu_indeksa++) bonisa_ixabiso(나중실행[iluphu_indeksa]);
        for (int iluphu_indeksa = 0; iluphu_indeksa < Store_inani_elipheleleyo.length; iluphu_indeksa++) bonisa_ixabiso(Store_inani_elipheleleyo[iluphu_indeksa]);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 종수; iluphu_indeksa++) bonisa_ixabiso(종잠금[iluphu_indeksa]);
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (잠금깊이[검사자리] > 0) bonisa_ixabiso(검사자리);
        bonisa_ixabiso(던진객체);
        for (int iluphu_indeksa = 0; iluphu_indeksa < 잠시수; iluphu_indeksa++) bonisa_ixabiso(잠시참조[iluphu_indeksa]);
        while (표시수 > 0) {
            int into_Isalathiso = 표시대기[--표시수], 분류코드 = 힙[into_Isalathiso];
            for (int iluphu_indeksa = into_Isalathiso + 2; iluphu_indeksa < into_Isalathiso + 힙폭[into_Isalathiso]; iluphu_indeksa++) if (분류코드 == 3 || 분류코드 == 4 || 힙참조[iluphu_indeksa] != 0) bonisa_ixabiso(힙[iluphu_indeksa]);
        }
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙표시[검사자리] == 0) 힙[검사자리] = 0;
        for (int 검사자리 = 1; 검사자리 < 힙끝; 검사자리 += 힙폭[검사자리]) if (힙[검사자리] == 0) {
            while (검사자리 + 힙폭[검사자리] < 힙끝 && 힙[검사자리 + 힙폭[검사자리]] == 0) { int 다음자리 = 검사자리 + 힙폭[검사자리]; 힙폭[검사자리] += 힙폭[다음자리]; 힙폭[다음자리] = 0; }
            if (검사자리 + 힙폭[검사자리] == 힙끝) { 힙끝 = 검사자리; break; }
        }
    }
    static int 새기억(int 종류, int ubude_ixabiso) {
        if (ubude_ixabiso < 0) { ukungaphumeleli_ixabiso("NegativeArraySizeException"); return 0; }
        if (ubude_ixabiso > 힙.length - 3) { ukungaphumeleli_ixabiso("object heap exhausted"); return 0; }
        int 필요수 = ubude_ixabiso + 2, into_Isalathiso = 0;
        if (필요수 <= 힙.length - 힙끝) { into_Isalathiso = 힙끝; 힙끝 += 필요수; }
        else {
            수거();
            for (int 읽는자리 = 1; 읽는자리 < 힙끝; 읽는자리 += 힙폭[읽는자리]) if (힙[읽는자리] == 0 && 힙폭[읽는자리] >= 필요수) { into_Isalathiso = 읽는자리; break; }
            if (into_Isalathiso != 0) {
                int 남은길이 = 힙폭[into_Isalathiso] - 필요수;
                if (남은길이 >= 2) { 힙폭[into_Isalathiso + 필요수] = 남은길이; 힙[into_Isalathiso + 필요수] = 0; }
                else 필요수 += 남은길이;
            } else if (필요수 <= 힙.length - 힙끝) { into_Isalathiso = 힙끝; 힙끝 += 필요수; }
        }
        if (into_Isalathiso == 0) { ukungaphumeleli_ixabiso("object heap exhausted"); return 0; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 필요수; iluphu_indeksa++) { 힙[into_Isalathiso + iluphu_indeksa] = 0; 힙참조[into_Isalathiso + iluphu_indeksa] = 0; 힙폭[into_Isalathiso + iluphu_indeksa] = 0; }
        ULUHLU_ielement[into_Isalathiso] = 0;
        힙폭[into_Isalathiso] = 필요수; 힙[into_Isalathiso] = 종류; 힙[into_Isalathiso + 1] = ubude_ixabiso; khusela_ixabiso(into_Isalathiso); return into_Isalathiso;
    }
    static int 예외종(String igama_engajikiyo) {
        if (자바도구.같음(igama_engajikiyo, "java/lang/Throwable")) return 1;
        if (자바도구.같음(igama_engajikiyo, "java/lang/Exception")) return 2;
        if (자바도구.같음(igama_engajikiyo, "java/lang/RuntimeException")) return 3;
        if (자바도구.같음(igama_engajikiyo, "java/lang/ArithmeticException")) return 4;
        if (자바도구.같음(igama_engajikiyo, "java/lang/NullPointerException")) return 5;
        if (자바도구.같음(igama_engajikiyo, "java/lang/IndexOutOfBoundsException")) return 6;
        if (자바도구.같음(igama_engajikiyo, "java/lang/ArrayIndexOutOfBoundsException")) return 7;
        if (자바도구.같음(igama_engajikiyo, "java/lang/StringIndexOutOfBoundsException")) return 8;
        if (자바도구.같음(igama_engajikiyo, "java/lang/IllegalArgumentException")) return 9;
        if (자바도구.같음(igama_engajikiyo, "java/lang/NumberFormatException")) return 10;
        if (자바도구.같음(igama_engajikiyo, "java/io/IOException")) return 11;
        if (자바도구.같음(igama_engajikiyo, "java/io/FileNotFoundException")) return 12;
        if (자바도구.같음(igama_engajikiyo, "java/lang/IllegalStateException")) return 13;
        if (자바도구.같음(igama_engajikiyo, "java/lang/ClassCastException")) return 14;
        if (자바도구.같음(igama_engajikiyo, "java/lang/NegativeArraySizeException")) return 15;
        return 0;
    }
    static int 예외상수(int Igama) {
        for (int iluphu_indeksa = 1; iluphu_indeksa <= 41; iluphu_indeksa++) if (Igama_I_SMS(Igama, 예외이름(iluphu_indeksa))) return iluphu_indeksa;
        return 0;
    }
    static String 예외이름(int isazisi_ixabiso) {
        if (isazisi_ixabiso == 40) return "java/lang/InterruptedException";
        if (isazisi_ixabiso == 41) return "isiXhosa/자체/대기중단예외";
        if (isazisi_ixabiso == 39) return "java/net/SocketException";
        if (isazisi_ixabiso == 20) return "isiXhosa/자체/예외";
        if (isazisi_ixabiso == 21) return "isiXhosa/자체/실행예외";
        if (isazisi_ixabiso == 22) return "isiXhosa/자체/입출력예외";
        if (isazisi_ixabiso == 23) return "isiXhosa/자체/대기시간초과예외";
        if (isazisi_ixabiso == 24) return "isiXhosa/자체/주소확인예외";
        if (isazisi_ixabiso == 25) return "isiXhosa/자체/파일없음예외";
        if (isazisi_ixabiso == 26) return "isiXhosa/자체/통신예외";
        if (isazisi_ixabiso == 27) return "isiXhosa/자체/잘못된인수예외";
        if (isazisi_ixabiso == 28) return "isiXhosa/자체/숫자형식예외";
        if (isazisi_ixabiso == 29) return "isiXhosa/자체/범위예외";
        if (isazisi_ixabiso == 30) return "isiXhosa/자체/배열범위예외";
        if (isazisi_ixabiso == 31) return "isiXhosa/자체/문자열범위예외";
        if (isazisi_ixabiso == 32) return "isiXhosa/자체/빈참조예외";
        if (isazisi_ixabiso == 33) return "isiXhosa/자체/산술예외";
        if (isazisi_ixabiso == 34) return "isiXhosa/자체/상태예외";
        if (isazisi_ixabiso == 35) return "isiXhosa/자체/형변환예외";
        if (isazisi_ixabiso == 36) return "isiXhosa/자체/음수배열크기예외";
        if (isazisi_ixabiso == 37) return "isiXhosa/자체/ULUHLU_Store_ukungaphumeleli";
        if (isazisi_ixabiso == 38) return "isiXhosa/자체/가닥상태예외";
        if (isazisi_ixabiso == 1) return "java/lang/Throwable"; if (isazisi_ixabiso == 2) return "java/lang/Exception";
        if (isazisi_ixabiso == 3) return "java/lang/RuntimeException"; if (isazisi_ixabiso == 4) return "java/lang/ArithmeticException";
        if (isazisi_ixabiso == 5) return "java/lang/NullPointerException"; if (isazisi_ixabiso == 6) return "java/lang/IndexOutOfBoundsException";
        if (isazisi_ixabiso == 7) return "java/lang/ArrayIndexOutOfBoundsException"; if (isazisi_ixabiso == 8) return "java/lang/StringIndexOutOfBoundsException";
        if (isazisi_ixabiso == 9) return "java/lang/IllegalArgumentException"; if (isazisi_ixabiso == 10) return "java/lang/NumberFormatException";
        if (isazisi_ixabiso == 11) return "java/io/IOException"; if (isazisi_ixabiso == 12) return "java/io/FileNotFoundException";
        if (isazisi_ixabiso == 17) return "java/lang/ArrayStoreException";
        if (isazisi_ixabiso == 18) return "java/net/UnknownHostException";
        if (isazisi_ixabiso == 19) return "java/net/SocketTimeoutException";
        if (isazisi_ixabiso == 16) return "java/lang/IllegalThreadStateException";
        if (isazisi_ixabiso == 13) return "java/lang/IllegalStateException"; if (isazisi_ixabiso == 14) return "java/lang/ClassCastException";
        return "java/lang/NegativeArraySizeException";
    }
    static int 예외부모(int isazisi_ixabiso) {
        if (isazisi_ixabiso == 40) return 2;
        if (isazisi_ixabiso == 41) return 40;
        if (isazisi_ixabiso == 39) return 11;
        if (isazisi_ixabiso == 1) return 0;
        if (isazisi_ixabiso == 2) return 1;
        if (isazisi_ixabiso == 3) return 2;
        if (isazisi_ixabiso == 4) return 3;
        if (isazisi_ixabiso == 5) return 3;
        if (isazisi_ixabiso == 6) return 3;
        if (isazisi_ixabiso == 7) return 6;
        if (isazisi_ixabiso == 8) return 6;
        if (isazisi_ixabiso == 9) return 3;
        if (isazisi_ixabiso == 10) return 9;
        if (isazisi_ixabiso == 11) return 2;
        if (isazisi_ixabiso == 12) return 11;
        if (isazisi_ixabiso == 13) return 3;
        if (isazisi_ixabiso == 14) return 3;
        if (isazisi_ixabiso == 15) return 3;
        if (isazisi_ixabiso == 16) return 9;
        if (isazisi_ixabiso == 17) return 3;
        if (isazisi_ixabiso == 18) return 11;
        if (isazisi_ixabiso == 19) return 11;
        if (isazisi_ixabiso == 20) return 2;
        if (isazisi_ixabiso == 21) return 3;
        if (isazisi_ixabiso == 22) return 11;
        if (isazisi_ixabiso == 23) return 22;
        if (isazisi_ixabiso == 24) return 22;
        if (isazisi_ixabiso == 25) return 22;
        if (isazisi_ixabiso == 26) return 22;
        if (isazisi_ixabiso == 27) return 9;
        if (isazisi_ixabiso == 28) return 27;
        if (isazisi_ixabiso == 29) return 6;
        if (isazisi_ixabiso == 30) return 29;
        if (isazisi_ixabiso == 31) return 29;
        if (isazisi_ixabiso == 32) return 5;
        if (isazisi_ixabiso == 33) return 4;
        if (isazisi_ixabiso == 34) return 13;
        if (isazisi_ixabiso == 35) return 14;
        if (isazisi_ixabiso == 36) return 15;
        if (isazisi_ixabiso == 37) return 17;
        if (isazisi_ixabiso == 38) return 16;
        return 0;
    }
    static boolean 예외포함(int eyona_yenzekileyo_ixabiso, int 요구값) {
        for (int 깊이 = 0; eyona_yenzekileyo_ixabiso != 0 && 깊이 < 16; 깊이++, eyona_yenzekileyo_ixabiso = 예외부모(eyona_yenzekileyo_ixabiso))
            if (eyona_yenzekileyo_ixabiso == 요구값) return true;
        return false;
    }
    static void 예외던짐(int isazisi_ixabiso, String i_README_Isalathiso) {
        int into_Isalathiso = 새기억(9, 2); if (Impazamo) return;
        힙[into_Isalathiso + 2] = isazisi_ixabiso; 힙[into_Isalathiso + 3] = umsingathi_ikharakhtha(i_README_Isalathiso); 힙참조[into_Isalathiso + 3] = 1;
        던진객체 = into_Isalathiso; Impazamo = true;
    }
    static boolean 맞는객체(int into_Isalathiso, int Igama) {
        if (into_Isalathiso == 0) return true;
        if (!객체유효(into_Isalathiso)) return false;
        int 분류코드 = 힙[into_Isalathiso];
        if (Igama_I_SMS(Igama, "java/lang/Object")) return true;
        if (분류코드 >= 32) return 종포함(분류코드 - 32, Igama);
        if (분류코드 == 9) { int ithagethi_idilesi = 예외상수(Igama); return ithagethi_idilesi != 0 && 예외포함(힙[into_Isalathiso + 2], ithagethi_idilesi); }
        if (분류코드 == 1) return Igama_I_SMS(Igama, "java/lang/String") || Igama_I_SMS(Igama, "java/lang/CharSequence");
        if (분류코드 == 4) return Igama_I_SMS(Igama, "java/lang/StringBuilder") || Igama_I_SMS(Igama, "java/lang/CharSequence");
        if (분류코드 == 10) return Igama_I_SMS(Igama, "java/util/ArrayList") || Igama_I_SMS(Igama, "java/util/List");
        if (분류코드 == 11) return Igama_I_SMS(Igama, "java/util/HashMap") || Igama_I_SMS(Igama, "java/util/Map");
        if (분류코드 == 12) return Igama_I_SMS(Igama, "java/lang/Integer") || Igama_I_SMS(Igama, "java/lang/Number");
        if (분류코드 >= 24 && 분류코드 <= 28 && 힙[into_Isalathiso + 13] != 0) return 한국어화면종(Igama) == 분류코드 || Igama_I_SMS(Igama, "isiXhosa/자체/화면구성요소");
        if (분류코드 >= 24 && 분류코드 <= 28) return (한국어화면종(Igama) == 0 && 화면종(Igama) == 분류코드) || Igama_I_SMS(Igama, "java/awt/Component") || Igama_I_SMS(Igama, "java/awt/Container") || Igama_I_SMS(Igama, "javax/swing/JComponent");
        if (분류코드 == 29) return Igama_I_SMS(Igama, 힙[into_Isalathiso + 3] != 0 ? "isiXhosa/자체/동작알림" : "java/awt/event/ActionEvent");
        if (분류코드 == 30) return Igama_I_SMS(Igama, "java/awt/FlowLayout") || Igama_I_SMS(Igama, "java/awt/LayoutManager");
        if (분류코드 == 17) return Igama_I_SMS(Igama, "java/net/Socket");
        if (분류코드 == 18) return Igama_I_SMS(Igama, "java/net/ServerSocket");
        if (분류코드 == 19) return Igama_I_SMS(Igama, 힙[into_Isalathiso + 3] == 0 ? "java/io/InputStream" : "java/io/OutputStream");
        if (분류코드 == 14) return Igama_I_SMS(Igama, "java/net/InetAddress");
        if (분류코드 == 15) return Igama_I_SMS(Igama, "java/net/DatagramSocket");
        if (분류코드 == 16) return Igama_I_SMS(Igama, "java/net/DatagramPacket");
        if (분류코드 == 13) return Igama_I_SMS(Igama, 힙[into_Isalathiso + 3] != 0 ? "isiXhosa/자체/작업가닥" : "java/lang/Thread");
        if (분류코드 == 2) return Igama_I_SMS(Igama, "[I"); if (분류코드 == 20) return Igama_I_SMS(Igama, "[B"); if (분류코드 == 21) return Igama_I_SMS(Igama, "[Z");
        if (분류코드 == 22) return Igama_I_SMS(Igama, "[C"); if (분류코드 == 23) return Igama_I_SMS(Igama, "[S");
        if (분류코드 != 3) return false;
        if (Igama_I_SMS(Igama, "[Ljava/lang/Object;")) return true;
        int inxenye_yento = ULUHLU_ielement[into_Isalathiso];
        if (inxenye_yento == -1) return Igama_I_SMS(Igama, "[Ljava/lang/String;") || Igama_I_SMS(Igama, "[Ljava/lang/CharSequence;");
        if (inxenye_yento == 0) return false;
        if (배열종비교(inxenye_yento, Igama)) return true;
        if ((Igama_I_SMS(inxenye_yento, "java/lang/String") || Igama_I_SMS(inxenye_yento, "java/lang/StringBuilder")) && Igama_I_SMS(Igama, "[Ljava/lang/CharSequence;")) return true;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 종수; iluphu_indeksa++) if (같은말(iklasi_Ingcaciso_igama[iluphu_indeksa], inxenye_yento)) {
            for (int ikhowudi_yekharakhtha = iluphu_indeksa, 중첩깊이 = 0; ikhowudi_yekharakhtha >= 0 && 중첩깊이 < 16; 중첩깊이++, ikhowudi_yekharakhtha = 부모종(ikhowudi_yekharakhtha)) {
                if (배열종비교(종부모[ikhowudi_yekharakhtha], Igama)) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 종접면수[ikhowudi_yekharakhtha]; 안쪽자리++) if (배열종비교(iklasi_isinxulumanisi[ikhowudi_yekharakhtha * 16 + 안쪽자리], Igama)) return true;
            }
        }
        return false;
    }
    static boolean 배열종비교(int igama_engajikiyo, int 형식참조) {
        int 검사자리 = 상가[형식참조], 항목수 = 상나[형식참조];
        if (igama_engajikiyo == 0 || 항목수 < 4 || iFayili[검사자리] != '[' || iFayili[검사자리 + 1] != 'L' || iFayili[검사자리 + 항목수 - 1] != ';' || 상나[igama_engajikiyo] != 항목수 - 3) return false;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수 - 3; iluphu_indeksa++) if (iFayili[상가[igama_engajikiyo] + iluphu_indeksa] != iFayili[검사자리 + 2 + iluphu_indeksa]) return false;
        return true;
    }
    static void 예외처리() {
        if (던진객체 == 0) return;
        Impazamo = false;
        while (ifreyim_indeksa >= 현재가닥 * 32) {
            int ifayile_indeksa = ifreyim_imethodi[ifreyim_indeksa], 읽는자리 = ifreyim_umyalelo[ifreyim_indeksa];
            for (int iluphu_indeksa = 0; iluphu_indeksa < 잡기수; iluphu_indeksa++) if (잡기함수[iluphu_indeksa] == ifayile_indeksa && 읽는자리 >= 잡기시작[iluphu_indeksa] && 읽는자리 < 잡기끝[iluphu_indeksa]
                && (잡기종[iluphu_indeksa] == 0 || 맞는객체(던진객체, 잡기종[iluphu_indeksa]))) {
                틀위치[ifreyim_indeksa] = 잡기위치[iluphu_indeksa]; ifreyim_fumba[ifreyim_indeksa] = 0; 넣기(던진객체, 2); 던진객체 = 0; return;
            }
            if (qalisa_umsebenzi_ifreyim[ifreyim_indeksa] != 0) iklasi_Ingcaciso_imo[qalisa_umsebenzi_ifreyim[ifreyim_indeksa] - 1] = 3;
            if (틀잠금[ifreyim_indeksa] != 0) { 잠금풀기(틀잠금[ifreyim_indeksa]); 틀잠금[ifreyim_indeksa] = 0; }
            ifreyim_indeksa--;
        }
        umsebenzisi.Bhala("Uncaught ");
        if (힙[던진객체] == 9) { umsebenzisi.Bhala(예외이름(힙[던진객체 + 2])); umsebenzisi.Bhala(": "); bhala_I_SMS(힙[던진객체 + 3]); }
        else umsebenzisi.Bhala("user exception");
        umsebenzisi.bhala_ikharakhtha_ixabiso(10); 던진객체 = 0; Impazamo = true;
    }
    // 이 JVM의 스택 항목은 현재 category-1(int/reference)만 허용한다.
    static void fumba_umyalelo(int 명령코드) {
        int 첫값 = 빼기(0), 첫형식 = 반환형;
        if (명령코드 == 87) return;
        if (명령코드 == 89) { 넣기(첫값, 첫형식); 넣기(첫값, 첫형식); return; }
        int ibhayithi_iingcombolo = 빼기(0), 둘째형식 = 반환형;
        if (명령코드 == 88) return;
        if (명령코드 == 90) { 넣기(첫값, 첫형식); 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 92) { 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 95) { 넣기(첫값, 첫형식); 넣기(ibhayithi_iingcombolo, 둘째형식); return; }
        int ikhowudi_yekharakhtha = 빼기(0), 셋째형식 = 반환형;
        if (명령코드 == 91) { 넣기(첫값, 첫형식); 넣기(ikhowudi_yekharakhtha, 셋째형식); 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); return; }
        if (명령코드 == 93) { 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); 넣기(ikhowudi_yekharakhtha, 셋째형식); 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); return; }
        int 뒷값 = 빼기(0), 넷째형식 = 반환형;
        넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식); 넣기(뒷값, 넷째형식); 넣기(ikhowudi_yekharakhtha, 셋째형식); 넣기(ibhayithi_iingcombolo, 둘째형식); 넣기(첫값, 첫형식);
    }
    static void 새객체(int igama_engajikiyo, int 시작점) {
        int 분류코드 = 0, 유효길이 = 0, 예외참조 = 예외상수(igama_engajikiyo);
        if (Igama_I_SMS(igama_engajikiyo, "java/lang/StringBuilder")) { 분류코드 = 4; 유효길이 = 1; }
        if (Igama_I_SMS(igama_engajikiyo, "java/io/FileInputStream")) { 분류코드 = 5; 유효길이 = 2; }
        if (Igama_I_SMS(igama_engajikiyo, "java/io/FileOutputStream")) { 분류코드 = 6; 유효길이 = 2; }
        if (예외참조 != 0) { 분류코드 = 9; 유효길이 = 2; }
        if (Igama_I_SMS(igama_engajikiyo, "java/util/ArrayList")) { 분류코드 = 10; 유효길이 = 2; }
        if (Igama_I_SMS(igama_engajikiyo, "java/util/HashMap")) { 분류코드 = 11; 유효길이 = 2; }
        if (Igama_I_SMS(igama_engajikiyo, "java/lang/Integer")) { 분류코드 = 12; 유효길이 = 1; }
        if (Igama_I_SMS(igama_engajikiyo, "java/net/Socket")) { 분류코드 = 17; 유효길이 = 5; }
        if (Igama_I_SMS(igama_engajikiyo, "java/net/ServerSocket")) { 분류코드 = 18; 유효길이 = 5; }
        if (Igama_I_SMS(igama_engajikiyo, "java/net/DatagramSocket")) { 분류코드 = 15; 유효길이 = 3; }
        if (Igama_I_SMS(igama_engajikiyo, "java/net/DatagramPacket")) { 분류코드 = 16; 유효길이 = 4; }
        if (Igama_I_SMS(igama_engajikiyo, "java/lang/Thread") || Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/작업가닥")) { 분류코드 = 13; 유효길이 = 2; }
        if (Igama_I_SMS(igama_engajikiyo, "java/lang/Object")) { 분류코드 = 8; }
        if (분류코드 == 0 && 화면종(igama_engajikiyo) != 0) { 분류코드 = 화면종(igama_engajikiyo); 유효길이 = 12; }
        if (분류코드 == 0) {
            int ikhowudi_yekharakhtha = fumana_iklasi_Ingcaciso(igama_engajikiyo); if (ikhowudi_yekharakhtha < 0 || Impazamo || !qalisa_umsebenzi(ikhowudi_yekharakhtha, 시작점)) return;
            분류코드 = 32 + ikhowudi_yekharakhtha; 유효길이 = 종칸수[ikhowudi_yekharakhtha];
        }
        int into_Isalathiso = yabela_Ugcino(분류코드, 유효길이); if (Impazamo) return;
        if (분류코드 == 13 && Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/작업가닥")) 힙[into_Isalathiso + 3] = 1;
        if (분류코드 >= 24 && 분류코드 <= 28 && 한국어화면종(igama_engajikiyo) != 0) 힙[into_Isalathiso + 13] = 1;
        if (분류코드 == 5 || 분류코드 == 6 || 분류코드 == 15 || 분류코드 == 17 || 분류코드 == 18) 힙[into_Isalathiso + 2] = -1;
        if (분류코드 == 9) 힙[into_Isalathiso + 2] = 예외참조;
        넣기(into_Isalathiso, 2);
    }
    static boolean 값같음(int 첫값, int ibhayithi_iingcombolo) {
        if (첫값 == ibhayithi_iingcombolo) return true;
        if (첫값 == 0 || ibhayithi_iingcombolo == 0 || 첫값 < 0 || ibhayithi_iingcombolo < 0 || 첫값 >= 힙끝 || ibhayithi_iingcombolo >= 힙끝) return false;
        if (힙[첫값] == 1 && 힙[ibhayithi_iingcombolo] == 1) return 글같음(첫값, ibhayithi_iingcombolo, false);
        return 힙[첫값] == 12 && 힙[ibhayithi_iingcombolo] == 12 && 힙[첫값 + 2] == 힙[ibhayithi_iingcombolo + 2];
    }
    static int 글조각(int into_Isalathiso, int 시작자리, int 끝자리) {
        if (!into_ixabiso(into_Isalathiso, 1)) return 0;
        if (시작자리 < 0 || 끝자리 < 시작자리 || 끝자리 > 힙[into_Isalathiso + 1]) { ukungaphumeleli_ixabiso("StringIndexOutOfBoundsException"); return 0; }
        int 반환값 = yabela_Ugcino(1, 끝자리 - 시작자리); if (Impazamo) return 0;
        for (int iluphu_indeksa = 시작자리; iluphu_indeksa < 끝자리; iluphu_indeksa++) 힙[반환값 + 2 + iluphu_indeksa - 시작자리] = 힙[into_Isalathiso + 2 + iluphu_indeksa];
        return 반환값;
    }
    static int joyina_I_SMS(int 첫값, int ibhayithi_iingcombolo) {
        if (!into_ixabiso(첫값, 1) || !into_ixabiso(ibhayithi_iingcombolo, 1)) return 0;
        int 항목수 = 힙[첫값 + 1], imethodi_indeksa = 힙[ibhayithi_iingcombolo + 1], 반환값 = yabela_Ugcino(1, 항목수 + imethodi_indeksa); if (Impazamo) return 0;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 힙[반환값 + 2 + iluphu_indeksa] = 힙[첫값 + 2 + iluphu_indeksa];
        for (int iluphu_indeksa = 0; iluphu_indeksa < imethodi_indeksa; iluphu_indeksa++) 힙[반환값 + 2 + 항목수 + iluphu_indeksa] = 힙[ibhayithi_iingcombolo + 2 + iluphu_indeksa];
        return 반환값;
    }
    static boolean 기본호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        if (Igama_I_SMS(umnini, "isiXhosa/자체/실행인수") && 명령코드 == 184) {
            if (Igama_I_SMS(igama_engajikiyo, "개수") && Igama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.인수개수() - 1, 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "Umbhalo") && Igama_I_SMS(서술상수, "(I)Ljava/lang/String;")) {
                int 순번 = 빼기(1);
                if (순번 < 0 || 순번 >= umsebenzisi.인수개수() - 1) 예외던짐(29, "ukwenza_umyalelo 인수 범위를 벗어났습니다");
                else 넣기(umsingathi_ikharakhtha(umsebenzisi.인수(순번 + 1)), 2);
                return true;
            }
            ukungaphumeleli_ixabiso("지원하지 않는 isiXhosa ukwenza_umyalelo 인수 호출"); return true;
        }
        if (Igama_I_SMS(umnini, "isiXhosa/자체/작업가닥")) { Inkqubo_ithredi(igama_engajikiyo, 서술상수, 명령코드, true); return true; }
        if (한국어화면소유(umnini)) { 한국어화면호출(umnini, igama_engajikiyo, 서술상수, 명령코드); return true; }
        if (화면소유(umnini)) { 화면호출(umnini, igama_engajikiyo, 서술상수, 명령코드); return true; }
        if (Igama_I_SMS(umnini, "java/net/Socket") || Igama_I_SMS(umnini, "java/net/ServerSocket") || Igama_I_SMS(umnini, "java/io/InputStream") || Igama_I_SMS(umnini, "java/io/OutputStream")) { 흐름호출(umnini, igama_engajikiyo, 서술상수, 명령코드); return true; }
        if (Igama_I_SMS(umnini, "isiXhosa/자체/ikheneli_ixabiso") && 명령코드 == 184) {
            if (Igama_I_SMS(igama_engajikiyo, "화면너비") && Igama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.화면너비(), 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "화면높이") && Igama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.화면높이(), 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "밀리초") && Igama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.밀리초(), 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "그림대기") && Igama_I_SMS(서술상수, "()I")) { 넣기(umsebenzisi.그림대기(), 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "사각형") && Igama_I_SMS(서술상수, "(IIIII)I")) { int 색상 = 빼기(1), 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), isilungelelanisi_x = 빼기(1); 넣기(umsebenzisi.사각형(isilungelelanisi_x, 세로좌표, 너비, 높이, 색상), 1); return true; }
        }
        if (Igama_I_SMS(umnini, "java/net/InetAddress") || Igama_I_SMS(umnini, "java/net/DatagramPacket") || Igama_I_SMS(umnini, "java/net/DatagramSocket")) { 통신호출(umnini, igama_engajikiyo, 서술상수, 명령코드); return true; }
        if (Igama_I_SMS(umnini, "java/lang/Thread")) { 가닥호출(igama_engajikiyo, 서술상수, 명령코드); return true; }
        if (Igama_I_SMS(umnini, "java/lang/Object")) {
            if (Igama_I_SMS(igama_engajikiyo, "<init>") && Igama_I_SMS(서술상수, "()V") && 명령코드 == 183) { 객체유효(빼기(2)); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "equals") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int ibhayithi_iingcombolo = 빼기(2), 첫값 = 빼기(2); if (객체유효(첫값)) 넣기(첫값 == ibhayithi_iingcombolo ? 1 : 0, 1); return true; }
        }
        if (예외상수(umnini) != 0) {
            if (Igama_I_SMS(igama_engajikiyo, "<init>") && 명령코드 == 183 && (Igama_I_SMS(서술상수, "()V") || Igama_I_SMS(서술상수, "(Ljava/lang/String;)V"))) {
                int imo_yokulinda = Igama_I_SMS(서술상수, "()V") ? 0 : 빼기(2), into_Isalathiso = 빼기(2);
                if (into_ixabiso(into_Isalathiso, 9)) { 힙[into_Isalathiso + 3] = imo_yokulinda; 힙참조[into_Isalathiso + 3] = 1; } return true;
            }
            if ((Igama_I_SMS(igama_engajikiyo, "getMessage") || Igama_I_SMS(igama_engajikiyo, "설명")) && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 9)) 넣기(힙[into_Isalathiso + 3], 2); return true; }
        }
        if (Igama_I_SMS(umnini, "java/lang/String")) {
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "getBytes") && (Igama_I_SMS(서술상수, "()[B") || Igama_I_SMS(서술상수, "(Ljava/lang/String;)[B"))) {
                int ujiko_nkcukacha_zibe_ziikhowudi_igama = Igama_I_SMS(서술상수, "()[B") ? 0 : 빼기(2), into_Isalathiso = 빼기(2);
                if (!into_ixabiso(into_Isalathiso, 1)) return true;
                if (ujiko_nkcukacha_zibe_ziikhowudi_igama != 0 && !글같음(ujiko_nkcukacha_zibe_ziikhowudi_igama, umsingathi_ikharakhtha("UTF-8"), false) && !글같음(ujiko_nkcukacha_zibe_ziikhowudi_igama, umsingathi_ikharakhtha("UTF8"), false) && !글같음(ujiko_nkcukacha_zibe_ziikhowudi_igama, umsingathi_ikharakhtha("utf-8"), false)) { 예외던짐(11, "only UTF-8 encoding is supported"); return true; }
                int 항목수 = 힙[into_Isalathiso + 1], 반환값 = yabela_Ugcino(20, 항목수 * 3), 사용수 = 0; if (Impazamo) return true;
                for (int 안쪽자리 = 0; 안쪽자리 < 항목수; 안쪽자리++) {
                    int ikhowudi_yekharakhtha = 힙[into_Isalathiso + 2 + 안쪽자리];
                    if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdbff && 안쪽자리 + 1 < 항목수 && 힙[into_Isalathiso + 3 + 안쪽자리] >= 0xdc00 && 힙[into_Isalathiso + 3 + 안쪽자리] <= 0xdfff) ikhowudi_yekharakhtha = 0x10000 + ((ikhowudi_yekharakhtha - 0xd800) << 10) + 힙[into_Isalathiso + 2 + ++안쪽자리] - 0xdc00;
                    else if (ikhowudi_yekharakhtha >= 0xd800 && ikhowudi_yekharakhtha <= 0xdfff) ikhowudi_yekharakhtha = '?';
                    if (ikhowudi_yekharakhtha < 128) 힙[반환값 + 2 + 사용수++] = ikhowudi_yekharakhtha;
                    else { int 바이트수 = ikhowudi_yekharakhtha < 2048 ? 2 : ikhowudi_yekharakhtha < 65536 ? 3 : 4; 힙[반환값 + 2 + 사용수++] = (byte)((바이트수 == 2 ? 192 : 바이트수 == 3 ? 224 : 240) | ikhowudi_yekharakhtha >> (6 * (바이트수 - 1))); for (int 비교자리 = 바이트수 - 1; 비교자리 > 0; 비교자리--) 힙[반환값 + 2 + 사용수++] = (byte)(128 | ikhowudi_yekharakhtha >> (6 * (비교자리 - 1)) & 63); }
                }
                힙[반환값 + 1] = 사용수; 넣기(반환값, 2); return true;
            }
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "valueOf") && Igama_I_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(inani_ikharakhtha(빼기(1)), 2); return true; }
            if (명령코드 != 182) return false;
            if (Igama_I_SMS(igama_engajikiyo, "equals") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) { int ibhayithi_iingcombolo = 빼기(2), 첫값 = 빼기(2); if (into_ixabiso(첫값, 1)) 넣기(글같음(첫값, ibhayithi_iingcombolo, false) ? 1 : 0, 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "isEmpty") && Igama_I_SMS(서술상수, "()Z")) { int 첫값 = 빼기(2); if (into_ixabiso(첫값, 1)) 넣기(힙[첫값 + 1] == 0 ? 1 : 0, 1); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "substring") && (Igama_I_SMS(서술상수, "(I)Ljava/lang/String;") || Igama_I_SMS(서술상수, "(II)Ljava/lang/String;"))) {
                boolean 둘째값 = Igama_I_SMS(서술상수, "(II)Ljava/lang/String;"); int 끝자리 = 둘째값 ? 빼기(1) : 0, 시작점 = 빼기(1), 첫값 = 빼기(2);
                if (into_ixabiso(첫값, 1)) 넣기(글조각(첫값, 시작점, 둘째값 ? 끝자리 : 힙[첫값 + 1]), 2); return true;
            }
            if (Igama_I_SMS(igama_engajikiyo, "concat") && Igama_I_SMS(서술상수, "(Ljava/lang/String;)Ljava/lang/String;")) { int ibhayithi_iingcombolo = 빼기(2), 첫값 = 빼기(2); 넣기(joyina_I_SMS(첫값, ibhayithi_iingcombolo), 2); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "hashCode") && Igama_I_SMS(서술상수, "()I")) { int 첫값 = 빼기(2), i_hash_ixabiso = 0; if (into_ixabiso(첫값, 1)) { for (int iluphu_indeksa = 0; iluphu_indeksa < 힙[첫값 + 1]; iluphu_indeksa++) i_hash_ixabiso = i_hash_ixabiso * 31 + 힙[첫값 + 2 + iluphu_indeksa]; 넣기(i_hash_ixabiso, 1); } return true; }
            if (Igama_I_SMS(igama_engajikiyo, "toString") && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) { int 첫값 = 빼기(2); if (into_ixabiso(첫값, 1)) 넣기(첫값, 2); return true; }
        }
        if (Igama_I_SMS(umnini, "java/lang/Integer")) {
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "valueOf") && Igama_I_SMS(서술상수, "(I)Ljava/lang/Integer;")) { int iingcombolo_ixabiso = 빼기(1), into_Isalathiso = iingcombolo_ixabiso >= -128 && iingcombolo_ixabiso <= 127 ? Store_inani_elipheleleyo[iingcombolo_ixabiso + 128] : 0; if (into_Isalathiso == 0) { into_Isalathiso = yabela_Ugcino(12, 1); if (!Impazamo) { 힙[into_Isalathiso + 2] = iingcombolo_ixabiso; if (iingcombolo_ixabiso >= -128 && iingcombolo_ixabiso <= 127) Store_inani_elipheleleyo[iingcombolo_ixabiso + 128] = into_Isalathiso; } } 넣기(into_Isalathiso, 2); return true; }
            if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>") && Igama_I_SMS(서술상수, "(I)V")) { int iingcombolo_ixabiso = 빼기(1), into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 12)) 힙[into_Isalathiso + 2] = iingcombolo_ixabiso; return true; }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "intValue") && Igama_I_SMS(서술상수, "()I")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 12)) 넣기(힙[into_Isalathiso + 2], 1); return true; }
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "toString") && Igama_I_SMS(서술상수, "(I)Ljava/lang/String;")) { 넣기(inani_ikharakhtha(빼기(1)), 2); return true; }
        }
        if (Igama_I_SMS(umnini, "java/lang/Math") && 명령코드 == 184) {
            if (Igama_I_SMS(igama_engajikiyo, "abs") && Igama_I_SMS(서술상수, "(I)I")) { int 읽은값 = 빼기(1); 넣기(읽은값 < 0 ? -읽은값 : 읽은값, 1); return true; }
            if ((Igama_I_SMS(igama_engajikiyo, "min") || Igama_I_SMS(igama_engajikiyo, "max")) && Igama_I_SMS(서술상수, "(II)I")) { int ibhayithi_iingcombolo = 빼기(1), 첫값 = 빼기(1); 넣기(Igama_I_SMS(igama_engajikiyo, "min") ? (첫값 < ibhayithi_iingcombolo ? 첫값 : ibhayithi_iingcombolo) : (첫값 > ibhayithi_iingcombolo ? 첫값 : ibhayithi_iingcombolo), 1); return true; }
        }
        if (Igama_I_SMS(umnini, "java/lang/System") && 명령코드 == 184) {
            if (Igama_I_SMS(igama_engajikiyo, "gc") && Igama_I_SMS(서술상수, "()V")) { 수거(); return true; }
            if (Igama_I_SMS(igama_engajikiyo, "arraycopy") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;ILjava/lang/Object;II)V")) {
                int 항목수 = 빼기(1), indawo_ekuyiwa_kuyo_ixabiso_indeksa = 빼기(1), ibhayithi_iingcombolo = 빼기(2), 시작자리 = 빼기(1), 첫값 = 빼기(2);
                if (객체유효(첫값) && 객체유효(ibhayithi_iingcombolo)) {
                    int 분류코드 = 힙[첫값];
                    if (힙[ibhayithi_iingcombolo] != 분류코드 || (분류코드 != 2 && 분류코드 != 3 && (분류코드 < 20 || 분류코드 > 23))) ukungaphumeleli_ixabiso("arraycopy type mismatch");
                    else if (항목수 < 0 || 시작자리 < 0 || indawo_ekuyiwa_kuyo_ixabiso_indeksa < 0 || 시작자리 > 힙[첫값 + 1] - 항목수 || indawo_ekuyiwa_kuyo_ixabiso_indeksa > 힙[ibhayithi_iingcombolo + 1] - 항목수) ukungaphumeleli_ixabiso("ArrayIndexOutOfBoundsException");
                    else if (첫값 == ibhayithi_iingcombolo && indawo_ekuyiwa_kuyo_ixabiso_indeksa > 시작자리) { for (int iluphu_indeksa = 항목수 - 1; iluphu_indeksa >= 0; iluphu_indeksa--) 힙[ibhayithi_iingcombolo + 2 + indawo_ekuyiwa_kuyo_ixabiso_indeksa + iluphu_indeksa] = 힙[첫값 + 2 + 시작자리 + iluphu_indeksa]; }
                    else { for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수 && !Impazamo; iluphu_indeksa++) { int iingcombolo_ixabiso = 힙[첫값 + 2 + 시작자리 + iluphu_indeksa]; if (분류코드 != 3 || 배열저장가능(ibhayithi_iingcombolo, iingcombolo_ixabiso)) 힙[ibhayithi_iingcombolo + 2 + indawo_ekuyiwa_kuyo_ixabiso_indeksa + iluphu_indeksa] = iingcombolo_ixabiso; } }
                }
                return true;
            }
        }
        if (Igama_I_SMS(umnini, "java/util/ArrayList") || Igama_I_SMS(umnini, "java/util/List") || Igama_I_SMS(umnini, "java/util/HashMap") || Igama_I_SMS(umnini, "java/util/Map")) {
            모음호출(umnini, igama_engajikiyo, 서술상수, 명령코드); return true;
        }
        return false;
    }
    static void 모음늘리기(int into_Isalathiso, int 필요수) {
        int 이전값 = 힙[into_Isalathiso + 2], 용량값 = 이전값 == 0 ? 0 : 힙[이전값 + 1];
        if (용량값 >= 필요수) return;
        int 다음자리 = 용량값 < 8 ? 8 : 용량값 * 2; if (다음자리 < 필요수) 다음자리 = 필요수;
        int iingcombolo_ULUHLU = yabela_Ugcino(3, 다음자리); if (Impazamo) return;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 용량값; iluphu_indeksa++) 힙[iingcombolo_ULUHLU + 2 + iluphu_indeksa] = 힙[이전값 + 2 + iluphu_indeksa];
        힙[into_Isalathiso + 2] = iingcombolo_ULUHLU; 힙참조[into_Isalathiso + 2] = 1;
    }
    static void 모음호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        boolean 대응참조 = Igama_I_SMS(umnini, "java/util/HashMap") || Igama_I_SMS(umnini, "java/util/Map"); int 분류코드 = 대응참조 ? 11 : 10;
        if (Igama_I_SMS(igama_engajikiyo, "<init>") && 명령코드 == 183 && Igama_I_SMS(서술상수, "()V")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 분류코드)) 모음늘리기(into_Isalathiso, 8); return; }
        if (명령코드 != 182 && 명령코드 != 185) { ukungaphumeleli_ixabiso("invalid collection invocation"); return; }
        if (Igama_I_SMS(igama_engajikiyo, "size") && Igama_I_SMS(서술상수, "()I") || Igama_I_SMS(igama_engajikiyo, "isEmpty") && Igama_I_SMS(서술상수, "()Z")) {
            int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 분류코드)) 넣기(Igama_I_SMS(igama_engajikiyo, "size") ? 힙[into_Isalathiso + 3] : 힙[into_Isalathiso + 3] == 0 ? 1 : 0, 1); return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "clear") && Igama_I_SMS(서술상수, "()V")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 분류코드)) { int iingcombolo_ULUHLU = 힙[into_Isalathiso + 2]; for (int iluphu_indeksa = 0; iluphu_indeksa < 힙[iingcombolo_ULUHLU + 1]; iluphu_indeksa++) 힙[iingcombolo_ULUHLU + 2 + iluphu_indeksa] = 0; 힙[into_Isalathiso + 3] = 0; } return; }
        if (!대응참조 && Igama_I_SMS(igama_engajikiyo, "add") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            int iingcombolo_ixabiso = 빼기(2), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 10)) return;
            int 항목수 = 힙[into_Isalathiso + 3]; 모음늘리기(into_Isalathiso, 항목수 + 1); if (!Impazamo) { 힙[힙[into_Isalathiso + 2] + 2 + 항목수] = iingcombolo_ixabiso; 힙[into_Isalathiso + 3] = 항목수 + 1; 넣기(1, 1); } return;
        }
        if (!대응참조 && (Igama_I_SMS(igama_engajikiyo, "get") || Igama_I_SMS(igama_engajikiyo, "remove")) && Igama_I_SMS(서술상수, "(I)Ljava/lang/Object;") || !대응참조 && Igama_I_SMS(igama_engajikiyo, "set") && Igama_I_SMS(서술상수, "(ILjava/lang/Object;)Ljava/lang/Object;")) {
            boolean 지정여부 = Igama_I_SMS(igama_engajikiyo, "set"); int iingcombolo_ixabiso = 지정여부 ? 빼기(2) : 0, 항목자리 = 빼기(1), into_Isalathiso = 빼기(2);
            if (!into_ixabiso(into_Isalathiso, 10)) return;
            int 항목수 = 힙[into_Isalathiso + 3], iingcombolo_ULUHLU = 힙[into_Isalathiso + 2];
            if (항목자리 < 0 || 항목자리 >= 항목수) { 예외던짐(6, "list index"); return; }
            int 이전값 = 힙[iingcombolo_ULUHLU + 2 + 항목자리];
            if (지정여부) 힙[iingcombolo_ULUHLU + 2 + 항목자리] = iingcombolo_ixabiso;
            if (Igama_I_SMS(igama_engajikiyo, "remove")) { for (int iluphu_indeksa = 항목자리 + 1; iluphu_indeksa < 항목수; iluphu_indeksa++) 힙[iingcombolo_ULUHLU + 1 + iluphu_indeksa] = 힙[iingcombolo_ULUHLU + 2 + iluphu_indeksa]; 힙[iingcombolo_ULUHLU + 1 + 항목수] = 0; 힙[into_Isalathiso + 3] = 항목수 - 1; }
            넣기(이전값, 2); return;
        }
        if (대응참조 && (Igama_I_SMS(igama_engajikiyo, "get") || Igama_I_SMS(igama_engajikiyo, "remove")) && Igama_I_SMS(서술상수, "(Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Igama_I_SMS(igama_engajikiyo, "put") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;Ljava/lang/Object;)Ljava/lang/Object;") || 대응참조 && Igama_I_SMS(igama_engajikiyo, "containsKey") && Igama_I_SMS(서술상수, "(Ljava/lang/Object;)Z")) {
            boolean 넣기여부 = Igama_I_SMS(igama_engajikiyo, "put"), shenxisa = Igama_I_SMS(igama_engajikiyo, "remove");
            int iingcombolo_ixabiso = 넣기여부 ? 빼기(2) : 0, iqhosha_Isalathiso = 빼기(2), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 11)) return;
            int 항목수 = 힙[into_Isalathiso + 3], iingcombolo_ULUHLU = 힙[into_Isalathiso + 2], 찾은여부 = -1;
            for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) if (값같음(iqhosha_Isalathiso, 힙[iingcombolo_ULUHLU + 2 + 2 * iluphu_indeksa])) { 찾은여부 = iluphu_indeksa; break; }
            int 이전값 = 찾은여부 < 0 ? 0 : 힙[iingcombolo_ULUHLU + 3 + 2 * 찾은여부];
            if (넣기여부) {
                if (찾은여부 < 0) { 모음늘리기(into_Isalathiso, (항목수 + 1) * 2); iingcombolo_ULUHLU = 힙[into_Isalathiso + 2]; 찾은여부 = 항목수; if (!Impazamo) 힙[into_Isalathiso + 3] = 항목수 + 1; }
                if (!Impazamo) { 힙[iingcombolo_ULUHLU + 2 + 2 * 찾은여부] = iqhosha_Isalathiso; 힙[iingcombolo_ULUHLU + 3 + 2 * 찾은여부] = iingcombolo_ixabiso; }
            }
            if (shenxisa && 찾은여부 >= 0) { for (int iluphu_indeksa = 찾은여부 + 1; iluphu_indeksa < 항목수; iluphu_indeksa++) { 힙[iingcombolo_ULUHLU + 2 * iluphu_indeksa] = 힙[iingcombolo_ULUHLU + 2 + 2 * iluphu_indeksa]; 힙[iingcombolo_ULUHLU + 1 + 2 * iluphu_indeksa] = 힙[iingcombolo_ULUHLU + 3 + 2 * iluphu_indeksa]; } 힙[iingcombolo_ULUHLU + 2 * 항목수] = 0; 힙[iingcombolo_ULUHLU + 1 + 2 * 항목수] = 0; 힙[into_Isalathiso + 3] = 항목수 - 1; }
            if (Igama_I_SMS(igama_engajikiyo, "containsKey")) 넣기(찾은여부 >= 0 ? 1 : 0, 1); else 넣기(이전값, 2);
            return;
        }
        ukungaphumeleli_ixabiso("unsupported collection method");
    }
    static boolean 잠금얻기(int into_Isalathiso) {
        if (!객체유효(into_Isalathiso)) return false;
        if (잠금깊이[into_Isalathiso] != 0 && 잠금주인[into_Isalathiso] != 현재가닥 + 1) { 바꿈요청 = true; return false; }
        잠금주인[into_Isalathiso] = 현재가닥 + 1; 잠금깊이[into_Isalathiso]++; return true;
    }
    static void 잠금풀기(int into_Isalathiso) {
        if (!객체유효(into_Isalathiso)) return;
        if (잠금깊이[into_Isalathiso] == 0 || 잠금주인[into_Isalathiso] != 현재가닥 + 1) { 예외던짐(13, "monitor not owned"); return; }
        if (--잠금깊이[into_Isalathiso] == 0) 잠금주인[into_Isalathiso] = 0;
    }
    static boolean tshintshela_ithredi() {
        ithredi_ifreyim[현재가닥] = ifreyim_indeksa;
        if (ifreyim_indeksa < 현재가닥 * 32) ithredi_imo[현재가닥] = 3;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 가닥수; iluphu_indeksa++) if (ithredi_imo[iluphu_indeksa] == 2 && ithredi_imo[가닥대기[iluphu_indeksa]] == 3) ithredi_imo[iluphu_indeksa] = 1;
        for (int iluphu_indeksa = 1; iluphu_indeksa <= 가닥수; iluphu_indeksa++) {
            int 다음자리 = (현재가닥 + iluphu_indeksa) % 가닥수;
            if (ithredi_imo[다음자리] == 1) { 현재가닥 = 다음자리; ifreyim_indeksa = ithredi_ifreyim[다음자리]; 바꿈요청 = false; return true; }
        }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 가닥수; iluphu_indeksa++) if (ithredi_imo[iluphu_indeksa] != 3) { ukungaphumeleli_ixabiso("thread deadlock"); return false; }
        return false;
    }
    static void 가닥호출(int igama_engajikiyo, int 서술상수, int 명령코드) { Inkqubo_ithredi(igama_engajikiyo, 서술상수, 명령코드, false); }
    static void Inkqubo_ithredi(int igama_engajikiyo, int 서술상수, int 명령코드, boolean isiXhosa) {
        if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, isiXhosa ? "misa_okwexeshana_umsebenzi" : "yield") && Igama_I_SMS(서술상수, "()V")) { 바꿈요청 = true; return; }
        if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "currentThread") && Igama_I_SMS(서술상수, "()Ljava/lang/Thread;")) { 넣기(ithredi_into[현재가닥], 2); return; }
        if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>") && (Igama_I_SMS(서술상수, "()V") || Igama_I_SMS(서술상수, isiXhosa ? "(LisiXhosa/자체/실행할일;)V" : "(Ljava/lang/Runnable;)V"))) {
            int ithagethi_idilesi = Igama_I_SMS(서술상수, "()V") ? 0 : 빼기(2), into_Isalathiso = 빼기(2);
            if (!객체유효(into_Isalathiso)) return;
            if (힙[into_Isalathiso] == 13) { 힙[into_Isalathiso + 2] = ithagethi_idilesi; 힙참조[into_Isalathiso + 2] = 1; }
            else if (ithagethi_idilesi != 0) ukungaphumeleli_ixabiso("Runnable constructor for Thread subclass unsupported");
            return;
        }
        if (명령코드 == 182 && (Igama_I_SMS(igama_engajikiyo, isiXhosa ? "qala_umsebenzi" : "start") || Igama_I_SMS(igama_engajikiyo, isiXhosa ? "기다리기" : "join")) && Igama_I_SMS(서술상수, "()V") || 명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, isiXhosa ? "살아있는가" : "isAlive") && Igama_I_SMS(서술상수, "()Z")) {
            int into_Isalathiso = 빼기(2); if (!객체유효(into_Isalathiso)) return;
            int isazisi_ixabiso = -1; for (int iluphu_indeksa = 0; iluphu_indeksa < 가닥수; iluphu_indeksa++) if (ithredi_into[iluphu_indeksa] == into_Isalathiso) isazisi_ixabiso = iluphu_indeksa;
            if (Igama_I_SMS(igama_engajikiyo, isiXhosa ? "살아있는가" : "isAlive")) { 넣기(isazisi_ixabiso >= 0 && ithredi_imo[isazisi_ixabiso] != 3 ? 1 : 0, 1); return; }
            if (Igama_I_SMS(igama_engajikiyo, isiXhosa ? "기다리기" : "join")) { if (isazisi_ixabiso >= 0 && ithredi_imo[isazisi_ixabiso] != 3) { 가닥대기[현재가닥] = isazisi_ixabiso; ithredi_imo[현재가닥] = 2; 바꿈요청 = true; } return; }
            if (isazisi_ixabiso >= 0) { 예외던짐(isiXhosa ? 38 : 16, "thread already started"); return; }
            if (가닥수 == 4) { ukungaphumeleli_ixabiso("thread limit (4 including main)"); return; }
            int ithagethi_idilesi = 힙[into_Isalathiso] == 13 ? 힙[into_Isalathiso + 2] : into_Isalathiso;
            int ifayile_indeksa = ithagethi_idilesi > 0 && 힙[ithagethi_idilesi] >= 32 ? igama_imethodi(힙[ithagethi_idilesi] - 32, isiXhosa ? "ukwenza_umsebenzi" : "run", "()V") : -1;
            if (ithagethi_idilesi != 0 && ifayile_indeksa < 0) { ukungaphumeleli_ixabiso("Runnable.run required"); return; }
            isazisi_ixabiso = 가닥수++; ithredi_into[isazisi_ixabiso] = into_Isalathiso; ithredi_ithagethi[isazisi_ixabiso] = ithagethi_idilesi;
            int ifreyim = isazisi_ixabiso * 32; ithredi_ifreyim[isazisi_ixabiso] = ifayile_indeksa < 0 ? ifreyim - 1 : ifreyim; ithredi_imo[isazisi_ixabiso] = ifayile_indeksa < 0 ? 3 : 1;
            if (ifayile_indeksa >= 0) { ifreyim_imethodi[ifreyim] = ifayile_indeksa; 틀위치[ifreyim] = imethodi_qala[ifayile_indeksa]; eyale_ndawo_ixabiso[ifreyim * 128] = ithagethi_idilesi; eyale_ndawo_uhlobo[ifreyim * 128] = 2; }
            return;
        }
        ukungaphumeleli_ixabiso("unsupported Thread method");
    }
    static int[] 통신임시 = new int[514], idilesi_I_SMS = new int[16];
    static int eyale_ndawo_idilesi() { return idilesi_into(0x7f000001); }
    static int idilesi_into(int ixabiso) { int into_Isalathiso = yabela_Ugcino(14, 1); if (!Impazamo) 힙[into_Isalathiso + 2] = ixabiso; return into_Isalathiso; }
    static int 주소해독(int into_Isalathiso) {
        if (into_Isalathiso == 0 || 글같음(into_Isalathiso, umsingathi_ikharakhtha("localhost"), false)) return 0x7f000001;
        if (!into_ixabiso(into_Isalathiso, 1)) return 0;
        int iingcombolo_ixabiso = 0, 총수 = 0, idilesi_ibhayithi = 0, 자릿수 = 0, 항목수 = 힙[into_Isalathiso + 1];
        for (int iluphu_indeksa = 0; iluphu_indeksa <= 항목수; iluphu_indeksa++) {
            int ikhowudi_yekharakhtha = iluphu_indeksa == 항목수 ? '.' : 힙[into_Isalathiso + 2 + iluphu_indeksa];
            if (ikhowudi_yekharakhtha == '.') { if (자릿수 == 0 || 총수 == 4) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } iingcombolo_ixabiso = iingcombolo_ixabiso << 8 | idilesi_ibhayithi; 총수++; idilesi_ibhayithi = 자릿수 = 0; }
            else { if (ikhowudi_yekharakhtha < '0' || ikhowudi_yekharakhtha > '9' || ++자릿수 > 3 || (idilesi_ibhayithi = idilesi_ibhayithi * 10 + ikhowudi_yekharakhtha - '0') > 255) { 예외던짐(18, "numeric IPv4 address required; DNS unavailable"); return 0; } }
        }
        if (총수 != 4) { 예외던짐(18, "invalid IPv4 address"); return 0; } return iingcombolo_ixabiso;
    }
    static int idilesi_ikharakhtha(int iingcombolo_ixabiso) {
        int 항목수 = 0;
        for (int 이동비트 = 24; 이동비트 >= 0; 이동비트 -= 8) {
            int idilesi_ibhayithi = iingcombolo_ixabiso >>> 이동비트 & 255;
            if (idilesi_ibhayithi >= 100) idilesi_I_SMS[항목수++] = '0' + idilesi_ibhayithi / 100;
            if (idilesi_ibhayithi >= 10) idilesi_I_SMS[항목수++] = '0' + idilesi_ibhayithi / 10 % 10;
            idilesi_I_SMS[항목수++] = '0' + idilesi_ibhayithi % 10; if (이동비트 != 0) idilesi_I_SMS[항목수++] = '.';
        }
        int into_Isalathiso = yabela_Ugcino(1, 항목수); if (!Impazamo) for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 힙[into_Isalathiso + 2 + iluphu_indeksa] = idilesi_I_SMS[iluphu_indeksa]; return into_Isalathiso;
    }
    static void 통신호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        if (Igama_I_SMS(umnini, "java/net/InetAddress")) {
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "getLoopbackAddress") && Igama_I_SMS(서술상수, "()Ljava/net/InetAddress;")) { 넣기(eyale_ndawo_idilesi(), 2); return; }
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "getByName") && Igama_I_SMS(서술상수, "(Ljava/lang/String;)Ljava/net/InetAddress;")) {
                int iingcombolo_ixabiso = 주소해독(빼기(2)); if (던진객체 == 0 && !Impazamo) 넣기(idilesi_into(iingcombolo_ixabiso), 2); return;
            }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "getHostAddress") && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 14)) 넣기(idilesi_ikharakhtha(힙[into_Isalathiso + 2]), 2); return; }
        }
        if (Igama_I_SMS(umnini, "java/net/DatagramPacket")) {
            if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>") && (Igama_I_SMS(서술상수, "([BI)V") || Igama_I_SMS(서술상수, "([BILjava/net/InetAddress;I)V"))) {
                boolean indawo_ekuyiwa_kuyo_ixabiso_Isalathiso = Igama_I_SMS(서술상수, "([BILjava/net/InetAddress;I)V"); int 접속번호 = indawo_ekuyiwa_kuyo_ixabiso_Isalathiso ? 빼기(1) : 0, idilesi_Isalathiso = indawo_ekuyiwa_kuyo_ixabiso_Isalathiso ? 빼기(2) : 0;
                int 항목수 = 빼기(1), iingcombolo_ULUHLU = 빼기(2), into_Isalathiso = 빼기(2);
                if (!into_ixabiso(into_Isalathiso, 16) || !into_ixabiso(iingcombolo_ULUHLU, 20)) return;
                if (항목수 < 0 || 항목수 > 힙[iingcombolo_ULUHLU + 1] || 접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid datagram length/port"); return; }
                if (idilesi_Isalathiso != 0 && !into_ixabiso(idilesi_Isalathiso, 14)) return;
                힙[into_Isalathiso + 2] = iingcombolo_ULUHLU; 힙참조[into_Isalathiso + 2] = 1; 힙[into_Isalathiso + 3] = 항목수;
                힙[into_Isalathiso + 4] = idilesi_Isalathiso; 힙참조[into_Isalathiso + 4] = 1; 힙[into_Isalathiso + 5] = 접속번호; return;
            }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "setLength") && Igama_I_SMS(서술상수, "(I)V")) {
                int 항목수 = 빼기(1), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 16)) return;
                if (항목수 < 0 || 항목수 > 힙[힙[into_Isalathiso + 2] + 1]) 예외던짐(9, "invalid datagram length"); else 힙[into_Isalathiso + 3] = 항목수; return;
            }
            if (명령코드 == 182 && (Igama_I_SMS(igama_engajikiyo, "getData") && Igama_I_SMS(서술상수, "()[B") || Igama_I_SMS(igama_engajikiyo, "getLength") && Igama_I_SMS(서술상수, "()I") || Igama_I_SMS(igama_engajikiyo, "getAddress") && Igama_I_SMS(서술상수, "()Ljava/net/InetAddress;") || Igama_I_SMS(igama_engajikiyo, "getPort") && Igama_I_SMS(서술상수, "()I"))) {
                int into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 16)) return;
                int 항목자리 = Igama_I_SMS(igama_engajikiyo, "getData") ? 2 : Igama_I_SMS(igama_engajikiyo, "getLength") ? 3 : Igama_I_SMS(igama_engajikiyo, "getAddress") ? 4 : 5;
                넣기(힙[into_Isalathiso + 항목자리], 항목자리 == 2 || 항목자리 == 4 ? 2 : 1); return;
            }
        }
        if (Igama_I_SMS(umnini, "java/net/DatagramSocket")) {
            if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>") && (Igama_I_SMS(서술상수, "()V") || Igama_I_SMS(서술상수, "(I)V"))) {
                int 접속번호 = Igama_I_SMS(서술상수, "()V") ? 0 : 빼기(1), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 15)) return;
                if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
                int 열린파일번호 = umsebenzisi.vula_Inethiwekhi(접속번호); if (열린파일번호 < 0) 예외던짐(39, "UDP socket/bind failed"); else 힙[into_Isalathiso + 2] = 열린파일번호; return;
            }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "setSoTimeout") && Igama_I_SMS(서술상수, "(I)V")) {
                int 밀리초값 = 빼기(1), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 15)) return;
                if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[into_Isalathiso + 3] = 밀리초값; return;
            }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "getLocalPort") && Igama_I_SMS(서술상수, "()I")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 15)) 넣기(힙[into_Isalathiso + 2] < 0 ? -1 : umsebenzisi.Inethiwekhi_iphothi(힙[into_Isalathiso + 2]), 1); return; }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "isClosed") && Igama_I_SMS(서술상수, "()Z")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 15)) 넣기(힙[into_Isalathiso + 2] < 0 ? 1 : 0, 1); return; }
            if (명령코드 == 182 && Igama_I_SMS(igama_engajikiyo, "close") && Igama_I_SMS(서술상수, "()V")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 15) && 힙[into_Isalathiso + 2] >= 0) { umsebenzisi.파일서술자닫기(힙[into_Isalathiso + 2]); 힙[into_Isalathiso + 2] = -1; } return; }
            if (명령코드 == 182 && (Igama_I_SMS(igama_engajikiyo, "send") || Igama_I_SMS(igama_engajikiyo, "receive")) && Igama_I_SMS(서술상수, "(Ljava/net/DatagramPacket;)V")) {
                int ipakethe = 빼기(2), into_Isalathiso = 빼기(2); if (!into_ixabiso(ipakethe, 16) || !into_ixabiso(into_Isalathiso, 15)) return;
                int iingcombolo_ULUHLU = 힙[ipakethe + 2], 유효길이 = 힙[ipakethe + 3], 열린파일번호 = 힙[into_Isalathiso + 2];
                if (열린파일번호 < 0) { 예외던짐(39, "socket closed"); return; }
                if (Igama_I_SMS(igama_engajikiyo, "send")) {
                    if (!into_ixabiso(힙[ipakethe + 4], 14)) return;
                    if (유효길이 > 512) { 예외던짐(11, "datagram limit (512 bytes)"); return; }
                    for (int iluphu_indeksa = 0; iluphu_indeksa < 유효길이; iluphu_indeksa++) 통신임시[iluphu_indeksa] = 힙[iingcombolo_ULUHLU + 2 + iluphu_indeksa];
                    if (umsebenzisi.thumela_Inethiwekhi(열린파일번호, 힙[힙[ipakethe + 4] + 2], 힙[ipakethe + 5], 통신임시, 유효길이) < 0) 예외던짐(11, "UDP send failed");
                } else {
                    int 항목수 = umsebenzisi.통신받기(열린파일번호, 통신임시, 유효길이 > 512 ? 512 : 유효길이);
                    if (항목수 == -11) {
                        int 현재시각 = umsebenzisi.밀리초();
                        if (힙[into_Isalathiso + 4] == 0) 힙[into_Isalathiso + 4] = 현재시각 + 1;
                        if (힙[into_Isalathiso + 3] > 0 && 현재시각 - (힙[into_Isalathiso + 4] - 1) >= 힙[into_Isalathiso + 3]) { 힙[into_Isalathiso + 4] = 0; 예외던짐(19, "receive timed out"); return; }
                        넣기(into_Isalathiso, 2); 넣기(ipakethe, 2); 틀위치[ifreyim_indeksa] = ifreyim_umyalelo[ifreyim_indeksa]; 바꿈요청 = true; return;
                    }
                    힙[into_Isalathiso + 4] = 0;
                    if (항목수 < 0) { 예외던짐(11, "UDP receive failed"); return; }
                    for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 힙[iingcombolo_ULUHLU + 2 + iluphu_indeksa] = (byte)통신임시[iluphu_indeksa];
                    힙[ipakethe + 3] = 항목수; 힙[ipakethe + 4] = idilesi_into(통신임시[513]); 힙참조[ipakethe + 4] = 1; 힙[ipakethe + 5] = 통신임시[512];
                }
                return;
            }
        }
        ukungaphumeleli_ixabiso("unsupported java.net method");
    }
    static boolean 흐름대기(int into_Isalathiso) {
        int 현재시각 = umsebenzisi.밀리초();
        if (힙[into_Isalathiso + 5] == 0) 힙[into_Isalathiso + 5] = 현재시각 + 1;
        if (힙[into_Isalathiso + 3] > 0 && 현재시각 - (힙[into_Isalathiso + 5] - 1) >= 힙[into_Isalathiso + 3]) { 힙[into_Isalathiso + 5] = 0; 예외던짐(19, "stream wait timed out"); return false; }
        틀위치[ifreyim_indeksa] = ifreyim_umyalelo[ifreyim_indeksa]; 바꿈요청 = true; return true;
    }
    static void 흐름호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        boolean 수신쪽 = Igama_I_SMS(umnini, "java/net/ServerSocket"), Stream = Igama_I_SMS(umnini, "java/io/InputStream") || Igama_I_SMS(umnini, "java/io/OutputStream");
        if (!Stream && 명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>")) {
            boolean 빈여부 = Igama_I_SMS(서술상수, "()V"), 이름지정여부 = Igama_I_SMS(서술상수, "(Ljava/lang/String;I)V"), 주소지정여부 = Igama_I_SMS(서술상수, "(Ljava/net/InetAddress;I)V");
            if (!(빈여부 || 수신쪽 && Igama_I_SMS(서술상수, "(I)V") || !수신쪽 && (이름지정여부 || 주소지정여부))) { ukungaphumeleli_ixabiso("unsupported socket constructor"); return; }
            int 접속번호 = 빈여부 ? 0 : 빼기(1), idilesi_Isalathiso = 이름지정여부 || 주소지정여부 ? 빼기(2) : 0, into_Isalathiso = 빼기(2);
            if (!into_ixabiso(into_Isalathiso, 수신쪽 ? 18 : 17)) return;
            if (접속번호 < 0 || 접속번호 > 65535) { 예외던짐(9, "invalid port"); return; }
            if (주소지정여부 && !into_ixabiso(idilesi_Isalathiso, 14)) return;
            int Inethiwekhi_idilesi = 이름지정여부 ? 주소해독(idilesi_Isalathiso) : 주소지정여부 ? 힙[idilesi_Isalathiso + 2] : 0x7f000001;
            if (Impazamo || 던진객체 != 0) return;
            int 열린파일번호 = umsebenzisi.Stream_isilawuli(0, 0, 0); if (열린파일번호 < 0) { 예외던짐(39, "socket slots exhausted"); return; }
            int 처리값 = 빈여부 ? 0 : 수신쪽 ? umsebenzisi.Stream_isilawuli(1, 열린파일번호, 접속번호) : umsebenzisi.I_Connect_Stream(열린파일번호, Inethiwekhi_idilesi, 접속번호);
            if (처리값 < 0) { umsebenzisi.파일서술자닫기(열린파일번호); 예외던짐(39, "socket bind/connect failed"); return; }
            힙[into_Isalathiso + 2] = 열린파일번호; 힙[into_Isalathiso + 4] = 접속번호; 힙[into_Isalathiso + 6] = 빈여부 ? 0 : 1; return;
        }
        if (!Stream && Igama_I_SMS(igama_engajikiyo, "setSoTimeout") && Igama_I_SMS(서술상수, "(I)V")) { int 밀리초값 = 빼기(1), into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 수신쪽 ? 18 : 17)) return; if (밀리초값 < 0) 예외던짐(9, "negative timeout"); else 힙[into_Isalathiso + 3] = 밀리초값; return; }
        if (!Stream && Igama_I_SMS(igama_engajikiyo, "close") && Igama_I_SMS(서술상수, "()V")) { int into_Isalathiso = 빼기(2); if (into_ixabiso(into_Isalathiso, 수신쪽 ? 18 : 17) && 힙[into_Isalathiso + 2] >= 0) { umsebenzisi.파일서술자닫기(힙[into_Isalathiso + 2]); 힙[into_Isalathiso + 2] = -1; } return; }
        if (!Stream && (Igama_I_SMS(igama_engajikiyo, "getLocalPort") || Igama_I_SMS(igama_engajikiyo, "getPort") || Igama_I_SMS(igama_engajikiyo, "isClosed") || Igama_I_SMS(igama_engajikiyo, "isConnected"))) {
            int into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 수신쪽 ? 18 : 17)) return;
            넣기(Igama_I_SMS(igama_engajikiyo, "isClosed") ? 힙[into_Isalathiso + 2] < 0 ? 1 : 0 : Igama_I_SMS(igama_engajikiyo, "isConnected") ? 힙[into_Isalathiso + 6] : Igama_I_SMS(igama_engajikiyo, "getPort") ? 힙[into_Isalathiso + 4] : 힙[into_Isalathiso + 2] < 0 ? -1 : umsebenzisi.Stream_isilawuli(4, 힙[into_Isalathiso + 2], 0), 1); return;
        }
        if (수신쪽 && Igama_I_SMS(igama_engajikiyo, "accept") && Igama_I_SMS(서술상수, "()Ljava/net/Socket;")) {
            int into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 18)) return; int 열린파일번호 = umsebenzisi.Stream_isilawuli(3, 힙[into_Isalathiso + 2], 0);
            if (열린파일번호 == -11) { if (흐름대기(into_Isalathiso)) 넣기(into_Isalathiso, 2); return; }
            힙[into_Isalathiso + 5] = 0; if (열린파일번호 < 0) { 예외던짐(11, "accept failed"); return; }
            int 반환값 = yabela_Ugcino(17, 5); if (Impazamo) { umsebenzisi.파일서술자닫기(열린파일번호); return; } 힙[반환값 + 2] = 열린파일번호; 힙[반환값 + 4] = umsebenzisi.Stream_isilawuli(5, 열린파일번호, 0); 힙[반환값 + 6] = 1; 넣기(반환값, 2); return;
        }
        if (!수신쪽 && !Stream && ((Igama_I_SMS(igama_engajikiyo, "getInputStream") && Igama_I_SMS(서술상수, "()Ljava/io/InputStream;")) || (Igama_I_SMS(igama_engajikiyo, "getOutputStream") && Igama_I_SMS(서술상수, "()Ljava/io/OutputStream;")))) {
            int into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 17)) return; if (힙[into_Isalathiso + 2] < 0 || 힙[into_Isalathiso + 6] == 0) { 예외던짐(39, "socket is not connected"); return; }
            int 반환값 = yabela_Ugcino(19, 4); if (Impazamo) return; 힙[반환값 + 2] = into_Isalathiso; 힙참조[반환값 + 2] = 1; 힙[반환값 + 3] = Igama_I_SMS(igama_engajikiyo, "getInputStream") ? 0 : 1; 넣기(반환값, 2); return;
        }
        if (Stream) {
            boolean 읽기여부 = Igama_I_SMS(igama_engajikiyo, "read"), 쓰기여부 = Igama_I_SMS(igama_engajikiyo, "write"), thintela = Igama_I_SMS(서술상수, "([B)I") || Igama_I_SMS(서술상수, "([B)V"), 부분배열여부 = Igama_I_SMS(서술상수, "([BII)I") || Igama_I_SMS(서술상수, "([BII)V");
            int 항목수 = 부분배열여부 ? 빼기(1) : 0, 시작변위 = 부분배열여부 ? 빼기(1) : 0, iingcombolo_ULUHLU = thintela || 부분배열여부 ? 빼기(2) : 0;
            int iingcombolo_ixabiso = 쓰기여부 && Igama_I_SMS(서술상수, "(I)V") ? 빼기(1) : 0, into_Isalathiso = 빼기(2);
            if (!into_ixabiso(into_Isalathiso, 19)) return; int 부모참조 = 힙[into_Isalathiso + 2], 열린파일번호 = 힙[부모참조 + 2];
            if (열린파일번호 < 0) { 예외던짐(11, "stream closed"); return; }
            if (Igama_I_SMS(igama_engajikiyo, "close") && Igama_I_SMS(서술상수, "()V")) { umsebenzisi.파일서술자닫기(열린파일번호); 힙[부모참조 + 2] = -1; return; }
            if (Igama_I_SMS(igama_engajikiyo, "flush") && Igama_I_SMS(서술상수, "()V")) return;
            if ((!읽기여부 && !쓰기여부) || 읽기여부 != (힙[into_Isalathiso + 3] == 0)) { ukungaphumeleli_ixabiso("unsupported stream operation"); return; }
            if (thintela || 부분배열여부) { if (!into_ixabiso(iingcombolo_ULUHLU, 20)) return; if (thintela) 항목수 = 힙[iingcombolo_ULUHLU + 1]; if (시작변위 < 0 || 항목수 < 0 || 시작변위 > 힙[iingcombolo_ULUHLU + 1] - 항목수) { 예외던짐(6, "stream array bounds"); return; } }
            else 항목수 = 1;
            if (항목수 == 0) { if (읽기여부) 넣기(0, 1); return; }
            int 완료수 = 쓰기여부 ? 힙[into_Isalathiso + 4] : 0, 처리값 = 0;
            while (완료수 < 항목수) {
                처리값 = 읽기여부 ? umsebenzisi.파일한바이트읽기(열린파일번호) : umsebenzisi.파일한바이트쓰기(열린파일번호, thintela || 부분배열여부 ? 힙[iingcombolo_ULUHLU + 2 + 시작변위 + 완료수] : iingcombolo_ixabiso);
                if (처리값 < 0 || 읽기여부 && 처리값 == 256) break;
                if (읽기여부 && (thintela || 부분배열여부)) 힙[iingcombolo_ULUHLU + 2 + 시작변위 + 완료수] = (byte)처리값;
                완료수++; if (읽기여부 && !(thintela || 부분배열여부)) break;
            }
            if (처리값 == -11 && (쓰기여부 || 완료수 == 0)) {
                힙[into_Isalathiso + 4] = 완료수;
                if (흐름대기(부모참조)) { 넣기(into_Isalathiso, 2); if (thintela || 부분배열여부) 넣기(iingcombolo_ULUHLU, 2); if (부분배열여부) { 넣기(시작변위, 1); 넣기(항목수, 1); } if (쓰기여부 && !(thintela || 부분배열여부)) 넣기(iingcombolo_ixabiso, 1); } return;
            }
            힙[into_Isalathiso + 4] = 0; 힙[부모참조 + 5] = 0;
            if (처리값 < 0 && 처리값 != -11) { 예외던짐(11, "stream I/O failed"); return; }
            if (읽기여부) 넣기(완료수 == 0 && 처리값 == 256 ? -1 : thintela || 부분배열여부 ? 완료수 : 처리값, 1); return;
        }
        ukungaphumeleli_ixabiso("unsupported Socket/ServerSocket method");
    }
    static int[] 화면참조 = new int[32], 화면글임시 = new int[256], 나중실행 = new int[8];
    static int 나중수;
    static int[] 나중한국어 = new int[8];
    static boolean 사건중;
    static int 한국어화면종(int igama_engajikiyo) {
        if (Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/i_window")) return 24;
        if (Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/Ilebhile")) return 26;
        if (Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/iqhosha")) return 27;
        if (Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/I_SMS_ifildi")) return 28;
        if (Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/동작알림")) return 29;
        return 0;
    }
    static boolean 한국어화면소유(int igama_engajikiyo) {
        return 한국어화면종(igama_engajikiyo) != 0 || Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/화면구성요소") || Igama_I_SMS(igama_engajikiyo, "isiXhosa/자체/umcimbi_ityhu");
    }
    static int 화면종(int igama_engajikiyo) {
        int 한국어종 = 한국어화면종(igama_engajikiyo); if (한국어종 != 0) return 한국어종;
        if (Igama_I_SMS(igama_engajikiyo, "javax/swing/JFrame")) return 24;
        if (Igama_I_SMS(igama_engajikiyo, "javax/swing/JPanel")) return 25;
        if (Igama_I_SMS(igama_engajikiyo, "javax/swing/JLabel")) return 26;
        if (Igama_I_SMS(igama_engajikiyo, "javax/swing/JButton")) return 27;
        if (Igama_I_SMS(igama_engajikiyo, "javax/swing/JTextField")) return 28;
        if (Igama_I_SMS(igama_engajikiyo, "java/awt/event/ActionEvent")) return 29;
        if (Igama_I_SMS(igama_engajikiyo, "java/awt/FlowLayout")) return 30;
        return 0;
    }
    static boolean 화면소유(int igama_engajikiyo) {
        return 화면종(igama_engajikiyo) != 0 || Igama_I_SMS(igama_engajikiyo, "java/awt/Component") || Igama_I_SMS(igama_engajikiyo, "java/awt/Container") || Igama_I_SMS(igama_engajikiyo, "javax/swing/JComponent") || Igama_I_SMS(igama_engajikiyo, "javax/swing/AbstractButton") || Igama_I_SMS(igama_engajikiyo, "javax/swing/text/JTextComponent") || Igama_I_SMS(igama_engajikiyo, "javax/swing/SwingUtilities");
    }
    static boolean 화면객체(int into_Isalathiso) { if (!객체유효(into_Isalathiso)) return false; if (힙[into_Isalathiso] < 24 || 힙[into_Isalathiso] > 28) { ukungaphumeleli_ixabiso("unsupported Swing receiver"); return false; } return true; }
    static void 화면문자설정(int into_Isalathiso, int I_SMS_Isalathiso) {
        if (I_SMS_Isalathiso != 0 && !into_ixabiso(I_SMS_Isalathiso, 1)) return;
        int 항목수 = I_SMS_Isalathiso == 0 ? 0 : 힙[I_SMS_Isalathiso + 1]; if (항목수 > 254) { 예외던짐(9, "GUI text limit"); return; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) 화면글임시[iluphu_indeksa] = 힙[I_SMS_Isalathiso + 2 + iluphu_indeksa];
        if (umsebenzisi.화면글(힙[into_Isalathiso + 2], 화면글임시, 항목수) < 0) { 예외던짐(9, "GUI text too long/invalid"); return; }
        힙[into_Isalathiso + 3] = I_SMS_Isalathiso; 힙참조[into_Isalathiso + 3] = 1;
    }
    static int 화면문자읽기(int into_Isalathiso) {
        int isazisi_ixabiso = 힙[into_Isalathiso + 2], 항목수 = umsebenzisi.화면연결(8, isazisi_ixabiso, 0, 0, 0, 0), 사용수 = 0;
        if (항목수 < 0) { ukungaphumeleli_ixabiso("GUI text read failed"); return 0; }
        for (int iluphu_indeksa = 0; iluphu_indeksa < 항목수; iluphu_indeksa++) { int 부호값 = umsebenzisi.화면연결(9, isazisi_ixabiso, iluphu_indeksa, 0, 0, 0); if (부호값 >= 65536) { 부호값 -= 65536; 화면글임시[사용수++] = 0xd800 | 부호값 >> 10; 화면글임시[사용수++] = 0xdc00 | 부호값 & 1023; } else 화면글임시[사용수++] = 부호값; }
        int 반환값 = yabela_Ugcino(1, 사용수); if (!Impazamo) for (int iluphu_indeksa = 0; iluphu_indeksa < 사용수; iluphu_indeksa++) 힙[반환값 + 2 + iluphu_indeksa] = 화면글임시[iluphu_indeksa]; return 반환값;
    }
    /* isiXhosa 객체를 직접 만들고 ikheneli_ixabiso 화면 기능에 연결한다. Swing into_ixabiso/어댑터를 만들지 않는다. */
    static void 한국어화면호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        if (Igama_I_SMS(umnini, "isiXhosa/자체/umcimbi_ityhu")) {
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "나중에실행") && Igama_I_SMS(서술상수, "(LisiXhosa/자체/실행할일;)V")) {
                int umsebenzi_Isenzo = 빼기(2); if (!객체유효(umsebenzi_Isenzo)) return;
                if (나중수 == 8) { ukungaphumeleli_ixabiso("화면 작업 대기열이 가득 찼습니다"); return; }
                나중한국어[나중수] = 1; 나중실행[나중수++] = umsebenzi_Isenzo; return;
            }
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "사건처리중인가") && Igama_I_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ukungaphumeleli_ixabiso("지원하지 않는 isiXhosa 화면 일정 호출"); return;
        }
        if (Igama_I_SMS(umnini, "isiXhosa/자체/동작알림")) {
            int 알림 = 빼기(2); if (!into_ixabiso(알림, 29) || 힙[알림 + 3] == 0) return;
            if (Igama_I_SMS(igama_engajikiyo, "umcimbi_umthombo") && Igama_I_SMS(서술상수, "()LisiXhosa/자체/화면구성요소;")) 넣기(힙[알림 + 2], 2);
            else if (Igama_I_SMS(igama_engajikiyo, "umyalelo_I_SMS") && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[알림 + 2]), 2);
            else if (Igama_I_SMS(igama_engajikiyo, "indeksa") && Igama_I_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ukungaphumeleli_ixabiso("지원하지 않는 isiXhosa Intshukumo 알림 호출"); return;
        }
        if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>")) {
            int 종류 = 한국어화면종(umnini), 받이 = 0, 가로 = 0, 세로 = 0, 폭 = 0, 높이 = 0;
            if (종류 == 24 && Igama_I_SMS(서술상수, "(Ljava/lang/String;II)V")) {
                높이 = 빼기(1); 폭 = 빼기(1); 가로 = (umsebenzisi.화면너비() - 폭) / 2; 세로 = (umsebenzisi.화면높이() - 높이) / 2;
            } else if ((종류 == 26 || 종류 == 28) && Igama_I_SMS(서술상수, "(Ljava/lang/String;IIII)V") || 종류 == 27 && Igama_I_SMS(서술상수, "(Ljava/lang/String;IIIILisiXhosa/자체/동작받이;)V")) {
                if (종류 == 27) 받이 = 빼기(2);
                높이 = 빼기(1); 폭 = 빼기(1); 세로 = 빼기(1); 가로 = 빼기(1);
            } else { ukungaphumeleli_ixabiso("지원하지 않는 isiXhosa 화면 생성자"); return; }
            int Umbhalo = 빼기(2), ielement_ixabiso = 빼기(2); if (!화면객체(ielement_ixabiso)) return;
            if (폭 < 1 || 높이 < 1 || 가로 < 0 || 세로 < 0 || 폭 > umsebenzisi.화면너비() - 가로 || 높이 > umsebenzisi.화면높이() - 세로) { 예외던짐(27, "화면 영역을 벗어난 크기입니다"); return; }
            int indeksa = umsebenzisi.화면연결(0, 종류 - 23, 0, 0, 0, 0);
            if (indeksa < 1 || indeksa > 32) { ukungaphumeleli_ixabiso("화면 ielement_ixabiso 자리가 가득 찼습니다"); return; }
            힙[ielement_ixabiso + 2] = indeksa; 화면참조[indeksa - 1] = ielement_ixabiso;
            힙[ielement_ixabiso + 5] = 가로; 힙[ielement_ixabiso + 6] = 세로; 힙[ielement_ixabiso + 7] = 폭; 힙[ielement_ixabiso + 8] = 높이; 힙[ielement_ixabiso + 10] = 2;
            힙[ielement_ixabiso + 4] = 받이; 힙참조[ielement_ixabiso + 4] = 1; 힙[ielement_ixabiso + 12] = 1;
            umsebenzisi.화면연결(1, indeksa, 가로, 세로, 폭, 높이);
            if (종류 == 24) umsebenzisi.화면연결(7, indeksa, 2, 0, 0, 0);
            화면문자설정(ielement_ixabiso, Umbhalo); return;
        }
        if (명령코드 != 182) { ukungaphumeleli_ixabiso("잘못된 isiXhosa 화면 호출 Umyalelo"); return; }
        if (Igama_I_SMS(igama_engajikiyo, "bhala_I_SMS") && Igama_I_SMS(서술상수, "(Ljava/lang/String;)V")) {
            int Umbhalo = 빼기(2), ielement_ixabiso = 빼기(2); if (화면객체(ielement_ixabiso)) 화면문자설정(ielement_ixabiso, Umbhalo); return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "글읽기") && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) {
            int ielement_ixabiso = 빼기(2); if (화면객체(ielement_ixabiso)) 넣기(화면문자읽기(ielement_ixabiso), 2); return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "동작맡기기") && Igama_I_SMS(서술상수, "(LisiXhosa/자체/동작받이;)V")) {
            int 받이 = 빼기(2), ielement_ixabiso = 빼기(2);
            if (화면객체(ielement_ixabiso)) { 힙[ielement_ixabiso + 4] = 받이; 힙참조[ielement_ixabiso + 4] = 1; 힙[ielement_ixabiso + 12] = 1; } return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "yongeza_ielement") && Igama_I_SMS(서술상수, "(LisiXhosa/자체/화면구성요소;)V")) {
            int umntwana_ixabiso = 빼기(2), 부모 = 빼기(2); if (!화면객체(umntwana_ixabiso) || !화면객체(부모)) return;
            if (umsebenzisi.화면연결(2, 힙[부모 + 2], 힙[umntwana_ixabiso + 2], 0, 0, 0) < 0) { 예외던짐(27, "잘못된 화면 부모입니다"); return; }
            힙[umntwana_ixabiso + 11] = 부모; 힙참조[umntwana_ixabiso + 11] = 1; return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "자리정하기") && Igama_I_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 폭 = 빼기(1), 세로 = 빼기(1), 가로 = 빼기(1), ielement_ixabiso = 빼기(2); if (!화면객체(ielement_ixabiso)) return;
            if (umsebenzisi.화면연결(1, 힙[ielement_ixabiso + 2], 가로, 세로, 폭, 높이) < 0) { 예외던짐(27, "화면 영역을 벗어난 자리입니다"); return; }
            힙[ielement_ixabiso + 5] = 가로; 힙[ielement_ixabiso + 6] = 세로; 힙[ielement_ixabiso + 7] = 폭; 힙[ielement_ixabiso + 8] = 높이; return;
        }
        if ((Igama_I_SMS(igama_engajikiyo, "bonisa_i_window") || Igama_I_SMS(igama_engajikiyo, "Vala")) && Igama_I_SMS(서술상수, "()V")) {
            boolean ukubonakala_ixabiso = Igama_I_SMS(igama_engajikiyo, "bonisa_i_window"); int ielement_ixabiso = 빼기(2); if (!화면객체(ielement_ixabiso)) return;
            if (umsebenzisi.화면연결(ukubonakala_ixabiso ? 3 : 4, 힙[ielement_ixabiso + 2], ukubonakala_ixabiso ? 1 : 0, 0, 0, 0) < 0) { ukungaphumeleli_ixabiso("화면은 esebenzisana_nomsebenzi 명령에서 실행해야 합니다"); return; }
            힙[ielement_ixabiso + 9] = ukubonakala_ixabiso ? 1 : 0; return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "보이는가") && Igama_I_SMS(서술상수, "()Z")) { int ielement_ixabiso = 빼기(2); if (화면객체(ielement_ixabiso)) 넣기(힙[ielement_ixabiso + 9], 1); return; }
        ukungaphumeleli_ixabiso("지원하지 않는 isiXhosa 화면 imethodi_ixabiso");
    }
    static void 화면호출(int umnini, int igama_engajikiyo, int 서술상수, int 명령코드) {
        if (Igama_I_SMS(umnini, "javax/swing/SwingUtilities")) {
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "invokeLater") && Igama_I_SMS(서술상수, "(Ljava/lang/Runnable;)V")) { int into_Isalathiso = 빼기(2); if (!객체유효(into_Isalathiso)) return; if (나중수 == 8) { ukungaphumeleli_ixabiso("invokeLater queue full"); return; } 나중실행[나중수++] = into_Isalathiso; return; }
            if (명령코드 == 184 && Igama_I_SMS(igama_engajikiyo, "isEventDispatchThread") && Igama_I_SMS(서술상수, "()Z")) { 넣기(사건중 ? 1 : 0, 1); return; }
            ukungaphumeleli_ixabiso("unsupported SwingUtilities method"); return;
        }
        if (Igama_I_SMS(umnini, "java/awt/event/ActionEvent")) {
            int into_Isalathiso = 빼기(2); if (!into_ixabiso(into_Isalathiso, 29)) return;
            if (Igama_I_SMS(igama_engajikiyo, "getSource") && Igama_I_SMS(서술상수, "()Ljava/lang/Object;")) 넣기(힙[into_Isalathiso + 2], 2);
            else if (Igama_I_SMS(igama_engajikiyo, "getActionCommand") && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(힙[into_Isalathiso + 2]), 2);
            else if (Igama_I_SMS(igama_engajikiyo, "getID") && Igama_I_SMS(서술상수, "()I")) 넣기(1001, 1);
            else ukungaphumeleli_ixabiso("unsupported ActionEvent method"); return;
        }
        if (명령코드 == 183 && Igama_I_SMS(igama_engajikiyo, "<init>")) {
            int 열수 = 0, I_SMS_Isalathiso = 0;
            if (Igama_I_SMS(서술상수, "(I)V")) 열수 = 빼기(1);
            else if (Igama_I_SMS(서술상수, "(Ljava/lang/String;I)V")) { 열수 = 빼기(1); I_SMS_Isalathiso = 빼기(2); }
            else if (Igama_I_SMS(서술상수, "(Ljava/lang/String;)V")) I_SMS_Isalathiso = 빼기(2);
            else if (Igama_I_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) 빼기(2);
            else if (!Igama_I_SMS(서술상수, "()V")) { ukungaphumeleli_ixabiso("unsupported Swing constructor"); return; }
            int into_Isalathiso = 빼기(2); if (!객체유효(into_Isalathiso)) return;
            if (힙[into_Isalathiso] == 30) { ukungaphumeleli_ixabiso("FlowLayout is not implemented; use setLayout(null) and bounds"); return; }
            if (!화면객체(into_Isalathiso) || 열수 < 0) return;
            int isazisi_ixabiso = umsebenzisi.화면연결(0, 힙[into_Isalathiso] - 23, 0, 0, 0, 0);
            if (isazisi_ixabiso < 1 || isazisi_ixabiso > 32) { ukungaphumeleli_ixabiso("GUI widget slots exhausted"); return; }
            힙[into_Isalathiso + 2] = isazisi_ixabiso; 화면참조[isazisi_ixabiso - 1] = into_Isalathiso; 힙[into_Isalathiso + 5] = 힙[into_Isalathiso] == 24 ? 130 : 16; 힙[into_Isalathiso + 6] = 힙[into_Isalathiso] == 24 ? 110 : 16;
            힙[into_Isalathiso + 7] = 힙[into_Isalathiso] == 24 ? 380 : 220; 힙[into_Isalathiso + 8] = 힙[into_Isalathiso] == 24 ? 240 : 28; 힙[into_Isalathiso + 10] = 1;
            화면문자설정(into_Isalathiso, I_SMS_Isalathiso); return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "setText") || Igama_I_SMS(igama_engajikiyo, "setTitle")) { int I_SMS_Isalathiso = 빼기(2), into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso) && Igama_I_SMS(서술상수, "(Ljava/lang/String;)V")) 화면문자설정(into_Isalathiso, I_SMS_Isalathiso); return; }
        if (Igama_I_SMS(igama_engajikiyo, "getText") || Igama_I_SMS(igama_engajikiyo, "getTitle")) { int into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso) && Igama_I_SMS(서술상수, "()Ljava/lang/String;")) 넣기(화면문자읽기(into_Isalathiso), 2); return; }
        if (Igama_I_SMS(igama_engajikiyo, "addActionListener") && Igama_I_SMS(서술상수, "(Ljava/awt/event/ActionListener;)V")) { int 수신참조 = 빼기(2), into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) { 힙[into_Isalathiso + 4] = 수신참조; 힙참조[into_Isalathiso + 4] = 1; } return; }
        if (Igama_I_SMS(igama_engajikiyo, "getContentPane") && Igama_I_SMS(서술상수, "()Ljava/awt/Container;")) { int into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) 넣기(into_Isalathiso, 2); return; }
        if (Igama_I_SMS(igama_engajikiyo, "setLayout") && Igama_I_SMS(서술상수, "(Ljava/awt/LayoutManager;)V")) { int ubume_Isalathiso = 빼기(2), into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso) && ubume_Isalathiso != 0) ukungaphumeleli_ixabiso("only absolute layout (null) is supported"); return; }
        if (Igama_I_SMS(igama_engajikiyo, "add") && (Igama_I_SMS(서술상수, "(Ljava/awt/Component;)Ljava/awt/Component;") || Igama_I_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"))) {
            boolean ubume_imo = Igama_I_SMS(서술상수, "(Ljava/awt/Component;Ljava/lang/Object;)V"); if (ubume_imo) 빼기(2);
            int umntwana_Isalathiso = 빼기(2), into_Isalathiso = 빼기(2); if (!화면객체(umntwana_Isalathiso) || !화면객체(into_Isalathiso)) return;
            if (umsebenzisi.화면연결(2, 힙[into_Isalathiso + 2], 힙[umntwana_Isalathiso + 2], 0, 0, 0) < 0) { 예외던짐(9, "invalid GUI parent"); return; }
            힙[umntwana_Isalathiso + 11] = into_Isalathiso; 힙참조[umntwana_Isalathiso + 11] = 1; if (!ubume_imo) 넣기(umntwana_Isalathiso, 2); return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "setBounds") && Igama_I_SMS(서술상수, "(IIII)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), 세로좌표 = 빼기(1), isilungelelanisi_x = 빼기(1), into_Isalathiso = 빼기(2); if (!화면객체(into_Isalathiso)) return;
            if (umsebenzisi.화면연결(1, 힙[into_Isalathiso + 2], isilungelelanisi_x, 세로좌표, 너비, 높이) < 0) { 예외던짐(9, "GUI bounds"); return; }
            힙[into_Isalathiso + 5] = isilungelelanisi_x; 힙[into_Isalathiso + 6] = 세로좌표; 힙[into_Isalathiso + 7] = 너비; 힙[into_Isalathiso + 8] = 높이; return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "setSize") && Igama_I_SMS(서술상수, "(II)V")) {
            int 높이 = 빼기(1), 너비 = 빼기(1), into_Isalathiso = 빼기(2); if (!화면객체(into_Isalathiso)) return;
            if (umsebenzisi.화면연결(1, 힙[into_Isalathiso + 2], 힙[into_Isalathiso + 5], 힙[into_Isalathiso + 6], 너비, 높이) < 0) 예외던짐(9, "GUI size"); else { 힙[into_Isalathiso + 7] = 너비; 힙[into_Isalathiso + 8] = 높이; } return;
        }
        if (Igama_I_SMS(igama_engajikiyo, "setLocationRelativeTo") && Igama_I_SMS(서술상수, "(Ljava/awt/Component;)V")) { int 상대배치 = 빼기(2), into_Isalathiso = 빼기(2); if (!화면객체(into_Isalathiso)) return; if (상대배치 != 0) { ukungaphumeleli_ixabiso("only screen centering supported"); return; } 힙[into_Isalathiso + 5] = (umsebenzisi.화면너비() - 힙[into_Isalathiso + 7]) / 2; 힙[into_Isalathiso + 6] = (umsebenzisi.화면높이() - 힙[into_Isalathiso + 8]) / 2; umsebenzisi.화면연결(1, 힙[into_Isalathiso + 2], 힙[into_Isalathiso + 5], 힙[into_Isalathiso + 6], 힙[into_Isalathiso + 7], 힙[into_Isalathiso + 8]); return; }
        if (Igama_I_SMS(igama_engajikiyo, "setDefaultCloseOperation") && Igama_I_SMS(서술상수, "(I)V")) { int umgaqo_nkqubo = 빼기(1), into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) { if (umgaqo_nkqubo < 0 || umgaqo_nkqubo > 3) 예외던짐(9, "close policy"); else { 힙[into_Isalathiso + 10] = umgaqo_nkqubo; umsebenzisi.화면연결(7, 힙[into_Isalathiso + 2], umgaqo_nkqubo, 0, 0, 0); } } return; }
        if (Igama_I_SMS(igama_engajikiyo, "setVisible") && Igama_I_SMS(서술상수, "(Z)V")) { int iingcombolo_ixabiso = 빼기(1), into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) { int 처리값 = umsebenzisi.화면연결(3, 힙[into_Isalathiso + 2], iingcombolo_ixabiso, 0, 0, 0); if (처리값 < 0) ukungaphumeleli_ixabiso("Swing requires a standalone interactive command"); else 힙[into_Isalathiso + 9] = iingcombolo_ixabiso; } return; }
        if (Igama_I_SMS(igama_engajikiyo, "dispose") && Igama_I_SMS(서술상수, "()V")) { int into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) { umsebenzisi.화면연결(4, 힙[into_Isalathiso + 2], 0, 0, 0, 0); 힙[into_Isalathiso + 9] = 0; } return; }
        if (Igama_I_SMS(igama_engajikiyo, "repaint") || Igama_I_SMS(igama_engajikiyo, "validate")) { int into_Isalathiso = 빼기(2); if (!화면객체(into_Isalathiso) || !Igama_I_SMS(서술상수, "()V")) return; umsebenzisi.화면연결(1, 힙[into_Isalathiso + 2], 힙[into_Isalathiso + 5], 힙[into_Isalathiso + 6], 힙[into_Isalathiso + 7], 힙[into_Isalathiso + 8]); return; }
        if (Igama_I_SMS(igama_engajikiyo, "isVisible") && Igama_I_SMS(서술상수, "()Z")) { int into_Isalathiso = 빼기(2); if (화면객체(into_Isalathiso)) 넣기(힙[into_Isalathiso + 9], 1); return; }
        ukungaphumeleli_ixabiso("unsupported Swing method (native subset)");
    }
    static void 사건실행(int ithagethi_idilesi, int 사건번호, boolean isiXhosa) {
        if (ithagethi_idilesi < 1 || 힙[ithagethi_idilesi] < 32) { ukungaphumeleli_ixabiso("Java event listener required"); return; }
        int ifayile_indeksa = igama_imethodi(힙[ithagethi_idilesi] - 32, 사건번호 == 0 ? (isiXhosa ? "ukwenza_umsebenzi" : "run") : (isiXhosa ? "동작받기" : "actionPerformed"), 사건번호 == 0 ? "()V" : (isiXhosa ? "(LisiXhosa/자체/동작알림;)V" : "(Ljava/awt/event/ActionEvent;)V"));
        if (ifayile_indeksa < 0) { ukungaphumeleli_ixabiso("event callback missing"); return; }
        현재가닥 = 0; 가닥수 = 1; ifreyim_indeksa = 0; ithredi_imo[0] = 1; ifreyim_fumba[0] = 0; 틀잠금[0] = qalisa_umsebenzi_ifreyim[0] = 0; 바꿈요청 = false;
        for (int iluphu_indeksa = 0; iluphu_indeksa < 128; iluphu_indeksa++) { eyale_ndawo_ixabiso[iluphu_indeksa] = eyale_ndawo_uhlobo[iluphu_indeksa] = 0; }
        ifreyim_imethodi[0] = ifayile_indeksa; 틀위치[0] = imethodi_qala[ifayile_indeksa]; eyale_ndawo_ixabiso[0] = ithagethi_idilesi; eyale_ndawo_uhlobo[0] = 2;
        if (사건번호 != 0) { eyale_ndawo_ixabiso[1] = 사건번호; eyale_ndawo_uhlobo[1] = 2; }
        사건중 = true; ukwenza_umyalelo(); 사건중 = false;
    }
    static void 화면사건들() {
        while (!Impazamo) {
            if (나중수 > 0) { int ithagethi_idilesi = 나중실행[0], isiXhosa = 나중한국어[0]; for (int iluphu_indeksa = 1; iluphu_indeksa < 나중수; iluphu_indeksa++) { 나중실행[iluphu_indeksa - 1] = 나중실행[iluphu_indeksa]; 나중한국어[iluphu_indeksa - 1] = 나중한국어[iluphu_indeksa]; } 나중실행[--나중수] = 0; 나중한국어[나중수] = 0; 사건실행(ithagethi_idilesi, 0, isiXhosa != 0); continue; }
            if (umsebenzisi.화면연결(6, 0, 0, 0, 0, 0) == 0) return;
            int 사건번호 = umsebenzisi.화면연결(5, 0, 0, 0, 0, 0); if (사건번호 == 0) continue;
            if (사건번호 < 0) { ukungaphumeleli_ixabiso("GUI event I/O failed"); return; }
            int isazisi_ixabiso = 사건번호 & 65535; if (isazisi_ixabiso < 1 || isazisi_ixabiso > 32) continue; int into_Isalathiso = 화면참조[isazisi_ixabiso - 1]; if (into_Isalathiso == 0) continue;
            if ((사건번호 & 65536) != 0) {
                if (힙[into_Isalathiso + 10] != 0) 힙[into_Isalathiso + 9] = 0;
                if (힙[into_Isalathiso + 10] == 3) for (int iluphu_indeksa = 0; iluphu_indeksa < 32; iluphu_indeksa++) if (화면참조[iluphu_indeksa] != 0 && 힙[화면참조[iluphu_indeksa]] == 24) umsebenzisi.화면연결(4, iluphu_indeksa + 1, 0, 0, 0, 0);
            } else if (힙[into_Isalathiso + 4] != 0) {
                int i_README_Isalathiso = yabela_Ugcino(29, 2); if (Impazamo) return; 힙[i_README_Isalathiso + 2] = into_Isalathiso; 힙[i_README_Isalathiso + 3] = 힙[into_Isalathiso + 12]; 힙참조[i_README_Isalathiso + 2] = 1; 사건실행(힙[into_Isalathiso + 4], i_README_Isalathiso, 힙[into_Isalathiso + 12] != 0);
            }
        }
    }
    public static int Phumeza() {
        if (umsebenzisi.인수개수() == 1 && 자바도구.같음(umsebenzisi.인수(0), "-version")) {
            umsebenzisi.Bhala("jkoros JVM 0.4 (class/JAR subset; IPv4 TCP/UDP; not OpenJDK)\n"); return 0;
        }
        if (umsebenzisi.인수개수() < 1) { umsebenzisi.Bhala("Usage: java CLASS [ARGS]\n"); return 2; }
        ufako_nkcukacha_iklasi_Ingcaciso = layisha_iklasi_Ingcaciso(umsingathi_ikharakhtha(umsebenzisi.인수(0))); if (Impazamo || ufako_nkcukacha_iklasi_Ingcaciso < 0) return 1;
        int ufako_nkcukacha_inqaku_ixabiso = igama_imethodi(ufako_nkcukacha_iklasi_Ingcaciso, "Phumeza", "()V");
        boolean 한국어진입 = ufako_nkcukacha_inqaku_ixabiso >= 0 && (imethodi_fikelela[ufako_nkcukacha_inqaku_ixabiso] & 9) == 9;
        if (!한국어진입) ufako_nkcukacha_inqaku_ixabiso = igama_imethodi(ufako_nkcukacha_iklasi_Ingcaciso, "main", "([Ljava/lang/String;)V");
        if (ufako_nkcukacha_inqaku_ixabiso < 0 || (imethodi_fikelela[ufako_nkcukacha_inqaku_ixabiso] & 9) != 9) ukungaphumeleli_ixabiso("public static void Phumeza() or main(String[] args) required");
        if (Impazamo) return 1;
        int 인수 = yabela_Ugcino(3, umsebenzisi.인수개수() - 1); ULUHLU_ielement[인수] = -1;
        for (int 수 = 1; 수 < umsebenzisi.인수개수() && !Impazamo; 수++) 힙[인수 + 1 + 수] = umsingathi_ikharakhtha(umsebenzisi.인수(수));
        ifreyim_indeksa = 0; ifreyim_imethodi[0] = ufako_nkcukacha_inqaku_ixabiso; 틀위치[0] = imethodi_qala[ufako_nkcukacha_inqaku_ixabiso]; eyale_ndawo_ixabiso[0] = 한국어진입 ? 0 : 인수; eyale_ndawo_uhlobo[0] = 한국어진입 ? 0 : 2;
        ithredi_imo[0] = 1; ithredi_into[0] = yabela_Ugcino(13, 2);
        ukwenza_umyalelo(); if (!Impazamo) 화면사건들(); return Impazamo ? 1 : 0;
    }
}
