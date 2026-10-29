// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.jaringan_tumpuk;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP terima_VALUE 분배를 한곳에서 관리한다. */
public final class lapisan_jaringan {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_VALUE_entri(byte[] data, int jalankan, int panjang_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void daftar_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void daftar_IP(int kasus_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kasus_VALUE & 0xff), 처리기);
    }

    public void daftar_pengguna_data_unit(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void daftar_transmisi_kontrol(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean terima_Ethernet(byte[] bingkai_INDEX) {
        if (!jaringan_Alat.teknologi_informasi_Ethernet_bingkai(bingkai_INDEX)) {
            return false;
        }
        int 종류 = jaringan_Alat.Ethernet_UPPER_protokol(bingkai_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_entri(bingkai_INDEX, 14, bingkai_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && terima_cloud_paket(bingkai_INDEX, 14);
    }

    private boolean terima_cloud_paket(byte[] data, int jalankan) {
        if (!jaringan_Alat.teknologi_informasi_IPV_4_protokol(data, jalankan)) {
            return false;
        }
        int judul_panjang = (data[jalankan] & 0x0f) * 4;
        int total_panjang = jaringan_Alat.큰순서짧은정수(data, jalankan + 2);
        if (total_panjang < judul_panjang || jalankan + total_panjang > data.length) {
            return false;
        }
        int kasus_VALUE = data[jalankan + 9] & 0xff;
        int Isi_Mulai = jalankan + judul_panjang;
        int Isi_panjang = total_panjang - judul_panjang;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kasus_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_entri(data, Isi_Mulai, Isi_panjang);
            return true;
        }
        if (Isi_panjang < 4) {
            return false;
        }
        int tujuan_nomor_port = jaringan_Alat.큰순서짧은정수(data, Isi_Mulai + 2);
        Map<Integer, 자료처리기> port_tabel = kasus_VALUE == 17 ? 사용자자료단위처리기 : kasus_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabel.get(Integer.valueOf(tujuan_nomor_port));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_VALUE_entri(data, Isi_Mulai, Isi_panjang);
        return true;
    }
}

