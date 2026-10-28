// prep_card_for_print.jsx
// Automates formatting an SVG business card for 300 DPI, CMYK, and 0.125" bleed.

#target photoshop

function main() {
    if (app.documents.length === 0) {
        alert("Please open your SVG business card in Photoshop first.");
        return;
    }

    var doc = app.activeDocument;

    // 1. Convert to CMYK for print
    if (doc.mode !== DocumentMode.CMYK) {
        doc.changeMode(ChangeMode.CMYK);
    }

    // 2. Set Resolution to 300 DPI
    // Standard US Business Card is 3.5" x 2". 
    // At 300 DPI: 1050px x 600px
    doc.resizeImage(UnitValue(3.5, "in"), UnitValue(2.0, "in"), 300, ResampleMethod.BICUBIC);

    // 3. Add 0.125" Bleed on all sides (Total size becomes 3.75" x 2.25")
    // At 300 DPI: 1125px x 675px
    doc.resizeCanvas(UnitValue(3.75, "in"), UnitValue(2.25, "in"), AnchorPosition.MIDDLECENTER);

    // 4. Flatten image (optional, but good for PDFs)
    doc.flatten();

    // 5. Save as Print PDF
    var outPath = new File(doc.path + "/" + doc.name.split('.')[0] + "_PRINT_READY.pdf");
    var pdfSaveOptions = new PDFSaveOptions();
    pdfSaveOptions.PDFCompatibility = PDFCompatibility.PDF15; // Acrobat 6 (standard for printers)
    pdfSaveOptions.preserveEditing = false;
    pdfSaveOptions.embedColorProfile = true;
    pdfSaveOptions.optimizeForWeb = false;
    
    doc.saveAs(outPath, pdfSaveOptions, true, Extension.LOWERCASE);
    
    alert("Success! Print-ready PDF generated:\n" + outPath.fsName);
}

main();
