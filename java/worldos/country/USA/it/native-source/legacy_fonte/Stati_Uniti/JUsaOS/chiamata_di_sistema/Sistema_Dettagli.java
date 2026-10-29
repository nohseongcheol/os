// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Stati_Uniti.JUsaOS.chiamata_di_sistema;

public final class Sistema_Dettagli {
    private final String Sistema_nome;
    private final String nodo_nome;
    private final String edizione_VALORE;
    private final String versione_VALORE;
    private final String computer;

    public Sistema_Dettagli(String Sistema_nome, String nodo_nome, String edizione_VALORE, String versione_VALORE, String computer) {
        this.Sistema_nome = Sistema_nome;
        this.nodo_nome = nodo_nome;
        this.edizione_VALORE = edizione_VALORE;
        this.versione_VALORE = versione_VALORE;
        this.computer = computer;
    }

    public String Sistema_nome() { return Sistema_nome; }
    public String nodo_nome() { return nodo_nome; }
    public String edizione_VALORE() { return edizione_VALORE; }
    public String versione_VALORE() { return versione_VALORE; }
    public String computer() { return computer; }
}
