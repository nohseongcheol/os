// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statesch_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Reseau_Stapel {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Reseau_Mask = 0xffffff00; /* ip.conf:NETMASK */
    static final int Gateway_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_Längt = new int[4], RECEIVED_Adress = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_Daten = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, Identifikateur_VALUE = 0, 폐기수 = 0;

    static int Ganzzuel_16(int[] Rumm_INDEX, int positionéieren) { return (Rumm_INDEX[positionéieren] << 8) | Rumm_INDEX[positionéieren + 1]; }
    static int Ganzzuel_32(int[] Rumm_INDEX, int positionéieren) { return (Ganzzuel_16(Rumm_INDEX, positionéieren) << 16) | Ganzzuel_16(Rumm_INDEX, positionéieren + 2); }
    static void 넣기16(int[] Rumm_INDEX, int positionéieren, int VALUE) { Rumm_INDEX[positionéieren] = (VALUE >>> 8) & 255; Rumm_INDEX[positionéieren + 1] = VALUE & 255; }
    static void 넣기32(int[] Rumm_INDEX, int positionéieren, int VALUE) { 넣기16(Rumm_INDEX, positionéieren, VALUE >>> 16); 넣기16(Rumm_INDEX, positionéieren + 2, VALUE); }
    static int SUM_VALUE(int[] Rumm_INDEX, int Laf, int Längt_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX += 2)
            VALUE += (Rumm_INDEX[Laf + INDEX] << 8) | (INDEX + 1 < Längt_VALUE ? Rumm_INDEX[Laf + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int Längt_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + Längt_VALUE;
    }

    static void CLEAN_Prozess() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_Längt[INDEX] = -1; RECEIVED_Adress[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Reseau_Driver.받기(입력틀) == 0) break;
    }
    static int INDEX(int Handle_VALUE) { return Handle_VALUE >= 3 && Handle_VALUE < 7 && 접속번호들[Handle_VALUE - 3] != 0 ? Handle_VALUE - 3 : -1; }
    static int ariichten(int 접속번호) {
        if (Reseau_Driver.입출력기준주소 == 0) return -19;
        if (접속번호 < 0 || 접속번호 > 65535) return -22;
        if (접속번호 != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 접속번호) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (접속번호 == 0) {
                접속번호 = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int 앞 = 0; 앞 < 4; 앞++) if (접속번호들[앞] == 접속번호) 겹침 = true;
                    if (겹침) 접속번호++;
                }
            }
            접속번호들[INDEX] = 접속번호; RECEIVED_Längt[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Clôture(int Handle_VALUE) {
        int Slot_Agab = INDEX(Handle_VALUE);
        if (Slot_Agab < 0) return -9;
        접속번호들[Slot_Agab] = 0; RECEIVED_Längt[Slot_Agab] = -1;
        return 0;
    }
    static int Peer_Adress(int Handle_VALUE) { int Slot_Agab = INDEX(Handle_VALUE); return Slot_Agab < 0 ? -9 : RECEIVED_Adress[Slot_Agab]; }
    static int 상대접속번호(int Handle_VALUE) { int Slot_Agab = INDEX(Handle_VALUE); return Slot_Agab < 0 ? -9 : 받은접속번호[Slot_Agab]; }

    static void 바깥머리(int 종류, boolean Iwwerdroung_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = Iwwerdroung_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Reseau_Driver.Mobil_Adress[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int Zil_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Reseau_Driver.Mobil_Adress[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Zil_VALUE);
        Reseau_Driver.mailen(출력틀, 42);
    }
    static void Prozess_Adress(int Längt_VALUE) {
        if (Längt_VALUE < 42 || Ganzzuel_16(입력틀, 14) != 1 || Ganzzuel_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || Ganzzuel_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = Ganzzuel_16(입력틀, 20), Peer_VALUE = Ganzzuel_32(입력틀, 28);
        if (종류 == 2 && Peer_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Reseau_Driver.Mobil_Adress[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = Peer_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Reseau_Driver.Mobil_Adress[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, Peer_VALUE);
            Reseau_Driver.mailen(출력틀, 42);
        }
    }

    static void Prozess_Rumm(int Längt_VALUE) {
        if (Längt_VALUE < 14 || Längt_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, Iwwerdroung_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Reseau_Driver.Mobil_Adress[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) Iwwerdroung_VALUE = false;
        }
        if (!자기 && !Iwwerdroung_VALUE) return;
        if (Ganzzuel_16(입력틀, 12) == 0x0806) { Prozess_Adress(Längt_VALUE); return; }
        if (Ganzzuel_16(입력틀, 12) != 0x0800) return;
        if (Längt_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int En_tête_Längt = (입력틀[14] & 15) * 4, 전체길이 = Ganzzuel_16(입력틀, 16);
        if (En_tête_Längt < 20 || En_tête_Längt > 60 || 전체길이 < En_tête_Längt + 8 || 전체길이 > Längt_VALUE - 14
            || (Ganzzuel_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || Ganzzuel_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, En_tête_Längt, 0) != 65535) { 폐기수++; return; }
        int Laf = 14 + En_tête_Längt, Daten_Längt = Ganzzuel_16(입력틀, Laf + 4);
        if (Daten_Längt < 8 || Daten_Längt != 전체길이 - En_tête_Längt || Daten_Längt > 1032) { 폐기수++; return; }
        int 출발 = Ganzzuel_32(입력틀, 26);
        if (Ganzzuel_16(입력틀, Laf + 6) != 0 && SUM_VALUE(입력틀, Laf, Daten_Längt, 가상머리합(출발, 내주소, Daten_Längt)) != 65535) {
            폐기수++; return;
        }
        int Zil_VALUE = Ganzzuel_16(입력틀, Laf + 2);
        for (int Slot_Agab = 0; Slot_Agab < 4; Slot_Agab++) if (접속번호들[Slot_Agab] != 0 && 접속번호들[Slot_Agab] == Zil_VALUE) {
            if (RECEIVED_Längt[Slot_Agab] >= 0) { 폐기수++; return; }
            RECEIVED_Längt[Slot_Agab] = Daten_Längt - 8; RECEIVED_Adress[Slot_Agab] = 출발; 받은접속번호[Slot_Agab] = Ganzzuel_16(입력틀, Laf);
            for (int INDEX = 0; INDEX < Daten_Längt - 8; INDEX++) RECEIVED_Daten[Slot_Agab * 1024 + INDEX] = 입력틀[Laf + 8 + INDEX];
            return;
        }
    }

    static void verifizéieren() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int Längt_VALUE = Reseau_Driver.받기(입력틀);
            if (Längt_VALUE == 0) return;
            Prozess_Rumm(Längt_VALUE);
        }
    }
    static int FIND_Adress(int Adress) {
        if (Adress == 0 || Adress == -1 || (Adress >>> 28) >= 14 || (Adress >>> 24) == 127 || Adress == 내주소) return -101;
        int Weider_Element = (Adress & Reseau_Mask) == (내주소 & Reseau_Mask) ? Adress : Gateway_VALUE;
        if (Weider_Element == 찾은주소) return 0;
        찾을주소 = Weider_Element;
        int Laf = Mobil_VALUE.밀리초(), 다음요청 = Laf;
        while (Mobil_VALUE.밀리초() - Laf < 1000) {
            if (Mobil_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Weider_Element); 다음요청 += 300; }
            verifizéieren();
            if (찾은주소 == Weider_Element) return 0;
            Mobil_VALUE.잠시양보();
        }
        return -110;
    }
    static int mailen(int Handle_VALUE, int Adress, int 접속번호, int[] Daten, int Längt_VALUE) {
        int Slot_Agab = INDEX(Handle_VALUE);
        if (Slot_Agab < 0) return -9;
        if (Reseau_Driver.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || Längt_VALUE < 0 || Längt_VALUE > 1024) return -22;
        int Mooss = FIND_Adress(Adress);
        if (Mooss < 0) return Mooss;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + Längt_VALUE);
        넣기16(출력틀, 18, Identifikateur_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, Adress);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[Slot_Agab]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, Längt_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) 출력틀[42 + INDEX] = Daten[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, Längt_VALUE + 8, 가상머리합(내주소, Adress, Längt_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        Mooss = Reseau_Driver.mailen(출력틀, Längt_VALUE + 42);
        return Mooss < 0 ? Mooss : Längt_VALUE;
    }
    static int 받기(int Handle_VALUE, int[] Daten, int 용량, int 제한) {
        int Slot_Agab = INDEX(Handle_VALUE);
        if (Slot_Agab < 0) return -9;
        int Laf = Mobil_VALUE.밀리초();
        while (true) {
            verifizéieren();
            int Längt_VALUE = RECEIVED_Längt[Slot_Agab];
            if (Längt_VALUE >= 0) {
                RECEIVED_Längt[Slot_Agab] = -1;
                if (Längt_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < Längt_VALUE; INDEX++) Daten[INDEX] = RECEIVED_Daten[Slot_Agab * 1024 + INDEX];
                return Längt_VALUE;
            }
            if (제한 == 0) return -11;
            if (Mobil_VALUE.밀리초() - Laf >= 제한) return -110;
            Mobil_VALUE.잠시양보();
        }
    }
    static void Status_VALUE() {
        SMS_Terminal.schreiwen(Reseau_Driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.schreiwen("TX: "); SMS_Terminal.수쓰기(Reseau_Driver.송신수);
        SMS_Terminal.schreiwen(" RX: "); SMS_Terminal.수쓰기(Reseau_Driver.수신수);
        SMS_Terminal.schreiwen(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.schreiwen("\n");
    }
}
