// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ExceptionÉtatValeur : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ExceptionÉtatValeur extends java.lang.IllegalStateException {
    public ExceptionÉtatValeur() { super(); }
    public ExceptionÉtatValeur(String description) { super(description); }
    public String description() { return getMessage(); }
}
