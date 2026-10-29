// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.verkko_Pino;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP saada_ARVO 분배를 한곳에서 관리한다. */
public final class verkkotaso {
    @FunctionalInterface
    public interface 자료처리기 {
        void prosessi_ARVO_merkintä(byte[] data, int Suorita_2, int kesto_ARVO);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void rekisteri_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void rekisteri_IP(int sopimuksen_arvo, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(sopimuksen_arvo & 0xff), 처리기);
    }

    public void rekisteri_käyttäjä_data_osio(int laitteisto_portti, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(laitteisto_portti & 0xffff), 처리기);
    }

    public void rekisteri_lähettäminen_ohjain(int laitteisto_portti, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(laitteisto_portti & 0xffff), 처리기);
    }

    public boolean saada_Ethernet(byte[] kuva_INDEKSI) {
        if (!verkko_Työkalut.tietojärjestelmät_Ethernet_kuva(kuva_INDEKSI)) {
            return false;
        }
        int 종류 = verkko_Työkalut.Ethernet_ISOT_protokolla(kuva_INDEKSI);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.prosessi_ARVO_merkintä(kuva_INDEKSI, 14, kuva_INDEKSI.length - 14);
            return true;
        }
        return 종류 == 0x0800 && saada_pilvi_paketti(kuva_INDEKSI, 14);
    }

    private boolean saada_pilvi_paketti(byte[] data, int Suorita_2) {
        if (!verkko_Työkalut.tietojärjestelmät_IPV_4_protokolla(data, Suorita_2)) {
            return false;
        }
        int otsikko_kesto = (data[Suorita_2] & 0x0f) * 4;
        int summa_kesto = verkko_Työkalut.큰순서짧은정수(data, Suorita_2 + 2);
        if (summa_kesto < otsikko_kesto || Suorita_2 + summa_kesto > data.length) {
            return false;
        }
        int sopimuksen_arvo = data[Suorita_2 + 9] & 0xff;
        int Sisältö_alku = Suorita_2 + otsikko_kesto;
        int Sisältö_kesto = summa_kesto - otsikko_kesto;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(sopimuksen_arvo));
        if (직접처리기 != null) {
            직접처리기.prosessi_ARVO_merkintä(data, Sisältö_alku, Sisältö_kesto);
            return true;
        }
        if (Sisältö_kesto < 4) {
            return false;
        }
        int kohde_portin_numero = verkko_Työkalut.큰순서짧은정수(data, Sisältö_alku + 2);
        Map<Integer, 자료처리기> portti_taulukko = sopimuksen_arvo == 17 ? 사용자자료단위처리기 : sopimuksen_arvo == 6 ? 전송제어처리기 : null;
        if (portti_taulukko == null) {
            return false;
        }
        자료처리기 포트처리기 = portti_taulukko.get(Integer.valueOf(kohde_portin_numero));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.prosessi_ARVO_merkintä(data, Sisältö_alku, Sisältö_kesto);
        return true;
    }
}

