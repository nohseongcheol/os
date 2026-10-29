// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** λαμβάνω_τιμή_cef4d8ab(受信)·θύρα_τιμή(窓口): 들어오는 TCP 연결을 받아들이는 곳. */
public final class λαμβάνω_θύρα {
    private final java.net.ServerSocket 표준창구;
    private λαμβάνω_θύρα(int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준창구 = new java.net.ServerSocket(αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static λαμβάνω_θύρα Άνοιγμα(int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { return new λαμβάνω_θύρα(αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public σύνδεση λαμβάνω() throws είσοδος_έξοδος_εξαίρεση {
        try { return new σύνδεση(표준창구.accept());
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public int αριθμός_θύρας() { return 표준창구.getLocalPort(); }
    public void ΤΕΛΟΣ_ΧΡΟΝΟΥ(int 밀리초) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준창구.setSoTimeout(밀리초);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public boolean πληροφοριακά_συστήματα_κλειστή() { return 표준창구.isClosed(); }
    public void Κλείσιμο() throws είσοδος_έξοδος_εξαίρεση {
        try { 표준창구.close();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
