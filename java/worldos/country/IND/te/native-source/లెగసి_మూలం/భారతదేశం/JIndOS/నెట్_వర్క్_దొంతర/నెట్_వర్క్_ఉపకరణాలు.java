// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.నెట్_వర్క్_దొంతర;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 బైట్_మూల్యం 순서와 검사합 도구다. */
public final class నెట్_వర్క్_ఉపకరణాలు {
    private నెట్_వర్క్_ఉపకరణాలు() {
    }

    public static int 큰순서짧은정수(byte[] డేటా, int స్థానము) {
        범위확인(డేటా, స్థానము, 2);
        return ((డేటా[స్థానము] & 0xff) << 8) | (డేటా[స్థానము + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] డేటా, int స్థానము) {
        범위확인(డేటా, స్థానము, 4);
        return ((long) (డేటా[స్థానము] & 0xff) << 24)
                | ((long) (డేటా[స్థానము + 1] & 0xff) << 16)
                | ((long) (డేటా[స్థానము + 2] & 0xff) << 8)
                | (డేటా[స్థానము + 3] & 0xffL);
    }

    public static int 인터넷검사합(byte[] డేటా, int నడుపుము, int పొడవు_మూల్యం) {
        범위확인(డేటా, నడుపుము, పొడవు_మూల్యం);
        long 합 = 0;
        int 끝 = నడుపుము + పొడవు_మూల్యం;
        int స్థానము = నడుపుము;
        while (స్థానము + 1 < 끝) {
            합 += 큰순서짧은정수(డేటా, స్థానము);
            స్థానము += 2;
        }
        if (స్థానము < 끝) {
            합 += (డేటా[స్థానము] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean సమాచార_టెక్నాలజీ_ఇథర్నెట్_చట్రం(byte[] డేటా) {
        return డేటా != null && డేటా.length >= 14;
    }

    public static int 이더넷상위규약(byte[] డేటా) {
        if (!సమాచార_టెక్నాలజీ_ఇథర్నెట్_చట్రం(డేటా)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(డేటా, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] డేటా, int స్థానము) {
        if (డేటా == null || స్థానము < 0 || డేటా.length - స్థానము < 20) {
            return false;
        }
        int సంస్కరణ_మూల్యం = (డేటా[స్థానము] >>> 4) & 0xf;
        int శీర్షిక_పొడవు = (డేటా[స్థానము] & 0xf) * 4;
        return సంస్కరణ_మూల్యం == 4 && శీర్షిక_పొడవు >= 20 && డేటా.length - స్థానము >= శీర్షిక_పొడవు;
    }

    private static void 범위확인(byte[] డేటా, int నడుపుము, int పొడవు_మూల్యం) {
        if (డేటా == null || నడుపుము < 0 || పొడవు_మూల్యం < 0 || నడుపుము > డేటా.length - పొడవు_మూల్యం) {
            throw new IllegalArgumentException("నెట్_వర్క్_దొంతర డేటా 범위를 벗어났습니다.");
        }
    }
}

