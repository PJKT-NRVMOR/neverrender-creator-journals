#target photoshop

(function() {
    try {
        var inputFolderPath = "c:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/TEST_CLIPS";
        var outputFolderPath = "c:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/GRADED_PHOTOS";
        
        var inputFolder = new Folder(inputFolderPath);
        var outputFolder = new Folder(outputFolderPath);
        
        if (!inputFolder.exists) {
            alert("ERROR: TEST_CLIPS folder not found.");
            return;
        }
        
        if (!outputFolder.exists) {
            outputFolder.create();
        }

        var files = inputFolder.getFiles();
        var imageFiles = [];
        for (var i = 0; i < files.length; i++) {
            var f = files[i];
            if (f instanceof File && !f.hidden) {
                var name = f.name.toLowerCase();
                if (name.indexOf(".jpg") !== -1 || name.indexOf(".jpeg") !== -1 || name.indexOf(".png") !== -1) {
                    imageFiles.push(f);
                }
            }
        }

        if (imageFiles.length === 0) {
            alert("No photos found in TEST_CLIPS.");
            return;
        }

        app.displayDialogs = DialogModes.NO;

        for (var j = 0; j < imageFiles.length; j++) {
            var doc = app.open(imageFiles[j]);
            
            // 1. Levels Crush (Strip the haze)
            // Photoshop levels: (inputMin, inputMax, gamma, outputMin, outputMax)
            // Input 30 is roughly 12% of 255.
            doc.activeLayer.adjustLevels(30, 255, 1.0, 0, 255);

            // 2. Neon Color Wash (10% Tritone equivalent)
            var washLayer = doc.artLayers.add();
            washLayer.name = "8Bit Color Wash";
            washLayer.blendMode = BlendMode.COLORBLEND;
            washLayer.opacity = 10;
            
            var fillColor = new SolidColor();
            // Blending Neon Pink and Midnight Purple
            fillColor.rgb.red = 140;
            fillColor.rgb.green = 5;
            fillColor.rgb.blue = 60;
            
            doc.selection.selectAll();
            doc.selection.fill(fillColor);
            doc.selection.deselect();

            // 3. Cinematic Halation Glow
            // We mimic the AE glow by duplicating the base layer, thresholding it to only highlights, blurring it, and screening it
            doc.activeLayer = doc.layers[doc.layers.length - 1]; // select base layer
            var glowLayer = doc.activeLayer.duplicate(doc.activeLayer, ElementPlacement.PLACEBEFORE);
            glowLayer.name = "Cinematic Glow";
            
            // Threshold to isolate the bright neon screens/lights
            glowLayer.adjustLevels(180, 255, 1.0, 0, 255); 
            // Apply soft 28px spread
            glowLayer.applyGaussianBlur(28); 
            
            glowLayer.blendMode = BlendMode.SCREEN;
            glowLayer.opacity = 25; // Delicate intensity

            // 4. Export as JPG
            var saveOptions = new JPEGSaveOptions();
            saveOptions.quality = 12; // Maximum quality
            saveOptions.embedColorProfile = true;

            var finalFileName = doc.name.split('.')[0] + "_GRADED.jpg";
            var saveFile = new File(outputFolderPath + "/" + finalFileName);
            
            doc.saveAs(saveFile, saveOptions, true, Extension.LOWERCASE);
            doc.close(SaveOptions.DONOTSAVECHANGES);
        }
        
        alert("SUCCESS: Batch Grading Complete! Check the GRADED_PHOTOS folder.");

    } catch (e) {
        alert("CRITICAL FAULT at line " + e.line + ": " + e.message);
    }
})();
