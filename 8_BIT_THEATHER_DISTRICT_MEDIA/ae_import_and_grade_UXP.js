const fs = require("uxp").storage.localFileSystem;

async function runUXPIngestAndGrade() {
    try {
        app.beginUndoGroup("8-Bit Ingest, Build, and Horizon Split V13 (UXP)");

        const compName = "8Bit_Aesthetic_Test";
        
        // UXP File System Call to read the Test Clips folder
        const mediaFolderPath = "file:///c:/Users/Saturn/Desktop/G_AG_FLDR/8_BIT_THEATHER_DISTRICT_MEDIA/TEST_CLIPS";
        let mediaFolder = null;
        try {
            mediaFolder = await fs.getEntryWithUrl(mediaFolderPath);
        } catch(e) {
            console.log("ERROR: Test_Clips folder not found on disk.");
            app.endUndoGroup();
            return;
        }

        const files = await mediaFolder.getEntries();
        const validFiles = files.filter(f => f.isFile && !f.name.startsWith("."));

        if (validFiles.length === 0) { 
            console.log("ERROR: No files found inside the Test_Clips folder.");
            app.endUndoGroup();
            return; 
        }

        // Collect and clean native paths within the async UXP thread
        const nativePaths = validFiles.map(file => file.nativePath);
        
        console.log(`[UXP COGNITION]: Staging ${nativePaths.length} clean target paths for bridge transmission.`);

        // Compile the un-collapsed ExtendScript execution macro string
        const buildMacroScript = `
            (function() {
                var pathsArray = ${JSON.stringify(nativePaths)};
                var targetCompName = "${compName}";
                var importedIds = [];
                
                var project = app.project;
                var targetComp = null;
                for (var i = 1; i <= project.numItems; i++) {
                    if (project.item(i) instanceof CompItem && project.item(i).name === targetCompName) {
                        targetComp = project.item(i);
                        break;
                    }
                }
                
                if (!targetComp) {
                    targetComp = project.items.addComp(targetCompName, 1920, 1080, 1.0, 10, 30);
                }

                var currentStartTime = 0;

                for (var j = 0; j < pathsArray.length; j++) {
                    var fileRef = new File(pathsArray[j]);
                    if (fileRef.exists) {
                        var importOptions = new ImportOptions(fileRef);
                        var importedAsset = project.importFile(importOptions);
                        
                        if (importedAsset) {
                            importedIds.push(importedAsset.id);
                            
                            var itemDuration = importedAsset.duration;
                            if (itemDuration <= 0 || isNaN(itemDuration)) {
                                itemDuration = 5.0; 
                            }

                            // Dynamic comp duration expansion
                            if (currentStartTime + itemDuration > targetComp.duration) {
                                targetComp.duration = currentStartTime + itemDuration;
                            }

                            var srcWidth = importedAsset.width;
                            var srcHeight = importedAsset.height;
                            var compWidth = targetComp.width;
                            var compHeight = targetComp.height;

                            var scaleFitWidth = (compWidth / srcWidth) * 100;
                            var scaleFitHeight = (compHeight / srcHeight) * 100;

                            var scaleFit = Math.min(scaleFitWidth, scaleFitHeight);
                            var scaleFill = Math.max(scaleFitWidth, scaleFitHeight);

                            var isNonStandardRatio = (Math.abs(scaleFitWidth - scaleFitHeight) > 0.1);

                            // --- BACKGROUND LAYER (Horizon Split Blur) ---
                            if (isNonStandardRatio) {
                                var bgLayer = targetComp.layers.add(importedAsset);
                                bgLayer.startTime = currentStartTime;
                                bgLayer.outPoint = currentStartTime + itemDuration;
                                bgLayer.property("Scale").setValue([scaleFill, scaleFill]);

                                try {
                                    var blur = null;
                                    try { blur = bgLayer.property("Effects").addProperty("ADBE Gaussian Blur 2"); }
                                    catch(e) { blur = bgLayer.property("Effects").addProperty("Gaussian Blur"); }
                                    if (blur) {
                                        blur.property(1).setValue(150);
                                        try { blur.property(3).setValue(1); } catch(e2){} 
                                    }
                                } catch(e) {}
                                applyGrade(bgLayer);
                            }

                            // --- FOREGROUND LAYER (Primary Crisp Asset) ---
                            var fgLayer = targetComp.layers.add(importedAsset);
                            fgLayer.startTime = currentStartTime;
                            fgLayer.outPoint = currentStartTime + itemDuration;
                            
                            if (isNonStandardRatio) {
                                fgLayer.property("Scale").setValue([scaleFit, scaleFit]);
                            } else {
                                fgLayer.property("Scale").setValue([scaleFitWidth, scaleFitHeight]);
                            }
                            applyGrade(fgLayer);

                            currentStartTime += itemDuration;
                        }
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
                return JSON.stringify(importedIds);
            })();
        `;

        const pipelineResponse = await app.executeScript(buildMacroScript);
        const processedItemIds = JSON.parse(pipelineResponse);
        
        console.log("SUCCESS: UXP Ingest Complete. Registered IDs:", processedItemIds);
        app.endUndoGroup();

    } catch (error) {
        console.log("CRITICAL FAULT: " + error.message);
        app.endUndoGroup();
    }
}

runUXPIngestAndGrade();
