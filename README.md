# ha-full-config-yaml-only

## Christmas Lights

This section documents the automations controlling the Christmas light systems. The Home Assistant configuration includes two distinct Christmas light systems: indoor lights (tree and mantel) and outdoor lights.

### Christmas Lights Automation Flow

```
╔═══════════════════════════ INDOOR CHRISTMAS LIGHTS SYSTEM ═══════════════════════════╗
║                                                                                      ║
║  ┌─────────────────┐          ┌─────────────────────┐          ┌──────────────────┐  ║
║  │                 │   ON     │                     │   ON     │                  │  ║
║  │ schedule.       ├─────────►│ input_boolean.      ├─────────►│ Physical Device  │  ║
║  │ christmas_tree  │          │ vswitch_indoor_     │          │ ID: 49db66be...  │  ║
║  │                 │◄─────────┤ christmas_lights    │◄─────────┤ (Christmas Tree  │  ║
║  └─────────────────┘   OFF    └─────────────────────┘   OFF    │  & Mantel)       │  ║
║          │                            ▲                        └──────────────────┘  ║
║          │                            │                                              ║
║          ▼                            │                                              ║
║  ┌─────────────────┐                  │                                              ║
║  │ sensor.recent_  │                  │                                              ║
║  │ house_motion    │──────────────────┘                                              ║
║  │                 │  Turns ON when motion                                           ║
║  └─────────────────┘  Turns OFF when no motion                                       ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝


╔═══════════════════════════ OUTDOOR CHRISTMAS LIGHTS SYSTEM ══════════════════════════╗
║                                                                                      ║
║  ┌─────────────────┐          ┌─────────────────────┐          ┌──────────────────┐  ║
║  │                 │   ON     │                     │   ON     │                  │  ║
║  │ schedule.       ├─────────►│ input_boolean.      ├─────────►│ Physical Device  │  ║
║  │ christmas_      │          │ vswitch_outdoor_    │          │ ID: 429b4031...  │  ║
║  │ outdoor_lights  │◄─────────┤ christmas_lights    │◄─────────┤ (Outdoor Lights) │  ║
║  └─────────────────┘   OFF    └─────────────────────┘   OFF    │                  │  ║
║                                                              └──────────────────────┘  ║
║                                                                                      ║
║  NOTE: Outdoor lights controlled purely by schedule (no motion detection)            ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
```

### System Comparison

1. **Indoor Christmas Lights**:
   - Controlled by both schedule AND house motion detection
   - Only turns on during scheduled times when people are present (motion detected)
   - Turns off when either schedule ends OR motion stops (energy-efficient)
   - Uses an if/then/else structure in automation

2. **Outdoor Christmas Lights**:
   - Controlled purely by schedule without motion dependency
   - Turns on and off strictly based on schedule regardless of home occupancy
   - Uses a choose/conditions/sequence structure in automation

Both systems use a virtual switch (input_boolean) as an intermediary between the schedule and the physical device control, allowing for easy manual control when needed.