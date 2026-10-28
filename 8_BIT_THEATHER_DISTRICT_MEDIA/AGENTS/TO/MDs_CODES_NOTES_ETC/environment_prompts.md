# PROJECT_NEVERMORE: Surreal Futurist Environment Prompts & Rendering Presets
*System Status: Cemented // Production Matrix Active*  
*Metadata Standard: C2PA v1.3 Enabled*

This reference guide provides copy-pasteable, technically calibrated rendering prompts for the five primary chromatic systems of **PROJECT_NEVERMORE**. 

To prevent neural engines from randomly blending colors (a bug known as "attribute bleed"), these prompts are structured using **unpunctuated, constraint-based text strings** that isolate geometry, textures, lighting, and color percentages.

---

<!-- STREAMING_CHUNK:Writing Section 1: Prompting Syntax Guidelines... -->
## SECTION 1: The 60-30-10 Prompting Syntax

When prompting generative models (like Midjourney, DALL-E 3, or Stable Diffusion), describing a scene poetically (e.g., "a teal room with orange lights and coral details") causes the model to mix the colors unpredictably, resulting in blue skin or orange metal. 

To enforce strict color distribution, structure your prompts into four isolated constraint fields:

```
[Camera & Lens Geometry] + [Aerodynamic / Parametric Structural Assets] + [60-30-10 Chromatic Constraints] + [Engine Render Settings]
```

*   **Camera & Lens Geometry:** Simulates high-end, shallow-focus photography (e.g., tilt-shift, macro, round geometric bokeh) to isolate structural targets.
*   **Structural Assets:** Defines the physical curves, cantilevers, and heavy machinery inspired by Syd Mead, Chris Foss, and Zaha Hadid.
*   **Chromatic Constraints:** Specifies exact hex codes, color roles, and spatial surface-area allocations as direct physical rendering commands.
*   **Engine Render Settings:** Sets seed locks, scale parameters, and negative guardrails to prevent stochastic hallucinations.

---

<!-- STREAMING_CHUNK:Writing Section 2: Chromatic Environment Presets... -->
## SECTION 2: Canonical Chromatic Presets

### Preset 1: The Chrono-Port Terminal (NeverRender Labs Matrix)
*   **Aesthetic:** Clinical, heavy-industrial sci-fi with glowing diagnostics.
*   **Ratios:** 60% Deep Slate-Teal/Icy White, 30% Electric Cyan/Jade Teal, 10% Coral Pink-Red.

#### Midjourney V7 / V8.1 Prompt:
> Wide-angle interior shot of a soaring Chrono-Port hangar with Zaha Hadid curvilinear bulkheads and Chris Foss style industrial pipes, 60 percent of the scene is rendered in deep slate-teal (#124559) metal panels and clinical icy white floor tiles, 30 percent of the scene is glowing electric cyan (#00E5FF) and jade teal (#00C49A) diagnostics conduits running along the ceiling, 10 percent of the scene is sharp coral pink-red (#FF6B6B) terminal warning lights flashing on the interfaces, tilt-shift lens, sharp focus, atmospheric haze, volumetric sunset light rays streaming through the curved glass viewport --ar 16:9 --style raw --seed 4567

#### DALL-E 3 Prompt:
> An ultra-detailed wide-angle interior of a retro-futuristic hangar terminal. The architecture features sweeping curvilinear slate-teal panels and polished white floor tiles making up sixty percent of the image. Active power grids and conduit lines glowing with intense electric cyan and jade teal lights trace the ceiling and column outlines making up thirty percent of the image. Small sharp coral pink-red warning lights on terminal consoles provide a high-contrast accent of ten percent. Shot with a high-end camera lens simulating a shallow depth of field, warm golden sunset light streaming through a curved glass viewport creating beautiful lens flares and a cinematic atmosphere.

---

### Preset 2: The Vapor-Beach Observatory (Pastel Glow Matrix)
*   **Aesthetic:** Soft, dreamy, alien coastal ecology with mineral refractions.
*   **Ratios:** 60% Soft Peach-White, 30% Mint Turquoise, 10% Bright Lavender.

#### Midjourney V7 / V8.1 Prompt:
> Shallow depth of field macro shot of an aerodynamic observation pod on an alien beach, 60 percent of the frame is soft peach-white (#F4F4F4) polymer bulkheads and weathered sand, 30 percent of the frame is mint turquoise (#00F5D4) ocean waves cresting under a dual sun, 10 percent of the frame is bright lavender (#9B5DE5) opalescent crystals refracting light on the console deck, Moebius watercolor aesthetic, clean outlines, pastel neon grading, round geometric bokeh, hyper-detailed textures --ar 16:9 --style raw --seed 4567

#### DALL-E 3 Prompt:
> A soft dreamy illustration of a retro-futuristic beach observatory. The structure is built with smooth peach-white polymer curves and sits on soft beach sand covering sixty percent of the composition. The ocean waves and dynamic sky glow with a soft mint turquoise covering thirty percent. Glimmering bright lavender opalescent crystals are clustered in the foreground around a metallic hatch covering ten percent. The art style combines clean comic-book ink outlines with soft watercolor airbrush gradients, beautiful round bokeh circles in the soft focus background.

---

### Preset 3: The Virtual Core Corridor (Neon Night Matrix)
*   **Aesthetic:** High-contrast, glowing dystopian digital mainframe.
*   **Ratios:** 60% Midnight Black, 30% Intense Cyber-Cyan, 10% Electric Magenta.

#### Midjourney V7 / V8.1 Prompt:
> Low-angle tracking shot down a narrow cybernetic server corridor, 60 percent of the frame is matte midnight black (#100E2C) acoustic dampening panels and dark metal grids, 30 percent of the frame is intense cyber-cyan (#333D94) server racks and light guide strips lining the walls, 10 percent of the frame is electric magenta (#D41E79) data stream indicators flashing on the interfaces, synthwave aesthetic, high contrast, crisp ultraviolet neon reflections on wet steel floor plates, sharp perspective lines --ar 16:9 --style raw --seed 4567

#### DALL-E 3 Prompt:
> A high-contrast synthwave digital hallway. The walls and ceiling are constructed of matte midnight black panels and dark iron floor grates covering sixty percent of the scene. Glowing lines and arrays of server blocks emit a bright cyber-cyan neon light covering thirty percent of the scene. High-contrast electric magenta flashes from fiber-optic cable nodes provide ten percent accent dots. Crisp reflections of the ultraviolet light bounce off the wet metallic floor, creating deep shadows and an immersive, technologically saturated atmosphere.

---

### Preset 4: The Streamlined Machining Bay (Metallic Past Matrix)
*   **Aesthetic:** Timeless, polished space-age industrial design.
*   **Ratios:** 60% Antique Cream, 30% Silver-Gray Chrome, 10% Burnished Bronze.

#### Midjourney V7 / V8.1 Prompt:
> Eye-level shot of a streamlined vehicle assembly bay, 60 percent of the scene is smooth antique cream (#EDE6D6) enamel walls and retro-modern curved panels, 30 percent of the scene is mirror-polished silver-gray (#B88B5B) chrome levers and exposed hydraulic struts, 10 percent of the scene is warm burnished bronze (#C0C0C0) heavy structural rivets and joint rings, Syd Mead design aesthetic, pristine lighting, realistic metal reflections, sharp geometric shapes, industrial portfolio style --ar 16:9 --style raw --seed 4567

#### DALL-E 3 Prompt:
> A clean retro-futuristic workshop from the 1960s Space Age. The walls and large curved storage cabinets are painted in a smooth matte antique cream enamel making up sixty percent of the room. Polished silver-gray chrome hydraulic pistons, levers, and metal tabletops glint under bright workshop lights making up thirty percent. The joints of the heavy machinery and structural bolts are made of warm burnished bronze covering ten percent of the frame. The rendering has a smooth airbrush texture and clean geometric forms.

---

### Preset 5: The Subconscious Observatory (Dream Realism Matrix)
*   **Aesthetic:** Illogical, painterly landscape where sky and interior merge.
*   **Ratios:** 60% Sandy Yellow/Burnt Orange, 30% Soft Sky-Blue, 10% Rich Earth-Brown.

#### Midjourney V7 / V8.1 Prompt:
> Wide landscape shot of an open-air observatory where the ceiling is a melting clockwork sky, 60 percent of the frame is hazy sandy yellow (#D9D3B4) cracked earth and burnt orange (#D97C2B) twilight clouds, 30 percent of the frame is a soft sky-blue (#3698BF) ocean water pooling inside the building's floor basins, 10 percent of the frame is rich earth-brown (#441D0D) stone monoliths and antique mechanical dials, Salvador Dali dream realism style, oil painting texture, classical depth, surreal atmosphere, soft warm shadows --ar 16:9 --style raw --seed 4567

#### DALL-E 3 Prompt:
> A surrealist dreamscape painting of an astronomical observatory. Sixty percent of the canvas is covered in warm sandy yellow cracked earth and swirling burnt orange clouds in a twilight sky. A calm pool of soft sky-blue water occupies the interior floor channels of the temple ruins covering thirty percent. Intricately carved stone columns and heavy dials in rich earth-brown are placed in the foreground covering ten percent. The artwork has a detailed oil on canvas texture with long, dramatic shadows and a hazy, mystical atmosphere.

---

<!-- STREAMING_CHUNK:Writing Section 3: Platform Specific Controls... -->
## SECTION 3: Platform Integration Guidelines

### 1. Midjourney V7 / V8.1 Parameters
*   **Style Reference (`--sref`):** Once you generate a master environment using one of the prompts above, upscale it and use its URL in subsequent prompts: `--sref [Env_URL]`. This forces Midjourney to replicate the exact material luster, noise level, and lighting vectors.
*   **Style Weight (`--sw`):** Keep this at `--sw 100` (default) for standard continuity. Push it to `--sw 250` if the engine is attempting to replace your colors with generic sci-fi blue/orange.
*   **Seed Control (`--seed`):** Lock the seed to `--seed 4567` across your scene storyboard to prevent camera cutting from shifting the basic layout of background structures.

### 2. DALL-E 3 Conversation Locks
*   DALL-E 3 is prone to rewriting prompts through ChatGPT, which breaks the precise hex-code designations. To prevent this, always prefix your DALL-E requests with this command:
    > "Translate this prompt verbatim to DALL-E 3. Do not add, remove, or modify any words, and preserve all hexadecimal color codes exactly."
*   **Attribute Control:** Never use commas inside your character descriptions when combining them with these environments. Commas cause the model's text parser to split the subject from its surroundings, leaking the environment colors onto the character’s clothing or skin.

### 3. Stable Diffusion / ComfyUI Conditioning
*   **IP-Adapter:** When rendering a character inside these environments, run a dual IP-Adapter pipeline:
    1.  **IP-Adapter FaceID** (using your character pack reference at weight `0.6` to lock face bone-structure).
    2.  **IP-Adapter Standard** (using your upscaled environment keyframe at weight `0.4` connected strictly to the background latent zone).
*   **Contrastive Alignment (PuLID):** To guarantee your background's Moebius twilight colors do not leak onto Vespera's white flight suit, load Vespera's turnaround sheet into a **PuLID node** paired with an Eva-CLIP encoder. This ensures identity insertion without background style contamination.
