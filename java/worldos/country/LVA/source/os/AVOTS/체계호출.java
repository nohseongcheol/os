// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 lietotājs rādītājs/길이는 piekļūt_ievade 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int 배열길이(int adrese) {
        if (!실행관리.klips(adrese, 4)) return -14;
        int 길이 = 실행관리.numurs(adrese);
        if (길이 < 0 || 길이 > (실행관리.lietotājs_beigt_zvanu - adrese - 4) / 4) return -14;
        return 길이;
    }

    public static int Process_VALUE_ievade(int INDEX, int 가, int SECOND_operands, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.atvērt_Fails(가, SECOND_operands, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, SECOND_operands, 다);
        if (INDEX == 32) return 파일서술자관리.rakstīšana_Fails(가, SECOND_operands, 다);
        if (INDEX == 33) return 파일서술자관리.Aizvērt_Fails(가);
        if (INDEX == 34) return 파일서술자관리.meklēt_Fails(가, SECOND_operands, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, SECOND_operands, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, SECOND_operands);
        if (INDEX == 38) return 파일서술자관리.noņemt_Fails_ievade_nosaukums(가);
        if (INDEX == 39) return 파일서술자관리.파일길이정하기(가, SECOND_operands);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, SECOND_operands, 다);
        if (INDEX == 41) return 파일서술자관리.atvērt_dalībnieks(가, SECOND_operands, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_adrese(가, SECOND_operands, 다);
        if (INDEX == 43) return 파일서술자관리.sūtīt_datogramma_dati(가, SECOND_operands, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.saņemt_datogramma_dati(가, SECOND_operands, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, SECOND_operands, 다);
        if (INDEX == 46) return 파일서술자관리.kopa_saņemt_NOILGUMS(가, SECOND_operands);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinhronizēt();
        }
        if (INDEX == 1) {
            int 길이 = 배열길이(가);
            if (길이 < 0) return 길이;
            if (길이 > 4096) return -90;
            for (int rakstzīme_VALUE = 0; rakstzīme_VALUE < 길이; rakstzīme_VALUE++) SMS_Terminālis.문자(실행관리.numurs(가 + 4 + rakstzīme_VALUE * 4) & 65535);
            return 길이;
        }
        if (INDEX == 2) return 실행관리.arg_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.arg_COUNT ? 실행관리.arg_adrese[가] : 0;
        if (INDEX == 10) return tīkls_kopa.Atvērt(가);
        if (INDEX == 11) {
            int 길이 = 배열길이(라);
            if (길이 < 0) return 길이;
            if (마 < 0 || 마 > 길이 || 마 > 1024) return -90;
            for (int Novietojums = 0; Novietojums < 마; Novietojums++) 임시자료[Novietojums] = 실행관리.numurs(라 + 4 + Novietojums * 4) & 255;
            return tīkls_kopa.sūtīt(가, SECOND_operands, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int 길이 = 배열길이(SECOND_operands);
            if (길이 < 0) return 길이;
            if (다 < 0 || 다 > 2000) return -22;
            int mērs = tīkls_kopa.saņemt(가, 임시자료, 길이 < 1024 ? 길이 : 1024, 다);
            if (mērs >= 0) for (int Novietojums = 0; Novietojums < mērs; Novietojums++) 실행관리.rakstīšana_numurs(SECOND_operands + 4 + Novietojums * 4, 임시자료[Novietojums]);
            return mērs;
        }
        if (INDEX == 13) return tīkls_kopa.Aizvērt(가);
        if (INDEX == 14) return tīkls_kopa.내주소;
        if (INDEX == 15) return tīkls_kopa.vienranga_adrese(가);
        if (INDEX == 16) return tīkls_kopa.vienranga_porta_numurs(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminālis.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nosaukums_mainīt_izmērus = 배열길이(가), dati_mainīt_izmērus = 배열길이(SECOND_operands);
            if (nosaukums_mainīt_izmērus < 0 || dati_mainīt_izmērus < 0) return -14;
            if (nosaukums_mainīt_izmērus < 1 || nosaukums_mainīt_izmērus > 64) return -22;
            int 길이 = 0;
            while (길이 < nosaukums_mainīt_izmērus && 실행관리.numurs(가 + 4 + 길이 * 4) != 0) {
                atmiņa_failu_sistēma.Nosaukums[길이] = 실행관리.numurs(가 + 4 + 길이 * 4);
                길이++;
            }
            if (!atmiņa_failu_sistēma.čeks_nosaukums(atmiņa_failu_sistēma.Nosaukums, 길이)) return -22;
            if (INDEX == 20) {
                int Fails = atmiņa_failu_sistēma.FIND_ievade(atmiņa_failu_sistēma.Nosaukums, 길이);
                if (Fails < 0) return Fails;
                int Izmērs = atmiņa_failu_sistēma.mainīt_izmērus_Saraksts[Fails];
                if (Izmērs > dati_mainīt_izmērus) return -90;
                int adrese = ierīce_VALUE.Fails_atmiņa() + Fails * atmiņa_failu_sistēma.최대크기;
                for (int numurs = 0; numurs < Izmērs; numurs++) 실행관리.rakstīšana_numurs(SECOND_operands + 4 + numurs * 4, ierīce_VALUE.기억읽기(adrese + numurs));
                return Izmērs;
            }
            if (다 < 0 || 다 > dati_mainīt_izmērus) return -22;
            if (다 > atmiņa_failu_sistēma.최대크기) return -90;
            for (int numurs = 0; numurs < 다; numurs++) atmiņa_failu_sistēma.Rediģēt_VALUE[numurs] = 실행관리.numurs(SECOND_operands + 4 + numurs * 4) & 255;
            return atmiņa_failu_sistēma.Store_VALUE(atmiņa_failu_sistēma.Nosaukums, 길이, atmiņa_failu_sistēma.Rediģēt_VALUE, 다);
        }
        return -38;
    }
}
