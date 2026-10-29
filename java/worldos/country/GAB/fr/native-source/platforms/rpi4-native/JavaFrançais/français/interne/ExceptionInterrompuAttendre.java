// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package français.interne;

/** Indique l’interruption d’une opération attendant un fil d’exécution, pas la fin de la tâche elle-même. */
public class ExceptionInterrompuAttendre extends java.lang.InterruptedException {
    public ExceptionInterrompuAttendre() { super(); }
    public ExceptionInterrompuAttendre(String description) { super(description); }
    public String description() { return getMessage(); }
}
