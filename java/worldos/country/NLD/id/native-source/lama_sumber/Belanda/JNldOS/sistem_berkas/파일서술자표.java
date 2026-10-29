// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.sistem_berkas;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 berkas 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final sistem_berkas.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(sistem_berkas.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final sistem_berkas sistem_berkas;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(sistem_berkas sistem_berkas) {
        this.sistem_berkas = sistem_berkas;
    }

    public int Buka(String Nama_2) {
        sistem_berkas.열린파일 열린파일 = sistem_berkas.Buka(Nama_2);
        if (열린파일 == null) {
            return -2;
        }
        int INDEX = kosong_INDEX(3);
        if (INDEX < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(INDEX), new 서술자(열린파일));
        return INDEX;
    }

    public int Baca(int INDEX, byte[] terima_tujuan, int Ukuran) {
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        if (Ukuran < 0 || Ukuran > terima_tujuan.length) {
            return -22;
        }
        int 남음 = entri_VALUE.열린파일.data.length - entri_VALUE.열린파일.posisi;
        int 읽을크기 = Math.min(Ukuran, Math.max(남음, 0));
        System.arraycopy(entri_VALUE.열린파일.data, entri_VALUE.열린파일.posisi, terima_tujuan, 0, 읽을크기);
        entri_VALUE.열린파일.posisi += 읽을크기;
        return 읽을크기;
    }

    public int gerak_posisi(int INDEX, int 거리, int Tugas_akar) {
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        int wallpaper_VALUE;
        if (Tugas_akar == 0) {
            wallpaper_VALUE = 0;
        } else if (Tugas_akar == 1) {
            wallpaper_VALUE = entri_VALUE.열린파일.posisi;
        } else if (Tugas_akar == 2) {
            wallpaper_VALUE = entri_VALUE.열린파일.data.length;
        } else {
            return -22;
        }
        int 새위치 = wallpaper_VALUE + 거리;
        if (새위치 < 0) {
            return -22;
        }
        entri_VALUE.열린파일.posisi = 새위치;
        return 새위치;
    }

    public int Tutup(int INDEX) {
        서술자 entri_VALUE = 서술자들.remove(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        entri_VALUE.열린파일.Referensi_COUNT--;
        return 0;
    }

    public int 복제서술자(int INDEX, int 최소번호) {
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        int 새번호 = kosong_INDEX(최소번호);
        if (새번호 < 0) {
            return -24;
        }
        entri_VALUE.열린파일.Referensi_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(entri_VALUE.열린파일));
        return 새번호;
    }

    public int 지정복제(int INDEX, int 새번호) {
        if (INDEX == 새번호) {
            return 서술자들.containsKey(Integer.valueOf(INDEX)) ? INDEX : -9;
        }
        if (새번호 < 0 || 새번호 >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(INDEX));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(새번호))) {
            Tutup(새번호);
        }
        원본.열린파일.Referensi_COUNT++;
        서술자들.put(Integer.valueOf(새번호), new 서술자(원본.열린파일));
        return 새번호;
    }

    public int 실행시닫기설정(int INDEX, boolean VALUE) {
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        entri_VALUE.실행시닫기 = VALUE;
        return 0;
    }

    public int 실행시닫기값(int INDEX) {
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return -9;
        }
        return entri_VALUE.실행시닫기 ? 1 : 0;
    }

    public file_info msinfo32_exe(int INDEX) {
        if (INDEX >= 0 && INDEX <= 2) {
            return new file_info(0, 0020666);
        }
        서술자 entri_VALUE = 서술자들.get(Integer.valueOf(INDEX));
        if (entri_VALUE == null) {
            return null;
        }
        return new file_info(entri_VALUE.열린파일.data.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer INDEX : 번호들) {
            서술자 entri_VALUE = 서술자들.get(INDEX);
            if (entri_VALUE != null && entri_VALUE.실행시닫기) {
                Tutup(INDEX.intValue());
            }
        }
    }

    public boolean teknologi_informasi_buat(int INDEX) {
        return 서술자들.containsKey(Integer.valueOf(INDEX));
    }

    public 파일서술자표 klon_VALUE() {
        파일서술자표 hasil = new 파일서술자표(sistem_berkas);
        for (Map.Entry<Integer, 서술자> entri_VALUE : 서술자들.entrySet()) {
            entri_VALUE.getValue().열린파일.Referensi_COUNT++;
            서술자 새서술자 = new 서술자(entri_VALUE.getValue().열린파일);
            새서술자.실행시닫기 = entri_VALUE.getValue().실행시닫기;
            hasil.서술자들.put(entri_VALUE.getKey(), 새서술자);
        }
        return hasil;
    }

    private int kosong_INDEX(int 최소번호) {
        for (int INDEX = Math.max(0, 최소번호); INDEX < 최대서술자; INDEX++) {
            if (!서술자들.containsKey(Integer.valueOf(INDEX))) {
                return INDEX;
            }
        }
        return -1;
    }
}
