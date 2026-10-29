// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** είσοδος_τιμή(入力)과 ροή_τιμή: 순서대로 들어오는 바이트를 읽는 Κανάλι_καταχώρηση. */
public final class ροή_εισόδου {
    private final java.io.InputStream 표준흐름;
    ροή_εισόδου(java.io.InputStream 표준흐름) { this.표준흐름 = 표준흐름; }
    public int Ανάγνωση() throws είσοδος_έξοδος_εξαίρεση {
        try { return 표준흐름.read();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public int Ανάγνωση(byte[] δεδομένα) throws είσοδος_έξοδος_εξαίρεση {
        try { return 표준흐름.read(δεδομένα);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public int Ανάγνωση(byte[] δεδομένα, int Εκτέλεση_2, int διάρκεια_τιμή) throws είσοδος_έξοδος_εξαίρεση {
        try { return 표준흐름.read(δεδομένα, Εκτέλεση_2, διάρκεια_τιμή);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void Κλείσιμο() throws είσοδος_έξοδος_εξαίρεση {
        try { 표준흐름.close();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
