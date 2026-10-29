"""
NeverRender Labs // VCF Contact Card Compiler (vCard 3.0 with Base64 Crest Avatar)
Builds an iOS/Android-ready .vcf contact card with embedded JPEG avatar,
Toll-Free SMS/MMS line, direct showroom line, and primary/secondary emails.
"""
import os
import base64
from io import BytesIO
from PIL import Image


def build_chapman_vcf(crest_png_path: str, output_paths: list[str]) -> str:
    # Render the crest onto a clean 300x300 #F8F3EC parchment square for iOS Contact Avatar
    avatar_b64 = ""
    if os.path.exists(crest_png_path):
        img = Image.open(crest_png_path).convert("RGBA")
        canvas = Image.new("RGB", (300, 300), (248, 243, 236))
        img.thumbnail((240, 240), Image.Resampling.LANCZOS)
        ox = (300 - img.width) // 2
        oy = (300 - img.height) // 2
        canvas.paste(img, (ox, oy), img)
        buf = BytesIO()
        canvas.save(buf, format="JPEG", quality=90, optimize=True)
        avatar_b64 = base64.b64encode(buf.getvalue()).decode("ascii")

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        "N:Chapman;Melissa;;;",
        "FN:The Chapman Collection (Melissa Chapman)",
        "ORG:The Chapman Collection",
        "TITLE:Fine European Antiques, Period Furniture & Persian Carpets",
        "TEL;TYPE=CELL,VOICE,MSG,PREF:+18583492638",
        "TEL;TYPE=WORK,MSG:+18333494101",
        "EMAIL;TYPE=INTERNET,WORK,PREF:melissa@thechapmancollection.com",
        "EMAIL;TYPE=INTERNET,WORK:info@thechapmancollection.com",
        "URL:https://thechapmancollection.com",
        "ADR;TYPE=WORK:;;6014 La Granada;Rancho Santa Fe;CA;92067;United States",
        "NOTE:Curated by Melissa Chapman | Rancho Santa Fe Showroom. Call or text Melissa directly at (858) 349-2638 or reply to our VIP text line at (833) 349-4101.",
    ]
    if avatar_b64:
        lines.append(f"PHOTO;ENCODING=b;TYPE=JPEG:{avatar_b64}")
    lines.append("END:VCARD")

    vcf_content = "\r\n".join(lines) + "\r\n"
    for p in output_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="ascii") as f:
            f.write(vcf_content)
        print("Wrote VCF:", p)
    return vcf_content


if __name__ == "__main__":
    crest = r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\2026-10-27-autumn-warmth-and-old-world-peculiars\cuts\tcc-oct23-crest.png"
    targets = [
        r"c:\Users\Saturn\Desktop\G_AG_FLDR\NEVERRENDER_LABS_WEBSITE\drafts-for-pmc-approval\The-Chapman-Collection.vcf",
        r"c:\Users\Saturn\Desktop\project-marshall-college\project-marshall-college\04-campaigns-outreach-drops\approved-active-drops\2026-10-27-autumn-warmth-old-world-peculiars\The-Chapman-Collection.vcf",
    ]
    build_chapman_vcf(crest, targets)
