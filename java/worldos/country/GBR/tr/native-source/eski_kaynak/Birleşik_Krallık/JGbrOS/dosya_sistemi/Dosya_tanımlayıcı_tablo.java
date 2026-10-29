// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Birleşik_Krallık.JGbrOS.dosya_sistemi;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 dosya 설명을 유지한다. */
public final class Dosya_tanımlayıcı_tablo {
    private static final int 최대서술자 = 32;

    private static final class tanımlayıcı_girdi {
        private final dosya_sistemi.열린파일 열린파일;
        private boolean 실행시닫기;

        tanımlayıcı_girdi(dosya_sistemi.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final dosya_sistemi dosya_sistemi;
    private final Map<Integer, tanımlayıcı_girdi> 서술자들 = new HashMap<Integer, tanımlayıcı_girdi>();

    public Dosya_tanımlayıcı_tablo(dosya_sistemi dosya_sistemi) {
        this.dosya_sistemi = dosya_sistemi;
    }

    public int Aç(String İsim) {
        dosya_sistemi.열린파일 열린파일 = dosya_sistemi.Aç(İsim);
        if (열린파일 == null) {
            return -2;
        }
        int Dizin = boş_Dizin(3);
        if (Dizin < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(Dizin), new tanımlayıcı_girdi(열린파일));
        return Dizin;
    }

    public int Okuma(int Dizin, byte[] almak_hedef, int Boyut) {
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        if (Boyut < 0 || Boyut > almak_hedef.length) {
            return -22;
        }
        int 남음 = girdi_değer.열린파일.veri.length - girdi_değer.열린파일.konum;
        int 읽을크기 = Math.min(Boyut, Math.max(남음, 0));
        System.arraycopy(girdi_değer.열린파일.veri, girdi_değer.열린파일.konum, almak_hedef, 0, 읽을크기);
        girdi_değer.열린파일.konum += 읽을크기;
        return 읽을크기;
    }

    public int taşımak_konum(int Dizin, int 거리, int işlem_kök) {
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        int Arka_Plan_değer;
        if (işlem_kök == 0) {
            Arka_Plan_değer = 0;
        } else if (işlem_kök == 1) {
            Arka_Plan_değer = girdi_değer.열린파일.konum;
        } else if (işlem_kök == 2) {
            Arka_Plan_değer = girdi_değer.열린파일.veri.length;
        } else {
            return -22;
        }
        int 새위치 = Arka_Plan_değer + 거리;
        if (새위치 < 0) {
            return -22;
        }
        girdi_değer.열린파일.konum = 새위치;
        return 새위치;
    }

    public int Kapat(int Dizin) {
        tanımlayıcı_girdi girdi_değer = 서술자들.remove(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        girdi_değer.열린파일.Başvuru_BAĞ_DEĞ_SAY--;
        return 0;
    }

    public int 복제서술자(int Dizin, int 최소번호) {
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        int Yeni_Numara = boş_Dizin(최소번호);
        if (Yeni_Numara < 0) {
            return -24;
        }
        girdi_değer.열린파일.Başvuru_BAĞ_DEĞ_SAY++;
        서술자들.put(Integer.valueOf(Yeni_Numara), new tanımlayıcı_girdi(girdi_değer.열린파일));
        return Yeni_Numara;
    }

    public int 지정복제(int Dizin, int Yeni_Numara) {
        if (Dizin == Yeni_Numara) {
            return 서술자들.containsKey(Integer.valueOf(Dizin)) ? Dizin : -9;
        }
        if (Yeni_Numara < 0 || Yeni_Numara >= 최대서술자) {
            return -9;
        }
        tanımlayıcı_girdi 원본 = 서술자들.get(Integer.valueOf(Dizin));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Yeni_Numara))) {
            Kapat(Yeni_Numara);
        }
        원본.열린파일.Başvuru_BAĞ_DEĞ_SAY++;
        서술자들.put(Integer.valueOf(Yeni_Numara), new tanımlayıcı_girdi(원본.열린파일));
        return Yeni_Numara;
    }

    public int 실행시닫기설정(int Dizin, boolean değer) {
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        girdi_değer.실행시닫기 = değer;
        return 0;
    }

    public int 실행시닫기값(int Dizin) {
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return -9;
        }
        return girdi_değer.실행시닫기 ? 1 : 0;
    }

    public Dosya_bilgi msinfo32_exe(int Dizin) {
        if (Dizin >= 0 && Dizin <= 2) {
            return new Dosya_bilgi(0, 0020666);
        }
        tanımlayıcı_girdi girdi_değer = 서술자들.get(Integer.valueOf(Dizin));
        if (girdi_değer == null) {
            return null;
        }
        return new Dosya_bilgi(girdi_değer.열린파일.veri.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer Dizin : 번호들) {
            tanımlayıcı_girdi girdi_değer = 서술자들.get(Dizin);
            if (girdi_değer != null && girdi_değer.실행시닫기) {
                Kapat(Dizin.intValue());
            }
        }
    }

    public boolean bilgi_teknolojisi_açık(int Dizin) {
        return 서술자들.containsKey(Integer.valueOf(Dizin));
    }

    public Dosya_tanımlayıcı_tablo kopya_değer() {
        Dosya_tanımlayıcı_tablo sonuç = new Dosya_tanımlayıcı_tablo(dosya_sistemi);
        for (Map.Entry<Integer, tanımlayıcı_girdi> girdi_değer : 서술자들.entrySet()) {
            girdi_değer.getValue().열린파일.Başvuru_BAĞ_DEĞ_SAY++;
            tanımlayıcı_girdi 새서술자 = new tanımlayıcı_girdi(girdi_değer.getValue().열린파일);
            새서술자.실행시닫기 = girdi_değer.getValue().실행시닫기;
            sonuç.서술자들.put(girdi_değer.getKey(), 새서술자);
        }
        return sonuç;
    }

    private int boş_Dizin(int 최소번호) {
        for (int Dizin = Math.max(0, 최소번호); Dizin < 최대서술자; Dizin++) {
            if (!서술자들.containsKey(Integer.valueOf(Dizin))) {
                return Dizin;
            }
        }
        return -1;
    }
}
