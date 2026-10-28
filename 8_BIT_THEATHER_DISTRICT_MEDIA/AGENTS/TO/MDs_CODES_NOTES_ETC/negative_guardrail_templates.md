# PROJECT_NEVERMORE: Character & Visual Continuity Negative Guardrail Templates

This guide provides copy-pasteable, technically calibrated negative prompt templates engineered to act as secondary boundaries in visual diffusion engines. These templates prevent the diffusion scheduler from straying from bound reference tokens, neutralizing visual anomalies such as facial morphing, wardrobe mutations, and background warp.

---

## 1. Vespera's Specialized Star-Pilot Guardrail (Lock Pack)
This template is specifically optimized for **@Vespera** to preserve her unique aesthetic parameters (asymmetrical neon-teal bob, lavender eyes, sharp jawline, and white-and-orange retro-futuristic flight suit) across high-motion sequences in Kling 3.0, Runway Gen-4.5, and Stable Diffusion.

```text
glasses, sunglasses, long hair, symmetrical haircut, symmetrical bob, shifting hair length, changing hair color, shifting jawline, de-aging, baby-face, puffy face, changing clothes, flight suit color shift, shifting piping patterns, missing piping, open collar, disappearing collar, missing badge, black flight suit, extra limbs, blurry limbs, distorted joints, extra fingers, bad hands, malformed hands, flickering cockpit, moving controls, shifting dials, double faces, janus face, 3d-rendered look, video-game graphics
```

### Why this works:
*   **Symmetry Filter:** Explicitly forbidding a "symmetrical bob" and "symmetrical haircut" prevents the model from resolving her asymmetrical teal bob into a standard, uniform haircut.
*   **Suit Integrity:** Hardcoding "flight suit color shift" and "shifting piping patterns" prevents the pristine white fabric from blending with dark cockpit shadows or mutating her orange brass piping into different configurations.
*   **Controls Lock:** Precluding "moving controls" and "shifting dials" ensures the complex, retro-futuristic instrument panels behind her stay static and structurally sound during camera pans.

---

## 2. Core Anomaly Mitigation Templates

These modular blocks can be mixed and matched inside your visual engine's **Negative Elements / Negative Prompt** field depending on the specific rendering requirements of your scene.

### A. Facial Integrity & Identity Lock (Deep Portrait)
*Recommended for close-ups, camera push-ins, and dialogue shots.*
```text
de-aging, morphing features, shifting jawline, facial structure drift, eye color change, asymmetrical eyes, mismatched pupil size, squinting, shifting cheekbones, nose shape mutation, disappearing scars, moving blemishes, glasses, sunglasses, facial hair, beard, moustache, changing hair length, changing hair texture, skin tone shifts, wet skin, sweat, hyper-realistic skin blemishes, plastic skin texture
```

### B. Wardrobe & Accessory Lock (Structural Integrity)
*Recommended for scenes involving intricate garments, mechanical suits, and hand-held props.*
```text
changing clothes, shifting color, suit color shift, disappearing accessories, shifting jewelry, morphing buttons, zipper drift, changing collar height, sleeve length morphing, glove color shift, shifting apparel textures, pocket displacement, disappearing straps, shifting fabric weave, structural simplification, logo mutation
```

### C. Motion & Temporal Stability (Dynamic Sequences)
*Recommended for fast pans, character action shots, and tracking sequences.*
```text
extra limbs, blurry limbs, distorted joints, shifting bone structure, anatomy violations, rubber joints, detached hands, floating fingers, duplicate limbs, clipping clothing, background warping, sliding walls, morphing background objects, camera perspective warp, sliding horizon, background strobe, light flickering, atmospheric warping, periodic rippling, water melting
```

---

## 3. High-Fidelity Genre Configurations

### A. The Fantasy/Cinematic Template
*Focus: Persistent armor plates, fantasy markings, and sword/prop stability.*
```text
modern clothing, sneakers, glasses, shifting armor plating, morphing sword hilt, changing cape color, glowing eyes (unless prompted), disappearing scars, shifting tattoos, flickering jewelry, modern background elements, car, power lines, blurry limbs, extra limbs, distorted weapon, changing hair length
```

### B. The Corporate/Professional Template
*Focus: Clean, consistent talking-head styling.*
```text
glasses, sunglasses, facial hair, beard, changing clothes, suit color shift, missing tie, open collar, messy hair, sweat, skin changes, de-aging, fewer wrinkles, messy office, moving desk items, extra fingers, bad hands, shifting tie patterns
```

---

## 4. Platform-Specific Integration Protocols

### Midjourney V7/V8.1
Midjourney does not have a dedicated negative prompt box, but uses the double hyphen syntax. Append your negative constraints at the very end of your positive camera/action prompt using the `--no` parameter:
```text
[Positive Camera and Motion Prompt] --cref [Vespera_URL] --cw 100 --no glasses sunglasses long hair symmetrical bob changing clothes extra limbs --seed 4567 --ar 16:9
```

### Kling 3.0 Image-to-Video
*   **Positive Box:** Enter only: `[Action] + [Environment] + [Camera Path]` (e.g., *Vespera slowly turns her head to look at the instrument panel, tracking shot, cinematic studio lighting*). Do not re-describe Vespera's physical features.
*   **Negative Box:** Copy and paste the **Vespera Specialized Star-Pilot Guardrail** block.
*   **Subject Binding:** Ensure the master neutral turnaround sheet is active under the Subject Binding settings to lock her mathematical facial keypoints.
