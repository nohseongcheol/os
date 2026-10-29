// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
import java.util.HashMap;
/** λεξικό(辭典): 찾는 λέξη_μήνυμα(열쇠)에 값을 대응시킨다. */
public final class λεξικό {
    private final HashMap<String, String> καταχώρηση_τιμή = new HashMap<String, String>();
    public String 넣기(String 열쇠, String τιμή) { return καταχώρηση_τιμή.put(열쇠, τιμή); }
    public String Βρες_καταχώρηση(String 열쇠) { return καταχώρηση_τιμή.get(열쇠); }
    public boolean 있는가(String 열쇠) { return καταχώρηση_τιμή.containsKey(열쇠); }
    public String διαγράφω_καταχώρηση(String 열쇠) { return καταχώρηση_τιμή.remove(열쇠); }
    public int Μέγεθος() { return καταχώρηση_τιμή.size(); }
    public void εκκαθαρίζω_Περιεχόμενα() { καταχώρηση_τιμή.clear(); }
}
