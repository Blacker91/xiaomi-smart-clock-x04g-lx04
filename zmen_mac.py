#!/usr/bin/env python3
"""
Zmena MAC adresy v NVRAM souborech MediaTek (Xiaomi Mi Smart Clock).

Soubory z budiku (/data/nvram/APCFG/APRDEB/):
  WIFI     514 bajtu, MAC na bajtech 4-9
  BT_Addr   66 bajtu, MAC na bajtech 0-5

Na konci obou je dvojice bajtu: znacka 0xAA a kontrolni soucet.
Soucet: sude bajty se scitaji, liche se XORuji (po bajtech, modulo 256),
pres vsechno krome poslednich dvou bajtu.

Pouziti:
  python3 zmen_mac.py WIFI    WIFI_novy    AA:BB:CC:DD:EE:FF
  python3 zmen_mac.py BT_Addr BT_Addr_novy AA:BB:CC:DD:EE:FF

Puvodni soubor se nemeni, vysledek se zapise do noveho.
"""
import re
import sys

TYPY = {514: ("WIFI", 4), 66: ("BT_Addr", 0)}
ZNACKA = 0xAA


def soucet(data):
    c = 0
    for i, b in enumerate(data):
        c = (c + b) & 0xFF if i % 2 == 0 else c ^ b
    return c


def parse_mac(text):
    if not re.fullmatch(r"[0-9A-Fa-f]{2}([:-]?[0-9A-Fa-f]{2}){5}", text):
        sys.exit(f"CHYBA: '{text}' neni MAC adresa (cekam tvar AA:BB:CC:DD:EE:FF)")
    mac = bytes.fromhex(re.sub(r"[:-]", "", text))
    if mac[0] & 0x01:
        sys.exit("CHYBA: multicast MAC (lichy prvni bajt) nejde pouzit pro zarizeni")
    return mac


def fmt(mac):
    return ":".join(f"{b:02x}" for b in mac)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    vstup, vystup, mac_text = sys.argv[1:]
    mac = parse_mac(mac_text)

    data = bytearray(open(vstup, "rb").read())
    if len(data) not in TYPY:
        sys.exit(f"CHYBA: {vstup} ma {len(data)} bajtu, cekam 514 (WIFI) nebo 66 (BT_Addr)")
    nazev, off = TYPY[len(data)]

    # pojistka: zpracujeme jen soubor, ktery uz ted ma spravny tvar
    if data[-2] != ZNACKA or data[-1] != soucet(data[:-2]):
        sys.exit(f"CHYBA: {vstup} nema platny kontrolni soucet - neni to {nazev} z budiku, "
                 "nebo je poskozeny. Nic jsem nezapsal.")

    stara = bytes(data[off:off + 6])
    data[off:off + 6] = mac
    data[-1] = soucet(data[:-2])
    open(vystup, "wb").write(data)

    print(f"{nazev}: {fmt(stara)} -> {fmt(mac)}, soucet 0x{data[-1]:02x}, zapsano do {vystup}")


if __name__ == "__main__":
    main()
