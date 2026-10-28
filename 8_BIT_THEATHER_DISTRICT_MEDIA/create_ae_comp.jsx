#target aftereffects

(function() {
    try {
        $.writeln("Initializing 8-Bit Theater District Environment in After Effects...");
        
        var project = app.project;
        if (!project) {
            $.writeln("ERROR: No active project found.");
            return;
        }
        $.writeln("SUCCESS: Active After Effects project detected.");

        var compName = "8Bit_Aesthetic_Test";
        // Create a basic 1920x1080 30fps comp that is 10 seconds long
        var newComp = project.items.addComp(compName, 1920, 1080, 1, 10, 30);
        
        if (newComp) {
            $.writeln("SUCCESS: Composition '" + compName + "' built successfully.");
        }
        
    } catch (error) {
        $.writeln("CRITICAL FAULT: " + error.message);
    } finally {
        $.gc();
    }
})();
