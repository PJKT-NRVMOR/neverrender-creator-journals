const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');

const app = express();
app.use(cors());
app.use(express.json());

const CONTEXT_DIR = 'C:\\Users\\Saturn\\Desktop\\G_AG_FLDR\\8_BIT_THEATHER_DISTRICT_MEDIA\\AGENTS\\TO';

// Fetch available context files
app.get('/api/contexts', async (req, res) => {
    try {
        const files = await fs.readdir(CONTEXT_DIR);
        // Only return .md, .txt, .json files
        const contextFiles = files.filter(f => ['.md', '.txt', '.json'].includes(path.extname(f)));
        res.json({ files: contextFiles });
    } catch (err) {
        console.error("Error reading context directory:", err);
        res.status(500).json({ error: "Failed to read context directory." });
    }
});

// Compile the prompt
app.post('/api/compile', async (req, res) => {
    try {
        const {
            subject, lens, vector, aspectRatio, environment, lighting, phenomena, tokenLock, selectedContexts
        } = req.body;

        let compiledPrompt = `<OMNI_PROMPT>\n`;
        
        // 1. Core Parameters
        compiledPrompt += `  <PARAMETERS>\n`;
        compiledPrompt += `    <SUBJECT>${subject || 'N/A'}</SUBJECT>\n`;
        compiledPrompt += `    <LENS>${lens || 'N/A'}</LENS>\n`;
        compiledPrompt += `    <VECTOR>${vector || 'N/A'}</VECTOR>\n`;
        compiledPrompt += `    <ASPECT_RATIO>${aspectRatio || '16:9'}</ASPECT_RATIO>\n`;
        compiledPrompt += `    <ENVIRONMENT>${environment || 'N/A'}</ENVIRONMENT>\n`;
        compiledPrompt += `    <LIGHTING>${lighting || 'N/A'}</LIGHTING>\n`;
        compiledPrompt += `    <PHENOMENA>${phenomena ? phenomena.join(', ') : 'None'}</PHENOMENA>\n`;
        compiledPrompt += `    <TOKEN_LOCK>${tokenLock || 'N/A'}</TOKEN_LOCK>\n`;
        compiledPrompt += `  </PARAMETERS>\n\n`;

        // 2. Injected Contexts (Directly from FS)
        if (selectedContexts && selectedContexts.length > 0) {
            compiledPrompt += `  <CONTEXT_SOURCES>\n`;
            for (const file of selectedContexts) {
                const filePath = path.join(CONTEXT_DIR, file);
                try {
                    const content = await fs.readFile(filePath, 'utf-8');
                    compiledPrompt += `    <SOURCE file="${file}">\n`;
                    // Escape XML characters just in case
                    const safeContent = content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    compiledPrompt += `      ${safeContent}\n`;
                    compiledPrompt += `    </SOURCE>\n`;
                } catch (readErr) {
                    compiledPrompt += `    <SOURCE file="${file}">ERROR READING FILE</SOURCE>\n`;
                }
            }
            compiledPrompt += `  </CONTEXT_SOURCES>\n`;
        }
        
        compiledPrompt += `</OMNI_PROMPT>`;

        res.json({ result: compiledPrompt });
    } catch (err) {
        console.error("Error compiling prompt:", err);
        res.status(500).json({ error: "Compilation failed." });
    }
});

const PORT = 3001;
app.listen(PORT, () => {
    console.log(`Omni Prompt Studio Backend listening on http://localhost:${PORT}`);
});
