# GPS Lorenzo — prototipo gratuito

App web statica per consultare i risultati di una **ricerca parziale** nelle pubblicazioni ufficiali GPS di Bari (AB55 e AB56). Non è una chat AI e non certifica nomine, contratti, assenza di incarichi o disponibilità residue.

## Installazione senza scrivere codice

1. Scarica lo ZIP e **decomprimilo** sul Mac.
2. Nel repository GitHub apri **Add file → Upload files**. Trascina **il contenuto della cartella** `gps-lorenzo`, non la cartella esterna né lo ZIP. Devi caricare anche `.github/workflows/check.yml` (cartella nascosta su Mac: `Cmd + Shift + .` per mostrarla). Se l'interfaccia non mantiene le cartelle, usa la procedura alternativa sotto.
3. Premi **Commit changes**.
4. Vai su **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**. Attendi qualche minuto; GitHub mostrerà il collegamento pubblico del sito.
5. Vai su **Actions → Controllo pubblicazioni GPS → Run workflow**. Se necessario abilita Actions. Controlla i log: un'esecuzione riuscita non implica che siano stati trovati tutti i documenti.
6. Apri il sito dal telefono di tua madre; dal browser puoi scegliere **Aggiungi alla schermata Home**.

### Alternativa affidabile per caricare le cartelle

Se GitHub non accetta la cartella nascosta `.github`, usa il pulsante `Add file → Create new file`, come nome scrivi `.github/workflows/check.yml`, e incolla il contenuto del file locale omonimo. Crea nello stesso modo `scripts/check.py` e `data/results.json` se l'upload non mantiene i percorsi. I file nella radice sono `index.html`, `manifest.webmanifest`, `requirements.txt`, `README.md`.

## Limiti reali

- Il programma visita una pagina di ricerca dell'USP Bari, alcuni collegamenti che trova e fino a 15 PDF per esecuzione; **non** controlla tutti i turni, gli albi delle scuole, tutte le rettifiche o le altre province.
- Cerca parole chiave nel testo estraibile dei PDF; i PDF scannerizzati possono sfuggire.
- Rilevare il cognome in un documento **non equivale** a una nomina verificata. Servirebbe interpretare la riga e il contesto.
- L'archivio conserva i documenti già trovati, ma non garantisce che i link restino accessibili.
- Le esecuzioni pianificate di GitHub Actions possono subire ritardi o non partire; l'esecuzione manuale è disponibile.
- GitHub Pages e Actions possono essere usati gratuitamente per questo prototipo con repository pubblico, soggetti ai termini e ai limiti di GitHub.
- Tutto il contenuto del repository e dell'app è **pubblico**. Non inserire dati personali non già pubblici, numeri di telefono, documenti privati, password o token.

## Cosa serve per renderlo davvero utile

Integrare e verificare una lista completa di pagine istituzionali, i singoli turni GPS, le rettifiche e le graduatorie nominative; aggiungere estrazione strutturata delle righe e un controllo di qualità manuale per ogni tipologia di PDF. Solo allora si potranno presentare risultati affidabili su chi è stato nominato e sullo scorrimento.
