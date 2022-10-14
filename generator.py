from pathlib import Path
import random
from sys import argv
from typing import List, Union

import jinja2
import pandas as pd
import qrcode
from tqdm import tqdm



CHARSET: str = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
LENGTH: int = 4
OUTPUT_DIR: Path = Path("output")
URL_TEMPLATE: jinja2.Template = jinja2.Template(
    "https://mobilidade.rio/{{ code }}")
CODES= pd.read_csv('codes.csv')["code"].to_list()


def generate_code(charset: Union[str, List[str]] = CHARSET, length: int = LENGTH) -> str:
    return "".join(random.choice(charset) for _ in range(length))


def generate_url(code: str) -> str:
    return URL_TEMPLATE.render(code=code)


def generate_qr(code: str) -> str:
    img = qrcode.make(generate_url(code))
    img.save(OUTPUT_DIR / f"{code}.png")

if __name__ == "__main__":
    if len(argv) != 2:
        print("Usage: python3 generator.py <number of codes>")
        exit(1)

    try:
        number_of_codes = int(argv[1])
    except ValueError:
        print("Invalid number of codes")
        exit(1)

    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()

    for _ in tqdm(range(number_of_codes)):
        code_stop = True
        i=0
        while code_stop and i<1000:
            code= str = generate_code()
            code_stop = code in CODES    
            i+=1
            if not code_stop:
                generate_qr(code)
                CODES.append(code)
        done = _ +1
        pd.DataFrame(CODES,columns=["code"]).to_csv('codes.csv')
    
    print(f"Generated {done} codes")
    print(f"Output directory: {OUTPUT_DIR}")
