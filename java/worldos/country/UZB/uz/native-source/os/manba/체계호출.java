// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 foydalanuvchi kursor/길이는 kirish_huquqi_kiritish 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_uzunlik(int manzil) {
        if (!실행관리.klip(manzil, 4)) return -14;
        int uzunlik_VALUE = 실행관리.수(manzil);
        if (uzunlik_VALUE < 0 || uzunlik_VALUE > (실행관리.foydalanuvchi_to_xtatmoq - manzil - 4) / 4) return -14;
        return uzunlik_VALUE;
    }

    public static int Jarayon_VALUE_kiritish(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.ochmoq_fayl(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.yozmoq_fayl(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.yopmoq_fayl(가);
        if (INDEX == 34) return 파일서술자관리.izlamoq_fayl(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.olib_tashlamoq_fayl_kiritish_nom(가);
        if (INDEX == 39) return 파일서술자관리.to_plam_fayl_uzunlik(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BOG_LAMOQ_manzil(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.sinxronlashtirish();
        }
        if (INDEX == 1) {
            int uzunlik_VALUE = ARRAY_uzunlik(가);
            if (uzunlik_VALUE < 0) return uzunlik_VALUE;
            if (uzunlik_VALUE > 4096) return -90;
            for (int belgi_VALUE = 0; belgi_VALUE < uzunlik_VALUE; belgi_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + belgi_VALUE * 4) & 65535);
            return uzunlik_VALUE;
        }
        if (INDEX == 2) return 실행관리.dalil_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.dalil_COUNT ? 실행관리.dalil_manzil[가] : 0;
        if (INDEX == 10) return Tarmoq_Stack.Ochish(가);
        if (INDEX == 11) {
            int uzunlik_VALUE = ARRAY_uzunlik(라);
            if (uzunlik_VALUE < 0) return uzunlik_VALUE;
            if (마 < 0 || 마 > uzunlik_VALUE || 마 > 1024) return -90;
            for (int Holati = 0; Holati < 마; Holati++) 임시자료[Holati] = 실행관리.수(라 + 4 + Holati * 4) & 255;
            return Tarmoq_Stack.yuborish(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int uzunlik_VALUE = ARRAY_uzunlik(나);
            if (uzunlik_VALUE < 0) return uzunlik_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int o_lchov = Tarmoq_Stack.받기(가, 임시자료, uzunlik_VALUE < 1024 ? uzunlik_VALUE : 1024, 다);
            if (o_lchov >= 0) for (int Holati = 0; Holati < o_lchov; Holati++) 실행관리.수쓰기(나 + 4 + Holati * 4, 임시자료[Holati]);
            return o_lchov;
        }
        if (INDEX == 13) return Tarmoq_Stack.Yopish(가);
        if (INDEX == 14) return Tarmoq_Stack.내주소;
        if (INDEX == 15) return Tarmoq_Stack.bir_rangli_manzil(가);
        if (INDEX == 16) return Tarmoq_Stack.상대접속번호(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int nom_o_lcham = ARRAY_uzunlik(가), ma_lumotlar_o_lcham = ARRAY_uzunlik(나);
            if (nom_o_lcham < 0 || ma_lumotlar_o_lcham < 0) return -14;
            if (nom_o_lcham < 1 || nom_o_lcham > 64) return -22;
            int uzunlik_VALUE = 0;
            while (uzunlik_VALUE < nom_o_lcham && 실행관리.수(가 + 4 + uzunlik_VALUE * 4) != 0) {
                Xotira_fayllar_tizimi.Nomi[uzunlik_VALUE] = 실행관리.수(가 + 4 + uzunlik_VALUE * 4);
                uzunlik_VALUE++;
            }
            if (!Xotira_fayllar_tizimi.chek_nom(Xotira_fayllar_tizimi.Nomi, uzunlik_VALUE)) return -22;
            if (INDEX == 20) {
                int Fayl = Xotira_fayllar_tizimi.FIND_kiritish(Xotira_fayllar_tizimi.Nomi, uzunlik_VALUE);
                if (Fayl < 0) return Fayl;
                int Hajmi = Xotira_fayllar_tizimi.o_lcham_Ro_yxat[Fayl];
                if (Hajmi > ma_lumotlar_o_lcham) return -90;
                int manzil = qurilma_VALUE.fayl_Xotira() + Fayl * Xotira_fayllar_tizimi.최대크기;
                for (int 수 = 0; 수 < Hajmi; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, qurilma_VALUE.기억읽기(manzil + 수));
                return Hajmi;
            }
            if (다 < 0 || 다 > ma_lumotlar_o_lcham) return -22;
            if (다 > Xotira_fayllar_tizimi.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Xotira_fayllar_tizimi.tahrirlamoq_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Xotira_fayllar_tizimi.Store_VALUE(Xotira_fayllar_tizimi.Nomi, uzunlik_VALUE, Xotira_fayllar_tizimi.tahrirlamoq_VALUE, 다);
        }
        return -38;
    }
}
