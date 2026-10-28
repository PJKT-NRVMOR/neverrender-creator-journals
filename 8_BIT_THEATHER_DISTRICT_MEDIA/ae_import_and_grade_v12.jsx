#target aftereffects

(function() {
    try {
        var project = app.project;
        if (!project) {
            alert("ERROR: No active project found.");
            return;
        }

        app.beginUndoGroup("8-Bit Ingest, Build, and Horizon Split V12");

        var targetComp = null;
        var compName = "8Bit_Aesthetic_Test";
        for (var i = 1; i <= project.numItems; i++) {
            if (project.item(i) instanceof CompItem && project.item(i).name === compName) {
                targetComp = project.item(i);
                break;
            }
        }

        if (!targetComp) {
            targetComp = project.items.addComp(compName, 1920, 1080, 1, 10, 30);
        }

        var mediaFolder = new Folder("c:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/TEST_CLIPS");
        if (!mediaFolder.exists) {
            alert("ERROR: Test_Clips folder not found on disk.");
            app.endUndoGroup();
            return;
        }

        var files = mediaFolder.getFiles();
        var validFiles = [];
        
        for (var f = 0; f < files.length; f++) {
            if (files[f] instanceof File && !files[f].hidden) {
                validFiles.push(files[f]);
            }
        }

        if (validFiles.length === 0) { 
            alert("ERROR: No files found inside the Test_Clips folder.");
            app.endUndoGroup();
            return; 
        }

        var currentStartTime = 0;

        for (var v = 0; v < validFiles.length; v++) {
            var file = validFiles[v];
            var importOptions = new ImportOptions(file);
            var importedItem = null;
            
            try {
                importedItem = project.importFile(importOptions);
            } catch (importErr) { continue; }

            if (importedItem) {
                var itemDuration = importedItem.duration;
                if (itemDuration <= 0 || isNaN(itemDuration)) {
                    itemDuration = 5.0; 
                }

                if (currentStartTime + itemDuration > targetComp.duration) {
                    targetComp.duration = currentStartTime + itemDuration;
                }

                // Determine scaling math for a 1920x1080 comp
                var srcWidth = importedItem.width;
                var srcHeight = importedItem.height;
                var compWidth = targetComp.width;
                var compHeight = targetComp.height;

                var scaleFitWidth = (compWidth / srcWidth) * 100;
                var scaleFitHeight = (compHeight / srcHeight) * 100;

                // Scale to Fit (Foreground)
                var scaleFit = Math.min(scaleFitWidth, scaleFitHeight);
                
                // Scale to Fill (Background)
                var scaleFill = Math.max(scaleFitWidth, scaleFitHeight);

                var isNonStandardRatio = (Math.abs(scaleFitWidth - scaleFitHeight) > 0.1);

                // --- BACKGROUND LAYER (Horizon Split Blur) ---
                if (isNonStandardRatio) {
                    var bgLayer = targetComp.layers.add(importedItem);
                    bgLayer.startTime = currentStartTime;
                    bgLayer.outPoint = currentStartTime + itemDuration;
                    
                    // Scale to fill the empty black wings
                    bgLayer.property("Scale").setValue([scaleFill, scaleFill]);

                    // Add Heavy Camera Blur
                    try {
                        var blur = null;
                        try { blur = bgLayer.property("Effects").addProperty("ADBE Gaussian Blur 2"); }
                        catch(e) { blur = bgLayer.property("Effects").addProperty("Gaussian Blur"); }
                        
                        if (blur) {
                            blur.property(1).setValue(150); // Blur radius
                            // If property 3 is 'Repeat Edge Pixels' (standard in Gaussian Blur)
                            try { blur.property(3).setValue(1); } catch(e2){} 
                        }
                    } catch(e) {}

                    applyGrade(bgLayer);
                }

                // --- FOREGROUND LAYER (Primary Crisp Asset) ---
                var fgLayer = targetComp.layers.add(importedItem);
                fgLayer.startTime = currentStartTime;
                fgLayer.outPoint = currentStartTime + itemDuration;
                
                if (isNonStandardRatio) {
                    // Fit precisely into the frame center
                    fgLayer.property("Scale").setValue([scaleFit, scaleFit]);
                } else {
                    // Standard 16:9 file, scale it just in case it's 4K or 720p
                    fgLayer.property("Scale").setValue([scaleFitWidth, scaleFitHeight]);
                }

                // Apply the V11 cinematic grade to the foreground
                applyGrade(fgLayer);

                currentStartTime += itemDuration;
            }
        }

        function applyGrade(layer) {
            try {
                var levels = null;
                try { levels = layer.property("Effects").addProperty("ADBE Level2"); }
                catch(e1) { levels = layer.property("Effects").addProperty("Levels"); }
                if (levels) { levels.property(2).setValue(0.12); }
            } catch(e) {}

            try {
                var tritone = layer.property("Effects").addProperty("ADBE Tritone");
                // Highlights: Radioactive Mint (#89ECA4)
                tritone.property(1).setValue([137/255, 236/255, 164/255, 1.0]); 
                // Midtones: Deep Celadon (#36725B)
                tritone.property(2).setValue([54/255, 114/255, 91/255, 1.0]); 
                // Shadows: Deep Noir Plum (#4A203B)
                tritone.property(3).setValue([74/255, 32/255, 59/255, 1.0]); 
                // Blend with Original (85%)
                tritone.property(4).setValue(85); 
            } catch(e) {}

            try {
                var glow = null;
                try { glow = layer.property("Effects").addProperty("ADBE Glow2"); } 
                catch(e1) { glow = layer.property("Effects").addProperty("Glow"); }
                if (glow) {
                    glow.property(2).setValue(75); 
                    glow.property(3).setValue(28); 
                    glow.property(4).setValue(0.18); 
                }
            } catch(e) {}
        }

        targetComp.openInViewer();
        app.endUndoGroup();

    } catch (error) {
        alert("CRITICAL FAULT at line " + error.line + ": " + error.message);
    } finally {
        $.gc();
    }
})();
