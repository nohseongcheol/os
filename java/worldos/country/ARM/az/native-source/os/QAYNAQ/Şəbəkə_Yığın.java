// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Şəbəkə_Yığın {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Şəbəkə_maska = 0xffffff00; /* ip.conf:NETMASK */
    static final int şlüz_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_uzunluq = new int[4], RECEIVED_ünvan = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_verilənlər = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, identifikator_VALUE = 0, 폐기수 = 0;

    static int tam_ədəd_16(int[] kadr_INDEX, int yerinə_qoymaq) { return (kadr_INDEX[yerinə_qoymaq] << 8) | kadr_INDEX[yerinə_qoymaq + 1]; }
    static int tam_ədəd_32(int[] kadr_INDEX, int yerinə_qoymaq) { return (tam_ədəd_16(kadr_INDEX, yerinə_qoymaq) << 16) | tam_ədəd_16(kadr_INDEX, yerinə_qoymaq + 2); }
    static void 넣기16(int[] kadr_INDEX, int yerinə_qoymaq, int VALUE) { kadr_INDEX[yerinə_qoymaq] = (VALUE >>> 8) & 255; kadr_INDEX[yerinə_qoymaq + 1] = VALUE & 255; }
    static void 넣기32(int[] kadr_INDEX, int yerinə_qoymaq, int VALUE) { 넣기16(kadr_INDEX, yerinə_qoymaq, VALUE >>> 16); 넣기16(kadr_INDEX, yerinə_qoymaq + 2, VALUE); }
    static int SUM_VALUE(int[] kadr_INDEX, int İcra_Et, int uzunluq_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX += 2)
            VALUE += (kadr_INDEX[İcra_Et + INDEX] << 8) | (INDEX + 1 < uzunluq_VALUE ? kadr_INDEX[İcra_Et + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int uzunluq_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + uzunluq_VALUE;
    }

    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_uzunluq[INDEX] = -1; RECEIVED_ünvan[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Şəbəkə_drayver.받기(입력틀) == 0) break;
    }
    static int INDEX(int tutacaq_VALUE) { return tutacaq_VALUE >= 3 && tutacaq_VALUE < 7 && 접속번호들[tutacaq_VALUE - 3] != 0 ? tutacaq_VALUE - 3 : -1; }
    static int Aç(int 접속번호) {
        if (Şəbəkə_drayver.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 접속번호) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int ön_VALUE = 0; ön_VALUE < 4; ön_VALUE++) if (접속번호들[ön_VALUE] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[INDEX] = 접속번호; RECEIVED_uzunluq[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Bağla(int tutacaq_VALUE) {
        int slot_daxiletmə = INDEX(tutacaq_VALUE);
        if (slot_daxiletmə < 0) return -9;
        접속번호들[slot_daxiletmə] = 0; RECEIVED_uzunluq[slot_daxiletmə] = -1;
        return 0;
    }
    static int eynisəviyyəli_ünvan(int tutacaq_VALUE) { int slot_daxiletmə = INDEX(tutacaq_VALUE); return slot_daxiletmə < 0 ? -9 : RECEIVED_ünvan[slot_daxiletmə]; }
    static int 상대접속번호(int tutacaq_VALUE) { int slot_daxiletmə = INDEX(tutacaq_VALUE); return slot_daxiletmə < 0 ? -9 : 받은접속번호[slot_daxiletmə]; }

    static void 바깥머리(int 종류, boolean yayım_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = yayım_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Şəbəkə_drayver.cihaz_ünvan[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void HTTP_sorğusu_ünvan(int təyinat_VALUE_a0fbc067) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Şəbəkə_drayver.cihaz_ünvan[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, təyinat_VALUE_a0fbc067);
        Şəbəkə_drayver.göndərmək(출력틀, 42);
    }
    static void Proses_ünvan(int uzunluq_VALUE) {
        if (uzunluq_VALUE < 42 || tam_ədəd_16(입력틀, 14) != 1 || tam_ədəd_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || tam_ədəd_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = tam_ədəd_16(입력틀, 20), eynisəviyyəli_VALUE = tam_ədəd_32(입력틀, 28);
        if (종류 == 2 && eynisəviyyəli_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Şəbəkə_drayver.cihaz_ünvan[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = eynisəviyyəli_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Şəbəkə_drayver.cihaz_ünvan[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, eynisəviyyəli_VALUE);
            Şəbəkə_drayver.göndərmək(출력틀, 42);
        }
    }

    static void Proses_kadr(int uzunluq_VALUE) {
        if (uzunluq_VALUE < 14 || uzunluq_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, yayım_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Şəbəkə_drayver.cihaz_ünvan[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) yayım_VALUE = false;
        }
        if (!자기 && !yayım_VALUE) return;
        if (tam_ədəd_16(입력틀, 12) == 0x0806) { Proses_ünvan(uzunluq_VALUE); return; }
        if (tam_ədəd_16(입력틀, 12) != 0x0800) return;
        if (uzunluq_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Başlıq_uzunluq = (입력틀[14] & 15) * 4, 전체길이 = tam_ədəd_16(입력틀, 16);
        if (Başlıq_uzunluq < 20 || Başlıq_uzunluq > 60 || 전체길이 < Başlıq_uzunluq + 8 || 전체길이 > uzunluq_VALUE - 14
            || (tam_ədəd_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || tam_ədəd_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Başlıq_uzunluq, 0) != 65535) { 폐기수++; return; }
        int İcra_Et = 14 + Başlıq_uzunluq, verilənlər_uzunluq = tam_ədəd_16(입력틀, İcra_Et + 4);
        if (verilənlər_uzunluq < 8 || verilənlər_uzunluq != 전체길이 - Başlıq_uzunluq || verilənlər_uzunluq > 1032) { 폐기수++; return; }
        int 출발 = tam_ədəd_32(입력틀, 26);
        if (tam_ədəd_16(입력틀, İcra_Et + 6) != 0 && SUM_VALUE(입력틀, İcra_Et, verilənlər_uzunluq, 가상머리합(출발, 내주소, verilənlər_uzunluq)) != 65535) {
            폐기수++; return;
        }
        int təyinat_VALUE_a0fbc067 = tam_ədəd_16(입력틀, İcra_Et + 2);
        for (int slot_daxiletmə = 0; slot_daxiletmə < 4; slot_daxiletmə++) if (접속번호들[slot_daxiletmə] != 0 && 접속번호들[slot_daxiletmə] == təyinat_VALUE_a0fbc067) {
            if (RECEIVED_uzunluq[slot_daxiletmə] >= 0) { 폐기수++; return; }
            RECEIVED_uzunluq[slot_daxiletmə] = verilənlər_uzunluq - 8; RECEIVED_ünvan[slot_daxiletmə] = 출발; 받은접속번호[slot_daxiletmə] = tam_ədəd_16(입력틀, İcra_Et);
            for (int INDEX = 0; INDEX < verilənlər_uzunluq - 8; INDEX++) RECEIVED_verilənlər[slot_daxiletmə * 1024 + INDEX] = 입력틀[İcra_Et + 8 + INDEX];
            return;
        }
    }

    static void yoxlamaq() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int uzunluq_VALUE = Şəbəkə_drayver.받기(입력틀);
            if (uzunluq_VALUE == 0) return;
            Proses_kadr(uzunluq_VALUE);
        }
    }
    static int FIND_ünvan(int ünvan) {
        if (ünvan == 0 || ünvan == -1 || (ünvan >>> 28) >= 14 || (ünvan >>> 24) == 127 || ünvan == 내주소) return -101;
        int Sonrakı_element = (ünvan & Şəbəkə_maska) == (내주소 & Şəbəkə_maska) ? ünvan : şlüz_VALUE;
        if (Sonrakı_element == 찾은주소) return 0;
        찾을주소 = Sonrakı_element;
        int İcra_Et = cihaz_VALUE.밀리초(), Sonrakı_HTTP_sorğusu = İcra_Et;
        while (cihaz_VALUE.밀리초() - İcra_Et < 1000) {
            if (cihaz_VALUE.밀리초() - Sonrakı_HTTP_sorğusu >= 0) { HTTP_sorğusu_ünvan(Sonrakı_element); Sonrakı_HTTP_sorğusu += 300; }
            yoxlamaq();
            if (찾은주소 == Sonrakı_element) return 0;
            cihaz_VALUE.잠시양보();
        }
        return -110;
    }
    static int göndərmək(int tutacaq_VALUE, int ünvan, int 접속번호, int[] verilənlər, int uzunluq_VALUE) {
        int slot_daxiletmə = INDEX(tutacaq_VALUE);
        if (slot_daxiletmə < 0) return -9;
        if (Şəbəkə_drayver.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || uzunluq_VALUE < 0 || uzunluq_VALUE > 1024) return -22;
        int ölçü = FIND_ünvan(ünvan);
        if (ölçü < 0) return ölçü;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + uzunluq_VALUE);
        넣기16(출력틀, 18, identifikator_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, ünvan);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[slot_daxiletmə]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, uzunluq_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) 출력틀[42 + INDEX] = verilənlər[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, uzunluq_VALUE + 8, 가상머리합(내주소, ünvan, uzunluq_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        ölçü = Şəbəkə_drayver.göndərmək(출력틀, uzunluq_VALUE + 42);
        return ölçü < 0 ? ölçü : uzunluq_VALUE;
    }
    static int 받기(int tutacaq_VALUE, int[] verilənlər, int 용량, int 제한) {
        int slot_daxiletmə = INDEX(tutacaq_VALUE);
        if (slot_daxiletmə < 0) return -9;
        int İcra_Et = cihaz_VALUE.밀리초();
        while (true) {
            yoxlamaq();
            int uzunluq_VALUE = RECEIVED_uzunluq[slot_daxiletmə];
            if (uzunluq_VALUE >= 0) {
                RECEIVED_uzunluq[slot_daxiletmə] = -1;
                if (uzunluq_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < uzunluq_VALUE; INDEX++) verilənlər[INDEX] = RECEIVED_verilənlər[slot_daxiletmə * 1024 + INDEX];
                return uzunluq_VALUE;
            }
            if (제한 == 0) return -11;
            if (cihaz_VALUE.밀리초() - İcra_Et >= 제한) return -110;
            cihaz_VALUE.잠시양보();
        }
    }
    static void vəziyyət_VALUE() {
        SMS_Terminal.Yazma(Şəbəkə_drayver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Yazma("TX: "); SMS_Terminal.수쓰기(Şəbəkə_drayver.송신수);
        SMS_Terminal.Yazma(" RX: "); SMS_Terminal.수쓰기(Şəbəkə_drayver.수신수);
        SMS_Terminal.Yazma(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Yazma("\n");
    }
}
