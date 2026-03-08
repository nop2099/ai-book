## AI Has No Concept of Time

Ask an AI for a project plan and you'll often get a clean timeline that has never met a real Tuesday.

The model can sequence dependencies, but it has no lived sense of delay, fatigue, interruptions, or momentum. That's why its time estimates swing wildly in both directions: thirty-minute tasks that take three days, six-week plans finished in one night.

The same gap shows up in daily coaching. "You have three hours left before bed" is technically correct and behaviorally useless if the system can't read what the evening feels like.

I found two practical fixes that help.

First: include explicit timestamps in the operating context. When we started attaching current timestamp metadata to every Kai input, time-related behavior improved immediately. The model stopped free-floating and started reasoning against "now."

Second: force clock checks for time-sensitive answers. In one ChatGPT thread, I repeatedly pushed it to verify current time with an external tool (for example, Python system time) instead of guessing from latent priors. Accuracy improved when the model was required to ground time, not infer it.

For planning work, I use AI for sequence and use human calibration for duration. And for live behavior loops, I prefer short cadence checks over big static schedules. Oracle running every fifteen minutes beat any long-range perfect-looking timeline.

So the rule is simple: treat AI as strong on ordering and weak on felt time. Inject "now" explicitly, verify clocks externally, and keep planning loops short.

---
