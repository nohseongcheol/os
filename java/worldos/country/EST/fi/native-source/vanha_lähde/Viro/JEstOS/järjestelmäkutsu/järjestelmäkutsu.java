// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Viro.JEstOS.järjestelmäkutsu;

import Viro.JEstOS.Muisti_alue.page_Valvoja;
import Viro.JEstOS.작업.prosessi_ARVO;
import Viro.JEstOS.작업.Aikataulutus;
import Viro.JEstOS.tiedostojärjestelmä.suoritettava_tiedosto_latausohjelma;
import Viro.JEstOS.tiedostojärjestelmä.tiedostojärjestelmä;
import Viro.JEstOS.tiedostojärjestelmä.Tiedosto_info;
import Viro.JEstOS.ydin.laitteisto_ARVO;
import Viro.JEstOS.syöte_ARVO.syöte_Valvoja;
import Viro.JEstOS.syöte_ARVO.syöte_tapahtuma;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class järjestelmäkutsu {
    public static final int vain_luku_merkitä = 0;
    public static final int Hae_alku = 0;
    public static final int Hae_nykyinen = 1;
    public static final int ETSI_merkintä_lopettaa_puhelu = 2;

    private final tiedostojärjestelmä tiedostojärjestelmä;
    private final page_Valvoja 쪽관리;
    private final Aikataulutus Aikataulutus;
    private final suoritettava_tiedosto_latausohjelma latausohjelma = new suoritettava_tiedosto_latausohjelma();
    private final laitteisto_ARVO laite_ARVO;
    private final syöte_Valvoja 입력관리;

    public järjestelmäkutsu(tiedostojärjestelmä tiedostojärjestelmä, page_Valvoja 쪽관리, Aikataulutus Aikataulutus, laitteisto_ARVO laite_ARVO, syöte_Valvoja 입력관리) {
        this.tiedostojärjestelmä = tiedostojärjestelmä;
        this.쪽관리 = 쪽관리;
        this.Aikataulutus = Aikataulutus;
        this.laite_ARVO = laite_ARVO;
        this.입력관리 = 입력관리;
    }

    public int prosessi_tunniste(prosessi_ARVO nykyinen_prosessi) {
        return nykyinen_prosessi.tunniste_ARVO();
    }

    public int pää_prosessi_tunniste(prosessi_ARVO nykyinen_prosessi) {
        return nykyinen_prosessi.pää_tunniste();
    }

    public int Avaa(prosessi_ARVO nykyinen_prosessi, String Nimi, int merkitä_ARVO) {
        if (merkitä_ARVO != vain_luku_merkitä) {
            return -30;
        }
        return nykyinen_prosessi.파일서술자().Avaa(Nimi);
    }

    public int Luku(prosessi_ARVO nykyinen_prosessi, int 서술자, byte[] saada_kohde, int Koko) {
        if (서술자 == 0) {
            if (Koko <= 0 || saada_kohde.length == 0) {
                return 0;
            }
            syöte_tapahtuma Tapahtuma = 입력관리.Seuraava_tapahtuma();
            if (Tapahtuma == null || Tapahtuma.tapahtumatyyppi() != syöte_tapahtuma.종류.Avain_ei_toiminnassa) {
                return -11;
            }
            saada_kohde[0] = (byte) Tapahtuma.첫째값();
            return 1;
        }
        return nykyinen_prosessi.파일서술자().Luku(서술자, saada_kohde, Koko);
    }

    public int Kirjoitus(prosessi_ARVO nykyinen_prosessi, int 서술자, byte[] data, int Koko) {
        if (서술자 != 1 && 서술자 != 2) {
            return nykyinen_prosessi.파일서술자().tietojärjestelmät_avata(서술자) ? -30 : -9;
        }
        if (Koko < 0 || Koko > data.length) {
            return -22;
        }
        laite_ARVO.직렬출력(new String(data, 0, Koko, java.nio.charset.StandardCharsets.UTF_8));
        return Koko;
    }

    public int Sulje(prosessi_ARVO nykyinen_prosessi, int 서술자) {
        return nykyinen_prosessi.파일서술자().Sulje(서술자);
    }

    public int siirrä_toimi(prosessi_ARVO nykyinen_prosessi, int 서술자, int 거리, int aloite_juuri) {
        return nykyinen_prosessi.파일서술자().siirrä_toimi(서술자, 거리, aloite_juuri);
    }

    public int 서술자복제(prosessi_ARVO nykyinen_prosessi, int 서술자) {
        return nykyinen_prosessi.파일서술자().복제서술자(서술자, 0);
    }

    public int 지정서술자복제(prosessi_ARVO nykyinen_prosessi, int 서술자, int 새서술자) {
        return nykyinen_prosessi.파일서술자().지정복제(서술자, 새서술자);
    }

    public int 접근가능(String Nimi, int menetelmä_tila) {
        Tiedosto_info msinfo32_exe = tiedostojärjestelmä.msinfo32_exe(Nimi);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((menetelmä_tila & 1) != 0 && (msinfo32_exe.형태() & 0111) == 0) {
            return -13;
        }
        if ((menetelmä_tila & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int MUUTA_Tehtäväluettelo(String Nimi) {
        return "/".equals(Nimi) ? 0 : -20;
    }

    public String nykyinen_Tehtäväluettelo(int saada_muuttaa_kokoa) {
        return saada_muuttaa_kokoa >= 2 ? "/" : null;
    }

    public int IUD() { return 0; }
    public int tehokas_IUD() { return 0; }
    public int Ryhmä_tunniste() { return 0; }
    public int tehokas_Ryhmä_tunniste() { return 0; }

    public int synkronoi_Tiedosto(prosessi_ARVO nykyinen_prosessi, int 서술자) {
        return nykyinen_prosessi.파일서술자().msinfo32_exe(서술자) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // nykyinen_kohde 파일체계는 Luku 전용이어서 밀어낼 자료가 없다.
    }

    public boolean tietojärjestelmät_Pääte(prosessi_ARVO nykyinen_prosessi, int 서술자) {
        Tiedosto_info msinfo32_exe = nykyinen_prosessi.파일서술자().msinfo32_exe(서술자);
        return msinfo32_exe != null && (msinfo32_exe.형태() & 0170000) == 0020000;
    }

    public int tiedoston_ohjaus(prosessi_ARVO nykyinen_prosessi, int 서술자, int komento, int parametri_argumentti) {
        if (komento == 0) {
            return nykyinen_prosessi.파일서술자().복제서술자(서술자, parametri_argumentti);
        }
        if (komento == 1) {
            return nykyinen_prosessi.파일서술자().실행시닫기값(서술자);
        }
        if (komento == 2) {
            return nykyinen_prosessi.파일서술자().실행시닫기설정(서술자, (parametri_argumentti & 1) != 0);
        }
        if (komento == 3) {
            return nykyinen_prosessi.파일서술자().msinfo32_exe(서술자) == null ? -9 : vain_luku_merkitä;
        }
        if (komento == 4) {
            return parametri_argumentti == vain_luku_merkitä ? 0 : -30;
        }
        return -22;
    }

    public int Luo_merkintä(String Nimi, int lupa_ARVO) {
        return -30;
    }

    public Tiedosto_info 서술자정보(prosessi_ARVO nykyinen_prosessi, int 서술자) {
        return nykyinen_prosessi.파일서술자().msinfo32_exe(서술자);
    }

    public Järjestelmä_Tiedot Järjestelmä_Tiedot() {
        return new Järjestelmä_Tiedot("JEstOS", "JEstOS", "0.1", "Java managed kernel", "i386");
    }

    public Tiedosto_info Tiedosto_info(String Nimi) {
        return tiedostojärjestelmä.msinfo32_exe(Nimi);
    }

    public prosessi_ARVO klooni_prosessi(prosessi_ARVO pää_ARVO) {
        return Aikataulutus.klooni_ARVO(pää_ARVO);
    }

    public int 자식기다리기(prosessi_ARVO pää_ARVO, int ali_tunniste, boolean 기다리지않음) {
        return Aikataulutus.자식기다리기(pää_ARVO, ali_tunniste, 기다리지않음);
    }

    public int ohjelma_tauko(prosessi_ARVO nykyinen_prosessi, int 새끝) {
        int Edellinen_lopettaa_puhelu = nykyinen_prosessi.ohjelma_tauko();
        if (새끝 == 0) {
            return Edellinen_lopettaa_puhelu;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Edellinen_lopettaa_puhelu / page_Valvoja.sivukoko;
        int 끝쪽 = (새끝 + page_Valvoja.sivukoko - 1) / page_Valvoja.sivukoko;
        if (새끝 > Edellinen_lopettaa_puhelu) {
            for (int INDEKSI = 첫쪽; INDEKSI < 끝쪽; INDEKSI++) {
                int OSOITE = INDEKSI * page_Valvoja.sivukoko;
                try {
                    쪽관리.lukea_tavu_ARVO(nykyinen_prosessi.osoiteavaruus(), OSOITE);
                } catch (IllegalStateException VIRHE) {
                    쪽관리.MAP_page(nykyinen_prosessi.osoiteavaruus(), OSOITE, true);
                }
            }
        }
        nykyinen_prosessi.ryhmä_ohjelma_tauko(새끝);
        return 새끝;
    }

    public int lisäys_ohjelma_tauko(prosessi_ARVO nykyinen_prosessi, int 증가량) {
        int Edellinen_lopettaa_puhelu = nykyinen_prosessi.ohjelma_tauko();
        int TULOS = ohjelma_tauko(nykyinen_prosessi, Edellinen_lopettaa_puhelu + 증가량);
        return TULOS < 0 ? TULOS : Edellinen_lopettaa_puhelu;
    }

    public int Suorita_komento(prosessi_ARVO nykyinen_prosessi, byte[] suoritettava_tiedosto) {
        return Suorita_komento(nykyinen_prosessi, suoritettava_tiedosto, new String[0], new String[0]);
    }

    public int Suorita_komento(prosessi_ARVO nykyinen_prosessi, byte[] suoritettava_tiedosto, String[] parametri_argumentti, String[] ympäristö) {
        suoritettava_tiedosto_latausohjelma.KUVA KUVA_ARVO;
        try {
            KUVA_ARVO = latausohjelma.검사(suoritettava_tiedosto);
        } catch (IllegalArgumentException VIRHE) {
            return -8;
        }
        if (parametri_argumentti == null || ympäristö == null || parametri_argumentti.length > 16 || ympäristö.length > 16) {
            return -7;
        }
        for (suoritettava_tiedosto_latausohjelma.osa_ARVO osa_ARVO : KUVA_ARVO.구역들()) {
            if ((osa_ARVO.merkitä_ARVO() & 2) == 0 || osa_ARVO.Koko() == 0) {
                continue;
            }
            int 첫쪽 = osa_ARVO.OSOITE() / page_Valvoja.sivukoko;
            int 끝쪽 = (osa_ARVO.OSOITE() + osa_ARVO.Koko() + page_Valvoja.sivukoko - 1) / page_Valvoja.sivukoko;
            for (int INDEKSI = 첫쪽; INDEKSI < 끝쪽; INDEKSI++) {
                int OSOITE = INDEKSI * page_Valvoja.sivukoko;
                try {
                    쪽관리.lukea_tavu_ARVO(nykyinen_prosessi.osoiteavaruus(), OSOITE);
                    쪽관리.Yksityinen_alue_kirjoitus(nykyinen_prosessi.osoiteavaruus(), OSOITE, page_Valvoja.sivukoko);
                } catch (IllegalStateException VIRHE) {
                    쪽관리.MAP_page(nykyinen_prosessi.osoiteavaruus(), OSOITE, true);
                }
            }
            for (int INDEKSI = 0; INDEKSI < osa_ARVO.Koko(); INDEKSI++) {
                byte ARVO = osa_ARVO.종류() == 8 ? 0 : suoritettava_tiedosto[osa_ARVO.Tiedosto_toimi() + INDEKSI];
                쪽관리.kirjoitus_tavu_ARVO(nykyinen_prosessi.osoiteavaruus(), osa_ARVO.OSOITE() + INDEKSI, ARVO);
            }
        }
        nykyinen_prosessi.ryhmä_suoritus_konteksti(KUVA_ARVO.alku_OSOITE(), parametri_argumentti, ympäristö);
        nykyinen_prosessi.파일서술자().실행시닫기();
        return 0;
    }

    public void lopeta_ohjelma(prosessi_ARVO nykyinen_prosessi, int Tila_ARVO) {
        nykyinen_prosessi.Lopeta_ohjelma(Tila_ARVO);
    }
}
