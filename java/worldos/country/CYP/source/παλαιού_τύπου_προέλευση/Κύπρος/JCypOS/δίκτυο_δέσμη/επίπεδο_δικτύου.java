// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Κύπρος.JCypOS.δίκτυο_δέσμη;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP λαμβάνω_τιμή_cef4d8ab 분배를 한곳에서 관리한다. */
public final class επίπεδο_δικτύου {
    @FunctionalInterface
    public interface 자료처리기 {
        void διεργασία_τιμή_καταχώρηση(byte[] δεδομένα, int Εκτέλεση_2, int διάρκεια_τιμή);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void δήλωση_πρωτόκολλο_Internet(int εργασία_τιμή, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(εργασία_τιμή & 0xff), 처리기);
    }

    public void δήλωση_χρήστης_δεδομένα_μάθημα(int υλικό_θύρα, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(υλικό_θύρα & 0xffff), 처리기);
    }

    public void 전송제어등록(int υλικό_θύρα, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(υλικό_θύρα & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] κάδρο_Ευρετήριο) {
        if (!δίκτυο_Εργαλεία.이더넷틀인가(κάδρο_Ευρετήριο)) {
            return false;
        }
        int 종류 = δίκτυο_Εργαλεία.이더넷상위규약(κάδρο_Ευρετήριο);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.διεργασία_τιμή_καταχώρηση(κάδρο_Ευρετήριο, 14, κάδρο_Ευρετήριο.length - 14);
            return true;
        }
        return 종류 == 0x0800 && λαμβάνω_πλέγμα_πακέτο(κάδρο_Ευρετήριο, 14);
    }

    private boolean λαμβάνω_πλέγμα_πακέτο(byte[] δεδομένα, int Εκτέλεση_2) {
        if (!δίκτυο_Εργαλεία.πληροφοριακά_συστήματα_εμβόλιο_πολιομυελίτιδας_4_πρωτόκολλο(δεδομένα, Εκτέλεση_2)) {
            return false;
        }
        int κεφαλίδα_διάρκεια = (δεδομένα[Εκτέλεση_2] & 0x0f) * 4;
        int σύνολο_διάρκεια_ff8eaa6c = δίκτυο_Εργαλεία.큰순서짧은정수(δεδομένα, Εκτέλεση_2 + 2);
        if (σύνολο_διάρκεια_ff8eaa6c < κεφαλίδα_διάρκεια || Εκτέλεση_2 + σύνολο_διάρκεια_ff8eaa6c > δεδομένα.length) {
            return false;
        }
        int εργασία_τιμή = δεδομένα[Εκτέλεση_2 + 9] & 0xff;
        int Περιεχόμενο_αρχή = Εκτέλεση_2 + κεφαλίδα_διάρκεια;
        int Περιεχόμενο_διάρκεια = σύνολο_διάρκεια_ff8eaa6c - κεφαλίδα_διάρκεια;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(εργασία_τιμή));
        if (직접처리기 != null) {
            직접처리기.διεργασία_τιμή_καταχώρηση(δεδομένα, Περιεχόμενο_αρχή, Περιεχόμενο_διάρκεια);
            return true;
        }
        if (Περιεχόμενο_διάρκεια < 4) {
            return false;
        }
        int προορισμός_αριθμός_θύρας = δίκτυο_Εργαλεία.큰순서짧은정수(δεδομένα, Περιεχόμενο_αρχή + 2);
        Map<Integer, 자료처리기> θύρα_πίνακας = εργασία_τιμή == 17 ? 사용자자료단위처리기 : εργασία_τιμή == 6 ? 전송제어처리기 : null;
        if (θύρα_πίνακας == null) {
            return false;
        }
        자료처리기 포트처리기 = θύρα_πίνακας.get(Integer.valueOf(προορισμός_αριθμός_θύρας));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.διεργασία_τιμή_καταχώρηση(δεδομένα, Περιεχόμενο_αρχή, Περιεχόμενο_διάρκεια);
        return true;
    }
}

