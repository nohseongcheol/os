// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Tarmoq_Stack {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Tarmoq_niqob = 0xffffff00; /* ip.conf:NETMASK */
    static final int shluz_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_uzunlik = new int[4], RECEIVED_manzil = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_ma_lumotlar = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int butun_son_16(int[] kadr_INDEX, int Holati) { return (kadr_INDEX[Holati] << 8) | kadr_INDEX[Holati + 1]; }
    static int butun_son_32(int[] kadr_INDEX, int Holati) { return (butun_son_16(kadr_INDEX, Holati) << 16) | butun_son_16(kadr_INDEX, Holati + 2); }
    static void 넣기16(int[] kadr_INDEX, int Holati, int VALUE) { kadr_INDEX[Holati] = (VALUE >>> 8) & 255; kadr_INDEX[Holati + 1] = VALUE & 255; }
    static void 넣기32(int[] kadr_INDEX, int Holati, int VALUE) { 넣기16(kadr_INDEX, Holati, VALUE >>> 16); 넣기16(kadr_INDEX, Holati + 2, VALUE); }
    static int SUM_VALUE(int[] kadr_INDEX, int Bajarish, int uzunlik_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX += 2)
            VALUE += (kadr_INDEX[Bajarish + INDEX] << 8) | (INDEX + 1 < uzunlik_VALUE ? kadr_INDEX[Bajarish + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int uzunlik_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + uzunlik_VALUE;
    }

    static void Toza_Jarayon() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_uzunlik[INDEX] = -1; RECEIVED_manzil[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Tarmoq_drayver.받기(입력틀) == 0) break;
    }
    static int INDEX(int deskriptor_VALUE) { return deskriptor_VALUE >= 3 && deskriptor_VALUE < 7 && 접속번호들[deskriptor_VALUE - 3] != 0 ? deskriptor_VALUE - 3 : -1; }
    static int Ochish(int 접속번호) {
        if (Tarmoq_drayver.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 접속번호) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int old_kamera_VALUE = 0; old_kamera_VALUE < 4; old_kamera_VALUE++) if (접속번호들[old_kamera_VALUE] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[INDEX] = 접속번호; RECEIVED_uzunlik[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Yopish(int deskriptor_VALUE) {
        int in_kiritish = INDEX(deskriptor_VALUE);
        if (in_kiritish < 0) return -9;
        접속번호들[in_kiritish] = 0; RECEIVED_uzunlik[in_kiritish] = -1;
        return 0;
    }
    static int bir_rangli_manzil(int deskriptor_VALUE) { int in_kiritish = INDEX(deskriptor_VALUE); return in_kiritish < 0 ? -9 : RECEIVED_manzil[in_kiritish]; }
    static int 상대접속번호(int deskriptor_VALUE) { int in_kiritish = INDEX(deskriptor_VALUE); return in_kiritish < 0 ? -9 : 받은접속번호[in_kiritish]; }

    static void 바깥머리(int 종류, boolean translyatsiya_qilish_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = translyatsiya_qilish_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Tarmoq_drayver.qurilma_manzil[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int ko_chirish_joyi_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Tarmoq_drayver.qurilma_manzil[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, ko_chirish_joyi_VALUE);
        Tarmoq_drayver.yuborish(출력틀, 42);
    }
    static void Jarayon_manzil(int uzunlik_VALUE) {
        if (uzunlik_VALUE < 42 || butun_son_16(입력틀, 14) != 1 || butun_son_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || butun_son_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = butun_son_16(입력틀, 20), bir_rangli_VALUE = butun_son_32(입력틀, 28);
        if (종류 == 2 && bir_rangli_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Tarmoq_drayver.qurilma_manzil[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = bir_rangli_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Tarmoq_drayver.qurilma_manzil[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, bir_rangli_VALUE);
            Tarmoq_drayver.yuborish(출력틀, 42);
        }
    }

    static void Jarayon_kadr(int uzunlik_VALUE) {
        if (uzunlik_VALUE < 14 || uzunlik_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, translyatsiya_qilish_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Tarmoq_drayver.qurilma_manzil[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) translyatsiya_qilish_VALUE = false;
        }
        if (!자기 && !translyatsiya_qilish_VALUE) return;
        if (butun_son_16(입력틀, 12) == 0x0806) { Jarayon_manzil(uzunlik_VALUE); return; }
        if (butun_son_16(입력틀, 12) != 0x0800) return;
        if (uzunlik_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Sarlavha_uzunlik = (입력틀[14] & 15) * 4, 전체길이 = butun_son_16(입력틀, 16);
        if (Sarlavha_uzunlik < 20 || Sarlavha_uzunlik > 60 || 전체길이 < Sarlavha_uzunlik + 8 || 전체길이 > uzunlik_VALUE - 14
            || (butun_son_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || butun_son_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Sarlavha_uzunlik, 0) != 65535) { 폐기수++; return; }
        int Bajarish = 14 + Sarlavha_uzunlik, ma_lumotlar_uzunlik = butun_son_16(입력틀, Bajarish + 4);
        if (ma_lumotlar_uzunlik < 8 || ma_lumotlar_uzunlik != 전체길이 - Sarlavha_uzunlik || ma_lumotlar_uzunlik > 1032) { 폐기수++; return; }
        int 출발 = butun_son_32(입력틀, 26);
        if (butun_son_16(입력틀, Bajarish + 6) != 0 && SUM_VALUE(입력틀, Bajarish, ma_lumotlar_uzunlik, 가상머리합(출발, 내주소, ma_lumotlar_uzunlik)) != 65535) {
            폐기수++; return;
        }
        int ko_chirish_joyi_VALUE = butun_son_16(입력틀, Bajarish + 2);
        for (int in_kiritish = 0; in_kiritish < 4; in_kiritish++) if (접속번호들[in_kiritish] != 0 && 접속번호들[in_kiritish] == ko_chirish_joyi_VALUE) {
            if (RECEIVED_uzunlik[in_kiritish] >= 0) { 폐기수++; return; }
            RECEIVED_uzunlik[in_kiritish] = ma_lumotlar_uzunlik - 8; RECEIVED_manzil[in_kiritish] = 출발; 받은접속번호[in_kiritish] = butun_son_16(입력틀, Bajarish);
            for (int INDEX = 0; INDEX < ma_lumotlar_uzunlik - 8; INDEX++) RECEIVED_ma_lumotlar[in_kiritish * 1024 + INDEX] = 입력틀[Bajarish + 8 + INDEX];
            return;
        }
    }

    static void tasdiqlamoq() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int uzunlik_VALUE = Tarmoq_drayver.받기(입력틀);
            if (uzunlik_VALUE == 0) return;
            Jarayon_kadr(uzunlik_VALUE);
        }
    }
    static int FIND_manzil(int manzil) {
        if (manzil == 0 || manzil == -1 || (manzil >>> 28) >= 14 || (manzil >>> 24) == 127 || manzil == 내주소) return -101;
        int Keyingi_element = (manzil & Tarmoq_niqob) == (내주소 & Tarmoq_niqob) ? manzil : shluz_VALUE;
        if (Keyingi_element == 찾은주소) return 0;
        찾을주소 = Keyingi_element;
        int Bajarish = qurilma_VALUE.밀리초(), 다음요청 = Bajarish;
        while (qurilma_VALUE.밀리초() - Bajarish < 1000) {
            if (qurilma_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Keyingi_element); 다음요청 += 300; }
            tasdiqlamoq();
            if (찾은주소 == Keyingi_element) return 0;
            qurilma_VALUE.잠시양보();
        }
        return -110;
    }
    static int yuborish(int deskriptor_VALUE, int manzil, int 접속번호, int[] ma_lumotlar, int uzunlik_VALUE) {
        int in_kiritish = INDEX(deskriptor_VALUE);
        if (in_kiritish < 0) return -9;
        if (Tarmoq_drayver.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || uzunlik_VALUE < 0 || uzunlik_VALUE > 1024) return -22;
        int o_lchov = FIND_manzil(manzil);
        if (o_lchov < 0) return o_lchov;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + uzunlik_VALUE);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, manzil);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[in_kiritish]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, uzunlik_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) 출력틀[42 + INDEX] = ma_lumotlar[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, uzunlik_VALUE + 8, 가상머리합(내주소, manzil, uzunlik_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        o_lchov = Tarmoq_drayver.yuborish(출력틀, uzunlik_VALUE + 42);
        return o_lchov < 0 ? o_lchov : uzunlik_VALUE;
    }
    static int 받기(int deskriptor_VALUE, int[] ma_lumotlar, int 용량, int 제한) {
        int in_kiritish = INDEX(deskriptor_VALUE);
        if (in_kiritish < 0) return -9;
        int Bajarish = qurilma_VALUE.밀리초();
        while (true) {
            tasdiqlamoq();
            int uzunlik_VALUE = RECEIVED_uzunlik[in_kiritish];
            if (uzunlik_VALUE >= 0) {
                RECEIVED_uzunlik[in_kiritish] = -1;
                if (uzunlik_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < uzunlik_VALUE; INDEX++) ma_lumotlar[INDEX] = RECEIVED_ma_lumotlar[in_kiritish * 1024 + INDEX];
                return uzunlik_VALUE;
            }
            if (제한 == 0) return -11;
            if (qurilma_VALUE.밀리초() - Bajarish >= 제한) return -110;
            qurilma_VALUE.잠시양보();
        }
    }
    static void holat_VALUE_e10195a1() {
        SMS_Terminal.Yozish(Tarmoq_drayver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Yozish("TX: "); SMS_Terminal.수쓰기(Tarmoq_drayver.송신수);
        SMS_Terminal.Yozish(" RX: "); SMS_Terminal.수쓰기(Tarmoq_drayver.수신수);
        SMS_Terminal.Yozish(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Yozish("\n");
    }
}
