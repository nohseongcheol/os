// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.oma.문자;
import suomi.oma.tiedoston_nimi;
import suomi.oma.merkintä_luettelo;
import suomi.oma.sanakirja;
import suomi.oma.tulostuspaikka;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        tulostuspaikka.kirjoitus_rivi(문자.pura_salaus_data(문자.koodata(인사))); tulostuspaikka.kirjoitus_numero(문자.koodipiste_LASKE("한글😀"));
        tiedoston_nimi.Kirjoitus("한글자료.txt", 인사); tulostuspaikka.kirjoitus_rivi(tiedoston_nimi.Luku("한글자료.txt"));
        merkintä_luettelo 이름들 = new merkintä_luettelo(); 이름들.더하기("가람"); 이름들.더하기("누리"); tulostuspaikka.kirjoitus_rivi(이름들.Luku(1));
        sanakirja 뜻 = new sanakirja(); 뜻.넣기("가람", "강"); System.gc(); tulostuspaikka.kirjoitus_rivi(뜻.ETSI_merkintä("가람"));
        try { 문자.pura_salaus_data(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { tulostuspaikka.kirjoitus_rivi("UTF-8 VIRHE hylkää_ARVO_e3ecc00b"); }
        tulostuspaikka.kirjoitus_rivi("suomi kirjasto 완료");
    }
}
