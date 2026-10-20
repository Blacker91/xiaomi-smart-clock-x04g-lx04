# 7. Řešení problémů

## Chybové hlášky

| Hláška | Příčina a řešení |
|---|---|
| `ModuleNotFoundError: No module named 'usb'` | zapomenuté `source mtk_venv/bin/activate` |
| `Please disconnect, start mtkclient and reconnect` | budík je v jiném stavu — odpoj, vypni, znovu do BROM |
| `No emmc info, can't parse existing preloaders`, pak `DA hash mismatch` | mtkclient nedokáže vyčíst preloader z paměti — přidej `--preloader cesta/k/preloader.bin` |
| `Error: Couldn't detect partition: preloader` | preloader není v tabulce oddílů, leží v boot oblasti — přidej `--parttype boot1` |
| `Filename doesn't exists` | špatná cesta k souboru |
| „未发现mi.did" (mi.did nenalezen) | chybí `nvram` z čínského LX04 — viz [04](04-x04g-na-lx04.md) |
| displej problikne a zhasne hned po logu | zamčený bootloader — `python3 mtk.py da seccfg unlock` |
| při startu varování **Orange State** | bootloader je odemčený; po dokončení všech úprav ho můžeš zamknout — `python3 mtk.py da seccfg lock` ([04](04-x04g-na-lx04.md#na-závěr-zamknutí-bootloaderu-volitelné)) |
| SP Flash Tool: `STATUS_UNKNOWN_STORAGE_SECTION_TYPE` | *Format All* neumí boot oblast tohohle eMMC — formátuj ručně jen `EMMC_USER` |
| SP Flash Tool: „PMT changed for the ROM" | na disku zůstalo staré rozložení oddílů — nejdřív formát |
| Windows 11: budík se ve Správci zařízení neobjeví | přísnější podepisování ovladačů — použij Windows 10 |
| `da seccfg unlock`: `Device is either already unlocked or algo is unknown` | `seccfg` je z jiného čipu (typicky po klonování) — zapiš vlastní ze zálohy ([04](04-x04g-na-lx04.md#další-globální-kus-naklonování-jen-linux)) |
| po zápisu přes SP Flash Tool: 出现严重错误，需要恢复出厂设置 | očekávané — pokračuj nahráním SP6 a identity ([04](04-x04g-na-lx04.md#část-2--linux-sp6-a-identita)) |

## Co nefunguje a proč

**Preloader zapsaný přes mtkclient z firmwaru.** Oblast `EMMC_BOOT_1` začíná 2048bajtovou hlavičkou (`EMMC_BOOT` + `BRLYT`), teprve za ní jde preloader. Firmware ho obsahuje bez hlavičky. SP Flash Tool ji dopočítá (typ `SV5_BL_BIN` ve scatteru), mtkclient zapíše syrová data a nevaruje. Zápis ohlásí úspěch, displej zůstane mrtvý.

Hlavička se nedá spolehlivě sestavit ručně — hodnota v `BRLYT` na offsetu `0x220` neodpovídá velikosti preloaderu (LX04 `0x40800`, X04G `0x29CA0`). Funguje jen hlavička od SP Flash Toolu, nebo boot1 vyčtený z funkčního zařízení.

**Převod oddíl po oddílu bez formátu.** Na disku zůstanou `nvram`, `proinfo`, `protect1/2` a `persist` z předchozího systému. mtkclient zápis udělá bez varování a systém pak nenaběhne. (U aktualizace čínského LX04 na SP6 je to naopak žádoucí — tam se identita měnit nemá.)

**SP Flash Tool pod Wine.** Okno se otevře, ale komunikaci nenaváže. BROM okno trvá jen pár vteřin a Wine port nestihne otevřít. Potřeba je skutečný Windows.

## Slepé uličky

**Převod globálu od nuly jen přes mtkclient.** Tabulka oddílů LX04 (`wf gpt_lx04.bin`), boot1 vyčtený z funkčního LX04, kompletní SP6, odemčený bootloader — a pořád jen podsvícený černý displej. Nepomohl ani „hybridní" boot1 (preloader X04G v hlavičce LX04). Rozjelo se to až po SP Flash Toolu.

Při hledání chybějícího `mi.did` se nabízí i tohle — **nic z toho nepomůže**:

- `vbmeta` — v rozložení LX04 neexistuje
- `para` — prakticky prázdná, čínská a globální se liší jediným bajtem
- `protect1/2`, `persist` — `mi.did` v nich není
- `expdb` — zůstává prázdná, kernel se k zápisu logu nedostane

## Bezpečnost

- BROM režim funguje nezávisle na obsahu paměti. Během celé práce se nepodařilo budík znefunkčnit tak, aby ho nešlo obnovit.
- **Nikdy neodpojuj kabel uprostřed zápisu** (`w`, `wf`, `e`). Přerušený zápis je jediná reálná cesta k trvalému poškození.
