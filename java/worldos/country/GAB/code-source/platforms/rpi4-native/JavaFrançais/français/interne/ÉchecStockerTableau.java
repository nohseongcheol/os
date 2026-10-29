// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** ÉchecStockerTableau : exception pouvant être déclarée, levée et interceptée avec l’API française. */
public class ÉchecStockerTableau extends java.lang.ArrayStoreException {
    public ÉchecStockerTableau() { super(); }
    public ÉchecStockerTableau(String description) { super(description); }
    public String description() { return getMessage(); }
}
