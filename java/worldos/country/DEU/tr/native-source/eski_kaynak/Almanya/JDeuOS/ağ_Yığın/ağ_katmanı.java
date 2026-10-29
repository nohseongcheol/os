// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Almanya.JDeuOS.ağ_Yığın;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP almak_değer 분배를 한곳에서 관리한다. */
public final class ağ_katmanı {
    @FunctionalInterface
    public interface veri_işleyici {
        void işlem_değer_girdi(byte[] veri, int çalıştır, int süre_değer);
    }

    private final Map<Integer, veri_işleyici> Ethernet_işleyici = new HashMap<Integer, veri_işleyici>();
    private final Map<Integer, veri_işleyici> IP_işleyici = new HashMap<Integer, veri_işleyici>();
    private final Map<Integer, veri_işleyici> kullanıcı_veri_ders_işleyici = new HashMap<Integer, veri_işleyici>();
    private final Map<Integer, veri_işleyici> 전송제어처리기 = new HashMap<Integer, veri_işleyici>();

    public void yazmaç_Ethernet(int Tip_değer, veri_işleyici işleyici) {
        Ethernet_işleyici.put(Integer.valueOf(Tip_değer & 0xffff), işleyici);
    }

    public void yazmaç_IP(int sözleşme_değeri, veri_işleyici işleyici) {
        IP_işleyici.put(Integer.valueOf(sözleşme_değeri & 0xff), işleyici);
    }

    public void yazmaç_kullanıcı_veri_ders(int donanım_taşımak, veri_işleyici işleyici) {
        kullanıcı_veri_ders_işleyici.put(Integer.valueOf(donanım_taşımak & 0xffff), işleyici);
    }

    public void 전송제어등록(int donanım_taşımak, veri_işleyici işleyici) {
        전송제어처리기.put(Integer.valueOf(donanım_taşımak & 0xffff), işleyici);
    }

    public boolean almak_Ethernet(byte[] kare_Dizin) {
        if (!ağ_Araçlar.bilgi_teknolojisi_Ethernet_kare(kare_Dizin)) {
            return false;
        }
        int Tip_değer = ağ_Araçlar.Ethernet_BÜYÜKHARF_protokol(kare_Dizin);
        veri_işleyici 직접처리기 = Ethernet_işleyici.get(Integer.valueOf(Tip_değer));
        if (직접처리기 != null) {
            직접처리기.işlem_değer_girdi(kare_Dizin, 14, kare_Dizin.length - 14);
            return true;
        }
        return Tip_değer == 0x0800 && almak_bulut_paket(kare_Dizin, 14);
    }

    private boolean almak_bulut_paket(byte[] veri, int çalıştır) {
        if (!ağ_Araçlar.bilgi_teknolojisi_FFF_4_protokol(veri, çalıştır)) {
            return false;
        }
        int Başlık_süre = (veri[çalıştır] & 0x0f) * 4;
        int toplam_süre = ağ_Araçlar.큰순서짧은정수(veri, çalıştır + 2);
        if (toplam_süre < Başlık_süre || çalıştır + toplam_süre > veri.length) {
            return false;
        }
        int sözleşme_değeri = veri[çalıştır + 9] & 0xff;
        int içerik_Start = çalıştır + Başlık_süre;
        int içerik_süre = toplam_süre - Başlık_süre;
        veri_işleyici 직접처리기 = IP_işleyici.get(Integer.valueOf(sözleşme_değeri));
        if (직접처리기 != null) {
            직접처리기.işlem_değer_girdi(veri, içerik_Start, içerik_süre);
            return true;
        }
        if (içerik_süre < 4) {
            return false;
        }
        int hedef_bağlantı_noktası_numarası = ağ_Araçlar.큰순서짧은정수(veri, içerik_Start + 2);
        Map<Integer, veri_işleyici> taşımak_tablo = sözleşme_değeri == 17 ? kullanıcı_veri_ders_işleyici : sözleşme_değeri == 6 ? 전송제어처리기 : null;
        if (taşımak_tablo == null) {
            return false;
        }
        veri_işleyici taşımak_işleyici = taşımak_tablo.get(Integer.valueOf(hedef_bağlantı_noktası_numarası));
        if (taşımak_işleyici == null) {
            return false;
        }
        taşımak_işleyici.işlem_değer_girdi(veri, içerik_Start, içerik_süre);
        return true;
    }
}

