// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.rangkaian_tindan;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class rangkaian_lapisan {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_VALUE_pemasukan(byte[] data, int Jalan, int kepanjangan_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void daftar_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void daftar_IP(int kes_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kes_VALUE & 0xff), 처리기);
    }

    public void daftar_pengguna_data_unit(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void daftar_penghantaran_kawalan(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] bingkai_INDEX) {
        if (!rangkaian_Alat.teknologi_maklumat_Ethernet_bingkai(bingkai_INDEX)) {
            return false;
        }
        int 종류 = rangkaian_Alat.Ethernet_UPPER_protokol(bingkai_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_pemasukan(bingkai_INDEX, 14, bingkai_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(bingkai_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int Jalan) {
        if (!rangkaian_Alat.상호통신망규약사판인가(data, Jalan)) {
            return false;
        }
        int Pengepala_kepanjangan = (data[Jalan] & 0x0f) * 4;
        int 전체길이 = rangkaian_Alat.큰순서짧은정수(data, Jalan + 2);
        if (전체길이 < Pengepala_kepanjangan || Jalan + 전체길이 > data.length) {
            return false;
        }
        int kes_VALUE = data[Jalan + 9] & 0xff;
        int Kandungan_Mula = Jalan + Pengepala_kepanjangan;
        int Kandungan_kepanjangan = 전체길이 - Pengepala_kepanjangan;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kes_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_pemasukan(data, Kandungan_Mula, Kandungan_kepanjangan);
            return true;
        }
        if (Kandungan_kepanjangan < 4) {
            return false;
        }
        int destinasi_nombor_port = rangkaian_Alat.큰순서짧은정수(data, Kandungan_Mula + 2);
        Map<Integer, 자료처리기> port_jadual = kes_VALUE == 17 ? 사용자자료단위처리기 : kes_VALUE == 6 ? 전송제어처리기 : null;
        if (port_jadual == null) {
            return false;
        }
        자료처리기 포트처리기 = port_jadual.get(Integer.valueOf(destinasi_nombor_port));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_VALUE_pemasukan(data, Kandungan_Mula, Kandungan_kepanjangan);
        return true;
    }
}

