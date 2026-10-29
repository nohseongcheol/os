// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class rangkaian_tindan {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int rangkaian_topeng = 0xffffff00; /* ip.conf:NETMASK */
    static final int get_laluan_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_kepanjangan = new int[4], RECEIVED_e_mel = new int[4], RECEIVED_nombor_port = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, 식별자 = 0, 폐기수 = 0;

    static int integer_16(int[] bingkai_INDEX, int Kedudukan) { return (bingkai_INDEX[Kedudukan] << 8) | bingkai_INDEX[Kedudukan + 1]; }
    static int integer_32(int[] bingkai_INDEX, int Kedudukan) { return (integer_16(bingkai_INDEX, Kedudukan) << 16) | integer_16(bingkai_INDEX, Kedudukan + 2); }
    static void 넣기16(int[] bingkai_INDEX, int Kedudukan, int VALUE) { bingkai_INDEX[Kedudukan] = (VALUE >>> 8) & 255; bingkai_INDEX[Kedudukan + 1] = VALUE & 255; }
    static void 넣기32(int[] bingkai_INDEX, int Kedudukan, int VALUE) { 넣기16(bingkai_INDEX, Kedudukan, VALUE >>> 16); 넣기16(bingkai_INDEX, Kedudukan + 2, VALUE); }
    static int SUM_VALUE(int[] bingkai_INDEX, int Jalan, int kepanjangan_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX += 2)
            VALUE += (bingkai_INDEX[Jalan + INDEX] << 8) | (INDEX + 1 < kepanjangan_VALUE ? bingkai_INDEX[Jalan + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int kepanjangan_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + kepanjangan_VALUE;
    }

    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_kepanjangan[INDEX] = -1; RECEIVED_e_mel[INDEX] = 0; RECEIVED_nombor_port[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (rangkaian_pemacu.받기(입력틀) == 0) break;
    }
    static int INDEX(int pemegang_VALUE) { return pemegang_VALUE >= 3 && pemegang_VALUE < 7 && 접속번호들[pemegang_VALUE - 3] != 0 ? pemegang_VALUE - 3 : -1; }
    static int Buka(int nombor_port) {
        if (rangkaian_pemacu.입출력기준주소 == 0) return -19;
        if (nombor_port < 0 || nombor_port > 65535) return -22;
        if (nombor_port != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == nombor_port) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (nombor_port == 0) {
                nombor_port = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int hadapan_VALUE = 0; hadapan_VALUE < 4; hadapan_VALUE++) if (접속번호들[hadapan_VALUE] == nombor_port) 겹침 = true;
                    if (겹침) nombor_port++;
                }
            }
            접속번호들[INDEX] = nombor_port; RECEIVED_kepanjangan[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Tutup(int pemegang_VALUE) {
        int 칸 = INDEX(pemegang_VALUE);
        if (칸 < 0) return -9;
        접속번호들[칸] = 0; RECEIVED_kepanjangan[칸] = -1;
        return 0;
    }
    static int rakan_e_mel(int pemegang_VALUE) { int 칸 = INDEX(pemegang_VALUE); return 칸 < 0 ? -9 : RECEIVED_e_mel[칸]; }
    static int rakan_nombor_port(int pemegang_VALUE) { int 칸 = INDEX(pemegang_VALUE); return 칸 < 0 ? -9 : RECEIVED_nombor_port[칸]; }

    static void 바깥머리(int 종류, boolean siaran_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = siaran_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = rangkaian_pemacu.peranti_e_mel[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void permintaan_e_mel(int destinasi_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = rangkaian_pemacu.peranti_e_mel[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, destinasi_VALUE);
        rangkaian_pemacu.e_mel_9aee63bd(출력틀, 42);
    }
    static void Proses_e_mel(int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 42 || integer_16(입력틀, 14) != 1 || integer_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || integer_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = integer_16(입력틀, 20), rakan_VALUE = integer_32(입력틀, 28);
        if (종류 == 2 && rakan_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != rangkaian_pemacu.peranti_e_mel[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = rakan_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = rangkaian_pemacu.peranti_e_mel[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, rakan_VALUE);
            rangkaian_pemacu.e_mel_9aee63bd(출력틀, 42);
        }
    }

    static void Proses_bingkai(int kepanjangan_VALUE) {
        if (kepanjangan_VALUE < 14 || kepanjangan_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, siaran_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != rangkaian_pemacu.peranti_e_mel[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) siaran_VALUE = false;
        }
        if (!자기 && !siaran_VALUE) return;
        if (integer_16(입력틀, 12) == 0x0806) { Proses_e_mel(kepanjangan_VALUE); return; }
        if (integer_16(입력틀, 12) != 0x0800) return;
        if (kepanjangan_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int Pengepala_kepanjangan = (입력틀[14] & 15) * 4, 전체길이 = integer_16(입력틀, 16);
        if (Pengepala_kepanjangan < 20 || Pengepala_kepanjangan > 60 || 전체길이 < Pengepala_kepanjangan + 8 || 전체길이 > kepanjangan_VALUE - 14
            || (integer_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || integer_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, Pengepala_kepanjangan, 0) != 65535) { 폐기수++; return; }
        int Jalan = 14 + Pengepala_kepanjangan, data_kepanjangan = integer_16(입력틀, Jalan + 4);
        if (data_kepanjangan < 8 || data_kepanjangan != 전체길이 - Pengepala_kepanjangan || data_kepanjangan > 1032) { 폐기수++; return; }
        int 출발 = integer_32(입력틀, 26);
        if (integer_16(입력틀, Jalan + 6) != 0 && SUM_VALUE(입력틀, Jalan, data_kepanjangan, 가상머리합(출발, 내주소, data_kepanjangan)) != 65535) {
            폐기수++; return;
        }
        int destinasi_VALUE = integer_16(입력틀, Jalan + 2);
        for (int 칸 = 0; 칸 < 4; 칸++) if (접속번호들[칸] != 0 && 접속번호들[칸] == destinasi_VALUE) {
            if (RECEIVED_kepanjangan[칸] >= 0) { 폐기수++; return; }
            RECEIVED_kepanjangan[칸] = data_kepanjangan - 8; RECEIVED_e_mel[칸] = 출발; RECEIVED_nombor_port[칸] = integer_16(입력틀, Jalan);
            for (int INDEX = 0; INDEX < data_kepanjangan - 8; INDEX++) RECEIVED_data[칸 * 1024 + INDEX] = 입력틀[Jalan + 8 + INDEX];
            return;
        }
    }

    static void tentu_sahkan() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int kepanjangan_VALUE = rangkaian_pemacu.받기(입력틀);
            if (kepanjangan_VALUE == 0) return;
            Proses_bingkai(kepanjangan_VALUE);
        }
    }
    static int Cari_e_mel(int e_mel) {
        if (e_mel == 0 || e_mel == -1 || (e_mel >>> 28) >= 14 || (e_mel >>> 24) == 127 || e_mel == 내주소) return -101;
        int Seterusnya_item = (e_mel & rangkaian_topeng) == (내주소 & rangkaian_topeng) ? e_mel : get_laluan_VALUE;
        if (Seterusnya_item == 찾은주소) return 0;
        찾을주소 = Seterusnya_item;
        int Jalan = peranti_VALUE.밀리초(), Seterusnya_permintaan = Jalan;
        while (peranti_VALUE.밀리초() - Jalan < 1000) {
            if (peranti_VALUE.밀리초() - Seterusnya_permintaan >= 0) { permintaan_e_mel(Seterusnya_item); Seterusnya_permintaan += 300; }
            tentu_sahkan();
            if (찾은주소 == Seterusnya_item) return 0;
            peranti_VALUE.잠시양보();
        }
        return -110;
    }
    static int e_mel_9aee63bd(int pemegang_VALUE, int e_mel, int nombor_port, int[] data, int kepanjangan_VALUE) {
        int 칸 = INDEX(pemegang_VALUE);
        if (칸 < 0) return -9;
        if (rangkaian_pemacu.입출력기준주소 == 0) return -19;
        if (nombor_port < 1 || nombor_port > 65535 || kepanjangan_VALUE < 0 || kepanjangan_VALUE > 1024) return -22;
        int ukuran = Cari_e_mel(e_mel);
        if (ukuran < 0) return ukuran;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + kepanjangan_VALUE);
        넣기16(출력틀, 18, 식별자++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, e_mel);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[칸]); 넣기16(출력틀, 36, nombor_port);
        넣기16(출력틀, 38, kepanjangan_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int hasil_tambah_semak = (~SUM_VALUE(출력틀, 34, kepanjangan_VALUE + 8, 가상머리합(내주소, e_mel, kepanjangan_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, hasil_tambah_semak == 0 ? 65535 : hasil_tambah_semak);
        ukuran = rangkaian_pemacu.e_mel_9aee63bd(출력틀, kepanjangan_VALUE + 42);
        return ukuran < 0 ? ukuran : kepanjangan_VALUE;
    }
    static int 받기(int pemegang_VALUE, int[] data, int kapasiti_VALUE, int 제한) {
        int 칸 = INDEX(pemegang_VALUE);
        if (칸 < 0) return -9;
        int Jalan = peranti_VALUE.밀리초();
        while (true) {
            tentu_sahkan();
            int kepanjangan_VALUE = RECEIVED_kepanjangan[칸];
            if (kepanjangan_VALUE >= 0) {
                RECEIVED_kepanjangan[칸] = -1;
                if (kepanjangan_VALUE > kapasiti_VALUE) return -90;
                for (int INDEX = 0; INDEX < kepanjangan_VALUE; INDEX++) data[INDEX] = RECEIVED_data[칸 * 1024 + INDEX];
                return kepanjangan_VALUE;
            }
            if (제한 == 0) return -11;
            if (peranti_VALUE.밀리초() - Jalan >= 제한) return -110;
            peranti_VALUE.잠시양보();
        }
    }
    static void status_VALUE() {
        SMS_Terminal.Tulis(rangkaian_pemacu.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Tulis("TX: "); SMS_Terminal.수쓰기(rangkaian_pemacu.송신수);
        SMS_Terminal.Tulis(" RX: "); SMS_Terminal.수쓰기(rangkaian_pemacu.수신수);
        SMS_Terminal.Tulis(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Tulis("\n");
    }
}
