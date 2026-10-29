// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** Σύνδεση(連結)·Κανάλι_καταχώρηση(通路): 상대와 이어진 TCP 바이트 흐름의 τελικό_σημείο. */
public final class σύνδεση {
    private final java.net.Socket 표준연결;
    σύνδεση(java.net.Socket 표준연결) { this.표준연결 = 표준연결; }
    public static σύνδεση Άνοιγμα(String διεύθυνση, int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try {
            return new σύνδεση(new java.net.Socket(διεύθυνση, αριθμός_θύρας));
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public ροή_εισόδου είσοδος_τιμή() throws είσοδος_έξοδος_εξαίρεση {
        try { return new ροή_εισόδου(표준연결.getInputStream());
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public ροή_εξόδου Έξοδος() throws είσοδος_έξοδος_εξαίρεση {
        try { return new ροή_εξόδου(표준연결.getOutputStream());
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void ΤΕΛΟΣ_ΧΡΟΝΟΥ(int 밀리초) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준연결.setSoTimeout(밀리초);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public int αριθμός_θύρας() { return 표준연결.getPort(); }
    public int τοπικός_αριθμός_θύρας() { return 표준연결.getLocalPort(); }
    public boolean πληροφοριακά_συστήματα_κλειστή() { return 표준연결.isClosed(); }
    public boolean 연결됨() { return 표준연결.isConnected(); }
    public void Κλείσιμο() throws είσοδος_έξοδος_εξαίρεση {
        try { 표준연결.close();
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
}
