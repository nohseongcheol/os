// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** Έξοδος(出力)과 ροή_τιμή: 순서를 보존해 내보내는 바이트의 Κανάλι_καταχώρηση. */
public final class ροή_εξόδου {
    private final java.io.OutputStream 표준흐름;
    ροή_εξόδου(java.io.OutputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public void Εγγραφή(int τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.write(τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void Εγγραφή(byte[] δεδομένα) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.write(δεδομένα);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void Εγγραφή(byte[] δεδομένα, int Εκτέλεση_2, int διάρκεια_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.write(δεδομένα, Εκτέλεση_2, διάρκεια_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void 내보내기() throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.flush();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void Κλείσιμο() throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.close();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
