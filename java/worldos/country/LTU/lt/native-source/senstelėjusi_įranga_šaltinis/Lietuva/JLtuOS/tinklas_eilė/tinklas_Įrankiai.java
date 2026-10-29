// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lietuva.JLtuOS.tinklas_eilė;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 baitas_VALUE 순서와 kontrolinė_suma 도구다. */
public final class tinklas_Įrankiai {
    private tinklas_Įrankiai() {
    }

    public static int 큰순서짧은정수(byte[] duomenys, int Pozicija) {
        čekis_diapazonas(duomenys, Pozicija, 2);
        return ((duomenys[Pozicija] & 0xff) << 8) | (duomenys[Pozicija + 1] & 0xff);
    }

    public static long mažėjantys_baitai_sveikasis_skaičius(byte[] duomenys, int Pozicija) {
        čekis_diapazonas(duomenys, Pozicija, 4);
        return ((long) (duomenys[Pozicija] & 0xff) << 24)
                | ((long) (duomenys[Pozicija + 1] & 0xff) << 16)
                | ((long) (duomenys[Pozicija + 2] & 0xff) << 8)
                | (duomenys[Pozicija + 3] & 0xffL);
    }

    public static int debesis_kontrolinė_suma(byte[] duomenys, int Paleisti, int 길이) {
        čekis_diapazonas(duomenys, Paleisti, 길이);
        long SUM_VALUE = 0;
        int 끝 = Paleisti + 길이;
        int Pozicija = Paleisti;
        while (Pozicija + 1 < 끝) {
            SUM_VALUE += 큰순서짧은정수(duomenys, Pozicija);
            Pozicija += 2;
        }
        if (Pozicija < 끝) {
            SUM_VALUE += (duomenys[Pozicija] & 0xff) << 8;
        }
        while ((SUM_VALUE >>> 16) != 0) {
            SUM_VALUE = (SUM_VALUE & 0xffff) + (SUM_VALUE >>> 16);
        }
        return (int) (~SUM_VALUE) & 0xffff;
    }

    public static boolean informacinės_technologijos_eternetas_kadras(byte[] duomenys) {
        return duomenys != null && duomenys.length >= 14;
    }

    public static int eternetas_UPPER_protokolas(byte[] duomenys) {
        if (!informacinės_technologijos_eternetas_kadras(duomenys)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(duomenys, 12);
    }

    public static boolean informacinės_technologijos_SKN_4_protokolas(byte[] duomenys, int Pozicija) {
        if (duomenys == null || Pozicija < 0 || duomenys.length - Pozicija < 20) {
            return false;
        }
        int versija_VALUE = (duomenys[Pozicija] >>> 4) & 0xf;
        int 머리길이 = (duomenys[Pozicija] & 0xf) * 4;
        return versija_VALUE == 4 && 머리길이 >= 20 && duomenys.length - Pozicija >= 머리길이;
    }

    private static void čekis_diapazonas(byte[] duomenys, int Paleisti, int 길이) {
        if (duomenys == null || Paleisti < 0 || 길이 < 0 || Paleisti > duomenys.length - 길이) {
            throw new IllegalArgumentException("tinklas_eilė duomenys 범위를 벗어났습니다.");
        }
    }
}

