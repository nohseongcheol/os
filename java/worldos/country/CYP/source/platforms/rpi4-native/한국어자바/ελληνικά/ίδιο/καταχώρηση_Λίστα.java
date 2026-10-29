// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
import java.util.ArrayList;
/** καταχώρηση_Λίστα(目錄): 순서가 있는 항목의 모음. 이 판은 συμβολοσειρά_τιμή 목록을 제공한다. */
public final class καταχώρηση_Λίστα {
    private final ArrayList<String> καταχώρηση_τιμή = new ArrayList<String>();
    public void 더하기(String τιμή) { καταχώρηση_τιμή.add(τιμή); }
    public String Ανάγνωση(int σειρά_τιμή) { return καταχώρηση_τιμή.get(σειρά_τιμή); }
    public String αντικαθιστώ_τιμή(int σειρά_τιμή, String τιμή) { return καταχώρηση_τιμή.set(σειρά_τιμή, τιμή); }
    public String διαγράφω_καταχώρηση(int σειρά_τιμή) { return καταχώρηση_τιμή.remove(σειρά_τιμή); }
    public int Μέγεθος() { return καταχώρηση_τιμή.size(); }
    public boolean 비었는가() { return καταχώρηση_τιμή.isEmpty(); }
    public void εκκαθαρίζω_Περιεχόμενα() { καταχώρηση_τιμή.clear(); }
}
