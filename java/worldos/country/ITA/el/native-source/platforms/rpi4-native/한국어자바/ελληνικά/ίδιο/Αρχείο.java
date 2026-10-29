// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 χρήστης 용어를 보존한다. τρέχων_στοιχείο 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class Αρχείο {
    private Αρχείο() {}
    public static byte[] 바이트읽기(String Όνομα) throws είσοδος_έξοδος_εξαίρεση {
        try {
        FileInputStream ροή_τιμή = new FileInputStream(Όνομα);
        try {
            byte[] 임시 = new byte[16384]; int 수 = 0, τιμή;
            while ((τιμή = ροή_τιμή.read()) != -1) { if (수 == 임시.length) throw new είσοδος_έξοδος_εξαίρεση("Αρχείο Μέγεθος 제한"); 임시[수++] = (byte)τιμή; }
            byte[] μέτρηση = new byte[수]; System.arraycopy(임시, 0, μέτρηση, 0, 수); return μέτρηση;
        } finally { ροή_τιμή.close(); }
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void 바이트쓰기(String Όνομα, byte[] Περιεχόμενο_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try {
        FileOutputStream ροή_τιμή = new FileOutputStream(Όνομα);
        try { for (int βρόχος_Ευρετήριο = 0; βρόχος_Ευρετήριο < Περιεχόμενο_τιμή.length; βρόχος_Ευρετήριο++) ροή_τιμή.write(Περιεχόμενο_τιμή[βρόχος_Ευρετήριο] & 255); } finally { ροή_τιμή.close(); }
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static String Ανάγνωση(String Όνομα) throws είσοδος_έξοδος_εξαίρεση {
        try { return 문자.αποκρυπτογραφώ_δεδομένα(바이트읽기(Όνομα));
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static void Εγγραφή(String Όνομα, String Περιεχόμενο_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { 바이트쓰기(Όνομα, 문자.κωδικοποιώ(Περιεχόμενο_τιμή));
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
