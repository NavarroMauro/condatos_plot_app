# app/io_utils.py
from __future__ import annotations
import subprocess, sys
from pathlib import Path
from typing import Iterable
from PIL import Image
# Registrar HEIF/AVIF en Pillow
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except Exception:
    pass

def ensure_parent(outpath: Path):
    outpath.parent.mkdir(parents=True, exist_ok=True)

def save_fig_multi(fig, base: Path, formats: Iterable[str],
                   jpg_quality=92, webp_quality=92, avif_quality=55,
                   scour_svg=True):
    base = base.with_suffix("")
    for fmt in formats:
        fmt_lower = fmt.lower()
        if fmt_lower in {"png","pdf","svg"}:
            out = base.with_suffix(f".{fmt_lower}")
            ensure_parent(out)
            print(f"[save] {out}")
            fig.savefig(out, bbox_inches='tight', pad_inches=0.1)  # Añadimos bbox_inches y padding
            if fmt_lower == "svg" and scour_svg:
                try:
                    minified = base.with_suffix(".min.svg")
                    subprocess.run(["scour", "-i", str(out), "-o", str(minified),
                                    "--enable-id-stripping", "--enable-comment-stripping",
                                    "--shorten-ids", "--remove-metadata"],
                                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    minified.replace(out)
                except Exception:
                    pass
        elif fmt_lower in {"jpg","jpeg","webp","avif"}:
            tmp_png = base.with_suffix(".tmp.png")
            print(f"[tmp] {tmp_png}")
            fig.savefig(tmp_png, bbox_inches='tight', pad_inches=0.1)  # Aquí también
            im = Image.open(tmp_png)
            out = base.with_suffix(f".{fmt_lower}")
            ensure_parent(out)
            if fmt_lower in {"jpg","jpeg"}:
                im = im.convert("RGB")
                im.save(out, format="JPEG", quality=jpg_quality, optimize=True, progressive=True)
            elif fmt_lower == "webp":
                im.save(out, format="WEBP", quality=webp_quality, method=6)
            elif fmt_lower == "avif":
                try:
                    im.save(out, format="AVIF", quality=avif_quality)
                except Exception as e:
                    print(f"[WARN] AVIF no soportado ({e}); saltando", file=sys.stderr)
            tmp_png.unlink(missing_ok=True)
        else:
            print(f"[WARN] Formato no soportado: {fmt}", file=sys.stderr)