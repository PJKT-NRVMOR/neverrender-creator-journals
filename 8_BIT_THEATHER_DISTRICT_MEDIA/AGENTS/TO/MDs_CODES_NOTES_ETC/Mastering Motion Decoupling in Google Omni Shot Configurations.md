To prevent Google Omni's latent-space physics engine from warping the elevator cabin or failing to align the background movement with the descending motion, you must replace abstract verbs like "descending" with decoupled, relative motion vectors across isolated XML tags.  
Generative video models struggle with nested physical motion (a moving elevator chamber inside a moving shaft) because they rely on learned observation rather than explicit mechanical solvers. When a prompt simply says "the elevator descends," the model's attention layers often experience logical conflicts, causing the interior elevator walls to stretch, morph, or slide downward in tandem with the background.  
By using the Strict Single-Shot Isolation Method and restructuring your XML prompt, you can force the model's attention heads to parse the foreground cabin and the background shaft as separate, independent layers.  
---

1\. The Decoupled Motion Vector Strategy  
To resolve the elevator coordinate conflict, you must translate abstract concepts into explicit pixel-level movement instructions:

* Establish a Static Foreground Anchor: Explicitly prompt that the elevator cabin interior, the control console, and the subject are entirely static and locked-off relative to the camera frame.  
* Establish a Vertical Upward Background Vector: Describe the background outside the elevator's glass viewport as moving continuously upward (the inverse of descending). The upward movement of the shaft walls, pipes, and beams is what mathematically simulates descending velocity without stretching the foreground geometry.  
* Enforce Semantic Tag Isolation: Keep your camera trajectory (which should be locked or experiencing subtle handheld micro-shake) strictly separated from environmental action to prevent motion cues from bleeding together.

---

2\. Calibrated XML Shot Configuration Template  
Here is how you should restructure the XML block inside your source document (Project Nevermore: Cinematic Shot Configuration for The Domicile Descent) to lock the background motion path to the subject's descent:  
\<omni\_shot\_configuration shot\_index="1" duration="6s"\>  
  \<\!-- MODEL IDENTITY ANCHORING & VISUAL LOOKUP \--\>  
  \<model\_provenance\_locking\>  
    \<character\_dna file="character\_consistency\_reference\_guide.pdf"\>  
      Subject: @Vespera. Athletic female pilot, sharp jawline, asymmetrical neon-teal bob haircut, wearing a pristine white retro-futuristic flight suit with orange brass piping and a high collar \[3\].  
    \</character\_dna\>  
    \<continuity\_constraints\>  
      Enforce rigid identity preservation and material permanence. Zero facial morphing, apparel warping, or suit color shifts across the 6-second temporal window \[3\].  
    \</continuity\_constraints\>  
  \</model\_provenance\_locking\>

  \<\!-- ISOLATED CAMERA TRAJECTORY \--\>  
  \<camera\_profile\>  
    \<lens\_configuration\>24mm anamorphic wide-angle probe lens\</lens\_configuration\>  
    \<depth\_of\_field\>Medium shallow focus, keeping the interior cabin cabin-frame sharp while the viewport background drops into smooth bokeh\</depth\_of\_field\>  
    \<trajectory\_vector\>  
      Locked-off, interior-mounted camera perspective. Camera remains 100% stationary relative to the elevator car, with an organic 3% handheld micro-shake for physical realism \[3\].  
    \</trajectory\_vector\>  
  \</camera\_profile\>

  \<\!-- HIGH-CONTRAST 60-30-10 CHROMATIC SEGREGATION \--\>  
  \<color\_grading\_matrix palette\_source="vespera\_color\_palette.json"\>  
    \<base\_architecture weight="60%"\>  
      Elevator cabin interior walls rendered in rigid, matte Deep Slate-Teal (\#124559) and polished Clinical Icy White (\#EAFBFF) paneling to establish an unmoving foreground structure \[8\].  
    \</base\_architecture\>  
    \<dynamic\_energy weight="30%"\>  
      The passing structural beams and mechanical gears visible outside the glass window are illuminated in Electric Cyan (\#00E5FF) and Sunset Gold (\#F59E0B) \[8\].  
    \</dynamic\_energy\>  
    \<disruptive\_pop weight="10%"\>  
      Active terminal interface lights and warning indicators inside the cabin pulsing in hot Coral Red (\#FF6B6B) \[8\].  
    \</disruptive\_pop\>  
  \</color\_grading\_matrix\>

  \<\!-- DECOUPLED PHYSICAL PERFORMANCE AND SCENE MOVEMENT \--\>  
  \<scene\_action\>  
    \<temporal\_flow\>Real-time physical simulation \[8\]\</temporal\_flow\>  
    \<action\_core\>  
      Foreground execution: Vespera stands stationary in the center of the elevator car, her fingers resting lightly on the brass rails, her lavender eyes tracking the console.  
      Background execution: The elevator cabin remains entirely static. Outside the thick, clear glass viewport window, the dark metal industrial shaft structure, cables, and structural floor indicators translate continuously and smoothly in a direct vertical upward direction, simulating a high-velocity descent \[2, 3\].  
    \</action\_core\>  
  \</scene\_action\>  
\</omni\_shot\_configuration\>

---

3\. Verification & Guardrail Checklist

1. Enforce the Anchor-to-Video Rule: Do not generate this shot from a raw text prompt. Initialize the sequence in Google Flow or Kling 3.0 using a high-resolution visual starting keyframe (such as a Photoshop render of the elevator interior) to give the diffusion layers a rigid spatial map of the cabin boundaries.  
2. Solder the Negative Prompt Barrier: Copy and paste your standard structural negative prompt block directly into the generation pipeline's negative elements field to suppress temporal artifacting:  
3. Leverage the 6-Second Temporal Sweet Spot: Ensure your clip is scheduled for exactly 6.0 seconds rather than 4.0. Pushing the clip duration to 6 seconds grants Omni's autoregressive attention heads the necessary "breathing room" to distribute the motion math, drastically increasing background-to-foreground tracking fidelity.

👉 Would you like me to map out a transitional Shot 2 cutaway sequence (like a tight macro shot of the elevator's floor indicator dial spinning) to help mask the transition when Vespera reaches her terminal destination?  
