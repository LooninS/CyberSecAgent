---
name: Ghost Protocol
colors:
  surface: '#0b1229'
  surface-dim: '#0b1229'
  surface-bright: '#323851'
  surface-container-lowest: '#060d23'
  surface-container-low: '#141a31'
  surface-container: '#181e36'
  surface-container-high: '#232941'
  surface-container-highest: '#2d344c'
  on-surface: '#dce1ff'
  on-surface-variant: '#b9cacb'
  inverse-surface: '#dce1ff'
  inverse-on-surface: '#292f47'
  outline: '#849495'
  outline-variant: '#3b494b'
  surface-tint: '#00dbe9'
  primary: '#dbfcff'
  on-primary: '#00363a'
  primary-container: '#00f0ff'
  on-primary-container: '#006970'
  inverse-primary: '#006970'
  secondary: '#ecb1ff'
  on-secondary: '#520070'
  secondary-container: '#d05bff'
  on-secondary-container: '#480063'
  tertiary: '#f8f4ff'
  on-tertiary: '#302f39'
  tertiary-container: '#dbd8e4'
  on-tertiary-container: '#5f5e68'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#7df4ff'
  primary-fixed-dim: '#00dbe9'
  on-primary-fixed: '#002022'
  on-primary-fixed-variant: '#004f54'
  secondary-fixed: '#f9d8ff'
  secondary-fixed-dim: '#ecb1ff'
  on-secondary-fixed: '#320046'
  on-secondary-fixed-variant: '#75009e'
  tertiary-fixed: '#e4e1ed'
  tertiary-fixed-dim: '#c8c5d1'
  on-tertiary-fixed: '#1b1b23'
  on-tertiary-fixed-variant: '#47464f'
  background: '#0b1229'
  on-background: '#dce1ff'
  surface-variant: '#2d344c'
typography:
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 42px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.05em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  terminal-code:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: 0.05em
  body-main:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: 0em
  label-caps:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: 0.15em
spacing:
  grid-unit: 4px
  gutter: 16px
  margin: 24px
  terminal-gap: 8px
---

## Brand & Style

The design system is engineered to evoke the sensation of a high-tier hacking operative’s workspace: cold, efficient, and technologically superior. It targets a sophisticated power-user audience who values information density over decorative fluff. The aesthetic is a precise blend of **Minimalist Cyberpunk** and **Glassmorphism**, moving away from "dirty" retro-futurism toward a "clean-room" digital environment.

The emotional response should be one of "controlled chaos"—where vast amounts of data are organized into a lethal, streamlined interface. Visual depth is achieved through holographic layering, while micro-interactions utilize subtle RGB shifts and "glitch" frames to remind the user of the volatile nature of the data they are manipulating.

## Colors

The palette is anchored in the deep void of cyberspace. The foundation consists of `Midnight Navy (#05050A)` and `Pure Black (#000000)`, providing the necessary contrast for luminous elements. 

- **Primary (Electric Cyan):** Used for critical data paths, active terminal cursors, and primary actionable items.
- **Secondary (Cyber Violet):** Reserved for high-priority alerts, encryption status, and specialized agent tools.
- **Neutral:** A range of desaturated blues and greys used for non-essential telemetry and background grid lines.
- **Functional States:** Success is rendered in a sharp emerald green, while errors utilize a high-saturation red with a slight violet tint to maintain palette harmony.

## Typography

The typography utilizes **Space Grotesk** across all levels to maintain a technical, geometric rigor that feels "engineered." While traditionally a sans-serif, its idiosyncratic terminal ends and wide stance provide the futuristic, monospaced-adjacent feel required for a hacking agent interface without sacrificing readability in dense data sets.

All labels should be set in uppercase with increased letter-spacing to mimic military telemetry. Code blocks and data readouts use the same family but strictly adhere to a rigid vertical rhythm to simulate a terminal environment.

## Layout & Spacing

This design system employs a **Modular Terminal Grid**. The layout is divided into a 12-column master grid, but internal components function as "tiles" that snap to a 4px baseline. 

Layouts should feel like a modular dashboard where panels can be resized or rearranged. Use "Scanline" padding—vertical spacing is slightly tighter than horizontal spacing—to emphasize the horizontal flow of code readouts. Gutters are kept thin (16px) to maximize screen real estate, creating an "edge-to-edge" information density.

## Elevation & Depth

Depth is conveyed through **Holographic Glassmorphism**. Elements do not cast traditional black shadows; instead, they utilize "Backdrop Glows" and "Internal Refraction."

1.  **Base Layer:** The darkest midnight navy, acting as the void.
2.  **Modular Panels:** 40% opacity navy with a 20px backdrop blur and a 1px inner border in 20% white to simulate a glass edge.
3.  **Active Elements:** These carry a subtle "outer glow" using the primary cyan or secondary violet, suggesting a light-emitting display.
4.  **Floating Modals:** These use a higher blur (40px) and a distinct "glitch" border—a 2px offset line in a contrasting accent color to suggest the window is being projected into 3D space.

## Shapes

The shape language is strictly **Sharp (0px)**. Rounded corners are avoided to maintain an aggressive, industrial aesthetic. To break the monotony of rectangles, use "clipped corners" (45-degree chamfers) on primary buttons and container headers. This geometric "stealth" styling reinforces the hacking agent narrative, suggesting hardware that is built for utility and speed over comfort.

## Components

### Buttons & Inputs
Buttons are ghost-styled with 1px borders. On hover, they should fill with a semi-transparent tint of the accent color and trigger a 100ms "chromatic aberration" glitch effect where the text appears to split into RGB components. Input fields are simple underlines or full-width boxes with no background, using a blinking block cursor.

### Chips & Tags
Chips are used for "Status Telemetry." They should look like miniature hardware modules with a small status LED (glow circle) on the left side.

### Terminal Lists
Lists do not use alternating row colors. Instead, they use a subtle horizontal "scanline" texture (1px lines every 4px) and a high-contrast hover state that highlights the entire row in a transparent violet.

### Data Visualization
Charts must avoid solid fills. Use wireframes, dotted lines, and "pulse" animations for data points. All graphs should have a faint grid background that aligns with the master spacing system.

### Additional Elements
- **Scanlines:** A global, low-opacity overlay of horizontal lines to simulate a CRT/High-res HUD.
- **Brackets:** Use `[ ]` characters around active navigation items instead of traditional underlines.
- **Node Map:** A specialized component for visualizing network connections, using thin cyan lines and violet nodes.