// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** statik_VALUE IPv4/ARP/UDP. 최대 네 통신접속번호와 접속번호마다 한 데이터그램을 보관한다. */
public final class jaringan_tumpuk {
    static final int 내주소 = 0xc0a80064; /* ip.conf:IP */
    static final int jaringan_masker = 0xffffff00; /* ip.conf:NETMASK */
    static final int gateway_VALUE = 0xc0a80001; /* ip.conf:GATEWAY */
    static int[] 입력틀 = new int[1536], 출력틀 = new int[1536];
    static int[] 접속번호들 = new int[4], RECEIVED_panjang = new int[4], RECEIVED_surel = new int[4], RECEIVED_nomor_port = new int[4];
    static int[] RECEIVED_data = new int[4096], 찾은장치 = new int[6];
    static int 찾을주소 = 0, 찾은주소 = 0, pengidentifikasi_VALUE = 0, 폐기수 = 0;

    static int bilangan_bulat_16(int[] bingkai_INDEX, int posisi) { return (bingkai_INDEX[posisi] << 8) | bingkai_INDEX[posisi + 1]; }
    static int bilangan_bulat_32(int[] bingkai_INDEX, int posisi) { return (bilangan_bulat_16(bingkai_INDEX, posisi) << 16) | bilangan_bulat_16(bingkai_INDEX, posisi + 2); }
    static void 넣기16(int[] bingkai_INDEX, int posisi, int VALUE) { bingkai_INDEX[posisi] = (VALUE >>> 8) & 255; bingkai_INDEX[posisi + 1] = VALUE & 255; }
    static void 넣기32(int[] bingkai_INDEX, int posisi, int VALUE) { 넣기16(bingkai_INDEX, posisi, VALUE >>> 16); 넣기16(bingkai_INDEX, posisi + 2, VALUE); }
    static int SUM_VALUE(int[] bingkai_INDEX, int jalankan, int panjang_VALUE, int VALUE) {
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX += 2)
            VALUE += (bingkai_INDEX[jalankan + INDEX] << 8) | (INDEX + 1 < panjang_VALUE ? bingkai_INDEX[jalankan + INDEX + 1] : 0);
        while ((VALUE >>> 16) != 0) VALUE = (VALUE & 65535) + (VALUE >>> 16);
        return VALUE;
    }
    static int 가상머리합(int 출발, int 도착, int panjang_VALUE) {
        return (출발 >>> 16) + (출발 & 65535) + (도착 >>> 16) + (도착 & 65535) + 17 + panjang_VALUE;
    }

    static void CLEAN_Proses() {
        for (int INDEX = 0; INDEX < 4; INDEX++) {
            접속번호들[INDEX] = 0; RECEIVED_panjang[INDEX] = -1; RECEIVED_surel[INDEX] = 0; RECEIVED_nomor_port[INDEX] = 0;
        }
        for (int INDEX = 0; INDEX < 64; INDEX++) if (jaringan_driver.terima(입력틀) == 0) break;
    }
    static int INDEX(int handel_VALUE) { return handel_VALUE >= 3 && handel_VALUE < 7 && 접속번호들[handel_VALUE - 3] != 0 ? handel_VALUE - 3 : -1; }
    static int Buka(int nomor_port) {
        if (jaringan_driver.입출력기준주소 == 0) return -19;
        if (nomor_port < 0 || nomor_port > 65535) return -22;
        if (nomor_port != 0) for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == nomor_port) return -98;
        for (int INDEX = 0; INDEX < 4; INDEX++) if (접속번호들[INDEX] == 0) {
            if (nomor_port == 0) {
                nomor_port = 49152;
                boolean 겹침 = true;
                while (겹침) {
                    겹침 = false;
                    for (int depan_VALUE = 0; depan_VALUE < 4; depan_VALUE++) if (접속번호들[depan_VALUE] == nomor_port) 겹침 = true;
                    if (겹침) nomor_port++;
                }
            }
            접속번호들[INDEX] = nomor_port; RECEIVED_panjang[INDEX] = -1;
            return INDEX + 3;
        }
        return -24;
    }
    static int Tutup(int handel_VALUE) {
        int slot_entri = INDEX(handel_VALUE);
        if (slot_entri < 0) return -9;
        접속번호들[slot_entri] = 0; RECEIVED_panjang[slot_entri] = -1;
        return 0;
    }
    static int serekan_surel(int handel_VALUE) { int slot_entri = INDEX(handel_VALUE); return slot_entri < 0 ? -9 : RECEIVED_surel[slot_entri]; }
    static int serekan_nomor_port(int handel_VALUE) { int slot_entri = INDEX(handel_VALUE); return slot_entri < 0 ? -9 : RECEIVED_nomor_port[slot_entri]; }

    static void 바깥머리(int 종류, boolean siar_VALUE) {
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[INDEX] = siar_VALUE ? 255 : 찾은장치[INDEX];
            출력틀[6 + INDEX] = jaringan_driver.Ponsel_surel[INDEX];
        }
        넣기16(출력틀, 12, 종류);
    }
    static void permintaan_surel(int tujuan_VALUE) {
        바깥머리(0x0806, true);
        넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
        출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 1);
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            출력틀[22 + INDEX] = jaringan_driver.Ponsel_surel[INDEX]; 출력틀[32 + INDEX] = 0;
        }
        넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, tujuan_VALUE);
        jaringan_driver.kirim(출력틀, 42);
    }
    static void Proses_surel(int panjang_VALUE) {
        if (panjang_VALUE < 42 || bilangan_bulat_16(입력틀, 14) != 1 || bilangan_bulat_16(입력틀, 16) != 0x0800
            || 입력틀[18] != 6 || 입력틀[19] != 4 || bilangan_bulat_32(입력틀, 38) != 내주소) { 폐기수++; return; }
        int 종류 = bilangan_bulat_16(입력틀, 20), serekan_VALUE = bilangan_bulat_32(입력틀, 28);
        if (종류 == 2 && serekan_VALUE == 찾을주소) {
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                if (입력틀[6 + INDEX] != 입력틀[22 + INDEX] || 입력틀[32 + INDEX] != jaringan_driver.Ponsel_surel[INDEX]) return;
            }
            for (int INDEX = 0; INDEX < 6; INDEX++) 찾은장치[INDEX] = 입력틀[22 + INDEX];
            찾은주소 = serekan_VALUE;
        } else if (종류 == 1) {
            바깥머리(0x0806, false);
            넣기16(출력틀, 14, 1); 넣기16(출력틀, 16, 0x0800);
            출력틀[18] = 6; 출력틀[19] = 4; 넣기16(출력틀, 20, 2);
            for (int INDEX = 0; INDEX < 6; INDEX++) {
                출력틀[INDEX] = 입력틀[22 + INDEX]; 출력틀[32 + INDEX] = 입력틀[22 + INDEX];
                출력틀[22 + INDEX] = jaringan_driver.Ponsel_surel[INDEX];
            }
            넣기32(출력틀, 28, 내주소); 넣기32(출력틀, 38, serekan_VALUE);
            jaringan_driver.kirim(출력틀, 42);
        }
    }

    static void Proses_bingkai(int panjang_VALUE) {
        if (panjang_VALUE < 14 || panjang_VALUE > 입력틀.length) { 폐기수++; return; }
        boolean 자기 = true, siar_VALUE = true;
        for (int INDEX = 0; INDEX < 6; INDEX++) {
            if (입력틀[INDEX] != jaringan_driver.Ponsel_surel[INDEX]) 자기 = false;
            if (입력틀[INDEX] != 255) siar_VALUE = false;
        }
        if (!자기 && !siar_VALUE) return;
        if (bilangan_bulat_16(입력틀, 12) == 0x0806) { Proses_surel(panjang_VALUE); return; }
        if (bilangan_bulat_16(입력틀, 12) != 0x0800) return;
        if (panjang_VALUE < 34 || (입력틀[14] >>> 4) != 4) { 폐기수++; return; }
        int judul_panjang = (입력틀[14] & 15) * 4, total_panjang = bilangan_bulat_16(입력틀, 16);
        if (judul_panjang < 20 || judul_panjang > 60 || total_panjang < judul_panjang + 8 || total_panjang > panjang_VALUE - 14
            || (bilangan_bulat_16(입력틀, 20) & 0x3fff) != 0 || 입력틀[23] != 17
            || bilangan_bulat_32(입력틀, 30) != 내주소 || SUM_VALUE(입력틀, 14, judul_panjang, 0) != 65535) { 폐기수++; return; }
        int jalankan = 14 + judul_panjang, data_panjang = bilangan_bulat_16(입력틀, jalankan + 4);
        if (data_panjang < 8 || data_panjang != total_panjang - judul_panjang || data_panjang > 1032) { 폐기수++; return; }
        int 출발 = bilangan_bulat_32(입력틀, 26);
        if (bilangan_bulat_16(입력틀, jalankan + 6) != 0 && SUM_VALUE(입력틀, jalankan, data_panjang, 가상머리합(출발, 내주소, data_panjang)) != 65535) {
            폐기수++; return;
        }
        int tujuan_VALUE = bilangan_bulat_16(입력틀, jalankan + 2);
        for (int slot_entri = 0; slot_entri < 4; slot_entri++) if (접속번호들[slot_entri] != 0 && 접속번호들[slot_entri] == tujuan_VALUE) {
            if (RECEIVED_panjang[slot_entri] >= 0) { 폐기수++; return; }
            RECEIVED_panjang[slot_entri] = data_panjang - 8; RECEIVED_surel[slot_entri] = 출발; RECEIVED_nomor_port[slot_entri] = bilangan_bulat_16(입력틀, jalankan);
            for (int INDEX = 0; INDEX < data_panjang - 8; INDEX++) RECEIVED_data[slot_entri * 1024 + INDEX] = 입력틀[jalankan + 8 + INDEX];
            return;
        }
    }

    static void periksa() {
        for (int INDEX = 0; INDEX < 16; INDEX++) {
            int panjang_VALUE = jaringan_driver.terima(입력틀);
            if (panjang_VALUE == 0) return;
            Proses_bingkai(panjang_VALUE);
        }
    }
    static int FIND_surel(int surel) {
        if (surel == 0 || surel == -1 || (surel >>> 28) >= 14 || (surel >>> 24) == 127 || surel == 내주소) return -101;
        int Berikutnya_item = (surel & jaringan_masker) == (내주소 & jaringan_masker) ? surel : gateway_VALUE;
        if (Berikutnya_item == 찾은주소) return 0;
        찾을주소 = Berikutnya_item;
        int jalankan = Ponsel_VALUE.밀리초(), Berikutnya_permintaan = jalankan;
        while (Ponsel_VALUE.밀리초() - jalankan < 1000) {
            if (Ponsel_VALUE.밀리초() - Berikutnya_permintaan >= 0) { permintaan_surel(Berikutnya_item); Berikutnya_permintaan += 300; }
            periksa();
            if (찾은주소 == Berikutnya_item) return 0;
            Ponsel_VALUE.잠시양보();
        }
        return -110;
    }
    static int kirim(int handel_VALUE, int surel, int nomor_port, int[] data, int panjang_VALUE) {
        int slot_entri = INDEX(handel_VALUE);
        if (slot_entri < 0) return -9;
        if (jaringan_driver.입출력기준주소 == 0) return -19;
        if (nomor_port < 1 || nomor_port > 65535 || panjang_VALUE < 0 || panjang_VALUE > 1024) return -22;
        int hasil = FIND_surel(surel);
        if (hasil < 0) return hasil;
        바깥머리(0x0800, false);
        출력틀[14] = 0x45; 출력틀[15] = 0; 넣기16(출력틀, 16, 28 + panjang_VALUE);
        넣기16(출력틀, 18, pengidentifikasi_VALUE++); 넣기16(출력틀, 20, 0x4000);
        출력틀[22] = 64; 출력틀[23] = 17; 넣기16(출력틀, 24, 0);
        넣기32(출력틀, 26, 내주소); 넣기32(출력틀, 30, surel);
        넣기16(출력틀, 24, ~SUM_VALUE(출력틀, 14, 20, 0));
        넣기16(출력틀, 34, 접속번호들[slot_entri]); 넣기16(출력틀, 36, nomor_port);
        넣기16(출력틀, 38, panjang_VALUE + 8); 넣기16(출력틀, 40, 0);
        for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) 출력틀[42 + INDEX] = data[INDEX] & 255;
        int checksum = (~SUM_VALUE(출력틀, 34, panjang_VALUE + 8, 가상머리합(내주소, surel, panjang_VALUE + 8))) & 65535;
        넣기16(출력틀, 40, checksum == 0 ? 65535 : checksum);
        hasil = jaringan_driver.kirim(출력틀, panjang_VALUE + 42);
        return hasil < 0 ? hasil : panjang_VALUE;
    }
    static int terima(int handel_VALUE, int[] data, int kapasitas_VALUE, int 제한) {
        int slot_entri = INDEX(handel_VALUE);
        if (slot_entri < 0) return -9;
        int jalankan = Ponsel_VALUE.밀리초();
        while (true) {
            periksa();
            int panjang_VALUE = RECEIVED_panjang[slot_entri];
            if (panjang_VALUE >= 0) {
                RECEIVED_panjang[slot_entri] = -1;
                if (panjang_VALUE > kapasitas_VALUE) return -90;
                for (int INDEX = 0; INDEX < panjang_VALUE; INDEX++) data[INDEX] = RECEIVED_data[slot_entri * 1024 + INDEX];
                return panjang_VALUE;
            }
            if (제한 == 0) return -11;
            if (Ponsel_VALUE.밀리초() - jalankan >= 제한) return -110;
            Ponsel_VALUE.잠시양보();
        }
    }
    static void Status_VALUE() {
        SMS_Terminal.Tulis(jaringan_driver.입출력기준주소 == 0 ? "NET unavailable (RTL8139 required)\n" : "NET RTL8139 192.168.0.100/24 gateway 192.168.0.1 UDP\n");
        SMS_Terminal.Tulis("TX: "); SMS_Terminal.수쓰기(jaringan_driver.송신수);
        SMS_Terminal.Tulis(" RX: "); SMS_Terminal.수쓰기(jaringan_driver.terima_COUNT);
        SMS_Terminal.Tulis(" DROP: "); SMS_Terminal.수쓰기(폐기수);
        SMS_Terminal.Tulis("\n");
    }
}
