// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;

/** αυτοδύναμο_πακέτο(電文)·Κανάλι_καταχώρηση(通路): 경계를 가진 UDP 자료를 주고받는 τελικό_σημείο. */
public final class αυτοδύναμο_πακέτο_Κανάλι {
    private final java.net.DatagramSocket 표준종단;
    private αυτοδύναμο_πακέτο_Κανάλι(int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { 표준종단 = 통신.Άνοιγμα(αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public static αυτοδύναμο_πακέτο_Κανάλι Άνοιγμα(int αριθμός_θύρας) throws είσοδος_έξοδος_εξαίρεση {
        try { return new αυτοδύναμο_πακέτο_Κανάλι(αριθμός_θύρας);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void στέλνω(String διεύθυνση, int αριθμός_θύρας, String δεδομένα) throws είσοδος_έξοδος_εξαίρεση {
        try { 통신.στέλνω(표준종단, διεύθυνση, αριθμός_θύρας, δεδομένα);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public String λαμβάνω() throws είσοδος_έξοδος_εξαίρεση {
        try { return 통신.λαμβάνω(표준종단);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public void ΤΕΛΟΣ_ΧΡΟΝΟΥ(int 밀리초) throws είσοδος_έξοδος_εξαίρεση {
        try { 통신.ΤΕΛΟΣ_ΧΡΟΝΟΥ(표준종단, 밀리초);
        } catch (java.io.IOException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.είσοδος_έξοδος(ΣΦΑΛΜΑ); }
        catch (RuntimeException ΣΦΑΛΜΑ) { throw μετατρέπω_εξαίρεση.εκτελώ_εντολή(ΣΦΑΛΜΑ); }
    }
    public int αριθμός_θύρας() { return 표준종단.getLocalPort(); }
    public boolean πληροφοριακά_συστήματα_κλειστή() { return 표준종단.isClosed(); }
    public void Κλείσιμο() { 통신.Κλείσιμο(표준종단); }
}
