version: "3.1"

rules:
  - rule: fallback for unknown intent
    steps:
      - intent: unknown
      - action: utter_unknown

  - rule: greet user
    steps:
      - intent: greeting
      - action: utter_greeting
