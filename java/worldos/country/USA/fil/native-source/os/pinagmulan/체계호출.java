// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** int 0x80 게이트가 호출한다. 모든 gumagamit pointer/길이는 access_pagpasok 전에 검사한다. */
public final class 체계호출 {
    static int[] 임시자료 = new int[1024];

    static int ARRAY_haba(int email) {
        if (!실행관리.clip(email, 4)) return -14;
        int haba_VALUE = 실행관리.수(email);
        if (haba_VALUE < 0 || haba_VALUE > (실행관리.gumagamit_tapusin - email - 4) / 4) return -14;
        return haba_VALUE;
    }

    public static int Proseso_VALUE_pagpasok(int INDEX, int 가, int 나, int 다, int 라, int 마) {
        if (INDEX == 30) return 파일서술자관리.buksan_file(가, 나, 다);
        if (INDEX == 31) return 파일서술자관리.파일읽기(가, 나, 다);
        if (INDEX == 32) return 파일서술자관리.sumulat_file(가, 나, 다);
        if (INDEX == 33) return 파일서술자관리.isara_file(가);
        if (INDEX == 34) return 파일서술자관리.i_seek_file(가, 나, 다);
        if (INDEX == 35) return 파일서술자관리.서술자복제(가, 0, false, 0);
        if (INDEX == 36) return 파일서술자관리.서술자복제(가, 나, true, 0);
        if (INDEX == 37) return 파일서술자관리.파일상태읽기(가, 나);
        if (INDEX == 38) return 파일서술자관리.tanggalin_file_pagpasok_pangalan(가);
        if (INDEX == 39) return 파일서술자관리.set_file_haba(가, 나);
        if (INDEX == 40) return 파일서술자관리.서술자제어(가, 나, 다);
        if (INDEX == 41) return 파일서술자관리.통신종단점만들기(가, 나, 다);
        if (INDEX == 42) return 파일서술자관리.BIND_email(가, 나, 다);
        if (INDEX == 43) return 파일서술자관리.자료전문보내기(가, 나, 다, 라, 마);
        if (INDEX == 44) return 파일서술자관리.자료전문받기(가, 나, 다, 라, 마);
        if (INDEX == 45) return 파일서술자관리.통신주소읽기(가, 나, 다);
        if (INDEX == 46) return 파일서술자관리.수신대기정하기(가, 나);
        if (INDEX == 47) {
            int 기술 = 파일서술자관리.기술찾기(가);
            if (기술 < 0) return -9;
            if (파일서술자관리.종류[기술] != 2) return -22;
            return 파일보존.iakma();
        }
        if (INDEX == 1) {
            int haba_VALUE = ARRAY_haba(가);
            if (haba_VALUE < 0) return haba_VALUE;
            if (haba_VALUE > 4096) return -90;
            for (int karakter_VALUE = 0; karakter_VALUE < haba_VALUE; karakter_VALUE++) SMS_Terminal.문자(실행관리.수(가 + 4 + karakter_VALUE * 4) & 65535);
            return haba_VALUE;
        }
        if (INDEX == 2) return 실행관리.argumento_COUNT;
        if (INDEX == 3) return 가 >= 0 && 가 < 실행관리.argumento_COUNT ? 실행관리.argumento_email[가] : 0;
        if (INDEX == 10) return Network_Stack.buksan(가);
        if (INDEX == 11) {
            int haba_VALUE = ARRAY_haba(라);
            if (haba_VALUE < 0) return haba_VALUE;
            if (마 < 0 || 마 > haba_VALUE || 마 > 1024) return -90;
            for (int posisyon = 0; posisyon < 마; posisyon++) 임시자료[posisyon] = 실행관리.수(라 + 4 + posisyon * 4) & 255;
            return Network_Stack.i_email(가, 나, 다, 임시자료, 마);
        }
        if (INDEX == 12) {
            int haba_VALUE = ARRAY_haba(나);
            if (haba_VALUE < 0) return haba_VALUE;
            if (다 < 0 || 다 > 2000) return -22;
            int sukat = Network_Stack.받기(가, 임시자료, haba_VALUE < 1024 ? haba_VALUE : 1024, 다);
            if (sukat >= 0) for (int posisyon = 0; posisyon < sukat; posisyon++) 실행관리.수쓰기(나 + 4 + posisyon * 4, 임시자료[posisyon]);
            return sukat;
        }
        if (INDEX == 13) return Network_Stack.isara(가);
        if (INDEX == 14) return Network_Stack.내주소;
        if (INDEX == 15) return Network_Stack.peer_email(가);
        if (INDEX == 16) return Network_Stack.peer_numero_ng_port(가);
        if (INDEX == 22) {
            if (가 < 0 || 가 > 65535) return -22;
            SMS_Terminal.문자(가); return 1;
        }
        if (INDEX == 20 || INDEX == 21) {
            int pangalan_sukat = ARRAY_haba(가), data_sukat = ARRAY_haba(나);
            if (pangalan_sukat < 0 || data_sukat < 0) return -14;
            if (pangalan_sukat < 1 || pangalan_sukat > 64) return -22;
            int haba_VALUE = 0;
            while (haba_VALUE < pangalan_sukat && 실행관리.수(가 + 4 + haba_VALUE * 4) != 0) {
                Memory_sistema_ng_file.pangalan[haba_VALUE] = 실행관리.수(가 + 4 + haba_VALUE * 4);
                haba_VALUE++;
            }
            if (!Memory_sistema_ng_file.tseke_pangalan(Memory_sistema_ng_file.pangalan, haba_VALUE)) return -22;
            if (INDEX == 20) {
                int file = Memory_sistema_ng_file.FIND_pagpasok(Memory_sistema_ng_file.pangalan, haba_VALUE);
                if (file < 0) return file;
                int sukat_82232621 = Memory_sistema_ng_file.sukat_list[file];
                if (sukat_82232621 > data_sukat) return -90;
                int email = device_VALUE.file_Memory() + file * Memory_sistema_ng_file.최대크기;
                for (int 수 = 0; 수 < sukat_82232621; 수++) 실행관리.수쓰기(나 + 4 + 수 * 4, device_VALUE.기억읽기(email + 수));
                return sukat_82232621;
            }
            if (다 < 0 || 다 > data_sukat) return -22;
            if (다 > Memory_sistema_ng_file.최대크기) return -90;
            for (int 수 = 0; 수 < 다; 수++) Memory_sistema_ng_file.edit_VALUE[수] = 실행관리.수(나 + 4 + 수 * 4) & 255;
            return Memory_sistema_ng_file.Store_VALUE(Memory_sistema_ng_file.pangalan, haba_VALUE, Memory_sistema_ng_file.edit_VALUE, 다);
        }
        return -38;
    }
}
