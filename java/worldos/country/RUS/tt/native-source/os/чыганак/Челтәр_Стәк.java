// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** статик_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class Челтәр_Стәк {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int Челтәр_үрнәк = 0xffffff00; /* ip.conf:NETMASK */
    static final int шлюз_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_озынлык = new int[4], RECEIVED_адрес = new int[4], 받은접속번호 = new int[4];
    static int[] RECEIVED_мәгълүмат = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, күрсәткеч_VALUE = 0, 폐기수 = 0;

    static int бөтен_сан_16(int[] кадр_INDEX, int урнаштыру) { return (кадр_INDEX[урнаштыру] << 8) | кадр_INDEX[урнаштыру + 1]; }
    static int бөтен_сан_32(int[] кадр_INDEX, int урнаштыру) { return (бөтен_сан_16(кадр_INDEX, урнаштыру) << 16) | бөтен_сан_16(кадр_INDEX, урнаштыру + 2); }
    static void 넣기16(int[] кадр_INDEX, int урнаштыру, int VALUE) { кадр_INDEX[урнаштыру] = (VALUE >>> 8) & 255; кадр_INDEX[урнаштыру + 1] = VALUE & 255; }
    static void 넣기32(int[] кадр_INDEX, int урнаштыру, int VALUE) { 넣기16(кадр_INDEX, урнаштыру, VALUE >>> 16); 넣기16(кадр_INDEX, урнаштыру + 2, VALUE); }
    static int SUM_VALUE(int[] кадр_INDEX, int эшләтү, int озынлык_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX += 2)
            VALUE += (кадр_INDEX[эшләтү + INDEX] << 8) | (INDEX + 1 < озынлык_VALUE ? кадр_INDEX[эшләтү + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int озынлык_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + озынлык_VALUE;
    }

    static void CLEAN_Процесс() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_озынлык[INDEX] = -1; RECEIVED_адрес[INDEX] = 0; 받은접속번호[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (Челтәр_драйвер.받기(입력틀) == 0) break;
    }
    static int INDEX(int дескриптор_VALUE) { return дескриптор_VALUE >= 3 && дескриптор_VALUE < 7 && 접속번호들[дескриптор_VALUE - 3] != 0 ? дескриптор_VALUE - 3 : -1; }
    static int ачу(int 접속번호) {
        if (Челтәр_драйвер.입출력기준주소 == 0) return -19;
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
            접속번호들[INDEX] = 접속번호; RECEIVED_озынлык[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Yap(int дескриптор_VALUE) {
        int оя_кертү = INDEX(дескриптор_VALUE);
        if (оя_кертү < 0) return -9;
        접속번호들[оя_кертү] = 0; RECEIVED_озынлык[оя_кертү] = -1;
        return 0;
    }
    static int тиңдәш_адрес(int дескриптор_VALUE) { int оя_кертү = INDEX(дескриптор_VALUE); return оя_кертү < 0 ? -9 : RECEIVED_адрес[оя_кертү]; }
    static int 상대접속번호(int дескриптор_VALUE) { int оя_кертү = INDEX(дескриптор_VALUE); return оя_кертү < 0 ? -9 : 받은접속번호[оя_кертү]; }

    static void 바깥머리(int 종류, boolean киңтапшыру_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = киңтапшыру_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = Челтәр_драйвер.мобиль_адрес[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void 주소요청(int күчерү_урыны_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = Челтәр_драйвер.мобиль_адрес[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, күчерү_урыны_VALUE);
        Челтәр_драйвер.җибәрү(출력틀, 42);
    }
    static void Процесс_адрес(int озынлык_VALUE) {
        if (озынлык_VALUE < 42 || бөтен_сан_16(입력틀, 14) != 1 || бөтен_сан_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || бөтен_сан_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = бөтен_сан_16(입력틀, 20), тиңдәш_VALUE = бөтен_сан_32(입력틀, 28);
        if (종류 == 2 && тиңдәш_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != Челтәр_драйвер.мобиль_адрес[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = тиңдәш_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = Челтәр_драйвер.мобиль_адрес[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, тиңдәш_VALUE);
            Челтәр_драйвер.җибәрү(출력틀, 42);
        }
    }

    static void Процесс_кадр(int озынлык_VALUE) {
        if (озынлык_VALUE < 14 || озынлык_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, киңтапшыру_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != Челтәр_драйвер.мобиль_адрес[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) киңтапшыру_VALUE = false;
        }
        if (!자기 && !киңтапшыру_VALUE) return;
        if (бөтен_сан_16(입력틀, 12) == 0x0806) { Процесс_адрес(озынлык_VALUE); return; }
        if (бөтен_сан_16(입력틀, 12) != 0x0800) return;
        if (озынлык_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Башлама_озынлык = (입력틀[14] & 15) * 4, 전체길이 = бөтен_сан_16(입력틀, 16);
        if (Башлама_озынлык < 20 || Башлама_озынлык > 60 || 전체길이 < Башлама_озынлык + 8 || 전체길이 > озынлык_VALUE - 14
            || (бөтен_сан_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || бөтен_сан_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Башлама_озынлык, 0) != 65535) { 폐기수++; return; }
        int эшләтү = 14 + Башлама_озынлык, мәгълүмат_озынлык = бөтен_сан_16(입력틀, эшләтү + 4);
        if (мәгълүмат_озынлык < 8 || мәгълүмат_озынлык != 전체길이 - Башлама_озынлык || мәгълүмат_озынлык > 1032) { 폐기수++; return; }
        int 출발 = бөтен_сан_32(입력틀, 26);
        if (бөтен_сан_16(입력틀, эшләтү + 6) != 0 && SUM_VALUE(입력틀, эшләтү, мәгълүмат_озынлык, 가상머리합(출발, 내주소, мәгълүмат_озынлык)) != 65535) {
            폐기수++; return;
        }
        int күчерү_урыны_VALUE = бөтен_сан_16(입력틀, эшләтү + 2);
        for (int оя_кертү = 0; оя_кертү < 4; оя_кертү++) if (접속번호들[оя_кертү] != 0 && 접속번호들[оя_кертү] == күчерү_урыны_VALUE) {
            if (RECEIVED_озынлык[оя_кертү] >= 0) { 폐기수++; return; }
            RECEIVED_озынлык[оя_кертү] = мәгълүмат_озынлык - 8; RECEIVED_адрес[оя_кертү] = 출발; 받은접속번호[оя_кертү] = бөтен_сан_16(입력틀, эшләтү);
            for (int INDEX = 0; INDEX < мәгълүмат_озынлык - 8; INDEX++) RECEIVED_мәгълүмат[оя_кертү * 1024 + INDEX] = 입력틀[эшләтү + 8 + INDEX];
            return;
        }
    }

    static void раслау() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int озынлык_VALUE = Челтәр_драйвер.받기(입력틀);
            if (озынлык_VALUE == 0) return;
            Процесс_кадр(озынлык_VALUE);
        }
    }
    static int FIND_адрес(int адрес) {
        if (адрес == 0 || адрес == -1 || (адрес >>> 28) >= 14 || (адрес >>> 24) == 127 || адрес == 내주소) return -101;
        int Киләсе_элемент = (адрес & Челтәр_үрнәк) == (내주소 & Челтәр_үрнәк) ? адрес : шлюз_VALUE;
        if (Киләсе_элемент == 찾은주소) return 0;
        찾을주소 = Киләсе_элемент;
        int эшләтү = мобиль_VALUE.밀리초(), 다음요청 = эшләтү;
        while (мобиль_VALUE.밀리초() - эшләтү < 1000) {
            if (мобиль_VALUE.밀리초() - 다음요청 >= 0) { 주소요청(Киләсе_элемент); 다음요청 += 300; }
            раслау();
            if (찾은주소 == Киләсе_элемент) return 0;
            мобиль_VALUE.잠시양보();
        }
        return -110;
    }
    static int җибәрү(int дескриптор_VALUE, int адрес, int 접속번호, int[] мәгълүмат, int озынлык_VALUE) {
        int оя_кертү = INDEX(дескриптор_VALUE);
        if (оя_кертү < 0) return -9;
        if (Челтәр_драйвер.입출력기준주소 == 0) return -19;
        if (접속번호 < 1 || 접속번호 > 65535 || озынлык_VALUE < 0 || озынлык_VALUE > 1024) return -22;
        int үлчәм = FIND_адрес(адрес);
        if (үлчәм < 0) return үлчәм;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + озынлык_VALUE);
        넣기16(출력틀, 18, күрсәткеч_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, адрес);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[оя_кертү]); 넣기16(출력틀, 36, 접속번호);
        넣기16(출력틀, 38, озынлык_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX++) 출력틀[42 + INDEX] = мәгълүмат[INDEX] & 255;
        int 검사합 = (~SUM_VALUE(출력틀, 34, озынлык_VALUE + 8, 가상머리합(내주소, адрес, озынлык_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, 검사합 == 0 ? 65535 : 검사합);
        үлчәм = Челтәр_драйвер.җибәрү(출력틀, озынлык_VALUE + 42);
        return үлчәм < 0 ? үлчәм : озынлык_VALUE;
    }
    static int 받기(int дескриптор_VALUE, int[] мәгълүмат, int 용량, int 제한) {
        int оя_кертү = INDEX(дескриптор_VALUE);
        if (оя_кертү < 0) return -9;
        int эшләтү = мобиль_VALUE.밀리초();
        while (true) {
            раслау();
            int озынлык_VALUE = RECEIVED_озынлык[оя_кертү];
            if (озынлык_VALUE >= 0) {
                RECEIVED_озынлык[оя_кертү] = -1;
                if (озынлык_VALUE > 용량) return -90;
                for (int INDEX = 0; INDEX < озынлык_VALUE; INDEX++) мәгълүмат[INDEX] = RECEIVED_мәгълүмат[оя_кертү * 1024 + INDEX];
                return озынлык_VALUE;
            }
            if (제한 == 0) return -11;
            if (мобиль_VALUE.밀리초() - эшләтү >= 제한) return -110;
            мобиль_VALUE.잠시양보();
        }
    }
    static void халәт_VALUE() {
        СМС_Терминал.язу(Челтәр_драйвер.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        СМС_Терминал.язу("TX: "); СМС_Терминал.수쓰기(Челтәр_драйвер.송신수);
        СМС_Терминал.язу(" RX: "); СМС_Терминал.수쓰기(Челтәр_драйвер.수신수);
        СМС_Терминал.язу(" DROP: "); СМС_Терминал.수쓰기(폐기수);
        СМС_Терминал.язу("\n");
    }
}
