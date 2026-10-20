# 6. Návrat ze zálohy

Do původního stavu vrátíš budík jen ze **své** zálohy z kroku [02](02-zaloha.md). Pro globální verzi neexistuje žádný balíček, který by se dal nahrát — jediná cesta zpátky na X04G je obnova dumpu z tvého globálního kusu.

S budíkem v BROM režimu, každý příkaz zvlášť:

```bash
cd ~/mtkclient
source mtk_venv/bin/activate

python3 mtk.py wf zaloha_full.bin
python3 mtk.py w preloader boot1.bin --parttype boot1
```

Oba kroky nech doběhnout na 100 %. Obnova celé paměti trvá desítky minut.

## Když po obnově nenaběhne

Záloha vrací i `seccfg`, tedy stav zámku bootloaderu. Pokud se start zastaví hned po logu:

```bash
python3 mtk.py da seccfg unlock
```

## Ověření zálohy před obnovou

```bash
md5sum -c kontrolni_soucty.md5
```

Velikost dumpu musí sedět — LX04 3,6 GB, X04G 3,7 GB. Menší soubor je neúplný a obnova z něj by budík poškodila.

## Čínský budík na globální systém

> [!WARNING]
> **Tohle vyzkoušené nemáme.** Převod čínského budíku LX04 na globální systém tenhle návod nepopisuje.

Není to jen obrácený postup:

- **Záloha globálu se do čínského budíku nevejde.** Čínský eMMC je menší (`0xE2000000` proti `0xEC000000`), takže globální dump nejde nahrát přes `wf`. Je potřeba upravená tabulka oddílů a zápis po oddílech.
- **Novější čínské kusy prý s globálním systémem nenaběhnou** — podle zpráv na XDA jim globální firmware nemá ovladač displeje.

Postup popisuje projekt [AyraHikari/xiaomi-x04g-lx04](https://github.com/AyraHikari/xiaomi-x04g-lx04). Před pokusem si udělej kompletní [zálohu](02-zaloha.md) — s ní čínský budík vždycky vrátíš do původního stavu.
