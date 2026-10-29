// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Γερμανία.JDeuOS.σύστημα_αρχείων;

import java.util.HashMap;
import java.util.Map;

/** 과정마다 독립적인 서술자와 공유 가능한 열린 Αρχείο 설명을 유지한다. */
public final class 파일서술자표 {
    private static final int 최대서술자 = 32;

    private static final class 서술자 {
        private final σύστημα_αρχείων.열린파일 열린파일;
        private boolean 실행시닫기;

        서술자(σύστημα_αρχείων.열린파일 열린파일) {
            this.열린파일 = 열린파일;
        }
    }

    private final σύστημα_αρχείων σύστημα_αρχείων;
    private final Map<Integer, 서술자> 서술자들 = new HashMap<Integer, 서술자>();

    public 파일서술자표(σύστημα_αρχείων σύστημα_αρχείων) {
        this.σύστημα_αρχείων = σύστημα_αρχείων;
    }

    public int Άνοιγμα(String Όνομα) {
        σύστημα_αρχείων.열린파일 열린파일 = σύστημα_αρχείων.Άνοιγμα(Όνομα);
        if (열린파일 == null) {
            return -2;
        }
        int Ευρετήριο = 빈번호(3);
        if (Ευρετήριο < 0) {
            return -24;
        }
        서술자들.put(Integer.valueOf(Ευρετήριο), new 서술자(열린파일));
        return Ευρετήριο;
    }

    public int Ανάγνωση(int Ευρετήριο, byte[] λαμβάνω_προορισμός, int Μέγεθος) {
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        if (Μέγεθος < 0 || Μέγεθος > λαμβάνω_προορισμός.length) {
            return -22;
        }
        int 남음 = καταχώρηση_τιμή.열린파일.δεδομένα.length - καταχώρηση_τιμή.열린파일.Θέση;
        int 읽을크기 = Math.min(Μέγεθος, Math.max(남음, 0));
        System.arraycopy(καταχώρηση_τιμή.열린파일.δεδομένα, καταχώρηση_τιμή.열린파일.Θέση, λαμβάνω_προορισμός, 0, 읽을크기);
        καταχώρηση_τιμή.열린파일.Θέση += 읽을크기;
        return 읽을크기;
    }

    public int μετακινώ_θέση(int Ευρετήριο, int 거리, int έργο_ρίζα) {
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        int φόντο_τιμή;
        if (έργο_ρίζα == 0) {
            φόντο_τιμή = 0;
        } else if (έργο_ρίζα == 1) {
            φόντο_τιμή = καταχώρηση_τιμή.열린파일.Θέση;
        } else if (έργο_ρίζα == 2) {
            φόντο_τιμή = καταχώρηση_τιμή.열린파일.δεδομένα.length;
        } else {
            return -22;
        }
        int 새위치 = φόντο_τιμή + 거리;
        if (새위치 < 0) {
            return -22;
        }
        καταχώρηση_τιμή.열린파일.Θέση = 새위치;
        return 새위치;
    }

    public int Κλείσιμο(int Ευρετήριο) {
        서술자 καταχώρηση_τιμή = 서술자들.remove(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        καταχώρηση_τιμή.열린파일.참조수--;
        return 0;
    }

    public int 복제서술자(int Ευρετήριο, int 최소번호) {
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        int Νέος_αριθμός = 빈번호(최소번호);
        if (Νέος_αριθμός < 0) {
            return -24;
        }
        καταχώρηση_τιμή.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Νέος_αριθμός), new 서술자(καταχώρηση_τιμή.열린파일));
        return Νέος_αριθμός;
    }

    public int 지정복제(int Ευρετήριο, int Νέος_αριθμός) {
        if (Ευρετήριο == Νέος_αριθμός) {
            return 서술자들.containsKey(Integer.valueOf(Ευρετήριο)) ? Ευρετήριο : -9;
        }
        if (Νέος_αριθμός < 0 || Νέος_αριθμός >= 최대서술자) {
            return -9;
        }
        서술자 원본 = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (원본 == null) {
            return -9;
        }
        if (서술자들.containsKey(Integer.valueOf(Νέος_αριθμός))) {
            Κλείσιμο(Νέος_αριθμός);
        }
        원본.열린파일.참조수++;
        서술자들.put(Integer.valueOf(Νέος_αριθμός), new 서술자(원본.열린파일));
        return Νέος_αριθμός;
    }

    public int 실행시닫기설정(int Ευρετήριο, boolean τιμή) {
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        καταχώρηση_τιμή.실행시닫기 = τιμή;
        return 0;
    }

    public int 실행시닫기값(int Ευρετήριο) {
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return -9;
        }
        return καταχώρηση_τιμή.실행시닫기 ? 1 : 0;
    }

    public Αρχείο_πληροφορία Πληροφορίες_συστήματος(int Ευρετήριο) {
        if (Ευρετήριο >= 0 && Ευρετήριο <= 2) {
            return new Αρχείο_πληροφορία(0, 0020666);
        }
        서술자 καταχώρηση_τιμή = 서술자들.get(Integer.valueOf(Ευρετήριο));
        if (καταχώρηση_τιμή == null) {
            return null;
        }
        return new Αρχείο_πληροφορία(καταχώρηση_τιμή.열린파일.δεδομένα.length, 0100444);
    }

    public void 실행시닫기() {
        Integer[] 번호들 = 서술자들.keySet().toArray(new Integer[0]);
        for (Integer Ευρετήριο : 번호들) {
            서술자 καταχώρηση_τιμή = 서술자들.get(Ευρετήριο);
            if (καταχώρηση_τιμή != null && καταχώρηση_τιμή.실행시닫기) {
                Κλείσιμο(Ευρετήριο.intValue());
            }
        }
    }

    public boolean πληροφοριακά_συστήματα_ανοίγω(int Ευρετήριο) {
        return 서술자들.containsKey(Integer.valueOf(Ευρετήριο));
    }

    public 파일서술자표 κλώνος_τιμή() {
        파일서술자표 μέτρηση = new 파일서술자표(σύστημα_αρχείων);
        for (Map.Entry<Integer, 서술자> καταχώρηση_τιμή : 서술자들.entrySet()) {
            καταχώρηση_τιμή.getValue().열린파일.참조수++;
            서술자 새서술자 = new 서술자(καταχώρηση_τιμή.getValue().열린파일);
            새서술자.실행시닫기 = καταχώρηση_τιμή.getValue().실행시닫기;
            μέτρηση.서술자들.put(καταχώρηση_τιμή.getKey(), 새서술자);
        }
        return μέτρηση;
    }

    private int 빈번호(int 최소번호) {
        for (int Ευρετήριο = Math.max(0, 최소번호); Ευρετήριο < 최대서술자; Ευρετήριο++) {
            if (!서술자들.containsKey(Integer.valueOf(Ευρετήριο))) {
                return Ευρετήριο;
            }
        }
        return -1;
    }
}
