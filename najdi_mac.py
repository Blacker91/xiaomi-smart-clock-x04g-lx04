#!/usr/bin/env python3
"""
Najde MAC adresy Wi-Fi a Bluetooth v zaloze budiku (Xiaomi Mi Smart Clock).

Hleda stejne vzory bajtu, jake maji NVRAM zaznamy WIFI a BT_Addr:
  Wi-Fi:      04 01 ?? ?? [MAC 6 B] 00 00 25 25
  Bluetooth:  [MAC 6 B] 60 00 23 10 00 00 07 80

Pouziti:
  python3 najdi_mac.py nvram.bin          # zaloha oddilu nvram, rychle
  python3 najdi_mac.py zaloha_full.bin    # cely dump, trva par minut

Zaznam byva v zaloze vickrat; vsechny vyskyty by mely ukazovat
na stejnou adresu. Pokud se lisi, nekde je stara kopie - nepouzivej
ji naslepo.
"""
import re
import sys
from collections import OrderedDict

VZORY = {
    "Wi-Fi": re.compile(rb"\x04\x01..(.{6})\x00\x00\x25\x25", re.S),
    "Bluetooth": re.compile(rb"(.{6})\x60\x00\x23\x10\x00\x00\x07\x80", re.S),
}
BLOK = 64 * 1024 * 1024
PREKRYV = 32  # zaznam muze lezet na hranici dvou bloku


def fmt(mac):
    return ":".join(f"{b:02x}" for b in mac)


def platna(mac):
    return mac not in (b"\x00" * 6, b"\xff" * 6) and not (mac[0] & 0x01)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    nalezy = {k: OrderedDict() for k in VZORY}

    with open(sys.argv[1], "rb") as f:
        pozice = 0
        zbytek = b""
        while True:
            blok = f.read(BLOK)
            if not blok:
                break
            data = zbytek + blok
            zacatek = pozice - len(zbytek)
            for nazev, vzor in VZORY.items():
                for m in vzor.finditer(data):
                    off = zacatek + m.start()
                    mac = m.group(1)
                    if platna(mac):
                        nalezy[nazev].setdefault(mac, set()).add(off)
            zbytek = data[-PREKRYV:]
            pozice += len(blok)

    nic = True
    for nazev, macs in nalezy.items():
        for mac, offs in macs.items():
            nic = False
            print(f"{nazev:10s} {fmt(mac)}   ({len(offs)}x, prvni na 0x{min(offs):x})")
    if nic:
        sys.exit("Nic nenalezeno. Zkus cely dump misto jednoho oddilu.")
    for nazev, macs in nalezy.items():
        if len(macs) > 1:
            print(f"\nPOZOR: {nazev} ma v zaloze vic ruznych adres - over, ktera je spravna.")


if __name__ == "__main__":
    main()
