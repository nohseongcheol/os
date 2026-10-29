// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 istifadəçi göstərici/길이는 müraciət_daxiletmə 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_uzunluq(int ünvan) {
        if (!실행관리.klip(ünvan, 4)) return -14;
        int uzunluq_VALUE = 실행관리.수(ünvan);
        if (uzunluq_VALUE < 0 || uzunluq_VALUE > (실행관리.istifadəçi_bitirmək - ünvan - 4) / 4) return -14;
        return uzunluq_VALUE;
    }

    public static int Proses_VALUE_daxiletmə(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.açmaq_fayl(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.yazmaq_fayl(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.bağlamaq_fayl(가);
        if (INDEX == 34) return 파일서술자관리.axtarmaq_fayl(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.silmək_fayl_daxiletmə_ad(가);
        if (INDEX == 39) return 파일서술자관리.Dəst_fayl_uzunluq(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_ünvan(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinxronlaşdırmaq();
        }
        if (INDEX == 1) {
            int uzunluq_VALUE = ARRAY_uzunluq(가);
            if (uzunluq_VALUE < 0) return uzunluq_VALUE;
            if (uzunluq_VALUE > 4096) return -90;
            for (int simvol_VALUE_068c2631 = 0; simvol_VALUE_068c2631 < uzunluq_VALUE; simvol_VALUE_068c2631++) SMS_Terminal.문자(실행관리.수(가 + 4 + simvol_VALUE_068c2631 * 4) & 65535);
            return uzunluq_VALUE;
        }
        if (INDEX == 2) return 실행관리.arqument_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.arqument_COUNT ? 실행관리.arqument_ünvan[가] : 0;
        if (INDEX == 10) return Şəbəkə_Yığın.Aç(가);
        if (INDEX == 11) {
            int uzunluq_VALUE = ARRAY_uzunluq(라);
            if (uzunluq_VALUE < 0) return uzunluq_VALUE;
            if (마 < 0 || 마 > uzunluq_VALUE || 마 > 1024) return -90;
            for (int yerinə_qoymaq = 0; yerinə_qoymaq < 마; yerinə_qoymaq++) 임시자료[yerinə_qoymaq] = 실행관리.수(라 + 4 + yerinə_qoymaq * 4) & 255;
            return Şəbəkə_Yığın.göndərmək(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int uzunluq_VALUE = ARRAY_uzunluq(나);
            if (uzunluq_VALUE < 0) return uzunluq_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int ölçü = Şəbəkə_Yığın.받기(가, 임시자료, uzunluq_VALUE < 1024 ? uzunluq_VALUE : 1024, 다);
            if (ölçü >= 0) for (int yerinə_qoymaq = 0; yerinə_qoymaq < ölçü; yerinə_qoymaq++) 실행관리.수쓰기(나 + 4 + yerinə_qoymaq * 4, 임시자료[yerinə_qoymaq]);
            return ölçü;
        }
        if (INDEX == 13) return Şəbəkə_Yığın.Bağla(가);
        if (INDEX == 14) return Şəbəkə_Yığın.내주소;
        if (INDEX == 15) return Şəbəkə_Yığın.eynisəviyyəli_ünvan(가);
        if (INDEX == 16) return Şəbəkə_Yığın.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int ad_ölçünü_dəyişmək = ARRAY_uzunluq(가), verilənlər_ölçünü_dəyişmək = ARRAY_uzunluq(나);
            if (ad_ölçünü_dəyişmək < 0 || verilənlər_ölçünü_dəyişmək < 0) return -14;
            if (ad_ölçünü_dəyişmək < 1 || ad_ölçünü_dəyişmək > 64) return -22;
            int uzunluq_VALUE = 0;
            while (uzunluq_VALUE < ad_ölçünü_dəyişmək && 실행관리.수(가 + 4 + uzunluq_VALUE * 4) != 0) {
                Yaddaş_fayl_sistemi.Ad[uzunluq_VALUE] = 실행관리.수(가 + 4 + uzunluq_VALUE * 4);
                uzunluq_VALUE++;
            }
            if (!Yaddaş_fayl_sistemi.çek_ad(Yaddaş_fayl_sistemi.Ad, uzunluq_VALUE)) return -22;
            if (INDEX == 20) {
                int FAYL = Yaddaş_fayl_sistemi.FIND_daxiletmə(Yaddaş_fayl_sistemi.Ad, uzunluq_VALUE);
                if (FAYL < 0) return FAYL;
                int Böyüklük = Yaddaş_fayl_sistemi.ölçünü_dəyişmək_Siyahı[FAYL];
                if (Böyüklük > verilənlər_ölçünü_dəyişmək) return -90;
                int ünvan = cihaz_VALUE.fayl_Yaddaş() + FAYL * Yaddaş_fayl_sistemi.최대크기;
                for (int 수 = 0; 수 < Böyüklük; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, cihaz_VALUE.기억읽기(ünvan + 수));
                return Böyüklük;
            }
            if (다 < 0 || 다 > verilənlər_ölçünü_dəyişmək) return -22;
            if (다 > Yaddaş_fayl_sistemi.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Yaddaş_fayl_sistemi.redaktə_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Yaddaş_fayl_sistemi.Store_VALUE(Yaddaş_fayl_sistemi.Ad, uzunluq_VALUE, Yaddaş_fayl_sistemi.redaktə_VALUE, 다);
        }
        return -38;
    }
}
