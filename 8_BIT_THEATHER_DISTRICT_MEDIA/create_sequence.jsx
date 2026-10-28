#target premierepro
app.enableQE();

(function() {
    try {
        $.writeln("Initializing 8-Bit Theater District Environment...");
        
        var project = app.project;
        if (!project) {
            $.writeln("ERROR: No active project found.");
            return;
        }
        $.writeln("SUCCESS: Active Premiere Pro project detected.");

        var seqName = "8Bit_Aesthetic_Test";
        // Create sequence
        project.createNewSequence(seqName, "");
        
        $.writeln("SUCCESS: Sequence '" + seqName + "' built successfully.");
        
    } catch (error) {
        $.writeln("CRITICAL FAULT: " + error.message);
    } finally {
        $.gc();
    }
})();
