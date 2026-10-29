// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bulgaristan.JBgrOS.ağ_Yığın;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 bayt_değer 순서와 sağlama_toplamı 도구다. */
public final class ağ_Araçlar {
    private ağ_Araçlar() {
    }

    public static int 큰순서짧은정수(byte[] veri, int konum) {
        çek_aralık(veri, konum, 2);
        return ((veri[konum] & 0xff) << 8) | (veri[konum + 1] & 0xff);
    }

    public static long big_endian_bilgi(byte[] veri, int konum) {
        çek_aralık(veri, konum, 4);
        return ((long) (veri[konum] & 0xff) << 24)
                | ((long) (veri[konum + 1] & 0xff) << 16)
                | ((long) (veri[konum + 2] & 0xff) << 8)
                | (veri[konum + 3] & 0xffL);
    }

    public static int bulut_sağlama_toplamı(byte[] veri, int çalıştır, int süre_değer) {
        çek_aralık(veri, çalıştır, süre_değer);
        long SUM_değer = 0;
        int 끝 = çalıştır + süre_değer;
        int konum = çalıştır;
        while (konum + 1 < 끝) {
            SUM_değer += 큰순서짧은정수(veri, konum);
            konum += 2;
        }
        if (konum < 끝) {
            SUM_değer += (veri[konum] & 0xff) << 8;
        }
        while ((SUM_değer >>> 16) != 0) {
            SUM_değer = (SUM_değer & 0xffff) + (SUM_değer >>> 16);
        }
        return (int) (~SUM_değer) & 0xffff;
    }

    public static boolean bilgi_teknolojisi_Ethernet_kare(byte[] veri) {
        return veri != null && veri.length >= 14;
    }

    public static int Ethernet_BÜYÜKHARF_protokol(byte[] veri) {
        if (!bilgi_teknolojisi_Ethernet_kare(veri)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(veri, 12);
    }

    public static boolean bilgi_teknolojisi_FFF_4_protokol(byte[] veri, int konum) {
        if (veri == null || konum < 0 || veri.length - konum < 20) {
            return false;
        }
        int sürüm_değer = (veri[konum] >>> 4) & 0xf;
        int Başlık_süre = (veri[konum] & 0xf) * 4;
        return sürüm_değer == 4 && Başlık_süre >= 20 && veri.length - konum >= Başlık_süre;
    }

    private static void çek_aralık(byte[] veri, int çalıştır, int süre_değer) {
        if (veri == null || çalıştır < 0 || süre_değer < 0 || çalıştır > veri.length - süre_değer) {
            throw new IllegalArgumentException("ağ_Yığın veri 범위를 벗어났습니다.");
        }
    }
}

